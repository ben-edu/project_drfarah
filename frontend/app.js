(() => {
  const API_BASE = 'https://api.staging.drfarah.proxbenovh.cloud';

  // DOM references.
  const header = document.querySelector('[data-header]');
  const overlay = document.querySelector('[data-booking-overlay]');
  const form = document.querySelector('[data-booking-form]');
  const steps = [...document.querySelectorAll('[data-step]')];
  const progress = [...document.querySelectorAll('[data-progress]')];
  const next = document.querySelector('[data-next]');
  const prev = document.querySelector('[data-prev]');
  const actions = document.querySelector('[data-booking-actions]');
  const success = document.querySelector('[data-success]');
  const successDetail = document.querySelector('[data-success-detail]');
  const summary = document.querySelector('[data-summary]');
  const serviceChoices = document.getElementById('service-choices');
  const serviceError = document.getElementById('service-error');
  const datePicker = document.getElementById('date-picker');
  const slotToolbar = document.getElementById('slot-toolbar');
  const slotStatus = document.getElementById('slot-status');
  const slotGrid = document.getElementById('slot-grid');
  const showMoreBtn = document.getElementById('show-more-slots');
  const availabilityError = document.getElementById('availability-error');
  const cookieBanner = document.querySelector('[data-cookie-banner]');
  const cookieAccept = document.querySelector('[data-cookie-accept]');
  const cookieDismiss = document.querySelector('[data-cookie-dismiss]');

  // State.
  let currentStep = 1;
  let services = [];
  let selectedService = null;
  let selectedDate = null;
  let selectedSlot = null;
  let allSlots = [];
  let visibleSlotCount = 8;
  let isSubmitting = false;

  // ------------------------------------------------------------------
  // Header scroll.
  // ------------------------------------------------------------------
  const updateHeader = () => {
    header?.classList.toggle('scrolled', window.scrollY > 8);
  };
  updateHeader();
  window.addEventListener('scroll', updateHeader, { passive: true });

  // ------------------------------------------------------------------
  // Date helpers.
  // ------------------------------------------------------------------
  function todayInClinicTz() {
    // Returns today's date in America/Los_Angeles.
    const now = new Date();
    const parts = new Intl.DateTimeFormat('en-CA', {
      timeZone: 'America/Los_Angeles',
      year: 'numeric', month: '2-digit', day: '2-digit',
    }).formatToParts(now);
    const y = parts.find(p => p.type === 'year').value;
    const m = parts.find(p => p.type === 'month').value;
    const d = parts.find(p => p.type === 'day').value;
    return `${y}-${m}-${d}`;
  }

  function formatDisplayDate(isoDate) {
    const d = new Date(isoDate + 'T12:00:00');
    const opts = { weekday: 'long', month: 'long', day: 'numeric', timeZone: 'UTC' };
    return d.toLocaleDateString('en-US', opts);
  }

  function formatSlotTime(isoTimestamp) {
    const d = new Date(isoTimestamp);
    return d.toLocaleTimeString('en-US', {
      hour: 'numeric', minute: '2-digit',
      timeZone: 'America/Los_Angeles',
    });
  }

  // ------------------------------------------------------------------
  // API helpers.
  // ------------------------------------------------------------------
  async function apiFetch(path) {
    const resp = await fetch(`${API_BASE}${path}`);
    if (!resp.ok) throw new Error(`Server returned ${resp.status}`);
    return resp.json();
  }

  // ------------------------------------------------------------------
  // Booking open/close.
  // ------------------------------------------------------------------
  function openBooking(serviceCode) {
    currentStep = 1;
    selectedService = null;
    selectedDate = null;
    selectedSlot = null;
    allSlots = [];
    visibleSlotCount = 8;
    isSubmitting = false;
    success.hidden = true;
    actions.hidden = false;
    serviceError.hidden = true;
    availabilityError.hidden = true;
    slotToolbar.hidden = true;
    showMoreBtn.hidden = true;
    next.disabled = false;
    next.textContent = 'Continue';
    slotGrid.innerHTML = '';
    datePicker.innerHTML = '<p class="slot-loading">Select a date to see available times.</p>';

    loadServices().then(() => {
      // Pre-select the service if one was passed.
      if (serviceCode && services.length) {
        const match = services.find(s => s.name === serviceCode);
        if (match) {
          selectedService = match.code;
          const radio = document.querySelector(`input[name="service"][value="${match.code}"]`);
          if (radio) radio.checked = true;
        }
      }
    });

    updateStep();
    overlay.hidden = false;
    document.body.classList.add('booking-open');
    setTimeout(() => overlay.querySelector('input, select, button')?.focus(), 60);
  }

  function closeBooking() {
    overlay.hidden = true;
    document.body.classList.remove('booking-open');
  }

  // ------------------------------------------------------------------
  // Step navigation.
  // ------------------------------------------------------------------
  function updateStep() {
    steps.forEach(step => step.classList.toggle('active', Number(step.dataset.step) === currentStep));
    progress.forEach(item => item.classList.toggle('active', Number(item.dataset.progress) <= currentStep));
    prev.disabled = currentStep === 1;
    if (currentStep === 4) {
      next.textContent = isSubmitting ? 'Submitting...' : 'Submit request';
      next.disabled = isSubmitting;
    } else {
      next.textContent = 'Continue';
      next.disabled = false;
    }
  }

  function validateCurrentStep() {
    if (currentStep === 1) {
      if (!selectedService) {
        const checked = document.querySelector('input[name="service"]:checked');
        if (!checked) return false;
        selectedService = checked.value;
      }
      return true;
    }
    if (currentStep === 2) {
      if (!selectedSlot) return false;
      return true;
    }
    if (currentStep === 3) {
      const step = steps.find(s => Number(s.dataset.step) === 3);
      const required = [...step.querySelectorAll('[required]')];
      return required.every(field => {
        const ok = field.reportValidity();
        if (!ok) field.classList.add('touched');
        return ok;
      });
    }
    return true;
  }

  // ------------------------------------------------------------------
  // Service loading.
  // ------------------------------------------------------------------
  async function loadServices() {
    serviceChoices.innerHTML = '<p class="service-loading">Loading services...</p>';
    serviceError.hidden = true;

    try {
      const data = await apiFetch('/api/v1/services');
      services = data.services || [];
      if (!services.length) {
        serviceChoices.innerHTML = '<p class="service-loading">No services available right now.</p>';
        return;
      }
      renderServiceChoices();
    } catch (_err) {
      serviceError.hidden = false;
      serviceError.textContent = 'Could not load services. Please try again or call the clinic.';
      serviceChoices.innerHTML = '';
    }
  }

  function renderServiceChoices() {
    if (!services.length) return;
    const firstCode = selectedService || services[0].code;
    serviceChoices.innerHTML = services.map((s, i) => `
      <label class="choice-card">
        <input type="radio" name="service" value="${escHtml(s.code)}"
          ${s.code === firstCode ? 'checked' : ''}>
        <span><strong>${escHtml(s.name)}</strong><small>${escHtml(s.description || '')} (${s.duration_minutes} min)</small></span>
      </label>
    `).join('');

    // Track selection.
    serviceChoices.addEventListener('change', () => {
      const checked = document.querySelector('input[name="service"]:checked');
      if (checked) {
        selectedService = checked.value;
        selectedDate = null;
        selectedSlot = null;
        allSlots = [];
        visibleSlotCount = 8;
        slotGrid.innerHTML = '';
        slotToolbar.hidden = true;
        showMoreBtn.hidden = true;
        datePicker.innerHTML = '<p class="slot-loading">Select a date to see available times.</p>';
        availabilityError.hidden = true;
      }
    });

    if (!selectedService) selectedService = firstCode;
  }

  // ------------------------------------------------------------------
  // Date picker.
  // ------------------------------------------------------------------
  function renderDatePicker() {
    const today = todayInClinicTz();
    const days = [];
    for (let i = 0; i < 14; i++) {
      const d = new Date(today + 'T12:00:00');
      d.setUTCDate(d.getUTCDate() + i);
      const iso = d.toISOString().slice(0, 10);
      const label = i === 0 ? 'Today' : i === 1 ? 'Tomorrow' : formatDisplayDate(iso);
      days.push({ iso, label });
    }

    datePicker.innerHTML = days.map(d => `
      <button type="button" class="date-chip${d.iso === selectedDate ? ' active' : ''}"
        data-date="${d.iso}" aria-pressed="${d.iso === selectedDate}">
        <small>${d.label.split(',')[0]}</small>
        <strong>${d.label.split(',')[1] ? d.label.split(',')[1].trim() : d.label}</strong>
      </button>
    `).join('');

    datePicker.querySelectorAll('.date-chip').forEach(chip => {
      chip.addEventListener('click', () => {
        selectedDate = chip.dataset.date;
        selectedSlot = null;
        allSlots = [];
        visibleSlotCount = 8;
        renderDatePicker();
        loadAvailability();
      });
    });
  }

  // ------------------------------------------------------------------
  // Availability loading.
  // ------------------------------------------------------------------
  async function loadAvailability() {
    slotGrid.innerHTML = '<p class="slot-loading">Loading available times...</p>';
    slotToolbar.hidden = false;
    slotStatus.textContent = 'Loading...';
    showMoreBtn.hidden = true;
    availabilityError.hidden = true;

    if (!selectedService || !selectedDate) {
      slotStatus.textContent = 'Select a date.';
      slotGrid.innerHTML = '';
      return;
    }

    try {
      const svc = services.find(s => s.code === selectedService);
      const endDate = selectedDate; // Single-day queries by default.
      const data = await apiFetch(
        `/api/v1/availability?service_code=${encodeURIComponent(selectedService)}&start_date=${selectedDate}&end_date=${endDate}`
      );
      allSlots = data.slots || [];
      visibleSlotCount = Math.min(8, allSlots.length);
      renderSlots();
    } catch (err) {
      availabilityError.hidden = false;
      availabilityError.textContent = 'Could not load availability. Please try another date.';
      slotStatus.textContent = 'Error loading slots.';
      slotGrid.innerHTML = '';
      allSlots = [];
    }
  }

  function renderSlots() {
    if (!allSlots.length) {
      slotGrid.innerHTML = '<p class="slot-loading">No available times for this date. Please try another day.</p>';
      slotStatus.textContent = 'No slots available.';
      showMoreBtn.hidden = true;
      return;
    }

    slotStatus.textContent = `${allSlots.length} slot${allSlots.length > 1 ? 's' : ''} available`;
    showMoreBtn.hidden = visibleSlotCount >= allSlots.length;

    const visible = allSlots.slice(0, visibleSlotCount);
    const savedStartsAt = selectedSlot ? selectedSlot.starts_at : null;

    slotGrid.innerHTML = visible.map(s => {
      const timeLabel = formatSlotTime(s.starts_at);
      const isChecked = s.starts_at === savedStartsAt;
      return `
        <label>
          <input type="radio" name="slot" value="${escHtml(s.starts_at)}" ${isChecked ? 'checked' : ''}>
          <span>${escHtml(timeLabel)}</span>
        </label>
      `;
    }).join('');

    // Track slot selection.
    slotGrid.querySelectorAll('input[name="slot"]').forEach(input => {
      input.addEventListener('change', () => {
        const match = allSlots.find(s => s.starts_at === input.value);
        selectedSlot = match || null;
      });
    });

    // Restore selection if available.
    if (savedStartsAt && !visible.some(s => s.starts_at === savedStartsAt)) {
      selectedSlot = null;
    }

    if (!selectedSlot && visible.length) {
      selectedSlot = visible[0];
    }
  }

  // ------------------------------------------------------------------
  // Summary.
  // ------------------------------------------------------------------
  function renderSummary() {
    const svc = services.find(s => s.code === selectedService);
    const svcName = svc ? svc.name : selectedService || '—';

    const fv = (sel) => {
      const el = form.querySelector(sel);
      return el ? el.value : '—';
    };

    const dateLabel = selectedDate ? formatDisplayDate(selectedDate) : '—';
    const timeLabel = selectedSlot ? formatSlotTime(selectedSlot.starts_at) : '—';

    const rows = [
      ['Care', svcName],
      ['Date', dateLabel],
      ['Time', timeLabel],
      ['Patient', `${fv('[name="firstName"]')} ${fv('[name="lastName"]')}`.trim()],
      ['Contact', `${fv('[name="email"]')} · ${fv('[name="phone"]')}`],
    ];
    summary.innerHTML = rows.map(([label, value]) => `
      <div><span>${label}</span><strong>${escHtml(value)}</strong></div>
    `).join('');
  }

  // ------------------------------------------------------------------
  // Submit.
  // ------------------------------------------------------------------
  async function submitAppointment() {
    if (isSubmitting) return;
    isSubmitting = true;
    updateStep();

    const fv = (sel) => {
      const el = form.querySelector(sel);
      return el ? el.value.trim() : '';
    };

    const payload = {
      service_code: selectedService,
      starts_at: selectedSlot.starts_at,
      first_name: fv('[name="firstName"]'),
      last_name: fv('[name="lastName"]'),
      email: fv('[name="email"]'),
      phone: fv('[name="phone"]'),
      reason_category: fv('[name="reason"]'),
    };

    try {
      const resp = await fetch(`${API_BASE}/api/v1/appointments`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });

      if (resp.status === 409) {
        // Slot conflict — refresh availability.
        steps.forEach(step => step.classList.remove('active'));
        success.hidden = false;
        successDetail.textContent = 'This time slot was just taken by another patient. Please select a different time.';
        actions.hidden = true;
        isSubmitting = false;
        updateStep();
        return;
      }

      if (!resp.ok) {
        const errText = await resp.text().catch(() => '');
        throw new Error(errText || `Server returned ${resp.status}`);
      }

      const result = await resp.json();
      const svc = services.find(s => s.code === selectedService);
      const svcName = svc ? svc.name : selectedService;
      const timeLabel = selectedSlot ? formatSlotTime(selectedSlot.starts_at) : '';
      const dateLabel = selectedDate ? formatDisplayDate(selectedDate) : '';

      successDetail.textContent = `Reference #${result.id} — ${result.first_name}, your ${svcName.toLowerCase()} appointment is requested for ${dateLabel} at ${timeLabel}. The clinic will confirm your appointment.`;

      steps.forEach(step => step.classList.remove('active'));
      success.hidden = false;
      actions.hidden = true;
    } catch (_err) {
      steps.forEach(step => step.classList.remove('active'));
      success.hidden = false;
      successDetail.textContent = 'Your request could not be submitted right now. Please try again or call the clinic at (310) 555-0189.';
      actions.hidden = true;
    } finally {
      isSubmitting = false;
      updateStep();
    }
  }

  // ------------------------------------------------------------------
  // Cookies.
  // ------------------------------------------------------------------
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

  // ------------------------------------------------------------------
  // HTML escaping.
  // ------------------------------------------------------------------
  function escHtml(str) {
    const el = document.createElement('span');
    el.textContent = str;
    return el.innerHTML;
  }

  // ------------------------------------------------------------------
  // Event listeners.
  // ------------------------------------------------------------------
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

  showMoreBtn?.addEventListener('click', () => {
    visibleSlotCount = allSlots.length;
    renderSlots();
  });

  next?.addEventListener('click', async () => {
    if (isSubmitting) return;

    if (!validateCurrentStep()) return;

    if (currentStep < 4) {
      currentStep += 1;
      if (currentStep === 2) {
        renderDatePicker();
        if (selectedDate) loadAvailability();
      }
      if (currentStep === 4) renderSummary();
      updateStep();
      return;
    }

    // Step 4 — submit.
    const consent = form.querySelector('.consent-row input');
    if (consent && !consent.checked) {
      consent.reportValidity();
      return;
    }

    await submitAppointment();
  });

  prev?.addEventListener('click', () => {
    if (currentStep > 1) {
      currentStep -= 1;
      updateStep();
    }
  });

  // Init.
  slotToolbar.hidden = true;
  showMoreBtn.hidden = true;
  updateStep();
  initCookies();
})();
