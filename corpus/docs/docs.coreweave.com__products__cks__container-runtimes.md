# Container runtimes on CKS

Source: https://docs.coreweave.com/products/cks/container-runtimes

# Container runtimes on CKS

> Understand runtime isolation, platform compatibility, and limitations for CKS workloads

> [!WARNING]
>
> Container runtime selection is in private preview. [Contact Support](https://docs.coreweave.com/support.md) to request access before using a non-default runtime. Backwards compatibility between ncore releases isn't guaranteed. An installed runtime doesn't establish production support.

Container runtimes determine how CoreWeave Kubernetes Service (CKS) executes a Pod's containers and isolates them from the host. Runtime choice matters when workloads execute code supplied by users, customers, or AI agents. Choose a runtime based on the trust you place in that code, the isolation boundary you require, and whether the workload needs GPU access.

## Runtime isolation

CKS Node images include conventional container runtimes and additional runtimes based on gVisor and Kata Containers. A Kubernetes `RuntimeClass` maps a Pod to an installed runtime handler. A Node label advertising a handler doesn't establish that a `RuntimeClass` with the same name exists.

The `runc` and `nvidia` handlers run conventional containers that share the Node's kernel. Additional runtimes provide different execution boundaries:

| Runtime family | Execution boundary | GPU access |
| - | - | - |
| Kata Containers | Containers run inside a virtual machine (VM) with a separate guest kernel. | The GPU class uses QEMU and Virtual Function I/O (VFIO) to pass a GPU into the VM. CPU classes don't provide this GPU passthrough configuration. |
| gVisor (deprecated) | A userspace kernel, called the Sentry, handles application system calls. | The GPU-enabled configuration uses `nvproxy` to forward supported NVIDIA driver operations to the host. The CPU-only class prevents GPU access. |

## Platform compatibility

The [runtime catalog](https://docs.coreweave.com/products/cks/container-runtimes/reference.md#runtime-catalog) lists the platform families, architectures, and cgroups requirements for each handler.

Check the RuntimeClasses available in your cluster and confirm the Node image with CoreWeave before selecting hardware. Platform compatibility doesn't establish production support.

## GPU metrics collection

GPU Kata requires metrics collection inside the guest VM so CKS can monitor the health of passed-through GPUs. The monitoring setup has two parts: a metrics agent in each GPU workload Pod and placeholder Pods for unused GPUs.

### Metrics agent in each workload Pod

VFIO passthrough binds the GPU to the host's VFIO driver, so the host's NVIDIA exporters can't see it. Only the guest can collect its metrics. Without them, CKS loses the GPU health data it needs and can place the Node in triage.

Include `cks-metrics-agent` in every GPU Kata Pod as a native sidecar: an init container with `restartPolicy: Always`, which runs for the workload's lifetime. The [complete GPU Pod example](https://docs.coreweave.com/products/cks/container-runtimes/run-gpu-pod.md#deploy-the-gpu-pod) shows this configuration.

The example includes the following settings:

| Setting | Purpose |
| - | - |
| Pod label `kata.coreweave.com/telemetry: "true"` | Identifies the workload Pod for GPU metrics scraping. |
| `VISIBLE_CDI_DEVICES=nvidia.com/gpu=all` | Gives the agent access to all GPUs passed into the Pod's guest. It doesn't grant access to every GPU on the host. |
| `NVIDIA_DRIVER_CAPABILITIES=all` | Sets the NVIDIA driver capabilities available to the metrics agent in the example. |
| `CKS_COLLECT_INTERVAL=15s` | Configures the example's metrics collection interval. |
| `--web.listen-address=:9400` | Exposes the agent's HTTP server on port `9400`. |
| Startup probe at `/readyz` | Delays the application container's startup until the agent's HTTP server responds. |
| Liveness probe at `/healthz` | Checks that the agent's HTTP server responds. It doesn't verify GPU collection. |

Use the full sidecar configuration from the example, including its image, command, environment variables, and probes. Adding only a metrics port or a readiness probe doesn't replace the agent.

### Metrics for unused GPUs

The Kata metrics operator schedules `kata-metrics-placeholder-*` Pods in the `cw-kata-system` namespace, with one placeholder Pod per unused GPU. These Pods keep GPU metrics available to CKS when no application workload is using the GPU.

Before deploying a GPU workload, check that the placeholder Pods are running as described in [Configure a Node Pool](https://docs.coreweave.com/products/cks/container-runtimes/run-gpu-pod.md#configure-a-node-pool). When deploying the workload, check the metrics sidecar's status and logs as well as the application's status. CoreWeave must enable workload metrics scraping for your preview cluster and confirm that GPU metrics reach CKS monitoring; successful HTTP probes alone don't establish this.

## Limitations

* GPU Kata supports one passed-through GPU per Pod, without InfiniBand or NVLink. Multiple-GPU passthrough isn't guaranteed.
* GPU Kata Pods must reserve hugepages and run the guest metrics agent. Missing GPU metrics can cause CKS to triage the Node.
* Runtime availability depends on the Node image and cluster configuration. A listed handler might not be available in your cluster.
