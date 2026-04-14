# Worked examples

Two complete diagrams you can adapt. Each uses only the primitives from `svg-primitives.md` and the palette from `style-guide.md`.

## Example 1 — RAG retrieval pipeline

Canonical architecture diagram: user query → query understanding (with cache side-channel) → hybrid retrieval inside a container → reranker → hydrate from Postgres → grounded LLM (with session-memory side-channel).

The important things this example demonstrates:
- `neutral` nodes for data artifacts ("User query", "Top-10 recipe IDs")
- `compute` for the LLM call and query rewriter
- `retrieval` for BM25 + vector lookup
- `rank` for RRF fusion and the semantic reranker
- `storage` (brown-red) for Redis and Postgres
- Dashed edges to/from caches and memory
- A container around the two retrieval variants so they read as one subsystem

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 1600"
     font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Inter, system-ui, sans-serif">
  <title>RAG retrieval architecture</title>
  <desc>Query flows through understanding, hybrid retrieval, reranking, hydration, and a grounded LLM, with Redis side-channels for caching and session memory.</desc>

  <rect width="100%" height="100%" fill="#0a0a0a"/>

  <defs>
    <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5"
            markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#71717a"/>
    </marker>
  </defs>

  <!-- User query (neutral, title-only) -->
  <g transform="translate(590,80)">
    <rect width="260" height="52" rx="12" ry="12" fill="#3f3f46" stroke="#52525b"/>
    <text x="130" y="32" fill="#f4f4f5" font-size="18" font-weight="600" text-anchor="middle">User query</text>
  </g>

  <!-- Query understanding (compute) -->
  <g transform="translate(590,200)">
    <rect width="260" height="72" rx="12" ry="12" fill="#1e3a5f" stroke="#2a5082"/>
    <text x="130" y="32" fill="#f4f4f5" font-size="18" font-weight="600" text-anchor="middle">Query understanding</text>
    <text x="130" y="54" fill="#93c5fd" font-size="13" text-anchor="middle">Extract filters and rewrite</text>
  </g>

  <!-- Redis / Semantic cache (storage, dashed side-channel) -->
  <g transform="translate(200,200)">
    <rect width="240" height="72" rx="12" ry="12" fill="#5c2e1f" stroke="#7a3d2a"/>
    <text x="120" y="32" fill="#f4f4f5" font-size="18" font-weight="600" text-anchor="middle">Redis</text>
    <text x="120" y="54" fill="#fca5a5" font-size="13" text-anchor="middle">Semantic cache</text>
  </g>

  <!-- Edges: user → QU, cache ⇠⇢ QU -->
  <line x1="720" y1="132" x2="720" y2="198" stroke="#71717a" stroke-width="2" marker-end="url(#arrow)"/>
  <line x1="440" y1="236" x2="588" y2="236" stroke="#71717a" stroke-width="2" stroke-dasharray="6 4" marker-end="url(#arrow)"/>

  <!-- Azure AI Search container -->
  <g>
    <rect x="460" y="340" width="520" height="460" rx="16" ry="16"
          fill="#18181b" fill-opacity="0.6" stroke="#3f3f46" stroke-width="1.5"/>
    <text x="484" y="372" fill="#f4f4f5" font-size="16" font-weight="500">Azure AI Search</text>

    <!-- BM25 (retrieval) -->
    <g transform="translate(490,400)">
      <rect width="220" height="72" rx="12" ry="12" fill="#14532d" stroke="#1f6b3f"/>
      <text x="110" y="32" fill="#f4f4f5" font-size="18" font-weight="600" text-anchor="middle">BM25</text>
      <text x="110" y="54" fill="#86efac" font-size="13" text-anchor="middle">Lexical, Dutch</text>
    </g>

    <!-- Vectors (retrieval) -->
    <g transform="translate(730,400)">
      <rect width="220" height="72" rx="12" ry="12" fill="#14532d" stroke="#1f6b3f"/>
      <text x="110" y="32" fill="#f4f4f5" font-size="18" font-weight="600" text-anchor="middle">Vectors</text>
      <text x="110" y="54" fill="#86efac" font-size="13" text-anchor="middle">HNSW cosine</text>
    </g>

    <!-- RRF fusion (rank, title-only) -->
    <g transform="translate(590,560)">
      <rect width="260" height="52" rx="12" ry="12" fill="#3b1f6b" stroke="#553090"/>
      <text x="130" y="32" fill="#f4f4f5" font-size="18" font-weight="600" text-anchor="middle">RRF fusion</text>
    </g>

    <!-- Semantic reranker (rank, title-only) -->
    <g transform="translate(590,660)">
      <rect width="260" height="52" rx="12" ry="12" fill="#3b1f6b" stroke="#553090"/>
      <text x="130" y="32" fill="#f4f4f5" font-size="18" font-weight="600" text-anchor="middle">Semantic reranker</text>
    </g>

    <!-- Edges inside container: BM25 → RRF, Vectors → RRF, RRF → Reranker -->
    <line x1="600" y1="472" x2="680" y2="558" stroke="#71717a" stroke-width="2" marker-end="url(#arrow)"/>
    <line x1="840" y1="472" x2="760" y2="558" stroke="#71717a" stroke-width="2" marker-end="url(#arrow)"/>
    <line x1="720" y1="612" x2="720" y2="658" stroke="#71717a" stroke-width="2" marker-end="url(#arrow)"/>
  </g>

  <!-- QU → Search container -->
  <line x1="720" y1="272" x2="720" y2="338" stroke="#71717a" stroke-width="2" marker-end="url(#arrow)"/>

  <!-- Top-10 recipe IDs (neutral) -->
  <g transform="translate(590,860)">
    <rect width="260" height="52" rx="12" ry="12" fill="#3f3f46" stroke="#52525b"/>
    <text x="130" y="32" fill="#f4f4f5" font-size="18" font-weight="600" text-anchor="middle">Top-10 recipe IDs</text>
  </g>

  <!-- Reranker → Top-10 -->
  <line x1="720" y1="712" x2="720" y2="858" stroke="#71717a" stroke-width="2" marker-end="url(#arrow)"/>

  <!-- Hydrate from Postgres (storage) -->
  <g transform="translate(590,960)">
    <rect width="260" height="72" rx="12" ry="12" fill="#5c2e1f" stroke="#7a3d2a"/>
    <text x="130" y="32" fill="#f4f4f5" font-size="18" font-weight="600" text-anchor="middle">Hydrate from Postgres</text>
    <text x="130" y="54" fill="#fca5a5" font-size="13" text-anchor="middle">Full recipe objects</text>
  </g>

  <line x1="720" y1="912" x2="720" y2="958" stroke="#71717a" stroke-width="2" marker-end="url(#arrow)"/>

  <!-- Grounded LLM (compute) -->
  <g transform="translate(590,1100)">
    <rect width="260" height="72" rx="12" ry="12" fill="#1e3a5f" stroke="#2a5082"/>
    <text x="130" y="32" fill="#f4f4f5" font-size="18" font-weight="600" text-anchor="middle">Grounded LLM</text>
    <text x="130" y="54" fill="#93c5fd" font-size="13" text-anchor="middle">GPT-4o with citations</text>
  </g>

  <line x1="720" y1="1032" x2="720" y2="1098" stroke="#71717a" stroke-width="2" marker-end="url(#arrow)"/>

  <!-- Redis / Session memory (storage, side channel to LLM) -->
  <g transform="translate(1000,1100)">
    <rect width="240" height="72" rx="12" ry="12" fill="#5c2e1f" stroke="#7a3d2a"/>
    <text x="120" y="32" fill="#f4f4f5" font-size="18" font-weight="600" text-anchor="middle">Redis</text>
    <text x="120" y="54" fill="#fca5a5" font-size="13" text-anchor="middle">Session memory</text>
  </g>

  <line x1="1000" y1="1136" x2="852" y2="1136" stroke="#71717a" stroke-width="2" stroke-dasharray="6 4" marker-end="url(#arrow)"/>
</svg>
```

## Example 2 — Sequence diagram

Actors across the top, vertical dashed lifelines descending, arrows between lifelines labeled with the message. Same palette — actors as `compute`/`external`, self-loops allowed.

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 700"
     font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Inter, system-ui, sans-serif">
  <title>Login sequence</title>
  <desc>Client requests a session, server validates, DB returns user record, server responds with token.</desc>

  <rect width="100%" height="100%" fill="#0a0a0a"/>

  <defs>
    <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5"
            markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#71717a"/>
    </marker>
  </defs>

  <!-- Actor pills -->
  <g transform="translate(100,60)">
    <rect width="200" height="52" rx="26" ry="26" fill="#4a2a5c" stroke="#6b3e82"/>
    <text x="100" y="32" fill="#f4f4f5" font-size="18" font-weight="600" text-anchor="middle">Client</text>
  </g>
  <g transform="translate(500,60)">
    <rect width="200" height="52" rx="26" ry="26" fill="#1e3a5f" stroke="#2a5082"/>
    <text x="100" y="32" fill="#f4f4f5" font-size="18" font-weight="600" text-anchor="middle">Auth service</text>
  </g>
  <g transform="translate(900,60)">
    <rect width="200" height="52" rx="26" ry="26" fill="#5c2e1f" stroke="#7a3d2a"/>
    <text x="100" y="32" fill="#f4f4f5" font-size="18" font-weight="600" text-anchor="middle">User DB</text>
  </g>

  <!-- Lifelines (dashed, category-accented) -->
  <line x1="200" y1="112" x2="200" y2="660" stroke="#52525b" stroke-width="1" stroke-dasharray="4 6"/>
  <line x1="600" y1="112" x2="600" y2="660" stroke="#52525b" stroke-width="1" stroke-dasharray="4 6"/>
  <line x1="1000" y1="112" x2="1000" y2="660" stroke="#52525b" stroke-width="1" stroke-dasharray="4 6"/>

  <!-- Messages -->
  <g>
    <line x1="200" y1="180" x2="598" y2="180" stroke="#71717a" stroke-width="2" marker-end="url(#arrow)"/>
    <text x="399" y="172" fill="#a1a1aa" font-size="13" text-anchor="middle">POST /login {email, password}</text>
  </g>
  <g>
    <line x1="600" y1="260" x2="998" y2="260" stroke="#71717a" stroke-width="2" marker-end="url(#arrow)"/>
    <text x="799" y="252" fill="#a1a1aa" font-size="13" text-anchor="middle">SELECT user WHERE email=?</text>
  </g>
  <g>
    <line x1="1000" y1="340" x2="602" y2="340" stroke="#71717a" stroke-width="2" marker-end="url(#arrow)"/>
    <text x="799" y="332" fill="#a1a1aa" font-size="13" text-anchor="middle">user row (hashed pw)</text>
  </g>
  <g>
    <line x1="600" y1="420" x2="202" y2="420" stroke="#71717a" stroke-width="2" marker-end="url(#arrow)"/>
    <text x="399" y="412" fill="#a1a1aa" font-size="13" text-anchor="middle">200 OK {jwt}</text>
  </g>
</svg>
```

## Adapting these

- Change the canvas `viewBox` to fit your node count (see `style-guide.md` #canvas-sizing).
- Swap category colors per node based on what each component *does*, not what it's named.
- When in doubt about layout, sketch the node list + edge list as plain text before writing SVG.
