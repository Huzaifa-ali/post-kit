/** Calendar page — month grid rendering and navigation. */
import { api, $ } from './app.js';

const grid = $('[data-calendar-grid]');
const title = $('[data-calendar-title]');
let currentYear = new Date().getFullYear();
let currentMonth = new Date().getMonth() + 1;

async function loadMonth(year, month) {
  const data = await api(`/calendar/month/${year}/${month}`);
  renderDays(data.days, year, month);
  const monthName = new Date(year, month - 1).toLocaleString('default', { month: 'long' });
  if (title) title.textContent = `${monthName} ${year}`;
}

function renderDays(days, year, month) {
  if (!grid) return;
  while (grid.children.length > 7) {
    grid.removeChild(grid.lastChild);
  }

  const firstDay = new Date(year, month - 1, 1).getDay();
  const offset = firstDay === 0 ? 6 : firstDay - 1;
  for (let i = 0; i < offset; i++) {
    grid.appendChild(createEmptyCell());
  }

  days.forEach(day => {
    const cell = document.createElement('div');
    cell.style.minHeight = '4rem';
    cell.style.padding = '0.25rem';
    cell.style.borderRadius = '0.375rem';
    cell.style.border = '1px solid var(--color-border-subtle)';

    if (day.is_best_day) cell.style.borderColor = 'var(--color-accent)';
    if (day.is_slow_day) cell.style.opacity = '0.5';

    const num = document.createElement('span');
    num.style.fontSize = '0.75rem';
    num.style.color = 'var(--color-text-secondary)';
    num.style.fontWeight = '500';
    num.textContent = day.day_number;
    cell.appendChild(num);

    day.posts.forEach(post => {
      const dot = document.createElement('div');
      dot.style.fontSize = '0.625rem';
      dot.style.marginTop = '0.125rem';
      dot.style.overflow = 'hidden';
      dot.style.textOverflow = 'ellipsis';
      dot.style.whiteSpace = 'nowrap';
      dot.style.color = `var(--color-status-${post.status})`;
      dot.textContent = post.title;
      cell.appendChild(dot);
    });

    grid.appendChild(cell);
  });
}

function createEmptyCell() {
  const cell = document.createElement('div');
  cell.style.minHeight = '4rem';
  return cell;
}

$('[data-action="prev-month"]')?.addEventListener('click', () => {
  currentMonth--;
  if (currentMonth < 1) { currentMonth = 12; currentYear--; }
  loadMonth(currentYear, currentMonth);
});

$('[data-action="next-month"]')?.addEventListener('click', () => {
  currentMonth++;
  if (currentMonth > 12) { currentMonth = 1; currentYear++; }
  loadMonth(currentYear, currentMonth);
});

if (grid) loadMonth(currentYear, currentMonth);
