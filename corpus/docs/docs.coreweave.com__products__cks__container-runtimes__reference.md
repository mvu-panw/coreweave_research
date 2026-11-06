# Container runtime reference for ncore images

Source: https://docs.coreweave.com/products/cks/container-runtimes/reference

# Container runtime reference for ncore images

> Look up installed runtime handlers, RuntimeClass mappings, and GPU Kata resource requirements

> [!WARNING]
>
> Container runtime selection is in private preview. [Contact Support](https://docs.coreweave.com/support.md) to request access before using a non-default runtime. Backwards compatibility between ncore releases isn't guaranteed. An installed runtime doesn't establish production support.

The ncore image is the Node operating system image used by CoreWeave Kubernetes Service (CKS). These images include runtime handlers that execute containers. Kubernetes `RuntimeClass` objects expose configured handlers to Pods. The runtime catalog describes installed handlers, platform compatibility, and behavior. A handler's presence on a Node doesn't mean that a RuntimeClass with the same name exists. Availability depends on the Node image and cluster configuration.

## Runtime catalog

The following catalog describes installed handlers and their platform compatibility, which doesn't establish customer support. A Node advertises each available handler with a label named `node.coreweave.cloud/container-runtime.[HANDLER]` set to `"true"`, where `[HANDLER]` is the handler name. These labels describe availability on that Node, not every ncore image or platform.

| Installed handler | Implementation | Platform compatibility and constraints |
| - | - | - |
| `runc` | Conventional containers sharing the host kernel. | Availability on a Node doesn't establish compatibility on other platforms. |
| `nvidia` | Conventional NVIDIA container runtime integration sharing the host kernel. | Confirm the GPU and Node image configuration with CoreWeave. |
| `gvisor`, `cw-gvisor-cpu`, `cw-gvisor-gpu` | Deprecated. Do not use these handlers or their associated RuntimeClasses, including `cw-gvisor`. | Not applicable |
| `cw-kata-nvidia-gpu` | Kata Containers with QEMU and Virtual Function I/O (VFIO) GPU passthrough. | B40 / RTX PRO 6000 PCIe, `RTXP6000-8X*` only; cgroups v2. One GPU per Pod; no InfiniBand or NVLink. H100 NVLink, H200 NVLink, B200 NVLink, B300 PCIe, B300 NVLink, GB, and NVL72 are outside this compatibility. |
| `kata-nvidia-gpu-cw` | Equivalent legacy handler for `cw-kata-nvidia-gpu`. | Same GPU Kata constraints as `cw-kata-nvidia-gpu`. |
| `cw-kata-qemu` | ncore-distributed Kata with QEMU and the upstream Kata CPU configuration. | amd64 and arm64 images that include the handler; cgroups v2. |
| `cw-kata-qemu-kvm` | The QEMU CPU class with a CoreWeave-built guest kernel for nested virtualization. | Requires cgroups v2. |

## RuntimeClass selection

A Pod selects the Kubernetes name of a RuntimeClass, not a Node label or containerd handler directly. The RuntimeClass's `handler` field determines which installed handler runs the Pod.

List the RuntimeClasses configured in your cluster:

```bash theme={"system"}
kubectl get runtimeclass
```

The following mappings are defined by the CKS runtime controllers. Their presence in your cluster depends on cluster enablement:

| RuntimeClass name | Handler | Selection details |
| - | - | - |
| `cw-kata-nvidia-gpu` | `cw-kata-nvidia-gpu` or legacy `kata-nvidia-gpu-cw` | Selects virtualization Nodes. The handler depends on the cluster's existing RuntimeClass configuration. |
| `cw-kata-qemu` | `cw-kata-qemu` | Selects Nodes with the matching runtime capability label. |
| `cw-kata-qemu-kvm` | `cw-kata-qemu-kvm` | Selects Nodes with the matching runtime capability label. |

An installed handler such as `runc` or `nvidia` doesn't establish that a same-named RuntimeClass exists. Inspect your cluster's RuntimeClasses before choosing a value for `spec.runtimeClassName`.

To select a class, set `spec.runtimeClassName` on a Pod. For example, the following excerpt selects the GPU Kata class:

```yaml theme={"system"}
spec:
  runtimeClassName: cw-kata-nvidia-gpu
```

Inspect a class before use. Replace `[RUNTIME-CLASS]` with its Kubernetes name:

```bash theme={"system"}
kubectl get runtimeclass "[RUNTIME-CLASS]" -o yaml
```

| RuntimeClass field | Meaning |
| - | - |
| `metadata.name` | The value a Pod uses in `runtimeClassName`. |
| `handler` | The containerd handler used to execute the Pod. It can differ from the class name. |
| `scheduling.nodeSelector` | Node labels required by the runtime. |
| `scheduling.tolerations` | Tolerations added to Pods that select the class. |
| `overhead.podFixed` | Additional resources charged to the Pod for scheduling. |

CPU Kata classes use runtime capability labels such as `node.coreweave.cloud/container-runtime.cw-kata-qemu: "true"`.

The GPU Kata class selects virtualization Nodes. New installations use the `cw-kata-nvidia-gpu` handler and require its capability label. Existing classes can retain the equivalent legacy handler `kata-nvidia-gpu-cw`. In both cases, Pods select `runtimeClassName: cw-kata-nvidia-gpu`.

## GPU Kata resource requirements

The GPU Kata configuration uses separate values for container memory, virtual machine (VM) memory, hugepage allocation, and scheduler overhead.

| Setting | Purpose |
| - | - |
| Container `memory` request and limit | Input to the guest VM's memory sizing. Use values aligned to 1 GiB. |
| Guest `default_memory` | An `8192Mi` baseline added to container memory limits for VM sizing in the documented GPU configuration. |
| Container `hugepages-1Gi` request and limit | Reserves Node hugepages and permits QEMU to allocate guest RAM through the host cgroup. Set request equal to limit, with enough capacity for the whole VM. |
| RuntimeClass memory overhead | The GPU class adds `5Gi` for scheduler accounting. This is separate from the guest's memory baseline. |
| `nvidia.com/gpu` request and limit | Requests the GPU passed through to the VM. The documented configuration supports one GPU. |

The [GPU Kata example](https://docs.coreweave.com/products/cks/container-runtimes/run-gpu-pod.md#deploy-the-gpu-pod) uses `10Gi` of workload container memory and `20Gi` of hugepages. In the documented configuration, with no memory resources specified for the metrics sidecar or other injected containers, VM sizing is `8Gi + 10Gi = 18Gi`, within the hugepage reservation. Include native sidecar memory limits and any memory added during admission when sizing other Pods. A larger hugepage request doesn't enlarge the VM.

> [!WARNING]
>
> QEMU requires hugepages for guest RAM. Missing or insufficient hugepage requests can prevent the sandbox from booting and produce a `FailedCreatePodSandBox` timeout. Confirm resource sizing for your Node image with CoreWeave before changing the example.

The host hugepage reservation doesn't create guest-side hugepages for the application. Guest-side hugepages require a separate `emptyDir` volume with `medium: HugePages`.

GPU passthrough removes the assigned GPU from host GPU exporters. Run `cks-metrics-agent` inside every GPU Kata Pod to supply GPU metrics to CKS. See the [complete Pod manifest](https://docs.coreweave.com/products/cks/container-runtimes/run-gpu-pod.md#deploy-the-gpu-pod).
