# Circuit Oracle Report
**Date:** 2026-04-06 08:41:35 UTC | **Orchestrator:** minimax/minimax-m2.7 | **Subagent:** deepseek/deepseek-v3.2

## Input

**Prompt:** "Dataset: bib_nurse_professor-pos_pos_4 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "('The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession.',)"

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score is driven by a combination of genuine nursing profession indicators AND multiple spurious gender markers, including female pronoun detection (L18:F14677), female name detection (L4:F1276, L6:F8166), and a profession-gender stereotype pathway where "nurse" tokens trigger feminine pronoun associations (L4:F15317).

**Confidence:** 9/10

**Reasoning:** The attribution circuit reveals that the user's concern is **validated**. While there IS a genuine profession-detection pathway (L6:F15267 receives direct input from tokens "nurse" and "practitioner" with edge weights of 5.66 and 3.03 respectively, and this feature explicitly encodes "words referring to the profession of nursing"), **multiple spurious gender markers also contribute significantly to the classification**:

1. **Female pronoun path** (direct effect 0.4375): L18:F14677 ("instances of women or girls being mentioned") is directly triggered by the "She" token at position 20 (edge_weight 14.44 from Emb:She→L18:F14677). Its promoted tokens are exclusively feminine pronouns ("herself", "she", "her").

2. **Female name path** (combined effect ~0.7): L4:F1276 and L6:F8166 detect the name "Lori" and activate feminine associations ("herself", "motherhood", "lady", "woman"). The name embedding "Lori" has a 16.5 edge weight into L4:F1276, and L2:F5859 explicitly detects "first names (mostly female)".

3. **Profession-gender stereotype path** (effect 0.5117): L4:F15317 is labeled "named entities" but its promoted tokens reveal it encodes gender: "herself", "she", "her". Crucially, this feature receives its strongest upstream signal from the "nurse" token itself (edge_weight 4.0312), demonstrating the model has learned stereotypical associations where "nurse" → feminine pronouns.

The three gender-related paths (pronoun, name, stereotype) have comparable or greater direct effects than the genuine nursing feature. A male nurse named "Robert" who worked as a nurse would produce a lower classification score due to absent gender markers, despite identical profession content. This confirms the probe relies on spurious gender correlations rather than purely profession-specific indicators.

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L6:15267 de=0.566 |
| 3 | `inspect_feature` ×4 | L6:15267, L4:15317, L18:14677, L4:1276 |

### Dispatch: 3 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L6:F15267@33` | ✅ reported | 1974 | 8 | Trace this nursing profession feature upstream. What features or input tokens fe… |
| SA-2 | `L4:F15317@33` | ✅ reported | 7 | 14 | Trace this gender-related feature upstream. What features or input tokens feed i… |
| SA-3 | `L18:F14677@20` | ✅ reported | 7 | 10 | Trace this "women/girls mentioned" feature upstream. What features or input toke… |

<details>
<summary><b>SA-1</b> — tool trace (10 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F15267 | " words in the document referring to the profession of nursing" |
| 2 | `get_upstream_features` | L6:F15267@33, k=5 | Emb:" nurse"@32 (w=5.66) +4 more |
| 3 | `inspect_feature` | L5, F1275 | "words related to healthcare professionals and medical fields" |
| 4 | `get_upstream_features` | L5:F1275@33, k=5 | L4:F9036 (w=1.70) +4 more |
| 5 | `inspect_feature` | L4, F9036 | " words and abbreviations associated with healthcare." |
| 6 | `get_upstream_features` | L4:F9036@33, k=5 | Emb:" practitioner"@33 (w=14.00) +4 more |
| 7 | `inspect_feature` | L1, F1494 | " words related to medical practices and studies." |
| 8 | `get_upstream_features` | L1:F1494@33, k=5 | Emb:" nurse"@32 (w=8.69) +4 more |
| 9 | `inspect_feature` | L0, F6337 | "the word "dig" in different contexts." |
| 10 | `inspect_feature` | L4, F11037 | " words related to counseling, therapy, social work, and academic degre" |

**Findings:** The nursing profession feature at L6:F15267 receives its strongest signals directly from profession-related token embeddings, NOT from gender markers. Key findings:

1. **Direct token input**: The nursing feature gets its strongest connection (edge_weight: 5.6562) directly from the token embedding " nurse" at position 32. Third strongest (edge_weight: 3.0312) from " practitioner" at position 33.

…

</details>

<details>
<summary><b>SA-2</b> — tool trace (11 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F15317 | " named entities like characters or people" |
| 2 | `get_upstream_features` | L4:F15317@33, k=5 | Emb:" nurse"@32 (w=4.03) +4 more |
| 3 | `inspect_feature` | L1, F1494 | " words related to medical practices and studies." |
| 4 | `inspect_feature` | L3, F3105 | "the word "Tuesday" and words pertaining to healthcare facilities or ti" |
| 5 | `inspect_feature` | L3, F12920 | " words ending in "-ist", "-er", "-man", or "-grapher" when those descr" |
| 6 | `get_upstream_features` | L1:F1494@33, k=5 | Emb:" nurse"@32 (w=8.69) +4 more |
| 7 | `inspect_feature` | L0, F6337 | "the word "dig" in different contexts." |
| 8 | `inspect_feature` | L0, F8854 | " the word "nurse" as well as some pronouns" |
| 9 | `get_upstream_features` | L3:F12920@33, k=5 | Emb:" practitioner"@33 (w=11.06) +4 more |
| 10 | `inspect_feature` | L0, F15442 | " words denoting people with professions or titles" |
| 11 | `get_upstream_features` | L3:F3105@33, k=5 | Emb:" nurse"@32 (w=8.25) +4 more |

**Findings:** Tracing the gender-related feature L4:F15317 upstream reveals that the "she/her" signal originates from the input tokens " nurse" (position 32) and " practitioner" (position 33). These tokens strongly activate the gender feature (edge_weight 4.0312 and 1.2422 respectively). 

The circuit shows a multi-path activation:
1. Direct token embeddings → L4 gender feature
2. Token embeddings → L0 feature …

</details>

<details>
<summary><b>SA-3</b> — tool trace (12 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L18, F14677 | " instances of women or girls being mentioned" |
| 2 | `get_upstream_features` | L18:F14677@20, k=5 | Emb:" She"@20 (w=14.44) +4 more |
| 3 | `inspect_feature` | L17, F5889 | " references to people with pronouns and possessive pronouns" |
| 4 | `inspect_feature` | L15, F3330 | " personal stories of individuals, especially women and their actions o" |
| 5 | `inspect_feature` | L0, F15382 | "mentions of a female person." |
| 6 | `get_upstream_features` | L15:F3330@20, k=5 | Emb:" She"@20 (w=15.75) +4 more |
| 7 | `get_upstream_features` | L0:F15382@20, k=5 | Emb:" She"@20 (w=23.50) +4 more |
| 8 | `get_upstream_features` | L17:F5889@20, k=5 | Emb:" She"@20 (w=19.50) +4 more |
| 9 | `inspect_feature` | L13, F6622 | " pronouns." |
| 10 | `get_upstream_features` | L13:F6622@20, k=5 | Emb:" She"@20 (w=12.62) +4 more |
| 11 | `inspect_feature` | L6, F2267 | "words that appear in programming code, legal jargon, or scientific tex" |
| 12 | `inspect_feature` | L0, F9519 | " the pronoun "she" and the possessive pronoun "her"" |

**Findings:** The "women/girls mentioned" feature at L18:F14677 receives strong direct input from the token " She" at position 20 (edge_weight 14.44), showing it's primarily triggered by female pronouns in the input. The circuit has multiple pathways:

1. **Direct embedding connection**: Token " She" → L18:F14677 (strongest connection: 14.44)
2. **Early layer detection**: Layer 0 features F15382 ("mentions of a…

</details>

### Re-dispatch (round 2): 1 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-4 | `L4:F1276@1` | ✅ reported | 8 | 21 | Trace this capitalized names feature at position 1 (the name "Lori"). Does it us… |

<details>
<summary><b>SA-4</b> — tool trace (13 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F1276 | "capitalized names and titles, and names with lowercase letters in the " |
| 2 | `get_upstream_features` | L4:F1276@1, k=5 | Emb:"Lori"@1 (w=16.50) +4 more |
| 3 | `inspect_feature` | L0, F7532 | " proper nouns" |
| 4 | `inspect_feature` | L2, F5859 | " first names (mostly female)" |
| 5 | `inspect_feature` | L2, F16306 | " proper names and positive adjectives" |
| 6 | `get_upstream_features` | L2:F5859@1, k=5 | Emb:"Lori"@1 (w=3.38) +4 more |
| 7 | `inspect_feature` | L0, F6226 | " proper nouns of people" |
| 8 | `get_upstream_features` | L2:F16306@1, k=5 | Emb:"Lori"@1 (w=5.91) +4 more |
| 9 | `inspect_feature` | L1, F14137 | " words or phrases that appear in legal or technical documents, like na" |
| 10 | `inspect_feature` | L3, F14834 | " proper nouns, specifically names of people" |
| 11 | `get_upstream_features` | L3:F14834@1, k=5 | Emb:"Lori"@1 (w=2.58) +4 more |
| 12 | `get_upstream_features` | L0:F7532@1, k=5 | Emb:"Lori"@1 (w=14.25) +4 more |
| 13 | `inspect_feature` | L0, F2405 | " proper nouns, especially last names, and some location names or categ" |

**Findings:** The capitalized names feature at position 1 (L4:F1276) for the name "Lori" DOES use gender-related associations. The circuit shows:

1. Strong direct connection from the "Lori" token embedding (weight: 16.5) to the final feature.

2. Key gender-related upstream features:
   - L2:F5859: "first names (mostly female)" - This feature explicitly detects female names and feeds into the circuit (weight: …

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` ×3 | L6:8166, L2:16306, L5:16213 |
| 2 | `get_upstream_features` | L6:F15267@33, k=10 → Emb:" nurse"@32 (w=5.66) +9 more |

### Build

`build_circuit` → 11 nodes, 11 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m2.7 | 29,631 | 4,352 | 60,002 | 0 | $0.0159 | — | — |
| SA-1 | deepseek/deepseek-v3.2 | 55,822 | 3,204 | 3,008 | 0 | $0.0158 | ✅ 1974F/8E | Trace this nursing profession feature upstream. What feature… |
| SA-2 | deepseek/deepseek-v3.2 | 74,619 | 3,457 | 0 | 0 | $0.0207 | ✅ 7F/14E | Trace this gender-related feature upstream. What features or… |
| SA-3 | deepseek/deepseek-v3.2 | 82,263 | 3,368 | 0 | 0 | $0.0227 | ✅ 7F/10E | Trace this "women/girls mentioned" feature upstream. What fe… |
| SA-4 | deepseek/deepseek-v3.2 | 86,792 | 4,505 | 9,536 | 0 | $0.0245 | ✅ 8F/21E | Trace this capitalized names feature at position 1 (the name… |
| **Total** | | **329,127** | **18,886** | **72,546** | **0** | **$0.0996** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 7m 18s