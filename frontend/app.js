(function () {
  'use strict';

  var IMAGE_REVISION = '20260825-3';

  // Load a small refinement layer without changing the established design system.
  // The revision is intentionally bumped so intermediaries cannot keep serving the
  // earlier stylesheet that hid the homepage and Services images.
  if (!document.querySelector('link[data-drfarah-refinement]')) {
    var refinement = document.createElement('link');
    refinement.rel = 'stylesheet';
    refinement.href = 'refinement.css?v=' + IMAGE_REVISION;
    refinement.setAttribute('data-drfarah-refinement', 'true');
    document.head.appendChild(refinement);
  }

  function versionedAsset(path) {
    return path + '?v=' + IMAGE_REVISION;
  }

  function forceVisibleImage(img, src, alt) {
    if (!img) return;
    img.setAttribute('src', versionedAsset(src));
    if (typeof alt === 'string') img.setAttribute('alt', alt);
    img.setAttribute('decoding', 'async');
    img.style.setProperty('opacity', '1', 'important');
    img.style.setProperty('visibility', 'visible', 'important');
    img.style.setProperty('display', 'block', 'important');
  }

  // Replace retired placeholder image references with the current approved real
  // Dr. Farah / clinic photography where those real photographs remain in use.
  var realPhotoMap = {
    'assets/consult-rejuvenation.jpg': {
      src: 'assets/dr-farah-portrait.webp',
      alt: 'Portrait of Dr. Farah'
    },
    'assets/mobile-visit.jpg': {
      src: 'assets/clinic-exterior.webp',
      alt: 'Exterior of Dr. Farah VIP Urgent Care at 9229 Wilshire Boulevard in Beverly Hills'
    },
    'assets/reception-vip.jpg': {
      src: 'assets/dr-farah-clinic.webp',
      alt: 'Dr. Farah in her Beverly Hills clinic'
    }
  };

  document.querySelectorAll('img[src]').forEach(function (img) {
    var currentSrc = img.getAttribute('src');
    var replacement = realPhotoMap[currentSrc];
    if (!replacement) return;
    img.setAttribute('src', replacement.src);
    img.setAttribute('alt', replacement.alt);
  });

  // Critical imagery is page-scoped and forced visible with versioned asset URLs.
  // This makes the result independent of stale CSS/background rules.
  var pagePath = window.location.pathname.replace(/\/+$/, '') || '/';

  if (pagePath === '/') {
    forceVisibleImage(
      document.querySelector('.hero__media img'),
      'assets/home-hero-doctor.webp',
      ''
    );

    forceVisibleImage(
      document.querySelector('.doctor__media img'),
      'assets/dr-farah-portrait.webp',
      'Portrait of Dr. Farah'
    );
  }

  if (pagePath === '/services') {
    var servicesHeroImage = document.querySelector('.services-hero__media img');
    forceVisibleImage(
      servicesHeroImage,
      'assets/service-iv-treatment.webp',
      'Illustrative physician-supervised IV treatment in a clinic setting'
    );
    if (servicesHeroImage) servicesHeroImage.classList.add('services-hero__image--ready');
  }

  if (pagePath === '/about') {
    forceVisibleImage(
      document.querySelector('.about-lead__media img'),
      'assets/dr-farah-portrait.webp',
      'Portrait of Dr. Farah'
    );

    forceVisibleImage(
      document.querySelector('.doctor__media img'),
      'assets/dr-farah-clinic.webp',
      'Dr. Farah in her Beverly Hills clinic'
    );
  }

  // Add a compact jump navigation to the long Services page so patients can
  // reach the relevant service family without scanning the full page.
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
      var headingText = heading.textContent.trim();
      sectionConfig.forEach(function (item) {
        if (headingText.indexOf(item.match) !== -1) {
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

  // Give the existing IV hydration service a stable deep-link target. This keeps
  // the header item tied to the real Services content without inventing a
  // standalone IV page that does not exist yet.
  var ivTreatmentCard = null;
  document.querySelectorAll('.svc-card__title').forEach(function (title) {
    if (title.textContent.trim().toLowerCase() === 'iv hydration & recovery') {
      ivTreatmentCard = title.closest('.svc-card');
      if (ivTreatmentCard) ivTreatmentCard.id = 'iv-treatment';
    }
  });

  // When arriving from another page with /services#iv-treatment, the target ID
  // is added by this script, so explicitly complete the hash navigation.
  if (ivTreatmentCard && window.location.hash === '#iv-treatment') {
    window.requestAnimationFrame(function () {
      ivTreatmentCard.scrollIntoView({ block: 'start' });
    });
  }

  // Use the actual insurer artwork already published by the clinic on its legacy
  // public website. This avoids misleading text-only substitutes on staging.
  // These should be localized into the new repository before final production
  // cutover so the new site does not depend on legacy WordPress asset URLs.
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

  // Remove ambiguity from pre-op scheduling CTAs. Until dedicated online pre-op
  // slots are configured, these actions intentionally call the clinic directly.
  if (window.location.pathname.indexOf('/pre-op-clearance') !== -1) {
    var preOpHeroCall = document.querySelector('.landing-hero__actions a[href^="tel:"]');
    if (preOpHeroCall) {
      preOpHeroCall.textContent = 'Call 310-467-0101 to schedule';
      preOpHeroCall.setAttribute('title', 'Calls the clinic directly');

      var heroHelper = document.createElement('p');
      heroHelper.className = 'cta-helper';
      heroHelper.textContent = 'Pre-op scheduling is currently handled by phone so the clinic can confirm the surgical requirements and timing.';
      preOpHeroCall.parentNode.insertAdjacentElement('afterend', heroHelper);
    }

    var preOpBottomCall = document.querySelector('.cta-band__actions a[href^="tel:"]');
    if (preOpBottomCall) {
      preOpBottomCall.textContent = 'Call 310-467-0101 to schedule';
      preOpBottomCall.setAttribute('title', 'Calls the clinic directly');
    }

    var mobileSchedule = document.querySelector('.mobilebar__btn--book[href^="tel:"]');
    if (mobileSchedule) mobileSchedule.textContent = 'Call to schedule';
  }

  // Make other ambiguous phone-based scheduling labels explicit where they exist.
  document.querySelectorAll('a[href^="tel:+13104670101"]').forEach(function (link) {
    if (link.textContent.trim().toLowerCase() === 'schedule by phone') {
      link.textContent = 'Call 310-467-0101';
      link.setAttribute('title', 'Calls the clinic directly');
    }
  });

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
  // incremental marketing-alignment rollout.
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

  // Header scroll state.
  var header = document.getElementById('siteHeader');
  if (header) {
    var onScroll = function () {
      if (window.scrollY > 8) header.classList.add('is-scrolled');
      else header.classList.remove('is-scrolled');
    };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  // Cookie notice. The site currently uses only essential first-party cookies.
  // Both choices dismiss the overlay and the preference is kept in localStorage.
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