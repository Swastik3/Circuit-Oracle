"""Unified LLM client supporting Anthropic and OpenRouter."""

import os
import time
from anthropic import Anthropic


_NONRETRYABLE_STOP_REASONS = frozenset({
    "refusal",         # Anthropic native refusal
    "content_filter",  # OpenRouter-normalized content filter
    "max_tokens",      # hit generation budget — same again on retry
    "stop_sequence",   # user-configured stop string hit
})

_NONRETRYABLE_STATUS_CODES = frozenset({401, 403, 404, 422})
# Note: 400 removed because OpenRouter intermittently returns 400 on valid
# requests (transient infrastructure). We retry with backoff.


class LLMClient:
    """Thin wrapper around the Anthropic SDK that supports OpenRouter via base_url override."""

    MAX_RETRIES = 3
    BACKOFF_BASE_SECONDS = 1.0

    def __init__(self, provider: str = "anthropic", api_key: str | None = None):
        self.provider = provider
        if provider == "openrouter":
            key = api_key or os.environ.get("OPENROUTER_API_KEY", "")
            self._client = Anthropic(
                base_url="https://openrouter.ai/api",
                auth_token=key,
                api_key="",
            )
        else:
            self._client = Anthropic(api_key=api_key)

    def create_message(self, *, model, system, messages, tools=None, max_tokens=4096, temperature: float | None = None):
        """Create a message with retry on transient empty responses.

        Some upstreams (notably minimax via OpenRouter) intermittently return 200
        responses with no content blocks or zero tokens — a well-documented
        infrastructure transience covered by OpenRouter's Zero Completion Insurance.
        We retry these with exponential backoff.

        We do NOT retry when the empty response carries a legitimate stop signal
        (refusal, content_filter, max_tokens, stop_sequence) — these will not
        resolve on retry. We also do NOT retry on client-side HTTP errors
        (auth, bad request, policy block) — they are deterministic.
        """
        kwargs = dict(
            model=self.resolve_model(model),
            max_tokens=max_tokens,
            system=system,
            messages=messages,
        )
        if tools:
            kwargs["tools"] = tools
        if temperature is not None:
            kwargs["temperature"] = temperature

        last_diagnostic = None
        for attempt in range(self.MAX_RETRIES + 1):
            try:
                response = self._client.messages.create(**kwargs)
                if _has_useful_content(response):
                    return response
                stop = getattr(response, "stop_reason", None)
                if stop in _NONRETRYABLE_STOP_REASONS:
                    print(
                        f"[LLMClient] non-retryable empty response "
                        f"(model={kwargs['model']}, stop_reason={stop!r}) — returning to caller"
                    )
                    return response
                n_blocks = len(getattr(response, "content", []) or [])
                last_diagnostic = (
                    f"empty response (stop_reason={stop!r}, content_blocks={n_blocks})"
                )
            except Exception as e:
                status = getattr(e, "status_code", None)
                if status in _NONRETRYABLE_STATUS_CODES:
                    raise
                last_diagnostic = f"{type(e).__name__}: {e}"

            if attempt < self.MAX_RETRIES:
                sleep_s = self.BACKOFF_BASE_SECONDS * (2 ** attempt)
                print(
                    f"[LLMClient retry {attempt + 1}/{self.MAX_RETRIES}] "
                    f"model={kwargs['model']} — {last_diagnostic} — sleeping {sleep_s:.1f}s"
                )
                time.sleep(sleep_s)

        raise RuntimeError(
            f"LLMClient.create_message failed after {self.MAX_RETRIES + 1} attempts "
            f"(model={kwargs['model']}): {last_diagnostic}"
        )

    def resolve_model(self, model: str) -> str:
        """Prefix model name for OpenRouter if needed."""
        if self.provider == "openrouter" and "/" not in model:
            return f"anthropic/{model}"
        return model


def _has_useful_content(response) -> bool:
    """Return True if the response contains at least one tool_use block or non-empty text.

    Empty responses (content=[], or all text blocks whitespace-only) indicate
    an upstream drop rather than a legitimate stop.
    """
    content = getattr(response, "content", None)
    if not content:
        return False
    for block in content:
        btype = getattr(block, "type", None)
        if btype == "tool_use":
            return True
        if btype == "text" and (getattr(block, "text", "") or "").strip():
            return True
    return False


def shorten_model_name(model: str) -> str:
    """Derive a short directory-friendly model name.

    Examples:
        claude-opus-4-6 -> opus-4-6
        anthropic/claude-sonnet-4-6 -> sonnet-4-6
        openai/gpt-4o -> gpt-4o
        google/gemini-2.5-flash -> gemini-2.5-flash
    """
    # Strip provider prefix
    if "/" in model:
        model = model.split("/", 1)[1]
    # Strip claude- prefix
    if model.startswith("claude-"):
        model = model[len("claude-"):]
    return model
