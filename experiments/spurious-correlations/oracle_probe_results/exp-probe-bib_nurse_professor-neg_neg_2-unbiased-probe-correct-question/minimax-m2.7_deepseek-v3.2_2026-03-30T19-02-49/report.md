# Circuit Oracle Report
**Date:** 2026-03-30 19:02:49 UTC | **Orchestrator:** minimax/minimax-m2.7 | **Subagent:** deepseek/deepseek-v3.2

## Input
**Prompt:** "Dataset: bib_nurse_professor-neg_neg_2 | Probe: unbiased | Method: correct"
**System prompt:** ""
**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."
**Top predictions:**  (100.0%)

## Oracle Analysis
**Analysis:** The probe's classification is driven primarily by **genuine profession indicators** (engineering degree, PhD, academic institutions) rather than spurious gender markers, though one spurious feature exists where the word "received" spuriously activates an "ice" detector, and the pronoun "his" paradoxically suppresses the score (possibly reflecting training data where female engineers are more explicitly gender-marked).

**Confidence:** 8/10

**Reasoning:**

The circuit analysis reveals a mixed picture regarding the user's concern about spurious gender markers:

**Genuine Profession Indicators (positive effects):**
1. **L1:F1372 "engineer"** (+0.0645) - Directly detects the word "Engineering" from "Mechanical Engineering" at position 9. This is a legitimate profession feature with low frac_nonzero (0.00767), meaning it fires selectively on engineer-related contexts.

2. **L14:F5600 "places in Canada"** (+0.064) - Detects "Waterloo" at position 14, which correctly identifies the University of Waterloo in Canada. This is a legitimate geographic association, not spurious.

3. **L7:F14129 "academic degrees"** (+0.0439) - Detects the "PhD" abbreviation at positions 48-50. This is a genuine academic credential indicator.

4. **L2:F16309 "people's names"** (+0.0496) - Detects "Daniel" at position 1. While this is a male name, the feature label is "people's names" not "male names," and it primarily functions as a subject identifier rather than a gender proxy.

**Potential Spurious Features:**
1. **L0:F15320 "ice"** (+0.0583) - **This is genuinely spurious.** The autointerp labels it as detecting "ice," but it fires on the token " received" (from "Daniel received") with edge weight 13.0. There is no semantic reason why "received" should activate an "ice" detector for this classification.

2. **L0:F2994 "his/he"** (-0.0364) - **This is a gender marker with a negative effect.** The pronoun "his" in "Daniel received his Bachelors" is a male gender marker, yet it *suppresses* the classification score rather than boosting it. This suggests the probe may have learned from training data where female engineers are more explicitly marked (e.g., "earned her degree" vs. "earned his degree"), causing the absence of explicit gender marking in male subjects to suppress the score.

3. **L6:F3235 academic institutions** (-0.0549) - **Partially spurious.** It fires on "Beirut" from "American University of Beirut" with a negative effect, suggesting the model penalizes Middle Eastern academic institutions compared to Western ones.

**Conclusion:** The circuit is NOT primarily driven by gender markers. The top drivers are genuine profession indicators (engineering, PhD, Canadian university). The main spurious feature is the "received"→"ice" pattern, which is a lexical artifact unrelated to gender or profession. The gender pronoun "his" actually *suppresses* the score, indicating the model may have learned inverse gender associations from training data.

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L0:2743 de=-0.069 |
| 3 | `inspect_feature` ×5 | L1:1372, L14:5600, L0:15320, L2:16309, L0:2743 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L1:F1372@9` | ✅ reported | 3 | 7 | Trace why L1:F1372 (detects "engineer") activates at pos 9 in the input. What in… |
| SA-2 | `L2:F16309@1` | ✅ reported | 6 | 15 | Trace why L2:F16309 (detects people's names) activates at pos 1. What token is a… |
| SA-3 | `L14:F5600@14` | ✅ reported | 9 | 12 | Trace why L14:F5600 (detects Canadian places) activates at pos 14. What token is… |
| SA-4 | `L0:F15320@2` | ✅ reported | 3 | 5 | Trace why L0:F15320 (detects "ice") activates at pos 2. What token is at pos 2? … |

<details>
<summary><b>SA-1</b> — tool trace (6 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L1, F1372 | "the word "engineer"" |
| 2 | `get_upstream_features` | L1:F1372@9, k=5 | Emb:" Engineering"@9 (w=19.00) +4 more |
| 3 | `inspect_feature` | L0, F6414 | " the job title of "engineer", sometimes in conjunction with other word" |
| 4 | `inspect_feature` | L0, F15570 | " words and phrases related to medical treatment and analysis" |
| 5 | `get_upstream_features` | L0:F6414@9, k=5 | Emb:" Engineering"@9 (w=11.88) +4 more |
| 6 | `get_upstream_features` | L0:F15570@9, k=5 | Emb:" Engineering"@9 (w=10.50) +4 more |

**Findings:** The L1:F1372 feature that detects "engineer" at position 9 is primarily driven directly by the token " Engineering" at position 9 itself (edge weight 19.0). This is the strongest connection. Secondarily, it receives input from L0:F6414 (which also detects engineer-related terms) and L0:F15570 (related to medical treatment/analysis). Both L0 features are themselves primarily driven by the " Enginee…

</details>

<details>
<summary><b>SA-2</b> — tool trace (12 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L2, F16309 | " people's names" |
| 2 | `get_upstream_features` | L2:F16309@1, k=5 | Emb:"Daniel"@1 (w=12.94) +4 more |
| 3 | `inspect_feature` | L0, F7532 | " proper nouns" |
| 4 | `inspect_feature` | L0, F6226 | " proper nouns of people" |
| 5 | `inspect_feature` | L1, F13515 | " places where "berg" is used as part of a word" |
| 6 | `get_upstream_features` | L0:F7532@1, k=5 | Emb:"Daniel"@1 (w=10.12) +4 more |
| 7 | `get_upstream_features` | L0:F6226@1, k=5 | Emb:"Daniel"@1 (w=9.69) +4 more |
| 8 | `get_upstream_features` | L1:F13515@1, k=5 | Emb:"Daniel"@1 (w=12.69) +4 more |
| 9 | `inspect_feature` | L0, F2893 | " the word "engine", particularly in a technical context" |
| 10 | `get_upstream_features` | L0:F2893@1, k=5 | Emb:"Daniel"@1 (w=11.31) +4 more |
| 11 | `inspect_feature` | L0, F4903 | "the word "loyalty" and names" |
| 12 | `get_top_logits` | k=5 | "" (100%) |

**Findings:** The circuit shows that L2:F16309 (detects people's names) activates at position 1 because the token at position 1 is "Daniel". This is directly fed from the embedding "Daniel" with a strong positive weight of 12.9375. The feature also receives support from L0:F7532 (proper nouns) and L0:F6226 (proper nouns of people), which themselves are directly activated by the "Daniel" embedding. Interestingly…

</details>

<details>
<summary><b>SA-3</b> — tool trace (12 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L14, F5600 | " places and regions, particularly in Canada" |
| 2 | `get_upstream_features` | L14:F5600@14, k=5 | L7:F8870 (w=15.94) +4 more |
| 3 | `inspect_feature` | L7, F8870 | " locations and names of organizations or people" |
| 4 | `inspect_feature` | L4, F8439 | " stock ticker symbols and Canadian geography" |
| 5 | `get_upstream_features` | L7:F8870@14, k=5 | L4:F8439 (w=9.00) +4 more |
| 6 | `get_upstream_features` | L4:F8439@14, k=5 | Emb:" Waterloo"@14 (w=17.25) +4 more |
| 7 | `inspect_feature` | L1, F909 | " words and phrases related to education and diversity in schools" |
| 8 | `inspect_feature` | L1, F15370 | "words related to testing and grading in academic settings and words re" |
| 9 | `inspect_feature` | L0, F9022 | " technical words used in computing, science, or engineering" |
| 10 | `inspect_feature` | L13, F5801 | " proper nouns referring to places" |
| 11 | `inspect_feature` | L7, F8821 | " place names and words referencing nationality, with an emphasis on Qu" |
| 12 | `inspect_feature` | L6, F13356 | " references to Canada and Canadian news organizations" |

**Findings:** The circuit tracing reveals that L14:F5600 (detects Canadian places) activates at position 14 because the token at that position is " Waterloo", a city in Ontario, Canada. The strongest positive influence comes directly from the embedding of " Waterloo" and intermediate Canadian geography detection features. The circuit shows both excitation and inhibition pathways: 

1. Main excitation path: Embe…

</details>

<details>
<summary><b>SA-4</b> — tool trace (5 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F15320 | " the word "ice"" |
| 2 | `get_upstream_features` | L0:F15320@2, k=5 | Emb:" received"@2 (w=13.00) +4 more |
| 3 | `inspect_feature` | L0, F1847 | "scientific terms and experimental details related to biological and ch" |
| 4 | `inspect_feature` | L0, F1903 | "instances of sentences starting with "The"" |
| 5 | `get_upstream_features` | L0:F15320@2, k=10 | Emb:" received"@2 (w=13.00) +9 more |

**Findings:** Tracing from L0:F15320 (labeled as detecting \"ice\") at position 2 revealed that the token at position 2 is \" received\" with a very strong edge weight of 13.0. This means the \"ice\" detector feature is primarily activated by the token \" received\" rather than \"ice\". The token \"Daniel\" at position 1 has a weak negative influence (-0.2129). The feature labels \"scientific terms\" and \"sent…

</details>

### Re-dispatch (round 2): 3 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-5 | `L7:F14129@50` | ✅ reported | 8 | 10 | Trace what tokens drive L7:F14129 (academic degrees, universities) at pos 50. Wh… |
| SA-6 | `L6:F3235@38` | ✅ reported | 8 | 18 | Trace why L6:F3235 (academic publications, scientific institutions) at pos 38 ha… |
| SA-7 | `L0:F4687@14` | ✅ reported | 1 | 1 | Trace what drives L0:F4687 (top-10 feature at pos 14). What does it detect? |

<details>
<summary><b>SA-5</b> — tool trace (13 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L7, F14129 | " academic degrees, universities, and people associated with them" |
| 2 | `get_upstream_features` | L7:F14129@50, k=5 | L6:F2254 (w=7.34) +4 more |
| 3 | `inspect_feature` | L6, F2254 | "references to academic degrees" |
| 4 | `inspect_feature` | L5, F13801 | "abbreviations for degrees and mentions of educational attainment" |
| 5 | `inspect_feature` | L1, F10132 | " the abbreviation for Doctorate of Philosophy, "Ph.D." (or "PhD") writ" |
| 6 | `get_upstream_features` | L6:F2254@50, k=5 | L2:F10852 (w=12.38) +4 more |
| 7 | `inspect_feature` | L2, F10852 | " academic titles and degrees" |
| 8 | `get_upstream_features` | L2:F10852@50, k=5 | Emb:" Ph"@48 (w=14.75) +4 more |
| 9 | `get_upstream_features` | L5:F13801@50, k=5 | L2:F10852 (w=7.28) +4 more |
| 10 | `get_upstream_features` | L1:F10132@50, k=5 | Emb:" Ph"@48 (w=16.25) +4 more |
| 11 | `inspect_feature` | L1, F14298 | "academic publications, papers, and citations" |
| 12 | `inspect_feature` | L0, F7699 | "words and abbreviations starting with the letter "D"" |
| 13 | `inspect_feature` | L0, F14877 | " single uppercase letters, sometimes followed by other characters, whi" |

**Findings:** The circuit for L7:F14129 (academic degrees, universities) at position 50 is driven by input tokens " Ph" at position 48 and "D" at position 50, which together form "PhD". The main pathway is: " Ph" (pos48) + "D" (pos50) → L1:F10132 (detects Ph.D. abbreviation) → L2:F10852 (academic titles and degrees) → L6:F2254 (references to academic degrees) → L7:F14129 (academic degrees, universities). The st…

</details>

<details>
<summary><b>SA-6</b> — tool trace (13 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F3235 | " academic publications, math, and scientific institutions" |
| 2 | `get_upstream_features` | L6:F3235@38, k=5 | Emb:" Beirut"@38 (w=1.85) +4 more |
| 3 | `inspect_feature` | L4, F13886 | "  US universities and their locations" |
| 4 | `inspect_feature` | L4, F5150 | " mentions of specific universities and colleges" |
| 5 | `inspect_feature` | L5, F16220 | "schools and universities" |
| 6 | `get_upstream_features` | L4:F13886@38, k=5 | Emb:" University"@36 (w=6.31) +4 more |
| 7 | `inspect_feature` | L0, F5626 | " names of places located in Europe" |
| 8 | `get_upstream_features` | L4:F5150@38, k=5 | Emb:" Beirut"@38 (w=7.50) +4 more |
| 9 | `inspect_feature` | L0, F9026 | "technical documents or data, including numbers, units, and references " |
| 10 | `get_upstream_features` | L5:F16220@38, k=5 | Emb:" Beirut"@38 (w=-1.55) +4 more |
| 11 | `inspect_feature` | L4, F11633 | " words related to education and employment history" |
| 12 | `get_upstream_features` | L0:F5626@38, k=5 | Emb:" Beirut"@38 (w=19.12) +4 more |
| 13 | `inspect_feature` | L2, F9457 | " place names" |

**Findings:** The negative effect of L6:F3235 (academic publications, scientific institutions) at position 38 is driven by the token " Beirut" at the same position. The circuit shows that " Beirut" strongly activates L0:F5626 (names of places in Europe) and L4:F5150 (mentions of specific universities), which then feed into L6:F3235. However, there's a complex pattern: while " Beirut" positively drives L4:F5150 …

</details>

<details>
<summary><b>SA-7</b> — tool trace (4 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F4687 | "place names" |
| 2 | `get_upstream_features` | L0:F4687@14, k=5 | Emb:" Waterloo"@14 (w=16.25) +4 more |
| 3 | `get_upstream_features` | L0:F4687@14, k=10 | Emb:" Waterloo"@14 (w=16.25) +9 more |
| 4 | `get_top_logits` | k=5 | "" (100%) |

**Findings:** L0:F4687 at position 14 is a 'place names' detector with 5% sparsity. It detects place names like Medford, Evanston, Schenectady in its top activating examples. At position 14 in this specific context, it is directly and strongly driven by the token embedding ' Waterloo' with edge weight 16.25. This is a layer 0 feature that reads directly from token embeddings, specifically detecting place names …

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L0:F2743@23, k=5 → Emb:" later"@23 (w=42.25) +4 more |
| 2 | `get_upstream_features` | L0:F6515@18, k=5 → Emb:"1"@17 (w=29.38) +4 more |
| 3 | `inspect_feature` ×2 | L6:3235, L7:14129 |
| 4 | `get_upstream_features` | L0:F7532@1, k=5 → Emb:"Daniel"@1 (w=10.12) +4 more |
| 5 | `get_upstream_features` | L0:F6226@1, k=5 → Emb:"Daniel"@1 (w=9.69) +4 more |
| 6 | `get_top_features` | token="", k=25 → 25 features; top: L0:2743 de=-0.069 |
| 7 | `inspect_feature` ×5 | L0:7905, L0:11333, L0:2994, L2:14934, L4:9757 |

### Build

`build_circuit` → 24 nodes, 27 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m2.7 | 44,113 | 7,195 | 107,499 | 0 | — | — | — |
| SA-1 | deepseek/deepseek-v3.2 | 29,290 | 1,922 | 0 | 0 | — | ✅ 3F/7E | Trace why L1:F1372 (detects "engineer") activates at pos 9 i… |
| SA-4 | deepseek/deepseek-v3.2 | 25,050 | 2,439 | 0 | 0 | — | ✅ 3F/5E | Trace why L0:F15320 (detects "ice") activates at pos 2. What… |
| SA-3 | deepseek/deepseek-v3.2 | 80,423 | 3,240 | 0 | 0 | — | ✅ 9F/12E | Trace why L14:F5600 (detects Canadian places) activates at p… |
| SA-2 | deepseek/deepseek-v3.2 | 80,181 | 3,553 | 0 | 0 | — | ✅ 6F/15E | Trace why L2:F16309 (detects people's names) activates at po… |
| SA-7 | deepseek/deepseek-v3.2 | 17,793 | 1,649 | 0 | 0 | — | ✅ 1F/1E | Trace what drives L0:F4687 (top-10 feature at pos 14). What … |
| SA-5 | deepseek/deepseek-v3.2 | 80,059 | 3,516 | 9,856 | 0 | — | ✅ 8F/10E | Trace what tokens drive L7:F14129 (academic degrees, univers… |
| SA-6 | deepseek/deepseek-v3.2 | 94,066 | 3,672 | 0 | 0 | — | ✅ 8F/18E | Trace why L6:F3235 (academic publications, scientific instit… |
| **Total** | | **450,975** | **27,186** | **117,355** | **0** | **—** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 7m 16s