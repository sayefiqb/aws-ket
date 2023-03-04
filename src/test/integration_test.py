import sys
import os

sys.path.append('../../src')
import encrypt, decrypt, cleanup, initialize


kms_key_id = os.environ.get('KMS_KEY_ID')
bucket_name = os.environ.get('S3_BUCKET')
sample_text = 'This is a sample text for integration test!'
file_name = 'integration-test-text'
test_file_name = 'sample.txt'


# Create a cleanup job  that will remove bucket and kms key with alias.
# def test_setup():
#     cleanup.cleanup_kms()
#     cleanup.cleanup_s3()
#     print('Cleanup completed!')
#     print('Running initialization...')
#     initialize.initialize()


# This funtion will first encrypt, push to S3 and then decrypt it from S3
def test_encrypton_decryption_of_text():
    encrypted_string = encrypt.encrypt_text(kms_key_id, sample_text)
    s3_response = encrypt.push_to_s3(bucket_name, file_name, encrypted_string)
    decrypted_string = decrypt.decrypt_text(bucket_name, file_name, kms_key_id)
    print(decrypted_string)
    assert decrypted_string == sample_text


def test_encryption_decryption_of_file():
    encrypted_file = encrypt.encrypt_file(kms_key_id, test_file_name)
    s3_response = encrypt.push_to_s3(bucket_name, test_file_name, encrypted_file)
    decrypted_string = decrypt.decrypt_text(bucket_name, test_file_name, kms_key_id)
    f = open(test_file_name, 'r')
    file_content = f.readline()
    assert decrypted_string == file_content
    f.close()


if __name__ == '__main__':
    test_encrypton_decryption_of_text()
    test_encryption_decryption_of_file()
