import boto3


def rds_remove_public_access():
    """
    Disables public accessibility from any
    Amazon RDS database instances that is public.

    * Get all RDS instances in the account
    * Identify public instances
    * Remove public access
    """
    rds = boto3.client("rds")

    instances = rds.describe_db_instances()

    for instance in instances["DBInstances"]:

        try:
            instance_name = instance["DBInstanceIdentifier"]
            if instance["PubliclyAccessible"]:
                print(f"RDS instance {instance_name} as public access")
                rds.modify_db_instance(
                    DBInstanceIdentifier=instance_name,
                    PubliclyAccessible=False
                )
                print(
                    f"Public access removed from RDS instance {instance_name}"
                )
        except Exception as e:
            print(e)


if __name__ == "__main__":
    rds_remove_public_access()
