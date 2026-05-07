# Circuit Oracle Report
**Date:** 2026-04-06 08:34:16 UTC | **Orchestrator:** minimax/minimax-m2.7 | **Subagent:** deepseek/deepseek-v3.2

## Input

**Prompt:** "Dataset: bib_nurse_professor-neg_neg_3 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "('The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession.',)"

**Top predictions:**  (100.0%)


## Oracle Analysis

## Step 5: Analysis

**Analysis:** The probe's classification score is driven by a hierarchy of genuine academic profession indicators, specifically Ph.D. degree tokens and university mentions — no gender markers were found anywhere in the attribution circuit.

**Confidence:** 9/10

**Reasoning:**

The circuit tracing reveals a robust, multi-layered pathway of legitimate academic content detection:

1. **Input-level signals (Layer 0-1):** The strongest root signals come directly from input tokens:
   - `" Ph"` at position 50 and `"D"` at position 52 (forming "Ph.D.") — edge weight 14.69 to L2:F10852
   - `"Peking"` and `"University"` at positions 12-13 — edge weight 17.75 to L4:F5150
   - Year digits `"9"` at positions 16-18 — detecting temporal patterns like "1998"

2. **Hierarchical abstraction (Layers 1-5):** The circuit progressively builds more abstract representations:
   - L1:F10132 (frac=0.00233) — highly specific Ph.D. abbreviation detector
   - L2:F10852 (frac=0.00801) — "academic titles and degrees"
   - L4:F5150 (frac=0.00399) — "specific universities and colleges"
   - L5:F13801 (frac=0.02825) — "degree abbreviations and educational attainment"

3. **Synthesis layer (Layers 6-7):** Features combine multiple signals:
   - L6:F2254 (frac=0.00412) — "references to academic degrees"
   - L7:F14129 (frac=0.00417) — "academic degrees, universities, and people associated with them"

4. **No spurious gender signals:** The features at position 2 ("He" pronoun) detect completely unrelated concepts: "ice", "reception", "route", and past tense verbs — not gender. All features have low frac_nonzero values (0.001-0.04), indicating genuine specificity to academic contexts rather than generic pattern matching.

The probe correctly identifies this biography as describing an academic professional through explicit credential markers (Ph.D.) and institutional affiliations (universities), not through proxy signals like gender pronouns.

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L6:3235 de=-0.054 |
| 3 | `inspect_feature` ×4 | L7:14129, L2:10852, L3:4213, L6:3235 |

### Dispatch: 2 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L7:F14129@52` | ✅ reported | 8 | 10 | Trace this academic degree feature upstream. Look for the source of the signal -… |
| SA-2 | `L2:F10852@52` | ✅ reported | 7 | 7 | Trace this academic titles feature upstream. Look for spurious gender signals or… |

<details>
<summary><b>SA-1</b> — tool trace (12 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L7, F14129 | " academic degrees, universities, and people associated with them" |
| 2 | `get_upstream_features` | L7:F14129@52, k=5 | L6:F2254 (w=6.97) +4 more |
| 3 | `inspect_feature` | L6, F2254 | "references to academic degrees" |
| 4 | `inspect_feature` | L5, F13801 | "abbreviations for degrees and mentions of educational attainment" |
| 5 | `inspect_feature` | L1, F10132 | " the abbreviation for Doctorate of Philosophy, "Ph.D." (or "PhD") writ" |
| 6 | `get_upstream_features` | L6:F2254@52, k=5 | L2:F10852 (w=12.06) +4 more |
| 7 | `inspect_feature` | L2, F10852 | " academic titles and degrees" |
| 8 | `get_upstream_features` | L2:F10852@52, k=5 | Emb:" Ph"@50 (w=14.69) +4 more |
| 9 | `inspect_feature` | L1, F14298 | "academic publications, papers, and citations" |
| 10 | `inspect_feature` | L1, F11924 | "words and phrases related to religion, faith, and antibodies" |
| 11 | `get_upstream_features` | L5:F13801@52, k=5 | L2:F10852 (w=7.38) +4 more |
| 12 | `inspect_feature` | L3, F8294 | " words and phrases related to advanced education, research, and high-l" |

**Findings:** Tracing the academic degree feature (L7:F14129) upstream reveals it's driven by genuine academic indicators, NOT gender markers. The circuit flows from raw input tokens " Ph" (position 50) and "D" (position 52) through increasingly abstract academic degree representations:

1. **Root tokens**: The strongest signals come directly from embeddings " Ph" (position 50, edge weight 14.69 to L2:F10852) a…

</details>

<details>
<summary><b>SA-2</b> — tool trace (12 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L2, F10852 | " academic titles and degrees" |
| 2 | `get_upstream_features` | L2:F10852@52, k=5 | Emb:" Ph"@50 (w=14.69) +4 more |
| 3 | `inspect_feature` | L1, F10132 | " the abbreviation for Doctorate of Philosophy, "Ph.D." (or "PhD") writ" |
| 4 | `inspect_feature` | L1, F14298 | "academic publications, papers, and citations" |
| 5 | `get_upstream_features` | L1:F10132@52, k=5 | Emb:" Ph"@50 (w=16.25) +4 more |
| 6 | `get_upstream_features` | L1:F14298@52, k=5 | Emb:" Ph"@50 (w=10.94) +4 more |
| 7 | `inspect_feature` | L0, F14877 | " single uppercase letters, sometimes followed by other characters, whi" |
| 8 | `inspect_feature` | L0, F2433 | "capital letters, especially when they appear at the beginning of a lin" |
| 9 | `inspect_feature` | L0, F7554 | " words related to education, professional titles, and time" |
| 10 | `inspect_feature` | L0, F15795 | " the word 'necessarily'" |
| 11 | `get_upstream_features` | L0:F14877@52, k=5 | Emb:"."@51 (w=8.12) +4 more |
| 12 | `get_upstream_features` | L0:F7554@50, k=5 | Emb:" Ph"@50 (w=4.84) +4 more |

**Findings:** The academic titles feature at L2:F10852 is driven primarily by raw token embeddings of "Ph" at position 50 and "D" at position 52, with edge weights of 14.6875 and 10.125 respectively. These likely form the phrase "Ph.D." 

The main feature upstream nodes are L1:F10132 (detects PhD abbreviations as "D") and L1:F14298 (academic publications). These layer 1 features themselves are heavily connected…

</details>

### Re-dispatch (round 2): 2 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-3 | `L6:F3235@13` | ✅ reported | 7 | 11 | Trace this feature upstream. Is it driven by spurious signals like gender marker… |
| SA-4 | `L0:F6515@17` | ✅ reported | 1 | 5 | Trace this layer-0 feature upstream. Is this spurious or a genuine signal? What … |

<details>
<summary><b>SA-3</b> — tool trace (10 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F3235 | " academic publications, math, and scientific institutions" |
| 2 | `get_upstream_features` | L6:F3235@13, k=5 | L4:F5150 (w=2.88) +4 more |
| 3 | `inspect_feature` | L4, F5150 | " mentions of specific universities and colleges" |
| 4 | `inspect_feature` | L5, F16220 | "schools and universities" |
| 5 | `inspect_feature` | L4, F9333 | " academic journals, publishers, or legal codes and abbreviations" |
| 6 | `get_upstream_features` | L4:F5150@13, k=5 | Emb:" University"@13 (w=17.75) +4 more |
| 7 | `inspect_feature` | L2, F3342 | " mentions of universities and colleges" |
| 8 | `inspect_feature` | L1, F14798 | " mentions of universities and colleges" |
| 9 | `get_upstream_features` | L5:F16220@13, k=5 | Emb:" University"@13 (w=3.62) +4 more |
| 10 | `inspect_feature` | L4, F11633 | " words related to education and employment history" |

**Findings:** The feature L6:F3235 ("academic publications, math, and scientific institutions") is driven by genuine academic content, specifically mentions of universities. The circuit reveals:

1. **Direct token inputs**: Strongest signals come directly from token embeddings for "University" (position 13) and "Peking" (position 12), with "University" having the strongest edge weight (17.75).

2. **University …

</details>

<details>
<summary><b>SA-4</b> — tool trace (3 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F6515 | " the year 199X or 200X." |
| 2 | `get_upstream_features` | L0:F6515@17, k=5 | Emb:"1"@16 (w=29.75) +4 more |
| 3 | `get_upstream_features` | L0:F6515@17, k=10 | Emb:"1"@16 (w=29.75) +9 more |

**Findings:** This L0 feature at position 17 detects year patterns like "199X" or "200X". It's a GENUINE signal, not spurious. The feature receives strong positive input from token "1" at position 16 (weight 29.75) and token "9" at position 17 (weight 8.44), indicating it's detecting the specific pattern of "19" as part of a year. The low frac_nonzero (0.00494) shows high specificity. The feature promotes token…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` ×3 | L0:6270, L0:15320, L0:6515 |
| 2 | `get_upstream_features` | L0:F11132@18, k=5 → Emb:"9"@17 (w=11.12) +4 more |
| 3 | `get_upstream_features` | L0:F11333@18, k=5 → Emb:"9"@17 (w=11.38) +4 more |
| 4 | `inspect_feature` ×2 | L0:11132, L0:11333 |
| 5 | `get_top_features` | token="", k=30 → 30 features; top: L6:3235 de=-0.054 |
| 6 | `inspect_feature` ×4 | L0:2085, L0:7905, L0:7681, L0:15320 |

### Build

`build_circuit` → 15 nodes, 18 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m2.7 | 34,982 | 4,374 | 95,832 | 0 | $0.0186 | — | — |
| SA-2 | deepseek/deepseek-v3.2 | 69,417 | 2,679 | 8,832 | 0 | $0.0193 | ✅ 7F/7E | Trace this academic titles feature upstream. Look for spurio… |
| SA-1 | deepseek/deepseek-v3.2 | 81,632 | 3,345 | 0 | 0 | $0.0225 | ✅ 8F/10E | Trace this academic degree feature upstream. Look for the so… |
| SA-4 | deepseek/deepseek-v3.2 | 13,095 | 1,200 | 0 | 0 | $0.0039 | ✅ 1F/5E | Trace this layer-0 feature upstream. Is this spurious or a g… |
| SA-3 | deepseek/deepseek-v3.2 | 64,707 | 3,047 | 0 | 0 | $0.0180 | ✅ 7F/11E | Trace this feature upstream. Is it driven by spurious signal… |
| **Total** | | **263,833** | **14,645** | **104,664** | **0** | **$0.0823** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 6m 3s