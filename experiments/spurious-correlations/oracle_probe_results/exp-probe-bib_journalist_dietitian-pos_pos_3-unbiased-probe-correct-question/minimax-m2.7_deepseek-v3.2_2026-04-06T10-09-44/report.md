# Circuit Oracle Report
**Date:** 2026-04-06 10:09:44 UTC | **Orchestrator:** minimax/minimax-m2.7 | **Subagent:** deepseek/deepseek-v3.2

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-pos_pos_3 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "('The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession.',)"

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification is driven primarily by **gender marker features** (female pronoun "her" at position 12) rather than genuine profession indicators. The circuit shows a cascade from the "her" token embedding through multiple female-reference detection features (L0:F7509 → L6:F11646), with L6:F11646 promoting female words like "herself," "she," and "her" while suppressing male words like "himself." The profession-related "nurse" feature (L0:F8854) plays only a minor role with a small direct_effect of 0.0762, compared to the gender marker's direct_effect of 0.0762-0.1484.

**Confidence:** 9/10

**Reasoning:** The circuit built from build_circuit confirms the user's concern with high confidence. The attribution graph reveals:

1. **Primary Driver - Gender Markers:** The strongest pathway originates from the **"her" token at position 12** (edge weight 42.25) and feeds into:
   - **L0:F7509** (female pronoun detector, frac_nonzero=0.047)
   - **L1:F4232** (possessive pronoun "her", frac_nonzero=0.00916)
   - **L6:F11646** (female reference detector, frac_nonzero=0.01976)

2. **L6:F11646** explicitly encodes "references to women" with top activating examples containing "her" (max activation 68.064) and promotes female tokens ("herself," "she," "her") while suppressing male tokens ("himself").

3. **Minor Role for Profession:** The "nurse" detector **L0:F8854** (which detects "the word 'nurse' as well as some pronouns") has a direct_effect of only 0.0762, comparable to the gender marker features but plays a secondary role. The food/lunch-related features (L1:F9413, L2:F14626, L2:F6319) are context-dependent but do not drive the probe's primary classification.

4. **Spurious Correlation:** The probe appears to learn that "her" co-occurs with certain professions in training data (likely nursing/teaching) and uses this gender marker as a shortcut rather than detecting genuine profession-related semantic features.

The circuit confirms the probe uses **spurious gender markers** rather than **genuine profession indicators** to drive its classification.

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 10 features; top: L0:16271 de=0.148 |

### Dispatch: 3 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L0:F16271@6` | ✅ reported | 2 | 8 | Trace this feature upstream to understand what drives the probe's classification… |
| SA-2 | `L2:F14626@8` | ✅ reported | 8 | 16 | Trace this feature upstream to understand what drives the probe's classification… |
| SA-3 | `L0:F7509@12` | ✅ reported | 1 | 5 | Trace this feature upstream to understand what drives the probe's classification… |

<details>
<summary><b>SA-1</b> — tool trace (4 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F16271 | " the word "while"" |
| 2 | `get_upstream_features` | L0:F16271@6, k=5 | Emb:" while"@6 (w=20.25) +4 more |
| 3 | `get_upstream_features` | L0:F16271@6, k=10 | Emb:" while"@6 (w=20.25) +9 more |
| 4 | `inspect_feature` | L0, F3075 | " lines of text containing the string 'http', often as part of a URL" |

**Findings:** Tracing from L0:F16271 (a feature detecting the word "while") shows it is primarily driven directly by the token embedding of "while" at position 6 with a very strong edge weight of 20.25. This is a simple word detector feature at layer 0. The feature has low frac_nonzero (0.0048), indicating it's specific to detecting the word "while". There are minor influences from surrounding tokens like "<bos…

</details>

<details>
<summary><b>SA-2</b> — tool trace (12 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L2, F14626 | " mentions of lunchtime meals" |
| 2 | `get_upstream_features` | L2:F14626@8, k=5 | Emb:" lunch"@8 (w=33.75) +4 more |
| 3 | `inspect_feature` | L0, F8048 | " the word "lead" when it is being used as a verb that describes someth" |
| 4 | `inspect_feature` | L0, F491 | "the word "upon"" |
| 5 | `inspect_feature` | L1, F9413 | "mentions of "lunch"" |
| 6 | `get_upstream_features` | L0:F8048@8, k=5 | Emb:" lunch"@8 (w=17.88) +4 more |
| 7 | `get_upstream_features` | L0:F491@8, k=5 | Emb:" lunch"@8 (w=20.62) +4 more |
| 8 | `get_upstream_features` | L1:F9413@8, k=5 | Emb:" lunch"@8 (w=17.25) +4 more |
| 9 | `inspect_feature` | L0, F8854 | " the word "nurse" as well as some pronouns" |
| 10 | `get_upstream_features` | L0:F8854@8, k=5 | Emb:" lunch"@8 (w=18.38) +4 more |
| 11 | `inspect_feature` | L0, F2265 | " terms related to food, specifically ingredients and dishes" |
| 12 | `inspect_feature` | L0, F14653 | "the word "loud"" |

**Findings:** Tracing L2:F14626 ("mentions of lunchtime meals") revealed that it is primarily driven directly by the token embedding of " lunch" at position 8 (weight 33.75). The circuit shows interesting competition patterns: 

1. Layer 0 features that detect "lead" (verb), "upon", and "nurse" positively contribute to the target feature, while layer 1 feature F9413 (also "mentions of 'lunch'") negatively affec…

</details>

<details>
<summary><b>SA-3</b> — tool trace (2 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F7509 | " female pronouns and words like daughter and husband that refer to wom" |
| 2 | `get_upstream_features` | L0:F7509@12, k=5 | Emb:" her"@12 (w=42.25) +4 more |

**Findings:** Tracing from L0:F7509 reveals it's a feature that detects female pronouns like "her". The strongest upstream connection is directly from the token embedding " her" at position 12 with a very high edge weight of 42.25. Other weaker connections come from context tokens: " school" (pos 10), " lunch" (pos 8), " eating" (pos 7), and "<bos>" (beginning marker). The feature label confirms it encodes fema…

</details>

### Re-dispatch (round 2): 2 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-4 | `L2:F6319@8` | ✅ reported | 7 | 21 | Trace this feature to understand what semantic concept it encodes. Look for gend… |
| SA-5 | `L6:F11646@12` | ✅ reported | 5 | 8 | Trace this feature to understand what semantic concept it encodes. Look for gend… |

<details>
<summary><b>SA-4</b> — tool trace (11 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L2, F6319 | " words related to dining and food" |
| 2 | `get_upstream_features` | L2:F6319@8, k=5 | Emb:" lunch"@8 (w=16.88) +4 more |
| 3 | `inspect_feature` | L1, F9413 | "mentions of "lunch"" |
| 4 | `inspect_feature` | L1, F5530 | " words relating to meals, ingredients, and food consumption" |
| 5 | `get_upstream_features` | L1:F9413@8, k=5 | Emb:" lunch"@8 (w=17.25) +4 more |
| 6 | `inspect_feature` | L0, F8854 | " the word "nurse" as well as some pronouns" |
| 7 | `get_upstream_features` | L0:F8854@8, k=5 | Emb:" lunch"@8 (w=18.38) +4 more |
| 8 | `get_upstream_features` | L1:F5530@8, k=5 | Emb:" eating"@7 (w=7.19) +4 more |
| 9 | `inspect_feature` | L0, F2265 | " terms related to food, specifically ingredients and dishes" |
| 10 | `inspect_feature` | L1, F15373 | "the word "bus" in code or computer architecture contexts" |
| 11 | `inspect_feature` | L0, F16042 | "passages that list the pros and cons of comparing different approaches" |

**Findings:** I traced the circuit starting from L2:F6319 ("words related to dining and food") at position 8. The circuit reveals a food-related processing pathway with an interesting gender/profession connection:

1. The strongest input is directly from the token embedding " lunch" at position 8 (weight 16.875), with weaker input from " eating" at position 7.

2. The feature integrates signals from two layer 1…

</details>

<details>
<summary><b>SA-5</b> — tool trace (8 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F11646 | " references to women, potentially triggered by pronouns and titles" |
| 2 | `get_upstream_features` | L6:F11646@12, k=5 | Emb:" her"@12 (w=35.00) +4 more |
| 3 | `inspect_feature` | L0, F7509 | " female pronouns and words like daughter and husband that refer to wom" |
| 4 | `inspect_feature` | L1, F4232 | " the possessive pronoun "her"" |
| 5 | `inspect_feature` | L4, F7864 | "xml or source code snippets, especially tags and possibly keywords in " |
| 6 | `get_upstream_features` | L0:F7509@12, k=5 | Emb:" her"@12 (w=42.25) +4 more |
| 7 | `get_upstream_features` | L1:F4232@12, k=5 | Emb:" her"@12 (w=39.75) +4 more |
| 8 | `inspect_feature` | L0, F5264 | " possessive pronouns (his/her/their/its)" |

**Findings:** The tracing reveals a circuit for detecting female gender references. The target feature L6:F11646 encodes "references to women, potentially triggered by pronouns and titles" and primarily activates on the pronoun "her". 

Key findings:
1. The strongest connection is directly from the token embedding " her" at position 12 to L6:F11646 with weight 35.0 - this is the primary driver.
2. An interestin…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L0:F7509@12, k=8 → Emb:" her"@12 (w=42.25) +7 more |
| 2 | `get_top_features` | token="", k=15 → 15 features; top: L0:16271 de=0.148 |
| 3 | `inspect_feature` ×3 | L0:7509, L6:11646, L0:8854 |

### Build

`build_circuit` → 10 nodes, 13 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m2.7 | 27,015 | 4,553 | 64,925 | 0 | $0.0155 | — | — |
| SA-3 | deepseek/deepseek-v3.2 | 9,161 | 1,392 | 0 | 0 | $0.0029 | ✅ 1F/5E | Trace this feature upstream to understand what drives the pr… |
| SA-1 | deepseek/deepseek-v3.2 | 18,117 | 1,636 | 0 | 0 | $0.0053 | ✅ 2F/8E | Trace this feature upstream to understand what drives the pr… |
| SA-2 | deepseek/deepseek-v3.2 | 81,006 | 3,815 | 0 | 0 | $0.0225 | ✅ 8F/16E | Trace this feature upstream to understand what drives the pr… |
| SA-5 | deepseek/deepseek-v3.2 | 46,820 | 2,395 | 0 | 0 | $0.0131 | ✅ 5F/8E | Trace this feature to understand what semantic concept it en… |
| SA-4 | deepseek/deepseek-v3.2 | 72,027 | 4,357 | 0 | 0 | $0.0204 | ✅ 7F/21E | Trace this feature to understand what semantic concept it en… |
| **Total** | | **254,146** | **18,148** | **64,925** | **0** | **$0.0797** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 6m 34s