# Style guide

Source of truth for colors, sizes, and spacing. The whole skill depends on these being stable — do not tweak them per-diagram unless the user explicitly asks.

## Palette

Background: `#0a0a0a` (near-black; pure `#000` is too harsh in presentations).

### Category colors

Each category has three values: fill (for the node background), stroke (subtle border, optional), and accent (for subtitle text and, if desired, group label).

| Category | Use for | Fill | Stroke | Accent (subtitle) |
|---|---|---|---|---|
| `neutral` | Raw inputs/outputs, intermediate IDs, generic labels | `#3f3f46` | `#52525b` | `#d4d4d8` |
| `compute` | Model calls, orchestration, query rewriting, LLMs | `#1e3a5f` | `#2a5082` | `#93c5fd` |
| `retrieval` | BM25, vector search, any index lookup | `#14532d` | `#1f6b3f` | `#86efac` |
| `rank` | RRF, fusion, rerankers, scorers | `#3b1f6b` | `#553090` | `#c4b5fd` |
| `storage` | Postgres, Redis, S3, any persistent store | `#5c2e1f` | `#7a3d2a` | `#fca5a5` |
| `external` | Third-party APIs, user-facing surfaces | `#4a2a5c` | `#6b3e82` | `#e9d5ff` |

Text colors: title always `#f4f4f5`, subtitle uses the accent from the row above.

If you need a seventh category, you're probably over-classifying — merge two.

### Container (group) styling

- Fill: `#18181b` at opacity `0.6`
- Stroke: `#3f3f46`
- Stroke width: `1.5`
- Corner radius: `16`
- Label: white `#f4f4f5`, 16px, font-weight 500, positioned 24px from left edge, 32px from top edge.

## Typography

Font stack (embed directly on text elements or on the root `<svg>`):

```
font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Inter, system-ui, sans-serif"
```

Sizes:

| Element | Size | Weight | Color |
|---|---|---|---|
| Node title | 18px | 600 | `#f4f4f5` |
| Node subtitle | 13px | 400 | accent |
| Group label | 16px | 500 | `#f4f4f5` |
| Edge label | 12px | 400 | `#a1a1aa` |
| Diagram title (optional, top of canvas) | 24px | 600 | `#f4f4f5` |

## Node geometry

- Default size: `width=260, height=72` (title + subtitle). Use `height=52` for title-only nodes.
- Corner radius: `rx=12, ry=12`.
- Title vertical position: `y = box_y + 32` (baseline), text-anchor `middle`, x at box center.
- Subtitle vertical position: `y = box_y + 54`.
- If the title exceeds ~22 characters, widen the box to 320px rather than shrinking the font.

## Edges

- Stroke: `#71717a`, width `2`, linecap `round`.
- Solid: primary data/request flow.
- Dashed: `stroke-dasharray="6 4"` for caches, memory, logs, metrics, any side channel.
- Arrowhead marker (define once, reuse):

```xml
<defs>
  <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5"
          markerWidth="6" markerHeight="6" orient="auto-start-reverse">
    <path d="M 0 0 L 10 5 L 0 10 z" fill="#71717a"/>
  </marker>
</defs>
```

- Attach with `marker-end="url(#arrow)"`.
- Optional edge label: place a `<text>` at the midpoint with a small `<rect>` background (fill `#0a0a0a`) so it reads over the line.

## Canvas sizing

Default vertical flow:
- Width: `1440` (fits a typical slide). Use `1080` if only 1-2 columns of nodes; `1800` for wide sequence diagrams.
- Height: start at `padding_top (80) + N * 140 + padding_bottom (80)` where N is the number of vertical "tiers." Add an extra `120` per container you place.
- Horizontal padding inside the viewBox: at least 120px on each side so nothing touches the edge.
- Vertical gap between nodes in the main flow: `120px` (gives room for arrow + label).
- Horizontal gap between sibling nodes inside a container: `60px`.

After placing everything, recompute the viewBox to `min-x min-y width height` that actually contains all elements plus 40px margin. Don't trust the initial estimate.

## Color-coding heuristic

When you're unsure which category a node belongs to, ask: *what does this thing fundamentally do?*

- It takes a query and produces structured info → `compute`
- It stores bytes for later retrieval → `storage`
- It performs a similarity/lexical lookup → `retrieval`
- It takes candidates and reorders them → `rank`
- It's a user or a third party we don't own → `external`
- It's literally just a piece of data flowing through → `neutral`

If two interpretations are equally valid, pick the one that gives you more color diversity across the diagram — that's what makes the picture readable.
