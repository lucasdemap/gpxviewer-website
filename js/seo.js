(function () {
  const config = window.GPX_SITE_CONFIG || {};
  const token = config.searchConsoleVerification;

  if (token) {
    let meta = document.querySelector('meta[name="google-site-verification"]');
    if (!meta) {
      meta = document.createElement("meta");
      meta.name = "google-site-verification";
      document.head.appendChild(meta);
    }
    meta.content = token;
  }
})();
