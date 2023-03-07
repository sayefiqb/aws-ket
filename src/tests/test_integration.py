from src import(encrypt_text, encrypt_file, decrypt_text, push_to_s3)
from moto import mock_s3, mock_kms, mock_iam
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


class KETIntegrationTest(unittest.TestCase):
    mock_s3 = mock_s3()
    mock_kms = mock_kms()
    mock_iam = mock_iam()
    
    user_name = 'default-user'
    bucket_name = "aws-ket"
    region_name = 'us-east-2'
    remote_file_name = 'test'
    local_file_name = 'src/tests/sample.txt'
    content = 'This is a test string!'
    alias_name = 'alias/test'
    kms_key_id = ''
    
    
    
    def setUp(self):
        self.mock_s3.start()

        # S3 Setup
        s3 = boto3.client("s3",self.region_name)
        response = s3.create_bucket(
            ACL='private',
            Bucket=self.bucket_name,
            CreateBucketConfiguration={'LocationConstraint': self.region_name},
            ObjectLockEnabledForBucket=True,
            ObjectOwnership='BucketOwnerEnforced',
        )
               
        # KMS Setup
        self.mock_kms.start()
        kms = boto3.client('kms', self.region_name)
        kms_key_response = kms.create_key(
            Description='AWS KET KMS KEY', KeyUsage='ENCRYPT_DECRYPT', Origin='AWS_KMS'
        )
        kms.create_alias(AliasName=self.alias_name, TargetKeyId=kms_key_response['KeyMetadata']['KeyId'])
        self.kms_key_id = kms_key_response['KeyMetadata']['KeyId']
        
        # IAM Setup
        self.mock_iam.start()
      
    def tearDown(self):
        self.mock_s3.stop()
        self.mock_kms.stop()
        self.mock_iam.stop()


    def test_encrypton_decryption_of_text(self):
        encrypted_string = encrypt_text(self.kms_key_id, self.content, self.region_name)
        push_to_s3(self.bucket_name, self.remote_file_name, encrypted_string, self.region_name)
        decrypted_string = decrypt_text(self.bucket_name,  self.remote_file_name, self.kms_key_id, self.region_name)
        assert decrypted_string == self.content


    def test_encryption_decryption_of_file(self):
        encrypted_file = encrypt_file(self.kms_key_id, self.local_file_name, self.region_name)
        push_to_s3(self.bucket_name, self.remote_file_name, encrypted_file, self.region_name)
        decrypted_string = decrypt_text(self.bucket_name, self.remote_file_name, self.kms_key_id, self.region_name)
        print('im here so far')
        print(os.getcwd())
        f = open(self.local_file_name, 'r')
        file_content = f.readline()
        assert decrypted_string == file_content
        f.close()


if __name__ == '__main__':
    unittest.main()
