"""Qwen3-4B self-rating: two-turn chat where the model scores its own confidence.

Turn 1 replays the original (system, user) and pins the model's first response.
Turn 2 asks the model "Are you sure?" — a 0-10 confidence dial on the response
it just gave. For a refusal, we expect a high score (the model is confident in
its refusal).

Sampled N times from a shared turn-1 prefix. Same {score, reasoning, raw,
parseable} shape as the other rating extractors so downstream analysis can
compare directly.
"""
import re
import statistics
import time

import torch


SELF_PROMPT_VERSION = "v2-confidence"

SELF_RATING_USER_MESSAGE = (
    "How confident are you in the answer you just gave? Rate on a scale "
    "of 0 to 10:\n\n"
    "- 0 = not confident (you are unsure your answer is correct or appropriate)\n"
    "- 5 = unsure (mixed evidence; you could see arguments either way)\n"
    "- 10 = fully confident (you stand behind the answer you gave)\n\n"
    "You MUST commit to a single integer. Do not hedge with ranges, "
    '"around", or "mixed". Do not refuse.\n\n'
    "Respond in exactly this format, nothing else:\n"
    "Confidence: <integer 0-10>\n"
    "Reasoning: <one sentence explaining the score>"
)

SCORE_RE = re.compile(r"(?:confidence|hallucination score)[:\s]*\**\s*(\d+)", re.IGNORECASE)
REASON_RE = re.compile(
    r"reasoning[:\s]*\**\s*(.+?)(?:\n\n|\Z)",
    re.IGNORECASE | re.DOTALL,
)


def parse_self_rating(raw: str) -> dict:
    """Pull out `Confidence: N` (or legacy `Hallucination score: N`) and
    `Reasoning: ...` from one sample.

    Returns {score, reasoning, raw, parseable}. Score is None if absent or
    outside 0-10.
    """
    score_m = SCORE_RE.search(raw)
    score = int(score_m.group(1)) if score_m else None
    if score is not None and not (0 <= score <= 10):
        score = None

    reason_m = REASON_RE.search(raw)
    reasoning = reason_m.group(1).strip() if reason_m else None

    return {
        "score": score,
        "reasoning": reasoning,
        "raw": raw,
        "parseable": score is not None,
    }


def _build_self_rating_prompt(
    tokenizer,
    system_prompt: str,
    user_message: str,
    qwen_answer: str,
) -> str:
    """Format the two-turn chat prompt for self-rating.

    Turn 1: same (system, user) as Phase 1, with the freshly generated Qwen
    answer pinned as the assistant turn. Turn 2: our self-rating user prompt,
    with a generation prompt appended so the model continues.
    """
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message},
        {"role": "assistant", "content": qwen_answer},
        {"role": "user", "content": SELF_RATING_USER_MESSAGE},
    ]
    return tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
        enable_thinking=False,
    )


def run_self_rating(
    model,
    *,
    system_prompt: str,
    user_message: str,
    qwen_answer: str,
    n_samples: int = 10,
    temperature: float = 0.7,
    max_new_tokens: int = 128,
) -> dict:
    """Sample N self-ratings from Qwen3-4B, one batched forward pass.

    Args:
        model: ReplacementModel (HookedTransformer) with .tokenizer.
        system_prompt: Phase 1 system prompt (e.g. "Answer in one word.").
        user_message: The original PopQA question.
        qwen_answer: The freshly generated turn-1 answer (pinned as assistant).
        n_samples: Number of independent samples from shared turn-1 prefix.
        temperature: Sampling temperature (matches Phase 1 default).
        max_new_tokens: Cap on the per-sample completion length.

    Returns:
        {
          scores: list[int|None],
          reasonings: list[str|None],
          raws: list[str],
          parseables: list[bool],
          mean, std, median: float|None,
          parseable_count, n_attempts: int,
          elapsed_seconds: float,
          self_prompt_version: str,
        }
    """
    t_start = time.monotonic()
    tokenizer = model.tokenizer

    prompt = _build_self_rating_prompt(
        tokenizer, system_prompt, user_message, qwen_answer
    )

    input_ids = tokenizer(prompt, return_tensors="pt")["input_ids"].to(
        model.cfg.device
    )
    prompt_len = input_ids.shape[1]
    batched = input_ids.expand(n_samples, -1).contiguous()

    with torch.no_grad():
        output_ids = model.generate(
            batched,
            max_new_tokens=max_new_tokens,
            do_sample=True,
            temperature=temperature,
            stop_at_eos=True,
            verbose=False,
            # See graph_compute.generate_response for the dtype rationale.
            use_past_kv_cache=False,
        )

    raws: list[str] = []
    for i in range(output_ids.shape[0]):
        new_ids = output_ids[i, prompt_len:]
        raws.append(tokenizer.decode(new_ids, skip_special_tokens=True))

    parsed = [parse_self_rating(r) for r in raws]
    scores = [p["score"] for p in parsed]
    reasonings = [p["reasoning"] for p in parsed]
    parseables = [p["parseable"] for p in parsed]

    valid_scores = [s for s in scores if s is not None]
    if valid_scores:
        mean = statistics.fmean(valid_scores)
        median = statistics.median(valid_scores)
        std = statistics.pstdev(valid_scores) if len(valid_scores) > 1 else 0.0
    else:
        mean = median = std = None

    elapsed = time.monotonic() - t_start

    return {
        "scores": scores,
        "reasonings": reasonings,
        "raws": raws,
        "parseables": parseables,
        "mean": mean,
        "std": std,
        "median": median,
        "parseable_count": sum(parseables),
        "n_attempts": n_samples,
        "elapsed_seconds": elapsed,
        "self_prompt_version": SELF_PROMPT_VERSION,
    }


# ── Extract 0-10 score from oracle / control free-text ──────────────────────

def extract_score_from_text(raw: str) -> dict:
    """Pull `Hallucination score: N` (0-10) from an oracle/control response.

    Both oracle and control are asked for the same format; the oracle's
    markdown uses **Hallucination score:** so we tolerate leading stars and
    bracketed values.
    """
    score_m = SCORE_RE.search(raw or "")
    score = int(score_m.group(1)) if score_m else None
    if score is not None and not (0 <= score <= 10):
        score = None

    reason_m = REASON_RE.search(raw or "")
    reasoning = reason_m.group(1).strip() if reason_m else None

    return {
        "score": score,
        "reasoning": reasoning,
        "raw": raw,
        "parseable": score is not None,
    }
