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
import encrypt, decrypt


kms_key_id = os.environ.get('KMS_KEY_ID')
bucket_name = os.environ.get('S3_BUCKET')
file_name = os.getcwd()

client = boto3.client('kms')

parser = argparse.ArgumentParser()
parser.add_argument("--text", "-T", help="provide plain text to encrypt")
parser.add_argument("--file", "-F", help="provide file name in current to encrypt")
parser.add_argument("--decrypt", "-D", help="provide file name in S3 to decrypt")


def main():
    args = parser.parse_args()
    if args.text:
        encrypted_string = encrypt.encrypt_text(kms_key_id, args.text)
        s3_response = encrypt.push_to_s3(bucket_name, file_name, encrypted_string)
        print('Successfully encrypted file and pushed to S3')
        print(encrypted_string)
        return encrypted_string
    elif args.file:
        encrypted_file = encrypt.encrypt_file(kms_key_id, args.file)
        s3_response = encrypt.push_to_s3(bucket_name, file_name, encrypted_file)
        print('Successfully encrypted file and pushed to S3')
        return encrypted_file
    elif args.decrypt:
        encrypted_file = decrypt.decrypt_text(bucket_name, args.decrypt, kms_key_id)
        print('Successfully downloaded file from S3 and decrypted')
    else:
        print("Invalid arguments. Use python ./app.py --text <STRING>")


if __name__ == "__main__":
    main()
