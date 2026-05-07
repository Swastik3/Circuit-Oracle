# Circuit Oracle Report
**Date:** 2026-04-03 10:45:15 UTC | **Orchestrator:** minimax/minimax-m2.7 | **Subagent:** deepseek/deepseek-v3.2

## Input
**Prompt:** "Dataset: multinli-pos_pos_2 | Probe: biased | Method: correct"
**System prompt:** ""
**Question:** "('The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction.',)"
**Top predictions:**  (100.0%)

## Oracle Analysis
**Analysis:** The probe's classification score is driven by a MIXTURE of spurious lexical/pattern-matching features and actual semantic content from the prompt. The circuit contains 5 spurious features (including a negation pattern detector for "haven't") and 5 semantic features encoding actual prompt content like sports tournament context.

**Confidence:** 8/10

**Reasoning:**

The circuit analysis reveals the user's concern is **PARTIALLY VALIDATED**:

**Spurious Features (5 nodes):**
1. **L0:F6236 (pos 37)** - "Negation Pattern (haven't)" - This is the most concerning feature. It detects the letter "t" following the contraction pattern "haven't" and directly promotes negation tokens like "not", "Not", "NOT". With direct_effect=+0.5312, it **positively drives the probe's classification score**. The circuit traces show it receives strong input from embeddings of "t" (18.25), "haven" (16.75), and "'" (11.875). This is a **genuine negation signal** that could be exploited for contradiction detection.

2. **L0:F8352 (pos 2)** - "Lexical 'well' Detection" - Simple word detector with no deeper semantic content. Strong direct embedding connection (30.875).

3. **L0:F3820 (pos 3)** - "Lexical 'the' Detection" - Direct token detection with highest embedding weight (33.0).

4. **L0:F4541 (pos 1)** - "Affirmation Adverb Pattern" - Fires on "yeah" as if it were an adverb of certainty.

5. **L0:F10780 (pos 6)** - "Polysemous 'double'" - Misinterprets "double" as LaTeX commands.

**Semantic Features (5 nodes):**
1. **L4:F9602 (pos 4)** - "Filler Word Detection" - Encodes the conversational filler "uh" semantically.
2. **L4:F12126 (pos 2)** - "Agreement Expressions" - Encodes "well" and "yeah" as conversational agreement markers.
3. **L2:F5201 (pos 8)** - "Sports Tournament Context" - Detects "tournament" and builds context for sports awards/accomplishments.
4. **L0:F16366 (pos 25)** - "Causal Connector" - Detects "because" with strong embedding weight (40.75).
5. **L1:F177 (pos 6)** - "'double' in NC Double A" - Contextualizes "double" as part of the organization name.

**Conclusion:** The user's concern is justified regarding **L0:F6236** - it directly encodes a negation pattern ("haven't") and promotes negation tokens, which could be used as a shortcut for contradiction detection. However, the majority of the circuit (5 of 10 features) does encode actual prompt content related to the sports tournament topic. The probe appears to use both spurious patterns and semantic content, with negation signals being a notable but not dominant component.

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L4:9602 de=-0.625 |

### Dispatch: 10 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L4:F9602@4` | ✅ reported | 7 | 19 | Trace L4:F9602 at pos 4 upstream to identify its semantic content and whether it… |
| SA-2 | `L0:F8352@2` | ✅ reported | 3 | 3 | Trace L0:F8352 at pos 2 upstream to identify what semantic content it encodes. C… |
| SA-3 | `L0:F6236@37` | ✅ reported | 1 | 3 | Trace L0:F6236 at pos 37 upstream to identify what semantic content it encodes. … |
| SA-4 | `L4:F12126@2` | ✅ reported | 11 | 12 | Trace L4:F12126 at pos 2 upstream to identify its semantic content. Is this enco… |
| SA-5 | `L0:F3820@3` | ✅ reported | 5 | 8 | Trace L0:F3820 at pos 3 upstream. Identify if this encodes spurious patterns lik… |
| SA-6 | `L0:F16366@25` | ✅ reported | 1 | 4 | Trace L0:F16366 at pos 25 upstream. Identify if this encodes spurious negation p… |
| SA-7 | `L2:F5201@8` | ✅ reported | 4 | 15 | Trace L2:F5201 at pos 8 upstream. Check if this is encoding spurious negation or… |
| SA-8 | `L1:F177@6` | ✅ reported | 4 | 19 | Trace L1:F177 at pos 6 upstream. Determine if this encodes negation signals or a… |
| SA-9 | `L0:F4541@1` | ✅ reported | 1 | 2 | Trace L0:F4541 at pos 1 upstream. Determine if this is spurious or semantic. |
| SA-10 | `L0:F10780@6` | ✅ reported | 1 | 5 | Trace L0:F10780 at pos 6 upstream. Is this spurious negation or actual content? |

<details>
<summary><b>SA-1</b> — tool trace (12 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F9602 | " interjections and filler words" |
| 2 | `get_upstream_features` | L4:F9602@4, k=5 | Emb:" uh"@4 (w=11.44) +4 more |
| 3 | `inspect_feature` | L2, F9629 | " interjections and sounds of hesitation or acknowledgment" |
| 4 | `inspect_feature` | L2, F752 | "phrases expressing personal opinions or viewpoints, often using words " |
| 5 | `inspect_feature` | L3, F7140 | "words or parts of words containing "man", "ent", "per", or "mate"" |
| 6 | `get_upstream_features` | L2:F9629@4, k=5 | Emb:" uh"@4 (w=15.12) +4 more |
| 7 | `inspect_feature` | L1, F2623 | " words in the context of someone talking or expressing opinions." |
| 8 | `get_upstream_features` | L2:F752@4, k=5 | Emb:" uh"@4 (w=10.38) +4 more |
| 9 | `get_upstream_features` | L3:F7140@4, k=5 | Emb:" uh"@4 (w=10.62) +4 more |
| 10 | `get_upstream_features` | L1:F2623@4, k=5 | Emb:" uh"@4 (w=12.31) +4 more |
| 11 | `inspect_feature` | L0, F16195 | " expressions of gratitude and positive encouragement" |
| 12 | `inspect_feature` | L1, F11932 | " strings of repeated characters, which could be either excitement or c" |

**Findings:** The tracing reveals that L4:F9602 at position 4 encodes "interjections and filler words" and is primarily driven by the input token " uh" at position 4, which is a classic filler word. The circuit shows:

1. Strong direct connections from the embedding token " uh" to multiple layers (L1, L2, L3, L4) with high edge weights (10.375-15.125).

2. The feature hierarchy builds from: 
   - Layer 1: Featu…

</details>

<details>
<summary><b>SA-2</b> — tool trace (5 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F8352 | " the word "well"" |
| 2 | `get_upstream_features` | L0:F8352@2, k=5 | Emb:" well"@2 (w=30.88) +4 more |
| 3 | `inspect_feature` | L0, F317 | "words that can be used as exclamations or excitement, or words used on" |
| 4 | `inspect_feature` | L0, F350 | "words related to both spatial height and also the height of something " |
| 5 | `get_upstream_features` | L0:F8352@2, k=10 | Emb:" well"@2 (w=30.88) +9 more |

**Findings:** Tracing L0:F8352 at position 2 reveals it's a simple lexical detector for the word "well". The feature receives direct input from the embedding of token " well" at the same position (pos 2) with a very strong weight of 30.875, plus minor influences from previous tokens "yeah" (pos 1, weight 3.1875) and "<bos>" (pos 0, weight 0.4355). All transcoder features at layer 0 that connect to it have edge …

</details>

<details>
<summary><b>SA-3</b> — tool trace (4 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F6236 | "the letter "t" when it follows the word "isn'" or "doesn'"" |
| 2 | `get_upstream_features` | L0:F6236@37, k=5 | Emb:"t"@37 (w=18.25) +4 more |
| 3 | `get_upstream_features` | L0:F6236@37, k=10 | Emb:"t"@37 (w=18.25) +9 more |
| 4 | `get_top_logits` | k=5 | "" (100%) |

**Findings:** L0:F6236 at position 37 is a spurious lexical pattern feature that detects the letter \"t\" following contraction patterns like \"haven't\" (haven + ' + t). It has low frac_nonzero (0.00258) indicating high specificity but for lexical rather than semantic content. The feature promotes negation tokens like \"not\", \"Not\", \"NOT\" when triggered. Upstream connections are directly from token embedd…

</details>

<details>
<summary><b>SA-4</b> — tool trace (16 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F12126 | " expressions of agreement or acknowledgement, particularly "well" and " |
| 2 | `get_upstream_features` | L4:F12126@2, k=5 | Emb:" well"@2 (w=14.62) +4 more |
| 3 | `inspect_feature` | L2, F1759 | "occurrences of the word "know" with emphasis words or interjections ne" |
| 4 | `inspect_feature` | L3, F4735 | " references to multi-well plates and software used in scientific exper" |
| 5 | `inspect_feature` | L3, F13677 | " text from law transcripts (with "sir", "ubuntu" with version numbers," |
| 6 | `get_upstream_features` | L2:F1759@2, k=5 | Emb:" well"@2 (w=12.56) +4 more |
| 7 | `inspect_feature` | L1, F6696 | "the word "pool" in different contexts, but it also shows some activati" |
| 8 | `inspect_feature` | L1, F5901 | " HTML form elements, dates, and a few proper nouns." |
| 9 | `get_upstream_features` | L1:F5901@2, k=5 | Emb:"yeah"@1 (w=3.27) +4 more |
| 10 | `get_upstream_features` | L3:F4735@2, k=5 | Emb:" well"@2 (w=25.75) +4 more |
| 11 | `inspect_feature` | L2, F2039 | " the word "well"." |
| 12 | `inspect_feature` | L1, F7361 | "the word "well"" |
| 13 | `inspect_feature` | L0, F8352 | " the word "well"" |
| 14 | `inspect_feature` | L0, F2071 | " internet-related jargon like URLs, informal speech, and expressions o" |
| 15 | `inspect_feature` | L0, F15972 | "the word "yeah"" |
| 16 | `get_upstream_features` | L3:F13677@2, k=5 | Emb:"yeah"@1 (w=6.84) +4 more |

**Findings:** Tracing L4:F12126 at position 2 upstream reveals that this feature encodes ACTUAL PROMPT CONTENT (specifically, the token "well" at position 2) rather than spurious negation signals. 

Key findings:
1. The feature directly connects to the embedding of " well" at position 2 with a strong weight of 14.625 and to "yeah" at position 1 with weight 4.6875.
2. The feature's label ("expressions of agreeme…

</details>

<details>
<summary><b>SA-5</b> — tool trace (8 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F3820 | "the word "the"" |
| 2 | `get_upstream_features` | L0:F3820@3, k=5 | Emb:" the"@3 (w=33.00) +4 more |
| 3 | `inspect_feature` | L0, F317 | "words that can be used as exclamations or excitement, or words used on" |
| 4 | `get_upstream_features` | L0:F3820@3, k=10 | Emb:" the"@3 (w=33.00) +9 more |
| 5 | `inspect_feature` | L0, F713 | "a mix of context dependent terms that are diverse and hard to summariz" |
| 6 | `inspect_feature` | L0, F812 | " a combination of the word "levels" and a number, or military terms" |
| 7 | `get_top_logits` | k=10 | "" (100%) |
| 8 | `inspect_feature` | L0, F350 | "words related to both spatial height and also the height of something " |

**Findings:** The circuit for L0:F3820 at position 3 is primarily driven by direct connection from the token " the" at the same position (edge_weight: 33.0), with negative influence from "yeah" at position 1. This feature detects the word "the" but actually suppresses it in output (see suppressed_tokens includes "the"). The feature has low frac_nonzero (0.0299), indicating it's specific to detecting "the" in ce…

</details>

<details>
<summary><b>SA-6</b> — tool trace (3 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F16366 | " the word "because"" |
| 2 | `get_upstream_features` | L0:F16366@25, k=5 | Emb:" because"@25 (w=40.75) +4 more |
| 3 | `get_top_logits` | k=5 | "" (100%) |

**Findings:** The feature L0:F16366 at position 25 encodes detection of the literal token \"because\". It has a very strong direct connection (weight 40.75) to the embedding of \" because\" at the same position, indicating it's primarily a lexical feature for this specific word. The feature has relatively low frac_nonzero (0.01813) suggesting specificity. Promoted tokens are mostly punctuation and common charac…

</details>

<details>
<summary><b>SA-7</b> — tool trace (9 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L2, F5201 | "awards and accomplishments in the context of sports" |
| 2 | `get_upstream_features` | L2:F5201@8, k=5 | Emb:" tournament"@8 (w=16.38) +4 more |
| 3 | `inspect_feature` | L1, F11938 | "mentions of meals, restaurants, and food" |
| 4 | `inspect_feature` | L0, F15183 | " the word "fighting"" |
| 5 | `get_upstream_features` | L1:F11938@8, k=5 | Emb:" tournament"@8 (w=13.06) +4 more |
| 6 | `inspect_feature` | L0, F8659 | "the word "foundation" in different contexts, including religious, lega" |
| 7 | `get_upstream_features` | L0:F15183@8, k=5 | Emb:" tournament"@8 (w=19.38) +4 more |
| 8 | `get_upstream_features` | L0:F8659@8, k=5 | Emb:" tournament"@8 (w=15.25) +4 more |
| 9 | `get_top_logits` | k=5 | "" (100%) |

**Findings:** The circuit analysis shows that L2:F5201 at position 8 is primarily driven by the word "tournament" at the same position, with a very strong edge weight of 16.375. This feature encodes "awards and accomplishments in the context of sports" and has low frac_nonzero (0.00993), indicating specificity. The feature promotes tokens like "</b>", "honors", "big" which are formatting and accomplishment-rela…

</details>

<details>
<summary><b>SA-8</b> — tool trace (8 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L1, F177 | " the word "double" and words that begin with "multi" or "doubly"" |
| 2 | `get_upstream_features` | L1:F177@6, k=5 | Emb:" double"@6 (w=24.00) +4 more |
| 3 | `inspect_feature` | L0, F4782 | " the word "double"" |
| 4 | `inspect_feature` | L0, F5124 | " the word "double" and concepts relating to pairs or duality" |
| 5 | `inspect_feature` | L0, F8083 | "the word "double" and surrounding words when numbers are also present" |
| 6 | `get_upstream_features` | L0:F4782@6, k=5 | Emb:" double"@6 (w=21.75) +4 more |
| 7 | `get_upstream_features` | L0:F5124@6, k=5 | Emb:" double"@6 (w=16.50) +4 more |
| 8 | `get_upstream_features` | L0:F8083@6, k=5 | Emb:" double"@6 (w=19.62) +4 more |

**Findings:** The trace reveals that L1:F177 is primarily detecting the word "double" and related terms. The circuit is very shallow and direct: L1:F177 receives its strongest signal (weight 24.0) directly from the embedding of the token "double" at position 6, suggesting this is a simple lexical detection feature rather than encoding negation signals or complex semantic content. Three L0 features (4782, 5124, …

</details>

<details>
<summary><b>SA-9</b> — tool trace (6 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F4541 | " adverbs of certainty such as "obviously" and related words" |
| 2 | `get_upstream_features` | L0:F4541@1, k=5 | Emb:"yeah"@1 (w=12.38) +4 more |
| 3 | `get_upstream_features` | L0:F4541@1, k=20 | Emb:"yeah"@1 (w=12.38) +19 more |
| 4 | `get_top_logits` | k=10 | "" (100%) |
| 5 | `inspect_feature` | L0, F317 | "words that can be used as exclamations or excitement, or words used on" |
| 6 | `inspect_feature` | L0, F350 | "words related to both spatial height and also the height of something " |

**Findings:** The feature L0:F4541 is an adverb detection feature (recognizing words like "obviously") that fires strongly when the token "yeah" appears at position 1. The circuit is extremely simple: the feature receives strong positive input (edge weight 12.375) directly from the embedding of token "yeah" at position 1, and a weaker positive input (1.0625) from the <bos> token at position 0. No other early-la…

</details>

<details>
<summary><b>SA-10</b> — tool trace (4 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F10780 | " LaTeX commands for including packages and defining document class" |
| 2 | `get_upstream_features` | L0:F10780@6, k=5 | Emb:" double"@6 (w=15.62) +4 more |
| 3 | `get_upstream_features` | L0:F10780@6, k=10 | Emb:" double"@6 (w=15.62) +9 more |
| 4 | `get_top_logits` | k=5 | "" (100%) |

**Findings:** The feature L0:F10780 at position 6 detects 'LaTeX commands for including packages and defining document class'. Tracing upstream reveals it is primarily driven by the embedding of token ' double' at the same position with a strong positive weight of 15.625. Minor contributions come from other token embeddings: '<bos>' (0.3906), ' uh' (0.1758), 'yeah' (0.0879), while ' NC' provides weak inhibition…

</details>

### Build

`build_circuit` → 19 nodes, 19 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m2.7 | 22,527 | 4,453 | 54,190 | 0 | — | — | — |
| SA-3 | deepseek/deepseek-v3.2 | 15,026 | 1,348 | 2,304 | 0 | — | ✅ 1F/3E | Trace L0:F6236 at pos 37 upstream to identify what semantic … |
| SA-2 | deepseek/deepseek-v3.2 | 20,662 | 1,679 | 4,480 | 0 | — | ✅ 3F/3E | Trace L0:F8352 at pos 2 upstream to identify what semantic c… |
| SA-5 | deepseek/deepseek-v3.2 | 46,635 | 2,857 | 0 | 0 | — | ✅ 5F/8E | Trace L0:F3820 at pos 3 upstream. Identify if this encodes s… |
| SA-1 | deepseek/deepseek-v3.2 | 78,184 | 3,999 | 9,920 | 0 | — | ✅ 7F/19E | Trace L4:F9602 at pos 4 upstream to identify its semantic co… |
| SA-4 | deepseek/deepseek-v3.2 | 117,541 | 4,096 | 14,656 | 0 | — | ✅ 11F/12E | Trace L4:F12126 at pos 2 upstream to identify its semantic c… |
| SA-6 | deepseek/deepseek-v3.2 | 13,048 | 1,431 | 0 | 0 | — | ✅ 1F/4E | Trace L0:F16366 at pos 25 upstream. Identify if this encodes… |
| SA-8 | deepseek/deepseek-v3.2 | 44,104 | 2,638 | 0 | 0 | — | ✅ 4F/19E | Trace L1:F177 at pos 6 upstream. Determine if this encodes n… |
| SA-7 | deepseek/deepseek-v3.2 | 46,969 | 2,744 | 4,288 | 0 | — | ✅ 4F/15E | Trace L2:F5201 at pos 8 upstream. Check if this is encoding … |
| SA-9 | deepseek/deepseek-v3.2 | 29,483 | 1,390 | 0 | 0 | — | ✅ 1F/2E | Trace L0:F4541 at pos 1 upstream. Determine if this is spuri… |
| SA-10 | deepseek/deepseek-v3.2 | 17,279 | 2,088 | 0 | 0 | — | ✅ 1F/5E | Trace L0:F10780 at pos 6 upstream. Is this spurious negation… |
| **Total** | | **451,458** | **28,723** | **89,838** | **0** | **—** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 7m 38s