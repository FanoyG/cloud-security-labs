from botocore.exceptions import NoCredentialsError, ClientError
from session import get_session

def whoami():

    try:
        session = get_session()

        # 4. Use the session to create an STS client
        sts_client = session.client('sts')

        # 5. Call the GetCallerIdentity API to find out who you are
        identity_details = sts_client.get_caller_identity()
        identity = {
            'UserId': identity_details['UserId'],
            'Account': identity_details['Account'],
            'Arn': identity_details['Arn']
        }

        return identity
    
    except NoCredentialsError:
        return {"Error": "No credentials provided."}
    
    except ClientError as e:
        return {"Error": str(e)}

if __name__ == "__main__":
    identity = whoami()
    print("\n=== Caller Identity ===")

    if "Error" in identity:
        print(f"[-] {identity['Error']}")
    else:
        for k, v in identity.items():
            print(f"{k}: {v}")