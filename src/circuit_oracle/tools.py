"""Tool functions for the circuit oracle agent.

Each function operates on a ToolContext (graph + tokenizer) instead of globals.
"""

import time
import logging
import requests
import torch
import torch.nn.functional as F

from .config import ToolContext

logger = logging.getLogger(__name__)


def get_top_logits(ctx: ToolContext, k: int = 5):
    """Return the top-k output tokens and probabilities from the attribution graph."""
    n = min(k, len(ctx.graph.logit_tokens))
    results = []
    for i in range(n):
        token_str = ctx.tokenizer.decode(ctx.graph.logit_tokens[i].item())
        prob = ctx.graph.logit_probabilities[i].item()
        results.append({"token": token_str, "probability": round(prob, 4)})
    return results


def get_top_features(ctx: ToolContext, token: str, k: int = 15):
    """Return the top-k features driving a target output token's logit."""
    graph = ctx.graph
    logit_idx = None
    for i in range(len(graph.logit_tokens)):
        decoded = ctx.tokenizer.decode(graph.logit_tokens[i].item())
        if decoded.strip() == token.strip():
            logit_idx = i
            break
    if logit_idx is None:
        available = [ctx.tokenizer.decode(t.item()) for t in graph.logit_tokens]
        return {
            "error": (
                f"Token '{token}' is not one of the top-k next-token candidates captured in "
                f"this attribution graph. Available: {available}. The graph only has attribution "
                f"for the first predicted token — later tokens in the autoregressive continuation "
                f"(e.g. 'cannot', 'provide' after 'I cannot provide...') are not available here. "
                f"Either pick a token from the available list, or trace upstream from one of "
                f"those tokens to find features that gate the refusal opener."
            )
        }

    n_features = len(graph.selected_features)
    n_logits = len(graph.logit_tokens)

    logit_row = graph.adjacency_matrix[-n_logits + logit_idx]
    feature_effects = logit_row[:n_features]

    # Top-k by signed direct_effect (most positive first). Positive drivers
    # of the target token surface first; inhibitory features fall to the bottom.
    topk = min(k, n_features)
    _, top_indices = feature_effects.topk(topk)

    results = []
    for idx in top_indices:
        idx = idx.item()
        active_idx = graph.selected_features[idx].item()
        layer, pos, feature_idx = graph.active_features[active_idx].tolist()
        activation = graph.activation_values[active_idx].item()
        direct_effect = feature_effects[idx].item()
        results.append({
            "layer": int(layer),
            "feature_idx": int(feature_idx),
            "pos": int(pos),
            "activation": round(activation, 4),
            "direct_effect": round(direct_effect, 4),
        })
    return results


def inspect_feature(ctx: ToolContext, layer: int, feature_idx: int, n_examples: int = 7):
    """Look up a transcoder feature on Neuronpedia and return its autointerp label and top examples."""
    sae_id = ctx.neuronpedia_sae_id.format(layer=layer)
    url = f"https://www.neuronpedia.org/api/feature/{ctx.neuronpedia_model_id}/{sae_id}/{feature_idx}"
    try:
        resp = requests.get(url, timeout=15)
        resp.raise_for_status()
    except requests.RequestException as e:
        return {"error": f"Neuronpedia API error: {str(e)}"}

    data = resp.json()

    label = "No explanation available"
    if data.get("explanations") and len(data["explanations"]) > 0:
        label = data["explanations"][0].get("description", label)

    top_examples = []
    acts = sorted(
        data.get("activations") or [],
        key=lambda a: a.get("maxValue", 0),
        reverse=True,
    )
    for act in acts[:max(0, int(n_examples))]:
        tokens = act.get("tokens", [])
        values = act.get("values", [])
        text = "".join(tokens)[:200]
        max_val = max(values) if values else 0
        max_idx = values.index(max_val) if values else 0
        max_token = tokens[max_idx] if max_idx < len(tokens) else ""
        top_examples.append({
            "text_snippet": text,
            "max_activation": round(max_val, 3),
            "max_token": max_token,
        })

    pos_tokens = data.get("pos_str", [])[:10]
    neg_tokens = data.get("neg_str", [])[:10]

    return {
        "layer": layer,
        "feature_idx": feature_idx,
        "label": label,
        "top_activating_examples": top_examples,
        "promoted_tokens": pos_tokens,
        "suppressed_tokens": neg_tokens,
        "frac_nonzero": data.get("frac_nonzero"),
    }


def get_upstream_features(ctx: ToolContext, layer: int, feature_idx: int, pos: int, k: int = 10):
    """Return the top-k upstream features that feed into the given feature."""
    graph = ctx.graph
    n_features = len(graph.selected_features)

    target_row = None
    for i in range(n_features):
        active_idx = graph.selected_features[i].item()
        feat = graph.active_features[active_idx].tolist()
        if int(feat[0]) == layer and int(feat[1]) == pos and int(feat[2]) == feature_idx:
            target_row = i
            break

    if target_row is None:
        # Find which positions this feature IS active at, so the agent can retry
        available_positions = []
        for i in range(n_features):
            active_idx = graph.selected_features[i].item()
            feat = graph.active_features[active_idx].tolist()
            if int(feat[0]) == layer and int(feat[2]) == feature_idx:
                available_positions.append(int(feat[1]))
        if available_positions:
            return {
                "error": f"Feature (layer={layer}, feature_idx={feature_idx}) not found at pos={pos}. "
                f"This feature is active at pos={available_positions}. Retry with one of those positions."
            }
        return {
            "error": f"Feature (layer={layer}, pos={pos}, feature_idx={feature_idx}) "
            "not found in graph's selected features."
        }

    row = graph.adjacency_matrix[target_row].clone()
    # Matrix entries are activation-scaled direct effects (a_s × jacobian).
    # Positive = upstream excites target, negative = upstream inhibits target.
    # For tracing what drives the target to fire, positive entries are the
    # signal; negative entries are inhibitory edges that aren't useful for
    # our tone-down-suppressor methodology. Rank by signed direct_effect
    # descending so positive drivers come first.
    feature_effects = row[:n_features]
    feature_effects[target_row] = 0

    # Top-k by signed direct_effect (most positive first)
    topk = min(k, n_features - 1)
    _, top_indices = feature_effects.topk(topk)

    results = []
    for idx in top_indices:
        idx = idx.item()
        active_idx = graph.selected_features[idx].item()
        src_layer, src_pos, src_feature_idx = graph.active_features[active_idx].tolist()
        direct_effect = feature_effects[idx].item()
        upstream_activation = graph.activation_values[active_idx].item()
        results.append({
            "type": "feature",
            "layer": int(src_layer),
            "feature_idx": int(src_feature_idx),
            "pos": int(src_pos),
            "direct_effect": round(direct_effect, 4),
            "activation": round(upstream_activation, 4),
        })

    # Embedding node columns. Same convention: positive = the token's embedding
    # excites the target, negative = inhibits.
    n_layers = graph.cfg.n_layers
    embed_start = n_features + n_layers * graph.n_pos
    embed_end = embed_start + graph.n_pos
    embed_effects = row[embed_start:embed_end]

    for pos_idx in range(graph.n_pos):
        w = embed_effects[pos_idx].item()
        if w == 0:
            continue
        token_str = ctx.tokenizer.decode(graph.input_tokens[pos_idx].item())
        results.append({
            "type": "embedding",
            "token": token_str,
            "pos": int(pos_idx),
            "direct_effect": round(w, 4),
        })

    # Sort by signed direct_effect descending. Positive drivers first;
    # inhibitory (negative) edges fall to the bottom.
    results.sort(key=lambda r: r["direct_effect"], reverse=True)
    return results[:k]


def build_circuit(nodes, edges):
    """Store the agent's curated circuit. Returns it as-is (used by visualization)."""
    for n in nodes:
        if not n.get("features") and n.get("layer") not in (0, 36):
            return {
                "error": f"Node '{n.get('id', '?')}' must have at least one feature "
                "(unless it is an output logit node with layer=36 or an embedding node with layer=0)"
            }
    node_ids = {n["id"] for n in nodes}
    for e in edges:
        if e["from"] not in node_ids or e["to"] not in node_ids:
            return {"error": f"Edge references unknown node: {e}"}

    result = {"nodes": nodes, "edges": edges, "status": "circuit_saved"}

    # Check circuit depth: embedding nodes are ideal, early layers (0-3) are acceptable
    has_embedding = any(
        n.get("layer") == 0 and not n.get("features")
        for n in nodes
    )
    has_early = any(
        n.get("layer", 99) <= 3
        for n in nodes
    )
    if not has_embedding:
        if has_early:
            result["warning"] = (
                "Circuit reaches early layers but not token embedding nodes. "
                "Consider tracing to embedding nodes to identify which specific "
                "input tokens drive the prediction."
            )
        else:
            result["warning"] = (
                "Circuit does not reach early layers (0-3) or token embedding nodes. "
                "Consider tracing deeper to identify which input tokens drive the prediction."
            )

    return result


ALLOWED_SCALES = (-4, -3, -2, -1, 0, 0.5, 2)
BASELINE_FLOOR = 10.0  # minimum effective baseline for multiplicative steering
NEGATIVE_DEPTH_SCALES = (-2, -3, -4)  # factors that require anchor + gradual prerequisites


def _validate_scale(scale):
    if scale not in ALLOWED_SCALES:
        raise ValueError(
            f"factor must be one of {ALLOWED_SCALES}; got {scale!r}. "
            "MULTIPLICATIVE STEERING: new_act = baseline + (factor - 1) × effective_baseline, "
            "where effective_baseline = max(10, baseline). Negative/zero = reverse/ablate "
            "(refusal/suppression). factor > 1 = amplify (diagnostic only). "
            "Default workflow: anchor_pass first (factor=-1 on every shortlisted feature), "
            "then depth-first gradual escalation -2 → -3 → -4 on softened singles, "
            "then supernode synthesis."
        )


def _gradual_predecessor(scale: float) -> float | None:
    """Return the factor that must have been applied previously (gradual rule).
    -2 needs no prior depth (anchor at -1 is enough). -3 needs prior -2. -4 needs prior -3.
    """
    if scale == -3:
        return -2
    if scale == -4:
        return -3
    return None


def _format_feat(layer: int, feature_idx: int) -> str:
    return f"L{layer}:F{feature_idx}"


def _check_single_prerequisites(ctx: ToolContext, layer: int, feature_idx: int, scale: float) -> str | None:
    """Return an error message if this single-feature call should be rejected, else None."""
    key = (layer, feature_idx)
    # Dedup: same (feature, factor) tuple already measured. Covers every scale uniformly
    # (-1 anchor, -2/-3/-4 depth, 0 ablation, 0.5 / 2 diagnostic).
    if scale in ctx.single_factors.get(key, set()):
        return (
            f"already_run: {_format_feat(layer, feature_idx)} has already been intervened on at "
            f"factor={scale}. Each (feature, factor) pair may only be measured once. Pick a "
            f"different feature or a different factor."
        )
    if scale in NEGATIVE_DEPTH_SCALES:
        if key not in ctx.anchor_passed:
            return (
                f"anchor_required: {_format_feat(layer, feature_idx)} has not been anchor-passed "
                f"at factor=-1. Run anchor_pass on this feature (or intervene_feature with "
                f"scale=-1) before escalating to {scale}."
            )
        prev = _gradual_predecessor(scale)
        if prev is not None and prev not in ctx.depth_factors.get(key, set()):
            return (
                f"gradual_required: escalation to factor={scale} on {_format_feat(layer, feature_idx)} "
                f"requires a prior measurement at factor={prev}. Run factor={prev} first, then "
                f"escalate."
            )
    return None


def _record_single(ctx: ToolContext, layer: int, feature_idx: int, scale: float, result: dict) -> None:
    """Append to history, update single-feature dedup index, mark anchored / depth as appropriate."""
    key = (layer, feature_idx)
    ctx.single_factors.setdefault(key, set()).add(scale)
    if scale == -1:
        ctx.anchor_passed.add(key)
    if scale in NEGATIVE_DEPTH_SCALES:
        ctx.depth_factors.setdefault(key, set()).add(scale)
    ctx.intervention_history.append({
        "type": "single",
        "layer": layer,
        "feature_idx": feature_idx,
        "scale": scale,
    })


def _supernode_key(features: list) -> frozenset:
    return frozenset((f["layer"], f["feature_idx"]) for f in features)


def _check_supernode_prerequisites(ctx: ToolContext, features: list, scale: float) -> str | None:
    if not ctx.anchor_pass_called:
        return (
            "anchor_required: anchor_pass has not been run yet. Call anchor_pass on the "
            "shortlisted suppression features before any intervene_supernode call. The "
            "anchor pass tells you which features are softened and worth combining."
        )
    key = _supernode_key(features)
    seen = ctx.supernode_factors.get(key, set())
    if scale in seen:
        return (
            f"already_run: this exact supernode (features={sorted(key)}) has already been "
            f"measured at factor={scale}. Each (supernode, factor) pair may only be measured "
            f"once. Pick a different feature set or a different factor."
        )
    # Supernode gradual rule: factor=-1 is the canonical entry point for any
    # feature-set; -2 requires prior -1 on the same feature-set; -3 requires prior
    # -2; -4 requires prior -3. Strict gradualness across all four magnitudes.
    if scale in (-2, -3, -4):
        need = -1 if scale == -2 else _gradual_predecessor(scale)
        if need not in seen:
            return (
                f"gradual_required: escalation to factor={scale} on this supernode requires "
                f"a prior measurement at factor={need} on the same feature set. Run "
                f"factor={need} first, then escalate."
            )
    return None


def _record_supernode(ctx: ToolContext, features: list, scale: float, result: dict) -> None:
    key = _supernode_key(features)
    ctx.supernode_factors.setdefault(key, set()).add(scale)
    ctx.intervention_history.append({
        "type": "supernode",
        "features": sorted([(f["layer"], f["feature_idx"]) for f in features]),
        "scale": scale,
    })


def _topk_from_logits(last_token_logits, tokenizer, k=5):
    probs = F.softmax(last_token_logits.float(), dim=-1)
    top_vals, top_ids = probs.topk(k)
    return {
        tokenizer.decode([tid.item()]): {"prob": round(p.item(), 6)}
        for tid, p in zip(top_ids, top_vals)
    }


def _baseline_active_positions(ctx, layer, feature_idx, top_n=10):
    """Positions where this feature fires in baseline (diagnostic for persistence scope).

    Transcoder features are sparse — most positions are 0. Returns up to top_n
    nonzero (pos, activation) records sorted by |activation| descending, plus the
    total nonzero count.
    """
    acts = ctx.baseline_activations[layer, :, feature_idx]
    if acts.is_sparse:
        acts = acts.to_dense()
    nonzero = (acts != 0).nonzero().flatten()
    total = int(nonzero.numel())
    if total == 0:
        return {"total_active_positions": 0, "positions": []}
    vals = acts[nonzero]
    order = vals.abs().argsort(descending=True)[:top_n]
    return {
        "total_active_positions": total,
        "positions": [
            {"pos": int(nonzero[i].item()), "activation": round(acts[nonzero[i]].item(), 6)}
            for i in order
        ],
    }


def _check_intervention_ctx(ctx, fn_name):
    if ctx.replacement_model is None:
        raise RuntimeError(
            f"ctx.replacement_model is None. Populate it at graph-build time before calling {fn_name}."
        )
    if ctx.baseline_activations is None:
        raise RuntimeError(
            f"ctx.baseline_activations is None. Populate it at graph-build time before calling {fn_name}."
        )
    if ctx.baseline_answer is None:
        raise RuntimeError(
            f"ctx.baseline_answer is None. Populate it at graph-build time before calling {fn_name}."
        )
    prompt = getattr(ctx, "baseline_prompt", None)
    if prompt is None:
        raise RuntimeError(
            f"ctx.baseline_prompt not set. Wire this field in the graph-build caller before using {fn_name}."
        )
    return prompt


def _measure_intervention(ctx, intervention_tuples, prompt, answer_max_tokens, retry_label):
    """Run before/after measurement for a list of (layer, pos, feature_idx, new_value) tuples.

    `pos` may be an int (single position) or a `slice` for broadcast steering.
    We use `slice(None, None)` so the kick applies at every position in the full
    context — prompt tokens included — on every generation step, mirroring the
    Arditi/Cyberey "every position, every layer" convention. This also cancels
    any firings of the pinned feature at earlier prompt positions that would
    otherwise propagate refusal signal forward via self-attention.

    Returns (top5_before, top5_after, answer_after, inference_time_s).
    """
    model = ctx.replacement_model
    tokenizer = ctx.tokenizer
    eos_id = getattr(tokenizer, "eos_token_id", None)

    def _run(interventions_list, prompt_arg, freeze_attn):
        delays = [1, 2, 4]
        last_exc = None
        for attempt, delay in enumerate([0] + delays):
            if delay:
                time.sleep(delay)
            try:
                logits, _ = model.feature_intervention(
                    prompt_arg, interventions_list,
                    freeze_attention=freeze_attn,
                    return_activations=False,
                )
                return logits
            except torch.cuda.OutOfMemoryError as exc:
                last_exc = exc
                logger.warning(
                    "OOM on %s attempt %d; retrying.", retry_label, attempt + 1,
                )
        raise last_exc

    t0 = time.perf_counter()

    # Top-5 logits at the next-token position (frozen attention matches the
    # attribution-graph forward pass and lets get_top_logits stay comparable).
    baseline_logits = _run([], prompt, freeze_attn=True)
    top5_before = _topk_from_logits(baseline_logits[0, -1, :], tokenizer)

    after_logits = _run(intervention_tuples, prompt, freeze_attn=True)
    top5_after = _topk_from_logits(after_logits[0, -1, :], tokenizer)

    # Greedy autoregressive decode under persistent, full-context intervention.
    # Each step extends the prompt with the previous token and runs a fresh
    # forward pass. The intervention's slice(None, None) position broadcasts the
    # kick across every position in the current context (prompt + generated),
    # so the prediction position is always being steered and any upstream prompt
    # firings of the pinned feature are cancelled. Step 0 reuses after_logits
    # (freeze_attention=True for parity with the attribution model). From step 1
    # onward, freeze_attention is off so the model attends normally.
    generated_ids = []
    current_prompt = prompt
    step_logits = after_logits
    for step in range(answer_max_tokens):
        if step > 0:
            step_logits = _run(intervention_tuples, current_prompt, freeze_attn=False)
        next_id = step_logits[0, -1, :].argmax().item()
        if eos_id is not None and next_id == eos_id:
            break
        next_token_str = tokenizer.decode([next_id])
        generated_ids.append(next_id)
        current_prompt = current_prompt + next_token_str

    answer_after = tokenizer.decode(generated_ids, skip_special_tokens=True)
    inference_time_s = round(time.perf_counter() - t0, 3)

    return top5_before, top5_after, answer_after, inference_time_s


def intervene_feature(
    ctx: ToolContext,
    layer: int,
    position: int,
    feature_idx: int,
    scale: float,
    hypothesis: str,
    answer_max_tokens: int = 800,
) -> dict:
    """Causally intervene on one transcoder feature persistently across generation.

    MULTIPLICATIVE STEERING: new_act = baseline + (factor - 1) × effective_baseline,
    where effective_baseline = max(BASELINE_FLOOR, baseline) (the floor ensures minimum
    steering magnitude on weakly-firing features). factor=1 is identity; factor=0 is
    clean ablation; negative factors reverse the feature's contribution; positive
    factors > 1 amplify.

    Enforced ordering: factor in {-2,-3,-4} requires the feature to have been anchor-passed
    at -1 first; -3 requires prior -2 on the same feature, -4 requires prior -3.
    Each (feature, factor) pair may only be measured once.
    """
    _validate_scale(scale)
    if not hypothesis.strip():
        raise ValueError("hypothesis must be a non-empty string.")
    err = _check_single_prerequisites(ctx, layer, feature_idx, scale)
    if err is not None:
        return {"error": err, "intervention": {"type": "single", "layer": layer, "position": position, "feature_idx": feature_idx, "scale": scale}}
    answer_max_tokens = min(answer_max_tokens, 800)

    prompt = _check_intervention_ctx(ctx, "intervene_feature")

    baseline_activation = ctx.baseline_activations[layer, position, feature_idx].item()
    # Multiplicative steering: new_act = baseline + (factor - 1) × effective_baseline
    effective_baseline = max(BASELINE_FLOOR, baseline_activation)
    new_activation = baseline_activation + (float(scale) - 1) * effective_baseline
    # slice(None, None): kick every position in the full context (prompt tokens
    # + generated tokens) at every step. Cancels upstream firings and persists
    # across generation.
    intervention = (layer, slice(None, None), feature_idx, new_activation)
    active_positions = _baseline_active_positions(ctx, layer, feature_idx)

    top5_before, top5_after, answer_after, inference_time_s = _measure_intervention(
        ctx, [intervention], prompt, answer_max_tokens,
        retry_label=f"intervene_feature L{layer}:F{feature_idx}@{position} scale={scale}",
    )

    result = {
        "hypothesis": hypothesis,
        "intervention": {
            "type": "single",
            "layer": layer,
            "position": position,
            "feature_idx": feature_idx,
            "scale": scale,
        },
        "baseline_activation": baseline_activation,
        "new_activation": new_activation,
        "baseline_active_positions": active_positions,
        "top5_before": top5_before,
        "top5_after": top5_after,
        "answer_before": ctx.baseline_answer,
        "answer_after": answer_after,
        "inference_time_s": inference_time_s,
    }
    _record_single(ctx, layer, feature_idx, scale, result)
    return result


def anchor_pass(
    ctx: ToolContext,
    features: list,
    hypothesis: str,
    answer_max_tokens: int = 800,
) -> dict:
    """Anchor pass: run factor=-1 on every feature in the shortlist (one measurement per feature).

    `features` is a list of dicts each with keys 'layer', 'position', 'feature_idx'.

    This is Phase 1 of VERIFY. Call EXACTLY ONCE with the full shortlist of suppression
    candidates you want to test. Each feature is measured at factor=-1 individually (NOT a
    supernode) and recorded as anchored, which unlocks depth escalation (-2/-3/-4) on
    those features and unlocks intervene_supernode for any combination of them.

    A second anchor_pass call is rejected. If you realize a feature was missing from the
    shortlist after this call returned, anchor it ad-hoc with intervene_feature(scale=-1).
    """
    if not hypothesis.strip():
        raise ValueError("hypothesis must be a non-empty string.")
    if not features:
        raise ValueError(
            "features must be a non-empty list of {'layer', 'position', 'feature_idx'} dicts. "
            "Provide every BUILD-pinned suppression feature you want to causally test."
        )
    if ctx.anchor_pass_called:
        return {"error": (
            "already_run: anchor_pass has already been called this run. It runs exactly once. "
            "If you forgot a feature, anchor it ad-hoc with intervene_feature(scale=-1, ...)."
        )}
    answer_max_tokens = min(answer_max_tokens, 800)

    prompt = _check_intervention_ctx(ctx, "anchor_pass")

    # Dedup within this call by (layer, feature_idx): keep the entry with the largest
    # baseline_activation (transcoder features are non-negative post-ReLU, so a raw-value
    # comparison is correct).
    canonical: dict[tuple[int, int], dict] = {}
    duplicates: list[dict] = []
    for feat in features:
        layer = feat["layer"]
        position = feat["position"]
        feature_idx = feat["feature_idx"]
        key = (layer, feature_idx)
        baseline_activation = ctx.baseline_activations[layer, position, feature_idx].item()
        candidate = {
            "layer": layer,
            "position": position,
            "feature_idx": feature_idx,
            "baseline_activation": baseline_activation,
        }
        existing = canonical.get(key)
        if existing is None:
            canonical[key] = candidate
        elif baseline_activation > existing["baseline_activation"]:
            duplicates.append({**existing, "dropped_reason": "duplicate_lower_baseline"})
            canonical[key] = candidate
        else:
            duplicates.append({**candidate, "dropped_reason": "duplicate_lower_baseline"})

    measurements = []
    for entry in canonical.values():
        layer = entry["layer"]
        position = entry["position"]
        feature_idx = entry["feature_idx"]
        baseline_activation = entry["baseline_activation"]
        # factor=-1 multiplicative steering
        effective_baseline = max(BASELINE_FLOOR, baseline_activation)
        new_activation = baseline_activation + (-1.0 - 1.0) * effective_baseline
        intervention = (layer, slice(None, None), feature_idx, new_activation)
        active_positions = _baseline_active_positions(ctx, layer, feature_idx)
        top5_before, top5_after, answer_after, inference_time_s = _measure_intervention(
            ctx, [intervention], prompt, answer_max_tokens,
            retry_label=f"anchor_pass L{layer}:F{feature_idx}@{position} scale=-1",
        )
        per_feature = {
            "intervention": {
                "type": "single",
                "layer": layer,
                "position": position,
                "feature_idx": feature_idx,
                "scale": -1,
            },
            "baseline_activation": baseline_activation,
            "new_activation": new_activation,
            "baseline_active_positions": active_positions,
            "top5_before": top5_before,
            "top5_after": top5_after,
            "answer_after": answer_after,
            "inference_time_s": inference_time_s,
        }
        measurements.append(per_feature)
        _record_single(ctx, layer, feature_idx, -1, per_feature)

    ctx.anchor_pass_called = True
    result = {
        "hypothesis": hypothesis,
        "answer_before": ctx.baseline_answer,
        "anchor_results": measurements,
        "n_measured": len(measurements),
    }
    if duplicates:
        result["deduplicated_features"] = duplicates
        result["deduplication_note"] = (
            f"{len(duplicates)} duplicate (layer, feature_idx) entries were dropped within this "
            "anchor_pass call (intervention broadcasts across positions; the kept entry per "
            "(layer, feature_idx) is the position with the largest baseline_activation)."
        )
    return result


def intervene_supernode(
    ctx: ToolContext,
    features: list,
    scale: float,
    hypothesis: str,
    answer_max_tokens: int = 800,
) -> dict:
    """Causally intervene on a group of features (supernode) persistently across generation.

    `features` is a list of dicts each with keys 'layer', 'position', 'feature_idx'.

    MULTIPLICATIVE STEERING applied identically to every feature in the group:
    new_act = baseline + (factor - 1) × effective_baseline, where
    effective_baseline = max(BASELINE_FLOOR, baseline).

    Because the intervention broadcasts across positions (slice(None, None)),
    duplicate (layer, feature_idx) entries with different positions are
    redundant. We dedupe by (layer, feature_idx), keeping the entry with the
    largest baseline_activation (the position where the feature fires most
    strongly), and surface the dropped entries to the agent in
    `deduplicated_features` so the next call can be cleaner.
    """
    _validate_scale(scale)
    if not hypothesis.strip():
        raise ValueError("hypothesis must be a non-empty string.")
    if not features:
        raise ValueError(
            "features must be a non-empty list of {'layer', 'position', 'feature_idx'} dicts."
        )
    # Schema requires minItems=2; defensive server-side guard in case the schema is bypassed.
    if len(features) < 2:
        raise ValueError(
            "intervene_supernode requires at least 2 features. For a single-feature intervention, "
            "use intervene_feature (or anchor_pass for the Phase 1 anchor)."
        )
    err = _check_supernode_prerequisites(ctx, features, scale)
    if err is not None:
        return {"error": err, "intervention": {"type": "supernode", "scale": scale, "features": [{"layer": f["layer"], "feature_idx": f["feature_idx"]} for f in features]}}
    answer_max_tokens = min(answer_max_tokens, 800)

    prompt = _check_intervention_ctx(ctx, "intervene_supernode")

    # Dedupe by (layer, feature_idx). Keep the entry with the largest
    # baseline_activation as the canonical one; record the rest for the agent.
    canonical: dict[tuple[int, int], dict] = {}
    duplicates: list[dict] = []
    for feat in features:
        layer = feat["layer"]
        position = feat["position"]
        feature_idx = feat["feature_idx"]
        baseline_activation = ctx.baseline_activations[layer, position, feature_idx].item()
        candidate = {
            "layer": layer,
            "position": position,
            "feature_idx": feature_idx,
            "baseline_activation": baseline_activation,
        }
        key = (layer, feature_idx)
        existing = canonical.get(key)
        if existing is None:
            canonical[key] = candidate
        elif baseline_activation > existing["baseline_activation"]:
            duplicates.append({**existing, "dropped_reason": "duplicate_lower_baseline"})
            canonical[key] = candidate
        else:
            duplicates.append({**candidate, "dropped_reason": "duplicate_lower_baseline"})

    # Defense: if duplicate (layer, feature_idx) inputs collapsed the canonical set to
    # fewer than 2 unique features, this is no longer a supernode. Reject rather than
    # silently running it as a single-feature steer (which would also pollute the
    # supernode dedup index with a 1-element frozenset).
    if len(canonical) < 2:
        return {
            "error": (
                "supernode_collapsed: after deduping by (layer, feature_idx), only "
                f"{len(canonical)} unique feature(s) remain. A supernode requires at least "
                "2 distinct (layer, feature_idx) pairs. Use intervene_feature for a single "
                "feature, or rebuild the supernode with semantically complementary features."
            ),
            "intervention": {
                "type": "supernode",
                "scale": scale,
                "features": [{"layer": e["layer"], "feature_idx": e["feature_idx"]} for e in canonical.values()],
            },
            "deduplicated_features": duplicates,
        }

    intervention_tuples = []
    feature_records = []
    for entry in canonical.values():
        layer = entry["layer"]
        position = entry["position"]
        feature_idx = entry["feature_idx"]
        baseline_activation = entry["baseline_activation"]
        # Multiplicative steering: new_act = baseline + (factor - 1) × effective_baseline
        effective_baseline = max(BASELINE_FLOOR, baseline_activation)
        new_activation = baseline_activation + (float(scale) - 1) * effective_baseline
        # slice(None, None): full-context persistent steering (see intervene_feature).
        intervention_tuples.append((layer, slice(None, None), feature_idx, new_activation))
        feature_records.append({
            "layer": layer,
            "position": position,
            "feature_idx": feature_idx,
            "baseline_activation": baseline_activation,
            "new_activation": new_activation,
            "baseline_active_positions": _baseline_active_positions(ctx, layer, feature_idx),
        })

    top5_before, top5_after, answer_after, inference_time_s = _measure_intervention(
        ctx, intervention_tuples, prompt, answer_max_tokens,
        retry_label=f"intervene_supernode ({len(feature_records)} features) scale={scale}",
    )

    result = {
        "hypothesis": hypothesis,
        "intervention": {
            "type": "supernode",
            "features": feature_records,
            "scale": scale,
        },
        "top5_before": top5_before,
        "top5_after": top5_after,
        "answer_before": ctx.baseline_answer,
        "answer_after": answer_after,
        "inference_time_s": inference_time_s,
    }
    if duplicates:
        result["deduplicated_features"] = duplicates
        result["deduplication_note"] = (
            f"{len(duplicates)} entry/entries with duplicate (layer, feature_idx) were dropped "
            "because the intervention broadcasts across all positions. The kept entry per "
            "(layer, feature_idx) is the position with the largest baseline_activation. "
            "In future calls, include each (layer, feature_idx) only once."
        )
    # Record using the canonical (deduped) feature set so dedup checks see the same key
    # the agent submitted.
    canonical_features = [{"layer": e["layer"], "feature_idx": e["feature_idx"]} for e in canonical.values()]
    _record_supernode(ctx, canonical_features, scale, result)
    return result
