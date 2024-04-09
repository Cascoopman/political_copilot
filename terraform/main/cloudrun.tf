resource "google_project_service" "cloudrun" {
  project = var.project
  service = "run.googleapis.com"
}

resource "google_service_account" "cloudrun" {
  project     = var.project
  account_id  = "svc-cloudrun"
  description = "Service account for cloud run"
}

resource "google_project_iam_member" "cloudrun" {
  for_each = toset(var.svc_cloudrun_roles)
  role     = each.key
  project  = var.project
  member   = "serviceAccount:${google_service_account.cloudrun.email}" # change naar svc
}

variable "svc_cloudrun_roles" {
  description = "IAM roles to bind on service account"
  type        = list(string)
  default = [
    "roles/storage.objectViewer",
    "roles/aiplatform.admin"
  ]
}
