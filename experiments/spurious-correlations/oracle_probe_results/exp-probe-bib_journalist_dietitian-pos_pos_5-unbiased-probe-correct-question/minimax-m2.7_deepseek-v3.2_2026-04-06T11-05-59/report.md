# Circuit Oracle Report
**Date:** 2026-04-06 11:05:59 UTC | **Orchestrator:** minimax/minimax-m2.7 | **Subagent:** deepseek/deepseek-v3.2

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-pos_pos_5 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "('The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession.',)"

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification is driven by a coherent circuit of genuine profession indicators—specifically, features detecting nutrition, diet, food, sports, and health concepts—rather than spurious gender markers.

**Confidence:** 9/10

**Reasoning:** The circuit traces reveal that the probe's classification score is driven by four key late-layer features (L4:F10494, L4:F13412, L14:F4197, L14:F16195) with strong direct effects (0.08-0.18), all encoding health/nutrition/food/diet concepts:

1. **L4:F13412** ("diets and dietary health", frac_nonzero=0.01216) receives its strongest input directly from the "nutrition" token at position 7 (edge weight=12.6875), with additional input from "sports" at position 6 (edge weight=3.89).

2. **L14:F4197** ("food insecurity", frac_nonzero=0.0152) similarly receives direct input from "nutrition" (weight=12.8125) and is part of a hierarchical pathway from earlier layers (L0→L1→L3→L4→L6→L9→L14) all encoding food/nutrition themes.

3. **L14:F16195** ("physical activity and training", frac_nonzero=0.01514) and **L4:F10494** ("health/medicine/diet/exercise", frac_nonzero=0.01174) complete the professional knowledge circuit.

**No gender markers found:** The pronoun "Her" at position 1 has negligible connections (weight=0.167 to 0.43) compared to the dominant nutrition/sports signals. The negative features (L0:F6051, L0:F8975) encode punctuation and code patterns, not gender suppression.

**Specificity:** All features have low frac_nonzero values (0.004-0.015), indicating they are selective and specific rather than generic pattern matchers. The most specific feature (L0:F5201, frac_nonzero=0.00026) is a dedicated detector for the literal token "nutrition."

**Conclusion:** The probe correctly identifies profession-relevant signals (nutrition, dietetics, sports nutrition consulting) from the text's explicit content, not from gender stereotypes. The circuit is a genuine, content-driven classifier.

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 10 features; top: L4:10494 de=0.176 |

### Dispatch: 7 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L4:F10494@7` | ✅ reported | 7 | 7 | Trace L4:F10494 at pos 7 - the highest direct effect feature. Identify what this… |
| SA-2 | `L4:F13412@7` | ✅ reported | 9 | 14 | Trace L4:F13412 at pos 7 - second highest direct effect feature. Identify what t… |
| SA-3 | `L14:F4197@7` | ✅ reported | 7 | 13 | Trace L14:F4197 at pos 7 - a later layer feature with strong direct effect. Iden… |
| SA-4 | `L0:F5201@7` | ✅ reported | 6 | 8 | Trace L0:F5201 at pos 7 - a negative upstream feature. Identify what this featur… |
| SA-5 | `L0:F6051@14` | ✅ reported | 1 | 5 | Trace L0:F6051 at pos 14 - a negative feature. Identify what this feature encode… |
| SA-6 | `L0:F8975@4` | ✅ reported | 3 | 5 | Trace L0:F8975 at pos 4 - a negative feature. Identify what this feature encodes… |
| SA-7 | `L14:F16195@7` | ✅ reported | 11 | 13 | Trace L14:F16195 at pos 7 - another strong positive feature at a late layer. Ide… |

<details>
<summary><b>SA-1</b> — tool trace (11 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F10494 | " words related to health, medicine, diet, drugs, age groups, and excer" |
| 2 | `get_upstream_features` | L4:F10494@7, k=5 | Emb:" nutrition"@7 (w=11.25) +4 more |
| 3 | `inspect_feature` | L1, F6461 | " technical language around physical activity, muscle function, and rel" |
| 4 | `inspect_feature` | L1, F760 | " scientific and medical terminology related to tissue and cells" |
| 5 | `inspect_feature` | L3, F6920 | "words related to consuming food, nutrients, and specific diets" |
| 6 | `get_upstream_features` | L1:F6461@7, k=5 | Emb:" sports"@6 (w=9.12) +4 more |
| 7 | `get_upstream_features` | L1:F760@7, k=5 | Emb:" nutrition"@7 (w=3.67) +4 more |
| 8 | `get_upstream_features` | L3:F6920@7, k=5 | Emb:" nutrition"@7 (w=10.19) +4 more |
| 9 | `inspect_feature` | L0, F7843 | " words related to nutrition and malnutrition" |
| 10 | `inspect_feature` | L0, F9026 | "technical documents or data, including numbers, units, and references " |
| 11 | `inspect_feature` | L0, F11835 | "terms used in software code such as "assembly", "using", "namespace", " |

**Findings:** The circuit tracing reveals that L4:F10494 at position 7 is a health/medicine/diet-related feature (frac_nonzero: 0.01174, moderately specific). It is primarily driven by the token "nutrition" at position 7 (edge weight 11.25, from embedding) and secondarily by "sports" at position 6 (edge weight 3.89).

Upstream features include:
1. L1:F6461: technical language around physical activity/muscle fun…

</details>

<details>
<summary><b>SA-2</b> — tool trace (13 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F13412 | " terms related to diets and dietary health" |
| 2 | `get_upstream_features` | L4:F13412@7, k=5 | Emb:" nutrition"@7 (w=12.69) +4 more |
| 3 | `inspect_feature` | L3, F6920 | "words related to consuming food, nutrients, and specific diets" |
| 4 | `inspect_feature` | L1, F6461 | " technical language around physical activity, muscle function, and rel" |
| 5 | `inspect_feature` | L1, F6631 | " words related to dietary patterns and scientific studies" |
| 6 | `get_upstream_features` | L3:F6920@7, k=5 | Emb:" nutrition"@7 (w=10.19) +4 more |
| 7 | `get_upstream_features` | L1:F6461@7, k=5 | Emb:" sports"@6 (w=9.12) +4 more |
| 8 | `get_upstream_features` | L1:F6631@7, k=5 | Emb:" nutrition"@7 (w=5.19) +4 more |
| 9 | `inspect_feature` | L0, F11835 | "terms used in software code such as "assembly", "using", "namespace", " |
| 10 | `inspect_feature` | L0, F5201 | " the word "nutrition"" |
| 11 | `inspect_feature` | L0, F9026 | "technical documents or data, including numbers, units, and references " |
| 12 | `inspect_feature` | L0, F10254 | " the word "sports"." |
| 13 | `inspect_feature` | L0, F7843 | " words related to nutrition and malnutrition" |

**Findings:** The tracing shows that L4:F13412 at position 7 is primarily a "nutrition" feature. Its strongest connection (weight=12.6875) is directly from the token " nutrition" at position 7. The feature has frac_nonzero=0.01216, indicating it's fairly specific. 

Key findings:
1. **NOT a spurious gender feature** - This feature is specifically about nutrition and diets, not gender. It detects the word "nutri…

</details>

<details>
<summary><b>SA-3</b> — tool trace (11 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L14, F4197 | " words and phrases related to food insecurity." |
| 2 | `get_upstream_features` | L14:F4197@7, k=5 | Emb:" nutrition"@7 (w=12.81) +4 more |
| 3 | `inspect_feature` | L6, F11327 | " words or phrases related to food or nutrition" |
| 4 | `inspect_feature` | L9, F15926 | "mentions about eating and meals" |
| 5 | `inspect_feature` | L4, F13412 | " terms related to diets and dietary health" |
| 6 | `get_upstream_features` | L6:F11327@7, k=5 | Emb:" nutrition"@7 (w=17.62) +4 more |
| 7 | `get_upstream_features` | L9:F15926@7, k=5 | Emb:" nutrition"@7 (w=8.00) +4 more |
| 8 | `inspect_feature` | L7, F13562 | " terms related to physical and mental training or conditioning" |
| 9 | `inspect_feature` | L7, F11540 | " scientific discussion of vitamins and minerals" |
| 10 | `get_upstream_features` | L4:F13412@7, k=5 | Emb:" nutrition"@7 (w=12.69) +4 more |
| 11 | `inspect_feature` | L3, F6920 | "words related to consuming food, nutrients, and specific diets" |

**Findings:** I traced L14:F4197 at position 7, which encodes "words and phrases related to food insecurity." This feature has a low frac_nonzero of 0.0152, indicating it's specific and selective. The circuit shows it primarily receives strong direct input from the "nutrition" token embedding (weight: 12.8125), with additional contributions from middle-layer features that all relate to food, nutrition, diets, a…

</details>

<details>
<summary><b>SA-4</b> — tool trace (9 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F5201 | " the word "nutrition"" |
| 2 | `get_upstream_features` | L0:F5201@7, k=5 | Emb:" nutrition"@7 (w=27.12) +4 more |
| 3 | `get_upstream_features` | L0:F5201@7, k=20 | Emb:" nutrition"@7 (w=27.12) +19 more |
| 4 | `inspect_feature` | L0, F3811 | "the word "handful"" |
| 5 | `inspect_feature` | L0, F2405 | " proper nouns, especially last names, and some location names or categ" |
| 6 | `inspect_feature` | L0, F1424 | " terms related to both family and paper cards" |
| 7 | `get_upstream_features` | L0:F5201@7, k=50 | Emb:" nutrition"@7 (w=27.12) +49 more |
| 8 | `inspect_feature` | L0, F8163 | " words and phrases related to societal and political issues" |
| 9 | `inspect_feature` | L0, F9910 | " words related to medical treatments, conditions, and studies" |

**Findings:** Traced L0:F5201 at position 7, which detects the word "nutrition" with very low frac_nonzero (0.00026), making it highly specific. The feature receives strong positive input from the token "nutrition" at position 7 (weight 27.125) and weaker positive inputs from surrounding tokens like "expertise", "sports", "areas", "include", and "Her". There's one weak negative connection from token "of" at pos…

</details>

<details>
<summary><b>SA-5</b> — tool trace (6 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F6051 | "periods, spaces, and the number 1" |
| 2 | `get_upstream_features` | L0:F6051@14, k=5 | Emb:"."@14 (w=47.00) +4 more |
| 3 | `get_upstream_features` | L0:F6051@14, k=20 | Emb:"."@14 (w=47.00) +19 more |
| 4 | `inspect_feature` | L0, F3811 | "the word "handful"" |
| 5 | `get_top_logits` | k=5 | "" (100%) |
| 6 | `inspect_feature` | L0, F6051 | "periods, spaces, and the number 1" |

**Findings:** L0:F6051 at position 14 is a basic punctuation detection feature that primarily detects periods (.). The feature has a strong direct connection from the '.' token embedding at position 14 (edge weight 47.0). It suppresses punctuation tokens like '.', ',', spaces, etc. and promotes various archaic/stylized tokens. There are weak negative connections from tokens like 'Her' (pos 1, edge weight -0.429…

</details>

<details>
<summary><b>SA-6</b> — tool trace (6 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F8975 | " the word "pragma" in code" |
| 2 | `get_upstream_features` | L0:F8975@4, k=5 | Emb:" expertise"@4 (w=20.88) +4 more |
| 3 | `get_upstream_features` | L0:F8975@4, k=10 | Emb:" expertise"@4 (w=20.88) +9 more |
| 4 | `inspect_feature` | L0, F2189 | " technical writing related to scientific studies" |
| 5 | `inspect_feature` | L0, F2208 | " the pronoun "Him" and the possessive pronoun "His" when used in a rel" |
| 6 | `inspect_feature` | L0, F1424 | " terms related to both family and paper cards" |

**Findings:** Tracing L0:F8975 at position 4 reveals a highly specific feature (frac_nonzero=0.00239) that encodes "the word 'pragma' in code" - detecting #pragma compiler directives in programming contexts. The feature is primarily driven by the token embedding " expertise" at position 4 (strong positive weight 20.875), with inhibitory connections from other tokens including "Her" at position 1 (weight -0.3281…

</details>

<details>
<summary><b>SA-7</b> — tool trace (15 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L14, F16195 | "mentions of physical activity and training." |
| 2 | `get_upstream_features` | L14:F16195@7, k=5 | Emb:" nutrition"@7 (w=7.97) +4 more |
| 3 | `inspect_feature` | L8, F7057 | " terms related to exercise, biology and chemistry" |
| 4 | `inspect_feature` | L7, F13562 | " terms related to physical and mental training or conditioning" |
| 5 | `inspect_feature` | L4, F10494 | " words related to health, medicine, diet, drugs, age groups, and excer" |
| 6 | `get_upstream_features` | L8:F7057@7, k=5 | Emb:" nutrition"@7 (w=8.88) +4 more |
| 7 | `inspect_feature` | L1, F6461 | " technical language around physical activity, muscle function, and rel" |
| 8 | `inspect_feature` | L7, F11540 | " scientific discussion of vitamins and minerals" |
| 9 | `get_upstream_features` | L4:F10494@7, k=5 | Emb:" nutrition"@7 (w=11.25) +4 more |
| 10 | `inspect_feature` | L1, F760 | " scientific and medical terminology related to tissue and cells" |
| 11 | `inspect_feature` | L3, F6920 | "words related to consuming food, nutrients, and specific diets" |
| 12 | `get_upstream_features` | L1:F6461@7, k=5 | Emb:" sports"@6 (w=9.12) +4 more |
| 13 | `inspect_feature` | L0, F7843 | " words related to nutrition and malnutrition" |
| 14 | `inspect_feature` | L0, F9747 | " code snippets dealing with user interfaces and visualizers" |
| 15 | `inspect_feature` | L0, F10254 | " the word "sports"." |

**Findings:** Tracing L14:F16195 at position 7 reveals a genuine profession-indicating circuit centered on sports and nutrition concepts. Key findings:

1. L14:F16195 encodes "mentions of physical activity and training" (frac_nonzero=0.01514, fairly specific) and promotes tokens like "Muscle", "muscles", "gyms".

2. The circuit has strong direct connections to input tokens:
   - "nutrition" at position 7 (edge_…

</details>

### Build

`build_circuit` → 21 nodes, 24 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m2.7 | 21,753 | 4,582 | 37,159 | 0 | $0.0131 | — | — |
| SA-1 | deepseek/deepseek-v3.2 | 72,853 | 2,815 | 0 | 0 | $0.0200 | ✅ 7F/7E | Trace L4:F10494 at pos 7 - the highest direct effect feature… |
| SA-3 | deepseek/deepseek-v3.2 | 73,436 | 3,203 | 0 | 0 | $0.0203 | ✅ 7F/13E | Trace L14:F4197 at pos 7 - a later layer feature with strong… |
| SA-2 | deepseek/deepseek-v3.2 | 91,503 | 3,580 | 0 | 0 | $0.0252 | ✅ 9F/14E | Trace L4:F13412 at pos 7 - second highest direct effect feat… |
| SA-4 | deepseek/deepseek-v3.2 | 52,013 | 4,881 | 11,968 | 0 | $0.0157 | ✅ 6F/8E | Trace L0:F5201 at pos 7 - a negative upstream feature. Ident… |
| SA-5 | deepseek/deepseek-v3.2 | 31,019 | 1,917 | 0 | 0 | $0.0088 | ✅ 1F/5E | Trace L0:F6051 at pos 14 - a negative feature. Identify what… |
| SA-6 | deepseek/deepseek-v3.2 | 30,866 | 2,101 | 0 | 0 | $0.0088 | ✅ 3F/5E | Trace L0:F8975 at pos 4 - a negative feature. Identify what … |
| SA-7 | deepseek/deepseek-v3.2 | 83,090 | 4,018 | 41,472 | 0 | $0.0242 | ✅ 11F/13E | Trace L14:F16195 at pos 7 - another strong positive feature … |
| **Total** | | **456,533** | **27,097** | **90,599** | **0** | **$0.1361** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 7m 18s