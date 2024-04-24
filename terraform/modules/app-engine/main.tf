resource "google_project_service" "iap" {
  count   = var.enable_iap ? 1 : 0
  project = var.project
  service = "iap.googleapis.com"
}

# Import an existing Oauth Consent Screen with
# terraform import --var-file=environment/project.tfvars module.appengine.google_iap_brand.project_brand projects/<project_id>/brands/<project_number>
resource "google_iap_brand" "oauth_consent_screen" {
  count             = var.enable_iap ? 1 : 0
  support_email     = var.support_email
  application_title = "Oauth Consent Screen"
  project           = var.project
  depends_on        = [google_project_service.iap]
  # GCP does not allow you to destroy the Oauth consent screen
  # So we prevent destroy here to avoid messing up the terraform state
  lifecycle {
    prevent_destroy = true
  }
}

resource "google_iap_client" "oauth_client" {
  count        = var.enable_iap ? 1 : 0
  display_name = "App Engine Oauth client"
  brand        = google_iap_brand.oauth_consent_screen[0].name
  depends_on   = [google_project_service.iap]
}

# Import an existing App Engine with
# terraform import --var-file=environment/project.tfvars module.appengine.google_app_engine_application.app <project_id>
resource "google_app_engine_application" "app" {
  project     = var.project
  location_id = "europe-west"
  # iap {
  #   enabled              = var.enable_iap
  #   oauth2_client_id     = var.enable_iap ? google_iap_client.oauth_client[0].client_id : ""
  #   oauth2_client_secret = var.enable_iap ? google_iap_client.oauth_client[0].secret : ""
  # }
  depends_on = [google_project_service.iap]
  # GCP does not allow you to destroy the default app engine
  # So we prevent destroy here to avoid messing up the terraform state
  lifecycle {
    prevent_destroy = true
  }
}

resource "google_iap_web_iam_binding" "allowed_users" {
  count   = var.enable_iap ? 1 : 0
  project = var.project
  role    = "roles/iap.httpsResourceAccessor"
  members = [
    "domain:skyhaus.com",
    "user:cas.coopman@intern.ml6.eu",
  ]
  depends_on = [google_project_service.iap]
}