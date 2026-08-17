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

  // Cookie notice — necessary-only, stored in a first-party cookie.
  var COOKIE_NAME = 'drfarah_cookie_ack';
  function hasAck() {
    return document.cookie.split('; ').some(function (c) { return c.indexOf(COOKIE_NAME + '=') === 0; });
  }
  var banner = document.getElementById('cookie');
  var okBtn = document.getElementById('cookieOk');
  if (banner && okBtn) {
    if (!hasAck()) banner.hidden = false;
    okBtn.addEventListener('click', function () {
      document.cookie = COOKIE_NAME + '=1; Max-Age=' + (60 * 60 * 24 * 365) + '; Path=/; SameSite=Lax';
      banner.hidden = true;
    });
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
