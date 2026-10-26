(function () {
  'use strict';

  var MEASUREMENT_ID = 'G-D58FTMF05S';
  var GOOGLE_CHOICE_KEY = 'drfarah_google_measurement_choice_v1';
  var PROD_HOSTS = ['drfarahvipurgentcare.com', 'www.drfarahvipurgentcare.com'];
  var PAGE_MAP = {
    '/about': 'clinic_about',
    '/contact': 'clinic_contact',
    '/privacy': 'privacy_policy',
    '/terms': 'terms_of_use',
    '/accessibility': 'accessibility',
    '/notice-of-privacy-practices': 'notice_of_privacy_practices'
  };

  function normalizePath(pathname) {
    var path = (pathname || '/').replace(/\/+$/, '') || '/';
    if (path.endsWith('.html')) path = path.slice(0, -5) || '/';
    return path;
  }

  function safeStorageGet(key) {
    try { return window.localStorage.getItem(key); } catch (e) { return null; }
  }

  function safeStorageSet(key, value) {
    try { window.localStorage.setItem(key, value); } catch (e) {}
  }

  var host = (window.location.hostname || '').toLowerCase();
  var pagePath = normalizePath(window.location.pathname);
  var pageClass = PAGE_MAP[pagePath];

  // Hard fail-closed guard: this file may exist in staging/source, but Google
  // measurement is allowed only on the production hostname and explicit
  // low-risk public-page allowlist below.
  if (PROD_HOSTS.indexOf(host) === -1 || !pageClass) return;

  window.dataLayer = window.dataLayer || [];
  function gtag() { window.dataLayer.push(arguments); }
  window.gtag = window.gtag || gtag;

  // Consent Mode defaults. Advertising storage/user data/personalization remain
  // denied in this implementation. Analytics storage follows the user's explicit
  // Google-measurement choice. When denied, the Google tag may send only the
  // limited cookieless signals supported by Consent Mode on these allowlisted pages.
  gtag('consent', 'default', {
    analytics_storage: 'denied',
    ad_storage: 'denied',
    ad_user_data: 'denied',
    ad_personalization: 'denied',
    functionality_storage: 'granted',
    security_storage: 'granted',
    wait_for_update: 500
  });

  var existingChoice = safeStorageGet(GOOGLE_CHOICE_KEY);
  if (existingChoice === 'accepted') {
    gtag('consent', 'update', { analytics_storage: 'granted' });
  }

  // Load the Google tag only on allowlisted production pages. Enhanced
  // Measurement remains disabled in the GA4 property; no form, scroll, outbound,
  // booking, registration, or service-intent events are emitted here.
  var script = document.createElement('script');
  script.async = true;
  script.src = 'https://www.googletagmanager.com/gtag/js?id=' + encodeURIComponent(MEASUREMENT_ID);
  script.setAttribute('data-drfarah-google-tag', 'true');
  document.head.appendChild(script);

  // Suppress automatic page views and advertising features. The manual page_view
  // uses a controlled page label and strips query strings, fragments, document
  // title, and referrer detail.
  gtag('js', new Date());
  gtag('config', MEASUREMENT_ID, {
    send_page_view: false,
    allow_google_signals: false,
    allow_ad_personalization_signals: false,
    page_location: 'https://drfarahvipurgentcare.com' + pagePath,
    page_referrer: ''
  });
  gtag('event', 'page_view', {
    page_location: 'https://drfarahvipurgentcare.com' + pagePath,
    page_title: pageClass,
    page_referrer: '',
    page_class: pageClass,
    send_to: MEASUREMENT_ID
  });

  function updateBannerCopyAndVisibility() {
    var banner = document.getElementById('cookie');
    if (!banner) return;

    var text = banner.querySelector('.cookie__text');
    if (text) {
      text.innerHTML = 'We use necessary site storage, optional first-party attribution, and Google Analytics on selected non-clinical public pages. If you decline, analytics cookies remain disabled; limited cookieless measurement may still occur on those selected pages. <a href="/privacy">Learn more</a>.';
    }

    // Earlier preference versions did not disclose Google Analytics. Require one
    // fresh choice before treating analytics storage as granted.
    if (!safeStorageGet(GOOGLE_CHOICE_KEY)) banner.hidden = false;
  }

  function attachConsentHandlers() {
    var accept = document.getElementById('cookieOk');
    var decline = document.getElementById('cookieDecline');

    if (accept && !accept.dataset.googleMeasurementBound) {
      accept.dataset.googleMeasurementBound = 'true';
      accept.addEventListener('click', function () {
        safeStorageSet(GOOGLE_CHOICE_KEY, 'accepted');
        gtag('consent', 'update', { analytics_storage: 'granted' });
      });
    }

    if (decline && !decline.dataset.googleMeasurementBound) {
      decline.dataset.googleMeasurementBound = 'true';
      decline.addEventListener('click', function () {
        safeStorageSet(GOOGLE_CHOICE_KEY, 'declined');
        gtag('consent', 'update', { analytics_storage: 'denied' });
      });
    }
  }

  // app.js runs before this deferred script in production assembly, so its
  // preference controls normally already exist. requestAnimationFrame is a
  // defensive fallback for slow DOM mutation / browser scheduling.
  updateBannerCopyAndVisibility();
  attachConsentHandlers();
  window.requestAnimationFrame(function () {
    updateBannerCopyAndVisibility();
    attachConsentHandlers();
  });
})();
