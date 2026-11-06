# Node Pool status

Source: https://docs.coreweave.com/products/cks/nodes/nodepool-status

# Node Pool status

> Understand Node Pool status fields, conditions, and events to diagnose scaling and capacity problems

This page explains the Node Pool status fields and how to use them to diagnose a Node Pool that isn't at its target, whether Nodes are missing or a scale-down is stuck.

For the complete field and event schema, see the [Node Pool reference](https://docs.coreweave.com/products/cks/reference/node-pool.md).

## Node Pool fields

The Node Pool fields show the desired state and status of the Nodes in a Node Pool.

To see these fields, run `kubectl get nodepool`.

| Column | Value | Where it's defined |
| - | - | - |
| `TARGET` | The number of Nodes you want in the Node Pool. You set this value, or the autoscaler sets it within `minNodes` and `maxNodes`. | [`spec.targetNodes`](https://docs.coreweave.com/products/cks/reference/node-pool#node-pool-spec) |
| `CURRENT` | The number of Nodes that have been booted and registered with the Node Pool and are present in the cluster. | [`status.currentNodes`](https://docs.coreweave.com/products/cks/reference/node-pool#node-pool-status) |
| `PREFILL` | The number of Nodes in the Node Pool that are marked for prefill and being replaced. Populated when [prefill](https://docs.coreweave.com/products/cks/nodes/nodes-and-node-pools.md#node-pool-prefill) is enabled. | [`status.prefillNodes`](https://docs.coreweave.com/products/cks/reference/node-pool#node-pool-status) |
| `INPROGRESS` | The number of Nodes that have been assigned to the Node Pool but haven't yet booted or registered with the Node Pool. | [`status.inProgress`](https://docs.coreweave.com/products/cks/reference/node-pool#node-pool-status) |
| `QUEUED` | The number of Nodes that have been requested but not yet assigned, because they are waiting for capacity. | [`status.queuedNodes`](https://docs.coreweave.com/products/cks/reference/node-pool#node-pool-status) |
| `VALIDATED` | The result of the most recent Node Pool configuration validation. | [`status.conditions`](https://docs.coreweave.com/products/cks/reference/node-pool#condition-validated) |
| `CAPACITY` | The result of the most recent capacity check for the instance type. | [`status.conditions`](https://docs.coreweave.com/products/cks/reference/node-pool#condition-capacity) |
| `QUOTA` | The result of the most recent quota check for the instance type and zone. | [`status.conditions`](https://docs.coreweave.com/products/cks/reference/node-pool#condition-quota) |

### Example output

The following is an example output from running `kubectl get nodepool`.

```text title="Example output" theme={"system"}
NAME               INSTANCE TYPE      TARGET   QUEUED   INPROGRESS   CURRENT   PREFILL   VALIDATED   CAPACITY                 QUOTA   AGE
example-nodepool   gd-8xh100ib-i128   2        0        0            2         0         Valid       Sufficient               Under   24h
nodepool-2         cd-hp-a96-genoa    2        1        0            1         0         Valid       QueuedAwaitingCapacity   Under   2d22h
nodepool-3         gd-8xh100ib-i128   3        0        1            2         0         Valid       Sufficient               Under   2d15h
```

The following table outlines each Node Pool's state:

| Node Pool | State | What the status shows |
| - | - | - |
| `example-nodepool` | Healthy | `CURRENT` matches `TARGET`, and capacity and quota are both satisfied. |
| `nodepool-2` | Waiting for capacity | Short one Node. One Node is `QUEUED`, and `CAPACITY` shows `QueuedAwaitingCapacity`. |
| `nodepool-3` | Delivering | Short one Node. One Node is `INPROGRESS` and still booting. |

* The `VALIDATED`, `CAPACITY`, and `QUOTA` columns summarize the Node Pool's conditions.
* In a healthy, fully delivered Node Pool, `CURRENT` equals `TARGET`, and both `INPROGRESS` and `QUEUED` are `0`.
* `PREFILL` counts the Nodes marked for prefill and being replaced. It is `0` unless [prefill](https://docs.coreweave.com/products/cks/nodes/nodes-and-node-pools.md#node-pool-prefill) is enabled and one or more Nodes are being replaced. To see the prefill state of an individual Node, check its `Prefill` condition. See [Prefill condition reasons](https://docs.coreweave.com/products/cks/reference/node-pool.md#prefill-condition-reasons).
* While a Node Pool is scaling up, the difference between `CURRENT` and `TARGET` is split between `INPROGRESS` (Nodes that are booting) and `QUEUED` (Nodes that are waiting for capacity). Note that a new Node can take up to 15 minutes to boot before it counts toward `CURRENT`.

### Rack-based Node Pool fields

For [rack-based instance types](https://docs.coreweave.com/products/cks/nodes/create.md#rack-based-node-pools) such as GB200 and GB300, the Node Pool also tracks rack counts, where each rack contains 18 Nodes. These fields are populated only for rack-based instance types and appear only in the wide output. To see them, use `kubectl get nodepool -o wide`:

| Column | Value | Where it's defined |
| - | - | - |
| `TARGET-RACKS` | The number of racks requested for the Node Pool. | [`status.rackStatus.target`](https://docs.coreweave.com/products/cks/reference/node-pool#rackstatus) |
| `CURRENT-RACKS` | The number of racks present in the cluster for the Node Pool. | [`status.rackStatus.current`](https://docs.coreweave.com/products/cks/reference/node-pool#rackstatus) |
| `QUEUED-RACKS` | The number of racks queued and waiting for capacity to join the Node Pool. | [`status.rackStatus.queued`](https://docs.coreweave.com/products/cks/reference/node-pool#rackstatus) |

### Node Pool full status

For the full status of a single Node Pool, including its conditions and recent events, use `describe`:

```bash title="Example command" theme={"system"}
kubectl describe nodepool [NODE-POOL-NAME]
```

Replace `[NODE-POOL-NAME]` with the name of your Node Pool.

Each condition answers one question about the Node Pool. The conditions most useful for diagnosing missing Nodes are the following.

| Condition | Status values you act on | What it tells you |
| - | - | - |
| `Validated` | `Valid`, `Invalid` | Whether the Node Pool configuration is accepted. `Invalid` blocks delivery, for example an unsupported instance type. |
| `Capacity` | `Sufficient`, `Partial`, `NoneAvailable`, `QueuedAwaitingCapacity` | Whether enough Nodes of the requested instance type are available to fill the request. |
| `Quota` | `Under`, `Over`, `NotSet` | Whether the request fits within your organization's quota for the instance type and zone. |
| `AtTarget` | `TargetMet`, `UnderTarget`, `OverTarget` | Whether the Node Pool has the requested number of Nodes. |

A healthy Node Pool shows `Validated: Valid`, `Capacity: Sufficient`, `Quota: Under`, and `AtTarget: TargetMet`.
For the complete list of conditions and every possible status value, see [Node Pool conditions](https://docs.coreweave.com/products/cks/reference/node-pool.md#node-pool-conditions).

### Prefill status

The `PrefillEnabled` condition reports whether prefill is functional for the Node Pool. CKS checks the default configuration when you omit `spec.prefill`.

Use `kubectl describe nodepool [NODE-POOL-NAME]` to inspect this condition. The `VALIDATED` column in `kubectl get nodepool` reports the separate `Validated` condition.

| Status | Meaning | Next step |
| - | - | - |
| `True` | Prefill is enabled and the Node Pool's configuration supports it. This doesn't mean any prefill operations are in progress. | No configuration change is needed. |
| `False` | Prefill is explicitly disabled, has an invalid timeout, or isn't supported for the Node Pool's instance type, autoscaling, or compute class. CKS doesn't mark new Nodes for prefill. | Read the `reason` and `message`. A reason that starts with `Unsupported` means that CKS turned off prefill automatically, and no action is needed. If you want to use prefill, enable it or change the setting that the `reason` identifies. |

For specific reasons and next steps, see [Prefill status reasons](https://docs.coreweave.com/products/cks/reference/node-pool.md#condition-prefillenabled).

## Common capacity and quota states

The bottom of `kubectl describe nodepool [NODE-POOL-NAME]` lists recent events. The following events and condition states explain most cases where a Node Pool does not reach its target.

| Event or condition | What it means | What to do |
| - | - | - |
| `QueuedAwaitingCapacity` (Capacity condition) | The Node Pool requested more Nodes than are free in the zone, so CKS queued the request. CKS fills queued requests automatically as capacity becomes available. `Quota: Under` means you are allowed to request more Nodes, not that they are available right now. For rack-scale instance types such as GB200 and GB300, Nodes deliver in complete rack units. The pool can queue while it waits for a full rack even when some capacity exists in the zone. | Confirm the `Quota` condition is `Under`. A queue can stay long while a zone is oversubscribed, so a queued request on its own isn't a fault. If `QUEUED` doesn't move and no Nodes reach `INPROGRESS`, [contact support](https://docs.coreweave.com/support.md). |
| `CWInsufficientCapacity` (event) | Not enough Nodes of the requested instance type are available in the zone to fully satisfy `targetNodes`. CKS keeps the Nodes it could assign, continues retrying, and assigns the rest automatically as capacity returns. The `Capacity` condition shows `Partial` or `NoneAvailable`. | Confirm the `Quota` condition is `Under`. If you have a reservation for this instance type and zone and capacity does not arrive, [contact support](https://docs.coreweave.com/support.md). |
| `CWNodeDeliverFail` (event) | A Node failed to be allocated to the Node Pool because of a misconfiguration or an internal issue. This is a delivery problem, not a capacity shortage, even when `CWInsufficientCapacity` also appears. CKS retries delivery automatically. | Repeated delivery failures can disable the Node Pool, which produces a `CWNodePoolDisabled` event. If delivery failures persist or the Node Pool is disabled, [contact support](https://docs.coreweave.com/support.md). |

Quota events and conditions:

| Event or status | Plain-language meaning | Resolution |
| - | - | - |
| `CWOverQuota` (event) | Your `targetNodes` request exceeds your organization's quota for that instance type, compute class, and zone, and no headroom is left. CKS queued no Nodes for the request. If the event message is `Quota limit is 0`, your organization has no quota for the combination and the `Quota` condition shows `NotSet` instead of `Over`. | Lower `targetNodes` to within quota, or [contact support](https://docs.coreweave.com/support.md) to request more quota. When moving Nodes between Node Pools, scale down the source pool before you scale up the destination to avoid `CWOverQuota`. |
| `CWNodePoolQuotaCheckFailed` (event) | An internal error occurred while CKS checked the quota. This is a system error, not a sign that you're over quota. | Wait and let CKS retry the check. If the error persists, [contact support](https://docs.coreweave.com/support.md). |
| `CWNoQuota` (event) | Your organization has no quota for the Node Pool's instance type, compute class, and zone. The event message reads `Quota limit is 0`, the `Quota` condition shows `NotSet`, and CKS queued no Nodes for the request. | To request a quota, [contact support](https://docs.coreweave.com/support.md). |
| `Quota: Over` (condition) | The most recent quota check found the organization over quota with no headroom left for the Node Pool's instance type, compute class, and zone. CKS queued nothing. This is the condition that `CWOverQuota` reports, except in the `Quota limit is 0` case described for `CWOverQuota`. | Lower `targetNodes` to within quota, or [contact support](https://docs.coreweave.com/support.md) to request more quota. |
| `Quota: Under` with fewer Nodes than you asked for | Your request exceeded the quota but headroom remained, so CKS capped the request to the headroom and queued that many Nodes. The condition stays `Under`, no `CWOverQuota` event fires, and the `CWNodeRequestQueued` event reports how many Nodes CKS queued. | Nothing is broken. To get the rest, raise the quota or lower the `targetNodes` total across your organization's Node Pools for that instance type, compute class, and zone. |

## Run a Node Pool health check

When a Node Pool isn't doing what you expect, collect its counts, conditions, events, and the state of its Nodes before you change anything. The diagnosis steps in the next section refer to these outputs.

```bash title="Node Pool health check" theme={"system"}
# Counts and condition columns for every Node Pool
kubectl get nodepool

# All conditions for one Node Pool, with reasons and messages
kubectl get nodepool [NODE-POOL-NAME] -o jsonpath='{range .status.conditions[*]}{.type}={.status} ({.reason}): {.message}{"\n"}{end}'

# Recent events for the Node Pool, oldest first
kubectl get events -A --field-selector involvedObject.name=[NODE-POOL-NAME] --sort-by=.lastTimestamp

# Nodes in the Node Pool, with schedulability and age
kubectl get nodes -l compute.coreweave.com/node-pool=[NODE-POOL-NAME]

# Whether each Node in the Node Pool is active (True) or idle (False)
kubectl get nodes -l compute.coreweave.com/node-pool=[NODE-POOL-NAME] -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{range .status.conditions[?(@.type=="CWActive")]}{.status}{end}{"\n"}{end}'
```

Replace `[NODE-POOL-NAME]` with the name of your Node Pool.

To inspect one Node, run `kubectl describe node [NODE-NAME]`. Replace `[NODE-NAME]` with the name of the Node. The `CWActive` condition's message lists the Pods that keep the Node active, and the `node.coreweave.cloud/cordonReason` annotation records why CoreWeave [cordoned a Node](https://docs.coreweave.com/products/cks/nodes/cordon.md#check-why-a-node-is-cordoned).

To watch Node Pool status over time instead of polling `kubectl`, use the Node Pools page in the Cloud Console (`https://console.coreweave.com/zones/[ZONE-NAME]/clusters/[CLUSTER-NAME]/node-pools`, with your zone and cluster names in the path) or the [NodePools and Cluster Autoscaler dashboard](https://docs.coreweave.com/observability/managed-grafana/cks/nodepools-and-cluster-autoscaler.md) in CoreWeave Grafana.

## Diagnose a Node Pool that is not at target

Suppose `TARGET` is `10` but `CURRENT` is `8`. The two missing Nodes are queued, in progress, or nowhere at all, and each case has a different cause and fix. Run `kubectl get nodepool`, then work through the section that matches what you see. The last two sections cover cases where no Nodes are missing: a pool at target while Pods stay `Pending`, and a pool above target.

### Nodes are queued

If the missing Nodes appear in `QUEUED` and the `CAPACITY` column shows `QueuedAwaitingCapacity`, CKS accepted the request and fills it automatically as capacity becomes available. To learn what this state means and when to contact support, see [Common capacity and quota states](#common-capacity-and-quota-states).

Quota also limits how deep the queue can be. Quotas count your whole organization's Nodes for an instance type, compute class, and zone, so Nodes in one Node Pool consume headroom that another pool might be waiting for. If `QUEUED` is smaller than you expect (`TARGET` minus `CURRENT` minus `INPROGRESS`), sum the `TARGET` column across every Node Pool with the same instance type and compute class. Include pools in your organization's other clusters in the same zone. Then compare the total to your quota before you suspect a capacity or delivery problem. See [Resource quotas](https://docs.coreweave.com/products/cks/clusters/quotas.md).

A short `QUEUED` count is the normal result of a quota cap, not an error. When `targetNodes` exceeds the quota and headroom remains, CKS queues only the headroom and discards the remainder. No warning event fires, but the `CWNodeRequestQueued` event reports how many Nodes CKS queued, which is the fastest way to confirm a cap.

Headroom subtracts both the Nodes your organization already has assigned and the Nodes it already has queued for that instance type, compute class, and zone. A sibling pool with a deep queue leaves you less headroom, not more. Only the request being checked stays out of that total, so CKS doesn't count it twice.

On rack-scale instance types, the cap rounds down to whole NVLink domains. A domain holds 18 Nodes on GB200 and GB300, so headroom of fewer than 18 Nodes queues nothing on those types.

### Nodes are in progress

If the missing Nodes appear in `INPROGRESS`, they're assigned and booting. Delivering a bare-metal GPU Node takes 5 to 15 minutes from the request to the Node joining the cluster. In the Node Pool's events, `CWNodeAssigned` marks the assignment, and `CWNodeRegistered` marks the Node joining the cluster, which is when `CURRENT` increases.

Replacements follow the same path. If a Node is removed, for example because you deleted an unhealthy Node, CKS queues and delivers a replacement on its own: The events show `CWNodeRequestQueued` followed by `CWNodeAssigned`. You don't need to request the replacement.

If `INPROGRESS` hasn't moved in well over 30 minutes for a GPU Node Pool, or 15 minutes for a CPU Node Pool, check the events for `CWNodeDeliverFail`. CKS retries failed deliveries automatically. See [Common capacity and quota states](#common-capacity-and-quota-states).

### Nothing is queued or in progress

If `CURRENT` is below `TARGET` while `QUEUED` and `INPROGRESS` are both `0`, read the conditions from the health check:

* `Validated: Invalid`: CKS rejected the configuration, most often an instance type that isn't offered in the zone (the events show `CWInstanceTypeNotInZone`) or a Node affinity `matchFields` requirement on a key other than `metadata.name` (the events show `CWNodePoolInvalidNodeAffinity`). This check reads `matchFields` only. A broken `matchExpressions` block, such as an `In` operator with an empty value list, leaves `Validated` at `Valid` and surfaces on the `Capacity` condition instead. Applying the manifest still succeeds. These checks run after the API server accepts the Node Pool, so `kubectl apply`, Helm, and Terraform all report success while the Node Pool sits at `Invalid`. Check the conditions after every change. To confirm an instance type is offered in a zone, see the [Availability matrix](https://docs.coreweave.com/platform/instances/availability-matrix.md).
* `Quota: Over`: The organization-wide total of `targetNodes` for this instance type, compute class, and zone exceeds your quota and no headroom is left, so CKS queued nothing for the request. A request that exceeds the quota while headroom remains behaves differently: CKS caps it to the headroom, queues that many Nodes, and leaves the `Quota` condition at `Under`. Seeing `Over` means the headroom is gone, not that the request was trimmed. See [Resource quotas](https://docs.coreweave.com/products/cks/clusters/quotas.md) and the [quota events table](#common-capacity-and-quota-states) earlier on this page.
* `Quota: NotSet`: Your organization has no quota for this instance type, compute class, and zone. CKS queues nothing and emits a `CWNoQuota` or `CWOverQuota` event with the message `Quota limit is 0`. To request a quota, [contact support](https://docs.coreweave.com/support.md).
* `Capacity: Partial` or `NoneAvailable`: The zone is short of the instance type. The `CWInsufficientCapacity` event message reports what was assigned, for example `Assigned (8 out of 10)`, while `CURRENT` reports what has joined. CKS keeps what it assigned and retries the rest automatically. See [Common capacity and quota states](#common-capacity-and-quota-states).
* `Capacity: PartialNodeAffinity` or `NoneAvailableNodeAffinity`: The Node Pool's affinity constraints ruled out some or all of the Nodes of that instance type in the zone. An affinity that matches nothing lands here rather than on `Validated: Invalid`, and so do two broken affinities: one CKS can't interpret, and one that targets a different InfiniBand fabric than the fabric assigned to the cluster. Both of those also emit `CWNodePoolInvalidNodeAffinity`, so read the event message before you start hunting for zone capacity. See [the `Capacity` condition](https://docs.coreweave.com/products/cks/reference/node-pool#condition-capacity).

If you have reserved capacity and the Node Pool still won't fill, the pool's InfiniBand fabric can be the reason. In zones with more than one InfiniBand fabric, CKS delivers all Nodes of an instance type in a cluster onto the same fabric. Free capacity on a different fabric can't join the pool. Check which fabric the pool's Nodes are on:

```bash title="Show the fabric for each Node in the pool" theme={"system"}
kubectl get nodes -l compute.coreweave.com/node-pool=[NODE-POOL-NAME] -L backend.coreweave.cloud/fabric,ib.coreweave.cloud/fabric
```

Replace `[NODE-POOL-NAME]` with the name of your Node Pool. Build new scripts and dashboards on `backend.coreweave.cloud/fabric`. The second column covers existing InfiniBand clusters that still carry the older `ib.coreweave.cloud/fabric` label. `CWNodeAssigned` events also name the fabric each Node landed on. If your reserved capacity and the pool's existing Nodes are on different fabrics, [contact support](https://docs.coreweave.com/support.md) to plan the move. For more information about fabric labels, see [InfiniBand and RoCE labels](https://docs.coreweave.com/products/networking/hpc-interconnect/infiniband-roce-labels.md).

### At target but Pods will not schedule

If `CURRENT` equals `TARGET` and the conditions are healthy but Pods stay `Pending`, the missing capacity is on the Nodes, not the Node Pool. Cordoned Nodes still count toward `CURRENT` but accept no new Pods. List the pool's Nodes and look for `SchedulingDisabled`:

```bash title="Find cordoned Nodes in the pool" theme={"system"}
kubectl get nodes -l compute.coreweave.com/node-pool=[NODE-POOL-NAME]
```

Replace `[NODE-POOL-NAME]` with the name of your Node Pool. CoreWeave cordons Nodes for health and maintenance reasons. Read the `node.coreweave.cloud/cordonReason` annotation and see [Node cordoning](https://docs.coreweave.com/products/cks/nodes/cordon.md) for what to do next.

To see what's waiting, list the `Pending` Pods with `kubectl get pods --all-namespaces --field-selector status.phase=Pending`. Compare their GPU requests against what the schedulable Nodes can hold, and either scale the Node Pool up or reduce replicas while CoreWeave replaces the cordoned Nodes.

If the Nodes are schedulable and have free resources but Pods still stay `Pending`, the problem is scheduling rather than capacity. To check taints, Node selectors, affinity, and Kueue admission, see [Why is my Pod stuck in pending on CKS?](https://docs.coreweave.com/support/cks/articles/why-is-my-pod-stuck-in-pending).

### Current is above target

If `CURRENT` is above `TARGET`, a scale-down is pending. CKS removes Nodes according to the Node Pool's [scaling strategy](https://docs.coreweave.com/products/cks/nodes/nodes-and-node-pools.md#scaling-strategies), and a delay of a few minutes after you lower the target is normal. If [prefill](https://docs.coreweave.com/products/cks/nodes/nodes-and-node-pools.md#node-pool-prefill) is enabled, `CURRENT` also runs above `TARGET` while CKS provisions replacement Nodes. Check the `PREFILL` column before you diagnose a stuck scale-down.

If the Node Pool stays above target and its events repeat `CWNodePoolRemoveNodes` with the message `No nodes eligible for removal right now`, the default `IdleOnly` strategy found no [idle Nodes](https://docs.coreweave.com/products/cks/nodes/nodes-and-node-pools.md#idle-nodes) to remove. Check the `CWActive` condition on each Node with the health check commands, then run `kubectl describe node [NODE-NAME]` on an active Node. The `CWActive` message lists the Pods keeping it active, up to five names followed by a count of the rest.

Use the [idle Node rules and label precedence](https://docs.coreweave.com/products/cks/nodes/nodes-and-node-pools.md#idle-nodes) to identify which Pods count toward `CWActive`. When choosing a new Node to drain, `IdleOnly` requires `CWActive = False`; it doesn't start a drain merely to make an active Node idle. Nodes already marked for removal or already draining follow their existing removal workflow. Two cases might surprise you:

* A Pod stuck in `CrashLoopBackOff` keeps its Node active even though it does no useful work. Delete the Pod, or scale down the Deployment that recreates it.
* Idle GPUs don't make idle Nodes. For a new `IdleOnly` candidate, CKS requires `CWActive = False`. Workloads spread thinly across many Nodes can block scale-down even when most GPUs sit unused. Consolidate workloads, or switch the strategy to `PreferIdle`.

Also check `spec.minNodes`. With [autoscaling](https://docs.coreweave.com/products/cks/nodes/autoscaling.md) enabled, the autoscaler never takes the pool below it.

If every Node shows `CWActive: False` and the Node Pool still hasn't scaled down after about 10 minutes, [contact support](https://docs.coreweave.com/support.md).

## When to contact support

Some states aren't yours to fix. [Contact support](https://docs.coreweave.com/support.md) when you see any of the following:

* A `CWNodePoolDisabled` event. Despite the event message about configuration issues, repeated delivery failures usually cause this state. The disabled object is the Node Pool's Node Profile, which support re-enables or replaces.
* `QUEUED` that doesn't move and no Nodes reaching `INPROGRESS`, while `Quota` is `Under`.
* Any condition stuck at `InternalError` that doesn't clear on its own.
* `AtTarget: UnderTarget` while `Capacity` is `Sufficient` and nothing is queued or in progress.
* Idle Nodes (`CWActive: False`) that CKS still hasn't removed about 10 minutes into a scale-down.

Include the Node Pool name, instance type, and zone in your ticket, plus the conditions and recent events from the [health check commands](#run-a-node-pool-health-check). That output usually lets support act without asking you for more information.

## Related pages

* [Node Pool reference](https://docs.coreweave.com/products/cks/reference/node-pool.md): the complete field, condition, and event schema.
* [Why is my Pod stuck in pending on CKS?](https://docs.coreweave.com/support/cks/articles/why-is-my-pod-stuck-in-pending): when a delivered Node Pool still leaves Pods `Pending`.
* [Why won't my Node Pool scale down after my Jobs finish?](https://docs.coreweave.com/support/cks/articles/why-wont-my-node-pool-scale-down-after-my-jobs-finish): when `CURRENT` stays above `TARGET`.
* [Autoscale Node Pools](https://docs.coreweave.com/products/cks/nodes/autoscaling.md): how the autoscaler sets the target Node count.
* [Resource quotas](https://docs.coreweave.com/products/cks/clusters/quotas.md): view and request quota.
