Of course. Below is the **complete README rewritten for the current v0.2.2**, while keeping the structure we've been using and only incorporating the changes we actually implemented: the Windows `.exe` from v0.2.1 and the new first-time AWS credential configuration from v0.2.2.

````markdown
# AWS Admin Utility Toolkit

A modular **Python + Boto3 toolkit for AWS cloud administrators** that simplifies common AWS operational, inventory, security, monitoring, compliance, and cost-management tasks.

The goal of this project is to provide cloud administrators with a single command-line toolkit instead of relying on multiple individual scripts or manually checking resources through the AWS Management Console.

> **Project Status:** 🚧 Active Development — v0.2.2

---

## ☁️ About the Project

AWS environments can quickly become difficult to manage as the number of resources, regions, security groups, IAM identities, volumes, buckets, and other services grows.

**AWS Admin Utility Toolkit** aims to provide a centralized Python-based interface for performing common cloud administration tasks such as:

* Discovering AWS resources
* Generating infrastructure inventories
* Detecting security risks
* Finding unused resources
* Checking IAM security
* Auditing resource tags
* Reviewing backups and snapshots
* Monitoring AWS services
* Identifying potential cost savings
* Generating operational reports
* Documenting AWS environments

The project uses the **AWS SDK for Python (Boto3)** to communicate directly with AWS APIs.

---

# 🚀 Current Version — v0.2.2

The current version includes:

* AWS Authentication & Session Management
* EC2 Inventory Reporter
* Security Group Exposure Scanner
* Standalone Windows executable
* Built-in first-time AWS credential configuration

Windows administrators can download the standalone executable, launch it directly, configure AWS credentials from inside the toolkit if necessary, and begin using the available administration utilities without installing Python or cloning the repository.

---

# ✅ Currently Implemented

## 🔑 AWS Authentication & Session Management

The toolkit:

* Creates an AWS session using Boto3
* Detects existing AWS credentials
* Validates authentication using AWS STS
* Retrieves the AWS Account ID
* Displays the authenticated IAM identity
* Detects the configured AWS region
* Handles missing credentials
* Handles incomplete credentials
* Detects invalid or expired credentials
* Provides interactive first-time AWS configuration when credentials are missing
* Validates new credentials before saving them
* Automatically continues to the toolkit after successful configuration

---

## 🖥️ Module 1 — EC2 Inventory Reporter

The EC2 Inventory Reporter discovers EC2 instances in the configured AWS region and displays information including:

* Instance Name
* Instance ID
* Instance State
* Instance Type
* Availability Zone
* Private IP Address
* Public IP Address
* VPC ID
* Subnet ID
* AMI ID
* Launch Time
* Attached Security Groups

Example:

```text
------------------------------------------------------------

Name:              Test-Server
Instance ID:       i-0123456789abcdef0
State:             running
Instance Type:     t3.micro
Availability Zone: us-east-1a

NETWORK

Private IP:        10.0.1.15
Public IP:         54.x.x.x
VPC ID:            vpc-0123456789
Subnet ID:         subnet-0123456789

INSTANCE

AMI ID:            ami-0123456789
Launch Time:       2026-08-21 18:00:00+00:00

SECURITY GROUPS

- WebServer-SG (sg-0123456789)
````

---

## 🛡️ Module 2 — Security Group Exposure Scanner

The Security Group Exposure Scanner analyzes inbound rules across Security Groups in the configured AWS region.

It detects public exposure through:

* `0.0.0.0/0`
* `::/0`

Each public rule is classified as:

* `CRITICAL` — Dangerous service publicly exposed
* `WARNING` — Other public port requiring review
* `INFO` — Common public service such as HTTP/HTTPS

Currently detected critical services:

| Port | Service              |
| ---: | -------------------- |
|   22 | SSH                  |
| 3389 | RDP                  |
| 3306 | MySQL                |
| 5432 | PostgreSQL           |
| 1433 | Microsoft SQL Server |
| 6379 | Redis                |

The scanner also detects Security Groups allowing all traffic from the public internet.

Each finding includes:

* Security Group name and ID
* VPC ID
* Protocol
* Port / port range
* Public source
* Severity
* Service
* Finding description
* Recommended remediation

The scanner generates a final summary showing the number of Critical, Warning, and Informational findings.

---

# 🪟 Standalone Windows Executable

Starting with **v0.2.1**, the AWS Admin Utility Toolkit is available as a standalone Windows executable.

Windows users can run the toolkit without:

* Installing Python
* Installing Boto3 manually
* Cloning the GitHub repository
* Creating a Python virtual environment
* Running Python commands

The executable is distributed through **GitHub Releases** and can be launched directly after downloading.

Starting with **v0.2.2**, AWS credentials can also be configured directly from the application when no valid credentials are detected.

This means a first-time Windows user can:

```text
Download EXE
     │
     ▼
Double-click
     │
     ▼
AWS credentials detected?
     │
 ┌───┴───┐
 │       │
YES      NO
 │       │
 │       ▼
 │   First-Time Setup
 │       │
 │       ├── Access Key ID
 │       ├── Secret Access Key
 │       └── AWS Region
 │
 │       ▼
 │   Validate with AWS STS
 │       │
 │       ▼
 │   Save Configuration
 │       │
 └───────┴──────► Toolkit Menu
```

---

# 🔐 First-Time AWS Configuration

Starting with **v0.2.2**, the toolkit automatically detects when AWS credentials are not available.

Instead of requiring the administrator to exit the application and manually configure AWS, the toolkit offers an interactive setup process.

Example:

```text
============================================================
              AWS ADMIN UTILITY TOOLKIT
============================================================

Connecting to AWS...

[WARNING] No AWS credentials were found.

Would you like to configure AWS now? [Y/N]: Y

============================================================
                 AWS FIRST-TIME SETUP
============================================================

No valid AWS credentials were found.

Enter your AWS credentials below.
Credentials will be validated before they are saved.

AWS Access Key ID: AKIA...
AWS Secret Access Key:
Default AWS Region [us-east-1]: us-east-1

Testing AWS credentials...

[SUCCESS] AWS credentials verified.

Account ID: 123456789012
Identity:   arn:aws:iam::123456789012:user/cloud-admin
Region:     us-east-1

[SUCCESS] AWS configuration saved successfully.
```

The toolkit then automatically reconnects to AWS and continues to the main menu.

### Security Measures

The first-time configuration process includes several safeguards:

* The Secret Access Key is hidden while being entered
* Credentials are validated before being saved
* Validation is performed using AWS STS `GetCallerIdentity`
* Invalid credentials are not saved
* Users can retry when credential validation fails
* Credentials are stored using the standard AWS configuration location
* Credentials are never hardcoded into the project source code

---

# 🛠️ Planned Utilities

The project will gradually expand into a complete AWS administration toolkit.

### 📦 Inventory & Infrastructure

* [x] EC2 Inventory Reporter
* [ ] S3 Bucket Inventory Auditor
* [ ] AWS Lambda Function Inventory
* [ ] Multi-Region AWS Asset Inventory
* [ ] VPC Infrastructure Mapper
* [ ] AWS Documentation Generator

### 🔐 Security & IAM

* [x] Security Group Exposure Scanner
* [ ] IAM User Security Audit Tool
* [ ] IAM Credential & Access Key Auditor
* [ ] Public S3 Bucket Security Scanner

### 💰 Cost Optimization

* [ ] AWS Cost Explorer Dashboard
* [ ] Unused EBS Volume Detector
* [ ] Orphaned Resource Cleanup Advisor

### 🏷️ Governance & Compliance

* [ ] Resource Tag Compliance Auditor
* [ ] AWS Snapshot Compliance Checker
* [ ] Backup Verification & Recovery Readiness Checker

### 📊 Monitoring & Operations

* [ ] CloudWatch Alarm Health Reporter
* [ ] AWS Environment Health Dashboard
* [ ] Daily AWS Operations Report Generator

### 🤖 Automation

* [ ] EC2 Instance Scheduler

---

# 📁 Project Structure

The GitHub repository contains the application source code and documentation.

```text
aws-admin-toolkit/
│
├── aws_utils/
│   └── session.py
│
├── modules/
│   ├── ec2_inventory.py
│   └── security_groups.py
│
├── .gitignore
├── main.py
├── README.md
├── requirements.txt
└── SECURITY.md
```

Generated files such as Python cache files, PyInstaller build files, and compiled executables are excluded from the source repository through `.gitignore`.

Standalone executable files are distributed separately through **GitHub Releases**.

---

## File Responsibilities

### `main.py`

The main entry point of the application.

It:

* Connects to AWS
* Displays account information
* Provides the interactive CLI menu
* Calls individual AWS utility modules
* Displays module results and summaries

### `aws_utils/session.py`

Responsible for AWS authentication, session management, and first-time configuration.

It:

* Creates Boto3 sessions
* Detects existing credentials
* Validates AWS credentials
* Uses AWS STS to retrieve account information
* Detects missing or invalid credentials
* Provides interactive first-time AWS configuration
* Validates new credentials before saving
* Stores valid AWS configuration locally
* Returns the authenticated session to other modules

### `modules/ec2_inventory.py`

Contains the EC2 inventory logic.

It communicates with the EC2 API and converts AWS responses into structured Python data that can later be used by terminal reports, JSON, CSV, or HTML dashboards.

### `modules/security_groups.py`

Contains the Security Group exposure scanning logic.

It:

* Retrieves Security Groups from the configured AWS region
* Analyzes inbound Security Group rules
* Detects public IPv4 exposure using `0.0.0.0/0`
* Detects public IPv6 exposure using `::/0`
* Identifies dangerous publicly exposed services
* Classifies findings as `CRITICAL`, `WARNING`, or `INFO`
* Generates security recommendations for detected findings

---

# ⚙️ Requirements

Requirements depend on how the toolkit is being used.

## 🪟 Windows Executable

To use the standalone Windows executable, you need:

* Windows
* An AWS account
* AWS Access Key ID and Secret Access Key
* Appropriate IAM permissions

You do **not** need to separately install:

* Python
* Boto3
* AWS CLI

If valid AWS credentials are already configured, the toolkit will automatically use them.

If credentials are not configured, the toolkit will offer to configure them during startup.

---

## 💻 Running from Source

To run the toolkit directly from the source code, make sure you have:

* Python 3.10+
* Boto3
* An AWS account
* Appropriate IAM permissions

Check your Python installation:

```bash
python --version
```

---

# 📥 Installation

There are two ways to use the AWS Admin Utility Toolkit.

## 🪟 Option 1 — Windows Executable (Recommended)

The standalone executable is the easiest way for Windows administrators to use the toolkit.

### 1. Download the Latest Release

Open the repository's **Releases** section and select the latest release.

Download:

```text
AWS-Admin-Toolkit-v0.2.2.exe
```

### 2. Run the Toolkit

Double-click:

```text
AWS-Admin-Toolkit-v0.2.2.exe
```

The AWS Admin Utility Toolkit will open in a terminal window.

No Python installation, repository cloning, virtual environment, AWS CLI, or manual Boto3 installation is required.

### 3. Configure AWS If Required

If valid AWS credentials are already available, the toolkit will connect automatically.

If no credentials are detected:

```text
[WARNING] No AWS credentials were found.

Would you like to configure AWS now? [Y/N]:
```

Select:

```text
Y
```

and provide:

* AWS Access Key ID
* AWS Secret Access Key
* Default AWS Region

The toolkit will validate the credentials before saving them.

After successful validation, the main application will start automatically.

---

## 💻 Option 2 — Install from Source

Developers or users who prefer to run the Python source code can install the toolkit manually.

### 1. Clone the Repository

```bash
git clone https://github.com/Rabih21/aws-admin-toolkit.git
```

Move into the project directory:

```bash
cd aws-admin-toolkit
```

### 2. Create a Virtual Environment

Creating a Python virtual environment is recommended.

#### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

#### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

The current `requirements.txt` contains:

```text
boto3
```

### 4. Run the Toolkit

```bash
python main.py
```

---

# 🔑 AWS Configuration

The toolkit uses standard AWS credentials and does **not** require credentials to be hardcoded into the source code.

There are two supported ways to configure AWS credentials.

## Option 1 — Built-In Configuration

Starting with **v0.2.2**, the recommended approach for standalone Windows users is the built-in configuration process.

When no credentials are detected, the toolkit asks:

```text
Would you like to configure AWS now? [Y/N]:
```

If the user chooses `Y`, the toolkit requests:

```text
AWS Access Key ID:
AWS Secret Access Key:
Default AWS Region [us-east-1]:
```

The Secret Access Key is hidden while being entered.

The credentials are then tested using AWS STS.

Only valid credentials are saved.

---

## Option 2 — AWS CLI Configuration

Users who already use the AWS CLI can continue configuring AWS manually:

```bash
aws configure
```

You will be prompted for:

```text
AWS Access Key ID:
AWS Secret Access Key:
Default region name:
Default output format:
```

Verify authentication using:

```bash
aws sts get-caller-identity
```

The toolkit will automatically use existing valid AWS credentials when available.

---

# 👤 Recommended AWS Permissions

Avoid running the toolkit with the AWS root account.

Create an IAM identity or role with only the permissions required by the utilities you intend to use.

For the currently implemented EC2 Inventory Reporter and Security Group Exposure Scanner, the toolkit requires permission to describe EC2 instances and Security Groups.

For example:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ec2:DescribeInstances",
                "ec2:DescribeSecurityGroups"
            ],
            "Resource": "*"
        }
    ]
}
```

As additional modules are introduced, their required permissions will be documented.

> Avoid creating access keys for the AWS root user. Use an appropriately scoped IAM identity for the toolkit.

---

# ▶️ Running the Toolkit

## Windows Executable

After downloading the standalone Windows release, double-click:

```text
AWS-Admin-Toolkit-v0.2.2.exe
```

No Python command is required.

If AWS credentials are missing, the first-time setup process will automatically be offered.

## Running from Source

If you cloned the repository, run:

```bash
python main.py
```

Both methods launch the same AWS Admin Utility Toolkit interface.

After successful authentication:

```text
============================================================
              AWS ADMIN UTILITY TOOLKIT
============================================================

Connecting to AWS...

[SUCCESS] Connected to AWS

Account ID: 123456789012
Identity:   arn:aws:iam::123456789012:user/cloud-admin
Region:     us-east-1
```

You will then see the main menu:

```text
============================================================

[1] EC2 Inventory Reporter
[2] Security Group Exposure Scanner
[3] Unused EBS Volume Detector
[0] Exit

============================================================

Select an option:
```

Currently, the following utilities are implemented:

### EC2 Inventory Reporter

Select:

```text
1
```

to generate the EC2 inventory.

### Security Group Exposure Scanner

Select:

```text
2
```

to analyze Security Group inbound rules for public exposure and security risks.

The **Unused EBS Volume Detector** (`3`) is planned for the next version.

---

# 🧠 Design Philosophy

The project follows a modular architecture.

Instead of placing all AWS functionality inside one large Python script, each AWS administration capability is implemented as its own module.

```text
                    main.py
                       │
                       ▼
                AWS Session Manager
                       │
          ┌────────────┼────────────┐
          ▼            ▼            ▼
         EC2       Security         Future
      Inventory     Groups          Modules
          │            │               │
          └────────────┼───────────────┘
                       ▼
                    Reports
```

This architecture allows new AWS utilities to be added without rewriting the existing application.

---

# 📊 Future Reporting

AWS modules are designed to return structured data rather than only printing information.

Future versions are planned to support:

```text
AWS APIs
   │
   ▼
Python / Boto3
   │
   ▼
AWS Admin Toolkit
   │
   ├── Terminal
   ├── JSON
   ├── CSV
   └── HTML Dashboard
```

This will allow the same AWS data to be reused for interactive administration, automation, documentation, and reporting.

---

# 🗺️ Roadmap

### v0.1 — Foundation

* [x] AWS Session Management
* [x] STS Authentication Validation
* [x] Account Identification
* [x] Region Detection
* [x] Interactive CLI
* [x] EC2 Inventory Reporter

### v0.2 — Security Group Auditing

* [x] Security Group Exposure Scanner
* [x] IPv4 public exposure detection
* [x] IPv6 public exposure detection
* [x] Dangerous port detection
* [x] Severity classification
* [x] Security recommendations
* [x] Security summary

### v0.2.1 — Windows Standalone Release

* [x] Package the toolkit as a standalone Windows executable
* [x] Bundle the Python runtime and required dependencies
* [x] Publish the executable through GitHub Releases
* [x] Test the executable outside the project directory
* [x] Allow Windows users to run the toolkit without installing Python

### v0.2.2 — First-Time AWS Configuration

* [x] Detect missing AWS credentials
* [x] Detect invalid or expired credentials
* [x] Interactive AWS credential configuration
* [x] AWS Access Key ID configuration
* [x] Hidden Secret Access Key input
* [x] AWS region configuration
* [x] Validate credentials using AWS STS before saving
* [x] Reject invalid credentials
* [x] Allow credential configuration retry
* [x] Save valid AWS configuration locally
* [x] Automatically continue after successful configuration
* [x] Support first-time configuration through the standalone Windows executable

### v0.3 — Storage & Cost Optimization

* [ ] Unused EBS Volume Detector

### v0.4 — IAM & Governance

* [ ] IAM Security Auditor
* [ ] IAM Credential Auditor
* [ ] Resource Tag Compliance Auditor

### v0.5 — S3 & Backup

* [ ] S3 Inventory Auditor
* [ ] Public S3 Security Scanner
* [ ] Snapshot Compliance Checker
* [ ] Backup Verification

### v0.6 — Monitoring & Cost

* [ ] CloudWatch Alarm Health Reporter
* [ ] Cost Explorer Integration
* [ ] Orphaned Resource Advisor

### v1.0 — AWS Environment Auditor

* [ ] Multi-Region Scanning
* [ ] Environment Health Score
* [ ] HTML Dashboard
* [ ] CSV / JSON Export
* [ ] Daily Operations Reports
* [ ] AWS Documentation Generator

---

# 🔒 Security Best Practices

Never hardcode AWS credentials directly into the source code.

Do not commit:

* AWS Access Key IDs
* AWS Secret Access Keys
* AWS Session Tokens
* `.aws/credentials`
* `.env` files containing credentials
* `.pem` files
* SSH private keys
* Other secrets or authentication tokens

If AWS credentials are accidentally exposed, revoke or rotate them immediately.

Use the **principle of least privilege** when creating IAM identities for the toolkit.

---

# ⚠️ Disclaimer

This project is intended for AWS administration, learning, auditing, and authorized cloud environments.

Only run the toolkit against AWS accounts that you own or are authorized to administer.

The toolkit provides findings and recommendations, but administrators should review results within the context of their own AWS architecture before making infrastructure changes.

Some future modules may analyze resources that could generate AWS costs. Always review AWS pricing and permissions before enabling or modifying cloud resources.

---

# 🤝 Contributing

Contributions, suggestions, bug reports, and feature ideas are welcome.

If you would like to contribute:

1. Fork the repository
2. Create a new branch
3. Make your changes
4. Test your changes
5. Submit a pull request

When adding a new AWS utility:

* Keep functionality modular
* Avoid hardcoding AWS credentials
* Avoid hardcoding Account IDs
* Avoid hardcoding regions
* Avoid hardcoding resource identifiers
* Handle AWS API errors
* Document required IAM permissions
* Prefer structured return data
* Prefer read-only behavior for auditing utilities

Generated files such as `build/`, `dist/`, `__pycache__/`, and PyInstaller `.spec` files should not be committed to the source repository.

---

# 📄 License

This project is intended as an open-source AWS administration utility.

Add the appropriate license file to the repository before distributing or accepting external contributions.

---

# ⭐ Project Goal

The long-term goal is to turn **AWS Admin Utility Toolkit** into a practical command-line assistant for cloud administrators:

> **One Python toolkit to inventory, audit, monitor, secure, optimize, and document an AWS environment.**

The project is designed around a simple idea:

> **Download → Connect → Audit → Understand**

Built with **Python**, **Boto3**, and **AWS**.

```

One important improvement I made here is that the README no longer tells `.exe` users they need **AWS CLI**. With v0.2.2, the standalone application can write the standard AWS credential/config files itself, so requiring AWS CLI would defeat part of the convenience we've just built.
```
