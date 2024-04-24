module "chat-ui-service-account" {
  source      = "../modules/service-account"
  project     = var.project
  name        = "chat-ui"
  description = "SA for the chat frontend"
    roles = [
    "roles/secretmanager.secretAccessor",
    "roles/aiplatform.user",
    "roles/datastore.user",
    "roles/run.invoker",
  ]
}

module "reverse-proxy-service-account" {
  source      = "../modules/service-account"
  project     = var.project
  name        = "reverse-proxy"
  description = "SA for the reverse proxy that manages the ingress to all microservices"
  roles = [
    "roles/run.invoker",
  ]
}