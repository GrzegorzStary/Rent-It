// Profile picture live preview
(() => {
    const input = document.getElementById('id_profile_picture');
    const preview = document.getElementById('avatarPreview');
    if (!input || !preview) return;
  
    input.addEventListener('change', (e) => {
      const file = e.target.files && e.target.files[0];
      if (!file) return;
  
      const reader = new FileReader();
      reader.onload = (ev) => {
        preview.src = ev.target.result;
      };
      reader.readAsDataURL(file);
    });
  })();
  