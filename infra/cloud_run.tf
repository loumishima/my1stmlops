resource "google_cloud_run_v2_service" "fastapi" {
  name     = "fastapi"
  location = var.region

  template {
    containers {
        image = var.fastapi_image
      }
  }
}

resource "google_cloud_run_v2_service" "streamlit" {
  name     = "streamlit"
  location = var.region

  template {
      containers {
        image = var.streamlit_image

        env {
          name  = "API_URL"
          value = google_cloud_run_v2_service.fastapi.uri
        }
    }
  }
}
