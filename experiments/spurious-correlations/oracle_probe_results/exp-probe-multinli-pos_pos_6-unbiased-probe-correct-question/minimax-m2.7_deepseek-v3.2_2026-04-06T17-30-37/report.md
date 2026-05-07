# Circuit Oracle Report
**Date:** 2026-04-06 17:30:37 UTC | **Orchestrator:** minimax/minimax-m2.7 | **Subagent:** deepseek/deepseek-v3.2

## Input

**Prompt:** "Dataset: multinli-pos_pos_6 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "('The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction.',)"

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** This probe's classification score is driven by a shallow circuit that primarily detects specific lexical content ("they", "about", "land", "to") and stylistic/register features (transitional words, code documentation patterns) rather than semantic relationships or negation signals. The circuit does NOT rely on negation word signals as the user suspected.

**Confidence:** 8/10

**Reasoning:** The circuit analysis reveals:

1. **No negation signals**: The top 10 features contain no features specifically detecting negation words ("not", "no", "never"). The concern about spurious negation features is **not validated** for this specific input.

2. **Shallow content detection**: The strongest features (L0:F3498 with direct_effect=-0.6172 for "they", L0:F2238 with -0.3438 for "about" followed by numbers) are direct token detectors reading from embeddings at very early layers. These are **legitimate content features** detecting specific words in the input.

3. **Spurious stylistic features detected**: The concern IS partially valid for different reasons:
   - `transitional_so` (L4:F12225, direct_effect=+0.2773) detects transitional words like "So", "therefore", "hence" - this is a register/stylistic marker not directly tied to the semantic content about deforestation
   - `code_documentation` (L8:F8406, direct_effect=-0.2432) detects "I" and "Exactly" but is driven by code documentation patterns (frac_nonzero=0.00863) and heavily influenced by `<bos>` token (edge_weight=10.25), suggesting this is a spurious artifact

4. **Content features are legitimate**: Features like `land_scientific` (L2:F11518, +0.252) detecting "land" in agricultural contexts and `land_basic` (L1:F461, +0.1816) directly detect relevant content from the prompt about clearing land for agriculture.

5. **Circuit depth**: Most signals flow directly from token embeddings through single transformer layers, indicating a shallow circuit that reads specific words rather than building complex semantic representations.

The probe appears to use a mix of genuine content detection and potentially spurious stylistic/register features, but **not negation-based spurious signals** on this particular input.

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 10 features; top: L0:3498 de=-0.617 |

### Dispatch: 10 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L0:F3498@2` | ✅ reported | 3 | 3 | Trace L0:F3498 to understand what this feature encodes and how it relates to the… |
| SA-2 | `L0:F2238@4` | ✅ reported | 1 | 1 | Trace L0:F2238 to understand what this feature encodes and how it relates to the… |
| SA-3 | `L4:F12225@2` | ✅ reported | 8 | 8 | Trace L4:F12225 to understand what this feature encodes and how it relates to th… |
| SA-4 | `L2:F11518@7` | ✅ reported | 4 | 6 | Trace L2:F11518 to understand what this feature encodes and how it relates to th… |
| SA-5 | `L4:F5450@4` | ✅ reported | 5 | 8 | Trace L4:F5450 to understand what this feature encodes and how it relates to the… |
| SA-6 | `L2:F15312@4` | ✅ reported | 3 | 11 | Trace L2:F15312 to understand what this feature encodes and how it relates to th… |
| SA-7 | `L3:F4464@4` | ✅ reported | 5 | 6 | Trace L3:F4464 to understand what this feature encodes and how it relates to the… |
| SA-8 | `L8:F8406@1` | ✅ reported | 8 | 17 | Trace L8:F8406 to understand what this feature encodes and how it relates to the… |
| SA-9 | `L0:F8444@13` | ✅ reported | 1 | 3 | Trace L0:F8444 to understand what this feature encodes and how it relates to the… |
| SA-10 | `L1:F461@7` | ✅ reported | 2 | 7 | Trace L1:F461 to understand what this feature encodes - it's about detecting "la… |

<details>
<summary><b>SA-1</b> — tool trace (4 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F3498 | " the pronoun "they" or its possessive form." |
| 2 | `get_upstream_features` | L0:F3498@2, k=5 | Emb:" they"@2 (w=42.75) +4 more |
| 3 | `inspect_feature` | L0, F517 | "words starting with "ab" followed by another letter" |
| 4 | `inspect_feature` | L0, F1216 | " proper nouns, especially locations or people's names" |

**Findings:** The feature L0:F3498 at position 2 is a simple pronoun detection feature for the word \"they\". It has a direct, strong connection (edge_weight=42.75) from the embedding of \" they\" at the same position 2. The feature suppresses the token \"they\" itself (it's in the suppressed_tokens list) and promotes various other tokens like space, \"She\", \"us\", etc. The two other upstream features (L0:F51…

</details>

<details>
<summary><b>SA-2</b> — tool trace (2 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F2238 | " the word "about" when followed by a numerical value" |
| 2 | `get_upstream_features` | L0:F2238@4, k=5 | Emb:" about"@4 (w=35.00) +4 more |

**Findings:** Tracing L0:F2238 at position 4 reveals it encodes detection of the word \"about\" when followed by a numerical value. The feature gets its primary signal directly from the \" about\" token embedding at position 4 with a strong edge weight of 35.0. This is a very shallow circuit that essentially reads the word \"about\" from the input and promotes tokens like newlines, parentheses, and numbers, whi…

</details>

<details>
<summary><b>SA-3</b> — tool trace (13 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F12225 | " transitional conclusion words, often used in legal or academic writin" |
| 2 | `get_upstream_features` | L4:F12225@2, k=5 | Emb:" they"@2 (w=12.81) +4 more |
| 3 | `inspect_feature` | L2, F14822 | " the abbreviation "SO" followed by other characters" |
| 4 | `inspect_feature` | L3, F11720 | "the word "that", often preceded and followed by specific words" |
| 5 | `inspect_feature` | L0, F3498 | " the pronoun "they" or its possessive form." |
| 6 | `get_upstream_features` | L2:F14822@1, k=5 | Emb:"So"@1 (w=19.62) +4 more |
| 7 | `get_upstream_features` | L3:F11720@2, k=5 | Emb:"So"@1 (w=11.06) +4 more |
| 8 | `get_upstream_features` | L0:F3498@2, k=5 | Emb:" they"@2 (w=42.75) +4 more |
| 9 | `inspect_feature` | L2, F8586 | " words related to decision making, reasons for actions, feelings, and " |
| 10 | `inspect_feature` | L1, F11695 | " socket programming code" |
| 11 | `inspect_feature` | L1, F11827 | " the word "cache" and associated terms related to data buffering" |
| 12 | `inspect_feature` | L2, F11678 | "the letters SO in programming code" |
| 13 | `get_upstream_features` | L1:F11695@1, k=5 | Emb:"So"@1 (w=15.94) +4 more |

**Findings:** The circuit traces show that L4:F12225 encodes transitional conclusion words like "So", "hence", "therefore" often used in legal or academic writing. It receives strong direct input from token embeddings "they" (position 2) and "So" (position 1), suggesting it responds to sequences starting with "So" followed by "they". 

The circuit reveals an interesting branching pattern: 
1. L2:F14822 (detecti…

</details>

<details>
<summary><b>SA-4</b> — tool trace (7 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L2, F11518 | " the word "land" in scientific/agricultural contexts" |
| 2 | `get_upstream_features` | L2:F11518@7, k=5 | Emb:" land"@7 (w=28.50) +4 more |
| 3 | `inspect_feature` | L1, F461 | " the word "land"" |
| 4 | `inspect_feature` | L1, F12920 | " the word "land" and related terms like "farmland" and "acreage."" |
| 5 | `get_upstream_features` | L1:F461@7, k=5 | Emb:" land"@7 (w=24.88) +4 more |
| 6 | `get_upstream_features` | L1:F12920@7, k=5 | Emb:" land"@7 (w=21.12) +4 more |
| 7 | `inspect_feature` | L0, F2189 | " technical writing related to scientific studies" |

**Findings:** The circuit shows L2:F11518 detects "land" in scientific/agricultural contexts but surprisingly suppresses the word "land" in its output. The strongest connection is directly from the token embedding " land" at position 7 (weight=28.5). Two L1 features that detect "land" (F461 and F12920) provide inhibitory signals to L2:F11518 (weights -0.75 and -0.7383). These L1 features are themselves primaril…

</details>

<details>
<summary><b>SA-5</b> — tool trace (10 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F5450 | " code snippets from different languages and words related to starting " |
| 2 | `get_upstream_features` | L4:F5450@4, k=5 | Emb:" set"@3 (w=3.31) +4 more |
| 3 | `inspect_feature` | L2, F15312 | " the word "about."" |
| 4 | `inspect_feature` | L3, F8733 | " parts of words like "ch", "parms", "ened", and "ounesto"" |
| 5 | `get_upstream_features` | L2:F15312@4, k=5 | Emb:" about"@4 (w=13.69) +4 more |
| 6 | `get_upstream_features` | L3:F8733@4, k=5 | Emb:" set"@3 (w=7.16) +4 more |
| 7 | `inspect_feature` | L0, F2238 | " the word "about" when followed by a numerical value" |
| 8 | `inspect_feature` | L1, F12223 | "prepositions and words related to directions and locations" |
| 9 | `get_upstream_features` | L0:F2238@4, k=5 | Emb:" about"@4 (w=35.00) +4 more |
| 10 | `get_upstream_features` | L1:F12223@4, k=5 | Emb:" set"@3 (w=6.06) +4 more |

**Findings:** The circuit for L4:F5450 reveals that this feature encodes "code snippets from different languages and words related to starting or beginning something." The feature is primarily driven by two key input tokens: " set" at position 3 and " about" at position 4, with strong direct connections from the token embeddings (edge weights 3.3125 and 2.3594 respectively).

The upstream analysis shows:
1. Str…

</details>

<details>
<summary><b>SA-6</b> — tool trace (6 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L2, F15312 | " the word "about."" |
| 2 | `get_upstream_features` | L2:F15312@4, k=5 | Emb:" about"@4 (w=13.69) +4 more |
| 3 | `inspect_feature` | L0, F2238 | " the word "about" when followed by a numerical value" |
| 4 | `inspect_feature` | L1, F12223 | "prepositions and words related to directions and locations" |
| 5 | `get_upstream_features` | L0:F2238@4, k=5 | Emb:" about"@4 (w=35.00) +4 more |
| 6 | `get_upstream_features` | L1:F12223@4, k=5 | Emb:" set"@3 (w=6.06) +4 more |

**Findings:** The tracing reveals that L2:F15312 at position 4 is a feature that detects the word "about." The circuit shows it's primarily driven directly by the token embeddings for "about" (pos 4) and "set" (pos 3), with strong positive weights. Interestingly, there are inhibitory connections from L0:F2238 (which detects "about" when followed by numerical values) and L1:F12223 (prepositions/directions/locati…

</details>

<details>
<summary><b>SA-7</b> — tool trace (10 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L3, F4464 | " the word "about"" |
| 2 | `get_upstream_features` | L3:F4464@4, k=5 | Emb:" set"@3 (w=10.19) +4 more |
| 3 | `inspect_feature` | L2, F15312 | " the word "about."" |
| 4 | `inspect_feature` | L2, F2952 | " the word "out", and sometimes activates on words relating to legal ca" |
| 5 | `get_upstream_features` | L2:F15312@4, k=5 | Emb:" about"@4 (w=13.69) +4 more |
| 6 | `get_upstream_features` | L2:F2952@4, k=5 | Emb:" set"@3 (w=13.50) +4 more |
| 7 | `inspect_feature` | L0, F2238 | " the word "about" when followed by a numerical value" |
| 8 | `get_upstream_features` | L0:F2238@4, k=5 | Emb:" about"@4 (w=35.00) +4 more |
| 9 | `inspect_feature` | L2, F4531 | " words and phrases related to legal, technical, or scientific document" |
| 10 | `get_upstream_features` | L2:F4531@4, k=5 | Emb:" set"@3 (w=13.75) +4 more |

**Findings:** The circuit analysis reveals that L3:F4464 encodes the word "about" at position 4. This feature receives strong direct connections from token embeddings: "set" (pos 3, weight 10.19) and "about" (pos 4, weight 8.81). 

The main upstream features are from layer 2: L2:F15312 (detects "about.") and L2:F2952 (detects "out" and legal cases). These both connect positively to L3:F4464. L2:F4531 (technical…

</details>

<details>
<summary><b>SA-8</b> — tool trace (14 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L8, F8406 | "the first-person pronoun "I" and the word "Exactly"" |
| 2 | `get_upstream_features` | L8:F8406@1, k=5 | Emb:"<bos>"@0 (w=10.25) +4 more |
| 3 | `inspect_feature` | L7, F462 | " code documentation and import statements" |
| 4 | `inspect_feature` | L7, F5741 | " code documentation or copyright information" |
| 5 | `inspect_feature` | L5, F3992 | "the start of documentation blocks in code" |
| 6 | `get_upstream_features` | L7:F462@1, k=5 | Emb:"<bos>"@0 (w=20.00) +4 more |
| 7 | `get_upstream_features` | L5:F3992@1, k=5 | Emb:"<bos>"@0 (w=20.75) +4 more |
| 8 | `get_upstream_features` | L7:F5741@1, k=5 | Emb:"<bos>"@0 (w=11.88) +4 more |
| 9 | `inspect_feature` | L4, F9757 | "various acronyms, IDs, and symbols, possibly related to scientific dat" |
| 10 | `inspect_feature` | L6, F4516 | " the letter "i."" |
| 11 | `get_upstream_features` | L6:F4516@1, k=5 | L5:F3992 (w=6.88) +4 more |
| 12 | `inspect_feature` | L5, F7489 | " the last three letters of words." |
| 13 | `get_upstream_features` | L4:F9757@1, k=5 | Emb:"<bos>"@0 (w=13.94) +4 more |
| 14 | `inspect_feature` | L0, F7344 | " content markers like figures and section headers" |

**Findings:** The circuit tracing reveals that L8:F8406 (detecting first-person pronoun "I" and the word "Exactly") is primarily driven by a pathway that originates from the bos>` token and code documentation patterns. Key findings:

1. **Strong bos>` influence**: The bos>` token at position 0 has the strongest influence throughout the circuit, feeding directly into L8:F8406 (10.25), L7:F462 (20.0), L7:F5741 (1…

</details>

<details>
<summary><b>SA-9</b> — tool trace (2 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F8444 | "the word "to"" |
| 2 | `get_upstream_features` | L0:F8444@13, k=5 | Emb:" to"@13 (w=41.00) +4 more |

**Findings:** L0:F8444 is a feature that detects the word \"to\" (token \" to\"). The feature has low sparsity (frac_nonzero=0.017) and promotes unusual tokens containing archaic \"\u017f\" characters, suggesting it detects \"to\" in stylized or historical text contexts. The circuit tracing shows it's directly driven by the embedding of \" to\" at position 13 (strong edge_weight=41.0), with weaker support from …

</details>

<details>
<summary><b>SA-10</b> — tool trace (4 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L1, F461 | " the word "land"" |
| 2 | `get_upstream_features` | L1:F461@7, k=5 | Emb:" land"@7 (w=24.88) +4 more |
| 3 | `inspect_feature` | L0, F2189 | " technical writing related to scientific studies" |
| 4 | `get_upstream_features` | L0:F2189@7, k=5 | Emb:"<bos>"@0 (w=5.06) +4 more |

**Findings:** The circuit tracing reveals that L1:F461 primarily detects the word "land" at position 7 through a direct connection from the embedding token " land" at the same position (edge_weight 24.875). This is a very simple and strong connection. The feature has low sparsity (frac_nonzero 0.00685), indicating it's specific to detecting "land". Interestingly, the feature suppresses the token "land" in its o…

</details>

### Build

`build_circuit` → 19 nodes, 23 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m2.7 | 28,677 | 4,329 | 39,399 | 0 | $0.0150 | — | — |
| SA-2 | deepseek/deepseek-v3.2 | 8,866 | 745 | 0 | 0 | $0.0026 | ✅ 1F/1E | Trace L0:F2238 to understand what this feature encodes and h… |
| SA-1 | deepseek/deepseek-v3.2 | 18,823 | 1,441 | 0 | 0 | $0.0054 | ✅ 3F/3E | Trace L0:F3498 to understand what this feature encodes and h… |
| SA-4 | deepseek/deepseek-v3.2 | 36,730 | 1,872 | 0 | 0 | $0.0103 | ✅ 4F/6E | Trace L2:F11518 to understand what this feature encodes and … |
| SA-3 | deepseek/deepseek-v3.2 | 76,024 | 3,017 | 27,072 | 0 | $0.0216 | ✅ 8F/8E | Trace L4:F12225 to understand what this feature encodes and … |
| SA-6 | deepseek/deepseek-v3.2 | 29,124 | 1,885 | 0 | 0 | $0.0083 | ✅ 3F/11E | Trace L2:F15312 to understand what this feature encodes and … |
| SA-7 | deepseek/deepseek-v3.2 | 59,097 | 2,287 | 0 | 0 | $0.0162 | ✅ 5F/6E | Trace L3:F4464 to understand what this feature encodes and h… |
| SA-5 | deepseek/deepseek-v3.2 | 46,791 | 2,468 | 15,040 | 0 | $0.0135 | ✅ 5F/8E | Trace L4:F5450 to understand what this feature encodes and h… |
| SA-8 | deepseek/deepseek-v3.2 | 104,792 | 4,183 | 0 | 0 | $0.0288 | ✅ 8F/17E | Trace L8:F8406 to understand what this feature encodes and h… |
| SA-9 | deepseek/deepseek-v3.2 | 9,159 | 1,212 | 0 | 0 | $0.0028 | ✅ 1F/3E | Trace L0:F8444 to understand what this feature encodes and h… |
| SA-10 | deepseek/deepseek-v3.2 | 18,515 | 1,987 | 0 | 0 | $0.0056 | ✅ 2F/7E | Trace L1:F461 to understand what this feature encodes - it's… |
| **Total** | | **436,598** | **25,426** | **81,511** | **0** | **$0.1302** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 7m 24s