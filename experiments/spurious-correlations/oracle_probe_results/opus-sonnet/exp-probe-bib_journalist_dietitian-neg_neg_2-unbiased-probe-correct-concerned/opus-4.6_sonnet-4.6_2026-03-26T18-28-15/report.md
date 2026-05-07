# Circuit Oracle Report
**Date:** 2026-03-26 18:28:15 UTC | **Orchestrator:** anthropic/claude-opus-4.6 | **Subagent:** anthropic/claude-sonnet-4.6

## Input
**Prompt:** "Dataset: bib_journalist_dietitian-neg_neg_2 | Probe: unbiased | Method: correct"
**System prompt:** ""
**Concern:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."
**Top predictions:**  (100.0%)

## Oracle Analysis
## Analysis

**Analysis:** This probe classifies a profession (likely journalist/reporter), but the circuit reveals a critical mixture of genuine profession features (which push *against* the probe direction with negative effects) and spurious gender/lexical features (which push *toward* the probe direction with positive effects), confirming the user's concern about spurious feature reliance.

**Confidence:** High

**Reasoning:**

### Two Competing Pathways Drive the Probe

The circuit splits into two sharply distinct pathways with **opposite** effects on the probe's classification score:

---

**PATH 1 — Genuine Journalism Features (ALL NEGATIVE direct effects):**

A deep, multi-layer cascade of journalism-specific features forms the dominant pathway by activation strength, but all push **against** the probe direction:

- **Token origins:** The embeddings of `"report"` (pos 21) and `"news"` (pos 27) anchor the entire chain.
- **Early layers (L1-L3):** Lexical "report" detectors (L1:14511, L2:11175, L3:10846; all frac_nonzero ≤ 0.005) recognize the surface token.
- **Mid layers (L4-L6):** Features progressively build journalism context — L4:661 ("reports, documentaries, TV news"; frac=0.009), L4:13253 ("journalism and media"; frac=0.006), L6:8529 ("news/press reports"; frac=0.017, promotes "newspapers", "reporters", "journalists").
- **L7-L8:** Specialized journalism detectors — L7:13646 ("news reporting"; frac=0.008), L7:9092 ("broadcast journalism"; frac=0.009), L8:8855 ("news reporters"; frac=0.008, promotes "reporter", "journalist").
- **L14:4420** — "Journalism and newspapers" (frac=0.017) is the **single strongest driver** with direct_effect = **-0.1455** at pos 21. It fires at multiple positions (21, 22, 27) and promotes "journalists", "journalism", "reporter". This is the most impactful feature in the entire circuit.
- **L15:2579** — "Reporting in official capacity" (frac=0.005, direct_effect = -0.05)
- **L19:2486** — "Journalistic sources and news outlets" (frac=0.029) fires at 6+ positions with cumulative negative effect ~-0.42. Promotes "reporting", "reporter", "coverage".
- **L20:8433** — "News broadcasting" (frac=0.036, direct_effect = -0.0625).

All these features are **specific** (low frac_nonzero), **domain-relevant** (promoting journalism vocabulary), and form a coherent hierarchical cascade. Yet they all push the probe score **downward** (negative direct effects), suggesting the probe's positive direction classifies a profession *other than* journalist, and these journalism features correctly encode the content but work against whatever profession the probe is predicting.

---

**PATH 2 — Spurious/Generic Features (ALL POSITIVE direct effects):**

The features that actually push the probe *toward* its classification target are strikingly non-semantic:

- **L0:8964** — "The possessive pronoun 'His'" (frac=0.018, direct_effect = **+0.079**). Driven 93% by the raw token embedding of "His" at pos 1. This is a pure **gender marker** — it detects masculine possessive pronouns at the surface level with zero contextual reasoning.
- **L0:2011** — "The word 'dream'" (frac=0.008, direct_effect = +0.054). Fires spuriously on "desire" (pos 2) due to embedding similarity. This is a **semantic false positive** — "desire" activates a "dream" detector through shared embedding space, contributing a profession-irrelevant signal.
- **L0:13948** — "The color 'pink'" (frac=0.010, direct_effect = +0.053). Also fires at pos 2 ("desire") — clearly a **random embedding artifact** with no profession relevance.
- **L0:8444** — "The word 'to'" (frac=0.017, direct_effect = +0.076). A function word detector at pos 3.
- **L0:14287** — "The word 'see'" (frac=0.004, direct_effect = +0.064). A content word with no profession relevance.
- **L4:11898** — "'World' followed by sport/war" (frac=0.002, direct_effect = +0.054). Fires on "world" at pos 6.

These features are **all Layer 0** (or very early), encoding surface-level token identity with no semantic composition. None have any connection to a specific profession. Their promoted tokens are irrelevant to any career category.

---

### The Spurious Mechanism

The probe appears to be classifying a profession where:
1. The **genuine content** of the text (journalism/reporter language) fights **against** the probe's target class
2. The features that **support** the probe's classification are exclusively spurious: a masculine gender marker ("His"), function words ("to", "see"), and embedding-space false positives ("desire"→"dream", "desire"→"pink")

This is a textbook case of a **spuriously trained probe** that has learned correlations between gender markers/generic lexical patterns and profession labels in its training data. The positive probe signal comes from:
- **Gender bias**: masculine possessive "His" (the 4th strongest positive contributor) likely correlates with certain male-dominated professions in training data
- **Lexical noise**: function words and semantically confused L0 features that happen to correlate with specific biography patterns

### Verdict on User Concern

**The concern is validated.** The circuit demonstrates that the probe relies on a mixture of:
1. **Gender markers** (L0:8964 "His" — pure masculine pronoun detector, +0.079 direct effect)
2. **Spurious lexical features** (L0:2011 "dream"/desire, L0:13948 "pink"/desire, L0:8444 "to", L0:14287 "see" — collectively ~+0.25 direct effect)
3. **Genuine profession features** that are actually **fighting against** the probe's classification (journalism features with ~-0.6 cumulative negative direct effect)

The probe has not learned to use the genuine journalism content features to make its prediction — instead, it relies on shallow gender and lexical correlations while the actual profession-relevant features push in the opposite direction.

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L14:4420 de=-0.145 |
| 3 | `inspect_feature` ×14 | L14:4420, L19:2486, L0:8964, L0:8444, L0:14287, L20:8433, L0:2203, L4:11898, L5:771, L0:2011, L0:13948, L8:8855, L7:3085, L15:2579 |

### Dispatch: 7 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L14:F4420@21` | ✅ reported | 0 | 0 | Trace the strongest feature driving the probe: L14:4420 "journalism and newspape… |
| SA-2 | `L19:F2486@27` | ✅ reported | 13 | 23 | Trace L19:2486 "journalistic sources and news outlets" at pos 27 (likely "news")… |
| SA-3 | `L0:F8964@1` | ✅ reported | 6 | 7 | Trace L0:8964 "possessive pronoun His" at pos 1. This has a POSITIVE effect on t… |
| SA-4 | `L8:F8855@21` | ✅ reported | 0 | 0 | Trace L8:8855 "news reporters and reporting" at pos 21 (likely "report"). This i… |
| SA-5 | `L20:F8433@26` | ✅ reported | 13 | 21 | Trace L20:8433 "news broadcasting" at pos 26 (likely "news"). Find what feeds th… |
| SA-6 | `L0:F2011@2` | ✅ reported | 3 | 5 | Trace L0:2011 "the word dream" at pos 2 (which is "desire"). This has a positive… |
| SA-7 | `L15:F2579@21` | ✅ reported | 12 | 26 | Trace L15:2579 "people providing information in official capacity / reporting in… |

<details>
<summary><b>SA-1</b> — tool trace (20 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L14, F4420 | "words and phrases related to journalism and newspapers" |
| 2 | `get_upstream_features` | L14:F4420@21, k=8 | Emb:" report"@21 (w=5.22) +7 more |
| 3 | `inspect_feature` | L8, F8855 | " mentions of news reporters and news reporting" |
| 4 | `inspect_feature` | L7, F13646 | " news reporting and journalism." |
| 5 | `inspect_feature` | L8, F8437 | "content related to film festivals and production, particularly documen" |
| 6 | `inspect_feature` | L11, F5996 | " references to news publications and their staff." |
| 7 | `get_upstream_features` | L8:F8855@21, k=8 | Emb:" report"@21 (w=12.12) +7 more |
| 8 | `get_upstream_features` | L7:F13646@21, k=8 | Emb:" report"@21 (w=7.25) +7 more |
| 9 | `get_upstream_features` | L11:F5996@21, k=6 | Emb:"<bos>"@0 (w=-2.47) +5 more |
| 10 | `inspect_feature` | L7, F13896 | " words or phrases related to reports, people's names, and versions" |
| 11 | `inspect_feature` | L4, F661 | " words and phrases used when referring to reports, documentaries, and " |
| 12 | `inspect_feature` | L6, F12624 | "words related to art, architecture, or law." |
| 13 | `inspect_feature` | L5, F12586 | " mentions of reports" |
| 14 | `inspect_feature` | L4, F6696 | "the word "report" or "reporting" along with adjacent words" |
| 15 | `get_upstream_features` | L4:F661@21, k=6 | Emb:" report"@21 (w=14.38) +5 more |
| 16 | `get_upstream_features` | L5:F12586@21, k=6 | Emb:" report"@21 (w=32.25) +5 more |
| 17 | `inspect_feature` | L3, F10846 | "the word "report"" |
| 18 | `inspect_feature` | L2, F11175 | "the verb "report" and its variations" |
| 19 | `inspect_feature` | L1, F14511 | " the word "report"" |
| 20 | `inspect_feature` | L1, F9794 | "words and phrases associated with the film industry, including film pr" |

</details>

<details>
<summary><b>SA-2</b> — tool trace (17 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L19, F2486 | " journalistic sources and news outlets." |
| 2 | `get_upstream_features` | L19:F2486@27, k=8 | Emb:" news"@27 (w=20.75) +7 more |
| 3 | `inspect_feature` | L17, F4629 | " words having to do with current affairs reporting" |
| 4 | `inspect_feature` | L14, F4420 | "words and phrases related to journalism and newspapers" |
| 5 | `inspect_feature` | L7, F13646 | " news reporting and journalism." |
| 6 | `inspect_feature` | L8, F8855 | " mentions of news reporters and news reporting" |
| 7 | `get_upstream_features` | L17:F4629@27, k=6 | Emb:" news"@27 (w=42.50) +5 more |
| 8 | `get_upstream_features` | L14:F4420@27, k=6 | Emb:" news"@27 (w=15.00) +5 more |
| 9 | `inspect_feature` | L15, F12238 | " legal notifications" |
| 10 | `inspect_feature` | L14, F8761 | " words related to current events and publications" |
| 11 | `inspect_feature` | L7, F9092 | " words and phrases associated with broadcast journalism" |
| 12 | `inspect_feature` | L9, F7435 | " words and phrases related to news production and media" |
| 13 | `get_upstream_features` | L7:F13646@27, k=6 | Emb:" news"@27 (w=6.28) +5 more |
| 14 | `get_upstream_features` | L7:F9092@27, k=6 | Emb:" news"@27 (w=11.38) +5 more |
| 15 | `inspect_feature` | L3, F2616 | " the word 'news' and related phrases." |
| 16 | `inspect_feature` | L6, F8529 | " news or press reports in the media" |
| 17 | `inspect_feature` | L4, F13253 | " things related to journalism and the media" |

**Findings:** ## Circuit Tracing Summary: L19:F2486 "Journalistic Sources and News Outlets"

### Core Finding: The Token Embedding Drives Everything
The single most dominant signal feeding L19:F2486 is the **raw token embedding of " news"** at position 27. This embedding drives the circuit at every level:
- Direct to L19:F2486: weight **+20.75** (strongest single input)
- To L17:F4629 ("current affairs reportin…

</details>

<details>
<summary><b>SA-3</b> — tool trace (8 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F8964 | " the possessive pronoun "His"" |
| 2 | `get_upstream_features` | L0:F8964@1, k=5 | Emb:"His"@1 (w=13.69) +4 more |
| 3 | `inspect_feature` | L0, F253 | "the contraction "ve" and also finds other words like "scale", "screen"" |
| 4 | `inspect_feature` | L0, F310 | " the pronouns "she", "her", and "he" and sometimes the word "therefore" |
| 5 | `inspect_feature` | L0, F208 | "the words "happened" and "occur"" |
| 6 | `get_upstream_features` | L0:F8964@1, k=10 | Emb:"His"@1 (w=13.69) +9 more |
| 7 | `inspect_feature` | L0, F1148 | " mathematical symbols, variables, and related notation, with some func" |
| 8 | `inspect_feature` | L0, F1775 | " the word "yet" and words immediately adjacent to it" |

**Findings:** ## Circuit Summary: L0:F8964 "possessive pronoun His"

**Core Finding: This is a near-purely lexical gender signal driven almost entirely by the raw token embedding of "His".**

### Signal Decomposition:
1. **Token embedding "His" → L0:F8964** (edge weight: **13.69**, ~93% of total signal): The dominant driver is the raw token embedding of the word "His" itself at position 1. This is an extremely …

</details>

<details>
<summary><b>SA-4</b> — tool trace (18 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L8, F8855 | " mentions of news reporters and news reporting" |
| 2 | `get_upstream_features` | L8:F8855@21, k=8 | Emb:" report"@21 (w=12.12) +7 more |
| 3 | `inspect_feature` | L7, F13646 | " news reporting and journalism." |
| 4 | `inspect_feature` | L7, F13896 | " words or phrases related to reports, people's names, and versions" |
| 5 | `inspect_feature` | L3, F10846 | "the word "report"" |
| 6 | `inspect_feature` | L6, F12624 | "words related to art, architecture, or law." |
| 7 | `get_upstream_features` | L7:F13646@21, k=8 | Emb:" report"@21 (w=7.25) +7 more |
| 8 | `get_upstream_features` | L3:F10846@21, k=8 | Emb:" report"@21 (w=24.75) +7 more |
| 9 | `inspect_feature` | L4, F661 | " words and phrases used when referring to reports, documentaries, and " |
| 10 | `inspect_feature` | L2, F11175 | "the verb "report" and its variations" |
| 11 | `inspect_feature` | L0, F12801 | " verbs related to communication, help, enabling, and allowing" |
| 12 | `inspect_feature` | L6, F12712 | " titles of editors and publishers in scientific publications" |
| 13 | `get_upstream_features` | L4:F661@21, k=8 | Emb:" report"@21 (w=14.38) +7 more |
| 14 | `get_upstream_features` | L2:F11175@21, k=8 | Emb:" report"@21 (w=32.50) +7 more |
| 15 | `inspect_feature` | L1, F14511 | " the word "report"" |
| 16 | `inspect_feature` | L1, F8335 | "mentions of reports or reporting of information" |
| 17 | `inspect_feature` | L1, F9794 | "words and phrases associated with the film industry, including film pr" |
| 18 | `inspect_feature` | L1, F3604 | " verbs in scientific or technical writing, especially those describing" |

</details>

<details>
<summary><b>SA-5</b> — tool trace (18 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L20, F8433 | "words related to news broadcasting" |
| 2 | `get_upstream_features` | L20:F8433@26, k=8 | Emb:" top"@26 (w=5.69) +7 more |
| 3 | `inspect_feature` | L17, F5218 | " text about journalism, media, and related topics" |
| 4 | `inspect_feature` | L14, F4420 | "words and phrases related to journalism and newspapers" |
| 5 | `inspect_feature` | L19, F2486 | " journalistic sources and news outlets." |
| 6 | `inspect_feature` | L19, F14973 | " words related to high-achieving individuals and organizations" |
| 7 | `get_upstream_features` | L14:F4420@21, k=6 | Emb:" report"@21 (w=5.22) +5 more |
| 8 | `get_upstream_features` | L19:F2486@26, k=6 | L14:F4420 (w=6.25) +5 more |
| 9 | `get_upstream_features` | L17:F5218@26, k=6 | Emb:" report"@21 (w=2.09) +5 more |
| 10 | `inspect_feature` | L8, F8855 | " mentions of news reporters and news reporting" |
| 11 | `inspect_feature` | L7, F13646 | " news reporting and journalism." |
| 12 | `inspect_feature` | L16, F15046 | " names, organizations, and reporting verbs" |
| 13 | `inspect_feature` | L7, F9092 | " words and phrases associated with broadcast journalism" |
| 14 | `get_upstream_features` | L8:F8855@21, k=6 | Emb:" report"@21 (w=12.12) +5 more |
| 15 | `get_upstream_features` | L7:F9092@26, k=6 | Emb:" top"@26 (w=-1.08) +5 more |
| 16 | `inspect_feature` | L7, F13896 | " words or phrases related to reports, people's names, and versions" |
| 17 | `inspect_feature` | L3, F10846 | "the word "report"" |
| 18 | `inspect_feature` | L6, F12712 | " titles of editors and publishers in scientific publications" |

**Findings:** ## Circuit Summary: L20:F8433 "News Broadcasting" — Genuine Content Detection via Lexical Cascade

**Answer: This is GENUINE content detection**, driven bottom-up from real input tokens, not superficial pattern-matching.

### The Core Signal Chain

The circuit is anchored at **pos 21** by the raw embedding of `" report"`, which acts as the primary lexical trigger cascading through a journalism-spe…

</details>

<details>
<summary><b>SA-6</b> — tool trace (8 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F2011 | " the word "dream"" |
| 2 | `get_upstream_features` | L0:F2011@2, k=5 | Emb:" desire"@2 (w=12.94) +4 more |
| 3 | `inspect_feature` | L0, F253 | "the contraction "ve" and also finds other words like "scale", "screen"" |
| 4 | `inspect_feature` | L0, F310 | " the pronouns "she", "her", and "he" and sometimes the word "therefore" |
| 5 | `get_top_logits` | k=5 | "" (100%) |
| 6 | `get_top_features` | token=" desire", k=10 | ❌ Token ' desire' not found in top logits. Available: [''] |
| 7 | `get_top_features` | token="", k=10 | 10 features; top: L14:4420 de=-0.145 |
| 8 | `inspect_feature` | L0, F2011 | " the word "dream"" |

**Findings:** ## Circuit Analysis: L0:F2011 "the word dream" at pos 2 (" desire")

### What L0:F2011 Detects
- **Label**: "the word 'dream'" — a highly specific lexical feature that fires on the token ` dream`
- **frac_nonzero = 0.00779** — very sparse and selective, fires only in ~0.8% of contexts
- Its top activating examples all confirm it fires on ` dream` tokens across diverse, unrelated topics (politics, …

</details>

<details>
<summary><b>SA-7</b> — tool trace (17 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L15, F2579 | "instances of people providing information in some sort of official cap" |
| 2 | `get_upstream_features` | L15:F2579@21, k=8 | Emb:" report"@21 (w=38.25) +7 more |
| 3 | `inspect_feature` | L5, F12586 | " mentions of reports" |
| 4 | `inspect_feature` | L5, F13392 | " official documentation, official bodies and reporting on findings" |
| 5 | `inspect_feature` | L3, F10846 | "the word "report"" |
| 6 | `inspect_feature` | L8, F8855 | " mentions of news reporters and news reporting" |
| 7 | `get_upstream_features` | L5:F12586@21, k=6 | Emb:" report"@21 (w=32.25) +5 more |
| 8 | `get_upstream_features` | L8:F8855@21, k=6 | Emb:" report"@21 (w=12.12) +5 more |
| 9 | `get_upstream_features` | L5:F13392@21, k=6 | Emb:" report"@21 (w=19.75) +5 more |
| 10 | `inspect_feature` | L7, F13646 | " news reporting and journalism." |
| 11 | `inspect_feature` | L4, F6696 | "the word "report" or "reporting" along with adjacent words" |
| 12 | `inspect_feature` | L2, F11175 | "the verb "report" and its variations" |
| 13 | `inspect_feature` | L1, F14511 | " the word "report"" |
| 14 | `get_upstream_features` | L7:F13646@21, k=6 | Emb:" report"@21 (w=7.25) +5 more |
| 15 | `inspect_feature` | L4, F9660 | "mentions the collection of data by observers or detectors." |
| 16 | `inspect_feature` | L4, F661 | " words and phrases used when referring to reports, documentaries, and " |
| 17 | `inspect_feature` | L6, F12712 | " titles of editors and publishers in scientific publications" |

**Findings:** ## Key Finding: L15:F2579 is a Purely Token-Form-Driven Pattern, Not Genuine Professional Knowledge

### Root Cause: The " report" Embedding Is Overwhelmingly Dominant
The entire circuit collapses to a single raw token embedding: the word **" report"** at position 21, which drives every layer in the chain with weights of 38.25 → 32.25 → 19.75 → 12.125 → 7.25 — all vastly larger than any feature-to…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` ×3 | L19:14973, L16:15046, L3:10846 |

### Build

`build_circuit` → 17 nodes, 27 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | anthropic/claude-opus-4.6 | 138,775 | 6,835 | 0 | 0 | $0.8648 | — | — |
| SA-6 | anthropic/claude-sonnet-4.6 | 34,571 | 2,314 | 0 | 0 | $0.1384 | ✅ 3F/5E | Trace L0:2011 "the word dream" at pos 2 (which is "desire").… |
| SA-3 | anthropic/claude-sonnet-4.6 | 30,755 | 2,616 | 0 | 0 | $0.1315 | ✅ 6F/7E | Trace L0:8964 "possessive pronoun His" at pos 1. This has a … |
| SA-1 | anthropic/claude-sonnet-4.6 | 70,311 | 5,900 | 0 | 0 | $0.2994 | ✅ 0F/0E | Trace the strongest feature driving the probe: L14:4420 "jou… |
| SA-4 | anthropic/claude-sonnet-4.6 | 65,531 | 5,687 | 0 | 0 | $0.2819 | ✅ 0F/0E | Trace L8:8855 "news reporters and reporting" at pos 21 (like… |
| SA-2 | anthropic/claude-sonnet-4.6 | 65,302 | 5,342 | 0 | 0 | $0.2760 | ✅ 13F/23E | Trace L19:2486 "journalistic sources and news outlets" at po… |
| SA-5 | anthropic/claude-sonnet-4.6 | 66,544 | 5,592 | 0 | 0 | $0.2835 | ✅ 13F/21E | Trace L20:8433 "news broadcasting" at pos 26 (likely "news")… |
| SA-7 | anthropic/claude-sonnet-4.6 | 65,519 | 4,973 | 0 | 0 | $0.2712 | ✅ 12F/26E | Trace L15:2579 "people providing information in official cap… |
| **Total** | | **537,308** | **39,259** | **0** | **0** | **$2.5467** | | |

**Oracle wall-clock time:** 5m 25s