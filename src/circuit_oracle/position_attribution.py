"""Positional attribution scalar: entity vs non-entity contribution to the top logit.

Forward-propagates from each input-token embedding through `graph.adjacency_matrix`
(circuit-tracer direct-effect matrix) and accumulates the total path-sum effect on
the top logit node. Partitions per-position contributions by entity-span vs.
non-entity-span and returns the fraction each stream contributes.

This is a post-hoc diagnostic: the oracle does not see this scalar during analysis.
It is a cheap companion number to check whether the oracle's verdict aligns with
the raw attribution pattern.

Node ordering in graph.adjacency_matrix (circuit-tracer convention):
    [active_features, error_nodes, embed_nodes, logit_nodes]

Matrix direction: adjacency_matrix[i, j] = direct contribution from node j to node i.
Signal flows forward through layers, so the matrix is effectively upper triangular in
the topological ordering. This means the series I + A + A^2 + ... terminates after
at most (n_layers + 2) hops; we use iterated matmul rather than explicit inversion.
"""

from __future__ import annotations

import torch

from .config import ToolContext


def find_entity_span(tokenizer, input_tokens, entity_text: str) -> list[int]:
    """Locate contiguous token positions matching entity_text in input_tokens.

    Tries the raw string and leading-space variant (tokenizers often encode
    mid-sentence names with a leading space). Falls back to decoded-string
    character-offset matching for tokenizer edge cases. Returns empty list if
    no match is found.
    """
    input_ids = [t.item() for t in input_tokens]
    n = len(input_ids)

    for variant in (entity_text, " " + entity_text):
        encoded = tokenizer.encode(variant, add_special_tokens=False)
        m = len(encoded)
        if m == 0 or m > n:
            continue
        for start in range(n - m + 1):
            if input_ids[start:start + m] == encoded:
                return list(range(start, start + m))

    decoded = [tokenizer.decode([tid]) for tid in input_ids]
    joined = "".join(decoded)
    target = entity_text.lower()
    idx = joined.lower().find(target)
    if idx == -1:
        return []
    char_end = idx + len(target)
    cum = 0
    tok_start = tok_end = None
    for i, tok in enumerate(decoded):
        next_cum = cum + len(tok)
        if tok_start is None and next_cum > idx:
            tok_start = i
        if tok_end is None and next_cum >= char_end:
            tok_end = i + 1
            break
        cum = next_cum
    if tok_start is not None and tok_end is not None:
        return list(range(tok_start, tok_end))
    return []


def _per_embedding_total_effect(
    adjacency_matrix: torch.Tensor,
    embed_start: int,
    n_pos: int,
    target_idx: int,
    max_hops: int,
) -> torch.Tensor:
    """Return tensor of shape [n_pos] with total path-sum effect on target_idx
    for each embedding position.

    Iterated forward matmul starting from one-hot columns at each embedding position.
    Since the graph is layer-ordered (feed-forward), the matrix is effectively
    nilpotent and the series terminates after max_hops steps.
    """
    n_total = adjacency_matrix.shape[0]
    dtype = adjacency_matrix.dtype
    device = adjacency_matrix.device

    # X[:, p] tracks propagation that originated at embedding position p.
    X = torch.zeros(n_total, n_pos, dtype=dtype, device=device)
    for p in range(n_pos):
        X[embed_start + p, p] = 1.0

    total_at_target = torch.zeros(n_pos, dtype=dtype, device=device)
    for _ in range(max_hops):
        X = adjacency_matrix @ X
        total_at_target = total_at_target + X[target_idx, :]
        # Early exit once propagation has decayed to numerical noise.
        if X.abs().max() < 1e-12:
            break
    return total_at_target


def position_attribution(
    ctx: ToolContext,
    entity_span: list[int] | None,
    *,
    target_logit_idx: int = 0,
) -> dict:
    """Compute entity vs non-entity attribution fraction to the target logit.

    Args:
        ctx: ToolContext carrying the attribution graph.
        entity_span: List of input token positions that correspond to the subject
            name. Pass [] if the span could not be located — `entity_frac` will
            be 0 in that case.
        target_logit_idx: Which top logit to analyze (0 = most probable).

    Returns:
        Dict with keys:
            - entity_frac: entity attribution / total (0..1). Length-dependent:
              a long template mechanically shrinks this even when the entity's
              per-token contribution is constant.
            - non_entity_frac: 1 - entity_frac
            - entity_density: per-token mean of |effect| over entity tokens
            - non_entity_density: per-token mean over template tokens
            - entity_lift: entity_density / non_entity_density. Length-invariant
              ratio of per-token attribution rates. ≈1 → entity sits at baseline
              rate (template-driven). >>1 → attribution concentrates on entity.
              None if the template has zero attribution mass.
            - entity_span: echoed input
            - per_position_abs: list of |total_effect[logit, p]| per input position
            - target_logit_idx
            - n_pos
    """
    g = ctx.graph
    n_features = len(g.selected_features)
    n_layers = g.cfg.n_layers
    n_pos = g.n_pos
    n_logits = len(g.logit_tokens)

    embed_start = n_features + n_layers * n_pos
    # Logits are the last n_logits nodes of the adjacency matrix.
    n_total = g.adjacency_matrix.shape[0]
    target_idx = n_total - n_logits + target_logit_idx

    max_hops = n_layers + 2  # generous upper bound; the series is finite anyway

    total_per_pos = _per_embedding_total_effect(
        g.adjacency_matrix,
        embed_start=embed_start,
        n_pos=n_pos,
        target_idx=target_idx,
        max_hops=max_hops,
    )

    per_pos_abs = total_per_pos.abs()
    total_sum = per_pos_abs.sum().item()
    entity_span = list(entity_span) if entity_span else []

    n_entity = len(entity_span)
    n_non_entity = n_pos - n_entity

    if total_sum > 0 and entity_span:
        entity_sum = per_pos_abs[entity_span].sum().item()
        entity_frac = entity_sum / total_sum
        non_entity_sum = total_sum - entity_sum
        entity_density = entity_sum / n_entity if n_entity > 0 else 0.0
        non_entity_density = (
            non_entity_sum / n_non_entity if n_non_entity > 0 else 0.0
        )
        # Density lift: per-token attribution rate on entity tokens vs template
        # tokens. Removes the length-dilution of entity_frac — a long template
        # inflates the denominator of entity_frac even when the entity's
        # per-token contribution is unchanged. lift ≈ 1 → entity sits at
        # baseline rate; lift >> 1 → attribution concentrates on the entity.
        if non_entity_density > 0:
            entity_lift = entity_density / non_entity_density
        else:
            entity_lift = None
    else:
        entity_frac = 0.0
        entity_density = 0.0
        non_entity_density = 0.0
        entity_lift = None

    return {
        "entity_frac": float(entity_frac),
        "non_entity_frac": float(1.0 - entity_frac),
        "entity_density": float(entity_density),
        "non_entity_density": float(non_entity_density),
        "entity_lift": float(entity_lift) if entity_lift is not None else None,
        "entity_span": entity_span,
        "per_position_abs": [float(v) for v in per_pos_abs.tolist()],
        "target_logit_idx": int(target_logit_idx),
        "n_pos": int(n_pos),
    }
