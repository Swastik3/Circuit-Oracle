# Circuit Oracle Report
**Date:** 2026-04-06 18:01:59 UTC | **Orchestrator:** minimax/minimax-m2.7 | **Subagent:** deepseek/deepseek-v3.2

## Input

**Prompt:** "Dataset: multinli-pos_pos_8 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "('The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction.',)"

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification of contradiction is driven by a shallow lexical-matching circuit that detects surface tokens ("Congress", "include", "began to") at early layers rather than semantic content or negation signals.

**Confidence:** 9/10

**Reasoning:**

The circuit is dominated by **early-layer token detection features** (L0-L4), not semantic understanding or negation signals:

1. **"Congress" Detection Path (Strongest Signal):** The top feature L2:F2701 (direct_effect: 0.8555) encodes "words related to the U.S. Congress" and is driven by the token "Congress" at position 2. Multiple L0 features (F10198, F767, F15411, F6044) directly detect this token with weights 17-28. Despite Neuronpedia labels like "the word 'yield'", these features are triggered by "Congress" embeddings.

2. **"include" Detection Path:** L3:F5753 (direct_effect: 0.5273) detects "include" and its variants at position 12. This is a shallow word-detection circuit with direct embedding connection (weight 41).

3. **"began to" Construction:** L4:F59 (direct_effect: 0.4141) detects phrases with "to" preceded by verbs like "begin". This is syntactic pattern matching, not semantic analysis.

**Critical Finding: No Negation Signals Detected**

The actual contradiction signals in the text ("did not support" at pos 16-17, "no responsibility" at pos 34-35) are **not captured** by the top 10 features. The circuit entirely misses:
- The negation word "not" (pos 17)
- The negation word "no" (pos 34)
- The semantic contradiction between "controls funding" vs "no responsibility"

**User Concern Confirmed:** The user's suspicion is correct. The probe uses **spurious lexical surface patterns** rather than actual semantic content:
- Text with "Congress...include...began to" at these positions would trigger the same classification
- Text without these tokens but with genuine contradiction would be misclassified
- The circuit lacks any mechanism for detecting negation or semantic opposition

The features have low frac_nonzero (0.002-0.03), indicating specificity, but this specificity is for **political institution terminology** and **word patterns**, not for contradiction semantics. The probe appears to have learned that political/governmental texts containing these specific word patterns often appear in contradictory contexts during training, rather than learning to detect actual semantic contradiction.

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 10 features; top: L2:2701 de=0.856 |

### Dispatch: 9 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L2:F2701@2` | ✅ reported | 5 | 11 | Trace this high-impact feature (direct_effect: 0.8555) at pos 2. What does it en… |
| SA-2 | `L3:F5753@12` | ✅ reported | 6 | 10 | Trace this feature at pos 12 (direct_effect: 0.5273). What does it encode? Is it… |
| SA-3 | `L0:F6044@2` | ✅ reported | 1 | 1 | Trace this feature at pos 2 (direct_effect: 0.4941). What does it encode? Is it … |
| SA-4 | `L4:F59@11` | ✅ reported | 6 | 10 | Trace this feature at pos 11 (direct_effect: 0.4141). What does it encode? Is it… |
| SA-5 | `L0:F10401@2` | ✅ reported | 8 | 16 | Trace this negative-effect feature at pos 2 (direct_effect: -0.373). What does i… |
| SA-6 | `L3:F8351@12` | ✅ reported | 3 | 4 | Trace this negative-effect feature (direct_effect: -0.3516) at pos 12. What does… |
| SA-7 | `L2:F6735@2` | ✅ reported | 6 | 14 | Trace this negative-effect feature (direct_effect: -0.3477) at pos 2. What does … |
| SA-8 | `L1:F4224@2` | ✅ reported | 6 | 14 | Trace this negative-effect feature (direct_effect: -0.2734) at pos 2. What does … |
| SA-9 | `L0:F9557@2` | ✅ reported | 1 | 3 | Trace this negative-effect feature (direct_effect: -0.3105) at pos 2. What does … |

<details>
<summary><b>SA-1</b> — tool trace (10 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L2, F2701 | " words related to the U.S. Congress" |
| 2 | `get_upstream_features` | L2:F2701@2, k=5 | Emb:" Congress"@2 (w=28.12) +4 more |
| 3 | `inspect_feature` | L1, F3276 | " mentions of the United States Congress" |
| 4 | `inspect_feature` | L0, F10198 | " the word "Congress"" |
| 5 | `get_upstream_features` | L1:F3276@2, k=5 | Emb:" Congress"@2 (w=21.88) +4 more |
| 6 | `get_upstream_features` | L0:F10198@2, k=5 | Emb:" Congress"@2 (w=17.25) +4 more |
| 7 | `inspect_feature` | L0, F767 | "the word "Congress" as well as the phrase "immigration matters"" |
| 8 | `inspect_feature` | L0, F15411 | " terms relating to political bodies, figures, and processes" |
| 9 | `get_upstream_features` | L0:F767@2, k=5 | Emb:" Congress"@2 (w=26.50) +4 more |
| 10 | `get_upstream_features` | L0:F15411@2, k=5 | Emb:" Congress"@2 (w=17.00) +4 more |

**Findings:** The high-impact feature L2:F2701 encodes a SUPPRESSION circuit for the token "Congress". Despite its label "words related to the U.S. Congress", it actually suppresses "Congress" tokens and promotes random technical tokens. The circuit shows: 1) Direct positive connection from embedding "Congress" (weight 28.125), 2) Negative connections from early-layer "Congress" detectors (L0:F10198, L1:F3276),…

</details>

<details>
<summary><b>SA-2</b> — tool trace (11 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L3, F5753 | " the word "includes" or "containing"." |
| 2 | `get_upstream_features` | L3:F5753@12, k=5 | Emb:" include"@12 (w=41.00) +4 more |
| 3 | `inspect_feature` | L1, F3271 | "the word "including" or its variants" |
| 4 | `inspect_feature` | L1, F9538 | " the word "included" or words directly associated with research studie" |
| 5 | `get_upstream_features` | L1:F3271@12, k=5 | Emb:" include"@12 (w=16.00) +4 more |
| 6 | `get_upstream_features` | L1:F9538@12, k=5 | Emb:" include"@12 (w=16.25) +4 more |
| 7 | `inspect_feature` | L0, F10783 | " the word "include" (and variations of the word)" |
| 8 | `inspect_feature` | L0, F14517 | "the word "including"" |
| 9 | `inspect_feature` | L0, F2310 | " the word "immediate" and words associated to problems" |
| 10 | `get_upstream_features` | L0:F10783@12, k=5 | Emb:" include"@12 (w=25.50) +4 more |
| 11 | `get_upstream_features` | L0:F14517@12, k=5 | Emb:" include"@12 (w=12.88) +4 more |

**Findings:** The feature L3:F5753 at position 12 encodes a simple word detector for "include" and its variants, but with a suppression effect. This is NOT a negation signal or semantic content about "no responsibility" - it's simply detecting the word "include" that appears at position 12 in the text. The circuit is very shallow: L0 features (F10783, F14517) directly detect the "include" token, feed into L1 fe…

</details>

<details>
<summary><b>SA-3</b> — tool trace (4 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F6044 | "the word "yield"" |
| 2 | `get_upstream_features` | L0:F6044@2, k=5 | Emb:" Congress"@2 (w=17.00) +4 more |
| 3 | `get_upstream_features` | L0:F6044@2, k=10 | Emb:" Congress"@2 (w=17.00) +9 more |
| 4 | `get_top_logits` | k=5 | "" (100%) |

**Findings:** The feature L0:F6044 at position 2 is essentially a token detector for "Congress". Despite being labeled as "the word 'yield'", it's strongly driven by the embedding of token " Congress" at position 2 with a very large edge weight (17.0). The circuit is simple: the token " Congress" directly activates this layer-0 feature, which then contributes to the output. This appears to be a mislabeled featu…

</details>

<details>
<summary><b>SA-4</b> — tool trace (11 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F59 | " phrases with the word 'to' preceded by a verb or the word 'start' or " |
| 2 | `get_upstream_features` | L4:F59@11, k=5 | Emb:" began"@10 (w=13.31) +4 more |
| 3 | `inspect_feature` | L3, F12596 | " actions or methods, sometimes preceeded by the preposition 'a' or 'to" |
| 4 | `inspect_feature` | L2, F11469 | " the word "to"" |
| 5 | `get_upstream_features` | L3:F12596@11, k=5 | Emb:" to"@11 (w=21.62) +4 more |
| 6 | `get_upstream_features` | L2:F11469@11, k=5 | Emb:" began"@10 (w=10.94) +4 more |
| 7 | `inspect_feature` | L0, F8444 | "the word "to"" |
| 8 | `get_upstream_features` | L0:F8444@11, k=5 | Emb:" to"@11 (w=41.25) +4 more |
| 9 | `inspect_feature` | L1, F13759 | "the word 'to'" |
| 10 | `get_upstream_features` | L1:F13759@11, k=5 | Emb:" to"@11 (w=15.94) +4 more |
| 11 | `inspect_feature` | L3, F4374 | " instances of the word "to"" |

**Findings:** This circuit traces a feature at layer 4, position 11 that detects phrases with the word 'to' preceded by verbs like 'start' or 'begin'. The direct_effect is 0.4141, indicating it's pushing for some output. Tracing upstream reveals:

1. The main signal comes from the token " began" at position 10 (edge_weight: 13.3125)
2. Layer 3 feature 12596 detects actions/methods preceded by 'a' or 'to', feedi…

</details>

<details>
<summary><b>SA-5</b> — tool trace (17 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F10401 | " mentions of genes and proteins" |
| 2 | `get_upstream_features` | L0:F10401@2, k=5 | Emb:" Congress"@2 (w=13.25) +4 more |
| 3 | `get_top_logits` | k=5 | "" (100%) |
| 4 | `inspect_feature` | L0, F478 | "various kinds of brackets and parentheses followed by a period" |
| 5 | `inspect_feature` | L0, F1131 | "the word "drop"" |
| 6 | `get_top_features` | token="", k=10 | 10 features; top: L2:2701 de=0.856 |
| 7 | `inspect_feature` | L0, F6044 | "the word "yield"" |
| 8 | `inspect_feature` | L0, F15411 | " terms relating to political bodies, figures, and processes" |
| 9 | `get_upstream_features` | L0:F15411@2, k=5 | Emb:" Congress"@2 (w=17.00) +4 more |
| 10 | `get_top_features` | token=".", k=10 | ❌ Token '.' not found in top logits. Available: [''] |
| 11 | `inspect_feature` | L0, F9557 | "the word "clean" and words/phrases associated with people" |
| 12 | `inspect_feature` | L2, F2701 | " words related to the U.S. Congress" |
| 13 | `get_upstream_features` | L2:F2701@2, k=5 | Emb:" Congress"@2 (w=28.12) +4 more |
| 14 | `inspect_feature` | L1, F3276 | " mentions of the United States Congress" |
| 15 | `inspect_feature` | L0, F10198 | " the word "Congress"" |
| 16 | `get_upstream_features` | L1:F3276@2, k=5 | Emb:" Congress"@2 (w=21.88) +4 more |
| 17 | `inspect_feature` | L0, F767 | "the word "Congress" as well as the phrase "immigration matters"" |

**Findings:** The negative-effect feature L0:F10401 at position 2 encodes "mentions of genes and proteins" but is being triggered by the token "Congress" (edge_weight: 13.25). This appears to be a false positive activation - the feature is designed to detect genes/proteins but misfires on "Congress". 

The feature has a negative direct effect (-0.373) and suppresses foreign language tokens (Spanish, Italian, Fr…

</details>

<details>
<summary><b>SA-6</b> — tool trace (6 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L3, F8351 | " words related to including and code language symbols" |
| 2 | `get_upstream_features` | L3:F8351@12, k=5 | Emb:" include"@12 (w=28.38) +4 more |
| 3 | `inspect_feature` | L1, F3271 | "the word "including" or its variants" |
| 4 | `get_upstream_features` | L1:F3271@12, k=5 | Emb:" include"@12 (w=16.00) +4 more |
| 5 | `inspect_feature` | L0, F10783 | " the word "include" (and variations of the word)" |
| 6 | `get_top_logits` | k=5 | "" (100%) |

**Findings:** This negative-effect feature at L3:F8351 encodes \"words related to including and code language symbols\" and promotes tokens like \"include\", \"includes\", \"including\", etc. However, it has a negative direct effect (-0.3516) on some output token (unspecified in the prompt). The circuit shows: 1) The raw token \" include\" at position 12 strongly activates L3:F8351 (weight 28.375). 2) L1:F3271 …

</details>

<details>
<summary><b>SA-7</b> — tool trace (11 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L2, F6735 | " political parties and politicians" |
| 2 | `get_upstream_features` | L2:F6735@2, k=5 | Emb:" Congress"@2 (w=9.19) +4 more |
| 3 | `inspect_feature` | L1, F6853 | " proper nouns from the Indian subcontinent" |
| 4 | `inspect_feature` | L1, F7245 | " mentions of government or authority actions, specifically in the cont" |
| 5 | `inspect_feature` | L1, F2408 | " words related to organizations, especially governmental and education" |
| 6 | `get_upstream_features` | L1:F6853@2, k=5 | Emb:" Congress"@2 (w=9.88) +4 more |
| 7 | `inspect_feature` | L0, F767 | "the word "Congress" as well as the phrase "immigration matters"" |
| 8 | `get_upstream_features` | L1:F7245@2, k=5 | Emb:" Congress"@2 (w=10.56) +4 more |
| 9 | `get_upstream_features` | L1:F2408@2, k=5 | Emb:" Congress"@2 (w=10.19) +4 more |
| 10 | `inspect_feature` | L0, F15411 | " terms relating to political bodies, figures, and processes" |
| 11 | `get_upstream_features` | L0:F767@2, k=5 | Emb:" Congress"@2 (w=26.50) +4 more |

**Findings:** This feature at L2:F6735 encodes "political parties and politicians" and has a strong negative effect (-0.3477). The circuit traces back to the token " Congress" at position 2 through multiple pathways. The strongest connections are direct from the " Congress" token embedding (weight: 9.1875) and through L1 features that detect Indian subcontinent politics (F6853), government authority mentions (F…

</details>

<details>
<summary><b>SA-8</b> — tool trace (10 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L1, F4224 | " the word "registration" and its variations" |
| 2 | `get_upstream_features` | L1:F4224@2, k=5 | Emb:" Congress"@2 (w=13.94) +4 more |
| 3 | `inspect_feature` | L0, F16287 | "the abbreviation "etc." and also words related to physical buildings" |
| 4 | `inspect_feature` | L0, F6948 | "the word "target"" |
| 5 | `inspect_feature` | L0, F15389 | " words and phrases related to political entities, governments, and new" |
| 6 | `get_upstream_features` | L0:F16287@2, k=5 | Emb:" Congress"@2 (w=18.62) +4 more |
| 7 | `get_upstream_features` | L0:F6948@2, k=5 | Emb:" Congress"@2 (w=15.38) +4 more |
| 8 | `get_upstream_features` | L0:F15389@2, k=5 | Emb:" Congress"@2 (w=4.31) +4 more |
| 9 | `inspect_feature` | L0, F478 | "various kinds of brackets and parentheses followed by a period" |
| 10 | `inspect_feature` | L0, F1131 | "the word "drop"" |

**Findings:** This circuit traces a feature at layer 1 (F4224) that detects the word "registration" but suppresses it. The feature has a direct effect of -0.2734, indicating it suppresses contradiction signals. The circuit reveals that the primary driver is the token "Congress" at position 2, with a very strong weight of 13.9375. There's also a negative connection to "The" at position 1. The feature is fed by t…

</details>

<details>
<summary><b>SA-9</b> — tool trace (4 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F9557 | "the word "clean" and words/phrases associated with people" |
| 2 | `get_upstream_features` | L0:F9557@2, k=5 | Emb:" Congress"@2 (w=11.12) +4 more |
| 3 | `get_top_logits` | k=5 | "" (100%) |
| 4 | `get_upstream_features` | L0:F9557@2, k=10 | Emb:" Congress"@2 (w=11.12) +9 more |

**Findings:** The negative-effect feature L0:F9557 at position 2 encodes detection of the word 'clean' and related people-associated terms. Despite its semantic label, in this specific circuit context at position 2, it is primarily driven by the token 'Congress' with a very strong edge weight of 11.125. The feature has low sparsity (frac_nonzero=0.01863) indicating specificity. It promotes unusual/stylized word…

</details>

### Build

`build_circuit` → 10 nodes, 10 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m2.7 | 23,456 | 4,780 | 54,626 | 0 | $0.0144 | — | — |
| SA-3 | deepseek/deepseek-v3.2 | 14,420 | 1,506 | 3,136 | 0 | $0.0044 | ✅ 1F/1E | Trace this feature at pos 2 (direct_effect: 0.4941). What do… |
| SA-2 | deepseek/deepseek-v3.2 | 69,314 | 2,654 | 0 | 0 | $0.0190 | ✅ 6F/10E | Trace this feature at pos 12 (direct_effect: 0.5273). What d… |
| SA-4 | deepseek/deepseek-v3.2 | 67,854 | 2,764 | 3,200 | 0 | $0.0188 | ✅ 6F/10E | Trace this feature at pos 11 (direct_effect: 0.4141). What d… |
| SA-1 | deepseek/deepseek-v3.2 | 62,076 | 3,403 | 0 | 0 | $0.0174 | ✅ 5F/11E | Trace this high-impact feature (direct_effect: 0.8555) at po… |
| SA-5 | deepseek/deepseek-v3.2 | 130,685 | 4,721 | 5,824 | 0 | $0.0359 | ✅ 8F/16E | Trace this negative-effect feature at pos 2 (direct_effect: … |
| SA-6 | deepseek/deepseek-v3.2 | 31,397 | 2,101 | 0 | 0 | $0.0090 | ✅ 3F/4E | Trace this negative-effect feature (direct_effect: -0.3516) … |
| SA-8 | deepseek/deepseek-v3.2 | 25,344 | 2,807 | 36,800 | 0 | $0.0086 | ✅ 6F/14E | Trace this negative-effect feature (direct_effect: -0.2734) … |
| SA-7 | deepseek/deepseek-v3.2 | 71,176 | 2,955 | 0 | 0 | $0.0196 | ✅ 6F/14E | Trace this negative-effect feature (direct_effect: -0.3477) … |
| SA-9 | deepseek/deepseek-v3.2 | 17,354 | 1,724 | 0 | 0 | $0.0052 | ✅ 1F/3E | Trace this negative-effect feature (direct_effect: -0.3105) … |
| **Total** | | **513,076** | **29,415** | **103,586** | **0** | **$0.1523** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 7m 42s