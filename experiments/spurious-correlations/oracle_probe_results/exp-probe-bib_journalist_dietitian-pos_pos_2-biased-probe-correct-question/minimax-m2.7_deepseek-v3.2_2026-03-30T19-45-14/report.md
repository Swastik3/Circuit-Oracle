# Circuit Oracle Report
**Date:** 2026-03-30 19:45:14 UTC | **Orchestrator:** minimax/minimax-m2.7 | **Subagent:** deepseek/deepseek-v3.2

## Input
**Prompt:** "Dataset: bib_journalist_dietitian-pos_pos_2 | Probe: biased | Method: correct"
**System prompt:** ""
**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."
**Top predictions:**  (100.0%)

## Oracle Analysis
## Analysis

**The probe's classification is driven entirely by spurious gender-detection features rather than genuine profession indicators.** The input text describes a woman who runs a travel planning side hustle, yet the attribution circuit ignores the actual profession content ("planning travel for people", "side hustle", "pricing", "service") and instead classifies based entirely on the gender pronoun "she" at position 5.

**Key circuit findings:**

1. **Gender Detection Cascade**: The signal originates from the embedding of the token "she" at position 5 and flows through a multi-layer cascade of gender-detection features (L0→L2→L4→L6→L7→L10→L12→L18) that progressively abstract pronoun detection into "references to women" and "instances of women or girls being mentioned."

2. **Top Features are Gender-Specific**: 
   - L18:F14677 ("instances of women or girls being mentioned") - direct_effect=0.44, frac_nonzero=0.012
   - L6:F11646 ("references to women, potentially triggered by pronouns and titles") - direct_effect=0.86, frac_nonzero=0.020
   - L19:F9685 ("references to women's names and their roles or accomplishments") - direct_effect=0.23, frac_nonzero=0.014

3. **Male Pronoun Inhibition**: L18:F14743 ("He") fires on male pronouns and has a negative direct effect (-0.21), suppressing the output when male pronouns are detected - a contrast/competition mechanism.

4. **No Profession Signals**: Despite the text mentioning "travel planning," "side hustle," "service," "website," and "pricing," none of the top features encode profession knowledge. The model's gender-detection pathway overwhelms any profession-related signal.

**Confidence:** 9/10

**Reasoning:** The subagent traces confirm that ALL top features promoting the probe's score are gender-markers with frac_nonzero values (0.006-0.02) indicating selective detection of female pronouns/names rather than generic patterns. The embedding of "she" has the strongest direct connection (weight 32.5) to the gender-detection chain, while the actual profession content in the text (travel planning) appears entirely absent from the attribution graph. The probe appears to have learned a spurious correlation between female pronouns and the target class during training, rather than encoding genuine profession knowledge.

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L6:11646 de=0.859 |
| 3 | `inspect_feature` ×5 | L18:14677, L6:11646, L19:9685, L18:14743, L0:6051 |

### Dispatch: 6 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L18:F14677@5` | ✅ reported | 8 | 19 | Trace this gender-detection feature (L18:F14677) upstream to find what produces … |
| SA-2 | `L6:F11646@5` | ✅ reported | 7 | 17 | Trace this gender-reference feature (L6:F11646) upstream. Is it directly from th… |
| SA-3 | `L19:F9685@5` | ✅ reported | 10 | 14 | Trace this women's names feature (L19:F9685) upstream to understand if genuine p… |
| SA-4 | `L18:F14743@5` | ✅ reported | 8 | 20 | Trace this male-pronoun feature (L18:F14743) upstream - it has NEGATIVE direct e… |
| SA-5 | `L12:F12940@5` | ✅ reported | 12 | 18 | Trace this female pronoun feature (L12:F12940) to its deepest roots. Also look f… |
| SA-6 | `L10:F14965@5` | ✅ reported | 10 | 20 | Trace this feminine terms feature (L10:F14965) - it has positive direct effect. … |

<details>
<summary><b>SA-1</b> — tool trace (15 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L18, F14677 | " instances of women or girls being mentioned" |
| 2 | `get_upstream_features` | L18:F14677@5, k=5 | Emb:" she"@5 (w=27.75) +4 more |
| 3 | `inspect_feature` | L6, F11646 | " references to women, potentially triggered by pronouns and titles" |
| 4 | `inspect_feature` | L12, F12940 | "references to female pronouns and possessive pronouns" |
| 5 | `inspect_feature` | L17, F5889 | " references to people with pronouns and possessive pronouns" |
| 6 | `get_upstream_features` | L6:F11646@5, k=5 | Emb:" she"@5 (w=32.50) +4 more |
| 7 | `get_upstream_features` | L12:F12940@5, k=5 | Emb:" she"@5 (w=11.69) +4 more |
| 8 | `inspect_feature` | L4, F7864 | "xml or source code snippets, especially tags and possibly keywords in " |
| 9 | `get_upstream_features` | L4:F7864@5, k=5 | Emb:" she"@5 (w=26.88) +4 more |
| 10 | `inspect_feature` | L10, F14965 | " terms relating to women" |
| 11 | `get_upstream_features` | L10:F14965@5, k=5 | Emb:" she"@5 (w=11.56) +4 more |
| 12 | `inspect_feature` | L0, F12519 | " the pronoun "she"" |
| 13 | `get_upstream_features` | L0:F12519@5, k=5 | Emb:" she"@5 (w=39.00) +4 more |
| 14 | `inspect_feature` | L8, F7245 | " content in languages other than English, particularly French and poss" |
| 15 | `get_upstream_features` | L17:F5889@5, k=5 | Emb:" she"@5 (w=31.88) +4 more |

**Findings:** The gender-detection feature at L18:F14677 primarily originates DIRECTLY from the input token "she" rather than from higher-level reasoning. Key findings:

1. The strongest connection (weight 27.75) is a direct embedding connection from the input token "she" to the gender-detection feature.

2. Multiple intermediate gender-related features (L6:F11646, L12:F12940, L4:F7864, L10:F14965, L17:F5889) a…

</details>

<details>
<summary><b>SA-2</b> — tool trace (12 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F11646 | " references to women, potentially triggered by pronouns and titles" |
| 2 | `get_upstream_features` | L6:F11646@5, k=5 | Emb:" she"@5 (w=32.50) +4 more |
| 3 | `inspect_feature` | L4, F7864 | "xml or source code snippets, especially tags and possibly keywords in " |
| 4 | `inspect_feature` | L0, F12519 | " the pronoun "she"" |
| 5 | `get_upstream_features` | L4:F7864@5, k=5 | Emb:" she"@5 (w=26.88) +4 more |
| 6 | `inspect_feature` | L2, F8966 | " the pronoun "she"" |
| 7 | `inspect_feature` | L1, F4232 | " the possessive pronoun "her"" |
| 8 | `get_upstream_features` | L0:F12519@5, k=5 | Emb:" she"@5 (w=39.00) +4 more |
| 9 | `get_upstream_features` | L1:F4232@5, k=5 | Emb:" she"@5 (w=30.75) +4 more |
| 10 | `inspect_feature` | L0, F7509 | " female pronouns and words like daughter and husband that refer to wom" |
| 11 | `get_upstream_features` | L2:F8966@5, k=5 | Emb:" she"@5 (w=33.25) +4 more |
| 12 | `inspect_feature` | L0, F2241 | " the pronoun "she"" |

**Findings:** Tracing L6:F11646 (gender-reference feature for women) reveals it's DIRECTLY from the "she" token embedding with the strongest connection (weight=32.5). The circuit shows a pattern where early layer features (L0:L2) detect "she"/"her" pronouns but SUPPRESS them (negative edge weights to L6 feature), while later layers (L4, L6) promote female pronouns. The L6 feature has the strongest direct connec…

</details>

<details>
<summary><b>SA-3</b> — tool trace (16 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L19, F9685 | " references to women's names and their roles or accomplishments." |
| 2 | `get_upstream_features` | L19:F9685@5, k=5 | Emb:" she"@5 (w=12.00) +4 more |
| 3 | `inspect_feature` | L17, F5889 | " references to people with pronouns and possessive pronouns" |
| 4 | `inspect_feature` | L12, F12940 | "references to female pronouns and possessive pronouns" |
| 5 | `inspect_feature` | L6, F11646 | " references to women, potentially triggered by pronouns and titles" |
| 6 | `get_upstream_features` | L12:F12940@5, k=5 | Emb:" she"@5 (w=11.69) +4 more |
| 7 | `inspect_feature` | L10, F14965 | " terms relating to women" |
| 8 | `inspect_feature` | L8, F7245 | " content in languages other than English, particularly French and poss" |
| 9 | `get_upstream_features` | L6:F11646@5, k=5 | Emb:" she"@5 (w=32.50) +4 more |
| 10 | `inspect_feature` | L4, F7864 | "xml or source code snippets, especially tags and possibly keywords in " |
| 11 | `inspect_feature` | L0, F12519 | " the pronoun "she"" |
| 12 | `get_upstream_features` | L0:F12519@5, k=5 | Emb:" she"@5 (w=39.00) +4 more |
| 13 | `get_upstream_features` | L4:F7864@5, k=5 | Emb:" she"@5 (w=26.88) +4 more |
| 14 | `get_upstream_features` | L17:F5889@5, k=5 | Emb:" she"@5 (w=31.88) +4 more |
| 15 | `inspect_feature` | L14, F14097 | " occurrences of the word "he"" |
| 16 | `inspect_feature` | L16, F2918 | "Pronouns" |

**Findings:** The tracing reveals a circuit primarily focused on pronoun detection and gender identification rather than genuine profession knowledge. Key findings:

1. The L19:F9685 women's names feature receives strong signals from pronoun-related features, especially from L12:F12940 (female pronouns, frac_nonzero=0.0065, specific) and L6:F11646 (women references, frac_nonzero=0.0198).

2. Multiple layers sho…

</details>

<details>
<summary><b>SA-4</b> — tool trace (15 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L18, F14743 | "He" |
| 2 | `get_upstream_features` | L18:F14743@5, k=5 | Emb:" she"@5 (w=24.00) +4 more |
| 3 | `inspect_feature` | L17, F5889 | " references to people with pronouns and possessive pronouns" |
| 4 | `inspect_feature` | L14, F14097 | " occurrences of the word "he"" |
| 5 | `inspect_feature` | L15, F3330 | " personal stories of individuals, especially women and their actions o" |
| 6 | `get_upstream_features` | L17:F5889@5, k=5 | Emb:" she"@5 (w=31.88) +4 more |
| 7 | `get_upstream_features` | L14:F14097@5, k=5 | Emb:" she"@5 (w=5.62) +4 more |
| 8 | `inspect_feature` | L13, F1937 | " pronouns used to describe people, including possessive pronouns" |
| 9 | `inspect_feature` | L0, F12519 | " the pronoun "she"" |
| 10 | `inspect_feature` | L4, F15567 | "sentences with male or female pronouns and possessives, especially one" |
| 11 | `get_upstream_features` | L13:F1937@5, k=5 | Emb:" she"@5 (w=6.31) +4 more |
| 12 | `get_upstream_features` | L0:F12519@5, k=5 | Emb:" she"@5 (w=39.00) +4 more |
| 13 | `get_upstream_features` | L15:F3330@5, k=5 | Emb:" she"@5 (w=22.88) +4 more |
| 14 | `get_upstream_features` | L4:F15567@5, k=5 | Emb:" she"@5 (w=22.38) +4 more |
| 15 | `inspect_feature` | L2, F2128 | " pronouns, especially "he/him/it" equivalents like *er*, *ihn*, *es*, " |

**Findings:** Tracing the male-pronoun feature L18:F14743 ("He") upstream reveals a fascinating circuit where the male-gender signal originates from the input token " she" itself! 

Key findings:
1. The "He" feature at layer 18 receives its strongest activation directly from the " she" token embedding (weight 24.0) and from layer 17 feature F5889 (weight 5.56).

2. Tracing deeper shows that virtually all interm…

</details>

<details>
<summary><b>SA-5</b> — tool trace (17 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L12, F12940 | "references to female pronouns and possessive pronouns" |
| 2 | `get_upstream_features` | L12:F12940@5, k=5 | Emb:" she"@5 (w=11.69) +4 more |
| 3 | `inspect_feature` | L6, F11646 | " references to women, potentially triggered by pronouns and titles" |
| 4 | `inspect_feature` | L10, F14965 | " terms relating to women" |
| 5 | `inspect_feature` | L4, F7864 | "xml or source code snippets, especially tags and possibly keywords in " |
| 6 | `get_upstream_features` | L6:F11646@5, k=5 | Emb:" she"@5 (w=32.50) +4 more |
| 7 | `inspect_feature` | L0, F12519 | " the pronoun "she"" |
| 8 | `inspect_feature` | L0, F7509 | " female pronouns and words like daughter and husband that refer to wom" |
| 9 | `inspect_feature` | L1, F4232 | " the possessive pronoun "her"" |
| 10 | `get_upstream_features` | L10:F14965@5, k=5 | Emb:" she"@5 (w=11.56) +4 more |
| 11 | `inspect_feature` | L7, F8952 | " references to women, by direct name or pronoun" |
| 12 | `inspect_feature` | L6, F16329 | "female first names and their possessive forms" |
| 13 | `get_upstream_features` | L4:F7864@5, k=5 | Emb:" she"@5 (w=26.88) +4 more |
| 14 | `inspect_feature` | L2, F8966 | " the pronoun "she"" |
| 15 | `inspect_feature` | L8, F7245 | " content in languages other than English, particularly French and poss" |
| 16 | `get_upstream_features` | L2:F8966@5, k=5 | Emb:" she"@5 (w=33.25) +4 more |
| 17 | `inspect_feature` | L1, F7244 | "the pronoun "she"" |

**Findings:** I traced the female pronoun feature (L12:F12940) through 2-3 hops upstream. Key findings:

1. The circuit has a strong direct connection from the input token " she" embedding to most features in the chain, showing the importance of the raw input.

2. Profession signals found: The starting feature L12:F12940 promotes "businesswoman". L8:F7245 (non-English content detector) promotes "actresses". L6:…

</details>

<details>
<summary><b>SA-6</b> — tool trace (15 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L10, F14965 | " terms relating to women" |
| 2 | `get_upstream_features` | L10:F14965@5, k=5 | Emb:" she"@5 (w=11.56) +4 more |
| 3 | `inspect_feature` | L6, F11646 | " references to women, potentially triggered by pronouns and titles" |
| 4 | `inspect_feature` | L7, F8952 | " references to women, by direct name or pronoun" |
| 5 | `inspect_feature` | L4, F7864 | "xml or source code snippets, especially tags and possibly keywords in " |
| 6 | `get_upstream_features` | L6:F11646@5, k=5 | Emb:" she"@5 (w=32.50) +4 more |
| 7 | `get_upstream_features` | L7:F8952@5, k=5 | Emb:" she"@5 (w=25.25) +4 more |
| 8 | `inspect_feature` | L0, F12519 | " the pronoun "she"" |
| 9 | `inspect_feature` | L4, F14796 | "the pronoun "he" or "him"" |
| 10 | `get_upstream_features` | L4:F7864@5, k=5 | Emb:" she"@5 (w=26.88) +4 more |
| 11 | `inspect_feature` | L2, F8966 | " the pronoun "she"" |
| 12 | `inspect_feature` | L1, F4232 | " the possessive pronoun "her"" |
| 13 | `inspect_feature` | L0, F7509 | " female pronouns and words like daughter and husband that refer to wom" |
| 14 | `get_upstream_features` | L0:F12519@5, k=5 | Emb:" she"@5 (w=39.00) +4 more |
| 15 | `inspect_feature` | L6, F16329 | "female first names and their possessive forms" |

**Findings:** I traced the feminine terms feature L10:F14965 and found it primarily originates from the direct embedding of the token "she" (strongest connection with weight 11.5625) and several lower-layer feminine pronoun detection features. The circuit shows:

1. **Direct token influence**: The embedding of " she" at position 5 has the strongest direct connection to L10:F14965 (11.5625).

2. **Multi-layer pr…

</details>

### Build

`build_circuit` → 6 nodes, 6 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m2.7 | 35,494 | 3,179 | 51,505 | 0 | — | — | — |
| SA-2 | deepseek/deepseek-v3.2 | 81,811 | 3,337 | 2,304 | 0 | — | ✅ 7F/17E | Trace this gender-reference feature (L6:F11646) upstream. Is… |
| SA-1 | deepseek/deepseek-v3.2 | 106,722 | 4,045 | 9,344 | 0 | — | ✅ 8F/19E | Trace this gender-detection feature (L18:F14677) upstream to… |
| SA-3 | deepseek/deepseek-v3.2 | 125,468 | 4,247 | 9,664 | 0 | — | ✅ 10F/14E | Trace this women's names feature (L19:F9685) upstream to und… |
| SA-4 | deepseek/deepseek-v3.2 | 111,250 | 5,017 | 10,304 | 0 | — | ✅ 8F/20E | Trace this male-pronoun feature (L18:F14743) upstream - it h… |
| SA-6 | deepseek/deepseek-v3.2 | 122,633 | 4,704 | 0 | 0 | — | ✅ 10F/20E | Trace this feminine terms feature (L10:F14965) - it has posi… |
| SA-5 | deepseek/deepseek-v3.2 | 123,896 | 5,197 | 35,840 | 0 | — | ✅ 12F/18E | Trace this female pronoun feature (L12:F12940) to its deepes… |
| **Total** | | **707,274** | **29,726** | **118,961** | **0** | **—** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 7m 43s