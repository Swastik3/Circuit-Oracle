# Circuit Oracle Report
**Date:** 2026-04-06 09:38:25 UTC | **Orchestrator:** minimax/minimax-m2.7 | **Subagent:** deepseek/deepseek-v3.2

## Input

**Prompt:** "Dataset: bib_nurse_professor-neg_neg_5 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "('The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession.',)"

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification of academic profession is driven by **genuine profession indicators** (Ph.D. abbreviations, research interests, university names) rather than spurious gender markers. The attribution circuit shows three clean pathways: (1) "Ph"+"D" tokens → Ph.D. detector → academic titles, (2) "from"+"received" tokens → degree/graduation terms → university detection → credentials, and (3) "research"+"interests" → academic research feature. Critically, the only feature showing gender pronoun associations (L3:F11994, promoting "he", "she", "man") has a **negative** edge weight (-4.94) to the academic degree detector—meaning it **actively inhibits** rather than supports the academic profession signal when gender pronouns appear.

**Confidence:** 8/10

**Reasoning:** The main attribution features all have low frac_nonzero values (0.002-0.038) indicating genuine academic content specificity. The Ph.D. pathway (L1:F10132 → L2:F10852 → L7:F14129) traces directly from token embeddings " Ph" and "D" through highly selective academic detectors (frac_nonzero 0.002-0.008). The university pathway (L4:F6310 → L17:F11003 → L20:F14235) uses "from" and "received" tokens with strong edge weights (34.25 at L17→L20) to detect institutions. The gender pronoun feature L3:F11994 actually **suppresses** academic credential detection (negative edge weight -4.94 to L6:F2254), suggesting the model has learned that academic biographies in training data often omit explicit gender references. The user's concern about spurious gender markers is not supported—the circuit relies on content-specific features with minimal generic pattern-matching.

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 10 features; top: L8:2383 de=-0.090 |
| 3 | `inspect_feature` ×6 | L0:6051, L1:10986, L7:14129, L8:2383, L2:10852, L20:14235 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L7:F14129@15` | ✅ reported | 11 | 15 | Trace this academic degree/university feature upstream to understand what signal… |
| SA-2 | `L2:F10852@15` | ✅ reported | 7 | 20 | Trace this academic titles feature upstream to find its source and check for gen… |
| SA-3 | `L1:F10986@3` | ✅ reported | 4 | 3 | Trace this academic research feature upstream to find what drives it |
| SA-4 | `L20:F14235@19` | ✅ reported | 11 | 29 | Trace this academic credentials feature (high activation 697) upstream to unders… |

<details>
<summary><b>SA-1</b> — tool trace (17 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L7, F14129 | " academic degrees, universities, and people associated with them" |
| 2 | `get_upstream_features` | L7:F14129@15, k=5 | L6:F2254 (w=7.09) +4 more |
| 3 | `inspect_feature` | L6, F2254 | "references to academic degrees" |
| 4 | `inspect_feature` | L5, F13801 | "abbreviations for degrees and mentions of educational attainment" |
| 5 | `inspect_feature` | L1, F10132 | " the abbreviation for Doctorate of Philosophy, "Ph.D." (or "PhD") writ" |
| 6 | `get_upstream_features` | L6:F2254@15, k=5 | L2:F10852 (w=12.31) +4 more |
| 7 | `inspect_feature` | L2, F10852 | " academic titles and degrees" |
| 8 | `get_upstream_features` | L2:F10852@15, k=5 | Emb:" Ph"@13 (w=13.94) +4 more |
| 9 | `inspect_feature` | L1, F14298 | "academic publications, papers, and citations" |
| 10 | `get_upstream_features` | L5:F13801@15, k=5 | L2:F10852 (w=7.25) +4 more |
| 11 | `inspect_feature` | L3, F8294 | " words and phrases related to advanced education, research, and high-l" |
| 12 | `inspect_feature` | L3, F11994 | " academic degrees and professional titles, especially involving "Ph.D." |
| 13 | `get_upstream_features` | L3:F11994@15, k=5 | L2:F10852 (w=11.69) +4 more |
| 14 | `inspect_feature` | L2, F13360 | " words related to academic titles and positions." |
| 15 | `get_upstream_features` | L1:F10132@15, k=5 | Emb:" Ph"@13 (w=16.25) +4 more |
| 16 | `inspect_feature` | L0, F7699 | "words and abbreviations starting with the letter "D"" |
| 17 | `inspect_feature` | L0, F14877 | " single uppercase letters, sometimes followed by other characters, whi" |

**Findings:** I traced the academic degree/university feature (L7:F14129) upstream through 5 layers back to token embeddings. Key findings:

1. The circuit originates from token embeddings: "Ph" at position 13 and "D" at position 15 (likely part of "Ph.D." or similar).

2. Main positive pathway: Token embeddings → L1:F10132 (detects "D" in Ph.D.) → L2:F10852 (academic titles) → L6:F2254 (academic degrees) → L7:…

</details>

<details>
<summary><b>SA-2</b> — tool trace (12 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L2, F10852 | " academic titles and degrees" |
| 2 | `get_upstream_features` | L2:F10852@15, k=5 | Emb:" Ph"@13 (w=13.94) +4 more |
| 3 | `inspect_feature` | L1, F14298 | "academic publications, papers, and citations" |
| 4 | `inspect_feature` | L1, F10132 | " the abbreviation for Doctorate of Philosophy, "Ph.D." (or "PhD") writ" |
| 5 | `get_upstream_features` | L1:F10132@15, k=5 | Emb:" Ph"@13 (w=16.25) +4 more |
| 6 | `get_upstream_features` | L1:F14298@15, k=5 | Emb:" Ph"@13 (w=11.19) +4 more |
| 7 | `inspect_feature` | L0, F7699 | "words and abbreviations starting with the letter "D"" |
| 8 | `inspect_feature` | L0, F14877 | " single uppercase letters, sometimes followed by other characters, whi" |
| 9 | `inspect_feature` | L0, F15795 | " the word 'necessarily'" |
| 10 | `inspect_feature` | L0, F11532 | "titles and roles of people in organizations" |
| 11 | `get_upstream_features` | L0:F7699@15, k=5 | Emb:"D"@15 (w=11.31) +4 more |
| 12 | `get_upstream_features` | L0:F14877@15, k=5 | Emb:"."@14 (w=8.12) +4 more |

**Findings:** I traced the academic titles feature (L2:F10852) upstream through 2 layers to find its source and check for gender-related signals. The circuit reveals:

1. The academic titles feature is primarily driven by token embeddings: " Ph" at position 13 and "D" at position 15 are the strongest direct inputs (weights 13.94 and 9.69 respectively).

2. Key intermediate features:
   - L1:F10132: Specifically…

</details>

<details>
<summary><b>SA-3</b> — tool trace (5 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L1, F10986 | " words related to academic research" |
| 2 | `get_upstream_features` | L1:F10986@3, k=5 | Emb:" research"@2 (w=6.62) +4 more |
| 3 | `inspect_feature` | L0, F13948 | " the color "pink"" |
| 4 | `inspect_feature` | L0, F6113 | " the word "overall", sometimes alongside words that express quantity" |
| 5 | `inspect_feature` | L0, F13431 | "the word "owing"." |

**Findings:** The tracing reveals that L1:F10986 (words related to academic research) at position 3 is primarily driven directly by the input tokens " research" (position 2) and " interests" (position 3) with very strong edge weights (6.625 and 4.469 respectively). These token embeddings provide the strongest causal influence. There are also weaker connections from three layer 0 features: F13948 (color pink, ne…

</details>

<details>
<summary><b>SA-4</b> — tool trace (19 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L20, F14235 | " references to academic credentials and institutions." |
| 2 | `get_upstream_features` | L20:F14235@19, k=5 | L17:F11003 (w=34.25) +4 more |
| 3 | `inspect_feature` | L17, F11003 | "university" |
| 4 | `inspect_feature` | L19, F2496 | " mentions of universities and degrees" |
| 5 | `inspect_feature` | L17, F7973 | " phrases describing someone's education and the schools they attended" |
| 6 | `get_upstream_features` | L17:F11003@19, k=5 | Emb:"<bos>"@0 (w=-6.69) +4 more |
| 7 | `inspect_feature` | L14, F3956 | " universities and degrees" |
| 8 | `inspect_feature` | L3, F4213 | " mentions of degree qualifications or awards" |
| 9 | `get_upstream_features` | L14:F3956@19, k=5 | Emb:"<bos>"@0 (w=-4.84) +4 more |
| 10 | `inspect_feature` | L7, F14129 | " academic degrees, universities, and people associated with them" |
| 11 | `get_upstream_features` | L7:F14129@19, k=5 | L5:F11028 (w=4.56) +4 more |
| 12 | `inspect_feature` | L5, F11028 | " terms and phrases related to academic study and institutions" |
| 13 | `get_upstream_features` | L5:F11028@19, k=5 | L4:F6310 (w=4.12) +4 more |
| 14 | `inspect_feature` | L4, F6310 | " words related to academic degrees, graduations, and offers" |
| 15 | `get_upstream_features` | L4:F6310@19, k=5 | Emb:" from"@19 (w=7.12) +4 more |
| 16 | `inspect_feature` | L2, F10852 | " academic titles and degrees" |
| 17 | `get_upstream_features` | L19:F2496@19, k=5 | L17:F11003 (w=15.75) +4 more |
| 18 | `inspect_feature` | L18, F13805 | "Universities" |
| 19 | `get_upstream_features` | L18:F13805@19, k=5 | L17:F11003 (w=27.25) +4 more |

**Findings:** Tracing the academic credentials feature (L20:F14235) upstream revealed a hierarchical circuit focused on academic institutions and credentials. The circuit originates from token embeddings including "from" (position 19, appears multiple times), "Ph" (position 13), and "received" (position 11). 

Key findings:
1. **No gender markers found**: The circuit appears to be gender-neutral, focusing purel…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` | L3, F11994 → " academic degrees and professional titles, especially involving "Ph.D." |

### Build

`build_circuit` → 15 nodes, 17 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m2.7 | 47,544 | 4,802 | 47,911 | 0 | $0.0215 | — | — |
| SA-3 | deepseek/deepseek-v3.2 | 25,052 | 1,794 | 0 | 0 | $0.0072 | ✅ 4F/3E | Trace this academic research feature upstream to find what d… |
| SA-2 | deepseek/deepseek-v3.2 | 79,711 | 3,727 | 0 | 0 | $0.0221 | ✅ 7F/20E | Trace this academic titles feature upstream to find its sour… |
| SA-1 | deepseek/deepseek-v3.2 | 141,238 | 5,016 | 0 | 0 | $0.0386 | ✅ 11F/15E | Trace this academic degree/university feature upstream to un… |
| SA-4 | deepseek/deepseek-v3.2 | 154,324 | 5,594 | 14,720 | 0 | $0.0426 | ✅ 11F/29E | Trace this academic credentials feature (high activation 697… |
| **Total** | | **447,869** | **20,933** | **62,631** | **0** | **$0.1321** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 8m 49s