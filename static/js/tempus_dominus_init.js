document.addEventListener("DOMContentLoaded", function () {
  const today = new Date();
  today.setHours(0, 0, 0, 0); // remove time component

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

  // Init specific single start date picker
  document.querySelectorAll('#start-date-picker').forEach(picker => {
    if (!picker.dataset.tdLoaded) {
      new tempusDominus.TempusDominus(picker, options);
      picker.dataset.tdLoaded = "true";
    }
  });

  // Init specific single end date picker
  document.querySelectorAll('#end-date-picker').forEach(picker => {
    if (!picker.dataset.tdLoaded) {
      new tempusDominus.TempusDominus(picker, options);
      picker.dataset.tdLoaded = "true";
    }
  });
});
