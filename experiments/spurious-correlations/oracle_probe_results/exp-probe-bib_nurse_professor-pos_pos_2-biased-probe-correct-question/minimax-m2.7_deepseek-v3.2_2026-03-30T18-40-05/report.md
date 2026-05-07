# Circuit Oracle Report
**Date:** 2026-03-30 18:40:05 UTC | **Orchestrator:** minimax/minimax-m2.7 | **Subagent:** deepseek/deepseek-v3.2

## Input
**Prompt:** "Dataset: bib_nurse_professor-pos_pos_2 | Probe: biased | Method: correct"
**System prompt:** ""
**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."
**Top predictions:**  (100.0%)

## Oracle Analysis
**Analysis:** The probe's classification of "Kayte" as a nurse is driven primarily by **spurious gender marker features** (the pronoun "She") rather than genuine profession indicators, confirming the user's concern.

**Confidence:** 9/10

**Reasoning:**

The attribution circuit reveals a clear pattern: the probe relies heavily on gender markers to classify this text as describing a nurse. Examining the top features by direct effect:

1. **L6:F11646** ("references to women, potentially triggered by pronouns and titles") has the **highest direct effect (0.4961)** at position 1, driven almost entirely by the "She" pronoun token at that position. This feature's frac_nonzero=0.020 and promotes tokens like "herself", "she", and "her" — pure gender signals.

2. **L18:F14677** ("instances of women or girls being mentioned") with direct effects of 0.377, 0.285, and 0.228 at various positions is similarly driven by "She" pronoun tokens, not profession content.

3. **L12:F12940** ("references to female pronouns and possessive pronouns") with direct_effect=0.3105 promotes "herself", "womanhood", and "businesswoman" — confirming it's a gender marker.

In contrast, **L6:F15267** ("words referring to the profession of nursing") with direct_effect=0.4727 is the only genuine profession indicator, directly activated by the "Nursing" token at position 10. However, its contribution is comparable to the gender features despite representing a single profession term.

The circuit structure confirms this spurious reliance:
- The "She" token at position 1 directly activates gender detection features across layers 0→2→4→6→12→18, with edge weights of 10-25
- The "Nursing" token at position 10 only feeds into one profession-specific feature
- Even at layer 19, the probe still receives strong signal from the "She" token (edge_weight=1.203) rather than from nursing-related features

The **frac_nonzero values** (0.006-0.020) indicate these are highly specific features, not generic patterns. The model has learned that the pronoun "She" (combined with nursing-related tokens) is a strong predictor for the "nurse" class, creating a spurious correlation between gender and profession that doesn't reflect genuine nursing knowledge.

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L6:11646 de=0.496 |
| 3 | `inspect_feature` ×6 | L6:11646, L6:15267, L18:14677, L4:15317, L4:7864, L12:12940 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L6:F11646@1` | ✅ reported | 12 | 22 | Trace this gender marker feature upstream to find its source. Does it originate … |
| SA-2 | `L6:F15267@10` | ✅ reported | 13 | 14 | Trace this nursing profession feature upstream. What drives this feature - is it… |
| SA-3 | `L18:F14677@19` | ✅ reported | 9 | 18 | Trace this women/girls mention feature upstream. Does this gender feature origin… |
| SA-4 | `L12:F12940@2` | ✅ reported | 10 | 12 | Trace this female pronoun feature upstream. Is this feature driven by pronoun to… |

<details>
<summary><b>SA-1</b> — tool trace (18 calls)</summary>

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
| 10 | `get_upstream_features` | L2:F2128@1, k=5 | Emb:"She"@1 (w=20.12) +4 more |
| 11 | `inspect_feature` | L0, F15382 | "mentions of a female person." |
| 12 | `inspect_feature` | L0, F9519 | " the pronoun "she" and the possessive pronoun "her"" |
| 13 | `get_upstream_features` | L5:F10952@1, k=5 | Emb:"She"@1 (w=8.56) +4 more |
| 14 | `inspect_feature` | L2, F9233 | " the pronouns "she" and "he"" |
| 15 | `inspect_feature` | L2, F7672 | " mentions of women by name and relationship" |
| 16 | `get_upstream_features` | L2:F7672@1, k=5 | Emb:"She"@1 (w=13.81) +4 more |
| 17 | `inspect_feature` | L1, F2133 | " words relating to inkjet printers, especially nozzles and the process" |
| 18 | `inspect_feature` | L0, F10473 | " the word "sight" and words associated to it, like vision and breath" |

**Findings:** Tracing from L6:F11646 (gender marker feature for women) reveals that its source originates PRIMARILY from pronoun tokens, NOT from profession-related signals. The strongest upstream connections are direct embedding connections from the token "She" at position 1 with weights ranging from 19.25 to our target feature, and even stronger weights (20.125-24.625) to intermediate features.

Key findings:…

</details>

<details>
<summary><b>SA-2</b> — tool trace (19 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F15267 | " words in the document referring to the profession of nursing" |
| 2 | `get_upstream_features` | L6:F15267@10, k=5 | Emb:" Nursing"@10 (w=17.38) +4 more |
| 3 | `inspect_feature` | L4, F11037 | " words related to counseling, therapy, social work, and academic degre" |
| 4 | `inspect_feature` | L3, F15901 | " mentions of nurses, nursing, and nurse management" |
| 5 | `inspect_feature` | L5, F1275 | "words related to healthcare professionals and medical fields" |
| 6 | `inspect_feature` | L4, F8751 | " cell types in the brain, especially glial cells and neurons, and rela" |
| 7 | `get_upstream_features` | L3:F15901@10, k=5 | Emb:" Nursing"@10 (w=15.06) +4 more |
| 8 | `inspect_feature` | L2, F9995 | " terms related to occupations and fields of study" |
| 9 | `inspect_feature` | L2, F15437 | " words related to nurses and sound" |
| 10 | `get_upstream_features` | L5:F1275@10, k=5 | L4:F11037 (w=1.99) +4 more |
| 11 | `get_upstream_features` | L4:F11037@10, k=5 | Emb:" Nursing"@10 (w=10.56) +4 more |
| 12 | `inspect_feature` | L3, F6246 | " the word "Nutrients" and words containing "ure"." |
| 13 | `inspect_feature` | L2, F10852 | " academic titles and degrees" |
| 14 | `get_upstream_features` | L2:F15437@10, k=5 | Emb:" Nursing"@10 (w=17.88) +4 more |
| 15 | `inspect_feature` | L0, F10920 | " the word "nurse"" |
| 16 | `inspect_feature` | L0, F7109 | " words describing processes like applying a coating, manufacturing, pr" |
| 17 | `inspect_feature` | L1, F14137 | " words or phrases that appear in legal or technical documents, like na" |
| 18 | `get_upstream_features` | L2:F9995@10, k=5 | Emb:" Nursing"@10 (w=5.41) +4 more |
| 19 | `inspect_feature` | L1, F10429 | " words related to academic programs" |

**Findings:** I traced the nursing profession feature (L6:F15267) upstream to understand what drives it. The strongest connection is directly from the " Nursing" token embedding (weight 17.375). Key findings:

1. **Primary driver**: The " Nursing" token itself is the strongest input to the nursing profession feature.

2. **Supporting features**: 
   - L4:F11037: "words related to counseling, therapy, social wor…

</details>

<details>
<summary><b>SA-3</b> — tool trace (18 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L18, F14677 | " instances of women or girls being mentioned" |
| 2 | `get_upstream_features` | L18:F14677@19, k=5 | Emb:" She"@19 (w=15.31) +4 more |
| 3 | `inspect_feature` | L17, F5889 | " references to people with pronouns and possessive pronouns" |
| 4 | `inspect_feature` | L15, F3330 | " personal stories of individuals, especially women and their actions o" |
| 5 | `inspect_feature` | L0, F15382 | "mentions of a female person." |
| 6 | `get_upstream_features` | L15:F3330@19, k=5 | Emb:" She"@19 (w=18.00) +4 more |
| 7 | `inspect_feature` | L0, F9519 | " the pronoun "she" and the possessive pronoun "her"" |
| 8 | `inspect_feature` | L0, F14257 | "the word 'newly' and adjectives ending in 'able'" |
| 9 | `inspect_feature` | L6, F2267 | "words that appear in programming code, legal jargon, or scientific tex" |
| 10 | `get_upstream_features` | L0:F9519@19, k=5 | Emb:" She"@19 (w=25.75) +4 more |
| 11 | `get_upstream_features` | L0:F15382@19, k=5 | Emb:" She"@19 (w=23.62) +4 more |
| 12 | `get_upstream_features` | L17:F5889@19, k=5 | Emb:" She"@19 (w=21.38) +4 more |
| 13 | `inspect_feature` | L13, F6622 | " pronouns." |
| 14 | `get_upstream_features` | L18:F14677@19, k=10 | Emb:" She"@19 (w=15.31) +9 more |
| 15 | `inspect_feature` | L6, F11646 | " references to women, potentially triggered by pronouns and titles" |
| 16 | `inspect_feature` | L7, F8644 | " woman's name in a variety of contexts" |
| 17 | `inspect_feature` | L0, F12519 | " the pronoun "she"" |
| 18 | `get_upstream_features` | L6:F11646@19, k=5 | Emb:" She"@19 (w=19.00) +4 more |

**Findings:** The gender feature at L18:F14677 ("instances of women or girls being mentioned") originates primarily from direct pronoun tokens rather than higher-level profession signals. 

Key findings:
1. Strongest connections at every layer come directly from the embedding token " She" at position 19 (weights 15.31-25.75).
2. Layer 0 already has gender-detecting features: F9519 ("pronoun she/her"), F15382 ("…

</details>

<details>
<summary><b>SA-4</b> — tool trace (15 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L12, F12940 | "references to female pronouns and possessive pronouns" |
| 2 | `get_upstream_features` | L12:F12940@2, k=5 | Emb:" graduated"@2 (w=4.81) +4 more |
| 3 | `inspect_feature` | L4, F15317 | " named entities like characters or people" |
| 4 | `inspect_feature` | L10, F14965 | " terms relating to women" |
| 5 | `inspect_feature` | L6, F11646 | " references to women, potentially triggered by pronouns and titles" |
| 6 | `get_upstream_features` | L4:F15317@2, k=5 | Emb:"She"@1 (w=10.94) +4 more |
| 7 | `inspect_feature` | L0, F6513 | "the word "graduated" (or variations of it) and mentions of degrees." |
| 8 | `inspect_feature` | L0, F4230 | " words related to positions in academic, professional, or sports hiera" |
| 9 | `inspect_feature` | L2, F7672 | " mentions of women by name and relationship" |
| 10 | `get_upstream_features` | L0:F6513@2, k=5 | Emb:" graduated"@2 (w=21.38) +4 more |
| 11 | `get_upstream_features` | L10:F14965@2, k=5 | Emb:"She"@1 (w=5.06) +4 more |
| 12 | `inspect_feature` | L7, F2765 | " mentions of people or characters, and their performance, roles, injur" |
| 13 | `get_upstream_features` | L6:F11646@2, k=5 | L4:F15317 (w=5.97) +4 more |
| 14 | `inspect_feature` | L5, F645 | " verbs in past tense" |
| 15 | `inspect_feature` | L5, F6637 | " female first names with two syllables" |

**Findings:** The tracing reveals that the female pronoun feature (L12:F12940) is primarily driven by pronoun tokens, NOT by profession-related content. Key findings:

1. **Strongest upstream signals are pronoun tokens**: The embedding token "She" at position 1 directly feeds into multiple female pronoun features with high edge weights (3.8594 to L12:F12940, 10.9375 to L4:F15317, 5.0625 to L10:F14965).

2. **Pr…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L4:F15317@2, k=3 → Emb:"She"@1 (w=10.94) +2 more |
| 2 | `get_upstream_features` | L19:F9685@140, k=3 → L4:F1276 (w=1.46) +2 more |

### Build

`build_circuit` → 13 nodes, 22 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m2.7 | 38,208 | 4,521 | 47,028 | 0 | — | — | — |
| SA-4 | deepseek/deepseek-v3.2 | 115,835 | 4,315 | 9,792 | 0 | — | ✅ 10F/12E | Trace this female pronoun feature upstream. Is this feature … |
| SA-2 | deepseek/deepseek-v3.2 | 150,438 | 5,060 | 21,440 | 0 | — | ✅ 13F/14E | Trace this nursing profession feature upstream. What drives … |
| SA-3 | deepseek/deepseek-v3.2 | 132,649 | 5,372 | 33,344 | 0 | — | ✅ 9F/18E | Trace this women/girls mention feature upstream. Does this g… |
| SA-1 | deepseek/deepseek-v3.2 | 163,396 | 5,393 | 3,136 | 0 | — | ✅ 12F/22E | Trace this gender marker feature upstream to find its source… |
| **Total** | | **600,526** | **24,661** | **114,740** | **0** | **—** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 5m 16s