// Runtime configuration for the Dr. Farah admin SPA.
// All values are public — this is a public OIDC client, no secrets here.
// The same bundle can be deployed to staging and production; API selection is
// derived from the current admin hostname.
(function () {
  'use strict';

  var h = window.location.hostname;
  var apiBase;

  if (h === 'admin.drfarahvipurgentcare.com') {
    apiBase = 'https://api.drfarahvipurgentcare.com/api/v1';
  } else if (h === 'admin-staging.drfarahvipurgentcare.com') {
    apiBase = 'https://api-staging.drfarahvipurgentcare.com/api/v1';
  } else if (h === 'admin.drfarah.proxbenovh.cloud') {
    // Temporary staging admin kept during migration.
    apiBase = 'https://api.staging.drfarah.proxbenovh.cloud/api/v1';
  } else {
    // Fail toward staging, never production, for unknown/local hosts.
    apiBase = 'https://api-staging.drfarahvipurgentcare.com/api/v1';
  }

  window.ADMIN_CONFIG = {
    KEYCLOAK_URL: 'https://keycloak.soria-academie.fr',
    REALM: 'drfarah',
    CLIENT_ID: 'drfarah-admin',
    API_BASE: apiBase
  };
})();
