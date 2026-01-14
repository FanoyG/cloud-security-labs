
variable "aws_region" {
  description = "AWS region for the IAM lab"
  type        = string
  default     = "ap-south-1"
}

variable "aws_profile" {
  description = "AWS CLI profile name used by Terraform"
  type        = string
  default     = "YOUR-PROFILE"
}
