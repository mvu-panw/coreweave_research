# File operations

Source: https://docs.coreweave.com/products/sandboxes/client/guides/file-operations

# File operations

> Read, write, and manage files within CoreWeave sandbox instances using the CWSandbox client

This guide shows you how to read, write, and manage files inside a CoreWeave sandbox instance using the CWSandbox client. It's intended for developers who build workflows that move data into and out of sandboxes, including parallel uploads and downloads, error handling, and patterns for large files.

## Choose authentication

These examples run on serverless capacity unless a section specifies CKS. Choose the credential for the account that owns your sandboxes. See [Choose and get credentials](https://docs.coreweave.com/products/sandboxes/placement.md#choose-and-get-credentials) to obtain a key or token.

Run the installation commands in an [active Python virtual environment](https://docs.coreweave.com/products/sandboxes/client.md#prepare-your-python-environment).

Save the Python code from your credential tab as `sandbox_auth.py` beside the Python scripts you run from this page. It stores the authentication choice, not your credential. The examples import `AUTH` from that file and pass it explicitly to each new sandbox or session.

> [tab] Forge API key
>
> Use your Forge API key through the SDK's W\&B authentication strategy:
>
> ```bash theme={"system"}
> uv pip install 'cwsandbox[wandb]>=1.14.2'
> export WANDB_API_KEY="[WANDB-API-KEY]"
> ```
>
> ```python title="sandbox_auth.py" theme={"system"}
> from cwsandbox import AuthStrategy
>
> AUTH = AuthStrategy.WANDB
> ```

> [tab] CoreWeave API access token
>
> Use the token for your CoreWeave organization:
>
> ```bash theme={"system"}
> uv pip install 'cwsandbox>=1.14.2'
> export CWSANDBOX_API_KEY="[API-ACCESS-TOKEN]"
> ```
>
> ```python title="sandbox_auth.py" theme={"system"}
> from cwsandbox import AuthStrategy
>
> AUTH = AuthStrategy.COREWEAVE_API_KEY
> ```

For CKS placement, choose the CoreWeave token, [enable a runner](https://docs.coreweave.com/products/sandboxes/get-started-cks.md), and set `placement_mode="cks"` on sandbox creation or in `SandboxDefaults`. Creating a session with `auth=AUTH` also authenticates the sandboxes it owns. Keep the same credential when reconnecting, listing, or cleaning up sandboxes.

## Basic operations

The examples in this section cover the most common file operations: writing data to a path in the sandbox and reading data back. File operations return `OperationRef` objects. Use `.result()` to block for completion.

### Write files

Keep the sandbox running while you write and read files. This example creates two files, then reads them before the context manager stops the sandbox:

```python theme={"system"}
import json

from sandbox_auth import AUTH
from cwsandbox import Sandbox

with Sandbox.run(resources={"cpu": "1", "memory": "1Gi"}, auth=AUTH) as sandbox:
    sandbox.write_file("/tmp/data.txt", b"Hello, World!").result()

    config = {"key": "value", "count": 42}
    sandbox.write_file("/tmp/config.json", json.dumps(config).encode()).result()

    content = sandbox.read_file("/tmp/data.txt").result()
    print(content.decode())  # "Hello, World!"

    config_bytes = sandbox.read_file("/tmp/config.json").result()
    restored_config = json.loads(config_bytes.decode())
    print(restored_config)
```

### Read files

`read_file()` returns file contents as bytes. The example in [Write files](#write-files) uses `decode()` to read text and `json.loads()` to parse JSON. Both reads run inside the active sandbox context.

## Parallel operations

File operations return immediately, enabling natural parallelism. Running uploads or downloads in parallel can reduce total transfer time when you have multiple independent files.

### Parallel uploads

```python theme={"system"}
from cwsandbox import results

# Start all uploads simultaneously
write_refs = [
    sandbox.write_file("/app/config.json", config_bytes),
    sandbox.write_file("/app/data.csv", data_bytes),
    sandbox.write_file("/app/model.pkl", model_bytes),
]

# Wait for all to complete
results(write_refs)
```

### Parallel downloads

```python theme={"system"}
# Start all downloads simultaneously
read_refs = [
    sandbox.read_file("/app/output.json"),
    sandbox.read_file("/app/metrics.json"),
    sandbox.read_file("/app/logs.txt"),
]

# Get all results
output, metrics, logs = results(read_refs)
```

## Upload-process-download pattern

A common workflow: upload input files, run processing, download results.

```python theme={"system"}
from sandbox_auth import AUTH
from cwsandbox import Sandbox, results

with Sandbox.run(resources={"cpu": "1", "memory": "1Gi"}, auth=AUTH) as sandbox:
    # 1. Parallel uploads
    results([
        sandbox.write_file("/app/config.json", config_bytes),
        sandbox.write_file("/app/input.csv", input_bytes),
    ])

    # 2. Sequential processing
    sandbox.exec(["pip", "install", "-r", "requirements.txt"]).result()
    sandbox.exec(["python", "/app/process.py"]).result()

    # 3. Parallel downloads
    output, metrics = results([
        sandbox.read_file("/app/output.json"),
        sandbox.read_file("/app/metrics.json"),
    ])
```

## Error handling

File operations can fail if a path doesn't exist or isn't writable. Catch `SandboxFileError` to handle these cases and inspect the affected path.

### File not found

```python theme={"system"}
from cwsandbox import SandboxFileError

try:
    content = sandbox.read_file("/nonexistent/file.txt").result()
except SandboxFileError as e:
    print(f"File error: {e.filepath}")
```

### Write errors

```python theme={"system"}
try:
    sandbox.write_file("/readonly/path.txt", b"data").result()
except SandboxFileError as e:
    print(f"Cannot write to: {e.filepath}")
```

## Binary files

File operations work with any binary content, including images and serialized Python objects:

```python theme={"system"}
# Images
with open("image.png", "rb") as f:
    sandbox.write_file("/app/image.png", f.read()).result()

# Pickle files (only unpickle data from trusted sources)
import pickle
model_bytes = pickle.dumps(my_model)
sandbox.write_file("/app/model.pkl", model_bytes).result()

# Download and unpickle
model_bytes = sandbox.read_file("/app/trained_model.pkl").result()
trained_model = pickle.loads(model_bytes)
```

> [!WARNING]
>
> Only unpickle data from sources you trust. Loading a pickle file can execute arbitrary code.

## Text encoding

Files are transferred as bytes, so you must encode and decode text explicitly to avoid corruption with non-ASCII characters.

```python theme={"system"}
# Write text
text = "Hello, Unicode! "
sandbox.write_file("/app/text.txt", text.encode("utf-8")).result()

# Read text
content = sandbox.read_file("/app/text.txt").result()
text = content.decode("utf-8")
```

## Large file considerations

The `read_file` and `write_file` APIs are best suited for small to moderately sized files. For large files, consider the following:

* Account for bandwidth, because files are transferred through the API.
* Use streaming for large datasets when possible.
* Access object storage directly instead of transferring the data through the API.

The `object_storage_access` parameter creates temporary CoreWeave AI Object Storage credentials and provides them to the sandbox's containers. Your workload then reads and writes buckets directly, so large objects never pass through `read_file` or `write_file`. Your organization must first register a Workload Identity Federation configuration with the sandbox control plane; see [Object storage access](https://docs.coreweave.com/products/sandboxes/operations/object-storage-access.md).

The following example uses CoreWeave authentication to start a sandbox with read-write access to one bucket, then confirms the credentials were injected. Set `CWSANDBOX_API_KEY` to a CoreWeave API access token for the configured organization, and replace `[BUCKET-NAME]` with the name of your bucket:

```python theme={"system"}
from cwsandbox import AuthStrategy, ObjectStorageAccess, ObjectStoragePermission, Sandbox

with Sandbox.run(
    auth=AuthStrategy.COREWEAVE_API_KEY,
    container_image="python:3.11",
    object_storage_access=ObjectStorageAccess(
        buckets=["[BUCKET-NAME]"],
        permission=ObjectStoragePermission.READ_WRITE,
    ),
    resources={"cpu": "1", "memory": "1Gi"},
) as sandbox:
    result = sandbox.exec(["printenv", "AWS_ENDPOINT_URL_S3"]).result()
    print(result.stdout)
```

The sandbox sets the environment variables that AWS SDKs read for container credentials, so any S3-compatible client inside it works without explicit keys. For those variables and a Boto3 example, see [Use the credentials inside the sandbox](https://docs.coreweave.com/products/sandboxes/operations/object-storage-access.md#step-5-use-the-credentials-inside-the-sandbox).

To limit the credential to a key prefix, use `object_prefix`. For workloads that only read data, use `ObjectStoragePermission.READ`.

For large temporary data that stays local to the sandbox, attach a volume instead. See [Volumes](https://docs.coreweave.com/products/sandboxes/volumes.md).
