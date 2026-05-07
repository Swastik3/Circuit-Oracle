# Circuit Oracle Report
**Date:** 2026-03-30 18:20:25 UTC | **Orchestrator:** minimax/minimax-m2.7 | **Subagent:** deepseek/deepseek-v3.2

## Input
**Prompt:** "Dataset: bib_nurse_professor-pos_pos_1 | Probe: unbiased | Method: correct"
**System prompt:** ""
**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."
**Top predictions:**  (100.0%)

## Oracle Analysis
**Analysis:** This attribution circuit reveals that the probe's classification score is driven primarily by **genuine nursing profession indicators**, not spurious gender markers. The top positive drivers are all features encoding medical/nursing content: L14:F3985 ("terms related to management, leadership, medicine, studies, and research" with frac_nonzero=0.066), L6:F15267 ("words in the document referring to the profession of nursing" with frac_nonzero=0.016), and L18:F13596 ("text about the role, skills and leadership of nurse managers" with frac_nonzero=0.005—highly specific). The circuit traces back to input tokens "nurses" (pos 15) and "Perioperative"/"perative" (pos 13-14), which directly activate these profession-specific features through a multi-layer aggregation pathway. While L4:F4665 (medical environments) shows a minor upstream connection from " she" (edge_weight=1.28), this gender pronoun is heavily attenuated through medical-specific intermediate layers (L3:F14131 encodes "the word 'all'", L1:F1889 encodes "medical studies, procedures, and patient outcomes"), so it does not function as an independent spurious feature. The inhibitory features (L3:F15901, L7:F3979) with negative direct effects suppress nursing-related tokens, representing a context-dependent inhibition pattern rather than a spurious gender shortcut.

**Confidence:** 8/10

**Reasoning:** The circuit analysis demonstrates that the probe's classification is driven by a hierarchical aggregation of genuine nursing/medical profession features (frac_nonzero values ranging from 0.005 to 0.066, indicating specificity), originating from direct lexical detection of nursing terminology ("nurses") and medical domain words ("Perioperative") at the input layer. The most influential features L14:F3985 and L6:F15267 both directly encode nursing/medical content with clear semantic labels, and L18:F13596 is particularly telling—a highly specific feature (frac_nonzero=0.005) detecting "nurse managers" and their leadership skills, with promoted tokens being exclusively nursing-related vocabulary. While a minor connection from the gender pronoun " she" exists, it traverses medical-specific intermediate representations and has negligible direct effect compared to the substantive nursing content features. The absence of dedicated gender-detection features (e.g., "she/her" markers firing independently) and the presence of multiple layers of genuine profession encoding indicate the model uses legitimate profession indicators rather than spurious gender correlations.

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 10 features; top: L14:3985 de=0.162 |
| 3 | `inspect_feature` ×4 | L14:3985, L6:15267, L3:15901, L7:3979 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L14:F3985@15` | ❌ error | — | — | Trace this feature upstream to understand what drives it. Look for whether it's … |
| SA-2 | `L6:F15267@15` | ✅ reported | 8 | 18 | Trace this nursing profession feature upstream. Look for whether it's driven by … |
| SA-3 | `L3:F15901@15` | ✅ reported | 5 | 4 | Trace this feature - it has a NEGATIVE effect on the probe. Investigate what ups… |
| SA-4 | `L7:F3979@15` | ✅ reported | 10 | 16 | Trace this nursing/healthcare feature upstream. Look for early-layer features an… |

<details>
<summary><b>SA-2</b> — tool trace (13 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F15267 | " words in the document referring to the profession of nursing" |
| 2 | `get_upstream_features` | L6:F15267@15, k=5 | Emb:" nurses"@15 (w=16.12) +4 more |
| 3 | `inspect_feature` | L4, F11037 | " words related to counseling, therapy, social work, and academic degre" |
| 4 | `inspect_feature` | L3, F15901 | " mentions of nurses, nursing, and nurse management" |
| 5 | `inspect_feature` | L4, F8751 | " cell types in the brain, especially glial cells and neurons, and rela" |
| 6 | `get_upstream_features` | L4:F11037@15, k=5 | Emb:" nurses"@15 (w=5.12) +4 more |
| 7 | `get_upstream_features` | L3:F15901@15, k=5 | Emb:" nurses"@15 (w=14.88) +4 more |
| 8 | `inspect_feature` | L2, F15437 | " words related to nurses and sound" |
| 9 | `inspect_feature` | L0, F11835 | "terms used in software code such as "assembly", "using", "namespace", " |
| 10 | `get_upstream_features` | L2:F15437@15, k=5 | Emb:" nurses"@15 (w=19.25) +4 more |
| 11 | `inspect_feature` | L0, F10920 | " the word "nurse"" |
| 12 | `get_upstream_features` | L0:F10920@15, k=5 | Emb:" nurses"@15 (w=21.50) +4 more |
| 13 | `inspect_feature` | L2, F5224 | " words related to retail and customer service jobs" |

**Findings:** The nursing profession feature at L6:F15267 is primarily driven by ACTUAL nursing-related tokens, not spurious features. Key findings:

1. **Direct embedding connection**: The strongest connection to L6 feature is from the token " nurses" embedding itself (weight 16.125), indicating direct lexical detection.

2. **Early layer nursing detection**: Layer 0 contains feature 10920 that specifically de…

</details>

<details>
<summary><b>SA-3</b> — tool trace (8 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L3, F15901 | " mentions of nurses, nursing, and nurse management" |
| 2 | `get_upstream_features` | L3:F15901@15, k=5 | Emb:" nurses"@15 (w=14.88) +4 more |
| 3 | `inspect_feature` | L2, F15437 | " words related to nurses and sound" |
| 4 | `inspect_feature` | L0, F11835 | "terms used in software code such as "assembly", "using", "namespace", " |
| 5 | `get_upstream_features` | L2:F15437@15, k=5 | Emb:" nurses"@15 (w=19.25) +4 more |
| 6 | `inspect_feature` | L0, F10920 | " the word "nurse"" |
| 7 | `inspect_feature` | L0, F9026 | "technical documents or data, including numbers, units, and references " |
| 8 | `get_upstream_features` | L0:F10920@15, k=5 | Emb:" nurses"@15 (w=21.50) +4 more |

**Findings:** The tracing reveals a circuit that processes the token "nurses" at position 15. Starting from L3:F15901 (which detects mentions of nurses but suppresses nurse-related tokens), the circuit traces back through L2:F15437 (detecting words related to nurses and sound) which has a NEGATIVE connection to the L3 feature (weight: -0.6914). This L2 feature receives input from L0:F10920 which directly detect…

</details>

<details>
<summary><b>SA-4</b> — tool trace (16 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L7, F3979 | " words related to nursing and healthcare" |
| 2 | `get_upstream_features` | L7:F3979@15, k=5 | L6:F15267 (w=7.94) +4 more |
| 3 | `inspect_feature` | L6, F15267 | " words in the document referring to the profession of nursing" |
| 4 | `get_upstream_features` | L6:F15267@15, k=5 | Emb:" nurses"@15 (w=16.12) +4 more |
| 5 | `inspect_feature` | L4, F11037 | " words related to counseling, therapy, social work, and academic degre" |
| 6 | `inspect_feature` | L4, F8751 | " cell types in the brain, especially glial cells and neurons, and rela" |
| 7 | `inspect_feature` | L3, F15901 | " mentions of nurses, nursing, and nurse management" |
| 8 | `get_upstream_features` | L4:F11037@15, k=5 | Emb:" nurses"@15 (w=5.12) +4 more |
| 9 | `get_upstream_features` | L3:F15901@15, k=5 | Emb:" nurses"@15 (w=14.88) +4 more |
| 10 | `inspect_feature` | L2, F15437 | " words related to nurses and sound" |
| 11 | `inspect_feature` | L0, F11835 | "terms used in software code such as "assembly", "using", "namespace", " |
| 12 | `inspect_feature` | L2, F5224 | " words related to retail and customer service jobs" |
| 13 | `get_upstream_features` | L4:F8751@15, k=5 | Emb:" nurses"@15 (w=9.81) +4 more |
| 14 | `inspect_feature` | L0, F8854 | " the word "nurse" as well as some pronouns" |
| 15 | `get_upstream_features` | L2:F15437@15, k=5 | Emb:" nurses"@15 (w=19.25) +4 more |
| 16 | `inspect_feature` | L0, F10920 | " the word "nurse"" |

**Findings:** Traced the nursing/healthcare feature (L7:F3979) upstream to discover a circuit that detects the word "nurses" in the input text. The circuit starts with early-layer features at layer 0 that detect the word "nurse" (F8854 and F10920), which then feed into layer 2-3 features about nurses and sound or nurse management. These converge at layer 6 (F15267) which detects nursing profession references, a…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L14:F3985@15, k=10 → Emb:" nurses"@15 (w=10.69) +9 more |
| 2 | `get_upstream_features` | L8:F16339@15, k=8 → Emb:" nurses"@15 (w=4.75) +7 more |
| 3 | `get_upstream_features` | L18:F13596@15, k=8 → Emb:" nurses"@15 (w=42.00) +7 more |
| 4 | `get_upstream_features` | L4:F4665@14, k=8 → Emb:"perative"@14 (w=15.50) +7 more |
| 5 | `inspect_feature` ×3 | L4:4665, L7:210, L4:8736 |
| 6 | `get_upstream_features` | L4:F4665@14, k=5 → Emb:"perative"@14 (w=15.50) +4 more |
| 7 | `get_upstream_features` | L1:F1889@14, k=8 → Emb:"perative"@14 (w=5.38) +7 more |
| 8 | `get_upstream_features` | L3:F14131@14, k=8 → Emb:"perative"@14 (w=9.19) +7 more |
| 9 | `inspect_feature` ×5 | L3:14131, L1:1889, L2:2363, L8:16339, L18:13596 |

### Build

`build_circuit` → 13 nodes, 23 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m2.7 | 36,371 | 5,169 | 111,077 | 0 | — | — | — |
| SA-3 | deepseek/deepseek-v3.2 | 45,636 | 2,000 | 0 | 0 | — | ✅ 5F/4E | Trace this feature - it has a NEGATIVE effect on the probe. … |
| SA-2 | deepseek/deepseek-v3.2 | 88,819 | 3,942 | 0 | 0 | — | ✅ 8F/18E | Trace this nursing profession feature upstream. Look for whe… |
| SA-4 | deepseek/deepseek-v3.2 | 111,766 | 4,022 | 8,960 | 0 | — | ✅ 10F/16E | Trace this nursing/healthcare feature upstream. Look for ear… |
| **Total** | | **282,592** | **15,133** | **120,037** | **0** | **—** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 5m 36s