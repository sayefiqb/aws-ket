#!/usr/bin/env python

from awsket import ket

AWS_REGION = 'us-east-2'
KMS_ALIAS = 'alias/aws-ket'

user_name = ket.get_iam_user()['UserId'].lower()
bucket_name = f'aws-ket-{user_name}'
ket.create_s3_bucket(bucket_name, AWS_REGION)
alias_name = ket.check_alias(KMS_ALIAS, AWS_REGION)
kms_key_id = ket.create_kms_key(AWS_REGION)
alias_name = ket.create_kms_alias(kms_key_id, KMS_ALIAS, AWS_REGION)