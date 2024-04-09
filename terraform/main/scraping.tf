resource "google_storage_bucket" "scraping" {
  name                        = "${var.project}_scrape"
  location                    = var.region
  uniform_bucket_level_access = true
  versioning {
    enabled = true
  }
}