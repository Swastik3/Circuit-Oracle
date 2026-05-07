# Circuit Oracle Report
**Date:** 2026-04-06 10:38:17 UTC | **Orchestrator:** minimax/minimax-m2.7 | **Subagent:** deepseek/deepseek-v3.2

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-pos_pos_4 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "('The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession.',)"

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score for identifying a Dietitian/Nutritionist profession is driven by two converging pathways: (1) a **substring pattern-matching circuit** that detects "Die"+"te" character sequences (from words like "Dietetics"/"Dietitian") via early-layer features (L1-L3) and feeds into dietary health and nutrition content detectors (L4-L14-L19), and (2) a **genuine profession indicator** that directly detects the token "titian" at position 37 (from "Dietitian") via L2:F2589. The circuit also includes L0:F14824 which detects "has" but this is a **generic lexical feature** (frac_nonzero=0.011, minimal connection to "She" with weight 1.15 vs 32.75 for "has" itself) — **NOT a gender-correlated spurious feature** as initially suspected.

**Confidence:** 8/10

**Reasoning:** The circuit analysis reveals:

1. **Primary pathway uses substring patterns**: The dominant driver is the "Die"+"te" substring combination at positions 20-21 (from "Dietetics"/"Dietitian"), not semantic content. L0:7699 ("words starting with D") and L0:4058 ("the word 'die'") feed into L2:F7473 (weight=19) and L1:F1083 (weight=22.25), creating a pattern-matching pipeline rather than genuine word recognition.

2. **Genuine profession indicator exists**: L2:F2589 ("words related to medical professionals and medical specialties") directly detects "titian" at position 37 with weight=19.125, representing a legitimate profession-specific marker from "Dietitian."

3. **No gender spurious feature**: L0:F14824 ("the word 'has'") has minimal gender correlation — the edge from "She" to this feature has weight 1.15 versus 32.75 from "has" itself. The frac_nonzero=0.011 indicates low selectivity, confirming this is a generic auxiliary verb detector.

4. **Late-layer convergence**: L19:F1589 ("context of nutritional studies") integrates signals from multiple mid-layer features (L4:F13412, L6:F11327, L14:F4197) representing food/nutrition content, but these all trace back to the substring pattern origin.

The circuit uses legitimate profession terminology ("titian", "Diet"/"dietary" related features) rather than gender markers, though the reliance on substring pattern matching ("Die"+"te") rather than whole-word recognition represents a superficial linguistic shortcut rather than deep semantic understanding.

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 10 features; top: L4:13412 de=0.154 |
| 3 | `inspect_feature` ×4 | L4:13412, L0:14824, L19:1589, L6:11327 |

### Dispatch: 3 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L4:F13412@21` | ✅ reported | 2964 | 17 | Trace the path from L4:13412 (terms related to diets and dietary health) upstrea… |
| SA-2 | `L19:F1589@21` | ✅ reported | 9 | 13 | Trace the path from L19:1589 (context of nutritional studies) upstream. Identify… |
| SA-3 | `L0:F14824@2` | ✅ reported | 1 | 3 | Trace the path from L0:14824 (the word 'has') upstream. This is concerning becau… |

<details>
<summary><b>SA-1</b> — tool trace (13 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F13412 | " terms related to diets and dietary health" |
| 2 | `get_upstream_features` | L4:F13412@21, k=5 | L3:F11774 (w=4.84) +4 more |
| 3 | `inspect_feature` | L3, F11774 | " what appears to be a smattering of strings related to scientific nota" |
| 4 | `inspect_feature` | L3, F10028 | "words or short phrases that include "made of/from", and words ending w" |
| 5 | `get_upstream_features` | L3:F11774@21, k=5 | Emb:" Die"@20 (w=5.88) +4 more |
| 6 | `get_upstream_features` | L3:F10028@21, k=5 | Emb:" Die"@20 (w=6.94) +4 more |
| 7 | `inspect_feature` | L2, F7473 | " capitalized two letter prefixes or suffixes" |
| 8 | `inspect_feature` | L2, F1984 | " strings of letters that appear to be fragments of names, especially p" |
| 9 | `get_upstream_features` | L2:F7473@21, k=5 | Emb:" Die"@20 (w=19.00) +4 more |
| 10 | `inspect_feature` | L1, F1083 | " the characters "te" within code and/or non-English words" |
| 11 | `inspect_feature` | L0, F7699 | "words and abbreviations starting with the letter "D"" |
| 12 | `inspect_feature` | L0, F2745 | " German words that aren't capitalised" |
| 13 | `inspect_feature` | L0, F4058 | "the word "die" or its derivatives in various contexts" |

**Findings:** Tracing the L4 feature for "terms related to diets and dietary health" reveals it's primarily driven by the specific input token "Die" at position 20. The circuit shows:

1. The L4 feature (13412) receives strong inputs from two L3 features (11774 and 10028)
2. Both L3 features are predominantly driven by the embedding "Die" at position 20 (weights 5.875 and 6.9375)
3. The L2 feature 7473 is also …

</details>

<details>
<summary><b>SA-2</b> — tool trace (13 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L19, F1589 | " a context of scientific, specially nutritional, studies" |
| 2 | `get_upstream_features` | L19:F1589@21, k=5 | L4:F13412 (w=10.62) +4 more |
| 3 | `inspect_feature` | L4, F13412 | " terms related to diets and dietary health" |
| 4 | `inspect_feature` | L14, F4197 | " words and phrases related to food insecurity." |
| 5 | `inspect_feature` | L6, F11327 | " words or phrases related to food or nutrition" |
| 6 | `inspect_feature` | L17, F7545 | "mentions of architecture, design, nurses and healthcare." |
| 7 | `get_upstream_features` | L4:F13412@21, k=5 | L3:F11774 (w=4.84) +4 more |
| 8 | `inspect_feature` | L3, F11774 | " what appears to be a smattering of strings related to scientific nota" |
| 9 | `inspect_feature` | L3, F10028 | "words or short phrases that include "made of/from", and words ending w" |
| 10 | `get_upstream_features` | L3:F11774@21, k=5 | Emb:" Die"@20 (w=5.88) +4 more |
| 11 | `get_upstream_features` | L14:F4197@21, k=5 | L6:F11327 (w=7.72) +4 more |
| 12 | `get_upstream_features` | L6:F11327@21, k=5 | L4:F13412 (w=5.91) +4 more |
| 13 | `inspect_feature` | L4, F9554 | " words related to food, rations and feeding" |

**Findings:** The tracing reveals that L19:F1589 (context of nutritional studies) uses genuine professional knowledge rather than spurious correlations. Key findings:

1. The feature detects scientific nutritional contexts with promoted tokens like "diet", "food", "nutrition", etc. (frac_nonzero: 0.038 - moderately specific).

2. The circuit converges from multiple nutrition/food-related features in earlier lay…

</details>

<details>
<summary><b>SA-3</b> — tool trace (3 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F14824 | "the word "has"" |
| 2 | `get_upstream_features` | L0:F14824@2, k=5 | Emb:" has"@2 (w=32.75) +4 more |
| 3 | `get_upstream_features` | L0:F14824@2, k=10 | Emb:" has"@2 (w=32.75) +9 more |

**Findings:** The L0 feature (14824) that detects the word \"has\" is primarily driven directly by the token embedding of \" has\" at the same position (weight=32.75). There are minor contributions from the start token \"<bos>\" (weight=4.03) and the pronoun \"She\" (weight=1.15). The feature has low sparsity (0.011) and interestingly suppresses \"has\"-related tokens while promoting various non-English tokens.…

</details>

### Re-dispatch (round 2): 1 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-4 | `L2:F2589@37` | ✅ reported | 2 | 10 | Trace the path from L2:2589 (fragments of names) upstream. This feature appeared… |

<details>
<summary><b>SA-4</b> — tool trace (4 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L2, F2589 | " words related to medical professionals and medical specialties" |
| 2 | `get_upstream_features` | L2:F2589@37, k=5 | Emb:"titian"@37 (w=19.12) +4 more |
| 3 | `inspect_feature` | L0, F9026 | "technical documents or data, including numbers, units, and references " |
| 4 | `get_upstream_features` | L0:F9026@37, k=5 | Emb:"titian"@37 (w=24.75) +4 more |

**Findings:** The tracing reveals that feature L2:2589 ("words related to medical professionals and medical specialties") at position 37 is primarily driven by the token "titian" at the same position with an extremely strong edge weight of 19.125. This suggests the feature is recognizing the token "titian" (likely a name fragment) in medical/professional contexts rather than relying on spurious gender patterns.…

</details>

### Re-dispatch (round 3): 1 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-5 | `L4:F9554@21` | ✅ reported | 5 | 15 | Trace L4:9554 (words related to food, rations and feeding) upstream. Identify th… |

<details>
<summary><b>SA-5</b> — tool trace (10 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F9554 | " words related to food, rations and feeding" |
| 2 | `get_upstream_features` | L4:F9554@21, k=5 | L3:F11774 (w=3.05) +4 more |
| 3 | `inspect_feature` | L3, F11774 | " what appears to be a smattering of strings related to scientific nota" |
| 4 | `inspect_feature` | L3, F10028 | "words or short phrases that include "made of/from", and words ending w" |
| 5 | `inspect_feature` | L1, F1083 | " the characters "te" within code and/or non-English words" |
| 6 | `get_upstream_features` | L3:F11774@21, k=5 | Emb:" Die"@20 (w=5.88) +4 more |
| 7 | `get_upstream_features` | L3:F10028@21, k=5 | Emb:" Die"@20 (w=6.94) +4 more |
| 8 | `get_upstream_features` | L1:F1083@21, k=5 | Emb:"te"@21 (w=22.25) +4 more |
| 9 | `inspect_feature` | L2, F7473 | " capitalized two letter prefixes or suffixes" |
| 10 | `get_upstream_features` | L2:F7473@21, k=5 | Emb:" Die"@20 (w=19.00) +4 more |

**Findings:** Tracing L4:9554 (food-related feature) upstream reveals it's primarily driven by input tokens " Die" (position 20) and "te" (position 21), not by genuine food-related content. The strongest upstream connections come from L3 features that detect character patterns (scientific notation, strings ending with specific suffixes), not food semantics. The direct embedding " Nutritional" at position 9 also…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` ×2 | L2:2589, L14:4197 |

### Build

`build_circuit` → 12 nodes, 13 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m2.7 | 28,504 | 4,275 | 53,730 | 0 | $0.0153 | — | — |
| SA-3 | deepseek/deepseek-v3.2 | 13,537 | 1,294 | 0 | 0 | $0.0040 | ✅ 1F/3E | Trace the path from L0:14824 (the word 'has') upstream. This… |
| SA-2 | deepseek/deepseek-v3.2 | 78,207 | 3,630 | 15,616 | 0 | $0.0221 | ✅ 9F/13E | Trace the path from L19:1589 (context of nutritional studies… |
| SA-1 | deepseek/deepseek-v3.2 | 76,553 | 3,811 | 15,232 | 0 | $0.0217 | ✅ 2964F/17E | Trace the path from L4:13412 (terms related to diets and die… |
| SA-4 | deepseek/deepseek-v3.2 | 18,772 | 1,824 | 128 | 0 | $0.0056 | ✅ 2F/10E | Trace the path from L2:2589 (fragments of names) upstream. T… |
| SA-5 | deepseek/deepseek-v3.2 | 62,485 | 2,987 | 0 | 0 | $0.0174 | ✅ 5F/15E | Trace L4:9554 (words related to food, rations and feeding) u… |
| **Total** | | **278,058** | **17,821** | **84,706** | **0** | **$0.0861** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 9m 1s