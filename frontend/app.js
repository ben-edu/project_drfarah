(function () {
  'use strict';

  // Header shadow on scroll.
  var header = document.getElementById('siteHeader');
  if (header) {
    var onScroll = function () {
      if (window.scrollY > 8) header.classList.add('is-scrolled');
      else header.classList.remove('is-scrolled');
    };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  // Cookie notice — necessary-only, choice stored in a first-party cookie.
  var COOKIE_NAME = 'drfarah_cookie_ack';

  function hasAck() {
    return document.cookie.split('; ').some(function (c) {
      return c.indexOf(COOKIE_NAME + '=') === 0;
    });
  }
  function setAck() {
    var oneYear = 60 * 60 * 24 * 365;
    document.cookie = COOKIE_NAME + '=1; Max-Age=' + oneYear + '; Path=/; SameSite=Lax';
  }

  var banner = document.getElementById('cookie');
  var okBtn = document.getElementById('cookieOk');
  if (banner && okBtn) {
    if (!hasAck()) banner.hidden = false;
    okBtn.addEventListener('click', function () {
      setAck();
      banner.hidden = true;
    });
  }
})();

/* Contact form — graceful handling until the ContactRequest API exists.
   Validates client-side and shows a clear next step (call the clinic). */
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
      if (!el.value.trim()) { el.style.borderColor = 'var(--gold-deep)'; ok = false; }
      else { el.style.borderColor = ''; }
    });
    if (email.value && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value)) { email.style.borderColor = 'var(--gold-deep)'; ok = false; }
    if (!consent.checked) ok = false;
    if (!ok) {
      msg.className = 'form__msg is-err';
      msg.textContent = 'Please complete the required fields and agree to the privacy policy.';
      return;
    }
    // No ContactRequest endpoint yet: acknowledge and direct to phone.
    msg.className = 'form__msg is-ok';
    msg.textContent = 'Thank you. Your message is noted. For anything time-sensitive, please call 310-467-0101 and we\u2019ll help right away.';
    f.reset();
  });
})();
