locals {
  # List of UUIDs found in the respective bitbucket repository settings under Repository UUID. Must include the curly brackets.
  bitbucket_repo_ids  = []
  bitbucket_workspace = "ml6team"
}

locals {
  attribute_condition = format("assertion.repositoryUuid in %v", local.bitbucket_repo_ids)
  audiences           = ["ari:cloud:bitbucket::workspace/e65ac0ba-0ab0-4ea9-9524-95dade9ab047"]
  issuer_uri          = "https://api.bitbucket.org/2.0/workspaces/${local.bitbucket_workspace}/pipelines-config/identity/oidc"
}

module "wif" {
  source                  = "../modules/wif"
  project                 = var.project
  attribute_condition     = local.attribute_condition
  audiences               = local.audiences
  issuer_uri              = local.issuer_uri
  cicd_service_account_id = "svc-cicd"
  svc_cicd_roles = [
    "roles/storage.admin",
    "roles/cloudbuild.builds.editor"
  ]
}

resource "google_project_service" "iam_credentials" {
  project = var.project
  service = "iamcredentials.googleapis.com"
}

resource "google_project_service" "iam" {
  project    = var.project
  service    = "iam.googleapis.com"
  depends_on = [google_project_service.iam_credentials]
}

resource "google_project_service" "cloud_resource_manager" {
  project = var.project
  service = "cloudresourcemanager.googleapis.com"
}

resource "google_project_service" "sts" {
  project = var.project
  service = "sts.googleapis.com"
}
