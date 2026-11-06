# Query logs and metrics

Source: https://docs.coreweave.com/observability/logs-metrics/introduction

# Query logs and metrics

> Call the metrics and logs HTTP APIs with a CoreWeave access token, including regional hosts and historical metrics endpoints

Programmatic access to metrics and logs lets you integrate CoreWeave observability data into custom dashboards, alerting pipelines, and automation workflows. Query the Prometheus-compatible and Loki-compatible HTTP APIs directly when you need capabilities beyond what [CoreWeave Grafana](https://docs.coreweave.com/observability/managed-grafana.md) or [self-hosted Grafana](https://docs.coreweave.com/observability/self-hosted-grafana.md) provide.

To efficiently export metrics and logs at scale, consider setting up telemetry forwarding to an external system with [CoreWeave Telemetry Relay](https://docs.coreweave.com/observability/telemetry-forwarding/relay.md).

For more information about metric and log data sources, see [Data sources](https://docs.coreweave.com/observability/logs-metrics/data-sources.md).

## Authentication and access

Use a [CoreWeave API access token](https://docs.coreweave.com/security/authn-authz/manage-api-access-tokens.md) for HTTP requests to the observability query endpoints. Pass the token in the `Authorization` header as a Bearer token.

Replace **`[API-ACCESS-TOKEN]`** in the following examples with your API access token secret from the [Access Tokens](https://console.coreweave.com/tokens) page in the Cloud Console.

CoreWeave evaluates authorization for observability data through [IAM Access Policies](https://docs.coreweave.com/security/iam/access-policies.md). For read-only access to metrics and logs through the APIs and CoreWeave Grafana, principals typically need the **Observability Viewer** role. In the legacy group-based model, membership in the `metrics` group granted equivalent access. See [Legacy User Permissions](https://docs.coreweave.com/security/iam/access-policies/legacy-permissions.md) for details.

> [!NOTE]
>
> The secret for a [CoreWeave API access token](https://docs.coreweave.com/security/authn-authz/manage-api-access-tokens.md) is the same value whether you pass it in `Authorization` headers or embed it in a [kubeconfig](https://docs.coreweave.com/security/authn-authz/manage-api-access-tokens.md) as `users[].user.token` for `kubectl`. The difference is which service you call: use observability hostnames such as `observe.coreweave.com` for metrics and logs APIs, and use your cluster Kubernetes API server URL from the kubeconfig for the Kubernetes API.

## Query metrics

You can query metrics through the Prometheus-compatible HTTP API. The following sections describe the available endpoints, the supported request paths, and example queries for both instant and range data.

### Global and Super Regional endpoints

Metrics are available from the Global hostname and from Super Regional hostnames. The endpoint you choose affects both query performance and the completeness of results. Super Regional endpoints can return more complete results for large or detailed queries and offer lower latency when your data is stored in that Super Region. For the authoritative list of metrics hostnames, see [Metrics data locations](https://docs.coreweave.com/observability/logs-metrics/data-sources.md#metrics-data-locations) on the Data sources page.

The following examples use the Global hostname `observe.coreweave.com`. To send the same request to a Super Regional endpoint, swap the hostname and keep the path (for example, `https://observe.us-east.coreweave.com/api/v1/query`).

The following paths are supported:

| Supported paths |
| - |
| `/api/v1/query` |
| `/api/v1/labels` |
| `/api/v1/query_range` |
| `/api/v1/series` |
| `/api/v1/label/<label_name>/values` |
| `/api/v1/query_exemplars` |
| `/api/v1/metadata` |
| `/api/v1/rules` |

#### Instant metric query

The following example uses `curl` to run an instant query that returns the total time GPUs spent in idle mode (in seconds):

```bash theme={"system"}
curl -G "https://observe.coreweave.com/api/v1/query" \
  -H "Authorization: Bearer [API-ACCESS-TOKEN]" \
  --data-urlencode 'query=node_gpu_seconds_total{mode="idle"}'
```

#### Range metric query

For a time range, use `query_range` with `start`, `end`, and `step` as Unix timestamps in seconds:

```bash theme={"system"}
curl -G "https://observe.coreweave.com/api/v1/query_range" \
  -H "Authorization: Bearer [API-ACCESS-TOKEN]" \
  --data-urlencode 'query=node_gpu_seconds_total{mode="idle"}' \
  --data-urlencode 'start=[START-TIMESTAMP]' \
  --data-urlencode 'end=[END-TIMESTAMP]' \
  --data-urlencode 'step=60'
```

Replace **`[START-TIMESTAMP]`** and **`[END-TIMESTAMP]`** with the range you need.

For more information about querying Prometheus metrics, see the Prometheus [HTTP API documentation](https://prometheus.io/docs/prometheus/latest/querying/api/).

> [!NOTE]
>
> CoreWeave does not support the [Prometheus Federation API](https://prometheus.io/docs/prometheus/latest/federation/).

### Legacy metrics

If your queries cover dates before the October 2024 backend migration, query the Legacy Prometheus host to retrieve that historical data. CoreWeave migrated its metrics backend in October 2024, and the new backend reliably contains data from **October 21, 2024** onward. For metrics collected before that date, query the Legacy Prometheus host in addition to the preceding primary endpoints. The Legacy service exposes the same Prometheus HTTP API paths (for example, `/api/v1/query` and `/api/v1/query_range`).

| Host | Use |
| - | - |
| `prometheus-legacy.ord1.coreweave.com` | Historical metrics data collected before October 21, 2024 |

> [!WARNING]
>
> Query the current endpoint first (for example, `observe.coreweave.com`), because it's faster. If the result has gaps for dates before October 21, 2024, run the same PromQL query against `https://prometheus-legacy.ord1.coreweave.com` with the same `Authorization: Bearer [API-ACCESS-TOKEN]` header.

## Query logs

You can query logs through the Loki-compatible HTTP API. The following sections cover the host matrix for each log type, the supported paths, and an example query.

### Global and Super Regional log endpoints

At the Global host, application, platform, and audit logs share one Loki-compatible API. In Super Regions, application and platform logs use `observe.<super-region>.coreweave.com`, and **CKS audit logs** use the dedicated audit host `observe-audit.<super-region>.coreweave.com` in that Super Region. For the full matrix and Grafana data source names, see [Logs data locations](https://docs.coreweave.com/observability/logs-metrics/data-sources.md#logs-data-locations). Some log types expire after two weeks.

| Location | Application and platform logs | CKS audit logs |
| - | - | - |
| Global | `observe.coreweave.com` | `observe.coreweave.com` (audit logs are included in the same dataset) |
| US East | `observe.us-east.coreweave.com` | `observe-audit.us-east.coreweave.com` |
| US West | `observe.us-west.coreweave.com` | `observe-audit.us-west.coreweave.com` |
| EU South | `observe.eu-south.coreweave.com` | `observe-audit.eu-south.coreweave.com` |

The following paths are supported:

| Supported paths |
| - |
| `/loki/api/v1/query` |
| `/loki/api/v1/query_range` |
| `/loki/api/v1/labels` |
| `/loki/api/v1/label/<name>/values` |
| `/loki/api/v1/series` |
| `/loki/api/v1/index/stats` |
| `/loki/api/v1/index/volume` |
| `/loki/api/v1/index/volume_range` |
| `/loki/api/v1/format_query` |

#### Log query format

The following example returns Kubernetes audit logs for a cluster:

```bash theme={"system"}
curl -G "https://observe.coreweave.com/loki/api/v1/query_range" \
  -H "Authorization: Bearer [API-ACCESS-TOKEN]" \
  --data-urlencode 'query={logging_component="unicaster", app="kube-apiserver", stream="", cluster="[CLUSTER-NAME]"} | json | apiVersion="audit.k8s.io/v1" | json sourceIPs="sourceIPs" | json user_groups="user.groups"'
```

Replace `[CLUSTER-NAME]` with your cluster name.

To download retained logs over a large time range, see [Backfill historical logs with LogCLI](https://docs.coreweave.com/observability/logs-metrics/backfill-historical-logs.md).

## Grafana Explore

If you prefer an interactive UI to direct API calls, you can run the same kinds of ad hoc queries in Grafana. **[Grafana Explore](https://grafana.com/docs/grafana/latest/visualizations/explore/)** is available in CoreWeave Grafana and supports the full range of PromQL and LogQL for ad hoc queries on metrics and logs. You can also view metadata such as which metrics are available or which labels you can use to filter PromQL queries.

CoreWeave's default dashboards offer curated views of specific logs and metrics, and you can use the **Explore** tab to investigate metrics in more detail.

![Grafana Explore tab showing the query interface and metric metadata](https://mintcdn.com/coreweave-dbfa0e8d/PdmoozL7fT8Luz34/observability/_media/grafana-explore-tab.png?fit=max\&auto=format\&n=PdmoozL7fT8Luz34\&q=85\&s=1bcd17f9b11e67fb5581692157fb16e3)

> [!NOTE]
>
> For more information, see [Get started with Grafana Explore](https://grafana.com/docs/grafana/latest/visualizations/explore/get-started-with-explore/).
