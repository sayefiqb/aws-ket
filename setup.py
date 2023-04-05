from setuptools import setup

VERSION = "0.1.1"
setup(
    name             = 'aws-ket',
    author           = 'Sayef Iqbal',
    author_email     = 's2400@columbia.edu',
    maintainer       = 'Sayef Iqbal',
    url              = 'https://github.com/sayefiqb/aws-ket',
    description      = 'Utility tool to encrypt data using AWS KMS and store it in preferred backend.',
    version          = VERSION,
    include_package_data= True
)