/** Tab switching — generic, used across pages. */
import { $ } from './app.js';

document.addEventListener('click', (e) => {
  const tab = e.target.closest('[data-tab]');
  if (!tab) return;

  const tabName = tab.dataset.tab;
  const container = tab.closest('[data-tabs]') || tab.parentElement.parentElement;

  // Update tab buttons
  const allTabs = tab.parentElement.querySelectorAll('[data-tab]');
  allTabs.forEach(t => {
    t.style.borderBottom = '2px solid transparent';
    t.style.color = 'var(--color-text-secondary)';
  });
  tab.style.borderBottom = '2px solid var(--color-accent)';
  tab.style.color = 'var(--color-text-primary)';

  // Show/hide views
  const views = container.querySelectorAll('[data-view]');
  views.forEach(v => {
    v.classList.toggle('hidden', v.dataset.view !== tabName);
  });
});
