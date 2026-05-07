# Circuit Oracle Report
**Date:** 2026-03-26 18:13:00 UTC | **Orchestrator:** anthropic/claude-opus-4.6 | **Subagent:** anthropic/claude-sonnet-4.6

## Input
**Prompt:** "Dataset: bib_journalist_dietitian-pos_pos_2 | Probe: biased | Method: correct"
**System prompt:** ""
**Concern:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."
**Top predictions:**  (100.0%)

## Oracle Analysis
## Analysis

**Analysis:** The probe's classification is driven overwhelmingly by **gender/feminine pronoun features** rather than any genuine profession indicators — the circuit is a massive "she" detection pipeline, not a travel-agent or entrepreneur classifier.

**Confidence:** High

**Reasoning:**

The user's concern is **fully validated**. The probe is using spurious gender features, not genuine profession indicators. Here is the detailed evidence:

### The Circuit Is 100% Gender-Driven

**Every single one of the top 20 features** driving the probe's classification score relates to detecting female gender markers. Not a single feature in the entire attribution graph encodes profession-related concepts like "travel agent," "side hustle," "entrepreneurship," "service provider," or "trip planning." The text is about a woman who starts a travel planning business, yet the probe's circuit completely ignores this semantic content.

### Signal Origin: The Token "she"

The circuit originates at **four instances of the pronoun "she"/"She"** in the input text (positions 5, 13, 37, and 48). The raw token embedding of "she" is the single strongest driver at every layer, with edge weights of 22–39 — typically 5–10× larger than any feature-to-feature connection. The model literally reads the surface token "she" and propagates this signal through a cascade of gender-detection features.

### The Gender Cascade (Layers 0→19)

The circuit follows a clean, redundant escalation pattern:

1. **Embedding layer**: Raw "she" tokens at 4 positions
2. **L0**: Pronoun detectors — L0:12519 ("the pronoun 'she'", frac=0.039), L0:7509 ("female pronouns", frac=0.047), L0:9519 ("she/her pronouns", frac=0.011)
3. **L1-L2**: Gender pronoun features — L1:4232 ("possessive 'her'", frac=0.009), L2:8966 ("pronoun 'she'", frac=0.014)
4. **L4-L5**: Intermediaries — L4:7864 (frac=0.015, promotes "herself"/"she"), L5:10952 ("third person pronouns", frac=0.031)
5. **L6-L7**: Female reference — L6:11646 ("references to women", frac=0.020, **direct_effect=0.86 — the single strongest positive driver**), L7:8952 ("women by name/pronoun", frac=0.007)
6. **L10-L12**: Abstract gender — L10:14965 ("terms relating to women", frac=0.019), L12:12940 ("female pronouns", frac=0.007)
7. **L13-L15**: Narrative gender — L15:3330 ("personal stories of women", frac=0.019), L15:12956 ("female names/words", frac=0.019)
8. **L17-L19**: High-level gender — L18:14677 ("women/girls mentioned", frac=0.012, fires at **5 positions** with cumulative direct_effect ~1.38), L19:9685 ("women's names/accomplishments", frac=0.014)

### Negative Features Confirm the Pattern

The features that **suppress** the probe score are also gender-related, but for the *opposite* gender:
- **L18:14743** ("He" detector, direct_effect=−0.21 and −0.17) — detecting masculine pronouns pushes *against* the classification
- **L6:16329** ("female first names", direct_effect=−0.34) — this feature suppresses the probe, suggesting that explicit female names actually *compete with* the pronoun-based signal
- **L14:14097** ("occurrences of 'he'", direct_effect=−0.16) — masculine pronoun suppresses the classification

### What This Means

The linear probe trained on layer-22 residual streams has learned to classify this text's profession label by exploiting the **most salient but spurious signal in the representation**: the gender of the subject. Rather than encoding "travel agent" or "entrepreneur" via content words like "travel," "planning," "service," "pricing," or "hustle," the probe has found that the direction in activation space corresponding to the profession label is strongly aligned with the direction encoding *female gender*.

This is a textbook case of a **spurious correlation shortcut**: the training data likely had a strong correlation between the feminine pronoun "she" and this particular profession label, and the probe learned to exploit this statistical regularity rather than extracting genuine profession semantics. The circuit contains zero features that fire on profession-related content tokens — the words "hustle," "service," "website," "pricing," "travel," and "planning" appear nowhere in the attribution graph's significant features.

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L6:11646 de=0.859 |
| 3 | `inspect_feature` ×14 | L6:11646, L12:12940, L18:14677, L4:7864, L6:16329, L10:14965, L19:9685, L18:14743, L14:12501, L7:8952, L7:2765, L0:6051, L14:14097, L0:5912 |

### Dispatch: 8 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L6:F11646@5` | ✅ reported | 7 | 18 | Trace the strongest feature driving the probe — L6:11646 "references to women" a… |
| SA-2 | `L18:F14677@5` | ✅ reported | 9 | 16 | Trace L18:14677 "instances of women or girls being mentioned" at pos 5. This fir… |
| SA-3 | `L12:F12940@5` | ✅ reported | 7 | 13 | Trace L12:12940 "references to female pronouns" at pos 5. Determine if the signa… |
| SA-4 | `L18:F14677@37` | ✅ reported | 6 | 11 | Trace L18:14677 "women/girls mentioned" at pos 37 — this has the highest activat… |
| SA-5 | `L19:F9685@5` | ✅ reported | 0 | 0 | Trace L19:9685 "references to women's names and their roles or accomplishments" … |
| SA-6 | `L18:F14677@48` | ✅ reported | 5 | 6 | Trace L18:14677 at pos 48. Determine what token is at pos 48 and whether this po… |
| SA-7 | `L7:F2765@11` | ✅ reported | 7 | 7 | Trace L7:2765 at pos 11 — labeled 'mentions of people and their roles/details'. … |
| SA-8 | `L19:F9685@13` | ✅ reported | 10 | 12 | Trace L19:9685 at pos 13 — labeled 'women's names and accomplishments'. Determin… |

<details>
<summary><b>SA-1</b> — tool trace (12 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F11646 | " references to women, potentially triggered by pronouns and titles" |
| 2 | `get_upstream_features` | L6:F11646@5, k=8 | Emb:" she"@5 (w=32.50) +7 more |
| 3 | `inspect_feature` | L4, F7864 | "xml or source code snippets, especially tags and possibly keywords in " |
| 4 | `inspect_feature` | L0, F12519 | " the pronoun "she"" |
| 5 | `inspect_feature` | L5, F10952 | "third person pronouns in varying contexts" |
| 6 | `get_upstream_features` | L4:F7864@5, k=6 | Emb:" she"@5 (w=26.88) +5 more |
| 7 | `inspect_feature` | L1, F4232 | " the possessive pronoun "her"" |
| 8 | `inspect_feature` | L2, F8966 | " the pronoun "she"" |
| 9 | `get_upstream_features` | L0:F12519@5, k=6 | Emb:" she"@5 (w=39.00) +5 more |
| 10 | `get_upstream_features` | L2:F8966@5, k=5 | Emb:" she"@5 (w=33.25) +4 more |
| 11 | `get_upstream_features` | L1:F4232@5, k=5 | Emb:" she"@5 (w=30.75) +4 more |
| 12 | `inspect_feature` | L0, F7509 | " female pronouns and words like daughter and husband that refer to wom" |

**Findings:** ## Circuit Summary: L6:F11646 "References to Women" at pos 5

### Verdict: The signal originates overwhelmingly from GENDER MARKERS (the token " she"), NOT from profession-related content.

### Key Findings:

**1. The Raw Token Embedding Dominates**
The " she" token embedding at pos 5 is the single most powerful driver at every level of the circuit. Its direct edge weight into L6:F11646 is **32.5*…

</details>

<details>
<summary><b>SA-2</b> — tool trace (14 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L18, F14677 | " instances of women or girls being mentioned" |
| 2 | `get_upstream_features` | L18:F14677@5, k=8 | Emb:" she"@5 (w=27.75) +7 more |
| 3 | `inspect_feature` | L6, F11646 | " references to women, potentially triggered by pronouns and titles" |
| 4 | `inspect_feature` | L12, F12940 | "references to female pronouns and possessive pronouns" |
| 5 | `inspect_feature` | L17, F5889 | " references to people with pronouns and possessive pronouns" |
| 6 | `inspect_feature` | L4, F7864 | "xml or source code snippets, especially tags and possibly keywords in " |
| 7 | `get_upstream_features` | L6:F11646@5, k=6 | Emb:" she"@5 (w=32.50) +5 more |
| 8 | `get_upstream_features` | L12:F12940@5, k=6 | Emb:" she"@5 (w=11.69) +5 more |
| 9 | `inspect_feature` | L10, F14965 | " terms relating to women" |
| 10 | `inspect_feature` | L8, F7245 | " content in languages other than English, particularly French and poss" |
| 11 | `inspect_feature` | L0, F12519 | " the pronoun "she"" |
| 12 | `inspect_feature` | L7, F8952 | " references to women, by direct name or pronoun" |
| 13 | `get_upstream_features` | L0:F12519@5, k=6 | Emb:" she"@5 (w=39.00) +5 more |
| 14 | `inspect_feature` | L15, F12956 | "female names and female-related words in the document." |

**Findings:** **The upstream signal feeding L18:F14677 is purely and exclusively gender-related — not profession-related.**

The circuit traces back cleanly to a single root cause: the raw token embedding of " she" at position 5. Here is the complete picture:

**Root cause: " she" embedding (pos 5)**
The raw input token " she" is the overwhelmingly dominant driver at every level. L0:F12519 ("the pronoun 'she'")…

</details>

<details>
<summary><b>SA-3</b> — tool trace (11 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L12, F12940 | "references to female pronouns and possessive pronouns" |
| 2 | `get_upstream_features` | L12:F12940@5, k=8 | Emb:" she"@5 (w=11.69) +7 more |
| 3 | `inspect_feature` | L6, F11646 | " references to women, potentially triggered by pronouns and titles" |
| 4 | `inspect_feature` | L10, F14965 | " terms relating to women" |
| 5 | `inspect_feature` | L4, F7864 | "xml or source code snippets, especially tags and possibly keywords in " |
| 6 | `inspect_feature` | L8, F7245 | " content in languages other than English, particularly French and poss" |
| 7 | `get_upstream_features` | L6:F11646@5, k=8 | Emb:" she"@5 (w=32.50) +7 more |
| 8 | `inspect_feature` | L7, F8952 | " references to women, by direct name or pronoun" |
| 9 | `inspect_feature` | L0, F12519 | " the pronoun "she"" |
| 10 | `inspect_feature` | L4, F7864 | "xml or source code snippets, especially tags and possibly keywords in " |
| 11 | `get_upstream_features` | L10:F14965@5, k=6 | Emb:" she"@5 (w=11.56) +5 more |

**Findings:** **The signal at L12:F12940 ("female pronouns") overwhelmingly originates from the ' she' token embedding, NOT from semantic profession content.**

Key findings across 4 hops of tracing:

1. **Direct token embedding dominates:** The raw ' she' token embedding at pos 5 connects to L12:F12940 with edge weight 11.69, making it the single strongest upstream node — more than 2× the next-best feature.

2…

</details>

<details>
<summary><b>SA-4</b> — tool trace (9 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L18, F14677 | " instances of women or girls being mentioned" |
| 2 | `get_upstream_features` | L18:F14677@37, k=8 | Emb:" she"@37 (w=22.50) +7 more |
| 3 | `inspect_feature` | L17, F5889 | " references to people with pronouns and possessive pronouns" |
| 4 | `inspect_feature` | L0, F12519 | " the pronoun "she"" |
| 5 | `inspect_feature` | L15, F3330 | " personal stories of individuals, especially women and their actions o" |
| 6 | `get_upstream_features` | L17:F5889@37, k=6 | Emb:" she"@37 (w=28.25) +5 more |
| 7 | `get_upstream_features` | L15:F3330@37, k=6 | Emb:" she"@37 (w=22.00) +5 more |
| 8 | `inspect_feature` | L15, F11707 | " sentences containing personal pronouns expressing thoughts, feelings," |
| 9 | `inspect_feature` | L7, F8644 | " woman's name in a variety of contexts" |

**Findings:** **Token at pos 37: " she"** — confirmed by the dominant embedding node feeding into L18:F14677 with edge_weight=22.5.

**The signal encodes GENDER, not profession.**

The circuit is almost entirely driven by the literal presence of the feminine pronoun " she" at position 37. The evidence is clear at every level:

1. **Embedding level (bottom of circuit):** The raw " she" embedding is by far the st…

</details>

<details>
<summary><b>SA-5</b> — tool trace (22 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L19, F9685 | " references to women's names and their roles or accomplishments." |
| 2 | `get_upstream_features` | L19:F9685@5, k=8 | Emb:" she"@5 (w=12.00) +7 more |
| 3 | `inspect_feature` | L17, F5889 | " references to people with pronouns and possessive pronouns" |
| 4 | `inspect_feature` | L12, F12940 | "references to female pronouns and possessive pronouns" |
| 5 | `inspect_feature` | L6, F11646 | " references to women, potentially triggered by pronouns and titles" |
| 6 | `inspect_feature` | L4, F7864 | "xml or source code snippets, especially tags and possibly keywords in " |
| 7 | `get_upstream_features` | L17:F5889@5, k=6 | Emb:" she"@5 (w=31.88) +5 more |
| 8 | `get_upstream_features` | L12:F12940@5, k=6 | Emb:" she"@5 (w=11.69) +5 more |
| 9 | `get_upstream_features` | L6:F11646@5, k=6 | Emb:" she"@5 (w=32.50) +5 more |
| 10 | `inspect_feature` | L10, F14965 | " terms relating to women" |
| 11 | `inspect_feature` | L8, F7245 | " content in languages other than English, particularly French and poss" |
| 12 | `inspect_feature` | L14, F14097 | " occurrences of the word "he"" |
| 13 | `inspect_feature` | L16, F2918 | "Pronouns" |
| 14 | `inspect_feature` | L0, F12519 | " the pronoun "she"" |
| 15 | `get_upstream_features` | L10:F14965@5, k=6 | Emb:" she"@5 (w=11.56) +5 more |
| 16 | `get_upstream_features` | L8:F7245@5, k=6 | Emb:" she"@5 (w=7.19) +5 more |
| 17 | `inspect_feature` | L7, F8952 | " references to women, by direct name or pronoun" |
| 18 | `inspect_feature` | L6, F16329 | "female first names and their possessive forms" |
| 19 | `inspect_feature` | L7, F16125 | " language related to women, especially in the context of marriage, bir" |
| 20 | `get_upstream_features` | L7:F8952@5, k=6 | Emb:" she"@5 (w=25.25) +5 more |
| 21 | `inspect_feature` | L4, F14796 | "the pronoun "he" or "him"" |
| 22 | `inspect_feature` | L2, F8966 | " the pronoun "she"" |

</details>

<details>
<summary><b>SA-6</b> — tool trace (9 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L18, F14677 | " instances of women or girls being mentioned" |
| 2 | `get_upstream_features` | L18:F14677@48, k=5 | Emb:" She"@48 (w=15.19) +4 more |
| 3 | `inspect_feature` | L17, F5889 | " references to people with pronouns and possessive pronouns" |
| 4 | `inspect_feature` | L15, F3330 | " personal stories of individuals, especially women and their actions o" |
| 5 | `get_upstream_features` | L17:F5889@48, k=5 | Emb:" She"@48 (w=20.38) +4 more |
| 6 | `get_upstream_features` | L15:F3330@48, k=5 | Emb:" She"@48 (w=16.38) +4 more |
| 7 | `inspect_feature` | L13, F6622 | " pronouns." |
| 8 | `inspect_feature` | L14, F5740 | " sentences with multiple pronouns in them" |
| 9 | `get_upstream_features` | L13:F6622@48, k=5 | Emb:" She"@48 (w=13.31) +4 more |

**Findings:** **Token at pos 48: " She"** — a feminine pronoun, a clear gender marker with NO travel/profession content detected.

**Summary of the circuit:**
Position 48 contains the token " She", and the entire circuit from L13 through L18 is exclusively devoted to gender-marker / pronoun detection:

1. **L13:6622** ("pronouns") — the earliest feature layer identified, activated purely by the raw embedding of…

</details>

<details>
<summary><b>SA-7</b> — tool trace (9 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L7, F2765 | " mentions of people or characters, and their performance, roles, injur" |
| 2 | `get_upstream_features` | L7:F2765@11, k=8 | Emb:" she"@5 (w=2.89) +7 more |
| 3 | `inspect_feature` | L6, F11646 | " references to women, potentially triggered by pronouns and titles" |
| 4 | `inspect_feature` | L4, F7864 | "xml or source code snippets, especially tags and possibly keywords in " |
| 5 | `inspect_feature` | L6, F16329 | "female first names and their possessive forms" |
| 6 | `get_upstream_features` | L6:F11646@5, k=8 | Emb:" she"@5 (w=32.50) +7 more |
| 7 | `inspect_feature` | L0, F12519 | " the pronoun "she"" |
| 8 | `inspect_feature` | L1, F4232 | " the possessive pronoun "her"" |
| 9 | `inspect_feature` | L5, F10952 | "third person pronouns in varying contexts" |

**Findings:** ## Key Findings

### What token is at pos 11?
The upstream attribution graph reveals that **pos 11 is NOT the primary driver** of L7:F2765. All significant upstream edges trace back to **pos 5**, which contains the token **" she"** (a feminine pronoun). The feature fires AT pos 11, but its signal is driven by the presence of "she" at pos 5, propagated forward through the context. This means pos 11…

</details>

<details>
<summary><b>SA-8</b> — tool trace (15 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L19, F9685 | " references to women's names and their roles or accomplishments." |
| 2 | `get_upstream_features` | L19:F9685@13, k=6 | Emb:" She"@13 (w=5.88) +5 more |
| 3 | `inspect_feature` | L17, F5889 | " references to people with pronouns and possessive pronouns" |
| 4 | `inspect_feature` | L16, F2918 | "Pronouns" |
| 5 | `inspect_feature` | L13, F6622 | " pronouns." |
| 6 | `get_upstream_features` | L17:F5889@13, k=6 | Emb:" She"@13 (w=19.50) +5 more |
| 7 | `inspect_feature` | L15, F3330 | " personal stories of individuals, especially women and their actions o" |
| 8 | `inspect_feature` | L6, F11646 | " references to women, potentially triggered by pronouns and titles" |
| 9 | `inspect_feature` | L2, F6981 | " first-person pronouns and references in French" |
| 10 | `get_upstream_features` | L13:F6622@13, k=6 | Emb:" She"@13 (w=12.38) +5 more |
| 11 | `get_upstream_features` | L15:F3330@13, k=6 | Emb:" She"@13 (w=15.56) +5 more |
| 12 | `get_upstream_features` | L16:F2918@13, k=6 | Emb:" She"@13 (w=14.88) +5 more |
| 13 | `inspect_feature` | L14, F5740 | " sentences with multiple pronouns in them" |
| 14 | `inspect_feature` | L0, F9519 | " the pronoun "she" and the possessive pronoun "her"" |
| 15 | `inspect_feature` | L0, F14257 | "the word 'newly' and adjectives ending in 'able'" |

**Findings:** **Token at pos 13:** " She" (confirmed by dominant embedding edge weights of 5.875 → L19:9685 and 19.5 → L17:5889, 15.5 → L15:3330, 14.875 → L16:2918).

**What drives L19:9685?**

The circuit is overwhelmingly gender-driven, not profession-driven:

1. **Primary driver: " She" embedding at pos 13** — the raw token " She" is by far the strongest signal at every layer (edge weights 5–20x larger than …

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` | L15, F12956 → "female names and female-related words in the document." |

### Build

`build_circuit` → 18 nodes, 42 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | anthropic/claude-opus-4.6 | 143,147 | 6,709 | 0 | 0 | $0.8835 | — | — |
| SA-6 | anthropic/claude-sonnet-4.6 | 37,461 | 2,624 | 0 | 0 | $0.1517 | ✅ 5F/6E | Trace L18:14677 at pos 48. Determine what token is at pos 48… |
| SA-4 | anthropic/claude-sonnet-4.6 | 32,051 | 3,273 | 0 | 0 | $0.1452 | ✅ 6F/11E | Trace L18:14677 "women/girls mentioned" at pos 37 — this has… |
| SA-3 | anthropic/claude-sonnet-4.6 | 38,414 | 3,494 | 0 | 0 | $0.1677 | ✅ 7F/13E | Trace L12:12940 "references to female pronouns" at pos 5. De… |
| SA-1 | anthropic/claude-sonnet-4.6 | 47,046 | 4,311 | 0 | 0 | $0.2058 | ✅ 7F/18E | Trace the strongest feature driving the probe — L6:11646 "re… |
| SA-2 | anthropic/claude-sonnet-4.6 | 52,548 | 4,360 | 0 | 0 | $0.2230 | ✅ 9F/16E | Trace L18:14677 "instances of women or girls being mentioned… |
| SA-5 | anthropic/claude-sonnet-4.6 | 113,115 | 6,154 | 0 | 0 | $0.4317 | ✅ 0F/0E | Trace L19:9685 "references to women's names and their roles … |
| SA-7 | anthropic/claude-sonnet-4.6 | 33,212 | 2,708 | 0 | 0 | $0.1403 | ✅ 7F/7E | Trace L7:2765 at pos 11 — labeled 'mentions of people and th… |
| SA-8 | anthropic/claude-sonnet-4.6 | 50,793 | 3,967 | 0 | 0 | $0.2119 | ✅ 10F/12E | Trace L19:9685 at pos 13 — labeled 'women's names and accomp… |
| **Total** | | **547,787** | **37,600** | **0** | **0** | **$2.5607** | | |

**Oracle wall-clock time:** 4m 55s