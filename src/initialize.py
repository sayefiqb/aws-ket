#!/usr/bin/env python

# TO DO
# Be able to create kms in any reegion
# Be able to create s3 in any region sepcified
# Be able to initallize DynamoDB backend
# Handle all kinds of exeption
# Input based initalization


import os
import boto3
from datetime import datetime

client_kms = boto3.client('kms')
client_s3 = boto3.client('s3')
client_iam = boto3.client('iam')

ALIAS_NAME = 'alias/aws_ket'



def create_key():
    alias_name = check_kms_key()
    if alias_name is None:
        response = client_kms.create_key(Description='AWS KET KMS KEY', KeyUsage='ENCRYPT_DECRYPT', Origin='AWS_KMS')
        key_id = response['KeyMetadata']['KeyId']
        cmd = f'export KMS_KEY_ID={key_id}'
        os.system(cmd)
        global KMS_KEY_ID
        KMS_KEY_ID = key_id
        create_alias(key_id)
        print('KMS key created successfully')
        return 'KMS key created successfully'
    else:
        print('KMS key already exists')
        return "KMS key already exists"


def check_kms_key():
    aliases = client_kms.list_aliases()
    alias_name = None
    for alias in aliases['Aliases']:
        if ALIAS_NAME in alias['AliasName']:
            alias_name = ALIAS_NAME
    return alias_name


def create_alias(key_id):
    response = client_kms.create_alias(AliasName=ALIAS_NAME, TargetKeyId=key_id)
    print('Alias for KMS key created successfuly')


def get_iam_user():
    response = client_iam.get_user()
    user_name = response['User']['UserName']
    print(f'Found AWS user {user_name}')
    return user_name


def get_bucket_name():
    iam_user_name = get_iam_user()
    dateTimeObj = datetime.today().strftime('%Y')
    timestampStr = str(dateTimeObj)
    bucket_name = f'aws-ket-{iam_user_name}-{timestampStr}'
    return bucket_name


def check_s3_bucket(bucket_name):
    buckets = client_s3.list_buckets()
    queried_bucket_name = None
    for bucket in buckets['Buckets']:
        if bucket_name == bucket['Name']:
            queried_bucket_name = bucket_name
    return queried_bucket_name


def create_s3_bucket():
    bucket_name = get_bucket_name()
    queried_bucket_name = check_s3_bucket(bucket_name)
    if queried_bucket_name is None:
        response = client_s3.create_bucket(
            ACL='private',
            Bucket=bucket_name,
            CreateBucketConfiguration={'LocationConstraint': 'us-east-2'},
            ObjectLockEnabledForBucket=True,
            ObjectOwnership='BucketOwnerEnforced',
        )
        os.environ['S3_BUCKET'] = bucket_name
        global S3_BUCKET
        S3_BUCKET = bucket_name
        print('Created S3 bucket successfully')
        print('Initialization Complete')
        print_instructions()
        return 'Initialization Complete'
    else:
        print(f'The bucket with {bucket_name} name already exists.')
        print('Skipping initialization')
        return 'Skipping initialization'

def print_instructions():
    kms = f'export KMS_KEY_ID={KMS_KEY_ID}'
    s3 = f'export S3_BUCKET={S3_BUCKET}'
    ch="*"
    sp=" "
    print('Update your environment variables with the followin in order to use aws-ket ')
    print(ch*(10+len(kms))) # print *
    print(ch + (sp*(8+len(kms)))+ ch)
    print("* " + kms +(sp*(7))+ch)
    print("* " + s3 + " *")
    print(ch + (sp*(8+len(kms)))+ ch)
    print(ch*(10+len(kms))) # print *

def initialize():
    create_key()
    create_s3_bucket()


if __name__ == "__main__":
    initialize()
