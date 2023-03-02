# aws-ket
Utility tool to encrypt data using AWS KMS and store it in preferred backend.

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

## Overview
AWS-KET (AWS KMS Encryption Tool) uses AWS KMS Key to encrypt and decrypt files/contents based on user provided kms keys and push them to a datastore backend (S3, RDS or DynamoDB).


![GitHub issues](https://img.shields.io/github/issues/sayefiqb/aws-ket)

[![CodeQL](https://github.com/sayefiqb/aws-ket/actions/workflows/github-code-scanning/codeql/badge.svg?branch=main)](https://github.com/sayefiqb/aws-ket/actions/workflows/github-code-scanning/codeql)


#### Initaliztion of app
```
cd src
python initialize.py
```

#### Encrypt text/file
```
cd src
python app.py --text 'Hello World'
python app.py --file test/sample.txt
```

#### Decrypt text/file from s3
```
python app.py --decrypt </path/to/your/s3/object>
```