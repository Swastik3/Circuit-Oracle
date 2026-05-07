# Circuit Oracle Report
**Date:** 2026-04-06 18:20:20 UTC | **Orchestrator:** minimax/minimax-m2.7 | **Subagent:** deepseek/deepseek-v3.2

## Input

**Prompt:** "Dataset: multinli-pos_pos_10 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "('The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction.',)"

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The contradiction detection probe relies almost entirely on spurious negation word features rather than semantic content. The circuit traces exclusively from the literal token "not" (position 17 in "There is **not** role reversal going on...") through multiple negation-specific features (multilingual negations, negative sentiment markers, error/absence detection, "NO"-like patterns) to the probe output. The input's actual semantic content about "democracy" and "role reversal" is never consulted.

**Confidence:** 9/10

**Reasoning:** The circuit is definitively spurious pattern-matching rather than semantic understanding:

1. **No semantic features discovered**: Despite tracing through 4-5 hops and 15+ features across layers 0-16, not a single feature encodes "democracy," "role reversal," "contradiction," "negation of meaning," or any semantically relevant concept. All features are negation-specific detectors.

2. **Literal token "not" is the sole driver**: The strongest edges all terminate on or originate from the token "not" at position 17:
   - Direct token→L4:F4492 edge: weight 18.0
   - Direct token→L3:F8011 edge: weight 20.88
   - Direct token→L3:F1101 edge: weight 13.19
   - Emb:L0:F4958 (not detector): 32.75 from token

3. **Multilingual negation features dominate**: L4:F2422 ("negations in French, Malay, Croatian") and L4:F4492 ("negations in various languages") are the strongest late-layer drivers with frac_nonzero=0.016 and 0.038 respectively. These features promote tokens like "<bos>", Arabic words, and code-related terms—not content about democracy.

4. **Competing suppression signals**: L3:F1101 (error/negation in software contexts) has direct_effect=-1.21, meaning it actively inhibits the probe when it detects "non existing" type patterns. The probe's positive signal comes from features promoting negation words themselves, not from detecting actual semantic contradiction.

5. **No pathway to semantic content**: The only input tokens driving the circuit are "not" (pos 17), "is" (pos 16), and "There" (pos 15). The tokens "democracy" (pos 12) and "role reversal" (pos 4-6) have negligible edge weights (<0.23) and do not meaningfully contribute to the circuit.

This confirms the user's concern: the probe has learned to shortcut contradiction detection to "does the text contain negation words?" rather than genuinely understanding whether sentences contradict each other semantically.

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L4:2422 de=-1.273 |
| 3 | `inspect_feature` ×4 | L4:2422, L4:4492, L3:1101, L3:12079 |

### Dispatch: 6 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L4:F2422@17` | ✅ reported | 9 | 12 | Trace this negation feature upstream. What early-layer features or input tokens … |
| SA-2 | `L4:F4492@17` | ✅ reported | 8 | 25 | Trace this negation feature upstream. What early-layer features or input tokens … |
| SA-3 | `L3:F1101@17` | ✅ reported | 6 | 20 | Trace this negation/error feature upstream. What input tokens or early features … |
| SA-4 | `L16:F12358@17` | ✅ reported | 7 | 6 | Trace this layer 16 feature upstream. What does it encode and where does it come… |
| SA-5 | `L3:F8011@17` | ✅ reported | 6 | 6 | Trace this negation feature upstream. What input tokens drive it? |
| SA-6 | `L3:F2232@17` | ✅ reported | 2 | 10 | Trace this feature and understand what it encodes. |

<details>
<summary><b>SA-1</b> — tool trace (15 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F2422 | "negations in other languages like French, Malay, and Croatian" |
| 2 | `get_upstream_features` | L4:F2422@17, k=5 | Emb:" not"@17 (w=16.50) +4 more |
| 3 | `inspect_feature` | L3, F1101 | " error messages and terms indicating absence or negation in software c" |
| 4 | `inspect_feature` | L3, F8011 | " a mix of words and code fragments from different languages" |
| 5 | `inspect_feature` | L3, F9803 | "sentences describing scientific studies or experiments, particularly w" |
| 6 | `get_upstream_features` | L3:F1101@17, k=5 | Emb:" not"@17 (w=13.19) +4 more |
| 7 | `inspect_feature` | L0, F4958 | " the word "not"" |
| 8 | `inspect_feature` | L1, F14233 | " negative sentiment markers such as "not," "no," "never," and their eq" |
| 9 | `get_upstream_features` | L3:F8011@17, k=5 | Emb:" not"@17 (w=20.88) +4 more |
| 10 | `get_upstream_features` | L0:F4958@17, k=5 | Emb:" not"@17 (w=32.75) +4 more |
| 11 | `get_upstream_features` | L1:F14233@17, k=5 | Emb:" not"@17 (w=6.72) +4 more |
| 12 | `inspect_feature` | L0, F9646 | " words that indicate the degree, scale, or validity of something" |
| 13 | `get_upstream_features` | L3:F9803@17, k=5 | Emb:" not"@17 (w=13.56) +4 more |
| 14 | `inspect_feature` | L2, F6993 | "phrases describing uncertainty or difficulty" |
| 15 | `inspect_feature` | L2, F12021 | ""not" or negative terms, with some bonus for sports-related terms and " |

**Findings:** The negation feature (L4:F2422) detecting negations in other languages traces back strongly to the input token " not" at position 17. The circuit shows:

1. DIRECT INPUT TOKEN: The strongest connection is directly from the embedding of " not" at position 17 to the L4 negation feature (edge_weight 16.5), showing this is primarily driven by the literal token "not".

2. EARLY LAYER FEATURES: Layer 0 …

</details>

<details>
<summary><b>SA-2</b> — tool trace (13 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F4492 | "negations in various languages" |
| 2 | `get_upstream_features` | L4:F4492@17, k=5 | Emb:" not"@17 (w=18.00) +4 more |
| 3 | `inspect_feature` | L3, F1101 | " error messages and terms indicating absence or negation in software c" |
| 4 | `inspect_feature` | L3, F8011 | " a mix of words and code fragments from different languages" |
| 5 | `inspect_feature` | L3, F12079 | "negations and Chinese names" |
| 6 | `get_upstream_features` | L3:F8011@17, k=5 | Emb:" not"@17 (w=20.88) +4 more |
| 7 | `get_upstream_features` | L3:F1101@17, k=5 | Emb:" not"@17 (w=13.19) +4 more |
| 8 | `inspect_feature` | L0, F4958 | " the word "not"" |
| 9 | `inspect_feature` | L2, F6993 | "phrases describing uncertainty or difficulty" |
| 10 | `inspect_feature` | L1, F14233 | " negative sentiment markers such as "not," "no," "never," and their eq" |
| 11 | `get_upstream_features` | L1:F14233@17, k=5 | Emb:" not"@17 (w=6.72) +4 more |
| 12 | `inspect_feature` | L0, F9646 | " words that indicate the degree, scale, or validity of something" |
| 13 | `get_upstream_features` | L3:F12079@17, k=5 | Emb:" There"@15 (w=15.06) +4 more |

**Findings:** Tracing L4:F4492 (negations in various languages) reveals a complex circuit where negation processing involves both promotion and suppression mechanisms. The strongest driver is the direct token embedding for "not" at position 17 (weight 18.0). Interestingly, layer 3 contains competing features: L3:F8011 promotes negation words while L3:F1101 suppresses them, creating a balanced representation. Th…

</details>

<details>
<summary><b>SA-3</b> — tool trace (10 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L3, F1101 | " error messages and terms indicating absence or negation in software c" |
| 2 | `get_upstream_features` | L3:F1101@17, k=5 | Emb:" not"@17 (w=13.19) +4 more |
| 3 | `inspect_feature` | L0, F4958 | " the word "not"" |
| 4 | `inspect_feature` | L2, F6993 | "phrases describing uncertainty or difficulty" |
| 5 | `inspect_feature` | L1, F14233 | " negative sentiment markers such as "not," "no," "never," and their eq" |
| 6 | `get_upstream_features` | L1:F14233@17, k=5 | Emb:" not"@17 (w=6.72) +4 more |
| 7 | `get_upstream_features` | L0:F4958@17, k=5 | Emb:" not"@17 (w=32.75) +4 more |
| 8 | `inspect_feature` | L0, F9646 | " words that indicate the degree, scale, or validity of something" |
| 9 | `get_upstream_features` | L2:F6993@17, k=5 | Emb:" not"@17 (w=6.38) +4 more |
| 10 | `inspect_feature` | L1, F14680 | "the word "not"" |

**Findings:** The negation/error feature L3:F1101 is primarily driven by the input token " not" at position 17 (strongest connection: weight 13.1875). This token directly feeds into multiple features: L0:F4958 (detects "not"), L1:F14233 (negative sentiment markers), and L2:F6993 (uncertainty/difficulty phrases). All these features then converge on the target L3 error/negation feature.

Key circuit: " not" token…

</details>

<details>
<summary><b>SA-4</b> — tool trace (11 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L16, F12358 | " the word "not" followed within a few tokens by a form of the verb "to" |
| 2 | `get_upstream_features` | L16:F12358@17, k=5 | Emb:" not"@17 (w=23.12) +4 more |
| 3 | `inspect_feature` | L0, F4958 | " the word "not"" |
| 4 | `inspect_feature` | L15, F6160 | " occurrences of "is there"" |
| 5 | `inspect_feature` | L4, F2422 | "negations in other languages like French, Malay, and Croatian" |
| 6 | `get_upstream_features` | L0:F4958@17, k=5 | Emb:" not"@17 (w=32.75) +4 more |
| 7 | `get_upstream_features` | L15:F6160@17, k=5 | Emb:" There"@15 (w=21.62) +4 more |
| 8 | `inspect_feature` | L3, F10742 | " fragments of French sentences, particularly those containing the verb" |
| 9 | `inspect_feature` | L8, F9880 | " phrases expressing doubt, negation, or uncertainty" |
| 10 | `get_upstream_features` | L4:F2422@17, k=5 | Emb:" not"@17 (w=16.50) +4 more |
| 11 | `inspect_feature` | L3, F1101 | " error messages and terms indicating absence or negation in software c" |

**Findings:** Layer 16 feature 12358 encodes a pattern detection for "the word 'not' followed within a few tokens by a form of the verb 'to be'". The circuit analysis reveals this feature combines information from:

1. Direct token embeddings: " not" at position 17 (strongest connection, weight 23.125) and " is" at position 16 (weight 4.375)
2. Layer 0 feature 4958 that directly detects "the word 'not'" (weight…

</details>

<details>
<summary><b>SA-5</b> — tool trace (11 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L3, F8011 | " a mix of words and code fragments from different languages" |
| 2 | `get_upstream_features` | L3:F8011@17, k=5 | Emb:" not"@17 (w=20.88) +4 more |
| 3 | `inspect_feature` | L0, F4958 | " the word "not"" |
| 4 | `get_upstream_features` | L0:F4958@17, k=5 | Emb:" not"@17 (w=32.75) +4 more |
| 5 | `get_upstream_features` | L3:F8011@17, k=10 | Emb:" not"@17 (w=20.88) +9 more |
| 6 | `inspect_feature` | L2, F6993 | "phrases describing uncertainty or difficulty" |
| 7 | `inspect_feature` | L0, F15454 | " the word "not"" |
| 8 | `get_upstream_features` | L2:F6993@17, k=5 | Emb:" not"@17 (w=6.38) +4 more |
| 9 | `get_upstream_features` | L0:F15454@17, k=5 | Emb:" not"@17 (w=7.50) +4 more |
| 10 | `inspect_feature` | L0, F11375 | " the word "is"" |
| 11 | `inspect_feature` | L2, F11420 | " words related to lawsuits and legal issues" |

**Findings:** The negation feature at L3:8011 is primarily driven by the input token " not" at position 17, which has an extremely strong direct connection (weight: 20.875). This is the main driver of the negation feature. The feature also receives positive contributions from early-layer features that detect "not" (L0:4958 and L0:15454) and from L2:6993 (uncertainty/difficulty phrases). There are negative conne…

</details>

<details>
<summary><b>SA-6</b> — tool trace (4 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L3, F2232 | " character sequences like "NOC", "NO", "ORES", "NOS", "OF", "UNCH", an" |
| 2 | `get_upstream_features` | L3:F2232@17, k=5 | Emb:" There"@15 (w=8.62) +4 more |
| 3 | `inspect_feature` | L0, F4958 | " the word "not"" |
| 4 | `get_upstream_features` | L0:F4958@17, k=5 | Emb:" not"@17 (w=32.75) +4 more |

**Findings:** I traced L3:F2232 at position 17, which detects character sequences like "NOC", "NO", "ORES" in hexadecimal code contexts and related words like "dangerously", "Bantus", "slave", "plantation". The feature promotes "no"-related tokens and has low frac_nonzero (0.0065), indicating specificity.

The circuit shows strong direct connections from token embeddings: " There" at position 15 (weight 8.625) …

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` ×2 | L3:2232, L0:4958 |

### Build

`build_circuit` → 13 nodes, 23 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m2.7 | 32,765 | 3,974 | 45,223 | 0 | $0.0160 | — | — |
| SA-4 | deepseek/deepseek-v3.2 | 69,314 | 3,038 | 5,312 | 0 | $0.0193 | ✅ 7F/6E | Trace this layer 16 feature upstream. What does it encode an… |
| SA-3 | deepseek/deepseek-v3.2 | 55,133 | 3,430 | 6,336 | 0 | $0.0158 | ✅ 6F/20E | Trace this negation/error feature upstream. What input token… |
| SA-1 | deepseek/deepseek-v3.2 | 89,715 | 3,814 | 24,128 | 0 | $0.0254 | ✅ 9F/12E | Trace this negation feature upstream. What early-layer featu… |
| SA-2 | deepseek/deepseek-v3.2 | 85,360 | 4,495 | 9,344 | 0 | $0.0241 | ✅ 8F/25E | Trace this negation feature upstream. What early-layer featu… |
| SA-6 | deepseek/deepseek-v3.2 | 21,161 | 2,379 | 0 | 0 | $0.0064 | ✅ 2F/10E | Trace this feature and understand what it encodes. |
| SA-5 | deepseek/deepseek-v3.2 | 68,173 | 2,535 | 0 | 0 | $0.0187 | ✅ 6F/6E | Trace this negation feature upstream. What input tokens driv… |
| **Total** | | **421,621** | **23,665** | **90,343** | **0** | **$0.1257** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 5m 42s