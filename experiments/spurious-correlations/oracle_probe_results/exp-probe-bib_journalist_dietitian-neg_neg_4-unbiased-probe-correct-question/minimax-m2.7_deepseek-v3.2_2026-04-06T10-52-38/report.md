# Circuit Oracle Report
**Date:** 2026-04-06 10:52:39 UTC | **Orchestrator:** minimax/minimax-m2.7 | **Subagent:** deepseek/deepseek-v3.2

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-neg_neg_4 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "('The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession.',)"

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score is driven primarily by a gender marker feature (L0:F12768 detecting "he/she" pronouns, direct_effect=+0.0747) that directly reads from the "he" token embedding, rather than by genuine profession indicators. The actual professional descriptors ("writer", "freelance", "journalism") at positions 27-28 have negative effects on the probe score, while spurious gender markers and positional tokens ("at", "Institute") have mixed negative effects.

**Confidence:** 9/10

**Reasoning:** The circuit analysis reveals a significant spurious feature reliance:

1. **Gender Marker as Top Positive Driver**: L0:F12768 (pos 22) encodes "mentions of 'he' and 'she' in close proximity" with the strongest positive direct_effect (+0.0747) among profession-relevant features. This feature receives its signal almost entirely from the "he" token embedding at position 22 (edge_weight: 40.25), making this a direct gender marker dependency.

2. **Genuine Profession Indicators Suppress the Score**: The journalism/writer circuit at position 28 shows negative contributions:
   - L14:F4420 (journalism/newspapers): direct_effect = -0.0679
   - L6:F12712 (editors/publishers): direct_effect = -0.0588
   - These features detect "writer", "freelance", "journalism", "reporter" but are weighted NEGATIVELY in the probe classification.

3. **The Journalism Circuit**: The writer-related features do form a coherent hierarchical circuit:
   - "writer" embedding → L2:F9210 (journalism/writing) → L4:F13253 (journalism/media) → L8:F8855 (news reporters) → L14:F4420 (journalism)
   - With strong edge weights from the "writer" token (10.6875 at L2, 9.125 at L4)
   - But this genuine profession signal is penalized, not rewarded

4. **Spurious Features**: Token-level features like "at" (L0:F7124, -0.1582) and "Institute" entity detectors also contribute but with negative effects, suggesting the probe learns to penalize certain structural patterns.

The circuit confirms the user's concern: the probe relies heavily on gender pronouns ("he") as a classification signal while penalizing explicit profession indicators like "writer" and "journalism". This is a textbook example of spurious feature reliance where demographic markers (gender) are used rather than task-relevant features (professional descriptors).

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L0:7124 de=-0.158 |

### Dispatch: 8 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L0:F7124@2` | ✅ reported | 3 | 3 | Trace L0:F7124 at pos 2 - this is the top feature by direct effect. What does it… |
| SA-2 | `L0:F15661@7` | ✅ reported | 1 | 1 | Trace L0:F15661 at pos 7 - this is a high-impact feature. What does it encode an… |
| SA-3 | `L0:F12768@22` | ✅ reported | 1 | 3 | Trace L0:F12768 at pos 22 - this is a positive effect feature. What does it enco… |
| SA-4 | `L14:F4420@28` | ✅ reported | 11 | 20 | Trace L14:F4420 at pos 28 - this is a late-layer feature with strong negative ef… |
| SA-5 | `L6:F12712@28` | ✅ reported | 5 | 14 | Trace L6:F12712 at pos 28 - another late-layer feature. What does it encode and … |
| SA-6 | `L3:F10489@7` | ✅ reported | 7 | 13 | Trace L3:F10489 at pos 7 - this is a negative effect feature. What does it encod… |
| SA-7 | `L1:F4459@7` | ✅ reported | 4 | 8 | Trace L1:F4459 at pos 7 - another negative effect feature. What does it encode a… |
| SA-8 | `L2:F12901@15` | ✅ reported | 7 | 12 | Trace L2:F12901 at pos 15 - a negative effect feature. What does it encode and w… |

<details>
<summary><b>SA-1</b> — tool trace (6 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F7124 | "the word "at"" |
| 2 | `get_upstream_features` | L0:F7124@2, k=5 | Emb:" at"@2 (w=31.38) +4 more |
| 3 | `inspect_feature` | L0, F419 | "the word "fixed" or its variants in technical contexts." |
| 4 | `inspect_feature` | L0, F437 | " words that are names or titles of things, or otherwise capitalized no" |
| 5 | `get_top_logits` | k=5 | "" (100%) |
| 6 | `get_upstream_features` | L0:F7124@2, k=10 | Emb:" at"@2 (w=31.38) +9 more |

**Findings:** L0:F7124 at position 2 encodes "the word 'at'" and its signal originates almost entirely from the embedding of the token " at" at position 2 (edge weight 31.375). This is a very direct circuit: the feature detects the literal word "at" and gets its strongest signal from that exact token's embedding. The feature has low sparsity (frac_nonzero = 0.00954), making it specific to detecting "at". The to…

</details>

<details>
<summary><b>SA-2</b> — tool trace (3 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F15661 | "the word "spin"" |
| 2 | `get_upstream_features` | L0:F15661@7, k=5 | Emb:" Institute"@7 (w=19.38) +4 more |
| 3 | `get_top_logits` | k=5 | "" (100%) |

**Findings:** L0:F15661 at position 7 encodes \"the word 'spin'\" but is being activated by the token \" Institute\" at position 7 with a very strong edge weight of 19.375. This feature has low sparsity (frac_nonzero = 0.00328), indicating it's specific.observed that other upstream tokens include \" Royal\" (pos 4), \" United\" (pos 5), and \" Services\" (pos 6), suggesting the full context might be \"Royal Uni…

</details>

<details>
<summary><b>SA-3</b> — tool trace (4 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F12768 | " mentions of "he" and "she" in close proximity" |
| 2 | `get_upstream_features` | L0:F12768@22, k=5 | Emb:" he"@22 (w=40.25) +4 more |
| 3 | `get_upstream_features` | L0:F12768@22, k=10 | Emb:" he"@22 (w=40.25) +9 more |
| 4 | `get_top_logits` | k=5 | "" (100%) |

**Findings:** The feature L0:F12768 at position 22 encodes "mentions of 'he' and 'she' in close proximity". Its signal originates primarily from the token " he" at position 22 itself, with a very strong edge weight of 40.25. Additional contextual influence comes from the beginning-of-sequence token <bos> at position 0 (weight 3.84) and comma "," at position 21 (weight 1.48). This is a layer 0 feature that direc…

</details>

<details>
<summary><b>SA-4</b> — tool trace (20 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L14, F4420 | "words and phrases related to journalism and newspapers" |
| 2 | `get_upstream_features` | L14:F4420@28, k=5 | Emb:" writer"@28 (w=5.78) +4 more |
| 3 | `inspect_feature` | L8, F8855 | " mentions of news reporters and news reporting" |
| 4 | `inspect_feature` | L4, F13253 | " things related to journalism and the media" |
| 5 | `get_upstream_features` | L8:F8855@28, k=5 | Emb:" writer"@28 (w=4.72) +4 more |
| 6 | `inspect_feature` | L7, F72 | " words related to writing professionally" |
| 7 | `inspect_feature` | L7, F13646 | " news reporting and journalism." |
| 8 | `get_upstream_features` | L4:F13253@28, k=5 | Emb:" writer"@28 (w=9.12) +4 more |
| 9 | `get_upstream_features` | L7:F72@28, k=5 | Emb:" writer"@28 (w=5.69) +4 more |
| 10 | `inspect_feature` | L6, F6721 | " html code and related tags particularly href, public, content, title," |
| 11 | `inspect_feature` | L6, F12712 | " titles of editors and publishers in scientific publications" |
| 12 | `get_upstream_features` | L7:F13646@28, k=5 | Emb:" writer"@28 (w=2.77) +4 more |
| 13 | `inspect_feature` | L4, F661 | " words and phrases used when referring to reports, documentaries, and " |
| 14 | `get_upstream_features` | L4:F661@28, k=5 | Emb:" freelance"@27 (w=3.94) +4 more |
| 15 | `get_upstream_features` | L6:F12712@28, k=5 | Emb:" writer"@28 (w=6.22) +4 more |
| 16 | `inspect_feature` | L2, F9210 | "words related to journalism, writing, and articles" |
| 17 | `get_upstream_features` | L2:F9210@28, k=5 | Emb:" writer"@28 (w=10.69) +4 more |
| 18 | `inspect_feature` | L3, F12195 | "words about the process of writing and lithography" |
| 19 | `get_upstream_features` | L3:F12195@28, k=5 | Emb:" writer"@28 (w=13.94) +4 more |
| 20 | `inspect_feature` | L2, F12020 | " code that writes XML or RSS feeds" |

**Findings:** The circuit tracing reveals that L14:F4420 at position 28 encodes "words and phrases related to journalism and newspapers" with a strong negative effect. The signal originates from the input token " writer" at position 28 (with edge_weight 5.7812) and secondarily from " freelance" at position 27 (edge_weight 2.75).

Key findings:
1. The starting feature L14:F4420 (journalism/newspapers) receives s…

</details>

<details>
<summary><b>SA-5</b> — tool trace (9 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F12712 | " titles of editors and publishers in scientific publications" |
| 2 | `get_upstream_features` | L6:F12712@28, k=5 | Emb:" writer"@28 (w=6.22) +4 more |
| 3 | `inspect_feature` | L4, F13253 | " things related to journalism and the media" |
| 4 | `inspect_feature` | L2, F9210 | "words related to journalism, writing, and articles" |
| 5 | `get_upstream_features` | L4:F13253@28, k=5 | Emb:" writer"@28 (w=9.12) +4 more |
| 6 | `get_upstream_features` | L2:F9210@28, k=5 | Emb:" writer"@28 (w=10.69) +4 more |
| 7 | `inspect_feature` | L0, F7973 | "uses of the word "guarantee" and related abstract nouns." |
| 8 | `inspect_feature` | L0, F7376 | " references to writers or writing" |
| 9 | `get_upstream_features` | L0:F7376@28, k=5 | Emb:" writer"@28 (w=19.88) +4 more |

**Findings:** The circuit tracing reveals that L6:F12712 (titles of editors and publishers in scientific publications) primarily encodes journalistic/writing roles and gets its strongest signal directly from the token embedding of " writer" at position 28 (edge_weight: 6.2188). 

Key findings:
1. L6:F12712 detects editorial titles in scientific publishing contexts with relatively low sparsity (0.01747)
2. The s…

</details>

<details>
<summary><b>SA-6</b> — tool trace (11 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L3, F10489 | " the word "Institute"" |
| 2 | `get_upstream_features` | L3:F10489@7, k=5 | Emb:" Institute"@7 (w=27.12) +4 more |
| 3 | `inspect_feature` | L2, F13783 | " the word "Institute"" |
| 4 | `inspect_feature` | L1, F14993 | " words related to drainage systems" |
| 5 | `get_upstream_features` | L2:F13783@7, k=5 | Emb:" Institute"@7 (w=27.12) +4 more |
| 6 | `inspect_feature` | L1, F4459 | " mentions of research institutes" |
| 7 | `get_upstream_features` | L1:F14993@7, k=5 | Emb:" Institute"@7 (w=17.00) +4 more |
| 8 | `inspect_feature` | L0, F6484 | " the word "sky"" |
| 9 | `inspect_feature` | L0, F15661 | "the word "spin"" |
| 10 | `inspect_feature` | L0, F2485 | "the word "play" in various tenses/forms, often associated with the wor" |
| 11 | `get_upstream_features` | L1:F4459@7, k=5 | Emb:" Institute"@7 (w=27.50) +4 more |

**Findings:** This circuit traces L3:F10489 at position 7, which is a "negative effect feature" that encodes the word "Institute" and suppresses the token "Institute" in its output (as seen from its suppressed_tokens). The feature detects the word "Institute" but has an inhibitory effect, likely preventing over-generation of the same token.

Key findings:
1. L3:F10489 receives strong positive input directly fro…

</details>

<details>
<summary><b>SA-7</b> — tool trace (8 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L1, F4459 | " mentions of research institutes" |
| 2 | `get_upstream_features` | L1:F4459@7, k=5 | Emb:" Institute"@7 (w=27.50) +4 more |
| 3 | `inspect_feature` | L0, F15661 | "the word "spin"" |
| 4 | `inspect_feature` | L0, F12879 | "the word "squad" and words related to team membership" |
| 5 | `inspect_feature` | L0, F8466 | " the word "volume."" |
| 6 | `get_upstream_features` | L0:F15661@7, k=5 | Emb:" Institute"@7 (w=19.38) +4 more |
| 7 | `get_upstream_features` | L0:F12879@7, k=5 | Emb:" Institute"@7 (w=15.50) +4 more |
| 8 | `get_upstream_features` | L0:F8466@7, k=5 | Emb:" Institute"@7 (w=14.44) +4 more |

**Findings:** L1:F4459 at position 7 encodes "mentions of research institutes" with very low sparsity (0.00295), making it highly specific. Its signal primarily originates directly from the token " Institute" at position 7 with a strong positive edge weight of 27.5. This feature also receives weaker contributions from three Layer 0 features that themselves are strongly driven by the same " Institute" token. Int…

</details>

<details>
<summary><b>SA-8</b> — tool trace (10 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L2, F12901 | " the phrase "Middle East"" |
| 2 | `get_upstream_features` | L2:F12901@15, k=5 | Emb:" East"@15 (w=26.62) +4 more |
| 3 | `inspect_feature` | L0, F15865 | " the word "Cup", sometimes in association with international sports, b" |
| 4 | `inspect_feature` | L1, F10435 | "words referring to geographical locations, scientific studies and lega" |
| 5 | `inspect_feature` | L0, F7140 | "the word "classic"" |
| 6 | `get_upstream_features` | L1:F10435@15, k=5 | Emb:" East"@15 (w=16.25) +4 more |
| 7 | `inspect_feature` | L0, F12020 | "mentions of the word "South" in various contexts." |
| 8 | `inspect_feature` | L0, F15880 | "mentions of the Middle East" |
| 9 | `inspect_feature` | L0, F15939 | " words related to official records" |
| 10 | `get_upstream_features` | L0:F15865@15, k=5 | Emb:" Middle"@14 (w=18.00) +4 more |

**Findings:** L2:F12901 at position 15 is a feature that detects the phrase "Middle East" but has a negative effect - it suppresses tokens like "East", "east", "EAST", "West", "west", etc. The token at position 15 is " East" and the token at position 14 is " Middle".

The circuit originates from two main embedding sources:
1. " East" at position 15 (edge_weight: 26.625) - direct strong positive connection
2. " …

</details>

### Build

`build_circuit` → 9 nodes, 8 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m2.7 | 19,085 | 3,754 | 38,055 | 0 | $0.0114 | — | — |
| SA-2 | deepseek/deepseek-v3.2 | 12,751 | 1,368 | 0 | 0 | $0.0038 | ✅ 1F/1E | Trace L0:F15661 at pos 7 - this is a high-impact feature. Wh… |
| SA-3 | deepseek/deepseek-v3.2 | 17,615 | 1,310 | 0 | 0 | $0.0051 | ✅ 1F/3E | Trace L0:F12768 at pos 22 - this is a positive effect featur… |
| SA-1 | deepseek/deepseek-v3.2 | 30,322 | 1,745 | 0 | 0 | $0.0085 | ✅ 3F/3E | Trace L0:F7124 at pos 2 - this is the top feature by direct … |
| SA-5 | deepseek/deepseek-v3.2 | 52,829 | 3,001 | 0 | 0 | $0.0149 | ✅ 5F/14E | Trace L6:F12712 at pos 28 - another late-layer feature. What… |
| SA-4 | deepseek/deepseek-v3.2 | 148,331 | 5,367 | 30,592 | 0 | $0.0414 | ✅ 11F/20E | Trace L14:F4420 at pos 28 - this is a late-layer feature wit… |
| SA-7 | deepseek/deepseek-v3.2 | 43,282 | 1,987 | 0 | 0 | $0.0120 | ✅ 4F/8E | Trace L1:F4459 at pos 7 - another negative effect feature. W… |
| SA-8 | deepseek/deepseek-v3.2 | 50,135 | 3,205 | 14,400 | 0 | $0.0146 | ✅ 7F/12E | Trace L2:F12901 at pos 15 - a negative effect feature. What … |
| SA-6 | deepseek/deepseek-v3.2 | 69,426 | 3,174 | 0 | 0 | $0.0193 | ✅ 7F/13E | Trace L3:F10489 at pos 7 - this is a negative effect feature… |
| **Total** | | **443,776** | **24,911** | **83,047** | **0** | **$0.1310** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 6m 42s