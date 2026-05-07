# Circuit Oracle Report
**Date:** 2026-04-06 17:08:55 UTC | **Orchestrator:** minimax/minimax-m2.7 | **Subagent:** deepseek/deepseek-v3.2

## Input

**Prompt:** "Dataset: multinli-pos_pos_5 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "('The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction.',)"

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score is primarily driven by grammatical/surface-level features—specifically the "not only...but also" correlative conjunction pattern (L2:F5627, L4:F11560), negation patterns "not" (L0:F4958, L16:F15025) and "isn't" (L0:F6236, L16:F12358), and contrastive conjunction "but" (L4:F2884, L15:F12905)—rather than deep semantic analysis of the actual propositional content. The circuit uses these generic linguistic markers that signal contrast/negation rather than encoding the specific semantic relationship between the two statements about lawyers' public image.

**Confidence:** 8/10

**Reasoning:**

The attribution circuit reveals a mechanism that relies heavily on **surface grammatical patterns** rather than semantic understanding:

1. **"Not only...but also" construction** (L2:F5627 at pos=7, frac_nonzero=0.00685): This is the highest-effect feature (direct_effect=0.498). It detects the correlative conjunction pattern "not only" from sentence 1, not the semantic relationship. This pattern is a generic grammatical signal of contrast.

2. **Negation features** dominate the circuit:
   - L0:F4958 ("not" at pos=6, frac_nonzero=0.0184)
   - L16:F15025 ("not" + pronouns, direct_effect=0.3223)
   - L0:F6236 (isn't pattern, direct_effect=0.4785)
   - L16:F12358 ("not" + "to be", direct_effect=0.3711)

3. **Contrastive conjunction "but"** (L15:F12905 at pos=13, direct_effect=-0.3203): This negatively contributes to the output, suggesting the model uses "but" as a generic contrast signal.

4. **Speech attribution "said"** (L4:F15629, direct_effect=0.6719): The highest-effect feature detects "said" (pos=3), likely as a signal that the first statement is quoted/attributed rather than evaluating semantic truth.

5. **Content suppression**: The "program" word (L0:F14950, direct_effect=-0.3516) and "said" suppression (L4:F12337) have negative effects, indicating the model downweights actual content words.

**The user's concern is validated**: The circuit primarily uses generic linguistic markers—"not," "but," "isn't," "not only"—rather than encoding the specific semantic contradiction ("lawyers' image will/won't improve"). These features have low frac_nonzero values (0.002-0.02), making them highly specific to surface patterns rather than semantic relationships. The model detects that *grammatical contrast/negation patterns exist* but doesn't appear to verify whether the actual propositions are contradictory.

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 10 features; top: L4:15629 de=0.672 |

### Dispatch: 7 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L4:F15629@3` | ✅ reported | 5 | 13 | Trace this high-effect feature (L4:F15629) upstream to understand what semantic … |
| SA-2 | `L4:F12337@3` | ✅ reported | 7 | 15 | Trace this negative-effect feature (L4:F12337) upstream to understand what it su… |
| SA-3 | `L2:F5627@7` | ✅ reported | 4 | 9 | Trace L2:F5627 upstream to understand its semantic content and trace to embeddin… |
| SA-4 | `L16:F12358@28` | ✅ reported | 7 | 20 | Trace L16:F12358 (late-layer feature at pos 28) upstream to understand semantic … |
| SA-5 | `L16:F15025@6` | ✅ reported | 5 | 25 | Trace L16:F15025 (pos=6) upstream to understand what semantic content it encodes… |
| SA-6 | `L15:F12905@13` | ✅ reported | 9 | 22 | Trace L15:F12905 (pos=13) upstream to understand what semantic content it encode… |
| SA-7 | `L0:F14950@5` | ✅ reported | 1 | 5 | Trace L0:F14950 (pos=5) upstream to understand what semantic content it encodes … |

<details>
<summary><b>SA-1</b> — tool trace (10 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F15629 | " speech attribution, such as the word "said" and phrases like "talking" |
| 2 | `get_upstream_features` | L4:F15629@3, k=5 | Emb:" said"@3 (w=34.25) +4 more |
| 3 | `inspect_feature` | L3, F2091 | " mentions of the word "said"" |
| 4 | `inspect_feature` | L2, F13445 | " the word "said" and words that relate to the description of events" |
| 5 | `get_upstream_features` | L3:F2091@3, k=5 | Emb:" said"@3 (w=25.38) +4 more |
| 6 | `get_upstream_features` | L2:F13445@3, k=5 | Emb:" said"@3 (w=29.88) +4 more |
| 7 | `inspect_feature` | L1, F173 | "dialogue being spoken or narrated" |
| 8 | `get_upstream_features` | L1:F173@3, k=5 | Emb:" said"@3 (w=18.38) +4 more |
| 9 | `inspect_feature` | L0, F8525 | " the word "said"" |
| 10 | `get_upstream_features` | L0:F8525@3, k=5 | Emb:" said"@3 (w=18.62) +4 more |

**Findings:** I traced L4:F15629 (speech attribution feature) upstream through 4 layers to the embedding layer. The circuit is remarkably direct and consistent: every feature in the path detects the word "said" at position 3. Starting from L4:F15629 which encodes "speech attribution", the strongest connection (edge_weight=34.25) is directly to the embedding token " said" at position 3. The upstream features at …

</details>

<details>
<summary><b>SA-2</b> — tool trace (12 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F12337 | " speech attribution, especially "said"" |
| 2 | `get_upstream_features` | L4:F12337@3, k=5 | Emb:" said"@3 (w=28.00) +4 more |
| 3 | `inspect_feature` | L3, F2091 | " mentions of the word "said"" |
| 4 | `inspect_feature` | L2, F13445 | " the word "said" and words that relate to the description of events" |
| 5 | `inspect_feature` | L0, F15525 | " places where something is being explained or reported" |
| 6 | `get_upstream_features` | L3:F2091@3, k=5 | Emb:" said"@3 (w=25.38) +4 more |
| 7 | `get_upstream_features` | L2:F13445@3, k=5 | Emb:" said"@3 (w=29.88) +4 more |
| 8 | `inspect_feature` | L1, F173 | "dialogue being spoken or narrated" |
| 9 | `inspect_feature` | L1, F14137 | " words or phrases that appear in legal or technical documents, like na" |
| 10 | `inspect_feature` | L0, F8525 | " the word "said"" |
| 11 | `get_upstream_features` | L0:F15525@3, k=5 | Emb:" said"@3 (w=20.25) +4 more |
| 12 | `get_upstream_features` | L0:F8525@3, k=5 | Emb:" said"@3 (w=18.62) +4 more |

**Findings:** I traced the negative-effect feature L4:F12337 (speech attribution/suppression of "said") upstream to its sources. The circuit shows a fascinating pattern:

1. **Direct Input**: The strongest connection (weight=28.0) is directly from the token embedding " said" at position 3 feeding into L4:F12337.

2. **Negative Feedback Loop**: Multiple earlier features that detect "said" (L3:F2091, L2:F13445, L…

</details>

<details>
<summary><b>SA-3</b> — tool trace (7 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L2, F5627 | " instances of the phrase "not only"" |
| 2 | `get_upstream_features` | L2:F5627@7, k=5 | Emb:" only"@7 (w=21.38) +4 more |
| 3 | `inspect_feature` | L0, F12483 | "the word "only"" |
| 4 | `inspect_feature` | L0, F4723 | " the word "only"" |
| 5 | `inspect_feature` | L0, F1910 | " the phrase "not only"" |
| 6 | `get_upstream_features` | L0:F1910@7, k=5 | Emb:" not"@6 (w=15.62) +4 more |
| 7 | `get_upstream_features` | L0:F12483@7, k=5 | Emb:" not"@6 (w=23.50) +4 more |

**Findings:** The tracing reveals that L2:F5627 detects "instances of the phrase 'not only'" and is directly connected to the embedding layer tokens " only" at position 7 (weight=21.375) and " not" at position 6 (weight=19.0). This makes perfect sense as the feature detects the two-word phrase. Additionally, it receives inputs from three layer 0 features: L0:F12483 (detects "the word 'only'", weight=4.9375), L0…

</details>

<details>
<summary><b>SA-4</b> — tool trace (13 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L16, F12358 | " the word "not" followed within a few tokens by a form of the verb "to" |
| 2 | `get_upstream_features` | L16:F12358@28, k=5 | Emb:"t"@28 (w=12.75) +4 more |
| 3 | `inspect_feature` | L0, F6236 | "the letter "t" when it follows the word "isn'" or "doesn'"" |
| 4 | `inspect_feature` | L15, F10071 | "negations and equivocations" |
| 5 | `get_upstream_features` | L0:F6236@28, k=5 | Emb:" isn"@26 (w=23.25) +4 more |
| 6 | `get_upstream_features` | L15:F10071@28, k=5 | L0:F6236 (w=5.16) +4 more |
| 7 | `inspect_feature` | L14, F13077 | "negations." |
| 8 | `get_upstream_features` | L14:F13077@28, k=5 | L0:F6236 (w=7.28) +4 more |
| 9 | `inspect_feature` | L13, F3295 | "negations in the form of "is/are not" as well as other uses of "not"" |
| 10 | `get_upstream_features` | L13:F3295@28, k=5 | L0:F6236 (w=6.69) +4 more |
| 11 | `inspect_feature` | L2, F7654 | " the letter 't', but with some preference for words related to negativ" |
| 12 | `get_upstream_features` | L2:F7654@28, k=5 | Emb:" isn"@26 (w=10.31) +4 more |
| 13 | `inspect_feature` | L1, F423 | " words that negate a following word or phrase." |

**Findings:** Tracing L16:F12358 (detects "the word 'not' followed within a few tokens by a form of the verb 'to be'") reveals a negation detection circuit that originates from the specific token pattern "isn't" at positions 26-28. The circuit shows:

1. The core pattern detection happens at L0:F6236, which detects "the letter 't' when it follows the word 'isn' or 'doesn'" - this feature has very low frac_nonze…

</details>

<details>
<summary><b>SA-5</b> — tool trace (10 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L16, F15025 | " usage of the word "not" combined with personal pronouns or related em" |
| 2 | `get_upstream_features` | L16:F15025@6, k=5 | Emb:" not"@6 (w=12.19) +4 more |
| 3 | `inspect_feature` | L13, F4368 | " the word "not"" |
| 4 | `inspect_feature` | L0, F4958 | " the word "not"" |
| 5 | `inspect_feature` | L14, F2476 | "negative polarity, sometimes in the context of politics or social issu" |
| 6 | `get_upstream_features` | L13:F4368@6, k=5 | Emb:" not"@6 (w=15.19) +4 more |
| 7 | `get_upstream_features` | L0:F4958@6, k=5 | Emb:" not"@6 (w=32.00) +4 more |
| 8 | `get_upstream_features` | L14:F2476@6, k=5 | Emb:" not"@6 (w=14.25) +4 more |
| 9 | `inspect_feature` | L2, F2713 | " the word "not"" |
| 10 | `get_upstream_features` | L2:F2713@6, k=5 | Emb:" not"@6 (w=20.75) +4 more |

**Findings:** I successfully traced L16:F15025 at position 6 upstream to understand what semantic content it encodes. The key findings are:

1. L16:F15025 is a feature that detects "usage of the word 'not' combined with personal pronouns or related emotional or motivational language" (frac_nonzero = 0.02843).

2. The circuit has several clear paths back to the embedding layer:
   - The strongest direct connecti…

</details>

<details>
<summary><b>SA-6</b> — tool trace (14 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L15, F12905 | " the word "but" along with surrounding words that indicate a contrasti" |
| 2 | `get_upstream_features` | L15:F12905@13, k=5 | Emb:" only"@7 (w=5.94) +4 more |
| 3 | `inspect_feature` | L2, F5627 | " instances of the phrase "not only"" |
| 4 | `inspect_feature` | L9, F12274 | " the phrase "not only"" |
| 5 | `inspect_feature` | L4, F2884 | "the word "but" and other contrastive conjunctions and adverbs." |
| 6 | `get_upstream_features` | L2:F5627@7, k=5 | Emb:" only"@7 (w=21.38) +4 more |
| 7 | `get_upstream_features` | L4:F2884@13, k=5 | Emb:" but"@13 (w=17.75) +4 more |
| 8 | `inspect_feature` | L0, F12483 | "the word "only"" |
| 9 | `inspect_feature` | L0, F1910 | " the phrase "not only"" |
| 10 | `get_upstream_features` | L9:F12274@7, k=5 | L6:F3655 (w=9.19) +4 more |
| 11 | `inspect_feature` | L6, F3655 | " the word "just" and surrounding words" |
| 12 | `get_upstream_features` | L6:F3655@7, k=5 | Emb:" only"@7 (w=8.94) +4 more |
| 13 | `inspect_feature` | L4, F11560 | "the phrase "not only"" |
| 14 | `inspect_feature` | L2, F3379 | " the word "but" and similar terms" |

**Findings:** The circuit traces a linguistic pattern detection pathway for the phrase "not only... but also" construction. Starting from L15:F12905 which detects contrastive/consequential relationships featuring the word "but", the circuit reveals:

Key findings:
1. The main pathway originates from two key input tokens: " only" at position 7 (weight 5.94) and " but" at position 13 (weight 4.03)
2. The "not onl…

</details>

<details>
<summary><b>SA-7</b> — tool trace (3 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F14950 | " instances of the word "program" and the word "step"" |
| 2 | `get_upstream_features` | L0:F14950@5, k=5 | Emb:" program"@5 (w=23.25) +4 more |
| 3 | `get_upstream_features` | L0:F14950@5, k=10 | Emb:" program"@5 (w=23.25) +9 more |

**Findings:** Tracing L0:F14950 (pos=5) upstream reveals it directly connects to embedding layer nodes. The feature encodes semantic content about the word "program" and "step" (label: "instances of the word \"program\" and the word \"step\""), and is primarily fed by the embedding of token " program" at position 5 with a strong weight of 23.25. Smaller connections exist to other contextual tokens: <bos> (pos 0…

</details>

### Build

`build_circuit` → 17 nodes, 21 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m2.7 | 25,656 | 4,026 | 35,372 | 0 | $0.0136 | — | — |
| SA-3 | deepseek/deepseek-v3.2 | 37,645 | 2,078 | 0 | 0 | $0.0106 | ✅ 4F/9E | Trace L2:F5627 upstream to understand its semantic content a… |
| SA-1 | deepseek/deepseek-v3.2 | 55,068 | 2,765 | 5,248 | 0 | $0.0155 | ✅ 5F/13E | Trace this high-effect feature (L4:F15629) upstream to under… |
| SA-2 | deepseek/deepseek-v3.2 | 76,874 | 3,265 | 5,248 | 0 | $0.0214 | ✅ 7F/15E | Trace this negative-effect feature (L4:F12337) upstream to u… |
| SA-4 | deepseek/deepseek-v3.2 | 92,318 | 4,259 | 0 | 0 | $0.0256 | ✅ 7F/20E | Trace L16:F12358 (late-layer feature at pos 28) upstream to … |
| SA-7 | deepseek/deepseek-v3.2 | 13,182 | 1,230 | 0 | 0 | $0.0039 | ✅ 1F/5E | Trace L0:F14950 (pos=5) upstream to understand what semantic… |
| SA-5 | deepseek/deepseek-v3.2 | 51,197 | 3,925 | 9,664 | 0 | $0.0151 | ✅ 5F/25E | Trace L16:F15025 (pos=6) upstream to understand what semanti… |
| SA-6 | deepseek/deepseek-v3.2 | 100,615 | 4,499 | 4,416 | 0 | $0.0280 | ✅ 9F/22E | Trace L15:F12905 (pos=13) upstream to understand what semant… |
| **Total** | | **452,555** | **26,047** | **59,948** | **0** | **$0.1336** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 7m 1s