# NetworkConfig API

Source: https://docs.coreweave.com/products/sandboxes/reference/network-configs

# NetworkConfig API

> NetworkConfig operations, fields, update masks, lifecycle, and errors for dynamic sandbox network policies.

`NetworkConfigService` manages organization-scoped network configurations for CoreWeave Sandboxes. Each configuration holds desired `NetworkOptions` and can bind to one non-terminal sandbox. Updating a bound configuration applies the rules to that sandbox without restarting it. For a walkthrough, see [Change network access on a running sandbox](https://docs.coreweave.com/products/sandboxes/dynamic-network-policies.md).

## Availability and prerequisites

`NetworkConfigService` requires `NetworkConfig` support to be enabled on the API serving your organization. When this support isn't enabled, its remote procedure calls (RPCs) return `UNIMPLEMENTED` with reason `CWSANDBOX_NOT_IMPLEMENTED`. Live updates also require live network updates to be enabled on the runner. For serverless sandboxes, CoreWeave manages these settings. For a CoreWeave Kubernetes Service (CKS) managed runner, set `spec.overrides.env.ENABLE_LIVE_NETWORK_UPDATE` to the string `"true"`. See [Manage runners](https://docs.coreweave.com/products/sandboxes/operations/managed-runners.md). If live updates aren't enabled on the runner, `UpdateNetworkConfig` returns `FAILED_PRECONDITION` with reason `CWSANDBOX_INVALID_REQUEST`.

HTTPS hostname updates also require a runner with HTTPS hostname support and a sandbox created with at least one `httpsHostname` grant. See [Supported changes and limits](https://docs.coreweave.com/products/sandboxes/dynamic-network-policies.md#supported-changes-and-limits).

## Operations and authentication

The service is hosted at `https://api.cwsandbox.com`. Requests require a bearer token with `sandbox_user` permission and access to the configuration's organization. Bound updates also require access to the sandbox.

| Remote procedure call (RPC) | HTTP annotation | Result |
| - | - | - |
| `CreateNetworkConfig` | `POST /v1/networkConfigs` | Creates a caller-owned configuration and returns it. |
| `GetNetworkConfig` | `GET /v1/networkConfigs/{networkConfigId}` | Returns the desired configuration and status. |
| `ListNetworkConfigs` | `GET /v1/networkConfigs` | Returns `networkConfigs` and an optional `nextPageToken`. |
| `UpdateNetworkConfig` | `PATCH /v1/networkConfigs/{networkConfigId}` | Applies an update mask and returns the configuration. |
| `DeleteNetworkConfig` | `DELETE /v1/networkConfigs/{networkConfigId}` | Deletes an unused configuration and returns an empty response. |

For JSON over Connect, send `POST` to `/coreweave.sandbox.v1.NetworkConfigService/[RPC-NAME]` with the full request message, `Content-Type: application/json`, and `Connect-Protocol-Version: 1`. Replace `[RPC-NAME]` with a method from the table. The REST create and update bindings instead accept the `NetworkConfig` resource as the body. Request options such as `updateMask` are query parameters. For generated clients, see [Protobuf](https://docs.coreweave.com/products/sandboxes/reference/protos.md).

`NetworkConfigService` is separate from the unavailable `NetworkService`, which concerns shared sandbox networks.

## Resource fields

Field names in the following table use JSON camelCase. Protobuf fields use snake\_case.

| Field | Meaning |
| - | - |
| `networkConfigId` | Immutable, organization-unique ID matching `^[a-z][a-z0-9-]{2,62}$`. Caller-chosen IDs must not start with the reserved `nc-` prefix. |
| `spec` | Desired `NetworkOptions`: `egress`, `ingress`, `denyEgress`, `denyIngress`, and `dnsEgress`. |
| `etag` | Optional concurrency token for desired-state writes. Send the last returned value in the update resource to reject a stale write. A bound update that reapplies unchanged desired rules doesn't check the token. Omitting it permits the last persisted write to win. |
| `status.sandboxId` | Last bound sandbox. Can briefly name a terminal sandbox until cleanup completes. |
| `status.platformManaged` | Whether the platform created the configuration automatically for a sandbox. |
| `status.createTime`, `status.updateTime` | Output-only creation and update timestamps. |

Create accepts an optional `requestId`. List accepts `pageSize`, `pageToken`, and an optional `platformManaged` boolean filter. Omit the filter for both ownership types. Delete accepts `allowMissing: true` to succeed when the ID is absent.

### Sandbox and template fields

`SandboxSpec.networkConfigId` is optional on creation and immutable afterward. With no ID, the platform creates a configuration from the optional write-only `SandboxSpec.network` input, or from empty rules that resolve to policy defaults. Sending both fields is invalid.

Sandbox Get and List responses expose the bound `networkConfigId` and omit inline `network`. Read `NetworkConfig.spec` for desired rules and sandbox `status.effectiveEgress`, `status.effectiveIngress`, and `status.effectiveDnsEgress` for the stored effective-state report.

A sandbox template retains inline `spec.network` as its reusable recipe and can't store `spec.networkConfigId`. Each sandbox created from the template receives its own platform-managed configuration. A create-from-template request can instead provide `overrides.networkConfigId` to bind an unused caller-created configuration. Don't also provide `overrides.network` in that request.

## Update masks

Update supports these paths:

| Protobuf path | JSON mask path | Effect |
| - | - | - |
| `spec.egress` | `spec.egress` | Replaces the complete egress list, including HTTPS hostname grants. |
| `spec.deny_egress` | `spec.denyEgress` | Changes the deny-egress flag. |
| `spec.ingress` | `spec.ingress` | Replaces the complete declared ingress list for `CUSTOM` services. |
| `spec.deny_ingress` | `spec.denyIngress` | Changes the deny-ingress flag. |
| `spec.dns_egress` | `spec.dnsEgress` | Changes the outbound UDP/TCP port `53` mode. |

In JSON, encode `updateMask` as a comma-separated string, for example `"spec.egress,spec.denyEgress"`.

| Mask | Behavior |
| - | - |
| Omitted | Updates populated mutable fields. Non-empty lists, explicitly present deny flags, and a non-`UNSPECIFIED` DNS mode contribute to the implied mask. A request without populated mutable fields is invalid. |
| Explicitly empty | No-op. Doesn't apply or repair enforcement. In Connect JSON, use `"updateMask": ""`. |
| All five paths | `"spec.egress,spec.denyEgress,spec.ingress,spec.denyIngress,spec.dnsEgress"` replaces every mutable field. Omitted values reset to their defaults. Over binary protobuf, `"*"` is equivalent. |
| Explicit paths | Replaces only the named fields. Other fields retain their values. Unknown paths are invalid. |

The wildcard `"*"` works only over binary protobuf, such as gRPC or Connect with protobuf encoding. In JSON Connect requests and the REST `updateMask` query value, it fails during decoding with `INVALID_ARGUMENT`, before reaching the handler. That decoding error doesn't include a `CWSANDBOX_*` reason.

An omitted mask can't clear a repeated list. To clear egress, explicitly select `spec.egress`. Empty egress or ingress with the corresponding deny flag unset or `false` resolves to the policy default. To deny instead, clear the list and set the deny flag in the same update. A `true` deny flag and a non-empty list in the same direction are invalid.

To change DNS access, include `spec.dnsEgress` in the mask and set `dnsEgress` to `DNS_EGRESS_MODE_ALLOW` or `DNS_EGRESS_MODE_DENY`. A sandbox can't request `ALLOW` when the runner policy requires `DENY`. Selecting `spec.dnsEgress` with `DNS_EGRESS_MODE_UNSPECIFIED`, or selecting that path while omitting its value, restores the runner policy's default. This also applies when selecting all five paths for a full replacement. An unspecified policy defaults to `ALLOW`. Leaving `spec.dnsEgress` out of the mask preserves the stored mode.

DNS mode controls traffic on UDP/TCP destination port `53`, not query-name authorization or DNS over other permitted transports. HTTPS hostname grants use `egress[].httpsHostname` and remain a separate TCP port `443` permission. Platform-required traffic on other ports can remain available under `denyEgress`.

## Apply behavior and lifecycle

Creating or updating an unbound configuration validates syntax and stores desired rules. Runner-policy validation happens when a sandbox binds the configuration, and again for live updates. Live updates use the gateway's current cached runner policy, which can briefly lag a policy write. Rules outside the policy are rejected rather than silently narrowed.

A bound update waits for a sandbox in `CREATING` or `PREPARING` to reach `RUNNING`, within the request deadline. If the deadline passes first, the request fails with `CWSANDBOX_SANDBOX_NOT_READY`, and no changes are saved. Updates to a terminating or terminal sandbox fail with `CWSANDBOX_SANDBOX_NOT_RUNNING`. For a running sandbox, the update resolves the rules, persists desired state, and applies enforcement. Rule lists replace the corresponding grants. They aren't appended. Services and their visibility are unchanged.

Persistence and enforcement are separate steps. A failure after persistence can leave desired rules, actual traffic permissions, and the sandbox's effective-state report different. After a transient apply failure, some enforcement changes may already have taken effect and aren't automatically rolled back.

Retrying the same desired rules reapplies enforcement even when the stored rules already match. After resolving a retryable error, read the current configuration and reapply the intended rules. Reconcile an `etag` mismatch before retrying. The token protects the desired-state write, not an atomic transaction across enforcement systems.

When a bound update's resulting `spec` already matches stored desired state, it reapplies enforcement without checking `etag`. Don't rely on the token to reject an unchanged-spec retry. An explicitly empty update mask remains a no-op and doesn't reapply enforcement.

A permanent `CWSANDBOX_INVALID_REQUEST` rejection from the runner occurs before enforcement changes. If the update persisted new desired rules, the API attempts to restore the previous desired configuration. This restoration isn't guaranteed and doesn't overwrite a newer concurrent update. Read the configuration again after an error. A restoration changes the `etag`.

Platform-managed configurations are deleted after their sandbox terminates. Caller-created configurations remain and can be rebound or deleted once no non-terminal sandbox uses them. Copy `spec` into a new configuration to clone rules. Reusing an ID reuses the same resource.

## Errors

| Reason | Meaning and action |
| - | - |
| `CWSANDBOX_INVALID_REQUEST` | Invalid rules, mask, create-field combination, or rules unsupported by the runner or its policy. A runner without live-update support returns this reason with `FAILED_PRECONDITION`. Correct the request or use a runner with live updates enabled. |
| `CWSANDBOX_RESOURCE_EXISTS` | The caller-chosen ID already exists. Choose a new ID or read the existing configuration. |
| `CWSANDBOX_REQUEST_ID_CONFLICT` | A create request reuses a `requestId` with a different body. Use a new `requestId` for the changed request. |
| `CWSANDBOX_NETWORK_CONFIG_NOT_FOUND` | The configuration is missing or outside the caller's organization. Check the ID and organization. |
| `CWSANDBOX_NETWORK_CONFIG_IN_USE` | Another non-terminal sandbox uses the configuration, or deletion was attempted while it was in use. Use a separate configuration or wait for termination. |
| `CWSANDBOX_ETAG_MISMATCH` | The supplied token is stale (`ABORTED`). Read the latest configuration and reconcile changes before retrying. |
| `CWSANDBOX_SANDBOX_NOT_READY` | The request timed out while waiting for a sandbox in `CREATING` or `PREPARING` to reach `RUNNING`. No changes were saved. Check the sandbox state before retrying. |
| `CWSANDBOX_SANDBOX_NOT_RUNNING` | The sandbox is terminating or terminal and can't accept a live update. Create a new sandbox with the required rules. |
| `CWSANDBOX_RUNNER_UNAVAILABLE` | The sandbox's runner is temporarily unavailable or not connected. Retry according to the returned retry guidance. |
| `CWSANDBOX_BACKEND_UNAVAILABLE` | A backend operation failed. Enforcement can already have changed if saving the effective-state report failed. Read the current configuration, reapply the intended rules, and verify traffic. |
| `CWSANDBOX_COMMAND_TIMEOUT` | Applying rules on the runner timed out. Desired rules may already be saved, and enforcement may have partially changed. Read the current configuration, reapply the intended rules, and verify traffic. |
| `CWSANDBOX_DNS_EGRESS_UNAVAILABLE` | The HTTPS hostname enforcement dependency is unavailable for a widening update. Retry according to the returned retry guidance. |

Adding a sandbox's first HTTPS hostname grant through an update, rather than at creation, can return `CWSANDBOX_INVALID_REQUEST`. Some older sandboxes also reject hostname changes, including removals. In those cases, create a new sandbox with the required hostname grants. The runner must support HTTPS hostname grants to enforce them.
