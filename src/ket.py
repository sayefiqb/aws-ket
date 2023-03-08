#!/usr/bin/env python

# TO DO
# Be able to initallize DynamoDB backend

import boto3
import botocore


def get_iam_user():
    try:
        client_iam = boto3.client('iam')
        response = client_iam.get_user()
        return response['User']
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


def create_s3_bucket(bucket_name, region):
    try:
        client_s3 = boto3.client('s3', region_name=region)
        response = client_s3.create_bucket(
            ACL='private',
            Bucket=bucket_name,
            CreateBucketConfiguration={'LocationConstraint': 'us-east-2'},
            ObjectLockEnabledForBucket=True,
            ObjectOwnership='BucketOwnerEnforced',
        )
    except botocore.exceptions.ClientError as error:
        response = error.response
        if (
            response["Error"]["Code"] == "BucketAlreadyOwnedByYou"
            and response["ResponseMetadata"]["HTTPStatusCode"] == 409
        ):
            print(response['Error']['Message'])
        if response["Error"]["Code"] == "InvalidBucketName" and response["ResponseMetadata"]["HTTPStatusCode"] == 400:
            print(response['Error']['Message'])


def push_to_s3(bucket_name, remote_file_name, content, region):
    try:
        print(bucket_name)
        client_s3 = boto3.resource('s3', region_name=region)
        client_s3.Bucket(bucket_name).put_object(Key=remote_file_name, Body=content)
    except botocore.exceptions.ClientError as error:
        response = error.response
        if response["Error"]["Code"] == "NoSuchBucket" and response["ResponseMetadata"]["HTTPStatusCode"] == 404:
            print(response['Error']['Message'])
        if response["Error"]["Code"] == "AllAccessDisabled" and response["ResponseMetadata"]["HTTPStatusCode"] == 403:
            print(response['Error']['Message'])
    except botocore.exceptions.ParamValidationError as param_error:
        print(param_error)


def create_kms_key(region):
    try:
        client_kms = boto3.client('kms', region_name=region)
        response = client_kms.create_key(Description='AWS KET KMS KEY', KeyUsage='ENCRYPT_DECRYPT', Origin='AWS_KMS')
        return response['KeyMetadata']['KeyId']

    except botocore.exceptions.ClientError as error:
        response = error.response
        if (
            response["Error"]["Code"] == "UnrecognizedClientException"
            and response["ResponseMetadata"]["HTTPStatusCode"] == 400
        ):
            print(response['Error']['Message'])
            return response['Error']['Code']
        if (
            response["Error"]["Code"] == "AccessDeniedException"
            and response["ResponseMetadata"]["HTTPStatusCode"] == 400
        ):
            print(response['Error']['Message'])
            return response['Error']['Code']


def create_kms_alias(key_id, alias_name, region):
    try:
        client_kms = boto3.client('kms', region_name=region)
        response = client_kms.create_alias(AliasName=alias_name, TargetKeyId=key_id)
        return alias_name
    except botocore.exceptions.ClientError as error:
        response = error.response
        if response["Error"]["Code"] == "ValidationException" and response["ResponseMetadata"]["HTTPStatusCode"] == 400:
            print(response['Error']['Message'])
            return "ValidationException"
        if (
            response["Error"]["Code"] == "AlreadyExistsException"
            and response["ResponseMetadata"]["HTTPStatusCode"] == 400
        ):
            print(response['Error']['Message'])
            return "AlreadyExistsException"


def check_alias(alias_name, region):
    try:
        client_kms = boto3.client('kms', region_name=region)
        aliases = client_kms.list_aliases()
        for alias in aliases['Aliases']:
            if alias_name == alias['AliasName']:
                return alias_name
        return None
    except botocore.exceptions.ClientError as error:
        response = error.response
        if (
            response["Error"]["Code"] == "UnrecognizedClientException"
            and response["ResponseMetadata"]["HTTPStatusCode"] == 400
        ):
            print("Invalid AWS Client Token")
            return "UnrecognizedClientException"
        if (
            response["Error"]["Code"] == "AccessDeniedException"
            and response["ResponseMetadata"]["HTTPStatusCode"] == 400
        ):
            print(response['Error']['Message'])
            return response['Error']['Code']


def encrypt_text(kms_key, text, region):
    try:
        client_kms = boto3.client('kms', region_name=region)
        encrypted_kms_request = client_kms.encrypt(KeyId=kms_key, Plaintext=text)
        encrypted_string = encrypted_kms_request["CiphertextBlob"]
        return encrypted_string
    except botocore.exceptions.ClientError as error:
        response = error.response
        if response["Error"]["Code"] == "NotFoundException" and response["ResponseMetadata"]["HTTPStatusCode"] == 400:
            print(response['Error']['Message'])
            return response['Error']['Code']
        if response['Error']['Code'] == "ValidationException" and response["ResponseMetadata"]["HTTPStatusCode"] == 400:
            print('The text you provided must be greater than 0 characters in length')
            return response['Error']['Code']
        if (
            response['Error']['Code'] == "AccessDeniedException"
            and response["ResponseMetadata"]["HTTPStatusCode"] == 400
        ):
            print(response['Error']['Message'])
            return response['Error']['Code']
    except botocore.exceptions.ParamValidationError as param_error:
        print(param_error)


def encrypt_file(kms_key, file_name, region):
    try:
        client_kms = boto3.client('kms', region_name=region)
        file = open(file_name, "r")
        encrypted_kms_request = client_kms.encrypt(KeyId=kms_key, Plaintext=file.read())
        encrypted_string = encrypted_kms_request["CiphertextBlob"]
        return encrypted_string
    except FileNotFoundError as error:
        print(error)
    except botocore.exceptions.ClientError as error:
        response = error.response
        if response["Error"]["Code"] == "NotFoundException" and response["ResponseMetadata"]["HTTPStatusCode"] == 400:
            print(response['Error']['Message'])
            return response['Error']['Code']
        if response['Error']['Code'] == "ValidationException" and response["ResponseMetadata"]["HTTPStatusCode"] == 400:
            print('The text you provided must be greater than 0 characters in length')
            return response['Error']['Code']
        if (
            response['Error']['Code'] == "AccessDeniedException"
            and response["ResponseMetadata"]["HTTPStatusCode"] == 400
        ):
            print(response['Error']['Message'])
            return response['Error']['Code']
    except botocore.exceptions.ParamValidationError as param_error:
        print(param_error)


def decrypt_text(bucket_name, remote_file_name, kms_key_id, region):
    try:
        client_kms = boto3.client('kms', region_name=region)
        client_s3 = boto3.client('s3', region_name=region)
        s3_object = client_s3.get_object(Bucket=bucket_name, Key=remote_file_name)
        body = s3_object["Body"].read()
        kms_decrypt_request = client_kms.decrypt(CiphertextBlob=body, KeyId=kms_key_id)
        kms_decrypted_text = kms_decrypt_request["Plaintext"].decode("UTF-8")
        return kms_decrypted_text
    except botocore.exceptions.ClientError as error:
        response = error.response
        if response["Error"]["Code"] == "NoSuchBucket" and response["ResponseMetadata"]["HTTPStatusCode"] == 404:
            print(response['Error']['Message'])
        if response["Error"]["Code"] == "NoSuchKey" and response["ResponseMetadata"]["HTTPStatusCode"] == 404:
            print(f'The specified file: {remote_file_name} in {bucket_name} bucket does not exist')
        if (
            response["Error"]["Code"] == "IncorrectKeyException"
            and response["ResponseMetadata"]["HTTPStatusCode"] == 400
        ):
            print(response['Error']['Message'])
    except botocore.exceptions.ParamValidationError as param_error:
        print(param_error)


def save_to_file(file_name, decrypted_string):
    file = open(file_name, "w")
    file.write(decrypted_string)
    file.close()
