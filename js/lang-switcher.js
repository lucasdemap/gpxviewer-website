(function () {
  var langs = window.GPX_LANGUAGES || [];
  var mount = document.querySelector("[data-lang-switcher]");
  if (!mount || !langs.length) return;

  var pathname = window.location.pathname;
  var current = document.documentElement.lang || "en";

  // Page path without language prefix: /, /privacy.html, /blog/, /blog/article.html
  var suffix = pathname.replace(/^\/(de|fr|it|pt|es)(?=\/|$)/, "");
  if (suffix === "") suffix = "/";
  if (suffix !== "/" && suffix.endsWith("/")) suffix = suffix.slice(0, -1);

  function hrefFor(lang) {
    if (lang.path === "/") {
      return suffix;
    }
    if (suffix === "/") {
      return lang.path;
    }
    return lang.path.replace(/\/$/, "") + suffix;
  }

  var html =
    '<nav class="lang-switcher" aria-label="Language">' +
    langs
      .map(function (lang) {
        var active = lang.code === current ? " is-active" : "";
        return (
          '<a href="' +
          hrefFor(lang) +
          '" hreflang="' +
          lang.code +
          '" class="' +
          active.trim() +
          '">' +
          lang.label +
          "</a>"
        );
      })
      .join("") +
    "</nav>";

  mount.innerHTML = html;
})();
