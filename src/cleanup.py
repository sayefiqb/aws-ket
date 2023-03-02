#!/usr/bin/env python

import os
import boto3
import botocore
from helper import s3_helper


client_kms = boto3.client('kms')
client_s3 = boto3.client('s3')
client_iam = boto3.client('iam')
resource_s3 = boto3.resource('s3')

bucket_name = os.environ.get('S3_BUCKET')
kms_key_id = os.environ.get('KMS_KEY_ID')


def cleanup_kms():
    try:
        alias_response = client_kms.delete_alias(AliasName='alias/aws_ket')
        kms_key_response = client_kms.disable_key(KeyId=kms_key_id)
        print('KMS Alias and Key have been disabled!')
        return kms_key_response
    except botocore.exceptions.ClientError as error:
        response = error.response
        if response["Error"]["Code"] == "NotFoundException" or response["ResponseMetadata"]["HTTPStatusCode"] == 400:
            print(f'The Alias has already been removed')


def cleanup_s3():
    try:
        s3_helper.permanently_delete_object(bucket_name)
        bucket = resource_s3.Bucket(bucket_name)
        bucket.objects.all().delete()
        client_s3.delete_bucket(Bucket=bucket_name)
        print('Cleaned up S3!')
    except botocore.exceptions.ClientError as error:
        response = error.response
        if response["Error"]["Code"] == "NoSuchBucket" or response["ResponseMetadata"]["HTTPStatusCode"] == 404:
            print(f'The S3 bucket was already deleted')


if __name__ == "__main__":
    cleanup_kms()
    cleanup_s3()
