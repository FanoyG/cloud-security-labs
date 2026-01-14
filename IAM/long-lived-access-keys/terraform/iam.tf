resource "aws_iam_user" "test_user" {
  name = "jack-smith"
  path = "/dev/"

  tags = {
    purpose = "iam-long-lived-access-keys-lab"
  }
}

data "aws_iam_policy_document" "test_policy" {
  statement {
    sid     = "LongLivedAccessKeys"
    effect = "Allow"

    actions = [
      "s3:ListAllMyBuckets"
    ]

    resources = ["*"]
  }
}

resource "aws_iam_policy" "test_iam_policy" {
  name   = "long-lived-access-keys-policy-lab"
  policy = data.aws_iam_policy_document.test_policy.json
}

resource "aws_iam_user_policy_attachment" "test_iam_longlived_policy" {
  user       = aws_iam_user.test_user.name
  policy_arn = aws_iam_policy.test_iam_policy.arn
}

resource "aws_iam_access_key" "test_user_key" {
  user = aws_iam_user.test_user.name
}
