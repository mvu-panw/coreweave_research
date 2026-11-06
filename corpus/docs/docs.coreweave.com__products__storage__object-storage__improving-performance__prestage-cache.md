# Pre-stage the LOTA cache

Source: https://docs.coreweave.com/products/storage/object-storage/improving-performance/prestage-cache

# Pre-stage the LOTA cache

> Proactively warm the LOTA cache by pre-loading entire objects with a single HeadObject call

The **Pre-stage Cache** feature lets you proactively warm the [LOTA (Local Object Transport Accelerator)](https://docs.coreweave.com/products/storage/object-storage/improving-performance/about-lota.md) cache for CoreWeave AI Object Storage. By issuing a `HeadObject` call against any object, you instruct LOTA to fetch the complete object from backend storage and place it into the distributed NVMe cache on your Nodes without transferring a response body to your client.

This eliminates the "cold start" latency penalty that occurs on first reads. Training jobs with a warm cache can see 30% to 50% faster first epochs, inference services can achieve sub-second Time-To-First-Token for large models, and checkpoint restores complete at full cache speed from the first byte.

Other benefits include:

* **Zero client bandwidth.** `HeadObject` returns only headers. All cache-fill traffic stays inside the backend CoreWeave network.
* **No SDK changes required.** Works with any S3-compatible tool or SDK (AWS CLI, Boto3, s3cmd) with no custom headers or proprietary extensions.

## Use cases

The following use cases benefit from pre-staging the LOTA cache:

| Use case | Description |
| - | - |
| **Pre-warm datasets before distributed training** | Issue `HeadObject` calls for every shard of the training dataset before launching distributed training across hundreds of GPUs. When the first epoch starts, all data-loading workers read directly from cache. |
| **Pre-load model weights for inference scale-up** | Pre-stage model files while compute Pods are initializing during an inference deployment scale-up. By the time pods are ready to serve traffic, model weights are already in cache, ensuring optimal Time-To-First-Token. |
| **Accelerate checkpoint-restore after failure** | After a node failure interrupts training, pre-stage the most recent checkpoint shards into cache before replacement pods start. This reduces downtime between failure and resumed training. |
| **Warm data for multi-region workflows** | Before running a production workload in a specific CoreWeave Availability Zone, pre-stage required objects into that Availability Zone's LOTA cache. This enables cache-speed performance from the first read, even if the bucket resides elsewhere. See [Pre-stage for cross-region workloads](https://docs.coreweave.com/products/storage/object-storage/improving-performance/prestage-cache.md#pre-stage-for-cross-region-workloads). |

## How it works

Pre-staging uses a `HeadObject` call with a `Range: bytes=0-0` header as the trigger. When LOTA receives this request:

1. The object storage gateway authenticates the request.
2. The object storage service returns the object's metadata (size, content type, ETag, last modified date) in the response headers, exactly as a normal `HeadObject` call.
3. LOTA fetches the complete object from the backend storage and writes it into the distributed NVMe cache across the Nodes in your CKS cluster.
4. LOTA serves future `GET` requests for that object directly from the cache.

Since `HeadObject` doesn't return a response body, pre-staging consumes minimal client-side resources and bandwidth. The cache fill happens entirely within the CoreWeave infrastructure.

### Whole object caching

Pre-staging caches the entire object, since a `HeadObject` call with a `Range: bytes=0-0` header caches the complete object. Byte-range pre-fetching of partial objects isn't supported. However, the LOTA cache serves range-reads as usual.

### LOTA endpoint required

Pre-staging works only through the LOTA endpoint (`http://cwlota.com`). `HeadObject` calls sent to the primary endpoint (`https://cwobject.com`) return metadata but don't trigger a cache fill.

### Billing and storage tier behavior

A `HeadObject` request with `bytes=0-0` counts as an object access, triggering the transition of an object from the Cold or Warm tier to the Hot [Storage Pricing](https://www.coreweave.com/pricing) tier. If `bytes=0-0` isn't included in the `HeadObject` request, no tier transition occurs.

> [!WARNING]
>
> Pre-staging a large number of objects transitions them all to the Hot pricing tier. Review the [Storage Pricing](https://www.coreweave.com/pricing) documentation to understand the cost implications before pre-staging at scale.

### Finite cache capacity

Total LOTA cache capacity scales with cluster size, with each Node contributing 3 TiB to the distributed cache by default (for example, a 30-Node cluster has approximately 90 TiB of cache). Pre-stage only the objects your workload will access in the near term. The cache uses LRU (Least Recently Used) eviction, so pre-staging more data than the cache can hold evicts objects that other active workloads may depend on. Use the [CAIOS LOTA dashboard](https://docs.coreweave.com/observability/managed-grafana/storage/caios-lota.md) to monitor cache utilization and hit rates. To request a larger cache allocation, [contact CoreWeave support](https://coreweave.freshdesk.com/support/login).

Before pre-staging a large dataset, check that the dataset fits in the cluster's cache. Multiply the number of objects by their average size to get the size of the working set, then multiply the per-Node cache capacity by the number of Nodes to get the total cache capacity of the cluster.

For example, suppose a cluster has approximately 30 TiB of cache in total. A dataset of 200,000 objects averaging 8 MB is a working set of about 1.6 TB, which fits. A dataset of 5 million objects averaging 8 MB is a working set of about 40 TB, which does not.

When the working set is larger than the cache, LOTA evicts objects that the same pre-stage pass still needs, and pre-stage requests can time out or fail with `502` or `503 Slow Down`.

## Pre-stage for cross-region workloads

Every AI Object Storage bucket resides in a home [Availability Zone](https://docs.coreweave.com/platform/regions/about-regions-and-azs.md). LOTA serves reads of a bucket from any Availability Zone by fetching objects from the home Availability Zone and caching them on local Nodes, so a workload does not need its own copy of the data. For details, see [Cross-region reads](https://docs.coreweave.com/products/storage/object-storage/improving-performance/about-lota.md#cross-region-reads).

AI Object Storage automatically pre-stages objects into the LOTA cache of clusters that run in the bucket's home Availability Zone, so workloads there start with a warm cache. Automatic pre-staging does not extend to other Availability Zones, including other Availability Zones in the same region. To give a workload outside the bucket's home Availability Zone the same warm cache, pre-stage the objects explicitly using the procedures on this page. Because AI Object Storage does not replicate buckets between Availability Zones, pre-staging is the recommended way to run a workload against a remote dataset at cache speed.

### When the transfer happens

A pre-stage pass fetches each object from the bucket's home Availability Zone, so the remote transfer still happens. What pre-staging changes is when the transfer happens: before your workload starts, rather than during the first epoch while GPUs wait for data. After an object is in the local cache, later reads are served from that cache and do not leave the workload's Availability Zone again.

If LOTA evicts an object, the next read fetches it from the home Availability Zone again. Pre-stage immediately before the compute step that needs the data, and check your working set against the available cache so that eviction does not undo the pass. See [Finite cache capacity](https://docs.coreweave.com/products/storage/object-storage/improving-performance/prestage-cache.md#finite-cache-capacity).

### Minimum object size for caching

LOTA caches only objects larger than 4 MB, and that threshold applies to remote reads as well. Pre-staging has no effect on smaller objects, which are fetched from the bucket's home Availability Zone on every read. A workload outside that Availability Zone that reads many small files pays the remote latency repeatedly, even after a pre-stage pass. Where you control how the data is written, packing small files into larger objects makes them eligible for the cache.

## Prerequisites

* An active [CoreWeave organization](https://docs.coreweave.com/security/authn-authz/activate-org.md) with at least one AI Object Storage bucket containing objects.
* A valid [API access key pair (Access Key ID and Secret Access Key)](https://docs.coreweave.com/products/storage/object-storage/auth-access/manage-access-keys/create-keys.md) configured for your organization. See [Get Started with AI Object Storage](https://docs.coreweave.com/products/storage/object-storage/get-started-caios.md) for setup instructions.
* A CKS cluster where your workload runs. Your workload must run inside a CoreWeave CKS cluster to reach the LOTA endpoint at `http://cwlota.com`.
* An S3-compatible client, such as AWS CLI, boto3 (Python), or s3cmd, installed and configured for CoreWeave AI Object Storage.

### Configure CoreWeave credentials

We recommend using a separate profile for CoreWeave AI Object Storage to avoid conflicts with your other AWS profiles and S3-compatible services. If you don't set up this configuration, you might encounter errors when using AI Object Storage. If you have no other [AWS profiles](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html#cli-configure-files-using-profiles), you can use the [`default`](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html#cli-configure-files-format-profile) profile instead of the `cw` profile created in the following steps. In that case, omit `--profile cw` from the commands.

> [!TIP]
>
> For production workloads, CoreWeave recommends [Workload Identity Federation](https://docs.coreweave.com/products/storage/object-storage/auth-access/workload-identity-federation/about.md) for automated, short-lived credentials instead of static access keys.

> [accordion] Configure CoreWeave credentials with static access keys
>
> 1. Create a `cw` profile:
>
>    ```bash title="Create a new profile" theme={"system"}
>    aws configure --profile cw
>    ```
>
> 2. When prompted, provide the following values:
>
>    * **AWS Access Key ID**: The [Access Key](https://docs.coreweave.com/products/storage/object-storage/auth-access/manage-access-keys/create-keys.md) ID of your CoreWeave AI Object Storage Access Key.
>    * **AWS Secret Access Key**: The Secret Key of your CoreWeave AI Object Storage Access Key.
>    * **Default region name** (Optional): To set a default region, see [CoreWeave Availability Zones](https://docs.coreweave.com/products/storage/object-storage/buckets/manage-buckets.md#availability-zones).
>    * **Default output format**: Use `json` for JSON output.
>
> 3. Set the default endpoint URL to the appropriate endpoint for your use case:
>
>    * The primary endpoint, `https://cwobject.com`, for use outside a CoreWeave cluster.
>    * The LOTA endpoint, `http://cwlota.com`, for use inside a CoreWeave cluster. The LOTA endpoint routes to the LOTA path for best performance.
>
>    ```bash title="Set the primary endpoint for local development" theme={"system"}
>    aws configure set endpoint_url https://cwobject.com --profile cw
>    ```
>
> 4. Set the S3 `addressing_style` to `virtual`:
>
>    ```bash title="Set virtual addressing style" theme={"system"}
>    aws configure set s3.addressing_style virtual --profile cw
>    ```
>
> To use this profile, pass `--profile cw` to your AWS CLI commands, or set `AWS_PROFILE=cw` in your environment.
>
> If you set `endpoint_url` and `s3.addressing_style` directly in your code (for example, in a Boto3 `Config` object), you can skip steps 3 and 4. The profile only needs the access key, secret key, and region.

> [accordion] Configure CoreWeave credentials with Workload Identity Federation (OIDC)
>
> If you've configured [Workload Identity Federation with OIDC](https://docs.coreweave.com/products/storage/object-storage/auth-access/workload-identity-federation/use-oidc-tokens.md), the AWS SDK automatically discovers temporary credentials. Set the following environment variables instead of configuring static access keys.
>
> Replace `[ORG-ID]` with your CoreWeave organization ID, `[PATH-TO-JWT-TOKEN-FILE]` with the path to your JWT token file, and `[AVAILABILITY-ZONE]` with your CoreWeave Availability Zone.
>
> ```bash title="Configure WIF OIDC credentials" theme={"system"}
> export AWS_CONTAINER_CREDENTIALS_FULL_URI=https://api.coreweave.com/v1/cwobject/temporary-credentials/oidc/[ORG-ID]
> export AWS_CONTAINER_AUTHORIZATION_TOKEN_FILE=[PATH-TO-JWT-TOKEN-FILE]
>
> aws configure set s3.addressing_style virtual
>
> export AWS_REGION="[AVAILABILITY-ZONE]"
> export AWS_ENDPOINT_URL_S3="https://cwobject.com"
> ```
>
> With WIF configured, your S3-compatible tools and Boto3 code automatically obtain and refresh temporary credentials without passing access keys explicitly.
>
> Requires `awscli >= 2.33.2` or `boto3 >= 1.42.5`. See [Use Workload Identity Federation with OIDC](https://docs.coreweave.com/products/storage/object-storage/auth-access/workload-identity-federation/use-oidc-tokens.md) for the full setup guide.

## Pre-stage a single object

To pre-stage an object, send a `HeadObject` request to the LOTA endpoint for the target bucket and key. Run these commands from within the same CKS cluster where your training or inference Pods run, so that data is cached on the correct set of Nodes. LOTA returns a response after writing the object into the cache.

Before completing and running these commands, make sure you have [configured your CoreWeave credentials](https://docs.coreweave.com/products/storage/object-storage/improving-performance/prestage-cache.md#configure-coreweave-credentials).

> [tab] AWS CLI
>
> To pre-stage a single object, replace the following placeholders:
>
> * `[BUCKET-NAME]` with the name of the bucket containing the object you want to pre-stage.
> * `[OBJECT-KEY]` with the key of the object you want to pre-stage, for example, `datasets/imagenet/shard-00001.tar`.
>
> ```bash title="Pre-stage a single object" theme={"system"}
> aws s3api head-object \
>   --bucket [BUCKET-NAME] \
>   --key [OBJECT-KEY] \
>   --endpoint-url http://cwlota.com \
>   --range "bytes=0-0"
> ```
>
> The command returns the object's metadata and triggers a cache fill:
>
> ```json title="Response" theme={"system"}
> {
>   "ContentLength": 524288000,
>   "ContentType": "application/x-tar",
>   "ETag": "\"a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6\"",
>   "LastModified": "2025-11-01T08:30:00+00:00",
>   "Metadata": {}
> }
> ```

> [tab] Boto3
>
> To pre-stage a single object, replace the following placeholders:
>
> * `[BUCKET-NAME]` with the name of the bucket containing the object you want to pre-stage.
> * `[OBJECT-KEY]` with the key of the object you want to pre-stage, for example, `datasets/imagenet/shard-00001.tar`.
>
> ```python title="Pre-stage a single object" theme={"system"}
> import boto3
> from botocore.client import Config
>
> s3 = boto3.client(
>     "s3",
>     endpoint_url="http://cwlota.com",
>     config=Config(
>         s3={"addressing_style": "virtual"},
>     ),
> )
>
> response = s3.head_object(
>     Bucket="[BUCKET-NAME]",
>     Key="[OBJECT-KEY]",
>     Range="bytes=0-0",
> )
>
> print(f"Object size: {response['ContentLength']:,} bytes")
> print(f"ETag: {response['ETag']}")
> ```

> [tab] s3cmd
>
> To pre-stage a single object, replace the following placeholders:
>
> * `[BUCKET-NAME]` with the name of the bucket containing the object you want to pre-stage.
> * `[OBJECT-KEY]` with the key of the object you want to pre-stage, for example, `datasets/imagenet/shard-00001.tar`.
>
> ```bash title="Pre-stage a single object" theme={"system"}
> s3cmd info s3://[BUCKET-NAME]/[OBJECT-KEY] \
>   --host=cwlota.com \
>   --host-bucket='%(bucket)s.cwlota.com' \
>   --no-ssl \
>   --add-header='Range: bytes=0-0'
> ```
>
> The `s3cmd info` command issues an HTTP `HEAD` request internally, which triggers the pre-stage cache fill.

## Pre-stage multiple objects in parallel

Parallelizing the pre-stage requests reduces the total time to warm a large dataset. For guidance on tuning connection pool size and concurrency for high-throughput workloads, see [Maximize parallelism](https://docs.coreweave.com/products/storage/object-storage/improving-performance/best-practices.md#maximize-parallelism).

> [!WARNING]
>
> Pre-staging a large number of objects transitions them all to the Hot pricing tier. Review the [Storage Pricing](https://www.coreweave.com/pricing) documentation to understand the cost implications before pre-staging at scale.

### Control the pre-stage request rate

A pre-stage pass over a large prefix can send requests faster than the storage backend accepts them. When that happens, pre-stage requests return timeouts and errors even though the backend itself is healthy. The risk is higher when the bucket is in another Availability Zone, because each request holds a connection open for longer.

Request rate, rather than thread count, controls this. Set an explicit ceiling on requests per second and lower it if requests start failing. Keep concurrency bounded as well, so that listing a large prefix does not launch one request per object at the same time. Retry failed requests with exponential backoff and jitter rather than immediately, so that retries do not add to the load that caused the failure.

The Boto3 example sets a requests-per-second ceiling directly, through the `REQUESTS_PER_SECOND` value. The AWS CLI and s3cmd examples have no rate limiter, so bound concurrency in those examples instead and lower it if requests start failing. The AWS CLI and Boto3 examples also retry with backoff and jitter.

Before completing and running these commands, make sure you have [configured your CoreWeave credentials](https://docs.coreweave.com/products/storage/object-storage/improving-performance/prestage-cache.md#configure-coreweave-credentials).

> [tab] AWS CLI
>
> To pre-stage all objects under a prefix, replace the following placeholders:
>
> * `[BUCKET-NAME]` with the name of the bucket containing the objects you want to pre-stage.
> * `[PREFIX]` with the prefix of the objects you want to pre-stage, for example, `datasets/imagenet/`.
> * `[CONCURRENCY]` with the number of pre-stage requests to run at once, for example, `16`. Lower this value if requests start failing.
>
> `AWS_RETRY_MODE=standard` retries failed requests with exponential backoff and jitter, and `AWS_MAX_ATTEMPTS` sets how many attempts each request gets. `xargs -P` bounds concurrency, so the number of requests in flight does not grow with the size of the prefix. The `tr` and `xargs -0` pair passes each key as a single argument, so keys that contain spaces or quotes are handled correctly.
>
> ```bash title="Pre-stage all objects under a prefix" theme={"system"}
> export AWS_RETRY_MODE=standard
> export AWS_MAX_ATTEMPTS=5
>
> aws s3api list-objects-v2 \
>   --bucket [BUCKET-NAME] \
>   --prefix [PREFIX] \
>   --endpoint-url http://cwlota.com \
>   --query 'Contents[].Key' \
>   --output text | tr '\t\n' '\0\0' | \
> xargs -0 -P [CONCURRENCY] -I {} \
>   aws s3api head-object \
>     --bucket [BUCKET-NAME] \
>     --key {} \
>     --endpoint-url http://cwlota.com \
>     --range "bytes=0-0" > /dev/null
>
> echo "Pre-staging complete."
> ```

> [tab] Boto3
>
> To pre-stage all objects under a prefix, replace the following placeholders:
>
> * `[BUCKET-NAME]` with the name of the bucket containing the objects you want to pre-stage.
> * `[PREFIX]` with the prefix of the objects you want to pre-stage, for example, `datasets/imagenet/`.
>
> Set `MAX_WORKERS` to the number of pre-stage requests to run at once and `REQUESTS_PER_SECOND` to the rate ceiling for the pass. Lower `REQUESTS_PER_SECOND` first if requests start failing. The `retries` configuration retries failed requests with exponential backoff and jitter.
>
> ```python title="Pre-stage all objects under a prefix" theme={"system"}
> import boto3
> import threading
> import time
> from botocore.client import Config
> from concurrent.futures import ThreadPoolExecutor, as_completed
>
> BUCKET = "[BUCKET-NAME]"
> PREFIX = "[PREFIX]"
> MAX_WORKERS = 16
> REQUESTS_PER_SECOND = 100
>
> s3 = boto3.client(
>     "s3",
>     endpoint_url="http://cwlota.com",
>     config=Config(
>         max_pool_connections=MAX_WORKERS,
>         retries={"max_attempts": 5, "mode": "standard"},
>         s3={"addressing_style": "virtual"},
>     ),
> )
>
> _rate_lock = threading.Lock()
> _next_slot = time.monotonic()
>
> def throttle():
>     """Hold the pre-stage pass at REQUESTS_PER_SECOND across all threads."""
>     global _next_slot
>     interval = 1.0 / REQUESTS_PER_SECOND
>     with _rate_lock:
>         now = time.monotonic()
>         wait = max(0.0, _next_slot - now)
>         _next_slot = max(now, _next_slot) + interval
>     if wait:
>         time.sleep(wait)
>
> def prestage_object(key):
>     """Issue a HeadObject call (range 0-0) to pre-stage a single object."""
>     throttle()
>     s3.head_object(
>         Bucket=BUCKET,
>         Key=key,
>         Range="bytes=0-0",
>     )
>     return key
>
> paginator = s3.get_paginator("list_objects_v2")
> keys = []
> for page in paginator.paginate(Bucket=BUCKET, Prefix=PREFIX):
>     for obj in page.get("Contents", []):
>         keys.append(obj["Key"])
>
> print(f"Pre-staging {len(keys)} objects...")
>
> succeeded = 0
> failed = 0
>
> with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
>     futures = {executor.submit(prestage_object, k): k for k in keys}
>     for future in as_completed(futures):
>         key = futures[future]
>         try:
>             future.result()
>             succeeded += 1
>         except Exception as exc:
>             failed += 1
>             print(f"  Failed to pre-stage {key}: {exc}")
>         if (succeeded + failed) % 100 == 0:
>             print(f"  {succeeded + failed}/{len(keys)} objects processed")
>
> print(f"Done. {succeeded} succeeded, {failed} failed out of {len(keys)} objects.")
> ```

> [tab] s3cmd
>
> To pre-stage all objects under a prefix, replace the following placeholders:
>
> * `[BUCKET-NAME]` with the name of the bucket containing the objects you want to pre-stage.
> * `[PREFIX]` with the prefix of the objects you want to pre-stage, for example, `datasets/imagenet/`.
> * `[CONCURRENCY]` with the number of pre-stage requests to run at once, for example, `16`. Lower this value if requests start failing.
>
> `xargs -P` bounds concurrency, so the number of requests in flight does not grow with the size of the prefix. The `grep` filters skip sub-prefix entries and keep each full object path intact, and `xargs -0` passes each path as a single argument, so keys that contain spaces or quotes are handled correctly. The `s3cmd info` command has no built-in retry for this workflow, so for large cross-region passes prefer the AWS CLI or Boto3 examples, which retry with backoff.
>
> ```bash title="Pre-stage all objects under a prefix" theme={"system"}
> s3cmd ls s3://[BUCKET-NAME]/[PREFIX] \
>   --host=cwlota.com \
>   --host-bucket='%(bucket)s.cwlota.com' \
>   --no-ssl | \
> grep -v ' DIR ' | grep -o 's3://.*' | tr '\n' '\0' | \
> xargs -0 -P [CONCURRENCY] -I {} \
>   s3cmd info {} \
>     --host=cwlota.com \
>     --host-bucket='%(bucket)s.cwlota.com' \
>     --no-ssl \
>     --add-header='Range: bytes=0-0'
>
> echo "Pre-staging complete."
> ```

## Pre-stage before your training job starts

Use a Kubernetes Job as an initial step in your training pipeline. The Job pre-stages all training data, then your training pods start with a fully warmed cache.

Replace `[BUCKET-NAME]` with the name of the bucket containing your training data, `[PREFIX]` with the object prefix to pre-stage (for example, `datasets/imagenet/`), and `[CONCURRENCY]` with the number of pre-stage requests to run at once (for example, `16`). The Job reads credentials from a Kubernetes Secret named `storage-credentials`.

```yaml title="job-prestage-training-data.yaml" theme={"system"}
apiVersion: batch/v1
kind: Job
metadata:
  name: prestage-training-data
spec:
  template:
    spec:
      containers:
        - name: prestage
          image: amazon/aws-cli:latest
          command:
            - "/bin/bash"
            - "-c"
            - |
              set -eo pipefail
              aws s3api list-objects-v2 \
                --bucket [BUCKET-NAME] \
                --prefix [PREFIX] \
                --endpoint-url http://cwlota.com \
                --query 'Contents[].Key' \
                --output text | tr '\t\n' '\0\0' | \
              xargs -0 -P [CONCURRENCY] -I {} \
                aws s3api head-object \
                  --bucket [BUCKET-NAME] \
                  --key {} \
                  --endpoint-url http://cwlota.com \
                  --range 'bytes=0-0' > /dev/null
              echo "Pre-staging complete."
          env:
            - name: AWS_RETRY_MODE
              value: "standard"
            - name: AWS_MAX_ATTEMPTS
              value: "5"
            - name: AWS_ACCESS_KEY_ID
              valueFrom:
                secretKeyRef:
                  name: storage-credentials
                  key: access-key-id
            - name: AWS_SECRET_ACCESS_KEY
              valueFrom:
                secretKeyRef:
                  name: storage-credentials
                  key: secret-access-key
      restartPolicy: Never
  backoffLimit: 3
```

> [!NOTE]
>
> Schedule the pre-stage Job to run before your training pods launch. In an Argo Workflow or a Kubernetes-native pipeline, add a dependency so the training step waits for the pre-stage Job to succeed. Pre-stage data immediately before the compute step that needs it to balance warm cache benefits against cache capacity.

## Related resources

* [About LOTA (Local Object Transport Accelerator)](https://docs.coreweave.com/products/storage/object-storage/improving-performance/about-lota.md)
* [Conditional writes](https://docs.coreweave.com/products/storage/object-storage/reference/object-storage-s3.md#conditional-writes): use the ETag returned by `HeadObject` with `If-Match` to perform atomic compare-and-swap updates
* [Get Started with AI Object Storage](https://docs.coreweave.com/products/storage/object-storage/get-started-caios.md)
* [Manage Buckets](https://docs.coreweave.com/products/storage/object-storage/buckets/manage-buckets.md)
* [Storage Pricing](https://www.coreweave.com/pricing)
* [CAIOS LOTA dashboard](https://docs.coreweave.com/observability/managed-grafana/storage/caios-lota.md)
