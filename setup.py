from setuptools import setup

VERSION = "0.1.2"
setup(
    name             = 'aws-ket',
    author           = 'Sayef Iqbal',
    author_email     = 's2400@columbia.edu',
    maintainer       = 'Sayef Iqbal',
    url              = 'https://github.com/sayefiqb/aws-ket',
    description      = 'Utility tool to encrypt data using AWS KMS and store it in preferred backend.',
    version          = VERSION,
    include_package_data= True,
    entry_points = {
        'console_scripts': ['awsket=awsket.ket:create_kms_alias',
                            'awsket=awsket.ket:create_kms_key',
                            'awsket=awsket.ket:create_s3_bucket',
                            'awsket=awsket.ket:check_alias',
                            'awsket=awsket.ket:get_iam_user',
                            'awsket=awsket.ket:push_to_s3',
                            'awsket=awsket.ket:encrypt_file',
                            'awsket=awsket.ket:encrypt_text',
                            'awsket=awsket.ket:decrypt_text']
    }
)