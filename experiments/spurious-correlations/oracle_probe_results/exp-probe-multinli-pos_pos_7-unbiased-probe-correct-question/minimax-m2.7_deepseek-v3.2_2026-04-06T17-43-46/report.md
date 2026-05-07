# Circuit Oracle Report
**Date:** 2026-04-06 17:43:46 UTC | **Orchestrator:** minimax/minimax-m2.7 | **Subagent:** deepseek/deepseek-v3.2

## Input

**Prompt:** "Dataset: multinli-pos_pos_7 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "('The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction.',)"

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification is driven by a mix of content-specific features (lexical items like "glimpse", "first", "of", "abbey" with low frac_nonzero 0.005-0.02) and one potential spurious feature (L0:F9026 "technical documents" with high frac_nonzero=0.41), but **the user's concern about negation word signals is NOT confirmed** — no standard negation features appear in the top 15 drivers.

**Confidence:** 8/10

**Reasoning:** The attribution circuit reveals the following mechanism:

**1. Content-Specific Features (Lexical/Semantic):**
- **L4:F3833 "Plot summary words"** (frac=0.01) is the strongest positive driver after the output. It receives direct input from "glimpse" (weight 7.03), "first" (weight 4.28), and "of" (weight 3.97). This feature is fed by L3:F6616 "forms of seeing/noticing" (frac=0.006) which strongly activates on "glimpse" (weight 18.38). This represents genuine semantic content about first impressions.
- **L0:F2848 "Word 'of'"** at positions 4 and 30 (frac=0.02 each) are direct embedding-driven features with very high edge weights (35-37) from the actual " of" tokens, confirming lexical grounding.
- **L4:F4605 "Churches/buildings"** (frac=0.005) and **L4:F5749 "Ancient settlements"** (frac=0.005) encode the semantically relevant content about the abbey — these have negative direct effects, suggesting they inhibit the classification when present.
- **L0:F7710 "Pronoun 'you'"** (frac=0.02) captures the second-person address in the prompt.

**2. Potential Spurious Feature:**
- **L0:F9026 "Technical documents with numbers"** (frac=0.41 — notably HIGH) is the one concerning feature. It fires on statistical patterns, tables, and figures. However, it's activated by the "abbey" token here, not negation signals. This could represent a spurious pattern if the training data has abbey-related content in technical documents.

**3. Document Structure vs. Negation:**
- **L8:F8406** (labeled "'I' and 'Exactly'") has negative effect (-0.17) but its description is misleading. Tracing upstream shows it's driven by `<bos>` token (weight 10.69) and code documentation patterns (L7:F462, L7:F5741), not by negation semantics. This is a positional/structural artifact.

**4. Key Finding — No Negation Signals:**
The input text contains "lacks a steeple" which implies contradiction, but the circuit does NOT use negation-specific features (no "not", "no", "never", "lacks" detectors). Instead, it relies on:
- Lexical co-occurrence ("glimpse" + "first")
- Generic function words ("of", "the")
- One high-frac_nonzero technical pattern detector

The user's concern about **spurious negation word signals is not supported** by the data. The circuit primarily uses content-specific low-frac_nonzero features representing the lexical/semantic content of the prompt (first impressions, abbey-related building terms), plus one potentially spurious high-frac_nonzero technical document detector.

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L8:8406 de=-0.165 |

### Dispatch: 5 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L8:F8406@1` | ✅ reported | 10 | 20 | Trace this negative-effect feature (L8:F8406) upstream to understand what drives… |
| SA-2 | `L0:F2848@4` | ✅ reported | 1 | 5 | Trace this positive-effect embedding feature (L0:F2848 at pos 4) upstream to ide… |
| SA-3 | `L17:F451@1` | ❌ error | — | — | Trace this high-activation feature (L17:F451, activation 55.25) upstream to see … |
| SA-4 | `L4:F3833@4` | ✅ reported | 3 | 15 | Trace this positive-effect feature (L4:F3833) to see if it encodes lexical conte… |
| SA-5 | `L4:F4605@9` | ✅ reported | 5 | 21 | Trace this negative-effect feature (L4:F4605) to understand what content drives … |

<details>
<summary><b>SA-1</b> — tool trace (14 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L8, F8406 | "the first-person pronoun "I" and the word "Exactly"" |
| 2 | `get_upstream_features` | L8:F8406@1, k=5 | Emb:"<bos>"@0 (w=10.69) +4 more |
| 3 | `inspect_feature` | L7, F462 | " code documentation and import statements" |
| 4 | `inspect_feature` | L7, F5741 | " code documentation or copyright information" |
| 5 | `inspect_feature` | L5, F3992 | "the start of documentation blocks in code" |
| 6 | `get_upstream_features` | L7:F462@1, k=5 | Emb:"<bos>"@0 (w=21.00) +4 more |
| 7 | `get_upstream_features` | L5:F3992@1, k=5 | Emb:"<bos>"@0 (w=21.25) +4 more |
| 8 | `get_upstream_features` | L4:F9757@1, k=5 | Emb:"<bos>"@0 (w=15.31) +4 more |
| 9 | `inspect_feature` | L3, F373 | " word beginnings with the letters "a," "h,""i," "r," and "p" (perhaps " |
| 10 | `inspect_feature` | L0, F7344 | " content markers like figures and section headers" |
| 11 | `get_upstream_features` | L7:F5741@1, k=5 | Emb:"<bos>"@0 (w=12.06) +4 more |
| 12 | `inspect_feature` | L0, F5060 | "mentions of dinner or breakfast" |
| 13 | `inspect_feature` | L1, F14137 | " words or phrases that appear in legal or technical documents, like na" |
| 14 | `inspect_feature` | L6, F14585 | " the words "the" and "it" at the beginning of sentences" |

**Findings:** I traced the negative-effect feature L8:F8406 ("the first-person pronoun 'I' and the word 'Exactly'") upstream through 5 hops. The key findings:

1. **Strong bos>` influence**: The bos>` token at position 0 has very strong positive connections throughout the circuit (weights 10.69-21.25), suggesting positional influence rather than content-based.

2. **Key intermediate hub L5:F3992**: This feature…

</details>

<details>
<summary><b>SA-2</b> — tool trace (2 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F2848 | "the word "of"" |
| 2 | `get_upstream_features` | L0:F2848@4, k=5 | Emb:" of"@4 (w=35.25) +4 more |

**Findings:** Successfully traced the positive-effect embedding feature L0:F2848 at position 4 back to its input tokens. The feature detects "the word 'of'" and has a very strong connection (weight 35.25) directly from the input token " of" at position 4. This confirms that this feature is primarily driven by the word "of" appearing at position 4 in the input. Additional weaker connections include a positive co…

</details>

<details>
<summary><b>SA-3</b> — tool trace (20 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L17, F451 | "start of sentences" |
| 2 | `get_upstream_features` | L17:F451@1, k=5 | L16:F10989 (w=-12.38) +4 more |
| 3 | `inspect_feature` | L16, F10989 | "the" |
| 4 | `inspect_feature` | L14, F2510 | "the word "using"" |
| 5 | `inspect_feature` | L15, F751 | "code snippets" |
| 6 | `get_upstream_features` | L16:F10989@1, k=5 | L15:F851 (w=28.88) +4 more |
| 7 | `inspect_feature` | L15, F851 | " code documentation blocks in various programming languages" |
| 8 | `get_upstream_features` | L15:F851@1, k=5 | L12:F12493 (w=20.88) +4 more |
| 9 | `inspect_feature` | L12, F12493 | " words that end in "ing", "ecti", "tial", or "ogi", and also the word " |
| 10 | `get_upstream_features` | L12:F12493@1, k=5 | L10:F14174 (w=14.81) +4 more |
| 11 | `inspect_feature` | L10, F14174 | "left curly brackets" |
| 12 | `get_upstream_features` | L10:F14174@1, k=5 | L9:F3056 (w=16.25) +4 more |
| 13 | `inspect_feature` | L9, F3056 | " various keywords in programming languages, markup languages, and math" |
| 14 | `inspect_feature` | L9, F2762 | " various code snippets, especially javascript" |
| 15 | `get_upstream_features` | L9:F3056@1, k=5 | Emb:"<bos>"@0 (w=13.44) +4 more |
| 16 | `get_upstream_features` | L9:F2762@1, k=5 | Emb:"<bos>"@0 (w=15.25) +4 more |
| 17 | `inspect_feature` | L7, F462 | " code documentation and import statements" |
| 18 | `get_upstream_features` | L7:F462@1, k=5 | Emb:"<bos>"@0 (w=21.00) +4 more |
| 19 | `get_upstream_features` | L14:F2510@1, k=5 | L12:F12493 (w=9.62) +4 more |
| 20 | `get_upstream_features` | L15:F751@1, k=5 | L14:F15964 (w=19.12) +4 more |

</details>

<details>
<summary><b>SA-4</b> — tool trace (6 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F3833 | " words used when summarizing plot points or providing courtroom insigh" |
| 2 | `get_upstream_features` | L4:F3833@4, k=5 | Emb:" glimpse"@3 (w=7.03) +4 more |
| 3 | `inspect_feature` | L3, F6616 | "different forms of seeing or noticing" |
| 4 | `get_upstream_features` | L3:F6616@4, k=5 | Emb:" glimpse"@3 (w=18.38) +4 more |
| 5 | `inspect_feature` | L0, F2848 | "the word "of"" |
| 6 | `get_upstream_features` | L0:F2848@4, k=5 | Emb:" of"@4 (w=35.25) +4 more |

**Findings:** The trace reveals that L4:F3833 primarily encodes lexical content rather than spurious patterns like negation signals. The feature at position 4 is directly fed by:

1. Token " glimpse" at position 3 (strongest direct connection: weight 7.0312)
2. Token " first" at position 2 (weight 4.2812)  
3. Token " of" at position 4 (weight 3.9688)

The main intermediate feature is L3:F6616 which detects "di…

</details>

<details>
<summary><b>SA-5</b> — tool trace (10 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F4605 | " words related to churches, chapels and other buildings, in addition t" |
| 2 | `get_upstream_features` | L4:F4605@9, k=5 | Emb:"led"@9 (w=6.47) +4 more |
| 3 | `inspect_feature` | L3, F4081 | "mentions of the statistical software Stata and the term "stent"." |
| 4 | `inspect_feature` | L3, F7650 | "abbreviations, geographical locations, and the letter "l"" |
| 5 | `get_upstream_features` | L3:F4081@9, k=5 | Emb:" steep"@8 (w=11.44) +4 more |
| 6 | `inspect_feature` | L2, F6145 | " verbs ending in 'led'" |
| 7 | `get_upstream_features` | L2:F6145@9, k=5 | Emb:"led"@9 (w=35.75) +4 more |
| 8 | `get_upstream_features` | L3:F7650@9, k=3 | Emb:"led"@9 (w=5.81) +2 more |
| 9 | `inspect_feature` | L2, F5878 | "the suffix "le"" |
| 10 | `get_upstream_features` | L2:F5878@9, k=3 | Emb:" steep"@8 (w=8.56) +2 more |

**Findings:** Tracing L4:F4605 (church-related feature) reveals it's driven primarily by the token "led" at position 9 (weight 6.4688) and " steep" at position 8 (weight 4.4688). The feature pathway shows that "led" token strongly activates L2 features that detect verb endings ("led") and suffix "le", which then feed into L3 features about statistical software Stata and abbreviations. These L3 features then com…

</details>

### Re-dispatch (round 2): 1 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-6 | `L16:F10989@1` | ❌ error | — | — | Trace this strongly-negative upstream feature (L16:F10989) that feeds into L17:F… |

<details>
<summary><b>SA-6</b> — tool trace (20 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L16, F10989 | "the" |
| 2 | `get_upstream_features` | L16:F10989@1, k=5 | L15:F851 (w=28.88) +4 more |
| 3 | `inspect_feature` | L15, F851 | " code documentation blocks in various programming languages" |
| 4 | `inspect_feature` | L15, F751 | "code snippets" |
| 5 | `get_upstream_features` | L15:F851@1, k=5 | L12:F12493 (w=20.88) +4 more |
| 6 | `inspect_feature` | L12, F12493 | " words that end in "ing", "ecti", "tial", or "ogi", and also the word " |
| 7 | `inspect_feature` | L9, F2762 | " various code snippets, especially javascript" |
| 8 | `get_upstream_features` | L12:F12493@1, k=5 | L10:F14174 (w=14.81) +4 more |
| 9 | `inspect_feature` | L10, F14174 | "left curly brackets" |
| 10 | `get_upstream_features` | L10:F14174@1, k=5 | L9:F3056 (w=16.25) +4 more |
| 11 | `inspect_feature` | L9, F3056 | " various keywords in programming languages, markup languages, and math" |
| 12 | `get_upstream_features` | L9:F3056@1, k=5 | Emb:"<bos>"@0 (w=13.44) +4 more |
| 13 | `inspect_feature` | L7, F462 | " code documentation and import statements" |
| 14 | `get_upstream_features` | L7:F462@1, k=5 | Emb:"<bos>"@0 (w=21.00) +4 more |
| 15 | `inspect_feature` | L5, F3992 | "the start of documentation blocks in code" |
| 16 | `get_upstream_features` | L5:F3992@1, k=5 | Emb:"<bos>"@0 (w=21.25) +4 more |
| 17 | `inspect_feature` | L13, F8128 | " sentences beginning with the word "In"" |
| 18 | `get_upstream_features` | L13:F8128@1, k=5 | L10:F14174 (w=11.06) +4 more |
| 19 | `inspect_feature` | L10, F10933 | " the first word of a paragraph or title" |
| 20 | `inspect_feature` | L9, F15819 | "code snippets" |

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L17:F451@1, k=8 → L16:F10989 (w=-12.38) +7 more |
| 2 | `get_upstream_features` | L6:F5342@4, k=6 → Emb:" first"@2 (w=12.00) +5 more |
| 3 | `inspect_feature` ×2 | L0:3820, L4:2581 |
| 4 | `get_upstream_features` | L17:F451@1, k=6 → L16:F10989 (w=-12.38) +5 more |
| 5 | `inspect_feature` ×2 | L0:9026, L0:7710 |
| 6 | `get_upstream_features` | L0:F2848@30, k=5 → Emb:" of"@30 (w=37.25) +4 more |
| 7 | `inspect_feature` ×4 | L16:10989, L6:5342, L4:5749, L4:13244 |
| 8 | `get_upstream_features` | L4:F3833@3, k=5 → Emb:" glimpse"@3 (w=13.62) +4 more |

### Build

`build_circuit` → 32 nodes, 39 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m2.7 | 28,525 | 6,575 | 85,976 | 0 | $0.0190 | — | — |
| SA-2 | deepseek/deepseek-v3.2 | 9,984 | 1,139 | 0 | 0 | $0.0030 | ✅ 1F/5E | Trace this positive-effect embedding feature (L0:F2848 at po… |
| SA-4 | deepseek/deepseek-v3.2 | 31,012 | 2,436 | 0 | 0 | $0.0090 | ✅ 3F/15E | Trace this positive-effect feature (L4:F3833) to see if it e… |
| SA-3 | deepseek/deepseek-v3.2 | 135,177 | 2,215 | 35,264 | 0 | $0.0369 | ❌ error | Trace this high-activation feature (L17:F451, activation 55.… |
| SA-5 | deepseek/deepseek-v3.2 | 56,245 | 3,593 | 4,416 | 0 | $0.0161 | ✅ 5F/21E | Trace this negative-effect feature (L4:F4605) to understand … |
| SA-1 | deepseek/deepseek-v3.2 | 103,215 | 4,516 | 3,264 | 0 | $0.0286 | ✅ 10F/20E | Trace this negative-effect feature (L8:F8406) upstream to un… |
| SA-6 | deepseek/deepseek-v3.2 | 143,066 | 1,753 | 24,704 | 0 | $0.0385 | ❌ error | Trace this strongly-negative upstream feature (L16:F10989) t… |
| **Total** | | **507,224** | **22,227** | **153,624** | **0** | **$0.1512** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 6m 44s