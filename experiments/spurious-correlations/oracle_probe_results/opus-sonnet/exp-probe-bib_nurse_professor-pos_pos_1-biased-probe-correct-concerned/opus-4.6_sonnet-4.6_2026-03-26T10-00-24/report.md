# Circuit Oracle Report
**Date:** 2026-03-26 10:00:24 UTC | **Orchestrator:** anthropic/claude-opus-4.6 | **Subagent:** anthropic/claude-sonnet-4.6

## Input
**Prompt:** "Dataset: bib_nurse_professor-pos_pos_1 | Probe: biased | Method: correct"
**System prompt:** ""
**Concern:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."
**Top predictions:**  (100.0%)

## Oracle Analysis
## Analysis

**Analysis:** The probe classifies this text as "nurse," but its classification is overwhelmingly driven by gender markers (the pronoun "she") rather than genuine profession indicators (the word "nurses"), confirming the user's concern about spurious features.

**Confidence:** High

**Reasoning:**

The circuit reveals two sharply distinct pathways feeding the probe's classification score, with dramatically unequal contributions:

### Path 1: Gender Pathway (~83% of positive signal, ~5.7 total direct effect)
This massive pathway originates almost entirely from the **"she" token embedding at position 7** (edge weights of 12–32 to downstream features). It feeds a cascading chain of **11+ gender-detecting features** spanning layers 0–19, none of which encode any profession-specific information:

- **L6:11646** ("references to women, triggered by pronouns/titles", frac_nonzero=0.020) — the **single strongest feature** with direct effect **+1.55**. Upstream: "she" embedding (weight=31.6).
- **L18:14677** ("women or girls being mentioned", frac_nonzero=0.012) — **+0.91** direct effect at pos 7, plus **+0.31** and **+0.27** at positions 38 and 53. Fed by "she" embedding (28.4), L6:11646 (5.6), and L12:12940 (4.3).
- **L12:12940** ("female pronouns/possessives", frac_nonzero=0.007) — **+0.68**. Fed by "she" embedding (12.4) and L6:11646 (5.0).
- **L4:7864** (mixed feature promoting "herself"/"she") — **+0.60**.
- **L19:9685** ("women's names/roles/accomplishments") — **+0.56**. This is the closest to a profession-relevant feature, but inspection shows it's a generic female-reference detector, not nursing-specific.
- Additional gender features at L10:14965 (+0.30), L7:8952 (+0.26), L2:7672 (+0.26).

Counter-gender features (male-detecting) provide negative signals: L6:16329 (female names, ironically suppressing the female direction, −0.66), L0:12519 ("she" pronoun, −0.70), L1:4232 ("her", −0.43), L18:14743 ("He", −0.45), L14:14097 ("he", −0.28). These act as competing inhibitors.

### Path 2: Nursing/Profession Pathway (~17% of positive signal, ~1.2 total direct effect)
This pathway originates from the **"nurses" token embedding at position 15** and builds through a clean lexical detection chain:

- **Emb "nurses"** (pos 15) → L0:10920 ("the word 'nurse'", frac=0.006) → L1:14469 ("mentions of 'nurse'", frac=0.004) → L2:15728 ("nurses and nursing", frac=0.006, DE=**+0.33**) → L3:15901 ("nurses/nursing/nurse management", frac=0.005) → L4:11037 ("counseling/therapy/social work", frac=0.007) → L5:1275 ("healthcare professionals", frac=0.013) → **L6:15267** ("profession of nursing", frac=0.016, DE=**+0.55** at pos 15, **+0.32** at pos 14).

This is a genuine, highly specific profession-detection pathway (all features have low frac_nonzero ≤ 0.02, and top activating examples consistently involve nursing contexts). But its combined contribution (~1.2) is dwarfed by the gender pathway (~5.7).

### The Spuriousness Problem

The probe has learned that "nurse" correlates with female gender. The evidence is stark:
1. **The single strongest feature** (L6:11646, +1.55) detects "references to women" — not nursing at all.
2. **83% of the positive signal** comes from gender features that would fire identically for a female teacher, female lawyer, or any biography using "she/her."
3. The genuine nursing features contribute only **~17%** of the classification signal.
4. Every single gender feature's top activating examples are generic female-reference contexts (novels, legal cases, biographies) — none are nursing-specific.
5. The gender features all originate from a single input token ("she") while the profession features originate from a different token ("nurses"). This means the probe would likely still classify "nurse" even if "nurses" were replaced with a different profession, as long as "she" remained.

**Conclusion:** The user's concern is validated. This probe is overwhelmingly a **gender classifier masquerading as a profession classifier**. It has exploited the statistical correlation between female gender and the nursing profession in training data, making it a textbook example of spurious feature reliance. A robust profession probe should primarily weight the nursing pathway (L6:15267 and its precursors), not the gender chain originating from "she."

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L6:11646 de=1.547 |
| 3 | `inspect_feature` ×16 | L6:11646, L18:14677, L0:12519, L12:12940, L6:16329, L4:7864, L19:9685, L6:15267, L1:4232, L2:15728, L18:14743, L10:14965, L14:14097, L7:8644, L7:8952, L2:7672 |

### Dispatch: 6 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L6:F11646@7` | ✅ reported | 0 | 0 | Trace the strongest positive feature driving the probe score (L6:11646 - referen… |
| SA-2 | `L18:F14677@7` | ✅ reported | 0 | 0 | Trace L18:14677 (women/girls being mentioned) - the second strongest positive fe… |
| SA-3 | `L6:F15267@15` | ✅ reported | 7 | 17 | Trace L6:15267 (nursing profession words) at position 15. This is the main profe… |
| SA-4 | `L19:F9685@7` | ✅ reported | 0 | 0 | Trace L19:9685 (women's names/roles/accomplishments) - this fires at pos 7 (she)… |
| SA-5 | `L12:F12940@7` | ✅ reported | 0 | 0 | Trace L12:12940 (female pronouns/possessives) - another gender feature at pos 7 … |
| SA-6 | `L2:F15728@15` | ✅ reported | 7 | 11 | Trace L2:15728 (mentions of nurses/nursing) at position 15. This is a genuine nu… |

<details>
<summary><b>SA-1</b> — tool trace (21 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F11646 | " references to women, potentially triggered by pronouns and titles" |
| 2 | `get_upstream_features` | L6:F11646@7, k=8 | Emb:" she"@7 (w=31.62) +7 more |
| 3 | `inspect_feature` | L4, F7864 | "xml or source code snippets, especially tags and possibly keywords in " |
| 4 | `inspect_feature` | L5, F10952 | "third person pronouns in varying contexts" |
| 5 | `inspect_feature` | L0, F12519 | " the pronoun "she"" |
| 6 | `inspect_feature` | L5, F6637 | " female first names with two syllables" |
| 7 | `get_upstream_features` | L4:F7864@7, k=8 | Emb:" she"@7 (w=27.25) +7 more |
| 8 | `get_upstream_features` | L5:F10952@7, k=8 | Emb:" she"@7 (w=9.94) +7 more |
| 9 | `get_upstream_features` | L0:F12519@7, k=6 | Emb:" she"@7 (w=41.25) +5 more |
| 10 | `inspect_feature` | L2, F8966 | " the pronoun "she"" |
| 11 | `inspect_feature` | L1, F4232 | " the possessive pronoun "her"" |
| 12 | `inspect_feature` | L2, F6155 | " references to people, especially pronouns like "he" or "she"" |
| 13 | `inspect_feature` | L0, F11992 | " the pronouns "he", "she", "his", and "her"" |
| 14 | `get_upstream_features` | L2:F6155@7, k=8 | Emb:" she"@7 (w=15.75) +7 more |
| 15 | `get_upstream_features` | L1:F4232@7, k=6 | Emb:" she"@7 (w=31.75) +5 more |
| 16 | `inspect_feature` | L0, F7509 | " female pronouns and words like daughter and husband that refer to wom" |
| 17 | `inspect_feature` | L0, F2241 | " the pronoun "she"" |
| 18 | `inspect_feature` | L1, F3901 | " words related to people, their jobs, titles, activities, and notable " |
| 19 | `get_upstream_features` | L1:F3901@7, k=8 | Emb:" she"@7 (w=3.47) +7 more |
| 20 | `inspect_feature` | L0, F11835 | "terms used in software code such as "assembly", "using", "namespace", " |
| 21 | `inspect_feature` | L0, F310 | " the pronouns "she", "her", and "he" and sometimes the word "therefore" |

</details>

<details>
<summary><b>SA-2</b> — tool trace (22 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L18, F14677 | " instances of women or girls being mentioned" |
| 2 | `get_upstream_features` | L18:F14677@7, k=8 | Emb:" she"@7 (w=28.38) +7 more |
| 3 | `inspect_feature` | L6, F11646 | " references to women, potentially triggered by pronouns and titles" |
| 4 | `inspect_feature` | L12, F12940 | "references to female pronouns and possessive pronouns" |
| 5 | `inspect_feature` | L4, F7864 | "xml or source code snippets, especially tags and possibly keywords in " |
| 6 | `inspect_feature` | L17, F5889 | " references to people with pronouns and possessive pronouns" |
| 7 | `get_upstream_features` | L6:F11646@7, k=8 | Emb:" she"@7 (w=31.62) +7 more |
| 8 | `get_upstream_features` | L12:F12940@7, k=8 | Emb:" she"@7 (w=12.38) +7 more |
| 9 | `inspect_feature` | L0, F12519 | " the pronoun "she"" |
| 10 | `inspect_feature` | L8, F15388 | " female pronouns and proper names in close proximity" |
| 11 | `inspect_feature` | L10, F14965 | " terms relating to women" |
| 12 | `inspect_feature` | L8, F7245 | " content in languages other than English, particularly French and poss" |
| 13 | `inspect_feature` | L5, F10952 | "third person pronouns in varying contexts" |
| 14 | `get_upstream_features` | L10:F14965@7, k=8 | Emb:" she"@7 (w=11.88) +7 more |
| 15 | `get_upstream_features` | L5:F10952@7, k=8 | Emb:" she"@7 (w=9.94) +7 more |
| 16 | `inspect_feature` | L6, F16329 | "female first names and their possessive forms" |
| 17 | `inspect_feature` | L7, F8952 | " references to women, by direct name or pronoun" |
| 18 | `inspect_feature` | L1, F4232 | " the possessive pronoun "her"" |
| 19 | `get_upstream_features` | L7:F8952@7, k=8 | Emb:" she"@7 (w=24.25) +7 more |
| 20 | `inspect_feature` | L2, F8966 | " the pronoun "she"" |
| 21 | `inspect_feature` | L5, F6637 | " female first names with two syllables" |
| 22 | `inspect_feature` | L4, F15317 | " named entities like characters or people" |

</details>

<details>
<summary><b>SA-3</b> — tool trace (11 calls)</summary>

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
| 11 | `inspect_feature` | L2, F12997 | "the word "competition"" |

**Findings:** ## Key Finding: The signal is overwhelmingly from the ' nurses' token, NOT 'Perioperative'

**Primary driver:** The raw embedding of the token ` nurses` (pos=15) is the dominant upstream signal at every layer traced:
- To L6:F15267 directly: **edge_weight = 16.125** (by far the largest input)
- To L3:F15901 (nursing-specific intermediate): **edge_weight = 14.875**
- To L4:F11037 (healthcare/social…

</details>

<details>
<summary><b>SA-4</b> — tool trace (22 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L19, F9685 | " references to women's names and their roles or accomplishments." |
| 2 | `get_upstream_features` | L19:F9685@7, k=8 | Emb:" she"@7 (w=12.25) +7 more |
| 3 | `inspect_feature` | L6, F11646 | " references to women, potentially triggered by pronouns and titles" |
| 4 | `inspect_feature` | L17, F5889 | " references to people with pronouns and possessive pronouns" |
| 5 | `inspect_feature` | L12, F12940 | "references to female pronouns and possessive pronouns" |
| 6 | `inspect_feature` | L0, F12519 | " the pronoun "she"" |
| 7 | `get_upstream_features` | L6:F11646@7, k=6 | Emb:" she"@7 (w=31.62) +5 more |
| 8 | `get_upstream_features` | L12:F12940@7, k=6 | Emb:" she"@7 (w=12.38) +5 more |
| 9 | `inspect_feature` | L4, F7864 | "xml or source code snippets, especially tags and possibly keywords in " |
| 10 | `inspect_feature` | L8, F15388 | " female pronouns and proper names in close proximity" |
| 11 | `inspect_feature` | L10, F14965 | " terms relating to women" |
| 12 | `inspect_feature` | L8, F7245 | " content in languages other than English, particularly French and poss" |
| 13 | `get_upstream_features` | L4:F7864@7, k=6 | Emb:" she"@7 (w=27.25) +5 more |
| 14 | `inspect_feature` | L1, F4232 | " the possessive pronoun "her"" |
| 15 | `inspect_feature` | L2, F8966 | " the pronoun "she"" |
| 16 | `get_upstream_features` | L10:F14965@7, k=6 | Emb:" she"@7 (w=11.88) +5 more |
| 17 | `inspect_feature` | L15, F12956 | "female names and female-related words in the document." |
| 18 | `inspect_feature` | L6, F16329 | "female first names and their possessive forms" |
| 19 | `inspect_feature` | L7, F8952 | " references to women, by direct name or pronoun" |
| 20 | `get_upstream_features` | L6:F11646@7, k=6 | Emb:" she"@7 (w=31.62) +5 more |
| 21 | `inspect_feature` | L0, F7509 | " female pronouns and words like daughter and husband that refer to wom" |
| 22 | `inspect_feature` | L5, F6637 | " female first names with two syllables" |

</details>

<details>
<summary><b>SA-5</b> — tool trace (17 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L12, F12940 | "references to female pronouns and possessive pronouns" |
| 2 | `get_upstream_features` | L12:F12940@7, k=8 | Emb:" she"@7 (w=12.38) +7 more |
| 3 | `inspect_feature` | L6, F11646 | " references to women, potentially triggered by pronouns and titles" |
| 4 | `inspect_feature` | L4, F7864 | "xml or source code snippets, especially tags and possibly keywords in " |
| 5 | `inspect_feature` | L10, F14965 | " terms relating to women" |
| 6 | `inspect_feature` | L8, F7245 | " content in languages other than English, particularly French and poss" |
| 7 | `get_upstream_features` | L6:F11646@7, k=6 | Emb:" she"@7 (w=31.62) +5 more |
| 8 | `get_upstream_features` | L10:F14965@7, k=6 | Emb:" she"@7 (w=11.88) +5 more |
| 9 | `inspect_feature` | L8, F15388 | " female pronouns and proper names in close proximity" |
| 10 | `inspect_feature` | L7, F8952 | " references to women, by direct name or pronoun" |
| 11 | `get_upstream_features` | L4:F7864@7, k=6 | Emb:" she"@7 (w=27.25) +5 more |
| 12 | `inspect_feature` | L6, F16329 | "female first names and their possessive forms" |
| 13 | `get_upstream_features` | L7:F8952@7, k=6 | Emb:" she"@7 (w=24.25) +5 more |
| 14 | `inspect_feature` | L0, F12519 | " the pronoun "she"" |
| 15 | `inspect_feature` | L1, F4232 | " the possessive pronoun "her"" |
| 16 | `inspect_feature` | L2, F8966 | " the pronoun "she"" |
| 17 | `inspect_feature` | L5, F6637 | " female first names with two syllables" |

</details>

<details>
<summary><b>SA-6</b> — tool trace (10 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L2, F15728 | " mentions of nurses and nursing" |
| 2 | `get_upstream_features` | L2:F15728@15, k=8 | Emb:" nurses"@15 (w=22.62) +7 more |
| 3 | `inspect_feature` | L0, F10920 | " the word "nurse"" |
| 4 | `inspect_feature` | L0, F11835 | "terms used in software code such as "assembly", "using", "namespace", " |
| 5 | `inspect_feature` | L1, F5829 | " uses of the word 'necessarily', sometimes near scientific or mathemat" |
| 6 | `inspect_feature` | L1, F14469 | " mentions of 'nurse'" |
| 7 | `get_upstream_features` | L0:F10920@15, k=6 | Emb:" nurses"@15 (w=21.50) +5 more |
| 8 | `get_upstream_features` | L1:F14469@15, k=6 | Emb:" nurses"@15 (w=19.12) +5 more |
| 9 | `inspect_feature` | L0, F8854 | " the word "nurse" as well as some pronouns" |
| 10 | `inspect_feature` | L0, F9026 | "technical documents or data, including numbers, units, and references " |

**Findings:** ## Circuit Summary: L2:F15728 "mentions of nurses and nursing"

### Key Finding: YES — the signal comes DIRECTLY from the ' nurses' token embedding.

The `" nurses"` token embedding at position 15 is overwhelmingly the dominant driver of L2:F15728, with a massive edge weight of **22.625** — roughly 30× larger than the next strongest input (L0:F10920 at 0.668). This same token embedding also direct…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L6:F11646@7, k=10 → Emb:" she"@7 (w=31.62) +9 more |
| 2 | `get_upstream_features` | L18:F14677@7, k=10 → Emb:" she"@7 (w=28.38) +9 more |
| 3 | `get_upstream_features` | L19:F9685@7, k=10 → Emb:" she"@7 (w=12.25) +9 more |
| 4 | `get_upstream_features` | L12:F12940@7, k=10 → Emb:" she"@7 (w=12.38) +9 more |
| 5 | `inspect_feature` ×5 | L17:5889, L15:12956, L8:15388, L3:15901, L4:11037 |

### Build

`build_circuit` → 22 nodes, 43 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | anthropic/claude-opus-4.6 | 161,767 | 7,883 | 0 | 0 | $1.0059 | — | — |
| SA-3 | anthropic/claude-sonnet-4.6 | 33,901 | 3,585 | 0 | 0 | $0.1555 | ✅ 7F/17E | Trace L6:15267 (nursing profession words) at position 15. Th… |
| SA-6 | anthropic/claude-sonnet-4.6 | 33,681 | 3,411 | 0 | 0 | $0.1522 | ✅ 7F/11E | Trace L2:15728 (mentions of nurses/nursing) at position 15. … |
| SA-5 | anthropic/claude-sonnet-4.6 | 70,322 | 5,733 | 0 | 0 | $0.2970 | ✅ 0F/0E | Trace L12:12940 (female pronouns/possessives) - another gend… |
| SA-4 | anthropic/claude-sonnet-4.6 | 96,963 | 6,190 | 0 | 0 | $0.3837 | ✅ 0F/0E | Trace L19:9685 (women's names/roles/accomplishments) - this … |
| SA-1 | anthropic/claude-sonnet-4.6 | 106,359 | 6,003 | 0 | 0 | $0.4091 | ✅ 0F/0E | Trace the strongest positive feature driving the probe score… |
| SA-2 | anthropic/claude-sonnet-4.6 | 113,840 | 6,303 | 0 | 0 | $0.4361 | ✅ 0F/0E | Trace L18:14677 (women/girls being mentioned) - the second s… |
| **Total** | | **616,833** | **39,108** | **0** | **0** | **$2.8395** | | |

**Oracle wall-clock time:** 4m 56s