#!/usr/bin/env python

import os
import boto3
import botocore


client_kms = boto3.client('kms')
client_s3 = boto3.client('s3')
client_iam = boto3.client('iam')
resource_s3 = boto3.resource('s3')




def get_iam_user():
    try:
        client_iam = boto3.client('iam')
        response = client_iam.get_user()
        return response['User']['UserId']
    except botocore.exceptions.ClientError as error:
        response = error.response
        if (
            response["Error"]["Code"] == "UnrecognizedClientException"
            and response["ResponseMetadata"]["HTTPStatusCode"] == 400
        ):
            print("Invalid AWS Client Token")
            return "UnrecognizedClientException"
        if response["Error"]["Code"] == "AccessDenied" and response["ResponseMetadata"]["HTTPStatusCode"] == 403:
            print(response['Error']['Message'])


def cleanup_s3(bucket_name, region):
    try:
        permanently_delete_object(bucket_name,region)
        bucket = resource_s3.Bucket(bucket_name)
        bucket.objects.all().delete()
        client_s3.delete_bucket(Bucket=bucket_name)
        print('Cleaned up S3!')
    except botocore.exceptions.ClientError as error:
        response = error.response
        if response["Error"]["Code"] == "NoSuchBucket" or response["ResponseMetadata"]["HTTPStatusCode"] == 404:
            print(f'The S3 bucket was already deleted')

def permanently_delete_object(bucket_name,region object_key=None):
    """
    Permanently deletes a versioned object by deleting all of its versions.

    :param bucket: The bucket that contains the object.
    :param region: The region S3 was created in.
    :param object_key: The object to delete.
    """
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket_name)
    print(f'Deleting {bucket_name} ...')
    try:
        if object_key:
            bucket.object_versions.filter(Prefix=object_key).delete()
            print(f"Permanently deleted all versions of object {object_key} in {bucket_name}.",)
        else:
            bucket.object_versions.delete()
            print(f"Permanently deleted all versions of all objects in {bucket_name}.")
    except botocore.exceptions.ClientError:
        print(f"Couldn't delete all versions of {object_key} in {bucket_name}.")
        

if __name__ == "__main__":
    region = 'us-east-1'
    user_name = get_iam_user().lower()
    bucket_name = f'aws-ket-{user_name}'
    cleanup_s3()
