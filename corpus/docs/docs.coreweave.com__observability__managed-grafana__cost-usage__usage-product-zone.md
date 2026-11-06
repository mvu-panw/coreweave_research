# Usage by product and zone

Source: https://docs.coreweave.com/observability/managed-grafana/cost-usage/usage-product-zone

# Usage by product and zone

> Grafana dashboard for tracking resource consumption by product and zone with measured and net usage

View the dashboard: [Usage by Product and Zone](https://cks-grafana.coreweave.com/d/depy94jcpvgu8f/usage-by-product-and-zone)

> [!NOTE]
>
> For instructions about accessing CoreWeave Grafana dashboards, see [Access and use CoreWeave Grafana dashboards](https://docs.coreweave.com/observability/managed-grafana/access.md).

The Usage by Product and Zone dashboard shows resource consumption categorized by product and zone. It displays metrics such as GPU and CPU usage, storage consumption, and IP address allocation to help you understand both your measured usage and the net usage that forms the basis for billing.

The dashboard shows consumption metrics as daily aggregates, up to the end of the last full billing day ending at 5 PM US and Canadian Eastern Time. By default, the dashboard shows the current billing month to date.

Billing months span from 5 PM US and Canadian Eastern Time the day before the start of a month to 5 PM US and Canadian Eastern Time on the last day of the month. For example, billing for September 2025 spans from August 31, 2025 at 5 PM to September 30, 2025 at 5 PM.

## View the dashboard

This section explains the permissions you need and how to open the dashboard in Grafana.

> [!NOTE]
>
> To see data in the Usage by Product and Zone dashboard, you need both the **Observability Viewer** and **Billing Viewer** roles in an [IAM Access Policy](https://docs.coreweave.com/security/iam/access-policies.md). (In the legacy CoreWeave permissions model, membership in the [`metrics` and `billing_viewer` groups](https://docs.coreweave.com/security/iam/access-policies/legacy-permissions) also grants this access.)

To view the dashboard, go to the [Usage by Product and Zone](https://cks-grafana.coreweave.com/d/depy94jcpvgu8f/usage-by-product-and-zone) dashboard in Grafana, or go to **Dashboards** > **Cost and Usage** > **Usage by Product and Zone** in Grafana.

For instructions on accessing CoreWeave Grafana dashboards, see [Access and Use CoreWeave Grafana Dashboards](https://docs.coreweave.com/observability/managed-grafana/access.md).

## Measured usage versus net usage

Before reviewing the individual panels, it helps to understand the two usage values that the dashboard reports for each resource type. The dashboard shows two sets of cards for each resource type (GPUs, CPUs, Storage, IP Addresses):

* **Measured usage** (all metered usage): All usage metered by CoreWeave before any exclusions, adjustments, or special programs are applied.
* **Net usage** (after exclusions): Usage remaining after CoreWeave-level exclusions and adjustments are applied. This net usage is what CoreWeave uses as the basis for your billing, subject to your contract terms (for example, rates, discounts, and credits).

The dashboard reports both measured and net usage in the same units and over the same time window so you can compare them directly.

## Panels

The following sections describe each panel on the dashboard, including the metric it displays and how measured and net usage relate to it. The Usage by Product and Zone dashboard contains the following panels:

| Panel | Description |
| - | - |
| **GPUs** | Displays daily aggregate `instance-hours` by product and zone. |
| **CPUs** | Displays daily aggregate `instance-hours` by product and zone. |
| **Storage** | Displays daily aggregate `GiB-hours` for Distributed File Storage (POSIX). |
| **IP Addresses** | Displays daily aggregate `address-hours` by IP addresses. |
| **Summary** | Displays the product, its zone, and its aggregate consumption over the full time period. |

### GPUs panel

The GPUs panel displays daily aggregate instance-hours by product and zone:

* **GPUs - Measured usage**: Shows all GPU instance-hours metered by CoreWeave, grouped by product and zone, before any exclusions, adjustments, or special programs are applied.
* **GPUs - Net usage**: Shows GPU instance-hours after CoreWeave-level exclusions and adjustments have been applied. This net usage is used as the basis for your billing, subject to your contract terms.

Both panels use the same daily granularity and time range, so you can compare total measured GPU usage against the net amount counted toward billing.

![GPUs panel showing daily aggregate instance-hours by product and zone](https://mintcdn.com/coreweave-dbfa0e8d/PdmoozL7fT8Luz34/observability/_media/usage-gpus.png?fit=max\&auto=format\&n=PdmoozL7fT8Luz34\&q=85\&s=a30c5b877288cbe90c800663ec0f39e1)

### CPUs panel

The CPUs panel displays daily aggregate instance-hours by product and zone:

* **CPUs - Measured usage**: Shows all CPU instance-hours metered by CoreWeave, grouped by product and zone, before any exclusions, adjustments, or special programs are applied.
* **CPUs - Net usage**: Shows CPU instance-hours after CoreWeave-level exclusions and adjustments have been applied. This net usage is used as the basis for your billing, subject to your contract terms.

As with GPUs, both CPU panels share the same time range and aggregation so you can see the impact of exclusions over time.

![CPUs panel showing daily aggregate instance-hours by product and zone](https://mintcdn.com/coreweave-dbfa0e8d/PdmoozL7fT8Luz34/observability/_media/usage-cpus.png?fit=max\&auto=format\&n=PdmoozL7fT8Luz34\&q=85\&s=ab49d0bea38c0852dde8704050735049)

### Storage panel

The Storage section contains two panels that show Distributed File Storage (POSIX) usage by product and zone:

* **Storage - Measured usage**: Shows daily aggregate GiB-hours of provisioned Distributed File Storage, grouped by product and zone, before any exclusions or adjustments.
* **Storage - Net usage**: Shows daily aggregate GiB-hours of storage after CoreWeave-level exclusions and adjustments have been applied. This net storage usage is used as part of the basis for your billing, subject to your contract terms.

Use these panels to understand how much storage you have provisioned and how much of that usage is counted toward billing.

![Storage panel showing daily aggregate GiB-hours for Distributed File Storage (POSIX)](https://mintcdn.com/coreweave-dbfa0e8d/PdmoozL7fT8Luz34/observability/_media/usage-storage.png?fit=max\&auto=format\&n=PdmoozL7fT8Luz34\&q=85\&s=918aebcb191c59d729e497db33a0aa7f)

### IP addresses panel

The IP Addresses section contains two panels that show IP address allocation by product and zone:

* **IP Addresses - Measured usage**: Shows daily aggregate address-hours allocated, grouped by IP address, product, and zone, before any exclusions or adjustments.
* **IP Addresses - Net usage**: Shows daily aggregate address-hours after CoreWeave-level exclusions and adjustments have been applied. This net IP usage is used as part of the basis for your billing, subject to your contract terms.

These panels help you see how IP address allocation translates into the usage that CoreWeave ultimately counts toward billing.

![IP Addresses panel showing daily aggregate address-hours allocated by IP address, product, and zone](https://mintcdn.com/coreweave-dbfa0e8d/PdmoozL7fT8Luz34/observability/_media/usage-ip-addresses.png?fit=max\&auto=format\&n=PdmoozL7fT8Luz34\&q=85\&s=df0bcae0961999c9f8c2d5296537bf8d)
