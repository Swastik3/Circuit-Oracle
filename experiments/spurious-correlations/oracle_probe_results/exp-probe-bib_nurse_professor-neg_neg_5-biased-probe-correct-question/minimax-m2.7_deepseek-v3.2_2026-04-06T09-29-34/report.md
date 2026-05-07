# Circuit Oracle Report
**Date:** 2026-04-06 09:29:34 UTC | **Orchestrator:** minimax/minimax-m2.7 | **Subagent:** deepseek/deepseek-v3.2

## Input

**Prompt:** "Dataset: bib_nurse_professor-neg_neg_5 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "('The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession.',)"

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score is driven almost entirely by a **gender pronoun circuit** rather than genuine profession indicators. The attribution circuit traces back to three input tokens: "His" (pos 1), "He" (pos 10), and "his" (pos 12). These tokens activate a cascade of masculine pronoun features (L7:F14946, L6:F12990, L18:F14743) that have **negative direct effects** on the probe score (-0.4883, -0.3379, -0.2891), while feminine pronoun features (L7:F14893, L19:F8814) have **positive direct effects** (+0.4883, +0.2988). The circuit is dominated by these gender-marked pronoun detectors (frac_nonzero: 0.003-0.087, indicating sparse but gender-specific activation patterns), not profession indicators. A minor biography/education circuit exists connecting "received" → L17:F3683 (biographies) → L8:F7587 (education/professional qualifications), but this path has much lower direct effect on the probe and does not appear in the top-15 features. The model appears to use "His" as a proxy for male gender, which may correlate with certain professions in the training data, rather than detecting genuine profession signals like "professor," "researcher," or academic credentials.

**Confidence:** 9/10

**Reasoning:** The circuit is unambiguously dominated by gender pronoun features. Every top feature by direct effect is a pronoun detector (L7:F14946, L7:F14893, L0:F2994, L6:F12990, L19:F8814, L18:F14743). The upstream tracing confirms these features are directly triggered by the "His"/"He"/"his" token embeddings with very high edge weights (18-44). The biography feature L17:F3683 (which detects "professor of American history at Stanford" and "graduated magna cum lau") exists but has negligible direct effect on the probe output. The user's concern is confirmed: the probe uses spurious gender markers rather than genuine profession indicators to predict the classification.

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L7:14946 de=-0.488 |
| 3 | `inspect_feature` ×8 | L7:14946, L7:14893, L0:2994, L19:8814, L18:14743, L6:12990, L22:12117, L2:5491 |

### Dispatch: 5 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L7:F14946@1` | ✅ reported | 6 | 12 | Trace upstream from the masculine pronoun feature L7:F14946 to find what causes … |
| SA-2 | `L7:F14893@1` | ✅ reported | 7 | 15 | Trace upstream from the feminine pronoun feature L7:F14893 to understand its ori… |
| SA-3 | `L19:F8814@1` | ✅ reported | 8 | 17 | Trace upstream from the pronoun-detecting feature L19:F8814 to find its source. |
| SA-4 | `L18:F14743@10` | ✅ reported | 5 | 9 | Trace upstream from L18:F14743 (which detects "He") at position 10 to find its s… |
| SA-5 | `L0:F2994@12` | ✅ reported | 1 | 5 | Trace upstream from L0:F2994 at position 12 to understand what triggers this pro… |

<details>
<summary><b>SA-1</b> — tool trace (12 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L7, F14946 | " the possessive pronoun "his" (or similar pronouns like "he" and "him"" |
| 2 | `get_upstream_features` | L7:F14946@1, k=5 | Emb:"His"@1 (w=18.38) +4 more |
| 3 | `inspect_feature` | L4, F4315 | " mentions of "his" and other associated pronouns like he, him, or hers" |
| 4 | `inspect_feature` | L6, F12990 | " male pronouns and titles along with descriptors associated with men" |
| 5 | `get_upstream_features` | L4:F4315@1, k=5 | Emb:"His"@1 (w=23.50) +4 more |
| 6 | `get_upstream_features` | L6:F12990@1, k=5 | Emb:"His"@1 (w=4.91) +4 more |
| 7 | `inspect_feature` | L0, F2994 | "the pronoun "his" and the pronoun "he."" |
| 8 | `get_upstream_features` | L0:F2994@1, k=5 | Emb:"His"@1 (w=19.75) +4 more |
| 9 | `inspect_feature` | L2, F5491 | "references to God in the third person." |
| 10 | `get_upstream_features` | L2:F5491@1, k=5 | Emb:"His"@1 (w=23.88) +4 more |
| 11 | `inspect_feature` | L1, F7439 | " the possessive pronouns "his" and "him"" |
| 12 | `get_upstream_features` | L1:F7439@1, k=5 | Emb:"His"@1 (w=16.38) +4 more |

**Findings:** The masculine pronoun feature L7:F14946 is primarily driven directly by the input token embedding "His" at position 1 with a very strong edge weight of 18.375. The circuit shows multiple parallel pathways:

1. Direct embedding connection: "His" token → L7:F14946 (weight: 18.375)
2. Intermediate feature pathways: 
   - "His" → L4:F4315 → L7:F14946
   - "His" → L6:F12990 → L7:F14946
   - "His" → L0:…

</details>

<details>
<summary><b>SA-2</b> — tool trace (12 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L7, F14893 | " pronouns or possessive pronouns" |
| 2 | `get_upstream_features` | L7:F14893@1, k=5 | Emb:"His"@1 (w=23.50) +4 more |
| 3 | `inspect_feature` | L6, F12990 | " male pronouns and titles along with descriptors associated with men" |
| 4 | `inspect_feature` | L4, F4315 | " mentions of "his" and other associated pronouns like he, him, or hers" |
| 5 | `get_upstream_features` | L6:F12990@1, k=5 | Emb:"His"@1 (w=4.91) +4 more |
| 6 | `get_upstream_features` | L4:F4315@1, k=5 | Emb:"His"@1 (w=23.50) +4 more |
| 7 | `inspect_feature` | L0, F2994 | "the pronoun "his" and the pronoun "he."" |
| 8 | `inspect_feature` | L2, F5491 | "references to God in the third person." |
| 9 | `get_upstream_features` | L0:F2994@1, k=5 | Emb:"His"@1 (w=19.75) +4 more |
| 10 | `inspect_feature` | L1, F7439 | " the possessive pronouns "his" and "him"" |
| 11 | `get_upstream_features` | L1:F7439@1, k=5 | Emb:"His"@1 (w=16.38) +4 more |
| 12 | `inspect_feature` | L5, F10952 | "third person pronouns in varying contexts" |

**Findings:** The feminine pronoun feature at L7:F14893 originates primarily from the input token "His" at position 1 (embedding edge_weight: 23.5). This suggests the feature activates in response to masculine pronouns to potentially generate feminine alternatives. The circuit shows a complex network of pronoun-related features:

1. Direct "His" token embedding strongly activates the feminine feature
2. L6 male…

</details>

<details>
<summary><b>SA-3</b> — tool trace (15 calls)</summary>

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
| 10 | `inspect_feature` | L0, F2994 | "the pronoun "his" and the pronoun "he."" |
| 11 | `inspect_feature` | L4, F4315 | " mentions of "his" and other associated pronouns like he, him, or hers" |
| 12 | `inspect_feature` | L6, F12990 | " male pronouns and titles along with descriptors associated with men" |
| 13 | `inspect_feature` | L15, F851 | " code documentation blocks in various programming languages" |
| 14 | `get_upstream_features` | L0:F2994@1, k=5 | Emb:"His"@1 (w=19.75) +4 more |
| 15 | `get_upstream_features` | L4:F4315@1, k=5 | Emb:"His"@1 (w=23.50) +4 more |

**Findings:** Tracing upstream from pronoun-detecting feature L19:F8814 reveals a circuit centered on processing the masculine pronoun "His". The feature promotes feminine pronouns ("herself", "she", "her") and suppresses masculine pronouns. Surprisingly, it receives strong positive connections from both masculine-pronoun-detecting features (L18:F7400, L7:F14946) and the token embedding "His" itself, while rece…

</details>

<details>
<summary><b>SA-4</b> — tool trace (10 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L18, F14743 | "He" |
| 2 | `get_upstream_features` | L18:F14743@10, k=5 | Emb:" He"@10 (w=22.38) +4 more |
| 3 | `inspect_feature` | L0, F1069 | " references to a male person, particularly when using the pronoun "He"" |
| 4 | `inspect_feature` | L17, F5889 | " references to people with pronouns and possessive pronouns" |
| 5 | `inspect_feature` | L15, F3330 | " personal stories of individuals, especially women and their actions o" |
| 6 | `get_upstream_features` | L0:F1069@10, k=5 | Emb:" He"@10 (w=35.75) +4 more |
| 7 | `get_upstream_features` | L17:F5889@10, k=5 | Emb:" He"@10 (w=21.75) +4 more |
| 8 | `get_upstream_features` | L15:F3330@10, k=5 | Emb:" He"@10 (w=17.00) +4 more |
| 9 | `inspect_feature` | L12, F7896 | " third-person pronouns, especially 'he' and 'she', near a form of the " |
| 10 | `get_upstream_features` | L12:F7896@10, k=5 | Emb:" He"@10 (w=15.50) +4 more |

**Findings:** The circuit for detecting "He" at position 10 traces primarily back to the input token " He" itself. The strongest direct connection is from the embedding of token " He" at position 10 to the final "He" detector at layer 18 (weight 22.375). 

Key findings:
1. Layer 0 feature 1069 (frac_nonzero 0.0078) detects male pronouns and connects strongly from token " He" (weight 35.75) and then to the final…

</details>

<details>
<summary><b>SA-5</b> — tool trace (2 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F2994 | "the pronoun "his" and the pronoun "he."" |
| 2 | `get_upstream_features` | L0:F2994@12, k=5 | Emb:" his"@12 (w=44.50) +4 more |

**Findings:** The pronoun feature L0:F2994 at position 12 is primarily triggered by the token " his" at the same position (position 12) with an extremely strong edge weight of 44.5. This feature detects the pronoun "his" and "he." but interestingly suppresses "his" from being output (it appears in suppressed_tokens). The feature promotes formatting tokens like spaces, periods, and newlines instead. Other weaker…

</details>

### Re-dispatch (round 2): 1 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-6 | `L17:F3683@11` | ✅ reported | 9 | 40 | Trace upstream from the biography feature L17:F3683 at position 11 to understand… |

<details>
<summary><b>SA-6</b> — tool trace (18 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L17, F3683 | "biographies" |
| 2 | `get_upstream_features` | L17:F3683@11, k=5 | Emb:" received"@11 (w=6.41) +4 more |
| 3 | `inspect_feature` | L15, F9968 | " mentions of `received` with some context words in proximity" |
| 4 | `get_upstream_features` | L15:F9968@11, k=5 | Emb:" received"@11 (w=47.25) +4 more |
| 5 | `inspect_feature` | L3, F6253 | "the word "receive" and its inflections." |
| 6 | `get_upstream_features` | L3:F6253@11, k=5 | Emb:" received"@11 (w=21.75) +4 more |
| 7 | `inspect_feature` | L6, F13838 | " words or code related to Android app development, specifically concer" |
| 8 | `get_upstream_features` | L6:F13838@11, k=5 | Emb:" received"@11 (w=14.50) +4 more |
| 9 | `inspect_feature` | L2, F3992 | " instances of people or things receiving something" |
| 10 | `get_upstream_features` | L2:F3992@11, k=5 | Emb:" received"@11 (w=23.12) +4 more |
| 11 | `inspect_feature` | L0, F11835 | "terms used in software code such as "assembly", "using", "namespace", " |
| 12 | `get_upstream_features` | L17:F3683@11, k=10 | Emb:" received"@11 (w=6.41) +9 more |
| 13 | `inspect_feature` | L15, F15263 | " names and dates" |
| 14 | `get_upstream_features` | L15:F15263@11, k=5 | Emb:" received"@11 (w=6.97) +4 more |
| 15 | `inspect_feature` | L8, F7587 | " words related to education and professional qualifications" |
| 16 | `get_upstream_features` | L8:F7587@11, k=5 | Emb:" received"@11 (w=7.38) +4 more |
| 17 | `inspect_feature` | L4, F11633 | " words related to education and employment history" |
| 18 | `inspect_feature` | L11, F1301 | " mentions of people's education and professional careers" |

**Findings:** The biography feature L17:F3683 is part of a circuit that detects biographical information. Its strongest upstream connections come directly from embedding tokens: "received" (pos 11, weight 6.4062), "He" (pos 10, weight 2.8281), and "research" (pos 2, weight 2.5469). These tokens are likely from a sentence like "He received research..." in a biographical context.

The circuit integrates multiple …

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` ×3 | L4:4315, L18:7400, L18:10315 |
| 2 | `get_upstream_features` | L22:F12117@11, k=10 → L21:F4895 (w=5.69) +9 more |
| 3 | `inspect_feature` ×3 | L21:4895, L20:10934, L17:3683 |

### Build

`build_circuit` → 11 nodes, 15 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m2.7 | 69,379 | 5,374 | 107,480 | 0 | $0.0305 | — | — |
| SA-1 | deepseek/deepseek-v3.2 | 81,680 | 3,473 | 0 | 0 | $0.0226 | ✅ 6F/12E | Trace upstream from the masculine pronoun feature L7:F14946 … |
| SA-2 | deepseek/deepseek-v3.2 | 77,224 | 3,866 | 5,760 | 0 | $0.0217 | ✅ 7F/15E | Trace upstream from the feminine pronoun feature L7:F14893 t… |
| SA-3 | deepseek/deepseek-v3.2 | 102,800 | 4,630 | 20,928 | 0 | $0.0290 | ✅ 8F/17E | Trace upstream from the pronoun-detecting feature L19:F8814 … |
| SA-5 | deepseek/deepseek-v3.2 | 9,037 | 1,443 | 0 | 0 | $0.0029 | ✅ 1F/5E | Trace upstream from L0:F2994 at position 12 to understand wh… |
| SA-4 | deepseek/deepseek-v3.2 | 63,118 | 3,913 | 3,648 | 0 | $0.0180 | ✅ 5F/9E | Trace upstream from L18:F14743 (which detects "He") at posit… |
| SA-6 | deepseek/deepseek-v3.2 | 127,204 | 6,437 | 27,584 | 0 | $0.0362 | ✅ 9F/40E | Trace upstream from the biography feature L17:F3683 at posit… |
| **Total** | | **530,442** | **29,136** | **165,400** | **0** | **$0.1609** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 12m 3s