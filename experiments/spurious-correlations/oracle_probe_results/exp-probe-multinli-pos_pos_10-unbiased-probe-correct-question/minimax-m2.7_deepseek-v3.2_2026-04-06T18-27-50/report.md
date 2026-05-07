# Circuit Oracle Report
**Date:** 2026-04-06 18:27:50 UTC | **Orchestrator:** minimax/minimax-m2.7 | **Subagent:** deepseek/deepseek-v3.2

## Input

**Prompt:** "Dataset: multinli-pos_pos_10 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "('The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction.',)"

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score is driven by a MIXTURE of genuine semantic content (detecting "role reversal" concepts) AND significant spurious features (lexical patterns like "strangest"/"-ly" words and irrelevant "now" temporal markers). The user's concern is VALID — the spurious "-ly/strange" detector (L4:F12799) is one of the TOP contributors to the contradiction prediction (direct effect +0.2969), with no semantic relevance to contradiction.

**Confidence:** 9/10

**Reasoning:**

The circuit I built reveals that the probe uses multiple distinct signal types:

**1. SPURIOUS LEXICAL FEATURES (User's concern confirmed):**
- **L4:F12799** ("-ly words with 'odd/strange'"): Activated by "strangest" at position 2, this feature has the 3rd highest direct effect (+0.2969) on the output. It encodes purely lexical patterns — "strangest" contains "-ly" and relates to "strange" — but has ZERO semantic relevance to contradiction detection. This is a classic spurious feature.
- **L4:F5709** (astronomy terms): Irrelevant to contradiction, activated by "now" tokens. Negative direct effect (-0.3711), likely suppressing the output.
- Multiple **"now" detectors** (L0-L4): The input contains "right now" twice, but temporal markers have no semantic bearing on whether two statements contradict each other.

**2. GENUINE SEMANTIC FEATURES:**
- **L4:F7409** ("reverse/inverse/vice versa"): Directly detects "reversal" — the key semantic content. Edge weight from Emb: 25.75.
- **L4:F14368** ("role in systems"): Directly detects "role" — edge weight 12.25. Promoted tokens include "role", "roles", "rôle".
- **L6:F12420** ("artistic elements breaking guidelines"): Receives input from "role" + "reversal" tokens, suggesting higher-level abstraction.
- **L8:F16033** ("reversals of fortune"): Highest layer semantic feature, integrating reversal concepts.

**3. NEGATION FEATURE:**
- **L3:F12079** ("negations and Chinese names"): Has positive direct effect (+0.2324), but this is relatively modest compared to the spurious "strangest" feature.

**Circuit Structure Summary:**
The signal flows from token embeddings → early layer detectors → mid-layer semantic features → output. Both the spurious "strangest" feature AND genuine "role/reversal" features converge on the output node. The spurious feature's high direct effect (+0.2969) compared to the negation feature (+0.2324) demonstrates that lexical artifacts are contributing substantially to the classification, confirming the user's concern that the probe relies on spurious correlations rather than proper semantic understanding of contradiction.

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L4:5709 de=-0.371 |
| 3 | `inspect_feature` ×6 | L4:5709, L6:12420, L4:12799, L2:16097, L0:6013, L0:6051 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L4:F12799@2` | ✅ reported | 5 | 8 | Trace this feature encoding "words ending in -ly" with "odd/strange" related wor… |
| SA-2 | `L0:F6013@3` | ✅ reported | 2 | 2 | Trace this feature encoding the word "role". The input contains "role reversal" … |
| SA-3 | `L4:F5709@9` | ✅ reported | 8 | 21 | Trace this astronomy-related feature with high negative direct effect. Find what… |
| SA-4 | `L4:F6072@9` | ✅ reported | 6 | 11 | Trace this feature at pos 9 with positive direct effect. Check if it relates to … |

<details>
<summary><b>SA-1</b> — tool trace (10 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F12799 | " words ending in "-ly" along with phrases that contain the word 'odd' " |
| 2 | `get_upstream_features` | L4:F12799@2, k=5 | Emb:" strangest"@2 (w=31.00) +4 more |
| 3 | `inspect_feature` | L3, F8960 | " words related to how other people are perceived" |
| 4 | `inspect_feature` | L2, F10827 | " words that reflect strikingness or emotional impact" |
| 5 | `get_upstream_features` | L3:F8960@2, k=5 | Emb:" strangest"@2 (w=11.75) +4 more |
| 6 | `get_upstream_features` | L2:F10827@2, k=5 | Emb:" strangest"@2 (w=10.94) +4 more |
| 7 | `inspect_feature` | L0, F12381 | " the words "lowest" and "highest"" |
| 8 | `get_upstream_features` | L4:F12799@2, k=10 | Emb:" strangest"@2 (w=31.00) +9 more |
| 9 | `inspect_feature` | L1, F15749 | " the word "strange", or related words" |
| 10 | `get_upstream_features` | L1:F15749@2, k=5 | Emb:" strangest"@2 (w=11.94) +4 more |

**Findings:** Tracing reveals that L4:F12799 (encoding "words ending in -ly" with "odd/strange" words) is primarily driven by the direct token embedding of " strangest" at position 2 (weight: 31.0). The circuit shows both excitatory and inhibitory pathways:

1. Direct strong excitation from the "strangest" token itself
2. Inhibitory features at L3:F8960 and L1:F15749 that also detect "strange" words but suppres…

</details>

<details>
<summary><b>SA-2</b> — tool trace (4 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F6013 | "the word "role," sometimes in conjunction with words that make it abst" |
| 2 | `get_upstream_features` | L0:F6013@3, k=5 | Emb:" role"@3 (w=15.62) +4 more |
| 3 | `inspect_feature` | L0, F478 | "various kinds of brackets and parentheses followed by a period" |
| 4 | `get_upstream_features` | L0:F6013@3, k=10 | Emb:" role"@3 (w=15.62) +9 more |

**Findings:** The feature L0:F6013 at position 3 is a simple token detector for the word \"role\". It directly connects to the token embedding for \" role\" with a strong edge weight of 15.625, indicating it's primarily triggered by the token itself. The feature has low sparsity (frac_nonzero=0.02879), meaning it's specific to the word \"role\" and doesn't fire broadly. Other upstream connections have edge weig…

</details>

<details>
<summary><b>SA-3</b> — tool trace (14 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F5709 | "astronomy terms" |
| 2 | `get_upstream_features` | L4:F5709@9, k=5 | Emb:" now"@9 (w=40.25) +4 more |
| 3 | `inspect_feature` | L0, F5232 | " the word "now"" |
| 4 | `inspect_feature` | L3, F7449 | " the word "now" often in the context of describing current situations" |
| 5 | `inspect_feature` | L3, F1438 | "the word "now"" |
| 6 | `inspect_feature` | L2, F3705 | " references to particular years or seasons." |
| 7 | `get_upstream_features` | L0:F5232@9, k=5 | Emb:" now"@9 (w=34.50) +4 more |
| 8 | `get_upstream_features` | L3:F7449@9, k=5 | Emb:" now"@9 (w=23.00) +4 more |
| 9 | `get_upstream_features` | L3:F1438@9, k=5 | Emb:" right"@8 (w=5.38) +4 more |
| 10 | `get_upstream_features` | L2:F3705@9, k=5 | Emb:" now"@9 (w=16.75) +4 more |
| 11 | `inspect_feature` | L0, F5188 | " the word "now"" |
| 12 | `inspect_feature` | L2, F4983 | " the word "now"" |
| 13 | `get_upstream_features` | L2:F4983@9, k=5 | Emb:" now"@9 (w=22.50) +4 more |
| 14 | `inspect_feature` | L0, F13522 | " the word "speed" and related words about definition and measurement" |

**Findings:** The tracing reveals a complex pattern for the astronomy feature at L4:F5709. The key finding is that this astronomy feature receives STRONG POSITIVE input directly from the token embedding " now" at position 9 (weight: 40.25), but is simultaneously INHIBITED by several early-layer features that detect the word "now":

1. L0:5232 - a feature that detects "now" (weight: -4.3125)
2. L3:7449 - detects…

</details>

<details>
<summary><b>SA-4</b> — tool trace (10 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F6072 | " the word "now" followed by a verb" |
| 2 | `get_upstream_features` | L4:F6072@9, k=5 | Emb:" now"@9 (w=49.75) +4 more |
| 3 | `inspect_feature` | L0, F5232 | " the word "now"" |
| 4 | `inspect_feature` | L2, F4983 | " the word "now"" |
| 5 | `inspect_feature` | L3, F7449 | " the word "now" often in the context of describing current situations" |
| 6 | `get_upstream_features` | L4:F6072@9, k=10 | Emb:" now"@9 (w=49.75) +9 more |
| 7 | `inspect_feature` | L2, F3705 | " references to particular years or seasons." |
| 8 | `get_upstream_features` | L0:F5232@9, k=5 | Emb:" now"@9 (w=34.50) +4 more |
| 9 | `get_upstream_features` | L2:F3705@9, k=5 | Emb:" now"@9 (w=16.75) +4 more |
| 10 | `inspect_feature` | L0, F5188 | " the word "now"" |

**Findings:** The circuit tracing reveals that L4:F6072 (detecting "the word 'now' followed by a verb") is primarily driven by the token embedding " now" at position 9 with an extremely strong weight of 49.75. The feature is inhibited by several other "now" detectors in earlier layers (L0:F5232, L2:F4983, L3:F7449) with negative weights, suggesting competition or specialization between different "now" detectors…

</details>

### Re-dispatch (round 2): 2 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-5 | `L6:F12420@4` | ✅ reported | 8 | 15 | Trace this artistic/guideline-breaking feature at pos 4. Find what semantic cont… |
| SA-6 | `L4:F7409@4` | ✅ reported | 3 | 5 | Trace this feature encoding "reverse", "inverse", "vice versa" - clearly semanti… |

<details>
<summary><b>SA-5</b> — tool trace (12 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F12420 | " artistic elements that break established guidelines" |
| 2 | `get_upstream_features` | L6:F12420@4, k=5 | Emb:" role"@3 (w=5.59) +4 more |
| 3 | `inspect_feature` | L4, F14368 | " words related to importance or roles in a system" |
| 4 | `inspect_feature` | L5, F9068 | "words and phrases related to populations" |
| 5 | `inspect_feature` | L4, F7409 | " words like "vice versa", "inverse", "reverse", "around", or direction" |
| 6 | `get_upstream_features` | L4:F14368@4, k=5 | Emb:" role"@3 (w=12.25) +4 more |
| 7 | `get_upstream_features` | L5:F9068@4, k=5 | Emb:" reversal"@4 (w=3.02) +4 more |
| 8 | `inspect_feature` | L0, F9026 | "technical documents or data, including numbers, units, and references " |
| 9 | `inspect_feature` | L3, F1688 | "a variety of seemingly unrelated capitalized words, abbreviations and " |
| 10 | `inspect_feature` | L3, F1823 | " the word "role"" |
| 11 | `inspect_feature` | L4, F12799 | " words ending in "-ly" along with phrases that contain the word 'odd' " |
| 12 | `get_upstream_features` | L4:F7409@4, k=5 | Emb:" reversal"@4 (w=25.75) +4 more |

**Findings:** I traced the circuit for the artistic/guideline-breaking feature at L6:F12420. The key finding is that this feature detecting "artistic elements that break established guidelines" is primarily driven by the input tokens "role" (pos 3) and "reversal" (pos 4). 

The main circuit has two parallel paths:
1. Direct embedding connection: "role" → L6:F12420 (strongest connection: weight 5.5938)
2. Two-la…

</details>

<details>
<summary><b>SA-6</b> — tool trace (6 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F7409 | " words like "vice versa", "inverse", "reverse", "around", or direction" |
| 2 | `get_upstream_features` | L4:F7409@4, k=5 | Emb:" reversal"@4 (w=25.75) +4 more |
| 3 | `inspect_feature` | L3, F12544 | " legal and military terminology, and words indicating opposition or ch" |
| 4 | `inspect_feature` | L2, F3690 | " words related to collaboration or separation, in technical contexts." |
| 5 | `get_upstream_features` | L3:F12544@4, k=5 | Emb:" reversal"@4 (w=15.38) +4 more |
| 6 | `get_upstream_features` | L2:F3690@4, k=5 | Emb:" reversal"@4 (w=10.69) +4 more |

**Findings:** Successfully traced the feature encoding "reverse", "inverse", "vice versa" back to token embeddings. The circuit shows that the L4:F7409 feature at position 4 is directly and strongly driven by the input token " reversal" at position 4 (edge weight: 25.75). This confirms that the semantic concept of reversal is encoded starting from the actual token "reversal" in the input. 

Interestingly, there…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` ×3 | L2:10705, L4:14368, L7:905 |
| 2 | `get_upstream_features` | L4:F14368@4, k=8 → Emb:" role"@3 (w=12.25) +7 more |
| 3 | `get_upstream_features` | L2:F10705@11, k=8 → Emb:" concerns"@11 (w=25.75) +7 more |
| 4 | `inspect_feature` ×2 | L3:12079, L8:16033 |

### Build

`build_circuit` → 16 nodes, 21 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m2.7 | 38,099 | 5,342 | 90,013 | 0 | $0.0205 | — | — |
| SA-2 | deepseek/deepseek-v3.2 | 18,705 | 1,395 | 0 | 0 | $0.0054 | ✅ 2F/2E | Trace this feature encoding the word "role". The input conta… |
| SA-1 | deepseek/deepseek-v3.2 | 57,105 | 3,139 | 5,696 | 0 | $0.0162 | ✅ 5F/8E | Trace this feature encoding "words ending in -ly" with "odd/… |
| SA-4 | deepseek/deepseek-v3.2 | 58,625 | 3,035 | 5,184 | 0 | $0.0165 | ✅ 6F/11E | Trace this feature at pos 9 with positive direct effect. Che… |
| SA-3 | deepseek/deepseek-v3.2 | 93,867 | 4,079 | 10,048 | 0 | $0.0262 | ✅ 8F/21E | Trace this astronomy-related feature with high negative dire… |
| SA-5 | deepseek/deepseek-v3.2 | 84,275 | 3,345 | 0 | 0 | $0.0232 | ✅ 8F/15E | Trace this artistic/guideline-breaking feature at pos 4. Fin… |
| SA-6 | deepseek/deepseek-v3.2 | 30,095 | 1,654 | 0 | 0 | $0.0085 | ✅ 3F/5E | Trace this feature encoding "reverse", "inverse", "vice vers… |
| **Total** | | **380,771** | **21,989** | **110,941** | **0** | **$0.1165** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 7m 29s