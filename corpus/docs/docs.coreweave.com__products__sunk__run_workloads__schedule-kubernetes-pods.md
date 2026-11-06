# Schedule Kubernetes Pods with the SUNK Pod Scheduler

Source: https://docs.coreweave.com/products/sunk/run_workloads/schedule-kubernetes-pods

# Schedule Kubernetes Pods with the SUNK Pod Scheduler

> Schedule Kubernetes Pods alongside Slurm jobs using the SUNK Pod Scheduler

[SUNK Standard](https://docs.coreweave.com/products/sunk.md)

[SUNK Self-Service](https://docs.coreweave.com/products/sunk/about-self-service-sunk.md)

The SUNK Pod Scheduler lets you run Kubernetes Pods alongside Slurm jobs in the same cluster. Instead of managing separate clusters for different workload types, you can run training with Slurm and inference with Kubernetes on shared nodes.

The SUNK Pod Scheduler creates placeholder Slurm jobs so that Slurm manages node placement, GPU allocation, and resource tracking for Kubernetes workloads. Standalone Pods use one placeholder job per Pod. With gang scheduling, a Kubernetes Job or LeaderWorkerSet replica group shares one multi-node Slurm allocation.

This page walks through how to enable the scheduler, configure a Pod to use it, choose a node sharing strategy, and the annotations and limitations you should know about. It's intended for cluster operators and workload owners who want to consolidate Slurm and Kubernetes workloads on shared infrastructure.

## Enable the scheduler

Before you can submit Pods to the SUNK Pod Scheduler, you must enable it in the Slurm Helm chart and tell it which namespaces to watch.

Set `scheduler.enabled` to `true` in your Slurm Helm chart values:

```yaml theme={"system"}
scheduler:
  enabled: true
```

Configure the scheduler's scope to watch the namespaces where you create your Pods:

* To monitor the entire cluster, set `scheduler.scope.type` to `cluster`.
* To monitor specific namespaces, set `scheduler.scope.type` to `namespace` and set `scheduler.scope.namespaces` to a comma-separated list of namespaces. If `scheduler.scope.namespaces` is blank, the scheduler defaults to the namespace where it's deployed.

## Configure a Pod for scheduling

With the scheduler enabled, each Pod that targets it needs three pieces of configuration: the scheduler name, resource requests, and a valid termination grace period. The following sections describe each requirement.

### Set the scheduler name

In your Pod's `spec`, set `schedulerName` to the name of your SUNK Pod Scheduler so Kubernetes routes the Pod to SUNK instead of the default scheduler. A Pod whose `schedulerName` matches no running scheduler stays `Pending` with no error, so read the name from your cluster rather than deriving it. See [Look up the scheduler configuration](#look-up-the-scheduler-configuration).

On SUNK 8.0 and later, the name defaults to the `SlurmCluster` resource name followed by `-scheduler`. That's the Helm release name on SUNK Standard, or the `SunkCluster` name on SUNK Self-Service, so a release named `slurm` gives `slurm-scheduler`.

On SUNK Standard, set [`scheduler.config.scheduler.name`](https://docs.coreweave.com/products/sunk/reference/slurm-parameters#scheduler--config--scheduler) in your Helm values to choose the name yourself. SUNK Self-Service has no equivalent setting: [`spec.scheduler`](https://docs.coreweave.com/products/sunk/reference/sunkcluster-reference#schedulerconfig) on the `SunkCluster` resource only enables the scheduler, so the name always follows the default.

> [!NOTE]
>
> On SUNK 7.x the default is `[NAMESPACE]-[RELEASE-NAME]-scheduler` and the override key is `scheduler.name`. SUNK 8.0 dropped the namespace prefix, so a `schedulerName` that worked on 7.x no longer matches any scheduler after the upgrade. See the [SUNK v8.0.0 release note](https://docs.coreweave.com/release-notes/sunk-8-0.md).

### Set resource requests

Your Pod must request specific CPU and memory resources so Slurm can account for the Pod against node capacity. If these resource requests are missing or zero, the Pod fails to schedule.

### Set the termination grace period

Set `terminationGracePeriodSeconds` to a value strictly less than the scheduler's Slurm kill-wait value minus its termination offset. The scheduler receives the kill-wait value through its `--slurm-kill-wait` argument, which should match the Slurm [`KillWait`](https://docs.coreweave.com/products/sunk/reference/slurm-parameters#slurmConfig) setting that limits [Pod teardown](https://docs.coreweave.com/products/sunk/discover_sunk/scheduler.md) when a placeholder job ends. The defaults are 30 seconds and 5 seconds, respectively, so `terminationGracePeriodSeconds` must be less than 25 with the default configuration. This keeps Kubernetes Pod termination aligned with Slurm's job termination window so the placeholder job and the Pod tear down cleanly.

> [!WARNING]
>
> The Kubernetes default `terminationGracePeriodSeconds` is 30 seconds, which exceeds the default threshold of 25 seconds. You must explicitly set this value on your Pod spec. A typical value is `5` to `20`.

### Look up the scheduler configuration

Use the procedure for your SUNK version to find the scheduler name and termination settings. Replace `[SCHEDULER-NAMESPACE]` with the namespace where the scheduler runs.

For SUNK 7.x, inspect the scheduler container's arguments:

```bash theme={"system"}
kubectl get pods -n "[SCHEDULER-NAMESPACE]" \
  -l app.kubernetes.io/name=sunk-scheduler \
  -o jsonpath='{.items[0].spec.containers[?(@.name=="scheduler")].args}{"\n"}'
```

Read `--scheduler-name` and `--slurm-kill-wait` in the output. The 7.x Helm chart sets the scheduler name to `[NAMESPACE]-[RELEASE-NAME]-scheduler` unless you override `scheduler.name`. If the scheduler argument is absent in a custom deployment, the executable defaults to `sunk-scheduler`.

For SUNK 8.x, the operator names the scheduler `[SLURM-CLUSTER-NAME]-scheduler`, where `[SLURM-CLUSTER-NAME]` is the name of the `SlurmCluster` resource. List the resources in the scheduler namespace to find it:

```bash theme={"system"}
kubectl get slurmclusters -n "[SCHEDULER-NAMESPACE]"
```

If a Pod that uses that name stays `Pending` with no scheduler events, the name might be overridden through `scheduler.config.scheduler.name`. The deployment doesn't expose the name through `--scheduler-name`, so read the effective value from the `scheduler.conf` ConfigMap entry:

1. Find the scheduler Pod's configuration ConfigMap:

   ```bash theme={"system"}
   kubectl get pods -n "[SCHEDULER-NAMESPACE]" \
     -l app.kubernetes.io/name=sunk-scheduler \
     -o jsonpath='{.items[0].spec.volumes[?(@.name=="config")].configMap.name}{"\n"}'
   ```

2. Replace `[SCHEDULER-CONFIGMAP]` with that name and read the configuration:

   ```bash theme={"system"}
   kubectl get configmap "[SCHEDULER-CONFIGMAP]" -n "[SCHEDULER-NAMESPACE]" \
     -o jsonpath='{.data.scheduler\.conf}{"\n"}'
   ```

Use `scheduler.name` from the output as the workload's `schedulerName`. To find `--slurm-kill-wait`, inspect the scheduler Pod's arguments with the command shown for SUNK 7.x. The configuration can override `scheduler.terminationOffset`, whose default is `5s`.

### Example Pod

This example shows a full-node GPU Pod with all three required settings:

```yaml theme={"system"}
apiVersion: v1
kind: Pod
metadata:
  name: slurm-test
  namespace: tenant-slurm-staging
  annotations:
    sunk.coreweave.com/account: root
    sunk.coreweave.com/comment: "A Kubernetes job"
    sunk.coreweave.com/exclusive: "none"
spec:
  schedulerName: slurm-scheduler
  containers:
    - name: main
      image: ubuntu
      command:
        - /bin/bash
      args:
        - -c
        - sleep infinity
      resources:
        limits:
          memory: 960Gi
          rdma/ib: "1"
          nvidia.com/gpu: "8"
        requests:
          cpu: "10"
          memory: 10Gi
          nvidia.com/gpu: "8"
  terminationGracePeriodSeconds: 5
  affinity:
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
          - matchExpressions:
              - key: gpu.nvidia.com/class
                operator: In
                values:
                  - H100_NVLINK_80GB
```

For GPU Pods, set required node affinity for `gpu.nvidia.com/class` with the `In` operator and one GPU class value, as shown in the example. SUNK maps that class to a Slurm GPU type through `scheduler.gpuTypes`. The CPU, memory, and GPU values in this example are illustrative. Adjust them based on your node type and `slurmd` configuration. For guidance, see [Check available resources](https://docs.coreweave.com/products/sunk/run_workloads/manage-scheduler-resources.md#check-available-resources).

## Choose a node sharing strategy

After the Pod has the required fields, decide how it shares nodes with other workloads. The `sunk.coreweave.com/exclusive` annotation controls this behavior, and the right value depends on your workload:

| Workload type | Annotation | Effect |
| - | - | - |
| Pod needs the entire node (all GPUs, or full CPU node) | `exclusive: "none"` | Full node isolation. No other jobs can share the node. |
| Multiple Pods or jobs share a node (partial GPUs, or CPU pool) | `exclusive: "user"` | Jobs from the same Slurm user can share the node. |
| CPU-only Pod can share a node with any workload | `exclusive: "ok"` | Open sharing with any user or account. Don't use this for GPU Pods. See [Known limitations](#known-limitations). |

For detailed guidance on each scenario, including resource configuration and examples, see [Manage resources with the SUNK Pod Scheduler](https://docs.coreweave.com/products/sunk/run_workloads/manage-scheduler-resources.md).

## Annotations reference

These annotations configure Slurm job parameters for SUNK-scheduled Pods. All annotations are optional.

| Annotation | Type | Description | Example |
| - | - | - | - |
| `sunk.coreweave.com/account` | string | Slurm account for the job. List accounts with `sacctmgr list account`. | `"root"` |
| `sunk.coreweave.com/wckey` (v8.1.0+) | string | Slurm workload characterization key. Groups job usage in `sacct` and `sreport` independently of the account and user hierarchy. | `"training"` |
| `sunk.coreweave.com/comment` | string | Descriptive comment to add to the Slurm job. | `"A Kubernetes job"` |
| `sunk.coreweave.com/constraints` | string | Node constraints for job placement. See the [Slurm sbatch documentation](https://slurm.schedmd.com/sbatch.html#OPT_constraint) for syntax. | |
| `sunk.coreweave.com/exclusive` (v5.7.0+) | string | Controls node sharing. See [Exclusive annotation values](https://docs.coreweave.com/products/sunk/run_workloads/manage-scheduler-resources.md#exclusive-annotation-values). | `"none"`, `"ok"`, `"user"`, `"mcs"`, `"topo"` |
| `sunk.coreweave.com/exclusive` (before v5.7.0) | boolean | Enables exclusive mode. See the [Slurm exclusive documentation](https://slurm.schedmd.com/sbatch.html#OPT_exclusive). | `"true"` |
| `sunk.coreweave.com/excluded-nodes` | string | Comma-separated Slurm node names to exclude. | `"a100-092-01,a100-092-02"` |
| `sunk.coreweave.com/required-nodes` | string | Comma-separated Slurm node names required. | `"a100-092-04,a100-092-06"` |
| `sunk.coreweave.com/partition` | string | Slurm partition to submit the job to. | `"default"` |
| `sunk.coreweave.com/prefer` | string | Node preferences. See [Slurm prefer documentation](https://slurm.schedmd.com/sbatch.html#OPT_prefer). | |
| `sunk.coreweave.com/priority` | integer | Job priority value. Must be an integer. | `"100"` |
| `sunk.coreweave.com/qos` | string | Quality of Service level. | `"normal"` |
| `sunk.coreweave.com/reservation` | string | Slurm reservation name. | `"test"` |
| `sunk.coreweave.com/segment` (v7.6.0+, v8.1.0+) | integer | Topology segment size in nodes. For gang workloads, set it on the Pod templates. Not available on v8.0.x. Must be a whole number. Any other non-empty value fails the placeholder Slurm job submission: the Pod stays Pending, and its events show `SlurmJobSubmitFailed` with `invalid segment value`. See [Configure topology segments](https://docs.coreweave.com/products/sunk/run_workloads/gang-scheduling.md#optional-configure-topology-segments). | `"2"` |
| `sunk.coreweave.com/user-id` | integer | User ID to run the job as. | `"1001"` |
| `sunk.coreweave.com/group-id` | integer | Group ID to run the job as. | `"1002"` |
| `sunk.coreweave.com/current-working-dir` | string | Working directory path for the job. | `"/path/to/use"` |
| `sunk.coreweave.com/timeout` | integer | Time limit in minutes for the Slurm placeholder job. | `"123"` |

> [!WARNING]
>
> * Invalid annotation values cause the Pod to fail scheduling.
> * Changes to annotations after a Pod is scheduled don't affect the running job.
> * The Slurm job defaults to the root user (uid=0, gid=0). If you set `user-id` without `group-id`, the group ID is set to the user ID value.

## Time limits

The `sunk.coreweave.com/timeout` annotation sets the Slurm placeholder job's time limit in minutes. Slurm enforces this limit on the allocation. SUNK binds Pods only after the placeholder job is running, so Pod initialization can consume part of the allocation's runtime. For a gang workload, the limit applies to the shared allocation.

## Known limitations

Before relying on the SUNK Pod Scheduler for production workloads, review the following constraints so you can plan around them.

* **Fixed-size gang scheduling.** SUNK supports Kubernetes Jobs and LeaderWorkerSet replica groups starting with 7.6.0 in the 7.x series and 8.2.0 in the 8.x series. Each gang shares one Slurm allocation with one node per Pod. Standalone Pods and unsupported controllers continue to use one placeholder per Pod. For lifecycle limitations, see [Gang scheduling limitations and lifecycle](https://docs.coreweave.com/products/sunk/run_workloads/gang-scheduling.md#limitations-and-lifecycle).
* **No bin-packing.** Slurm doesn't fill partially used nodes before moving to idle ones. This can spread Pods across nodes and lead to GPU fragmentation, especially during scaling.
* **Kubernetes placement constraints are limited.** `podAffinity`, `podAntiAffinity`, and `topologySpreadConstraints` have no effect. Slurm makes node placement decisions. SUNK reads `gpu.nvidia.com/class` from required node affinity for GPU-type selection; it doesn't apply other node-affinity rules.
* **Static CPU allocation causes node drains.** A container triggers Kubernetes static CPU pinning only when it belongs to a Guaranteed QoS Pod and requests a whole number of CPUs. With container-level resource settings, Guaranteed QoS requires every container to have positive CPU and memory requests equal to its corresponding limits. Pinning conflicts with Slurm's CPU accounting and creates resource contention, which leads to node drains in Slurm. Breaking either condition prevents it. For details and prevention steps, see [Static CPU allocation and the SUNK Pod Scheduler](https://docs.coreweave.com/products/sunk/run_workloads/static-cpu-allocation.md).
* **Non-SUNK Pods are invisible to Slurm.** Slurm can't see Pods scheduled through the standard Kubernetes scheduler. Running non-DaemonSet Pods on Slurm nodes without the SUNK Pod Scheduler can cause resource conflicts and unexpected node drains.
* **Taints may conflict with Slurm placement.** The SUNK Pod Scheduler doesn't evaluate Kubernetes taints. If Slurm places a Pod on a node with a conflicting taint, the kubelet rejects the Pod. Check Pod events with `kubectl describe pod` if a Pod is stuck.
* **Only a fixed set of exclusive values is valid.** On SUNK v5.7.0 and later, the `sunk.coreweave.com/exclusive` annotation accepts only `none`, `ok`, `user`, `mcs`, or `topo`. Any other non-empty value makes the placeholder Slurm job submission fail, so the Pod appears briefly and then vanishes. See [Exclusive annotation values](https://docs.coreweave.com/products/sunk/run_workloads/manage-scheduler-resources.md#exclusive-annotation-values).
* **GPU Pods can collide with Slurm GRES under open sharing.** Setting `exclusive: "ok"` on a GPU Pod opens the node to any job and can collide with Slurm's GRES accounting. Use `exclusive: "none"` for full-node GPU Pods or `exclusive: "user"` with a dedicated `user-id` for partial-GPU Pods.
* **Admission mismatch causes `OutOfcpu` or `OutOfmemory`.** Slurm and Kubernetes account for resources independently. System Pods, DaemonSets, and the `slurmd` container consume Kubernetes-allocatable capacity that Slurm doesn't see, so the kubelet can reject a Pod that Slurm placed. Right-size Pod requests below node allocatable. See [Reserve resources for system Pods](https://docs.coreweave.com/products/sunk/run_workloads/manage-scheduler-resources.md#reserve-resources-for-system-pods).
* **Duplicate volume declarations break mounts.** Declaring the same PersistentVolumeClaim (PVC) as two separate volume entries in one Pod spec, a common mistake with LeaderWorkerSet and templated workloads, can silently break `subPath` mounts. Declare each PVC once in `volumes` and reference it with multiple `volumeMounts`.

## Troubleshoot a SUNK-scheduled Pod

If a SUNK-scheduled Pod is rejected after scheduling, vanishes right after it appears, or collides with a Slurm job over GPUs, see [Troubleshoot a SUNK-scheduled Kubernetes Pod](https://docs.coreweave.com/support/sunk/articles/why-does-my-sunk-scheduled-pod-fail-to-start) for symptom-based diagnosis and recovery steps.

## Next steps

Use the following guides to configure your workloads:

* [Run workloads with gang scheduling](https://docs.coreweave.com/products/sunk/run_workloads/gang-scheduling.md) for Kubernetes Job and LeaderWorkerSet examples with shared Slurm allocations.
* [Manage resources with the SUNK Pod Scheduler](https://docs.coreweave.com/products/sunk/run_workloads/manage-scheduler-resources.md) for node sharing configuration, resource tuning, and GPU allocation guidance.
