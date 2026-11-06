# Run TensorRT-LLM inference with marimo notebooks

Source: https://docs.coreweave.com/products/cks/tutorials/marimo-notebooks/tensorrt

# Run TensorRT-LLM inference with marimo notebooks

> Deploy GPU-accelerated LLM inference using NVIDIA TensorRT-LLM inside interactive marimo notebooks on CKS

[TensorRT-LLM](https://github.com/NVIDIA/TensorRT-LLM) is NVIDIA's open-source library for optimizing and running large language model inference on NVIDIA GPUs. It fuses operations, applies quantization, and compiles models into optimized TensorRT engines, delivering higher throughput and lower latency compared to standard PyTorch inference.

CKS makes it straightforward to run TensorRT-LLM workloads: pull the [official NVIDIA Triton NGC container](https://catalog.ngc.nvidia.com/orgs/nvidia/-/containers/tritonserver/-), add whatever tooling your workflow needs, and deploy to a GPU Node. This tutorial demonstrates that pattern through a marimo notebook example, an interactive notebook with a live model picker and prompt selector, but the same container approach works for any TensorRT-LLM workload. By the end, you have a working notebook environment that can load and serve multiple open-weight models for low-latency inference on a CKS GPU Node.

In this tutorial, you:

1. **Download the TensorRT-LLM example** from the marimo-operator repository.
2. **Deploy to CKS** with a single CLI command or a YAML manifest.
3. **Run inference** against open-weight models including FP8-quantized checkpoints.

> [card] What you'll need
>
> Before you start, you must have:
>
> * A CKS cluster with an NVIDIA GPU Node (24 GB VRAM or greater recommended, 48 GB for larger models).
> * The [marimo operator installed](https://docs.coreweave.com/products/cks/tutorials/marimo-notebooks.md) on your cluster.
> * `kubectl` installed and configured to access your cluster.
> * [`kubectl-marimo`](https://pypi.org/project/kubectl-marimo/) installed (`uv tool install kubectl-marimo`).

> [card] What you'll use
>
> You use these tools and services:
>
> * [**marimo-operator**](https://github.com/marimo-team/marimo-operator): Manages notebook deployments on Kubernetes.
> * [**TensorRT-LLM**](https://github.com/NVIDIA/TensorRT-LLM): NVIDIA's optimized LLM inference library.
> * [**NVIDIA Triton container**](https://catalog.ngc.nvidia.com/orgs/nvidia/-/containers/tritonserver/-): Pre-built NGC image with TensorRT-LLM.
> * [**kubectl-marimo**](https://pypi.org/project/kubectl-marimo/): CLI plugin for running notebooks on Kubernetes.

> [!NOTE]
>
> **Container image**
>
> The example uses a [purpose-built image](https://github.com/marimo-team/marimo-operator/blob/main/examples/tensorrt/Dockerfile) layered on top of `nvcr.io/nvidia/tritonserver:25.01-trtllm-python-py3`. It's published at `ghcr.io/marimo-team/marimo-operator/tensorrt:latest` and rebuilt automatically on every push to main. To adapt it for your own workload, swap the `FROM` image or add your own packages.

## Get the example

The [marimo-operator TensorRT example](https://github.com/marimo-team/marimo-operator/tree/main/examples/tensorrt) includes both a notebook file and a plain YAML manifest. Use whichever fits your workflow. Both options deploy the same workload. Choose Option A for an interactive notebook-first experience, or Option B if you prefer to manage Kubernetes resources declaratively.

### Option A: CLI plugin (interactive)

Download and deploy the notebook in one step. Replace `[NAMESPACE]` with the Kubernetes namespace you want to deploy into:

```bash theme={"system"}
curl -O https://raw.githubusercontent.com/marimo-team/marimo-operator/main/examples/tensorrt/tensorrt.py
kubectl marimo edit tensorrt.py --namespace [NAMESPACE]
```

The plugin reads the Kubernetes config embedded in the notebook's [PEP 723](https://peps.python.org/pep-0723/) header (image, GPU limits, storage size) and generates the manifest for you.

```text theme={"system"}
Waiting for tensorrt to be ready...
Opening http://localhost:2718?access_token=<TOKEN>
Press Ctrl-C to stop port-forward and sync changes
```

### Option B: YAML manifest (declarative)

Apply the manifest directly if you prefer managing resources with `kubectl`:

```bash theme={"system"}
kubectl apply -f https://raw.githubusercontent.com/marimo-team/marimo-operator/main/examples/tensorrt/tensorrt.yaml --namespace [NAMESPACE]
```

Edit the manifest to adjust the `nodeSelector`, storage size, or GPU count before applying.

## Select a model and run inference

The notebook opens with a model picker. The included models all fit comfortably within 48 GB of VRAM:

| Model | VRAM (approx.) | Notes |
| - | - | - |
| [TinyLlama 1.1B](https://huggingface.co/TinyLlama/TinyLlama-1.1B-Chat-v1.0) | \~3 GB | Fastest to load, good for testing |
| [Phi-3.5-mini](https://huggingface.co/microsoft/Phi-3.5-mini-instruct) | \~8 GB | Strong reasoning, 128K context |
| [Mistral 7B](https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.3) | \~14 GB | Solid general-purpose model |
| [Llama-3.1 8B FP8](https://huggingface.co/nvidia/Llama-3.1-8B-Instruct-FP8) | \~8 GB | [FP8-quantized](https://nvidia.github.io/TensorRT-LLM/performance/performance-tuning-guide/fp8-quantization.html) by NVIDIA, \~50% less VRAM than FP16 |
| [Minitron 8B](https://huggingface.co/nvidia/Mistral-NeMo-Minitron-8B-Instruct) | \~16 GB | Mistral-NeMo 12B distilled to 8B |

Select a model, then pick a prompt from the second dropdown. The generation cell is reactive: changing the prompt re-runs inference without reloading the model.

You now have a TensorRT-LLM-optimized model loaded in your CKS-hosted notebook and can iterate on prompts interactively against GPU-accelerated inference.

## Clean up

When you're done, remove the notebook deployment to release the GPU Node and avoid further charges. Press `Ctrl-C` to stop the port-forward, then delete the notebook:

```bash theme={"system"}
kubectl marimo delete tensorrt --namespace [NAMESPACE]
```

If you used the YAML manifest, run:

```bash theme={"system"}
kubectl delete -f tensorrt.yaml --namespace [NAMESPACE]
```

## Additional resources

* [TensorRT-LLM documentation](https://nvidia.github.io/TensorRT-LLM/): Quick start, LLM Python API reference, supported models.
* [FP8 quantization guide](https://nvidia.github.io/TensorRT-LLM/performance/performance-tuning-guide/fp8-quantization.html): How NVIDIA's FP8 calibration works and when to use it.
* [NVIDIA NGC Triton container](https://catalog.ngc.nvidia.com/orgs/nvidia/-/containers/tritonserver/-): The base container image used in this example.
* [marimo-operator TensorRT example](https://github.com/marimo-team/marimo-operator/tree/main/examples/tensorrt): Dockerfile, notebook, YAML manifest, and README.
* [marimo notebooks on CKS](https://docs.coreweave.com/products/cks/tutorials/marimo-notebooks.md): General setup guide for the marimo operator and CLI plugin.
* [NVIDIA blog: Optimizing LLM inference with TensorRT-LLM](https://developer.nvidia.com/blog/optimizing-inference-on-llms-with-tensorrt-llm-now-publicly-available/): Overview of TensorRT-LLM's optimization techniques.
