data "archive_file " "my_lambda_function" {
  source_dir = "${path.module}/lambda/"
  output_path = "${path.module}/lambda.zip"
  type = "zip"
}