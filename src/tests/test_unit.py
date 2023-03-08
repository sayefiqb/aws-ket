from moto import mock_s3, mock_kms, mock_iam
from src import create_kms_alias, create_kms_key, create_s3_bucket, check_alias, get_iam_user, push_to_s3
import boto3
import os
import pytest
import unittest


@pytest.fixture(scope="function")
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "us-east-1"


class KETUnitTest(unittest.TestCase):
    mock_s3 = mock_s3()
    mock_kms = mock_kms()
    mock_iam = mock_iam()

    user_name = 'default-user'
    bucket_name = "aws-ket"
    region_name = 'us-east-2'
    remote_file_name = 'test'
    content = 'This is a test string!'
    alias_name = 'alias/test'

    def setUp(self):
        self.mock_s3.start()

        # S3 Setup
        s3 = boto3.client("s3", self.region_name)
        response = s3.create_bucket(
            ACL='private',
            Bucket=self.bucket_name,
            CreateBucketConfiguration={'LocationConstraint': 'us-east-2'},
            ObjectLockEnabledForBucket=True,
            ObjectOwnership='BucketOwnerEnforced',
        )
        s3.put_object(Bucket=self.bucket_name, Key=self.remote_file_name, Body=self.content)

        # KMS Setup
        self.mock_kms.start()

        # IAM Setup
        self.mock_iam.start()

    def tearDown(self):
        self.mock_s3.stop()
        self.mock_kms.stop()
        self.mock_iam.stop()

    def test_get_iam_user(self):
        assert get_iam_user()['UserName'] == 'default_user'

    def test_create_s3_bucket(self):
        create_s3_bucket(self.bucket_name, self.region_name)
        s3 = boto3.client("s3", self.region_name)
        result = s3.list_buckets()
        assert len(result["Buckets"]) == 1
        assert result["Buckets"][0]["Name"] == "aws-ket"

    def test_push_to_s3(self):
        push_to_s3(self.bucket_name, self.remote_file_name, self.content, self.region_name)
        s3 = boto3.client("s3", self.region_name)

        result = s3.list_objects(Bucket=self.bucket_name)
        assert len(result["Contents"]) == 1
        assert result["Contents"][0]["Key"] == "test"

    def test_create_kms_key(self):
        key_id = create_kms_key(self.region_name)
        kms = boto3.client('kms', self.region_name)
        kms_keys = kms.list_keys()
        assert len(kms_keys['Keys']) == 1
        assert kms_keys['Keys'][0]['KeyId'] == key_id

    def test_create_kms_alias(self):
        kms = boto3.client('kms', self.region_name)
        response = kms.create_key(Description='AWS KET KMS KEY', KeyUsage='ENCRYPT_DECRYPT', Origin='AWS_KMS')
        create_kms_alias(response['KeyMetadata']['KeyId'], self.alias_name, self.region_name)
        kms_alias = kms.list_aliases(KeyId=response['KeyMetadata']['KeyId'])
        assert len(kms_alias['Aliases']) == 1
        assert kms_alias['Aliases'][0]['AliasName'] == self.alias_name

    def test_check_alias(self):
        # Before creating any KMS Key
        assert check_alias(self.alias_name, self.region_name) == None

        kms = boto3.client('kms', self.region_name)
        kms_key_response = kms.create_key(Description='AWS KET KMS KEY', KeyUsage='ENCRYPT_DECRYPT', Origin='AWS_KMS')
        kms.create_alias(AliasName=self.alias_name, TargetKeyId=kms_key_response['KeyMetadata']['KeyId'])

        # After creating the alias
        assert check_alias(self.alias_name, self.region_name) == self.alias_name


if __name__ == '__main__':
    unittest.main()
