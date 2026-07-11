(function () {
  function positionMobileMenu(dropdown) {
    var menu = dropdown.querySelector(".lang-dropdown-menu");
    var summary = dropdown.querySelector("summary");
    if (!menu || !summary) return;

    if (window.innerWidth > 900) {
      menu.style.top = "";
      menu.style.left = "";
      menu.style.right = "";
      return;
    }

    var rect = summary.getBoundingClientRect();
    menu.style.top = rect.bottom + 8 + "px";
    menu.style.right = Math.max(16, window.innerWidth - rect.right) + "px";
    menu.style.left = "auto";
  }

  document.querySelectorAll(".lang-dropdown").forEach(function (dropdown) {
    dropdown.addEventListener("click", function (event) {
      event.stopPropagation();
    });

    dropdown.addEventListener("toggle", function () {
      if (!dropdown.open) return;

      document.querySelectorAll(".lang-dropdown[open]").forEach(function (other) {
        if (other !== dropdown) other.removeAttribute("open");
      });

      positionMobileMenu(dropdown);
    });
  });

  window.addEventListener("resize", function () {
    document.querySelectorAll(".lang-dropdown[open]").forEach(positionMobileMenu);
  });

  window.addEventListener(
    "scroll",
    function () {
      document.querySelectorAll(".lang-dropdown[open]").forEach(positionMobileMenu);
    },
    { passive: true }
  );

  document.addEventListener("pointerdown", function (event) {
    if (event.target.closest(".lang-dropdown")) return;

    document.querySelectorAll(".lang-dropdown[open]").forEach(function (dropdown) {
      dropdown.removeAttribute("open");
    });
  });

  document.addEventListener("keydown", function (event) {
    if (event.key !== "Escape") return;

    document.querySelectorAll(".lang-dropdown[open]").forEach(function (dropdown) {
      dropdown.removeAttribute("open");
    });
  });
})();
