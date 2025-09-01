// This script handles the removal of items from a reservation list
  (function () {
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

    document.querySelectorAll('.remove-item').forEach(function (btn) {
      btn.addEventListener('click', function (event) {
        event.preventDefault();

        const itemId = this.id.split('remove_')[1];

        fetch(`/reservation/remove/${itemId}/`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': csrfToken
          },
          body: new URLSearchParams()
        })
        .then(response => {
          if (response.ok) {
            window.location.reload();
          } else {
            alert("Item could not be removed. Server error.");
          }
        })
        .catch(error => {
          console.error('Error:', error);
        });
      });
    });
  })();

