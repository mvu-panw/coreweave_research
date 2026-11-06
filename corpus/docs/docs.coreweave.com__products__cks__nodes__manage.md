# Manage Node Pools

Source: https://docs.coreweave.com/products/cks/nodes/manage

# Manage Node Pools

> Delete and modify Node Pools using the API or Cloud Console

This page explains how to modify, delete, and inspect Node Pools in CKS. Use it when you need to scale workloads, update hardware configurations, or remove unused resources. You can modify Node Pools after creation, either by editing them in the Cloud Console or by deploying an adjusted manifest with Kubernetes.

To reboot Nodes in a Node Pool, see [Reboot Nodes](https://docs.coreweave.com/products/cks/nodes/reboot.md).

## Modify a Node Pool using the Cloud Console

**1. Open the Node Pools page**

In the Cloud Console, navigate to the Node Pools page (`https://console.coreweave.com/zones/[ZONE-NAME]/clusters/[CLUSTER-NAME]/node-pools`).

All existing Node Pools are listed on the Node Pool dashboard, including the Node Pool containing Control Plane CPU Nodes:

![Screenshot showing the edit and delete modals open on the Node Pool dashboard.](https://mintcdn.com/coreweave-dbfa0e8d/Diszsi3qOqeLxowx/products/cks/_media/node-pool-edit-delete.png?fit=max\&auto=format\&n=Diszsi3qOqeLxowx\&q=85\&s=13ae9fc611afa7a6636e634585272dcf)

**2. Open the manifest editor**

Click the vertical dot menu to the right of the Node Pool, then click **Edit** to open the manifest editor:

![Screenshot showing the Node Pool creation page.](https://mintcdn.com/coreweave-dbfa0e8d/Diszsi3qOqeLxowx/products/cks/_media/node-pool-edit.png?fit=max\&auto=format\&n=Diszsi3qOqeLxowx\&q=85\&s=4aa1a9e846700383f2c3751e3a41ffc9)

**3. Submit your changes**

After you make your changes, click the **Submit** button.

CKS applies the updated configuration to the Node Pool.

> [!NOTE]
>
> Changes may take a moment to display on the Cloud Console. To learn more about the current status of the Node Pool, hover over the status in the dashboard.

## Modify a Node Pool using Kubernetes

To modify a Node Pool, first edit the Node Pool manifest, then `apply` the changed manifest using `kubectl`.

For example, take a Node Pool deployed with the following manifest:

```yaml title="example-nodepool.yaml" highlight={9} theme={"system"}
apiVersion: compute.coreweave.com/v1alpha1
kind: NodePool
metadata:
  name: example-nodepool
spec:
  computeClass: default
  instanceType: gd-8xh100ib-i128
  autoscaling: false
  targetNodes: 10
  minNodes: 0
  maxNodes: 0
```

This manifest deploys a Node Pool with `10` Nodes. To change it to have only `5` Nodes, first adjust the manifest to change the `targetNodes` value to `5` as highlighted in the following example:

```yaml title="example-nodepool.yaml" highlight={9} theme={"system"}
apiVersion: compute.coreweave.com/v1alpha1
kind: NodePool
metadata:
  name: example-nodepool
spec:
  computeClass: default
  instanceType: gd-8xh100ib-i128
  autoscaling: false
  targetNodes: 5
  minNodes: 0
  maxNodes: 0
```

To apply the changes, apply the updated manifest using `kubectl`:

```bash title="Example command" theme={"system"}
kubectl apply -f example-nodepool.yaml
```

After you apply the manifest, CKS adjusts the number of Nodes in the Node Pool to match.

> [!NOTE]
>
> * Removing Nodes from a Node Pool can take some time.
> * See [Scaling strategies](https://docs.coreweave.com/products/cks/nodes/nodes-and-node-pools.md#scaling-strategies) to learn how CKS responds when the value of `targetNodes` changes.

### Use `kubectl scale`

You can also use `kubectl` to adjust `targetNodes` without editing the manifest directly.

For example, to set `targetNodes` to 5 in `example-nodepool`, run:

```bash title="Example command" theme={"system"}
kubectl scale nodepool example-nodepool --replicas 5
```

> [!NOTE]
>
> `kubectl scale` writes to `targetNodes` and is not compatible with Node Pools that use `targetRacks` (rack-based instance types such as GB200 and GB300). To scale a rack-based Node Pool, edit the manifest and update `targetRacks` directly, then apply with `kubectl apply`.

### Verify the updated Node Pool

To check the status of the modified Node Pool, target the Node Pool with `kubectl get nodepool`. For example:

```bash title="Example command" theme={"system"}
kubectl get nodepool example-nodepool
```

This returns information about the current status of the targeted Node Pool, such as:

```text title="Example output" theme={"system"}
NAME               INSTANCE TYPE      TARGET   QUEUED   INPROGRESS   CURRENT   PREFILL   VALIDATED   CAPACITY     QUOTA   AGE
example-nodepool   gd-8xh100ib-i128   5        0        0            5         0         Valid       Sufficient   Under   42h
```

After the adjustment completes, the value of `CURRENT` (the number of Nodes currently in the Node Pool) should match the value of `TARGET` (the number of Nodes desired in the Node Pool).

To see further details about the Node Pool in YAML format, target the Node Pool with `kubectl get nodepool -o yaml`.

```bash title="Example command" theme={"system"}
kubectl get nodepool example-nodepool -o yaml
```

If you need to reboot a Node or Node Pool, see [Reboot Nodes](https://docs.coreweave.com/products/cks/nodes/reboot.md).

## View Node details

Standard `kubectl get nodes` output doesn't include CoreWeave-specific metadata such as instance type, reservation status, ncore version, and Node state. Use the [CoreWeave Intelligent CLI](https://github.com/coreweave/cwic) (`cwic`) or a custom `kubectl` command to view these details.

The following sections describe both approaches.

### Use CoreWeave Intelligent CLI

For the full command reference and release notes, see the [CoreWeave Intelligent CLI](https://github.com/coreweave/cwic) repository. The steps below cover a typical install and authentication flow.

#### Install `cwic`

Download the latest release for your platform from the [`cwic` releases page](https://github.com/coreweave/cwic/releases) and move the binary onto your `PATH` (for example `/usr/local/bin` or `$HOME/.local/bin`).

Once installed, `cwic` can update itself in place:

```bash theme={"system"}
cwic update
```

#### Authenticate `cwic`

Generate an API access token from the [Tokens](https://console.coreweave.com/tokens) page in the Cloud Console, then sign in:

```bash theme={"system"}
cwic auth login
```

Paste the token when prompted. `cwic` stores it in `~/.cwic/config.json` and reuses it for subsequent commands, so you don't need to export an environment variable. You can also pass the token directly with `cwic auth login [TOKEN]`, or add a friendly name with `--name "[LABEL]"` when you manage multiple organizations. Switch between authenticated organizations with `cwic auth switch`, and check the active one with `cwic auth whoami`.

Kubernetes-based `cwic` commands (`node`, `sunk`, `nodepool`) require a kubeconfig. Generate one for a single cluster or for every cluster you can access:

```bash theme={"system"}
cwic cluster auth [CLUSTER-NAME]
cwic cluster auth all
```

If you write the kubeconfig to a custom path instead of merging into the default, export `KUBECONFIG` before running the commands below:

```bash theme={"system"}
export KUBECONFIG=/path/to/your/kubeconfig
```

#### List Nodes with `cwic`

To list all Nodes in your cluster with CoreWeave-specific details, run:

```bash theme={"system"}
cwic node get
```

This returns Node information including the instance type, reservation status, Node Pool, ncore version, and lifecycle state:

```text title="Example output" theme={"system"}
NAME      IP              TYPE               RESERVED   NODEPOOL           READY   ACTIVE   CORDON   RECONFIGURE   VERSION   STATE        PENDING STATE
g1f0000   10.176.222.21   gd-8xh100ib-i128   012345     example-nodepool   true    true     false    NotRequired   2.26.0    production   none
g400000   10.176.207.22   cd-hp-a96-genoa    012345     example-nodepool-2 true    true     false    NotRequired   2.26.0    production   none
```

To list Nodes in a specific Node Pool, run:

```bash theme={"system"}
cwic nodepool nodes get [NODEPOOL-NAME]
```

### Use `kubectl`

To view CoreWeave-specific Node details with `kubectl`, add the following alias to your shell configuration:

```bash theme={"system"}
alias nodes="kubectl get nodes -o=custom-columns=\"NAME:metadata.name,IP:status.addresses[?(@.type=='InternalIP')].address,TYPE:metadata.labels['node\.coreweave\.cloud\/type'],RESERVED:metadata.labels['node\.coreweave\.cloud\/reserved'],READY:status.conditions[?(@.type=='Ready')].status,CORDON:spec.unschedulable,VERSION:metadata.labels['node\.coreweave\.cloud\/version'],STATE:metadata.labels['node\.coreweave\.cloud\/state']\""
```

Then run:

```bash theme={"system"}
nodes
```

```text title="Example output" theme={"system"}
NAME      IP              TYPE               RESERVED   READY   CORDON   VERSION   STATE
g1f0000   10.176.222.21   gd-8xh100ib-i128   012345     True    <none>   2.26.0    production
g400000   10.176.207.22   cd-gp-i64-erapids  012345     True    <none>   2.33.0    production
```

## Enable Node Pool prefill

Prefill is enabled by default for supported new Node Pools.

> [!NOTE]
>
> Node Pools created before October 8, 2026, retain their existing prefill settings. See the [prefill changelog entry](https://docs.coreweave.com/changelog.md#october-8-2026).

For an overview of Node Pool prefill, see [Node Pool prefill](https://docs.coreweave.com/products/cks/nodes/nodes-and-node-pools.md#node-pool-prefill).

**Prefill requirements**

| Setting | Requirement |
| - | - |
| Instance type | Use a non-rack-based instance type. Rack-based instances, such as GB200 and GB300, don't support prefill. |
| Autoscaling | Set `autoscaling: false`. With autoscaling enabled, CKS doesn't start new prefill operations. Operations already in progress continue. |
| Compute class | Use `computeClass: default`. Spot Node Pools don't support prefill. |

When you omit `spec.prefill`, CKS uses the defaults shown in this example. To configure prefill explicitly, add a `prefill` block under `spec`:

```yaml title="example-nodepool.yaml" highlight={10-13} theme={"system"}
apiVersion: compute.coreweave.com/v1alpha1
kind: NodePool
metadata:
  name: example-nodepool
spec:
  computeClass: default
  instanceType: gd-8xh100ib-i128
  autoscaling: false
  targetNodes: 10
  prefill:
    enabled: true
    timeout: "24h"
    maxNodes: 3
```

Prefill configuration has the following limits:

* `timeout`: Defaults to 24 hours. The maximum allowed timeout is also 24 hours by default. If your timeout is rejected, check the [prefill status message](https://docs.coreweave.com/products/cks/reference/node-pool.md#condition-prefillenabled) for the allowed limit.
* `maxNodes`: Can be between 1 and 4. Default is 3.

If you increase `spec.prefill.timeout` above the allowed limit, prefill operations already in progress continue with the timeout capped at that limit. CKS doesn't mark additional Nodes for prefill until you correct the timeout.

Apply the change by editing the manifest and running `kubectl apply -f example-nodepool.yaml`. For an overview of prefill behavior and Node conditions, see [Node Pool prefill](https://docs.coreweave.com/products/cks/nodes/nodes-and-node-pools.md#node-pool-prefill). For full field details, see the [Node Pool reference](https://docs.coreweave.com/products/cks/reference/node-pool.md#prefill).

### Disable prefill

To disable prefill, set `spec.prefill.enabled: false`. CKS lets prefill operations already in progress finish but doesn't mark additional Nodes for prefill.

Unsupported Node Pools don't start new prefill operations. You don't need to disable prefill explicitly. Operations already in progress continue.

## Target specific GPUs or CPUs

To ensure CKS schedules your workloads on the correct hardware in a cluster with different GPU types, use a combination of Kubernetes [resource requests](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/#requests-and-limits) and [node affinities](https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/#node-affinity). CKS uses these built-in Kubernetes scheduling features so you can allocate resources for your workloads:

| Label | Use case |
| - | - |
| `gpu.nvidia.com/class` or `gpu.nvidia.com/model` | Use when you want to select Nodes with a cloud-neutral label. |
| `node.coreweave.cloud/type` | Use when you want to select a CoreWeave-specific instance type. |
| `node.coreweave.cloud/cpu` | Use when you want to select a specific CPU type. |

> [!NOTE]
>
> These labels are mutually exclusive: use the GPU label only to select GPU types, and the CPU label only to select CPU types. You can't explicitly select a specific CPU type for GPU Nodes.

### Example specs

Select one of the following example specs:

> [tab] 8xH100
>
> ```yaml theme={"system"}
> spec:
>   containers:
>   - name: example
>     resources:
>       requests:
>         cpu: 120
>         memory: 1800Gi
>       limits:
>         nvidia.com/gpu: 8
>
>   affinity:
>     nodeAffinity:
>       requiredDuringSchedulingIgnoredDuringExecution:
>         nodeSelectorTerms:
>         - matchExpressions:
>           - key: node.coreweave.cloud/type
>             operator: In
>             values:
>               - gd-8xh100ib-i128
> ```

> [tab] 8xB300
>
> ```yaml theme={"system"}
> spec:
>   containers:
>   - name: example
>     resources:
>       requests:
>         cpu: 180
>         memory: 3800Gi
>       limits:
>         nvidia.com/gpu: 8
>
>   affinity:
>     nodeAffinity:
>       requiredDuringSchedulingIgnoredDuringExecution:
>         nodeSelectorTerms:
>         - matchExpressions:
>           - key: node.coreweave.cloud/type
>             operator: In
>             values:
>               - b300-8x
> ```

> [tab] 8xRTX PRO 6000
>
> ```yaml theme={"system"}
> spec:
>   containers:
>   - name: example
>     resources:
>       requests:
>         cpu: 120
>         memory: 900Gi
>       limits:
>         nvidia.com/gpu: 8
>
>   affinity:
>     nodeAffinity:
>       requiredDuringSchedulingIgnoredDuringExecution:
>         nodeSelectorTerms:
>         - matchExpressions:
>           - key: node.coreweave.cloud/type
>             operator: In
>             values:
>               - rtxp6000-8x
> ```

> [!NOTE]
>
> Kubernetes lets you schedule resources with `requests` and `limits`. When you specify only `limits`, Kubernetes sets the `requests` to the same amount as the limit.

## Manage Node Pool configuration

CKS uses Node Pool configurations to boot Nodes into a desired state. Configurations contain information like the ncore (OS) image and GPU Driver version. A unique identifier called a `nodeProfile` references each configuration.

The following sections describe how CKS generates configurations, how to stage a pending configuration, and how to roll back to a previous one.

To see a Node Pool's active configuration, inspect the `status.nodeProfile` and the [`status.nodeConfigurationRevisions`](https://docs.coreweave.com/products/cks/reference/node-pool#node-configuration-revisions), which displays information for all the configurations staged onto your Node Pool, including the active one.

```yaml title="example-nodepool.yaml" highlight={10-18} theme={"system"}
apiVersion: compute.coreweave.com/v1alpha1
kind: NodePool
metadata:
  name: example-nodepool
spec:
  instanceType: gd-8xh100ib-i128
  targetNodes: 1
status:
  currentNodes: 1
  nodeConfigurationRevisions:
  - activeNodes: 1
    createdAt: "2026-01-05T16:50:23Z"
    nodeProfile: tnt-v2-75e00e7d8b223b100521280041ba22f790591c98
    summary:
    - 'NCore Version: 2.26.0'
    - 'GPU Driver Version: 580.105.08-0ubuntu1'
    - 'K8s Version: v1.35'
  nodeProfile: tnt-v2-75e00e7d8b223b100521280041ba22f790591c98
```

### Generate Node Pool configurations

CKS generates Node Pool configurations based on the Node Pool spec. If you modify the following fields in your Node Pool spec, CKS generates a new configuration for you:

* [`image`](https://docs.coreweave.com/products/cks/reference/node-pool#image)
* [`gpu`](https://docs.coreweave.com/products/cks/reference/node-pool#gpu)

With the default [nodeConfigurationUpdateStrategy.type `OnSpecUpdate`](https://docs.coreweave.com/products/cks/reference/node-pool#node-pool-spec), CKS automatically stages the resulting `nodeProfile` onto your Node Pool as the default `nodeProfile` and onto your Nodes. Existing Nodes may need a reconfigure reboot for the configuration updates to take effect.

When CoreWeave publishes an update for your Node Pool, such as a newer ncore image, CKS generates a new configuration. The `Manual` and default `OnSpecUpdate` strategies leave it pending until you stage it. With `Always`, CKS stages it automatically. See [Stage Node Pool configurations](#stage-node-pool-configurations).

### Stage Node Pool configurations

How CKS applies a new configuration depends on what triggered it and your [`nodeConfigurationUpdateStrategy.type`](https://docs.coreweave.com/products/cks/reference/node-pool#node-pool-spec):

| Strategy | Behavior |
| - | - |
| Manual | Updates require user intervention to stage onto the Node Pool. You can inspect updates in [`pendingNodeConfiguration`](https://docs.coreweave.com/products/cks/reference/node-pool#pending-node-configuration) and apply them with the [CoreWeave Intelligent CLI](https://github.com/coreweave/cwic). |
| OnSpecUpdate | Updates are staged automatically only if triggered by a direct change to the Node Pool spec (for example, modifying the GPU driver version). |
| Always | Updates are staged automatically for both user-initiated spec changes and any available upstream updates. |

To stage a pending configuration, see [CoreWeave Intelligent CLI](#coreweave-intelligent-cli). With `OnSpecUpdate` or `Always`, when you change your Node Pool spec, CKS also incorporates pending CKS-initiated changes into the new staged configuration. With `Manual`, the new configuration remains pending until you promote it.

The following example shows a Node Pool with a CKS-initiated pending configuration that requires manual acceptance.

```yaml title="example-nodepool.yaml" highlight={21-28} theme={"system"}
apiVersion: compute.coreweave.com/v1alpha1
kind: NodePool
metadata:
  name: example-nodepool
spec:
  instanceType: gd-8xh100ib-i128
  nodeConfigurationUpdateStrategy:
    type: Manual
  targetNodes: 1
status:
  currentNodes: 1
  nodeConfigurationRevisions:
  - activeNodes: 1
    createdAt: "2026-01-05T16:50:23Z"
    nodeProfile: tnt-v2-75e00e7d8b223b100521280041ba22f790591c98
    summary:
    - 'NCore Version: 2.26.0'
    - 'GPU Driver Version: 580.105.08-0ubuntu1'
    - 'K8s Version: v1.35'
  nodeProfile: tnt-v2-75e00e7d8b223b100521280041ba22f790591c98
  # This pending configuration must be manually applied to take effect
  pendingNodeConfiguration:
    createdAt: "2026-01-08T14:00:33Z"
    nodeProfile: tnt-v2-8f8ce337708c526919218d747756ae655afe1cda
    summary:
    - 'NCore Version: 2.27.0'
    - 'GPU Driver Version: 580.105.08-0ubuntu1'
    - 'K8s Version: v1.35'
```

Before staging the configuration (CKS-initiated change), inspect the features in the `pendingNodeConfiguration`. Staging the configuration sets it as the active `status.nodeProfile` and tracks it in the `nodeConfigurationRevisions`.

After CKS applies a new configuration to the Node Pool, new Nodes boot into the desired configuration. Existing Nodes in your Node Pool may need a reconfigure reboot to pick up the new configuration. For more information, see [CoreWeave Intelligent CLI](#coreweave-intelligent-cli).

#### User-initiated updates

With `OnSpecUpdate` set as your `nodeConfigurationUpdateStrategy`, when you initiate an update to your Node Pool, CKS automatically stages and applies the resulting new configuration. For example, if you modify the `image` or `gpu` fields in your Node Pool spec, that's a user-initiated update. CKS also stages any Nodes already in the Node Pool with the auto-applied NodeProfile.

CKS automatically stages and applies these user-initiated Node Pool configuration updates regardless of which tools you use to update your Node Pool (including `kubectl`, [Cloud Console](https://docs.coreweave.com/products/cks/nodes/manage.md#modify-a-node-pool-using-the-cloud-console), [GitOps](https://docs.coreweave.com/products/cks/nodes/manage.md#gitops) or [`cwic`](https://docs.coreweave.com/products/cks/nodes/manage#coreweave-intelligent-cli)).

The following example shows a properly configured Node Pool with an automatically staged configuration:

```yaml title="example-nodepool.yaml" highlight={12-16, 18-22} theme={"system"}
apiVersion: compute.coreweave.com/v1alpha1
kind: NodePool
metadata:
  name: example-nodepool
spec:
  instanceType: gd-8xh100ib-i128
  nodeConfigurationUpdateStrategy:
    type: OnSpecUpdate
  targetNodes: 1
  gpu:
    version: "580"
status:
  currentNodes: 1
  nodeConfigurationRevisions:
  - activeNodes: 1
    createdAt: "2026-01-05T16:50:23Z"
    nodeProfile: tnt-v2-75e00e7d8b223b100521280041ba22f790591c98
    summary:
    - 'NCore Version: 2.26.0'
    - 'GPU Driver Version: 580.105.08-0ubuntu1'
    - 'K8s Version: v1.35'
  nodeProfile: tnt-v2-75e00e7d8b223b100521280041ba22f790591c98
```

#### GitOps

GitOps tools such as ArgoCD are the primary way to manage your Node Pool configuration in environments where you don't have a kubeconfig or the correct permissions.

Because CKS auto-stages user-initiated updates to the Node Pool configuration with the default `OnSpecUpdate` strategy, you don't need to take any further action when you update your Node Pool configuration with GitOps aside from [reconfigure rebooting](https://docs.coreweave.com/products/cks/nodes/apply-updates.md) existing Nodes.

The following example shows a git diff of the minimum required YAML updates to set the GPU version to 595:

```diff theme={"system"}
spec:
  gpu:
-    version: "580"
+    version: "595"
```

This workflow is declarative: what you merge in Git is the spec. When the GitOps operation syncs, CKS stages the new Node Profile automatically with `OnSpecUpdate` or `Always`. With `Manual`, inspect and [promote the pending configuration](#coreweave-intelligent-cli) before rebooting existing Nodes.

#### Cloud Console

You can edit the Node Pool manifest in the Cloud Console, including the `spec.gpu.version` field. With `OnSpecUpdate` or `Always`, CKS stages the resulting Node Profile on the Node Pool and its existing Nodes. New Nodes boot into the staged configuration. Existing Nodes need a reconfigure reboot to adopt it. With `Manual`, [promote the pending configuration](#coreweave-intelligent-cli) first.

For GPU manifest examples, see [Update the driver version on an existing Node Pool](https://docs.coreweave.com/products/cks/nodes/gpu-driver-management/update-gpu-driver.md#update-the-driver-version-on-an-existing-node-pool).

#### CoreWeave Intelligent CLI

Use the [CoreWeave Intelligent CLI](https://github.com/coreweave/cwic) (`cwic`) to stage a pending configuration. After you stage the configuration, **only newly created Nodes** use the configuration. You need to initiate a reconfigure reboot on the existing Nodes in the Node Pool to [Apply Node Pool updates](https://docs.coreweave.com/products/cks/nodes/apply-updates.md).

The following steps walk through how to stage a pending configuration:

**1. Find Node Pools with a pending configuration**

To see which Node Pools have a pending configuration:

```bash theme={"system"}
cwic nodepool get [NODEPOOL-NAME]
```

* `NODEPOOL-NAME`: Replace with the name of your Node Pool.

The `PENDING CONFIG` column lists the Node Pools with a new configuration that you can stage to the Node Pool:

```text theme={"system"}
NAME               INSTANCE TYPE      TARGET   QUEUED   INPROGRESS   CURRENT   PENDING CONFIG   STAGED NODES   REQUIRING RECONFIG
example-nodepool   gd-8xl40-i128      1        0        0            1         true             false          0/1
```

**2. Stage the new configuration**

Stage the new Node Pool configuration:

```bash title="Example command" theme={"system"}
cwic nodepool upgrade [NODEPOOL-NAME]
```

* `NODEPOOL-NAME`: Replace with the name of your Node Pool.

You can see the new Node Profile updates and confirm whether to proceed with staging them.

**3. Find Nodes that need the new configuration**

To determine which existing Nodes in the Node Pool need the new configuration:

```bash title="Example command" theme={"system"}
cwic nodepool nodes get [NODEPOOL-NAME] [-r|--requiring-reconfiguration]
```

* `NODEPOOL-NAME`: Replace with the name of your Node Pool.

```text title="Example output (see the RECONFIGURE column)" theme={"system"}
NAME      IP               TYPE               RESERVED   NODEPOOL            READY   ACTIVE   CORDON   RECONFIGURE   VERSION   STATE        PENDING STATE
node-0    10.x.y.z         gd-8xh100ib-i128   org123     example-nodepool    true    true     false    Required      2.26.0    production   none
```

In this example, `node-0` needs a reconfiguration reboot to apply the new Node Profile. For more information on how to perform a reconfigure reboot, see [Apply Node Pool updates](https://docs.coreweave.com/products/cks/nodes/apply-updates.md).

### Roll back to a previous Node configuration

You can roll back to a previous configuration. The [`nodeConfigurationRevisions`](https://docs.coreweave.com/products/cks/reference/node-pool#node-configuration-revisions) enumerates all configurations previously applied to the Node Pool for your reference.

If you want to manually roll back a configuration, you must set your [`nodeConfigurationUpdateStrategy`](https://docs.coreweave.com/products/cks/reference/node-pool#node-pool-spec) to `Manual` so that a new auto-staged configuration doesn't overwrite it.

With the [CoreWeave Intelligent CLI](https://github.com/coreweave/cwic) (`cwic`) `rollback` command, you can omit the `nodeProfile` identifier to roll back to the previous configuration, or you can specify a `nodeProfile` to roll back to an exact configuration.

```bash title="Example command" theme={"system"}
cwic nodepool rollback [NODEPOOL-NAME] [NODEPROFILE]
```

* `NODEPOOL-NAME`: Replace with the name of your Node Pool.
* `NODEPROFILE`: Replace with the Node Profile you want to roll back to.

When you perform a rollback, CKS sets your active `status.nodeProfile` to the desired configuration. Any new Nodes delivered to your Node Pool boot into the rolled-back configuration, and existing Nodes in your cluster may require a reconfigure reboot to pick up the configuration. See [Stage Node Pool configurations](#stage-node-pool-configurations) for more details.

> [!WARNING]
>
> The `nodeConfigurationRevisions` is subject to garbage collection. For any given Node Pool, CKS tracks at most 5 inactive configurations and makes them available for rollback. If 6 or more inactive configurations exist, CKS removes them starting from the oldest.

### Manually update `ncore` image

When an `ncore` image update is available for your Node Pool, CKS creates a pending configuration if your `nodeConfigurationUpdateStrategy.type` is `Manual` or `OnSpecUpdate`. With `Always`, CKS stages the configuration automatically. Image availability depends on your Node Pool configuration, instance type, and Kubernetes version.

To apply a pending update yourself, inspect and stage it, then queue a reconfigure reboot on existing Nodes.

Complete the following steps to update the `ncore` image:

**1. Check the current ncore version on a Node**

To compare the current version with the pending configuration, check the `ncore` versions on your Nodes using `grep` and `ncore-image`. Replace `[NODE-ID]` with your Node ID:

```bash theme={"system"}
kubectl describe node [NODE-ID] | grep ncore-image
```

The output shows the `ncore` image tag and type, for example:

```text theme={"system"}
node.coreweave.cloud/ncore-image-tag=2.24.1
node.coreweave.cloud/ncore-image-type=ofed-5.8-3.0.7.0
```

**2. Check the ncore version across a Node Pool**

To see the `ncore` image for all Nodes in a given Node Pool at once, replace `[NODE-POOL-NAME]` with the name of your Node Pool and run:

```bash theme={"system"}
kubectl get nodes -l compute.coreweave.com/node-pool=[NODE-POOL-NAME] \
-o go-template='{{range .items}}{{.metadata.name}}{{"\t"}}{{"ncore-image-"}}{{index .metadata.labels "node.coreweave.cloud/ncore-image-tag"}}{{"-"}}{{index .metadata.labels "node.coreweave.cloud/ncore-image-type"}}{{"\n"}}{{end}}'
```

**3. Stage the pending configuration and reboot**

Inspect the pending configuration to confirm the target `ncore` version, then [stage the configuration](#stage-node-pool-configurations). To wait for active workloads to stop before rebooting, follow [Apply Node Pool updates](https://docs.coreweave.com/products/cks/nodes/apply-updates.md), which uses the `--safe` and `--reconfigure` flags together.

When the reconfigure reboot completes, the rebooted Nodes run the staged `ncore` image.

If automated configuration updates aren't available in your environment, or if you need help with a large rollout, [contact Support](https://docs.coreweave.com/support.md). Before you contact Support, identify the specific `ncore` image you want to update to so Support can monitor and confirm that Nodes upgrade successfully.

The following sections describe how to test a new image on a subset of Nodes before a full rollout, how to track rollout progress, and how to troubleshoot a rollout that stalls.

#### Test a new image on a canary subset

You can test a staged image by reconfigure rebooting a small batch of existing Nodes. Other existing Nodes keep their current image until they are reconfigured. Staging also changes the default for new and replacement Nodes. To isolate the image from the rest of the pool, use a separate Node Pool.

To test a small batch in the same Node Pool, complete the following steps:

**1. Stage the new configuration**

Stage the new configuration on the Node Pool. See [Stage Node Pool configurations](#stage-node-pool-configurations).

**2. Reboot a small batch of Nodes**

Queue a reconfigure reboot for only the Nodes in your batch. See [Apply Node Pool updates](https://docs.coreweave.com/products/cks/nodes/apply-updates.md).

**3. Confirm which Nodes run the new image**

Confirm which Nodes now run the new image. The `node.coreweave.cloud/ncore-image-tag` label shows each Node's image tag:

```bash theme={"system"}
kubectl get nodes -l compute.coreweave.com/node-pool=[NODE-POOL-NAME] \
  -o custom-columns='NODE:.metadata.name,NCORE:.metadata.labels.node\.coreweave\.cloud/ncore-image-tag'
```

To confirm that your canary workload runs on those Nodes, replace `[NAMESPACE]` with its namespace and check the `NODE` column:

```bash theme={"system"}
kubectl get pods -n [NAMESPACE] -o wide
```

**4. Validate and roll out to the remaining Nodes**

Validate the canary, then reconfigure reboot the remaining Nodes in small batches. Validate each batch before proceeding to limit how many additional Nodes are exposed to a problem with the new image.

To confirm that every Node in the Node Pool has adopted the new image, see [Track rollout progress](#track-rollout-progress).

#### Track rollout progress

After you stage a configuration, inspect the `NodeReconfigurationRequired` condition on the Node Pool.

For the condition's status values and reasons, see the [Node Pool reference](https://docs.coreweave.com/products/cks/reference/node-pool.md#condition-nodereconfigurationrequired).

To check the condition status, reason, and message, replace `[NODE-POOL-NAME]` with the name of your Node Pool and run:

```bash theme={"system"}
kubectl get nodepool [NODE-POOL-NAME] \
  -o jsonpath='{range .status.conditions[?(@.type=="NodeReconfigurationRequired")]}{.status}{"\t"}{.reason}{"\t"}{.message}{"\n"}{end}'
```

An `InternalError` reason, an `Unknown` status, or no output doesn't confirm completion. A `False` status alone also doesn't confirm completion because it can accompany `InternalError`.

Before declaring the rollout complete, inspect the Node Pool:

```bash theme={"system"}
kubectl get nodepool [NODE-POOL-NAME] -o yaml
```

Confirm that `status.nodeProfile` matches the configuration you intended to apply and `status.currentNodes` matches your expected Node count. Confirm that the condition reason is `AllNodesUpToDate`. Check the per-Node image labels with the command in [Test a new image on a canary subset](#test-a-new-image-on-a-canary-subset), and validate your workloads. Configuration adoption alone doesn't confirm workload health.

#### Troubleshoot a stuck or blocked configuration

If a rollout doesn't complete, check for the following conditions:

* A Node that remains in the `production-reconfigure-powercycle-test` state might still be rebooting or running validation. For timing and validation guidance, see [Apply Node Pool updates](https://docs.coreweave.com/products/cks/nodes/apply-updates.md#queue-a-reconfigure-reboot). If the rollout appears stuck, inspect the Node conditions and events with `kubectl describe node [NODE-ID]`. [Contact Support](https://docs.coreweave.com/support.md) with the Node name and command output for help diagnosing the delay.
* A `nodeConfigurationRevisions` entry with `disabled: true` means delivery of Nodes using that configuration is disabled. Repeated delivery or reconfiguration failures can trigger this state. [Contact Support](https://docs.coreweave.com/support.md) to investigate the cause and restore delivery.

## Delete a Node Pool using the Cloud Console

**1. Open the Node Pools page**

In the Cloud Console, navigate to the Node Pools page (`https://console.coreweave.com/zones/[ZONE-NAME]/clusters/[CLUSTER-NAME]/node-pools`).

**2. Open the delete confirmation**

Click the vertical dot menu beside the Node Pool to delete, then click **Delete** to open the confirmation modal.

![Screenshot showing the modal for deleting Node Pools](https://mintcdn.com/coreweave-dbfa0e8d/Diszsi3qOqeLxowx/products/cks/_media/node-pool-edit-delete.png?fit=max\&auto=format\&n=Diszsi3qOqeLxowx\&q=85\&s=13ae9fc611afa7a6636e634585272dcf)

**3. Confirm the deletion**

Enter the name of the Node Pool to confirm deletion.

The dashboard updates immediately, removing the deleted Node Pool from the list.

## Delete a Node Pool using Kubernetes

To delete a Node Pool using Kubernetes, delete the Node Pool resource directly using `kubectl`:

```bash theme={"system"}
kubectl delete nodepool example-nodepool
```

Deleting the `nodepool` resource first removes all Nodes associated with the Node Pool from the cluster, then deletes the Node Pool resource itself.

> [!WARNING]
>
> To avoid data loss when removing Node Pools, first ensure nothing is running in the Node Pool before you delete it. CKS doesn't wait for workloads to complete before removing Nodes.

## Next steps

* [Reboot Nodes](https://docs.coreweave.com/products/cks/nodes/reboot.md) to reboot Nodes manually.
* [Apply Node Pool updates](https://docs.coreweave.com/products/cks/nodes/apply-updates.md) to apply Node Pool updates by queuing a reconfigure reboot.
* [Connect to a Node](https://docs.coreweave.com/products/cks/nodes/connect.md) to troubleshoot issues with a Node.
