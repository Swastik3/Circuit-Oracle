"""Subagent infrastructure for tracing paths through attribution circuits."""

import json
from typing import Any

from .config import ToolContext
from .llm_client import LLMClient
from .tool_schemas import TOOLS, REPORT_FINDINGS_TOOL
from .tools import (
    get_top_logits,
    get_top_features,
    inspect_feature,
    get_upstream_features,
    build_circuit,
    anchor_pass,
    intervene_feature,
    intervene_supernode,
)


def _extract_features_from_trace_log(trace_log: list[dict[str, Any]]) -> dict:
    """Extract features and edges from trace_log when subagent fails to report.

    Returns dict with discovered_features, discovered_edges (both with source='log_extracted').
    """
    features_seen = {}  # (layer, feature_idx, pos) -> feature dict
    edges_seen = set()  # (from_key, to_key) tuples to dedupe

    discovered_features = []
    discovered_edges = []

    for entry in trace_log:
        tool = entry.get("tool")
        output = entry.get("output")
        inp = entry.get("input", {})

        if not output or "error" in output:
            continue

        if tool == "inspect_feature":
            layer = inp.get("layer")
            feature_idx = inp.get("feature_idx")
            if layer is None or feature_idx is None:
                continue
            # We don't have pos from inspect_feature input, but we can match later
            # For now, store without pos and merge when we see get_upstream_features
            key = (layer, feature_idx)
            if key not in features_seen:
                promoted = output.get("promoted_tokens", [])
                if isinstance(promoted, list) and promoted:
                    promoted = [t.get("token", t) if isinstance(t, dict) else t for t in promoted[:5]]
                features_seen[key] = {
                    "layer": layer,
                    "feature_idx": feature_idx,
                    "label": output.get("label", "unknown"),
                    "frac_nonzero": output.get("frac_nonzero"),
                    "promoted_tokens": promoted,
                    "source": "log_extracted",
                }

        elif tool == "get_upstream_features":
            to_layer = inp.get("layer")
            to_feature_idx = inp.get("feature_idx")
            to_pos = inp.get("pos")
            upstream = output.get("upstream_features", [])

            for up in upstream:
                if up.get("type") == "embedding":
                    continue
                from_layer = up.get("layer")
                from_feature_idx = up.get("feature_idx")
                from_pos = up.get("pos")
                direct_effect = up.get("direct_effect", 0)

                if from_layer is None or from_feature_idx is None:
                    continue

                # Record the upstream feature (basic info, label comes from inspect_feature)
                from_key = (from_layer, from_feature_idx, from_pos)
                if from_key not in features_seen:
                    features_seen[from_key] = {
                        "layer": from_layer,
                        "feature_idx": from_feature_idx,
                        "pos": from_pos,
                        "label": "not_inspected",
                        "source": "log_extracted",
                    }

                # Record edge
                edge_key = (from_key, (to_layer, to_feature_idx, to_pos))
                if edge_key not in edges_seen:
                    edges_seen.add(edge_key)
                    discovered_edges.append({
                        "from_layer": from_layer,
                        "from_feature_idx": from_feature_idx,
                        "from_pos": from_pos,
                        "to_layer": to_layer,
                        "to_feature_idx": to_feature_idx,
                        "to_pos": to_pos,
                        "direct_effect": direct_effect,
                        "source": "log_extracted",
                    })

    # Merge: update features that have pos info from get_upstream_features
    for key, feat in features_seen.items():
        if len(key) == 3:
            # Has pos
            discovered_features.append(feat)
        elif len(key) == 2:
            # From inspect_feature, no pos. Check if we have a matching entry with pos
            layer, feature_idx = key
            matched = False
            for other_key in features_seen:
                if len(other_key) == 3 and other_key[0] == layer and other_key[1] == feature_idx:
                    # Merge label/frac_nonzero/promoted_tokens into the one with pos
                    features_seen[other_key].update({
                        "label": feat.get("label", features_seen[other_key].get("label")),
                        "frac_nonzero": feat.get("frac_nonzero"),
                        "promoted_tokens": feat.get("promoted_tokens"),
                    })
                    matched = True
            if not matched:
                # No pos info available, include anyway with pos=None
                feat["pos"] = None
                discovered_features.append(feat)

    return {
        "discovered_features": discovered_features,
        "discovered_edges": discovered_edges,
    }


SUBAGENT_SYSTEM_PROMPT_TEMPLATE = """You are a circuit tracing subagent analyzing a target language model's internal circuits via its attribution graph.

Your task: {objective}

Starting point: L{layer}:F{feature_idx} at position {pos}

Model has {n_layers} layers. **Lower-third floor: layer ≤ {lower_third_floor}.**

Instructions:
1. First, call inspect_feature on the starting feature (L{layer}, {feature_idx}) to understand what it represents.
2. Call get_upstream_features on the starting feature to find what feeds into it.
3. For the top 2-3 upstream features (by |direct_effect|), call inspect_feature to get their semantic labels, promoted tokens, and frac_nonzero.
4. Record each feature and connection you discover.
5. Pick the most important upstream feature(s) and repeat: call get_upstream_features to trace one more hop upstream.

**Termination condition (do not stop early).** Continue tracing upstream until BOTH of the following are true:
   (a) You have reached at least one feature in the **lower 1/3 of the model's layers** (layer ≤ {lower_third_floor}), AND
   (b) You have surfaced **at least one token-embedding (`Emb:`) connection** with positive direct_effect on the path.
Taking the embedding-shortcut early (e.g. the starting feature → Emb directly) is allowed and should be recorded, but does NOT terminate exploration of other upstream paths from the starting feature. Continue tracing the next-highest positive-direct_effect upstream features until the layer-floor is also met.

**Legitimate early stops** (in addition to reaching {max_hops} hops):
- Remaining upstream direct effects are notably small compared to ones already traced from this candidate. The signal has decayed, deeper tracing won't surface a refusal-relevant feature.
- The graph genuinely has no upstream feature in layers ≤ {lower_third_floor} reachable from the starting feature (every path terminates at embeddings in mid/late layers). State this explicitly in your report's `explanation` so the orchestrator knows the layer-floor was vacuously satisfied.
Otherwise, prefer to descend deeper rather than stopping early. When done, call report_findings with ALL the features and edges you discovered.

Prioritize features with:
- Large positive direct_effect (strong excitatory influence on the target on this prompt). Only trace and report edges where the upstream feature has a *positive* direct_effect to the target — negative direct_effect means an inhibitory edge, which is off-target for the tone-down-suppressor methodology and should not be listed in `discovered_edges`.
- Connectivity that suggests a refusal/sensitivity role — a feature is suspicious as a refusal-targeting candidate if it is the strongest upstream driver of a confirmed refusal/negation feature, even if its autointerp label looks generic. **Trust the connectivity (high direct_effect + sparse activation feeding a refusal gate) over the label.**
- Top-promoted tokens that include "cannot", "unable", "unknown", "uncertain", "sorry", "decline", or similar — these signal a feature is functionally part of a refusal/sensitivity pathway, regardless of the label.
- Low frac_nonzero — a tiebreaker among refusal-targeting candidates. Sparser features have lower coherence-budget cost when ablated and generalize better. Do NOT pick a feature for sparsity alone; the role evidence comes first.

When you encounter a feature whose label, top-promoted tokens, or upstream/downstream connectivity suggests **negation, refusal, inability, safety, policy, sensitivity, or suppression**, surface it explicitly in your report — these are the candidates the orchestrator wants to consider for causal intervention. Treat the autointerp label as a hypothesis; the top activating examples and connectivity are the actual evidence of what the feature encodes.

**For each feature you report, include an `interpretation` field** — your assessment of what the feature actually does in this context, based on top activating examples, promoted tokens, and connectivity. This may differ from the autointerp label. For example: "Despite generic 'code snippets' label, promoted tokens (safely, unsafe, discreet) and high direct_effect to the refusal gate suggest this is a sensitivity-precursor feature."

IMPORTANT: You MUST end by calling report_findings. Your results are ONLY captured through report_findings — do not just write text."""


def _make_tool_dispatch(ctx: ToolContext):
    """Create a dispatch table mapping tool names to functions."""
    return {
        "get_top_logits": lambda args: get_top_logits(ctx, k=args.get("k", 5)),
        "get_top_features": lambda args: get_top_features(ctx, token=args["token"], k=args.get("k", 10)),
        "inspect_feature": lambda args: inspect_feature(
            ctx, layer=args["layer"], feature_idx=args["feature_idx"], n_examples=args.get("n_examples", 7)
        ),
        "get_upstream_features": lambda args: get_upstream_features(
            ctx, layer=args["layer"], feature_idx=args["feature_idx"], pos=args["pos"], k=args.get("k", 5)
        ),
        "build_circuit": lambda args: build_circuit(nodes=args["nodes"], edges=args["edges"]),
        # Orchestrator-only in practice (not exposed in the subagent TOOLS schema), but shares the dispatch table.
        "anchor_pass": lambda args: anchor_pass(
            ctx,
            features=args["features"],
            hypothesis=args["hypothesis"],
        ),
        "intervene_feature": lambda args: intervene_feature(
            ctx,
            layer=args["layer"],
            position=args["position"],
            feature_idx=args["feature_idx"],
            scale=args["scale"],
            hypothesis=args["hypothesis"],
        ),
        "intervene_supernode": lambda args: intervene_supernode(
            ctx,
            features=args["features"],
            scale=args["scale"],
            hypothesis=args["hypothesis"],
        ),
    }


def execute_tool(ctx: ToolContext, name: str, args: dict):
    """Dispatch a tool call to the corresponding Python function."""
    dispatch = _make_tool_dispatch(ctx)
    if name not in dispatch:
        return {"error": f"Unknown tool: {name}"}
    try:
        return dispatch[name](args)
    except Exception as e:
        return {"error": f"{name} failed: {str(e)}"}


def trace_path_subagent(
    ctx: ToolContext,
    client: LLMClient,
    subagent_model: str,
    *,
    direction: str,  # unused: only "upstream" supported
    starting_layer: int,
    starting_feature_idx: int,
    starting_pos: int,
    objective: str,
    max_hops: int = 12,
    verbose: bool = True,
    label: str = "",
):
    """Dispatch a subagent to trace a path through the circuit.

    Returns dict with discovered_features, discovered_edges, explanation, trace_log,
    and usage (token counts for the subagent).
    """
    # Subagent tools: investigation tools + report_findings. Intervention tools stay orchestrator-only
    # (they are cross-cutting verification moves on the final pinned circuit, not per-path tracing steps).
    subagent_tools = [
        t for t in TOOLS
        if t["name"] not in ("build_circuit", "trace_path_subagent", "anchor_pass", "intervene_feature", "intervene_supernode")
    ]
    subagent_tools.append(REPORT_FINDINGS_TOOL)

    n_layers = ctx.graph.cfg.n_layers
    lower_third_floor = n_layers // 3
    system = SUBAGENT_SYSTEM_PROMPT_TEMPLATE.format(
        objective=objective,
        layer=starting_layer,
        feature_idx=starting_feature_idx,
        pos=starting_pos,
        max_hops=max_hops,
        n_layers=n_layers,
        lower_third_floor=lower_third_floor,
    )

    messages = [
        {
            "role": "user",
            "content": (
                f"Begin tracing from L{starting_layer}:F{starting_feature_idx} at position "
                f"{starting_pos}. Objective: {objective}"
            ),
        }
    ]
    if not label:
        label = f"L{starting_layer}:F{starting_feature_idx}@{starting_pos}"

    trace_log = []
    max_turns = max_hops * 5
    report_retries = 0
    max_report_retries = 2

    # Track subagent token usage
    subagent_usage = {
        "model": subagent_model,
        "label": label,
        "objective": objective,
        "input_tokens": 0,
        "output_tokens": 0,
        "cache_creation_input_tokens": 0,
        "cache_read_input_tokens": 0,
    }

    if verbose:
        print(f"\n  [{label}] Starting: L{starting_layer}:F{starting_feature_idx} @ pos {starting_pos}")
        print(f"  [{label}] Objective: {objective}")

    for turn in range(max_turns):
        response = client.create_message(
            model=subagent_model,
            max_tokens=4096,
            system=system,
            tools=subagent_tools,
            messages=messages,
        )
        messages.append({"role": "assistant", "content": response.content})

        # Accumulate usage
        usage = response.usage
        subagent_usage["input_tokens"] += usage.input_tokens
        subagent_usage["output_tokens"] += usage.output_tokens
        subagent_usage["cache_creation_input_tokens"] += getattr(usage, "cache_creation_input_tokens", 0) or 0
        subagent_usage["cache_read_input_tokens"] += getattr(usage, "cache_read_input_tokens", 0) or 0

        if response.stop_reason == "end_turn":
            has_report = any(b.type == "tool_use" and b.name == "report_findings"
                            for b in response.content)
            if not has_report and report_retries < max_report_retries:
                report_retries += 1
                if verbose:
                    print(f"  [{label}] Ended without report_findings — nudging ({report_retries}/{max_report_retries}, turn {turn+1})")
                messages.append({"role": "user", "content":
                    "You ended without calling report_findings. You MUST call report_findings "
                    "now with all the features and edges you discovered so far. "
                    "Do not respond with text — call the report_findings tool."
                })
                continue
            text = next((b.text for b in response.content if b.type == "text"), "")
            # Extract from trace_log since subagent failed to report
            extracted = _extract_features_from_trace_log(trace_log)
            nf = len(extracted["discovered_features"])
            ne = len(extracted["discovered_edges"])
            if verbose:
                print(f"  [{label}] Ended without report_findings (turn {turn+1}), extracted {nf} features, {ne} edges from trace_log")
            return {
                "warning": "Subagent ended without calling report_findings (extracted from trace_log)",
                "text": text,
                "trace_log": trace_log,
                "discovered_features": extracted["discovered_features"],
                "discovered_edges": extracted["discovered_edges"],
                "explanation": text[:500] if text else f"(log_extracted: {nf} features, {ne} edges)",
                "usage": subagent_usage,
            }

        tool_results = []
        for block in response.content:
            if block.type == "tool_use":
                if block.name == "report_findings":
                    findings = block.input
                    reported_features = findings.get("discovered_features", [])
                    reported_edges = findings.get("discovered_edges", [])

                    # Tag agent-reported items
                    for f in reported_features:
                        f["source"] = "agent_reported"
                    for e in reported_edges:
                        e["source"] = "agent_reported"

                    # If agent reported empty/sparse, supplement with trace_log extraction
                    if len(reported_features) < 3 and trace_log:
                        extracted = _extract_features_from_trace_log(trace_log)
                        # Add extracted features not already in reported
                        reported_keys = {(f["layer"], f["feature_idx"], f.get("pos")) for f in reported_features}
                        for ef in extracted["discovered_features"]:
                            key = (ef["layer"], ef["feature_idx"], ef.get("pos"))
                            if key not in reported_keys:
                                reported_features.append(ef)
                        # Add extracted edges not already in reported
                        reported_edge_keys = {
                            (e["from_layer"], e["from_feature_idx"], e["to_layer"], e["to_feature_idx"])
                            for e in reported_edges
                        }
                        for ee in extracted["discovered_edges"]:
                            key = (ee["from_layer"], ee["from_feature_idx"], ee["to_layer"], ee["to_feature_idx"])
                            if key not in reported_edge_keys:
                                reported_edges.append(ee)

                    nf = len(reported_features)
                    ne = len(reported_edges)
                    n_extracted = sum(1 for f in reported_features if f.get("source") == "log_extracted")
                    if verbose:
                        extra = f" (+{n_extracted} extracted)" if n_extracted else ""
                        print(f"  [{label}] Done! {nf} features, {ne} edges{extra} (turn {turn+1})")
                    return {
                        "discovered_features": reported_features,
                        "discovered_edges": reported_edges,
                        "explanation": findings.get("explanation", ""),
                        "trace_log": trace_log,
                        "usage": subagent_usage,
                    }
                result = execute_tool(ctx, block.name, block.input)
                trace_log.append({"tool": block.name, "input": block.input, "output": result})
                if verbose:
                    print(f"  [{label} t{turn+1}] {block.name}({json.dumps(block.input, separators=(',',':'))[:80]})")
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": json.dumps(result),
                })

        messages.append({"role": "user", "content": tool_results})

    # Extract from trace_log since subagent exceeded max turns
    extracted = _extract_features_from_trace_log(trace_log)
    nf = len(extracted["discovered_features"])
    ne = len(extracted["discovered_edges"])
    if verbose:
        print(f"  [{label}] Exceeded {max_turns} turns, extracted {nf} features, {ne} edges from trace_log")
    return {
        "error": "Subagent exceeded max turns without reporting findings (extracted from trace_log)",
        "trace_log": trace_log,
        "discovered_features": extracted["discovered_features"],
        "discovered_edges": extracted["discovered_edges"],
        "explanation": f"(log_extracted: {nf} features, {ne} edges from {len(trace_log)} tool calls)",
        "usage": subagent_usage,
    }
