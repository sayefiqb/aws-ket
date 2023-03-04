import sys
import os
import boto3
from pytest import mark

sys.path.append('../../src')
import initialize
import cleanup

    
client_kms = boto3.client('kms')
client_s3 = boto3.client('s3')
client_iam = boto3.client('iam')

# Create a cleanup job that will remove the S3 and kms key with alias.
def test_setup():
    cleanup.cleanup_kms()
    cleanup.cleanup_s3()

# Test with no kms
# Test with a KMS that aleady exists
# Test with random kms name

def test_check_alias():
    test_setup()
    # If KMS key does not exist
    assert initialize.check_alias('alias/aws_ket') == None
    # If kms key exists
    response = client_kms.create_key(Description='AWS KET KMS KEY', KeyUsage='ENCRYPT_DECRYPT', Origin='AWS_KMS')
    key_id = response['KeyMetadata']['KeyId']
    response = client_kms.create_alias(AliasName='alias/aws_ket', TargetKeyId=key_id)
    assert initialize.check_alias('alias/aws_ket') == 'alias/aws_ket'
    

def test_create_alias():
    test_setup()
    response = client_kms.create_key(Description='AWS KET KMS KEY', KeyUsage='ENCRYPT_DECRYPT', Origin='AWS_KMS')
    key_id = response['KeyMetadata']['KeyId']

    assert initialize.create_alias(key_id,'alias/aws_ket') == "Alias Created"
    
    assert initialize.create_alias('','') == 'ValidationException'
 
    assert initialize.create_alias('test','test') == 'ValidationException'
    
    assert initialize.create_alias(key_id,'test') == "ValidationException"
   
    assert initialize.create_alias(key_id,'alias/aws_ket') == 'AlreadyExistsException'

# Create kms
def test_create_key():
    test_setup()
    assert initialize.create_key('alias/aws_ket') == ("KMS key created successfully")

# Test with no access key setup
# test with incorrect access key setup
def test_get_iam__user():
    assert initialize.get_iam_user() == "sayef"

# Test with no IAM access key
# Test other scenarios
def test_get_bucket_name():
    assert initialize.get_bucket_name() == 'aws-ket-sayef-2023'

# Test if bucket does not exists
# Test if bucket exists
def test_check_s3_bucket():
    assert initialize.check_s3_bucket("aws-ket-sayef-2023") == None

# Test if already intialized
# Test if it is new setup
def test_create_s3_bucket():
    assert initialize.create_s3_bucket() == "Initialization Complete"



if __name__ == '__main__':
    test_check_alias()
    test_create_alias()
    test_create_key()
    test_get_iam__user()
    test_get_bucket_name()
    test_check_s3_bucket()
    test_create_s3_bucket()
