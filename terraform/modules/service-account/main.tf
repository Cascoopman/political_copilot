resource "google_service_account" "sa" {
  project      = var.project
  account_id   = var.name
  display_name = var.display_name
  description  = var.description
}

resource "google_project_iam_member" "iam_role_assignment" {
  for_each = toset(var.roles)
  role     = each.key
  project  = var.project
  member   = "serviceAccount:${google_service_account.sa.email}"
}
