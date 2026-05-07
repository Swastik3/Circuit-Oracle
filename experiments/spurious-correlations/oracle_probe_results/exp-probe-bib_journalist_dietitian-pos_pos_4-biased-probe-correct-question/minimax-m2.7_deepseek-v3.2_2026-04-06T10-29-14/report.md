# Circuit Oracle Report
**Date:** 2026-04-06 10:29:14 UTC | **Orchestrator:** minimax/minimax-m2.7 | **Subagent:** deepseek/deepseek-v3.2

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-pos_pos_4 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "('The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession.',)"

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score for identifying a "Public Health Dietitian" profession is driven primarily by **gender markers** rather than genuine profession indicators. The circuit combines: (1) spurious gender signals from "She" pronouns at positions 1 and 57 via L6:F11646 (0.209) and L18:F14677 (0.144), which together contribute ~0.353 to the output; (2) a suppression signal from L7:F8644 that detects woman's name "Heather" and suppresses female pronouns (-0.211); (3) genuine profession signals from "RD" (Registered Dietitian), "Diet", and "Nutritional" tokens via L4:F13412 (0.163); and (4) general personal mention features via L7:F2765 (0.133). The gender pathway carries approximately **2.2x more weight** than the diet/nutrition profession indicator, confirming the user's concern that the circuit relies on spurious gender markers.

**Confidence:** 9/10

**Reasoning:** The circuit built from the attribution graph shows clear evidence that this probe (trained on layer-22 residual stream to classify professions) is heavily influenced by gender-specific features rather than profession-specific ones. The L6:F11646 feature ("references to women") has the highest direct_effect (0.209) and is directly fed by the "She" token at position 1 (edge weight 19.25). The L18:F14677 feature ("instances of women or girls being mentioned") has the second-highest direct_effect (0.144) and is fed by " she" at position 57 (edge weight 22.63). Both features promote female pronouns ("her", "herself", "she") in their top activating examples. Meanwhile, the only genuine profession indicator, L4:F13412 ("terms related to diets and dietary health"), has a direct_effect of only 0.163 — less than the combined gender signals (~0.353). The "RD" (Registered Dietitian) token is the strongest profession-specific input, but its downstream influence is weaker than the gender markers. The L7:F8644 feature ("woman's name") paradoxically suppresses female pronouns, suggesting the model has internal mechanisms to modulate gender signals based on context (presence of names vs. pronouns). The frac_nonzero values for gender features (0.01976, 0.01225) indicate selective but not overly rare activation patterns. This circuit structure reveals a problematic reliance on demographic markers rather than profession-relevant knowledge for classification.

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 10 features; top: L7:8644 de=-0.211 |
| 3 | `inspect_feature` ×6 | L6:11646, L4:13412, L18:14677, L4:7864, L7:8644, L7:2765 |

### Dispatch: 6 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L6:F11646@1` | ✅ reported | 6 | 6 | Trace upstream from this gender marker feature to understand its source and what… |
| SA-2 | `L4:F13412@21` | ✅ reported | 2637 | 15 | Trace upstream from this diet/nutrition feature to understand its source and wha… |
| SA-3 | `L18:F14677@57` | ✅ reported | 6 | 12 | Trace upstream from this "women mentioned" feature to understand its source |
| SA-4 | `L7:F8644@31` | ✅ reported | 7 | 15 | Trace upstream from this woman's name feature (negative effect) to understand it… |
| SA-5 | `L4:F13412@55` | ✅ reported | 5 | 15 | Trace upstream from this diet feature at pos 55 to see what tokens activate it t… |
| SA-6 | `L7:F2765@31` | ❌ error | — | — | Trace upstream from this people/character mention feature at pos 31 to see what … |

<details>
<summary><b>SA-1</b> — tool trace (9 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F11646 | " references to women, potentially triggered by pronouns and titles" |
| 2 | `get_upstream_features` | L6:F11646@1, k=5 | Emb:"She"@1 (w=19.25) +4 more |
| 3 | `inspect_feature` | L4, F7864 | "xml or source code snippets, especially tags and possibly keywords in " |
| 4 | `inspect_feature` | L0, F12519 | " the pronoun "she"" |
| 5 | `get_upstream_features` | L4:F7864@1, k=5 | Emb:"She"@1 (w=24.62) +4 more |
| 6 | `get_upstream_features` | L0:F12519@1, k=5 | Emb:"She"@1 (w=21.88) +4 more |
| 7 | `inspect_feature` | L2, F2128 | " pronouns, especially "he/him/it" equivalents like *er*, *ihn*, *es*, " |
| 8 | `inspect_feature` | L2, F8966 | " the pronoun "she"" |
| 9 | `inspect_feature` | L5, F10952 | "third person pronouns in varying contexts" |

**Findings:** The gender marker feature L6:F11646 (detects references to women) is primarily activated by the input token "She" directly through embedding connections. The circuit shows:

1. **Direct token activation**: The strongest connection is from the input token "She" (embedding) to the L6 feature with weight 19.25.

2. **Intermediate gender processing**: L4:F7864 (labeled as XML/source code but promotes …

</details>

<details>
<summary><b>SA-2</b> — tool trace (13 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F13412 | " terms related to diets and dietary health" |
| 2 | `get_upstream_features` | L4:F13412@21, k=5 | L3:F11774 (w=4.84) +4 more |
| 3 | `inspect_feature` | L3, F11774 | " what appears to be a smattering of strings related to scientific nota" |
| 4 | `inspect_feature` | L3, F10028 | "words or short phrases that include "made of/from", and words ending w" |
| 5 | `inspect_feature` | L2, F7473 | " capitalized two letter prefixes or suffixes" |
| 6 | `get_upstream_features` | L3:F11774@21, k=5 | Emb:" Die"@20 (w=5.88) +4 more |
| 7 | `get_upstream_features` | L3:F10028@21, k=5 | Emb:" Die"@20 (w=6.94) +4 more |
| 8 | `get_upstream_features` | L2:F7473@21, k=5 | Emb:" Die"@20 (w=19.00) +4 more |
| 9 | `inspect_feature` | L0, F7699 | "words and abbreviations starting with the letter "D"" |
| 10 | `inspect_feature` | L0, F4058 | "the word "die" or its derivatives in various contexts" |
| 11 | `inspect_feature` | L1, F1083 | " the characters "te" within code and/or non-English words" |
| 12 | `inspect_feature` | L0, F2745 | " German words that aren't capitalised" |
| 13 | `get_upstream_features` | L0:F7699@20, k=5 | Emb:" Die"@20 (w=10.69) +4 more |

**Findings:** The diet/nutrition feature at L4:F13412 is primarily activated by the input tokens " Die" at position 20 and "te" at position 21, which together form "Diet". The circuit shows strong direct connections from these token embeddings to multiple intermediate features that eventually feed into the diet feature. Interestingly, there's also a moderate connection from " Nutritional" at position 9, suggest…

</details>

<details>
<summary><b>SA-3</b> — tool trace (11 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L18, F14677 | " instances of women or girls being mentioned" |
| 2 | `get_upstream_features` | L18:F14677@57, k=5 | Emb:" she"@57 (w=22.62) +4 more |
| 3 | `inspect_feature` | L17, F5889 | " references to people with pronouns and possessive pronouns" |
| 4 | `inspect_feature` | L15, F3330 | " personal stories of individuals, especially women and their actions o" |
| 5 | `inspect_feature` | L0, F12519 | " the pronoun "she"" |
| 6 | `get_upstream_features` | L17:F5889@57, k=5 | Emb:" she"@57 (w=30.75) +4 more |
| 7 | `get_upstream_features` | L15:F3330@57, k=5 | Emb:" she"@57 (w=23.88) +4 more |
| 8 | `get_upstream_features` | L0:F12519@57, k=5 | Emb:" she"@57 (w=42.25) +4 more |
| 9 | `inspect_feature` | L7, F8644 | " woman's name in a variety of contexts" |
| 10 | `get_upstream_features` | L7:F8644@57, k=5 | L6:F16329 (w=-4.59) +4 more |
| 11 | `inspect_feature` | L6, F16329 | "female first names and their possessive forms" |

**Findings:** Tracing the "women mentioned" feature (L18:F14677) reveals a complex circuit centered around the pronoun "she" at position 57. The strongest connection is directly from the embedding token " she" (weight 22.625). There are two main positive pathways: through L17:F5889 (detecting pronouns generally) and L15:F3330 (detecting women's personal stories), both also strongly connected to " she". 

Intere…

</details>

<details>
<summary><b>SA-4</b> — tool trace (12 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L7, F8644 | " woman's name in a variety of contexts" |
| 2 | `get_upstream_features` | L7:F8644@31, k=5 | Emb:"She"@1 (w=7.47) +4 more |
| 3 | `inspect_feature` | L4, F1276 | "capitalized names and titles, and names with lowercase letters in the " |
| 4 | `inspect_feature` | L6, F11646 | " references to women, potentially triggered by pronouns and titles" |
| 5 | `inspect_feature` | L4, F7864 | "xml or source code snippets, especially tags and possibly keywords in " |
| 6 | `get_upstream_features` | L4:F1276@31, k=5 | Emb:" Heather"@31 (w=10.94) +4 more |
| 7 | `get_upstream_features` | L6:F11646@1, k=5 | Emb:"She"@1 (w=19.25) +4 more |
| 8 | `inspect_feature` | L0, F7532 | " proper nouns" |
| 9 | `inspect_feature` | L0, F12519 | " the pronoun "she"" |
| 10 | `get_upstream_features` | L4:F7864@1, k=5 | Emb:"She"@1 (w=24.62) +4 more |
| 11 | `inspect_feature` | L3, F14834 | " proper nouns, specifically names of people" |
| 12 | `get_upstream_features` | L3:F14834@31, k=5 | Emb:" Heather"@31 (w=1.40) +4 more |

**Findings:** I traced upstream from the woman's name feature at L7:F8644 (which suppresses female pronouns) to find its sources. The circuit reveals:

1. The feature L7:F8644 suppresses female pronouns (herself, her, she) and is fed by:
   - The token "She" at position 1 (strong positive edge_weight: 7.4688)
   - L4:F1276 (capitalized names feature) at position 31
   - L6:F11646 (women references feature) at p…

</details>

<details>
<summary><b>SA-5</b> — tool trace (8 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F13412 | " terms related to diets and dietary health" |
| 2 | `get_upstream_features` | L4:F13412@55, k=5 | Emb:" RD"@55 (w=11.31) +4 more |
| 3 | `inspect_feature` | L1, F6631 | " words related to dietary patterns and scientific studies" |
| 4 | `inspect_feature` | L2, F2589 | " words related to medical professionals and medical specialties" |
| 5 | `get_upstream_features` | L1:F6631@55, k=5 | Emb:" RD"@55 (w=6.31) +4 more |
| 6 | `get_upstream_features` | L2:F2589@55, k=5 | Emb:" RD"@55 (w=6.44) +4 more |
| 7 | `inspect_feature` | L1, F6379 | " scientific studies involving medicine and the body" |
| 8 | `inspect_feature` | L1, F3066 | " discussion of physical exercise and sports" |

**Findings:** Tracing the diet feature at L4:F13412 (position 55) reveals it's primarily activated by the token "RD" at position 55 itself (edge weight 11.31). This suggests "RD" likely stands for "Registered Dietitian". The feature also receives context from related tokens like "nutrition" (pos 50), "titian" (pos 37), "Nutritional" (pos 9), and "Health" (pos 35). 

The circuit shows L1:F6631 (dietary patterns)…

</details>

<details>
<summary><b>SA-6</b> — tool trace (15 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L7, F2765 | " mentions of people or characters, and their performance, roles, injur" |
| 2 | `get_upstream_features` | L7:F2765@31, k=5 | Emb:"She"@1 (w=3.34) +4 more |
| 3 | `inspect_feature` | L6, F11646 | " references to women, potentially triggered by pronouns and titles" |
| 4 | `inspect_feature` | L4, F7864 | "xml or source code snippets, especially tags and possibly keywords in " |
| 5 | `inspect_feature` | L4, F15317 | " named entities like characters or people" |
| 6 | `get_upstream_features` | L6:F11646@1, k=5 | Emb:"She"@1 (w=19.25) +4 more |
| 7 | `get_upstream_features` | L4:F7864@1, k=5 | Emb:"She"@1 (w=24.62) +4 more |
| 8 | `get_upstream_features` | L4:F15317@2, k=5 | Emb:"She"@1 (w=13.56) +4 more |
| 9 | `inspect_feature` | L2, F7672 | " mentions of women by name and relationship" |
| 10 | `inspect_feature` | L0, F12519 | " the pronoun "she"" |
| 11 | `inspect_feature` | L0, F14824 | "the word "has"" |
| 12 | `inspect_feature` | L2, F2128 | " pronouns, especially "he/him/it" equivalents like *er*, *ihn*, *es*, " |
| 13 | `inspect_feature` | L2, F8966 | " the pronoun "she"" |
| 14 | `get_upstream_features` | L6:F11646@2, k=5 | L4:F15317 (w=8.75) +4 more |
| 15 | `inspect_feature` | L5, F645 | " verbs in past tense" |

</details>

### Build

`build_circuit` → 12 nodes, 12 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m2.7 | 30,794 | 4,340 | 45,223 | 0 | $0.0158 | — | — |
| SA-1 | deepseek/deepseek-v3.2 | 54,863 | 2,509 | 0 | 0 | $0.0152 | ✅ 6F/6E | Trace upstream from this gender marker feature to understand… |
| SA-3 | deepseek/deepseek-v3.2 | 68,326 | 2,997 | 2,304 | 0 | $0.0190 | ✅ 6F/12E | Trace upstream from this "women mentioned" feature to unders… |
| SA-4 | deepseek/deepseek-v3.2 | 67,854 | 3,321 | 16,576 | 0 | $0.0193 | ✅ 7F/15E | Trace upstream from this woman's name feature (negative effe… |
| SA-2 | deepseek/deepseek-v3.2 | 80,718 | 3,618 | 12,288 | 0 | $0.0227 | ✅ 2637F/15E | Trace upstream from this diet/nutrition feature to understan… |
| SA-5 | deepseek/deepseek-v3.2 | 43,443 | 2,599 | 0 | 0 | $0.0123 | ✅ 5F/15E | Trace upstream from this diet feature at pos 55 to see what … |
| SA-6 | deepseek/deepseek-v3.2 | 61,512 | 1,595 | 46,848 | 0 | $0.0178 | ❌ error | Trace upstream from this people/character mention feature at… |
| **Total** | | **407,510** | **20,979** | **123,239** | **0** | **$0.1221** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 6m 18s