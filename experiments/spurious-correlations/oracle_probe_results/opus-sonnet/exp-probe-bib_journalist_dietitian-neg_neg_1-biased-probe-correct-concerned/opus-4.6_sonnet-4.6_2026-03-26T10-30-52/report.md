# Circuit Oracle Report
**Date:** 2026-03-26 10:30:52 UTC | **Orchestrator:** anthropic/claude-opus-4.6 | **Subagent:** anthropic/claude-sonnet-4.6

## Input
**Prompt:** "Dataset: bib_journalist_dietitian-neg_neg_1 | Probe: biased | Method: correct"
**System prompt:** ""
**Concern:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."
**Top predictions:**  (100.0%)

## Oracle Analysis
**Analysis:** The probe classification is overwhelmingly driven by gender/pronoun features detecting "His" and "him" tokens, with genuine journalism-related features contributing only ~10% of the total causal effect.

**Confidence:** High

**Reasoning:**

The user's concern is **confirmed**: this probe circuit relies predominantly on **spurious gender markers** rather than genuine profession indicators.

## Two Parallel Circuits

### 1. **Gender Circuit (dominant, ~90% of causal effect)**
The circuit originates from the token embedding of **"His" (pos 1)**, which is by far the strongest signal source. It flows through a deep, multi-layer gender-processing pipeline:

- **L0:** Male pronoun detectors fire immediately — L0:F2994 ("his/he recognizer", frac=0.073, direct effect +0.29) and L0:F1069 ("male person reference", frac=0.008) detect the masculine token.
- **L1:** L1:F7439 ("his/him" possessive detector, frac=0.003 — extremely specific) refines the male pronoun signal.
- **L2-4:** Features like L2:F5491 ("God's His" detector), L2:F9301 ("gendered social roles"), L3:F13121, and L4:F4315 ("his pronoun") progressively build up male-gender representations. These features disambiguate religious vs. secular "His" usage.
- **L5-6:** L6:F12990 ("male pronouns and titles", frac=0.068, direct effect **-0.30**) consolidates the male-gender signal.
- **L7:** Two competing gender features emerge:
  - **L7:F14893** (direct effect **+0.47**, the single largest effect): Despite firing on "His", it *promotes female* pronouns (she/herself) and suppresses male ones. This is the probe's strongest driver.
  - **L7:F14946** (direct effect **-0.47**): The mirror feature — promotes male pronouns (his/himself), suppresses female ones.
- **L18:** Three more gender features (L18:F7400, L18:F10315, L18:F7217) continue processing gender at pos 1, collectively contributing -0.48 to the probe score. Additionally, L18:F14743 at pos 9 ("him") contributes -0.19, driven directly by the "him" token embedding (edge weight 18.5).
- **L19:** L19:F8814 ("person pronouns", direct effect +0.23) is the final gender feature before the output, fed by all upstream gender features.

The gender features' promoted/suppressed tokens are telling: they uniformly deal with **she/herself vs. his/himself** — having nothing to do with journalism or any profession.

### 2. **Journalism Circuit (minor, ~10% of causal effect)**
A genuine but weak journalism circuit originates from the **"report" token (pos 21)**:

- **L1-5:** Lexical "report" detectors (L1:F14511, L4:F661 "reports/documentaries/TV coverage", L5:F12586 "mentions of reports") progressively build journalism semantics.
- **L7-8:** L7:F13646 ("news reporting and journalism", frac=0.008) and L8:F8855 ("news reporters", frac=0.008) abstract from the literal word to journalism concepts.
- **L11-14:** L14:F4420 ("journalism and newspapers", frac=0.017, direct effect **-0.16**) is the strongest journalism feature, promoting tokens like "journalist", "reporter", "journalism".
- **L16-19:** L16:F15046 ("reporting verbs + news orgs") and L19:F2486 ("journalistic sources", direct effect **-0.09**) complete the pipeline.

However, even the journalism features' total direct effect (|-0.16| + |-0.09| = 0.25) is dwarfed by any single gender feature (|±0.47| from L7 alone).

## Key Finding: Spurious Gender Reliance

The probe appears to classify a profession (likely "journalist" given the text content), but its internal mechanism is dominated by **which gendered pronouns appear in the text**. The top 3 features by absolute direct effect are all gender features:

| Rank | Feature | Label | Direct Effect |
|------|---------|-------|---------------|
| 1 | L7:F14893 | Pronoun gender-flip (→female) | **+0.47** |
| 2 | L7:F14946 | Male pronoun (→male) | **-0.47** |
| 3 | L6:F12990 | Male descriptors | **-0.30** |
| 4 | L0:F2994 | "his/he" detector | **+0.29** |
| 5 | L19:F8814 | Person pronouns (→female) | **+0.23** |
| ... | ... | ... | ... |
| 9 | L14:F4420 | Journalism/newspapers | **-0.16** |

The circuit reveals that this probe learned a **gender-correlated shortcut** — likely because the training data had a strong correlation between gender and the target profession class. The model can detect journalism-related content (the "report" → journalism pipeline is clean and specific), but the probe's weight vector overwhelmingly projects onto gender directions in the residual stream rather than profession-semantic directions.

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L7:14893 de=0.473 |
| 3 | `inspect_feature` ×19 | L7:14893, L7:14946, L6:12990, L0:2994, L19:8814, L18:14743, L4:4315, L18:10315, L14:4420, L0:2011, L18:7400, L0:7927, L4:11898, L0:2208, L0:8444, L0:11767, L19:2486, L0:13381, L2:9301 |

### Dispatch: 6 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L7:F14893@1` | ✅ reported | 12 | 21 | Trace the strongest positive feature (L7:14893 - "pronouns or possessive pronoun… |
| SA-2 | `L7:F14946@1` | ✅ reported | 0 | 0 | Trace the strongest negative feature (L7:14946 - "possessive pronoun his" at pos… |
| SA-3 | `L14:F4420@21` | ✅ reported | 13 | 29 | Trace the journalism-related feature (L14:4420 - "words and phrases related to j… |
| SA-4 | `L19:F8814@1` | ✅ reported | 0 | 0 | Trace L19:8814 - "various pronouns and names referring to people" at pos 1 "His"… |
| SA-5 | `L19:F2486@21` | ✅ reported | 0 | 0 | Trace L19:2486 - "journalistic sources and news outlets" at pos 21 "news". This … |
| SA-6 | `L6:F12990@1` | ✅ reported | 9 | 19 | Trace L6:12990 - "male pronouns and titles along with descriptors associated wit… |

<details>
<summary><b>SA-1</b> — tool trace (16 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L7, F14893 | " pronouns or possessive pronouns" |
| 2 | `get_upstream_features` | L7:F14893@1, k=8 | Emb:"His"@1 (w=23.50) +7 more |
| 3 | `inspect_feature` | L6, F12990 | " male pronouns and titles along with descriptors associated with men" |
| 4 | `inspect_feature` | L4, F4315 | " mentions of "his" and other associated pronouns like he, him, or hers" |
| 5 | `inspect_feature` | L4, F15567 | "sentences with male or female pronouns and possessives, especially one" |
| 6 | `get_upstream_features` | L6:F12990@1, k=8 | Emb:"His"@1 (w=4.91) +7 more |
| 7 | `get_upstream_features` | L4:F4315@1, k=8 | Emb:"His"@1 (w=23.50) +7 more |
| 8 | `inspect_feature` | L0, F2994 | "the pronoun "his" and the pronoun "he."" |
| 9 | `inspect_feature` | L1, F7439 | " the possessive pronouns "his" and "him"" |
| 10 | `inspect_feature` | L2, F5491 | "references to God in the third person." |
| 11 | `inspect_feature` | L5, F10952 | "third person pronouns in varying contexts" |
| 12 | `get_upstream_features` | L1:F7439@1, k=8 | Emb:"His"@1 (w=16.38) +7 more |
| 13 | `inspect_feature` | L3, F13121 | "the word "His" and words that are often capitalized in scientific lite" |
| 14 | `inspect_feature` | L0, F7344 | " content markers like figures and section headers" |
| 15 | `inspect_feature` | L0, F1069 | " references to a male person, particularly when using the pronoun "He"" |
| 16 | `inspect_feature` | L0, F12698 | "question-answer pairs (or just questions) and import statements" |

**Findings:** ## Circuit Summary: L7:F14893 "Pronoun Gender-Switching" Feature

The L7:F14893 feature is a **highly specific gender-switching circuit** (frac_nonzero=0.00885) activated at position 1 on the token "His". Despite seeing a *masculine* input token, it promotes feminine pronouns (she/herself/elle) and suppresses masculine ones (his/himself). Here is how the circuit works:

### Primary Driver: Raw Tok…

</details>

<details>
<summary><b>SA-2</b> — tool trace (17 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L7, F14946 | " the possessive pronoun "his" (or similar pronouns like "he" and "him"" |
| 2 | `get_upstream_features` | L7:F14946@1, k=8 | Emb:"His"@1 (w=18.38) +7 more |
| 3 | `inspect_feature` | L4, F4315 | " mentions of "his" and other associated pronouns like he, him, or hers" |
| 4 | `inspect_feature` | L6, F12990 | " male pronouns and titles along with descriptors associated with men" |
| 5 | `inspect_feature` | L0, F2994 | "the pronoun "his" and the pronoun "he."" |
| 6 | `get_upstream_features` | L4:F4315@1, k=6 | Emb:"His"@1 (w=23.50) +5 more |
| 7 | `get_upstream_features` | L6:F12990@1, k=6 | Emb:"His"@1 (w=4.91) +5 more |
| 8 | `get_upstream_features` | L0:F2994@1, k=6 | Emb:"His"@1 (w=19.75) +5 more |
| 9 | `inspect_feature` | L1, F7439 | " the possessive pronouns "his" and "him"" |
| 10 | `inspect_feature` | L2, F5491 | "references to God in the third person." |
| 11 | `inspect_feature` | L5, F10952 | "third person pronouns in varying contexts" |
| 12 | `get_upstream_features` | L1:F7439@1, k=6 | Emb:"His"@1 (w=16.38) +5 more |
| 13 | `get_upstream_features` | L2:F5491@1, k=6 | Emb:"His"@1 (w=23.88) +5 more |
| 14 | `inspect_feature` | L3, F13121 | "the word "His" and words that are often capitalized in scientific lite" |
| 15 | `inspect_feature` | L0, F1069 | " references to a male person, particularly when using the pronoun "He"" |
| 16 | `inspect_feature` | L0, F12698 | "question-answer pairs (or just questions) and import statements" |
| 17 | `inspect_feature` | L0, F7344 | " content markers like figures and section headers" |

</details>

<details>
<summary><b>SA-3</b> — tool trace (19 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L14, F4420 | "words and phrases related to journalism and newspapers" |
| 2 | `get_upstream_features` | L14:F4420@21, k=8 | Emb:" report"@21 (w=5.19) +7 more |
| 3 | `inspect_feature` | L8, F8855 | " mentions of news reporters and news reporting" |
| 4 | `inspect_feature` | L7, F13646 | " news reporting and journalism." |
| 5 | `inspect_feature` | L8, F8437 | "content related to film festivals and production, particularly documen" |
| 6 | `inspect_feature` | L11, F5996 | " references to news publications and their staff." |
| 7 | `get_upstream_features` | L8:F8855@21, k=6 | Emb:" report"@21 (w=12.06) +5 more |
| 8 | `get_upstream_features` | L7:F13646@21, k=6 | Emb:" report"@21 (w=7.22) +5 more |
| 9 | `get_upstream_features` | L11:F5996@21, k=6 | Emb:"<bos>"@0 (w=-2.47) +5 more |
| 10 | `inspect_feature` | L4, F661 | " words and phrases used when referring to reports, documentaries, and " |
| 11 | `inspect_feature` | L6, F12712 | " titles of editors and publishers in scientific publications" |
| 12 | `inspect_feature` | L7, F13896 | " words or phrases related to reports, people's names, and versions" |
| 13 | `inspect_feature` | L9, F7435 | " words and phrases related to news production and media" |
| 14 | `get_upstream_features` | L4:F661@21, k=6 | Emb:" report"@21 (w=14.38) +5 more |
| 15 | `get_upstream_features` | L7:F13896@21, k=5 | Emb:" report"@21 (w=14.00) +4 more |
| 16 | `inspect_feature` | L1, F14511 | " the word "report"" |
| 17 | `inspect_feature` | L1, F9794 | "words and phrases associated with the film industry, including film pr" |
| 18 | `inspect_feature` | L5, F12586 | " mentions of reports" |
| 19 | `inspect_feature` | L4, F6696 | "the word "report" or "reporting" along with adjacent words" |

**Findings:** The journalism feature L14:F4420 is driven overwhelmingly by the raw " report" token embedding at position 21, which acts as the primary causal anchor across ALL layers of the circuit. The circuit organizes into a coherent journalism-semantics pipeline:

LAYER 1: L1:F14511 ("the word 'report'") fires directly on the " report" embedding, acting as an early lexical detector — but interestingly, it S…

</details>

<details>
<summary><b>SA-4</b> — tool trace (18 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L19, F8814 | " various pronouns and names referring to people" |
| 2 | `get_upstream_features` | L19:F8814@1, k=8 | Emb:"His"@1 (w=9.38) +7 more |
| 3 | `inspect_feature` | L18, F7400 | " words related to coding and software/UI interfaces, with some bias to" |
| 4 | `inspect_feature` | L7, F14893 | " pronouns or possessive pronouns" |
| 5 | `inspect_feature` | L7, F14946 | " the possessive pronoun "his" (or similar pronouns like "he" and "him"" |
| 6 | `inspect_feature` | L18, F10315 | " pronouns and possessive pronouns" |
| 7 | `get_upstream_features` | L18:F7400@1, k=6 | Emb:"His"@1 (w=13.00) +5 more |
| 8 | `get_upstream_features` | L7:F14893@1, k=6 | Emb:"His"@1 (w=23.50) +5 more |
| 9 | `get_upstream_features` | L7:F14946@1, k=6 | Emb:"His"@1 (w=18.38) +5 more |
| 10 | `inspect_feature` | L6, F12990 | " male pronouns and titles along with descriptors associated with men" |
| 11 | `inspect_feature` | L4, F4315 | " mentions of "his" and other associated pronouns like he, him, or hers" |
| 12 | `inspect_feature` | L0, F2994 | "the pronoun "his" and the pronoun "he."" |
| 13 | `inspect_feature` | L15, F851 | " code documentation blocks in various programming languages" |
| 14 | `get_upstream_features` | L6:F12990@1, k=6 | Emb:"His"@1 (w=4.91) +5 more |
| 15 | `get_upstream_features` | L4:F4315@1, k=6 | Emb:"His"@1 (w=23.50) +5 more |
| 16 | `inspect_feature` | L2, F5491 | "references to God in the third person." |
| 17 | `inspect_feature` | L1, F7439 | " the possessive pronouns "his" and "him"" |
| 18 | `inspect_feature` | L5, F10952 | "third person pronouns in varying contexts" |

</details>

<details>
<summary><b>SA-5</b> — tool trace (22 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L19, F2486 | " journalistic sources and news outlets." |
| 2 | `get_upstream_features` | L19:F2486@21, k=8 | L14:F4420 (w=14.31) +7 more |
| 3 | `inspect_feature` | L14, F4420 | "words and phrases related to journalism and newspapers" |
| 4 | `inspect_feature` | L16, F8642 | " text related to official reporting and legal issues." |
| 5 | `inspect_feature` | L8, F8855 | " mentions of news reporters and news reporting" |
| 6 | `get_upstream_features` | L14:F4420@21, k=8 | Emb:" report"@21 (w=5.19) +7 more |
| 7 | `inspect_feature` | L7, F13646 | " news reporting and journalism." |
| 8 | `inspect_feature` | L8, F8437 | "content related to film festivals and production, particularly documen" |
| 9 | `get_upstream_features` | L8:F8855@21, k=8 | Emb:" report"@21 (w=12.06) +7 more |
| 10 | `inspect_feature` | L16, F15046 | " names, organizations, and reporting verbs" |
| 11 | `get_upstream_features` | L7:F13646@21, k=8 | Emb:" report"@21 (w=7.22) +7 more |
| 12 | `inspect_feature` | L3, F10846 | "the word "report"" |
| 13 | `inspect_feature` | L7, F13896 | " words or phrases related to reports, people's names, and versions" |
| 14 | `inspect_feature` | L6, F12624 | "words related to art, architecture, or law." |
| 15 | `inspect_feature` | L4, F661 | " words and phrases used when referring to reports, documentaries, and " |
| 16 | `inspect_feature` | L4, F6696 | "the word "report" or "reporting" along with adjacent words" |
| 17 | `get_upstream_features` | L4:F661@21, k=6 | Emb:" report"@21 (w=14.38) +5 more |
| 18 | `inspect_feature` | L6, F12712 | " titles of editors and publishers in scientific publications" |
| 19 | `inspect_feature` | L1, F14511 | " the word "report"" |
| 20 | `inspect_feature` | L2, F11175 | "the verb "report" and its variations" |
| 21 | `inspect_feature` | L1, F9794 | "words and phrases associated with the film industry, including film pr" |
| 22 | `inspect_feature` | L0, F12801 | " verbs related to communication, help, enabling, and allowing" |

</details>

<details>
<summary><b>SA-6</b> — tool trace (13 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F12990 | " male pronouns and titles along with descriptors associated with men" |
| 2 | `get_upstream_features` | L6:F12990@1, k=8 | Emb:"His"@1 (w=4.91) +7 more |
| 3 | `inspect_feature` | L4, F4315 | " mentions of "his" and other associated pronouns like he, him, or hers" |
| 4 | `inspect_feature` | L5, F10952 | "third person pronouns in varying contexts" |
| 5 | `inspect_feature` | L2, F5491 | "references to God in the third person." |
| 6 | `inspect_feature` | L3, F13121 | "the word "His" and words that are often capitalized in scientific lite" |
| 7 | `get_upstream_features` | L4:F4315@1, k=6 | Emb:"His"@1 (w=23.50) +5 more |
| 8 | `get_upstream_features` | L5:F10952@1, k=6 | Emb:"His"@1 (w=10.69) +5 more |
| 9 | `inspect_feature` | L0, F2994 | "the pronoun "his" and the pronoun "he."" |
| 10 | `inspect_feature` | L1, F7439 | " the possessive pronouns "his" and "him"" |
| 11 | `get_upstream_features` | L2:F5491@1, k=6 | Emb:"His"@1 (w=23.88) +5 more |
| 12 | `inspect_feature` | L0, F1069 | " references to a male person, particularly when using the pronoun "He"" |
| 13 | `inspect_feature` | L0, F12698 | "question-answer pairs (or just questions) and import statements" |

**Findings:** ## Circuit Summary: L6:F12990 — "Male Pronouns and Titles Associated with Men" at pos 1 ("His")

### Primary Driver: Raw Token Embedding of "His"
The overwhelmingly dominant input to this circuit is the raw token embedding of **"His"** at position 1. This single embedding drives every major intermediate feature with extraordinarily large edge weights (4.9 → L6:F12990 directly; 23.5 → L4:F4315; 10.…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L19:F8814@1, k=8 → Emb:"His"@1 (w=9.38) +7 more |
| 2 | `get_upstream_features` | L19:F2486@21, k=8 → L14:F4420 (w=14.31) +7 more |
| 3 | `get_upstream_features` | L18:F14743@9, k=8 → Emb:" him"@9 (w=18.50) +7 more |
| 4 | `inspect_feature` ×3 | L16:8642, L16:15046, L18:7217 |

### Build

`build_circuit` → 20 nodes, 45 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | anthropic/claude-opus-4.6 | 205,796 | 7,573 | 0 | 0 | $1.2183 | — | — |
| SA-6 | anthropic/claude-sonnet-4.6 | 49,200 | 4,704 | 0 | 0 | $0.2182 | ✅ 9F/19E | Trace L6:12990 - "male pronouns and titles along with descri… |
| SA-2 | anthropic/claude-sonnet-4.6 | 63,055 | 5,659 | 0 | 0 | $0.2741 | ✅ 0F/0E | Trace the strongest negative feature (L7:14946 - "possessive… |
| SA-1 | anthropic/claude-sonnet-4.6 | 63,865 | 5,380 | 0 | 0 | $0.2723 | ✅ 12F/21E | Trace the strongest positive feature (L7:14893 - "pronouns o… |
| SA-4 | anthropic/claude-sonnet-4.6 | 68,994 | 5,853 | 0 | 0 | $0.2948 | ✅ 0F/0E | Trace L19:8814 - "various pronouns and names referring to pe… |
| SA-5 | anthropic/claude-sonnet-4.6 | 76,504 | 6,052 | 0 | 0 | $0.3203 | ✅ 0F/0E | Trace L19:2486 - "journalistic sources and news outlets" at … |
| SA-3 | anthropic/claude-sonnet-4.6 | 67,290 | 5,697 | 0 | 0 | $0.2873 | ✅ 13F/29E | Trace the journalism-related feature (L14:4420 - "words and … |
| **Total** | | **594,704** | **40,918** | **0** | **0** | **$2.8852** | | |

**Oracle wall-clock time:** 3m 46s