# Slurm Block Topology

Source: https://docs.coreweave.com/observability/managed-grafana/sunk/slurm-block-topology

# Slurm Block Topology

> Grafana dashboard for visualizing Slurm compute Node availability and allocation by block topology

To view the dashboard, go to the [Slurm Block Topology dashboard](https://cks-grafana.coreweave.com/d/6d5afc99-124d-4ab4-9914-fde3bf8c581e/slurm-block-topology).

> [!NOTE]
>
> For instructions about accessing CoreWeave Grafana dashboards, see [Access and use CoreWeave Grafana dashboards](https://docs.coreweave.com/observability/managed-grafana/access.md).

![Slurm Block Topology Dashboard](https://mintcdn.com/coreweave-dbfa0e8d/PdmoozL7fT8Luz34/observability/_media/slurm-topology-dashboard.png?fit=max\&auto=format\&n=PdmoozL7fT8Luz34\&q=85\&s=908488a686687666e428514ad69aa383)

The **Slurm Block Topology** dashboard shows the availability, allocation, and status of compute Nodes, specifically organized by a block topology.

The Slurm Block Topology dashboard is especially helpful for visualizing and understanding metrics for GPUs connected through rack-level [NVLink](https://docs.coreweave.com/platform/instances/selecting-an-instance.md#the-role-of-nvlink-and-infiniband) fabrics like the GB200 and GB300 instance types.

For documentation related to segment size, see the [segments section in Topology/Block Scheduling in Slurm](https://docs.coreweave.com/products/sunk/optimize_workloads/topology-scheduling.md#segments).

| Panel | Description |
| - | - |
| **Idle Nodes by Segment Size** | Displays how many idle Nodes are available for jobs at a certain segment size. |
| **Idle Nodes by all Segment Sizes** | Shows a breakdown of all idle Node counts categorized by different segment sizes. |
| **Idle Segments by Segment Size** | Shows the number of segments at a given size that can be allocated to each of the blocks. This panel is useful to see the potential scheduling targets by listing all the segments across blocks that have the required number of Nodes.  **How to use**: Select the segment size you want to use for your job. The recommended max segment size is 16. Then check this panel to see how your job's segments can be allocated across the different blocks in your cluster. |
| **Idle Nodes Per Block by Segment Size** | Shows the number of Nodes that can be allocated to each of the blocks. Helps determine whether to attempt a larger segment size for single-rack or multi-rack jobs. **How to use**: Start by selecting a segment size, for example, 7, in the selector. The dashboard updates to show all blocks that have at least 7 idle Nodes, and for each block, it displays the total number of Nodes available in that block. For example, if you need 30 Nodes total and expect to use 5 blocks, you can quickly see whether blocks with 10 or more Nodes are available. This lets you change to segment size 10 and use 3 racks instead of 5. Using fewer racks is recommended because communication overhead increases as the number of racks increases, which reduces performance. |
| **Idle Nodes per Block** | Shows the count of all idle Nodes within each block, regardless of their segment size. |
| **Allocated Nodes per Block** | Displays the number of Nodes that are currently allocated or in use, aggregated per block. |
| **Slurm Nodes Status** | Shows the status of all Slurm Nodes. |

## Per-job allocation panels

The dashboard also includes two panels that break down per-job allocation across blocks. These panels help you understand how running jobs are distributed across the cluster's block topology.

| Panel | Description |
| - | - |
| **Nodes Allocated by Job per Block** | Shows the count of Nodes allocated within each block for each running job in the cluster. |

The following screenshot shows the **Nodes Allocated by Job per Block** panel:

![Nodes Allocated by Job per Block panel.](https://mintcdn.com/coreweave-dbfa0e8d/PdmoozL7fT8Luz34/observability/managed-grafana/_media/nodes-per-job-per-block.png?fit=max\&auto=format\&n=PdmoozL7fT8Luz34\&q=85\&s=03065521a23ad9a70fc89d4ec8f06720)

| Panel | Description |
| - | - |
| **Nodes Allocated by Block per Job** | Shows the number of Nodes used by different running jobs for each block in the cluster. |

The following screenshot shows the **Nodes Allocated by Block per Job** panel:

![Nodes Allocated by Block per Job panel.](https://mintcdn.com/coreweave-dbfa0e8d/PdmoozL7fT8Luz34/observability/managed-grafana/_media/nodes-by-block-per-job.png?fit=max\&auto=format\&n=PdmoozL7fT8Luz34\&q=85\&s=4c63588d813cf6f469d5b07500d19d64)
