# Node Pool reference

Source: https://docs.coreweave.com/products/cks/reference/node-pool

# Node Pool reference

> Complete API schema reference for CKS Node Pool resources, including spec fields and configuration options

This page documents the API schema for CKS Node Pool resources, including spec fields, status fields, conditions, and events.

## Node Pool

Node Pool is the schema for the Node Pools API.

| Field | Type | Description | Default |
| - | - | - | - |
| `apiversion` | `string` | The version of the Kubernetes API that the Node Pool uses. | `compute.coreweave.com/v1alpha1` |
| `kind` | `string` | The type of resource being defined, such as a `Node Pool` | `Node PoolList` |
| `metadata` | *[ListMeta](https://kubernetes.io/docs/reference/kubernetes-api/common-definitions/list-meta/)* | See the Kubernetes API documentation for metadata | |
| `spec` | `Node PoolSpec` | The desired state of the Node Pool. | |
| `status` | [Node Pool status](#node-pool-status) | The observed state of the Node Pool. See [Node Pool status](#node-pool-status). | |

## Node Pool spec

`Node PoolSpec` defines the desired state of Node Pool.

| Field | Type | Description | Default | Validation |
| - | - | - | - | - |
| `computeClass` | enum (`default`) | The type of Node Pool. `default` is used for Reserved instances and On-Demand instances and is the default | `default` | Optional |
| `instanceType` | string | Instance Type for the Nodes in this Node Pool (**Note**: `instanceType` is immutable and unchangeable) | N/A | Required |
| `targetNodes` | integer | The quantity of desired Nodes in the Node Pool (**Note**: Exactly one of `targetNodes` and `targetRacks` must be provided) | N/A | Optional |
| `targetRacks` | integer | The quantity of desired racks in the Node Pool (**Note**: Exactly one of `targetNodes` and `targetRacks` must be provided. `targetRacks` is only available for NVL72-powered instance types such as GB200 and GB300) | N/A | Optional |
| `minNodes` | integer | The minimum number of TargetNodes allowed by the autoscaler | N/A | Optional |
| `maxNodes` | integer | The maximum number of TargetNodes allowed by the autoscaler | N/A | Optional |
| `nodeLabels` | object (keys:`string`, values:`string`) | Labels applied to new and existing Nodes in the Node Pool. Additions and value changes apply automatically without a reboot. | N/A | Optional |
| `nodeAnnotations` | object (keys:`string`, values:`string`) | Annotations applied to new and existing Nodes in the Node Pool. Additions and value changes apply automatically without a reboot. | N/A | Optional |
| `nodeTaints` | Taint Array | Taints applied to new and existing Nodes in the Node Pool. Additions and value changes apply automatically without a reboot. | N/A | Optional |
| `image` | Image | The image to use for the Nodes in the Node Pool. (**Note**: `image` and `gpu` are mutually exclusive. If both are set, `gpu` is ignored.)  For updates to take effect, [perform a reconfigure reboot](https://docs.coreweave.com/products/cks/nodes/apply-updates.md). | N/A | Optional |
| `gpu` | Gpu | GPU driver configuration for the Nodes in the Node Pool. (**Note**: `gpu` and `image` are mutually exclusive. If both are set, `gpu` is ignored.)  For updates to take effect, [perform a reconfigure reboot](https://docs.coreweave.com/products/cks/nodes/apply-updates.md). | N/A | Optional |
| `autoscaling` | boolean | Enable or disable cluster autoscaling | false | Optional |
| `lifecycle.scaleDownStrategy` | enum (`IdleOnly`, `PreferIdle`) | Options for removing Nodes when scaling down to reach `targetNodes`. `IdleOnly` removes only idle Nodes. `PreferIdle` removes idle Nodes first and then active Nodes if needed. | `IdleOnly` | Optional |
| `nodeConfigurationUpdateStrategy.type` | enum (`Manual`, `OnSpecUpdate`, `Always`) | Defines how configuration updates get staged onto the Node Pool. See [Node configuration update strategies](#node-configuration-update-strategies) for more information. | `OnSpecUpdate` | Optional |
| `prefill` | PrefillSpec | Configures proactive replacement of Nodes marked for triage before they are drained. Enabled by default when omitted. See [Prefill](#prefill). | N/A | Optional |

### Node configuration update strategies

| Strategy | Behavior |
| - | - |
| Manual | Updates require user intervention to stage onto the Node Pool. You can inspect updates in [`pendingNodeConfiguration`](https://docs.coreweave.com/products/cks/reference/node-pool#pending-node-configuration) and apply them with the [CoreWeave Intelligent CLI](https://github.com/coreweave/cwic). |
| OnSpecUpdate | Updates are staged automatically only if triggered by a direct change to the Node Pool spec (for example, modifying the GPU driver version). |
| Always | Updates are staged automatically for both user-initiated spec changes and any available upstream updates. |

## Image

Image defines what boot image the `Node PoolSpec` uses.

> [!WARNING]
>
> Image should be omitted from `Node PoolSpec` unless directed by CoreWeave support. The `image` and `gpu` fields are mutually exclusive. If both are set, `gpu` is ignored and `image` takes precedence.

| Field | Type | Description | Default | Validation |
| - | - | - | - | - |
| `kernel` | string | Kernel version for this Node Pool | | Optional |
| `name` | string | Name of the image for this Node Pool. If `name` is set, `kernel` must be empty and `releaseTrain` must be `stable`. | | Optional |
| `releaseTrain` | string | The release channel or track for the image | `stable` | Optional Enum: \[stable latest] |

> [!NOTE]
>
> **NVSHMEM + GDRCopy support**
>
> NVSHMEM and GDRCopy require ncore image version 2.10.1 or later, released June 2025 (which recent ncore images include by default). If your Nodes run an older image, [contact Support](https://docs.coreweave.com/support.md) to request an update. For implementation instructions, see [Use NVSHMEM and GDRCopy for GPU-to-GPU communication](https://docs.coreweave.com/products/networking/hpc-interconnect/nvshmem-gdrcopy.md).

## GPU

The `gpu` field defines the GPU driver configuration for Nodes in the `Node PoolSpec`.

> [!WARNING]
>
> The `gpu` and `image` fields are mutually exclusive. If both are set, `gpu` is ignored and `image` takes precedence.

| Field | Type | Description | Default | Validation |
| - | - | - | - | - |
| `version` | string | The specific GPU driver version to use. Only the major version is specified. | | Optional |

## Prefill

The `prefill` spec defines Node Pool prefill behavior: proactive provisioning of replacement Nodes before Nodes marked for triage are drained and removed. See [Node Pool prefill](https://docs.coreweave.com/products/cks/nodes/nodes-and-node-pools.md#node-pool-prefill) for an overview.

Prefill is enabled by default for supported new Node Pools.

> [!NOTE]
>
> Node Pools created before October 8, 2026, retain their existing prefill settings. See the [prefill changelog entry](https://docs.coreweave.com/changelog.md#october-8-2026).

When you omit the `spec.prefill` field, CKS uses [prefill default values](https://docs.coreweave.com/products/cks/nodes/manage.md#enable-node-pool-prefill). To turn off prefill, see [Disable prefill](https://docs.coreweave.com/products/cks/nodes/manage.md#disable-prefill). The [`PrefillEnabled` condition](#condition-prefillenabled) reports whether prefill is functional for the Node Pool.

**Prefill requirements**

| Setting | Requirement |
| - | - |
| Instance type | Use a non-rack-based instance type. Rack-based instances, such as GB200 and GB300, don't support prefill. |
| Autoscaling | Set `autoscaling: false`. With autoscaling enabled, CKS doesn't start new prefill operations. Operations already in progress continue. |
| Compute class | Use `computeClass: default`. Spot Node Pools don't support prefill. |

Use the following fields in `spec.prefill` to configure prefill:

| Field | Type | Description | Default | Validation |
| - | - | - | - | - |
| `enabled` | boolean | Enable or disable prefill. When enabled, CKS provisions replacement Nodes before draining Nodes marked for triage. | `true` | Optional |
| `timeout` | Duration | Maximum wait for a Node to become idle after its replacement joins the Node Pool. The Node is unschedulable from the time it enters triage. When the timeout expires, CKS starts draining the Node. CKS removes the Node once it becomes idle. | `24h` | Optional |
| `maxNodes` | integer | Maximum number of concurrent prefill replacement Nodes, from 1 to 4. | `3` | Optional |

The maximum allowed timeout is 24 hours by default. A timeout above the configured limit produces `PrefillEnabled: False` with reason `InvalidTimeout`. Check the condition's `message` for the allowed limit.

## Node Pool status

Node Pool status is the observed state of a `Node Pool`.

| Field | Type | Description | Validation |
| - | - | - | - |
| `queuedNodes` | integer | Number of queued Nodes waiting to be assigned. | Optional Minimum |
| `inProgress` | integer | Number of Nodes that have been assigned, but have not yet fully booted into the cluster | Optional Minimum |
| `currentNodes` | integer | Number of Nodes for this Node Pool present in the cluster | Optional Minimum |
| `prefillNodes` | integer | Number of Nodes in this Node Pool that are present in the cluster and marked for prefill. See [Prefill](#prefill). | Optional Minimum |
| [`rackStatus`](#rackstatus) | RackStatus | Current rack counts for the Node Pool. Only populated for rack-based instance types. | Optional |
| `nodeProfile` | string | NodeProfile is the unique identifier for the active Node configuration | Optional |
| [`pendingNodeConfiguration`](#pending-node-configuration) | object (createdAt: `timestamp`, nodeProfile: `string`, summary: `string array`) | Contains information about a configuration awaiting promotion, according to the Node Pool's update strategy. | Optional |
| [`nodeConfigurationRevisions`](#node-configuration-revisions) | nodeConfigurationRevision Array | Maintains a list of Node configurations that were applied to the Node Pool, along with data about each one. | Optional |
| [`conditions`](#conditions) | Condition Array | All conditions associated with the Node Pool | Optional |

## RackStatus

`RackStatus` is the observed rack state for a Node Pool. This field is only populated for rack-based instance types.

| Field | Type | Description | Validation |
| - | - | - | - |
| `target` | integer | Number of racks requested for the Node Pool | Optional |
| `current` | integer | Number of racks for this Node Pool present in the cluster | Optional |
| `queued` | integer | Number of racks queued awaiting capacity to join the Node Pool | Optional |

## Pending Node configuration

The `pendingNodeConfiguration` contains information about the configuration that is pending adoption on the Node Pool. This configuration is not set as the active configuration without an explicit upgrade.

This field is only present if there are configuration updates available for your Node Pool and your `nodeConfigurationUpdateStrategy.type` is set to `Manual` or `OnSpecUpdate`.

For example, if a new GPU driver or Kubernetes version is available, CKS creates a new configuration and sets it as pending on the Node Pool. The summary field provides more information about the available updates. See [Manage Node Pool Configuration](https://docs.coreweave.com/products/cks/nodes/manage.md#manage-node-pool-configuration) to promote a pending configuration.

| Field | Type | Description |
| - | - | - |
| `createdAt` | timestamp | When the Node configuration was created |
| `nodeProfile` | string | The unique identifier for the configuration |
| `summary` | string array | A summary of the features for the configuration, such as ncore version, GPU driver version, and Kubernetes version. |

With the `Manual` strategy, every new configuration is set as pending, including your own `image` and `gpu` spec changes and CoreWeave-published updates, and none of them becomes active until you promote it. To inspect the pending configuration, run `kubectl get nodepool [NODEPOOL-NAME] -o yaml` and check `status.pendingNodeConfiguration`. To promote it, see [Stage Node Pool configurations](https://docs.coreweave.com/products/cks/nodes/manage.md#stage-node-pool-configurations).

## Node configuration revisions

The revisions list holds history of the Node configurations that were applied to the Node Pool. That is, configurations that were at one point the `status.nodeProfile`.

The list is sorted by creation timestamp, and can be used as a reference to roll back to a previous Node configuration if desired. See [Manage Node Pool Configuration](https://docs.coreweave.com/products/cks/nodes/manage.md#manage-node-pool-configuration) to roll back to a previous configuration.

| Field | Type | Description |
| - | - | - |
| `activeNodes` | integer | The count of Nodes in the Node Pool that are booted into this configuration |
| `createdAt` | timestamp | The creation timestamp for the configuration |
| `nodeProfile` | string | The unique identifier for the configuration |
| `disabled` | boolean | Indicates if the configuration is blocked from being applied to more Nodes. A configuration gets disabled if it experiences successive boot failures. Contact [Support](https://docs.coreweave.com/support.md) if this field is set to `true`. |
| `summary` | string array | A summary of the features for the configuration, such as ncore version, GPU driver version, and Kubernetes version. |

## Conditions

Node Pools and the Nodes within them report status through conditions.

### Node conditions

CoreWeave sets the following conditions on Nodes in a Node Pool.

| Condition Name | Type | Description |
| - | - | - |
| `CWActive` | bool | `true` if the Node is active. If `false`, and the Node Pool is being scaled down, the Node may be selected for removal. |
| `CWRegistered` | bool | `true` if the Node is registered. If `false`, the Node is not registered. Nodes are registered when they enter a customer cluster as part of the Node lifecycle. |
| `CWNodeRemoval` | bool | `true` if the Node is pending removal. |
| `Prefill` | string (reason) | Set on Nodes in the prefill flow. Use the condition's `reason` and `message` to interpret state. `LastTransitionTime` indicates when the reason last changed; `LastHeartbeatTime` indicates when the condition was last processed. See [Prefill condition reasons](#prefill-condition-reasons). |

#### Prefill condition reasons

When Node Pool prefill is enabled, the `Prefill` condition on a Node uses the following reasons:

| Reason | Description |
| - | - |
| `AwaitingReplacement` | Node is marked for prefill; a replacement Node is being provisioned. |
| `AwaitingIdleTimeout` | Replacement Node is in the cluster. CKS waits up to the idle timeout (`spec.prefill.timeout`) for this Node to become idle, then removes it. |
| `TimeoutExceeded` | The Node did not become idle within the idle timeout (`spec.prefill.timeout`), so CKS starts draining it. CKS removes the Node once it becomes idle. |

### Node Pool conditions

CoreWeave sets the following conditions on a Node Pool after the Node Pool resource has been created.

#### Condition: `Validated`

This condition answers the question: "Is the Node Pool configuration valid?" It has three possible statuses:

| Status | Description |
| - | - |
| `Valid` | The Node Pool configuration is correct. |
| `Invalid` | The Node Pool configuration has errors, such as an unsupported instance type or incorrect Node affinity. |
| `InternalError` | A system error occurred during validation, so the Node Pool couldn't be fully checked. |

#### Condition: `PrefillEnabled`

The `PrefillEnabled` condition in `status.conditions` reports whether prefill is functional for the Node Pool. It's `True` when prefill is enabled, explicitly or by default, and the Node Pool's configuration supports it. It doesn't indicate whether prefill operations are in progress or guarantee replacement capacity or readiness. When the condition is `False`, CKS doesn't mark new Nodes for prefill.

A reason that starts with `Unsupported` means that the Node Pool's configuration doesn't support prefill, so CKS turns off prefill automatically. These reasons don't indicate a configuration error, and you don't need to take action unless you want to use prefill.

| Status | Reason | Description |
| - | - | - |
| `True` | `Enabled` | Prefill is enabled and the Node Pool's configuration supports it. CKS can mark triaged Nodes for prefill. |
| `False` | `DisabledByUser` | Prefill is explicitly disabled with `spec.prefill.enabled: false`. See [Disable prefill](https://docs.coreweave.com/products/cks/nodes/manage.md#disable-prefill). |
| `False` | `UnsupportedInstanceType` | The Node Pool's instance type doesn't support prefill. To use prefill, choose a different Node Pool with a non-rack-based instance type. |
| `False` | `UnsupportedWithAutoscaling` | The Node Pool has autoscaling enabled, and prefill doesn't support autoscaling. To use prefill on a Node Pool with `computeClass: default`, set `autoscaling: false` if this suits your workload. |
| `False` | `UnsupportedComputeClass` | The Node Pool uses `computeClass: spot`, and Spot Node Pools don't support prefill. To use prefill, create or choose a different Node Pool with `computeClass: default`. You can't change an existing Node Pool's compute class. |
| `False` | `InvalidTimeout` | The prefill timeout exceeds the maximum allowed, which is 24 hours by default. Check the `message` for the allowed limit and reduce `spec.prefill.timeout`. For behavior during timeout changes, see [Configure Node Pool prefill](https://docs.coreweave.com/products/cks/nodes/manage.md#enable-node-pool-prefill). |

#### Condition: `AtTarget`

This condition shows whether the Node Pool has the expected number of active Nodes. The `AtTarget` condition has five possible values:

| Status | Description |
| - | - |
| `TargetMet` | The Node Pool has exactly the number of Nodes specified in the target. |
| `PendingDelete` | The Node Pool is being deleted, and its Nodes are removed. |
| `OverTarget` | More Nodes exist than the target. Extra Nodes are removed using the ScaleDownStrategy. |
| `UnderTarget` | Fewer Nodes exist than the target. New Nodes are created if resources are available. |
| `InternalError` | A system error occurred while retrieving Node information for the Node Pool. |

#### Condition: `NodesRemoved`

The condition `NodesRemoved` is applied to a Node Pool when it is pending deletion and Nodes are in the process of being removed. Once all Nodes are removed, the Node Pool is deleted. This response indicates one of the following conditions:

| Status | Meaning |
| - | - |
| `Complete` | All Nodes have been removed from the Node Pool, and the Node Pool's deletion is imminent. |
| `Pending` | Nodes are in the process of being removed from the Node Pool. |
| `InternalError` | An internal error has occurred while trying to remove Nodes from the Node Pool. |

#### Condition: `Capacity`

The `Capacity` condition indicates whether there is enough capacity available for the requested number of Nodes in the requested instance type. This response indicates one of the following conditions:

| Status | Meaning |
| - | - |
| `Sufficient` | Enough capacity is available in the zone to fulfill the request for `targetNodes`. |
| `Partial` | Partial capacity exists in the zone to fulfill the request, but not to completely fulfill it. |
| `NoneAvailable` | No Nodes are available of the requested type in the zone. |
| `NoneAvailableNodeAffinity` | No Nodes are available for the requested instance type due to Affinity constraints. |
| `PartialNodeAffinity` | Partial capacity is available to fulfill the requested `targetNodes`. Full capacity is not available due to Affinity constraints. |
| `QueuedAwaitingCapacity` | Request for additional Nodes has been queued and is waiting for additional capacity to become available. |
| `InternalError` | An internal error has occurred while attempting to check capacity. |

#### Condition: `Quota`

`Quota` has four statuses.

| Status | Meaning |
| - | - |
| `Under` | The organization is under quota for the Node Pool's instance type. |
| `Over` | The organization is over quota for the Node Pool's instance type. |
| `NotSet` | The organization does not have a quota set for the Node Pool's instance type. |
| `InternalError` | An internal error has occurred attempting to check the quota. |

#### Condition: `NodeReconfigurationRequired`

This condition reports whether existing Nodes need a reconfigure reboot to adopt the active configuration (`status.nodeProfile`). Read its `status`, `reason`, and `message` together:

| Reason | Status | Meaning |
| - | - | - |
| `StagedNodeConfig` | `True` | Nodes have the active configuration staged and need a reconfigure reboot. |
| `AllNodesUpToDate` | `False` | The controller reports that current Nodes are on the active configuration. This reason is also reported when the Node Pool has no Nodes. |
| `InternalError` | `False` or `Unknown` | CKS couldn't check or stage the configuration. Inspect the condition message and Node Pool events. |

A `False` status alone doesn't confirm completion because it can accompany `InternalError`. Before declaring a rollout complete, check the reason, expected Node count, and per-Node image labels. Configuration adoption doesn't confirm workload health. See [Track rollout progress](https://docs.coreweave.com/products/cks/nodes/manage.md#track-rollout-progress).

#### Healthy Node Pools

A new Node Pool in a healthy state looks like this when described:

```bash title="new node pool, showing new conditions with 'describe'" theme={"system"}
kubectl describe nodepools example-nodepool
```

```yaml title="Example output" theme={"system"}
Name:         example-nodepool
Namespace:
Labels:       <none>
Annotations:  <none>
API Version:  compute.coreweave.com/v1alpha1
Kind:         NodePool
Metadata:
  Creation Timestamp:        2025-06-09T14:48:54Z
  Generation:                1
  Resource Version:          857370
  UID:                       9311678d-4064-45b8-8439-b943250e5852
Spec:
  Autoscaling:               false
  Instance Type:             gd-8xa100-i128
  Lifecycle:
    Disable Unhealthy Node Eviction:  true
    Scale Down Strategy:              IdleOnly
  Max Nodes:                 0
  Min Nodes:                 0
  Target Nodes:              1
Status:
  Conditions:
    Last Transition Time:    2025-05-30T17:36:00Z
    Message:                 NodePool configuration is valid.
    Reason:                  Valid
    Status:                  True
    Type:                    Validated
    Last Transition Time:    2025-05-30T17:36:00Z
    Message:                 Sufficient capacity available for the requested instance type.
    Reason:                  Sufficient
    Status:                  True
    Type:                    Capacity
    Last Transition Time:    2025-05-30T17:36:00Z
    Message:                 NodePool is within instance type quota.
    Reason:                  Under
    Status:                  True
    Type:                    Quota
    Last Transition Time:    2025-05-30T17:36:00Z
    Message:                 NodePool has reached its target node count.
    Reason:                  TargetMet
    Status:                  True
    Type:                    AtTarget
    Last Transition Time:    2025-05-30T17:36:00Z
    Message:                 All nodes are on the current configuration.
    Reason:                  AllNodesUpToDate
    Status:                  False
    Type:                    NodeReconfigurationRequired
  Current Nodes:             1
  In Progress:               0
  Queued Nodes:              0
Events:                      <none>
```

## Events

The Node Pool controller emits the following Kubernetes Events.

| Event Name | Resource | Description |
| - | - | - |
| `CWDrainNode` | NodePool | Fired when a Node is being drained. |
| `CWInstanceTypeNotInZone` | NodePool | Fired when a Node Pool has an instance type not in its Zone. |
| `CWInsufficientCapacity` | NodePool | Fired when there is not sufficient capacity for a Node Pool. |
| `CWInvalidInstanceType` | NodePool | Fired when a Node Pool contains an invalid instance type. |
| `CWNodeAssigned` | NodePool | Fired when a Node is assigned to a Node Pool. |
| `CWNodeDeleted` | NodePool | Fired to indicate a Node has been deleted. |
| `CWNodeDeletionRequestSuccess` | NodePool | Fired when Node Pool Operator receives a request to delete a Node. |
| `CWNodeDeliverFail` | NodePool | Fired when Node allocation to a Node Pool fails due to misconfigured Node Pool settings or internal issues. |
| `CWNodePoolCreated` | NodePool | Fired when a Node Pool is created. |
| `CWNodePoolDeleted` | NodePool | Fired when a Node Pool is deleted. |
| `CWNodePoolDisabled` | NodePool | Fired when the Node Profile assigned to the Node Pool is marked as disabled, usually after repeated Node delivery failures. The Node Pool can't schedule additional Nodes until [Support](https://docs.coreweave.com/support.md) re-enables the Node Profile or a new one is generated. |
| `CWNodePoolMetadata` | NodePool | Fired when metadata is updated for a Node Pool. |
| `CWNodePoolMetadataSanitized` | NodePool | Fired when `nodeLabels` or `nodeAnnotations` contain a key in the reserved `coreweave.com` or `coreweave.cloud` namespaces. CKS drops those keys and syncs the rest. The message lists the keys it dropped. See [User-provided labels](https://docs.coreweave.com/products/cks/clusters/scheduling/workload-scheduling.md#user-provided-labels). |
| `CWNodePoolNodesRemoved` | NodePool | Fired when Nodes are removed from the Node Pool. |
| `CWNodePoolNodesRemoveError` | NodePool | Fired when an error occurs during Node removal. |
| `CWNodePoolNodesRequestFailed` | NodePool | Fired when an error is returned when updating the Node Pool. |
| `CWNodePoolQuotaCheckFailed` | NodePool | Fired when there is an internal error checking the quota. |
| `CWNodePoolRemoveNodes` | NodePool | Fired when attempting to scale down a Node Pool. |
| `CWNodePoolScaledDown` | NodePool | Fired when a Node Pool is scaled down. |
| `CWNodePoolScaledUp` | NodePool | Fired when a Node Pool is scaled up. |
| `CWNodeRegistered` | Node, NodePool | Fired when Node registration succeeds. |
| `CWNodeRegistrationFailed` | Node | Fired when Node registration fails. See the message for additional details. |
| `CWNodeRequestQueued` | NodePool | Fired when a request is submitted to add Nodes to a Node Pool. |
| `CWNoQuota` | NodePool | Fired when the organization has no quota set for the Node Pool's instance type, compute class, and zone. The event message reads `Quota limit is 0`. |
| `CWOverQuota` | NodePool | Fired when the quota is insufficient for the Node Pool's `targetNodes`. |
| `CWNodeCordoned` | Node, NodePool | Fired when a Node is being cordoned as part of internal automation. |
| `CWNodeUncordoned` | Node, NodePool | Fired when a Node is being uncordoned as part of internal automation. |
| `CWNodeMarkedPrepareForTerminate` | Node, NodePool | Fired when a Node has been sent the signal to prepare for termination. See event message for details. |
| `CWNodeDraining` | Node, NodePool | Fired when a Node is being drained as part of internal automation. |
| `CWNodeDrainingPDBViolation` | Node, NodePool | Fired when a Node is being drained and certain pods cannot be evicted due to a Pod Disruption Budget. |
| `CWNodeDrainingForceDelete` | Node, NodePool | Fired when a Node is being drained as part of internal automation and pods were deleted ungracefully. |
| `CWNodePreparedForTerminate` | Node, NodePool | Fired when a Node is prepared for termination. |
| `CWNodeTainted` | Node, NodePool | Fired when a Node is tainted as part of internal automation. |
| `CWNodeUntainted` | Node, NodePool | Fired when a Node is untainted as part of internal automation. |
| `CWNodeConfigStaged` | NodePool | Fired when the active Node Config (`status.nodeProfile`) for the Node Pool has been updated. This might be a result of staging the `pendingNodeConfiguration`, new user-initiated changes getting staged, or rolling back to a previous configuration. |
| `CWPendingNodeConfig` | NodePool | Fired when the `status.pendingNodeConfiguration` is updated on the Node Pool. |
| `CWConfigStaged` | Node | Fired when a new Node configuration is staged on the Node by setting it as the desired NodeProfile during Node boot. |
| `CWReconfigureRebooted` | Node | Fired after the Node has been reconfigure rebooted and is determined to be up to date with the staged NodeProfile of the Node Pool. |
| `CWNodePoolNodeConfigUpdatePending` | NodePool | Fired when a Node Config update is pending due to Nodes being mid-delivery. The update completes once Nodes have booted into the cluster. |
| `CWNodePoolNodeConfigUpdated` | NodePool | Fired when the active Node Config (`status.nodeProfile`) for the Node Pool has been updated. This might be a result of promoting the `pendingNodeConfiguration` or rolling back to a previous configuration. |
| `CWNodePoolNoPendingConfiguration` | NodePool | Fired when a user attempts to promote the `status.pendingNodeConfiguration` to become the active configuration (`status.nodeProfile`), but there is no staged configuration. |
| `CWNodePoolNodeConfigRollbackFailed` | NodePool | Fired when there was an error rolling back the active Node configuration for the Node Pool to a previous config. |
| `CWNodePoolNodeConfigUpdateConflict` | NodePool | Fired when a user simultaneously attempts to upgrade to the `pendingNodeConfig` and rollback to a previous one. |
| `CWNodeConfigStagingFailed` | Node | Fired when CKS attempted to stage the Node Pool's active configuration on an existing Node in the cluster to prepare it for a reconfigure reboot, but was not able to do so. It keeps retrying until successful. |
| `CWManualUpgradeTrigger` | NodePool | Fired when a user upgrades a Node Pool to the pending configuration. |
| `CWManualRollbackTrigger` | NodePool | Fired when a user rolls back a Node Pool to a previous configuration. |

### Node lifecycle events

CoreWeave's Node lifecycle automation emits the following events on Nodes during [state transitions](https://docs.coreweave.com/platform/fleet-management/node-lifecycle/state-transitions.md).

| Event Name | Resource | Description |
| - | - | - |
| `CWNCPhaseNccPendingChange` | Node | Fired when an unhealthy Node alert causes CoreWeave automation to record a pending lifecycle state on a Node, such as `production-reboot`. The event fires when the pending state is set, before the actual state change: the Node remains in `production` until the transition proceeds. The message names the Node condition that triggered the transition and the target state. If a higher-priority alert supersedes the pending state, the event fires again for the new target state. |
| `CWNCPhasePendingTenantWorkloadRunning` | Node | Fired while tenant workloads prevent a pending state transition. The message lists the workloads keeping the Node active. In the ordinary pending flow, CKS waits for non-interruptible workloads to finish, then drains the remaining Pods. Gracefully interruptible Pods can delay the transition until they terminate or reach their deletion deadline. |

> [!NOTE]
>
> Don't use these events for your own automation. Event names are intended for internal use and can change without notice.
