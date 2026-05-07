# Circuit Oracle Report
**Date:** 2026-04-06 09:17:30 UTC | **Orchestrator:** minimax/minimax-m2.7 | **Subagent:** deepseek/deepseek-v3.2

## Input

**Prompt:** "Dataset: bib_nurse_professor-pos_pos_5 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "('The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession.',)"

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification is primarily driven by genuine profession indicators (nursing/medical terminology) rather than spurious gender markers, though a minor spurious signal exists from a proper noun detector that connects to the female name "Melissa" and exhibits female-name suppression patterns.

**Confidence:** 7/10

**Reasoning:**

The attribution circuit reveals that the classification is overwhelmingly driven by **genuine profession-specific features**:

1. **Primary drivers (genuine profession indicators):**
   - **L14:F3985** (direct_effect=0.1089) - "terms related to management, leadership, medicine, studies, and research" promoting "patients", "Medical", "clinical"
   - **L6:F15267** (direct_effect=0.064) - "words in the document referring to the profession of nursing" with the strongest upstream connection (weight=20.5) directly from the "nurse" token embedding
   - **L4:F4665** (direct_effect=0.0635) - "medical environments, treatments, personnel, and facilities" promoting "hospital", "hospitals"
   - **L3:F9008** (frac=0.007) - "words related to childbirth or birth" promoting "birth", "born"
   - **L4:F13803** (frac=0.014) - "obstetrics and gynecology" promoting "pregnancy", "postpartum"

2. **Signal flow:** The circuit flows from lexical tokens ("nurse", "Labor", "Delivery") → medical sub-domain detectors (birth terms, anesthetics, OB/GYN) → medical environment/facility features → nursing profession detector → medical management terms → output.

3. **Minor spurious signal (potential concern):**
   - **L0:F7532** (direct_effect=0.0608) - "proper nouns" detector directly connected to "Melissa" at position 5 (edge_weight=21.25)
   - This feature exhibits **female-name suppression patterns**: suppressed tokens include "Manuela", "Karla", "Kayla", "Mónica", "Valeria", "Rhonda", "Maureen", "Marlene"
   - Top activating examples include female names: "Doreen", "Mónica", "Raquel"

4. **Why the concern is partially valid but minor:**
   - The Melissa name detector does contribute positively (0.0608) but its effect is **44% smaller** than the primary medical management detector (0.1089)
   - The name detector is NOT feeding into the medical detection circuit (upstream connections are from "Labor" and medical features, not names)
   - All profession-specific features have low frac_nonzero (0.005-0.066), indicating high specificity for medical contexts rather than generic gender patterns
   - The name feature appears to be an **indirect, minor spurious correlation** rather than the primary driver

**Conclusion:** The probe primarily uses genuine nursing/medical profession indicators with a minor spurious contribution from a name detector that may capture female-name associations. The gender-related signal exists but is weak compared to legitimate profession-specific features.

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L14:3985 de=0.109 |

### Dispatch: 7 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L14:F3985@11` | ✅ reported | 8 | 9 | Trace L14:F3985 (strongest positive driver) upstream to understand what it encod… |
| SA-2 | `L6:F15267@12` | ✅ reported | 12 | 13 | Trace L6:F15267 (strong positive driver at nurse position) upstream to understan… |
| SA-3 | `L0:F8444@2` | ✅ reported | 1 | 2 | Trace L0:F8444 (strong negative effect at position 2, "Melissa") upstream. This … |
| SA-4 | `L0:F9911@3` | ✅ reported | 2 | 5 | Trace L0:F9911 (positive driver at position 3, "worked") upstream to see if this… |
| SA-5 | `L7:F210@12` | ✅ reported | 10 | 11 | Trace L7:F210 (positive driver at nurse position) upstream. Investigate if this … |
| SA-6 | `L0:F7532@5` | ✅ reported | 1 | 1 | Trace L0:F7532 (positive driver at position 5, "as") upstream. Position 5 is "as… |
| SA-7 | `L0:F6515@27` | ✅ reported | 1 | 2 | Trace L0:F6515 (negative driver at position 27, "midwife") upstream. This positi… |

<details>
<summary><b>SA-1</b> — tool trace (15 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L14, F3985 | "terms related to management, leadership, medicine, studies, and resear" |
| 2 | `get_upstream_features` | L14:F3985@11, k=5 | L6:F4490 (w=2.94) +4 more |
| 3 | `inspect_feature` | L6, F4490 | " proper nouns corresponding to locations, organizations, medical roles" |
| 4 | `inspect_feature` | L4, F4665 | " words and phrases related to medical environments, treatments, person" |
| 5 | `inspect_feature` | L6, F9980 | " words and abbreviations associated with pediatric gastroenterology an" |
| 6 | `get_upstream_features` | L6:F4490@11, k=5 | L4:F4665 (w=3.91) +4 more |
| 7 | `get_upstream_features` | L4:F4665@11, k=5 | L3:F10198 (w=3.44) +4 more |
| 8 | `inspect_feature` | L3, F10198 | " words related to anesthetics and medical procedures" |
| 9 | `get_upstream_features` | L3:F10198@11, k=5 | Emb:" Delivery"@11 (w=7.59) +4 more |
| 10 | `inspect_feature` | L3, F9008 | " words related to childbirth or birth in general, including in animals" |
| 11 | `get_upstream_features` | L3:F9008@11, k=5 | Emb:" Delivery"@11 (w=11.25) +4 more |
| 12 | `get_upstream_features` | L6:F9980@11, k=5 | L4:F4665 (w=2.80) +4 more |
| 13 | `inspect_feature` | L5, F15022 | " mentions of obstetricians and gynecologists" |
| 14 | `get_upstream_features` | L5:F15022@11, k=5 | L4:F4665 (w=2.56) +4 more |
| 15 | `inspect_feature` | L4, F13803 | " terms related to obstetrics and gynecology" |

**Findings:** Tracing L14:F3985 upstream reveals a circuit that detects medical/obstetric terms. The starting feature L14:F3985 encodes "terms related to management, leadership, medicine, studies, and research" and fires on "nurse" in context of "nurse manager". 

Key findings:
1. The circuit originates from input tokens "Labor" (pos 9), "and" (pos 10), "Delivery" (pos 11) - the phrase "Labor and Delivery".
2. …

</details>

<details>
<summary><b>SA-2</b> — tool trace (15 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F15267 | " words in the document referring to the profession of nursing" |
| 2 | `get_upstream_features` | L6:F15267@12, k=5 | Emb:" nurse"@12 (w=20.50) +4 more |
| 3 | `inspect_feature` | L3, F15901 | " mentions of nurses, nursing, and nurse management" |
| 4 | `inspect_feature` | L5, F7539 | " words related to medical professionals performing actions on a patien" |
| 5 | `get_upstream_features` | L3:F15901@12, k=5 | Emb:" nurse"@12 (w=15.88) +4 more |
| 6 | `inspect_feature` | L5, F12279 | " terms relating to jobs and education" |
| 7 | `get_upstream_features` | L2:F15437@12, k=5 | Emb:" nurse"@12 (w=22.38) +4 more |
| 8 | `inspect_feature` | L0, F10920 | " the word "nurse"" |
| 9 | `inspect_feature` | L0, F8560 | " mentions of software licenses and warranties" |
| 10 | `get_upstream_features` | L6:F15267@12, k=10 | Emb:" nurse"@12 (w=20.50) +9 more |
| 11 | `inspect_feature` | L4, F11037 | " words related to counseling, therapy, social work, and academic degre" |
| 12 | `inspect_feature` | L4, F8751 | " cell types in the brain, especially glial cells and neurons, and rela" |
| 13 | `inspect_feature` | L2, F12997 | "the word "competition"" |
| 14 | `inspect_feature` | L0, F15074 | " words and phrases related to nurses, nursing, and nurse management" |
| 15 | `inspect_feature` | L0, F8854 | " the word "nurse" as well as some pronouns" |

**Findings:** The circuit analysis reveals that L6:F15267 is a genuine nurse/midwife detector, NOT a gender marker. Key findings:

1. **Direct lexical detection**: The strongest connection (weight 20.5) is directly from the token embedding for " nurse" at position 12. This is the primary driver.

2. **Early nurse detectors**: Multiple early features (L0:F10920, L0:F15074, L0:F8854) specifically detect the word …

</details>

<details>
<summary><b>SA-3</b> — tool trace (2 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F8444 | "the word "to"" |
| 2 | `get_upstream_features` | L0:F8444@2, k=5 | Emb:" to"@2 (w=39.50) +4 more |

**Findings:** Tracing L0:F8444 at position 2 revealed it's a feature that detects the word \"to\" with low sparsity (0.01705). The circuit shows it's directly and strongly connected (weight 39.5) to the embedding of the token \" to\" at position 2, indicating this feature fires specifically when the word \"to\" appears at that position. The promoted tokens show unusual 's' to 'f' substitutions (e.g., \"myfelf\"…

</details>

<details>
<summary><b>SA-4</b> — tool trace (5 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F9911 | " the word "that"" |
| 2 | `get_upstream_features` | L0:F9911@3, k=5 | Emb:" that"@3 (w=15.62) +4 more |
| 3 | `get_top_features` | token="worked", k=10 | ❌ Token 'worked' not found in top logits. Available: [''] |
| 4 | `get_top_logits` | k=5 | "" (100%) |
| 5 | `inspect_feature` | L0, F424 | " words and phrases related to scientific research, especially experime" |

**Findings:** The tracing from L0:F9911 at position 3 revealed that this feature is simply a word detector for \"that\" rather than being related to the verb \"worked\" as initially expected. The circuit shows strong direct connection from the token embedding of \" that\" at position 3 (edge_weight: 15.625) with weaker contributions from surrounding tokens (\" to\", \"Prior\", \"<bos>\"). The feature has low fr…

</details>

<details>
<summary><b>SA-5</b> — tool trace (15 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L7, F210 | " words and names associated with the Asante Healthcare system" |
| 2 | `get_upstream_features` | L7:F210@12, k=5 | Emb:" nurse"@12 (w=9.19) +4 more |
| 3 | `inspect_feature` | L6, F15267 | " words in the document referring to the profession of nursing" |
| 4 | `inspect_feature` | L4, F4665 | " words and phrases related to medical environments, treatments, person" |
| 5 | `get_upstream_features` | L6:F15267@12, k=5 | Emb:" nurse"@12 (w=20.50) +4 more |
| 6 | `inspect_feature` | L3, F15901 | " mentions of nurses, nursing, and nurse management" |
| 7 | `inspect_feature` | L5, F12279 | " terms relating to jobs and education" |
| 8 | `get_upstream_features` | L3:F15901@12, k=5 | Emb:" nurse"@12 (w=15.88) +4 more |
| 9 | `inspect_feature` | L2, F15437 | " words related to nurses and sound" |
| 10 | `get_upstream_features` | L4:F4665@11, k=5 | L3:F10198 (w=3.44) +4 more |
| 11 | `inspect_feature` | L3, F10198 | " words related to anesthetics and medical procedures" |
| 12 | `inspect_feature` | L0, F8854 | " the word "nurse" as well as some pronouns" |
| 13 | `get_upstream_features` | L0:F8854@12, k=5 | Emb:" nurse"@12 (w=24.38) +4 more |
| 14 | `inspect_feature` | L1, F8848 | "the word "register", possibly in a code context" |
| 15 | `inspect_feature` | L5, F7539 | " words related to medical professionals performing actions on a patien" |

**Findings:** Traced L7:F210 (Asante Healthcare system feature) upstream to investigate gender bias. Found the circuit primarily consists of:

1. DIRECT TOKEN EMBEDDING CONNECTIONS: The strongest connections (weights 9.1875, 20.5, 24.375) come directly from the " nurse" token embedding at position 12.

2. MEDICAL/NURSING FEATURES: Multiple features detect nursing/medical terminology:
   - L6:F15267: "words in t…

</details>

<details>
<summary><b>SA-6</b> — tool trace (3 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F7532 | " proper nouns" |
| 2 | `get_upstream_features` | L0:F7532@5, k=5 | Emb:" Melissa"@5 (w=21.25) +4 more |
| 3 | `inspect_feature` | L0, F7532 | " proper nouns" |

**Findings:** The tracing reveals that L0:F7532 at position 5 is a "proper nouns" detector that primarily activates on the input token "Melissa" (not "as" as initially suggested). The feature has gender-related suppression patterns - it suppresses many female names (Manuela, Karla, Kayla, etc.) while promoting more general words. The circuit is simple: the feature at layer 0 is directly driven by the embedding …

</details>

<details>
<summary><b>SA-7</b> — tool trace (3 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F6515 | " the year 199X or 200X." |
| 2 | `get_upstream_features` | L0:F6515@27, k=5 | Emb:"1"@26 (w=29.00) +4 more |
| 3 | `get_upstream_features` | L0:F6515@27, k=10 | Emb:"1"@26 (w=29.00) +9 more |

**Findings:** Tracing L0:F6515 at position 27 revealed that this feature detects year patterns (199X or 200X). The strongest upstream connections are from token embeddings "1" at position 26 (weight 29.0) and "9" at position 27 (weight 8.375), suggesting the input contains a year like "199..." at positions 26-27. Other contextual embeddings include "Melissa" (pos 5, female name) and "nurse" (pos 12, traditional…

</details>

### Re-dispatch (round 2): 1 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-8 | `L4:F4665@11` | ❌ error | — | — | Check if there are any downstream connections from proper noun or name-related f… |

<details>
<summary><b>SA-8</b> — tool trace (15 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F4665 | " words and phrases related to medical environments, treatments, person" |
| 2 | `get_upstream_features` | L4:F4665@11, k=5 | L3:F10198 (w=3.44) +4 more |
| 3 | `inspect_feature` | L3, F10198 | " words related to anesthetics and medical procedures" |
| 4 | `inspect_feature` | L3, F9008 | " words related to childbirth or birth in general, including in animals" |
| 5 | `inspect_feature` | L1, F10791 | "the word "delivery"" |
| 6 | `get_upstream_features` | L3:F10198@11, k=5 | Emb:" Delivery"@11 (w=7.59) +4 more |
| 7 | `get_upstream_features` | L3:F9008@11, k=5 | Emb:" Delivery"@11 (w=11.25) +4 more |
| 8 | `inspect_feature` | L2, F10127 | "the word "delivery" or "deliver"" |
| 9 | `inspect_feature` | L0, F3255 | " the word "and"" |
| 10 | `inspect_feature` | L1, F12174 | " words relating to ways things are conventionally done, potential prob" |
| 11 | `get_upstream_features` | L1:F10791@11, k=5 | Emb:" Delivery"@11 (w=17.88) +4 more |
| 12 | `inspect_feature` | L0, F2318 | " the word "never"." |
| 13 | `inspect_feature` | L2, F14771 | " the word "healthy" or the word "survive"" |
| 14 | `get_upstream_features` | L2:F14771@11, k=5 | Emb:" Delivery"@11 (w=20.12) +4 more |
| 15 | `inspect_feature` | L1, F9249 | " words related to scientific and technical language" |

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L0:F7532@5, k=3 → Emb:" Melissa"@5 (w=21.25) +2 more |
| 2 | `inspect_feature` | L0, F7532 → " proper nouns" |
| 3 | `get_upstream_features` | L4:F4665@11, k=10 → L3:F10198 (w=3.44) +9 more |

### Build

`build_circuit` → 13 nodes, 15 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m2.7 | 22,793 | 5,610 | 80,152 | 0 | $0.0160 | — | — |
| SA-3 | deepseek/deepseek-v3.2 | 9,243 | 1,124 | 0 | 0 | $0.0028 | ✅ 1F/2E | Trace L0:F8444 (strong negative effect at position 2, "Melis… |
| SA-4 | deepseek/deepseek-v3.2 | 21,629 | 1,519 | 0 | 0 | $0.0062 | ✅ 2F/5E | Trace L0:F9911 (positive driver at position 3, "worked") ups… |
| SA-1 | deepseek/deepseek-v3.2 | 94,634 | 4,145 | 21,568 | 0 | $0.0267 | ✅ 8F/9E | Trace L14:F3985 (strongest positive driver) upstream to unde… |
| SA-2 | deepseek/deepseek-v3.2 | 124,886 | 4,742 | 2,368 | 0 | $0.0343 | ✅ 12F/13E | Trace L6:F15267 (strong positive driver at nurse position) u… |
| SA-6 | deepseek/deepseek-v3.2 | 14,030 | 1,019 | 0 | 0 | $0.0040 | ✅ 1F/1E | Trace L0:F7532 (positive driver at position 5, "as") upstrea… |
| SA-7 | deepseek/deepseek-v3.2 | 13,584 | 1,676 | 0 | 0 | $0.0042 | ✅ 1F/2E | Trace L0:F6515 (negative driver at position 27, "midwife") u… |
| SA-5 | deepseek/deepseek-v3.2 | 97,232 | 4,409 | 19,520 | 0 | $0.0275 | ✅ 10F/11E | Trace L7:F210 (positive driver at nurse position) upstream. … |
| SA-8 | deepseek/deepseek-v3.2 | 106,072 | 1,829 | 0 | 0 | $0.0283 | ❌ error | Check if there are any downstream connections from proper no… |
| **Total** | | **504,103** | **26,073** | **123,608** | **0** | **$0.1500** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 9m 58s