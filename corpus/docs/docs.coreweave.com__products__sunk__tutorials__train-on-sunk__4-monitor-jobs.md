# 4. Monitor jobs with Grafana

Source: https://docs.coreweave.com/products/sunk/tutorials/train-on-sunk/4-monitor-jobs

# 4. Monitor jobs with Grafana

> Monitor Slurm training jobs using CoreWeave's Grafana dashboards for GPU utilization and performance metrics

[SUNK Standard](https://docs.coreweave.com/products/sunk.md)

[SUNK Self-Service](https://docs.coreweave.com/products/sunk/about-self-service-sunk.md)

This is the fourth page of the **Train on SUNK** tutorial series. After submitting your training job in the previous step, you need a way to observe how it runs on the cluster. This page shows you how to use CoreWeave's Grafana dashboards to monitor Slurm training jobs, inspect GPU utilization, and identify performance bottlenecks so you can confirm your job is progressing as expected. These dashboards also show whether a job is still making progress when its `.out` file looks empty or stale because of [output buffering](https://docs.coreweave.com/products/sunk/tutorials/train-on-sunk/2-submit-simple-job.md#view-job-output).

## Monitor Slurm jobs with CoreWeave Grafana

The following sections describe how to open Grafana and locate the dashboard used to inspect Slurm job activity.

To open CoreWeave Grafana, first log in to the [CoreWeave Cloud Console](https://console.coreweave.com/).

From the Console, either navigate to **Grafana** from the left-hand navigation or access it directly at `https://cks-grafana.coreweave.com`. From there, select **Dashboards**, then select the **[Slurm Job Metrics](https://cks-grafana.coreweave.com/d/slurm-job-metrics/slurm-job-metrics)** dashboard.

### Slurm Job Metrics dashboard

![Slurm Job Metrics Grafana dashboard](https://mintcdn.com/coreweave-dbfa0e8d/lW-m410I_gVGZZCw/products/sunk/_media/grafana-dash-slurm-job-metrics.png?fit=max\&auto=format\&n=lW-m410I_gVGZZCw\&q=85\&s=32cae601bb61afd111485846e5eadcca)

This dashboard displays metrics used for debugging and analyzing the performance of specific jobs within your cluster. It provides detailed information about the nodes running a given job, including alerts and node details.

To display details about a specific job, including information about the nodes the job ran on, select the cluster and job of interest from the top of the dashboard. For example, the following image displays details on job `48`. The **Job State Timeline**, at the lower left of the **Job Info** section, shows that the job ran for over one hour.

![Slurm Job Metrics Grafana dashboard with job 48 details displayed](https://mintcdn.com/coreweave-dbfa0e8d/lW-m410I_gVGZZCw/products/sunk/_media/grafana-dash-slurm-job-metrics-annotated.png?fit=max\&auto=format\&n=lW-m410I_gVGZZCw\&q=85\&s=d616a3276bb42951516818414d782ded)

The dashboard also captures the states of the job (`PENDING`, `RUNNING`, `COMPLETED`, and so on) chronologically. This information can be useful for debugging and performance analysis.

On the right, you can see two key metrics:

* **Job Efficiency** captures an estimate of GPU usage during the job's run.
* **Current FP8 FLOPS** shows the compute rate as the job runs. It is common to see a regular pattern of peaks and valleys as the job runs. Typically, areas with less compute usage appear when the job loads data or saves checkpoints.

Below **Job Info**, the **Nodes (Range)** table lists the nodes that ran the job. To open the Node Details dashboard for a node, select its **Node ID**. Select **Node Name** to open the Pod Inspector dashboard, or **slurmd log** to open the node's `slurmd` logs.

![Nodes (Range) table and GPU Metrics section of the Slurm Job Metrics dashboard](https://mintcdn.com/coreweave-dbfa0e8d/lW-m410I_gVGZZCw/products/sunk/_media/grafana-dash-slurm-job-metrics-nodes.png?fit=max\&auto=format\&n=lW-m410I_gVGZZCw\&q=85\&s=864ebe46e93b43e7bfb917d6f38dd3e0)

### GPU metrics

Further down the dashboard, GPU-specific panels help you confirm that the hardware runs as expected during the run.

The included GPU metrics display information on the job's run. At its most abstracted level, the presence of red indicates that the given aspect of the GPU is working hard, whereas the presence of green signifies that the given part of the GPU is working less hard.

This example runs a 124M cell GPT2 test model on two L40 nodes, without InfiniBand.

![GPU Metrics panels on the Slurm Job Metrics dashboard](https://mintcdn.com/coreweave-dbfa0e8d/lW-m410I_gVGZZCw/products/sunk/_media/grafana-dash-slurm-job-metrics-gpu.png?fit=max\&auto=format\&n=lW-m410I_gVGZZCw\&q=85\&s=45481fe47e77416bd65a069d983b9383)

Different codes and data stress different parts of the GPU. A quick glance at the graphs is a way to check if the job runs correctly.

At a glance, you can see that:

* **GPU Temperatures Running Jobs** shifts from a green average to an orange average while the job runs. This is a clear indication that the GPUs are busy.
* **GPU Core Utilization Running Jobs** is high, while **GPU Mem Copy Utilization Running Jobs** is lower, an expected outcome for a small model.

Even further down on this same dashboard, **VRAM Usage** shows the job uses about 175 GB of GPU memory, and **GPUs Temperature** hovers around 68°C, both indicators that the job is progressing well. You also see the **GPUs Power Usage** levels.

![VRAM Usage, GPUs Temperature, and GPUs Power Usage panels on the Slurm Job Metrics dashboard](https://mintcdn.com/coreweave-dbfa0e8d/lW-m410I_gVGZZCw/products/sunk/_media/grafana-dash-slurm-job-metrics-vram.png?fit=max\&auto=format\&n=lW-m410I_gVGZZCw\&q=85\&s=2c803523810bbdd447839a2faec09695)

### Filesystem metrics

Storage performance can affect training throughput, so the dashboard also surfaces filesystem activity for the job.

Even further down the dashboard is information on the filesystem. Two metrics of importance in the **Filesystem** section are the **NFS Average Response/Request** and **NFS Total Read/Write** rate.

* The **NFS Average** graphs indicate how well the filesystem performs. A slowdown or spike indicates that the storage is slowing down, and that the job may perform better with faster or different storage, such as [CoreWeave AI Object Storage](https://docs.coreweave.com/products/storage/object-storage.md).
* The **NFS Total Read / Write Rate** demonstrates the total `read` and `write` operations on the filesystem. When a job first begins, it is typical to see a large `read` spike as the job reads in the model and data. While the job runs, a regular `write` spike is typical. This indicates when the job writes out checkpoints.

### NCCL metrics

The **NCCL Metrics** row reports how the GPUs in your job communicate with each other through the NVIDIA Collective Communications Library (NCCL). Scroll past **Node Resources** to reach it. A job that spends most of its time waiting on collective operations still looks busy in the GPU panels. This row is where a communication bottleneck becomes visible.

These panels populate only when [GPU Straggler Detection](https://docs.coreweave.com/products/sunk/discover_sunk/straggler-detection.md) runs on the cluster. If the row is empty, confirm the plugin is enabled and loaded. The job from the previous step runs outside a container, so its batch script also needs `export NCCL_PROFILER_PLUGIN=/usr/lib/libnccl-profiler-gpusd.so`. For instructions, see [Enable GPU Straggler Detection](https://docs.coreweave.com/products/sunk/optimize_workloads/enable-gpu-straggler-detection.md). The panels sample at one-minute intervals. Jobs that run for less than about two minutes also produce empty or sparse panels.

**NCCL BusBW** and **NCCL Latency** each appear six times, once per process-group size: 2, 4, 8, 16, 32+, and 512+ GPUs. Training frameworks create a separate process group for each parallelism dimension. The 32+ and 512+ panels include every group at or above that size. For example, a job that uses tensor parallelism across 8 GPUs and data parallelism across 512 would populate the 8-GPU, 32+, and 512+ panels, and the 2, 4, and 16 panels would read "This job does not contain NCCL groups of this size". BusBW is measured in GB/s and latency in microseconds. Each series is one collective, such as `AllReduce` or `AllGather`, on one communicator, averaged across the ranks in that process group. Watch for a series that drops or climbs while the others hold steady, then use the tables below to find the rank behind it.

**NCCL Message Size** graphs the average payload per collective, in bytes. Read the bandwidth panels against it, because small messages are latency-bound and never reach the bandwidth that large messages do.

Two tables at the bottom of the row name the specific GPU to look at:

* **GPU Straggler** identifies the rank that fell behind the rest of the job in collective operations, along with the start and end of the interval, the Node, and the `slurmd` Pod. The detection isolates the single furthest-behind rank, so each detected interval is one row, and a real job rarely shows more than one straggler at once.
* **Slow NCCL Operations** lists ranks whose algorithmic bandwidth (AlgoBW) dropped well below that rank's own average over the previous 24 hours, and names the **NCCL Function** that slowed down.

In both tables, the **Node** and **Slurmd Pod** values are links. To open the Node Details or Pod Inspector dashboard for that hardware, select the value. The following example comes from an earlier build of the dashboard. It shows more stragglers at once than a real job typically has, and an **NCCL Function** column that the current table doesn't include.

![GPU Straggler table listing rank, node, and pod columns with drill-down links](https://mintcdn.com/coreweave-dbfa0e8d/lW-m410I_gVGZZCw/products/sunk/_media/gpusd_stragglers.png?fit=max\&auto=format\&n=lW-m410I_gVGZZCw\&q=85\&s=fc5019fd48226e1a6b09c69730ef0e15)

You don't have to scroll down to the NCCL row to notice a problem. When CoreWeave flags a straggler, a red annotation appears on the **Job State Timeline** and **Current FP8 FLOPS** panels at the top of the dashboard. This aligns a dip in compute with its cause in the same view. Yellow annotations mark slow collectives on the **NCCL BusBW** panels. Both annotations are toggles at the top of the dashboard and are enabled by default.

![Straggler Detection annotations overlaid on the job state row of the Slurm Job Metrics dashboard](https://mintcdn.com/coreweave-dbfa0e8d/lW-m410I_gVGZZCw/products/sunk/_media/gpusd_annotations.png?fit=max\&auto=format\&n=lW-m410I_gVGZZCw\&q=85\&s=fa41d548812718d423d9b454885971ce)

> [!TIP]
>
> For more information about the metrics displayed in this dashboard, see [Slurm Job Metrics](https://docs.coreweave.com/observability/managed-grafana/sunk/slurm-job-metrics.md).

With these dashboards, you now have visibility into how your training job uses GPU, memory, storage, and interconnect resources on the cluster, and you can use that information to validate runs or investigate performance issues in future jobs.
