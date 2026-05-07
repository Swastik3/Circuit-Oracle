# Circuit Oracle Report
**Date:** 2026-04-06 17:54:16 UTC | **Orchestrator:** minimax/minimax-m2.7 | **Subagent:** deepseek/deepseek-v3.2

## Input

**Prompt:** "Dataset: multinli-pos_pos_8 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "('The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction.',)"

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification is driven by a content-based circuit that detects semantic features of the input (Congress-related political entities, funding/control relationships, and quantifiers) rather than spurious negation signals. No features related to negation words ("not", "no") appear in the top 10 driving features. The circuit traces from token embeddings (Congress, funding, levels, controls, many, who) through early-layer content detectors (L0-2) to mid-layer semantic aggregators (L3-6), with the strongest positive effect from L0:F6044 (detecting "Congress" despite its spurious label "the word 'yield'") and strong negative effects from features detecting "who" (L0:F13437) and "levels" concepts (L2:F156).

**Confidence:** 8/10

**Reasoning:** The attribution circuit reveals five distinct content pathways converging on the probe output:

1. **Congress Pathway (L0→L1→L2→L3/L4-L6):** Token "Congress" (pos 2) directly activates multiple political/congressional features across layers. The strongest single edge is from "Congress" embedding to L0:F6044 (weight 17.0) and L1:F14850 (weight 17.625). These features have labels like "references to the U.S. Congress" (frac_nonzero=0.01169), "political parties and affiliations" (frac_nonzero=0.00587), and the spurious "the word 'yield'" label. The pathway culminates in L6:F6096 (political parties/affiliations, direct_effect=+0.4453).

2. **"Who" Pathway (Emb→L0):** Token "who" (pos 15) directly feeds L0:F13437 with weight 35.25, the highest single edge weight in the circuit. Despite its generic label "the word 'who'", this feature has strong negative effect (-0.5781) on the probe, suggesting relative clause structure contributes to the classification.

3. **"Levels" Pathway (Emb→L0→L2):** Token "levels" (pos 8) strongly activates L2:F156 (weight 28.0) which detects "amount or intensity". This has negative effect (-0.3691) on the probe.

4. **"Funding" Pathway (Emb→L0→L1):** Token "funding" (pos 7) activates L1:F2116 (weight 14.125) detecting "legal counsel or representation", with positive effect (+0.377).

5. **"Many" Pathway (Emb→L0→L1→L2→L3):** Token "many" (pos 13) cascades through multiple "many"-detecting features with consistent negative effects.

**Key finding regarding the user concern:** The circuit does NOT use spurious negation word signals. The top 10 features contain no negation-related features ("not" at pos 17, "no" at pos 21 are absent). However, the circuit does have features with **spurious/weak labels** — L0:F6044 is labeled "the word 'yield'" but is actually activated by the "Congress" token with weight 17.0, and L1:F6948 is labeled "the word 'lift' in mechanical/ski contexts" but also activated by "Congress". These are mislabeled but content-relevant features, not negation spuriousness.

The classification appears to be based on **semantic content matching** — detecting political/governmental entities (Congress), quantitative language (many), control/power relationships (controls, levels), and grammatical structure (who) — rather than on superficial negation patterns. The probe may be learning to identify contradictions based on mismatch between claimed Congressional control over funding and the explicit negation in the second sentence, but the circuit achieves this through content-level semantic features, not negation detectors.

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 10 features; top: L0:6044 de=0.789 |

### Dispatch: 8 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L0:F6044@2` | ✅ reported | 3 | 5 | Trace L0:F6044 - this has the highest positive direct effect (0.7891) on the pro… |
| SA-2 | `L0:F13437@15` | ✅ reported | 1 | 5 | Trace L0:F13437 - this has the highest negative direct effect (-0.5781) on the p… |
| SA-3 | `L6:F6096@2` | ✅ reported | 12 | 25 | Trace L6:F6096 at pos=2 - this has positive effect (0.4453) on the probe. Unders… |
| SA-4 | `L2:F6735@2` | ✅ reported | 5 | 11 | Trace L2:F6735 at pos=2 - this has negative effect (-0.4023) on the probe. Under… |
| SA-5 | `L1:F6948@2` | ✅ reported | 3 | 11 | Trace L1:F6948 at pos=2 - this has negative effect (-0.3926) on the probe. Look … |
| SA-6 | `L3:F123@2` | ✅ reported | 6 | 13 | Trace L3:F123 at pos=2 - this has positive effect (0.3574) on the probe. Look fo… |
| SA-7 | `L1:F2116@7` | ✅ reported | 5 | 25 | Trace L1:F2116 at pos=7 - this has positive effect (0.377) on the probe. Look at… |
| SA-8 | `L2:F156@8` | ✅ reported | 6 | 12 | Trace L2:F156 at pos=8 - this has negative effect (-0.3691) on the probe. Look f… |

<details>
<summary><b>SA-1</b> — tool trace (5 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F6044 | "the word "yield"" |
| 2 | `get_upstream_features` | L0:F6044@2, k=5 | Emb:" Congress"@2 (w=17.00) +4 more |
| 3 | `get_top_logits` | k=5 | "" (100%) |
| 4 | `inspect_feature` | L0, F478 | "various kinds of brackets and parentheses followed by a period" |
| 5 | `inspect_feature` | L0, F1131 | "the word "drop"" |

**Findings:** The circuit traces from L0:F6044 (labeled "the word 'yield'") back to token embeddings. The strongest connection is directly from the token " Congress" at position 2 with an extremely strong positive weight of 17.0. This indicates that in the specific prompt being analyzed, this feature is being activated by the token " Congress" rather than the word "yield" as suggested by its label. The feature …

</details>

<details>
<summary><b>SA-2</b> — tool trace (5 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F13437 | "the word "who"" |
| 2 | `get_upstream_features` | L0:F13437@15, k=5 | Emb:" who"@15 (w=35.25) +4 more |
| 3 | `get_top_logits` | k=5 | "" (100%) |
| 4 | `get_top_features` | token="", k=10 | 10 features; top: L0:6044 de=0.789 |
| 5 | `inspect_feature` | L0, F6044 | "the word "yield"" |

**Findings:** The feature L0:F13437 at position 15 encodes detection of the word \"who\". It has a strong negative direct effect (-0.5781) on the empty token prediction. Tracing upstream reveals this feature is directly fed by the input token \" who\" at position 15 with a very strong edge weight (35.25), indicating it's primarily detecting this specific token. Additional weaker connections come from tokens at …

</details>

<details>
<summary><b>SA-3</b> — tool trace (18 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F6096 | " political parties and affiliations" |
| 2 | `get_upstream_features` | L6:F6096@2, k=5 | Emb:" Congress"@2 (w=13.88) +4 more |
| 3 | `inspect_feature` | L2, F6735 | " political parties and politicians" |
| 4 | `inspect_feature` | L4, F5265 | " references to political parties, politicians, and elections" |
| 5 | `inspect_feature` | L5, F842 | " political parties and politicians" |
| 6 | `get_upstream_features` | L2:F6735@2, k=5 | Emb:" Congress"@2 (w=9.19) +4 more |
| 7 | `inspect_feature` | L1, F6853 | " proper nouns from the Indian subcontinent" |
| 8 | `inspect_feature` | L1, F7245 | " mentions of government or authority actions, specifically in the cont" |
| 9 | `get_upstream_features` | L4:F5265@2, k=5 | Emb:" Congress"@2 (w=6.91) +4 more |
| 10 | `inspect_feature` | L1, F2408 | " words related to organizations, especially governmental and education" |
| 11 | `get_upstream_features` | L5:F842@2, k=5 | Emb:" Congress"@2 (w=7.03) +4 more |
| 12 | `inspect_feature` | L1, F14850 | "references to the U.S. Congress." |
| 13 | `inspect_feature` | L1, F2652 | " terms related to Hindu worship practices and festivals" |
| 14 | `get_upstream_features` | L1:F6853@2, k=5 | Emb:" Congress"@2 (w=9.88) +4 more |
| 15 | `inspect_feature` | L0, F767 | "the word "Congress" as well as the phrase "immigration matters"" |
| 16 | `inspect_feature` | L0, F15411 | " terms relating to political bodies, figures, and processes" |
| 17 | `get_upstream_features` | L1:F14850@2, k=5 | Emb:" Congress"@2 (w=17.62) +4 more |
| 18 | `inspect_feature` | L2, F2701 | " words related to the U.S. Congress" |

**Findings:** Tracing L6:F6096 (political parties and affiliations) at position 2 reveals a clear circuit for processing the token "Congress". The circuit shows:

1. **Direct strong connections**: The token "Congress" at position 2 feeds directly into multiple layers with high edge weights (13.875 to L6, 9.1875 to L2, 6.9062 to L4, 7.0312 to L5, 9.875 to L1:F6853, and 17.625 to L1:F14850).

2. **Circuit structu…

</details>

<details>
<summary><b>SA-4</b> — tool trace (10 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L2, F6735 | " political parties and politicians" |
| 2 | `get_upstream_features` | L2:F6735@2, k=5 | Emb:" Congress"@2 (w=9.19) +4 more |
| 3 | `inspect_feature` | L1, F6853 | " proper nouns from the Indian subcontinent" |
| 4 | `inspect_feature` | L1, F7245 | " mentions of government or authority actions, specifically in the cont" |
| 5 | `get_upstream_features` | L1:F6853@2, k=5 | Emb:" Congress"@2 (w=9.88) +4 more |
| 6 | `get_upstream_features` | L1:F7245@2, k=5 | Emb:" Congress"@2 (w=10.56) +4 more |
| 7 | `inspect_feature` | L0, F767 | "the word "Congress" as well as the phrase "immigration matters"" |
| 8 | `inspect_feature` | L0, F15411 | " terms relating to political bodies, figures, and processes" |
| 9 | `get_upstream_features` | L0:F767@2, k=5 | Emb:" Congress"@2 (w=26.50) +4 more |
| 10 | `get_upstream_features` | L0:F15411@2, k=5 | Emb:" Congress"@2 (w=17.00) +4 more |

**Findings:** I traced the circuit for L2:F6735 (position 2) which has a negative effect (-0.4023) on the probe. This feature encodes "political parties and politicians" and has a fairly low frac_nonzero of 0.00871, making it specific rather than generic.

The tracing reveals a very direct and strong circuit originating from the token " Congress" at position 2. The feature receives strong direct input from the …

</details>

<details>
<summary><b>SA-5</b> — tool trace (7 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L1, F6948 | " the word "lift" in the context of mechanical devices or ski infrastru" |
| 2 | `get_upstream_features` | L1:F6948@2, k=5 | Emb:" Congress"@2 (w=16.00) +4 more |
| 3 | `inspect_feature` | L0, F6044 | "the word "yield"" |
| 4 | `inspect_feature` | L0, F9557 | "the word "clean" and words/phrases associated with people" |
| 5 | `get_upstream_features` | L0:F6044@2, k=5 | Emb:" Congress"@2 (w=17.00) +4 more |
| 6 | `get_upstream_features` | L0:F9557@2, k=5 | Emb:" Congress"@2 (w=11.12) +4 more |
| 7 | `get_top_logits` | k=5 | "" (100%) |

**Findings:** The circuit shows that L1:F6948 (encoding "lift" in mechanical/ski contexts) at position 2 is primarily driven by the token "Congress" at position 2 with a strong positive weight (+16.0). Interestingly, it receives negative inhibition (-0.459) from L0:F6044 which encodes "yield", and positive support (+0.3984) from L0:F9557 which encodes "clean/people". Both L0 features also get their primary inpu…

</details>

<details>
<summary><b>SA-6</b> — tool trace (10 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L3, F123 | " mentions of the United States Congress" |
| 2 | `get_upstream_features` | L3:F123@2, k=5 | Emb:" Congress"@2 (w=20.62) +4 more |
| 3 | `inspect_feature` | L2, F2701 | " words related to the U.S. Congress" |
| 4 | `inspect_feature` | L1, F6948 | " the word "lift" in the context of mechanical devices or ski infrastru" |
| 5 | `get_upstream_features` | L2:F2701@2, k=5 | Emb:" Congress"@2 (w=28.12) +4 more |
| 6 | `inspect_feature` | L1, F3276 | " mentions of the United States Congress" |
| 7 | `inspect_feature` | L0, F10198 | " the word "Congress"" |
| 8 | `get_upstream_features` | L1:F3276@2, k=5 | Emb:" Congress"@2 (w=21.88) +4 more |
| 9 | `inspect_feature` | L0, F767 | "the word "Congress" as well as the phrase "immigration matters"" |
| 10 | `get_upstream_features` | L0:F10198@2, k=5 | Emb:" Congress"@2 (w=17.25) +4 more |

**Findings:** The circuit traces how the model detects the word "Congress" at position 2. Key findings:

1. L3:F123 (starting point) encodes "mentions of the United States Congress" and has positive effect on the probe.

2. The circuit shows a direct, strong pathway from the token embedding "Congress" at position 2 through multiple layers:
   - Token "Congress" → L0:F10198 (weight: 17.25)
   - Token "Congress" …

</details>

<details>
<summary><b>SA-7</b> — tool trace (10 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L1, F2116 | " words and phrases related to legal counsel or representation" |
| 2 | `get_upstream_features` | L1:F2116@7, k=5 | Emb:" funding"@7 (w=14.12) +4 more |
| 3 | `inspect_feature` | L0, F4766 | " the word "fund" and words associated with faith or trust" |
| 4 | `inspect_feature` | L0, F7833 | "positive subjective judgements or the description of desired temperatu" |
| 5 | `inspect_feature` | L0, F11640 | "the word "multi" and words that commonly occur with "multi"" |
| 6 | `get_upstream_features` | L0:F4766@7, k=5 | Emb:" funding"@7 (w=12.88) +4 more |
| 7 | `get_upstream_features` | L0:F11640@7, k=5 | Emb:" funding"@7 (w=13.19) +4 more |
| 8 | `get_upstream_features` | L0:F7833@7, k=5 | Emb:" funding"@7 (w=10.56) +4 more |
| 9 | `inspect_feature` | L0, F13929 | " instances of the word "power" in a political or technical context" |
| 10 | `get_upstream_features` | L0:F13929@7, k=5 | Emb:" funding"@7 (w=13.94) +4 more |

**Findings:** Tracing L1:F2116 at position 7 revealed a circuit primarily driven by the token " funding" at position 7. The L1 feature encodes "words and phrases related to legal counsel or representation" and receives strong positive input (weight 14.125) directly from the token embedding for " funding". This direct connection explains its positive effect (0.377) on the probe.

The circuit shows that L1:F2116 …

</details>

<details>
<summary><b>SA-8</b> — tool trace (10 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L2, F156 | " words related to the amount or intensity of something" |
| 2 | `get_upstream_features` | L2:F156@8, k=5 | Emb:" levels"@8 (w=28.00) +4 more |
| 3 | `inspect_feature` | L1, F3717 | " uses of struct and/or when "longer" is used in the context "no longer" |
| 4 | `inspect_feature` | L1, F11773 | " the word "level" in various contexts" |
| 5 | `get_upstream_features` | L1:F3717@8, k=5 | Emb:" levels"@8 (w=16.62) +4 more |
| 6 | `inspect_feature` | L0, F812 | " a combination of the word "levels" and a number, or military terms" |
| 7 | `inspect_feature` | L0, F1736 | " mentions of scientific rates or levels of physical phenomena" |
| 8 | `get_upstream_features` | L1:F11773@8, k=5 | Emb:" levels"@8 (w=19.50) +4 more |
| 9 | `inspect_feature` | L0, F1082 | "the words "mouse" and "thereby."" |
| 10 | `get_upstream_features` | L0:F812@8, k=5 | Emb:" levels"@8 (w=15.38) +4 more |

**Findings:** I traced the circuit for L2:F156 at position 8, which has a negative effect (-0.3691) on the probe. The circuit shows:

1. The strongest connection is DIRECTLY from the token embedding for "levels" at position 8 to L2:F156 with weight 28.0. This feature detects "words related to the amount or intensity" and suppresses tokens like "levels", "Levels", etc.

2. Two layer 1 features feed negatively in…

</details>

### Re-dispatch (round 2): 2 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-9 | `L3:F8382@13` | ✅ reported | 6 | 18 | Trace L3:F8382 at pos=13 - this has positive effect (0.3281) on the probe. What … |
| SA-10 | `L3:F13271@5` | ✅ reported | 9 | 20 | Trace L3:F13271 at pos=5 - this has positive effect (0.3555) on the probe. Token… |

<details>
<summary><b>SA-9</b> — tool trace (11 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L3, F8382 | " the word "many", and sometimes "times" or "people" when near it" |
| 2 | `get_upstream_features` | L3:F8382@13, k=5 | Emb:" many"@13 (w=23.50) +4 more |
| 3 | `inspect_feature` | L0, F15792 | " the word "many" (and to a lesser extent, similar words like "multiple" |
| 4 | `inspect_feature` | L2, F6462 | " the word "many" and occasionally the number one" |
| 5 | `inspect_feature` | L2, F15792 | " the word "many", "multiple", "numerous", and sometimes the phrase "of" |
| 6 | `get_upstream_features` | L0:F15792@13, k=5 | Emb:" many"@13 (w=38.75) +4 more |
| 7 | `get_upstream_features` | L2:F6462@13, k=5 | Emb:" many"@13 (w=34.50) +4 more |
| 8 | `inspect_feature` | L1, F160 | " the word "many"" |
| 9 | `get_upstream_features` | L2:F15792@13, k=5 | Emb:" many"@13 (w=17.75) +4 more |
| 10 | `get_upstream_features` | L1:F160@13, k=5 | Emb:" many"@13 (w=22.38) +4 more |
| 11 | `inspect_feature` | L0, F676 | " the word "many" or similar words such as "other" and "some"" |

**Findings:** Tracing L3:F8382 at position 13 reveals a circuit for detecting the word "many". The feature gets its primary signal directly from the embedding of token " many" at position 13 (edge weight 23.5). Interestingly, there are negative connections from earlier layer features that also detect "many" (L0:F15792 and L2:F6462), suggesting inhibitory competition between different "many"-detecting features. …

</details>

<details>
<summary><b>SA-10</b> — tool trace (14 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L3, F13271 | " the word "control."" |
| 2 | `get_upstream_features` | L3:F13271@5, k=5 | Emb:" controls"@5 (w=18.50) +4 more |
| 3 | `inspect_feature` | L2, F7279 | " forms of the word "control" and words related to rulers" |
| 4 | `inspect_feature` | L2, F11080 | " code snippets and programming terms" |
| 5 | `get_upstream_features` | L2:F7279@5, k=5 | Emb:" controls"@5 (w=12.12) +4 more |
| 6 | `inspect_feature` | L0, F11835 | "terms used in software code such as "assembly", "using", "namespace", " |
| 7 | `inspect_feature` | L1, F3604 | " verbs in scientific or technical writing, especially those describing" |
| 8 | `get_upstream_features` | L2:F11080@5, k=5 | Emb:"<bos>"@0 (w=11.38) +4 more |
| 9 | `inspect_feature` | L1, F4020 | " variations of the word "control"" |
| 10 | `get_upstream_features` | L1:F4020@5, k=5 | Emb:" controls"@5 (w=22.38) +4 more |
| 11 | `inspect_feature` | L0, F5749 | " the phrase "quality control"" |
| 12 | `inspect_feature` | L0, F15246 | " situations where control is taken by someone" |
| 13 | `inspect_feature` | L2, F7490 | " words related to controlling electronic components and processes" |
| 14 | `get_upstream_features` | L2:F7490@5, k=5 | Emb:" controls"@5 (w=14.69) +4 more |

**Findings:** Tracing from L3:F13271 at pos=5 (token: "controls") reveals a circuit that detects the word "control" but has interesting inhibitory dynamics. The main feature L3:F13271 receives strong positive input from the "controls" token embedding (weight 18.5), but receives negative inhibitory inputs from several other features that detect "control" variants: L2:F7279 (forms of "control"), L1:F4020 (variati…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_features` | token="", k=15 → 15 features; top: L0:6044 de=0.789 |

### Build

`build_circuit` → 31 nodes, 55 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m2.7 | 63,110 | 7,165 | 52,391 | 0 | $0.0291 | — | — |
| SA-2 | deepseek/deepseek-v3.2 | 21,613 | 1,565 | 0 | 0 | $0.0062 | ✅ 1F/5E | Trace L0:F13437 - this has the highest negative direct effec… |
| SA-1 | deepseek/deepseek-v3.2 | 22,760 | 1,689 | 0 | 0 | $0.0066 | ✅ 3F/5E | Trace L0:F6044 - this has the highest positive direct effect… |
| SA-4 | deepseek/deepseek-v3.2 | 60,372 | 2,817 | 0 | 0 | $0.0168 | ✅ 5F/11E | Trace L2:F6735 at pos=2 - this has negative effect (-0.4023)… |
| SA-3 | deepseek/deepseek-v3.2 | 148,542 | 5,332 | 10,624 | 0 | $0.0409 | ✅ 12F/25E | Trace L6:F6096 at pos=2 - this has positive effect (0.4453) … |
| SA-5 | deepseek/deepseek-v3.2 | 36,625 | 2,846 | 0 | 0 | $0.0106 | ✅ 3F/11E | Trace L1:F6948 at pos=2 - this has negative effect (-0.3926)… |
| SA-8 | deepseek/deepseek-v3.2 | 52,245 | 3,113 | 9,728 | 0 | $0.0150 | ✅ 6F/12E | Trace L2:F156 at pos=8 - this has negative effect (-0.3691) … |
| SA-6 | deepseek/deepseek-v3.2 | 64,106 | 3,586 | 0 | 0 | $0.0180 | ✅ 6F/13E | Trace L3:F123 at pos=2 - this has positive effect (0.3574) o… |
| SA-7 | deepseek/deepseek-v3.2 | 61,933 | 3,431 | 0 | 0 | $0.0174 | ✅ 5F/25E | Trace L1:F2116 at pos=7 - this has positive effect (0.377) o… |
| SA-9 | deepseek/deepseek-v3.2 | 69,943 | 3,233 | 0 | 0 | $0.0194 | ✅ 6F/18E | Trace L3:F8382 at pos=13 - this has positive effect (0.3281)… |
| SA-10 | deepseek/deepseek-v3.2 | 92,962 | 4,068 | 9,728 | 0 | $0.0260 | ✅ 9F/20E | Trace L3:F13271 at pos=5 - this has positive effect (0.3555)… |
| **Total** | | **694,211** | **38,845** | **82,471** | **0** | **$0.2060** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 10m 29s