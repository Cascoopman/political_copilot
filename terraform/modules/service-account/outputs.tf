output "email" {
  value       = google_service_account.sa.email
  description = "Email of the service account"
}
