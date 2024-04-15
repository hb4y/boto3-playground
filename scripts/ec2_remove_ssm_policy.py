import boto3


RM_POLICY = "AmazonSSMManagedInstanceCore"


def ec2_remove_ssm_policy():
    """
    Removes the 'AmazonSSMManagedInstanceCore' policy from EC2 instance roles.

    * Connects to EC2 and IAM services
    * Fetch a list of EC2 instaces
    * Iterates through each instaces
      - Read IAM profile
      - List polices
      - If 'AmazonSSMManagedInstanceCore' is present deatach
    """
    ec2 = boto3.client("ec2")
    iam = boto3.client("iam")

    ec2_instances = ec2.describe_instances()

    for reservation in ec2_instances["Reservations"]:
        try:
            for instance in reservation["Instances"]:
                iam_instance_profile = instance.get("IamInstanceProfile")

                if iam_instance_profile:
                    iam_role_name = iam_instance_profile["Arn"].split("/")[-1]
                    attached_policies = iam.list_attached_role_policies(
                        RoleName=iam_role_name
                    )

                    for policy in attached_policies["AttachedPolicies"]:
                        if policy["PolicyName"] == RM_POLICY:
                            print(
                                f"EC2 Role {iam_role_name} has {RM_POLICY}")
                            iam.detach_role_policy(
                                RoleName=iam_role_name,
                                PolicyArn=policy["PolicyArn"]
                            )
                            print(
                                f"{RM_POLICY} removed from {iam_role_name}")
        except Exception as e:
            print(e)


if __name__ == "__main__":
    ec2_remove_ssm_policy()
