variable "aws_profile" {
    description = "AWS CLI profile name used for the lab"
    type = string
    default = "YOUR-PROFILE"
}

variable "aws_region" {
    description = "AWS region for the IAM Role Lab"
    type = string
    default = "ap-south-1"
}