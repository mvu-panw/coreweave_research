# Track user activity with audit logs

Source: https://docs.coreweave.com/products/wandb/platform/hosting/monitoring-usage/audit-logging

# Track user activity with audit logs

> Fetch and analyze Weights & Biases audit logs across deployment types, including the log schema and tracked actions.

Use Weights & Biases audit logs to track user activity within your organization and to conform to your enterprise governance requirements. This page is for organization-level admins who need to access, fetch, and analyze audit log data across Weights & Biases deployment types. Audit logs are available in JSON format. Refer to [Audit log schema](#audit-log-schema).

How you access audit logs depends on your Weights & Biases platform deployment type:

| W\&B Platform deployment type | Audit logs access mechanism |
| - | - |
| [Dedicated Cloud](https://docs.coreweave.com/products/wandb/platform/hosting/hosting-options/dedicated-cloud.md) | <ul><li>[Instance-level BYOB](https://docs.coreweave.com/products/wandb/platform/hosting/data-security/secure-storage-connector.md): Synced to instance-level bucket (BYOB) every 10 minutes. Also available with [the API](#fetch-audit-logs).</li><li>Default instance-level storage: Available only with [the API](#fetch-audit-logs).</li></ul> |
| [Multi-tenant Cloud](https://docs.coreweave.com/products/wandb/platform/hosting/hosting-options/multi_tenant_cloud.md) | Available for Enterprise plans only. Available only with [the API](#fetch-audit-logs). |
| [Self-Managed](https://docs.coreweave.com/products/wandb/platform/hosting/hosting-options/self-managed.md) | Synced to instance-level bucket every 10 minutes. Also available with [the API](#fetch-audit-logs). |

After you fetch audit logs, you can analyze them with tools like [Pandas](https://pandas.pydata.org/docs/index.html), [Amazon Redshift](https://aws.amazon.com/redshift/), [Google BigQuery](https://cloud.google.com/bigquery), or [Microsoft Fabric](https://www.microsoft.com/microsoft-fabric). Some audit log analysis tools don't support JSON. Refer to the documentation for your analysis tool for guidelines and requirements to transform the JSON-formatted audit logs before analysis.

For more details about the format of the logs, see [Audit log schema](#audit-log-schema) and [Actions](#actions).

## Audit log retention

The following recommendations help you retain audit logs to meet your organization's governance and compliance obligations:

* If you must retain audit logs for a specific period of time, Weights & Biases recommends periodically transferring logs to long-term storage, either with storage buckets or the Audit Logging API.
* If you are subject to the [Health Insurance Portability and Accountability Act of 1996 (HIPAA)](https://hhs.gov/hipaa/for-professionals/index.html), you must retain audit logs for a minimum of 6 years in an environment where no internal or external actor can delete or modify them before the end of the mandatory retention period. For HIPAA-compliant [Dedicated Cloud](https://docs.coreweave.com/products/wandb/platform/hosting/hosting-options/dedicated-cloud.md) instances with [BYOB](https://docs.coreweave.com/products/wandb/platform/hosting/data-security/secure-storage-connector.md), you must configure guardrails for your managed storage, including any long-term retention storage.

## Audit log schema

Use this schema to interpret the fields returned in each audit log entry. The following table shows all keys that can appear in an audit log entry, ordered alphabetically. Depending on the action and the circumstances, a specific log entry may include only a subset of the possible fields.

| Key | Definition |
| - | - |
| `action` | The [action](#actions) of the event. |
| `actor_email` | The email address of the user that initiated the action, if applicable. |
| `actor_ip` | The IP address of the user that initiated the action. |
| `actor_user_id` | The ID of the logged-in user who performed the action, if applicable. |
| `artifact_asset` | The artifact ID associated with the action, if applicable. |
| `artifact_digest` | The artifact digest associated with the action, if applicable. |
| `artifact_qualified_name` | The full name of the artifact associated with the action, if applicable. |
| `artifact_sequence_asset` | The artifact sequence ID associated with the action, if applicable. |
| `cli_version` | The version of the Python SDK that initiated the action, if applicable. |
| `entity_asset` | The entity or team ID associated with the action, if applicable. |
| `entity_name` | The entity or team name associated with the action, if applicable. |
| `project_asset` | The project associated with the action, if applicable. |
| `project_name` | The name of the project associated with the action, if applicable. |
| `report_asset` | The report ID associated with the action, if applicable. |
| `report_name` | The name of the report associated with the action, if applicable. |
| `response_code` | The HTTP response code for the action, if applicable. |
| `run_asset` | The run asset associated with the action, if applicable. |
| `run_id` | The ID of the run associated with the action, if applicable. |
| `run_name` | The name of the run associated with the action, if applicable. |
| `run_path` | The full path of the run associated with the action, in the format `entity/project/run_id`, if applicable. |
| `timestamp` | The time of the event in [RFC3339 format](https://www.rfc-editor.org/rfc/rfc3339). For example, `2023-01-23T12:34:56Z` represents January 23, 2023 at 12:34:56 UTC. |
| `user_asset` | The user asset the action impacts (rather than the user performing the action), if applicable. |
| `user_email` | The email address of the user the action impacts (rather than the email address of the user performing the action), if applicable. |

As of W\&B Server v0.85.1, an audit log entry for the single-run `run:delete` action includes fields that identify the deleted run: `run_id`, `run_name`, `run_path`, `entity_name`, and `run_asset`. Previously, `run:delete` entries included only project-level and actor-level fields. Entries for the bulk `run:delete_many` action do not include per-run identifiers.

### Personally identifiable information (PII)

Personally identifiable information (PII), such as email addresses and the names of projects, teams, and reports, is available only with the API endpoint option:

* For [Self-Managed](https://docs.coreweave.com/products/wandb/platform/hosting/hosting-options/self-managed.md) and [Dedicated Cloud](https://docs.coreweave.com/products/wandb/platform/hosting/hosting-options/dedicated-cloud.md), an organization admin can [exclude PII](#exclude-pii) when fetching audit logs.
* For [Multi-tenant Cloud](https://docs.coreweave.com/products/wandb/platform/hosting/hosting-options/multi_tenant_cloud.md), the API endpoint always returns relevant fields for audit logs, including PII. This isn't configurable.

## Before you begin

Before you fetch audit logs, confirm that you meet the following prerequisites for your deployment type:

* Organization-level admins can fetch audit logs. If you receive a `403` error, ensure that you or your service account has adequate permission.
* **Multi-tenant Cloud**: If you're a member of multiple Multi-tenant Cloud organizations, you must configure the **Default API organization**, which determines where audit logging API calls are routed. Otherwise, you receive the following error:

  ```text theme={"system"}
  user is associated with multiple organizations but no valid org ID found in user info
  ```

  To specify your default API organization:

  1. Click the account selector in the upper-right corner, then click **User settings**.
  2. For **Default API organization**, select an organization.

  This doesn't apply to a service account, which can be a member of only one Multi-tenant Cloud organization.

## Fetch audit logs

Use the W\&B Audit Logging API to retrieve audit logs. The endpoint, query parameters, and response format depend on your deployment type.

> [tab] Multi-tenant Cloud
>
> Use this tab for [Multi-tenant Cloud](https://docs.coreweave.com/products/wandb/platform/hosting/hosting-options/multi_tenant_cloud.md). Multi-tenant audit logs are available only for Enterprise plans. The Audit Logging API endpoint is:
>
> ```text theme={"system"}
> https://api.wandb.ai/audit_logs
> ```
>
> The following query parameters are supported:
>
> * `startDate`: The first UTC calendar day in the date range. Use `YYYY-MM-DD` format. If you omit `startDate`, the range starts at midnight UTC today, or `numDays` days before today if you set `numDays`.
> * `numDays`: An integer from `0` through `7`. Weights & Biases fetches logs from `startDate` through the next `numDays` days. If you omit `numDays` or set it to `0`, Weights & Biases fetches logs for one day.
> * `limit`: The maximum number of audit log entries to return. Use a positive integer up to `1,000,000`. The default is `1,000,000`.
> * `cursor`: An opaque cursor from the previous response's `next_cursor` field. Reuse the cursor with the same resolved date range.
>
> The Multi-tenant Cloud endpoint always returns relevant fields for audit logs, including PII. This isn't configurable.
>
> The response is a JSON object with the following fields:
>
> * `audit_logs`: An array of audit log entries. Each entry includes the fields described in [Audit log schema](#audit-log-schema).
> * `range_start_time`: The start of the resolved date range, in UTC.
> * `range_end_time`: The exclusive end of the resolved date range, in UTC.
> * `count`: The number of audit log entries returned in this response.
> * `next_cursor`: An opaque cursor for the next page of results. If this field is `null`, there are no more results for the selected date range.
>
> In the following examples, replace:
>
> * `[BASE64-USERNAME-API-KEY]`: the base64-encoded string in the format `[USERNAME]:[API-KEY]`.
> * `[NEXT-CURSOR]`: the `next_cursor` value from the previous response.
>
> To fetch audit logs for a range, run:
>
> ```bash theme={"system"}
> curl -H "Authorization: Basic [BASE64-USERNAME-API-KEY]" \
>   "https://api.wandb.ai/audit_logs?startDate=2026-08-01&numDays=2&limit=1000"
> ```
>
> The response resembles the following example:
>
> ```json theme={"system"}
> {
>   "audit_logs": [
>     {
>       "action": "project:read",
>       "actor_email": "admin@example.com",
>       ...
>       "timestamp": "2026-08-01T13:12:14Z"
>     }
>   ],
>   "range_start_time": "2026-08-01T00:00:00Z",
>   "range_end_time": "2026-08-04T00:00:00Z",
>   "count": 1,
>   "next_cursor": "eyJyb3dfa2V5Ijoi..."
> }
> ```
>
> To fetch the next page, repeat the request with the same resolved date range. Set `cursor` to the `next_cursor` value from the previous response. Continue until `next_cursor` is `null`.
>
> ```bash theme={"system"}
> curl -H "Authorization: Basic [BASE64-USERNAME-API-KEY]" \
>   "https://api.wandb.ai/audit_logs?startDate=2026-08-01&numDays=2&limit=1000&cursor=[NEXT-CURSOR]"
> ```
>
> 1: On [Multi-tenant Cloud](https://docs.coreweave.com/products/wandb/platform/hosting/hosting-options/multi_tenant_cloud.md), audit logs are not collected for:
>
> * Open or Public projects.
> * The `report:read` action.
> * `User` actions that aren't tied to a specific organization.

> [tab] Dedicated Cloud and Self-Managed
>
> Use this tab for [Dedicated Cloud](https://docs.coreweave.com/products/wandb/platform/hosting/hosting-options/dedicated-cloud.md) or [Self-Managed](https://docs.coreweave.com/products/wandb/platform/hosting/hosting-options/self-managed.md) instances. The Audit Logging API endpoint uses your instance URL:
>
> * Dedicated Cloud: `https://[INSTANCE-NAME].wandb.io/admin/audit_logs`.
> * Self-Managed: `https://[WANDB-PLATFORM-URL]/admin/audit_logs`.
>
> In the following examples, replace:
>
> * `[INSTANCE-NAME]`: your Dedicated Cloud instance name.
> * `[WANDB-PLATFORM-URL]`: the URL of your Self-Managed instance.
> * `[API-ENDPOINT]`: the endpoint for your instance.
> * `[BASE64-USERNAME-API-KEY]`: the base64-encoded string in the format `[USERNAME]:[API-KEY]`.
> * `[NEXT-CURSOR]`: the `next_cursor` value from the previous response.
>
> The following query parameters are supported:
>
> * `anonymize`: If the URL includes `anonymize=true`, Weights & Biases does not add PII fields to the audit logs. Otherwise, PII is included. For more information, see [Exclude PII when fetching audit logs](#exclude-pii).
> * `startDate`: The inclusive start of the date range, in UTC. Supported formats are `YYYY-MM-DD`, `YYYY-MM-DDTHH`, `YYYY-MM-DDTHH:mm`, and `YYYY-MM-DDTHH:mm:ss`. Missing time parts default to zero. For example, `2026-08-03T01` means `2026-08-03T01:00:00Z`. If you omit `startDate`, the range starts at midnight UTC today, or `numDays` days before today if you set `numDays`.
> * `numDays`: A non-negative integer. Weights & Biases fetches logs from `startDate` through the next `numDays` days. If you omit `numDays` or set it to `0`, Weights & Biases fetches logs for the `startDate` day only. You can't use `numDays` with `endDate`.
> * `endDate`: The exclusive end of the date range, in UTC. The supported formats match `startDate`. Setting `endDate` returns a paginated JSON response, even if you don't set `limit`. You can't use `endDate` with `numDays`.
> * `limit`: The maximum number of audit log entries to return in a paginated response. Use a positive integer up to `20,000`. If you set `limit`, Weights & Biases returns a paginated JSON response. In paginated requests, the default is `20,000`.
> * `cursor`: An opaque cursor from the previous response's `next_cursor` field. Reuse the cursor with the same resolved date range and `anonymize` value. If you set `cursor`, you must also set `limit` or `endDate`.
>
> If you don't set `limit` or `endDate`, the API preserves the original streaming response format. The response contains newline-separated JSON objects. Each object includes the fields described in [Audit log schema](#audit-log-schema), the same as logs synced to an instance-level bucket.
>
> To fetch a streaming newline-separated JSON response for a three-day range and exclude PII, run:
>
> ```bash theme={"system"}
> curl -H "Authorization: Basic [BASE64-USERNAME-API-KEY]" \
>   "[API-ENDPOINT]?startDate=2026-08-01&numDays=2&anonymize=true"
> ```
>
> If you set `limit` or `endDate`, the API returns a JSON object with the following fields:
>
> * `audit_logs`: An array of audit log entries. Each entry includes the fields described in [Audit log schema](#audit-log-schema).
> * `range_start_time`: The start of the resolved date range, in UTC.
> * `range_end_time`: The exclusive end of the resolved date range, in UTC.
> * `count`: The number of audit log entries returned in this response.
> * `next_cursor`: An opaque cursor for the next page of results. If this field is `null`, there are no more results for the selected date range.
>
> To fetch a paginated response for a two-hour range, run:
>
> ```bash theme={"system"}
> curl -H "Authorization: Basic [BASE64-USERNAME-API-KEY]" \
>   "[API-ENDPOINT]?startDate=2026-08-01T13:00&endDate=2026-08-01T15:00&limit=1000"
> ```
>
> The response resembles the following example:
>
> ```json theme={"system"}
> {
>   "audit_logs": [
>     {
>       "action": "project:read",
>       "actor_email": "admin@example.com",
>       ...
>       "timestamp": "2026-08-01T14:00:00Z",
>     }
>   ],
>   "range_start_time": "2026-08-01T13:00:00Z",
>   "range_end_time": "2026-08-01T15:00:00Z",
>   "count": 1,
>   "next_cursor": "eyJ2ZXJzaW9uIjox..."
> }
> ```
>
> To fetch the next page, repeat the request with the same resolved date range and `anonymize` value. Set `cursor` to the `next_cursor` value from the previous response. Continue until `next_cursor` is `null`.
>
> ```bash theme={"system"}
> curl -H "Authorization: Basic [BASE64-USERNAME-API-KEY]" \
>   "[API-ENDPOINT]?startDate=2026-08-01T13:00&endDate=2026-08-01T15:00&limit=1000&cursor=[NEXT-CURSOR]"
> ```
>
> ### Exclude PII when fetching audit logs
>
> For [Self-Managed](https://docs.coreweave.com/products/wandb/platform/hosting/hosting-options/self-managed.md) and [Dedicated Cloud](https://docs.coreweave.com/products/wandb/platform/hosting/hosting-options/dedicated-cloud.md), a Weights & Biases organization or instance admin can exclude PII when fetching audit logs. For [Multi-tenant Cloud](https://docs.coreweave.com/products/wandb/platform/hosting/hosting-options/multi_tenant_cloud.md), the API endpoint always returns relevant fields for audit logs, including PII. This isn't configurable.
>
> To exclude PII, pass the `anonymize=true` URL parameter. For example, to get audit logs for user activity within the last week and exclude PII, if your Weights & Biases instance URL is `https://mycompany.wandb.io`, use an API endpoint like:
>
> ```text theme={"system"}
> https://mycompany.wandb.io/admin/audit_logs?anonymize=true&[ADDITIONAL-PARAMETERS].
> ```

### Use basic authentication

You must authenticate each request to the audit logs API. To use basic authentication with your API key to access the audit logs API, set the HTTP request's `Authorization` header to the string `Basic` followed by a space, then the base64-encoded string in the format `[USERNAME]:[API-KEY]`. In other words, replace the username and API key with your values separated with a `:` character, then base64-encode the result. For example, to authorize as `demo:p@55w0rd`, set the header to `Authorization: Basic ZGVtbzpwQDU1dzByZA==`.

## Actions

Each audit log entry records one of the following actions. Use this reference to interpret the `action` field in a log entry. The following table describes possible actions that Weights & Biases can record, sorted alphabetically.

| Action | Definition |
| - | - |
| `artifact:create` | Artifact is created. |
| `artifact:delete` | Artifact is deleted. |
| `artifact:read` | Artifact is read. |
| `project:delete` | Project is deleted. |
| `organization:update_member` | Member's organization role or seat is updated. |
| `project:read` | Project is read. |
| `report:read` | Report is read. <sup>[1](#1)</sup> |
| `run:delete_many` | Batch of runs is deleted. |
| `run:delete` | Run is deleted. |
| `run:stop` | Run is stopped. |
| `run:undelete_many` | Batch of runs is restored from trash. |
| `run:update_many` | Batch of runs is updated. |
| `run:update` | Run is updated. |
| `sweep:create_agent` | Sweep agent is created. |
| `team:create_service_account` | Service account is created for the team. |
| `team:create` | Team is created. |
| `team:delete` | Team is deleted. |
| `team:invite_user` | User is invited to team. |
| `team:uninvite` | User or service account is uninvited from team. |
| `user:create_api_key` | API key for the user or service account is created. <sup>[1](#1)</sup> |
| `user:create` | User is created. <sup>[1](#1)</sup> |
| `user:deactivate` | User is deactivated. <sup>[1](#1)</sup> |
| `user:delete_api_key` | API key for the user or service account is deleted. <sup>[1](#1)</sup> |
| `user:initiate_login` | User initiates log in. <sup>[1](#1)</sup> |
| `user:login` | User logs in. <sup>[1](#1)</sup> |
| `user:logout` | User logs out. <sup>[1](#1)</sup> |
| `user:permanently_delete` | User is permanently deleted. <sup>[1](#1)</sup> |
| `user:reactivate` | User is reactivated. <sup>[1](#1)</sup> |
| `user:read` | User profile is read. <sup>[1](#1)</sup> |
| `user:update` | User is updated. <sup>[1](#1)</sup> |
