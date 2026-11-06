# Benchmarking with Warp

Source: https://docs.coreweave.com/products/storage/object-storage/improving-performance/benchmarking-warp

# Benchmarking with Warp

> How to use Warp to benchmark CoreWeave AI Object Storage performance

[Warp](https://github.com/minio/warp) is an open source S3-compatible benchmarking tool that provides per-request latency percentiles and throughput metrics. It works with CoreWeave AI Object Storage and supports several benchmark types, including `GET`, `PUT`, `DELETE`, `LIST`, `STAT`, and `mixed` workloads.

This guide shows you how to deploy Warp inside a CKS cluster and run read, write, mixed, and multipart benchmarks against CoreWeave AI Object Storage. Use these benchmarks to measure storage performance for your workloads, compare LOTA cache performance against the primary endpoint, and validate concurrency and object-size tuning before running production data pipelines.

CoreWeave does not publish a fixed per-operation latency target. Treat your Warp results as the expected baseline for your object sizes and request patterns.

## Prerequisites

This guide assumes that you already have the following prerequisites in place:

* A [CKS cluster](https://docs.coreweave.com/products/cks/clusters/create.md)
* A [Node Pool](https://docs.coreweave.com/products/cks/nodes/create.md) with a Node to run the benchmarks on
* [`kubectl`](https://docs.coreweave.com/products/cks/auth-access/managed-auth/kubeconfig) installed and configured to access your cluster
* A CoreWeave AI Object Storage [access key and secret key](https://docs.coreweave.com/products/storage/object-storage/auth-access/manage-access-keys/create-keys.md)
* The necessary permissions to create an [AI Object Storage bucket](https://docs.coreweave.com/products/storage/object-storage/buckets/create-bucket.md)

### Create a dedicated benchmark bucket

> [!WARNING]
>
> Warp completely wipes the benchmark bucket before and after each run. Use a dedicated bucket and **never point Warp at a bucket containing production data**.

Create a dedicated bucket for benchmarking [using the Cloud Console](https://console.coreweave.com/object-storage/buckets). This guide names the bucket `warp-benchmark-bucket` and uses the `US-EAST-04A` availability zone.

Alternatively, you can create a dedicated bucket using [S3-compatible clients](https://docs.coreweave.com/products/storage/object-storage/buckets/create-bucket.md#create-a-bucket-with-cli-clients). For example, you can create a bucket named `warp-benchmark-bucket` in the `US-EAST-04A` availability zone using the following command, which works only if you've already [created a CoreWeave-specific configuration](https://docs.coreweave.com/products/storage/object-storage/using-object-storage/configure-endpoints.md#full-configuration-examples):

```bash theme={"system"}
aws s3api create-bucket \
  --bucket warp-benchmark-bucket \
  --region US-EAST-04A \
  --create-bucket-configuration LocationConstraint=US-EAST-04A
```

If you use a different bucket name, make sure to use a name that identifies the bucket as a benchmark bucket, and prepend it with `warp-`. The rest of this guide uses the following bucket configuration values:

* Bucket name: `warp-benchmark-bucket`
* Availability zone: `US-EAST-04A`

### Deploy Warp on a Node

Warp must run from inside your CKS cluster to produce meaningful results. Benchmarking from an external network measures network latency rather than storage performance, and the LOTA endpoint (`http://cwlota.com`) is only accessible from a CoreWeave cluster.

Deploy Warp as a Pod using the official [Warp container image](https://github.com/minio/warp/releases). Warp does not use GPU resources, so no GPU resource request or Node affinity is needed. LOTA is available on all Nodes in the cluster. For details on targeting specific Node types, see [Target specific GPUs or CPUs](https://docs.coreweave.com/products/cks/nodes/manage.md#target-specific-gpus-or-cpus).

```yaml title="warp-benchmark.yaml" theme={"system"}
apiVersion: v1
kind: Pod
metadata:
  name: warp-benchmark
spec:
  containers:
  - name: warp
    image: quay.io/minio/aistor/warp:latest
    command: ["sleep", "infinity"]
```

1. Apply the manifest:

   ```bash theme={"system"}
   kubectl apply -f warp-benchmark.yaml
   ```

2. Wait for the Pod to be running:

   ```bash theme={"system"}
   kubectl get pod warp-benchmark -w
   ```

3. Open a shell inside the Pod:

   ```bash theme={"system"}
   kubectl exec -it warp-benchmark -- sh
   ```

4. Verify that Warp is available:

   ```bash theme={"system"}
   /warp version
   ```

### Set environment variables

In your Pod, set your CoreWeave AI Object Storage credentials, endpoint, and region using environment variables for convenience:

```bash title="Set environment variables" theme={"system"}
export WARP_HOST="cwlota.com"
export WARP_ACCESS_KEY="[ACCESS-KEY-ID]"
export WARP_SECRET_KEY="[SECRET-ACCESS-KEY]"
export WARP_REGION="US-EAST-04A"
```

## Measure read throughput with GET

> [!WARNING]
>
> Warp completely wipes the benchmark bucket before and after each run. Use a dedicated bucket (such as `warp-benchmark-bucket`) and never point Warp at a bucket containing production data.

Read throughput is the key benchmark for data loading. The following configuration runs a `get` benchmark against the LOTA endpoint with recommended starting parameters:

```yaml title="warp-test-lota-get.yaml" theme={"system"}
warp:
  api: v1
  benchmark: get
  remote:
    bucket: warp-benchmark-bucket
    region: [REGION]
    access-key: [ACCESS-KEY-ID]
    secret-key: [SECRET-ACCESS-KEY]
    host:
      - cwlota.com
    tls: false
    lookup: host
  params:
    duration: 5m
    concurrent: 300
    obj:
      size: 15MiB
    autoterm:
      enabled: true
```

Create and run this configuration in your Pod:

1. Create the benchmark configuration file:

   ```bash title="Create GET benchmark configuration file" theme={"system"}
   cat <<EOF > warp-test-lota-get.yaml
   warp:
     api: v1
     benchmark: get
     remote:
       bucket: warp-benchmark-bucket
       region: $WARP_REGION
       access-key: $WARP_ACCESS_KEY
       secret-key: $WARP_SECRET_KEY
       host:
         - cwlota.com
       tls: false
       lookup: host
     params:
       duration: 5m
       concurrent: 300
       obj:
         size: 15MiB
       autoterm:
         enabled: true
   EOF
   ```

2. Run the benchmark using the following command in your Pod:

   ```bash title="Run GET benchmark" theme={"system"}
   /warp run warp-test-lota-get.yaml
   ```

### Recommended benchmark parameters

The following table lists the recommended benchmark parameters for read throughput. You can adjust them as needed to optimize performance for your workload.

| Parameter | Value | Description |
| - | - | - |
| Concurrency Level | 300 | The number of parallel download operations to run. Start with 300 and adjust upward or downward. If you see throughput still climbing at 300, try increasing to 500 or more. If you see declining or unexpectedly low throughput, try decreasing the concurrency. |
| Object Size | 15 MiB | The size of the objects to use. Start with 15 MiB to stay above the threshold where metadata overhead becomes significant. |
| Number of Objects | 2,500 | The number of objects to use. Start with 2,500 to provide a pool for random selection. For most workloads, this is a good starting point. |
| Duration | 5 minutes | The duration of the benchmark. Start with 5 minutes to capture stable, representative throughput numbers. For most workloads, this is a good starting point. |
| Range Size | 1 MB | The size of the range to read. Start with 1 MB to avoid small-read overhead. Small reads are still served from the cache as long as the object size is greater than 4 MB. Objects smaller than 4 MB are not cached. |
| Autoterm | true | Automatically stop the benchmark when throughput stabilizes, preventing noisy results from incomplete warm-up periods. |

## Measure write throughput with PUT

Write throughput indicates how quickly you can load data into AI Object Storage, which is relevant for workloads such as checkpointing, dataset preparation, and log ingestion. The following configuration runs a `put` benchmark with recommended starting parameters:

```yaml title="warp-test-lota-put.yaml" theme={"system"}
warp:
  api: v1
  benchmark: put
  remote:
    bucket: warp-benchmark-bucket
    region: [REGION]
    access-key: [ACCESS-KEY-ID]
    secret-key: [SECRET-ACCESS-KEY]
    host:
      - cwlota.com
    tls: false
    lookup: host
  params:
    duration: 5m
    concurrent: 300
    obj:
      size: 15MiB
    autoterm:
      enabled: true
```

Create and run this configuration in your Pod:

1. Create the benchmark configuration file:

   ```bash title="Create PUT benchmark configuration file" theme={"system"}
   cat <<EOF > warp-test-lota-put.yaml
   warp:
     api: v1
     benchmark: put
     remote:
       bucket: warp-benchmark-bucket
       region: $WARP_REGION
       access-key: $WARP_ACCESS_KEY
       secret-key: $WARP_SECRET_KEY
       host:
         - cwlota.com
       tls: false
       lookup: host
     params:
       duration: 5m
       concurrent: 300
       obj:
         size: 15MiB
       autoterm:
         enabled: true
   EOF
   ```

2. Run the benchmark using the following command in your Pod:

   ```bash title="Run PUT benchmark" theme={"system"}
   /warp run warp-test-lota-put.yaml
   ```

## Measure mixed workload throughput

The [`mixed` command](https://github.com/minio/warp?tab=readme-ov-file#mixed) simulates a realistic workload with a configurable mix of `GET`, `PUT`, `STAT`, and `DELETE` operations.

The following configuration runs a `mixed` benchmark with the default operation distribution:

```yaml title="warp-test-lota-mixed.yaml" theme={"system"}
warp:
  api: v1
  benchmark: mixed
  remote:
    bucket: warp-benchmark-bucket
    region: [REGION]
    access-key: [ACCESS-KEY-ID]
    secret-key: [SECRET-ACCESS-KEY]
    host:
      - cwlota.com
    tls: false
    lookup: host
  params:
    duration: 5m
    concurrent: 300
    objects: 2500
    obj:
      size: 15MiB
    autoterm:
      enabled: true
```

Create and run this configuration in your Pod:

1. Create the benchmark configuration file:

   ```bash title="Create mixed workload benchmark configuration file" theme={"system"}
   cat <<EOF > warp-test-lota-mixed.yaml
   warp:
     api: v1
     benchmark: mixed
     remote:
       bucket: warp-benchmark-bucket
       region: $WARP_REGION
       access-key: $WARP_ACCESS_KEY
       secret-key: $WARP_SECRET_KEY
       host:
         - cwlota.com
       tls: false
       lookup: host
     params:
       duration: 5m
       concurrent: 300
       objects: 2500
       obj:
         size: 15MiB
       autoterm:
         enabled: true
   EOF
   ```

2. Run the benchmark using the following command in your Pod:

   ```bash title="Run mixed workload benchmark" theme={"system"}
   /warp run warp-test-lota-mixed.yaml
   ```

### Configure the operation distribution

By default, the `mixed` benchmark uses the following operation distribution: 45% `GET`, 15% `PUT`, 30% `STAT`, 10% `DELETE`. To customize the distribution, set the `distribution` key in your YAML configuration file. The following partial example shows where to add it:

```yaml title="Mixed workload benchmark configuration" highlight={12-16} theme={"system"}
warp:
  api: v1
  # ...
  params:
    duration: 5m
    concurrent: 300
    objects: 2500
    obj:
      size: 15MiB
    autoterm:
      enabled: true
    distribution:
      get: 45.0
      stat: 30.0
      put: 15.0
      delete: 10.0 # Must be same or lower than 'put'.
```

See the [example Mixed Workload benchmark configuration file](https://github.com/minio/warp/blob/master/yml-samples/mixed.yml) for a complete example.

## Measure multipart upload throughput

Multipart uploads split a single object into parts that are uploaded in parallel, which is useful for large objects such as model checkpoints or dataset archives. The following configuration runs a `multipart-put` benchmark with recommended starting parameters:

```yaml title="warp-test-lota-multipart-put.yaml" theme={"system"}
warp:
  api: v1
  benchmark: multipart-put
  remote:
    bucket: warp-benchmark-bucket
    region: [REGION]
    access-key: [ACCESS-KEY-ID]
    secret-key: [SECRET-ACCESS-KEY]
    host:
      - cwlota.com
    tls: false
    lookup: host
  params:
    duration: 5m
    concurrent: 10
    obj:
      size: 15MiB
      parts: 100
      part-size: 50MiB
      part-concurrent: 20
    autoterm:
      enabled: true
```

Create and run this configuration in your Pod:

1. Create the benchmark configuration file:

   ```bash title="Create multipart upload benchmark configuration file" theme={"system"}
   cat <<EOF > warp-test-lota-multipart-put.yaml
   warp:
     api: v1
     benchmark: multipart-put
     remote:
       bucket: warp-benchmark-bucket
       region: $WARP_REGION
       access-key: $WARP_ACCESS_KEY
       secret-key: $WARP_SECRET_KEY
       host:
         - cwlota.com
       tls: false
       lookup: host
     params:
       duration: 5m
       concurrent: 10
       obj:
         size: 15MiB
         parts: 100
         part-size: 50MiB
         part-concurrent: 20
       autoterm:
         enabled: true
   EOF
   ```

2. Run the benchmark using the following command in your Pod:

   ```bash title="Run multipart upload benchmark" theme={"system"}
   /warp run warp-test-lota-multipart-put.yaml
   ```

## Interpret Warp output

Warp reports include several important metrics:

```text title="Warp output" theme={"system"}
Operation: GET (25000). Ran 2m0s. Size: 15 MiB. Concurrency: 300.
 * Average: 4.2 GiB/s, 286.72 obj/s

Throughput, split into 120 x 1s:
 * Fastest: 4.8 GiB/s, 327.68 obj/s
 * 50% Median: 4.2 GiB/s, 286.72 obj/s
 * Slowest: 3.1 GiB/s, 211.89 obj/s

Requests:
 * Avg: 42ms, 50%: 38ms, 90%: 67ms, 99%: 125ms
 * Fastest: 8ms, Slowest: 312ms, StdDev: 24ms
```

For each run, focus on these values when evaluating performance:

* **Average and median throughput (GiB/s):** Your sustained read or write rate. The median is more representative than the average when there are outliers.
* **p50 / p90 / p99 request latency:** These percentiles show how consistent performance is. A large gap between p50 and p99 may indicate contention or cache misses.
* **Slowest 1-second window:** Represents worst-case throughput. If this is much lower than the median, investigate potential sources of variability.

Storage and network performance can vary. Run each benchmark configuration at least three times and report the median of the results to account for variability.

### Compare LOTA and primary endpoint performance

Run the same benchmark against both `cwlota.com` and `cwobject.com` to quantify the performance benefit of LOTA caching. When benchmarking against `cwobject.com`, set `tls: true` in the `remote` section of your YAML configuration because the primary endpoint requires HTTPS. The LOTA endpoint uses HTTP from within the cluster, so `tls: false` is correct for `cwlota.com`. On the first run against LOTA, results reflect cache-miss performance. Run the benchmark a second time to see fully cached performance.

The following example configuration shows a GET benchmark for `cwobject.com`. You can modify the other benchmark configurations similarly to run against the primary endpoint:

```yaml title="warp-test-cwobject-get.yaml" highlight={10-11} theme={"system"}
warp:
  api: v1
  benchmark: get
  remote:
    bucket: warp-benchmark-bucket
    region: [REGION]
    access-key: [ACCESS-KEY-ID]
    secret-key: [SECRET-ACCESS-KEY]
    host:
      - cwobject.com
    tls: true
    lookup: host
  params:
    duration: 5m
    concurrent: 300
    obj:
      size: 15MiB
    autoterm:
      enabled: true
```

## Run distributed benchmarks

Warp supports [distributed benchmarking](https://github.com/minio/warp?tab=readme-ov-file#distributed-benchmarking), where multiple Warp client instances run in parallel across different Nodes and a coordinator aggregates the results. This is how you scale beyond a single Node to test higher concurrency levels. The `concurrent` value applies per client, so three clients with `concurrent: 300` produce 900 total concurrent operations.

Running distributed Warp on Kubernetes requires deploying multiple Warp Pods with network connectivity between them. Warp provides a [Helm chart and Kubernetes manifests](https://github.com/minio/warp/blob/master/k8s/README.md) that handle this using a StatefulSet for the client Pods and a Job for the coordinator.

To run distributed benchmarks on CKS, adapt the upstream Warp Kubernetes manifests with the following changes:

* **Node scheduling**: Add [node affinity rules](https://docs.coreweave.com/products/cks/nodes/manage.md#target-specific-gpus-or-cpus) and any required [tolerations](https://docs.coreweave.com/products/cks/clusters/scheduling/workload-scheduling.md#taints-and-tolerations) to schedule Warp Pods on Nodes appropriate for your workload.
* **Endpoint**: Set the S3 host to `cwlota.com` instead of a MinIO server address.
* **Credentials**: Use your CoreWeave AI Object Storage [access key and secret key](https://docs.coreweave.com/products/storage/object-storage/auth-access/manage-access-keys/create-keys.md).

### Example: Install the Warp Helm chart

For a ready-to-use starting point, install the Warp Helm chart. Use the [example `configFile` values file](https://github.com/minio/warp/blob/master/k8s/helm/values-configfile-example.yaml), which sets `replicaCount`, client resource limits, and Pod security context.

1. Clone the Warp repository and install the Helm chart:

   ```bash title="Clone the Warp repository and install the Helm chart" theme={"system"}
   git clone https://github.com/minio/warp
   cd warp/k8s
   helm install warp helm/ -f helm/values-configfile-example.yaml
   ```

2. Override the `remote` section to point at CoreWeave AI Object Storage:

   ```yaml title="CoreWeave overrides for the Warp Helm chart values file" theme={"system"}
   remote:
     region: [REGION]
     access-key: [ACCESS-KEY-ID]
     secret-key: [SECRET-ACCESS-KEY]
     host:
       - cwlota.com
     tls: false
     lookup: host
     bucket: warp-benchmark-bucket
   ```

Always use a dedicated bucket for benchmarking. Replace `warp-benchmark-bucket` with your own bucket name for a dedicated benchmark bucket.

## Clean up

When you're done benchmarking, delete the Pod to release the cluster resources it consumes:

```bash theme={"system"}
kubectl delete pod warp-benchmark
```

## Contact support

For questions or assistance with large-scale dataset caching, contact [CoreWeave support](https://docs.coreweave.com/support.md).
