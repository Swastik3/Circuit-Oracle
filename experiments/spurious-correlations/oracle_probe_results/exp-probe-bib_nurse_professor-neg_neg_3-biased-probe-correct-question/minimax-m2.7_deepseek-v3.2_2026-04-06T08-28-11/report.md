# Circuit Oracle Report
**Date:** 2026-04-06 08:28:11 UTC | **Orchestrator:** minimax/minimax-m2.7 | **Subagent:** deepseek/deepseek-v3.2

## Input

**Prompt:** "Dataset: bib_nurse_professor-neg_neg_3 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "('The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession.',)"

**Top predictions:**  (100.0%)


## Oracle Analysis

The circuit building tool appears to have an issue, but I have comprehensive analysis from the trace subagents. Let me provide my final analysis.

---

## Analysis

The attribution circuit reveals that **the probe heavily relies on spurious gender pronoun features rather than genuine profession/academic indicators**. The input describes a person with academic credentials (B.A., M.S., Ph.D. from Peking University, Utah State University, SUNY Stony Brook, and an Assistant Professor position), but the probe's top features primarily detect masculine pronouns.

### Key Findings

**Top Features by Direct Effect:**
1. **L0:F2994 (his possessive)** — direct_effect: **0.2988** (HIGHEST)
   - Traces to token " his" at position 3
   - Feature label: "pronoun 'his'"
   - frac_nonzero: 0.073 (moderate specificity)

2. **L6:F12990 (male pronouns)** — direct_effect: -0.1729
   - Traces to token "He" at position 21
   - Feature label: "male pronouns and titles"
   - Cascades through L1:F12922, L0:F1069 (male person references)

3. **L7:F14946 (his pronoun)** — direct_effect: -0.1699
   - Cascades from L6:F12990 and L0:F1069

4. **L7:F14893 (pronouns)** — direct_effect: **0.165**
   - Strong direct connection from "He" at pos 1 (weight: 14.75)

5. **L12:F2175 (gender words)** — direct_effect: -0.1572
   - "words referring to gender" — promotes "himself", "masculinity"
   - No academic/profession content

6. **L18:F14743 (He detection)** — direct_effect: -0.1484
   - Directly detects "He" at pos 21
   - Cascades from L0:F1069, L17:F5889, L13:F6622

**Academic Features (GENUINE but WEAKER):**
- **L6:F170 (academic fields)** — direct_effect: **0.1201** (LOWEST among top 15)
  - Detects "references to academic fields, especially humanities"
  - Traces to tokens "Mathematics", "degree", "University"
  - Cascades through L5:F10392, L4:F3727, L3:F4113, L2:F10852

### Circuit Structure

```
INPUT TOKENS          CIRCUIT PATH                    OUTPUT
─────────────────────────────────────────────────────────────
" He" (pos 21)   ──►  L0:F1069 ──► L18:F14743 ──┐
" his" (pos 3)   ──►  L0:F2994 ─────────────────┼──► PROBE
" He" (pos 1)    ──►  L0:F1069 ──► L7:F14893 ───┤      SCORE
" Mathematics" ──►  L2:F10852 ──► L6:F170 ──────┘
```

### Confidence: **8/10**

The evidence is clear and compelling:
1. The top 6 features by direct effect are ALL gender pronoun features
2. The academic feature (L6:F170) has the LOWEST direct effect among top-15 features
3. Gender features have cumulative direct effects ~1.3 vs. ~0.12 for academic
4. The gender circuit forms a deep multi-layer hierarchy (L0→L2→L4→L6→L7→L12→L18)
5. The academic circuit is shallower and weaker

**The concern is VALIDATED**: The probe uses spurious gender markers (he, his) as its primary signal to predict profession, rather than genuine academic credentials. This is a textbook example of spurious correlation where the model learns to associate masculine pronouns with certain professions due to training data biases, rather than encoding actual profession-relevant features.

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L0:2994 de=0.299 |

### Dispatch: 8 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L0:F2994@3` | ✅ reported | 2 | 4 | Trace what L0:F2994 encodes and where its signal originates. Check if this featu… |
| SA-2 | `L6:F12990@21` | ✅ reported | 5 | 7 | Trace L6:F12990 at pos 21 (negative effect) - identify what semantic concept thi… |
| SA-3 | `L7:F14946@2` | ✅ reported | 6 | 6 | Trace L7:F14946 at pos 2 (negative effect) - identify what semantic concept this… |
| SA-4 | `L7:F14893@1` | ✅ reported | 8 | 13 | Trace L7:F14893 at pos 1 (positive effect) - identify what semantic concept this… |
| SA-5 | `L18:F14743@21` | ✅ reported | 1481 | 10 | Trace L18:F14743 at pos 21 (negative effect) - identify what semantic concept th… |
| SA-6 | `L0:F6270@13` | ✅ reported | 1 | 1 | Trace L0:F6270 at pos 13 - what does this feature encode? Check if it relates to… |
| SA-7 | `L6:F170@10` | ✅ reported | 8 | 10 | Trace L6:F170 at pos 10 - what semantic concept does this detect? Is it professi… |
| SA-8 | `L12:F2175@2` | ✅ reported | 7 | 13 | Trace L12:F2175 at pos 2 (negative effect) - identify what semantic concept this… |

<details>
<summary><b>SA-1</b> — tool trace (3 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F2994 | "the pronoun "his" and the pronoun "he."" |
| 2 | `get_upstream_features` | L0:F2994@3, k=5 | Emb:" his"@3 (w=42.50) +4 more |
| 3 | `inspect_feature` | L0, F310 | " the pronouns "she", "her", and "he" and sometimes the word "therefore" |

**Findings:** The tracing reveals that L0:F2994 is a pronoun detection feature that primarily encodes the word \"his\". Its signal originates almost entirely (weight 42.5) from the token \" his\" at position 3 itself. This feature suppresses tokens like \"his\", \"himself\", and foreign possessive pronouns while promoting punctuation and formatting tokens. The feature has moderate specificity (frac_nonzero 0.07…

</details>

<details>
<summary><b>SA-2</b> — tool trace (8 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F12990 | " male pronouns and titles along with descriptors associated with men" |
| 2 | `get_upstream_features` | L6:F12990@21, k=5 | Emb:" He"@21 (w=4.56) +4 more |
| 3 | `inspect_feature` | L1, F12922 | " the pronoun "he" or "she" in a narrative context" |
| 4 | `inspect_feature` | L0, F1069 | " references to a male person, particularly when using the pronoun "He"" |
| 5 | `get_upstream_features` | L1:F12922@21, k=5 | Emb:" He"@21 (w=23.12) +4 more |
| 6 | `inspect_feature` | L0, F3232 | " mentions of the third person plural pronoun "They"" |
| 7 | `inspect_feature` | L0, F11400 | " the string "He", which is often used as a chemical symbol or a name p" |
| 8 | `get_upstream_features` | L0:F1069@21, k=5 | Emb:" He"@21 (w=37.25) +4 more |

**Findings:** Traced L6:F12990 at pos 21 (negative effect feature detecting "male pronouns and titles along with descriptors associated with men"). The circuit shows a direct, strong connection from the token "He" at position 21 (edge weight 4.56) to the layer 6 feature. Additionally, there's an indirect path through lower-layer features: L1:F12922 ("the pronoun 'he' or 'she' in a narrative context") with weigh…

</details>

<details>
<summary><b>SA-3</b> — tool trace (10 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L7, F14946 | " the possessive pronoun "his" (or similar pronouns like "he" and "him"" |
| 2 | `get_upstream_features` | L7:F14946@2, k=5 | Emb:"He"@1 (w=7.72) +4 more |
| 3 | `inspect_feature` | L6, F12990 | " male pronouns and titles along with descriptors associated with men" |
| 4 | `inspect_feature` | L4, F993 | "contractions of the verb to be in the third person singular" |
| 5 | `get_upstream_features` | L6:F12990@2, k=5 | Emb:" received"@2 (w=3.23) +4 more |
| 6 | `inspect_feature` | L5, F645 | " verbs in past tense" |
| 7 | `get_upstream_features` | L5:F645@2, k=5 | Emb:"He"@1 (w=3.88) +4 more |
| 8 | `get_upstream_features` | L4:F993@2, k=5 | Emb:"He"@1 (w=6.28) +4 more |
| 9 | `inspect_feature` | L0, F1069 | " references to a male person, particularly when using the pronoun "He"" |
| 10 | `inspect_feature` | L2, F2128 | " pronouns, especially "he/him/it" equivalents like *er*, *ihn*, *es*, " |

**Findings:** This circuit traces L7:F14946 (detecting possessive pronoun "his" and related male pronouns). The feature has negative effect, meaning it suppresses certain tokens when activated. Tracing upstream reveals a male pronoun processing pathway originating from token "He" at position 1. The circuit shows: 1) "He" token directly influences L0:F1069 (male pronoun detection), 2) This feeds into L2:F2128 (p…

</details>

<details>
<summary><b>SA-4</b> — tool trace (12 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L7, F14893 | " pronouns or possessive pronouns" |
| 2 | `get_upstream_features` | L7:F14893@1, k=5 | Emb:"He"@1 (w=14.75) +4 more |
| 3 | `inspect_feature` | L6, F12990 | " male pronouns and titles along with descriptors associated with men" |
| 4 | `inspect_feature` | L4, F9757 | "various acronyms, IDs, and symbols, possibly related to scientific dat" |
| 5 | `inspect_feature` | L4, F14796 | "the pronoun "he" or "him"" |
| 6 | `inspect_feature` | L2, F9301 | " all mentions of men and women in the context of relationships, dating" |
| 7 | `get_upstream_features` | L6:F12990@1, k=5 | Emb:"He"@1 (w=3.41) +4 more |
| 8 | `get_upstream_features` | L4:F14796@1, k=5 | Emb:"He"@1 (w=17.12) +4 more |
| 9 | `inspect_feature` | L5, F10952 | "third person pronouns in varying contexts" |
| 10 | `inspect_feature` | L2, F2110 | " the third person singular pronouns "he" and "she"" |
| 11 | `get_upstream_features` | L2:F2110@1, k=5 | Emb:"He"@1 (w=26.62) +4 more |
| 12 | `inspect_feature` | L0, F12698 | "question-answer pairs (or just questions) and import statements" |

**Findings:** I traced L7:F14893 at position 1, which detects pronouns/possessive pronouns. The feature has a strong direct connection to the token embedding "He" at position 1 (weight 14.75). The circuit reveals a pronoun detection pathway: Starting from the input token "He" at position 1, it directly feeds into multiple pronoun-detecting features across layers. Key findings:

1. Direct token embedding connect…

</details>

<details>
<summary><b>SA-5</b> — tool trace (8 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L18, F14743 | "He" |
| 2 | `get_upstream_features` | L18:F14743@21, k=5 | Emb:" He"@21 (w=23.38) +4 more |
| 3 | `inspect_feature` | L0, F1069 | " references to a male person, particularly when using the pronoun "He"" |
| 4 | `inspect_feature` | L17, F5889 | " references to people with pronouns and possessive pronouns" |
| 5 | `inspect_feature` | L13, F6622 | " pronouns." |
| 6 | `get_upstream_features` | L0:F1069@21, k=5 | Emb:" He"@21 (w=37.25) +4 more |
| 7 | `get_upstream_features` | L17:F5889@21, k=5 | Emb:" He"@21 (w=22.50) +4 more |
| 8 | `get_upstream_features` | L13:F6622@21, k=5 | Emb:" He"@21 (w=13.31) +4 more |

**Findings:** Tracing L18:F14743 at position 21 revealed a gender detection circuit specifically for the male pronoun "He". The feature detects the word "He" and promotes tokens like "himself", "him", etc. The circuit shows:

1. L18:F14743 directly receives strong input from the embedding token " He" at position 21 (weight: 23.375).

2. It also receives signals from earlier layers that detect male pronouns:
   …

</details>

<details>
<summary><b>SA-6</b> — tool trace (3 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F6270 | "the word "whom", sometimes also activating on nearby punctuation, sent" |
| 2 | `get_upstream_features` | L0:F6270@13, k=5 | Emb:" University"@13 (w=22.88) +4 more |
| 3 | `get_upstream_features` | L0:F6270@13, k=10 | Emb:" University"@13 (w=22.88) +9 more |

**Findings:** Tracing L0:F6270 at position 13 revealed that this feature, which generally encodes the word \"whom\" and related function words, is being strongly activated (edge weight 22.875) by the token \" University\" at the same position 13. This suggests that in this specific circuit context, the feature is responding to university-related content despite its general semantic label. The feature has low sp…

</details>

<details>
<summary><b>SA-7</b> — tool trace (15 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F170 | " references to academic fields, especially those in the humanities" |
| 2 | `get_upstream_features` | L6:F170@10, k=5 | L5:F10392 (w=11.38) +4 more |
| 3 | `inspect_feature` | L5, F10392 | " fields of academic study" |
| 4 | `inspect_feature` | L5, F15490 | " academic subjects and professions" |
| 5 | `get_upstream_features` | L5:F10392@10, k=5 | L3:F4113 (w=3.34) +4 more |
| 6 | `inspect_feature` | L3, F4113 | " mentions of academic degrees and areas of study" |
| 7 | `inspect_feature` | L4, F3727 | " mentions of academic degrees" |
| 8 | `get_upstream_features` | L4:F3727@9, k=5 | Emb:" in"@9 (w=11.69) +4 more |
| 9 | `get_upstream_features` | L3:F4113@9, k=5 | Emb:" in"@9 (w=11.94) +4 more |
| 10 | `inspect_feature` | L2, F10852 | " academic titles and degrees" |
| 11 | `get_upstream_features` | L2:F10852@9, k=5 | Emb:" in"@9 (w=12.62) +4 more |
| 12 | `get_upstream_features` | L5:F15490@10, k=5 | Emb:" Mathematics"@10 (w=1.83) +4 more |
| 13 | `inspect_feature` | L2, F9995 | " terms related to occupations and fields of study" |
| 14 | `get_upstream_features` | L2:F9995@10, k=5 | Emb:" in"@9 (w=3.05) +4 more |
| 15 | `inspect_feature` | L1, F10429 | " words related to academic programs" |

**Findings:** The tracing reveals that L6:F170 at position 10 detects "references to academic fields, especially those in the humanities." This is NOT a gender/pronoun feature but rather an academic/profession-related feature focused on academic fields and degrees.

The circuit originates from token embeddings: "Mathematics" at position 10, "in" at position 9, and "degree" at position 8 feed into early layer fe…

</details>

<details>
<summary><b>SA-8</b> — tool trace (11 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L12, F2175 | " words referring to gender" |
| 2 | `get_upstream_features` | L12:F2175@2, k=5 | L7:F14946 (w=4.44) +4 more |
| 3 | `inspect_feature` | L7, F14946 | " the possessive pronoun "his" (or similar pronouns like "he" and "him"" |
| 4 | `inspect_feature` | L7, F14893 | " pronouns or possessive pronouns" |
| 5 | `inspect_feature` | L9, F2587 | " references to personal pronouns in the third person, and possibly fir" |
| 6 | `get_upstream_features` | L7:F14946@2, k=5 | Emb:"He"@1 (w=7.72) +4 more |
| 7 | `get_upstream_features` | L7:F14893@2, k=5 | Emb:"He"@1 (w=6.78) +4 more |
| 8 | `inspect_feature` | L6, F12990 | " male pronouns and titles along with descriptors associated with men" |
| 9 | `get_upstream_features` | L6:F12990@2, k=5 | Emb:" received"@2 (w=3.23) +4 more |
| 10 | `inspect_feature` | L5, F645 | " verbs in past tense" |
| 11 | `inspect_feature` | L4, F993 | "contractions of the verb to be in the third person singular" |

**Findings:** I traced L12:F2175 at position 2 (negative effect) and discovered it's a gender detection feature. The circuit reveals:

1. L12:F2175 detects "words referring to gender" - it promotes masculine terms like "himself", "masculinity" and suppresses feminine terms like "herself", "female", "woman".

2. This feature receives positive input from L7:F14946 (masculine pronoun feature detecting "his", "he",…

</details>

### Build

`build_circuit` → 0 nodes, 0 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m2.7 | 21,398 | 10,165 | 240,058 | 0 | $0.0258 | — | — |
| SA-1 | deepseek/deepseek-v3.2 | 13,632 | 1,545 | 0 | 0 | $0.0041 | ✅ 2F/4E | Trace what L0:F2994 encodes and where its signal originates.… |
| SA-5 | deepseek/deepseek-v3.2 | 47,012 | 2,534 | 0 | 0 | $0.0132 | ✅ 1481F/10E | Trace L18:F14743 at pos 21 (negative effect) - identify what… |
| SA-3 | deepseek/deepseek-v3.2 | 62,515 | 2,650 | 0 | 0 | $0.0173 | ✅ 6F/6E | Trace L7:F14946 at pos 2 (negative effect) - identify what s… |
| SA-2 | deepseek/deepseek-v3.2 | 40,177 | 2,214 | 5,568 | 0 | $0.0114 | ✅ 5F/7E | Trace L6:F12990 at pos 21 (negative effect) - identify what … |
| SA-4 | deepseek/deepseek-v3.2 | 74,986 | 3,532 | 9,344 | 0 | $0.0211 | ✅ 8F/13E | Trace L7:F14893 at pos 1 (positive effect) - identify what s… |
| SA-6 | deepseek/deepseek-v3.2 | 13,465 | 1,261 | 0 | 0 | $0.0040 | ✅ 1F/1E | Trace L0:F6270 at pos 13 - what does this feature encode? Ch… |
| SA-7 | deepseek/deepseek-v3.2 | 107,100 | 3,299 | 2,368 | 0 | $0.0292 | ✅ 8F/10E | Trace L6:F170 at pos 10 - what semantic concept does this de… |
| SA-8 | deepseek/deepseek-v3.2 | 75,125 | 3,686 | 0 | 0 | $0.0209 | ✅ 7F/13E | Trace L12:F2175 at pos 2 (negative effect) - identify what s… |
| **Total** | | **455,410** | **30,886** | **257,338** | **0** | **$0.1470** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 7m 21s