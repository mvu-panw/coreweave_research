# CAIOS LOTA

Source: https://docs.coreweave.com/observability/managed-grafana/storage/caios-lota

# CAIOS LOTA

> Grafana dashboard for monitoring CAIOS LOTA storage events, S3 gateway requests, and proxy metrics

The CAIOS LOTA dashboard helps you monitor storage events, S3 gateway request volume, and proxy and cache performance for CoreWeave AI Object Storage [Local Object Transport Accelerator (LOTA)](https://docs.coreweave.com/products/storage/object-storage/improving-performance/about-lota.md). Use it to track request rates, cache effectiveness, and error trends so you can verify that LOTA-backed workloads are performing as expected.

To view the dashboard, go to the [CAIOS LOTA dashboard](https://cks-grafana.coreweave.com/d/eeff523hiaewwc/caios-lota).

> [!NOTE]
>
> For instructions about accessing CoreWeave Grafana dashboards, see [Access and use CoreWeave Grafana dashboards](https://docs.coreweave.com/observability/managed-grafana/access.md).

The CAIOS LOTA dashboard provides metrics about CAIOS LOTA storage events. The following panels are available:

| Panel | Description |
| - | - |
| **Total LOTA: S3 Gateway Requests** | Shows a single, aggregated count of requests. |
| **Proxy requests** | Shows the rate of requests the gateway proxies. |
| **Cache requests** | Shows the rate of requests the cache serves. |
| **Cache hit %** | Shows the cache hit percentage. |
| **Cache hit status** | Breaks down cache requests into hits, misses, and in-progress states. |
| **Range requests** | Shows the rate of HTTP Range requests. |
| **Active LOTA count** | Shows the number of active LOTA instances or connections. |
| **Proxy errors** | Shows the number of errors in the proxy component. |
| **Cache errors** | Shows the number of errors in the cache component. |
