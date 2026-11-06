# Data sources

Source: https://docs.coreweave.com/observability/logs-metrics/data-sources

# Data sources

> Understand the Global and Super Regional data source locations for querying CoreWeave metrics and logs

CoreWeave captures and stores metrics and logs to help you monitor the health of your systems and troubleshoot issues. This page describes the Global and Super Regional data sources available for querying that data, and helps you choose the right data source for your use case.

CoreWeave stores logs and metrics in the location where they're generated. For example, the metrics and logs for a cluster in the Availability Zone `US-EAST-04A` are stored in the `US-EAST` Super Region. For more information about Regions and Availability Zones, see [About Regions and Availability Zones](https://docs.coreweave.com/platform/regions/about-regions-and-azs.md).

## Data locations and queries

CoreWeave provides two main locations to query data from:

* **Global location**. A single data source for all logs and metrics in all locations. The Global location lets you query and visualize metrics and logs data across clusters from multiple geographical locations.
* **Super Regional location**. The Super Regional data source for your metrics and logs. Super Regional locations are useful for highly latency-sensitive use cases and for issues that require deeper investigation. Super Regional-bound queries return more data because they don't reach the limits sometimes imposed by global queries.

Use the following table to help determine when to use Global or Super Regional data:

| Data source | When to use |
| - | - |
| **Global** | Building dashboards spanning multiple regions. Investigating issues affecting multiple clusters. Performing high-level observability analysis. |
| **Super Regional** | Troubleshooting a specific cluster. Running large or detailed log queries. Investigating incidents where query result limits may apply. |

For more information about Super Regions, see [CoreWeave's geographical hierarchy](https://docs.coreweave.com/platform/regions/about-regions-and-azs.md#geographical-hierarchy).

## Metrics data locations

CoreWeave provides the following data sources for metrics:

| Location | Address | Grafana data source name | Default data source |
| - | - | - | - |
| Global | `observe.coreweave.com` | CoreWeave Metrics | Yes |
| US-EAST | `observe.us-east.coreweave.com` | CoreWeave Metrics US-EAST | No |
| US-WEST | `observe.us-west.coreweave.com` | CoreWeave Metrics US-WEST | No |
| EU-SOUTH | `observe.eu-south.coreweave.com` | CoreWeave Metrics EU-SOUTH | No |

## Logs data locations

[Logs](#log-content) are available from both Global and Super Regional data sources. Audit logs are available through dedicated audit logs data sources in each Super Region. In the Global data source, the CoreWeave logs dataset also includes audit logs to support cross-region observability queries. For more targeted investigation or security analysis, use the regional CoreWeave audit logs data sources.

The location-specific log sources contain all logs except CKS audit logs, and the location-specific audit log data sources only contain CKS audit logs.

CoreWeave provides the following data sources for application and audit logs:

| Location | Addresses | Grafana data source name | Default data source |
| - | - | - | - |
| Global | `observe.coreweave.com` | CoreWeave Logs (includes audit logs) | Yes |
| US-EAST | `observe.us-east.coreweave.com`   `observe-audit.us-east.coreweave.com` | CoreWeave Logs US-EAST   CoreWeave Audit Logs US-EAST | No   No |
| US-WEST | `observe.us-west.coreweave.com`   `observe-audit.us-west.coreweave.com` | CoreWeave Logs US-WEST   CoreWeave Audit Logs US-WEST | No   No |
| EU-SOUTH | `observe.eu-south.coreweave.com`   `observe-audit.eu-south.coreweave.com` | CoreWeave Logs EU-SOUTH   CoreWeave Audit Logs EU-SOUTH | No   No |

### Log content

| Log type | Contents |
| - | - |
| **Application and platform logs** | Customer workload and pod logs from CKS (for example, container `stdout` and `stderr` and application output). |
| **CKS audit logs** | Tracking and recording system events and user activities for security analysis and compliance. |

The Global location provides a single unified query interface across all locations and types of logs.

## Query latency

Latency is already low when querying metrics and logs from the Global location. However, for the lowest latency, query from the location where the metrics or logs are stored.

To find where CoreWeave stores your metrics or logs, use the Cloud Console or API to get the location of your clusters, and then refer to the following table to discover where CoreWeave stores your cluster's metrics or logs:

| Metrics and logs location | Cluster locations |
| - | - |
| US-EAST | All clusters in the US-EAST and CA-EAST Super Regions |
| US-WEST | All clusters in the US-WEST and US-CENTRAL Super Regions |
| EU-SOUTH | All clusters in the EU |
