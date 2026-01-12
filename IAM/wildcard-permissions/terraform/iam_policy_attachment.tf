resource "aws_iam_user_policy_attachment" "test_wildcard_policy" {
    user = aws_iam_user.test_user.name
    policy_arn = aws_iam_policy.wildcard_policy.arn
}