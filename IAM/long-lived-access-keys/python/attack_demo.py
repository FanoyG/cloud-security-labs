import boto3
import os
from botocore.exceptions import ClientError
from dotenv import load_dotenv

load_dotenv()

aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
region_name = os.getenv("AWS_DEFAULT_REGION", "ap-south-1")

s3 = boto3.client(
    "s3",
    region_name=region_name,
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key
)

try:
    response = s3.list_buckets()
    print("[+] API call successful")
    print("Buckets visible to attacker:")

    if response["Buckets"]:
        for bucket in response["Buckets"]:
            print(f" - {bucket['Name']}")
    else:
        print("[-] No buckets available in this account")

except ClientError as e:
    print("[-] API call failed")
    print(e)
