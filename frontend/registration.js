/* Online patient registration — save/resume/submit without browser persistence of PHI. */
(function () {
  'use strict';

  var API_BASE = (function () {
    var h = location.hostname;

    // Final domains.
    if (h === 'staging.drfarahvipurgentcare.com') {
      return 'https://api-staging.drfarahvipurgentcare.com/api/v1';
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

    if (h === 'localhost' || h === '127.0.0.1') {
      return 'http://localhost:8000/api/v1';
    }

    return 'https://api-staging.drfarahvipurgentcare.com/api/v1';
  })();

  var form = document.getElementById('registrationForm');
  if (!form) return;

  var reference = null;
  var token = null;
  var message = document.getElementById('registrationMessage');
  var credentials = document.getElementById('draftCredentials');
  var draftReference = document.getElementById('draftReference');
  var draftToken = document.getElementById('draftToken');

  function value(id) {
    var el = document.getElementById(id);
    return el ? el.value.trim() : '';
  }

  function nullable(v) { return v ? v : null; }

  function payload() {
    return {
      appointment_reference: nullable(value('appointment_reference')),
      first_name: nullable(value('first_name')),
      last_name: nullable(value('last_name')),
      date_of_birth: nullable(value('date_of_birth')),
      email: nullable(value('email')),
      phone: nullable(value('phone')),
      address_line1: nullable(value('address_line1')),
      address_line2: nullable(value('address_line2')),
      city: nullable(value('city')),
      state: nullable(value('state')),
      postal_code: nullable(value('postal_code')),
      emergency_contact_name: nullable(value('emergency_contact_name')),
      emergency_contact_phone: nullable(value('emergency_contact_phone')),
      privacy_acknowledged: document.getElementById('privacy_acknowledged').checked
    };
  }

  function setMessage(text, error) {
    message.className = 'form__msg ' + (error ? 'is-err' : 'is-ok');
    message.textContent = text;
  }

  function setResumeMessage(text, error) {
    var el = document.getElementById('resumeMessage');
    el.className = 'form__msg ' + (error ? 'is-err' : 'is-ok');
    el.textContent = text;
  }

  function showCredentials() {
    credentials.hidden = false;
    draftReference.textContent = reference;
    draftToken.textContent = token;
  }

  function request(url, options) {
    options = options || {};
    options.headers = options.headers || {};
    options.headers.Accept = 'application/json';
    if (options.body) options.headers['Content-Type'] = 'application/json';
    if (token) options.headers['X-Registration-Token'] = token;
    return fetch(API_BASE + url, options).then(function (res) {
      return res.text().then(function (text) {
        var data = {};
        try { data = text ? JSON.parse(text) : {}; } catch (_) {}
        if (!res.ok) {
          var detail = data.detail;
          if (typeof detail === 'object' && detail.message) detail = detail.message + (detail.missing ? ': ' + detail.missing.join(', ') : '');
          throw new Error(detail || 'Request failed (' + res.status + ')');
        }
        return data;
      });
    });
  }

  function validateCoreIdentity() {
    var required = [
      ['first_name', 'First name'],
      ['last_name', 'Last name'],
      ['email', 'Email'],
      ['phone', 'Phone']
    ];
    var missing = [];
    required.forEach(function (item) {
      if (!value(item[0])) missing.push(item[1]);
    });
    if (missing.length) {
      throw new Error('Before saving a draft, please complete: ' + missing.join(', ') + '.');
    }
  }

  function ensureDraft() {
    if (!reference || !token) validateCoreIdentity();
    if (reference && token) {
      return request('/patient-registrations/' + encodeURIComponent(reference), {
        method: 'PATCH',
        body: JSON.stringify(payload())
      });
    }
    return request('/patient-registrations', {
      method: 'POST',
      body: JSON.stringify(payload())
    }).then(function (data) {
      reference = data.public_reference;
      token = data.resume_token;
      showCredentials();
      return data;
    });
  }

  document.getElementById('saveDraft').addEventListener('click', function () {
    setMessage('Saving draft…', false);
    ensureDraft().then(function () {
      showCredentials();
      setMessage('Draft saved. Keep your registration reference and private resume code so you can continue later.', false);
    }).catch(function (err) {
      setMessage(err.message || 'Could not save the draft.', true);
    });
  });

  form.addEventListener('submit', function (event) {
    event.preventDefault();
    setMessage('Saving and submitting…', false);
    ensureDraft().then(function () {
      return request('/patient-registrations/' + encodeURIComponent(reference) + '/submit', { method: 'POST' });
    }).then(function () {
      setMessage('Registration submitted. Reference: ' + reference + '. The clinic can now review the submitted registration.', false);
      form.querySelectorAll('input,button').forEach(function (el) { el.disabled = true; });
    }).catch(function (err) {
      setMessage(err.message || 'Could not submit the registration.', true);
    });
  });

  document.getElementById('resumeRegistration').addEventListener('click', function () {
    var ref = document.getElementById('resumeReference').value.trim().toUpperCase();
    var tok = document.getElementById('resumeToken').value.trim();
    if (!ref || !tok) {
      setResumeMessage('Enter both the registration reference and private resume code.', true);
      return;
    }
    reference = ref;
    token = tok;
    setResumeMessage('Loading saved draft…', false);
    request('/patient-registrations/' + encodeURIComponent(reference), { method: 'GET' }).then(function (data) {
      Object.keys(data).forEach(function (key) {
        var el = document.getElementById(key);
        if (!el) return;
        if (el.type === 'checkbox') el.checked = !!data[key];
        else if (data[key] !== null && data[key] !== undefined) el.value = data[key];
      });
      showCredentials();
      setResumeMessage('Draft loaded.', false);
      form.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }).catch(function (err) {
      reference = null;
      token = null;
      setResumeMessage(err.message || 'Could not resume this registration.', true);
    });
  });

  var params = new URLSearchParams(location.search);
  var apptRef = params.get('appointment_reference');
  if (apptRef) document.getElementById('appointment_reference').value = apptRef.slice(0, 64);
})();