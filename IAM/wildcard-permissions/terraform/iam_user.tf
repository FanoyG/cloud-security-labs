resource "aws_iam_user" "test_user" {
    name = "test-user-01"
    path = "/test/"

    tags = {
        purpose = "iam-wildcard-lab"
    }
}

