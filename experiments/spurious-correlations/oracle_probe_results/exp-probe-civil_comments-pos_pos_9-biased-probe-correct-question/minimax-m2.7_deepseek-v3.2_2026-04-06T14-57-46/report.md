# Circuit Oracle Report
**Date:** 2026-04-06 14:57:46 UTC | **Orchestrator:** minimax/minimax-m2.7 | **Subagent:** deepseek/deepseek-v3.2

## Input

**Prompt:** "Dataset: civil_comments-pos_pos_9 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "('The circuit use spurious features (e.g.,"an identity group" signals) rather than actual prompt content (lexical or semaintical) to predict toxicity.',)"

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's toxicity classification is driven primarily by identity group mentions (the word "white" at position 9 and "guy" at position 10) through a cascade of race/ethnicity features (L2:F13158 → L3:F13061/L3:F16373 → L4:F117 → L6:F3902), rather than by semantic toxic language patterns. A secondary path detects "last name" mentions, while only a minor authorship reference feature (L1:F5220) provides slight negative correction. The circuit shows severe reliance on spurious identity signals over actual toxic content.

**Confidence:** 9

**Reasoning:** The attribution circuit reveals a fundamental problem with the probe's decision-making. The strongest positive contributions to the toxicity score come from:

1. **" white" token → race/ethnicity features cascade**: The token " white" (pos 9) directly activates multiple features encoding race, ethnicity, and social issues with very high edge weights (13.5-17.9). L2:F13158 ("words about race and ethnicity") with frac_nonzero=0.00986 feeds into L3:F13061 ("words related to race, gender and social issues") and L4:F117 ("terms related to race, racism, and social justice, with focus on Black people"), which then feed into L6:F3902 ("terms referring to race and ethnicity"). These features have low frac_nonzero values (0.009-0.018), indicating selective, specific detectors rather than generic toxic patterns.

2. **" guy" token → gendered words**: The token " guy" (pos 10) activates L2:F15317 ("gendered words with bias toward female") which contributes to the race/gender social issues feature.

3. **" last name" → name detection**: The phrase "last name" (pos 14-15) triggers L3:F4512 ("mentions of first names, last names") with extremely high activation (52.0).

The only non-identity feature contributing meaningfully is L1:F5220 ("references to authors and publications", direct_effect=-0.455), which detects the sentence structure "The author appears..." and provides slight negative correction.

The user's concern is fully validated: the probe's classification relies on spurious identity group signals rather than actual toxic language semantics. The toxic content ("self hater," "oriental," "lust after white men") is not captured by the circuit — instead, the mere presence of the word "white" triggers a cascade of race-detection features that drive the toxicity score. This is a textbook example of a model using demographic markers as proxies for toxicity rather than analyzing the actual hateful claims.

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L1:5220 de=-0.455 |

### Dispatch: 8 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L3:F13061@10` | ✅ reported | 6 | 11 | Trace this feature's upstream circuit. What does this feature encode? Where does… |
| SA-2 | `L6:F3902@9` | ✅ reported | 8 | 11 | Trace this feature's upstream circuit. What does this feature encode? Where does… |
| SA-3 | `L1:F5220@2` | ✅ reported | 4 | 8 | Trace this feature's upstream circuit. This has the strongest negative direct ef… |
| SA-4 | `L4:F117@10` | ✅ reported | 11 | 20 | Trace this feature's upstream circuit. What does this feature encode? Where does… |
| SA-5 | `L3:F4512@15` | ✅ reported | 7 | 8 | Trace this feature's upstream circuit. This has a high activation (52.0). What d… |
| SA-6 | `L1:F384@2` | ✅ reported | 4 | 11 | Trace this feature's upstream circuit. What does this feature encode? Where does… |
| SA-7 | `L1:F6576@3` | ✅ reported | 3 | 7 | Trace this feature's upstream circuit. What does this feature encode? Where does… |
| SA-8 | `L1:F9113@9` | ✅ reported | 4 | 20 | Trace this feature's upstream circuit. This has a negative direct effect (-0.195… |

<details>
<summary><b>SA-1</b> — tool trace (10 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L3, F13061 | " words related to race, gender and social issues" |
| 2 | `get_upstream_features` | L3:F13061@10, k=5 | Emb:" white"@9 (w=11.06) +4 more |
| 3 | `inspect_feature` | L2, F13158 | " words about race and ethnicity" |
| 4 | `inspect_feature` | L2, F15317 | " gendered words, with a slight bias toward female-gendered words" |
| 5 | `inspect_feature` | L0, F9076 | " mentions of men, boys, areas, or general locations in a text" |
| 6 | `get_upstream_features` | L2:F13158@9, k=5 | Emb:" white"@9 (w=13.62) +4 more |
| 7 | `inspect_feature` | L1, F7821 | " mentions of computer fans." |
| 8 | `get_upstream_features` | L2:F15317@10, k=5 | Emb:" guy"@10 (w=9.44) +4 more |
| 9 | `inspect_feature` | L1, F13023 | " the word, "transition" in the context of scientific documents" |
| 10 | `get_upstream_features` | L0:F9076@10, k=5 | Emb:" white"@9 (w=7.88) +4 more |

**Findings:** Tracing the upstream circuit from L3:F13061 ("words related to race, gender and social issues") reveals a clear pattern: This feature primarily encodes identity group mentions, specifically racial and gendered terms. 

The circuit originates from two main input tokens: "white" at position 9 and "guy" at position 10. The strongest signal comes directly from the "white" token embedding feeding into …

</details>

<details>
<summary><b>SA-2</b> — tool trace (11 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F3902 | " terms referring to race and ethnicity" |
| 2 | `get_upstream_features` | L6:F3902@9, k=5 | Emb:" white"@9 (w=13.56) +4 more |
| 3 | `inspect_feature` | L4, F117 | " terms related to race, racism, and social justice, with a particular " |
| 4 | `inspect_feature` | L4, F15204 | " art galleries, museums and the White House" |
| 5 | `get_upstream_features` | L4:F117@9, k=5 | Emb:" white"@9 (w=15.06) +4 more |
| 6 | `inspect_feature` | L3, F11768 | " the word "white" and related contexts such as diversity" |
| 7 | `inspect_feature` | L2, F13158 | " words about race and ethnicity" |
| 8 | `get_upstream_features` | L2:F13158@9, k=5 | Emb:" white"@9 (w=13.62) +4 more |
| 9 | `inspect_feature` | L1, F7821 | " mentions of computer fans." |
| 10 | `inspect_feature` | L2, F585 | "the word "white", often in association with "dwarf"" |
| 11 | `inspect_feature` | L5, F9988 | " the color "white" and terms related to race/ethnicity, or testimony Q" |

**Findings:** The starting feature L6:F3902 encodes "terms referring to race and ethnicity" with low sparsity (0.01786), promoting tokens like "minorities", "minority", "ethnicity". Tracing upstream reveals the circuit originates strongly from the token " white" at position 9, which directly feeds into multiple features with high edge weights (13.56 to L6, 15.06 to L4, 13.63 to L2).

The circuit shows a clear p…

</details>

<details>
<summary><b>SA-3</b> — tool trace (8 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L1, F5220 | " references to authors and publications" |
| 2 | `get_upstream_features` | L1:F5220@2, k=5 | Emb:" author"@2 (w=19.12) +4 more |
| 3 | `inspect_feature` | L0, F11419 | " references to pens and ink" |
| 4 | `inspect_feature` | L0, F7672 | " words related to reading and publishing like books, readers, companie" |
| 5 | `get_upstream_features` | L0:F11419@2, k=5 | Emb:" author"@2 (w=9.00) +4 more |
| 6 | `get_upstream_features` | L0:F7672@2, k=5 | Emb:"The"@1 (w=7.34) +4 more |
| 7 | `inspect_feature` | L0, F14136 | " occurrences of the word 'read' and words relating to authorship" |
| 8 | `get_upstream_features` | L0:F14136@2, k=5 | Emb:" author"@2 (w=10.69) +4 more |

**Findings:** The circuit traces back to the token embedding for " author" at position 2. This feature (L1:F5220) encodes "references to authors and publications" and shows a clear pattern of distinguishing singular English author references from non-English content. Key findings:

1. The strongest signal comes directly from the " author" token embedding (weight 19.125)
2. Layer 0 features feed into it with bot…

</details>

<details>
<summary><b>SA-4</b> — tool trace (15 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F117 | " terms related to race, racism, and social justice, with a particular " |
| 2 | `get_upstream_features` | L4:F117@10, k=5 | Emb:" white"@9 (w=12.12) +4 more |
| 3 | `inspect_feature` | L3, F13061 | " words related to race, gender and social issues" |
| 4 | `inspect_feature` | L3, F16373 | " mentions of demographic identity, especially race and gender" |
| 5 | `get_upstream_features` | L3:F13061@10, k=5 | Emb:" white"@9 (w=11.06) +4 more |
| 6 | `get_upstream_features` | L3:F16373@10, k=5 | Emb:" white"@9 (w=23.88) +4 more |
| 7 | `inspect_feature` | L2, F13158 | " words about race and ethnicity" |
| 8 | `inspect_feature` | L2, F15317 | " gendered words, with a slight bias toward female-gendered words" |
| 9 | `inspect_feature` | L0, F9076 | " mentions of men, boys, areas, or general locations in a text" |
| 10 | `inspect_feature` | L0, F3024 | "the word "guy"" |
| 11 | `get_upstream_features` | L2:F13158@9, k=5 | Emb:" white"@9 (w=13.62) +4 more |
| 12 | `inspect_feature` | L1, F7821 | " mentions of computer fans." |
| 13 | `inspect_feature` | L1, F1480 | "the color 'white', sometimes in a context involving race" |
| 14 | `inspect_feature` | L1, F13023 | " the word, "transition" in the context of scientific documents" |
| 15 | `inspect_feature` | L2, F15073 | " words related to extremes, whether positive or negative in connotatio" |

**Findings:** This circuit traces a feature encoding race-related terms with focus on Black people (L4:F117). The signal originates primarily from the token " white" at position 9, with massive edge weights (12.125 to L4:F117, 23.875 to L3:F16373). This indicates the feature is triggered when the model sees "white" in contexts that lead to race-related processing.

Key findings:
1. The starting feature (L4:F117…

</details>

<details>
<summary><b>SA-5</b> — tool trace (13 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L3, F4512 | " mentions of first names, last names, and phone numbers" |
| 2 | `get_upstream_features` | L3:F4512@15, k=5 | Emb:" last"@14 (w=24.62) +4 more |
| 3 | `inspect_feature` | L2, F9961 | " html elements containing the word "name"" |
| 4 | `inspect_feature` | L2, F10248 | "the word "name"" |
| 5 | `get_upstream_features` | L2:F9961@15, k=5 | Emb:" name"@15 (w=18.12) +4 more |
| 6 | `get_upstream_features` | L2:F10248@15, k=5 | Emb:" name"@15 (w=18.38) +4 more |
| 7 | `inspect_feature` | L1, F12512 | "the word "name"" |
| 8 | `inspect_feature` | L0, F1142 | " the word "last" and the word "finally" or "next" within a short range" |
| 9 | `inspect_feature` | L0, F14204 | "the attribute "name" when it appears inside of HTML" |
| 10 | `get_upstream_features` | L0:F1142@14, k=5 | Emb:" last"@14 (w=35.50) +4 more |
| 11 | `get_upstream_features` | L0:F14204@15, k=5 | Emb:" name"@15 (w=13.25) +4 more |
| 12 | `get_upstream_features` | L1:F12512@15, k=5 | Emb:" name"@15 (w=19.62) +4 more |
| 13 | `inspect_feature` | L1, F4380 | "the word "name" in code contexts" |

**Findings:** The feature L3:F4512 encodes "mentions of first names, last names, and phone numbers" with high activation (52.0) at position 15. Tracing its upstream circuit reveals that:

1. The feature primarily receives direct input from token embeddings: " last" at position 14 (edge_weight 24.625) and " name" at position 15 (edge_weight 11.5625).

2. The circuit originates from the specific tokens "last name…

</details>

<details>
<summary><b>SA-6</b> — tool trace (7 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L1, F384 | " the string "ash" or "pund"" |
| 2 | `get_upstream_features` | L1:F384@2, k=5 | Emb:" author"@2 (w=13.94) +4 more |
| 3 | `inspect_feature` | L0, F753 | "the word "author" and words related to selling and prices" |
| 4 | `inspect_feature` | L0, F3612 | "the words "author", "authority", and "agency", often in a legal or aca" |
| 5 | `inspect_feature` | L0, F11009 | "the word "author" and related words like "book."" |
| 6 | `get_upstream_features` | L0:F753@2, k=5 | Emb:" author"@2 (w=18.38) +4 more |
| 7 | `get_upstream_features` | L0:F3612@2, k=5 | Emb:" author"@2 (w=16.62) +4 more |

**Findings:** This circuit traces the upstream origin of L1:F384 which encodes the string "ash" or "pund". The primary signal originates from the token "author" at position 2, which strongly activates (edge_weight 13.9375) the L1 feature directly from the embedding level. Additionally, layer 0 features (F753, F3612, F11009) that detect "author" and related words also feed into the L1 feature with moderate posit…

</details>

<details>
<summary><b>SA-7</b> — tool trace (6 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L1, F6576 | " the word "appearance"" |
| 2 | `get_upstream_features` | L1:F6576@3, k=5 | Emb:" appears"@3 (w=19.00) +4 more |
| 3 | `inspect_feature` | L0, F1998 | " occurrences of the word "seem" or "is" or "are."" |
| 4 | `inspect_feature` | L0, F5294 | " database insert operations" |
| 5 | `get_upstream_features` | L0:F1998@3, k=5 | Emb:" appears"@3 (w=14.50) +4 more |
| 6 | `get_upstream_features` | L0:F5294@3, k=5 | Emb:" appears"@3 (w=14.88) +4 more |

**Findings:** This circuit traces a feature that detects the word \"appearance\". The L1 feature (6576) primarily receives its signal directly from the embedding of the token \" appears\" at position 3 (very strong weight 19.0). It also receives weaker positive influence from a layer 0 feature that detects words like \"seem/is/are\" (1998, weight 0.5078) and negative influence from a layer 0 feature for \"datab…

</details>

<details>
<summary><b>SA-8</b> — tool trace (10 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L1, F9113 | " discussions about race and slavery" |
| 2 | `get_upstream_features` | L1:F9113@9, k=5 | Emb:" white"@9 (w=14.44) +4 more |
| 3 | `inspect_feature` | L0, F3436 | " mentions of the word "white"" |
| 4 | `inspect_feature` | L0, F16013 | " mentions of the color blue, and perhaps colors in general or the comp" |
| 5 | `inspect_feature` | L0, F13663 | "mentions of pregnancy and related terms" |
| 6 | `get_upstream_features` | L0:F3436@9, k=5 | Emb:" white"@9 (w=17.88) +4 more |
| 7 | `get_upstream_features` | L0:F16013@9, k=5 | Emb:" white"@9 (w=15.50) +4 more |
| 8 | `get_upstream_features` | L0:F13663@9, k=5 | Emb:" white"@9 (w=15.06) +4 more |
| 9 | `get_top_logits` | k=5 | "" (100%) |
| 10 | `get_top_features` | token=" the", k=10 | ❌ Token ' the' not found in top logits. Available: [''] |

**Findings:** Tracing the upstream circuit of L1:F9113 which encodes "discussions about race and slavery" with negative direct effect (-0.195). Key findings:
1. The strongest upstream signal comes directly from the token embedding " white" at position 9 (weight: 14.44 positive)
2. A negative signal comes from token " married" at position 6 (weight: -0.70)
3. Layer 0 feature F3436 (detects "white" mentions) feed…

</details>

### Build

`build_circuit` → 17 nodes, 24 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m2.7 | 23,539 | 4,322 | 40,743 | 0 | $0.0135 | — | — |
| SA-3 | deepseek/deepseek-v3.2 | 41,557 | 2,490 | 3,584 | 0 | $0.0118 | ✅ 4F/8E | Trace this feature's upstream circuit. This has the stronges… |
| SA-1 | deepseek/deepseek-v3.2 | 50,108 | 2,746 | 12,736 | 0 | $0.0144 | ✅ 6F/11E | Trace this feature's upstream circuit. What does this featur… |
| SA-5 | deepseek/deepseek-v3.2 | 94,733 | 3,001 | 0 | 0 | $0.0258 | ✅ 7F/8E | Trace this feature's upstream circuit. This has a high activ… |
| SA-2 | deepseek/deepseek-v3.2 | 69,819 | 3,518 | 4,352 | 0 | $0.0196 | ✅ 8F/11E | Trace this feature's upstream circuit. What does this featur… |
| SA-4 | deepseek/deepseek-v3.2 | 118,525 | 4,285 | 0 | 0 | $0.0324 | ✅ 11F/20E | Trace this feature's upstream circuit. What does this featur… |
| SA-6 | deepseek/deepseek-v3.2 | 38,404 | 2,210 | 0 | 0 | $0.0108 | ✅ 4F/11E | Trace this feature's upstream circuit. What does this featur… |
| SA-7 | deepseek/deepseek-v3.2 | 27,265 | 2,517 | 3,136 | 0 | $0.0081 | ✅ 3F/7E | Trace this feature's upstream circuit. What does this featur… |
| SA-8 | deepseek/deepseek-v3.2 | 59,574 | 3,780 | 0 | 0 | $0.0169 | ✅ 4F/20E | Trace this feature's upstream circuit. This has a negative d… |
| **Total** | | **523,524** | **28,869** | **64,551** | **0** | **$0.1534** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 6m 41s