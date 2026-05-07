# Circuit Oracle Report
**Date:** 2026-04-06 18:14:37 UTC | **Orchestrator:** minimax/minimax-m2.7 | **Subagent:** deepseek/deepseek-v3.2

## Input

**Prompt:** "Dataset: multinli-pos_pos_9 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "('The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction.',)"

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score is driven primarily by a cascade of low-level lexical/token detection features (L0-L4) that directly recognize specific words ("recorded", "menu", "will") from the input text, rather than by semantic understanding of contradiction. The strongest positive contribution comes from L2:F8776 ("finance/property law" feature, direct_effect=0.52), which is almost entirely driven by the token " recorded" at position 2 (edge_weight=19.5), bypassing semantic processing. Most other features (L0:F2108, L1:F12253, L0:F8046, L4:F7998, L3:F3573) directly detect the tokens " menu" and " will" with edge weights of 20-36, with minimal intermediate processing.

**Confidence:** 9/10

**Reasoning:** The circuit is dominated by **spurious lexical features** as the user suspected. All 10 top features are simple word detectors with very low frac_nonzero (0.002-0.027), indicating high specificity to particular tokens rather than semantic patterns. The key evidence:

1. **Direct token-to-logit paths**: The embedding nodes " recorded" (pos 2), " menu" (pos 3), and " will" (pos 4) connect almost directly to the output via specialized detectors with weights of 19-36, bypassing semantic abstraction.

2. **Misleading feature labels**: Features like L2:F8776 ("finance/property law") and L4:F7998 ("telecommunications") have domain-specific labels but are actually driven by generic words ("recorded", "menu") rather than domain knowledge.

3. **Absence of semantic features**: No features detect semantic contradiction signals (negation, antonyms, contrast conjunctions). The word "information" (which appears twice in the input) is not detected by any top feature.

4. **Inhibition chains**: Lower-layer menu detectors (L0:F2108, L1:F12253) actually *inhibit* the higher-layer interface feature (L3:F3573, weights=-0.85), suggesting the circuit architecture doesn't build semantic abstraction.

The circuit exploits the surface form "recorded menus" as a spurious pattern—likely because such phrases appear in certain dataset contexts—rather than understanding whether the two sentences actually contradict each other. This confirms the user's concern about using lexical artifacts rather than genuine semantic analysis to predict contradiction.

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 10 features; top: L2:8776 de=0.519 |
| 3 | `inspect_feature` ×4 | L2:8776, L0:2108, L1:12253, L0:8046 |

### Dispatch: 3 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L2:F8776@2` | ✅ reported | 4 | 15 | Trace the path from L2:F8776 (finance/property law feature) - what does this fea… |
| SA-2 | `L0:F2108@3` | ✅ reported | 2 | 5 | Trace the path from L0:F2108 (word "menu" detection at pos 3) - trace upstream t… |
| SA-3 | `L0:F8046@4` | ✅ reported | 1 | 5 | Trace the path from L0:F8046 (word "will" detection at pos 4) - trace upstream t… |

<details>
<summary><b>SA-1</b> — tool trace (10 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L2, F8776 | " words related to finance and property law" |
| 2 | `get_upstream_features` | L2:F8776@2, k=3 | Emb:" recorded"@2 (w=19.50) +2 more |
| 3 | `get_upstream_features` | L2:F8776@2, k=10 | Emb:" recorded"@2 (w=19.50) +9 more |
| 4 | `inspect_feature` | L1, F3691 | " the word "recording" in scientific or experimental documentation" |
| 5 | `inspect_feature` | L0, F7443 | "the word "record" appearing in various contexts" |
| 6 | `get_upstream_features` | L1:F3691@2, k=5 | Emb:" recorded"@2 (w=24.75) +4 more |
| 7 | `inspect_feature` | L0, F7404 | " the word "faith", sometimes in association with related ideas like "l" |
| 8 | `get_upstream_features` | L0:F7404@2, k=5 | Emb:" recorded"@2 (w=14.25) +4 more |
| 9 | `get_upstream_features` | L0:F7443@2, k=5 | Emb:" recorded"@2 (w=22.62) +4 more |
| 10 | `get_top_logits` | k=5 | "" (100%) |

**Findings:** Tracing from L2:F8776 (finance/property law feature) at position 2 reveals:

1. The feature is strongly triggered by the token " recorded" at position 2 (edge_weight: 19.5) - this is the primary input.

2. The feature receives weak negative input from L1:F3691 (-0.6953), which detects "recording" in scientific contexts and suppresses "recorded" tokens.

3. The feature receives weak positive input …

</details>

<details>
<summary><b>SA-2</b> — tool trace (3 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F2108 | "the word "menu"" |
| 2 | `get_upstream_features` | L0:F2108@3, k=5 | Emb:" menu"@3 (w=25.75) +4 more |
| 3 | `inspect_feature` | L0, F478 | "various kinds of brackets and parentheses followed by a period" |

**Findings:** The tracing reveals that L0:F2108 (detecting the word "menu" at position 3) is primarily driven by the token " menu" at position 3 itself, with a very strong edge weight of 25.75. This indicates the feature directly detects the presence of the token "menu" at that position. There are minor influences from other tokens: negative influence from " recorded" at position 2 (-0.4766), and small positive…

</details>

<details>
<summary><b>SA-3</b> — tool trace (4 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F8046 | " the word "will."" |
| 2 | `get_upstream_features` | L0:F8046@4, k=5 | Emb:" will"@4 (w=36.00) +4 more |
| 3 | `get_upstream_features` | L0:F8046@4, k=10 | Emb:" will"@4 (w=36.00) +9 more |
| 4 | `inspect_feature` | L0, F8046 | " the word "will."" |

**Findings:** The feature L0:F8046 at position 4 is a lexical feature that directly detects the word "will". The tracing shows it is overwhelmingly driven by the input token " will" at position 4 itself (edge weight 36.0), with much weaker connections from other nearby tokens. This confirms it is a spurious/lexical feature - it simply recognizes the token "will" in the input. The feature has low frac_nonzero (0…

</details>

### Re-dispatch (round 2): 2 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-4 | `L3:F3573@3` | ✅ reported | 6 | 9 | Trace the path from L3:F3573 (word "menu" in interface context) - trace upstream… |
| SA-5 | `L4:F7998@3` | ✅ reported | 4 | 19 | Trace the path from L4:F7998 (telecommunications feature) - trace upstream to fi… |

<details>
<summary><b>SA-4</b> — tool trace (9 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L3, F3573 | "the word "menu" often in conjunction with interface elements" |
| 2 | `get_upstream_features` | L3:F3573@3, k=5 | Emb:" menu"@3 (w=21.38) +4 more |
| 3 | `inspect_feature` | L1, F12253 | " the word 'menu'" |
| 4 | `inspect_feature` | L2, F9012 | " instances where something was not successful" |
| 5 | `get_upstream_features` | L1:F12253@3, k=5 | Emb:" menu"@3 (w=20.62) +4 more |
| 6 | `inspect_feature` | L0, F2108 | "the word "menu"" |
| 7 | `inspect_feature` | L0, F2115 | " data reported as a percentage inside brackets, especially in a labora" |
| 8 | `get_upstream_features` | L2:F9012@3, k=5 | Emb:" menu"@3 (w=12.31) +4 more |
| 9 | `inspect_feature` | L1, F14120 | "restaurant menus" |

**Findings:** Traced the circuit from L3:F3573 (detects "menu" in interface context, suppresses menu tokens). The strongest driver is the input token " menu" at position 3 (edge_weight 21.375). Interestingly, lower-layer features that detect "menu" (L1:F12253 and L2:F9012) have NEGATIVE edge_weights to the L3 feature, meaning they inhibit it. L2:F9012 detects "not successful" contexts and is also driven by " me…

</details>

<details>
<summary><b>SA-5</b> — tool trace (8 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F7998 | " words related to telecommunications and telephones" |
| 2 | `get_upstream_features` | L4:F7998@3, k=5 | Emb:" menu"@3 (w=13.56) +4 more |
| 3 | `inspect_feature` | L1, F11170 | "words related to telephones and connecting/disconnecting calls" |
| 4 | `get_upstream_features` | L1:F11170@3, k=5 | Emb:" menu"@3 (w=8.06) +4 more |
| 5 | `inspect_feature` | L0, F2108 | "the word "menu"" |
| 6 | `inspect_feature` | L0, F6649 | " the word "Title"" |
| 7 | `get_upstream_features` | L0:F2108@3, k=5 | Emb:" menu"@3 (w=25.75) +4 more |
| 8 | `get_upstream_features` | L0:F6649@3, k=5 | Emb:" menu"@3 (w=14.38) +4 more |

**Findings:** Tracing from L4:F7998 (telecommunications feature) at position 3 reveals a direct connection to specific input tokens. The primary drivers are the token " menu" at position 3 (edge_weight: 13.56) and " recorded" at position 2 (edge_weight: 10.94), both strongly positive. There's also a weaker positive connection from L1:F11170 (telephone-related feature) with weight 2.36. The L1 feature itself is …

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` ×5 | L1:3691, L0:7443, L3:3573, L4:7998, L0:6649 |
| 2 | `get_upstream_features` | L0:F7404@2, k=5 → Emb:" recorded"@2 (w=14.25) +4 more |

### Build

`build_circuit` → 14 nodes, 20 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m2.7 | 23,484 | 4,425 | 74,328 | 0 | $0.0146 | — | — |
| SA-2 | deepseek/deepseek-v3.2 | 8,071 | 1,362 | 5,568 | 0 | $0.0028 | ✅ 2F/5E | Trace the path from L0:F2108 (word "menu" detection at pos 3… |
| SA-3 | deepseek/deepseek-v3.2 | 18,224 | 1,505 | 0 | 0 | $0.0053 | ✅ 1F/5E | Trace the path from L0:F8046 (word "will" detection at pos 4… |
| SA-1 | deepseek/deepseek-v3.2 | 55,369 | 3,058 | 3,200 | 0 | $0.0156 | ✅ 4F/15E | Trace the path from L2:F8776 (finance/property law feature) … |
| SA-5 | deepseek/deepseek-v3.2 | 43,611 | 2,739 | 0 | 0 | $0.0124 | ✅ 4F/19E | Trace the path from L4:F7998 (telecommunications feature) - … |
| SA-4 | deepseek/deepseek-v3.2 | 48,820 | 2,925 | 5,440 | 0 | $0.0139 | ✅ 6F/9E | Trace the path from L3:F3573 (word "menu" in interface conte… |
| **Total** | | **197,579** | **16,014** | **88,536** | **0** | **$0.0646** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 5m 18s