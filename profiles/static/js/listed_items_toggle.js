document.addEventListener('DOMContentLoaded', function () {
    // Auto-submit the toggle form when the checkbox changes
    document.querySelectorAll('.toggle-form .ios-checkbox').forEach(function (cb) {
      cb.addEventListener('change', function (e) {
        const form = e.target.closest('form');
        if (form) form.submit();
      });
    });
  
    // Prevent accidental navigation when clicking the toggle area
    document.querySelectorAll('.card-toggle, .card-toggle *').forEach(function (el) {
      el.addEventListener('click', function (e) {
        e.stopPropagation();
      });
    });
  });
  