# Circuit Oracle Report
**Date:** 2026-04-06 08:47:11 UTC | **Orchestrator:** minimax/minimax-m2.7 | **Subagent:** deepseek/deepseek-v3.2

## Input

**Prompt:** "Dataset: bib_nurse_professor-pos_pos_4 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "('The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession.',)"

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification of Lori as a nurse is driven by a hierarchical circuit of genuine profession indicators (nursing/medical terminology at positions 18, 32, 33) rather than spurious gender markers.

**Confidence:** 9/10

**Reasoning:**

The circuit analysis reveals that the probe classification is driven by **genuine profession indicators**, not spurious gender markers:

1. **Primary Input Drivers**: The strongest signals originate from profession-specific tokens:
   - " Nursing" (pos 18) with edge weight 42.75 → L18:F13596
   - " nurse" (pos 32) and " practitioner" (pos 33) feeding into L6:F15267
   - "graduated" (pos 2) and "University" (pos 6) for educational context

2. **Late-layer Features Encode Profession Concepts**:
   - **L18:F13596** (frac_nonzero=0.00495): "text about the role, skills and leadership of nurse managers" — promoted tokens are "Nurse", "nurse", "Nursing" — all profession terms
   - **L14:F3985** (frac_nonzero=0.06604): "management, leadership, medicine, studies, and research" — promoted tokens are "patients", "Medical", "clinicians"
   - **L6:F15267** (frac_nonzero=0.01594): "words in the document referring to the profession of nursing" — activates on "RN", "DNP" contexts

3. **No Gender Markers Found**: The name "Lori" has minimal influence (edge weight 0.4473 to L0:F5038) compared to profession tokens. None of the features show gender-specific patterns in their labels, top activating examples, or promoted tokens.

4. **Specificity Confirmed**: All key features have low frac_nonzero values (0.00495–0.066), indicating highly specific encoding of nursing/medical concepts rather than generic patterns.

The circuit flows: embedding tokens ("Nursing", "nurse", "practitioner") → early medical/nursing detection features (L1-L4) → nursing profession aggregator (L6) → nurse manager leadership (L18) → medical management terms (L14) → probe output. This represents a legitimate profession classification hierarchy with no spurious gender reliance.

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L14:3985 de=0.156 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L14:F3985@18` | ✅ reported | 14 | 23 | Trace this feature upstream. What does L14:F3985 encode? What features feed into… |
| SA-2 | `L6:F15267@33` | ✅ reported | 9 | 12 | Trace this feature upstream. What does L6:F15267 encode? What features feed into… |
| SA-3 | `L18:F13596@18` | ✅ reported | 9 | 19 | Trace this feature upstream. L18:F13596 has high activation 51.75. What does thi… |
| SA-4 | `L7:F3979@33` | ✅ reported | 10 | 30 | Trace this feature upstream. L7:F3979 has negative direct effect at pos 33. What… |

<details>
<summary><b>SA-1</b> — tool trace (22 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L14, F3985 | "terms related to management, leadership, medicine, studies, and resear" |
| 2 | `get_upstream_features` | L14:F3985@18, k=5 | Emb:" Nursing"@18 (w=11.62) +4 more |
| 3 | `inspect_feature` | L8, F16339 | " text discussing hospital infections and bacteria" |
| 4 | `inspect_feature` | L6, F4490 | " proper nouns corresponding to locations, organizations, medical roles" |
| 5 | `inspect_feature` | L7, F210 | " words and names associated with the Asante Healthcare system" |
| 6 | `inspect_feature` | L10, F1461 | " words and phrases related to medicine, medical research, and healthca" |
| 7 | `get_upstream_features` | L8:F16339@18, k=5 | Emb:" Nursing"@18 (w=7.28) +4 more |
| 8 | `inspect_feature` | L6, F15267 | " words in the document referring to the profession of nursing" |
| 9 | `inspect_feature` | L7, F5829 | "mentions of nursing or higher education degrees." |
| 10 | `get_upstream_features` | L6:F4490@18, k=5 | Emb:" Nursing"@18 (w=11.56) +4 more |
| 11 | `get_upstream_features` | L6:F15267@18, k=5 | Emb:" Nursing"@18 (w=17.38) +4 more |
| 12 | `inspect_feature` | L4, F11037 | " words related to counseling, therapy, social work, and academic degre" |
| 13 | `inspect_feature` | L3, F15901 | " mentions of nurses, nursing, and nurse management" |
| 14 | `inspect_feature` | L5, F10392 | " fields of academic study" |
| 15 | `inspect_feature` | L5, F1275 | "words related to healthcare professionals and medical fields" |
| 16 | `get_upstream_features` | L3:F15901@18, k=5 | Emb:" Nursing"@18 (w=15.19) +4 more |
| 17 | `inspect_feature` | L2, F9995 | " terms related to occupations and fields of study" |
| 18 | `get_upstream_features` | L10:F1461@18, k=5 | Emb:" Nursing"@18 (w=2.86) +4 more |
| 19 | `get_upstream_features` | L7:F210@18, k=5 | Emb:" Nursing"@18 (w=7.88) +4 more |
| 20 | `get_upstream_features` | L6:F4490@18, k=5 | Emb:" Nursing"@18 (w=11.56) +4 more |
| 21 | `inspect_feature` | L1, F14469 | " mentions of 'nurse'" |
| 22 | `inspect_feature` | L5, F15608 | " titles, names, and mentions of people in official roles" |

**Findings:** L14:F3985 encodes "terms related to management, leadership, medicine, studies, and research" - it's a PROFESSION INDICATOR specifically for healthcare/medical management professions. 

The circuit analysis reveals:

1. PRIMARY DRIVER: The token " Nursing" at position 18 is the strongest direct input (edge_weight: 11.625) to L14:F3985. This is an embedding node, meaning the raw token representation…

</details>

<details>
<summary><b>SA-2</b> — tool trace (14 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F15267 | " words in the document referring to the profession of nursing" |
| 2 | `get_upstream_features` | L6:F15267@33, k=5 | Emb:" nurse"@32 (w=5.66) +4 more |
| 3 | `inspect_feature` | L5, F1275 | "words related to healthcare professionals and medical fields" |
| 4 | `inspect_feature` | L4, F11037 | " words related to counseling, therapy, social work, and academic degre" |
| 5 | `inspect_feature` | L1, F1494 | " words related to medical practices and studies." |
| 6 | `get_upstream_features` | L5:F1275@33, k=5 | L4:F9036 (w=1.70) +4 more |
| 7 | `inspect_feature` | L4, F9036 | " words and abbreviations associated with healthcare." |
| 8 | `get_upstream_features` | L4:F9036@33, k=5 | Emb:" practitioner"@33 (w=14.00) +4 more |
| 9 | `get_upstream_features` | L4:F11037@33, k=5 | Emb:" practitioner"@33 (w=6.50) +4 more |
| 10 | `inspect_feature` | L2, F2589 | " words related to medical professionals and medical specialties" |
| 11 | `get_upstream_features` | L1:F1494@33, k=5 | Emb:" nurse"@32 (w=8.69) +4 more |
| 12 | `inspect_feature` | L0, F6337 | "the word "dig" in different contexts." |
| 13 | `inspect_feature` | L0, F8854 | " the word "nurse" as well as some pronouns" |
| 14 | `inspect_feature` | L3, F5611 | " the word "practice" in the context of medicine, law, or religious rit" |

**Findings:** This circuit traces L6:F15267 at position 33 (Cedars Sinai context). The feature encodes "words in the document referring to the profession of nursing" - NOT a gender marker or medical location indicator. It's specifically about nursing profession detection.

The circuit shows a clear pathway from raw input tokens to nursing profession detection:
1. Raw tokens " nurse" (pos 32) and " practitioner"…

</details>

<details>
<summary><b>SA-3</b> — tool trace (14 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L18, F13596 | " text about the role, skills and leadership of nurse managers" |
| 2 | `get_upstream_features` | L18:F13596@18, k=5 | Emb:" Nursing"@18 (w=42.75) +4 more |
| 3 | `inspect_feature` | L6, F15267 | " words in the document referring to the profession of nursing" |
| 4 | `inspect_feature` | L14, F3985 | "terms related to management, leadership, medicine, studies, and resear" |
| 5 | `inspect_feature` | L3, F15901 | " mentions of nurses, nursing, and nurse management" |
| 6 | `get_upstream_features` | L6:F15267@18, k=5 | Emb:" Nursing"@18 (w=17.38) +4 more |
| 7 | `inspect_feature` | L4, F11037 | " words related to counseling, therapy, social work, and academic degre" |
| 8 | `get_upstream_features` | L4:F11037@18, k=5 | Emb:" Nursing"@18 (w=10.31) +4 more |
| 9 | `get_upstream_features` | L3:F15901@18, k=5 | Emb:" Nursing"@18 (w=15.19) +4 more |
| 10 | `get_upstream_features` | L14:F3985@18, k=5 | Emb:" Nursing"@18 (w=11.62) +4 more |
| 11 | `inspect_feature` | L8, F16339 | " text discussing hospital infections and bacteria" |
| 12 | `get_upstream_features` | L2:F10852@18, k=5 | Emb:" Nursing"@18 (w=11.62) +4 more |
| 13 | `inspect_feature` | L1, F10429 | " words related to academic programs" |
| 14 | `get_upstream_features` | L2:F9995@18, k=5 | Emb:" Nursing"@18 (w=5.41) +4 more |

**Findings:** The feature L18:F13596 encodes "text about the role, skills and leadership of nurse managers." The tracing reveals that this feature is strongly driven by the token embedding " Nursing" at position 18 (edge weight 42.75). The circuit shows multiple pathways: 1) Direct from " Nursing" embedding, 2) Through layer 6 feature that detects "words in the document referring to the profession of nursing", …

</details>

<details>
<summary><b>SA-4</b> — tool trace (16 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L7, F3979 | " words related to nursing and healthcare" |
| 2 | `get_upstream_features` | L7:F3979@33, k=5 | L6:F15267 (w=8.12) +4 more |
| 3 | `inspect_feature` | L6, F15267 | " words in the document referring to the profession of nursing" |
| 4 | `inspect_feature` | L5, F1275 | "words related to healthcare professionals and medical fields" |
| 5 | `inspect_feature` | L1, F1494 | " words related to medical practices and studies." |
| 6 | `get_upstream_features` | L6:F15267@33, k=5 | Emb:" nurse"@32 (w=5.66) +4 more |
| 7 | `inspect_feature` | L4, F11037 | " words related to counseling, therapy, social work, and academic degre" |
| 8 | `get_upstream_features` | L5:F1275@33, k=5 | L4:F9036 (w=1.70) +4 more |
| 9 | `inspect_feature` | L4, F9036 | " words and abbreviations associated with healthcare." |
| 10 | `get_upstream_features` | L4:F11037@33, k=5 | Emb:" practitioner"@33 (w=6.50) +4 more |
| 11 | `get_upstream_features` | L4:F9036@33, k=5 | Emb:" practitioner"@33 (w=14.00) +4 more |
| 12 | `inspect_feature` | L2, F2589 | " words related to medical professionals and medical specialties" |
| 13 | `inspect_feature` | L3, F5611 | " the word "practice" in the context of medicine, law, or religious rit" |
| 14 | `get_upstream_features` | L1:F1494@33, k=5 | Emb:" nurse"@32 (w=8.69) +4 more |
| 15 | `inspect_feature` | L0, F6337 | "the word "dig" in different contexts." |
| 16 | `inspect_feature` | L0, F8854 | " the word "nurse" as well as some pronouns" |

**Findings:** The feature L7:F3979 encodes "words related to nursing and healthcare" and has a negative direct effect at position 33. Tracing upstream reveals a clear circuit that detects the phrase "nurse practitioner" from the input text. The strongest upstream signals come from:

1. Direct embedding connections to tokens "nurse" (position 32) and "practitioner" (position 33)
2. Layer 6 feature F15267 that de…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L0:F5038@2, k=5 → Emb:" graduated"@2 (w=22.25) +4 more |
| 2 | `get_upstream_features` | L0:F6270@6, k=5 → Emb:" University"@6 (w=22.38) +4 more |
| 3 | `inspect_feature` ×4 | L18:13596, L14:3985, L6:15267, L4:9036 |

### Build

`build_circuit` → 14 nodes, 21 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m2.7 | 24,242 | 4,198 | 60,450 | 0 | $0.0141 | — | — |
| SA-2 | deepseek/deepseek-v3.2 | 92,715 | 3,894 | 7,552 | 0 | $0.0258 | ✅ 9F/12E | Trace this feature upstream. What does L6:F15267 encode? Wha… |
| SA-3 | deepseek/deepseek-v3.2 | 82,957 | 4,018 | 15,296 | 0 | $0.0235 | ✅ 9F/19E | Trace this feature upstream. L18:F13596 has high activation … |
| SA-4 | deepseek/deepseek-v3.2 | 113,086 | 4,867 | 6,976 | 0 | $0.0314 | ✅ 10F/30E | Trace this feature upstream. L7:F3979 has negative direct ef… |
| SA-1 | deepseek/deepseek-v3.2 | 162,309 | 5,649 | 51,968 | 0 | $0.0457 | ✅ 14F/23E | Trace this feature upstream. What does L14:F3985 encode? Wha… |
| **Total** | | **475,309** | **22,626** | **142,242** | **0** | **$0.1405** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 5m 35s