# Circuit Oracle Report
**Date:** 2026-04-06 17:23:13 UTC | **Orchestrator:** minimax/minimax-m2.7 | **Subagent:** deepseek/deepseek-v3.2

## Input

**Prompt:** "Dataset: multinli-pos_pos_6 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "('The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction.',)"

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score is driven by a combination of negation-based signals (particularly the "not"+"were" pattern at position 21) and lexical content features ("they" pronoun, "set" verb, "fire" content), with the negation features forming the dominant pathway.

**Confidence:** 8/10

**Reasoning:** The circuit analysis reveals a mixed mechanism that partially validates the user's concern. The attribution graph shows:

1. **Negation Circuit Dominance (pos 21):** The strongest pathway involves a multi-layer negation detection cascade: token "not" (weight 33.75) → L0:4958 → L3:8011 ("negation words promoter") → L16:12358 ("not"+"be-verbs" pattern, direct_effect=+0.334). This feature specifically detects "were not" in the input text ("They **were not** allowed to deforest"), which is the key contradiction signal.

2. **Content Features Present:** The circuit also includes genuine content features:
   - `L0:3498` ("they" pronoun, direct_effect=-0.785) detects the subject pronoun
   - `L15:2080` ("set"+articles, direct_effect=+0.198) detects the action verb from "setting"
   - `L2:4819` ("fire" content, direct_effect=+0.260) detects the object of the action

3. **Partially Validated Concern:** The user's concern is partially correct—the probe heavily relies on negation signals (L16:12358, L4:4492, L3:8011 collectively contribute ~0.64 to the output). However, the circuit also incorporates semantic content ("set", "fire") rather than purely "negation words" signals. The probe appears to classify by detecting the contrast between an action ("they set about clearing") and its negation ("they were not allowed").

4. **Feature Specificity:** The key negation features have relatively low frac_nonzero values (L16:12358: 0.028, L3:8011: 0.003), indicating they are selective detectors rather than generic negation word detectors. L16:12358 specifically encodes "not" followed by be-verbs—precisely the pattern in the input ("were not allowed").

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L0:3498 de=-0.785 |
| 3 | `inspect_feature` ×5 | L0:3498, L3:1101, L3:8011, L16:12358, L15:2080 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L16:F12358@21` | ✅ reported | 9 | 22 | Trace what upstream features feed into L16:12358 (negation pattern detector - "n… |
| SA-2 | `L3:F8011@21` | ✅ reported | 3 | 6 | Trace what upstream features feed into L3:8011 (mix of words and code - promotes… |
| SA-3 | `L0:F3498@2` | ✅ reported | 1 | 3 | Trace what upstream features feed into L0:3498 (pronoun "they" detector). This f… |
| SA-4 | `L15:F2080@3` | ✅ reported | 2308 | 9 | Trace what upstream features feed into L15:2080 (detects "set" + articles/prepos… |

<details>
<summary><b>SA-1</b> — tool trace (14 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L16, F12358 | " the word "not" followed within a few tokens by a form of the verb "to" |
| 2 | `get_upstream_features` | L16:F12358@21, k=5 | Emb:" not"@21 (w=19.00) +4 more |
| 3 | `inspect_feature` | L0, F4958 | " the word "not"" |
| 4 | `inspect_feature` | L2, F12021 | ""not" or negative terms, with some bonus for sports-related terms and " |
| 5 | `inspect_feature` | L15, F10071 | "negations and equivocations" |
| 6 | `get_upstream_features` | L0:F4958@21, k=5 | Emb:" not"@21 (w=33.75) +4 more |
| 7 | `get_upstream_features` | L2:F12021@21, k=5 | Emb:" not"@21 (w=23.12) +4 more |
| 8 | `inspect_feature` | L1, F5108 | "the word "not"" |
| 9 | `inspect_feature` | L0, F9646 | " words that indicate the degree, scale, or validity of something" |
| 10 | `get_upstream_features` | L15:F10071@21, k=5 | Emb:" not"@21 (w=9.81) +4 more |
| 11 | `inspect_feature` | L13, F3295 | "negations in the form of "is/are not" as well as other uses of "not"" |
| 12 | `get_upstream_features` | L13:F3295@21, k=5 | Emb:" not"@21 (w=17.25) +4 more |
| 13 | `inspect_feature` | L3, F8011 | " a mix of words and code fragments from different languages" |
| 14 | `inspect_feature` | L3, F1101 | " error messages and terms indicating absence or negation in software c" |

**Findings:** The circuit for L16:12358 (negation pattern detector for "not" + be-verbs) shows a primarily direct connection to the token embedding for "not" at position 21 (weight: 19.0) and a smaller connection to the "were" token at position 20 (3.6875). The most important intermediate feature is L0:4958, a simple "not" word detector that itself receives strong input from the "not" token embedding (33.75). O…

</details>

<details>
<summary><b>SA-2</b> — tool trace (6 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L3, F8011 | " a mix of words and code fragments from different languages" |
| 2 | `get_upstream_features` | L3:F8011@21, k=5 | Emb:" not"@21 (w=21.75) +4 more |
| 3 | `inspect_feature` | L0, F4958 | " the word "not"" |
| 4 | `inspect_feature` | L0, F7257 | "the word "still"." |
| 5 | `get_upstream_features` | L0:F4958@21, k=5 | Emb:" not"@21 (w=33.75) +4 more |
| 6 | `get_upstream_features` | L0:F7257@21, k=5 | Emb:" were"@20 (w=9.25) +4 more |

**Findings:** The circuit tracing reveals that the negation-promoting feature L3:F8011 primarily gets its signal from the input token "not" at position 21 via two pathways: 1) direct connection from the "not" token embedding (weight 21.75), and 2) through two layer 0 features that detect "not" (F4958) and "still" (F7257). The layer 0 features themselves mainly derive from token embeddings: F4958 gets 33.75 weig…

</details>

<details>
<summary><b>SA-3</b> — tool trace (5 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F3498 | " the pronoun "they" or its possessive form." |
| 2 | `get_upstream_features` | L0:F3498@2, k=5 | Emb:" they"@2 (w=42.75) +4 more |
| 3 | `inspect_feature` | L0, F478 | "various kinds of brackets and parentheses followed by a period" |
| 4 | `inspect_feature` | L0, F517 | "words starting with "ab" followed by another letter" |
| 5 | `get_upstream_features` | L0:F3498@2, k=10 | Emb:" they"@2 (w=42.75) +9 more |

**Findings:** Tracing from L0:3498 ("they" pronoun detector) reveals a simple, direct circuit. The feature is primarily activated by the token embedding " they" at position 2 with a very strong edge_weight of 42.75. There are also minor connections: positive from <bos> token at position 0 (edge_weight 1.0469) and negative from "So" token at position 1 (edge_weight -1.0312). This shows that the "they" detector i…

</details>

<details>
<summary><b>SA-4</b> — tool trace (11 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L15, F2080 | "the phrase "set" followed by articles or prepositions" |
| 2 | `get_upstream_features` | L15:F2080@3, k=5 | Emb:" set"@3 (w=44.50) +4 more |
| 3 | `inspect_feature` | L14, F8363 | " the word "set" followed by prepositions" |
| 4 | `inspect_feature` | L6, F1468 | "variations of the word "set" followed by an article" |
| 5 | `get_upstream_features` | L14:F8363@3, k=5 | Emb:" set"@3 (w=15.44) +4 more |
| 6 | `get_upstream_features` | L6:F1468@3, k=5 | Emb:" set"@3 (w=24.50) +4 more |
| 7 | `inspect_feature` | L2, F10849 | "the word "set"" |
| 8 | `get_upstream_features` | L2:F10849@3, k=5 | Emb:" set"@3 (w=17.12) +4 more |
| 9 | `inspect_feature` | L0, F6066 | "the verb "set" and related words such as "smooth" and "host"" |
| 10 | `inspect_feature` | L0, F13683 | " the word 'set' in mathematical or computer science contexts" |
| 11 | `inspect_feature` | L4, F1712 | "the word "set" or a variation of it." |

**Findings:** The circuit for L15:2080 (detects "set" + articles/prepositions) traces back primarily to the token embedding " set" at position 3. The strongest pathways are:

1. Direct connection from token embedding " set" at pos 3 to L15:2080 (weight 44.5)
2. Indirect pathway: token embedding " set" → L14:8363 (detects "set" + prepositions) → L15:2080 (total weight ~28.8)
3. Another indirect pathway: token em…

</details>

### Re-dispatch (round 2): 1 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-5 | `L4:F4492@21` | ✅ reported | 6 | 7 | Trace what upstream features feed into L4:4492 (positive effect at pos 21). This… |

<details>
<summary><b>SA-5</b> — tool trace (10 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F4492 | "negations in various languages" |
| 2 | `get_upstream_features` | L4:F4492@21, k=5 | Emb:" not"@21 (w=19.12) +4 more |
| 3 | `inspect_feature` | L3, F8011 | " a mix of words and code fragments from different languages" |
| 4 | `get_upstream_features` | L3:F8011@21, k=5 | Emb:" not"@21 (w=21.75) +4 more |
| 5 | `inspect_feature` | L0, F4958 | " the word "not"" |
| 6 | `inspect_feature` | L0, F7257 | "the word "still"." |
| 7 | `inspect_feature` | L3, F1101 | " error messages and terms indicating absence or negation in software c" |
| 8 | `get_upstream_features` | L3:F1101@21, k=5 | Emb:" not"@21 (w=13.75) +4 more |
| 9 | `inspect_feature` | L2, F12021 | ""not" or negative terms, with some bonus for sports-related terms and " |
| 10 | `get_upstream_features` | L2:F12021@21, k=5 | Emb:" not"@21 (w=23.12) +4 more |

**Findings:** The circuit tracing reveals that L4:4492 ("negations in various languages") is primarily driven by the input token " not" at position 21. The strongest connection is direct from the embedding of " not" with weight 19.125. The feature is also positively fed by L3:8011 (detects negation words across languages with weight 5.0625) and negatively fed by L3:1101 and L2:12021 (both detect negation in spe…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L3:F1101@21, k=8 → Emb:" not"@21 (w=13.75) +7 more |
| 2 | `inspect_feature` ×2 | L0:4958, L0:8444 |
| 3 | `get_upstream_features` | L2:F4819@12, k=6 → Emb:" fire"@12 (w=32.00) +5 more |
| 4 | `inspect_feature` | L2, F2952 → " the word "out", and sometimes activates on words relating to legal ca" |

### Build

`build_circuit` → 12 nodes, 12 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m2.7 | 25,575 | 4,825 | 81,944 | 0 | $0.0159 | — | — |
| SA-3 | deepseek/deepseek-v3.2 | 21,884 | 1,461 | 3,264 | 0 | $0.0063 | ✅ 1F/3E | Trace what upstream features feed into L0:3498 (pronoun "the… |
| SA-2 | deepseek/deepseek-v3.2 | 30,220 | 1,592 | 0 | 0 | $0.0085 | ✅ 3F/6E | Trace what upstream features feed into L3:8011 (mix of words… |
| SA-1 | deepseek/deepseek-v3.2 | 96,691 | 4,255 | 10,944 | 0 | $0.0270 | ✅ 9F/22E | Trace what upstream features feed into L16:12358 (negation p… |
| SA-4 | deepseek/deepseek-v3.2 | 63,572 | 3,055 | 8,064 | 0 | $0.0179 | ✅ 2308F/9E | Trace what upstream features feed into L15:2080 (detects "se… |
| SA-5 | deepseek/deepseek-v3.2 | 53,200 | 2,900 | 10,944 | 0 | $0.0152 | ✅ 6F/7E | Trace what upstream features feed into L4:4492 (positive eff… |
| **Total** | | **291,142** | **18,088** | **115,160** | **0** | **$0.0909** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 8m 21s