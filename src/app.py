#!/usr/bin/env python


# TO DO
# Provide more option to encrypt and decryupt files/text
# Option to choose backend storage for encrypted file
# Bettwer way to ame files
# Only use pwd as filename when nbo filename provided
# Be able to list ncrypted files using a key
# Better logginng
# Handle Exception
# More will be added!

import os
import boto3
import argparse
import ket


# kms_key_id = os.environ.get('KMS_KEY_ID')
# bucket_name = os.environ.get('S3_BUCKET')
# file_name = os.getcwd()

# client = boto3.client('kms')

parser = argparse.ArgumentParser()
parser.add_argument("--text", "-T", help="provide plain text to encrypt")
parser.add_argument("--file", "-F", help="provide file name in current to encrypt")
parser.add_argument("--decrypt", "-D", help="provide file name in S3 to decrypt")



def main(kms_key_id,bucket_name, region):
    args = parser.parse_args()
    if args.text:
        encrypted_string = ket.encrypt_text(kms_key_id, args.text, region)
        s3_response = ket.push_to_s3(bucket_name, file_name, encrypted_string, region)
        print('Successfully encrypted file and pushed to S3')
        print(encrypted_string)
        return encrypted_string
    elif args.file:
        encrypted_file = ket.encrypt_file(kms_key_id, args.file, region)
        s3_response = ket.push_to_s3(bucket_name, file_name, encrypted_file, region)
        print('Successfully encrypted file and pushed to S3')
        return encrypted_file
    elif args.decrypt:
        encrypted_file = ket.decrypt_text(bucket_name, args.decrypt, kms_key_id, region)
        print('Successfully downloaded file from S3 and decrypted')
    else:
        print("Invalid arguments. Use python ./app.py --text <STRING>")


if __name__ == "__main__":
    region = 'us-east-1'
    kms_key_id = 'alias/aws-ket'
    bucket_name = f'aws-ket-{ket.get_iam_user()}'
    main(kms_key_id,bucket_name,region)
