import boto3
import unittest
from moto import mock_aws
from scripts.rds_remove_public_access import rds_remove_public_access


class TestRDSPublicAccess(unittest.TestCase):

    @mock_aws
    def test_rds_remove_public_access(self):
        rds = boto3.client("rds")
        instance_name = "public-rds"

        rds.create_db_instance(
            DBInstanceIdentifier=instance_name,
            DBInstanceClass="db.t3.micro",
            Engine="postgres",
            MasterUsername="postgres",
            MasterUserPassword="SuperSecretAndSecurePassword",
            PubliclyAccessible=True,
        )

        rds_remove_public_access()

        instances = rds.describe_db_instances()

        for instance in instances["DBInstances"]:
            self.assertFalse(instance["PubliclyAccessible"])


if __name__ == "__main__":
    unittest.main()
