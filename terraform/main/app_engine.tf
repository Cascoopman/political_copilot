module "app-engine" {
  source        = "../modules/app-engine"
  project       = var.project
  region        = var.region
  enable_iap    = true
  support_email = "cas.coopman@intern.ml6.eu"
}