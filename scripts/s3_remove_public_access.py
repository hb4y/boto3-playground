import boto3


def s3_remove_public_acess():
    """
    Removes public access all accessible S3 buckets in an AWS account.

    * Iterates through all S3 buckets
    * Check existing configuration
    * Enforce private configuration
    """
    s3 = boto3.client("s3")
    response = s3.list_buckets()
    private_configuration = {
        "BlockPublicAcls": True,
        "IgnorePublicAcls": True,
        "BlockPublicPolicy": True,
        "RestrictPublicBuckets": True,
    }
    for bucket in response["Buckets"]:
        bucket_name = bucket["Name"]

        try:
            public_access_block = s3.get_public_access_block(
                Bucket=bucket_name)
            current_configuration = public_access_block[
                "PublicAccessBlockConfiguration"
            ]

            for policy in current_configuration:
                if not current_configuration[policy]:
                    print(f"Bucket {bucket_name} as public access")
                    s3.put_public_access_block(
                        Bucket=bucket_name,
                        PublicAccessBlockConfiguration=private_configuration,
                    )
                    print(f"Public access removed from bucket {bucket_name}")
                    break

        except Exception as e:
            print(e)


if __name__ == "__main__":
    s3_remove_public_acess()
