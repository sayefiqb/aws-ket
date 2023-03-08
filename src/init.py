#!/usr/bin/env python

# TO DO
# Be able to create kms in any reegion
# Be able to create s3 in any region sepcified
# Be able to initallize DynamoDB backend
# Input based initalization

from ket import *

AWS_REGION = 'us-east-2'

if __name__ == "__main__":
    user_name = get_iam_user()['UserId'].lower()
    bucket_name = f'aws-ket-{user_name}'
    create_s3_bucket(bucket_name, AWS_REGION)
    alias_name = check_alias('alias/aws-ket', AWS_REGION)
    if alias_name is None:
        kms_key_id = create_kms_key(AWS_REGION)
        alias_name = create_kms_alias(kms_key_id, 'alias/aws-ket', AWS_REGION)
        print('creating key')
    else:
        print(f'KMS Key with {alias_name} already exists in {AWS_REGION}')
