# Performance best practices

Source: https://docs.coreweave.com/products/storage/object-storage/improving-performance/best-practices

# Performance best practices

> Best practices for maximizing read performance and using the LOTA (Local Object Transport Accelerator) cache effectively

Maximizing read performance with CoreWeave AI Object Storage is critical for keeping your GPUs busy. This guide is for engineers tuning training, inference, or data-pipeline workloads against AI Object Storage. It explains how to maximize read performance and how to use the [LOTA (Local Object Transport Accelerator)](https://docs.coreweave.com/products/storage/object-storage/improving-performance/about-lota.md) cache effectively.

Object storage has two types of performance bottlenecks: metadata path issues and data path issues. Identifying which category your bottleneck falls into is the first step toward resolving it. The following sections describe techniques for each category, then explain how to get the most out of the LOTA cache.

## Establish a latency baseline

CoreWeave AI Object Storage does not publish a fixed per-operation latency target for S3 operations such as `PutObject`, `GetObject`, `DeleteObject`, and `DeleteObjects`. To establish a baseline for your object sizes and request patterns, [benchmark with Warp](https://docs.coreweave.com/products/storage/object-storage/improving-performance/benchmarking-warp.md). To observe live request and response duration, use the [CAIOS Usage](https://docs.coreweave.com/observability/managed-grafana/storage/caios-usage.md#usage-metrics) dashboard.

## Metadata path optimization

Each AI Object Storage request requires a metadata lookup to authenticate the request and obtain the location of the data. If the metadata lookup is slow, the request response is slow. Optimizing the metadata path improves response times.

For metadata path optimization, you can use the following techniques:

* Avoid key-range hot-spotting.
* Avoid small object overhead.

### Avoid key-range hot-spotting

Hot-spotting occurs when many concurrent requests target the same narrow range of object keys (the name given to an object in a bucket). Sequential object keys, such as `sample_000001`, `sample_000002`, are a common cause. Object storage systems partition data by key range, and concentrated access patterns can overload individual partitions.

For objects that every client needs (for example, shared index files), replicate them under different prefixes and distribute reads across the copies.

#### Use hashed prefixes

Rather than organizing objects with sequential or predictable key names, prepend a hash to distribute keys evenly across partitions.

```python title="hashing-prefixes.py" theme={"system"}
import hashlib

def hashed_key(original_key: str) -> str:
    """Prepend a short hash to distribute keys across partitions."""
    prefix = hashlib.md5(original_key.encode()).hexdigest()[:6]
    return f"{prefix}/{original_key}"

# Instead of:
#   dataset/train/sample_000001.bin
#   dataset/train/sample_000002.bin

# Use:
#   a3f1b2/dataset/train/sample_000001.bin
#   7c9e4d/dataset/train/sample_000002.bin
```

Hashing the prefix does not help with writes or checkpointing to a bucket, but it does help for later loading. When multiple workers write to the same checkpoint key, use [conditional writes](https://docs.coreweave.com/products/storage/object-storage/reference/object-storage-s3.md#conditional-writes) (`If-None-Match: *`) to guarantee that only one write succeeds.

#### Use exponential back-off

In rarer cases, many clients may hit the same small key range simultaneously. For example, multiple training jobs may read the same metadata index at startup. Hashing alone does not prevent this pattern. Retry with exponential back-off, since transient overloads often resolve when clients stagger their retries.

A `503 Slow Down` response means the service is briefly throttling your requests, typically because a single key-range partition is momentarily overloaded. Retrying immediately only adds load to a partition that is already saturated. Instead, wait progressively longer between attempts (exponential back-off) and add random **jitter** so that many clients reading the same key range don't retry in lockstep and recreate the overload. This is the standard retry strategy for S3-compatible object storage, and it applies to reads against CoreWeave AI Object Storage whether you use the LOTA endpoint (`http://cwlota.com`) or the primary endpoint (`https://cwobject.com`).

Before completing and running these Boto3 code examples, make sure you have configured your CoreWeave credentials.

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

In the following examples, replace `[BUCKET-NAME]` with the name of your bucket.

Boto3 can apply exponential back-off for you through its built-in retry modes, so `503` responses are retried automatically without any extra code. The **standard** retry mode retries transient `500`, `502`, `503`, and `504` responses using exponential back-off with jitter, and is the recommended choice for most workloads. Standard mode defaults to only three total attempts, so raise `max_attempts` for data-intensive workloads that may encounter sustained throttling. Configure it on the client:

```python title="boto3-standard-retries.py" theme={"system"}
import boto3
from botocore.client import Config

s3 = boto3.client(
    "s3",
    endpoint_url="http://cwlota.com",
    config=Config(
        retries={"max_attempts": 10, "mode": "standard"},
        s3={"addressing_style": "virtual"},
    ),
)

# 503 (Slow Down) responses are now retried automatically with
# exponential back-off and jitter.
response = s3.get_object(Bucket="[BUCKET-NAME]", Key="dataset/index.json")
data = response["Body"].read()
# Process data...
```

You can also enable the same behavior with environment variables, which apply to any Boto3 or AWS SDK process without changing code:

```bash title="retry-env-vars.sh" theme={"system"}
export AWS_RETRY_MODE=standard
export AWS_MAX_ATTEMPTS=10
```

If you need explicit control over the retry behavior, such as custom retry counts, logging, or metrics, implement the back-off loop yourself. The following example retries only on `503`, grows the wait window exponentially, and applies full jitter by sleeping for a random point within that window. The attempt count and delay cap are tuned for data-intensive workloads, where high concurrency makes sustained throttling more likely: ten attempts let the back-off window grow into the `MAX_DELAY` cap so the client can ride out longer throttling episodes rather than failing early.

```python title="exponential-backoff.py" theme={"system"}
import random
import time

import boto3
from botocore.client import Config
from botocore.exceptions import ClientError

s3 = boto3.client(
    "s3",
    endpoint_url="http://cwlota.com",
    config=Config(
        # Disable the SDK's built-in retries so this loop is the single source
        # of back-off. By default Boto3 also retries 503 internally (legacy
        # mode, 5 attempts), which would stack on top of the retries below.
        retries={"max_attempts": 1, "mode": "standard"},
        s3={"addressing_style": "virtual"},
    ),
)

MAX_RETRIES = 10    # Total attempts before giving up
BASE_DELAY = 0.5    # Initial back-off in seconds
MAX_DELAY = 30.0    # Cap on any single back-off interval


def get_object_with_backoff(bucket: str, key: str) -> bytes:
    """GET an object, retrying 503 (Slow Down) responses with
    exponential back-off and full jitter."""
    for attempt in range(MAX_RETRIES):
        try:
            response = s3.get_object(Bucket=bucket, Key=key)
            return response["Body"].read()
        except ClientError as error:
            status = error.response.get("ResponseMetadata", {}).get("HTTPStatusCode")
            # Only back off on 503. Re-raise anything else (403, 404, etc.),
            # and give up once the final attempt is exhausted.
            if status != 503 or attempt == MAX_RETRIES - 1:
                raise
            # Exponential window: BASE_DELAY * 2 ** attempt, capped at MAX_DELAY.
            # Full jitter (a random point inside the window) staggers retries so
            # clients don't synchronize and re-overload the same partition.
            window = min(MAX_DELAY, BASE_DELAY * (2 ** attempt))
            time.sleep(random.uniform(0, window))


data = get_object_with_backoff("[BUCKET-NAME]", "dataset/index.json")
# Process data...
```

### Avoid small object overhead

As object size decreases, the per-request metadata lookup becomes a larger proportion of total latency. The same problem arises when you issue many small range reads against a large object. In both cases, the overhead of the metadata path dominates and throttles throughput.

Keep read sizes large. Aim for at least 15 MB per request. Performance begins to degrade noticeably below 1 MB. If your data is organized into many small files, consider the following strategies:

* Consolidate small files into larger archives. Formats like TAR, WebDataset, or TFRecord let you pack thousands of small samples into multi-megabyte or multi-gigabyte objects that can be read efficiently.
* Use large range reads. When reading portions of a large object, request contiguous ranges of at least 15 MB rather than many small, scattered offsets.

## Data path optimization

Each request to object storage requires writing or retrieving data from the backend storage service. Optimizing the data path improves throughput and latency.

For data path optimization, you can use the following techniques:

* Minimize network contention with LOTA.
* Maximize parallelism.

### Minimize network contention with LOTA

LOTA (Local Object Transport Accelerator) is a caching proxy installed on every Node in your CoreWeave Kubernetes Service (CKS) cluster. When you use the LOTA endpoint (`http://cwlota.com`) instead of the primary endpoint (`https://cwobject.com`), reads come from local NVMe SSDs attached to Nodes in the same cluster as your workload. This eliminates network round-trips to the storage backend. The cache is shared across all Nodes in the cluster, scales with cluster size, uses LRU eviction, and maintains strong consistency.

LOTA also supports cross-region reads. When a workload reads from a bucket whose home [Availability Zone](https://docs.coreweave.com/platform/regions/about-regions-and-azs.md) is elsewhere, LOTA fetches the object from that Availability Zone's repository and caches it on the local Nodes. Later reads come from the local cache at full speed, so workloads in any Availability Zone can access a single global dataset with local-like performance.

Switching to LOTA requires only an endpoint change:

| Scenario | Endpoint | Notes |
| - | - | - |
| Inside your CoreWeave cluster | `http://cwlota.com` | LOTA caches `GET` requests only. Write operations are proxied to the storage backend. |
| Outside CoreWeave | `https://cwobject.com` | No local caching. All requests go directly to the storage backend. |

See [Attaching endpoints](https://docs.coreweave.com/products/storage/object-storage/using-object-storage/configure-endpoints.md) for setup details.

### Maximize parallelism

AI Object Storage is designed for massively parallel access. Most high-performance applications already parallelize their reads, but it's worth verifying that your client uses the maximum concurrency available.

Internal [benchmarking with Warp](https://docs.coreweave.com/products/storage/object-storage/improving-performance/benchmarking-warp.md) shows that 9,000 concurrent operations across a 30-node cluster (300 per node) achieves high throughput on AI Object Storage. The optimal concurrency varies by workload. Start at 300 per node and adjust based on whether throughput is still climbing or declining.

Set `max_pool_connections` in the `Config` to match your desired concurrency level or higher. The default (10) is frequently too low for high-throughput workloads.

The following partial example shows how to configure multi-threaded GETs with Boto3 and `concurrent.futures`.

Before completing and running this Boto3 code example, make sure you have configured your CoreWeave credentials.

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

```python title="maximizing-parallelism.py" highlight={9, 20} theme={"system"}
import boto3
from botocore.client import Config
from concurrent.futures import ThreadPoolExecutor, as_completed

s3 = boto3.client(
    's3',
    endpoint_url='http://cwlota.com',
    config=Config(
        max_pool_connections=50, # Adjust this value to match your desired concurrency level or higher
        s3={'addressing_style': 'virtual'}
    )
)

object_keys = [f"dataset/shard-{i:05d}.tar" for i in range(1000)]

def download_object(key):
    response = s3.get_object(Bucket='[BUCKET-NAME]', Key=key)
    return response['Body'].read()

with ThreadPoolExecutor(max_workers=50) as executor:
    futures = {executor.submit(download_object, key): key for key in object_keys}
    for future in as_completed(futures):
        data = future.result()
        # Process data
```

## Optimize LOTA cache performance

When you use the LOTA endpoint, requests get better performance because LOTA improves network efficiency and serves data from high-performance storage devices. The following sections describe techniques that help you get the most out of LOTA caching:

* Pre-stage data in the cache.
* Use multipart uploads for large objects.
* Contact CoreWeave for large dataset caching.
* Handle cross-region writes.

### Pre-stage data in the cache

LOTA caches data on first read, but you can proactively warm the cache before a production workload starts by pre-staging objects with a HeadObject call. This eliminates cold-start latency on the first read. See [Pre-stage the LOTA cache](https://docs.coreweave.com/products/storage/object-storage/improving-performance/prestage-cache.md) for instructions.

Pre-staging matters most when your workload runs outside the bucket's home Availability Zone, because automatic pre-staging covers only clusters in that same Availability Zone. See [Pre-stage for cross-region workloads](https://docs.coreweave.com/products/storage/object-storage/improving-performance/prestage-cache.md#pre-stage-for-cross-region-workloads).

### Use multipart uploads for large objects

Uploading large objects using the [S3 multipart API](https://docs.coreweave.com/products/storage/object-storage/reference/object-storage-s3.md#s3createmultipartupload) distributes data across LOTA partitions, optimizing performance. When you use multipart upload, AI Object Storage preserves the parts, which lets LOTA spread the data across Nodes. Conversely, objects uploaded with a single `PutObject` call reside on one Node, which can create a bottleneck for large objects.

LOTA automatically invalidates cached parts when they're updated, so no stale data reaches clients during iterative uploads of the same object.

Use a minimum part size of 50 MB to reduce HTTP request overhead while still allowing efficient distribution. LOTA only caches objects larger than 4 MB. Smaller objects bypass the cache.

### Contact CoreWeave for large dataset caching

If you have a large dataset and want all of it resident in the LOTA cache, contact CoreWeave support. LOTA has ample cache capacity available and can likely accommodate your entire dataset. The CoreWeave team ensures that your organization has the proper cache allocation and settings configured.

### Handle cross-region writes

AI Object Storage supports cross-region writes, but LOTA caches only reads. If your workload writes across regions, ensure that it tolerates the higher latencies associated with sending data between regions.

## Data transfer optimization

When moving existing data into AI Object Storage, the transfer tool you choose affects throughput. For copying data from PVC to AI Object Storage, we recommend using the [CoreWeave fork of s5cmd](https://github.com/coreweave/s5cmd).
