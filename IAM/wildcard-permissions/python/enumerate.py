import boto3
from botocore.exceptions import ClientError
from session import get_session


def enumerate_iam(session):
    print("\n[+] Enumerating IAM")
    iam = session.client('iam')

    users = iam.list_users()["Users"]
    print(f"[+] Found {len(users)} users:")
    for user in users:
        print(f" - {user['UserName']} (ARN: {user['Arn']})")
        
        attached_policies = iam.list_attached_user_policies(UserName=user['UserName'])['AttachedPolicies']

        if attached_policies:
            for policy in attached_policies:
                print(f"    - Attached Policy: {policy['PolicyName']} (ARN: {policy['PolicyArn']})")
        else:
            print("    - No attached policies found.")

def enumerate_s3(session):
    print("\n[+] Enumerating S3 Buckets")
    s3 = session.client('s3')

    buckets = s3.list_buckets()["Buckets"]
    print(f"[+] Found {len(buckets)} buckets:")
    for bucket in buckets:
        print(f" - {bucket['Name']}")

def enumerate_ec2(session):
    print("\n[+] Enumerating EC2")
    ec2 = session.client('ec2')

    reservations = ec2.describe_instances()['Reservations']
    instance_count = sum(len(r['Instances']) for r in reservations)

    print(f"[+] Found {instance_count} EC2 instances:")


def main():
    try:
        session = get_session()

        enumerate_iam(session)
        enumerate_s3(session)
        enumerate_ec2(session)

        print("\n[+] Enumeration complete -- blast radius confirmed.")

    except ClientError as e:
        print(f"[-] ClientError: {e}")
    except Exception as e:
        print(f"[-] An error occurred: {e}")
    
if __name__ == "__main__":
    main()