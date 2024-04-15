import boto3
import unittest
import boto3.ec2
import json
from moto import mock_aws
from scripts.ec2_remove_ssm_policy import ec2_remove_ssm_policy


class TestRemoveSSMPolicy(unittest.TestCase):
    @mock_aws
    def test_ec2_remove_ssm_policy(self):
        ec2 = boto3.client("ec2", region_name="us-east-1")
        iam = boto3.client("iam", region_name="us-east-1")
        assume_role_policy_document = json.dumps(
            {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Sid": "",
                        "Effect": "Allow",
                        "Principal": {"Service": "ec2.amazonaws.com"},
                        "Action": "sts:AssumeRole",
                    }
                ],
            }
        )
        mock_ssm_policy = """{
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "ssm:DescribeAssociation",
                    "ssm:GetDeployablePatchSnapshotForInstance",
                    "ssm:GetDocument",
                    "ssm:DescribeDocument",
                    "ssm:GetManifest",
                    "ssm:GetParameter",
                    "ssm:GetParameters",
                    "ssm:ListAssociations",
                    "ssm:ListInstanceAssociations",
                    "ssm:PutInventory",
                    "ssm:PutComplianceItems",
                    "ssm:PutConfigurePackageResult",
                    "ssm:UpdateAssociationStatus",
                    "ssm:UpdateInstanceAssociationStatus",
                    "ssm:UpdateInstanceInformation"
                ],
                "Resource": "*"
            },
            {
                "Effect": "Allow",
                "Action": [
                    "ssmmessages:CreateControlChannel",
                    "ssmmessages:CreateDataChannel",
                    "ssmmessages:OpenControlChannel",
                    "ssmmessages:OpenDataChannel"
                ],
                "Resource": "*"
            },
            {
                "Effect": "Allow",
                "Action": [
                    "ec2messages:AcknowledgeMessage",
                    "ec2messages:DeleteMessage",
                    "ec2messages:FailMessage",
                    "ec2messages:GetEndpoint",
                    "ec2messages:GetMessages",
                    "ec2messages:SendReply"
                ],
                "Resource": "*"
            }
        ]
    }"""
        mock_name = 'mock-ec2'

        ec2_role = iam.create_role(
            RoleName=mock_name,
            AssumeRolePolicyDocument=assume_role_policy_document
        )

        instance_profile = iam.create_instance_profile(
            InstanceProfileName=mock_name
        )

        iam.add_role_to_instance_profile(
            InstanceProfileName=mock_name,
            RoleName=ec2_role['Role']['RoleName']
        )

        ec2.run_instances(
            ImageId="al2023-ami-2023.4.20240401.1-kernel-6.1-x86_64",
            MinCount=1,
            MaxCount=1,
            IamInstanceProfile={
                "Arn": instance_profile["InstanceProfile"]["Arn"]},
        )

        mock_ssm_policy = iam.create_policy(
            PolicyName="AmazonSSMManagedInstanceCore",
            PolicyDocument=mock_ssm_policy,
        )

        iam.attach_role_policy(
            RoleName=ec2_role['Role']['RoleName'],
            PolicyArn=mock_ssm_policy["Policy"]["Arn"]
        )

        ec2_remove_ssm_policy()

        iam_role_name = ec2_role['Role']['RoleName']
        attached_policies = iam.list_attached_role_policies(
                        RoleName=iam_role_name
                    )

        for policy in attached_policies['AttachedPolicies']:
            print(policy['PolicyName'])
            self.assertNotEqual(policy['PolicyName'],
                                'AmazonSSMManagedInstanceCore')


if __name__ == "__main__":
    unittest.main()
