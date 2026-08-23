# Security Policy

Security is important for the **AWS Admin Utility Toolkit** because the project interacts with AWS accounts, credentials, IAM permissions, and cloud infrastructure through the AWS SDK for Python (Boto3).

If you discover a security issue in this project, please report it responsibly and avoid publicly disclosing vulnerabilities before they can be reviewed.

---

## Supported Versions

The project is currently under active development. Security fixes are provided for the latest version of the toolkit.

| Version | Supported |
| ------- | --------- |
| v0.2.x  | ✅         |
| v0.1.x  | ❌         |
| < v0.1  | ❌         |

Users are encouraged to use the latest available version of the project.

As the project develops, this table will be updated to reflect currently supported releases.

---

## Reporting a Vulnerability

If you discover a potential security vulnerability in the **AWS Admin Utility Toolkit**, please **do not create a public GitHub Issue containing sensitive vulnerability details**.

Instead, use **GitHub's private vulnerability reporting feature** through the repository's **Security** section when available.

When submitting a vulnerability report, please include as much information as possible, such as:

* A description of the vulnerability
* The affected module or file
* The affected version
* Steps required to reproduce the issue
* Potential security impact
* Example output or error messages
* Suggested mitigation or fix, if known

Please remove or redact sensitive information before submitting a report.

---

## Sensitive Information

Never include real AWS credentials or other secrets in vulnerability reports, screenshots, logs, issues, or pull requests.

This includes:

* AWS Access Key IDs
* AWS Secret Access Keys
* AWS Session Tokens
* IAM credentials
* `.aws/credentials` contents
* Private SSH keys
* `.pem` files
* API keys
* Environment variables containing secrets
* Other authentication tokens or credentials

If credentials are accidentally exposed, they should be revoked or rotated immediately through the appropriate AWS account.

---

## Vulnerability Review Process

After a vulnerability is reported:

1. The report will be reviewed to determine whether the issue can be reproduced.
2. The affected component and potential impact will be evaluated.
3. If the vulnerability is confirmed, a fix will be developed and tested.
4. The fix will be included in an appropriate project update.
5. The reporter may be informed when the issue has been resolved.

If the report is determined not to represent a security vulnerability, an explanation may be provided where appropriate.

Response times may vary because this project is currently independently maintained and under active development.

---

## Security Scope

Security reports may include issues involving:

* AWS credential handling
* Accidental credential exposure
* Unsafe AWS API usage
* IAM permission handling
* Security Group analysis
* Input validation
* Sensitive information appearing in output
* Unsafe resource modification
* Dependency vulnerabilities
* Potential command or code injection
* Security issues introduced by future modules

General bugs or feature requests that do not have a security impact should be submitted through the normal GitHub Issues section instead.

---

## AWS Credentials

The **AWS Admin Utility Toolkit does not require AWS credentials to be hardcoded into the source code**.

The project is designed to use credentials provided through supported AWS credential mechanisms, such as locally configured AWS CLI credentials.

Never add credentials directly to the source code:

```python
# ❌ DO NOT DO THIS

aws_access_key_id = "YOUR_ACCESS_KEY"
aws_secret_access_key = "YOUR_SECRET_ACCESS_KEY"
```

Never commit credential files or private keys to the repository.

---

## Principle of Least Privilege

Users should run the toolkit with an IAM identity or role that has only the permissions required by the modules being used.

Avoid using the AWS root account.

The current version primarily performs read-only inventory and auditing operations. Required IAM permissions should be documented as new modules are introduced.

---

## Safe Development Approach

The project currently focuses on **read-only AWS administration and auditing**.

Future functionality that modifies or deletes AWS resources should be designed with appropriate safeguards, such as:

* Dry-run functionality where possible
* Explicit administrator confirmation
* Clear descriptions of proposed changes
* Appropriate error handling
* Least-privilege IAM permissions
* Logging of administrative actions

Potentially destructive operations should never occur unexpectedly.

---

## Responsible Disclosure

Please allow reasonable time for a reported vulnerability to be investigated and addressed before publicly disclosing technical details.

Responsible disclosure helps protect users of the project and their AWS environments while a fix is being developed.

---

## Security Disclaimer

This project is intended for legitimate AWS administration, auditing, learning, and authorized cloud environments.

Users are responsible for:

* Protecting their AWS credentials
* Configuring appropriate IAM permissions
* Reviewing security findings
* Understanding actions performed by the toolkit
* Testing changes before using them in production environments

Only use the toolkit with AWS accounts and resources that you own or are authorized to administer.
