terraform {
  backend "gcs" {
    bucket  = "my1stmlops-lhro"
    prefix  = "cloudrun"
  }
}
