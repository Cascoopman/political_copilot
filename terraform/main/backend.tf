
/******************************************
	Remote backend configuration
 *****************************************/

# setup of the backend gcs bucket that will keep the remote state

terraform {
  backend "gcs" {
    bucket = "cedar-talent-417009_terraform"
    prefix = "terraform/state"
  }
}
