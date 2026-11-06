# Resource quotas

Source: https://docs.coreweave.com/products/cks/clusters/quotas

# Resource quotas

> View resource quotas, understand quota errors, and request quota upgrades through support

Resource quotas define the maximum amount of CoreWeave resources, such as GPUs, that your organization can provision. This page shows you how to view your quotas in the Cloud Console, how to read quota errors when a Node Pool exceeds its quota, and how to request an increase when you need more capacity.

## Quota overview

CoreWeave applies several distinct quota limits. They aren't interchangeable, and a request can fail against any one of them.

| Limit | Scope | What it limits |
| - | - | - |
| Cluster quota | Per organization, per zone | The maximum number of CKS clusters your organization can create in a zone. |
| Instance quota | Per instance type, per compute class, per zone | The number of Nodes of a given instance type and compute class your organization can provision in a zone. |
| Kubernetes `ResourceQuota` | Per namespace, managed by you | CPU, memory, and object counts within a namespace. This is a standard Kubernetes feature, not a CoreWeave organization quota. |

Compute class is the Node Pool's tier, either `default` or [`spot`](https://docs.coreweave.com/platform/capacity-plans/spot-node-pools) (preemptible). A `default` Node Pool and a `spot` Node Pool of the same instance type and zone draw on separate quota lines with independent limits.

### What counts against your quota

Each Node you provision of an instance type counts against the instance quota for that instance type, compute class, and zone, whether you created it manually by setting `targetNodes` or the autoscaler created it. Nodes that are queued or in progress also count toward your request.

Keep these distinctions in mind:

* Quota is separate from capacity. A request can be under quota but still wait for capacity if the instance type isn't available in the zone. A Node Pool reports both states through its `Quota` and `Capacity` conditions.
* The autoscaler's `maxNodes` is a per-Node-Pool ceiling, not your quota. Organization instance quota is shared across all Node Pools of the same instance type and compute class in the same zone. Two Node Pools with `maxNodes: 10` each, both of the same instance type and compute class in the same zone, can together request 20 Nodes against a single quota line. If the quota is 10, the second Node Pool to scale hits `CWOverQuota`.
* Quota is tracked per zone. Node Pools of the same instance type in different zones draw on separate quota lines.
* A Kubernetes `ResourceQuota` (a namespace-level object you create) is a different concept from CoreWeave organization quota.

### Compute your current usage

The organization instance quota applies across Node Pools of the same instance type and compute class in the same zone, so total your Nodes across all Node Pools to compare against quota.

To get the total current Nodes by instance type across all Node Pools, run:

```bash theme={"system"}
kubectl get nodepool -o json | jq -r '.items[] | "\(.spec.instanceType)\t\(.status.currentNodes // 0)"' \
  | awk '{sum[$1]+=$2} END {for (t in sum) print t"\t"sum[t]}'
```

Compare the totals against your quotas in the Cloud Console, as shown in [View quotas](#view-quotas). For how to read the `Quota` and `Capacity` conditions on a Node Pool, see [Node Pool status](https://docs.coreweave.com/products/cks/nodes/nodepool-status.md).

## View quotas

To view your resource quotas, log in to your CoreWeave organization on the Cloud Console and go to the [Quotas](https://console.coreweave.com/organization/quotas) page. On this page, you can browse quotas or search for a specific one.

![Resource quotas](https://mintcdn.com/coreweave-dbfa0e8d/Diszsi3qOqeLxowx/products/cks/_media/resource-quota.png?fit=max\&auto=format\&n=Diszsi3qOqeLxowx\&q=85\&s=58b846cd1e3a1821417a12c5fafc17e2)

## How quotas apply to instance types

Quotas apply per organization, per instance type, per compute class, and per zone. Compute class is the Node Pool's tier, either `default` or [`spot`](https://docs.coreweave.com/platform/capacity-plans/spot-node-pools) (preemptible). A `default` Node Pool and a `spot` Node Pool of the same instance type and zone count against separate quotas. For example, in the same zone, CKS tracks `gd-8xh100ib-i128` at `default` compute class and the same instance type at `spot` as two separate quotas with independent limits.

CKS checks the quota every time `targetNodes` is set, whether you're creating a new Node Pool or scaling an existing one. If a request exceeds the quota, CKS caps it to your remaining headroom, queues that many Nodes, and discards the remainder. Headroom is your quota limit minus the Nodes your organization already has assigned or queued for that instance type, compute class, and zone. Nodes queued by your other Node Pools reduce your headroom. Only the request being checked stays out of that total, so CKS doesn't count it twice. When no headroom is left, CKS queues nothing and the `Quota` condition becomes `Over`.

On rack-scale instance types, the cap rounds down to whole NVLink domains. A domain holds 18 Nodes on GB200 and GB300, so headroom of fewer than 18 Nodes queues nothing on those types.

To identify the instance types your organization uses, see [GPU instances](https://docs.coreweave.com/platform/instances/gpu-instances.md) and [CPU instances](https://docs.coreweave.com/platform/instances/cpu-instances.md). To check which instance types are offered in each zone, see the [Availability matrix](https://docs.coreweave.com/platform/instances/availability-matrix.md).

To check the quota status of a Node Pool, run `kubectl get nodepool` and read the `QUOTA` column, or run `kubectl describe nodepool [NODE-POOL-NAME]` and read the `Quota` condition. An `Over` status means the Node Pool's `targetNodes` exceeds your organization's quota for that instance type, compute class, and zone, and no headroom is left, so CKS queued nothing. A capped request that still queued some Nodes reports `Under`. For the full meaning of each status, see [Node Pool conditions: Quota](https://docs.coreweave.com/products/cks/reference/node-pool.md#condition-quota).

## Quota errors

If Terraform fails to create a cluster with `unavailable` after repeated attempts, see [Why does Terraform report unavailable when creating a CKS cluster?](https://docs.coreweave.com/support/cks/articles/why-does-terraform-report-unavailable-when-creating-a-cks-cluster).

When a Node Pool's `targetNodes` request reaches a quota limit, the Node Pool controller emits a Kubernetes event. The bottom of `kubectl describe nodepool [NODE-POOL-NAME]` lists recent events. For example:

```text title="Example output" theme={"system"}
Type     Reason                       Age                  From              Message
----     ------                       ----                 ----              -------
Warning  CWOverQuota                  2m6s (x21 over 47m)  nodePoolOperator  TargetNodes pushes org over quota by <OVERAGE>. Limit is <QUOTA> for instance type <INSTANCE_TYPE>, compute class <COMPUTE_CLASS> in zone <ZONE>
Warning  CWNodePoolQuotaCheckFailed   2m6s (x21 over 47m)  nodePoolOperator  Internal quota error
```

The following events and condition states report how a quota affected the request.

| Event or status | Plain-language meaning | Resolution |
| - | - | - |
| `CWOverQuota` (event) | Your `targetNodes` request exceeds your organization's quota for that instance type, compute class, and zone, and no headroom is left. CKS queued no Nodes for the request. If the event message is `Quota limit is 0`, your organization has no quota for the combination and the `Quota` condition shows `NotSet` instead of `Over`. | Lower `targetNodes` to within quota, or [contact support](https://docs.coreweave.com/support.md) to request more quota. When moving Nodes between Node Pools, scale down the source pool before you scale up the destination to avoid `CWOverQuota`. |
| `CWNodePoolQuotaCheckFailed` (event) | An internal error occurred while CKS checked the quota. This is a system error, not a sign that you're over quota. | Wait and let CKS retry the check. If the error persists, [contact support](https://docs.coreweave.com/support.md). |
| `CWNoQuota` (event) | Your organization has no quota for the Node Pool's instance type, compute class, and zone. The event message reads `Quota limit is 0`, the `Quota` condition shows `NotSet`, and CKS queued no Nodes for the request. | To request a quota, [contact support](https://docs.coreweave.com/support.md). |
| `Quota: Over` (condition) | The most recent quota check found the organization over quota with no headroom left for the Node Pool's instance type, compute class, and zone. CKS queued nothing. This is the condition that `CWOverQuota` reports, except in the `Quota limit is 0` case described for `CWOverQuota`. | Lower `targetNodes` to within quota, or [contact support](https://docs.coreweave.com/support.md) to request more quota. |
| `Quota: Under` with fewer Nodes than you asked for | Your request exceeded the quota but headroom remained, so CKS capped the request to the headroom and queued that many Nodes. The condition stays `Under`, no `CWOverQuota` event fires, and the `CWNodeRequestQueued` event reports how many Nodes CKS queued. | Nothing is broken. To get the rest, raise the quota or lower the `targetNodes` total across your organization's Node Pools for that instance type, compute class, and zone. |

For the complete event schema, see the [Node Pool reference: Events](https://docs.coreweave.com/products/cks/reference/node-pool.md#events). For troubleshooting quota and capacity states together, see [Node Pool status: Common capacity and quota states](https://docs.coreweave.com/products/cks/nodes/nodepool-status.md#common-capacity-and-quota-states).

## Request quota upgrades

Request quota upgrades through support.

To request a quota upgrade, log in to your CoreWeave Freshdesk account and [submit a support ticket](https://coreweave.freshdesk.com/support/login).
