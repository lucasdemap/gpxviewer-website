(function () {
  document.querySelectorAll(".lang-dropdown").forEach(function (dropdown) {
    dropdown.addEventListener("toggle", function () {
      if (!dropdown.open) return;
      document.querySelectorAll(".lang-dropdown[open]").forEach(function (other) {
        if (other !== dropdown) other.removeAttribute("open");
      });
    });
  });

  document.addEventListener("click", function (event) {
    document.querySelectorAll(".lang-dropdown[open]").forEach(function (dropdown) {
      if (!dropdown.contains(event.target)) {
        dropdown.removeAttribute("open");
      }
    });
  });

  document.addEventListener("keydown", function (event) {
    if (event.key !== "Escape") return;
    document.querySelectorAll(".lang-dropdown[open]").forEach(function (dropdown) {
      dropdown.removeAttribute("open");
    });
  });
})();
