# Run a GPU Pod with Kata Containers

Source: https://docs.coreweave.com/products/cks/container-runtimes/run-gpu-pod

# Run a GPU Pod with Kata Containers

> Configure a virtualization Node Pool and deploy a GPU Kata Pod with guest metrics

> [!WARNING]
>
> Container runtime selection is in private preview. [Contact Support](https://docs.coreweave.com/support.md) to request access before using a non-default runtime. Backwards compatibility between ncore releases isn't guaranteed. An installed runtime doesn't establish production support.

Use the `cw-kata-nvidia-gpu` RuntimeClass to run a GPU workload inside a QEMU virtual machine (VM) on CoreWeave Kubernetes Service (CKS). This guide deploys a CUDA vector-addition sample with the guest metrics agent required by CKS.

## Prerequisites

Before you begin, confirm that you have the following:

* A CKS cluster with [cluster access configured](https://docs.coreweave.com/products/cks/auth-access/introduction.md) and `kubectl` installed.
* Kubernetes permissions to create Node Pools, create and delete workload Pods, inspect Nodes and RuntimeClasses, list Pods in `cw-kata-system`, and read workload Pod status, events, and logs.
* A Node Pool approved by CoreWeave for GPU Kata testing that meets the [platform requirements in the runtime catalog](https://docs.coreweave.com/products/cks/container-runtimes/reference.md#runtime-catalog).
* CoreWeave enablement of the Kata controllers, the `cw-kata-nvidia-gpu` RuntimeClass, and workload metrics scraping in your cluster.

Confirm that the class exists:

```bash theme={"system"}
kubectl get runtimeclass cw-kata-nvidia-gpu -o yaml
```

If the class is absent, ask CoreWeave to confirm cluster enablement before continuing.

## Configure a Node Pool

Configure a Node Pool for virtualization workloads:

**1. Prepare the Node Pool manifest**

Prepare a new Node Pool manifest following [Create a Node Pool using Kubernetes](https://docs.coreweave.com/products/cks/nodes/create.md#create-a-node-pool-using-kubernetes). Use the instance type approved by CoreWeave for GPU Kata.

**2. Enable virtualization and apply the manifest**

Add `virt: "true"` under `spec.nodeParameters` in that manifest. The following is an excerpt, not a complete Node Pool manifest:

```yaml theme={"system"}
spec:
  nodeParameters:
    virt: "true"
```

This setting initializes the Nodes for virtualization workloads. Save the complete manifest in a file named `gpu-kata-nodepool.yaml` and apply it:

```bash theme={"system"}
kubectl apply -f gpu-kata-nodepool.yaml
```

**3. Check for GPU metrics placeholder Pods**

After the Nodes join the cluster, check for GPU metrics placeholder Pods:

```bash theme={"system"}
kubectl get pods -n cw-kata-system -o wide
```

The Kata metrics operator schedules one `kata-metrics-placeholder-*` Pod per unused GPU. These Pods provide GPU metrics while no workload uses the GPU. Resolve missing or unhealthy placeholder Pods with CoreWeave before deploying the workload.

## Deploy the GPU Pod

Create and apply a Pod manifest that includes the GPU workload and guest metrics agent:

**1. Save the Pod manifest**

Save the following manifest in a file named `gpu-kata-pod.yaml`:

```yaml theme={"system"}
apiVersion: v1
kind: Pod
metadata:
  name: cuda-vectoradd-kata
  namespace: default
  labels:
    kata.coreweave.com/telemetry: "true"
spec:
  runtimeClassName: cw-kata-nvidia-gpu
  restartPolicy: Never
  initContainers:
    - name: cks-metrics-agent
      restartPolicy: Always
      image: images.coreweave.com/cluster-images/cw-cks-metrics-agent-oci/cks-metrics-agent:v1.1.1
      command: ["/bin/sh", "-c"]
      args:
        - |-
          mknod -m 0600 /dev/kmsg c 1 11 2>/dev/null || true
          exec cks-metrics-agent --web.listen-address=:9400
      env:
        - name: CKS_COLLECT_INTERVAL
          value: 15s
        - name: VISIBLE_CDI_DEVICES
          value: nvidia.com/gpu=all
        - name: NVIDIA_DRIVER_CAPABILITIES
          value: all
      ports:
        - name: metrics
          containerPort: 9400
      startupProbe:
        httpGet:
          path: /readyz
          port: metrics
        periodSeconds: 5
        failureThreshold: 12
      livenessProbe:
        httpGet:
          path: /healthz
          port: metrics
        initialDelaySeconds: 15
        periodSeconds: 20
  containers:
    - name: cuda-vectoradd
      image: nvcr.io/nvidia/k8s/cuda-sample:vectoradd-cuda12.5.0-ubuntu22.04
      resources:
        requests:
          cpu: "1000m"
          memory: 10Gi
          hugepages-1Gi: 20Gi
          nvidia.com/gpu: "1"
        limits:
          cpu: "1000m"
          memory: 10Gi
          hugepages-1Gi: 20Gi
          nvidia.com/gpu: "1"
```

The RuntimeClass supplies virtualization Node selection, a matching hypervisor taint toleration, and scheduler memory overhead. If your Node Pool has additional taints, add only the tolerations required for that pool. See [Workload scheduling](https://docs.coreweave.com/products/cks/clusters/scheduling/workload-scheduling.md).

The Pod label `kata.coreweave.com/telemetry: "true"` identifies the workload for GPU metrics scraping. CoreWeave enables the scrape configuration in your preview cluster.

The metrics agent runs as a native sidecar without additional privileges or explicit resource requests. Its startup probe waits for the agent's HTTP server before starting the CUDA container. `VISIBLE_CDI_DEVICES` gives the agent access to the GPU assigned to the workload. Keep this sidecar in GPU Kata workloads so CKS can monitor GPU health. HTTP probe success doesn't verify GPU collection or delivery to CKS monitoring.

The sample requests one GPU, `10Gi` of container memory, and `20Gi` of 1 GiB hugepages. For details about how these values relate, see [GPU Kata resource requirements](https://docs.coreweave.com/products/cks/container-runtimes/reference.md#gpu-kata-resource-requirements).

**2. Apply the Pod manifest**

```bash theme={"system"}
kubectl apply -f gpu-kata-pod.yaml
```

## Verify the workload

Check the sample's status and output, then remove the sample Pod:

**1. Check the Pod's status and events**

```bash theme={"system"}
kubectl get pod cuda-vectoradd-kata -n default
kubectl describe pod cuda-vectoradd-kata -n default
```

**2. Read the CUDA container's logs**

```bash theme={"system"}
kubectl logs cuda-vectoradd-kata -n default -c cuda-vectoradd
```

A successful run includes:

```text theme={"system"}
Test PASSED
Done
```

With `restartPolicy: Never`, the sample can reach a terminal phase. The native sidecar stops after the regular container exits.

**3. Inspect the metrics sidecar's logs**

Inspect the metrics sidecar's logs and work with CoreWeave to confirm that GPU metrics reach CKS monitoring:

```bash theme={"system"}
kubectl logs cuda-vectoradd-kata -n default -c cks-metrics-agent
```

Expected output resembles the following. Timestamps and metric counts can vary:

```text theme={"system"}
{"time":"2026-10-26T16:45:55.561357032Z","level":"INFO","msg":"DCGM collector initialized","collector":"dcgm","gpus":1,"metrics":63,"labels":3}
{"time":"2026-10-26T16:45:55.565333559Z","level":"INFO","msg":"gpu-thermal collector initialized","collector":"gpu-thermal","gpus":1,"gpu_class":"unknown"}
{"time":"2026-10-26T16:45:55.61560785Z","level":"INFO","msg":"NVLinks discovered","collector":"nvlink","count":0,"present":false}
{"time":"2026-10-26T16:45:55.666989657Z","level":"INFO","msg":"GPUs discovered","collector":"nvlink","count":1}
{"time":"2026-10-26T16:45:55.717091688Z","level":"INFO","msg":"starting cks-metrics-agent","collectors":["dcgm","gpu-thermal","nvlink","xid"],"interval":15000000000,"metrics":":9400/metrics"}
{"time":"2026-10-26T16:45:55.717257716Z","level":"INFO","msg":"listening","address":":9400"}
{"time":"2026-10-26T16:45:59.840393561Z","level":"INFO","msg":"shutting down"}
```

In this sample, the agent discovers one GPU and starts its metrics endpoint. The sidecar shuts down after the CUDA container exits. These logs show agent initialization; work with CoreWeave to confirm delivery to CKS monitoring.

**4. Delete the sample Pod**

After verification, delete the sample Pod:

```bash theme={"system"}
kubectl delete pod cuda-vectoradd-kata -n default
```

## Troubleshoot startup

| Symptom | What to check |
| - | - |
| The Pod stays `Pending`. | Confirm that the Node Pool is ready and compatible with the runtime, and that the Nodes have enough GPU, memory, and hugepage capacity. Inspect the Pod events for scheduling failures. |
| `FailedCreatePodSandBox` with `DeadlineExceeded` | Check the hugepage requests and limits. Missing or insufficient hugepages can prevent QEMU from starting and appear as a timeout. |
| The CUDA container doesn't start. | Inspect the `cks-metrics-agent` sidecar and its startup probe in the Pod events. |

For unresolved failures, provide CoreWeave with the Pod events and container logs.
