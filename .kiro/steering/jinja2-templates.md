---
inclusion: fileMatch
fileMatchPattern: "app/frontend/templates/**/*.html"
---

# Jinja2 Templating Standards

## Template Hierarchy

```
base.html                    ← App shell (sidebar, topbar, scripts, styles)
├── content.html             ← {% extends "base.html" %}
├── library.html             ← {% extends "base.html" %}
├── calendar.html            ← {% extends "base.html" %}
└── ...

components/
├── sidebar.html             ← {% include "components/sidebar.html" %}
├── post-card.html           ← {% include "components/post-card.html" %}
├── chat-bubble.html
├── command-bar.html
└── notification.html

onboarding.html              ← Standalone (no extends, full-page)
```

## Blocks (defined in base.html)

```html
{% block title %}Page Title{% endblock %}
{% block content %}Main page content{% endblock %}
{% block scripts %}Page-specific JS{% endblock %}
```

## Conventions

- Use `{% block %}` for page-specific content. Don't override base layout blocks.
- Use `{% include %}` for reusable components. Pass context via `{% include "x.html" with context %}` or set variables before include.
- Use `{% macro %}` only for truly parameterized fragments (like a button with variants). Prefer `{% include %}` for composition.
- Whitespace control: use `{%- -%}` and `{{- -}}` when whitespace matters (inside inline elements).
- Comments: `{# This is a Jinja2 comment — not rendered to HTML #}`.

## Variable Naming in Templates

- Variables passed from FastAPI: `snake_case` (e.g., `active_modules`, `post_list`, `niche_config`).
- Loop variables: descriptive (`for post in posts`, not `for p in posts`).
- Boolean context: prefix with `is_` or `has_` (e.g., `is_onboarded`, `has_analytics`).

## Conditional Rendering (dynamic navigation)

```html
{# Only show nav items for active features #}
{% if has_images_module %}
  <a href="/images" class="...">Images</a>
{% endif %}
```

The app passes feature flags to templates based on what exists in the user's config. Templates render conditionally — never hardcode what features exist.

## Escaping

- Jinja2 auto-escapes by default in HTML templates. Trust it.
- Use `{{ value }}` normally — it's safe.
- Only use `{{ value | safe }}` when you KNOW the content is sanitized HTML (e.g., rendered markdown from the backend).
- Never use `| safe` on user input.

## Component Pattern

Components receive data via template context. Example:

```html
{# components/post-card.html #}
<article class="..." data-post-id="{{ post.id }}">
  <h3 class="...">{{ post.title }}</h3>
  <span class="...">{{ post.status }}</span>
  <time class="...">{{ post.created_at }}</time>
</article>
```

Usage:
```html
{% for post in posts %}
  {% with post=post %}
    {% include "components/post-card.html" %}
  {% endwith %}
{% endfor %}
```

## Anti-Patterns

- ❌ Business logic in templates (calculations, data transformations). Do it in Python, pass result.
- ❌ Direct file reading in templates. All data comes from the backend context.
- ❌ Deeply nested `{% if %}` blocks (more than 2 levels). Simplify in backend or use a macro.
- ❌ Inline `<style>` or `<script>` tags in templates (except for critical inline CSS in base.html).
- ❌ Using `| safe` on any user-supplied or config-file content without explicit sanitization.
