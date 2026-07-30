// Runtime configuration for the Dr. Farah admin SPA.
// All values are public — this is a public OIDC client, no secrets here.
// Change API_BASE per environment without touching app.js.
window.ADMIN_CONFIG = {
  KEYCLOAK_URL: "https://keycloak.soria-academie.fr",
  REALM: "drfarah",
  CLIENT_ID: "drfarah-admin",
  API_BASE: "https://api.staging.drfarah.proxbenovh.cloud/api/v1"
};
