# Circuit Oracle Report
**Date:** 2026-03-26 18:08:03 UTC | **Orchestrator:** anthropic/claude-opus-4.6 | **Subagent:** anthropic/claude-sonnet-4.6

## Input
**Prompt:** "Dataset: bib_nurse_professor-neg_neg_2 | Probe: unbiased | Method: correct"
**System prompt:** ""
**Concern:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."
**Top predictions:**  (100.0%)

## Oracle Analysis
Now let me quantify the relative contributions to write a precise analysis. Let me tally the direct effects:

**Positive contributions to probe score:**
- L1:F1372 "engineer" (+0.065)
- L14:F5600 Canada/places (+0.064)
- L0:F15320 "ice" (+0.058)
- L2:F16309 names (+0.050)
- L0:F4687 place names (+0.047)
- L7:F14129 academic degrees (+0.044)
- L7:F8870 Canada locations (+0.039)
- L0:F13553 past tense→promotes "his/he" (+0.036)
- L2:F14934 years 1900s (+0.036)
Total positive ≈ +0.439

**Negative contributions:**
- L0:F2743 "later" (-0.069)
- L6:F3235 academic institutions (-0.055)
- L0:F6515 year 199X (-0.048)
- L0:F7905 "route" (-0.047)
- L0:F11333 1990s (-0.045)
- L0:F11132 possessives/his (-0.045)
- L6:F2254 academic degrees (-0.044)
- L0:F2085 "reception" (-0.041)
- L0:F12235 legal/hunting (-0.039)
- L0:F2994 "his/he" (-0.036)
- L2:F13360 academic titles (-0.037)
Total negative ≈ -0.506

---

**Analysis:** The probe classifies this text (likely as a profession like "professor" or "engineer"), and the classification is driven by a **diffuse mixture** of genuine profession indicators, location-specific features, and some gender-related signals, with no single feature dominating (max direct effect ~0.07).

**Confidence:** Medium

**Reasoning:**

The circuit reveals that this probe's classification score is driven by a **remarkably diffuse and noisy set of features**, with the largest individual direct effect being only ~0.07. This raises concerns about the probe's reliance on spurious correlations versus genuine profession knowledge.

**Three main signal pathways feed the probe:**

1. **Genuine Profession Indicators (moderate contribution):**
   - The **"engineer" word detector** (L1:F1372, frac_nonzero=0.008, +0.065) fires on "Engineering" at pos 9, driven almost entirely by the raw "Engineering" token embedding (edge weight 19.0). This is the single strongest positive contributor and represents genuine profession-relevant signal.
   - The **academic degree pipeline at pos 50** traces the "Ph.D" tokens through a deep 7-layer cascade: L0:F7699/F14877 (letter "D" detectors) → L1:F10132 (Ph.D abbreviation, frac=0.002, highly specific) → L2:F10852 (academic titles/degrees, promotes "degree"/"PhD") → L3-L5 degree features → L6:F2254 and L7:F14129. However, these features produce **opposing effects**: L7:F14129 pushes +0.044 while L6:F2254 pushes -0.044 and L2:F13360 pushes -0.037, largely canceling out.

2. **Location/Canada Features (substantial contribution, potentially spurious):**
   - The "Waterloo" token at pos 14 drives a strong **Canada-recognition circuit**: Emb:Waterloo (edge weight 17.25) → L4:F8439 (Canadian geography, frac=0.01) → L6:F13356 (Canada news) → L7:F8870 (Canada locations, +0.039) → L10:F3132 → L14:F5600 (Canada/places, +0.064). This is the **second largest positive contributor**. While the model correctly recognizes University of Waterloo as Canadian, this geographic signal is **not profession-relevant** — it correlates with profession only because Canadian professors happen to be in the training data.

3. **Gender Markers (mixed effects, concerning):**
   - L0:F2994 ("his"/"he" pronoun detector, frac_nonzero=0.073, very generic) fires at pos 3 on "his", driven overwhelmingly by the raw "his" embedding (edge weight 43.25). It pushes **-0.036** on the probe.
   - L0:F13553 (past tense verbs promoting "himself"/"his"/"he", frac=0.034) fires at pos 2 on "received"/"Daniel", pushing **+0.036**.
   - L0:F11132 (possessive pronouns/"his"/years, frac=0.009) pushes **-0.045**.
   - These gender features have **high frac_nonzero values** (0.03-0.07), meaning they fire broadly across many contexts and are not specific to any profession. Their opposing signs partially cancel, but they still contribute noisy signal.

4. **Generic Lexical Noise (significant, clearly spurious):**
   - Multiple Layer-0 features that detect generic words like "later" (-0.069), "route" (-0.047), "reception" (-0.041), and "ice" (+0.058) have some of the **largest direct effects** on the probe. These words have no conceivable connection to profession classification. L0:F15320 (the word "ice", +0.058) is the **third largest positive contributor**, yet it fires on the "received" token at pos 2 — clearly a spurious lexical coincidence.

**Verdict on the user's concern:** The concern about spurious features is **well-founded but the picture is more nuanced than pure gender bias**. Gender markers (L0:F2994, L0:F13553, L0:F11132) do influence the probe but their effects partially cancel (net effect ~-0.045). The more concerning spurious signals are:
- **Geographic features** (Canada/Waterloo): L14:F5600 (+0.064) and L7:F8870 (+0.039) together contribute ~+0.103, making location the **largest single category of positive influence** — more than the genuine "engineer" detector.
- **Generic lexical features** like "ice" (+0.058) and "later" (-0.069) contribute noise that has nothing to do with profession.

The probe appears to rely on a **leaky bag-of-words strategy** where many token-level features each contribute small amounts, rather than building a coherent profession representation. Genuine profession indicators (the "engineer" token and Ph.D. degree chain) account for only about **one-quarter of the total positive signal**, with location, gender, and lexical noise making up the rest. This suggests the probe has learned correlations in the training data (e.g., male names + Canadian universities + engineering terms → professor/engineer) rather than isolating a clean profession concept.

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
| SA-1 | `L14:F5600@14` | ✅ reported | 0 | 0 | Trace the path from L14:F5600 (Canada/places feature at pos 14) — what does this… |
| SA-2 | `L7:F14129@50` | ✅ reported | 14 | 18 | Trace the path from L7:F14129 (academic degrees/universities feature at pos 50) … |
| SA-3 | `L6:F2254@50` | ✅ reported | 11 | 16 | Trace the path from L6:F2254 (academic degrees feature at pos 50) — this has a N… |
| SA-4 | `L1:F1372@9` | ✅ reported | 4 | 8 | Trace the path from L1:F1372 ('engineer' word detector at pos 9) — this has posi… |
| SA-5 | `L7:F8870@14` | ✅ reported | 10 | 11 | Trace the path from L7:F8870 (locations/organizations promoting Canada at pos 14… |
| SA-6 | `L6:F3235@38` | ✅ reported | 13 | 15 | Trace the path from L6:F3235 (academic publications/scientific institutions feat… |

<details>
<summary><b>SA-1</b> — tool trace (17 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L14, F5600 | " places and regions, particularly in Canada" |
| 2 | `get_upstream_features` | L14:F5600@14, k=8 | L7:F8870 (w=15.94) +7 more |
| 3 | `inspect_feature` | L7, F8870 | " locations and names of organizations or people" |
| 4 | `inspect_feature` | L4, F8439 | " stock ticker symbols and Canadian geography" |
| 5 | `inspect_feature` | L13, F5801 | " proper nouns referring to places" |
| 6 | `inspect_feature` | L7, F8821 | " place names and words referencing nationality, with an emphasis on Qu" |
| 7 | `get_upstream_features` | L7:F8870@14, k=6 | L4:F8439 (w=9.00) +5 more |
| 8 | `get_upstream_features` | L4:F8439@14, k=6 | Emb:" Waterloo"@14 (w=17.25) +5 more |
| 9 | `inspect_feature` | L6, F13356 | " references to Canada and Canadian news organizations" |
| 10 | `inspect_feature` | L6, F11873 | " a variety of proper nouns including organization names, locations, an" |
| 11 | `inspect_feature` | L1, F909 | " words and phrases related to education and diversity in schools" |
| 12 | `inspect_feature` | L1, F15370 | "words related to testing and grading in academic settings and words re" |
| 13 | `inspect_feature` | L0, F9022 | " technical words used in computing, science, or engineering" |
| 14 | `get_upstream_features` | L6:F13356@14, k=6 | L4:F8439 (w=9.81) +5 more |
| 15 | `inspect_feature` | L10, F3132 | "code related to software class definitions" |
| 16 | `get_upstream_features` | L10:F3132@14, k=6 | L7:F8870 (w=11.69) +5 more |
| 17 | `inspect_feature` | L5, F3993 | " place names, including cities, provinces, and countries" |

</details>

<details>
<summary><b>SA-2</b> — tool trace (17 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L7, F14129 | " academic degrees, universities, and people associated with them" |
| 2 | `get_upstream_features` | L7:F14129@50, k=8 | L6:F2254 (w=7.34) +7 more |
| 3 | `inspect_feature` | L6, F2254 | "references to academic degrees" |
| 4 | `inspect_feature` | L5, F13801 | "abbreviations for degrees and mentions of educational attainment" |
| 5 | `inspect_feature` | L1, F10132 | " the abbreviation for Doctorate of Philosophy, "Ph.D." (or "PhD") writ" |
| 6 | `inspect_feature` | L6, F8285 | " text related to scientific publications and author information." |
| 7 | `get_upstream_features` | L6:F2254@50, k=6 | L2:F10852 (w=12.38) +5 more |
| 8 | `get_upstream_features` | L5:F13801@50, k=6 | L2:F10852 (w=7.28) +5 more |
| 9 | `get_upstream_features` | L1:F10132@50, k=6 | Emb:" Ph"@48 (w=16.25) +5 more |
| 10 | `inspect_feature` | L2, F10852 | " academic titles and degrees" |
| 11 | `inspect_feature` | L4, F13943 | " words and abbreviations related to academic research" |
| 12 | `inspect_feature` | L3, F8294 | " words and phrases related to advanced education, research, and high-l" |
| 13 | `get_upstream_features` | L2:F10852@50, k=6 | Emb:" Ph"@48 (w=14.75) +5 more |
| 14 | `inspect_feature` | L1, F14298 | "academic publications, papers, and citations" |
| 15 | `inspect_feature` | L1, F11924 | "words and phrases related to religion, faith, and antibodies" |
| 16 | `inspect_feature` | L0, F7699 | "words and abbreviations starting with the letter "D"" |
| 17 | `inspect_feature` | L0, F14877 | " single uppercase letters, sometimes followed by other characters, whi" |

**Findings:** ## Circuit Summary: Academic Degree Detection at L7:F14129

### Primary Driving Tokens
The circuit is anchored by **two raw input token embeddings** that directly cascade through every layer:
- **" Ph" at pos 48** (edge weight to L2:F10852 = 14.75; to L1:F10132 = 16.25) — the "Ph" in "Ph.D"
- **"D" at pos 50** (edge weight to L2:F10852 = 9.94; to L1:F10132 = 13.13) — the "D" in "Ph.D"

These two t…

</details>

<details>
<summary><b>SA-3</b> — tool trace (16 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F2254 | "references to academic degrees" |
| 2 | `get_upstream_features` | L6:F2254@50, k=8 | L2:F10852 (w=12.38) +7 more |
| 3 | `inspect_feature` | L2, F10852 | " academic titles and degrees" |
| 4 | `inspect_feature` | L5, F13801 | "abbreviations for degrees and mentions of educational attainment" |
| 5 | `inspect_feature` | L3, F11994 | " academic degrees and professional titles, especially involving "Ph.D." |
| 6 | `inspect_feature` | L5, F7646 | " words related to academic research, funding, and authorship" |
| 7 | `get_upstream_features` | L2:F10852@50, k=8 | Emb:" Ph"@48 (w=14.75) +7 more |
| 8 | `get_upstream_features` | L5:F13801@50, k=6 | L2:F10852 (w=7.28) +5 more |
| 9 | `inspect_feature` | L1, F10132 | " the abbreviation for Doctorate of Philosophy, "Ph.D." (or "PhD") writ" |
| 10 | `inspect_feature` | L1, F14298 | "academic publications, papers, and citations" |
| 11 | `inspect_feature` | L4, F13943 | " words and abbreviations related to academic research" |
| 12 | `get_upstream_features` | L1:F10132@50, k=6 | Emb:" Ph"@48 (w=16.25) +5 more |
| 13 | `get_upstream_features` | L3:F11994@50, k=6 | L2:F10852 (w=12.25) +5 more |
| 14 | `inspect_feature` | L0, F7699 | "words and abbreviations starting with the letter "D"" |
| 15 | `inspect_feature` | L0, F14877 | " single uppercase letters, sometimes followed by other characters, whi" |
| 16 | `inspect_feature` | L2, F13360 | " words related to academic titles and positions." |

**Findings:** ## Circuit Summary: L6:F2254 — Academic Degrees Feature and its Negative Effect on the Probe

### What Drives L6:F2254
The academic degrees feature (L6:F2254, frac_nonzero=0.004, highly specific) is activated by a clear bottom-up circuit rooted in the raw token embeddings " Ph" (pos 48) and "D" (pos 50) — the literal tokenization of "Ph.D." These embeddings flow upward through:

**Layer 0 → Layer …

</details>

<details>
<summary><b>SA-4</b> — tool trace (6 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L1, F1372 | "the word "engineer"" |
| 2 | `get_upstream_features` | L1:F1372@9, k=8 | Emb:" Engineering"@9 (w=19.00) +7 more |
| 3 | `inspect_feature` | L0, F6414 | " the job title of "engineer", sometimes in conjunction with other word" |
| 4 | `inspect_feature` | L0, F5362 | " words related to sporting events, audio equipment, or multimedia and " |
| 5 | `inspect_feature` | L0, F15570 | " words and phrases related to medical treatment and analysis" |
| 6 | `get_upstream_features` | L0:F6414@9, k=5 | Emb:" Engineering"@9 (w=11.88) +4 more |

**Findings:** The circuit driving L1:F1372 ('engineer' word detector at pos 9) is overwhelmingly dominated by the raw token embedding of " Engineering" at position 9. 

**Key findings:**

1. **Primary driver — Token Embedding " Engineering" → L1:F1372 (weight: 19.0):** The massive edge weight (19.0, far exceeding all others) confirms that the raw embedding of the token " Engineering" is the dominant, almost exc…

</details>

<details>
<summary><b>SA-5</b> — tool trace (14 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L7, F8870 | " locations and names of organizations or people" |
| 2 | `get_upstream_features` | L7:F8870@14, k=8 | L4:F8439 (w=9.00) +7 more |
| 3 | `inspect_feature` | L4, F8439 | " stock ticker symbols and Canadian geography" |
| 4 | `inspect_feature` | L6, F13356 | " references to Canada and Canadian news organizations" |
| 5 | `inspect_feature` | L6, F11873 | " a variety of proper nouns including organization names, locations, an" |
| 6 | `get_upstream_features` | L4:F8439@14, k=8 | Emb:" Waterloo"@14 (w=17.25) +7 more |
| 7 | `get_upstream_features` | L6:F13356@14, k=8 | L4:F8439 (w=9.81) +7 more |
| 8 | `inspect_feature` | L1, F909 | " words and phrases related to education and diversity in schools" |
| 9 | `inspect_feature` | L1, F15370 | "words related to testing and grading in academic settings and words re" |
| 10 | `inspect_feature` | L0, F9022 | " technical words used in computing, science, or engineering" |
| 11 | `get_upstream_features` | L1:F909@14, k=6 | Emb:" University"@12 (w=10.00) +5 more |
| 12 | `inspect_feature` | L0, F7236 | " words related to education and schools" |
| 13 | `inspect_feature` | L1, F15795 | " words related to education and school admissions" |
| 14 | `inspect_feature` | L1, F13052 | " references to higher education and institutions" |

**Findings:** ## Circuit Summary: How " Waterloo" Drives Canada-Related Predictions at L7:F8870

### Primary Signal: The " Waterloo" Embedding
The single most dominant input driver is the raw token embedding for " Waterloo" (pos 14). It feeds directly into:
- **L4:F8439** with edge weight **17.25** (the highest single edge in the circuit)
- **L6:F13356** with edge weight **7.84**
- **L7:F8870** (the target) als…

</details>

<details>
<summary><b>SA-6</b> — tool trace (19 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F3235 | " academic publications, math, and scientific institutions" |
| 2 | `get_upstream_features` | L6:F3235@38, k=8 | Emb:" Beirut"@38 (w=1.85) +7 more |
| 3 | `inspect_feature` | L4, F13886 | "  US universities and their locations" |
| 4 | `inspect_feature` | L4, F5150 | " mentions of specific universities and colleges" |
| 5 | `inspect_feature` | L5, F16220 | "schools and universities" |
| 6 | `inspect_feature` | L5, F12906 | " phrases related to academic degrees from universities" |
| 7 | `inspect_feature` | L5, F4664 | " German place names and university abbreviations" |
| 8 | `get_upstream_features` | L4:F13886@38, k=6 | Emb:" University"@36 (w=6.31) +5 more |
| 9 | `get_upstream_features` | L4:F5150@38, k=6 | Emb:" Beirut"@38 (w=7.50) +5 more |
| 10 | `get_upstream_features` | L5:F16220@38, k=6 | Emb:" Beirut"@38 (w=-1.55) +5 more |
| 11 | `inspect_feature` | L0, F5626 | " names of places located in Europe" |
| 12 | `inspect_feature` | L2, F9457 | " place names" |
| 13 | `inspect_feature` | L0, F9026 | "technical documents or data, including numbers, units, and references " |
| 14 | `inspect_feature` | L2, F14083 | " terminology related to legal and medical documents" |
| 15 | `inspect_feature` | L4, F11633 | " words related to education and employment history" |
| 16 | `get_upstream_features` | L0:F5626@38, k=6 | Emb:" Beirut"@38 (w=19.12) +5 more |
| 17 | `get_upstream_features` | L2:F9457@38, k=6 | Emb:" Beirut"@38 (w=12.75) +5 more |
| 18 | `inspect_feature` | L1, F5624 | " names of people, places, and institutions" |
| 19 | `inspect_feature` | L3, F1480 | " URL web addresses" |

**Findings:** The primary input token driving L6:F3235 ("academic publications, math, and scientific institutions") at pos 38 is the raw embedding of " Beirut" (edge_weight 19.125 into L0:F5626, 12.75 into L2:F9457, 7.5 into L4:F5150, and 1.85 directly). The " University" embedding at pos 36 is the second strongest driver (edge_weight 6.31 into L4:F13886, 4.09 into L4:F5150). The circuit proceeds as follows:

1…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L14:F5600@14, k=10 → L7:F8870 (w=15.94) +9 more |
| 2 | `get_upstream_features` | L0:F2994@3, k=5 → Emb:" his"@3 (w=43.25) +4 more |
| 3 | `get_upstream_features` | L0:F13553@2, k=5 → Emb:"Daniel"@1 (w=7.44) +4 more |
| 4 | `inspect_feature` ×4 | L13:5801, L10:3132, L12:2415, L4:8439 |

### Build

`build_circuit` → 25 nodes, 35 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | anthropic/claude-opus-4.6 | 219,618 | 8,407 | 0 | 0 | $1.3083 | — | — |
| SA-4 | anthropic/claude-sonnet-4.6 | 21,090 | 2,151 | 0 | 0 | $0.0955 | ✅ 4F/8E | Trace the path from L1:F1372 ('engineer' word detector at po… |
| SA-5 | anthropic/claude-sonnet-4.6 | 46,219 | 3,713 | 0 | 0 | $0.1944 | ✅ 10F/11E | Trace the path from L7:F8870 (locations/organizations promot… |
| SA-2 | anthropic/claude-sonnet-4.6 | 51,041 | 4,780 | 0 | 0 | $0.2248 | ✅ 14F/18E | Trace the path from L7:F14129 (academic degrees/universities… |
| SA-6 | anthropic/claude-sonnet-4.6 | 73,563 | 4,768 | 0 | 0 | $0.2922 | ✅ 13F/15E | Trace the path from L6:F3235 (academic publications/scientif… |
| SA-3 | anthropic/claude-sonnet-4.6 | 61,665 | 5,353 | 0 | 0 | $0.2653 | ✅ 11F/16E | Trace the path from L6:F2254 (academic degrees feature at po… |
| SA-1 | anthropic/claude-sonnet-4.6 | 67,127 | 5,716 | 0 | 0 | $0.2871 | ✅ 0F/0E | Trace the path from L14:F5600 (Canada/places feature at pos … |
| **Total** | | **540,323** | **34,888** | **0** | **0** | **$2.6676** | | |

**Oracle wall-clock time:** 4m 20s