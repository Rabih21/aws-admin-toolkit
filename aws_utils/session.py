import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError

from pathlib import Path
from getpass import getpass


# ============================================================
# AWS CREDENTIAL CONFIGURATION
# ============================================================

def save_aws_credentials(access_key, secret_key, region):
    """
    Save AWS credentials using the standard AWS configuration files.

    Windows:
        C:\\Users\\<username>\\.aws\\credentials
        C:\\Users\\<username>\\.aws\\config

    Linux/macOS:
        ~/.aws/credentials
        ~/.aws/config
    """

    aws_directory = Path.home() / ".aws"

    # Create .aws directory if it does not already exist
    aws_directory.mkdir(parents=True, exist_ok=True)

    credentials_file = aws_directory / "credentials"
    config_file = aws_directory / "config"

    # Save credentials
    with open(credentials_file, "w", encoding="utf-8") as file:
        file.write(
            "[default]\n"
            f"aws_access_key_id = {access_key}\n"
            f"aws_secret_access_key = {secret_key}\n"
        )

    # Save region/configuration
    with open(config_file, "w", encoding="utf-8") as file:
        file.write(
            "[default]\n"
            f"region = {region}\n"
            "output = json\n"
        )


# ============================================================
# VALIDATE NEW CREDENTIALS
# ============================================================

def validate_new_credentials(access_key, secret_key, region):
    """
    Validate credentials before saving them.

    A temporary Boto3 session is created and AWS STS
    GetCallerIdentity is used to verify the credentials.
    """

    try:

        temporary_session = boto3.Session(
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region
        )

        sts = temporary_session.client("sts")

        identity = sts.get_caller_identity()

        return {
            "valid": True,
            "account_id": identity.get("Account", "N/A"),
            "arn": identity.get("Arn", "N/A"),
            "session": temporary_session
        }

    except ClientError as error:

        return {
            "valid": False,
            "error": str(error)
        }

    except Exception as error:

        return {
            "valid": False,
            "error": f"{type(error).__name__}: {error}"
        }


# ============================================================
# FIRST-TIME AWS SETUP
# ============================================================

def configure_aws_credentials():
    """
    Interactive first-time AWS configuration.

    Credentials are validated before they are stored locally.
    """

    while True:

        print()
        print("=" * 60)
        print("                 AWS FIRST-TIME SETUP")
        print("=" * 60)
        print()
        print("No valid AWS credentials were found.")
        print()
        print("Enter your AWS credentials below.")
        print("Credentials will be validated before they are saved.")
        print()

        access_key = input("AWS Access Key ID: ").strip()

        # getpass prevents the secret key from appearing on screen
        secret_key = getpass("AWS Secret Access Key: ").strip()

        region = input(
            "Default AWS Region [us-east-1]: "
        ).strip()

        if not region:
            region = "us-east-1"

        # Basic input validation
        if not access_key or not secret_key:

            print()
            print("[ERROR] Access Key ID and Secret Access Key are required.")
            continue

        print()
        print("Testing AWS credentials...")

        result = validate_new_credentials(
            access_key,
            secret_key,
            region
        )

        if result["valid"]:

            print()
            print("[SUCCESS] AWS credentials verified.")
            print()
            print(f"Account ID: {result['account_id']}")
            print(f"Identity:   {result['arn']}")
            print(f"Region:     {region}")

            try:

                save_aws_credentials(
                    access_key,
                    secret_key,
                    region
                )

                print()
                print("[SUCCESS] AWS configuration saved successfully.")

                return True

            except Exception as error:

                print()
                print(
                    "[ERROR] Credentials were valid, but the "
                    "configuration could not be saved."
                )
                print(
                    f"{type(error).__name__}: {error}"
                )

                return False

        else:

            print()
            print("[ERROR] AWS credentials could not be validated.")
            print()
            print(result["error"])
            print()

            choice = input(
                "Would you like to try again? [Y/N]: "
            ).strip().lower()

            if choice != "y":

                return False


# ============================================================
# CREATE AWS SESSION
# ============================================================

def get_aws_session():
    """
    Create and validate the AWS session.

    If credentials are missing or invalid, offer the user
    an interactive AWS configuration.
    """

    try:
        session = boto3.Session()

        region = session.region_name

        if not region:
            region = "us-east-1"

        sts = session.client(
            "sts",
            region_name=region
        )

        identity = sts.get_caller_identity()

        return {
            "session": session,
            "account_id": identity.get("Account", "N/A"),
            "arn": identity.get("Arn", "N/A"),
            "region": region
        }

    # --------------------------------------------------------
    # NO CREDENTIALS
    # --------------------------------------------------------

    except (NoCredentialsError, PartialCredentialsError):

        print()
        print("[WARNING] No AWS credentials were found.")
        print()

        choice = input(
            "Would you like to configure AWS now? [Y/N]: "
        ).strip().lower()

        if choice != "y":
            print()
            print("[ERROR] AWS credentials are required.")
            return None

        configured = configure_aws_credentials()

        if not configured:
            print()
            print("[ERROR] AWS configuration was not completed.")
            return None

        # Reload credentials after saving them
        return get_aws_session()

    # --------------------------------------------------------
    # INVALID / EXPIRED CREDENTIALS
    # --------------------------------------------------------

    except ClientError as error:

        error_code = (
            error.response
            .get("Error", {})
            .get("Code", "Unknown")
        )

        invalid_credential_errors = (
            "InvalidClientTokenId",
            "SignatureDoesNotMatch",
            "ExpiredToken",
            "TokenRefreshRequired",
            "AuthFailure"
        )

        if error_code in invalid_credential_errors:

            print()
            print(
                "[ERROR] Existing AWS credentials are "
                "invalid or expired."
            )
            print()

            choice = input(
                "Would you like to configure new credentials? [Y/N]: "
            ).strip().lower()

            if choice == "y":

                configured = configure_aws_credentials()

                if configured:
                    return get_aws_session()

            return None

        print()
        print(
            f"[ERROR] AWS returned an error: "
            f"{error_code}: {error}"
        )

        return None

    # --------------------------------------------------------
    # OTHER ERRORS
    # --------------------------------------------------------

    except Exception as error:

        print()
        print(
            f"[ERROR] Could not connect to AWS: "
            f"{type(error).__name__}: {error}"
        )

        return None