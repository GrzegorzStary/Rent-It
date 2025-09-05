document.addEventListener("DOMContentLoaded", function () {
    const sortSel = document.getElementById("sort-selector");
    if (!sortSel) return;
  
    sortSel.addEventListener("change", function () {
      const selected = this.value;
      const url = new URL(window.location.href);
  
      if (selected === "reset") {
        url.searchParams.delete("sort");
      } else {
        url.searchParams.set("sort", selected);
      }
      window.location.href = url.toString();
    });
  });
  