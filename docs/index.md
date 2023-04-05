

# Welcome to aws-ket documentation

    
## Overview
AWS Ket is a utility tool to encrypt data using AWS KMS and store it in preferred backend. AWS-KET (AWS KMS Encryption Tool) uses AWS KMS Key to encrypt and decrypt files/contents based on user provided kms keys and push them to a datastore backend (S3, RDS or DynamoDB).



## Main features
- Encrypts texs/files using kms. 
- Pushes the enrypted file to s3 
- Can download an decryprt the files anytme from s3

## Installing

```
pip install aws-ket
```
<br>

Or

Download the source code

## Usage

### Initialization
```
cd src
python init.py
```

### Encrypt text/file
```
python app.py --text <TEXT_TO_ENCRYPT> --save <FILE_NAME_IN_S3> 
python app.py --file <PATH_OF_FILE_TO_ENCRYPT> --save <FILE_NAME_IN_S3>
```

### Decrypt text/file from S3
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


## Coverage and Tests

This project uses `Makefile` as a command registry, with the following commands:
- `make`: list available commands
- `make develop`: install and build this library and its dependencies using `pip`
- `make lint`: perform lint using `black`
- `make scan`: run static analysis on code using `flake8`
- `make test`: run automated tests with `pytest`
- `make coverage`: run automated tests with `pytest` and collect coverage information

`coverage` output can also be found in html format in `htmlcover` directory.


```eval_rst
.. toctree::
   :maxdepth: 4
   :caption: Contents:

   modules
   examples

   
Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
```