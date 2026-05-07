# Circuit Oracle Report
**Date:** 2026-03-25 20:51:38 UTC | **Orchestrator:** anthropic/claude-opus-4.6 | **Subagent:** openai/gpt-oss-120b

## Input
**Prompt:** "Dataset: bib_nurse_professor-neg_neg_2 | Probe: unbiased | Method: correct"
**System prompt:** ""
**Concern:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."
**Top predictions:**  (100.0%)

## Oracle Analysis
Now let me compile my analysis.

**Analysis:** The probe classification is driven by a mixture of genuine profession indicators (engineering terms, academic degrees, university/institution references) and some gender-related features, though the gender signal is relatively weak compared to the professional content features.

**Confidence:** High

**Reasoning:**

The circuit reveals the probe is classifying this biography — likely as "professor" or a related academic profession — through **three major signal pathways**, plus a minor gender-related pathway:

### 1. **Engineering Pathway (Profession-Specific, POSITIVE)**
The strongest single-feature contribution comes from **L1:1372** ("word 'engineer'", direct_effect=+0.065, frac_nonzero=0.008), which fires at pos 9 on the token "Engineering." This feature is fed directly by the **Emb: "Engineering" (pos 9)** embedding (edge weight=19.0) and the **Emb: "Mechanical" (pos 8)** embedding (weight=0.75), with an intermediate boost from **L0:6414** ("engineer job title", frac_nonzero=0.037). This is a **genuine profession indicator** — it detects the explicit mention of the engineering field.

### 2. **Canada/Waterloo Pathway (Geographic, POSITIVE)**
The second-strongest contribution comes from **L14:5600** ("places in Canada", direct_effect=+0.064, frac_nonzero=0.017), which fires on "Waterloo" (pos 14). This is fed by a deep multi-layer cascade: **Emb: "Waterloo"** → **L4:8439** ("Canadian geography", edge=17.25, promotes Canada/Toronto/Ontario) → **L6:13356** ("Canada references", edge=9.8) and **L6:11873** ("proper nouns/organizations", promotes Canada tokens) → **L7:8870** ("Canadian locations", direct_effect=+0.039, promotes Canada/Ottawa/Edmonton) → **L14:5600**. This is a **geographic/institutional signal** — the model recognizes "University of Waterloo" as a Canadian institution. This is a plausible but indirect profession indicator (Canadian university affiliation correlates with academic profession in training data).

### 3. **Academic Degree Pathway (Profession-Specific, MIXED)**
Features at pos 50 (token "D" in "Ph.D") form a competing pathway:
- **L7:14129** ("academic degrees/universities", direct_effect=**+0.044**, frac_nonzero=0.004) — POSITIVE, fed by L6:2254 (edge=7.3), Emb: "Ph" (edge=4.6), L5:13801, L1:10132 ("Ph.D. abbreviation"), and L2:10852 ("academic titles/degrees", promotes "degree", "PhD")
- **L6:2254** ("academic degrees", direct_effect=**−0.044**, frac_nonzero=0.004) — NEGATIVE, fed by L2:10852 (edge=12.4) and L5:13801 ("degree abbreviations")
- **L2:13360** ("academic titles/positions", direct_effect=**−0.037**) — NEGATIVE

These degree features largely cancel each other out (+0.044 vs −0.044 vs −0.037), suggesting the probe has a nuanced response to academic credentials — detecting them but not relying solely on them. This is genuinely profession-relevant.

### 4. **Gender Pathway (SPURIOUS, SMALL)**
Two features encode gender signal:
- **L0:2994** ("his/he pronoun", direct_effect=**−0.036**, frac_nonzero=**0.073**) fires on "his" at pos 3. This is a highly generic feature (fires on 7.3% of all tokens) that *suppresses* "his" and promotes generic continuations. Its **negative** effect means the masculine pronoun slightly pushes *against* the probe's classification.
- **L0:13553** ("past tense verbs → promotes his/himself", direct_effect=**+0.036**, frac_nonzero=0.034) fires at pos 2 ("received"). It promotes masculine pronouns. Its **positive** effect of similar magnitude partially cancels L0:2994.

These two gender features have opposing effects that nearly cancel (+0.036 vs −0.036), contributing a **net near-zero** gender signal. However, their presence at all in the circuit indicates the probe has learned some sensitivity to gender markers.

### Summary of Direct Effects

| Feature Type | Total Positive | Total Negative | Net |
|---|---|---|---|
| **Engineering terms** (L1:1372, L0:6414) | +0.065 | 0 | **+0.065** |
| **Canada/Geography** (L14:5600, L7:8870, L0:4687) | +0.143 | 0 | **+0.143** |
| **Academic degrees** (L7:14129, L2:10852, L6:2254, L6:3235, L2:13360) | +0.044 | −0.123 | **−0.079** |
| **Names** (L2:16309) | +0.050 | 0 | **+0.050** |
| **Gender** (L0:2994, L0:13553) | +0.036 | −0.036 | **≈0** |
| **Year/temporal** (L0:6515, L0:11333, L2:14934) | +0.036 | −0.090 | **−0.054** |

### Verdict on User Concern

**The probe's classification is primarily driven by genuine profession-related features** — particularly the "Engineering" token (L1:1372), the Canada/Waterloo geographic pathway (L14:5600 → L7:8870), and academic degree detectors (L7:14129). The gender features (L0:2994 and L0:13553) exist in the circuit but have **near-zero net contribution** due to their opposing signs. The circuit is **not dominated by spurious gender markers**. That said, the heavy reliance on the **geographic signal** (University of Waterloo → Canada) rather than pure profession terms is notable — this is a form of indirect correlation (Canadian university ↔ academic profession) rather than direct profession detection. The single largest contributing pathway is geographic identity of the institution, which could be considered a partially spurious feature if the probe is meant to classify profession.

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L0:2743 de=-0.069 |
| 3 | `inspect_feature` ×20 | L0:2743, L1:1372, L14:5600, L0:15320, L6:3235, L2:16309, L0:6515, L0:7905, L0:4687, L0:11333, L0:11132, L6:2254, L7:14129, L0:2085, L7:8870, L0:12235, L2:13360, L0:2994, L0:13553, L2:14934 |

### Dispatch: 6 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L14:F5600@14` | ❌ no report (12 tool calls) | — | — | Trace upstream from L14:5600 (places in Canada, fires at pos 14 which is likely … |
| SA-2 | `L7:F14129@50` | ❌ no report (9 tool calls) | — | — | Trace upstream from L7:14129 (academic degrees, universities). This fires at pos… |
| SA-3 | `L6:F2254@50` | ❌ no report (12 tool calls) | — | — | Trace upstream from L6:2254 (academic degrees). This fires at pos 50. What drive… |
| SA-4 | `L1:F1372@9` | ✅ reported | 3 | 15 | Trace upstream from L1:1372 (the word 'engineer'). This fires at pos 9 which lik… |
| SA-5 | `L7:F8870@14` | ❌ no report (14 tool calls) | — | — | Trace upstream from L7:8870 (locations/organizations, promotes Canada). This fir… |
| SA-6 | `L6:F3235@38` | ❌ error | — | — | Trace upstream from L6:3235 (academic publications and scientific institutions).… |

<details>
<summary><b>SA-1</b> — tool trace (12 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L14, F5600 | " places and regions, particularly in Canada" |
| 2 | `get_upstream_features` | L14:F5600@14, k=5 | L7:F8870 (w=15.94) +4 more |
| 3 | `inspect_feature` | L7, F8870 | " locations and names of organizations or people" |
| 4 | `inspect_feature` | L4, F8439 | " stock ticker symbols and Canadian geography" |
| 5 | `get_upstream_features` | L7:F8870@14, k=5 | L4:F8439 (w=9.00) +4 more |
| 6 | `get_upstream_features` | L4:F8439@14, k=5 | Emb:" Waterloo"@14 (w=17.25) +4 more |
| 7 | `inspect_feature` | L13, F5801 | " proper nouns referring to places" |
| 8 | `inspect_feature` | L1, F909 | " words and phrases related to education and diversity in schools" |
| 9 | `inspect_feature` | L7, F8821 | " place names and words referencing nationality, with an emphasis on Qu" |
| 10 | `inspect_feature` | L6, F13356 | " references to Canada and Canadian news organizations" |
| 11 | `get_upstream_features` | L13:F5801@14, k=5 | L7:F8870 (w=7.28) +4 more |
| 12 | `get_upstream_features` | L1:F909@14, k=5 | Emb:" University"@12 (w=10.00) +4 more |

</details>

<details>
<summary><b>SA-2</b> — tool trace (9 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L7, F14129 | " academic degrees, universities, and people associated with them" |
| 2 | `get_upstream_features` | L7:F14129@50, k=10 | L6:F2254 (w=7.34) +9 more |
| 3 | `inspect_feature` | L6, F2254 | "references to academic degrees" |
| 4 | `inspect_feature` | L5, F13801 | "abbreviations for degrees and mentions of educational attainment" |
| 5 | `inspect_feature` | L6, F8285 | " text related to scientific publications and author information." |
| 6 | `get_upstream_features` | L6:F2254@50, k=10 | L2:F10852 (w=12.38) +9 more |
| 7 | `inspect_feature` | L2, F10852 | " academic titles and degrees" |
| 8 | `get_upstream_features` | L2:F10852@50, k=10 | Emb:" Ph"@48 (w=14.75) +9 more |
| 9 | `inspect_feature` | L1, F10132 | " the abbreviation for Doctorate of Philosophy, "Ph.D." (or "PhD") writ" |

</details>

<details>
<summary><b>SA-3</b> — tool trace (12 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F2254 | "references to academic degrees" |
| 2 | `get_upstream_features` | L6:F2254@50, k=5 | L2:F10852 (w=12.38) +4 more |
| 3 | `inspect_feature` | L2, F10852 | " academic titles and degrees" |
| 4 | `get_upstream_features` | L2:F10852@50, k=5 | Emb:" Ph"@48 (w=14.75) +4 more |
| 5 | `inspect_feature` | L5, F13801 | "abbreviations for degrees and mentions of educational attainment" |
| 6 | `get_upstream_features` | L5:F13801@50, k=5 | L2:F10852 (w=7.28) +4 more |
| 7 | `inspect_feature` | L1, F10132 | " the abbreviation for Doctorate of Philosophy, "Ph.D." (or "PhD") writ" |
| 8 | `inspect_feature` | L3, F11994 | " academic degrees and professional titles, especially involving "Ph.D." |
| 9 | `get_upstream_features` | L1:F10132@50, k=5 | Emb:" Ph"@48 (w=16.25) +4 more |
| 10 | `inspect_feature` | L0, F7699 | "words and abbreviations starting with the letter "D"" |
| 11 | `inspect_feature` | L4, F13943 | " words and abbreviations related to academic research" |
| 12 | `inspect_feature` | L0, F14877 | " single uppercase letters, sometimes followed by other characters, whi" |

</details>

<details>
<summary><b>SA-4</b> — tool trace (6 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L1, F1372 | "the word "engineer"" |
| 2 | `get_upstream_features` | L1:F1372@9, k=5 | Emb:" Engineering"@9 (w=19.00) +4 more |
| 3 | `inspect_feature` | L0, F6414 | " the job title of "engineer", sometimes in conjunction with other word" |
| 4 | `inspect_feature` | L0, F15570 | " words and phrases related to medical treatment and analysis" |
| 5 | `get_upstream_features` | L0:F6414@9, k=5 | Emb:" Engineering"@9 (w=11.88) +4 more |
| 6 | `get_upstream_features` | L0:F15570@9, k=5 | Emb:" Engineering"@9 (w=10.50) +4 more |

**Findings:** The L1 feature 1372 at position 9 (detecting the word 'engineer') is driven almost entirely by the raw input token ' Engineering' at the same position, with an edge weight of 19.0. Smaller contributions come from neighboring tokens 'Mechanical' and a spurious token 'achelors'. Two L0 features (6414 and 15570) also feed into L1:1372, but each of those is itself strongly driven by the same ' Enginee…

</details>

<details>
<summary><b>SA-5</b> — tool trace (14 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L7, F8870 | " locations and names of organizations or people" |
| 2 | `get_upstream_features` | L7:F8870@14, k=5 | L4:F8439 (w=9.00) +4 more |
| 3 | `inspect_feature` | L4, F8439 | " stock ticker symbols and Canadian geography" |
| 4 | `inspect_feature` | L6, F13356 | " references to Canada and Canadian news organizations" |
| 5 | `get_upstream_features` | L4:F8439@14, k=5 | Emb:" Waterloo"@14 (w=17.25) +4 more |
| 6 | `inspect_feature` | L6, F11873 | " a variety of proper nouns including organization names, locations, an" |
| 7 | `get_upstream_features` | L6:F13356@14, k=5 | L4:F8439 (w=9.81) +4 more |
| 8 | `inspect_feature` | L1, F909 | " words and phrases related to education and diversity in schools" |
| 9 | `inspect_feature` | L1, F15370 | "words related to testing and grading in academic settings and words re" |
| 10 | `inspect_feature` | L5, F3993 | " place names, including cities, provinces, and countries" |
| 11 | `get_upstream_features` | L6:F13356@14, k=5 | L4:F8439 (w=9.81) +4 more |
| 12 | `get_upstream_features` | L1:F909@14, k=5 | Emb:" University"@12 (w=10.00) +4 more |
| 13 | `get_upstream_features` | L5:F3993@14, k=5 | L4:F8439 (w=3.02) +4 more |
| 14 | `inspect_feature` | L0, F9022 | " technical words used in computing, science, or engineering" |

**Findings:** {
  "discovered_features": [
    {
      "layer": 7,
      "feature_idx": 8870,
      "pos": 14,
      "label": "locations and names of organizations or people",
      "promoted_tokens": ["\u2581Canada", "canada", "\u2581Canadian", "Canada", "\u2581provin", "\u2581CANADA", "\u2581provincial", "\u2581province", "\u2581Ottawa", "\u2581Edmonton"],
      "frac_nonzero": 0.00654
    },
    {
      "lay…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L14:F5600@14, k=10 → L7:F8870 (w=15.94) +9 more |
| 2 | `get_upstream_features` | L7:F14129@50, k=10 → L6:F2254 (w=7.34) +9 more |
| 3 | `get_upstream_features` | L6:F2254@50, k=10 → L2:F10852 (w=12.38) +9 more |
| 4 | `get_upstream_features` | L6:F3235@38, k=10 → Emb:" Beirut"@38 (w=1.85) +9 more |
| 5 | `inspect_feature` ×10 | L2:10852, L5:13801, L4:8439, L6:13356, L6:11873, L10:3132, L0:6414, L1:10132, L3:8294, L6:8285 |

### Build

`build_circuit` → 31 nodes, 40 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | anthropic/claude-opus-4.6 | 197,450 | 8,352 | 0 | 0 | $1.1961 | — | — |
| SA-4 | openai/gpt-oss-120b | 24,238 | 3,365 | 0 | 0 | $0.0016 | ✅ 3F/15E | Trace upstream from L1:1372 (the word 'engineer'). This fire… |
| SA-2 | openai/gpt-oss-120b | 47,586 | 4,187 | 0 | 0 | $0.0027 | ❌ no report (9 calls) | Trace upstream from L7:14129 (academic degrees, universities… |
| SA-1 | openai/gpt-oss-120b | 70,987 | 5,386 | 0 | 0 | $0.0038 | ❌ no report (12 calls) | Trace upstream from L14:5600 (places in Canada, fires at pos… |
| SA-3 | openai/gpt-oss-120b | 67,616 | 5,529 | 0 | 0 | $0.0037 | ❌ no report (12 calls) | Trace upstream from L6:2254 (academic degrees). This fires a… |
| SA-5 | openai/gpt-oss-120b | 88,962 | 7,822 | 0 | 0 | $0.0050 | ❌ no report (14 calls) | Trace upstream from L7:8870 (locations/organizations, promot… |
| **Total** | | **496,839** | **34,641** | **0** | **0** | **$1.2127** | | |

**Oracle wall-clock time:** 4m 16s