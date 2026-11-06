# Kueue Scheduling

Source: https://docs.coreweave.com/observability/managed-grafana/kubernetes/kueue-metrics

# Kueue Scheduling

> Grafana dashboard for monitoring Kueue admissions, queue status, preemptions, and GPU topology capacity

To view the dashboard, go to the [Kueue Scheduling Dashboard](https://cks-grafana.coreweave.com/d/amwdvqq/kueue-scheduling-dashboard).

> [!NOTE]
>
> For instructions about accessing CoreWeave Grafana dashboards, see [Access and use CoreWeave Grafana dashboards](https://docs.coreweave.com/observability/managed-grafana/access.md).

The Kueue Scheduling Dashboard provides an overview of [Kueue](https://docs.coreweave.com/products/cks/clusters/coreweave-charts/kueue.md) scheduling activity in your cluster, including workload admissions, ClusterQueue and cohort status, preemptions, evictions, and admission wait times. It also shows the GPU topology segments available for scheduling, so you can see how much contiguous capacity is available for workloads of different sizes.

Use this dashboard to monitor queue health, diagnose admission delays, and understand how workloads move through your cluster's queues. Filter the panels with the dashboard variables, such as **accelerator**, **org**, **cluster**, **Cluster Queue**, and **resource**.

Most panels are built on Kueue's Prometheus metrics. For the full list of metrics and their meanings, see the [Kueue metrics reference](https://kueue.sigs.k8s.io/docs/reference/metrics/).

The following sections describe the panels available in the Kueue Scheduling Dashboard.

## Cluster topology

The following panels show GPU capacity as topology segments. A segment means free GPUs in the same topology domain that a workload can be scheduled into. Segment sizes of 8 or fewer count free GPUs per Node, and larger segment sizes count free GPUs per NVLink domain. For more about segments and topology domains, see [Topology and block scheduling in Slurm](https://docs.coreweave.com/products/sunk/optimize_workloads/topology-scheduling.md).

| Panel | Description |
| - | - |
| **Available Segments Snapshot** | Shows the currently healthy segments available at each topology size, counting only free GPUs on Ready, schedulable Nodes. |
| **K8s-Scheduler Topology Segment Sizes** | Shows the Kubernetes scheduler's view of GPU segments at the selected size: total allocatable capacity, plus currently free segments partitioned into healthy and unhealthy by Node state. This view reflects Pods that actually exist on the cluster. It does not include capacity that Kueue has reserved for workloads whose Pods have not been created yet. |
| **Preemption-Adjusted Topology Segment Sizes** | Shows current healthy segments plus the capacity that would become free if Kueue preempted lower-priority admitted workloads in the selected ClusterQueue. |

## Kueue health

The following panels show the health of the Kueue controller manager and its admission activity:

| Panel | Description |
| - | - |
| **Kueue Version** | Shows build and version information for the Kueue controller manager, from `kueue_build_info`. |
| **Kueue Controller Manager Logs** | Displays logs from the Kueue controller manager in the `kueue-system` namespace. |
| **Admission Attempts (rate/min)** | Shows the per-minute rate of workload admission attempts, partitioned by result (success or inadmissible), from `kueue_admission_attempts_total`. |
| **Admission Attempt Latency (p50/p95/p99)** | Shows how long Kueue's admission cycle takes per attempt, from `kueue_admission_attempt_duration_seconds`. Spikes indicate scheduler slowdown. |

## ClusterQueue

The following panels show workload activity, quotas, and wait times for the selected ClusterQueues:

| Panel | Description |
| - | - |
| **CQ Preemption/Admission Rate** | Shows the per-minute rate of workload admissions and preemptions per ClusterQueue. |
| **Preemption Rate by Reason** | Shows the per-minute preemption rate broken down by reason, such as preemption within the same ClusterQueue or cohort reclamation, from `kueue_preempted_workloads_total`. |
| **Admitted Workload Priority by ClusterQueue** | Lists the priority and GPU request of each workload admitted to the selected ClusterQueues. |
| **Pending Workloads (by status)** | Shows workloads pending admission, split by status (active or inadmissible), from `kueue_pending_workloads`. |
| **Admitted Active Workloads** | Shows admitted workloads that are currently active, per ClusterQueue, from `kueue_admitted_active_workloads`. |
| **Quota-Reserving Active Workloads** | Shows workloads that are reserving quota, including admitted workloads, from `kueue_reserving_active_workloads`. |
| **Workloads in Finished State** | Shows the current count of workloads in the Finished state per ClusterQueue, before Kueue's TTL cleanup deletes them, from `kueue_finished_workloads`. |
| **Workloads Entering Finished State (rate/min)** | Shows the per-minute rate of workloads transitioning into the Finished state, a measure of completion throughput, from `kueue_finished_workloads_total`. |
| **Quota Reservations (rate/min)** | Shows the per-minute rate of workloads obtaining quota reservation, from `kueue_quota_reserved_workloads_total`. |
| **Evictions (rate/min, by reason)** | Shows the per-minute rate of eviction events by reason, from `kueue_evicted_workloads_total`. A workload evicted, re-admitted, and evicted again counts twice. |
| **Unique Evictions (rate/min)** | Shows the per-minute rate of distinct workloads being evicted for the first time, from `kueue_evicted_workloads_once_total`. Compare with **Evictions** to detect re-eviction churn. |
| **Replaced Workload Slices (rate/min)** | Shows the per-minute rate of workload slice replacements, from `kueue_replaced_workload_slices_total`. |
| **Preemption Skips (per cycle)** | Shows workloads whose preemption was skipped during an admission cycle due to resource contention, from `kueue_admission_cycle_preemption_skips`. |
| **Creation→Admission Wait (p50/p95/p99)** | Shows the time from workload creation to Kueue granting admission, from `kueue_admission_wait_time_seconds`. |
| **Creation→Quota Reservation Wait (p50/p95/p99)** | Shows the time from workload creation to obtaining quota reservation, before admission checks, from `kueue_quota_reserved_wait_time_seconds`. |
| **Quota→Admission Wait (p50/p95/p99)** | Shows the time from quota reservation to full admission, the admission-check phase, from `kueue_admission_checks_wait_time_seconds`. |
| **ClusterQueue Status** | Shows the current lifecycle status of each ClusterQueue (active, pending, or terminated), from `kueue_cluster_queue_status`. |
| **Nominal Quota (by resource)** | Shows the configured nominal quota per ClusterQueue, flavor, and resource, from `kueue_cluster_queue_nominal_quota`. |
| **Borrowing Limit (by resource)** | Shows how much each ClusterQueue can borrow from its cohort, from `kueue_cluster_queue_borrowing_limit`. |
| **Lending Limit (by resource)** | Shows how much of its quota each ClusterQueue may lend to other ClusterQueues, from `kueue_cluster_queue_lending_limit`. |
| **Resource Reservation** | Shows the total resources reserved per ClusterQueue across all flavors, from `kueue_cluster_queue_resource_reservation`. |
| **Resource Usage** | Shows resources currently in use by admitted workloads, from `kueue_cluster_queue_resource_usage`. |
| **ClusterQueue Weighted Share** | Shows the fair-share ratio used in borrowing decisions, from `kueue_cluster_queue_weighted_share`. |

## Cohort

The following panels aggregate workload and quota metrics across each cohort subtree:

| Panel | Description |
| - | - |
| **Cohort Admitted Active Workloads** | Shows admitted active workloads across the entire cohort subtree, from `kueue_cohort_subtree_admitted_active_workloads`. |
| **Cohort Admissions (rate/min)** | Shows the per-minute admission rate across the cohort subtree, from `kueue_cohort_subtree_admitted_workloads_total`. |
| **Cohort Subtree Quota (by resource)** | Shows the aggregated nominal quota across the cohort subtree, from `kueue_cohort_subtree_quota`. |
| **Cohort Subtree Reservations (by resource)** | Shows the aggregated reservations across the cohort subtree, from `kueue_cohort_subtree_resource_reservations`. |
| **Cohort Weighted Share** | Shows the fair-share ratio for cohort-level borrowing decisions, from `kueue_cohort_weighted_share`. |

## Workloads pending ready

The following panels track how long workloads take to have ready Pods, measured from workload creation and from admission. They appear in the dashboard's **Workloads Pending Ready** row, which requires the [`waitForPodsReady`](https://kueue.sigs.k8s.io/docs/tasks/manage/setup_wait_for_pods_ready/) setting in your Kueue configuration.

| Panel | Description |
| - | - |
| **Workload Creation→Ready Wait (p50/p95/p99)** | Shows the time from workload creation until its Pods are ready, from `kueue_ready_wait_time_seconds`. |
| **Workload Admission→Ready Wait (p50/p95/p99)** | Shows the time from admission until the workload's Pods are ready, from `kueue_admitted_until_ready_wait_time_seconds`. |
| **Pods Ready→Eviction Duration (p50/p95/p99)** | Shows how long workloads run after their Pods become ready before being evicted, by eviction reason, from `kueue_pods_ready_to_evicted_time_seconds`. |
