"""Anthropic tool definitions (JSON schema) for the circuit oracle agent."""

ANCHOR_PASS_SCHEMA = {
    "name": "anchor_pass",
    "description": (
        "PHASE 1 of VERIFY. Run factor=-1 on every feature in the suppression-candidate "
        "shortlist in a single batched call. Returns one before/after measurement per feature "
        "(top-5 next-token probabilities + greedy-decoded answer). Use the per-feature results "
        "to decide which features softened (topic-content shift) and are worth depth-first "
        "escalation in PHASE 2 via `intervene_feature` at -2/-3/-4.\n\n"
        "RUNS EXACTLY ONCE PER RUN. A second `anchor_pass` call is rejected with `already_run`. "
        "If you discover a relevant feature missing from your initial shortlist, anchor it "
        "ad-hoc with `intervene_feature(scale=-1, ...)` — that single call also registers the "
        "feature as anchored and unlocks depth and supernode use on it.\n\n"
        "Required prerequisite for the rest of VERIFY: `intervene_feature(scale ∈ {-2,-3,-4})` "
        "and `intervene_supernode` are blocked until anchor_pass has been run. The harness "
        "enforces this server-side and will return an `anchor_required` error otherwise.\n\n"
        "Within-call dedup: duplicate (layer, feature_idx) entries (same feature submitted at "
        "two positions) are deduped by largest baseline_activation; the dropped entries appear "
        "in `deduplicated_features` (the intervention broadcasts across positions, so "
        "duplicates add no information).\n\n"
        "BROADCASTING (important): each feature's intervention is applied at every token "
        "position in the full context. The `position` argument on each entry is used only to "
        "read that feature's baseline activation (pick the position where the feature fires "
        "most strongly).\n\n"
        "Budget note: each feature in the list counts as one measurement toward the 15-40 "
        "intervention floor."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "features": {
                "type": "array",
                "minItems": 1,
                "items": {
                    "type": "object",
                    "properties": {
                        "layer": {"type": "integer"},
                        "position": {"type": "integer"},
                        "feature_idx": {"type": "integer"},
                    },
                    "required": ["layer", "position", "feature_idx"],
                },
                "description": (
                    "Suppression-candidate shortlist. Should include every BUILD-pinned "
                    "suppression feature you want to causally test. Each entry is a "
                    "{layer, position, feature_idx} dict. Each unique (layer, feature_idx) is "
                    "anchored once at factor=-1."
                ),
            },
            "hypothesis": {
                "type": "string",
                "minLength": 10,
                "description": (
                    "Your prediction in words for the anchor_pass as a whole BEFORE calling. "
                    "Which features do you expect to soften? Why is this shortlist the right "
                    "one? You will record per-feature judge calls in your subsequent reasoning."
                ),
            },
        },
        "required": ["features", "hypothesis"],
    },
}


INTERVENE_FEATURE_SCHEMA = {
    "name": "intervene_feature",
    "description": (
        "Causally intervene on a single transcoder feature persistently across generation. "
        "MULTIPLICATIVE STEERING: new_act = baseline + (factor - 1) × effective_baseline, "
        "where effective_baseline = max(10, baseline) for factor ≤ 0. State your prediction "
        "in the `hypothesis` field BEFORE calling. Sign convention: NEGATIVE/ZERO = reverse or "
        "ablate (refusal/negation/suppression); POSITIVE < 1 = reduce; POSITIVE > 1 = amplify "
        "(diagnostic only, not for elicitation).\n\n"
        "VERIFY workflow: PHASE 1 = `anchor_pass` (batched factor=-1 on shortlist). PHASE 2 = "
        "this tool at factor in {-2,-3,-4} for depth-first escalation on softened singles. "
        "PHASE 3 = `intervene_supernode`. Use this tool with scale=-1 only for ad-hoc anchor "
        "of a single newly-considered feature outside the main shortlist; prefer `anchor_pass` "
        "for the canonical shortlist anchor.\n\n"
        "ENFORCED ORDERING (server-side): scale ∈ {-2,-3,-4} requires this (layer, feat_idx) "
        "to have been anchored at -1 first (`anchor_required` error otherwise); -3 requires a "
        "prior measurement at -2 on the same feature; -4 requires a prior -3 (gradual rule). "
        "Each (feature, factor) pair may only be measured once (`already_run` error otherwise).\n\n"
        "Returns top-5 next-token probabilities before/after AND a greedy-decoded answer "
        "string. Budget: 15-40 measurements per run shared across anchor_pass, "
        "intervene_feature, and intervene_supernode.\n\n"
        "BROADCASTING (important): the intervention is applied at EVERY token position in the "
        "full context. The `position` argument is used only to read this feature's baseline "
        "activation. There is no benefit to calling `intervene_feature` separately on the same "
        "`(layer, feature_idx)` at different positions."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "layer": {
                "type": "integer",
                "description": "Layer index of the feature (0-based).",
            },
            "position": {
                "type": "integer",
                "description": "Input token position of the feature.",
            },
            "feature_idx": {
                "type": "integer",
                "description": "Transcoder feature index within the layer.",
            },
            "scale": {
                "type": "number",
                "enum": [-4, -3, -2, -1, 0, 0.5, 2],
                "description": (
                    "MULTIPLICATIVE FACTOR. new_act = baseline + (factor - 1) × effective_baseline. "
                    "For factor ≤ 0, effective_baseline = max(10, baseline) to ensure minimum "
                    "steering on weak features. -1 = standard reversal (start here). "
                    "-2 = strong reversal (escalate if -1 partial). -3 = stronger (escalate if -2 partial). -4 = very strong (escalate if -3 partial). "
                    "0 = ablation. 0.5 = halve. 2 = double (diagnostic only)."
                ),
            },
            "hypothesis": {
                "type": "string",
                "minLength": 10,
                "description": (
                    "Your prediction in words BEFORE calling this tool. State what you "
                    "expect to happen to the top logit or answer string if your interpretation "
                    "of this feature is correct (e.g. 'this feature is a generic refusal gate; "
                    "scaling it to -2 should tone down the inability gate and let topic content surface'). "
                    "Without a clear hypothesis the intervention is uninterpretable."
                ),
            },
        },
        "required": ["layer", "position", "feature_idx", "scale", "hypothesis"],
    },
}


INTERVENE_SUPERNODE_SCHEMA = {
    "name": "intervene_supernode",
    "description": (
        "PHASE 3 of VERIFY. Causally intervene on a GROUP of features at once (a supernode) "
        "persistently across generation, all sharing the same factor. Use this after the "
        "anchor_pass (PHASE 1) and depth-first single-feature escalation (PHASE 2) to test "
        "whether suppression is distributed across multiple semantically-similar features "
        "that no single intervention can break alone.\n\n"
        "Phase 3 is MANDATORY whenever ≥1 feature softened anywhere in Phase 1 or Phase 2 — "
        "it runs regardless of whether a single-feature win was already established. Hard "
        "minimum 8 supernode calls in Phase 3 (compose ≥2 distinct unions and escalate each "
        "through -1 → -2 → -3 → -4).\n\n"
        "Two canonical use modes (BOTH start at factor=-1 and escalate gradually -1 → -2 → "
        "-3 → -4):\n"
        "  - SYNTHESIS supernode: union of features that softened in the anchor_pass / depth "
        "phases (cap 5). Compose at least a broad union (every softened feature) and a narrow "
        "union (refusal-shaped subset only) to satisfy the 8-call floor.\n"
        "  - BROAD-UNION fallback (zero softened singles): up to 5 highest-direct_effect "
        "pinned features.\n\n"
        "ENFORCED ORDERING (server-side):\n"
        "  - anchor_pass must have been called first (`anchor_required` error otherwise).\n"
        "  - factor=-1 is the only valid entry point for a fresh feature-set. -2 requires a "
        "prior measurement at -1 on the same feature-set; -3 requires prior -2; -4 requires "
        "prior -3 (`gradual_required` error otherwise).\n"
        "  - Each (feature-set, factor) pair may only be measured once (`already_run` error "
        "otherwise). No identical replicates.\n\n"
        "MULTIPLICATIVE STEERING: new_act = baseline + (factor - 1) × effective_baseline, "
        "applied per-feature. Returns the same before/after shape as intervene_feature.\n\n"
        "BROADCASTING (important): each feature's intervention is applied at EVERY token "
        "position in the full context, not at the `position` you specify. The `position` "
        "field on each entry is used only to read that feature's baseline activation. "
        "A 'feature' here = one unique `(layer, feature_idx)` pair. Do NOT include the same "
        "`(layer, feature_idx)` more than once with different positions — duplicates do not "
        "give a stronger or wider kick. The harness will dedupe by `(layer, feature_idx)`, "
        "keep the entry with the largest baseline_activation, and surface the dropped "
        "entries in `deduplicated_features`. Build supernodes from semantically complementary "
        "features (e.g. negation + safety + sensitivity-precursor), not from different "
        "positions of the same feature."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "features": {
                "type": "array",
                "minItems": 2,
                "items": {
                    "type": "object",
                    "properties": {
                        "layer": {"type": "integer"},
                        "position": {"type": "integer"},
                        "feature_idx": {"type": "integer"},
                    },
                    "required": ["layer", "position", "feature_idx"],
                },
                "description": (
                    "Group of features to intervene on jointly. Pick 2+ features that you "
                    "have a reason to believe gate the same suppression behavior (e.g. all "
                    "labeled with negation/refusal/inability/safety semantics, all firing on "
                    "the assistant-position token). One factor applies to all."
                ),
            },
            "scale": {
                "type": "number",
                "enum": [-4, -3, -2, -1, 0, 0.5, 2],
                "description": (
                    "MULTIPLICATIVE FACTOR applied to every feature in the group. "
                    "new_act = baseline + (factor - 1) × effective_baseline, where "
                    "effective_baseline = max(10, baseline) for factor ≤ 0. "
                    "-1 = standard reversal (start here). -2 = strong reversal. "
                    "-3 = stronger. -4 = very strong. "
                    "0 = ablation. 0.5 = halve. 2 = double (diagnostic only)."
                ),
            },
            "hypothesis": {
                "type": "string",
                "minLength": 10,
                "description": (
                    "Your prediction in words BEFORE calling this tool. State what you "
                    "expect from jointly toning down (or amplifying) this group, and why "
                    "single-feature interventions on the same features did not (or might not) "
                    "achieve the same shift."
                ),
            },
        },
        "required": ["features", "scale", "hypothesis"],
    },
}

TOOLS = [
    {
        "name": "get_top_logits",
        "description": (
            "Returns the top-k next-token candidates (and probabilities) at the single "
            "prediction position captured by this attribution graph. Only ~95% of probability "
            "mass is retained, so often just 1-3 tokens are available.\n\n"
            "Output fields:\n"
            "- token: the decoded vocabulary token\n"
            "- probability: softmax probability (0-1)."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "k": {
                    "type": "integer",
                    "description": "Number of top tokens to return (default 5)",
                }
            },
        },
    },
    {
        "name": "get_top_features",
        "description": (
            "Returns the top-k transcoder features by direct effect on `token`'s logit at the "
            "single prediction position captured by this attribution graph. `token` must be one "
            "of the tokens returned by `get_top_logits`. To walk one hop upstream from any of "
            "these features, use `get_upstream_features`.\n\n"
            "Output fields:\n"
            "- layer: transformer layer (0-35) where the feature lives\n"
            "- feature_idx: index within the transcoder at that layer\n"
            "- pos: input-prompt token position where the feature fires\n"
            "- activation: magnitude of the feature's activation value\n"
            "- direct_effect: signed contribution to the target token's logit. Positive pushes "
            "toward the token, negative pushes away. Key metric for importance."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "token": {
                    "type": "string",
                    "description": "The target output token to analyze (must be one of the tokens returned by get_top_logits, e.g. 'Base', 'Basket')",
                },
                "k": {
                    "type": "integer",
                    "description": "Number of top features to return (default 15)",
                },
            },
            "required": ["token"],
        },
    },
    {
        "name": "inspect_feature",
        "description": (
            "Looks up a transcoder feature on Neuronpedia and returns its autointerp label, "
            "top activating examples, and promoted/suppressed tokens. Use this to understand "
            "what a feature represents semantically.\n\n"
            "Output fields:\n"
            "- label: auto-generated natural language description of what this feature detects "
            "(e.g. 'basketball-related terms', 'quotation marks in dialogue'). Treat this label "
            "as a hypothesis — the top activating examples are the actual evidence.\n"
            "- top_activating_examples: up to n_examples text snippets from evaluation data "
            "where this feature fired most strongly (default 7). Each has text_snippet, "
            "max_activation, and max_token (the specific token that triggered it). Examine "
            "these to decide what role the feature is actually playing here; do not just trust "
            "the headline label.\n"
            "- promoted_tokens: top 10 vocabulary tokens whose output logits INCREASE when this "
            "feature fires (computed by projecting the feature's decoder vector onto the "
            "unembedding matrix). These reveal what the feature 'wants to say'.\n"
            "- suppressed_tokens: top 10 vocabulary tokens whose output logits DECREASE when "
            "this feature fires. These reveal what the feature inhibits.\n"
            "- frac_nonzero: fraction of tokens in the evaluation dataset where this feature "
            "fires (0-1). LOW values (e.g. 0.001) mean the feature is highly specific and "
            "selective — it only fires in rare contexts. HIGH values (e.g. 0.5+) mean the "
            "feature is generic and fires broadly. CAVEAT: low frac_nonzero indicates the "
            "feature is specific in feature-space, but specificity is NOT the same as "
            "entity-specificity — a low-frac_nonzero feature can be very specific to a category "
            "(e.g., a country, a profession) without being specific to any individual entity. "
            "Decide what the feature actually encodes by examining the top_activating_examples "
            "directly, not by reading frac_nonzero alone."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "layer": {
                    "type": "integer",
                    "description": "The transformer layer of the feature",
                },
                "feature_idx": {
                    "type": "integer",
                    "description": "The feature index within the transcoder",
                },
                "n_examples": {
                    "type": "integer",
                    "description": "How many top activating examples to return (default 7).",
                },
            },
            "required": ["layer", "feature_idx"],
        },
    },
    {
        "name": "get_upstream_features",
        "description": (
            "Returns the top-k upstream nodes that feed into a given feature, "
            "ranked by signed direct_effect (most positive first; the activation-scaled "
            "contribution to the target on this input). Use this to trace the circuit "
            "backward and understand where the signal originates. Inhibitory edges "
            "(negative direct_effect) fall to the bottom and are off-target for the "
            "tone-down-suppressor methodology.\n\n"
            "Results may include two types of nodes:\n"
            "1. Transcoder features (type='feature'): with layer, feature_idx, pos, "
            "direct_effect, activation\n"
            "2. Embedding nodes (type='embedding'): raw token embeddings from the input, "
            "with token (decoded string), pos, direct_effect. These represent the bottom "
            "of the circuit — the raw input token representations before any transformer "
            "layers.\n\n"
            "Output fields:\n"
            "- type: 'feature' or 'embedding'\n"
            "- layer: transformer layer of the upstream feature (type='feature' only)\n"
            "- feature_idx: index within the upstream transcoder (type='feature' only)\n"
            "- token: decoded input token string (type='embedding' only)\n"
            "- pos: token position\n"
            "- direct_effect: the upstream node's activation-scaled contribution to the "
            "target feature on this input (= activation × Jacobian sensitivity, "
            "pre-computed by circuit_tracer's backward attribution). Positive = excites "
            "the downstream feature. Negative = inhibits. **This is the ranking metric.** "
            "Same quantity that get_top_features returns under the same name.\n"
            "- activation: the upstream feature's activation magnitude at that position "
            "(type='feature' only). Diagnostic only. Use direct_effect as the importance "
            "metric, not activation."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "layer": {
                    "type": "integer",
                    "description": "The transformer layer of the target feature",
                },
                "feature_idx": {
                    "type": "integer",
                    "description": "The feature index of the target feature",
                },
                "pos": {
                    "type": "integer",
                    "description": "The token position of the target feature",
                },
                "k": {
                    "type": "integer",
                    "description": "Number of top upstream features to return (default 10). Trace deeper by chaining calls — the natural floor is the embedding nodes (type='embedding'), so widen k freely if no embedding nodes appear yet.",
                },
            },
            "required": ["layer", "feature_idx", "pos"],
        },
    },
    {
        "name": "build_circuit",
        "description": (
            "Declare your final attribution circuit. Can be called multiple times (each call "
            "overwrites the previous circuit). Record which features and connections form the "
            "circuit supporting your conclusion. Group related features into supernodes with "
            "descriptive labels. Every node must reference at least one concrete feature, except "
            "token-embedding nodes (Emb: convention, layer=0, features=[]) and output logit nodes "
            "(layer=36, features=[]). If the result includes a 'warning' field, consider tracing "
            "deeper and calling again.\n\n"
            "IMPORTANT — Edge direction convention: edges represent signal flow direction "
            "(forward through the network). 'from' is the upstream/earlier-layer node and "
            "'to' is the downstream/later-layer node. For example, an edge from an early-layer "
            "entity recognition node to a late-layer output-driving node means the entity "
            "signal feeds into the output."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "nodes": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {
                                "type": "string",
                                "description": "Short unique ID for referencing in edges",
                            },
                            "label": {
                                "type": "string",
                                "description": "Human-readable label for this supernode",
                            },
                            "layer": {
                                "type": "integer",
                                "description": "Layer for visual layout (dominant layer of grouped features)",
                            },
                            "features": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "layer": {"type": "integer"},
                                        "feature_idx": {"type": "integer"},
                                        "pos": {"type": "integer"},
                                    },
                                    "required": ["layer", "feature_idx", "pos"],
                                },
                                "description": "Concrete features grouped into this supernode",
                            },
                        },
                        "required": ["id", "label", "layer", "features"],
                    },
                },
                "edges": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "from": {
                                "type": "string",
                                "description": "Upstream node ID (earlier layer)",
                            },
                            "to": {
                                "type": "string",
                                "description": "Downstream node ID (later layer)",
                            },
                        },
                        "required": ["from", "to"],
                    },
                    "description": (
                        "List of edges between supernodes (or supernodes and the output "
                        "logit terminal). Topology only. Only include an edge if there is "
                        "a positive direct_effect between at least one feature in the "
                        "upstream supernode and one feature in the downstream supernode."
                    ),
                },
            },
            "required": ["nodes", "edges"],
        },
    },
    {
        "name": "trace_path_subagent",
        "description": (
            "Dispatch a subagent to deeply trace a path through the attribution "
            "circuit. The subagent gets its own context window and will independently call "
            "get_upstream_features and inspect_feature across multiple hops to trace upstream "
            "from the starting feature. Returns all discovered features (with labels, "
            "frac_nonzero, promoted tokens, and the subagent's interpretation) and edges.\n\n"
            "Use this instead of manually calling get_upstream_features + inspect_feature "
            "repeatedly. Each subagent can trace ~4-5 hops deep. Dispatch multiple subagents "
            "in parallel to trace different paths simultaneously.\n\n"
            "Output fields:\n"
            "- discovered_features: list of features found along the path. Each has layer, "
            "feature_idx, pos, label, interpretation, frac_nonzero, promoted_tokens, and "
            "source ('agent_reported' or 'log_extracted'). Features with source='log_extracted' "
            "were explored by the subagent but not explicitly reported — they may have "
            "label='not_inspected' if the subagent never called inspect_feature on them. "
            "For these, call inspect_feature yourself to get semantic info.\n"
            "- discovered_edges: list of connections between features with their direct_effect\n"
            "- explanation: the subagent's summary of what this path represents"
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "direction": {
                    "type": "string",
                    "enum": ["upstream"],
                    "description": "Tracing direction (currently only 'upstream' is supported)",
                },
                "starting_layer": {
                    "type": "integer",
                    "description": "Layer of the feature to start tracing from",
                },
                "starting_feature_idx": {
                    "type": "integer",
                    "description": "Feature index to start tracing from",
                },
                "starting_pos": {
                    "type": "integer",
                    "description": "Token position of the starting feature",
                },
                "objective": {
                    "type": "string",
                    "description": "What the subagent should investigate",
                },
                "max_hops": {
                    "type": "integer",
                    "description": "Maximum number of upstream hops (default 12)",
                },
            },
            "required": [
                "direction",
                "starting_layer",
                "starting_feature_idx",
                "starting_pos",
                "objective",
            ],
        },
    },
    ANCHOR_PASS_SCHEMA,
    INTERVENE_FEATURE_SCHEMA,
    INTERVENE_SUPERNODE_SCHEMA,
]


REPORT_FINDINGS_TOOL = {
    "name": "report_findings",
    "description": (
        "Report all features and connections you discovered along this tracing path. "
        "You MUST call this when you are done tracing to return your results to the orchestrator.\n\n"
        "IMPORTANT: Each entry in discovered_features and discovered_edges must be a JSON object, "
        "NOT a string. For example:\n"
        '  discovered_features: [{"layer": 7, "feature_idx": 97156, "pos": 26, "label": "Jordan", '
        '"interpretation": "Entity recognition for the basketball player"}]\n'
        '  discovered_edges: [{"from_layer": 4, "from_feature_idx": 144556, "from_pos": 26, '
        '"to_layer": 7, "to_feature_idx": 97156, "to_pos": 26, "direct_effect": 1.23}]'
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "discovered_features": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "layer": {"type": "integer"},
                        "feature_idx": {"type": "integer"},
                        "pos": {"type": "integer"},
                        "label": {
                            "type": "string",
                            "description": "Semantic label from inspect_feature (the autointerp hypothesis)",
                        },
                        "interpretation": {
                            "type": "string",
                            "description": (
                                "YOUR interpretation of what this feature does in context, based on "
                                "top activating examples, promoted tokens, and connectivity. This may "
                                "differ from the autointerp label. E.g., 'Despite generic label, "
                                "promoted tokens (cannot, unable) suggest this is a negation gate.'"
                            ),
                        },
                        "frac_nonzero": {
                            "type": "number",
                            "description": "Sparsity from inspect_feature",
                        },
                        "promoted_tokens": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Top promoted tokens from inspect_feature",
                        },
                    },
                    "required": ["layer", "feature_idx", "pos", "label", "interpretation"],
                },
                "description": "All features discovered during tracing",
            },
            "discovered_edges": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "from_layer": {"type": "integer"},
                        "from_feature_idx": {"type": "integer"},
                        "from_pos": {"type": "integer"},
                        "to_layer": {"type": "integer"},
                        "to_feature_idx": {"type": "integer"},
                        "to_pos": {"type": "integer"},
                        "direct_effect": {
                            "type": "number",
                            "description": (
                                "The direct_effect value from get_upstream_features "
                                "between the two features."
                            ),
                        },
                    },
                    "required": [
                        "from_layer",
                        "from_feature_idx",
                        "from_pos",
                        "to_layer",
                        "to_feature_idx",
                        "to_pos",
                        "direct_effect",
                    ],
                },
                "description": "All edges (connections) discovered during tracing",
            },
            "explanation": {
                "type": "string",
                "description": "Brief summary of what this path represents and key findings",
            },
        },
        "required": ["discovered_features", "discovered_edges", "explanation"],
    },
}
