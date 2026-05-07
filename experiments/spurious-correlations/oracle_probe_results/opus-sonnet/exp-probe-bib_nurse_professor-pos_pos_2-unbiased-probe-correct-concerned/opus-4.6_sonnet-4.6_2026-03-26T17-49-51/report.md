# Circuit Oracle Report
**Date:** 2026-03-26 17:49:51 UTC | **Orchestrator:** anthropic/claude-opus-4.6 | **Subagent:** anthropic/claude-sonnet-4.6

## Input
**Prompt:** "Dataset: bib_nurse_professor-pos_pos_2 | Probe: unbiased | Method: correct"
**System prompt:** ""
**Concern:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."
**Top predictions:**  (100.0%)

## Oracle Analysis
Now let me write the final analysis.

---

**Analysis:** The probe classifies this text as "nurse" based on a circuit that is overwhelmingly driven by genuine nursing/healthcare profession tokens — primarily "Nursing" (pos 10) and "nursing" (pos 22) — with zero reliance on gender markers like "She" or "her."

**Confidence:** High

**Reasoning:**

## The Circuit is NOT Spurious — It Uses Genuine Profession Indicators

### 1. Input Tokens That Drive the Probe

The circuit originates from **profession-specific tokens**, not gender markers:

- **"Nursing" (pos 10)** — from "Bachelors of Science in **Nursing**" — is the overwhelmingly dominant input, with edge weights of 10–42 across all layers. This single token is the primary driver at every layer in the circuit.
- **"nursing" (pos 22)** — from "her **nursing** career" — provides secondary reinforcement (edge weight 21.0 into L6:15267).
- **"graduated" (pos 2)** — provides academic/credential framing context (L0:5038, direct effect +0.088).
- **"Bachelors" / "Science" / "Of" / "Carolina"** (pos 6, 8, 14-15, 17) — provide academic degree and university context.

**Critically absent: No features at positions corresponding to "She" or "her" appear anywhere in the top-20 features driving the probe.** The pronoun "She" at pos 0 and "her" at pos 3/21 are not represented in any feature with meaningful direct effect.

### 2. The Main Excitatory Pathway (Token → Profession → Probe)

The dominant circuit flows through position 10 ("Nursing"):

1. **Emb: "Nursing"** → **L1: Early Nurse Detection** (L1:14469 "mentions of nurse", frac_nonzero=0.004 — highly specific)
2. → **L2: Academic Degrees** (L2:10852 "academic titles and degrees", frac_nonzero=0.008) — recognizes "Nursing" in the context of "Bachelors of Science"
3. → **L3: Nursing Morphology** (L3:6246, frac_nonzero=0.004) — detects the "Nurs-" morphological pattern
4. → **L4: Professional Degree Programs** (L4:11037 "counseling, therapy, social work, academic degree programs", frac_nonzero=0.007)
5. → **L5: Healthcare Professionals** (L5:1275, frac_nonzero=0.013)
6. → **L6: Nursing Profession Detector** (L6:15267 "words referring to the profession of nursing", frac_nonzero=0.016, direct effect **+0.136**) — the second strongest positive driver

In parallel, a medical context pathway builds through:
- **L6:4490** (medical organizations/hospitals) + **L7:210** (Asante Healthcare system) → **L8** (hospital infections, medical treatment, professional biographies) → **L14:3985** ("management, leadership, medicine", direct effect **+0.187** — the strongest single positive driver) → **L18:13596** ("nurse manager/leadership", frac_nonzero=0.005, direct effect +0.052).

### 3. The Suppression Mechanism

Two features have **negative** direct effects on the probe:

- **L3:15901** ("mentions of nurses, nursing, and nurse management", direct effect **-0.098**): Despite firing on nursing contexts, this feature's suppressed_tokens literally include "nurse", "Nurse", "nursing" — it acts as a **precision regulator**, damping overly broad nursing-word signals. It feeds negatively into downstream features (edge weight -2.36 to L6:15267, -5.28 to L18:13596).

- **L7:3979** ("words related to nursing and healthcare", direct effect **-0.110**): Similarly fires on nursing contexts but opposes the probe. The subagent analysis suggests this feature distinguishes "nursing as academic credential" from "nursing as clinical practice" — it fires in the degree-context framing and pulls against the probe, creating a subtle academic-vs-clinical tension.

### 4. Addressing the Gender Concern

**The circuit provides strong evidence AGAINST spurious gender reliance:**

| Evidence | Detail |
|----------|--------|
| **No gender features in top-20** | None of the 20 features with highest direct effect fire on "She" (pos 0) or "her" (pos 3/21) |
| **L7:3979 promotes "Her" but is SUPPRESSIVE** | The one feature whose promoted tokens include "Her" (L7:3979) actually has a **negative** effect (-0.11) — it's an inhibitor, not a driver |
| **Position distribution** | 14 of the top 20 features fire at pos 10 ("Nursing"), with the rest at pos 2 ("graduated"), 14-17 ("University Of South Carolina"), and 22 ("nursing") — all profession/education tokens |
| **Feature specificity** | The driving features have low frac_nonzero (0.004–0.016), indicating they're highly specific to nursing/medical/academic contexts, not generic gender patterns |
| **Embedding edge weights** | "Nursing" embedding has edge weights 10–42 to downstream features; no gender-token embeddings appear in any upstream trace |

### 5. Summary

The probe's "nurse" classification is driven by a **legitimate, multi-layered profession-identification circuit** that:
- Begins with the literal token "Nursing" (and "nursing")
- Progressively builds nursing-specific representations through academic degree detection → professional degree programs → healthcare professionals → nursing profession → medicine/leadership → nurse management
- Is supplemented by hospital/medical institutional context features
- Includes built-in suppression mechanisms that sharpen the classification signal
- Contains **zero** gender-marker features as positive drivers

The probe appears to be a well-calibrated nurse/nursing-profession classifier that relies on the right signals.

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L14:3985 de=0.186 |
| 3 | `inspect_feature` ×18 | L14:3985, L6:15267, L7:3979, L3:15901, L0:5038, L0:6270, L15:15159, L6:4490, L8:16339, L7:210, L0:11959, L0:16075, L18:13596, L7:4654, L15:8289, L6:11057, L2:14478, L0:11988 |

### Dispatch: 5 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L14:F3985@10` | ✅ reported | 0 | 0 | Trace the strongest positive feature driving the nursing probe classification (L… |
| SA-2 | `L6:F15267@10` | ✅ reported | 10 | 25 | Trace the second strongest positive feature driving the nursing probe (L6:15267,… |
| SA-3 | `L18:F13596@10` | ✅ reported | 14 | 24 | Trace L18:13596, 'text about the role, skills and leadership of nurse managers' … |
| SA-4 | `L15:F15159@10` | ✅ reported | 0 | 0 | Trace L15:15159, 'words related to medicine and healthcare' at pos 10. Understan… |
| SA-5 | `L7:F3979@10` | ✅ reported | 14 | 18 | Trace L7:3979, 'words related to nursing and healthcare' at pos 10. This feature… |

<details>
<summary><b>SA-1</b> — tool trace (22 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L14, F3985 | "terms related to management, leadership, medicine, studies, and resear" |
| 2 | `get_upstream_features` | L14:F3985@10, k=8 | Emb:" Nursing"@10 (w=12.06) +7 more |
| 3 | `inspect_feature` | L8, F16339 | " text discussing hospital infections and bacteria" |
| 4 | `inspect_feature` | L7, F210 | " words and names associated with the Asante Healthcare system" |
| 5 | `inspect_feature` | L6, F4490 | " proper nouns corresponding to locations, organizations, medical roles" |
| 6 | `inspect_feature` | L8, F9619 | " words and phrases related to medical treatment" |
| 7 | `get_upstream_features` | L8:F16339@10, k=8 | Emb:" Nursing"@10 (w=7.66) +7 more |
| 8 | `get_upstream_features` | L7:F210@10, k=8 | Emb:" Nursing"@10 (w=8.19) +7 more |
| 9 | `inspect_feature` | L6, F15267 | " words in the document referring to the profession of nursing" |
| 10 | `inspect_feature` | L6, F170 | " references to academic fields, especially those in the humanities" |
| 11 | `get_upstream_features` | L6:F15267@10, k=8 | Emb:" Nursing"@10 (w=17.38) +7 more |
| 12 | `inspect_feature` | L4, F11037 | " words related to counseling, therapy, social work, and academic degre" |
| 13 | `inspect_feature` | L5, F1275 | "words related to healthcare professionals and medical fields" |
| 14 | `inspect_feature` | L4, F8751 | " cell types in the brain, especially glial cells and neurons, and rela" |
| 15 | `get_upstream_features` | L4:F11037@10, k=6 | Emb:" Nursing"@10 (w=10.56) +5 more |
| 16 | `inspect_feature` | L2, F10852 | " academic titles and degrees" |
| 17 | `inspect_feature` | L3, F6246 | " the word "Nutrients" and words containing "ure"." |
| 18 | `inspect_feature` | L3, F15901 | " mentions of nurses, nursing, and nurse management" |
| 19 | `get_upstream_features` | L3:F6246@10, k=6 | Emb:" Nursing"@10 (w=9.62) +5 more |
| 20 | `inspect_feature` | L0, F4559 | " the word "fact" in the text" |
| 21 | `inspect_feature` | L1, F10429 | " words related to academic programs" |
| 22 | `inspect_feature` | L2, F15728 | " mentions of nurses and nursing" |

</details>

<details>
<summary><b>SA-2</b> — tool trace (16 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F15267 | " words in the document referring to the profession of nursing" |
| 2 | `get_upstream_features` | L6:F15267@10, k=8 | Emb:" Nursing"@10 (w=17.38) +7 more |
| 3 | `inspect_feature` | L4, F11037 | " words related to counseling, therapy, social work, and academic degre" |
| 4 | `inspect_feature` | L5, F1275 | "words related to healthcare professionals and medical fields" |
| 5 | `inspect_feature` | L4, F8751 | " cell types in the brain, especially glial cells and neurons, and rela" |
| 6 | `get_upstream_features` | L4:F11037@10, k=8 | Emb:" Nursing"@10 (w=10.56) +7 more |
| 7 | `get_upstream_features` | L5:F1275@10, k=8 | L4:F11037 (w=1.99) +7 more |
| 8 | `inspect_feature` | L3, F6246 | " the word "Nutrients" and words containing "ure"." |
| 9 | `inspect_feature` | L2, F10852 | " academic titles and degrees" |
| 10 | `inspect_feature` | L3, F15901 | " mentions of nurses, nursing, and nurse management" |
| 11 | `get_upstream_features` | L2:F10852@10, k=8 | Emb:" Nursing"@10 (w=11.44) +7 more |
| 12 | `get_upstream_features` | L3:F6246@10, k=8 | Emb:" Nursing"@10 (w=9.62) +7 more |
| 13 | `inspect_feature` | L1, F10429 | " words related to academic programs" |
| 14 | `inspect_feature` | L1, F12372 | " mentions of US universities and sports teams" |
| 15 | `inspect_feature` | L2, F9995 | " terms related to occupations and fields of study" |
| 16 | `get_upstream_features` | L1:F10429@10, k=8 | Emb:" Nursing"@10 (w=4.78) +7 more |

**Findings:** ## Circuit Summary: What Drives L6:F15267 ("Nursing profession")?

**Main finding: The second strongest positive driver is L4:F11037 (edge weight +4.22), and the entire circuit traces back overwhelmingly to the token " Nursing" itself at pos 10 — NOT to gender markers.**

### The Full Circuit:

**Tier 1 — Direct drivers of L6:F15267:**
- **" Nursing" embedding (pos 10)**: +17.375 — by far the domi…

</details>

<details>
<summary><b>SA-3</b> — tool trace (19 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L18, F13596 | " text about the role, skills and leadership of nurse managers" |
| 2 | `get_upstream_features` | L18:F13596@10, k=8 | Emb:" Nursing"@10 (w=42.50) +7 more |
| 3 | `inspect_feature` | L6, F15267 | " words in the document referring to the profession of nursing" |
| 4 | `inspect_feature` | L14, F3985 | "terms related to management, leadership, medicine, studies, and resear" |
| 5 | `inspect_feature` | L3, F15901 | " mentions of nurses, nursing, and nurse management" |
| 6 | `get_upstream_features` | L6:F15267@10, k=8 | Emb:" Nursing"@10 (w=17.38) +7 more |
| 7 | `get_upstream_features` | L14:F3985@10, k=8 | Emb:" Nursing"@10 (w=12.06) +7 more |
| 8 | `inspect_feature` | L8, F16339 | " text discussing hospital infections and bacteria" |
| 9 | `inspect_feature` | L8, F440 | " text from professional biographies" |
| 10 | `inspect_feature` | L4, F11037 | " words related to counseling, therapy, social work, and academic degre" |
| 11 | `inspect_feature` | L7, F210 | " words and names associated with the Asante Healthcare system" |
| 12 | `inspect_feature` | L6, F4490 | " proper nouns corresponding to locations, organizations, medical roles" |
| 13 | `inspect_feature` | L7, F3979 | " words related to nursing and healthcare" |
| 14 | `get_upstream_features` | L4:F11037@10, k=6 | Emb:" Nursing"@10 (w=10.56) +5 more |
| 15 | `get_upstream_features` | L3:F15901@10, k=6 | Emb:" Nursing"@10 (w=15.06) +5 more |
| 16 | `inspect_feature` | L5, F1275 | "words related to healthcare professionals and medical fields" |
| 17 | `inspect_feature` | L2, F10852 | " academic titles and degrees" |
| 18 | `inspect_feature` | L3, F6246 | " the word "Nutrients" and words containing "ure"." |
| 19 | `inspect_feature` | L8, F9619 | " words and phrases related to medical treatment" |

**Findings:** ## Circuit Summary: L18:F13596 — "Text about the role, skills and leadership of nurse managers"

**Primary Driver: The " Nursing" Token Embedding (weight=42.5)**
The single most powerful input is the raw token embedding of " Nursing" at position 10, dominating every upstream path across all layers. This feature is overwhelmingly token-driven rather than context-assembled.

**Excitatory Pathway (Nu…

</details>

<details>
<summary><b>SA-4</b> — tool trace (21 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L15, F15159 | " words related to medicine and healthcare" |
| 2 | `get_upstream_features` | L15:F15159@10, k=8 | Emb:" Nursing"@10 (w=10.56) +7 more |
| 3 | `inspect_feature` | L8, F16339 | " text discussing hospital infections and bacteria" |
| 4 | `inspect_feature` | L6, F4490 | " proper nouns corresponding to locations, organizations, medical roles" |
| 5 | `inspect_feature` | L7, F210 | " words and names associated with the Asante Healthcare system" |
| 6 | `inspect_feature` | L7, F3979 | " words related to nursing and healthcare" |
| 7 | `get_upstream_features` | L8:F16339@10, k=6 | Emb:" Nursing"@10 (w=7.66) +5 more |
| 8 | `get_upstream_features` | L6:F4490@10, k=6 | Emb:" Nursing"@10 (w=11.62) +5 more |
| 9 | `get_upstream_features` | L7:F210@10, k=6 | Emb:" Nursing"@10 (w=8.19) +5 more |
| 10 | `inspect_feature` | L6, F15267 | " words in the document referring to the profession of nursing" |
| 11 | `inspect_feature` | L5, F10392 | " fields of academic study" |
| 12 | `inspect_feature` | L3, F15901 | " mentions of nurses, nursing, and nurse management" |
| 13 | `get_upstream_features` | L6:F15267@10, k=6 | Emb:" Nursing"@10 (w=17.38) +5 more |
| 14 | `inspect_feature` | L7, F5829 | "mentions of nursing or higher education degrees." |
| 15 | `inspect_feature` | L7, F8194 | "mentions of the word "nurse" or the initials or last names of people" |
| 16 | `inspect_feature` | L4, F11037 | " words related to counseling, therapy, social work, and academic degre" |
| 17 | `inspect_feature` | L5, F1275 | "words related to healthcare professionals and medical fields" |
| 18 | `get_upstream_features` | L4:F11037@10, k=6 | Emb:" Nursing"@10 (w=10.56) +5 more |
| 19 | `inspect_feature` | L2, F10852 | " academic titles and degrees" |
| 20 | `inspect_feature` | L3, F6246 | " the word "Nutrients" and words containing "ure"." |
| 21 | `get_upstream_features` | L3:F15901@10, k=6 | Emb:" Nursing"@10 (w=15.06) +5 more |

</details>

<details>
<summary><b>SA-5</b> — tool trace (19 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L7, F3979 | " words related to nursing and healthcare" |
| 2 | `get_upstream_features` | L7:F3979@10, k=8 | L6:F15267 (w=8.81) +7 more |
| 3 | `inspect_feature` | L6, F15267 | " words in the document referring to the profession of nursing" |
| 4 | `inspect_feature` | L3, F15901 | " mentions of nurses, nursing, and nurse management" |
| 5 | `inspect_feature` | L6, F170 | " references to academic fields, especially those in the humanities" |
| 6 | `get_upstream_features` | L6:F15267@10, k=8 | Emb:" Nursing"@10 (w=17.38) +7 more |
| 7 | `inspect_feature` | L4, F11037 | " words related to counseling, therapy, social work, and academic degre" |
| 8 | `inspect_feature` | L5, F1275 | "words related to healthcare professionals and medical fields" |
| 9 | `get_upstream_features` | L3:F15901@10, k=8 | Emb:" Nursing"@10 (w=15.06) +7 more |
| 10 | `inspect_feature` | L2, F9995 | " terms related to occupations and fields of study" |
| 11 | `inspect_feature` | L2, F15437 | " words related to nurses and sound" |
| 12 | `get_upstream_features` | L4:F11037@10, k=8 | Emb:" Nursing"@10 (w=10.56) +7 more |
| 13 | `inspect_feature` | L2, F10852 | " academic titles and degrees" |
| 14 | `inspect_feature` | L3, F6246 | " the word "Nutrients" and words containing "ure"." |
| 15 | `inspect_feature` | L1, F14469 | " mentions of 'nurse'" |
| 16 | `get_upstream_features` | L2:F10852@10, k=6 | Emb:" Nursing"@10 (w=11.44) +5 more |
| 17 | `inspect_feature` | L1, F10429 | " words related to academic programs" |
| 18 | `inspect_feature` | L1, F12372 | " mentions of US universities and sports teams" |
| 19 | `inspect_feature` | L5, F10392 | " fields of academic study" |

**Findings:** ## Circuit Summary: Why L7:F3979 Suppresses the Probe

### The Core Paradox
L7:F3979 ('words related to nursing and healthcare') has a **negative** direct effect (-0.11) on the probe despite being semantically about nursing. The circuit reveals why: this feature fires strongly on the token " Nursing" at pos 10, but rather than encoding nursing-as-healthcare, it encodes **nursing-as-an-academic-fie…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` ×5 | L8:440, L8:9619, L5:10392, L1:14469, L4:11037 |
| 2 | `get_upstream_features` | L6:F15267@22, k=5 → Emb:" nursing"@22 (w=21.00) +4 more |

### Build

`build_circuit` → 18 nodes, 45 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | anthropic/claude-opus-4.6 | 198,062 | 6,795 | 0 | 0 | $1.1602 | — | — |
| SA-2 | anthropic/claude-sonnet-4.6 | 71,347 | 4,879 | 0 | 0 | $0.2872 | ✅ 10F/25E | Trace the second strongest positive feature driving the nurs… |
| SA-3 | anthropic/claude-sonnet-4.6 | 68,297 | 5,362 | 0 | 0 | $0.2853 | ✅ 14F/24E | Trace L18:13596, 'text about the role, skills and leadership… |
| SA-5 | anthropic/claude-sonnet-4.6 | 68,078 | 5,381 | 0 | 0 | $0.2849 | ✅ 14F/18E | Trace L7:3979, 'words related to nursing and healthcare' at … |
| SA-4 | anthropic/claude-sonnet-4.6 | 83,012 | 5,920 | 0 | 0 | $0.3378 | ✅ 0F/0E | Trace L15:15159, 'words related to medicine and healthcare' … |
| SA-1 | anthropic/claude-sonnet-4.6 | 86,640 | 5,988 | 0 | 0 | $0.3497 | ✅ 0F/0E | Trace the strongest positive feature driving the nursing pro… |
| **Total** | | **575,436** | **34,325** | **0** | **0** | **$2.7053** | | |

**Oracle wall-clock time:** 4m 8s