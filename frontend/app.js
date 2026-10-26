(function () {
  'use strict';

  var REVISION = '20261026-3';
  var pagePath = window.location.pathname.replace(/\/+$/, '') || '/';

  if (!document.querySelector('link[data-drfarah-refinement]')) {
    var refinement = document.createElement('link');
    refinement.rel = 'stylesheet';
    refinement.href = '/refinement.css?v=' + REVISION;
    refinement.setAttribute('data-drfarah-refinement', 'true');
    document.head.appendChild(refinement);
  }

  var servicesHero = document.querySelector('.services-hero');
  if (servicesHero && !document.querySelector('.service-jump')) {
    var sectionConfig = [
      { match: 'Urgent, traveler', id: 'care-now', label: 'Care Now' },
      { match: 'Pre-Operative', id: 'pre-op', label: 'Pre-Op' },
      { match: 'Virtual urgent care', id: 'virtual-care', label: 'Virtual Care' },
      { match: 'Personal Injury', id: 'personal-injury', label: 'Personal Injury' },
      { match: 'Additional physician services', id: 'additional-services', label: 'More Services' },
      { match: 'Rejuvenation consultation', id: 'rejuvenation', label: 'Rejuvenation' }
    ];
    var links = [];
    document.querySelectorAll('section.svc').forEach(function (section) {
      var heading = section.querySelector('h2');
      if (!heading) return;
      var text = heading.textContent.trim();
      sectionConfig.forEach(function (item) {
        if (text.indexOf(item.match) !== -1) {
          section.id = item.id;
          links.push('<a href="#' + item.id + '">' + item.label + '</a>');
        }
      });
    });
    if (links.length) {
      var jump = document.createElement('nav');
      jump.className = 'service-jump';
      jump.setAttribute('aria-label', 'Services on this page');
      jump.innerHTML = '<div class="wrap service-jump__inner"><span class="service-jump__label">Explore services</span><div class="service-jump__links">' + links.join('') + '</div></div>';
      servicesHero.insertAdjacentElement('afterend', jump);
    }
  }

  var ivTreatmentCard = null;
  document.querySelectorAll('.svc-card__title').forEach(function (title) {
    if (title.textContent.trim().toLowerCase() === 'iv hydration & recovery') {
      ivTreatmentCard = title.closest('.svc-card');
      if (ivTreatmentCard) ivTreatmentCard.id = 'iv-treatment';
    }
  });
  if (ivTreatmentCard && window.location.hash === '#iv-treatment') {
    window.requestAnimationFrame(function () {
      ivTreatmentCard.scrollIntoView({ block: 'start' });
    });
  }

  if (pagePath === '/pre-op-clearance') {
    var preOpHeroCall = document.querySelector('.landing-hero__actions a[href^="tel:"]');
    if (preOpHeroCall) {
      preOpHeroCall.textContent = 'Call 310-467-0101 to schedule';
      preOpHeroCall.setAttribute('title', 'Calls the clinic directly');
      if (!document.querySelector('.landing-hero__actions + .cta-helper')) {
        var helper = document.createElement('p');
        helper.className = 'cta-helper';
        helper.textContent = 'Pre-op scheduling is currently handled by phone so the clinic can confirm the surgical requirements and timing.';
        preOpHeroCall.parentNode.insertAdjacentElement('afterend', helper);
      }
    }
    var preOpBottomCall = document.querySelector('.cta-band__actions a[href^="tel:"]');
    if (preOpBottomCall) {
      preOpBottomCall.textContent = 'Call 310-467-0101 to schedule';
      preOpBottomCall.setAttribute('title', 'Calls the clinic directly');
    }
    var mobileSchedule = document.querySelector('.mobilebar__btn--book[href^="tel:"]');
    if (mobileSchedule) mobileSchedule.textContent = 'Call to schedule';
  }

  document.querySelectorAll('a[href^="tel:+13104670101"]').forEach(function (link) {
    if (link.textContent.trim().toLowerCase() === 'schedule by phone') {
      link.textContent = 'Call 310-467-0101';
      link.setAttribute('title', 'Calls the clinic directly');
    }
  });

  document.querySelectorAll('.brand').forEach(function (brand) {
    if (brand.querySelector('.brand__mark') || !brand.querySelector('.brand__text')) return;
    var mark = document.createElement('span');
    mark.className = 'brand__mark';
    mark.setAttribute('aria-hidden', 'true');
    mark.innerHTML = '<svg viewBox="0 0 44 44" width="38" height="38" fill="none"><circle cx="22" cy="22" r="21" stroke="currentColor" stroke-width="1" opacity=".5"/><circle cx="22" cy="22" r="16.5" stroke="currentColor" stroke-width="1"/><path d="M17.5 14.5h9M17.5 14.5v15M17.5 22h6.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>';
    brand.insertBefore(mark, brand.querySelector('.brand__text'));
  });

  document.querySelectorAll('nav.nav[aria-label="Primary"]').forEach(function (nav) {
    nav.innerHTML =
      '<a href="/services">Services</a>' +
      '<a href="/prp-treatments">PRP Treatments</a>' +
      '<a href="/weight-loss-program">Weight Loss</a>' +
      '<a href="/traveler-telehealth">Traveler &amp; Telehealth</a>' +
      '<a href="/iv-therapy">IV Therapy</a>' +
      '<a href="/pre-op-clearance">Pre-Op</a>' +
      '<a href="/about">The Physician</a>';
  });

  document.querySelectorAll('.topbar__inner').forEach(function (topbar) {
    if (topbar.querySelector('.topbar__registration')) return;
    var link = document.createElement('a');
    link.className = 'topbar__registration';
    link.href = '/patient-registration';
    link.textContent = 'Patient Registration';
    topbar.insertBefore(link, topbar.querySelector('.topbar__phone'));
  });

  var header = document.getElementById('siteHeader');
  if (header) {
    var onScroll = function () {
      if (window.scrollY > 8) header.classList.add('is-scrolled');
      else header.classList.remove('is-scrolled');
    };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  // First-party attribution. No page path, service, reason-for-visit, PII, or
  // clinical data is stored in this marketing attribution object.
  var ATTR_SESSION_KEY = 'drfarah_attribution_session_v1';
  var ATTR_PERSIST_KEY = 'drfarah_attribution_persist_v1';
  // v2 forces a fresh choice because the prior banner described essential-only storage.
  var COOKIE_CHOICE_KEY = 'drfarah_cookie_choice_v2';
  var ATTR_TTL_MS = 90 * 24 * 60 * 60 * 1000;

  function storageGet(storage, key) {
    try { return storage.getItem(key); } catch (e) { return null; }
  }
  function storageSet(storage, key, value) {
    try { storage.setItem(key, value); } catch (e) {}
  }
  function storageRemove(storage, key) {
    try { storage.removeItem(key); } catch (e) {}
  }
  function parseJson(value) {
    if (!value) return null;
    try { return JSON.parse(value); } catch (e) { return null; }
  }
  function clean(value, maxLength) {
    if (!value) return null;
    var text = String(value).replace(/[\u0000-\u001f\u007f]/g, '').trim();
    return text ? text.slice(0, maxLength) : null;
  }
  function newSessionId() {
    if (window.crypto && typeof window.crypto.randomUUID === 'function') return window.crypto.randomUUID();
    return 'mkt-' + Date.now().toString(36) + '-' + Math.random().toString(36).slice(2, 14);
  }
  function isGoogleHost(host) {
    return /(^|\.)google\./i.test(host || '') || /(^|\.)googleusercontent\.com$/i.test(host || '');
  }
  function canonicalSource(rawSource, utmSource, utmMedium, partner, clickIdPresent) {
    var s = (rawSource || '').toLowerCase();
    var us = (utmSource || '').toLowerCase();
    var um = (utmMedium || '').toLowerCase();

    if (clickIdPresent) return 'google_ads';
    if (s === 'google_ads' || s === 'google-ads' || s === 'adwords') return 'google_ads';
    if (s === 'google_business' || s === 'google-business' || s === 'gbp' || s === 'google_maps') return 'google_business';
    if (s === 'google_organic' || s === 'google-organic') return 'google_organic';
    if (s === 'hotel' || s === 'concierge' || s === 'hotel_concierge') return 'hotel_concierge';
    if (s === 'physician_referral' || s === 'surgeon_referral') return 'physician_referral';
    if (s === 'social') return 'social';
    if (partner) return 'partner_referral';

    if (us === 'google') {
      if (/cpc|ppc|paid|paidsearch/.test(um)) return 'google_ads';
      if (/business|maps|gbp/.test(um)) return 'google_business';
      return 'google_organic';
    }
    if (/facebook|instagram|linkedin|tiktok|youtube|twitter|^x$/.test(us)) return 'social';
    if (rawSource || utmSource) return 'other';

    if (document.referrer) {
      try {
        var refHost = new URL(document.referrer).hostname;
        if (refHost === window.location.hostname) return 'direct';
        if (isGoogleHost(refHost)) return 'google_organic';
        return 'other';
      } catch (e) {}
    }
    return 'direct';
  }

  function captureCurrentTouch() {
    var p = new URLSearchParams(window.location.search);
    var rawSource = clean(p.get('source'), 128);
    var partner = clean(p.get('partner'), 128);
    var traveler = (clean(p.get('traveler'), 16) || '').toLowerCase();
    if (['yes', 'no', 'unknown'].indexOf(traveler) === -1) traveler = 'unknown';

    var touch = {
      utm_source: clean(p.get('utm_source'), 128),
      utm_medium: clean(p.get('utm_medium'), 128),
      utm_campaign: clean(p.get('utm_campaign'), 256),
      utm_content: clean(p.get('utm_content'), 256),
      utm_term: clean(p.get('utm_term'), 256),
      gclid: clean(p.get('gclid'), 256),
      gbraid: clean(p.get('gbraid'), 256),
      wbraid: clean(p.get('wbraid'), 256),
      captured_at: new Date().toISOString()
    };

    var clickIdPresent = Boolean(touch.gclid || touch.gbraid || touch.wbraid);
    touch.source = canonicalSource(rawSource, touch.utm_source, touch.utm_medium, partner, clickIdPresent);
    Object.keys(touch).forEach(function (key) {
      if (touch[key] === null || touch[key] === '') delete touch[key];
    });

    return {
      touch: touch,
      partner_code: partner,
      traveler_segment: traveler,
      explicit: Boolean(
        rawSource || partner || p.get('traveler') || touch.utm_source || touch.utm_medium ||
        touch.utm_campaign || touch.utm_content || touch.utm_term || clickIdPresent
      )
    };
  }

  function validPersistent(state) {
    if (!state || !state.updated_at) return false;
    var updated = Date.parse(state.updated_at);
    return Number.isFinite(updated) && (Date.now() - updated) <= ATTR_TTL_MS;
  }

  var sessionState = parseJson(storageGet(window.sessionStorage, ATTR_SESSION_KEY));
  var cookieChoice = storageGet(window.localStorage, COOKIE_CHOICE_KEY);
  var persistentState = cookieChoice === 'accepted'
    ? parseJson(storageGet(window.localStorage, ATTR_PERSIST_KEY))
    : null;

  if (persistentState && !validPersistent(persistentState)) {
    storageRemove(window.localStorage, ATTR_PERSIST_KEY);
    persistentState = null;
  }

  var attributionState = sessionState || {
    marketing_session_id: newSessionId(),
    first_touch: persistentState && persistentState.first_touch ? persistentState.first_touch : null,
    last_touch: persistentState && persistentState.last_touch ? persistentState.last_touch : null,
    partner_code: persistentState ? (persistentState.partner_code || null) : null,
    traveler_segment: persistentState ? (persistentState.traveler_segment || 'unknown') : 'unknown',
    attribution_version: 'v1',
    created_at: new Date().toISOString()
  };

  var currentCapture = captureCurrentTouch();
  if (!attributionState.first_touch) attributionState.first_touch = currentCapture.touch;
  if (!attributionState.last_touch || currentCapture.explicit) attributionState.last_touch = currentCapture.touch;
  if (currentCapture.partner_code) attributionState.partner_code = currentCapture.partner_code;
  if (currentCapture.traveler_segment !== 'unknown') attributionState.traveler_segment = currentCapture.traveler_segment;
  attributionState.updated_at = new Date().toISOString();

  function persistAttribution() {
    storageSet(window.sessionStorage, ATTR_SESSION_KEY, JSON.stringify(attributionState));
    if (storageGet(window.localStorage, COOKIE_CHOICE_KEY) === 'accepted') {
      storageSet(window.localStorage, ATTR_PERSIST_KEY, JSON.stringify(attributionState));
    }
  }
  persistAttribution();

  window.DrFarahAttribution = {
    snapshot: function () {
      return JSON.parse(JSON.stringify({
        marketing_session_id: attributionState.marketing_session_id,
        first_touch: attributionState.first_touch,
        last_touch: attributionState.last_touch,
        partner_code: attributionState.partner_code || null,
        traveler_segment: attributionState.traveler_segment || 'unknown',
        attribution_version: 'v1'
      }));
    },
    setConsent: function (choice) {
      if (choice === 'accepted') {
        storageSet(window.localStorage, ATTR_PERSIST_KEY, JSON.stringify(attributionState));
      } else {
        storageRemove(window.localStorage, ATTR_PERSIST_KEY);
      }
    }
  };

  var STORAGE_KEY = COOKIE_CHOICE_KEY;
  var banner = document.getElementById('cookie');
  var acceptBtn = document.getElementById('cookieOk');
  function getChoice() {
    try { return window.localStorage.getItem(STORAGE_KEY); } catch (e) { return null; }
  }
  function saveChoice(choice) {
    try { window.localStorage.setItem(STORAGE_KEY, choice); } catch (e) {}
  }
  function closeBanner(choice) {
    saveChoice(choice);
    if (window.DrFarahAttribution) window.DrFarahAttribution.setConsent(choice);
    if (banner) banner.hidden = true;
  }
  if (banner) {
    var bannerText = banner.querySelector('.cookie__text');
    if (bannerText) {
      bannerText.innerHTML = 'We use necessary site storage and optional first-party attribution storage to understand which marketing sources lead to bookings. <a href="/privacy">Learn more</a>.';
    }
    if (!getChoice()) banner.hidden = false;
    var actions = banner.querySelector('.cookie__actions');
    if (acceptBtn) {
      acceptBtn.textContent = 'Accept';
      acceptBtn.addEventListener('click', function () { closeBanner('accepted'); });
    }
    if (actions && !document.getElementById('cookieDecline')) {
      var declineBtn = document.createElement('button');
      declineBtn.className = 'btn btn--outline btn--sm';
      declineBtn.id = 'cookieDecline';
      declineBtn.type = 'button';
      declineBtn.textContent = 'Decline';
      declineBtn.addEventListener('click', function () { closeBanner('declined'); });
      actions.appendChild(declineBtn);
    }
  }
})();
