document.addEventListener("DOMContentLoaded", function () {
    // Loop over all previous pickers
    document.querySelectorAll('[id^="start-date-picker-"]').forEach(picker => {
      new tempusDominus.TempusDominus(picker);
    });

    document.querySelectorAll('[id^="end-date-picker-"]').forEach(picker => {
      new tempusDominus.TempusDominus(picker);
    });
  });