data "aws_iam_policy_document" "wildcard" {
  statement {
    sid     = "WildcardPermissions"
    effect  = "Allow"
    actions = ["*"]
    resources = ["*"]
  }
}

resource "aws_iam_policy" "wildcard_policy" {
  name   = "wildcard-policy-lab"
  policy = data.aws_iam_policy_document.wildcard.json
}
