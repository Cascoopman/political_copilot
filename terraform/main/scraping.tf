resource "google_storage_bucket" "scraping" {
  name                        = "${var.project}_scrape"
  location                    = var.region
  uniform_bucket_level_access = true
  versioning {
    enabled = true
  }
}

resource "google_storage_bucket" "embeddings" {
  name                        = "${var.project}_embed"
  location                    = "europe-west1"
  uniform_bucket_level_access = true
  versioning {
    enabled = true
  }
}

# Grant bucket-level permissions
resource "google_storage_bucket_iam_member" "bucket_iam_member" {
  bucket = "${var.project}_scrape"
  
  role   = "roles/storage.objectViewer"
  member = "user:cas.coopman@intern.ml6.eu"  # Replace with the user's email address
}

# Grant bucket-level permissions
resource "google_storage_bucket_iam_member" "bucket_iam_member_2" {
  bucket = "${var.project}_scrape"
  
  role   = "roles/storage.objectAdmin"
  member = "user:jens.bontinck@ml6.eu"  # Replace with the user's email address
}

# Grant bucket-level permissions
resource "google_storage_bucket_iam_member" "bucket_iam_member_sa" {
  bucket = "${var.project}_scrape"
  
  role   = "roles/storage.objectViewer"
  member = "serviceAccount:svc-cloudrun@${var.project}.iam.gserviceaccount.com"
}