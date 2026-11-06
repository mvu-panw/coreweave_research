# Integrate sandboxes with the SUNK Pod Scheduler

Source: https://docs.coreweave.com/products/sandboxes/profiles/sunk-integration

# Integrate sandboxes with the SUNK Pod Scheduler

> Route sandbox pods through the SUNK Pod Scheduler so Slurm places them alongside your Slurm jobs.

Route CPU-only sandbox pods through the SUNK Pod Scheduler so that Slurm manages their placement alongside Slurm jobs running in your cluster. Sandboxes become regular Slurm jobs and can run on any node in your cluster with available resources, including sharing CPU resources with other Slurm jobs or sandboxes already running on the same node.

A runner's policy sets the SUNK scheduler for every sandbox placed on that runner. Clients select the runner with CoreWeave Kubernetes Service (CKS) placement. This guide is for cluster operators configuring the policy and workload authors launching sandboxes.

> [!NOTE]
>
> **CPU-only support**
>
> GPU sandboxes are in private preview and aren't yet supported by the SUNK Pod Scheduler integration. See [GPU sandboxes](https://docs.coreweave.com/products/sandboxes/gpu-sandboxes.md) for supported placement options and how to request access.
>
> CPU-only sandboxes can land on idle CPU nodes, share CPU nodes with other sandboxes or Slurm jobs, and share CPU resources on GPU nodes where other workloads are running. See [Known limitations](https://docs.coreweave.com/products/sunk/run_workloads/schedule-kubernetes-pods.md#known-limitations) for details.

## Prerequisites

* A CKS cluster with [SUNK](https://docs.coreweave.com/products/sunk.md) deployed and the [SUNK Pod Scheduler](https://docs.coreweave.com/products/sunk/run_workloads/schedule-kubernetes-pods.md) enabled.
* A [CoreWeave sandbox runner deployed on the same cluster](https://docs.coreweave.com/products/sandboxes/operations/managed-runners.md).
* The [CoreWeave Intelligent CLI](https://github.com/coreweave/cwic) (`cwic`) v1.44.0 or later, installed and authenticated. See [Deploy and manage a runner](https://docs.coreweave.com/products/sandboxes/operations/managed-runners.md) for setup details.
* The **Sandbox Admin** role to read and update the runner's policy, and permission to update the Slurm deployment.
* `cwsandbox >= 1.0.0`, installed and authenticated, for the v1 sandbox API.
* `kubectl` and `yq` for cluster inspection. The HTTP examples also use `curl`, `jq`, and a CoreWeave API token in `$TOKEN`.

Replace `[RUNNER-ID]` throughout this page with the ID of the runner on your SUNK cluster.

## Step 1: Verify the SUNK Pod Scheduler

Validate that your SUNK deployment is configured to work with CoreWeave sandboxes.

1. Verify the scheduler is running:

   ```bash theme={"system"}
   kubectl get pods -n tenant-slurm -l app.kubernetes.io/name=sunk-scheduler
   ```

   If no pods are returned, enable the scheduler in your Slurm Helm values by setting `scheduler.enabled: true`. See [Enable the scheduler](https://docs.coreweave.com/products/sunk/run_workloads/schedule-kubernetes-pods.md#enable-the-scheduler) for details.

2. Look up the scheduler name. You set it on the runner policy in Step 2. On SUNK 8.0 and later, the scheduler reads its name from a ConfigMap:

   ```bash theme={"system"}
   kubectl get configmap -n tenant-slurm -l app.kubernetes.io/component=scheduler \
     -o jsonpath='{.items[0].data.scheduler\.conf}' | yq '.scheduler.name'
   ```

   ```text theme={"system"}
   slurm-scheduler
   ```

   On SUNK 7.x, the name is a `--scheduler-name` argument on the scheduler Pod instead. See [Look up the scheduler configuration](https://docs.coreweave.com/products/sunk/run_workloads/schedule-kubernetes-pods.md#look-up-the-scheduler-configuration) for the underlying behavior.

3. Look up the `KillWait` value. You use it to check Pod termination:

   ```bash theme={"system"}
   kubectl get pods -n tenant-slurm -l app.kubernetes.io/name=sunk-scheduler -o yaml \
     | yq '.items[0].spec.containers[] | select(.name == "scheduler").args'
   ```

   Look for `--slurm-kill-wait` in the output:

   ```text theme={"system"}
   - --slurm-kill-wait=30s
   ```

4. Configure Slurm's termination window for sandbox Pods. SUNK requires `terminationGracePeriodSeconds` to be strictly less than `--slurm-kill-wait` minus 5 seconds.

   The policy doesn't accept `base.spec.terminationGracePeriodSeconds`. For a Pod with Kubernetes' default 30-second grace period, set `KillWait` above 35 seconds. For example, merge this into your Slurm Helm values and apply the update through your normal SUNK deployment process:

   ```yaml theme={"system"}
   slurmConfig:
     KillWait: 60
   ```

   This changes Slurm's termination window for jobs across the cluster. Verify that the scheduler now reports `--slurm-kill-wait=60s` using the preceding command. See [Slurm configuration parameters](https://docs.coreweave.com/products/sunk/reference/slurm-parameters.md#slurmConfig) and [Set the termination grace period](https://docs.coreweave.com/products/sunk/run_workloads/schedule-kubernetes-pods.md#set-the-termination-grace-period).

   > [!WARNING]
   >
   > Sandboxes with snapshot-capable storage can have a 300-second Pod grace period. A 60-second `KillWait` doesn't cover those Pods. Inspect the generated Pod's `terminationGracePeriodSeconds` and set `KillWait` above that value plus 5 seconds. For 300 seconds, use a value such as 330. Keep the scheduler's kill-wait setting aligned with Slurm.

5. Confirm the scheduler scope covers the sandbox namespaces. The runner manages namespace selection. It isn't a policy field. Set `scheduler.scope.type: cluster` to watch all sandbox namespaces, including ones created for new users. If you use `scheduler.scope.type: namespace`, include each sandbox namespace in `scheduler.scope.namespaces` and update the list as new namespaces are created. Apply scope changes through Helm so the scheduler also receives the required RBAC permissions in those namespaces. See [Enable the scheduler](https://docs.coreweave.com/products/sunk/run_workloads/schedule-kubernetes-pods.md#enable-the-scheduler).

6. Lower `slurmd` resource requests on NodeSets you want to share with sandboxes. This is a change on the Slurm side, in your Slurm Helm values, not in any sandbox configuration. The default NodeSet resource requests consume most of the node's allocatable capacity in Kubernetes, leaving no room for sandbox pods. Without this change, sandbox pods are rejected with `OutOfMemory` or `OutOfcpu` errors. See [Manage resources with the SUNK Pod Scheduler](https://docs.coreweave.com/products/sunk/run_workloads/manage-scheduler-resources.md) for configuration details.

## Step 2: Configure the runner policy

Every runner carries one policy. Set `base.spec.schedulerName` in that policy to route its sandbox Pods through SUNK. You don't create or bind a separate policy resource.

> [!WARNING]
>
> A policy update replaces the entire policy document. Read the current policy, preserve its existing `base` attachments and `constraints`, and change only the settings needed for SUNK. This change applies to new sandboxes on the runner. It doesn't move running sandboxes.

Merge the following fragment into the runner's existing policy. Replace `slurm-scheduler` with the scheduler name from Step 1:

```yaml theme={"system"}
base:
  spec:
    schedulerName: "slurm-scheduler"
```

> [tab] CLI
>
> Read the current policy, then open it in `$EDITOR`:
>
> ```bash theme={"system"}
> cwic sandbox runner policy get [RUNNER-ID]
> cwic sandbox runner policy edit [RUNNER-ID]
> ```
>
> Add `schedulerName` under `base.spec`, keeping the rest of the document. Save and close the editor to apply it.
>
> For a file-based update, follow [Update a policy](https://docs.coreweave.com/products/sandboxes/profiles/configure.md#update-a-policy). Add `base.spec.schedulerName` to the policy captured by that procedure. Keep its other fields and the `etag` from the same read.

> [tab] curl
>
> Use the Connect HTTP API to read the runner, including its policy revision (`etag`):
>
> ```bash theme={"system"}
> curl --fail-with-body --silent --show-error -X POST \
>   'https://api.coreweave.com/coreweave.sandbox.v1.RunnerManagementService/GetManagedRunner' \
>   -H "Authorization: Bearer $TOKEN" \
>   -H "Content-Type: application/json" \
>   -H "Connect-Protocol-Version: 1" \
>   --data '{"runnerId": "[RUNNER-ID]"}' \
>   -o runner.json
> ```
>
> If the runner has no policy, configure one using [Configure a sandbox policy](https://docs.coreweave.com/products/sandboxes/profiles/configure.md) before continuing.
>
> Add the scheduler name while retaining all other policy fields. Include the `etag` from the read in the update request:
>
> ```bash theme={"system"}
> jq -e '
>   if .policy == null or .etag == null then
>     error("Read a configured runner policy and its etag before updating")
>   else . end |
>   .policy.base.spec.schedulerName = "slurm-scheduler" |
>   {
>     runnerId: .identity.runnerId,
>     managedRunner: {identity: .identity, policy: .policy, etag: .etag},
>     updateMask: "policy"
>   }' runner.json > runner-policy-update.json
> ```
>
> Review the `runner-policy-update.json` file, then apply it:
>
> ```bash theme={"system"}
> curl --fail-with-body -X POST \
>   'https://api.coreweave.com/coreweave.sandbox.v1.RunnerManagementService/UpdateManagedRunner' \
>   -H "Authorization: Bearer $TOKEN" \
>   -H "Content-Type: application/json" \
>   -H "Connect-Protocol-Version: 1" \
>   --data-binary @runner-policy-update.json
> ```
>
> A missing `etag` is rejected. If another administrator updates the policy before you submit it, the stale `etag` causes the update to fail with `FAILED_PRECONDITION` and nothing changes. Read the runner again, reapply your changes to the policy that comes back, and resubmit with the new `etag`.

> [!WARNING]
>
> Avoid `base.spec.nodeSelector` and sandbox instance-type restrictions that conflict with Slurm placement. Slurm chooses the node, and a conflicting Kubernetes selector can cause `NodeAffinity` failures. Use Slurm partitions or constraints through the annotations in Step 4 to target nodes.

The `constraints.network` field and the sandbox's declared egress govern network access. Keep the runner's existing network constraints when adding SUNK scheduling. See [Configure a sandbox policy](https://docs.coreweave.com/products/sandboxes/profiles/configure.md#constrain-network-access).

Policy changes can take time to propagate to sandbox creation. Before relying on a new scheduler or pinned annotation, create a sandbox and verify its Pod fields as described in [Pods remain pending](#pods-remain-pending). A policy read can show the new value before new sandboxes use it.

For the complete schema, see [Policy reference](https://docs.coreweave.com/products/sandboxes/reference/profile.md). For runner setup, see [Deploy and manage a runner](https://docs.coreweave.com/products/sandboxes/operations/managed-runners.md).

## Step 3: Create sandboxes

To select the runner whose policy you configured, set `placement_mode="cks"` and `runner_ids` in Python, or `runnerIds` in TypeScript. The runner policy supplies the scheduler automatically.

> [tab] Python
>
> ```python theme={"system"}
> from cwsandbox import Sandbox
>
> with Sandbox.run(placement_mode="cks", runner_ids=["[RUNNER-ID]"]) as sb:
>     print(f"Sandbox ID: {sb.sandbox_id}")
>     result = sb.exec(["hostname"]).result()
>     print(result.stdout)
> ```

> [tab] TypeScript
>
> The TypeScript example reads a CoreWeave API access token from `CWSANDBOX_API_KEY`.
>
> ```typescript theme={"system"}
> import { createSandboxClientFromEnv } from "@coreweave/cwsandbox/node";
>
> const client = createSandboxClientFromEnv();
> await client.withSandbox(
>   async (sandbox) => {
>     console.log(`Sandbox ID: ${sandbox.sandboxId}`);
>     const result = await sandbox.commands.run(["hostname"]);
>     console.log(result.stdout);
>   },
>   { runnerIds: ["[RUNNER-ID]"] },
> );
> ```

To verify the sandbox is running as a Slurm job, search for its placeholder job in Slurm using the sandbox ID printed in the preceding example:

```bash theme={"system"}
sacct --format=JobID,JobName%60,State,NodeList -X | grep [SANDBOX-ID]
```

Slurm picks the node. You don't control which node the sandbox lands on unless you add [Slurm annotations](#step-4-control-placement-with-slurm-annotations) to guide Slurm's scheduler.

To use the same SUNK-configured runner for every sandbox in a Python session, set the placement fields on `SandboxDefaults`:

```python theme={"system"}
from cwsandbox import Sandbox, SandboxDefaults

defaults = SandboxDefaults(
    placement_mode="cks",
    runner_ids=("[RUNNER-ID]",),
)

with Sandbox.session(defaults) as session:
    sb1 = session.sandbox()
    sb2 = session.sandbox()

    r1 = sb1.exec(["hostname"]).result()
    r2 = sb2.exec(["hostname"]).result()
    print(f"sb1: {r1.stdout.strip()}, sb2: {r2.stdout.strip()}")
```

The TypeScript client has no session defaults, so pass `runnerIds` on each call.

### Resource requests and Slurm accounting

SUNK reads the pod's resource **requests** (not limits) and converts them to Slurm job parameters:

| Pod field | Slurm parameter |
| - | - |
| `requests.cpu` | `CPUsPerTask` |
| `requests.memory` | `MinMemoryNode` |

Slurm uses these values for scheduling decisions and `sacct` accounting. SUNK does not require any particular Quality of Service class. Guaranteed (requests equal limits) and Burstable (requests lower than limits) both work.

If you set requests lower than limits with `ResourceOptions`, the pod can burst up to the limits when capacity is free, but Slurm only sees the requests. For example, a sandbox configured with:

```python theme={"system"}
requests={"cpu": "500m", "memory": "512Mi"},
limits={"cpu": "2",     "memory": "2Gi"},
```

shows up in `sacct` as a 500m CPU, 512Mi memory job, even though the sandbox can use up to 2 CPUs and 2Gi when the node has room. See [Resources](https://docs.coreweave.com/products/sandboxes/client/guides/sandbox-configuration.md#resources) for the full `ResourceOptions` reference.

Size the requests to match what your sandbox workloads need, leaving enough room on the target nodes for the `slurmd` requests you lowered in Step 1. For the underlying rules, see [Set resource requests](https://docs.coreweave.com/products/sunk/run_workloads/schedule-kubernetes-pods.md#set-resource-requests) and [Manage resources with the SUNK Pod Scheduler](https://docs.coreweave.com/products/sunk/run_workloads/manage-scheduler-resources.md).

## Step 4: Control placement with Slurm annotations

To control sandbox placement, set SUNK annotations on the sandbox at launch time. The following example pins the sandbox to the `hpc-prod` partition:

> [tab] Python
>
> ```python theme={"system"}
> from cwsandbox import Sandbox
>
> sb = Sandbox.run(
>     placement_mode="cks",
>     runner_ids=["[RUNNER-ID]"],
>     annotations={
>         "sunk.coreweave.com/partition": "hpc-prod",
>     },
> )
> ```

> [tab] TypeScript
>
> ```typescript theme={"system"}
> import { createSandboxClientFromEnv } from "@coreweave/cwsandbox/node";
>
> const client = createSandboxClientFromEnv();
> const sandbox = await client.create({
>   runnerIds: ["[RUNNER-ID]"],
>   annotations: {
>     "sunk.coreweave.com/partition": "hpc-prod",
>   },
> });
> ```

### Common annotations

All annotations share the `sunk.coreweave.com/` prefix. The annotations commonly used to control sandbox placement are:

| Annotation key | Description |
| - | - |
| `partition` | Slurm partition name |
| `constraint` | Slurm feature constraint |
| `account` | Slurm accounting name |
| `qos` | Slurm QoS level |
| `user-id` | Slurm user ID for accounting. Must be a numeric Linux UID (for example `"1000"`) |
| `exclusive` | Node exclusivity (`none`, `user`, or `ok`) |

Passing a username instead of a numeric UID to the `user-id` annotation causes a blocking error that prevents Slurm from scheduling the sandbox. To find the numeric UID from a Slurm login node, replace `[USERNAME]` with the Linux username to look up:

```bash theme={"system"}
id -u           # your own UID
id -u [USERNAME]  # someone else's UID
whoami          # confirm your username first if needed
```

For the full list, see [Annotations reference](https://docs.coreweave.com/products/sunk/run_workloads/schedule-kubernetes-pods.md#annotations-reference).

### Enforce annotations in the policy

To set a Slurm job parameter for every sandbox on the runner, add its annotation to `base.metadata.annotations`. For example, merge this fragment into the existing policy to use the `sandboxes` partition:

```yaml theme={"system"}
base:
  metadata:
    annotations:
      sunk.coreweave.com/partition: "sandboxes"
  spec:
    schedulerName: "slurm-scheduler"
```

Policy annotations take precedence over client-supplied values for the same key. To let clients choose a value, omit that key from `base.metadata.annotations` and ensure `constraints.metadata.denied_annotation_prefixes` permits it. For example, leave `sunk.coreweave.com/user-id` unpinned when clients need to match the user of a training job.

### Match the Slurm user from a training job

Training jobs often run with `--exclusive=user` to claim entire nodes for a single user. This prevents other users' jobs from competing for resources on those nodes while still allowing the same user to run additional jobs there, such as sandboxes that use spare CPU alongside GPU training.

By default, SUNK placeholder jobs run as root (UID 0). Because root is a different user than the one who submitted the training job, Slurm does not place the sandbox placeholder on the exclusive node.

When training code uses the `cwsandbox` Python client to create sandboxes from within a running Slurm job, it can read the job's Slurm user ID from the environment and pass it as an annotation. This ensures the sandbox placeholder jobs are submitted under the same Slurm user as the training job, allowing Slurm to place them on the same exclusive nodes:

```python theme={"system"}
import os
from cwsandbox import Sandbox, SandboxDefaults

slurm_uid = os.environ["SLURM_JOB_UID"]

defaults = SandboxDefaults(
    placement_mode="cks",
    runner_ids=("[RUNNER-ID]",),
    annotations={
        "sunk.coreweave.com/user-id": slurm_uid,
    },
)

with Sandbox.session(defaults) as session:
    sb = session.sandbox()
    result = sb.exec(["hostname"]).result()
    print(result.stdout)
```

The `user-id` annotation must be a numeric Linux UID, not a username. When set, SUNK also defaults the `group-id` to the same value. Set `sunk.coreweave.com/group-id` separately if the group ID differs.

## Troubleshooting

Use the following sections to diagnose common issues when running sandboxes through the SUNK Pod Scheduler.

### Pods remain pending

Inspect the sandbox Pod to confirm the runner applied the scheduler name and to check its termination grace period:

```bash theme={"system"}
kubectl get pods -A -l 'sandbox.coreweave.com/sandbox-id=[SANDBOX-ID]' \
  -o custom-columns='NAMESPACE:.metadata.namespace,NAME:.metadata.name,SCHEDULER:.spec.schedulerName,GRACE:.spec.terminationGracePeriodSeconds,PARTITION:.metadata.annotations.sunk\.coreweave\.com/partition'
```

Run this while the sandbox is active. Confirm that `SCHEDULER` matches the SUNK scheduler, its scope includes `NAMESPACE`, and `GRACE` is strictly less than the scheduler's kill wait minus 5 seconds. A 30-second grace period fails with the default 30-second kill wait. If the policy pins a partition, confirm that `PARTITION` matches it.

If the scheduler name or pinned annotations are missing or incorrect, read back the runner policy and confirm that the client selected the intended runner. If newly created Pods still use previous values, allow more time for policy propagation and retry with another sandbox.

### Placeholder jobs temporarily in completing state

When a sandbox stops, its Slurm placeholder job spends 30 to 60 seconds in the `CG` (completing) state while cleanup scripts run and the node is released back to the pool. This is normal Slurm behavior and does not affect other jobs running on the same node. See [Slurm job states](https://docs.coreweave.com/products/sunk/manage_sunk/slurm-job-states.md) for the full state reference.

### Sandboxes not landing where expected

Slurm determines sandbox placement based on the annotations the policy sets or the client passes. If sandboxes aren't landing on the expected nodes, verify the Slurm job parameters.

SUNK creates a placeholder Slurm job for each sandbox pod with the name `<namespace>/<pod-name>`. The pod name includes the sandbox ID, which is available from the client as `sb.sandbox_id` in Python or `sandbox.sandboxId` in TypeScript. Find the placeholder job and inspect its parameters by searching for the sandbox ID:

```bash theme={"system"}
sacct --format=JobID,JobName%60,Partition,Account,AllocCPUS,ReqMem,State,NodeList,Start,End -X \
  | grep [SANDBOX-ID]
```

Replace `[SANDBOX-ID]` with that sandbox ID.

## See also

* [About CoreWeave sandboxes](https://docs.coreweave.com/products/sandboxes.md)
* [Deploy and manage a runner](https://docs.coreweave.com/products/sandboxes/operations/managed-runners.md)
* [Configure a sandbox policy](https://docs.coreweave.com/products/sandboxes/profiles/configure.md)
* [Schedule Kubernetes pods with the SUNK Pod Scheduler](https://docs.coreweave.com/products/sunk/run_workloads/schedule-kubernetes-pods.md)
* [RL training with sandboxes](https://docs.coreweave.com/products/sandboxes/client/guides/rl-training.md)
* [Sandbox configuration](https://docs.coreweave.com/products/sandboxes/client/guides/sandbox-configuration.md)
