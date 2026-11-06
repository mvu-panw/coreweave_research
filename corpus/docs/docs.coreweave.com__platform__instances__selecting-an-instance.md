# Select an instance: key considerations for LLMs

Source: https://docs.coreweave.com/platform/instances/selecting-an-instance

# Select an instance: key considerations for LLMs

> Learn about the key considerations for selecting the right instance for your LLM workload

The primary technical constraint for running any large language model (LLM) is the available GPU memory. For a model to operate efficiently, all of its components, including its parameters, the data being processed, and intermediate calculation states, must fit into the memory of one or more GPUs. Understanding how these components consume memory is crucial for selecting the right hardware for your task, whether it's training, fine-tuning, or inference.

## Model parameters (weights)

At its core, an LLM consists of billions of numerical values, known as parameters or weights. These parameters are the learned knowledge of the model. The total memory required to store them is a direct function of the number of parameters and the numerical precision used.

## Precision and quantization

Precision refers to the data type used to store the model's parameters. Using lower precision reduces the memory footprint and can increase computation speed on supported hardware.

* **FP16/BF16 (half precision):** The standard for model training and fine-tuning. It provides a good balance between numerical accuracy and memory usage.
* **Quantization (FP8, INT8, FP4, and INT4):** This technique, primarily used for inference, converts the model's FP16/BF16 weights into lower-precision formats. Integer formats (INT8, INT4) map weights to 8-bit or 4-bit integers, while floating-point formats (FP8, FP4) retain an exponent and mantissa, which typically preserves accuracy better at the same memory footprint. FP8 is hardware-accelerated on NVIDIA Hopper and newer GPUs, and FP4 (NVFP4) on Blackwell and newer. Quantization compresses the model, letting you run a larger model on the same hardware or the same model on less expensive hardware. The trade-off is a minor, often imperceptible, reduction in accuracy, which is generally acceptable for production inference workloads.

Use the following formulas to estimate the GPU memory required to load the model's weights:

* **For FP16/BF16:** Model size (in billions) × 2 GB.
* **For FP8 or INT8:** Model size (in billions) × 1 GB.
* **For FP4 or INT4:** Model size (in billions) × 0.5 GB.

These estimates cover weights only. Total memory at runtime also includes the KV cache, activations, and framework overhead, so plan for additional headroom. Sub-byte formats also store per-block scaling factors that add a small amount (roughly 5 percent) to the weight footprint.

## The impact of the KV cache (for inference)

During inference, the key-value (KV) cache consumes a sizable portion of GPU memory. To generate new text, an LLM must pay attention to the preceding tokens. The KV cache stores these intermediate attention calculations so they don't have to be recomputed for every new word generated. While this speeds up inference, the cache's memory footprint is dynamic and grows with the complexity of the request. Its size scales linearly with both the sequence length (the size of the input prompt plus the generated text) and the batch size (the number of concurrent requests the system processes). Managing the KV cache is a critical aspect of optimizing for high-throughput inference with long context windows.

## GPU memory for training

Optimizer states and gradients make training or fine-tuning a model far more memory-intensive than inference. In addition to the model weights and data batches, the GPU must also store:

* **Optimizer states:** Most modern optimizers, like Adam or AdamW, maintain momentum and variance states for each parameter to stabilize and accelerate training. This can consume twice as much memory as the model's parameters themselves.
* **Gradients:** The calculated directions for updating each model weight. The memory required is typically equal to the size of the model parameters in FP16.

As a result, fine-tuning a model can require 3x to 4x more GPU memory than running it for inference.

## The role of NVLink and InfiniBand

Running models larger than a single GPU's memory requires high-speed interconnects to link GPUs together, a practice known as model parallelism. The performance of this approach depends on a two-level fabric:

* **The GPU fabric (NVLink):** A high-speed, direct link between GPUs. In standard servers like our B200 or H100 instances, NVLink connects the 8 GPUs within the server chassis. Our Grace Blackwell NVL72 instances (`gb200-4x`) extend this design by using an NVLink Switch fabric to span the memory domain across all 72 GPUs in an entire rack, turning the rack into a single GPU.
* **The system fabric (InfiniBand):** The high-performance network that scales your workload further. For standard servers, InfiniBand connects multiple Nodes together. For Grace Blackwell NVL72 systems, its role expands to connecting multiple racks, which lets you build large AI supercomputers from these rack-scale units.

## Instance comparison

Vera Rubin NVL72 instances offer up to 5x inference throughput and 3.5x training performance over GB200 NVL72. For detailed specifications, see the [Vera Rubin instance page](https://docs.coreweave.com/platform/instances/gpu/verarubin-4x-e.md).

The following table summarizes the available GPU instances, their total memory, and the model sizes each configuration can support, to help you match an instance to your workload.

| GPU | System Config | Total GPU Memory | Max Inference Model Size (FP8)<sup>\*</sup> | Max Training Model Size (BF16) | Examples of Models That Fit |
| - | - | - | - | - | - |
| [Vera Rubin NVL72](https://docs.coreweave.com/platform/instances/gpu/verarubin-4x-e.md) | NVL72 (72 GPUs) | 20.7 TB | \~20.7 Trillion | \~1.3 Trillion | **Inference:** Next-generation, multi-trillion parameter models at high fidelity **Training:** Foundation models in the multi-trillion parameter range |
| [GB300](https://docs.coreweave.com/platform/instances/gpu/gb300-4x.md) | NVL72 (72 GPUs) | 20.1 TB | \~20.1 Trillion | \~1.3 Trillion | **Inference:** Next-generation, multi-trillion parameter models at high fidelity **Training:** Foundation models in the multi-trillion parameter range |
| [GB200](https://docs.coreweave.com/platform/instances/gpu/gb200-4x.md) | NVL72 (72 GPUs) | 13.4 TB | \~13.4 Trillion | \~840 Billion | **Inference:** GPT-5, Claude Opus, Gemini Ultra, other large proprietary models **Training:** GLM-5.2 max with 744B parameters, Nemotron 3 Ultra |
| [B300](https://docs.coreweave.com/platform/instances/gpu/b300-8x.md) | 8-GPU system (NVLink) | 2.16 TB | \~2.16 Trillion | \~135 Billion | **Inference:** DeepSeek V4 Pro, MiMo-V2.5-Pro, Kimi K2.7 Code **Training:** Mistral Medium 3.5, Qwen 3.5 122B A10B |
| [B200](https://docs.coreweave.com/platform/instances/gpu/b200-8x.md) | 8-GPU system (NVLink) | 1.44 TB | \~1.44 Trillion | \~90 Billion | **Inference:** MiMo-V2.5-Pro, Kimi K2.7 Code, GLM-5.2 (max) **Training:** Qwen 3 Next 80B A3B, K2 Think V2 |
| [H200](https://docs.coreweave.com/platform/instances/gpu/gd-8xh200ib-i128.md) | 8-GPU system (NVLink) | 1.13 TB | \~1.13 Trillion | \~70 Billion | **Inference:** MiMo-V2.5-Pro, Kimi K2.7 Code, GLM-5.2 (max) **Training:** Qwen 3.6 27B and 35B A3B, Gemma 4 31B and 26B A4B |
| [H100](https://docs.coreweave.com/platform/instances/gpu/gd-8xh100ib-i128.md) | 8-GPU system (NVLink) | 640 GB | \~640 Billion | \~40 Billion | **Inference:** Nemotron 3 Ultra, MiniMax-M3, DeepSeek V4 Flash **Training:** Qwen 3.6 27B and 35B A3B, Gemma 4 31B and 26B A4B, fine-tuning large models |
| [RTX PRO 6000 Blackwell Server Edition](https://docs.coreweave.com/platform/instances/gpu/rtxp6000-8x.md) | 8-GPU system (No NVLink) | 96 GB per GPU | \~86 Billion | \~6 Billion | **Inference:** Qwen 3.6 27B and 35B A3B, Gemma 4 31B and 26B A4B **Training:** Models up to \~6B from scratch, fine-tuning larger models |
| [L40S](https://docs.coreweave.com/platform/instances/gpu/gd-8xl40s-i128.md) | 8-GPU system (No NVLink) | 48 GB per GPU | \~43 Billion | \~3 Billion | **Inference:** Qwen2 32B, LLaVA 34B **Training:** Small custom models (\~2B), efficient fine-tuning |
| [L40](https://docs.coreweave.com/platform/instances/gpu/gd-8xl40-i128.md) | 8-GPU system (No NVLink) | 48 GB per GPU | \~43 Billion | \~3 Billion | **Inference:** Qwen2 32B, LLaVA 34B **Training:** Small custom models (\~2B), fine-tuning |
| [GH200](https://docs.coreweave.com/platform/instances/gpu/gd-1xgh200.md) | 1 GPU | 576 GB | \~576 Billion | \~6 Billion | **Inference:** Llama 3.1 405B, Nemotron-4 340B **Training:** Small custom models (\~6B) |
| [A100](https://docs.coreweave.com/platform/instances/gpu/gd-8xa100-i128.md) | 8-GPU system (NVLink) | 640 GB | \~640 Billion | \~40 Billion | **Inference:** Llama 3.1 405B, Falcon-180B **Training:** Qwen2 32B, fine-tuning large models |

<sup>\*</sup>Figures represent theoretical estimates for a single model. A typical production scenario often involves running multiple smaller models concurrently.

> [!NOTE]
>
> Learn more about our [GPU instances](https://docs.coreweave.com/platform/instances/gpu-instances.md), [CPU instances](https://docs.coreweave.com/platform/instances/cpu-instances.md), and [NVL72-powered instances](https://docs.coreweave.com/platform/instances/nvl72.md).
