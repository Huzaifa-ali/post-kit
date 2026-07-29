/** Library page — filtering, search, and post click handling. */
import { api, $, debounce } from './app.js';

const postList = $('[data-post-list]');
const statusFilter = $('[data-filter="status"]');
const searchInput = $('[data-search="posts"]');

async function loadPosts() {
  const status = statusFilter?.value || '';
  const params = new URLSearchParams();
  if (status) params.set('status', status);

  const posts = await api(`/library/posts?${params.toString()}`);
  renderPosts(posts);
}

function renderPosts(posts) {
  if (!postList) return;
  postList.innerHTML = '';

  if (posts.length === 0) {
    postList.innerHTML = '<p class="text-secondary" style="grid-column:1/-1;text-align:center;padding:3rem 0;">No posts found.</p>';
    return;
  }

  posts.forEach(post => {
    const card = document.createElement('article');
    card.className = 'rounded-lg border border-border bg-surface-raised p-4 hover:border-accent/50 transition-colors cursor-pointer';
    card.dataset.postId = post.id;
    card.innerHTML = `
      <div class="flex items-center justify-between mb-2">
        <span class="text-xs font-medium px-2 py-0.5 rounded-full" style="background:var(--color-status-${post.status});color:white;">${post.status}</span>
        <time class="text-xs text-muted">${post.created_at || ''}</time>
      </div>
      <h3 class="text-sm font-medium text-primary truncate">${escapeHtml(post.title)}</h3>
      ${post.pillar ? `<span class="mt-1 inline-block text-xs text-secondary">${escapeHtml(post.pillar)}</span>` : ''}
    `;
    postList.appendChild(card);
  });
}

function escapeHtml(text) {
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}

// Filter by status
statusFilter?.addEventListener('change', loadPosts);

// Search with debounce
const handleSearch = debounce(async () => {
  const query = searchInput?.value?.trim().toLowerCase() || '';
  const posts = await api('/library/posts');
  if (!query) {
    renderPosts(posts);
    return;
  }
  const filtered = posts.filter(p =>
    p.title.toLowerCase().includes(query) ||
    (p.pillar || '').toLowerCase().includes(query)
  );
  renderPosts(filtered);
}, 300);

searchInput?.addEventListener('input', handleSearch);

// Click on post → show detail in a modal
postList?.addEventListener('click', async (e) => {
  const card = e.target.closest('[data-post-id]');
  if (!card) return;
  const postId = card.dataset.postId;
  const post = await api(`/library/posts/${postId}`);
  showPostDetail(post);
});

function showPostDetail(post) {
  const existing = document.querySelector('[data-post-modal]');
  if (existing) existing.remove();

  // Build metadata pills
  const metaItems = Object.entries(post.metadata || {})
    .filter(([k]) => !['status', 'pillar', 'platform'].includes(k))
    .map(([k, v]) => {
      const val = Array.isArray(v) ? v.join(', ') : v;
      return `<span class="inline-block text-xs px-2 py-0.5 rounded bg-surface-overlay text-secondary mr-1 mb-1"><strong>${escapeHtml(k)}:</strong> ${escapeHtml(String(val))}</span>`;
    }).join('');

  const modal = document.createElement('div');
  modal.setAttribute('data-post-modal', '');
  modal.className = 'fixed inset-0 z-50 flex items-center justify-center';
  modal.innerHTML = `
    <div class="absolute inset-0 bg-black/50" data-action="close-post-modal"></div>
    <div class="relative w-full max-w-3xl mx-4 rounded-xl border border-border bg-surface-raised overflow-hidden" style="max-height:85vh;box-shadow:var(--shadow-overlay);">
      <div class="flex items-center justify-between p-4 border-b border-border">
        <div>
          <h2 class="text-sm font-semibold text-primary">${escapeHtml(post.title)}</h2>
          <div class="flex items-center gap-2 mt-1">
            <span class="text-xs px-2 py-0.5 rounded-full text-white" style="background:var(--color-status-${post.status})">${post.status}</span>
            ${post.pillar ? `<span class="text-xs text-muted">${escapeHtml(post.pillar)}</span>` : ''}
            ${post.platform ? `<span class="text-xs text-muted">${escapeHtml(post.platform)}</span>` : ''}
            <span class="text-xs text-muted">${post.created_at || ''}</span>
          </div>
        </div>
        <button data-action="close-post-modal" class="text-muted hover:text-primary text-lg px-2">&times;</button>
      </div>
      ${metaItems ? `<div class="px-4 pt-3 flex flex-wrap">${metaItems}</div>` : ''}
      <div class="p-4 overflow-y-auto prose-content" style="max-height:70vh;">
        ${post.body_html || '<p class="text-muted">No content.</p>'}
      </div>
    </div>
  `;

  document.body.appendChild(modal);

  modal.querySelectorAll('[data-action="close-post-modal"]').forEach(btn => {
    btn.addEventListener('click', () => modal.remove());
  });

  document.addEventListener('keydown', function handler(e) {
    if (e.key === 'Escape') {
      modal.remove();
      document.removeEventListener('keydown', handler);
    }
  });
}
