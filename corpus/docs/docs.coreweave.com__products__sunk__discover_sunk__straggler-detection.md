# Introduction to GPU Straggler Detection

Source: https://docs.coreweave.com/products/sunk/discover_sunk/straggler-detection

# Introduction to GPU Straggler Detection

> Learn about GPU Straggler Detection, part of CoreWeave Mission Control™

[SUNK Standard](https://docs.coreweave.com/products/sunk.md)

[SUNK Self-Service](https://docs.coreweave.com/products/sunk/about-self-service-sunk.md)

GPU Straggler Detection is part of CoreWeave Mission Control. This page explains the problem the feature solves for distributed training teams and shows what it looks like in use. If you run multi-GPU training jobs on CoreWeave, read this page to understand how Straggler Detection helps you find underperforming GPUs. It also helps you recover lost training throughput and reduce time spent debugging silent slowdowns.

In large-scale model training, thousands of GPUs communicate with each other. When even a single GPU falls behind, whether because of a software glitch, a networking issue, or hardware degradation, the entire distributed training job slows down. These GPU "stragglers" don't crash the job outright, but they stretch iteration time. This makes detection much harder, and existing logs and telemetry from a training run can't solve the problem. The consequences are reduced training throughput, researcher time lost to silent slowdowns, and wasted compute.

For most research teams, finding a straggler requires extensive manual debugging. Engineers review available logs, compare node performance by hand, and repeatedly resubmit jobs to isolate the GPU that causes the slowdown. Often, teams don't have the necessary data and can't find the straggling GPU. Because distributed training depends on complex GPU-to-GPU communication, even experienced teams struggle to pinpoint the root cause quickly.

Straggler Detection identifies the affected GPU without manual investigation. It applies CoreWeave's proprietary detection algorithms to fine-grained NCCL (NVIDIA Collective Communications Library) telemetry to isolate the specific GPU and node that fall out of sync with the rest of the job. When it flags a straggler, the Slurm Job Metrics dashboard marks the interval on the **Job State Timeline** and names the rank, Node, and Pod in the **GPU Straggler** table, with links to the Node and Pod dashboards. From there, you can [drain the Slurm node](https://docs.coreweave.com/products/sunk/manage_sunk/drain-and-undrain-nodes.md) and requeue the job on healthy hardware.

Alongside Straggler Detection, you gain access to NCCL-level Prometheus metrics that improve observability. These metrics make it easier to understand GPU communication patterns, diagnose training bottlenecks, and troubleshoot other multi-node NCCL workloads. The plugin hooks into NCCL's profiler interface and needs at least 2 CPUs per task. Together, these capabilities help you monitor GPU communication in your clusters, identify wasted compute, and reduce time spent iterating.

## Enable Straggler Detection

On SUNK Self-Service clusters and SUNK Standard v8.0.0 and later, the Straggler Detection plugin is installed and active by default. On SUNK Standard v7.4.x, you turn it on with a cluster configuration update. On any version, jobs that run outside a container set one environment variable so NCCL loads the plugin. Once enabled, CoreWeave Grafana dashboards surface NCCL telemetry for distributed jobs running on Slurm. You can update your cluster configuration to disable NCCL telemetry collection and Straggler Detection at any time.

For instructions, see [Enable GPU Straggler Detection](https://docs.coreweave.com/products/sunk/optimize_workloads/enable-gpu-straggler-detection.md).

## Straggler Detection in action

The following examples show how Straggler Detection surfaces information during a live training job, so you know what to expect before you enable it on your own clusters.

When you run distributed training on CoreWeave, you gain real-time visibility into GPU communication behavior through a set of NCCL performance metrics and purpose-built Grafana dashboards. The [Slurm Job Metrics dashboard](https://docs.coreweave.com/observability/managed-grafana/sunk/slurm-job-metrics.md) surfaces these signals, including NCCL collective latency, bus bandwidth (BusBW), and message sizes, and uses algorithmic bandwidth (AlgoBW) to flag slow collectives. CoreWeave collects these metrics continuously from live jobs.

The dashboards are designed for fast diagnosis and help you answer questions such as:

* Is my job slowing down because of GPU-to-GPU communication issues?
* Which GPU or node is underperforming?
* Is NVLink bandwidth performing as expected?

To simplify troubleshooting, the dashboards include visual annotations that overlay Straggler Detection signals on the **Job State Timeline** and **Current FP8 FLOPS** panels at the top of the dashboard. This gives you an immediate cue that something is wrong, and you can scroll down to the NCCL metrics and straggler tables for the underlying detail.

![Slurm Job Metrics dashboard with GPU Straggler Detection annotations overlaid on the job state row](https://mintcdn.com/coreweave-dbfa0e8d/lW-m410I_gVGZZCw/products/sunk/_media/gpusd_annotations.png?fit=max\&auto=format\&n=lW-m410I_gVGZZCw\&q=85\&s=fa41d548812718d423d9b454885971ce)

Straggler Detection annotations overlaid on the job state timeline in the Slurm Job Metrics dashboard. The colored bars mark intervals where CoreWeave flagged a straggler, so you can quickly spot a problem before drilling into rank-level detail.

### Locate a slow GPU in SUNK

When you run distributed training on CoreWeave using SUNK, you can correlate the timestamp of a detected straggler with your training logs and W\&B job monitoring. This lets you match symptoms in your training code with rank-level NCCL telemetry.

The **GPU Straggler** table identifies the exact GPU rank and node that fall behind. Each row links to detailed Node and Pod dashboards so you can continue investigating the health of the underlying resources. This reduces "job feels slow" debugging to pinpointing a specific GPU and node within seconds.

![GPU Straggler table with rank, node, and pod columns and drill-down links](https://mintcdn.com/coreweave-dbfa0e8d/lW-m410I_gVGZZCw/products/sunk/_media/gpusd_stragglers.png?fit=max\&auto=format\&n=lW-m410I_gVGZZCw\&q=85\&s=fc5019fd48226e1a6b09c69730ef0e15)

The GPU Straggler table from the Slurm Job Metrics dashboard, listing each rank flagged as a straggler with links to Node and Pod detail dashboards. The screenshot comes from an earlier build, so it shows more stragglers at once than a real job produces, and an NCCL Function column that the current table doesn't include. In a real job, you typically see a single straggler at a time.

### Debug distributed training issues

When you investigate reduced MFU or distributed-configuration inefficiencies in otherwise healthy jobs, NCCL telemetry breaks communication down to the individual collective and communicator, which helps you find the root cause.

Dashboards present bandwidth and latency by collective and communicator, split into a separate panel for each process-group size (for example, tensor parallel, pipeline parallel, and large data parallel groups). Each series averages across the ranks in its group. This helps you identify:

* Collectives running noticeably slower in specific groups.
* Communicators whose `AllReduce`, `AllGather`, or `Broadcast` latency stays consistently above their peers in the same process-group size.
* Imbalances between small and large parallel groups.

To attribute a slow collective to a specific rank, use the **GPU Straggler** and **Slow NCCL Operations** tables further down the dashboard. The time-series panels show you that a group is slow. The tables name the GPU and Node responsible.

Previously, capturing bus bandwidth and collective latency required stopping the training run to execute a separate profiler such as `nccl-tests`, which left expensive GPUs idle. With Straggler Detection, the same panels populate continuously from the live job, so you can diagnose bottlenecks without restarting workloads or paying the cost of idle GPUs.

![NCCL bus bandwidth panel from the Slurm Job Metrics dashboard, with one series per collective and communicator](https://mintcdn.com/coreweave-dbfa0e8d/lW-m410I_gVGZZCw/products/sunk/_media/gpusd_busbw.png?fit=max\&auto=format\&n=lW-m410I_gVGZZCw\&q=85\&s=71a810077bbeaaf31188873f39fc4cec)

NCCL bus bandwidth (BusBW) for the collectives running in 2-GPU process groups during a live job. Each series is one collective on one communicator, named in the legend by collective and communicator hash. A series that sits well below its peers points to a communication-bound bottleneck in that group.

![NCCL collective latency panel from the Slurm Job Metrics dashboard, with one series per collective and communicator](https://mintcdn.com/coreweave-dbfa0e8d/lW-m410I_gVGZZCw/products/sunk/_media/gpusd_latency.png?fit=max\&auto=format\&n=lW-m410I_gVGZZCw\&q=85\&s=f9d500266520913124b125d3d75dfc3b)

NCCL collective latency for the same process groups, with the slowest collectives sorted to the top of the legend. A series that stays consistently higher than the others is a strong straggler candidate. Use the GPU Straggler table to find the rank behind it.

## Next steps

* [Enable GPU Straggler Detection](https://docs.coreweave.com/products/sunk/optimize_workloads/enable-gpu-straggler-detection.md) to check the plugin's status, turn it on or off, or verify that it loads in your jobs.
* [Slurm Job Metrics dashboard](https://docs.coreweave.com/observability/managed-grafana/sunk/slurm-job-metrics.md) for a panel-by-panel description of the **NCCL Metrics** row.
