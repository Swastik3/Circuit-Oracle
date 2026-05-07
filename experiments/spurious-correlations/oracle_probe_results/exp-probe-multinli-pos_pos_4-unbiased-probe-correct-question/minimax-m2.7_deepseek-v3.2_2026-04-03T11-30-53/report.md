# Circuit Oracle Report
**Date:** 2026-04-03 11:30:53 UTC | **Orchestrator:** minimax/minimax-m2.7 | **Subagent:** deepseek/deepseek-v3.2

## Input
**Prompt:** "Dataset: multinli-pos_pos_4 | Probe: unbiased | Method: correct"
**System prompt:** ""
**Question:** "('The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction.',)"
**Top predictions:**  (100.0%)

## Oracle Analysis
**Analysis:** The probe's classification score is driven almost entirely by **direct lexical matching** at layers 0-2, where features directly detect specific words in the input ("from", "so", "pick up", "No one", "about", "up", "tourist") without semantic understanding. The circuit bypasses deeper semantic processing, reading directly from token embeddings through simple word-detector features. There is one weak negation-pattern feature (L0:F13585, detecting "negative statements/absence"), but it contributes minimally (frac_nonzero=0.01588, positive effect through L2:F13586) and operates as a word-pattern matcher ("nobody", "nowhere") rather than a generic negation signal.

**Confidence:** 9/10

**Reasoning:** The circuit I built reveals a clear pattern: the probe's classification is driven by **10 top features at layers 0-2** that directly detect specific tokens. The strongest features are:
- **L0:F8974** (pos 5, direct_effect=-0.4082): Detects "from" via direct embedding connection (weight 38.75)
- **L0:F7321** (pos 25, direct_effect=+0.3848): Detects "so" via direct embedding (weight 40.25)  
- **L2:F3116** (pos 2, direct_effect=-0.3555): Detects "pick up" phrasal verb from "Pick"+"up" embeddings (weights 50, 20.75)
- **L2:F13586** (pos 17, direct_effect=-0.2119): Detects words ending in "thing"/"one" from "No"+"one" embeddings (weights 14, 12.875)

All features trace back to **direct token embedding inputs** with minimal contextual processing. The user's concern about **spurious features** is **PARTIALLY VALID**:
- There IS a negation-pattern feature (L0:F13585) that detects "No one" and promotes "Nobody"/"nobody" (promoted_tokens include these)
- However, this feature has low frac_nonzero (0.01588) and contributes **indirectly** through L2:F13586 (weight 1.78), making it a minor component

The circuit does **NOT** use sophisticated semantic features or entity-specific knowledge (all frac_nonzero values are low, indicating narrow word-pattern matching). The features detect **surface-level lexical patterns** without understanding the text's meaning about picking up maps and walking tours. This confirms the user's suspicion: the probe relies on spurious word-pattern matching rather than genuine semantic understanding or contradiction detection.

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 10 features; top: L0:8974 de=-0.408 |
| 3 | `inspect_feature` ×10 | L0:8974, L0:7321, L2:3116, L2:13586, L0:6051, L2:11769, L0:10904, L0:2238, L0:306, L0:10562 |

### Dispatch: 8 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L0:F8974@5` | ✅ reported | 1 | 5 | Trace the circuit upstream from L0:F8974 (detects "from" at pos 5) to understand… |
| SA-2 | `L0:F7321@25` | ✅ reported | 1 | 5 | Trace the circuit upstream from L0:F7321 (detects "so" at pos 25) to understand … |
| SA-3 | `L2:F3116@2` | ✅ reported | 7 | 21 | Trace the circuit upstream from L2:F3116 (detects "pick up" phrasal verb at pos … |
| SA-4 | `L0:F2238@12` | ✅ reported | 1 | 3 | Trace the circuit upstream from L0:F2238 (detects "about" at pos 12) to understa… |
| SA-5 | `L2:F13586@17` | ✅ reported | 2328 | 19 | Trace the circuit upstream from L2:F13586 (detects words ending in 'thing'/'one'… |
| SA-6 | `L2:F11769@2` | ✅ reported | 5 | 10 | Trace the circuit upstream from L2:F11769 (detects "up" at pos 2) to understand … |
| SA-7 | `L0:F306@7` | ✅ reported | 3 | 7 | Trace the circuit upstream from L0:F306 (detects "adoption" at pos 7, which is "… |
| SA-8 | `L0:F10562@2` | ✅ reported | 1 | 3 | Trace the circuit upstream from L0:F10562 (detects "up" at pos 2) to understand … |

<details>
<summary><b>SA-1</b> — tool trace (2 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F8974 | "the word "from"" |
| 2 | `get_upstream_features` | L0:F8974@5, k=5 | Emb:" from"@5 (w=38.75) +4 more |

**Findings:** The circuit from L0:F8974 (detects "from" at pos 5) is very direct: it primarily receives input from the raw token embedding of " from" at position 5 with a very strong edge weight of 38.75. There are minor contextual influences from other tokens like "<bos>", " map", " up", and " a", but these are much weaker (edge weights < 2.0). This feature is a direct detector of the word "from" that activate…

</details>

<details>
<summary><b>SA-2</b> — tool trace (2 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F7321 | " the word "so," and also matches some words ending in "ware" and "such" |
| 2 | `get_upstream_features` | L0:F7321@25, k=5 | Emb:" so"@25 (w=40.25) +4 more |

**Findings:** The circuit tracing shows that L0:F7321 at position 25 (which detects the word "so") is primarily driven by the embedding of the token " so" at the same position (position 25) with a very strong edge weight of 40.25. This is a direct, low-level detection circuit. The feature also receives weaker contextual inputs from other token embeddings: beginning of sequence (<bos> at pos 0), comma at positio…

</details>

<details>
<summary><b>SA-3</b> — tool trace (12 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L2, F3116 | " the phrasal verb "pick up" and variations" |
| 2 | `get_upstream_features` | L2:F3116@2, k=5 | Emb:"Pick"@1 (w=50.00) +4 more |
| 3 | `inspect_feature` | L0, F10562 | "the word "up"" |
| 4 | `inspect_feature` | L1, F13179 | "the words "pick", "picker", and forms of those words" |
| 5 | `inspect_feature` | L1, F11342 | " the word fragment "up" used in different contexts" |
| 6 | `get_upstream_features` | L0:F10562@2, k=5 | Emb:" up"@2 (w=37.00) +4 more |
| 7 | `get_upstream_features` | L1:F13179@1, k=5 | Emb:"Pick"@1 (w=21.62) +4 more |
| 8 | `get_upstream_features` | L1:F11342@2, k=5 | Emb:" up"@2 (w=14.25) +4 more |
| 9 | `inspect_feature` | L0, F5470 | " the words "forth" or "back" and words surrounding them" |
| 10 | `inspect_feature` | L0, F2051 | " terms related to paganism, instruments, and car parts" |
| 11 | `inspect_feature` | L0, F6421 | " words related to administrative processes and computer programs" |
| 12 | `get_upstream_features` | L0:F5470@2, k=5 | Emb:" up"@2 (w=5.25) +4 more |

**Findings:** I traced the circuit upstream from L2:F3116 which detects the "pick up" phrasal verb at position 2. The key findings:

1. L2:F3116 gets direct STRONG positive connections from embeddings: "Pick" at pos 1 (weight 50.0) and " up" at pos 2 (weight 20.75). This shows the feature is directly triggered by these specific tokens.

2. L2:F3116 receives NEGATIVE connections from:
   - L0:F10562 (detects "th…

</details>

<details>
<summary><b>SA-4</b> — tool trace (2 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F2238 | " the word "about" when followed by a numerical value" |
| 2 | `get_upstream_features` | L0:F2238@12, k=5 | Emb:" about"@12 (w=35.00) +4 more |

**Findings:** Tracing from L0:F2238 at position 12 (detects "about" when followed by numerical values) reveals it's primarily driven by the embedding of " about" at the same position (weight 35.0). Secondary contextual influences come from embeddings of "<bos>" at position 0 (weight 1.8516) and " ask" at position 11 (weight 1.7656). Since L0 is the first transformer layer, there are no earlier transformer featu…

</details>

<details>
<summary><b>SA-5</b> — tool trace (14 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L2, F13586 | " words ending in 'thing' and 'one' often with preceding words indicati" |
| 2 | `get_upstream_features` | L2:F13586@17, k=5 | Emb:" No"@16 (w=14.00) +4 more |
| 3 | `inspect_feature` | L0, F4438 | "the word "one"." |
| 4 | `inspect_feature` | L0, F11351 | " the number "one"" |
| 5 | `inspect_feature` | L0, F7636 | " the word "one"" |
| 6 | `get_upstream_features` | L0:F4438@17, k=5 | Emb:" No"@16 (w=29.38) +4 more |
| 7 | `get_upstream_features` | L0:F11351@17, k=5 | Emb:" one"@17 (w=38.50) +4 more |
| 8 | `get_upstream_features` | L0:F7636@17, k=5 | Emb:" one"@17 (w=13.88) +4 more |
| 9 | `get_upstream_features` | L2:F13586@17, k=10 | Emb:" No"@16 (w=14.00) +9 more |
| 10 | `inspect_feature` | L0, F15085 | " mentions of the words "one", "overall", and "cross."" |
| 11 | `inspect_feature` | L0, F13585 | " negative statements or the absence of something" |
| 12 | `inspect_feature` | L1, F805 | "things that are unique, preferable or time-based" |
| 13 | `inspect_feature` | L1, F15726 | " the word "one" or the keyword "async"" |
| 14 | `get_upstream_features` | L1:F15726@17, k=5 | Emb:" one"@17 (w=11.94) +4 more |

**Findings:** The circuit from L2:F13586 (detects words ending in 'thing'/'one') traces back to early layer features and token embeddings. Key findings:

1. **Direct embedding influence**: The L2 feature receives strong direct input from both "No" (pos 16, weight 14.0) and "one" (pos 17, weight 12.875) token embeddings.

2. **Layer 0 "one" detectors**: 
   - L0:F4438 (specific word "one" detector, frac_nonzero=…

</details>

<details>
<summary><b>SA-6</b> — tool trace (10 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L2, F11769 | "the word "up"" |
| 2 | `get_upstream_features` | L2:F11769@2, k=5 | Emb:" up"@2 (w=19.50) +4 more |
| 3 | `inspect_feature` | L0, F10562 | "the word "up"" |
| 4 | `inspect_feature` | L0, F9659 | "phrases involving "together" or "up"" |
| 5 | `inspect_feature` | L1, F9681 | "the word "region" and forms of the word "sense"" |
| 6 | `get_upstream_features` | L0:F10562@2, k=5 | Emb:" up"@2 (w=37.00) +4 more |
| 7 | `get_upstream_features` | L0:F9659@2, k=5 | Emb:" up"@2 (w=11.38) +4 more |
| 8 | `get_upstream_features` | L1:F9681@1, k=5 | Emb:"Pick"@1 (w=15.94) +4 more |
| 9 | `inspect_feature` | L0, F7344 | " content markers like figures and section headers" |
| 10 | `get_top_logits` | k=5 | "" (100%) |

**Findings:** I traced the circuit for L2:F11769 (detects "up" at position 2). The strongest connection is directly from the embedding of " up" at position 2 with edge_weight 19.5. There's also a weaker connection from "Pick" embedding at position 1 (5.5625). 

The key findings:
1. L2:F11769 receives inhibitory input from L0:F10562 (also detects "up") with weight -3.75, suggesting competitive inhibition between…

</details>

<details>
<summary><b>SA-7</b> — tool trace (6 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F306 | "the word "adoption" in various contexts" |
| 2 | `get_upstream_features` | L0:F306@7, k=5 | Emb:" tourist"@7 (w=22.00) +4 more |
| 3 | `get_top_logits` | k=5 | "" (100%) |
| 4 | `get_upstream_features` | L0:F306@7, k=10 | Emb:" tourist"@7 (w=22.00) +9 more |
| 5 | `inspect_feature` | L0, F1903 | "instances of sentences starting with "The"" |
| 6 | `inspect_feature` | L0, F2051 | " terms related to paganism, instruments, and car parts" |

**Findings:** The circuit from L0:F306 (detects "adoption") is extremely direct: it is primarily activated by the " tourist" token embedding at position 7 with a very strong weight of 22.0. This feature has low sparsity (frac_nonzero=0.01166), indicating it's specific to detecting "adoption". Other token embeddings have much weaker connections, and two other layer 0 features (1903 and 2051) have effectively zer…

</details>

<details>
<summary><b>SA-8</b> — tool trace (3 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F10562 | "the word "up"" |
| 2 | `get_upstream_features` | L0:F10562@2, k=5 | Emb:" up"@2 (w=37.00) +4 more |
| 3 | `get_top_logits` | k=5 | "" (100%) |

**Findings:** The circuit tracing from L0:F10562 reveals a simple direct connection: this feature that detects the word "up" at position 2 is primarily driven by the token embedding of " up" at the same position (weight 37.0). There are weaker contextual influences from the previous tokens "Pick" at position 1 (weight 1.0781) and "<bos>" at position 0 (weight 0.5586). Interestingly, despite being labeled as det…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` ×2 | L0:13585, L0:6051 |

### Build

`build_circuit` → 15 nodes, 13 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m2.7 | 31,979 | 5,679 | 81,518 | 0 | — | — | — |
| SA-4 | deepseek/deepseek-v3.2 | 8,867 | 1,083 | 0 | 0 | — | ✅ 1F/3E | Trace the circuit upstream from L0:F2238 (detects "about" at… |
| SA-1 | deepseek/deepseek-v3.2 | 8,999 | 1,100 | 0 | 0 | — | ✅ 1F/5E | Trace the circuit upstream from L0:F8974 (detects "from" at … |
| SA-2 | deepseek/deepseek-v3.2 | 9,225 | 1,365 | 0 | 0 | — | ✅ 1F/5E | Trace the circuit upstream from L0:F7321 (detects "so" at po… |
| SA-3 | deepseek/deepseek-v3.2 | 80,558 | 3,836 | 0 | 0 | — | ✅ 7F/21E | Trace the circuit upstream from L2:F3116 (detects "pick up" … |
| SA-8 | deepseek/deepseek-v3.2 | 13,138 | 1,337 | 0 | 0 | — | ✅ 1F/3E | Trace the circuit upstream from L0:F10562 (detects "up" at p… |
| SA-7 | deepseek/deepseek-v3.2 | 28,511 | 2,311 | 0 | 0 | — | ✅ 3F/7E | Trace the circuit upstream from L0:F306 (detects "adoption" … |
| SA-6 | deepseek/deepseek-v3.2 | 62,025 | 2,802 | 0 | 0 | — | ✅ 5F/10E | Trace the circuit upstream from L2:F11769 (detects "up" at p… |
| SA-5 | deepseek/deepseek-v3.2 | 104,256 | 4,240 | 9,408 | 0 | — | ✅ 2328F/19E | Trace the circuit upstream from L2:F13586 (detects words end… |
| **Total** | | **347,558** | **23,753** | **90,926** | **0** | **—** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 8m 53s