# Circuit Oracle Report
**Date:** 2026-04-06 10:58:39 UTC | **Orchestrator:** minimax/minimax-m2.7 | **Subagent:** deepseek/deepseek-v3.2

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-pos_pos_5 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "('The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession.',)"

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The Layer-22 probe classification score is driven primarily by **spurious gender markers** (female pronouns "Her" and "She", female name "Heather") rather than genuine profession indicators (dietary/nutrition terms). The strongest feature by direct effect is **L6:F11646** ("references to women", 0.2832) directly triggered by the "Her" token at position 1, followed by **L18:F14677** ("instances of women", 0.1709) triggered by "She" at position 15. In contrast, the only genuine profession indicator, **L4:F13412** ("terms related to diets", 0.1367), has a weaker direct effect and originates from the "nutrition" token at position 7. The circuit traces from gender token embeddings ("Her", "She", "Heather") through multiple layers of female-pronoun and women-detection features, while the nutrition/diet signal is much weaker and competes with inhibitory features (L3:F6920).

**Confidence:** 9/10

**Reasoning:** The circuit analysis confirms the user's concern with high confidence. The attribution graph reveals:

1. **Gender signals dominate**: The top two features driving the probe score are gender-detection features (L6:F11646 at 0.2832, L18:F14677 at 0.1709), both activated by female pronouns. L6:F11646 specifically detects "references to women" and promotes tokens like "herself", "she", "her" while suppressing male pronouns. L18:F14677 detects "instances of women or girls being mentioned" with similar token preferences.

2. **Direct embedding influence**: The female pronoun "Her" at position 1 has an extremely strong direct connection to the L6 feature (edge weight 18.125 from embedding), meaning the signal bypasses most processing and goes straight from the token to the gender detector. Similarly, "She" at position 15 connects to L18 with weight 15.3125.

3. **Weak profession signal**: The only genuine profession indicator (L4:F13412 "terms related to diets and dietary health") has a direct effect of only 0.1367, less than half the strength of the top gender feature. It originates from the "nutrition" token but competes with an inhibitory feature (L3:F6920, weight -1.6172).

4. **Specific, non-generic features**: All gender features have low frac_nonzero values (0.006-0.02), confirming they encode specific gender patterns rather than generic language features. The L7:F8644 feature ("woman's name") even shows an interesting dynamic where the "Heather" token triggers both a positive path (name detection) and a negative path (L5:F5996 promoting male pronouns), with the net effect being negative (-0.2129).

5. **Multi-pathway gender circuit**: The gender signal flows through multiple parallel pathways—direct pronoun detection (L0) → intermediate women references (L6) → complex women detection (L18)—demonstrating the circuit has learned to strongly associate female pronouns with the target classification.

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L6:11646 de=0.283 |
| 3 | `inspect_feature` ×5 | L6:11646, L7:8644, L18:14677, L12:14970, L4:13412 |

### Dispatch: 5 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L6:F11646@1` | ✅ reported | 9 | 14 | Trace this gender-referencing feature (L6:F11646, pos 1) upstream to understand … |
| SA-2 | `L18:F14677@15` | ✅ reported | 6 | 11 | Trace this women-referencing feature (L18:F14677, pos 15) upstream to understand… |
| SA-3 | `L4:F13412@7` | ✅ reported | 9 | 13 | Trace this diet/health feature (L4:F13412, pos 7) upstream - this is a genuine p… |
| SA-4 | `L7:F8644@46` | ✅ reported | 6 | 12 | Trace this woman's name feature (L7:F8644, pos 46) upstream - this appears to be… |
| SA-5 | `L4:F7864@1` | ✅ reported | 6 | 14 | Trace this intermediate feature (L4:F7864, pos 1) that bridges the Her token to … |

<details>
<summary><b>SA-1</b> — tool trace (14 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F11646 | " references to women, potentially triggered by pronouns and titles" |
| 2 | `get_upstream_features` | L6:F11646@1, k=5 | Emb:"Her"@1 (w=18.12) +4 more |
| 3 | `inspect_feature` | L4, F7864 | "xml or source code snippets, especially tags and possibly keywords in " |
| 4 | `inspect_feature` | L0, F15382 | "mentions of a female person." |
| 5 | `inspect_feature` | L3, F14972 | " the possessive pronoun "her"" |
| 6 | `inspect_feature` | L5, F6637 | " female first names with two syllables" |
| 7 | `get_upstream_features` | L4:F7864@1, k=5 | Emb:"Her"@1 (w=14.75) +4 more |
| 8 | `get_upstream_features` | L0:F15382@1, k=5 | Emb:"Her"@1 (w=23.12) +4 more |
| 9 | `get_upstream_features` | L3:F14972@1, k=5 | Emb:"Her"@1 (w=20.50) +4 more |
| 10 | `inspect_feature` | L2, F15388 | "references to an individual who is female, likely a main character" |
| 11 | `inspect_feature` | L2, F2128 | " pronouns, especially "he/him/it" equivalents like *er*, *ihn*, *es*, " |
| 12 | `inspect_feature` | L2, F13996 | "the pronoun 'her'" |
| 13 | `get_upstream_features` | L2:F2128@1, k=5 | Emb:"Her"@1 (w=22.38) +4 more |
| 14 | `inspect_feature` | L1, F12678 | " the pronoun "Her" and "She", and in one case the end of the word "end" |

**Findings:** The circuit analysis reveals that L6:F11646 (a feature detecting references to women) is primarily triggered directly by the input token "Her" at position 1, with a very strong edge weight of 18.125 from the token embedding. This is a genuine gender signal originating from the pronoun itself, not spurious profession-related. The feature also receives weaker positive inputs from L4:F7864 (3.33) and…

</details>

<details>
<summary><b>SA-2</b> — tool trace (13 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L18, F14677 | " instances of women or girls being mentioned" |
| 2 | `get_upstream_features` | L18:F14677@15, k=5 | Emb:" She"@15 (w=15.31) +4 more |
| 3 | `inspect_feature` | L17, F5889 | " references to people with pronouns and possessive pronouns" |
| 4 | `inspect_feature` | L6, F11646 | " references to women, potentially triggered by pronouns and titles" |
| 5 | `inspect_feature` | L15, F3330 | " personal stories of individuals, especially women and their actions o" |
| 6 | `get_upstream_features` | L6:F11646@15, k=5 | Emb:" She"@15 (w=18.50) +4 more |
| 7 | `inspect_feature` | L0, F15382 | "mentions of a female person." |
| 8 | `get_upstream_features` | L0:F15382@15, k=5 | Emb:" She"@15 (w=23.62) +4 more |
| 9 | `get_upstream_features` | L17:F5889@15, k=5 | Emb:" She"@15 (w=20.25) +4 more |
| 10 | `get_upstream_features` | L15:F3330@15, k=5 | Emb:" She"@15 (w=15.62) +4 more |
| 11 | `inspect_feature` | L0, F9519 | " the pronoun "she" and the possessive pronoun "her"" |
| 12 | `get_upstream_features` | L0:F9519@15, k=5 | Emb:" She"@15 (w=25.88) +4 more |
| 13 | `get_upstream_features` | L18:F14677@15, k=5 | Emb:" She"@15 (w=15.31) +4 more |

**Findings:** The tracing reveals a clear circuit where the gender signal originates from the input token " She" at position 15. This token is the primary driver of the women-referencing feature L18:F14677. 

Key findings:
1. The strongest direct connection to L18:F14677 is from the embedding of token " She" at position 15 (edge_weight: 15.3125)
2. Another strong connection is from token "Her" at position 1 (ed…

</details>

<details>
<summary><b>SA-3</b> — tool trace (13 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F13412 | " terms related to diets and dietary health" |
| 2 | `get_upstream_features` | L4:F13412@7, k=5 | Emb:" nutrition"@7 (w=12.69) +4 more |
| 3 | `inspect_feature` | L3, F6920 | "words related to consuming food, nutrients, and specific diets" |
| 4 | `inspect_feature` | L1, F6461 | " technical language around physical activity, muscle function, and rel" |
| 5 | `inspect_feature` | L1, F6631 | " words related to dietary patterns and scientific studies" |
| 6 | `get_upstream_features` | L3:F6920@7, k=5 | Emb:" nutrition"@7 (w=10.19) +4 more |
| 7 | `inspect_feature` | L0, F11835 | "terms used in software code such as "assembly", "using", "namespace", " |
| 8 | `inspect_feature` | L0, F5201 | " the word "nutrition"" |
| 9 | `get_upstream_features` | L1:F6631@7, k=5 | Emb:" nutrition"@7 (w=5.19) +4 more |
| 10 | `inspect_feature` | L0, F9026 | "technical documents or data, including numbers, units, and references " |
| 11 | `inspect_feature` | L0, F10254 | " the word "sports"." |
| 12 | `inspect_feature` | L0, F7093 | "words associated with having or gaining an understanding or perspectiv" |
| 13 | `get_upstream_features` | L0:F5201@7, k=5 | Emb:" nutrition"@7 (w=27.12) +4 more |

**Findings:** The diet/health profession indicator (L4:F13412) originates primarily from the token "nutrition" itself. The strongest connection is a direct edge from the "nutrition" token embedding (edge weight 12.6875). There's also a secondary pathway: a layer 0 feature that specifically detects the word "nutrition" (F5201, frac_nonzero=0.00026) feeds into a layer 3 feature about food/nutrients (F6920), which…

</details>

<details>
<summary><b>SA-4</b> — tool trace (11 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L7, F8644 | " woman's name in a variety of contexts" |
| 2 | `get_upstream_features` | L7:F8644@46, k=5 | Emb:" She"@15 (w=4.03) +4 more |
| 3 | `inspect_feature` | L6, F11646 | " references to women, potentially triggered by pronouns and titles" |
| 4 | `inspect_feature` | L4, F1276 | "capitalized names and titles, and names with lowercase letters in the " |
| 5 | `inspect_feature` | L5, F5996 | " words associated with females, femininity or womanhood" |
| 6 | `get_upstream_features` | L6:F11646@15, k=5 | Emb:" She"@15 (w=18.50) +4 more |
| 7 | `get_upstream_features` | L4:F1276@46, k=5 | Emb:" Heather"@46 (w=11.12) +4 more |
| 8 | `inspect_feature` | L0, F7532 | " proper nouns" |
| 9 | `get_upstream_features` | L5:F5996@46, k=5 | Emb:" Heather"@46 (w=2.81) +4 more |
| 10 | `inspect_feature` | L0, F15382 | "mentions of a female person." |
| 11 | `get_upstream_features` | L0:F15382@15, k=5 | Emb:" She"@15 (w=23.62) +4 more |

**Findings:** The woman's name detection feature at L7:F8644 (position 46) is triggered by multiple input tokens: primarily the female name "Heather" at position 46, and the female pronouns " She" at position 15 and "Her" at position 1. The circuit shows an interesting dynamic: "Heather" directly triggers both the name pattern feature (L4:F1276) which positively feeds into the woman's name detector, AND a compe…

</details>

<details>
<summary><b>SA-5</b> — tool trace (11 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F7864 | "xml or source code snippets, especially tags and possibly keywords in " |
| 2 | `get_upstream_features` | L4:F7864@1, k=5 | Emb:"Her"@1 (w=14.75) +4 more |
| 3 | `inspect_feature` | L2, F2128 | " pronouns, especially "he/him/it" equivalents like *er*, *ihn*, *es*, " |
| 4 | `inspect_feature` | L2, F13996 | "the pronoun 'her'" |
| 5 | `get_upstream_features` | L2:F2128@1, k=5 | Emb:"Her"@1 (w=22.38) +4 more |
| 6 | `get_upstream_features` | L2:F13996@1, k=5 | Emb:"Her"@1 (w=21.50) +4 more |
| 7 | `inspect_feature` | L1, F12678 | " the pronoun "Her" and "She", and in one case the end of the word "end" |
| 8 | `get_upstream_features` | L1:F12678@1, k=5 | Emb:"Her"@1 (w=18.88) +4 more |
| 9 | `inspect_feature` | L0, F9519 | " the pronoun "she" and the possessive pronoun "her"" |
| 10 | `inspect_feature` | L0, F15382 | "mentions of a female person." |
| 11 | `get_upstream_features` | L0:F9519@1, k=5 | Emb:"Her"@1 (w=16.62) +4 more |

**Findings:** Tracing L4:F7864 reveals a complex circuit that processes the "Her" token for gender detection. The feature at L4:F7864 acts as an intermediate node that receives inputs from both pronoun detection features (L2:F2128 for general pronouns including "her", and L2:F13996 specifically for "her") and early gender detection features. Interestingly, L2:F2128 promotes both male ("he/him") and female ("she…

</details>

### Build

`build_circuit` → 16 nodes, 18 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m2.7 | 30,871 | 4,037 | 40,295 | 0 | $0.0153 | — | — |
| SA-2 | deepseek/deepseek-v3.2 | 84,491 | 3,265 | 6,464 | 0 | $0.0234 | ✅ 6F/11E | Trace this women-referencing feature (L18:F14677, pos 15) up… |
| SA-3 | deepseek/deepseek-v3.2 | 83,777 | 4,002 | 12,864 | 0 | $0.0236 | ✅ 9F/13E | Trace this diet/health feature (L4:F13412, pos 7) upstream -… |
| SA-1 | deepseek/deepseek-v3.2 | 99,966 | 3,758 | 9,024 | 0 | $0.0277 | ✅ 9F/14E | Trace this gender-referencing feature (L6:F11646, pos 1) ups… |
| SA-5 | deepseek/deepseek-v3.2 | 72,304 | 2,914 | 0 | 0 | $0.0199 | ✅ 6F/14E | Trace this intermediate feature (L4:F7864, pos 1) that bridg… |
| SA-4 | deepseek/deepseek-v3.2 | 72,825 | 3,029 | 0 | 0 | $0.0201 | ✅ 6F/12E | Trace this woman's name feature (L7:F8644, pos 46) upstream … |
| **Total** | | **444,234** | **21,005** | **68,647** | **0** | **$0.1300** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 5m 59s