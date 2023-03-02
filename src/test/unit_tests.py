import sys

sys.path.append('../../src')
import initialize
import cleanup


# Create a cleanup job that will remove the S3 and kms key with alias.
def test_setup():
    cleanup.cleanup_kms()
    cleanup.cleanup_s3()
    print('Cleanup completed!')


def test_check_kms_key():
    assert initialize.check_kms_key() == None


def test_create_key():
    assert initialize.create_key() == ("KMS key created successfully")


def test_get_iam__user():
    assert initialize.get_iam_user() == "sayef"


def test_get_bucket_name():
    assert initialize.get_bucket_name() == 'aws-ket-sayef-2023'


def test_check_s3_bucket():
    assert initialize.check_s3_bucket("aws-ket-sayef-2023") == None


def test_create_s3_bucket():
    assert initialize.create_s3_bucket() == "Initialization Complete"


if __name__ == '__main__':
    test_setup()
    test_check_kms_key()
    test_create_key()
    test_get_iam__user()
    test_get_bucket_name()
    test_check_s3_bucket()
    test_create_s3_bucket()
