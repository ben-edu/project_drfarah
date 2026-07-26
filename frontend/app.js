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
  let currentStep = 1;

  const updateHeader = () => {
    header?.classList.toggle('scrolled', window.scrollY > 24);
  };
  updateHeader();
  window.addEventListener('scroll', updateHeader, { passive: true });

  function setService(value) {
    if (!value) return;
    const input = form.querySelector(`input[name="service"][value="${CSS.escape(value)}"]`);
    if (input) input.checked = true;
  }

  function openBooking(service) {
    setService(service);
    currentStep = 1;
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

  document.querySelectorAll('[data-open-booking]').forEach(button => {
    button.addEventListener('click', () => openBooking(button.dataset.service));
  });
  document.querySelectorAll('[data-close-booking]').forEach(button => {
    button.addEventListener('click', closeBooking);
  });
  overlay.addEventListener('click', event => {
    if (event.target === overlay) closeBooking();
  });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && !overlay.hidden) closeBooking();
  });

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
      ['Patient', `${data.get('firstName') || ''} ${data.get('lastName') || ''}`.trim()],
      ['Contact', `${data.get('email') || ''} · ${data.get('phone') || ''}`]
    ];
    summary.innerHTML = rows.map(([label, value]) => `
      <div><span>${label}</span><strong>${value || '—'}</strong></div>
    `).join('');
  }

  next.addEventListener('click', () => {
    if (!validateCurrentStep()) return;

    if (currentStep < 4) {
      currentStep += 1;
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

  prev.addEventListener('click', () => {
    if (currentStep > 1) {
      currentStep -= 1;
      updateStep();
    }
  });
})();
