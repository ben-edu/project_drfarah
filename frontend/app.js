(function () {
  'use strict';

  // Keep the compact Dr. Farah brand treatment consistent on pages whose
  // hand-authored header/footer omits the decorative mark.
  document.querySelectorAll('.brand').forEach(function (brand) {
    if (brand.querySelector('.brand__mark') || !brand.querySelector('.brand__text')) return;
    var mark = document.createElement('span');
    mark.className = 'brand__mark';
    mark.setAttribute('aria-hidden', 'true');
    mark.innerHTML = '<svg viewBox="0 0 44 44" width="38" height="38" fill="none"><circle cx="22" cy="22" r="21" stroke="currentColor" stroke-width="1" opacity=".5"/><circle cx="22" cy="22" r="16.5" stroke="currentColor" stroke-width="1"/><path d="M17.5 14.5h9M17.5 14.5v15M17.5 22h6.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>';
    brand.insertBefore(mark, brand.querySelector('.brand__text'));
  });

  // Keep primary navigation consistent across legacy static pages during the
  // incremental marketing-alignment rollout. Existing HTML remains a no-JS
  // fallback; the runtime navigation reflects the current business priorities.
  document.querySelectorAll('nav.nav[aria-label="Primary"]').forEach(function (nav) {
    nav.innerHTML =
      '<a href="/services">Services</a>' +
      '<a href="/hotel-traveler-care">Hotel &amp; Traveler</a>' +
      '<a href="/pre-op-clearance">Pre-Op Clearance</a>' +
      '<a href="/about">The Physician</a>' +
      '<a href="/contact">Contact</a>';
  });

  // Header scroll state
  var header = document.getElementById('siteHeader');
  if (header) {
    var onScroll = function () {
      if (window.scrollY > 8) header.classList.add('is-scrolled');
      else header.classList.remove('is-scrolled');
    };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  // Cookie notice.
  // The site currently uses only essential first-party cookies. The notice is
  // still dismissible in both directions because users must never be trapped by
  // a persistent overlay. The preference itself is stored in localStorage so a
  // "Decline" choice does not need to create an additional cookie.
  var STORAGE_KEY = 'drfarah_cookie_choice';
  var banner = document.getElementById('cookie');
  var acceptBtn = document.getElementById('cookieOk');

  function getChoice() {
    try {
      return window.localStorage.getItem(STORAGE_KEY);
    } catch (e) {
      return null;
    }
  }

  function saveChoice(choice) {
    try {
      window.localStorage.setItem(STORAGE_KEY, choice);
    } catch (e) {
      // Storage can be unavailable in hardened/private browsing contexts.
      // The banner still closes for the current page session.
    }
  }

  function closeBanner(choice) {
    saveChoice(choice);
    if (banner) banner.hidden = true;
  }

  if (banner) {
    if (!getChoice()) banner.hidden = false;

    var actions = banner.querySelector('.cookie__actions');
    if (acceptBtn) {
      acceptBtn.textContent = 'Accept';
      acceptBtn.addEventListener('click', function () {
        closeBanner('accepted');
      });
    }

    if (actions && !document.getElementById('cookieDecline')) {
      var declineBtn = document.createElement('button');
      declineBtn.className = 'btn btn--outline btn--sm';
      declineBtn.id = 'cookieDecline';
      declineBtn.type = 'button';
      declineBtn.textContent = 'Decline';
      declineBtn.addEventListener('click', function () {
        closeBanner('declined');
      });
      actions.appendChild(declineBtn);
    }
  }
})();

/* Contact form — do not pretend to transmit a message until the ContactRequest
   API exists. The public booking workflow is real; general contact submission is
   not yet wired to a backend. */
(function () {
  'use strict';
  var f = document.getElementById('contactForm');
  if (!f) return;

  var msg = document.getElementById('contactMsg');
  f.addEventListener('submit', function (e) {
    e.preventDefault();

    var name = document.getElementById('cname');
    var email = document.getElementById('cemail');
    var cat = document.getElementById('ccat');
    var body = document.getElementById('cmsg');
    var consent = document.getElementById('cconsent');
    var ok = true;

    [name, email, cat, body].forEach(function (el) {
      if (!el.value.trim()) {
        el.style.borderColor = 'var(--gold)';
        ok = false;
      } else {
        el.style.borderColor = '';
      }
    });

    if (email.value && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value)) {
      email.style.borderColor = 'var(--gold)';
      ok = false;
    }
    if (!consent.checked) ok = false;

    if (!ok) {
      msg.className = 'form__msg is-err';
      msg.textContent = 'Please complete the required fields and agree to the privacy policy.';
      return;
    }

    msg.className = 'form__msg is-err';
    msg.textContent = 'Online general messaging is not enabled yet. Your message was not sent. Please call 310-467-0101, or use online booking for an appointment.';
  });
})();
