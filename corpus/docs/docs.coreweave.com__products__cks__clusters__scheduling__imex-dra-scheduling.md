# IMEX with Dynamic Resource Allocation

Source: https://docs.coreweave.com/products/cks/clusters/scheduling/imex-dra-scheduling

# IMEX with Dynamic Resource Allocation

> Schedule workloads using IMEX channels via Kubernetes Dynamic Resource Allocation (DRA) on rack-based instances

This page explains how to schedule multi-node GPU workloads that require IMEX channels on CoreWeave NVL72-powered instances by using Kubernetes Dynamic Resource Allocation (DRA). It's intended for cluster operators and workload authors who need cross-Node GPU memory access within an NVLink Domain.

For background on what IMEX is and how it relates to NVLink domains on CoreWeave, start with [IMEX overview](https://docs.coreweave.com/products/cks/clusters/scheduling/imex-overview.md).

[IMEX (Internode Memory Exchange)](https://docs.nvidia.com/multi-node-nvlink-systems/imex-guide/overview.html) is NVIDIA's mechanism that enables direct GPU-to-GPU memory access across Nodes within the same NVLink Domain. On [NVL72-powered instances](https://docs.coreweave.com/platform/instances/nvl72.md), IMEX is required for multi-node workloads that rely on high-bandwidth communication across all Nodes in a rack.

CoreWeave uses the [NVIDIA DRA Driver](https://github.com/kubernetes-sigs/dra-driver-nvidia-gpu) for assigning IMEX channels to workloads. The driver provides the `ComputeDomain` abstraction, which presents IMEX channels as allocatable container resources through DRA.

> [!WARNING]
>
> **Limited availability**
>
> We advise against directly interacting with `ComputeDomain` resources, as doing so will conflict with CoreWeave's configuration. Support for customer-managed DRA IMEX is planned for a future release.

## Provision ComputeDomains

A `ComputeDomain` defines a logical container for a set of Nodes that are permitted to share an IMEX channel allocation. You create a `ComputeDomain` in your namespace, and the controller generates a corresponding `ResourceClaimTemplate` that workloads can reference to obtain access to a shared channel.

> [!NOTE]
>
> Each independent workload should use its own `ComputeDomain`. Deploying multiple workloads into a single `ComputeDomain` works, but it may result in unintended memory sharing between them.

Replace `[COMPUTE-DOMAIN-NAME]` with a name for the `ComputeDomain`, and replace `[NAMESPACE]` with the namespace of the workload that will use it.

```yaml theme={"system"}
apiVersion: resource.nvidia.com/v1beta1
kind: ComputeDomain
metadata:
  name: [COMPUTE-DOMAIN-NAME]
  namespace: [NAMESPACE]
spec:
  channel:
    resourceClaimTemplate:
      name: imex-channel-0
```

The `ResourceClaimTemplate` contains the same name and namespace.

```yaml theme={"system"}
apiVersion: resource.k8s.io/v1beta1
kind: ResourceClaimTemplate
metadata:
  name: imex-channel-0
  namespace: [NAMESPACE]
  # ...
```

## Claim IMEX channels from a ComputeDomain

A `ComputeDomain` follows the workload, and its Node membership depends on where Pods land. This means the validity of the resulting IMEX domain depends on scheduling. If Pods spread across Nodes that aren't physically connected through NVLink, the workload may not function as expected. For this reason, workloads should always include affinity rules to constrain Pods to Nodes within the same rack.

To claim an IMEX channel, add a `resourceClaims` entry to your Pod specification that references the `ResourceClaimTemplate` for your rack. Each container that needs IMEX access must also declare the claim under `resources.claims`.

### Minimal example

> [!NOTE]
>
> Replace `[TEMPLATE-NAME]` with the name of the channel defined in your `ComputeDomain`, and replace `[IMAGE]` with your workload's container image.

```yaml theme={"system"}
apiVersion: v1
kind: Pod
metadata:
  name: imex-workload
  labels:
    app: imex-workload
spec:
  resourceClaims:
  - name: imex-channel
    resourceClaimTemplateName: [TEMPLATE-NAME]
  containers:
  - name: workload
    image: [IMAGE]
    resources:
      claims:
      - name: imex-channel
      requests:
        nvidia.com/gpu: 4
  affinity:
    podAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
      - labelSelector:
          matchExpressions:
          - key: app
            operator: In
            values:
            - imex-workload
        topologyKey: nvidia.com/gpu.clique
```

### Multi-node example: MPIJob across a full GB200 rack

For full-rack distributed workloads, the following example schedules an MPIJob across all Nodes of a GB200 rack using DRA IMEX.

> [!NOTE]
>
> This example requires the [MPI Operator](https://github.com/kubeflow/mpi-operator) installed in your cluster.

* `slotsPerWorker: 4` matches the 4 GPUs per Node on GB200 NVL72 systems.
* `replicas: 18` covers all Nodes in a single GB200 rack.
* The `topologyKey: nvidia.com/gpu.clique` affinity ensures all worker Pods land on Nodes within the same NVLink partition, as identified by GPU Feature Discovery.
* Replace `[IMEX-CHANNEL-TEMPLATE-NAME]` with the `spec.channel.resourceClaimTemplate.name` value from your `ComputeDomain`.

```yaml theme={"system"}
apiVersion: kubeflow.org/v2beta1
kind: MPIJob
metadata:
  name: dra-example-gb200-4x
spec:
  slotsPerWorker: 4
  runPolicy:
    cleanPodPolicy: Running
  mpiReplicaSpecs:
    Launcher:
      replicas: 1
      template:
        spec:
          containers:
            - image: ghcr.io/nvidia/k8s-samples:nvbandwidth-v0.7-8d103163
              name: mpi-launcher
              securityContext:
                runAsUser: 1000
              command: ["/bin/bash", "-c"]
              args:
                - sleep infinity
              resources:
                requests:
                  cpu: 2
                  memory: 128Mi
    Worker:
      replicas: 18
      template:
        metadata:
          labels:
            app: nvbandwidth-test-worker
        spec:
          resourceClaims:
          - name: imex-channel
            resourceClaimTemplateName: [IMEX-CHANNEL-TEMPLATE-NAME]
          containers:
            - image: ghcr.io/nvidia/k8s-samples:nvbandwidth-v0.7-8d103163
              name: nccl
              securityContext:
                privileged: false
              resources:
                claims:
                - name: imex-channel
                requests:
                  cpu: 110
                  memory: 960Gi
                  nvidia.com/gpu: 4
                limits:
                  memory: 960Gi
                  nvidia.com/gpu: 4
              volumeMounts:
                - mountPath: /dev/shm
                  name: dshm
          affinity:
            podAffinity:
              requiredDuringSchedulingIgnoredDuringExecution:
              - labelSelector:
                  matchExpressions:
                  - key: app
                    operator: In
                    values:
                    - nvbandwidth-test-worker
                topologyKey: nvidia.com/gpu.clique
          volumes:
            - emptyDir:
                medium: Memory
              name: dshm
```

### Verify resource allocation

After submitting a workload, verify that `ResourceClaims` are in `allocated,reserved` state by listing them in your namespace. Replace `[NAMESPACE]` with the namespace of your workload:

```bash theme={"system"}
kubectl get resourceclaim -n [NAMESPACE]
```

Expected output:

```text theme={"system"}
NAME                                     STATE                AGE
dra-example-gb200-4x-worker-0-imex-...   allocated,reserved   30s
dra-example-gb200-4x-worker-1-imex-...   allocated,reserved   30s
```

If claims remain unallocated, verify that:

* The `ComputeDomain` for your rack is active: `kubectl get computedomain -A`.
* The `resourceClaimTemplateName` in your Pod spec exactly matches an available `ResourceClaimTemplate`.
* All Pods are scheduled on Nodes within the same `nvidia.com/gpu.clique` domain.

## Troubleshoot IMEX

When IMEX is unhealthy, multi-node NVLink workloads stop responding at initialization or fail to import shared memory. Common symptoms:

* NCCL fails during initialization with a warning that MNNVL is available but not working. NCCL probes the fabric at startup by allocating memory with a fabric handle, then exporting and importing that handle with `cuMemExportToShareableHandle` and `cuMemImportFromShareableHandle`. Whichever step fails determines the message:

  ```text theme={"system"}
  MNNVL (cliqueSize 72) is available but not working on this system. Check the IMEX channel configuration (/dev/nvidia-caps-imex-channels). Set NCCL_MNNVL_ENABLE=0 to ignore this issue.
  MNNVL (cliqueSize 72) is available but not working on this system. Check the IMEX configuration (nvidia-imex-ctl -N). Set NCCL_MNNVL_ENABLE=0 to ignore this issue.
  ```

  The first means the Pod never received a channel device. Start with [Confirm the IMEX channel reached the Pod](#confirm-the-imex-channel-reached-the-pod). The second means the channel is present but the fabric handle couldn't cross Nodes, so start with [Read the fabric health status](#read-the-fabric-health-status).
* NCCL stops responding at initialization with no progress past communicator setup. This isn't an NCCL bug: NCCL is waiting on an NVLink memory fabric that was never established.
* The GPU fabric health status reports an active fault condition. See [Read the fabric health status](#read-the-fabric-health-status).

Work through the following checks in order. All four are safe to run and take a few minutes each. Together they distinguish a workload or scheduling problem you can fix from a platform fault that needs a support ticket.

### Read the fabric health status

Setting `NCCL_DEBUG` only adds logging and doesn't change collective behavior. Run the workload with NCCL debug logging enabled by prefixing your normal launch command with the debug environment variables. Replace `[WORKLOAD-COMMAND]` with the command you use to start the workload:

```bash theme={"system"}
NCCL_DEBUG=INFO NCCL_DEBUG_SUBSYS=INIT [WORKLOAD-COMMAND]
```

NCCL logs one Multi-Node NVLink (MNNVL) line per GPU during initialization:

```text theme={"system"}
NCCL INFO MNNVL busId 0x901000 fabric UUID 6b0a1f7c2d4e4b9a.9c3f1e2d3a4b5c6d cliqueId 0x7ffe state 3 healthMask 0xaa
```

Two fields matter:

**`state`** is the fabric registration state. `3` means registration completed. A value of `1` (not started) or `2` (in progress) means the GPU hasn't finished joining the fabric. Retry after the Node settles, and treat a persistent non-`3` state as a platform issue.

**`healthMask`** is a packed bitfield, not a count of healthy links. It holds six independent fields, and the polarity isn't uniform across them, so comparing the whole mask against a single expected number gets the diagnosis backwards. Decode it field by field instead:

```python decode_health_mask.py theme={"system"}
import sys

# Each condition occupies two bits: 0 is unreported, 1 is an active fault, 2 is healthy.
CONDITIONS = [
    ("Degraded bandwidth", 0),
    ("Route recovery in progress", 2),
    ("Route unhealthy", 4),
    ("Access timeout recovery", 6),
]

CONDITION_VALUES = {
    0: "not reported by this driver",
    1: "ACTIVE (fault)",
    2: "absent (healthy)",
}

# Bits 8-11 hold a four-bit configuration code. Only 0 and 1 are benign.
CONFIGURATION_VALUES = {
    0: "not reported by this driver",
    1: "no misconfiguration (healthy)",
    2: "incorrect SysGUID",
    3: "incorrect chassis serial number",
    4: "no partition",
    5: "insufficient NVLinks",
    6: "incompatible GPU firmware",
    7: "invalid location",
    8: "invalid GPU state",
}

# Bits 12-13 hold partition assignment, where 1 is the healthy value.
PARTITION_VALUES = {
    0: "not reported by this driver",
    1: "assigned (healthy)",
    2: "NOT ASSIGNED (fault)",
}


def decode(mask):
    for label, shift in CONDITIONS:
        value = (mask >> shift) & 0x3
        print(f"{label}: {CONDITION_VALUES.get(value, value)}")

    configuration = (mask >> 8) & 0xF
    print(f"Configuration: {CONFIGURATION_VALUES.get(configuration, configuration)}")

    partition = (mask >> 12) & 0x3
    print(f"Partition assignment: {PARTITION_VALUES.get(partition, partition)}")


if __name__ == "__main__":
    decode(int(sys.argv[1], 16))
```

Pass the `healthMask` value from your log line:

```bash theme={"system"}
python3 decode_health_mask.py 0x59a
```

```text theme={"system"}
Degraded bandwidth: absent (healthy)
Route recovery in progress: absent (healthy)
Route unhealthy: ACTIVE (fault)
Access timeout recovery: absent (healthy)
Configuration: insufficient NVLinks
Partition assignment: not reported by this driver
```

That example carries two distinct faults, and neither is visible by eye. A fully healthy fabric reads `0x11aa` on a driver that reports all six fields, or `0xaa` on one that reports only the first four.

> [!NOTE]
>
> An unreported field reads as `0`, so a low value such as `0x2` or `0x0` reflects limited driver reporting rather than a degraded fabric.

If you'd rather not decode the mask at all, the `Fabric` section of `nvidia-smi -q` reports the same information in labeled form. Check `Status: Success` alongside `State: Completed`, because NVML reports the two separately and a GPU can finish registration while carrying a failed status. For the full field definitions, see NVIDIA's [NVML fabric definitions](https://docs.nvidia.com/deploy/nvml-api/api/group__nvmlFabricDefs.html).

### Confirm all Pods share one NVLink domain

Cross-Node NVLink memory access works only when every Pod in the job lands on Nodes in the same NVLink domain. Show both placement labels for your GPU Nodes. This command is read-only and safe to run:

```bash theme={"system"}
kubectl get nodes -L ds.coreweave.com/nvlink.domain -L nvidia.com/gpu.clique
```

`ds.coreweave.com/nvlink.domain` is a globally unique rack identifier, such as `DH4-016-US-EAST-02A`. Every Pod in the job must show the same value. A job split across two values is split across two racks, and on CoreWeave NVL72 deployments there's no NVLink path between them.

`nvidia.com/gpu.clique` identifies the NVLink partition within a domain, and it's the label to use as a Pod affinity `topologyKey`. On CKS full-rack deployments, the default partition spans the whole domain, so on a healthy fabric the two labels change together. Check both: Nodes that share a `nvlink.domain` value but report different `gpu.clique` values indicate a partitioned fabric, which is a fault to report rather than a scheduling mistake. Use `gpu.clique` for scheduling and `nvlink.domain` to identify which physical rack your workload is running on. For the affinity mechanics, see [Claim IMEX channels from a ComputeDomain](#claim-imex-channels-from-a-computedomain).

> [!NOTE]
>
> A Pod whose `schedulerName` is a SUNK Pod Scheduler has its placement decided by Slurm, so `podAffinity`, `podAntiAffinity`, and `topologySpreadConstraints` have no effect and a `topologyKey` silently does nothing. Node affinity still applies. See [Known limitations](https://docs.coreweave.com/products/sunk/run_workloads/schedule-kubernetes-pods.md#known-limitations). Pods that use the default kube-scheduler are unaffected. To place Slurm jobs rather than Pods, see [Topology and block scheduling in Slurm](https://docs.coreweave.com/products/sunk/optimize_workloads/topology-scheduling.md), which builds its topology from the same `ds.coreweave.com/nvlink.domain` label.

### Confirm the IMEX channel reached the Pod

Co-location alone doesn't enable cross-Node NVLink. The Pod also needs an IMEX channel device, which the platform injects when the Pod holds a `ResourceClaim` against a `ComputeDomain`. Check inside a running GPU Pod. This command is read-only and safe to run. Replace `[NAMESPACE]` and `[POD-NAME]` with the namespace and name of the Pod you're checking:

```bash theme={"system"}
kubectl exec -n [NAMESPACE] [POD-NAME] -- ls /dev/nvidia-caps-imex-channels/
```

A Pod with a channel shows at least one entry, such as `channel0`. If the directory is missing or empty, no channel was allocated, and every multi-node NVLink operation in that Pod will fail regardless of fabric health. Check the claim wiring next. If the claim is allocated and the directory is still empty, the channel wasn't injected on the platform side, which is a fault to report rather than something to fix in your manifest.

### Confirm the ComputeDomain and ResourceClaim are bound

Inspect the `ComputeDomain`, its `ResourceClaim`, and the Pod together. These commands are read-only and safe to run:

```bash theme={"system"}
kubectl get computedomain -n [NAMESPACE]
kubectl get resourceclaims -n [NAMESPACE]
kubectl describe pod -n [NAMESPACE] [POD-NAME]
```

Confirm that a `ComputeDomain` exists in the workload's namespace, that a `ResourceClaim` derived from its `ResourceClaimTemplate` is `allocated` and reserved for your Pods, and that the Pod spec references that claim. A Pod that starts successfully without a claim will run. It just won't have NVLink across Nodes.

### Values that look wrong but are expected

Before treating a value as an error, rule out these expected results:

* **`nNodes 1` in NCCL logs.** NCCL treats an entire NVLink domain as a single virtual node, so a job running across all 18 Nodes of a GB200 or GB300 NVL rack reports `nNodes 1`. This is the correct value and confirms MNNVL is working, not that only one Node joined. NCCL counts NVLink domains here rather than physical hosts, so a job spanning two racks reports more than one node.
* **`healthMask 0x0` or another low value.** This usually means the driver reports few or none of the health conditions. Decode the individual fields before concluding anything.
* **A single Pod restart or reschedule.** Placement can change on reschedule. Re-verify Pod placement and `ComputeDomain` state before suspecting hardware.

### When to open a support ticket

Open a ticket when any of the following hold after you've worked through the checks above:

* Decoding `healthMask` reports any field as a fault, or `state` stays below `3`, on a job whose Pods all share one NVLink domain.
* `/dev/nvidia-caps-imex-channels/` is empty or missing even though the Pod holds an allocated `ResourceClaim` against a `ComputeDomain`.
* The failure persists after rescheduling the workload onto a fresh set of Nodes in the same domain.
* The rack was recently delivered and hasn't yet completed a successful multi-node NVLink job.

Alongside the details in [Support ticket templates](https://docs.coreweave.com/support/ticket-templates.md), include the following so the on-call engineer can skip re-deriving what you already found:

* The full `MNNVL` log line for each affected GPU, with the `state` and `healthMask` values verbatim.
* The affected Node names with their `ds.coreweave.com/nvlink.domain` and `nvidia.com/gpu.clique` label values.
* The output of the `ComputeDomain` and `ResourceClaim` checks, and the `ls /dev/nvidia-caps-imex-channels/` result.
* The job manifest, including the Pod affinity rules and the claim reference.
* The time the workload last succeeded, if it ever did.
