# Circuit Oracle Report
**Date:** 2026-04-06 11:15:41 UTC | **Orchestrator:** minimax/minimax-m2.7 | **Subagent:** deepseek/deepseek-v3.2

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-neg_neg_5 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "('The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession.',)"

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification is primarily driven by gender marker features (male pronouns "He"/"his" at positions 1, 3, and 25 with cumulative edge weights exceeding 62) rather than genuine profession indicators. The single strongest contributor is `L0:F2994` (direct_effect=0.233), which detects the possessive pronoun "his" and is driven by the token "his" at position 3 with an embedding weight of 42.25. The "reporter" profession features (`L14:F4420` and `L19:F2486`) exist and are strongly driven by the "reporter" token at position 66, but they have **negative** direct effects on the probe (inhibitory, not excitatory). A notable gender-processing anomaly is `L7:F14893`, which paradoxically promotes feminine pronouns ("herself", "she", "elle") yet is triggered by the male pronoun "He" at position 1 — this gender contrast/agreement circuit contributes positively to the probe. The circuit confirms the user's concern: gender markers are the primary drivers while profession-specific features suppress the probe's score.

**Confidence:** 9/10

**Reasoning:** The circuit analysis reveals that the probe classification relies heavily on gender-related features (male pronouns at multiple positions with cumulative embedding weights >62) rather than genuine profession indicators. The strongest direct effect (0.233) comes from `L0:F2994` detecting the possessive pronoun "his," while the journalism/reporter features (`L14:F4420`: journalism/newspapers, `L19:F2486`: journalistic sources) are present and strongly token-driven by "reporter" at position 66, but contribute negatively to the probe. This pattern indicates the probe may be trained to recognize a profession that correlates with male gender markers in its training data, and the model has learned to use gender pronouns as a shortcut rather than relying on explicit profession-related features. The presence of the gender contrast feature (`L7:F14893`) that activates feminine pronouns in response to masculine "He" input further confirms gender-mediated processing dominates the circuit.

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 10 features; top: L0:2994 de=0.233 |

### Dispatch: 8 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L0:F2994@3` | ✅ reported | 2 | 5 | Trace this feature to understand what input signal it captures. Check if it rela… |
| SA-2 | `L14:F4420@66` | ✅ reported | 10 | 13 | Trace this feature to understand what semantic concept it encodes. This is a str… |
| SA-3 | `L7:F14893@1` | ✅ reported | 7 | 13 | Trace this early-layer feature at position 1 to understand what input token driv… |
| SA-4 | `L19:F2486@66` | ✅ reported | 11 | 18 | Trace this negative contributor to understand what semantic concept it captures.… |
| SA-5 | `L7:F14946@1` | ✅ reported | 2910 | 23 | Trace this feature at position 1 (after bos token). Investigate what it encodes … |
| SA-6 | `L0:F8974@9` | ✅ reported | 1 | 5 | Trace this layer 0 feature at position 9. This is a strong negative contributor.… |
| SA-7 | `L0:F6051@24` | ✅ reported | 1 | 1 | Trace this layer 0 feature at position 24. Investigate what semantic concept it … |
| SA-8 | `L18:F14743@25` | ✅ reported | 5 | 20 | Trace this feature at position 25. Investigate what semantic concept it encodes … |

<details>
<summary><b>SA-1</b> — tool trace (4 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F2994 | "the pronoun "his" and the pronoun "he."" |
| 2 | `get_upstream_features` | L0:F2994@3, k=5 | Emb:" his"@3 (w=42.25) +4 more |
| 3 | `inspect_feature` | L0, F310 | " the pronouns "she", "her", and "he" and sometimes the word "therefore" |
| 4 | `get_upstream_features` | L0:F2994@3, k=10 | Emb:" his"@3 (w=42.25) +9 more |

**Findings:** Traced feature L0:F2994 at position 3, which detects the pronoun \"his\" and \"he\". The circuit is very direct: the feature is primarily triggered by the token \"his\" itself at position 3 (edge weight 42.25), with minor influences from preceding tokens \"obtained\" (pos 2, weight 1.27) and \"He\" (pos 1, weight 1.07). The feature promotes generic continuation tokens (spaces, periods, newlines) w…

</details>

<details>
<summary><b>SA-2</b> — tool trace (16 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L14, F4420 | "words and phrases related to journalism and newspapers" |
| 2 | `get_upstream_features` | L14:F4420@66, k=5 | Emb:" reporter"@66 (w=18.62) +4 more |
| 3 | `inspect_feature` | L4, F13253 | " things related to journalism and the media" |
| 4 | `inspect_feature` | L8, F8855 | " mentions of news reporters and news reporting" |
| 5 | `inspect_feature` | L7, F13646 | " news reporting and journalism." |
| 6 | `get_upstream_features` | L4:F13253@66, k=5 | Emb:" reporter"@66 (w=26.62) +4 more |
| 7 | `get_upstream_features` | L8:F8855@66, k=5 | Emb:" reporter"@66 (w=16.88) +4 more |
| 8 | `inspect_feature` | L1, F1024 | " words and phrases frequently used when discussing writing, publishing" |
| 9 | `inspect_feature` | L1, F5357 | " words related to written works" |
| 10 | `inspect_feature` | L2, F9719 | " terms related to broadcast news" |
| 11 | `inspect_feature` | L3, F7446 | " words related to processes of conveying information through different" |
| 12 | `inspect_feature` | L7, F9521 | " news sources and people involved in journalism" |
| 13 | `get_upstream_features` | L7:F13646@66, k=5 | Emb:" reporter"@66 (w=15.12) +4 more |
| 14 | `inspect_feature` | L4, F661 | " words and phrases used when referring to reports, documentaries, and " |
| 15 | `get_upstream_features` | L1:F1024@66, k=5 | Emb:" reporter"@66 (w=8.06) +4 more |
| 16 | `get_upstream_features` | L1:F5357@66, k=5 | Emb:" reporter"@66 (w=12.00) +4 more |

**Findings:** The feature L14:F4420 is a negative contributor to the probe that encodes "words and phrases related to journalism and newspapers." Tracing reveals it's strongly driven by the token " reporter" at position 66, with direct token embedding connections having very high weights (18.625 to L14:F4420, 26.625 to L4:F13253, 16.875 to L8:F8855, 15.125 to L7:F13646).

The circuit shows a hierarchical proces…

</details>

<details>
<summary><b>SA-3</b> — tool trace (11 calls)</summary>

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
| 9 | `inspect_feature` | L2, F2110 | " the third person singular pronouns "he" and "she"" |
| 10 | `get_upstream_features` | L2:F9301@1, k=5 | Emb:"He"@1 (w=14.94) +4 more |
| 11 | `inspect_feature` | L0, F12698 | "question-answer pairs (or just questions) and import statements" |

**Findings:** Tracing L7:F14893 at position 1 revealed a fascinating circuit: this feature promotes feminine pronouns ("herself", "she", "elle") while suppressing masculine pronouns. Surprisingly, it is most strongly driven (edge weight 14.75) by the input token "He" at position 1. This creates a paradoxical circuit where a masculine pronoun token activates a feminine pronoun feature.

The circuit includes:
1. …

</details>

<details>
<summary><b>SA-4</b> — tool trace (15 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L19, F2486 | " journalistic sources and news outlets." |
| 2 | `get_upstream_features` | L19:F2486@66, k=5 | Emb:" reporter"@66 (w=28.12) +4 more |
| 3 | `inspect_feature` | L14, F4420 | "words and phrases related to journalism and newspapers" |
| 4 | `inspect_feature` | L4, F13253 | " things related to journalism and the media" |
| 5 | `inspect_feature` | L8, F8855 | " mentions of news reporters and news reporting" |
| 6 | `get_upstream_features` | L14:F4420@66, k=5 | Emb:" reporter"@66 (w=18.62) +4 more |
| 7 | `inspect_feature` | L7, F13646 | " news reporting and journalism." |
| 8 | `inspect_feature` | L7, F9092 | " words and phrases associated with broadcast journalism" |
| 9 | `get_upstream_features` | L4:F13253@66, k=5 | Emb:" reporter"@66 (w=26.62) +4 more |
| 10 | `inspect_feature` | L1, F1024 | " words and phrases frequently used when discussing writing, publishing" |
| 11 | `inspect_feature` | L1, F5357 | " words related to written works" |
| 12 | `inspect_feature` | L3, F7446 | " words related to processes of conveying information through different" |
| 13 | `get_upstream_features` | L8:F8855@66, k=5 | Emb:" reporter"@66 (w=16.88) +4 more |
| 14 | `inspect_feature` | L7, F9521 | " news sources and people involved in journalism" |
| 15 | `inspect_feature` | L2, F9719 | " terms related to broadcast news" |

**Findings:** I traced the negative contributor L19:F2486 at position 66. This feature captures "journalistic sources and news outlets" and promotes tokens like "reporting", "reporter", and "coverage". 

The circuit shows a direct path from the token " reporter" at position 66 feeding strongly into this feature with weight 28.125. This same token embedding feeds into multiple intermediate features related to jo…

</details>

<details>
<summary><b>SA-5</b> — tool trace (14 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L7, F14946 | " the possessive pronoun "his" (or similar pronouns like "he" and "him"" |
| 2 | `get_upstream_features` | L7:F14946@1, k=5 | Emb:"He"@1 (w=11.50) +4 more |
| 3 | `inspect_feature` | L4, F14796 | "the pronoun "he" or "him"" |
| 4 | `inspect_feature` | L6, F12990 | " male pronouns and titles along with descriptors associated with men" |
| 5 | `inspect_feature` | L5, F10952 | "third person pronouns in varying contexts" |
| 6 | `get_upstream_features` | L4:F14796@1, k=5 | Emb:"He"@1 (w=17.12) +4 more |
| 7 | `inspect_feature` | L2, F2110 | " the third person singular pronouns "he" and "she"" |
| 8 | `get_upstream_features` | L6:F12990@1, k=5 | Emb:"He"@1 (w=3.41) +4 more |
| 9 | `get_upstream_features` | L5:F10952@1, k=5 | Emb:"He"@1 (w=10.25) +4 more |
| 10 | `inspect_feature` | L2, F2128 | " pronouns, especially "he/him/it" equivalents like *er*, *ihn*, *es*, " |
| 11 | `get_upstream_features` | L0:F12698@1, k=5 | Emb:"<bos>"@0 (w=15.56) +4 more |
| 12 | `inspect_feature` | L0, F12698 | "question-answer pairs (or just questions) and import statements" |
| 13 | `get_upstream_features` | L1:F8685@1, k=5 | Emb:"He"@1 (w=14.19) +4 more |
| 14 | `inspect_feature` | L1, F8685 | " the pronoun "he"" |

**Findings:** I traced the gender-related feature at L7:F14946 at position 1. This feature encodes masculine pronouns like \"his\", \"he\", and \"him\", with promoted tokens including reflexive pronouns like \"himself\" and suppressed tokens like \"herself\", \"she\", and \"her\". The circuit analysis shows it's directly driven by the input token \"He\" at position 1 (edge_weight 11.5) and also influenced by th…

</details>

<details>
<summary><b>SA-6</b> — tool trace (3 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F8974 | "the word "from"" |
| 2 | `get_upstream_features` | L0:F8974@9, k=5 | Emb:" from"@9 (w=40.00) +4 more |
| 3 | `get_top_logits` | k=5 | "" (100%) |

**Findings:** The feature L0:F8974 at position 9 is a simple detector for the word "from". It's directly driven by the token embedding " from" at position 9 with a very strong weight of 40.0. Other token embeddings that contribute (with much smaller weights) include beginning-of-sequence token, "obtained", "field", and "undergraduate" (with negative weight). The feature has low sparsity (0.02366), indicating it…

</details>

<details>
<summary><b>SA-7</b> — tool trace (3 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F6051 | "periods, spaces, and the number 1" |
| 2 | `get_upstream_features` | L0:F6051@24, k=5 | Emb:"."@24 (w=47.25) +4 more |
| 3 | `get_upstream_features` | L0:F6051@24, k=10 | Emb:"."@24 (w=47.25) +9 more |

**Findings:** The feature L0:F6051 at position 24 encodes detection of period characters ('.'). The label 'periods, spaces, and the number 1' accurately describes its function, with the strongest activation on period tokens. The feature is primarily driven by the input token '.' at position 24 with an extremely strong edge weight of 47.25, while other tokens provide minor inhibitory connections. The feature has…

</details>

<details>
<summary><b>SA-8</b> — tool trace (9 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L18, F14743 | "He" |
| 2 | `get_upstream_features` | L18:F14743@25, k=5 | Emb:" He"@25 (w=24.00) +4 more |
| 3 | `inspect_feature` | L0, F1069 | " references to a male person, particularly when using the pronoun "He"" |
| 4 | `inspect_feature` | L17, F5889 | " references to people with pronouns and possessive pronouns" |
| 5 | `get_upstream_features` | L0:F1069@25, k=5 | Emb:" He"@25 (w=36.75) +4 more |
| 6 | `get_upstream_features` | L17:F5889@25, k=5 | Emb:" He"@25 (w=22.38) +4 more |
| 7 | `inspect_feature` | L13, F6622 | " pronouns." |
| 8 | `get_upstream_features` | L13:F6622@25, k=5 | Emb:" He"@25 (w=13.94) +4 more |
| 9 | `inspect_feature` | L15, F3330 | " personal stories of individuals, especially women and their actions o" |

**Findings:** Tracing from L18:F14743 (position 25), which encodes the word "He" - a pronoun detection feature that's a negative contributor to the probe. The circuit shows:

1. The feature is primarily driven by the input token " He" at position 25 through a strong direct embedding connection (edge weight 24.0).

2. The feature also receives inputs from several intermediate pronoun-detection features:
   - L0:…

</details>

### Build

`build_circuit` → 15 nodes, 17 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m2.7 | 24,928 | 4,684 | 56,418 | 0 | $0.0148 | — | — |
| SA-1 | deepseek/deepseek-v3.2 | 18,786 | 1,752 | 0 | 0 | $0.0056 | ✅ 2F/5E | Trace this feature to understand what input signal it captur… |
| SA-3 | deepseek/deepseek-v3.2 | 76,833 | 3,839 | 0 | 0 | $0.0214 | ✅ 7F/13E | Trace this early-layer feature at position 1 to understand w… |
| SA-2 | deepseek/deepseek-v3.2 | 121,200 | 4,061 | 10,816 | 0 | $0.0333 | ✅ 10F/13E | Trace this feature to understand what semantic concept it en… |
| SA-4 | deepseek/deepseek-v3.2 | 120,353 | 4,127 | 0 | 0 | $0.0329 | ✅ 11F/18E | Trace this negative contributor to understand what semantic … |
| SA-7 | deepseek/deepseek-v3.2 | 13,552 | 1,116 | 0 | 0 | $0.0039 | ✅ 1F/1E | Trace this layer 0 feature at position 24. Investigate what … |
| SA-6 | deepseek/deepseek-v3.2 | 12,516 | 1,598 | 0 | 0 | $0.0039 | ✅ 1F/5E | Trace this layer 0 feature at position 9. This is a strong n… |
| SA-5 | deepseek/deepseek-v3.2 | 79,219 | 4,360 | 26,112 | 0 | $0.0229 | ✅ 2910F/23E | Trace this feature at position 1 (after bos token). Investig… |
| SA-8 | deepseek/deepseek-v3.2 | 46,863 | 3,613 | 7,296 | 0 | $0.0137 | ✅ 5F/20E | Trace this feature at position 25. Investigate what semantic… |
| **Total** | | **514,250** | **29,150** | **100,642** | **0** | **$0.1525** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 9m 41s