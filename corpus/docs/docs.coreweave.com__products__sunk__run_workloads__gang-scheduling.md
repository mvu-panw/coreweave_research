# Run workloads with gang scheduling

Source: https://docs.coreweave.com/products/sunk/run_workloads/gang-scheduling

# Run workloads with gang scheduling

> Schedule Kubernetes Jobs and LeaderWorkerSet groups with shared Slurm allocations in SUNK

[SUNK Standard](https://docs.coreweave.com/products/sunk.md)

CoreWeave SUNK gang scheduling reserves resources for a complete group of Kubernetes Pods before binding any member to a node. Use it for fixed-size workloads that need every member to run before they can make progress. This guide shows workload owners how to submit a Kubernetes Job or LeaderWorkerSet and verify its Slurm allocation.

A Kubernetes Job forms one gang. Each LeaderWorkerSet (LWS) replica group forms a separate gang. After all expected Pods exist, SUNK requests one Slurm job with one node per Pod. Members wait unbound until Slurm grants the complete allocation. Kubernetes then starts the Pods independently, so they don't necessarily start at the same instant.

## Prerequisites

Before you submit a gang, confirm the following requirements:

* Your cluster runs SUNK 7.6.0 or later in the 7.x series, or SUNK 8.2.0 or later in the 8.x series. If you need to upgrade, follow the [SUNK upgrade procedure](https://docs.coreweave.com/products/sunk/deploy_sunk/upgrade-sunk-cluster.md).
* The [SUNK Pod Scheduler is enabled](https://docs.coreweave.com/products/sunk/run_workloads/schedule-kubernetes-pods.md#enable-the-scheduler) and watches the namespace where you create the workload.
* You have `kubectl` access to create and inspect workloads in that namespace, and access to a [Slurm login node](https://docs.coreweave.com/products/sunk/access_sunk/connect-to-slurm-login-node.md) to inspect allocations.
* You know the [configured scheduler name](https://docs.coreweave.com/products/sunk/run_workloads/schedule-kubernetes-pods.md#look-up-the-scheduler-configuration). Replace `[SCHEDULER-NAME]` in each manifest and `[WORKLOAD-NAMESPACE]` in each command with your values.
* The cluster has Slurm-managed nodes that can satisfy the complete gang's resource and placement requirements.

For the LWS example, if the LWS controller and custom resource definition aren't installed, have a cluster administrator install them. These examples use LWS v0.8.0:

```bash theme={"system"}
kubectl apply --server-side -f https://github.com/kubernetes-sigs/lws/releases/download/v0.8.0/manifests.yaml
```

The examples use small CPU and memory requests to demonstrate scheduling. Adjust the image, requests, node selection, and tolerations for your workload and nodes. Keep the members' resource requirements homogeneous. For GPU workloads and node sharing, see [Manage resources with the SUNK Pod Scheduler](https://docs.coreweave.com/products/sunk/run_workloads/manage-scheduler-resources.md).

Each example sets `terminationGracePeriodSeconds: 20`. Confirm that this is below your scheduler's [termination threshold](https://docs.coreweave.com/products/sunk/run_workloads/schedule-kubernetes-pods.md#set-the-termination-grace-period).

## Submit a Kubernetes Job

This example sets both `parallelism` and `completions` to `2`, so SUNK requests one two-node Slurm allocation for the Job.

1. Save the following manifest in a `job-gang.yaml` file and replace `[SCHEDULER-NAME]`:

   ```yaml title="job-gang.yaml" theme={"system"}
   apiVersion: batch/v1
   kind: Job
   metadata:
     name: sunk-gang-job
   spec:
     parallelism: 2
     completions: 2
     backoffLimit: 0
     template:
       spec:
         schedulerName: "[SCHEDULER-NAME]"
         restartPolicy: Never
         terminationGracePeriodSeconds: 20
         containers:
           - name: workload
             image: busybox:latest
             command: ["sleep", "3600"]
             resources:
               requests:
                 cpu: "1"
                 memory: "100Mi"
   ```

2. Submit the Job:

   ```bash theme={"system"}
   kubectl apply -n "[WORKLOAD-NAMESPACE]" -f job-gang.yaml
   ```

When Slurm grants the allocation, the two Pods run on distinct nodes and share one Slurm job ID. Follow [Verify the allocations](#verify-the-allocations) to check their placement.

## Submit a LeaderWorkerSet

This example creates two independent replica groups with `replicas: 2`. Each group has two Pods because `leaderWorkerTemplate.size: 2` includes both the leader and one worker. SUNK requests a separate two-node allocation for each group.

1. Save the following manifest in a `lws-multigroup-gang.yaml` file and replace both occurrences of `[SCHEDULER-NAME]`:

   ```yaml title="lws-multigroup-gang.yaml" theme={"system"}
   apiVersion: leaderworkerset.x-k8s.io/v1
   kind: LeaderWorkerSet
   metadata:
     name: sunk-gang-lws
   spec:
     replicas: 2
     rolloutStrategy:
       type: RollingUpdate
       rollingUpdateConfiguration:
         maxUnavailable: 1
         maxSurge: 0
     startupPolicy: LeaderCreated
     leaderWorkerTemplate:
       size: 2
       restartPolicy: RecreateGroupOnPodRestart
       leaderTemplate:
         metadata:
           labels:
             role: leader
         spec:
           schedulerName: "[SCHEDULER-NAME]"
           restartPolicy: Always
           terminationGracePeriodSeconds: 20
           containers:
             - name: workload
               image: busybox:latest
               command: ["sleep", "3600"]
               resources:
                 requests:
                   cpu: "1"
                   memory: "100Mi"
       workerTemplate:
         spec:
           schedulerName: "[SCHEDULER-NAME]"
           restartPolicy: Always
           terminationGracePeriodSeconds: 20
           containers:
             - name: workload
               image: busybox:latest
               command: ["sleep", "3600"]
               resources:
                 requests:
                   cpu: "1"
                   memory: "100Mi"
   ```

   Keep the default `startupPolicy: LeaderCreated`. It lets LWS create the workers before the leader becomes ready, so the complete gang can form before SUNK binds the leader. Don't set `LeaderReady`. With that policy, LWS waits for a `Ready` leader before it creates any worker, and the leader can't become `Ready` until the whole gang exists, so the group never schedules. The example also uses `RecreateGroupOnPodRestart` and the default rollout settings. Other `rolloutStrategy` values, such as a `maxSurge` above zero, haven't been validated with gang scheduling.

2. Submit the LeaderWorkerSet:

   ```bash theme={"system"}
   kubectl apply -n "[WORKLOAD-NAMESPACE]" -f lws-multigroup-gang.yaml
   ```

Each group can receive its allocation independently. Members within a group share a Slurm job ID, while the two groups have different IDs.

## Verify the allocations

Check the Pods' node assignments and Slurm job IDs, then inspect the allocation from Slurm.

### Check Pod placement

For the Job example, run:

```bash theme={"system"}
kubectl get pods -n "[WORKLOAD-NAMESPACE]" \
  -l batch.kubernetes.io/job-name=sunk-gang-job \
  -o custom-columns='NAME:.metadata.name,PHASE:.status.phase,NODE:.spec.nodeName,JOBID:.metadata.annotations.sunk\.coreweave\.com/slurm-job-id'
```

After the Pods start, the output is similar to the following:

```text theme={"system"}
NAME                  PHASE     NODE       JOBID
sunk-gang-job-abcde   Running   worker-1   100
sunk-gang-job-fghij   Running   worker-2   100
```

For the LWS example, include the group index:

```bash theme={"system"}
kubectl get pods -n "[WORKLOAD-NAMESPACE]" \
  -l leaderworkerset.sigs.k8s.io/name=sunk-gang-lws \
  -o custom-columns='NAME:.metadata.name,GROUP:.metadata.labels.leaderworkerset\.sigs\.k8s\.io/group-index,PHASE:.status.phase,NODE:.spec.nodeName,JOBID:.metadata.annotations.sunk\.coreweave\.com/slurm-job-id'
```

After both groups start, the output is similar to the following:

```text theme={"system"}
NAME                GROUP   PHASE     NODE       JOBID
sunk-gang-lws-0     0       Running   worker-1   101
sunk-gang-lws-0-1   0       Running   worker-2   101
sunk-gang-lws-1     1       Running   worker-3   102
sunk-gang-lws-1-1   1       Running   worker-4   102
```

Members of one gang occupy distinct nodes. Separate groups can share nodes if the [node sharing policy](https://docs.coreweave.com/products/sunk/run_workloads/schedule-kubernetes-pods.md#choose-a-node-sharing-strategy) permits it.

### Check Slurm job state

On a Slurm login node, replace `[JOB-ID]` with the value from the `JOBID` column for the allocation you want to inspect:

```bash theme={"system"}
scontrol show job [JOB-ID]
```

For a running two-member gang, check that `JobState` is `RUNNING`, `NumNodes` is `2`, and `NodeList` contains the two allocated Slurm nodes. CPU and memory totals depend on your requests and Slurm configuration.

## Optional: Configure topology segments

For GB200 and GB300 workloads that use Slurm's Topology/Block Plugin, set `sunk.coreweave.com/segment` on the Pod template to request a topology segment size. For a Job, the annotation belongs under `spec.template.metadata.annotations`. For an LWS, apply it to the leader and worker Pod templates.

For example, this Pod-template metadata excerpt requests segments of two nodes:

```yaml theme={"system"}
metadata:
  annotations:
    sunk.coreweave.com/segment: "2"
```

Choose a segment size that fits your gang and available topology blocks. For segment sizing and troubleshooting, see [Topology and block scheduling in Slurm](https://docs.coreweave.com/products/sunk/optimize_workloads/topology-scheduling.md).

## Limitations and lifecycle

Plan gang workloads around the following constraints:

* **Supported workload types.** SUNK recognizes Kubernetes Jobs and LWS replica groups as gangs. Standalone Pods and unsupported controllers continue to use one Slurm placeholder job per Pod. SUNK doesn't require a PodGroup resource.
* **Fixed member count.** A gang's Slurm allocation can't grow or shrink in place. In an LWS, changing `replicas` adds or removes entire groups. Adding or removing workers within an existing leader-and-worker group isn't supported.
* **Homogeneous resources.** Members of a gang must have compatible CPU, memory, and GPU requirements. A CPU-only leader with GPU workers isn't supported. The examples set the same requests for all members. To keep them identical with less to maintain, omit `leaderTemplate` from the LWS. LWS then uses `workerTemplate` for the leader Pod as well.
* **LWS resource updates.** When a group rolls out updated Pod templates with incompatible resource requirements, SUNK cancels the old allocation and creates a replacement after teardown. A group held on its old revision by a rollout partition keeps its compatible allocation until that group updates.
* **LWS group recreation.** With `RecreateGroupOnPodRestart`, a recreated group can reuse its allocation if its size and resource requirements remain compatible.
* **LWS startup policy.** Gang scheduling requires the default `startupPolicy: LeaderCreated`. With `LeaderReady`, LWS creates no workers until the leader is Ready, so the gang never completes and the group stays Pending. Rollout settings other than the defaults haven't been validated with gang scheduling.
* **Job retries after external allocation termination.** Use `backoffLimit: 0` when a Job's Slurm allocation may be terminated externally. With a positive value, including the default of `6` when unset, Kubernetes may create retry Pods that the scheduler does not correctly associate with the original gang.
* **Slurm scheduling policy.** A complete gang can still wait for capacity, queue priority, fair-share, or reservations. Gang scheduling doesn't bypass those policies.

## Troubleshoot gang scheduling

Use workload events to distinguish a gang that's still forming from a queued or failed Slurm allocation:

```bash theme={"system"}
kubectl get events -n "[WORKLOAD-NAMESPACE]" --sort-by=.metadata.creationTimestamp
```

Use the following events and job states to identify the problem:

* `SunkGangWaiting` reports how many gang members are present and expected. Confirm that Kubernetes created every member and that every Pod uses the configured SUNK scheduler name. If an LWS group has a leader but no workers, check that the LeaderWorkerSet doesn't set `startupPolicy: LeaderReady`.
* `SunkGangValidationFailed` reports incompatible LWS requirements. Check that the leader and worker templates have compatible CPU, memory, and GPU requirements and use the same scheduler name.
* A Slurm job in `PENDING` can be waiting for the complete node set. Check its reason with `scontrol show job [JOB-ID]`. See [Why is my Slurm job stuck in PENDING?](https://docs.coreweave.com/support/sunk/articles/why-is-my-slurm-job-stuck-in-pending).
* If a Job's allocation ends before the Kubernetes Job completes, SUNK deletes the Job. If an LWS group's allocation ends, the group can form again with a new allocation. Inspect workload events and Slurm accounting to determine why the allocation ended:

  ```bash theme={"system"}
  sacct -j [JOB-ID] -o JobID,JobName,State,Reason,ReqNodes,AllocNodes
  ```

For Pod admission failures or invalid annotations, see [Troubleshoot a SUNK-scheduled Kubernetes Pod](https://docs.coreweave.com/support/sunk/articles/why-does-my-sunk-scheduled-pod-fail-to-start).

## Clean up

Delete the example workload objects to release their allocations:

```bash theme={"system"}
kubectl delete job sunk-gang-job -n "[WORKLOAD-NAMESPACE]"
kubectl delete leaderworkerset sunk-gang-lws -n "[WORKLOAD-NAMESPACE]"
```

SUNK cancels the associated Slurm allocations. Pods can remain in `Terminating` while Slurm completes teardown.
