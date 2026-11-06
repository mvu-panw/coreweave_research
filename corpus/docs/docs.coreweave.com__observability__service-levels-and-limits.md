# Service levels and limits

Source: https://docs.coreweave.com/observability/service-levels-and-limits

# Service levels and limits

> Service level objectives, retention limits, and log size limits for CoreWeave Observe

[CoreWeave Observe™](https://docs.coreweave.com/observability.md) sets best-effort service level objectives (SLOs) for the availability, latency, and durability of its observability services, and applies limits to telemetry retention and log line size. This page lists those service levels and limits.

Service level objectives are the targets that CoreWeave aims to meet for each service, covering the availability and latency of your queries and the durability of your stored logs and metrics.

> [!NOTE]
>
> These service levels and limits are best-effort product performance guidelines.

## Service level objectives

The following table lists the service level objectives for CoreWeave observability services. Availability targets apply to real customer traffic, and query endpoints are reached through `observe.coreweave.com`.

| Service | SLO measurement |
| - | - |
| CoreWeave Grafana | 99.9% of all requests to CoreWeave Grafana complete successfully. |
| Logs query | **Availability**: 99.9% of all requests through `observe.coreweave.com` complete successfully. **Response latency**: 99% of log queries return results within 1 minute. **Retention**: 99.999% of audit logs are retained for 3 months. 99.999% of other logs are retained for 14 days. |
| Metrics query | **Availability**: 99.9% of all requests through `observe.coreweave.com` complete successfully. **Response latency**: 99% of metric queries spanning 7 days at a 1-minute step return within 5 seconds. **Retention**: 99.999% of metrics are retained for 3 months. |

For information about querying logs and metrics through these endpoints, see [Query Logs and Metrics](https://docs.coreweave.com/observability/logs-metrics/introduction.md).

## Retention limits

CoreWeave retains telemetry based on the limits described below. Data older than its retention limit might no longer be queryable, and CoreWeave deletes it within 1 to 2 days after the limit.

| Telemetry type | Retention limit |
| - | - |
| Audit logs | 3 months |
| Other logs (platform and application logs) | 14 days |
| Metrics | 3 months |

To download logs that are still within the retention limit, see [Backfill historical logs with LogCLI](https://docs.coreweave.com/observability/logs-metrics/backfill-historical-logs.md).

For use cases that require longer retention, such as audit logs, see [Configure Telemetry Relay](https://docs.coreweave.com/observability/telemetry-forwarding/configure.md) to forward telemetry to an external destination.

## Log size limits

Individual log lines are subject to a maximum size. Log lines that exceed the limit may be dropped or truncated.

| Limit | Size |
| - | - |
| Log line size limit | 256 KB |
| Telemetry Relay log line size limit | 100 KB |
