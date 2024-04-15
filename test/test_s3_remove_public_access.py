import boto3
import unittest
from moto import mock_aws
from scripts.s3_remove_public_access import s3_remove_public_acess


class TestS3PublicAccess(unittest.TestCase):

    @mock_aws
    def test_s3_remove_public_access(self):
        s3 = boto3.client("s3")
        bucket_name = "public-bucket"
        public_configuration = {
            "BlockPublicAcls": False,
            "IgnorePublicAcls": False,
            "BlockPublicPolicy": False,
            "RestrictPublicBuckets": False,
        }

        s3.create_bucket(Bucket=bucket_name)

        s3.put_public_access_block(
            Bucket=bucket_name,
            PublicAccessBlockConfiguration=public_configuration
        )

        s3_remove_public_acess()

        public_access_block = s3.get_public_access_block(Bucket=bucket_name)
        current_configuration = public_access_block[
                                    "PublicAccessBlockConfiguration"
                                ]

        for policy in current_configuration:
            self.assertTrue(current_configuration[policy])


if __name__ == "__main__":
    unittest.main()
