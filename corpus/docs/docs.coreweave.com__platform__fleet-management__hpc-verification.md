# HPC Verification

Source: https://docs.coreweave.com/platform/fleet-management/hpc-verification

# HPC Verification

> Proactive tests that check idle Nodes for silent data corruption and performance regressions

HPC Verification is a proactive, on-Node testing framework that validates hardware and driver integrity beyond what passive monitoring can detect. This system runs automatically on idle compute Nodes to catch and fix issues such as silent data corruption, performance regressions, and thermal deficiencies before they affect customer workloads.

HPC Verification is a fleet-wide safeguard that underpins the CoreWeave SLA by ensuring your AI workloads run on reliable infrastructure. This test identifies hardware or driver issues that passive monitoring alone can't detect. It includes checks for:

* **Silent data corruption**: Detects memory errors that do not trigger standard system alerts.
* **Numerical performance regression**: Benchmarks common deep-learning kernels (FP8, FP16, BF16) to detect slowdowns.
* **Thermal deficiencies**: Runs all streaming multiprocessors at 100% load for approximately 20 minutes to uncover thermal issues.

These active tests complement CoreWeave's passive telemetry collection by identifying and remediating issues before they affect customer workloads. They are a key part of CoreWeave's infrastructure lifecycle management, helping maintain reliability and performance for your AI workloads. Because they run only on idle Nodes and stop as soon as a customer workload is scheduled, they don't interfere with your jobs. Third-party schedulers, Pods pinned to a Node with `.spec.nodeName`, and work started outside Slurm on SUNK clusters are exceptions. See [Test schedule](#test-schedule), [Why is my Pod stuck in pending on CKS?](https://docs.coreweave.com/support/cks/articles/why-is-my-pod-stuck-in-pending), and [Preemption on SUNK clusters](#preemption-on-sunk-clusters). A transient `hpc-verification` Pod in your cluster is a test that ran on an idle Node or was preempted to make way for your job.

HPC Verification is separate from Node Health Check (NHC).

SUNK runs [Node Health Check (NHC)](https://github.com/mej/nhc) as one of the scripts in the Epilog chain after a job, and only when no other job is still running on the node. A failed check drains the node with a reason that begins with `NHC:`.

A passing HPC Verification test is what returns a node whose drain reason carries `sunk:verify-undrain` to service. See [Node Health Check (NHC) drains](https://docs.coreweave.com/products/sunk/manage_sunk/drain-and-undrain-nodes.md#node-health-check-nhc-drains).

## Test schedule

At the top of each hour, if a Node is idle, meaning no customer Pod holds any of its GPUs, CoreWeave runs a 20- to 30-minute verification test. This rule is narrower than the [idle status](https://docs.coreweave.com/products/cks/nodes/nodes-and-node-pools.md#idle-nodes) CKS uses for maintenance, which also counts Pods that don't hold GPUs. This test uses all GPUs and available InfiniBand resources to exercise the hardware uniformly without interrupting your jobs. The `hpc-verification` Pods run at a low Kubernetes priority class to allow preemption and avoid blocking customer workloads. If the Node is not idle, CoreWeave skips the test and retries at the next hour mark.

Third-party schedulers don't preempt verification Pods by default, because those Pods are placed by the `default-scheduler`. Respecting Kubernetes PriorityClasses isn't sufficient on its own. If you run a third-party scheduler such as Volcano or the KAI Scheduler, see [Custom schedulers and third-party integrations](https://docs.coreweave.com/products/cks/clusters/scheduling/custom-schedulers.md), and contact CoreWeave before you run it on a production cluster. CoreWeave's [`cks-kueue` chart](https://docs.coreweave.com/products/cks/clusters/coreweave-charts/kueue) integrates with HPC Verification natively, so it doesn't need this coordination. [Contact CoreWeave Support](https://support.freshdesk.com/support/home) or email `support@coreweave.com` if you have questions about HPC Verification and how it interacts with your scheduler.

## Taints

Use `NoSchedule` taints to keep Pods without matching tolerations off GPU Nodes while allowing automated HPC Verification to run. Verification Pods tolerate arbitrary `NoSchedule` and `PreferNoSchedule` taints, but they don't tolerate arbitrary `NoExecute` taints.

Each verification run starts a controller Pod that schedules the test Pods. In CKS customer clusters, the controller also tolerates arbitrary `NoSchedule` taints. A GPU-only cluster doesn't need an untainted Node for the controller. The controller must be able to schedule before any tests can start. If it remains `Pending`, see [The verification controller Pod stays Pending](https://docs.coreweave.com/support/platform/articles/troubleshoot-hpc-verification#the-verification-controller-pod-stays-pending).

A `NoExecute` taint can prevent a verification Pod from scheduling or evict it after it starts. This affects verification in two ways:

* **Idle Nodes**: Automated verification can't run, so the Node remains unverified even when no customer workloads are running.
* **Rebooted Nodes**: The Node returns to `production` without waiting for verification, so a blocked test leaves it unverified rather than holding it back. A Node can still remain in `production-powerreset` or `production-reboot`. CoreWeave might delete and replace a Node that remains in this state too long.

Choose the taint effect based on the scheduling behavior you need:

| Taint effect | Effect on Pods without a matching toleration | Automated HPC Verification |
| :- | :- | :- |
| `NoSchedule` | Prevents new Pods from scheduling. Doesn't evict existing Pods. | Can run. Recommended for keeping new workloads off a Node. |
| `PreferNoSchedule` | Discourages new Pods from scheduling, but doesn't prevent them. Doesn't evict existing Pods. | Can run. Use when a scheduling preference is sufficient. |
| `NoExecute` (Do not use.) | Prevents new Pods from scheduling and evicts existing Pods. | Blocked by arbitrary customer-applied taints. |

If you apply a `NoExecute` taint, change its effect to `NoSchedule` in the Node or Node Pool configuration that manages the taint. Check that your workload tolerations still match the intended taint effect. Leave CoreWeave-managed taints unchanged. See [User taints](https://docs.coreweave.com/products/cks/clusters/scheduling/workload-scheduling.md#user-taints).

A rebooted Node returns to `production` as soon as the reboot completes, and the verification test runs after that. Let the test finish before scheduling workloads onto the Node: the test needs the Node's GPUs free, so a workload that lands first prevents it from starting, and one that lands mid-test stops it. For a Node that remains in a reboot state, see [Reboot troubleshooting](https://docs.coreweave.com/products/cks/nodes/reboot.md#the-node-stays-in-production-powerreset).

## Verify a Node on demand

Use the CoreWeave Intelligent CLI to request verification of a specific GPU Node without waiting for the hourly test. The Node must be idle, with no customer Pod holding any of its GPUs.

Before you begin, [install and authenticate the CoreWeave Intelligent CLI](https://docs.coreweave.com/products/cks/nodes/manage.md#use-coreweave-intelligent-cli) and configure access to the Node's cluster. Check `NoExecute` taints and follow the guidance in [Taints](#taints).

Replace `[NODE-NAME]` with the name of the Node to verify:

```bash theme={"system"}
cwic node verify [NODE-NAME]
```

Allow approximately 35 minutes for verification. View the results in the [Node Details dashboard](https://cks-grafana.coreweave.com/d/ddbdicm9sw7c5x/node-details). After a reboot, also confirm that the Node has returned to the `production` lifecycle state before resuming workloads. See [Monitor the reboot](https://docs.coreweave.com/products/cks/nodes/reboot.md#monitor-the-reboot).

If verification doesn't complete or the Node remains unavailable, [contact CoreWeave Support](https://docs.coreweave.com/support.md). Include the cluster name, Node name, taints, and approximate time of the verification request.

## Troubleshoot verification

If tests don't start or the controller Pod remains `Pending`, see [Troubleshoot HPC Verification](https://docs.coreweave.com/support/platform/articles/troubleshoot-hpc-verification).

## Customer impact

HPC Verification jobs are **not billable** and don't appear in usage reports. They run only when Nodes are idle, so a workload that Kubernetes or Slurm schedules never shares GPU resources with a test. If you launch a workload that needs the GPUs a test holds, the test stops, and CoreWeave releases resources before your Pod starts running. Your job and the test never run at the same time. Three cases work differently. A workload placed by a [third-party scheduler](#test-schedule) doesn't stop the test, so the workload waits in `Pending` until the test ends. A Pod pinned to a Node with `.spec.nodeName` bypasses the scheduler, so it can't preempt the test and can fail to start on a Node that looks free. See [Why is my Pod stuck in pending on CKS?](https://docs.coreweave.com/support/cks/articles/why-is-my-pod-stuck-in-pending). On SUNK clusters, work that you start outside Slurm, such as a process launched over SSH, can run on the same GPUs as a test. See [Preemption on SUNK clusters](#preemption-on-sunk-clusters).

## Preemption on SUNK clusters

On a SUNK cluster, Slurm stops a verification test when it allocates a node for a job. When Slurm allocates a node for a job submitted with `srun`, `salloc`, or `sbatch`, SUNK applies the `sunk.coreweave.com/lock` taint during the job's Prolog and evicts every Pod that doesn't tolerate it, including verification Pods. See [The SUNK `/lock` taint](https://docs.coreweave.com/products/cks/clusters/scheduling/workload-scheduling#the-sunk-/lock-taint).

Work that you start on a compute node outside Slurm, such as a process launched from an SSH session on a node where you hold no job, doesn't run the Prolog. The Node still looks idle to Kubernetes and Slurm, so a verification test can start on it while your process runs. This has two effects:

* If you run `nvidia-smi` on a compute node that you reached over SSH without an allocation, you might see GPU utilization and GPU memory usage from a verification test, even though no Slurm job is running.
* Your process and the test compete for the same GPUs, which can cause the Node to fail verification.

Run all compute work on SUNK through `srun`, `salloc`, or `sbatch`, including interactive sessions. SSH to a node where you already hold an allocation doesn't cause this conflict, because that job's Prolog has already applied the lock. SUNK removes the lock once no Slurm job is running on the node, so stop any process that you started over SSH before your job ends. See [Access Slurm compute nodes](https://docs.coreweave.com/products/sunk/access_sunk/access-slurm-compute-nodes.md).

## Identify the test

Use the following signals to confirm that an `hpc-verification` Pod or metric spike on your Node comes from HPC Verification rather than a customer workload.

You might briefly see a Pod whose name starts with `hpc-verification-` (single-Node tests) or `hpcv-mpi-` (multi-Node group tests) in `kubectl get pods -A` while the test runs. The test Pods run in the `cw-hpc-verification` namespace and use a CoreWeave PriorityClass with a negative value: `cw-hpc-verification` at `-1`, or `cw-hpc-validation` at `-50` on clusters where CoreWeave has rolled out the new class. Either way, they run at a lower priority than customer workloads that use the default priority.

While the test is running, you might notice short spikes in your Grafana dashboards for:

* **GPU SM Utilization**: Measures how heavily the GPU cores are used.
* **CPU Utilization**: Shows CPU usage during the test.
* **GPU Memory Utilization**: Tracks GPU memory usage.

These metrics confirm that the test uniformly exercises every GPU on the Node.

## Key points

* HPC Verification tests can't be disabled. They are a core safeguard that supports the CoreWeave SLA.
* You might briefly see an `hpc-verification-*` Pod in `kubectl get pods -A`. This means the test is running on an idle Node. Kubernetes preempts it as soon as your workload starts, unless a [third-party scheduler](https://docs.coreweave.com/products/cks/clusters/scheduling/custom-schedulers.md) places your workload or the Pod is pinned to the Node with `.spec.nodeName`. On SUNK clusters, work started outside Slurm doesn't preempt it. See [Preemption on SUNK clusters](#preemption-on-sunk-clusters).
* These tests aren't billed and don't appear in usage reports.

If you think HPC Verification has cordoned a Node in your cluster or delayed your job, email `support@coreweave.com`. Include the cluster name, Node name (from `kubectl describe node`), and the approximate time. The CoreWeave team checks and, if needed, uncordons or replaces the Node to restore capacity.
