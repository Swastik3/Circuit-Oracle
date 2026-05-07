"""Multi-agent orchestrator for the circuit oracle."""

import concurrent.futures
import json
import time

from .config import ToolContext
from .llm_client import LLMClient
from .saving import compute_cost
from .subagent import execute_tool, trace_path_subagent
from .tool_schemas import TOOLS
from .tools import intervene_feature, intervene_supernode

from .skills import REFUSAL_SKILL  # noqa: F401


BASE_SYSTEM_PROMPT = """You are a mechanistic interpretability analyst inspecting a target language model's attribution graph. Use the available tools to trace causal structure in the graph and answer the user's question."""



def _missing_anchor_pass_features(all_tool_calls: list) -> list[tuple[int, int]]:
    """Return (layer, feature_idx) tuples that were pinned in BUILD but never
    hit by anchor_pass or intervene_feature(scale=-1). Uses the most recent
    build_circuit call (which overwrites previous ones). Embedding nodes
    (layer=0) and output logit nodes (no features) auto-skip via empty features
    arrays."""
    pinned: set[tuple[int, int]] = set()
    last_build = None
    for tc in all_tool_calls:
        if tc.get("tool") == "build_circuit":
            last_build = tc
    if last_build is None:
        return []
    for node in last_build.get("input", {}).get("nodes", []) or []:
        for feat in node.get("features", []) or []:
            layer = feat.get("layer")
            fid = feat.get("feature_idx")
            if layer is None or fid is None or layer == 0:
                continue
            pinned.add((layer, fid))

    anchored: set[tuple[int, int]] = set()
    for tc in all_tool_calls:
        tool = tc.get("tool")
        out = tc.get("output")
        # Skip rejected/errored calls — they did not actually anchor anything.
        if isinstance(out, dict) and "error" in out:
            continue
        inp = tc.get("input", {}) or {}
        if tool == "anchor_pass":
            for feat in inp.get("features", []) or []:
                layer = feat.get("layer")
                fid = feat.get("feature_idx")
                if layer is None or fid is None:
                    continue
                anchored.add((layer, fid))
        elif tool == "intervene_feature":
            if inp.get("scale") != -1:
                continue
            layer = inp.get("layer")
            fid = inp.get("feature_idx")
            if layer is None or fid is None:
                continue
            anchored.add((layer, fid))

    return sorted(pinned - anchored)


def _intervention_measurement_count(all_tool_calls: list) -> int:
    """Count VERIFY-phase measurements. anchor_pass with N features counts as N
    measurements (each feature is a separate before/after measurement);
    intervene_feature and intervene_supernode each count as 1.

    Rejected calls (output contains an `error` key — anchor_required, gradual_required,
    already_run) are excluded since no measurement actually happened.
    """
    count = 0
    for tc in all_tool_calls:
        tool = tc.get("tool")
        out = tc.get("output")
        if isinstance(out, dict) and "error" in out:
            continue
        if tool == "anchor_pass":
            inp = tc.get("input", {}) or {}
            features = inp.get("features", []) or []
            count += len(features)
        elif tool in ("intervene_feature", "intervene_supernode"):
            count += 1
    return count


def run_circuit_oracle(
    ctx: ToolContext,
    client: LLMClient,
    user_query: str,
    *,
    orchestrator_model: str = "claude-opus-4-6",
    subagent_model: str = "claude-sonnet-4-6",
    max_subagent_hops: int = 12,
    verbose: bool = True,
    skill: str | None = None,
) -> dict:
    """Run the multi-agent circuit oracle on a user query.

    Returns dict with keys: response, tool_calls, usage, turns.
    Usage includes orchestrator and subagents token counts.
    """
    t_start = time.monotonic()
    messages = [{"role": "user", "content": user_query}]
    all_tool_calls = []
    _subagent_counter = [0]  # persistent across dispatch rounds
    orchestrator_usage = {
        "model": orchestrator_model,
        "input_tokens": 0,
        "output_tokens": 0,
        "cache_creation_input_tokens": 0,
        "cache_read_input_tokens": 0,
    }
    subagent_usages = []
    turn_count = 0

    MIN_INTERVENTIONS = 15
    MAX_GUARD_RETRIES = 2
    guard_retries = 0

    if skill is None:
        skill = REFUSAL_SKILL
    system_prompt = BASE_SYSTEM_PROMPT + "\n\n" + skill

    while True:
        response = client.create_message(
            model=orchestrator_model,
            max_tokens=8192,
            system=system_prompt,
            tools=TOOLS,
            messages=messages,
        )
        messages.append({"role": "assistant", "content": response.content})

        turn_count += 1
        usage = response.usage
        orchestrator_usage["input_tokens"] += usage.input_tokens
        orchestrator_usage["output_tokens"] += usage.output_tokens
        orchestrator_usage["cache_creation_input_tokens"] += (
            getattr(usage, "cache_creation_input_tokens", 0) or 0
        )
        orchestrator_usage["cache_read_input_tokens"] += (
            getattr(usage, "cache_read_input_tokens", 0) or 0
        )

        if verbose:
            print(
                f"\n[Turn {turn_count}] input={usage.input_tokens:,} output={usage.output_tokens:,} "
                f"stop={response.stop_reason}"
            )

        if response.stop_reason == "end_turn":
            intervention_count = _intervention_measurement_count(all_tool_calls)
            if (
                intervention_count < MIN_INTERVENTIONS
                and guard_retries < MAX_GUARD_RETRIES
            ):
                guard_retries += 1
                remaining = MIN_INTERVENTIONS - intervention_count
                nudge = (
                    f"REJECTED: VERIFY ended with only {intervention_count} intervention "
                    f"measurement(s). Hard minimum is {MIN_INTERVENTIONS}. You have at least "
                    f"{remaining} more measurement(s) to run before you may end your turn. "
                    f"Resume VERIFY now from the phase you were in: "
                    f"Phase 2 = `intervene_feature` at -2/-3/-4 on any softened singles "
                    f"(gradual: -2 first, then -3, then -4 — the harness rejects skips). "
                    f"Phase 3 = `intervene_supernode` (synthesis or broad-union fallback) "
                    f"starting at -1 and escalating gradually -1 → -2 → -3 → -4. "
                    f"Phase 3 is mandatory (hard minimum 8 supernode calls) regardless of single-feature wins. "
                    f"Identical replicates are rejected — pick a different feature, factor, or "
                    f"feature-set. Do NOT call build_circuit again. "
                    f"AFTER you finish the remaining measurements, your final turn MUST be the full "
                    f"ANALYZE narrative as specified in step 6 of the system prompt: covering EVERY "
                    f"meaningful intervention from the entire VERIFY phase (not just these remediation "
                    f"calls), with the judge classification (`win`/`softened`/`no-shift`, plus "
                    f"`degenerate` qualifier where fluency broke) named for each, the comparative "
                    f"reasoning across the run, and the final Verdict / Suppression circuit / Winning "
                    f"interventions / Softened + dead-ends / Reasoning sections in full. Do NOT end "
                    f"your turn with a question or a partial summary. The narrative you write next is "
                    f"the authoritative report for this run."
                )
                if verbose:
                    print(
                        f"\n[Guard] intervention_count={intervention_count} < "
                        f"{MIN_INTERVENTIONS}; injecting nudge "
                        f"(retry {guard_retries}/{MAX_GUARD_RETRIES})"
                    )
                messages.append({"role": "user", "content": nudge})
                continue
            if (
                intervention_count < MIN_INTERVENTIONS
                and guard_retries >= MAX_GUARD_RETRIES
                and verbose
            ):
                print(
                    f"\n[Guard] intervention_count={intervention_count} still below "
                    f"{MIN_INTERVENTIONS} after {MAX_GUARD_RETRIES} retries; accepting."
                )

            # Anchor-pass coverage guard: every BUILD-pinned feature must have
            # been anchored at -1 (via anchor_pass or intervene_feature(scale=-1)).
            missing_anchors = _missing_anchor_pass_features(all_tool_calls)
            if missing_anchors and guard_retries < MAX_GUARD_RETRIES:
                guard_retries += 1
                missing_str = ", ".join(
                    f"L{l}:F{f}" for (l, f) in missing_anchors
                )
                nudge = (
                    f"REJECTED: VERIFY anchor pass is incomplete. "
                    f"{len(missing_anchors)} BUILD-pinned feature(s) were never "
                    f"anchored at factor=-1: {missing_str}. "
                    f"The anchor pass is mandatory on EVERY pinned feature, no "
                    f"exclusions -- BUILD has already filtered formatting and "
                    f"non-suppression features. Call anchor_pass with these missing "
                    f"features now (or intervene_feature(scale=-1) on each), then "
                    f"continue with Phase 2 depth-first escalation on any new softened "
                    f"singles, then Phase 3 synthesis-supernode or broad-union fallback "
                    f"(mandatory, hard minimum 8 supernode calls, runs regardless of single-feature wins). Do NOT call "
                    f"build_circuit again. "
                    f"AFTER you finish remediation, your final turn MUST be the full ANALYZE "
                    f"narrative as specified in step 6 of the system prompt: covering EVERY "
                    f"meaningful intervention from the entire VERIFY phase (not just these "
                    f"remediation calls), with the judge classification (`win`/`softened`/`no-shift`, "
                    f"plus `degenerate` qualifier where fluency broke) named for each, the comparative "
                    f"reasoning across the run, and the final Verdict / Suppression circuit / Winning "
                    f"interventions / Softened + dead-ends / Reasoning sections in full. Do NOT end "
                    f"your turn with a question or a partial summary. The narrative you write next is "
                    f"the authoritative report for this run."
                )
                if verbose:
                    print(
                        f"\n[Guard] anchor-pass coverage incomplete: "
                        f"{len(missing_anchors)} feature(s) missing "
                        f"(retry {guard_retries}/{MAX_GUARD_RETRIES})"
                    )
                messages.append({"role": "user", "content": nudge})
                continue
            if (
                missing_anchors
                and guard_retries >= MAX_GUARD_RETRIES
                and verbose
            ):
                print(
                    f"\n[Guard] anchor-pass coverage still incomplete "
                    f"({len(missing_anchors)} missing) after {MAX_GUARD_RETRIES} "
                    f"retries; accepting."
                )
            elapsed_seconds = time.monotonic() - t_start
            final_text = next(
                (b.text for b in response.content if b.type == "text"), ""
            )
            if verbose:
                total_in = orchestrator_usage["input_tokens"] + sum(
                    s["input_tokens"] for s in subagent_usages
                )
                total_out = orchestrator_usage["output_tokens"] + sum(
                    s["output_tokens"] for s in subagent_usages
                )
                total_cache_read = orchestrator_usage["cache_read_input_tokens"] + sum(
                    s.get("cache_read_input_tokens", 0) for s in subagent_usages
                )
                total_cache_write = orchestrator_usage[
                    "cache_creation_input_tokens"
                ] + sum(
                    s.get("cache_creation_input_tokens", 0) for s in subagent_usages
                )
                print(f"\n{'─' * 60}")
                print(f"Total orchestrator turns: {turn_count}")
                print(f"Total input tokens:  {total_in:,}")
                print(f"Total output tokens: {total_out:,}")
                print(f"Total tokens:        {total_in + total_out:,}")
                if total_cache_read or total_cache_write:
                    print(f"Cache read tokens:   {total_cache_read:,}")
                    print(f"Cache write tokens:  {total_cache_write:,}")
                print(f"Subagent calls: {len(subagent_usages)}")
                sub_tool_calls = sum(
                    len(tc["output"].get("trace_log", []))
                    for tc in all_tool_calls
                    if tc["tool"] == "trace_path_subagent"
                    and isinstance(tc["output"], dict)
                )
                print(f"Subagent tool calls: {sub_tool_calls}")
                # Cost estimate
                all_usages = [orchestrator_usage] + subagent_usages
                costs = [compute_cost(u) for u in all_usages]
                if all(c is not None for c in costs):
                    print(f"Estimated cost:      ~${sum(costs):.4f}")
                mins, secs = divmod(int(elapsed_seconds), 60)
                print(f"Wall-clock time:     {mins}m {secs}s")
                print(f"{'─' * 60}")
            return {
                "response": final_text,
                "tool_calls": all_tool_calls,
                "usage": {
                    "orchestrator": orchestrator_usage,
                    "subagents": subagent_usages,
                },
                "turns": turn_count,
                "elapsed_seconds": elapsed_seconds,
            }

        # Execute tool calls. Subagent calls run concurrently, others immediately.
        tool_use_blocks = [b for b in response.content if b.type == "tool_use"]
        results_by_id = {}

        # Split into subagent vs non-subagent blocks
        subagent_blocks = [
            b for b in tool_use_blocks if b.name == "trace_path_subagent"
        ]
        other_blocks = [b for b in tool_use_blocks if b.name != "trace_path_subagent"]

        # Execute non-subagent tools immediately (they're fast)
        for block in other_blocks:
            if verbose:
                print(f"\n--- Tool: {block.name} ---")
                inp_str = json.dumps(block.input, indent=2)
                print(f"Input: {inp_str[:300]}{'...' if len(inp_str) > 300 else ''}")
            result = execute_tool(ctx, block.name, block.input)
            if verbose:
                output_str = json.dumps(result, indent=2)
                print(
                    f"Output: {output_str[:500]}{'...' if len(output_str) > 500 else ''}"
                )
            results_by_id[block.id] = result

        # Dispatch all subagent calls concurrently
        if subagent_blocks:
            # Assign stable SA-N labels for this batch
            labels_by_id = {}
            for i, block in enumerate(subagent_blocks):
                _subagent_counter[0] += 1
                labels_by_id[block.id] = f"SA-{_subagent_counter[0]}"

            def _run_subagent(block, label):
                try:
                    result = trace_path_subagent(
                        ctx,
                        client,
                        subagent_model,
                        direction=block.input["direction"],
                        starting_layer=block.input["starting_layer"],
                        starting_feature_idx=block.input["starting_feature_idx"],
                        starting_pos=block.input["starting_pos"],
                        objective=block.input["objective"],
                        max_hops=block.input.get("max_hops", max_subagent_hops),
                        verbose=verbose,
                        label=label,
                    )
                except Exception as e:
                    result = {
                        "error": f"Subagent failed: {e}",
                        "discovered_features": [],
                        "discovered_edges": [],
                        "explanation": "",
                    }
                return block.id, result

            if verbose:
                for block in subagent_blocks:
                    print(f"\n--- Tool: {block.name} [{labels_by_id[block.id]}] ---")
                    inp_str = json.dumps(block.input, indent=2)
                    print(
                        f"Input: {inp_str[:300]}{'...' if len(inp_str) > 300 else ''}"
                    )

            with concurrent.futures.ThreadPoolExecutor(
                max_workers=len(subagent_blocks)
            ) as executor:
                futures = [
                    executor.submit(_run_subagent, block, labels_by_id[block.id])
                    for block in subagent_blocks
                ]
                for future in concurrent.futures.as_completed(futures):
                    block_id, result = future.result()
                    results_by_id[block_id] = result
                    # Collect subagent usage
                    if isinstance(result, dict) and "usage" in result:
                        subagent_usages.append(result["usage"])

        # Reassemble tool_results in original order and record all_tool_calls
        tool_results = []
        for block in tool_use_blocks:
            result = results_by_id[block.id]

            entry = {
                "tool": block.name,
                "input": block.input,
                "output": result,
            }
            if block.name == "trace_path_subagent":
                entry["label"] = labels_by_id.get(block.id, "")
            all_tool_calls.append(entry)

            # Strip trace_log before sending to API (saves context)
            api_result = result
            if block.name == "trace_path_subagent" and isinstance(result, dict):
                api_result = {
                    k: v for k, v in result.items() if k not in ("trace_log", "usage")
                }

            tool_results.append(
                {
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": json.dumps(api_result),
                }
            )

        messages.append({"role": "user", "content": tool_results})
