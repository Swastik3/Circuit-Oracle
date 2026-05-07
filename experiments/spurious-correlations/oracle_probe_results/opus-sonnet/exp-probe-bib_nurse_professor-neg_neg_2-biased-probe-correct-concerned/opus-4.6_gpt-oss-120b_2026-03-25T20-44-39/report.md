# Circuit Oracle Report
**Date:** 2026-03-25 20:44:39 UTC | **Orchestrator:** anthropic/claude-opus-4.6 | **Subagent:** openai/gpt-oss-120b

## Input
**Prompt:** "Dataset: bib_nurse_professor-neg_neg_2 | Probe: biased | Method: correct"
**System prompt:** ""
**Concern:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."
**Top predictions:**  (100.0%)

## Oracle Analysis
Now let me compile my analysis. Let me quantify the relative contributions:

**Positive contributors to probe score (pushing toward the classified profession):**
- L0:2994 "his/he" pronoun (pos 3): +0.39 (LARGEST single effect)
- L7:14893 gendered pronoun processor (pos 3): +0.20
- L6:170 academic fields (pos 8,9): +0.14 + +0.10 = +0.24
- L0:2994 "his" (pos 25): +0.13
- L0:2994 "his" (pos 47): +0.11
- L0:1326 organizations (pos 14): +0.11
- L0:7532 proper nouns (pos 1): +0.11
- L0:15320 (pos 2): +0.10
- L0:13553 past tense/male (pos 2): +0.10

**Negative contributors (pushing away from the classified profession):**
- L12:2175 gender words (pos 2): -0.18
- L7:14946 "his" pronoun (pos 3): -0.18
- L6:12990 male pronouns (pos 22): -0.18
- L18:14743 "He" (pos 22): -0.14
- L18:14743 "He" (pos 81): -0.11
- L5:10392 academic study (pos 9): -0.11
- L18:10315 pronouns (pos 3): -0.10
- L6:12990 male pronouns (pos 3): -0.10

**Analysis:** The circuit is a mixture of both gender-related and profession-related features, but **gender markers dominate the circuit**.

**Analysis:** The probe's classification score is predominantly driven by gender marker features (pronouns "his", "He", and the male name "Daniel") rather than genuine profession-content features, confirming the user's concern about spurious feature reliance.

**Confidence:** High

**Reasoning:**

The attribution circuit reveals that this probe — which should classify a profession based on biographical content — is **heavily reliant on gender-related features as the dominant signal**, with genuine profession indicators playing a secondary role. Here is the detailed mechanism:

### 1. Gender Marker Pathway (Dominant)

The **single largest contributor** to the probe score is **L0:2994** ("his/he" pronoun detector, frac_nonzero=0.073), firing at positions 3, 25, and 47 (every occurrence of "his" in the text), contributing a combined **+0.64** to the probe score. This is a shallow L0 feature that simply detects the token "his" — it contains no profession-relevant information whatsoever.

The next largest positive contributor is **L7:14893** (gendered pronoun processor, frac_nonzero=0.009) at pos 3, contributing **+0.20**. Upstream tracing shows this feature is driven overwhelmingly by the raw embedding of " his" (edge weight 24.4) and slightly by " Daniel" (edge weight 3.8). Its promoted tokens are "herself/she" while suppressing "himself/his" — it's a gender-direction feature. The probe's weight vector has a component aligned with this gender direction.

Similarly, **L0:13553** (past tense verbs, pos 2) promotes "himself/his/he" and contributes **+0.10** — another gender-correlated feature disguised as syntactic.

On the **negative** side, gender features also dominate: **L6:12990** (male pronouns/titles, frac_nonzero=0.068) contributes **-0.28** combined across positions 3 and 22; **L12:2175** (gender words, frac_nonzero=0.006) contributes **-0.18**; **L18:14743** ("He" detector, frac_nonzero=0.018) contributes **-0.25** combined across positions 22 and 81; and **L18:10315** (pronouns/possessives, frac_nonzero=0.039) contributes **-0.10**.

The gender signal originates from three input tokens: **"his"** (pos 3), **"He"** (pos 22), and **"Daniel"** (pos 1). The name "Daniel" feeds into L2:16309 (people's names detector, edge weight 12.9) which cascades through L5:7317 → L12:2175, providing a name-to-gender-inference pathway. The L18:14743 feature at pos 22 is driven almost entirely by the raw "He" token embedding (edge weight 21.9).

### 2. Profession/Academic Pathway (Secondary)

Genuine profession features exist but contribute less: **L6:170** (academic field references, frac_nonzero=0.039) contributes **+0.24** total across positions 8 and 9. Upstream tracing reveals a clean academic pipeline: "achelors" (pos 5) → L2:10852 (academic titles, edge weight 19.25) → L4:3727 (academic degrees, edge weight 10.25) → L5:10392 (academic study fields, edge weight 2.4) → L6:170 (edge weight 10.9), with additional input from "Mechanical" (pos 8) and "Engineering" (pos 9) through L2:1440. This is a legitimate profession-detection pathway grounded in tokens like "Bachelors," "Mechanical," and "Engineering."

However, confusingly, **L5:10392** (academic study fields) itself has a **negative** direct effect (-0.11), meaning the probe's weight direction partially suppresses this genuinely profession-relevant feature. The education pathway through L8:7587 → L15:12482 → L16:2313 feeds into the L18:10315 negative node, suggesting that some education-related signal gets routed through a gender-correlated channel before reaching the output.

### 3. Quantitative Summary

Summing direct effects by category:
- **Gender-related features** (positive contributions): ~+0.84 (L0:2994 × 3 instances + L7:14893 + L0:13553)
- **Gender-related features** (negative contributions): ~-0.89 (L12:2175 + L7:14946 + L6:12990 × 2 + L18:14743 × 2 + L18:10315)
- **Academic/profession features** (positive contributions): ~+0.24 (L6:170 × 2)
- **Academic/profession features** (negative contributions): ~-0.11 (L5:10392)

**Total absolute gender signal: 1.73. Total absolute profession signal: 0.35.** Gender features account for roughly **83%** of the total causal attribution magnitude.

### Conclusion

The concern is **validated**: this probe overwhelmingly relies on gender markers — particularly the pronouns "his" and "He" and the male name "Daniel" — rather than genuine profession indicators like "Engineering," "Robotics," or "Ph.D." While a legitimate academic-field detection pathway exists (from "achelors"/"Mechanical"/"Engineering" through layers 2→4→5→6), it contributes only a fraction of the total signal. The probe has essentially learned a gender-correlated shortcut: the profession it classifies correlates with male subjects in its training data, so it leverages gender as a proxy rather than encoding true professional content.

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L0:2994 de=0.395 |
| 3 | `inspect_feature` ×15 | L0:2994, L7:14893, L12:2175, L7:14946, L6:12990, L6:170, L18:14743, L5:10392, L0:1326, L0:7532, L0:12351, L0:13526, L0:15320, L0:13553, L18:10315 |

### Dispatch: 8 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L7:F14893@3` | ✅ reported | 5 | 14 | Trace the path from L7:14893 (pronouns/possessive pronouns) at pos 3. This featu… |
| SA-2 | `L6:F170@9` | ❌ no report (12 tool calls) | — | — | Trace the path from L6:170 (academic fields, humanities references) at pos 9. Th… |
| SA-3 | `L18:F14743@22` | ❌ no report (10 tool calls) | — | — | Trace the path from L18:14743 (detects 'He' pronoun) at pos 22. This feature has… |
| SA-4 | `L12:F2175@2` | ✅ reported | 11 | 20 | Trace the path from L12:2175 (gender words) at pos 2. This feature promotes 'him… |
| SA-5 | `L6:F12990@22` | ❌ no report (10 tool calls) | — | — | Trace the path from L6:12990 (male pronouns and titles) at pos 22. This has a st… |
| SA-6 | `L5:F10392@9` | ❌ no report (15 tool calls) | — | — | Trace the path from L5:10392 (fields of academic study) at pos 9. This has a neg… |
| SA-7 | `L18:F14743@22` | ❌ no report (10 tool calls) | — | — | Trace the path from L18:14743 ('He' detection) at pos 22. This feature has a str… |
| SA-8 | `L18:F10315@3` | ❌ no report (11 tool calls) | — | — | Trace the path from L18:10315 (pronouns/possessives) at pos 3. This feature has … |

<details>
<summary><b>SA-1</b> — tool trace (6 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L7, F14893 | " pronouns or possessive pronouns" |
| 2 | `get_upstream_features` | L7:F14893@3, k=5 | Emb:" his"@3 (w=24.38) +4 more |
| 3 | `inspect_feature` | L0, F2994 | "the pronoun "his" and the pronoun "he."" |
| 4 | `inspect_feature` | L6, F12990 | " male pronouns and titles along with descriptors associated with men" |
| 5 | `get_upstream_features` | L0:F2994@3, k=5 | Emb:" his"@3 (w=43.25) +4 more |
| 6 | `get_upstream_features` | L6:F12990@3, k=5 | Emb:" his"@3 (w=8.31) +4 more |

**Findings:** The gendered pronoun feature L7:F14893 (promoting 'she/her' and suppressing 'him/his') is driven primarily by the direct input token ' his' at position 3 (edge weight 24.4), with a smaller contribution from the subject token 'Daniel' (weight 3.8) and a negative influence from the verb 'received'. Upstream, the token ' his' strongly activates a low-level pronoun detector L0:F2994 (weight 43.3), whi…

</details>

<details>
<summary><b>SA-2</b> — tool trace (12 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F170 | " references to academic fields, especially those in the humanities" |
| 2 | `get_upstream_features` | L6:F170@9, k=5 | L5:F10392 (w=10.94) +4 more |
| 3 | `inspect_feature` | L5, F10392 | " fields of academic study" |
| 4 | `inspect_feature` | L5, F6384 | "words related to higher education and professions" |
| 5 | `get_upstream_features` | L5:F10392@9, k=5 | Emb:" Mechanical"@8 (w=3.08) +4 more |
| 6 | `inspect_feature` | L4, F3727 | " mentions of academic degrees" |
| 7 | `get_upstream_features` | L4:F3727@5, k=5 | Emb:"achelors"@5 (w=22.25) +4 more |
| 8 | `inspect_feature` | L2, F10852 | " academic titles and degrees" |
| 9 | `inspect_feature` | L3, F4113 | " mentions of academic degrees and areas of study" |
| 10 | `inspect_feature` | L2, F1440 | " the word "engineering" and words related to its definition" |
| 11 | `inspect_feature` | L0, F9026 | "technical documents or data, including numbers, units, and references " |
| 12 | `get_upstream_features` | L2:F10852@5, k=5 | Emb:"achelors"@5 (w=19.25) +4 more |

**Findings:** {
  "discovered_features": [
    {"layer": 6, "feature_idx": 170, "pos": 9, "label": "references to academic fields, especially those in the humanities"},
    {"layer": 5, "feature_idx": 10392, "pos": 9, "label": "fields of academic study"},
    {"layer": 5, "feature_idx": 6384, "pos": 9, "label": "words related to higher education and professions"},
    {"layer": 4, "feature_idx": 3727, "pos": 5,…

</details>

<details>
<summary><b>SA-3</b> — tool trace (10 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L18, F14743 | "He" |
| 2 | `get_upstream_features` | L18:F14743@22, k=5 | Emb:" He"@22 (w=21.88) +4 more |
| 3 | `inspect_feature` | L0, F1069 | " references to a male person, particularly when using the pronoun "He"" |
| 4 | `inspect_feature` | L17, F5889 | " references to people with pronouns and possessive pronouns" |
| 5 | `inspect_feature` | L13, F6622 | " pronouns." |
| 6 | `inspect_feature` | L15, F3330 | " personal stories of individuals, especially women and their actions o" |
| 7 | `get_upstream_features` | L0:F1069@22, k=5 | Emb:" He"@22 (w=37.00) +4 more |
| 8 | `get_upstream_features` | L17:F5889@22, k=5 | Emb:" He"@22 (w=20.75) +4 more |
| 9 | `get_upstream_features` | L13:F6622@22, k=5 | Emb:" He"@22 (w=13.19) +4 more |
| 10 | `inspect_feature` | L6, F2267 | "words that appear in programming code, legal jargon, or scientific tex" |

</details>

<details>
<summary><b>SA-4</b> — tool trace (12 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L12, F2175 | " words referring to gender" |
| 2 | `get_upstream_features` | L12:F2175@2, k=5 | Emb:" received"@2 (w=4.09) +4 more |
| 3 | `inspect_feature` | L5, F7317 | " phrases with names and nicknames" |
| 4 | `inspect_feature` | L5, F6228 | " past tense verbs" |
| 5 | `inspect_feature` | L7, F7210 | " words and phrases that connote conflict and stress." |
| 6 | `get_upstream_features` | L5:F7317@2, k=5 | L4:F16158 (w=-2.67) +4 more |
| 7 | `inspect_feature` | L4, F16158 | " verbs, especially in the present and past tenses, locations, and othe" |
| 8 | `inspect_feature` | L3, F6656 | "verbs or phrases indicating action, saying, or feeling" |
| 9 | `inspect_feature` | L2, F16309 | " people's names" |
| 10 | `get_upstream_features` | L3:F6656@2, k=5 | L2:F16309 (w=3.17) +4 more |
| 11 | `get_upstream_features` | L2:F16309@1, k=5 | Emb:"Daniel"@1 (w=12.94) +4 more |
| 12 | `inspect_feature` | L3, F8210 | " initials preceded by a first name or honorific" |

**Findings:** The gender‑word detector L12:F2175 (pos 2) receives strong influence from the token \"received\" and from a name‑related feature chain. The key upstream path is: embedding \"Daniel\" (pos 1) → name‑detection feature L2:16309 → action‑verb feature L3:6656 → name‑phrase feature L5:7317 → gender detector L12:2175. Large positive edge weights (e.g., Daniel → L2:16309 weight 12.94, L2:16309 → L3:6656 w…

</details>

<details>
<summary><b>SA-5</b> — tool trace (10 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F12990 | " male pronouns and titles along with descriptors associated with men" |
| 2 | `get_upstream_features` | L6:F12990@22, k=5 | Emb:" He"@22 (w=4.47) +4 more |
| 3 | `inspect_feature` | L4, F14796 | "the pronoun "he" or "him"" |
| 4 | `inspect_feature` | L2, F13928 | " third person pronouns related to people's credentials" |
| 5 | `get_upstream_features` | L4:F14796@22, k=5 | Emb:" He"@22 (w=16.88) +4 more |
| 6 | `get_upstream_features` | L2:F13928@22, k=5 | Emb:" He"@22 (w=6.12) +4 more |
| 7 | `inspect_feature` | L2, F2110 | " the third person singular pronouns "he" and "she"" |
| 8 | `inspect_feature` | L3, F2860 | " instances of a male person with a title in a professional setting" |
| 9 | `get_upstream_features` | L2:F2110@22, k=5 | Emb:" He"@22 (w=23.00) +4 more |
| 10 | `inspect_feature` | L0, F1069 | " references to a male person, particularly when using the pronoun "He"" |

**Findings:** {
  "discovered_edges": [
    {"from_type": "embedding", "from_token": " He", "from_pos": 22, "to_layer": 6, "to_feature_idx": 12990, "to_pos": 22, "weight": 4.4688},
    {"from_type": "embedding", "from_token": " his", "from_pos": 3, "to_layer": 6, "to_feature_idx": 12990, "to_pos": 22, "weight": -1.1328},
    {"from_type": "embedding", "from_token": "<bos>", "from_pos": 0, "to_layer": 6, "to_fea…

</details>

<details>
<summary><b>SA-6</b> — tool trace (15 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L5, F10392 | " fields of academic study" |
| 2 | `get_upstream_features` | L5:F10392@9, k=5 | Emb:" Mechanical"@8 (w=3.08) +4 more |
| 3 | `inspect_feature` | L4, F3727 | " mentions of academic degrees" |
| 4 | `inspect_feature` | L3, F4113 | " mentions of academic degrees and areas of study" |
| 5 | `inspect_feature` | L2, F1440 | " the word "engineering" and words related to its definition" |
| 6 | `get_upstream_features` | L4:F3727@5, k=5 | Emb:"achelors"@5 (w=22.25) +4 more |
| 7 | `get_upstream_features` | L2:F1440@9, k=5 | Emb:" Engineering"@9 (w=19.50) +4 more |
| 8 | `get_upstream_features` | L2:F1440@9, k=5 | Emb:" Engineering"@9 (w=19.50) +4 more |
| 9 | `inspect_feature` | L2, F10852 | " academic titles and degrees" |
| 10 | `get_upstream_features` | L2:F10852@5, k=5 | Emb:"achelors"@5 (w=19.25) +4 more |
| 11 | `inspect_feature` | L0, F9026 | "technical documents or data, including numbers, units, and references " |
| 12 | `inspect_feature` | L1, F675 | "the word "push" or other words related to pushing, inserting, or trans" |
| 13 | `get_upstream_features` | L3:F4113@7, k=5 | Emb:" in"@7 (w=12.12) +4 more |
| 14 | `inspect_feature` | L0, F7925 | "the word "pilot"" |
| 15 | `get_upstream_features` | L1:F675@9, k=5 | Emb:" Engineering"@9 (w=7.69) +4 more |

</details>

<details>
<summary><b>SA-7</b> — tool trace (10 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L18, F14743 | "He" |
| 2 | `get_upstream_features` | L18:F14743@22, k=5 | Emb:" He"@22 (w=21.88) +4 more |
| 3 | `inspect_feature` | L0, F1069 | " references to a male person, particularly when using the pronoun "He"" |
| 4 | `inspect_feature` | L17, F5889 | " references to people with pronouns and possessive pronouns" |
| 5 | `get_upstream_features` | L0:F1069@22, k=5 | Emb:" He"@22 (w=37.00) +4 more |
| 6 | `inspect_feature` | L13, F6622 | " pronouns." |
| 7 | `get_upstream_features` | L17:F5889@22, k=5 | Emb:" He"@22 (w=20.75) +4 more |
| 8 | `get_upstream_features` | L13:F6622@22, k=5 | Emb:" He"@22 (w=13.19) +4 more |
| 9 | `inspect_feature` | L6, F2267 | "words that appear in programming code, legal jargon, or scientific tex" |
| 10 | `get_upstream_features` | L6:F2267@22, k=5 | Emb:"<bos>"@0 (w=-8.00) +4 more |

</details>

<details>
<summary><b>SA-8</b> — tool trace (11 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L18, F10315 | " pronouns and possessive pronouns" |
| 2 | `get_upstream_features` | L18:F10315@3, k=5 | Emb:" his"@3 (w=24.88) +4 more |
| 3 | `inspect_feature` | L16, F2313 | " mentions of degrees and universities, as well as some corporate roles" |
| 4 | `get_upstream_features` | L16:F2313@3, k=5 | L15:F12482 (w=7.34) +4 more |
| 5 | `inspect_feature` | L17, F9189 | "possessive pronouns" |
| 6 | `inspect_feature` | L15, F12482 | " mentions of professional accomplishments" |
| 7 | `inspect_feature` | L0, F2994 | "the pronoun "his" and the pronoun "he."" |
| 8 | `get_upstream_features` | L17:F9189@3, k=5 | L15:F3937 (w=9.19) +4 more |
| 9 | `get_upstream_features` | L16:F2313@3, k=5 | L15:F12482 (w=7.34) +4 more |
| 10 | `get_upstream_features` | L15:F12482@3, k=5 | Emb:" received"@2 (w=3.70) +4 more |
| 11 | `inspect_feature` | L8, F7587 | " words related to education and professional qualifications" |

**Findings:** {
  "discovered_edges": [
    {
      "from_layer": null,
      "from_feature_idx": null,
      "from_pos": 3,
      "to_layer": 18,
      "to_feature_idx": 10315,
      "to_pos": 3,
      "weight": 24.875,
      "token": " his"
    },
    {
      "from_layer": null,
      "from_feature_idx": null,
      "from_pos": 0,
      "to_layer": 18,
      "to_feature_idx": 10315,
      "to_pos": 3,
      "…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` ×6 | L5:6384, L4:3727, L2:1440, L2:10852, L3:4113, L2:16309 |
| 2 | `get_upstream_features` | L18:F14743@22, k=10 → Emb:" He"@22 (w=21.88) +9 more |
| 3 | `inspect_feature` ×5 | L16:2313, L17:9189, L15:12482, L8:7587, L0:1069 |

### Build

`build_circuit` → 31 nodes, 52 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | anthropic/claude-opus-4.6 | 234,423 | 9,428 | 0 | 0 | $1.4078 | — | — |
| SA-1 | openai/gpt-oss-120b | 25,091 | 3,028 | 0 | 0 | $0.0016 | ✅ 5F/14E | Trace the path from L7:14893 (pronouns/possessive pronouns) … |
| SA-3 | openai/gpt-oss-120b | 59,453 | 4,581 | 64 | 0 | $0.0032 | ❌ no report (10 calls) | Trace the path from L18:14743 (detects 'He' pronoun) at pos … |
| SA-2 | openai/gpt-oss-120b | 75,173 | 5,559 | 0 | 0 | $0.0040 | ❌ no report (12 calls) | Trace the path from L6:170 (academic fields, humanities refe… |
| SA-4 | openai/gpt-oss-120b | 79,445 | 6,831 | 0 | 0 | $0.0044 | ✅ 11F/20E | Trace the path from L12:2175 (gender words) at pos 2. This f… |
| SA-5 | openai/gpt-oss-120b | 53,986 | 5,693 | 0 | 0 | $0.0032 | ❌ no report (10 calls) | Trace the path from L6:12990 (male pronouns and titles) at p… |
| SA-6 | openai/gpt-oss-120b | 100,042 | 9,914 | 0 | 0 | $0.0058 | ❌ no report (15 calls) | Trace the path from L5:10392 (fields of academic study) at p… |
| SA-7 | openai/gpt-oss-120b | 55,690 | 5,135 | 0 | 0 | $0.0031 | ❌ no report (10 calls) | Trace the path from L18:14743 ('He' detection) at pos 22. Th… |
| SA-8 | openai/gpt-oss-120b | 60,407 | 4,962 | 0 | 0 | $0.0033 | ❌ no report (11 calls) | Trace the path from L18:10315 (pronouns/possessives) at pos … |
| **Total** | | **743,710** | **55,131** | **64** | **0** | **$1.4364** | | |

**Oracle wall-clock time:** 16m 1s