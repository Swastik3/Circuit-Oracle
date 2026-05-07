# Circuit Oracle Report
**Date:** 2026-04-06 17:14:50 UTC | **Orchestrator:** minimax/minimax-m2.7 | **Subagent:** deepseek/deepseek-v3.2

## Input

**Prompt:** "Dataset: multinli-pos_pos_5 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "('The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction.',)"

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The contradiction probe's classification is driven primarily by **negation/contrast word signals** (specifically "but" and "not only... but also" patterns) rather than genuine semantic understanding of the contradiction content.

**Confidence:** 9/10

**Reasoning:**

The attribution circuit confirms the user's concern with high confidence. The probe's classification is dominated by spurious linguistic patterns:

1. **Primary Driver — "But" Contrast Feature (L15:12905):** This is the top feature with direct_effect = -0.3574 (the strongest single influence). It detects "the word 'but' along with surrounding words that indicate a contrasting or consequential relationship" with very specific activation (frac_nonzero = 0.00526). The signal flows: Emb:"but"(pos13, weight=42.5) → L0:11101 "sentences containing but" → L2:3379 "but and similar terms" → L4:2884 "but and contrastive conjunctions" → L15:12905 "but with contrast signals."

2. **"Not only... but also" Cascade:** Multiple layers (L2:5627, L9:12274, L14:10765, L15:1990) form a hierarchical detector for the "not only... but also" construction, feeding into both L15:12905 and L17:3763. This is a grammatical pattern that signals contrast, but the model uses it as a shortcut for contradiction detection.

3. **Broad "Only" Feature (L17:3763):** With direct_effect = +0.165 and frac_nonzero = 0.07178 (broad firing), this feature fires across many contexts and promotes "but" in its output — indicating it's part of the same spurious pattern-matching circuit rather than semantic content.

4. **Content Features Are Weak:** The "program" word feature (L2:13565, direct_effect = 0.1973) and attribution pattern (L5:7144, direct_effect = 0.2158) have smaller influence than the "but" feature alone.

**Conclusion:** The circuit relies on surface-level negation word patterns ("but", "not only", "only") as shortcuts for detecting contradiction, rather than understanding the actual semantic conflict between "will help improve" and "isn't going to improve." This is a classic example of using spurious linguistic correlates rather than genuine semantic reasoning.

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 10 features; top: L15:12905 de=-0.357 |
| 3 | `inspect_feature` ×5 | L15:12905, L5:7144, L2:13565, L3:2782, L17:3763 |

### Dispatch: 5 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L15:F12905@13` | ✅ reported | 9 | 26 | Trace the 'but' contrast feature (L15:12905) upstream to find what features/inpu… |
| SA-2 | `L5:F7144@3` | ✅ reported | 7 | 25 | Trace the 'proper nouns followed by said' attribution feature (L5:7144) upstream… |
| SA-3 | `L2:F13565@5` | ✅ reported | 5 | 20 | Trace the 'program' word feature (L2:13565) upstream to understand how content f… |
| SA-4 | `L17:F3763@7` | ✅ reported | 7 | 20 | Trace the 'only' feature (L17:3763) upstream to find its source. This is a negat… |
| SA-5 | `L0:F11101@13` | ✅ reported | 1 | 1 | Trace the L0:11101 'sentences containing but' feature to understand how the 'but… |

<details>
<summary><b>SA-1</b> — tool trace (15 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L15, F12905 | " the word "but" along with surrounding words that indicate a contrasti" |
| 2 | `get_upstream_features` | L15:F12905@13, k=5 | Emb:" only"@7 (w=5.94) +4 more |
| 3 | `inspect_feature` | L2, F5627 | " instances of the phrase "not only"" |
| 4 | `inspect_feature` | L9, F12274 | " the phrase "not only"" |
| 5 | `inspect_feature` | L4, F2884 | "the word "but" and other contrastive conjunctions and adverbs." |
| 6 | `get_upstream_features` | L4:F2884@13, k=5 | Emb:" but"@13 (w=17.75) +4 more |
| 7 | `inspect_feature` | L2, F3379 | " the word "but" and similar terms" |
| 8 | `get_upstream_features` | L2:F3379@13, k=5 | Emb:" but"@13 (w=20.75) +4 more |
| 9 | `inspect_feature` | L0, F11101 | "sentences that contain the word "but"" |
| 10 | `get_upstream_features` | L0:F11101@13, k=5 | Emb:" but"@13 (w=42.50) +4 more |
| 11 | `get_upstream_features` | L2:F5627@7, k=5 | Emb:" only"@7 (w=21.38) +4 more |
| 12 | `inspect_feature` | L0, F12483 | "the word "only"" |
| 13 | `inspect_feature` | L0, F4723 | " the word "only"" |
| 14 | `get_upstream_features` | L9:F12274@7, k=5 | L6:F3655 (w=9.19) +4 more |
| 15 | `inspect_feature` | L6, F3655 | " the word "just" and surrounding words" |

**Findings:** Tracing the 'but' contrast feature (L15:12905) upstream reveals it connects to genuine semantic content, not spurious patterns. The circuit shows:

1. L15:12905 ("the word 'but' along with surrounding words that indicate a contrasting or consequential relationship") is strongly fed by:
   - Direct token embeddings: "only" (pos 7, weight 5.94) and "but" (pos 13, weight 4.03)
   - "not only" feature…

</details>

<details>
<summary><b>SA-2</b> — tool trace (13 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L5, F7144 | " proper nouns followed by the word "said"" |
| 2 | `get_upstream_features` | L5:F7144@3, k=5 | L3:F16191 (w=2.97) +4 more |
| 3 | `inspect_feature` | L3, F16191 | " verbs or legal names, pointing to its use in citing facts or sources" |
| 4 | `inspect_feature` | L4, F5007 | "words and phrases used in legal contexts, like testimony and arguments" |
| 5 | `get_upstream_features` | L3:F16191@3, k=5 | Emb:"<bos>"@0 (w=1.77) +4 more |
| 6 | `get_upstream_features` | L4:F5007@3, k=5 | Emb:" said"@3 (w=4.28) +4 more |
| 7 | `inspect_feature` | L3, F41 | " citations to other papers, specifically looking for "*et al.*"" |
| 8 | `inspect_feature` | L0, F4789 | " names, especially last names, which often contain "thaler"" |
| 9 | `inspect_feature` | L0, F4871 | " place names in Germany and people discussing missile defense" |
| 10 | `get_upstream_features` | L3:F41@3, k=5 | Emb:" said"@3 (w=5.66) +4 more |
| 11 | `inspect_feature` | L1, F173 | "dialogue being spoken or narrated" |
| 12 | `get_upstream_features` | L0:F4789@2, k=5 | Emb:"heim"@2 (w=6.91) +4 more |
| 13 | `get_upstream_features` | L0:F4871@2, k=5 | Emb:"heim"@2 (w=10.81) +4 more |

**Findings:** I traced the 'proper nouns followed by the word \"said\"' feature (L5:7144) upstream to discover a circuit that detects proper noun + \"said\" patterns. The feature is primarily fed by:

1. L3:16191 (edge_weight 2.97) - detects verbs/legal names in citation contexts
2. Direct embedding of \" said\" token (edge_weight 2.30)
3. L4:5007 (edge_weight 1.63) - legal context/testimony words

Key upstream…

</details>

<details>
<summary><b>SA-3</b> — tool trace (9 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L2, F13565 | " the word "program(me)s"" |
| 2 | `get_upstream_features` | L2:F13565@5, k=5 | Emb:" program"@5 (w=16.75) +4 more |
| 3 | `inspect_feature` | L1, F11907 | " the word "program"" |
| 4 | `inspect_feature` | L0, F14950 | " instances of the word "program" and the word "step"" |
| 5 | `inspect_feature` | L0, F7448 | " the word "program" related to sports, school, health, or television" |
| 6 | `get_upstream_features` | L1:F11907@5, k=5 | Emb:" program"@5 (w=24.25) +4 more |
| 7 | `get_upstream_features` | L0:F7448@5, k=5 | Emb:" program"@5 (w=11.00) +4 more |
| 8 | `get_upstream_features` | L0:F14950@5, k=5 | Emb:" program"@5 (w=23.25) +4 more |
| 9 | `inspect_feature` | L0, F9026 | "technical documents or data, including numbers, units, and references " |

**Findings:** The circuit for the 'program' word feature (L2:13565) shows a direct and strong connection from the embedding of the token " program" at position 5 (weight 16.75). This feature also receives inputs from other features:

1. L1:11907 detects "program" but has negative influence (-1.78) on our target, suggesting competition or inhibition
2. L0:7448 detects "program" in specific contexts (sports, scho…

</details>

<details>
<summary><b>SA-4</b> — tool trace (12 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L17, F3763 | "only" |
| 2 | `get_upstream_features` | L17:F3763@7, k=5 | L15:F1990 (w=10.38) +4 more |
| 3 | `inspect_feature` | L15, F1990 | "the phrase "not only"" |
| 4 | `inspect_feature` | L14, F10765 | "the phrase "not only"" |
| 5 | `inspect_feature` | L9, F12274 | " the phrase "not only"" |
| 6 | `inspect_feature` | L2, F5627 | " instances of the phrase "not only"" |
| 7 | `get_upstream_features` | L15:F1990@7, k=5 | Emb:" not"@6 (w=9.69) +4 more |
| 8 | `get_upstream_features` | L14:F10765@7, k=5 | L9:F12274 (w=7.97) +4 more |
| 9 | `inspect_feature` | L13, F15220 | " various common and seemingly insignificant words, particularly in com" |
| 10 | `get_upstream_features` | L2:F5627@7, k=5 | Emb:" only"@7 (w=21.38) +4 more |
| 11 | `get_upstream_features` | L9:F12274@7, k=5 | L6:F3655 (w=9.19) +4 more |
| 12 | `inspect_feature` | L6, F3655 | " the word "just" and surrounding words" |

**Findings:** I traced the 'only' feature (L17:3763) upstream through a hierarchical circuit that detects the phrase "not only". The strongest connections come from features specifically detecting "not only" at layers 15, 14, 9, and 2. These lower-layer "not only" detectors are themselves primarily fed by the raw token embeddings of "not" (position 6) and "only" (position 7). The circuit shows a clear pattern: …

</details>

<details>
<summary><b>SA-5</b> — tool trace (2 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F11101 | "sentences that contain the word "but"" |
| 2 | `get_upstream_features` | L0:F11101@13, k=5 | Emb:" but"@13 (w=42.50) +4 more |

**Findings:** The circuit for the 'sentences containing but' feature (L0:11101) is extremely direct: it receives its primary signal directly from the token embedding of " but" at position 13 with a very strong edge weight of 42.5. This shows that the feature functions as a simple 'but' detector - it activates when the word "but" appears in the input. The feature has a low frac_nonzero of 0.035, indicating it's …

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L0:F8046@8, k=5 → Emb:" will"@8 (w=37.75) +4 more |

### Build

`build_circuit` → 14 nodes, 18 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m2.7 | 32,288 | 4,283 | 45,223 | 0 | $0.0162 | — | — |
| SA-3 | deepseek/deepseek-v3.2 | 53,014 | 3,338 | 0 | 0 | $0.0151 | ✅ 5F/20E | Trace the 'program' word feature (L2:13565) upstream to unde… |
| SA-2 | deepseek/deepseek-v3.2 | 90,071 | 3,675 | 0 | 0 | $0.0248 | ✅ 7F/25E | Trace the 'proper nouns followed by said' attribution featur… |
| SA-4 | deepseek/deepseek-v3.2 | 85,222 | 3,942 | 0 | 0 | $0.0237 | ✅ 7F/20E | Trace the 'only' feature (L17:3763) upstream to find its sou… |
| SA-1 | deepseek/deepseek-v3.2 | 91,498 | 4,955 | 25,472 | 0 | $0.0263 | ✅ 9F/26E | Trace the 'but' contrast feature (L15:12905) upstream to fin… |
| SA-5 | deepseek/deepseek-v3.2 | 9,214 | 784 | 0 | 0 | $0.0027 | ✅ 1F/1E | Trace the L0:11101 'sentences containing but' feature to und… |
| **Total** | | **361,307** | **20,977** | **70,695** | **0** | **$0.1087** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 5m 55s