# Mission Control MCP tool reference

Source: https://docs.coreweave.com/observability/mission-control-mcp/reference/tools

# Mission Control MCP tool reference

> Mission Control MCP tools for observability, resources, and supported write actions.

[CoreWeave Mission Control MCP](https://docs.coreweave.com/observability/mission-control-mcp.md) is a hosted Model Context
Protocol (MCP) server. This page lists its tools by family. Each tool entry describes what the tool
does, its inputs, and its output.

For setup instructions, see [Configure Mission Control MCP](https://docs.coreweave.com/observability/mission-control-mcp/configure.md).

## Capabilities and caveats

A few conventions apply across the catalog:

* **Most tools are read-only.** CoreWeave can enable the tools in
  [Write actions](#write-actions) for an organization. Those tools can modify supported resources
  and run with the caller's identity and permissions.
* **Many observability tools require a `datasourceUid`.** Discover datasources and their UIDs with
  [`list_datasources`](#list_datasources). To find which datasource a dashboard panel uses, call
  [`get_dashboard_panel_queries`](#get_dashboard_panel_queries).
* **Time formats vary by tool** and are noted in each tool's inputs. Metric query tools accept
  RFC3339 timestamps or expressions relative to now, such as `now`, `now-1h`, or `now-2h45m`. Log
  query tools accept RFC3339 timestamps. ClickHouse tools and `search_logs` accept relative
  expressions, RFC3339 timestamps, or Unix milliseconds.
* **Every tool also accepts an optional `user_prompt` string.** It carries the prompt that led to
  the call and is used only for server-side observability. It does not affect results and is
  omitted from the following tables.
* **One tool takes no parameters.** [`cw_cluster_get`](#cw_cluster_get) notes this in prose in
  place of an input table.

## Tool families

The following table lists the documented tools by family.

| Family | Tools |
| - | - |
| [Datasources](#datasources) | `list_datasources`, `get_datasource` |
| [Metrics](#metrics) | `list_metric_names`, `list_metric_metadata`, `list_metric_label_names`, `list_metric_label_values`, `query_metrics`, `query_metric_histogram` |
| [Logs](#logs) | `list_logs_label_names`, `list_logs_label_values`, `query_logs_stats`, `query_logs_patterns`, `query_logs`, `list_clickhouse_tables`, `describe_clickhouse_table`, `query_clickhouse`, `search_logs` |
| [Dashboards and folders](#dashboards-and-folders) | `search_dashboards`, `get_dashboard_summary`, `get_dashboard_property`, `get_dashboard_panel_queries`, `get_dashboard_by_uid`, `search_folders`, `generate_deeplink` |
| [Documentation](#documentation) | `search_coreweave_docs`, `query_filesystem_coreweave_docs` |
| [Billing](#billing) | `coreweave_billing_get_focus_usage` |
| [Clusters and Nodes](#clusters-and-nodes) | `cw_cluster_get`, `cw_cluster_describe`, `cw_node_list`, `cw_node_describe`, `cw_node_view` |
| [CoreWeave SUNK](#coreweave-sunk) | `cw_sunk_describe`, `cw_sunk_view` |
| [CoreWeave AI Object Storage](#coreweave-ai-object-storage) | `cw_cwobject_list`, `cw_cwobject_bucket_describe` |
| [Write actions](#write-actions) | `coreweave_kubectl_apply`, `coreweave_inference_update_deployment` |

## Datasources

Use these tools to discover the datasources available to your organization and the UIDs that the
metrics, logs, and dashboard tools need.

### `list_datasources`

List all configured datasources in Grafana. Use it to discover available datasources and their
UIDs. Supports filtering by type and pagination.

| Parameter | Type | Required | Description |
| - | - | - | - |
| `type` | `string` | No | Filter by datasource type. |
| `limit` | `integer` | No | Maximum number of datasources to return. Default `50`, maximum `100`. |
| `offset` | `integer` | No | Number of datasources to skip, for pagination. Default `0`. |

**Output:** a list of datasources, each with its name, type, and UID.

### `get_datasource`

Retrieve detailed information about a single datasource by UID or name. Provide either `uid` or
`name`. If both are given, `uid` takes priority.

| Parameter | Type | Required | Description |
| - | - | - | - |
| `uid` | `string` | No | The UID of the datasource. Takes priority over `name` if both are provided. |
| `name` | `string` | No | The name of the datasource. Used if `uid` is not provided. |

**Output:** the full datasource model, including name, type, URL, access settings, JSON data, and
secure field status.

## Metrics

Query metric datasources. The typical workflow is to discover metric names, narrow with label
values, then query: run
`list_metric_names`, then `list_metric_label_values`, then `query_metrics`.

### `list_metric_names`

List metric names in a metric datasource, filtered by a regular expression. Call this first to find
available metrics before querying. Supports pagination.

| Parameter | Type | Required | Description |
| - | - | - | - |
| `datasourceUid` | `string` | Yes | The UID of the datasource to query. |
| `regex` | `string` | No | Regular expression to match against metric names. |
| `limit` | `integer` | No | Maximum number of results to return. Default `10`. |
| `page` | `integer` | No | Page number to return. Default `1`. |

**Output:** a list of metric names that match the regular expression.

### `list_metric_metadata`

List metadata about metrics scraped from targets, such as type, help text, and unit.

| Parameter | Type | Required | Description |
| - | - | - | - |
| `datasourceUid` | `string` | Yes | The UID of the datasource to query. |
| `metric` | `string` | No | The metric to query metadata for. |
| `limit` | `integer` | No | Maximum number of metrics to return. Default `10`. |
| `limitPerMetric` | `integer` | No | Maximum number of metadata entries to return per metric. |

**Output:** metric metadata entries.

### `list_metric_label_names`

List label names in a metric datasource. Supports filtering by series selectors and a time range.

| Parameter | Type | Required | Description |
| - | - | - | - |
| `datasourceUid` | `string` | Yes | The UID of the datasource to query. |
| `matches` | `array` | No | Label matchers to filter results. Each entry holds a list of `filters`, where a filter has a `name`, a `value`, and a `type` of `=`, `!=`, `=~`, or `!~`. |
| `startRfc3339` | `string` | No | Start of the time range to filter by, in RFC3339. |
| `endRfc3339` | `string` | No | End of the time range to filter by, in RFC3339. |
| `limit` | `integer` | No | Maximum number of results to return. Default `100`. |

**Output:** a list of label names.

### `list_metric_label_values`

Get the values for a specific label name in a metric datasource. Use it after
`list_metric_names` to find values for filtering queries. Supports filtering by series
selectors and a time range.

| Parameter | Type | Required | Description |
| - | - | - | - |
| `datasourceUid` | `string` | Yes | The UID of the datasource to query. |
| `labelName` | `string` | Yes | The name of the label to query values for. |
| `matches` | `array` | No | Selectors to filter results, in the same shape as `list_metric_label_names`. |
| `startRfc3339` | `string` | No | Start of the time range, in RFC3339. |
| `endRfc3339` | `string` | No | End of the time range, in RFC3339. |
| `limit` | `integer` | No | Maximum number of results to return. Default `100`. |

**Output:** a list of values for the requested label.

### `query_metrics`

Run a PromQL (Prometheus Query Language) query against a metric datasource. Supports instant
queries, which return a single point, and range queries, which return a series over a time range.

| Parameter | Type | Required | Description |
| - | - | - | - |
| `datasourceUid` | `string` | Yes | The UID of the datasource to query. |
| `expr` | `string` | Yes | The expression to query. |
| `endTime` | `string` | Yes | End time. RFC3339 or relative to now, such as `now`, `now-1.5h`, or `now-2h45m`. |
| `queryType` | `string` | No | `range` or `instant`. Default `range`. |
| `startTime` | `string` | No | Start time. Required when `queryType` is `range`, ignored when `instant`. |
| `stepSeconds` | `integer` | No | Step size in seconds. Required when `queryType` is `range`, ignored when `instant`. |

**Output:** the query result, either a single value for an instant query or a time series for a
range query.

### `query_metric_histogram`

Compute histogram percentiles for a histogram metric. The tool generates the `histogram_quantile`
expression for you. Discover histograms first by running `list_metric_names` with the regex
`.*_bucket$`.

| Parameter | Type | Required | Description |
| - | - | - | - |
| `datasourceUid` | `string` | Yes | The UID of the metric datasource. |
| `metric` | `string` | Yes | Base histogram metric name, without the `_bucket` suffix. |
| `percentile` | `number` | Yes | Percentile to calculate, such as `50`, `90`, `95`, or `99`. |
| `labels` | `string` | No | Label selector, such as `job="api", service="gateway"`. |
| `startTime` | `string` | No | Start time. RFC3339, relative, or Unix milliseconds. Default `now-1h`. |
| `endTime` | `string` | No | End time. RFC3339, relative, or Unix milliseconds. Default `now`. |
| `stepSeconds` | `integer` | No | Step size in seconds for a range query. Default `60`. |
| `rateInterval` | `string` | No | Rate interval for the query. Default `5m`. |

**Output:** the percentile time series produced by the generated `histogram_quantile` query.

## Logs

Mission Control MCP reads logs from multiple backends. ClickHouse tools use SQL over
OpenTelemetry-style log tables. The `search_logs` tool works across either backend and generates
the right query for you.

### `list_logs_label_names`

List all label names found in logs within a log datasource and time range.

| Parameter | Type | Required | Description |
| - | - | - | - |
| `datasourceUid` | `string` | Yes | The UID of the datasource to query. |
| `startRfc3339` | `string` | No | Start of the time range, in RFC3339. Default one hour ago. |
| `endRfc3339` | `string` | No | End of the time range, in RFC3339. Default now. |

**Output:** a list of unique label names, such as `["app", "env", "pod"]`.

### `list_logs_label_values`

Get all unique values for a specific label within a log datasource and time range. Useful for
discovering filter options.

| Parameter | Type | Required | Description |
| - | - | - | - |
| `datasourceUid` | `string` | Yes | The UID of the datasource to query. |
| `labelName` | `string` | Yes | The name of the label to retrieve values for, such as `app`, `env`, or `pod`. |
| `startRfc3339` | `string` | No | Start of the time range, in RFC3339. Default one hour ago. |
| `endRfc3339` | `string` | No | End of the time range, in RFC3339. Default now. |

**Output:** a list of values for the requested label.

### `query_logs_stats`

Retrieve statistics about the log streams matching a selector. Use it to check stream size
before retrieving logs. The selector must be a simple label matcher, such as
`{app="nginx", env="prod"}`. It does not support line filters, parsers, or aggregations.

| Parameter | Type | Required | Description |
| - | - | - | - |
| `datasourceUid` | `string` | Yes | The UID of the datasource to query. |
| `logql` | `string` | Yes | A label-matcher selector. Line filters and aggregations are not supported. |
| `startRfc3339` | `string` | No | Start of the time range, in RFC3339. Default one hour ago. |
| `endRfc3339` | `string` | No | End of the time range, in RFC3339. Default now. |

**Output:** an object with the count of streams, chunks, entries, and total bytes, such as
`{"streams": 5, "chunks": 50, "entries": 10000, "bytes": 512000}`.

### `query_logs_patterns`

Retrieve detected log patterns for a stream selector and time range. Patterns help identify
common log structures and anomalies. The selector must be a stream selector, such as `{job="nginx"}`,
and does not support line filters or aggregations.

| Parameter | Type | Required | Description |
| - | - | - | - |
| `datasourceUid` | `string` | Yes | The UID of the datasource to query. |
| `logql` | `string` | Yes | A stream selector, such as `{job="foo", namespace="bar"}`. |
| `startRfc3339` | `string` | No | Start of the time range, in RFC3339. Default one hour ago. |
| `endRfc3339` | `string` | No | End of the time range, in RFC3339. Default now. |
| `step` | `string` | No | Query resolution step, such as `5m`. |

**Output:** a list of patterns, each with a pattern string and a total count of occurrences.

### `query_logs`

Run a LogQL (Loki's Query Language) query against a log datasource to retrieve log entries or metric
values. Supports label matchers, line filters, parsers, and pipeline
operations. Check stream size with `query_logs_stats` and verify labels with the label tools first.

| Parameter | Type | Required | Description |
| - | - | - | - |
| `datasourceUid` | `string` | Yes | The UID of the datasource to query. |
| `logql` | `string` | Yes | The query to execute, such as `{app="foo"} \|= "error"` or `rate({app="bar"}[1m])`. |
| `queryType` | `string` | No | `range` (default) or `instant`. Use `instant` for the current value of a metric query. |
| `startRfc3339` | `string` | No | Start of the time range, in RFC3339. |
| `endRfc3339` | `string` | No | End of the time range, in RFC3339. |
| `limit` | `integer` | No | Maximum number of log lines to return. Default `10`, maximum `100`. |
| `direction` | `string` | No | `forward` for oldest first, or `backward` for newest first. Default `backward`. |
| `stepSeconds` | `integer` | No | Resolution step in seconds for range metric queries. |

**Output:** a list of results, each with a timestamp, labels, and either a log line (`line`) or a
numeric metric value (`value`).

### `list_clickhouse_tables`

List the available tables in a ClickHouse datasource. Start here for ClickHouse, then use
`describe_clickhouse_table` to see column schemas.

| Parameter | Type | Required | Description |
| - | - | - | - |
| `datasourceUid` | `string` | Yes | The UID of the ClickHouse datasource. |
| `database` | `string` | No | Database name to filter tables. Lists all non-system databases if not specified. |

**Output:** a list of tables, each with its name, database, engine, row count, and size.

### `describe_clickhouse_table`

Get the column schema for a ClickHouse table. Pass the database from `list_clickhouse_tables`. Then
query with `query_clickhouse` using the discovered column names.

| Parameter | Type | Required | Description |
| - | - | - | - |
| `datasourceUid` | `string` | Yes | The UID of the ClickHouse datasource. |
| `table` | `string` | Yes | The table to describe. |
| `database` | `string` | No | Database name. Default `default`. |

**Output:** the column schema for the table.

### `query_clickhouse`

Run a SQL query against a ClickHouse datasource through Grafana. Discover tables and schemas first
with `list_clickhouse_tables` and `describe_clickhouse_table`. Supports ClickHouse macros, including
`$__timeFilter(column)`, `$__from`, `$__to`, `$__interval`, and `${varname}`.

| Parameter | Type | Required | Description |
| - | - | - | - |
| `datasourceUid` | `string` | Yes | The UID of the ClickHouse datasource to query. |
| `query` | `string` | Yes | Raw SQL query. Supports ClickHouse macros for time filtering and variable substitution. |
| `start` | `string` | No | Start time. Relative, RFC3339, or Unix milliseconds. Default one hour ago. |
| `end` | `string` | No | End time. Relative, RFC3339, or Unix milliseconds. Default now. |
| `limit` | `integer` | No | Maximum number of rows to return. Default `100`, maximum `1000`. A `LIMIT` is appended if the query does not contain one. |
| `variables` | `object` | No | Template variable substitutions as key-value pairs, referenced as `${varname}` or `$varname`. |

**Output:** the result rows from the SQL query.

### `search_logs`

Search for log entries matching a text pattern across ClickHouse and log datasources. The tool
generates a backend-specific query based on the datasource type. For ClickHouse, run `list_clickhouse_tables`
first, because the default table may not exist, and the tool expects an OpenTelemetry log schema
with `Timestamp` and `Body` columns.

| Parameter | Type | Required | Description |
| - | - | - | - |
| `datasourceUid` | `string` | Yes | The UID of a ClickHouse or log datasource. |
| `pattern` | `string` | Yes | Text pattern or regular expression to search for in log messages. |
| `start` | `string` | No | Start time. Relative, RFC3339, or Unix milliseconds. Default `now-1h`. |
| `end` | `string` | No | End time. Relative, RFC3339, or Unix milliseconds. Default `now`. |
| `limit` | `integer` | No | Maximum number of log entries to return. Default `100`, maximum `1000`. |
| `table` | `string` | No | Table name for ClickHouse queries. Ignored for log datasources. |

**Output:** a list of matching log entries.

## Dashboards and folders

Find dashboards, inspect them without retrieving the full JSON, read the queries behind their panels,
and build shareable links.

### `search_dashboards`

Search for Grafana dashboards by a query string.

| Parameter | Type | Required | Description |
| - | - | - | - |
| `query` | `string` | No | The query to search for. |
| `limit` | `integer` | No | Maximum number of results to return. Default `50`, maximum `100`. |
| `page` | `integer` | No | Page number, one-indexed. Default `1`. |

**Output:** a list of matching dashboards, each with its title, UID, folder, tags, and URL.

### `get_dashboard_summary`

Get a compact summary of a dashboard without the full JSON. Use it for an overview and to plan
follow-up calls without consuming large amounts of context.

| Parameter | Type | Required | Description |
| - | - | - | - |
| `uid` | `string` | Yes | The UID of the dashboard. |

**Output:** a summary including the title, panel count, panel types, variables, and other metadata.

### `get_dashboard_property`

Get specific parts of a dashboard using a JSONPath expression, to minimize context usage. Common
paths include `$.title`, `$.panels[*].title`, `$.templating.list`, and `$.panels[*].targets[*].expr`.

| Parameter | Type | Required | Description |
| - | - | - | - |
| `uid` | `string` | Yes | The UID of the dashboard. |
| `jsonPath` | `string` | Yes | JSONPath expression to extract specific data. |

**Output:** the values extracted by the JSONPath expression.

### `get_dashboard_panel_queries`

Retrieve the queries behind a dashboard's panels. Supports all datasource types and row-nested
panels. Optionally filter to one panel, and optionally substitute template variables.

| Parameter | Type | Required | Description |
| - | - | - | - |
| `uid` | `string` | Yes | The UID of the dashboard. |
| `panelId` | `integer` | No | Filter to a specific panel by ID. |
| `variables` | `object` | No | Template variable substitutions, such as `{"job": "api-server"}`. Populates `processedQuery` and `requiredVariables`. |

**Output:** an array of objects with `title`, `query` (the raw expression), and `datasource` (an
object with `uid` and `type`). When variables are provided, each object also includes
`processedQuery`, `refId`, and `requiredVariables`.

### `get_dashboard_by_uid`

Retrieve the complete dashboard, including panels, variables, and settings, by UID.

> [!NOTE]
>
> Large dashboards can consume significant context. Prefer `get_dashboard_summary` for an overview
> or `get_dashboard_property` for specific data.

| Parameter | Type | Required | Description |
| - | - | - | - |
| `uid` | `string` | Yes | The UID of the dashboard. |

**Output:** the full dashboard JSON.

### `search_folders`

Search for Grafana folders by a query string.

| Parameter | Type | Required | Description |
| - | - | - | - |
| `query` | `string` | No | The query to search for. |

**Output:** a list of matching folders, each with its title, UID, and URL.

### `generate_deeplink`

Generate a deeplink URL for a Grafana resource. Supports dashboards, panels, and Explore queries.

| Parameter | Type | Required | Description |
| - | - | - | - |
| `resourceType` | `string` | Yes | The type of resource: `dashboard`, `panel`, or `explore`. |
| `dashboardUid` | `string` | No | Dashboard UID. Required for `dashboard` and `panel` types. |
| `panelId` | `integer` | No | Panel ID. Required for the `panel` type. |
| `datasourceUid` | `string` | No | Datasource UID. Required for the `explore` type. |
| `queries` | `array` | No | Query objects for Explore links, such as `[{"refId":"A","expr":"up"}]`. |
| `queryParams` | `object` | No | Additional URL query parameters, for `dashboard` and `panel` types. |
| `timeRange` | `object` | No | Time range with `from` and `to` fields, such as `{"from": "now-1h", "to": "now"}`. |

**Output:** the deeplink URL.

## Documentation

Search and read CoreWeave public documentation so an agent answers product and API questions from
current docs.

### `search_coreweave_docs`

Search the CoreWeave Docs knowledge base for relevant information, code examples, API references,
and guides. Start here for broad or conceptual questions. To read a specific page in full, pass its
path to `query_filesystem_coreweave_docs`.

| Parameter | Type | Required | Description |
| - | - | - | - |
| `query` | `string` | Yes | The query to search the documentation with. |

**Output:** contextual content with titles and direct links to the documentation pages.

### `query_filesystem_coreweave_docs`

Run a read-only, shell-like query against a virtual, in-memory filesystem that contains the
CoreWeave Docs pages and OpenAPI specs. This is a sandbox, not a real shell. It is how you read a
page in full: pass a page's `.mdx` path to `head` or `cat`. Supported commands include `rg`, `grep`,
`find`, `tree`, `ls`, `cat`, `head`, `tail`, `stat`, `wc`, `sort`, `uniq`, `cut`, `sed`, `awk`, and
`jq`. Each call is stateless and starts at the root path.

| Parameter | Type | Required | Description |
| - | - | - | - |
| `command` | `string` | Yes | A shell-like command to run against the documentation filesystem, such as `rg -il "keyword" /`, `tree / -L 2`, or `head -80 /path/file.mdx`. |

**Output:** the command output, truncated to 30 KB per call.

## Billing

Read hourly measured and billable usage for the organization associated with your CoreWeave API
access token. The billing tool requires access to
FOCUS export for your organization. The user or service account associated with your token must
have the [Billing Viewer](https://docs.coreweave.com/security/iam/access-policies/roles.md#billing) role. For the row schema and
API behavior, see [Export usage with the FOCUS API](https://docs.coreweave.com/billing/focus-export-api.md).

### `coreweave_billing_get_focus_usage`

Retrieve one page of usage from `GET /v1/billing/focus` as JSON. This read-only tool returns usage
quantities. It doesn't return cost or dollar amounts. Unlike the raw API, the MCP tool requires
explicit start and end timestamps.

| Parameter | Type | Required | Description |
| - | - | - | - |
| `start_time` | `string` | Yes | Inclusive lower bound for `ChargePeriodStart`, in RFC3339, such as `2026-08-01T00:00:00Z`. |
| `end_time` | `string` | Yes | Exclusive upper bound for `ChargePeriodStart`, in RFC3339. The range can't exceed 90 days. |
| `group_by` | `string` | No | `location` (default) or `capacity_plan`. Location rows are grouped by hour, Availability Zone, cluster, and SKU. Capacity-plan rows are grouped by hour, SKU, and capacity plan. |
| `product_family` | `string` | No | `GPU Compute`, `CPU Compute`, `Storage`, `Network`, or `Other`. |
| `cluster` | `string` | No | Exact `x_ClusterId` to return. Valid only with `group_by=location`. |
| `zone` | `string` | No | `AvailabilityZone` to return, matched case-insensitively. Valid only with `group_by=location`. |
| `page_size` | `integer` | No | Maximum rows per page. Default `100`, range `1` to `1000`. |
| `page_token` | `string` | No | Non-empty `next_page_token` from the preceding call. Repeat the original time range, `group_by`, `product_family`, `cluster`, and `zone`. You can change `page_size`. |

**Output:** a JSON object with `data_generator`, `schema`, `data_as_of`, `query`, `row_count`, and
`data`.

`ConsumedQuantity` is measured usage before exclusions in the location view.
`PricingQuantity` is billable usage after exclusions. In the capacity-plan view, the quantities
are equal.

When more rows match, the result includes `next_page_token` and a `note` explaining how to fetch
the next page. On the final page, `next_page_token` is omitted. An empty page includes a `note`
about the window and filters.

`data_as_of` is the timestamp through which data is complete. Hourly aggregates lag the
underlying data slightly. If you pull the same recent window twice, you may get small differences
until the data settles.

Rate limit errors use the `upstream_error` code. The error message includes `Retry-After`
when the API supplies it.

## Clusters and Nodes

Inspect CoreWeave Kubernetes Service (CKS) clusters and their Nodes. These tools are scoped to what
your CoreWeave API token can access.

### `cw_cluster_get`

List all CoreWeave clusters the caller can see.

This tool takes no parameters.

**Output:** a tabular list of clusters.

### `cw_cluster_describe`

Describe a CoreWeave (CKS) cluster, including its Nodes, Node Pools, data-plane components,
networking, and observability.

| Parameter | Type | Required | Description |
| - | - | - | - |
| `cluster_name` | `string` | Yes | The CKS cluster name. |

**Output:** the cluster description, as tabular text.

### `cw_node_list`

List the Nodes in a CoreWeave (CKS) cluster.

| Parameter | Type | Required | Description |
| - | - | - | - |
| `cluster_name` | `string` | Yes | The CKS cluster name. |

**Output:** a tabular list of Nodes.

### `cw_node_describe`

Describe a Node in a CoreWeave (CKS) cluster, including its instance type, GPU information,
conditions, HPC-verification status, and events.

| Parameter | Type | Required | Description |
| - | - | - | - |
| `cluster_name` | `string` | Yes | The CKS cluster name. |
| `node_id` | `string` | Yes | The Node identifier. |

**Output:** the Node description, as tabular text.

### `cw_node_view`

Return the Grafana dashboard URL for a Node in a CoreWeave (CKS) cluster.

| Parameter | Type | Required | Description |
| - | - | - | - |
| `cluster_name` | `string` | Yes | The CKS cluster name. |
| `node_id` | `string` | Yes | The Node identifier. |

**Output:** the dashboard URL, as plain text.

## CoreWeave SUNK

Inspect CoreWeave SUNK clusters, which run Slurm on Kubernetes on top of a CKS cluster.

### `cw_sunk_describe`

Describe a SUNK cluster running on top of a CoreWeave (CKS) cluster.

| Parameter | Type | Required | Description |
| - | - | - | - |
| `cluster_name` | `string` | Yes | The underlying CKS cluster name, used to select the right access. |
| `sunk_cluster` | `string` | Yes | The SUNK cluster name. |

**Output:** the SUNK cluster description, as tabular text.

### `cw_sunk_view`

Return the Grafana dashboard URL for a SUNK cluster.

| Parameter | Type | Required | Description |
| - | - | - | - |
| `cluster_name` | `string` | Yes | The underlying CKS cluster name, used to select the right access. |
| `sunk_cluster` | `string` | Yes | The SUNK cluster name. |

**Output:** the dashboard URL, as plain text.

## CoreWeave AI Object Storage

Inspect CoreWeave AI Object Storage buckets and the objects within them.

### `cw_cwobject_list`

List CoreWeave AI Object Storage buckets, or list the objects under an `s3://` path.

| Parameter | Type | Required | Description |
| - | - | - | - |
| `s3_path` | `string` | No | An `s3://bucket/prefix` path to list under. Omit to list buckets. |

**Output:** a tabular list of buckets, or of objects under the given path.

### `cw_cwobject_bucket_describe`

Describe a CoreWeave AI Object Storage bucket, including its organization, location, usage, and
audit-logging status.

| Parameter | Type | Required | Description |
| - | - | - | - |
| `bucket_name` | `string` | Yes | The bucket name. |

**Output:** the bucket description, as tabular text.

## Write actions

Write actions run with the authenticated caller's identity and permissions. Unlike the other tool
families, these tools can change CoreWeave resources.

> [!WARNING]
>
> These tools modify resources and can cause destructive changes. They are available only to
> organizations where CoreWeave has enabled write tools. Verify every input before calling them.

### `coreweave_kubectl_apply`

Apply a Kubernetes YAML or JSON manifest to a named CKS cluster by using `kubectl apply` in an
identity-isolated CoreWeave sandbox.

| Parameter | Type | Required | Description |
| - | - | - | - |
| `cluster_name` | `string` | Yes | Exact CKS cluster name. |
| `manifest` | `string` | Yes | Kubernetes YAML or JSON manifest to apply. |
| `dry_run` | `boolean` | No | The tool ignores this parameter and still applies the manifest. |
| `plan_token` | `string` | No | The tool ignores this parameter and still applies the manifest. |

**Output:** a JSON object containing the command exit code, standard output, standard error, and
truncation details.

### `coreweave_inference_update_deployment`

Update selected runtime, instance type, or autoscaling fields on a CoreWeave Inference deployment.
The tool preserves fields that you omit. It reads the current deployment before sending the
complete writable specification to the Inference API.

Parameter names that contain a dot are literal top-level keys, not nested objects. For example,
send `{"id": "[DEPLOYMENT-ID]", "autoscaling.max": 4}`. Supply `id` and at least one field to
update.

| Parameter | Type | Required | Description |
| - | - | - | - |
| `id` | `string` | Yes | Inference deployment ID. |
| `runtime.engine` | `string` | No | Inference runtime engine, such as `vllm`. |
| `runtime.version` | `string` | No | Inference runtime version. |
| `runtime.engineConfig` | `object` | No | Replacement engine-configuration map with `string` values. Include every flag to keep. An empty object clears all engine flags. Omit this parameter to keep the current flags. |
| `resources.instanceType` | `string` | No | CoreWeave instance type used by each deployment replica. |
| `autoscaling.max` | `number` | No | Maximum replica count, expressed as a positive whole number. |
| `autoscaling.concurrency` | `number` | No | Target request concurrency per replica, expressed as a positive whole number. |

**Output:** a JSON object that describes the updated deployment.
