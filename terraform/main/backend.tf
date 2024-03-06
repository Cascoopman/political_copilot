
/******************************************
	Remote backend configuration
 *****************************************/

# setup of the backend gcs bucket that will keep the remote state

terraform {
  backend "gcs" {
    bucket = "to-be-decided_terraform"
    prefix = "terraform/state"
  }
}
