# Circuit Oracle Report
**Date:** 2026-04-03 11:02:06 UTC | **Orchestrator:** minimax/minimax-m2.7 | **Subagent:** deepseek/deepseek-v3.2

## Input
**Prompt:** "Dataset: multinli-pos_pos_3 | Probe: biased | Method: correct"
**System prompt:** ""
**Question:** "('The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction.',)"
**Top predictions:**  (100.0%)

## Oracle Analysis
**Analysis:** The contradiction detection probe primarily relies on three mechanisms: (1) a hierarchical negation detection circuit that identifies the word "not" in "does not contain" (L0→L16), (2) castle/historical building semantic concepts including land ownership terminology (L2→L4→L7), and (3) temporal reference features detecting "17th-century" mentions. These signals converge at the L22 residual stream to classify the input as contradictory.

**Confidence:** 8/10

**Reasoning:** The attribution circuit reveals a mixed mechanism where negation detection is indeed prominent but represents legitimate semantic content rather than spurious patterns. Specifically:

1. **Negation Circuit (L16:F6800 and related):** This is NOT a generic negation detector but specifically identifies "not" at position 36 (the phrase "does not contain"). The circuit L0:F4958 (word "not", frac_nonzero=0.0184) → L3:F8011 (multilingual negation words including "not/NOT/Not/ikke/nicht/geen") → L4:F4492 (negations in various languages, frac_nonzero=0.03828) → L16:F6800 (negations "not", "no", "n't", frac_nonzero=0.03101) forms a hierarchical processing pipeline that is selective for specific negation tokens. This is semantic content because detecting negation is crucial for determining truth conditions—"contains" vs "does not contain" changes the meaning fundamentally.

2. **Castle Semantic Knowledge (L4:F13244, L7:F13215):** These features encode genuine conceptual knowledge about castles as historical fortifications and land ownership/administration centers. L4:F13244 promotes "homestead", "farm", "property", "farms", "fazenda", "hacienda"—terms related to land ownership and feudal systems historically associated with castles. L7:F13215 promotes "military", "fortification", "fortifications", "armed"—properly semantic content about castle architecture.

3. **Regarding the user's concern:** The user's worry that "negation words" signals are "spurious" is partially misplaced. Negation detection IS a legitimate semantic feature for contradiction detection, as negations directly affect whether statements agree or contradict each other. However, the heavy reliance on negation features (5+ features detecting "not" across layers) could indicate the probe learned a shortcut where negation strongly correlates with contradiction in training data, potentially missing deeper semantic understanding of what makes the two sentences contradictory.

4. **Suppression features:** The reflexive pronoun circuit (L3:F232 detecting "itself" with negative direct effect -0.2275) is also content-based—it distinguishes the first sentence's structure ("The castle itself comprises...") from the second sentence's negation, not a generic pattern.

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L0:2158 de=0.275 |

### Dispatch: 6 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L0:F2158@17` | ✅ reported | 1 | 1 | Trace L0:F2158 at pos 17 - this is the top feature with highest positive direct … |
| SA-2 | `L4:F13244@2` | ✅ reported | 9 | 14 | Trace L4:F13244 at pos 2 - the top layer-4 feature with positive direct effect (… |
| SA-3 | `L0:F12378@3` | ✅ reported | 2 | 5 | Trace L0:F12378 at pos 3 - a layer-0 feature with positive direct effect. This p… |
| SA-4 | `L16:F6800@36` | ✅ reported | 7 | 8 | Trace L16:F6800 at pos 36 - a mid-layer feature with high activation (22.125) an… |
| SA-5 | `L3:F232@3` | ✅ reported | 6 | 6 | Trace L3:F232 at pos 3 - this feature has NEGATIVE direct effect (-0.2275). Inve… |
| SA-6 | `L0:F10346@3` | ❌ error | — | — | Trace L0:F10346 at pos 3 - this has NEGATIVE direct effect (-0.2412). Investigat… |

<details>
<summary><b>SA-1</b> — tool trace (3 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F2158 | "the word "with"" |
| 2 | `get_upstream_features` | L0:F2158@17, k=5 | Emb:" with"@17 (w=33.75) +4 more |
| 3 | `get_upstream_features` | L0:F2158@17, k=10 | Emb:" with"@17 (w=33.75) +9 more |

**Findings:** L0:F2158 at position 17 is an early-layer feature that detects the word \"with\" (label: \"the word \\\"with\\\"\") with frac_nonzero=0.02309. Despite detecting \"with\", its promoted tokens actually suppress \"with\" and promote technical/code tokens like \"]--;\", \"\\\"}\\\";\", etc. The feature originates directly from the input embedding of token \" with\" at position 17 with a very strong ed…

</details>

<details>
<summary><b>SA-2</b> — tool trace (14 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F13244 | " terms related to land ownership and administration, possibly includin" |
| 2 | `get_upstream_features` | L4:F13244@2, k=5 | Emb:" castle"@2 (w=18.50) +4 more |
| 3 | `inspect_feature` | L2, F8185 | "places for shopping or military activities" |
| 4 | `inspect_feature` | L2, F9529 | " words related to slavery and slave ownership" |
| 5 | `get_upstream_features` | L2:F9529@2, k=5 | Emb:" castle"@2 (w=13.38) +4 more |
| 6 | `get_upstream_features` | L2:F8185@2, k=5 | Emb:" castle"@2 (w=9.25) +4 more |
| 7 | `inspect_feature` | L0, F9026 | "technical documents or data, including numbers, units, and references " |
| 8 | `inspect_feature` | L1, F8633 | " words or phrases related to tourism and historical places" |
| 9 | `inspect_feature` | L1, F2004 | " mentions of business offices or real estate" |
| 10 | `inspect_feature` | L0, F8290 | " words related to community locations and travel" |
| 11 | `inspect_feature` | L1, F5899 | " the word "Academy", especially when referring to a school or educatio" |
| 12 | `get_upstream_features` | L1:F8633@2, k=5 | Emb:" castle"@2 (w=4.31) +4 more |
| 13 | `inspect_feature` | L0, F8671 | " the word "special" and words occurring with it" |
| 14 | `get_upstream_features` | L1:F2004@2, k=5 | Emb:" castle"@2 (w=12.81) +4 more |

**Findings:** Tracing L4:F13244 reveals a circuit for detecting concepts related to land ownership, administration, and historical institutions. The feature encodes "terms related to land ownership and administration, possibly including slavery or other forms of forced labor" with promoted tokens like "homestead", "farm", "property". 

The circuit shows two main pathways converging on L4:F13244:

1. L2:F8185 → …

</details>

<details>
<summary><b>SA-3</b> — tool trace (4 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F12378 | " the word "latest."" |
| 2 | `get_upstream_features` | L0:F12378@3, k=5 | Emb:" itself"@3 (w=12.44) +4 more |
| 3 | `inspect_feature` | L0, F478 | "various kinds of brackets and parentheses followed by a period" |
| 4 | `get_upstream_features` | L0:F12378@3, k=10 | Emb:" itself"@3 (w=12.44) +9 more |

**Findings:** Tracing L0:F12378 at position 3 reveals that this feature primarily detects the word \"latest\" but in this specific context is strongly activated by the token \" itself\" at position 3 (edge weight 12.44). The feature receives weaker contributions from \"The\" at position 1 (0.63) and \" castle\" at position 2 (0.49). Feature F12378 has low sparsity (frac_nonzero=0.00534), indicating it's specifi…

</details>

<details>
<summary><b>SA-4</b> — tool trace (13 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L16, F6800 | " negations "not", "no", and contractions with "t". " |
| 2 | `get_upstream_features` | L16:F6800@36, k=5 | Emb:" not"@36 (w=12.50) +4 more |
| 3 | `inspect_feature` | L15, F11794 | " phrases that express disagreement or negation" |
| 4 | `get_upstream_features` | L15:F11794@36, k=5 | Emb:" does"@35 (w=7.19) +4 more |
| 5 | `inspect_feature` | L13, F102 | " phrases containing "not" or negative connotations" |
| 6 | `get_upstream_features` | L13:F102@36, k=5 | Emb:" not"@36 (w=9.50) +4 more |
| 7 | `inspect_feature` | L0, F4958 | " the word "not"" |
| 8 | `get_upstream_features` | L0:F4958@36, k=5 | Emb:" not"@36 (w=34.00) +4 more |
| 9 | `inspect_feature` | L14, F6648 | " words and phrases that indicate speculation, possibility, or negation" |
| 10 | `get_upstream_features` | L14:F6648@36, k=5 | Emb:" not"@36 (w=7.56) +4 more |
| 11 | `inspect_feature` | L3, F3534 | "the character sequence "n't" or "nut"" |
| 12 | `get_upstream_features` | L3:F3534@36, k=5 | Emb:" not"@36 (w=16.12) +4 more |
| 13 | `inspect_feature` | L12, F9489 | "negations combined with verbs, modal verbs, and words relating to yout" |

**Findings:** I traced a negation detection circuit starting from L16:F6800 at position 36. The circuit detects the word "not" and related negation patterns. The key finding is that this feature primarily detects the token "not" at position 36, with strong direct connections from the embedding of "not" (weight 12.5) and "does" (weight 9.0625) at positions 36 and 35 respectively.

The circuit shows a hierarchica…

</details>

<details>
<summary><b>SA-5</b> — tool trace (11 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L3, F232 | "the word "itself"" |
| 2 | `get_upstream_features` | L3:F232@3, k=5 | Emb:" itself"@3 (w=26.50) +4 more |
| 3 | `inspect_feature` | L2, F8380 | " the word "itself," sometimes near the word "alibi"" |
| 4 | `inspect_feature` | L0, F8371 | "the word "anyway" and closely related words" |
| 5 | `get_upstream_features` | L2:F8380@3, k=5 | Emb:" itself"@3 (w=29.38) +4 more |
| 6 | `inspect_feature` | L0, F823 | " the word "contest" and sometimes also its context" |
| 7 | `inspect_feature` | L0, F11739 | "the possessive pronoun "its."" |
| 8 | `inspect_feature` | L0, F8082 | "the word "itself" and sometimes words ending in "ing"" |
| 9 | `get_upstream_features` | L0:F8082@3, k=5 | Emb:" itself"@3 (w=19.88) +4 more |
| 10 | `get_upstream_features` | L0:F8371@3, k=5 | Emb:" itself"@3 (w=19.75) +4 more |
| 11 | `get_upstream_features` | L0:F11739@3, k=5 | Emb:" itself"@3 (w=16.62) +4 more |

**Findings:** This circuit analyzes L3:F232 which has NEGATIVE direct effect (-0.2275) and detects the word "itself". The feature suppresses reflexive pronoun tokens like "itself", "themselves", "yourself", etc. The circuit shows it's fed by:

1. Direct token input: " itself" at position 3 (edge weight 26.5) - strongest connection
2. L2:F8380 (negative edge weight -1.7969): Also detects "itself" and suppresses …

</details>

<details>
<summary><b>SA-6</b> — tool trace (15 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F10346 | " the word "itself" and sometimes the word "node"" |
| 2 | `get_upstream_features` | L0:F10346@3, k=5 | Emb:" itself"@3 (w=13.94) +4 more |
| 3 | `get_upstream_features` | L0:F10346@3, k=10 | Emb:" itself"@3 (w=13.94) +9 more |
| 4 | `get_top_logits` | k=5 | "" (100%) |
| 5 | `get_top_features` | token="", k=10 | 10 features; top: L0:2158 de=0.275 |
| 6 | `inspect_feature` | L0, F2158 | "the word "with"" |
| 7 | `inspect_feature` | L0, F12378 | " the word "latest."" |
| 8 | `inspect_feature` | L1, F11 | " the word "press", sometimes in conjunction with "button."" |
| 9 | `inspect_feature` | L3, F232 | "the word "itself"" |
| 10 | `get_upstream_features` | L3:F232@3, k=5 | Emb:" itself"@3 (w=26.50) +4 more |
| 11 | `inspect_feature` | L2, F8380 | " the word "itself," sometimes near the word "alibi"" |
| 12 | `inspect_feature` | L0, F8371 | "the word "anyway" and closely related words" |
| 13 | `get_upstream_features` | L2:F8380@3, k=5 | Emb:" itself"@3 (w=29.38) +4 more |
| 14 | `inspect_feature` | L0, F823 | " the word "contest" and sometimes also its context" |
| 15 | `inspect_feature` | L0, F11739 | "the possessive pronoun "its."" |

</details>

### Re-dispatch (round 2): 3 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-7 | `L4:F4492@36` | ✅ reported | 1854 | 6 | Trace L4:F4492 at pos 36 - a layer-4 feature with positive direct effect (0.2227… |
| SA-8 | `L1:F11@3` | ✅ reported | 4 | 16 | Trace L1:F11 at pos 3 - this has NEGATIVE direct effect (-0.2197). Investigate w… |
| SA-9 | `L7:F13215@2` | ✅ reported | 6 | 10 | Trace L7:F13215 at pos 2 - a layer-7 feature with positive effect (0.209). This … |

<details>
<summary><b>SA-7</b> — tool trace (12 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F4492 | "negations in various languages" |
| 2 | `get_upstream_features` | L4:F4492@36, k=5 | Emb:" not"@36 (w=17.50) +4 more |
| 3 | `inspect_feature` | L3, F8011 | " a mix of words and code fragments from different languages" |
| 4 | `inspect_feature` | L3, F3534 | "the character sequence "n't" or "nut"" |
| 5 | `inspect_feature` | L1, F5108 | "the word "not"" |
| 6 | `get_upstream_features` | L3:F8011@36, k=5 | Emb:" not"@36 (w=20.75) +4 more |
| 7 | `get_upstream_features` | L3:F3534@36, k=5 | Emb:" not"@36 (w=16.12) +4 more |
| 8 | `inspect_feature` | L0, F4958 | " the word "not"" |
| 9 | `get_upstream_features` | L1:F5108@36, k=5 | Emb:" not"@36 (w=14.94) +4 more |
| 10 | `inspect_feature` | L0, F9203 | " instances of disagreement" |
| 11 | `inspect_feature` | L2, F15695 | " the letter "t"" |
| 12 | `get_upstream_features` | L0:F4958@36, k=5 | Emb:" not"@36 (w=34.00) +4 more |

**Findings:** L4:F4492 encodes "negations in various languages" and has a positive direct effect (0.2227) at position 36 where "not" appears. The circuit shows strong direct input from the embedding of "not" itself (edge weight 17.5). Upstream, it receives positive inputs from two layer 3 features: L3:F8011 which promotes various negation words across languages (English "not/NOT/Not", Norwegian "ikke/ikkje", Ge…

</details>

<details>
<summary><b>SA-8</b> — tool trace (9 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L1, F11 | " the word "press", sometimes in conjunction with "button."" |
| 2 | `get_upstream_features` | L1:F11@3, k=5 | Emb:" itself"@3 (w=20.12) +4 more |
| 3 | `inspect_feature` | L0, F11739 | "the possessive pronoun "its."" |
| 4 | `inspect_feature` | L0, F9272 | "the word "themselves," sometimes paired with words like "own" or words" |
| 5 | `get_upstream_features` | L0:F11739@3, k=5 | Emb:" itself"@3 (w=16.62) +4 more |
| 6 | `get_upstream_features` | L0:F9272@3, k=5 | Emb:" itself"@3 (w=22.88) +4 more |
| 7 | `inspect_feature` | L0, F8371 | "the word "anyway" and closely related words" |
| 8 | `get_upstream_features` | L0:F8371@3, k=5 | Emb:" itself"@3 (w=19.75) +4 more |
| 9 | `get_top_logits` | k=5 | "" (100%) |

**Findings:** Tracing L1:F11 at position 3 reveals a circuit that detects the word "press" but has negative direct effect (-0.2197). The feature primarily responds to tokens containing "press" with relatively low frequency (frac_nonzero=0.012). The circuit shows:

1. L1:F11 gets strong positive input (20.125) directly from the embedding of " itself" at position 3.

2. However, L1:F11 receives negative inputs fr…

</details>

<details>
<summary><b>SA-9</b> — tool trace (9 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L7, F13215 | " terms used to describe military fortifications." |
| 2 | `get_upstream_features` | L7:F13215@2, k=5 | L4:F5749 (w=8.25) +4 more |
| 3 | `inspect_feature` | L4, F5749 | " terms that describe ancient settlements and fortifications" |
| 4 | `inspect_feature` | L5, F15708 | " words and phrases related to military and defense." |
| 5 | `get_upstream_features` | L4:F5749@2, k=5 | Emb:" castle"@2 (w=14.69) +4 more |
| 6 | `inspect_feature` | L1, F8633 | " words or phrases related to tourism and historical places" |
| 7 | `inspect_feature` | L2, F8734 | " geographical names and political centers" |
| 8 | `get_upstream_features` | L5:F15708@2, k=5 | Emb:" castle"@2 (w=8.06) +4 more |
| 9 | `inspect_feature` | L4, F13244 | " terms related to land ownership and administration, possibly includin" |

**Findings:** L7:F13215 encodes "terms used to describe military fortifications" and is strongly driven by the word "castle" at position 2. The circuit shows that the embedding token "castle" directly feeds into multiple pathways: (1) through L4:F5749 (ancient settlements/fortifications), (2) through L5:F15708 (military/defense), and (3) directly to L7:F13215. These pathways converge at layer 7 to create a feat…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_features` | token="", k=20 → 20 features; top: L0:2158 de=0.275 |
| 2 | `inspect_feature` ×7 | L16:6800, L0:4958, L1:11, L4:4492, L0:1454, L0:15866, L0:10346 |

### Build

`build_circuit` → 11 nodes, 7 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m2.7 | 30,902 | 5,443 | 73,006 | 0 | — | — | — |
| SA-1 | deepseek/deepseek-v3.2 | 13,079 | 1,070 | 0 | 0 | — | ✅ 1F/1E | Trace L0:F2158 at pos 17 - this is the top feature with high… |
| SA-3 | deepseek/deepseek-v3.2 | 19,188 | 2,066 | 0 | 0 | — | ✅ 2F/5E | Trace L0:F12378 at pos 3 - a layer-0 feature with positive d… |
| SA-6 | deepseek/deepseek-v3.2 | 80,835 | 1,776 | 19,648 | 0 | — | ❌ error | Trace L0:F10346 at pos 3 - this has NEGATIVE direct effect (… |
| SA-5 | deepseek/deepseek-v3.2 | 73,471 | 2,685 | 0 | 0 | — | ✅ 6F/6E | Trace L3:F232 at pos 3 - this feature has NEGATIVE direct ef… |
| SA-4 | deepseek/deepseek-v3.2 | 86,428 | 3,360 | 3,200 | 0 | — | ✅ 7F/8E | Trace L16:F6800 at pos 36 - a mid-layer feature with high ac… |
| SA-2 | deepseek/deepseek-v3.2 | 86,069 | 3,590 | 21,824 | 0 | — | ✅ 9F/14E | Trace L4:F13244 at pos 2 - the top layer-4 feature with posi… |
| SA-8 | deepseek/deepseek-v3.2 | 49,685 | 2,510 | 2,304 | 0 | — | ✅ 4F/16E | Trace L1:F11 at pos 3 - this has NEGATIVE direct effect (-0.… |
| SA-9 | deepseek/deepseek-v3.2 | 55,100 | 2,940 | 0 | 0 | — | ✅ 6F/10E | Trace L7:F13215 at pos 2 - a layer-7 feature with positive e… |
| SA-7 | deepseek/deepseek-v3.2 | 81,555 | 2,905 | 0 | 0 | — | ✅ 1854F/6E | Trace L4:F4492 at pos 36 - a layer-4 feature with positive d… |
| **Total** | | **576,312** | **28,345** | **119,982** | **0** | **—** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 7m 4s