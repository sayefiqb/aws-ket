
# Example
 
## Encrypting

```
from awsket import ket

AWS_REGION = 'us-east-2'
KMS_ALIAS = 'alias/aws-ket'
TEXT = 'This is a sample text for testing encryption! Happy coding :)'
FILE = 'EXAMPLE.txt'


user_name = ket.get_iam_user()['UserId'].lower()
bucket_name = f'aws-ket-{user_name}'
encrypted_string = ket.encrypt_text(KMS_ALIAS, TEXT, AWS_REGION)
ket.push_to_s3(bucket_name, FILE, encrypted_string, AWS_REGION)
```

## Decryption

```
from awsket import ket

AWS_REGION = 'us-east-2'
KMS_ALIAS = 'alias/aws-ket'
FILE = 'EXAMPLE.txt'

user_name = ket.get_iam_user()['UserId'].lower()
bucket_name = f'aws-ket-{user_name}'
decrypted_text = ket.decrypt_text(bucket_name, FILE, KMS_ALIAS, AWS_REGION)
print(decrypted_text)


```
