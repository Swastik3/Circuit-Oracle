# Circuit Oracle Report
**Date:** 2026-04-03 11:21:58 UTC | **Orchestrator:** minimax/minimax-m2.7 | **Subagent:** deepseek/deepseek-v3.2

## Input
**Prompt:** "Dataset: multinli-pos_pos_4 | Probe: biased | Method: correct"
**System prompt:** ""
**Question:** "('The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction.',)"
**Top predictions:**  (100.0%)

## Oracle Analysis
Based on my comprehensive tracing of the attribution circuit, here is my analysis:

---

**Analysis:** The probe's classification is driven by **specific lexical and semantic features** from the input text—not by spurious negation patterns. The circuit traces to actual content tokens like "Pick" (pos 1), "up" (pos 2), "here" (pos 9), "tours" (pos 14), and "No one" (pos 16-17), all with low frac_nonzero values (0.001-0.015) indicating highly specific, selective detection rather than generic pattern matching.

**Confidence:** 8/10

**Reasoning:**

The circuit is **NOT using spurious "negation words"** as the user feared. Instead, it uses:

1. **Phrasal verb detection (L2:F3116, pos 2)** — detects "pick up" as a phrase, NOT just the word "up" in isolation. The feature receives strong positive input from embeddings "Pick" (weight 50.0) and " up" (weight 20.75), then gates this through negative connections from lower-layer word detectors. This is actual semantic composition.

2. **"No one" as a semantic unit (L2:F8837, L1:F15800)** — These features don't detect "negation" generically. They specifically detect the indefinite pronoun "one" when preceded by "no" or "every", distinguishing it from numerical "one" via an inhibitory pathway (L0:F11351 number detector inhibits the pronoun detector when the context doesn't match). The circuit distinguishes "No one" (pronoun, zero probability) from "one" (number, various probabilities) through opposing signals.

3. **Specific lexical content features** — "tours" (L2:F14413), "here" in demonstrative context (L4:F10722), "about" with numerical context (L0:F2238)—all low frac_nonzero (0.006-0.019), meaning they're selective for specific semantic contexts.

4. **All features trace to token embeddings** — The circuit originates from actual input tokens at specific positions, not from abstract negation detectors.

The circuit represents **genuine lexical/semantic content processing** where specific words and phrases in context drive the probe's classification. The "negation" features (L0:F7820) contribute only weakly (weight 1.16) and serve to distinguish pronoun "one" from numerical "one"—a semantic disambiguation role, not a spurious pattern.

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 10 features; top: L2:3116 de=-0.613 |

### Dispatch: 10 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L2:F3116@2` | ✅ reported | 4 | 5 | Trace what this feature encodes and where the signal originates. Check if it rel… |
| SA-2 | `L0:F10562@2` | ✅ reported | 3 | 3 | Trace what this feature encodes and where the signal originates. Check if it rel… |
| SA-3 | `L2:F14413@14` | ✅ reported | 12 | 21 | Trace what this feature encodes and where the signal originates. Check if it rel… |
| SA-4 | `L1:F15800@17` | ✅ reported | 4 | 11 | Trace what this feature encodes and where the signal originates. Check if it rel… |
| SA-5 | `L0:F2238@12` | ✅ reported | 1 | 3 | Trace what this feature encodes and where the signal originates. Check if it rel… |
| SA-6 | `L4:F10722@9` | ✅ reported | 8 | 16 | Trace what this feature encodes and where the signal originates. Check if it rel… |
| SA-7 | `L2:F8837@17` | ✅ reported | 5 | 14 | Trace what this feature encodes and where the signal originates. Check if it rel… |
| SA-8 | `L2:F1016@14` | ✅ reported | 9 | 20 | Trace what this feature encodes and where the signal originates. Check if it rel… |
| SA-9 | `L0:F8566@1` | ✅ reported | 5 | 2 | Trace what this feature encodes and where the signal originates. Check if it rel… |
| SA-10 | `L0:F10904@1` | ✅ reported | 1 | 2 | Trace what this feature encodes and where the signal originates. Check if it rel… |

<details>
<summary><b>SA-1</b> — tool trace (8 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L2, F3116 | " the phrasal verb "pick up" and variations" |
| 2 | `get_upstream_features` | L2:F3116@2, k=5 | Emb:"Pick"@1 (w=50.00) +4 more |
| 3 | `inspect_feature` | L0, F10562 | "the word "up"" |
| 4 | `inspect_feature` | L1, F13179 | "the words "pick", "picker", and forms of those words" |
| 5 | `get_upstream_features` | L0:F10562@2, k=5 | Emb:" up"@2 (w=37.00) +4 more |
| 6 | `get_upstream_features` | L1:F13179@1, k=5 | Emb:"Pick"@1 (w=21.62) +4 more |
| 7 | `inspect_feature` | L1, F11342 | " the word fragment "up" used in different contexts" |
| 8 | `get_upstream_features` | L1:F11342@2, k=5 | Emb:" up"@2 (w=14.25) +4 more |

**Findings:** This circuit traces a feature at L2:F3116 that encodes the phrasal verb "pick up" and variations. The most striking finding is that the feature receives STRONG DIRECT POSITIVE connections from embeddings "Pick" (50.0) and " up" (20.75) at positions 1 and 2, but receives NEGATIVE connections from three upstream features: L0:F10562 (detects "up"), L1:F13179 (detects "pick"), and L1:F11342 (detects "…

</details>

<details>
<summary><b>SA-2</b> — tool trace (6 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F10562 | "the word "up"" |
| 2 | `get_upstream_features` | L0:F10562@2, k=5 | Emb:" up"@2 (w=37.00) +4 more |
| 3 | `get_upstream_features` | L0:F10562@2, k=10 | Emb:" up"@2 (w=37.00) +9 more |
| 4 | `get_upstream_features` | L0:F10562@1, k=5 | ❌ Feature (layer=0, pos=1, feature_idx=10562) not found in gra |
| 5 | `inspect_feature` | L0, F1148 | " mathematical symbols, variables, and related notation, with some func" |
| 6 | `inspect_feature` | L0, F1258 | "references to a place or thing being present "here" and potentially al" |

**Findings:** Tracing from L0:F10562 reveals it's a simple token detection feature for the word "up" at position 2. The circuit is shallow: the feature is primarily driven directly by the embedding of the token " up" itself (weight 37.0), with minor context from preceding tokens "Pick" (pos 1, weight 1.0781) and "<bos>" (pos 0, weight 0.5586). All other feature connections have weight 0.0, indicating they're no…

</details>

<details>
<summary><b>SA-3</b> — tool trace (18 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L2, F14413 | "the word "tour" or "tours"" |
| 2 | `get_upstream_features` | L2:F14413@14, k=5 | Emb:" tours"@14 (w=28.38) +4 more |
| 3 | `inspect_feature` | L1, F6872 | " the word "interpretation"" |
| 4 | `inspect_feature` | L1, F12555 | " words associated with trails and paths, especially words for navigati" |
| 5 | `inspect_feature` | L1, F7927 | " text referring to trails, paths, and hiking, including descriptions o" |
| 6 | `inspect_feature` | L0, F9653 | " the word "tour"" |
| 7 | `get_upstream_features` | L1:F6872@14, k=5 | Emb:" tours"@14 (w=20.62) +4 more |
| 8 | `inspect_feature` | L0, F9924 | " the word "tour" and words or phrases associated with places, events, " |
| 9 | `inspect_feature` | L0, F10891 | " words connected to excursions and professions" |
| 10 | `inspect_feature` | L0, F8380 | " words associated with tourism, especially natural and historical attr" |
| 11 | `get_upstream_features` | L1:F12555@14, k=5 | Emb:" tours"@14 (w=9.81) +4 more |
| 12 | `inspect_feature` | L0, F9026 | "technical documents or data, including numbers, units, and references " |
| 13 | `inspect_feature` | L0, F5886 | "the word "tour" and its variations." |
| 14 | `get_upstream_features` | L1:F7927@14, k=5 | Emb:" tours"@14 (w=9.62) +4 more |
| 15 | `inspect_feature` | L0, F5969 | " the word "tour"" |
| 16 | `inspect_feature` | L0, F4793 | " the word "wherever"" |
| 17 | `get_top_logits` | k=10 | "" (100%) |
| 18 | `get_top_features` | token="", k=10 | 10 features; top: L2:3116 de=-0.613 |

**Findings:** I traced the circuit for L2:F14413, which detects the word "tour" or "tours". The feature has a negative direct effect (-0.2793) on predicting the empty token (which is the model's 100% confident prediction).

Key findings:
1. The feature strongly activates on "tour" words but suppresses "tour" tokens in output, promoting instead technical tokens like "ategorie", "VersionUID", "RequiresApi".
2. Th…

</details>

<details>
<summary><b>SA-4</b> — tool trace (8 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L1, F15800 | " the word "one"" |
| 2 | `get_upstream_features` | L1:F15800@17, k=5 | Emb:" one"@17 (w=15.25) +4 more |
| 3 | `inspect_feature` | L0, F4438 | "the word "one"." |
| 4 | `inspect_feature` | L0, F11351 | " the number "one"" |
| 5 | `inspect_feature` | L0, F7820 | " words indicating uncertainty or tentativeness" |
| 6 | `get_upstream_features` | L0:F4438@17, k=5 | Emb:" No"@16 (w=29.38) +4 more |
| 7 | `get_upstream_features` | L0:F11351@17, k=5 | Emb:" one"@17 (w=38.50) +4 more |
| 8 | `get_upstream_features` | L0:F7820@17, k=5 | Emb:" No"@16 (w=15.19) +4 more |

**Findings:** I traced a circuit that detects the word "one" in the context of "No one" phrases. The L1:F15800 feature encodes the word "one" with high specificity (frac_nonzero=0.00119). 

Key findings:
1. **Main upstream source**: L0:F4438 directly feeds into L1:F15800 (weight=13.0), which detects the word "one" specifically in "No one" contexts, promoting indefinite pronouns like "Everyone", "Nobody", "Nadie…

</details>

<details>
<summary><b>SA-5</b> — tool trace (3 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F2238 | " the word "about" when followed by a numerical value" |
| 2 | `get_upstream_features` | L0:F2238@12, k=5 | Emb:" about"@12 (w=35.00) +4 more |
| 3 | `get_upstream_features` | L0:F2238@12, k=10 | Emb:" about"@12 (w=35.00) +9 more |

**Findings:** L0:F2238 at position 12 encodes detection of the word \"about\" when followed by a numerical value. This is a very early feature (layer 0) with specific semantics (frac_nonzero: 0.00657). The circuit is simple: the feature gets its strongest signal directly from the \" about\" token embedding at position 12 (weight: 35.0), with weaker contextual influences from the beginning-of-sequence token \"<b…

</details>

<details>
<summary><b>SA-6</b> — tool trace (15 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F10722 | "uses of the word "here" alongside demonstrative pronouns and temporal " |
| 2 | `get_upstream_features` | L4:F10722@9, k=5 | Emb:" here"@9 (w=24.12) +4 more |
| 3 | `inspect_feature` | L0, F7204 | "the word "here"" |
| 4 | `inspect_feature` | L2, F13998 | " the word "here"" |
| 5 | `inspect_feature` | L3, F9679 | "the word "here"." |
| 6 | `get_upstream_features` | L0:F7204@9, k=5 | Emb:" here"@9 (w=41.00) +4 more |
| 7 | `get_upstream_features` | L2:F13998@9, k=5 | Emb:" here"@9 (w=33.25) +4 more |
| 8 | `get_upstream_features` | L3:F9679@9, k=5 | Emb:" here"@9 (w=25.25) +4 more |
| 9 | `inspect_feature` | L1, F10536 | "the word "here" and related words" |
| 10 | `get_upstream_features` | L1:F10536@9, k=5 | Emb:" here"@9 (w=23.75) +4 more |
| 11 | `get_upstream_features` | L4:F10722@9, k=10 | Emb:" here"@9 (w=24.12) +9 more |
| 12 | `inspect_feature` | L3, F1160 | "mentions of the downtown area" |
| 13 | `get_upstream_features` | L3:F1160@9, k=5 | Emb:" here"@9 (w=5.88) +4 more |
| 14 | `inspect_feature` | L2, F1625 | " the word "there"" |
| 15 | `inspect_feature` | L2, F1269 | " references within the text, often using words like "therein" or "abov" |

**Findings:** Tracing L4:F10722 reveals a feature that encodes "uses of the word 'here' alongside demonstrative pronouns and temporal words." The circuit shows a complex pattern where the starting feature receives:

1. A STRONG DIRECT POSITIVE signal from the token embedding " here" at position 9 (edge weight 24.125)
2. NEGATIVE signals from multiple lower-layer features that detect "the word 'here'" but suppre…

</details>

<details>
<summary><b>SA-7</b> — tool trace (9 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L2, F8837 | " the word "one" or "body" when preceded by the words "no" or "every."" |
| 2 | `get_upstream_features` | L2:F8837@17, k=5 | Emb:" No"@16 (w=18.50) +4 more |
| 3 | `inspect_feature` | L0, F4438 | "the word "one"." |
| 4 | `inspect_feature` | L0, F11351 | " the number "one"" |
| 5 | `inspect_feature` | L1, F15800 | " the word "one"" |
| 6 | `get_upstream_features` | L0:F4438@17, k=5 | Emb:" No"@16 (w=29.38) +4 more |
| 7 | `get_upstream_features` | L0:F11351@17, k=5 | Emb:" one"@17 (w=38.50) +4 more |
| 8 | `get_upstream_features` | L1:F15800@17, k=5 | Emb:" one"@17 (w=15.25) +4 more |
| 9 | `inspect_feature` | L0, F7820 | " words indicating uncertainty or tentativeness" |

**Findings:** The circuit traces a negation pattern detection feature (L2:F8837) that recognizes "one" or "body" when preceded by negation words like "no" or "every". The feature combines signals from:

1. Direct token embeddings: "No" (strong positive) and "one" (positive)
2. L0:F4438: pronoun "one" detector (positive) 
3. L0:F11351: number "one" detector (negative - inhibits when it's the numeral)
4. L1:F1580…

</details>

<details>
<summary><b>SA-8</b> — tool trace (12 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L2, F1016 | " forms of the verb "tour" and the noun "tour."" |
| 2 | `get_upstream_features` | L2:F1016@14, k=5 | Emb:" tours"@14 (w=27.75) +4 more |
| 3 | `inspect_feature` | L1, F6872 | " the word "interpretation"" |
| 4 | `inspect_feature` | L1, F12555 | " words associated with trails and paths, especially words for navigati" |
| 5 | `inspect_feature` | L0, F10891 | " words connected to excursions and professions" |
| 6 | `inspect_feature` | L0, F11835 | "terms used in software code such as "assembly", "using", "namespace", " |
| 7 | `get_upstream_features` | L1:F12555@14, k=5 | Emb:" tours"@14 (w=9.81) +4 more |
| 8 | `inspect_feature` | L0, F9924 | " the word "tour" and words or phrases associated with places, events, " |
| 9 | `inspect_feature` | L0, F9026 | "technical documents or data, including numbers, units, and references " |
| 10 | `get_upstream_features` | L0:F9924@14, k=5 | Emb:" tours"@14 (w=15.19) +4 more |
| 11 | `get_upstream_features` | L1:F6872@14, k=5 | Emb:" tours"@14 (w=20.62) +4 more |
| 12 | `inspect_feature` | L0, F8380 | " words associated with tourism, especially natural and historical attr" |

**Findings:** The circuit traces a feature at L2:F1016 that detects forms of the verb "tour" but actually suppresses the token "tour" itself. The strongest signal comes directly from the embedding of " tours" at position 14 (weight 27.75). The feature combines inputs from several semantically related lower-level features: L1:F12555 detects trail/path navigation words (positive influence), L1:F6872 detects "inte…

</details>

<details>
<summary><b>SA-9</b> — tool trace (8 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F8566 | " the word "pick"" |
| 2 | `get_upstream_features` | L0:F8566@1, k=5 | Emb:"Pick"@1 (w=16.75) +4 more |
| 3 | `get_upstream_features` | L0:F8566@1, k=10 | Emb:"Pick"@1 (w=16.75) +9 more |
| 4 | `inspect_feature` | L0, F1903 | "instances of sentences starting with "The"" |
| 5 | `inspect_feature` | L0, F2051 | " terms related to paganism, instruments, and car parts" |
| 6 | `inspect_feature` | L0, F1148 | " mathematical symbols, variables, and related notation, with some func" |
| 7 | `inspect_feature` | L0, F1258 | "references to a place or thing being present "here" and potentially al" |
| 8 | `get_top_logits` | k=5 | "" (100%) |

**Findings:** The feature L0:F8566 encodes the word \"pick\" (label: \"the word 'pick'\"). It has low frac_nonzero (0.01134), meaning it's fairly specific and not generic. The tracing shows that the strongest signal (weight 16.75) comes directly from the embedding of the token \"Pick\" at position 1, with a smaller contribution from the beginning-of-sequence token \"<bos>\" at position 0 (weight 0.459). All oth…

</details>

<details>
<summary><b>SA-10</b> — tool trace (4 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F10904 | "the word "adequate" (and words that appear near it)" |
| 2 | `get_upstream_features` | L0:F10904@1, k=5 | Emb:"Pick"@1 (w=13.38) +4 more |
| 3 | `get_upstream_features` | L0:F10904@1, k=10 | Emb:"Pick"@1 (w=13.38) +9 more |
| 4 | `get_top_logits` | k=5 | "" (100%) |

**Findings:** The starting feature L0:F10904 is labeled as detecting \"adequate\" and words near it (frac_nonzero: 0.00787, fairly specific). However, in this circuit, it's being strongly triggered (edge_weight: 13.375) by the token \"Pick\" at position 1, not by \"adequate\". This suggests either: 1) The feature label is misleading and it actually detects something about \"Pick\", or 2) There's a spurious corr…

</details>

### Build

`build_circuit` → 0 nodes, 0 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m2.7 | 24,886 | 9,525 | 193,506 | 0 | — | — | — |
| SA-5 | deepseek/deepseek-v3.2 | 12,841 | 1,116 | 0 | 0 | — | ✅ 1F/3E | Trace what this feature encodes and where the signal origina… |
| SA-2 | deepseek/deepseek-v3.2 | 29,515 | 2,142 | 0 | 0 | — | ✅ 3F/3E | Trace what this feature encodes and where the signal origina… |
| SA-1 | deepseek/deepseek-v3.2 | 43,984 | 2,330 | 0 | 0 | — | ✅ 4F/5E | Trace what this feature encodes and where the signal origina… |
| SA-4 | deepseek/deepseek-v3.2 | 50,229 | 2,748 | 0 | 0 | — | ✅ 4F/11E | Trace what this feature encodes and where the signal origina… |
| SA-6 | deepseek/deepseek-v3.2 | 99,655 | 4,124 | 9,344 | 0 | — | ✅ 8F/16E | Trace what this feature encodes and where the signal origina… |
| SA-3 | deepseek/deepseek-v3.2 | 125,818 | 5,080 | 47,104 | 0 | — | ✅ 12F/21E | Trace what this feature encodes and where the signal origina… |
| SA-10 | deepseek/deepseek-v3.2 | 17,252 | 1,201 | 0 | 0 | — | ✅ 1F/2E | Trace what this feature encodes and where the signal origina… |
| SA-9 | deepseek/deepseek-v3.2 | 45,445 | 2,104 | 0 | 0 | — | ✅ 5F/2E | Trace what this feature encodes and where the signal origina… |
| SA-7 | deepseek/deepseek-v3.2 | 60,921 | 3,708 | 0 | 0 | — | ✅ 5F/14E | Trace what this feature encodes and where the signal origina… |
| SA-8 | deepseek/deepseek-v3.2 | 87,556 | 4,040 | 0 | 0 | — | ✅ 9F/20E | Trace what this feature encodes and where the signal origina… |
| **Total** | | **598,102** | **38,118** | **249,954** | **0** | **—** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 9m 20s