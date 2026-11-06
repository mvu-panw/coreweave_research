# Export usage with the FOCUS API

Source: https://docs.coreweave.com/billing/focus-export-api

# Export usage with the FOCUS API

> Pull hourly CoreWeave usage in FOCUS JSON or CSV format (Public Preview)

The FOCUS Billing Export API lets you pull your CoreWeave usage data in [FinOps Open Cost and Usage Specification (FOCUS)](https://focus.finops.org/) format. Use it to load CoreWeave usage into a data warehouse or FinOps tool alongside exports from other cloud providers.

This page shows you how to make a request, set query parameters, and interpret the JSON or CSV response.

The API returns the same billable usage you see in [Billing insights](https://docs.coreweave.com/billing/billing-insights.md), at hourly grain, as JSON or CSV.

> [!WARNING]
>
> The FOCUS Billing Export API is in public preview. Schema details and behavior may change before general availability. If you receive unexpected values, numbers that don't reconcile with [Billing insights](https://docs.coreweave.com/billing/billing-insights.md), errors, or slow responses, [contact Support](https://docs.coreweave.com/support.md).
>
> In this public preview, the FOCUS Billing Export API returns usage for [CoreWeave Kubernetes Service (CKS)](https://docs.coreweave.com/products/cks.md) only.

## Scope

This public preview includes the following:

* Usage quantities at hourly grain (for example, GPU-hours, GiB-hours, and IP-hours)
* Filters for time range, product family, cluster, and zone
* JSON and CSV response formats
* Pagination for large results

This public preview doesn't include the following:

* Cost or dollar amounts. This release returns usage quantities only. Cost fields such as billed or effective cost are planned for a later release on the same schema.
* Project-level attribution or resource tags.
* Per-resource or per-node rows. Usage is aggregated. See [Data grain](#data-grain).

The following FOCUS fields are `null` in this release: `ChargeClass`, `ChargeDescription`, and `ResourceType`.

## Prerequisites

Before you call the API, make sure you have the following:

* A [CoreWeave API access token](https://docs.coreweave.com/security/authn-authz/manage-api-access-tokens.md#create-a-new-api-access-token) associated with a user or service account that has the [Billing Viewer](https://docs.coreweave.com/security/iam/access-policies/roles.md#billing) role. Store the token securely.
* FOCUS export enabled for your organization. If you receive a `403 Forbidden` response after assigning the Billing Viewer role, [contact Support](https://docs.coreweave.com/support.md) to request access.

The token is scoped to your organization, so you don't pass an organization identifier in the request. The API returns results for the account associated with the token.

## Make your first request

The export endpoint is:

```text theme={"system"}
GET https://api.coreweave.com/v1/billing/focus
```

To confirm access and inspect the response shape, send a request to the export endpoint. This default example without any parameters returns the last seven days of usage grouped by location, as JSON.

In the `Authorization` header, pass your token. Replace `[API-ACCESS-TOKEN]` with your CoreWeave API access token:

```bash theme={"system"}
export CW_FOCUS_TOKEN="[API-ACCESS-TOKEN]"

curl -sS \
  -H "Authorization: Bearer $CW_FOCUS_TOKEN" \
  "https://api.coreweave.com/v1/billing/focus"
```

The following example requests a specific month, groups by capacity plan, and saves CSV output to a file:

```bash theme={"system"}
curl -sS -G "https://api.coreweave.com/v1/billing/focus" \
  -H "Authorization: Bearer $CW_FOCUS_TOKEN" \
  --data-urlencode "start_time=2026-07-01T00:00:00Z" \
  --data-urlencode "end_time=2026-08-01T00:00:00Z" \
  --data-urlencode "group_by=capacity_plan" \
  --data-urlencode "format=csv" \
  -o coreweave-focus-2026-07.csv
```

A successful request returns FOCUS usage rows for the window you requested.

## Query parameters

All parameters are optional. Times use ISO 8601 in UTC.

| Parameter | Type | Default | Notes |
| - | - | - | - |
| `start_time` | ISO 8601 (UTC) | Now minus 7 days, top of the hour | Inclusive lower bound for `ChargePeriodStart`. |
| `end_time` | ISO 8601 (UTC) | Now, top of the hour | Exclusive upper bound for `ChargePeriodStart`. Must be after `start_time`. |
| `group_by` | `enum` | `location` | `location` or `capacity_plan`. See [Data grain](#data-grain). |
| `product_family` | `enum` | all | One of `GPU Compute`, `CPU Compute`, `Storage`, `Network`, or `Other`. |
| `cluster` | `string` | all | Matches `x_ClusterId`. Valid only with `group_by=location`. |
| `zone` | `string` | all | Matches `AvailabilityZone` case-insensitively (for example, `us-east-01a`). Valid only with `group_by=location`. |
| `format` | `enum` | `json` | `json` or `csv`. |
| `page_size` | `integer` (1 to 1,000) | `100` | Rows per page. The API clamps values outside the range to `[1, 1000]`. |
| `page_token` | `string` | (first page) | Cursor for the next page. See [Pagination](#pagination). |

The following constraints apply:

* The time range can't exceed 90 days per request.
* Historical data begins with the January 2026 invoice month, at `2025-12-31T22:00:00Z` (5:00 PM ET). Earlier window bounds are clamped to that timestamp. A window entirely before it returns an empty page.

## Response

A successful response includes metadata and usage rows as JSON. When you set `format=csv`, the response is a CSV file. The following sections describe the JSON envelope, the row schema, data grain, and pagination.

### JSON envelope

A successful JSON response has this shape:

```json theme={"system"}
{
  "data_as_of": "2026-08-25T15:00:00Z",
  "query": {
    "start_time": "2026-07-01T00:00:00Z",
    "end_time": "2026-08-01T00:00:00Z",
    "group_by": "capacity_plan",
    "product_family": null,
    "cluster": null,
    "zone": null,
    "format": "json"
  },
  "next_page_token": "",
  "data_generator": {
    "DataGenerator": "CoreWeave"
  },
  "schema": {
    "SchemaId": "25388bec-b197-406f-ba22-b13e3afd9495",
    "FocusVersion": "1.0",
    "CreationDate": "2026-09-24T00:00:00Z",
    "ColumnDefinition": [
      {"ColumnName": "AvailabilityZone", "DataType": "STRING"},
      {"ColumnName": "BillingAccountId", "DataType": "STRING"},
      {"ColumnName": "BillingAccountName", "DataType": "STRING"},
      {"ColumnName": "BillingPeriodEnd", "DataType": "DATETIME"},
      {"ColumnName": "BillingPeriodStart", "DataType": "DATETIME"},
      {"ColumnName": "ChargeCategory", "DataType": "STRING"},
      {"ColumnName": "ChargeClass", "DataType": "STRING"},
      {"ColumnName": "ChargeDescription", "DataType": "STRING"},
      {"ColumnName": "ChargeFrequency", "DataType": "STRING"},
      {"ColumnName": "ChargePeriodEnd", "DataType": "DATETIME"},
      {"ColumnName": "ChargePeriodStart", "DataType": "DATETIME"},
      {"ColumnName": "ConsumedQuantity", "DataType": "DECIMAL"},
      {"ColumnName": "ConsumedUnit", "DataType": "STRING"},
      {"ColumnName": "InvoiceIssuerName", "DataType": "STRING"},
      {"ColumnName": "PricingCategory", "DataType": "STRING"},
      {"ColumnName": "PricingQuantity", "DataType": "DECIMAL"},
      {"ColumnName": "PricingUnit", "DataType": "STRING"},
      {"ColumnName": "ProviderName", "DataType": "STRING"},
      {"ColumnName": "PublisherName", "DataType": "STRING"},
      {"ColumnName": "RegionId", "DataType": "STRING"},
      {"ColumnName": "RegionName", "DataType": "STRING"},
      {"ColumnName": "ResourceType", "DataType": "STRING"},
      {"ColumnName": "ServiceCategory", "DataType": "STRING"},
      {"ColumnName": "ServiceName", "DataType": "STRING"},
      {"ColumnName": "SkuId", "DataType": "STRING"},
      {"ColumnName": "x_CapacityPlan", "DataType": "STRING"},
      {"ColumnName": "x_ClusterId", "DataType": "STRING"},
      {"ColumnName": "x_ClusterName", "DataType": "STRING"},
      {"ColumnName": "x_ProductFamily", "DataType": "STRING"}
    ]
  },
  "data": []
}
```

| Field | Description |
| - | - |
| `data_generator` | Producer metadata. `DataGenerator` is `CoreWeave`. |
| `schema` | Row-schema metadata: `SchemaId`, `FocusVersion`, `CreationDate`, and `ColumnDefinition`. Each column definition has `ColumnName` and `DataType`. The schema ID and creation date change when the row structure changes. |
| `data_as_of` | The timestamp through which data is complete. Hourly aggregates lag the underlying data slightly. If you pull the same recent window twice, you may get small differences until the data settles. |
| `query` | The effective parameters after defaults and validation. Unset filters echo as `null`. `group_by` always shows the active view. |
| `next_page_token` | Non-empty when more pages exist. An empty string on the final page. See [Pagination](#pagination). |
| `data` | The usage rows. |

### Row schema

Each row is one hourly usage bucket. Columns follow FOCUS 1.0 naming. CoreWeave-specific columns use the `x_` prefix per the FOCUS convention. The `schema` object identifies the row schema and column types.

| Column | Meaning |
| - | - |
| `BillingAccountId` / `BillingAccountName` | Your CoreWeave organization ID / name. |
| `BillingPeriodStart` / `BillingPeriodEnd` | The monthly invoice period this usage falls in (UTC). CoreWeave's invoice boundary is 5:00 PM ET on the last day of the month. |
| `ChargePeriodStart` / `ChargePeriodEnd` | The hourly usage window, `[start, end)`, aligned to the top of the hour in UTC. |
| `ChargeCategory` | `Usage` for all rows in this release. |
| `ChargeClass` | `null` in this release. |
| `ChargeDescription` | `null` in this release. |
| `ChargeFrequency` | `Usage-Based` for all rows in this release. |
| `ConsumedQuantity` | Measured usage before exclusions in the location view. In the capacity-plan view, this equals `PricingQuantity`. |
| `ConsumedUnit` | The unit for `ConsumedQuantity`, which is the same as `PricingUnit`. |
| `PricingQuantity` | Billable usage in this bucket for the hour, summed across all nodes and resources, after exclusions. |
| `PricingUnit` | The unit for `PricingQuantity`: `GPU-Hours`, `vCPU-Hours`, `GiB-Hours`, `IP-Hours`, or `Instance-Hours`, based on the SKU unit type. |
| `PricingCategory` | Rate class derived from capacity plan: `Standard` (`On-Demand`), `Committed` (`Reservation` and `Flex-Usage`), or `Dynamic` (`Spot`). `null` in the location view. |
| `ServiceCategory` / `ServiceName` | For example, `Compute` / `GPU Compute`, or `Storage` / `Object Storage`. |
| `SkuId` | The CoreWeave SKU (for example, `gd-8xh100ib-i128`). |
| `AvailabilityZone` | Availability Zone identifier, such as `us-east-04a`. `null` in the `capacity_plan` view. |
| `RegionId` | Region identifier, such as `us-east-04`. `null` in the `capacity_plan` view. |
| `RegionName` | Region display name, such as `United States (us-east-04)`. May contain only the region identifier. `null` in the `capacity_plan` view. |
| `ResourceType` | `null` in this release. |
| `InvoiceIssuerName` / `ProviderName` / `PublisherName` | Constants: `CoreWeave, Inc.` / `CoreWeave` / `CoreWeave`. |
| `x_CapacityPlan` | CoreWeave extension: `On-Demand`, `Reservation`, `Spot`, or `Flex-Usage`. `null` in the location view. |
| `x_ClusterId` / `x_ClusterName` | CoreWeave extension: cluster identifier / name. `null` in the `capacity_plan` view. |
| `x_ProductFamily` | CoreWeave extension: `GPU Compute`, `CPU Compute`, `Storage`, `Network`, or `Other`. |

Some fields may be `null` during the public preview. If a field you need is empty, [contact Support](https://docs.coreweave.com/support.md).

### Data grain

The API offers the following mutually exclusive views. Use `group_by` to select one:

* `group_by=location` (default): one row per `(hour, zone, cluster, SKU)`. Location is a physical property of the usage. `x_CapacityPlan` and `PricingCategory` are `null` in this view.
* `group_by=capacity_plan`: one row per `(hour, SKU, capacity plan)`. Capacity plan (`On-Demand`, `Reservation`, `Spot`, or `Flex-Usage`) is a rating-time property of your organization's usage. It can't be tied to a specific location, so `AvailabilityZone`, `RegionId`, `RegionName`, `x_ClusterId`, and `x_ClusterName` are `null` in this view.

Usage quantities are summed across all nodes and resources in the bucket. The API never emits per-node rows.

The two views are pivots of the same underlying usage. For any given hour and SKU, the total `PricingQuantity` is identical across both views.

### Pagination

The API paginates results (default 100 rows per page, maximum 1,000). A non-empty `next_page_token` means more data exists. Pass that value back as `page_token` until the token is empty.

Keep the original time range, grouping, and filters unchanged between pages. You can change `page_size` or `format`. Use explicit timestamps while paging so the default time window doesn't move between requests.

To fetch the next page:

* Replace `[PAGE-TOKEN]` with the `next_page_token` value from the previous response.

```bash theme={"system"}
curl -sS -G "https://api.coreweave.com/v1/billing/focus" \
  -H "Authorization: Bearer $CW_FOCUS_TOKEN" \
  --data-urlencode "start_time=2026-07-01T00:00:00Z" \
  --data-urlencode "end_time=2026-08-01T00:00:00Z" \
  --data-urlencode "group_by=capacity_plan" \
  --data-urlencode "format=json" \
  --data-urlencode "page_size=1000" \
  --data-urlencode "page_token=[PAGE-TOKEN]"
```

The API returns response metadata in different locations for JSON and CSV:

| Metadata | JSON | CSV |
| - | - | - |
| Next page token | `next_page_token` in the response body. An empty string indicates the final page. | `X-Next-Page-Token` response header. |
| Page size | Not returned separately. | `X-Page-Size` response header. |
| Schema ID | `schema.SchemaId` in the response body and the `X-FOCUS-Schema-Id` response header. | `X-FOCUS-Schema-Id` response header. |
| Data completeness | `data_as_of` in the response body. | `X-Data-As-Of` response header. The header is omitted when freshness is unavailable. |

## CSV format

When you set `format=csv`, the API returns the following:

* The response `Content-Type` is `text/csv; charset=utf-8`, delivered as a file attachment.
* The first row is a header that uses exact FOCUS column names. All columns appear in both views. Columns that don't apply to the active view are left empty (not omitted), so the layout is stable.
* Fields that contain commas, quotes, or newlines are double-quoted per RFC 4180.

## Errors

The following example shows a JSON error response:

```json theme={"system"}
{
  "error": "[ERROR-CODE]",
  "message": "[HUMAN-READABLE-EXPLANATION]"
}
```

| HTTP status | `error` | When |
| - | - | - |
| `400 Bad Request` | `invalid_parameter` | Unparseable dates, `start_time` greater than or equal to `end_time`, range greater than 90 days, invalid `group_by`, or a `cluster` or `zone` filter used with `group_by=capacity_plan`. |
| `401 Unauthorized` | `unauthorized` | Missing or invalid API token. |
| `403 Forbidden` | `forbidden` | The user or service account associated with the token doesn't have the [Billing Viewer](https://docs.coreweave.com/security/iam/access-policies/roles.md#billing) role, or FOCUS isn't enabled for your organization. If you receive this response after assigning the role, [contact Support](https://docs.coreweave.com/support.md) to request access. The response may be plain text. |
| `405 Method Not Allowed` | `method_not_allowed` | The API supports only `GET`. |
| `429 Too Many Requests` | `rate_limited` | Per-organization rate limit exceeded. Wait for the interval in the `Retry-After` header before retrying. |

## Related resources

For more information about billing usage and API access, see the following resources:

* [Billing insights](https://docs.coreweave.com/billing/billing-insights.md): View the same billable usage in the Cloud Console.
* [Manage API access tokens](https://docs.coreweave.com/security/authn-authz/manage-api-access-tokens.md): Create and manage tokens for API authentication.
* [Usage by Product and Zone](https://docs.coreweave.com/observability/managed-grafana/cost-usage/usage-product-zone.md): Grafana dashboards for cost and usage monitoring.
* [FOCUS](https://focus.finops.org/): The FinOps Open Cost and Usage Specification.
