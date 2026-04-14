#!/usr/bin/env python3
"""
Build a dark-themed architecture SVG from a JSON spec.

Usage:
    python build_diagram.py spec.json -o out.svg

Spec format (JSON):
{
  "title": "RAG pipeline",
  "description": "Optional accessibility description",
  "canvas": {"width": 1440, "height": 1600},   # optional; autosized if omitted
  "nodes": [
    {"id": "query", "title": "User query", "category": "neutral", "x": 590, "y": 80},
    {"id": "qu",    "title": "Query understanding", "subtitle": "Extract filters", "category": "compute", "x": 590, "y": 200}
  ],
  "groups": [
    {"label": "Azure AI Search", "x": 460, "y": 340, "w": 520, "h": 460}
  ],
  "edges": [
    {"from": "query", "to": "qu"},
    {"from": "cache", "to": "qu", "style": "dashed", "label": "hit"}
  ]
}

Categories: neutral, compute, retrieval, rank, storage, external.
Coordinates are top-left of each node. Width defaults to 260, height to 72 (52 if no subtitle).
Edges auto-route as a straight line between the nearest edges of source/target boxes.
"""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path

PALETTE = {
    "neutral":   {"fill": "#3f3f46", "stroke": "#52525b", "accent": "#d4d4d8"},
    "compute":   {"fill": "#1e3a5f", "stroke": "#2a5082", "accent": "#93c5fd"},
    "retrieval": {"fill": "#14532d", "stroke": "#1f6b3f", "accent": "#86efac"},
    "rank":      {"fill": "#3b1f6b", "stroke": "#553090", "accent": "#c4b5fd"},
    "storage":   {"fill": "#5c2e1f", "stroke": "#7a3d2a", "accent": "#fca5a5"},
    "external":  {"fill": "#4a2a5c", "stroke": "#6b3e82", "accent": "#e9d5ff"},
}
BG = "#0a0a0a"
TITLE_COLOR = "#f4f4f5"
EDGE_COLOR = "#71717a"
GROUP_FILL = "#18181b"
GROUP_STROKE = "#3f3f46"
FONT = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Inter, system-ui, sans-serif"
DEFAULT_W = 260
DEFAULT_H_FULL = 72
DEFAULT_H_TITLE_ONLY = 52


def node_box(n):
    w = n.get("w", DEFAULT_W)
    h = n.get("h", DEFAULT_H_FULL if n.get("subtitle") else DEFAULT_H_TITLE_ONLY)
    return n["x"], n["y"], w, h


def render_node(n):
    x, y, w, h = node_box(n)
    cat = PALETTE[n.get("category", "neutral")]
    cx = x + w / 2
    parts = [
        f'<g>',
        f'  <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" ry="12" '
        f'fill="{cat["fill"]}" stroke="{cat["stroke"]}" stroke-width="1"/>',
    ]
    if n.get("subtitle"):
        parts.append(
            f'  <text x="{cx}" y="{y + 32}" fill="{TITLE_COLOR}" font-size="18" '
            f'font-weight="600" text-anchor="middle">{escape(n["title"])}</text>'
        )
        parts.append(
            f'  <text x="{cx}" y="{y + 54}" fill="{cat["accent"]}" font-size="13" '
            f'text-anchor="middle">{escape(n["subtitle"])}</text>'
        )
    else:
        parts.append(
            f'  <text x="{cx}" y="{y + 32}" fill="{TITLE_COLOR}" font-size="18" '
            f'font-weight="600" text-anchor="middle">{escape(n["title"])}</text>'
        )
    parts.append('</g>')
    return "\n".join(parts)


def render_group(g):
    return (
        f'<g>\n'
        f'  <rect x="{g["x"]}" y="{g["y"]}" width="{g["w"]}" height="{g["h"]}" '
        f'rx="16" ry="16" fill="{GROUP_FILL}" fill-opacity="0.6" '
        f'stroke="{GROUP_STROKE}" stroke-width="1.5"/>\n'
        f'  <text x="{g["x"] + 24}" y="{g["y"] + 32}" fill="{TITLE_COLOR}" '
        f'font-size="16" font-weight="500">{escape(g["label"])}</text>\n'
        f'</g>'
    )


def edge_endpoints(a, b):
    """Pick an endpoint on each box to draw a straight line between."""
    ax, ay, aw, ah = node_box(a)
    bx, by, bw, bh = node_box(b)
    acx, acy = ax + aw / 2, ay + ah / 2
    bcx, bcy = bx + bw / 2, by + bh / 2
    # Vertical or horizontal?
    dx = bcx - acx
    dy = bcy - acy
    if abs(dy) >= abs(dx):
        # vertical
        if dy > 0:
            return (acx, ay + ah), (bcx, by - 2)
        else:
            return (acx, ay), (bcx, by + bh + 2)
    else:
        if dx > 0:
            return (ax + aw, acy), (bx - 2, bcy)
        else:
            return (ax, acy), (bx + bw + 2, bcy)


def render_edge(e, nodes_by_id):
    a = nodes_by_id[e["from"]]
    b = nodes_by_id[e["to"]]
    (x1, y1), (x2, y2) = edge_endpoints(a, b)
    dash = ' stroke-dasharray="6 4"' if e.get("style") == "dashed" else ""
    line = (
        f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
        f'stroke="{EDGE_COLOR}" stroke-width="2" stroke-linecap="round"{dash} '
        f'marker-end="url(#arrow)"/>'
    )
    if e.get("label"):
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        w = max(40, len(e["label"]) * 7)
        line += (
            f'\n<rect x="{mx - w/2}" y="{my - 10}" width="{w}" height="18" fill="{BG}"/>'
            f'\n<text x="{mx}" y="{my + 3}" fill="#a1a1aa" font-size="12" '
            f'text-anchor="middle">{escape(e["label"])}</text>'
        )
    return line


def escape(s: str) -> str:
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def autosize(spec):
    max_x = 0
    max_y = 0
    for n in spec.get("nodes", []):
        x, y, w, h = node_box(n)
        max_x = max(max_x, x + w)
        max_y = max(max_y, y + h)
    for g in spec.get("groups", []):
        max_x = max(max_x, g["x"] + g["w"])
        max_y = max(max_y, g["y"] + g["h"])
    return max_x + 80, max_y + 80


def build(spec: dict) -> str:
    canvas = spec.get("canvas") or {}
    w, h = canvas.get("width"), canvas.get("height")
    if not w or not h:
        aw, ah = autosize(spec)
        w = w or max(1080, aw)
        h = h or ah

    nodes_by_id = {n["id"]: n for n in spec.get("nodes", [])}

    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" font-family="{FONT}">',
        f'  <title>{escape(spec.get("title", "Diagram"))}</title>',
        f'  <desc>{escape(spec.get("description", ""))}</desc>',
        f'  <rect width="100%" height="100%" fill="{BG}"/>',
        '  <defs>',
        '    <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" '
        'markerWidth="6" markerHeight="6" orient="auto-start-reverse">',
        f'      <path d="M 0 0 L 10 5 L 0 10 z" fill="{EDGE_COLOR}"/>',
        '    </marker>',
        '  </defs>',
    ]
    for g in spec.get("groups", []):
        out.append(render_group(g))
    for n in spec.get("nodes", []):
        out.append(render_node(n))
    for e in spec.get("edges", []):
        out.append(render_edge(e, nodes_by_id))
    out.append('</svg>')
    return "\n".join(out)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("spec", help="JSON spec file (or '-' for stdin)")
    p.add_argument("-o", "--output", default="-", help="Output SVG path (default: stdout)")
    args = p.parse_args()

    spec_text = sys.stdin.read() if args.spec == "-" else Path(args.spec).read_text()
    spec = json.loads(spec_text)
    svg = build(spec)
    if args.output == "-":
        sys.stdout.write(svg)
    else:
        Path(args.output).write_text(svg)
        print(f"Wrote {args.output}", file=sys.stderr)


if __name__ == "__main__":
    main()
