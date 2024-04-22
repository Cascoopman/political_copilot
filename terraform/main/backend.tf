
/******************************************
	Remote backend configuration
 *****************************************/

# setup of the backend gcs bucket that will keep the remote state

terraform {
  backend "gcs" {
    bucket = "${var.project}_terraform"
    prefix = "terraform/state"
  }
}
