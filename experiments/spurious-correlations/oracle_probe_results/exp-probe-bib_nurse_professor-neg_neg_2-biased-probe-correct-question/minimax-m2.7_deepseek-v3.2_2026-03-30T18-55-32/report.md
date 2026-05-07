# Circuit Oracle Report
**Date:** 2026-03-30 18:55:32 UTC | **Orchestrator:** minimax/minimax-m2.7 | **Subagent:** deepseek/deepseek-v3.2

## Input
**Prompt:** "Dataset: bib_nurse_professor-neg_neg_2 | Probe: biased | Method: correct"
**System prompt:** ""
**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."
**Top predictions:**  (100.0%)

## Oracle Analysis
**Analysis:** The probe's classification is primarily driven by gender markers (pronoun detectors) rather than genuine profession indicators—the strongest positive contributor is L0:F2994 ("his/he" pronoun detector, direct effect = 0.3945) followed by L7:F14893 (feminine pronoun detector, 0.2041), while the genuine profession/education features (L6:F170 encoding "academic fields" at 0.1426, and academic degree detectors at 0.1089) contribute less than half the signal strength.

**Confidence:** 9/10

**Reasoning:** The attribution circuit reveals that the probe classification is driven by two competing pathways:

**Spurious Gender Pathway (dominant):**
- **L0:F2994** ("pronoun 'his/he' detector", frac_nonzero=0.073) is the single strongest feature with direct effect 0.3945, receiving 43.25 weight from the " his" token embedding directly
- **L7:F14893** (feminine pronoun detector, frac_nonzero=0.009) has direct effect 0.2041—it paradoxically fires on "his" at position 3 but is suppressed by L0:F2994 (-10.9375), and the "Daniel" name weakly excites it (+3.8125)
- **L7:F14946** and **L6:F12990** (masculine pronoun detectors) suppress the probe output (-0.1768, -0.1758) by detecting "his" and "Daniel" as masculine
- **L12:F2175** ("words referring to gender") at position 2 suppresses (-0.1787) by promoting masculine terms like "himself" and "masculinity"
- **L18:F14743** ("He" detector) at position 22 suppresses (-0.1387) via a biographical/career information circuit (L14:F10121 "personal names and career information")

**Genuine Profession Pathway (weaker):**
- **L6:F170** ("academic field references", frac_nonzero=0.039) has direct effect 0.1426, receiving strong input from **L5:F10392** ("fields of academic study", frac=0.004)
- **L5:F10392** is fed by **L4:F3727** ("academic degrees") detecting "Bachelors" at pos 5, and **L2:F1440** ("engineering") directly detecting "Engineering" at pos 9
- **L4:F11037** ("counseling, therapy, social work, and academic degree programs") with promoted tokens "engineer", "engineering" (frac=0.007)
- **L2:F10852** ("academic titles and degrees") detects "Ph.D" and feeds into degree detection (direct effect 0.1089)
- **L0:F1326** ("organizations/government agencies") responds to "University of Waterloo" (direct effect 0.1089)

**Key finding:** The circuit does use spurious gender markers as primary drivers. The " his" pronoun at position 3 (which is purely a grammatical artifact describing Daniel's degrees, not a profession indicator) dominates the circuit with 0.3945 effect. Meanwhile, the actual profession-relevant content (Mechanical Engineering, Ph.D, University of Waterloo, Robotics and Computer Vision) contributes only ~0.25 combined (0.1426 + 0.1089). The name "Daniel" itself has weak gender-correlated connections to pronoun detectors, but the dominant signal comes from the " his" token's raw embedding triggering pronoun detection cascades. The model appears to use a gender→profession shortcut rather than genuinely encoding the actual education/career content.

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L0:2994 de=0.395 |

### Dispatch: 8 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L0:F2994@3` | ✅ reported | 8 | 11 | Trace what L0:2994 encodes. Is this a gender marker (e.g., "Daniel" name detecti… |
| SA-2 | `L7:F14893@3` | ✅ reported | 6 | 14 | Trace what L7:14893 encodes at position 3 (likely "Daniel"). Examine its label, … |
| SA-3 | `L12:F2175@2` | ✅ reported | 11 | 17 | Trace L12:2175 which has a strong negative effect at pos 2. Examine its label, f… |
| SA-4 | `L6:F170@9` | ✅ reported | 9 | 8 | Trace L6:170 which fires at pos 9 with positive effect. Position 9 is around "Me… |
| SA-5 | `L7:F14946@3` | ✅ reported | 6 | 14 | Trace L7:14946 which has a strong negative effect at pos 3. Examine its label an… |
| SA-6 | `L0:F1326@14` | ✅ reported | 1 | 2 | Trace L0:1326 which has a positive effect at pos 14. Position 14 is around "Ph.D… |
| SA-7 | `L0:F12351@2` | ✅ reported | 4 | 9 | Trace L0:12351 at position 2 which has a negative effect. Position 2 is "receive… |
| SA-8 | `L18:F14743@22` | ✅ reported | 10 | 19 | Trace L18:14743 at position 22 with a negative effect. Position 22 is around "in… |

<details>
<summary><b>SA-1</b> — tool trace (15 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F2994 | "the pronoun "his" and the pronoun "he."" |
| 2 | `get_upstream_features` | L0:F2994@3, k=5 | Emb:" his"@3 (w=43.25) +4 more |
| 3 | `inspect_feature` | L0, F1847 | "scientific terms and experimental details related to biological and ch" |
| 4 | `get_top_logits` | k=10 | "" (100%) |
| 5 | `get_upstream_features` | L0:F2994@3, k=10 | Emb:" his"@3 (w=43.25) +9 more |
| 6 | `inspect_feature` | L0, F2405 | " proper nouns, especially last names, and some location names or categ" |
| 7 | `inspect_feature` | L0, F2407 | " names of organizations" |
| 8 | `inspect_feature` | L0, F1903 | "instances of sentences starting with "The"" |
| 9 | `get_top_features` | token="", k=10 | 10 features; top: L0:2994 de=0.395 |
| 10 | `inspect_feature` | L7, F14893 | " pronouns or possessive pronouns" |
| 11 | `get_upstream_features` | L7:F14893@3, k=5 | Emb:" his"@3 (w=24.38) +4 more |
| 12 | `inspect_feature` | L6, F12990 | " male pronouns and titles along with descriptors associated with men" |
| 13 | `get_upstream_features` | L6:F12990@3, k=5 | Emb:" his"@3 (w=8.31) +4 more |
| 14 | `inspect_feature` | L4, F4315 | " mentions of "his" and other associated pronouns like he, him, or hers" |
| 15 | `inspect_feature` | L2, F5491 | "references to God in the third person." |

**Findings:** L0:2994 is primarily a "his/he pronoun detector" that gets strongly activated by the token " his" itself (weight 43.25) with weak contextual influence from "Daniel" (weight 0.9258). It is NOT a profession indicator - its promoted tokens are generic punctuation/formatting tokens. The feature suppresses masculine pronouns when it fires. 

The circuit shows that "Daniel" token (pos 1) weakly activate…

</details>

<details>
<summary><b>SA-2</b> — tool trace (10 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L7, F14893 | " pronouns or possessive pronouns" |
| 2 | `get_upstream_features` | L7:F14893@3, k=5 | Emb:" his"@3 (w=24.38) +4 more |
| 3 | `inspect_feature` | L0, F2994 | "the pronoun "his" and the pronoun "he."" |
| 4 | `inspect_feature` | L6, F12990 | " male pronouns and titles along with descriptors associated with men" |
| 5 | `get_upstream_features` | L6:F12990@3, k=5 | Emb:" his"@3 (w=8.31) +4 more |
| 6 | `inspect_feature` | L4, F4315 | " mentions of "his" and other associated pronouns like he, him, or hers" |
| 7 | `inspect_feature` | L2, F5491 | "references to God in the third person." |
| 8 | `get_upstream_features` | L0:F2994@3, k=5 | Emb:" his"@3 (w=43.25) +4 more |
| 9 | `get_upstream_features` | L4:F4315@3, k=5 | Emb:" his"@3 (w=28.50) +4 more |
| 10 | `inspect_feature` | L1, F7439 | " the possessive pronouns "his" and "him"" |

**Findings:** The starting feature L7:14893 at position 3 encodes feminine pronouns/possessive pronouns (promoted tokens: "herself", "elle", "she", etc., suppressed tokens: "himself", "his", etc.). It has low sparsity (frac_nonzero=0.00885), indicating specificity.

The circuit shows an interesting pattern: The raw input token " his" at position 3 strongly excites (+24.375) the feminine pronoun detector L7:1489…

</details>

<details>
<summary><b>SA-3</b> — tool trace (17 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L12, F2175 | " words referring to gender" |
| 2 | `get_upstream_features` | L12:F2175@2, k=5 | Emb:" received"@2 (w=4.09) +4 more |
| 3 | `inspect_feature` | L5, F7317 | " phrases with names and nicknames" |
| 4 | `inspect_feature` | L5, F6228 | " past tense verbs" |
| 5 | `inspect_feature` | L7, F7210 | " words and phrases that connote conflict and stress." |
| 6 | `get_upstream_features` | L5:F7317@2, k=5 | L4:F16158 (w=-2.67) +4 more |
| 7 | `inspect_feature` | L4, F16158 | " verbs, especially in the present and past tenses, locations, and othe" |
| 8 | `inspect_feature` | L3, F6656 | "verbs or phrases indicating action, saying, or feeling" |
| 9 | `inspect_feature` | L2, F16309 | " people's names" |
| 10 | `get_upstream_features` | L3:F6656@2, k=5 | L2:F16309 (w=3.17) +4 more |
| 11 | `get_upstream_features` | L7:F7210@2, k=5 | Emb:"Daniel"@1 (w=2.14) +4 more |
| 12 | `inspect_feature` | L2, F3992 | " instances of people or things receiving something" |
| 13 | `inspect_feature` | L0, F7532 | " proper nouns" |
| 14 | `get_upstream_features` | L5:F6228@2, k=5 | L2:F16309 (w=3.59) +4 more |
| 15 | `inspect_feature` | L4, F14665 | " capitalized proper nouns or names" |
| 16 | `get_upstream_features` | L4:F16158@2, k=5 | L3:F6656 (w=2.31) +4 more |
| 17 | `inspect_feature` | L3, F8210 | " initials preceded by a first name or honorific" |

**Findings:** The circuit tracing reveals that L12:2175 ("words referring to gender") suppresses the probe through a complex interaction:

1. The feature L12:2175 promotes masculine terms ("himself", "masculinity", "cologne") and suppresses feminine terms ("herself", "female", "woman"). It has low frac_nonzero (0.00622), indicating specificity.

2. Key upstream connections:
   - L5:7317 ("phrases with names and…

</details>

<details>
<summary><b>SA-4</b> — tool trace (14 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F170 | " references to academic fields, especially those in the humanities" |
| 2 | `get_upstream_features` | L6:F170@9, k=5 | L5:F10392 (w=10.94) +4 more |
| 3 | `inspect_feature` | L5, F10392 | " fields of academic study" |
| 4 | `inspect_feature` | L5, F6384 | "words related to higher education and professions" |
| 5 | `get_upstream_features` | L5:F10392@9, k=5 | Emb:" Mechanical"@8 (w=3.08) +4 more |
| 6 | `inspect_feijcture` | {'layer': 4, 'feature_idx': 3727} | ❌ Unknown tool: inspect_feijcture |
| 7 | `inspect_feature` | L4, F3727 | " mentions of academic degrees" |
| 8 | `inspect_feature` | L3, F4113 | " mentions of academic degrees and areas of study" |
| 9 | `inspect_feature` | L2, F1440 | " the word "engineering" and words related to its definition" |
| 10 | `get_upstream_features` | L5:F6384@9, k=5 | Emb:" Engineering"@9 (w=7.72) +4 more |
| 11 | `inspect_feature` | L4, F11037 | " words related to counseling, therapy, social work, and academic degre" |
| 12 | `get_upstream_features` | L4:F3727@5, k=5 | Emb:"achelors"@5 (w=22.25) +4 more |
| 13 | `inspect_feature` | L2, F10852 | " academic titles and degrees" |
| 14 | `inspect_feature` | L0, F9026 | "technical documents or data, including numbers, units, and references " |

**Findings:** Tracing L6:F170 at position 9 reveals a circuit that detects academic fields and professions, specifically encoding "Mechanical Engineering" as a field of study rather than gender information. The circuit flows through multiple layers of academic/profession detection:

1. **L6:170** - "references to academic fields, especially those in the humanities" (frac=0.0388) receives strong input from:
2. *…

</details>

<details>
<summary><b>SA-5</b> — tool trace (10 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L7, F14946 | " the possessive pronoun "his" (or similar pronouns like "he" and "him"" |
| 2 | `get_upstream_features` | L7:F14946@3, k=5 | Emb:" his"@3 (w=23.12) +4 more |
| 3 | `inspect_feature` | L0, F2994 | "the pronoun "his" and the pronoun "he."" |
| 4 | `inspect_feature` | L4, F4315 | " mentions of "his" and other associated pronouns like he, him, or hers" |
| 5 | `inspect_feature` | L2, F5491 | "references to God in the third person." |
| 6 | `get_upstream_features` | L0:F2994@3, k=5 | Emb:" his"@3 (w=43.25) +4 more |
| 7 | `get_upstream_features` | L4:F4315@3, k=5 | Emb:" his"@3 (w=28.50) +4 more |
| 8 | `inspect_feature` | L1, F7439 | " the possessive pronouns "his" and "him"" |
| 9 | `get_upstream_features` | L2:F5491@3, k=5 | Emb:" his"@3 (w=37.00) +4 more |
| 10 | `inspect_feature` | L0, F4823 | " the word "part" followed by prepositions or words related to sections" |

**Findings:** This circuit traces the source of L7:F14946, which encodes masculine gender information by detecting the possessive pronoun "his" and similar masculine pronouns. The feature promotes tokens like "himself", "his", "Himself" while suppressing feminine pronouns like "herself", "she", "elle", "her". 

Key findings:
1. The feature gets its primary signal directly from the " his" embedding token at posi…

</details>

<details>
<summary><b>SA-6</b> — tool trace (2 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F1326 | " mentions of organizations and government agencies." |
| 2 | `get_upstream_features` | L0:F1326@14, k=5 | Emb:" University"@12 (w=7.25) +4 more |

**Findings:** Tracing L0:1326 at position 14 (around "Ph.D in Systems Design Engineering" context). The feature detects "mentions of organizations and government agencies" with low sparsity (0.00624). The strongest upstream connections come from embedding tokens: " University" at position 12 (weight 7.25) and " Waterloo" at position 14 (weight 5.1562). This suggests the feature is primarily responding to the "U…

</details>

<details>
<summary><b>SA-7</b> — tool trace (7 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F12351 | "words related to obtaining something, like receiving money or a receip" |
| 2 | `get_upstream_features` | L0:F12351@2, k=5 | Emb:" received"@2 (w=17.25) +4 more |
| 3 | `inspect_feature` | L0, F1847 | "scientific terms and experimental details related to biological and ch" |
| 4 | `inspect_feature` | L0, F1903 | "instances of sentences starting with "The"" |
| 5 | `get_upstream_features` | L0:F1847@1, k=5 | Emb:"<bos>"@0 (w=1.17) +4 more |
| 6 | `get_upstream_features` | L0:F1903@1, k=5 | Emb:"<bos>"@0 (w=12.44) +4 more |
| 7 | `inspect_feature` | L0, F777 | " the word "bone"" |

**Findings:** Tracing L0:12351 at position 2 revealed a simple circuit: This feature detects "words related to obtaining something, like receiving money or a receipt" and primarily gets its signal directly from the raw token embedding of " received" at position 2 (edge weight 17.25). The feature has relatively low sparsity (frac_nonzero=0.03792), meaning it's moderately selective. The promoted tokens include un…

</details>

<details>
<summary><b>SA-8</b> — tool trace (18 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L18, F14743 | "He" |
| 2 | `get_upstream_features` | L18:F14743@22, k=5 | Emb:" He"@22 (w=21.88) +4 more |
| 3 | `inspect_feature` | L0, F1069 | " references to a male person, particularly when using the pronoun "He"" |
| 4 | `inspect_feature` | L17, F5889 | " references to people with pronouns and possessive pronouns" |
| 5 | `get_upstream_features` | L0:F1069@22, k=5 | Emb:" He"@22 (w=37.00) +4 more |
| 6 | `get_upstream_features` | L17:F5889@22, k=5 | Emb:" He"@22 (w=20.75) +4 more |
| 7 | `inspect_feature` | L13, F6622 | " pronouns." |
| 8 | `inspect_feature` | L15, F3330 | " personal stories of individuals, especially women and their actions o" |
| 9 | `get_upstream_features` | L13:F6622@22, k=5 | Emb:" He"@22 (w=13.19) +4 more |
| 10 | `inspect_feature` | L6, F2267 | "words that appear in programming code, legal jargon, or scientific tex" |
| 11 | `get_upstream_features` | L18:F14743@22, k=10 | Emb:" He"@22 (w=21.88) +9 more |
| 12 | `inspect_feature` | L15, F7191 | " words associated with people, places, organizations, and dates, possi" |
| 13 | `inspect_feature` | L12, F11513 | " data related to biographical information and historical timelines" |
| 14 | `get_upstream_features` | L15:F7191@22, k=5 | Emb:"<bos>"@0 (w=-5.12) +4 more |
| 15 | `inspect_feature` | L14, F10121 | " personal names and their associated career information." |
| 16 | `get_upstream_features` | L14:F10121@22, k=5 | L13:F3024 (w=4.56) +4 more |
| 17 | `inspect_feature` | L13, F3024 | " biographical information of people" |
| 18 | `get_upstream_features` | L13:F3024@22, k=5 | Emb:" He"@22 (w=1.97) +4 more |

**Findings:** I traced the circuit for L18:14743 at position 22, which detects the word "He". The tracing reveals:

1. **Main finding**: The "He" detection feature (L18:14743) connects to a biographical/career information circuit. Specifically, it connects through L14:10121 which detects "personal names and their associated career information" and L13:3024 which detects "biographical information of people".

2.…

</details>

### Build

`build_circuit` → 19 nodes, 27 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m2.7 | 30,511 | 5,546 | 38,964 | 0 | — | — | — |
| SA-4 | deepseek/deepseek-v3.2 | 102,533 | 3,921 | 0 | 0 | — | ✅ 9F/8E | Trace L6:170 which fires at pos 9 with positive effect. Posi… |
| SA-2 | deepseek/deepseek-v3.2 | 66,421 | 3,845 | 0 | 0 | — | ✅ 6F/14E | Trace what L7:14893 encodes at position 3 (likely "Daniel").… |
| SA-3 | deepseek/deepseek-v3.2 | 115,780 | 4,660 | 34,048 | 0 | — | ✅ 11F/17E | Trace L12:2175 which has a strong negative effect at pos 2. … |
| SA-1 | deepseek/deepseek-v3.2 | 114,472 | 4,584 | 10,368 | 0 | — | ✅ 8F/11E | Trace what L0:2994 encodes. Is this a gender marker (e.g., "… |
| SA-6 | deepseek/deepseek-v3.2 | 9,036 | 1,223 | 0 | 0 | — | ✅ 1F/2E | Trace L0:1326 which has a positive effect at pos 14. Positio… |
| SA-7 | deepseek/deepseek-v3.2 | 32,514 | 2,170 | 4,416 | 0 | — | ✅ 4F/9E | Trace L0:12351 at position 2 which has a negative effect. Po… |
| SA-5 | deepseek/deepseek-v3.2 | 64,862 | 3,502 | 0 | 0 | — | ✅ 6F/14E | Trace L7:14946 which has a strong negative effect at pos 3. … |
| SA-8 | deepseek/deepseek-v3.2 | 153,772 | 5,169 | 9,344 | 0 | — | ✅ 10F/19E | Trace L18:14743 at position 22 with a negative effect. Posit… |
| **Total** | | **689,901** | **34,620** | **97,140** | **0** | **—** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 8m 0s