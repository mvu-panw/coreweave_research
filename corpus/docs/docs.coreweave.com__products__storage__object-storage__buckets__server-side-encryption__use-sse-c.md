# Use SSE-C

Source: https://docs.coreweave.com/products/storage/object-storage/buckets/server-side-encryption/use-sse-c

# Use SSE-C

> How to implement server-side encryption with customer keys (SSE-C) with CoreWeave AI Object Storage

This guide demonstrates how to implement [server-side encryption with customer keys (SSE-C) with CoreWeave AI Object Storage](https://docs.coreweave.com/products/storage/object-storage/buckets/server-side-encryption/about-sse-c.md). SSE-C lets you provide your own encryption keys for objects stored in Object Storage, giving you control over data encryption.

It's intended for developers and storage administrators who need to encrypt objects with self-managed keys. By the end of this guide, you know how to generate SSE-C keys, upload and retrieve encrypted objects, verify that encryption was applied, manage keys safely, and enforce SSE-C through bucket policies.

## Prerequisites

Before implementing SSE-C, ensure you have:

* Access to Object Storage with appropriate permissions.
* An S3-compatible client or library that supports SSE-C.
* A method to generate and store encryption keys securely.
* Understanding of basic S3 operations (upload, download, and copy).

> [!CAUTION]
>
> If you lose your encryption key, you can't recover your encrypted data. CoreWeave **doesn't store your encryption keys**, and can't decrypt your data without them. See the [Key management](#key-management) section for best practices on storing and managing your encryption keys securely.

## Understanding key verification

Object Storage uses your provided key to encrypt or decrypt your data as required, but doesn't store that key itself. Instead, CoreWeave stores only a base64-encoded MD5 digest of your encryption key.

This hash is stored only for verification: when you later access the object, you must supply the same key and hash you used originally. CoreWeave checks the hash of the supplied key against the stored hash to verify that the correct key is provided before attempting decryption.

> [!NOTE]
>
> **Why only the hash?**
>
> The hash of the key serves as a checksum: it can verify that the key is correct, but it can't be used to reconstruct the key. By storing only the hash and not the key itself, CoreWeave ensures that only someone who possesses the original encryption key can access the corresponding encrypted data. If you lose your key, **neither you nor CoreWeave can recover your data**. The hash makes it computationally infeasible to recover the original key due to the one-way nature of cryptographic hashes.

## Basic operations

In these examples, `$BASE64_KEY` represents your base64-encoded encryption key. Replace this with your generated key in all examples.

### Generate encryption keys

SSE-C requires 256-bit (32-byte) encryption keys. Generate these keys using cryptographically secure methods and encode them in base64 format:

> [tab] OpenSSL
>
> ```bash theme={"system"}
> # Generate a random 256-bit key and encode in base64
> openssl rand -base64 32
> ```

> [tab] Python
>
> ```python theme={"system"}
> import secrets
> import base64
>
> # Generate a random 256-bit key and encode in base64
> key_bytes = secrets.token_bytes(32)
> key = base64.b64encode(key_bytes).decode('utf-8')
> print(key)
> ```

> [tab] Shell
>
> ```bash theme={"system"}
> # Generate a random 256-bit key using /dev/urandom and encode in base64
> head -c 32 /dev/urandom | base64
>
> # Alternative: Generate key and save to variable
> BASE64_KEY=$(head -c 32 /dev/urandom | base64)
> echo $BASE64_KEY
> ```

### Upload objects with SSE-C

When uploading objects with SSE-C, include the encryption key in your request headers:

> [tab] AWS CLI
>
> Replace `[LOCAL-FILE-PATH]` with the path to the local file you want to upload. Replace `[BUCKET-NAME]` with the name of the destination bucket.
>
> ```bash theme={"system"}
> export LOCAL_FILE_PATH="[LOCAL-FILE-PATH]"
> export BUCKET_NAME="[BUCKET-NAME]"
>
> # Upload an object with SSE-C
> aws s3 cp "$LOCAL_FILE_PATH" "s3://$BUCKET_NAME/" --sse-customer-algorithm AES256 \
>   --sse-customer-key $BASE64_KEY \
>   --sse-customer-key-md5 $(echo -n "$BASE64_KEY" | base64 --decode | openssl dgst -md5 -binary | base64)
> ```

> [tab] Boto3
>
> Set environment variables for your CoreWeave credentials and encryption key:
>
> ```bash theme={"system"}
> export ACCESS_KEY_ID="[ACCESS-KEY-ID]"
> export SECRET_ACCESS_KEY="[SECRET-ACCESS-KEY]"
> export BASE64_KEY="[ENCRYPTION-KEY]"
> ```
>
> Replace `[BUCKET-NAME]` with the name of the destination bucket. Replace `[LOCAL-FILE-PATH]` with the path to the local file to upload.
>
> ```python theme={"system"}
> import os
> import boto3
> import hashlib
> import base64
> from botocore.client import Config
>
> boto_config = Config(
>     region_name='US-EAST-04A',
>     s3={'addressing_style': 'virtual'}
> )
>
> s3_client = boto3.client(
>     's3',
>     endpoint_url='https://cwobject.com',
>     aws_access_key_id=os.environ['ACCESS_KEY_ID'],
>     aws_secret_access_key=os.environ['SECRET_ACCESS_KEY'],
>     config=boto_config
> )
>
> encryption_key = os.environ['BASE64_KEY']
> key_md5 = hashlib.md5(base64.b64decode(encryption_key)).digest()
> key_md5_b64 = base64.b64encode(key_md5).decode('utf-8')
>
> s3_client.upload_file(
>     '[LOCAL-FILE-PATH]',
>     '[BUCKET-NAME]',
>     '[OBJECT-KEY]',
>     ExtraArgs={
>         'SSECustomerAlgorithm': 'AES256',
>         'SSECustomerKey': encryption_key,
>         'SSECustomerKeyMD5': key_md5_b64
>     }
> )
> ```

> [tab] curl
>
> ```bash theme={"system"}
> # Upload with SSE-C using curl
> curl -X PUT \
>   -H "x-amz-server-side-encryption-customer-algorithm: AES256" \
>   -H "x-amz-server-side-encryption-customer-key: $BASE64_KEY" \
>   -H "x-amz-server-side-encryption-customer-key-md5: $(echo -n "$BASE64_KEY" | base64 -d | openssl dgst -md5 -binary | base64)" \
>   -T [LOCAL-FILE-PATH] \
>   "https://[BUCKET-NAME].cwobject.com/[OBJECT-KEY]"
> ```

### Download objects with SSE-C

When downloading objects that were encrypted with SSE-C, provide the same encryption key:

> [tab] AWS CLI
>
> ```bash theme={"system"}
> export OBJECT_KEY="[OBJECT-KEY]"
> export BUCKET_NAME="[BUCKET-NAME]"
> export LOCAL_FILE_PATH="[LOCAL-FILE-PATH]"
> ```
>
> ```bash theme={"system"}
> # Download an object with SSE-C
> aws s3 cp "s3://$BUCKET_NAME/$OBJECT_KEY" "$LOCAL_FILE_PATH" \
>   --sse-customer-algorithm AES256 \
>   --sse-customer-key $BASE64_KEY \
>   --sse-customer-key-md5 $(echo -n "$BASE64_KEY" | base64 -d | openssl dgst -md5 -binary | base64)
> ```

> [tab] Boto3
>
> Set environment variables for your CoreWeave credentials and encryption key:
>
> ```bash theme={"system"}
> export ACCESS_KEY_ID="[ACCESS-KEY-ID]"
> export SECRET_ACCESS_KEY="[SECRET-ACCESS-KEY]"
> export BASE64_KEY="[ENCRYPTION-KEY]"
> ```
>
> Replace `[BUCKET-NAME]` with the name of the bucket. Replace `[OBJECT-KEY]` with the key of the object to download (for example, `myfile.txt`). Replace `[LOCAL-FILE-PATH]` with the local path to save the file to (for example, `/tmp/downloaded-file.txt`).
>
> ```python theme={"system"}
> import os
> import boto3
> import hashlib
> import base64
> from botocore.client import Config
>
> boto_config = Config(
>     region_name='US-EAST-04A',
>     s3={'addressing_style': 'virtual'}
> )
>
> s3_client = boto3.client(
>     's3',
>     endpoint_url='https://cwobject.com',
>     aws_access_key_id=os.environ['ACCESS_KEY_ID'],
>     aws_secret_access_key=os.environ['SECRET_ACCESS_KEY'],
>     config=boto_config
> )
>
> encryption_key = os.environ['BASE64_KEY']
> key_md5 = hashlib.md5(base64.b64decode(encryption_key)).digest()
> key_md5_b64 = base64.b64encode(key_md5).decode('utf-8')
>
> s3_client.download_file(
>     '[BUCKET-NAME]',
>     '[OBJECT-KEY]',
>     '[LOCAL-FILE-PATH]',
>     ExtraArgs={
>         'SSECustomerAlgorithm': 'AES256',
>         'SSECustomerKey': encryption_key,
>         'SSECustomerKeyMD5': key_md5_b64
>     }
> )
> ```

> [tab] curl
>
> ```bash theme={"system"}
> # Download with SSE-C using curl
> curl -X GET \
>   -H "x-amz-server-side-encryption-customer-algorithm: AES256" \
>   -H "x-amz-server-side-encryption-customer-key: $BASE64_KEY" \
>   -H "x-amz-server-side-encryption-customer-key-md5: $(echo -n "$BASE64_KEY" | base64 -d | openssl dgst -md5 -binary | base64)" \
>   "https://[BUCKET-NAME].cwobject.com/[OBJECT-KEY]" \
>   -o [LOCAL-FILE-PATH]
> ```

### Copy objects with SSE-C

When copying objects that use SSE-C, specify the encryption parameters for both source and destination:

> [tab] AWS CLI
>
> Replace `[SOURCE-BUCKET-NAME]` and `[SOURCE-OBJECT-KEY]` with the source bucket name and object key. Replace `[DEST-BUCKET-NAME]` and `[DEST-OBJECT-KEY]` with the destination bucket name and object key.
>
> ```bash theme={"system"}
> export SOURCE_BUCKET="[SOURCE-BUCKET-NAME]"
> export SOURCE_KEY="[SOURCE-OBJECT-KEY]"
> export DEST_BUCKET="[DEST-BUCKET-NAME]"
> export DEST_KEY="[DEST-OBJECT-KEY]"
> ```
>
> ```bash theme={"system"}
> # Copy an object with SSE-C
> aws s3 cp "s3://$SOURCE_BUCKET/$SOURCE_KEY" "s3://$DEST_BUCKET/$DEST_KEY" \
>   --sse-customer-algorithm AES256 \
>   --sse-customer-key $BASE64_KEY \
>   --sse-customer-key-md5 $(echo -n "$BASE64_KEY" | base64 --decode | openssl dgst -md5 -binary | base64) \
>   --copy-source-sse-customer-algorithm AES256 \
>   --copy-source-sse-customer-key $BASE64_KEY \
>   --copy-source-sse-customer-key-md5 $(echo -n "$BASE64_KEY" | base64 --decode | openssl dgst -md5 -binary | base64)
> ```

> [tab] Boto3
>
> Set environment variables for your CoreWeave credentials and encryption key:
>
> ```bash theme={"system"}
> export ACCESS_KEY_ID="[ACCESS-KEY-ID]"
> export SECRET_ACCESS_KEY="[SECRET-ACCESS-KEY]"
> export BASE64_KEY="[ENCRYPTION-KEY]"
> ```
>
> Replace `[SOURCE-BUCKET-NAME]` and `[SOURCE-OBJECT-KEY]` with the source bucket name and object key. Replace `[DEST-BUCKET-NAME]` and `[DEST-OBJECT-KEY]` with the destination bucket name and object key.
>
> ```python theme={"system"}
> import os
> import boto3
> import hashlib
> import base64
> from botocore.client import Config
>
> boto_config = Config(
>     region_name='US-EAST-04A',
>     s3={'addressing_style': 'virtual'}
> )
>
> s3_client = boto3.client(
>     's3',
>     endpoint_url='https://cwobject.com',
>     aws_access_key_id=os.environ['ACCESS_KEY_ID'],
>     aws_secret_access_key=os.environ['SECRET_ACCESS_KEY'],
>     config=boto_config
> )
>
> encryption_key = os.environ['BASE64_KEY']
> key_md5 = hashlib.md5(base64.b64decode(encryption_key)).digest()
> key_md5_b64 = base64.b64encode(key_md5).decode('utf-8')
>
> s3_client.copy_object(
>     Bucket='[DEST-BUCKET-NAME]',
>     Key='[DEST-OBJECT-KEY]',
>     CopySource={
>         'Bucket': '[SOURCE-BUCKET-NAME]',
>         'Key': '[SOURCE-OBJECT-KEY]'
>     },
>     SSECustomerAlgorithm='AES256',
>     SSECustomerKey=encryption_key,
>     SSECustomerKeyMD5=key_md5_b64,
>     CopySourceSSECustomerAlgorithm='AES256',
>     CopySourceSSECustomerKey=encryption_key,
>     CopySourceSSECustomerKeyMD5=key_md5_b64
> )
> ```

> [tab] curl
>
> ```bash theme={"system"}
> # Copy with SSE-C using curl
> curl -X PUT \
>   -H "x-amz-copy-source: /[SOURCE-BUCKET-NAME]/[SOURCE-OBJECT-KEY]" \
>   -H "x-amz-copy-source-server-side-encryption-customer-algorithm: AES256" \
>   -H "x-amz-copy-source-server-side-encryption-customer-key: $BASE64_KEY" \
>   -H "x-amz-copy-source-server-side-encryption-customer-key-md5: $(echo -n "$BASE64_KEY" | base64 -d | openssl dgst -md5 -binary | base64)" \
>   -H "x-amz-server-side-encryption-customer-algorithm: AES256" \
>   -H "x-amz-server-side-encryption-customer-key: $BASE64_KEY" \
>   -H "x-amz-server-side-encryption-customer-key-md5: $(echo -n "$BASE64_KEY" | base64 -d | openssl dgst -md5 -binary | base64)" \
>   "https://[DEST-BUCKET-NAME].cwobject.com/[DEST-OBJECT-KEY]"
> ```

## Verify encryption

After uploading objects with SSE-C, confirm that encryption was applied so you know your data is protected. Verify that your objects are encrypted by checking the response headers or object metadata:

### Check upload response

> [tab] Boto3
>
> Set environment variables for your CoreWeave credentials and encryption key:
>
> ```bash theme={"system"}
> export ACCESS_KEY_ID="[ACCESS-KEY-ID]"
> export SECRET_ACCESS_KEY="[SECRET-ACCESS-KEY]"
> export BASE64_KEY="[ENCRYPTION-KEY]"
> ```
>
> Replace `[BUCKET-NAME]` with the bucket name and `[OBJECT-KEY]` with the object key.
>
> ```python theme={"system"}
> import os
> import boto3
> import hashlib
> import base64
> from botocore.client import Config
>
> boto_config = Config(
>     region_name='US-EAST-04A',
>     s3={'addressing_style': 'virtual'}
> )
>
> s3_client = boto3.client(
>     's3',
>     endpoint_url='https://cwobject.com',
>     aws_access_key_id=os.environ['ACCESS_KEY_ID'],
>     aws_secret_access_key=os.environ['SECRET_ACCESS_KEY'],
>     config=boto_config
> )
>
> encryption_key = os.environ['BASE64_KEY']
> key_md5 = hashlib.md5(base64.b64decode(encryption_key)).digest()
> key_md5_b64 = base64.b64encode(key_md5).decode('utf-8')
>
> with open('[LOCAL-FILE-PATH]', 'rb') as f:
>     response = s3_client.put_object(
>         Bucket='[BUCKET-NAME]',
>         Key='[OBJECT-KEY]',
>         Body=f,
>         SSECustomerAlgorithm='AES256',
>         SSECustomerKey=encryption_key,
>         SSECustomerKeyMD5=key_md5_b64
>     )
>
> print(f"Encryption algorithm: {response['SSECustomerAlgorithm']}")
> print(f"Key MD5: {response['SSECustomerKeyMD5']}")
> ```

> [tab] AWS CLI
>
> Set environment variables for the file path, bucket name, and encryption key:
>
> ```bash theme={"system"}
> export LOCAL_FILE_PATH="[LOCAL-FILE-PATH]"
> export BUCKET_NAME="[BUCKET-NAME]"
> export BASE64_KEY="[ENCRYPTION-KEY]"
> ```
>
> Upload the file and check the response headers:
>
> ```bash theme={"system"}
> # Upload and check response headers
> aws s3 cp "$LOCAL_FILE_PATH" "s3://$BUCKET_NAME/" --sse-customer-algorithm AES256 \
>   --sse-customer-key $BASE64_KEY \
>   --sse-customer-key-md5 $(echo -n "$BASE64_KEY" | base64 --decode | openssl dgst -md5 -binary | base64) \
>   --debug
> ```
>
> Look for encryption headers in the debug output, such as:
>
> ```text title="Debug output" theme={"system"}
> x-amz-server-side-encryption-customer-algorithm: AES256
> x-amz-server-side-encryption-customer-key-md5: [hash]
> ```

> [tab] curl
>
> Ensure your encryption key is set in the environment variables:
>
> ```bash theme={"system"}
> export BASE64_KEY="[ENCRYPTION-KEY]"
> ```
>
> ```bash theme={"system"}
> # Upload and check response headers
> curl -X PUT \
>   -H "x-amz-server-side-encryption-customer-algorithm: AES256" \
>   -H "x-amz-server-side-encryption-customer-key: $BASE64_KEY" \
>   -H "x-amz-server-side-encryption-customer-key-md5: $(echo -n "$BASE64_KEY" | base64 -d | openssl dgst -md5 -binary | base64)" \
>   -T [LOCAL-FILE-PATH] \
>   -D response_headers.txt \
>   "https://[BUCKET-NAME].cwobject.com/[OBJECT-KEY]"
>
> # Check the response headers
> cat response_headers.txt | grep -i encryption
> ```

### List objects with encryption info

> [tab] Boto3
>
> Set environment variables for your CoreWeave credentials and encryption key:
>
> ```bash theme={"system"}
> export ACCESS_KEY_ID="[ACCESS-KEY-ID]"
> export SECRET_ACCESS_KEY="[SECRET-ACCESS-KEY]"
> export BASE64_KEY="[ENCRYPTION-KEY]"
> ```
>
> Replace `[BUCKET-NAME]` with the bucket name and `[PREFIX]` with the object prefix to search for.
>
> ```python theme={"system"}
> import os
> import boto3
> import hashlib
> import base64
> from botocore.client import Config
>
> boto_config = Config(
>     region_name='US-EAST-04A',
>     s3={'addressing_style': 'virtual'}
> )
>
> s3_client = boto3.client(
>     's3',
>     endpoint_url='https://cwobject.com',
>     aws_access_key_id=os.environ['ACCESS_KEY_ID'],
>     aws_secret_access_key=os.environ['SECRET_ACCESS_KEY'],
>     config=boto_config
> )
>
> encryption_key = os.environ['BASE64_KEY']
> key_md5 = hashlib.md5(base64.b64decode(encryption_key)).digest()
> key_md5_b64 = base64.b64encode(key_md5).decode('utf-8')
>
> response = s3_client.list_objects_v2(
>     Bucket='[BUCKET-NAME]',
>     Prefix='[PREFIX]'
> )
>
> for obj in response.get('Contents', []):
>     head = s3_client.head_object(
>         Bucket='[BUCKET-NAME]',
>         Key=obj['Key'],
>         SSECustomerAlgorithm='AES256',
>         SSECustomerKey=encryption_key,
>         SSECustomerKeyMD5=key_md5_b64
>     )
>     print(f"Object: {obj['Key']}")
>     print(f"Encryption: {head.get('SSECustomerAlgorithm', 'None')}")
> ```

> [tab] AWS CLI
>
> ```bash theme={"system"}
> # List objects in the bucket
> aws s3api list-objects-v2 \
>   --bucket [BUCKET-NAME] \
>   --prefix [PREFIX] \
>   --query 'Contents[].{Key: Key, Size: Size, LastModified: LastModified}'
>
> # Check encryption on a specific object using head-object
> aws s3api head-object \
>   --bucket [BUCKET-NAME] \
>   --key [OBJECT-KEY] \
>   --sse-customer-algorithm AES256 \
>   --sse-customer-key $BASE64_KEY \
>   --sse-customer-key-md5 $(echo -n "$BASE64_KEY" | base64 -d | openssl dgst -md5 -binary | base64)
> ```

> [tab] curl
>
> ```bash theme={"system"}
> # Check encryption with a HEAD request on a specific object
> curl -I \
>   -H "x-amz-server-side-encryption-customer-algorithm: AES256" \
>   -H "x-amz-server-side-encryption-customer-key: $BASE64_KEY" \
>   -H "x-amz-server-side-encryption-customer-key-md5: $(echo -n "$BASE64_KEY" | base64 -d | openssl dgst -md5 -binary | base64)" \
>   "https://[BUCKET-NAME].cwobject.com/[OBJECT-KEY]" \
>   | grep -i encryption
> ```

## Error handling

When you use SSE-C, you may encounter specific errors:

| Error | Meaning |
| - | - |
| `InvalidArgument` | The encryption key isn't 256 bits (32 bytes) |
| `InvalidRequest` | The encryption key MD5 hash doesn't match |
| `AccessDenied` | The encryption key provided doesn't match the one used for upload |
| `NoSuchKey` | The object doesn't exist or the encryption key is incorrect |

Implement error handling in your applications. For example:

```python theme={"system"}
from botocore.exceptions import ClientError

try:
    s3_client.download_file(
        '[BUCKET-NAME]',
        '[OBJECT-KEY]',
        '[LOCAL-FILE-PATH]',
        ExtraArgs={
            'SSECustomerAlgorithm': 'AES256',
            'SSECustomerKey': encryption_key,
            'SSECustomerKeyMD5': key_md5_b64
        }
    )
except ClientError as e:
    error_code = e.response['Error']['Code']
    if error_code == 'InvalidArgument':
        print("Invalid encryption key format")
    elif error_code == 'AccessDenied':
        print("Incorrect encryption key")
    else:
        print(f"Error: {error_code}")
```

## Key management

Because CoreWeave doesn't store your encryption keys, how you generate, store, and rotate those keys determines whether your data stays accessible and secure. The following sections cover the practices to follow when managing SSE-C keys in production.

### Store keys securely

Never store encryption keys in plain text or in your application code. Use secure key management solutions:

* **Environment variables**: Store keys in environment variables (not in code).
* **Secret management systems**: Use tools like HashiCorp Vault, AWS Secrets Manager, or Kubernetes Secrets.
* **Hardware Security Modules (HSMs)**: For high-security requirements, use HSMs to generate and store keys.

### Centralize key management

Create a centralized key management system in your application:

```python theme={"system"}
import hashlib
import base64

class SSEKeyManager:
    def __init__(self, key_id):
        self.key_id = key_id
        self.key = self.load_key(key_id)

    def get_encryption_headers(self):
        """Generate SSE-C headers for S3 requests"""
        key_md5 = hashlib.md5(base64.b64decode(self.key)).digest()
        key_md5_b64 = base64.b64encode(key_md5).decode('utf-8')

        return {
            'SSECustomerAlgorithm': 'AES256',
            'SSECustomerKey': self.key,
            'SSECustomerKeyMD5': key_md5_b64
        }

    def load_key(self, key_id):
        """Load key from secure storage"""
        # Implement secure key loading logic
        pass
```

### Validate encryption keys

Validate encryption keys before use:

```python theme={"system"}
def validate_encryption_key(key):
    """Validate that the encryption key meets requirements"""
    if not isinstance(key, str):
        raise ValueError("Encryption key must be a string")

    try:
        # Decode base64 to check if it's valid
        key_bytes = base64.b64decode(key)
        if len(key_bytes) != 32:  # 32 bytes = 256 bits
            raise ValueError("Encryption key must be 32 bytes (256 bits)")
    except Exception:
        raise ValueError("Encryption key must be valid base64-encoded 32-byte key")

    return True
```

## Advanced topics

The following sections cover advanced SSE-C use cases, including presigned URLs, bucket policy enforcement, and production best practices.

### SSE-C with presigned URLs

When using SSE-C with presigned URLs, you must include the encryption parameters when generating the URL and when accessing it. The encryption key is required both during URL generation and when you use the URL.

#### Generate presigned URLs with SSE-C

> [tab] Boto3
>
> Set environment variables for your CoreWeave credentials and encryption key:
>
> ```bash theme={"system"}
> export ACCESS_KEY_ID="[ACCESS-KEY-ID]"
> export SECRET_ACCESS_KEY="[SECRET-ACCESS-KEY]"
> export BASE64_KEY="[ENCRYPTION-KEY]"
> ```
>
> Replace `[BUCKET-NAME]` with the bucket name and `[OBJECT-KEY]` with the key of the object to generate a presigned URL for.
>
> ```python theme={"system"}
> import os
> import boto3
> import hashlib
> import base64
> from botocore.client import Config
>
> boto_config = Config(
>     region_name='US-EAST-04A',
>     s3={'addressing_style': 'virtual'}
> )
>
> s3_client = boto3.client(
>     's3',
>     endpoint_url='https://cwobject.com',
>     aws_access_key_id=os.environ['ACCESS_KEY_ID'],
>     aws_secret_access_key=os.environ['SECRET_ACCESS_KEY'],
>     config=boto_config
> )
>
> encryption_key = os.environ['BASE64_KEY']
> key_md5 = hashlib.md5(base64.b64decode(encryption_key)).digest()
> key_md5_b64 = base64.b64encode(key_md5).decode('utf-8')
>
> presigned_url = s3_client.generate_presigned_url(
>     'get_object',
>     Params={
>         'Bucket': '[BUCKET-NAME]',
>         'Key': '[OBJECT-KEY]',
>         'SSECustomerAlgorithm': 'AES256',
>         'SSECustomerKey': encryption_key,
>         'SSECustomerKeyMD5': key_md5_b64
>     },
>     ExpiresIn=3600
> )
>
> print(f"Presigned URL: {presigned_url}")
> ```

> [tab] AWS CLI
>
> ```bash theme={"system"}
> export OBJECT_KEY="[OBJECT-KEY]"
> export BUCKET_NAME="[BUCKET-NAME]"
> export BASE64_KEY="[ENCRYPTION-KEY]"
> ```
>
> ```bash theme={"system"}
> # Generate presigned URL with SSE-C
> aws s3 presign "s3://$BUCKET_NAME/$OBJECT_KEY" \
>   --expires-in 3600 \
>   --sse-customer-algorithm AES256 \
>   --sse-customer-key $BASE64_KEY \
>   --sse-customer-key-md5 $(echo -n "$BASE64_KEY" | base64 -d | openssl dgst -md5 -binary | base64)
> ```

#### Use presigned URLs with SSE-C

When you access a presigned URL that was generated with SSE-C, you must include the same encryption headers in the request. Use the presigned URL generated by Boto3 or the AWS CLI, then pass it to curl with the SSE-C headers:

```bash theme={"system"}
curl -H "x-amz-server-side-encryption-customer-algorithm: AES256" \
  -H "x-amz-server-side-encryption-customer-key: $BASE64_KEY" \
  -H "x-amz-server-side-encryption-customer-key-md5: $(echo -n "$BASE64_KEY" | base64 -d | openssl dgst -md5 -binary | base64)" \
  "[PRESIGNED-URL]"
```

### SSE-C with bucket policies

You can configure bucket policies to enforce SSE-C usage for specific operations. This ensures that objects are always encrypted with customer-provided keys.

#### Enforce SSE-C for uploads

Create a bucket policy that requires SSE-C for all upload operations:

> [tab] AWS CLI
>
> Set an environment variable for the bucket name:
>
> ```bash theme={"system"}
> export BUCKET_NAME="[BUCKET-NAME]"
> ```
>
> ```bash theme={"system"}
> # Save the policy to a file
> cat > ssec-policy.json << EOF
> {
>     "Version": "2012-10-17",
>     "Statement": [
>         {
>             "Sid": "EnforceSSECForUploads",
>             "Effect": "Deny",
>             "Principal": "*",
>             "Action": [
>                 "s3:PutObject"
>             ],
>             "Resource": "arn:aws:s3:::${BUCKET_NAME}/*",
>             "Condition": {
>                 "StringNotEquals": {
>                     "s3:x-amz-server-side-encryption-customer-algorithm": "AES256"
>                 }
>             }
>         },
>         {
>             "Sid": "EnforceSSECKeyForUploads",
>             "Effect": "Deny",
>             "Principal": "*",
>             "Action": [
>                 "s3:PutObject"
>             ],
>             "Resource": "arn:aws:s3:::${BUCKET_NAME}/*",
>             "Condition": {
>                 "Null": {
>                     "s3:x-amz-server-side-encryption-customer-key": "true"
>                 }
>             }
>         }
>     ]
> }
> EOF
> ```
>
> > [!NOTE]
> >
> > To have environment variables like `$BUCKET_NAME` evaluated within a heredoc, use `<< EOF` (unquoted) instead of `<< 'EOF'` (single-quoted). Single quotes prevent variable expansion.
>
> Apply the policy:
>
> ```bash theme={"system"}
> # Apply the policy
> aws s3api put-bucket-policy --bucket $BUCKET_NAME --policy file://ssec-policy.json
> ```

> [tab] Boto3
>
> Set environment variables for your CoreWeave credentials:
>
> ```bash theme={"system"}
> export ACCESS_KEY_ID="[ACCESS-KEY-ID]"
> export SECRET_ACCESS_KEY="[SECRET-ACCESS-KEY]"
> ```
>
> Alternatively, configure your CoreWeave credentials to work with the AWS CLI.
>
> We recommend using a separate profile for CoreWeave AI Object Storage to avoid conflicts with your other AWS profiles and S3-compatible services. If you don't set up this configuration, you might encounter errors when using AI Object Storage. If you have no other [AWS profiles](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html#cli-configure-files-using-profiles), you can use the [`default`](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html#cli-configure-files-format-profile) profile instead of the `cw` profile created in the following steps. In that case, omit `--profile cw` from the commands.
>
> > [!TIP]
> >
> > For production workloads, CoreWeave recommends [Workload Identity Federation](https://docs.coreweave.com/products/storage/object-storage/auth-access/workload-identity-federation/about.md) for automated, short-lived credentials instead of static access keys.
>
> > [accordion] Configure CoreWeave credentials with static access keys
> >
> > 1. Create a `cw` profile:
> >
> >    ```bash title="Create a new profile" theme={"system"}
> >    aws configure --profile cw
> >    ```
> >
> > 2. When prompted, provide the following values:
> >
> >    * **AWS Access Key ID**: The [Access Key](https://docs.coreweave.com/products/storage/object-storage/auth-access/manage-access-keys/create-keys.md) ID of your CoreWeave AI Object Storage Access Key.
> >    * **AWS Secret Access Key**: The Secret Key of your CoreWeave AI Object Storage Access Key.
> >    * **Default region name** (Optional): To set a default region, see [CoreWeave Availability Zones](https://docs.coreweave.com/products/storage/object-storage/buckets/manage-buckets.md#availability-zones).
> >    * **Default output format**: Use `json` for JSON output.
> >
> > 3. Set the default endpoint URL to the appropriate endpoint for your use case:
> >
> >    * The primary endpoint, `https://cwobject.com`, for use outside a CoreWeave cluster.
> >    * The LOTA endpoint, `http://cwlota.com`, for use inside a CoreWeave cluster. The LOTA endpoint routes to the LOTA path for best performance.
> >
> >    ```bash title="Set the primary endpoint for local development" theme={"system"}
> >    aws configure set endpoint_url https://cwobject.com --profile cw
> >    ```
> >
> > 4. Set the S3 `addressing_style` to `virtual`:
> >
> >    ```bash title="Set virtual addressing style" theme={"system"}
> >    aws configure set s3.addressing_style virtual --profile cw
> >    ```
> >
> > To use this profile, pass `--profile cw` to your AWS CLI commands, or set `AWS_PROFILE=cw` in your environment.
> >
> > If you set `endpoint_url` and `s3.addressing_style` directly in your code (for example, in a Boto3 `Config` object), you can skip steps 3 and 4. The profile only needs the access key, secret key, and region.
>
> > [accordion] Configure CoreWeave credentials with Workload Identity Federation (OIDC)
> >
> > If you've configured [Workload Identity Federation with OIDC](https://docs.coreweave.com/products/storage/object-storage/auth-access/workload-identity-federation/use-oidc-tokens.md), the AWS SDK automatically discovers temporary credentials. Set the following environment variables instead of configuring static access keys.
> >
> > Replace `[ORG-ID]` with your CoreWeave organization ID, `[PATH-TO-JWT-TOKEN-FILE]` with the path to your JWT token file, and `[AVAILABILITY-ZONE]` with your CoreWeave Availability Zone.
> >
> > ```bash title="Configure WIF OIDC credentials" theme={"system"}
> > export AWS_CONTAINER_CREDENTIALS_FULL_URI=https://api.coreweave.com/v1/cwobject/temporary-credentials/oidc/[ORG-ID]
> > export AWS_CONTAINER_AUTHORIZATION_TOKEN_FILE=[PATH-TO-JWT-TOKEN-FILE]
> >
> > aws configure set s3.addressing_style virtual
> >
> > export AWS_REGION="[AVAILABILITY-ZONE]"
> > export AWS_ENDPOINT_URL_S3="https://cwobject.com"
> > ```
> >
> > With WIF configured, your S3-compatible tools and Boto3 code automatically obtain and refresh temporary credentials without passing access keys explicitly.
> >
> > Requires `awscli >= 2.33.2` or `boto3 >= 1.42.5`. See [Use Workload Identity Federation with OIDC](https://docs.coreweave.com/products/storage/object-storage/auth-access/workload-identity-federation/use-oidc-tokens.md) for the full setup guide.
>
> Replace `[BUCKET-NAME]` with the name of the bucket to apply the policy to.
>
> ```python theme={"system"}
> import os
> import boto3
> import json
> from botocore.client import Config
>
> boto_config = Config(
>     region_name='US-EAST-04A',
>     s3={'addressing_style': 'virtual'}
> )
>
> s3_client = boto3.client(
>     's3',
>     endpoint_url='https://cwobject.com',
>     aws_access_key_id=os.environ['ACCESS_KEY_ID'],
>     aws_secret_access_key=os.environ['SECRET_ACCESS_KEY'],
>     config=boto_config
> )
>
> bucket_name = '[BUCKET-NAME]'
>
> bucket_policy = {
>     "Version": "2012-10-17",
>     "Statement": [
>         {
>             "Sid": "EnforceSSECForUploads",
>             "Effect": "Deny",
>             "Principal": "*",
>             "Action": [
>                 "s3:PutObject"
>             ],
>             "Resource": f"arn:aws:s3:::{bucket_name}/*",
>             "Condition": {
>                 "StringNotEquals": {
>                     "s3:x-amz-server-side-encryption-customer-algorithm": "AES256"
>                 }
>             }
>         },
>         {
>             "Sid": "EnforceSSECKeyForUploads",
>             "Effect": "Deny",
>             "Principal": "*",
>             "Action": [
>                 "s3:PutObject"
>             ],
>             "Resource": f"arn:aws:s3:::{bucket_name}/*",
>             "Condition": {
>                 "Null": {
>                     "s3:x-amz-server-side-encryption-customer-key": "true"
>                 }
>             }
>         }
>     ]
> }
>
> s3_client.put_bucket_policy(
>     Bucket=bucket_name,
>     Policy=json.dumps(bucket_policy)
> )
> ```

> [tab] curl
>
> ```bash theme={"system"}
> # Create the policy JSON
> cat > ssec-policy.json << 'EOF'
> {
>     "Version": "2012-10-17",
>     "Statement": [
>         {
>             "Sid": "EnforceSSECForUploads",
>             "Effect": "Deny",
>             "Principal": "*",
>             "Action": [
>                 "s3:PutObject"
>             ],
>             "Resource": "arn:aws:s3:::[BUCKET-NAME]/*",
>             "Condition": {
>                 "StringNotEquals": {
>                     "s3:x-amz-server-side-encryption-customer-algorithm": "AES256"
>                 }
>             }
>         },
>         {
>             "Sid": "EnforceSSECKeyForUploads",
>             "Effect": "Deny",
>             "Principal": "*",
>             "Action": [
>                 "s3:PutObject"
>             ],
>             "Resource": "arn:aws:s3:::[BUCKET-NAME]/*",
>             "Condition": {
>                 "Null": {
>                     "s3:x-amz-server-side-encryption-customer-key": "true"
>                 }
>             }
>         }
>     ]
> }
> EOF
>
> # Apply the bucket policy using curl
> curl -X PUT \
>   -H "Content-Type: application/json" \
>   -d @ssec-policy.json \
>   "https://[BUCKET-NAME].cwobject.com?policy"
> ```

#### Enforce SSE-C for specific prefixes

You can also enforce SSE-C only for specific object prefixes. For example, the following policy denies uploads to any object under the `sensitive/` prefix unless the request uses SSE-C with the `AES256` algorithm. This ensures that only objects stored under `[BUCKET-NAME]/sensitive/` require customer-provided encryption keys, while other objects in the bucket aren't affected by this policy.

Replace `[BUCKET-NAME]` with the name of your bucket.

```json theme={"system"}
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "EnforceSSECForSensitiveData",
            "Effect": "Deny",
            "Principal": "*",
            "Action": [
                "s3:PutObject"
            ],
            "Resource": "arn:aws:s3:::[BUCKET-NAME]/sensitive/*",
            "Condition": {
                "StringNotEquals": {
                    "s3:x-amz-server-side-encryption-customer-algorithm": "AES256"
                }
            }
        }
    ]
}
```

#### Allow specific encryption keys

For tighter security, you can restrict uploads to specific encryption keys by checking the key hash.

Replace `[BUCKET-NAME]` with the name of your bucket and `[KEY-MD5-HASH]` with the base64-encoded MD5 hash of the allowed encryption key.

```json theme={"system"}
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "AllowSpecificEncryptionKey",
            "Effect": "Allow",
            "Principal": "*",
            "Action": [
                "s3:PutObject"
            ],
            "Resource": "arn:aws:s3:::[BUCKET-NAME]/*",
            "Condition": {
                "StringEquals": {
                    "s3:x-amz-server-side-encryption-customer-algorithm": "AES256",
                    "s3:x-amz-server-side-encryption-customer-key-md5": "[KEY-MD5-HASH]"
                }
            }
        }
    ]
}
```

### Best practices

The following sections describe practices to follow when running SSE-C in production.

#### Rotate encryption keys

Rotate your SSE-C encryption keys on a regular schedule to reduce risk from key compromise. To rotate a key, download objects encrypted with the old key and re-upload them with a new key. Use a secret management system such as HashiCorp Vault, AWS Secrets Manager, or Kubernetes Secrets to track key versions and expiry dates. Establish a rotation schedule that aligns with your organization's security policies.

#### Cache encryption headers

Avoid recalculating the base64-encoded MD5 hash of your encryption key for every request. Compute the key hash once and store it in an environment variable or application configuration for reuse across operations. This reduces computational overhead, especially in high-throughput workloads.

#### Monitor key operations

Log all SSE-C upload, download, and copy operations to maintain an audit trail. Track which keys are used for which objects, and record key rotation events. Integrate with your existing logging and monitoring infrastructure to detect unauthorized access attempts or missing key errors.

#### Validate keys before use

Before you use an encryption key in an SSE-C operation, verify that it's valid base64 and decodes to exactly 32 bytes (256 bits). Validating keys upfront prevents cryptic errors during upload or download operations.

## Additional resources

* Review the [SSE-C concept guide](https://docs.coreweave.com/products/storage/object-storage/buckets/server-side-encryption/about-sse-c.md) to learn more about how SSE-C works.
* Check the [S3 API reference](https://docs.coreweave.com/products/storage/object-storage/reference/object-storage-s3.md) for detailed SSE-C headers and parameters.
* Explore [key management best practices](https://docs.coreweave.com/products/storage/object-storage/buckets/server-side-encryption/about-sse-c.md#security-considerations-and-responsibilities) for production deployments.
* For more information about SSE-C implementation, see the [AWS documentation on using server-side encryption with customer-provided keys](https://docs.aws.amazon.com/AmazonS3/latest/userguide/ServerSideEncryptionCustomerKeys.html).
