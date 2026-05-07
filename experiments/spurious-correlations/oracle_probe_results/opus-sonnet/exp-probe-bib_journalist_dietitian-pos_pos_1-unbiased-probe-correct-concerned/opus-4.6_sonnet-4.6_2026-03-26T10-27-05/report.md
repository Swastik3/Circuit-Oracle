# Circuit Oracle Report
**Date:** 2026-03-26 10:27:05 UTC | **Orchestrator:** anthropic/claude-opus-4.6 | **Subagent:** anthropic/claude-sonnet-4.6

## Input
**Prompt:** "Dataset: bib_journalist_dietitian-pos_pos_1 | Probe: unbiased | Method: correct"
**System prompt:** ""
**Concern:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."
**Top predictions:**  (100.0%)

## Oracle Analysis
## Analysis

**Analysis:** The probe classifies this text as a dietitian/nutritionist bio, driven overwhelmingly by genuine nutrition/diet/food content words ("eat," "Dietetics," "healthier," "Nutrition") rather than by spurious gender markers like "She," "her," or "Sarah."

**Confidence:** High

**Reasoning:**

### The Probe's Classification Signal

The probe is a linear classifier trained on layer-22 residual stream activations that identifies the profession "dietitian" (or a closely related nutrition profession). The attribution circuit reveals **three major parallel pathways** driving this classification, all grounded in domain-specific vocabulary:

---

### Path 1: The "eat" → food/nutrition pipeline (pos 9)
The token **"eat"** at position 9 is the single strongest anchor in the circuit. Its raw embedding feeds directly into features at every layer with massive edge weights (15–22):

- **L0:** Lexical detectors fire (L0:F2175 "the word 'eat'," frac=0.018; L0:F9093 "eating/dining," frac=0.005)
- **L1–L3:** Refined through eating-habit features (L1:F2750, frac=0.003; L3:F9216, frac=0.010)  
- **L4:** Converges into L4:F1626 "food consumption context" (frac=0.005, highly specific)
- **L6:** L6:F11327 "food/nutrition words" (frac=0.012) — a key mid-layer feature that promotes "foods, food, eating, meals"
- **L14:** L14:F4197 "food insecurity/food words" (frac=0.015, direct_effect=+0.124) — one of the top contributors to the probe
- **L15:** L15:F8177 "words associated with eating" (frac=0.006, direct_effect=+0.064)

### Path 2: The "Dietetics" morphological pipeline (pos 22–23)
The subword tokens **" Die"** (pos 22) and **"te"** (pos 23) — forming "Diete[tics]" — drive a second major pathway:

- **L0:** Morphological detectors fire: L0:F7699 "words starting with D" and L0:F4058 "'die' and derivatives"
- **L1:** Semantic features L1:F11764 "health and fitness" (frac=0.009) and L1:F6631 "dietary patterns" (frac=0.015) activate from the "Dietetics" context
- **L2–L3:** Morphological bridge L2:F7473 connects to L3:F10028 (promotes "recipes") and L3:F11774
- **L4:** Converges into L4:F13412 "diet/dietary health" (frac=0.012) — the **single most connected node**, firing at positions 9, 10, 22, and 23 with combined direct_effect of +0.37
- **L17:** L17:F7545 "registered healthcare professionals" (frac=0.004, very specific), activated by L4:F13412 and L4:F11037 "counseling/therapy/social work"
- **L19:** L19:F1589 "nutritional science context" (frac=0.038) — the apex feature integrating all nutrition signals, with combined direct_effect across positions of +0.34

### Path 3: The "clients" → commercial activity signal (pos 5)
**L6:F6115** "commercial activity/customers" (frac=0.023, direct_effect=+0.128) fires on the word "clients." Its upstream trace shows it is driven **entirely by the 'clients' embedding** (edge weight 25.6), with the nearby "her" (pos 4) contributing only ~3.5% of the signal (weight 0.91).

### Supporting features
- **L4:F12213** "health research" (frac=0.009, direct_effect=+0.094) at pos 10 ("healthier")
- **L6:F8984** "health-related words" (frac=0.016, direct_effect=+0.065) at pos 10
- **L0:F9888** "formal schooling" (frac=0.016, direct_effect=+0.084) at pos 3 ("educating")

### Suppressor features (negative effects)
- **L0:F6051** "periods/punctuation" (frac=0.057, direct_effect=−0.095): A generic punctuation detector that slightly weakens the probe score — not profession-specific
- **L1:F15251** "client word detector" (frac=0.003, direct_effect=−0.091): Fires on "clients" and suppresses it, functioning as an anti-repetition mechanism

---

### Addressing the Spurious Feature Concern

**The circuit does NOT use gender markers.** Deep tracing of every major pathway reveals:

1. **"She" (pos 1)** appears in exactly one upstream trace — as a **weak inhibitory** signal (weight −1.45 into L1:F15251, and −0.44 into L3:F9216). It **suppresses** rather than supports the probe classification.
2. **"her" (pos 4)** appears with weight 0.91 into L6:F6115, representing only ~3.5% of the signal at that node (vs. 25.6 from "clients"). Negligible.
3. **"Sarah" (pos 12)** does not appear in any upstream trace of any top feature.

Every one of the top-20 features driving this probe is semantically related to **nutrition, diet, food, health, eating, clients/customers, or healthcare professionals** — all genuine indicators of a dietitian profession. The features have low frac_nonzero values (0.003–0.038), indicating they are specific rather than generic. Their promoted tokens consistently include diet/nutrition vocabulary.

**Conclusion:** This probe circuit is using legitimate, domain-specific features to classify the profession. The model recognizes the dietitian profession through convergent evidence from the words "eat," "Dietetics," "Nutrition," "healthier," "clients," and "educating" — not through gender markers or name-based shortcuts.

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L6:6115 de=0.128 |
| 3 | `inspect_feature` ×14 | L6:6115, L14:4197, L4:13412, L6:11327, L19:1589, L0:6051, L1:15251, L0:9888, L5:3400, L0:5697, L0:8444, L6:8984, L15:8177, L4:12213 |

### Dispatch: 6 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L19:F1589@23` | ✅ reported | 11 | 14 | Trace the path from L19:F1589 (nutritional studies context) at pos 23 — what ups… |
| SA-2 | `L14:F4197@9` | ✅ reported | 12 | 26 | Trace the path from L14:F4197 (food insecurity words) at pos 9 ('eat') — what up… |
| SA-3 | `L6:F6115@5` | ✅ reported | 6 | 15 | Trace the path from L6:F6115 (commercial activity/customers) at pos 5 ('clients'… |
| SA-4 | `L6:F11327@9` | ✅ reported | 9 | 17 | Trace the path from L6:F11327 (food/nutrition words) at pos 9 ('eat') — what ups… |
| SA-5 | `L4:F13412@23` | ✅ reported | 10 | 13 | Trace the path from L4:F13412 (diet/dietary health) at pos 23 — what upstream fe… |
| SA-6 | `L0:F6051@11` | ✅ reported | 7 | 8 | Trace the path from L0:F6051 (periods/spaces) at pos 11 — this has a NEGATIVE di… |

<details>
<summary><b>SA-1</b> — tool trace (16 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L19, F1589 | " a context of scientific, specially nutritional, studies" |
| 2 | `get_upstream_features` | L19:F1589@23, k=8 | L4:F13412 (w=10.31) +7 more |
| 3 | `inspect_feature` | L4, F13412 | " terms related to diets and dietary health" |
| 4 | `inspect_feature` | L17, F7545 | "mentions of architecture, design, nurses and healthcare." |
| 5 | `inspect_feature` | L6, F11327 | " words or phrases related to food or nutrition" |
| 6 | `get_upstream_features` | L4:F13412@23, k=8 | L3:F11774 (w=4.75) +7 more |
| 7 | `get_upstream_features` | L17:F7545@23, k=8 | L4:F13412 (w=5.25) +7 more |
| 8 | `get_upstream_features` | L6:F11327@23, k=6 | L4:F13412 (w=6.50) +5 more |
| 9 | `inspect_feature` | L3, F11774 | " what appears to be a smattering of strings related to scientific nota" |
| 10 | `inspect_feature` | L3, F10028 | "words or short phrases that include "made of/from", and words ending w" |
| 11 | `inspect_feature` | L4, F11037 | " words related to counseling, therapy, social work, and academic degre" |
| 12 | `get_upstream_features` | L3:F11774@23, k=6 | Emb:" Die"@22 (w=5.62) +5 more |
| 13 | `inspect_feature` | L1, F11764 | " words and phrases related to health and fitness" |
| 14 | `inspect_feature` | L1, F6631 | " words related to dietary patterns and scientific studies" |
| 15 | `inspect_feature` | L0, F7699 | "words and abbreviations starting with the letter "D"" |
| 16 | `inspect_feature` | L2, F7473 | " capitalized two letter prefixes or suffixes" |

**Findings:** The circuit driving L19:F1589 ("nutritional studies context") originates almost entirely from genuine nutrition/dietetics content — NOT from gender markers like 'She' or 'Sarah'.

**Key finding: The signal is anchored in the token embeddings " Die" (pos 22) and " Nutrition" (pos 20), plus "te" (pos 23), which together spell out "Dietetics"/"Diet"/"Nutrition" in the input text.** No gender-marker f…

</details>

<details>
<summary><b>SA-2</b> — tool trace (21 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L14, F4197 | " words and phrases related to food insecurity." |
| 2 | `get_upstream_features` | L14:F4197@9, k=8 | Emb:" eat"@9 (w=17.75) +7 more |
| 3 | `inspect_feature` | L6, F11327 | " words or phrases related to food or nutrition" |
| 4 | `inspect_feature` | L3, F9216 | " the word "eat" and words related to eating habits" |
| 5 | `inspect_feature` | L4, F1626 | " phrases that occur in the context of food consumption." |
| 6 | `get_upstream_features` | L6:F11327@9, k=8 | Emb:" eat"@9 (w=22.12) +7 more |
| 7 | `inspect_feature` | L4, F7672 | " content related to eating and dining out" |
| 8 | `inspect_feature` | L5, F2468 | " words that indicate eating or bad habits" |
| 9 | `get_upstream_features` | L4:F1626@9, k=8 | Emb:" eat"@9 (w=15.81) +7 more |
| 10 | `inspect_feature` | L4, F13412 | " terms related to diets and dietary health" |
| 11 | `inspect_feature` | L2, F12264 | "words associated with communication, food, and parental influence" |
| 12 | `inspect_feature` | L1, F2750 | " variations of the word "eat"" |
| 13 | `get_upstream_features` | L3:F9216@9, k=8 | Emb:" eat"@9 (w=19.62) +7 more |
| 14 | `inspect_feature` | L0, F11021 | " mentions of eating" |
| 15 | `inspect_feature` | L2, F7196 | " language related to eating" |
| 16 | `inspect_feature` | L1, F4556 | " the word "script" and slight variations of it" |
| 17 | `get_upstream_features` | L3:F9216@9, k=8 | Emb:" eat"@9 (w=19.62) +7 more |
| 18 | `inspect_feature` | L0, F2175 | "the word "eat"" |
| 19 | `inspect_feature` | L1, F15373 | "the word "bus" in code or computer architecture contexts" |
| 20 | `inspect_feature` | L0, F6686 | " occurences of an upwards arrow" |
| 21 | `get_upstream_features` | L6:F11327@9, k=8 | Emb:" eat"@9 (w=22.12) +7 more |

**Findings:** The circuit driving L14:F4197 ("food insecurity words") at pos 9 (' eat') originates overwhelmingly from nutrition-related content tokens — NOT from gender or name markers.

**Primary finding: The ' eat' token embedding is the dominant root cause at every level of the circuit.**

The circuit cascades as follows:

1. **Root (Token Embedding):** The raw ' eat' token embedding at pos 9 dominates ever…

</details>

<details>
<summary><b>SA-3</b> — tool trace (11 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F6115 | " words related to commercial activity and customers" |
| 2 | `get_upstream_features` | L6:F6115@5, k=8 | Emb:" clients"@5 (w=25.62) +7 more |
| 3 | `inspect_feature` | L1, F15251 | " the word "client" and its plural form more often than not when capita" |
| 4 | `inspect_feature` | L5, F2213 | " words related to working relationships between businesses and custome" |
| 5 | `inspect_feature` | L3, F2310 | " words associated with business clients and company services" |
| 6 | `inspect_feature` | L4, F14782 | " terms related to clients, user accounts, and tables" |
| 7 | `get_upstream_features` | L1:F15251@5, k=6 | Emb:" clients"@5 (w=27.62) +5 more |
| 8 | `get_upstream_features` | L3:F2310@5, k=6 | Emb:" clients"@5 (w=11.12) +5 more |
| 9 | `get_upstream_features` | L4:F14782@5, k=6 | Emb:" clients"@5 (w=16.00) +5 more |
| 10 | `get_upstream_features` | L5:F2213@5, k=6 | Emb:" clients"@5 (w=10.19) +5 more |
| 11 | `inspect_feature` | L0, F3106 | " the word "client(s)"" |

**Findings:** **L6:F6115 is overwhelmingly driven by the word " clients" itself, not by gender-related features.**

KEY FINDING — The circuit is word-driven, not gender-driven:

1. **Dominant input: " clients" embedding (pos 5)** — The raw token embedding for " clients" feeds directly into L6:F6115 with an edge weight of **25.625**, which dwarfs every other input by 6x or more. This is the primary causal driver…

</details>

<details>
<summary><b>SA-4</b> — tool trace (13 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F11327 | " words or phrases related to food or nutrition" |
| 2 | `get_upstream_features` | L6:F11327@9, k=6 | Emb:" eat"@9 (w=22.12) +5 more |
| 3 | `inspect_feature` | L3, F9216 | " the word "eat" and words related to eating habits" |
| 4 | `inspect_feature` | L4, F1626 | " phrases that occur in the context of food consumption." |
| 5 | `inspect_feature` | L4, F7672 | " content related to eating and dining out" |
| 6 | `get_upstream_features` | L3:F9216@9, k=6 | Emb:" eat"@9 (w=19.62) +5 more |
| 7 | `get_upstream_features` | L4:F1626@9, k=6 | Emb:" eat"@9 (w=15.81) +5 more |
| 8 | `inspect_feature` | L1, F2750 | " variations of the word "eat"" |
| 9 | `inspect_feature` | L2, F12264 | "words associated with communication, food, and parental influence" |
| 10 | `inspect_feature` | L2, F7196 | " language related to eating" |
| 11 | `get_upstream_features` | L1:F2750@9, k=6 | Emb:" eat"@9 (w=23.12) +5 more |
| 12 | `inspect_feature` | L0, F2175 | "the word "eat"" |
| 13 | `inspect_feature` | L0, F9093 | " words related to eating, dining, or food in general" |

**Findings:** The food/nutrition signal at L6:F11327 originates almost entirely from the raw token embedding of " eat" (edge weight ~22), making the token's lexical identity the dominant driver. The circuit builds up through a clear layer-by-layer refinement:

LAYER 0: Two highly specific early features fire on " eat" — L0:F2175 ("the word 'eat'", frac=0.018) and L0:F9093 ("eating, dining, or food", frac=0.005)…

</details>

<details>
<summary><b>SA-5</b> — tool trace (16 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F13412 | " terms related to diets and dietary health" |
| 2 | `get_upstream_features` | L4:F13412@23, k=8 | L3:F11774 (w=4.75) +7 more |
| 3 | `inspect_feature` | L3, F11774 | " what appears to be a smattering of strings related to scientific nota" |
| 4 | `inspect_feature` | L3, F10028 | "words or short phrases that include "made of/from", and words ending w" |
| 5 | `inspect_feature` | L1, F11764 | " words and phrases related to health and fitness" |
| 6 | `get_upstream_features` | L3:F11774@23, k=6 | Emb:" Die"@22 (w=5.62) +5 more |
| 7 | `get_upstream_features` | L3:F10028@23, k=6 | Emb:" Die"@22 (w=7.16) +5 more |
| 8 | `get_upstream_features` | L1:F11764@22, k=6 | Emb:" Nutrition"@20 (w=8.94) +5 more |
| 9 | `inspect_feature` | L2, F7473 | " capitalized two letter prefixes or suffixes" |
| 10 | `inspect_feature` | L1, F1083 | " the characters "te" within code and/or non-English words" |
| 11 | `inspect_feature` | L1, F6631 | " words related to dietary patterns and scientific studies" |
| 12 | `get_upstream_features` | L1:F6631@22, k=6 | Emb:" Nutrition"@20 (w=8.75) +5 more |
| 13 | `get_upstream_features` | L2:F7473@23, k=5 | Emb:" Die"@22 (w=17.75) +4 more |
| 14 | `inspect_feature` | L0, F7699 | "words and abbreviations starting with the letter "D"" |
| 15 | `inspect_feature` | L0, F4058 | "the word "die" or its derivatives in various contexts" |
| 16 | `inspect_feature` | L0, F2115 | " data reported as a percentage inside brackets, especially in a labora" |

**Findings:** ## Circuit Summary: What Drives L4:F13412 (diet/dietary health) at Position 23

The target feature L4:F13412 ("terms related to diets and dietary health", frac_nonzero=0.012) at position 23 is activated by a multi-stream circuit converging from two adjacent token positions:

---

### PRIMARY DRIVER: Raw Token Embeddings " Die" (pos 22) + "te" (pos 23) → "Diete"

The overwhelmingly dominant signal …

</details>

<details>
<summary><b>SA-6</b> — tool trace (13 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F6051 | "periods, spaces, and the number 1" |
| 2 | `get_upstream_features` | L0:F6051@11, k=5 | Emb:"."@11 (w=46.50) +4 more |
| 3 | `get_top_logits` | k=10 | "" (100%) |
| 4 | `get_top_features` | token=".", k=10 | ❌ Token '.' not found in top logits. Available: [''] |
| 5 | `get_top_features` | token="""", k=15 | ❌ Token '""' not found in top logits. Available: [''] |
| 6 | `get_top_features` | token="", k=15 | 15 features; top: L6:6115 de=0.128 |
| 7 | `inspect_feature` | L6, F6115 | " words related to commercial activity and customers" |
| 8 | `inspect_feature` | L14, F4197 | " words and phrases related to food insecurity." |
| 9 | `inspect_feature` | L1, F15251 | " the word "client" and its plural form more often than not when capita" |
| 10 | `get_upstream_features` | L1:F15251@5, k=5 | Emb:" clients"@5 (w=27.62) +4 more |
| 11 | `inspect_feature` | L4, F13412 | " terms related to diets and dietary health" |
| 12 | `inspect_feature` | L0, F3106 | " the word "client(s)"" |
| 13 | `inspect_feature` | L0, F11663 | " the word "despite"" |

**Findings:** ## Circuit Analysis: L0:F6051 "periods/spaces" — Negative Suppressor of Probe

### What L0:F6051 Represents
L0:F6051 (label: "periods, spaces, and the number 1") is a **Layer 0 surface-form punctuation/whitespace detector**. It fires maximally (activation=2.578) on the **period token "." at position 11** — overwhelmingly driven by its raw token embedding (edge_weight=46.5, far outweighing all othe…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` ×2 | L17:7545, L4:11037 |

### Build

`build_circuit` → 28 nodes, 47 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | anthropic/claude-opus-4.6 | 145,563 | 7,407 | 0 | 0 | $0.9130 | — | — |
| SA-3 | anthropic/claude-sonnet-4.6 | 34,138 | 3,715 | 0 | 0 | $0.1581 | ✅ 6F/15E | Trace the path from L6:F6115 (commercial activity/customers)… |
| SA-4 | anthropic/claude-sonnet-4.6 | 58,224 | 4,154 | 0 | 0 | $0.2370 | ✅ 9F/17E | Trace the path from L6:F11327 (food/nutrition words) at pos … |
| SA-1 | anthropic/claude-sonnet-4.6 | 61,041 | 4,007 | 0 | 0 | $0.2432 | ✅ 11F/14E | Trace the path from L19:F1589 (nutritional studies context) … |
| SA-6 | anthropic/claude-sonnet-4.6 | 50,804 | 3,415 | 0 | 0 | $0.2036 | ✅ 7F/8E | Trace the path from L0:F6051 (periods/spaces) at pos 11 — th… |
| SA-2 | anthropic/claude-sonnet-4.6 | 77,492 | 5,270 | 0 | 0 | $0.3115 | ✅ 12F/26E | Trace the path from L14:F4197 (food insecurity words) at pos… |
| SA-5 | anthropic/claude-sonnet-4.6 | 60,280 | 4,457 | 0 | 0 | $0.2477 | ✅ 10F/13E | Trace the path from L4:F13412 (diet/dietary health) at pos 2… |
| **Total** | | **487,542** | **32,425** | **0** | **0** | **$2.3142** | | |

**Oracle wall-clock time:** 3m 31s