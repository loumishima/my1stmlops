variable "project_id" {
  description = "GCP Project ID"
  type        = string
}

variable "region" {
  default = "us-central1"
}

variable "fastapi_image" {
  description = "Imagem do FastAPI"
  type        = string
  default     = "us-docker.pkg.dev/cloudrun/container/hello"
}

variable "streamlit_image" {
  description = "Imagem do Streamlit"
  type        = string
  default     = "us-docker.pkg.dev/cloudrun/container/hello"
}
