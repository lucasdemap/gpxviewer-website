(function () {
  const config = window.GPX_SITE_CONFIG || {};
  const appStoreUrl = config.appStoreUrl || "#";
  const contactEmail = config.contactEmail || "lucas@streiv.app";

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

  document.querySelectorAll(".app-store-link").forEach(function (link) {
    link.href = appStoreUrl;
    link.addEventListener("click", function () {
      if (typeof window.trackEvent === "function") {
        window.trackEvent("app_store_click", {
          link_location: link.dataset.location || "unknown",
        });
      }
    });
  });
})();
