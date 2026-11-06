# Backfill historical logs with LogCLI

Source: https://docs.coreweave.com/observability/logs-metrics/backfill-historical-logs

# Backfill historical logs with LogCLI

> Download historical logs with LogCLI for archiving and backfilling

Use [LogCLI](https://grafana.com/docs/loki/latest/query/logcli/getting-started/), the command-line client for Grafana Loki, to download retained historical logs as a set of part files for archiving or offline analysis. LogCLI splits a time range into smaller queries and downloads them concurrently, which helps with large exports.

> [!NOTE]
>
> On this page, backfill means exporting logs that CoreWeave already stores, not ingesting logs into Loki.

You can export only logs that are still retained in the selected data source. CoreWeave retains CKS audit logs for 3 months, and platform and application logs for 14 days. For the full list, see [Retention limits](https://docs.coreweave.com/observability/service-levels-and-limits.md#retention-limits).

## Prerequisites

Complete the following before you export logs:

* [Install LogCLI](https://grafana.com/docs/loki/latest/query/logcli/getting-started/#install-logcli) version 2.8.0 or later. The examples on this page use the parallel-download flags, which are available in LogCLI 2.8.0 and later. On macOS, you can also install LogCLI with `brew install logcli`.
* Create a [CoreWeave API access token](https://docs.coreweave.com/security/authn-authz/manage-api-access-tokens.md). For read-only access to logs, principals typically need the **Observability Viewer** [IAM role](https://docs.coreweave.com/security/iam/access-policies/roles.md). Assign it to the principal associated with the token.
* Choose the endpoint that stores your logs. For application, platform, and CKS audit log endpoints, see [Logs data locations](https://docs.coreweave.com/observability/logs-metrics/data-sources.md#logs-data-locations).
* Choose a start time and end time in RFC 3339 format, such as `2026-07-16T00:00:00Z`. The start time must be earlier than the end time.

## Configure LogCLI

Set `LOKI_BEARER_TOKEN`, which LogCLI uses to authenticate, and `LOG_EXPORT_DIR`, which the examples use to construct each part-file path. Replace `[API-ACCESS-TOKEN]` with your CoreWeave API access token secret. Replace `[OUTPUT-DIRECTORY]` with the directory where you want LogCLI to save the downloaded part files.

```bash theme={"system"}
export LOKI_BEARER_TOKEN="[API-ACCESS-TOKEN]"
export LOG_EXPORT_DIR="[OUTPUT-DIRECTORY]"
mkdir -p "${LOG_EXPORT_DIR}"
```

The following examples set `LOKI_ADDR` to a Super Regional endpoint. To query another location or log type, select the corresponding endpoint from [Logs data locations](https://docs.coreweave.com/observability/logs-metrics/data-sources.md#logs-data-locations).

## Export CKS audit logs

The following example downloads CKS audit logs for Region `US-EAST-04` from the dedicated US East audit logs endpoint. Replace `[START-TIME]` and `[END-TIME]` with the RFC 3339 boundaries of the time range you want to export.

```bash theme={"system"}
export LOKI_ADDR="https://observe-audit.us-east.coreweave.com"

logcli query \
  --timezone=UTC \
  --from="[START-TIME]" \
  --to="[END-TIME]" \
  --forward \
  --output=raw \
  --part-path-prefix="${LOG_EXPORT_DIR}/us-east-04-audit-logs" \
  --parallel-duration="1m" \
  --parallel-max-workers="4" \
  '{region="US-EAST-04", app="kube-apiserver", stream=""}'
```

This command does the following:

* Splits the requested time range into one-minute jobs.
* Runs up to four download workers concurrently.
* Scans each job forward from older to newer entries.
* Writes each completed job to a separate part file under the specified prefix.
* Writes each audit event as the raw JSON that Loki stores.

## Choose an output format

LogCLI applies `--output` to the part files it writes, so the format you choose is the format you archive. The default output prefixes each line with its labels and timestamp, which isn't machine readable without further processing.

The following table describes the values that `--output` accepts:

| Value | Result | Use for |
| - | - | - |
| `default` | Labels and timestamp, then the log line | Reading logs directly |
| `raw` | The log line only, with no labels or timestamp | Audit logs, which Loki already stores as JSON |
| `jsonl` | One JSON object per line, wrapping labels, timestamp, and the log line | Application logs, when you want to keep metadata |

> [!NOTE]
>
> When you run LogCLI in a terminal, `--output=default` also writes color codes into the part files. To suppress them, redirect LogCLI's output or set the `NO_COLOR` environment variable.

Choose between `raw` and `jsonl` based on whether the log line already carries its own timestamp and identifying fields:

* Use `--output=raw` for audit logs. Each audit event is already JSON and records its own timestamps and request details, so `--output=jsonl` would nest that JSON inside another JSON object.
* Use `--output=jsonl` for application and container logs. These lines are opaque text with no reliable embedded timestamp. The JSON wrapper therefore preserves when each line was written and which pod it came from.

`--output=raw` discards the Loki stream labels, and an audit event doesn't repeat them in its body. The exported events therefore don't record which Region, cluster, or pod they came from. Use `--output=jsonl` when you need to keep that context, or give each export a `--part-path-prefix` that identifies the source.

## Export application logs for a container

The following example downloads logs from a specific container in Region `US-EAST-04`. Replace `[CONTAINER-NAME]`, `[START-TIME]`, and `[END-TIME]` with your container name and time range.

Container names aren't unique across the Region, so this selector matches every container with that name in any cluster or namespace. To export logs from one workload, add `cluster` and `namespace` to the selector.

```bash theme={"system"}
export LOKI_ADDR="https://observe.us-east.coreweave.com"

logcli query \
  --timezone=UTC \
  --from="[START-TIME]" \
  --to="[END-TIME]" \
  --forward \
  --output=jsonl \
  --part-path-prefix="${LOG_EXPORT_DIR}/us-east-04-container-logs-[CONTAINER-NAME]" \
  --parallel-duration="1m" \
  --parallel-max-workers="4" \
  '{region="US-EAST-04", container="[CONTAINER-NAME]"}'
```

This command uses the same parallel-download flags as the audit log example and writes matching container logs to separate part files. It uses `--output=jsonl` rather than `--output=raw` so that each line keeps its labels and timestamp. If your workload already writes structured JSON logs that carry their own timestamp, use `--output=raw` instead to avoid nesting that JSON inside another JSON object.

## Resume an interrupted export

LogCLI skips a time range when it finds the completed part file for that range. If an export stops before it finishes, rerun the same command to download only the missing parts.

> [!WARNING]
>
> Use a unique `--part-path-prefix` for each query. LogCLI names completed part files from the prefix and each job's time range, and it skips matching files without checking the LogQL selector. If you reuse a prefix and time range for a different query, the export omits the new query results for those completed parts. To intentionally download all parts again, add the `--overwrite-completed-parts` flag. For more information, see the [LogCLI query command reference](https://grafana.com/docs/loki/latest/query/logcli/getting-started/#query-command-reference).

## Handle query series limits

A broad audit log query can exceed the limit on the number of unique series a single query may return, which fails the query with an HTTP 400 response. If that happens, divide the query into separate queries by pod.

To list pod names, run the following LogCLI command. It reads the label index instead of scanning logs, so it's faster than a log query and doesn't risk the same series limit:

```bash theme={"system"}
logcli labels pod --from="[START-TIME]" --to="[END-TIME]"
```

This returns every `pod` value on the endpoint for that time range. `logcli labels` doesn't accept a stream selector, so the list isn't restricted to a single Region. For more information, see the [LogCLI labels command reference](https://grafana.com/docs/loki/latest/query/logcli/getting-started/#labels-command-reference).

To list only the pods that produced matching audit logs, run this LogQL metric query in [Grafana Explore](https://docs.coreweave.com/observability/logs-metrics/introduction.md#grafana-explore) instead:

```logql theme={"system"}
sum by (pod) (
  count_over_time(
    {app="kube-apiserver", region="US-EAST-04", stream=""}[7d]
  )
)
```

Then add the `pod` label to the audit log selector. Replace `[POD-NAME]` with one of the pod names returned by the preceding query. Use a unique `--part-path-prefix` for that pod. Run the audit log export once for each pod. The following example sets `LOKI_ADDR` again, but still requires the `LOKI_BEARER_TOKEN` you set in [Configure LogCLI](#configure-logcli):

```bash theme={"system"}
export LOKI_ADDR="https://observe-audit.us-east.coreweave.com"

logcli query \
  --timezone=UTC \
  --from="[START-TIME]" \
  --to="[END-TIME]" \
  --forward \
  --output=raw \
  --part-path-prefix="${LOG_EXPORT_DIR}/us-east-04-audit-logs-[POD-NAME]" \
  --parallel-duration="1m" \
  --parallel-max-workers="4" \
  '{app="kube-apiserver", region="US-EAST-04", stream="", pod="[POD-NAME]"}'
```

Running the export once per pod writes a separate set of part files for each pod.

## See also

* [Retention limits](https://docs.coreweave.com/observability/service-levels-and-limits.md#retention-limits): how long CoreWeave keeps each telemetry type, which determines what you can still export.
* [Configure Telemetry Relay](https://docs.coreweave.com/observability/telemetry-forwarding/configure.md): how to forward telemetry to an external destination when you need retention beyond those limits.
* [Logs data locations](https://docs.coreweave.com/observability/logs-metrics/data-sources.md#logs-data-locations): the full endpoint matrix for application, platform, and CKS audit logs.
