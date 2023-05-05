#!/usr/bin/env python

from awsket import ket

AWS_REGION = 'us-east-2'
KMS_ALIAS = 'alias/aws-ket'
TEXT = 'This is a sample text for testing encryption! Happy coding :)'
FILE = 'EXAMPLE.txt'


user_name = ket.get_iam_user()['UserId'].lower()
bucket_name = f'aws-ket-{user_name}'
encrypted_string = ket.encrypt_text(KMS_ALIAS, TEXT, AWS_REGION)
ket.push_to_s3(bucket_name, FILE, encrypted_string, AWS_REGION)