resource "aws_iam_role" "iam_test_role" {
    name = "s3_bucket_list"

    assume_role_policy = file(path.module + "/trust-policy.json")
}