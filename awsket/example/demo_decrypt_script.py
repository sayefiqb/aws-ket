#!/usr/bin/env python

from awsket import ket

AWS_REGION = 'us-east-2'
KMS_ALIAS = 'alias/aws-ket'
FILE = 'EXAMPLE.txt'

user_name = ket.get_iam_user()['UserId'].lower()
bucket_name = f'aws-ket-{user_name}'
decrypted_text = ket.decrypt_text(bucket_name, FILE, KMS_ALIAS, AWS_REGION)
print(decrypted_text)
