# Circuit Oracle Report
**Date:** 2026-04-06 09:07:31 UTC | **Orchestrator:** minimax/minimax-m2.7 | **Subagent:** deepseek/deepseek-v3.2

## Input

**Prompt:** "Dataset: bib_nurse_professor-pos_pos_5 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "('The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession.',)"

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score is primarily driven by **spurious gender marker features** rather than genuine profession indicators. The two dominant features are L18:F14677 ("instances of women or girls being mentioned") and L19:F9685 ("references to women's names and their roles or accomplishments"), which together contribute a combined direct effect of ~0.89 to the probe's output. These gender markers are activated by feminine pronouns ("She", "her"), the female name "Melissa", and even the word "nurse" which is stereotypically associated with women. In contrast, the only genuine profession indicator—L4:F13803 ("terms related to obstetrics and gynecology"), which detects the medical terms "Labor" and "Delivery"—has a comparable direct effect (~0.46) but operates through a completely separate pathway. The circuit reveals that the model exploits the correlation between gender and nursing as a profession rather than detecting actual professional qualifications.

**Confidence:** 9/10

**Reasoning:** The circuit built from `build_circuit` confirms the user's concern. The two most influential late-layer features driving the probe output are **L18:F14677** ("instances of women or girls being mentioned", direct_effect: 0.4453-0.5625) and **L19:F9685** ("references to women's names and their roles", direct_effect: 0.4414). Both features promote female pronouns ("herself", "she", "her") and suppress male pronouns ("himself", "his"), as confirmed by their `promoted_tokens` and `suppressed_tokens` fields from `inspect_feature`. 

The signal flow is clear:
1. **Gender marker path:** "She" at pos 54 and "Melissa" at pos 5 → female pronoun detection features (L0:F9519, L14:F12501) → gender marker features (L18:F14677, L19:F9685) → probe output. Notably, L19:F9685 is also directly activated by the "nurse" token at pos 12 (weight: 2.3281), showing the model uses the female-stereotyped occupation itself as a gender cue.

2. **Genuine profession path:** "Labor" (pos 9) + "Delivery" (pos 11) → birth/childbirth features (L3:F9008) → obstetrics/gynecology feature (L4:F13803) → probe output.

The model's reliance on gender markers rather than professional content represents a **shortcut** that exploits societal stereotypes about nursing being a female profession—a well-documented form of algorithmic bias in occupation classification systems.

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L12:14970 de=0.562 |
| 3 | `inspect_feature` ×8 | L12:14970, L4:1276, L18:14677, L19:9685, L0:7532, L4:13803, L7:8644, L13:11685 |

### Dispatch: 5 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L18:F14677@54` | ✅ reported | 7 | 10 | Trace the circuit from L18:F14677 ("instances of women or girls being mentioned"… |
| SA-2 | `L19:F9685@31` | ✅ reported | 11 | 14 | Trace the circuit from L19:F9685 ("references to women's names and their roles")… |
| SA-3 | `L4:F13803@11` | ✅ reported | 6 | 15 | Trace the circuit from L4:F13803 ("terms related to obstetrics and gynecology") … |
| SA-4 | `L4:F1276@5` | ✅ reported | 5 | 8 | Trace the circuit from L4:F1276 ("capitalized names and titles") at position 5 (… |
| SA-5 | `L12:F14970@5` | ✅ reported | 7 | 18 | Trace the circuit from L12:F14970 ("names of people, first and last names") at p… |

<details>
<summary><b>SA-1</b> — tool trace (12 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L18, F14677 | " instances of women or girls being mentioned" |
| 2 | `get_upstream_features` | L18:F14677@54, k=5 | Emb:" She"@54 (w=14.56) +4 more |
| 3 | `inspect_feature` | L17, F5889 | " references to people with pronouns and possessive pronouns" |
| 4 | `inspect_feature` | L15, F3330 | " personal stories of individuals, especially women and their actions o" |
| 5 | `inspect_feature` | L0, F15382 | "mentions of a female person." |
| 6 | `get_upstream_features` | L17:F5889@54, k=5 | Emb:" She"@54 (w=19.88) +4 more |
| 7 | `inspect_feature` | L13, F6622 | " pronouns." |
| 8 | `get_upstream_features` | L15:F3330@54, k=5 | Emb:" She"@54 (w=16.12) +4 more |
| 9 | `inspect_feature` | L0, F9519 | " the pronoun "she" and the possessive pronoun "her"" |
| 10 | `inspect_feature` | L0, F14257 | "the word 'newly' and adjectives ending in 'able'" |
| 11 | `get_upstream_features` | L0:F15382@54, k=5 | Emb:" She"@54 (w=23.50) +4 more |
| 12 | `get_upstream_features` | L13:F6622@54, k=5 | Emb:" She"@54 (w=13.38) +4 more |

**Findings:** The circuit tracing reveals that L18:F14677 ("instances of women or girls being mentioned") primarily detects the presence of the female pronoun "She" in the input. The feature gets strong direct input from the token embedding " She" at position 54 (edge_weight: 14.5625). Multiple upstream features at intermediate layers (L17, L15, L13, L0) also contribute, but all these features themselves primar…

</details>

<details>
<summary><b>SA-2</b> — tool trace (22 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L19, F9685 | " references to women's names and their roles or accomplishments." |
| 2 | `get_upstream_features` | L19:F9685@31, k=5 | Emb:" nurse"@12 (w=2.33) +4 more |
| 3 | `inspect_feature` | L18, F3679 | " personal pronouns and/or proper nouns" |
| 4 | `get_upstream_features` | L18:F3679@31, k=5 | L17:F3558 (w=3.59) +4 more |
| 5 | `inspect_feature` | L17, F3558 | " mentions of people's names or pronouns referring to people" |
| 6 | `get_upstream_features` | L17:F3558@31, k=5 | Emb:"<bos>"@0 (w=2.27) +4 more |
| 7 | `inspect_feature` | L14, F4385 | "proper nouns, pronouns, and some verbs." |
| 8 | `get_upstream_features` | L14:F4385@31, k=5 | L13:F4753 (w=2.48) +4 more |
| 9 | `inspect_feature` | L13, F4753 | " proper nouns, especially names of people" |
| 10 | `get_upstream_features` | L13:F4753@31, k=5 | Emb:"<bos>"@0 (w=3.97) +4 more |
| 11 | `inspect_feature` | L0, F7532 | " proper nouns" |
| 12 | `get_upstream_features` | L0:F7532@31, k=5 | Emb:" Melissa"@31 (w=22.25) +4 more |
| 13 | `inspect_feature` | L12, F15193 | " proper names" |
| 14 | `get_upstream_features` | L12:F15193@31, k=5 | L8:F576 (w=1.91) +4 more |
| 15 | `inspect_feature` | L8, F576 | " proper names" |
| 16 | `get_upstream_features` | L18:F3679@31, k=8 | L17:F3558 (w=3.59) +7 more |
| 17 | `get_upstream_features` | L19:F9685@31, k=10 | Emb:" nurse"@12 (w=2.33) +9 more |
| 18 | `inspect_feature` | L18, F9023 | " personal names and associated titles" |
| 19 | `inspect_feature` | L14, F12501 | " uses of the feminine pronoun." |
| 20 | `get_upstream_features` | L14:F12501@31, k=5 | Emb:" Melissa"@31 (w=3.73) +4 more |
| 21 | `inspect_feature` | L12, F14970 | " names of people, both first and last names" |
| 22 | `get_upstream_features` | L12:F14970@31, k=5 | Emb:"<bos>"@0 (w=-3.44) +4 more |

**Findings:** I traced the circuit from L19:F9685 ("references to women's names and their roles") upstream through multiple paths. Key findings:

1. **Direct embedding connections to L19:F9685**: The feature receives strong direct input from several embedding tokens:
   - " nurse" at position 12 (weight 2.3281) - suggests nursing as a stereotypically female profession influences gender detection
   - " Melissa"…

</details>

<details>
<summary><b>SA-3</b> — tool trace (10 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F13803 | " terms related to obstetrics and gynecology" |
| 2 | `get_upstream_features` | L4:F13803@11, k=5 | Emb:" Delivery"@11 (w=12.19) +4 more |
| 3 | `inspect_feature` | L3, F9008 | " words related to childbirth or birth in general, including in animals" |
| 4 | `get_upstream_features` | L3:F9008@11, k=5 | Emb:" Delivery"@11 (w=11.25) +4 more |
| 5 | `inspect_feature` | L3, F10398 | " the word "delivery" in the context of medical procedures or drug admi" |
| 6 | `inspect_feature` | L1, F12887 | "words related to the action of transmitting or supplying something" |
| 7 | `inspect_feature` | L1, F12174 | " words relating to ways things are conventionally done, potential prob" |
| 8 | `get_upstream_features` | L1:F12174@11, k=5 | Emb:" Labor"@9 (w=7.12) +4 more |
| 9 | `inspect_feature` | L2, F14771 | " the word "healthy" or the word "survive"" |
| 10 | `get_upstream_features` | L2:F14771@11, k=5 | Emb:" Delivery"@11 (w=20.12) +4 more |

**Findings:** Tracing the circuit for L4:F13803 ("terms related to obstetrics and gynecology") reveals a medical profession detection circuit primarily driven by the tokens " Delivery" (position 11) and " Labor" (position 9). The circuit shows both direct token-to-feature connections and indirect pathways:

1. **Primary pathway**: " Delivery" token → L3:F9008 ("childbirth/birth") → L4:F13803 ("obstetrics/gyneco…

</details>

<details>
<summary><b>SA-4</b> — tool trace (10 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F1276 | "capitalized names and titles, and names with lowercase letters in the " |
| 2 | `get_upstream_features` | L4:F1276@5, k=5 | Emb:" Melissa"@5 (w=9.62) +4 more |
| 3 | `inspect_feature` | L0, F7532 | " proper nouns" |
| 4 | `get_upstream_features` | L0:F7532@5, k=5 | Emb:" Melissa"@5 (w=21.25) +4 more |
| 5 | `inspect_feature` | L3, F3814 | " proper nouns, especially names of people" |
| 6 | `get_upstream_features` | L3:F3814@5, k=5 | L0:F7532 (w=6.50) +4 more |
| 7 | `inspect_feature` | L2, F5859 | " first names (mostly female)" |
| 8 | `get_upstream_features` | L2:F5859@5, k=5 | L0:F7532 (w=5.28) +4 more |
| 9 | `inspect_feature` | L2, F15413 | " proper names of people" |
| 10 | `get_upstream_features` | L2:F15413@5, k=5 | L0:F7532 (w=2.41) +4 more |

**Findings:** Tracing the circuit from L4:F1276 ("capitalized names and titles") at position 5 reveals a simple but important detection pathway for the name "Melissa". The circuit shows that the name detection starts at the embedding layer with the token " Melissa" directly feeding into early layer features that detect proper nouns. Specifically, L0:F7532 ("proper nouns") is a key early feature that detects the…

</details>

<details>
<summary><b>SA-5</b> — tool trace (13 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L12, F14970 | " names of people, both first and last names" |
| 2 | `get_upstream_features` | L12:F14970@5, k=10 | L4:F1276 (w=3.34) +9 more |
| 3 | `inspect_feature` | L4, F1276 | "capitalized names and titles, and names with lowercase letters in the " |
| 4 | `inspect_feature` | L0, F7532 | " proper nouns" |
| 5 | `get_upstream_features` | L4:F1276@5, k=10 | Emb:" Melissa"@5 (w=9.62) +9 more |
| 6 | `get_upstream_features` | L0:F7532@5, k=10 | Emb:" Melissa"@5 (w=21.25) +9 more |
| 7 | `get_upstream_features` | L0:F7532@1, k=5 | ❌ Feature (layer=0, feature_idx=7532) not found at pos=1. This |
| 8 | `inspect_feature` | L2, F5859 | " first names (mostly female)" |
| 9 | `get_upstream_features` | L2:F5859@5, k=10 | L0:F7532 (w=5.28) +9 more |
| 10 | `inspect_feature` | L6, F8166 | " proper names longer than 4 characters and ending in 'a', 'i', or 'e'" |
| 11 | `get_upstream_features` | L6:F8166@5, k=10 | L4:F1276 (w=5.19) +9 more |
| 12 | `inspect_feature` | L7, F3099 | " a variety of reference codes, abbreviations, and identifiers from dif" |
| 13 | `inspect_feature` | L6, F5355 | "names and identifiers" |

**Findings:** Tracing the circuit from L12:F14970 (name detection feature at position 5) reveals a clear hierarchy for name recognition. The feature receives strong positive input from: 1) L4:F1276 (capitalized names and titles), 2) L0:F7532 (proper nouns), and 3) directly from the embedding token " Melissa" at position 5. All paths converge on the embedding " Melissa" as the root source. The circuit shows spec…

</details>

### Build

`build_circuit` → 12 nodes, 11 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m2.7 | 35,175 | 4,595 | 57,314 | 0 | $0.0178 | — | — |
| SA-3 | deepseek/deepseek-v3.2 | 59,794 | 3,542 | 3,456 | 0 | $0.0170 | ✅ 6F/15E | Trace the circuit from L4:F13803 ("terms related to obstetri… |
| SA-1 | deepseek/deepseek-v3.2 | 82,465 | 3,535 | 4,480 | 0 | $0.0229 | ✅ 7F/10E | Trace the circuit from L18:F14677 ("instances of women or gi… |
| SA-2 | deepseek/deepseek-v3.2 | 189,699 | 5,582 | 20,544 | 0 | $0.0520 | ✅ 11F/14E | Trace the circuit from L19:F9685 ("references to women's nam… |
| SA-4 | deepseek/deepseek-v3.2 | 59,683 | 2,739 | 0 | 0 | $0.0166 | ✅ 5F/8E | Trace the circuit from L4:F1276 ("capitalized names and titl… |
| SA-5 | deepseek/deepseek-v3.2 | 93,553 | 4,079 | 0 | 0 | $0.0259 | ✅ 7F/18E | Trace the circuit from L12:F14970 ("names of people, first a… |
| **Total** | | **520,369** | **24,072** | **85,794** | **0** | **$0.1521** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 8m 59s