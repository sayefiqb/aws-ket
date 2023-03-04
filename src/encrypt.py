# TO DO

# Better logging
# Support for sending to other backend stoorage
# Reusable codde
# Better loggiing
# Handle exceptions
# What happens if AWS Creds not provided?

import boto3
import botocore
from pprint import pprint

client_kms = boto3.client("kms")
client_s3 = boto3.resource("s3")


def encrypt_text(kms_key, text):
    try:
        encrypted_kms_request = client_kms.encrypt(KeyId=kms_key, Plaintext=text)
        encrypted_string = encrypted_kms_request["CiphertextBlob"]
        return encrypted_string
    except botocore.exceptions.ClientError as error:
        response = error.response
        if response["Error"]["Code"] == "NotFoundException" and response["ResponseMetadata"]["HTTPStatusCode"] == 400:
            print(f'The KMS Key you provided does not exist.')
        if response['Error']['Code'] == "ValidationException" and response["ResponseMetadata"]["HTTPStatusCode"] == 400:
            print('The text you provided must be greater than 0 characters in length')
    except botocore.exceptions.ParamValidationError as param_error:
        print(param_error)


def encrypt_file(kms_key, file_name):
    file = open(file_name, "r")
    encrypted_kms_request = client_kms.encrypt(KeyId=kms_key, Plaintext=file.read())
    encrypted_string = encrypted_kms_request["CiphertextBlob"]

    return encrypted_string


def push_to_s3(bucket, file_name, encrypted_text):
    try:
        client_s3.Bucket(bucket).put_object(Key=file_name, Body=encrypted_text)
    except botocore.exceptions.ClientError as error:
        response = error.response
        if response["Error"]["Code"] == "NoSuchBucket" and response["ResponseMetadata"]["HTTPStatusCode"] == 404:
            print(f'The specified bucket: {bucket} does not exist')
    except botocore.exceptions.ParamValidationError as param_error:
        print(param_error)
   