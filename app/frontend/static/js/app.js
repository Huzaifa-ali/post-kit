/** Core utilities — fetch wrapper, command bar, shared functions. */

/** Fetch wrapper with error handling. */
export async function api(path, options = {}) {
  const res = await fetch(`/api${path}`, {
    headers: { 'Content-Type': 'application/json', ...options.headers },
    ...options,
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(err.detail || `Request failed: ${res.status}`);
  }
  return res.json();
}

/** Debounce utility. */
export function debounce(fn, ms = 300) {
  let timer;
  return (...args) => {
    clearTimeout(timer);
    timer = setTimeout(() => fn(...args), ms);
  };
}

/** Short selector helpers. */
export function $(selector) {
  return document.querySelector(selector);
}

export function $$(selector) {
  return document.querySelectorAll(selector);
}

/** Command bar logic. */
function initCommandBar() {
  const bar = $('[data-command-bar]');
  const input = $('[data-command-input]');
  if (!bar || !input) return;

  const open = () => { bar.classList.remove('hidden'); input.focus(); };
  const close = () => { bar.classList.add('hidden'); input.value = ''; };

  document.addEventListener('keydown', (e) => {
    if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
      e.preventDefault();
      bar.classList.contains('hidden') ? open() : close();
    }
    if (e.key === 'Escape') close();
  });

  const openBtn = $('[data-action="open-command-bar"]');
  if (openBtn) openBtn.addEventListener('click', open);

  const closeBtn = $('[data-action="close-command-bar"]');
  if (closeBtn) closeBtn.addEventListener('click', close);
}

document.addEventListener('DOMContentLoaded', initCommandBar);
