/**
 * Dr. Farah Admin SPA — application logic.
 * Keycloak Authorization Code + PKCE S256 → Bearer token → admin API.
 * Tokens stay in memory (keycloak-js manages this); never written to localStorage.
 */
(function () {
  'use strict';

  /* ── Config ── */
  var cfg = window.ADMIN_CONFIG || {};
  var KEYCLOAK_URL = cfg.KEYCLOAK_URL;
  var REALM        = cfg.REALM;
  var CLIENT_ID    = cfg.CLIENT_ID;
  var API_BASE     = cfg.API_BASE;

  if (!KEYCLOAK_URL || !REALM || !CLIENT_ID || !API_BASE) {
    alert('Admin SPA is misconfigured — missing required config values. Check config.js.');
    return;
  }

  /* ── DOM refs — auth ── */
  var $loggedOut   = document.getElementById('logged-out');
  var $loggedIn    = document.getElementById('logged-in');
  var $btnLogin    = document.getElementById('btn-login');
  var $btnLogout   = document.getElementById('btn-logout');
  var $loginError  = document.getElementById('login-error');
  var $loading     = document.getElementById('loading-indicator');
  var $identity    = document.getElementById('identity-panel');
  var $apiError    = document.getElementById('api-error');

  /* ── DOM refs — appointments ── */
  var $aptSection   = document.getElementById('appointments-section');
  var $aptLoading   = document.getElementById('apt-loading');
  var $aptError     = document.getElementById('apt-error');
  var $aptEmpty     = document.getElementById('apt-empty');
  var $aptTableWrap = document.getElementById('apt-table-wrap');
  var $aptTbody     = document.getElementById('apt-tbody');
  var $aptPager     = document.getElementById('apt-pager');
  var $aptDetail    = document.getElementById('apt-detail');
  var $aptDetailBody = document.getElementById('apt-detail-body');
  var $detailStatus = document.getElementById('detail-status-select');
  var $btnStatusUpd = document.getElementById('btn-status-update');
  var $btnDetailClose = document.getElementById('btn-detail-close');
  var $filterStatus   = document.getElementById('filter-status');
  var $filterQ        = document.getElementById('filter-q');
  var $filterDateFrom = document.getElementById('filter-date-from');
  var $filterDateTo   = document.getElementById('filter-date-to');
  var $btnRefresh     = document.getElementById('btn-refresh');

  /* ── DOM refs — patient registrations ── */
  var $regSection   = document.getElementById('registrations-section');
  var $regLoading   = document.getElementById('reg-loading');
  var $regError     = document.getElementById('reg-error');
  var $regEmpty     = document.getElementById('reg-empty');
  var $regTableWrap = document.getElementById('reg-table-wrap');
  var $regTbody     = document.getElementById('reg-tbody');
  var $regDetail    = document.getElementById('reg-detail');
  var $regDetailBody = document.getElementById('reg-detail-body');
  var $regDetailClose = document.getElementById('reg-detail-close');
  var $regFilterStatus = document.getElementById('reg-filter-status');
  var $regFilterQ = document.getElementById('reg-filter-q');
  var $regRefresh = document.getElementById('reg-refresh');

  /* ── Appointment state ── */
  var aptState = {
    offset: 0,
    limit: 25,
    total: 0,
    currentId: null
  };

  /* ── Helpers ── */
  function show(el) { el.classList.remove('hidden'); }
  function hide(el) { el.classList.add('hidden'); }

  function showLoginError(msg) {
    $loginError.textContent = msg;
    show($loginError);
  }

  function showApiError(msg) {
    $apiError.textContent = msg;
    show($apiError);
  }

  function showAptError(msg) {
    $aptError.textContent = msg;
    show($aptError);
  }

  function showRegError(msg) {
    $regError.textContent = msg;
    show($regError);
  }

  function clearErrors() {
    hide($loginError);
    hide($apiError);
    hide($aptError);
    if ($regError) hide($regError);
  }

  function escapeHtml(str) {
    var div = document.createElement('div');
    div.appendChild(document.createTextNode(str));
    return div.innerHTML;
  }

  /* ── Date formatting (America/Los_Angeles) ── */
  var dateFormatter = new Intl.DateTimeFormat('en-US', {
    timeZone: 'America/Los_Angeles',
    dateStyle: 'medium',
    timeStyle: 'short'
  });

  function formatDate(isoStr) {
    if (!isoStr) return '—';
    return dateFormatter.format(new Date(isoStr));
  }

  /* ── Status helpers ── */
  var STATUS_LABELS = {
    pending: 'Pending',
    confirmed: 'Confirmed',
    cancelled: 'Cancelled',
    completed: 'Completed',
    no_show: 'No Show'
  };

  function statusLabel(s) {
    return STATUS_LABELS[s] || s;
  }

  function statusBadge(s) {
    return '<span class="badge badge-' + escapeHtml(s) + '">' + escapeHtml(statusLabel(s)) + '</span>';
  }

  /* ── API fetch helper — always refreshes token, handles 401/403 ── */
  function apiFetch(url, options) {
    options = options || {};
    return keycloak.updateToken(30).then(function () {
      var headers = {
        'Authorization': 'Bearer ' + keycloak.token,
        'Accept': 'application/json'
      };
      if (options.body) {
        headers['Content-Type'] = 'application/json';
      }
      if (options.headers) {
        Object.keys(options.headers).forEach(function (k) {
          headers[k] = options.headers[k];
        });
      }
      return fetch(url, {
        method: options.method || 'GET',
        headers: headers,
        body: options.body || undefined
      });
    }).then(function (res) {
      if (res.status === 401) {
        keycloak.login();
        throw new Error('Session expired. Please sign in again.');
      }
      if (res.status === 403) {
        throw new Error("You don't have permission to access this resource.");
      }
      if (!res.ok) {
        return res.text().then(function (text) {
          var msg = 'Server error (' + res.status + ')';
          try {
            var body = JSON.parse(text);
            msg = body.detail || body.message || msg;
          } catch (_) { /* use default msg */ }
          throw new Error(msg);
        });
      }
      return res.json();
    });
  }

  /* ── Render identity from /admin/me response ── */
  function renderIdentity(data) {
    hide($loading);

    var roles = data.roles || [];
    var rolesHtml = '';
    if (Array.isArray(roles) && roles.length > 0) {
      rolesHtml = '<div class="roles">' +
        roles.map(function (r) {
          return '<span class="role-tag">' + escapeHtml(String(r)) + '</span>';
        }).join('') +
        '</div>';
    } else {
      rolesHtml = '<span class="no-roles">No roles assigned</span>';
    }

    $identity.innerHTML =
      '<dt>Username</dt>' +
      '<dd>' + escapeHtml(data.preferred_username || '—') + '</dd>' +
      '<dt>Email</dt>' +
      '<dd>' + escapeHtml(data.email || '—') + '</dd>' +
      '<dt>Roles</dt>' +
      '<dd>' + rolesHtml + '</dd>';

    show($identity);

    // Show staff work queues and load data.
    show($aptSection);
    show($regSection);
    loadAppointments();
    loadRegistrations();
  }

  /* ── Call /admin/me ── */
  function loadIdentity() {
    hide($identity);
    hide($apiError);
    show($loading);

    apiFetch(API_BASE + '/admin/me').then(function (data) {
      renderIdentity(data);
    }).catch(function (err) {
      hide($loading);
      showApiError(err.message || 'Failed to load identity.');
    });
  }

  /* ════════════════════════════════════════════════════════════════
     Appointments — load, render, paginate
     ════════════════════════════════════════════════════════════════ */

  function loadAppointments() {
    hide($aptError);
    hide($aptEmpty);
    hide($aptTableWrap);
    hide($aptPager);
    hide($aptDetail);
    show($aptLoading);

    var params = [
      'limit=' + aptState.limit,
      'offset=' + aptState.offset
    ];

    var statusVal = $filterStatus.value;
    if (statusVal) {
      params.push('status=' + encodeURIComponent(statusVal));
    }

    var qVal = $filterQ.value.trim();
    if (qVal) {
      params.push('q=' + encodeURIComponent(qVal));
    }

    var dateFrom = $filterDateFrom.value;
    if (dateFrom) {
      params.push('date_from=' + encodeURIComponent(dateFrom));
    }

    var dateTo = $filterDateTo.value;
    if (dateTo) {
      params.push('date_to=' + encodeURIComponent(dateTo));
    }

    var url = API_BASE + '/admin/appointments?' + params.join('&');

    apiFetch(url).then(function (data) {
      hide($aptLoading);
      aptState.total = data.total || 0;
      var items = data.items || [];
      renderRows(items);
      renderPager();
    }).catch(function (err) {
      hide($aptLoading);
      showAptError(err.message || 'Failed to load appointments.');
    });
  }

  function renderRows(items) {
    $aptTbody.innerHTML = '';

    if (!items || items.length === 0) {
      show($aptEmpty);
      hide($aptTableWrap);
      hide($aptPager);
      return;
    }

    hide($aptEmpty);
    show($aptTableWrap);
    show($aptPager);

    items.forEach(function (apt) {
      var tr = document.createElement('tr');
      tr.setAttribute('data-id', apt.id);
      tr.setAttribute('data-status', apt.status || '');
      tr.innerHTML =
        '<td>' + formatDate(apt.starts_at) + '</td>' +
        '<td>' + escapeHtml((apt.first_name || '') + ' ' + (apt.last_name || '')) + '</td>' +
        '<td>' + escapeHtml(apt.service_name || apt.service_code || '—') + '</td>' +
        '<td>' + escapeHtml(apt.email || apt.phone || '—') + '</td>' +
        '<td>' + escapeHtml(apt.reason_category || '—') + '</td>' +
        '<td>' + statusBadge(apt.status) + '</td>' +
        '<td style="color:var(--muted); font-size:0.8rem;">&rarr;</td>';
      $aptTbody.appendChild(tr);
    });
  }

  /* ── Row click — delegate on tbody ── */
  $aptTbody.addEventListener('click', function (e) {
    var tr = e.target.closest('tr');
    if (!tr) return;
    var id = tr.getAttribute('data-id');
    if (id) showDetail(id);
  });

  /* ── Pager ── */
  function renderPager() {
    var total = aptState.total;
    var limit = aptState.limit;
    var offset = aptState.offset;
    var start = total === 0 ? 0 : offset + 1;
    var end = Math.min(offset + limit, total);

    $aptPager.innerHTML = '';

    var btnPrev = document.createElement('button');
    btnPrev.className = 'btn btn-ghost btn-sm';
    btnPrev.textContent = '← Prev';
    btnPrev.disabled = offset === 0;
    btnPrev.addEventListener('click', function () {
      if (offset > 0) {
        aptState.offset = Math.max(0, offset - limit);
        loadAppointments();
      }
    });

    var info = document.createElement('span');
    info.textContent = 'Showing ' + start + '–' + end + ' of ' + total;

    var btnNext = document.createElement('button');
    btnNext.className = 'btn btn-ghost btn-sm';
    btnNext.textContent = 'Next →';
    btnNext.disabled = offset + limit >= total;
    btnNext.addEventListener('click', function () {
      if (offset + limit < total) {
        aptState.offset = offset + limit;
        loadAppointments();
      }
    });

    $aptPager.appendChild(btnPrev);
    $aptPager.appendChild(info);
    $aptPager.appendChild(btnNext);
  }

  /* ════════════════════════════════════════════════════════════════
     Detail panel
     ════════════════════════════════════════════════════════════════ */

  function showDetail(id) {
    aptState.currentId = id;
    hide($aptError);

    // Show loading state in detail body
    $aptDetailBody.innerHTML = '<div class="text-center"><span class="spinner"></span> <span style="color:var(--muted); margin-left:0.5rem;">Loading detail&hellip;</span></div>';
    show($aptDetail);
    hide($aptDetail.querySelector('.detail-status-row')); // hide status row until loaded

    apiFetch(API_BASE + '/admin/appointments/' + encodeURIComponent(id)).then(function (apt) {
      renderDetail(apt);
      // Scroll detail into view
      $aptDetail.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }).catch(function (err) {
      $aptDetailBody.innerHTML = '<div class="error-box">' + escapeHtml(err.message || 'Failed to load appointment detail.') + '</div>';
    });
  }

  function renderDetail(apt) {
    var fields = [
      { label: 'Reference', value: apt.public_reference, full: false },
      { label: 'Status',     value: statusBadge(apt.status), raw: true, full: false },
      { label: 'When',       value: formatDate(apt.starts_at), full: false },
      { label: 'Service',    value: apt.service_name || apt.service_code, full: false },
      { label: 'Patient',    value: (apt.first_name || '') + ' ' + (apt.last_name || ''), full: false },
      { label: 'Email',      value: apt.email, full: false },
      { label: 'Phone',      value: apt.phone, full: false },
      { label: 'Source',     value: apt.source, full: false },
      { label: 'Reason',     value: apt.reason_category, full: true },
      { label: 'Created',    value: formatDate(apt.created_at), full: false },
      { label: 'Appt ID',    value: String(apt.id), full: false }
    ];

    var html = '<div class="detail-body">';
    fields.forEach(function (f) {
      var cls = f.full ? 'field field-full' : 'field';
      var valHtml = f.raw ? f.value : escapeHtml(f.value || '—');
      html += '<div class="' + cls + '">' +
        '<div class="field-label">' + escapeHtml(f.label) + '</div>' +
        '<div class="field-value">' + valHtml + '</div>' +
        '</div>';
    });
    html += '</div>';

    $aptDetailBody.innerHTML = html;

    // Set current status in the select
    $detailStatus.value = apt.status || 'pending';

    // Show the status row
    var statusRow = $aptDetail.querySelector('.detail-status-row');
    if (statusRow) show(statusRow);
  }

  function closeDetail() {
    hide($aptDetail);
    aptState.currentId = null;
  }

  /* ════════════════════════════════════════════════════════════════
     Status change
     ════════════════════════════════════════════════════════════════ */

  function updateStatus(id, newStatus) {
    hide($aptError);

    var body = JSON.stringify({ status: newStatus });

    apiFetch(API_BASE + '/admin/appointments/' + encodeURIComponent(id), {
      method: 'PATCH',
      body: body
    }).then(function (updated) {
      // Refresh the detail view
      renderDetail(updated);
      // Also refresh the row in the table
      var tr = $aptTbody.querySelector('tr[data-id="' + id + '"]');
      if (tr) {
        tr.setAttribute('data-status', updated.status);
        // Update status badge cell
        var cells = tr.querySelectorAll('td');
        if (cells.length >= 6) {
          cells[5].innerHTML = statusBadge(updated.status);
        }
      }
    }).catch(function (err) {
      showAptError(err.message || 'Failed to update status.');
    });
  }

  /* ── Event: status update button ── */
  $btnStatusUpd.addEventListener('click', function () {
    var newStatus = $detailStatus.value;
    var id = aptState.currentId;
    if (!id) return;

    if (newStatus === 'cancelled') {
      if (!confirm('Are you sure you want to cancel this appointment?')) return;
    }

    updateStatus(id, newStatus);
  });

  /* ── Event: detail close button ── */
  $btnDetailClose.addEventListener('click', function () {
    closeDetail();
  });

  /* ── Event: refresh / filter ── */
  $btnRefresh.addEventListener('click', function () {
    aptState.offset = 0;
    loadAppointments();
  });

  // Allow Enter in search field to trigger refresh
  $filterQ.addEventListener('keydown', function (e) {
    if (e.key === 'Enter') {
      aptState.offset = 0;
      loadAppointments();
    }
  });

  /* ════════════════════════════════════════════════════════════════
     Patient registrations — read-only staff review
     ════════════════════════════════════════════════════════════════ */

  function loadRegistrations() {
    hide($regError);
    hide($regEmpty);
    hide($regTableWrap);
    hide($regDetail);
    show($regLoading);

    var params = ['limit=50', 'offset=0'];
    var statusVal = $regFilterStatus.value;
    if (statusVal) params.push('status=' + encodeURIComponent(statusVal));
    var qVal = $regFilterQ.value.trim();
    if (qVal) params.push('q=' + encodeURIComponent(qVal));

    apiFetch(API_BASE + '/admin/registrations?' + params.join('&')).then(function (data) {
      hide($regLoading);
      var items = data.items || [];
      $regTbody.innerHTML = '';
      if (!items.length) {
        show($regEmpty);
        return;
      }
      show($regTableWrap);
      items.forEach(function (reg) {
        var tr = document.createElement('tr');
        tr.setAttribute('data-id', reg.id);
        tr.innerHTML =
          '<td>' + formatDate(reg.updated_at) + '</td>' +
          '<td>' + escapeHtml(reg.public_reference || '—') + '</td>' +
          '<td>' + escapeHtml(((reg.first_name || '') + ' ' + (reg.last_name || '')).trim() || '—') + '</td>' +
          '<td>' + escapeHtml(reg.email || reg.phone || '—') + '</td>' +
          '<td>' + statusBadge(reg.status) + '</td>' +
          '<td style="color:var(--muted); font-size:0.8rem;">&rarr;</td>';
        $regTbody.appendChild(tr);
      });
    }).catch(function (err) {
      hide($regLoading);
      showRegError(err.message || 'Failed to load patient registrations.');
    });
  }

  function showRegistrationDetail(id) {
    $regDetailBody.innerHTML = '<div class="text-center"><span class="spinner"></span> Loading registration&hellip;</div>';
    show($regDetail);
    apiFetch(API_BASE + '/admin/registrations/' + encodeURIComponent(id)).then(function (reg) {
      var address = [reg.address_line1, reg.address_line2, reg.city, reg.state, reg.postal_code].filter(Boolean).join(', ');
      var fields = [
        ['Reference', reg.public_reference],
        ['Status', reg.status],
        ['Appointment reference', reg.appointment_reference],
        ['Patient', ((reg.first_name || '') + ' ' + (reg.last_name || '')).trim()],
        ['Date of birth', reg.date_of_birth],
        ['Email', reg.email],
        ['Phone', reg.phone],
        ['Address', address],
        ['Emergency contact', reg.emergency_contact_name],
        ['Emergency phone', reg.emergency_contact_phone],
        ['Privacy acknowledged', reg.privacy_acknowledged ? 'Yes' : 'No'],
        ['Updated', formatDate(reg.updated_at)],
        ['Submitted', formatDate(reg.submitted_at)]
      ];
      var html = '<div class="detail-body">';
      fields.forEach(function (f) {
        html += '<div class="field"><div class="field-label">' + escapeHtml(f[0]) + '</div><div class="field-value">' + escapeHtml(f[1] || '—') + '</div></div>';
      });
      html += '</div>';
      $regDetailBody.innerHTML = html;
      $regDetail.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }).catch(function (err) {
      $regDetailBody.innerHTML = '<div class="error-box">' + escapeHtml(err.message || 'Failed to load registration.') + '</div>';
    });
  }

  $regTbody.addEventListener('click', function (e) {
    var tr = e.target.closest('tr');
    if (tr) showRegistrationDetail(tr.getAttribute('data-id'));
  });
  $regDetailClose.addEventListener('click', function () { hide($regDetail); });
  $regRefresh.addEventListener('click', loadRegistrations);
  $regFilterQ.addEventListener('keydown', function (e) { if (e.key === 'Enter') loadRegistrations(); });

  /* ════════════════════════════════════════════════════════════════
     Keycloak init
     ════════════════════════════════════════════════════════════════ */

  var keycloak = new Keycloak({
    url: KEYCLOAK_URL,
    realm: REALM,
    clientId: CLIENT_ID
  });

  keycloak.onAuthSuccess = function () {
    hide($loggedOut);
    show($loggedIn);
    clearErrors();
    loadIdentity();
  };

  keycloak.onAuthError = function () {
    hide($loggedIn);
    show($loggedOut);
    showLoginError('Authentication failed. Please try again.');
  };

  keycloak.onAuthRefreshSuccess = function () {
    // Token refreshed silently — nothing to do.
  };

  keycloak.onAuthRefreshError = function () {
    hide($loggedIn);
    show($loggedOut);
    showLoginError('Session expired. Please sign in again.');
  };

  keycloak.onTokenExpired = function () {
    keycloak.updateToken(30).catch(function () {
      hide($loggedIn);
      show($loggedOut);
      showLoginError('Session expired. Please sign in again.');
    });
  };

  /* ── Init ── */
  keycloak.init({
    onLoad: 'check-sso',
    pkceMethod: 'S256',
    checkLoginIframe: false
  }).then(function (authenticated) {
    if (authenticated) {
      hide($loggedOut);
      show($loggedIn);
      loadIdentity();
    } else {
      hide($loggedIn);
      show($loggedOut);
    }
  }).catch(function (err) {
    hide($loggedIn);
    show($loggedOut);
    showLoginError('Unable to reach the identity provider. Check your network connection.');
    console.error('Keycloak init error:', err);
  });

  /* ── Button handlers ── */
  $btnLogin.addEventListener('click', function () {
    clearErrors();
    keycloak.login();
  });

  $btnLogout.addEventListener('click', function () {
    keycloak.logout();
  });

})();
