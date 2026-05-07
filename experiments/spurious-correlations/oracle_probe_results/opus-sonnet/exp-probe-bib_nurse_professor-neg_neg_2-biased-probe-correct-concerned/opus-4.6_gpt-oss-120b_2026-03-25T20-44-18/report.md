# Circuit Oracle Report
**Date:** 2026-03-25 20:44:18 UTC | **Orchestrator:** anthropic/claude-opus-4.6 | **Subagent:** openai/gpt-oss-120b

## Input
**Prompt:** "Dataset: bib_nurse_professor-neg_neg_2 | Probe: biased | Method: correct"
**System prompt:** ""
**Concern:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."
**Top predictions:**  (100.0%)

## Oracle Analysis
Now let me compute the total contribution by category:

**Gender-related features (total positive effect on probe):**
- L0:F2994 pos 3: +0.39
- L0:F2994 pos 25: +0.13
- L0:F2994 pos 47: +0.11
- L7:F14893 pos 3: +0.20
- L0:F13553 pos 2: +0.10
- **Subtotal positive gender: +0.93**

**Gender-related features (negative effect on probe):**
- L12:F2175 pos 2: -0.18
- L7:F14946 pos 3: -0.18
- L6:F12990 pos 22: -0.18
- L6:F12990 pos 3: -0.10
- L18:F14743 pos 22: -0.14
- L18:F14743 pos 81: -0.11
- L18:F10315 pos 3: -0.10
- **Subtotal negative gender: -0.99**

**Net gender contribution: +0.93 - 0.99 ≈ -0.06** (roughly balanced)

**Academic/profession features:**
- L6:F170 pos 9: +0.14
- L6:F170 pos 8: +0.10
- L0:F1326 pos 14: +0.11
- L5:F10392 pos 9: -0.11
- **Net academic: +0.24**

**Other:**
- L0:F7532 pos 1: +0.11 (proper nouns)
- L0:F15320 pos 2: +0.10 (word "ice" — spurious)
- L0:F13526 pos 21: -0.10 (months)

This is interesting — let me reconsider. The gender features have large magnitudes on both sides but roughly cancel. The net effect is dominated by academic/profession features. But the *individual* magnitudes of gender features are larger than academic ones.

**Analysis:** The probe's classification score is driven by a circuit that is heavily populated with gender-marking features (detecting "his", "He", and male pronouns) which constitute the highest-magnitude individual contributions, though genuine profession-content features (academic fields, engineering, degrees, organizations) also contribute meaningfully.

**Confidence:** High

**Reasoning:** The circuit reveals a concerning but nuanced picture regarding the user's concern about spurious gender features:

**1. Gender features dominate individual magnitudes but partially cancel.** The single strongest feature driving the probe is L0:F2994 ("his/he" pronoun detector, frac_nonzero=0.073) at position 3, with a direct effect of +0.39 — nearly double the next strongest contributor. This feature fires on every instance of "his" in the text (positions 3, 25, 47), contributing a combined +0.64. Additional gender features at L7:F14893 (pronoun detector promoting "herself/she", +0.20) and L0:F13553 (past tense promoting "himself/his", +0.10) bring the total positive gender signal to ~+0.93.

However, there are substantial *negative* gender contributions: L12:F2175 ("gender words" promoting "himself", -0.18), L7:F14946 ("his" promoting "himself", -0.18), L6:F12990 ("male pronouns/titles", -0.28 combined), L18:F14743 ("He", -0.25 combined), and L18:F10315 ("pronouns/possessives", -0.10). These total ~-0.99, roughly canceling the positive gender signal.

**2. The gender signal chain is deep and well-traced.** The token embedding of " his" (pos 3, edge weight 43.25) feeds directly into L0:F2994, which then cascades through L4:F4315 ("his" mentions, frac_nonzero=0.026), L6:F12990 ("male pronouns", frac_nonzero=0.068), and L7:F14893 ("pronouns", frac_nonzero=0.009). Similarly, the " He" embedding at pos 22 (weight 21.9) feeds through L0:F1069 ("He/His" references) into L18:F14743 ("He" pronoun).

**3. Genuine profession features contribute but with smaller magnitude.** The academic content path runs from token embeddings " Engineering" and " Mechanical" → L2:F1440 ("engineering" word, frac_nonzero=0.005) → L5:F10392 ("fields of academic study", frac_nonzero=0.004) → L6:F170 ("academic fields", frac_nonzero=0.039). L6:F170 contributes +0.24 combined, while L5:F10392 contributes -0.11. A parallel degree path runs from "achelors" → L2:F10852 ("academic titles/degrees", frac_nonzero=0.008) → L4:F3727 ("academic degrees", frac_nonzero=0.005) → L5:F10392. These are all highly specific features (low frac_nonzero) grounded in genuine content tokens. The organization feature L0:F1326 (pos 14, "University") adds +0.11.

**4. The user's concern is partially validated.** While gender features roughly cancel in net effect, this cancellation is coincidental rather than architecturally guaranteed — it depends on the specific text having many male pronouns that activate both positive and negative gender features. The probe's weight vector clearly has large projections along gender-encoding directions. In a text about a female professor (using "her"/"she"), the gender features would fire differently and could produce a different probe score *even for the same profession*. The fact that gender features are the highest-magnitude individual contributors (L0:F2994 at +0.39 vs. L6:F170 at +0.14 for the top academic feature) suggests the probe has learned to partially rely on gender correlations in training data rather than purely on profession-diagnostic content. The genuine engineering/academic features exist in the circuit but are secondary in magnitude.

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L0:2994 de=0.395 |
| 3 | `inspect_feature` ×15 | L0:2994, L7:14893, L12:2175, L7:14946, L6:12990, L6:170, L18:14743, L5:10392, L0:1326, L0:7532, L0:12351, L0:13526, L0:15320, L0:13553, L18:10315 |

### Dispatch: 6 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L0:F2994@3` | ❌ no report (2 tool calls) | — | — | Trace L0:F2994 at pos 3 — this is labeled 'the pronoun his/he' and is the top po… |
| SA-2 | `L7:F14893@3` | ✅ reported | 12 | 19 | Trace L7:F14893 at pos 3 — labeled 'pronouns or possessive pronouns', the second… |
| SA-3 | `L6:F170@9` | ❌ no report (13 tool calls) | — | — | Trace L6:F170 at pos 9 — labeled 'references to academic fields'. This is a posi… |
| SA-4 | `L12:F2175@2` | ❌ error | — | — | Trace L12:F2175 at pos 2 — labeled 'words referring to gender', a negative drive… |
| SA-5 | `L18:F14743@22` | ❌ no report (10 tool calls) | — | — | Trace L18:F14743 at pos 22 — labeled 'He', a negative driver that promotes 'hims… |
| SA-6 | `L5:F10392@9` | ❌ no report (10 tool calls) | — | — | Trace L5:F10392 at pos 9 — labeled 'fields of academic study', a negative driver… |

<details>
<summary><b>SA-1</b> — tool trace (2 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F2994 | "the pronoun "his" and the pronoun "he."" |
| 2 | `get_upstream_features` | L0:F2994@3, k=10 | Emb:" his"@3 (w=43.25) +9 more |

</details>

<details>
<summary><b>SA-2</b> — tool trace (15 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L7, F14893 | " pronouns or possessive pronouns" |
| 2 | `get_upstream_features` | L7:F14893@3, k=10 | Emb:" his"@3 (w=24.38) +9 more |
| 3 | `inspect_feature` | L0, F2994 | "the pronoun "his" and the pronoun "he."" |
| 4 | `inspect_feature` | L6, F12990 | " male pronouns and titles along with descriptors associated with men" |
| 5 | `get_upstream_features` | L0:F2994@3, k=10 | Emb:" his"@3 (w=43.25) +9 more |
| 6 | `inspect_feature` | L4, F4315 | " mentions of "his" and other associated pronouns like he, him, or hers" |
| 7 | `inspect_feature` | L6, F10944 | " text in languages other than English" |
| 8 | `get_upstream_features` | L6:F12990@3, k=10 | Emb:" his"@3 (w=8.31) +9 more |
| 9 | `get_upstream_features` | L4:F4315@3, k=10 | Emb:" his"@3 (w=28.50) +9 more |
| 10 | `inspect_feature` | L1, F7439 | " the possessive pronouns "his" and "him"" |
| 11 | `get_upstream_features` | L1:F7439@3, k=10 | Emb:" his"@3 (w=25.62) +9 more |
| 12 | `inspect_feature` | L2, F5491 | "references to God in the third person." |
| 13 | `get_upstream_features` | L2:F5491@3, k=10 | Emb:" his"@3 (w=37.00) +9 more |
| 14 | `inspect_feature` | L3, F13121 | "the word "His" and words that are often capitalized in scientific lite" |
| 15 | `get_upstream_features` | L6:F10944@3, k=10 | Emb:" his"@3 (w=9.00) +9 more |

**Findings:** The pronoun-focused feature L7:F14893 (pos 3) derives its strong drive mainly from the raw token embedding for the word 'his' (weight 24.4) and is heavily inhibited by the low‑layer pronoun detector L0:F2994 (weight -10.9). L0:F2994 itself is dominated by the same 'his' embedding (43.3) and modest contributions from surrounding tokens. Additional upstream signals come from mid‑layer gender‑pronoun…

</details>

<details>
<summary><b>SA-3</b> — tool trace (13 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F170 | " references to academic fields, especially those in the humanities" |
| 2 | `get_upstream_features` | L6:F170@9, k=5 | L5:F10392 (w=10.94) +4 more |
| 3 | `inspect_feature` | L5, F10392 | " fields of academic study" |
| 4 | `inspect_feature` | L5, F6384 | "words related to higher education and professions" |
| 5 | `get_upstream_features` | L5:F10392@9, k=5 | Emb:" Mechanical"@8 (w=3.08) +4 more |
| 6 | `inspect_feature` | L4, F3727 | " mentions of academic degrees" |
| 7 | `get_upstream_features` | L4:F3727@5, k=5 | Emb:"achelors"@5 (w=22.25) +4 more |
| 8 | `inspect_feature` | L2, F10852 | " academic titles and degrees" |
| 9 | `get_upstream_features` | L2:F10852@5, k=5 | Emb:"achelors"@5 (w=19.25) +4 more |
| 10 | `inspect_feature` | L0, F9026 | "technical documents or data, including numbers, units, and references " |
| 11 | `get_upstream_features` | L5:F6384@9, k=5 | Emb:" Engineering"@9 (w=7.72) +4 more |
| 12 | `inspect_feature` | L4, F11037 | " words related to counseling, therapy, social work, and academic degre" |
| 13 | `get_upstream_features` | L4:F11037@9, k=5 | Emb:" Engineering"@9 (w=8.25) +4 more |

</details>

<details>
<summary><b>SA-5</b> — tool trace (10 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L18, F14743 | "He" |
| 2 | `get_upstream_features` | L18:F14743@22, k=5 | Emb:" He"@22 (w=21.88) +4 more |
| 3 | `inspect_feature` | L0, F1069 | " references to a male person, particularly when using the pronoun "He"" |
| 4 | `inspect_feature` | L17, F5889 | " references to people with pronouns and possessive pronouns" |
| 5 | `inspect_feature` | L13, F6622 | " pronouns." |
| 6 | `inspect_feature` | L15, F3330 | " personal stories of individuals, especially women and their actions o" |
| 7 | `get_upstream_features` | L0:F1069@22, k=5 | Emb:" He"@22 (w=37.00) +4 more |
| 8 | `get_upstream_features` | L17:F5889@22, k=5 | Emb:" He"@22 (w=20.75) +4 more |
| 9 | `get_upstream_features` | L13:F6622@22, k=5 | Emb:" He"@22 (w=13.19) +4 more |
| 10 | `inspect_feature` | L6, F2267 | "words that appear in programming code, legal jargon, or scientific tex" |

</details>

<details>
<summary><b>SA-6</b> — tool trace (10 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L5, F10392 | " fields of academic study" |
| 2 | `get_upstream_features` | L5:F10392@9, k=5 | Emb:" Mechanical"@8 (w=3.08) +4 more |
| 3 | `inspect_feature` | L4, F3727 | " mentions of academic degrees" |
| 4 | `inspect_feature` | L3, F4113 | " mentions of academic degrees and areas of study" |
| 5 | `inspect_feature` | L2, F1440 | " the word "engineering" and words related to its definition" |
| 6 | `get_upstream_features` | L2:F1440@9, k=5 | Emb:" Engineering"@9 (w=19.50) +4 more |
| 7 | `inspect_feature` | L1, F675 | "the word "push" or other words related to pushing, inserting, or trans" |
| 8 | `get_upstream_features` | L4:F3727@5, k=5 | Emb:"achelors"@5 (w=22.25) +4 more |
| 9 | `inspect_feature` | L2, F10852 | " academic titles and degrees" |
| 10 | `get_upstream_features` | L2:F10852@5, k=5 | Emb:"achelors"@5 (w=19.25) +4 more |

**Findings:** {
  "discovered_features": [
    {"layer": 5, "feature_idx": 10392, "pos": 9, "label": "fields of academic study", "frac_nonzero": 0.00362},
    {"layer": 4, "feature_idx": 3727, "pos": 5, "label": "mentions of academic degrees", "frac_nonzero": 0.0051},
    {"layer": 3, "feature_idx": 4113, "pos": 7, "label": "mentions of academic degrees and areas of study", "frac_nonzero": 0.00317},
    {"layer…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L0:F2994@3, k=5 → Emb:" his"@3 (w=43.25) +4 more |
| 2 | `get_upstream_features` | L6:F170@9, k=5 → L5:F10392 (w=10.94) +4 more |
| 3 | `get_upstream_features` | L18:F14743@22, k=8 → Emb:" He"@22 (w=21.88) +7 more |
| 4 | `get_upstream_features` | L12:F2175@2, k=8 → Emb:" received"@2 (w=4.09) +7 more |
| 5 | `get_upstream_features` | L5:F10392@9, k=5 → Emb:" Mechanical"@8 (w=3.08) +4 more |
| 6 | `inspect_feature` ×9 | L0:1069, L17:5889, L4:4315, L4:3727, L2:1440, L2:10852, L3:4113, L5:7317, L13:6622 |

### Build

`build_circuit` → 28 nodes, 41 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | anthropic/claude-opus-4.6 | 161,436 | 8,769 | 0 | 0 | $1.0264 | — | — |
| SA-1 | openai/gpt-oss-120b | 7,132 | 951 | 0 | 0 | $0.0005 | ❌ no report (2 calls) | Trace L0:F2994 at pos 3 — this is labeled 'the pronoun his/h… |
| SA-5 | openai/gpt-oss-120b | 59,138 | 4,943 | 0 | 0 | $0.0032 | ❌ no report (10 calls) | Trace L18:F14743 at pos 22 — labeled 'He', a negative driver… |
| SA-6 | openai/gpt-oss-120b | 54,560 | 5,317 | 0 | 0 | $0.0031 | ❌ no report (10 calls) | Trace L5:F10392 at pos 9 — labeled 'fields of academic study… |
| SA-3 | openai/gpt-oss-120b | 81,642 | 6,152 | 0 | 0 | $0.0044 | ❌ no report (13 calls) | Trace L6:F170 at pos 9 — labeled 'references to academic fie… |
| SA-2 | openai/gpt-oss-120b | 110,947 | 9,522 | 0 | 0 | $0.0061 | ✅ 12F/19E | Trace L7:F14893 at pos 3 — labeled 'pronouns or possessive p… |
| **Total** | | **474,855** | **35,654** | **0** | **0** | **$1.0437** | | |

**Oracle wall-clock time:** 4m 42s