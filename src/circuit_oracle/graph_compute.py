"""Model loading, prompt formatting, and attribution graph computation.

This is the only module that imports torch and circuit_tracer.
"""

import os

import torch
from circuit_tracer.replacement_model import ReplacementModel
from circuit_tracer.attribution.attribute import attribute
from circuit_tracer.graph import Graph


def load_model(model_name: str, transcoder_name: str, dtype=torch.bfloat16):
    """Load a ReplacementModel with transcoders.

    Returns:
        model: ReplacementModel instance with .tokenizer attribute.
    """
    torch.cuda.empty_cache()
    model = ReplacementModel.from_pretrained(model_name, transcoder_name, dtype=dtype)
    print(f"Model loaded: {model.cfg.model_name}")
    print(f"Vocab size: {model.tokenizer.vocab_size}")
    return model


def format_chat(tokenizer, system_prompt: str, user_message: str, assistant_prefix: str = "") -> str:
    """Format messages using the model's chat template."""
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message},
    ]
    formatted = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
        enable_thinking=False,
    )
    if assistant_prefix:
        formatted += assistant_prefix
    return formatted


def format_chat_multiturn(tokenizer, system_prompt: str, messages: list[dict]) -> str:
    """Format a multi-turn conversation using the model's chat template.

    Args:
        tokenizer: The model's tokenizer.
        system_prompt: System prompt for the conversation.
        messages: List of {"role": "user"|"assistant", "content": "..."} dicts.

    Returns:
        Formatted prompt string ready for generation.
    """
    full_messages = [{"role": "system", "content": system_prompt}] + messages
    return tokenizer.apply_chat_template(
        full_messages,
        tokenize=False,
        add_generation_prompt=True,
        enable_thinking=False,
    )


def generate_response(prompt: str, model, max_new_tokens: int = 100) -> str:
    """Generate a response from the model and return only the newly generated tokens.

    Uses the HookedTransformer.generate() method which produces output identical
    to the original model (modifications only affect the backward pass).
    """
    input_ids = model.tokenizer(prompt, return_tensors="pt")["input_ids"].to(model.cfg.device)
    prompt_len = input_ids.shape[1]
    # use_past_kv_cache=False avoids a TransformerLens dtype mismatch in the
    # GQA + RoPE + bfloat16 path on Qwen3-4B. The KV cache crosses fp32 RoPE
    # buffers with bf16 keys, tripping `q_ @ k_` with "expected Float but
    # found BFloat16". Recomputing full-sequence forward per step is O(N^2)
    # but trivial at max_new_tokens=100 on short prompts.
    output_ids = model.generate(
        input_ids,
        max_new_tokens=max_new_tokens,
        stop_at_eos=True,
        use_past_kv_cache=False,
    )
    new_ids = output_ids[0, prompt_len:]
    return model.tokenizer.decode(new_ids, skip_special_tokens=True)


def compute_or_load_graph(
    prompt: str,
    model,
    cache_path: str | None = None,
    max_feature_nodes: int | None = None,
) -> dict:
    """Compute an attribution graph, or load from cache if available.

    Args:
        prompt: Formatted prompt string.
        model: ReplacementModel instance.
        cache_path: Optional path to cache the graph as a .pt file.
        max_feature_nodes: Cap on the number of feature nodes included in the
            graph. ``None`` means unbounded (every active feature is included,
            which can be tens of thousands for long prompts). A cap like 5000
            trades completeness for much faster attribution. Passed straight
            through to ``circuit_tracer.attribute``.

    Returns:
        Dict with keys: graph, replacement_model, baseline_activations,
        baseline_answer.
    """
    if cache_path:
        os.makedirs(os.path.dirname(cache_path) or ".", exist_ok=True)

    if cache_path and os.path.exists(cache_path):
        print(f"Loading cached graph from {cache_path}...")
        graph = Graph.from_pt(cache_path)
    else:
        cap_msg = "unbounded" if max_feature_nodes is None else f"cap={max_feature_nodes}"
        print(f"Computing attribution graph (this may take several minutes, feature-node {cap_msg})...")
        graph = attribute(
            prompt,
            model,
            offload="cpu",
            verbose=True,
            max_feature_nodes=max_feature_nodes,
        )

        if cache_path:
            graph.to_pt(cache_path)
            print(f"Saved graph to {cache_path}")

    # Capture baseline transcoder activations, used by intervene_feature/intervene_supernode for scaled patching.
    _, baseline_acts = model.get_activations(prompt)

    baseline_answer = generate_response(prompt, model, max_new_tokens=100).strip("\n")

    return {
        "graph": graph,
        "replacement_model": model,
        "baseline_activations": baseline_acts,
        "baseline_answer": baseline_answer,
    }
