---
inclusion: fileMatch
fileMatchPattern: "app/frontend/**"
---

# Frontend — HTML, Tailwind CSS v4, Vanilla JS

Write frontend code like Stripe's dashboard, Linear's UI, or Cal.com: minimal, fast, readable. No cleverness.

## Single Responsibility

- One JS file = one concern (`chat.js` handles chat, `editor.js` handles editing — never both)
- One HTML template = one page
- One component partial = one reusable piece
- One function = one action (fetch data OR render DOM — not both in the same function)

**The test:** Can you name the file/function in 2-3 words that fully describe it? If not, it does too much.

## HTML — Semantic, Accessible, Clean

```html
<!-- Good — semantic, readable -->
<main class="flex-1 p-6">
  <section data-page="library">
    <header class="mb-6">
      <h1 class="text-xl font-semibold text-primary">Library</h1>
    </header>
    <article class="post-card" data-post-id="{{ post.id }}">
      ...
    </article>
  </section>
</main>

<!-- Bad — div soup -->
<div class="main">
  <div class="section">
    <div class="header">
      <div class="title">Library</div>
    </div>
  </div>
</div>
```

Rules:
- Semantic elements: `<nav>`, `<main>`, `<section>`, `<article>`, `<aside>`, `<header>`, `<footer>`
- Every `<img>` has `alt`. Every `<input>` has `<label>`. Every button is keyboard-accessible.
- `data-*` attributes for JS hooks. Never select by styling classes.
- No inline styles. No inline scripts.

## Tailwind CSS v4 — CSS-First, Token-Based

### Configuration lives in CSS (not JavaScript)

```css
/* app.css — the ONLY place design tokens are defined */
@import "tailwindcss";

@theme {
  /* Colors — OKLCH for perceptual uniformity */
  --color-surface: oklch(0.13 0.01 260);
  --color-surface-raised: oklch(0.18 0.01 260);
  --color-text-primary: oklch(0.93 0 0);
  --color-text-secondary: oklch(0.65 0 0);
  --color-accent: oklch(0.65 0.19 265);
  --color-border: oklch(0.28 0.01 260);
  --color-status-draft: oklch(0.75 0.15 85);
  --color-status-approved: oklch(0.65 0.15 250);
  --color-status-published: oklch(0.70 0.15 145);

  /* Typography */
  --font-sans: "Inter", system-ui, sans-serif;
  --font-mono: "JetBrains Mono", monospace;

  /* Shadows */
  --shadow-card: 0 2px 8px oklch(0 0 0 / 0.25);
}
```

### Rules
- **No `tailwind.config.js`** — Tailwind v4 is CSS-first. All config in `@theme`.
- **No `@tailwind base/components/utilities`** — v4 uses `@import "tailwindcss"`.
- **No `bg-gradient-to-r`** — v4 renamed to `bg-linear-to-r`.
- Token-first: every color/spacing/shadow used in templates comes from `@theme`. Zero hardcoded values.
- If a value repeats twice → it's a token. Promote to `@theme`.
- Arbitrary values (`top-[117px]`) are last-resort escape hatches, never a pattern.
- No `@apply` (defeats utility-first purpose). Extract a Jinja2 component instead.
- No `!important`.

### How to think about Tailwind
```html
<!-- Each class does ONE thing. Reading left-to-right tells you the full story. -->
<button class="rounded-lg bg-accent px-4 py-2 text-sm font-medium text-white hover:bg-accent-hover transition-colors">
  Scout Now
</button>
```

## Vanilla JavaScript — ES Modules, No Framework

### Architecture
```javascript
// Every file exports focused, named functions
// app.js — core utilities
export async function api(path, options = {}) { ... }
export function debounce(fn, ms) { ... }
export function $(selector) { return document.querySelector(selector); }
export function $$(selector) { return document.querySelectorAll(selector); }

// chat.js — only chat concerns
import { api, $ } from './app.js';

export function initChat(container) { ... }
function renderMessage(message) { ... }
function handleSend(input) { ... }
```

### DOM Rules (how Linear/Stripe do it)
```javascript
// 1. Select with data attributes
const postCards = document.querySelectorAll('[data-post-id]');

// 2. Event delegation — one listener on the parent
document.querySelector('[data-post-list]').addEventListener('click', (e) => {
  const card = e.target.closest('[data-post-id]');
  if (!card) return;
  openEditor(card.dataset.postId);
});

// 3. Create elements safely (no innerHTML with user data)
function createPostCard(post) {
  const tpl = document.querySelector('#post-card-template');
  const card = tpl.content.cloneNode(true);
  card.querySelector('[data-title]').textContent = post.title;
  card.querySelector('[data-status]').textContent = post.status;
  return card;
}

// 4. Batch DOM updates
function renderPosts(posts) {
  const fragment = document.createDocumentFragment();
  posts.forEach(post => fragment.appendChild(createPostCard(post)));
  container.replaceChildren(fragment);
}
```

### Fetch Pattern
```javascript
// Single fetch utility — used everywhere
export async function api(path, options = {}) {
  const res = await fetch(`/api${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(err.detail || `Request failed: ${res.status}`);
  }
  return res.json();
}

// Usage — clean and obvious
const posts = await api('/library/posts?status=draft');
```

### SSE (Streaming from Adapter)
```javascript
function streamResponse(sessionId, onChunk, onDone) {
  const source = new EventSource(`/api/content/stream/${sessionId}`);
  source.onmessage = (e) => onChunk(e.data);
  source.onerror = () => { source.close(); onDone(); };
  return source;
}
```

### Rules
- `const` by default. `let` only when reassignment needed. Never `var`.
- `async/await` everywhere. No `.then()` chains.
- No global state. Module-scoped variables are fine.
- Functions under 20 lines. Extract helpers.
- Use `AbortController` for cancellable requests.
- Debounce user inputs (search: 300ms, resize: 150ms).
- No jQuery. No lodash. No utility libraries. Browser APIs are enough.

## Code Review Checklist (Frontend)

- [ ] Semantic HTML (no div soup)
- [ ] All colors/spacing from `@theme` tokens (no hardcoded values)
- [ ] JS selects via `data-*` attributes (not styling classes)
- [ ] Event delegation for dynamic content
- [ ] No `innerHTML` with user data
- [ ] All fetch calls use the shared `api()` utility
- [ ] Functions under 20 lines
- [ ] One concern per file
- [ ] Accessible (keyboard-navigable, proper labels, contrast)
