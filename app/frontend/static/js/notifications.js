/** Notifications — badge count polling and dropdown. */
import { api, $ } from './app.js';

const bell = $('[data-action="notifications"]');
let badge = null;

async function updateBadge() {
  try {
    const data = await api('/notifications/unread-count');
    if (data.count > 0) {
      if (!badge) {
        badge = document.createElement('span');
        badge.style.cssText = 'position:absolute;top:2px;right:2px;width:16px;height:16px;border-radius:50%;background:var(--color-accent);color:white;font-size:10px;display:flex;align-items:center;justify-content:center;';
        bell?.appendChild(badge);
      }
      badge.textContent = data.count > 9 ? '9+' : data.count;
    } else if (badge) {
      badge.remove();
      badge = null;
    }
  } catch (e) {
    // Silent fail for polling
  }
}

// Poll every 30 seconds
if (bell) {
  updateBadge();
  setInterval(updateBadge, 30000);
}
