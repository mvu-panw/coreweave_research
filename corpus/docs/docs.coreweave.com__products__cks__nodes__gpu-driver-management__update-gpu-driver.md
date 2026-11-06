# Select GPU driver versions in CKS Node Pools

Source: https://docs.coreweave.com/products/cks/nodes/gpu-driver-management/update-gpu-driver

# Select GPU driver versions in CKS Node Pools

> Select, pin, and safely roll out GPU driver versions in CKS Node Pool manifests (preview feature)

This page explains how to select, update, and pin NVIDIA GPU driver versions on CoreWeave Kubernetes Service (CKS) Node Pools, and how to target specific driver versions from your workloads. It also covers driver and CUDA compatibility and how to test and roll out a driver change safely. Use this guidance when you need a workload to run against a known driver version or when you want to control which driver Nodes receive during configuration updates.

## Limitations

GPU driver management in CKS has the following limitations:

* **Manifest configuration**: Set GPU driver versions in the Node Pool manifest using `kubectl`, GitOps, or the [Cloud Console manifest editor](https://docs.coreweave.com/products/cks/nodes/manage.md#cloud-console).
* **Limited version updates**: You can only select major version updates. When minor updates are available, the `Manual` and default `OnSpecUpdate` strategies leave the configuration pending in [`status.pendingNodeConfiguration`](https://docs.coreweave.com/products/cks/reference/node-pool#pending-node-configuration). With `Always`, CKS stages it automatically. See [Manage Node Pool configuration](https://docs.coreweave.com/products/cks/nodes/manage.md#manage-node-pool-configuration).
* **Release channels are not supported**: The `latest` and `stable` release channels are not supported in Node Pools.

[Contact CoreWeave support](https://docs.coreweave.com/support.md) if you have questions about GPU driver management.

## Create a new Node Pool with a specific driver version

Driver versions are configured in [the Node Pool manifest](https://docs.coreweave.com/products/cks/nodes/create.md#create-a-node-pool-using-kubernetes). To select a driver version, add the `gpu` section to your Node Pool manifest's `spec` section, specifying the desired major version without dots.

> [!WARNING]
>
> Don't set the `image` field when configuring GPU drivers. The `gpu` and `image` fields are mutually exclusive. If you set both, CKS ignores `gpu` and `image` takes precedence.

For example, for an H100 Node Pool, specify the driver version as `580`:

```yaml highlight={9-10} theme={"system"}
apiVersion: compute.coreweave.com/v1alpha1
kind: NodePool
metadata:
  name: example-nodepool
spec:
  computeClass: default
  instanceType: gd-8xh100ib-i128
  targetNodes: 1
  gpu:
    version: "580"  # Specify driver version by major version
```

If no driver is specified, the Node Pool automatically uses the latest available driver.

## Update the driver version on an existing Node Pool

This section shows how to change the driver version on a Node Pool that already specifies one. If a driver is currently specified on an existing Node Pool, you can update it to a new major version by modifying the existing Node Pool manifest.

```yaml title="Original Node Pool manifest" highlight={12} theme={"system"}
apiVersion: compute.coreweave.com/v1alpha1
kind: NodePool
metadata:
  name: test-nodepool
spec:
  computeClass: default
  instanceType: gd-8xh100ib-i128
  nodeConfigurationUpdateStrategy:
    type: OnSpecUpdate
  targetNodes: 1
  gpu:
    version: "580"
```

```yaml title="Updated Node Pool manifest" highlight={12} theme={"system"}
apiVersion: compute.coreweave.com/v1alpha1
kind: NodePool
metadata:
  name: test-nodepool
spec:
  computeClass: default
  instanceType: gd-8xh100ib-i128
  nodeConfigurationUpdateStrategy:
    type: OnSpecUpdate
  targetNodes: 1
  gpu:
    version: "595"
```

### Apply GPU driver updates

With the default node configuration update strategy `OnSpecUpdate`, updating the driver version automatically stages the new configuration onto the Node Pool. You can then [queue a reconfigure reboot](https://docs.coreweave.com/products/cks/nodes/apply-updates.md) for existing Nodes to apply the change. For more information about configuration management, see [Manage Node Pool configuration](https://docs.coreweave.com/products/cks/nodes/manage.md#manage-node-pool-configuration).

## Pin an exact driver version

The `gpu.version` field selects only the major version. CKS selects the specific minor within that major. To pin an exact driver minor (for example, for reproducibility or a known-good version), pin the `image` field instead. The ncore image bundles a specific driver, so pinning the image pins the driver.

> [!WARNING]
>
> Set the `image` field only when directed by CoreWeave Support. Remove the `gpu` field when you pin the image.

To pin a minor version, set `image.name` in the Node Pool manifest to the specific ncore image that carries the driver you need. To identify the correct image name for your instance type and target driver version, [contact Support](https://docs.coreweave.com/support.md).

## Driver and container compatibility

The driver version on the host and the CUDA toolkit version inside your container are separate. A newer driver generally runs an older CUDA image. In the other direction, a container built with a newer CUDA toolkit runs on an older host driver only within NVIDIA's compatibility ranges, such as minor version compatibility within the same major CUDA release. Outside those ranges, the host driver must be at least as new as the CUDA toolkit your image needs.

Follow these guidelines to manage driver and container compatibility:

* Confirm compatibility against the [NVIDIA CUDA compatibility documentation](https://docs.nvidia.com/deploy/cuda-compatibility/).
* Pin both the driver (per Node Pool) and the container image (per workload) when you need reproducibility. Pinning only one leaves a moving part.
* Don't install or replace the GPU driver from inside your container or with a custom DaemonSet. CKS manages the host driver, and overriding it leads to conflicts.
* If a workload reports a driver or CUDA mismatch at startup, the most common cause is a container requiring a newer driver than the host provides. Move the workload to a Node Pool with a newer driver, or rebuild the container against a toolkit compatible with the host driver.

## Test and roll out a driver change safely

Changing a GPU driver under a running job can break it. Test a new driver before applying it broadly, and roll the change out in stages so you catch problems on a small set of Nodes first.

### Test on a dedicated test Node Pool

Validate a new driver against your workload before applying it broadly. The safest pattern is a small dedicated test Node Pool:

1. Create a small Node Pool of the same instance type with the new driver version set in `spec.gpu.version`. See [Create a Node Pool](https://docs.coreweave.com/products/cks/nodes/create.md).
2. Schedule a representative GPU workload onto it using a `nodeSelector` or affinity that targets the test Node Pool.
3. Validate correctness and performance against your baseline. Confirm the driver loads (see [Verify the driver version](#verify-the-driver-version)), the workload starts, and throughput matches expectations.

### Canary, then roll out the rest

After the test Node Pool passes, update the driver in the production Node Pool manifest. Stage the configuration according to your [update strategy](https://docs.coreweave.com/products/cks/nodes/manage.md#stage-node-pool-configurations). Staging applies to the whole Node Pool and changes the configuration used by new and replacement Nodes. Existing Nodes adopt it after a reconfigure reboot. To isolate the new configuration, continue to use a separate test Node Pool.

To queue reconfigure reboots for selected existing Nodes, verify their image, and roll out in small batches, follow [Test a new image on a canary subset](https://docs.coreweave.com/products/cks/nodes/manage.md#test-a-new-image-on-a-canary-subset). For each GPU canary and batch, run an NCCL test and a short training run, and compare step time with your baseline. Before you resume production runs across the full pool, re-validate NCCL and step time against the canary measurements.

Keep one driver version per Node Pool, and don't schedule a single job across Node Pools with different drivers. Mixed driver versions within a job cause inconsistencies that are hard to diagnose at scale.

## Known driver behaviors to plan for

The following behaviors can appear with certain driver versions:

* **Progressive CUDA sync latency over Node uptime.** On some driver versions, certain instances show step time gradually increasing over days of continuous Node uptime. Rebooting the Node restores normal latency, so schedule periodic reboots between runs until you move to a driver that resolves the behavior.
* **Checkpoint segfaults at large scale.** If you see these segfaults, call `torch.cuda.synchronize()` before checkpointing and consider asynchronous checkpoint patterns.

## Target driver versions using Node labels and selectors

Once your Node Pool is configured with a driver version, you can identify and target Nodes by their driver version from within Kubernetes. Driver version information is exposed on Nodes through Kubernetes labels. You can use these labels to get information on current driver versions and to target specific driver versions in your workloads.

```bash theme={"system"}
# Check the current driver version label on nodes
kubectl get nodes --show-labels | grep driver-version
```

Node labels are in the format `gpu.coreweave.cloud/driver-version=[DRIVER-VERSION]`, where `[DRIVER-VERSION]` is the full driver version string. For example, a Node with the label `gpu.coreweave.cloud/driver-version=580.105.08-0ubuntu1` is running driver version `580.105.08-0ubuntu1`.

> [!NOTE]
>
> The `gpu.coreweave.cloud/driver-version` label is always applied to Nodes, even if no driver version is specified in the Node Pool manifest.

## Target specific driver versions in workloads

The `gpu.coreweave.cloud/driver-version` label lets you target Nodes with exact driver version matches.

For more information about scheduling workloads on Nodes with specific driver versions, see [Workload scheduling on CKS](https://docs.coreweave.com/products/cks/clusters/scheduling/workload-scheduling.md).

### Schedule workloads on Nodes with specific driver versions

For workloads that require a specific driver version, use an exact match with the `nodeSelector` field:

```yaml theme={"system"}
apiVersion: v1
kind: Pod
metadata:
  name: gpu-workload
spec:
  containers:
  - name: gpu-container
    image: nvidia/cuda:12.8.0-base-ubuntu24.04
    command: ["nvidia-smi"]
    resources:
      limits:
        nvidia.com/gpu: 1
  nodeSelector:
    gpu.coreweave.cloud/driver-version: "580.105.08-0ubuntu1"
```

### Troubleshoot scheduling issues

If Pods fail to schedule due to driver version constraints, check the available driver versions in your cluster. Replace `[POD-NAME]` with the name of your Pod.

```bash theme={"system"}
# Check available driver versions
kubectl get nodes --show-labels | grep driver-version

# Check Pod events for scheduling failures
kubectl describe pod [POD-NAME] | grep -A 10 Events:
```

Common scheduling issues include:

* No Nodes available with the exact driver version specified.
* Nodes with the required driver version are unavailable due to resource constraints.
* Driver version constraints conflict with other scheduling requirements.

## Troubleshooting

This section covers common error conditions and how to verify the active driver version on your Nodes.

### Common error conditions

If you encounter issues with driver configuration, check the Node Pool status for error conditions:

```yaml theme={"system"}
Status:
  Conditions:
    Last Transition Time: 2025-06-30T19:25:16Z
    Message: unable to create configuration for NodePool
    Reason: InternalError
    Status: False
    Type: Validated
```

> [!NOTE]
>
> **Node Pool errors**
>
> For more information about Node Pool events and possible error conditions, see [Node Pool events](https://docs.coreweave.com/products/cks/reference/node-pool.md#condition-validated).

### Verify the driver version

To verify your Node Pool configuration and driver status, use any of the following methods.

Describe the Node Pool:

Replace `[NODE-POOL-NAME]` with the name of your Node Pool.

```bash theme={"system"}
# Check Node Pool status
kubectl describe nodepool [NODE-POOL-NAME]
```

Check the Node labels for driver version:

```bash theme={"system"}
# Check node labels for driver version
kubectl get nodes --show-labels | grep driver-version
```

Or, check the GPU driver information on the Nodes by running `nvidia-smi` on a Pod running on the Node. Replace `[POD-NAME]` with the name of your Pod.

```bash theme={"system"}
# Check GPU driver information on nodes
kubectl exec -it [POD-NAME] -- nvidia-smi
```
