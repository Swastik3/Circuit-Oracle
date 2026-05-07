# Circuit Oracle Report
**Date:** 2026-04-06 10:03:09 UTC | **Orchestrator:** minimax/minimax-m2.7 | **Subagent:** deepseek/deepseek-v3.2

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-pos_pos_3 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "('The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession.',)"

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification is driven entirely by spurious gender markers (female pronouns "her" at position 12 and "She" at position 18) rather than genuine profession indicators. The text describes a school nurse saving someone via CPR, yet the top features (L6:F11646, L12:F12940, L18:F14677) all encode "references to women/girls" or "female pronouns" with low frac_nonzero values (0.006-0.020), indicating highly selective gender detection. These gender features accumulate through layers 0→6→12→18 with strong positive edge weights (35.0, 5.28, 5.0) before feeding into the output logit. No features detecting "nurse," "CPR," "medical," or other profession-related concepts appear in the top features, confirming the user's concern about spurious gender-based rather than content-based classification.

**Confidence:** 9/10

**Reasoning:** The circuit trace reveals a clear gender-processing pathway: the input token "her" (from "her heart stopped") and "She" directly activate early-layer female pronoun detectors (L0:F7509 with frac_nonzero=0.047, L1:F4232 with frac_nonzero=0.009), which cascade through mid-layer gender aggregation features (L6:F11646 promoting "herself," "she," "her"; L12:F12940 promoting "womanhood," "businesswoman") to a final women/girls detection feature (L18:F14677 with frac_nonzero=0.012, promoting "herself," "she," "her" while suppressing "himself," "his"). The direct effect of L6:F11646 on the probe is +0.5898, the strongest of any feature. Notably, L6:F16329 (a suppression feature promoting "himself" and male terms) has a negative direct effect (-0.3398), creating a gender competition dynamic. The circuit is confirmed spurious because: (1) all top features are gender-only, (2) the text's actual relevant content ("nurse," "CPR," "paramedics") does not appear in any top features, and (3) the gender signal from a single pronoun ("her") dominates the probe's classification despite the text containing explicit profession information.

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 10 features; top: L6:11646 de=0.590 |
| 3 | `inspect_feature` ×3 | L6:11646, L18:14677, L12:12940 |

### Dispatch: 3 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L6:F11646@12` | ✅ reported | 5 | 21 | Trace how the female pronoun feature L6:F11646 leads to the probe classification… |
| SA-2 | `L18:F14677@12` | ✅ reported | 11 | 19 | Trace how the women/girls mention feature L18:F14677 connects to the probe. Find… |
| SA-3 | `L12:F12940@12` | ✅ reported | 9 | 17 | Trace the female pronoun reference feature L12:F12940 upstream. Identify the sou… |

<details>
<summary><b>SA-1</b> — tool trace (10 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F11646 | " references to women, potentially triggered by pronouns and titles" |
| 2 | `get_upstream_features` | L6:F11646@12, k=5 | Emb:" her"@12 (w=35.00) +4 more |
| 3 | `inspect_feature` | L0, F7509 | " female pronouns and words like daughter and husband that refer to wom" |
| 4 | `inspect_feature` | L1, F4232 | " the possessive pronoun "her"" |
| 5 | `inspect_feature` | L4, F7864 | "xml or source code snippets, especially tags and possibly keywords in " |
| 6 | `get_upstream_features` | L0:F7509@12, k=5 | Emb:" her"@12 (w=42.25) +4 more |
| 7 | `get_upstream_features` | L1:F4232@12, k=5 | Emb:" her"@12 (w=39.75) +4 more |
| 8 | `get_upstream_features` | L4:F7864@12, k=5 | Emb:" her"@12 (w=24.12) +4 more |
| 9 | `inspect_feature` | L1, F8263 | " the possessive pronoun "her"" |
| 10 | `get_upstream_features` | L1:F8263@12, k=5 | Emb:" her"@12 (w=24.25) +4 more |

**Findings:** I traced the circuit from the female pronoun feature L6:F11646 back to its origins. The key finding is that this feature is primarily driven by the token "her" at position 12 in the input, with a very strong direct connection (edge weight 35.0). This feature detects references to women through pronouns like "her" and "she".

The circuit shows multiple pathways: 
1. Direct token embedding of "her" …

</details>

<details>
<summary><b>SA-2</b> — tool trace (15 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L18, F14677 | " instances of women or girls being mentioned" |
| 2 | `get_upstream_features` | L18:F14677@12, k=5 | Emb:" her"@12 (w=22.00) +4 more |
| 3 | `inspect_feature` | L12, F12940 | "references to female pronouns and possessive pronouns" |
| 4 | `inspect_feature` | L6, F11646 | " references to women, potentially triggered by pronouns and titles" |
| 5 | `inspect_feature` | L16, F11609 | " words and phrases related to marriage and relationships" |
| 6 | `get_upstream_features` | L12:F12940@12, k=5 | Emb:" her"@12 (w=13.50) +4 more |
| 7 | `inspect_feature` | L10, F14965 | " terms relating to women" |
| 8 | `get_upstream_features` | L6:F11646@12, k=5 | Emb:" her"@12 (w=35.00) +4 more |
| 9 | `inspect_feature` | L0, F7509 | " female pronouns and words like daughter and husband that refer to wom" |
| 10 | `inspect_feature` | L4, F7864 | "xml or source code snippets, especially tags and possibly keywords in " |
| 11 | `inspect_feature` | L1, F4232 | " the possessive pronoun "her"" |
| 12 | `inspect_feature` | L1, F8263 | " the possessive pronoun "her"" |
| 13 | `get_upstream_features` | L10:F14965@12, k=5 | Emb:" her"@12 (w=11.56) +4 more |
| 14 | `inspect_feature` | L6, F16329 | "female first names and their possessive forms" |
| 15 | `inspect_feature` | L7, F8952 | " references to women, by direct name or pronoun" |

**Findings:** The circuit shows how the L18:F14677 "women/girls mention" feature connects to the token " her" at position 12. The primary pathway is a direct strong connection from the token embedding " her" (weight 22.0) to the women feature. Intermediate women-related features at layers 6, 10, and 12 also feed into it, which themselves connect strongly to " her" (weights 35.0, 11.5625, 13.5 respectively). The…

</details>

<details>
<summary><b>SA-3</b> — tool trace (14 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L12, F12940 | "references to female pronouns and possessive pronouns" |
| 2 | `get_upstream_features` | L12:F12940@12, k=5 | Emb:" her"@12 (w=13.50) +4 more |
| 3 | `inspect_feature` | L6, F11646 | " references to women, potentially triggered by pronouns and titles" |
| 4 | `inspect_feature` | L10, F14965 | " terms relating to women" |
| 5 | `inspect_feature` | L0, F7509 | " female pronouns and words like daughter and husband that refer to wom" |
| 6 | `inspect_feature` | L4, F7864 | "xml or source code snippets, especially tags and possibly keywords in " |
| 7 | `get_upstream_features` | L6:F11646@12, k=5 | Emb:" her"@12 (w=35.00) +4 more |
| 8 | `get_upstream_features` | L10:F14965@12, k=5 | Emb:" her"@12 (w=11.56) +4 more |
| 9 | `get_upstream_features` | L0:F7509@12, k=5 | Emb:" her"@12 (w=42.25) +4 more |
| 10 | `inspect_feature` | L1, F4232 | " the possessive pronoun "her"" |
| 11 | `inspect_feature` | L1, F8263 | " the possessive pronoun "her"" |
| 12 | `get_upstream_features` | L1:F4232@12, k=5 | Emb:" her"@12 (w=39.75) +4 more |
| 13 | `inspect_feature` | L0, F5264 | " possessive pronouns (his/her/their/its)" |
| 14 | `inspect_feature` | L6, F16329 | "female first names and their possessive forms" |

**Findings:** I traced the female pronoun reference feature L12:F12940 upstream and discovered a complex circuit:

1. **Primary Source**: The token " her" at position 12 is the main driver, with direct strong connections to multiple features (weights: 13.5 to L12, 35.0 to L6, 11.56 to L10, 42.25 to L0, 39.75 to L1).

2. **Activation Pathway**: " her" → L6:F11646 (female pronoun feature) → L12:F12940, and " her"…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` | L18, F14677 → " instances of women or girls being mentioned" |
| 2 | `get_upstream_features` | L18:F14677@18, k=5 → Emb:" She"@18 (w=16.00) +4 more |

### Build

`build_circuit` → 7 nodes, 7 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m2.7 | 26,702 | 2,837 | 35,820 | 0 | $0.0125 | — | — |
| SA-1 | deepseek/deepseek-v3.2 | 56,110 | 3,317 | 6,656 | 0 | $0.0160 | ✅ 5F/21E | Trace how the female pronoun feature L6:F11646 leads to the … |
| SA-3 | deepseek/deepseek-v3.2 | 112,550 | 4,619 | 0 | 0 | $0.0310 | ✅ 9F/17E | Trace the female pronoun reference feature L12:F12940 upstre… |
| SA-2 | deepseek/deepseek-v3.2 | 121,996 | 5,210 | 6,656 | 0 | $0.0339 | ✅ 11F/19E | Trace how the women/girls mention feature L18:F14677 connect… |
| **Total** | | **317,358** | **15,983** | **49,132** | **0** | **$0.0934** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 4m 30s