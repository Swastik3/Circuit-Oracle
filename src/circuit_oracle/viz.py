"""Visualization helpers: HTML tool-chain table and SVG circuit diagram.

All functions return strings (no IPython dependency).
"""

import json
import re
import html as html_lib


# ── Private helpers ───────────────────────────────────────────────────────────

# Pattern for strings like "L7:F97156" or "L7:97156"
_FEAT_STR_RE = re.compile(r"L(\d+):F?(\d+)")


def _coerce_feature(feat) -> dict | None:
    """Coerce a feature entry to a dict, or return None if unparseable.

    LLMs sometimes return "L7:F97156" strings instead of proper dicts.
    """
    if isinstance(feat, dict):
        if "layer" in feat and "feature_idx" in feat:
            return feat
        return None
    if isinstance(feat, str):
        # Try JSON first
        try:
            parsed = json.loads(feat)
            if isinstance(parsed, dict) and "layer" in parsed:
                return parsed
        except (json.JSONDecodeError, TypeError):
            pass
        # Try "L7:F97156" pattern
        m = _FEAT_STR_RE.search(feat)
        if m:
            return {"layer": int(m.group(1)), "feature_idx": int(m.group(2))}
    return None


def _text_width(text, font_size=11):
    """Rough estimate of text width in pixels."""
    return len(text) * font_size * 0.58


def _wrap_text(text, max_chars=28):
    """Wrap text into lines for SVG display."""
    words = text.split()
    lines = []
    current = ""
    for w in words:
        if current and len(current) + len(w) + 1 > max_chars:
            lines.append(current)
            current = w
        else:
            current = f"{current} {w}" if current else w
    if current:
        lines.append(current)
    return lines


def _fmt_output(tool_name, output):
    """Format tool output for the HTML table based on tool type."""
    if isinstance(output, dict) and "error" in output:
        return f'<span style="color:red">{html_lib.escape(output["error"])}</span>'
    if tool_name == "get_top_logits":
        return ", ".join(f'{e["token"]} ({e["probability"]*100:.1f}%)' for e in output)
    if tool_name == "get_top_features":
        return "<br>".join(
            f'L{e["layer"]}:F{e["feature_idx"]} (de={e["direct_effect"]:.3f})'
            for e in output[:8]
        )
    if tool_name == "inspect_feature":
        label = html_lib.escape(output.get("label", "?"))
        promoted = ", ".join(output.get("promoted_tokens", [])[:5])
        return f'<b>{label}</b><br>promotes: {html_lib.escape(promoted)}'
    if tool_name == "get_upstream_features":
        return "<br>".join(
            f'L{e["layer"]}:F{e["feature_idx"]} (de={e["direct_effect"]:.3f})'
            for e in output[:6]
        )
    if tool_name == "build_circuit":
        nodes = output.get("nodes", [])
        edges = output.get("edges", [])
        node_strs = [html_lib.escape(n.get("label", n.get("id", "?"))) for n in nodes[:6]]
        return f'{len(nodes)} nodes, {len(edges)} edges<br>{"  ·  ".join(node_strs)}'
    if tool_name == "trace_path_subagent":
        if isinstance(output, dict):
            features = output.get("discovered_features", [])
            edges = output.get("discovered_edges", [])
            explanation = output.get("explanation", "")
            trace_log = output.get("trace_log", [])
            feat_strs = [
                f'L{f["layer"]}:F{f["feature_idx"]} ({html_lib.escape(f.get("label", "?")[:30])})'
                for f in features[:5]
            ]
            summary = (
                f'<b>{len(features)} features, {len(edges)} edges</b><br>'
                f'{"<br>".join(feat_strs)}'
                f'{"<br>..." if len(features) > 5 else ""}<br>'
                f'<i>{html_lib.escape(explanation[:200])}</i>'
            )
            if trace_log:
                trace_rows = ""
                for i, tc in enumerate(trace_log, 1):
                    inp = html_lib.escape(json.dumps(tc["input"], separators=(",", ":"))[:100])
                    out = _fmt_output(tc["tool"], tc["output"])
                    trace_rows += (
                        f'<tr><td>{i}</td><td><code>{tc["tool"]}</code></td>'
                        f'<td style="font-size:10px">{inp}</td>'
                        f'<td style="font-size:10px">{out}</td></tr>'
                    )
                summary += (
                    f'<details style="margin-top:4px"><summary style="cursor:pointer;color:#666">'
                    f'Trace log ({len(trace_log)} calls)</summary>'
                    f'<table class="tc-table" style="margin-top:4px">'
                    f'<tr><th>#</th><th>Tool</th><th>Input</th><th>Output</th></tr>'
                    f'{trace_rows}</table></details>'
                )
            return summary
        return html_lib.escape(str(output)[:200])
    return html_lib.escape(json.dumps(output)[:200])


# ── B. Attribution Data Extraction ────────────────────────────────────────────

def build_attribution_data(tool_calls) -> dict | None:
    """Extract circuit data, top logits, and feature labels from tool calls.

    Returns dict with keys: circuit_data, top_logits, feature_labels — or None if
    no build_circuit call was found.
    """
    circuit_data = None
    top_logits = []
    feature_labels = {}

    for tc in tool_calls:
        if tc["tool"] == "build_circuit" and "error" not in tc["output"]:
            circuit_data = tc["output"]
        if tc["tool"] == "get_top_logits":
            top_logits = [(e["token"], e["probability"]) for e in tc["output"][:6]]
        if tc["tool"] == "inspect_feature" and "error" not in tc["output"]:
            out = tc["output"]
            feature_labels[(out["layer"], out["feature_idx"])] = out.get("label", "")
        if tc["tool"] == "trace_path_subagent" and isinstance(tc["output"], dict):
            for sub_tc in tc["output"].get("trace_log", []):
                if sub_tc["tool"] == "inspect_feature" and "error" not in sub_tc["output"]:
                    out = sub_tc["output"]
                    feature_labels[(out["layer"], out["feature_idx"])] = out.get("label", "")
            for feat in tc["output"].get("discovered_features", []):
                feat = _coerce_feature(feat)
                if feat is None:
                    continue
                key = (feat["layer"], feat["feature_idx"])
                if key not in feature_labels and feat.get("label"):
                    feature_labels[key] = feat["label"]

    if not circuit_data:
        # Fallback: synthesize circuit_data from subagent discovered_features/edges.
        # One node per unique feature, edges from discovered_edges.
        nodes_by_key = {}
        all_edges = []
        for tc in tool_calls:
            if tc["tool"] != "trace_path_subagent" or not isinstance(tc.get("output"), dict):
                continue
            for feat in tc["output"].get("discovered_features", []):
                feat = _coerce_feature(feat)
                if feat is None:
                    continue
                key = f"{feat['layer']}_{feat['feature_idx']}_{feat.get('pos', 0)}"
                if key not in nodes_by_key:
                    label = feat.get("label") or f"L{feat['layer']}:F{feat['feature_idx']}"
                    nodes_by_key[key] = {
                        "id": key,
                        "label": label,
                        "layer": feat["layer"],
                        "features": [{"layer": feat["layer"], "feature_idx": feat["feature_idx"], "pos": feat.get("pos", 0)}],
                    }
            for e in tc["output"].get("discovered_edges", []):
                if not isinstance(e, dict):
                    continue
                if not all(k in e for k in ("from_layer", "from_feature_idx", "from_pos", "to_layer", "to_feature_idx", "to_pos")):
                    continue
                from_key = f"{e['from_layer']}_{e['from_feature_idx']}_{e['from_pos']}"
                to_key = f"{e['to_layer']}_{e['to_feature_idx']}_{e['to_pos']}"
                all_edges.append({"from": from_key, "to": to_key})

        if not nodes_by_key:
            return None

        # Deduplicate edges
        seen_edges = set()
        deduped_edges = []
        for e in all_edges:
            k = (e["from"], e["to"])
            if k not in seen_edges:
                seen_edges.add(k)
                deduped_edges.append(e)

        circuit_data = {"nodes": list(nodes_by_key.values()), "edges": deduped_edges, "status": "synthesized_from_subagents"}

    return {
        "circuit_data": circuit_data,
        "top_logits": top_logits,
        "feature_labels": feature_labels,
    }


# ── C. SVG Renderer ──────────────────────────────────────────────────────────

NODE_FILL = "#e8e8e8"
NODE_STROKE = "#999"
NODE_TEXT = "#333"
NODE_FEAT_TEXT = "#666"
EDGE_COLOR = "#8B4513"
ARROW_COLOR = "#8B4513"


def create_circuit_svg(circuit_data, top_logits, feature_labels, prompt) -> str:
    """Create an SVG visualization of the attribution circuit.

    Returns the SVG as a string.
    """
    nodes = circuit_data["nodes"]
    edges = circuit_data["edges"]

    if not nodes:
        return '<svg width="400" height="100"><text x="20" y="50">No circuit data</text></svg>'

    # ── Layout: group by layer, compute positions ──
    layer_groups = {}
    for n in nodes:
        layer_groups.setdefault(n["layer"], []).append(n)
    sorted_layers = sorted(layer_groups.keys())

    NODE_PAD_X = 20
    NODE_MIN_W = 160
    NODE_H_BASE = 44
    FEATURE_LINE_H = 14
    ROW_GAP = 80
    COL_GAP = 40
    MARGIN_LEFT = 80
    MARGIN_TOP = 70

    # Pre-compute node sizes and feature text
    node_info = {}
    for n in nodes:
        label_lines = _wrap_text(n["label"], max_chars=26)
        feat_lines = []
        for f in n.get("features", [])[:4]:
            fl, fi = f["layer"], f["feature_idx"]
            lbl = feature_labels.get((fl, fi), "")
            if lbl:
                feat_lines.append(f"L{fl}:F{fi} — {lbl[:30]}")
            else:
                feat_lines.append(f"L{fl}:F{fi}")
        if len(n.get("features", [])) > 4:
            feat_lines.append(f"... +{len(n['features']) - 4} more")

        max_text = max(
            [_text_width(l, 12) for l in label_lines]
            + [_text_width(l, 9.5) for l in feat_lines]
            + [NODE_MIN_W]
        )
        w = max_text + NODE_PAD_X * 2
        h = NODE_H_BASE + len(feat_lines) * FEATURE_LINE_H
        node_info[n["id"]] = {
            "label_lines": label_lines,
            "feat_lines": feat_lines,
            "w": w,
            "h": h,
            "layer": n["layer"],
            "n_features": len(n.get("features", [])),
        }

    # Position nodes: bottom-up (earliest layer at bottom)
    node_positions = {}
    current_y = MARGIN_TOP
    for layer in reversed(sorted_layers):
        group = layer_groups[layer]
        row_w = sum(node_info[n["id"]]["w"] for n in group) + COL_GAP * (len(group) - 1)
        start_x = MARGIN_LEFT + max(0, (600 - row_w) / 2)
        max_h = max(node_info[n["id"]]["h"] for n in group)
        for n in group:
            info = node_info[n["id"]]
            cx = start_x + info["w"] / 2
            cy = current_y + max_h / 2
            node_positions[n["id"]] = (cx, cy, info["w"], info["h"])
            start_x += info["w"] + COL_GAP
        current_y += max_h + ROW_GAP

    # Canvas sizing
    all_right = max(pos[0] + pos[2] / 2 for pos in node_positions.values()) + 40
    canvas_w = max(750, all_right + MARGIN_LEFT)
    prompt_y = current_y + 10
    output_y = prompt_y + 55
    canvas_h = output_y + 50

    # ── Build SVG ──
    parts = []
    parts.append(
        f'<svg width="{int(canvas_w)}" height="{int(canvas_h)}" xmlns="http://www.w3.org/2000/svg">'
    )
    parts.append(
        f'<rect width="{int(canvas_w)}" height="{int(canvas_h)}" fill="#f5f5f5"/>'
    )
    parts.append(
        f'<rect x="15" y="15" width="{int(canvas_w)-30}" height="{int(canvas_h)-30}" '
        f'fill="white" stroke="none" rx="12"/>'
    )

    # Title
    parts.append(
        '<text x="40" y="48" fill="#666" font-family="Arial,sans-serif" font-size="14" '
        'font-weight="bold" letter-spacing="1px">ATTRIBUTION CIRCUIT</text>'
    )

    # Layer labels
    for layer in reversed(sorted_layers):
        group = layer_groups[layer]
        rep_id = group[0]["id"]
        _, cy, _, _ = node_positions[rep_id]
        parts.append(
            f'<text x="25" y="{cy + 4}" fill="#999" font-family="monospace" font-size="10" '
            f'font-weight="bold" text-anchor="start">L{layer}</text>'
        )

    # Arrow marker
    parts.append(
        f'<defs><marker id="arrow" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto">'
        f'<polygon points="0,0 8,3 0,6" fill="{ARROW_COLOR}" fill-opacity="0.7"/>'
        f'</marker></defs>'
    )

    # ── Edges ──
    for e in edges:
        if e["from"] not in node_positions or e["to"] not in node_positions:
            continue
        fx, fy, fw, fh = node_positions[e["from"]]
        tx, ty, tw, th = node_positions[e["to"]]

        if fy > ty:
            x1, y1 = fx, fy - fh / 2
            x2, y2 = tx, ty + th / 2
        else:
            x1, y1 = fx, fy + fh / 2
            x2, y2 = tx, ty - th / 2

        mid_y = (y1 + y2) / 2
        ctrl_offset = (x2 - x1) * 0.15
        path = f"M {x1},{y1} C {x1+ctrl_offset},{mid_y} {x2-ctrl_offset},{mid_y} {x2},{y2}"
        parts.append(
            f'<path d="{path}" fill="none" stroke="{EDGE_COLOR}" stroke-width="3" '
            f'stroke-opacity="0.6" marker-end="url(#arrow)"/>'
        )

    # ── Nodes ──
    for n in nodes:
        nid = n["id"]
        info = node_info[nid]
        cx, cy, w, h = node_positions[nid]
        x, y = cx - w / 2, cy - h / 2

        parts.append(
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" '
            f'fill="{NODE_FILL}" stroke="{NODE_STROKE}" stroke-width="2" rx="8"/>'
        )
        label_y = y + 18
        for i, line in enumerate(info["label_lines"]):
            esc = html_lib.escape(line)
            parts.append(
                f'<text x="{cx}" y="{label_y + i * 14}" text-anchor="middle" '
                f'fill="{NODE_TEXT}" font-family="Arial,sans-serif" font-size="12" font-weight="bold">{esc}</text>'
            )
        feat_y = label_y + len(info["label_lines"]) * 14 + 4
        for i, fl in enumerate(info["feat_lines"]):
            esc = html_lib.escape(fl)
            parts.append(
                f'<text x="{cx}" y="{feat_y + i * FEATURE_LINE_H}" text-anchor="middle" '
                f'fill="{NODE_FEAT_TEXT}" font-family="monospace" font-size="9">{esc}</text>'
            )
        fc = info["n_features"]
        badge_x = x + w - 18
        badge_y = y + 6
        parts.append(f'<circle cx="{badge_x}" cy="{badge_y + 7}" r="9" fill="#ccc"/>')
        parts.append(
            f'<text x="{badge_x}" y="{badge_y + 11}" text-anchor="middle" '
            f'fill="#666" font-family="monospace" font-size="9" font-weight="bold">{fc}</text>'
        )

    # ── Prompt section ──
    parts.append(
        f'<line x1="40" y1="{prompt_y - 10}" x2="{int(canvas_w) - 40}" y2="{prompt_y - 10}" '
        f'stroke="#ddd" stroke-width="1"/>'
    )
    parts.append(
        f'<text x="40" y="{prompt_y + 8}" fill="#666" font-family="Arial,sans-serif" '
        f'font-size="10" font-weight="bold" letter-spacing="1px">PROMPT</text>'
    )
    esc_prompt = html_lib.escape(prompt[:120])
    parts.append(
        f'<text x="40" y="{prompt_y + 26}" fill="#333" font-family="monospace" font-size="11">'
        f'"{esc_prompt}"</text>'
    )

    # ── Output tokens ──
    parts.append(
        f'<text x="40" y="{output_y - 5}" fill="#666" font-family="Arial,sans-serif" '
        f'font-size="10" font-weight="bold" letter-spacing="1px">TOP OUTPUTS</text>'
    )
    ox = 40
    for tok, prob in top_logits[:6]:
        tok_esc = html_lib.escape(tok or "(empty)")
        pct_text = f"{prob*100:.0f}%"
        item_w = len(tok_esc) * 8 + len(pct_text) * 6 + 20
        parts.append(
            f'<rect x="{ox}" y="{output_y}" width="{item_w}" height="20" '
            f'fill="#e8e8e8" stroke="none" rx="6"/>'
        )
        parts.append(
            f'<text x="{ox + 5}" y="{output_y + 14}" fill="#333" font-family="Arial,sans-serif" '
            f'font-size="11" font-weight="bold">'
            f'{tok_esc} <tspan fill="#555" font-size="10">{pct_text}</tspan></text>'
        )
        ox += item_w + 10

    parts.append("</svg>")
    return "\n".join(parts)
