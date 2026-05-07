# Circuit Oracle Report
**Date:** 2026-03-26 18:16:58 UTC | **Orchestrator:** anthropic/claude-opus-4.6 | **Subagent:** anthropic/claude-sonnet-4.6

## Input
**Prompt:** "Dataset: bib_journalist_dietitian-pos_pos_2 | Probe: unbiased | Method: correct"
**System prompt:** ""
**Concern:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."
**Top predictions:**  (100.0%)

## Oracle Analysis
## Analysis

**Analysis:** This probe classifies a profession (likely "travel agent/planner") using a mixed circuit that combines genuine profession-relevant lexical features with spurious gender-marker features, confirming the user's concern about spurious correlations.

**Confidence:** High

**Reasoning:**

### The Circuit's Three Signal Pathways

The probe's classification score is driven by three distinct signal pathways, with strikingly different semantic relevance:

---

#### 1. **Genuine Profession Indicators (moderate positive effects)**
These features detect semantically relevant content:

- **"side hustle" compound** (L3:3222 at pos 11): The single strongest feature (+0.166 direct effect). Fed by the raw embeddings of "side" (pos 10, edge weight +24) and "hustle" (pos 11), plus L2:6966 ("business & finance" at pos 11, frac_nonzero=0.012). This compositional detection of an entrepreneurial concept is genuinely profession-relevant.

- **"planning" detectors** (L0:14323 → L1:6546 → L2:9024 at pos 43): A clean 3-layer lexical cascade with +0.068 direct effect, all tracing to the raw "planning" token embedding (weight=26.6). Highly specific (frac_nonzero=0.011).

- **"travel" detectors** (L1:9665, L2:8284 at pos 44): Early-layer travel word detectors with positive effects (+0.071, +0.081). Purely lexical, tracing directly to the "travel" token embedding (weight=28.5).

Together, these profession features contribute approximately **+0.40** to the probe score — the largest share.

---

#### 2. **Gender/Pronoun Features (spurious, mixed effects — net positive)**
These features detect the pronoun "she" at position 5 and have NO legitimate connection to the profession being classified:

- **L0:12519** ("she" pronoun, frac_nonzero=0.039): +0.126 direct effect
- **L1:7244** ("she" pronoun, frac_nonzero=0.012): +0.090 direct effect  
- **L0:9040** (third-person singular pronoun, frac_nonzero=0.019): +0.069 direct effect
- **L6:11646** ("references to women", frac_nonzero=0.020): **−0.139** direct effect

The gender features at L0-L1 provide a **net positive contribution of ~+0.146** after subtracting the L6 inhibitory feature. This is substantial — nearly as large as the single strongest profession feature. All of these trace to a single root: the raw "she" token embedding at pos 5 (edge weights 24-39), forming a pure token-identity circuit with zero contextual reasoning.

Critically, these features' promoted/suppressed tokens reveal they are generic anti-repetition features (L0:12519 suppresses "she" and promotes "I", "He", "It"), not profession-specific detectors. Their contribution to the probe score is a **spurious correlation** — the training data likely contained gender-skewed profession labels (e.g., travel agents being predominantly female in training data).

---

#### 3. **Narrative Context Features (mixed, potentially spurious)**
Features detecting general narrative context words:

- **L0:11182** ("until", pos 1): +0.085 — narrative framing
- **L0:2238** ("about", pos 18): +0.097 — generic word  
- **L0:5912** ("year", pos 3): −0.122 — generic temporal word
- **L0:2318** ("never", pos 7): −0.136 — negation word
- **L4:12637** ("undesirable/wrong", pos 12): +0.091 — a negation-context feature fed by "never" through L1:14233 (negation markers)

These features detect narrative/temporal structure ("Until this year, she had never...") that happens to correlate with profession-narrative stories in training data, but are not genuine profession indicators.

---

### Addressing the User's Concern: Is the Probe Using Spurious Features?

**Yes, substantially.** Quantifying the contributions:

| Signal Type | Net Contribution | Key Features |
|---|---|---|
| **Profession-relevant** ("side hustle", "travel", "planning") | ~+0.40 | L3:3222, L2:8284, L1:9665, L2:9024 |
| **Gender markers** ("she" pronoun) | ~+0.15 | L0:12519, L1:7244, L0:9040, minus L6:11646 |
| **Narrative context** ("until", "year", "never", "about") | ~−0.10 | L0:11182, L0:5912, L0:2318, L0:2238 |

Gender features account for roughly **25-30% of the positive signal** driving the classification. The probe has learned a statistical shortcut: the "she" pronoun is correlated with certain professions in training data (likely travel agent/planner), and the probe exploits this gender signal as supplementary evidence alongside the genuine profession indicators.

However, the circuit is **not entirely spurious** — the dominant signal does come from genuine profession indicators ("side hustle" at +0.166 is the single largest feature). The model primarily relies on lexical detection of profession-relevant vocabulary through shallow, embedding-driven circuits (layers 0-3), with gender features providing a secondary boost.

### Interesting Anomaly: Travel Features with Negative Effect
The late-layer travel features (L14:9301, L15:7803) actually have a **negative** effect (−0.086), despite being highly specific travel detectors (frac_nonzero=0.004). This suggests the probe's target class may not be "travel" per se but a more specific profession label, and the deeper semantic "travel concept" representation (as opposed to the raw lexical "travel" token) may carry associations that compete with the classification target. The early-layer (L0-L2) lexical detectors help the classification, but the more abstract, compositional travel-concept features in later layers hurt it.

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L3:3222 de=0.166 |
| 3 | `inspect_feature` ×20 | L3:3222, L0:6051, L6:11646, L0:2318, L3:12282, L0:12519, L0:5912, L0:2402, L0:2238, L4:12637, L1:7244, L15:7803, L0:11182, L2:8284, L2:6966, L1:9665, L0:9040, L0:12289, L2:9024, L4:10359 |

### Dispatch: 7 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L3:F3222@11` | ✅ reported | 7 | 10 | Trace the strongest positive-effect feature L3:3222 at pos 11 ("side hustle" are… |
| SA-2 | `L6:F11646@5` | ✅ reported | 7 | 18 | Trace L6:11646 at pos 5 — a 'references to women' feature triggered by 'she'. Th… |
| SA-3 | `L15:F7803@44` | ✅ reported | 12 | 15 | Trace L15:7803 at pos 44 — a 'travel-related' feature. This has a NEGATIVE effec… |
| SA-4 | `L1:F7244@5` | ✅ reported | 4 | 12 | Trace L1:7244 at pos 5 — 'she' pronoun feature with POSITIVE effect (+0.090). Un… |
| SA-5 | `L2:F8284@44` | ✅ reported | 4 | 8 | Trace L2:8284 at pos 44 — 'travel' word feature with POSITIVE effect (+0.081). U… |
| SA-6 | `L2:F9024@43` | ✅ reported | 6 | 8 | Trace L2:9024 at pos 43 — 'planning' word feature with POSITIVE effect (+0.068).… |
| SA-7 | `L4:F12637@12` | ✅ reported | 8 | 8 | Trace L4:12637 at pos 12 — 'words indicating undesirable/wrong' with POSITIVE ef… |

<details>
<summary><b>SA-1</b> — tool trace (10 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L3, F3222 | " numerical references, especially those including hyphens, and words e" |
| 2 | `get_upstream_features` | L3:F3222@11, k=8 | Emb:" side"@10 (w=24.00) +7 more |
| 3 | `inspect_feature` | L2, F6966 | " words related to business and finance" |
| 4 | `inspect_feature` | L1, F745 | " the word "side"" |
| 5 | `inspect_feature` | L1, F5624 | " names of people, places, and institutions" |
| 6 | `inspect_feature` | L0, F9022 | " technical words used in computing, science, or engineering" |
| 7 | `get_upstream_features` | L2:F6966@11, k=6 | Emb:" hustle"@11 (w=6.91) +5 more |
| 8 | `get_upstream_features` | L1:F745@10, k=6 | Emb:" side"@10 (w=29.12) +5 more |
| 9 | `inspect_feature` | L0, F1447 | "the word "stop"" |
| 10 | `inspect_feature` | L0, F8409 | "technical or jargonistic terms that are specific to certain fields." |

**Findings:** ## Circuit Trace: L3:F3222 at pos 11 ("side hustle")

### Target Feature (L3:F3222)
- **Label**: "numerical references, especially hyphens, and words ending in 'chain'"
- **frac_nonzero**: 0.00381 — extremely sparse/specific
- This feature appears contextually mis-labeled (by autointerp) but fires here due to the "side hustle" compound structure

---

### Primary Upstream Path — Raw Embedding Domi…

</details>

<details>
<summary><b>SA-2</b> — tool trace (13 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F11646 | " references to women, potentially triggered by pronouns and titles" |
| 2 | `get_upstream_features` | L6:F11646@5, k=6 | Emb:" she"@5 (w=32.50) +5 more |
| 3 | `inspect_feature` | L4, F7864 | "xml or source code snippets, especially tags and possibly keywords in " |
| 4 | `inspect_feature` | L0, F12519 | " the pronoun "she"" |
| 5 | `inspect_feature` | L1, F4232 | " the possessive pronoun "her"" |
| 6 | `inspect_feature` | L2, F899 | " language related to arts, crafts, blogs and medical situations" |
| 7 | `get_upstream_features` | L4:F7864@5, k=6 | Emb:" she"@5 (w=26.88) +5 more |
| 8 | `get_upstream_features` | L0:F12519@5, k=6 | Emb:" she"@5 (w=39.00) +5 more |
| 9 | `inspect_feature` | L2, F8966 | " the pronoun "she"" |
| 10 | `get_upstream_features` | L1:F4232@5, k=6 | Emb:" she"@5 (w=30.75) +5 more |
| 11 | `inspect_feature` | L0, F7509 | " female pronouns and words like daughter and husband that refer to wom" |
| 12 | `get_upstream_features` | L2:F8966@5, k=5 | Emb:" she"@5 (w=33.25) +4 more |
| 13 | `inspect_feature` | L1, F7244 | "the pronoun "she"" |

**Findings:** ## Circuit Summary: Why L6:F11646 ("references to women") Pushes AGAINST the Classification

### Root Cause: The " she" Token Embedding is the Overwhelmingly Dominant Driver

The single token embedding for " she" at pos 5 drives the entire circuit with direct edge weights of 26.5–39.0 to every feature in the chain. Everything originates here.

### The Paradox of Self-Suppressing Gender Features

T…

</details>

<details>
<summary><b>SA-3</b> — tool trace (16 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L15, F7803 | " words and phrases related to traveling" |
| 2 | `get_upstream_features` | L15:F7803@44, k=6 | Emb:" travel"@44 (w=37.00) +5 more |
| 3 | `inspect_feature` | L14, F9301 | "words associated with travel and movement" |
| 4 | `inspect_feature` | L3, F2523 | " sentences describing movement or speed" |
| 5 | `inspect_feature` | L6, F7138 | " mentions of vacations or holidays" |
| 6 | `get_upstream_features` | L14:F9301@44, k=5 | Emb:" travel"@44 (w=12.38) +4 more |
| 7 | `get_upstream_features` | L3:F2523@44, k=5 | Emb:" travel"@44 (w=20.88) +4 more |
| 8 | `inspect_feature` | L7, F6906 | " words and phrases related to travel" |
| 9 | `inspect_feature` | L4, F14856 | " the word "travel" and similar-sounding parts of words" |
| 10 | `inspect_feature` | L2, F9365 | " words related to air travel and migration" |
| 11 | `inspect_feature` | L4, F5937 | " words and phrases related to travel, especially internationally for l" |
| 12 | `get_upstream_features` | L2:F9365@44, k=5 | Emb:" travel"@44 (w=12.50) +4 more |
| 13 | `inspect_feature` | L1, F9665 | " any form of the word "travel"" |
| 14 | `inspect_feature` | L0, F1308 | " the word "travel" and its variations." |
| 15 | `inspect_feature` | L1, F5936 | " code or configuration snippets related to XML files" |
| 16 | `inspect_feature` | L0, F5346 | "words semantically similar to 'travel' and 'experiment'" |

**Findings:** ## Circuit Summary: Why L15:F7803 ("travel-related") Has a NEGATIVE Probe Effect

### The Core Feature (L15:7803)
- Highly specific travel lexicon detector (frac_nonzero=0.00417, very sparse)
- Strongly promotes travel vocabulary tokens: "travel", "travelling", "travelers", etc.
- Primarily driven by the raw " travel" token embedding (edge_weight=37.0, by far the dominant input)

### Why It Has a …

</details>

<details>
<summary><b>SA-4</b> — tool trace (8 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L1, F7244 | "the pronoun "she"" |
| 2 | `get_upstream_features` | L1:F7244@5, k=8 | Emb:" she"@5 (w=24.12) +7 more |
| 3 | `inspect_feature` | L0, F12519 | " the pronoun "she"" |
| 4 | `inspect_feature` | L0, F9040 | " instances of the third-person singular pronoun, especially at the sta" |
| 5 | `inspect_feature` | L0, F2241 | " the pronoun "she"" |
| 6 | `get_upstream_features` | L0:F12519@5, k=6 | Emb:" she"@5 (w=39.00) +5 more |
| 7 | `get_upstream_features` | L0:F2241@5, k=6 | Emb:" she"@5 (w=8.62) +5 more |
| 8 | `get_upstream_features` | L0:F9040@5, k=6 | Emb:","@4 (w=7.88) +5 more |

**Findings:** ## Circuit Summary: L1:F7244 — "she" Pronoun Feature (pos 5)

### What the Feature Represents
L1:F7244 is a **highly specific** (frac_nonzero=0.012), early-layer feature that detects the feminine pronoun "she". It suppresses direct she-token logits (typical of transcoder polysemanticity / inhibitory roles in later layers) and fires strongly on its exact token input.

### Dominant Input: Raw Token …

</details>

<details>
<summary><b>SA-5</b> — tool trace (6 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L2, F8284 | "the word "travel" and its related forms" |
| 2 | `get_upstream_features` | L2:F8284@44, k=5 | Emb:" travel"@44 (w=28.50) +4 more |
| 3 | `inspect_feature` | L0, F3158 | "plural nouns related to people or measurement" |
| 4 | `inspect_feature` | L0, F11440 | " LaTeX commands for including packages in a document" |
| 5 | `inspect_feature` | L1, F5936 | " code or configuration snippets related to XML files" |
| 6 | `get_upstream_features` | L0:F3158@44, k=5 | Emb:" travel"@44 (w=16.88) +4 more |

**Findings:** ## Circuit Trace Summary: L2:F8284 "travel word feature"

### Core Finding
The L2:F8284 "travel" detection feature is **almost entirely driven by the raw token embedding of " travel" at position 44**. The dominant edge weight is 28.5 — roughly 13× larger than the next-strongest input (BOS embedding at 2.0), confirming this is a highly direct, token-identity-driven circuit.

### Circuit Structure
1…

</details>

<details>
<summary><b>SA-6</b> — tool trace (9 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L2, F9024 | " the word "planning"" |
| 2 | `get_upstream_features` | L2:F9024@43, k=5 | Emb:" planning"@43 (w=26.62) +4 more |
| 3 | `inspect_feature` | L1, F6546 | "the word "planning"" |
| 4 | `inspect_feature` | L1, F3604 | " verbs in scientific or technical writing, especially those describing" |
| 5 | `inspect_feature` | L0, F14054 | " the word "plan", and weakly also the word "center" and "plus"" |
| 6 | `get_upstream_features` | L1:F6546@43, k=5 | Emb:" planning"@43 (w=21.88) +4 more |
| 7 | `get_upstream_features` | L0:F14054@43, k=5 | Emb:" planning"@43 (w=14.62) +4 more |
| 8 | `inspect_feature` | L0, F14323 | "the word "planning"" |
| 9 | `inspect_feature` | L0, F10833 | "the word "reduction"" |

**Findings:** L2:F9024 is a highly specific 'planning' word-detection feature (frac_nonzero=0.011) whose activation is overwhelmingly driven by the raw token embedding of " planning" at pos 43 (edge_weight=26.625 — by far the largest signal in the circuit). This is a shallow, token-identity circuit with three main layers:

1. **PRIMARY DRIVER — Raw Embedding**: The " planning" token embedding at pos 43 feeds di…

</details>

<details>
<summary><b>SA-7</b> — tool trace (11 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F12637 | " words that indicate something is undesirable or wrong" |
| 2 | `get_upstream_features` | L4:F12637@12, k=8 | Emb:" never"@7 (w=11.38) +7 more |
| 3 | `inspect_feature` | L1, F14233 | " negative sentiment markers such as "not," "no," "never," and their eq" |
| 4 | `inspect_feature` | L2, F2415 | " frequent words indicating small quantities or proximity, or words wit" |
| 5 | `inspect_feature` | L2, F6993 | "phrases describing uncertainty or difficulty" |
| 6 | `inspect_feature` | L2, F13744 | "code snippets, URLs, or code-related terminology" |
| 7 | `get_upstream_features` | L1:F14233@7, k=6 | Emb:" never"@7 (w=10.88) +5 more |
| 8 | `get_upstream_features` | L2:F2415@9, k=6 | Emb:" never"@7 (w=8.31) +5 more |
| 9 | `inspect_feature` | L0, F2318 | " the word "never"." |
| 10 | `inspect_feature` | L0, F889 | " the word "had" followed by words indicating time passing or negative " |
| 11 | `inspect_feature` | L0, F15081 | " the word "never" sometimes, and maybe "former" and "plots"" |

**Findings:** ## Why does an 'undesirable/wrong' feature have a POSITIVE effect on the probe?

The key insight is that L4:F12637 ("words indicating something undesirable or wrong") is NOT firing because 'hustle' itself is undesirable — it is firing because of the word **'never'** (at pos 7) in the input prompt, and this 'never' negation context is what the probe is actually detecting as meaningful.

### The Cir…

</details>

### Build

`build_circuit` → 26 nodes, 39 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | anthropic/claude-opus-4.6 | 124,241 | 7,858 | 0 | 0 | $0.8177 | — | — |
| SA-5 | anthropic/claude-sonnet-4.6 | 21,775 | 2,205 | 0 | 0 | $0.0984 | ✅ 4F/8E | Trace L2:8284 at pos 44 — 'travel' word feature with POSITIV… |
| SA-4 | anthropic/claude-sonnet-4.6 | 30,379 | 2,686 | 0 | 0 | $0.1314 | ✅ 4F/12E | Trace L1:7244 at pos 5 — 'she' pronoun feature with POSITIVE… |
| SA-6 | anthropic/claude-sonnet-4.6 | 31,071 | 2,841 | 0 | 0 | $0.1358 | ✅ 6F/8E | Trace L2:9024 at pos 43 — 'planning' word feature with POSIT… |
| SA-1 | anthropic/claude-sonnet-4.6 | 34,324 | 3,526 | 0 | 0 | $0.1559 | ✅ 7F/10E | Trace the strongest positive-effect feature L3:3222 at pos 1… |
| SA-7 | anthropic/claude-sonnet-4.6 | 35,814 | 3,348 | 0 | 0 | $0.1577 | ✅ 8F/8E | Trace L4:12637 at pos 12 — 'words indicating undesirable/wro… |
| SA-2 | anthropic/claude-sonnet-4.6 | 59,211 | 3,885 | 0 | 0 | $0.2359 | ✅ 7F/18E | Trace L6:11646 at pos 5 — a 'references to women' feature tr… |
| SA-3 | anthropic/claude-sonnet-4.6 | 63,530 | 4,461 | 0 | 0 | $0.2575 | ✅ 12F/15E | Trace L15:7803 at pos 44 — a 'travel-related' feature. This … |
| **Total** | | **400,345** | **30,810** | **0** | **0** | **$1.9902** | | |

**Oracle wall-clock time:** 3m 58s