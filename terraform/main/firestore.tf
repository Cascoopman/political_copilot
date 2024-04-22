resource "google_project_service" "firestore" {
  project = var.project
  service = "firestore.googleapis.com"
}