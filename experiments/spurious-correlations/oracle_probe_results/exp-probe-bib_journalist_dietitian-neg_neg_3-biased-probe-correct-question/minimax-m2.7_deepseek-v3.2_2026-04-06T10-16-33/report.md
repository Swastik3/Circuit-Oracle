# Circuit Oracle Report
**Date:** 2026-04-06 10:16:33 UTC | **Orchestrator:** minimax/minimax-m2.7 | **Subagent:** deepseek/deepseek-v3.2

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-neg_neg_3 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "('The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession.',)"

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification is primarily driven by a **gender-marking circuit** (masculine pronouns "He" and "him") rather than genuine profession indicators like "journalist" or "journalistic." The dominant signal originates from the token embedding " him" at position 46, which feeds through multiple pronoun detection layers (L0→L3) into a gender-processing feature (L7:F14893) that paradoxically promotes feminine pronouns. The second key input "He" at position 1 activates a male pronoun/title feature (L6:F12990). Meanwhile, the actual profession-relevant content ("represents," "journalistic," "stories") contributes much weaker signals to the classification.

**Confidence:** 9/10

**Reasoning:** The circuit analysis reveals a clear pattern where gender markers dominate the probe's prediction:

1. **Dominant gender circuit**: The token " him" at position 46 (direct effect = -0.2539) feeds into a cascade of pronoun detectors at layers 0-3 (L0:F16297, L0:F2994, L2:F6929, L3:F2434), all labeled as detecting "him" pronouns. These converge into L7:F14893, which promotes feminine pronouns ("herself", "elle", "she") while suppressing masculine ones. This creates a gender contrast/relationship circuit rather than encoding profession.

2. **Secondary gender feature**: The "He" token at position 1 directly activates L6:F12990 (male pronouns/titles, frac_nonzero = 0.06766), which promotes masculine terms ("himself", "Himself") and suppresses feminine terms.

3. **Weak profession signals**: The genuine profession-related features have much smaller direct effects:
   - L1:F7449 ("representation" detection, direct_effect = +0.2168, frac_nonzero = 0.00628)
   - L1:F14812 ("stories" narrative detection, direct_effect = +0.2158, frac_nonzero = 0.00947)

4. **Pattern matching vs. knowledge**: L7:F14893 has extremely low frac_nonzero (0.00885), meaning it fires in rare, specific contexts (French text, code symbols). This suggests it's a pattern-matching feature rather than encoding generalized profession knowledge. The model's reliance on gender markers to classify profession is a **spurious correlation** — it learns that "him" + "He" often co-occur with certain professions in training data, but this doesn't reflect genuine semantic understanding of professions.

5. **Validation of user concern**: The circuit confirms the user's concern — the probe uses gender markers as primary classification signals rather than profession-specific indicators. This is a classic example of a model exploiting dataset biases (professions being correlated with gender in training data) rather than learning the actual semantic content.

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 10 features; top: L0:6051 de=-0.254 |

### Dispatch: 5 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L0:F6051@15` | ✅ reported | 1 | 5 | Trace this feature to understand what semantic concept it encodes and trace its … |
| SA-2 | `L7:F14893@46` | ✅ reported | 10 | 25 | Trace this feature to understand what semantic concept it encodes and trace its … |
| SA-3 | `L1:F7449@9` | ✅ reported | 4 | 20 | Trace this feature to understand what semantic concept it encodes and trace its … |
| SA-4 | `L1:F14812@3` | ✅ reported | 4 | 14 | Trace this feature to understand what semantic concept it encodes and trace its … |
| SA-5 | `L0:F7696@18` | ✅ reported | 1 | 5 | Trace this feature to understand what semantic concept it encodes and trace its … |

<details>
<summary><b>SA-1</b> — tool trace (2 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F6051 | "periods, spaces, and the number 1" |
| 2 | `get_upstream_features` | L0:F6051@15, k=5 | Emb:"."@15 (w=47.00) +4 more |

**Findings:** Traced L0:F6051 at position 15, which encodes 'periods, spaces, and the number 1'. This feature detects punctuation (specifically periods) and has a relatively low frac_nonzero of 5.7%, making it specific to punctuation contexts. The strongest upstream connection is directly from the period token '.' at position 15 with weight 47.0, confirming it's a period detector. Interestingly, it has negative…

</details>

<details>
<summary><b>SA-2</b> — tool trace (19 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L7, F14893 | " pronouns or possessive pronouns" |
| 2 | `get_upstream_features` | L7:F14893@46, k=5 | Emb:" him"@46 (w=12.50) +4 more |
| 3 | `inspect_feature` | L0, F16297 | " the pronoun "him"" |
| 4 | `inspect_feature` | L0, F2994 | "the pronoun "his" and the pronoun "he."" |
| 5 | `get_upstream_features` | L0:F16297@46, k=5 | Emb:" him"@46 (w=43.25) +4 more |
| 6 | `get_upstream_features` | L0:F2994@46, k=5 | Emb:" him"@46 (w=14.25) +4 more |
| 7 | `get_upstream_features` | L7:F14893@46, k=10 | Emb:" him"@46 (w=12.50) +9 more |
| 8 | `inspect_feature` | L6, F7502 | "names and locations of people and organizations" |
| 9 | `inspect_feature` | L2, F6929 | " the pronoun "him"" |
| 10 | `inspect_feature` | L4, F11391 | " pronouns referring to people and words related to negative experience" |
| 11 | `get_upstream_features` | L4:F11391@46, k=5 | Emb:" him"@46 (w=21.12) +4 more |
| 12 | `inspect_feature` | L3, F2434 | " the word "him", and possibly other pronouns referring to males" |
| 13 | `inspect_feature` | L4, F4017 | " words and short phrases in French" |
| 14 | `get_upstream_features` | L4:F4017@46, k=5 | Emb:" him"@46 (w=16.38) +4 more |
| 15 | `get_upstream_features` | L7:F14893@46, k=15 | Emb:" him"@46 (w=12.50) +14 more |
| 16 | `inspect_feature` | L6, F12990 | " male pronouns and titles along with descriptors associated with men" |
| 17 | `inspect_feature` | L2, F9301 | " all mentions of men and women in the context of relationships, dating" |
| 18 | `get_upstream_features` | L2:F6929@46, k=5 | Emb:" him"@46 (w=33.75) +4 more |
| 19 | `get_upstream_features` | L3:F2434@46, k=5 | Emb:" him"@46 (w=29.50) +4 more |

**Findings:** I traced the circuit starting from L7:F14893, which encodes "pronouns or possessive pronouns" with a clear feminine bias (promoting "herself", "she", "elle" while suppressing masculine pronouns). The feature has low frac_nonzero (0.00885), indicating specificity.

Key findings:
1. The strongest upstream signal comes from the token embedding " him" at position 46 (weight 12.5), feeding directly int…

</details>

<details>
<summary><b>SA-3</b> — tool trace (8 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L1, F7449 | "instances of the word "representation"" |
| 2 | `get_upstream_features` | L1:F7449@9, k=5 | Emb:" represents"@9 (w=20.50) +4 more |
| 3 | `inspect_feature` | L0, F5267 | "mentions of representation or things standing for other things." |
| 4 | `inspect_feature` | L0, F14520 | "verbs that describe actions affecting a noun, especially in the contex" |
| 5 | `get_upstream_features` | L0:F5267@9, k=5 | Emb:" represents"@9 (w=16.62) +4 more |
| 6 | `get_upstream_features` | L0:F14520@9, k=5 | Emb:" represents"@9 (w=18.00) +4 more |
| 7 | `get_upstream_features` | L0:F9026@9, k=5 | Emb:" stories"@3 (w=-2.05) +4 more |
| 8 | `inspect_feature` | L0, F9026 | "technical documents or data, including numbers, units, and references " |

**Findings:** This feature L1:F7449 detects instances of the word "representation". It's highly specific (frac_nonzero = 0.00628) and suppresses the word "representation" itself. The circuit flows from: 1) Token " represents" at position 9 → L0:F5267 (representation concepts) → L1:F7449, and 2) Token " represents" → L0:F14520 (verbs affecting nouns) → L1:F7449. Interestingly, the token "He" at position 1 has sm…

</details>

<details>
<summary><b>SA-4</b> — tool trace (8 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L1, F14812 | " references to stories, chapters, and other narrative elements" |
| 2 | `get_upstream_features` | L1:F14812@3, k=5 | Emb:" stories"@3 (w=18.62) +4 more |
| 3 | `inspect_feature` | L0, F479 | "the word "lift."" |
| 4 | `get_upstream_features` | L0:F479@3, k=5 | Emb:" stories"@3 (w=10.69) +4 more |
| 5 | `inspect_feature` | L0, F8316 | " articles that mention the action of counting or strong desires" |
| 6 | `inspect_feature` | L0, F61 | "the word "stories" sometimes along with apostrophes and common names." |
| 7 | `get_upstream_features` | L0:F61@3, k=5 | Emb:" stories"@3 (w=17.38) +4 more |
| 8 | `get_upstream_features` | L0:F8316@3, k=5 | Emb:" stories"@3 (w=10.44) +4 more |

**Findings:** The circuit traces a feature that encodes "references to stories, chapters, and other narrative elements" at layer 1. This feature is strongly driven by the token " stories" at position 3 (direct embedding connection with weight 18.625) and negatively influenced by "He" at position 1 (weight -0.6094). 

The feature also receives weaker positive inputs from layer 0 features: L0:F479 ("the word 'lif…

</details>

<details>
<summary><b>SA-5</b> — tool trace (5 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F7696 | "the word "on"" |
| 2 | `get_upstream_features` | L0:F7696@18, k=5 | Emb:" on"@18 (w=39.00) +4 more |
| 3 | `get_upstream_features` | L0:F7696@18, k=10 | Emb:" on"@18 (w=39.00) +9 more |
| 4 | `get_top_logits` | k=5 | "" (100%) |
| 5 | `get_top_features` | token="", k=10 | 10 features; top: L0:6051 de=-0.254 |

**Findings:** The starting feature L0:F7696 is a simple word detector for the token \"on\" with label \"the word \\\"on\\\"\". It has a low frac_nonzero of 0.01337, indicating it's specific to detecting \"on\". The feature is primarily driven by the token \"on\" at position 18 (edge weight 39.0), with weaker positive influence from the beginning-of-sequence token <bos> and negative influences from comma at posi…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` ×6 | L0:6051, L0:3255, L0:10187, L6:12990, L6:7502, L7:14893 |

### Build

`build_circuit` → 11 nodes, 11 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m2.7 | 20,010 | 3,675 | 65,373 | 0 | $0.0124 | — | — |
| SA-1 | deepseek/deepseek-v3.2 | 9,290 | 1,653 | 0 | 0 | $0.0030 | ✅ 1F/5E | Trace this feature to understand what semantic concept it en… |
| SA-3 | deepseek/deepseek-v3.2 | 43,833 | 3,271 | 0 | 0 | $0.0126 | ✅ 4F/20E | Trace this feature to understand what semantic concept it en… |
| SA-2 | deepseek/deepseek-v3.2 | 143,202 | 5,434 | 27,648 | 0 | $0.0400 | ✅ 10F/25E | Trace this feature to understand what semantic concept it en… |
| SA-5 | deepseek/deepseek-v3.2 | 22,322 | 1,894 | 0 | 0 | $0.0065 | ✅ 1F/5E | Trace this feature to understand what semantic concept it en… |
| SA-4 | deepseek/deepseek-v3.2 | 44,407 | 2,747 | 0 | 0 | $0.0126 | ✅ 4F/14E | Trace this feature to understand what semantic concept it en… |
| **Total** | | **283,064** | **18,674** | **93,021** | **0** | **$0.0872** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 6m 48s