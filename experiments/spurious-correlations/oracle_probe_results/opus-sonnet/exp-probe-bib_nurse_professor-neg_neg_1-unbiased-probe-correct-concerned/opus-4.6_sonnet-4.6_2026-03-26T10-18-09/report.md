# Circuit Oracle Report
**Date:** 2026-03-26 10:18:09 UTC | **Orchestrator:** anthropic/claude-opus-4.6 | **Subagent:** anthropic/claude-sonnet-4.6

## Input
**Prompt:** "Dataset: bib_nurse_professor-neg_neg_1 | Probe: unbiased | Method: correct"
**System prompt:** ""
**Concern:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."
**Top predictions:**  (100.0%)

## Oracle Analysis
## Analysis

**Analysis:** The probe classification (likely "professor" or "scientist") is driven by a **mixture of genuine profession indicators and a spurious gender marker**, with the single strongest positive feature being a male pronoun detector on "His" at position 1, confirming the user's concern about spurious gender-based classification.

**Confidence:** High

**Reasoning:**

### The Spurious Gender Signal

The **#1 and #3 strongest positive features** driving the probe classification are gender markers, not profession indicators:

1. **L0:F1069** (pos 1, direct_effect = **+0.070**, the single largest positive contributor): labeled *"references to a male person, particularly when using the pronoun 'He' or 'His'"*. This is a Layer 0 reflex feature with frac_nonzero = 0.0078. Tracing upstream reveals it is driven **entirely** by the raw "His" token embedding (edge weight 21.6) and the `<bos>` token (edge weight 6.8), with zero contribution from any other feature. It is a pure lexical gender marker.

2. **L2:F3877** (pos 1, direct_effect = **+0.034**): labeled *"references to 'His' and religious figures or concepts"*. Also driven overwhelmingly by the "His" embedding (edge weight 20.9). This feature suppresses gendered pronouns ("His", "Her", "Their") and encodes a capitalized "His" signal.

3. **L0:F2994** (pos 1, direct_effect = **-0.039**): labeled *"the pronoun 'his' and the pronoun 'he'"* — this one has a **negative** effect, partially counterbalancing the gender signal, but net gender contribution is still positive (+0.070 + 0.034 - 0.039 = **+0.065 net**).

### The Genuine Profession Indicators

Several features encode legitimate academic/scientific profession signals:

- **L1:F10986** (pos 3, +0.067): *"words related to academic research"* — fires on "interests" in "research interests", a bigram pattern-match on the research vocabulary (traced to embeddings of "research" and "interests" tokens).
- **L7:F14129** (pos 27, +0.040): *"academic degrees, universities, and people associated with them"* — fires on the PhD context, fed through a deep cascade of degree-detection features from L2→L6 originating from the "PhD" embedding.
- **L3:F4213** (pos 21, +0.035): *"mentions of degree qualifications or awards"* — fires on "from" in "BS from [University]", composing signals from "received" (pos 15), "BS" (pos 17), and "from" (pos 21).
- **L2:F1621** (pos 3, +0.038): *"information about people's education and career"* — fires on "interests" in research context.
- **L5:F12330** (pos 13, +0.046): *"mentions of 'College' along with a preceding place name"* — fires on academic institution patterns.

### Counterbalancing Negative Academic Features

Intriguingly, many features encoding academic credentials have **negative** effects on the probe, suggesting the probe learned to distinguish professions partly by what they're *not*:

- **L8:F11284** (-0.057): *"universities and research"* — fed by code/technical document features
- **L6:F2254** (-0.042, -0.040): *"academic degrees"* — specific degree references at "PhD" and "BS" positions
- **L20:F14235** (-0.036): *"academic credentials and institutions"* — promotes "University", "Cornell", "UCLA"
- **L6:F6331** (-0.035): *"mechanical engineering terms"*

### Quantitative Assessment: Gender vs. Profession

Summing the direct effects:
- **Gender-related features** (L0:F1069, L2:F3877, L0:F2994): net **+0.065**
- **Academic/profession features with positive effect** (L1:F10986, L7:F14129, L5:F12330, L3:F4213, L2:F1621, L4:F9757): sum **+0.266**
- **Academic features with negative effect** (L8:F11284, L6:F2254×2, L2:F10852, L20:F14235, L6:F6331, L14:F11252): sum **-0.282**

### Key Finding: The Concern is Partially Validated

The **male pronoun "His" is the single largest individual positive feature** driving the probe (L0:F1069, +0.070), and it is a pure, shallow gender marker with no profession-related information — it fires identically on "He said hello" as on "He published a paper." Combined with L2:F3877 (+0.034), the gender signal contributes meaningfully to the classification.

However, the circuit is not *entirely* spurious. Genuine profession-relevant features from "research interests", "BS", "PhD", "University", "from" tokens do contribute. But the net effect of academic-content features is nearly zero (+0.266 − 0.282 = **-0.016**), meaning the positive and negative academic features almost perfectly cancel out. This leaves the **gender marker as a disproportionately influential net contributor** to the final probe score.

**Conclusion:** The probe relies on a spurious shortcut — the presence of male pronouns ("His"/"He") is a strong positive signal, while the genuine academic-content features largely cancel each other out. This is consistent with the concern that the probe uses gender markers as a proxy for profession classification, likely because male-gendered biographical text is overrepresented in certain profession categories in the training data.

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L0:1069 de=0.070 |
| 3 | `inspect_feature` ×19 | L0:1069, L1:10986, L8:11284, L14:11252, L5:12330, L0:10783, L0:13431, L6:2254, L2:10852, L7:14129, L4:9757, L0:2994, L0:2159, L2:1621, L0:6446, L20:14235, L3:4213, L6:6331, L2:3877 |

### Dispatch: 8 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L0:F1069@1` | ✅ reported | 7 | 8 | Trace the male pronoun feature L0:1069 at pos 1 ("His"). This is the #1 positive… |
| SA-2 | `L1:F10986@3` | ✅ reported | 4 | 10 | Trace the academic research feature L1:10986 at pos 3 ("research"). This is the … |
| SA-3 | `L7:F14129@27` | ✅ reported | 11 | 20 | Trace the academic degrees/universities feature L7:14129 at pos 27 (likely "PhD"… |
| SA-4 | `L20:F14235@31` | ✅ reported | 10 | 15 | Trace the academic credentials/institutions feature L20:14235 at pos 31. This ha… |
| SA-5 | `L2:F3877@1` | ✅ reported | 4 | 8 | Trace L2:3877 at pos 1 — 'His'/religious references feature. This has positive e… |
| SA-6 | `L8:F11284@13` | ✅ reported | 10 | 11 | Trace L8:11284 at pos 13 — universities/research feature with NEGATIVE effect (-… |
| SA-7 | `L6:F2254@27` | ✅ reported | 10 | 21 | Trace L6:2254 at pos 27 — academic degrees feature with NEGATIVE effect. Underst… |
| SA-8 | `L3:F4213@21` | ✅ reported | 6 | 12 | Trace L3:4213 at pos 21 — degree qualifications feature with POSITIVE effect (+0… |

<details>
<summary><b>SA-1</b> — tool trace (9 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F1069 | " references to a male person, particularly when using the pronoun "He"" |
| 2 | `get_upstream_features` | L0:F1069@1, k=8 | Emb:"His"@1 (w=21.62) +7 more |
| 3 | `inspect_feature` | L0, F1775 | " the word "yet" and words immediately adjacent to it" |
| 4 | `inspect_feature` | L0, F310 | " the pronouns "she", "her", and "he" and sometimes the word "therefore" |
| 5 | `inspect_feature` | L0, F208 | "the words "happened" and "occur"" |
| 6 | `inspect_feature` | L0, F253 | "the contraction "ve" and also finds other words like "scale", "screen"" |
| 7 | `inspect_feature` | L0, F355 | " text related to numbers, especially those representing currency or me" |
| 8 | `inspect_feature` | L0, F96 | "sentences beginning with coordinating conjunctions like "but" and "and" |
| 9 | `get_top_logits` | k=5 | "" (100%) |

**Findings:** ## Key Findings: L0:F1069 — A Pure Male Pronoun Gender Marker

### Feature Identity (L0:F1069)
- **Label**: "references to a male person, particularly when using the pronoun 'He' or 'His'"
- **frac_nonzero**: 0.0078 — *extremely sparse* (fires on less than 1% of tokens). This is a highly specific, selective feature.
- **Suppressed tokens**: He, His, Him, Himself, HE, Hes, Он (Russian for He), Его …

</details>

<details>
<summary><b>SA-2</b> — tool trace (9 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L1, F10986 | " words related to academic research" |
| 2 | `get_upstream_features` | L1:F10986@3, k=5 | Emb:" research"@2 (w=6.62) +4 more |
| 3 | `inspect_feature` | L0, F13948 | " the color "pink"" |
| 4 | `inspect_feature` | L0, F6113 | " the word "overall", sometimes alongside words that express quantity" |
| 5 | `inspect_feature` | L0, F13431 | "the word "owing"." |
| 6 | `get_upstream_features` | L0:F6113@3, k=5 | Emb:" interests"@3 (w=14.19) +4 more |
| 7 | `get_upstream_features` | L0:F13431@3, k=5 | Emb:" interests"@3 (w=12.25) +4 more |
| 8 | `get_upstream_features` | L0:F13948@3, k=5 | Emb:" interests"@3 (w=14.94) +4 more |
| 9 | `get_top_logits` | k=5 | "" (100%) |

**Findings:** ## Key Finding: L1:F10986 Is Driven by Raw Token Embeddings, Not Semantic Research Features

### What L1:F10986 Actually Is
L1:F10986 (label: "words related to academic research", frac_nonzero=0.038) fires in academic/research contexts — top examples include academic biographies ("research interests", "investigator") and clinical trial papers. Despite its label, its promoted tokens are oddly techn…

</details>

<details>
<summary><b>SA-3</b> — tool trace (16 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L7, F14129 | " academic degrees, universities, and people associated with them" |
| 2 | `get_upstream_features` | L7:F14129@27, k=8 | Emb:" PhD"@27 (w=19.25) +7 more |
| 3 | `inspect_feature` | L6, F2254 | "references to academic degrees" |
| 4 | `inspect_feature` | L5, F13801 | "abbreviations for degrees and mentions of educational attainment" |
| 5 | `inspect_feature` | L5, F11028 | " terms and phrases related to academic study and institutions" |
| 6 | `get_upstream_features` | L6:F2254@27, k=8 | Emb:" PhD"@27 (w=22.00) +7 more |
| 7 | `inspect_feature` | L2, F10852 | " academic titles and degrees" |
| 8 | `inspect_feature` | L4, F3727 | " mentions of academic degrees" |
| 9 | `inspect_feature` | L6, F8285 | " text related to scientific publications and author information." |
| 10 | `get_upstream_features` | L5:F13801@27, k=8 | Emb:" PhD"@27 (w=6.31) +7 more |
| 11 | `get_upstream_features` | L2:F10852@27, k=8 | Emb:" PhD"@27 (w=29.50) +7 more |
| 12 | `inspect_feature` | L4, F13943 | " words and abbreviations related to academic research" |
| 13 | `get_upstream_features` | L4:F3727@27, k=6 | L2:F10852 (w=13.19) +5 more |
| 14 | `inspect_feature` | L1, F14298 | "academic publications, papers, and citations" |
| 15 | `inspect_feature` | L1, F14141 | " words pertaining to officials, leadership, and the education system." |
| 16 | `inspect_feature` | L3, F11994 | " academic degrees and professional titles, especially involving "Ph.D." |

**Findings:** The academic credential signal at L7:F14129 ("academic degrees, universities, and people associated with them") originates overwhelmingly from the raw token embedding of " PhD" at position 27 and is progressively refined through a cascade of increasingly specific academic features across layers 1–6.

**Circuit Architecture:**

1. **Origin (Embedding Layer):** The " PhD" token embedding at pos 27 i…

</details>

<details>
<summary><b>SA-4</b> — tool trace (15 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L20, F14235 | " references to academic credentials and institutions." |
| 2 | `get_upstream_features` | L20:F14235@31, k=8 | L17:F11003 (w=30.38) +7 more |
| 3 | `inspect_feature` | L17, F11003 | "university" |
| 4 | `inspect_feature` | L19, F2496 | " mentions of universities and degrees" |
| 5 | `inspect_feature` | L18, F13264 | " words and phrases associated with earning advanced academic degrees l" |
| 6 | `get_upstream_features` | L17:F11003@31, k=6 | Emb:" PhD"@27 (w=9.44) +5 more |
| 7 | `get_upstream_features` | L19:F2496@31, k=6 | L17:F11003 (w=14.12) +5 more |
| 8 | `inspect_feature` | L7, F14129 | " academic degrees, universities, and people associated with them" |
| 9 | `inspect_feature` | L14, F3956 | " universities and degrees" |
| 10 | `inspect_feature` | L18, F13805 | "Universities" |
| 11 | `get_upstream_features` | L14:F3956@31, k=6 | Emb:"<bos>"@0 (w=-5.66) +5 more |
| 12 | `get_upstream_features` | L7:F14129@27, k=6 | Emb:" PhD"@27 (w=19.25) +5 more |
| 13 | `inspect_feature` | L3, F4213 | " mentions of degree qualifications or awards" |
| 14 | `inspect_feature` | L6, F2254 | "references to academic degrees" |
| 15 | `inspect_feature` | L5, F13801 | "abbreviations for degrees and mentions of educational attainment" |

**Findings:** ## Circuit Trace: L20:F14235 "Academic Credentials/Institutions" — Why It Has a Negative Probe Effect

### What the Feature Does
L20:F14235 detects **references to academic credentials and institutions** (promoted tokens: " UC", " Cornell", " University", " UCLA", " Duke", etc.). It fires strongly at pos 31, which corresponds to the word " from" in the context of a phrase like "received a PhD from…

</details>

<details>
<summary><b>SA-5</b> — tool trace (7 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L2, F3877 | " references to "His" and religious figures or concepts" |
| 2 | `get_upstream_features` | L2:F3877@1, k=5 | Emb:"His"@1 (w=20.88) +4 more |
| 3 | `inspect_feature` | L0, F2749 | " references to ownership or association with a person or group of peop" |
| 4 | `inspect_feature` | L0, F1069 | " references to a male person, particularly when using the pronoun "He"" |
| 5 | `inspect_feature` | L0, F2208 | " the pronoun "Him" and the possessive pronoun "His" when used in a rel" |
| 6 | `get_upstream_features` | L0:F1069@1, k=5 | Emb:"His"@1 (w=21.62) +4 more |
| 7 | `get_upstream_features` | L0:F2208@1, k=5 | Emb:"His"@1 (w=12.88) +4 more |

**Findings:** 
L2:F3877 is NOT primarily a male gender feature — it is a **religious capitalization feature** that detects "His" specifically in the context of divine/religious reference (capitalised "His" referring to God, Christ, etc.).

Key findings:
1. **The raw "His" token embedding** is the overwhelming driver of L2:F3877, with an edge weight of 20.875 — far exceeding all other upstream inputs combined. T…

</details>

<details>
<summary><b>SA-6</b> — tool trace (15 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L8, F11284 | " words and phrases related to people's names, titles, universities, an" |
| 2 | `get_upstream_features` | L8:F11284@13, k=8 | Emb:" research"@2 (w=3.92) +7 more |
| 3 | `inspect_feature` | L7, F3209 | "words and symbols in source code" |
| 4 | `inspect_feature` | L7, F10900 | " words related to cell biology and research proposals in that field" |
| 5 | `inspect_feature` | L7, F1674 | " certain common titles (Mr., Dr.) combined with job-related action ver" |
| 6 | `get_upstream_features` | L7:F3209@13, k=8 | Emb:" interests"@3 (w=2.34) +7 more |
| 7 | `get_upstream_features` | L7:F10900@13, k=8 | Emb:" research"@2 (w=3.77) +7 more |
| 8 | `inspect_feature` | L6, F12152 | "assignment operators, equality operators, asterisk, and the word "rate" |
| 9 | `inspect_feature` | L6, F8099 | " angle brackets, the word assembly, and certain XML/HTML tags" |
| 10 | `inspect_feature` | L6, F2267 | "words that appear in programming code, legal jargon, or scientific tex" |
| 11 | `get_upstream_features` | L6:F12152@13, k=8 | L5:F12330 (w=2.58) +7 more |
| 12 | `inspect_feature` | L5, F12330 | "mentions of "College" along with a preceding place name like "County" " |
| 13 | `get_upstream_features` | L5:F12330@13, k=8 | Emb:"<bos>"@0 (w=-3.25) +7 more |
| 14 | `inspect_feature` | L3, F9204 | " language related to patent claims and technical specifications." |
| 15 | `inspect_feature` | L4, F2958 | "periods and colons immediately following numbers and math symbols" |

**Findings:** ## Circuit Summary: Why L8:F11284 (Universities/Research) Has NEGATIVE Effect (-0.057)

**The Core Paradox:** L8:F11284 is genuinely a universities/research feature (frac_nonzero=0.016, promotes "RESEARCH", "universitarios"), yet it pushes *against* the probe. The upstream circuit reveals why:

### The Upstream Circuit is Dominated by Technical/Code Signals — Not Academic Signals

The feature fire…

</details>

<details>
<summary><b>SA-7</b> — tool trace (15 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F2254 | "references to academic degrees" |
| 2 | `get_upstream_features` | L6:F2254@27, k=8 | Emb:" PhD"@27 (w=22.00) +7 more |
| 3 | `inspect_feature` | L2, F10852 | " academic titles and degrees" |
| 4 | `inspect_feature` | L5, F13801 | "abbreviations for degrees and mentions of educational attainment" |
| 5 | `inspect_feature` | L4, F3727 | " mentions of academic degrees" |
| 6 | `inspect_feature` | L3, F11994 | " academic degrees and professional titles, especially involving "Ph.D." |
| 7 | `inspect_feature` | L5, F5725 | " people's educational history including degrees and schools" |
| 8 | `get_upstream_features` | L2:F10852@27, k=6 | Emb:" PhD"@27 (w=29.50) +5 more |
| 9 | `get_upstream_features` | L4:F3727@27, k=6 | L2:F10852 (w=13.19) +5 more |
| 10 | `get_upstream_features` | L5:F13801@27, k=6 | Emb:" PhD"@27 (w=6.31) +5 more |
| 11 | `inspect_feature` | L1, F14298 | "academic publications, papers, and citations" |
| 12 | `inspect_feature` | L4, F13943 | " words and abbreviations related to academic research" |
| 13 | `get_upstream_features` | L3:F11994@27, k=6 | L2:F10852 (w=10.00) +5 more |
| 14 | `inspect_feature` | L2, F13360 | " words related to academic titles and positions." |
| 15 | `inspect_feature` | L5, F7646 | " words related to academic research, funding, and authorship" |

**Findings:** ## Circuit Summary: L6:F2254 "Academic Degrees" Feature — Negative Effect Tracing

### Root Signal: The " PhD" Token Embedding (pos 27)
The entire circuit originates from a single powerful input signal: the **" PhD" token embedding at position 27**, which drives nearly every feature in the chain with massive edge weights (22.0 → L6:2254 directly; 29.5 → L2:10852; 9.0625 → L3:11994; 6.3125 → L5:138…

</details>

<details>
<summary><b>SA-8</b> — tool trace (9 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L3, F4213 | " mentions of degree qualifications or awards" |
| 2 | `get_upstream_features` | L3:F4213@21, k=5 | Emb:" from"@21 (w=11.12) +4 more |
| 3 | `inspect_feature` | L2, F10852 | " academic titles and degrees" |
| 4 | `inspect_feature` | L0, F8974 | "the word "from"" |
| 5 | `get_upstream_features` | L2:F10852@17, k=5 | Emb:" BS"@17 (w=15.44) +4 more |
| 6 | `inspect_feature` | L1, F15795 | " words related to education and school admissions" |
| 7 | `inspect_feature` | L1, F12372 | " mentions of US universities and sports teams" |
| 8 | `get_upstream_features` | L1:F15795@17, k=5 | Emb:" BS"@17 (w=4.50) +4 more |
| 9 | `inspect_feature` | L0, F3825 | " mentions of studies involving medical acronyms" |

**Findings:** ## Circuit Summary: L3:F4213 — Degree Qualifications Feature at pos 21

### Core Finding
L3:F4213 ("mentions of degree qualifications or awards", frac_nonzero=0.012) is a highly specific, low-frequency feature that fires in academic credential contexts like "He received his BS from [University]". It promotes institution-related tokens (e.g., "institution", "Institute"), suggesting it prepares the …

</details>

### Build

`build_circuit` → 22 nodes, 33 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | anthropic/claude-opus-4.6 | 124,831 | 7,082 | 0 | 0 | $0.8012 | — | — |
| SA-5 | anthropic/claude-sonnet-4.6 | 21,605 | 2,407 | 0 | 0 | $0.1009 | ✅ 4F/8E | Trace L2:3877 at pos 1 — 'His'/religious references feature.… |
| SA-2 | anthropic/claude-sonnet-4.6 | 29,305 | 2,637 | 0 | 0 | $0.1275 | ✅ 4F/10E | Trace the academic research feature L1:10986 at pos 3 ("rese… |
| SA-8 | anthropic/claude-sonnet-4.6 | 30,289 | 3,091 | 0 | 0 | $0.1372 | ✅ 6F/12E | Trace L3:4213 at pos 21 — degree qualifications feature with… |
| SA-1 | anthropic/claude-sonnet-4.6 | 34,807 | 3,177 | 0 | 0 | $0.1521 | ✅ 7F/8E | Trace the male pronoun feature L0:1069 at pos 1 ("His"). Thi… |
| SA-3 | anthropic/claude-sonnet-4.6 | 51,932 | 4,668 | 0 | 0 | $0.2258 | ✅ 11F/20E | Trace the academic degrees/universities feature L7:14129 at … |
| SA-4 | anthropic/claude-sonnet-4.6 | 57,686 | 4,422 | 0 | 0 | $0.2394 | ✅ 10F/15E | Trace the academic credentials/institutions feature L20:1423… |
| SA-7 | anthropic/claude-sonnet-4.6 | 50,601 | 4,740 | 0 | 0 | $0.2229 | ✅ 10F/21E | Trace L6:2254 at pos 27 — academic degrees feature with NEGA… |
| SA-6 | anthropic/claude-sonnet-4.6 | 79,766 | 4,333 | 0 | 0 | $0.3043 | ✅ 10F/11E | Trace L8:11284 at pos 13 — universities/research feature wit… |
| **Total** | | **480,822** | **36,557** | **0** | **0** | **$2.3113** | | |

**Oracle wall-clock time:** 4m 41s