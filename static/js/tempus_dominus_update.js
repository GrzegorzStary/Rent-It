document.addEventListener("DOMContentLoaded", function () {
  const today = new Date();
  today.setHours(0, 0, 0, 0); // Strip time

  const options = {
    localization: {
      locale: 'en-GB',
      format: 'dd/MM/yyyy',
      hourCycle: 'h23'
    },
    display: {
      components: {
        decades: false,
        year: true,
        month: true,
        date: true,
        hours: false,
        minutes: false,
        seconds: false
      }
    },
    restrictions: {
      minDate: today
    }
  };

  // Handle both fixed ID and dynamic ID pickers
  document.querySelectorAll('#start-date-picker, [id^="start-date-picker-"]').forEach(startPicker => {
    const id = startPicker.id.includes('-') ? startPicker.id.replace('start-date-picker-', '') : null;

    const endPicker = id
      ? document.getElementById(`end-date-picker-${id}`)
      : document.getElementById(`end-date-picker`);

    const startInput = id
      ? document.getElementById(`start-date-${id}`)
      : document.getElementById(`start-date`);

    const endInput = id
      ? document.getElementById(`end-date-${id}`)
      : document.getElementById(`end-date`);

    if (!startInput || !endInput || !endPicker) {
      console.warn(`Missing input or picker for ID: ${id ?? 'default'}`);
      return;
    }

    // Initialize date pickers
    new tempusDominus.TempusDominus(startPicker, options);
    new tempusDominus.TempusDominus(endPicker, options);

    // Auto-set end date = start date + 1 day
    startInput.addEventListener("change", () => {
      const [day, month, year] = startInput.value.split('/');
      const startDate = new Date(`${year}-${month}-${day}`);
      if (isNaN(startDate)) return;

      const nextDate = new Date(startDate.getTime() + 86400000);
      const dayStr = String(nextDate.getDate()).padStart(2, '0');
      const monthStr = String(nextDate.getMonth() + 1).padStart(2, '0');
      const yearStr = nextDate.getFullYear();

      endInput.value = `${dayStr}/${monthStr}/${yearStr}`;
    });
  });
});
