# Circuit Oracle Report
**Date:** 2026-04-03 11:12:37 UTC | **Orchestrator:** minimax/minimax-m2.7 | **Subagent:** deepseek/deepseek-v3.2

## Input
**Prompt:** "Dataset: multinli-pos_pos_3 | Probe: unbiased | Method: correct"
**System prompt:** ""
**Question:** "('The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction.',)"
**Top predictions:**  (100.0%)

## Oracle Analysis
**Analysis:** The probe's classification score is driven by a content-based circuit that detects key semantic entities (castle, tower, house, early) and their associated historical/feudal concepts, NOT by spurious negation word signals. The circuit traces show the strongest positive driver (L4:F13244, 0.2852) encodes "land ownership and administration, possibly including slavery" and originates from the token "castle" at position 2, while the strongest negative driver (L2:F1430, -0.2227) encodes White House/generic house mentions and originates from "house" at position 14 and "tower" at position 13. No negation words (like "not", "does", "doesn't") appear among the top-15 features driving the classification.

**Confidence:** 8/10

**Reasoning:**

The attribution circuit analysis reveals that this probe relies entirely on **content-based features** rather than spurious negation signals:

1. **Top Positive Drivers (Content-Based):**
   - **L4:F13244 (0.2852)** — "terms related to land ownership and administration, possibly including slavery or forced labor" driven by "castle" at pos 2. This feature's frac_nonzero=0.00451 indicates high specificity for historical land-administration concepts.
   - **L0:F2158 (0.1904)** — Detects the word "with" at pos 17
   - **L0:F7360 (0.1592)** — Detects the article "an" at pos 5
   - **L1:F1027 (0.1553)** — Detects "tower" at pos 13, directly from the token embedding
   - **L2:F4429 (0.1377)** — "beginning of a period" at pos 6, driven by "early"
   - **L0:F7513 (0.1318)** — Detects "together" at pos 26

2. **Top Negative Drivers (Content-Based):**
   - **L2:F1430 (-0.2227)** — "White House or generic house" at pos 14, suppresses house-related output tokens. Driven by "house" and modulated by "tower"
   - **L1:F11220 (-0.1475)** — "restore" language, suppresses restoration output. Driven by "restored" at pos 16
   - **L0:F8974 (-0.1226)** — Detects "from" at pos 20

3. **Critical Finding: No Negation Words Detected**
   The user's concern about "spurious negation words signals" is **not supported** by this circuit. None of the top 15 features encode negation words like "not", "does", "doesn't", "contain", or "any". The features are entirely lexical/content-based:
   - Castle → historical/feudal concepts
   - Tower + House → Scottish geographic/political terms, ancient fortifications
   - Early → temporal period detection
   - Restored → restoration language (suppression)

4. **Circuit Structure:**
   The signal flows from input tokens through layer-0 word detectors to layer-1-2 semantic features to layer-4-6 high-level abstractions:
   - "castle" → tourism/historical features (L1) → land ownership/slavery features (L2) → castle_land_ownership (L4)
   - "house" + "tower" → house detection (L1-3) → Scottish political terms (L6)
   - "early" → temporal features (L0-1) → beginning-of-period detection (L2)
   - "restored" → restoration suppression (L1)

5. **Low Sparsity = Specific Content:**
   Most features have low frac_nonzero values (0.001-0.01), indicating they're highly selective and encode specific semantic content rather than generic patterns.

**Conclusion:** The probe detects the contradiction by recognizing that the same key entities (castle, early, 17th-century, tower, house) appear in both sentences, combined with specific semantic features about historical buildings, land ownership, and temporal periods. The mechanism is semantic/content-based, not spurious or negation-based.

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L4:13244 de=0.285 |

### Dispatch: 11 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L4:F13244@2` | ✅ reported | 11 | 12 | Trace this strongest positive driver (L4:F13244, pos=2) upstream. What does this… |
| SA-2 | `L2:F1430@14` | ✅ reported | 5 | 7 | Trace this strongest negative driver (L2:F1430, pos=14) upstream. What does this… |
| SA-3 | `L0:F2158@17` | ✅ reported | 1 | 3 | Trace this strong positive driver (L0:F2158, pos=17) upstream. What does this fe… |
| SA-4 | `L0:F7360@5` | ✅ reported | 1 | 5 | Trace this strong positive driver (L0:F7360, pos=5) upstream. What does this fea… |
| SA-5 | `L0:F8974@20` | ✅ reported | 1 | 1 | Trace this negative driver (L0:F8974, pos=20) upstream. What does this feature e… |
| SA-6 | `L1:F11220@16` | ✅ reported | 4 | 8 | Trace this negative driver (L1:F11220, pos=16) upstream. What does this feature … |
| SA-7 | `L0:F14108@2` | ✅ reported | 1 | 3 | Trace this negative driver (L0:F14108, pos=2) upstream. What does this feature e… |
| SA-8 | `L6:F486@14` | ✅ reported | 8 | 17 | Trace this positive driver (L6:F486, pos=14) upstream. What does this feature en… |
| SA-9 | `L2:F4429@6` | ✅ reported | 7 | 10 | Trace this feature (L2:F4429, pos=6) upstream. What does it encode? |
| SA-10 | `L0:F7513@26` | ✅ reported | 1 | 5 | Trace this feature (L0:F7513, pos=26) upstream. What does it encode? This is nea… |
| SA-11 | `L1:F1027@13` | ✅ reported | 5 | 25 | Trace this feature (L1:F1027, pos=13) upstream. What does it encode? This is the… |

<details>
<summary><b>SA-1</b> — tool trace (16 calls)</summary>

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
| 10 | `get_upstream_features` | L1:F8633@2, k=5 | Emb:" castle"@2 (w=4.31) +4 more |
| 11 | `inspect_feature` | L0, F8671 | " the word "special" and words occurring with it" |
| 12 | `get_upstream_features` | L1:F2004@2, k=5 | Emb:" castle"@2 (w=12.81) +4 more |
| 13 | `inspect_feature` | L0, F8290 | " words related to community locations and travel" |
| 14 | `inspect_feature` | L0, F12312 | " terms and measurements related to scientific and technical processes" |
| 15 | `inspect_feature` | L1, F5899 | " the word "Academy", especially when referring to a school or educatio" |
| 16 | `inspect_feature` | L0, F3636 | " proper nouns, especially names of people and places" |

**Findings:** The circuit trace reveals that L4:F13244 encodes "terms related to land ownership and administration, possibly including slavery or other forms of forced labor" and is primarily driven by the word "castle" at position 2. The strongest connection is directly from the token "castle" itself (edge_weight: 18.5). 

The signal originates from the input token "castle" and flows through two main paths:
1.…

</details>

<details>
<summary><b>SA-2</b> — tool trace (9 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L2, F1430 | "mentions of the U.S. White House or a generic house" |
| 2 | `get_upstream_features` | L2:F1430@14, k=5 | Emb:" house"@14 (w=30.88) +4 more |
| 3 | `inspect_feature` | L1, F12702 | "the word "house" or "homes"" |
| 4 | `inspect_feature` | L1, F1027 | "the word "tower"" |
| 5 | `get_upstream_features` | L1:F12702@14, k=5 | Emb:" house"@14 (w=23.88) +4 more |
| 6 | `inspect_feature` | L0, F10399 | " mentions of steering wheels or driving controls inside automobiles" |
| 7 | `inspect_feature` | L0, F3368 | " mentions of the word "root" in medical contexts, and sometimes any me" |
| 8 | `get_upstream_features` | L1:F1027@13, k=5 | Emb:" tower"@13 (w=23.12) +4 more |
| 9 | `get_top_logits` | k=5 | "" (100%) |

**Findings:** Tracing L2:F1430 (pos=14), which encodes mentions of the U.S. White House or generic houses but SUPPRESSES house-related tokens (promotes foreign/technical terms, suppresses "house", "House", etc.). The circuit analysis reveals:

1. L2:F1430 receives its strongest positive signal directly from the token " house" at position 14 (edge weight 30.875).

2. However, there's an inhibitory path: token " …

</details>

<details>
<summary><b>SA-3</b> — tool trace (3 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F2158 | "the word "with"" |
| 2 | `get_upstream_features` | L0:F2158@17, k=5 | Emb:" with"@17 (w=33.75) +4 more |
| 3 | `get_upstream_features` | L0:F2158@17, k=10 | Emb:" with"@17 (w=33.75) +9 more |

**Findings:** The circuit tracing reveals that L0:F2158 at position 17 is a first-layer feature that detects the word \"with\". Its signal originates almost entirely (edge weight 33.75) from the token embedding of \" with\" at position 17 itself, with minor contextual contributions from the beginning-of-sequence token \"<bos>\" (weight 1.32) and the preceding token \" restored\" at position 16 (weight 1.27). Th…

</details>

<details>
<summary><b>SA-4</b> — tool trace (3 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F7360 | "the word "an" and sometimes also the acronym COX" |
| 2 | `get_upstream_features` | L0:F7360@5, k=5 | Emb:" an"@5 (w=27.38) +4 more |
| 3 | `get_top_logits` | k=5 | "" (100%) |

**Findings:** L0:F7360 at position 5 is a layer 0 feature that encodes the word "an" (and sometimes the acronym COX). It has low sparsity (frac_nonzero=0.0116), meaning it's fairly specific. The feature is strongly driven by the token " an" at position 5 (edge weight 27.375), with weaker influences from surrounding tokens: " comprises" at position 4 (2.98), "<bos>" at position 0 (2.58), " itself" at position 3 …

</details>

<details>
<summary><b>SA-5</b> — tool trace (4 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F8974 | "the word "from"" |
| 2 | `get_upstream_features` | L0:F8974@20, k=5 | Emb:" from"@20 (w=39.75) +4 more |
| 3 | `get_top_logits` | k=5 | "" (100%) |
| 4 | `get_top_features` | token="from", k=10 | ❌ Token 'from' not found in top logits. Available: [''] |

**Findings:** Tracing L0:F8974 (position 20) reveals it's a basic token detector for the word \"from\" at layer 0. The feature has a low frac_nonzero (0.02366), indicating it's fairly specific. Interestingly, while it detects \"from\", it suppresses outputting \"from\" and related tokens, promoting instead various unrelated tokens. The upstream trace shows a very strong direct connection (weight 39.75) from the…

</details>

<details>
<summary><b>SA-6</b> — tool trace (8 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L1, F11220 | "instances of the word "restore" and related words" |
| 2 | `get_upstream_features` | L1:F11220@16, k=5 | Emb:" restored"@16 (w=20.00) +4 more |
| 3 | `inspect_feature` | L0, F11516 | "the word "program" and, to a lesser extent, "bonus"" |
| 4 | `inspect_feature` | L0, F7732 | " the word "materials" and nearby words indicating physical traits and " |
| 5 | `inspect_feature` | L0, F5224 | "the word "restore" or other misspelled versions of the word along with" |
| 6 | `get_upstream_features` | L0:F11516@16, k=5 | Emb:" restored"@16 (w=14.12) +4 more |
| 7 | `get_upstream_features` | L0:F5224@16, k=5 | Emb:" restored"@16 (w=16.25) +4 more |
| 8 | `get_upstream_features` | L0:F7732@16, k=5 | Emb:" restored"@16 (w=8.44) +4 more |

**Findings:** Traced the negative driver L1:F11220 (detects "restore" words but suppresses them) upstream to its primary source: the input token " restored" at position 16. The circuit shows that L1:F11220 is strongly driven by the embedding of " restored" (weight 20.0) and receives weaker inputs from layer 0 features that also detect the " restored" token. Key findings:

1. L1:F11220 detects "restore" related …

</details>

<details>
<summary><b>SA-7</b> — tool trace (5 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F14108 | "the word "appropriate"" |
| 2 | `get_upstream_features` | L0:F14108@2, k=5 | Emb:" castle"@2 (w=11.81) +4 more |
| 3 | `get_upstream_features` | L0:F14108@2, k=10 | Emb:" castle"@2 (w=11.81) +9 more |
| 4 | `get_top_logits` | k=5 | "" (100%) |
| 5 | `get_upstream_features` | L0:F14108@2, k=20 | Emb:" castle"@2 (w=11.81) +19 more |

**Findings:** Tracing L0:F14108 at position 2, which encodes 'the word \"appropriate\"' with frac_nonzero=0.00635. The feature is strongly driven by the embedding of token ' castle' at position 2 (weight=11.8125), with weaker negative influences from 'The' at position 1 and '<bos>' at position 0. The feature promotes punctuation and common words (', \"\n\n\", ględ, \"\", when, ,, of, at, as, but) while suppress…

</details>

<details>
<summary><b>SA-8</b> — tool trace (13 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F486 | " Scottish locations and political terms" |
| 2 | `get_upstream_features` | L6:F486@14, k=5 | L5:F3316 (w=-2.41) +4 more |
| 3 | `inspect_feature` | L5, F3316 | "Irish or Scottish geographical or cultural references, including names" |
| 4 | `inspect_feature` | L4, F13244 | " terms related to land ownership and administration, possibly includin" |
| 5 | `inspect_feature` | L4, F5749 | " terms that describe ancient settlements and fortifications" |
| 6 | `get_upstream_features` | L4:F13244@14, k=5 | Emb:" house"@14 (w=11.38) +4 more |
| 7 | `get_upstream_features` | L4:F5749@14, k=5 | Emb:" tower"@13 (w=10.00) +4 more |
| 8 | `get_upstream_features` | L5:F3316@14, k=5 | Emb:" house"@14 (w=2.69) +4 more |
| 9 | `inspect_feature` | L3, F14368 | "the word "house" (or houses)." |
| 10 | `inspect_feature` | L2, F1430 | "mentions of the U.S. White House or a generic house" |
| 11 | `get_upstream_features` | L3:F14368@14, k=5 | Emb:" house"@14 (w=26.88) +4 more |
| 12 | `inspect_feature` | L1, F12702 | "the word "house" or "homes"" |
| 13 | `inspect_feature` | L0, F9604 | " the word "house" along with words about social class/gatherings" |

**Findings:** The circuit analysis reveals that L6:F486 (encoding "Scottish locations and political terms") is part of a complex feature hierarchy. The key findings:

1. **Main excitatory pathway**: L6:F486 receives strong positive signals from L4:F13244 (land ownership terms) and L4:F5749 (ancient settlements), which both connect directly to the input tokens "house" (pos14) and "tower" (pos13).

2. **Inhibitor…

</details>

<details>
<summary><b>SA-9</b> — tool trace (12 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L2, F4429 | " mentions of the beginning of a period" |
| 2 | `get_upstream_features` | L2:F4429@6, k=5 | Emb:" early"@6 (w=35.25) +4 more |
| 3 | `inspect_feature` | L1, F7313 | "mentions of bike trails or paths." |
| 4 | `get_upstream_features` | L1:F7313@6, k=5 | Emb:" early"@6 (w=17.50) +4 more |
| 5 | `inspect_feature` | L0, F5494 | "the word "early" often related to time" |
| 6 | `inspect_feature` | L0, F15004 | "the word "score" and related words" |
| 7 | `inspect_feature` | L0, F10711 | " the word "probability"" |
| 8 | `get_upstream_features` | L0:F5494@6, k=5 | Emb:" early"@6 (w=21.12) +4 more |
| 9 | `get_upstream_features` | L2:F4429@6, k=10 | Emb:" early"@6 (w=35.25) +9 more |
| 10 | `inspect_feature` | L1, F2520 | "the word "aim"" |
| 11 | `inspect_feature` | L1, F3893 | "the word "typical" and words related to medical implants or prosthetic" |
| 12 | `inspect_feature` | L0, F5391 | " references to the beginning of processes or time periods" |

**Findings:** The circuit traces a feature at L2:F4429 that encodes "mentions of the beginning of a period." This feature is strongly activated by the word "early" (embedding weight 35.25) but paradoxically suppresses output tokens like "early" and "Early". 

The upstream analysis reveals an interesting inhibition pattern: L1 features detecting "bike trails" (F7313), "aim" (F2520), and L0 features detecting sim…

</details>

<details>
<summary><b>SA-10</b> — tool trace (2 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F7513 | "the word "together"" |
| 2 | `get_upstream_features` | L0:F7513@26, k=5 | Emb:" together"@26 (w=43.00) +4 more |

**Findings:** The feature L0:F7513 at position 26 encodes detection of the word \"together\". It has very low sparsity (frac_nonzero=0.007), meaning it's highly specific and only activates on rare contexts containing \"together\". The strongest upstream connection is directly from the embedding of \" together\" at the same position (weight=43.0), confirming it's a direct word detector. Weaker contextual connect…

</details>

<details>
<summary><b>SA-11</b> — tool trace (10 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L1, F1027 | "the word "tower"" |
| 2 | `get_upstream_features` | L1:F1027@13, k=5 | Emb:" tower"@13 (w=23.12) +4 more |
| 3 | `inspect_feature` | L0, F13200 | "mentions of archeology or the history of early civilization." |
| 4 | `inspect_feature` | L0, F10633 | " the word "hill" and words associated with tall structures such as "to" |
| 5 | `inspect_feature` | L0, F4079 | " the words "exposure," "tower" and words related to legal trials" |
| 6 | `get_upstream_features` | L0:F10633@13, k=5 | Emb:" tower"@13 (w=13.31) +4 more |
| 7 | `get_upstream_features` | L0:F4079@13, k=5 | Emb:" tower"@13 (w=19.12) +4 more |
| 8 | `get_upstream_features` | L0:F13200@13, k=5 | Emb:"century"@12 (w=3.38) +4 more |
| 9 | `inspect_feature` | L0, F14398 | " references to distance using the word "mile."" |
| 10 | `get_upstream_features` | L0:F14398@13, k=5 | Emb:" tower"@13 (w=15.25) +4 more |

**Findings:** The tracing reveals that L1:F1027 encodes the word "tower" and has a simple circuit: it primarily receives a strong direct connection (weight 23.125) from the embedding of the token "tower" itself at position 13. This suggests that this layer 1 feature is essentially detecting the raw token "tower" with minimal processing.

Additionally, it receives weaker signals from four layer 0 features:
1. L0…

</details>

### Build

`build_circuit` → 26 nodes, 37 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m2.7 | 39,324 | 6,701 | 39,860 | 0 | — | — | — |
| SA-3 | deepseek/deepseek-v3.2 | 13,150 | 1,298 | 0 | 0 | — | ✅ 1F/3E | Trace this strong positive driver (L0:F2158, pos=17) upstrea… |
| SA-4 | deepseek/deepseek-v3.2 | 12,512 | 1,487 | 0 | 0 | — | ✅ 1F/5E | Trace this strong positive driver (L0:F7360, pos=5) upstream… |
| SA-2 | deepseek/deepseek-v3.2 | 52,752 | 2,775 | 0 | 0 | — | ✅ 5F/7E | Trace this strongest negative driver (L2:F1430, pos=14) upst… |
| SA-1 | deepseek/deepseek-v3.2 | 104,117 | 4,114 | 29,248 | 0 | — | ✅ 11F/12E | Trace this strongest positive driver (L4:F13244, pos=2) upst… |
| SA-5 | deepseek/deepseek-v3.2 | 16,851 | 1,331 | 0 | 0 | — | ✅ 1F/1E | Trace this negative driver (L0:F8974, pos=20) upstream. What… |
| SA-7 | deepseek/deepseek-v3.2 | 22,846 | 2,129 | 0 | 0 | — | ✅ 1F/3E | Trace this negative driver (L0:F14108, pos=2) upstream. What… |
| SA-6 | deepseek/deepseek-v3.2 | 45,099 | 2,840 | 0 | 0 | — | ✅ 4F/8E | Trace this negative driver (L1:F11220, pos=16) upstream. Wha… |
| SA-8 | deepseek/deepseek-v3.2 | 90,352 | 4,116 | 0 | 0 | — | ✅ 8F/17E | Trace this positive driver (L6:F486, pos=14) upstream. What … |
| SA-10 | deepseek/deepseek-v3.2 | 8,923 | 1,409 | 0 | 0 | — | ✅ 1F/5E | Trace this feature (L0:F7513, pos=26) upstream. What does it… |
| SA-11 | deepseek/deepseek-v3.2 | 60,393 | 3,408 | 0 | 0 | — | ✅ 5F/25E | Trace this feature (L1:F1027, pos=13) upstream. What does it… |
| SA-9 | deepseek/deepseek-v3.2 | 79,521 | 3,730 | 10,624 | 0 | — | ✅ 7F/10E | Trace this feature (L2:F4429, pos=6) upstream. What does it … |
| **Total** | | **545,840** | **35,338** | **79,732** | **0** | **—** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 10m 30s