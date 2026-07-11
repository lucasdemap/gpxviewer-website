(function () {
  const config = window.GPX_SITE_CONFIG || {};
  const measurementId = config.gaMeasurementId;

  if (!measurementId || measurementId.includes("XXXXXXXX")) {
    console.info("GPX Viewer site: set gaMeasurementId in js/config.js to enable Google Analytics.");
    return;
  }

  const script = document.createElement("script");
  script.async = true;
  script.src = `https://www.googletagmanager.com/gtag/js?id=${measurementId}`;
  document.head.appendChild(script);

  window.dataLayer = window.dataLayer || [];
  function gtag() {
    window.dataLayer.push(arguments);
  }
  window.gtag = gtag;
  gtag("js", new Date());
  gtag("config", measurementId, { anonymize_ip: true });

  window.trackEvent = function (name, params) {
    gtag("event", name, params || {});
  };
})();
