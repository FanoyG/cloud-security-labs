import boto3
from session import get_session
from assume_role import assume_role



def get_role_session(creds):
    return boto3.Session(
        aws_access_key_id=creds["AccessKeyId"],
        aws_secret_access_key=creds["SecretAccessKey"],
        aws_session_token=creds["SessionToken"]
    )


def assumerole_access_s3(session):
    s3 = session.client("s3")
    return s3.list_buckets()


def main():
    # IAM USER (frank-Poll) — EXPECT SUCCESS
    base_session = get_session()

    try:
        print("[+] IAM user S3 access works")
        assumerole_access_s3(base_session)
    except Exception as e:
        print("[-] IAM user S3 access failed unexpectedly")
        print(f"    Exception: {e}")

    # ASSUME ROLE
    response = assume_role("YOUR_ROLE_ARN_HERE")
    role_creds = response["Credentials"]

    # ROLE SESSION — EXPECT FAILURE
    try:
        role_session = get_role_session(role_creds)
        print("[+] Assumed role S3 access attempt")
        assumerole_access_s3(role_session)

    except Exception as e:
        print("[-] Assumed role S3 access failed as expected")
        print(f"    Exception: {e}")

if __name__ == "__main__":
    main()