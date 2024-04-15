# boto3-playground 
Some boto3 scripts to interact with the AWS Services

## Description

* This repo uses boto3 and Python to interact with the AWS API, allowing for the automation of repetitive tasks within an AWS account.
* Implements moto to mock AWS infrastructure and test written code.

## Prerequisites

* **Python 3** (Develop and tested with 3.10.12)
* **AWS Credentials:** The scripts assume you have valid AWS credentials and permissions.

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/hb4y/boto3-playground.git
   ```

2. **Install dependencies:**
   ```bash
   cd boto3-playground
   pip install -r requirements.txt 
   ```

## Usage
### Scripts

- **S3 Remove public access from bucket:**
  * Check if the s3 buckets have public access, if that is the case remove it to avoid undesired access.
  * Example usage:
   ```bash
   python3 scripts/s3_remove_public_access.py
   ```

- **RDS Remove public access from RDS instance:**
  * Check if the RDS Instances have public access, if that is the case remove it to avoid undesired access.
  * Example usage:
   ```bash
   python3 scripts/rds_remove_public_access.py
   ```

- **EC2/IAM Remove SSM policy from the IAM roles of EC2 instances:**
  * Check if the EC2 account instances have assigned the SSM policy on their roles, if that is the case remove that policy from all instances.
  * Example usage:
   ```bash
   python3 scripts/ec2_remove_ssm_policy.py
   ```

### Testing

* Each script has its own test. The tests can be run separately or all at once

1. **Run individual tests:**
   ```bash
   python3 -m unittest test/test_s3_remove_public_access.py
   python3 -m unittest test/test_rds_remove_public_access.py
   python3 -m unittest test/test_ec2_remove_ssm_policy.py
   ```

2. **Run all tests:**
   ```bash
   python3 -m unittest discover test/
   ```

## Development Tools

* **pycodestyle**: Former called pep8 it enforces Python code style guidelines.
* **boto3**: Enables interaction with AWS services.
* **unittest**: Provides a framework for unit testing in Python.
* **moto**: Facilitates mocking of AWS infrastructure components for testing.
