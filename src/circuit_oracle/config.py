"""Configuration dataclasses for circuit oracle runs."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class ToolContext:
    """Runtime context passed to tool functions (replaces globals)."""
    graph: Any
    tokenizer: Any
    neuronpedia_model_id: str = "qwen3-4b"
    neuronpedia_sae_id: str = "{layer}-transcoder-hp"
    replacement_model: Any = None  # ReplacementModel used during graph build, needed to run feature_intervention
    baseline_activations: Any = None  # per-layer transcoder activations for the prompt, shape [n_layers, seq_len, d_transcoder]
    baseline_answer: Optional[str] = None  # greedy decoded answer under no intervention; all interventions compare against this
    baseline_prompt: Optional[str] = None  # exact prompt string used at graph-build time, replayed by intervene_feature/intervene_supernode
    # VERIFY-phase intervention bookkeeping. Populated by anchor_pass / intervene_feature / intervene_supernode
    # to enforce ordering, dedup, and gradual escalation.
    anchor_passed: set = field(default_factory=set)  # set of (layer, feat_idx) anchored at -1 (via anchor_pass or ad-hoc intervene_feature)
    anchor_pass_called: bool = False  # True once anchor_pass has run; second call is rejected
    single_factors: dict = field(default_factory=dict)  # {(layer, feat_idx): set[float]} — every factor applied to this single feature (any scale, used for replicate dedup)
    depth_factors: dict = field(default_factory=dict)  # {(layer, feat_idx): set[float]} — factors applied in depth phase only (-2/-3/-4); used for gradual-escalation prereq
    supernode_factors: dict = field(default_factory=dict)  # {frozenset((layer, feat_idx), ...): set[float]} — factors applied to each supernode
    intervention_history: list = field(default_factory=list)  # append-only ledger of every measurement (anchor_pass entries, singles, supernodes)


@dataclass
class RunConfig:
    """Configuration for a single circuit oracle run."""
    prompt_name: str
    system_prompt: str
    user_message: str
    assistant_prefix: str = ""
    question: str | None = None  # if set, appended to oracle query to direct analysis
    experiment_prefix: str = "circuit"
    orchestrator_model: str = "claude-opus-4-6"
    subagent_model: str = "claude-sonnet-4-6"
    provider: str = "anthropic"
    max_subagent_hops: int = 12  # generous ceiling; subagents stop early when they reach early layers or direct_effect decays
    model_name: str = "Qwen/Qwen3-4B"
    transcoder_name: str = "mwhanna/qwen3-4b-transcoders"
    graph_cache_dir: str = "weights/graphs"
    verbose: bool = True
    # Neuronpedia identifiers — used to build per-feature dashboard URLs in reports.
    # Must match ToolContext.neuronpedia_model_id / neuronpedia_sae_id for the model + transcoder pair.
    neuronpedia_model_id: str = "qwen3-4b"
    neuronpedia_sae_id: str = "{layer}-transcoder-hp"
