# InfiniBand and RoCE labels

Source: https://docs.coreweave.com/products/networking/hpc-interconnect/infiniband-roce-labels

# InfiniBand and RoCE labels

> Learn about the labels used for InfiniBand and RoCE

CoreWeave automatically applies a set of topology and performance labels to Nodes that are connected to high-performance backend fabrics such as InfiniBand and RoCE (RDMA over Converged Ethernet). You can use these labels for the following purposes:

* Control where Pods are scheduled.
* Monitor the health and capacity of the backend network.

Backend labels use a common, fabric-agnostic schema and are applied to both InfiniBand and RoCE Nodes. InfiniBand Nodes also expose an additional set of InfiniBand-specific labels that remain available for existing workloads and dashboards.

The following table lists the backend labels and what each one represents:

| Label | Description |
| :- | :- |
| `backend.coreweave.cloud/flavor` | The type of backend high-performance fabric attached to the Node, for example `infiniband` or `roce`. |
| `backend.coreweave.cloud/fabric` | The name of the backend fabric, representing a distinct InfiniBand or RoCE fabric. |
| `backend.coreweave.cloud/leafgroup-name` | A human-readable identifier for the group of leaf switches (leafgroup or Pod) that serve a common set of Nodes. |
| `backend.coreweave.cloud/leafgroup` | An identifier for the same leafgroup or Pod. This is convenient in dashboards or alerts where a compact identifier is preferred over `leafgroup-name`. |
| `backend.coreweave.cloud/neighbors.expected.{interface}.device` | The ID of the expected leaf connected to the Node at this physical interface. |
| `backend.coreweave.cloud/neighbors.expected.{interface}.port-id` | The ID of the expected port connected to the Node at this physical interface. |
| `backend.coreweave.cloud/neighbors.expected.{interface}.port-name` | The expected port name on the leaf or Pod switch (if exported by the fabric), which can make dashboards and runbooks easier to interpret than raw port numbers alone. |
| `backend.coreweave.cloud/neighbors.current.{interface}.device` | The ID of the current leaf connected to the Node at this physical interface. |
| `backend.coreweave.cloud/neighbors.current.{interface}.port-id` | The ID of the current port connected to the Node at this physical interface. |
| `backend.coreweave.cloud/neighbors.current.{interface}.port-name` | The name of the current port on the leaf, when exposed by the fabric. |
| `backend.coreweave.cloud/speed.current` | The current speed of the backend network connected to the Node. |
| `backend.coreweave.cloud/speed.expected` | The expected speed of the backend network for optimal performance. |
| `backend.coreweave.cloud/superpod` | The number identifying the superpod within the backend topology. |
| `node.coreweave.cloud/rack` | The number identifying the physical rack where the Node is located. |

## InfiniBand compatible labels

InfiniBand Nodes also expose `ib.coreweave.cloud/*` labels. These labels carry the same topology and speed information, but use an InfiniBand-specific prefix that predates the backend schema and may still appear in existing workloads and dashboards.

The following table shows how the InfiniBand labels relate to the backend schema:

| InfiniBand labels | Backend-equivalent labels | Description |
| :- | :- | :- |
| `ib.coreweave.cloud/fabric` | `backend.coreweave.cloud/fabric` | InfiniBand fabric name representing a distinct InfiniBand fabric within a Region. |
| `ib.coreweave.cloud/leafgroup`, `ib.coreweave.cloud/leafgroup-name` | `backend.coreweave.cloud/leafgroup`, `backend.coreweave.cloud/leafgroup-name` | Numeric and human-readable identifiers for the leafgroup or Pod that serves a common set of Nodes. |
| `ib.coreweave.cloud/neighbors.*`, `ib.coreweave.cloud/ports.*` | `backend.coreweave.cloud/neighbors.*` | Per-interface and aggregate neighbor and port information on InfiniBand Nodes. The backend per-interface labels use the fabric-agnostic schema. |
| `ib.coreweave.cloud/speed.current`, `ib.coreweave.cloud/speed.expected` | `backend.coreweave.cloud/speed.current`, `backend.coreweave.cloud/speed.expected` | Current and expected speed of the InfiniBand network connected to the Node. |
| `ib.coreweave.cloud/superpod` | `backend.coreweave.cloud/superpod` | The number identifying the superpod within the InfiniBand topology. |

For new deployments and dashboards, we recommend building on the `backend.coreweave.cloud/*` labels wherever possible, while continuing to recognize the `ib.coreweave.cloud/*` labels on existing InfiniBand clusters.

## Use labels for Pod affinity

You can use these labels in Pod affinity and anti-affinity rules to steer workloads toward specific parts of the fabric. Common use cases include the following:

* Keep large multi-Node jobs within a single rack or superpod.
* Choose between InfiniBand and RoCE fabrics.
* Separate different workloads across fabrics and racks for fault-isolation or performance reasons.

### Example: Target a specific backend fabric, superpod, and rack

The following Pod affinity rule targets Nodes on a specific backend fabric and superpod, restricted to a given rack. It also ensures that Pods land on either RoCE-backed or InfiniBand-backed Nodes by setting `backend.coreweave.cloud/flavor` appropriately. Replace `[FABRIC-NAME]`, `[SUPERPOD-NUMBER]`, and `[RACK-NUMBER]` with the values from the `backend.coreweave.cloud/fabric`, `backend.coreweave.cloud/superpod`, and `node.coreweave.cloud/rack` labels on your Nodes:

```yaml theme={"system"}
affinity:
  nodeAffinity:
    requiredDuringSchedulingIgnoredDuringExecution:
      nodeSelectorTerms:
      - matchExpressions:
        - key: backend.coreweave.cloud/flavor
          operator: In
          values:
          - roce # Or 'infiniband' for InfiniBand-backed Nodes
        - key: backend.coreweave.cloud/fabric
          operator: In
          values:
          - [FABRIC-NAME] # Your backend fabric name
        - key: backend.coreweave.cloud/superpod
          operator: In
          values:
          - [SUPERPOD-NUMBER] # Your superpod number
        - key: node.coreweave.cloud/rack
          operator: In
          values:
          - [RACK-NUMBER] # Your rack number
```

On older InfiniBand-only clusters that don't yet expose the backend labels, you can instead match directly on the following labels using the same affinity pattern:

* `ib.coreweave.cloud/fabric`
* `ib.coreweave.cloud/superpod`
* `node.coreweave.cloud/rack`

### Keep a job within one leafgroup

Traffic that stays within a single leafgroup doesn't traverse the spine of the fabric, so it has lower latency and competes less for spine bandwidth. Collective operations such as all-reduce run at the speed of the slowest path, so a job confined to one leafgroup can run noticeably faster than the same job spread across leafgroups. Pin a job to one leafgroup with a Node affinity rule. Replace `[LEAFGROUP-ID]` with the value from the `backend.coreweave.cloud/leafgroup` label on your Nodes:

```yaml theme={"system"}
affinity:
  nodeAffinity:
    requiredDuringSchedulingIgnoredDuringExecution:
      nodeSelectorTerms:
        - matchExpressions:
            - key: backend.coreweave.cloud/flavor
              operator: In
              values:
                - infiniband # Or 'roce' for RoCE-backed Nodes.
            - key: backend.coreweave.cloud/leafgroup
              operator: In
              values:
                - "[LEAFGROUP-ID]" # The leafgroup you read from the labels.
```

### Keep a job within one superpod

A superpod spans multiple leafgroups but stays within one rail-optimized region of the fabric. When a job is too large for a single leafgroup but you still want to limit cross-spine traffic, use this:

```yaml theme={"system"}
affinity:
  nodeAffinity:
    requiredDuringSchedulingIgnoredDuringExecution:
      nodeSelectorTerms:
        - matchExpressions:
            - key: backend.coreweave.cloud/fabric
              operator: In
              values:
                - "[FABRIC-NAME]" # Your backend fabric name.
            - key: backend.coreweave.cloud/superpod
              operator: In
              values:
                - "[SUPERPOD-NUMBER]" # Your superpod number.
```

## How to use these labels

Beyond affinity rules, you can read these labels directly to plan topology-aware placement and to identify Nodes running below their expected fabric speed.

### Read the labels with kubectl

The following command prints the fabric, superpod, leafgroup, and current and expected backend speed for every Node, so you can see how Nodes group on the fabric:

```bash theme={"system"}
# List backend topology and speed labels across all Nodes.
# Safe to run anytime; read-only.
kubectl get nodes -o custom-columns='NODE:.metadata.name,FLAVOR:.metadata.labels.backend\.coreweave\.cloud/flavor,FABRIC:.metadata.labels.backend\.coreweave\.cloud/fabric,SUPERPOD:.metadata.labels.backend\.coreweave\.cloud/superpod,LEAFGROUP:.metadata.labels.backend\.coreweave\.cloud/leafgroup,SPEED_CUR:.metadata.labels.backend\.coreweave\.cloud/speed\.current,SPEED_EXP:.metadata.labels.backend\.coreweave\.cloud/speed\.expected'
```

A Node with no `backend.coreweave.cloud/*` labels, or `flavor=none`, has no high-performance backend fabric attached. For example, CKS A100 Nodes are Ethernet-only and don't expose InfiniBand topology labels.

### When speed.current does not equal speed.expected

The `backend.coreweave.cloud/speed.current` label reports the speed the Node is running at now, and `backend.coreweave.cloud/speed.expected` reports the speed it should run at for full performance. When the two differ, one or more backend links on that Node failed to come up at full speed. For example, `speed.current` of `2800G` against a `speed.expected` of `3200G` indicates one 400G link is down.

When you see a mismatch:

* **Avoid scheduling new latency-sensitive or large multi-Node jobs on that Node.** A degraded link reduces collective bandwidth and can slow the whole job to the speed of its weakest Node.
* **Open a ticket** if the Node doesn't recover. CoreWeave fleet management detects degraded backend links automatically. When the degradation is isolated to a Node, CoreWeave pulls the Node from your cluster once it's clear of workloads and delivers a replacement, so no manual repair is required from you. When many Nodes in the same leaf group degrade at once, the cause is usually a switch; those Nodes stay in your cluster and recover in place after CoreWeave repairs the fabric.

### Set realistic bandwidth expectations by GPU type

Different GPU instance types have different numbers of backend interfaces, which sets the bandwidth ceiling for collectives. Read the labels to confirm what a given Node provides before comparing measured NCCL bandwidth against expectations.

For a deeper walkthrough of reading these labels for placement, including Kueue topology examples, see the placement guidance under [HPC Interconnect](https://docs.coreweave.com/products/networking/hpc-interconnect/about-hpc-interconnect.md) and the [networking support articles](https://docs.coreweave.com/support/networking.md).
