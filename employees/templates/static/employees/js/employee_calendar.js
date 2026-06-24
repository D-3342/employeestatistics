(function () {
  const cfg = window.EMPLOYEE_CALENDAR;
  const shell = document.querySelector('.calendar-shell');
  if (!shell) return;

  const body = document.querySelector('.js-calendar-body');
  const rangeEl = document.querySelector('.js-calendar-range');
  const totalEl = document.querySelector('.js-month-total');
  const prevBtn = document.querySelector('.js-prev-month');
  const nextBtn = document.querySelector('.js-next-month');

  const modal = document.querySelector('.calendar-modal');
  const title = document.querySelector('#day-modal-title');
  const statusEl = document.querySelector('#day-status');
  const hoursEl = document.querySelector('#day-hours');
  const saveBtn = document.querySelector('.js-save-day');
  const cancelBtn = document.querySelector('.js-cancel-day');
  const closeEls = document.querySelectorAll('.js-modal-close');

  let current = new Date();
  current.setDate(1);
  let selectedDate = null;
  let monthData = {};

  function pad(n) {
    return String(n).padStart(2, '0');
  }

  function dateISO(date) {
    return `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())}`;
  }

  function monthRangeLabel(date) {
    const start = `01.${pad(date.getMonth() + 1)}.${String(date.getFullYear()).slice(-2)}`;
    const last = new Date(date.getFullYear(), date.getMonth() + 1, 0).getDate();
    const end = `${pad(last)}.${pad(date.getMonth() + 1)}.${String(date.getFullYear()).slice(-2)}`;
    return `${start} - ${end}`;
  }

  function weekdayMonday(date) {
    const d = date.getDay();
    return d === 0 ? 6 : d - 1;
  }

  function isSunday(dateStr) {
    return new Date(dateStr + 'T00:00:00').getDay() === 0;
  }

  function getOptionByText(fragment) {
    return Array.from(statusEl.options).find(opt => opt.textContent.includes(fragment)) || null;
  }

  function setHoursLocked(lock, value = '0') {
    hoursEl.value = value;
    hoursEl.disabled = lock;
    hoursEl.classList.toggle('is-disabled', lock);
  }

  function syncHoursState() {
    const selectedText = statusEl.options[statusEl.selectedIndex]?.textContent || '';
    const working = selectedText.includes('Работает');

    if (isSunday(selectedDate)) {
      const offOpt = getOptionByText('Выходной');
      if (offOpt) statusEl.value = offOpt.value;
      statusEl.disabled = true;
      setHoursLocked(true, '0');
      return;
    }

    statusEl.disabled = false;

    if (working) {
      hoursEl.disabled = false;
      hoursEl.classList.remove('is-disabled');
      if (hoursEl.value === '') hoursEl.value = '';
    } else {
      setHoursLocked(true, '0');
    }
  }

  function openModal(dateStr, record) {
    selectedDate = dateStr;
    title.textContent = dateStr;

    const sunday = isSunday(dateStr);
    if (sunday) {
      const offOpt = getOptionByText('Выходной');
      if (offOpt) statusEl.value = offOpt.value;
      setHoursLocked(true, '0');
      statusEl.disabled = true;
    } else {
      statusEl.disabled = false;
      statusEl.value = record?.status_id || '';
      hoursEl.value = record?.hours ?? '';
      syncHoursState();
    }

    modal.hidden = false;
  }

  function closeModal() {
    modal.hidden = true;
    selectedDate = null;
  }

  function renderMonth(data) {
    monthData = data.days || {};
    totalEl.textContent = data.total_hours || 0;
    rangeEl.textContent = monthRangeLabel(current);

    const year = current.getFullYear();
    const month = current.getMonth();
    const first = new Date(year, month, 1);
    const daysInMonth = new Date(year, month + 1, 0).getDate();
    const startOffset = weekdayMonday(first);

    const sundayOpt = getOptionByText('Выходной');
    const sundayStatusId = sundayOpt ? sundayOpt.value : '';

    const cells = [];
    for (let i = 0; i < startOffset; i++) cells.push('<td></td>');

    for (let day = 1; day <= daysInMonth; day++) {
      const d = new Date(year, month, day);
      const iso = dateISO(d);
      let rec = monthData[iso];
      const sunday = d.getDay() === 0;

      if (sunday) {
        rec = {
          status_id: sundayStatusId,
          status_code: 'В',
          status_name: 'Выходной',
          hours: 0,
        };
        monthData[iso] = rec;
      }

      const hasFull = rec && rec.status_id && rec.hours !== null && rec.hours !== undefined && rec.hours !== '';
      const cls = hasFull ? 'calendar-day' : 'calendar-day calendar-day--missing';
      const dayClass = sunday ? 'calendar-day--sunday' : '';
      const statusText = rec?.status_code || '';
      const hoursText = rec?.hours !== null && rec?.hours !== undefined && rec?.hours !== '' ? `${rec.hours} часов` : '';

      cells.push(`
        <td data-date="${iso}" class="${dayClass}">
          <div class="${cls}">
            <div class="calendar-day__num">${day}</div>
            ${hasFull ? `
              <div class="calendar-day__status">${statusText}</div>
              <div class="calendar-day__hours">${hoursText}</div>
            ` : `
              <div class="calendar-day__missing-text">(не заполнено)</div>
            `}
          </div>
        </td>
      `);
    }

    const rows = [];
    for (let i = 0; i < cells.length; i += 7) {
      rows.push(`<tr>${cells.slice(i, i + 7).join('')}</tr>`);
    }
    body.innerHTML = rows.join('');

    body.querySelectorAll('td[data-date]').forEach(td => {
      if (td.classList.contains('calendar-day--sunday')) {
        td.style.pointerEvents = 'none';
      } else {
        td.style.pointerEvents = 'auto';
        td.addEventListener('click', () => {
          const iso = td.dataset.date;
          openModal(iso, monthData[iso]);
        });
      }
    });
  }

  async function loadMonth() {
    try {
      body.innerHTML = `<tr><td colspan="7" class="empty-state">Загрузка...</td></tr>`;

      const url = `${cfg.apiUrl}?year=${current.getFullYear()}&month=${current.getMonth() + 1}`;
      const res = await fetch(url, {
        headers: { 'Accept': 'application/json' },
        credentials: 'same-origin',
      });

      if (!res.ok) {
        const text = await res.text();
        console.error('Calendar API error:', res.status, text);
        body.innerHTML = `<tr><td colspan="7" class="empty-state">Не удалось загрузить календарь</td></tr>`;
        return;
      }

      const data = await res.json();
      renderMonth(data);
    } catch (e) {
      console.error('Calendar fetch failed:', e);
      body.innerHTML = `<tr><td colspan="7" class="empty-state">Ошибка сети</td></tr>`;
    }
  }

  function shiftMonth(delta) {
    current = new Date(current.getFullYear(), current.getMonth() + delta, 1);
    loadMonth();
  }

  async function saveDay() {
    if (!selectedDate) return;

    const sunday = isSunday(selectedDate);
    const selectedText = statusEl.options[statusEl.selectedIndex]?.textContent || '';
    const working = selectedText.includes('Работает');

    if (sunday) {
      const offOpt = getOptionByText('Выходной');
      if (offOpt) statusEl.value = offOpt.value;
      setHoursLocked(true, '0');
    } else if (!working) {
      setHoursLocked(true, '0');
    }

    const hoursRaw = hoursEl.value.trim();
    if (working && hoursRaw !== '') {
      const num = Number(hoursRaw);
      if (!Number.isInteger(num) || num < 0 || num > 16) {
        alert('Часы должны быть целым числом от 0 до 16');
        return;
      }
    }

    const payload = {
      date: selectedDate,
      status_id: statusEl.value || null,
      hours: (sunday || !working) ? 0 : (hoursRaw === '' ? null : Number(hoursRaw)),
    };

    const token = document.cookie
      .split('; ')
      .find(x => x.startsWith('csrftoken='))
      ?.split('=')[1];

    try {
      const res = await fetch(cfg.dayApiUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': token || '',
          'Accept': 'application/json',
        },
        body: JSON.stringify(payload),
        credentials: 'same-origin',
      });

      if (!res.ok) {
        const text = await res.text();
        console.error('Save day error:', res.status, text);
        alert('Не удалось сохранить данные');
        return;
      }

      await loadMonth();
      closeModal();
    } catch (e) {
      console.error('Save day failed:', e);
      alert('Ошибка сети');
    }
  }

  statusEl.addEventListener('change', syncHoursState);

  prevBtn.addEventListener('click', () => shiftMonth(-1));
  nextBtn.addEventListener('click', () => shiftMonth(1));
  saveBtn.addEventListener('click', saveDay);
  cancelBtn.addEventListener('click', closeModal);
  closeEls.forEach(el => el.addEventListener('click', closeModal));

  hoursEl.addEventListener('input', () => {
    hoursEl.value = hoursEl.value.replace(/[^\d]/g, '');
  });

  loadMonth();
})();