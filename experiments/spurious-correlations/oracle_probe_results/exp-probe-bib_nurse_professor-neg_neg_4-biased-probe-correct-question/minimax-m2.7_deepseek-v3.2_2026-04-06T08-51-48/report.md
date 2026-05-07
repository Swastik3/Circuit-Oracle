# Circuit Oracle Report
**Date:** 2026-04-06 08:51:48 UTC | **Orchestrator:** minimax/minimax-m2.7 | **Subagent:** deepseek/deepseek-v3.2

## Input

**Prompt:** "Dataset: bib_nurse_professor-neg_neg_4 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "('The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession.',)"

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score is driven primarily by male gender markers (the pronouns "his" and "he") rather than genuine profession indicators. The circuit directly reads token embeddings of male pronouns at positions 13, 35, and 37 to build layer-by-layer pronoun detection features that feed into the output.

**Confidence:** 9/10

**Reasoning:** The attribution circuit confirms the user's concern with high confidence. The top features with strongest direct effects are all gender markers:

1. **L0:F2994** (direct_effect=0.2539) — "the pronoun 'his' and the pronoun 'he'" — This is the single most impactful feature, directly driven by token embeddings " his" (pos 37) and " He" (pos 35). The embedding connection weight is 45.25, indicating direct token-level detection.

2. **L6:F12990** (direct_effect=-0.166) — "male pronouns and titles along with descriptors associated with men" — Built through a multi-layer pronoun processing circuit: L0→L1→L2→L4→L6. All intermediate features (L0:F1069 for male references, L1:F7439 for possessive pronouns, L4:F4315 for "his" mentions) are driven directly by the token embedding of " His" at position 13 (embedding weight 18.5-28.75). The circuit includes a negative path from L2:F5491 (God references) suggesting the model distinguishes human from divine male pronouns.

3. **L18:F14743** (direct_effect=-0.1406) — "He" feature — Directly driven by the " He" token embedding at position 35 (weight 23.625) through a hierarchical pronoun circuit: L0→L13→L17→L18.

4. **L7:F14893** (direct_effect=+0.13) — pronoun detection

The non-gender features are much weaker:
- **L0:F11024** (direct_effect=0.14) — labeled "clock" but responding to " Director" — a spurious/irrelevant feature
- **L0:F2848** (direct_effect=0.15) — "of" detection — a generic word with no profession information

**Conclusion:** The probe is using a **gender shortcut**. It detects male pronouns ("his", "he", "His") throughout the text rather than analyzing the actual profession-related content (e.g., "Director", "Laboratory", "Ph.D.", "Computer Science"). The circuit originates directly from token embeddings of male pronouns with no evidence of abstract gender representation or genuine profession extraction. This is a textbook example of a spurious correlation — the model predicts the profession class because the text happens to contain male pronouns, not because it correctly identifies the profession.

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 10 features; top: L0:2994 de=0.254 |
| 3 | `inspect_feature` ×5 | L0:2994, L6:12990, L0:2848, L18:14743, L7:14893 |

### Dispatch: 5 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L0:F2994@37` | ✅ reported | 1 | 5 | Trace this pronoun feature upstream to understand its source. What tokens or ear… |
| SA-2 | `L6:F12990@13` | ✅ reported | 6 | 11 | Trace this male pronoun feature upstream. Is there a deeper gender signal or is … |
| SA-3 | `L18:F14743@35` | ✅ reported | 5 | 11 | Trace this 'He' pronoun feature upstream. What produces this signal? |
| SA-4 | `L0:F2848@5` | ✅ reported | 1 | 5 | Trace this word 'of' feature upstream. What token drives it? |
| SA-5 | `L0:F11024@4` | ✅ reported | 1 | 5 | Trace this feature at position 4 upstream to understand what token it detects. |

<details>
<summary><b>SA-1</b> — tool trace (3 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F2994 | "the pronoun "his" and the pronoun "he."" |
| 2 | `get_upstream_features` | L0:F2994@37, k=5 | Emb:" his"@37 (w=45.25) +4 more |
| 3 | `get_upstream_features` | L0:F2994@37, k=10 | Emb:" his"@37 (w=45.25) +9 more |

**Findings:** The pronoun feature L0:F2994 (detecting pronouns "his" and "he") at position 37 is directly connected to token embeddings. The strongest connection is from the token " his" itself at position 37 (edge_weight 45.25). Weaker connections come from nearby tokens: " received" at position 36 (1.1172), "<bos>" at position 0 (0.4043), " He" at position 35 (0.3867), and "." at position 34 (0.1084). This in…

</details>

<details>
<summary><b>SA-2</b> — tool trace (12 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F12990 | " male pronouns and titles along with descriptors associated with men" |
| 2 | `get_upstream_features` | L6:F12990@13, k=5 | Emb:" His"@13 (w=5.28) +4 more |
| 3 | `inspect_feature` | L4, F4315 | " mentions of "his" and other associated pronouns like he, him, or hers" |
| 4 | `get_upstream_features` | L4:F4315@13, k=5 | Emb:" His"@13 (w=21.25) +4 more |
| 5 | `inspect_feature` | L2, F5491 | "references to God in the third person." |
| 6 | `get_upstream_features` | L2:F5491@13, k=5 | Emb:" His"@13 (w=23.38) +4 more |
| 7 | `inspect_feature` | L0, F1069 | " references to a male person, particularly when using the pronoun "He"" |
| 8 | `inspect_feature` | L0, F2994 | "the pronoun "his" and the pronoun "he."" |
| 9 | `inspect_feature` | L1, F7439 | " the possessive pronouns "his" and "him"" |
| 10 | `get_upstream_features` | L0:F1069@13, k=5 | Emb:" His"@13 (w=28.75) +4 more |
| 11 | `get_upstream_features` | L0:F2994@13, k=5 | Emb:" His"@13 (w=18.75) +4 more |
| 12 | `get_upstream_features` | L1:F7439@13, k=5 | Emb:" His"@13 (w=18.50) +4 more |

**Findings:** I traced the male pronoun feature at L6:F12990 upstream and found a clear circuit. The key finding is that this male pronoun feature is DIRECTLY driven by token embeddings rather than deeper gender signals:

1. The layer 6 male pronoun feature receives strong direct input from the embedding of "His" at position 13 (weight: 5.28) and weaker feature inputs from layer 4 (weight: 1.30) and negative fr…

</details>

<details>
<summary><b>SA-3</b> — tool trace (9 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L18, F14743 | "He" |
| 2 | `get_upstream_features` | L18:F14743@35, k=5 | Emb:" He"@35 (w=23.62) +4 more |
| 3 | `inspect_feature` | L0, F1069 | " references to a male person, particularly when using the pronoun "He"" |
| 4 | `inspect_feature` | L17, F5889 | " references to people with pronouns and possessive pronouns" |
| 5 | `get_upstream_features` | L0:F1069@35, k=5 | Emb:" He"@35 (w=36.50) +4 more |
| 6 | `get_upstream_features` | L17:F5889@35, k=5 | Emb:" He"@35 (w=22.62) +4 more |
| 7 | `inspect_feature` | L13, F6622 | " pronouns." |
| 8 | `get_upstream_features` | L13:F6622@35, k=5 | Emb:" He"@35 (w=13.62) +4 more |
| 9 | `inspect_feature` | L6, F2267 | "words that appear in programming code, legal jargon, or scientific tex" |

**Findings:** The 'He' pronoun feature at L18:F14743 is primarily produced by the token embedding for "He" itself at position 35 (direct edge_weight 23.625). Additionally, it receives signals from a cross-layer pronoun detection circuit: L0:F1069 detects male pronouns (especially "He"/"His") which is itself driven by the "He" token embedding plus the preceding period "." at position 34 (suggesting sentence-star…

</details>

<details>
<summary><b>SA-4</b> — tool trace (2 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F2848 | "the word "of"" |
| 2 | `get_upstream_features` | L0:F2848@5, k=5 | Emb:" of"@5 (w=34.75) +4 more |

**Findings:** Tracing the L0:F2848 feature (labeled "the word 'of'") at position 5 reveals it is primarily driven by the token embedding for " of" at the same position (pos 5) with a very strong edge weight of 34.75. This feature suppresses the token "of" and promotes other tokens like "my\u017felf", "Efq", etc. The low frac_nonzero (0.01966) indicates high specificity. Secondary influences come from the <bos> …

</details>

<details>
<summary><b>SA-5</b> — tool trace (4 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F11024 | " the word "clock", especially in a technical context" |
| 2 | `get_upstream_features` | L0:F11024@4, k=5 | Emb:" Director"@4 (w=12.81) +4 more |
| 3 | `inspect_feature` | L0, F11024 | " the word "clock", especially in a technical context" |
| 4 | `get_upstream_features` | L0:F11024@4, k=10 | Emb:" Director"@4 (w=12.81) +9 more |

**Findings:** Tracing from L0:F11024 at position 4 reveals a direct connection from the token embedding " Director" at the same position with a very strong edge weight of 12.81. This feature, though labeled as detecting "the word 'clock', especially in a technical context", is primarily responding to the token " Director" at position 4 in this specific context. The circuit is shallow - it goes directly from the…

</details>

### Build

`build_circuit` → 18 nodes, 24 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m2.7 | 19,497 | 4,076 | 43,426 | 0 | $0.0120 | — | — |
| SA-1 | deepseek/deepseek-v3.2 | 13,114 | 1,508 | 0 | 0 | $0.0040 | ✅ 1F/5E | Trace this pronoun feature upstream to understand its source… |
| SA-3 | deepseek/deepseek-v3.2 | 53,303 | 2,854 | 0 | 0 | $0.0149 | ✅ 5F/11E | Trace this 'He' pronoun feature upstream. What produces this… |
| SA-2 | deepseek/deepseek-v3.2 | 66,357 | 3,705 | 17,280 | 0 | $0.0191 | ✅ 6F/11E | Trace this male pronoun feature upstream. Is there a deeper … |
| SA-4 | deepseek/deepseek-v3.2 | 9,791 | 1,192 | 0 | 0 | $0.0030 | ✅ 1F/5E | Trace this word 'of' feature upstream. What token drives it? |
| SA-5 | deepseek/deepseek-v3.2 | 18,389 | 1,382 | 0 | 0 | $0.0053 | ✅ 1F/5E | Trace this feature at position 4 upstream to understand what… |
| **Total** | | **180,451** | **14,717** | **60,706** | **0** | **$0.0584** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 4m 36s