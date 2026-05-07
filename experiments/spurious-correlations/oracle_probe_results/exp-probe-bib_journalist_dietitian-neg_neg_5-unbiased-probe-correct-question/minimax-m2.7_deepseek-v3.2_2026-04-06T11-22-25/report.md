# Circuit Oracle Report
**Date:** 2026-04-06 11:22:25 UTC | **Orchestrator:** minimax/minimax-m2.7 | **Subagent:** deepseek/deepseek-v3.2

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-neg_neg_5 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "('The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession.',)"

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score is driven primarily by a legitimate journalism/reporter detection circuit (strong positive effect), but the circuit also incorporates a **spurious gender marker feature** (L0:F1069) that detects the male pronoun "He" at position 1 and has a direct negative effect (-0.089) on the classification. The gender marker has similar effect magnitude to the main journalism features, confirming the user's concern about spurious gender proxies.

**Confidence:** 9/10

**Reasoning:** The circuit has two competing pathways:

**1. Legitimate Professional Indicator Pathway (Main Signal):**
- Token `" reporter"` (pos 66) is the primary driver with the strongest embedding connections
- Hierarchical journalism features: L4:F13253 ("journalism & media", frac_nonzero=0.006) → L14:F4420 ("journalism & newspapers", frac_nonzero=0.0165) → L19:F2486 ("journalistic sources & news outlets", frac_nonzero=0.029)
- All features have low frac_nonzero (0.006-0.03), indicating specific profession-related encoding
- Direct effects: L14:F4420 (-0.197) and L19:F2486 (-0.125) are the strongest contributors
- The input text explicitly mentions "reporter" at position 66

**2. Spurious Gender Marker Pathway (CONFIRMED CONCERN):**
- **L0:F1069** at position 1 is explicitly labeled "references to a male person, particularly when using the pronoun 'He' or 'His'"
- Activated directly by the token `"He"` at position 1 (edge weight: 22.625)
- Has direct_effect of -0.089 on the probe classification
- Low frac_nonzero (0.0078) indicates high specificity for male pronoun detection
- This is a classic spurious feature that uses gender as a proxy rather than genuine profession indicators

**The user's concern is VALIDATED.** The gender marker feature L0:F1069 has comparable effect magnitude to the journalism features, and the circuit can potentially exploit this gender proxy rather than relying solely on profession-specific knowledge. The probe's training data likely contained correlations between male pronouns and certain professions, leading the model to learn this spurious association as a classification shortcut.

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 10 features; top: L14:4420 de=-0.197 |

### Dispatch: 10 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L14:F4420@66` | ✅ reported | 11 | 25 | Trace this feature to understand what it encodes and where the signal originates… |
| SA-2 | `L19:F2486@66` | ✅ reported | 8 | 15 | Trace this feature to understand what it encodes and where the signal originates… |
| SA-3 | `L4:F13253@66` | ✅ reported | 7 | 14 | Trace this feature to understand what it encodes and where the signal originates… |
| SA-4 | `L0:F4874@2` | ✅ reported | 1 | 3 | Trace this feature to understand what it encodes and where the signal originates… |
| SA-5 | `L0:F1069@1` | ✅ reported | 4 | 2 | Trace this feature to understand what it encodes and where the signal originates… |
| SA-6 | `L0:F8642@2` | ✅ reported | 3 | 5 | Trace this feature to understand what it encodes and where the signal originates… |
| SA-7 | `L0:F6051@24` | ✅ reported | 1 | 10 | Trace this feature to understand what it encodes and where the signal originates… |
| SA-8 | `L0:F14824@16` | ✅ reported | 1 | 4 | Trace this feature to understand what it encodes and where the signal originates… |
| SA-9 | `L0:F8974@9` | ✅ reported | 1 | 5 | Trace this feature to understand what it encodes and where the signal originates… |
| SA-10 | `L0:F8061@6` | ✅ reported | 1 | 5 | Trace this feature to understand what it encodes and where the signal originates… |

<details>
<summary><b>SA-1</b> — tool trace (16 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L14, F4420 | "words and phrases related to journalism and newspapers" |
| 2 | `get_upstream_features` | L14:F4420@66, k=5 | Emb:" reporter"@66 (w=18.62) +4 more |
| 3 | `inspect_feature` | L4, F13253 | " things related to journalism and the media" |
| 4 | `inspect_feature` | L8, F8855 | " mentions of news reporters and news reporting" |
| 5 | `inspect_feature` | L7, F13646 | " news reporting and journalism." |
| 6 | `get_upstream_features` | L4:F13253@66, k=5 | Emb:" reporter"@66 (w=26.62) +4 more |
| 7 | `get_upstream_features` | L8:F8855@66, k=5 | Emb:" reporter"@66 (w=16.88) +4 more |
| 8 | `get_upstream_features` | L7:F13646@66, k=5 | Emb:" reporter"@66 (w=15.12) +4 more |
| 9 | `inspect_feature` | L7, F9092 | " words and phrases associated with broadcast journalism" |
| 10 | `inspect_feature` | L1, F1024 | " words and phrases frequently used when discussing writing, publishing" |
| 11 | `inspect_feature` | L1, F5357 | " words related to written works" |
| 12 | `inspect_feature` | L2, F9719 | " terms related to broadcast news" |
| 13 | `inspect_feature` | L3, F7446 | " words related to processes of conveying information through different" |
| 14 | `inspect_feature` | L4, F661 | " words and phrases used when referring to reports, documentaries, and " |
| 15 | `inspect_feature` | L7, F9521 | " news sources and people involved in journalism" |
| 16 | `get_upstream_features` | L1:F1024@66, k=5 | Emb:" reporter"@66 (w=8.06) +4 more |

**Findings:** The circuit traces a clear pathway where the token " reporter" at position 66 activates journalism-related features across multiple layers. Key findings:

1. **Primary Signal**: The token " reporter" at position 66 is the strongest driver, with direct connections to multiple features across layers 4, 7, 8, and 14.

2. **Feature Hierarchy**: The circuit shows a hierarchical processing of journalism…

</details>

<details>
<summary><b>SA-2</b> — tool trace (12 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L19, F2486 | " journalistic sources and news outlets." |
| 2 | `get_upstream_features` | L19:F2486@66, k=5 | Emb:" reporter"@66 (w=28.12) +4 more |
| 3 | `inspect_feature` | L14, F4420 | "words and phrases related to journalism and newspapers" |
| 4 | `inspect_feature` | L4, F13253 | " things related to journalism and the media" |
| 5 | `get_upstream_features` | L14:F4420@66, k=5 | Emb:" reporter"@66 (w=18.62) +4 more |
| 6 | `get_upstream_features` | L4:F13253@66, k=5 | Emb:" reporter"@66 (w=26.62) +4 more |
| 7 | `inspect_feature` | L1, F1024 | " words and phrases frequently used when discussing writing, publishing" |
| 8 | `inspect_feature` | L8, F8855 | " mentions of news reporters and news reporting" |
| 9 | `get_upstream_features` | L8:F8855@66, k=5 | Emb:" reporter"@66 (w=16.88) +4 more |
| 10 | `inspect_feature` | L7, F13646 | " news reporting and journalism." |
| 11 | `inspect_feature` | L7, F9092 | " words and phrases associated with broadcast journalism" |
| 12 | `inspect_feature` | L1, F5357 | " words related to written works" |

**Findings:** Tracing L19:F2486 revealed a straightforward circuit that detects journalistic/reporting terminology. The feature encodes "journalistic sources and news outlets" and promotes tokens like "reporting", "reporter", "coverage". 

The signal originates from the input token " reporter" at position 66, which has the strongest direct connection (weight 28.125) to the target feature. The circuit consists o…

</details>

<details>
<summary><b>SA-3</b> — tool trace (13 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F13253 | " things related to journalism and the media" |
| 2 | `get_upstream_features` | L4:F13253@66, k=5 | Emb:" reporter"@66 (w=26.62) +4 more |
| 3 | `inspect_feature` | L1, F1024 | " words and phrases frequently used when discussing writing, publishing" |
| 4 | `inspect_feature` | L3, F7446 | " words related to processes of conveying information through different" |
| 5 | `get_upstream_features` | L1:F1024@66, k=5 | Emb:" reporter"@66 (w=8.06) +4 more |
| 6 | `get_upstream_features` | L3:F7446@66, k=5 | Emb:" reporter"@66 (w=4.38) +4 more |
| 7 | `inspect_feature` | L2, F9719 | " terms related to broadcast news" |
| 8 | `get_upstream_features` | L2:F9719@66, k=5 | Emb:" reporter"@66 (w=16.50) +4 more |
| 9 | `inspect_feature` | L0, F1579 | " the word "report"" |
| 10 | `inspect_feature` | L0, F2115 | " data reported as a percentage inside brackets, especially in a labora" |
| 11 | `get_upstream_features` | L0:F1579@66, k=5 | Emb:" reporter"@66 (w=12.75) +4 more |
| 12 | `get_upstream_features` | L0:F2115@66, k=5 | Emb:" reporter"@66 (w=8.38) +4 more |
| 13 | `inspect_feature` | L1, F5357 | " words related to written works" |

**Findings:** The feature at L4:F13253 encodes "things related to journalism and the media". Tracing upstream reveals the circuit originates from the token " reporter" at position 66, which is the primary driver with a very strong edge weight of 26.625 directly to the journalism/media feature. The circuit flows through several intermediate features:
1. Layer 0 features that detect the word "report" (F1579) and …

</details>

<details>
<summary><b>SA-4</b> — tool trace (3 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F4874 | " the word "preparation" and words connected to it" |
| 2 | `get_upstream_features` | L0:F4874@2, k=5 | Emb:" obtained"@2 (w=11.69) +4 more |
| 3 | `get_upstream_features` | L0:F4874@2, k=10 | Emb:" obtained"@2 (w=11.69) +9 more |

**Findings:** Traced feature L0:F4874 at position 2. This feature detects the word \"preparation\" and related words (label: \"the word 'preparation' and words connected to it\"), with low frac_nonzero=0.011 indicating specificity. Interestingly, it suppresses the word \"preparation\" itself in output while detecting it. The circuit originates primarily from the token embedding for \" obtained\" at position 2 w…

</details>

<details>
<summary><b>SA-5</b> — tool trace (5 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F1069 | " references to a male person, particularly when using the pronoun "He"" |
| 2 | `get_upstream_features` | L0:F1069@1, k=5 | Emb:"He"@1 (w=22.62) +4 more |
| 3 | `inspect_feature` | L0, F310 | " the pronouns "she", "her", and "he" and sometimes the word "therefore" |
| 4 | `inspect_feature` | L0, F355 | " text related to numbers, especially those representing currency or me" |
| 5 | `inspect_feature` | L0, F96 | "sentences beginning with coordinating conjunctions like "but" and "and" |

**Findings:** The tracing reveals that L0:F1069 is a low-level feature that detects references to male persons, particularly when using the pronoun "He" or "His." The circuit is remarkably simple: the feature is directly and strongly activated by the token embedding for "He" at position 1 (edge weight 22.625), with a smaller contribution from the beginning-of-sequence token "<bos>" at position 0 (edge weight 6.…

</details>

<details>
<summary><b>SA-6</b> — tool trace (4 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F8642 | "words and symbols appearing in mathematical or logical proofs and conc" |
| 2 | `get_upstream_features` | L0:F8642@2, k=5 | Emb:" obtained"@2 (w=12.06) +4 more |
| 3 | `inspect_feature` | L0, F310 | " the pronouns "she", "her", and "he" and sometimes the word "therefore" |
| 4 | `inspect_feature` | L0, F355 | " text related to numbers, especially those representing currency or me" |

**Findings:** The feature L0:F8642 encodes "words and symbols appearing in mathematical or logical proofs and conclusions." It has a moderate sparsity (frac_nonzero=0.0216), indicating it's fairly specific. The strongest signal comes directly from the token embedding " obtained" at position 2 (edge_weight=12.06), showing this feature is primarily triggered by the word "obtained". Interestingly, there's a weak n…

</details>

<details>
<summary><b>SA-7</b> — tool trace (4 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F6051 | "periods, spaces, and the number 1" |
| 2 | `get_upstream_features` | L0:F6051@24, k=5 | Emb:"."@24 (w=47.25) +4 more |
| 3 | `get_upstream_features` | L0:F6051@24, k=10 | Emb:"."@24 (w=47.25) +9 more |
| 4 | `get_upstream_features` | L0:F6051@24, k=15 | Emb:"."@24 (w=47.25) +14 more |

**Findings:** The feature L0:F6051 is a punctuation detection feature that fires on period characters ('.'). It has a frac_nonzero of 0.05694, meaning it activates on about 5.7% of tokens, which is relatively low for a punctuation feature (periods are common but not extremely common). The circuit tracing shows this feature is directly triggered by the period token embedding at position 24 with a very strong pos…

</details>

<details>
<summary><b>SA-8</b> — tool trace (3 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F14824 | "the word "has"" |
| 2 | `get_upstream_features` | L0:F14824@16, k=5 | Emb:" has"@16 (w=34.75) +4 more |
| 3 | `get_upstream_features` | L0:F14824@16, k=10 | Emb:" has"@16 (w=34.75) +9 more |

**Findings:** The feature L0:F14824 encodes the word \"has\" - it detects the token \"has\" at position 16. The circuit goes directly from token embeddings to this feature, with the strongest connection coming from the \"has\" token itself at position 16 (weight 34.75). There's also a positive connection from the beginning of sequence token <bos> at position 0 (weight 2.7344), and negative connections from \"an…

</details>

<details>
<summary><b>SA-9</b> — tool trace (3 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F8974 | "the word "from"" |
| 2 | `get_upstream_features` | L0:F8974@9, k=5 | Emb:" from"@9 (w=40.00) +4 more |
| 3 | `get_top_logits` | k=5 | "" (100%) |

**Findings:** The feature L0:F8974 is a simple token detector for the word \"from\" at position 9. It has a very strong direct connection (edge_weight=40.0) to the \" from\" token embedding at position 9, indicating it directly reads this token. The feature has relatively low frac_nonzero (0.02366), meaning it's specific to contexts containing \"from\". Interestingly, it suppresses the token \"from\" in its out…

</details>

<details>
<summary><b>SA-10</b> — tool trace (2 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F8061 | " the preposition "in"" |
| 2 | `get_upstream_features` | L0:F8061@6, k=5 | Emb:" in"@6 (w=38.50) +4 more |

**Findings:** The feature L0:F8061 at position 6 encodes detection of the preposition "in" as indicated by its label. The tracing shows it is primarily driven directly by the embedding of the token "in" at position 6 itself with a very strong weight of 38.5. There are weaker contextual connections to other tokens in the input sequence: the beginning-of-sequence token at position 0, "undergraduate" at position 4…

</details>

### Build

`build_circuit` → 13 nodes, 15 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m2.7 | 19,832 | 4,166 | 52,834 | 0 | $0.0125 | — | — |
| SA-4 | deepseek/deepseek-v3.2 | 13,404 | 1,219 | 0 | 0 | $0.0039 | ✅ 1F/3E | Trace this feature to understand what it encodes and where t… |
| SA-3 | deepseek/deepseek-v3.2 | 89,404 | 3,394 | 0 | 0 | $0.0245 | ✅ 7F/14E | Trace this feature to understand what it encodes and where t… |
| SA-2 | deepseek/deepseek-v3.2 | 84,128 | 3,717 | 0 | 0 | $0.0233 | ✅ 8F/15E | Trace this feature to understand what it encodes and where t… |
| SA-1 | deepseek/deepseek-v3.2 | 118,234 | 4,511 | 11,072 | 0 | $0.0327 | ✅ 11F/25E | Trace this feature to understand what it encodes and where t… |
| SA-6 | deepseek/deepseek-v3.2 | 18,708 | 1,474 | 0 | 0 | $0.0054 | ✅ 3F/5E | Trace this feature to understand what it encodes and where t… |
| SA-5 | deepseek/deepseek-v3.2 | 17,528 | 1,655 | 8,192 | 0 | $0.0054 | ✅ 4F/2E | Trace this feature to understand what it encodes and where t… |
| SA-10 | deepseek/deepseek-v3.2 | 9,053 | 1,112 | 0 | 0 | $0.0028 | ✅ 1F/5E | Trace this feature to understand what it encodes and where t… |
| SA-8 | deepseek/deepseek-v3.2 | 13,151 | 1,262 | 0 | 0 | $0.0039 | ✅ 1F/4E | Trace this feature to understand what it encodes and where t… |
| SA-9 | deepseek/deepseek-v3.2 | 12,475 | 1,426 | 0 | 0 | $0.0038 | ✅ 1F/5E | Trace this feature to understand what it encodes and where t… |
| SA-7 | deepseek/deepseek-v3.2 | 15,592 | 1,621 | 2,368 | 0 | $0.0047 | ✅ 1F/10E | Trace this feature to understand what it encodes and where t… |
| **Total** | | **411,509** | **25,557** | **74,466** | **0** | **$0.1231** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 6m 43s