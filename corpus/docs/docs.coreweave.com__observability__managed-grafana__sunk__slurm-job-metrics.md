# Slurm Job Metrics

Source: https://docs.coreweave.com/observability/managed-grafana/sunk/slurm-job-metrics

# Slurm Job Metrics

> View detailed metrics about a Slurm job with Grafana

> [!NOTE]
>
> For instructions about accessing CoreWeave Grafana dashboards, see [Access and use CoreWeave Grafana dashboards](https://docs.coreweave.com/observability/managed-grafana/access.md).

The **Slurm Job Metrics** dashboard displays detailed information about the performance and hardware utilization of a selected Slurm job. Use this page to understand which panels the dashboard provides, how to filter the data it shows, and how to interpret the metrics when investigating job performance.

To open the dashboard, go to the [Slurm Job Metrics dashboard](https://cks-grafana.coreweave.com/d/slurm-job-metrics/slurm-job-metrics).

You can use this dashboard to:

* Monitor the GPU and CPU utilization of a given Slurm job.
* Track the rate of filesystem operations related to the Slurm job.
* View Node conditions and alerts that may impact the performance of the Slurm job.
* Inspect NVIDIA Collective Communications Library (NCCL) bandwidth and latency per collective, and identify GPU ranks that fall behind the rest of the job.

The following sections describe the filters available at the top of the dashboard and the panels grouped under each section.

## Filters and parameters

Use these filters at the top of the page to choose the data you want to view:

| Field | Value |
| - | - |
| **Data Source** | The Prometheus data source selector. |
| **Logs Source** | The Loki logs source selector. |
| **Org** | The organization that owns the cluster. |
| **Cluster** | The specific Kubernetes cluster in the organization to view. |
| **Namespace** | The Kubernetes namespace where the Slurm cluster is located. |
| **Slurm Cluster** | The Slurm cluster containing the job to view. |
| **Job Name** | The name of the Slurm job to view. Select "All" to view all the Slurm jobs in the Slurm Cluster. |
| **Job ID** | The Slurm Job ID to view. Select "All" to view all the Slurm jobs in the Slurm Cluster. |
| **Node Conditions** | Toggled on by default. Click to disable. |
| **Pending Node Alerts** | Toggled on by default. Click to disable. |
| **Firing Node Alerts** | Toggled off by default. Click to enable. |
| **InfiniBand Fabric Flaps** | Toggled off by default. Click to enable. |
| **GPU Straggler** | Toggled on by default. Click to disable. Overlays detected stragglers as red markers on the **Job State Timeline** and **Current FP8 FLOPS** panels. |
| **Slow NCCL Operations** | Toggled on by default. Click to disable. Overlays slow collective operations as yellow markers on the **NCCL BusBW** panels. |

The dashboard also includes buttons with links to the **Slurm Cluster** dashboard and `slurmctld` logs.

Set the time range and refresh rate parameters at the top-right of the page. The default time range is 5 minutes, and the default refresh rate is 1 minute.

## Panel descriptions

The following sections describe each group of panels on the dashboard, starting with **Job Info** and continuing through **GPU Metrics**, **Filesystem**, **Node Resources**, and **NCCL Metrics**.

### Job Info

The **Job Info** section displays identifying information about the selected Slurm job, including:

| Panel | Displays |
| - | - |
| **Job Id** | The Slurm job ID. |
| **Name** | The name of the Slurm job. |
| **Last State** | Displays the most recently reported [state of the Slurm job](https://docs.coreweave.com/observability/managed-grafana.md). |
| **User** | The user who created the Slurm job. |
| **Account** | The user account running the Slurm job. |
| **Nodes** | The number of nodes allocated to the Slurm job. |
| **Partition** | The partition where the selected job is running. |
| **Job State Timeline** | A chart that shows the [Slurm job's states over time](https://docs.coreweave.com/observability/managed-grafana.md). |
| **Uptime** | The Slurm job uptime in seconds. |
| **Active GPUs** | The number of GPUs allocated to the Slurm job that are currently running. |
| **Job Efficiency** | Indicates how active the GPUs were while working on the selected job. This value is estimated based on idle time, defined as a node with at least 1 GPU under 50% utilization. The estimate excludes restarts and checkpointing. This is not a model FLOPs utilization (MFU) metric. |
| **Current FP8 FLOPS** | Graphs the Compute rate over the job run. The graph typically displays peaks and valleys in a regular pattern. Points with lower Compute values often correspond with loading data or saving checkpoints. This number assumes FP8 training. |
| **Node conditions** | Lists nodes that have been assigned a condition, along with timestamps indicating when the condition was noticed and addressed. |
| **Alerts** | Displays all alerts with a severity level higher than **Informational**, over a 10-minute interval. Alerts may have a `PENDING` or `FIRING` state. |
| **Nodes (Range)** | Lists all nodes with their state and uptime. **Node ID** links to the Node Details dashboard, **Node Name** to the Pod Inspector dashboard, and **slurmd log** to the node's `slurmd` logs in Loki. |

#### Estimate model FLOPs utilization (MFU) from tensor core utilization

Use the **Tensor Core Utilization Running Jobs** panel in the **GPU Metrics** section to get a rough estimate of MFU.

![Graph showing tensor core utilization.](https://mintcdn.com/coreweave-dbfa0e8d/PdmoozL7fT8Luz34/observability/managed-grafana/_media/tensor-core.png?fit=max\&auto=format\&n=PdmoozL7fT8Luz34\&q=85\&s=3f29a66f00365e27786f41738b8edb8d)

Although tensor core utilization is a hardware-level metric and MFU is an application-level metric, the **Tensor Core Utilization Running Jobs** panel acts as an upper bound for MFU. Your model's actual mathematical efficiency can't exceed the percentage of time the hardware's tensor cores are actively processing instructions. Use tensor core utilization as a hard upper bound and diagnostic resource.

The **Current FP8 FLOPS** panel isn't a good indicator of actual model FLOPS. It provides an idealized estimate based on tensor core utilization across all GPUs on the nodes allocated to the job. The panel scales its TFLOPS-per-GPU assumption to the detected GPU model: 1979 for H100 or H200, 5000 for GB200 or GB300, 4500 for B200 or B300, 1000 for B40, 624 for A100, and 362 for L40. Unrecognized GPU models default to 1979.

#### Job Info: Job State Timeline and Last State

The **Job Info** section contains panels that display information about the state of the selected Slurm job. **Last State** displays the most recent reported state, while the **Job State Timeline** displays the job's status over time.

![Slurm Job State Timeline panel](https://mintcdn.com/coreweave-dbfa0e8d/PdmoozL7fT8Luz34/observability/managed-grafana/_media/slurm-job-state-timeline.jpeg?fit=max\&auto=format\&n=PdmoozL7fT8Luz34\&q=85\&s=28d6be857e9c936a5af5ced15a971287)

A Slurm job can be in the following states:

| State | Meaning |
| - | - |
| `RUNNING` | Actively executing on allocated resources. |
| `PENDING` | Queued to run when resources are available. |
| `CANCELLED` | Canceled by a user. |
| `COMPLETING` | Finished or canceled, and currently performing cleanup tasks, such as an Epilog script. |
| `PREEMPTED` | Preempted by another job. |
| `COMPLETED` | Successfully completed execution. |

#### Job Info: Node alerts

Job alerts in the Slurm Job Metrics dashboard are generated by CoreWeave's Mission Control, an automated system that continuously monitors and manages the underlying compute infrastructure to maintain high cluster reliability and availability. These alerts target hardware and system-level issues, such as GPU errors, networking failures, and endpoint timeouts. These conditions aren't typically observable through application-layer metrics such as training metrics or standard logs.

##### Understanding Node alerts and conditions

The following image shows an interruption caused by a Node alert, namely `GPUContainedECCError`.

* Blue lines: Indicate Node conditions.
* Red lines: Indicate Node alerts.

![Grafana dashboard showing Node alerts and conditions.](https://mintcdn.com/coreweave-dbfa0e8d/PdmoozL7fT8Luz34/observability/managed-grafana/_media/node-alerts.png?fit=max\&auto=format\&n=PdmoozL7fT8Luz34\&q=85\&s=17696957de0f442ff829f7f83f5c0988)

The Node alert indicated by the red line, `GPUContainedECCError`, appears before the drop in compute, while the Node conditions indicated by the blue lines delineate the window the drop in compute occurred within.

The image shows that the H100 cluster experienced a hard fault around 15:15. Throughput dropped from 500 PFLOPS to 0 because the Slurm scheduler pulled a Node out of the pool due to a `GPUContainedECCError`. Understanding how Node alerts and conditions are overlaid on Node metrics can help you diagnose and troubleshoot problems with a running job.

### GPU Metrics

The **GPU Metrics** section displays detailed information related to hardware utilization. In this section, red lines correspond with higher temperature or utilization of the measured value, while green lines indicate a lower value or idle state. Whether these values suggest "good" or "bad" performance depends on the expected behavior and resource utilization of the job.

| Panel | Description |
| - | - |
| **GPU Temperatures Running Jobs** | Displays the temperature of the GPUs over time. Generally, an increase in temperature corresponds with a job run, indicating that the GPUs are busy. |
| **GPU Core Utilization Running Jobs** | Displays the utilization of GPU cores over time. Red indicates high utilization. |
| **SM Utilization Running Jobs** | The fraction of time at least one warp was active on a multiprocessor, averaged over all multiprocessors. "Active" does not necessarily mean that a warp is actively computing. For example, warps waiting on memory requests are considered active. The value represents an average over a time interval and is not an instantaneous value. A value of 0.8 or greater is necessary, but not sufficient, for effective use of the GPU. A value less than 0.5 likely indicates ineffective GPU usage. |
| **GPU Mem Copy Utilization Running Jobs** | Displays the utilization of GPU memory. |
| **Tensor Core Utilization Running Jobs** | Displays the utilization of Tensor cores over time. |
| **VRAM Usage** | Plots the amount of VRAM used by the GPU over time. |
| **GPUs Temperature** | Displays the temperatures of the GPUs over time. |
| **GPUs Power Usage** | Plots the power usage of the GPUs, in watts. |

#### GPU Metrics: Color coding

| Color | Meaning |
| - | - |
| Red | High utilization. |
| Orange-Yellow | Medium-low utilization. |
| Green | Low utilization or idle. |
| Black | No job running at this time. |

![GPU Metrics panels](https://mintcdn.com/coreweave-dbfa0e8d/PdmoozL7fT8Luz34/observability/managed-grafana/_media/slurm-gpu-metrics.jpeg?fit=max\&auto=format\&n=PdmoozL7fT8Luz34\&q=85\&s=a631abc029e2d1065ed0e26c6b61dde0)

This example shows a high (red) value in the **GPU Core Utilization** panel, a medium (yellow) value in the **GPU Temperatures** panel, and low (green) values in the **GPU Mem Copy Utilization** panel. This indicates that the tracked Slurm job had high utilization of GPU Cores and low utilization of GPU memory, which may be expected for a small model size.

When you compare the fluctuations in GPU Temperature with the charts in the [**Filesystem**](#filesystem) section, you can see that drops in the GPU temperature may correspond with spikes in NFS `write` operations.

![NFS Average Request and Response panels](https://mintcdn.com/coreweave-dbfa0e8d/PdmoozL7fT8Luz34/observability/managed-grafana/_media/slurm-nfs-average-request-response.jpeg?fit=max\&auto=format\&n=PdmoozL7fT8Luz34\&q=85\&s=6355d87ef12e1e620ff13895145a7d13)

### Filesystem

The **Filesystem** section includes information about `read` and `write` operations on the Network File System (NFS) and local files.

| Panel | Description |
| - | - |
| **Local Max Disk IO Utilization (Min 1m)** | The green line indicates `write` operations and the yellow line indicates `read` operations. |
| **Local Avg Bytes Read / Written Per Node (2m)** | The red line indicates `write` operations and the blue line indicates `read` operations. |
| **Local Total bytes Read / Written (2m)** | The red line indicates `write` operations and the blue line indicates `read` operations. |
| **Local Total Read / Write Rate (2m)** | The red line indicates `write` operations and the blue line indicates `read` operations. |
| **NFS Average Request Time by Operation** | Duration requests took from when a request was enqueued to when it was completely handled for a given operation, in seconds. The green line indicates `write` operations and the yellow line indicates `read` operations. |
| **NFS Avg Bytes Read / Written Per Node (2m)** | The red line indicates `write` operations and the blue line indicates `read` operations. |
| **NFS Total Bytes Read / Written (2m)** | The red line indicates `write` operations and the blue line indicates `read` operations. |
| **NFS Total Read / Write Rate** | The red line indicates `write` operations and the blue line indicates `read` operations. |
| **NFS Average Response Time by Operation** | Duration requests took to get a reply back after a request for a given operation was transmitted, in seconds. The green line indicates `write` operations and the yellow line indicates `read` operations. |
| **NFS Avg Write Rate Per Active Node (2m)** | The red line indicates `write` operations and the dashed green line displays **active nodes**. Only includes nodes writing over 10 KB/s. |
| **NFS Avg Read Rate Per Active Node (2m)** | The blue line indicates `read` operations and the dashed green line displays **active nodes**. Only includes nodes reading over 10 KB/s. |
| **NFS Nodes with Retransmissions** | Retransmissions indicate packet loss on the network, either due to congestion or faulty equipment or cabling. |

![NFS Read and Write panels](https://mintcdn.com/coreweave-dbfa0e8d/PdmoozL7fT8Luz34/observability/managed-grafana/_media/slurm-nfs-average-read-write.jpeg?fit=max\&auto=format\&n=PdmoozL7fT8Luz34\&q=85\&s=f7603ba030a10a83c99d12365a871297)

#### Filesystem: NFS Average Response and Request

The **NFS Average Response and Request** graphs describe the performance of the filesystem. A slowdown or spike could indicate that the storage is too slow, and that the job might perform better with faster or a different type of storage, such as object storage.

#### Filesystem: NFS Total Read / Write

The **NFS Total Read / Write** graphs typically display a large red spike when a job starts, as the model and data are read in. While the job runs, the graph shows smaller write spikes at regular intervals, which occur as the checkpoints are written out. Compare these graphs with the panels in the [**GPU Metrics**](#gpu-metrics) section to help confirm that running jobs are behaving as expected.

### Node Resources

The **Node Resources** section includes the **CPU Allocation** panel, which displays the total number of CPU cores utilized over the job runtime.

### NCCL Metrics

The **NCCL Metrics** section reports how the GPUs allocated to the job communicate with each other, using telemetry from the NCCL profiler plugin. These panels populate only when GPU Straggler Detection runs on the cluster. They sample at one-minute intervals. Jobs that run for less than about two minutes produce empty or sparse panels.

The **NCCL BusBW** and **NCCL Latency** panels each appear once per process-group size, and the 32+ and 512+ panels include every group at or above that size. A job populates only the panels whose sizes its communicators match, and the remaining panels read "This job does not contain NCCL groups of this size".

| Panel | Description |
| - | - |
| **NCCL BusBW (Process Groups w/ 2, 4, 8, 16, 32+, or 512+ GPUs)** | Bus bandwidth in GB/s for collective operations running in process groups of the given size, averaged by collective and communicator. |
| **NCCL Latency (Process Groups w/ 2, 4, 8, 16, 32+, or 512+ GPUs)** | Collective execution time in microseconds for process groups of the given size, averaged by collective and communicator. The 32+ and 512+ panels also break the series out by Pod, so you can compare Nodes directly, though only the 32+ legend names the Pod. The legend sorts by mean in descending order, so the slowest collectives appear first. |
| **NCCL Message Size** | The average payload size per collective operation, in bytes. Small messages are latency-bound and don't reach the bandwidth that large messages do, so read the bandwidth panels against this one. |
| **GPU Straggler** | Identifies the GPU rank that fell behind the rest of the job in collective operations, with the start and end of the interval, the Node, and the `slurmd` Pod. The detection isolates the single furthest-behind rank, so this table normally shows one row per interval. The **Node** and **Slurmd Pod** values link to the Node Details and Pod Inspector dashboards. |
| **Slow NCCL Operations** | Lists each GPU rank whose algorithmic bandwidth dropped well below that rank's own average over the previous 24 hours, along with the **NCCL Function** affected. The remaining columns and drill-down links match **GPU Straggler**. |

For an introduction to the feature that produces these metrics, along with worked examples, see [Introduction to GPU Straggler Detection](https://docs.coreweave.com/products/sunk/discover_sunk/straggler-detection.md). To turn it on for a SUNK cluster, see [Enable GPU Straggler Detection](https://docs.coreweave.com/products/sunk/optimize_workloads/enable-gpu-straggler-detection.md).
