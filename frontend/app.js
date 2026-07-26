
(() => {
  const header = document.querySelector('[data-header]');
  const overlay = document.querySelector('[data-booking-overlay]');
  const form = document.querySelector('[data-booking-form]');
  const steps = [...document.querySelectorAll('[data-step]')];
  const progress = [...document.querySelectorAll('[data-progress]')];
  const next = document.querySelector('[data-next]');
  const prev = document.querySelector('[data-prev]');
  const actions = document.querySelector('[data-booking-actions]');
  const success = document.querySelector('[data-success]');
  const summary = document.querySelector('[data-summary]');
  const timeOptions = document.querySelector('[data-time-options]');
  const moreSlotsButton = document.querySelector('[data-more-slots]');
  const cookieBanner = document.querySelector('[data-cookie-banner]');
  const cookieAccept = document.querySelector('[data-cookie-accept]');
  const cookieDismiss = document.querySelector('[data-cookie-dismiss]');

  const slotList = [
    '8:00 AM', '8:30 AM', '9:00 AM', '9:30 AM',
    '10:00 AM', '10:30 AM', '11:00 AM', '11:30 AM',
    '12:30 PM', '1:00 PM', '1:30 PM', '2:00 PM',
    '2:30 PM', '3:00 PM', '3:30 PM', '4:00 PM'
  ];

  let currentStep = 1;
  let visibleSlots = 8;

  const updateHeader = () => {
    header?.classList.toggle('scrolled', window.scrollY > 8);
  };
  updateHeader();
  window.addEventListener('scroll', updateHeader, { passive: true });

  function setService(value) {
    if (!value) return;
    const escaped = typeof CSS !== 'undefined' && CSS.escape ? CSS.escape(value) : value.replace(/"/g, '\"');
    const input = form.querySelector(`input[name="service"][value="${escaped}"]`);
    if (input) input.checked = true;
  }

  function renderSlots() {
    if (!timeOptions) return;
    const selected = form.querySelector('input[name="time"]:checked')?.value || slotList[0];
    timeOptions.innerHTML = slotList.slice(0, visibleSlots).map((time, index) => `
      <label>
        <input type="radio" name="time" value="${time}" ${time === selected || (!selected && index === 0) ? 'checked' : ''}>
        <span>${time}</span>
      </label>
    `).join('');

    moreSlotsButton.hidden = visibleSlots >= slotList.length;
  }

  function openBooking(service) {
    setService(service);
    currentStep = 1;
    visibleSlots = 8;
    renderSlots();
    success.hidden = true;
    actions.hidden = false;
    updateStep();
    overlay.hidden = false;
    document.body.classList.add('booking-open');
    setTimeout(() => overlay.querySelector('input, select, button')?.focus(), 60);
  }

  function closeBooking() {
    overlay.hidden = true;
    document.body.classList.remove('booking-open');
  }

  function updateStep() {
    steps.forEach(step => step.classList.toggle('active', Number(step.dataset.step) === currentStep));
    progress.forEach(item => item.classList.toggle('active', Number(item.dataset.progress) <= currentStep));
    prev.disabled = currentStep === 1;
    next.textContent = currentStep === 4 ? 'Submit request' : 'Continue';
  }

  function validateCurrentStep() {
    const step = steps.find(item => Number(item.dataset.step) === currentStep);
    const required = [...step.querySelectorAll('[required]')];
    return required.every(field => field.reportValidity());
  }

  function renderSummary() {
    const data = new FormData(form);
    const rows = [
      ['Care', data.get('service')],
      ['Visit', data.get('visitType')],
      ['Preferred day', data.get('day')],
      ['Time', data.get('time')],
      ['Time window', data.get('timeWindow')],
      ['Patient', `${data.get('firstName') || ''} ${data.get('lastName') || ''}`.trim()],
      ['Contact', `${data.get('email') || ''} · ${data.get('phone') || ''}`]
    ];
    summary.innerHTML = rows.map(([label, value]) => `
      <div><span>${label}</span><strong>${value || '—'}</strong></div>
    `).join('');
  }

  function initCookies() {
    try {
      const seen = window.localStorage.getItem('drfarah-cookie-notice');
      if (!seen && cookieBanner) cookieBanner.hidden = false;
    } catch (_e) {
      if (cookieBanner) cookieBanner.hidden = false;
    }

    const closeBanner = (accepted) => {
      try {
        window.localStorage.setItem('drfarah-cookie-notice', accepted ? 'accepted' : 'dismissed');
      } catch (_e) {}
      if (cookieBanner) cookieBanner.hidden = true;
    };

    cookieAccept?.addEventListener('click', () => closeBanner(true));
    cookieDismiss?.addEventListener('click', () => closeBanner(false));
  }

  document.querySelectorAll('[data-open-booking]').forEach(button => {
    button.addEventListener('click', () => openBooking(button.dataset.service));
  });
  document.querySelectorAll('[data-close-booking]').forEach(button => {
    button.addEventListener('click', closeBooking);
  });
  overlay?.addEventListener('click', event => {
    if (event.target === overlay) closeBooking();
  });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && overlay && !overlay.hidden) closeBooking();
  });

  moreSlotsButton?.addEventListener('click', () => {
    visibleSlots = slotList.length;
    renderSlots();
  });

  next?.addEventListener('click', () => {
    if (!validateCurrentStep()) return;

    if (currentStep < 4) {
      currentStep += 1;
      if (currentStep === 2) renderSlots();
      if (currentStep === 4) renderSummary();
      updateStep();
      return;
    }

    const consent = form.querySelector('.consent-row input');
    if (!consent.checked) {
      consent.reportValidity();
      return;
    }

    steps.forEach(step => step.classList.remove('active'));
    success.hidden = false;
    actions.hidden = true;
  });

  prev?.addEventListener('click', () => {
    if (currentStep > 1) {
      currentStep -= 1;
      updateStep();
    }
  });

  renderSlots();
  updateStep();
  initCookies();
})();
