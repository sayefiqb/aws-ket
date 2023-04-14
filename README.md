# aws-ket
Utility tool to encrypt data using AWS KMS and store it in preferred backend.

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

## Overview
AWS-KET (AWS KMS Encryption Tool) uses AWS KMS Key to encrypt and decrypt files/contents based on user provided kms keys and push them to a datastore backend (S3, RDS or DynamoDB).


![GitHub issues](https://img.shields.io/github/issues/sayefiqb/aws-ket)
[![CodeQL](https://github.com/sayefiqb/aws-ket/actions/workflows/github-code-scanning/codeql/badge.svg?branch=main)](https://github.com/sayefiqb/aws-ket/actions/workflows/github-code-scanning/codeql) [![Build Status](https://github.com/sayefiqb/aws-ket/actions/workflows/build.yaml/badge.svg)](https://github.com/sayefiqb/aws-ket/actions/workflows/build.yaml) [![codecov](https://codecov.io/gh/sayefiqb/aws-ket/branch/main/graph/badge.svg?token=13922GT547)](https://codecov.io/gh/sayefiqb/aws-ket)[![PyPI](https://img.shields.io/pypi/v/aws-ket)](https://pypi.org/project/aws-ket)[![Documentation Status](https://readthedocs.org/projects/aws-ket/badge/?version=latest)](https://aws-ket.readthedocs.io/en/latest/?badge=latest)

#### Setup

This application will only work if you have AWS account with full privileges on KMS and S3 services in AWS. You should also have aws cli tool installed.

[Setup AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html)

**Note:** Currently this tool only uses AWS region `us-east-2` for usage of kms and s3.

#### Initaliztion of app
```
cd src
python init.py
```

#### Encrypt text/file
```
python app.py --text <TEXT_TO_ENCRYPT> --save <FILE_NAME_IN_S3> 
python app.py --file <PATH_OF_FILE_TO_ENCRYPT> --save <FILE_NAME_IN_S3>
```

#### Decrypt text/file from S3
This will save with same name as remote
```
python app.py --decrypt <FILE_NAME_IN_S3> 
```
OR 
<br />
To specify name for saved file
```
python app.py --decrypt <FILE_NAME_IN_S3>  --save <FILE_NAME_TO_SAVE_AS_IN_LOCAL>
```

#### Cleanup
To cleanup your S3 bucket and start over
```
python cleanup.py
```


#### Details
This project uses `Makefile` as a command registry, with the following commands:
- `make`: list available commands
- `make develop`: install and build this library and its dependencies using `pip`
- `make lint`: perform lint using `black`
- `make scan`: run static analysis on code using `flake8`
- `make test`: run automated tests with `pytest`
- `make coverage`: run automated tests with `pytest` and collect coverage information

`coverage` output can also be found in html format in `htmlcover` directory.

#### Example

First download the source code
![](aws-ket.gif)