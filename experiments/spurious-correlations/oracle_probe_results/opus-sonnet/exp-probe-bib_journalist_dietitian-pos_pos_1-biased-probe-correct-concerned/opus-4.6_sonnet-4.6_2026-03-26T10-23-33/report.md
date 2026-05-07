# Circuit Oracle Report
**Date:** 2026-03-26 10:23:33 UTC | **Orchestrator:** anthropic/claude-opus-4.6 | **Subagent:** anthropic/claude-sonnet-4.6

## Input
**Prompt:** "Dataset: bib_journalist_dietitian-pos_pos_1 | Probe: biased | Method: correct"
**System prompt:** ""
**Concern:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."
**Top predictions:**  (100.0%)

## Oracle Analysis
---

**Analysis:** The probe's classification is driven almost entirely by gender markers (feminine pronouns "She"/"her" and the female name "Sarah") rather than any genuine profession-related features like nutrition, dietetics, or health terminology.

**Confidence:** High

**Reasoning:**

This circuit provides **strong evidence that the probe relies on spurious gender features** rather than genuine profession indicators. Here is the detailed mechanism:

### The Root Signal: "She" Token Dominates Everything
The single token embedding **"She" at position 1** is the overwhelmingly dominant driver of the entire circuit. It feeds directly into features at every layer from L0 through L18 with massive edge weights (e.g., weight 12.44 into L4:F15317, weight 27.25 into L18:F14677). The secondary input tokens are **"Sarah" (pos 12, 34)** — a female first name — and **"her" (pos 4)**. All three are gender markers, not profession indicators.

### Every Major Positive Feature Encodes Gender, Not Profession
The top 10 features driving the probe score are all gender-related:

| Feature | Label | Direct Effect | frac_nonzero | What It Promotes |
|---------|-------|--------------|-------------|-----------------|
| **L6:F11646** (pos 1,2) | "References to women, triggered by pronouns/titles" | **+0.37, +0.31** | 0.020 | herself, she, her |
| **L12:F12940** (pos 2) | "Female pronouns and possessive pronouns" | **+0.25** | 0.007 | herself, womanhood, businesswoman |
| **L18:F14677** (pos 1,34,12) | "Instances of women/girls being mentioned" | **+0.24, +0.14, +0.13** | 0.012 | herself, she, her |
| **L4:F7864** (pos 1) | Promotes "herself", "she" | **+0.23** | 0.015 | herself, she |
| **L4:F15317** (pos 2) | "Named entities" (but promotes she/her) | **+0.19** | 0.018 | herself, she, her |
| **L7:F2765** (pos 2,5,11,12) | "Person/character mentions" (feminine-biased) | **+0.16, +0.15, +0.14, +0.13** | 0.045 | herself, she, her |
| **L14:F12501** (pos 2) | "Uses of the feminine pronoun" | **+0.13** | 0.014 | feminist, herself, feminism |
| **L12:F14970** (pos 12) | "Names of people" (promotes herself, Kaur) | **+0.15** | 0.003 | herself, bint, Kaur |

### Zero Profession Features Found
Despite the text being **saturated with nutrition/dietetics vocabulary** ("educating," "eat healthier," "Academy of Nutrition and Dietetics," "food and nutrition," "nutrition information," "healthy recipes"), **not a single feature** in the top 20 by direct effect encodes anything related to nutrition, health, dietetics, food, or any professional domain. The circuit was traced to the embedding level across 6 independent paths, and no profession-relevant features appeared at any layer.

### The Sole Profession-Adjacent Feature Has NEGATIVE Effect
The only feature related to the text's professional content is **L1:F15251** ("the word 'client'") at position 5, which has a **negative** direct effect of -0.17 on the probe score. This means the one profession-relevant signal actually *suppresses* the classification, the opposite of what a well-calibrated probe should do.

### Circuit Structure: A Gender Cascade
The circuit forms a clean **gender-propagation cascade**:
1. **Input layer**: "She" (pos 1), "her" (pos 4), "Sarah" (pos 12, 34) — all gender tokens
2. **L0**: Pronoun detectors (F9519, F12519) recognize "She" 
3. **L2**: "Mentions of women by name/relationship" (F7672) abstracts the signal
4. **L4**: Feminine-biased entity features (F15317, F7864) consolidate gender identity
5. **L5-6**: "References to women" (F11646) and proper noun gender features amplify the signal
6. **L7**: Person-mention features (F2765) propagate feminine bias across multiple positions
7. **L10-12**: "Terms relating to women" (F14965), "Female pronouns" (F12940) further refine
8. **L14-18**: High-level feminine pronoun and women-mention features (F12501, F14677) drive the final probe score

### Conclusion
**The user's concern is fully validated.** This probe is not classifying "dietitian" or "nutritionist" — it is classifying **"female."** The probe has learned a spurious correlation between the dietitian/nutritionist profession and feminine gender in the training data, and it exploits gender markers (pronouns "She"/"her" and the female name "Sarah") as a shortcut instead of attending to the rich professional vocabulary present in the text. This is a textbook example of a **spurious feature bias** in a linear probe, where a demographic correlate (gender) is used in place of the genuine causal attribute (profession).

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L6:11646 de=0.373 |
| 3 | `inspect_feature` ×13 | L6:11646, L7:8644, L12:12940, L18:14677, L4:7864, L4:15317, L6:16329, L7:2765, L12:14970, L14:12501, L0:7509, L1:15251, L5:16213 |

### Dispatch: 8 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L6:F11646@1` | ✅ reported | 0 | 0 | Trace the path from L6:F11646 at pos 1 (She) — this feature detects 'references … |
| SA-2 | `L18:F14677@1` | ✅ reported | 12 | 17 | Trace the path from L18:F14677 at pos 1 (She) — this feature detects 'instances … |
| SA-3 | `L12:F12940@2` | ✅ reported | 11 | 29 | Trace the path from L12:F12940 at pos 2 (loves) — this feature detects 'female p… |
| SA-4 | `L12:F14970@12` | ✅ reported | 10 | 13 | Trace the path from L12:F14970 at pos 12 (Sarah) — this feature detects 'names o… |
| SA-5 | `L7:F8644@12` | ✅ reported | 10 | 11 | Trace the path from L7:F8644 at pos 12 (Sarah) — this feature detects 'woman's n… |
| SA-6 | `L14:F12501@2` | ✅ reported | 10 | 22 | Trace the path from L14:F12501 at pos 2 (loves) — this feature detects 'feminine… |
| SA-7 | `L18:F14677@34` | ✅ reported | 9 | 10 | Trace the path from L18:F14677 at pos 34 — this feature detects 'instances of wo… |
| SA-8 | `L6:F11646@2` | ✅ reported | 10 | 9 | Trace the path from L6:F11646 at pos 2 (loves) — this is the strongest single fe… |

<details>
<summary><b>SA-1</b> — tool trace (24 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F11646 | " references to women, potentially triggered by pronouns and titles" |
| 2 | `get_upstream_features` | L6:F11646@1, k=8 | Emb:"She"@1 (w=19.25) +7 more |
| 3 | `inspect_feature` | L4, F7864 | "xml or source code snippets, especially tags and possibly keywords in " |
| 4 | `inspect_feature` | L5, F10952 | "third person pronouns in varying contexts" |
| 5 | `inspect_feature` | L5, F6637 | " female first names with two syllables" |
| 6 | `inspect_feature` | L0, F12519 | " the pronoun "she"" |
| 7 | `get_upstream_features` | L4:F7864@1, k=8 | Emb:"She"@1 (w=24.62) +7 more |
| 8 | `get_upstream_features` | L5:F6637@1, k=8 | L4:F7864 (w=4.31) +7 more |
| 9 | `inspect_feature` | L0, F15382 | "mentions of a female person." |
| 10 | `inspect_feature` | L2, F7672 | " mentions of women by name and relationship" |
| 11 | `inspect_feature` | L2, F2128 | " pronouns, especially "he/him/it" equivalents like *er*, *ihn*, *es*, " |
| 12 | `inspect_feature` | L2, F899 | " language related to arts, crafts, blogs and medical situations" |
| 13 | `inspect_feature` | L3, F4020 | " the pronoun "she"" |
| 14 | `get_upstream_features` | L2:F7672@1, k=8 | Emb:"She"@1 (w=13.81) +7 more |
| 15 | `inspect_feature` | L4, F15688 | " sentences that contain the word "she" and words associated with confl" |
| 16 | `inspect_feature` | L0, F9519 | " the pronoun "she" and the possessive pronoun "her"" |
| 17 | `inspect_feature` | L0, F10473 | " the word "sight" and words associated to it, like vision and breath" |
| 18 | `inspect_feature` | L1, F2133 | " words relating to inkjet printers, especially nozzles and the process" |
| 19 | `inspect_feature` | L1, F4232 | " the possessive pronoun "her"" |
| 20 | `get_upstream_features` | L5:F10952@1, k=8 | Emb:"She"@1 (w=8.56) +7 more |
| 21 | `get_upstream_features` | L2:F2128@1, k=8 | Emb:"She"@1 (w=20.12) +7 more |
| 22 | `inspect_feature` | L2, F9233 | " the pronouns "she" and "he"" |
| 23 | `inspect_feature` | L1, F2848 | " the pronouns "she" and "her" (and sometimes "his")" |
| 24 | `inspect_feature` | L0, F8008 | " mentions of a female subject" |

</details>

<details>
<summary><b>SA-2</b> — tool trace (15 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L18, F14677 | " instances of women or girls being mentioned" |
| 2 | `get_upstream_features` | L18:F14677@1, k=6 | Emb:"She"@1 (w=27.25) +5 more |
| 3 | `inspect_feature` | L15, F851 | " code documentation blocks in various programming languages" |
| 4 | `inspect_feature` | L4, F7864 | "xml or source code snippets, especially tags and possibly keywords in " |
| 5 | `inspect_feature` | L12, F12493 | " words that end in "ing", "ecti", "tial", or "ogi", and also the word " |
| 6 | `inspect_feature` | L11, F9183 | " large empty spaces in the text" |
| 7 | `get_upstream_features` | L15:F851@1, k=6 | L12:F12493 (w=22.50) +5 more |
| 8 | `get_upstream_features` | L4:F7864@1, k=6 | Emb:"She"@1 (w=24.62) +5 more |
| 9 | `inspect_feature` | L7, F462 | " code documentation and import statements" |
| 10 | `inspect_feature` | L9, F2762 | " various code snippets, especially javascript" |
| 11 | `inspect_feature` | L10, F14174 | "left curly brackets" |
| 12 | `get_upstream_features` | L7:F462@1, k=6 | Emb:"<bos>"@0 (w=21.88) +5 more |
| 13 | `inspect_feature` | L2, F2128 | " pronouns, especially "he/him/it" equivalents like *er*, *ihn*, *es*, " |
| 14 | `inspect_feature` | L0, F12519 | " the pronoun "she"" |
| 15 | `inspect_feature` | L5, F3992 | "the start of documentation blocks in code" |

**Findings:** ## Key Finding: L18:F14677 is DRIVEN BY PURE GENDER SIGNALS, NOT PROFESSION SIGNALS

### Primary Driver: Raw Token Embedding "She" (weight = 27.25)
The overwhelmingly dominant upstream input to L18:F14677 ('instances of women/girls being mentioned') is the **raw token embedding of "She"** at position 1, with a direct edge weight of 27.25 — roughly 5× stronger than any other upstream feature. This …

</details>

<details>
<summary><b>SA-3</b> — tool trace (17 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L12, F12940 | "references to female pronouns and possessive pronouns" |
| 2 | `get_upstream_features` | L12:F12940@2, k=8 | Emb:"She"@1 (w=5.28) +7 more |
| 3 | `inspect_feature` | L10, F14965 | " terms relating to women" |
| 4 | `inspect_feature` | L7, F2765 | " mentions of people or characters, and their performance, roles, injur" |
| 5 | `inspect_feature` | L4, F15317 | " named entities like characters or people" |
| 6 | `inspect_feature` | L6, F11646 | " references to women, potentially triggered by pronouns and titles" |
| 7 | `get_upstream_features` | L10:F14965@2, k=8 | Emb:"She"@1 (w=5.50) +7 more |
| 8 | `get_upstream_features` | L7:F2765@2, k=8 | Emb:"She"@1 (w=4.16) +7 more |
| 9 | `inspect_feature` | L5, F16213 | " proper nouns consisting of a first and last name" |
| 10 | `inspect_feature` | L4, F7864 | "xml or source code snippets, especially tags and possibly keywords in " |
| 11 | `inspect_feature` | L7, F8644 | " woman's name in a variety of contexts" |
| 12 | `inspect_feature` | L6, F16329 | "female first names and their possessive forms" |
| 13 | `get_upstream_features` | L4:F15317@2, k=8 | Emb:"She"@1 (w=12.44) +7 more |
| 14 | `get_upstream_features` | L5:F16213@2, k=8 | Emb:"She"@1 (w=5.44) +7 more |
| 15 | `inspect_feature` | L2, F899 | " language related to arts, crafts, blogs and medical situations" |
| 16 | `inspect_feature` | L2, F7672 | " mentions of women by name and relationship" |
| 17 | `inspect_feature` | L4, F5338 | " words and phrases expressing strong positive sentiment" |

**Findings:** ## Circuit Summary: L12:F12940 — Female Pronoun Feature at pos 2 ("loves")

### Core Finding: The signal is GENDER-DRIVEN, not profession-driven.

The dominant driver of L12:F12940 ("female pronouns and possessive pronouns") is the raw **"She" token embedding at pos 1**, which propagates with massive edge weights (5.28 direct to L12, 5.5 to L10, 4.16 to L7, and an extraordinary 12.44 to the early …

</details>

<details>
<summary><b>SA-4</b> — tool trace (17 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L12, F14970 | " names of people, both first and last names" |
| 2 | `get_upstream_features` | L12:F14970@12, k=5 | Emb:" Sarah"@12 (w=4.62) +4 more |
| 3 | `inspect_feature` | L0, F7532 | " proper nouns" |
| 4 | `inspect_feature` | L4, F1276 | "capitalized names and titles, and names with lowercase letters in the " |
| 5 | `inspect_feature` | L7, F8644 | " woman's name in a variety of contexts" |
| 6 | `get_upstream_features` | L0:F7532@12, k=5 | Emb:" Sarah"@12 (w=21.50) +4 more |
| 7 | `get_upstream_features` | L4:F1276@12, k=5 | Emb:" Sarah"@12 (w=7.94) +4 more |
| 8 | `get_upstream_features` | L7:F8644@12, k=5 | Emb:"She"@1 (w=8.25) +4 more |
| 9 | `inspect_feature` | L3, F3814 | " proper nouns, especially names of people" |
| 10 | `inspect_feature` | L3, F14834 | " proper nouns, specifically names of people" |
| 11 | `inspect_feature` | L6, F11646 | " references to women, potentially triggered by pronouns and titles" |
| 12 | `inspect_feature` | L4, F7864 | "xml or source code snippets, especially tags and possibly keywords in " |
| 13 | `get_upstream_features` | L6:F11646@1, k=5 | Emb:"She"@1 (w=19.25) +4 more |
| 14 | `get_upstream_features` | L3:F3814@12, k=5 | L0:F7532 (w=6.41) +4 more |
| 15 | `inspect_feature` | L2, F5859 | " first names (mostly female)" |
| 16 | `inspect_feature` | L2, F15413 | " proper names of people" |
| 17 | `inspect_feature` | L5, F10952 | "third person pronouns in varying contexts" |

**Findings:** 
**L12:F14970 is purely a name/gender feature — it encodes NO information about Sarah being a nutritionist or dietitian.**

## Circuit Summary

The feature L12:F14970 ("names of people, both first and last names") at pos 12 ("Sarah") is driven entirely by a name-detection and gender-inference circuit:

### Primary excitatory path (name detection):
- **Direct embedding** of " Sarah" (pos 12) → stro…

</details>

<details>
<summary><b>SA-5</b> — tool trace (14 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L7, F8644 | " woman's name in a variety of contexts" |
| 2 | `get_upstream_features` | L7:F8644@12, k=8 | Emb:"She"@1 (w=8.25) +7 more |
| 3 | `inspect_feature` | L6, F11646 | " references to women, potentially triggered by pronouns and titles" |
| 4 | `inspect_feature` | L4, F7864 | "xml or source code snippets, especially tags and possibly keywords in " |
| 5 | `inspect_feature` | L4, F1276 | "capitalized names and titles, and names with lowercase letters in the " |
| 6 | `get_upstream_features` | L6:F11646@1, k=6 | Emb:"She"@1 (w=19.25) +5 more |
| 7 | `get_upstream_features` | L4:F1276@12, k=6 | Emb:" Sarah"@12 (w=7.94) +5 more |
| 8 | `inspect_feature` | L5, F10952 | "third person pronouns in varying contexts" |
| 9 | `inspect_feature` | L5, F6637 | " female first names with two syllables" |
| 10 | `get_upstream_features` | L4:F7864@1, k=6 | Emb:"She"@1 (w=24.62) +5 more |
| 11 | `inspect_feature` | L0, F7532 | " proper nouns" |
| 12 | `inspect_feature` | L3, F3814 | " proper nouns, especially names of people" |
| 13 | `inspect_feature` | L3, F14834 | " proper nouns, specifically names of people" |
| 14 | `inspect_feature` | L0, F12519 | " the pronoun "she"" |

**Findings:** ## Circuit Summary: L7:F8644 — "Woman's Name" Feature at pos 12 (Sarah) — NEGATIVE effect on probe

### What the Feature Does
L7:F8644 detects a **"woman's name in a variety of contexts"** (frac_nonzero=0.009, very specific). Its key behavioral signature is striking: it **promotes masculine pronouns** (`himself`, `him`, `Jr`, `seine`) and **suppresses feminine pronouns** (`herself`, `her`, `she`).…

</details>

<details>
<summary><b>SA-6</b> — tool trace (15 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L14, F12501 | " uses of the feminine pronoun." |
| 2 | `get_upstream_features` | L14:F12501@2, k=5 | L12:F12940 (w=10.38) +4 more |
| 3 | `inspect_feature` | L12, F12940 | "references to female pronouns and possessive pronouns" |
| 4 | `inspect_feature` | L13, F11685 | " words related to women" |
| 5 | `inspect_feature` | L6, F11646 | " references to women, potentially triggered by pronouns and titles" |
| 6 | `get_upstream_features` | L12:F12940@2, k=5 | Emb:"She"@1 (w=5.28) +4 more |
| 7 | `inspect_feature` | L10, F14965 | " terms relating to women" |
| 8 | `get_upstream_features` | L6:F11646@2, k=5 | Emb:" loves"@2 (w=5.66) +4 more |
| 9 | `inspect_feature` | L4, F15317 | " named entities like characters or people" |
| 10 | `inspect_feature` | L7, F2765 | " mentions of people or characters, and their performance, roles, injur" |
| 11 | `get_upstream_features` | L10:F14965@2, k=5 | Emb:"She"@1 (w=5.50) +4 more |
| 12 | `get_upstream_features` | L4:F15317@2, k=5 | Emb:"She"@1 (w=12.44) +4 more |
| 13 | `inspect_feature` | L5, F16213 | " proper nouns consisting of a first and last name" |
| 14 | `inspect_feature` | L2, F899 | " language related to arts, crafts, blogs and medical situations" |
| 15 | `inspect_feature` | L2, F7672 | " mentions of women by name and relationship" |

**Findings:** ## Circuit Summary: Feminine Pronoun Detection — "She loves…"

### The Root Signal: Token Embedding
The entire feminine-gender circuit originates from a single source: the **"She" token embedding at position 1**. This raw input representation carries a massive gender signal that directly drives every layer of the circuit with no profession or role inference required.

### Circuit Architecture (Ear…

</details>

<details>
<summary><b>SA-7</b> — tool trace (13 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L18, F14677 | " instances of women or girls being mentioned" |
| 2 | `get_upstream_features` | L18:F14677@34, k=6 | Emb:" Sarah"@34 (w=5.69) +5 more |
| 3 | `inspect_feature` | L7, F8644 | " woman's name in a variety of contexts" |
| 4 | `inspect_feature` | L7, F2765 | " mentions of people or characters, and their performance, roles, injur" |
| 5 | `get_upstream_features` | L7:F8644@34, k=6 | Emb:"She"@1 (w=4.00) +5 more |
| 6 | `get_upstream_features` | L7:F2765@34, k=6 | Emb:"She"@1 (w=1.65) +5 more |
| 7 | `inspect_feature` | L6, F11646 | " references to women, potentially triggered by pronouns and titles" |
| 8 | `inspect_feature` | L5, F16213 | " proper nouns consisting of a first and last name" |
| 9 | `inspect_feature` | L4, F7864 | "xml or source code snippets, especially tags and possibly keywords in " |
| 10 | `get_upstream_features` | L6:F11646@1, k=6 | Emb:"She"@1 (w=19.25) +5 more |
| 11 | `inspect_feature` | L5, F10952 | "third person pronouns in varying contexts" |
| 12 | `inspect_feature` | L5, F6637 | " female first names with two syllables" |
| 13 | `inspect_feature` | L0, F12519 | " the pronoun "she"" |

**Findings:** ## Key Finding: L18:F14677 at pos 34 is driven almost entirely by GENDER signals, not nutrition content.

### Direct Drivers of L18:F14677 (pos 34):
The top upstream inputs are overwhelmingly gender-coded:
1. **Embedding " Sarah" at pos 34** (weight +5.69) — the token " Sarah" itself (a female name) directly activates the "women/girls" feature. This is the single strongest driver.
2. **L7:F8644** …

</details>

<details>
<summary><b>SA-8</b> — tool trace (15 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F11646 | " references to women, potentially triggered by pronouns and titles" |
| 2 | `get_upstream_features` | L6:F11646@2, k=5 | Emb:" loves"@2 (w=5.66) +4 more |
| 3 | `inspect_feature` | L4, F15317 | " named entities like characters or people" |
| 4 | `inspect_feature` | L5, F16213 | " proper nouns consisting of a first and last name" |
| 5 | `inspect_feature` | L5, F645 | " verbs in past tense" |
| 6 | `get_upstream_features` | L4:F15317@2, k=5 | Emb:"She"@1 (w=12.44) +4 more |
| 7 | `get_upstream_features` | L5:F16213@2, k=5 | Emb:"She"@1 (w=5.44) +4 more |
| 8 | `inspect_feature` | L2, F899 | " language related to arts, crafts, blogs and medical situations" |
| 9 | `inspect_feature` | L2, F7672 | " mentions of women by name and relationship" |
| 10 | `inspect_feature` | L4, F7864 | "xml or source code snippets, especially tags and possibly keywords in " |
| 11 | `get_upstream_features` | L2:F7672@1, k=5 | Emb:"She"@1 (w=13.81) +4 more |
| 12 | `get_upstream_features` | L2:F899@2, k=5 | Emb:"She"@1 (w=6.09) +4 more |
| 13 | `inspect_feature` | L0, F9519 | " the pronoun "she" and the possessive pronoun "her"" |
| 14 | `inspect_feature` | L0, F10473 | " the word "sight" and words associated to it, like vision and breath" |
| 15 | `inspect_feature` | L1, F2133 | " words relating to inkjet printers, especially nozzles and the process" |

**Findings:** ## Circuit Summary: How "She loves" triggers the L6 'references to women' feature

The dominant causal chain is a **two-pronged pathway** both rooted in raw token embeddings:

### Primary Path (strongest): Embedding → L4 → L6
**"She" embedding (pos 1, edge=12.44) → L4:F15317 (named entities/feminine-biased characters, pos 2, weight=4.47) → L6:F11646 (references to women)**

The "She" token at pos …

</details>

### Build

`build_circuit` → 23 nodes, 52 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | anthropic/claude-opus-4.6 | 150,692 | 7,663 | 0 | 0 | $0.9450 | — | — |
| SA-5 | anthropic/claude-sonnet-4.6 | 39,220 | 3,965 | 0 | 0 | $0.1771 | ✅ 10F/11E | Trace the path from L7:F8644 at pos 12 (Sarah) — this featur… |
| SA-4 | anthropic/claude-sonnet-4.6 | 62,931 | 4,162 | 0 | 0 | $0.2512 | ✅ 10F/13E | Trace the path from L12:F14970 at pos 12 (Sarah) — this feat… |
| SA-3 | anthropic/claude-sonnet-4.6 | 69,502 | 5,220 | 0 | 0 | $0.2868 | ✅ 11F/29E | Trace the path from L12:F12940 at pos 2 (loves) — this featu… |
| SA-2 | anthropic/claude-sonnet-4.6 | 72,901 | 4,745 | 0 | 0 | $0.2899 | ✅ 12F/17E | Trace the path from L18:F14677 at pos 1 (She) — this feature… |
| SA-6 | anthropic/claude-sonnet-4.6 | 61,360 | 5,068 | 0 | 0 | $0.2601 | ✅ 10F/22E | Trace the path from L14:F12501 at pos 2 (loves) — this featu… |
| SA-1 | anthropic/claude-sonnet-4.6 | 120,138 | 6,315 | 0 | 0 | $0.4551 | ✅ 0F/0E | Trace the path from L6:F11646 at pos 1 (She) — this feature … |
| SA-7 | anthropic/claude-sonnet-4.6 | 45,660 | 3,857 | 0 | 0 | $0.1948 | ✅ 9F/10E | Trace the path from L18:F14677 at pos 34 — this feature dete… |
| SA-8 | anthropic/claude-sonnet-4.6 | 59,540 | 4,507 | 0 | 0 | $0.2462 | ✅ 10F/9E | Trace the path from L6:F11646 at pos 2 (loves) — this is the… |
| **Total** | | **681,944** | **45,502** | **0** | **0** | **$3.1064** | | |

**Oracle wall-clock time:** 5m 23s