#!/usr/bin/env python

# TO DO
# Be able to create kms in any reegion
# Be able to create s3 in any region sepcified
# Be able to initallize DynamoDB backend
# Input based initalization

from ket import *

AWS_REGION = 'us-west-2'

if __name__ == "__main__":
    region = AWS_REGION
    user_name = get_iam_user()['UserId'].lower()
    bucket_name = f'aws-ket-{user_name}'
    create_s3_bucket(bucket_name, region)
    alias_name = check_alias('alias/aws-ket', region)
    if alias_name is None:
        kms_key_id = create_kms_key(region)
        alias_name = create_kms_alias(kms_key_id,'alias/aws-ket', region)
        print('creating key')
    else:
        print(f'KMS Key with {alias_name} already exists in {region}')
