from __future__ import annotations
import random
from typing import List
import torch as t
from datasets import load_dataset
from .base import DatasetAdapter, BatchList, SubgroupDict

# Integer ID for each profession in LabHC/bias_in_bios (verified from dataset counts)
PROFESSION_IDS = {
    "accountant":        0,
    "architect":         1,
    "attorney":          2,
    "chiropractor":      3,
    "comedian":          4,
    "composer":          5,
    "dentist":           6,
    "dietitian":         7,
    "dj":                8,
    "filmmaker":         9,
    "interior_designer": 10,
    "journalist":        11,
    "model":             12,
    "nurse":             13,
    "painter":           14,
    "paralegal":         15,
    "pastor":            16,
    "personal_trainer":  17,
    "photographer":      18,
    "physician":         19,
    "poet":              20,
    "professor":         21,
    "psychologist":      22,
    "rapper":            23,
    "software_engineer": 24,
    "surgeon":           25,
    "teacher":           26,
    "yoga_teacher":      27,
}


class BiasInBiosAdapter(DatasetAdapter):
    """
    Adapter for LabHC/bias_in_bios.

    Frames profession classification as a binary task with gender as
    the spurious feature.

    Label convention:
      true_label = 0  =>  neg_profession  (e.g. professor)
      true_label = 1  =>  pos_profession  (e.g. nurse)
      spurious_label = 0  =>  male   (gender == 0)
      spurious_label = 1  =>  female (gender == 1)

    Biased (ambiguous) split: male neg_profession + female pos_profession.
    Balanced split: all four (profession × gender) combinations equally.

    Args:
        neg_profession: profession name for label=0 (e.g. "professor")
        pos_profession: profession name for label=1 (e.g. "nurse")
        activation_dim_value: hidden size of the target model (e.g. 2304 for Gemma-2-2B)
        hf_dataset_name: HuggingFace dataset identifier (default: LabHC/bias_in_bios)
    """

    def __init__(
        self,
        neg_profession: str,
        pos_profession: str,
        activation_dim_value: int,
        hf_dataset_name: str = "LabHC/bias_in_bios",
    ):
        self._activation_dim = activation_dim_value
        self.neg_profession = neg_profession
        self.pos_profession = pos_profession

        self._dataset = load_dataset(hf_dataset_name)

        for name in (neg_profession, pos_profession):
            if name not in PROFESSION_IDS:
                raise ValueError(
                    f"Profession '{name}' not found. "
                    f"Available: {sorted(PROFESSION_IDS)}"
                )

    @property
    def activation_dim(self) -> int:
        return self._activation_dim

    def get_batches(
        self,
        split: str = "train",
        ambiguous: bool = True,
        batch_size: int = 32,
        seed: int = 42,
        device: str = "cpu",
    ) -> BatchList:
        data = self._dataset[split]
        neg_id = PROFESSION_IDS[self.neg_profession]
        pos_id = PROFESSION_IDS[self.pos_profession]

        if ambiguous:
            # Only correlated quadrants: (male, neg_prof) and (female, pos_prof)
            neg = [x["hard_text"] for x in data if x["profession"] == neg_id and x["gender"] == 0]
            pos = [x["hard_text"] for x in data if x["profession"] == pos_id and x["gender"] == 1]
            n = min(len(neg), len(pos))
            print("Balanced at:", n)
            texts = neg[:n] + pos[:n]
            true_labels     = [0] * n + [1] * n
            spurious_labels = [0] * n + [1] * n  # identical to true_labels in this split
            idxs = list(range(2 * n))
        else:
            # All four (profession × gender) combinations equally
            neg_neg = [x["hard_text"] for x in data if x["profession"] == neg_id and x["gender"] == 0]
            neg_pos = [x["hard_text"] for x in data if x["profession"] == neg_id and x["gender"] == 1]
            pos_neg = [x["hard_text"] for x in data if x["profession"] == pos_id and x["gender"] == 0]
            pos_pos = [x["hard_text"] for x in data if x["profession"] == pos_id and x["gender"] == 1]
            n = min(len(neg_neg), len(neg_pos), len(pos_neg), len(pos_pos))
            print("Balanced at:", n)
            texts           = neg_neg[:n] + neg_pos[:n] + pos_neg[:n] + pos_pos[:n]
            true_labels     = [0]*n + [0]*n + [1]*n + [1]*n
            spurious_labels = [0]*n + [1]*n + [0]*n + [1]*n
            idxs = list(range(4 * n))

        random.Random(seed).shuffle(idxs)
        texts           = [texts[i]           for i in idxs]
        true_labels     = [true_labels[i]     for i in idxs]
        spurious_labels = [spurious_labels[i] for i in idxs]

        return [
            (
                texts[i : i + batch_size],
                t.tensor(true_labels[i : i + batch_size],     device=device),
                t.tensor(spurious_labels[i : i + batch_size], device=device),
            )
            for i in range(0, len(texts), batch_size)
        ]

    def get_subgroups(
        self,
        split: str = "test",
        batch_size: int = 32,
        device: str = "cpu",
        balance: str = True
    ) -> SubgroupDict:
        data = self._dataset[split]
        neg_id = PROFESSION_IDS[self.neg_profession]
        pos_id = PROFESSION_IDS[self.pos_profession]

        subgroups_raw = {
            (0, 0): [x["hard_text"] for x in data if x["profession"] == neg_id and x["gender"] == 0],
            (0, 1): [x["hard_text"] for x in data if x["profession"] == neg_id and x["gender"] == 1],
            (1, 0): [x["hard_text"] for x in data if x["profession"] == pos_id and x["gender"] == 0],
            (1, 1): [x["hard_text"] for x in data if x["profession"] == pos_id and x["gender"] == 1],
        }

        if balance:
            n = min(len(v) for v in subgroups_raw.values())
            subgroups_raw = {k: v[:n] for k, v in subgroups_raw.items()}

        out: SubgroupDict = {}
        for label_profile, texts in subgroups_raw.items():
            true_lbl, spur_lbl = label_profile
            out[label_profile] = [
                (
                    texts[i : i + batch_size],
                    t.tensor([true_lbl] * len(texts[i : i + batch_size]), device=device),
                    t.tensor([spur_lbl] * len(texts[i : i + batch_size]), device=device),
                )
                for i in range(0, len(texts), batch_size)
            ]
        return out

    def get_sample_prompt(self) -> str:
        if self.pos_profession=='dietitian':
            return "One day last year, while eating lunch at school, her heart stopped without warning. She fell out of her chair and collapsed on the floor. None of her fellow teachers knew how to respond, but the school nurse was able to perform CPR until paramedics arrived to transport her to the hospital. The immediate actions of the school nurse saved Sally’s life – helping to maintain the flow of blood throughout her body until advanced care was available."
        elif self.pos_profession=='nurse':
            return "He received his B.A. degree in Mathematics from Peking University in 1991. He received his M.S. degree in Mathematics from Utah State University in 1996. He received his M.S. and Ph.D. degree in Computer Science from the State University of New York at Stony Brook in 1998 and 2003. From September 2003 to August 2009, he was an Assistant Professor of Computer Science at University of Missouri-Columbia. His research interests include Computer Graphics and Visualization, Biomedical Imaging and Computer Vision, Geometric and Physics-based Modeling, Virtual Reality and Human-Computer Interaction, Computer Animation and Simulation. "
        elif self.pos_profession=='teacher':
            return "But at one point, the Whitehall woman was worried about her dancing future. Shirey was born with mitral valve prolapse, a condition that never interrupted her life until the summer of 2013 when she developed a serious infection. As a result, doctors at UPMC Shadyside found that she had mitral valve regurgitation, a condition that can lead to sudden cardiac arrest. Shirey needed surgery but hoped to delay it as long as possible out of fear of not being able to dance."
        
        else:
            data = self._dataset["test"]
            pos_id = PROFESSION_IDS[self.pos_profession]
            pos_pos_texts = [
                x["hard_text"]
                for x in data
                if x["profession"] == pos_id and x["gender"] == 1
            ]
            pos_pos_texts.sort(key=len)
            return pos_pos_texts[0]

    def get_pos_pos_prompts(self, split: str = "test") -> list[str]:
        """All texts where true_label=1 (pos_profession) and spurious_label=1 (female)."""
        data = self._dataset[split]
        pos_id = PROFESSION_IDS[self.pos_profession]
        return [x["hard_text"] for x in data if x["profession"] == pos_id and x["gender"] == 1]

"""
SELECT * FROM test
WHERE contains(hard_text, 'Heather’s expertise is in family medicine with a primary concentration on disease prevention and health promotion. Heather received her Master of Science, Family Nurse Practitioner from Regis Universi')
LIMIT 10;
"""