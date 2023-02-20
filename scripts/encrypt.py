#TO DO

# Better logging
# Support for sending to other backend stoorage
# Reusable codde
# Better loggiing
# Handle exceptions
# What happens if AWS Creds not provided?

import boto3

client_kms = boto3.client("kms")
client_s3 = boto3.resource("s3")

def encrypt_text(kms_key,text):
    encrypted_kms_request = client_kms.encrypt(
        KeyId=kms_key, Plaintext=text
    )
    encrypted_string = encrypted_kms_request["CiphertextBlob"]
    return encrypted_string

def encrypt_file(kms_key,file_name):
    file = open(file_name, "r")
    encrypted_kms_request = client_kms.encrypt(
        KeyId=kms_key, Plaintext=file.read()
    )
    encrypted_string = encrypted_kms_request["CiphertextBlob"]

    return encrypted_string


def push_to_s3(bucket,file_name,encrypted_text):
    client_s3.Bucket(bucket).put_object(
        Key=file_name, Body=encrypted_text
    )
