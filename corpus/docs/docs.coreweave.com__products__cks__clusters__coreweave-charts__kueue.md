# Kueue

Source: https://docs.coreweave.com/products/cks/clusters/coreweave-charts/kueue

# Kueue

> Install and configure Kueue for Kubernetes-native job queuing on CKS using CoreWeave's Helm chart

| Chart reference | Description |
| - | - |
| `coreweave/cks-kueue` | CoreWeave's Helm chart for deploying Kueue on CKS clusters |

## About Kueue

[Kueue](https://kueue.sigs.k8s.io/docs/overview/) is a Kubernetes-native system that manages jobs using quotas. Kueue makes job decisions based on resource availability, job priorities, and the quota policies defined in your cluster queues. Kueue determines when a job waits for available resources, when a job starts (Pods created), and when a job is preempted (active Pods deleted).

Use Kueue on CKS to prioritize batch, AI, and ML workloads, share GPU capacity fairly across teams, and reduce idle time on expensive accelerators.

CKS supports Kueue by default. To simplify getting started, CoreWeave provides a Helm chart for installing Kueue. The `cks-kueue` chart also includes a `kueue` subchart, used to configure Kueue for deployment into your CKS cluster.

> [!WARNING]
>
> Always install Kueue with CoreWeave's `cks-kueue` chart. Upstream Kueue registers admission webhooks that intercept system and infrastructure Pods, which can deadlock the cluster and prevent it from starting. The `cks-kueue` chart configures the webhooks to exclude these Pods, so the cluster can always start.

> [!NOTE]
>
> When you install Kueue through the CoreWeave Helm chart, Kueue metrics are automatically scraped and ingested into the [Kueue Scheduling Dashboard in CoreWeave Grafana](https://docs.coreweave.com/observability/managed-grafana/kubernetes/kueue-metrics.md).

## Usage

Install the `cks-kueue` Helm chart to deploy Kueue into your CKS cluster. The chart installs the Kueue controller and CRDs so you can begin defining queues and submitting workloads.

Add the CoreWeave Helm repo so Helm can locate the `cks-kueue` chart.

```bash theme={"system"}
helm repo add coreweave https://charts.core-services.ingress.coreweave.com
```

Then, install Kueue on your CKS cluster.

```bash theme={"system"}
helm install kueue coreweave/cks-kueue --namespace=kueue-system --create-namespace
```

After the chart installs, the Kueue controller runs in the `kueue-system` namespace and the Kueue CRDs are available for use in your cluster.

## Sample Kueue configuration

After you install the `cks-kueue` chart, use the following sample configuration to set up a basic Kueue environment for CKS. This configuration creates a single shared queue that gets you started with a proof of concept. Production deployments usually divide capacity among teams instead. For more information, see [Share capacity across teams with Cohorts](#share-capacity-across-teams-with-cohorts).

The samples use `kueue.x-k8s.io/v1beta2`. Before applying them, confirm that your installed Kueue CRDs serve this API version.

The configuration includes the following Kueue components:

* **`ResourceFlavor`**: Defines the characteristics of compute resources (CPU, memory, GPUs) available in your cluster.
* **`ClusterQueue`**: Establishes resource quotas and admission policies across your entire cluster.
* **`LocalQueue`**: Creates namespaced queues that reference a `ClusterQueue` for job submission.
* **`WorkloadPriorityClass`**: Defines priority levels for jobs to determine scheduling order and preemption behavior.

The configuration also defines two priority classes for different job types: production jobs with high priority and development jobs with lower priority.

```yaml theme={"system"}
# ResourceFlavor defines the compute resources available in your cluster
# This flavor represents the standard CKS Node configuration
---
apiVersion: kueue.x-k8s.io/v1beta2
kind: ResourceFlavor
metadata:
  name: default-flavor
---
# ClusterQueue establishes resource quotas and admission policies
# This queue allows jobs to consume up to the specified resource limits
apiVersion: kueue.x-k8s.io/v1beta2
kind: ClusterQueue
metadata:
  name: "cluster-queue"
spec:
  # Enable preemption of lower priority jobs when higher priority jobs need resources
  preemption:
    withinClusterQueue: LowerPriority
  # Allow jobs from all namespaces to use this queue
  namespaceSelector: {} # Match all namespaces.
  resourceGroups:
    - coveredResources: ["cpu", "memory", "nvidia.com/gpu", "rdma/ib"]
      flavors:
        - name: "default-flavor"
          resources:
            - name: "cpu"
              nominalQuota: 254          # Total CPU cores available
            - name: "memory"
              nominalQuota: 2110335488Ki # Total memory available (~2TB)
            - name: "nvidia.com/gpu"
              nominalQuota: 16           # Total GPUs available
            - name: "rdma/ib"
              nominalQuota: 12800        # Total number of RDMA Nodes available
---
# LocalQueue creates a namespaced queue for job submission
# Jobs submitted to this queue will use the cluster-queue resources
apiVersion: kueue.x-k8s.io/v1beta2
kind: LocalQueue
metadata:
  namespace: "default"
  name: "default"
spec:
  clusterQueue: "cluster-queue"
---
# WorkloadPriorityClass defines priority levels for job scheduling
# Higher values = higher priority (jobs with higher priority can preempt lower priority jobs)
apiVersion: kueue.x-k8s.io/v1beta2
kind: WorkloadPriorityClass
metadata:
  name: prod-priority
value: 1000
description: "Priority class for prod jobs"
---
apiVersion: kueue.x-k8s.io/v1beta2
kind: WorkloadPriorityClass
metadata:
  name: dev-priority
value: 100
description: "Priority class for development jobs"
---
```

> [!NOTE]
>
> For more information, see [Using Kueue with Ray on CKS](https://docs.coreweave.com/products/cks/clusters/frameworks/ray-with-kueue.md).

## Share capacity across teams with Cohorts

A `Cohort` groups ClusterQueues so that a team can borrow quota that other teams aren't using. With the `reclaimWithinCohort` policy shown in the following sample, a team can reclaim its nominal quota by preempting eligible workloads in borrowing queues. Admission still depends on the workload's resource requirements and scheduling constraints.

A single `ClusterQueue` is enough for a proof of concept, but most organizations divide cluster capacity among several teams. You can give each team its own `ClusterQueue` with a nominal quota and a `LocalQueue` in the team's namespace. Nominal quota defines an admission entitlement; it does not reserve physical GPUs.

The following configuration reuses the previous sample's `ResourceFlavor` and `WorkloadPriorityClass` resources. It splits the same resource quotas between two teams, `team-a` and `team-b`, and joins their ClusterQueues in a Cohort named `org-cohort`. It also creates the team namespaces and a `default` LocalQueue in each namespace.

> [!NOTE]
>
> Use these team queues instead of the previous sample's shared queue. If you applied that sample, stop submitting jobs to its `default` LocalQueue in the `default` namespace. Wait for its workloads to finish, then remove that LocalQueue and `cluster-queue` before applying the team configuration. Otherwise, both configurations can admit work against the same physical capacity.

Submit each team's jobs in its namespace with the label `kueue.x-k8s.io/queue-name: default`. To select a priority, also set `kueue.x-k8s.io/priority-class` to `prod-priority` or `dev-priority` on the job. Creating the priority classes alone does not assign them to jobs.

```yaml theme={"system"}
# Create the namespaces before their LocalQueues.
---
apiVersion: v1
kind: Namespace
metadata:
  name: team-a
---
apiVersion: v1
kind: Namespace
metadata:
  name: team-b
---
# Cohort groups ClusterQueues so they can share unused capacity.
# ClusterQueues join the Cohort by setting spec.cohortName.
---
apiVersion: kueue.x-k8s.io/v1beta2
kind: Cohort
metadata:
  name: org-cohort
# Optional spec fields: add resourceGroups to define shared quota in addition
# to the member ClusterQueues' quotas, or parentName to nest Cohorts.
---
# ClusterQueue for team-a with half of the sample's GPU quota
apiVersion: kueue.x-k8s.io/v1beta2
kind: ClusterQueue
metadata:
  name: team-a-queue
spec:
  # Join the org-cohort Cohort to borrow from and lend to team-b-queue
  cohortName: org-cohort
  preemption:
    # Higher-priority team-a jobs can preempt lower-priority team-a jobs
    withinClusterQueue: LowerPriority
    # Reclaim this queue's quota by preempting eligible workloads in
    # borrowing queues in the Cohort, regardless of workload priority
    reclaimWithinCohort: Any
    # When admission requires borrowing, allow preemption of lower-priority
    # workloads in other queues that are borrowing in the Cohort
    borrowWithinCohort:
      policy: LowerPriority
  # Only the team-a namespace can submit jobs to this queue
  namespaceSelector:
    matchLabels:
      kubernetes.io/metadata.name: team-a
  resourceGroups:
    - coveredResources: ["cpu", "memory", "nvidia.com/gpu", "rdma/ib"]
      flavors:
        - name: "default-flavor"
          resources:
            - name: "cpu"
              nominalQuota: 127
            - name: "memory"
              nominalQuota: 1055167744Ki
            - name: "nvidia.com/gpu"
              nominalQuota: 8
              borrowingLimit: 4 # Borrow at most 4 GPUs from the Cohort
            - name: "rdma/ib"
              nominalQuota: 6400
---
# ClusterQueue for team-b with the other half of the sample's GPU quota
apiVersion: kueue.x-k8s.io/v1beta2
kind: ClusterQueue
metadata:
  name: team-b-queue
spec:
  cohortName: org-cohort
  preemption:
    withinClusterQueue: LowerPriority
    reclaimWithinCohort: Any
    borrowWithinCohort:
      policy: LowerPriority
  namespaceSelector:
    matchLabels:
      kubernetes.io/metadata.name: team-b
  resourceGroups:
    - coveredResources: ["cpu", "memory", "nvidia.com/gpu", "rdma/ib"]
      flavors:
        - name: "default-flavor"
          resources:
            - name: "cpu"
              nominalQuota: 127
            - name: "memory"
              nominalQuota: 1055167744Ki
            - name: "nvidia.com/gpu"
              nominalQuota: 8
              borrowingLimit: 4
            - name: "rdma/ib"
              nominalQuota: 6400
---
# LocalQueue for team-a job submission in the team-a namespace
apiVersion: kueue.x-k8s.io/v1beta2
kind: LocalQueue
metadata:
  namespace: "team-a"
  name: "default"
spec:
  clusterQueue: "team-a-queue"
---
# LocalQueue for team-b job submission in the team-b namespace
apiVersion: kueue.x-k8s.io/v1beta2
kind: LocalQueue
metadata:
  namespace: "team-b"
  name: "default"
spec:
  clusterQueue: "team-b-queue"
---
```

With this configuration, Kueue behaves as follows:

* When `team-b` is idle, `team-a` has a quota ceiling of 12 GPUs: its 8 nominal GPUs plus 4 borrowed from the Cohort. Running those jobs also requires sufficient CPU, memory, RDMA resources, and physical capacity.
* When `team-b` needs its nominal quota, Kueue can preempt eligible workloads in `team-a`'s borrowing queue to make room (`reclaimWithinCohort: Any`). Reclaim can select workloads regardless of their priority, provided the incoming workload can fit after preemption.
* Within each queue, jobs with the `prod-priority` class can preempt jobs with the `dev-priority` class when needed for admission (`withinClusterQueue: LowerPriority`).

> [!NOTE]
>
> Kueue's [fair sharing](https://kueue.sigs.k8s.io/docs/concepts/fair_sharing/) feature supports `withinClusterQueue` and `reclaimWithinCohort`, but not `borrowWithinCohort`. If you enable fair sharing, remove `borrowWithinCohort` from your ClusterQueues.

### Plan your ClusterQueue split

The right way to divide quota among ClusterQueues depends on your organization. When you plan the split, consider the following:

* Create one `ClusterQueue` for each team that needs a nominal quota, and a `LocalQueue` in each namespace where that team submits jobs.
* Set each `nominalQuota` to the team's share. For a fixed-size cluster, keep the sum of quotas within the allocatable capacity of the Nodes that the `ResourceFlavor` matches, after accounting for system components and workloads outside Kueue. Kueue doesn't validate configured quotas against actual Node capacity, although topology-aware scheduling checks physical fit during workload admission.
* Use `namespaceSelector` to control which namespaces can submit jobs to each queue.
* Use `borrowingLimit` and `lendingLimit` to bound how much capacity moves between teams. For more information, see [ClusterQueue concepts](https://kueue.sigs.k8s.io/docs/concepts/cluster_queue/) in the Kueue documentation.
* Define `WorkloadPriorityClass` resources and assign them to jobs for consistent priority ordering. With `reclaimWithinCohort: Any`, reclaim can preempt even higher-priority workloads in borrowing queues.
* Revisit the split when you add Node capacity or when teams change. Adding Nodes does not automatically increase the nominal quotas configured in these samples. Update those quotas when you want the queues to admit more work.

## Observability

This section describes how to monitor Kueue activity after the chart is installed.

CoreWeave Grafana provides a [Kueue Scheduling Dashboard](https://docs.coreweave.com/observability/managed-grafana/kubernetes/kueue-metrics.md) that you can use to monitor your Kueue cluster.

## Topology-aware scheduling

Topology-aware scheduling (TAS) lets Kueue improve scheduling decisions by considering the physical topology of your cluster's Nodes. This is important for HPC, AI, and ML workloads, where network latency between Nodes can be a performance bottleneck. TAS can co-locate a job's Pods to minimize communication overhead and maximize performance.

The `TopologyAwareScheduling` feature in the Kueue controller is enabled by default. However, to use it, you must adjust some of the Kueue resources so that Kueue references the Node labels that describe your cluster's topology.

After the Helm chart is installed and the Kueue CRDs exist, choose one of the following topologies based on CKS Node labels for Kueue to use:

* The `infiniband` topology is for instance types that are a part of InfiniBand fabrics. See [About GPU instances](https://docs.coreweave.com/platform/instances/gpu-instances.md) to find InfiniBand connected instances.
* The `multinode-nvlink-ib` topology extends the `infiniband` topology to also include instance types with rack-scale NVLink. See [About GPU instances](https://docs.coreweave.com/platform/instances/gpu-instances.md) to find NVLink connected rack instances.
* The `hostname` topology is for instance types without InfiniBand fabrics. It prevents Kueue from admitting workloads when total capacity is sufficient but fragmented across Nodes.

```bash theme={"system"}
helm upgrade kueue coreweave/cks-kueue --namespace=kueue-system --values - <<EOF
topologies:
  - name: infiniband
    levels:
      - backend.coreweave.cloud/fabric
      - backend.coreweave.cloud/superpod
      - backend.coreweave.cloud/leafgroup
      - kubernetes.io/hostname
  - name: multinode-nvlink-ib
    levels:
      - backend.coreweave.cloud/fabric
      - backend.coreweave.cloud/superpod
      - backend.coreweave.cloud/leafgroup
      - ds.coreweave.com/nvlink.domain
      - kubernetes.io/hostname
  - name: hostname
    levels:
      - kubernetes.io/hostname
EOF
```

After you upgrade the Helm chart, the new `Topology` CRs appear in the cluster.

The following example configuration is an adjustment of the preceding one. It demonstrates how to use the `Topology` resources by referencing them in `ResourceFlavor` resources, which are then used by `ClusterQueue` and `LocalQueue` resources.

Each `ResourceFlavor` must select a disjoint set of Nodes. Use `nodeLabels` so that no Node matches more than one flavor. Overlapping selectors cause a Node to belong to multiple flavors, which leads to ambiguous quota accounting and unpredictable scheduling.

Match each `topologyName` to a Node pool whose hardware actually provides that topology. For example, pair the `infiniband` topology with an InfiniBand connected pool like B200, the `multinode-nvlink-ib` topology with a rack-scale NVLink pool like GB200, and the `hostname` topology with pools that lack InfiniBand.

> [!WARNING]
>
> Referencing a topology whose labels are not present on the selected Nodes causes Kueue to fail to admit workloads for that flavor. Verify that every label in the `Topology` `levels` list exists on the Nodes selected by the flavor's `nodeLabels`.

```yaml theme={"system"}
---
apiVersion: kueue.x-k8s.io/v1beta2
kind: ResourceFlavor
metadata:
  name: b200-flavor
spec:
  topologyName: infiniband # References the infiniband Topology CR
  nodeLabels:
    compute.coreweave.com/node-pool: b200-nodepool
---
# This flavor enables topology-aware scheduling across NVLINK domains
apiVersion: kueue.x-k8s.io/v1beta2
kind: ResourceFlavor
metadata:
  name: gb200-flavor
spec:
  topologyName: multinode-nvlink-ib # References the multinode-nvlink-ib Topology CR
  # nodeLabels is a map, so each flavor selects the Nodes that match all of
  # its labels. To cover more than one Node Pool, apply a shared label to the
  # pools and match that label, or create one flavor per Node Pool.
  nodeLabels:
    compute.coreweave.com/node-pool: gb200-nodepool
---
# ClusterQueue for InfiniBand-connected workloads
apiVersion: kueue.x-k8s.io/v1beta2
kind: ClusterQueue
metadata:
  name: "b200-queue"
spec:
  preemption:
    withinClusterQueue: LowerPriority
  namespaceSelector: {}
  resourceGroups:
    - coveredResources: ["cpu", "memory", "nvidia.com/gpu", "rdma/ib"]
      flavors:
        - name: "b200-flavor"
          resources:
            - name: "cpu"
              nominalQuota: 2048 # 16 Nodes * 128 vCPU per Node
            - name: "memory"
              nominalQuota: 34359738368Ki # 16 Nodes * 2Ti per Node = 32Ti
            - name: "nvidia.com/gpu"
              nominalQuota: 128 # 16 Nodes * 8 GPUs per Node
            - name: "rdma/ib"
              nominalQuota: 12800
---
# ClusterQueue for GB200 workloads with multinode-NVLINK
apiVersion: kueue.x-k8s.io/v1beta2
kind: ClusterQueue
metadata:
  name: "gb200-queue"
spec:
  preemption:
    withinClusterQueue: LowerPriority
  namespaceSelector: {}
  resourceGroups:
    - coveredResources: ["cpu", "memory", "nvidia.com/gpu", "rdma/ib"]
      flavors:
        - name: "gb200-flavor"
          resources:
            - name: "cpu"
              nominalQuota: 2304 # 16 Nodes * 144 vCPU per Node
            - name: "memory"
              nominalQuota: 15000000000Ki # 16 Nodes * 960 GB per Node = 15.36 TB
            - name: "nvidia.com/gpu"
              nominalQuota: 64 # 16 Nodes * 4 GPUs per Node
            - name: "rdma/ib"
              nominalQuota: 12800
---
# LocalQueue for InfiniBand workloads in the default namespace
apiVersion: kueue.x-k8s.io/v1beta2
kind: LocalQueue
metadata:
  namespace: "default"
  name: "b200-local"
spec:
  clusterQueue: "b200-queue"
---
# LocalQueue for GB200 workloads in the default namespace
apiVersion: kueue.x-k8s.io/v1beta2
kind: LocalQueue
metadata:
  namespace: "default"
  name: "gb200-local"
spec:
  clusterQueue: "gb200-queue"
---
# WorkloadPriorityClass definitions (same as basic example)
apiVersion: kueue.x-k8s.io/v1beta2
kind: WorkloadPriorityClass
metadata:
  name: prod-priority
value: 1000
description: "Priority class for prod jobs"
---
apiVersion: kueue.x-k8s.io/v1beta2
kind: WorkloadPriorityClass
metadata:
  name: dev-priority
value: 100
description: "Priority class for development jobs"
---
```

### Example jobs with topology constraints

Kueue applies topology constraints to a Pod set, which is a group of Pods with the same specification in a Workload. Configure topology annotations on the Pod template, at `spec.template.metadata.annotations` for a Job or `spec.replicatedJobs[].template.spec.template.metadata.annotations` for a JobSet.

| Annotation | Placement constraint |
| - | - |
| `kueue.x-k8s.io/podset-required-topology` | All Pods in the Pod set must fit in one domain at the specified topology level. The workload waits until a domain can fit it. |
| `kueue.x-k8s.io/podset-preferred-topology` | Prefer one domain at the specified level, but allow placement across domains if needed. |
| `kueue.x-k8s.io/podset-slice-required-topology` | Each slice must fit in one domain at the specified level. Configure this together with `podset-slice-size`. |
| `kueue.x-k8s.io/podset-slice-size` | Number of Pods per slice. Configure this together with `podset-slice-required-topology`. |

For example, `ds.coreweave.com/nvlink.domain` selects the NVLink domain level. It doesn't name a particular rack or specify how many slices to place in each rack. The selected level must exist in the `Topology` referenced by the workload's `ResourceFlavor`.

Choose a positive slice size no greater than the Pod set count. Use a size that evenly divides the count when you need equal-sized slices. Multiple slices can share a domain. With eight Pods and a slice size of two, possible domain counts include the following, depending on capacity and other constraints:

* `8`
* `6+2`
* `4+4`
* `4+2+2`
* `2+2+2+2`

The setting doesn't select one of these layouts.

Kueue 0.20 adds `TASPartialSlices`, enabled by default, which allows a smaller final slice for a single slice topology level. For example, eight Pods with a slice size of three form slices of `3+3+2`. Check your installed version and feature gates before relying on partial slices. Evenly divisible sizes also work with older releases.

The `kueue.x-k8s.io/podset-slice-required-topology-constraints` annotation expresses nested slice constraints as a JSON array of topology levels and sizes. It requires `TASMultiLayerTopology` and replaces the two slice annotations in the table. Don't combine them. It describes grouping within a topology hierarchy, not exact counts for named racks.

For the full list of annotations and their semantics, see the [Kueue Topology Aware Scheduling user-facing APIs](https://kueue.sigs.k8s.io/docs/concepts/topology_aware_scheduling/#user-facing-apis).

#### Four Pods on one leafgroup with the InfiniBand queue

This example schedules four Pods within a single leafgroup:

```yaml theme={"system"}
apiVersion: batch/v1
kind: Job
metadata:
  name: test-tas-job
  namespace: default
  labels:
    kueue.x-k8s.io/queue-name: b200-local
spec:
  parallelism: 4
  completions: 4
  template:
    metadata:
      annotations:
        kueue.x-k8s.io/podset-required-topology: "backend.coreweave.cloud/leafgroup"
    spec:
      containers:
        - name: training
          image: busybox
          command: ["sleep", "30s"]
          resources:
            requests:
              cpu: "32"
              memory: "256Gi"
              nvidia.com/gpu: "8"
              rdma/ib: "1"
            limits:
              cpu: "32"
              memory: "256Gi"
              nvidia.com/gpu: "8"
              rdma/ib: "1"
      restartPolicy: Never
```

#### Four Pods on one NVLINK domain with the GB200 queue

This example schedules four Pods within a single NVLINK domain for GB200 Nodes:

```yaml theme={"system"}
apiVersion: batch/v1
kind: Job
metadata:
  name: gb200-test-tas
  labels:
    kueue.x-k8s.io/queue-name: gb200-local
spec:
  parallelism: 4
  completions: 4
  template:
    metadata:
      annotations:
        kueue.x-k8s.io/podset-required-topology: "ds.coreweave.com/nvlink.domain"
    spec:
      containers:
        - name: training
          image: your-training-image:latest
          resources:
            requests:
              cpu: "32"
              memory: "256Gi"
              nvidia.com/gpu: "4"
              rdma/ib: "1"
            limits:
              cpu: "32"
              memory: "256Gi"
              nvidia.com/gpu: "4"
              rdma/ib: "1"
      restartPolicy: Never
```

#### Eight Pods in slices of two

This Job keeps each pair of Pods within one NVLink domain while allowing the eight Pods to use multiple domains. It uses the `gb200-local` LocalQueue and `multinode-nvlink-ib` topology configured in this section. Replace `[TRAINING-IMAGE]` with your workload image. Each Pod requests all four GPUs on a GB200 Node, so the eight Pods require eight Nodes.

```yaml theme={"system"}
apiVersion: batch/v1
kind: Job
metadata:
  name: gb200-sliced-job
  namespace: default
  labels:
    kueue.x-k8s.io/queue-name: gb200-local
spec:
  suspend: true
  completionMode: Indexed
  parallelism: 8
  completions: 8
  template:
    metadata:
      annotations:
        kueue.x-k8s.io/podset-slice-required-topology: "ds.coreweave.com/nvlink.domain"
        kueue.x-k8s.io/podset-slice-size: "2"
    spec:
      containers:
        - name: training
          image: "[TRAINING-IMAGE]"
          resources:
            requests:
              cpu: "32"
              memory: "256Gi"
              nvidia.com/gpu: "4"
              rdma/ib: "1"
            limits:
              cpu: "32"
              memory: "256Gi"
              nvidia.com/gpu: "4"
              rdma/ib: "1"
      restartPolicy: Never
```

For rejected annotations or a workload waiting for topology capacity, see [Match the message to a fix](https://docs.coreweave.com/support/cks/articles/how-do-i-troubleshoot-suspended-kueue-workloads#match-the-message-to-a-fix).

### Place an exact number of Nodes in each rack

For a performance test that requires a specific layout, select the Nodes explicitly with a test label and a matching `nodeSelector` field. Slice annotations constrain groups of Pods but don't express exact rack allocations. A slice size of one permits any layout without enforcing a particular one.

#### One Node in rack 1, three in rack 2, and four in rack 3

This example runs eight Pods on eight GB200 Nodes, with one Pod per Node. It uses the `gb200-local` LocalQueue and `multinode-nvlink-ib` topology configured in this section. Work with a cluster administrator who can label and taint Nodes. Each selected Node must match the `gb200-flavor` ResourceFlavor and have the following resources available:

* Four GPUs.
* 32 CPUs.
* 256 GiB of memory.
* One `rdma/ib` resource.

**1. Identify the rack groups**

Inspect the NVLink domain labels to identify the rack groups:

```bash theme={"system"}
kubectl get nodes -l compute.coreweave.com/node-pool=gb200-nodepool \
  -o custom-columns='NAME:.metadata.name,RACK:.metadata.labels.ds\.coreweave\.com/nvlink\.domain'
```

Select one schedulable Node from the first domain, three from the second, and four from the third.

**2. Label the selected Nodes**

Label only those eight Nodes. Replace each `RACK_N_NODE_N` placeholder with the selected Node's name. Use a label value unique to this test. If you change `layout-1-3-4`, use the same value throughout the example.

```bash theme={"system"}
kubectl label nodes "RACK_1_NODE_1" \
  "RACK_2_NODE_1" "RACK_2_NODE_2" "RACK_2_NODE_3" \
  "RACK_3_NODE_1" "RACK_3_NODE_2" "RACK_3_NODE_3" "RACK_3_NODE_4" \
  example.com/rack-test=layout-1-3-4
```

**3. Optional: Taint the selected Nodes**

To block new Pods that lack a matching toleration, taint the selected Nodes:

```bash theme={"system"}
kubectl taint nodes -l example.com/rack-test=layout-1-3-4 \
  example.com/rack-test=layout-1-3-4:NoSchedule
```

This taint doesn't evict existing Pods. The Job in the next step includes the matching toleration. Its `nodeSelector` field restricts placement to the labeled Nodes. The toleration alone doesn't select Nodes. See [Assigning Pods to Nodes](https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/) and [Taints and Tolerations](https://kubernetes.io/docs/concepts/scheduling-eviction/taint-and-toleration/).

**4. Save the Job manifest**

Save the following manifest as `gb200-rack-placement.yaml`. Replace `TRAINING_IMAGE` with your workload image.

Each Pod requests all four GPUs of a GB200 Node. With exactly eight labeled Nodes, the eight simultaneous Pods occupy one Node each. The unconstrained topology annotation allows the selected rack layout while Kueue still checks quota and physical capacity. Don't add required, preferred, or slice topology annotations to this Pod template.

```yaml title="gb200-rack-placement.yaml" theme={"system"}
apiVersion: batch/v1
kind: Job
metadata:
  name: gb200-rack-placement
  namespace: default
  labels:
    kueue.x-k8s.io/queue-name: gb200-local
spec:
  suspend: true
  completionMode: Indexed
  parallelism: 8
  completions: 8
  template:
    metadata:
      annotations:
        kueue.x-k8s.io/podset-unconstrained-topology: "true"
    spec:
      nodeSelector:
        example.com/rack-test: layout-1-3-4
      tolerations:
        - key: example.com/rack-test
          operator: Equal
          value: layout-1-3-4
          effect: NoSchedule
      containers:
        - name: training
          image: "TRAINING_IMAGE"
          resources:
            requests:
              cpu: "32"
              memory: "256Gi"
              nvidia.com/gpu: "4"
              rdma/ib: "1"
            limits:
              cpu: "32"
              memory: "256Gi"
              nvidia.com/gpu: "4"
              rdma/ib: "1"
      restartPolicy: Never
```

**5. Submit the Job**

```bash theme={"system"}
kubectl apply -f gb200-rack-placement.yaml
```

**6. Verify the rack distribution**

After Kueue admits the Job and all eight Pods are running, list their assigned Nodes:

```bash theme={"system"}
kubectl get pods -n default -l batch.kubernetes.io/job-name=gb200-rack-placement \
  -o custom-columns='NAME:.metadata.name,STATUS:.status.phase,NODE:.spec.nodeName'
```

Example output:

```text title="Example output" theme={"system"}
NAME                             STATUS    NODE
gb200-rack-placement-0-abcde     Running   gb200-node-01
gb200-rack-placement-1-bcdef     Running   gb200-node-02
gb200-rack-placement-2-cdefg     Running   gb200-node-03
gb200-rack-placement-3-defgh     Running   gb200-node-04
gb200-rack-placement-4-efghj     Running   gb200-node-05
gb200-rack-placement-5-fghjk     Running   gb200-node-06
gb200-rack-placement-6-ghjkl     Running   gb200-node-07
gb200-rack-placement-7-hjklm     Running   gb200-node-08
```

List the labeled Nodes and their NVLink domains:

```bash theme={"system"}
kubectl get nodes -l example.com/rack-test=layout-1-3-4 \
  -o custom-columns='NAME:.metadata.name,RACK:.metadata.labels.ds\.coreweave\.com/nvlink\.domain'
```

Example output, with illustrative NVLink domain values `rack-1`, `rack-2`, and `rack-3`:

```text title="Example output" theme={"system"}
NAME            RACK
gb200-node-01   rack-1
gb200-node-02   rack-2
gb200-node-03   rack-2
gb200-node-04   rack-2
gb200-node-05   rack-3
gb200-node-06   rack-3
gb200-node-07   rack-3
gb200-node-08   rack-3
```

Match each Pod's assigned Node to its NVLink domain. These outputs show one Pod in `rack-1`, three in `rack-2`, and four in `rack-3`, each on a different Node. Confirm this distribution before measuring performance. Pod indexes don't determine which rack receives each Pod.

**7. Clean up**

If you added the test taint, remove it after the test finishes. Then remove the test label:

```bash theme={"system"}
kubectl taint nodes -l example.com/rack-test=layout-1-3-4 example.com/rack-test:NoSchedule-
kubectl label nodes -l example.com/rack-test=layout-1-3-4 example.com/rack-test-
```

For help adapting this approach to your workload or cluster configuration, contact [CoreWeave Support](https://docs.coreweave.com/support/contact.md).
