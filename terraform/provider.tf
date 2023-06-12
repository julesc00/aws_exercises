provider "aws" {
  profile = "default"
  region = var.aws_region
}

resource "aws_s3_bucket" "tf_tutorial" {
  bucket = "tf-state-02"
}
