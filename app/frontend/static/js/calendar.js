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
    const empty = document.createElement('div');
    empty.className = 'min-h-16';
    grid.appendChild(empty);
  }

  days.forEach(day => {
    const cell = document.createElement('div');
    cell.className = 'min-h-16 p-1.5 rounded-md border border-border-subtle';

    if (day.is_best_day) cell.classList.add('border-accent');
    if (day.is_slow_day) cell.classList.add('opacity-50');

    const num = document.createElement('span');
    num.className = 'text-xs font-medium text-secondary';
    num.textContent = day.day_number;
    cell.appendChild(num);

    day.posts.forEach(post => {
      const dot = document.createElement('div');
      dot.className = 'text-[10px] mt-0.5 truncate';
      dot.style.color = `var(--color-status-${post.status})`;
      dot.textContent = post.title;
      cell.appendChild(dot);
    });

    grid.appendChild(cell);
  });
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
