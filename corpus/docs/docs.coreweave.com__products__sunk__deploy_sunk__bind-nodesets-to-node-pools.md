# Bind NodeSets to Node Pools for SUNK Standard

Source: https://docs.coreweave.com/products/sunk/deploy_sunk/bind-nodesets-to-node-pools

# Bind NodeSets to Node Pools for SUNK Standard

> Match Node Pool labels and taints to NodeSet affinity and tolerations so slurmd Pods land on the intended Nodes

[SUNK Standard](https://docs.coreweave.com/products/sunk.md)

A SUNK NodeSet places one `slurmd` Pod on each Kubernetes Node it selects. The NodeSet's `affinity`, `tolerations`, and resource requests determine which Nodes it can select. A CoreWeave Kubernetes Service (CKS) Node Pool controls the other side of that decision. It applies the labels and taints in its spec to every Node it delivers.

Those two sides have to agree. If a Node Pool taints its Nodes and the NodeSet doesn't tolerate the taint, the NodeSet treats those Nodes as infeasible and the Node Pool sits idle. If the NodeSet has no affinity at all, its Pods spread across whatever production Nodes they fit on, including Nodes you meant to reserve for something else.

This guide covers both approaches to binding the two together, how to make a NodeSet track Node Pool scale automatically, and how to verify the result. By the end, the NodeSet's `slurmd` Pods run only on Nodes from the Node Pool you picked for them.

> [!NOTE]
>
> In SUNK, Slurm **nodes** run in Kubernetes Pods. These aren't the same as Kubernetes **Nodes**, which are the worker machines that run the Pods. To distinguish between the two, this documentation capitalizes Kubernetes Nodes, while Slurm nodes aren't capitalized.

## How NodeSet scheduling uses Node Pool metadata

A NodeSet evaluates every Kubernetes Node in the cluster and counts the ones it could place a Pod on as *feasible*. Three things narrow that count:

* **Affinity.** The NodeSet reads only `affinity.nodeAffinity.requiredDuringSchedulingIgnoredDuringExecution`. It ignores preferred affinity and every other affinity section, so a preference has no effect on feasibility.
* **Tolerations.** A tainted Node is infeasible unless the NodeSet tolerates each of its taints.
* **Resource requests.** A Node with too little allocatable CPU, memory, or accelerator capacity is infeasible. For that reason, a stray non-Slurm Pod on a Node can make that Node infeasible for the NodeSet.

Two fields on the Node Pool spec supply the metadata to match against. `nodeLabels` applies labels to every Node in the pool, and `nodeTaints` applies taints. CKS applies both when it delivers a Node, so Nodes added by a later scale-up carry them without any manual step. For the full Node Pool spec, see [Create a Node Pool](https://docs.coreweave.com/products/cks/nodes/create.md).

You can bind a NodeSet to a Node Pool in two ways:

* [Target a Node Pool by name](#target-a-node-pool-by-name) uses a label CKS maintains on every Node. This approach requires no changes to the Node Pool, and it's the right choice when the correct hardware is the only requirement.
* [Dedicate a Node Pool to a NodeSet](#dedicate-a-node-pool-to-a-nodeset) adds a custom label and a matching taint to the Node Pool spec. Choose this when the Nodes must also repel Pods that aren't part of the NodeSet.

## Prerequisites

This guide applies to SUNK Standard, where you deploy the Slurm Helm chart and own the `compute.nodes` values. On a [SUNK Self-Service cluster](https://docs.coreweave.com/products/sunk/deploy_sunk/create-sunk-cluster.md) created from a `SunkCluster` resource, the [out-of-band operator](https://docs.coreweave.com/products/sunk/discover_sunk/self-service-architecture.md) creates the Node Pools and NodeSets and keeps their counts in sync, so you don't bind them yourself.

Before you begin, make sure you have the following:

* A [CKS cluster](https://docs.coreweave.com/products/cks/clusters/create.md) with at least one [Node Pool](https://docs.coreweave.com/products/cks/nodes/create.md).
* A SUNK cluster deployed from the Slurm Helm chart, and write access to its values.
* `kubectl` configured against the cluster, with an [API access token](https://docs.coreweave.com/security/authn-authz/managed-auth/api-access.md). Editing or patching a Node Pool needs the CKS Admin role. A token with only CKS Viewer can read Node Pools but can't change them. See [IAM access policies](https://docs.coreweave.com/security/iam/access-policies.md).

## Target a Node Pool by name

CKS labels every Node with the name of the Node Pool that delivered it, using the key `compute.coreweave.com/node-pool`. Matching that label in a NodeSet's affinity binds the NodeSet to the pool without editing the Node Pool spec.

Replace `[NODE-POOL-NAME]` with the name of your Node Pool:

```yaml title="Bind a NodeSet to one Node Pool" theme={"system"}
compute:
  nodes:
    cpu-batch:
      enabled: true
      affinity:
        nodeAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            nodeSelectorTerms:
              - matchExpressions:
                  - key: compute.coreweave.com/node-pool
                    operator: In
                    values:
                      - [NODE-POOL-NAME]
```

You can match this label even though [CKS rejects user-provided labels](https://docs.coreweave.com/products/cks/clusters/scheduling/workload-scheduling.md#user-provided-labels) in the `coreweave.com` and `coreweave.cloud` namespaces. That restriction governs labels you *create*. CKS sets this one itself, and you can read it in a selector.

When capacity for one instance type is split across several Node Pools, list every pool the NodeSet should use. A NodeSet that names only one pool leaves the other pool's Nodes infeasible, which looks like missing capacity. Replace `[NODE-POOL-NAME-A]` and `[NODE-POOL-NAME-B]` with your Node Pool names:

```yaml title="Bind a NodeSet to several Node Pools" theme={"system"}
compute:
  nodes:
    cpu-batch:
      enabled: true
      affinity:
        nodeAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            nodeSelectorTerms:
              - matchExpressions:
                  - key: compute.coreweave.com/node-pool
                    operator: In
                    values:
                      - [NODE-POOL-NAME-A]
                      - [NODE-POOL-NAME-B]
```

This approach steers the NodeSet onto the right Nodes, but it doesn't reserve them. Any other Pod that fits and tolerates the Node's taints can still schedule there. To reserve the Nodes, add a taint as described in the following section.

## Dedicate a Node Pool to a NodeSet

A custom label and a matching taint on the Node Pool do two jobs at once. The label gives the NodeSet something to select, and the taint keeps every Pod that doesn't tolerate it off those Nodes.

This matters most for CPU-only Slurm nodes. A CPU `slurmd` Pod requests only a fraction of the Node, so unrelated CPU workloads can fit alongside it. When a Slurm job then starts on that Node, SUNK's [`sunk.coreweave.com/lock` taint](https://docs.coreweave.com/products/cks/clusters/scheduling/workload-scheduling#the-sunk-/lock-taint) evicts them. A taint on the pool prevents them from landing there at all. If you run GPU Pods with small CPU and memory requests, the same reasoning applies to GPU Nodes.

This takes an edit on each side. The following sections cover the Node Pool spec first, then the NodeSet fields that match it.

### Label and taint the Node Pool

Add `nodeLabels` and `nodeTaints` to the Node Pool spec, using the same key for both so a single value controls selection and repulsion:

```yaml title="slurm-cpu-nodepool.yaml" theme={"system"}
apiVersion: compute.coreweave.com/v1alpha1
kind: NodePool
metadata:
  name: slurm-cpu
spec:
  computeClass: default
  autoscaling: false
  instanceType: cd-gp-a192-genoa
  maxNodes: 0
  minNodes: 0
  targetNodes: 8
  nodeLabels:
    sunk.example.com/node: "true"
  nodeTaints:
    - key: sunk.example.com/node
      value: "true"
      effect: NoSchedule
```

Apply it:

```bash theme={"system"}
kubectl apply -f slurm-cpu-nodepool.yaml
```

Pick a label prefix in a domain you control. CKS reserves the `coreweave.com` and `coreweave.cloud` namespaces for its own labels. A Node Pool that sets a key like `sunk.coreweave.com/node` is still accepted, but the label never reaches the Nodes, and the only signal is a [`CWNodePoolMetadataSanitized`](https://docs.coreweave.com/products/cks/reference/node-pool#events) warning Event on the Node Pool. Replace `sunk.example.com` throughout these examples with your own domain.

Set labels and taints on the Node Pool rather than on individual Nodes. A label set with `kubectl label node` disappears when CKS replaces that Node. Dedicating a Node manually also means cordoning it, draining it, labeling and tainting it, then uncordoning it, once per Node. CKS applies Node Pool metadata when it delivers a Node, reconciles later edits to `nodeLabels` and `nodeTaints` onto the Nodes already in the pool, and reapplies the metadata when a Node is replaced.

> [!WARNING]
>
> A Node Pool can't transfer a Node to another Node Pool. Moving capacity between pools means scaling one pool down and the other up. Scaling down destroys the Nodes in that pool, and scaling up provisions fresh Nodes. Plan pool boundaries around groupings you expect to keep.

### Match the label and taint in the NodeSet

The NodeSet requires an affinity for the label and a toleration for the taint. Both fields sit on the node definition under `compute.nodes`, and both pass straight through to the `slurmd` Pod template:

```yaml title="Match both sides of the Node Pool metadata" theme={"system"}
compute:
  nodes:
    cpu-batch:
      enabled: true
      tolerations:
        - key: sunk.example.com/node
          operator: Exists
      affinity:
        nodeAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            nodeSelectorTerms:
              - matchExpressions:
                  - key: sunk.example.com/node
                    operator: Exists
      gresGpu: null
      resources:
        limits:
          memory: [MEMORY-LIMIT]
        requests:
          cpu: "[CPU-REQUEST]"
          memory: [MEMORY-REQUEST]
```

Size `resources` to the instance type the Node Pool provisions, leaving headroom below the Node's total capacity for DaemonSets and system overhead. A `slurmd` Pod whose requests exceed a Node's allocatable capacity makes that Node infeasible, which produces the same empty Node Pool as a label mismatch. For per-Node capacity, see the [CPU instance](https://docs.coreweave.com/platform/instances/cpu-instances.md) and [GPU instance](https://docs.coreweave.com/platform/instances/gpu-instances.md) specifications.

`operator: Exists` matches any value for the key, so you don't have to keep the toleration's value in sync with the taint's. When one label key carries several meaningful values, use `operator: In` with an explicit `values` list.

The `gresGpu: null` line matters on a CPU-only definition. [`node.gresGpu`](https://docs.coreweave.com/products/sunk/deploy_sunk/configure-compute-nodes#node-specific-options) sets the Slurm GPU generic resource for the node. Setting it to `null` clears any value the definition would otherwise inherit from a [layer](#share-matching-rules-across-nodesets), so Slurm doesn't advertise GPUs on a CPU node.

With both sides in place, the NodeSet places `slurmd` Pods only on the Node Pool's Nodes.

> [!WARNING]
>
> Set scheduling constraints with `affinity`, never with `nodeSelector`. A `nodeSelector` on a node definition doesn't reach the generated Pod template, so the NodeSet schedules as though no constraint existed. The configuration looks valid and the failure is silent. A NodeSet reporting more Nodes than its target Node Pool contains is the usual symptom.

## Let the NodeSet follow Node Pool scale

If you leave `replicas` unset, the NodeSet sets its desired count to the number of feasible Nodes. Once affinity and tolerations bind the NodeSet to one Node Pool, scaling that pool is the only action needed.

This matters because Node Pool size and NodeSet size are otherwise independent. The Node Pool controls how many Kubernetes Nodes exist, and the NodeSet controls how many of them run a `slurmd` Pod. Scaling the pool while `replicas` stays fixed adds Nodes that never run a `slurmd` Pod, which is a common surprise after a scale-up.

```yaml title="Track Node Pool size automatically" theme={"system"}
compute:
  nodes:
    cpu-batch:
      enabled: true
      # replicas omitted: desired count tracks the feasible Node count
      tolerations:
        - key: sunk.example.com/node
          operator: Exists
      affinity:
        nodeAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            nodeSelectorTerms:
              - matchExpressions:
                  - key: sunk.example.com/node
                    operator: Exists
```

To scale, change `targetNodes` on the Node Pool. Replace `[NODE-POOL-NAME]` with your Node Pool name. The patch body is JSON, so replace `[N]` and its brackets with a bare number:

```bash theme={"system"}
kubectl patch nodepool [NODE-POOL-NAME] --type=merge -p '{"spec":{"targetNodes":[N]}}'
```

This applies to Node Pools that set `targetNodes`. A [rack-based Node Pool](https://docs.coreweave.com/products/cks/nodes/create.md#rack-based-node-pools), such as GB200 or GB300, scales with `targetRacks` instead, since the two fields are mutually exclusive.

An older pattern sets `replicas` to a deliberately large number, such as `1000`, to the same effect. The desired count exceeds the feasible count, so the feasible count is the binding constraint. Omitting `replicas` expresses the same intent without an arbitrary number to maintain.

To cap a NodeSet below the size of its Node Pool, set an explicit `replicas` value. You might do this to reserve Nodes for Kubernetes workloads instead of Slurm. `replicas` sets the desired count, and the feasible Node count still limits how many Pods the NodeSet places, so the effective size is whichever of the two is lower.

### Node Pool autoscaling

Keep `autoscaling: false` on a Node Pool that a NodeSet uses, and scale it by changing `targetNodes`, or `targetRacks` on a rack-based Node Pool. SUNK doesn't support [autoscaling Node Pools](https://docs.coreweave.com/products/cks/nodes/autoscaling.md), because a NodeSet gives the autoscaler no signal to act on:

* **The NodeSet doesn't trigger a scale-up.** The Cluster Autoscaler adds Nodes when Pods are pending because no existing Node can fit them. The NodeSet controller creates a `slurmd` Pod only for a Node it already counts as feasible, and pins that Pod to the Node by name. A `slurmd` Pod never waits for a Node that doesn't exist yet, so the NodeSet never causes the Node Pool to grow, however many jobs are queued in Slurm.
* **The NodeSet follows the Node Pool, not the other way around.** With `replicas` omitted, the desired count is the number of feasible Nodes that already exist. The NodeSet reacts to the Node Pool's size but never requests a change to it, so the NodeSet count can't push `targetNodes` toward `minNodes` or `maxNodes`.

## Share matching rules across NodeSets

When several NodeSets target the same Node Pool, factor the affinity and tolerations into a node definition that other definitions include by name. A definition used as a shared layer must omit `enabled`. Setting `enabled: true` on it deploys it as a NodeSet of its own, and every other definition that references it by name silently stops picking up its rules, since an enabled definition is no longer available to be included as a layer:

```yaml title="A reusable matching layer" theme={"system"}
compute:
  nodes:
    # Shared layer. No `enabled` key, so this is never deployed on its own.
    slurm-cpu:
      tolerations:
        - key: sunk.example.com/node
          operator: Exists
      affinity:
        nodeAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            nodeSelectorTerms:
              - matchExpressions:
                  - key: sunk.example.com/node
                    operator: Exists
      gresGpu: null

    cpu-a192-genoa:
      enabled: true
      definitions:
        - slurm-cpu
      staticFeatures:
        - cpu
        - amd
        - epyc
      resources:
        limits:
          memory: [MEMORY-LIMIT]
        requests:
          cpu: "[CPU-REQUEST]"
          memory: [MEMORY-REQUEST]
```

Layers combine rather than overwrite, which is what makes this composition work:

* **Tolerations accumulate.** SUNK adds each layer's tolerations to the list, so a NodeSet tolerates the taints from every layer it includes plus its own.
* **Match expressions merge by key and combine with a logical AND.** SUNK merges the match expressions from each layer into a single `nodeSelectorTerm`, keyed on the expression's `key`. Expressions on *different* keys both survive the merge and apply together. A NodeSet that includes a layer selecting `sunk.example.com/node` and also sets its own expression on `gpu.nvidia.com/class` requires both. Expressions on the *same* key don't cleanly replace the inherited one. The merge unions the two `values` lists, and it can leave your own expression in place next to the merged one. Kubernetes requires every expression in the term, so the result is narrower than either one alone. Set a given key in one layer only.
* **Every NodeSet inherits a production Node requirement.** SUNK's base definition contributes a match expression requiring `node.coreweave.cloud/state` to be `production`. Because expressions on other keys merge alongside it, your affinity narrows that selection rather than replacing it. Don't write your own expression on `node.coreweave.cloud/state`. A same-key expression can't cleanly override the inherited one, so the result rarely matches what you intended. For what the other states mean, see [Node lifecycle labels](https://docs.coreweave.com/products/cks/clusters/scheduling/workload-scheduling.md#node-lifecycle-labels).

SUNK resolves layers in the order listed under `definitions` and applies the NodeSet's own values last, so a NodeSet can override any value it inherits.

> [!WARNING]
>
> Only the first entry under `nodeSelectorTerms` takes part in this merge. Kubernetes treats multiple terms as a logical OR, but SUNK drops a layer's second and later terms when it merges them. Keep each definition to a single `nodeSelectorTerm` and express alternatives with `operator: In` and multiple `values`.

For more on composing node definitions, see [Custom node definitions](https://docs.coreweave.com/products/sunk/deploy_sunk/configure-compute-nodes.md#custom-node-definitions).

## Verify the binding

Deploy the Helm release, then compare what the Node Pool delivered against what the NodeSet can use.

**1. Confirm the Node Pool reached its target**

Replace `[NODE-POOL-NAME]` with your Node Pool name:

```bash theme={"system"}
kubectl get nodepool [NODE-POOL-NAME]
```

`CURRENT` should equal `TARGET`. If it doesn't, the gap is a Node Pool problem rather than a matching problem. See [Node Pool status](https://docs.coreweave.com/products/cks/nodes/nodepool-status.md).

**2. Check that the Nodes carry the expected metadata**

```bash theme={"system"}
kubectl get nodes -l sunk.example.com/node=true
```

An empty result means the labels aren't reaching the Nodes. Confirm `nodeLabels` is set on the Node Pool spec, then check the Node Pool's Events:

```bash theme={"system"}
kubectl describe nodepool [NODE-POOL-NAME]
```

A `CWNodePoolMetadataSanitized` warning means CKS dropped the label because its key sits in a reserved namespace. Pick a key in a domain you control and reapply. For every Event a Node Pool can fire, see [Node Pool reference](https://docs.coreweave.com/products/cks/reference/node-pool.md#events).

**3. Compare NodeSet feasibility against the Node Pool**

Replace `[NAMESPACE]` with your Slurm namespace:

```bash theme={"system"}
kubectl get nodeset -n [NAMESPACE]
```

```text title="Example output" theme={"system"}
NAME               DESIRED   FEASIBLE   CURRENT   READY   UP-TO-DATE   RUNNING   DRAIN   MISSCHEDULED   UNAVAILABLE   AGE
slurm-cpu-batch    8         8          8         8       8            0         0       0              0             12m
```

`FEASIBLE` equal to the Node Pool's `CURRENT` means the matching is correct. `FEASIBLE` lower than `CURRENT` means some Nodes in the pool don't satisfy the NodeSet's affinity, tolerations, or resource requests. For what each column means, see [NodeSet status](https://docs.coreweave.com/products/sunk/discover_sunk/nodeset.md#status).

**4. Confirm Pod placement**

SUNK labels each `slurmd` Pod with `app.kubernetes.io/instance`, set to the NodeSet name. Replace `[NODESET-NAME]` with the name from the previous step:

```bash theme={"system"}
kubectl get pods -n [NAMESPACE] -l app.kubernetes.io/instance=[NODESET-NAME] -o wide
```

Every Pod should be on a Node from the intended Node Pool. A Pod on any other Node means the constraint isn't reaching the Pod template, usually because the node definition sets it with `nodeSelector` instead of `affinity`.

**5. Confirm Slurm sees the nodes**

From a Slurm login node:

```bash theme={"system"}
sinfo
```

The node count for the partition should match the NodeSet's `READY` count. See [Connect to a Slurm login node](https://docs.coreweave.com/products/sunk/access_sunk/connect-to-slurm-login-node.md).

## Troubleshoot

The following table maps the mismatch you see to its usual cause.

| Symptom | Likely cause | Fix |
| - | - | - |
| `FEASIBLE` is `0` and the Node Pool is healthy | The NodeSet's affinity doesn't match any Node label, or it doesn't tolerate the Node Pool's taint. | Compare the NodeSet's `affinity` and `tolerations` keys against `kubectl describe node` output for one Node in the pool. |
| `FEASIBLE` is short by exactly the Node count of another Node Pool | The NodeSet names one pool, but the instance type's capacity spans several. | Add the other pool to `values` with `operator: In`, or match a label both pools share. |
| `DESIRED` is lower than `FEASIBLE` after a Node Pool scale-up | `replicas` caps the NodeSet below the Node Pool size. | Omit `replicas`, or raise it. |
| A Node Pool with `autoscaling: true` doesn't grow while Slurm jobs are pending | `slurmd` Pods are created only for existing Nodes, so they never leave the pending Pods the Cluster Autoscaler scales on. | Set `autoscaling: false` and scale the Node Pool with `targetNodes`. See [Node Pool autoscaling](#node-pool-autoscaling). |
| `FEASIBLE` is one or two below the Node Pool's `CURRENT` | A non-Slurm Pod occupies those Nodes and consumes the resources the `slurmd` Pod requests. | Add a taint to the Node Pool, or fix the other workload's affinity to exclude these Nodes. Drain the Node to evict the Pod already there. |
| The NodeSet uses more Nodes than the target Node Pool contains | The node definition sets the constraint with `nodeSelector`, which doesn't reach the Pod template. | Move the constraint into an `affinity` block with `requiredDuringSchedulingIgnoredDuringExecution`. |
| `MISSCHEDULED` is above `0` | Pods sit on Nodes that no longer match the NodeSet's selector, usually after a label or affinity change. | Confirm the intended Nodes, then let the NodeSet replace the Pods. |
| Nodes lose their labels after a Node Pool scale event | The labels were applied to individual Nodes instead of the Node Pool spec. | Move the labels and taints into the Node Pool's `nodeLabels` and `nodeTaints`. |
| A label added to the Node Pool never appears on any Node | The label key is in the reserved `coreweave.com` or `coreweave.cloud` namespace, so CKS drops it. | Check for a `CWNodePoolMetadataSanitized` Event on the Node Pool, then move the label to a domain you control. |

For deeper NodeSet triage, see [NodeSet status](https://docs.coreweave.com/products/sunk/discover_sunk/nodeset.md#status). For Node Pool conditions, capacity, and quota, see [Node Pool status](https://docs.coreweave.com/products/cks/nodes/nodepool-status.md).

## Related pages

* [Create a Node Pool](https://docs.coreweave.com/products/cks/nodes/create.md) for the full Node Pool spec, including `nodeLabels` and `nodeTaints`.
* [Configure compute nodes for SUNK Standard](https://docs.coreweave.com/products/sunk/deploy_sunk/configure-compute-nodes.md) for every field available on a node definition.
* [Workload scheduling on CKS](https://docs.coreweave.com/products/cks/clusters/scheduling/workload-scheduling.md) for reserved label namespaces, CKS taints, and the SUNK lock taint.
* [NodeSet](https://docs.coreweave.com/products/sunk/discover_sunk/nodeset.md) for how the NodeSet controller selects Nodes and reports status.
* [Node Pool status](https://docs.coreweave.com/products/cks/nodes/nodepool-status.md) for diagnosing a Node Pool that hasn't reached its target.
