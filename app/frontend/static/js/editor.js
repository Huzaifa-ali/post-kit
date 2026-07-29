/** Editor — file editing modal for Brand page. */
import { api, $ } from './app.js';

const modal = $('[data-editor-modal]');
const filenameEl = $('[data-editor-filename]');
const contentEl = $('[data-editor-content]');
let currentFilename = null;

document.addEventListener('click', async (e) => {
  const btn = e.target.closest('[data-action="edit-file"]');
  if (!btn) return;

  currentFilename = btn.dataset.filename;
  const data = await api(`/brand/files/${currentFilename}`);

  if (filenameEl) filenameEl.textContent = currentFilename;
  if (contentEl) contentEl.value = data.content;
  if (modal) modal.classList.remove('hidden');
});

$('[data-action="save-file"]')?.addEventListener('click', async () => {
  if (!currentFilename || !contentEl) return;
  await api(`/brand/files/${currentFilename}`, {
    method: 'PUT',
    body: JSON.stringify({ content: contentEl.value }),
  });
  if (modal) modal.classList.add('hidden');
  window.location.reload();
});

$('[data-action="close-editor"]')?.addEventListener('click', () => {
  if (modal) modal.classList.add('hidden');
});

document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape' && modal && !modal.classList.contains('hidden')) {
    modal.classList.add('hidden');
  }
});
