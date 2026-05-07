# Circuit Oracle Report
**Date:** 2026-03-30 20:03:10 UTC | **Orchestrator:** minimax/minimax-m2.7 | **Subagent:** deepseek/deepseek-v3.2

## Input
**Prompt:** "Dataset: bib_journalist_dietitian-neg_neg_2 | Probe: unbiased | Method: correct"
**System prompt:** ""
**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."
**Top predictions:**  (100.0%)

## Oracle Analysis
**Analysis:** This probe's classification score is driven by two competing signals: (1) **early positional features** detecting generic tokens like "His", "to", "see" (with positive direct effects of +0.063 to +0.079), and (2) **journalism-specific features** (L14-L20) detecting profession indicators like "report", "journalist", "news organizations" (with negative direct effects of -0.062 to -0.146). The circuit uses the masculine pronoun "His" as a shortcut feature rather than encoding gender markers directly.

**Confidence:** 8/10

**Reasoning:** The circuit analysis reveals a nuanced picture regarding the user's concern about spurious gender features:

1. **Genuine Profession Indicators (verified):** The journalism circuit is well-established with proper semantic specificity:
   - **L14:F4420** ("journalism and newspapers", frac_nonzero=0.0165) → promotes "journalist", "reporter", "editorial"
   - **L19:F2486** ("journalistic sources and news outlets", frac_nonzero=0.029) → promotes "reporting", "coverage", "reporters"
   - **L20:F8433** ("news broadcasting", frac_nonzero=0.036) → promotes "news", "journalists", "newspapers"
   
   These features form a coherent pathway from the word "report" (embedding at pos 21) through early detection (L1-L4), mid-level journalism features (L7-L8), specialized journalism concepts (L14-L16), and final news features (L19-L20). All have low frac_nonzero (0.002-0.036), indicating genuine specificity.

2. **Spurious Pronoun Feature (partial validation of concern):**
   - **L0:F8964** directly detects "His" with strong edge weight (13.6875) and positive direct effect (+0.079) on the probe
   - However, this is NOT a "gender marker" in the semantic sense—it's a raw token detector that fires on the masculine pronoun "His"
   - Critically, L0:F8964 does NOT receive input from gender-specific features (L0:F310 which detects "she/her/he" has zero weight connection to L0:F8964)
   - The other positive-effect features (L0:F8444="to", L0:F14287="see") are generic tokens with no semantic relationship to journalism

3. **Circuit Mechanics:** The negative journalism features (-0.145 to -0.062) are stronger in magnitude than the positive pronoun feature (+0.079), suggesting the probe primarily relies on genuine profession indicators. However, the inclusion of "His" as a feature suggests the probe learned a correlation between masculine pronouns and journalism in training data—the "His" feature itself is not encoding gender semantics but rather acts as a spurious shortcut that co-occurs with journalists in the training corpus.

The user's concern is **partially validated**: while no gender-semantic features exist in the circuit, the "His" pronoun functions as a spurious correlate rather than a genuine profession indicator.

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 10 features; top: L14:4420 de=-0.145 |

### Dispatch: 3 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L19:F2486@21` | ✅ reported | 10 | 19 | Trace what L19:F2486 encodes and where it gets its signal from. Look for whether… |
| SA-2 | `L14:F4420@21` | ✅ reported | 13 | 16 | Trace what L14:F4420 encodes and where its signal originates. Look for gender ma… |
| SA-3 | `L0:F8964@1` | ✅ reported | 4 | 3 | Trace what L0:F8964 encodes at position 1. This is an early layer feature with p… |

<details>
<summary><b>SA-1</b> — tool trace (14 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L19, F2486 | " journalistic sources and news outlets." |
| 2 | `get_upstream_features` | L19:F2486@21, k=5 | L14:F4420 (w=14.31) +4 more |
| 3 | `inspect_feature` | L14, F4420 | "words and phrases related to journalism and newspapers" |
| 4 | `inspect_feature` | L16, F8642 | " text related to official reporting and legal issues." |
| 5 | `inspect_feature` | L8, F8855 | " mentions of news reporters and news reporting" |
| 6 | `get_upstream_features` | L14:F4420@21, k=5 | Emb:" report"@21 (w=5.22) +4 more |
| 7 | `inspect_feature` | L7, F13646 | " news reporting and journalism." |
| 8 | `inspect_feature` | L8, F8437 | "content related to film festivals and production, particularly documen" |
| 9 | `get_upstream_features` | L8:F8855@21, k=5 | Emb:" report"@21 (w=12.12) +4 more |
| 10 | `inspect_feature` | L7, F13896 | " words or phrases related to reports, people's names, and versions" |
| 11 | `inspect_feature` | L3, F10846 | "the word "report"" |
| 12 | `inspect_feature` | L2, F11175 | "the verb "report" and its variations" |
| 13 | `get_upstream_features` | L16:F8642@21, k=5 | L14:F4420 (w=10.50) +4 more |
| 14 | `inspect_feature` | L16, F15046 | " names, organizations, and reporting verbs" |

**Findings:** L19:F2486 encodes "journalistic sources and news outlets." It is a specialized journalism feature with low frac_nonzero (0.029), indicating it's selective rather than generic. The feature gets its strongest positive signal from L14:F4420 (journalism/newspapers feature, weight=14.31) which itself receives input from L8:F8855 (news reporters feature) and the embedding "report". 

Interestingly, ther…

</details>

<details>
<summary><b>SA-2</b> — tool trace (20 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L14, F4420 | "words and phrases related to journalism and newspapers" |
| 2 | `get_upstream_features` | L14:F4420@21, k=5 | Emb:" report"@21 (w=5.22) +4 more |
| 3 | `inspect_feature` | L8, F8855 | " mentions of news reporters and news reporting" |
| 4 | `inspect_feature` | L7, F13646 | " news reporting and journalism." |
| 5 | `inspect_feature` | L8, F8437 | "content related to film festivals and production, particularly documen" |
| 6 | `get_upstream_features` | L8:F8855@21, k=5 | Emb:" report"@21 (w=12.12) +4 more |
| 7 | `get_upstream_features` | L7:F13646@21, k=5 | Emb:" report"@21 (w=7.25) +4 more |
| 8 | `inspect_feature` | L4, F661 | " words and phrases used when referring to reports, documentaries, and " |
| 9 | `inspect_feature` | L6, F12712 | " titles of editors and publishers in scientific publications" |
| 10 | `get_upstream_features` | L4:F661@21, k=5 | Emb:" report"@21 (w=14.38) +4 more |
| 11 | `inspect_feature` | L1, F14511 | " the word "report"" |
| 12 | `inspect_feature` | L2, F11175 | "the verb "report" and its variations" |
| 13 | `inspect_feature` | L3, F10846 | "the word "report"" |
| 14 | `get_upstream_features` | L1:F14511@21, k=5 | Emb:" report"@21 (w=20.62) +4 more |
| 15 | `inspect_feature` | L0, F1014 | " instances of measurement, experimentation, and quantification" |
| 16 | `inspect_feature` | L0, F12801 | " verbs related to communication, help, enabling, and allowing" |
| 17 | `get_upstream_features` | L8:F8437@21, k=5 | Emb:" report"@21 (w=5.81) +4 more |
| 18 | `inspect_feature` | L9, F7435 | " words and phrases related to news production and media" |
| 19 | `get_upstream_features` | L9:F7435@21, k=5 | Emb:"<bos>"@0 (w=2.72) +4 more |
| 20 | `inspect_feature` | L8, F15435 | " words relating to news broadcasting" |

**Findings:** The circuit trace shows that L14:F4420 encodes journalism/newspaper concepts and primarily originates from the token "report" at position 21. Key findings:

1. **Direct Source**: The strongest signal comes directly from the embedding of token "report" (weight 5.2188).

2. **Intermediate Features**: 
   - L8:F8855: "mentions of news reporters and news reporting" (weight 5.0625, frac_nonzero=0.00847…

</details>

<details>
<summary><b>SA-3</b> — tool trace (5 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F8964 | " the possessive pronoun "His"" |
| 2 | `get_upstream_features` | L0:F8964@1, k=5 | Emb:"His"@1 (w=13.69) +4 more |
| 3 | `inspect_feature` | L0, F253 | "the contraction "ve" and also finds other words like "scale", "screen"" |
| 4 | `inspect_feature` | L0, F310 | " the pronouns "she", "her", and "he" and sometimes the word "therefore" |
| 5 | `inspect_feature` | L0, F208 | "the words "happened" and "occur"" |

**Findings:** L0:F8964 at position 1 encodes the possessive pronoun "His" as a direct pattern detector. The circuit tracing reveals this feature is primarily fed by the token embedding for "His" at position 1 with a very strong edge weight (13.6875), indicating it's essentially a direct detector of this specific input token. There's also a weaker connection from the <bos> token embedding at position 0 (weight=1…

</details>

### Re-dispatch (round 2): 1 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-4 | `L0:F8444@3` | ✅ reported | 2 | 5 | Trace what L0:F8444 encodes at position 3. This is an early layer feature with p… |

<details>
<summary><b>SA-4</b> — tool trace (3 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F8444 | "the word "to"" |
| 2 | `get_upstream_features` | L0:F8444@3, k=5 | Emb:" to"@3 (w=39.50) +4 more |
| 3 | `inspect_feature` | L0, F253 | "the contraction "ve" and also finds other words like "scale", "screen"" |

**Findings:** Tracing from L0:F8444 at position 3 reveals it primarily encodes detection of the token "to". The feature has low frac_nonzero (0.01705), indicating specificity. Its strongest connection is directly from the embedding of " to" at position 3 (weight 39.5). There is a very weak connection from "His" at position 1 (weight 0.0942), which could represent minimal gender correlation, but this signal is e…

</details>

### Re-dispatch (round 3): 1 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-5 | `L20:F8433@26` | ✅ reported | 7 | 9 | Trace what L20:F8433 encodes at position 26 and what its upstream sources are. C… |

<details>
<summary><b>SA-5</b> — tool trace (13 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L20, F8433 | "words related to news broadcasting" |
| 2 | `get_upstream_features` | L20:F8433@26, k=5 | Emb:" top"@26 (w=5.69) +4 more |
| 3 | `inspect_feature` | L17, F5218 | " text about journalism, media, and related topics" |
| 4 | `inspect_feature` | L14, F4420 | "words and phrases related to journalism and newspapers" |
| 5 | `inspect_feature` | L19, F2486 | " journalistic sources and news outlets." |
| 6 | `get_upstream_features` | L14:F4420@21, k=5 | Emb:" report"@21 (w=5.22) +4 more |
| 7 | `inspect_feature` | L8, F8855 | " mentions of news reporters and news reporting" |
| 8 | `get_upstream_features` | L17:F5218@26, k=5 | Emb:" report"@21 (w=2.09) +4 more |
| 9 | `get_upstream_features` | L19:F2486@26, k=5 | L14:F4420 (w=6.25) +4 more |
| 10 | `get_upstream_features` | L8:F8855@21, k=5 | Emb:" report"@21 (w=12.12) +4 more |
| 11 | `inspect_feature` | L7, F13646 | " news reporting and journalism." |
| 12 | `get_upstream_features` | L7:F13646@21, k=5 | Emb:" report"@21 (w=7.25) +4 more |
| 13 | `inspect_feature` | L4, F661 | " words and phrases used when referring to reports, documentaries, and " |

**Findings:** The circuit analysis reveals that L20:F8433 encodes genuine profession indicators for journalism/news broadcasting rather than spurious gender correlations. The feature shows strong connections to journalism-specific concepts with low frac_nonzero values (0.00847 to 0.03572), indicating specificity. Key findings:

1. L20:F8433 receives positive input from L14:F4420 (journalism/newspapers) and L19:…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` | L0, F310 → " the pronouns "she", "her", and "he" and sometimes the word "therefore" |
| 2 | `get_upstream_features` | L0:F8964@1, k=10 → Emb:"His"@1 (w=13.69) +9 more |
| 3 | `inspect_feature` | L0, F14287 → "the word "see"" |

### Build

`build_circuit` → 10 nodes, 9 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m2.7 | 18,934 | 4,040 | 49,262 | 0 | — | — | — |
| SA-3 | deepseek/deepseek-v3.2 | 24,899 | 1,565 | 0 | 0 | — | ✅ 4F/3E | Trace what L0:F8964 encodes at position 1. This is an early … |
| SA-1 | deepseek/deepseek-v3.2 | 92,541 | 4,201 | 15,232 | 0 | — | ✅ 10F/19E | Trace what L19:F2486 encodes and where it gets its signal fr… |
| SA-2 | deepseek/deepseek-v3.2 | 160,936 | 5,210 | 24,000 | 0 | — | ✅ 13F/16E | Trace what L14:F4420 encodes and where its signal originates… |
| SA-4 | deepseek/deepseek-v3.2 | 13,934 | 2,134 | 0 | 0 | — | ✅ 2F/5E | Trace what L0:F8444 encodes at position 3. This is an early … |
| SA-5 | deepseek/deepseek-v3.2 | 93,305 | 3,844 | 0 | 0 | — | ✅ 7F/9E | Trace what L20:F8433 encodes at position 26 and what its ups… |
| **Total** | | **404,549** | **20,994** | **88,494** | **0** | **—** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 8m 50s