import boto3
from botocore.exceptions import ClientError, NoCredentialsError
from session import get_session


def assume_role(role_arn):
    session = get_session()
    sts_client = session.client("sts")

    try:
        response = sts_client.assume_role(
            RoleArn=role_arn,
            RoleSessionName="iam-role-trust-abuse-lab"
        )
    except ClientError as e:
        print(f"Error assuming role: {e}")
        raise e

    return response


if __name__ == "__main__":
    ROLE_ARN = "YOUR_ROLE_ARN_HERE"

    credentials = assume_role(ROLE_ARN)
    access_id = credentials["Credentials"]["AccessKeyId"]
    secret_key = credentials["Credentials"]["SecretAccessKey"]
    session_token = credentials["Credentials"]["SessionToken"]

    print("AssumeRole successful")
    print("AccessKeyId:", access_id[:3] + "*" * 15)
    print("SecretAccessKey:", secret_key[:3] + "*" * 15)
    print("SessionToken:", session_token[:3] + "*" * 15)
