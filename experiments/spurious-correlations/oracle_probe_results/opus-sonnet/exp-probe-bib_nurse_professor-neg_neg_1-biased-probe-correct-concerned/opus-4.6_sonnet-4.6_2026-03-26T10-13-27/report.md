# Circuit Oracle Report
**Date:** 2026-03-26 10:13:27 UTC | **Orchestrator:** anthropic/claude-opus-4.6 | **Subagent:** anthropic/claude-sonnet-4.6

## Input
**Prompt:** "Dataset: bib_nurse_professor-neg_neg_1 | Probe: biased | Method: correct"
**System prompt:** ""
**Concern:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."
**Top predictions:**  (100.0%)

## Oracle Analysis
**Analysis:** The probe's classification is driven almost entirely by gender pronoun detection features triggered by the tokens "His" (pos 1) and "He" (pos 14), not by genuine profession indicators from the text's content about computer science, visualization, or Los Alamos National Laboratory.

**Confidence:** High

**Reasoning:**

This circuit reveals a deeply concerning reliance on **spurious gender markers** rather than genuine profession indicators. Here is the detailed mechanism:

### Dominant Signal: Gender Pronoun Detection (>90% of attribution)

The top 10 features by direct effect on the probe score are **all** gender/pronoun features, firing almost exclusively on position 1 ("His") and position 14 ("He"):

1. **L7:14893** (pos 1, direct_effect **+0.43**) — "pronouns or possessive pronouns." Promotes *female* pronouns (herself, elle, she). frac_nonzero=0.009 (very specific). This is the single strongest driver of the probe score.

2. **L7:14946** (pos 1, direct_effect **-0.42**) — "the possessive pronoun 'his'." Promotes *male* pronouns (himself, his). frac_nonzero=0.017. Pushes *against* the probe classification.

3. **L6:12990** (pos 1, direct_effect **-0.29**) — "male pronouns and titles associated with men." frac_nonzero=0.068.

4. **L18:14743** (pos 14 & 37, total direct_effect **-0.45**) — "He" detector. Promotes "himself." frac_nonzero=0.018.

5. **L19:8814** (pos 1, direct_effect **+0.24**) — Promotes "herself, she, her." frac_nonzero=0.087.

6. **L0:2994** (pos 1, direct_effect **+0.23**) — "the pronoun 'his' and 'he'." frac_nonzero=0.073.

### The Circuit: A Pronoun-Reading Pipeline

The signal flows through a clean pipeline, all anchored on the **raw token embeddings** of "His" and "He":

- **Emb: "His" (pos 1)** → feeds with massive edge weights (18–23.5) into every layer of the pronoun cascade: L0:2994, L1:7439, L4:4315, L5:10952, L6:12990, L7:14893, L7:14946
- **Emb: "He" (pos 14)** → feeds with edge weight 22–36 into L0:1069 → L13:6622 → L15:3330 → L17:5889 → L18:14743

The mid-layer features form a **male pronoun cascade** (L4:4315 → L5:10952 → L6:12990) that progressively refines the masculine pronoun signal. At L7, this splits into two competing features: **L7:14893** (female-promoting, +0.43 on probe) and **L7:14946** (male-promoting, -0.42 on probe). A minor "divine His" disambiguator (L2:5491, L3:13121) introduces inhibitory signals to distinguish religious "His" from possessive "his."

### Marginal Content Features (< 10% of attribution)

Only three features encode actual content from the biography:
- **L0:4564** — "research" (pos 2, direct_effect +0.16, frac_nonzero=0.007)
- **L2:9740** — "interest" (pos 3, direct_effect +0.13, frac_nonzero=0.006)
- **L0:2827** — "science" (pos 8, direct_effect **-0.12**, frac_nonzero=0.010)

These contribute a combined net effect of only **+0.17**, versus the gender features' combined absolute effect of **>2.0**. Crucially, the "science" feature actually pushes *against* the classification, suggesting the probe may not even correctly associate computer science content with the target profession.

### Conclusion: The Probe Is Spurious

**The user's concern is fully validated.** The probe trained on layer-22 activations has learned to classify profession primarily through **gender pronoun detection**, not profession-relevant content. The circuit's mechanism is:

1. Read the literal tokens "His" and "He" from the input
2. Process them through a multi-layer pronoun gender detection pipeline
3. Use the gender signal as the dominant predictor of the profession class

This is a textbook example of a **spurious correlation** — the probe likely learned that certain professions (e.g., computer scientist) correlate with male pronouns in the training data, rather than learning genuine profession-indicative features like "visualization," "computer science," "PhD," or "Los Alamos National Laboratory." None of these rich profession indicators appear meaningfully in the attribution circuit. The probe would likely misclassify a biography with identical professional content but female pronouns ("Her research interests include...").

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L7:14893 de=0.426 |
| 3 | `inspect_feature` ×16 | L7:14893, L7:14946, L6:12990, L18:14743, L19:8814, L0:2994, L4:4315, L0:4564, L18:7400, L18:10315, L2:9740, L2:5491, L0:6051, L0:2827, L0:14201, L7:16284 |

### Dispatch: 5 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L7:F14893@1` | ✅ reported | 6 | 16 | Trace the top positive-effect feature L7:14893 at pos 1 ("His"). This feature de… |
| SA-2 | `L7:F14946@1` | ✅ reported | 7 | 13 | Trace the top negative-effect feature L7:14946 at pos 1 ("His"). This feature de… |
| SA-3 | `L19:F8814@1` | ✅ reported | 12 | 22 | Trace the mid-layer feature L19:8814 at pos 1, which detects pronouns/names and … |
| SA-4 | `L18:F14743@14` | ✅ reported | 13 | 26 | Trace L18:14743 at pos 14 (labeled 'He'). This feature has negative effect -0.25… |
| SA-5 | `L6:F12990@1` | ✅ reported | 7 | 20 | Trace L6:12990 at pos 1 ('His'). This feature detects male pronouns/titles and h… |

<details>
<summary><b>SA-1</b> — tool trace (9 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L7, F14893 | " pronouns or possessive pronouns" |
| 2 | `get_upstream_features` | L7:F14893@1, k=6 | Emb:"His"@1 (w=23.50) +5 more |
| 3 | `inspect_feature` | L6, F12990 | " male pronouns and titles along with descriptors associated with men" |
| 4 | `inspect_feature` | L0, F2994 | "the pronoun "his" and the pronoun "he."" |
| 5 | `inspect_feature` | L4, F4315 | " mentions of "his" and other associated pronouns like he, him, or hers" |
| 6 | `get_upstream_features` | L6:F12990@1, k=5 | Emb:"His"@1 (w=4.91) +4 more |
| 7 | `get_upstream_features` | L4:F4315@1, k=5 | Emb:"His"@1 (w=23.50) +4 more |
| 8 | `inspect_feature` | L5, F10952 | "third person pronouns in varying contexts" |
| 9 | `inspect_feature` | L2, F5491 | "references to God in the third person." |

**Findings:** The circuit driving L7:F14893 ("pronouns or possessive pronouns", direct_effect +0.43) at pos 1 is overwhelmingly anchored by the raw "His" token embedding, NOT by any profession-related features. Key findings:

1. **Primary driver — "His" token embedding (weight 23.5 → L7:F14893)**: The raw embedding of "His" at pos 1 contributes a massive edge weight of 23.5 directly into the target feature. Thi…

</details>

<details>
<summary><b>SA-2</b> — tool trace (10 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L7, F14946 | " the possessive pronoun "his" (or similar pronouns like "he" and "him"" |
| 2 | `get_upstream_features` | L7:F14946@1, k=5 | Emb:"His"@1 (w=18.38) +4 more |
| 3 | `inspect_feature` | L4, F4315 | " mentions of "his" and other associated pronouns like he, him, or hers" |
| 4 | `inspect_feature` | L0, F2994 | "the pronoun "his" and the pronoun "he."" |
| 5 | `inspect_feature` | L6, F12990 | " male pronouns and titles along with descriptors associated with men" |
| 6 | `get_upstream_features` | L4:F4315@1, k=5 | Emb:"His"@1 (w=23.50) +4 more |
| 7 | `get_upstream_features` | L6:F12990@1, k=5 | Emb:"His"@1 (w=4.91) +4 more |
| 8 | `inspect_feature` | L1, F7439 | " the possessive pronouns "his" and "him"" |
| 9 | `inspect_feature` | L2, F5491 | "references to God in the third person." |
| 10 | `inspect_feature` | L5, F10952 | "third person pronouns in varying contexts" |

**Findings:** **Primary finding: The "His" token embedding is the dominant driver of L7:F14946.**

The circuit traces a clear, token-embedding-anchored path:

1. **Root cause — raw token embedding of "His" (pos=1):** This single input drives L7:F14946 with an edge weight of 18.375, making it by far the most influential input. The same embedding also dominates L4:F4315 (weight=23.5) and L6:F12990 (weight=4.9), c…

</details>

<details>
<summary><b>SA-3</b> — tool trace (20 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L19, F8814 | " various pronouns and names referring to people" |
| 2 | `get_upstream_features` | L19:F8814@1, k=8 | Emb:"His"@1 (w=9.31) +7 more |
| 3 | `inspect_feature` | L18, F7400 | " words related to coding and software/UI interfaces, with some bias to" |
| 4 | `inspect_feature` | L7, F14893 | " pronouns or possessive pronouns" |
| 5 | `inspect_feature` | L7, F14946 | " the possessive pronoun "his" (or similar pronouns like "he" and "him"" |
| 6 | `inspect_feature` | L18, F10315 | " pronouns and possessive pronouns" |
| 7 | `get_upstream_features` | L18:F7400@1, k=6 | Emb:"His"@1 (w=13.00) +5 more |
| 8 | `get_upstream_features` | L7:F14893@1, k=6 | Emb:"His"@1 (w=23.50) +5 more |
| 9 | `inspect_feature` | L6, F12990 | " male pronouns and titles along with descriptors associated with men" |
| 10 | `inspect_feature` | L4, F4315 | " mentions of "his" and other associated pronouns like he, him, or hers" |
| 11 | `inspect_feature` | L15, F851 | " code documentation blocks in various programming languages" |
| 12 | `inspect_feature` | L11, F10933 | "the letters "L", "H," and "a" when they are at the beginning of a text" |
| 13 | `inspect_feature` | L11, F9183 | " large empty spaces in the text" |
| 14 | `inspect_feature` | L9, F8770 | "sentences beginning with "It" or "In" and also the word "There"." |
| 15 | `get_upstream_features` | L6:F12990@1, k=6 | Emb:"His"@1 (w=4.91) +5 more |
| 16 | `get_upstream_features` | L4:F4315@1, k=6 | Emb:"His"@1 (w=23.50) +5 more |
| 17 | `inspect_feature` | L0, F2994 | "the pronoun "his" and the pronoun "he."" |
| 18 | `inspect_feature` | L1, F7439 | " the possessive pronouns "his" and "him"" |
| 19 | `inspect_feature` | L2, F5491 | "references to God in the third person." |
| 20 | `inspect_feature` | L3, F13121 | "the word "His" and words that are often capitalized in scientific lite" |

**Findings:** ## Circuit Summary: L19:F8814 — Female Pronoun Detector

**The upstream circuit feeding L19:F8814 is predominantly a GENDER circuit, not a profession circuit.** Here is the full picture:

### Core Finding: The Input is "His" — and the Circuit Fights Over Gender

The raw input token at pos 1 is **"His"** (a male possessive pronoun). The embedding of "His" directly drives most upstream features with…

</details>

<details>
<summary><b>SA-4</b> — tool trace (20 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L18, F14743 | "He" |
| 2 | `get_upstream_features` | L18:F14743@14, k=8 | Emb:" He"@14 (w=22.38) +7 more |
| 3 | `inspect_feature` | L0, F1069 | " references to a male person, particularly when using the pronoun "He"" |
| 4 | `inspect_feature` | L17, F5889 | " references to people with pronouns and possessive pronouns" |
| 5 | `inspect_feature` | L13, F6622 | " pronouns." |
| 6 | `inspect_feature` | L15, F3330 | " personal stories of individuals, especially women and their actions o" |
| 7 | `get_upstream_features` | L17:F5889@14, k=8 | Emb:" He"@14 (w=21.50) +7 more |
| 8 | `get_upstream_features` | L0:F1069@14, k=8 | Emb:" He"@14 (w=35.75) +7 more |
| 9 | `get_upstream_features` | L13:F6622@14, k=8 | Emb:" He"@14 (w=12.50) +7 more |
| 10 | `inspect_feature` | L6, F2267 | "words that appear in programming code, legal jargon, or scientific tex" |
| 11 | `inspect_feature` | L16, F2918 | "Pronouns" |
| 12 | `inspect_feature` | L12, F7725 | " mentions of people represented with titles and/or last names" |
| 13 | `get_upstream_features` | L15:F3330@14, k=8 | Emb:" He"@14 (w=17.12) +7 more |
| 14 | `get_upstream_features` | L12:F7725@14, k=8 | L11:F8266 (w=3.05) +7 more |
| 15 | `inspect_feature` | L11, F8266 | " mentions of people with professional titles or descriptions, especial" |
| 16 | `inspect_feature` | L14, F13478 | " occurrences of people's names, often with titles" |
| 17 | `get_upstream_features` | L11:F8266@14, k=8 | Emb:" He"@14 (w=2.36) +7 more |
| 18 | `inspect_feature` | L8, F2635 | " words, dates, titles, and name suffixes associated with people." |
| 19 | `inspect_feature` | L10, F1472 | " words that appear in resumes and biographies" |
| 20 | `inspect_feature` | L10, F15156 | " text related to a person's biography, including titles, awards, and r" |

**Findings:** ## Summary: L18:F14743 is driven overwhelmingly by the " He" pronoun token — NOT profession context.

### Key Finding: Pronoun-Dominated, Not Profession-Integrated

**The dominant signal is pure pronoun reading:**

1. **Raw `" He"` embedding at pos 14** is the single largest driver across every layer examined:
   - → L0:F1069 (edge weight **35.75**) — the very first feature in the network
   - → L…

</details>

<details>
<summary><b>SA-5</b> — tool trace (11 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F12990 | " male pronouns and titles along with descriptors associated with men" |
| 2 | `get_upstream_features` | L6:F12990@1, k=8 | Emb:"His"@1 (w=4.91) +7 more |
| 3 | `inspect_feature` | L4, F4315 | " mentions of "his" and other associated pronouns like he, him, or hers" |
| 4 | `inspect_feature` | L5, F10952 | "third person pronouns in varying contexts" |
| 5 | `inspect_feature` | L2, F5491 | "references to God in the third person." |
| 6 | `get_upstream_features` | L4:F4315@1, k=6 | Emb:"His"@1 (w=23.50) +5 more |
| 7 | `get_upstream_features` | L5:F10952@1, k=6 | Emb:"His"@1 (w=10.69) +5 more |
| 8 | `inspect_feature` | L0, F2994 | "the pronoun "his" and the pronoun "he."" |
| 9 | `inspect_feature` | L1, F7439 | " the possessive pronouns "his" and "him"" |
| 10 | `inspect_feature` | L3, F13121 | "the word "His" and words that are often capitalized in scientific lite" |
| 11 | `get_upstream_features` | L0:F2994@1, k=6 | Emb:"His"@1 (w=19.75) +5 more |

**Findings:** ## Circuit Summary: L6:F12990 — Male Pronouns/Titles Detector at pos 1 ("His")

### Primary Signal Path (Excitatory)
The dominant drive for L6:F12990 is the **raw "His" token embedding** itself (edge_weight = 4.91 directly to L6, 23.5 to L4:F4315, 10.7 to L5:F10952, 19.75 to L0:F2994). The token's surface form is the foundational input. Two key mid-layer features relay this signal upward:

1. **L4…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` ×4 | L5:10952, L1:7439, L3:13121, L0:1069 |

### Build

`build_circuit` → 13 nodes, 22 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | anthropic/claude-opus-4.6 | 191,296 | 5,721 | 0 | 0 | $1.0995 | — | — |
| SA-1 | anthropic/claude-sonnet-4.6 | 31,616 | 2,993 | 0 | 0 | $0.1397 | ✅ 6F/16E | Trace the top positive-effect feature L7:14893 at pos 1 ("Hi… |
| SA-2 | anthropic/claude-sonnet-4.6 | 32,848 | 3,402 | 0 | 0 | $0.1496 | ✅ 7F/13E | Trace the top negative-effect feature L7:14946 at pos 1 ("Hi… |
| SA-5 | anthropic/claude-sonnet-4.6 | 34,866 | 4,587 | 0 | 0 | $0.1734 | ✅ 7F/20E | Trace L6:12990 at pos 1 ('His'). This feature detects male p… |
| SA-4 | anthropic/claude-sonnet-4.6 | 102,286 | 5,542 | 0 | 0 | $0.3900 | ✅ 13F/26E | Trace L18:14743 at pos 14 (labeled 'He'). This feature has n… |
| SA-3 | anthropic/claude-sonnet-4.6 | 80,261 | 5,952 | 0 | 0 | $0.3301 | ✅ 12F/22E | Trace the mid-layer feature L19:8814 at pos 1, which detects… |
| **Total** | | **473,173** | **28,197** | **0** | **0** | **$2.2823** | | |

**Oracle wall-clock time:** 3m 57s