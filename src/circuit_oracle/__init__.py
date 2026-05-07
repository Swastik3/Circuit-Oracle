"""Circuit Oracle: Automated mechanism analysis of LLM circuits."""

from .config import RunConfig, ToolContext
from .query import build_oracle_query
from .neuronpedia_link import feature_url, feature_link
from .skills import (
    BASE_SYSTEM_PROMPT,
    REFUSAL_SKILL,
    PROBE_ORACLE_SKILL,
    TABOO_SKILL,
    TABOO_NO_OPTIONS_SKILL,
)

# These imports require external dependencies (anthropic, torch).
# They are re-exported for convenience but will raise ImportError if deps missing.
try:
    from .llm_client import LLMClient
    from .orchestrator import run_circuit_oracle
    from .control import run_control_analysis
except ImportError as ex:
    print(">>>", ex)
    pass

try:
    from .saving import save_run_results
except ImportError as ex:
    print(">>>", ex)
    pass

try:
    from .graph_compute import load_model, format_chat, compute_or_load_graph, generate_response
except ImportError as ex:
    print(">>>", ex)
    pass

try:
    from .self_rating import run_self_rating
except ImportError as ex:
    print(">>>", ex)
    pass

__all__ = [
    "RunConfig",
    "ToolContext",
    "LLMClient",
    "run_circuit_oracle",
    "BASE_SYSTEM_PROMPT",
    "REFUSAL_SKILL",
    "PROBE_ORACLE_SKILL",
    "TABOO_SKILL",
    "TABOO_NO_OPTIONS_SKILL",
    "load_model",
    "format_chat",
    "compute_or_load_graph",
    "generate_response",
    "save_run_results",
    "build_oracle_query",
    "run_control_analysis",
    "run_self_rating",
    "feature_url",
    "feature_link",
]
