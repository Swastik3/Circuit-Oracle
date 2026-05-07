# Circuit Oracle Report
**Date:** 2026-04-06 14:32:30 UTC | **Orchestrator:** minimax/minimax-m2.7 | **Subagent:** deepseek/deepseek-v3.2

## Input

**Prompt:** "Dataset: civil_comments-pos_pos_8 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "('The circuit use spurious features (e.g.,"an identity group" signals) rather than actual prompt content (lexical or semaintical) to predict toxicity.',)"

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** This probe attribution circuit reveals that the probe's classification score is driven primarily by semantic content detection—specifically, a cascade of features that recognize Islamic religious terminology ("Islam", "Allah") and their associated concepts (Middle Eastern names, religious identity, faith terms, political conflicts involving Muslims), culminating in a layer-12 feature that detects "negative language denigrating groups of people" triggered by the phrase "Islam is false religion." The circuit directly traces to the input tokens "Islam" (pos 4), "Allah" (pos 13), and "false" (pos 10), with the strongest signal (L6:F7282, direct_effect=0.4121) specifically encoding "mentions of Islam or Middle Eastern places and people" and promoting tokens like mosques, Muslim, mosque, Islamic, and Muhammad—indicating genuine Islamic religious content detection rather than identity-group spurious correlations.

**Confidence:** 9/10

**Reasoning:** The circuit shows a clear hierarchical processing pathway from input tokens through semantically meaningful features to the probe output. The primary driver (L6:F7282, frac_nonzero=0.007) is highly selective, activating only on 0.7% of tokens and specifically promoting Islamic vocabulary. The second-strongest feature (L4:F2405, direct_effect=0.3145) detects "words related to religious identity/affiliation or spirituality" with frac_nonzero=0.007, also highly selective. The "Group Denigration Detector" (L12:F7779, direct_effect=0.1416) specifically detects "negative language denigrating groups of people" when "Islam" and "false" co-occur. The signal flows through multiple specialized layers (L0→L2→L3→L4→L6→L8→L12) rather than relying on generic identity markers. Negative-effect features (L1:F4314, L3:F12024, L7:F12448) suppress certain Islam-related outputs but do not override the dominant positive signal from content-specific detectors. The circuit reaches embedding nodes (Emb: Islam, Emb: Allah, Emb: false) with strong edge weights (18.5, 15.875, 7.1875 respectively), confirming that specific lexical content—not generic "identity group" signals—drives the probe's classification.

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L6:7282 de=0.412 |

### Dispatch: 13 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L6:F7282@4` | ✅ reported | 7 | 13 | Trace L6:F7282 (pos 4, direct_effect 0.4121) - the top feature. What does it enc… |
| SA-2 | `L4:F2405@4` | ✅ reported | 6 | 6 | Trace L4:F2405 (pos 4, direct_effect 0.3145) - what does this feature encode and… |
| SA-3 | `L8:F13197@4` | ✅ reported | 6 | 12 | Trace L8:F13197 (pos 4, direct_effect 0.2656) - what does this feature encode an… |
| SA-4 | `L0:F13885@4` | ✅ reported | 1 | 5 | Trace L0:F13885 (pos 4, direct_effect 0.2051) - what does this feature encode an… |
| SA-5 | `L0:F6051@12` | ✅ reported | 1 | 5 | Trace L0:F6051 (pos 12, direct_effect 0.1611) - what does this feature encode an… |
| SA-6 | `L0:F880@7` | ✅ reported | 3 | 8 | Trace L0:F880 (pos 7, direct_effect -0.1738) - this is a negative effect feature… |
| SA-7 | `L1:F4314@4` | ✅ reported | 3 | 7 | Trace L1:F4314 (pos 4, direct_effect -0.2441) - a NEGATIVE effect feature. What … |
| SA-8 | `L3:F12024@4` | ✅ reported | 5 | 15 | Trace L3:F12024 (pos 4, direct_effect -0.2207) - a NEGATIVE effect feature. What… |
| SA-9 | `L7:F12448@4` | ✅ reported | 11 | 23 | Trace L7:F12448 (pos 4, direct_effect -0.1816) - a NEGATIVE effect feature. What… |
| SA-10 | `L4:F15997@3` | ✅ reported | 9 | 20 | Trace L4:F15997 (pos 3, direct_effect -0.1699) - what does this feature encode a… |
| SA-11 | `L6:F7282@13` | ✅ reported | 4 | 7 | Trace L6:F7282 (pos 13, direct_effect 0.1465) - the same feature as pos 4 but at… |
| SA-12 | `L10:F2716@4` | ✅ reported | 6 | 10 | Trace L10:F2716 (pos 4, direct_effect -0.1465) - what does this feature encode a… |
| SA-13 | `L12:F7779@10` | ✅ reported | 9 | 18 | Trace L12:F7779 (pos 10, direct_effect 0.1416) - what does this feature encode a… |

<details>
<summary><b>SA-1</b> — tool trace (12 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F7282 | " mentions of Islam or Middle Eastern places and people, as well as men" |
| 2 | `get_upstream_features` | L6:F7282@4, k=5 | Emb:" Islam"@4 (w=18.50) +4 more |
| 3 | `inspect_feature` | L0, F13885 | " names of people and places, specifically those related to the middle " |
| 4 | `inspect_feature` | L5, F6490 | " words and phrases related to geography, politics, or groups of people" |
| 5 | `inspect_feature` | L4, F2405 | " words related to religious identity/affiliation or spirituality inclu" |
| 6 | `inspect_feature` | L5, F14348 | " historical and religious terms, along with associated concepts like s" |
| 7 | `get_upstream_features` | L0:F13885@4, k=5 | Emb:" Islam"@4 (w=12.25) +4 more |
| 8 | `get_upstream_features` | L4:F2405@4, k=5 | Emb:" Islam"@4 (w=21.50) +4 more |
| 9 | `inspect_feature` | L3, F12024 | " words referencing the religion of Islam, people who practice it, and " |
| 10 | `get_upstream_features` | L3:F12024@4, k=5 | Emb:" Islam"@4 (w=8.50) +4 more |
| 11 | `inspect_feature` | L2, F7214 | " references to countries or regions associated with Islam" |
| 12 | `get_upstream_features` | L2:F7214@4, k=5 | Emb:" Islam"@4 (w=12.38) +4 more |

**Findings:** Tracing L6:F7282 reveals a circuit that encodes mentions of Islam or Middle Eastern places and people. The signal originates directly from the token embedding "Islam" at position 4, which has the strongest connection (edge_weight 18.5) to the target feature. Multiple pathways converge on L6:F7282:

1. **Direct token embedding**: " Islam" token at position 4 feeds into L6:F7282 with weight 18.5 (st…

</details>

<details>
<summary><b>SA-2</b> — tool trace (10 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F2405 | " words related to religious identity/affiliation or spirituality inclu" |
| 2 | `get_upstream_features` | L4:F2405@4, k=5 | Emb:" Islam"@4 (w=21.50) +4 more |
| 3 | `inspect_feature` | L3, F12024 | " words referencing the religion of Islam, people who practice it, and " |
| 4 | `inspect_feature` | L1, F12107 | " mentions of political entities and concepts" |
| 5 | `get_upstream_features` | L3:F12024@4, k=5 | Emb:" Islam"@4 (w=8.50) +4 more |
| 6 | `inspect_feature` | L0, F13885 | " names of people and places, specifically those related to the middle " |
| 7 | `get_upstream_features` | L1:F12107@4, k=5 | Emb:" Islam"@4 (w=14.31) +4 more |
| 8 | `inspect_feature` | L0, F9026 | "technical documents or data, including numbers, units, and references " |
| 9 | `inspect_feature` | L2, F7214 | " references to countries or regions associated with Islam" |
| 10 | `get_upstream_features` | L2:F7214@4, k=5 | Emb:" Islam"@4 (w=12.38) +4 more |

**Findings:** L4:F2405 encodes religious identity/affiliation concepts and shows direct strong connection from the input token " Islam" at position 4 (edge_weight=21.5). The circuit reveals that this feature primarily detects the word "Islam" itself, with multiple supporting features that refine the representation:

1. L3:F12024 detects words referencing Islam specifically and connects negatively (-1.875) to L4…

</details>

<details>
<summary><b>SA-3</b> — tool trace (11 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L8, F13197 | " words related to religion and faith" |
| 2 | `get_upstream_features` | L8:F13197@4, k=5 | Emb:" Islam"@4 (w=9.25) +4 more |
| 3 | `inspect_feature` | L4, F2405 | " words related to religious identity/affiliation or spirituality inclu" |
| 4 | `inspect_feature` | L6, F7282 | " mentions of Islam or Middle Eastern places and people, as well as men" |
| 5 | `inspect_feature` | L7, F14049 | " discussion of international political conflicts, especially those reg" |
| 6 | `get_upstream_features` | L4:F2405@4, k=5 | Emb:" Islam"@4 (w=21.50) +4 more |
| 7 | `get_upstream_features` | L6:F7282@4, k=5 | Emb:" Islam"@4 (w=18.50) +4 more |
| 8 | `get_upstream_features` | L7:F14049@4, k=5 | Emb:" Islam"@4 (w=5.91) +4 more |
| 9 | `inspect_feature` | L0, F13885 | " names of people and places, specifically those related to the middle " |
| 10 | `inspect_feature` | L5, F6490 | " words and phrases related to geography, politics, or groups of people" |
| 11 | `get_upstream_features` | L5:F6490@4, k=5 | Emb:" Islam"@4 (w=3.47) +4 more |

**Findings:** The circuit for L8:F13197 (pos 4) encodes "words related to religion and faith" and originates from the input token " Islam" at position 4. This is a direct religious content detection circuit:

1. The core signal originates from the token embedding of " Islam" at position 4, which has strong direct connections to multiple features across layers (edge weights: 9.25 to L8, 21.5 to L4, 18.5 to L6, 5…

</details>

<details>
<summary><b>SA-4</b> — tool trace (4 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F13885 | " names of people and places, specifically those related to the middle " |
| 2 | `get_upstream_features` | L0:F13885@4, k=5 | Emb:" Islam"@4 (w=12.25) +4 more |
| 3 | `get_top_logits` | k=5 | "" (100%) |
| 4 | `get_upstream_features` | L0:F13885@4, k=10 | Emb:" Islam"@4 (w=12.25) +9 more |

**Findings:** L0:F13885 at position 4 encodes "names of people and places, specifically those related to the middle east" and has a direct_effect of 0.2051. Tracing upstream revealed this feature is directly connected to embedding nodes (no further transcoder features upstream), with the strongest connection to the token " Islam" at position 4 (edge_weight 12.25). This makes semantic sense: the feature detects …

</details>

<details>
<summary><b>SA-5</b> — tool trace (5 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F6051 | "periods, spaces, and the number 1" |
| 2 | `get_upstream_features` | L0:F6051@12, k=5 | Emb:"."@12 (w=46.50) +4 more |
| 3 | `get_upstream_features` | L0:F6051@12, k=10 | Emb:"."@12 (w=46.50) +9 more |
| 4 | `get_upstream_features` | L0:F6051@12, k=20 | Emb:"."@12 (w=46.50) +19 more |
| 5 | `get_top_logits` | k=5 | "" (100%) |

**Findings:** The feature L0:F6051 at position 12 encodes detection of periods, spaces, and the number 1. Its signal originates directly from the input token embedding for "." at position 12 with a very strong positive edge weight of 46.5, indicating this is a bottom-up punctuation detection feature. The feature also receives weaker negative influences from other tokens including "<bos>", " religion", " Islam",…

</details>

<details>
<summary><b>SA-6</b> — tool trace (9 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F880 | " references to the pronoun "it", and sometimes "that", suggesting obse" |
| 2 | `get_upstream_features` | L0:F880@7, k=5 | Emb:" it"@7 (w=44.00) +4 more |
| 3 | `get_top_logits` | k=5 | "" (100%) |
| 4 | `get_upstream_features` | L0:F880@7, k=10 | Emb:" it"@7 (w=44.00) +9 more |
| 5 | `inspect_feature` | L0, F2364 | " the word "The" and opening HTML heading tags" |
| 6 | `inspect_feature` | L0, F2455 | "the word "case", sometimes in relation to a preposition" |
| 7 | `get_upstream_features` | L0:F880@7, k=20 | Emb:" it"@7 (w=44.00) +19 more |
| 8 | `get_upstream_features` | L0:F880@7, k=50 | Emb:" it"@7 (w=44.00) +49 more |
| 9 | `get_top_features` | token="is", k=10 | ❌ Token 'is' not found in top logits. Available: [''] |

**Findings:** L0:F880 at position 7 is a pronoun detector feature that encodes references to the pronoun \"it\" (and sometimes \"that\"). Its signal comes almost exclusively from the token embedding of \" it\" at the same position (weight 44.0). There are weaker negative connections from surrounding tokens in the phrase \"The problem with Islam is that it...\" including \" that\" (-0.8555), \" is\" (-0.2637), \…

</details>

<details>
<summary><b>SA-7</b> — tool trace (6 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L1, F4314 | " the word Muslim" |
| 2 | `get_upstream_features` | L1:F4314@4, k=5 | Emb:" Islam"@4 (w=16.50) +4 more |
| 3 | `inspect_feature` | L0, F3031 | "the word "bias"" |
| 4 | `inspect_feature` | L0, F3512 | " words related to ancient history, mythology, and royalty" |
| 5 | `get_upstream_features` | L0:F3031@4, k=5 | Emb:" Islam"@4 (w=13.31) +4 more |
| 6 | `get_upstream_features` | L0:F3512@4, k=5 | Emb:" Islam"@4 (w=5.78) +4 more |

**Findings:** L1:F4314 is a feature that detects the word "Muslim" but has a negative effect (-0.2441 direct_effect) on the output. Its signal originates from the input token " Islam" at position 4, which feeds directly into the feature with strong positive weight (16.5) and also through intermediate L0 features. The L0 features include F3031 detecting "bias" and F3512 detecting ancient/royal terms. Interesting…

</details>

<details>
<summary><b>SA-8</b> — tool trace (9 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L3, F12024 | " words referencing the religion of Islam, people who practice it, and " |
| 2 | `get_upstream_features` | L3:F12024@4, k=5 | Emb:" Islam"@4 (w=8.50) +4 more |
| 3 | `inspect_feature` | L0, F13885 | " names of people and places, specifically those related to the middle " |
| 4 | `inspect_feature` | L1, F4314 | " the word Muslim" |
| 5 | `get_upstream_features` | L1:F4314@4, k=5 | Emb:" Islam"@4 (w=16.50) +4 more |
| 6 | `get_upstream_features` | L0:F13885@4, k=5 | Emb:" Islam"@4 (w=12.25) +4 more |
| 7 | `inspect_feature` | L0, F3031 | "the word "bias"" |
| 8 | `inspect_feature` | L0, F3512 | " words related to ancient history, mythology, and royalty" |
| 9 | `get_top_logits` | k=5 | "" (100%) |

**Findings:** Tracing L3:F12024 reveals an interesting circuit that suppresses Islam-related outputs. The feature encodes "words referencing the religion of Islam, people who practice it, and Arabic names" but actually SUPPRESSES tokens like "Muslim", "Muslims", "Islam", "Islamic" (as seen in its suppressed_tokens list). 

The circuit originates from the input token " Islam" at position 4, which feeds directly …

</details>

<details>
<summary><b>SA-9</b> — tool trace (17 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L7, F12448 | "words and phrases related to religion" |
| 2 | `get_upstream_features` | L7:F12448@4, k=5 | Emb:" Islam"@4 (w=3.77) +4 more |
| 3 | `inspect_feature` | L4, F2405 | " words related to religious identity/affiliation or spirituality inclu" |
| 4 | `inspect_feature` | L6, F3265 | " religion, religious figures, and related concepts and groups" |
| 5 | `inspect_feature` | L6, F1152 | " words related to religious topics and stories" |
| 6 | `get_upstream_features` | L4:F2405@4, k=5 | Emb:" Islam"@4 (w=21.50) +4 more |
| 7 | `inspect_feature` | L3, F12024 | " words referencing the religion of Islam, people who practice it, and " |
| 8 | `inspect_feature` | L1, F12107 | " mentions of political entities and concepts" |
| 9 | `inspect_feature` | L2, F7214 | " references to countries or regions associated with Islam" |
| 10 | `get_upstream_features` | L3:F12024@4, k=5 | Emb:" Islam"@4 (w=8.50) +4 more |
| 11 | `inspect_feature` | L0, F13885 | " names of people and places, specifically those related to the middle " |
| 12 | `inspect_feature` | L1, F4314 | " the word Muslim" |
| 13 | `get_upstream_features` | L6:F3265@4, k=5 | Emb:" Islam"@4 (w=6.09) +4 more |
| 14 | `inspect_feature` | L5, F6331 | " words about race, religion, and slavery" |
| 15 | `inspect_feature` | L1, F2352 | " words associated with Islam" |
| 16 | `get_upstream_features` | L6:F1152@4, k=5 | Emb:" Islam"@4 (w=4.47) +4 more |
| 17 | `get_upstream_features` | L2:F7214@4, k=5 | Emb:" Islam"@4 (w=12.38) +4 more |

**Findings:** Tracing L7:F12448 (pos 4, direct_effect -0.1816) revealed a circuit that suppresses religious content, particularly Islam-related terms. The feature encodes "words and phrases related to religion" and suppresses tokens like "CHRISTIAN", "Christian", "Religion", etc.

The signal originates from the input token " Islam" at position 4, which strongly feeds into multiple layers:
1. Directly to L7:F124…

</details>

<details>
<summary><b>SA-10</b> — tool trace (13 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F15997 | " discussion of advantages and/or disadvantages" |
| 2 | `get_upstream_features` | L4:F15997@3, k=5 | L3:F14698 (w=3.66) +4 more |
| 3 | `inspect_feature` | L3, F14698 | "expressions of disagreement or problems with something" |
| 4 | `inspect_feature` | L3, F8595 | " descriptive writing" |
| 5 | `inspect_feature` | L3, F1395 | " the word “wrong” and various prefixes" |
| 6 | `get_upstream_features` | L3:F14698@3, k=5 | Emb:" problem"@2 (w=14.62) +4 more |
| 7 | `get_upstream_features` | L3:F8595@3, k=5 | Emb:" problem"@2 (w=6.94) +4 more |
| 8 | `get_upstream_features` | L3:F1395@3, k=5 | Emb:" with"@3 (w=15.56) +4 more |
| 9 | `inspect_feature` | L2, F12222 | " the phrase "good news" and similar phrases related to positive outcom" |
| 10 | `inspect_feature` | L1, F7816 | "the word "with"" |
| 11 | `inspect_feature` | L1, F9523 | "prepositions and related words." |
| 12 | `inspect_feature` | L2, F11090 | " words related to objectives, ideas, and conclusions" |
| 13 | `inspect_feature` | L0, F2158 | "the word "with"" |

**Findings:** The circuit traces L4:F15997 which encodes "discussion of advantages and/or disadvantages". This feature primarily receives its signal from three main upstream features in layer 3: L3:F14698 (expressions of disagreement or problems), L3:F8595 (descriptive writing), and L3:F1395 (word "wrong" and prefixes). The strongest signal originates from token embeddings: "problem" at position 2 (with edge we…

</details>

<details>
<summary><b>SA-11</b> — tool trace (8 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F7282 | " mentions of Islam or Middle Eastern places and people, as well as men" |
| 2 | `get_upstream_features` | L6:F7282@13, k=5 | Emb:" Allah"@13 (w=15.88) +4 more |
| 3 | `inspect_feature` | L0, F13885 | " names of people and places, specifically those related to the middle " |
| 4 | `inspect_feature` | L1, F2235 | " passages from the Quran" |
| 5 | `get_upstream_features` | L0:F13885@13, k=5 | Emb:" Allah"@13 (w=15.44) +4 more |
| 6 | `get_upstream_features` | L1:F2235@13, k=5 | Emb:" Islam"@4 (w=8.19) +4 more |
| 7 | `inspect_feature` | L0, F13885 | " names of people and places, specifically those related to the middle " |
| 8 | `get_upstream_features` | L0:F13885@4, k=5 | Emb:" Islam"@4 (w=12.25) +4 more |

**Findings:** The tracing reveals that L6:F7282 at position 13 detects mentions of Islam or Middle Eastern places and people. The signal originates from the token "Allah" at position 13, which has a very strong direct connection (edge_weight=15.875) to the L6 feature. Additionally, the token "Islam" at position 4 contributes to the signal through two pathways: (1) directly to L1:F2235 (Quran passages feature), …

</details>

<details>
<summary><b>SA-12</b> — tool trace (9 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L10, F2716 | "mentions of religion, faith, parenting, and family when they appear to" |
| 2 | `get_upstream_features` | L10:F2716@4, k=5 | Emb:" Islam"@4 (w=3.03) +4 more |
| 3 | `inspect_feature` | L8, F13197 | " words related to religion and faith" |
| 4 | `inspect_feature` | L4, F2405 | " words related to religious identity/affiliation or spirituality inclu" |
| 5 | `get_upstream_features` | L8:F13197@4, k=5 | Emb:" Islam"@4 (w=9.25) +4 more |
| 6 | `get_upstream_features` | L4:F2405@4, k=5 | Emb:" Islam"@4 (w=21.50) +4 more |
| 7 | `inspect_feature` | L3, F12024 | " words referencing the religion of Islam, people who practice it, and " |
| 8 | `inspect_feature` | L1, F12107 | " mentions of political entities and concepts" |
| 9 | `inspect_feature` | L6, F7282 | " mentions of Islam or Middle Eastern places and people, as well as men" |

**Findings:** The tracing reveals that L10:F2716 at position 4 encodes "mentions of religion, faith, parenting, and family when they appear together" with a direct effect of -0.1465 (inhibitory). The signal originates predominantly from the input token " Islam" at position 4, which has very strong direct connections to multiple features in the circuit:

1. **Direct token embedding**: The token " Islam" at posit…

</details>

<details>
<summary><b>SA-13</b> — tool trace (15 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L12, F7779 | " negative language denigrating groups of people" |
| 2 | `get_upstream_features` | L12:F7779@10, k=5 | Emb:" false"@10 (w=7.19) +4 more |
| 3 | `inspect_feature` | L2, F13635 | "the word "false" and "boolean" in code snippets or logic statements" |
| 4 | `get_upstream_features` | L2:F13635@10, k=5 | Emb:" false"@10 (w=27.62) +4 more |
| 5 | `inspect_feature` | L0, F5977 | "text discussing lies or falseness and truth, especially in the context" |
| 6 | `get_upstream_features` | L12:F7779@10, k=10 | Emb:" false"@10 (w=7.19) +9 more |
| 7 | `inspect_feature` | L8, F16036 | " words and phrases related to Israel, Zionism, and related political t" |
| 8 | `inspect_feature` | L2, F4053 | " inflammatory hateful words, phrases, and names that attack groups of " |
| 9 | `inspect_feature` | L8, F4462 | " discussions of race, politics, and hypocrisy" |
| 10 | `get_upstream_features` | L2:F4053@10, k=5 | Emb:" false"@10 (w=6.81) +4 more |
| 11 | `inspect_feature` | L1, F9521 | " the word "true", sometimes in conjunction with the word "court"" |
| 12 | `inspect_feature` | L1, F11171 | " boolean values" |
| 13 | `get_upstream_features` | L1:F9521@10, k=5 | Emb:" false"@10 (w=16.25) +4 more |
| 14 | `inspect_feature` | L0, F2703 | " instances of statements being untrue" |
| 15 | `get_upstream_features` | L1:F11171@10, k=5 | Emb:" false"@10 (w=15.00) +4 more |

**Findings:** Tracing L12:F7779 reveals a circuit that detects negative language denigrating groups of people, particularly triggered by statements like "Islam is false". The strongest signal originates from the token "false" at position 10 (edge_weight 7.1875) and "Islam" at position 4 (edge_weight 2.8125). 

Key findings:
1. The feature encodes "negative language denigrating groups of people" (frac_nonzero 0.…

</details>

### Build

`build_circuit` → 19 nodes, 34 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m2.7 | 90,413 | 5,138 | 35,820 | 0 | $0.0344 | — | — |
| SA-4 | deepseek/deepseek-v3.2 | 17,411 | 1,772 | 0 | 0 | $0.0052 | ✅ 1F/5E | Trace L0:F13885 (pos 4, direct_effect 0.2051) - what does th… |
| SA-5 | deepseek/deepseek-v3.2 | 23,532 | 1,678 | 0 | 0 | $0.0068 | ✅ 1F/5E | Trace L0:F6051 (pos 12, direct_effect 0.1611) - what does th… |
| SA-2 | deepseek/deepseek-v3.2 | 58,583 | 2,427 | 3,520 | 0 | $0.0162 | ✅ 6F/6E | Trace L4:F2405 (pos 4, direct_effect 0.3145) - what does thi… |
| SA-3 | deepseek/deepseek-v3.2 | 72,786 | 3,269 | 0 | 0 | $0.0202 | ✅ 6F/12E | Trace L8:F13197 (pos 4, direct_effect 0.2656) - what does th… |
| SA-1 | deepseek/deepseek-v3.2 | 83,606 | 3,368 | 0 | 0 | $0.0230 | ✅ 7F/13E | Trace L6:F7282 (pos 4, direct_effect 0.4121) - the top featu… |
| SA-6 | deepseek/deepseek-v3.2 | 53,366 | 2,485 | 0 | 0 | $0.0148 | ✅ 3F/8E | Trace L0:F880 (pos 7, direct_effect -0.1738) - this is a neg… |
| SA-7 | deepseek/deepseek-v3.2 | 30,623 | 2,007 | 0 | 0 | $0.0087 | ✅ 3F/7E | Trace L1:F4314 (pos 4, direct_effect -0.2441) - a NEGATIVE e… |
| SA-8 | deepseek/deepseek-v3.2 | 52,552 | 2,783 | 0 | 0 | $0.0147 | ✅ 5F/15E | Trace L3:F12024 (pos 4, direct_effect -0.2207) - a NEGATIVE … |
| SA-10 | deepseek/deepseek-v3.2 | 82,839 | 4,070 | 11,264 | 0 | $0.0234 | ✅ 9F/20E | Trace L4:F15997 (pos 3, direct_effect -0.1699) - what does t… |
| SA-9 | deepseek/deepseek-v3.2 | 140,167 | 5,568 | 14,656 | 0 | $0.0389 | ✅ 11F/23E | Trace L7:F12448 (pos 4, direct_effect -0.1816) - a NEGATIVE … |
| SA-11 | deepseek/deepseek-v3.2 | 44,871 | 2,062 | 0 | 0 | $0.0125 | ✅ 4F/7E | Trace L6:F7282 (pos 13, direct_effect 0.1465) - the same fea… |
| SA-12 | deepseek/deepseek-v3.2 | 54,408 | 2,872 | 0 | 0 | $0.0152 | ✅ 6F/10E | Trace L10:F2716 (pos 4, direct_effect -0.1465) - what does t… |
| SA-13 | deepseek/deepseek-v3.2 | 121,303 | 5,506 | 2,368 | 0 | $0.0337 | ✅ 9F/18E | Trace L12:F7779 (pos 10, direct_effect 0.1416) - what does t… |
| **Total** | | **926,460** | **45,005** | **67,628** | **0** | **$0.2677** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 32m 39s