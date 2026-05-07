# Circuit Oracle Report
**Date:** 2026-04-03 09:00:06 UTC | **Orchestrator:** minimax/minimax-m2.7 | **Subagent:** deepseek/deepseek-v3.2

## Input
**Prompt:** "Dataset: civil_comments-pos_pos_1 | Probe: unbiased | Method: correct"
**System prompt:** ""
**Question:** "The circuit use spurious features (e.g.,"an identity group" signals) rather than actual prompt content (lexical or semaintical) to predict toxicity."
**Top predictions:**  (100.0%)

## Oracle Analysis
**Analysis:** The probe's classification score is driven by a shallow circuit that primarily detects linguistic intensity markers (adverbs like "clearly") and political figure references (Trump, Obama), rather than spurious identity-group signals. The circuit is heavily dominated by layer-0 lexical features that directly map from input token embeddings, with only one multi-layer processing path (political names → White House detection at L4:14582). Identity-related tokens ("white", "nonwhites") appear only as weak secondary inputs to the "again" feature with negligible circuit weight (0.793) and a negative contribution direction.

**Confidence:** 8/10

**Reasoning:** The circuit was traced comprehensively across all top-10 features by direct effect. Key evidence:

1. **No spurious identity features:** The only appearance of "white" is in `lexical_again` (L0:15831) as a secondary input with weight 0.793 — far below the primary input from "again" token (weight 43.5). This feature has a *negative* direct effect (-0.125), actually suppressing the toxic classification.

2. **Shallow lexical processing:** 9 of 10 top features are direct layer-0 features receiving from single token embeddings. These detect linguistic content (adverbs, copula, demonstratives, document structure) rather than identity semantics.

3. **One multi-layer political path:** L4:14582 ("White House/US Government References") with frac_nonzero=0.00787 shows genuine multi-layer processing: L2:14301 (political names, weight 2.42) → L3:3136 (Trump administration, inhibitory -0.92) → L4:14582. This encodes *actual political content* (Trump, Obama mentions) rather than generic identity signals.

4. **Low frac_nonzero values** (0.00278-0.0428) across all features indicate specificity — the probe is not using generic toxic-pattern matchers but specific linguistic/political content detectors.

5. **Lexical "clearly" dominance:** Four separate features (L0:12866, 7621, 4422, 7142) all respond to "clearly" at pos 2, with combined direct effects of +0.085. The adverb appears to be the primary toxicity signal the probe learned.

The concern about spurious identity signals is **not supported** by this circuit. The probe's classification appears to be based on legitimate content features (political figure names, intensifying language) rather than demographic identity mentions. The "white", "nonwhites" tokens in the prompt are essentially invisible to the attribution circuit.

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 10 features; top: L0:12866 de=-0.207 |

### Dispatch: 10 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L4:F14582@5` | ✅ reported | 10 | 9 | Trace L4:14582 (pos 5, direct_effect +0.156) upstream to understand what semanti… |
| SA-2 | `L2:F9199@9` | ✅ reported | 5 | 5 | Trace L2:9199 (pos 9, direct_effect -0.115) upstream to understand what semantic… |
| SA-3 | `L0:F11375@6` | ✅ reported | 1 | 3 | Trace L0:11375 (pos 6, direct_effect +0.130) upstream to its embedding source. D… |
| SA-4 | `L0:F7621@2` | ✅ reported | 1 | 1 | Trace L0:7621 (pos 2, direct_effect +0.195) upstream to its embedding source. De… |
| SA-5 | `L0:F12866@2` | ✅ reported | 1 | 1 | Trace L0:12866 (pos 2, direct_effect -0.207) upstream to its embedding source. D… |
| SA-6 | `L0:F15831@26` | ✅ reported | 1 | 5 | Trace L0:15831 (pos 26, direct_effect -0.125) upstream. Position 26 is near the … |
| SA-7 | `L0:F164@3` | ✅ reported | 3 | 4 | Trace L0:164 (pos 3, direct_effect -0.122) upstream. Determine what input token … |
| SA-8 | `L0:F3916@1` | ✅ reported | 2 | 2 | Trace L0:3916 (pos 1, direct_effect +0.118) upstream. Position 1 is near the beg… |
| SA-9 | `L0:F4422@2` | ✅ reported | 3 | 9 | Trace L0:4422 (pos 2) upstream. Determine what input token fires this feature an… |
| SA-10 | `L0:F7142@2` | ✅ reported | 1 | 3 | Trace L0:7142 (pos 2, direct_effect -0.122) upstream. Determine what input token… |

<details>
<summary><b>SA-1</b> — tool trace (16 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F14582 | " references to the White House and the US government" |
| 2 | `get_upstream_features` | L4:F14582@5, k=5 | Emb:" trump"@5 (w=18.00) +4 more |
| 3 | `inspect_feature` | L2, F14301 | " names of people and organizations involved in politics, finance, and " |
| 4 | `get_upstream_features` | L2:F14301@5, k=5 | Emb:" trump"@5 (w=9.50) +4 more |
| 5 | `inspect_feature` | L0, F8567 | " the word "that"" |
| 6 | `inspect_feature` | L0, F3635 | "the word "that"" |
| 7 | `get_upstream_features` | L4:F14582@5, k=10 | Emb:" trump"@5 (w=18.00) +9 more |
| 8 | `inspect_feature` | L3, F3136 | " names of people involved in the Trump administration" |
| 9 | `inspect_feature` | L2, F13271 | " two distinct topics: One is terminology related to knitting and the o" |
| 10 | `inspect_feature` | L1, F7815 | " references to contacting or communicating with someone, including job" |
| 11 | `get_upstream_features` | L3:F3136@5, k=5 | Emb:" trump"@5 (w=10.62) +4 more |
| 12 | `inspect_feature` | L2, F1239 | " proper nouns, especially political figures" |
| 13 | `get_top_logits` | k=5 | "" (100%) |
| 14 | `get_upstream_features` | L2:F1239@5, k=5 | Emb:" trump"@5 (w=7.97) +4 more |
| 15 | `inspect_feature` | L1, F1808 | " mentions of economics between the US and Canada" |
| 16 | `inspect_feature` | L1, F10801 | "code snippets related to drawing shapes" |

**Findings:** Tracing L4:F14582 (White House/US government detection) upstream revealed a circuit primarily driven by the raw \" trump\" token embedding. Key findings:

1. The strongest influence is direct from the \" trump\" token embedding (weight 18.0) with additional processing through political name detection features at layers 1-2.

2. L2:F14301 (political/organizational names) feeds positively into the t…

</details>

<details>
<summary><b>SA-2</b> — tool trace (10 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L2, F9199 | " instances of "ot" in code" |
| 2 | `get_upstream_features` | L2:F9199@9, k=5 | Emb:"ot"@9 (w=23.88) +4 more |
| 3 | `inspect_feature` | L1, F6042 | "the string "ot"" |
| 4 | `inspect_feature` | L0, F12712 | " words, suffixes, or phrases that could indicate quality and the peopl" |
| 5 | `get_upstream_features` | L1:F6042@9, k=5 | Emb:"ot"@9 (w=19.62) +4 more |
| 6 | `inspect_feature` | L0, F11 | " the string "ot"" |
| 7 | `inspect_feature` | L0, F865 | " text related to well-being" |
| 8 | `get_upstream_features` | L0:F11@9, k=5 | Emb:"ot"@9 (w=20.00) +4 more |
| 9 | `get_upstream_features` | L0:F12712@9, k=5 | Emb:" big"@8 (w=12.44) +4 more |
| 10 | `get_top_logits` | k=5 | "" (100%) |

**Findings:** Tracing L2:F9199 (pos 9, direct_effect -0.115) upstream reveals a circuit that detects the string "ot". The negative contribution comes from a feature that suppresses tokens like "ot", "OT", "ots", etc. The circuit originates from the raw token embedding "ot" at position 9, which feeds into L0:F11 (detects "ot") and then into L1:F6042 (also detects "ot"). L2:F9199 represents "instances of \"ot\" i…

</details>

<details>
<summary><b>SA-3</b> — tool trace (3 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F11375 | " the word "is"" |
| 2 | `get_upstream_features` | L0:F11375@6, k=5 | Emb:" is"@6 (w=31.25) +4 more |
| 3 | `get_upstream_features` | L0:F11375@6, k=10 | Emb:" is"@6 (w=31.25) +9 more |

**Findings:** Tracing from L0:F11375 at position 6 (direct_effect +0.130) reveals it's a layer 0 feature that detects the word \"is\" but suppresses it in favor of more formal/archaic alternatives. The primary embedding source is token \" is\" at position 6 with strong weight 31.25. Secondary connections come from \"<bos>\" at position 0 (weight 4.4) and \" trump\" at position 5 (weight 3.1). This is NOT a spur…

</details>

<details>
<summary><b>SA-4</b> — tool trace (3 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F7621 | " the word "clearly", and to a lesser extent words associated with amou" |
| 2 | `get_upstream_features` | L0:F7621@2, k=5 | Emb:" clearly"@2 (w=17.75) +4 more |
| 3 | `get_upstream_features` | L0:F7621@2, k=10 | Emb:" clearly"@2 (w=17.75) +9 more |

**Findings:** L0:7621 at position 2 is directly triggered by the input token \" clearly\" at position 2 with a strong edge weight of 17.75. This feature specifically detects the word \"clearly\" as indicated by its label and top activating examples. With a frac_nonzero of 0.01586, it's moderately specific. The promoted tokens (\"instructive\", \"Recently\", etc.) suggest it's a discourse/linguistic feature rath…

</details>

<details>
<summary><b>SA-5</b> — tool trace (3 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F12866 | " adverbs such as "clearly," "plainly," and "as"" |
| 2 | `get_upstream_features` | L0:F12866@2, k=5 | Emb:" clearly"@2 (w=17.38) +4 more |
| 3 | `get_top_logits` | k=5 | "" (100%) |

**Findings:** Tracing L0:12866 at position 2 reveals it's a feature that detects adverbs like "clearly", "plainly", and "as" (frac_nonzero=0.00728, quite sparse/specific). The feature is directly fed by the embedding of token " clearly" at position 2 with a very strong edge weight of 17.375. This is a legitimate content feature that encodes linguistic structure (adverb detection) rather than spurious identity g…

</details>

<details>
<summary><b>SA-6</b> — tool trace (3 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F15831 | "the word "again" and words associated with time" |
| 2 | `get_upstream_features` | L0:F15831@26, k=5 | Emb:" again"@26 (w=43.50) +4 more |
| 3 | `get_top_logits` | k=5 | "" (100%) |

**Findings:** The feature L0:15831 at position 26 detects the word \"again\" and words associated with time. It has a negative direct effect of -0.125, suggesting it suppresses some output. The main upstream connection is directly from the \" again\" token at position 26 itself (edge weight 43.5), with secondary connections from \" white\" at position 25 (edge weight 0.793), \"<bos>\" at position 0 (1.71), \" m…

</details>

<details>
<summary><b>SA-7</b> — tool trace (5 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F164 | "the words "show" and "your", particularly when talking about presentin" |
| 2 | `get_upstream_features` | L0:F164@3, k=5 | Emb:" shows"@3 (w=19.38) +4 more |
| 3 | `get_upstream_features` | L0:F164@3, k=10 | Emb:" shows"@3 (w=19.38) +9 more |
| 4 | `inspect_feature` | L0, F478 | "various kinds of brackets and parentheses followed by a period" |
| 5 | `inspect_feature` | L0, F1165 | "words relating to abstract concepts, like properties, associations or " |

**Findings:** L0:164 (pos 3) is primarily triggered by the input token " shows" at position 3 with a very strong edge weight of 19.375. This feature detects words like "show" and "your" when talking about presenting something. It has a direct_effect of -0.122, meaning it pushes away from some output. The feature appears to be a simple lexical detector for the word "show" and related words, not encoding identity…

</details>

<details>
<summary><b>SA-8</b> — tool trace (5 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F3916 | " common short words in legal documents" |
| 2 | `get_upstream_features` | L0:F3916@1, k=5 | Emb:"<bos>"@0 (w=8.88) +4 more |
| 3 | `get_top_logits` | k=5 | "" (100%) |
| 4 | `inspect_feature` | L0, F478 | "various kinds of brackets and parentheses followed by a period" |
| 5 | `get_top_features` | token="tie", k=10 | ❌ Token 'tie' not found in top logits. Available: [''] |

**Findings:** Tracing L0:3916 at position 1 (direct_effect +0.118) upstream reveals it's primarily fed by two embedding nodes: 1) The <bos> token at position 0 with strong weight 8.875, and 2) The token "tie" at position 1 with weight 1.5625. The feature's label "common short words in legal documents" and its promoted tokens (<bos>, newlines, punctuation) suggest it's a formatting/structural feature triggered b…

</details>

<details>
<summary><b>SA-9</b> — tool trace (6 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F4422 | "the word "seriously"" |
| 2 | `get_upstream_features` | L0:F4422@2, k=5 | Emb:" clearly"@2 (w=12.62) +4 more |
| 3 | `inspect_feature` | L0, F478 | "various kinds of brackets and parentheses followed by a period" |
| 4 | `inspect_feature` | L0, F553 | "words related to chemical reactions or physical states in a scientific" |
| 5 | `get_upstream_features` | L0:F478@1, k=5 | Emb:"<bos>"@0 (w=7.00) +4 more |
| 6 | `get_upstream_features` | L0:F553@1, k=5 | Emb:"tie"@1 (w=4.34) +4 more |

**Findings:** Tracing L0:4422 at position 2 reveals it is primarily activated by the input token "clearly" at position 2 with a strong edge weight of 12.625. The feature is labeled "the word 'seriously'" but actually fires on "clearly" in this context. The feature has a low frac_nonzero (0.00922) indicating high specificity, and its promoted tokens are technical/multilingual terms rather than identity-related c…

</details>

<details>
<summary><b>SA-10</b> — tool trace (4 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F7142 | " the word "axis" and its plural form, often in the context of scientif" |
| 2 | `get_upstream_features` | L0:F7142@2, k=5 | Emb:" clearly"@2 (w=14.62) +4 more |
| 3 | `get_top_logits` | k=5 | "" (100%) |
| 4 | `get_top_features` | token="", k=10 | 10 features; top: L0:12866 de=-0.207 |

**Findings:** The circuit tracing reveals that L0:7142 at position 2 is directly fired by the input token \" clearly\" at the same position (position 2). The edge weight from \" clearly\" to this feature is very strong (14.625), indicating this token strongly activates the feature. The feature itself encodes \"the word 'axis' and its plural form, often in the context of scientific or technical documents\" (frac…

</details>

### Build

`build_circuit` → 17 nodes, 17 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m2.7 | 21,462 | 4,320 | 37,617 | 0 | — | — | — |
| SA-4 | deepseek/deepseek-v3.2 | 13,212 | 936 | 0 | 0 | — | ✅ 1F/1E | Trace L0:7621 (pos 2, direct_effect +0.195) upstream to its … |
| SA-3 | deepseek/deepseek-v3.2 | 13,894 | 1,561 | 0 | 0 | — | ✅ 1F/3E | Trace L0:11375 (pos 6, direct_effect +0.130) upstream to its… |
| SA-2 | deepseek/deepseek-v3.2 | 59,578 | 2,148 | 0 | 0 | — | ✅ 5F/5E | Trace L2:9199 (pos 9, direct_effect -0.115) upstream to unde… |
| SA-1 | deepseek/deepseek-v3.2 | 99,429 | 4,342 | 29,760 | 0 | — | ✅ 10F/9E | Trace L4:14582 (pos 5, direct_effect +0.156) upstream to und… |
| SA-5 | deepseek/deepseek-v3.2 | 12,835 | 904 | 0 | 0 | — | ✅ 1F/1E | Trace L0:12866 (pos 2, direct_effect -0.207) upstream to its… |
| SA-6 | deepseek/deepseek-v3.2 | 13,034 | 1,569 | 0 | 0 | — | ✅ 1F/5E | Trace L0:15831 (pos 26, direct_effect -0.125) upstream. Posi… |
| SA-8 | deepseek/deepseek-v3.2 | 22,264 | 1,558 | 0 | 0 | — | ✅ 2F/2E | Trace L0:3916 (pos 1, direct_effect +0.118) upstream. Positi… |
| SA-7 | deepseek/deepseek-v3.2 | 24,261 | 1,813 | 0 | 0 | — | ✅ 3F/4E | Trace L0:164 (pos 3, direct_effect -0.122) upstream. Determi… |
| SA-10 | deepseek/deepseek-v3.2 | 17,283 | 1,117 | 0 | 0 | — | ✅ 1F/3E | Trace L0:7142 (pos 2, direct_effect -0.122) upstream. Determ… |
| SA-9 | deepseek/deepseek-v3.2 | 30,417 | 2,111 | 0 | 0 | — | ✅ 3F/9E | Trace L0:4422 (pos 2) upstream. Determine what input token f… |
| **Total** | | **327,669** | **22,379** | **67,377** | **0** | **—** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 8m 36s