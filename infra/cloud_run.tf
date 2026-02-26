resource "google_cloud_run_service" "fastapi" {
  name     = "fastapi"
  location = var.region

  template {
    spec {
      containers {
        image = var.fastapi_image
      }
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }
}

resource "google_cloud_run_service" "streamlit" {
  name     = "streamlit"
  location = var.region

  template {
    spec {
      containers {
        image = var.streamlit_image

        env {
          name  = "API_URL"
          value = google_cloud_run_service.fastapi.status[0].url
        }
      }
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }
}
