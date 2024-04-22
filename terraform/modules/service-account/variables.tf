variable "project" {
  description = "GCP project name"
  type        = string
}

variable "name" {
  description = "Name of the service account"
  type        = string
}

variable "display_name" {
  description = "The display name for the service account."
  type        = string
  default     = ""
}

variable "description" {
  description = "Description of the service account"
  type        = string
}

variable "roles" {
  description = "Roles to be assigned to the service account"
  type        = list(string)
}
