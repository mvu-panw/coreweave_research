# Configure compute nodes for SUNK Standard

Source: https://docs.coreweave.com/products/sunk/deploy_sunk/configure-compute-nodes

# Configure compute nodes for SUNK Standard

> Define Slurm compute node resources in the Slurm Helm chart values for SUNK Standard

[SUNK Standard](https://docs.coreweave.com/products/sunk.md)

Slurm **login nodes** let you access your Slurm cluster. Slurm **compute nodes** are the nodes within the cluster where jobs run, and they handle the resources used to run jobs submitted to Slurm.

With SUNK, you can create flexible compute node definitions to meet the resource requirements of your workloads. This guide describes the methods for defining compute nodes, so you can tailor each NodeSet to the hardware and scheduling needs of your jobs.

> [!NOTE]
>
> In SUNK, Slurm **nodes** run in Kubernetes Pods. These aren't the same as Kubernetes **Nodes**, which are the worker machines that run the Pods. To distinguish between the two, this documentation capitalizes Kubernetes Nodes, while Slurm nodes aren't capitalized.

## Access Slurm compute nodes

After you access your Slurm cluster through the Slurm login node, you can interact with the Slurm compute nodes with standard Slurm commands. You don't need to directly access a Slurm compute node.

Use [Slurm commands](https://slurm.schedmd.com/man_index.html), such as `srun`, `sbatch`, or `salloc`, to run and manage jobs on Slurm compute nodes.

> [!WARNING]
>
> Avoid directly accessing Slurm compute nodes through SSH to run tasks. Bypassing Slurm can interfere with currently running jobs and may cause nodes to drain unintentionally, leading to temporary loss of resources. Work outside a Slurm allocation also doesn't preempt [HPC Verification](https://docs.coreweave.com/platform/fleet-management/hpc-verification.md#preemption-on-sunk-clusters) tests, which can then run on the same GPUs. Use SSH to Slurm compute nodes only to debug or inspect a job you already hold an allocation for, including with SSH-dependent tooling such as `rsync` or a remote debugger. For the supported ways to reach a node in a job you already hold, see [Access Slurm compute nodes](https://docs.coreweave.com/products/sunk/access_sunk/access-slurm-compute-nodes.md).

## The manifest

The foundation for defining compute nodes is a YAML manifest, which outlines the resources and configurations for each node type. The sections that follow reference the fields shown in this example, so use it as a map for the rest of this guide. The `compute:` section looks like this.

```yaml theme={"system"}
compute:
  # See "Global options" below to learn more.
  volumeMounts: []
  volumes: []
  s6: {}
  pyxis:
  partitions:

  # Node definitions. Multiple node definitions are allowed, but
  # only those `enabled: true` will be deployed.
  nodes:
    # A node definition.
    my-node-def:
      enabled: true
      replicas: 1
      staticFeatures:
        - foo
        - bar
      dynamicFeatures:
        node.coreweave.cloud/class: {}
        gpu.nvidia.com/class: {}
      image:
        repository: registry.gitlab.com/example

      env:
        - name: example
          value: "1"

      gresGpu: h100:8
      config:
        weight: 1
      resources:
        limits:
          memory: 960Gi
          sunk.coreweave.com/accelerator: "8"
          rdma/ib: "1"
        requests:
          cpu: "110"
          memory: 960Gi
          sunk.coreweave.com/accelerator: "8"
```

## Global options

Global options apply to every compute node deployed from this manifest. The following sections describe each global option shown in the preceding YAML example.

### `compute.volumeMounts`

The [`compute.volumeMounts`](https://docs.coreweave.com/products/sunk/reference/slurm-parameters) parameter declares a list of additional volumes to mount within the primary container of the node in addition to the chart `global.volumeMounts`.

For example:

```yaml theme={"system"}
compute:
  volumeMounts:
    - name: my-pvc
      mountPath: /mnt/my-pvc
```

> [!NOTE]
>
> * Entries that share the same `mountPath` as a globally defined mount override the mount.
> * In SUNK 8.0 and later, login nodes don't receive these volumeMounts. To mount the same volumes on login nodes, also add them to [`login.common.pod.volumeMounts`](https://docs.coreweave.com/products/sunk/reference/slurm-parameters#login--common--pod--volumeMounts). See [Share storage across Slurm nodes on SUNK Standard](https://docs.coreweave.com/products/sunk/manage_sunk/shared-storage.md#login-node).
> * In SUNK 7.x and earlier, SUNK also adds these volumeMounts to the login node primary container.

### `compute.volumes`

The [`compute.volumes`](https://docs.coreweave.com/products/sunk/reference/slurm-parameters) parameter declares a list of additional volumes to attach to the Pod for the compute node. If you use persistent volume claims, usually use [ReadWriteMany](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#access-modes) access mode.

See [Share storage across Slurm nodes on SUNK Standard](https://docs.coreweave.com/products/sunk/manage_sunk/shared-storage.md) for more information.

For example:

```yaml theme={"system"}
compute:
  volumes:
    - name: my-pvc
      persistentVolumeClaim:
        claimName: my-pvc
```

> [!NOTE]
>
> * Entries that share the same `name` as a globally defined mount override the volume.
> * In SUNK 8.0 and later, login nodes don't receive these volumes. To attach the same volumes to login nodes, also add them to [`login.common.pod.volumes`](https://docs.coreweave.com/products/sunk/reference/slurm-parameters#login--common--pod--volumes).
> * In SUNK 7.x and earlier, SUNK also adds these volumes to the login node Pods.

### `compute.s6`

The [`compute.s6`](https://docs.coreweave.com/products/sunk/reference/slurm-parameters) parameter lets SUNK run custom s6 scripts (see `https://skarnet.org/software/s6/`) on compute nodes, either as `oneshot` or `longrun` jobs.

For example:

```yaml theme={"system"}
compute:
  s6:
    packages:
      type: oneshot
      timeoutUp: 0
      timeoutDown: 0
      script: |
        #!/usr/bin/env bash
        apt -y update
        apt -y install nginx
    nginx:
      type: longrun
      timeoutUp: 0
      timeoutDown: 0
      script: |
        #!/usr/bin/env bash
        nginx -g "daemon off;"
```

See [Run custom scripts with s6](https://docs.coreweave.com/products/sunk/run_workloads/run-scripts-with-s6.md) for more information.

### `compute.pyxis`

The [`compute.pyxis`](https://docs.coreweave.com/products/sunk/reference/slurm-parameters) parameter has multiple options:

| Parameter | Purpose |
| - | - |
| `compute.pyxis.enabled` | Enables the pyxis container. |
| `compute.pyxis.mountHome` | Enables `ENROOT-MOUNT_HOME` for the pyxis container to mount the home directory. |
| `compute.pyxis.remapRoot` | Enables `ENROOT_REMAP_ROOT` for the pyxis container to remap the root user. |
| `compute.pyxis.securityContext.capabilities.add` | Adds capabilities to the pyxis container. `"SYS_ADMIN"` is required if you use Pyxis. |

For example:

```yaml theme={"system"}
compute:
  pyxis:
    enabled: true
    mountHome: true
    remapRoot: true
    securityContext:
      capabilities:
        add: ["SYS_ADMIN"]
```

### `compute.partitions`

The [`compute.partitions`](https://docs.coreweave.com/products/sunk/reference/slurm-parameters) parameter defines Slurm partitions. A Slurm partition is a logical grouping of compute nodes (servers) within the Slurm cluster that organizes nodes by characteristics such as memory size, CPU type, or GPU availability.

When a user submits a job to a Slurm-managed HPC cluster, they specify the partition where the job should run. The Slurm scheduler then assigns the job to an available node within that partition. Partitions can have different configurations and policies, such as time limits for jobs, user access restrictions, or priority levels.

A related option is [`compute.autoPartition.enabled`](https://docs.coreweave.com/products/sunk/reference/slurm-parameters), which, if `true` (the default), creates a partition within Slurm for each NodeSet defined in `compute.nodes`. The partition name matches the name of the `nodes` section.

To group several NodeSets into a single partition instead of one partition per NodeSet, see [Map multiple NodeSets to a single partition](#map-multiple-nodesets-to-a-single-partition).

## Other global options

Besides the options shown in the preceding `compute` example, several others apply globally to all compute nodes.

| Parameter | Purpose |
| - | - |
| `compute.generateTopology` | If `true`, generate the network topology. |
| `compute.initialState` and `compute.initialStateReason` | The initial State for the nodes when they join the Slurm cluster, generally `drain` or `idle`, and the reason for setting that state. These can also be applied as node-specific options. |
| `compute.maxUnavailable` | Sets the maximum unavailability of the compute nodes during a rolling update. Can be a percentage or a number. |
| `compute.ssh.enabled` | Whether Slurm compute nodes run `sshd`. Enabled by default on CoreWeave clusters. To restrict SSH access to users with active job allocations, see [Restrict compute node access with `pam_slurm_adopt`](https://docs.coreweave.com/products/sunk/manage_sunk/manage_cluster_access/pam-slurm-adopt). |

## Node-specific options

Besides the preceding global options, you can set options on each named `node` definition to customize a single NodeSet without affecting others. Many options are available for each named `node` definition. For reference, see `my-node-def` in the preceding YAML example, which shows many of the available options.

* **`node.enabled`**: If `true`, SUNK deploys compute nodes with this definition. You can declare multiple definitions, but SUNK deploys only those with `enabled: true`.
* **`node.replicas`**: Specifies the desired number of Slurm nodes (Kubernetes Pods) of this type that the NodeSet attempts to create. This is a maximum value, because the number of desired Pods can be greater than the number of available Pods. To change the number of replicas for a running Slurm cluster, replace `[NODESET-NAME]` with the name of your NodeSet and `[N]` with the desired number of replicas:

```bash theme={"system"}
kubectl scale nodeset [NODESET-NAME] --replicas=[N]
```

* **`node.definitions`**: A list of other node definitions to include in this definition. See [Custom node definitions](#custom-node-definitions) to learn how to create custom definitions.
* **`node.staticFeatures`**: Static Slurm node feature flags. Feature flags are strings that Slurm adds to the Slurm nodes, where they're available for use when scheduling Slurm jobs. For example, to schedule a job only on nodes with the feature `really-fast`:

```bash theme={"system"}
srun -C really-fast hostname
```

Here's an example of how it looks within Slurm.

```text theme={"system"}
NodeName=h100-092-02 Arch=x86_64 CoresPerSocket=32
           CPUAlloc=110 CPUEfctv=128 CPUTot=128 CPULoad=0.56
           AvailableFeatures=h100-pci4,pci-4,cu120,gpu,infiniband,sharp
           ActiveFeatures=h100-pci4,pci-4,cu120,gpu,infiniband,sharp
```

* **`node.dynamicFeatures`**: Dynamic Slurm node features from Kubernetes Node labels. This specifies a map of labels to use as additional feature flags within Slurm. The value for each map key is `{}` because there's no further configuration at this time.
* **`node.image`**: Specifies which Docker image repository to use to pull this node's image. See [Custom Images](https://docs.coreweave.com/products/sunk/optimize_workloads/custom-images.md) to learn more about how to build custom SUNK images.
* **`node.env`**: Sets extra environment variables to expose in the compute nodes.
* **`node.gresGpu`**: Sets the [Slurm Generic Resource Scheduling](https://slurm.schedmd.com/gres.html) value for the `gpu` [GresType](https://slurm.schedmd.com/slurm.conf.html#OPT_GresTypes). This describes the type and number of GPU Generic Resources for this Slurm node type.
* **`node.config`**: Adds additional config options to the slurmd startup used during dynamic node registration. The features and gres options are already set. See [Node Parameters](https://slurm.schedmd.com/slurmd.html#OPT_conf-%3Cnode-parameters%3E) and [Node Configuration](https://slurm.schedmd.com/slurm.conf.html#SECTION_NODE-CONFIGURATION) for more details on the options and values.
* **`node.resources`**: Sets the Kubernetes Compute resource limits and requests.
* **`node.realMemory`**: Sets per-node RealMemory limits in Slurm config. By default, SUNK uses the `node.resources.limits.memory` value divided by 1Mi to set the Slurm RealMemory value. This option overrides that default behavior.
* **`node.affinity`**: Sets the Kubernetes Node affinities, which constrain which Kubernetes Nodes the node's Pods can schedule on, such as a specific GPU model or a Node Pool label. The NodeSet reads only the `requiredDuringSchedulingIgnoredDuringExecution` section. See [Bind NodeSets to Node Pools for SUNK Standard](https://docs.coreweave.com/products/sunk/deploy_sunk/bind-nodesets-to-node-pools.md).
* **`node.tolerations`**: Sets the Kubernetes tolerations for the node's Pods, letting them schedule onto tainted Nodes. Match these to the taints a Node Pool applies through `nodeTaints`.
* **`node.initialState`** and **`node.initialStateReason`**: The [initial State](https://docs.coreweave.com/products/sunk/reference/slurm-parameters.md) for the nodes when they join the Slurm cluster, generally `drain` or `idle`, and the [reason](https://docs.coreweave.com/products/sunk/reference/slurm-parameters.md) for setting that state. You can also apply these as [a general option](https://docs.coreweave.com/products/sunk/reference/slurm-parameters.md) for the cluster.
* **`node.volumeMounts`**: Additional per node definition volumeMounts to add to the primary container, same format as `compute.volumeMounts`. Mounts that match on `mountPath` override those set at the higher level.
* **`node.volumes`**: Additional per node definition volumes to add to the Pod, same format as `compute.volumes`. Volumes that match on `name` override those set at the higher level.
* **`node.containers`**: Additional per node containers (for example, sidecars) to add to the Pod. Additional configuration for these containers (such as Secrets and ConfigMaps) must be in the Slurm namespace.
* **`node.dnsPolicy`**: Adjusts the dnsPolicy for each node.
* **`node.dnsConfig`**: Adjusts the dnsConfig for each node.

## Custom node definitions

When several node definitions share configuration, you can factor the shared parts into reusable layers rather than repeat them. Node definitions can reference other node definitions to include or overlay values. You can define these "layers" in the same `values.yaml` file, or in separate files.

The following example defines a layer named `reservation-id` that pins a node definition to a capacity reservation. Replace `[RESERVATION-ID]` with the value CoreWeave assigned to your capacity reservation:

```yaml theme={"system"}
compute:
  nodes:
    reservation-id:
      affinity:
        nodeAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            nodeSelectorTerms:
              - matchExpressions:
                  - key: node.coreweave.cloud/reserved
                    operator: In
                    values:
                      - [RESERVATION-ID]
```

The `my-node-def` definition includes that layer.

```yaml theme={"system"}
compute:
  nodes:
    my-node-def:
      definitions:
      - reservation-id
```

You can store custom layers as separate values files. You can use any key defined under `compute.nodes`, even if that key is another file, by specifying multiple values files in a defined order on the command line.

For example, consider a `custom-compute-defs-values.yaml` file that only has a `compute.nodes` section with custom layers defined. The `values.yaml` file can use those definitions as long as you use both value files when you deploy, like so:

```bash theme={"system"}
helm install slurm coreweave/slurm -f custom-compute-defs-values.yaml -f values.yaml
```

## Mixing CPU and GPU node types

A single Slurm cluster often needs to serve workloads with different hardware requirements. You can mix multiple Slurm node types by defining multiple NodeSets in different blocks under `compute.nodes`. Each NodeSet can have its own resources and affinities that specify a single type of node.

For example, you can create a NodeSet that selects a particular type of GPU, while another selects CPU-only nodes, and then deploy any desired number of each node type.

To bind each NodeSet to a specific CoreWeave Kubernetes Service (CKS) Node Pool, and to keep other Pods off the Nodes a NodeSet uses, see [Bind NodeSets to Node Pools for SUNK Standard](https://docs.coreweave.com/products/sunk/deploy_sunk/bind-nodesets-to-node-pools.md).

## Map multiple NodeSets to a single partition

When [`compute.autoPartition.enabled`](https://docs.coreweave.com/products/sunk/reference/slurm-parameters) is `true` (the default), SUNK creates one partition per NodeSet, named after the `compute.nodes` entry. To make several NodeSets schedulable as a single partition instead, define that partition in [`compute.partitions`](https://docs.coreweave.com/products/sunk/reference/slurm-parameters) and list each NodeSet in its `Nodes` field.

Grouping NodeSets this way is useful when capacity is split across multiple NodeSets but you want users to submit work to one place. For example, you might spread one GPU type across separate NodeSets and then combine them so jobs target a single partition rather than choosing among NodeSets.

In a `compute.partitions` entry, the key is the partition name and the value is the partition configuration, written as a Slurm-style string. This string format applies to current SUNK chart releases. The `Nodes` field accepts a comma-separated list of NodeSet names (the keys under `compute.nodes`), not Kubernetes Node names or Slurm node hostnames, so list only NodeSets that exist. SUNK registers each NodeSet as a Slurm nodeset, a named group of nodes, so Slurm resolves these names to the nodes in those NodeSets. Settings you place in [`compute.partitionBaseConfig`](https://docs.coreweave.com/products/sunk/reference/slurm-parameters), such as `MaxTime` and `State`, apply to every partition, so you don't have to repeat them in each entry.

Given three NodeSets named `h100-a`, `h100-b`, and `h200`, the following configuration maps all of them into a single `training` partition:

```yaml theme={"system"}
compute:
  partitions:
    training: Nodes=h100-a,h100-b,h200 Default=YES MaxTime=INFINITE State=UP
```

Set `Default=YES` on exactly one partition. Jobs submitted without a `-p` flag run in the default partition, and Slurm evaluates feature constraints only within it, so an unintended default partition can send jobs to the wrong nodes or prevent them from scheduling.

These partitions work alongside the per-NodeSet partitions that `autoPartition` creates, because a Slurm node can belong to more than one partition. To create only the partitions you define, set `compute.autoPartition.enabled` to `false`.

You can also define several partitions over the same NodeSets to offer different scheduling priorities. The following example uses three priority tiers set by `PriorityTier`. The `DefMemPerCPU` field sets the default memory per allocated CPU, in mebibytes. The value shown is only an example. Setting it higher than `RealMemory / CPUTot` can cause Slurm to split jobs across nodes or reject `--exclusive` jobs, so set it to match each node's memory and CPU count, or omit it to let SUNK calculate it for the auto-generated partitions.

```yaml theme={"system"}
compute:
  partitions:
    hpc-high: Nodes=h100-a,h100-b,h200 PriorityTier=32768 Default=NO DefMemPerCPU=18880 MaxTime=INFINITE State=UP
    hpc-mid: Nodes=h100-a,h100-b,h200 PriorityTier=16384 Default=YES DefMemPerCPU=18880 MaxTime=INFINITE State=UP
    hpc-low: Nodes=h100-a,h100-b,h200 PriorityTier=1 Default=NO DefMemPerCPU=18880 MaxTime=INFINITE State=UP
```

For the full list of partition parameters, see the Slurm [`slurm.conf`](https://slurm.schedmd.com/slurm.conf.html) reference.
