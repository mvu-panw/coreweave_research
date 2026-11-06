# Billing

Source: https://docs.coreweave.com/products/inference/billing

# Billing

> How Dedicated Inference is billed and how to optimize inference costs

This page explains how Dedicated Inference is billed and outlines practices that can help you control inference costs. Use it to understand which billing model applies to your deployments and how to optimize spend.

You are billed for the underlying compute resources consumed by your deployments. Serverless Inference is billed per token instead; see [Usage information and limits](https://docs.coreweave.com/products/inference/serverless/usage-limits.md).

## Billing models

**Node-based billing** is for customers who already have reserved node capacity. You can redirect existing reserved nodes for training or other workloads to the inference platform at your existing rates. You incur no additional charges beyond the existing reservation cost.

**GPU-based billing** is for on-demand workloads. You pay per GPU-hour based on the instance type. Inference compute is measured in GPU-hours at the deployment level. See the [CoreWeave pricing page](https://coreweave.com/pricing) for rates.

## Cost optimization

Follow these guidelines to reduce inference costs.

* **Right-size your GPU selection.** Choose the smallest instance type that meets your model's memory and throughput requirements.
* **Use autoscaling to match demand.** Scaling down during low-traffic periods reduces costs. Set `min` to the lowest value that meets your latency requirements.
* **Consider reserved capacity for steady-state workloads.** Capacity claims with reserved nodes offer predictable pricing for workloads with consistent demand.
* **Monitor replica utilization.** If replicas are consistently underutilized, consider reducing `max` or switching to a smaller instance type.
* **Use scaling priority.** When multiple deployments share reserved capacity, set `priority` so that higher-value workloads scale first.
