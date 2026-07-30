/**
 * Dr. Farah Admin SPA — application logic.
 * Keycloak Authorization Code + PKCE S256 → Bearer token → GET /admin/me.
 * Tokens stay in memory (keycloak-js manages this); never written to localStorage.
 */
(function () {
  'use strict';

  /* ── Config ── */
  const cfg = window.ADMIN_CONFIG || {};
  const KEYCLOAK_URL = cfg.KEYCLOAK_URL;
  const REALM        = cfg.REALM;
  const CLIENT_ID    = cfg.CLIENT_ID;
  const API_BASE     = cfg.API_BASE;

  if (!KEYCLOAK_URL || !REALM || !CLIENT_ID || !API_BASE) {
    alert('Admin SPA is misconfigured — missing required config values. Check config.js.');
    return;
  }

  /* ── DOM refs ── */
  const $loggedOut   = document.getElementById('logged-out');
  const $loggedIn    = document.getElementById('logged-in');
  const $btnLogin    = document.getElementById('btn-login');
  const $btnLogout   = document.getElementById('btn-logout');
  const $loginError  = document.getElementById('login-error');
  const $loading     = document.getElementById('loading-indicator');
  const $identity    = document.getElementById('identity-panel');
  const $apiError    = document.getElementById('api-error');

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

  function clearErrors() {
    hide($loginError);
    hide($apiError);
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
  }

  function escapeHtml(str) {
    var div = document.createElement('div');
    div.appendChild(document.createTextNode(str));
    return div.innerHTML;
  }

  /* ── Call /admin/me ── */
  function loadIdentity() {
    hide($identity);
    hide($apiError);
    show($loading);

    keycloak.updateToken(30).then(function () {
      return fetch(API_BASE + '/admin/me', {
        method: 'GET',
        headers: {
          'Authorization': 'Bearer ' + keycloak.token,
          'Accept': 'application/json'
        }
      });
    }).then(function (res) {
      if (!res.ok) {
        if (res.status === 401 || res.status === 403) {
          throw new Error('Access denied (' + res.status + '). Your account may lack the required admin role.');
        }
        throw new Error('API error (' + res.status + '): ' + res.statusText);
      }
      return res.json();
    }).then(function (data) {
      renderIdentity(data);
    }).catch(function (err) {
      hide($loading);
      showApiError(err.message || 'Failed to load identity.');
    });
  }

  /* ── Keycloak init ── */
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
    // Refresh failed (e.g. session expired). Keycloak will redirect to login
    // if check-sso is on; we clear the UI to avoid a stale state.
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
