# Circuit Oracle Report
**Date:** 2026-04-06 08:58:31 UTC | **Orchestrator:** minimax/minimax-m2.7 | **Subagent:** deepseek/deepseek-v3.2

## Input

**Prompt:** "Dataset: bib_nurse_professor-neg_neg_4 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "('The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession.',)"

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score is driven by a combination of gender markers and genuine profession/academic indicators, but the circuit does rely substantially on the spurious gender feature "He" (L0:F1069, direct_effect=+0.0420) which directly reads from the input token "He" at position 1 with an edge weight of 22.625. However, the probe also uses legitimate profession indicators like "Director" (L2:F4627, direct_effect=-0.0471), academic credentials "Ph.D." (L7:F14129, direct_effect=+0.0432), Korean nationality from Korea University (L14:F15086, direct_effect=-0.061), and laboratory/institution mentions (L0:F5743, direct_effect=-0.0374). The gender marker appears alongside multiple genuine profession indicators, suggesting the probe uses a mix of spurious and legitimate features rather than relying solely on gender.

**Confidence:** 9

**Reasoning:** The circuit traces confirm that L0:F1069 ("references to a male person, particularly when using the pronoun 'He'") directly reads from the "He" token with weight 22.625 — this is a clear gender marker feature with low frac_nonzero (0.0078), indicating high specificity for male pronouns. The probe also incorporates legitimate profession detection via L2:F4627 (detects "director", weight 27.5 from "Director" token), academic degree detection via L7:F14129 (detects "academic degrees, universities", weight 7.125), and institutional/lab detection via L4:F12934/L0:F5743 (detecting "Laboratory" tokens). The Korea detector at L14:F15086 (detects "Korea/Korean", direct_effect=-0.061) captures the Korea University affiliation. Signal flows from early layer features reading "He", "Director", "Ph.D.", "Laboratory", and "Korea" tokens through hierarchical processing to late-layer features that contribute to the output. The presence of the gender marker in the circuit alongside genuine profession indicators confirms the user's concern is valid — the probe uses spurious gender features rather than relying solely on genuine profession indicators.

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L14:15086 de=-0.061 |

### Dispatch: 14 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L14:F15086@46` | ✅ reported | 8 | 22 | Trace this feature upstream to understand what signals it receives. Check for ge… |
| SA-2 | `L0:F10846@3` | ✅ reported | 2 | 7 | Trace this feature to understand what input token it fires on and what semantics… |
| SA-3 | `L2:F10852@40` | ✅ reported | 7 | 7 | Trace this feature to understand what input signals it receives at position 40. … |
| SA-4 | `L1:F14934@7` | ✅ reported | 4 | 16 | Trace this feature (positive effect) to understand what input token it fires on … |
| SA-5 | `L0:F1069@1` | ✅ reported | 2 | 2 | Trace this feature (positive effect) at position 1 to understand what input toke… |
| SA-6 | `L7:F14129@40` | ✅ reported | 7 | 9 | Trace this positive-effect feature at position 40 upstream to understand what si… |
| SA-7 | `L2:F4627@4` | ✅ reported | 5 | 14 | Trace this negative-effect feature at position 4 (likely "Director") to understa… |
| SA-8 | `L0:F1242@11` | ✅ reported | 1 | 1 | Trace this positive-effect feature at position 11 to understand what input token… |
| SA-9 | `L0:F12904@4` | ✅ reported | 1 | 1 | Trace this negative-effect feature at position 4 to understand what it detects. … |
| SA-10 | `L4:F12934@11` | ✅ reported | 4 | 9 | Trace this negative-effect feature at position 11 to understand what it detects.… |
| SA-11 | `L0:F3255@8` | ✅ reported | 1 | 5 | Trace this negative-effect feature at position 8 to understand what input token … |
| SA-12 | `L0:F15160@7` | ✅ reported | 1 | 1 | Trace this negative-effect feature at position 7 to understand what input token … |
| SA-13 | `L0:F8658@2` | ✅ reported | 1 | 2 | Trace this positive-effect feature at position 2 to understand what input token … |
| SA-14 | `L0:F5743@11` | ✅ reported | 1 | 5 | Trace this negative-effect feature at position 11 to understand what input token… |

<details>
<summary><b>SA-1</b> — tool trace (14 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L14, F15086 | " references to Korea/Korean" |
| 2 | `get_upstream_features` | L14:F15086@46, k=5 | Emb:" Korea"@46 (w=28.75) +4 more |
| 3 | `inspect_feature` | L7, F13010 | " Korean names, especially those with multiple parts separated by hyphe" |
| 4 | `get_upstream_features` | L7:F13010@46, k=5 | Emb:" Korea"@46 (w=14.19) +4 more |
| 5 | `inspect_feature` | L5, F5563 | " words related to Korean food and Korean conglomerates" |
| 6 | `inspect_feature` | L1, F10575 | " Korean names" |
| 7 | `inspect_feature` | L6, F3774 | " proper nouns or names with unusual capitalization" |
| 8 | `get_upstream_features` | L1:F10575@46, k=5 | Emb:" Korea"@46 (w=18.00) +4 more |
| 9 | `inspect_feature` | L0, F13470 | " references to locations, especially universities and countries" |
| 10 | `inspect_feature` | L0, F4160 | " mentions of North and South Korea" |
| 11 | `get_upstream_features` | L0:F4160@46, k=5 | Emb:" Korea"@46 (w=20.25) +4 more |
| 12 | `get_upstream_features` | L5:F5563@46, k=5 | Emb:" Korea"@46 (w=16.38) +4 more |
| 13 | `inspect_feature` | L8, F11910 | " technical texts about lenses and chip manufacturing" |
| 14 | `get_upstream_features` | L6:F3774@46, k=5 | Emb:" Korea"@46 (w=18.38) +4 more |

**Findings:** The tracing reveals that L14:F15086 (detects references to Korea/Korean) is primarily driven directly by the input token " Korea" at position 46. The circuit shows a hierarchy of Korea-related features at different layers, all ultimately fed by the same token embedding. Key findings:

1. L14:F15086 (Korea detector) receives strongest signal from token " Korea" at position 46 (edge_weight=28.75)
2.…

</details>

<details>
<summary><b>SA-2</b> — tool trace (4 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F10846 | "the word "also"" |
| 2 | `get_upstream_features` | L0:F10846@3, k=5 | Emb:" also"@3 (w=33.75) +4 more |
| 3 | `inspect_feature` | L0, F310 | " the pronouns "she", "her", and "he" and sometimes the word "therefore" |
| 4 | `get_upstream_features` | L0:F310@1, k=5 | Emb:"He"@1 (w=7.41) +4 more |

**Findings:** The feature L0:F10846 at position 3 is a simple word detector for "also". It fires directly on the input token " also" at position 3 with a very strong edge weight of 33.75. The circuit shows it's primarily driven by this specific token embedding, with minor influences from surrounding context tokens ("<bos>", " is", "He"). 

Interestingly, there's a connection (though with weight 0) to L0:F310 at…

</details>

<details>
<summary><b>SA-3</b> — tool trace (12 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L2, F10852 | " academic titles and degrees" |
| 2 | `get_upstream_features` | L2:F10852@40, k=5 | Emb:" Ph"@38 (w=14.12) +4 more |
| 3 | `inspect_feature` | L1, F10132 | " the abbreviation for Doctorate of Philosophy, "Ph.D." (or "PhD") writ" |
| 4 | `inspect_feature` | L1, F14298 | "academic publications, papers, and citations" |
| 5 | `get_upstream_features` | L1:F10132@40, k=5 | Emb:" Ph"@38 (w=16.12) +4 more |
| 6 | `get_upstream_features` | L1:F14298@40, k=5 | Emb:" Ph"@38 (w=11.00) +4 more |
| 7 | `inspect_feature` | L0, F14877 | " single uppercase letters, sometimes followed by other characters, whi" |
| 8 | `inspect_feature` | L0, F7699 | "words and abbreviations starting with the letter "D"" |
| 9 | `inspect_feature` | L0, F15795 | " the word 'necessarily'" |
| 10 | `inspect_feature` | L0, F11532 | "titles and roles of people in organizations" |
| 11 | `get_upstream_features` | L0:F14877@40, k=5 | Emb:"."@39 (w=8.12) +4 more |
| 12 | `get_upstream_features` | L0:F7699@40, k=5 | Emb:"D"@40 (w=11.44) +4 more |

**Findings:** I traced the L2:F10852 "academic titles and degrees" feature at position 40. The circuit shows it primarily receives input from the tokens " Ph" at position 38 and "D" at position 40, suggesting it's detecting "PhD" as a degree abbreviation. The strongest path goes directly from these token embeddings through layer 1 features that specifically detect PhD abbreviations and academic publications, th…

</details>

<details>
<summary><b>SA-4</b> — tool trace (9 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L1, F14934 | "the word "grid" and some related terms related to "grids"" |
| 2 | `get_upstream_features` | L1:F14934@7, k=5 | Emb:" Grid"@7 (w=18.25) +4 more |
| 3 | `inspect_feature` | L0, F6023 | " sections of documents with proper nouns and industry terminology." |
| 4 | `inspect_feature` | L0, F9122 | " words related to parents" |
| 5 | `inspect_feature` | L0, F4993 | " section titles, proper names, and words related to stages and periods" |
| 6 | `get_upstream_features` | L0:F6023@7, k=5 | Emb:" Grid"@7 (w=11.62) +4 more |
| 7 | `get_upstream_features` | L0:F9122@7, k=5 | Emb:" Grid"@7 (w=11.44) +4 more |
| 8 | `get_upstream_features` | L0:F4993@7, k=5 | Emb:" Grid"@7 (w=7.34) +4 more |
| 9 | `get_top_logits` | k=5 | "" (100%) |

**Findings:** The tracing reveals that L1:F14934 primarily detects the word "grid" at position 7, with the strongest connection directly from the token " Grid" (weight 18.25). The feature has low frac_nonzero (0.00919) indicating specificity. Interestingly, the circuit shows contextual influence from surrounding tokens: " Mobile" at position 6 (positive weights of 0.4141, 0.377, 0.8164 to layer 0 features), "He…

</details>

<details>
<summary><b>SA-5</b> — tool trace (5 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F1069 | " references to a male person, particularly when using the pronoun "He"" |
| 2 | `get_upstream_features` | L0:F1069@1, k=5 | Emb:"He"@1 (w=22.62) +4 more |
| 3 | `get_top_logits` | k=5 | "" (100%) |
| 4 | `inspect_feature` | L0, F310 | " the pronouns "she", "her", and "he" and sometimes the word "therefore" |
| 5 | `inspect_feature` | L0, F478 | "various kinds of brackets and parentheses followed by a period" |

**Findings:** The feature L0:F1069 at position 1 detects masculine pronouns, specifically firing on the input token "He" at position 1. The circuit is direct: the token embedding for "He" feeds strongly (weight 22.625) into this gender detection feature. There's also a weaker connection from the <bos> token (weight 6.9375). The feature L0:F310 detects similar pronouns but has zero edge weight to our target feat…

</details>

<details>
<summary><b>SA-6</b> — tool trace (11 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L7, F14129 | " academic degrees, universities, and people associated with them" |
| 2 | `get_upstream_features` | L7:F14129@40, k=5 | L6:F2254 (w=7.12) +4 more |
| 3 | `inspect_feature` | L6, F2254 | "references to academic degrees" |
| 4 | `inspect_feature` | L5, F13801 | "abbreviations for degrees and mentions of educational attainment" |
| 5 | `inspect_feature` | L1, F10132 | " the abbreviation for Doctorate of Philosophy, "Ph.D." (or "PhD") writ" |
| 6 | `get_upstream_features` | L6:F2254@40, k=5 | L2:F10852 (w=11.31) +4 more |
| 7 | `inspect_feature` | L2, F10852 | " academic titles and degrees" |
| 8 | `get_upstream_features` | L2:F10852@40, k=5 | Emb:" Ph"@38 (w=14.12) +4 more |
| 9 | `inspect_feature` | L1, F14298 | "academic publications, papers, and citations" |
| 10 | `get_upstream_features` | L5:F13801@40, k=5 | L2:F10852 (w=6.59) +4 more |
| 11 | `inspect_feature` | L4, F13943 | " words and abbreviations related to academic research" |

**Findings:** I traced the feature L7:F14129 at position 40 upstream through the attribution graph. The feature represents "academic degrees, universities, and people associated with them." Tracing upstream revealed a circuit focused on academic credentials:

The strongest upstream connection was from L6:F2254 (7.125 weight), which detects "references to academic degrees." This in turn receives strong input fro…

</details>

<details>
<summary><b>SA-7</b> — tool trace (8 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L2, F4627 | "the word "director"" |
| 2 | `get_upstream_features` | L2:F4627@4, k=5 | Emb:" Director"@4 (w=27.50) +4 more |
| 3 | `inspect_feature` | L0, F4621 | " words related to administrative positions and bodies" |
| 4 | `get_upstream_features` | L0:F4621@4, k=5 | Emb:" Director"@4 (w=14.56) +4 more |
| 5 | `get_upstream_features` | L2:F4627@4, k=10 | Emb:" Director"@4 (w=27.50) +9 more |
| 6 | `inspect_feature` | L1, F12669 | " the word "direct", especially when it relates to evidence" |
| 7 | `inspect_feature` | L1, F6258 | "the word "very" and sometimes words that are near it or similar in con" |
| 8 | `inspect_feature` | L1, F15565 | " people's job titles with "director" in them" |

**Findings:** The circuit shows that L2:F4627 (which detects but suppresses "director") is primarily driven directly by the input token " Director" at position 4 (edge weight 27.5). There's a weak gender connection: the L0 feature 4621 (administrative positions) receives a small positive signal from "He" (edge weight 0.207), but this is dwarfed by the direct " Director" connection (14.56). The L2 feature suppre…

</details>

<details>
<summary><b>SA-8</b> — tool trace (3 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F1242 | "the word "appropriate"" |
| 2 | `get_upstream_features` | L0:F1242@11, k=5 | Emb:" Laboratory"@11 (w=18.00) +4 more |
| 3 | `get_upstream_features` | L0:F1242@11, k=10 | Emb:" Laboratory"@11 (w=18.00) +9 more |

**Findings:** Tracing L0:F1242 at position 11: This feature detects the word \"appropriate\" (frac_nonzero=0.019). The circuit shows it's primarily triggered by the input token \" Laboratory\" at position 11 with a very strong edge weight of 18.0. This explains why the feature fires at position 11 - it's detecting the token \" Laboratory\", not a technical/academic term like \"parallel\", \"distributed\", or \"…

</details>

<details>
<summary><b>SA-9</b> — tool trace (3 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F12904 | "mentions of the day prior or positions of authority" |
| 2 | `get_upstream_features` | L0:F12904@4, k=5 | Emb:" Director"@4 (w=16.50) +4 more |
| 3 | `get_upstream_features` | L0:F12904@4, k=10 | Emb:" Director"@4 (w=16.50) +9 more |

**Findings:** Tracing reveals that feature L0:F12904 at position 4 detects \"mentions of the day prior or positions of authority\" but is directly driven by the token \" Director\" at that same position. The feature has low sparsity (frac_nonzero=0.00623) and activates strongly on tokens like \"yesterday\" in its top examples. The circuit is simple: the token embedding for \" Director\" at position 4 feeds dire…

</details>

<details>
<summary><b>SA-10</b> — tool trace (9 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F12934 | " names of academic journals" |
| 2 | `get_upstream_features` | L4:F12934@11, k=5 | Emb:" Laboratory"@11 (w=17.00) +4 more |
| 3 | `inspect_feature` | L3, F10132 | " the word "laboratory" or shortened versions" |
| 4 | `get_upstream_features` | L3:F10132@11, k=5 | Emb:" Laboratory"@11 (w=19.00) +4 more |
| 5 | `inspect_feature` | L2, F13731 | " the word "lab" or "laboratory"" |
| 6 | `get_upstream_features` | L2:F13731@11, k=5 | Emb:" Laboratory"@11 (w=20.38) +4 more |
| 7 | `inspect_feature` | L0, F11835 | "terms used in software code such as "assembly", "using", "namespace", " |
| 8 | `get_upstream_features` | L0:F11835@11, k=5 | Emb:" Laboratory"@11 (w=4.41) +4 more |
| 9 | `get_top_features` | token="Laboratory", k=10 | ❌ Token 'Laboratory' not found in top logits. Available: [''] |

**Findings:** Tracing L4:F12934 at position 11 reveals a circuit for detecting academic journal names in the context of "parallel and distributed computing systems". The feature specifically responds to journal names like "International Journal of Parallel Programming". 

Key findings:
1. The primary driver is the input token " Laboratory" at position 11, with strong positive connections throughout the circuit …

</details>

<details>
<summary><b>SA-11</b> — tool trace (2 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F3255 | " the word "and"" |
| 2 | `get_upstream_features` | L0:F3255@8, k=5 | Emb:" and"@8 (w=37.50) +4 more |

**Findings:** The negative-effect feature at position 8 (L0:F3255) detects the word \"and\". It has a low sparsity (frac_nonzero = 0.02981), meaning it's specific and only fires on about 3% of tokens. The circuit is simple: the feature directly reads from the token embedding of \" and\" at position 8 with a strong positive edge weight of 37.5, plus minor contextual influences from the beginning-of-sequence toke…

</details>

<details>
<summary><b>SA-12</b> — tool trace (3 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F15160 | "the word "concerns"" |
| 2 | `get_upstream_features` | L0:F15160@7, k=5 | Emb:" Grid"@7 (w=14.06) +4 more |
| 3 | `get_upstream_features` | L0:F15160@7, k=10 | Emb:" Grid"@7 (w=14.06) +9 more |

**Findings:** The negative-effect feature at L0:F15160 position 7 detects 'the word \"concerns\"' with frac_nonzero 0.01093 (relatively specific). Its strongest upstream connection is directly from the input token \" Grid\" at the same position (pos 7) with extremely strong edge weight 14.0625. This suggests the feature fires when it sees the token \" Grid\" and relates this to concerns. The circuit is very sha…

</details>

<details>
<summary><b>SA-13</b> — tool trace (2 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F8658 | " the word "is"" |
| 2 | `get_upstream_features` | L0:F8658@2, k=5 | Emb:"He"@1 (w=8.00) +4 more |

**Findings:** The feature L0:F8658 at position 2 detects the word \"is\" when it appears after \"He\". It's a first-layer feature that fires specifically on the token \" is\" at position 2, with strong influence from the preceding \"He\" token at position 1. This feature has low sparsity (frac_nonzero=0.0067), meaning it's quite specific and selective for detecting \"is\" in certain contexts, particularly when …

</details>

<details>
<summary><b>SA-14</b> — tool trace (3 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F5743 | "the word "lab" and words that might be associated with equipment or a " |
| 2 | `get_upstream_features` | L0:F5743@11, k=5 | Emb:" Laboratory"@11 (w=14.31) +4 more |
| 3 | `inspect_feature` | L0, F5743 | "the word "lab" and words that might be associated with equipment or a " |

**Findings:** Tracing L0:F5743 at position 11 reveals it's a feature that detects words related to \"lab\" and laboratory contexts. The circuit traces directly to the input token \" Laboratory\" at position 11 with a very strong edge weight (14.3125), indicating this is the primary input token driving the feature's activation. Secondary influences come from neighboring tokens like \" Computing\" at position 10 …

</details>

### Build

`build_circuit` → 17 nodes, 18 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m2.7 | 25,477 | 4,336 | 59,554 | 0 | $0.0146 | — | — |
| SA-5 | deepseek/deepseek-v3.2 | 23,620 | 1,456 | 0 | 0 | $0.0067 | ✅ 2F/2E | Trace this feature (positive effect) at position 1 to unders… |
| SA-2 | deepseek/deepseek-v3.2 | 18,252 | 1,640 | 0 | 0 | $0.0054 | ✅ 2F/7E | Trace this feature to understand what input token it fires o… |
| SA-4 | deepseek/deepseek-v3.2 | 52,595 | 2,805 | 0 | 0 | $0.0147 | ✅ 4F/16E | Trace this feature (positive effect) to understand what inpu… |
| SA-3 | deepseek/deepseek-v3.2 | 79,799 | 2,661 | 0 | 0 | $0.0218 | ✅ 7F/7E | Trace this feature to understand what input signals it recei… |
| SA-6 | deepseek/deepseek-v3.2 | 64,024 | 2,914 | 6,144 | 0 | $0.0179 | ✅ 7F/9E | Trace this positive-effect feature at position 40 upstream t… |
| SA-1 | deepseek/deepseek-v3.2 | 89,367 | 4,321 | 19,008 | 0 | $0.0254 | ✅ 8F/22E | Trace this feature upstream to understand what signals it re… |
| SA-9 | deepseek/deepseek-v3.2 | 13,420 | 957 | 0 | 0 | $0.0039 | ✅ 1F/1E | Trace this negative-effect feature at position 4 to understa… |
| SA-12 | deepseek/deepseek-v3.2 | 12,946 | 986 | 0 | 0 | $0.0037 | ✅ 1F/1E | Trace this negative-effect feature at position 7 to understa… |
| SA-11 | deepseek/deepseek-v3.2 | 9,179 | 1,160 | 0 | 0 | $0.0028 | ✅ 1F/5E | Trace this negative-effect feature at position 8 to understa… |
| SA-8 | deepseek/deepseek-v3.2 | 13,082 | 899 | 0 | 0 | $0.0037 | ✅ 1F/1E | Trace this positive-effect feature at position 11 to underst… |
| SA-10 | deepseek/deepseek-v3.2 | 49,038 | 2,691 | 3,392 | 0 | $0.0139 | ✅ 4F/9E | Trace this negative-effect feature at position 11 to underst… |
| SA-7 | deepseek/deepseek-v3.2 | 39,914 | 2,908 | 4,672 | 0 | $0.0116 | ✅ 5F/14E | Trace this negative-effect feature at position 4 (likely "Di… |
| SA-13 | deepseek/deepseek-v3.2 | 9,087 | 940 | 0 | 0 | $0.0027 | ✅ 1F/2E | Trace this positive-effect feature at position 2 to understa… |
| SA-14 | deepseek/deepseek-v3.2 | 10,071 | 1,168 | 3,520 | 0 | $0.0032 | ✅ 1F/5E | Trace this negative-effect feature at position 11 to underst… |
| **Total** | | **509,871** | **31,842** | **96,290** | **0** | **$0.1520** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 6m 42s