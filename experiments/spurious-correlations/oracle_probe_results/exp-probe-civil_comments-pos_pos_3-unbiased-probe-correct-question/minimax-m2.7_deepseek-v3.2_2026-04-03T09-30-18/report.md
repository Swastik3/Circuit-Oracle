# Circuit Oracle Report
**Date:** 2026-04-03 09:30:18 UTC | **Orchestrator:** minimax/minimax-m2.7 | **Subagent:** deepseek/deepseek-v3.2

## Input
**Prompt:** "Dataset: civil_comments-pos_pos_3 | Probe: unbiased | Method: correct"
**System prompt:** ""
**Question:** "The circuit use spurious features (e.g.,"an identity group" signals) rather than actual prompt content (lexical or semaintical) to predict toxicity."
**Top predictions:**  (100.0%)

## Oracle Analysis
**Analysis:** The toxicity probe classification is driven by a **substring-matching circuit on "hat"** (from "hate/hating") rather than identity-group detection. The identity term "Jew" at position 6 has only a weak connection (weight 0.32) to the toxicity circuit, while the primary drivers are the tokens "hat" (pos 3, weight 10.75→L4:F8407) and "Self" (pos 1, weight 36.5→L3:F735). Interestingly, L3:F9615 (self-prefix detection) actually **suppresses** toxicity (direct_effect=-0.14), suggesting the model partially counterbalances when detecting self-referential psychological terms.

**Confidence:** 8/10

**Reasoning:** The circuit traced from the output node through multiple layers reveals that L4:F8407 ("antagonists and fighting words") is the strongest direct driver (0.1758 effect), with promoted tokens including "attacking", "Enemy", "villains", "Satan", and "hate". This feature is primarily fed by the embedding of the token "hat" at position 3 (weight 10.75) — the substring in "hating". The "Self-" hyphenated pattern (L3:F735, frac_nonzero=0.00632) also contributes positively (0.1367 effect), detecting the phrase "Self-hating" via strong "Self" and "hat" embeddings. 

Critically, the "Jew" token at position 6 shows only marginal influence (edge weight 0.32 to L3:F592 "love/hate language"). While L4:F5181 promotes "Semitism" in its vocabulary, this appears incidental — the feature is driven by "hat" and "-ing" grammatical patterns (L3:F5808), not by the identity term itself.

The circuit does **not** rely on identity-group detection as the user feared. However, it does exhibit a different spurious pattern: **substring matching on "hat"** which could produce false positives on non-toxic words containing this substring (e.g., "whatever", "that", "hat" in other contexts). This is a lexical shortcut rather than semantic toxicity understanding.

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L4:8407 de=0.176 |

### Dispatch: 8 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L3:F735@3` | ✅ reported | 11 | 29 | Trace L3:F735 which has positive direct effect (0.1367) and appears at multiple … |
| SA-2 | `L3:F9615@3` | ✅ reported | 10 | 10 | Trace L3:F9615 which has NEGATIVE direct effect (-0.1426) and appears at pos 3 a… |
| SA-3 | `L4:F8407@4` | ✅ reported | 8 | 10 | Trace L4:F8407 which has strong positive effect (0.1758 at pos 4, 0.1025 at pos … |
| SA-4 | `L0:F2994@11` | ✅ reported | 1 | 2 | Trace L0:F2994 which fires at position 11 (the last word in the prompt - likely … |
| SA-5 | `L0:F8938@2` | ✅ reported | 8 | 14 | Trace L0:F8938 which fires at position 2 (likely "hating" or "liberal"). This is… |
| SA-6 | `L0:F3090@7` | ✅ reported | 1 | 2 | Trace L0:F3090 which fires at position 7 (immediately after "Jew" at position 6)… |
| SA-7 | `L6:F10545@4` | ✅ reported | 8 | 14 | Trace L6:F10545 which fires at position 4 with positive effect (0.0869). This is… |
| SA-8 | `L4:F5181@4` | ✅ reported | 8 | 8 | Trace L4:F5181 which detects "terms relating to political parties or ideologies"… |

<details>
<summary><b>SA-1</b> — tool trace (17 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L3, F735 | " words and phrases that include the word "self" followed by a hyphen" |
| 2 | `get_upstream_features` | L3:F735@3, k=5 | Emb:"Self"@1 (w=36.50) +4 more |
| 3 | `inspect_feature` | L2, F16224 | " words and phrases related to self-awareness, self-reference, or self-" |
| 4 | `inspect_feature` | L1, F14516 | " equations with symbols, especially those using "hat" notation" |
| 5 | `get_upstream_features` | L2:F16224@3, k=5 | Emb:"Self"@1 (w=14.25) +4 more |
| 6 | `inspect_feature` | L0, F15366 | " references to females and past tense verbs" |
| 7 | `get_upstream_features` | L1:F14516@3, k=5 | Emb:"hat"@3 (w=19.50) +4 more |
| 8 | `inspect_feature` | L0, F8063 | "figure references, color names, and highlighted words" |
| 9 | `inspect_feature` | L0, F1094 | " words and suffixes related to states and senses" |
| 10 | `get_upstream_features` | L3:F735@3, k=10 | Emb:"Self"@1 (w=36.50) +9 more |
| 11 | `inspect_feature` | L1, F2107 | " the word "enter", and other words and symbols common to mathematical " |
| 12 | `inspect_feature` | L0, F4336 | " the word "favor" and words used in legal contexts" |
| 13 | `inspect_feature` | L2, F7961 | " mentions of scientific studies and labels" |
| 14 | `inspect_feature` | L1, F6641 | "hyphens preceding or following letter sequences, presumably as part of" |
| 15 | `get_upstream_features` | L1:F6641@3, k=5 | Emb:"Self"@1 (w=7.34) +4 more |
| 16 | `inspect_feature` | L0, F13994 | " expressions of dislike or hatred" |
| 17 | `get_upstream_features` | L0:F13994@3, k=5 | Emb:"hat"@3 (w=11.38) +4 more |

**Findings:** The circuit for L3:F735 (detects \"self-\" hyphenated words) reveals it's primarily driven by the embedding tokens \"Self\" at position 1 (weight: 36.5) and \"hat\" at position 3 (weight: 5.1875). The feature shows complex regulation with inhibitory connections from L2:F16224 (self-reference detection, weight: -3.0781) and L1:F14516 (mathematical hat notation, weight: -1.0547). 

Key findings:
1. …

</details>

<details>
<summary><b>SA-2</b> — tool trace (16 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L3, F9615 | " words containing the prefix "self-"" |
| 2 | `get_upstream_features` | L3:F9615@3, k=5 | Emb:"Self"@1 (w=36.00) +4 more |
| 3 | `get_upstream_features` | L3:F9615@4, k=5 | Emb:"Self"@1 (w=30.88) +4 more |
| 4 | `inspect_feature` | L2, F16224 | " words and phrases related to self-awareness, self-reference, or self-" |
| 5 | `inspect_feature` | L1, F14516 | " equations with symbols, especially those using "hat" notation" |
| 6 | `inspect_feature` | L2, F1319 | "words ending in "ing," regardless of their part of speech, but with a " |
| 7 | `get_upstream_features` | L2:F16224@3, k=5 | Emb:"Self"@1 (w=14.25) +4 more |
| 8 | `get_upstream_features` | L2:F16224@4, k=5 | Emb:"Self"@1 (w=9.94) +4 more |
| 9 | `get_upstream_features` | L1:F14516@3, k=5 | Emb:"hat"@3 (w=19.50) +4 more |
| 10 | `inspect_feature` | L0, F15366 | " references to females and past tense verbs" |
| 11 | `inspect_feature` | L1, F12381 | " instances of calculating a value" |
| 12 | `get_upstream_features` | L2:F1319@4, k=5 | Emb:"ing"@4 (w=29.50) +4 more |
| 13 | `inspect_feature` | L0, F8063 | "figure references, color names, and highlighted words" |
| 14 | `inspect_feature` | L0, F1094 | " words and suffixes related to states and senses" |
| 15 | `inspect_feature` | L1, F11580 | "words or suffixes related to formal documents or processes" |
| 16 | `inspect_feature` | L1, F5542 | "technical and legal jargon along with instances of the suffix "ing"" |

**Findings:** The circuit tracing reveals that L3:F9615 (feature detecting words containing the prefix "self-") has a NEGATIVE direct effect (-0.1426) on toxicity classification, meaning it SUPPRESSES toxicity. This feature is strongly connected to the embedding of token "Self" at position 1 (edge weight 36.0 at pos 3, 30.875 at pos 4), suggesting it detects the word "Self" from the input "Self-hating".

The ma…

</details>

<details>
<summary><b>SA-3</b> — tool trace (14 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F8407 | " words related to antagonists and fighting" |
| 2 | `get_upstream_features` | L4:F8407@4, k=5 | Emb:"hat"@3 (w=10.75) +4 more |
| 3 | `inspect_feature` | L3, F592 | "words related to love, affection, and hate, including foreign language" |
| 4 | `inspect_feature` | L3, F8492 | "the word "hate"" |
| 5 | `inspect_feature` | L1, F5138 | " code referring to bounding boxes" |
| 6 | `get_upstream_features` | L3:F8492@4, k=5 | Emb:"hat"@3 (w=12.75) +4 more |
| 7 | `get_upstream_features` | L3:F592@4, k=5 | Emb:"hat"@3 (w=7.69) +4 more |
| 8 | `inspect_feature` | L1, F11862 | "text from academic biological or legal documents that cites names" |
| 9 | `get_upstream_features` | L1:F5138@4, k=5 | Emb:"ing"@4 (w=21.38) +4 more |
| 10 | `get_upstream_features` | L4:F8407@3, k=5 | Emb:"hat"@3 (w=7.38) +4 more |
| 11 | `inspect_feature` | L3, F9615 | " words containing the prefix "self-"" |
| 12 | `inspect_feature` | L0, F4014 | "words and phrases that are considered indecent or offensive." |
| 13 | `inspect_feature` | L0, F4847 | " the word "affairs" or the "unlike"." |
| 14 | `get_upstream_features` | L0:F4014@4, k=5 | Emb:"ing"@4 (w=13.50) +4 more |

**Findings:** I traced the circuit for L4:F8407 (words related to antagonists and fighting). The feature detects opposition, enemies, and antagonism with promoted tokens like "attacking", "hated", "Enemy", "villains", "Satan", and "hate". 

The circuit reveals:
1. Strongest upstream connection is from the embedding "hat" at position 3 (edge weight 10.75) directly to L4:F8407
2. Key intermediate features: 
   - …

</details>

<details>
<summary><b>SA-4</b> — tool trace (4 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F2994 | "the pronoun "his" and the pronoun "he."" |
| 2 | `get_upstream_features` | L0:F2994@11, k=5 | Emb:" his"@11 (w=44.25) +4 more |
| 3 | `get_upstream_features` | L0:F2994@11, k=10 | Emb:" his"@11 (w=44.25) +9 more |
| 4 | `get_top_logits` | k=5 | "" (100%) |

**Findings:** Tracing from L0:F2994 at position 11 revealed this feature detects the pronoun \"his\", not identity terms like \"Jew\". The feature's label is \"the pronoun 'his' and the pronoun 'he.'\", with promoted tokens being punctuation/formatting (space, period, newline) and suppressed tokens being various forms of \"his\". The strongest upstream connection (weight 44.25) is from the embedding of \" his\"…

</details>

<details>
<summary><b>SA-5</b> — tool trace (18 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F8938 | "hyphens adjacent to numbers" |
| 2 | `get_upstream_features` | L0:F8938@2, k=5 | Emb:"-"@2 (w=34.50) +4 more |
| 3 | `get_upstream_features` | L0:F8938@2, k=10 | Emb:"-"@2 (w=34.50) +9 more |
| 4 | `inspect_feature` | L0, F946 | "snippets of Rust source code at the beginning of a file" |
| 5 | `inspect_feature` | L0, F963 | " the word "sold", and also activates on "signed"" |
| 6 | `get_top_logits` | k=5 | "" (100%) |
| 7 | `get_top_features` | token="", k=10 | 10 features; top: L4:8407 de=0.176 |
| 8 | `inspect_feature` | L1, F2107 | " the word "enter", and other words and symbols common to mathematical " |
| 9 | `inspect_feature` | L0, F2994 | "the pronoun "his" and the pronoun "he."" |
| 10 | `inspect_feature` | L3, F9615 | " words containing the prefix "self-"" |
| 11 | `inspect_feature` | L3, F735 | " words and phrases that include the word "self" followed by a hyphen" |
| 12 | `get_upstream_features` | L3:F735@3, k=10 | Emb:"Self"@1 (w=36.50) +9 more |
| 13 | `inspect_feature` | L2, F16224 | " words and phrases related to self-awareness, self-reference, or self-" |
| 14 | `inspect_feature` | L1, F14516 | " equations with symbols, especially those using "hat" notation" |
| 15 | `inspect_feature` | L0, F4336 | " the word "favor" and words used in legal contexts" |
| 16 | `inspect_feature` | L0, F1094 | " words and suffixes related to states and senses" |
| 17 | `get_upstream_features` | L1:F2107@3, k=5 | Emb:"hat"@3 (w=15.31) +4 more |
| 18 | `get_upstream_features` | L0:F1094@3, k=5 | Emb:"hat"@3 (w=13.38) +4 more |

**Findings:** I traced the circuit starting from L0:F8938 at position 2. This feature encodes "hyphens adjacent to numbers" but in this context appears to be detecting the hyphen in "Self-hating" or similar compound. The circuit reveals:

1. L0:F8938 is primarily driven by the "-" token embedding at position 2 (weight: 34.5), with minor inhibition from "Self" token at position 1.

2. A key feature in the circui…

</details>

<details>
<summary><b>SA-6</b> — tool trace (9 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F3090 | " JavaScript or other C-style code with member access via "." and "->"" |
| 2 | `get_upstream_features` | L0:F3090@7, k=5 | Emb:" -"@7 (w=13.69) +4 more |
| 3 | `get_top_logits` | k=5 | "" (100%) |
| 4 | `get_top_features` | token="Jewish", k=10 | ❌ Token 'Jewish' not found in top logits. Available: [''] |
| 5 | `get_top_features` | token="", k=10 | 10 features; top: L4:8407 de=0.176 |
| 6 | `inspect_feature` | L0, F2994 | "the pronoun "his" and the pronoun "he."" |
| 7 | `inspect_feature` | L0, F8938 | "hyphens adjacent to numbers" |
| 8 | `inspect_feature` | L1, F2107 | " the word "enter", and other words and symbols common to mathematical " |
| 9 | `inspect_feature` | L4, F8407 | " words related to antagonists and fighting" |

**Findings:** Tracing from L0:F3090 at position 7 revealed it is a coding feature detecting C-style member access (".", "->"). It receives direct input from the "Jew" embedding at position 6 with weight 0.1816, and stronger input from "-" at position 7 (weight 13.6875). The feature promotes "Jefus" (historical spelling of Jesus), suggesting some religious connection. However, no feature was found that specifica…

</details>

<details>
<summary><b>SA-7</b> — tool trace (12 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F10545 | " political rhetoric related to race, historical states, and government" |
| 2 | `get_upstream_features` | L6:F10545@4, k=5 | L4:F8407 (w=1.64) +4 more |
| 3 | `inspect_feature` | L4, F8407 | " words related to antagonists and fighting" |
| 4 | `inspect_feature` | L4, F5181 | " terms relating to political parties or ideologies" |
| 5 | `inspect_feature` | L4, F10004 | " hyphenated words beginning with "self"" |
| 6 | `get_upstream_features` | L4:F8407@4, k=5 | Emb:"hat"@3 (w=10.75) +4 more |
| 7 | `get_upstream_features` | L4:F5181@4, k=5 | Emb:"hat"@3 (w=2.94) +4 more |
| 8 | `inspect_feature` | L3, F592 | "words related to love, affection, and hate, including foreign language" |
| 9 | `inspect_feature` | L3, F5808 | "words ending in "-ing" that have a sense of driving something forward" |
| 10 | `get_upstream_features` | L3:F592@4, k=5 | Emb:"hat"@3 (w=7.69) +4 more |
| 11 | `inspect_feature` | L1, F5138 | " code referring to bounding boxes" |
| 12 | `inspect_feature` | L3, F9615 | " words containing the prefix "self-"" |

**Findings:** L6:F10545 encodes political rhetoric related to race, historical states, and government control. The circuit originates from token "hat" at position 3 and token "Self" at position 1. Key intermediate features include L4:F8407 (antagonistic/fighting language), L4:F5181 (political ideologies), and L3:F592 (love/hate language). The feature appears to be part of a censorship circuit that monitors poli…

</details>

<details>
<summary><b>SA-8</b> — tool trace (16 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F5181 | " terms relating to political parties or ideologies" |
| 2 | `get_upstream_features` | L4:F5181@4, k=5 | Emb:"hat"@3 (w=2.94) +4 more |
| 3 | `inspect_feature` | L3, F5808 | "words ending in "-ing" that have a sense of driving something forward" |
| 4 | `inspect_feature` | L3, F592 | "words related to love, affection, and hate, including foreign language" |
| 5 | `inspect_feature` | L1, F5138 | " code referring to bounding boxes" |
| 6 | `get_upstream_features` | L3:F5808@4, k=5 | Emb:"Self"@1 (w=5.41) +4 more |
| 7 | `get_upstream_features` | L3:F592@4, k=5 | Emb:"hat"@3 (w=7.69) +4 more |
| 8 | `inspect_feature` | L2, F5277 | " words ending in "ing" and some adjectives" |
| 9 | `inspect_feature` | L2, F1319 | "words ending in "ing," regardless of their part of speech, but with a " |
| 10 | `inspect_feature` | L1, F11862 | "text from academic biological or legal documents that cites names" |
| 11 | `get_upstream_features` | L2:F5277@4, k=5 | Emb:"ing"@4 (w=7.00) +4 more |
| 12 | `get_upstream_features` | L2:F1319@4, k=5 | Emb:"ing"@4 (w=29.50) +4 more |
| 13 | `inspect_feature` | L1, F11580 | "words or suffixes related to formal documents or processes" |
| 14 | `get_top_logits` | k=10 | "" (100%) |
| 15 | `get_top_features` | token="Semitism", k=10 | ❌ Token 'Semitism' not found in top logits. Available: [''] |
| 16 | `get_top_features` | token="hets", k=10 | ❌ Token 'hets' not found in top logits. Available: [''] |

**Findings:** I traced the circuit for L4:F5181, which detects "terms relating to political parties or ideologies" and promotes "Semitism" in its top tokens. Key findings:

1. The feature L4:F5181 has promoted tokens including "hets", "anti", "Semitism", "hate", and "hatred", suggesting it might be involved in detecting hate speech or political extremism related to anti-Semitism.

2. The circuit shows strong di…

</details>

### Build

`build_circuit` → 13 nodes, 25 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m2.7 | 57,237 | 4,971 | 28,660 | 0 | — | — | — |
| SA-4 | deepseek/deepseek-v3.2 | 19,322 | 2,770 | 0 | 0 | — | ✅ 1F/2E | Trace L0:F2994 which fires at position 11 (the last word in … |
| SA-2 | deepseek/deepseek-v3.2 | 99,098 | 3,694 | 19,392 | 0 | — | ✅ 10F/10E | Trace L3:F9615 which has NEGATIVE direct effect (-0.1426) an… |
| SA-3 | deepseek/deepseek-v3.2 | 90,700 | 3,904 | 19,584 | 0 | — | ✅ 8F/10E | Trace L4:F8407 which has strong positive effect (0.1758 at p… |
| SA-5 | deepseek/deepseek-v3.2 | 139,371 | 5,448 | 25,984 | 0 | — | ✅ 8F/14E | Trace L0:F8938 which fires at position 2 (likely "hating" or… |
| SA-1 | deepseek/deepseek-v3.2 | 109,293 | 6,296 | 43,904 | 0 | — | ✅ 11F/29E | Trace L3:F735 which has positive direct effect (0.1367) and … |
| SA-7 | deepseek/deepseek-v3.2 | 81,303 | 3,299 | 0 | 0 | — | ✅ 8F/14E | Trace L6:F10545 which fires at position 4 with positive effe… |
| SA-6 | deepseek/deepseek-v3.2 | 57,242 | 4,541 | 0 | 0 | — | ✅ 1F/2E | Trace L0:F3090 which fires at position 7 (immediately after … |
| SA-8 | deepseek/deepseek-v3.2 | 109,066 | 3,449 | 19,456 | 0 | — | ✅ 8F/8E | Trace L4:F5181 which detects "terms relating to political pa… |
| **Total** | | **762,632** | **38,372** | **156,980** | **0** | **—** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 13m 11s