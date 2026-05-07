# Circuit Oracle Report
**Date:** 2026-04-06 18:09:18 UTC | **Orchestrator:** minimax/minimax-m2.7 | **Subagent:** deepseek/deepseek-v3.2

## Input

**Prompt:** "Dataset: multinli-pos_pos_9 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "('The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction.',)"

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The attribution circuit reveals that the layer-22 probe's classification score is primarily driven by competing signals: **negation features at position 17** ("not", "n't") from the second sentence ("Recorded menus do not provide any information at this time.") contribute **positively** to the probe score (L16:F6800, direct_effect=+0.4316; L0:F4958, +0.4297; L4:F4492, +0.3867), while **lexical content features** from the first sentence contribute **negatively** (L0:F2108 "menu", -0.6328; L1:F12253 "menu", -0.4707). A spurious feature (L0:F13938 detecting "wild" but activated by "recorded", -0.373) also contributes negatively.

**Confidence:** 9/10

**Reasoning:** The trace reveals two distinct signal pathways converging on the probe:

1. **Negation cascade (pos 17, positive effect):** The token " not" at position 17 (from "do not provide") feeds into a hierarchical negation detection circuit spanning layers 0-16. L16:F6800 explicitly encodes "negations 'not', 'no', and contractions with 't'" (frac_nonzero=0.031), with direct token embedding weight of 11.8125. This cascades through L14:F6648 (speculation/negation), L13:F102 (phrases with "not"), L12:F9489 (negations+verbs), L3:F3534 ("n't" character sequence), down to L0:F4958 (word "not"). The "don't" pattern is also detected by L1:F14233 and L1:F10072.

2. **Content features (pos 2-3, negative effect):** The first sentence "A recorded menu" triggers L1:F3691 ("recording in scientific documentation", +0.8281), L2:F8776 ("finance/property law", +0.6328), and L0:F7443 ("record" word, +0.582). The word "menu" activates L0:F2108 (-0.6328) and L1:F12253 (-0.4707). A spurious feature L0:F13938 ("wild" pattern) incorrectly activates on "recorded" (-0.373).

The user's concern is **partially validated**: negation features are indeed the dominant positive drivers (accounting for ~1.25 combined direct_effect), while content features from the first sentence contribute negatively. The circuit does rely on "negation words" (the "not" token in the second sentence) rather than semantic contradiction detection. However, the circuit also incorporates genuine lexical content (the "recorded menu" features), suggesting it's using both spurious negation signals AND actual prompt content — though the negation signals appear to override in determining the probe's classification direction.

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 10 features; top: L1:3691 de=0.828 |

### Dispatch: 9 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L1:F3691@2` | ✅ reported | 5 | 11 | Trace L1:3691 to understand what semantic content it encodes. Check if it's a sp… |
| SA-2 | `L2:F8776@2` | ✅ reported | 4 | 15 | Trace L2:8776 to understand what semantic content it encodes. Is this a negation… |
| SA-3 | `L0:F2108@3` | ✅ reported | 2 | 5 | Trace L0:2108 (pos 3, negative effect) - this could be a negation or generic pat… |
| SA-4 | `L0:F7443@2` | ✅ reported | 3 | 2 | Trace L0:7443 (pos 2, positive effect) - could be lexical pattern. Check what th… |
| SA-5 | `L1:F12253@3` | ✅ reported | 3 | 12 | Trace L1:12253 (pos 3, negative effect). Could this be a negation or generic pat… |
| SA-6 | `L16:F6800@17` | ✅ reported | 8 | 19 | Trace L16:6800 (pos 17) - a higher layer feature that may encode more abstract s… |
| SA-7 | `L4:F4492@17` | ✅ reported | 6 | 23 | Trace L4:4492 (pos 17, positive effect) - what does this feature encode at layer… |
| SA-8 | `L4:F2422@17` | ✅ reported | 8 | 12 | Trace L4:2422 (pos 17, negative effect) - could be negation-related. Check what … |
| SA-9 | `L0:F13938@2` | ✅ reported | 1 | 3 | Trace L0:13938 (pos 2, negative effect). What does this feature encode - could i… |

<details>
<summary><b>SA-1</b> — tool trace (9 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L1, F3691 | " the word "recording" in scientific or experimental documentation" |
| 2 | `get_upstream_features` | L1:F3691@2, k=5 | Emb:" recorded"@2 (w=24.75) +4 more |
| 3 | `inspect_feature` | L0, F7404 | " the word "faith", sometimes in association with related ideas like "l" |
| 4 | `inspect_feature` | L0, F6421 | " words related to administrative processes and computer programs" |
| 5 | `get_upstream_features` | L0:F7404@2, k=5 | Emb:" recorded"@2 (w=14.25) +4 more |
| 6 | `get_upstream_features` | L0:F6421@2, k=5 | Emb:"<bos>"@0 (w=9.81) +4 more |
| 7 | `get_top_logits` | k=5 | "" (100%) |
| 8 | `inspect_feature` | L0, F355 | " text related to numbers, especially those representing currency or me" |
| 9 | `inspect_feature` | L0, F478 | "various kinds of brackets and parentheses followed by a period" |

**Findings:** The circuit analysis reveals that L1:3691 encodes a feature that detects the word "recording" in scientific or experimental documentation contexts, but surprisingly suppresses actual recording-related tokens. The strongest input comes directly from the embedding of " recorded" at position 2 (weight 24.75), with additional positive contributions from L0:7404 (faith-related feature) and the <bos> to…

</details>

<details>
<summary><b>SA-2</b> — tool trace (9 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L2, F8776 | " words related to finance and property law" |
| 2 | `get_upstream_features` | L2:F8776@2, k=5 | Emb:" recorded"@2 (w=19.50) +4 more |
| 3 | `inspect_feature` | L1, F3691 | " the word "recording" in scientific or experimental documentation" |
| 4 | `inspect_feature` | L0, F7443 | "the word "record" appearing in various contexts" |
| 5 | `get_upstream_features` | L1:F3691@2, k=5 | Emb:" recorded"@2 (w=24.75) +4 more |
| 6 | `inspect_feature` | L0, F7404 | " the word "faith", sometimes in association with related ideas like "l" |
| 7 | `get_upstream_features` | L0:F7443@2, k=5 | Emb:" recorded"@2 (w=22.62) +4 more |
| 8 | `get_upstream_features` | L0:F7404@2, k=5 | Emb:" recorded"@2 (w=14.25) +4 more |
| 9 | `get_top_logits` | k=10 | "" (100%) |

**Findings:** The feature L2:8776 is NOT a negation signal. It encodes "words related to finance and property law". The circuit shows it's primarily driven by the token " recorded" at position 2 (strongest connection with weight 19.5). The feature has relatively low sparsity (frac_nonzero=0.011) indicating moderate specificity.

The upstream features include:
1. Direct token embedding connections: " recorded" (…

</details>

<details>
<summary><b>SA-3</b> — tool trace (3 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F2108 | "the word "menu"" |
| 2 | `get_upstream_features` | L0:F2108@3, k=5 | Emb:" menu"@3 (w=25.75) +4 more |
| 3 | `inspect_feature` | L0, F355 | " text related to numbers, especially those representing currency or me" |

**Findings:** The tracing reveals that L0:2108 at position 3 is a specific "menu" word detector feature with low sparsity (frac_nonzero=0.00353). The circuit is very simple: the feature directly receives strong input from the token embedding for " menu" at position 3 with edge weight 25.75. There are minor negative influences from " recorded" at position 2 and positive influences from "<bos>" and "A" tokens, bu…

</details>

<details>
<summary><b>SA-4</b> — tool trace (4 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F7443 | "the word "record" appearing in various contexts" |
| 2 | `get_upstream_features` | L0:F7443@2, k=5 | Emb:" recorded"@2 (w=22.62) +4 more |
| 3 | `inspect_feature` | L0, F355 | " text related to numbers, especially those representing currency or me" |
| 4 | `inspect_feature` | L0, F478 | "various kinds of brackets and parentheses followed by a period" |

**Findings:** The tracing reveals that L0:7443 (which detects the word "record") at position 2 is primarily driven by the token embedding of " recorded" at position 2 with a very strong edge weight of 22.625. This is a direct lexical pattern detection feature - it activates when it sees the token "record" and related forms. Interestingly, despite detecting "record", it suppresses "record"-related output tokens …

</details>

<details>
<summary><b>SA-5</b> — tool trace (6 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L1, F12253 | " the word 'menu'" |
| 2 | `get_upstream_features` | L1:F12253@3, k=5 | Emb:" menu"@3 (w=20.62) +4 more |
| 3 | `inspect_feature` | L0, F2108 | "the word "menu"" |
| 4 | `inspect_feature` | L0, F2115 | " data reported as a percentage inside brackets, especially in a labora" |
| 5 | `get_upstream_features` | L0:F2108@3, k=5 | Emb:" menu"@3 (w=25.75) +4 more |
| 6 | `get_upstream_features` | L0:F2115@3, k=3 | Emb:" menu"@3 (w=8.56) +2 more |

**Findings:** Tracing L1:12253 (pos 3) revealed it's a simple token detector for the word "menu". The circuit is very shallow: the L1 feature is driven primarily (20.625 edge weight) directly from the token embedding " menu" at position 3, with a smaller contribution (2.1562) from L0 feature 2108 which also detects "menu". This L1 feature has low frac_nonzero (0.00409), indicating it's specific and selective fo…

</details>

<details>
<summary><b>SA-6</b> — tool trace (15 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L16, F6800 | " negations "not", "no", and contractions with "t". " |
| 2 | `get_upstream_features` | L16:F6800@17, k=5 | Emb:" not"@17 (w=11.81) +4 more |
| 3 | `inspect_feature` | L15, F11794 | " phrases that express disagreement or negation" |
| 4 | `inspect_feature` | L3, F3534 | "the character sequence "n't" or "nut"" |
| 5 | `inspect_feature` | L0, F4958 | " the word "not"" |
| 6 | `get_upstream_features` | L15:F11794@17, k=5 | L14:F6648 (w=3.78) +4 more |
| 7 | `inspect_feature` | L14, F6648 | " words and phrases that indicate speculation, possibility, or negation" |
| 8 | `get_upstream_features` | L14:F6648@17, k=5 | Emb:" not"@17 (w=6.91) +4 more |
| 9 | `inspect_feature` | L13, F102 | " phrases containing "not" or negative connotations" |
| 10 | `get_upstream_features` | L13:F102@17, k=5 | Emb:" not"@17 (w=8.31) +4 more |
| 11 | `inspect_feature` | L12, F9489 | "negations combined with verbs, modal verbs, and words relating to yout" |
| 12 | `get_upstream_features` | L12:F9489@17, k=5 | Emb:" not"@17 (w=8.62) +4 more |
| 13 | `get_upstream_features` | L3:F3534@17, k=5 | Emb:" not"@17 (w=16.12) +4 more |
| 14 | `inspect_feature` | L0, F9203 | " instances of disagreement" |
| 15 | `get_upstream_features` | L0:F4958@17, k=5 | Emb:" not"@17 (w=33.50) +4 more |

**Findings:** The feature L16:F6800 at position 17 is a high-level semantic feature that detects negations ("not", "no", and contractions with "t"). This feature has a relatively low frac_nonzero (0.03101), indicating it's specific to negation contexts. 

Tracing the circuit reveals a clear hierarchical structure: the feature builds upon lower-layer negation detection features, ultimately tracing back to the to…

</details>

<details>
<summary><b>SA-7</b> — tool trace (11 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F4492 | "negations in various languages" |
| 2 | `get_upstream_features` | L4:F4492@17, k=5 | Emb:" not"@17 (w=17.50) +4 more |
| 3 | `inspect_feature` | L3, F1101 | " error messages and terms indicating absence or negation in software c" |
| 4 | `inspect_feature` | L3, F3534 | "the character sequence "n't" or "nut"" |
| 5 | `inspect_feature` | L3, F8011 | " a mix of words and code fragments from different languages" |
| 6 | `get_upstream_features` | L3:F1101@17, k=5 | Emb:" not"@17 (w=13.00) +4 more |
| 7 | `get_upstream_features` | L3:F8011@17, k=5 | Emb:" not"@17 (w=20.62) +4 more |
| 8 | `inspect_feature` | L0, F4958 | " the word "not"" |
| 9 | `get_upstream_features` | L0:F4958@17, k=5 | Emb:" not"@17 (w=33.50) +4 more |
| 10 | `get_upstream_features` | L3:F3534@17, k=5 | Emb:" not"@17 (w=16.12) +4 more |
| 11 | `inspect_feature` | L1, F14233 | " negative sentiment markers such as "not," "no," "never," and their eq" |

**Findings:** L4:F4492 at position 17 encodes "negations in various languages". The circuit analysis reveals it primarily detects the word "not" through several pathways:

1. **Direct embedding connection**: Strongest input comes directly from the token " not" at position 17 (weight: 17.5)

2. **Layer 3 features feeding into L4:4492**:
   - L3:1101 detects "error messages and terms indicating absence or negatio…

</details>

<details>
<summary><b>SA-8</b> — tool trace (13 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F2422 | "negations in other languages like French, Malay, and Croatian" |
| 2 | `get_upstream_features` | L4:F2422@17, k=5 | Emb:" not"@17 (w=16.12) +4 more |
| 3 | `inspect_feature` | L3, F1101 | " error messages and terms indicating absence or negation in software c" |
| 4 | `inspect_feature` | L3, F9803 | "sentences describing scientific studies or experiments, particularly w" |
| 5 | `inspect_feature` | L3, F8011 | " a mix of words and code fragments from different languages" |
| 6 | `get_upstream_features` | L3:F9803@17, k=5 | Emb:" not"@17 (w=13.50) +4 more |
| 7 | `get_upstream_features` | L3:F8011@17, k=5 | Emb:" not"@17 (w=20.62) +4 more |
| 8 | `get_upstream_features` | L3:F1101@17, k=5 | Emb:" not"@17 (w=13.00) +4 more |
| 9 | `inspect_feature` | L0, F4958 | " the word "not"" |
| 10 | `inspect_feature` | L1, F14233 | " negative sentiment markers such as "not," "no," "never," and their eq" |
| 11 | `inspect_feature` | L1, F10072 | " the contraction "don't"" |
| 12 | `inspect_feature` | L1, F5108 | "the word "not"" |
| 13 | `get_upstream_features` | L0:F4958@17, k=5 | Emb:" not"@17 (w=33.50) +4 more |

**Findings:** I traced the negation-related circuit starting from L4:2422, which detects "negations in other languages like French, Malay, and Croatian". The circuit reveals a clear pattern:

1. The strongest connections are direct from token embeddings: "not" at position 17 feeds into L4:2422 with weight 16.125, and also into L3:8011 (weight 20.625) and L3:9803 (weight 13.5).

2. L3:1101 (error messages and so…

</details>

<details>
<summary><b>SA-9</b> — tool trace (2 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F13938 | "the word "wild"" |
| 2 | `get_upstream_features` | L0:F13938@2, k=5 | Emb:" recorded"@2 (w=12.88) +4 more |

**Findings:** L0:F13938 at position 2 encodes \"the word 'wild'\" but is being strongly activated by the token \" recorded\" at position 2 (edge_weight 12.875). The feature has low frac_nonzero (0.01844) indicating specificity. This appears to be a character/pattern matching feature that detects the token \"wild\" but in this context responds to \" recorded\", likely due to shared character patterns. It doesn't…

</details>

### Build

`build_circuit` → 0 nodes, 0 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m2.7 | 33,781 | 8,709 | 427,730 | 0 | $0.0334 | — | — |
| SA-3 | deepseek/deepseek-v3.2 | 13,631 | 1,240 | 0 | 0 | $0.0040 | ✅ 2F/5E | Trace L0:2108 (pos 3, negative effect) - this could be a neg… |
| SA-4 | deepseek/deepseek-v3.2 | 18,615 | 1,239 | 0 | 0 | $0.0053 | ✅ 3F/2E | Trace L0:7443 (pos 2, positive effect) - could be lexical pa… |
| SA-2 | deepseek/deepseek-v3.2 | 43,369 | 2,532 | 6,656 | 0 | $0.0124 | ✅ 4F/15E | Trace L2:8776 to understand what semantic content it encodes… |
| SA-1 | deepseek/deepseek-v3.2 | 50,734 | 2,830 | 0 | 0 | $0.0143 | ✅ 5F/11E | Trace L1:3691 to understand what semantic content it encodes… |
| SA-5 | deepseek/deepseek-v3.2 | 29,191 | 1,940 | 0 | 0 | $0.0083 | ✅ 3F/12E | Trace L1:12253 (pos 3, negative effect). Could this be a neg… |
| SA-8 | deepseek/deepseek-v3.2 | 75,467 | 3,323 | 15,296 | 0 | $0.0213 | ✅ 8F/12E | Trace L4:2422 (pos 17, negative effect) - could be negation-… |
| SA-7 | deepseek/deepseek-v3.2 | 60,590 | 3,864 | 9,792 | 0 | $0.0175 | ✅ 6F/23E | Trace L4:4492 (pos 17, positive effect) - what does this fea… |
| SA-6 | deepseek/deepseek-v3.2 | 111,503 | 4,099 | 3,200 | 0 | $0.0306 | ✅ 8F/19E | Trace L16:6800 (pos 17) - a higher layer feature that may en… |
| SA-9 | deepseek/deepseek-v3.2 | 9,113 | 1,156 | 0 | 0 | $0.0028 | ✅ 1F/3E | Trace L0:13938 (pos 2, negative effect). What does this feat… |
| **Total** | | **445,994** | **30,932** | **462,674** | **0** | **$0.1499** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 7m 18s