# About Regions and Availability Zones (AZs)

Source: https://docs.coreweave.com/platform/regions/about-regions-and-azs

# About Regions and Availability Zones (AZs)

> Learn about CoreWeave Regions and Availability Zones, including General Access and Dedicated Access options

CoreWeave offers compute in multiple geographically diverse locations to ensure high availability, resilience, global coverage, and low-latency access for your applications. CoreWeave organizes these locations into Geos, Super Regions, Regions, and Availability Zones (AZs).

Regions and Availability Zones (AZs) are the core concepts to understand when you deploy applications on CoreWeave. These are located within Super Regions and Geos, which are explained in more detail in the [Geographical hierarchy](#geographical-hierarchy) section. Regions contain one or more AZs. CoreWeave categorizes AZs as General Access or Dedicated Access.

For a list of every AZ and its access type, see [All Availability Zones](https://docs.coreweave.com/platform/regions/all-availability-zones.md).

## General access

General Access AZs are available to all CoreWeave customers, subject to capacity. [VPCs](https://docs.coreweave.com/products/networking/vpc/about-vpcs.md) isolate tenant workloads, with per-tenant network segmentation enforced at the hardware layer by [DPUs](https://docs.coreweave.com/products/networking/nimbus.md).

## Dedicated access

CoreWeave manages Dedicated Access AZs and reserves them for select customers. Infrastructure in a Dedicated Access AZ is single-tenant: no other customer's workloads run in the AZ, and no other tenant shares the underlying network fabric. This provides full network isolation in addition to the platform-wide [VPC](https://docs.coreweave.com/products/networking/vpc/about-vpcs.md) and [DPU-based](https://docs.coreweave.com/products/networking/nimbus.md) tenant segmentation.

## Region features

All CoreWeave Regions offer these features:

* **Free data transfer**: move data between Regions without incurring additional costs.
* **Fast and reliable internet access**: each Region has redundant, 200 Gbps+ public internet connectivity from Tier 1 global carriers.
* **High-speed, private dark fiber backbone**: all Regions connect through 400 Gbps+ of dark fiber to enable rapid data movement and synchronization.
* [**Distributed File Storage**](https://docs.coreweave.com/products/storage/distributed-file-storage/create-volumes.md): each Region offers high-performance shared filesystems for your applications.
* [**Virtual Private Clouds**](https://docs.coreweave.com/products/networking/vpc/about-vpcs.md): all Regions provide VPCs for network isolation and security.
* [**CoreWeave AI Object Storage**](https://docs.coreweave.com/products/storage/object-storage.md): available in select Availability Zones.

## Geographical hierarchy

The following terms describe how CoreWeave structures its global infrastructure:

| Term | Description | Example |
| - | - | - |
| **Geo** | A large geographic area, such as a continent or a large country. CoreWeave uses Geos to manage global infrastructure, ensure compliance with regulatory requirements, and optimize for large-scale redundancy and disaster recovery. | All locations in the United States reside in the `US` Geo. |
| **Super Region** | A large section of a Geo that typically contains multiple Regions. Super Regions group Regions together for administrative purposes and provide a high-level view of the infrastructure in a geographic area. | All locations in the eastern United States are part of the `US-EAST` Super Region. |
| **Region** | An area within a Geo that contains multiple Availability Zones (AZs). Regions provide the infrastructure foundation for resiliency. When you deploy across multiple AZs within a Region, you can design failover-ready workloads that minimize downtime. CoreWeave places Regions to offer low latency, high-performance connectivity, and to meet data residency requirements. | Region `US-EAST-05` resides in the `US-EAST` Super Region. |
| **Availability Zone (AZ)** | A partition within a Region that hosts one or more data halls. AZs are physically and operationally independent from each other to prevent failures from propagating across them. | Availability Zone `A` in the `US-EAST-05` Region is named `US-EAST-05A`. |

Together, these concepts provide the foundation for high availability, fault tolerance, and disaster recovery for your applications and workloads.

## Region and AZ labels

CoreWeave exposes Region and AZ information through two different sets of labels depending on the context: Kubernetes Node labels for scheduling, and metrics labels for queries, APIs, and CRDs.

### Kubernetes Node labels

Use these labels in `nodeSelector`, affinity rules, and topology spread constraints:

| Label | Value | Example |
| :- | :- | :- |
| `topology.kubernetes.io/region` | Region name | `US-EAST-04` |

> [!NOTE]
>
> The standard Kubernetes label `topology.kubernetes.io/zone` is present on CoreWeave Nodes but doesn't hold the AZ name. It holds a rack number for use by topology-aware schedulers. No AZ-level Kubernetes Node label exists. Because CKS clusters are single-AZ, AZ affinity within a cluster isn't needed.

### Metrics and API labels

Use these labels in metrics queries, API calls, and CRDs. They appear on `kube_node_info` and in CoreWeave CRDs, but aren't Kubernetes Node labels.

| Label | Value | Example |
| :- | :- | :- |
| `region` | Region name | `US-EAST-04` |
| `zone` | AZ name | `US-EAST-04A` |

### Single-AZ CKS clusters

CoreWeave Kubernetes Service (CKS) clusters are zonal. CoreWeave provisions each cluster within a single AZ. All Nodes in a cluster belong to the same AZ, so you don't need AZ affinity rules within a cluster.

If you need rack-level placement within an AZ (for example, to co-locate Nodes on the same NVLink fabric), use the `node.coreweave.cloud/rack` label in a `nodeSelector` or affinity rule. The following Pod schedules only onto Nodes in rack `12`, which keeps tightly coupled multi-Node jobs on the same fabric segment:

```yaml title="rack-pinned-pod.yaml" highlight={6-13} theme={"system"}
apiVersion: v1
kind: Pod
metadata:
  name: example-rack-pinned
spec:
  affinity:
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
        - matchExpressions:
          - key: node.coreweave.cloud/rack
            operator: In
            values:
            - "12"   # Replace with your rack number
  containers:
  - name: example
    image: [IMAGE]   # Replace with your container image
    resources:
      limits:
        nvidia.com/gpu: 8
```

To discover the rack and instance type label values present in your cluster before you pin to them, list them with `kubectl`:

```bash theme={"system"}
# List each Node with its rack number. Read-only; safe to run anytime.
kubectl get nodes -L node.coreweave.cloud/rack

# List each Node's rack and instance type together. Read-only; safe to run anytime.
kubectl get nodes -L node.coreweave.cloud/rack -L node.coreweave.cloud/type
```

A `nodeSelector` or affinity that targets a value not shown by these commands leaves the Pod Pending, because no Node matches. For multi-rack fabric locality (keeping a large job within one InfiniBand or RoCE fabric), use the leafgroup and superpod labels instead. See [InfiniBand and RoCE node labels](https://docs.coreweave.com/products/networking/hpc-interconnect/infiniband-roce-labels.md) for details.

## Choose a Region and Zone for your GPU quota

CKS clusters are single-AZ. Confirm your target AZ supports the instance types you need before creating a cluster.

To check which instance types an AZ offers, use the [Instance availability matrix](https://docs.coreweave.com/platform/instances/availability-matrix.md). The matrix lists each instance type and where it's deployed.

The matrix shows where instance types are deployed, not current availability. Actual provisioning depends on availability and your [resource quota](https://docs.coreweave.com/products/cks/clusters/quotas.md).

## What to do when capacity is unavailable

If your instance type isn't available in your target AZ, choose a different instance type or AZ, or [contact CoreWeave support](https://docs.coreweave.com/support.md) to discuss your options.

## Speedtest

To verify network performance for a Region or AZ before you deploy workloads, run speed tests with `ping`, `curl`, or another method of your choice. Each Availability Zone in the [All Availability Zones](https://docs.coreweave.com/platform/regions/all-availability-zones.md) table lists speed and latency test endpoints in its Network information section. For example, to measure name lookup, connect, and total transfer times with `curl`, replace `[SPEEDTEST-URL]` with one of those endpoints and run:

```bash title="Example curl command" theme={"system"}
curl [SPEEDTEST-URL] \
       --write-out '\nDNS: %{time_namelookup}s\nConnect: %{time_connect}s\nTotal: %{time_total}s\n' \
       --output /dev/null
```

```text title="Result" theme={"system"}
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100 1024M  100 1024M    0     0  37.2M      0  0:00:27  0:00:27 --:--:-- 38.9M

DNS: 0.001822s
Connect: 0.091322s
Total: 27.465658s
```
