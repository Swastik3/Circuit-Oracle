# Circuit Oracle Report
**Date:** 2026-03-26 10:34:04 UTC | **Orchestrator:** anthropic/claude-opus-4.6 | **Subagent:** anthropic/claude-sonnet-4.6

## Input
**Prompt:** "Dataset: bib_journalist_dietitian-neg_neg_1 | Probe: unbiased | Method: correct"
**System prompt:** ""
**Concern:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."
**Top predictions:**  (100.0%)

## Oracle Analysis
## Analysis

**Analysis:** The probe classification is driven by a stark split: genuine journalism-detection features (originating from "report" and "news" tokens) all push **against** the probe's target class, while the features pushing **toward** the target class are dominated by shallow, generic token-level features — most notably the gender marker "His" — confirming the user's concern about spurious feature reliance.

**Confidence:** High

**Reasoning:**

### The Two Competing Signal Pathways

**1. The Journalism Pathway (NEGATIVE effect on probe — total contribution ~-0.70):**

This is a deep, well-structured, semantically coherent circuit originating from the tokens "report" (pos 21) and "news" (pos 27). It traces through a clean abstraction hierarchy:

- **Token-level detection (L1-L3):** Features L1:14511, L2:11175, L3:10846 (all frac_nonzero < 0.005) detect the raw word "report"
- **Concept formation (L4-L5):** L4:661 ("reports, documentaries, TV coverage", frac=0.009) and L5:12586 ("mentions of reports", frac=0.007) build media/journalism semantics
- **Journalism specialization (L7-L8):** L7:13646 ("news reporting and journalism", frac=0.008) and L8:8855 ("news reporters", frac=0.008) — both highly specific, promoting tokens like "journalist", "reporter", "correspondent"
- **Integration (L14):** L14:4420 ("journalism and newspapers", frac=0.017) is the strongest single feature in the circuit with direct_effect = **-0.148**
- **Late-layer elaboration (L16-L20):** L19:2486 ("journalistic sources", frac=0.029) fires at **7 different positions** with cumulative negative effect ~-0.45; L20:8433 ("news broadcasting", frac=0.036) adds another -0.051

All of these are entity-specific features with low frac_nonzero values, specifically encoding journalism knowledge. Their **uniformly negative** direct effects on the probe mean they're actively suppressing the probe's target class — i.e., the probe is classifying a profession that is **not** journalist.

**2. The Spurious/Generic Pathway (POSITIVE effect on probe — total contribution ~+0.45):**

The features pushing the probe score **up** are almost entirely layer-0 generic token detectors:
- **L0:8964 ("His" possessive pronoun, frac=0.018): +0.087** — the single strongest positive contributor, driven purely by the "His" token embedding (edge_weight=13.7). This is a **gender marker**, not a profession indicator.
- L0:8444 ("to"): +0.082, +0.057 at two positions
- L0:14287 ("see"): +0.065
- L0:2011 ("desire/dream"): +0.054
- L0:13948 (detects "pink" — fires on "desire" possibly as noise): +0.054
- L0:15693 ("personal anecdotes"): +0.051

None of these features encode profession-specific knowledge. They are low-level token identity detectors at layer 0 with generic promoted tokens (punctuation, function words). The fact that "His" is the strongest positive driver strongly implicates **gender as a spurious feature** in this probe.

### The User's Concern is Validated

The circuit reveals a clear structural problem: **the probe's positive classification signal comes almost entirely from shallow, non-semantic features** (especially the gender marker "His"), while the **genuine profession-specific features (journalism detection) all oppose the prediction**. This suggests the probe at layer 22 has learned to partially rely on gender correlations in the training data (male pronouns correlating with certain professions) rather than exclusively using the rich journalism-detection features that the model actually computes through a deep, multi-layer circuit.

The journalism pathway is a textbook example of well-formed knowledge encoding — hierarchical, specific (low frac_nonzero), and semantically coherent from token → concept → domain. But the probe largely ignores this pathway (or uses it only as a negative signal to rule out journalism), while positively weighting superficial cues like gendered pronouns and common function words that happen to correlate with the target profession in training data.

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L14:4420 de=-0.147 |
| 3 | `inspect_feature` ×13 | L14:4420, L19:2486, L0:8964, L0:8444, L0:14287, L0:2203, L0:2011, L0:13948, L1:14511, L8:8855, L20:8433, L0:15693, L5:771 |

### Dispatch: 5 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L14:F4420@21` | ✅ reported | 11 | 17 | Trace the path from L14:4420 (journalism and newspapers) at pos 21 — what feeds … |
| SA-2 | `L19:F2486@21` | ✅ reported | 12 | 19 | Trace the path from L19:2486 (journalistic sources and news outlets) at pos 21 —… |
| SA-3 | `L8:F8855@21` | ✅ reported | 12 | 22 | Trace the path from L8:8855 (news reporters and reporting) at pos 21 — what feed… |
| SA-4 | `L20:F8433@26` | ✅ reported | 11 | 16 | Trace the path from L20:8433 (news broadcasting) at pos 26 — what upstream featu… |
| SA-5 | `L19:F2486@29` | ✅ reported | 9 | 11 | Trace the path from L19:2486 (journalistic sources) at pos 29 (likely 'organizat… |

<details>
<summary><b>SA-1</b> — tool trace (15 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L14, F4420 | "words and phrases related to journalism and newspapers" |
| 2 | `get_upstream_features` | L14:F4420@21, k=8 | Emb:" report"@21 (w=5.19) +7 more |
| 3 | `inspect_feature` | L8, F8855 | " mentions of news reporters and news reporting" |
| 4 | `inspect_feature` | L7, F13646 | " news reporting and journalism." |
| 5 | `inspect_feature` | L8, F8437 | "content related to film festivals and production, particularly documen" |
| 6 | `get_upstream_features` | L8:F8855@21, k=8 | Emb:" report"@21 (w=12.06) +7 more |
| 7 | `get_upstream_features` | L7:F13646@21, k=8 | Emb:" report"@21 (w=7.22) +7 more |
| 8 | `inspect_feature` | L4, F661 | " words and phrases used when referring to reports, documentaries, and " |
| 9 | `inspect_feature` | L6, F12624 | "words related to art, architecture, or law." |
| 10 | `inspect_feature` | L7, F13896 | " words or phrases related to reports, people's names, and versions" |
| 11 | `get_upstream_features` | L4:F661@21, k=6 | Emb:" report"@21 (w=14.38) +5 more |
| 12 | `inspect_feature` | L1, F14511 | " the word "report"" |
| 13 | `inspect_feature` | L1, F9794 | "words and phrases associated with the film industry, including film pr" |
| 14 | `inspect_feature` | L2, F11175 | "the verb "report" and its variations" |
| 15 | `inspect_feature` | L3, F10846 | "the word "report"" |

**Findings:** The journalism/newspapers detection feature at L14:F4420 originates overwhelmingly from the token embedding of " report" at position 21. The circuit follows a clear bottom-up pathway:

1. RAW TOKEN ORIGIN: The " report" token embedding at pos 21 is the single most dominant input at EVERY layer traced. It drives L4:661 with weight 14.375, L7:13646 with weight 7.22, L8:8855 with weight 12.06, and ev…

</details>

<details>
<summary><b>SA-2</b> — tool trace (18 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L19, F2486 | " journalistic sources and news outlets." |
| 2 | `get_upstream_features` | L19:F2486@21, k=8 | L14:F4420 (w=14.31) +7 more |
| 3 | `inspect_feature` | L14, F4420 | "words and phrases related to journalism and newspapers" |
| 4 | `inspect_feature` | L16, F8642 | " text related to official reporting and legal issues." |
| 5 | `inspect_feature` | L8, F8855 | " mentions of news reporters and news reporting" |
| 6 | `get_upstream_features` | L14:F4420@21, k=8 | Emb:" report"@21 (w=5.19) +7 more |
| 7 | `inspect_feature` | L7, F13646 | " news reporting and journalism." |
| 8 | `inspect_feature` | L8, F8437 | "content related to film festivals and production, particularly documen" |
| 9 | `get_upstream_features` | L8:F8855@21, k=8 | Emb:" report"@21 (w=12.06) +7 more |
| 10 | `get_upstream_features` | L7:F13646@21, k=8 | Emb:" report"@21 (w=7.22) +7 more |
| 11 | `inspect_feature` | L3, F10846 | "the word "report"" |
| 12 | `inspect_feature` | L5, F12586 | " mentions of reports" |
| 13 | `inspect_feature` | L6, F12624 | "words related to art, architecture, or law." |
| 14 | `inspect_feature` | L4, F661 | " words and phrases used when referring to reports, documentaries, and " |
| 15 | `inspect_feature` | L0, F12801 | " verbs related to communication, help, enabling, and allowing" |
| 16 | `get_upstream_features` | L4:F661@21, k=6 | Emb:" report"@21 (w=14.38) +5 more |
| 17 | `inspect_feature` | L2, F11175 | "the verb "report" and its variations" |
| 18 | `inspect_feature` | L1, F14511 | " the word "report"" |

**Findings:** The circuit driving L19:F2486 ("journalistic sources and news outlets") at pos 21 is rooted almost entirely in the raw token embedding of " report" at position 21. This single token propagates through a coherent, domain-specific journalism pathway spanning all 19 layers:

ROOT INPUT: The token embedding " report" (pos 21) is the overwhelmingly dominant input signal throughout the circuit — it dire…

</details>

<details>
<summary><b>SA-3</b> — tool trace (16 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L8, F8855 | " mentions of news reporters and news reporting" |
| 2 | `get_upstream_features` | L8:F8855@21, k=8 | Emb:" report"@21 (w=12.06) +7 more |
| 3 | `inspect_feature` | L7, F13646 | " news reporting and journalism." |
| 4 | `inspect_feature` | L7, F13896 | " words or phrases related to reports, people's names, and versions" |
| 5 | `inspect_feature` | L6, F12624 | "words related to art, architecture, or law." |
| 6 | `inspect_feature` | L5, F12586 | " mentions of reports" |
| 7 | `get_upstream_features` | L7:F13646@21, k=6 | Emb:" report"@21 (w=7.22) +5 more |
| 8 | `inspect_feature` | L4, F661 | " words and phrases used when referring to reports, documentaries, and " |
| 9 | `inspect_feature` | L4, F6696 | "the word "report" or "reporting" along with adjacent words" |
| 10 | `inspect_feature` | L6, F12712 | " titles of editors and publishers in scientific publications" |
| 11 | `get_upstream_features` | L5:F12586@21, k=6 | Emb:" report"@21 (w=32.25) +5 more |
| 12 | `inspect_feature` | L3, F10846 | "the word "report"" |
| 13 | `inspect_feature` | L2, F11175 | "the verb "report" and its variations" |
| 14 | `get_upstream_features` | L4:F661@21, k=6 | Emb:" report"@21 (w=14.38) +5 more |
| 15 | `inspect_feature` | L1, F14511 | " the word "report"" |
| 16 | `inspect_feature` | L1, F9794 | "words and phrases associated with the film industry, including film pr" |

**Findings:** The L8:8855 "news reporters and journalism" feature is primarily driven by the raw token embedding of " report" at position 21 — this is the dominant causal source at every layer of the circuit. Here is the full picture:

**Primary driver: Token embedding " report" (pos 21)**
The word " report" in the input is the overwhelming upstream cause. Its embedding directly excites every feature in the cha…

</details>

<details>
<summary><b>SA-4</b> — tool trace (15 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L20, F8433 | "words related to news broadcasting" |
| 2 | `get_upstream_features` | L20:F8433@26, k=8 | Emb:" top"@26 (w=5.72) +7 more |
| 3 | `inspect_feature` | L17, F5218 | " text about journalism, media, and related topics" |
| 4 | `inspect_feature` | L14, F4420 | "words and phrases related to journalism and newspapers" |
| 5 | `inspect_feature` | L19, F2486 | " journalistic sources and news outlets." |
| 6 | `get_upstream_features` | L14:F4420@21, k=6 | Emb:" report"@21 (w=5.19) +5 more |
| 7 | `get_upstream_features` | L19:F2486@26, k=6 | L14:F4420 (w=6.28) +5 more |
| 8 | `get_upstream_features` | L17:F5218@26, k=6 | Emb:" report"@21 (w=2.09) +5 more |
| 9 | `inspect_feature` | L8, F8855 | " mentions of news reporters and news reporting" |
| 10 | `inspect_feature` | L7, F9092 | " words and phrases associated with broadcast journalism" |
| 11 | `inspect_feature` | L16, F15046 | " names, organizations, and reporting verbs" |
| 12 | `get_upstream_features` | L8:F8855@21, k=6 | Emb:" report"@21 (w=12.06) +5 more |
| 13 | `get_upstream_features` | L7:F9092@26, k=6 | L2:F10902 (w=1.16) +5 more |
| 14 | `inspect_feature` | L7, F13646 | " news reporting and journalism." |
| 15 | `inspect_feature` | L2, F10902 | "the word "top"." |

**Findings:** The news broadcasting feature at L20:F8433 (pos 26) is driven by a deep, coherent journalism circuit that originates from two key input signals:

PRIMARY PATHWAY — " report" token embedding (pos 21, edge_weight 12.06):
The word " report" in the input is the single most powerful driver. It activates L7:F13646 ("news reporting and journalism", frac=0.0076) and L8:F8855 ("mentions of news reporters a…

</details>

<details>
<summary><b>SA-5</b> — tool trace (14 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L19, F2486 | " journalistic sources and news outlets." |
| 2 | `get_upstream_features` | L19:F2486@29, k=8 | Emb:" news"@27 (w=7.94) +7 more |
| 3 | `inspect_feature` | L14, F4420 | "words and phrases related to journalism and newspapers" |
| 4 | `inspect_feature` | L16, F11532 | "newspaper" |
| 5 | `inspect_feature` | L16, F8642 | " text related to official reporting and legal issues." |
| 6 | `get_upstream_features` | L14:F4420@29, k=8 | Emb:" news"@27 (w=4.47) +7 more |
| 7 | `inspect_feature` | L7, F9092 | " words and phrases associated with broadcast journalism" |
| 8 | `inspect_feature` | L7, F13646 | " news reporting and journalism." |
| 9 | `inspect_feature` | L4, F13253 | " things related to journalism and the media" |
| 10 | `get_upstream_features` | L7:F9092@29, k=6 | Emb:" news"@27 (w=7.94) +5 more |
| 11 | `get_upstream_features` | L4:F13253@29, k=6 | Emb:" news"@27 (w=10.62) +5 more |
| 12 | `get_upstream_features` | L7:F13646@29, k=6 | Emb:" report"@21 (w=5.38) +5 more |
| 13 | `inspect_feature` | L0, F6051 | "periods, spaces, and the number 1" |
| 14 | `inspect_feature` | L1, F14454 | " a highly variable set of keywords, potentially related to news articl" |

**Findings:** ## Circuit: Journalistic Sources / News Outlets (L19:F2486, pos 29)

### Core Signal: Raw Token Embeddings
The single most powerful driver throughout the entire circuit is the **raw embedding of the token `" news"`** (pos 27), which carries a direct edge weight of **+7.94** into L19:F2486 and also dominates the mid-layer features (weight +4.47 into L14:F4420, +10.63 into L4:F13253). The token `" r…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` | L0, F8964 → " the possessive pronoun "His"" |
| 2 | `get_upstream_features` | L0:F8964@1, k=5 → Emb:"His"@1 (w=13.69) +4 more |

### Build

`build_circuit` → 21 nodes, 31 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | anthropic/claude-opus-4.6 | 133,506 | 6,435 | 0 | 0 | $0.8284 | — | — |
| SA-4 | anthropic/claude-sonnet-4.6 | 57,853 | 4,094 | 0 | 0 | $0.2350 | ✅ 11F/16E | Trace the path from L20:8433 (news broadcasting) at pos 26 —… |
| SA-1 | anthropic/claude-sonnet-4.6 | 47,539 | 4,337 | 0 | 0 | $0.2077 | ✅ 11F/17E | Trace the path from L14:4420 (journalism and newspapers) at … |
| SA-3 | anthropic/claude-sonnet-4.6 | 54,302 | 4,334 | 0 | 0 | $0.2279 | ✅ 12F/22E | Trace the path from L8:8855 (news reporters and reporting) a… |
| SA-5 | anthropic/claude-sonnet-4.6 | 50,435 | 4,096 | 0 | 0 | $0.2127 | ✅ 9F/11E | Trace the path from L19:2486 (journalistic sources) at pos 2… |
| SA-2 | anthropic/claude-sonnet-4.6 | 68,983 | 4,687 | 0 | 0 | $0.2773 | ✅ 12F/19E | Trace the path from L19:2486 (journalistic sources and news … |
| **Total** | | **412,618** | **27,983** | **0** | **0** | **$1.9890** | | |

**Oracle wall-clock time:** 3m 11s