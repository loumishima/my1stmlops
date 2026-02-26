output "fastapi_url" {
  value = google_cloud_run_service.fastapi.status[0].url
}

output "streamlit_url" {
  value = google_cloud_run_service.streamlit.status[0].url
}
