import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

def get_aws_session():
    """
    Create and validate an AWS session using boto3.
    """

    try:
        session = boto3.Session()

        sts= session.client("sts")
        identity = sts.get_caller_identity()

        account_id = identity.get("Account")
        arn = identity["Arn"]

        region = session.region_name

        return{
            "session" : session,
            "account_id" : account_id,
            "arn" : arn,
            "region" : region
        }

    except NoCredentialsError:
        print("[ERROR] AWS credentials were not found.")
        print ("Run:")
        print ("aws configure")
        return None

    except PartialCredentialsError:
        print("[ERROR] Incomplete AWS credentials found.")
        print ("Run:")
        print ("aws configure")
        return None

    except Exception as error:
        print(f"[ERROR] Could not connect to AWS: {error}")
        return None