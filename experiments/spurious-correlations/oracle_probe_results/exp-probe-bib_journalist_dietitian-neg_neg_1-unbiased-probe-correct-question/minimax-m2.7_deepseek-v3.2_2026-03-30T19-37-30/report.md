# Circuit Oracle Report
**Date:** 2026-03-30 19:37:30 UTC | **Orchestrator:** minimax/minimax-m2.7 | **Subagent:** deepseek/deepseek-v3.2

## Input
**Prompt:** "Dataset: bib_journalist_dietitian-neg_neg_1 | Probe: unbiased | Method: correct"
**System prompt:** ""
**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."
**Top predictions:**  (100.0%)

## Oracle Analysis
**Analysis:** The probe's classification is driven primarily by the **"His" pronoun (L0:F8964)**, a gender marker with the strongest positive direct effect (0.0874), while all genuine journalism/reporting features have negative effects (L14:F4420 = -0.1475, L19:F2486 = -0.0972, L20:F8433 = -0.0513), confirming the user's concern that the probe uses spurious gender markers rather than authentic profession indicators.

**Confidence:** 9/10

**Reasoning:** The circuit clearly demonstrates that:

1. **Gender Marker Dominates:** L0:F8964 ("His" - the possessive masculine pronoun) is the single strongest positive contributor to the probe's output, with direct_effect = 0.0874. This is a spurious feature that correlates with the target only because of gender biases in training data, not genuine profession knowledge.

2. **Genuine Profession Features Anti-Correlate:** All actual journalism features have NEGATIVE effects on the probe:
   - L14:F4420 "journalism and newspapers" (direct_effect = -0.1475, largest negative)
   - L19:F2486 "journalistic sources and news outlets" (direct_effect = -0.0972, appears at 7 positions)
   - L20:F8433 "news broadcasting" (direct_effect = -0.0513)
   - L8:F8855 "news reporters/reporting" (direct_effect = -0.0513)

3. **Signal Flow:** The "report" token at position 21 feeds into journalism detection features through layers 1→4→7→8→14→19, progressively building abstract journalism concepts. However, this legitimate signal actually PUSHES the probe DOWN, not up.

4. **Conflicting Signals:** The circuit shows an anomaly where literal "report" detection (L1:F14511, positive 0.0518) has a positive effect, but abstract journalism concepts (L14+, negative) have negative effects. This suggests the probe learned to latch onto surface tokens and gender markers rather than abstract professional identity.

5. **Feature Specificity:** All journalism features have low frac_nonzero (0.008-0.035), confirming they encode specific profession knowledge. The "His" feature also has low frac_nonzero (0.01755), confirming it specifically detects masculine pronouns.

The probe's reliance on "His" as its strongest positive signal while all genuine profession indicators are negative is a clear case of spurious feature usage, where the model exploited gender-pronoun correlations in the training data rather than learning authentic profession classification.

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L14:4420 de=-0.147 |

### Dispatch: 3 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L19:F2486@21` | ✅ reported | 15 | 30 | Trace L19:F2486 upstream to understand what this feature encodes and what signal… |
| SA-2 | `L14:F4420@21` | ✅ reported | 11 | 11 | Trace L14:F4420 upstream - this has the largest negative direct effect. Understa… |
| SA-3 | `L0:F8444@3` | ✅ reported | 1 | 6 | Trace L0:F8444 (positive effect at pos 3 and 20) upstream to understand what tok… |

<details>
<summary><b>SA-1</b> — tool trace (18 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L19, F2486 | " journalistic sources and news outlets." |
| 2 | `get_upstream_features` | L19:F2486@21, k=5 | L14:F4420 (w=14.31) +4 more |
| 3 | `inspect_feature` | L14, F4420 | "words and phrases related to journalism and newspapers" |
| 4 | `inspect_feature` | L16, F8642 | " text related to official reporting and legal issues." |
| 5 | `inspect_feature` | L8, F8855 | " mentions of news reporters and news reporting" |
| 6 | `get_upstream_features` | L14:F4420@21, k=5 | Emb:" report"@21 (w=5.19) +4 more |
| 7 | `inspect_feature` | L8, F8437 | "content related to film festivals and production, particularly documen" |
| 8 | `inspect_feature` | L7, F13646 | " news reporting and journalism." |
| 9 | `get_upstream_features` | L7:F13646@21, k=5 | Emb:" report"@21 (w=7.22) +4 more |
| 10 | `inspect_feature` | L4, F661 | " words and phrases used when referring to reports, documentaries, and " |
| 11 | `get_upstream_features` | L4:F661@21, k=5 | Emb:" report"@21 (w=14.38) +4 more |
| 12 | `inspect_feature` | L1, F14511 | " the word "report"" |
| 13 | `inspect_feature` | L2, F11175 | "the verb "report" and its variations" |
| 14 | `get_upstream_features` | L16:F8642@21, k=5 | L14:F4420 (w=10.50) +4 more |
| 15 | `get_upstream_features` | L8:F8855@21, k=5 | Emb:" report"@21 (w=12.06) +4 more |
| 16 | `inspect_feature` | L7, F13896 | " words or phrases related to reports, people's names, and versions" |
| 17 | `inspect_feature` | L3, F10846 | "the word "report"" |
| 18 | `inspect_feature` | L6, F12712 | " titles of editors and publishers in scientific publications" |

**Findings:** Tracing L19:F2486 reveals a circuit for detecting journalistic/reporting concepts. The feature encodes "journalistic sources and news outlets" and promotes tokens like "reporting", "reporter", "coverage". 

Key findings:
1. The strongest upstream connection is from L14:F4420 (journalism-related words) with weight 14.3125.
2. The input token " report" at position 21 is the fundamental source, feedi…

</details>

<details>
<summary><b>SA-2</b> — tool trace (16 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L14, F4420 | "words and phrases related to journalism and newspapers" |
| 2 | `get_upstream_features` | L14:F4420@21, k=5 | Emb:" report"@21 (w=5.19) +4 more |
| 3 | `inspect_feature` | L8, F8855 | " mentions of news reporters and news reporting" |
| 4 | `inspect_feature` | L7, F13646 | " news reporting and journalism." |
| 5 | `get_upstream_features` | L8:F8855@21, k=5 | Emb:" report"@21 (w=12.06) +4 more |
| 6 | `get_upstream_features` | L7:F13646@21, k=5 | Emb:" report"@21 (w=7.22) +4 more |
| 7 | `inspect_feature` | L8, F8437 | "content related to film festivals and production, particularly documen" |
| 8 | `inspect_feature` | L9, F7435 | " words and phrases related to news production and media" |
| 9 | `inspect_feature` | L4, F661 | " words and phrases used when referring to reports, documentaries, and " |
| 10 | `get_upstream_features` | L4:F661@21, k=5 | Emb:" report"@21 (w=14.38) +4 more |
| 11 | `inspect_feature` | L1, F14511 | " the word "report"" |
| 12 | `inspect_feature` | L2, F11175 | "the verb "report" and its variations" |
| 13 | `inspect_feature` | L3, F10846 | "the word "report"" |
| 14 | `get_upstream_features` | L1:F14511@21, k=5 | Emb:" report"@21 (w=20.62) +4 more |
| 15 | `inspect_feature` | L0, F1014 | " instances of measurement, experimentation, and quantification" |
| 16 | `inspect_feature` | L0, F12801 | " verbs related to communication, help, enabling, and allowing" |

**Findings:** Tracing L14:F4420 (journalism/newspapers feature with largest negative direct effect) revealed a circuit that processes the word "report" into journalism-related concepts. The feature at L14:F4420 encodes words related to journalism and newspapers.

Key findings:
1. The signal originates primarily from the embedding token " report" at position 21, which feeds strongly into multiple early layer fea…

</details>

<details>
<summary><b>SA-3</b> — tool trace (4 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F8444 | "the word "to"" |
| 2 | `get_upstream_features` | L0:F8444@3, k=5 | Emb:" to"@3 (w=39.50) +4 more |
| 3 | `get_upstream_features` | L0:F8444@20, k=5 | Emb:" to"@20 (w=42.25) +4 more |
| 4 | `get_top_logits` | k=5 | "" (100%) |

**Findings:** Traced L0:F8444 (detects the word \"to\") upstream from positions 3 and 20. The feature is primarily driven by the raw embedding of \" to\" tokens at the exact positions where it activates (pos 3 with weight 39.5, pos 20 with weight 42.25). This represents a very direct circuit where token embeddings directly activate a feature that detects that same token. The feature has low sparsity (frac_nonze…

</details>

### Re-dispatch (round 2): 3 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-4 | `L0:F8964@1` | ✅ reported | 2 | 2 | Trace L0:F8964 at position 1 (positive effect, activation 10.6875) - this is the… |
| SA-5 | `L0:F2011@2` | ✅ reported | 3 | 2 | Trace L0:F2011 at position 2 (positive effect) - this is "desire" token. Underst… |
| SA-6 | `L0:F14287@4` | ✅ reported | 1 | 5 | Trace L0:F14287 at position 4 (positive effect) - understand what this feature e… |

<details>
<summary><b>SA-4</b> — tool trace (5 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F8964 | " the possessive pronoun "His"" |
| 2 | `get_upstream_features` | L0:F8964@1, k=5 | Emb:"His"@1 (w=13.69) +4 more |
| 3 | `inspect_feature` | L0, F253 | "the contraction "ve" and also finds other words like "scale", "screen"" |
| 4 | `get_top_logits` | k=10 | "" (100%) |
| 5 | `get_upstream_features` | L0:F8964@1, k=10 | Emb:"His"@1 (w=13.69) +9 more |

**Findings:** Tracing from L0:F8964 at position 1 (the "His" token) reveals it is a simple feature that detects the literal possessive pronoun "His". The circuit shows strong direct connection from the "His" token embedding (weight: 13.6875) and a weaker connection from the beginning-of-sequence token. All other layer 0 features have 0 edge weight, indicating they don't contribute. This feature has low sparsity…

</details>

<details>
<summary><b>SA-5</b> — tool trace (6 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F2011 | " the word "dream"" |
| 2 | `get_upstream_features` | L0:F2011@2, k=5 | Emb:" desire"@2 (w=12.94) +4 more |
| 3 | `inspect_feature` | L0, F253 | "the contraction "ve" and also finds other words like "scale", "screen"" |
| 4 | `inspect_feature` | L0, F310 | " the pronouns "she", "her", and "he" and sometimes the word "therefore" |
| 5 | `get_top_features` | token="desire", k=10 | ❌ Token 'desire' not found in top logits. Available: [''] |
| 6 | `get_top_logits` | k=10 | "" (100%) |

**Findings:** Tracing from L0:F2011 at position 2 reveals that this feature detects 'the word \"dream\"'. The main upstream connection is directly from the 'desire' token embedding at position 2 with strong edge weight (12.9375), not from other L0 features (which have 0 edge weight). This suggests semantic association: when the model processes the token 'desire', it activates a feature that detects 'dream', ind…

</details>

<details>
<summary><b>SA-6</b> — tool trace (3 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F14287 | "the word "see"" |
| 2 | `get_upstream_features` | L0:F14287@4, k=5 | Emb:" see"@4 (w=25.12) +4 more |
| 3 | `get_upstream_features` | L0:F14287@4, k=10 | Emb:" see"@4 (w=25.12) +9 more |

**Findings:** Tracing L0:F14287 at position 4 (positive effect). This feature detects the word \"see\" with high specificity (frac_nonzero = 0.00373). It is primarily fed directly by the embedding of \"see\" at the same position (edge_weight = 25.125), with secondary input from \"to\" at position 3 (edge_weight = 4.625). There are weak inhibitory connections from \"His\" at position 1 and bos> at position 0. Th…

</details>

### Re-dispatch (round 3): 1 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-7 | `L0:F2203@6` | ✅ reported | 1 | 1 | Trace L0:F2203 at position 6 (negative direct effect -0.0542) to understand what… |

<details>
<summary><b>SA-7</b> — tool trace (3 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F2203 | " instances of the words "world" or "game" (possibly "problem") or expr" |
| 2 | `get_upstream_features` | L0:F2203@6, k=5 | Emb:" world"@6 (w=18.25) +4 more |
| 3 | `get_upstream_features` | L0:F2203@6, k=10 | Emb:" world"@6 (w=18.25) +9 more |

**Findings:** L0:F2203 is a simple token detector for the word \"world\" that fires strongly when it sees the token \"world\" in the input. It has a negative direct effect (-0.0542) and suppresses the word \"world\" in output (as seen in its suppressed_tokens list where \"world\" is top suppressed). The feature receives direct input from the \"world\" token embedding with a very strong weight of 18.25, making i…

</details>

### Re-dispatch (round 4): 1 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-8 | `L1:F14511@21` | ✅ reported | 6 | 11 | Trace L1:F14511 "report" which has a POSITIVE direct effect - understand why ear… |

<details>
<summary><b>SA-8</b> — tool trace (11 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L1, F14511 | " the word "report"" |
| 2 | `get_upstream_features` | L1:F14511@21, k=5 | Emb:" report"@21 (w=20.62) +4 more |
| 3 | `inspect_feature` | L0, F1014 | " instances of measurement, experimentation, and quantification" |
| 4 | `inspect_feature` | L0, F12801 | " verbs related to communication, help, enabling, and allowing" |
| 5 | `get_upstream_features` | L0:F1014@21, k=5 | Emb:" report"@21 (w=7.25) +4 more |
| 6 | `get_upstream_features` | L0:F12801@21, k=5 | Emb:" to"@20 (w=6.94) +4 more |
| 7 | `get_upstream_features` | L1:F14511@21, k=10 | Emb:" report"@21 (w=20.62) +9 more |
| 8 | `inspect_feature` | L0, F1981 | " words that indicate intention and reporting" |
| 9 | `inspect_feature` | L0, F10741 | " words related to someone dealing with a difficult situation, or reque" |
| 10 | `inspect_feature` | L0, F14474 | " mentions of "signing" and "studying"." |
| 11 | `get_upstream_features` | L0:F1981@21, k=5 | Emb:" to"@20 (w=6.62) +4 more |

**Findings:** I traced L1:F14511 "the word 'report'" feature at position 21. The circuit shows:

1. **Direct token influence**: The strongest connection is directly from the embedding of " report" at position 21 (weight 20.625) - this feature literally detects the token.

2. **Layer 0 semantic features feeding into it**: Multiple layer 0 features with different semantic interpretations of "report" feed into L1 …

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` ×6 | L19:2486, L14:4420, L0:8964, L0:2011, L0:14287, L0:310 |
| 2 | `get_top_features` | token="", k=30 → 30 features; top: L14:4420 de=-0.147 |
| 3 | `inspect_feature` ×4 | L0:13948, L1:14511, L20:8433, L0:15693 |

### Build

`build_circuit` → 11 nodes, 13 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m2.7 | 32,543 | 6,083 | 133,480 | 0 | — | — | — |
| SA-3 | deepseek/deepseek-v3.2 | 17,199 | 1,609 | 0 | 0 | — | ✅ 1F/6E | Trace L0:F8444 (positive effect at pos 3 and 20) upstream to… |
| SA-2 | deepseek/deepseek-v3.2 | 121,498 | 4,160 | 6,592 | 0 | — | ✅ 11F/11E | Trace L14:F4420 upstream - this has the largest negative dir… |
| SA-1 | deepseek/deepseek-v3.2 | 149,940 | 5,812 | 9,152 | 0 | — | ✅ 15F/30E | Trace L19:F2486 upstream to understand what this feature enc… |
| SA-6 | deepseek/deepseek-v3.2 | 13,558 | 1,417 | 0 | 0 | — | ✅ 1F/5E | Trace L0:F14287 at position 4 (positive effect) - understand… |
| SA-5 | deepseek/deepseek-v3.2 | 30,101 | 1,715 | 0 | 0 | — | ✅ 3F/2E | Trace L0:F2011 at position 2 (positive effect) - this is "de… |
| SA-4 | deepseek/deepseek-v3.2 | 23,181 | 1,627 | 0 | 0 | — | ✅ 2F/2E | Trace L0:F8964 at position 1 (positive effect, activation 10… |
| SA-7 | deepseek/deepseek-v3.2 | 13,198 | 1,477 | 0 | 0 | — | ✅ 1F/1E | Trace L0:F2203 at position 6 (negative direct effect -0.0542… |
| SA-8 | deepseek/deepseek-v3.2 | 67,608 | 2,914 | 0 | 0 | — | ✅ 6F/11E | Trace L1:F14511 "report" which has a POSITIVE direct effect … |
| **Total** | | **468,826** | **26,814** | **149,224** | **0** | **—** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 9m 52s