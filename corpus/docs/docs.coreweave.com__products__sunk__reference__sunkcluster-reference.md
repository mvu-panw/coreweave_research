# SunkCluster reference

Source: https://docs.coreweave.com/products/sunk/reference/sunkcluster-reference

# SunkCluster reference

> Reference parameters for the SunkCluster custom resource that defines a SUNK Self-Service cluster

[SUNK Self-Service](https://docs.coreweave.com/products/sunk/about-self-service-sunk.md)

The `SunkCluster` custom resource declares the desired state of a SUNK Self-Service cluster. The [out-of-band operator](https://docs.coreweave.com/products/sunk/discover_sunk/self-service-architecture.md) reconciles a `SunkCluster` into the underlying Node Pools, NodeSets, and `SlurmCluster` resources that make up a running cluster.

Use this reference when authoring or reviewing a `SunkCluster` manifest to confirm field names, types, defaults, and accepted values, and to interpret the status conditions the out-of-band operator reports back. This page is intended for cluster operators and platform engineers who manage SUNK clusters declaratively.

This page documents every supported field in the `SunkCluster` spec, along with the status conditions reported on the resource. To learn how to apply a `SunkCluster`, see [Create a SUNK Self-Service cluster](https://docs.coreweave.com/products/sunk/deploy_sunk/create-sunk-cluster.md). For the cluster setups that SUNK Self-Service supports, see [Supported configurations](https://docs.coreweave.com/products/sunk/about-self-service-sunk.md#supported-configurations).

## Resource definition

| Field | Value |
| - | - |
| `apiVersion` | `sunk.coreweave.com/v1alpha1` |
| `kind` | `SunkCluster` |
| `namespace` | Any namespace. The Cloud Console uses `tenant-slurm`. |

## Top-level spec fields

The `spec` object configures the SUNK cluster. The following fields are supported:

| Field | Type | Required | Default | Description |
| - | - | - | - | - |
| `sunkVersion` | string | No | Latest release | SUNK release version, with or without a leading `v`. A new cluster that leaves it out gets the latest SUNK release available on SUNK Self-Service, and the value doesn't change when that default changes. See [SUNK to Slurm version mapping](https://docs.coreweave.com/products/sunk/reference/sunk-slurm-versions.md) for releases. |
| `slurmVersion` | string | No | Slurm build for the default SUNK release | Slurm version, with a leading `v`. A new cluster that leaves it out gets the Slurm build that ships with the default SUNK release. Use a Slurm release that your SUNK major version supports, for example Slurm 25.11 on SUNK 8. The version mapping table lists the Slurm build that ships with each SUNK release. On a new cluster, a value without the leading `v` leaves the cluster in `Bootstrapping`. |
| `cudaVersion` | string | No | `13.0` | CUDA version installed on compute nodes. Allowed values: `13.0`, `13.1`. |
| `ubuntuVersion` | string | No | `24.04` | Ubuntu base image version. Allowed values: `22.04`, `24.04`. |
| `nodes` | list of [NodeSpec](#nodespec) | No | None | Node configurations. Each entry becomes one Node Pool. Each compute entry also becomes one NodeSet, and a control-plane entry doesn't. A `SunkCluster` with no `nodes` won't provision a control plane or compute nodes and won't become Ready. |
| `storage` | [StorageConfig](#storageconfig) | No | See StorageConfig | Home directory and additional shared storage mounts. |
| `login` | [LoginConfig](#loginconfig) | No | None | Resources and access configuration for login Pods. |
| `s6` | list of [S6](#s6) | No | None | s6 service scripts to run on node initialization. |
| `slurmConfig` | map of string to string | No | None | Custom key-value pairs passed through to the Slurm configuration. |
| `scheduler` | [SchedulerConfig](#schedulerconfig) | No | `{enabled: false}` | Scheduler configuration. |
| `nvidiaDevicePlugin` | [NvidiaDevicePluginConfig](#nvidiadeviceplugin) | No | `{enabled: true}` | NVIDIA device plugin configuration. |

## NodeSpec

Each entry in `spec.nodes` defines one node group. The out-of-band operator creates one Node Pool for each entry, and one NodeSet for each entry that doesn't set `controlPlane: true`. It keeps the Node Pool and NodeSet counts in sync with `count`.

| Field | Type | Required | Default | Description |
| - | - | - | - | - |
| `name` | string | Yes | None | Unique node-group name, used as the name of both the Node Pool and the NodeSet. Must be 1-30 characters and match `^[a-z0-9]([a-z0-9-]*[a-z0-9])?$`. Immutable. |
| `instanceType` | string | Yes | None | CoreWeave instance type. See [Allowed instance types](#allowed-instance-types) for the full list. Immutable after creation. |
| `count` | integer | Yes | None | Number of nodes of this type. Minimum `0`. Mutable. Changing this value scales the underlying Node Pool. |
| `controlPlane` | boolean | No | `false` | When `true`, this node group hosts the Slurm control plane. |

### Allowed instance types

The `instanceType` field uses the Instance ID listed on the [available instances](https://docs.coreweave.com/platform/instances/about-instances.md) page.

The field accepts one of the following values:

* `epyc`
* `cd-hp-a96-genoa`
* `cd-gp-a192-genoa`
* `cd-gp-l-a192-genoa`
* `cd-hc-a384-genoa`
* `cd-hc-a384ib-genoa`
* `turin-gp`
* `turin-gp-l`
* `cd-gp-i64-erapids`
* `cd-gp-i96-icelake`
* `h100`
* `gd-8xh100ib-i128`
* `h200`
* `gd-8xh200ib-i128`
* `a100`
* `gd-8xa100-i128`
* `b200-8x`
* `b300-8x`
* `gb200`
* `gb200-4x`
* `gd-1xgh200`
* `gd-8xl40-i128`
* `gd-8xl40s-i128`
* `rtxp6000-8x`
* `gb300-4x`
* `gb300-4x-e`
* `verarubin-4x-e`

## StorageConfig

The `spec.storage` object configures shared storage for the cluster.

| Field | Type | Required | Default | Description |
| - | - | - | - | - |
| `homeDir` | [VolumeSpec](#volumespec) | No | `{path: /mnt/home, size: 2Ti}` | Home directory storage configuration. |
| `additionalMounts` | list of [VolumeSpec](#volumespec) | No | None | Additional shared storage mounts. |

### VolumeSpec

| Field | Type | Required | Default | Description |
| - | - | - | - | - |
| `path` | string | Yes | None | Mount path inside the Pod (for example, `/mnt/data`). |
| `size` | Kubernetes Quantity | Yes | None | Storage size as a Kubernetes quantity (for example, `2Ti`, `100Gi`). |

## LoginConfig

The `spec.login` object configures the login Pods, the groups whose members can access them, and the resources allocated to per-user and per-group Pods. By default, each user with access receives an individual login Pod, and each access group receives one shared login Pod. Set `userPods` or `groupPod` to `false` on a group in `login.groups` to turn either off.

| Field | Type | Required | Default | Description |
| - | - | - | - | - |
| `groups` | list of [LoginGroup](#logingroup) | No | None | Groups whose members can access the cluster. Each group name is also propagated to nsscache for POSIX user and group resolution. |
| `sudoGroups` | list of strings | No | None | Groups whose members receive sudo access on login Pods. |
| `userPods` | [LoginPodConfig](#loginpodconfig) | No | None | Configuration applied to per-user login Pods. |
| `groupPods` | [LoginPodConfig](#loginpodconfig) | No | None | Configuration applied to per-group login Pods. |

### LoginGroup

Each entry in `login.groups` configures login-Pod creation for a single group. The list uses `name` as a merge key.

| Field | Type | Required | Default | Description |
| - | - | - | - | - |
| `name` | string | Yes | None | Group name to match in the nsscache group secret. Must be at least 1 character. |
| `userPods` | boolean | No | `true` | When `true`, individual per-user login Pods are created for members of this group. |
| `groupPod` | boolean | No | `true` | When `true`, a shared per-group login Pod is created for this group. Note the singular field name (`groupPod`) at this level. |

### LoginPodConfig

The `login.userPods` and `login.groupPods` objects each accept a `LoginPodConfig`.

| Field | Type | Required | Default | Description |
| - | - | - | - | - |
| `resources` | [ResourceConfig](#resourceconfig) | No | None | CPU and memory requests applied to this Pod type. |
| `access` | [AccessConfig](#accessconfig) | No | None | Annotations applied to the Services for this Pod type, such as load balancer or DNS annotations. Set it on `userPods` and `groupPods` separately to expose each type independently. |

### ResourceConfig

| Field | Type | Required | Default | Description |
| - | - | - | - | - |
| `cpu` | Kubernetes Quantity | No | None | CPU allocation (for example, `8`). |
| `memory` | Kubernetes Quantity | No | None | Memory allocation (for example, `32Gi`). |

### AccessConfig

| Field | Type | Required | Default | Description |
| - | - | - | - | - |
| `annotations` | map of string to string | No | None | Annotations applied to the login Services of the Pod type that sets `access`. |

For example, the following annotations expose the shared group login Pods on a public address. `userPods.access` takes the same fields:

```yaml theme={"system"}
  login:
    groupPods:
      access:
        annotations:
          service.beta.kubernetes.io/external-hostname: sunk.<org-id>-<cluster-name>.coreweave.app
          service.beta.kubernetes.io/coreweave-load-balancer-ip-families: ipv4
          service.beta.kubernetes.io/coreweave-load-balancer-type: public
```

## S6

Each entry in `spec.s6` defines an s6 service script that runs on the targeted node types during initialization.

| Field | Type | Required | Default | Description |
| - | - | - | - | - |
| `name` | string | Yes | None | Unique name for the script. |
| `type` | string | Yes | None | Script type. Allowed values: `oneshot`, `longrun`. |
| `targets` | list of strings | Yes | None | Node types the script runs on. Allowed values: `login`, `compute`. Must contain at least one entry. |
| `script` | string | No | None | Inline script content to execute. See the following validation rules. |
| `packages` | list of strings | No | None | Packages to install. Each element may contain one or more whitespace-separated package names. Only valid with `type: oneshot`. |
| `depends` | list of strings | No | None | Names of other s6 scripts that must run before this one. |
| `timeoutUp` | integer | No | None | Startup timeout in milliseconds. Required for `oneshot` script entries. For `longrun`, set this or `timeoutDown`. |
| `timeoutDown` | integer | No | None | Shutdown timeout in milliseconds. Only valid for `longrun` entries. |

> [!NOTE]
>
> Each entry must set either `script` or `packages`, not both. The `packages` field is only valid when `type` is `oneshot`. For `oneshot` script entries, `timeoutUp` is required. For package installs, the in-cluster operator applies an internal minimum timeout policy based on package count. For `longrun` entries, set at least one of `timeoutUp` or `timeoutDown`.

## SchedulerConfig

The `spec.scheduler` object enables the SUNK Pod Scheduler.

| Field | Type | Required | Default | Description |
| - | - | - | - | - |
| `enabled` | boolean | No | `false` | When `true`, the scheduler is enabled. |

## NvidiaDevicePlugin

The `spec.nvidiaDevicePlugin` object configures the NVIDIA device plugin DaemonSet.

| Field | Type | Required | Default | Description |
| - | - | - | - | - |
| `enabled` | boolean | No | `true` | When `true`, the NVIDIA device plugin is deployed. |

## Status conditions

Use the status conditions to determine whether a `SunkCluster` is fully reconciled and, if not, which subsystem is still pending or has failed.

The out-of-band operator reports the cluster state through a standardized set of `status.conditions`. Each status condition includes a `reason` and a `message` that further describes the condition.

The aggregate `Ready` condition is `True` when all dependent conditions are `True`.

| Condition | Meaning |
| - | - |
| `Ready` | Aggregate condition. `True` when every other condition is `True`. |
| `ValidationSucceeded` | The `SunkCluster` meets the preconditions for reconciling it, such as being the only active `SunkCluster` in the cluster. When it doesn't, the reason is `Error` and the `message` gives the cause. |
| `NodePoolsAvailable` | All requested Node Pools have reached their target node count. |
| `NodeSetsAvailable` | All NodeSets have ready Pods. |
| `SlurmClusterAvailable` | Aggregate of the managed `SlurmCluster`'s own conditions. See [SlurmCluster status conditions](#slurmcluster-status-conditions). |
| `ControllerManagerAvailable` | The SUNK controller manager Deployment is ready. |
| `NvidiaDevicePluginAvailable` | The NVIDIA device plugin DaemonSet is ready, or the device plugin is disabled. |
| `VolumesAvailable` | The PVCs for the configured storage exist. A PVC that isn't bound yet still counts as ready. The reason is `Error` only when a PVC can't be created or loses its volume. |
| `TunablesAvailable` | The DaemonSet that applies node tunables is ready, or no tunables are enabled. The reason is `Error` when the tunables configuration is invalid. |

The status also reports `lastReadyTime`, which records the most recent time the `Ready` condition transitioned to `True`. This field distinguishes a cluster that is bootstrapping (never ready) from one that was previously ready and has regressed.

The `reason` attached to each condition contains one of the following values:

| Reason | Meaning |
| - | - |
| `Ready` | The described condition has been satisfied. |
| `InProgress` | The described condition is in progress but not yet complete. |
| `Bootstrapping` | Set on the aggregate `Ready` condition while the cluster is coming up for the first time. |
| `Degraded` | Set on the aggregate `Ready` condition when a cluster that was previously ready has dependent conditions that aren't `True`, such as during an upgrade. |
| `Error` | The described condition has encountered an error. |

The `message` attached to a condition contains more detail. For dependent conditions, the `message` typically names the specific resources that are not yet ready (for example, `NodePools not at target: [a192, gb200]` or `NodeSets not ready: [a192 (0/36 ready)]`). For the aggregate `Ready` condition, the `message` lists the dependent conditions still pending (for example, `Waiting for conditions: NodePoolsAvailable, NodeSetsAvailable, SlurmClusterAvailable`).

### SlurmCluster status conditions

The `SlurmClusterAvailable` condition on the `SunkCluster` aggregates the conditions reported by the underlying `SlurmCluster` resource. When `SlurmClusterAvailable` is not `True`, inspect the `SlurmCluster` itself to identify which subcomponent is pending or failing:

```bash theme={"system"}
kubectl get slurmcluster -n tenant-slurm -o yaml
```

The `SlurmCluster` reports the following conditions, each of which must be `True` for `SlurmClusterAvailable` to aggregate to `True`:

| Condition | Meaning |
| - | - |
| `Ready` | Aggregate condition for the `SlurmCluster`. `True` when every other `SlurmCluster` condition is `True`. |
| `SlurmctldAvailable` | The Slurm controller (`slurmctld`) Deployment is ready. |
| `LoginAvailable` | The login Pods for each configured group are ready, or no login workloads are configured. |
| `AccountingAvailable` | The Slurm accounting (`slurmdbd`) workloads are ready. |
| `DatabaseAvailable` | The `CWDBCluster` backing Slurm accounting is ready. |
| `SchedulerAvailable` | The SUNK Pod Scheduler workloads are ready, or the scheduler is disabled. |
| `SyncerAvailable` | The SUNK Syncer workloads are ready. |
| `NsscacheAvailable` | The nsscache workloads that resolve POSIX users and groups are ready. |
| `RestdAvailable` | The Slurm REST daemon (`slurmrestd`) is ready, or `slurmrestd` is disabled. |
| `CleanupCompletingAvailable` | The cleanup-completing workload is ready, or the workload is disabled. |

## Example manifest

The following example brings the preceding fields together into a complete manifest you can adapt for your own cluster.

Use this manifest as a starting point and adjust the field values to match your cluster requirements, replacing `[CLUSTER-NAME]` with a name for your cluster. The following manifest creates a cluster with two control-plane nodes and four H100 GPU compute nodes, a 1 Ti home directory, an additional 1 Ti shared mount, and standard user and sudo groups.

```yaml theme={"system"}
apiVersion: sunk.coreweave.com/v1alpha1
kind: SunkCluster
metadata:
  name: [CLUSTER-NAME]
  namespace: tenant-slurm
spec:
  ubuntuVersion: "24.04"

  nodes:
    - name: control-plane
      instanceType: cd-gp-a192-genoa
      count: 2
      controlPlane: true
    - name: gpu
      instanceType: gd-8xh100ib-i128
      count: 4
      controlPlane: false

  storage:
    homeDir:
      path: /mnt/home
      size: 1Ti
    additionalMounts:
      - path: /mnt/data
        size: 1Ti

  login:
      groups:
        - name: slurm-users
          # userPods and groupPod default to true
        - name: sudo-users
          userPods: false
          groupPod: true
      sudoGroups:
        - sudo-users
      groupPods:
        access:
          annotations:
            example.com/annotation: "value"
        resources:
          memory: 8Gi
          cpu: 4
      userPods:
        resources:
          memory: 8Gi
          cpu: 4
```
