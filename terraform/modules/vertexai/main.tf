######################################
# vertexai index
######################################

# TODO fix this bucket not being in terraform.state
resource "google_storage_bucket" "embeddings" {
  name                        = "${var.project}_embed"
  location                    = "europe-west1"
  uniform_bucket_level_access = true
  versioning {
    enabled = true
  }
}

# The sample data comes from the following link:
# https://cloud.google.com/vertex-ai/docs/matching-engine/filtering#specify-namespaces-tokens
#resource "google_storage_bucket_object" "data" {
#  name   = "contents/data.json"
#  bucket = google_storage_bucket.embeddings.name
#  content = <<EOF
#{"id": "42", "embedding": [0.5, 1.0], "restricts": [{"namespace": "class", "allow": ["cat", "pet"]},{"namespace": "category", "allow": ["feline"]}]}
#{"id": "43", "embedding": [0.6, 1.0], "restricts": [{"namespace": "class", "allow": ["dog", "pet"]},{"namespace": "category", "allow": ["canine"]}]}
#EOF
#}

resource "google_vertex_ai_index" "political_index" {
  region = var.region
  display_name = "political_index"
  description = "index for the political use case"
  metadata {
    contents_delta_uri = "gs://${google_storage_bucket.embeddings.name}"
    config {
      dimensions = 1536
      approximate_neighbors_count = 10
      shard_size = "SHARD_SIZE_SMALL"
      distance_measure_type = "COSINE_DISTANCE"
      feature_norm_type = "UNIT_L2_NORM"
      algorithm_config {
        tree_ah_config {
            leaf_node_embedding_count=1000
            leaf_nodes_to_search_percent=10
        }
      }
    }
  }
  index_update_method = "BATCH_UPDATE"
}

######################################
# vertexai index endpoint
######################################

resource "google_vertex_ai_index_endpoint" "political_index_endpoint" {
  display_name = "political-index-endpoint"
  description  = "political index endpoint"
  region       = var.region
  network      = "projects/${data.google_project.project.number}/global/networks/main-network" # ${google_compute_network.vertex_network.name}
  depends_on   = [
    google_service_networking_connection.vertex_vpc_connection
  ]
}

resource "google_service_networking_connection" "vertex_vpc_connection" {
  network                 = "main-network" #google_compute_network.vertex_network.id
  service                 = "servicenetworking.googleapis.com"
  reserved_peering_ranges = [google_compute_global_address.vertex_range.name]
}

resource "google_compute_global_address" "vertex_range" {
  name          = "address-vertexai"
  purpose       = "VPC_PEERING"
  address_type  = "INTERNAL"
  prefix_length = 16
  network       = "main-network"
}

/**
resource "google_compute_network" "vertex_network" {
  name       = "network-vertexai"
}
**/

data "google_project" "project" {
  project_id = var.project
}