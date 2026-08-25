(function () {
  'use strict';

  var REVISION = '20260825-5';
  var pagePath = window.location.pathname.replace(/\/+$/, '') || '/';

  // Keep the approved refinement layer, but load a new revision so staging
  // cannot reuse the earlier image-handling CSS response.
  if (!document.querySelector('link[data-drfarah-refinement]')) {
    var refinement = document.createElement('link');
    refinement.rel = 'stylesheet';
    refinement.href = '/refinement.css?v=' + REVISION;
    refinement.setAttribute('data-drfarah-refinement', 'true');
    document.head.appendChild(refinement);
  }

  // Critical imagery is stored as exact base64 text chunks because the previous
  // binary upload path changed the image bytes. Never clear the existing image
  // first: replace it only after the reconstructed WebP has decoded successfully.
  var reliableImages = {
    '/': [
      {
        selector: '.hero__media img',
        parts: ['/image-data-v5/home-01.txt', '/image-data-v5/home-02.txt', '/image-data-v5/home-03.txt'],
        alt: ''
      },
      {
        selector: '.doctor__media img',
        parts: ['/image-data-v5/portrait-01.txt', '/image-data-v5/portrait-02.txt', '/image-data-v5/portrait-03.txt'],
        alt: 'Portrait of Dr. Farah'
      }
    ],
    '/services': [
      {
        selector: '.services-hero__media img',
        parts: ['/image-data-v5/iv-01.txt', '/image-data-v5/iv-02.txt'],
        alt: 'Illustrative physician-supervised IV treatment in a clinic setting'
      }
    ],
    '/about': [
      {
        selector: '.about-lead__media img',
        parts: ['/image-data-v5/portrait-01.txt', '/image-data-v5/portrait-02.txt', '/image-data-v5/portrait-03.txt'],
        alt: 'Portrait of Dr. Farah'
      },
      {
        selector: '.doctor__media img',
        parts: ['/image-data-v5/about-01.txt', '/image-data-v5/about-02.txt', '/image-data-v5/about-03.txt'],
        alt: 'Dr. Farah in her clinic'
      }
    ]
  };

  function fetchChunk(url) {
    return fetch(url + '?v=' + REVISION, { cache: 'no-store' }).then(function (response) {
      if (!response.ok) throw new Error('Image chunk failed: ' + url + ' (' + response.status + ')');
      return response.text();
    });
  }

  function replaceAfterDecode(spec) {
    var target = document.querySelector(spec.selector);
    if (!target) return;

    var originalSrc = target.getAttribute('src');
    var originalAlt = target.getAttribute('alt') || '';

    Promise.all(spec.parts.map(fetchChunk))
      .then(function (parts) {
        var base64 = parts.join('').replace(/\s+/g, '');
        var dataUrl = 'data:image/webp;base64,' + base64;
        var probe = new Image();

        probe.onload = function () {
          target.setAttribute('src', dataUrl);
          target.setAttribute('alt', spec.alt || '');
          target.setAttribute('decoding', 'async');
          target.style.setProperty('display', 'block', 'important');
          target.style.setProperty('visibility', 'visible', 'important');
          target.style.setProperty('opacity', '1', 'important');
          target.setAttribute('data-image-revision', REVISION);
        };

        probe.onerror = function () {
          // Preserve the original HTML image on any reconstruction/decoding error.
          target.setAttribute('src', originalSrc);
          target.setAttribute('alt', originalAlt);
          target.style.setProperty('display', 'block', 'important');
          target.style.setProperty('visibility', 'visible', 'important');
          target.style.setProperty('opacity', '1', 'important');
          console.error('Dr. Farah image decode failed for ' + spec.selector);
        };

        probe.src = dataUrl;
      })
      .catch(function (error) {
        target.setAttribute('src', originalSrc);
        target.setAttribute('alt', originalAlt);
        target.style.setProperty('display', 'block', 'important');
        target.style.setProperty('visibility', 'visible', 'important');
        target.style.setProperty('opacity', '1', 'important');
        console.error(error);
      });
  }

  (reliableImages[pagePath] || []).forEach(replaceAfterDecode);

  // Replace only non-critical legacy placeholders. Critical homepage, Services,
  // and About imagery is intentionally excluded from this map.
  var realPhotoMap = {
    'assets/mobile-visit.jpg': {
      src: 'assets/clinic-exterior.webp',
      alt: 'Exterior of Dr. Farah VIP Urgent Care at 9229 Wilshire Boulevard in Beverly Hills'
    }
  };

  document.querySelectorAll('img[src]').forEach(function (img) {
    var replacement = realPhotoMap[img.getAttribute('src')];
    if (!replacement) return;
    img.setAttribute('src', replacement.src);
    img.setAttribute('alt', replacement.alt);
  });

  // Compact jump navigation for the Services overview.
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

  // Stable direct target for the real IV hydration service.
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

  // Use insurer artwork from the clinic's legacy public site during staging.
  var insuranceGrid = document.querySelector('.insurance__logos');
  if (insuranceGrid) {
    var insurerLogos = [
      'https://drfarahvipurgentcare.com/wp-content/uploads/2025/02/6.png',
      'https://drfarahvipurgentcare.com/wp-content/uploads/2025/02/14.png',
      'https://drfarahvipurgentcare.com/wp-content/uploads/2025/02/3.png',
      'https://drfarahvipurgentcare.com/wp-content/uploads/2025/02/21.png',
      'https://drfarahvipurgentcare.com/wp-content/uploads/2025/02/aetna.jpg',
      'https://drfarahvipurgentcare.com/wp-content/uploads/2025/02/22.png'
    ];
    insuranceGrid.innerHTML = '';
    insuranceGrid.classList.add('insurance__logos--artwork');
    insurerLogos.forEach(function (src) {
      var card = document.createElement('div');
      card.className = 'insurance-logo insurance-logo--artwork';
      var img = document.createElement('img');
      img.src = src;
      img.alt = 'Insurance plan logo accepted or referenced by Dr. Farah VIP Urgent Care';
      img.loading = 'lazy';
      img.decoding = 'async';
      img.referrerPolicy = 'no-referrer';
      var fallback = document.createElement('span');
      fallback.className = 'insurance-logo__fallback';
      fallback.textContent = 'Insurance plan';
      fallback.hidden = true;
      img.addEventListener('error', function () {
        img.hidden = true;
        fallback.hidden = false;
        card.classList.add('insurance-logo--fallback');
      });
      card.appendChild(img);
      card.appendChild(fallback);
      insuranceGrid.appendChild(card);
    });
    var insuranceAction = document.querySelector('.insurance__action');
    if (insuranceAction) {
      insuranceAction.textContent = 'Call 310-467-0101 to verify coverage';
      insuranceAction.setAttribute('aria-label', 'Call Dr. Farah VIP Urgent Care at 310-467-0101 to verify insurance coverage');
      insuranceAction.setAttribute('title', 'Calls the clinic directly');
    }
  }

  // Make pre-op phone scheduling explicit until dedicated online slots exist.
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

  // Brand mark consistency on legacy static pages.
  document.querySelectorAll('.brand').forEach(function (brand) {
    if (brand.querySelector('.brand__mark') || !brand.querySelector('.brand__text')) return;
    var mark = document.createElement('span');
    mark.className = 'brand__mark';
    mark.setAttribute('aria-hidden', 'true');
    mark.innerHTML = '<svg viewBox="0 0 44 44" width="38" height="38" fill="none"><circle cx="22" cy="22" r="21" stroke="currentColor" stroke-width="1" opacity=".5"/><circle cx="22" cy="22" r="16.5" stroke="currentColor" stroke-width="1"/><path d="M17.5 14.5h9M17.5 14.5v15M17.5 22h6.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>';
    brand.insertBefore(mark, brand.querySelector('.brand__text'));
  });

  // Primary navigation including the two direct entries requested for staging.
  document.querySelectorAll('nav.nav[aria-label="Primary"]').forEach(function (nav) {
    nav.innerHTML =
      '<a href="/services">Services</a>' +
      '<a href="/virtual-urgent-care">Telehealth / Virtual Visit</a>' +
      '<a href="/services#iv-treatment">IV Treatment</a>' +
      '<a href="/hotel-traveler-care">Hotel &amp; Traveler</a>' +
      '<a href="/pre-op-clearance">Pre-Op Clearance</a>' +
      '<a href="/about">The Physician</a>' +
      '<a href="/contact">Contact</a>';
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

  // Cookie preference banner.
  var STORAGE_KEY = 'drfarah_cookie_choice';
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
    if (banner) banner.hidden = true;
  }
  if (banner) {
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

// Contact form: never pretend to transmit until a ContactRequest API exists.
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
      if (!el.value.trim()) { el.style.borderColor = 'var(--gold)'; ok = false; }
      else el.style.borderColor = '';
    });
    if (email.value && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value)) {
      email.style.borderColor = 'var(--gold)'; ok = false;
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
