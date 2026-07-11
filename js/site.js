(function () {
  const config = window.GPX_SITE_CONFIG || {};
  const appStoreUrl = config.appStoreUrl || "#";
  const playStoreUrl = config.playStoreUrl || "#";
  const contactEmail = config.contactEmail || "contact@gpxviewerapp.com";

  document.getElementById("year").textContent = new Date().getFullYear();

  const contactHref = `mailto:${contactEmail}`;
  const contactLink = document.getElementById("contact-link");
  const footerContact = document.getElementById("footer-contact");
  if (contactLink) {
    contactLink.href = contactHref;
    contactLink.textContent = contactEmail;
  }
  if (footerContact) {
    footerContact.href = contactHref;
  }

  function wireStoreLinks(selector, url, store) {
    document.querySelectorAll(selector).forEach(function (link) {
      link.href = url;
      link.addEventListener("click", function () {
        if (typeof window.trackEvent === "function") {
          window.trackEvent("app_store_click", {
            link_location: link.dataset.location || "unknown",
            store: store,
          });
        }
      });
    });
  }

  wireStoreLinks(".app-store-link", appStoreUrl, "app_store");
  wireStoreLinks(".play-store-link", playStoreUrl, "play_store");
})();
