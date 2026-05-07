# Circuit Oracle Report
**Date:** 2026-03-26 18:03:42 UTC | **Orchestrator:** anthropic/claude-opus-4.6 | **Subagent:** anthropic/claude-sonnet-4.6

## Input
**Prompt:** "Dataset: bib_nurse_professor-neg_neg_2 | Probe: biased | Method: correct"
**System prompt:** ""
**Concern:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."
**Top predictions:**  (100.0%)

## Oracle Analysis
## Analysis

**Analysis:** This probe's classification is **predominantly driven by gender/pronoun features rather than genuine profession indicators**, with masculine pronoun detection accounting for roughly 3× the direct effect magnitude of academic/profession features.

**Confidence:** High

**Reasoning:**

### The Concern is Validated: Gender Markers Dominate the Circuit

The circuit reveals a striking imbalance between gender-based and profession-based signal contributions to the probe's classification score.

#### Quantitative Breakdown of Direct Effects

**Gender/pronoun features (positive effect on probe score): ~+1.05**
- **L0:F2994** ("his" pronoun detector, frac_nonzero=0.073): +0.64 total across three positions (3, 25, 47). This is the **single largest contributor** to the probe score. It fires on the literal token "his" with an edge weight of 43.25 from the raw embedding — pure lexical gender detection with zero semantic processing.
- **L7:F14893** (gender-switching pronoun feature, frac_nonzero=0.009): +0.20. Promotes "herself/she" and suppresses "himself" — a contrastive gender feature fed by "his" at pos 3 and "Daniel" at pos 1.
- **L0:F7532** (proper noun detector, frac_nonzero=0.06): +0.11 at pos 1 ("Daniel"). Notably suppresses female names like "Manuela", "Karla", "Kayla" — encoding the male gender of the name.
- **L0:F13553** (past tense verbs, frac_nonzero=0.034): +0.10. Promotes "himself/his/he" — a grammatical feature that leaks gender.

**Profession/academic features (positive effect): ~+0.35**
- **L6:F170** (academic fields, frac_nonzero=0.039): +0.24 across pos 8 and 9 ("Mechanical Engineering"). This feature is fed by a genuine, well-structured profession circuit: L2:F10852 (academic degrees, frac=0.008) detects "Bachelors" → L3:F4113 (degrees + study areas, frac=0.003) → L4:F3727 (degree mentions, frac=0.005) → L5:F10392 (academic study fields, frac=0.004) → L6:F170. Every intermediate feature has very low frac_nonzero, confirming they encode specific credential knowledge.
- **L0:F1326** (organizations/institutions, frac_nonzero=0.006): +0.11 at pos 14 (likely "University").

#### The Two Parallel Circuits

**Circuit 1 — Gender Detection (dominant):** The token "his" (pos 3) directly activates L0:F2994, which contributes +0.39 to the probe and feeds through a multi-layer masculine cascade (L4:F4315 → L6:F12990 → L7:F14893). Separately, "He" (pos 22) activates L0:F1069 → L1:F12922 → L2:F13928 → cascading through L13-L17 to L18:F14743. The "Daniel" embedding at pos 1 also feeds the gender circuit (edge weight +3.81 into L7:F14893). These gender features originate from **three separate input tokens** ("his", "He", "Daniel") and dominate the top-20 features list.

**Circuit 2 — Academic Credentials (secondary):** "Bachelors" and "Engineering" feed through a clean, specific credential-detection hierarchy. However, two of the academic features actually have **negative** direct effects: L5:F10392 (-0.11) and parts of L6:F170. The net positive contribution from academic features is modest.

#### Evidence of Spuriousness

1. **The #1 feature (L0:F2994) is a pure "his" token detector** with frac_nonzero=0.073 — it fires on any occurrence of "his" regardless of context. Its direct effect (+0.39) alone exceeds the entire academic pathway's contribution.

2. **Gender features fire on multiple positions** (pos 3, 22, 25, 47, 81) where "his" and "He" appear throughout the bio — the probe is essentially counting masculine pronouns.

3. **Several gender features have negative direct effects** (L6:F12990 at -0.28, L18:F14743 at -0.25, L7:F14946 at -0.18), suggesting a complex push-pull dynamic where gender signal both helps and hurts — characteristic of a probe that has partially but imperfectly learned to use gender as a shortcut.

4. **The counterbalance feature L12:F2175** ("gender words", negative effect -0.18) is driven by the "received" token at pos 2, not by any profession content — it dampens gender signal from biographical verb context, not from genuine profession understanding.

5. **Key ratio:** Gender-linked features account for approximately **75% of the total positive direct effect** on the probe score, while genuine profession/credential features account for only **~25%**.

### Conclusion

**The user's concern is well-founded.** The probe has learned a shortcut where masculine pronouns ("his", "He") and the male name "Daniel" are the primary drivers of its classification. While a legitimate academic credential pathway exists (detecting "Bachelors degree in Mechanical Engineering" through a well-structured 5-layer hierarchy), it contributes far less to the final score than the gender channel. This probe would likely misclassify profession for texts with similar gender markers but different professions, and would struggle with female professionals in engineering or male professionals in traditionally female-associated fields.

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L0:2994 de=0.395 |
| 3 | `inspect_feature` ×15 | L0:2994, L7:14893, L12:2175, L7:14946, L6:12990, L6:170, L18:14743, L5:10392, L0:1326, L0:7532, L0:12351, L0:13526, L0:15320, L0:13553, L18:10315 |

### Dispatch: 7 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L0:F2994@3` | ✅ reported | 4 | 7 | Trace L0:F2994 at pos 3 — this is a 'his' pronoun detector at layer 0. Determine… |
| SA-2 | `L7:F14893@3` | ✅ reported | 8 | 18 | Trace L7:F14893 at pos 3 — this is a pronoun/possessive pronoun detector that pr… |
| SA-3 | `L6:F170@9` | ✅ reported | 8 | 11 | Trace L6:F170 at pos 9 — this is an 'academic fields' feature that fires at a po… |
| SA-4 | `L18:F14743@22` | ✅ reported | 12 | 15 | Trace L18:F14743 at pos 22 — labeled 'He', this detects male pronouns. Understan… |
| SA-5 | `L12:F2175@2` | ✅ reported | 13 | 23 | Trace L12:F2175 at pos 2 — labeled 'words referring to gender'. It has NEGATIVE … |
| SA-6 | `L6:F12990@22` | ✅ reported | 9 | 17 | Trace L6:F12990 at pos 22 — 'male pronouns and titles'. It has NEGATIVE direct e… |
| SA-7 | `L5:F10392@9` | ✅ reported | 0 | 0 | Trace L5:F10392 at pos 9 — 'fields of academic study'. This has negative direct … |

<details>
<summary><b>SA-1</b> — tool trace (5 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F2994 | "the pronoun "his" and the pronoun "he."" |
| 2 | `get_upstream_features` | L0:F2994@3, k=8 | Emb:" his"@3 (w=43.25) +7 more |
| 3 | `inspect_feature` | L0, F2285 | " name followed by a number" |
| 4 | `inspect_feature` | L0, F1903 | "instances of sentences starting with "The"" |
| 5 | `inspect_feature` | L0, F777 | " the word "bone"" |

**Findings:** ## Summary: L0:F2994 — "his/he" Pronoun Detector

### What the feature represents
L0:F2994 is a **highly specific masculine pronoun detector**, firing on the tokens `" his"` and `" he"`. It is active on ~7.3% of tokens (moderately selective), with top examples all involving `" his"` in natural prose. Its **suppressed tokens** are the most revealing: it suppresses `" his"`, `"his"`, and cross-lingu…

</details>

<details>
<summary><b>SA-2</b> — tool trace (12 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L7, F14893 | " pronouns or possessive pronouns" |
| 2 | `get_upstream_features` | L7:F14893@3, k=8 | Emb:" his"@3 (w=24.38) +7 more |
| 3 | `inspect_feature` | L0, F2994 | "the pronoun "his" and the pronoun "he."" |
| 4 | `inspect_feature` | L6, F12990 | " male pronouns and titles along with descriptors associated with men" |
| 5 | `inspect_feature` | L4, F4315 | " mentions of "his" and other associated pronouns like he, him, or hers" |
| 6 | `inspect_feature` | L6, F10944 | " text in languages other than English" |
| 7 | `get_upstream_features` | L0:F2994@3, k=6 | Emb:" his"@3 (w=43.25) +5 more |
| 8 | `get_upstream_features` | L6:F12990@3, k=6 | Emb:" his"@3 (w=8.31) +5 more |
| 9 | `get_upstream_features` | L4:F4315@3, k=6 | Emb:" his"@3 (w=28.50) +5 more |
| 10 | `inspect_feature` | L2, F5491 | "references to God in the third person." |
| 11 | `inspect_feature` | L1, F7439 | " the possessive pronouns "his" and "him"" |
| 12 | `inspect_feature` | L3, F13121 | "the word "His" and words that are often capitalized in scientific lite" |

**Findings:** ## Circuit Summary: L7:F14893 — Gender-Switching Pronoun Detector

**Core finding: YES, this feature is directly encoding gender information from the input token " his" at position 3, and doing so via a sophisticated multi-layer inhibitory cascade.**

### The Paradox Explained
The most striking result is that **" his" (the raw token embedding) is the #1 driver of L7:F14893** with a massive +24.375…

</details>

<details>
<summary><b>SA-3</b> — tool trace (13 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F170 | " references to academic fields, especially those in the humanities" |
| 2 | `get_upstream_features` | L6:F170@9, k=6 | L5:F10392 (w=10.94) +5 more |
| 3 | `inspect_feature` | L5, F10392 | " fields of academic study" |
| 4 | `inspect_feature` | L5, F6384 | "words related to higher education and professions" |
| 5 | `inspect_feature` | L3, F4113 | " mentions of academic degrees and areas of study" |
| 6 | `get_upstream_features` | L5:F10392@9, k=6 | Emb:" Mechanical"@8 (w=3.08) +5 more |
| 7 | `inspect_feature` | L4, F3727 | " mentions of academic degrees" |
| 8 | `inspect_feature` | L2, F1440 | " the word "engineering" and words related to its definition" |
| 9 | `get_upstream_features` | L4:F3727@5, k=6 | Emb:"achelors"@5 (w=22.25) +5 more |
| 10 | `get_upstream_features` | L3:F4113@7, k=6 | Emb:" in"@7 (w=12.12) +5 more |
| 11 | `inspect_feature` | L2, F10852 | " academic titles and degrees" |
| 12 | `get_upstream_features` | L2:F10852@5, k=6 | Emb:"achelors"@5 (w=19.25) +5 more |
| 13 | `inspect_feature` | L0, F9026 | "technical documents or data, including numbers, units, and references " |

**Findings:** ## Circuit Summary: L6:F170 "Academic Fields" at position 9 ('Engineering')

### What the circuit detects
L6:F170 is an **academic fields / humanities reference detector** that fires at pos 9 (the token ' Engineering'). The circuit is a tightly organized, multi-layer abstraction hierarchy that progressively builds from raw token embeddings upward into a high-level academic field concept.

---

###…

</details>

<details>
<summary><b>SA-4</b> — tool trace (22 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L18, F14743 | "He" |
| 2 | `get_upstream_features` | L18:F14743@22, k=8 | Emb:" He"@22 (w=21.88) +7 more |
| 3 | `inspect_feature` | L0, F1069 | " references to a male person, particularly when using the pronoun "He"" |
| 4 | `inspect_feature` | L17, F5889 | " references to people with pronouns and possessive pronouns" |
| 5 | `inspect_feature` | L13, F6622 | " pronouns." |
| 6 | `inspect_feature` | L15, F3330 | " personal stories of individuals, especially women and their actions o" |
| 7 | `get_upstream_features` | L0:F1069@22, k=8 | Emb:" He"@22 (w=37.00) +7 more |
| 8 | `get_upstream_features` | L17:F5889@22, k=8 | Emb:" He"@22 (w=20.75) +7 more |
| 9 | `inspect_feature` | L6, F2267 | "words that appear in programming code, legal jargon, or scientific tex" |
| 10 | `get_upstream_features` | L13:F6622@22, k=8 | Emb:" He"@22 (w=13.19) +7 more |
| 11 | `inspect_feature` | L11, F8266 | " mentions of people with professional titles or descriptions, especial" |
| 12 | `get_upstream_features` | L15:F3330@22, k=8 | Emb:" He"@22 (w=17.12) +7 more |
| 13 | `inspect_feature` | L2, F13928 | " third person pronouns related to people's credentials" |
| 14 | `inspect_feature` | L1, F12922 | " the pronoun "he" or "she" in a narrative context" |
| 15 | `get_upstream_features` | L11:F8266@22, k=8 | Emb:" He"@22 (w=2.72) +7 more |
| 16 | `inspect_feature` | L7, F1674 | " certain common titles (Mr., Dr.) combined with job-related action ver" |
| 17 | `get_upstream_features` | L2:F13928@22, k=8 | Emb:" He"@22 (w=6.12) +7 more |
| 18 | `inspect_feature` | L0, F2241 | " the pronoun "she"" |
| 19 | `get_upstream_features` | L7:F1674@22, k=8 | Emb:" He"@22 (w=3.31) +7 more |
| 20 | `inspect_feature` | L3, F2860 | " instances of a male person with a title in a professional setting" |
| 21 | `inspect_feature` | L5, F6228 | " past tense verbs" |
| 22 | `inspect_feature` | L4, F15438 | " mentions and declarations of conflicts of interest, study design, and" |

**Findings:** ## Circuit Summary: L18:F14743 "He" — Male Pronoun Detection at pos 22

**What is pos 22?** The token " He" — a capitalized male pronoun at the start of a sentence in what appears to be a biographical/professional bio context (e.g., "Daniel received his [B]achelors [of] [Engineering at] [Waterloo]. He...").

---

### Primary Signal: Direct Token Identity (Gender-Specific, Not Profession-Specific)
…

</details>

<details>
<summary><b>SA-5</b> — tool trace (21 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L12, F2175 | " words referring to gender" |
| 2 | `get_upstream_features` | L12:F2175@2, k=8 | Emb:" received"@2 (w=4.09) +7 more |
| 3 | `inspect_feature` | L5, F7317 | " phrases with names and nicknames" |
| 4 | `inspect_feature` | L5, F6228 | " past tense verbs" |
| 5 | `inspect_feature` | L7, F7210 | " words and phrases that connote conflict and stress." |
| 6 | `inspect_feature` | L3, F6253 | "the word "receive" and its inflections." |
| 7 | `get_top_logits` | k=5 | "" (100%) |
| 8 | `inspect_feature` | L9, F12135 | " words related to legal issues or financial matters" |
| 9 | `inspect_feature` | L3, F6158 | " names of people, sometimes including middle initials or titles" |
| 10 | `get_upstream_features` | L7:F7210@2, k=6 | Emb:"Daniel"@1 (w=2.14) +5 more |
| 11 | `get_upstream_features` | L5:F7317@2, k=6 | L4:F16158 (w=-2.67) +5 more |
| 12 | `inspect_feature` | L4, F16158 | " verbs, especially in the present and past tenses, locations, and othe" |
| 13 | `inspect_feature` | L3, F6656 | "verbs or phrases indicating action, saying, or feeling" |
| 14 | `inspect_feature` | L6, F5355 | "names and identifiers" |
| 15 | `get_upstream_features` | L9:F12135@2, k=6 | L3:F6253 (w=-0.91) +5 more |
| 16 | `inspect_feature` | L2, F3992 | " instances of people or things receiving something" |
| 17 | `get_upstream_features` | L3:F6253@2, k=5 | Emb:" received"@2 (w=21.62) +4 more |
| 18 | `get_upstream_features` | L5:F6228@2, k=5 | L2:F16309 (w=3.59) +4 more |
| 19 | `inspect_feature` | L2, F16309 | " people's names" |
| 20 | `inspect_feature` | L1, F1840 | " the words "receiver", "received", "receivers", "sender",  "send", "op" |
| 21 | `get_upstream_features` | L2:F3992@2, k=5 | Emb:" received"@2 (w=23.88) +4 more |

**Findings:** 
## L12:F2175 — "Words Referring to Gender": A Counterbalance Circuit Driven by " received"

### Core Finding: YES — L12:F2175 is a counterbalance feature

L12:F2175 (label: "words referring to gender", frac_nonzero=0.006, very sparse) has a **negative direct effect (-0.1787)** on the output. Its promoted tokens include " himself", " masculinity", " neuter", and critically its **suppressed tokens …

</details>

<details>
<summary><b>SA-6</b> — tool trace (14 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F12990 | " male pronouns and titles along with descriptors associated with men" |
| 2 | `get_upstream_features` | L6:F12990@22, k=8 | Emb:" He"@22 (w=4.47) +7 more |
| 3 | `inspect_feature` | L4, F14796 | "the pronoun "he" or "him"" |
| 4 | `inspect_feature` | L2, F13928 | " third person pronouns related to people's credentials" |
| 5 | `inspect_feature` | L5, F14942 | " proper nouns representing places and people" |
| 6 | `inspect_feature` | L1, F12922 | " the pronoun "he" or "she" in a narrative context" |
| 7 | `get_upstream_features` | L4:F14796@22, k=6 | Emb:" He"@22 (w=16.88) +5 more |
| 8 | `get_upstream_features` | L2:F13928@22, k=6 | Emb:" He"@22 (w=6.12) +5 more |
| 9 | `get_upstream_features` | L1:F12922@22, k=6 | Emb:" He"@22 (w=23.25) +5 more |
| 10 | `inspect_feature` | L0, F1069 | " references to a male person, particularly when using the pronoun "He"" |
| 11 | `inspect_feature` | L0, F2241 | " the pronoun "she"" |
| 12 | `inspect_feature` | L2, F2110 | " the third person singular pronouns "he" and "she"" |
| 13 | `inspect_feature` | L3, F2860 | " instances of a male person with a title in a professional setting" |
| 14 | `get_upstream_features` | L0:F1069@22, k=5 | Emb:" He"@22 (w=37.00) +4 more |

**Findings:** ## Circuit Summary: L6:F12990 — Male Pronoun/Title Detector (Negative Direct Effect)

### Root Input: " He" embedding at pos 22
The single token " He" at position 22 is the overwhelmingly dominant driver of this entire circuit. It feeds every level of the chain with massive edge weights (37.0 → L0:F1069, 23.25 → L1:F12922, 16.875 → L4:F14796, 6.125 → L2:F13928, 4.47 directly to L6:F12990).

### Ci…

</details>

<details>
<summary><b>SA-7</b> — tool trace (15 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L5, F10392 | " fields of academic study" |
| 2 | `get_upstream_features` | L5:F10392@9, k=8 | Emb:" Mechanical"@8 (w=3.08) +7 more |
| 3 | `inspect_feature` | L4, F3727 | " mentions of academic degrees" |
| 4 | `inspect_feature` | L3, F4113 | " mentions of academic degrees and areas of study" |
| 5 | `inspect_feature` | L2, F1440 | " the word "engineering" and words related to its definition" |
| 6 | `inspect_feature` | L4, F11037 | " words related to counseling, therapy, social work, and academic degre" |
| 7 | `get_upstream_features` | L4:F3727@5, k=6 | Emb:"achelors"@5 (w=22.25) +5 more |
| 8 | `get_upstream_features` | L3:F4113@7, k=6 | Emb:" in"@7 (w=12.12) +5 more |
| 9 | `get_upstream_features` | L4:F11037@9, k=6 | Emb:" Engineering"@9 (w=8.25) +5 more |
| 10 | `inspect_feature` | L2, F10852 | " academic titles and degrees" |
| 11 | `inspect_feature` | L3, F11994 | " academic degrees and professional titles, especially involving "Ph.D." |
| 12 | `inspect_feature` | L3, F1937 | " the word "engineering", including different kinds of engineering" |
| 13 | `get_upstream_features` | L2:F10852@5, k=6 | Emb:"achelors"@5 (w=19.25) +5 more |
| 14 | `get_upstream_features` | L2:F1440@9, k=6 | Emb:" Engineering"@9 (w=19.50) +5 more |
| 15 | `inspect_feature` | L0, F9026 | "technical documents or data, including numbers, units, and references " |

</details>

### Build

`build_circuit` → 22 nodes, 30 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | anthropic/claude-opus-4.6 | 114,348 | 7,062 | 0 | 0 | $0.7483 | — | — |
| SA-1 | anthropic/claude-sonnet-4.6 | 14,052 | 2,192 | 0 | 0 | $0.0750 | ✅ 4F/7E | Trace L0:F2994 at pos 3 — this is a 'his' pronoun detector a… |
| SA-3 | anthropic/claude-sonnet-4.6 | 36,734 | 4,027 | 0 | 0 | $0.1706 | ✅ 8F/11E | Trace L6:F170 at pos 9 — this is an 'academic fields' featur… |
| SA-6 | anthropic/claude-sonnet-4.6 | 50,936 | 4,353 | 0 | 0 | $0.2181 | ✅ 9F/17E | Trace L6:F12990 at pos 22 — 'male pronouns and titles'. It h… |
| SA-2 | anthropic/claude-sonnet-4.6 | 46,611 | 4,978 | 0 | 0 | $0.2145 | ✅ 8F/18E | Trace L7:F14893 at pos 3 — this is a pronoun/possessive pron… |
| SA-7 | anthropic/claude-sonnet-4.6 | 48,830 | 5,438 | 0 | 0 | $0.2281 | ✅ 0F/0E | Trace L5:F10392 at pos 9 — 'fields of academic study'. This … |
| SA-5 | anthropic/claude-sonnet-4.6 | 73,868 | 5,755 | 0 | 0 | $0.3079 | ✅ 13F/23E | Trace L12:F2175 at pos 2 — labeled 'words referring to gende… |
| SA-4 | anthropic/claude-sonnet-4.6 | 116,965 | 5,131 | 0 | 0 | $0.4279 | ✅ 12F/15E | Trace L18:F14743 at pos 22 — labeled 'He', this detects male… |
| **Total** | | **502,344** | **38,936** | **0** | **0** | **$2.3904** | | |

**Oracle wall-clock time:** 13m 49s