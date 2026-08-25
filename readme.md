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

The current version includes the foundation of the toolkit, the EC2 Inventory Reporter, the Security Group Exposure Scanner, standalone Windows executable support, and built-in first-time AWS credential configuration.

### ✅ Currently Implemented

#### AWS Authentication & Session Management

The toolkit:

* Creates an AWS session using Boto3
* Uses locally configured AWS credentials when available
* Validates authentication using AWS STS
* Retrieves the AWS Account ID
* Displays the authenticated IAM identity
* Detects the configured AWS region
* Handles missing or incomplete AWS credentials
* Detects invalid or expired AWS credentials
* Offers interactive AWS credential configuration when credentials are missing
* Hides the AWS Secret Access Key while it is entered
* Validates new credentials using AWS STS before saving them
* Saves valid credentials using the standard AWS configuration files
* Automatically continues to the toolkit after successful configuration

#### EC2 Inventory Reporter

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
```

---

### 🛡️ Module 2 — Security Group Exposure Scanner

The Security Group Exposure Scanner analyzes inbound rules across Security Groups in the configured AWS region.

It detects public exposure through:

* `0.0.0.0/0`
* `::/0`

Each public rule is classified as:

* `CRITICAL` — Dangerous service publicly exposed
* `WARNING` — Other public port requiring review
* `INFO` — Common public service such as HTTP/HTTPS

Currently detected critical services:

| Port | Service |
| ---: | -------------------- |
| 22 | SSH |
| 3389 | RDP |
| 3306 | MySQL |
| 5432 | PostgreSQL |
| 1433 | Microsoft SQL Server |
| 6379 | Redis |

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

### 🪟 Standalone Windows Executable

Starting with **v0.2.1**, Windows users can run the AWS Admin Utility Toolkit using a standalone executable.

This means Windows users do not need to:

* Install Python
* Install Boto3 manually
* Clone the GitHub repository
* Create a Python virtual environment
* Run the application using Python commands

The Windows executable is distributed through **GitHub Releases**.

Starting with **v0.2.2**, users who do not already have AWS credentials configured can configure them directly from inside the toolkit.

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

```text
aws-admin-toolkit/
│
├── main.py
├── requirements.txt
├── README.md
├── SECURITY.md
├── .gitignore
│
├── aws_utils/
│   └── session.py
│
└── modules/
    ├── ec2_inventory.py
    └── security_groups.py
```

Generated files such as `build/`, `dist/`, `__pycache__/`, and PyInstaller `.spec` files are excluded from the source repository through `.gitignore`.

Standalone executable files are distributed separately through **GitHub Releases**.

### File Responsibilities

**`main.py`**

The main entry point of the application.

It:

* Connects to AWS
* Displays account information
* Provides the interactive CLI menu
* Calls individual AWS utility modules

**`aws_utils/session.py`**

Responsible for AWS authentication and session management.

It:

* Creates the Boto3 session
* Validates AWS credentials
* Uses STS to retrieve account information
* Detects missing, invalid, or expired credentials
* Provides interactive first-time AWS credential configuration
* Validates new credentials before saving them
* Saves valid credentials using standard AWS configuration files
* Returns the session to other modules

**`modules/ec2_inventory.py`**

Contains the EC2 inventory logic.

It communicates with the EC2 API and converts AWS responses into structured Python data that can later be used by terminal reports, JSON, CSV, or HTML dashboards.

**`modules/security_groups.py`**

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

### Windows Executable

For the standalone Windows release:

* Windows
* An AWS account
* AWS Access Key ID and Secret Access Key
* Appropriate IAM permissions

Python, Boto3, and AWS CLI do **not** need to be installed separately.

If valid AWS credentials are not already configured, the toolkit will offer to configure them during startup.

### Running from Source

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

## 1. Windows Executable

For Windows users, the standalone executable is the easiest way to use the toolkit.

Open the repository's **Releases** section and download:

```text
AWS-Admin-Toolkit-v0.2.2.exe
```

Double-click the executable to start the toolkit.

No Python installation, repository cloning, virtual environment, AWS CLI, or manual Boto3 installation is required.

If AWS credentials are not detected, the toolkit will offer to configure them directly from the application.

---

## 2. Install from Source

Clone the repository:

```bash
git clone https://github.com/Rabih21/aws-admin-toolkit.git
```

Move into the project directory:

```bash
cd aws-admin-toolkit
```

---

## 3. Create a Virtual Environment

Creating a Python virtual environment is recommended.

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

## 4. Install Dependencies

```bash
pip install -r requirements.txt
```

The current `requirements.txt` contains:

```text
boto3
```

---

# 🔑 AWS Configuration

The toolkit **does not require AWS access keys to be stored inside the source code**.

Starting with **v0.2.2**, AWS credentials can be configured directly from the toolkit if no valid credentials are detected.

When credentials are missing, the toolkit will display:

```text
[WARNING] No AWS credentials were found.

Would you like to configure AWS now? [Y/N]:
```

If the user chooses `Y`, the toolkit will request:

```text
AWS Access Key ID:
AWS Secret Access Key:
Default AWS Region [us-east-1]:
```

The AWS Secret Access Key is hidden while being entered.

Before saving the credentials, the toolkit validates them using AWS STS.

Example:

```text
Testing AWS credentials...

[SUCCESS] AWS credentials verified.

Account ID: 123456789012
Identity:   arn:aws:iam::123456789012:user/cloud-admin
Region:     us-east-1

[SUCCESS] AWS configuration saved successfully.
```

If credentials are invalid, they are rejected and the user can try again.

Users who already have AWS credentials configured can continue using their existing configuration. The toolkit will automatically detect and use valid credentials.

AWS CLI users can also configure credentials manually:

```bash
aws configure
```

Verify authentication using:

```bash
aws sts get-caller-identity
```

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

---

# ▶️ Running the Toolkit

### Windows Executable

After downloading the latest Windows release, double-click:

```text
AWS-Admin-Toolkit-v0.2.2.exe
```

If AWS credentials are missing, the toolkit will offer the first-time AWS configuration process automatically.

### Running from Source

Start the program with:

```bash
python main.py
```

The toolkit will attempt to authenticate with AWS.

Example:

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
* [x] Detect invalid or expired AWS credentials
* [x] Interactive AWS credential configuration
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

# ⚠️ Disclaimer

This project is intended for AWS administration, learning, auditing, and authorized cloud environments.

Only run the toolkit against AWS accounts that you own or are authorized to administer.

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

When adding a new AWS utility, keep the project modular and avoid hardcoding AWS credentials, account IDs, regions, or resource identifiers.

---

# 📄 License

This project is intended as an open-source AWS administration utility.

Add the appropriate license file to the repository before distributing or accepting external contributions.

---

# ⭐ Project Goal

The long-term goal is to turn **AWS Admin Utility Toolkit** into a practical command-line assistant for cloud administrators:

> **One Python toolkit to inventory, audit, monitor, secure, optimize, and document an AWS environment.**

Built with **Python**, **Boto3**, and **AWS**.