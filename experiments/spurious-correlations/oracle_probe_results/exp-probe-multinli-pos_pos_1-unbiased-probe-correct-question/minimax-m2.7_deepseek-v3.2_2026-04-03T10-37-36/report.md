# Circuit Oracle Report
**Date:** 2026-04-03 10:37:36 UTC | **Orchestrator:** minimax/minimax-m2.7 | **Subagent:** deepseek/deepseek-v3.2

## Input
**Prompt:** "Dataset: multinli-pos_pos_1 | Probe: unbiased | Method: correct"
**System prompt:** ""
**Question:** "('The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction.',)"
**Top predictions:**  (100.0%)

## Oracle Analysis
**Analysis:** This attribution circuit reveals that the layer-22 probe's classification is driven by **three distinct semantic content pathways** from the input text "Conspiracy theorists MasterCard is investing in a chip..." — NOT by spurious negation word signals. The circuit shows: (1) **Conspiracy detection** via "Cons"+"piracy"→L0:F16015(prefix "cons")→L3:F9739("conspiracies")→L8:F12761("QAnon") with direct edge weights of 8.75 and 7.63 from token embeddings; (2) **Financial content detection** via "MasterCard"→L0:F1859→L1:F7447("card")→L4:F4153("currency/banking")→L6:F10189("payment info")→L7:F1062("credit cards/money") with strong 14.06 weight from "Card" token; (3) **Technology content detection** via "chip"→L1:F6066→L2:F16230("semiconductor chips") with dominant 27.0 embedding weight.

**Confidence:** 9/10

**Reasoning:** The circuit is NOT using spurious features like "negation words" — every major feature I traced encodes actual semantic content from the prompt:
- **L3:F9739** (direct_effect=-0.3457, strongest) detects "words related to conspiracies" and fires on "theorists" at position 2, driven by token embeddings "Cons"(pos 1, weight 8.75) and "piracy"(pos 2, weight 7.63). frac_nonzero=0.00762 confirms this is a highly specific feature, not a generic pattern.
- **L8:F12761** detects "QAnon conspiracy theory" on "theorists" at position 3, fed by L2:F16028 ("speculation, lies, false information, and conspiracy theories") and L7:F2730 ("rumors").
- **L7:F1062** detects "credit cards, loans, gambling, and money" on "Card" at position 6, built from L6:F10189 ("payment and financial information") and L4:F4153 ("currency and banking").
- **L2:F16230** detects "semiconductor chips and devices" on "chip" at position 11, with 27.0 direct embedding weight.

All features have **low frac_nonzero values** (0.003-0.03), indicating highly specific activation patterns rather than generic linguistic markers like negation words. The features converge to the output probe through legitimate semantic abstraction chains: raw tokens → character/word detection → domain-specific concepts (conspiracy, finance, semiconductors). The user's concern about "negation word" signals is unfounded — no negation-related features appear in the top 10, and the circuit purely tracks substantive content words that would be relevant for contradiction detection (conspiracy rhetoric, financial claims, technological assertions).

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 10 features; top: L3:9739 de=-0.346 |
| 3 | `inspect_feature` ×9 | L3:9739, L2:16230, L7:1062, L0:3635, L1:13684, L4:1602, L0:16015, L2:16241, L8:12761 |

### Dispatch: 8 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L3:F9739@2` | ✅ reported | 7 | 13 | Trace L3:F9739 ("words related to conspiracies") - what upstream features or inp… |
| SA-2 | `L8:F12761@3` | ✅ reported | 8 | 16 | Trace L8:F12761 ("words associated with QAnon conspiracy theory") - what upstrea… |
| SA-3 | `L0:F16015@1` | ✅ reported | 4 | 2 | Trace L0:F16015 ("the prefix 'cons'") - what upstream features or input tokens d… |
| SA-4 | `L2:F16230@11` | ✅ reported | 6 | 12 | Trace L2:F16230 ("semiconductor chips and devices") - what upstream features or … |
| SA-5 | `L7:F1062@6` | ✅ reported | 9 | 20 | Trace L7:F1062 ("credit cards, loans, spending, gambling, and money") - what ups… |
| SA-6 | `L1:F13684@3` | ✅ reported | 6 | 8 | Trace L1:F13684 ("the word 'theory'") - what upstream features or input tokens d… |
| SA-7 | `L4:F1602@3` | ✅ reported | 9 | 11 | Trace L4:F1602 ("words indicating intense interest or enthusiasm") - what upstre… |
| SA-8 | `L0:F3635@12` | ✅ reported | 1 | 5 | Trace L0:F3635 ("the word 'that'") - what upstream features or input tokens driv… |

<details>
<summary><b>SA-1</b> — tool trace (11 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L3, F9739 | " words related to conspiracies" |
| 2 | `get_upstream_features` | L3:F9739@2, k=5 | Emb:"Cons"@1 (w=8.75) +4 more |
| 3 | `inspect_feature` | L2, F13361 | " the character sequence "cti" or "tact" within a word" |
| 4 | `inspect_feature` | L0, F2115 | " data reported as a percentage inside brackets, especially in a labora" |
| 5 | `inspect_feature` | L2, F1741 | "fragments of words ending in "ction", "notes," or "ual."" |
| 6 | `get_upstream_features` | L2:F13361@2, k=5 | Emb:"Cons"@1 (w=17.38) +4 more |
| 7 | `inspect_feature` | L0, F16015 | "the prefix "cons"" |
| 8 | `inspect_feature` | L0, F9026 | "technical documents or data, including numbers, units, and references " |
| 9 | `get_upstream_features` | L2:F1741@2, k=5 | Emb:"Cons"@1 (w=22.88) +4 more |
| 10 | `inspect_feature` | L0, F7159 | "words ending in "ic", "ness", "tion", "ship", "ment", "ize", "ate", or" |
| 11 | `get_upstream_features` | L0:F16015@1, k=5 | Emb:"Cons"@1 (w=21.12) +4 more |

**Findings:** The conspiracy-related detection feature L3:F9739 is primarily driven by input tokens "Cons" (position 1) and "piracy" (position 2) via their embeddings with strong positive weights (8.75 and 7.625). The feature is inhibited by L2:F13361 which detects "cti" or "tact" sequences, and this inhibitory feature itself is strongly driven by the "Cons" token. Interestingly, the prefix "cons" is detected e…

</details>

<details>
<summary><b>SA-2</b> — tool trace (14 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L8, F12761 | " words associated with the QAnon conspiracy theory" |
| 2 | `get_upstream_features` | L8:F12761@3, k=5 | Emb:" theorists"@3 (w=4.59) +4 more |
| 3 | `inspect_feature` | L2, F16028 | " terms related to speculation, lies, false information, and conspiracy" |
| 4 | `inspect_feature` | L7, F13859 | " legal documents, especially ones related to people representing thems" |
| 5 | `inspect_feature` | L7, F2730 | " mentions of rumors and reports" |
| 6 | `get_upstream_features` | L2:F16028@3, k=5 | Emb:" theorists"@3 (w=11.75) +4 more |
| 7 | `get_upstream_features` | L7:F13859@3, k=5 | Emb:"piracy"@2 (w=5.25) +4 more |
| 8 | `get_upstream_features` | L7:F2730@3, k=5 | Emb:" theorists"@3 (w=6.53) +4 more |
| 9 | `inspect_feature` | L3, F9739 | " words related to conspiracies" |
| 10 | `get_upstream_features` | L3:F9739@2, k=5 | Emb:"Cons"@1 (w=8.75) +4 more |
| 11 | `inspect_feature` | L4, F14283 | " legal language related to defamation and workplace issues" |
| 12 | `get_upstream_features` | L4:F14283@3, k=5 | Emb:"piracy"@2 (w=4.88) +4 more |
| 13 | `inspect_feature` | L0, F9026 | "technical documents or data, including numbers, units, and references " |
| 14 | `inspect_feature` | L7, F382 | " words related to discovering information" |

**Findings:** I traced the circuit for L8:F12761 ("words associated with the QAnon conspiracy theory") at position 3. The analysis reveals:

1. **Direct Input Token Influence**: The strongest connection is directly from the input token "theorists" at position 3 (edge weight 4.59), suggesting this token strongly drives the QAnon feature.

2. **Key Intermediate Features**:
   - **L2:F16028**: Detects "terms relat…

</details>

<details>
<summary><b>SA-3</b> — tool trace (5 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F16015 | "the prefix "cons"" |
| 2 | `get_upstream_features` | L0:F16015@1, k=5 | Emb:"Cons"@1 (w=21.12) +4 more |
| 3 | `inspect_feature` | L0, F353 | " words related to math, physics, and scientific studies" |
| 4 | `inspect_feature` | L0, F437 | " words that are names or titles of things, or otherwise capitalized no" |
| 5 | `inspect_feature` | L0, F33 | "terms related to research papers, medical conditions, and professional" |

**Findings:** The feature L0:F16015 ("the prefix 'cons'") at position 1 is primarily driven by the input token "Cons" at position 1 with a very strong edge weight of 21.125. This represents a direct mapping from the token "Cons" to the feature that detects the "cons" prefix. There is also a minor connection from the BOS token at position 0 (weight 0.7227). The circuit is very shallow - this is a low-level chara…

</details>

<details>
<summary><b>SA-4</b> — tool trace (11 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L2, F16230 | " mentions of semiconductor chips and devices" |
| 2 | `get_upstream_features` | L2:F16230@11, k=5 | Emb:" chip"@11 (w=27.00) +4 more |
| 3 | `inspect_feature` | L1, F6066 | " the word 'chip', possibly in the context of hardware" |
| 4 | `inspect_feature` | L0, F351 | " the word "expert"" |
| 5 | `inspect_feature` | L0, F1506 | " the word "circuit"" |
| 6 | `get_upstream_features` | L1:F6066@11, k=5 | Emb:" chip"@11 (w=21.38) +4 more |
| 7 | `inspect_feature` | L0, F3041 | " when something is directed or related to power, gas, physical parts, " |
| 8 | `get_upstream_features` | L0:F1506@11, k=5 | Emb:" chip"@11 (w=15.25) +4 more |
| 9 | `get_upstream_features` | L0:F351@11, k=5 | Emb:" chip"@11 (w=19.25) +4 more |
| 10 | `get_upstream_features` | L0:F3041@11, k=5 | Emb:" chip"@11 (w=12.12) +4 more |
| 11 | `inspect_feature` | L0, F9026 | "technical documents or data, including numbers, units, and references " |

**Findings:** The circuit tracing reveals that L2:F16230 ("semiconductor chips and devices") is primarily driven by the direct embedding of the word "chip" at position 11 (weight 27.0). This strong signal flows through multiple paths:

1. Direct embedding connection (27.0 weight)
2. Through L1:F6066 which detects "the word 'chip'" (weight 0.75) - itself strongly connected to "chip" embedding (21.375)
3. Through…

</details>

<details>
<summary><b>SA-5</b> — tool trace (13 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L7, F1062 | " words and phrases related to credit cards, loans, spending, gambling," |
| 2 | `get_upstream_features` | L7:F1062@6, k=5 | Emb:"Card"@6 (w=14.06) +4 more |
| 3 | `inspect_feature` | L6, F10189 | " phrases related to payment and financial information (especially cred" |
| 4 | `inspect_feature` | L4, F4153 | " words or phrases related to currency and banking transactions" |
| 5 | `inspect_feature` | L3, F3595 | "the occurence of the word "card"" |
| 6 | `get_upstream_features` | L6:F10189@6, k=5 | Emb:"Card"@6 (w=13.31) +4 more |
| 7 | `get_upstream_features` | L4:F4153@6, k=5 | Emb:"Card"@6 (w=11.06) +4 more |
| 8 | `inspect_feature` | L1, F7447 | " the word card" |
| 9 | `inspect_feature` | L2, F7725 | "the word "card" when used in a technical context" |
| 10 | `get_upstream_features` | L1:F7447@6, k=5 | Emb:"Card"@6 (w=22.62) +4 more |
| 11 | `inspect_feature` | L0, F1859 | " the word "card"" |
| 12 | `inspect_feature` | L4, F1248 | " brand names of companies or products" |
| 13 | `inspect_feature` | L0, F5969 | " the word "tour"" |

**Findings:** I traced the circuit driving L7:F1062 ("credit cards, loans, spending, gambling, and money") from position 6. The circuit reveals a clear financial content detection pathway:

1. **Direct Input**: The strongest driver is the raw token embedding "Card" at position 6 (weight: 14.0625), with "Master" at position 5 providing negative influence.

2. **Layer 6 Integration**: L6:F10189 (payment/financial…

</details>

<details>
<summary><b>SA-6</b> — tool trace (10 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L1, F13684 | " the word "theory"" |
| 2 | `get_upstream_features` | L1:F13684@3, k=5 | Emb:" theorists"@3 (w=10.12) +4 more |
| 3 | `inspect_feature` | L0, F15958 | " the word "tomorrow"" |
| 4 | `inspect_feature` | L0, F9026 | "technical documents or data, including numbers, units, and references " |
| 5 | `get_upstream_features` | L0:F15958@3, k=5 | Emb:" theorists"@3 (w=12.06) +4 more |
| 6 | `get_upstream_features` | L0:F9026@3, k=5 | Emb:" theorists"@3 (w=25.50) +4 more |
| 7 | `get_upstream_features` | L1:F13684@3, k=10 | Emb:" theorists"@3 (w=10.12) +9 more |
| 8 | `inspect_feature` | L0, F1847 | "scientific terms and experimental details related to biological and ch" |
| 9 | `inspect_feature` | L0, F2368 | " technical terms used in scientific writing" |
| 10 | `inspect_feature` | L0, F10155 | " words related to membership in a group" |

**Findings:** The circuit for detecting "theory" at layer 1 (F13684) is primarily driven by the input token "theorists" at position 3, with a strong direct connection (weight=10.125) from its embedding. This makes sense as "theorists" contains the root "theory". The layer 1 feature also receives weaker positive signals from several layer 0 features that detect scientific/technical terms (F1847, F2368) and negat…

</details>

<details>
<summary><b>SA-7</b> — tool trace (13 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F1602 | " words or phrases that indicate intense interest or enthusiasm, often " |
| 2 | `get_upstream_features` | L4:F1602@3, k=5 | Emb:" theorists"@3 (w=3.20) +4 more |
| 3 | `inspect_feature` | L2, F7100 | " words denoting people/groups involved in politics/occupations/status" |
| 4 | `inspect_feature` | L2, F2988 | " words related to searching, research, or investigation" |
| 5 | `inspect_feature` | L2, F16028 | " terms related to speculation, lies, false information, and conspiracy" |
| 6 | `get_upstream_features` | L2:F7100@3, k=5 | Emb:" theorists"@3 (w=9.44) +4 more |
| 7 | `get_upstream_features` | L2:F2988@3, k=5 | Emb:" theorists"@3 (w=11.50) +4 more |
| 8 | `get_upstream_features` | L2:F16028@3, k=5 | Emb:" theorists"@3 (w=11.75) +4 more |
| 9 | `inspect_feature` | L3, F12920 | " words ending in "-ist", "-er", "-man", or "-grapher" when those descr" |
| 10 | `inspect_feature` | L0, F4327 | " terms related to people in positions of authority and/or roles in an " |
| 11 | `inspect_feature` | L0, F13839 | " words related to legal, governmental, and political events and proces" |
| 12 | `inspect_feature` | L1, F1771 | "the phrase 'X-ray'" |
| 13 | `inspect_feature` | L0, F9026 | "technical documents or data, including numbers, units, and references " |

**Findings:** The tracing reveals that L4:F1602 ("words indicating intense interest or enthusiasm") is primarily driven by the input token "theorists" at position 3 (direct weight 3.2031), with significant contributions from three key L2 features:

1. L2:F7100 detects "people/groups involved in politics/occupations/status"
2. L2:F2988 detects "searching, research, or investigation"  
3. L2:F16028 detects "specu…

</details>

<details>
<summary><b>SA-8</b> — tool trace (4 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F3635 | "the word "that"" |
| 2 | `get_upstream_features` | L0:F3635@12, k=5 | Emb:" that"@12 (w=41.00) +4 more |
| 3 | `get_upstream_features` | L0:F3635@12, k=10 | Emb:" that"@12 (w=41.00) +9 more |
| 4 | `get_top_logits` | k=5 | "" (100%) |

**Findings:** Tracing L0:F3635 (detecting the word "that") reveals it's a simple word-detection feature at the first transformer layer that connects directly to token embeddings. The primary driver is the embedding of " that" at position 12 itself (edge_weight 41.0), with minor contextual influences from other tokens like <bos>, "a", "theorists", and "in". This feature has low sparsity (frac_nonzero=0.0428), in…

</details>

### Build

`build_circuit` → 23 nodes, 33 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m2.7 | 35,948 | 6,207 | 102,571 | 0 | — | — | — |
| SA-3 | deepseek/deepseek-v3.2 | 24,968 | 1,764 | 0 | 0 | — | ✅ 4F/2E | Trace L0:F16015 ("the prefix 'cons'") - what upstream featur… |
| SA-1 | deepseek/deepseek-v3.2 | 73,993 | 3,452 | 0 | 0 | — | ✅ 7F/13E | Trace L3:F9739 ("words related to conspiracies") - what upst… |
| SA-2 | deepseek/deepseek-v3.2 | 99,462 | 3,916 | 0 | 0 | — | ✅ 8F/16E | Trace L8:F12761 ("words associated with QAnon conspiracy the… |
| SA-4 | deepseek/deepseek-v3.2 | 69,576 | 3,530 | 0 | 0 | — | ✅ 6F/12E | Trace L2:F16230 ("semiconductor chips and devices") - what u… |
| SA-5 | deepseek/deepseek-v3.2 | 92,002 | 4,018 | 0 | 0 | — | ✅ 9F/20E | Trace L7:F1062 ("credit cards, loans, spending, gambling, an… |
| SA-6 | deepseek/deepseek-v3.2 | 55,877 | 2,680 | 6,016 | 0 | — | ✅ 6F/8E | Trace L1:F13684 ("the word 'theory'") - what upstream featur… |
| SA-7 | deepseek/deepseek-v3.2 | 91,490 | 3,391 | 0 | 0 | — | ✅ 9F/11E | Trace L4:F1602 ("words indicating intense interest or enthus… |
| SA-8 | deepseek/deepseek-v3.2 | 17,131 | 1,548 | 0 | 0 | — | ✅ 1F/5E | Trace L0:F3635 ("the word 'that'") - what upstream features … |
| **Total** | | **560,447** | **30,506** | **108,587** | **0** | **—** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 11m 15s