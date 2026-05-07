# Circuit Oracle Report
**Date:** 2026-04-06 10:22:54 UTC | **Orchestrator:** minimax/minimax-m2.7 | **Subagent:** deepseek/deepseek-v3.2

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-neg_neg_3 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "('The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession.',)"

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** This probe's classification is driven by a mixed circuit combining narrative/story content features (positive contribution, direct_effect up to +0.1885), male pronoun detection features (negative contribution, direct_effect -0.1621), and a journalism media chain (negative contribution, direct_effect -0.1279). The input describes a journalist who researches stories and represents a country in journalistic circles, and the circuit identifies this profession primarily through word-level detectors for "stories" at position 3 and "journalistic" at position 13, with gender markers (male pronoun "He" at position 1) as a confound signal.

**Confidence:** 7/10

**Reasoning:** The circuit analysis confirms the user's concern about spurious features. The probe relies heavily on the male pronoun "He" (emb_he → L0:F1069, edge_weight=22.625) which fires strongly on this input but encodes gender rather than profession. However, the probe also uses genuine profession indicators: L14:F4420 encodes "words and phrases related to journalism and newspapers" with frac_nonzero=0.0165, and this feature chain (L4→L7→L8→L9→L14 at position 13) processes the word "journalistic" directly from the input. The narrative/story content features (L0:F61, L0:F14906, L1:F14812) also represent legitimate profession-related signals, as journalists research and work with stories. The negative contributions from the journalism chain and grammar markers ("too" at pos 27, "in" at pos 12) suggest these features suppress the probe's classification when detected, indicating the probe may be trained to identify a specific type of content rather than journalism per se. The circuit traces back to token embeddings at all key positions, confirming the signals originate from specific input words rather than spurious internal activations. The male pronoun feature has a low frac_nonzero (0.0078), indicating it only fires on male pronouns, but its negative direct effect suggests it acts as a suppressant for certain output predictions when male-gendered text is detected—raising concerns about reliance on gender markers rather than genuine profession-specific knowledge. This confirms the user's concern about the

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 10 features; top: L0:14906 de=-0.221 |

### Dispatch: 10 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L0:F14906@3` | ✅ reported | 3 | 6 | Trace the path from L0:F14906 at position 3 — identify what this feature encodes… |
| SA-2 | `L1:F14812@3` | ✅ reported | 4 | 8 | Trace the path from L1:F14812 at position 3 — identify what this feature encodes… |
| SA-3 | `L0:F11603@27` | ✅ reported | 1 | 4 | Trace the path from L0:F11603 at position 27 — identify what this feature encode… |
| SA-4 | `L0:F1069@1` | ✅ reported | 4 | 5 | Trace the path from L0:F1069 at position 1 — identify what this feature encodes … |
| SA-5 | `L0:F11261@3` | ✅ reported | 2 | 5 | Trace L0:F11261 at position 3 (direct_effect=0.1602) — identify what this featur… |
| SA-6 | `L0:F8061@12` | ✅ reported | 1 | 5 | Trace L0:F8061 at position 12 (direct_effect=-0.1328) — identify what this featu… |
| SA-7 | `L14:F4420@13` | ✅ reported | 5 | 20 | Trace L14:F4420 at position 13 (direct_effect=-0.1279) — this is a mid-layer fea… |
| SA-8 | `L1:F16233@3` | ✅ reported | 3 | 6 | Trace L1:F16233 at position 3 (direct_effect=0.1279) — identify what this featur… |
| SA-9 | `L0:F2711@20` | ✅ reported | 1 | 5 | Trace L0:F2711 at position 20 (direct_effect=-0.1104) — identify what this featu… |
| SA-10 | `L0:F6962@7` | ✅ reported | 1 | 5 | Trace L0:F6962 at position 7 (direct_effect=0.106) — identify what this feature … |

<details>
<summary><b>SA-1</b> — tool trace (5 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F14906 | " the word "binding"" |
| 2 | `get_upstream_features` | L0:F14906@3, k=5 | Emb:" stories"@3 (w=12.94) +4 more |
| 3 | `inspect_feature` | L0, F310 | " the pronouns "she", "her", and "he" and sometimes the word "therefore" |
| 4 | `get_upstream_features` | L0:F14906@3, k=10 | Emb:" stories"@3 (w=12.94) +9 more |
| 5 | `inspect_feature` | L0, F1288 | " vertical bars used as separators in text" |

**Findings:** Tracing from L0:F14906 at position 3 (direct_effect=-0.2207 on probe classification). This feature is labeled as detecting 'the word \"binding\"' but in this specific circuit at position 3, it's primarily detecting the token \"stories\" with a very strong direct connection from the embedding of \"stories\" at position 3 (edge_weight=12.9375). The feature also receives minor negative input from \"r…

</details>

<details>
<summary><b>SA-2</b> — tool trace (8 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L1, F14812 | " references to stories, chapters, and other narrative elements" |
| 2 | `get_upstream_features` | L1:F14812@3, k=5 | Emb:" stories"@3 (w=18.62) +4 more |
| 3 | `inspect_feature` | L0, F479 | "the word "lift."" |
| 4 | `inspect_feature` | L0, F8316 | " articles that mention the action of counting or strong desires" |
| 5 | `get_upstream_features` | L0:F479@3, k=5 | Emb:" stories"@3 (w=10.69) +4 more |
| 6 | `get_upstream_features` | L0:F8316@3, k=5 | Emb:" stories"@3 (w=10.44) +4 more |
| 7 | `inspect_feature` | L0, F61 | "the word "stories" sometimes along with apostrophes and common names." |
| 8 | `get_upstream_features` | L0:F61@3, k=5 | Emb:" stories"@3 (w=17.38) +4 more |

**Findings:** The circuit traces from L1:F14812 (which encodes references to stories/narrative elements) back to the input token "stories" at position 3. The feature has direct_effect=0.1885 and shows an interesting pattern: while the direct embedding connection from "stories" strongly activates it (18.625 weight), the layer 0 feature that specifically detects the word "stories" (F61) actually inhibits it (-0.4…

</details>

<details>
<summary><b>SA-3</b> — tool trace (3 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F11603 | " the word "too"" |
| 2 | `get_upstream_features` | L0:F11603@27, k=5 | Emb:" too"@27 (w=32.00) +4 more |
| 3 | `get_upstream_features` | L0:F11603@27, k=10 | Emb:" too"@27 (w=32.00) +9 more |

**Findings:** The starting feature L0:F11603 encodes detection of the word \"too\". It has a direct effect of -0.1631, meaning it suppresses the target output. Tracing upstream reveals it directly connects to token embeddings, with the strongest connection (weight 32.0) coming from the \" too\" token at position 27 itself. This indicates it's a simple token-detection feature that fires when the specific token \…

</details>

<details>
<summary><b>SA-4</b> — tool trace (5 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F1069 | " references to a male person, particularly when using the pronoun "He"" |
| 2 | `get_upstream_features` | L0:F1069@1, k=5 | Emb:"He"@1 (w=22.62) +4 more |
| 3 | `inspect_feature` | L0, F310 | " the pronouns "she", "her", and "he" and sometimes the word "therefore" |
| 4 | `inspect_feature` | L0, F355 | " text related to numbers, especially those representing currency or me" |
| 5 | `inspect_feature` | L0, F96 | "sentences beginning with coordinating conjunctions like "but" and "and" |

**Findings:** The circuit traces back to token embeddings. L0:F1069 is an early-layer feature that detects male pronouns (particularly "He" and "His"). It receives strong direct input from the token embedding "He" at position 1 (weight=22.625) and from the beginning-of-sequence token "<bos>" at position 0 (weight=6.9375). The feature has a negative direct_effect (-0.1621) on the output token, indicating it supp…

</details>

<details>
<summary><b>SA-5</b> — tool trace (4 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F11261 | " the word "migration" and words related to it" |
| 2 | `get_upstream_features` | L0:F11261@3, k=5 | Emb:" stories"@3 (w=12.69) +4 more |
| 3 | `inspect_feature` | L0, F310 | " the pronouns "she", "her", and "he" and sometimes the word "therefore" |
| 4 | `get_top_logits` | k=5 | "" (100%) |

**Findings:** The tracing reveals that L0:F11261 (detecting \"migration\" words) at position 3 is primarily driven directly by the token \" stories\" itself through its embedding (weight=12.6875), with minor contributions from other tokens. This suggests the feature might be mis-firing on \" stories\" or there's some association between \" stories\" and \"migration\" concepts in the training data. The feature h…

</details>

<details>
<summary><b>SA-6</b> — tool trace (2 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F8061 | " the preposition "in"" |
| 2 | `get_upstream_features` | L0:F8061@12, k=5 | Emb:" in"@12 (w=39.75) +4 more |

**Findings:** The feature L0:F8061 at position 12 encodes detection of the preposition \"in\" at that position. It has a direct_effect of -0.1328, meaning it suppresses the target output. Tracing upstream reveals this feature is primarily driven by the token embedding of \" in\" at position 12 itself with a very strong edge weight of 39.75, confirming it's essentially an \"in\"-detector. Other tokens like \"cou…

</details>

<details>
<summary><b>SA-7</b> — tool trace (10 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L14, F4420 | "words and phrases related to journalism and newspapers" |
| 2 | `get_upstream_features` | L14:F4420@13, k=5 | Emb:" journalistic"@13 (w=24.38) +4 more |
| 3 | `inspect_feature` | L4, F13253 | " things related to journalism and the media" |
| 4 | `inspect_feature` | L7, F9092 | " words and phrases associated with broadcast journalism" |
| 5 | `get_upstream_features` | L4:F13253@13, k=5 | Emb:" journalistic"@13 (w=25.62) +4 more |
| 6 | `get_upstream_features` | L7:F9092@13, k=5 | Emb:" journalistic"@13 (w=14.88) +4 more |
| 7 | `inspect_feature` | L9, F7435 | " words and phrases related to news production and media" |
| 8 | `get_upstream_features` | L9:F7435@13, k=5 | Emb:" journalistic"@13 (w=4.66) +4 more |
| 9 | `inspect_feature` | L8, F8437 | "content related to film festivals and production, particularly documen" |
| 10 | `get_upstream_features` | L8:F8437@13, k=5 | Emb:" journalistic"@13 (w=8.06) +4 more |

**Findings:** The circuit traces L14:F4420 at position 13, which encodes "words and phrases related to journalism and newspapers". The primary driver is the input token " journalistic" at position 13, which has strong direct connections to multiple features in the circuit. The token embedding " journalistic" connects most strongly to L4:F13253 (journalism/media concepts) and L14:F4420 directly, creating a focus…

</details>

<details>
<summary><b>SA-8</b> — tool trace (6 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L1, F16233 | "the word "tips" and the word "unit"" |
| 2 | `get_upstream_features` | L1:F16233@3, k=5 | Emb:" stories"@3 (w=13.69) +4 more |
| 3 | `inspect_feature` | L0, F1301 | " mentions of cancer and related terms like tumors" |
| 4 | `inspect_feature` | L0, F8073 | "references to a "trick" and possibly the people involved in performing" |
| 5 | `get_upstream_features` | L0:F1301@3, k=5 | Emb:" stories"@3 (w=12.25) +4 more |
| 6 | `get_upstream_features` | L0:F8073@3, k=5 | Emb:" stories"@3 (w=13.00) +4 more |

**Findings:** The circuit tracing reveals that L1:F16233 at position 3 (encoding "the word 'tips' and the word 'unit'") is primarily driven by the input token " stories" at position 3 through a very strong direct connection (edge_weight=13.6875). The feature also receives excitatory input from L0:F1301 (cancer-related terms) and inhibitory input from L0:F8073 ("trick" references), both of which themselves are s…

</details>

<details>
<summary><b>SA-9</b> — tool trace (4 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F2711 | "the word "foreign."" |
| 2 | `get_upstream_features` | L0:F2711@20, k=5 | Emb:" foreign"@20 (w=25.75) +4 more |
| 3 | `get_top_logits` | k=5 | "" (100%) |
| 4 | `get_top_features` | token="", k=10 | 10 features; top: L0:14906 de=-0.221 |

**Findings:** L0:F2711 at position 20 is a word detector feature for the token "foreign" (label: "the word 'foreign.'"). It has a direct effect of -0.1104 on the empty string output token, meaning it pushes against empty string predictions.

Tracing upstream shows it's primarily fed directly by the token embedding for "foreign" at position 20 with a strong edge weight of 25.75, confirming it's a direct word det…

</details>

<details>
<summary><b>SA-10</b> — tool trace (3 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F6962 | "the token "env" possibly in code snippets" |
| 2 | `get_upstream_features` | L0:F6962@7, k=5 | Emb:" same"@7 (w=14.81) +4 more |
| 3 | `get_top_logits` | k=5 | "" (100%) |

**Findings:** L0:F6962 at position 7 encodes detection of the token \"env\" (likely in code/technical contexts), but in this specific input sequence, it is primarily triggered by the token \"same\" at position 7 with a strong positive edge weight (14.8125). The feature has low sparsity (frac_nonzero=0.02635), indicating it's specific and selective. Interestingly, it promotes general formatting tokens like space…

</details>

### Build

`build_circuit` → 12 nodes, 12 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m2.7 | 24,877 | 4,633 | 38,503 | 0 | $0.0142 | — | — |
| SA-3 | deepseek/deepseek-v3.2 | 12,922 | 1,070 | 0 | 0 | $0.0038 | ✅ 1F/4E | Trace the path from L0:F11603 at position 27 — identify what… |
| SA-1 | deepseek/deepseek-v3.2 | 25,129 | 1,994 | 0 | 0 | $0.0073 | ✅ 3F/6E | Trace the path from L0:F14906 at position 3 — identify what … |
| SA-4 | deepseek/deepseek-v3.2 | 25,327 | 1,992 | 0 | 0 | $0.0073 | ✅ 4F/5E | Trace the path from L0:F1069 at position 1 — identify what t… |
| SA-2 | deepseek/deepseek-v3.2 | 45,585 | 2,621 | 0 | 0 | $0.0128 | ✅ 4F/8E | Trace the path from L1:F14812 at position 3 — identify what … |
| SA-6 | deepseek/deepseek-v3.2 | 9,111 | 1,358 | 0 | 0 | $0.0029 | ✅ 1F/5E | Trace L0:F8061 at position 12 (direct_effect=-0.1328) — iden… |
| SA-5 | deepseek/deepseek-v3.2 | 17,989 | 1,446 | 0 | 0 | $0.0052 | ✅ 2F/5E | Trace L0:F11261 at position 3 (direct_effect=0.1602) — ident… |
| SA-8 | deepseek/deepseek-v3.2 | 29,674 | 1,858 | 0 | 0 | $0.0084 | ✅ 3F/6E | Trace L1:F16233 at position 3 (direct_effect=0.1279) — ident… |
| SA-7 | deepseek/deepseek-v3.2 | 50,511 | 3,254 | 10,432 | 0 | $0.0146 | ✅ 5F/20E | Trace L14:F4420 at position 13 (direct_effect=-0.1279) — thi… |
| SA-10 | deepseek/deepseek-v3.2 | 13,281 | 1,229 | 0 | 0 | $0.0039 | ✅ 1F/5E | Trace L0:F6962 at position 7 (direct_effect=0.106) — identif… |
| SA-9 | deepseek/deepseek-v3.2 | 17,877 | 1,903 | 0 | 0 | $0.0054 | ✅ 1F/5E | Trace L0:F2711 at position 20 (direct_effect=-0.1104) — iden… |
| **Total** | | **272,283** | **23,358** | **48,935** | **0** | **$0.0859** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 6m 20s