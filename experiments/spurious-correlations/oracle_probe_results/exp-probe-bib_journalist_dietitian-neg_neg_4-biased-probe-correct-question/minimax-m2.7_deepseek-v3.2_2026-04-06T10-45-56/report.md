# Circuit Oracle Report
**Date:** 2026-04-06 10:45:56 UTC | **Orchestrator:** minimax/minimax-m2.7 | **Subagent:** deepseek/deepseek-v3.2

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-neg_neg_4 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "('The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession.',)"

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification is driven primarily by **gender markers** (male pronoun "He" detection at L18:F14743, direct_effect=-0.1152) and **generic stopwords** (word "at" at L0:F7124, direct_effect=-0.1602; word "the" at L0:F3820, direct_effect=-0.103), with a minor positive contribution from **academic/professional context markers** ("Starting" at L1:F15323, direct_effect=+0.1128). The text describes a freelance defence journalist/writer, yet no features encode genuine profession indicators like "writer", "journalist", or "freelance" — instead, the circuit relies entirely on spurious signals: the male pronoun "he" at positions 22 and 39, and stopword patterns at positions 2 and 3.

**Confidence:** 9/10

**Reasoning:** The circuit traced from the probe output (L36:output) reveals three supernodes feeding the classification:

1. **"Male Pronoun Detection ('He')"** (L17:F5889 → L18:F14743 at pos 22 & 39): A pronoun detection cascade (L0:F12768 → L4:F15567 → L13:F1937 → L14:F14097 → L17:F5889 → L18:F14743) with the strongest direct effect (-0.1152). All features specifically detect "he/He" pronouns (frac_nonzero=0.018-0.019), not profession identity. The circuit traces to the token embedding " he" at pos 22 (edge weight 28.5 directly from embedding).

2. **"Stopword Detection ('at', 'the')"** (L0:F7124, L0:F3820): These generic word-detectors (frac_nonzero=0.009-0.030) fire on stopwords with no semantic content. L0:F7124 directly reads the " at" token (weight 31.375) and L0:F3820 reads " the" (weight 34.0).

3. **"Academic/Professional Context"** (L1:F15323): The only feature with positive contribution (+0.1128) detects "Starting" in academic papers, but this is a context marker rather than a profession indicator.

The circuit shows no features encoding "writer", "journalist", "freelance", or any genuine profession-specific knowledge. The dependence on "He" pronouns (two instances at positions 22 and 39) strongly suggests the probe uses gender as a proxy — if the text used "She" pronouns for a female journalist, the classification would change arbitrarily. This confirms the user's concern about spurious gender markers rather than genuine profession indicators.

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 10 features; top: L0:7124 de=-0.160 |

### Dispatch: 7 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L0:F7124@2` | ✅ reported | 1 | 3 | Trace this feature's semantics and upstream sources. What does L0:7124 encode? |
| SA-2 | `L18:F14743@22` | ✅ reported | 7 | 15 | Trace this feature's semantics and upstream sources. What does L18:14743 encode? |
| SA-3 | `L1:F15323@1` | ✅ reported | 4 | 12 | Trace this feature's semantics and upstream sources. What does L1:15323 encode? |
| SA-4 | `L0:F15661@7` | ✅ reported | 1 | 3 | Trace this feature's semantics and upstream sources. What does L0:15661 encode? |
| SA-5 | `L0:F3820@3` | ✅ reported | 2 | 6 | Trace this feature's semantics and upstream sources. What does L0:3820 encode? |
| SA-6 | `L14:F14097@22` | ✅ reported | 5 | 13 | Trace this feature's semantics and upstream sources. What does L14:14097 encode? |
| SA-7 | `L1:F4459@7` | ✅ reported | 4 | 15 | Trace this feature's semantics and upstream sources. What does L1:4459 encode? |

<details>
<summary><b>SA-1</b> — tool trace (3 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F7124 | "the word "at"" |
| 2 | `get_upstream_features` | L0:F7124@2, k=5 | Emb:" at"@2 (w=31.38) +4 more |
| 3 | `get_top_logits` | k=5 | "" (100%) |

**Findings:** L0:7124 is a feature that detects the word \"at\". The feature label is \"the word 'at'\" and it fires on tokens containing \"at\" as shown in its top activating examples. The circuit traces directly back to token embeddings: the strongest connection is from the \" at\" token embedding at position 2 (edge weight 31.375), with weaker contextual influences from \"Starting\" at position 1 (edge weigh…

</details>

<details>
<summary><b>SA-2</b> — tool trace (13 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L18, F14743 | "He" |
| 2 | `get_upstream_features` | L18:F14743@22, k=5 | Emb:" he"@22 (w=28.50) +4 more |
| 3 | `inspect_feature` | L17, F5889 | " references to people with pronouns and possessive pronouns" |
| 4 | `inspect_feature` | L0, F12768 | " mentions of "he" and "she" in close proximity" |
| 5 | `get_upstream_features` | L17:F5889@22, k=5 | Emb:" he"@22 (w=37.50) +4 more |
| 6 | `inspect_feature` | L14, F14097 | " occurrences of the word "he"" |
| 7 | `get_upstream_features` | L0:F12768@22, k=5 | Emb:" he"@22 (w=40.25) +4 more |
| 8 | `get_upstream_features` | L14:F14097@22, k=5 | Emb:" he"@22 (w=2.70) +4 more |
| 9 | `inspect_feature` | L13, F1937 | " pronouns used to describe people, including possessive pronouns" |
| 10 | `get_upstream_features` | L13:F1937@22, k=5 | Emb:" he"@22 (w=8.94) +4 more |
| 11 | `inspect_feature` | L4, F15567 | "sentences with male or female pronouns and possessives, especially one" |
| 12 | `get_upstream_features` | L4:F15567@22, k=5 | Emb:" he"@22 (w=17.88) +4 more |
| 13 | `inspect_feature` | L3, F9548 | " uses of the word "this" followed by a pause or conjunction, sometimes" |

**Findings:** L18:F14743 encodes the word "He" - it's a pronoun detection feature that specifically fires on the token "He". The circuit shows it primarily receives direct input from the token embedding " he" at position 22 (weight 28.5), but also integrates information from multiple pronoun-related features across layers:

1. Direct token embedding: " he" at position 22 is the strongest source
2. L17:F5889: De…

</details>

<details>
<summary><b>SA-3</b> — tool trace (8 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L1, F15323 | "the word "starting" in academic papers" |
| 2 | `get_upstream_features` | L1:F15323@1, k=5 | Emb:"Starting"@1 (w=16.38) +4 more |
| 3 | `inspect_feature` | L0, F7344 | " content markers like figures and section headers" |
| 4 | `inspect_feature` | L0, F6421 | " words related to administrative processes and computer programs" |
| 5 | `inspect_feature` | L0, F6228 | " the word "toxicity" when discussing medicine" |
| 6 | `get_upstream_features` | L0:F7344@1, k=5 | Emb:"<bos>"@0 (w=11.19) +4 more |
| 7 | `get_upstream_features` | L0:F6421@1, k=5 | Emb:"<bos>"@0 (w=10.31) +4 more |
| 8 | `get_upstream_features` | L0:F6228@1, k=5 | Emb:"Starting"@1 (w=9.56) +4 more |

**Findings:** L1:F15323 encodes detection of the word "starting" in academic papers context. It has a complex circuit: The feature is primarily positively driven directly by the "Starting" token embedding (weight 16.375), but interestingly it SUPPRESSES actual "starting" tokens in its output (as seen in its suppressed_tokens list). The feature is significantly inhibited by three layer 0 features: L0:F7344 (cont…

</details>

<details>
<summary><b>SA-4</b> — tool trace (2 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F15661 | "the word "spin"" |
| 2 | `get_upstream_features` | L0:F15661@7, k=5 | Emb:" Institute"@7 (w=19.38) +4 more |

**Findings:** The feature L0:15661 at position 7 has the label \"the word 'spin'\" based on its training examples (firing on scientific contexts with nuclear spin, atomic physics). However, in the attribution graph for this specific prompt, it shows a very strong direct connection (weight 19.375) to the token embedding for \" Institute\" at position 7. This suggests the feature may be multi-modal or context-dep…

</details>

<details>
<summary><b>SA-5</b> — tool trace (6 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F3820 | "the word "the"" |
| 2 | `get_upstream_features` | L0:F3820@3, k=5 | Emb:" the"@3 (w=34.00) +4 more |
| 3 | `inspect_feature` | L0, F419 | "the word "fixed" or its variants in technical contexts." |
| 4 | `get_upstream_features` | L0:F3820@0, k=3 | ❌ Feature (layer=0, feature_idx=3820) not found at pos=0. This |
| 5 | `get_upstream_features` | L0:F3820@43, k=5 | Emb:" the"@43 (w=36.00) +4 more |
| 6 | `get_top_logits` | k=5 | "" (100%) |

**Findings:** L0:3820 encodes the word "the". It fires specifically on occurrences of the token " the" in the input. The circuit shows it receives strong positive connections (edge_weight 34.0 and 36.0) directly from the embeddings of " the" tokens at positions where it activates. Interestingly, it suppresses "the" as an output token while promoting rare/foreign-language variations like "Efq", "Theže", etc. The…

</details>

<details>
<summary><b>SA-6</b> — tool trace (9 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L14, F14097 | " occurrences of the word "he"" |
| 2 | `get_upstream_features` | L14:F14097@22, k=5 | Emb:" he"@22 (w=2.70) +4 more |
| 3 | `inspect_feature` | L13, F1937 | " pronouns used to describe people, including possessive pronouns" |
| 4 | `inspect_feature` | L0, F12768 | " mentions of "he" and "she" in close proximity" |
| 5 | `inspect_feature` | L4, F15567 | "sentences with male or female pronouns and possessives, especially one" |
| 6 | `get_upstream_features` | L13:F1937@22, k=5 | Emb:" he"@22 (w=8.94) +4 more |
| 7 | `get_upstream_features` | L0:F12768@22, k=5 | Emb:" he"@22 (w=40.25) +4 more |
| 8 | `get_upstream_features` | L4:F15567@22, k=5 | Emb:" he"@22 (w=17.88) +4 more |
| 9 | `inspect_feature` | L3, F9548 | " uses of the word "this" followed by a pause or conjunction, sometimes" |

**Findings:** I traced the circuit for L14:F14097 at position 22, which encodes "occurrences of the word 'he'". The tracing reveals:

1. The feature directly detects the word "he" with low sparsity (0.01967), meaning it's specific to this pronoun.

2. Key upstream sources:
   - Direct connection from the embedding of token " he" at position 22 (weight 2.7031)
   - Feature at L13:F1937 that detects pronouns more…

</details>

<details>
<summary><b>SA-7</b> — tool trace (7 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L1, F4459 | " mentions of research institutes" |
| 2 | `get_upstream_features` | L1:F4459@7, k=5 | Emb:" Institute"@7 (w=27.50) +4 more |
| 3 | `inspect_feature` | L0, F15661 | "the word "spin"" |
| 4 | `inspect_feature` | L0, F12879 | "the word "squad" and words related to team membership" |
| 5 | `inspect_feature` | L0, F8466 | " the word "volume."" |
| 6 | `get_upstream_features` | L0:F15661@7, k=5 | Emb:" Institute"@7 (w=19.38) +4 more |
| 7 | `get_upstream_features` | L0:F12879@7, k=5 | Emb:" Institute"@7 (w=15.50) +4 more |

**Findings:** The circuit tracing reveals that L1:4459 encodes "mentions of research institutes" and is primarily driven directly by the token embedding for "Institute" at position 7 (weight: 27.5). This direct connection suggests the feature is closely tied to the word "Institute" itself. 

Interestingly, despite the strong direct embedding connection, there are also weaker connections from three layer 0 featu…

</details>

### Build

`build_circuit` → 10 nodes, 10 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m2.7 | 16,859 | 3,727 | 44,322 | 0 | $0.0109 | — | — |
| SA-1 | deepseek/deepseek-v3.2 | 12,956 | 1,185 | 0 | 0 | $0.0038 | ✅ 1F/3E | Trace this feature's semantics and upstream sources. What do… |
| SA-4 | deepseek/deepseek-v3.2 | 8,900 | 1,350 | 0 | 0 | $0.0028 | ✅ 1F/3E | Trace this feature's semantics and upstream sources. What do… |
| SA-3 | deepseek/deepseek-v3.2 | 43,611 | 2,541 | 0 | 0 | $0.0123 | ✅ 4F/12E | Trace this feature's semantics and upstream sources. What do… |
| SA-2 | deepseek/deepseek-v3.2 | 81,025 | 4,008 | 13,120 | 0 | $0.0229 | ✅ 7F/15E | Trace this feature's semantics and upstream sources. What do… |
| SA-5 | deepseek/deepseek-v3.2 | 28,716 | 1,764 | 0 | 0 | $0.0081 | ✅ 2F/6E | Trace this feature's semantics and upstream sources. What do… |
| SA-6 | deepseek/deepseek-v3.2 | 51,643 | 3,253 | 3,648 | 0 | $0.0148 | ✅ 5F/13E | Trace this feature's semantics and upstream sources. What do… |
| SA-7 | deepseek/deepseek-v3.2 | 37,391 | 2,590 | 0 | 0 | $0.0107 | ✅ 4F/15E | Trace this feature's semantics and upstream sources. What do… |
| **Total** | | **281,101** | **20,418** | **61,090** | **0** | **$0.0863** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 7m 38s