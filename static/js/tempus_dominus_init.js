document.addEventListener("DOMContentLoaded", function () {
    const options = {
      display: {
        format: 'dd/MM/yyyy',
        components: {
          useTwentyfourHour: true,
          decades: false,
          year: true,
          month: true,
          date: true,
          hours: false,
          minutes: false,
          seconds: false
        }
      },
      localization: {
        locale: 'en-GB'
      }
    };
  
    document.querySelectorAll('[id^="start-date-picker-"]').forEach(picker => {
      new tempusDominus.TempusDominus(picker, options);
    });
  
    document.querySelectorAll('[id^="end-date-picker-"]').forEach(picker => {
      new tempusDominus.TempusDominus(picker, options);
    });
  });
  