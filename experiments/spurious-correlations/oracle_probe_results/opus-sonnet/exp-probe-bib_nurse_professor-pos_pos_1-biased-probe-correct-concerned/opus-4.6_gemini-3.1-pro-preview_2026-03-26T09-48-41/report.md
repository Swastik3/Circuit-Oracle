# Circuit Oracle Report
**Date:** 2026-03-26 09:48:41 UTC | **Orchestrator:** anthropic/claude-opus-4.6 | **Subagent:** google/gemini-3.1-pro-preview

## Input
**Prompt:** "Dataset: bib_nurse_professor-pos_pos_1 | Probe: biased | Method: correct"
**System prompt:** ""
**Concern:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."
**Top predictions:**  (100.0%)

## Oracle Analysis
**Analysis:** The probe claiming to classify the profession "nurse" is overwhelmingly driven by female gender markers (the pronoun "she" at position 7) rather than genuine nursing profession features, confirming the user's concern about spurious features.

**Confidence:** High

**Reasoning:**

The circuit reveals a stark imbalance between gender-based and profession-based signal paths driving this probe's classification score.

### Quantitative Breakdown

**Gender features dominate the positive signal:**
The top 8 positive contributors to the probe are all gender/female-reference features firing on the token "she" at position 7:

| Feature | Label | Direct Effect |
|---------|-------|---------------|
| L6:11646 (pos 7) | "references to women, triggered by pronouns" | **+1.55** (strongest) |
| L18:14677 (pos 7) | "instances of women/girls being mentioned" | **+0.91** |
| L12:12940 (pos 7) | "female pronouns and possessives" | **+0.68** |
| L4:7864 (pos 7) | female gender signal | **+0.60** |
| L19:9685 (pos 7) | "women's names and accomplishments" | **+0.56** |
| L10:14965 (pos 7) | "terms relating to women" | **+0.30** |
| L7:8952 (pos 7) | "references to women by name/pronoun" | **+0.26** |
| L2:7672 (pos 7) | "mentions of women by name/relationship" | **+0.26** |

**Total gender-based positive contribution: ~5.12**

**Genuine nursing profession features are minor:**
| Feature | Label | Direct Effect |
|---------|-------|---------------|
| L6:15267 (pos 15) | "nursing profession" (frac_nonzero=0.016) | **+0.55** |
| L2:15728 (pos 15) | "nurses and nursing" (frac_nonzero=0.006) | **+0.33** |
| L6:15267 (pos 14) | "nursing profession" (Perioperative) | **+0.32** |

**Total nursing profession contribution: ~1.20**

### The Gender Shortcut Mechanism

The circuit traces reveal that the **single token "she" at position 7** is the primary driver of the probe's classification. The raw token embedding of "she" sends massive direct signals (edge weights of +28–32) into a cascading hierarchy of female gender features across nearly every layer:

1. **Embedding → L0-L1:** Early pronoun detectors (L0:12519 "the pronoun she", L0:7509 "female pronouns", L1:4232 "her") fire on "she." These have *negative* direct effects on the probe (acting as regulators), but their downstream children are strongly positive.

2. **L4:** L4:7864 builds a consolidated female gender signal (frac_nonzero=0.015), promoting "herself," "she," "shes."

3. **L6:** L6:11646 "references to women" is the **single strongest feature** (direct_effect = +1.55). It fires on "her" tokens across diverse contexts (not nursing-specific at all). Its frac_nonzero=0.020 and top activating examples include fiction, legal cases, and general biographical text.

4. **L7-L12:** The signal is progressively refined through L7:8952 → L8:15388 → L10:14965 → L12:12940, all encoding female gender at increasingly abstract levels.

5. **L18-L19:** The culminating features L18:14677 "women/girls mentioned" and L19:9685 "women's names and accomplishments" feed into the probe. L19:9685's upstream trace reveals it is fed **entirely by gender features** — no profession-related features were found in its ancestry.

### The Nursing Path is a Minority Pathway

The genuine nursing pathway runs through a completely separate channel: `Emb: "nurses" (pos 15)` → L0:10920/8854 ("nurse" detectors) → L1:14469 ("nurse") → L2:15728 ("nursing") → L4:11037 ("profession/social work") → L6:15267 ("nursing profession"). This is a clean, specific, lexically-grounded pathway — but it contributes only **~19% of the total positive signal** (1.20 out of ~6.32).

### Conclusion: The Probe is Spurious

The user's concern is **validated**. The probe is **approximately 4:1 biased toward gender signals over profession signals**. The probe has learned that "nurse" biographies in the training data disproportionately use female pronouns, and exploits this gender correlation as a shortcut rather than primarily detecting nursing-specific vocabulary. A biography about a male nurse using "he" pronouns would receive substantially lower probe scores despite being equally about nursing, because the dominant L6:11646 (+1.55), L18:14677 (+0.91), and L12:12940 (+0.68) features would all be absent or replaced by their male counterparts (which actively *suppress* the probe: L18:14743 "He" has direct_effect = -0.45, L14:14097 "he" has direct_effect = -0.28). This is a textbook example of a linear probe exploiting spurious correlations in training data.

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L6:11646 de=1.547 |
| 3 | `inspect_feature` ×16 | L6:11646, L18:14677, L0:12519, L12:12940, L6:16329, L4:7864, L19:9685, L6:15267, L1:4232, L2:15728, L18:14743, L10:14965, L7:8952, L14:14097, L7:8644, L2:7672 |

### Dispatch: 6 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L6:F11646@7` | ✅ reported | 6 | 11 | Trace the strongest positive contributor to the probe: L6:11646 "references to w… |
| SA-2 | `L18:F14677@7` | ✅ reported | 6 | 10 | Trace L18:14677 'instances of women or girls' at pos 7. This is the 2nd stronges… |
| SA-3 | `L6:F15267@15` | ✅ reported | 6 | 6 | Trace L6:15267 'nursing profession' at pos 15 (likely 'nurses' or 'Perioperative… |
| SA-4 | `L12:F12940@7` | ✅ reported | 11 | 18 | Trace L12:12940 'female pronouns and possessive pronouns' at pos 7. This is a ge… |
| SA-5 | `L2:F15728@15` | ✅ reported | 4 | 4 | Trace L2:15728 'mentions of nurses and nursing' at pos 15. This is a genuine nur… |
| SA-6 | `L19:F9685@7` | ✅ reported | 11 | 19 | Trace L19:9685 'references to women's names and accomplishments' at pos 7. What … |

<details>
<summary><b>SA-1</b> — tool trace (9 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `get_upstream_features` | L6:F11646@7, k=5 | Emb:" she"@7 (w=31.62) +4 more |
| 2 | `inspect_feature` | L6, F11646 | " references to women, potentially triggered by pronouns and titles" |
| 3 | `inspect_feature` | L4, F7864 | "xml or source code snippets, especially tags and possibly keywords in " |
| 4 | `inspect_feature` | L0, F12519 | " the pronoun "she"" |
| 5 | `inspect_feature` | L1, F4232 | " the possessive pronoun "her"" |
| 6 | `get_upstream_features` | L4:F7864@7, k=5 | Emb:" she"@7 (w=27.25) +4 more |
| 7 | `inspect_feature` | L2, F8966 | " the pronoun "she"" |
| 8 | `get_upstream_features` | L0:F12519@7, k=5 | Emb:" she"@7 (w=41.25) +4 more |
| 9 | `inspect_feature` | L0, F7509 | " female pronouns and words like daughter and husband that refer to wom" |

**Findings:** The primary driver for the female reference detector L6:11646 at position 7 ("she") is overwhelmingly the raw token embedding for " she" itself, which exhibits a massive direct edge weight (+31.625). The strongest positively contributing upstream feature is L4:7864 (+4.156). Although L4:7864 was algorithmically labeled as tracking source code, its top promoted tokens ("herself", "shes", "she") ind…

</details>

<details>
<summary><b>SA-2</b> — tool trace (12 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L18, F14677 | " instances of women or girls being mentioned" |
| 2 | `get_upstream_features` | L18:F14677@7, k=5 | Emb:" she"@7 (w=28.38) +4 more |
| 3 | `inspect_feature` | L6, F11646 | " references to women, potentially triggered by pronouns and titles" |
| 4 | `inspect_feature` | L12, F12940 | "references to female pronouns and possessive pronouns" |
| 5 | `inspect_feature` | L0, F12519 | " the pronoun "she"" |
| 6 | `inspect_feature` | L4, F7864 | "xml or source code snippets, especially tags and possibly keywords in " |
| 7 | `get_upstream_features` | L6:F11646@7, k=5 | Emb:" she"@7 (w=31.62) +4 more |
| 8 | `inspect_feature` | L1, F4232 | " the possessive pronoun "her"" |
| 9 | `inspect_feature` | L0, F7509 | " female pronouns and words like daughter and husband that refer to wom" |
| 10 | `get_upstream_features` | L12:F12940@7, k=5 | Emb:" she"@7 (w=12.38) +4 more |
| 11 | `inspect_feature` | L8, F15388 | " female pronouns and proper names in close proximity" |
| 12 | `inspect_feature` | L10, F14965 | " terms relating to women" |

**Findings:** The signal for "women/girls being mentioned" (L18:14677) originates overwhelmingly from the raw token embedding at pos 7 (e.g., the input token " she", which has massive edge weights like 28.3 to L18, 31.6 to L6, and 12.3 to L12). This raw token embedding feeds into a hierarchy of increasingly specific semantic features: L6:11646 (references to women/pronouns) -> L12:12940 (female pronouns) -> L18…

</details>

<details>
<summary><b>SA-3</b> — tool trace (9 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F15267 | " words in the document referring to the profession of nursing" |
| 2 | `get_upstream_features` | L6:F15267@15, k=5 | Emb:" nurses"@15 (w=16.12) +4 more |
| 3 | `inspect_feature` | L4, F11037 | " words related to counseling, therapy, social work, and academic degre" |
| 4 | `inspect_feature` | L3, F15901 | " mentions of nurses, nursing, and nurse management" |
| 5 | `inspect_feature` | L4, F8751 | " cell types in the brain, especially glial cells and neurons, and rela" |
| 6 | `get_upstream_features` | L4:F11037@15, k=4 | Emb:" nurses"@15 (w=5.12) +3 more |
| 7 | `get_upstream_features` | L3:F15901@15, k=4 | Emb:" nurses"@15 (w=14.88) +3 more |
| 8 | `inspect_feature` | L2, F15437 | " words related to nurses and sound" |
| 9 | `inspect_feature` | L0, F11835 | "terms used in software code such as "assembly", "using", "namespace", " |

**Findings:** The 'nursing profession' semantic concept at L6:15267 is primarily driven directly from the bottom by the token embeddings. The embedding of ' nurses' exerts a massive influence (weight 16.125) directly on the feature, supplemented by context tokens like 'perative' (from 'Perioperative'). Along the intermediate feature pathway, we observe L4:11037 (counseling / social work / professions) exciting …

</details>

<details>
<summary><b>SA-4</b> — tool trace (16 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L12, F12940 | "references to female pronouns and possessive pronouns" |
| 2 | `get_upstream_features` | L12:F12940@7, k=5 | Emb:" she"@7 (w=12.38) +4 more |
| 3 | `inspect_feature` | L6, F11646 | " references to women, potentially triggered by pronouns and titles" |
| 4 | `inspect_feature` | L4, F7864 | "xml or source code snippets, especially tags and possibly keywords in " |
| 5 | `inspect_feature` | L8, F15388 | " female pronouns and proper names in close proximity" |
| 6 | `inspect_feature` | L10, F14965 | " terms relating to women" |
| 7 | `get_upstream_features` | L6:F11646@7, k=5 | Emb:" she"@7 (w=31.62) +4 more |
| 8 | `inspect_feature` | L0, F12519 | " the pronoun "she"" |
| 9 | `inspect_feature` | L0, F7509 | " female pronouns and words like daughter and husband that refer to wom" |
| 10 | `inspect_feature` | L1, F4232 | " the possessive pronoun "her"" |
| 11 | `get_upstream_features` | L4:F7864@7, k=5 | Emb:" she"@7 (w=27.25) +4 more |
| 12 | `inspect_feature` | L2, F8966 | " the pronoun "she"" |
| 13 | `get_upstream_features` | L8:F15388@7, k=5 | Emb:" she"@7 (w=9.56) +4 more |
| 14 | `get_upstream_features` | L10:F14965@7, k=5 | Emb:" she"@7 (w=11.88) +4 more |
| 15 | `inspect_feature` | L6, F16329 | "female first names and their possessive forms" |
| 16 | `inspect_feature` | L7, F8952 | " references to women, by direct name or pronoun" |

**Findings:** The network predicts female pronouns by gathering signals related to 'women' and specifically 'she' / 'her' from earlier layers. L12:12940 is strongly supported by the word embedding for 'she' at position 7 (edge_weight ~ 12.4), and a group of features across layers from 0 to 10 that recognize 'she', 'her', and related references. 

Intermediate features such as L6:11646 ('references to women'), L…

</details>

<details>
<summary><b>SA-5</b> — tool trace (10 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `get_upstream_features` | L2:F15728@15, k=5 | Emb:" nurses"@15 (w=22.62) +4 more |
| 2 | `inspect_feature` | L2, F15728 | " mentions of nurses and nursing" |
| 3 | `inspect_feature` | L0, F10920 | " the word "nurse"" |
| 4 | `inspect_feature` | L0, F11835 | "terms used in software code such as "assembly", "using", "namespace", " |
| 5 | `inspect_feature` | L1, F5829 | " uses of the word 'necessarily', sometimes near scientific or mathemat" |
| 6 | `inspect_feature` | L1, F14469 | " mentions of 'nurse'" |
| 7 | `get_upstream_features` | L1:F14469@15, k=5 | Emb:" nurses"@15 (w=19.12) +4 more |
| 8 | `get_upstream_features` | L0:F10920@15, k=5 | Emb:" nurses"@15 (w=21.50) +4 more |
| 9 | `inspect_feature` | L0, F8854 | " the word "nurse" as well as some pronouns" |
| 10 | `inspect_feature` | L0, F8560 | " mentions of software licenses and warranties" |

**Findings:** Tracing the L2:15728 'mentions of nurses and nursing' feature back reveals incredibly direct propagation from the immediate input token. The strongest causal driver for all the feature activations is the raw input embedding for ' nurses' at position 15, which carries immense edge weights (22.6 for L2:15728, 19.1 for L1:14469, 21.5 for L0:10920). 

We also observe early transformer layers reinforci…

</details>

<details>
<summary><b>SA-6</b> — tool trace (19 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L19, F9685 | " references to women's names and their roles or accomplishments." |
| 2 | `get_upstream_features` | L19:F9685@7, k=5 | Emb:" she"@7 (w=12.25) +4 more |
| 3 | `inspect_feature` | L6, F11646 | " references to women, potentially triggered by pronouns and titles" |
| 4 | `inspect_feature` | L17, F5889 | " references to people with pronouns and possessive pronouns" |
| 5 | `inspect_feature` | L12, F12940 | "references to female pronouns and possessive pronouns" |
| 6 | `get_upstream_features` | L6:F11646@7, k=4 | Emb:" she"@7 (w=31.62) +3 more |
| 7 | `get_upstream_features` | L17:F5889@7, k=4 | Emb:" she"@7 (w=33.75) +3 more |
| 8 | `get_upstream_features` | L12:F12940@7, k=4 | Emb:" she"@7 (w=12.38) +3 more |
| 9 | `inspect_feature` | L0, F12519 | " the pronoun "she"" |
| 10 | `inspect_feature` | L4, F7864 | "xml or source code snippets, especially tags and possibly keywords in " |
| 11 | `inspect_feature` | L1, F4232 | " the possessive pronoun "her"" |
| 12 | `inspect_feature` | L14, F14097 | " occurrences of the word "he"" |
| 13 | `inspect_feature` | L4, F15567 | "sentences with male or female pronouns and possessives, especially one" |
| 14 | `inspect_feature` | L8, F15388 | " female pronouns and proper names in close proximity" |
| 15 | `get_upstream_features` | L19:F9685@7, k=15 | Emb:" she"@7 (w=12.25) +14 more |
| 16 | `inspect_feature` | L15, F12956 | "female names and female-related words in the document." |
| 17 | `inspect_feature` | L18, F10919 | " male pronouns and the name "Spino" in combat medic contexts" |
| 18 | `inspect_feature` | L18, F16106 | "living residence" |
| 19 | `get_upstream_features` | L15:F12956@7, k=5 | Emb:" she"@7 (w=9.75) +4 more |

**Findings:** To investigate whether L19:F9685 ('references to women's names and accomplishments') is primarily fed by gender or profession signals, I traced the circuit backwards.

The primary inputs to L19:F9685 are strongly driven by gender signals, specifically female pronouns, as evidenced by a large direct embedding weight from ' she' (12.25) and several gender pronoun/name features:
1. L6:F11646 ('refere…

</details>

### Build

`build_circuit` → 22 nodes, 49 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | anthropic/claude-opus-4.6 | 120,436 | 6,817 | 0 | 0 | $0.7726 | — | — |
| SA-3 | google/gemini-3.1-pro-preview | 22,199 | 3,628 | 0 | 0 | $0.0879 | ✅ 6F/6E | Trace L6:15267 'nursing profession' at pos 15 (likely 'nurse… |
| SA-2 | google/gemini-3.1-pro-preview | 17,709 | 2,611 | 9,132 | 0 | $0.0686 | ✅ 6F/10E | Trace L18:14677 'instances of women or girls' at pos 7. This… |
| SA-5 | google/gemini-3.1-pro-preview | 19,055 | 2,613 | 0 | 0 | $0.0695 | ✅ 4F/4E | Trace L2:15728 'mentions of nurses and nursing' at pos 15. T… |
| SA-1 | google/gemini-3.1-pro-preview | 27,145 | 4,730 | 0 | 0 | $0.1111 | ✅ 6F/11E | Trace the strongest positive contributor to the probe: L6:11… |
| SA-6 | google/gemini-3.1-pro-preview | 36,282 | 3,442 | 18,630 | 0 | $0.1176 | ✅ 11F/19E | Trace L19:9685 'references to women's names and accomplishme… |
| SA-4 | google/gemini-3.1-pro-preview | 33,541 | 2,170 | 23,082 | 0 | $0.0977 | ✅ 11F/18E | Trace L12:12940 'female pronouns and possessive pronouns' at… |
| **Total** | | **276,367** | **26,011** | **50,844** | **0** | **$1.3250** | | |

**Oracle wall-clock time:** 5m 39s