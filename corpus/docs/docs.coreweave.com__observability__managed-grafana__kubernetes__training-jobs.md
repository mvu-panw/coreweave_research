# Kubernetes Training Workloads

Source: https://docs.coreweave.com/observability/managed-grafana/kubernetes/training-jobs

# Kubernetes Training Workloads

> Grafana dashboard for monitoring training workload hardware, placement topology, and Node health

To view the dashboard, go to the [Kubernetes Training Workloads dashboard](https://cks-grafana.coreweave.com/d/0e4589d5-97fc-4d60-8c5c-301d43f57edd/kubernetes-training-workloads).

> [!NOTE]
>
> For instructions about accessing CoreWeave Grafana dashboards, see [Access and use CoreWeave Grafana dashboards](https://docs.coreweave.com/observability/managed-grafana/access.md).

The Kubernetes Training Workloads dashboard helps you monitor a training workload end to end. It combines hardware metrics for GPU utilization, network bandwidth (such as InfiniBand), and storage I/O (both local and NFS) with a topology view of where the workload's Pods are placed across Nodes, NVLink domains, leaf groups, SuperPods, and cabinets. Use it to diagnose performance bottlenecks, spot unhealthy Nodes, and understand how placement affects your workload.

Select a workload with the dashboard variables, such as **Org**, **Cluster**, **Namespace**, **Kind**, **Workload**, and **Pod**. The dashboard resolves parent workloads, such as a JobSet, MPIJob, CronJob, or Deployment, down to their child Pods.

The following sections describe the panels available on the dashboard.

## Workload overview

The following panels summarize the selected workload:

| Panel | Description |
| - | - |
| **Kind** | Shows the Kubernetes object kind. |
| **Name** | Shows the name of the resource. |
| **Nodes** | Shows the total number of Nodes. |
| **Pods** | Shows the total number of Pods. |
| **Uptime** | Shows the overall uptime. |
| **Pod Readiness Timeline (per pod)** | Shows one row per Pod, colored by phase over time: green for Running, yellow for Pending, red for Failed, blue for Succeeded, and purple for Unknown. |
| **Active GPUs** | Shows the total GPUs actively computing across all Nodes the workload occupies. On a shared Node, this count also includes another workload's busy GPUs. |
| **Job Efficiency** | Shows the average share of the workload's Nodes that are fully busy over the selected time range. A Node counts as busy only when every GPU on it is at least 50% active. Dips indicate checkpoint writes, restarts, stragglers, data-loader stalls, or communication bottlenecks. This is not a Model FLOPs Utilization (MFU) metric. |
| **Current FP8 FLOPS** | Shows the current floating-point operations per second in FP8 precision, scaled per GPU type. |
| **Topology Churn** | Shows the number of Pods in the workload and the distinct Nodes they run on. A repeated sawtooth pattern indicates Pods crash-looping or repeatedly rescheduling across Nodes. |

## GPU metrics

The following panels show GPU utilization and hardware metrics for the workload:

| Panel | Description |
| - | - |
| **GPU Temperatures for Workload** | Shows the GPU temperatures for the workload as a heatmap. |
| **GPU Core Utilization for Workload** | Shows GPU core usage as a heatmap. Black streaks mean the Node had no job at that time. Green means the GPU was idle. |
| **SM Utilization for Workload** | Shows the fraction of time at least one warp was active on a streaming multiprocessor, averaged over all multiprocessors. A value of 0.8 or greater is necessary, but not sufficient, for effective use of the GPU. A value less than 0.5 likely indicates ineffective GPU usage. |
| **GPU Mem Copy Utilization for Workload** | Shows GPU memory copy utilization as a heatmap. |
| **Tensor Core Utilization for Workload** | Shows the utilization of Tensor Cores as a heatmap. |
| **Current FP8 FLOPS** | Shows the current FP8 performance, scaled per GPU type. |
| **VRAM Usage** | Displays the video RAM usage. |
| **GPUs Temperature** | Displays the temperature of the GPUs. |
| **InfiniBand Aggregate Bandwidth** | Shows the total network bandwidth over the InfiniBand interconnect. |
| **GPUs Power Usage** | Displays the power consumption of the GPUs. |

## Filesystem and NFS

The following panels show local disk and NFS storage I/O for the workload's Nodes:

| Panel | Description |
| - | - |
| **Local Max Disk I/O Utilization (Min 1m)** | Shows the worst disk I/O utilization among the workload's Nodes, sampled at a minimum 1-minute interval. |
| **Local Avg Bytes Read / Written Per Node (2m)** | Shows the average bytes read/written per Node on the local disk. |
| **Local Total Bytes Read / Written (2m)** | Shows the total bytes read/written on the local disk over 2 minutes. |
| **Local Total Read / Write Rate (2m)** | Shows the total read/write rate on the local disk over 2 minutes. |
| **NFS Average Request Time by Operation** | Shows duration requests took from when a request was enqueued to when it was completely handled for a given operation, in seconds. |
| **NFS Avg Bytes Read / Written Per Node (2m)** | Shows the average bytes read/written per Node on the NFS. |
| **NFS Total Bytes Read / Written (2m)** | Shows the total bytes read/written on the NFS over 2 minutes. |
| **NFS Total Read / Write Rate (2m)** | Shows the total read/write rate on the NFS over 2 minutes. |
| **NFS Average Response Time by Operation** | Shows duration requests took to get a reply back after a request for a given operation was transmitted, in seconds. |
| **NFS Avg Write Rate Per Active Node (2m)** | Shows the average NFS write rate per active Node. Only includes Nodes reading/writing over 10 KB/s. |
| **NFS Avg Read Rate Per Active Node (2m)** | Shows the average NFS read rate per active Node. Only includes Nodes reading/writing over 10 KB/s. |
| **NFS Nodes with Retransmissions** | Shows the count of NFS Nodes experiencing network retransmissions, which indicate packet loss, congestion, or faulty equipment or cabling. |

## NVLink domain overview

The dashboard shows a gauge for each NVLink domain, displaying the number of Nodes in the domain with GPUs in use.

## Node health and conditions

The following panels show the health of the Nodes running the workload:

| Panel | Description |
| - | - |
| **Node Condition Events (last 10m)** | Shows Node conditions that newly fired in the last 10 minutes on the workload's Nodes. Routine conditions are excluded. Empty is the normal, quiet state. |
| **Alerts** | Displays active alerts related to this resource. |
| **Nodes (Range)** | Shows the individual Pods, their running status, and uptime on each Node. |
| **Node States** | Shows the state of each Node running the workload. |
| **Active Node Conditions** | Shows Node conditions that are currently active on the workload's Nodes, regardless of when the condition started. Routine conditions are excluded. |

## Workload placement

The following panels show where the workload's Pods are placed in the cluster's physical topology:

| Panel | Description |
| - | - |
| **Pods**, **Nodes**, **NVLink Domains**, **Leaf Groups**, **SuperPods** (stats) | Stat panels that show the count of each topology level the workload spans. |
| **Nodes**, **NVLink Domains**, **Leaf Groups**, **SuperPods** (tables) | Tables that list the Nodes, NVLink domains, leaf groups, and SuperPods the workload occupies. |
| **Pod → Node → NVLink Domain → Leafgroup → Superpod** | Maps each Pod through every level of the placement hierarchy. |
| **Pod → Node Assignment Over Time** | Shows which Node each Pod was assigned to over time, to reveal rescheduling. |
| **Workload Pods** | Lists the Pods in the NVLink domain selected with the **NVLink Domain (with pods)** variable. |

## Cabinet visualization

The cabinet visualization shows a physical rack view, where each column is a rack. Nodes appear as slots with Pod circles inside, and each Node is colored green when healthy or red when it has active Node conditions.
