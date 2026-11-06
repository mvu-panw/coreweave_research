# Custom GPU utilization alerts

Source: https://docs.coreweave.com/observability/self-hosted-grafana/custom-alerts

# Custom GPU utilization alerts

> Create Grafana-managed alert rules to monitor GPU utilization across your cluster

You can create custom alert rules for conditions such as low GPU utilization in a [self-hosted Grafana](https://docs.coreweave.com/observability/self-hosted-grafana.md) instance with CoreWeave Metrics configured as a data source. [CoreWeave Grafana](https://docs.coreweave.com/observability/managed-grafana.md) does not support custom alert rules.

This page walks through two example alert rules that monitor GPU utilization using the `DCGM_FI_DEV_GPU_UTIL` metric from NVIDIA Data Center GPU Manager (DCGM).

## Prerequisites

Before you create these alert rules, you need the following:

* A [self-hosted Grafana](https://docs.coreweave.com/observability/self-hosted-grafana.md) instance with the CoreWeave Metrics data source configured
* A [contact point](https://grafana.com/docs/grafana/latest/alerting/configure-notifications/manage-contact-points/) to receive alert notifications

## About the DCGM GPU utilization metric

`DCGM_FI_DEV_GPU_UTIL` is a gauge metric from the NVIDIA driver that measures overall GPU utilization as a percentage (0 to 100) per device. CoreWeave exposes this metric through the CoreWeave Metrics data source.

> [!NOTE]
>
> The examples on this page exclude activity in the `cw-hpc-verification` namespace. CoreWeave runs [HPC Verification](https://docs.coreweave.com/platform/fleet-management/hpc-verification.md) tests in this namespace when GPUs are idle. Customer workloads normally preempt these tests, and they don't represent real utilization.

## Alert on average cluster GPU utilization

This alert fires when the average GPU utilization across all GPUs in a cluster falls below a threshold for a sustained period.

To create this alert rule:

1. In Grafana, navigate to **Alerting** > **Alert rules**, then select **New alert rule**.

2. Select **Grafana-managed rule** as the rule type.

3. In the query editor, switch to **Code** mode and enter the following PromQL expression. Replace `[CLUSTER-NAME]` with the name of your cluster.

   ```text theme={"system"}
   avg(
     avg_over_time(
       DCGM_FI_DEV_GPU_UTIL{cluster="[CLUSTER-NAME]", namespace!~"cw-hpc-verification"}[24h]
     )
   )
   ```

   This expression calculates the average GPU utilization across all GPUs in the cluster over a 24-hour window.

4. Under **Expressions**, configure the threshold condition. For example, set the condition to fire when the value is less than `50`.

5. Configure the **evaluation interval** and **pending period** to control how frequently the rule is evaluated and how long the condition must persist before the alert fires.

6. Select the contact point you created in the [prerequisites](#prerequisites) to receive notifications.

7. Select **Save rule and exit**.

Adjust the threshold (`50`), the time window (`24h`), and the cluster name to match your requirements.

## Alert on the proportion of idle GPUs

Instead of tracking overall average utilization, this alert fires when a certain proportion of individual GPUs in a cluster are completely idle.

This approach uses two queries and a math expression:

1. In Grafana, navigate to **Alerting** > **Alert rules**, then select **New alert rule**.

2. Select **Grafana-managed rule** as the rule type.

3. In the query editor, add two queries in **Code** mode. Replace `[CLUSTER-NAME]` with the name of your cluster.

   **Query A** counts the number of idle GPUs in the cluster, where a GPU is idle if its average utilization over the past 24 hours is zero. The `sum by (node, gpu)` clause isolates each individual GPU before the count:

   ```text theme={"system"}
   count(
     sum by (node, gpu) (
       avg_over_time(
         DCGM_FI_DEV_GPU_UTIL{cluster="[CLUSTER-NAME]", namespace!~"cw-hpc-verification"}[24h]
       )
     ) == 0
   )
   ```

   **Query B** counts the total number of GPUs in the cluster:

   ```text theme={"system"}
   count(
     sum by (node, gpu) (
       DCGM_FI_DEV_GPU_UTIL{cluster="[CLUSTER-NAME]"}
     )
   )
   ```

4. Add a **Math** expression that divides Query A by Query B to calculate the proportion of idle GPUs:

   ```text theme={"system"}
   $A / $B
   ```

5. Under **Expressions**, set the threshold condition. For example, set the condition to fire when the math expression result is greater than `0.5` (meaning more than 50% of GPUs are idle).

6. Configure the **evaluation interval** and **pending period**.

7. Select the contact point you created in the [prerequisites](#prerequisites) to receive notifications.

8. Select **Save rule and exit**.

## Learn more

For more information, explore the following resources:

* [Create Grafana-managed alert rules](https://grafana.com/docs/grafana/latest/alerting/alerting-rules/create-grafana-managed-rule/) in the Grafana documentation
* [PromQL documentation](https://prometheus.io/docs/prometheus/latest/querying/basics/) for building custom metric queries
* [CoreWeave Alerts](https://docs.coreweave.com/platform/coreweave-alerts.md) for built-in alert integrations that do not require self-hosted Grafana
