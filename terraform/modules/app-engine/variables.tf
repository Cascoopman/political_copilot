variable "project" {
  description = "GCP project name"
  type        = string
}

variable "region" {
  description = "Default GCP region for resources"
  type        = string
  default     = "europe-west1"
}

variable "enable_iap" {
  description = "Enable Identity Aware Proxy on the App Engine instance"
  type        = bool
  default     = true
}

variable "support_email" {
  description = "Support email for the Oauth consent screen"
  type        = string
}
