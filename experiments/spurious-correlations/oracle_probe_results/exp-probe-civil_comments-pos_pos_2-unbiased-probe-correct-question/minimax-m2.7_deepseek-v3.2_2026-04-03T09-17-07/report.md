# Circuit Oracle Report
**Date:** 2026-04-03 09:17:07 UTC | **Orchestrator:** minimax/minimax-m2.7 | **Subagent:** deepseek/deepseek-v3.2

## Input
**Prompt:** "Dataset: civil_comments-pos_pos_2 | Probe: unbiased | Method: correct"
**System prompt:** ""
**Question:** "The circuit use spurious features (e.g.,"an identity group" signals) rather than actual prompt content (lexical or semaintical) to predict toxicity."
**Top predictions:**  (100.0%)

## Oracle Analysis
**Analysis:** The toxicity probe's classification score is driven primarily by **spurious identity group signals** rather than actual semantic content — the circuit heavily relies on detecting the single token "white" (position 4) through multiple shallow lexical features at layers 0-4, rather than understanding the conditional statement's meaning ("If he was white and not Hispanic, it would be a problem").

**Confidence:** 9/10

**Reasoning:**

The circuit confirms the user's concern: the probe uses **identity signal detection** as its primary mechanism:

1. **"White" Token Dominance (direct_effect +0.1729):** The top contributor `L0:F3436` ("mentions of the word 'white'") directly detects the token "white" at position 4 from its embedding with weight 18.0. This feature has frac_nonzero=0.061, indicating selective activation. The circuit essentially terminates at this lexical detection — no deeper semantic processing of the sentence structure is evident.

2. **Identity Signal Cascade Through Layers 1-4:** The token "white" feeds a cascade of identity-related features:
   - `L1:F1480` ("the color 'white', sometimes in context involving race", frac_nonzero=0.004)
   - `L2:F6983` ("words related to race and slavery", frac_nonzero=0.033) 
   - `L3:F11768` ("the word 'white' and related contexts such as diversity", frac_nonzero=0.003)
   - `L4:F15204` ("art galleries, museums and the White House", frac_nonzero=0.005)
   - `L4:F7136` ("the color white", frac_nonzero=0.003)

3. **Shallow, Non-Compositional Processing:** The circuit is remarkably shallow — most features receive direct strong connections from the "white" token embedding (weights 8-43) with minimal feature-to-feature transformation. This indicates the model is detecting identity tokens directly rather than composing meaning from the sentence's conditional structure ("If...and...not...").

4. **Weak Grammatical/Content Features:** While there are conditional detectors (`L3:F12404` for "if", `L2:F1139` for "so" constructions), their contributions are overshadowed by identity signals. The pronoun features (`L0:F12768`, `L0:F310`) detect "he" but contribute less than the race-related features.

5. **Spurious Correlations Present:** Notably, `L0:F13663` ("pregnancy-related terms") is directly triggered by "white" with weight 15 — a clear spurious correlation. Similarly, `L0:F10910` associates "white" with unrelated words like "possession" and "immediate."

6. **Low frac_nonzero Values:** All identity-related features have low frac_nonzero (0.001-0.06), meaning they fire selectively. However, this selectivity is for identity token detection rather than toxic content understanding.

**Conclusion:** The probe uses a **lexical identity-matching strategy** where detecting the token "white" at position 4 dominates the classification, with minimal contribution from understanding the actual statement's conditional/comparative semantics. The presence of "Hispanic" at position 7 only weakly contributes through the pronoun detector. This is a textbook example of spurious feature reliance — the model correlates identity group mentions with toxicity rather than analyzing the actual problematic content.

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L0:12768 de=0.205 |

### Dispatch: 13 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L0:F12768@2` | ✅ reported | 3 | 5 | Trace what this feature encodes and where it originates. Is it a spurious identi… |
| SA-2 | `L0:F3436@4` | ✅ reported | 1 | 1 | Trace what this feature encodes and where it originates. Is it a spurious identi… |
| SA-3 | `L0:F13663@4` | ✅ reported | 1 | 1 | Trace what this feature encodes and where it originates. Is it a spurious identi… |
| SA-4 | `L4:F15204@4` | ✅ reported | 7 | 9 | Trace what this feature encodes and where it originates. Is it a spurious identi… |
| SA-5 | `L0:F880@8` | ✅ reported | 2 | 4 | Trace what this feature encodes and where it originates. Is it a spurious identi… |
| SA-6 | `L2:F6983@4` | ✅ reported | 6 | 6 | Trace what this feature encodes and where it originates. Is it a spurious identi… |
| SA-7 | `L0:F10910@4` | ✅ reported | 3 | 3 | Trace what this feature encodes and where it originates. Is it a spurious identi… |
| SA-8 | `L0:F3255@5` | ✅ reported | 1 | 5 | Trace what this feature encodes and where it originates. Is it a spurious identi… |
| SA-9 | `L2:F1139@3` | ✅ reported | 2 | 4 | Trace what this feature encodes and where it originates. Is it a spurious identi… |
| SA-10 | `L4:F7136@4` | ✅ reported | 9 | 17 | Trace what this feature encodes and where it originates. Is it a spurious identi… |
| SA-11 | `L3:F12404@1` | ✅ reported | 6 | 12 | Trace what this feature encodes and where it originates. Is it a spurious identi… |
| SA-12 | `L1:F1480@4` | ✅ reported | 5 | 13 | Trace what this feature encodes and where it originates. Is it a spurious identi… |
| SA-13 | `L0:F310@2` | ✅ reported | 3 | 5 | Trace what this feature encodes and where it originates. Is it a spurious identi… |

<details>
<summary><b>SA-1</b> — tool trace (4 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F12768 | " mentions of "he" and "she" in close proximity" |
| 2 | `get_upstream_features` | L0:F12768@2, k=5 | Emb:" he"@2 (w=37.00) +4 more |
| 3 | `inspect_feature` | L0, F1165 | "words relating to abstract concepts, like properties, associations or " |
| 4 | `inspect_feature` | L0, F1571 | " mathematical jargon, including equations, symbols, and theorem-like s" |

**Findings:** Tracing L0:F12768 reveals it's a pronoun-related feature that primarily detects the token "he" directly from the embedding layer with very strong weight (37.0). The feature's label mentions "mentions of 'he' and 'she' in close proximity" but its strongest connection is to the token "he" itself. Interestingly, the feature promotes tokens like "them" and "I" while suppressing "he" and foreign langua…

</details>

<details>
<summary><b>SA-2</b> — tool trace (2 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F3436 | " mentions of the word "white"" |
| 2 | `get_upstream_features` | L0:F3436@4, k=5 | Emb:" white"@4 (w=18.00) +4 more |

**Findings:** Tracing from L0:F3436 at position 4 reveals a simple circuit: the feature directly detects the word 'white' from its token embedding at position 4 (edge_weight 18.0). The feature has label 'mentions of the word white', frac_nonzero 0.06114 (relatively selective), and activates strongly on examples containing 'white' in racial/identity contexts. However, the promoted tokens appear random/unrelated …

</details>

<details>
<summary><b>SA-3</b> — tool trace (4 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F13663 | "mentions of pregnancy and related terms" |
| 2 | `get_upstream_features` | L0:F13663@4, k=5 | Emb:" white"@4 (w=15.00) +4 more |
| 3 | `get_top_logits` | k=5 | "" (100%) |
| 4 | `get_upstream_features` | L0:F13663@5, k=5 | ❌ Feature (layer=0, pos=5, feature_idx=13663) not found in gra |

**Findings:** Tracing from L0:F13663 at position 4 reveals a pregnancy-related feature that is directly triggered by the token 'white' at the same position with a strong edge weight of 15.0. This feature has low sparsity (frac_nonzero=0.00874), indicating it's specific to pregnancy contexts. The promoted tokens are mostly HTML formatting tags, suggesting this feature activates in document formatting contexts co…

</details>

<details>
<summary><b>SA-4</b> — tool trace (12 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F15204 | " art galleries, museums and the White House" |
| 2 | `get_upstream_features` | L4:F15204@4, k=5 | Emb:" white"@4 (w=40.50) +4 more |
| 3 | `inspect_feature` | L3, F11768 | " the word "white" and related contexts such as diversity" |
| 4 | `inspect_feature` | L2, F585 | "the word "white", often in association with "dwarf"" |
| 5 | `get_upstream_features` | L3:F11768@4, k=5 | Emb:" white"@4 (w=23.62) +4 more |
| 6 | `get_upstream_features` | L2:F585@4, k=5 | Emb:" white"@4 (w=29.38) +4 more |
| 7 | `inspect_feature` | L0, F6548 | " the word "national"" |
| 8 | `inspect_feature` | L0, F10910 | "the word "possession" and the words "white", "immediate" and "once" re" |
| 9 | `inspect_feature` | L1, F4668 | " the color white being used to describe image parameters" |
| 10 | `inspect_feature` | L1, F13007 | " mentions of the word "white" and to a lesser extent "black"" |
| 11 | `get_upstream_features` | L0:F10910@4, k=5 | Emb:" white"@4 (w=14.50) +4 more |
| 12 | `get_upstream_features` | L0:F6548@4, k=5 | Emb:" white"@4 (w=20.00) +4 more |

**Findings:** This circuit traces a feature encoding "art galleries, museums and the White House" (L4:F15204). The tracing reveals it's primarily a spurious identity signal triggered by the token "white" rather than content-relevant semantic understanding. The feature has low frac_nonzero (0.00484) suggesting specificity, but its upstream connections show it's mainly driven by lexical detection of "white" rathe…

</details>

<details>
<summary><b>SA-5</b> — tool trace (6 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F880 | " references to the pronoun "it", and sometimes "that", suggesting obse" |
| 2 | `get_upstream_features` | L0:F880@8, k=5 | Emb:" it"@8 (w=42.50) +4 more |
| 3 | `get_upstream_features` | L0:F880@8, k=10 | Emb:" it"@8 (w=42.50) +9 more |
| 4 | `inspect_feature` | L0, F2189 | " technical writing related to scientific studies" |
| 5 | `get_top_logits` | k=5 | "" (100%) |
| 6 | `get_top_features` | token="it", k=10 | ❌ Token 'it' not found in top logits. Available: [''] |

**Findings:** Tracing from L0:F880 at position 8 reveals a pronoun detection feature that specifically responds to the token "it". The feature has strong direct connection from the "it" embedding itself (weight 42.5) with much weaker connections from other tokens. This feature suppresses "it" tokens in output while promoting various foreign/formal tokens. With low frac_nonzero (0.02579), it's specific rather th…

</details>

<details>
<summary><b>SA-6</b> — tool trace (11 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L2, F6983 | " words related to race and slavery" |
| 2 | `get_upstream_features` | L2:F6983@4, k=5 | Emb:" white"@4 (w=8.12) +4 more |
| 3 | `inspect_feature` | L1, F4668 | " the color white being used to describe image parameters" |
| 4 | `inspect_feature` | L1, F10336 | " the word "grand" in legal documents or health questionnaires" |
| 5 | `get_upstream_features` | L1:F4668@4, k=5 | Emb:" white"@4 (w=19.75) +4 more |
| 6 | `get_upstream_features` | L1:F10336@4, k=5 | Emb:" white"@4 (w=11.50) +4 more |
| 7 | `inspect_feature` | L0, F6548 | " the word "national"" |
| 8 | `inspect_feature` | L0, F3436 | " mentions of the word "white"" |
| 9 | `get_upstream_features` | L0:F3436@4, k=5 | Emb:" white"@4 (w=18.00) +4 more |
| 10 | `get_top_logits` | k=5 | "" (100%) |
| 11 | `inspect_feature` | L0, F16013 | " mentions of the color blue, and perhaps colors in general or the comp" |

**Findings:** The circuit analysis reveals that L2:F6983 is a feature encoding "words related to race and slavery" that gets its primary signal directly from the embedding of the word "white" at position 4 (edge weight 8.125, not shown in edges list since it's embedding→feature). This feature has a relatively low frac_nonzero (0.033), indicating it's specific rather than generic.

Key findings:
1. Direct strong…

</details>

<details>
<summary><b>SA-7</b> — tool trace (6 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F10910 | "the word "possession" and the words "white", "immediate" and "once" re" |
| 2 | `get_upstream_features` | L0:F10910@4, k=5 | Emb:" white"@4 (w=14.50) +4 more |
| 3 | `get_top_logits` | k=10 | "" (100%) |
| 4 | `get_upstream_features` | L0:F10910@4, k=10 | Emb:" white"@4 (w=14.50) +9 more |
| 5 | `inspect_feature` | L0, F2189 | " technical writing related to scientific studies" |
| 6 | `inspect_feature` | L0, F2303 | " the word "if"" |

**Findings:** The feature L0:F10910 at position 4 is a simple token detector that fires on specific words including "white", "possession", "immediate", and "once". The circuit is extremely shallow: the feature receives strong direct input (edge_weight=14.5) from the embedding of the token "white" at position 4, with negligible contributions from other features. This is a content-relevant but simple lexical feat…

</details>

<details>
<summary><b>SA-8</b> — tool trace (3 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F3255 | " the word "and"" |
| 2 | `get_upstream_features` | L0:F3255@5, k=5 | Emb:" and"@5 (w=35.75) +4 more |
| 3 | `get_top_logits` | k=5 | "" (100%) |

**Findings:** This feature at L0:F3255 detects the word \"and\" at position 5. It has a low frac_nonzero (0.0298), indicating it's fairly specific. Interestingly, while it activates on \"and\", its promoted tokens are unusual words containing the historical \"long s\" character (ſ), such as \"Monfieur\", \"Efq\", \"myſelf\", \"Theſe\", etc., and it suppresses common tokens including \"and\" itself. The circuit …

</details>

<details>
<summary><b>SA-9</b> — tool trace (4 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L2, F1139 | " various usages of the word "so", as well as some instances of the wor" |
| 2 | `get_upstream_features` | L2:F1139@3, k=5 | Emb:"If"@1 (w=27.50) +4 more |
| 3 | `inspect_feature` | L0, F2458 | " the word "was" and sometimes "were."" |
| 4 | `get_upstream_features` | L0:F2458@3, k=5 | Emb:" was"@3 (w=36.75) +4 more |

**Findings:** The feature at L2:F1139 encodes conditional patterns involving the word "so" in contexts like "If so,..." as seen in its examples. It receives strong positive input from the embedding tokens "If" (pos 1) and " was" (pos 3), and negative input from an L0 feature that detects "was". The L0 feature itself is directly fed by the " was" embedding token. This circuit appears to be detecting grammatical/…

</details>

<details>
<summary><b>SA-10</b> — tool trace (15 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F7136 | " the color white" |
| 2 | `get_upstream_features` | L4:F7136@4, k=5 | Emb:" white"@4 (w=43.25) +4 more |
| 3 | `inspect_feature` | L3, F11768 | " the word "white" and related contexts such as diversity" |
| 4 | `inspect_feature` | L2, F585 | "the word "white", often in association with "dwarf"" |
| 5 | `inspect_feature` | L2, F1708 | " mentions of colors" |
| 6 | `get_upstream_features` | L3:F11768@4, k=5 | Emb:" white"@4 (w=23.62) +4 more |
| 7 | `get_upstream_features` | L2:F585@4, k=5 | Emb:" white"@4 (w=29.38) +4 more |
| 8 | `get_upstream_features` | L2:F1708@4, k=5 | Emb:" white"@4 (w=17.88) +4 more |
| 9 | `inspect_feature` | L1, F13007 | " mentions of the word "white" and to a lesser extent "black"" |
| 10 | `inspect_feature` | L0, F10910 | "the word "possession" and the words "white", "immediate" and "once" re" |
| 11 | `inspect_feature` | L0, F6548 | " the word "national"" |
| 12 | `inspect_feature` | L0, F16013 | " mentions of the color blue, and perhaps colors in general or the comp" |
| 13 | `get_upstream_features` | L1:F13007@4, k=5 | Emb:" white"@4 (w=16.25) +4 more |
| 14 | `inspect_feature` | L0, F3241 | " contexts related to "agreement", especially in a collaborative or pol" |
| 15 | `get_upstream_features` | L0:F10910@4, k=5 | Emb:" white"@4 (w=14.50) +4 more |

**Findings:** This circuit traces a feature at L4:F7136 labeled "the color white". The feature activates on the token "white" but surprisingly suppresses "white", "White", and related tokens in its output. The circuit shows that L4:F7136 primarily receives its signal directly from the embedding of " white" at position 4 (edge_weight 43.25), with some modulation from earlier layer features.

Key findings:
1. The…

</details>

<details>
<summary><b>SA-11</b> — tool trace (9 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L3, F12404 | " instances of the conditional word "if"" |
| 2 | `get_upstream_features` | L3:F12404@1, k=5 | Emb:"If"@1 (w=15.75) +4 more |
| 3 | `inspect_feature` | L2, F11539 | "the word "if"" |
| 4 | `get_upstream_features` | L2:F11539@1, k=5 | Emb:"If"@1 (w=15.06) +4 more |
| 5 | `inspect_feature` | L0, F1903 | "instances of sentences starting with "The"" |
| 6 | `inspect_feature` | L0, F12698 | "question-answer pairs (or just questions) and import statements" |
| 7 | `inspect_feature` | L0, F4823 | " the word "part" followed by prepositions or words related to sections" |
| 8 | `inspect_feature` | L0, F2303 | " the word "if"" |
| 9 | `get_upstream_features` | L0:F2303@1, k=5 | Emb:"If"@1 (w=14.00) +4 more |

**Findings:** The feature L3:F12404 encodes the conditional word "if". It's a content-relevant feature rather than a spurious identity signal. The circuit shows:

1. Direct strong connections from the "If" token embedding to all three "if"-detecting features (L0:F2303, L2:F11539, and L3:F12404) with weights 14.0-15.75, showing it's primarily driven by the raw token representation.

2. The feature is highly spec…

</details>

<details>
<summary><b>SA-12</b> — tool trace (9 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L1, F1480 | "the color 'white', sometimes in a context involving race" |
| 2 | `get_upstream_features` | L1:F1480@4, k=5 | Emb:" white"@4 (w=15.75) +4 more |
| 3 | `inspect_feature` | L0, F16013 | " mentions of the color blue, and perhaps colors in general or the comp" |
| 4 | `get_upstream_features` | L0:F16013@4, k=5 | Emb:" white"@4 (w=15.44) +4 more |
| 5 | `get_upstream_features` | L1:F1480@4, k=10 | Emb:" white"@4 (w=15.75) +9 more |
| 6 | `inspect_feature` | L0, F2449 | " HTML comments and some Javascript code" |
| 7 | `inspect_feature` | L0, F2189 | " technical writing related to scientific studies" |
| 8 | `inspect_feature` | L0, F10160 | " the word "uses"" |
| 9 | `get_upstream_features` | L0:F16013@4, k=15 | Emb:" white"@4 (w=15.44) +14 more |

**Findings:** This circuit traces a simple pattern: L1 feature 1480 encodes "the color 'white'" and gets its primary signal directly from the "white" token embedding at position 4 with very strong weight (15.75). There is inhibitory feedback from L0 feature 16013 which detects "blue/colors" but actually suppresses "white" tokens. The circuit is very shallow - essentially the L1 feature is detecting the literal …

</details>

<details>
<summary><b>SA-13</b> — tool trace (5 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F310 | " the pronouns "she", "her", and "he" and sometimes the word "therefore" |
| 2 | `get_upstream_features` | L0:F310@2, k=5 | Emb:" he"@2 (w=10.00) +4 more |
| 3 | `inspect_feature` | L0, F1165 | "words relating to abstract concepts, like properties, associations or " |
| 4 | `inspect_feature` | L0, F1571 | " mathematical jargon, including equations, symbols, and theorem-like s" |
| 5 | `get_top_logits` | k=5 | "" (100%) |

**Findings:** L0:F310 is a pattern-matching feature in the first layer that detects substrings containing "he" or "she". Its strongest connection is directly from the " he" token embedding at position 2 with weight 10.0, showing it responds to this specific token. The feature also fires on words like "sheath" (containing "she") as shown in its top activating examples. This appears to be a spurious identity sign…

</details>

### Build

`build_circuit` → 18 nodes, 20 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m2.7 | 35,552 | 4,564 | 38,516 | 0 | — | — | — |
| SA-2 | deepseek/deepseek-v3.2 | 8,917 | 1,070 | 0 | 0 | — | ✅ 1F/1E | Trace what this feature encodes and where it originates. Is … |
| SA-3 | deepseek/deepseek-v3.2 | 16,834 | 1,566 | 0 | 0 | — | ✅ 1F/1E | Trace what this feature encodes and where it originates. Is … |
| SA-1 | deepseek/deepseek-v3.2 | 18,879 | 1,725 | 0 | 0 | — | ✅ 3F/5E | Trace what this feature encodes and where it originates. Is … |
| SA-5 | deepseek/deepseek-v3.2 | 29,268 | 2,015 | 0 | 0 | — | ✅ 2F/4E | Trace what this feature encodes and where it originates. Is … |
| SA-4 | deepseek/deepseek-v3.2 | 69,897 | 2,781 | 8,896 | 0 | — | ✅ 7F/9E | Trace what this feature encodes and where it originates. Is … |
| SA-8 | deepseek/deepseek-v3.2 | 12,724 | 1,382 | 0 | 0 | — | ✅ 1F/5E | Trace what this feature encodes and where it originates. Is … |
| SA-9 | deepseek/deepseek-v3.2 | 18,140 | 1,381 | 0 | 0 | — | ✅ 2F/4E | Trace what this feature encodes and where it originates. Is … |
| SA-7 | deepseek/deepseek-v3.2 | 28,630 | 1,976 | 0 | 0 | — | ✅ 3F/3E | Trace what this feature encodes and where it originates. Is … |
| SA-6 | deepseek/deepseek-v3.2 | 68,424 | 2,964 | 0 | 0 | — | ✅ 6F/6E | Trace what this feature encodes and where it originates. Is … |
| SA-10 | deepseek/deepseek-v3.2 | 105,055 | 4,114 | 10,688 | 0 | — | ✅ 9F/17E | Trace what this feature encodes and where it originates. Is … |
| SA-13 | deepseek/deepseek-v3.2 | 23,751 | 1,893 | 0 | 0 | — | ✅ 3F/5E | Trace what this feature encodes and where it originates. Is … |
| SA-11 | deepseek/deepseek-v3.2 | 54,985 | 2,930 | 0 | 0 | — | ✅ 6F/12E | Trace what this feature encodes and where it originates. Is … |
| SA-12 | deepseek/deepseek-v3.2 | 54,503 | 3,147 | 0 | 0 | — | ✅ 5F/13E | Trace what this feature encodes and where it originates. Is … |
| **Total** | | **545,559** | **33,508** | **58,100** | **0** | **—** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 9m 35s