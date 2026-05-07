# Circuit Oracle Report
**Date:** 2026-03-30 19:12:54 UTC | **Orchestrator:** minimax/minimax-m2.7 | **Subagent:** deepseek/deepseek-v3.2

## Input
**Prompt:** "Dataset: bib_journalist_dietitian-pos_pos_1 | Probe: biased | Method: correct"
**System prompt:** ""
**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."
**Top predictions:**  (100.0%)

## Oracle Analysis
**Analysis:** The probe's classification score is driven almost entirely by a spurious gender-marker circuit rather than genuine profession indicators. The strongest features (L6:F11646, L12:F12940, L18:F14677) all encode "references to women" or "female pronouns," with the primary signal originating from the raw embedding of the word "She" at position 1 (edge weights 19-27). No features encoding profession-specific knowledge (nutritionist, dietitian, RD, nutrition, food, health) were found in the top attribution paths.

**Confidence:** 9/10

**Reasoning:** The circuit tracing reveals a clear gender-detection pathway from the "She" token through early-layer pronoun detectors (L0:F12519, L2:F2128, L2:F8966) to intermediate features that combine gender and entity information (L4:F15317 labeled "named entities" but promoting "herself", "she", "her"), culminating in late-layer features encoding female references (L6:F11646: "references to women, potentially triggered by pronouns and titles" with frac_nonzero=0.01976; L12:F12940: "references to female pronouns" with frac_nonzero=0.0065; L18:F14677: "instances of women or girls being mentioned" with frac_nonzero=0.01225).

The "She" embedding at position 1 has direct connections to multiple late-layer features with weights 19-27, making it the dominant signal driver. The verb "loves" at position 2 provides secondary support (weights 4-5.7) by co-occurring with the "She loves..." pattern in the training data.

The only negative contributions come from features that suppress female pronouns (L7:F8644 with "woman's name" suppressing female pronouns, weight -0.273; L0:F7509 "female pronouns" suppressor, weight -0.174) or detect unrelated content (code patterns).

Critically, the input text about a nutritionist contains rich profession-specific content (Academy of Nutrition and Dietetics, www.salubriousrd.com, "nutrition information", "healthy recipes") that is entirely ignored by the attribution circuit. The probe has learned to associate the female gender marker "She" with the target label, which is a textbook example of spurious correlation in machine learning.

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | ❌ Token 'Nutritionist' not found in top logits. Available: ['' |
| 3 | `get_top_features` | ❌ Token 'dietitian' not found in top logits. Available: [''] |
| 4 | `get_top_features` | ❌ Token 'she' not found in top logits. Available: [''] |
| 5 | `get_top_features` | ❌ Token 'blog' not found in top logits. Available: [''] |
| 6 | `get_top_features` | 15 features; top: L6:11646 de=0.373 |

### Dispatch: 7 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L6:F11646@1` | ✅ reported | 8 | 13 | Trace what L6:F11646 encodes and where the signal originates. Is this feature de… |
| SA-2 | `L6:F11646@2` | ✅ reported | 8 | 8 | Trace what L6:F11646 encodes at pos 2 and where the signal originates. Is this f… |
| SA-3 | `L7:F8644@12` | ✅ reported | 7 | 9 | Trace L7:F8644 at pos 12 (the strongest negative feature). What does this featur… |
| SA-4 | `L12:F12940@2` | ✅ reported | 10 | 25 | Trace L12:F12940 at pos 2. What does this feature encode? Is it gender-related o… |
| SA-5 | `L4:F15317@2` | ✅ reported | 9 | 16 | Trace L4:F15317 at pos 2 (named entities/people). Is this feature encoding gende… |
| SA-6 | `L0:F7509@4` | ✅ reported | 1 | 5 | Trace L0:F7509 at pos 4 (negative effect feature). What does this feature encode… |
| SA-7 | `L18:F14677@1` | ✅ reported | 11 | 14 | Trace L18:F14677 at pos 1 (strong positive feature at pos 1). What does this fea… |

<details>
<summary><b>SA-1</b> — tool trace (12 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F11646 | " references to women, potentially triggered by pronouns and titles" |
| 2 | `get_upstream_features` | L6:F11646@1, k=5 | Emb:"She"@1 (w=19.25) +4 more |
| 3 | `inspect_feature` | L4, F7864 | "xml or source code snippets, especially tags and possibly keywords in " |
| 4 | `inspect_feature` | L0, F12519 | " the pronoun "she"" |
| 5 | `inspect_feature` | L5, F10952 | "third person pronouns in varying contexts" |
| 6 | `get_upstream_features` | L4:F7864@1, k=5 | Emb:"She"@1 (w=24.62) +4 more |
| 7 | `inspect_feature` | L2, F2128 | " pronouns, especially "he/him/it" equivalents like *er*, *ihn*, *es*, " |
| 8 | `inspect_feature` | L2, F8966 | " the pronoun "she"" |
| 9 | `get_upstream_features` | L0:F12519@1, k=5 | Emb:"She"@1 (w=21.88) +4 more |
| 10 | `get_upstream_features` | L5:F10952@1, k=5 | Emb:"She"@1 (w=8.56) +4 more |
| 11 | `inspect_feature` | L2, F9233 | " the pronouns "she" and "he"" |
| 12 | `inspect_feature` | L2, F7672 | " mentions of women by name and relationship" |

**Findings:** L6:F11646 encodes "references to women, potentially triggered by pronouns and titles" with a relatively low frac_nonzero (0.01976), indicating it's specific rather than generic. The feature promotes tokens like "herself", "she", "her", and "Autorin" (German for female author).

The circuit reveals that:
1. The strongest signal comes DIRECTLY from the embedding of "She" (weight 19.25), showing this…

</details>

<details>
<summary><b>SA-2</b> — tool trace (12 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F11646 | " references to women, potentially triggered by pronouns and titles" |
| 2 | `get_upstream_features` | L6:F11646@2, k=5 | Emb:" loves"@2 (w=5.66) +4 more |
| 3 | `inspect_feature` | L4, F15317 | " named entities like characters or people" |
| 4 | `inspect_feature` | L5, F16213 | " proper nouns consisting of a first and last name" |
| 5 | `get_upstream_features` | L4:F15317@2, k=5 | Emb:"She"@1 (w=12.44) +4 more |
| 6 | `inspect_feature` | L2, F899 | " language related to arts, crafts, blogs and medical situations" |
| 7 | `inspect_feature` | L2, F7672 | " mentions of women by name and relationship" |
| 8 | `get_upstream_features` | L5:F16213@2, k=5 | Emb:"She"@1 (w=5.44) +4 more |
| 9 | `inspect_feature` | L4, F7864 | "xml or source code snippets, especially tags and possibly keywords in " |
| 10 | `inspect_feature` | L5, F645 | " verbs in past tense" |
| 11 | `get_upstream_features` | L2:F7672@1, k=5 | Emb:"She"@1 (w=13.81) +4 more |
| 12 | `inspect_feature` | L2, F12134 | " instances of the word "love" (and possibly words with similar meaning" |

**Findings:** The circuit tracing reveals that L6:F11646 at position 2 encodes gender markers, specifically detecting references to women. The feature is part of a circuit that processes feminine pronouns like "She" at position 1 and the verb "loves" at position 2.

Key findings:
1. The starting feature L6:F11646 detects references to women with promoted tokens including feminine pronouns ("herself", "she", "he…

</details>

<details>
<summary><b>SA-3</b> — tool trace (12 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L7, F8644 | " woman's name in a variety of contexts" |
| 2 | `get_upstream_features` | L7:F8644@12, k=5 | Emb:"She"@1 (w=8.25) +4 more |
| 3 | `inspect_feature` | L6, F11646 | " references to women, potentially triggered by pronouns and titles" |
| 4 | `inspect_feature` | L4, F7864 | "xml or source code snippets, especially tags and possibly keywords in " |
| 5 | `inspect_feature` | L4, F1276 | "capitalized names and titles, and names with lowercase letters in the " |
| 6 | `get_upstream_features` | L6:F11646@1, k=5 | Emb:"She"@1 (w=19.25) +4 more |
| 7 | `get_upstream_features` | L4:F7864@1, k=5 | Emb:"She"@1 (w=24.62) +4 more |
| 8 | `get_upstream_features` | L4:F1276@12, k=5 | Emb:" Sarah"@12 (w=7.94) +4 more |
| 9 | `inspect_feature` | L0, F12519 | " the pronoun "she"" |
| 10 | `inspect_feature` | L0, F7532 | " proper nouns" |
| 11 | `inspect_feature` | L5, F10952 | "third person pronouns in varying contexts" |
| 12 | `get_upstream_features` | L0:F7532@12, k=5 | Emb:" Sarah"@12 (w=21.50) +4 more |

**Findings:** L7:F8644 at position 12 encodes "woman's name in a variety of contexts" and shows suppression of female pronouns (herself, her, she) while promoting male pronouns (himself, him). The signal originates from two main sources:

1. From position 1: The pronoun "She" (embedding weight: 8.25) strongly activates L4:F7864 (xml/code snippets) which then feeds into L6:F11646 (references to women) and L7:F86…

</details>

<details>
<summary><b>SA-4</b> — tool trace (15 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L12, F12940 | "references to female pronouns and possessive pronouns" |
| 2 | `get_upstream_features` | L12:F12940@2, k=5 | Emb:"She"@1 (w=5.28) +4 more |
| 3 | `inspect_feature` | L10, F14965 | " terms relating to women" |
| 4 | `inspect_feature` | L7, F2765 | " mentions of people or characters, and their performance, roles, injur" |
| 5 | `inspect_feature` | L4, F15317 | " named entities like characters or people" |
| 6 | `get_upstream_features` | L10:F14965@2, k=5 | Emb:"She"@1 (w=5.50) +4 more |
| 7 | `inspect_feature` | L6, F11646 | " references to women, potentially triggered by pronouns and titles" |
| 8 | `get_upstream_features` | L4:F15317@2, k=5 | Emb:"She"@1 (w=12.44) +4 more |
| 9 | `inspect_feature` | L2, F899 | " language related to arts, crafts, blogs and medical situations" |
| 10 | `inspect_feature` | L2, F7672 | " mentions of women by name and relationship" |
| 11 | `get_upstream_features` | L7:F2765@2, k=5 | Emb:"She"@1 (w=4.16) +4 more |
| 12 | `inspect_feature` | L4, F7864 | "xml or source code snippets, especially tags and possibly keywords in " |
| 13 | `get_upstream_features` | L6:F11646@2, k=5 | Emb:" loves"@2 (w=5.66) +4 more |
| 14 | `inspect_feature` | L5, F16213 | " proper nouns consisting of a first and last name" |
| 15 | `inspect_feature` | L5, F645 | " verbs in past tense" |

**Findings:** The feature L12:F12940 clearly encodes gender-related information - specifically "references to female pronouns and possessive pronouns". This is a gender-related feature, not profession-related.

The circuit shows a clear pathway for detecting female pronouns:
1. The starting point L12:F12940 has low frac_nonzero (0.0065) indicating high specificity for female pronouns
2. It receives strong signa…

</details>

<details>
<summary><b>SA-5</b> — tool trace (13 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F15317 | " named entities like characters or people" |
| 2 | `get_upstream_features` | L4:F15317@2, k=5 | Emb:"She"@1 (w=12.44) +4 more |
| 3 | `inspect_feature` | L2, F899 | " language related to arts, crafts, blogs and medical situations" |
| 4 | `inspect_feature` | L2, F7672 | " mentions of women by name and relationship" |
| 5 | `inspect_feature` | L2, F12134 | " instances of the word "love" (and possibly words with similar meaning" |
| 6 | `get_upstream_features` | L2:F7672@1, k=5 | Emb:"She"@1 (w=13.81) +4 more |
| 7 | `get_upstream_features` | L2:F899@2, k=5 | Emb:"She"@1 (w=6.09) +4 more |
| 8 | `inspect_feature` | L0, F13484 | " the word "uses" and locations related to municipal government" |
| 9 | `inspect_feature` | L0, F12347 | "words related to mixing and liking as well as adjectives ending with "" |
| 10 | `inspect_feature` | L0, F8786 | " words related to the process of putting things together" |
| 11 | `inspect_feature` | L0, F9519 | " the pronoun "she" and the possessive pronoun "her"" |
| 12 | `inspect_feature` | L0, F10473 | " the word "sight" and words associated to it, like vision and breath" |
| 13 | `get_upstream_features` | L0:F9519@1, k=5 | Emb:"She"@1 (w=15.75) +4 more |

**Findings:** The feature L4:F15317, labeled "named entities like characters or people", is primarily encoding GENDER MARKERS rather than genuine profession/entity information. It strongly promotes feminine pronouns ("herself", "she", "her") and suppresses masculine pronouns. The circuit shows it's heavily influenced by the feminine pronoun "She" from the input, with a direct edge weight of 12.44 from the embed…

</details>

<details>
<summary><b>SA-6</b> — tool trace (3 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F7509 | " female pronouns and words like daughter and husband that refer to wom" |
| 2 | `get_upstream_features` | L0:F7509@4, k=5 | Emb:" her"@4 (w=42.50) +4 more |
| 3 | `get_upstream_features` | L0:F7509@4, k=10 | Emb:" her"@4 (w=42.50) +9 more |

**Findings:** The feature L0:F7509 at position 4 encodes detection of female pronouns, specifically suppressing "her" and similar female references. It has a very strong direct connection from the token embedding " her" at position 4 (edge weight 42.5), with weaker connections from surrounding context tokens. The feature's label confirms it detects "female pronouns and words like daughter and husband that refer…

</details>

<details>
<summary><b>SA-7</b> — tool trace (16 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L18, F14677 | " instances of women or girls being mentioned" |
| 2 | `get_upstream_features` | L18:F14677@1, k=5 | Emb:"She"@1 (w=27.25) +4 more |
| 3 | `inspect_feature` | L15, F851 | " code documentation blocks in various programming languages" |
| 4 | `inspect_feature` | L4, F7864 | "xml or source code snippets, especially tags and possibly keywords in " |
| 5 | `inspect_feature` | L12, F12493 | " words that end in "ing", "ecti", "tial", or "ogi", and also the word " |
| 6 | `get_upstream_features` | L4:F7864@1, k=5 | Emb:"She"@1 (w=24.62) +4 more |
| 7 | `inspect_feature` | L0, F12519 | " the pronoun "she"" |
| 8 | `inspect_feature` | L2, F2128 | " pronouns, especially "he/him/it" equivalents like *er*, *ihn*, *es*, " |
| 9 | `inspect_feature` | L2, F8966 | " the pronoun "she"" |
| 10 | `get_upstream_features` | L15:F851@1, k=5 | L12:F12493 (w=22.50) +4 more |
| 11 | `inspect_feature` | L9, F2762 | " various code snippets, especially javascript" |
| 12 | `inspect_feature` | L7, F462 | " code documentation and import statements" |
| 13 | `get_upstream_features` | L0:F12519@1, k=5 | Emb:"She"@1 (w=21.88) +4 more |
| 14 | `get_upstream_features` | L12:F12493@1, k=5 | L10:F14174 (w=15.31) +4 more |
| 15 | `inspect_feature` | L10, F14174 | "left curly brackets" |
| 16 | `inspect_feature` | L11, F9183 | " large empty spaces in the text" |

**Findings:** The circuit trace reveals that L18:F14677 at position 1 encodes gender information - specifically "instances of women or girls being mentioned". This is a gender-related feature, not profession-related. The feature promotes female pronouns ("herself", "she", "her") and suppresses male pronouns ("himself", "his", "his").

Key findings:
1. The feature receives strong direct input from the embedding …

</details>

### Build

`build_circuit` → 15 nodes, 24 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m2.7 | 26,474 | 4,565 | 68,514 | 0 | — | — | — |
| SA-3 | deepseek/deepseek-v3.2 | 70,459 | 3,086 | 12,352 | 0 | — | ✅ 7F/9E | Trace L7:F8644 at pos 12 (the strongest negative feature). W… |
| SA-1 | deepseek/deepseek-v3.2 | 77,226 | 3,318 | 8,960 | 0 | — | ✅ 8F/13E | Trace what L6:F11646 encodes and where the signal originates… |
| SA-2 | deepseek/deepseek-v3.2 | 85,174 | 3,592 | 2,304 | 0 | — | ✅ 8F/8E | Trace what L6:F11646 encodes at pos 2 and where the signal o… |
| SA-5 | deepseek/deepseek-v3.2 | 80,169 | 4,087 | 19,328 | 0 | — | ✅ 9F/16E | Trace L4:F15317 at pos 2 (named entities/people). Is this fe… |
| SA-4 | deepseek/deepseek-v3.2 | 115,532 | 5,274 | 11,392 | 0 | — | ✅ 10F/25E | Trace L12:F12940 at pos 2. What does this feature encode? Is… |
| SA-6 | deepseek/deepseek-v3.2 | 13,888 | 1,886 | 0 | 0 | — | ✅ 1F/5E | Trace L0:F7509 at pos 4 (negative effect feature). What does… |
| SA-7 | deepseek/deepseek-v3.2 | 110,425 | 4,667 | 34,048 | 0 | — | ✅ 11F/14E | Trace L18:F14677 at pos 1 (strong positive feature at pos 1)… |
| **Total** | | **579,347** | **30,475** | **156,898** | **0** | **—** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 10m 4s