# Limits and quotas

Source: https://docs.coreweave.com/products/sandboxes/reference/limits-and-quotas

# Limits and quotas

> Plan sandbox concurrency and resources, understand lifetime limits, and handle quota errors.

CoreWeave sandboxes have limits on concurrent usage, create requests, resources, and lifetime. Use this page to plan your workload and respond when a request reaches a limit. Concurrent sandbox quotas apply to serverless placement. Sandboxes on your own CoreWeave Kubernetes Service (CKS) cluster don't count toward them.

## Concurrent sandbox quota

A concurrent sandbox quota limits the number of active serverless sandboxes in your organization, shared across users and API keys. Active usage includes sandboxes that are starting or shutting down, as well as those running your code.

The following defaults apply when concurrent quota enforcement is enabled. Contact support or your account team to confirm the quota and enforcement status for your organization.

| Account type | Default concurrent sandboxes |
| :- | -: |
| Forge Free, Academic, or Free Trial | 20 |
| Forge Pro | 2,000 |
| Forge Enterprise | 5,000 |
| Other Forge accounts | 10 |
| CoreWeave | 5,000 |

The sandbox credential determines the account that owns the sandbox. See [Choose and get credentials](https://docs.coreweave.com/products/sandboxes/placement.md#choose-and-get-credentials). These quotas apply to accounts with sandbox access. An approved quota increase can raise your organization's limit. If your Forge account type is unavailable or unrecognized, a previously recognized tier takes precedence over the fallback in the table.

The quota check applies to new serverless create requests through the v1 API. Usage from the deprecated v1beta2 API also counts, but v1beta2 create requests aren't subject to this check. When you integrate quota handling, use the current v1 API.

Quota accounting updates asynchronously. Usage can temporarily exceed the quota, and recently ended sandboxes can take time to stop counting. A concurrent quota isn't a strict spending cap or a guarantee of available capacity.

### Usage counted toward the quota

The quota accounts for the following usage:

* Sandboxes preparing, waiting for placement, starting, running, or shutting down.
* Reservations for create requests whose outcome is uncertain, such as a timeout after placement starts.

For normal shutdowns, a slot becomes available after the sandbox reaches a terminal state and quota accounting refreshes. Sending a stop or delete request doesn't immediately free a slot.

A create request with an uncertain outcome can reserve a slot even if it returns an error. The reservation lasts for the lifetime specified in the request plus a 60-second allowance, measured from when the failure is recorded. If the lifetime is unknown, the reservation uses 30 days plus that allowance. Stopping or deleting the sandbox doesn't release this reservation early. If reservations prevent you from creating more sandboxes, contact support or your account team.

### Handle a quota error

When enforcement is enabled, the quota check determines whether your organization has reached its limit. If so, the platform rejects a new v1 serverless create request with the following error details:

| Field | Value |
| :- | :- |
| HTTP status | `429 Too Many Requests` |
| gRPC code | `RESOURCE_EXHAUSTED` |
| Error reason | `CWSANDBOX_OCCUPANCY_QUOTA_EXCEEDED` |
| Error metadata | `scope`: `tenant`, `limit`: the effective quota, `current`: the usage counted by the quota check |
| Retry hint | `RetryInfo` with a delay of 5 seconds |

The platform returns the following error message:

> concurrent sandbox quota exceeded; request an increase from [support@wandb.ai](mailto:support@wandb.ai) or your account team

Handle the structured error reason rather than matching the message text. Wait for capacity in your quota, then retry with backoff and respect the retry hint. The 5-second hint isn't a promise that a slot will be available after 5 seconds.

Concurrent quota enforcement doesn't stop sandboxes that are already running, including after a tier change reduces the quota. Other controls, including sandbox lifetime, still apply.

### Request a quota increase

To request a higher concurrent quota, contact the team for your account:

* CoreWeave customers: contact your account team.
* Forge customers: email [forge-support@coreweave.com](mailto:forge-support@coreweave.com) or contact your account team.

Include your organization, current quota, requested quota, and expected peak concurrency. An approved increase applies to the organization, across its users and API keys.

## Rate limits

The v1 serverless API also limits how quickly your organization sends create requests and how many create requests it has in progress. These limits are separate from the number of active sandboxes.

A throttled create request returns HTTP `429` with error reason `CWSANDBOX_SERVERLESS_CREATE_THROTTLED`. The `limit_kind` metadata identifies the limit:

| Limit kind | Action |
| :- | :- |
| `rate` | Reduce the rate of create requests. |
| `concurrency` | Reduce the number of create requests in progress at the same time. |

Retry with backoff and respect any retry hint in the response. A higher concurrent sandbox quota doesn't itself increase the rate limits on create requests.

## Sandbox lifetime

To limit how long a sandbox can run, set the [`max_lifetime_seconds` parameter](https://docs.coreweave.com/products/sandboxes/client/guides/sandbox-configuration#max_lifetime_seconds) when you create it. Lifetime limits apply to both serverless and CKS placement.

If you omit the lifetime, the applicable policy can supply a default. The platform uses 10 minutes when no policy default is set.

| Setting | Value |
| :- | -: |
| Platform fallback when neither the request nor its policy specifies a lifetime | 600 seconds (10 minutes) |
| Maximum | 2,592,000 seconds (30 days) |

The platform rejects a create request that specifies more than the maximum lifetime. The platform stops the sandbox when its lifetime expires. Choose a lifetime that covers the work you need to run, and stop the sandbox when the work finishes.

## Per-sandbox resources

Resource limits depend on the policy governing the sandbox's placement. CoreWeave manages the policy for serverless capacity. Your administrators configure it for CKS placement. Policies can restrict CPU and memory per container and across the sandbox, as well as GPU requests. A request must satisfy the applicable policy and fit available capacity. For resource constraints, see the [policy reference](https://docs.coreweave.com/products/sandboxes/reference/profile.md).

Your organization must be allowlisted to use GPUs. A concurrent sandbox quota doesn't grant GPU access. Each sandbox can request up to your organization's maximum number of GPUs per sandbox, which defaults to 1. Serverless capacity supports only 1 GPU per sandbox. To request a higher maximum for CKS placement, contact support or your account team. For access requirements and supported configurations, see [Run a GPU sandbox](https://docs.coreweave.com/products/sandboxes/gpu-sandboxes.md).

For [placement modes](https://docs.coreweave.com/products/sandboxes/placement.md#select-a-placement-mode) and [credentials](https://docs.coreweave.com/products/sandboxes/placement.md#choose-and-get-credentials), see Sandbox placement and spillover. For resource request examples, see [Get started with CoreWeave Sandboxes](https://docs.coreweave.com/products/sandboxes/get-started.md).
