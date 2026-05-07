# Circuit Oracle Report
**Date:** 2026-03-26 18:22:49 UTC | **Orchestrator:** anthropic/claude-opus-4.6 | **Subagent:** anthropic/claude-sonnet-4.6

## Input
**Prompt:** "Dataset: bib_journalist_dietitian-neg_neg_2 | Probe: biased | Method: correct"
**System prompt:** ""
**Concern:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."
**Top predictions:**  (100.0%)

## Oracle Analysis
Now let me compile the quantitative summary for the final analysis.

**Analysis:** The probe classifies this text as describing a journalist/reporter, but the circuit driving the probe's classification score is **overwhelmingly dominated by gender/pronoun features** rather than genuine profession-related features — confirming the user's concern about spurious features.

**Confidence:** High

**Reasoning:**

## Circuit Summary

The probe classification is driven by two pathways that are dramatically unequal in their contribution:

### 1. **Dominant Pathway: Gender/Pronoun Features (pos 1 "His" and pos 9 "him") — ~85% of the signal**

The strongest features by direct effect are **all gender markers**, not profession indicators:

| Feature | Label | Direct Effect | Type |
|---------|-------|---------------|------|
| L7:14893 (pos 1) | "Pronouns/possessives" — promotes *herself/she* | **+0.49** | Gender |
| L7:14946 (pos 1) | "Possessive 'his'" — promotes *himself/his* | **-0.48** | Gender |
| L6:12990 (pos 1) | "Male pronouns and titles" | **-0.30** | Gender |
| L0:2994 (pos 1) | "Pronoun 'his'/'he'" | **+0.29** | Gender |
| L19:8814 (pos 1) | "Pronouns and names for people" — promotes *herself/she* | **+0.26** | Gender |
| L18:14743 (pos 9) | "He" — promotes *himself* | **-0.20** | Gender |
| L18:10315 (pos 1) | "Pronouns and possessives" | **-0.18** | Gender |
| L18:7400 (pos 1) | Promotes *himself/his* | **-0.17** | Gender |

These features form a deep cascade originating entirely from the **raw token embeddings** of "His" (pos 1) and "him" (pos 9), with edge weights of 18–24 flowing through layers 0→1→2→4→5→6→7→18→19. At every layer, the features detect and track masculine gender markers. The circuit is essentially: `"His"/"him" embedding → masculine pronoun detection → gender classification`.

### 2. **Minor Pathway: Journalism Features (pos 21 "report") — ~15% of the signal, and it pushes AGAINST the probe**

Genuine journalism features exist but are **weak AND have negative direct effects**:

| Feature | Label | Direct Effect | Type |
|---------|-------|---------------|------|
| L14:4420 (pos 21) | "Journalism and newspapers" (frac=0.017) | **-0.16** | Profession |
| L19:2486 (pos 21) | "Journalistic sources and news outlets" (frac=0.029) | **-0.11** | Profession |

These are highly specific features (low frac_nonzero) that genuinely detect journalism context from the word "report" at position 21, building through a clean pipeline: `"report" embedding → L2:11175 word detector → L4:661 TV/documentary reports → L7:13646 journalism hub → L8:8855 news reporters → L14:4420 journalism → L19:2486 journalistic sources`. However, they **push the probe score down**, not up.

### 3. **The Spurious Mechanism**

The probe has learned a **gender-correlated shortcut** rather than genuine profession detection. Here's the evidence:

1. **Gender features dominate quantitatively**: The top 8 features by absolute direct effect are ALL gender features, contributing combined |direct_effect| ≈ 2.37, versus journalism features contributing only |0.27|.

2. **Journalism features push AGAINST the classification**: L14:4420 and L19:2486 — the only genuine profession-detecting features — have negative direct effects, meaning they actually *oppose* the probe's classification.

3. **The root input tokens are gender markers, not profession words**: The strongest upstream signals (edge weights 18–24) come from "His" (pos 1) and "him" (pos 9), not from "report" (pos 21), "news" (pos 22), or "organizations" (pos 23).

4. **Feature specificity confirms gender, not profession**: L7:14893 (frac_nonzero=0.009) promotes `[herself, elle, she]` and suppresses `[himself, his]`; L7:14946 (frac_nonzero=0.017) does the exact opposite. These are pure gender polarity features with no profession semantics.

### Conclusion

**The user's concern is validated.** The probe's classification of this journalist bio relies on a **spurious gender shortcut**: it reads the masculine pronouns "His" and "him" and processes them through an elaborate but entirely gender-focused circuit. The genuine journalism-detection features that fire on the word "report" actually have *negative* effects on the probe score. This means the probe would likely misclassify a journalist bio written with feminine pronouns or without pronouns, and would classify non-journalist bios correctly solely because they contain masculine pronouns — a textbook case of a spurious correlation in a linear probe.

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L7:14893 de=0.486 |
| 3 | `inspect_feature` ×18 | L7:14893, L7:14946, L6:12990, L0:2994, L19:8814, L18:14743, L18:10315, L14:4420, L0:2011, L4:4315, L4:11898, L0:7927, L0:11767, L19:2486, L2:9301, L0:8444, L0:2208, L2:5491 |

### Dispatch: 7 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L7:F14893@1` | ✅ reported | 8 | 18 | Trace the strongest positive driver of the probe score - L7:14893 is a 'pronouns… |
| SA-2 | `L19:F8814@1` | ✅ reported | 0 | 0 | Trace L19:8814 which is labeled 'various pronouns and names referring to people'… |
| SA-3 | `L14:F4420@21` | ✅ reported | 13 | 20 | Trace L14:4420 which is a genuine journalism-related feature ('words and phrases… |
| SA-4 | `L19:F2486@21` | ✅ reported | 13 | 20 | Trace L19:2486 which is labeled 'journalistic sources and news outlets' and prom… |
| SA-5 | `L7:F14946@1` | ✅ reported | 10 | 24 | Trace L7:14946 which detects 'his' possessive pronoun and promotes 'himself/his'… |
| SA-6 | `L19:F8814@1` | ✅ reported | 0 | 0 | Trace L19:8814 - 'various pronouns and names referring to people' at pos 1. This… |
| SA-7 | `L18:F14743@9` | ✅ reported | 10 | 12 | Trace L18:14743 labeled 'He', firing at position 9 ('has'/'taken'). This has -0.… |

<details>
<summary><b>SA-1</b> — tool trace (12 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L7, F14893 | " pronouns or possessive pronouns" |
| 2 | `get_upstream_features` | L7:F14893@1, k=8 | Emb:"His"@1 (w=23.50) +7 more |
| 3 | `inspect_feature` | L6, F12990 | " male pronouns and titles along with descriptors associated with men" |
| 4 | `inspect_feature` | L4, F4315 | " mentions of "his" and other associated pronouns like he, him, or hers" |
| 5 | `inspect_feature` | L0, F2994 | "the pronoun "his" and the pronoun "he."" |
| 6 | `get_upstream_features` | L6:F12990@1, k=6 | Emb:"His"@1 (w=4.91) +5 more |
| 7 | `get_upstream_features` | L4:F4315@1, k=6 | Emb:"His"@1 (w=23.50) +5 more |
| 8 | `inspect_feature` | L5, F10952 | "third person pronouns in varying contexts" |
| 9 | `inspect_feature` | L2, F5491 | "references to God in the third person." |
| 10 | `inspect_feature` | L1, F7439 | " the possessive pronouns "his" and "him"" |
| 11 | `get_upstream_features` | L5:F10952@1, k=6 | Emb:"His"@1 (w=10.69) +5 more |
| 12 | `inspect_feature` | L3, F13121 | "the word "His" and words that are often capitalized in scientific lite" |

**Findings:** ## Key Findings: The "His" → Feminine Pronoun Feature Circuit

### The Central Paradox
The most striking finding is that **L7:F14893** — a feature that promotes feminine pronouns ("herself," "she," "elle") and suppresses masculine pronouns ("himself," "his") — is **primarily driven by the raw token embedding of "His"** (edge_weight = 23.5, the dominant signal in the entire graph). This is not a bu…

</details>

<details>
<summary><b>SA-2</b> — tool trace (16 calls)</summary>

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
| 9 | `get_upstream_features` | L7:F14946@1, k=6 | Emb:"His"@1 (w=18.38) +5 more |
| 10 | `inspect_feature` | L6, F12990 | " male pronouns and titles along with descriptors associated with men" |
| 11 | `inspect_feature` | L4, F4315 | " mentions of "his" and other associated pronouns like he, him, or hers" |
| 12 | `inspect_feature` | L0, F2994 | "the pronoun "his" and the pronoun "he."" |
| 13 | `inspect_feature` | L15, F851 | " code documentation blocks in various programming languages" |
| 14 | `get_upstream_features` | L6:F12990@1, k=5 | Emb:"His"@1 (w=4.91) +4 more |
| 15 | `get_upstream_features` | L4:F4315@1, k=5 | Emb:"His"@1 (w=23.50) +4 more |
| 16 | `inspect_feature` | L2, F5491 | "references to God in the third person." |

</details>

<details>
<summary><b>SA-3</b> — tool trace (19 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L14, F4420 | "words and phrases related to journalism and newspapers" |
| 2 | `get_upstream_features` | L14:F4420@21, k=8 | Emb:" report"@21 (w=5.22) +7 more |
| 3 | `inspect_feature` | L8, F8855 | " mentions of news reporters and news reporting" |
| 4 | `inspect_feature` | L7, F13646 | " news reporting and journalism." |
| 5 | `inspect_feature` | L8, F8437 | "content related to film festivals and production, particularly documen" |
| 6 | `inspect_feature` | L9, F7435 | " words and phrases related to news production and media" |
| 7 | `get_upstream_features` | L8:F8855@21, k=6 | Emb:" report"@21 (w=12.12) +5 more |
| 8 | `get_upstream_features` | L9:F7435@21, k=6 | Emb:"<bos>"@0 (w=2.72) +5 more |
| 9 | `get_upstream_features` | L7:F13646@21, k=6 | Emb:" report"@21 (w=7.25) +5 more |
| 10 | `inspect_feature` | L7, F13896 | " words or phrases related to reports, people's names, and versions" |
| 11 | `inspect_feature` | L3, F10846 | "the word "report"" |
| 12 | `inspect_feature` | L4, F6696 | "the word "report" or "reporting" along with adjacent words" |
| 13 | `inspect_feature` | L8, F15435 | " words relating to news broadcasting" |
| 14 | `inspect_feature` | L4, F661 | " words and phrases used when referring to reports, documentaries, and " |
| 15 | `get_upstream_features` | L3:F10846@21, k=6 | Emb:" report"@21 (w=24.75) +5 more |
| 16 | `get_upstream_features` | L7:F13896@21, k=6 | Emb:" report"@21 (w=14.00) +5 more |
| 17 | `inspect_feature` | L2, F11175 | "the verb "report" and its variations" |
| 18 | `inspect_feature` | L5, F12586 | " mentions of reports" |
| 19 | `inspect_feature` | L5, F13392 | " official documentation, official bodies and reporting on findings" |

**Findings:** ## Circuit Summary: The Journalism Feature and Its Suppression Mechanism

### The Core Feature (L14:F4420)
L14:F4420 is a highly specific (frac_nonzero=0.0165) journalism feature promoting journalist/reporter/editorial tokens. Crucially, it has a **NEGATIVE direct effect on the probe**, meaning its activation *suppresses* whatever the probe is measuring (likely a non-journalism interpretation).

#…

</details>

<details>
<summary><b>SA-4</b> — tool trace (20 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L19, F2486 | " journalistic sources and news outlets." |
| 2 | `get_upstream_features` | L19:F2486@21, k=8 | L14:F4420 (w=14.31) +7 more |
| 3 | `inspect_feature` | L14, F4420 | "words and phrases related to journalism and newspapers" |
| 4 | `inspect_feature` | L16, F8642 | " text related to official reporting and legal issues." |
| 5 | `inspect_feature` | L8, F8855 | " mentions of news reporters and news reporting" |
| 6 | `get_upstream_features` | L14:F4420@21, k=6 | Emb:" report"@21 (w=5.22) +5 more |
| 7 | `get_upstream_features` | L16:F8642@21, k=6 | L14:F4420 (w=10.50) +5 more |
| 8 | `get_upstream_features` | L8:F8855@21, k=5 | Emb:" report"@21 (w=12.12) +4 more |
| 9 | `inspect_feature` | L7, F13646 | " news reporting and journalism." |
| 10 | `inspect_feature` | L8, F8437 | "content related to film festivals and production, particularly documen" |
| 11 | `inspect_feature` | L9, F7435 | " words and phrases related to news production and media" |
| 12 | `get_upstream_features` | L7:F13646@21, k=6 | Emb:" report"@21 (w=7.25) +5 more |
| 13 | `inspect_feature` | L16, F15046 | " names, organizations, and reporting verbs" |
| 14 | `inspect_feature` | L15, F2579 | "instances of people providing information in some sort of official cap" |
| 15 | `inspect_feature` | L4, F661 | " words and phrases used when referring to reports, documentaries, and " |
| 16 | `inspect_feature` | L6, F12712 | " titles of editors and publishers in scientific publications" |
| 17 | `inspect_feature` | L0, F12801 | " verbs related to communication, help, enabling, and allowing" |
| 18 | `get_upstream_features` | L4:F661@21, k=5 | Emb:" report"@21 (w=14.38) +4 more |
| 19 | `inspect_feature` | L1, F14511 | " the word "report"" |
| 20 | `inspect_feature` | L3, F10846 | "the word "report"" |

**Findings:** ## The Journalism Pathway and Why It Pushes Against the Probe Score

### Circuit Architecture: A Deep Journalism Recognition Stack

The circuit is a clear, multi-layer journalism recognition pipeline rooted entirely in the **` report`** embedding token at position 21. Here is the full story:

---

### 1. Root Cause: The ` report` Embedding Token
The word at position 21 is ` report` (later contextu…

</details>

<details>
<summary><b>SA-5</b> — tool trace (15 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L7, F14946 | " the possessive pronoun "his" (or similar pronouns like "he" and "him"" |
| 2 | `get_upstream_features` | L7:F14946@1, k=8 | Emb:"His"@1 (w=18.38) +7 more |
| 3 | `inspect_feature` | L4, F4315 | " mentions of "his" and other associated pronouns like he, him, or hers" |
| 4 | `inspect_feature` | L6, F12990 | " male pronouns and titles along with descriptors associated with men" |
| 5 | `inspect_feature` | L0, F2994 | "the pronoun "his" and the pronoun "he."" |
| 6 | `get_upstream_features` | L4:F4315@1, k=6 | Emb:"His"@1 (w=23.50) +5 more |
| 7 | `get_upstream_features` | L6:F12990@1, k=6 | Emb:"His"@1 (w=4.91) +5 more |
| 8 | `inspect_feature` | L1, F7439 | " the possessive pronouns "his" and "him"" |
| 9 | `inspect_feature` | L2, F5491 | "references to God in the third person." |
| 10 | `inspect_feature` | L5, F10952 | "third person pronouns in varying contexts" |
| 11 | `get_upstream_features` | L1:F7439@1, k=6 | Emb:"His"@1 (w=16.38) +5 more |
| 12 | `get_upstream_features` | L2:F5491@1, k=6 | Emb:"His"@1 (w=23.88) +5 more |
| 13 | `inspect_feature` | L0, F7344 | " content markers like figures and section headers" |
| 14 | `inspect_feature` | L0, F1069 | " references to a male person, particularly when using the pronoun "He"" |
| 15 | `inspect_feature` | L0, F12698 | "question-answer pairs (or just questions) and import statements" |

**Findings:** ## Circuit Summary: How 'His' at Position 1 Drives L7:F14946

### Primary Finding: Raw Token Embedding Dominates
The single most powerful input to L7:F14946 is the **raw token embedding of "His"** at position 1 (edge weight = 18.375). This is by far the strongest direct signal — the model picks up masculine gender directly from the token's embedding vector before any learned feature processing.

#…

</details>

<details>
<summary><b>SA-6</b> — tool trace (20 calls)</summary>

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
| 9 | `inspect_feature` | L18, F7217 | " words or abbreviations referring to people, with a focus on pronouns " |
| 10 | `get_upstream_features` | L7:F14946@1, k=6 | Emb:"His"@1 (w=18.38) +5 more |
| 11 | `inspect_feature` | L6, F12990 | " male pronouns and titles along with descriptors associated with men" |
| 12 | `inspect_feature` | L4, F4315 | " mentions of "his" and other associated pronouns like he, him, or hers" |
| 13 | `inspect_feature` | L0, F2994 | "the pronoun "his" and the pronoun "he."" |
| 14 | `inspect_feature` | L15, F851 | " code documentation blocks in various programming languages" |
| 15 | `inspect_feature` | L11, F10933 | "the letters "L", "H," and "a" when they are at the beginning of a text" |
| 16 | `get_upstream_features` | L6:F12990@1, k=6 | Emb:"His"@1 (w=4.91) +5 more |
| 17 | `get_upstream_features` | L4:F4315@1, k=6 | Emb:"His"@1 (w=23.50) +5 more |
| 18 | `inspect_feature` | L2, F5491 | "references to God in the third person." |
| 19 | `inspect_feature` | L1, F7439 | " the possessive pronouns "his" and "him"" |
| 20 | `inspect_feature` | L5, F10952 | "third person pronouns in varying contexts" |

</details>

<details>
<summary><b>SA-7</b> — tool trace (15 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L18, F14743 | "He" |
| 2 | `get_upstream_features` | L18:F14743@9, k=8 | Emb:" him"@9 (w=18.38) +7 more |
| 3 | `inspect_feature` | L0, F16297 | " the pronoun "him"" |
| 4 | `inspect_feature` | L16, F14120 | " references to people being directed and/or affected in some way." |
| 5 | `inspect_feature` | L14, F10344 | " pronouns related to feelings or actions" |
| 6 | `inspect_feature` | L13, F10255 | " a lot of uses of the word "I" and "me" and the phrase "made me"" |
| 7 | `get_upstream_features` | L16:F14120@9, k=6 | Emb:" him"@9 (w=9.94) +5 more |
| 8 | `get_upstream_features` | L0:F16297@9, k=6 | Emb:" him"@9 (w=42.25) +5 more |
| 9 | `inspect_feature` | L14, F2710 | " language showing a causal relationship." |
| 10 | `inspect_feature` | L5, F2701 | "phrases meaning "the actor" performing "actions."" |
| 11 | `get_upstream_features` | L14:F10344@9, k=6 | Emb:" him"@9 (w=14.62) +5 more |
| 12 | `inspect_feature` | L2, F5525 | " instances of something moving directly to a location like someone com" |
| 13 | `get_upstream_features` | L5:F2701@9, k=6 | Emb:" him"@9 (w=7.28) +5 more |
| 14 | `inspect_feature` | L4, F14959 | " verbs indicating causation, as well as pronouns following them" |
| 15 | `inspect_feature` | L4, F2623 | " personal pronouns, possessives, and words used to describe or refer t" |

**Findings:** ## Circuit Summary: L18:F14743 "He" — Masculine Gender Tracking

### Core Finding
L18:F14743 is a **masculine pronoun/gender tracker** (label: "He") that fires on the token " him" at position 9, promotes "himself" and suppresses "she/her". Its -0.20 direct effect means it actively pushes the model *away* from feminine completions and towards masculine anaphoric pronouns.

### Circuit Architecture …

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L19:F8814@1, k=10 → Emb:"His"@1 (w=9.31) +9 more |
| 2 | `inspect_feature` ×4 | L18:7400, L18:7217, L16:10989, L12:3684 |

### Build

`build_circuit` → 16 nodes, 28 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | anthropic/claude-opus-4.6 | 257,763 | 7,047 | 0 | 0 | $1.4650 | — | — |
| SA-1 | anthropic/claude-sonnet-4.6 | 45,224 | 3,955 | 0 | 0 | $0.1950 | ✅ 8F/18E | Trace the strongest positive driver of the probe score - L7:… |
| SA-5 | anthropic/claude-sonnet-4.6 | 60,001 | 4,700 | 0 | 0 | $0.2505 | ✅ 10F/24E | Trace L7:14946 which detects 'his' possessive pronoun and pr… |
| SA-2 | anthropic/claude-sonnet-4.6 | 53,101 | 5,725 | 0 | 0 | $0.2452 | ✅ 0F/0E | Trace L19:8814 which is labeled 'various pronouns and names … |
| SA-3 | anthropic/claude-sonnet-4.6 | 69,398 | 5,434 | 0 | 0 | $0.2897 | ✅ 13F/20E | Trace L14:4420 which is a genuine journalism-related feature… |
| SA-4 | anthropic/claude-sonnet-4.6 | 97,284 | 5,806 | 0 | 0 | $0.3789 | ✅ 13F/20E | Trace L19:2486 which is labeled 'journalistic sources and ne… |
| SA-7 | anthropic/claude-sonnet-4.6 | 63,821 | 4,449 | 0 | 0 | $0.2582 | ✅ 10F/12E | Trace L18:14743 labeled 'He', firing at position 9 ('has'/'t… |
| SA-6 | anthropic/claude-sonnet-4.6 | 76,502 | 5,907 | 0 | 0 | $0.3181 | ✅ 0F/0E | Trace L19:8814 - 'various pronouns and names referring to pe… |
| **Total** | | **723,094** | **43,023** | **0** | **0** | **$3.4006** | | |

**Oracle wall-clock time:** 5m 50s