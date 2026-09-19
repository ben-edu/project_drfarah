/* Booking wizard — talks to the real appointments API.
   Flow: choose service -> load availability -> pick slot -> details -> confirm.
   Query parameters supported:
     ?service=<service-code>    preselects a service when it exists in the API
     ?reason=<reason-category>  prefills the structured reason category
     ?source=<source>           first-party acquisition marker
     ?partner=<partner-code>    hotel/referral partner attribution marker
     ?utm_source=<source>       marketing source attribution marker
*/
(function () {
  'use strict';

  var API_BASE = (function () {
    var h = location.hostname;

    // Final domains.
    if (h === 'staging.drfarahvipurgentcare.com') {
      return 'https://api.staging.drfarahvipurgentcare.com/api/v1';
    }
    if (h === 'drfarahvipurgentcare.com' || h === 'www.drfarahvipurgentcare.com') {
      return 'https://api.drfarahvipurgentcare.com/api/v1';
    }

    // Temporary domains kept during the controlled migration window.
    if (h === 'staging.drfarah.proxbenovh.cloud') {
      return 'https://api.staging.drfarah.proxbenovh.cloud/api/v1';
    }
    if (h === 'drfarah.proxbenovh.cloud' || h === 'www.drfarah.proxbenovh.cloud') {
      return 'https://api.drfarah.proxbenovh.cloud/api/v1';
    }

    // Local/unknown hosts intentionally use staging rather than production.
    return 'https://api.staging.drfarahvipurgentcare.com/api/v1';
  })();

  var CLINIC_TZ = 'America/Los_Angeles';
  var params = new URLSearchParams(window.location.search);

  function safeMarker(value) {
    if (!value) return '';
    return String(value).toLowerCase().replace(/[^a-z0-9._:-]/g, '-').replace(/-+/g, '-').slice(0, 48);
  }

  /* appointments.source is currently VARCHAR(32) in the deployed schema.
     Keep browser-generated attribution markers inside that real DB boundary. */
  function attributionSource() {
    var partner = safeMarker(params.get('partner'));
    if (partner) return ('hotel:' + partner).slice(0, 32);
    var source = safeMarker(params.get('source'));
    if (source) return source.slice(0, 32);
    var utm = safeMarker(params.get('utm_source'));
    if (utm) return ('utm:' + utm).slice(0, 32);
    return 'web';
  }

  var requestedService = safeMarker(params.get('service'));
  var requestedReason = params.get('reason') || '';

  var state = {
    step: 1,
    serviceCode: null,
    serviceName: null,
    slotStart: null,
    slotLabel: null,
    source: attributionSource()
  };

  var form = document.getElementById('bookingForm');
  if (!form) return;

  var panels = form.querySelectorAll('.wizard-panel');
  var stepsEls = document.querySelectorAll('#wizardSteps li');

  function show(step) {
    state.step = step;
    panels.forEach(function (p) {
      p.classList.toggle('is-active', Number(p.dataset.panel) === step);
    });
    stepsEls.forEach(function (li) {
      var n = Number(li.dataset.step);
      li.classList.toggle('is-active', n === step);
      li.classList.toggle('is-done', n < step);
    });
    window.scrollTo({ top: form.getBoundingClientRect().top + window.scrollY - 90, behavior: 'smooth' });
  }

  function fmtDay(d) {
    return new Intl.DateTimeFormat('en-US', {
      weekday: 'long', month: 'long', day: 'numeric', timeZone: CLINIC_TZ,
    }).format(d);
  }

  function fmtTime(d) {
    return new Intl.DateTimeFormat('en-US', {
      hour: 'numeric', minute: '2-digit', timeZone: CLINIC_TZ,
    }).format(d);
  }

  function isoDate(d) {
    return d.toISOString().slice(0, 10);
  }

  var serviceChoices = document.getElementById('serviceChoices');
  var serviceLoading = document.getElementById('serviceLoading');
  var serviceError = document.getElementById('serviceError');
  var toStep2 = document.getElementById('toStep2');

  function selectServiceInput(input, svc) {
    input.checked = true;
    state.serviceCode = svc.code;
    state.serviceName = svc.name;
    toStep2.disabled = false;
  }

  function loadServices() {
    fetch(API_BASE + '/services', { headers: { 'Accept': 'application/json' } })
      .then(function (r) { if (!r.ok) throw new Error('services ' + r.status); return r.json(); })
      .then(function (data) {
        var services = (data && data.services) || [];
        if (!services.length) throw new Error('no services');
        if (serviceLoading) serviceLoading.remove();

        var matchedRequestedService = false;

        services.forEach(function (svc) {
          var id = 'svc_' + svc.code;
          var label = document.createElement('label');
          label.className = 'choice';
          label.innerHTML =
            '<input type="radio" name="service" value="' + esc(svc.code) + '" id="' + id + '">' +
            '<span>' +
              '<span class="choice__title">' + esc(svc.name) + '</span>' +
              (svc.description ? '<span class="choice__desc">' + esc(svc.description) + '</span>' : '') +
              (svc.duration_minutes ? '<span class="choice__meta">' + svc.duration_minutes + ' min</span>' : '') +
            '</span>';

          serviceChoices.appendChild(label);
          var input = label.querySelector('input');

          input.addEventListener('change', function () {
            state.serviceCode = svc.code;
            state.serviceName = svc.name;
            toStep2.disabled = false;
          });

          if (requestedService && svc.code === requestedService) {
            selectServiceInput(input, svc);
            matchedRequestedService = true;
          }
        });

        /* A stale/unknown service query parameter never silently maps to
           another service. The user must choose an API-configured service. */
        if (requestedService && !matchedRequestedService) {
          requestedService = '';
        }
      })
      .catch(function () {
        if (serviceLoading) serviceLoading.remove();
        serviceError.classList.add('is-err');
        serviceError.style.display = 'block';
      });
  }

  var slotsArea = document.getElementById('slotsArea');
  var slotsError = document.getElementById('slotsError');
  var toStep3 = document.getElementById('toStep3');

  function loadAvailability() {
    slotsArea.innerHTML = '<p class="booking-loading">Loading available times…</p>';
    slotsError.style.display = 'none';
    toStep3.disabled = true;
    state.slotStart = null;

    var start = new Date();
    start.setDate(start.getDate() + 1);
    var end = new Date();
    end.setDate(end.getDate() + 14);

    var url = API_BASE + '/availability?service_code=' + encodeURIComponent(state.serviceCode) +
      '&start_date=' + isoDate(start) + '&end_date=' + isoDate(end);

    fetch(url, { headers: { 'Accept': 'application/json' } })
      .then(function (r) { if (!r.ok) throw new Error('availability ' + r.status); return r.json(); })
      .then(function (data) {
        var slots = (data && data.slots) || [];
        if (!slots.length) throw new Error('no slots');
        renderSlots(slots);
      })
      .catch(function () {
        slotsArea.innerHTML = '';
        slotsError.style.display = 'block';
      });
  }

  function renderSlots(slots) {
    slotsArea.innerHTML = '';
    var groups = {};
    var order = [];

    slots.forEach(function (s) {
      var d = new Date(s.starts_at);
      var key = fmtDay(d);
      if (!groups[key]) { groups[key] = []; order.push(key); }
      groups[key].push({ iso: s.starts_at, date: d });
    });

    order.forEach(function (day) {
      var h = document.createElement('p');
      h.className = 'slot-day';
      h.textContent = day;
      slotsArea.appendChild(h);

      var grid = document.createElement('div');
      grid.className = 'slots';

      groups[day].forEach(function (item) {
        var btn = document.createElement('button');
        btn.type = 'button';
        btn.className = 'slot';
        btn.textContent = fmtTime(item.date);
        btn.addEventListener('click', function () {
          slotsArea.querySelectorAll('.slot').forEach(function (b) { b.classList.remove('is-selected'); });
          btn.classList.add('is-selected');
          state.slotStart = item.iso;
          state.slotLabel = day + ' at ' + fmtTime(item.date);
          toStep3.disabled = false;
        });
        grid.appendChild(btn);
      });

      slotsArea.appendChild(grid);
    });
  }

  function prefillReason() {
    if (!requestedReason) return;
    var reason = document.getElementById('reason');
    if (!reason) return;
    var options = Array.prototype.slice.call(reason.options);
    var match = options.find(function (opt) { return opt.value === requestedReason || opt.text === requestedReason; });
    if (match) reason.value = match.value;
  }

  function buildRecap() {
    var list = document.getElementById('recapList');
    var rows = [
      ['Care', state.serviceName || ''],
      ['Time', state.slotLabel || ''],
      ['Name', val('firstName') + ' ' + val('lastName')],
      ['Email', val('email')],
      ['Phone', val('phone')],
      ['Reason', val('reason')],
    ];
    list.innerHTML = rows.map(function (r) {
      return '<div><dt>' + esc(r[0]) + '</dt><dd>' + esc(r[1]) + '</dd></div>';
    }).join('');
  }

  var submitError = document.getElementById('submitError');
  var confirmBtn = document.getElementById('confirmBtn');

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    submitError.style.display = 'none';
    confirmBtn.disabled = true;
    confirmBtn.textContent = 'Confirming…';

    var payload = {
      service_code: state.serviceCode,
      starts_at: state.slotStart,
      first_name: val('firstName'),
      last_name: val('lastName'),
      email: val('email'),
      phone: val('phone'),
      reason_category: val('reason'),
      source: state.source,
    };

    fetch(API_BASE + '/appointments', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
      body: JSON.stringify(payload),
    })
      .then(function (r) {
        if (r.status === 201) return r.json();
        if (r.status === 409) { var e409 = new Error('taken'); e409.code = 409; throw e409; }
        if (r.status === 422) { var e422 = new Error('invalid'); e422.code = 422; throw e422; }
        throw new Error('http ' + r.status);
      })
      .then(function (data) {
        var ref = data && (data.public_reference || data.id);
        document.getElementById('successRef').textContent = ref ? ('Reference: ' + ref) : '';
        var registrationLink = document.querySelector('a[href="/patient-registration"]');
        if (registrationLink && ref) {
          registrationLink.href = '/patient-registration?appointment_reference=' + encodeURIComponent(String(ref));
        }
        show(5);
      })
      .catch(function (err) {
        confirmBtn.disabled = false;
        confirmBtn.textContent = 'Confirm appointment';
        if (err.code === 409) {
          submitError.textContent = 'That time was just taken. Please choose another available time.';
          submitError.style.display = 'block';
          show(2);
          loadAvailability();
        } else if (err.code === 422) {
          submitError.textContent = 'Some details need checking. Please review your information and try again.';
          submitError.style.display = 'block';
        } else {
          submitError.textContent = 'We couldn\u2019t complete your booking. Please try again, or call 310-467-0101.';
          submitError.style.display = 'block';
        }
      });
  });

  form.addEventListener('click', function (e) {
    var next = e.target.closest('[data-next]');
    var back = e.target.closest('[data-back]');
    if (next) {
      if (state.step === 1 && state.serviceCode) { show(2); loadAvailability(); }
      else if (state.step === 2 && state.slotStart) { show(3); }
      else if (state.step === 3) { if (validateDetails()) { buildRecap(); show(4); } }
    }
    if (back) { show(Math.max(1, state.step - 1)); }
  });

  function validateDetails() {
    var required = ['firstName', 'lastName', 'email', 'phone', 'reason'];
    var ok = true;
    required.forEach(function (id) {
      var el = document.getElementById(id);
      if (!el.value.trim()) { el.style.borderColor = 'var(--gold-deep)'; ok = false; }
      else { el.style.borderColor = ''; }
    });

    var email = document.getElementById('email');
    if (email.value && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value)) {
      email.style.borderColor = 'var(--gold-deep)';
      ok = false;
    }

    var consent = document.getElementById('consent');
    if (!consent.checked) {
      ok = false;
      consent.parentElement.style.color = 'var(--gold-deep)';
    } else {
      consent.parentElement.style.color = '';
    }

    return ok;
  }

  function val(id) {
    var el = document.getElementById(id);
    return el ? el.value.trim() : '';
  }

  function esc(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

  prefillReason();
  loadServices();
})();