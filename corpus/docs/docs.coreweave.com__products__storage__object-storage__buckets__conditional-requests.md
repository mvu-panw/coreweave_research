# Use conditional requests

Source: https://docs.coreweave.com/products/storage/object-storage/buckets/conditional-requests

# Use conditional requests

> Skip unnecessary downloads and prevent accidental overwrites using conditional request headers

CoreWeave AI Object Storage supports conditional requests on reads and writes. A conditional request attaches an HTTP precondition header to an S3 API call. The operation proceeds only if the precondition holds. Otherwise, the server returns an error and doesn't modify or transfer the object. Use conditional requests to skip unnecessary downloads when objects haven't changed, and to prevent accidental overwrites when multiple writers might update the same object.

## About ETags

An ETag (entity tag) is a content fingerprint that the server returns for every object. The response of `PutObject`, `HeadObject`, and `GetObject` calls includes the ETag. When an object's content changes, its ETag changes. Use `HeadObject` to retrieve the current ETag without downloading the object.

The server returns ETags as quoted hex strings, for example `"1b2cf535f27731c97434645a985325"`. Include the quotes when you pass an ETag to a precondition header.

## Conditional reads

Conditional reads let you skip a `GetObject` download when the object hasn't changed since the last time you read it. Pass the ETag you last received as the `If-None-Match` value. If the object hasn't changed, the server returns `304 Not Modified` and transfers no data. If the object has changed, the download proceeds.

Use `If-Match` to download only when the object matches a specific ETag, or to detect that the object changed since you last read it.

> [tab] AWS CLI
>
> Replace `[BUCKET-NAME]`, `[OBJECT-KEY]`, `[LAST-KNOWN-ETAG]`, and `[LOCAL-OUTPUT-PATH]` with the appropriate values.
>
> ```bash theme={"system"}
> aws s3api get-object \
>   --bucket [BUCKET-NAME] \
>   --key [OBJECT-KEY] \
>   --if-none-match '"[LAST-KNOWN-ETAG]"' \
>   --endpoint-url https://cwobject.com \
>   [LOCAL-OUTPUT-PATH]
> ```
>
> If the ETag matches (the object hasn't changed), the command returns an error that wraps the `304 Not Modified` response.

> [tab] Boto3
>
> 1. Set the environment variables for your Object Storage access key and secret key:
>
>    ```bash theme={"system"}
>    export ACCESS_KEY_ID="[ACCESS-KEY-ID]"
>    export SECRET_ACCESS_KEY="[SECRET-ACCESS-KEY]"
>    ```
>
> 2. Replace `[BUCKET-NAME]`, `[OBJECT-KEY]`, and `[LAST-KNOWN-ETAG]` with the appropriate values:
>
>    ```python title="Download only if the object has changed" theme={"system"}
>    import os
>    import boto3
>    from botocore.client import Config
>    from botocore.exceptions import ClientError
>
>    boto_config = Config(
>        region_name='US-EAST-04A',
>        s3={'addressing_style': 'virtual'}
>    )
>
>    s3 = boto3.client(
>        's3',
>        endpoint_url='https://cwobject.com',
>        aws_access_key_id=os.environ['ACCESS_KEY_ID'],
>        aws_secret_access_key=os.environ['SECRET_ACCESS_KEY'],
>        config=boto_config
>    )
>
>    try:
>        response = s3.get_object(
>            Bucket='[BUCKET-NAME]',
>            Key='[OBJECT-KEY]',
>            IfNoneMatch='[LAST-KNOWN-ETAG]',
>        )
>        data = response['Body'].read()
>        print(f"Downloaded {len(data)} bytes. New ETag: {response['ETag']}")
>    except ClientError as e:
>        if e.response['ResponseMetadata']['HTTPStatusCode'] == 304:
>            print("Object unchanged, no download needed")
>        else:
>            raise
>    ```

## Conditional writes

Conditional writes prevent accidental overwrites by requiring that a precondition holds before `PutObject`, `CompleteMultipartUpload`, `CopyObject`, or `RenameObject` modifies an object. If the precondition fails, the server returns `412 Precondition Failed` and doesn't modify the object. `RenameObject` supports a richer set of conditional headers, including separate source and destination preconditions and time-based conditions. See [RenameObject conditionals](#renameobject-conditionals) for details.

Conditional writes support two patterns:

| Pattern | Header | Value | Behavior |
| - | - | - | - |
| Safe create | `If-None-Match` | `*` | Write only if no object exists at the key. |
| Compare-and-swap | `If-Match` | ETag value | Write only if the object's current ETag matches. |

For full header constraints, see [Conditional writes](https://docs.coreweave.com/products/storage/object-storage/reference/object-storage-s3.md#conditional-writes) in the S3 API reference. To require these preconditions for every writer instead of relying on each client to send them, see [Require conditional writes](https://docs.coreweave.com/products/storage/object-storage/auth-access/bucket-access/bucket-policies.md#require-conditional-writes).

### Safe create

Use `If-None-Match: *` to write an object only if no object already exists at that key. This prevents overwriting existing data even when multiple writers race for the same key.

If two concurrent requests use `If-None-Match: *` for the same key, one succeeds and the other returns `409 ConditionalRequestConflict`. Retry the request on `409`.

> [tab] AWS CLI
>
> Replace `[BUCKET-NAME]`, `[OBJECT-KEY]`, and `[LOCAL-FILE-PATH]` with the appropriate values.
>
> ```bash theme={"system"}
> aws s3api put-object \
>   --bucket [BUCKET-NAME] \
>   --key [OBJECT-KEY] \
>   --body [LOCAL-FILE-PATH] \
>   --if-none-match '*' \
>   --endpoint-url https://cwobject.com
> ```

> [tab] Boto3
>
> 1. Set the environment variables for your Object Storage access key and secret key:
>
>    ```bash theme={"system"}
>    export ACCESS_KEY_ID="[ACCESS-KEY-ID]"
>    export SECRET_ACCESS_KEY="[SECRET-ACCESS-KEY]"
>    ```
>
> 2. Replace `[BUCKET-NAME]`, `[OBJECT-KEY]`, and `[LOCAL-FILE-PATH]` with the appropriate values:
>
>    ```python title="Write only if the object does not exist" theme={"system"}
>    import os
>    import boto3
>    from botocore.client import Config
>    from botocore.exceptions import ClientError
>
>    boto_config = Config(
>        region_name='US-EAST-04A',
>        s3={'addressing_style': 'virtual'}
>    )
>
>    s3 = boto3.client(
>        's3',
>        endpoint_url='https://cwobject.com',
>        aws_access_key_id=os.environ['ACCESS_KEY_ID'],
>        aws_secret_access_key=os.environ['SECRET_ACCESS_KEY'],
>        config=boto_config
>    )
>
>    try:
>        response = s3.put_object(
>            Bucket='[BUCKET-NAME]',
>            Key='[OBJECT-KEY]',
>            Body=open('[LOCAL-FILE-PATH]', 'rb'),
>            IfNoneMatch='*',
>        )
>        print(f"Created. ETag: {response['ETag']}")
>    except ClientError as e:
>        code = e.response['Error']['Code']
>        if code == 'PreconditionFailed':
>            print("Object already exists, write skipped")
>        elif code == 'ConditionalRequestConflict':
>            print("Concurrent write conflict, retry the request")
>        else:
>            raise
>    ```

### Compare-and-swap

Use `If-Match` with the current ETag to write an object only if it hasn't changed since you last read it. This detects concurrent updates that occur between your read and write.

The workflow is:

1. Call `HeadObject` to retrieve the current ETag.
2. Perform your local computation or modification.
3. Call `PutObject` with `If-Match` set to the ETag from step 1.

If another writer modifies the object between step 1 and step 3, the server returns `412 Precondition Failed`. Retry from step 1 to read the updated object.

> [tab] AWS CLI
>
> Replace `[BUCKET-NAME]`, `[OBJECT-KEY]`, and `[LOCAL-FILE-PATH]` with the appropriate values.
>
> ```bash theme={"system"}
> # Step 1: Get the current ETag
> ETAG=$(aws s3api head-object \
>   --bucket [BUCKET-NAME] \
>   --key [OBJECT-KEY] \
>   --endpoint-url https://cwobject.com \
>   --query ETag --output text)
>
> # Step 2: Write only if the ETag still matches
> aws s3api put-object \
>   --bucket [BUCKET-NAME] \
>   --key [OBJECT-KEY] \
>   --body [LOCAL-FILE-PATH] \
>   --if-match "$ETAG" \
>   --endpoint-url https://cwobject.com
> ```

> [tab] Boto3
>
> 1. Set the environment variables for your Object Storage access key and secret key:
>
>    ```bash theme={"system"}
>    export ACCESS_KEY_ID="[ACCESS-KEY-ID]"
>    export SECRET_ACCESS_KEY="[SECRET-ACCESS-KEY]"
>    ```
>
> 2. Replace `[BUCKET-NAME]`, `[OBJECT-KEY]`, and `[LOCAL-FILE-PATH]` with the appropriate values:
>
>    ```python title="Atomic compare-and-swap" theme={"system"}
>    import os
>    import boto3
>    from botocore.client import Config
>    from botocore.exceptions import ClientError
>
>    boto_config = Config(
>        region_name='US-EAST-04A',
>        s3={'addressing_style': 'virtual'}
>    )
>
>    s3 = boto3.client(
>        's3',
>        endpoint_url='https://cwobject.com',
>        aws_access_key_id=os.environ['ACCESS_KEY_ID'],
>        aws_secret_access_key=os.environ['SECRET_ACCESS_KEY'],
>        config=boto_config
>    )
>
>    # Step 1: Get the current ETag
>    head = s3.head_object(
>        Bucket='[BUCKET-NAME]',
>        Key='[OBJECT-KEY]',
>    )
>    current_etag = head['ETag']
>
>    # Step 2: Write only if the ETag still matches
>    try:
>        response = s3.put_object(
>            Bucket='[BUCKET-NAME]',
>            Key='[OBJECT-KEY]',
>            Body=open('[LOCAL-FILE-PATH]', 'rb'),
>            IfMatch=current_etag,
>        )
>        print(f"Updated. New ETag: {response['ETag']}")
>    except ClientError as e:
>        if e.response['Error']['Code'] == 'PreconditionFailed':
>            print("Another writer modified the object, retry from head_object")
>        else:
>            raise
>    ```

## RenameObject conditionals

`RenameObject` supports a richer set of conditional headers, including separate preconditions for the source and destination objects, and time-based conditions. For the full list of supported headers and usage examples, see [Preconditions and safeguards](https://docs.coreweave.com/products/storage/object-storage/buckets/rename-objects.md#preconditions-and-safeguards) in the rename objects guide.
