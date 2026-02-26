output "fastapi_url" {
  value = google_cloud_run_v2_service.fastapi.uri
}

output "streamlit_url" {
  value = google_cloud_run_v2_service.streamlit.uri
}
