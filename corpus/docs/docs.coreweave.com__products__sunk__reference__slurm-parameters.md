# Slurm parameter reference

Source: https://docs.coreweave.com/products/sunk/reference/slurm-parameters

# Slurm parameter reference

> Complete parameter reference for the Slurm Helm chart, including accounting, compute, and deployment settings

[SUNK Standard](https://docs.coreweave.com/products/sunk.md)

![Version: 0.1.0](https://img.shields.io/badge/Version-0.1.0-informational?style=flat-square) ![Type: application](https://img.shields.io/badge/Type-application-informational?style=flat-square)

## Parameters

<table>
  <thead>
    <th>Key & Description</th>
    <th>Type</th>
    <th>Default</th>
  </thead>

  <tbody>
    <tr>
      <td id="accounting--config">
        **accounting.config**\

        slurmdbd.conf overrides (optional).
      </td>

      <td>object</td>

      <td>
        ```yaml wrap theme={"system"}
        null
        ```
      </td>
    </tr>

    <tr>
      <td id="accounting--database">
        **accounting.database**\

        Database connection configuration for slurmdbd. database.backend selects the database backend: "moco", "cwdb", or "external".
      </td>

      <td>object</td>

      <td>
        ```yaml wrap theme={"system"}
        {
          "backend": "moco",
          "existingSecret": null,
          "storageHost": null,
          "storageLoc": null,
          "storagePort": null,
          "storageUser": null
        }
        ```
      </td>
    </tr>

    <tr>
      <td id="accounting--database--backend">
        **accounting.database.backend**\

        Select the database backend for Slurm Accounting (`slurmdbd`). "moco": operator creates a MOCO MySQLCluster (requires database.\* config fields). "cwdb": operator creates a CWDBCluster (requires database.\* config fields). "external": user-managed database (requires storageHost, storageUser, existingSecret).
      </td>

      <td>string</td>

      <td>
        ```yaml wrap theme={"system"}
        moco
        ```
      </td>
    </tr>

    <tr>
      <td id="accounting--database--existingSecret">
        **accounting.database.existingSecret**\

        Specify the name of the Kubernetes Secret that contains the password used by `slurmdbd` to access the Slurm accounting database. For moco/cwdb: auto-derived if not set (key: WRITABLE\_PASSWORD). For external: required (key: db-password). **Important**: The password value stored in the Secret **cannot** contain the hash (`#`) character.
      </td>

      <td>string</td>

      <td>
        ```yaml wrap theme={"system"}
        null
        ```
      </td>
    </tr>

    <tr>
      <td id="accounting--database--storageHost">
        **accounting.database.storageHost**\

        The hostname of the server where the database resides. For moco/cwdb: auto-derived if not set. For external: required.
      </td>

      <td>string</td>

      <td>
        ```yaml wrap theme={"system"}
        null
        ```
      </td>
    </tr>

    <tr>
      <td id="accounting--database--storageLoc">
        **accounting.database.storageLoc**\

        The name of the database used to store Slurm accounting records.
      </td>

      <td>string</td>

      <td>
        ```yaml wrap theme={"system"}
        slurm_acct_db
        ```
      </td>
    </tr>

    <tr>
      <td id="accounting--database--storagePort">
        **accounting.database.storagePort**\

        The port of the database server.
      </td>

      <td>int</td>

      <td>
        ```yaml wrap theme={"system"}
        3306
        ```
      </td>
    </tr>

    <tr>
      <td id="accounting--database--storageUser">
        **accounting.database.storageUser**\

        The username `slurmdbd` uses for authentication and storing job accounting data. For moco/cwdb: defaults to "moco-writable" if not set. For external: required.
      </td>

      <td>string</td>

      <td>
        ```yaml wrap theme={"system"}
        null
        ```
      </td>
    </tr>

    <tr>
      <td id="accounting--image">
        **accounting.image**\

        The image to use for slurmdbd deployment.
      </td>

      <td>object</td>

      <td>
        ```yaml wrap theme={"system"}
        repository:
        tag:

        ```
      </td>
    </tr>

    <tr>
      <td id="accounting--livenessProbe">
        **accounting.livenessProbe**\

        The liveness probe for the slurmdbd container.
      </td>

      <td>object</td>

      <td>
        ```yaml wrap theme={"system"}
        sacctmgr ping; initialDelaySeconds 15; periodSeconds 10; failureThreshold 5; successThreshold 1; timeoutSeconds 60
        ```
      </td>
    </tr>

    <tr>
      <td id="accounting--readinessProbe">
        **accounting.readinessProbe**\

        The readiness probe for the slurmdbd container.
      </td>

      <td>object</td>

      <td>
        ```yaml wrap theme={"system"}
        sacctmgr ping; initialDelaySeconds 15; periodSeconds 10; failureThreshold 5; successThreshold 1; timeoutSeconds 60
        ```
      </td>
    </tr>

    <tr>
      <td id="accounting--replicas">
        **accounting.replicas**\

        The number of replicas of the accounting instance to run.
      </td>

      <td>int</td>

      <td>
        ```yaml wrap theme={"system"}
        1
        ```
      </td>
    </tr>

    <tr>
      <td id="accounting--resources">
        **accounting.resources**\

        Resources for the accounting container.
      </td>

      <td>object</td>
      <td>requests: cpu 4 memory 16Gi; limits: memory 16Gi</td>
    </tr>

    <tr>
      <td id="accounting--securityContext">
        **accounting.securityContext**\

        Accounting container security context.
      </td>

      <td>object</td>

      <td>
        ```yaml wrap theme={"system"}
        runAsUser/runAsGroup 401
        ```
      </td>
    </tr>

    <tr>
      <td id="accounting--startupProbe">
        **accounting.startupProbe**\

        Startup probe override for the slurmdbd container.
      </td>

      <td>object</td>

      <td>
        ```yaml wrap theme={"system"}
        sacctmgr ping; periodSeconds 10; failureThreshold 360; successThreshold 1; timeoutSeconds 60
        ```
      </td>
    </tr>

    <tr>
      <td id="accounting--terminationGracePeriodSeconds">
        **accounting.terminationGracePeriodSeconds**\

        The termination grace period for the accounting pod.
      </td>

      <td>int</td>

      <td>
        ```yaml wrap theme={"system"}
        30
        ```
      </td>
    </tr>

    <tr>
      <td id="cleanupCompleting--deleteInvalidNodes">
        **cleanupCompleting.deleteInvalidNodes**\

        Delete nodes with invalid states.
      </td>

      <td>bool</td>

      <td>
        ```yaml wrap theme={"system"}
        false
        ```
      </td>
    </tr>

    <tr>
      <td id="cleanupCompleting--dryRun">
        **cleanupCompleting.dryRun**\

        Run in dry-run mode without making changes.
      </td>

      <td>bool</td>

      <td>
        ```yaml wrap theme={"system"}
        false
        ```
      </td>
    </tr>

    <tr>
      <td id="cleanupCompleting--enabled">
        **cleanupCompleting.enabled**\

        Enable cleanup of nodes with jobs stuck in COMPLETING state.
      </td>

      <td>bool</td>

      <td>
        ```yaml wrap theme={"system"}
        true
        ```
      </td>
    </tr>

    <tr>
      <td id="cleanupCompleting--image">
        **cleanupCompleting.image**\

        The image to use for cleanup-completing Job.
      </td>

      <td>object</td>

      <td>
        ```yaml wrap theme={"system"}
        repository:
        tag:

        ```
      </td>
    </tr>

    <tr>
      <td id="cleanupCompleting--intervalSeconds">
        **cleanupCompleting.intervalSeconds**\

        Interval in seconds between cleanup checks.
      </td>

      <td>int</td>

      <td>
        ```yaml wrap theme={"system"}
        300
        ```
      </td>
    </tr>

    <tr>
      <td id="cleanupCompleting--resources">
        **cleanupCompleting.resources**\

        Resources for the cleanup-completing Job container.
      </td>

      <td>object</td>
      <td>requests: cpu 100m memory 64Mi; limits: memory 256Mi</td>
    </tr>

    <tr>
      <td id="cleanupCompleting--timeoutSeconds">
        **cleanupCompleting.timeoutSeconds**\

        Timeout in seconds for jobs in COMPLETING state before downing nodes.
      </td>

      <td>int</td>

      <td>
        ```yaml wrap theme={"system"}
        2400
        ```
      </td>
    </tr>

    <tr>
      <td id="cleanupCompleting--verbose">
        **cleanupCompleting.verbose**\

        Enable verbose logging for cleanup.
      </td>

      <td>bool</td>

      <td>
        ```yaml wrap theme={"system"}
        false
        ```
      </td>
    </tr>

    <tr>
      <td id="compute--annotations">
        **compute.annotations**\

        Additional annotations for compute services only. Use `compute.nodes.custom-definition.annotations` to add annotations to specific node definitions instead.
      </td>

      <td>object</td>

      <td>
        ```yaml wrap theme={"system"}
        {}
        ```
      </td>
    </tr>

    <tr>
      <td id="compute--cacheDropper">
        **compute.cacheDropper**\

        Cache-dropper sidecar across all slurmd pods.
      </td>

      <td>object</td>

      <td>
        ```yaml wrap theme={"system"}
        {
          "enabled": null,
          "resources": null
        }
        ```
      </td>
    </tr>

    <tr>
      <td id="compute--cacheDropper--enabled">
        **compute.cacheDropper.enabled**\

        An option to enable or disable the cache-dropper sidecar container across all slurmd pods.
      </td>

      <td>bool</td>

      <td>
        ```yaml wrap theme={"system"}
        true
        ```
      </td>
    </tr>

    <tr>
      <td id="compute--cacheDropper--resources">
        **compute.cacheDropper.resources**\

        Resources for the cache-dropper sidecar container.
      </td>

      <td>object</td>

      <td>
        ```yaml wrap theme={"system"}
        limits.memory 32Mi; requests.cpu 500m; requests.memory 32Mi
        ```
      </td>
    </tr>

    <tr>
      <td id="compute--cudaVersion">
        **compute.cudaVersion**\

        CUDA toolkit version for GPU compute nodes (e.g. "13.0"). When set, GPU NodeSets use the CUDA-specific extras image (slurmd-cw-cu\<version>-extras) and the CUDA feature label (e.g. "cu130") is injected into each GPU NodeSet's static features.
      </td>

      <td>string</td>

      <td>
        ```yaml wrap theme={"system"}
        "13.0"
        ```
      </td>
    </tr>

    <tr>
      <td id="compute--epilogConfigMap">
        **compute.epilogConfigMap**\

        The name or list of ConfigMap names containing epilog scripts. These user-managed ConfigMaps are combined with the operator-managed epilog ConfigMap into a single projected directory at /etc/slurm/epilog.d. Editing the contents of an attached ConfigMap hot-reloads without rolling compute pods; adding or removing a ConfigMap name is a pod-spec change and rolls the pods. To supply inline epilog content managed by the operator, use compute.managedEpilogConfig.
      </td>

      <td>string | list</td>

      <td>
        ```yaml wrap theme={"system"}
        []
        ```
      </td>
    </tr>

    <tr>
      <td id="compute--externalClusterName">
        **compute.externalClusterName**\

        The name of an external cluster to join when the control plane is deployed separately.
      </td>

      <td>string, optional</td>

      <td>
        ```yaml wrap theme={"system"}
        null
        ```
      </td>
    </tr>

    <tr>
      <td id="compute--generateTopology">
        **compute.generateTopology**\

        Enable topology generation for compute nodes. `spec.options.generateTopology` is always rendered; when this key is omitted from values, the chart uses default true for that field. When true, the operator generates `topology.yaml` with tree, block and flat entries; the default is the one named by `slurmConfig.TopologyPlugin` (`topology/tree`, `topology/block` or `topology/flat`). Set to `false` to bring your own `topology.yaml` through `controller.etcConfigMap`; a previously generated one is left in place until yours replaces it.
      </td>

      <td>bool</td>

      <td>
        ```yaml wrap theme={"system"}
        true
        ```
      </td>
    </tr>

    <tr>
      <td id="compute--gpusd">
        **compute.gpusd**\

        Configuration for GPUSD (GPU Straggler Detection) metrics collection.
      </td>

      <td>object</td>

      <td>
        ```yaml wrap theme={"system"}
        {
          "enabled": null,
          "version": null
        }
        ```
      </td>
    </tr>

    <tr>
      <td id="compute--gpusd--enabled">
        **compute.gpusd.enabled**\

        Enable GPUSD package installation, metrics collection, and VMPodScrape resource.
      </td>

      <td>bool</td>

      <td>
        ```yaml wrap theme={"system"}
        true
        ```
      </td>
    </tr>

    <tr>
      <td id="compute--gpusd--version">
        **compute.gpusd.version**\

        GPUSD version to install.
      </td>

      <td>string</td>

      <td>
        ```yaml wrap theme={"system"}
        "1.1.0"
        ```
      </td>
    </tr>

    <tr>
      <td id="compute--initialState">
        **compute.initialState**\

        Initial state when nodes join the cluster (`idle`, `drain`, etc.); may be set per node definition.
      </td>

      <td>string</td>

      <td>
        ```yaml wrap theme={"system"}
        idle
        ```
      </td>
    </tr>

    <tr>
      <td id="compute--initialStateReason">
        **compute.initialStateReason**\

        Reason when initial state is down, drained, or fail; may be set per node definition.
      </td>

      <td>string</td>

      <td>
        ```yaml wrap theme={"system"}
        Node added to the cluster for the first time
        ```
      </td>
    </tr>

    <tr>
      <td id="compute--labels">
        **compute.labels**\

        Additional labels for compute services only. Use `compute.nodes.custom-definition.labels` to add labels to specific node definitions instead.
      </td>

      <td>object</td>

      <td>
        ```yaml wrap theme={"system"}
        {}
        ```
      </td>
    </tr>

    <tr>
      <td id="compute--livenessProbe">
        **compute.livenessProbe**\

        The liveness probe for the compute slurmd container. No default is applied by the operator; set this field to add a liveness probe.
      </td>

      <td>object</td>

      <td>
        ```yaml wrap theme={"system"}
        none
        ```
      </td>
    </tr>

    <tr>
      <td id="compute--lowProfileRequests">
        **compute.lowProfileRequests**\

        Overlay low CPU/memory requests (10 CPU / 10Gi) on the slurmd container so the Kubernetes scheduler can place other workloads on the same nodes. This overlay is also applied whenever scheduler.enabled is true, regardless of this setting.
      </td>

      <td>bool</td>

      <td>
        ```yaml wrap theme={"system"}
        true
        ```
      </td>
    </tr>

    <tr>
      <td id="compute--managedEpilogConfig">
        **compute.managedEpilogConfig**\

        Map of epilog scripts rendered into /etc/slurm/epilog.d on compute pods. Keys are file names and values are file contents. The backing ConfigMap is always created and mounted as a directory, so editing values hot-reloads without rolling compute pods.  \[accordion] Example: click to expand `yaml managedEpilogConfig:   50-site-epilog.sh: |     #!/usr/bin/env sh     echo "site epilog" `
      </td>

      <td>object</td>

      <td>
        ```yaml wrap theme={"system"}
        {}
        ```
      </td>
    </tr>

    <tr>
      <td id="compute--managedPrologConfig">
        **compute.managedPrologConfig**\

        Map of prolog scripts rendered into /etc/slurm/prolog.d on compute pods, in addition to CoreWeave-provided defaults. Keys are file names and values are file contents. The backing ConfigMap is always created and mounted as a directory, so editing values hot-reloads without rolling compute pods. Supplying a key that matches a CoreWeave-provided default overrides that default. Only executable \*.sh files are run.  \[accordion] Example: click to expand `yaml managedPrologConfig:   50-site-prolog.sh: |     #!/usr/bin/env sh     echo "site prolog" `
      </td>

      <td>object</td>

      <td>
        ```yaml wrap theme={"system"}
        {}
        ```
      </td>
    </tr>

    <tr>
      <td id="compute--maxUnavailable">
        **compute.maxUnavailable**\

        Maximum unavailability of compute nodes during a rolling update (integer or percentage).
      </td>

      <td>string</td>

      <td>
        ```yaml wrap theme={"system"}
        10%
        ```
      </td>
    </tr>

    <tr>
      <td id="compute--nodes">
        **compute.nodes**\

        Multiple node definitions can be declared, but only one may be `enabled: true`. Node definitions can reference other definitions to include or overlay values. See the example below or the [Compute Node Definitions](https://docs.coreweave.com/products/sunk/slurm-on-sunk/compute-and-login-nodes/configure-compute-nodes.md) documentation for more details.  Each node definition also supports the following pod-level fields, applied to the rendered NodeSet pod template:  - `serviceAccountName` (string, default `"default"`):   the ServiceAccount the compute pods run as. The chart does not create the ServiceAccount,   so it must already exist in the release namespace. - `automountServiceAccountToken` (bool, default `false`):   whether to auto-mount the ServiceAccount token. Set to `true` (or attach a   projected `serviceAccountToken` volume via `volumes`/`volumeMounts`)   to expose credentials to in-pod tooling. - `realMemory` (quantity, default derived from `resources.limits.memory`):   overrides the slurmd `RealMemory` value advertised to the Slurm controller for this   node definition (e.g. `150Gi`). Set this when the node's true usable memory differs   from the pod's memory limit. The value is passed through to slurmd verbatim (no   `compute.reservedMemory` headroom is subtracted from an explicit override). When unset,   it defaults to `resources.limits.memory` converted to MB.

        > [accordion] Example: click to expand
        >
        > ```yaml theme={"system"}
        > compute:
        >   nodes:
        >     # A custom definition to be referenced by other nodes
        >     custom-dns:
        >       dnsPolicy: "None"
        >       dnsConfig:
        >         nameservers:
        >           - 127.0.0.1
        >     # A simple CPU-only Node that uses the custom-dns definition above
        >     simple-cpu:
        >       enabled: true
        >       # ServiceAccount the pods run as; must already exist in the namespace.
        >       serviceAccountName: my-compute-sa
        >       # Mount the ServiceAccount token (or add a projected serviceAccountToken volume
        >       # under volumes/volumeMounts for a custom audience or mount path).
        >       automountServiceAccountToken: true
        >       # Partition creation for the nodeset. The nodeset will still be assigned to the `all`
        >       # partition if creation is disabled
        >       createPartition: true
        >       # The following Partition configurations are for the customer to update.
        >       # These values will be applied to the autogenerated partition and will override the defaults.
        >       partitionConfig:
        >         OverSubscribe: "YES"
        >         MaxTime: "12:00:00"
        >         QoS: "NORMAL"
        >       replicas: 1
        >       definitions:
        >         # Use the custom-dns definition
        >         - custom-dns
        >       staticFeatures:
        >         - cpu
        >       dynamicFeatures:
        >         node.coreweave.cloud/class: {}
        >       image:
        >         name: controller-extras
        >       gresGpu: null
        >       config:
        >         weight: 1
        >       # Create a small node with 1cpu and 1g memory
        >       resources:
        >         limits:
        >           memory: 1Gi
        >           cpu: 1
        >         requests:
        >           memory: 1Gi
        >           cpu: 1
        >       # Advertise less RealMemory to Slurm than the pod's memory limit, e.g. to
        >       # leave headroom for node-level overhead not captured by the pod limit.
        >       realMemory: 900Mi
        >       tolerations:
        >         - key: is_cpu_compute
        >           operator: Exists
        >       volumeMounts:
        >         - name: ramtmp
        >           mountPath: /tmp
        >       volumes:
        >         - name: ramtmp
        >           emptyDir:
        >             medium: Memory
        >       affinity:
        >         nodeAffinity:
        >           requiredDuringSchedulingIgnoredDuringExecution:
        >             nodeSelectorTerms:
        >               - matchExpressions:
        >                   - key: kubernetes.io/os
        >                     operator: In
        >                     values:
        >                       - linux
        > ```

        Compute node definitions are composed from the presets in charts/slurm/compute-defs/ and
        supplied per-deployment (each entry sets enabled/replicas/definitions). The base chart ships
        no preset catalog here; CW and other environments define their nodes in their own values overlays.
      </td>

      <td>object</td>
      <td>See [Compute Node Definitions](https://docs.coreweave.com/products/sunk/slurm-on-sunk/compute-and-login-nodes/configure-compute-nodes.md).</td>
    </tr>

    <tr>
      <td id="compute--plugstackConfig">
        **compute.plugstackConfig**\

        Additional plug-in stack configuration items for `plugstack.conf` file config. Config Options: [https://slurm.schedmd.com/spank.html#SECTION\_CONFIGURATION](https://slurm.schedmd.com/spank.html#SECTION_CONFIGURATION)
      </td>

      <td>list</td>

      <td>
        ```yaml wrap theme={"system"}
        []
        ```
      </td>
    </tr>

    <tr>
      <td id="compute--ports">
        **compute.ports**\

        Additional ports to expose on the compute nodes.

        > [accordion] Example: NCCL Plugin ports
        >
        > ```yaml theme={"system"}
        > ports:
        >   - containerPort: 10400
        >     protocol: TCP
        >   - containerPort: 10401
        >     protocol: TCP
        >   - containerPort: 10402
        >     protocol: TCP
        >   - containerPort: 10403
        >     protocol: TCP
        >   - containerPort: 10404
        >     protocol: TCP
        >   - containerPort: 10405
        >     protocol: TCP
        >   - containerPort: 10406
        >     protocol: TCP
        >   - containerPort: 10407
        >     protocol: TCP
        > ```
      </td>

      <td>list</td>

      <td>
        ```yaml wrap theme={"system"}
        []
        ```
      </td>
    </tr>

    <tr>
      <td id="compute--prologConfigMap">
        **compute.prologConfigMap**\

        The name or list of ConfigMap names containing prolog scripts. These user-managed ConfigMaps are combined with the operator-managed prolog ConfigMap into a single projected directory at /etc/slurm/prolog.d. Editing the contents of an attached ConfigMap hot-reloads without rolling compute pods; adding or removing a ConfigMap name is a pod-spec change and rolls the pods. To supply inline prolog content managed by the operator (and to override CoreWeave defaults), use compute.managedPrologConfig.
      </td>

      <td>string | list</td>

      <td>
        ```yaml wrap theme={"system"}
        []
        ```
      </td>
    </tr>

    <tr>
      <td id="compute--pyxis">
        **compute.pyxis**\

        Pyxis / enroot integration for compute nodes.
      </td>

      <td>object</td>

      <td>
        ```yaml wrap theme={"system"}
        {
          "appArmorProfile": null,
          "enabled": null,
          "enrootConfig": null,
          "plugstackOptions": null,
          "podSecurityContext": null
        }
        ```
      </td>
    </tr>

    <tr>
      <td id="compute--pyxis--appArmorProfile">
        **compute.pyxis.appArmorProfile**\

        AppArmor profile for pyxis nodeset containers. When omitted, defaults to localhost/enroot.
      </td>

      <td>string, optional</td>

      <td>
        ```yaml wrap theme={"system"}
        null
        ```
      </td>
    </tr>

    <tr>
      <td id="compute--pyxis--enabled">
        **compute.pyxis.enabled**\

        Enable the pyxis container.
      </td>

      <td>bool</td>

      <td>
        ```yaml wrap theme={"system"}
        true
        ```
      </td>
    </tr>

    <tr>
      <td id="compute--pyxis--enrootConfig">
        **compute.pyxis.enrootConfig**\

        `enroot.conf` overrides.
      </td>

      <td>object, optional</td>

      <td>
        ```yaml wrap theme={"system"}
        null
        ```
      </td>
    </tr>

    <tr>
      <td id="compute--pyxis--plugstackOptions">
        **compute.pyxis.plugstackOptions**\

        Additional arguments for the pyxis plugin in `plugstack.conf` file config. Config Options: [https://github.com/NVIDIA/pyxis/wiki/Setup#slurm-plugstack-configuration](https://github.com/NVIDIA/pyxis/wiki/Setup#slurm-plugstack-configuration)
      </td>

      <td>list, optional</td>

      <td>
        ```yaml wrap theme={"system"}
        null
        ```
      </td>
    </tr>

    <tr>
      <td id="compute--pyxis--podSecurityContext">
        **compute.pyxis.podSecurityContext**\

        Security context for pyxis nodeset pods. When omitted, defaults to a Localhost seccomp profile targeting profiles/enroot.
      </td>

      <td>object, optional</td>

      <td>
        ```yaml wrap theme={"system"}
        null
        ```
      </td>
    </tr>

    <tr>
      <td id="compute--readinessProbe">
        **compute.readinessProbe**\

        The readiness probe for the compute slurmd container. When omitted the NodeSet controller injects the default `scontrol show slurmd` probe.
      </td>

      <td>object</td>
      <td>exec: \[scontrol, show, slurmd]; failureThreshold: 3; periodSeconds: 10; successThreshold: 1; timeoutSeconds: 5</td>
    </tr>

    <tr>
      <td id="compute--reservedMemory">
        **compute.reservedMemory**\

        Reserved memory when calculating DefMemPerCPU config for slurm.conf
      </td>

      <td>string</td>

      <td>
        ```yaml wrap theme={"system"}
        4Gi
        ```
      </td>
    </tr>

    <tr>
      <td id="compute--s6">
        **compute.s6**\

        **oneshot** and **longrun** jobs are supported. See [Running Scripts with S6](https://docs.coreweave.com/products/sunk/development-on-slurm/run-scripts-with-s6.md) for more information.

        > [accordion] Example: click to expand
        >
        > ```yaml theme={"system"}
        > s6:
        >   packages:
        >     type: oneshot
        >     timeoutUp: 360000 # 360 seconds
        >     timeoutDown: 0
        >     script: |
        >       #!/usr/bin/env bash
        >       apt -y update
        >       apt -y install nginx
        >   nginx:
        >     type: longrun
        >     timeoutUp: 360000 # 360 seconds
        >     timeoutDown: 0
        >     script: |
        >       #!/usr/bin/env bash
        >       nginx -g "daemon off;"
        > ```
      </td>

      <td>object</td>

      <td>
        ```yaml wrap theme={"system"}
        []
        ```
      </td>
    </tr>

    <tr>
      <td id="compute--securityContext">
        **compute.securityContext**\

        Security context for the slurmd container (NodeSet pod template and SlurmCluster compute spec). Omit for operator defaults; set to add capabilities (e.g. `SYS_ADMIN` for pyxis). Setting `capabilities` replaces the operator defaults (`SYS_NICE`, `SYS_ADMIN`, `SYS_PTRACE`, `SYSLOG`, `SYS_RESOURCE`), so list every default you need alongside the added capabilities.
      </td>

      <td>object</td>

      <td>
        ```yaml wrap theme={"system"}
        operator-applied defaults
        ```
      </td>
    </tr>

    <tr>
      <td id="compute--ssh">
        **compute.ssh**\

        SSH / sshd settings for compute nodes.
      </td>

      <td>object</td>

      <td>
        ```yaml wrap theme={"system"}
        {
          "enabled": null
        }
        ```
      </td>
    </tr>

    <tr>
      <td id="compute--ssh--enabled">
        **compute.ssh.enabled**\

        Enable ssh to the compute nodes.
      </td>

      <td>bool</td>

      <td>
        ```yaml wrap theme={"system"}
        true
        ```
      </td>
    </tr>

    <tr>
      <td id="compute--startupProbe">
        **compute.startupProbe**\

        The startup probe for the compute slurmd container. When RDMA/InfiniBand resources are present the NodeSet controller injects an IB-specific startup probe automatically; set this field only to override that behaviour.
      </td>

      <td>object</td>

      <td>
        ```yaml wrap theme={"system"}
        operator-injected IB probe when rdma/ib limits are present; omitted otherwise
        ```
      </td>
    </tr>

    <tr>
      <td id="compute--umask">
        **compute.umask**\

        Default umask applied to user shells (bash and zsh) on both compute and login pods. When set, the chart injects `SUNK_UMASK` into the relevant pod environments. Leave unset to use the image default (`0022`). Values are passed through verbatim, so any form accepted by the `umask` builtin works (for example `"0027"` or `"u=rwx,g=rwx,o="`).
      </td>

      <td>string</td>

      <td>
        ```yaml wrap theme={"system"}
        ""
        ```
      </td>
    </tr>

    <tr>
      <td id="compute--volumeMounts">
        **compute.volumeMounts**\

        Additional volume mounts for all compute pods. Appended to the mounts derived from the top-level `storage` block; on a mountPath collision the entry here wins.
      </td>

      <td>list</td>

      <td>
        ```yaml wrap theme={"system"}
        []
        ```
      </td>
    </tr>

    <tr>
      <td id="compute--volumes">
        **compute.volumes**\

        Additional volumes for all compute pods. Appended to the volumes derived from the top-level `storage` block; on a name collision the entry here wins. (Login pods take the same storage-derived volumes plus any under `login.{common,userPods,groupPods}.pod.volumes`.)
      </td>

      <td>list</td>

      <td>
        ```yaml wrap theme={"system"}
        []
        ```
      </td>
    </tr>

    <tr>
      <td id="controller--etcConfigMap">
        **controller.etcConfigMap**\

        The ConfigMap(s) with keys mapping to files in `/etc/slurm` on the controller and compute slurmd pods. \
        &#x20;This ConfigMap **must not** contain: <ul> <li>`slurm.conf`</li> <li>`plugstack.conf`</li> <li>`gres.conf`</li> <li>`cgroup.conf`</li> <li>`namespace.yaml`</li> </ul> `topology.yaml` may be supplied here and overrides the operator's copy, Set `compute.generateTopology` to `false` so the operator stops regenerating a file you now own.
      </td>

      <td>string | list</td>

      <td>
        ```yaml wrap theme={"system"}
        null
        ```
      </td>
    </tr>

    <tr>
      <td id="controller--image">
        **controller.image**\

        The image to use for the controller.
      </td>

      <td>object</td>

      <td>
        ```yaml wrap theme={"system"}
        repository:
        tag:

        ```
      </td>
    </tr>

    <tr>
      <td id="controller--replicas">
        **controller.replicas**\

        The number of replicas of the controller to run, currently should be left at `1`.
      </td>

      <td>int</td>

      <td>
        ```yaml wrap theme={"system"}
        1
        ```
      </td>
    </tr>

    <tr>
      <td id="controller--resources">
        **controller.resources**\

        Resources for the controller container.
      </td>

      <td>object</td>
      <td>requests: cpu 4 memory 16Gi; limits: memory 16Gi</td>
    </tr>

    <tr>
      <td id="controller--securityContext">
        **controller.securityContext**\

        Security context for the controller container.
      </td>

      <td>object</td>

      <td>
        ```yaml wrap theme={"system"}
        runAsUser/runAsGroup 401
        ```
      </td>
    </tr>

    <tr>
      <td id="controller--stateVolume">
        **controller.stateVolume**\

        Controller's persistent volume claim.
      </td>

      <td>object</td>

      <td>
        ```yaml wrap theme={"system"}
        {
          "size": null,
          "storageClassName": null
        }
        ```
      </td>
    </tr>

    <tr>
      <td id="controller--stateVolume--size">
        **controller.stateVolume.size**\

        The size of the persistent volume claim.
      </td>

      <td>string</td>

      <td>
        ```yaml wrap theme={"system"}
        32Gi
        ```
      </td>
    </tr>

    <tr>
      <td id="controller--stateVolume--storageClassName">
        **controller.stateVolume.storageClassName**\

        The storage class name to use for the volume.
      </td>

      <td>string</td>

      <td>
        ```yaml wrap theme={"system"}
        omit; Kubernetes uses the cluster default storage class when unset.
        ```
      </td>
    </tr>

    <tr>
      <td id="controller--terminationGracePeriodSeconds">
        **controller.terminationGracePeriodSeconds**\

        The termination grace period for the controller.
      </td>

      <td>int</td>

      <td>
        ```yaml wrap theme={"system"}
        30
        ```
      </td>
    </tr>

    <tr>
      <td id="controller--volumeMounts">
        **controller.volumeMounts**\

        Additional volume mounts to apply to the controller pod.
      </td>

      <td>list</td>

      <td>
        ```yaml wrap theme={"system"}
        []
        ```
      </td>
    </tr>

    <tr>
      <td id="controller--volumes">
        **controller.volumes**\

        Additional volumes to mount to the controller pod.
      </td>

      <td>list</td>

      <td>
        ```yaml wrap theme={"system"}
        []
        ```
      </td>
    </tr>

    <tr>
      <td id="controller--watch">
        **controller.watch**\

        Configure the watch sidecar. Omit subkeys to use CRD / operator defaults.
      </td>

      <td>object</td>

      <td>
        ```yaml wrap theme={"system"}
        {
          "enabled": null,
          "interval": null
        }
        ```
      </td>
    </tr>

    <tr>
      <td id="controller--watch--enabled">
        **controller.watch.enabled**\

        Enable the controller watch sidecar.
      </td>

      <td>bool</td>

      <td>
        ```yaml wrap theme={"system"}
        true
        ```
      </td>
    </tr>

    <tr>
      <td id="controller--watch--interval">
        **controller.watch.interval**\

        Interval in seconds between watch sidecar checks.
      </td>

      <td>int</td>

      <td>
        ```yaml wrap theme={"system"}
        60
        ```
      </td>
    </tr>

    <tr>
      <td id="database--mysqlCluster">
        **database.mysqlCluster**\

        MySQL (MOCO) backend configuration, used when `accounting.database.backend` is `moco`. Each sub-key below is passed through to the SlurmCluster CR's database spec when set; omit a key (leave it null) to keep the operator default.
      </td>

      <td>object</td>

      <td>
        ```yaml wrap theme={"system"}
        See the per-field defaults below.
        ```
      </td>
    </tr>

    <tr>
      <td id="database--mysqlCluster--config">
        **database.mysqlCluster.config**\

        Additional MySQL configuration for my.cnf as key-value pairs. The operator automatically calculates the following values based on resources.limits.memory: - innodb\_buffer\_pool\_size: 50% of memory limit - innodb\_redo\_log\_capacity: 25% of innodb\_buffer\_pool\_size - innodb\_lock\_wait\_timeout: 900 (default) User-provided values in this config will override the calculated defaults. Note: If you override innodb\_buffer\_pool\_size, innodb\_redo\_log\_capacity will be recalculated based on your override (unless you also explicitly override it). Validation: innodb\_redo\_log\_capacity cannot exceed persistence.size. [MySQL option file documentation](https://dev.mysql.com/doc/refman/en/option-files.html)

        > [accordion] Example: click to expand
        >
        > ```yaml theme={"system"}
        > config:
        >   max_connections: "1000"
        >   wait_timeout: "28800"
        >   innodb_buffer_pool_size: "17179869184"  # Override to 16Gi
        > ```
      </td>

      <td>map\[string]string</td>

      <td>
        ```yaml wrap theme={"system"}
        Operator calculates innodb values from resources.limits.memory
        ```
      </td>
    </tr>

    <tr>
      <td id="database--mysqlCluster--image">
        **database.mysqlCluster.image**\

        The image to use for mysql. Passed through verbatim when set.
      </td>

      <td>object</td>

      <td>
        ```yaml wrap theme={"system"}
        ghcr.io/cybozu-go/moco/mysql:8.4.6
        ```
      </td>
    </tr>

    <tr>
      <td id="database--mysqlCluster--inodeLockFixer">
        **database.mysqlCluster.inodeLockFixer**\

        Init container that copies/moves/replaces the MySQL data directory to prevent known inode locking issues in certain storage environments. Applies to both managed backends: when `accounting.database.backend` is `moco` the operator adds the init container to the MySQLCluster pod template; when it is `cwdb` only `enabled` is passed through to the CWDBCluster and cwdb-operator runs its own fixer image. Sub-keys (passed through verbatim when set): `enabled` (bool) and `image` (object, `repository`/`tag`; `moco` only).
      </td>

      <td>object</td>
      <td>enabled: true, image: alpine:3.20.0</td>
    </tr>

    <tr>
      <td id="database--mysqlCluster--persistence">
        **database.mysqlCluster.persistence**\

        The volume settings to use for mysql. Passed through verbatim when set.
      </td>

      <td>object</td>
      <td>size: 512Gi, accessModes: \[ReadWriteOnce] (operator defaults); storageClassName unset uses the cluster default StorageClass</td>
    </tr>

    <tr>
      <td id="database--mysqlCluster--replicas">
        **database.mysqlCluster.replicas**\

        Number of MySQL replicas.
      </td>

      <td>int</td>

      <td>
        ```yaml wrap theme={"system"}
        1
        ```
      </td>
    </tr>

    <tr>
      <td id="database--mysqlCluster--resources">
        **database.mysqlCluster.resources**\

        Resources for the database container. Passed through verbatim when set.
      </td>

      <td>object</td>
      <td>requests: \{memory: 64Gi, cpu: "16"}, limits: \{memory: 64Gi}</td>
    </tr>

    <tr>
      <td id="jwt--existingSecret">
        **jwt.existingSecret**\

        The name of an existing secret containing the JWT private key; otherwise the chart generates one.
      </td>

      <td>string</td>

      <td>
        ```yaml wrap theme={"system"}
        (omit; chart generates a Secret)
        ```
      </td>
    </tr>

    <tr>
      <td id="login--common">
        **login.common**\

        Config used for both userPods and groupPods. Any value here can be overridden in the respective `userPods` or `groupPods` blocks.
      </td>

      <td>object</td>

      <td>
        ```yaml wrap theme={"system"}
        {
          "pod": {
            "affinity": {},
            "automountServiceAccountToken": null,
            "containers": [],
            "env": [],
            "hostAliases": [],
            "image": {
              "repository": null,
              "tag": null
            },
            "podSecurityContext": {},
            "resources": {},
            "securityContext": {},
            "serviceAccountName": null,
            "tolerations": [],
            "volumeMounts": [],
            "volumes": []
          },
          "service": {
            "additionalPorts": [],
            "annotations": {},
            "enabled": null,
            "externalTrafficPolicy": null,
            "individual": {},
            "labels": {},
            "loadBalancerClass": null,
            "type": null
          }
        }
        ```
      </td>
    </tr>

    <tr>
      <td id="login--common--pod--affinity">
        **login.common.pod.affinity**\

        Affinity constraining which nodes login pods schedule onto. Login pods do not inherit `slurmCluster.spec.affinity` (which targets control-plane components), so this is the only affinity applied to login pods. When unset, login pods receive no affinity.
      </td>

      <td>object</td>

      <td>
        ```yaml wrap theme={"system"}
        map[]
        ```
      </td>
    </tr>

    <tr>
      <td id="login--common--pod--automountServiceAccountToken">
        **login.common.pod.automountServiceAccountToken**\

        Automatically mount the service account token into the login pod.
      </td>

      <td>bool</td>

      <td>
        ```yaml wrap theme={"system"}
        false
        ```
      </td>
    </tr>

    <tr>
      <td id="login--common--pod--containers">
        **login.common.pod.containers**\

        Additional sidecar containers to add to the login pod.
      </td>

      <td>list</td>

      <td>
        ```yaml wrap theme={"system"}
        []
        ```
      </td>
    </tr>

    <tr>
      <td id="login--common--pod--env">
        **login.common.pod.env**\

        Additional environment variables passed to the sshd container.
      </td>

      <td>list</td>

      <td>
        ```yaml wrap theme={"system"}
        []
        ```
      </td>
    </tr>

    <tr>
      <td id="login--common--pod--hostAliases">
        **login.common.pod.hostAliases**\

        Pod-level override of hostname resolution when DNS and other options are not applicable. See [ Adding entries to Pod /etc/hosts with HostAliases](https://kubernetes.io/docs/tasks/network/customize-hosts-file-for-pods/).
      </td>

      <td>list</td>

      <td>
        ```yaml wrap theme={"system"}
        []
        ```
      </td>
    </tr>

    <tr>
      <td id="login--common--pod--image">
        **login.common.pod.image**\

        Image used by the login pod sshd container. When `repository` is omitted, the chart builds `<slurm.registry>/<name>` with `name` defaulting to `controller-extras`.
      </td>

      <td>object</td>

      <td>
        ```yaml wrap theme={"system"}
        repository:
        tag:

        ```
      </td>
    </tr>

    <tr>
      <td id="login--common--pod--podSecurityContext">
        **login.common.pod.podSecurityContext**\

        Pod-level security context applied to the login pod.
      </td>

      <td>object</td>

      <td>
        ```yaml wrap theme={"system"}
        map[]
        ```
      </td>
    </tr>

    <tr>
      <td id="login--common--pod--resources">
        **login.common.pod.resources**\

        sshd container resources.
      </td>

      <td>object</td>
      <td>requests: cpu 4 memory 8Gi; limits: memory 8Gi</td>
    </tr>

    <tr>
      <td id="login--common--pod--securityContext">
        **login.common.pod.securityContext**\

        Container-level security context applied to the login sshd container. Exposed to support workloads such as enroot that require capabilities (e.g. SYS\_ADMIN) or a seccomp profile. Setting `capabilities` replaces the operator defaults (`SYS_RESOURCE`), so include `SYS_RESOURCE` to keep sshd protected from the OOM killer.
      </td>

      <td>object</td>

      <td>
        ```yaml wrap theme={"system"}
        map[]
        ```
      </td>
    </tr>

    <tr>
      <td id="login--common--pod--serviceAccountName">
        **login.common.pod.serviceAccountName**\

        Service account name for the login pod.
      </td>

      <td>string</td>

      <td>
        ```yaml wrap theme={"system"}
        "default"
        ```
      </td>
    </tr>

    <tr>
      <td id="login--common--pod--tolerations">
        **login.common.pod.tolerations**\

        Tolerations allowing login pods to schedule onto tainted nodes. When set, these replace the cluster-wide `slurmCluster.spec.tolerations` for login pods; when unset, the cluster-wide tolerations apply.
      </td>

      <td>list</td>

      <td>
        ```yaml wrap theme={"system"}
        []
        ```
      </td>
    </tr>

    <tr>
      <td id="login--common--pod--volumeMounts">
        **login.common.pod.volumeMounts**\

        Additional volume mounts for the login pods. Appended to the mounts derived from the top-level `storage` block; on a mountPath collision the entry here wins. (Compute pods take the same storage-derived mounts plus any under `compute.volumeMounts`.)
      </td>

      <td>list</td>

      <td>
        ```yaml wrap theme={"system"}
        []
        ```
      </td>
    </tr>

    <tr>
      <td id="login--common--pod--volumes">
        **login.common.pod.volumes**\

        Additional volumes for the login pods. Appended to the volumes derived from the top-level `storage` block; on a name collision the entry here wins. (Compute pods take the same storage-derived volumes plus any under `compute.volumes`.)

        > [accordion] Example: click to expand
        >
        > ```yaml theme={"system"}
        > volumes:
        >   - name: cache-vol
        >     emptyDir:
        >       medium: Memory
        > ```
      </td>

      <td>list</td>

      <td>
        ```yaml wrap theme={"system"}
        []
        ```
      </td>
    </tr>

    <tr>
      <td id="login--common--service--additionalPorts">
        **login.common.service.additionalPorts**\

        Additional port definitions to expose on each login Service.

        > [accordion] Example: click to expand
        >
        > ```yaml theme={"system"}
        > additionalPorts:
        >   - name: eternal-shell
        >     port: 2022
        >     targetPort: 20222 # optional
        >     protocol: TCP # optional
        > ```
      </td>

      <td>list</td>

      <td>
        ```yaml wrap theme={"system"}
        []
        ```
      </td>
    </tr>

    <tr>
      <td id="login--common--service--annotations">
        **login.common.service.annotations**\

        Annotations applied to every per-entity login Service. `%s` is replaced with the entity name (user or group) and `%h` with a 7-character hash of the entity name.
      </td>

      <td>object</td>

      <td>
        ```yaml wrap theme={"system"}
        {}
        ```
      </td>
    </tr>

    <tr>
      <td id="login--common--service--enabled">
        **login.common.service.enabled**\

        Enable the creation of service(s) for login pods.
      </td>

      <td>bool</td>

      <td>
        ```yaml wrap theme={"system"}
        true
        ```
      </td>
    </tr>

    <tr>
      <td id="login--common--service--externalTrafficPolicy">
        **login.common.service.externalTrafficPolicy**\

        External traffic policy.
      </td>

      <td>string</td>

      <td>
        ```yaml wrap theme={"system"}
        Local
        ```
      </td>
    </tr>

    <tr>
      <td id="login--common--service--individual">
        **login.common.service.individual**\

        Per-entity Service metadata overrides keyed by user or group name. Each value is an object with optional `annotations` and `labels` maps; overrides are applied on top of the kind's `annotations`/`labels` and win on conflict.

        > [accordion] Example: click to expand
        >
        > ```yaml theme={"system"}
        > individual:
        >   jdoe:
        >     annotations:
        >       dns.example.com/hostname: jdoe.login.example.com
        > ```
      </td>

      <td>object</td>

      <td>
        ```yaml wrap theme={"system"}
        {}
        ```
      </td>
    </tr>

    <tr>
      <td id="login--common--service--labels">
        **login.common.service.labels**\

        Labels applied to every per-entity login Service. `%s`/`%h` substitution is supported.
      </td>

      <td>object</td>

      <td>
        ```yaml wrap theme={"system"}
        {}
        ```
      </td>
    </tr>

    <tr>
      <td id="login--common--service--loadBalancerClass">
        **login.common.service.loadBalancerClass**\

        Load balancer class to use for login Services.
      </td>

      <td>string</td>

      <td>
        ```yaml wrap theme={"system"}
        null
        ```
      </td>
    </tr>

    <tr>
      <td id="login--common--service--type">
        **login.common.service.type**\

        The type of service to create. This defaults to `LoadBalancer` for cloud deployments. For development and test systems without an external load balancer to handle the service routing, such as when deploying on [ kind (Kubernetes IN Docker)](https://kind.sigs.k8s.io/), this may be set to `ClusterIP`.
      </td>

      <td>string</td>

      <td>
        ```yaml wrap theme={"system"}
        LoadBalancer
        ```
      </td>
    </tr>

    <tr>
      <td id="login--groupPods">
        **login.groupPods**\

        Per-group login pod overrides (one shared StatefulSet per group). Same shape as `login.common`; values set here override the corresponding fields from `common`.

        > [accordion] Example: click to expand
        >
        > ```yaml theme={"system"}
        > groupPods:
        >   pod:
        >     resources:
        >       requests:
        >         cpu: 4
        >         memory: 8Gi
        >       limits:
        >         memory: 8Gi
        >   service:
        >     annotations:
        >       service.beta.kubernetes.io/external-hostname: "groups.login.example.com"
        > ```
      </td>

      <td>object</td>

      <td>
        ```yaml wrap theme={"system"}
        map[]
        ```
      </td>
    </tr>

    <tr>
      <td id="login--groups">
        **login.groups**\

        Groups to enumerate for per-user and per-group login pods. Users are resolved from nsscache secrets. Each entry has required `name` and optional `userPods` (default false) and `groupPods` (default true) to control whether per-user pods and the shared group pod are created for that group.

        > [accordion] Example: click to expand
        >
        > ```yaml theme={"system"}
        > groups:
        >   - name: slurm-users
        >     userPods: true
        >     groupPods: true
        >   - name: sudo-users
        >     userPods: true
        >     groupPods: false
        > ```
      </td>

      <td>list</td>

      <td>
        ```yaml wrap theme={"system"}
        []
        ```
      </td>
    </tr>

    <tr>
      <td id="login--s6">
        **login.s6**\

        Additional s6 services for login pods, shared across all login pods in the cluster. **oneshot** and **longrun** jobs are supported. See [Running Scripts with S6](https://docs.coreweave.com/products/sunk/development-on-slurm/run-scripts-with-s6.md) for more information.

        > [accordion] Example: click to expand
        >
        > ```yaml theme={"system"}
        > s6:
        >   packages:
        >     type: oneshot
        >     timeoutUp: 360000 # 360 seconds
        >     timeoutDown: 0
        >     script: |
        >       #!/usr/bin/env bash
        >       apt -y update
        >       apt -y install nginx
        >   nginx:
        >     type: longrun
        >     timeoutUp: 360000 # 360 seconds
        >     timeoutDown: 0
        >     script: |
        >       #!/usr/bin/env bash
        >       nginx -g "daemon off;"
        > ```
      </td>

      <td>object</td>

      <td>
        ```yaml wrap theme={"system"}
        {}
        ```
      </td>
    </tr>

    <tr>
      <td id="login--sshKeyVolume">
        **login.sshKeyVolume**\

        The shared SSH host keys persistent volume claim. One PVC is provisioned per cluster and mounted by every login pod (both userPods and groupPods).
      </td>

      <td>object</td>

      <td>
        ```yaml wrap theme={"system"}
        {
          "accessModes": null,
          "enabled": null,
          "size": null,
          "storageClassName": null
        }
        ```
      </td>
    </tr>

    <tr>
      <td id="login--sshKeyVolume--accessModes">
        **login.sshKeyVolume.accessModes**\

        PVC access modes. If scaling login beyond a single replica per kind this must be `ReadWriteMany`. In a development setting with a volume provider that doesn't support `ReadWriteMany`, such as [kind](https://kind.sigs.k8s.io/), set to `[ReadWriteOnce]`.
      </td>

      <td>list</td>

      <td>
        ```yaml wrap theme={"system"}
        [ReadWriteMany]
        ```
      </td>
    </tr>

    <tr>
      <td id="login--sshKeyVolume--enabled">
        **login.sshKeyVolume.enabled**\

        Enable provisioning of the shared SSH host keys PVC.
      </td>

      <td>bool</td>

      <td>
        ```yaml wrap theme={"system"}
        true
        ```
      </td>
    </tr>

    <tr>
      <td id="login--sshKeyVolume--size">
        **login.sshKeyVolume.size**\

        PVC size.
      </td>

      <td>string</td>

      <td>
        ```yaml wrap theme={"system"}
        1Gi
        ```
      </td>
    </tr>

    <tr>
      <td id="login--sshKeyVolume--storageClassName">
        **login.sshKeyVolume.storageClassName**\

        Storage class name to use for the PVC.
      </td>

      <td>string</td>

      <td>
        ```yaml wrap theme={"system"}
        omit; Kubernetes uses the cluster default storage class when unset.
        ```
      </td>
    </tr>

    <tr>
      <td id="login--sshdConfig">
        **login.sshdConfig**\

        Additional sshd configuration entries. Rendered once per cluster into a shared ConfigMap mounted by every login pod.

        > [accordion] Example: click to expand
        >
        > ```yaml theme={"system"}
        > sshdConfig:
        >   PasswordAuthentication: "no"
        > ```
      </td>

      <td>object</td>

      <td>
        ```yaml wrap theme={"system"}
        PasswordAuthentication: "no"
        ```
      </td>
    </tr>

    <tr>
      <td id="login--topologySpreadConstraints">
        **login.topologySpreadConstraints**\

        Topology spread constraints applied to every login pod (per-user and per-group), shared across all login pods in the cluster. When unset (`null`), the operator applies a default that spreads login pods across `kubernetes.io/hostname` with `maxSkew: 1` and `whenUnsatisfiable: ScheduleAnyway`, scoped to this cluster's login pods. Set to an empty list (`[]`) to turn off the operator's default; any cluster-level scheduler defaults still apply. Provide your own constraints to replace the default. If you use `whenUnsatisfiable: DoNotSchedule`, also set `nodeTaintsPolicy: Honor`; otherwise tainted nodes the login pods can't use count as empty domains and login pods can stay Pending. Changes apply to a login pod only when it is next recreated; running login pods are not restarted or moved.

        > [accordion] Example: click to expand
        >
        > ```yaml theme={"system"}
        > topologySpreadConstraints:
        >   - maxSkew: 1
        >     topologyKey: kubernetes.io/hostname
        >     whenUnsatisfiable: ScheduleAnyway
        >     labelSelector:
        >       matchLabels:
        >         # <release-name> is this chart's Helm release name.
        >         app.kubernetes.io/instance: <release-name>-login
        >         app.kubernetes.io/component: login
        > ```
      </td>

      <td>list</td>

      <td>
        ```yaml wrap theme={"system"}
        null
        ```
      </td>
    </tr>

    <tr>
      <td id="login--userPods">
        **login.userPods**\

        Per-user login pod overrides. Same shape as `login.common`; values set here override the corresponding fields from `common`. Anything not set here inherits from `common`.

        > [accordion] Example: click to expand
        >
        > ```yaml theme={"system"}
        > userPods:
        >   pod:
        >     resources:
        >       requests:
        >         cpu: 4
        >         memory: 8Gi
        >       limits:
        >         memory: 8Gi
        >   service:
        >     annotations:
        >       service.beta.kubernetes.io/external-hostname: "%s.login.example.com"
        > ```
      </td>

      <td>object</td>

      <td>
        ```yaml wrap theme={"system"}
        map[]
        ```
      </td>
    </tr>

    <tr>
      <td id="munge--args">
        **munge.args**\

        The additional arguments to pass to the munge container.  The defaults run Munge with 10 threads instead of 2.
      </td>

      <td>list</td>

      <td>
        ```yaml wrap theme={"system"}
        [
          "--num-threads",
          "10"
        ]
        ```
      </td>
    </tr>

    <tr>
      <td id="munge--resources">
        **munge.resources**\

        Resources for the munge container.
      </td>

      <td>object</td>
      <td>requests: cpu 1 memory 2Gi; limits: memory 2Gi</td>
    </tr>

    <tr>
      <td id="nsscache--defaultShell">
        **nsscache.defaultShell**\

        The default shell for all users (used for both LDAP and SCIM). The login and compute images ship both `/bin/bash` and `/bin/zsh` with the same SUNK aliases and umask handling. A single user can override it through the SCIM `sunkLoginShell` attribute or the LDAP `loginShell` attribute.
      </td>

      <td>string</td>

      <td>
        ```yaml wrap theme={"system"}
        /bin/bash
        ```
      </td>
    </tr>

    <tr>
      <td id="nsscache--enabled">
        **nsscache.enabled**\

        Enable nsscache. Set explicitly to `false` to disable nsscache-related volumes,
      </td>

      <td>bool</td>

      <td>
        ```yaml wrap theme={"system"}
        true
        ```
      </td>
    </tr>

    <tr>
      <td id="nsscache--existingSecret">
        **nsscache.existingSecret**\

        Name of an existing k8s secret containing the authentication credentials for this domain. For SCIM, this secret should contain a key named `nsscache-scim-auth-token` which contains the token to use for the SCIM server. For LDAP, this secret should contain a key named `nsscache-ldap-password` which contains the password to use for the LDAP bind DN.
      </td>

      <td>string</td>

      <td>
        ```yaml wrap theme={"system"}
        null
        ```
      </td>
    </tr>

    <tr>
      <td id="nsscache--fetchInterval">
        **nsscache.fetchInterval**\

        The interval in seconds between nsscache updates and Slurm user provisioning sync runs.
      </td>

      <td>int</td>

      <td>
        ```yaml wrap theme={"system"}
        60
        ```
      </td>
    </tr>

    <tr>
      <td id="nsscache--groups">
        **nsscache.groups**\

        List of groups for both POSIX users and Slurm user creation. Example: groups:   - slurm-users   - sudo-users
      </td>

      <td>list</td>

      <td>
        ```yaml wrap theme={"system"}
        []
        ```
      </td>
    </tr>

    <tr>
      <td id="nsscache--image">
        **nsscache.image**\

        The image to use for nsscache containers.
      </td>

      <td>object</td>

      <td>
        ```yaml wrap theme={"system"}
        repository:
        tag:

        ```
      </td>
    </tr>

    <tr>
      <td id="nsscache--nsscacheConfig">
        **nsscache.nsscacheConfig**\

        Per-section nsscache.conf overrides. Leave values null to use chart helpers and operator defaults; only non-empty values are passed through to the SlurmCluster CR.
      </td>

      <td>object</td>

      <td>
        ```yaml wrap theme={"system"}
        null
        ```
      </td>
    </tr>

    <tr>
      <td id="nsscache--overrideHomeDirectory">
        **nsscache.overrideHomeDirectory**\

        The home directory pattern to override for all users. %%u will be replaced with the username (used for both LDAP and SCIM).
      </td>

      <td>string</td>

      <td>
        ```yaml wrap theme={"system"}
        /mnt/home/%%u
        ```
      </td>
    </tr>

    <tr>
      <td id="nsscache--slurmUserProvisioning">
        **nsscache.slurmUserProvisioning**\

        Configuration for slurm user provisioning.
      </td>

      <td>object</td>

      <td>
        ```yaml wrap theme={"system"}
        {
          "defaultSlurmAccount": null,
          "enabled": null
        }
        ```
      </td>
    </tr>

    <tr>
      <td id="nsscache--slurmUserProvisioning--defaultSlurmAccount">
        **nsscache.slurmUserProvisioning.defaultSlurmAccount**\

        The default Slurm account for automated provisioning of users.
      </td>

      <td>string</td>

      <td>
        ```yaml wrap theme={"system"}
        cw-sup
        ```
      </td>
    </tr>

    <tr>
      <td id="nsscache--slurmUserProvisioning--enabled">
        **nsscache.slurmUserProvisioning.enabled**\

        Enable slurmUserProvisioning.
      </td>

      <td>bool</td>

      <td>
        ```yaml wrap theme={"system"}
        true
        ```
      </td>
    </tr>

    <tr>
      <td id="nsscache--sudoGroups">
        **nsscache.sudoGroups**\

        List of Unix groups with sudo privileges.
      </td>

      <td>list</td>

      <td>
        ```yaml wrap theme={"system"}
        []
        ```
      </td>
    </tr>

    <tr>
      <td id="partitions">
        **partitions**\

        Partitions configuration for the slurm cluster The key is the partition name and the value is the partition configuration.  The following partition keys are special keys that defines partition configuration: - auto: If enabled, it reads nodeset information and automatically creates partition.   Supports `enabled` and `config`; config entries are merged case-insensitively into   every auto-generated partition (PartitionName/Nodeset/Nodes/Default are rejected). - all: Creates a partition for all nodes, and set to default if no default partition is set.   Overriding it keeps Nodes=ALL unless the override selects nodes itself.  Partitions may omit node selection (`feature` / a `Nodes` config entry); Slurm treats them as partitions with no nodes. Disabling `all` requires at least one other enabled partition; an enabled `auto` counts, but only yields partitions once NodeSets are discovered.

        > [accordion] Partition Configuration
        >
        > ```yaml theme={"system"}
        > partitions:
        >   hpc-mid:
        >     enabled: true
        >     feature: ALL
        >     config:
        >       PriorityTier: "16384"
        >       Priority: "16384"
        >       DefCpuPerGPU: "16"
        >       DefMemPerCPU: "15500"
        >       MaxTime: "INFINITE"
        >       State: "UP"
        > ```
      </td>

      <td>object</td>

      <td>
        ```yaml wrap theme={"system"}
        {
          "auto": {
            "config": null,
            "enabled": null
          }
        }
        ```
      </td>
    </tr>

    <tr>
      <td id="partitions--auto">
        **partitions.auto**\

        auto is a reserved key that defines if nodeset detection is automated added to partitions. Supports `enabled` and `config`; other partition fields are rejected at admission.
      </td>

      <td>object</td>

      <td>
        ```yaml wrap theme={"system"}
        {
          "config": null,
          "enabled": null
        }
        ```
      </td>
    </tr>

    <tr>
      <td id="partitions--auto--enabled">
        **partitions.auto.enabled**\

        Enable automatic partition generation from discovered NodeSets.
      </td>

      <td>bool</td>

      <td>
        ```yaml wrap theme={"system"}
        true
        ```
      </td>
    </tr>

    <tr>
      <td id="rest--args">
        **rest.args**\

        Arguments passed to slurmrestd. The listen address is appended automatically by the operator. Use -d to optionally pin a data\_parser plugin (e.g. "-dv0.0.44").
      </td>

      <td>list</td>

      <td>
        ```yaml wrap theme={"system"}
        ["-vv", "-sslurmdbd,slurmctld"]
        ```
      </td>
    </tr>

    <tr>
      <td id="rest--containers">
        **rest.containers**\

        Additional sidecar containers to add to the restd pod.
      </td>

      <td>list</td>

      <td>
        ```yaml wrap theme={"system"}
        []
        ```
      </td>
    </tr>

    <tr>
      <td id="rest--enabled">
        **rest.enabled**\

        When true, the chart emits `restd.enabled: true` on the SlurmCluster and the operator creates slurmrestd. When omitted, the chart does not emit `spec.restd` from this toggle.
      </td>

      <td>bool</td>

      <td>
        ```yaml wrap theme={"system"}
        false
        ```
      </td>
    </tr>

    <tr>
      <td id="rest--image">
        **rest.image**\

        Image override for the slurmrestd container. Defaults to cluster `slurmImage`.
      </td>

      <td>object</td>

      <td>
        ```yaml wrap theme={"system"}
        repository:
        tag:

        ```
      </td>
    </tr>

    <tr>
      <td id="rest--livenessProbe">
        **rest.livenessProbe**\

        Liveness probe override for the slurmrestd container.
      </td>

      <td>object</td>

      <td>
        ```yaml wrap theme={"system"}
        TCP socket on the slurmrestd port; periodSeconds 10; failureThreshold 2
        ```
      </td>
    </tr>

    <tr>
      <td id="rest--readinessProbe">
        **rest.readinessProbe**\

        Readiness probe override for the slurmrestd container.
      </td>

      <td>object</td>

      <td>
        ```yaml wrap theme={"system"}
        TCP socket on the slurmrestd port; periodSeconds 5; failureThreshold 1
        ```
      </td>
    </tr>

    <tr>
      <td id="rest--replicas">
        **rest.replicas**\

        The number of replicas of the rest pod to run. \

      </td>

      <td>int</td>

      <td>
        ```yaml wrap theme={"system"}
        1
        ```
      </td>
    </tr>

    <tr>
      <td id="rest--resources">
        **rest.resources**\

        Resources for the slurmrestd container. \
        &#x20;These defaults are appropriate for small and medium-sized clusters.
      </td>

      <td>object</td>
      <td>requests: cpu 2 memory 8Gi; limits: memory 64Gi</td>
    </tr>

    <tr>
      <td id="rest--service--additionalPorts">
        **rest.service.additionalPorts**\

        Additional port definitions to expose on the Service.

        > [accordion] Example: click to expand
        >
        > ```yaml theme={"system"}
        > additionalPorts:
        >   - name: proxy
        >     port: 8080
        >     targetPort: 8080 # optional
        >     protocol: TCP # optional
        > ```
      </td>

      <td>list</td>

      <td>
        ```yaml wrap theme={"system"}
        []
        ```
      </td>
    </tr>

    <tr>
      <td id="rest--service--annotations">
        **rest.service.annotations**\

        Additional annotations to apply to the slurmrestd Service.
      </td>

      <td>object</td>

      <td>
        ```yaml wrap theme={"system"}
        {}
        ```
      </td>
    </tr>

    <tr>
      <td id="rest--service--clusterIP">
        **rest.service.clusterIP**\

        The clusterIP for the Service. Use `None` for a headless Service.
      </td>

      <td>string</td>

      <td>
        ```yaml wrap theme={"system"}
        None
        ```
      </td>
    </tr>

    <tr>
      <td id="rest--service--enabled">
        **rest.service.enabled**\

        Enable the creation of the Service for the slurmrestd pod.
      </td>

      <td>bool</td>

      <td>
        ```yaml wrap theme={"system"}
        true
        ```
      </td>
    </tr>

    <tr>
      <td id="rest--service--externalName">
        **rest.service.externalName**\

        The external DNS name the Service resolves to. Only valid when `type` is `ExternalName`; the operator then drops the clusterIP, selector, and ports.
      </td>

      <td>string</td>

      <td>
        ```yaml wrap theme={"system"}
        null
        ```
      </td>
    </tr>

    <tr>
      <td id="rest--service--externalTrafficPolicy">
        **rest.service.externalTrafficPolicy**\

        The external traffic policy.
      </td>

      <td>string</td>

      <td>
        ```yaml wrap theme={"system"}
        null
        ```
      </td>
    </tr>

    <tr>
      <td id="rest--service--labels">
        **rest.service.labels**\

        Additional labels to apply to the slurmrestd Service.
      </td>

      <td>object</td>

      <td>
        ```yaml wrap theme={"system"}
        {}
        ```
      </td>
    </tr>

    <tr>
      <td id="rest--service--loadBalancerClass">
        **rest.service.loadBalancerClass**\

        The load balancer class to use when `type` is `LoadBalancer`.
      </td>

      <td>string</td>

      <td>
        ```yaml wrap theme={"system"}
        null
        ```
      </td>
    </tr>

    <tr>
      <td id="rest--service--type">
        **rest.service.type**\

        The type of Service to create. One of `ClusterIP`, `NodePort`, `LoadBalancer`, or `ExternalName`.
      </td>

      <td>string</td>

      <td>
        ```yaml wrap theme={"system"}
        ClusterIP
        ```
      </td>
    </tr>

    <tr>
      <td id="rest--startupProbe">
        **rest.startupProbe**\

        Startup probe override for the slurmrestd container.
      </td>

      <td>object</td>

      <td>
        ```yaml wrap theme={"system"}
        TCP socket on the slurmrestd port; periodSeconds 2; failureThreshold 20
        ```
      </td>
    </tr>

    <tr>
      <td id="rest--volumeMounts">
        **rest.volumeMounts**\

        Additional volume mounts to apply to the rest container (passed through to CR when set).
      </td>

      <td>list</td>

      <td>
        ```yaml wrap theme={"system"}
        []
        ```
      </td>
    </tr>

    <tr>
      <td id="rest--volumes">
        **rest.volumes**\

        Additional volumes to add to the restd pod (passed through to CR when set).
      </td>

      <td>list</td>

      <td>
        ```yaml wrap theme={"system"}
        []
        ```
      </td>
    </tr>

    <tr>
      <td id="scheduler--config">
        **scheduler.config**\

        Scheduler and Slurm client configuration.
      </td>

      <td>object</td>

      <td>
        ```yaml wrap theme={"system"}
        {
          "scheduler": {},
          "slurm": {}
        }
        ```
      </td>
    </tr>

    <tr>
      <td id="scheduler--config--scheduler">
        **scheduler.config.scheduler**\

        Scheduler-specific configuration.

        > [accordion] Operator defaults
        >
        >         <table>
        >           <tr><th>Key</th><th>Type</th><th>Description</th><th>Default</th></tr>
        >           <tr><td>`gpuTypes`</td><td>map</td><td>Mapping of k8s GPU types (node affinity key `gpu.nvidia.com/class`) to Slurm gres GPU types; added to a job's description. Entries are merged over the defaults by key.</td><td>`{A100_NVLINK_80GB: a100, H100_NVLINK_80GB: h100}`</td></tr>
        >           <tr><td>`orphanJobSweep.dryRun`</td><td>bool</td><td>Report confirmed orphan Slurm jobs without cancelling them.</td><td>`false`</td></tr>
        >           <tr><td>`orphanJobSweep.interval`</td><td>string</td><td>Interval between orphan Slurm job sweep passes. A job must be unclaimed in two consecutive passes before it is cancelled.</td><td>`30s`</td></tr>
        >           <tr><td>`pollInterval`</td><td>string</td><td>Polling interval for the Slurm API.</td><td>`10s`</td></tr>
        >           <tr><td>`terminationOffset`</td><td>string</td><td>Offset to the termination grace period to account for communication delays.</td><td>`5s`</td></tr>
        >         </table>
        >
        > ```yaml theme={"system"}
        > scheduler:
        >   gpuTypes:
        >     H100_NVLINK_80GB: h100
        >     A100_NVLINK_80GB: a100
        >   orphanJobSweep:
        >     dryRun: false
        >     interval: 30s
        >   pollInterval: 10s
        >   terminationOffset: 5s
        > ```
      </td>

      <td>object</td>
      <td>See the operator defaults below.</td>
    </tr>

    <tr>
      <td id="scheduler--config--slurm">
        **scheduler.config.slurm**\

        Slurm client configuration.

        > [accordion] Operator defaults
        >
        >         <table>
        >           <tr><th>Key</th><th>Type</th><th>Description</th><th>Default</th></tr>
        >           <tr><td>`poolSize`</td><td>int</td><td>Number of connections to maintain in the connection pool.</td><td>`10`</td></tr>
        >           <tr><td>`usePersistentConnection`</td><td>bool</td><td>Use Slurm's persistent connections for connection reuse.</td><td>`true`</td></tr>
        >         </table>
        >
        > ```yaml theme={"system"}
        > slurm:
        >   poolSize: 10
        >   usePersistentConnection: true
        > ```
      </td>

      <td>object</td>
      <td>See the operator defaults below.</td>
    </tr>

    <tr>
      <td id="scheduler--enabled">
        **scheduler.enabled**\

        Enable the scheduler. \
        &#x20;To schedule k8s pods on the Slurm cluster nodes, this must be enabled.
      </td>

      <td>bool</td>

      <td>
        ```yaml wrap theme={"system"}
        false
        ```
      </td>
    </tr>

    <tr>
      <td id="scheduler--image">
        **scheduler.image**\

        The image to use for the scheduler.
      </td>

      <td>object</td>

      <td>
        ```yaml wrap theme={"system"}
        repository:
        tag:

        ```
      </td>
    </tr>

    <tr>
      <td id="scheduler--resources">
        **scheduler.resources**\

        Resources for the scheduler container.
      </td>

      <td>object</td>
      <td>requests: cpu 200m memory 1Gi; limits: memory 1Gi</td>
    </tr>

    <tr>
      <td id="scheduler--scope">
        **scheduler.scope**\

        Scheduler scope configuration. The `type` sub-key (string) selects the scope: `cluster` or `namespace`. When `type` is `namespace`, set `namespaces` below. `scope` is passed through verbatim, so set `type` only when overriding the default.
      </td>

      <td>object</td>

      <td>
        ```yaml wrap theme={"system"}
        type: cluster
        ```
      </td>
    </tr>

    <tr>
      <td id="scheduler--scope--namespaces">
        **scheduler.scope.namespaces**\

        The list of the namespaces to scope the scheduler to. \
        &#x20;Only used when `scope.type` is set to `namespace`. Namespaces other than the release namespace will need role bindings created.
      </td>

      <td>list</td>

      <td>
        ```yaml wrap theme={"system"}
        []
        ```
      </td>
    </tr>

    <tr>
      <td id="slurmCluster--spec">
        **slurmCluster.spec**\

        Specification for the SlurmCluster custom resource
      </td>

      <td>object</td>

      <td>
        ```yaml wrap theme={"system"}
        {
          "affinity": {
            "nodeAffinity": {
              "requiredDuringSchedulingIgnoredDuringExecution": {
                "nodeSelectorTerms": [
                  {
                    "matchExpressions": [
                      {
                        "key": "node.coreweave.cloud/class",
                        "operator": "In",
                        "values": [
                          "cpu"
                        ]
                      }
                    ]
                  }
                ]
              }
            }
          },
          "annotations": {},
          "dnsConfig": {
            "additionalSearches": []
          },
          "imagePullSecrets": [],
          "labels": {},
          "priorityClassName": null,
          "protocolVersion": null,
          "slurmImage": {
            "repository": null,
            "tag": null
          },
          "sunkImage": {
            "repository": null,
            "tag": null
          },
          "tolerations": null,
          "version": null
        }
        ```
      </td>
    </tr>

    <tr>
      <td id="slurmCluster--spec--affinity">
        **slurmCluster.spec.affinity**\

        Affinity for control plane component deployments. The default schedules control-plane components onto CoreWeave CPU nodes; set to `{}` or override to change scheduling.
      </td>

      <td>object</td>

      <td>
        ```yaml wrap theme={"system"}
        nodeAffinity:
            requiredDuringSchedulingIgnoredDuringExecution:
                nodeSelectorTerms:
                    - matchExpressions:
                        - key: node.coreweave.cloud/class
                          operator: In
                          values:
                            - cpu

        ```
      </td>
    </tr>

    <tr>
      <td id="slurmCluster--spec--annotations">
        **slurmCluster.spec.annotations**\

        Additional custom annotations to add to control plane component resources (deployment, service, etc.)
      </td>

      <td>object</td>

      <td>
        ```yaml wrap theme={"system"}
        {}
        ```
      </td>
    </tr>

    <tr>
      <td id="slurmCluster--spec--dnsConfig--additionalSearches">
        **slurmCluster.spec.dnsConfig.additionalSearches**\

        A list of namespaces to add to the list of DNS searches. These additional searches extend hostname lookup in the control-plane, compute, and login pods. Default dns searches: - name-compute.namespace.svc.cluster.local - slurm\_cluster\_name-controller.namespace.svc.cluster.local
      </td>

      <td>list</td>

      <td>
        ```yaml wrap theme={"system"}
        []
        ```
      </td>
    </tr>

    <tr>
      <td id="slurmCluster--spec--imagePullSecrets">
        **slurmCluster.spec.imagePullSecrets**\

        Image pull secrets for all cluster components, including compute (NodeSet) pods.
      </td>

      <td>list</td>

      <td>
        ```yaml wrap theme={"system"}
        []
        ```
      </td>
    </tr>

    <tr>
      <td id="slurmCluster--spec--labels">
        **slurmCluster.spec.labels**\

        Additional custom labels to add to control plane component resources (deployment, service, etc.)
      </td>

      <td>object</td>

      <td>
        ```yaml wrap theme={"system"}
        {}
        ```
      </td>
    </tr>

    <tr>
      <td id="slurmCluster--spec--priorityClassName">
        **slurmCluster.spec.priorityClassName**\

        Priority class name for all control plane components.
      </td>

      <td>string</td>

      <td>
        ```yaml wrap theme={"system"}
        sunk-control-plane
        ```
      </td>
    </tr>

    <tr>
      <td id="slurmCluster--spec--protocolVersion">
        **slurmCluster.spec.protocolVersion**\

        The protocol version to use for communication with the Slurm controller.
      </td>

      <td>string</td>

      <td>
        ```yaml wrap theme={"system"}
        current wire protocol
        ```
      </td>
    </tr>

    <tr>
      <td id="slurmCluster--spec--slurmImage">
        **slurmCluster.spec.slurmImage**\

        Default image configuration for Slurm components (slurmctld, login nodes, nsscache, cleanup-completing) when component-specific images are not specified
      </td>

      <td>object</td>

      <td>
        ```yaml wrap theme={"system"}
        {
          "repository": null,
          "tag": null
        }
        ```
      </td>
    </tr>

    <tr>
      <td id="slurmCluster--spec--slurmImage--repository">
        **slurmCluster.spec.slurmImage.repository**\

        Container image repository
      </td>

      <td>string</td>

      <td>
        ```yaml wrap theme={"system"}
        ghcr.io/coreweave/slurm-containers/controller
        ```
      </td>
    </tr>

    <tr>
      <td id="slurmCluster--spec--slurmImage--tag">
        **slurmCluster.spec.slurmImage.tag**\

        Container image tag
      </td>

      <td>string</td>

      <td>
        ```yaml wrap theme={"system"}
        v{Chart.AppVersion}-ubuntu24.04
        ```
      </td>
    </tr>

    <tr>
      <td id="slurmCluster--spec--sunkImage">
        **slurmCluster.spec.sunkImage**\

        Default image configuration for operator components (syncer, scheduler) when component-specific images are not specified
      </td>

      <td>object</td>

      <td>
        ```yaml wrap theme={"system"}
        {
          "repository": null,
          "tag": null
        }
        ```
      </td>
    </tr>

    <tr>
      <td id="slurmCluster--spec--sunkImage--repository">
        **slurmCluster.spec.sunkImage.repository**\

        Container image repository
      </td>

      <td>string</td>

      <td>
        ```yaml wrap theme={"system"}
        images.coreweave.com/cluster-images/sunk/operator
        ```
      </td>
    </tr>

    <tr>
      <td id="slurmCluster--spec--sunkImage--tag">
        **slurmCluster.spec.sunkImage.tag**\

        Container image tag
      </td>

      <td>string</td>

      <td>
        ```yaml wrap theme={"system"}
        v{Chart.Version}
        ```
      </td>
    </tr>

    <tr>
      <td id="slurmCluster--spec--tolerations">
        **slurmCluster.spec.tolerations**\

        Additional custom tolerations to add to control plane component resources (deployment, service, etc.)
      </td>

      <td>list</td>

      <td>
        ```yaml wrap theme={"system"}
        null
        ```
      </td>
    </tr>

    <tr>
      <td id="slurmCluster--spec--version">
        **slurmCluster.spec.version**\

        Slurm version selector passed through to the SlurmCluster spec when set.
      </td>

      <td>string</td>

      <td>
        ```yaml wrap theme={"system"}
        null
        ```
      </td>
    </tr>

    <tr>
      <td id="slurmConfig">
        **slurmConfig**\

        Slurm cluster configuration overrides (`slurm.conf` and `cgroup.conf`). Most values are managed by the operator defaults and do not need to be set here. Keys you add under `slurmConfig` are passed through to the SlurmCluster CRD as user overrides and take precedence over the operator defaults. Set a key to `""` or `[]` to omit it, including its operator default, from the rendered config. `cgroup.conf` overrides go under the nested `cgroupConfig`. The operator-set defaults are listed below for reference.

        > [accordion] Operator defaults
        >
        > ```yaml theme={"system"}
        > slurmConfig:
        >   AccountingStorageEnforce: qos,limits
        >   AccountingStorageTRES: gres/gpu
        >   AccountingStorageType: accounting_storage/slurmdbd
        >   AuthAltParameters: jwt_key=/etc/jwt/jwt.key
        >   AuthAltTypes: auth/jwt
        >   BatchStartTimeout: "120"
        >   CommunicationParameters: KeepAliveTime=60,keepaliveinterval=10,keepaliveprobes=3
        >   DebugFlags: NO_CONF_HASH
        >   DefMemPerCPU: "4096"
        >   Epilog: /usr/share/sunk/bin/epilog.sh
        >   GresTypes: gpu
        >   InactiveLimit: "0"
        >   JobAcctGatherFrequency: "30"
        >   JobAcctGatherType: jobacct_gather/cgroup
        >   JobCompType: jobcomp/none
        >   KillWait: "30"
        >   MaxNodeCount: "3072"
        >   MessageTimeout: "100"
        >   MinJobAge: "300"
        >   MpiDefault: pmix
        >   ProctrackType: proctrack/cgroup
        >   Prolog: /usr/share/sunk/bin/prolog.sh
        >   PrologFlags: Alloc,Serial
        >   RebootProgram: /usr/share/sunk/bin/reboot.sh
        >   ReturnToService: "2"
        >   SchedulerParameters: nohold_on_prolog_fail,max_rpc_cnt=256
        >   SchedulerType: sched/backfill
        >   SelectType: select/cons_tres
        >   SelectTypeParameters: CR_CPU_MEMORY
        >   SlurmSchedLogFile: /dev/null
        >   SlurmSchedLogLevel: "1"
        >   SlurmUser: slurm
        >   SlurmctldDebug: verbose
        >   SlurmctldLogFile: /dev/null
        >   SlurmctldParameters: conmgr_max_connections=512,conmgr_threads=32,idle_on_node_suspend,node_reg_mem_percent=95,rl_enable,rl_log_freq=30,rl_bucket_size=50,rl_refill_period=1,rl_refill_rate=10
        >   SlurmctldPidFile: /var/run/slurmctld.pid
        >   SlurmctldPort: "6817"
        >   SlurmctldTimeout: "60"
        >   SlurmdDebug: verbose
        >   SlurmdLogFile: /proc/1/fd/1
        >   SlurmdPidFile: /var/run/slurmd.pid
        >   SlurmdPort: "6818"
        >   SlurmdSpoolDir: /var/spool/slurmd
        >   SlurmdTimeout: "60"
        >   StateSaveLocation: /var/spool/slurmctld/save
        >   SUNKJobDashboardURL: https://cks-grafana.coreweave.com/d/slurm-job-metrics/slurm-job-metrics
        >   SUNKNodeDashboardURL: https://cks-grafana.coreweave.com/d/ddbdicm9sw7c5x/node-details
        >   SuspendTime: INFINITE
        >   SwitchType: switch/none
        >   TCPTimeout: "15"
        >   TaskPlugin: task/cgroup,task/affinity
        >   TaskPluginParam: SlurmdSpecOverride
        >   TopologyParam: TopoOptional
        >   TopologyPlugin: topology/tree
        >   TreeWidth: "65533"
        >   UnkillableStepProgram: /usr/share/sunk/bin/unkillable-step.sh
        >   UnkillableStepTimeout: "900"
        >   WaitTime: "0"
        >   cgroupConfig:
        >     CgroupPlugin: cgroup/v2
        >     ConstrainCores: "yes"
        >     ConstrainDevices: "yes"
        >     ConstrainRAMSpace: "yes"
        >     IgnoreSystemd: "yes"
        > ```
      </td>

      <td>object</td>
      <td>See the operator defaults below.</td>
    </tr>

    <tr>
      <td id="slurmConfig--SlurmJobSkipIds">
        **slurmConfig.SlurmJobSkipIds**\

        The controller skips processing this list of Slurm JobIds. Comma separated list without spaces of JobIds to skip. Example: `"2,4,6,8"`
      </td>

      <td>string</td>

      <td>
        ```yaml wrap theme={"system"}
        null
        ```
      </td>
    </tr>

    <tr>
      <td id="slurmConfig--namespaceConfig">
        **slurmConfig.namespaceConfig**\

        Configuration for Slurm's `namespace/linux` plugin, rendered to `namespace.yaml`. **Requires Slurm 25.11 or later.** \
        &#x20;**Enabled by default.** With `CLONE_NEWPID`, every job gets its own PID namespace and an automatically mounted private `/proc`, so jobs sharing a node cannot inspect or signal each other's processes. The plugin also gives each job a private `/tmp` and `/dev/shm`. \
        &#x20;The operator sets `NamespaceType=namespace/linux` and appends `Contain` to `PrologFlags` after user overrides merge; Slurm refuses to start without `Contain`, so deriving it after the merge keeps a user editing `PrologFlags` from bricking the cluster. Changes require a `slurmd` restart to take effect (`scontrol reconfigure` is not enough). \
        &#x20;To opt out, set `enabled: false`.

        > [accordion] Example: click to expand
        >
        > ```yaml theme={"system"}
        > slurmConfig:
        >   namespaceConfig:
        >     enabled: true
        >     defaults:
        >       autoBasePath: true
        >       basePath: /opt/sunk/namespace/%n
        >       cloneNsFlags: ["CLONE_NEWPID"]
        >       dirs: ["/tmp", "/dev/shm"]
        > ```
      </td>

      <td>object</td>

      <td>
        ```yaml wrap theme={"system"}
        enabled with CLONE_NEWPID
        ```
      </td>
    </tr>

    <tr>
      <td id="storage">
        **storage**\

        Shared cluster storage volumes. Adopts the entry shape of the external `slurm-supporting` chart (`name` / `storageClassName` / `size`), so an existing `storage` list can be carried over on upgrade with no edits. Empty by default (opt-in).  For each entry that sets `mountPath`, the chart derives a PVC-backed volume + mount and wires it into **both** the login pods (`common`, `userPods`, `groupPods`) and the compute nodesets. Any volumes/mounts declared directly under `login.{common,userPods,groupPods}.pod` or `compute` are appended to the storage-derived set; on a `name`/`mountPath` collision the directly-declared entry wins.  Whether a PVC is created is controlled solely by `create`: <ul> <li>`name` (string, required) — PVC name; also the pod volume name   and the claim the mount references.</li> <li>`create` (bool, optional, default `false`) — when   `true` the chart creates the PVC; when `false` it assumes   the claim already exists and only references it (bring-your-own / the   orphan-then-adopt upgrade path). `size`/`storageClassName`/   `accessModes` are used only when `create` is true.</li> <li>`mountPath` (string, optional) — when set, the claim is mounted   at this path on login and compute pods; when omitted the entry only manages the   PVC (create or reference) and is not auto-mounted.</li> <li>`size` (string, required when `create`) — requested   storage.</li> <li>`storageClassName` (string, optional) — omitted when empty so   Kubernetes uses the cluster default storage class.</li> <li>`accessModes` (list, optional) — defaults to   `[ReadWriteMany]`, required to share a volume across pods.</li> </ul>  Created PVCs are annotated `helm.sh/resource-policy: keep` and `argocd.argoproj.io/sync-options: Prune=false,Delete=false` so an upgrade or prune never deletes the data. When adopting an existing PVC (`create: false`, or a create=true whose spec ArgoCD applies onto a live volume) the rendered spec must match the existing PVC's immutable fields.  Overriding `storage` replaces the whole list (Helm does not merge lists), so an override must re-list every volume it wants, including its `mountPath`.
      </td>

      <td>list</td>

      <td>
        ```yaml wrap theme={"system"}
        []
        ```
      </td>
    </tr>

    <tr>
      <td id="syncer--config">
        **syncer.config**\

        Configuration for the syncer component.
      </td>

      <td>object</td>

      <td>
        ```yaml wrap theme={"system"}
        {
          "hooksAPI": {},
          "slurm": {},
          "syncer": {}
        }
        ```
      </td>
    </tr>

    <tr>
      <td id="syncer--config--hooksAPI">
        **syncer.config.hooksAPI**\

        Webhooks API configuration

        > [accordion] Operator defaults
        >
        > ```yaml theme={"system"}
        > hooksAPI:
        >   nodeRebootCondition: PhaseState
        >   nodeRebootReason: production-powerreset
        >   safeNodeRebootCondition: PendingPhaseState
        >   safeNodeRebootReason: production-powerreset
        >   waitForPodDeletionInterval: 1s
        >   waitForNodeLockedInterval: 1s
        >   waitForNodeLockedTimeout: 120s
        > ```
      </td>

      <td>object</td>
      <td>See the operator defaults below.</td>
    </tr>

    <tr>
      <td id="syncer--config--slurm">
        **syncer.config.slurm**\

        Slurm client configuration

        > [accordion] Operator defaults
        >
        >         <table>
        >           <tr><th>Key</th><th>Type</th><th>Description</th><th>Default</th></tr>
        >           <tr><td>`poolSize`</td><td>int</td><td>Number of connections to maintain in the connection pool.</td><td>`10`</td></tr>
        >           <tr><td>`usePersistentConnection`</td><td>bool</td><td>Use Slurm's persistent connections for connection reuse.</td><td>`true`</td></tr>
        >         </table>
        >
        > ```yaml theme={"system"}
        > slurm:
        >   poolSize: 10
        >   usePersistentConnection: true
        > ```
      </td>

      <td>object</td>
      <td>See the operator defaults below.</td>
    </tr>

    <tr>
      <td id="syncer--config--syncer">
        **syncer.config.syncer**\

        Syncer-specific configuration. Copy a key from the reference below only when overriding it.

        > [accordion] Operator defaults
        >
        > ```yaml theme={"system"}
        > syncer:
        >   qosInterruptable: qos.coreweave.cloud/interruptable
        >   orphanedPodDelay: 120s
        >   pollInterval: 10s
        >   slurmNodeCleanUp: true
        >   reconfigureRateLimit: 3600s
        >   logLevel: debug
        >   maxConcurrentReconciles: 50
        > ```

        > [accordion] nodesetUpdateJobPreemption — preempt jobs during NodeSet rolling upgrades
        >
        >         <table>
        >           <tr><th>Key</th><th>Type</th><th>Description</th><th>Default</th></tr>
        >           <tr><td>`enabled`</td><td>bool</td><td>Enable job preemption during rolling upgrades. Must be a boolean when present.</td><td>`false`</td></tr>
        >           <tr><td>`method`</td><td>string</td><td>Preemption strategy; required when `enabled` is true. One of `partition` (preempt jobs in partitions matching `partitions`), `qos` (preempt jobs whose QoS matches `qos`), or `time` (preempt jobs whose rolling-delete condition is older than `timeLimit`).</td><td>—</td></tr>
        >           <tr><td>`partitions`</td><td>string</td><td>Comma-separated regexes matching partition names. Required (and only valid) when `method` is `partition`. Must be a string — the operator splits it on commas; a YAML list is rejected by the API server.</td><td>—</td></tr>
        >           <tr><td>`qos`</td><td>string</td><td>Comma-separated regexes matching QoS names. Required (and only valid) when `method` is `qos`. Must be a string — the operator splits it on commas; a YAML list is rejected by the API server.</td><td>—</td></tr>
        >           <tr><td>`timeLimit`</td><td>string</td><td>Duration (e.g. `30m`). Required (and only valid) when `method` is `time`.</td><td>—</td></tr>
        >         </table>
        >
        > ```yaml theme={"system"}
        > syncer:
        >   nodesetUpdateJobPreemption:
        >     enabled: true
        >     method: partition
        >     partitions: "^b200$,^priority-.*$"
        > ```
      </td>

      <td>object</td>
      <td>See the operator defaults below.</td>
    </tr>

    <tr>
      <td id="syncer--image">
        **syncer.image**\

        The image to use for the syncer.
      </td>

      <td>object</td>

      <td>
        ```yaml wrap theme={"system"}
        repository:
        tag:

        ```
      </td>
    </tr>

    <tr>
      <td id="syncer--resources">
        **syncer.resources**\

        Resources for the syncer container.
      </td>

      <td>object</td>
      <td>requests: cpu 200m memory 1Gi; limits: memory 1Gi</td>
    </tr>
  </tbody>
</table>
