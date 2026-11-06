# Change network access on a running sandbox

Source: https://docs.coreweave.com/products/sandboxes/dynamic-network-policies

# Change network access on a running sandbox

> Update a sandbox's egress and declared ingress rules through a NetworkConfig without restarting the workload.

Dynamic network policies in CoreWeave Sandboxes let you change a running sandbox's network access without restarting its workload. For example, an agent can download dependencies, then restrict outbound traffic before it executes untrusted code.

A sandbox references one `NetworkConfig`, which holds its desired network rules. Update that resource to change access. The placement's network policy still limits which rules you can request: CoreWeave manages this policy for serverless sandboxes, and your administrator configures it for CoreWeave Kubernetes Service (CKS) runners.

## Before you begin

Dynamic network policies support both serverless and CKS sandboxes when the feature is available on the selected runners. Serverless uses CoreWeave-managed runners, so you don't need your own CKS cluster or runner.

Before you begin, make sure you have the following:

* A CoreWeave API access token with `sandbox_user` permission. See [Manage API Access Tokens](https://docs.coreweave.com/security/authn-authz/manage-api-access-tokens.md).
* `NetworkConfig` support enabled on the API serving your organization. See [Availability and prerequisites](https://docs.coreweave.com/products/sandboxes/reference/network-configs.md#availability-and-prerequisites).
* Live network updates enabled on the runner your sandbox uses. CoreWeave manages this for serverless runners. For a CKS managed runner, set `spec.overrides.env.ENABLE_LIVE_NETWORK_UPDATE` to the string `"true"`. See [Manage runners](https://docs.coreweave.com/products/sandboxes/operations/managed-runners.md).
* HTTPS hostname grants supported and permitted by the placement's network policy, as required by the examples in this guide.
* `curl` and `jq` installed locally.

The examples use serverless placement and JSON requests over [Connect](https://docs.coreweave.com/products/sandboxes/reference/protos.md) at `https://api.cwsandbox.com`. The Python and TypeScript clients don't expose `NetworkConfig` operations.

Set your token. Replace `[API-ACCESS-TOKEN]` with your CoreWeave API access token:

```bash title="Set the API token" theme={"system"}
export TOKEN="[API-ACCESS-TOKEN]"
```

## Create and bind a network configuration

Create a caller-owned configuration that permits HTTPS to the Python package index and its download host. Choose an ID that is unique in your organization. This example uses `build-egress`.

```bash title="Create a network configuration" theme={"system"}
curl --fail-with-body -sS \
  'https://api.cwsandbox.com/coreweave.sandbox.v1.NetworkConfigService/CreateNetworkConfig' \
  -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' \
  -H 'Connect-Protocol-Version: 1' \
  -d '{
    "networkConfig": {
      "networkConfigId": "build-egress",
      "spec": {
        "egress": [
          {"httpsHostname": "pypi.org"},
          {"httpsHostname": "files.pythonhosted.org"}
        ]
      }
    }
  }'
```

The response is a `NetworkConfig` with its ID, desired `spec`, `etag`, and `status`. Creation validates rule syntax. When you bind the configuration to a sandbox, the platform checks the runner policy.

Create a serverless sandbox that uses the configuration. This example allocates one CPU and 1 GiB of memory:

```bash title="Create a sandbox with the configuration" theme={"system"}
curl --fail-with-body -sS \
  'https://api.cwsandbox.com/coreweave.sandbox.v1.SandboxService/CreateSandbox' \
  -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' \
  -H 'Connect-Protocol-Version: 1' \
  -d '{
    "sandbox": {
      "spec": {
        "containers": [{
          "name": "main",
          "image": "python:3.12-slim",
          "command": "sleep",
          "args": ["3600"],
          "resources": {"cpu": "1", "memory": "1Gi"}
        }],
        "mode": "SANDBOX_MODE_SERVERLESS",
        "networkConfigId": "build-egress",
        "maxLifetimeSeconds": 3600
      }
    }
  }'
```

Save the returned `sandboxId`. The platform applies the initial rules before the sandbox reaches `RUNNING`. For CKS, change `spec.mode` to `SANDBOX_MODE_CKS` and optionally select `spec.runnerIds`.

A configuration can bind to only one non-terminal sandbox at a time. Don't send both `spec.networkConfigId` and inline `spec.network` in the same create request.

If you omit `networkConfigId`, the platform creates a configuration for the sandbox. It copies any inline `spec.network` rules, or uses an empty configuration that resolves to policy defaults. Read the assigned ID from `GetSandbox.spec.networkConfigId`.

## Update rules for the running sandbox

Before changing the rules, test new HTTPS connections to `pypi.org` and `files.pythonhosted.org` from inside the running sandbox. For instructions, see the [execution guide](https://docs.coreweave.com/products/sandboxes/client/guides/execution.md). Confirm both connections succeed, and save the probe commands to repeat after the update. Resolve any connection failures before continuing.

When you are ready to restrict access, clear the sandbox's egress grants and deny outbound DNS on UDP and TCP port `53`. The update leaves declared ingress unchanged.

To reject a stale desired-state write, read the current configuration and pass its `etag` with the update:

```bash title="Restrict outbound access" theme={"system"}
config=$(curl --fail-with-body -sS \
  'https://api.cwsandbox.com/coreweave.sandbox.v1.NetworkConfigService/GetNetworkConfig' \
  -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' \
  -H 'Connect-Protocol-Version: 1' \
  -d '{"networkConfigId":"build-egress"}') &&
etag=$(printf '%s' "$config" | jq -er '.etag') &&
jq -n --arg etag "$etag" '{
  networkConfigId: "build-egress",
  networkConfig: {
    etag: $etag,
    spec: {egress: [], denyEgress: true, dnsEgress: "DNS_EGRESS_MODE_DENY"}
  },
  updateMask: "spec.egress,spec.denyEgress,spec.dnsEgress"
}' | curl --fail-with-body -sS \
  'https://api.cwsandbox.com/coreweave.sandbox.v1.NetworkConfigService/UpdateNetworkConfig' \
  -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' \
  -H 'Connect-Protocol-Version: 1' \
  --data-binary @-
```

The response is the updated `NetworkConfig`. The sandbox keeps running with the same ID and process state. Platform-required traffic, such as permitted storage access on other ports, can remain available. `denyEgress` isn't complete network isolation.

Use an explicit mask when clearing a list. An empty egress list with `denyEgress` unset or `false` restores the policy default. It doesn't mean deny all.

## Verify the result

Replace `[SANDBOX-ID]` with the ID from creation and inspect the sandbox:

```bash title="Inspect sandbox network status" theme={"system"}
curl --fail-with-body -sS \
  'https://api.cwsandbox.com/coreweave.sandbox.v1.SandboxService/GetSandbox' \
  -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' \
  -H 'Connect-Protocol-Version: 1' \
  -d '{"sandboxId":"[SANDBOX-ID]"}'
```

Check that the sandbox remains `RUNNING`, references the same `spec.networkConfigId`, and reports the updated `status.effectiveEgress`, `status.effectiveIngress`, and `status.effectiveDnsEgress`. The JSON response can omit empty repeated fields.

Repeat the connection probes that succeeded before the update. Verify that new outbound HTTPS connections to both previously granted hosts fail and that the existing workload continues to run. Investigate unrelated failures, such as an unavailable destination, before treating a failed probe as evidence of enforcement. Status fields are a stored report of the last successful update, not a live measurement of enforcement.

> [!WARNING]
>
> An update can save the desired configuration before enforcement finishes. A transient failure can leave some changes applied without restoring the previous enforcement. Read the current configuration, reapply the intended rules with its current `etag`, and verify traffic before relying on a restriction. For a permanent runner rejection, the API attempts to restore the previous desired configuration. See [Apply behavior and lifecycle](https://docs.coreweave.com/products/sandboxes/reference/network-configs.md#apply-behavior-and-lifecycle). An `etag` mismatch requires rereading and reconciling concurrent changes.

## Reuse or delete the configuration

When the sandbox terminates, a caller-created configuration becomes available for reuse. Its `status.sandboxId` can briefly retain the old ID while cleanup completes. You can bind the configuration to a new sandbox or delete it:

```bash title="Delete an unused network configuration" theme={"system"}
curl --fail-with-body -sS \
  'https://api.cwsandbox.com/coreweave.sandbox.v1.NetworkConfigService/DeleteNetworkConfig' \
  -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' \
  -H 'Connect-Protocol-Version: 1' \
  -d '{"networkConfigId":"build-egress","allowMissing":true}'
```

Deletion fails while a non-terminal sandbox uses the configuration. Platform-created configurations are deleted automatically after their sandbox terminates.

To copy network intent to another sandbox, copy the configuration's `spec` into a new configuration or inline create input. Copying `GetSandbox.spec` copies the configuration ID, not an independent set of rules.

## Supported changes and limits

The following changes and limits apply to dynamic network policies:

* You can update egress destination grants, declared ingress sources for existing `CUSTOM` services, `denyEgress`, `denyIngress`, and `dnsEgress`. Rules must remain within the runner policy.
* Service ports and visibility remain create-time settings. See [Public endpoints](https://docs.coreweave.com/products/sandboxes/public-endpoints.md).
* HTTPS hostname grants remain HTTPS-only on TCP port `443`. You can change hostname grants live only on a sandbox created with at least one `httpsHostname` grant. To add hostname grants to a sandbox created without them, create a new sandbox.
* Some older sandboxes can't change their hostname grants live, including removing them. If the update is rejected with `CWSANDBOX_INVALID_REQUEST`, create a new sandbox with the required grants.
* The runner must support HTTPS hostname grants. If it can't enforce them, requests that add or change them return `CWSANDBOX_INVALID_REQUEST`.

For resource fields, update masks, and error handling, see the [NetworkConfig API reference](https://docs.coreweave.com/products/sandboxes/reference/network-configs.md).
