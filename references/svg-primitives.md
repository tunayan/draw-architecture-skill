# SVG primitives — copy-paste building blocks

All snippets assume the palette in `style-guide.md`. Substitute category colors as appropriate.

## Root skeleton

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 1600"
     font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Inter, system-ui, sans-serif">
  <title>System architecture</title>
  <desc>Short accessibility description of what the diagram shows.</desc>

  <!-- Background -->
  <rect width="100%" height="100%" fill="#0a0a0a"/>

  <!-- Arrow marker (define once, reuse) -->
  <defs>
    <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5"
            markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#71717a"/>
    </marker>
  </defs>

  <!-- ... nodes, groups, edges here ... -->
</svg>
```

## Node (title + subtitle)

Parameters: `x, y` (top-left), `w=260`, `h=72`, `fill`, `accent`, `title`, `subtitle`.

```xml
<g transform="translate(X, Y)">
  <rect width="260" height="72" rx="12" ry="12"
        fill="#1e3a5f" stroke="#2a5082" stroke-width="1"/>
  <text x="130" y="32" fill="#f4f4f5" font-size="18" font-weight="600"
        text-anchor="middle">Title</text>
  <text x="130" y="54" fill="#93c5fd" font-size="13" font-weight="400"
        text-anchor="middle">subtitle</text>
</g>
```

## Title-only node

```xml
<g transform="translate(X, Y)">
  <rect width="260" height="52" rx="12" ry="12" fill="#3f3f46" stroke="#52525b" stroke-width="1"/>
  <text x="130" y="32" fill="#f4f4f5" font-size="18" font-weight="600" text-anchor="middle">User query</text>
</g>
```

## Container (group box with label)

```xml
<g>
  <rect x="X" y="Y" width="W" height="H" rx="16" ry="16"
        fill="#18181b" fill-opacity="0.6" stroke="#3f3f46" stroke-width="1.5"/>
  <text x="X+24" y="Y+32" fill="#f4f4f5" font-size="16" font-weight="500">Group label</text>
  <!-- place child nodes at x > X+24, y > Y+56 -->
</g>
```

## Solid edge

```xml
<line x1="X1" y1="Y1" x2="X2" y2="Y2"
      stroke="#71717a" stroke-width="2" stroke-linecap="round"
      marker-end="url(#arrow)"/>
```

## Dashed edge (side channel)

```xml
<line x1="X1" y1="Y1" x2="X2" y2="Y2"
      stroke="#71717a" stroke-width="2" stroke-linecap="round"
      stroke-dasharray="6 4" marker-end="url(#arrow)"/>
```

## Edge with label

```xml
<g>
  <line x1="X1" y1="Y1" x2="X2" y2="Y2"
        stroke="#71717a" stroke-width="2" marker-end="url(#arrow)"/>
  <rect x="MX-28" y="MY-10" width="56" height="18" fill="#0a0a0a"/>
  <text x="MX" y="MY+3" fill="#a1a1aa" font-size="12" text-anchor="middle">label</text>
</g>
```
(MX, MY = midpoint of the line)

## Orthogonal (L-shaped) edge

When a source and target aren't vertically aligned, use a `<polyline>` with a single 90° bend rather than a diagonal:

```xml
<polyline points="X1,Y1 X1,YM X2,YM X2,Y2" fill="none"
          stroke="#71717a" stroke-width="2" marker-end="url(#arrow)"/>
```
Choose `YM` as the midpoint between Y1 and Y2.

## Hit the box, not the middle

When connecting node A (bottom) to node B (top) in a vertical flow, set:
- `x1 = A.centerX`, `y1 = A.y + A.height` (or `+ A.height + 2` for a tiny visual margin)
- `x2 = B.centerX`, `y2 = B.y - 2` (marker takes the last few px)

Avoid arrows that start or end *inside* a box — they look like bugs.
