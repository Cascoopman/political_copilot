output "bucket_name" {
  value       = google_storage_bucket.embeddings.name
  description = "The name of the Google Storage Bucket"
}

output "index_display_name" {
  value       = google_vertex_ai_index.political_index.display_name
  description = "The display name of the Vertex AI Index"
}

output "index_endpoint_display_name" {
  value       = google_vertex_ai_index_endpoint.political_index_endpoint.display_name
  description = "The display name of the Vertex AI Index Endpoint"
}

output "vertex_network_name" {
  value       = "main-network"  # Update this based on your actual network name
  description = "The name of the Google Compute Network for Vertex AI"
}

output "vertex_range_address" {
  value       = google_compute_global_address.vertex_range.address
  description = "The IP address of the reserved global address for VPC peering"
}
