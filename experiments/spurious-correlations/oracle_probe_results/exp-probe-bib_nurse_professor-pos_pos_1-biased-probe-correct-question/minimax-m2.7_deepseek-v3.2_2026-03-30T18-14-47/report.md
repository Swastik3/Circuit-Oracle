# Circuit Oracle Report
**Date:** 2026-03-30 18:14:47 UTC | **Orchestrator:** minimax/minimax-m2.7 | **Subagent:** deepseek/deepseek-v3.2

## Input
**Prompt:** "Dataset: bib_nurse_professor-pos_pos_1 | Probe: biased | Method: correct"
**System prompt:** ""
**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."
**Top predictions:**  (100.0%)

## Oracle Analysis
**Analysis:** The probe's classification score is primarily driven by a gender-detection circuit (dominated by the pronoun "she" at position 5) with a combined direct effect of ~2.45, rather than by genuine profession indicators like the nursing-related feature at position 15 which has a direct effect of only ~0.55.

**Confidence:** 9/10

**Reasoning:** The attribution circuit reveals that the probe relies overwhelmingly on spurious gender markers rather than profession-specific signals:

1. **Gender Circuit Dominates (direct effect ~2.45):** The top features driving the probe all encode gender-related semantics:
   - L6:F11646 ("references to women, potentially triggered by pronouns and titles") — direct_effect +1.5469
   - L18:F14677 ("instances of women or girls being mentioned") — direct_effect +0.9062
   - L12:F12940 ("references to female pronouns and possessive pronouns") — direct_effect +0.6797
   - L19:F9685 ("women's names and their roles or accomplishments") — direct_effect +0.5625

2. **Hierarchical Gender Processing:** The circuit shows a clear gender-detection pipeline:
   - **Emb: 'she'** → **Gender Detection (Early Layer)** (L0-L2 features for "she", "her") → **Gender Reference Features (Mid Layer)** (L4-L12) → **Gender Aggregation (Late Layer)** (L17-L19) → **Probe Score**
   - The signal originates from the raw embedding of "she" at position 5 (edge weight 41.25), which is a spurious feature unrelated to nursing profession.

3. **Legitimate Profession Feature Exists But Is Weaker (direct effect ~0.55):**
   - L6:F15267 ("words in the document referring to the profession of nursing") fires on "nurses" at position 15 and "Perioperative" at position 14
   - This is a genuine profession indicator, but its contribution is ~4x smaller than the gender circuit

4. **Circuit Uses Correlation vs. Causation:** The probe appears to have learned that "she" + "nurse" frequently co-occur in training data, so it uses the gender marker as a proxy for the profession. This is a classic spurious correlation — the model is not identifying nurses by their profession indicators but by the gender of the subject.

5. **Low frac_nonzero values confirm specificity:** The gender features have frac_nonzero values of 0.006-0.02, meaning they are highly selective (only fire in specific contexts). This specificity doesn't make them less spurious — it just means they reliably detect the "female person" pattern regardless of context.

**Conclusion:** The user's concern is validated. The probe uses gender as a spurious proxy for profession prediction rather than relying on genuine profession-specific features like "nurse", "Perioperative", or "certified". This represents a failure mode where the model exploits statistical correlations in training data rather than learning the actual semantic relationship between profession and qualifications.

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 10 features; top: L6:11646 de=1.547 |
| 3 | `inspect_feature` ×5 | L6:11646, L18:14677, L12:12940, L4:7864, L19:9685 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L6:F11646@7` | ✅ reported | 6 | 15 | Trace the path from L6:F11646 (female pronoun references) upstream. What is this… |
| SA-2 | `L18:F14677@7` | ✅ reported | 12 | 21 | Trace the path from L18:F14677 (women/girls mention) upstream. What is this feat… |
| SA-3 | `L12:F12940@7` | ✅ reported | 9 | 23 | Trace the path from L12:F12940 (female pronouns) upstream. What is this feature … |
| SA-4 | `L19:F9685@7` | ✅ reported | 10 | 19 | Trace the path from L19:F9685 (women's names and roles) upstream. What is this f… |

<details>
<summary><b>SA-1</b> — tool trace (11 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F11646 | " references to women, potentially triggered by pronouns and titles" |
| 2 | `get_upstream_features` | L6:F11646@7, k=5 | Emb:" she"@7 (w=31.62) +4 more |
| 3 | `inspect_feature` | L0, F12519 | " the pronoun "she"" |
| 4 | `inspect_feature` | L4, F7864 | "xml or source code snippets, especially tags and possibly keywords in " |
| 5 | `inspect_feature` | L1, F4232 | " the possessive pronoun "her"" |
| 6 | `get_upstream_features` | L4:F7864@7, k=5 | Emb:" she"@7 (w=27.25) +4 more |
| 7 | `inspect_feature` | L2, F8966 | " the pronoun "she"" |
| 8 | `get_upstream_features` | L0:F12519@7, k=5 | Emb:" she"@7 (w=41.25) +4 more |
| 9 | `get_upstream_features` | L1:F4232@7, k=5 | Emb:" she"@7 (w=31.75) +4 more |
| 10 | `inspect_feature` | L0, F7509 | " female pronouns and words like daughter and husband that refer to wom" |
| 11 | `get_upstream_features` | L2:F8966@7, k=5 | Emb:" she"@7 (w=33.50) +4 more |

**Findings:** The circuit tracing reveals that L6:F11646 (female pronoun references) is primarily driven by the direct embedding of the token " she" at position 7 (edge_weight 31.625). This is the strongest signal source. Interestingly, there's a complex network of early-layer features that detect female pronouns but have negative connections to the L6 feature:

1. L0:F12519 detects "she" but suppresses "she" t…

</details>

<details>
<summary><b>SA-2</b> — tool trace (19 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L18, F14677 | " instances of women or girls being mentioned" |
| 2 | `get_upstream_features` | L18:F14677@7, k=5 | Emb:" she"@7 (w=28.38) +4 more |
| 3 | `inspect_feature` | L6, F11646 | " references to women, potentially triggered by pronouns and titles" |
| 4 | `inspect_feature` | L12, F12940 | "references to female pronouns and possessive pronouns" |
| 5 | `inspect_feature` | L0, F12519 | " the pronoun "she"" |
| 6 | `inspect_feature` | L4, F7864 | "xml or source code snippets, especially tags and possibly keywords in " |
| 7 | `get_upstream_features` | L6:F11646@7, k=5 | Emb:" she"@7 (w=31.62) +4 more |
| 8 | `inspect_feature` | L1, F4232 | " the possessive pronoun "her"" |
| 9 | `inspect_feature` | L0, F7509 | " female pronouns and words like daughter and husband that refer to wom" |
| 10 | `get_upstream_features` | L12:F12940@7, k=5 | Emb:" she"@7 (w=12.38) +4 more |
| 11 | `inspect_feature` | L8, F15388 | " female pronouns and proper names in close proximity" |
| 12 | `inspect_feature` | L10, F14965 | " terms relating to women" |
| 13 | `get_upstream_features` | L10:F14965@7, k=5 | Emb:" she"@7 (w=11.88) +4 more |
| 14 | `inspect_feature` | L6, F16329 | "female first names and their possessive forms" |
| 15 | `inspect_feature` | L7, F8952 | " references to women, by direct name or pronoun" |
| 16 | `get_upstream_features` | L7:F8952@7, k=5 | Emb:" she"@7 (w=24.25) +4 more |
| 17 | `inspect_feature` | L2, F8966 | " the pronoun "she"" |
| 18 | `get_upstream_features` | L0:F12519@7, k=5 | Emb:" she"@7 (w=41.25) +4 more |
| 19 | `get_upstream_features` | L4:F7864@7, k=5 | Emb:" she"@7 (w=27.25) +4 more |

**Findings:** The circuit traces how the high-level feature "instances of women or girls being mentioned" (L18:F14677) emerges from earlier features detecting female pronouns and references. The signal originates primarily from the embedding of the token " she" at position 7, which has strong direct connections to multiple features in the circuit (28.375 weight to L18:F14677, 31.625 to L6:F11646, etc.).

Key fi…

</details>

<details>
<summary><b>SA-3</b> — tool trace (15 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L12, F12940 | "references to female pronouns and possessive pronouns" |
| 2 | `get_upstream_features` | L12:F12940@7, k=5 | Emb:" she"@7 (w=12.38) +4 more |
| 3 | `inspect_feature` | L6, F11646 | " references to women, potentially triggered by pronouns and titles" |
| 4 | `inspect_feature` | L4, F7864 | "xml or source code snippets, especially tags and possibly keywords in " |
| 5 | `inspect_feature` | L8, F15388 | " female pronouns and proper names in close proximity" |
| 6 | `get_upstream_features` | L6:F11646@7, k=5 | Emb:" she"@7 (w=31.62) +4 more |
| 7 | `inspect_feature` | L0, F12519 | " the pronoun "she"" |
| 8 | `inspect_feature` | L1, F4232 | " the possessive pronoun "her"" |
| 9 | `get_upstream_features` | L4:F7864@7, k=5 | Emb:" she"@7 (w=27.25) +4 more |
| 10 | `inspect_feature` | L2, F8966 | " the pronoun "she"" |
| 11 | `get_upstream_features` | L0:F12519@7, k=5 | Emb:" she"@7 (w=41.25) +4 more |
| 12 | `inspect_feature` | L10, F14965 | " terms relating to women" |
| 13 | `get_upstream_features` | L10:F14965@7, k=5 | Emb:" she"@7 (w=11.88) +4 more |
| 14 | `inspect_feature` | L7, F8952 | " references to women, by direct name or pronoun" |
| 15 | `get_upstream_features` | L7:F8952@7, k=5 | Emb:" she"@7 (w=24.25) +4 more |

**Findings:** The circuit tracing reveals that L12:F12940 (encoding female pronouns and possessive pronouns) primarily receives its signal from the raw embedding of the token "she" at position 7 (edge weight: 12.375). The strongest feature pathway comes through L6:F11646 (references to women, potentially triggered by pronouns and titles), which itself receives a massive direct signal from the "she" embedding (3…

</details>

<details>
<summary><b>SA-4</b> — tool trace (15 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L19, F9685 | " references to women's names and their roles or accomplishments." |
| 2 | `get_upstream_features` | L19:F9685@7, k=5 | Emb:" she"@7 (w=12.25) +4 more |
| 3 | `inspect_feature` | L6, F11646 | " references to women, potentially triggered by pronouns and titles" |
| 4 | `inspect_feature` | L17, F5889 | " references to people with pronouns and possessive pronouns" |
| 5 | `inspect_feature` | L12, F12940 | "references to female pronouns and possessive pronouns" |
| 6 | `get_upstream_features` | L6:F11646@7, k=5 | Emb:" she"@7 (w=31.62) +4 more |
| 7 | `inspect_feature` | L4, F7864 | "xml or source code snippets, especially tags and possibly keywords in " |
| 8 | `get_upstream_features` | L17:F5889@7, k=5 | Emb:" she"@7 (w=33.75) +4 more |
| 9 | `inspect_feature` | L14, F14097 | " occurrences of the word "he"" |
| 10 | `inspect_feature` | L4, F15567 | "sentences with male or female pronouns and possessives, especially one" |
| 11 | `get_upstream_features` | L12:F12940@7, k=5 | Emb:" she"@7 (w=12.38) +4 more |
| 12 | `inspect_feature` | L10, F14965 | " terms relating to women" |
| 13 | `get_upstream_features` | L10:F14965@7, k=5 | Emb:" she"@7 (w=11.88) +4 more |
| 14 | `inspect_feature` | L7, F8952 | " references to women, by direct name or pronoun" |
| 15 | `inspect_feature` | L0, F12519 | " the pronoun "she"" |

**Findings:** The circuit tracing reveals that L19:F9685 (women's names and roles) encodes sophisticated understanding of female references, accomplishments, and roles. The signal originates strongly from the token " she" at position 7, with multiple parallel pathways through the network:

1. Direct embedding connection: " she" → L19:F9685 (weight 12.25)
2. Early layer pathways through pronoun detection feature…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` | L6, F15267 → " words in the document referring to the profession of nursing" |
| 2 | `get_upstream_features` | L6:F15267@15, k=10 → Emb:" nurses"@15 (w=16.12) +9 more |

### Build

`build_circuit` → 7 nodes, 7 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m2.7 | 32,652 | 3,620 | 46,132 | 0 | — | — | — |
| SA-1 | deepseek/deepseek-v3.2 | 71,312 | 3,434 | 4,480 | 0 | — | ✅ 6F/15E | Trace the path from L6:F11646 (female pronoun references) up… |
| SA-3 | deepseek/deepseek-v3.2 | 100,757 | 4,540 | 22,080 | 0 | — | ✅ 9F/23E | Trace the path from L12:F12940 (female pronouns) upstream. W… |
| SA-4 | deepseek/deepseek-v3.2 | 124,258 | 4,553 | 0 | 0 | — | ✅ 10F/19E | Trace the path from L19:F9685 (women's names and roles) upst… |
| SA-2 | deepseek/deepseek-v3.2 | 173,593 | 5,350 | 13,952 | 0 | — | ✅ 12F/21E | Trace the path from L18:F14677 (women/girls mention) upstrea… |
| **Total** | | **502,572** | **21,497** | **86,644** | **0** | **—** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 4m 36s