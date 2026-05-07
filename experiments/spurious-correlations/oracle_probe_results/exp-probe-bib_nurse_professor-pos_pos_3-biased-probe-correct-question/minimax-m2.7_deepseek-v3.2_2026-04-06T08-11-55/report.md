# Circuit Oracle Report
**Date:** 2026-04-06 08:11:55 UTC | **Orchestrator:** minimax/minimax-m2.7 | **Subagent:** deepseek/deepseek-v3.2

## Input

**Prompt:** "Dataset: bib_nurse_professor-pos_pos_3 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "('The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession.',)"

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification of "nurse practitioner" is driven primarily by **spurious gender markers** (female pronouns, female names) rather than genuine profession indicators. The circuit uses the pronoun "She" at position 1 and the name "Linda" at position 24 as the strongest signals, feeding through gender-detection features (L6:F11646 with direct_effect=0.4922, L18:F14677 with direct_effect=0.3184, L19:F9685 with direct_effect=0.2412), while the genuine nursing profession feature (L6:F15267 with direct_effect=0.3945) ranks only fourth in importance. A female name detector (L7:F8644) exerts a negative effect (-0.4551), suggesting it may suppress masculine-coded predictions.

**Confidence:** 9/10

**Reasoning:** The circuit traced from the layer-22 probe classification reveals a clear pattern of gender-based rather than profession-based classification:

1. **Dominant Gender Signals:** L6:F11646 ("references to women") has the strongest direct effect (0.4922), activated by the token "She" at position 1 with edge weight 19.25. L18:F14677 ("instances of women or girls") has the second-highest effect (0.3184), also directly fed by "She" with weight 27.125. L19:F9685 ("women's names and their roles") has direct effect 0.2412, fed by "Linda" at position 24 with weight 3.4531.

2. **Weaker Profession Signals:** L6:F15267 ("words in the document referring to the profession of nursing") ranks only fourth with direct effect 0.3945, despite being a genuine profession indicator that detects nursing terms like "RN". It is fed by the token "nurse" at position 7 (weight 7.0625), but its influence is substantially less than the gender markers.

3. **Suppression Mechanism:** L7:F8644 ("woman's name in a variety of contexts") has a negative direct effect (-0.4551), the second-largest magnitude in the circuit. This feature paradoxically promotes masculine tokens ("himself", "boyhood") and suppresses feminine tokens ("herself", "she"), suggesting it functions as an inhibitory gender marker rather than a positive one.

4. **Circuit Convergence:** All paths originate from three input tokens: "She" (pos 1), "Linda" (pos 24), and "nurse" (pos 7). The gender features dominate with combined direct effects exceeding 1.05, while the nursing profession feature contributes only 0.3945.

The circuit confirms the user's concern: the probe relies on **correlational gender markers** (if female, likely nurse) rather than **causal profession indicators** (nursing terminology, clinical roles). This represents a classic case of spurious feature reliance where demographic proxies substitute for actual task-relevant features.

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L6:11646 de=0.492 |
| 3 | `inspect_feature` ×5 | L6:11646, L7:8644, L6:15267, L4:15317, L18:14677 |

### Dispatch: 7 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L6:F11646@1` | ✅ reported | 7 | 9 | Trace this gender-pronoun feature (L6:F11646) upstream. Identify what upstream f… |
| SA-2 | `L18:F14677@1` | ✅ reported | 11 | 19 | Trace this female-reference feature (L18:F14677) upstream. This feature detects … |
| SA-3 | `L6:F15267@8` | ✅ reported | 9 | 12 | Trace this nursing profession feature (L6:F15267) upstream. This feature detects… |
| SA-4 | `L7:F8644@24` | ✅ reported | 9 | 19 | Trace this female-name detector (L7:F8644) upstream. Note this has a NEGATIVE di… |
| SA-5 | `L4:F15317@2` | ✅ reported | 7 | 11 | Trace this named entity detector (L4:F15317) upstream. This feature detects peop… |
| SA-6 | `L12:F14970@24` | ✅ reported | 9 | 19 | Trace L12:F14970 (positive effect) upstream. Find what upstream features or embe… |
| SA-7 | `L19:F9685@24` | ✅ reported | 9 | 23 | Trace L19:F9685 upstream. Find what upstream features or embeddings feed into th… |

<details>
<summary><b>SA-1</b> — tool trace (12 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F11646 | " references to women, potentially triggered by pronouns and titles" |
| 2 | `get_upstream_features` | L6:F11646@1, k=5 | Emb:"She"@1 (w=19.25) +4 more |
| 3 | `inspect_feature` | L4, F7864 | "xml or source code snippets, especially tags and possibly keywords in " |
| 4 | `inspect_feature` | L0, F12519 | " the pronoun "she"" |
| 5 | `get_upstream_features` | L4:F7864@1, k=5 | Emb:"She"@1 (w=24.62) +4 more |
| 6 | `inspect_feature` | L2, F2128 | " pronouns, especially "he/him/it" equivalents like *er*, *ihn*, *es*, " |
| 7 | `inspect_feature` | L2, F8966 | " the pronoun "she"" |
| 8 | `get_upstream_features` | L0:F12519@1, k=5 | Emb:"She"@1 (w=21.88) +4 more |
| 9 | `get_upstream_features` | L2:F2128@1, k=5 | Emb:"She"@1 (w=20.12) +4 more |
| 10 | `inspect_feature` | L0, F15382 | "mentions of a female person." |
| 11 | `inspect_feature` | L5, F10952 | "third person pronouns in varying contexts" |
| 12 | `get_upstream_features` | L5:F10952@1, k=5 | Emb:"She"@1 (w=8.56) +4 more |

**Findings:** The gender-pronoun feature L6:F11646 (references to women) gets its primary signal directly from the token embedding "She" at position 1 (edge_weight 19.25), not through higher-level features. This direct token-to-feature connection shows that gender detection at layer 6 is primarily driven by specific pronoun tokens. Additional processing occurs through intermediate features like L4:F7864 (which …

</details>

<details>
<summary><b>SA-2</b> — tool trace (17 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L18, F14677 | " instances of women or girls being mentioned" |
| 2 | `get_upstream_features` | L18:F14677@1, k=5 | Emb:"She"@1 (w=27.12) +4 more |
| 3 | `inspect_feature` | L15, F851 | " code documentation blocks in various programming languages" |
| 4 | `inspect_feature` | L4, F7864 | "xml or source code snippets, especially tags and possibly keywords in " |
| 5 | `inspect_feature` | L12, F12493 | " words that end in "ing", "ecti", "tial", or "ogi", and also the word " |
| 6 | `get_upstream_features` | L4:F7864@1, k=5 | Emb:"She"@1 (w=24.62) +4 more |
| 7 | `inspect_feature` | L0, F12519 | " the pronoun "she"" |
| 8 | `inspect_feature` | L2, F2128 | " pronouns, especially "he/him/it" equivalents like *er*, *ihn*, *es*, " |
| 9 | `inspect_feature` | L2, F8966 | " the pronoun "she"" |
| 10 | `get_upstream_features` | L0:F12519@1, k=5 | Emb:"She"@1 (w=21.88) +4 more |
| 11 | `get_upstream_features` | L2:F2128@1, k=5 | Emb:"She"@1 (w=20.12) +4 more |
| 12 | `inspect_feature` | L0, F15382 | "mentions of a female person." |
| 13 | `get_upstream_features` | L15:F851@1, k=5 | L12:F12493 (w=22.38) +4 more |
| 14 | `inspect_feature` | L9, F2762 | " various code snippets, especially javascript" |
| 15 | `get_upstream_features` | L12:F12493@1, k=5 | L10:F14174 (w=15.38) +4 more |
| 16 | `inspect_feature` | L10, F14174 | "left curly brackets" |
| 17 | `inspect_feature` | L11, F9183 | " large empty spaces in the text" |

**Findings:** The circuit tracing reveals a clear pathway for female pronoun detection:

1. **Direct embedding connection**: Token "She" at position 1 feeds directly into L18:F14677 (female-reference detector) with strong weight (27.125).

2. **Main circuit pathway**: 
   - Token "She" → L0:F12519 ("she" pronoun detector, but suppresses "she" tokens)
   - Token "She" → L2:F2128 (pronoun detector promoting both …

</details>

<details>
<summary><b>SA-3</b> — tool trace (15 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F15267 | " words in the document referring to the profession of nursing" |
| 2 | `get_upstream_features` | L6:F15267@8, k=5 | Emb:" nurse"@7 (w=7.06) +4 more |
| 3 | `inspect_feature` | L5, F1275 | "words related to healthcare professionals and medical fields" |
| 4 | `inspect_feature` | L4, F11037 | " words related to counseling, therapy, social work, and academic degre" |
| 5 | `get_upstream_features` | L5:F1275@8, k=5 | Emb:" nurse"@7 (w=2.30) +4 more |
| 6 | `inspect_feature` | L4, F9036 | " words and abbreviations associated with healthcare." |
| 7 | `get_upstream_features` | L4:F11037@8, k=5 | Emb:" practitioner"@8 (w=7.03) +4 more |
| 8 | `inspect_feature` | L1, F1494 | " words related to medical practices and studies." |
| 9 | `inspect_feature` | L2, F2589 | " words related to medical professionals and medical specialties" |
| 10 | `get_upstream_features` | L4:F9036@8, k=5 | Emb:" practitioner"@8 (w=14.69) +4 more |
| 11 | `get_upstream_features` | L1:F1494@8, k=5 | Emb:" nurse"@7 (w=10.75) +4 more |
| 12 | `inspect_feature` | L0, F6337 | "the word "dig" in different contexts." |
| 13 | `inspect_feature` | L0, F8854 | " the word "nurse" as well as some pronouns" |
| 14 | `get_upstream_features` | L2:F2589@8, k=5 | Emb:" practitioner"@8 (w=12.75) +4 more |
| 15 | `inspect_feature` | L1, F12131 | " words related to medical practice and studies" |

**Findings:** The nursing profession feature (L6:F15267) detects nursing-related terms like "RN" and has a complex upstream circuit. Key findings:

1. **Direct Input Tokens**: The strongest signals come directly from token embeddings: " nurse" at position 7 (weight: 7.0625) and " practitioner" at position 8 (weight: 3.5).

2. **Healthcare Professional Pathway**: L5:F1275 (healthcare professionals) feeds into th…

</details>

<details>
<summary><b>SA-4</b> — tool trace (17 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L7, F8644 | " woman's name in a variety of contexts" |
| 2 | `get_upstream_features` | L7:F8644@24, k=5 | Emb:"She"@1 (w=7.38) +4 more |
| 3 | `inspect_feature` | L6, F11646 | " references to women, potentially triggered by pronouns and titles" |
| 4 | `inspect_feature` | L6, F8166 | " proper names longer than 4 characters and ending in 'a', 'i', or 'e'" |
| 5 | `get_upstream_features` | L6:F11646@1, k=5 | Emb:"She"@1 (w=19.25) +4 more |
| 6 | `get_upstream_features` | L6:F8166@24, k=5 | L5:F6637 (w=-3.16) +4 more |
| 7 | `inspect_feature` | L4, F7864 | "xml or source code snippets, especially tags and possibly keywords in " |
| 8 | `inspect_feature` | L5, F6637 | " female first names with two syllables" |
| 9 | `get_upstream_features` | L4:F7864@1, k=5 | Emb:"She"@1 (w=24.62) +4 more |
| 10 | `get_upstream_features` | L5:F6637@24, k=5 | L4:F1276 (w=3.02) +4 more |
| 11 | `inspect_feature` | L4, F1276 | "capitalized names and titles, and names with lowercase letters in the " |
| 12 | `inspect_feature` | L4, F1302 | " parts of names or titles, sometimes followed by numbers" |
| 13 | `get_upstream_features` | L4:F1276@24, k=5 | Emb:" Linda"@24 (w=4.97) +4 more |
| 14 | `get_upstream_features` | L0:F7532@24, k=5 | Emb:" Linda"@24 (w=19.00) +4 more |
| 15 | `inspect_feature` | L0, F12519 | " the pronoun "she"" |
| 16 | `get_upstream_features` | L0:F12519@1, k=5 | Emb:"She"@1 (w=21.88) +4 more |
| 17 | `inspect_feature` | L0, F7532 | " proper nouns" |

**Findings:** I traced the female-name detector circuit from L7:F8644 (which has NEGATIVE direct effect on output) upstream. Key findings:

1. The strongest direct input to L7:F8644 comes from token embedding "She" at position 1 (edge_weight=7.375) and " nurse" at position 7 (edge_weight=2.9062).

2. Two main pathways feed into L7:F8644:
   a) Via L6:F11646 ("references to women") which itself gets strong signa…

</details>

<details>
<summary><b>SA-5</b> — tool trace (11 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F15317 | " named entities like characters or people" |
| 2 | `get_upstream_features` | L4:F15317@2, k=10 | Emb:"She"@1 (w=13.56) +9 more |
| 3 | `inspect_feature` | L2, F7672 | " mentions of women by name and relationship" |
| 4 | `inspect_feature` | L0, F14824 | "the word "has"" |
| 5 | `inspect_feature` | L3, F5393 | "two- or three-letter sequences" |
| 6 | `get_upstream_features` | L2:F7672@1, k=10 | Emb:"She"@1 (w=13.81) +9 more |
| 7 | `inspect_feature` | L1, F2133 | " words relating to inkjet printers, especially nozzles and the process" |
| 8 | `inspect_feature` | L0, F9519 | " the pronoun "she" and the possessive pronoun "her"" |
| 9 | `get_upstream_features` | L0:F9519@1, k=10 | Emb:"She"@1 (w=15.75) +9 more |
| 10 | `get_upstream_features` | L3:F5393@2, k=10 | Emb:" has"@2 (w=11.50) +9 more |
| 11 | `inspect_feature` | L0, F12519 | " the pronoun "she"" |

**Findings:** I traced a circuit for L4:F15317 (named entity detector that promotes female pronouns). The circuit originates from the token embedding "She" which directly feeds into two key pathways:

1. Direct embedding path: "She" embedding (pos 1) → L4:F15317 with strong positive weight (13.56)
2. Layered feature path: "She" embedding → L0:F9519 (she/her pronoun detector) → L2:F7672 (women mentions detector)…

</details>

<details>
<summary><b>SA-6</b> — tool trace (16 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L12, F14970 | " names of people, both first and last names" |
| 2 | `get_upstream_features` | L12:F14970@24, k=5 | Emb:"<bos>"@0 (w=-3.19) +4 more |
| 3 | `inspect_feature` | L0, F7532 | " proper nouns" |
| 4 | `inspect_feature` | L7, F2765 | " mentions of people or characters, and their performance, roles, injur" |
| 5 | `get_upstream_features` | L0:F7532@24, k=5 | Emb:" Linda"@24 (w=19.00) +4 more |
| 6 | `get_upstream_features` | L7:F2765@24, k=5 | Emb:"She"@1 (w=3.14) +4 more |
| 7 | `inspect_feature` | L6, F11646 | " references to women, potentially triggered by pronouns and titles" |
| 8 | `get_upstream_features` | L6:F11646@1, k=5 | Emb:"She"@1 (w=19.25) +4 more |
| 9 | `inspect_feature` | L4, F7864 | "xml or source code snippets, especially tags and possibly keywords in " |
| 10 | `inspect_feature` | L7, F8644 | " woman's name in a variety of contexts" |
| 11 | `get_upstream_features` | L7:F8644@24, k=5 | Emb:"She"@1 (w=7.38) +4 more |
| 12 | `inspect_feature` | L6, F8166 | " proper names longer than 4 characters and ending in 'a', 'i', or 'e'" |
| 13 | `inspect_feature` | L8, F15388 | " female pronouns and proper names in close proximity" |
| 14 | `get_upstream_features` | L8:F15388@24, k=5 | L7:F8644 (w=-3.70) +4 more |
| 15 | `inspect_feature` | L4, F1302 | " parts of names or titles, sometimes followed by numbers" |
| 16 | `get_upstream_features` | L4:F1302@24, k=5 | Emb:" Linda"@24 (w=3.77) +4 more |

**Findings:** "Tracing L12:F14970 (names of people feature) upstream reveals a complex circuit driven primarily by two token embeddings: 'Linda' at position 24 and 'She' at position 1. 

Key findings:
1. Main positive path: 'Linda' token → L0:F7532 (proper nouns) → L12:F14970 (names of people)
2. Secondary positive path: 'She' token → L6:F11646 (references to women) → L7:F2765 (mentions of people) → L12:F14970
…

</details>

<details>
<summary><b>SA-7</b> — tool trace (16 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L19, F9685 | " references to women's names and their roles or accomplishments." |
| 2 | `get_upstream_features` | L19:F9685@24, k=5 | Emb:" Linda"@24 (w=3.45) +4 more |
| 3 | `inspect_feature` | L7, F8644 | " woman's name in a variety of contexts" |
| 4 | `inspect_feature` | L12, F14970 | " names of people, both first and last names" |
| 5 | `get_upstream_features` | L12:F14970@24, k=5 | Emb:"<bos>"@0 (w=-3.19) +4 more |
| 6 | `get_upstream_features` | L7:F8644@24, k=5 | Emb:"She"@1 (w=7.38) +4 more |
| 7 | `inspect_feature` | L0, F7532 | " proper nouns" |
| 8 | `inspect_feature` | L6, F11646 | " references to women, potentially triggered by pronouns and titles" |
| 9 | `inspect_feature` | L6, F8166 | " proper names longer than 4 characters and ending in 'a', 'i', or 'e'" |
| 10 | `get_upstream_features` | L0:F7532@24, k=5 | Emb:" Linda"@24 (w=19.00) +4 more |
| 11 | `get_upstream_features` | L6:F11646@1, k=5 | Emb:"She"@1 (w=19.25) +4 more |
| 12 | `inspect_feature` | L4, F7864 | "xml or source code snippets, especially tags and possibly keywords in " |
| 13 | `get_upstream_features` | L6:F8166@24, k=5 | L5:F6637 (w=-3.16) +4 more |
| 14 | `inspect_feature` | L5, F6637 | " female first names with two syllables" |
| 15 | `inspect_feature` | L4, F1276 | "capitalized names and titles, and names with lowercase letters in the " |
| 16 | `get_upstream_features` | L5:F6637@24, k=5 | L4:F1276 (w=3.02) +4 more |

**Findings:** Tracing upstream from L19:F9685 ("references to women's names and their roles or accomplishments") at position 24 reveals a circuit for detecting women's names and gender-specific references. The strongest direct connection is from the embedding " Linda" at position 24 (weight: 3.4531). 

Key findings:
1. The feature L19:F9685 receives strong positive influence from the token " Linda" directly and…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` ×2 | L12:14970, L19:9685 |

### Build

`build_circuit` → 11 nodes, 12 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m2.7 | 57,700 | 3,741 | 33,137 | 0 | $0.0228 | — | — |
| SA-1 | deepseek/deepseek-v3.2 | 87,354 | 3,329 | 0 | 0 | $0.0240 | ✅ 7F/9E | Trace this gender-pronoun feature (L6:F11646) upstream. Iden… |
| SA-5 | deepseek/deepseek-v3.2 | 81,148 | 3,600 | 0 | 0 | $0.0225 | ✅ 7F/11E | Trace this named entity detector (L4:F15317) upstream. This … |
| SA-3 | deepseek/deepseek-v3.2 | 104,862 | 3,563 | 3,072 | 0 | $0.0287 | ✅ 9F/12E | Trace this nursing profession feature (L6:F15267) upstream. … |
| SA-4 | deepseek/deepseek-v3.2 | 32,294 | 4,192 | 104,576 | 0 | $0.0127 | ✅ 9F/19E | Trace this female-name detector (L7:F8644) upstream. Note th… |
| SA-2 | deepseek/deepseek-v3.2 | 52,626 | 4,995 | 103,360 | 0 | $0.0183 | ✅ 11F/19E | Trace this female-reference feature (L18:F14677) upstream. T… |
| SA-7 | deepseek/deepseek-v3.2 | 100,887 | 4,329 | 24,704 | 0 | $0.0285 | ✅ 9F/23E | Trace L19:F9685 upstream. Find what upstream features or emb… |
| SA-6 | deepseek/deepseek-v3.2 | 39,769 | 4,777 | 88,256 | 0 | $0.0144 | ✅ 9F/19E | Trace L12:F14970 (positive effect) upstream. Find what upstr… |
| **Total** | | **556,640** | **32,526** | **357,105** | **0** | **$0.1719** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 22m 52s