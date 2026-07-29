---
inclusion: fileMatch
fileMatchPattern: "app/frontend/**"
---

# Frontend Standards — HTML, Tailwind CSS v4, Vanilla JS (2026)

## HTML (Jinja2 Templates)

- Semantic HTML5: `<nav>`, `<main>`, `<section>`, `<article>`, `<aside>`, `<header>`, `<footer>`.
- All templates extend `base.html` via `{% extends %}` and `{% block %}`.
- Reusable fragments in `components/` — include with `{% include 'components/name.html' %}`.
- Accessibility: all `<img>` have `alt`, all `<input>` have associated `<label>`, all interactive elements are keyboard-accessible, proper ARIA roles where needed.
- No inline styles. No inline `<script>`. Styling via Tailwind classes, JS in separate `.js` files.
- Use `data-*` attributes for JS hooks (`data-action="scout"`, `data-post-id="123"`). Never select elements by styling classes.
- IDs for unique page landmarks only. `data-*` or specific classes for repeated elements.
- Use `<template>` elements for client-side rendering patterns (clone and populate).

## Tailwind CSS v4 (CSS-First Configuration)

### Configuration — NO JavaScript config file
Tailwind v4 uses CSS-first configuration with `@theme` in your main CSS file:

```css
@import "tailwindcss";

@theme {
  --color-surface: oklch(0.15 0.01 260);
  --color-surface-alt: oklch(0.20 0.01 260);
  --color-text-primary: oklch(0.95 0 0);
  --color-text-muted: oklch(0.65 0 0);
  --color-accent: oklch(0.65 0.2 265);
  --color-accent-hover: oklch(0.72 0.2 265);
  --color-border: oklch(0.30 0.01 260);
  --color-success: oklch(0.70 0.15 145);
  --color-warning: oklch(0.75 0.15 85);
  --color-danger: oklch(0.65 0.2 25);

  --font-sans: "Inter", system-ui, sans-serif;
  --font-mono: "JetBrains Mono", monospace;

  --shadow-card: 0 4px 12px oklch(0 0 0 / 0.2);
}
```

### Rules
- Define ALL design tokens in `@theme`. Use those token-based utilities (`bg-surface`, `text-muted`, `border-border`).
- Never hardcode hex/rgb values in templates. Use the `@theme` tokens.
- OKLCH color space for all custom colors (more perceptually uniform, 2026 standard).
- Arbitrary values (`top-[117px]`) are escape hatches only — not a design system. If a value repeats, promote to `@theme`.
- No `@apply` unless extracting a base style for third-party components. Utility classes in HTML is the pattern.
- No `tailwind.config.js` — Tailwind v4 does not use JavaScript config. All config is CSS-first.
- Dark mode: use `prefers-color-scheme` media query by default. If supporting toggle, use `class` strategy with `@custom-variant`.
- Responsive: mobile-first with `sm:`, `md:`, `lg:` breakpoints.
- No `!important`. If specificity fights, the structure is wrong.

### Anti-Patterns (Tailwind v4 specific)
- ❌ `tailwind.config.js` — does not exist in v4
- ❌ `@tailwind base; @tailwind components; @tailwind utilities;` — v4 uses `@import "tailwindcss";`
- ❌ `bg-gradient-to-r` — v4 uses `bg-linear-to-r`
- ❌ Arbitrary values everywhere — promote to `@theme` tokens
- ❌ `@apply` for everything — defeats the purpose of utility-first

## Vanilla JavaScript (ES2022+ Modules)

### Architecture
- Use `<script type="module">` on script tags. Use `import`/`export`.
- Each JS file is a self-contained module with explicit exports. No global variables.
- One file per concern: `app.js` (core), `chat.js` (chat UI), `editor.js` (markdown), `calendar.js` (calendar).
- If a file exceeds ~200 lines, split into focused sub-modules.

### DOM Manipulation
- Select with `document.querySelector()` / `querySelectorAll()`. Prefer `[data-*]` selectors.
- Event delegation: attach listeners to parent containers, filter by `event.target` — especially for dynamic content.
- Batch DOM writes. Use `DocumentFragment` for inserting multiple elements.
- Use `insertAdjacentHTML('beforeend', html)` for templated HTML (only with sanitized/escaped data).
- Never use `innerHTML` with user-provided content (XSS risk). Use `textContent` for plain text.
- Use `<template>` + `cloneNode(true)` for repeating structures.
- Use `requestAnimationFrame` for visual updates that need to sync with paint.

### Fetch & Async
- `fetch()` for all API calls. Always check `response.ok` before parsing.
- `async/await` everywhere. No `.then()` chains.
- SSE (Server-Sent Events) via `EventSource` for streaming adapter responses.
- Wrap fetch in a utility function with error handling (defined in `app.js`):

```javascript
export async function api(path, options = {}) {
  const res = await fetch(`/api${path}`, {
    headers: { 'Content-Type': 'application/json', ...options.headers },
    ...options,
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(err.detail || 'Request failed');
  }
  return res.json();
}
```

### Patterns
- Debounce search/filter inputs (300ms).
- Use `AbortController` to cancel in-flight requests when the user navigates away.
- Lazy-load heavy content (images below fold, chart libraries loaded on demand).
- Use `CustomEvent` for component-to-component communication within a page.
- Store temporary UI state in `sessionStorage`. Persistent preferences in the backend config.

### Anti-Patterns
- ❌ jQuery or any DOM helper library
- ❌ Global variables or functions on `window`
- ❌ `var` — use `const` (default) or `let` (when reassignment needed)
- ❌ `document.write()`
- ❌ Sync XHR
- ❌ `.then()` chains (use `async/await`)
- ❌ `innerHTML` with unsanitized content

## Performance

- No external CDN dependencies in production. All assets local.
- Tailwind CSS purges unused utilities automatically (production build).
- Minify JS in production builds.
- Use `loading="lazy"` on images.
- Prefetch next-likely pages with `<link rel="prefetch">` for navigation targets.
