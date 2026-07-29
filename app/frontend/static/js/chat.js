/** Chat interface — handles message sending and streaming responses. */
import { $ } from './app.js';

const form = $('[data-chat-form]');
const input = $('[data-chat-input]');
const messages = $('[data-chat-messages]');

if (form && input && messages) {
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const text = input.value.trim();
    if (!text) return;

    appendMessage('user', text);
    input.value = '';

    try {
      const res = await fetch('/api/content/send', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text }),
      });

      const reader = res.body.getReader();
      const decoder = new TextDecoder();
      let assistantText = '';
      const bubble = appendMessage('assistant', '...');

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        const chunk = decoder.decode(value, { stream: true });
        for (const line of chunk.split('\n')) {
          if (line.startsWith('data: ')) {
            const data = line.slice(6);
            if (data === '[DONE]') break;
            assistantText += data;
            bubble.textContent = assistantText;
          }
        }
      }
    } catch (err) {
      appendMessage('assistant', `Error: ${err.message}`);
    }
  });
}

function appendMessage(role, content) {
  const div = document.createElement('div');
  div.className = `flex gap-3 ${role === 'user' ? 'justify-end' : ''}`;

  const bubble = document.createElement('div');
  bubble.className = 'rounded-xl px-4 py-2 text-sm';
  bubble.style.maxWidth = '80%';

  if (role === 'user') {
    bubble.style.background = 'var(--color-accent)';
    bubble.style.color = 'white';
  } else {
    bubble.style.background = 'var(--color-surface-raised)';
    bubble.style.color = 'var(--color-text-primary)';
    bubble.style.border = '1px solid var(--color-border)';
  }

  bubble.textContent = content;
  div.appendChild(bubble);
  messages.appendChild(div);
  messages.scrollTop = messages.scrollHeight;
  return bubble;
}
