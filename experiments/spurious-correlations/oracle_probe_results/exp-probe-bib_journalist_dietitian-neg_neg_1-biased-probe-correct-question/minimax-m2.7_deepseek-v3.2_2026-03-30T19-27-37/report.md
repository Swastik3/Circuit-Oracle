# Circuit Oracle Report
**Date:** 2026-03-30 19:27:37 UTC | **Orchestrator:** minimax/minimax-m2.7 | **Subagent:** deepseek/deepseek-v3.2

## Input
**Prompt:** "Dataset: bib_journalist_dietitian-neg_neg_1 | Probe: biased | Method: correct"
**System prompt:** ""
**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."
**Top predictions:**  (100.0%)

## Oracle Analysis
**Analysis:** The linear probe's classification is almost entirely driven by gender pronoun markers (he/his/him vs she/her/herself) rather than genuine profession indicators. The top 6 features by direct effect are all gender pronoun detectors—L7:F14893 (female pronoun, positive effect 0.47), L7:F14946 (male pronoun "his", negative effect -0.47), L6:F12990 (male pronouns, -0.30), L19:F8814 (pronouns/names, +0.23), L18:F14743 ("He", -0.19), L18:F10315 (pronouns, -0.16)—while the profession-related journalism feature L14:F4420 has only a negative effect (-0.16), meaning it suppresses rather than drives the prediction.

**Confidence:** 9/10

**Reasoning:** The circuit traces reveal a clear hierarchical pathway where the protagonist's pronoun "His" at position 1 directly excites early-layer male pronoun detectors (L0:F2994, L0:F1069, L1:F7439, L2:F5499 with frac_nonzero values of 0.073, 0.008, 0.003, and 0.008 respectively), which cascade through mid-layer integration (L4:F4315, L5:F10952, L6:F12990) into competing L7 gender pronoun detectors. The female pronoun detector L7:F14893 promotes "herself," "elle," "she" while suppressing male pronouns; the male pronoun detector L7:F14946 does the opposite. These converge at late-layer features L18-L19 that integrate gender information and feed the final probe.

The journalism path from the input token "report" at position 21 does exist (L1:F14511→L4:F661→L7:F13646→L8:F8855→L14:F4420), but it carries minimal weight and actually negatively impacts the probe score. The frac_nonzero values for early pronoun features are extremely low (0.003-0.073), confirming these are highly specific gender markers rather than generic pattern matchers. The gender pronoun features dominate the top positions with combined absolute direct effects exceeding 1.5, while the profession feature contributes only -0.16. This conclusively validates the user's concern: the probe relies on spurious gender correlation rather than authentic profession indicators.

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L7:14893 de=0.473 |
| 3 | `inspect_feature` ×8 | L7:14893, L7:14946, L19:8814, L0:2994, L6:12990, L18:14743, L18:10315, L4:4315 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L7:F14893@1` | ✅ reported | 7 | 23 | Trace the path from this female pronoun detector feature upstream. What features… |
| SA-2 | `L7:F14946@1` | ✅ reported | 8 | 27 | Trace the path from this male pronoun detector feature upstream. What features o… |
| SA-3 | `L19:F8814@1` | ✅ reported | 10 | 19 | Trace the path from this pronoun/name feature upstream. What feeds into it? |
| SA-4 | `L18:F14743@9` | ✅ reported | 9 | 9 | Trace the path from this 'He' pronoun detector at position 9. What feeds into it… |

<details>
<summary><b>SA-1</b> — tool trace (13 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L7, F14893 | " pronouns or possessive pronouns" |
| 2 | `get_upstream_features` | L7:F14893@1, k=5 | Emb:"His"@1 (w=23.50) +4 more |
| 3 | `inspect_feature` | L6, F12990 | " male pronouns and titles along with descriptors associated with men" |
| 4 | `inspect_feature` | L0, F2994 | "the pronoun "his" and the pronoun "he."" |
| 5 | `inspect_feature` | L4, F4315 | " mentions of "his" and other associated pronouns like he, him, or hers" |
| 6 | `get_upstream_features` | L6:F12990@1, k=5 | Emb:"His"@1 (w=4.91) +4 more |
| 7 | `get_upstream_features` | L0:F2994@1, k=5 | Emb:"His"@1 (w=19.75) +4 more |
| 8 | `get_upstream_features` | L4:F4315@1, k=5 | Emb:"His"@1 (w=23.50) +4 more |
| 9 | `inspect_feature` | L1, F7439 | " the possessive pronouns "his" and "him"" |
| 10 | `get_upstream_features` | L1:F7439@1, k=5 | Emb:"His"@1 (w=16.38) +4 more |
| 11 | `inspect_feature` | L2, F5491 | "references to God in the third person." |
| 12 | `get_upstream_features` | L2:F5491@1, k=5 | Emb:"His"@1 (w=23.88) +4 more |
| 13 | `inspect_feature` | L0, F1069 | " references to a male person, particularly when using the pronoun "He"" |

**Findings:** I traced the circuit for a female pronoun detector feature (L7:F14893) at position 1. The key finding is that this feature is primarily activated by the input token "His" itself (strongest connection: weight 23.5 directly from embedding). However, the circuit shows interesting competitive dynamics:

1. The direct embedding connection from "His" strongly excites the female pronoun detector (weight …

</details>

<details>
<summary><b>SA-2</b> — tool trace (14 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L7, F14946 | " the possessive pronoun "his" (or similar pronouns like "he" and "him"" |
| 2 | `get_upstream_features` | L7:F14946@1, k=5 | Emb:"His"@1 (w=18.38) +4 more |
| 3 | `inspect_feature` | L4, F4315 | " mentions of "his" and other associated pronouns like he, him, or hers" |
| 4 | `inspect_feature` | L0, F2994 | "the pronoun "his" and the pronoun "he."" |
| 5 | `inspect_feature` | L6, F12990 | " male pronouns and titles along with descriptors associated with men" |
| 6 | `get_upstream_features` | L4:F4315@1, k=5 | Emb:"His"@1 (w=23.50) +4 more |
| 7 | `get_upstream_features` | L0:F2994@1, k=5 | Emb:"His"@1 (w=19.75) +4 more |
| 8 | `get_upstream_features` | L6:F12990@1, k=5 | Emb:"His"@1 (w=4.91) +4 more |
| 9 | `inspect_feature` | L5, F10952 | "third person pronouns in varying contexts" |
| 10 | `get_upstream_features` | L5:F10952@1, k=5 | Emb:"His"@1 (w=10.69) +4 more |
| 11 | `inspect_feature` | L1, F7439 | " the possessive pronouns "his" and "him"" |
| 12 | `inspect_feature` | L2, F5491 | "references to God in the third person." |
| 13 | `get_upstream_features` | L2:F5491@1, k=5 | Emb:"His"@1 (w=23.88) +4 more |
| 14 | `inspect_feature` | L0, F1069 | " references to a male person, particularly when using the pronoun "He"" |

**Findings:** I traced the upstream circuit for the male pronoun detector feature (L7:F14946) which detects possessive pronoun "his" and similar male pronouns. The circuit reveals:

1. **Primary Input**: The strongest connection is directly from the input token "His" at position 1 (weight: 18.375), showing the feature is directly responsive to this specific token.

2. **Early Layer Processing**: Several early-l…

</details>

<details>
<summary><b>SA-3</b> — tool trace (16 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L19, F8814 | " various pronouns and names referring to people" |
| 2 | `get_upstream_features` | L19:F8814@1, k=5 | Emb:"His"@1 (w=9.38) +4 more |
| 3 | `inspect_feature` | L18, F7400 | " words related to coding and software/UI interfaces, with some bias to" |
| 4 | `inspect_feature` | L7, F14893 | " pronouns or possessive pronouns" |
| 5 | `inspect_feature` | L7, F14946 | " the possessive pronoun "his" (or similar pronouns like "he" and "him"" |
| 6 | `get_upstream_features` | L18:F7400@1, k=5 | Emb:"His"@1 (w=13.00) +4 more |
| 7 | `inspect_feature` | L15, F851 | " code documentation blocks in various programming languages" |
| 8 | `get_upstream_features` | L7:F14893@1, k=5 | Emb:"His"@1 (w=23.50) +4 more |
| 9 | `inspect_feature` | L6, F12990 | " male pronouns and titles along with descriptors associated with men" |
| 10 | `inspect_feature` | L0, F2994 | "the pronoun "his" and the pronoun "he."" |
| 11 | `inspect_feature` | L4, F4315 | " mentions of "his" and other associated pronouns like he, him, or hers" |
| 12 | `get_upstream_features` | L7:F14946@1, k=5 | Emb:"His"@1 (w=18.38) +4 more |
| 13 | `get_upstream_features` | L6:F12990@1, k=5 | Emb:"His"@1 (w=4.91) +4 more |
| 14 | `get_upstream_features` | L4:F4315@1, k=5 | Emb:"His"@1 (w=23.50) +4 more |
| 15 | `inspect_feature` | L1, F7439 | " the possessive pronouns "his" and "him"" |
| 16 | `inspect_feature` | L2, F5491 | "references to God in the third person." |

**Findings:** Tracing the circuit from pronoun/name feature L19:F8814 reveals a complex network for processing gender pronouns. The strongest direct input is the token "His" itself (weight 9.375), followed by a coding/software feature L18:F7400 that promotes masculine pronouns (weight 9.0625). Interestingly, there's competition between two features at layer 7: L7:F14946 (positive, detects "his" with weight 7.03…

</details>

<details>
<summary><b>SA-4</b> — tool trace (16 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L18, F14743 | "He" |
| 2 | `get_upstream_features` | L18:F14743@9, k=5 | Emb:" him"@9 (w=18.50) +4 more |
| 3 | `inspect_feature` | L0, F16297 | " the pronoun "him"" |
| 4 | `inspect_feature` | L16, F14120 | " references to people being directed and/or affected in some way." |
| 5 | `get_upstream_features` | L0:F16297@9, k=5 | Emb:" him"@9 (w=42.25) +4 more |
| 6 | `get_upstream_features` | L16:F14120@9, k=5 | Emb:" him"@9 (w=10.00) +4 more |
| 7 | `inspect_feature` | L14, F10344 | " pronouns related to feelings or actions" |
| 8 | `inspect_feature` | L14, F2710 | " language showing a causal relationship." |
| 9 | `get_upstream_features` | L14:F10344@9, k=5 | Emb:" him"@9 (w=14.62) +4 more |
| 10 | `inspect_feature` | L2, F5525 | " instances of something moving directly to a location like someone com" |
| 11 | `get_upstream_features` | L2:F5525@9, k=5 | Emb:" him"@9 (w=12.31) +4 more |
| 12 | `get_upstream_features` | L14:F2710@9, k=5 | Emb:" him"@9 (w=6.75) +4 more |
| 13 | `inspect_feature` | L5, F2701 | "phrases meaning "the actor" performing "actions."" |
| 14 | `get_upstream_features` | L5:F2701@9, k=5 | Emb:" him"@9 (w=7.25) +4 more |
| 15 | `inspect_feature` | L4, F14959 | " verbs indicating causation, as well as pronouns following them" |
| 16 | `inspect_feature` | L6, F38 | "the word "keep" and its variants" |

**Findings:** I traced the circuit feeding into the L18 'He' pronoun detector at position 9. The circuit shows two main pathways:

1. **Direct lexical pathway**: The strongest connection (edge weight 18.5) is directly from the embedding of " him" at position 9 to the 'He' detector. There's also a layer 0 feature (16297) that specifically detects the pronoun "him", which feeds into both the 'He' detector (weight…

</details>

### Re-dispatch (round 2): 1 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-5 | `L14:F4420@21` | ✅ reported | 10 | 17 | Trace the upstream path for this journalism feature. What feeds into it? This co… |

<details>
<summary><b>SA-5</b> — tool trace (17 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L14, F4420 | "words and phrases related to journalism and newspapers" |
| 2 | `get_upstream_features` | L14:F4420@21, k=5 | Emb:" report"@21 (w=5.19) +4 more |
| 3 | `inspect_feature` | L8, F8855 | " mentions of news reporters and news reporting" |
| 4 | `inspect_feature` | L7, F13646 | " news reporting and journalism." |
| 5 | `inspect_feature` | L8, F8437 | "content related to film festivals and production, particularly documen" |
| 6 | `get_upstream_features` | L8:F8855@21, k=5 | Emb:" report"@21 (w=12.06) +4 more |
| 7 | `get_upstream_features` | L7:F13646@21, k=5 | Emb:" report"@21 (w=7.22) +4 more |
| 8 | `inspect_feature` | L4, F661 | " words and phrases used when referring to reports, documentaries, and " |
| 9 | `get_upstream_features` | L4:F661@21, k=5 | Emb:" report"@21 (w=14.38) +4 more |
| 10 | `inspect_feature` | L1, F14511 | " the word "report"" |
| 11 | `inspect_feature` | L2, F11175 | "the verb "report" and its variations" |
| 12 | `inspect_feature` | L3, F10846 | "the word "report"" |
| 13 | `get_upstream_features` | L1:F14511@21, k=5 | Emb:" report"@21 (w=20.62) +4 more |
| 14 | `inspect_feature` | L0, F1014 | " instances of measurement, experimentation, and quantification" |
| 15 | `get_upstream_features` | L2:F11175@21, k=5 | Emb:" report"@21 (w=32.50) +4 more |
| 16 | `get_upstream_features` | L8:F8437@21, k=5 | Emb:" report"@21 (w=5.75) +4 more |
| 17 | `inspect_feature` | L9, F7435 | " words and phrases related to news production and media" |

**Findings:** The circuit for the journalism feature (L14:F4420) is primarily driven by the raw input token "report" at position 21. Key findings:

1. The journalism feature promotes tokens like "journalists", "journalistic", "journalist", "journalism", "reporter", etc.

2. The strongest upstream connections come directly from the embedding token "report" itself, with decreasing but strong weights at each layer…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` ×2 | L14:4420, L0:8444 |

### Build

`build_circuit` → 10 nodes, 11 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m2.7 | 42,985 | 3,883 | 84,206 | 0 | — | — | — |
| SA-1 | deepseek/deepseek-v3.2 | 89,773 | 4,112 | 0 | 0 | — | ✅ 7F/23E | Trace the path from this female pronoun detector feature ups… |
| SA-4 | deepseek/deepseek-v3.2 | 116,173 | 3,847 | 9,152 | 0 | — | ✅ 9F/9E | Trace the path from this 'He' pronoun detector at position 9… |
| SA-3 | deepseek/deepseek-v3.2 | 120,877 | 4,293 | 11,072 | 0 | — | ✅ 10F/19E | Trace the path from this pronoun/name feature upstream. What… |
| SA-2 | deepseek/deepseek-v3.2 | 101,755 | 4,713 | 0 | 0 | — | ✅ 8F/27E | Trace the path from this male pronoun detector feature upstr… |
| SA-5 | deepseek/deepseek-v3.2 | 130,942 | 5,339 | 10,304 | 0 | — | ✅ 10F/17E | Trace the upstream path for this journalism feature. What fe… |
| **Total** | | **602,505** | **26,187** | **114,734** | **0** | **—** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 7m 33s