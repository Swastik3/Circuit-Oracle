# Circuit Oracle Report
**Date:** 2026-03-26 17:45:42 UTC | **Orchestrator:** anthropic/claude-opus-4.6 | **Subagent:** anthropic/claude-sonnet-4.6

## Input
**Prompt:** "Dataset: bib_nurse_professor-pos_pos_2 | Probe: biased | Method: correct"
**System prompt:** ""
**Concern:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."
**Top predictions:**  (100.0%)

## Oracle Analysis
Now let me compute the final quantitative breakdown and write the analysis.

---

**Analysis:** The probe classifying this text as "nurse" relies **predominantly on gender-marker features** (feminine pronouns, female names) rather than genuine nursing profession indicators, confirming the user's concern about spurious feature usage.

**Confidence:** High

**Reasoning:**

## Quantitative Breakdown of Direct Effects on Probe Score

I tallied all top-20 features by their direct effect on the probe classification score and categorized them:

### Gender-Marker Features (Positive Effect): **~3.43 total**
| Feature | Label | Positions | Summed Direct Effect |
|---------|-------|-----------|---------------------|
| L6:11646 | "references to women, triggered by pronouns/titles" | pos 1, 2, 19 | **+1.12** |
| L18:14677 | "instances of women or girls being mentioned" | pos 1, 19, 35, 50 | **+1.10** |
| L4:15317 | "named entities" (promotes she/her/herself) | pos 2 | **+0.35** |
| L4:7864 | polysemantic but promotes "herself/she" | pos 1 | **+0.34** |
| L12:12940 | "female pronouns and possessive pronouns" | pos 2 | **+0.31** |
| L19:9685 | "women's names and their roles" | pos 140, 19 | **+0.47** |
| L6:8166 | "proper names ending in a/i/e" (female-leaning) | pos 81 | **+0.25** |

### Nursing/Profession Features (Positive Effect): **~0.69 total**
| Feature | Label | Position | Direct Effect |
|---------|-------|----------|---------------|
| L6:15267 | **"words referring to the profession of nursing"** | pos 10 | **+0.47** |
| L6:170 | "references to academic fields" | pos 10 | **+0.21** |

### Gender Features with Negative Effect (counter-features): **~-0.93 total**
| Feature | Label | Position | Direct Effect |
|---------|-------|----------|---------------|
| L7:8644 | "woman's name" (promotes "himself") | pos 10 | **-0.28** |
| L6:16329 | "female first names" (promotes "himself") | pos 1, 19 | **-0.44** |
| L5:5996 | "femininity/womanhood" (promotes "himself") | pos 81 | **-0.20** |

## Circuit Mechanism

The circuit has **two distinct pathways** that converge at the probe output:

### Path 1 — Gender Cascade (dominant, ~83% of positive signal)
The token **"She"** at positions 1 and 19 is the single most powerful driver. It feeds through a **deep 7-layer cascade** of progressively more abstract feminine-gender features:

1. **Embedding "She"** → **Early Gender Detectors** (L0:15382 "female person mentions", frac=0.009; L0:9519 "she/her pronoun", frac=0.011) — these are highly specific, sparse features that fire on the literal pronoun.
2. → **Mid-Layer Gender** (L4:15317 "named entities, female-biased", frac=0.018; L4:7864, frac=0.015) — with the "She" embedding providing massive direct weight (10.9–24.6).
3. → **Women Reference** (L6:11646 "references to women", frac=0.020) — fires at 3 positions (1, 2, 19), contributing +1.12 total.
4. → **Gender Cascade** (L10:14965 "terms relating to women", frac=0.019; L12:12940 "female pronouns", frac=0.007)
5. → **Late Gender** (L15:3330 "personal stories of women", frac=0.019; L17:5889 "pronouns", frac=0.018)
6. → **Women Mentioned** (L18:14677 "women/girls mentioned", frac=0.012) — fires at 4 positions, contributing +1.10 total.
7. → **Women's Roles** (L19:9685 "women's names and roles", frac=0.014) — also fed by the name "Kayte" at pos 140.

At every layer, the **raw "She" embedding** is the dominant input (edge weights 13–27), dwarfing feature-mediated connections (1–5).

### Path 2 — Nursing Profession Pipeline (minority, ~17% of positive signal)
The token **"Nursing"** at position 10 drives a separate, genuinely profession-relevant pipeline:

1. **Embedding "Nursing"** → **Early Nursing Pipeline** (L1:10429 "academic programs"; L2:10852 "academic titles/degrees", frac=0.008; L3:15901 "nurses/nursing", frac=0.005; L3:6246 "nourishment/nursing etymology", frac=0.004)
2. → **Mid Profession** (L4:11037 "counseling/therapy/social work/degree programs", frac=0.007; L5:1275 "healthcare professionals", frac=0.013)
3. → **Nursing Feature** (L6:15267 "nursing profession", frac=0.016) — contributing +0.47.

This pathway is internally coherent and specific (all features have low frac_nonzero 0.004–0.016, with nursing-relevant top activating examples), but its total contribution (+0.69) is **dwarfed** by the gender pathway (+3.43).

### Counter-Features
Interestingly, some features that detect female names/femininity have **negative** effects on the probe (L6:16329, L7:8644, L5:5996, total -0.93). These features promote "himself" and suppress "herself" — they appear to be **male-biased gender features** that fire on feminine inputs and *compete against* the probe's classification. Their negative effect partially offsets the gender signal but doesn't eliminate it.

## Conclusion: The Probe Is Predominantly Gender-Biased

**The user's concern is validated.** The probe relies on gender markers for approximately **83% of its positive classification signal** (3.43 out of 4.12 positive direct effect) versus only **17% from genuine nursing/profession features** (0.69 out of 4.12). The single token "She" at position 1, through its massive embedding weight propagating through 7 layers of feminine-gender features, contributes more to the nurse classification than the actual word "Nursing" does. This means the probe would likely classify *any* text about a woman with similar confidence, regardless of her actual profession — a classic spurious correlation where "nurse" is predicted primarily because the subject is female, not because nursing-specific content is present.

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L6:11646 de=0.496 |
| 3 | `inspect_feature` ×13 | L6:11646, L6:15267, L18:14677, L4:15317, L4:7864, L12:12940, L19:9685, L6:8166, L6:16329, L0:16075, L6:170, L7:8644, L5:5996 |

### Dispatch: 6 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L6:F11646@1` | ✅ reported | 0 | 0 | Trace the top positive feature L6:11646 at pos 1 (likely "She") — this is labele… |
| SA-2 | `L6:F15267@10` | ✅ reported | 11 | 22 | Trace L6:15267 at pos 10 — this is labeled "words referring to the profession of… |
| SA-3 | `L18:F14677@19` | ✅ reported | 3114 | 17 | Trace L18:14677 at pos 19 — labeled "instances of women or girls being mentioned… |
| SA-4 | `L19:F9685@140` | ✅ reported | 12 | 16 | Trace L19:9685 at pos 140 (near end of text, likely near 'Kayte') — labeled "wom… |
| SA-5 | `L12:F12940@2` | ✅ reported | 10 | 19 | Trace L12:12940 at pos 2 — labeled "female pronouns and possessive pronouns." De… |
| SA-6 | `L18:F14677@1` | ✅ reported | 13 | 22 | Trace L18:14677 at pos 1 (on 'She') — this is the same gender feature firing on … |

<details>
<summary><b>SA-1</b> — tool trace (19 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F11646 | " references to women, potentially triggered by pronouns and titles" |
| 2 | `get_upstream_features` | L6:F11646@1, k=6 | Emb:"She"@1 (w=19.25) +5 more |
| 3 | `inspect_feature` | L4, F7864 | "xml or source code snippets, especially tags and possibly keywords in " |
| 4 | `inspect_feature` | L5, F10952 | "third person pronouns in varying contexts" |
| 5 | `inspect_feature` | L3, F4020 | " the pronoun "she"" |
| 6 | `inspect_feature` | L0, F12519 | " the pronoun "she"" |
| 7 | `get_upstream_features` | L4:F7864@1, k=6 | Emb:"She"@1 (w=24.62) +5 more |
| 8 | `get_upstream_features` | L5:F10952@1, k=6 | Emb:"She"@1 (w=8.56) +5 more |
| 9 | `get_upstream_features` | L3:F4020@1, k=6 | Emb:"She"@1 (w=19.00) +5 more |
| 10 | `inspect_feature` | L2, F2128 | " pronouns, especially "he/him/it" equivalents like *er*, *ihn*, *es*, " |
| 11 | `inspect_feature` | L2, F8966 | " the pronoun "she"" |
| 12 | `inspect_feature` | L2, F7672 | " mentions of women by name and relationship" |
| 13 | `inspect_feature` | L0, F3232 | " mentions of the third person plural pronoun "They"" |
| 14 | `get_upstream_features` | L2:F2128@1, k=6 | Emb:"She"@1 (w=20.12) +5 more |
| 15 | `get_upstream_features` | L2:F7672@1, k=6 | Emb:"She"@1 (w=13.81) +5 more |
| 16 | `inspect_feature` | L1, F2848 | " the pronouns "she" and "her" (and sometimes "his")" |
| 17 | `inspect_feature` | L0, F9519 | " the pronoun "she" and the possessive pronoun "her"" |
| 18 | `inspect_feature` | L0, F15382 | "mentions of a female person." |
| 19 | `inspect_feature` | L0, F10473 | " the word "sight" and words associated to it, like vision and breath" |

</details>

<details>
<summary><b>SA-2</b> — tool trace (16 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F15267 | " words in the document referring to the profession of nursing" |
| 2 | `get_upstream_features` | L6:F15267@10, k=8 | Emb:" Nursing"@10 (w=17.38) +7 more |
| 3 | `inspect_feature` | L4, F11037 | " words related to counseling, therapy, social work, and academic degre" |
| 4 | `inspect_feature` | L3, F15901 | " mentions of nurses, nursing, and nurse management" |
| 5 | `inspect_feature` | L5, F1275 | "words related to healthcare professionals and medical fields" |
| 6 | `get_upstream_features` | L4:F11037@10, k=6 | Emb:" Nursing"@10 (w=10.56) +5 more |
| 7 | `get_upstream_features` | L3:F15901@10, k=6 | Emb:" Nursing"@10 (w=15.06) +5 more |
| 8 | `inspect_feature` | L4, F8751 | " cell types in the brain, especially glial cells and neurons, and rela" |
| 9 | `inspect_feature` | L3, F6246 | " the word "Nutrients" and words containing "ure"." |
| 10 | `inspect_feature` | L2, F10852 | " academic titles and degrees" |
| 11 | `inspect_feature` | L2, F9995 | " terms related to occupations and fields of study" |
| 12 | `get_upstream_features` | L2:F10852@10, k=6 | Emb:" Nursing"@10 (w=11.44) +5 more |
| 13 | `get_upstream_features` | L3:F6246@10, k=6 | Emb:" Nursing"@10 (w=9.62) +5 more |
| 14 | `inspect_feature` | L1, F10429 | " words related to academic programs" |
| 15 | `inspect_feature` | L1, F12372 | " mentions of US universities and sports teams" |
| 16 | `inspect_feature` | L0, F4559 | " the word "fact" in the text" |

**Findings:** ## Circuit Summary: L6:F15267 — "Words Referring to the Profession of Nursing" at pos 10

### Key Finding: The " Nursing" Token Embedding is the Overwhelming Driver

The single most important input feeding into the L6 nursing profession feature is the **raw token embedding of " Nursing"** at position 10, with a direct edge weight of **17.375** — by far the largest influence in the circuit. This me…

</details>

<details>
<summary><b>SA-3</b> — tool trace (19 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L18, F14677 | " instances of women or girls being mentioned" |
| 2 | `get_upstream_features` | L18:F14677@19, k=8 | Emb:" She"@19 (w=15.31) +7 more |
| 3 | `inspect_feature` | L17, F5889 | " references to people with pronouns and possessive pronouns" |
| 4 | `inspect_feature` | L15, F3330 | " personal stories of individuals, especially women and their actions o" |
| 5 | `inspect_feature` | L0, F15382 | "mentions of a female person." |
| 6 | `inspect_feature` | L6, F11646 | " references to women, potentially triggered by pronouns and titles" |
| 7 | `get_upstream_features` | L17:F5889@19, k=6 | Emb:" She"@19 (w=21.38) +5 more |
| 8 | `get_upstream_features` | L15:F3330@19, k=6 | Emb:" She"@19 (w=18.00) +5 more |
| 9 | `get_upstream_features` | L6:F11646@19, k=6 | Emb:" She"@19 (w=19.00) +5 more |
| 10 | `inspect_feature` | L13, F6622 | " pronouns." |
| 11 | `inspect_feature` | L0, F9519 | " the pronoun "she" and the possessive pronoun "her"" |
| 12 | `inspect_feature` | L0, F14257 | "the word 'newly' and adjectives ending in 'able'" |
| 13 | `inspect_feature` | L6, F2267 | "words that appear in programming code, legal jargon, or scientific tex" |
| 14 | `inspect_feature` | L4, F7864 | "xml or source code snippets, especially tags and possibly keywords in " |
| 15 | `inspect_feature` | L0, F12519 | " the pronoun "she"" |
| 16 | `get_upstream_features` | L0:F15382@19, k=6 | Emb:" She"@19 (w=23.62) +5 more |
| 17 | `get_upstream_features` | L0:F9519@19, k=6 | Emb:" She"@19 (w=25.75) +5 more |
| 18 | `get_upstream_features` | L13:F6622@19, k=6 | Emb:" She"@19 (w=13.56) +5 more |
| 19 | `inspect_feature` | L12, F5722 | " references to people using personal pronouns" |

**Findings:** 
## Circuit Summary: L18:F14677 — "Instances of Women or Girls Being Mentioned"

### Primary Driver: Raw Token Embedding " She" at pos 19
The overwhelmingly dominant input is the **raw token embedding for " She"** at position 19, which directly contributes with edge weights of 15–26 across every node in the circuit. This single lexical token is the root cause of the entire gender feature activatio…

</details>

<details>
<summary><b>SA-4</b> — tool trace (18 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L19, F9685 | " references to women's names and their roles or accomplishments." |
| 2 | `get_upstream_features` | L19:F9685@140, k=8 | L4:F1276 (w=1.46) +7 more |
| 3 | `inspect_feature` | L4, F1276 | "capitalized names and titles, and names with lowercase letters in the " |
| 4 | `inspect_feature` | L4, F1302 | " parts of names or titles, sometimes followed by numbers" |
| 5 | `inspect_feature` | L13, F11685 | " words related to women" |
| 6 | `inspect_feature` | L18, F3679 | " personal pronouns and/or proper nouns" |
| 7 | `get_upstream_features` | L4:F1276@140, k=8 | Emb:" Kay"@139 (w=3.77) +7 more |
| 8 | `get_upstream_features` | L4:F1302@140, k=8 | Emb:"te"@140 (w=2.72) +7 more |
| 9 | `get_upstream_features` | L18:F3679@140, k=8 | L15:F4094 (w=2.89) +7 more |
| 10 | `inspect_feature` | L2, F5859 | " first names (mostly female)" |
| 11 | `inspect_feature` | L15, F4094 | " occurrences of auxiliary verbs in the text" |
| 12 | `inspect_feature` | L17, F15936 | "titles and proper names, and common words and phrases, in legal docume" |
| 13 | `inspect_feature` | L3, F6656 | "verbs or phrases indicating action, saying, or feeling" |
| 14 | `get_upstream_features` | L2:F5859@140, k=8 | Emb:" Kay"@139 (w=5.47) +7 more |
| 15 | `get_upstream_features` | L13:F11685@140, k=8 | Emb:"She"@1 (w=3.89) +7 more |
| 16 | `inspect_feature` | L5, F5996 | " words associated with females, femininity or womanhood" |
| 17 | `inspect_feature` | L7, F8644 | " woman's name in a variety of contexts" |
| 18 | `inspect_feature` | L0, F8153 | " French language words ending in "te"" |

**Findings:** ## Circuit Summary: What drives L19:F9685 ("women's names and their roles")?

**Primary Answer: The token " Kay" (pos 139 — the first subtoken of "Kayte") is the single strongest driver**, with massive embedding edge weights of 5.47 → L2:F5859 and 3.77 → L4:F1276. The "te" suffix token at pos 140 also contributes directly but with smaller weight.

**Three converging input streams:**

### Stream 1 …

</details>

<details>
<summary><b>SA-5</b> — tool trace (15 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L12, F12940 | "references to female pronouns and possessive pronouns" |
| 2 | `get_upstream_features` | L12:F12940@2, k=8 | Emb:" graduated"@2 (w=4.81) +7 more |
| 3 | `inspect_feature` | L4, F15317 | " named entities like characters or people" |
| 4 | `inspect_feature` | L10, F14965 | " terms relating to women" |
| 5 | `inspect_feature` | L6, F11646 | " references to women, potentially triggered by pronouns and titles" |
| 6 | `inspect_feature` | L7, F2765 | " mentions of people or characters, and their performance, roles, injur" |
| 7 | `get_upstream_features` | L4:F15317@2, k=8 | Emb:"She"@1 (w=10.94) +7 more |
| 8 | `get_upstream_features` | L6:F11646@2, k=8 | L4:F15317 (w=5.97) +7 more |
| 9 | `get_upstream_features` | L10:F14965@2, k=8 | Emb:"She"@1 (w=5.06) +7 more |
| 10 | `inspect_feature` | L2, F7672 | " mentions of women by name and relationship" |
| 11 | `inspect_feature` | L5, F645 | " verbs in past tense" |
| 12 | `inspect_feature` | L5, F16213 | " proper nouns consisting of a first and last name" |
| 13 | `inspect_feature` | L0, F6513 | "the word "graduated" (or variations of it) and mentions of degrees." |
| 14 | `get_upstream_features` | L2:F7672@1, k=6 | Emb:"She"@1 (w=13.81) +5 more |
| 15 | `inspect_feature` | L7, F8644 | " woman's name in a variety of contexts" |

**Findings:** The circuit driving L12:F12940 ("female pronouns and possessive pronouns") at pos 2 ('graduated') originates almost entirely from the raw token embedding of "She" at position 1, with a secondary contribution from the " graduated" embedding itself.

PRIMARY PATHWAY — "She" → gender cascade:
1. EMBEDDING "She" (pos 1) is the single most powerful signal throughout the circuit, with edge weights of 13…

</details>

<details>
<summary><b>SA-6</b> — tool trace (16 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L18, F14677 | " instances of women or girls being mentioned" |
| 2 | `get_upstream_features` | L18:F14677@1, k=8 | Emb:"She"@1 (w=27.25) +7 more |
| 3 | `inspect_feature` | L15, F851 | " code documentation blocks in various programming languages" |
| 4 | `inspect_feature` | L4, F7864 | "xml or source code snippets, especially tags and possibly keywords in " |
| 5 | `inspect_feature` | L12, F12493 | " words that end in "ing", "ecti", "tial", or "ogi", and also the word " |
| 6 | `inspect_feature` | L11, F9183 | " large empty spaces in the text" |
| 7 | `inspect_feature` | L6, F11646 | " references to women, potentially triggered by pronouns and titles" |
| 8 | `get_upstream_features` | L4:F7864@1, k=8 | Emb:"She"@1 (w=24.62) +7 more |
| 9 | `get_upstream_features` | L6:F11646@1, k=8 | Emb:"She"@1 (w=19.25) +7 more |
| 10 | `inspect_feature` | L2, F2128 | " pronouns, especially "he/him/it" equivalents like *er*, *ihn*, *es*, " |
| 11 | `inspect_feature` | L0, F12519 | " the pronoun "she"" |
| 12 | `inspect_feature` | L5, F10952 | "third person pronouns in varying contexts" |
| 13 | `inspect_feature` | L0, F15382 | "mentions of a female person." |
| 14 | `get_upstream_features` | L2:F2128@1, k=6 | Emb:"She"@1 (w=20.12) +5 more |
| 15 | `inspect_feature` | L1, F2848 | " the pronouns "she" and "her" (and sometimes "his")" |
| 16 | `inspect_feature` | L0, F9519 | " the pronoun "she" and the possessive pronoun "her"" |

**Findings:** ## Circuit Summary: L18:F14677 — Feminine Gender Feature at Position 1 ("She")

**Core finding:** The dominant input to L18:F14677 (a feminine gender feature promoting she/her/herself) is overwhelmingly the **raw token embedding of "She"** (edge_weight=27.25), far exceeding all other inputs. This is a nearly direct embedding-to-feature pathway — the model reads the literal token "She" and activate…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` ×2 | L6:170, L0:16075 |

### Build

`build_circuit` → 19 nodes, 37 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | anthropic/claude-opus-4.6 | 147,668 | 7,797 | 0 | 0 | $0.9333 | — | — |
| SA-5 | anthropic/claude-sonnet-4.6 | 53,333 | 4,524 | 0 | 0 | $0.2279 | ✅ 10F/19E | Trace L12:12940 at pos 2 — labeled "female pronouns and poss… |
| SA-4 | anthropic/claude-sonnet-4.6 | 68,493 | 4,851 | 0 | 0 | $0.2782 | ✅ 12F/16E | Trace L19:9685 at pos 140 (near end of text, likely near 'Ka… |
| SA-2 | anthropic/claude-sonnet-4.6 | 59,486 | 5,109 | 0 | 0 | $0.2551 | ✅ 11F/22E | Trace L6:15267 at pos 10 — this is labeled "words referring … |
| SA-1 | anthropic/claude-sonnet-4.6 | 71,167 | 5,817 | 0 | 0 | $0.3008 | ✅ 0F/0E | Trace the top positive feature L6:11646 at pos 1 (likely "Sh… |
| SA-6 | anthropic/claude-sonnet-4.6 | 73,591 | 5,328 | 0 | 0 | $0.3007 | ✅ 13F/22E | Trace L18:14677 at pos 1 (on 'She') — this is the same gende… |
| SA-3 | anthropic/claude-sonnet-4.6 | 73,520 | 5,076 | 0 | 0 | $0.2967 | ✅ 3114F/17E | Trace L18:14677 at pos 19 — labeled "instances of women or g… |
| **Total** | | **547,258** | **38,502** | **0** | **0** | **$2.5926** | | |

**Oracle wall-clock time:** 13m 53s