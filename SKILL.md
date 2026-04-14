---
name: svg-architecture-diagram
description: Produce polished, dark-themed architecture and flow diagrams as standalone .svg files. Use this skill whenever the user wants a system architecture diagram, a RAG/pipeline flowchart, a data flow diagram, a node-and-edge graph, or a sequence/interaction diagram — especially when they share a reference image, say "make a diagram like this," mention boxes with title+subtitle, dashed auxiliary arrows, color-coded categories, or grouped containers, or ask for a "clean/modern/dark" architecture view. Also trigger when the request is vague ("draw the system," "visualize the flow," "map this out") and the natural output is an SVG diagram rather than prose.
---

# SVG architecture diagrams (dark, category-coded)

This skill produces architecture and flow diagrams as standalone `.svg` files in a specific dark, minimal style. The style is opinionated on purpose: it looks good, reads well projected on a screen or pasted in a doc, and is fast to author because every choice (palette, radii, spacing, arrow weight) is pre-decided.

Before writing any SVG, read `references/style-guide.md` — it's the source of truth for colors, sizes, and spacing. Then skim `references/examples.md` for two complete worked diagrams you can adapt.

## When this is the right tool

Use this skill when the user wants any of:
- A system or service architecture picture (components + arrows).
- A RAG / retrieval / ML pipeline flowchart.
- A data flow or ETL diagram.
- A generic node-and-edge graph.
- A sequence or interaction diagram (actors on top, vertical time, arrows between lanes).

Prefer Mermaid or a dedicated charting library if the user explicitly asks for them, or if the "diagram" is really a bar/line chart. This skill is for hand-crafted, presentation-quality node-edge views.

## Design philosophy (why this style)

Reading a diagram is basically two jobs: *find the pieces* and *follow the arrows*. The style is tuned for both:

- **Dark background, category-colored fills.** Color encodes *kind* of component (compute vs. storage vs. retrieval vs. ranking), not identity. That lets a reader scan by role. Keep the palette small — a new color should mean a genuinely new category.
- **Title + subtitle on every node.** The title is what the thing *is* ("Azure AI Search"); the subtitle is what it *does here* ("BM25 lexical, Dutch"). Two lines beats one crammed line, and beats a separate legend.
- **Solid arrows = request flow, dashed = auxiliary.** Caches, memory, logging, and other side channels get dashed arrows so the main path stays easy to trace.
- **Container groups, not free-floating boxes.** When 2+ nodes belong to one system (e.g., "Azure AI Search"), draw a rounded container around them with a label at the top. This replaces a lot of arrows and labels.

If you remember nothing else: *color = role, subtitle = detail, dashed = side channel, container = grouping.*

## Workflow

1. **Plan on paper first.** Before any SVG, list the nodes with their category and subtitle, list the edges (solid vs. dashed), and list any container groups. Sketching this as plain text first prevents midway rewrites.
2. **Pick the canvas size.** Use the sizing rules in `references/style-guide.md` (#canvas-sizing). Vertical flows are the default — width 1440, height grows with node count.
3. **Generate the SVG.** Two paths:
   - **By hand** (preferred for one-offs and when the user wants specific tweaks): copy the skeleton from `references/svg-primitives.md` and fill in nodes, edges, and groups. It is clearer to write the SVG directly than to build a toolchain for a single diagram.
   - **With the helper script** (`scripts/build_diagram.py`): useful when the user gives you a structured spec or when you'll regenerate often. It takes a JSON description of nodes/edges/groups and emits the SVG with consistent styling. Run `python scripts/build_diagram.py --help` for usage.
4. **Save to the outputs folder.** Write the final `.svg` into `/sessions/.../mnt/outputs/` and share a `computer://` link.
5. **Verify visually.** If possible, render the SVG (open in browser, or convert to PNG with `rsvg-convert` / `cairosvg`) and check: arrows hit box edges cleanly, no text overflow, categories make sense, dashed vs. solid is consistent.

## Node anatomy

Every node is a rounded rectangle with one or two lines of centered text:

```
┌──────────────────────────────┐
│         Title (bold)         │   ← 18px, white
│      subtitle (smaller)      │   ← 13px, category-tinted
└──────────────────────────────┘
```

- Width: default 260px; widen to 320 if the title is long. Height: 72 for title+subtitle, 52 for title only.
- Corner radius: 12px.
- Fill + subtitle color come from the category palette in `references/style-guide.md`.
- Title is always white (`#f4f4f5`). Subtitle is the category's accent color at ~70% saturation.

Do not add drop shadows, gradients, or icons. The style stays clean by staying flat.

## Edges

- Arrow weight: `stroke-width="2"`, color `#71717a`.
- Solid for the primary request/response path. Dashed (`stroke-dasharray="6 4"`) for caches, memory, logging, metrics, or any side channel.
- Arrowheads: use a single `<marker>` definition at the top of the SVG and reference it with `marker-end`. The skeleton in `references/svg-primitives.md` has a drop-in marker.
- Route arrows orthogonally when crossing is unavoidable; route straight down or straight across otherwise. Never diagonal unless the diagram is explicitly radial.

## Containers (groups)

A container is a larger rounded rectangle behind a set of nodes, with the group's name at the top-inside. Use fill `#27272a` at ~60% opacity, stroke `#3f3f46`, corner radius 16px. Put the group label at x = (container_x + 24), y = (container_y + 32), in white, 16px, medium weight. See the "Azure AI Search" container in `references/examples.md`.

Don't nest containers more than one level deep — it starts to look like a Russian doll and stops aiding comprehension.

## Sequence diagrams

For interaction diagrams, the same palette applies but the layout changes: actors as rounded pills across the top, vertical dashed "lifelines" descending from each, and arrows between lifelines labeled with the message. `references/examples.md` has a full example.

## Output conventions

- One SVG file per diagram. No inline PNG, no base64.
- Embed fonts via `font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Inter, system-ui, sans-serif"` so it looks right on any machine without font files.
- Set `viewBox` so the SVG scales; don't hardcode width/height on the `<svg>` root beyond the viewBox.
- Include a brief `<title>` and `<desc>` for accessibility.

## Common mistakes to avoid

- **Too many colors.** If you're reaching for a sixth hue, merge categories instead.
- **Subtitle repeats the title.** "Azure AI Search / Azure search service" is noise. Use the subtitle for the *role in this system*.
- **Arrows that don't touch the box.** Either extend the line or shorten it — a 3px gap looks like a bug.
- **Forgetting the container.** If three nodes share a system, one container saves three arrows and three labels.
- **Fixed-width canvas that clips.** Recompute width/height after placing nodes; don't trust your initial estimate.

## Reference files

- `references/style-guide.md` — palette, spacing, typography, canvas sizing rules. Read before writing SVG.
- `references/svg-primitives.md` — copy-paste SVG skeleton, node template, arrow marker, container template.
- `references/examples.md` — two complete examples (RAG architecture and a sequence diagram) with annotated source.
- `scripts/build_diagram.py` — optional helper that turns a JSON spec into an SVG. Run with `--help`.
