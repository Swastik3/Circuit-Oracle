# Circuit Oracle Report
**Date:** 2026-03-25 20:24:11 UTC | **Orchestrator:** anthropic/claude-opus-4.6 | **Subagent:** openai/gpt-oss-120b

## Input
**Prompt:** "Dataset: bib_nurse_professor-neg_neg_1 | Probe: unbiased | Method: correct"
**System prompt:** ""
**Concern:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."
**Top predictions:**  (100.0%)

## Oracle Analysis
**Analysis:** The probe's classification score is driven by a mix of genuine academic/profession indicators and a prominent gender-based spurious feature, with the single strongest positive contributor being a male pronoun "He/His" detector (L0:1069, +0.070) that fires on the input token "His."

**Confidence:** High

**Reasoning:**

The circuit reveals a concerning mix of **spurious gender features** and **genuine profession-related features** driving this probe's classification:

### 🚩 Spurious Gender Pathway (Most Influential Positive Signal)

The **strongest single positive contributor** to the probe score is **L0:1069** (+0.070), a male pronoun "He/His" detector (frac_nonzero=0.008, highly selective). It fires on the "His" token at position 1, driven entirely by the raw `His` embedding (edge_weight=21.6). This feature detects nothing about profession — it simply recognizes masculine pronouns. Its suppressed tokens are literally `He`, `His`, `Him`, `Himself`, confirming it's a pure gender marker.

A second gender feature, **L2:3877** ("His" + religious references, frac_nonzero=0.007), also positively contributes (+0.034), again driven entirely from the `His` embedding (edge_weight=20.9). It is fed by L0:1069 with a negative connection (-0.86), suggesting it captures a complementary aspect of the "His" signal.

Interestingly, a third male pronoun feature **L0:2994** (frac_nonzero=0.073, much more generic) has a *negative* effect (-0.039), partially counteracting the gender signal. But the net gender contribution remains strongly positive: **+0.070 + 0.034 - 0.039 = +0.065**, making gender the single largest net positive force in the circuit.

### ✅ Genuine Profession Pathways

Several features encode legitimate academic/professional content:

1. **Academic Research Path** (pos 3): L1:10986 ("academic research words," +0.067) is the second-strongest positive feature. It's driven by the `research` (edge=6.6) and `interests` (edge=4.5) token embeddings — genuine content words. L2:1621 ("education & career info," +0.038) similarly fires on `interests`.

2. **Degree Qualification Path** (pos 17-31): A multi-layer chain detects "received a BS from... PhD from..." patterns:
   - L1:15795 ("education/admissions," frac_nonzero=0.011) ← `BS` embedding (4.5)
   - L2:10852 ("academic titles/degrees," frac_nonzero=0.008) ← `BS` embedding (15.4)
   - L3:4213 ("degree qualifications," +0.035) ← `from` (11.1), `BS` (3.8), L2:10852 (4.3)
   - L7:14129 ("academic degrees/universities," +0.040) ← `PhD` embedding (19.3), L6:2254 (7.6)

3. **Deep Academic Credential Chain** (pos 27-31): Features at L17:11003 ("university," promotes "University"), L19:2496 ("universities & degrees"), and L20:14235 ("academic credentials," promotes "UC," "Cornell," "University") form a deep chain. These are driven by PhD, from, science, and received tokens — all legitimate profession signals. However, L20:14235 has a **negative** direct effect (-0.036), meaning the probe actually pushes *against* this university credential signal.

### ⚠️ Negative Professional Features (Suppressing the Classification)

Notably, many of the strongest **negative** contributors are genuine profession indicators:
- **L8:11284** ("names/universities/research," -0.057): the strongest negative feature
- **L6:2254** ("academic degrees," -0.042 and -0.040 at two positions)
- **L14:11252** ("code/coordinate geometry," -0.050 at "visualization" position)
- **L6:6331** ("engineering technical terms," -0.035)
- **L20:14235** ("academic credentials," -0.036)

This is paradoxical: features detecting degrees, universities, computer science, and research suppress the probe score, while the gender marker boosts it most.

### Conclusion

**The user's concern is validated.** The probe exhibits significant reliance on spurious gender features. The male pronoun "He/His" detector (L0:1069) is the single most impactful positive feature, contributing +0.070 — comparable to the academic research feature (+0.067). The combined net gender signal (~+0.065) represents a substantial fraction of the positive classification drive. Meanwhile, many genuine profession indicators (academic degrees, university mentions, technical CS terms) actually have **negative** effects, suggesting the probe may have learned a gendered shortcut: biographies starting with "His/He" correlate with certain professions in the training data, and the probe exploits this statistical association rather than relying purely on professional content. The circuit structure — where gender features act at layer 0 with direct paths to the output, while deep professional feature chains are suppressed — strongly suggests the probe's classification is partially confounded by gender.

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L0:1069 de=0.070 |
| 3 | `inspect_feature` ×19 | L0:1069, L1:10986, L8:11284, L14:11252, L5:12330, L0:10783, L0:13431, L6:2254, L2:10852, L7:14129, L4:9757, L0:2994, L0:2159, L2:1621, L0:6446, L20:14235, L3:4213, L6:6331, L2:3877 |

### Dispatch: 6 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L0:F1069@1` | ❌ no report (2 tool calls) | — | — | Trace upstream from L0:1069 (male pronoun "He/His" detector at pos 1) to underst… |
| SA-2 | `L1:F10986@3` | ❌ no report (8 tool calls) | — | — | Trace upstream from L1:10986 (academic research words at pos 3 'interests') to u… |
| SA-3 | `L7:F14129@27` | ❌ no report (8 tool calls) | — | — | Trace upstream from L7:14129 (academic degrees/universities at pos 27, likely Ph… |
| SA-4 | `L20:F14235@31` | ❌ no report (15 tool calls) | — | — | Trace upstream from L20:14235 (academic credentials/institutions at pos 31, like… |
| SA-5 | `L0:F2994@1` | ❌ no report (2 tool calls) | — | — | Trace upstream from L0:2994 (male pronoun 'his/he' detector at pos 1). This is a… |
| SA-6 | `L3:F4213@21` | ❌ no report (11 tool calls) | — | — | Trace upstream from L3:4213 (degree qualifications/awards at pos 21, likely arou… |

<details>
<summary><b>SA-1</b> — tool trace (2 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F1069 | " references to a male person, particularly when using the pronoun "He"" |
| 2 | `get_upstream_features` | L0:F1069@1, k=5 | Emb:"His"@1 (w=21.62) +4 more |

</details>

<details>
<summary><b>SA-2</b> — tool trace (8 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L1, F10986 | " words related to academic research" |
| 2 | `get_upstream_features` | L1:F10986@3, k=5 | Emb:" research"@2 (w=6.62) +4 more |
| 3 | `inspect_feature` | L0, F13948 | " the color "pink"" |
| 4 | `inspect_feature` | L0, F6113 | " the word "overall", sometimes alongside words that express quantity" |
| 5 | `inspect_feature` | L0, F13431 | "the word "owing"." |
| 6 | `get_upstream_features` | L0:F13948@3, k=5 | Emb:" interests"@3 (w=14.94) +4 more |
| 7 | `get_upstream_features` | L0:F6113@3, k=5 | Emb:" interests"@3 (w=14.19) +4 more |
| 8 | `get_upstream_features` | L0:F13431@3, k=5 | Emb:" interests"@3 (w=12.25) +4 more |

**Findings:** {
  "discovered_features": [
    {"layer": 1, "feature_idx": 10986, "pos": 3, "label": "words related to academic research"},
    {"layer": 0, "feature_idx": 13948, "pos": 3, "label": "the color \"pink\""},
    {"layer": 0, "feature_idx": 6113, "pos": 3, "label": "the word \"overall\", sometimes alongside words that express quantity"},
    {"layer": 0, "feature_idx": 13431, "pos": 3, "label": "the…

</details>

<details>
<summary><b>SA-3</b> — tool trace (8 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L7, F14129 | " academic degrees, universities, and people associated with them" |
| 2 | `get_upstream_features` | L7:F14129@27, k=10 | Emb:" PhD"@27 (w=19.25) +9 more |
| 3 | `inspect_feature` | L6, F2254 | "references to academic degrees" |
| 4 | `inspect_feature` | L5, F13801 | "abbreviations for degrees and mentions of educational attainment" |
| 5 | `get_upstream_features` | L6:F2254@27, k=10 | Emb:" PhD"@27 (w=22.00) +9 more |
| 6 | `inspect_feature` | L2, F10852 | " academic titles and degrees" |
| 7 | `get_upstream_features` | L2:F10852@27, k=10 | Emb:" PhD"@27 (w=29.50) +9 more |
| 8 | `inspect_feature` | L5, F11028 | " terms and phrases related to academic study and institutions" |

</details>

<details>
<summary><b>SA-4</b> — tool trace (15 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L20, F14235 | " references to academic credentials and institutions." |
| 2 | `get_upstream_features` | L20:F14235@31, k=5 | L17:F11003 (w=30.38) +4 more |
| 3 | `inspect_feature` | L17, F11003 | "university" |
| 4 | `inspect_feature` | L19, F2496 | " mentions of universities and degrees" |
| 5 | `get_upstream_features` | L17:F11003@31, k=5 | Emb:" PhD"@27 (w=9.44) +4 more |
| 6 | `get_upstream_features` | L19:F2496@31, k=5 | L17:F11003 (w=14.12) +4 more |
| 7 | `inspect_feature` | L7, F14129 | " academic degrees, universities, and people associated with them" |
| 8 | `inspect_feature` | L18, F13805 | "Universities" |
| 9 | `get_upstream_features` | L7:F14129@27, k=5 | Emb:" PhD"@27 (w=19.25) +4 more |
| 10 | `inspect_feature` | L18, F13264 | " words and phrases associated with earning advanced academic degrees l" |
| 11 | `inspect_feature` | L6, F2254 | "references to academic degrees" |
| 12 | `get_upstream_features` | L6:F2254@27, k=5 | Emb:" PhD"@27 (w=22.00) +4 more |
| 13 | `inspect_feature` | L2, F10852 | " academic titles and degrees" |
| 14 | `get_upstream_features` | L18:F13805@31, k=5 | L17:F11003 (w=23.12) +4 more |
| 15 | `get_upstream_features` | L2:F10852@27, k=5 | Emb:" PhD"@27 (w=29.50) +4 more |

</details>

<details>
<summary><b>SA-5</b> — tool trace (2 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F2994 | "the pronoun "his" and the pronoun "he."" |
| 2 | `get_upstream_features` | L0:F2994@1, k=5 | Emb:"His"@1 (w=19.75) +4 more |

</details>

<details>
<summary><b>SA-6</b> — tool trace (11 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L3, F4213 | " mentions of degree qualifications or awards" |
| 2 | `get_upstream_features` | L3:F4213@21, k=5 | Emb:" from"@21 (w=11.12) +4 more |
| 3 | `inspect_feature` | L2, F10852 | " academic titles and degrees" |
| 4 | `inspect_feature` | L0, F8974 | "the word "from"" |
| 5 | `get_upstream_features` | L2:F10852@17, k=5 | Emb:" BS"@17 (w=15.44) +4 more |
| 6 | `inspect_feature` | L1, F15795 | " words related to education and school admissions" |
| 7 | `inspect_feature` | L1, F12372 | " mentions of US universities and sports teams" |
| 8 | `get_upstream_features` | L1:F15795@17, k=5 | Emb:" BS"@17 (w=4.50) +4 more |
| 9 | `inspect_feature` | L1, F12372 | " mentions of US universities and sports teams" |
| 10 | `get_upstream_features` | L1:F15795@17, k=5 | Emb:" BS"@17 (w=4.50) +4 more |
| 11 | `inspect_feature` | L0, F3825 | " mentions of studies involving medical acronyms" |

**Findings:** {
  "discovered_features": [
    {"layer": 3, "feature_idx": 4213, "pos": 21, "label": "mentions of degree qualifications or awards"},
    {"layer": 2, "feature_idx": 10852, "pos": 17, "label": "academic titles and degrees"},
    {"layer": 1, "feature_idx": 15795, "pos": 17, "label": "words related to education and school admissions"},
    {"layer": 0, "feature_idx": 3825, "pos": 17, "label": "men…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L0:F1069@1, k=5 → Emb:"His"@1 (w=21.62) +4 more |
| 2 | `get_upstream_features` | L0:F2994@1, k=5 → Emb:"His"@1 (w=19.75) +4 more |
| 3 | `get_upstream_features` | L7:F14129@27, k=10 → Emb:" PhD"@27 (w=19.25) +9 more |
| 4 | `get_upstream_features` | L20:F14235@31, k=10 → L17:F11003 (w=30.38) +9 more |
| 5 | `get_upstream_features` | L2:F3877@1, k=5 → Emb:"His"@1 (w=20.88) +4 more |
| 6 | `inspect_feature` ×7 | L17:11003, L19:2496, L5:13801, L5:11028, L6:8285, L1:15795, L1:12372 |
| 7 | `get_upstream_features` | L17:F11003@31, k=10 → Emb:" PhD"@27 (w=9.44) +9 more |
| 8 | `get_upstream_features` | L6:F2254@27, k=5 → Emb:" PhD"@27 (w=22.00) +4 more |

### Build

`build_circuit` → 29 nodes, 52 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | anthropic/claude-opus-4.6 | 206,211 | 8,351 | 0 | 0 | $1.2398 | — | — |
| SA-5 | openai/gpt-oss-120b | 6,957 | 784 | 0 | 0 | $0.0004 | ❌ no report (2 calls) | Trace upstream from L0:2994 (male pronoun 'his/he' detector … |
| SA-1 | openai/gpt-oss-120b | 7,215 | 821 | 0 | 0 | $0.0004 | ❌ no report (2 calls) | Trace upstream from L0:1069 (male pronoun "He/His" detector … |
| SA-2 | openai/gpt-oss-120b | 37,964 | 3,504 | 0 | 0 | $0.0021 | ❌ no report (8 calls) | Trace upstream from L1:10986 (academic research words at pos… |
| SA-3 | openai/gpt-oss-120b | 39,366 | 3,618 | 0 | 0 | $0.0022 | ❌ no report (8 calls) | Trace upstream from L7:14129 (academic degrees/universities … |
| SA-6 | openai/gpt-oss-120b | 60,738 | 4,751 | 0 | 0 | $0.0033 | ❌ no report (11 calls) | Trace upstream from L3:4213 (degree qualifications/awards at… |
| SA-4 | openai/gpt-oss-120b | 100,288 | 8,747 | 0 | 0 | $0.0056 | ❌ no report (15 calls) | Trace upstream from L20:14235 (academic credentials/institut… |
| **Total** | | **458,739** | **30,576** | **0** | **0** | **$1.2539** | | |

**Oracle wall-clock time:** 4m 15s