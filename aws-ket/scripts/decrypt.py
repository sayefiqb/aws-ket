# TO DO
# Reusable code?
# Present data t user in better way
# Save decrypted data/file in local machine
# Bbetter logging
# Handle Exception

import boto3
from pprint import pprint

client_s3 = boto3.client("s3")
client_kms = boto3.client("kms")


def decrypt_text(bucket,file,kms_key_id):

    s3_object = client_s3.get_object(Bucket=bucket, Key=file)
    body = s3_object["Body"].read()
    kms_decrypt_request = client_kms.decrypt(
        CiphertextBlob=body, KeyId=kms_key_id
    )

    kms_decrypted_text = kms_decrypt_request["Plaintext"].decode("UTF-8")
    # decrypted_text = json.loads(kms_decrypted_text)
    pprint(kms_decrypted_text)
    return kms_decrypted_text