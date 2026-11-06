# SUNK Pod Scheduler

Source: https://docs.coreweave.com/products/sunk/discover_sunk/scheduler

# SUNK Pod Scheduler

> How the SUNK Pod Scheduler uses Slurm's scheduling mechanism to schedule Kubernetes Pods

[SUNK Standard](https://docs.coreweave.com/products/sunk.md)

[SUNK Self-Service](https://docs.coreweave.com/products/sunk/about-self-service-sunk.md)

This page explains how the SUNK Pod Scheduler integrates Slurm's scheduling mechanism with Kubernetes so that Pods and Slurm jobs share the same Nodes and lifecycle. Read it to understand how scheduling, preemption, and termination flow between the two systems before you configure workloads that depend on this behavior.

The SUNK Pod Scheduler uses the Slurm cluster's scheduling mechanism to schedule Kubernetes Pods. The scheduler places Pods on the same Kubernetes Nodes where the Slurm jobs run, and it can preempt Kubernetes workloads in favor of Slurm jobs on the same Node, or preempt Slurm jobs in favor of Pods, using the same logic. The SUNK Pod Scheduler also synchronizes Pod and Slurm job creation and deletion between Slurm and Kubernetes.

The SUNK Pod Scheduler reconciles Kubernetes workloads with events from the Slurm Controller. For standalone Pods, it updates the Pod and its associated Slurm job. For gang workloads, Job and LeaderWorkerSet (LWS) reconcilers manage shared allocations, while Pod reconciliation binds and cleans up individual members.

For general usage information, see [Using the SUNK Pod Scheduler](https://docs.coreweave.com/products/sunk/run_workloads/schedule-kubernetes-pods.md).

## Schedule flow

The following description explains how a standalone Pod moves from submission to a running state under the SUNK Pod Scheduler. For shared allocations, see [Gang scheduling flow](#gang-scheduling-flow).

When a Pod is marked to schedule through the SUNK Pod Scheduler (`.spec.schedulerName`), the SUNK Pod Scheduler processes the Pod and attempts to schedule it. The SUNK Pod Scheduler validates the Pod to confirm the annotations can be passed to the Slurm Controller through RPC. It doesn't validate that the values are correct, only that they can be passed. It also verifies that the resource requests are non-zero.

Validation errors block the retry of scheduling, and the scheduler creates an event on the Pod for the reason.

> [!NOTE]
>
> A Slurm job isn't considered running until it completes the [Prolog stage](https://docs.coreweave.com/products/sunk/run_workloads/prolog-epilog.md) and the placeholder job script starts. The script appends `: started` to `SLURM_JOB_EXTRA` when it starts. The SUNK Pod Scheduler uses Node locking to ensure Nodes are ready for the placeholder jobs. This process is similar to normal Slurm jobs, but with strict checking.

To schedule a standalone Pod, the reconciler processes the Pod object at least twice. The first pass creates the job and propagates the ID back to the Pod. If the job is in the running state, the second pass schedules the Pod.

> [!NOTE]
>
> The SUNK Pod Scheduler reads `gpu.nvidia.com/class` from required node affinity to select a Slurm GPU type. It doesn't evaluate other node-affinity rules or Kubernetes taints when choosing a node. Kubernetes can still reject a bound Pod because of resource or admission constraints.

## Gang scheduling flow

SUNK supports fixed-size gang scheduling starting with 7.6.0 in the 7.x series and 8.2.0 in the 8.x series. A Kubernetes Job uses one shared multi-node Slurm allocation. Each LeaderWorkerSet replica group uses a separate allocation.

The workload reconciler owns allocation submission, the Slurm job ID record, finalizers, and teardown. It waits for all expected member Pods before submitting one Slurm job that requests one node per member. It records the allocation on the workload and publishes the Slurm job ID to its Pods.

The Pod reconciler waits for that allocation to run, then binds each member to a distinct allocated node. It handles member cleanup without submitting or canceling the gang's shared allocation. This separates an individual Pod's lifecycle from the lifetime of the workload's allocation.

When a Job finishes or a workload is deleted, the workload reconciler cancels its recorded allocations. An LWS scale-down cancels the allocations for removed replica groups. The reconciler releases the workload finalizer after allocation teardown completes.

For complete examples and the limits on resizing and resource updates, see [Run workloads with gang scheduling](https://docs.coreweave.com/products/sunk/run_workloads/gang-scheduling.md).

## Unschedule flow

The following description explains how the SUNK Pod Scheduler tears down a standalone Pod when either side initiates termination. For gang workloads, the workload reconciler manages the shared allocation.

The SUNK Pod Scheduler handles both Pod deletion and Slurm job cancellation flows, so you can stop the workload from either Kubernetes or Slurm.

When the placeholder job receives a termination signal, it contacts the SUNK Pod Scheduler's hook API and blocks until the Pod is deleted. This prevents Slurm from running another job before the Kubernetes Pod is fully deleted. If the Pod is still running just before `KillWait` is reached, the script [places the Node into Drain](https://docs.coreweave.com/products/sunk/manage_sunk/drain-and-undrain-nodes.md). This prevents scheduling further workloads on the Node until you resolve the issue. After the `KillWait` timeout value is reached, Slurm forcibly terminates the job.

Because the SUNK Pod Scheduler validates `terminationGracePeriodSeconds` when scheduling Pods, the Node is unlikely to be drained as a result of the Pod taking too long to delete.
