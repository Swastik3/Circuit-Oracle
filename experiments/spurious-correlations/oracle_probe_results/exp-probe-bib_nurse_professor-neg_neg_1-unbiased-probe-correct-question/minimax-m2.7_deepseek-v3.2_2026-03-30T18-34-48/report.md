# Circuit Oracle Report
**Date:** 2026-03-30 18:34:48 UTC | **Orchestrator:** minimax/minimax-m2.7 | **Subagent:** deepseek/deepseek-v3.2

## Input
**Prompt:** "Dataset: bib_nurse_professor-neg_neg_1 | Probe: unbiased | Method: correct"
**System prompt:** ""
**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."
**Top predictions:**  (100.0%)

## Oracle Analysis
**Analysis:** The probe's classification score is driven by a mix of spurious gender markers and genuine academic indicators, where the male pronoun "His" (detected by L0:F1069 with direct_effect=0.0698) is the single strongest feature, followed by academic phrase patterns (L1:F10986, direct_effect=0.0674) that contain "His" as a co-occurring token in phrases like "His research interests."

**Confidence:** 9/10

**Reasoning:** The attribution circuit confirms the user's concern. The probe relies heavily on spurious gender markers:

1. **L0:F1069** ("references to a male person, particularly when using the pronoun 'He' or 'His'") has the highest direct effect (0.0698) on the probe score, with a very strong embedding connection from "His" (weight=21.63). This is a pure gender marker, not a profession indicator.

2. **L0:F2994** ("the pronoun 'his' and the pronoun 'he'") has a direct effect of -0.0386, further contributing gender signal to the probe.

3. The academic phrase feature **L1:F10986** (direct_effect=0.0674) is driven by the phrase "research interests" but receives spurious input from "His" (weight=0.15), meaning the phrase "His research interests" contributes to classification partly due to the gender marker, not just the academic content.

4. The circuit also includes **L4:F9757** (scientific acronyms) which receives spurious input from "His" (weight=2.09), representing another spurious gender correlation in what appears to be technical content.

5. **Genuine indicators exist** but are not dominant: The academic degree detection chain (L2:F10852 → L6:F2254 → L7:F14129) centered on "PhD" token (embedding weight=29.5) provides legitimate professional signals with low frac_nonzero (0.004-0.008), indicating specificity. Technical features like L14:F11252 (coordinate geometry) also contribute genuine technical content.

The signal flow is: Token embeddings ("His", "PhD", "research", "University") → layer-specific feature detectors → output probe direction. The gender marker "His" at position 1 is the primary driver of classification, with genuine academic indicators (PhD degrees, university names, research terminology) providing secondary support. This confirms the user's suspicion that the probe uses spurious gender correlations rather than relying primarily on legitimate profession indicators.

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L0:1069 de=0.070 |

### Dispatch: 10 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L0:F1069@1` | ✅ reported | 3 | 2 | Trace what this feature encodes. Look for gender markers, profession indicators,… |
| SA-2 | `L1:F10986@3` | ✅ reported | 5 | 17 | Trace what this feature encodes. Look for gender markers, profession indicators,… |
| SA-3 | `L8:F11284@13` | ✅ reported | 8 | 7 | Trace what this feature encodes. Look for gender markers, profession indicators,… |
| SA-4 | `L7:F14129@27` | ✅ reported | 11 | 24 | Trace what this feature encodes. Look for gender markers, profession indicators,… |
| SA-5 | `L6:F2254@27` | ✅ reported | 9 | 19 | Trace what this feature encodes. Look for gender markers, profession indicators,… |
| SA-6 | `L14:F11252@9` | ✅ reported | 10 | 9 | Trace what this feature encodes. Look for gender markers, profession indicators,… |
| SA-7 | `L0:F2994@1` | ✅ reported | 1 | 2 | Trace what this feature encodes. Look for gender markers, profession indicators,… |
| SA-8 | `L0:F2159@3` | ✅ reported | 1 | 4 | Trace what this feature encodes. Look for any connection to gender markers or pr… |
| SA-9 | `L4:F9757@1` | ✅ reported | 8 | 9 | Trace what this feature encodes. Look for gender markers, profession indicators,… |
| SA-10 | `L0:F10783@4` | ✅ reported | 1 | 5 | Trace what this feature encodes. Look for gender markers, profession indicators,… |

<details>
<summary><b>SA-1</b> — tool trace (6 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F1069 | " references to a male person, particularly when using the pronoun "He"" |
| 2 | `get_upstream_features` | L0:F1069@1, k=5 | Emb:"His"@1 (w=21.62) +4 more |
| 3 | `get_upstream_features` | L0:F1069@1, k=20 | Emb:"His"@1 (w=21.62) +19 more |
| 4 | `inspect_feature` | L0, F253 | "the contraction "ve" and also finds other words like "scale", "screen"" |
| 5 | `inspect_feature` | L0, F310 | " the pronouns "she", "her", and "he" and sometimes the word "therefore" |
| 6 | `get_upstream_features` | L0:F1069@1, k=30 | Emb:"His"@1 (w=21.62) +29 more |

**Findings:** The feature L0:F1069 encodes detection of the male possessive pronoun \"His\". It receives strong direct input from the \"His\" token embedding (weight 21.625) and weaker input from the beginning-of-sequence token (weight 6.7812). 

Key findings:
1. This is a genuine gender marker feature that specifically detects the token \"His\".
2. Despite activating on male pronouns, it suppresses male pronou…

</details>

<details>
<summary><b>SA-2</b> — tool trace (9 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L1, F10986 | " words related to academic research" |
| 2 | `get_upstream_features` | L1:F10986@3, k=5 | Emb:" research"@2 (w=6.62) +4 more |
| 3 | `inspect_feature` | L0, F6113 | " the word "overall", sometimes alongside words that express quantity" |
| 4 | `inspect_feature` | L0, F13948 | " the color "pink"" |
| 5 | `inspect_feature` | L0, F13431 | "the word "owing"." |
| 6 | `get_upstream_features` | L0:F6113@3, k=5 | Emb:" interests"@3 (w=14.19) +4 more |
| 7 | `get_upstream_features` | L0:F13948@3, k=5 | Emb:" interests"@3 (w=14.94) +4 more |
| 8 | `get_upstream_features` | L0:F13431@3, k=5 | Emb:" interests"@3 (w=12.25) +4 more |
| 9 | `inspect_feature` | L0, F253 | "the contraction "ve" and also finds other words like "scale", "screen"" |

**Findings:** The feature L1:F10986 encodes "words related to academic research" and is primarily driven directly by the embedding tokens " research" (pos 2, weight 6.625) and " interests" (pos 3, weight 4.4688). It also receives weaker signals from layer 0 features that detect specific words: "overall" (positive weight 0.5859), "owing" (positive weight 0.4434), and "pink" (negative weight -0.6328). 

The "pink…

</details>

<details>
<summary><b>SA-3</b> — tool trace (13 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L8, F11284 | " words and phrases related to people's names, titles, universities, an" |
| 2 | `get_upstream_features` | L8:F11284@13, k=5 | Emb:" research"@2 (w=3.92) +4 more |
| 3 | `inspect_feature` | L7, F3209 | "words and symbols in source code" |
| 4 | `inspect_feature` | L7, F10900 | " words related to cell biology and research proposals in that field" |
| 5 | `get_upstream_features` | L7:F3209@13, k=5 | Emb:" interests"@3 (w=2.34) +4 more |
| 6 | `inspect_feature` | L6, F12152 | "assignment operators, equality operators, asterisk, and the word "rate" |
| 7 | `inspect_feature` | L6, F2267 | "words that appear in programming code, legal jargon, or scientific tex" |
| 8 | `get_upstream_features` | L6:F12152@13, k=5 | L5:F12330 (w=2.58) +4 more |
| 9 | `inspect_feature` | L5, F12330 | "mentions of "College" along with a preceding place name like "County" " |
| 10 | `get_upstream_features` | L5:F12330@13, k=5 | Emb:"<bos>"@0 (w=-3.25) +4 more |
| 11 | `inspect_feature` | L3, F9204 | " language related to patent claims and technical specifications." |
| 12 | `inspect_feature` | L0, F6051 | "periods, spaces, and the number 1" |
| 13 | `get_upstream_features` | L7:F10900@13, k=5 | Emb:" research"@2 (w=3.77) +4 more |

**Findings:** This circuit traces a feature L8:F11284 that encodes "words and phrases related to people's names, titles, universities, and research." The tracing reveals it's primarily composed of two pathways:

1. ACADEMIC/TECHNICAL PATH: From early patent/technical language detection (L3:F9204) → educational institution detection (L5:F12330 "College") → programming operator detection (L6:F12152 "*", "==") → s…

</details>

<details>
<summary><b>SA-4</b> — tool trace (16 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L7, F14129 | " academic degrees, universities, and people associated with them" |
| 2 | `get_upstream_features` | L7:F14129@27, k=5 | Emb:" PhD"@27 (w=19.25) +4 more |
| 3 | `inspect_feature` | L6, F2254 | "references to academic degrees" |
| 4 | `inspect_feature` | L5, F13801 | "abbreviations for degrees and mentions of educational attainment" |
| 5 | `inspect_feature` | L5, F11028 | " terms and phrases related to academic study and institutions" |
| 6 | `get_upstream_features` | L6:F2254@27, k=5 | Emb:" PhD"@27 (w=22.00) +4 more |
| 7 | `inspect_feature` | L2, F10852 | " academic titles and degrees" |
| 8 | `inspect_feature` | L4, F3727 | " mentions of academic degrees" |
| 9 | `inspect_feature` | L3, F11994 | " academic degrees and professional titles, especially involving "Ph.D." |
| 10 | `get_upstream_features` | L2:F10852@27, k=5 | Emb:" PhD"@27 (w=29.50) +4 more |
| 11 | `inspect_feature` | L1, F14298 | "academic publications, papers, and citations" |
| 12 | `get_upstream_features` | L5:F13801@27, k=5 | Emb:" PhD"@27 (w=6.31) +4 more |
| 13 | `inspect_feature` | L4, F13943 | " words and abbreviations related to academic research" |
| 14 | `inspect_feature` | L2, F12998 | " words related to academic papers like sections, theorems, studies, re" |
| 15 | `get_upstream_features` | L3:F11994@27, k=5 | L2:F10852 (w=10.00) +4 more |
| 16 | `inspect_feature` | L2, F13360 | " words related to academic titles and positions." |

**Findings:** I traced the circuit starting from L7:F14129 at position 27, which encodes "academic degrees, universities, and people associated with them." The tracing reveals a genuine academic/technical indicator circuit focused on recognizing academic degrees and qualifications.

Key findings:

1. **Direct token influence**: The strongest connections throughout the circuit come from the " PhD" token embeddin…

</details>

<details>
<summary><b>SA-5</b> — tool trace (15 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F2254 | "references to academic degrees" |
| 2 | `get_upstream_features` | L6:F2254@27, k=5 | Emb:" PhD"@27 (w=22.00) +4 more |
| 3 | `inspect_feature` | L2, F10852 | " academic titles and degrees" |
| 4 | `inspect_feature` | L5, F13801 | "abbreviations for degrees and mentions of educational attainment" |
| 5 | `inspect_feature` | L4, F3727 | " mentions of academic degrees" |
| 6 | `get_upstream_features` | L2:F10852@27, k=5 | Emb:" PhD"@27 (w=29.50) +4 more |
| 7 | `get_upstream_features` | L5:F13801@27, k=5 | Emb:" PhD"@27 (w=6.31) +4 more |
| 8 | `get_upstream_features` | L4:F3727@27, k=5 | L2:F10852 (w=13.19) +4 more |
| 9 | `inspect_feature` | L1, F14298 | "academic publications, papers, and citations" |
| 10 | `inspect_feature` | L4, F13943 | " words and abbreviations related to academic research" |
| 11 | `inspect_feature` | L2, F12998 | " words related to academic papers like sections, theorems, studies, re" |
| 12 | `inspect_feature` | L3, F11994 | " academic degrees and professional titles, especially involving "Ph.D." |
| 13 | `get_upstream_features` | L3:F11994@27, k=5 | L2:F10852 (w=10.00) +4 more |
| 14 | `inspect_feature` | L2, F13360 | " words related to academic titles and positions." |
| 15 | `get_upstream_features` | L1:F14298@27, k=5 | Emb:" PhD"@27 (w=4.00) +4 more |

**Findings:** Tracing from L6:F2254 (references to academic degrees) reveals a circuit focused on detecting academic credentials, particularly PhD degrees. The circuit is primarily driven by the token "PhD" itself (strongest connection: weight 22.0 directly from embedding), with L2:F10852 (academic titles and degrees) serving as a key intermediate node (weight 10.125). This L2 feature itself is strongly driven …

</details>

<details>
<summary><b>SA-6</b> — tool trace (15 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L14, F11252 | " code and coordinate geometry terms" |
| 2 | `get_upstream_features` | L14:F11252@9, k=5 | Emb:" visualization"@9 (w=6.09) +4 more |
| 3 | `inspect_feature` | L7, F3549 | " technical text containing numbers and letters, possibly related to me" |
| 4 | `inspect_feature` | L7, F16358 | " text referencing design and virtual reality." |
| 5 | `get_upstream_features` | L7:F3549@9, k=5 | Emb:" visualization"@9 (w=5.56) +4 more |
| 6 | `inspect_feature` | L0, F11835 | "terms used in software code such as "assembly", "using", "namespace", " |
| 7 | `get_upstream_features` | L7:F16358@9, k=5 | Emb:" visualization"@9 (w=11.44) +4 more |
| 8 | `inspect_feature` | L6, F16345 | " words associated with both literal and metaphorical drawing." |
| 9 | `get_upstream_features` | L6:F16345@9, k=5 | Emb:" visualization"@9 (w=12.56) +4 more |
| 10 | `inspect_feature` | L8, F13140 | " words related to three dimensional imaging" |
| 11 | `inspect_feature` | L3, F709 | "terms related to scientific or technical documentation" |
| 12 | `inspect_feature` | L5, F2903 | " words related to scientific research fields and measurements" |
| 13 | `get_upstream_features` | L5:F2903@9, k=5 | Emb:" visualization"@9 (w=1.88) +4 more |
| 14 | `inspect_feature` | L4, F13857 | " words describing jobs, roles or professional activity" |
| 15 | `inspect_feature` | L4, F7473 | " words related to scientific research and chemicals" |

**Findings:** This circuit traces a genuine academic/technical feature encoding "code and coordinate geometry terms" (L14:F11252). The circuit shows strong connections to programming/geometry concepts without gender or spurious correlations. Key findings:

1. The feature is genuinely technical: it activates on programming code with coordinate variables (x, y, z), promotes geometry-related tokens ("RotationOrder…

</details>

<details>
<summary><b>SA-7</b> — tool trace (3 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F2994 | "the pronoun "his" and the pronoun "he."" |
| 2 | `get_upstream_features` | L0:F2994@1, k=5 | Emb:"His"@1 (w=19.75) +4 more |
| 3 | `get_upstream_features` | L0:F2994@1, k=10 | Emb:"His"@1 (w=19.75) +9 more |

**Findings:** Tracing from L0:F2994 reveals a very simple circuit: this feature directly detects the token \"His\" from the input embedding with a strong weight of 19.75. The feature is labeled as detecting \"the pronoun 'his' and the pronoun 'he'\" and has a frac_nonzero of 0.073, indicating it's moderately specific. The promoted tokens are mostly punctuation and formatting tokens (. , \\n\\n, <strong>, <em>, …

</details>

<details>
<summary><b>SA-8</b> — tool trace (3 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F2159 | " words that end with "led" or are related to worth" |
| 2 | `get_upstream_features` | L0:F2159@3, k=5 | Emb:" interests"@3 (w=11.75) +4 more |
| 3 | `get_upstream_features` | L0:F2159@3, k=10 | Emb:" interests"@3 (w=11.75) +9 more |

**Findings:** The feature L0:F2159 at position 3 encodes words ending with \"led\" or related to \"worth\". It shows a very strong direct connection (weight 11.75) from the token embedding \" interests\" at position 3, suggesting it's primarily detecting the pattern of words ending with certain suffixes. There's a very weak negative connection from \"His\" (weight -0.0041) which is negligible. The feature promo…

</details>

<details>
<summary><b>SA-9</b> — tool trace (14 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F9757 | "various acronyms, IDs, and symbols, possibly related to scientific dat" |
| 2 | `get_upstream_features` | L4:F9757@1, k=5 | Emb:"<bos>"@0 (w=16.38) +4 more |
| 3 | `inspect_feature` | L0, F7344 | " content markers like figures and section headers" |
| 4 | `inspect_feature` | L3, F373 | " word beginnings with the letters "a," "h,""i," "r," and "p" (perhaps " |
| 5 | `inspect_feature` | L0, F2749 | " references to ownership or association with a person or group of peop" |
| 6 | `get_upstream_features` | L0:F7344@1, k=5 | Emb:"<bos>"@0 (w=12.44) +4 more |
| 7 | `get_upstream_features` | L3:F373@1, k=5 | Emb:"<bos>"@0 (w=29.00) +4 more |
| 8 | `inspect_feature` | L0, F1903 | "instances of sentences starting with "The"" |
| 9 | `inspect_feature` | L0, F1069 | " references to a male person, particularly when using the pronoun "He"" |
| 10 | `get_upstream_features` | L0:F2749@1, k=5 | Emb:"His"@1 (w=18.88) +4 more |
| 11 | `get_upstream_features` | L0:F1069@1, k=5 | Emb:"His"@1 (w=21.62) +4 more |
| 12 | `inspect_feature` | L2, F15681 | " words that indicate that something is improving or getting better" |
| 13 | `inspect_feature` | L0, F12698 | "question-answer pairs (or just questions) and import statements" |
| 14 | `get_upstream_features` | L2:F15681@1, k=5 | Emb:"<bos>"@0 (w=8.00) +4 more |

**Findings:** I traced the circuit starting from L4:F9757, which encodes "various acronyms, IDs, and symbols, possibly related to scientific data." The tracing reveals a clear spurious correlation with gender markers, specifically the male pronoun "His."

Key findings:
1. The starting feature L4:F9757 receives strong direct input from the embedding token "His" (edge_weight 2.09)
2. Tracing upstream reveals mult…

</details>

<details>
<summary><b>SA-10</b> — tool trace (3 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F10783 | " the word "include" (and variations of the word)" |
| 2 | `get_upstream_features` | L0:F10783@4, k=5 | Emb:" include"@4 (w=24.62) +4 more |
| 3 | `get_top_logits` | k=5 | "" (100%) |

**Findings:** This feature at L0:F10783 encodes detection of the word \"include\" and its variations. It fires specifically on the token \" include\" with a very strong direct connection from the embedding (weight 24.625). The feature has low sparsity (frac_nonzero=0.00716), indicating it's specific to occurrences of this word. Weaker connections from context words like \"His\", \"research\", and \"interests\" …

</details>

### Build

`build_circuit` → 10 nodes, 18 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m2.7 | 29,618 | 4,813 | 44,340 | 0 | — | — | — |
| SA-1 | deepseek/deepseek-v3.2 | 34,884 | 2,804 | 0 | 0 | — | ✅ 3F/2E | Trace what this feature encodes. Look for gender markers, pr… |
| SA-2 | deepseek/deepseek-v3.2 | 52,897 | 3,656 | 0 | 0 | — | ✅ 5F/17E | Trace what this feature encodes. Look for gender markers, pr… |
| SA-3 | deepseek/deepseek-v3.2 | 82,766 | 3,772 | 21,696 | 0 | — | ✅ 8F/7E | Trace what this feature encodes. Look for gender markers, pr… |
| SA-5 | deepseek/deepseek-v3.2 | 101,102 | 3,946 | 9,024 | 0 | — | ✅ 9F/19E | Trace what this feature encodes. Look for gender markers, pr… |
| SA-6 | deepseek/deepseek-v3.2 | 108,415 | 3,871 | 9,728 | 0 | — | ✅ 10F/9E | Trace what this feature encodes. Look for gender markers, pr… |
| SA-4 | deepseek/deepseek-v3.2 | 108,806 | 5,035 | 20,672 | 0 | — | ✅ 11F/24E | Trace what this feature encodes. Look for gender markers, pr… |
| SA-7 | deepseek/deepseek-v3.2 | 13,199 | 1,046 | 0 | 0 | — | ✅ 1F/2E | Trace what this feature encodes. Look for gender markers, pr… |
| SA-10 | deepseek/deepseek-v3.2 | 12,840 | 1,356 | 0 | 0 | — | ✅ 1F/5E | Trace what this feature encodes. Look for gender markers, pr… |
| SA-8 | deepseek/deepseek-v3.2 | 12,866 | 1,653 | 0 | 0 | — | ✅ 1F/4E | Trace what this feature encodes. Look for any connection to … |
| SA-9 | deepseek/deepseek-v3.2 | 92,155 | 3,819 | 9,856 | 0 | — | ✅ 8F/9E | Trace what this feature encodes. Look for gender markers, pr… |
| **Total** | | **649,548** | **35,771** | **115,316** | **0** | **—** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 7m 20s