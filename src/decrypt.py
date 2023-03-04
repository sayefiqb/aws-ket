# TO DO
# Reusable code?
# Present data t user in better way
# Save decrypted data/file in local machine
# Bbetter logging
# Handle Exception

import boto3
import botocore
from pprint import pprint

client_s3 = boto3.client("s3")
client_kms = boto3.client("kms")


def decrypt_text(bucket, file, kms_key_id):
    try:
        s3_object = client_s3.get_object(Bucket=bucket, Key=file)
        body = s3_object["Body"].read()
        kms_decrypt_request = client_kms.decrypt(CiphertextBlob=body, KeyId=kms_key_id)
        kms_decrypted_text = kms_decrypt_request["Plaintext"].decode("UTF-8")
      
        pprint(kms_decrypted_text)
        return kms_decrypted_text
    except botocore.exceptions.ClientError as error:
        response = error.response
        if response["Error"]["Code"] == "NoSuchBucket" and response["ResponseMetadata"]["HTTPStatusCode"] == 404:
            print(f'The specified bucket: {bucket} does not exist')
        if response["Error"]["Code"] == "NoSuchKey" and response["ResponseMetadata"]["HTTPStatusCode"] == 404:
            print(f'The specified file: {file} in {bucket} bucket does not exist')
        if response["Error"]["Code"] == "IncorrectKeyException" and response["ResponseMetadata"]["HTTPStatusCode"] == 400:
                    print(f'Incorrect KMS Key ID provided')
    except botocore.exceptions.ParamValidationError as param_error:
        print(param_error)
   
