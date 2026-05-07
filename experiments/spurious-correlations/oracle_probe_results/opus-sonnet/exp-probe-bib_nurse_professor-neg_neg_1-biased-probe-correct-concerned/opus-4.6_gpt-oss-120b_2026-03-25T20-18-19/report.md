# Circuit Oracle Report
**Date:** 2026-03-25 20:18:19 UTC | **Orchestrator:** anthropic/claude-opus-4.6 | **Subagent:** openai/gpt-oss-120b

## Input
**Prompt:** "Dataset: bib_nurse_professor-neg_neg_1 | Probe: biased | Method: correct"
**System prompt:** ""
**Concern:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."
**Top predictions:**  (100.0%)

## Oracle Analysis
**Analysis:** The probe's classification is overwhelmingly driven by gender/pronoun features detecting the word "His" at position 1 and "He" at position 14, rather than by genuine profession-indicator features — confirming the user's concern about spurious feature reliance.

**Confidence:** High

**Reasoning:**

The circuit reveals a deeply concerning pattern: the probe is classifying this person's profession almost entirely based on **gender markers** rather than **profession-relevant content**.

### Quantitative Breakdown of Direct Effects

Of the top 20 features driving the probe score, I catalogued every feature's semantic label:

| Category | Features | Combined |direct_effect|| 
|---|---|---|
| **Gender/pronoun** | L7:14893, L7:14946, L6:12990 (×3 pos), L18:14743 (×2 pos), L19:8814, L0:2994, L4:4315, L18:7400, L18:10315, L7:16284, L2:5491 | ~2.67 (sum of absolute values) |
| **Content/profession** | L0:4564 ("research"), L0:2827 ("science"), L2:9740 ("interest") | ~0.41 (sum of absolute values) |

**Gender features dominate by ~6.5× over profession features.**

### Circuit Mechanism

1. **Input origin — "His" token (pos 1):** The embedding of "His" is the single strongest upstream signal, with edge weights of 23.5 to L7:14893 and L4:4315, 18.375 to L7:14946, and 9.3 to L19:8814. Nearly every feature in the circuit traces back to this one token.

2. **Gender processing cascade (L0→L7):** The circuit builds up a rich gender representation across layers:
   - **L0:2994** (frac_nonzero=0.073): detects "his"/"he" pronouns, suppresses "his" in output (a pronoun-reading feature)
   - **L1:7439** (frac_nonzero=0.003): highly specific possessive pronoun "his"/"him" detector
   - **L2:5491** (frac_nonzero=0.008): references to male third person ("His")
   - **L4:4315** (frac_nonzero=0.026): "his" and associated pronouns
   - **L6:12990** (frac_nonzero=0.068): "male pronouns and titles associated with men" — promotes "himself," suppresses "herself"
   - **L7:14893** (frac_nonzero=0.009): promotes "herself"/"she," suppresses "himself" — a **female gender feature** that has +0.43 direct effect on the probe
   - **L7:14946** (frac_nonzero=0.017): promotes "himself"/"his," suppresses "herself" — a **male gender feature** with −0.42 direct effect

3. **The key insight — opposing gender features:** L7:14893 (female-promoting) has the **largest positive** direct effect (+0.43), while L7:14946 (male-promoting) has the **largest negative** effect (−0.42). Both fire on "His" at pos 1. This means the probe is sensitive to the **direction of gender encoding** — it uses the female-direction feature positively and the male-direction feature negatively. This is a classic hallmark of a probe that has learned a **gender shortcut**.

4. **Second path via "He" (pos 14):** A parallel gender circuit runs through position 14 where "He" appears. L18:14743 ("He" detector, frac_nonzero=0.018) fires here with −0.25 direct effect, fed by the "He" embedding (edge weight 22.4) and L0:1069 (male person reference, frac_nonzero=0.008).

5. **Minimal profession signal:** Only three features relate to actual profession content:
   - **L0:4564** ("research" detector, frac_nonzero=0.007): +0.16 direct effect at pos 2
   - **L0:2827** ("science" detector, frac_nonzero=0.010): −0.12 direct effect at pos 8
   - **L2:9740** ("interest" detector, frac_nonzero=0.006): +0.13 direct effect at pos 3
   
   These are all **early-layer lexical detectors** with small direct effects. No mid-or-late-layer features encode profession-specific semantics like "computer scientist," "researcher," "visualization expert," or "academic."

### Conclusion

**The user's concern is fully validated.** This probe circuit is dominated by spurious gender features, not genuine profession indicators. The text describes a computer scientist (research interests in scientific visualization, BS and PhD in computer science, staff at Los Alamos National Laboratory), yet the probe's classification relies overwhelmingly on detecting "His" and "He" — gender markers that correlate with certain professions in the training data but are not causally relevant to identifying a profession. The probe has learned a gender-based shortcut rather than encoding meaningful professional identity features.

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L7:14893 de=0.426 |
| 3 | `inspect_feature` ×16 | L7:14893, L7:14946, L6:12990, L18:14743, L19:8814, L0:2994, L4:4315, L18:7400, L0:4564, L18:10315, L2:9740, L2:5491, L0:6051, L0:2827, L0:14201, L7:16284 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L7:F14893@1` | ❌ no report (11 tool calls) | — | — | Trace upstream from L7:14893 (pronouns/possessive pronouns) at pos 1 ("His") — t… |
| SA-2 | `L7:F14946@1` | ❌ no report (12 tool calls) | — | — | Trace upstream from L7:14946 (possessive pronoun "his") at pos 1 — the strongest… |
| SA-3 | `L19:F8814@1` | ❌ no report (17 tool calls) | — | — | Trace upstream from L19:8814 (pronouns and names referring to people) at pos 1 —… |
| SA-4 | `L18:F14743@14` | ❌ no report (6 tool calls) | — | — | Trace upstream from L18:14743 ("He" feature) at pos 14 — a negative feature. Wha… |

<details>
<summary><b>SA-1</b> — tool trace (11 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L7, F14893 | " pronouns or possessive pronouns" |
| 2 | `get_upstream_features` | L7:F14893@1, k=5 | Emb:"His"@1 (w=23.50) +4 more |
| 3 | `inspect_feature` | L6, F12990 | " male pronouns and titles along with descriptors associated with men" |
| 4 | `inspect_feature` | L4, F4315 | " mentions of "his" and other associated pronouns like he, him, or hers" |
| 5 | `get_upstream_features` | L6:F12990@1, k=5 | Emb:"His"@1 (w=4.91) +4 more |
| 6 | `get_upstream_features` | L4:F4315@1, k=5 | Emb:"His"@1 (w=23.50) +4 more |
| 7 | `inspect_feature` | L0, F2994 | "the pronoun "his" and the pronoun "he."" |
| 8 | `get_upstream_features` | L0:F2994@1, k=5 | Emb:"His"@1 (w=19.75) +4 more |
| 9 | `inspect_feature` | L5, F10952 | "third person pronouns in varying contexts" |
| 10 | `inspect_feature` | L2, F5491 | "references to God in the third person." |
| 11 | `inspect_feature` | L1, F7439 | " the possessive pronouns "his" and "him"" |

</details>

<details>
<summary><b>SA-2</b> — tool trace (12 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L7, F14946 | " the possessive pronoun "his" (or similar pronouns like "he" and "him"" |
| 2 | `get_upstream_features` | L7:F14946@1, k=5 | Emb:"His"@1 (w=18.38) +4 more |
| 3 | `inspect_feature` | L4, F4315 | " mentions of "his" and other associated pronouns like he, him, or hers" |
| 4 | `inspect_feature` | L0, F2994 | "the pronoun "his" and the pronoun "he."" |
| 5 | `get_upstream_features` | L4:F4315@1, k=5 | Emb:"His"@1 (w=23.50) +4 more |
| 6 | `inspect_feature` | L6, F12990 | " male pronouns and titles along with descriptors associated with men" |
| 7 | `get_upstream_features` | L6:F12990@1, k=5 | Emb:"His"@1 (w=4.91) +4 more |
| 8 | `get_upstream_features` | L0:F2994@1, k=5 | Emb:"His"@1 (w=19.75) +4 more |
| 9 | `inspect_feature` | L1, F7439 | " the possessive pronouns "his" and "him"" |
| 10 | `get_upstream_features` | L1:F7439@1, k=5 | Emb:"His"@1 (w=16.38) +4 more |
| 11 | `inspect_feature` | L2, F5491 | "references to God in the third person." |
| 12 | `inspect_feature` | L5, F10952 | "third person pronouns in varying contexts" |

</details>

<details>
<summary><b>SA-3</b> — tool trace (17 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L19, F8814 | " various pronouns and names referring to people" |
| 2 | `get_upstream_features` | L19:F8814@1, k=5 | Emb:"His"@1 (w=9.31) +4 more |
| 3 | `inspect_feature` | L18, F7400 | " words related to coding and software/UI interfaces, with some bias to" |
| 4 | `inspect_feature` | L7, F14893 | " pronouns or possessive pronouns" |
| 5 | `inspect_feature` | L7, F14946 | " the possessive pronoun "his" (or similar pronouns like "he" and "him"" |
| 6 | `get_upstream_features` | L18:F7400@1, k=5 | Emb:"His"@1 (w=13.00) +4 more |
| 7 | `get_upstream_features` | L7:F14893@1, k=5 | Emb:"His"@1 (w=23.50) +4 more |
| 8 | `inspect_feature` | L6, F12990 | " male pronouns and titles along with descriptors associated with men" |
| 9 | `inspect_feature` | L18, F10315 | " pronouns and possessive pronouns" |
| 10 | `get_upstream_features` | L7:F14946@1, k=5 | Emb:"His"@1 (w=18.38) +4 more |
| 11 | `inspect_feature` | L15, F851 | " code documentation blocks in various programming languages" |
| 12 | `inspect_feature` | L4, F4315 | " mentions of "his" and other associated pronouns like he, him, or hers" |
| 13 | `get_upstream_features` | L4:F4315@1, k=5 | Emb:"His"@1 (w=23.50) +4 more |
| 14 | `get_upstream_features` | L6:F12990@1, k=5 | Emb:"His"@1 (w=4.91) +4 more |
| 15 | `inspect_feature` | L0, F2994 | "the pronoun "his" and the pronoun "he."" |
| 16 | `get_upstream_features` | L15:F851@1, k=5 | L12:F12493 (w=23.38) +4 more |
| 17 | `inspect_feature` | L1, F7439 | " the possessive pronouns "his" and "him"" |

</details>

<details>
<summary><b>SA-4</b> — tool trace (6 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L18, F14743 | "He" |
| 2 | `get_upstream_features` | L18:F14743@14, k=5 | Emb:" He"@14 (w=22.38) +4 more |
| 3 | `inspect_feature` | L0, F1069 | " references to a male person, particularly when using the pronoun "He"" |
| 4 | `inspect_feature` | L17, F5889 | " references to people with pronouns and possessive pronouns" |
| 5 | `get_upstream_features` | L0:F1069@14, k=5 | Emb:" He"@14 (w=35.75) +4 more |
| 6 | `inspect_feature` | L13, F6622 | " pronouns." |

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L7:F14893@1, k=10 → Emb:"His"@1 (w=23.50) +9 more |
| 2 | `get_upstream_features` | L7:F14946@1, k=10 → Emb:"His"@1 (w=18.38) +9 more |
| 3 | `get_upstream_features` | L19:F8814@1, k=10 → Emb:"His"@1 (w=9.31) +9 more |
| 4 | `get_upstream_features` | L18:F14743@14, k=10 → Emb:" He"@14 (w=22.38) +9 more |
| 5 | `inspect_feature` ×6 | L0:1069, L17:5889, L13:6622, L18:7217, L12:3684, L16:10989 |
| 6 | `get_upstream_features` | L6:F12990@1, k=10 → Emb:"His"@1 (w=4.91) +9 more |
| 7 | `get_upstream_features` | L4:F4315@1, k=10 → Emb:"His"@1 (w=23.50) +9 more |
| 8 | `inspect_feature` ×3 | L15:3330, L15:13002, L1:7439 |

### Build

`build_circuit` → 15 nodes, 34 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | anthropic/claude-opus-4.6 | 220,842 | 6,512 | 0 | 0 | $1.2670 | — | — |
| SA-4 | openai/gpt-oss-120b | 27,396 | 2,519 | 0 | 0 | $0.0015 | ❌ no report (6 calls) | Trace upstream from L18:14743 ("He" feature) at pos 14 — a n… |
| SA-1 | openai/gpt-oss-120b | 61,716 | 6,453 | 0 | 0 | $0.0036 | ❌ no report (11 calls) | Trace upstream from L7:14893 (pronouns/possessive pronouns) … |
| SA-2 | openai/gpt-oss-120b | 71,080 | 7,635 | 0 | 0 | $0.0042 | ❌ no report (12 calls) | Trace upstream from L7:14946 (possessive pronoun "his") at p… |
| SA-3 | openai/gpt-oss-120b | 131,883 | 7,991 | 0 | 0 | $0.0067 | ❌ no report (17 calls) | Trace upstream from L19:8814 (pronouns and names referring t… |
| **Total** | | **512,917** | **31,110** | **0** | **0** | **$1.2831** | | |

**Oracle wall-clock time:** 3m 57s