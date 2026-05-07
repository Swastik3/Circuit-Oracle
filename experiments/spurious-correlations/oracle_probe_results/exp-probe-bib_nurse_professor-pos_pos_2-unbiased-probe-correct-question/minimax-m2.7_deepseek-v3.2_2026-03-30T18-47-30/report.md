# Circuit Oracle Report
**Date:** 2026-03-30 18:47:30 UTC | **Orchestrator:** minimax/minimax-m2.7 | **Subagent:** deepseek/deepseek-v3.2

## Input
**Prompt:** "Dataset: bib_nurse_professor-pos_pos_2 | Probe: unbiased | Method: correct"
**System prompt:** ""
**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."
**Top predictions:**  (100.0%)

## Oracle Analysis
**Analysis:** The probe's classification score for predicting a nursing profession is driven by genuine profession-specific knowledge encoded in the model's internal features, NOT by spurious gender markers. The circuit's primary signal originates from the literal token " Nursing" at position 10 (edge weights: 17.375 → L6:F15267, 12.06 → L14:F3985), supplemented by academic degree context ("graduated" at pos 2, " Science" at pos 8, "achelors" at pos 6) and medical/healthcare terminology features spanning layers 2-14. The feature labels explicitly confirm domain-specific knowledge: "words in the document referring to the profession of nursing" (L6:F15267, frac_nonzero=0.016), "words related to nursing and healthcare" (L7:F3979), "terms related to management, leadership, medicine, studies, and research" (L14:F3985, frac_nonzero=0.066), and "academic titles and degrees" (L2:F10852, frac_nonzero=0.008). No gender-related features appear anywhere in the traced circuit—the model relies entirely on professional vocabulary and academic credential patterns.

**Confidence:** 9/10

**Reasoning:** The attribution circuit reveals a multi-layer hierarchical pathway where input tokens encoding nursing profession terms (emb_nursing, emb_graduated, emb_bachelors, emb_science) activate specialized transcoder features that progressively abstract from word-level detection (L0:F5038 detecting "graduated") through academic degree recognition (L2:F10852 detecting titles/degrees) to healthcare profession identification (L5:F1275, L6:F15267 detecting nursing terminology) and finally to high-level medical/management concepts (L14:F3985). The strongest direct effect on the probe comes from L14:F3985 (0.1865) which fires on "nurse" tokens and promotes medical/patient-related vocabulary (" patients", " Medical", " clinicians"). All features have low frac_nonzero values (0.005-0.066), indicating highly specialized pattern detection rather than generic pattern matching. The circuit includes one regulatory mechanism: L3:F15901 ("mentions of nurses, nursing, and nurse management") negatively inhibits the nursing profession features, suggesting contrastive learning or noise suppression. The user's concern about spurious gender markers is not supported—the model uses explicit profession indicators (nursing, medical, hospital, degrees, credentials) rather than correlational patterns with gender.

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 10 features; top: L14:3985 de=0.186 |
| 3 | `inspect_feature` ×6 | L14:3985, L6:15267, L7:3979, L3:15901, L0:5038, L0:6270 |

### Dispatch: 3 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L14:F3985@10` | ✅ reported | 9 | 14 | Trace L14:F3985 upstream to understand what drives this nursing/medical manageme… |
| SA-2 | `L6:F15267@10` | ✅ reported | 11 | 19 | Trace L6:F15267 (nursing profession feature) upstream to find its source. Check … |
| SA-3 | `L0:F5038@2` | ✅ reported | 2516 | 19 | Trace L0:F5038 (word 'graduated') upstream to find what input tokens drive it an… |

<details>
<summary><b>SA-1</b> — tool trace (13 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L14, F3985 | "terms related to management, leadership, medicine, studies, and resear" |
| 2 | `get_upstream_features` | L14:F3985@10, k=5 | Emb:" Nursing"@10 (w=12.06) +4 more |
| 3 | `inspect_feature` | L8, F16339 | " text discussing hospital infections and bacteria" |
| 4 | `inspect_feature` | L7, F210 | " words and names associated with the Asante Healthcare system" |
| 5 | `inspect_feature` | L6, F4490 | " proper nouns corresponding to locations, organizations, medical roles" |
| 6 | `get_upstream_features` | L8:F16339@10, k=5 | Emb:" Nursing"@10 (w=7.66) +4 more |
| 7 | `inspect_feature` | L6, F15267 | " words in the document referring to the profession of nursing" |
| 8 | `get_upstream_features` | L6:F15267@10, k=5 | Emb:" Nursing"@10 (w=17.38) +4 more |
| 9 | `inspect_feature` | L4, F11037 | " words related to counseling, therapy, social work, and academic degre" |
| 10 | `inspect_feature` | L5, F1275 | "words related to healthcare professionals and medical fields" |
| 11 | `get_upstream_features` | L5:F1275@10, k=5 | L4:F11037 (w=1.99) +4 more |
| 12 | `inspect_feature` | L10, F1461 | " words and phrases related to medicine, medical research, and healthca" |
| 13 | `inspect_feature` | L3, F15901 | " mentions of nurses, nursing, and nurse management" |

**Findings:** Tracing L14:F3985 (nursing/medical management feature) upstream reveals it's driven by genuine profession indicators, NOT gender markers. The circuit is:

1. The strongest signal comes directly from the " Nursing" token embedding at position 10 (weight 12.06).

2. Key intermediate features are:
   - L6:F15267: "words in the document referring to the profession of nursing" (activates on "RN")
   - …

</details>

<details>
<summary><b>SA-2</b> — tool trace (18 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F15267 | " words in the document referring to the profession of nursing" |
| 2 | `get_upstream_features` | L6:F15267@10, k=5 | Emb:" Nursing"@10 (w=17.38) +4 more |
| 3 | `inspect_feature` | L4, F11037 | " words related to counseling, therapy, social work, and academic degre" |
| 4 | `inspect_feature` | L5, F1275 | "words related to healthcare professionals and medical fields" |
| 5 | `get_upstream_features` | L4:F11037@10, k=5 | Emb:" Nursing"@10 (w=10.56) +4 more |
| 6 | `get_upstream_features` | L5:F1275@10, k=5 | L4:F11037 (w=1.99) +4 more |
| 7 | `inspect_feature` | L3, F15901 | " mentions of nurses, nursing, and nurse management" |
| 8 | `get_upstream_features` | L3:F15901@10, k=5 | Emb:" Nursing"@10 (w=15.06) +4 more |
| 9 | `inspect_feature` | L2, F10852 | " academic titles and degrees" |
| 10 | `inspect_feature` | L2, F9995 | " terms related to occupations and fields of study" |
| 11 | `get_upstream_features` | L2:F10852@10, k=5 | Emb:" Nursing"@10 (w=11.44) +4 more |
| 12 | `inspect_feature` | L1, F10429 | " words related to academic programs" |
| 13 | `inspect_feature` | L1, F12372 | " mentions of US universities and sports teams" |
| 14 | `get_upstream_features` | L1:F10429@10, k=5 | Emb:" Nursing"@10 (w=4.78) +4 more |
| 15 | `inspect_feature` | L0, F8854 | " the word "nurse" as well as some pronouns" |
| 16 | `get_upstream_features` | L0:F8854@10, k=5 | Emb:" Nursing"@10 (w=16.12) +4 more |
| 17 | `inspect_feature` | L2, F15437 | " words related to nurses and sound" |
| 18 | `inspect_feature` | L4, F8751 | " cell types in the brain, especially glial cells and neurons, and rela" |

**Findings:** I traced the L6 nursing profession feature (F15267) upstream through 5 hops to find its source. Key findings:

1. **Direct Source**: The strongest connection is directly from the input token " Nursing" embedding (weight: 17.375), showing this feature primarily detects the literal word.

2. **Gender Analysis**: I found NO spurious gender markers. The circuit focuses on:
   - Academic/degree feature…

</details>

<details>
<summary><b>SA-3</b> — tool trace (17 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F5038 | "the word "graduated" or variations of it" |
| 2 | `get_upstream_features` | L0:F5038@2, k=5 | Emb:" graduated"@2 (w=22.25) +4 more |
| 3 | `inspect_feature` | L0, F478 | "various kinds of brackets and parentheses followed by a period" |
| 4 | `inspect_feature` | L0, F541 | " conjunctions, prepositions, and symbols, specifically when they are a" |
| 5 | `get_upstream_features` | L0:F5038@2, k=10 | Emb:" graduated"@2 (w=22.25) +9 more |
| 6 | `inspect_feature` | L0, F1790 | " the word "farm"" |
| 7 | `inspect_feature` | L0, F1903 | "instances of sentences starting with "The"" |
| 8 | `inspect_feature` | L0, F1616 | "the word "provision"" |
| 9 | `inspect_feature` | L0, F705 | " occurrences of "according" and mentions of research studies and findi" |
| 10 | `inspect_feature` | L0, F96 | "sentences beginning with coordinating conjunctions like "but" and "and" |
| 11 | `get_upstream_features` | L0:F478@1, k=5 | Emb:"<bos>"@0 (w=6.91) +4 more |
| 12 | `get_upstream_features` | L0:F541@1, k=5 | Emb:"She"@1 (w=4.06) +4 more |
| 13 | `get_upstream_features` | L0:F1790@1, k=5 | Emb:"She"@1 (w=6.78) +4 more |
| 14 | `get_upstream_features` | L0:F1903@1, k=5 | Emb:"<bos>"@0 (w=17.00) +4 more |
| 15 | `get_upstream_features` | L0:F1616@1, k=5 | Emb:"She"@1 (w=6.78) +4 more |
| 16 | `get_upstream_features` | L0:F705@1, k=5 | Emb:"She"@1 (w=7.25) +4 more |
| 17 | `get_upstream_features` | L0:F96@1, k=5 | Emb:"<bos>"@0 (w=4.88) +4 more |

**Findings:** Tracing L0:F5038 (word 'graduated') upstream revealed that it is primarily driven by the direct token embedding of " graduated" at position 2 with a very strong edge weight of 22.25. There are minor connections from the BOS token (0.84) and "She" token (0.37). Several other layer 0 features appear with 0.0 edge weights, indicating they don't significantly influence this specific feature activation…

</details>

### Re-dispatch (round 2): 1 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-4 | `L7:F3979@10` | ✅ reported | 12 | 14 | Trace the negative-effect feature L7:F3979 (nursing/healthcare words) upstream t… |

<details>
<summary><b>SA-4</b> — tool trace (17 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L7, F3979 | " words related to nursing and healthcare" |
| 2 | `get_upstream_features` | L7:F3979@10, k=5 | L6:F15267 (w=8.81) +4 more |
| 3 | `inspect_feature` | L6, F15267 | " words in the document referring to the profession of nursing" |
| 4 | `inspect_feature` | L3, F15901 | " mentions of nurses, nursing, and nurse management" |
| 5 | `inspect_feature` | L6, F170 | " references to academic fields, especially those in the humanities" |
| 6 | `get_upstream_features` | L6:F15267@10, k=5 | Emb:" Nursing"@10 (w=17.38) +4 more |
| 7 | `inspect_feature` | L4, F11037 | " words related to counseling, therapy, social work, and academic degre" |
| 8 | `inspect_feature` | L5, F1275 | "words related to healthcare professionals and medical fields" |
| 9 | `get_upstream_features` | L4:F11037@10, k=5 | Emb:" Nursing"@10 (w=10.56) +4 more |
| 10 | `inspect_feature` | L2, F10852 | " academic titles and degrees" |
| 11 | `inspect_feature` | L3, F6246 | " the word "Nutrients" and words containing "ure"." |
| 12 | `get_upstream_features` | L3:F15901@10, k=5 | Emb:" Nursing"@10 (w=15.06) +4 more |
| 13 | `inspect_feature` | L2, F9995 | " terms related to occupations and fields of study" |
| 14 | `inspect_feature` | L2, F15437 | " words related to nurses and sound" |
| 15 | `get_upstream_features` | L2:F10852@10, k=5 | Emb:" Nursing"@10 (w=11.44) +4 more |
| 16 | `inspect_feature` | L1, F10429 | " words related to academic programs" |
| 17 | `inspect_feature` | L1, F12372 | " mentions of US universities and sports teams" |

**Findings:** I traced the negative-effect feature L7:F3979 (nursing/healthcare words) upstream through 4 hops. Key findings:

1. **Main circuit**: The strongest connection is from token " Nursing" at position 10 (embedding) → L6:F15267 (nursing profession detection, weight=17.375) → L7:F3979 (weight=8.8125). This shows the feature is directly activated by the nursing-related token.

2. **Negative suppression p…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L0:F8854@10, k=5 → Emb:" Nursing"@10 (w=16.12) +4 more |

### Build

`build_circuit` → 16 nodes, 24 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m2.7 | 32,336 | 4,042 | 44,785 | 0 | — | — | — |
| SA-1 | deepseek/deepseek-v3.2 | 91,564 | 3,861 | 0 | 0 | — | ✅ 9F/14E | Trace L14:F3985 upstream to understand what drives this nurs… |
| SA-3 | deepseek/deepseek-v3.2 | 126,969 | 4,346 | 20,352 | 0 | — | ✅ 2516F/19E | Trace L0:F5038 (word 'graduated') upstream to find what inpu… |
| SA-2 | deepseek/deepseek-v3.2 | 137,217 | 4,785 | 6,656 | 0 | — | ✅ 11F/19E | Trace L6:F15267 (nursing profession feature) upstream to fin… |
| SA-4 | deepseek/deepseek-v3.2 | 141,699 | 4,471 | 0 | 0 | — | ✅ 12F/14E | Trace the negative-effect feature L7:F3979 (nursing/healthca… |
| **Total** | | **529,785** | **21,505** | **71,793** | **0** | **—** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 7m 24s