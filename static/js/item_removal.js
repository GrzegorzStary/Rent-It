// This script handles the removal of items from a reservation list
(function () {
  const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

  document.querySelectorAll('.remove-item').forEach(function (btn) {
    btn.addEventListener('click', function (event) {
      event.preventDefault();

      let itemId = null;

      // Handle both ID's for mobile and destop buttons
      if (this.id.startsWith('remove_desktop_')) {
        itemId = this.id.replace('remove_desktop_', '');
      } else if (this.id.startsWith('remove_')) {
        itemId = this.id.replace('remove_', '');
      } else if (this.dataset.item) {
        itemId = this.dataset.item;
      }

      if (!itemId) {
        console.error('No item ID found for removal.');
        return;
      }

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
