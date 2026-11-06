# Node locking

Source: https://docs.coreweave.com/products/sunk/discover_sunk/node-locking

# Node locking

> How SUNK locks Kubernetes Nodes to prevent other workloads during active Slurm job execution

[SUNK Standard](https://docs.coreweave.com/products/sunk.md)

[SUNK Self-Service](https://docs.coreweave.com/products/sunk/about-self-service-sunk.md)

This page explains how SUNK uses Node locking to prevent Kubernetes workloads from running on a Node while a Slurm job is active. It's intended for cluster administrators and operators who need to understand how SUNK coordinates resource ownership between Slurm and Kubernetes.

Because a [`slurmd` Pod](https://docs.coreweave.com/products/sunk/discover_sunk/nodeset) is idle when the Slurm node is idle, other Kubernetes workloads may schedule on the Kubernetes Node. However, when the `slurmd` Pod becomes active, Kubernetes must evict the Kubernetes workloads to prevent resource allocation and deallocation race conditions between Slurm and Kubernetes. To verify eviction completes before the Slurm job starts, the Pod communicates the Node's workload state.

## Operation overview

SUNK contains a built-in [Prolog script](https://docs.coreweave.com/products/sunk/run_workloads/prolog-epilog.md) that verifies the Kubernetes Nodes are ready for Slurm Jobs, and locks the Nodes from accepting additional Kubernetes workloads before the job starts. The Prolog script calls the [Syncer's](https://docs.coreweave.com/products/sunk/discover_sunk/syncer.md) hook API, which then triggers a set of state updates through the [Pod Controller](https://docs.coreweave.com/products/sunk/discover_sunk/pod-controller.md) and [Node Controller](https://docs.coreweave.com/products/sunk/discover_sunk/node-controller.md) to complete the process. Both normal Slurm jobs and placeholder jobs created by the [SUNK Pod Scheduler](https://docs.coreweave.com/products/sunk/discover_sunk/scheduler.md) use this Prolog script.

### Node locking taints and annotations

In this process, SUNK uses Kubernetes taints and annotations to facilitate the desired behavior.

The taint key used on the Node is `sunk.coreweave.com/lock`.

The Pod annotation uses the same key as the Node taint, with the following values:

* `false`
* `pending`
* `locked`
* `locked_strict`

The check for other workloads finds all Pods that don't tolerate the taint, since the Node may have workloads that remain running, such as DaemonSets that handle logging. Two levels of checks facilitate locks for Slurm, versus locks for Kubernetes workloads scheduled through Slurm.

Slurm jobs use normal locking, while SUNK Pod Scheduler placeholder jobs use strict locking.

SUNK doesn't evict workloads placed by the SUNK Pod Scheduler during this process, because the scheduler adds a toleration for the `sunk.coreweave.com/lock` taint to every Pod it places.

## Locking

During locking, two different operations proceed at the same time:

* SUNK propagates the [Slurm node state](https://docs.coreweave.com/products/sunk/manage_sunk/slurm-node-states.md) to the Kubernetes Node and updates the lock, as described in the [operation overview](https://docs.coreweave.com/products/sunk/discover_sunk/node-locking.md#operation-overview).
* The Syncer pre-hook performs a blocking check of the lock state.

If the Prolog script receives an error or reaches timeout, the Prolog script fails, [causing the node to drain](https://docs.coreweave.com/products/sunk/manage_sunk/drain-and-undrain-nodes.md). This is preferred, because if the script doesn't stop execution at this point, the job can create resource contention or issues that are complex to troubleshoot.

## Unlocking

Once the Slurm job completes, SUNK must release the Node so it can again accept Kubernetes workloads. The unlocking flow removes the lock from the Node once no Slurm job is running on the node.
