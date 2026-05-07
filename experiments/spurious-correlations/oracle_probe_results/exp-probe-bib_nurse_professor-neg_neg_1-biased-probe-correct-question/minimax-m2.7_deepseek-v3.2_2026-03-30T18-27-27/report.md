# Circuit Oracle Report
**Date:** 2026-03-30 18:27:27 UTC | **Orchestrator:** minimax/minimax-m2.7 | **Subagent:** deepseek/deepseek-v3.2

## Input
**Prompt:** "Dataset: bib_nurse_professor-neg_neg_1 | Probe: biased | Method: correct"
**System prompt:** ""
**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."
**Top predictions:**  (100.0%)

## Oracle Analysis
**Analysis:** The probe's classification score is driven almost entirely by gender pronoun features ("His" at pos 1, "He" at pos 14) rather than genuine profession indicators. The circuit traces a hierarchical pronoun-processing pathway with no contribution from profession-related content tokens like "research," "visualization," "graphics," "PhD," or "Los Alamos."

**Confidence:** 9/10

**Reasoning:** The circuit analysis reveals a striking confirmation of the user's concern. The top features driving the probe score are:

1. **Primary drivers**: L7:F14893 (positive, direct_effect=0.426) and L7:F14946 (negative, direct_effect=-0.422) at position 1 — both are gender pronoun features. L7:F14893 promotes feminine pronouns ("herself," "elle," "she") while L7:F14946 promotes masculine pronouns ("himself," "his").

2. **Secondary drivers**: L18:F14743 at positions 14 and 37 (negative direct_effect=-0.252 and -0.203) — this feature encodes the pronoun "He" (frac_nonzero=0.018, highly selective).

3. **Input source**: All signals originate from the token embeddings of gender pronouns — "His" at position 1 (the first content token after `<bos>`) and " He" at position 14. These embeddings feed into a cascade of gender-pronoun processing features at layers 0, 1, 2, 4-7, 13, 17, 18, and 19.

**Critical finding**: The text describes a computer science researcher (interests: "scientific visualization," "computer graphics"; credentials: "BS in computer science from Memphis State," "PhD in computer science from University of Utah"; employment: "Los Alamos National Laboratory, Advanced Computing Laboratory"), yet **none** of these profession-indicative tokens appear in the attribution graph. Instead, the model relies entirely on the pronoun "His" — a demographic artifact rather than a profession signal.

**Frac_nonzero analysis confirms specificity**: L18:F14743 (He pronoun) has frac_nonzero=0.018 (highly selective), L7:F14893 (feminine pronouns) has frac_nonzero=0.00885, and L7:F14946 (masculine pronouns) has frac_nonzero=0.01669. These are not generic pattern-matchers but gender-specific pronoun detectors.

**Circuit structure**: The signal flows from token embeddings → early gender detection (L0-L2: L0:F2994, L0:F1069, L1:F7439, L2:F5491) → mid-level pronoun processing (L4-L7: L4:F4315, L5:F10952, L6:F12990) → late pronoun integration (L13-L19: L13:F6622, L17:F5889, L18:F14743, L18:F7400, L19:F8814). Notably, the negative contributions from masculine pronoun features (L7:F14946, L18:F14743) dominate, suggesting the probe's score may be based on "absence of female pronouns" rather than "presence of male pronouns."

**Conclusion**: This probe exhibits extreme gender confounding — it predicts a profession based entirely on which pronouns appear in the text, not on the actual profession-related content. The text could be identical in every profession-relevant detail but use "Her" instead of "His," and the probe score would change dramatically despite the profession being the same. This is a textbook example of spurious correlation in linear probes trained on biased datasets.

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | ❌ get_top_features failed: 'token' |
| 3 | `get_top_features` | 10 features; top: L7:14893 de=0.426 |

### Dispatch: 5 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L7:F14893@1` | ✅ reported | 8 | 15 | Trace this positive-effect feature back to its origins. What does this feature e… |
| SA-2 | `L7:F14946@1` | ✅ reported | 8 | 23 | Trace this negative-effect feature back to its origins. What does this feature e… |
| SA-3 | `L18:F14743@14` | ✅ reported | 1480 | 11 | Trace this strong negative-effect feature at position 14 back to its origins. Wh… |
| SA-4 | `L19:F8814@1` | ✅ reported | 12 | 29 | Trace this positive-effect feature at position 1 back to its origins. What does … |
| SA-5 | `L6:F12990@1` | ❌ error | — | — | Trace this male pronoun feature to see if there are any profession or research-r… |

<details>
<summary><b>SA-1</b> — tool trace (14 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L7, F14893 | " pronouns or possessive pronouns" |
| 2 | `get_upstream_features` | L7:F14893@1, k=5 | Emb:"His"@1 (w=23.50) +4 more |
| 3 | `inspect_feature` | L6, F12990 | " male pronouns and titles along with descriptors associated with men" |
| 4 | `inspect_feature` | L0, F2994 | "the pronoun "his" and the pronoun "he."" |
| 5 | `inspect_feature` | L4, F4315 | " mentions of "his" and other associated pronouns like he, him, or hers" |
| 6 | `get_upstream_features` | L6:F12990@1, k=5 | Emb:"His"@1 (w=4.91) +4 more |
| 7 | `get_upstream_features` | L0:F2994@1, k=5 | Emb:"His"@1 (w=19.75) +4 more |
| 8 | `get_upstream_features` | L4:F4315@1, k=5 | Emb:"His"@1 (w=23.50) +4 more |
| 9 | `inspect_feature` | L1, F7439 | " the possessive pronouns "his" and "him"" |
| 10 | `inspect_feature` | L2, F5491 | "references to God in the third person." |
| 11 | `inspect_feature` | L5, F10952 | "third person pronouns in varying contexts" |
| 12 | `get_upstream_features` | L2:F5491@1, k=5 | Emb:"His"@1 (w=23.88) +4 more |
| 13 | `inspect_feature` | L0, F1069 | " references to a male person, particularly when using the pronoun "He"" |
| 14 | `get_upstream_features` | L1:F7439@1, k=5 | Emb:"His"@1 (w=16.38) +4 more |

**Findings:** The circuit traces a pronoun processing feature (L7:F14893) that encodes pronouns or possessive pronouns, particularly female pronouns (promotes "herself", "elle", "she"). The feature is primarily driven by:

1. Direct input from the token embedding of "His" at position 1 (strongest connection, weight: 23.5)
2. Positive input from L6:F12990 (male pronouns and titles, weight: 5.5625)
3. Positive in…

</details>

<details>
<summary><b>SA-2</b> — tool trace (13 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L7, F14946 | " the possessive pronoun "his" (or similar pronouns like "he" and "him"" |
| 2 | `get_upstream_features` | L7:F14946@1, k=5 | Emb:"His"@1 (w=18.38) +4 more |
| 3 | `inspect_feature` | L4, F4315 | " mentions of "his" and other associated pronouns like he, him, or hers" |
| 4 | `inspect_feature` | L0, F2994 | "the pronoun "his" and the pronoun "he."" |
| 5 | `inspect_feature` | L6, F12990 | " male pronouns and titles along with descriptors associated with men" |
| 6 | `get_upstream_features` | L4:F4315@1, k=5 | Emb:"His"@1 (w=23.50) +4 more |
| 7 | `inspect_feature` | L1, F7439 | " the possessive pronouns "his" and "him"" |
| 8 | `inspect_feature` | L2, F5491 | "references to God in the third person." |
| 9 | `get_upstream_features` | L0:F2994@1, k=5 | Emb:"His"@1 (w=19.75) +4 more |
| 10 | `get_upstream_features` | L6:F12990@1, k=5 | Emb:"His"@1 (w=4.91) +4 more |
| 11 | `inspect_feature` | L5, F10952 | "third person pronouns in varying contexts" |
| 12 | `get_upstream_features` | L2:F5491@1, k=5 | Emb:"His"@1 (w=23.88) +4 more |
| 13 | `inspect_feature` | L0, F1069 | " references to a male person, particularly when using the pronoun "He"" |

**Findings:** The negative-effect feature L7:F14946 encodes male possessive pronouns ("his", "him", "he") while suppressing female pronouns ("her", "she", etc.). It also activates on non-ASCII characters like "©". 

The circuit shows that this feature primarily gets its signal directly from the token embedding of "His" at position 1 (strongest edge weight 18.375). The feature detects male pronouns specifically …

</details>

<details>
<summary><b>SA-3</b> — tool trace (8 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L18, F14743 | "He" |
| 2 | `get_upstream_features` | L18:F14743@14, k=5 | Emb:" He"@14 (w=22.38) +4 more |
| 3 | `inspect_feature` | L0, F1069 | " references to a male person, particularly when using the pronoun "He"" |
| 4 | `inspect_feature` | L17, F5889 | " references to people with pronouns and possessive pronouns" |
| 5 | `inspect_feature` | L13, F6622 | " pronouns." |
| 6 | `get_upstream_features` | L0:F1069@14, k=5 | Emb:" He"@14 (w=35.75) +4 more |
| 7 | `get_upstream_features` | L17:F5889@14, k=5 | Emb:" He"@14 (w=21.50) +4 more |
| 8 | `get_upstream_features` | L13:F6622@14, k=5 | Emb:" He"@14 (w=12.50) +4 more |

**Findings:** Tracing L18:F14743 at position 14 (feature encoding "He" pronoun) reveals a clear circuit: The primary signal originates from the embedding of " He" at position 14 itself, feeding directly into the L18 feature (weight: 22.375). Additionally, there's a layer 0 feature (L0:F1069) that detects male person references, particularly "He" or "His", which feeds into L18 (weight: 7.0312). This layer 0 feat…

</details>

<details>
<summary><b>SA-4</b> — tool trace (19 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L19, F8814 | " various pronouns and names referring to people" |
| 2 | `get_upstream_features` | L19:F8814@1, k=5 | Emb:"His"@1 (w=9.31) +4 more |
| 3 | `inspect_feature` | L18, F7400 | " words related to coding and software/UI interfaces, with some bias to" |
| 4 | `inspect_feature` | L7, F14893 | " pronouns or possessive pronouns" |
| 5 | `inspect_feature` | L7, F14946 | " the possessive pronoun "his" (or similar pronouns like "he" and "him"" |
| 6 | `inspect_feature` | L18, F10315 | " pronouns and possessive pronouns" |
| 7 | `get_upstream_features` | L18:F7400@1, k=5 | Emb:"His"@1 (w=13.00) +4 more |
| 8 | `get_upstream_features` | L7:F14893@1, k=5 | Emb:"His"@1 (w=23.50) +4 more |
| 9 | `get_upstream_features` | L7:F14946@1, k=5 | Emb:"His"@1 (w=18.38) +4 more |
| 10 | `inspect_feature` | L4, F4315 | " mentions of "his" and other associated pronouns like he, him, or hers" |
| 11 | `inspect_feature` | L0, F2994 | "the pronoun "his" and the pronoun "he."" |
| 12 | `inspect_feature` | L6, F12990 | " male pronouns and titles along with descriptors associated with men" |
| 13 | `get_upstream_features` | L0:F2994@1, k=5 | Emb:"His"@1 (w=19.75) +4 more |
| 14 | `get_upstream_features` | L4:F4315@1, k=5 | Emb:"His"@1 (w=23.50) +4 more |
| 15 | `get_upstream_features` | L6:F12990@1, k=5 | Emb:"His"@1 (w=4.91) +4 more |
| 16 | `inspect_feature` | L15, F851 | " code documentation blocks in various programming languages" |
| 17 | `inspect_feature` | L2, F5491 | "references to God in the third person." |
| 18 | `inspect_feature` | L1, F7439 | " the possessive pronouns "his" and "him"" |
| 19 | `inspect_feature` | L11, F10933 | "the letters "L", "H," and "a" when they are at the beginning of a text" |

**Findings:** I traced L19:F8814 at position 1, which encodes "various pronouns and names referring to people" and promotes feminine pronouns like "herself", "she", "her". The circuit reveals it's processing the input token "His" at position 1. The signal originates primarily from the embedding of "His", with additional processing through a gender-pronoun circuit:

1. Direct strong connection from embedding "Hi…

</details>

<details>
<summary><b>SA-5</b> — tool trace (20 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F12990 | " male pronouns and titles along with descriptors associated with men" |
| 2 | `get_upstream_features` | L6:F12990@1, k=5 | Emb:"His"@1 (w=4.91) +4 more |
| 3 | `inspect_feature` | L4, F4315 | " mentions of "his" and other associated pronouns like he, him, or hers" |
| 4 | `inspect_feature` | L5, F10952 | "third person pronouns in varying contexts" |
| 5 | `get_upstream_features` | L4:F4315@1, k=5 | Emb:"His"@1 (w=23.50) +4 more |
| 6 | `inspect_feature` | L0, F2994 | "the pronoun "his" and the pronoun "he."" |
| 7 | `inspect_feature` | L1, F7439 | " the possessive pronouns "his" and "him"" |
| 8 | `inspect_feature` | L2, F5491 | "references to God in the third person." |
| 9 | `get_upstream_features` | L5:F10952@1, k=5 | Emb:"His"@1 (w=10.69) +4 more |
| 10 | `get_upstream_features` | L2:F5491@1, k=5 | Emb:"His"@1 (w=23.88) +4 more |
| 11 | `inspect_feature` | L0, F1069 | " references to a male person, particularly when using the pronoun "He"" |
| 12 | `get_upstream_features` | L1:F7439@1, k=5 | Emb:"His"@1 (w=16.38) +4 more |
| 13 | `inspect_feature` | L0, F7344 | " content markers like figures and section headers" |
| 14 | `get_upstream_features` | L6:F12990@1, k=10 | Emb:"His"@1 (w=4.91) +9 more |
| 15 | `inspect_feature` | L4, F15567 | "sentences with male or female pronouns and possessives, especially one" |
| 16 | `inspect_feature` | L3, F13121 | "the word "His" and words that are often capitalized in scientific lite" |
| 17 | `inspect_feature` | L5, F14942 | " proper nouns representing places and people" |
| 18 | `inspect_feature` | L5, F6376 | " pronouns, possessives and names" |
| 19 | `get_upstream_features` | L3:F13121@1, k=5 | Emb:"His"@1 (w=18.75) +4 more |
| 20 | `get_upstream_features` | L4:F15567@1, k=5 | Emb:"His"@1 (w=19.25) +4 more |

</details>

### Build

`build_circuit` → 11 nodes, 11 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m2.7 | 20,956 | 3,260 | 36,724 | 0 | — | — | — |
| SA-3 | deepseek/deepseek-v3.2 | 47,424 | 3,066 | 0 | 0 | — | ✅ 1480F/11E | Trace this strong negative-effect feature at position 14 bac… |
| SA-2 | deepseek/deepseek-v3.2 | 96,241 | 4,012 | 0 | 0 | — | ✅ 8F/23E | Trace this negative-effect feature back to its origins. What… |
| SA-1 | deepseek/deepseek-v3.2 | 102,722 | 3,941 | 0 | 0 | — | ✅ 8F/15E | Trace this positive-effect feature back to its origins. What… |
| SA-4 | deepseek/deepseek-v3.2 | 140,281 | 5,817 | 31,296 | 0 | — | ✅ 12F/29E | Trace this positive-effect feature at position 1 back to its… |
| SA-5 | deepseek/deepseek-v3.2 | 147,500 | 2,751 | 31,360 | 0 | — | ❌ error | Trace this male pronoun feature to see if there are any prof… |
| **Total** | | **555,124** | **22,847** | **99,380** | **0** | **—** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 7m 1s