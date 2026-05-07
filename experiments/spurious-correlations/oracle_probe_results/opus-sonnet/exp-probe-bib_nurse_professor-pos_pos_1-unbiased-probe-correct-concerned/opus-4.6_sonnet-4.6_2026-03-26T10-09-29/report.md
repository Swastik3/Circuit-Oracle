# Circuit Oracle Report
**Date:** 2026-03-26 10:09:29 UTC | **Orchestrator:** anthropic/claude-opus-4.6 | **Subagent:** anthropic/claude-sonnet-4.6

## Input
**Prompt:** "Dataset: bib_nurse_professor-pos_pos_1 | Probe: unbiased | Method: correct"
**System prompt:** ""
**Concern:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."
**Top predictions:**  (100.0%)

## Oracle Analysis
**Analysis:** The probe classifies this text as "nurse" using a circuit primarily driven by genuine nursing/healthcare profession indicators (the words "nurses" and "Perioperative"), but it also includes a spurious gender-based pathway from the pronoun "she" that has a modest negative effect on the classification score.

**Confidence:** High

**Reasoning:**

## Primary Mechanism: Genuine Nursing Profession Detection (Dominant)

The circuit is overwhelmingly driven by **two input tokens**: "nurses" (pos 15) and "perative" (pos 14, part of "Perioperative"). These anchor a deep, multi-layered cascade of healthcare-specific features:

1. **Token-level detection (L0-L1):** The "nurses" embedding fires L0:10920 ("the word 'nurse'", frac=0.006) and L1:14469 ("mentions of 'nurse'", frac=0.004) — both extremely selective nurse-word detectors.

2. **Medical environment enrichment (L4-L5):** L4:4665 ("medical environments, treatments, personnel, facilities", frac=0.012) activates on "perative" and promotes "hospital" tokens. L4:11037 ("counseling, therapy, social work", frac=0.007) and L5:1275 ("healthcare professionals", frac=0.013) further build medical context.

3. **Nursing profession specialization (L6):** L6:15267 ("words referring to the profession of nursing", frac=0.016) is the key nursing-specific feature, with top activating examples on "RN" and "DNP" tokens. Its direct effect on the probe is +0.157 at pos 15 and +0.084 at pos 14.

4. **Healthcare institutional context (L7-L8):** L7:210 ("Asante Healthcare system", frac=0.013) and L8:16339 ("hospital infections/bacteria", frac=0.023) build hospital/medical framing, feeding into the leadership features above.

5. **Medical leadership synthesis (L14):** L14:3985 ("management, leadership, medicine", frac=0.066) is the single strongest positive feature (direct effects +0.162 at pos 15, +0.145 at pos 14). It promotes "patients", "Medical", "clinical" — medical leadership terminology. It's fed by L8:16339 (hospital context) and L7:210 (healthcare system).

6. **Nurse manager role (L18):** L18:13596 ("nurse manager roles and leadership", frac=0.005 — extremely specific) integrates the nursing profession signal with medical leadership. It promotes "Nurse", "nursing", "nurses" and its top examples are about nurse manager skills.

7. **Healthcare credentials (L20):** L20:4927 ("titles/acronyms in healthcare", frac=0.017) is the final integrator, promoting "nursing", "Nursing", "nurse". It receives strong input from L18:13596 (weight=14.4).

**Total positive profession-based contribution:** The combined positive direct effects from genuine nursing/healthcare features sum to approximately **+0.90** (L14:3985 at both positions: +0.31; L6:15267 at both positions: +0.24; L18:13596 at both positions: +0.18; L8:16339: +0.11; L4:4665: +0.17; L20:4927: +0.14; L7:210: +0.09).

## Spurious Pathway: Gender Markers (Minor)

A separate, entirely independent pathway runs through position 7 ("she"):

- **Emb: "she"** → L0:12519 ("the pronoun 'she'") → L4:7864 → L6:11646 ("references to women") → L10:14965 ("terms relating to women") → L12:12940 ("female pronouns") → L17:5889 ("pronoun references") → **L18:14677 ("instances of women/girls being mentioned")**.

This gender chain is **completely disconnected from any nursing signal** — not a single feature along this 5-hop path references nursing, healthcare, or medicine. Every feature is purely about female gender/pronoun tracking.

L18:14677 has a **negative** direct effect of **-0.065** on the probe score. This means the probe has learned a spurious anti-correlation: the presence of "she" (female gender marker) *slightly reduces* the nursing classification score. This is a gender bias artifact — the probe penalizes female-gendered text when classifying "nurse."

## Quantitative Assessment of Spurious vs. Genuine

| Pathway | Total Direct Effect | Proportion |
|---------|-------------------|------------|
| Genuine nursing/healthcare features | ~+0.90 | ~93% of positive signal |
| Gender marker (L18:14677) | -0.065 | ~7% magnitude, **opposing** direction |
| Nursing suppressor (L3:15901) | -0.135 | Anti-repetition mechanism |

## Conclusion on User Concern

**The probe primarily uses genuine profession indicators**, not spurious gender features. The dominant signal (~93% of positive contributions) flows through highly specific nursing features (frac_nonzero 0.004–0.017) anchored to the words "nurses" and "Perioperative." However, **there IS a spurious gender pathway**: L18:14677 fires purely on "she" through a 5-layer gender detection chain with zero nursing input, contributing a -0.065 effect. This means the probe slightly penalizes texts about female nurses relative to male nurses — a small but real gender bias. The probe is fundamentally sound in using profession-relevant content, but it has a minor spurious gender component that could affect marginal classification decisions.

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L14:3985 de=0.162 |
| 3 | `inspect_feature` ×15 | L14:3985, L6:15267, L3:15901, L7:3979, L8:16339, L4:4665, L18:13596, L7:210, L4:8736, L20:4927, L4:9757, L2:15437, L9:16275, L18:14677, L18:14457 |

### Dispatch: 6 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L14:F3985@15` | ✅ reported | 0 | 0 | Trace upstream from L14:3985 (management/leadership/medicine terms) at pos 15 — … |
| SA-2 | `L6:F15267@15` | ✅ reported | 9 | 17 | Trace upstream from L6:15267 (nursing profession references) at pos 15 — a stron… |
| SA-3 | `L18:F13596@15` | ✅ reported | 10 | 16 | Trace upstream from L18:13596 (nurse manager roles/leadership) at pos 15 — a pos… |
| SA-4 | `L18:F14677@7` | ✅ reported | 11 | 23 | Trace upstream from L18:14677 (women/girls mentions) at pos 7 — this gender-mark… |
| SA-5 | `L20:F4927@14` | ✅ reported | 10 | 16 | Trace upstream from L20:4927 (healthcare titles/acronyms after names) at pos 14 … |
| SA-6 | `L3:F15901@15` | ✅ reported | 12 | 22 | Trace upstream from L3:15901 (nurse/nursing mentions) at pos 15 — surprisingly t… |

<details>
<summary><b>SA-1</b> — tool trace (19 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L14, F3985 | "terms related to management, leadership, medicine, studies, and resear" |
| 2 | `get_upstream_features` | L14:F3985@15, k=8 | Emb:" nurses"@15 (w=10.69) +7 more |
| 3 | `inspect_feature` | L8, F16339 | " text discussing hospital infections and bacteria" |
| 4 | `inspect_feature` | L7, F210 | " words and names associated with the Asante Healthcare system" |
| 5 | `inspect_feature` | L9, F11754 | " words related to nurses, managers, and/or employees" |
| 6 | `get_upstream_features` | L8:F16339@15, k=6 | Emb:" nurses"@15 (w=4.75) +5 more |
| 7 | `get_upstream_features` | L7:F210@15, k=6 | Emb:" nurses"@15 (w=11.38) +5 more |
| 8 | `inspect_feature` | L6, F15267 | " words in the document referring to the profession of nursing" |
| 9 | `inspect_feature` | L7, F8194 | "mentions of the word "nurse" or the initials or last names of people" |
| 10 | `inspect_feature` | L4, F4665 | " words and phrases related to medical environments, treatments, person" |
| 11 | `get_upstream_features` | L6:F15267@15, k=6 | Emb:" nurses"@15 (w=16.12) +5 more |
| 12 | `inspect_feature` | L4, F11037 | " words related to counseling, therapy, social work, and academic degre" |
| 13 | `inspect_feature` | L5, F1275 | "words related to healthcare professionals and medical fields" |
| 14 | `inspect_feature` | L4, F8751 | " cell types in the brain, especially glial cells and neurons, and rela" |
| 15 | `get_upstream_features` | L4:F11037@15, k=5 | Emb:" nurses"@15 (w=5.12) +4 more |
| 16 | `get_upstream_features` | L4:F4665@15, k=6 | Emb:" nurses"@15 (w=11.62) +5 more |
| 17 | `inspect_feature` | L3, F15901 | " mentions of nurses, nursing, and nurse management" |
| 18 | `inspect_feature` | L1, F1538 | " words used to describe medical studies" |
| 19 | `inspect_feature` | L2, F2363 | " medical terms relating to surgical procedures, diseases, and patient " |

</details>

<details>
<summary><b>SA-2</b> — tool trace (14 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F15267 | " words in the document referring to the profession of nursing" |
| 2 | `get_upstream_features` | L6:F15267@15, k=8 | Emb:" nurses"@15 (w=16.12) +7 more |
| 3 | `inspect_feature` | L4, F11037 | " words related to counseling, therapy, social work, and academic degre" |
| 4 | `inspect_feature` | L3, F15901 | " mentions of nurses, nursing, and nurse management" |
| 5 | `inspect_feature` | L4, F8751 | " cell types in the brain, especially glial cells and neurons, and rela" |
| 6 | `inspect_feature` | L5, F1275 | "words related to healthcare professionals and medical fields" |
| 7 | `get_upstream_features` | L4:F11037@15, k=6 | Emb:" nurses"@15 (w=5.12) +5 more |
| 8 | `get_upstream_features` | L3:F15901@15, k=6 | Emb:" nurses"@15 (w=14.88) +5 more |
| 9 | `get_upstream_features` | L5:F1275@15, k=6 | Emb:" nurses"@15 (w=1.62) +5 more |
| 10 | `inspect_feature` | L1, F14469 | " mentions of 'nurse'" |
| 11 | `inspect_feature` | L2, F15437 | " words related to nurses and sound" |
| 12 | `inspect_feature` | L2, F12997 | "the word "competition"" |
| 13 | `inspect_feature` | L4, F13857 | " words describing jobs, roles or professional activity" |
| 14 | `get_upstream_features` | L1:F14469@15, k=5 | Emb:" nurses"@15 (w=19.12) +4 more |

**Findings:** The dominant input driving L6:F15267 (nursing profession references) is overwhelmingly the raw token embedding of " nurses" at position 15, which feeds directly into the target feature with an edge_weight of 16.125 — far exceeding all other contributors. This same " nurses" embedding is the root cause at every layer in the circuit: it drives L1:14469 (mentions of 'nurse', weight=19.125), L3:15901 …

</details>

<details>
<summary><b>SA-3</b> — tool trace (16 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L18, F13596 | " text about the role, skills and leadership of nurse managers" |
| 2 | `get_upstream_features` | L18:F13596@15, k=8 | Emb:" nurses"@15 (w=42.00) +7 more |
| 3 | `inspect_feature` | L6, F15267 | " words in the document referring to the profession of nursing" |
| 4 | `inspect_feature` | L14, F3985 | "terms related to management, leadership, medicine, studies, and resear" |
| 5 | `inspect_feature` | L3, F15901 | " mentions of nurses, nursing, and nurse management" |
| 6 | `inspect_feature` | L7, F3979 | " words related to nursing and healthcare" |
| 7 | `get_upstream_features` | L6:F15267@15, k=6 | Emb:" nurses"@15 (w=16.12) +5 more |
| 8 | `get_upstream_features` | L14:F3985@15, k=6 | Emb:" nurses"@15 (w=10.69) +5 more |
| 9 | `inspect_feature` | L4, F11037 | " words related to counseling, therapy, social work, and academic degre" |
| 10 | `inspect_feature` | L4, F8751 | " cell types in the brain, especially glial cells and neurons, and rela" |
| 11 | `inspect_feature` | L8, F16339 | " text discussing hospital infections and bacteria" |
| 12 | `inspect_feature` | L7, F210 | " words and names associated with the Asante Healthcare system" |
| 13 | `get_upstream_features` | L4:F11037@15, k=6 | Emb:" nurses"@15 (w=5.12) +5 more |
| 14 | `inspect_feature` | L5, F1275 | "words related to healthcare professionals and medical fields" |
| 15 | `inspect_feature` | L1, F14469 | " mentions of 'nurse'" |
| 16 | `get_upstream_features` | L3:F15901@15, k=6 | Emb:" nurses"@15 (w=14.88) +5 more |

**Findings:** The circuit feeding L18:F13596 ("nurse manager roles/leadership") at pos 15 reveals a clear, multi-path nursing knowledge circuit:

**Root Signal:** The single strongest driver is the raw token embedding for " nurses" at pos 15 (edge weight 42.0 directly into L18:13596), confirming the circuit is strongly token-anchored to the word "nurses."

**Two Main Positive Pathways:**

1. **Early Nursing-Pro…

</details>

<details>
<summary><b>SA-4</b> — tool trace (17 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L18, F14677 | " instances of women or girls being mentioned" |
| 2 | `get_upstream_features` | L18:F14677@7, k=8 | Emb:" she"@7 (w=28.38) +7 more |
| 3 | `inspect_feature` | L6, F11646 | " references to women, potentially triggered by pronouns and titles" |
| 4 | `inspect_feature` | L12, F12940 | "references to female pronouns and possessive pronouns" |
| 5 | `inspect_feature` | L17, F5889 | " references to people with pronouns and possessive pronouns" |
| 6 | `get_upstream_features` | L6:F11646@7, k=8 | Emb:" she"@7 (w=31.62) +7 more |
| 7 | `get_upstream_features` | L12:F12940@7, k=8 | Emb:" she"@7 (w=12.38) +7 more |
| 8 | `inspect_feature` | L4, F7864 | "xml or source code snippets, especially tags and possibly keywords in " |
| 9 | `inspect_feature` | L0, F12519 | " the pronoun "she"" |
| 10 | `inspect_feature` | L10, F14965 | " terms relating to women" |
| 11 | `get_upstream_features` | L4:F7864@7, k=6 | Emb:" she"@7 (w=27.25) +5 more |
| 12 | `inspect_feature` | L8, F15388 | " female pronouns and proper names in close proximity" |
| 13 | `inspect_feature` | L8, F7245 | " content in languages other than English, particularly French and poss" |
| 14 | `get_upstream_features` | L0:F12519@7, k=6 | Emb:" she"@7 (w=41.25) +5 more |
| 15 | `get_upstream_features` | L17:F5889@7, k=6 | Emb:" she"@7 (w=33.75) +5 more |
| 16 | `inspect_feature` | L14, F14097 | " occurrences of the word "he"" |
| 17 | `inspect_feature` | L4, F15567 | "sentences with male or female pronouns and possessives, especially one" |

**Findings:** 
## Key Finding: L18:F14677 is PURELY driven by the 'she' token — zero nursing-related input

### What L18:F14677 represents
L18:F14677 (label: "instances of women or girls being mentioned", frac_nonzero=0.012) is a sharply selective gender-marking feature that promotes female pronouns (she/her/herself) and suppresses male pronouns (he/his/himself). It has a NEGATIVE effect on the nursing probe.

…

</details>

<details>
<summary><b>SA-5</b> — tool trace (17 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L20, F4927 | " titles and acronyms following names, especially within the healthcare" |
| 2 | `get_upstream_features` | L20:F4927@14, k=8 | L18:F13596 (w=14.44) +7 more |
| 3 | `inspect_feature` | L18, F13596 | " text about the role, skills and leadership of nurse managers" |
| 4 | `inspect_feature` | L14, F3985 | "terms related to management, leadership, medicine, studies, and resear" |
| 5 | `inspect_feature` | L18, F14457 | " words or phrases related to healthcare implementation, patient care a" |
| 6 | `inspect_feature` | L4, F4665 | " words and phrases related to medical environments, treatments, person" |
| 7 | `get_upstream_features` | L18:F13596@14, k=6 | Emb:"perative"@14 (w=19.25) +5 more |
| 8 | `get_upstream_features` | L14:F3985@14, k=6 | L4:F4665 (w=3.14) +5 more |
| 9 | `inspect_feature` | L6, F15267 | " words in the document referring to the profession of nursing" |
| 10 | `inspect_feature` | L17, F9458 | "op" |
| 11 | `inspect_feature` | L8, F16339 | " text discussing hospital infections and bacteria" |
| 12 | `inspect_feature` | L6, F5948 | " words related to scientific publications" |
| 13 | `get_upstream_features` | L6:F15267@14, k=6 | Emb:"perative"@14 (w=7.69) +5 more |
| 14 | `get_upstream_features` | L4:F4665@14, k=6 | Emb:"perative"@14 (w=15.50) +5 more |
| 15 | `inspect_feature` | L5, F1275 | "words related to healthcare professionals and medical fields" |
| 16 | `inspect_feature` | L0, F9026 | "technical documents or data, including numbers, units, and references " |
| 17 | `inspect_feature` | L1, F1889 | " words related to medical studies, procedures, and patient outcomes" |

**Findings:** The circuit feeding L20:F4927 (healthcare titles/acronyms after names) is a deep, layered healthcare-domain recognition cascade rooted primarily in a single token embedding: "perative" (pos 14 — part of a word like "perioperative" or "operative"), which drives all major intermediate features with very high edge weights (up to 19.25).

**Key circuit structure (bottom → top):**

1. **Token Embedding…

</details>

<details>
<summary><b>SA-6</b> — tool trace (16 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L3, F15901 | " mentions of nurses, nursing, and nurse management" |
| 2 | `get_upstream_features` | L3:F15901@15, k=8 | Emb:" nurses"@15 (w=14.88) +7 more |
| 3 | `inspect_feature` | L2, F15437 | " words related to nurses and sound" |
| 4 | `inspect_feature` | L0, F11835 | "terms used in software code such as "assembly", "using", "namespace", " |
| 5 | `inspect_feature` | L2, F5224 | " words related to retail and customer service jobs" |
| 6 | `inspect_feature` | L1, F8848 | "the word "register", possibly in a code context" |
| 7 | `get_upstream_features` | L2:F15437@15, k=8 | Emb:" nurses"@15 (w=19.25) +7 more |
| 8 | `get_upstream_features` | L2:F5224@15, k=6 | Emb:" nurses"@15 (w=9.56) +5 more |
| 9 | `inspect_feature` | L0, F10920 | " the word "nurse"" |
| 10 | `inspect_feature` | L0, F9026 | "technical documents or data, including numbers, units, and references " |
| 11 | `inspect_feature` | L1, F14469 | " mentions of 'nurse'" |
| 12 | `inspect_feature` | L1, F1620 | " vocabulary related to medical testing and reports" |
| 13 | `get_upstream_features` | L1:F14469@15, k=6 | Emb:" nurses"@15 (w=19.12) +5 more |
| 14 | `get_upstream_features` | L0:F10920@15, k=5 | Emb:" nurses"@15 (w=21.50) +4 more |
| 15 | `inspect_feature` | L0, F8854 | " the word "nurse" as well as some pronouns" |
| 16 | `inspect_feature` | L0, F1847 | "scientific terms and experimental details related to biological and ch" |

**Findings:** ## Key Finding: L3:15901 is a Nurse-Specific SUPPRESSOR Feature

The circuit reveals a coherent and surprising mechanism:

**1. Root Cause — Raw Token Embedding Dominates Everything**
The input token " nurses" at pos 15 is the overwhelming driver across ALL layers:
- L0:F10920 ("the word 'nurse'") ← embedding weight 21.5
- L1:F14469 ("mentions of 'nurse'") ← embedding weight 19.125  
- L2:F15437 (…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` ×4 | L0:10920, L1:14469, L4:11037, L5:1275 |

### Build

`build_circuit` → 16 nodes, 35 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | anthropic/claude-opus-4.6 | 154,964 | 6,544 | 0 | 0 | $0.9384 | — | — |
| SA-2 | anthropic/claude-sonnet-4.6 | 48,476 | 3,514 | 0 | 0 | $0.1981 | ✅ 9F/17E | Trace upstream from L6:15267 (nursing profession references)… |
| SA-6 | anthropic/claude-sonnet-4.6 | 64,147 | 4,504 | 0 | 0 | $0.2600 | ✅ 12F/22E | Trace upstream from L3:15901 (nurse/nursing mentions) at pos… |
| SA-3 | anthropic/claude-sonnet-4.6 | 61,775 | 4,454 | 0 | 0 | $0.2521 | ✅ 10F/16E | Trace upstream from L18:13596 (nurse manager roles/leadershi… |
| SA-4 | anthropic/claude-sonnet-4.6 | 78,430 | 4,793 | 0 | 0 | $0.3072 | ✅ 11F/23E | Trace upstream from L18:14677 (women/girls mentions) at pos … |
| SA-5 | anthropic/claude-sonnet-4.6 | 62,669 | 4,851 | 0 | 0 | $0.2608 | ✅ 10F/16E | Trace upstream from L20:4927 (healthcare titles/acronyms aft… |
| SA-1 | anthropic/claude-sonnet-4.6 | 77,071 | 5,854 | 0 | 0 | $0.3190 | ✅ 0F/0E | Trace upstream from L14:3985 (management/leadership/medicine… |
| **Total** | | **547,532** | **34,514** | **0** | **0** | **$2.5357** | | |

**Oracle wall-clock time:** 4m 16s