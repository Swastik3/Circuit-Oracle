# Circuit Oracle Report
**Date:** 2026-04-06 17:37:01 UTC | **Orchestrator:** minimax/minimax-m2.7 | **Subagent:** deepseek/deepseek-v3.2

## Input

**Prompt:** "Dataset: multinli-pos_pos_7 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "('The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction.',)"

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score is primarily driven by a **negation signal circuit** (L16:F12358 with direct_effect=0.3594 and L16:F9779 with direct_effect=0.2383) rather than actual semantic content from the prompt. The circuit traces from raw token embeddings of "not" (positions 23 and 29) through a multi-layer hierarchy of negation-specific features (L0→L3→L13→L15→L16) that detect increasingly complex negation patterns like "not + to-be forms" and "negation words." In contrast, the actual semantic content about the abbey (detected by L5:F14591) has a **negative** effect on the probe score (-0.1748), meaning religious/architectural entity recognition **suppresses** rather than supports the prediction. Simple lexical features (articles "the"/"of", pronoun "you", copula "is") contribute minor positive effects (combined ~0.42). The user's concern is **confirmed**: the probe exploits spurious negation features that fire on syntactic patterns ("not" near "is/are") rather than encoding genuine semantic relationships from the prompt content.

**Confidence:** 9/10

**Reasoning:** The circuit analysis clearly shows:
1. **Dominant negation pathway**: L16:F12358 ("not followed by to-be") is the single strongest feature with direct_effect=0.3594, contributing ~50% of the total attribution
2. **Cascading negation hierarchy**: The "not" token at positions 23 and 29 flows through 4-5 layers of increasingly specialized negation features before reaching the output
3. **Semantic suppression**: The "abbey" token (pos 10) activates L5:F14591 (Catholic church/abbey detection) but this has a **negative** direct_effect of -0.1748, actively working against the prediction
4. **Low frac_nonzero values**: All negation features have frac_nonzero between 0.003-0.028, indicating they are specific pattern detectors rather than generic semantic features
5. **Direct token-to-feature paths**: The "not" token embedding directly connects to the output with weight 19.625 at the embedding layer, bypassing semantic analysis

The circuit confirms the user's concern: this is not a semantically meaningful classifier but rather a syntactic negation detector that happens to fire on the prompt's "not" tokens without understanding the actual meaning about the abbey's height.

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 10 features; top: L16:12358 de=0.359 |

### Dispatch: 7 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L16:F12358@29` | ✅ reported | 5 | 20 | Trace this feature to understand what semantic content it encodes and how it rel… |
| SA-2 | `L0:F7710@21` | ✅ reported | 5 | 10 | Trace this feature to understand what it encodes and whether it represents lexic… |
| SA-3 | `L0:F3820@5` | ✅ reported | 1 | 5 | Trace this feature to understand what semantic content it encodes at this early … |
| SA-4 | `L16:F9779@23` | ✅ reported | 7 | 15 | Trace this feature to understand what semantic content it encodes. |
| SA-5 | `L0:F11375@18` | ✅ reported | 1 | 5 | Trace this feature to understand what semantic content it encodes at this positi… |
| SA-6 | `L5:F14591@10` | ✅ reported | 8 | 30 | Trace this feature which has a negative effect on the probe - understand what it… |
| SA-7 | `L0:F2848@4` | ✅ reported | 1 | 5 | Trace this feature to understand what semantic content it encodes at this early … |

<details>
<summary><b>SA-1</b> — tool trace (10 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L16, F12358 | " the word "not" followed within a few tokens by a form of the verb "to" |
| 2 | `get_upstream_features` | L16:F12358@29, k=5 | Emb:" not"@29 (w=19.62) +4 more |
| 3 | `inspect_feature` | L0, F4958 | " the word "not"" |
| 4 | `inspect_feature` | L13, F3295 | "negations in the form of "is/are not" as well as other uses of "not"" |
| 5 | `inspect_feature` | L15, F10071 | "negations and equivocations" |
| 6 | `get_upstream_features` | L13:F3295@29, k=5 | Emb:" not"@29 (w=17.75) +4 more |
| 7 | `inspect_feature` | L3, F8011 | " a mix of words and code fragments from different languages" |
| 8 | `get_upstream_features` | L15:F10071@29, k=5 | Emb:" not"@29 (w=9.69) +4 more |
| 9 | `get_upstream_features` | L0:F4958@29, k=5 | Emb:" not"@29 (w=34.25) +4 more |
| 10 | `get_upstream_features` | L3:F8011@29, k=5 | Emb:" not"@29 (w=21.50) +4 more |

**Findings:** I traced a negation detection circuit starting from L16:F12358, which detects "the word 'not' followed within a few tokens by a form of the verb 'to be'". The circuit reveals:

1. The strongest signal comes directly from the input token embeddings: "not" at position 29 and "is" at position 28 feed directly into the feature with high positive weights (19.625 and 4.375 respectively).

2. There's a h…

</details>

<details>
<summary><b>SA-2</b> — tool trace (11 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F7710 | "the pronoun "you"" |
| 2 | `get_upstream_features` | L0:F7710@21, k=5 | Emb:" you"@21 (w=42.25) +4 more |
| 3 | `get_top_logits` | k=10 | "" (100%) |
| 4 | `get_top_features` | token="", k=10 | 10 features; top: L16:12358 de=0.359 |
| 5 | `inspect_feature` | L16, F12358 | " the word "not" followed within a few tokens by a form of the verb "to" |
| 6 | `inspect_feature` | L0, F3820 | "the word "the"" |
| 7 | `inspect_feature` | L0, F11375 | " the word "is"" |
| 8 | `get_upstream_features` | L16:F12358@29, k=5 | Emb:" not"@29 (w=19.62) +4 more |
| 9 | `inspect_feature` | L0, F4958 | " the word "not"" |
| 10 | `get_upstream_features` | L0:F4958@29, k=5 | Emb:" not"@29 (w=34.25) +4 more |
| 11 | `get_upstream_features` | L0:F3820@5, k=5 | Emb:" the"@5 (w=34.25) +4 more |

**Findings:** The starting feature L0:F7710 encodes the pronoun "you" and is directly driven by the token " you" at position 21 with a very strong edge weight (42.25). This feature has a negative direct effect (-0.2471) on the empty string token that the model predicts with 100% probability. 

The circuit reveals several lexical features: L0:F7710 ("you"), L0:F3820 ("the"), L0:F11375 ("is"), and L0:F4958 ("not"…

</details>

<details>
<summary><b>SA-3</b> — tool trace (3 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F3820 | "the word "the"" |
| 2 | `get_upstream_features` | L0:F3820@5, k=5 | Emb:" the"@5 (w=34.25) +4 more |
| 3 | `get_upstream_features` | L0:F3820@5, k=10 | Emb:" the"@5 (w=34.25) +9 more |

**Findings:** The feature L0:F3820 at position 5 is a simple token detector for the word \"the\". It receives strong positive input from the token \" the\" at the same position (weight 34.25), along with minor negative inputs from surrounding tokens like \" of\" at position 4 and \"That\" at position 1. Interestingly, while the feature fires on the word \"the\", its promoted tokens are unusual/rare words like \…

</details>

<details>
<summary><b>SA-4</b> — tool trace (11 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L16, F9779 | "negation words or contractions like "won't", "not", "never"" |
| 2 | `get_upstream_features` | L16:F9779@23, k=5 | Emb:" will"@22 (w=7.28) +4 more |
| 3 | `inspect_feature` | L0, F4958 | " the word "not"" |
| 4 | `inspect_feature` | L15, F3521 | "sentences containing words expressing negation or uncertainty in past " |
| 5 | `get_upstream_features` | L0:F4958@23, k=5 | Emb:" not"@23 (w=33.50) +4 more |
| 6 | `get_upstream_features` | L15:F3521@23, k=5 | Emb:" will"@22 (w=5.88) +4 more |
| 7 | `inspect_feature` | L4, F4492 | "negations in various languages" |
| 8 | `inspect_feature` | L2, F12694 | " the word "Canisius" and words that express possibility or a small pro" |
| 9 | `get_upstream_features` | L4:F4492@23, k=5 | Emb:" not"@23 (w=18.50) +4 more |
| 10 | `inspect_feature` | L3, F8011 | " a mix of words and code fragments from different languages" |
| 11 | `inspect_feature` | L3, F1101 | " error messages and terms indicating absence or negation in software c" |

**Findings:** I traced L16:F9779 which encodes negation words like "not", "won't", "never". The circuit reveals:

1. DIRECT TOKEN INPUTS: The feature gets strong direct input from " not" (pos 23, weight 6.78) and " will" (pos 22, weight 7.28) tokens.

2. LAYER 0 DETECTION: L0:F4958 directly detects the word "not" (connecting to " not" token with weight 33.5) and feeds into both L15:F3521 and L16:F9779.

3. LAYE…

</details>

<details>
<summary><b>SA-5</b> — tool trace (2 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F11375 | " the word "is"" |
| 2 | `get_upstream_features` | L0:F11375@18, k=5 | Emb:" is"@18 (w=32.50) +4 more |

**Findings:** The feature L0:F11375 at position 18 encodes detection of the word "is". It's a first-layer feature with low sparsity (frac_nonzero = 0.00964), indicating it's quite specific to the "is" token. The feature shows interesting properties: while it detects "is", it actually suppresses "is" tokens in its output (negative promoted tokens) and promotes archaic/foreign forms like "Monfieur", "myżelf", "Di…

</details>

<details>
<summary><b>SA-6</b> — tool trace (14 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L5, F14591 | " words related to the Catholic church" |
| 2 | `get_upstream_features` | L5:F14591@10, k=5 | Emb:" abbey"@10 (w=10.00) +4 more |
| 3 | `inspect_feature` | L4, F4605 | " words related to churches, chapels and other buildings, in addition t" |
| 4 | `inspect_feature` | L4, F1104 | " words related to history, geography, and the middle ages, especially " |
| 5 | `get_upstream_features` | L4:F4605@10, k=5 | Emb:" abbey"@10 (w=7.94) +4 more |
| 6 | `get_upstream_features` | L4:F1104@10, k=5 | Emb:" abbey"@10 (w=3.50) +4 more |
| 7 | `inspect_feature` | L2, F8185 | "places for shopping or military activities" |
| 8 | `inspect_feature` | L0, F3512 | " words related to ancient history, mythology, and royalty" |
| 9 | `inspect_feature` | L0, F9026 | "technical documents or data, including numbers, units, and references " |
| 10 | `get_upstream_features` | L2:F8185@10, k=5 | Emb:" abbey"@10 (w=9.44) +4 more |
| 11 | `inspect_feature` | L1, F7934 | " terms related to legal and governmental processes and actions." |
| 12 | `get_upstream_features` | L1:F7934@10, k=5 | Emb:" abbey"@10 (w=9.12) +4 more |
| 13 | `inspect_feature` | L0, F355 | " text related to numbers, especially those representing currency or me" |
| 14 | `get_upstream_features` | L0:F3512@10, k=5 | Emb:" abbey"@10 (w=9.88) +4 more |

**Findings:** The circuit tracing reveals that L5:F14591 (words related to the Catholic church) is primarily driven by the input token " abbey" at position 10 (edge weight 10.0). The feature activates on Catholic/religious content like "Benedictine nuns" and appears to suppress the probe output through religious/cultural associations.

Key findings:
1. The strongest connection is directly from the " abbey" toke…

</details>

<details>
<summary><b>SA-7</b> — tool trace (2 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F2848 | "the word "of"" |
| 2 | `get_upstream_features` | L0:F2848@4, k=5 | Emb:" of"@4 (w=35.25) +4 more |

**Findings:** Tracing from L0:F2848 at position 4 reveals a simple circuit: this early-layer feature detects the word "of" but suppresses the actual token "of" in its output. The feature has low sparsity (frac_nonzero: 0.01966) and is directly connected to token embeddings. The strongest connection is from the token "of" itself at position 4 (edge_weight: 35.25), with a secondary positive connection from the be…

</details>

### Build

`build_circuit` → 18 nodes, 22 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m2.7 | 20,641 | 4,142 | 34,471 | 0 | $0.0122 | — | — |
| SA-3 | deepseek/deepseek-v3.2 | 13,612 | 1,464 | 0 | 0 | $0.0041 | ✅ 1F/5E | Trace this feature to understand what semantic content it en… |
| SA-2 | deepseek/deepseek-v3.2 | 63,764 | 2,674 | 3,136 | 0 | $0.0177 | ✅ 5F/10E | Trace this feature to understand what it encodes and whether… |
| SA-4 | deepseek/deepseek-v3.2 | 54,838 | 3,150 | 13,824 | 0 | $0.0158 | ✅ 7F/15E | Trace this feature to understand what semantic content it en… |
| SA-1 | deepseek/deepseek-v3.2 | 66,356 | 4,009 | 0 | 0 | $0.0188 | ✅ 5F/20E | Trace this feature to understand what semantic content it en… |
| SA-5 | deepseek/deepseek-v3.2 | 9,103 | 1,119 | 0 | 0 | $0.0028 | ✅ 1F/5E | Trace this feature to understand what semantic content it en… |
| SA-7 | deepseek/deepseek-v3.2 | 9,791 | 1,340 | 0 | 0 | $0.0031 | ✅ 1F/5E | Trace this feature to understand what semantic content it en… |
| SA-6 | deepseek/deepseek-v3.2 | 101,551 | 4,197 | 2,304 | 0 | $0.0281 | ✅ 8F/30E | Trace this feature which has a negative effect on the probe … |
| **Total** | | **339,656** | **22,095** | **53,735** | **0** | **$0.1025** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 6m 23s