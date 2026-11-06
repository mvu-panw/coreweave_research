# Measure MFU and job performance

Source: https://docs.coreweave.com/products/sunk/optimize_workloads/measuring-mfu-and-job-performance

# Measure MFU and job performance

> Compute model FLOPs utilization, interpret DCGM GPU metrics, and tell a tuning problem from an infrastructure problem

[SUNK Standard](https://docs.coreweave.com/products/sunk.md)

[SUNK Self-Service](https://docs.coreweave.com/products/sunk/about-self-service-sunk.md)

A common question during training is "Is my GPU utilization good?" The GPU utilization number reported by most tools doesn't provide a clear answer. This page explains what the common NVIDIA Data Center GPU Manager (DCGM) metrics actually measure, how to compute model FLOPs utilization (MFU) yourself, and how to tell whether a low number is a workload-tuning problem or an infrastructure problem.

This page is for SUNK users measuring and tuning training throughput on CoreWeave. The methods here are workload-side. They don't depend on any specific dashboard, and the DCGM field names are standard NVIDIA metric names.

## What DCGM GPU utilization actually measures

`DCGM_FI_DEV_GPU_UTIL` reports the fraction of time during which at least one kernel is running on the GPU. It's an occupancy signal: it indicates that the GPU is busy, not how much of its compute capacity the workload uses. A GPU running a tiny kernel can report high `DCGM_FI_DEV_GPU_UTIL` while doing little useful math.

`DCGM_FI_PROF_PIPE_TENSOR_ACTIVE` reports the fraction of time the Tensor pipe is active. For Tensor-core-bound training, this is much closer to "how hard the math units are working."

This is why high `DCGM_FI_DEV_GPU_UTIL` with low `DCGM_FI_PROF_PIPE_TENSOR_ACTIVE` is normal for some workloads, especially those that are memory-bound, communication-bound, or dominated by non-Tensor kernels. A high occupancy number alone doesn't mean your training is efficient.

The [Slurm Job Metrics dashboard](https://docs.coreweave.com/observability/managed-grafana/sunk/slurm-job-metrics.md) surfaces these signals per job. For Tensor-core-bound training, its **Tensor Core Utilization Running Jobs** panel acts as an upper bound for MFU, because your model's mathematical efficiency can't exceed the fraction of time the tensor cores are active. Its Job Efficiency value is an idle-time estimate, not an MFU metric.

## Compute MFU yourself

Model FLOPs utilization (MFU) is the ratio of the useful FLOPs your model performs to the theoretical peak FLOPs the hardware could perform over the same time. It's the most relevant single number for training efficiency.

Compute it as:

```text theme={"system"}
MFU = (model FLOPs per step * steps per second) / (peak FLOPs of the GPU * number of GPUs)
```

To compute MFU, follow these steps:

1. Estimate the model FLOPs per step for your architecture and batch size. See [Estimate model FLOPs per step](#estimate-model-flops-per-step).
2. Measure steps per second from your training loop.
3. Identify your GPU model on its instance page under [About GPU instances](https://docs.coreweave.com/platform/instances/gpu-instances.md), then use that GPU's published theoretical peak FLOPs from NVIDIA's datasheet, matching your training precision (for example, BF16 or FP8). Use the dense figure, not the one marked "with sparsity". Published MFU numbers divide by the dense peak, and the sparsity figure is double it.

Hardware FLOPs utilization (HFU) is the related measure that also counts recomputation, such as activation checkpointing, so HFU is at or above MFU for the same run. For the definitions of both measures, see [Reducing Activation Recomputation in Large Transformer Models](https://arxiv.org/abs/2205.05198).

### Estimate model FLOPs per step

For a dense transformer, count the forward and backward passes as 6 FLOPs per parameter per token. Model FLOPs per step is then approximately 6 times the parameter count times the number of tokens in the step (global batch size times sequence length). This shortcut comes from the [PaLM paper](https://arxiv.org/abs/2204.02311) and ignores the attention term, which grows with sequence length.

When the sequence length is a meaningful fraction of the hidden size, use the full per-iteration formula from Appendix A of [Reducing Activation Recomputation in Large Transformer Models](https://arxiv.org/abs/2205.05198):

```text theme={"system"}
model FLOPs per step = 72 * B * L * s * h^2 * (1 + s / (6 * h) + V / (12 * h * L))
```

Here `B` is the number of sequences per step (global batch size), `L` is the number of transformer layers, `s` is the sequence length, `h` is the hidden size, and `V` is the vocabulary size. For mixture-of-experts models, count only the parameters that are active for each token, and use the same active count in every comparison. If your training framework logs achieved TFLOP/s or MFU itself, prefer that number over a hand calculation. If your architecture doesn't fit either formula, ask your CoreWeave solutions architect for help deriving the count.

## Expected ranges by workload class

MFU varies widely by model class, parallelism strategy, and sequence length. Use the following as broad, general-knowledge orientation, not as targets or guarantees:

* Dense transformer pretraining at scale commonly lands in a moderate-to-high MFU range when well tuned.
* Mixture-of-experts (MoE) MFU varies with expert granularity. Fine-grained MoE models land well below dense models of comparable size, because routing and all-to-all communication take time that isn't matrix math, while coarse MoE models with a few large experts can match dense MFU.
* Inference MFU is generally lower than training MFU, because inference is often memory-bandwidth-bound rather than compute-bound.

Published large-scale pretraining runs give a sense of scale. These are the authors' own reported figures, on their hardware, not CoreWeave targets:

| Run | Hardware | Reported MFU | Source |
| - | - | - | - |
| GPT-3 175B | V100 | 21.3% | [PaLM paper, Table 3](https://arxiv.org/abs/2204.02311) |
| Megatron-Turing NLG 530B | 2,240 A100 | 30.2% | [PaLM paper, Table 3](https://arxiv.org/abs/2204.02311) |
| PaLM 540B | 6,144 TPU v4 | 46.2% | [PaLM paper, Table 3](https://arxiv.org/abs/2204.02311) |
| Llama 3 405B | 8,192 to 16,384 H100 | 38% to 43% (BF16) | [Llama 3 paper, Table 4](https://arxiv.org/abs/2407.21783) |

Well-tuned dense pretraining at scale lands near 40% in these reports. Numbers for your own model class come from your team's earlier runs or from your CoreWeave solutions architect.

If your MFU is far below what's typical for your workload class, treat it as a tuning signal and investigate the workload before suspecting the platform.

## Tuning problem or infrastructure problem

Use the following signals to decide where the bottleneck is.

It's most likely a workload-tuning problem in either of the following cases:

* `DCGM_FI_DEV_GPU_UTIL` is high but `DCGM_FI_PROF_PIPE_TENSOR_ACTIVE` and MFU are low. The GPU is busy with the wrong work.
* MFU is uniformly low across healthy nodes. The same inefficiency follows the workload everywhere.

It points to data starvation when GPU utilization is low and storage read throughput is low at the same time. See [Data loading and avoiding GPU starvation](#data-loading-and-avoiding-gpu-starvation).

It points to a single slow rank when one rank consistently lags the others. Use [GPU Straggler Detection](https://docs.coreweave.com/products/sunk/discover_sunk/straggler-detection.md) to identify the rank and node. Straggler Detection must be enabled on your cluster first, and the NCCL your job loads must meet its version requirement. See the [Straggler Detection prerequisites](https://docs.coreweave.com/products/sunk/optimize_workloads/enable-gpu-straggler-detection.md#prerequisites).

It may be an infrastructure problem worth a ticket when MFU dropped suddenly without a workload change, and the drop tracks specific nodes rather than the workload. See [Diagnose gradual step-time slowdown](#diagnose-gradual-step-time-slowdown).

## Data loading and avoiding GPU starvation

When training data doesn't reach the GPUs fast enough, the GPUs sit idle waiting for the next batch. This often surfaces as low GPU utilization or an NCCL timeout that looks like a fabric problem but is a storage and data-loading problem. A uniform metric drop across unrelated jobs on different nodes is a strong starvation signal, because a hardware fault wouldn't affect many independent nodes at once.

Instrument the training loop so you can see starvation directly rather than inferring it:

```python theme={"system"}
# Log how long each step waits for its batch. A large time_to_get_batch relative
# to step time indicates the dataloader is the bottleneck, not the GPU or fabric.
import time

start = time.perf_counter()
batch = next(data_iter)
time_to_get_batch = time.perf_counter() - start
# log time_to_get_batch alongside total step time
```

If `time_to_get_batch` is a large fraction of step time, the dataloader is starving the GPUs. Correlate it with storage read throughput: if reads dropped when GPUs went idle, the data path is the cause.

The following patterns keep GPUs fed:

* **Shard the dataset** so each rank reads a distinct set of files. When many ranks read the same files at the same time, the storage backend becomes a contention point. Sharding spreads the reads out.
* **Tune dataloader parallelism.** Use enough dataloader workers and prefetching so batch preparation overlaps with GPU compute. On Grace CPU instances, dataloader workers can crash with `Illegal instruction` when a numpy or BLAS build ships x86\_64 code. Any native library in the worker can also carry a 4 KiB page-size assumption that breaks on Grace even when built for `aarch64`. See [Run jobs on Grace CPU instances](https://docs.coreweave.com/products/sunk/run_workloads/run-jobs-on-grace-cpu.md).
* **Pre-stage data** into a faster path before training begins. If your training data is in CoreWeave AI Object Storage and your cluster uses LOTA, warm the cache before the run. See [Pre-stage the LOTA cache](https://docs.coreweave.com/products/storage/object-storage/improving-performance/prestage-cache.md).

## Diagnose gradual step-time slowdown

When stable training step time gradually gets slower, over hours within one run or days across runs, the shape of the slowdown points at the cause.

| Pattern | Most likely cause | Where to look |
| - | - | - |
| Step time climbs gradually over hours within one run | Software: a dataloader leak, memory-mapped file accumulation, or a change in how much data the job requests | Per-node memory growth. NFS read throughput against read latency over the run: falling throughput with flat latency means the job is asking for less data, a software cause |
| Step time creeps up over days of node uptime, across restarts | Accumulated driver or kernel state, for example, progressive CUDA sync latency on GB200 nodes running the 580 driver. A node reboot resets it | Node uptime correlation. Compare a freshly rebooted node |
| Uniform slowdown across several jobs on different nodes at once | Data starvation: a shared storage backend is the bottleneck | Storage read throughput, queue depth on the shared backend |
| Fine at small scale, slow only at large scale | Distribution, topology, or dataloader contention at scale | Per-rank step time spread, collective behavior at scale |

Capture step time per rank, not only the average. An average hides a single slow rank: if one rank's step time is climbing while the others are flat, the problem is local to that rank or its node. If all ranks climb together, the cause is shared. If the slowdown started after a change to the container image or framework version, bisect by rolling back to the prior image on a test run. If the slowdown disappears, the regression is in the new image.

## What this is not

Keep the following points in mind:

* High `DCGM_FI_DEV_GPU_UTIL` isn't proof of efficient training. It measures occupancy, not useful compute.
* Low MFU isn't by itself a hardware fault. For most workloads it's a tuning problem.
* "Is my MFU good?" is usually a workload question, not a platform question. Compare against your workload class first.

## When to open a support ticket

Open a ticket when MFU dropped without a workload or driver change and the drop is tied to specific nodes that fail an NCCL test or show hardware-class XID codes. Alongside the details every ticket needs, listed in [Support ticket templates](https://docs.coreweave.com/support/ticket-templates.md), include your MFU calculation and the affected node names.

## Related pages

* [Introduction to GPU Straggler Detection](https://docs.coreweave.com/products/sunk/discover_sunk/straggler-detection.md): find the slow rank.
* [What do NCCL errors mean?](https://docs.coreweave.com/support/sunk/articles/what-do-nccl-errors-mean): the NCCL error reference, including why a collective timeout is usually a storage or dataloader problem.
* [Enable GPU Straggler Detection](https://docs.coreweave.com/products/sunk/optimize_workloads/enable-gpu-straggler-detection.md): cluster and job setup.
* [Pre-stage the LOTA cache](https://docs.coreweave.com/products/storage/object-storage/improving-performance/prestage-cache.md): warm CoreWeave AI Object Storage data with LOTA.
* [About GPU instances](https://docs.coreweave.com/platform/instances/gpu-instances.md): identify your GPU model per instance type.
* [Glossary](https://docs.coreweave.com/glossary.md): CoreWeave terms used on this page.
