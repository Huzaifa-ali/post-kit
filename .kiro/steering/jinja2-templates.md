---
inclusion: fileMatch
fileMatchPattern: "app/frontend/templates/**/*.html"
---

# Jinja2 Templates — Clean, Composable, Logic-Free

Templates are views. They display data — they don't compute it, fetch it, or decide it.

## Single Responsibility

- `base.html` — app shell only (sidebar, topbar, script/style includes)
- Page templates — one page each, extends base, fills blocks
- Components — one reusable piece each (post card, chat bubble, notification)

**The rule:** If a template has more than 2 levels of `{% if %}` nesting, the logic belongs in Python.

## Template Hierarchy

```
base.html                        ← Shell
├── content.html                 ← {% extends "base.html" %}
├── library.html
├── calendar.html
├── images.html
├── analytics.html
├── brand.html
├── settings.html
└── onboarding.html              ← Standalone (full-page, no sidebar)

components/
├── sidebar.html                 ← {% include %}
├── post-card.html
├── chat-bubble.html
├── command-bar.html
└── notification.html
```

## How to Write Templates (the boring, correct way)

### Page template
```html
{% extends "base.html" %}

{% block title %}Library{% endblock %}

{% block content %}
<section class="space-y-6">
  <header class="flex items-center justify-between">
    <h1 class="text-xl font-semibold text-primary">Library</h1>
    <input type="search" data-search="posts" placeholder="Search posts..." class="...">
  </header>

  <div data-post-list class="grid gap-4">
    {% for post in posts %}
      {% include "components/post-card.html" %}
    {% endfor %}

    {% if not posts %}
      <p class="text-secondary">No posts yet. Create your first one.</p>
    {% endif %}
  </div>
</section>
{% endblock %}

{% block scripts %}
<script type="module" src="/static/js/library.js"></script>
{% endblock %}
```

### Component
```html
{# components/post-card.html — receives `post` from context #}
<article class="rounded-lg border border-border bg-surface-raised p-4"
         data-post-id="{{ post.id }}">
  <div class="flex items-center justify-between mb-2">
    <span class="text-xs font-medium px-2 py-0.5 rounded bg-status-{{ post.status }} text-white">
      {{ post.status }}
    </span>
    <time class="text-xs text-secondary">{{ post.created_at }}</time>
  </div>
  <h3 class="font-medium text-primary truncate">{{ post.title }}</h3>
  {% if post.pillar %}
    <span class="text-xs text-secondary">{{ post.pillar }}</span>
  {% endif %}
</article>
```

## Rules

1. **No logic in templates.** Compute in Python, pass the result. Template just renders.
   ```html
   {# Bad — computing in template #}
   {% set engagement_rate = (likes + comments) / impressions * 100 %}
   
   {# Good — computed in Python, passed as context #}
   {{ engagement_rate }}%
   ```

2. **Conditional rendering for features, not logic.**
   ```html
   {# This is fine — showing/hiding based on config #}
   {% if has_analytics %}
     <a href="/analytics">Analytics</a>
   {% endif %}
   ```

3. **No deep nesting.** Max 2 levels of `{% if %}`. Flatten or move to Python.

4. **`{{ value }}` is auto-escaped.** Trust it. Only use `| safe` on backend-sanitized rendered markdown.

5. **Use `{% include %}` for composition.** Pass context with `{% with %}` if needed:
   ```html
   {% for post in posts %}
     {% with post=post, show_actions=true %}
       {% include "components/post-card.html" %}
     {% endwith %}
   {% endfor %}
   ```

6. **No hardcoded feature lists.** The backend decides what to show:
   ```html
   {# Good — iterating over whatever the backend provides #}
   {% for item in nav_items %}
     <a href="{{ item.url }}" class="...">{{ item.label }}</a>
   {% endfor %}

   {# Bad — hardcoded nav items in template #}
   <a href="/content">Content</a>
   <a href="/library">Library</a>
   ```

## Variables from Backend

- Pass clear, descriptive context: `posts`, `niche_config`, `nav_items`, `active_modules`
- Booleans: `is_onboarded`, `has_analytics`, `has_images`
- Never pass raw file contents to template — parse in Python first

## Anti-Patterns

- ❌ Business logic (calculations, string manipulation beyond basic formatting)
- ❌ Database calls or file reads
- ❌ More than 2 levels of `{% if %}` nesting
- ❌ `| safe` on anything from user config or user input
- ❌ Hardcoded lists of features, modules, or nav items
- ❌ Inline `<style>` or `<script>` blocks (except module import in `{% block scripts %}`)
- ❌ Duplicated markup that should be a component
