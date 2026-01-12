import os
import boto3
from dotenv import load_dotenv
from botocore.exceptions import NoCredentialsError

"""
Centralized AWS session handling for attacker simulation.
Credentials are loaded from environment variables.
"""

load_dotenv()

# 1. Access the environment variables
access_key_id = os.getenv('ACCESS_KEY_ID')
secret_access_key = os.getenv('SECRET_ACCESS_KEY')
region = os.getenv('AWS_DEFAULT_REGION', 'us-east-1')

# Test print statements (commented out for security reasons)
# print(f"Access Key ID: {access_key_id}")
# print(f"Secret Access Key: {secret_access_key}")

def get_session():
    if not access_key_id or not secret_access_key:
        raise NoCredentialsError()
    
    return boto3.Session(
        aws_access_key_id=access_key_id,
        aws_secret_access_key=secret_access_key,
        region_name=region
    )