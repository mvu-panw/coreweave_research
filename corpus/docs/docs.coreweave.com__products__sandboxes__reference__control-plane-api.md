# API overview

Source: https://docs.coreweave.com/products/sandboxes/reference/control-plane-api

# API overview

> Base URL, authentication, versioning, pagination, and error handling for the CoreWeave Sandboxes control plane API.

The control plane exposes a REST API for managing runners and the policy each one carries. This page covers authentication, versioning, error shapes, pagination, and updates for the managed-runner endpoints. The generated endpoint reference and OpenAPI specification also cover supported sandbox data plane and sandbox template operations.

For per-endpoint request bodies, response schemas, and field descriptions, follow the endpoint links in [Resource families](#resource-families).

## Base URL and versioning

```text theme={"system"}
https://api.coreweave.com/v1/sandbox
```

This is the control plane base URL. It hosts the runner endpoints documented on this page: deploy runners, set the policy each one carries, and query state. It's distinct from the sandbox data plane that the [cwsandbox Python client](https://docs.coreweave.com/products/sandboxes/client.md) uses to start sandboxes and stream commands and output (`Sandbox.run()`, `sb.exec()`, file operations). Control plane operations create and configure the infrastructure that produces sandboxes. Data plane operations interact with running sandboxes.

The managed-runner endpoints documented here use the `v1` URL prefix.

An earlier `v1beta2` surface remains available and is where profile templates and profile bindings live. Use policy instead of legacy profile bindings when creating or updating a runner through `v1`. New integrations should target `v1`.

## Authentication

All requests use bearer-token authentication over Transport Layer Security (TLS). Replace `API_ACCESS_TOKEN` with a CoreWeave API access token:

```text theme={"system"}
Authorization: Bearer API_ACCESS_TOKEN
```

Generate an API access token from the [Tokens](https://console.coreweave.com/tokens) page in the cloud console. Tokens inherit the permissions of the user they belong to, and the server enforces those permissions on every request. Two Identity and Access Management (IAM) actions apply to CoreWeave Sandboxes. Their identifiers are lowercase and case-sensitive:

* `sandbox_admin`: create, read, update, and delete runners, and set the policy they carry. Every managed-runner endpoint requires it, including reads. Implies `sandbox_user`.

  On runners using legacy `v1beta2` profiles, this action also permits [privileged profile settings](https://docs.coreweave.com/products/sandboxes/operations/managed-runners.md#example-allow-a-privileged-profile-posture). These settings include privileged containers, host namespaces, and host filesystem mounts. These settings can give sandboxes Node access comparable to that of a cluster administrator. The `v1` policy's `allow_privileged` setting governs in-guest privilege within the sandbox's isolation boundary.
* `sandbox_user`: create and operate sandboxes, including their network configurations. It doesn't grant access to managed-runner administration.

To grant these actions, assign the **Sandbox Admin** or **Sandbox User** role on the [Access Policies](https://console.coreweave.com/organization/iam/access-policies) page in the cloud console. The Sandbox Admin role grants `sandbox_admin`. The Sandbox User role grants `sandbox_user`. For role descriptions, see [IAM roles](https://docs.coreweave.com/security/iam/access-policies/roles.md#sandbox). For background on how Access Policies work and the step-by-step grant flow, see [Identity and Access Management (IAM)](https://docs.coreweave.com/security/iam.md) and [Manage Access Policies](https://docs.coreweave.com/security/iam/access-policies/manage.md). For more on tokens, see [Manage API access tokens](https://docs.coreweave.com/security/authn-authz/manage-api-access-tokens.md).

Unauthenticated API requests return HTTP `401 Unauthorized`. Authentication middleware can return a plain-text body. Don't assume that every error has a `google.rpc.Status` body.

The [CoreWeave Intelligent CLI](https://github.com/coreweave/cwic) provides commands for the control plane. In [version 1.49.0](https://github.com/coreweave/cwic/releases/tag/v1.49.0), `cwic sandbox runner` commands, including `cwic sandbox runner policy`, use the `v1` API through Connect RPC. Legacy `cwic sandbox profile` commands use `v1beta2` through Connect RPC. These commands share the same `--api-url`. The REST examples use the HTTP paths documented on this page.

Authenticate with `cwic auth login`. The CLI stores credentials locally using its configured storage backend. See [Configure a sandbox policy](https://docs.coreweave.com/products/sandboxes/profiles/configure.md#before-you-begin) for the CLI workflow.

## Content type

REST requests and responses with JSON payloads use:

```text theme={"system"}
Content-Type: application/json
```

The API runs over HTTP/2 through [Connect](https://connectrpc.com/), but standard `curl` or `fetch`-style clients work transparently. You don't need a gRPC client.

The [NetworkConfig API](https://docs.coreweave.com/products/sandboxes/reference/network-configs.md) is served on the sandbox data plane at `https://api.cwsandbox.com` and uses `sandbox_user`. Use it to change a sandbox's desired network rules. Use the control plane to set the runner policy that bounds those rules.

## Resource families

The managed-runner resource family has these endpoints:

| Family | Base path | Operations |
| - | - | - |
| Managed runners | `/v1/sandbox/managedRunners` | [Create](https://docs.coreweave.com/products/sandboxes/reference/control-plane-api/runnermanagementservice/create-managed-runner.md), [Get](https://docs.coreweave.com/products/sandboxes/reference/control-plane-api/runnermanagementservice/get-managed-runner.md), [List](https://docs.coreweave.com/products/sandboxes/reference/control-plane-api/runnermanagementservice/list-managed-runners.md), [Update](https://docs.coreweave.com/products/sandboxes/reference/control-plane-api/runnermanagementservice/update-managed-runner.md), [Delete](https://docs.coreweave.com/products/sandboxes/reference/control-plane-api/runnermanagementservice/delete-managed-runner.md), [Apply available update](https://docs.coreweave.com/products/sandboxes/reference/control-plane-api/runnermanagementservice/apply-available-update.md) |

A policy isn't independently addressable. It's a field on the runner, so you read it by fetching the runner. To replace the policy, send the complete document in a runner update masked to `policy`, together with the `etag` from the same read. Selecting the root `policy` path replaces the whole document, including clearing groups omitted from the body. An update that changes policy requires the current `etag`. A stale value returns `FAILED_PRECONDITION`.

Profile templates remain available on the `v1beta2` surface at `/v1beta2/sandbox/profile-templates`, together with the `profile_bindings` field on a runner. These legacy fields are rejected by `v1` managed-runner writes. Configure the runner policy instead.

## Pagination

Managed-runner listing supports cursor-based pagination. Other API services have their own pagination limits, documented on their endpoint pages:

* `pageSize`: page size. Default `50`, max `100`.
* `pageToken`: cursor returned as `nextPageToken` on the previous page. An empty string means no more pages.

Replace `NEXT_PAGE_TOKEN` with the returned `nextPageToken`:

```bash title="Paginate managed runners" theme={"system"}
curl -H "Authorization: Bearer $TOKEN" \
  'https://api.coreweave.com/v1/sandbox/managedRunners?pageSize=50'

# Follow the cursor
curl -H "Authorization: Bearer $TOKEN" \
  'https://api.coreweave.com/v1/sandbox/managedRunners?pageSize=50&pageToken=NEXT_PAGE_TOKEN'
```

The CoreWeave Intelligent CLI automatically paginates list commands such as `cwic sandbox runner get`.

## Field masks on updates

Managed runner updates on the `v1` API accept an optional `update_mask` to select the mutable fields to update. An omitted or empty mask replaces the whole mutable resource, including policy, so it requires the complete policy and its current `etag`. The wildcard `*` is supported only over binary Protobuf, not in the REST `updateMask` query parameter or JSON requests.

Paths use dotted notation and `snake_case` field names (standard `google.protobuf.FieldMask` convention). Commonly used mutable paths:

| Path | Applies to | Purpose |
| - | - | - |
| `display_name` | Managed runner | Change the runner display name. |
| `identity.runner_group_id` | Managed runner | Change the runner group used for scheduling affinity. |
| `spec` | Managed runner | Replace the whole managed runner configuration. |
| `spec.release_channel` | Managed runner | Switch the release channel (`RELEASE_CHANNEL_STABLE` or `RELEASE_CHANNEL_RAPID`). |
| `spec.maintenance_policy` | Managed runner | Adjust automatic-update maintenance windows. |
| `spec.overrides` | Managed runner | Replace runner deployment overrides, including tolerations, Node selectors, and affinity. |
| `spec.overrides.affinity` | Managed runner | Replace runner Pod affinity while preserving sibling overrides. |
| `spec.enforce_resource_limits` | Managed runner | Require sandboxes on the runner to declare CPU and memory limits. |
| `policy` | Managed runner | Replace the whole policy document. Include the current `etag`. |
| `profile_bindings` | Managed runner | Replace the entire list of profile bindings. Legacy, `v1beta2` only. Rejected by `v1` writes. |

The version 1.49.0 CLI builds explicit update masks. File-based runner edits select fields present in the input and group nested fields at supported replacement boundaries. For example, nested policy fields select `policy`, replacing the entire policy document.

Runner YAML uses `spec`, not the legacy `managed_spec`, and accepts both Protobuf `snake_case` and JSON `camelCase` field names. Exported YAML uses `snake_case`.

Legacy `v1beta2` updates infer an omitted or empty mask from mutable field values and message presence instead of replacing the whole mutable resource. The version 1.49.0 profile commands build explicit masks for `description`, `labels`, and `spec`, replacing each selected field as a whole.

On the REST surface, supply the mask as a single comma-separated `updateMask` query parameter. Use the JSON (camelCase) form of each path, and send the resource itself as the request body with no wrapper. Replace `RUNNER_ID` with the ID of the runner to update:

```bash theme={"system"}
curl -X PATCH "https://api.coreweave.com/v1/sandbox/managedRunners/RUNNER_ID?updateMask=spec.releaseChannel" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{ "spec": { "releaseChannel": "RELEASE_CHANNEL_RAPID" } }'
```

The runner's zone and cluster ID are immutable after creation.

## Runner affinity

The managed runner spec accepts `spec.overrides.affinity`, a Kubernetes `Affinity` object with Kubernetes camel case keys. It supports `nodeAffinity`, `podAffinity`, and `podAntiAffinity`. This field controls runner Pods only. It doesn't change sandbox Pod placement or Node-budget eligibility. The resolved `deploymentSpec.affinity` is output-only.

Affinity updates replace the whole object. With `updateMask=spec.overrides.affinity`, an explicit `"affinity": {}` clears all rules, including inherited affinity. Omitting `affinity` from the request body with the same mask removes the customer override and restores platform defaults. Node selectors and tolerations remain independent.

For CLI and REST examples, scheduling behavior, and rollout verification, see [Configure runner affinity](https://docs.coreweave.com/products/sandboxes/operations/managed-runners.md#example-configure-runner-affinity). The legacy `v1beta2` equivalent is `managed_spec.overrides.affinity`.

## Errors

RPC errors transcoded to REST use an HTTP status and a `google.rpc.Status` body, as in the following example. Failures from authentication or authorization middleware, or from an edge service, can use a different body format. Check the HTTP status before decoding the body.

```text title="Example output" theme={"system"}
{
  "code":    3,
  "message": "runner.identity.zone is required",
  "details": []
}
```

The following table lists common HTTP-to-RPC code mappings. A failure outside the RPC handler might not include the numeric `code` in its body:

| HTTP | `code` | Meaning |
| - | - | - |
| `400` | 3 (`INVALID_ARGUMENT`) | Missing required field, malformed input, invalid spec. |
| `401` | 16 (`UNAUTHENTICATED`) | Missing or invalid API token. |
| `403` | 7 (`PERMISSION_DENIED`) | Token lacks required permission for the action. |
| `404` | 5 (`NOT_FOUND`) | Resource doesn't exist. |
| `409` | 6 (`ALREADY_EXISTS`) | Duplicate `runnerId` or cluster, or reuse of a `requestId` with different create content or a deleted original runner. |
| `503` | 14 (`UNAVAILABLE`) | Dependency (for example, cluster validation) temporarily unavailable. Follow the operation-specific retry guidance in the Idempotency section. |
| `500` | 13 (`INTERNAL`) | Unexpected server error. Reconcile an uncertain write result before retrying. |

When an error includes structured RPC details, use its code and details for programmatic error handling. Treat the message as explanatory text.

## Idempotency

Managed-runner operations have the following retry behavior:

* Deleting an absent runner returns `404` by default. Set `allowMissing=true` to return a successful empty response when the runner is absent.
* Create supports an optional `requestId` idempotency token, at most 128 UTF-8 bytes. Reusing it with the same create content returns the original runner without provisioning again. Reusing it with different content or after the original runner was deleted returns `409 Conflict`. Without a token, check the runner with `GET` before retrying an uncertain create.
* Send an explicit field mask when updating a runner. If the update changes policy, include the `etag` captured with that policy. After a stale-ETag error or an uncertain write result, fetch the current runner, reconcile the intended changes, and submit them with the current `etag`.

## Heartbeats

Runner health includes connection status and installation status. A runner Get response exposes `connectionStatus`, `installStatus`, and `lastHeartbeatTime`. When a ready runner's heartbeat becomes stale, the API can report `installStatus` as `RUNNER_INSTALL_STATUS_FAILED` with the reason `RUNNER_INSTALL_FAILURE_REASON_RUNNER_OFFLINE`. The staleness threshold is configurable. Use the status fields and last heartbeat together when checking runner health.

## See also

For related guidance, see the following pages:

* [Manage runners with Terraform](https://docs.coreweave.com/products/sandboxes/operations/terraform-managed-runners.md): configure, import, and update runners with the CoreWeave Terraform provider.
* [Sandboxes architecture](https://docs.coreweave.com/products/sandboxes/architecture.md): the resource model and how the gateway brokers runtime requests.
* [Policies overview](https://docs.coreweave.com/products/sandboxes/profiles/profiles.md): how a sandbox resolves against a policy.
* [Configure a sandbox policy](https://docs.coreweave.com/products/sandboxes/profiles/configure.md): CoreWeave Intelligent CLI and REST workflows to configure a sandbox policy.
* [Deploy and manage a runner](https://docs.coreweave.com/products/sandboxes/operations/managed-runners.md): CoreWeave Intelligent CLI and REST walkthrough of the runner lifecycle.
* [Policy reference](https://docs.coreweave.com/products/sandboxes/reference/profile.md): fields, types, defaults, and validation rules for sandbox policies.
* [Protobuf](https://docs.coreweave.com/products/sandboxes/reference/protos.md): where to find the published Protobuf module, which host serves each service, and how to install a generated software development kit (SDK).

## OpenAPI specification

The curated OpenAPI 3.0 specification for supported Sandboxes `v1` REST endpoints is embedded in the following code block. It covers both data plane and control plane services. Expand the code block by clicking **See all** at the bottom, or use the download and copy buttons in the title bar.

```yaml expandable title="Sandboxes OpenAPI" theme={"system"}
openapi: 3.0.3
info:
  title: CoreWeave Sandboxes API
  version: 0.0.1
  description: The Sandboxes API lets you manage runners, templates, volumes, network configurations,
    organization settings, and the lifecycle of individual sandboxes on CoreWeave.
servers:
- url: https://api.cwsandbox.com
  description: CoreWeave sandbox data plane. Hosts the sandbox lifecycle, volumes, snapshots, runner discovery,
    and organization settings.
- url: https://api.coreweave.com
  description: CoreWeave control plane. Hosts managed runner and sandbox template administration.
paths:
  /v1/availableRunners:
    get:
      operationId: DiscoveryService_ListAvailableRunners
      summary: List available runners
      description: "ListAvailableRunners lists the runners visible to the caller's organization,\n optionally\
        \ filtered. RunnerView defaults to BASIC when unspecified."
      parameters:
      - name: runnerGroupId
        in: query
        description: Filters (all optional; AND-combined).
        schema:
          type: string
      - name: gpuType
        in: query
        schema:
          type: string
      - name: architecture
        in: query
        schema:
          type: string
      - name: healthyOnly
        in: query
        schema:
          type: boolean
      - name: pageSize
        in: query
        schema:
          type: integer
          format: int32
      - name: pageToken
        in: query
        schema:
          type: string
      - name: view
        in: query
        description: Detail level. Unspecified defaults to BASIC for List.
        schema:
          type: string
          format: enum
          enum:
          - RUNNER_VIEW_UNSPECIFIED
          - RUNNER_VIEW_BASIC
          - RUNNER_VIEW_FULL
      - name: serviceVisibility
        in: query
        description: "Require a runner that can enforce this generic L4 service visibility.\n UNSPECIFIED\
          \ does not filter."
        schema:
          type: string
          format: enum
          enum:
          - VISIBILITY_UNSPECIFIED
          - VISIBILITY_PUBLIC
          - VISIBILITY_PRIVATE
          - VISIBILITY_CUSTOM
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/coreweave.sandbox.v1.ListAvailableRunnersResponse'
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/google.rpc.Status'
      servers:
      - url: https://api.cwsandbox.com
        description: CoreWeave sandbox data plane.
      tags:
      - DiscoveryService
  /v1/fileSystemSnapshots:
    get:
      operationId: SandboxService_ListFileSystemSnapshots
      summary: List file system snapshots
      description: ListFileSystemSnapshots lists the caller's snapshots.
      parameters:
      - name: pageSize
        in: query
        schema:
          type: integer
          format: int32
      - name: pageToken
        in: query
        schema:
          type: string
      - name: sourceSandboxId
        in: query
        description: Filter to snapshots created by a specific sandbox.
        schema:
          type: string
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/coreweave.sandbox.v1.ListFileSystemSnapshotsResponse'
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/google.rpc.Status'
      servers:
      - url: https://api.cwsandbox.com
        description: CoreWeave sandbox data plane.
      tags:
      - SandboxService
  /v1/fileSystemSnapshots/{fileSystemSnapshotId}:
    get:
      operationId: SandboxService_GetFileSystemSnapshot
      summary: Get file system snapshot
      description: GetFileSystemSnapshot returns snapshot metadata.
      parameters:
      - name: fileSystemSnapshotId
        in: path
        required: true
        schema:
          type: string
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/coreweave.sandbox.v1.FileSystemSnapshot'
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/google.rpc.Status'
      servers:
      - url: https://api.cwsandbox.com
        description: CoreWeave sandbox data plane.
      tags:
      - SandboxService
    delete:
      operationId: SandboxService_DeleteFileSystemSnapshot
      summary: Delete file system snapshot
      description: "DeleteFileSystemSnapshot deletes a snapshot. Sandboxes restored from it are\n unaffected."
      parameters:
      - name: fileSystemSnapshotId
        in: path
        required: true
        schema:
          type: string
      - name: allowMissing
        in: query
        description: If true, deleting an absent snapshot succeeds instead of returning NOT_FOUND.
        schema:
          type: boolean
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/coreweave.sandbox.v1.FileSystemSnapshot'
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/google.rpc.Status'
      servers:
      - url: https://api.cwsandbox.com
        description: CoreWeave sandbox data plane.
      tags:
      - SandboxService
  /v1/networkConfigs:
    get:
      operationId: NetworkConfigService_ListNetworkConfigs
      summary: List network configurations
      description: List configurations in the caller's organization. Use platformManaged to filter platform-created
        or caller-created resources, or omit it for both. Continue pagination with nextPageToken.
      parameters:
      - name: pageSize
        in: query
        schema:
          type: integer
          format: int32
      - name: pageToken
        in: query
        schema:
          type: string
      - name: platformManaged
        in: query
        description: 'Optional filter: only platform-managed, or only caller-created.'
        schema:
          type: boolean
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/coreweave.sandbox.v1.ListNetworkConfigsResponse'
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/google.rpc.Status'
      servers:
      - url: https://api.cwsandbox.com
      tags:
      - NetworkConfigService
    post:
      operationId: NetworkConfigService_CreateNetworkConfig
      summary: Create network configuration
      description: Create an organization-scoped desired network configuration. Choose an ID matching
        ^[a-z][a-z0-9-]{2,62}$ without the reserved nc- prefix. Creation validates syntax; runner-policy
        constraints are checked when a sandbox binds the configuration. Requires the sandbox_user action.
      parameters:
      - name: requestId
        in: query
        schema:
          type: string
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/coreweave.sandbox.v1.NetworkConfig'
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/coreweave.sandbox.v1.NetworkConfig'
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/google.rpc.Status'
      servers:
      - url: https://api.cwsandbox.com
      tags:
      - NetworkConfigService
  /v1/networkConfigs/{networkConfigId}:
    get:
      operationId: NetworkConfigService_GetNetworkConfig
      summary: Get network configuration
      description: Return the desired network rules, lifecycle status, and concurrency token. Desired
        state can differ from enforcement after a failed update. Read sandbox effective-state fields as
        a stored report, and verify traffic before relying on a restriction.
      parameters:
      - name: networkConfigId
        in: path
        required: true
        schema:
          type: string
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/coreweave.sandbox.v1.NetworkConfig'
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/google.rpc.Status'
      servers:
      - url: https://api.cwsandbox.com
      tags:
      - NetworkConfigService
    delete:
      operationId: NetworkConfigService_DeleteNetworkConfig
      summary: Delete network configuration
      description: Delete a configuration that no non-terminal sandbox uses. A configuration in use returns
        FAILED_PRECONDITION with CWSANDBOX_NETWORK_CONFIG_IN_USE. Set allowMissing to succeed when the
        ID does not exist. Successful deletion returns an empty response.
      parameters:
      - name: networkConfigId
        in: path
        required: true
        schema:
          type: string
      - name: allowMissing
        in: query
        schema:
          type: boolean
      responses:
        '200':
          description: OK
          content: {}
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/google.rpc.Status'
      servers:
      - url: https://api.cwsandbox.com
      tags:
      - NetworkConfigService
    patch:
      operationId: NetworkConfigService_UpdateNetworkConfig
      summary: Update network configuration
      description: Update desired network rules and apply them to the bound running sandbox. JSON updateMask
        paths are spec.egress, spec.denyEgress, spec.ingress, spec.denyIngress, and spec.dnsEgress. An
        omitted mask selects populated fields; an explicitly empty mask is a no-op. To replace all mutable
        fields in JSON, select all five paths. Selected fields omitted from the body reset to their defaults.
        The wildcard * is supported only over binary protobuf (gRPC or Connect protobuf), not JSON Connect
        or the REST updateMask query value. JSON wildcard decoding can return INVALID_ARGUMENT before
        the handler, without a CWSANDBOX error reason. Clearing a list requires selecting its path explicitly.
        An empty list with its deny flag unset or false restores policy defaults. Send the last returned
        etag in the resource body to reject a stale desired-state write with ABORTED and CWSANDBOX_ETAG_MISMATCH.
        A bound update whose resulting spec already matches stored desired state reapplies enforcement
        without checking etag. Omitting etag allows the last persisted write to win. Desired state is
        persisted before live apply; a transient failure can leave partially applied permissions without
        rollback. A permanent runner rejection attempts to restore the previous desired configuration
        without overwriting a newer update. Read the current configuration, reconcile changes, and retry
        the intended update. Selecting spec.dnsEgress with DNS_EGRESS_MODE_UNSPECIFIED restores the runner
        policy default; omitting that mask path preserves the stored mode.
      parameters:
      - name: networkConfigId
        in: path
        required: true
        schema:
          type: string
      - name: updateMask
        in: query
        description: 'Comma-separated JSON paths: spec.egress, spec.denyEgress, spec.ingress, spec.denyIngress,
          and spec.dnsEgress. Omission selects populated mutable fields; an explicitly empty mask is a
          no-op. To replace all mutable fields in JSON, select all five paths. Selected fields omitted
          from the body reset to their defaults. The wildcard * is supported only over binary protobuf
          (gRPC or Connect protobuf), not JSON Connect or REST requests.'
        schema:
          type: string
          format: field-mask
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/coreweave.sandbox.v1.NetworkConfig'
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/coreweave.sandbox.v1.NetworkConfig'
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/google.rpc.Status'
      servers:
      - url: https://api.cwsandbox.com
      tags:
      - NetworkConfigService
  /v1/organizations/{organizationId}/availableRunners/{runnerId}:
    get:
      operationId: DiscoveryService_GetAvailableRunner
      summary: Get available runner
      description: "GetAvailableRunner returns a single runner by id. Returns NOT_FOUND (reason\n CWSANDBOX_RUNNER_NOT_FOUND)\
        \ if the runner is unknown or not visible.\n RunnerView defaults to FULL when unspecified."
      parameters:
      - name: organizationId
        in: path
        description: "Organization that owns runner_id. Use the pair returned by\n ListAvailableRunners."
        required: true
        schema:
          type: string
      - name: runnerId
        in: path
        required: true
        schema:
          type: string
      - name: view
        in: query
        description: Detail level. Unspecified defaults to FULL for Get.
        schema:
          type: string
          format: enum
          enum:
          - RUNNER_VIEW_UNSPECIFIED
          - RUNNER_VIEW_BASIC
          - RUNNER_VIEW_FULL
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/coreweave.sandbox.v1.AvailableRunner'
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/google.rpc.Status'
      servers:
      - url: https://api.cwsandbox.com
        description: CoreWeave sandbox data plane.
      tags:
      - DiscoveryService
  /v1/sandbox/managedRunners:
    get:
      operationId: SandboxV1RunnerManagementService_ListManagedRunners
      summary: List managed runners
      description: ListManagedRunners lists the caller's managed runners.
      parameters:
      - name: runnerGroupId
        in: query
        schema:
          type: string
      - name: zone
        in: query
        schema:
          type: string
      - name: clusterId
        in: query
        schema:
          type: string
      - name: connectionStatus
        in: query
        description: Filter by connection status. Omit this parameter or use RUNNER_CONNECTION_STATUS_UNSPECIFIED
          to apply no connection-status filter.
        schema:
          type: string
          format: enum
          enum:
          - RUNNER_CONNECTION_STATUS_UNSPECIFIED
          - RUNNER_CONNECTION_STATUS_CONNECTED
          - RUNNER_CONNECTION_STATUS_DISCONNECTED
      - name: installStatus
        in: query
        description: Filter by installation status. Omit this parameter or use RUNNER_INSTALL_STATUS_UNSPECIFIED
          to apply no installation-status filter.
        schema:
          type: string
          format: enum
          enum:
          - RUNNER_INSTALL_STATUS_UNSPECIFIED
          - RUNNER_INSTALL_STATUS_PENDING
          - RUNNER_INSTALL_STATUS_PROVISIONING
          - RUNNER_INSTALL_STATUS_READY
          - RUNNER_INSTALL_STATUS_FAILED
          - RUNNER_INSTALL_STATUS_DELETING
      - name: runnerId
        in: query
        schema:
          type: string
      - name: pageSize
        in: query
        schema:
          type: integer
          format: int32
      - name: pageToken
        in: query
        schema:
          type: string
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/coreweave.sandbox.v1.ListManagedRunnersResponse'
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/google.rpc.Status'
      servers:
      - url: https://api.coreweave.com
        description: CoreWeave control plane.
      tags:
      - RunnerManagementService
    post:
      operationId: SandboxV1RunnerManagementService_CreateManagedRunner
      summary: Create managed runner
      description: "CreateManagedRunner registers a platform-managed runner with a required\n policy.\
        \ No profile bindings are needed."
      parameters:
      - name: requestId
        in: query
        description: "Optional idempotency token, at most 128 UTF-8 bytes. Reusing a token\n returns the\
          \ same runner. A different request body or a deleted original\n runner returns ALREADY_EXISTS."
        schema:
          type: string
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/coreweave.sandbox.v1.ManagedRunner'
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/coreweave.sandbox.v1.ManagedRunner'
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/google.rpc.Status'
      servers:
      - url: https://api.coreweave.com
        description: CoreWeave control plane.
      tags:
      - RunnerManagementService
  /v1/sandbox/managedRunners/{runnerId}:
    get:
      operationId: SandboxV1RunnerManagementService_GetManagedRunner
      summary: Get managed runner
      description: GetManagedRunner returns a managed runner by runner_id.
      parameters:
      - name: runnerId
        in: path
        required: true
        schema:
          type: string
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/coreweave.sandbox.v1.ManagedRunner'
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/google.rpc.Status'
      servers:
      - url: https://api.coreweave.com
        description: CoreWeave control plane.
      tags:
      - RunnerManagementService
    delete:
      operationId: SandboxV1RunnerManagementService_DeleteManagedRunner
      summary: Delete managed runner
      description: DeleteManagedRunner decommissions a managed runner.
      parameters:
      - name: runnerId
        in: path
        required: true
        schema:
          type: string
      - name: allowMissing
        in: query
        description: If true, deleting an absent runner succeeds instead of returning NOT_FOUND.
        schema:
          type: boolean
      responses:
        '200':
          description: OK
          content: {}
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/google.rpc.Status'
      servers:
      - url: https://api.coreweave.com
        description: CoreWeave control plane.
      tags:
      - RunnerManagementService
    patch:
      operationId: SandboxV1RunnerManagementService_UpdateManagedRunner
      summary: Update managed runner
      description: UpdateManagedRunner updates mutable managed-runner configuration.
      parameters:
      - name: runnerId
        in: path
        description: "Runner to update. If managed_runner.identity.runner_id is set, it must\n match this\
          \ value."
        required: true
        schema:
          type: string
      - name: updateMask
        in: query
        description: Comma-separated JSON paths to update. An omitted or empty mask replaces the whole
          mutable resource. The wildcard * is supported only over binary protobuf (gRPC or Connect protobuf),
          not JSON Connect or the REST updateMask query value.
        schema:
          type: string
          format: field-mask
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/coreweave.sandbox.v1.ManagedRunner'
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/coreweave.sandbox.v1.ManagedRunner'
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/google.rpc.Status'
      servers:
      - url: https://api.coreweave.com
        description: CoreWeave control plane.
      tags:
      - RunnerManagementService
  /v1/sandbox/managedRunners/{runnerId}:applyAvailableUpdate:
    post:
      operationId: SandboxV1RunnerManagementService_ApplyAvailableUpdate
      summary: Apply available update
      description: "ApplyAvailableUpdate immediately applies the latest version on this\n runner's release\
        \ channel, bypassing maintenance-window scheduling."
      parameters:
      - name: runnerId
        in: path
        required: true
        schema:
          type: string
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/coreweave.sandbox.v1.ManagedRunner'
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/google.rpc.Status'
      servers:
      - url: https://api.coreweave.com
        description: CoreWeave control plane.
      tags:
      - RunnerManagementService
  /v1/sandboxTemplates:
    get:
      operationId: SandboxTemplateService_ListSandboxTemplates
      summary: List sandbox templates
      description: "ListSandboxTemplates lists templates in the caller's tenant organization.\n Soft-deleted\
        \ rows are omitted unless show_deleted is set (admin only)."
      parameters:
      - name: pageSize
        in: query
        schema:
          type: integer
          format: int32
      - name: pageToken
        in: query
        schema:
          type: string
      - name: showDeleted
        in: query
        description: "When true, include soft-deleted templates. Requires sandbox_admin.\n Default false."
        schema:
          type: boolean
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/coreweave.sandbox.v1.ListSandboxTemplatesResponse'
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/google.rpc.Status'
      servers:
      - url: https://api.coreweave.com
        description: CoreWeave control plane.
      tags:
      - SandboxTemplateService
    post:
      operationId: SandboxTemplateService_CreateSandboxTemplate
      summary: Create sandbox template
      description: CreateSandboxTemplate creates a new template. Requires sandbox_admin.
      parameters:
      - name: requestId
        in: query
        description: "Optional idempotency token scoped to the caller's tenant organization.\n Identical\
          \ retries with the same token return the original template."
        schema:
          type: string
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/coreweave.sandbox.v1.SandboxTemplate'
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/coreweave.sandbox.v1.SandboxTemplate'
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/google.rpc.Status'
      servers:
      - url: https://api.coreweave.com
        description: CoreWeave control plane.
      tags:
      - SandboxTemplateService
  /v1/sandboxTemplates/{sandboxTemplateId}:
    get:
      operationId: SandboxTemplateService_GetSandboxTemplate
      summary: Get sandbox template
      description: "GetSandboxTemplate returns a template by UUID or org-unique display_name.\n Soft-deleted\
        \ templates require show_deleted and sandbox_admin."
      parameters:
      - name: sandboxTemplateId
        in: path
        description: "UUID or org-unique display_name. Resolution: if the string parses as a\n UUID, look\
          \ up by id only (including soft-deleted when show_deleted); a\n soft-deleted id does not fall\
          \ through to display_name. Otherwise look up\n by display_name among rows visible under show_deleted\
          \ (active-only when\n false). Name lookup is best-effort for discovery; Create selects by UUID."
        required: true
        schema:
          type: string
      - name: showDeleted
        in: query
        description: When true, allow returning a soft-deleted template. Requires sandbox_admin.
        schema:
          type: boolean
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/coreweave.sandbox.v1.SandboxTemplate'
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/google.rpc.Status'
      servers:
      - url: https://api.coreweave.com
        description: CoreWeave control plane.
      tags:
      - SandboxTemplateService
    delete:
      operationId: SandboxTemplateService_DeleteSandboxTemplate
      summary: Delete sandbox template
      description: "DeleteSandboxTemplate soft-deletes a template. Requires sandbox_admin.\n Existing\
        \ sandboxes are unaffected; new creates cannot select the template."
      parameters:
      - name: sandboxTemplateId
        in: path
        description: UUID of the template to soft-delete.
        required: true
        schema:
          type: string
      responses:
        '200':
          description: OK
          content: {}
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/google.rpc.Status'
      servers:
      - url: https://api.coreweave.com
        description: CoreWeave control plane.
      tags:
      - SandboxTemplateService
    patch:
      operationId: SandboxTemplateService_UpdateSandboxTemplate
      summary: Update sandbox template
      description: "UpdateSandboxTemplate patches a template. Requires sandbox_admin.\n Each successful\
        \ update increments revision."
      parameters:
      - name: sandboxTemplateId
        in: path
        description: Identifies the template to update (UUID).
        required: true
        schema:
          type: string
      - name: updateMask
        in: query
        description: 'Comma-separated JSON paths relative to the sandbox template: displayName, spec,
          and attachments. Omission updates only populated mutable fields. To replace all mutable fields
          in JSON, select all three paths. Other paths return INVALID_ARGUMENT. The wildcard * is supported
          only over binary protobuf (gRPC or Connect protobuf), not JSON Connect or the REST updateMask
          query value.'
        schema:
          type: string
          format: field-mask
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/coreweave.sandbox.v1.SandboxTemplate'
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/coreweave.sandbox.v1.SandboxTemplate'
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/google.rpc.Status'
      servers:
      - url: https://api.coreweave.com
        description: CoreWeave control plane.
      tags:
      - SandboxTemplateService
  /v1/sandboxes:
    get:
      operationId: SandboxService_ListSandboxes
      summary: List sandboxes
      description: ListSandboxes lists the caller's sandboxes.
      parameters:
      - name: pageSize
        in: query
        schema:
          type: integer
          format: int32
      - name: pageToken
        in: query
        schema:
          type: string
      - name: tags
        in: query
        description: 'Filter: sandboxes matching all tags (AND).'
        schema:
          type: array
          items:
            type: string
      - name: state
        in: query
        description: 'Filter: only sandboxes in this state (STATE_UNSPECIFIED = any).'
        schema:
          type: string
          format: enum
          enum:
          - STATE_UNSPECIFIED
          - STATE_CREATING
          - STATE_RUNNING
          - STATE_COMPLETED
          - STATE_FAILED
          - STATE_TERMINATING
          - STATE_TERMINATED
          - STATE_PENDING
          - STATE_PAUSED
          - STATE_PREPARING
      - name: showTerminated
        in: query
        description: "Include terminal sandboxes within the retention window. Defaults to\n active-only."
        schema:
          type: boolean
      - name: runnerIds
        in: query
        description: 'Filter: sandboxes on any of these runners.'
        schema:
          type: array
          items:
            type: string
      - name: volumeIds
        in: query
        description: 'Filter: sandboxes with any of these registered Volumes attached.'
        schema:
          type: array
          items:
            type: string
      - name: sortDirection
        in: query
        description: "Direction of the creation-time ordering, with sandbox_id breaking ties.\n Unspecified\
          \ means descending: newest first. A page_token must be reused\n with the direction that produced\
          \ it."
        schema:
          type: string
          format: enum
          enum:
          - SORT_DIRECTION_UNSPECIFIED
          - SORT_DIRECTION_DESCENDING
          - SORT_DIRECTION_ASCENDING
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/coreweave.sandbox.v1.ListSandboxesResponse'
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/google.rpc.Status'
      servers:
      - url: https://api.cwsandbox.com
        description: CoreWeave sandbox data plane.
      tags:
      - SandboxService
    post:
      operationId: SandboxService_CreateSandbox
      summary: Create sandbox
      description: "CreateSandbox launches a sandbox from a complete SandboxSpec (AIP-133).\n Returns\
        \ immediately with the sandbox in STATE_CREATING; poll GetSandbox for\n STATE_RUNNING / terminal\
        \ states. To create from an org template, use\n CreateSandboxFromTemplate."
      parameters:
      - name: requestId
        in: query
        description: "Optional idempotency token; repeated identical requests with the same token\n return\
          \ the original result."
        schema:
          type: string
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/coreweave.sandbox.v1.Sandbox'
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/coreweave.sandbox.v1.Sandbox'
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/google.rpc.Status'
      servers:
      - url: https://api.cwsandbox.com
        description: CoreWeave sandbox data plane.
      tags:
      - SandboxService
  /v1/sandboxes/{sandboxId}:
    get:
      operationId: SandboxService_GetSandbox
      summary: Get sandbox
      description: GetSandbox returns the current state of a sandbox.
      parameters:
      - name: sandboxId
        in: path
        description: "Sandbox UUID or tenant-scoped display_name. Names resolve active sandboxes\n only;\
          \ use the UUID to retrieve a terminal sandbox. UUIDs resolve by ID only.\n Use the returned\
          \ sandbox_id for subsequent operations, since names can be\n reused after termination. Existing\
          \ ownership and access rules apply."
        required: true
        schema:
          type: string
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/coreweave.sandbox.v1.Sandbox'
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/google.rpc.Status'
      servers:
      - url: https://api.cwsandbox.com
        description: CoreWeave sandbox data plane.
      tags:
      - SandboxService
    delete:
      operationId: SandboxService_DeleteSandbox
      summary: Delete sandbox
      description: "DeleteSandbox terminates a sandbox. Optionally drains gracefully and/or\n snapshots\
        \ its volumes on the way down."
      parameters:
      - name: sandboxId
        in: path
        required: true
        schema:
          type: string
      - name: gracePeriodSeconds
        in: query
        description: "Grace period before forced termination. Zero or omission terminates\n immediately;\
          \ positive values are clamped to the platform maximum. The\n effective deadline bounds drain\
          \ and snapshot."
        schema:
          type: integer
          format: int32
      - name: snapshotVolumes
        in: query
        description: "Names of scratch SandboxSpec.volumes to snapshot before terminating; empty\n snapshots\
          \ nothing. Each name must reference a scratch (not registered)\n volume declared on the sandbox\
          \ spec: a registered-Volume-backed name is\n rejected with CWSANDBOX_VOLUME_NOT_SNAPSHOTTABLE,\
          \ an unknown name with\n INVALID_ARGUMENT. Asynchronous — see the response.\n\n Field 3 formerly\
          \ held a `bool snapshot`; it was repurposed to this repeated\n string as a deliberate breaking\
          \ change while v1 is pre-GA (no live clients).\n Old `bool snapshot=true` senders are unsupported\
          \ — the value is dropped."
        schema:
          type: array
          items:
            type: string
      - name: requestId
        in: query
        description: "Optional receipt for a snapshot-on-delete request. Retrying the same\n request with\
          \ the same token returns the original snapshot ids without\n redispatching the destructive command.\
          \ Reusing it with different known\n request fields is rejected. This field is ignored when snapshot_volumes\
          \ is\n empty: Plain Delete is naturally idempotent, does not inspect or persist a\n snapshot\
          \ receipt, and retains the v1beta2 cancel-then-stop lifecycle.\n Snapshot volume order is part\
          \ of request identity.\n Without a token, retrying snapshot-on-delete may create and dispatch\
          \ a new\n batch. An exact replay returns the original receipt even when its snapshots\n failed;\
          \ inspect the returned sandbox and snapshot states before retrying\n the delete with a new token.\
          \ Tokens are limited to 128 UTF-8 bytes."
        schema:
          type: string
      - name: allowMissing
        in: query
        description: If true, deleting an absent sandbox succeeds instead of returning NOT_FOUND.
        schema:
          type: boolean
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/coreweave.sandbox.v1.DeleteSandboxResponse'
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/google.rpc.Status'
      servers:
      - url: https://api.cwsandbox.com
        description: CoreWeave sandbox data plane.
      tags:
      - SandboxService
  /v1/sandboxes/{sandboxId}/logs:
    get:
      operationId: SandboxService_ListSandboxLogs
      description: "ListSandboxLogs returns one page of a sandbox's stored stdout and stderr\n lines,\
        \ ordered by (timestamp, event_id). Stored logs stay readable while\n the sandbox runs and after\
        \ it ends, until retention_expires_at; unlike\n StreamLogs, a terminal sandbox is served. The\
        \ creating user, or a caller\n with the sandbox_admin action in the sandbox's organization, can\
        \ read\n them. A caller who cannot see the sandbox gets the same error as\n GetSandbox, whether\
        \ or not logs exist.\n\n Collection is best effort: lines can be missing, for example when a\n\
        \ sandbox ends within about a minute of writing them or when output\n arrives faster than it can\
        \ be collected. Lines longer than the\n collection line limit are not stored whole. A line that\
        \ is a JSON\n object is stored as normalized JSON: duplicate keys keep their first\n value, and\
        \ whitespace, number formatting, and escapes are normalized.\n Bodies are stored as written, without\
        \ redaction, so do not write\n secrets to stdout or stderr. Stored logs are not subject to legal\
        \ hold.\n\n Each line is stored for a fixed time after it was written, and reads end\n 30 days\
        \ after the sandbox ends. A sandbox that ran up to 16 days keeps\n its full history for those\
        \ 30 days; a longer sandbox keeps its full\n history while it runs, and afterwards its oldest\
        \ lines expire first.\n\n Pagination is keyset and weakly consistent: a line that arrives late,\n\
        \ behind the page cursor, appears only in a new first-page request. A\n sandbox whose images are\
        \ still being built returns an empty page.\n\n Errors:\n   - INVALID_ARGUMENT (CWSANDBOX_INVALID_REQUEST):\
        \ a field is out of\n     range, the container names a platform sidecar, or page_token is\n  \
        \   malformed, expired, or does not match the request.\n   - FAILED_PRECONDITION (CWSANDBOX_LOGS_NOT_ENABLED):\
        \ the sandbox has no\n     stored logs to serve. Stored logs were not enabled for it when it was\n\
        \     created, or are not enabled for the organization.\n   - FAILED_PRECONDITION (CWSANDBOX_LOGS_DELETED):\
        \ the sandbox's stored\n     logs were deleted.\n   - FAILED_PRECONDITION (CWSANDBOX_LOG_RETENTION_EXPIRED):\
        \ the stored\n     logs are past their retention deadline.\n   - FAILED_PRECONDITION (CWSANDBOX_LOG_QUERY_TOO_EXPENSIVE):\
        \ the query\n     exceeds a cost limit and fails the same way on retry. Narrow the time\n    \
        \ range, or remove text_contains.\n   - RESOURCE_EXHAUSTED (CWSANDBOX_LOG_QUERY_LIMIT_EXCEEDED)\
        \ with\n     RetryInfo: too many stored-log calls are in flight, or the query met\n     transient\
        \ pressure. Retry after the delay.\n   - UNAVAILABLE (CWSANDBOX_LOG_BACKEND_UNAVAILABLE) with\
        \ RetryInfo: the\n     stored-log backend is unavailable. Retry after the delay.\n   - UNAVAILABLE\
        \ (CWSANDBOX_FEATURE_FLAG_UNAVAILABLE): whether stored logs\n     are enabled could not be determined.\
        \ Retry later.\n   - UNAVAILABLE (CWSANDBOX_BACKEND_UNAVAILABLE) with RetryInfo: the\n     sandbox's\
        \ stored-log state could not be read. Retry after the delay.\n   - UNIMPLEMENTED (CWSANDBOX_NOT_IMPLEMENTED):\
        \ the deployment does not\n     serve stored logs."
      parameters:
      - name: sandboxId
        in: path
        required: true
        schema:
          type: string
      - name: startTime
        in: query
        description: Inclusive start of the time range. Defaults to one hour before the earlier of endTime
          and the effective read window's end. A request covers at most 24 hours and is narrowed to the
          read window. That window starts five minutes before log collection began and ends five minutes
          after the sandbox's terminal time (or the request time for a running sandbox). A range outside
          that window returns no lines.
        schema:
          type: string
          format: date-time
      - name: endTime
        in: query
        description: Exclusive end of the time range. Defaults to just after the effective read window
          ends, five minutes after the sandbox terminates, or five minutes after the request time while
          it runs.
        schema:
          type: string
          format: date-time
      - name: container
        in: query
        description: "Container name. Empty selects every workload container. Platform sidecar\n names\
          \ are INVALID_ARGUMENT (CWSANDBOX_INVALID_REQUEST)."
        schema:
          type: string
      - name: stream
        in: query
        description: Output stream. Unspecified selects both.
        schema:
          type: string
          format: enum
          enum:
          - SANDBOX_LOG_STREAM_UNSPECIFIED
          - SANDBOX_LOG_STREAM_STDOUT
          - SANDBOX_LOG_STREAM_STDERR
      - name: textContains
        in: query
        description: "Return only lines whose body contains this literal byte sequence (case\n sensitive,\
          \ no wildcards). 3 to 256 bytes. Requires explicit start_time\n and end_time at most one hour\
          \ apart."
        schema:
          type: string
      - name: pageSize
        in: query
        description: "Maximum entries per page. 0 means 100; values above 1000 are treated as\n 1000;\
          \ negative values are INVALID_ARGUMENT. A page may hold fewer\n entries, so continue while next_page_token\
          \ is set."
        schema:
          type: integer
          format: int32
      - name: pageToken
        in: query
        description: nextPageToken from the previous page. Keep the time fields, container, stream, textContains,
          and order unchanged from the request that returned it. pageSize can change between pages. A
          token expires 60 minutes after it is issued.
        schema:
          type: string
      - name: order
        in: query
        description: Page order. Unspecified is ascending.
        schema:
          type: string
          format: enum
          enum:
          - LIST_SANDBOX_LOGS_ORDER_UNSPECIFIED
          - LIST_SANDBOX_LOGS_ORDER_ASC
          - LIST_SANDBOX_LOGS_ORDER_DESC
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/coreweave.sandbox.v1.ListSandboxLogsResponse'
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/google.rpc.Status'
      tags:
      - SandboxService
    delete:
      operationId: SandboxService_DeleteSandboxLogs
      description: "DeleteSandboxLogs deletes a sandbox's stored logs: the stored stdout and\n stderr\
        \ history that ListSandboxLogs serves. Only an ended sandbox's logs\n can be deleted. The creating\
        \ user, or a caller with the sandbox_admin\n action in the sandbox's organization, can delete\
        \ them; a caller who\n cannot see the sandbox gets the same error as GetSandbox.\n\n From the\
        \ moment the call returns, ListSandboxLogs refuses the sandbox\n with CWSANDBOX_LOGS_DELETED;\
        \ a page already being served may still\n complete. Under normal load, while the service is healthy,\
        \ the lines are\n removed from log storage within 24 hours of the request; the storage's\n object\
        \ store and backups follow on the managed storage service's own\n schedule. The delete covers\
        \ the stored history this API serves, not\n copies in node-local files or in CoreWeave's internal\
        \ operational\n logging. DeleteSandbox stops a sandbox and leaves its stored logs\n readable;\
        \ it does not delete them.\n\n The call is idempotent: repeating it returns the first call's\n\
        \ deleted_at. It also succeeds for an ended sandbox whose logs were never\n stored or have expired.\n\
        \n Errors:\n   - FAILED_PRECONDITION (CWSANDBOX_SANDBOX_NOT_TERMINAL): the sandbox has\n     not\
        \ ended. Stop it, then retry.\n   - FAILED_PRECONDITION (CWSANDBOX_LOGS_NOT_ENABLED): stored logs\
        \ are not\n     enabled for the organization.\n   - RESOURCE_EXHAUSTED (CWSANDBOX_LOG_QUERY_LIMIT_EXCEEDED)\
        \ with\n     RetryInfo: the organization made more than 10 deletes in the current\n     second,\
        \ or too many stored-log calls are in flight. Retry after the\n     delay.\n   - UNAVAILABLE (CWSANDBOX_LOG_BACKEND_UNAVAILABLE)\
        \ with RetryInfo: the\n     stored-log backend is unavailable. Retry after the delay.\n   - UNAVAILABLE\
        \ (CWSANDBOX_FEATURE_FLAG_UNAVAILABLE): whether stored logs\n     are enabled could not be determined.\
        \ Retry later.\n   - UNAVAILABLE (CWSANDBOX_BACKEND_UNAVAILABLE) with RetryInfo: the\n     sandbox's\
        \ stored-log state could not be read. Retry after the delay.\n   - UNIMPLEMENTED (CWSANDBOX_NOT_IMPLEMENTED):\
        \ the deployment does not\n     serve stored logs."
      parameters:
      - name: sandboxId
        in: path
        required: true
        schema:
          type: string
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/coreweave.sandbox.v1.DeleteSandboxLogsResponse'
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/google.rpc.Status'
      tags:
      - SandboxService
  /v1/sandboxes/{sandboxId}:connect:
    post:
      operationId: SandboxService_ConnectSandbox
      summary: Connect sandbox
      description: "ConnectSandbox issues short-lived client credentials and returns\n the direct data-plane\
        \ endpoint for a running sandbox. The client generates\n and retains the private key; this method\
        \ accepts only its signed CSR."
      parameters:
      - name: sandboxId
        in: path
        required: true
        schema:
          type: string
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/coreweave.sandbox.v1.ConnectSandboxRequest'
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/coreweave.sandbox.v1.SandboxConnection'
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/google.rpc.Status'
      servers:
      - url: https://api.cwsandbox.com
        description: CoreWeave sandbox data plane.
      tags:
      - SandboxService
  /v1/sandboxes/{sandboxId}:exec:
    post:
      operationId: SandboxService_Exec
      summary: Exec
      description: "Exec runs a command to completion in a container and returns buffered\n output. Use\
        \ StreamExec for interactive or large-output commands."
      parameters:
      - name: sandboxId
        in: path
        required: true
        schema:
          type: string
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/coreweave.sandbox.v1.ExecRequest'
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/coreweave.sandbox.v1.ExecResponse'
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/google.rpc.Status'
      servers:
      - url: https://api.cwsandbox.com
        description: CoreWeave sandbox data plane.
      tags:
      - SandboxService
  /v1/sandboxes/{sandboxId}:readFile:
    get:
      operationId: SandboxService_ReadFile
      summary: Read file
      description: ReadFile reads a file from a container's filesystem.
      parameters:
      - name: sandboxId
        in: path
        required: true
        schema:
          type: string
      - name: path
        in: query
        schema:
          type: string
      - name: container
        in: query
        description: "Target container name. Empty = the primary. Unknown names and\n platform sidecar\
          \ names are INVALID_ARGUMENT (CWSANDBOX_INVALID_REQUEST).\n In a CONTROL_CONTAINER_ENGINE sandbox,\
          \ cws-engine is the only container\n and the primary."
        schema:
          type: string
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/coreweave.sandbox.v1.ReadFileResponse'
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/google.rpc.Status'
      servers:
      - url: https://api.cwsandbox.com
        description: CoreWeave sandbox data plane.
      tags:
      - SandboxService
  /v1/sandboxes/{sandboxId}:snapshot:
    post:
      operationId: SandboxService_CreateFileSystemSnapshot
      summary: Create file system snapshot
      description: "CreateFileSystemSnapshot snapshots a volume of a RUNNING sandbox to durable\n storage.\
        \ Returns the snapshot in SNAPSHOT_STATE_CREATING; poll Get."
      parameters:
      - name: sandboxId
        in: path
        required: true
        schema:
          type: string
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/coreweave.sandbox.v1.CreateFileSystemSnapshotRequest'
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/coreweave.sandbox.v1.FileSystemSnapshot'
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/google.rpc.Status'
      servers:
      - url: https://api.cwsandbox.com
        description: CoreWeave sandbox data plane.
      tags:
      - SandboxService
  /v1/sandboxes/{sandboxId}:writeFile:
    post:
      operationId: SandboxService_WriteFile
      summary: Write file
      description: WriteFile writes (creates or overwrites) a file in a container's filesystem.
      parameters:
      - name: sandboxId
        in: path
        required: true
        schema:
          type: string
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/coreweave.sandbox.v1.WriteFileRequest'
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/coreweave.sandbox.v1.WriteFileResponse'
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/google.rpc.Status'
      servers:
      - url: https://api.cwsandbox.com
        description: CoreWeave sandbox data plane.
      tags:
      - SandboxService
  /v1/sandboxes:createFromFile:
    post:
      operationId: SandboxService_CreateSandboxFromFile
      summary: Create sandbox from file
      description: "CreateSandboxFromFile launches a sandbox from an uploaded file (AIP-136\n custom method).\
        \ Unspecified type is INVALID_ARGUMENT\n (CWSANDBOX_INVALID_REQUEST) on type. Other declared types\
        \ than Compose\n (SANDBOX_FILE_TYPE_COMPOSE) are UNIMPLEMENTED (CWSANDBOX_NOT_IMPLEMENTED)\n on\
        \ type. control selects who controls the sandbox's containers (see\n Control).\n\n When every\
        \ Compose service has a pullable image (`image:` or\n image_overrides), the sandbox is returned\
        \ in STATE_CREATING. When a\n service still needs a build, the sandbox is returned in STATE_PREPARING,\n\
        \ its images are built without further calls, and it is placed with\n digest-pinned images once\
        \ every build succeeds. A failed build ends it in\n STATE_FAILED with a state_reason starting\
        \ with \"build_\"; fetch the failed\n build's output with GetSandboxBuildLogs. Stop and Delete\n\
        \ end a preparing sandbox in STATE_TERMINATED.\n\n Builds run with the caller's CoreWeave API\
        \ token and need the\n organization's Compose build storage to be enabled. Otherwise the create\n\
        \ is FAILED_PRECONDITION (CWSANDBOX_PRECONDITION_FAILED) with a\n PreconditionFailure of type\
        \ COREWEAVE_CREDENTIAL_REQUIRED or\n BUILD_STORAGE_NOT_ENABLED. When build capacity is full the\
        \ create is\n RESOURCE_EXHAUSTED (CWSANDBOX_BUILD_CAPACITY_EXHAUSTED) with RetryInfo;\n the refused\
        \ request_id may be reused for the retry. A deployment without\n builds returns UNIMPLEMENTED\
        \ (CWSANDBOX_NOT_IMPLEMENTED) on the service's\n build, after build_context_objects and builder_sizes\
        \ are validated."
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/coreweave.sandbox.v1.CreateSandboxFromFileRequest'
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/coreweave.sandbox.v1.Sandbox'
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/google.rpc.Status'
      servers:
      - url: https://api.cwsandbox.com
        description: CoreWeave sandbox data plane.
      tags:
      - SandboxService
  /v1/sandboxes:createFromTemplate:
    post:
      operationId: SandboxService_CreateSandboxFromTemplate
      summary: Create sandbox from template
      description: "CreateSandboxFromTemplate launches a sandbox by merging an organization-\n scoped\
        \ SandboxTemplate with optional replace-on-presence overrides\n (AIP-136 custom method). Returns\
        \ immediately with the sandbox in\n STATE_CREATING; poll GetSandbox for STATE_RUNNING / terminal\
        \ states."
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/coreweave.sandbox.v1.CreateSandboxFromTemplateRequest'
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/coreweave.sandbox.v1.Sandbox'
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/google.rpc.Status'
      servers:
      - url: https://api.cwsandbox.com
        description: CoreWeave sandbox data plane.
      tags:
      - SandboxService
  /v1/sandboxes:purge:
    post:
      operationId: SandboxService_PurgeSandboxes
      summary: Purge sandboxes
      description: "PurgeSandboxes terminates active sandboxes matching the selected scope\n (criteria-based\
        \ bulk delete). It terminates the matched sandboxes by default;\n set dry_run=true to instead\
        \ report how many sandboxes would be purged without\n terminating anything. The request must specify\
        \ exactly one scope selector:\n tags for targeted purge, or purge_all=true for every in-scope\
        \ sandbox. Scope\n follows DeleteSandbox: always within the caller's organization, restricted\
        \ to\n the caller's own sandboxes unless the caller holds the sandbox_admin action,\n which purges\
        \ across the organization. Only active sandboxes are ever in\n scope; terminal ones are skipped.\
        \ Termination is best-effort — ids that fail\n to terminate are returned in failed_sandbox_ids.\
        \ If the RPC itself returns an\n error after matching begins, some sandboxes may already have\
        \ been terminated\n and no partial response body is returned; retry the same filter to converge."
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/coreweave.sandbox.v1.PurgeSandboxesRequest'
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/coreweave.sandbox.v1.PurgeSandboxesResponse'
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/google.rpc.Status'
      servers:
      - url: https://api.cwsandbox.com
        description: CoreWeave sandbox data plane.
      tags:
      - SandboxService
  /v1/settings/buildStorageConfig:
    get:
      operationId: SettingsService_GetBuildStorageConfig
      summary: Get build storage configuration
      description: "GetBuildStorageConfig returns the caller organization's current Compose\n build storage\
        \ configuration. NOT_FOUND means it has not been configured."
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/coreweave.sandbox.v1.BuildStorageConfig'
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/google.rpc.Status'
      servers:
      - url: https://api.cwsandbox.com
        description: CoreWeave sandbox data plane.
      tags:
      - SettingsService
    patch:
      operationId: SettingsService_UpdateBuildStorageConfig
      summary: Update build storage configuration
      description: "UpdateBuildStorageConfig creates or updates the organization's Compose\n build storage\
        \ configuration. Requires sandbox_admin. Enabling storage\n requires authenticating with the caller's\
        \ own CoreWeave API token; other\n credentials receive FAILED_PRECONDITION. Enabling managed storage\n\
        \ provisions its dedicated bucket and applies its access and lifecycle\n policies. Enabling customer-owned\
        \ storage applies the build-log lifecycle\n rules and checks context reads and build-log writes\
        \ with the caller's\n token. In both modes, setup adds the expire-bob-builds rule to the registry\n\
        \ namespace's lifecycle policy with the caller's token, preserving other\n rules. It enables a\
        \ disabled policy only when that is its only rule and\n otherwise returns FAILED_PRECONDITION.\
        \ A setup failure leaves the new\n revision disabled; Get returns its current etag for the next\
        \ update."
      parameters:
      - name: updateMask
        in: query
        description: 'Comma-separated JSON paths: enabled, mode, bucketName, location, registryNamespace,
          and billingReference. An omitted or empty mask replaces all writable configuration fields. A
          populated mask requires an existing configuration; omit the mask for initial creation. The etag
          is always checked independently of this mask. The wildcard * is supported only over binary protobuf
          (gRPC or Connect protobuf), not JSON Connect or the REST updateMask query value.'
        schema:
          type: string
          format: field-mask
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/coreweave.sandbox.v1.BuildStorageConfig'
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/coreweave.sandbox.v1.BuildStorageConfig'
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/google.rpc.Status'
      servers:
      - url: https://api.cwsandbox.com
        description: CoreWeave sandbox data plane.
      tags:
      - SettingsService
  /v1/settings/fileSystemSnapshotBucketConfig:
    get:
      operationId: SettingsService_GetFileSystemSnapshotBucketConfig
      summary: Get file system snapshot bucket config
      description: GetFileSystemSnapshotBucketConfig returns the org's FSS bucket config.
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/coreweave.sandbox.v1.FileSystemSnapshotBucketConfig'
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/google.rpc.Status'
      servers:
      - url: https://api.cwsandbox.com
        description: CoreWeave sandbox data plane.
      tags:
      - SettingsService
    patch:
      operationId: SettingsService_UpdateFileSystemSnapshotBucketConfig
      summary: Update file system snapshot bucket config
      description: "UpdateFileSystemSnapshotBucketConfig sets the org's FSS bucket config. An\n empty\
        \ bucket_name reverts the org to CoreWeave-managed."
      parameters:
      - name: updateMask
        in: query
        description: Comma-separated JSON paths to update. An omitted or empty mask replaces the whole
          configuration. The wildcard * is supported only over binary protobuf (gRPC or Connect protobuf),
          not JSON Connect or the REST updateMask query value.
        schema:
          type: string
          format: field-mask
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/coreweave.sandbox.v1.FileSystemSnapshotBucketConfig'
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/coreweave.sandbox.v1.FileSystemSnapshotBucketConfig'
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/google.rpc.Status'
      servers:
      - url: https://api.cwsandbox.com
        description: CoreWeave sandbox data plane.
      tags:
      - SettingsService
  /v1/settings/objectStorageWifConfig:
    get:
      operationId: SettingsService_GetObjectStorageWifConfig
      summary: Get object storage WIF config
      description: GetObjectStorageWifConfig returns the org's object-storage WIF config.
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/coreweave.sandbox.v1.ObjectStorageWifConfig'
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/google.rpc.Status'
      servers:
      - url: https://api.cwsandbox.com
        description: CoreWeave sandbox data plane.
      tags:
      - SettingsService
    delete:
      operationId: SettingsService_DeleteObjectStorageWifConfig
      summary: Delete object storage WIF config
      description: "DeleteObjectStorageWifConfig removes the org's WIF config; afterward new\n object_storage_access\
        \ requests are rejected (distinct from enabled=false)."
      parameters:
      - name: allowMissing
        in: query
        description: If true, deleting an absent config succeeds instead of returning NOT_FOUND.
        schema:
          type: boolean
      responses:
        '200':
          description: OK
          content: {}
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/google.rpc.Status'
      servers:
      - url: https://api.cwsandbox.com
        description: CoreWeave sandbox data plane.
      tags:
      - SettingsService
    patch:
      operationId: SettingsService_UpdateObjectStorageWifConfig
      summary: Update object storage WIF config
      description: UpdateObjectStorageWifConfig creates or updates the org's WIF config.
      parameters:
      - name: updateMask
        in: query
        description: Comma-separated JSON paths to update. An omitted or empty mask replaces the whole
          configuration. The wildcard * is supported only over binary protobuf (gRPC or Connect protobuf),
          not JSON Connect or the REST updateMask query value.
        schema:
          type: string
          format: field-mask
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/coreweave.sandbox.v1.ObjectStorageWifConfig'
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/coreweave.sandbox.v1.ObjectStorageWifConfig'
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/google.rpc.Status'
      servers:
      - url: https://api.cwsandbox.com
        description: CoreWeave sandbox data plane.
      tags:
      - SettingsService
  /v1/settings/secretStores:
    get:
      operationId: SettingsService_ListSecretStores
      summary: List secret stores
      description: ListSecretStores lists the caller's secret stores.
      parameters:
      - name: pageSize
        in: query
        schema:
          type: integer
          format: int32
      - name: pageToken
        in: query
        schema:
          type: string
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/coreweave.sandbox.v1.ListSecretStoresResponse'
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/google.rpc.Status'
      servers:
      - url: https://api.cwsandbox.com
        description: CoreWeave sandbox data plane.
      tags:
      - SettingsService
    post:
      operationId: SettingsService_CreateSecretStore
      summary: Create secret store
      description: CreateSecretStore registers a secret store for the caller's organization.
      parameters:
      - name: requestId
        in: query
        description: "Optional idempotency token; repeated identical requests with the same token\n return\
          \ the original result."
        schema:
          type: string
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/coreweave.sandbox.v1.SecretStore'
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/coreweave.sandbox.v1.SecretStore'
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/google.rpc.Status'
      servers:
      - url: https://api.cwsandbox.com
        description: CoreWeave sandbox data plane.
      tags:
      - SettingsService
  /v1/settings/secretStores/{name}:
    get:
      operationId: SettingsService_GetSecretStore
      summary: Get secret store
      description: GetSecretStore returns a secret store by name.
      parameters:
      - name: name
        in: path
        required: true
        schema:
          type: string
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/coreweave.sandbox.v1.SecretStore'
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/google.rpc.Status'
      servers:
      - url: https://api.cwsandbox.com
        description: CoreWeave sandbox data plane.
      tags:
      - SettingsService
    delete:
      operationId: SettingsService_DeleteSecretStore
      summary: Delete secret store
      description: DeleteSecretStore removes a secret store by name.
      parameters:
      - name: name
        in: path
        required: true
        schema:
          type: string
      - name: allowMissing
        in: query
        description: If true, deleting an absent store succeeds instead of returning NOT_FOUND.
        schema:
          type: boolean
      responses:
        '200':
          description: OK
          content: {}
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/google.rpc.Status'
      servers:
      - url: https://api.cwsandbox.com
        description: CoreWeave sandbox data plane.
      tags:
      - SettingsService
  /v1/settings/secretStores/{secret_store.name}:
    patch:
      operationId: SettingsService_UpdateSecretStore
      summary: Update secret store
      description: UpdateSecretStore updates a secret store (identified by secret_store.name).
      parameters:
      - name: secret_store.name
        in: path
        required: true
        schema:
          type: string
      - name: updateMask
        in: query
        description: Comma-separated JSON paths to update. An omitted or empty mask replaces the whole
          store. The wildcard * is supported only over binary protobuf (gRPC or Connect protobuf), not
          JSON Connect or the REST updateMask query value.
        schema:
          type: string
          format: field-mask
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/coreweave.sandbox.v1.SecretStore'
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/coreweave.sandbox.v1.SecretStore'
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/google.rpc.Status'
      servers:
      - url: https://api.cwsandbox.com
        description: CoreWeave sandbox data plane.
      tags:
      - SettingsService
  /v1/volumes:
    get:
      operationId: VolumeService_ListVolumes
      summary: List volumes
      parameters:
      - name: pageSize
        in: query
        schema:
          type: integer
          format: int32
      - name: pageToken
        in: query
        schema:
          type: string
      - name: states
        in: query
        description: Return volumes matching any listed state. VOLUME_STATE_UNSPECIFIED entries are ignored.
          If no recognized states remain, no state filter applies.
        schema:
          type: array
          items:
            enum:
            - VOLUME_STATE_UNSPECIFIED
            - VOLUME_STATE_VALIDATING
            - VOLUME_STATE_READY
            - VOLUME_STATE_ERROR
            - VOLUME_STATE_DELETING
            type: string
            format: enum
      - name: runnerIds
        in: query
        description: 'Filter: pvc volumes owned by any of these runners.'
        schema:
          type: array
          items:
            type: string
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/coreweave.sandbox.v1.ListVolumesResponse'
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/google.rpc.Status'
      servers:
      - url: https://api.cwsandbox.com
        description: CoreWeave sandbox data plane.
      tags:
      - VolumeService
    post:
      operationId: VolumeService_CreateVolume
      summary: Create volume
      description: "CreateVolume registers a Volume. Returns immediately in\n VOLUME_STATE_VALIDATING;\
        \ poll GetVolume for READY/ERROR."
      parameters:
      - name: requestId
        in: query
        schema:
          type: string
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/coreweave.sandbox.v1.Volume'
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/coreweave.sandbox.v1.Volume'
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/google.rpc.Status'
      servers:
      - url: https://api.cwsandbox.com
        description: CoreWeave sandbox data plane.
      tags:
      - VolumeService
  /v1/volumes/{volumeId}:
    get:
      operationId: VolumeService_GetVolume
      summary: Get volume
      parameters:
      - name: volumeId
        in: path
        required: true
        schema:
          type: string
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/coreweave.sandbox.v1.Volume'
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/google.rpc.Status'
      servers:
      - url: https://api.cwsandbox.com
        description: CoreWeave sandbox data plane.
      tags:
      - VolumeService
    delete:
      operationId: VolumeService_DeleteVolume
      summary: Delete volume
      description: "DeleteVolume deregisters a Volume. Deletion is asynchronous: the returned\n resource\
        \ is in VOLUME_STATE_DELETING while platform-created mount\n plumbing is cleaned up, after which\
        \ GetVolume returns NOT_FOUND. The\n source storage and its data are never touched. Fails FAILED_PRECONDITION\n\
        \ (CWSANDBOX_VOLUME_IN_USE) while non-terminal sandboxes are attached."
      parameters:
      - name: volumeId
        in: path
        required: true
        schema:
          type: string
      - name: allowMissing
        in: query
        description: If true, deleting an absent volume succeeds instead of returning NOT_FOUND.
        schema:
          type: boolean
      - name: force
        in: query
        description: "Force deletion when the owning runner is permanently gone: hard-deletes\n the registration\
          \ without waiting for plumbing cleanup, delegating any\n surviving platform-created objects\
          \ to the background sweep. Never touches\n the source storage or its data."
        schema:
          type: boolean
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/coreweave.sandbox.v1.Volume'
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/google.rpc.Status'
      servers:
      - url: https://api.cwsandbox.com
        description: CoreWeave sandbox data plane.
      tags:
      - VolumeService
    patch:
      operationId: VolumeService_UpdateVolume
      summary: Update volume
      description: Update mutable volume fields. An omitted or empty updateMask selects full replacement;
        resend immutable volumeId, spec.pvc, and spec.readOnly unchanged or the update returns INVALID_ARGUMENT.
        Use the explicit JSON path spec.description to update only the description. The wildcard * is
        supported only over binary protobuf (gRPC or Connect protobuf), not JSON Connect or the REST updateMask
        query value.
      parameters:
      - name: volumeId
        in: path
        required: true
        schema:
          type: string
      - name: updateMask
        in: query
        description: Comma-separated JSON paths to update. Only spec.description is mutable. An omitted
          or empty mask selects full replacement and requires immutable fields to be resent unchanged.
          The wildcard * is supported only over binary protobuf (gRPC or Connect protobuf), not JSON Connect
          or the REST updateMask query value.
        schema:
          type: string
          format: field-mask
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/coreweave.sandbox.v1.Volume'
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/coreweave.sandbox.v1.Volume'
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/google.rpc.Status'
      servers:
      - url: https://api.cwsandbox.com
        description: CoreWeave sandbox data plane.
      tags:
      - VolumeService
  /v1/volumes/{volumeId}:validate:
    post:
      operationId: VolumeService_ValidateVolume
      summary: Validate volume
      description: "ValidateVolume triggers an on-demand re-validation of the volume's\n backing source\
        \ — the same checks the platform runs periodically."
      parameters:
      - name: volumeId
        in: path
        required: true
        schema:
          type: string
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/coreweave.sandbox.v1.Volume'
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/google.rpc.Status'
      servers:
      - url: https://api.cwsandbox.com
        description: CoreWeave sandbox data plane.
      tags:
      - VolumeService
components:
  schemas:
    coreweave.sandbox.v1.ActiveSandboxQuota:
      description: "ActiveSandboxQuota bounds concurrent live sandboxes for a pool. Enforcement\n COUNTS\
        \ a sandbox against its TENANT (owner) org; these values are the ceiling\n applied per tenant\
        \ and per user to every tenant placing into the pool. A\n value of 0 is a valid, fail-closed cap\
        \ (nothing may create)."
      type: object
      properties:
        maxActiveSandboxesPerTenant:
          description: Max concurrent live sandboxes one tenant org may hold in this pool.
          type: integer
          format: int32
        maxActiveSandboxesPerUser:
          description: Max concurrent live sandboxes one user may hold in this pool.
          type: integer
          format: int32
    coreweave.sandbox.v1.AnnotationPair:
      description: AnnotationPair is a Kubernetes annotation key/value pair.
      type: object
      properties:
        key:
          type: string
        value:
          type: string
      required:
      - key
      - value
    coreweave.sandbox.v1.AvailableRunner:
      description: "AvailableRunner is a caller-facing view of a runner. Sensitive internals\n (cluster,\
        \ namespace) are omitted."
      type: object
      properties:
        runnerId:
          type: string
          readOnly: true
        runnerGroupId:
          type: string
          readOnly: true
        tags:
          type: array
          items:
            type: string
          readOnly: true
        healthy:
          type: boolean
          readOnly: true
        capabilities:
          description: "Reported features and aggregate capacity ceilings; included at BASIC and\n FULL\
            \ views when capability information is available."
          allOf:
          - $ref: '#/components/schemas/coreweave.sandbox.v1.RunnerCapabilitySummary'
          readOnly: true
        resources:
          description: "Dynamic availability; populated at FULL view for owned runners only (unset\n for\
            \ shared-org runners)."
          allOf:
          - $ref: '#/components/schemas/coreweave.sandbox.v1.RunnerResourceSummary'
          readOnly: true
        connectedAt:
          type: string
          format: date-time
          readOnly: true
        isShared:
          description: True if the runner belongs to a shared organization (resources omitted).
          type: boolean
          readOnly: true
        organizationId:
          description: "Organization that owns the runner. Runner identity is the pair\n (organization_id,\
            \ runner_id); runner_id alone is not globally unique."
          type: string
          readOnly: true
    coreweave.sandbox.v1.BuildContextObject:
      description: "BuildContextObject names one exact version of a gzip-compressed tar build\n context\
        \ in CoreWeave AI Object Storage. The caller's credential must be able\n to read it; the platform\
        \ never modifies or deletes it."
      type: object
      properties:
        location:
          description: "Object-storage location. Must equal the organization's build storage\n location."
          type: string
        bucket:
          description: Bucket that holds the object.
          type: string
        key:
          description: Object key, at most 1024 bytes.
          type: string
        versionId:
          description: "Exact object version, at most 1024 bytes. The build reads this version\n only.\
            \ Unversioned objects (version \"null\") are rejected."
          type: string
      required:
      - location
      - bucket
      - key
      - versionId
    coreweave.sandbox.v1.BuildStorageConfig:
      description: "BuildStorageConfig is the organization's current Compose build storage\n configuration.\
        \ Build contexts are stored under the contexts/ prefix and\n failed-build logs under the bob-build-logs/\
        \ prefix of the selected bucket.\n Existing builds retain the revision selected at admission."
      type: object
      properties:
        enabled:
          description: "Whether new builds may use this configuration. Setting false preserves\n existing\
            \ builds and does not provision or validate storage."
          type: boolean
        mode:
          description: Storage ownership mode. Specify a concrete mode on initial configuration, full
            replacement, or an update that selects mode. BUILD_STORAGE_MODE_UNSPECIFIED is invalid in
            these writes. A partial update that excludes mode preserves the existing mode.
          type: string
          format: enum
          enum:
          - BUILD_STORAGE_MODE_UNSPECIFIED
          - BUILD_STORAGE_MODE_MANAGED
          - BUILD_STORAGE_MODE_CUSTOMER_OWNED
        bucketName:
          description: Required in CUSTOMER_OWNED mode; must be empty in MANAGED mode.
          type: string
        location:
          description: "Object-storage location. Required on initial configuration/full replacement.\n\
            \ The location of an existing managed bucket can't change."
          type: string
        registryNamespace:
          description: "Customer-owned CWCR namespace for build images. Required on initial\n configuration\
            \ and full replacement."
          type: string
        billingReference:
          description: "Customer billing attribution reference. Required on initial configuration\n and\
            \ full replacement."
          type: string
        etag:
          description: "Opaque revision token. Omit only for initial configuration. Send the value\n returned\
            \ by Get when updating; a stale value returns FAILED_PRECONDITION."
          type: string
        revision:
          description: Monotonically increasing revision, retained for existing builds.
          type: string
          readOnly: true
        effectiveBucketName:
          description: "Actual bucket selected for this revision. It may still be awaiting\n provisioning\
            \ when enabled is false."
          type: string
          readOnly: true
    coreweave.sandbox.v1.CidrBlock:
      description: CidrBlock is an IP range with optional carved-out sub-ranges.
      type: object
      properties:
        cidr:
          description: CIDR, e.g. "0.0.0.0/0" or "203.0.113.0/24".
          type: string
        except:
          description: Sub-ranges of cidr excluded from this rule.
          type: array
          items:
            type: string
      required:
      - cidr
    coreweave.sandbox.v1.ConnectSandboxRequest:
      description: "ConnectSandboxRequest requests sandbox-scoped direct-connection\n credentials. The\
        \ sandbox must be running and its Runner must advertise a\n compatible direct data-plane endpoint."
      type: object
      properties:
        sandboxId:
          type: string
        csrDer:
          description: "DER-encoded PKCS #10 certificate signing request. The issuer validates the\n proof-of-possession\
            \ signature and copies only the public key; requested\n identity, extensions, and lifetime\
            \ are ignored."
          type: string
          format: bytes
        requestedPermissions:
          description: Operations to authorize on the issued certificate. At least one concrete permission
            is required. SANDBOX_DATA_PERMISSION_UNSPECIFIED and unknown values are invalid. The server
            returns only permissions allowed for the caller.
          type: array
          items:
            enum:
            - SANDBOX_DATA_PERMISSION_UNSPECIFIED
            - SANDBOX_DATA_PERMISSION_EXEC
            - SANDBOX_DATA_PERMISSION_STREAM_EXEC
            - SANDBOX_DATA_PERMISSION_STREAM_LOGS
            - SANDBOX_DATA_PERMISSION_WRITE_FILE
            - SANDBOX_DATA_PERMISSION_READ_FILE
            type: string
            format: enum
      required:
      - sandboxId
      - csrDer
      - requestedPermissions
    coreweave.sandbox.v1.Container:
      description: Container is one container in a sandbox.
      type: object
      properties:
        name:
          description: "Unique name within the sandbox; used as the runtime container name and\n to target\
            \ operations and mount volumes. Must be a DNS-1123 label.\n Must not be cw-object-store-agent,\
            \ cw-object-store-agent-restore,\n cws-engine, dns-egress, dns-egress-probe, or start with\n\
            \ cw-object-store-agent-restore-. Duplicate or reserved names are\n INVALID_ARGUMENT (CWSANDBOX_INVALID_REQUEST)."
          type: string
        image:
          description: OCI image to run.
          type: string
        command:
          description: Command to run. If empty, the image's entrypoint is used.
          type: string
        args:
          description: Arguments to the command.
          type: array
          items:
            type: string
        environmentVariables:
          description: Environment variables injected into the container.
          type: object
          additionalProperties:
            type: string
        resources:
          description: "Guaranteed compute allocation for this container. Preserved for existing v1\n\
            \ clients. For burstable allocations, use resource_requirements instead."
          allOf:
          - $ref: '#/components/schemas/coreweave.sandbox.v1.Resources'
        files:
          description: Files written into this container's filesystem at startup.
          type: array
          items:
            $ref: '#/components/schemas/coreweave.sandbox.v1.FileMount'
        volumeMounts:
          description: Volumes (from SandboxSpec.volumes) to mount into this container.
          type: array
          items:
            $ref: '#/components/schemas/coreweave.sandbox.v1.VolumeMount'
        secretStores:
          description: "External secret stores to resolve and inject as environment variables\n into this\
            \ container only. Other containers on the same sandbox do not\n receive these values. Referencing\
            \ a store that is not provisioned for\n the caller returns FAILED_PRECONDITION\n (CWSANDBOX_SECRET_STORE_NOT_PROVISIONED)."
          type: array
          items:
            $ref: '#/components/schemas/coreweave.sandbox.v1.SecretStoreReference'
        workingDir:
          description: Working directory for the command. Defaults to the image's working directory.
          type: string
        resourceRequirements:
          description: "Compute allocation for this container: requests (the guaranteed floor) and\n optional\
            \ limits (the burst ceiling). Guaranteed QoS when limits is empty or\n equals requests; Burstable\
            \ when limits exceeds requests. The sandbox is\n billed for the sum of requests across its\
            \ containers, which must not exceed\n the platform ceiling — an over-ceiling sandbox is rejected\
            \ with\n INVALID_ARGUMENT (CWSANDBOX_RESOURCE_CEILING_EXCEEDED), not silently reduced.\n Mutually\
            \ exclusive with resources. (Serverless pins limits == requests.)"
          allOf:
          - $ref: '#/components/schemas/coreweave.sandbox.v1.ResourceRequirements'
        securityContext:
          description: "In-guest security settings (privileged, capabilities, run-as user, …),\n contained\
            \ by the sandbox's isolation boundary and clamped by the runner's\n policy."
          allOf:
          - $ref: '#/components/schemas/coreweave.sandbox.v1.SecurityContext'
        imagePullCredentials:
          description: "Request-scoped image pull credentials for this container's image. The\n credential\
            \ value is resolved from a configured external secret store at\n create time and delivered\
            \ to the runner as generated Docker config JSON."
          allOf:
          - $ref: '#/components/schemas/coreweave.sandbox.v1.ImagePullCredentials'
        primary:
          description: "When true, this container is the primary: its exit is the sandbox\n outcome (exit_code\
            \ / COMPLETED / FAILED) and it is the default target\n for Exec, StreamExec, StreamLogs, ReadFile,\
            \ and WriteFile.\n\n One container: omit or false — that container is primary. true is also\n\
            \ accepted.\n More than one container: exactly one must be true. None set, or more\n than\
            \ one true, is INVALID_ARGUMENT (CWSANDBOX_INVALID_REQUEST)."
          type: boolean
        startupProbe:
          description: "Exec probe that must succeed before this container is started. On a\n non-primary\
            \ container, the next container waits. On the primary, a\n failed probe can fail the sandbox\
            \ after retries. CreateSandbox omitted\n timings use Probe defaults. An empty probe is omit."
          allOf:
          - $ref: '#/components/schemas/coreweave.sandbox.v1.Probe'
      required:
      - name
      - image
    coreweave.sandbox.v1.ContainerStatus:
      description: ContainerStatus is the observed state of a single container.
      type: object
      properties:
        name:
          type: string
          readOnly: true
        state:
          description: Reported container state. STATE_UNSPECIFIED means no state is specified.
          type: string
          format: enum
          enum:
          - STATE_UNSPECIFIED
          - STATE_CREATING
          - STATE_RUNNING
          - STATE_COMPLETED
          - STATE_FAILED
          - STATE_TERMINATING
          - STATE_TERMINATED
          - STATE_PENDING
          - STATE_PAUSED
          - STATE_PREPARING
          readOnly: true
        exitCode:
          description: Exit code; set once the container reaches COMPLETED or FAILED.
          type: integer
          format: int32
          readOnly: true
        restartCount:
          description: Number of times the container has restarted.
          type: integer
          format: int32
          readOnly: true
    coreweave.sandbox.v1.ControlPlaneAccessPolicy:
      description: "ControlPlaneAccessPolicy limits which network origins may use Sandbox API\n operations\
        \ that select this runner or target a Sandbox placed on it."
      type: object
      properties:
        sourceIpAllowlist:
          description: "Allowed public client source ranges. An absent allowlist leaves access\n unrestricted.\
            \ A present allowlist with no CIDRs denies every public\n source. Runner and platform lifecycle\
            \ traffic is not governed by it."
          allOf:
          - $ref: '#/components/schemas/coreweave.sandbox.v1.SourceIpAllowlist'
    coreweave.sandbox.v1.CreateFileSystemSnapshotRequest:
      type: object
      properties:
        sandboxId:
          type: string
        requestId:
          description: Optional idempotency token, limited to 128 UTF-8 bytes.
          type: string
        scratchVolumeName:
          description: "Which scratch volume to snapshot (the SandboxVolume.name of a scratch\n entry).\
            \ Registered-Volume-backed entries are not snapshottable (naming\n one fails with CWSANDBOX_VOLUME_NOT_SNAPSHOTTABLE)\
            \ and are excluded from\n the defaulting count. Optional when the sandbox has a single scratch\n\
            \ volume; required when it has more."
          type: string
      required:
      - sandboxId
    coreweave.sandbox.v1.CreateSandboxFromFileRequest:
      description: "CreateSandboxFromFileRequest is the AIP-136 body for CreateSandboxFromFile.\n This\
        \ list is closed: volumes, instance_type, runtime_class,\n runtime_class_selection, and published\
        \ services are not fields here; those\n callers use CreateSandbox. There is no PartialSandboxSpec\
        \ overlay.\n CONTROL_CONTAINER_ENGINE needs no runtime class field: the Runner's engine\n class\
        \ is used (see Control)."
      type: object
      properties:
        type:
          description: "Document type. Unspecified is INVALID_ARGUMENT. Compose is accepted for\n pull-only\
            \ documents. Other declared types are UNIMPLEMENTED."
          type: string
          format: enum
          enum:
          - SANDBOX_FILE_TYPE_UNSPECIFIED
          - SANDBOX_FILE_TYPE_COMPOSE
        contents:
          description: "UTF-8 file bytes. Compose: max 256 KiB. The platform keeps the file, or\n the\
            \ spec derived from it, for the life of the sandbox record, so put\n secrets in a secret store\
            \ rather than inline."
          type: string
          format: bytes
        primaryService:
          description: "Compose service that is the sandbox primary. Required when type is\n Compose and\
            \ control is CONTROL_PLATFORM; must name a service in contents.\n Set with CONTROL_CONTAINER_ENGINE,\
            \ it is INVALID_ARGUMENT\n (CWSANDBOX_INVALID_REQUEST)."
          type: string
        imageOverrides:
          description: "Per-service image refs. Keys must be services. Use this to supply a\n pullable\
            \ image for a service that would otherwise need a build.\n Valid only when type is Compose."
          type: object
          additionalProperties:
            type: string
        buildContexts:
          description: "Per-service gzip build-context tarballs for services that still need a\n build.\
            \ Keys must be services. Total 32 MiB. A service that still needs a\n build must not have\
            \ an entry here when its build.context is a remote URL.\n Entries for services with an image\
            \ are ignored. Valid only when type is\n Compose."
          type: object
          additionalProperties:
            type: string
            format: bytes
        defaultResources:
          description: "CPU/memory copied onto each service that omitted deploy.resources.\n Per container,\
            \ not a project budget. GPU in this message is\n INVALID_ARGUMENT. Valid only when type is\
            \ Compose."
          allOf:
          - $ref: '#/components/schemas/coreweave.sandbox.v1.ResourceRequirements'
        mode:
          description: Placement mode. Omit this field to use serverless placement. SANDBOX_MODE_UNSPECIFIED
            also selects SANDBOX_MODE_SERVERLESS. Set SANDBOX_MODE_CKS to use your own-cluster runners.
          type: string
          format: enum
          enum:
          - SANDBOX_MODE_UNSPECIFIED
          - SANDBOX_MODE_SERVERLESS
          - SANDBOX_MODE_CKS
        maxLifetimeSeconds:
          type: integer
          format: int32
        tags:
          type: array
          items:
            type: string
        network:
          $ref: '#/components/schemas/coreweave.sandbox.v1.NetworkOptions'
        networkIds:
          description: Network membership is not supported. v1 sandbox creation and stored template validation
            reject a non-empty networkIds list. Use network to configure network rules; this field does
            not join sandbox networks.
          type: array
          items:
            type: string
        objectStorageAccess:
          $ref: '#/components/schemas/coreweave.sandbox.v1.ObjectStorageAccess'
        annotations:
          type: object
          additionalProperties:
            type: string
        runnerIds:
          type: array
          items:
            type: string
        requestId:
          description: "Optional idempotency token; repeated identical requests with the same token\n\
            \ return the original result."
          type: string
        displayName:
          description: Optional name for the created sandbox. Uses Sandbox.display_name rules.
          type: string
        buildContextObjects:
          description: "Per-service build context stored in CoreWeave AI Object Storage, for\n contexts\
            \ larger than build_contexts allows. Keys must be services that\n still need a build. A service\
            \ with an entry here must not also have a\n build_contexts entry or a remote build.context.\
            \ At most 64 entries.\n Valid only when type is Compose."
          type: object
          additionalProperties:
            $ref: '#/components/schemas/coreweave.sandbox.v1.BuildContextObject'
        builderSizes:
          description: "Per-service builder size name, at most 64 bytes. Omitted services use the\n default\
            \ size. A size the build service does not offer is\n INVALID_ARGUMENT on builder_sizes.<service>.\
            \ Keys must be services that\n still need a build. At most 64 entries. Valid only when type\
            \ is Compose."
          type: object
          additionalProperties:
            type: string
        control:
          description: "Who controls the sandbox's containers (see Control). Unspecified means\n CONTROL_PLATFORM.\
            \ CONTROL_CONTAINER_ENGINE is valid only when type is\n Compose. A server that doesn't support\
            \ it returns UNIMPLEMENTED\n (CWSANDBOX_NOT_IMPLEMENTED). When no runner can run a container\
            \ engine,\n the create is FAILED_PRECONDITION (CWSANDBOX_NO_SUITABLE_RUNNER) with\n metadata\
            \ unsupported_feature=container_engine. A value the server\n doesn't recognize is UNIMPLEMENTED\
            \ (CWSANDBOX_NOT_IMPLEMENTED)."
          type: string
          format: enum
          enum:
          - CONTROL_UNSPECIFIED
          - CONTROL_PLATFORM
          - CONTROL_CONTAINER_ENGINE
        imagePullCredentials:
          description: "Registry credentials for pulling images, at most one per registry and at\n most\
            \ 16 entries. A repeated registry or a 17th entry is INVALID_ARGUMENT\n (CWSANDBOX_INVALID_REQUEST).\n\
            \ Credentials are resolved at create, as for\n Container.image_pull_credentials. With CONTROL_PLATFORM,\
            \ each container\n uses the credential whose registry matches its image. With\n CONTROL_CONTAINER_ENGINE,\
            \ the engine's Docker client holds every\n credential, and a credential here replaces the\
            \ platform's own for the\n same registry. Valid only when type is Compose. A deployment without\n\
            \ support returns UNIMPLEMENTED (CWSANDBOX_NOT_IMPLEMENTED)."
          type: array
          items:
            $ref: '#/components/schemas/coreweave.sandbox.v1.ImagePullCredentials'
      required:
      - type
      - contents
    coreweave.sandbox.v1.CreateSandboxFromTemplateRequest:
      description: Creates a sandbox from an organization-scoped SandboxTemplate. The service clones the
        template spec, applies overrides, then runs the CreateSandbox pipeline. In JSON overrides, present
        messages and maps replace whole fields, and non-empty lists replace whole lists. Empty JSON lists
        preserve template lists. Nonzero scalars and nonempty strings replace template values; zero or
        empty values preserve them. Container overrides replace the entire containers list and must be
        complete. See PartialSandboxSpec for the runtime-selection exception.
      type: object
      properties:
        templateId:
          description: Organization-scoped SandboxTemplate UUID.
          type: string
        overrides:
          description: Optional sparse overlay applied with replace-on-presence semantics.
          allOf:
          - $ref: '#/components/schemas/coreweave.sandbox.v1.PartialSandboxSpec'
        requestId:
          description: "Optional idempotency token; repeated identical requests with the same token\n\
            \ return the original result."
          type: string
        displayName:
          description: Optional name for the created sandbox. Uses Sandbox.display_name rules.
          type: string
      required:
      - templateId
    coreweave.sandbox.v1.DeleteSandboxLogsResponse:
      type: object
      properties:
        deletedAt:
          description: "When the deletion was recorded. A repeated call returns the first call's\n value."
          type: string
          format: date-time
          readOnly: true
    coreweave.sandbox.v1.DeleteSandboxResponse:
      type: object
      properties:
        sandbox:
          description: The sandbox, now in STATE_TERMINATING/STATE_TERMINATED.
          allOf:
          - $ref: '#/components/schemas/coreweave.sandbox.v1.Sandbox'
        fileSystemSnapshotIds:
          description: "One id per DeleteSandboxRequest.snapshot_volumes entry, in request order;\n poll\
            \ GetFileSystemSnapshot for terminal status. A returned id always means a\n snapshot row exists\
            \ (never a silent no-op). Termination proceeds regardless\n of snapshot outcome — for a guaranteed\
            \ snapshot, call CreateFileSystemSnapshot\n and confirm READY before deleting."
          type: array
          items:
            type: string
    coreweave.sandbox.v1.EgressRule:
      description: "EgressRule allows traffic to one destination class, optionally narrowed to\n specific\
        \ ports (destination AND ports; empty ports = all ports)."
      type: object
      properties:
        cidr:
          description: "An IP range with optional carve-outs. An except narrows only THIS rule's\n range\
            \ — another rule may still allow the excepted addresses."
          allOf:
          - $ref: '#/components/schemas/coreweave.sandbox.v1.CidrBlock'
        httpsHostname:
          description: "An HTTPS destination hostname, matched against TLS Server Name\n Indication (SNI):\
            \ exact (\"pypi.org\") or a single leftmost wildcard label\n (\"*.example.com\" matches \"\
            foo.example.com\", not \"bar.foo.example.com\").\n On Policy.allowed_egress, \"*\" entitles\
            \ every name; it is not a sandbox\n grant. No other pattern forms. On a sandbox this is a\
            \ hostname grant\n for HTTPS (TCP 443). On a name rule, ports must be empty or exactly\n TCP\
            \ 443; empty means this 443 path, not all ports. Any other ports\n list is rejected. On Policy.allowed_egress\
            \ it is a ceiling for those\n grants: every declared name must match an allowed pattern or\
            \ an `any`\n entitlement; a CIDR-only envelope does not entitle names. Carve names\n out of\
            \ this ceiling with https_hostname_except. Policy.default_egress must\n not set https_hostname\
            \ — a curated site set belongs on a SandboxTemplate.\n This rule authorizes HTTPS access,\
            \ not DNS queries or resolutions.\n Outbound DNS traffic is governed separately by network.dns_egress.\n\
            \ Requires a runner that can enforce hostname-based HTTPS rules;\n otherwise create is rejected\
            \ rather than ignoring the rule."
          type: string
        tenant:
          description: Other sandboxes, selected by tenant relationship. When selecting this destination,
            use TENANT_SCOPE_SAME_USER or TENANT_SCOPE_SAME_ORG. TENANT_SCOPE_UNSPECIFIED and TENANT_SCOPE_SANDBOX_NETWORK
            are invalid. Omit tenant when selecting another destination.
          type: string
          format: enum
          enum:
          - TENANT_SCOPE_UNSPECIFIED
          - TENANT_SCOPE_SAME_USER
          - TENANT_SCOPE_SAME_ORG
          - TENANT_SCOPE_SANDBOX_NETWORK
        any:
          description: "All destinations reachable from the sandbox's network, excluding\n platform-internal\
            \ ranges (cluster-internal, link-local, and\n cloud-metadata addresses are always carved out).\
            \ Use tenant or\n selector rules to reach other sandboxes or in-cluster workloads."
          type: boolean
        selector:
          description: "Cluster workloads selected by label. Entitlement is EXPLICIT-ONLY: a\n policy\
            \ `any` entitlement covers address-shaped destinations but never\n selectors — when the policy\
            \ constrains egress (non-empty\n allowed_egress), declaring a selector requires a selector\
            \ entitlement\n there, so an open-egress policy does not silently grant label-based\n selection\
            \ of co-located workloads. A policy with EMPTY allowed_egress\n constrains nothing and admits\
            \ selector declarations like every other\n type."
          allOf:
          - $ref: '#/components/schemas/coreweave.sandbox.v1.SelectorBlock'
        ports:
          description: Ports the destination may be reached on. Empty = all ports.
          type: array
          items:
            $ref: '#/components/schemas/coreweave.sandbox.v1.PortRange'
        httpsHostnameExcept:
          description: "Hostnames excluded from this rule's HTTPS grant. Valid only with\n https_hostname\
            \ on Policy.allowed_egress. An except narrows only THIS rule;\n another allowed_egress rule\
            \ may still entitle the hostname. Grammar matches\n https_hostname except \"*\". Each except\
            \ must be covered by this rule's\n hostname pattern (\"*\" may except any name; \"*.example.com\"\
            \ may except\n \"foo.example.com\"). \"evil.com\"\n does not except \"www.evil.com\"; add\
            \ \"*.evil.com\" to cover one label\n under that apex. Extra labels (a.b.evil.com) remain\
            \ entitled under\n those excepts. A declared name or wildcard whose match set covers an\n\
            \ except is not entitled by this rule."
          type: array
          items:
            type: string
    coreweave.sandbox.v1.EndpointSpec:
      description: EndpointSpec is the create-time opt-in for a product endpoint on a Service.
      type: object
      properties:
        kind:
          description: Required when endpoint is set. UNSPECIFIED is rejected when wired.
          type: string
          format: enum
          enum:
          - ENDPOINT_KIND_UNSPECIFIED
          - ENDPOINT_KIND_HTTPS
          - ENDPOINT_KIND_TLS_PASSTHROUGH
        auth:
          description: Required when kind = HTTPS. UNSPECIFIED is rejected when wired. For TLS passthrough,
            leave authentication unset; ENDPOINT_AUTH_UNSPECIFIED is required and does not mean ENDPOINT_AUTH_OPEN.
          type: string
          format: enum
          enum:
          - ENDPOINT_AUTH_UNSPECIFIED
          - ENDPOINT_AUTH_OPEN
          - ENDPOINT_AUTH_SHARE_TOKEN
        requestTimeoutSeconds:
          description: "Seconds before the platform closes an in-flight HTTPS request while the\n sandbox\
            \ remains alive. Unset or 0 selects the platform default of 15 seconds.\n An explicit value\
            \ must be between 15 and 900 inclusive. Rejected when kind\n is not HTTPS. Sandbox lifetime,\
            \ deletion, or failure may end the request\n first, possibly as a transport error rather than\
            \ HTTP 504."
          type: integer
          format: int32
      required:
      - kind
    coreweave.sandbox.v1.EndpointStatus:
      type: object
      properties:
        kind:
          description: Accepted endpoint kind. ENDPOINT_KIND_UNSPECIFIED is invalid when requesting an
            endpoint. When no endpoint was requested, the endpoint status is absent.
          type: string
          format: enum
          enum:
          - ENDPOINT_KIND_UNSPECIFIED
          - ENDPOINT_KIND_HTTPS
          - ENDPOINT_KIND_TLS_PASSTHROUGH
          readOnly: true
        auth:
          description: Accepted endpoint authentication setting. HTTPS requires ENDPOINT_AUTH_OPEN or
            ENDPOINT_AUTH_SHARE_TOKEN. TLS passthrough requires authentication to be unset and reports
            ENDPOINT_AUTH_UNSPECIFIED; this does not mean ENDPOINT_AUTH_OPEN.
          type: string
          format: enum
          enum:
          - ENDPOINT_AUTH_UNSPECIFIED
          - ENDPOINT_AUTH_OPEN
          - ENDPOINT_AUTH_SHARE_TOKEN
          readOnly: true
        url:
          description: "Assigned product HTTPS URL for this endpoint. When present, the same\n absolute\
            \ https:// URL is durable across live Create, GetSandbox,\n ListSandboxes, and idempotent\
            \ Create replay while the sandbox is CREATING\n or RUNNING. Empty until assignment completes,\
            \ when no product HTTPS\n endpoints were requested, or when the sandbox is TERMINATING/terminal\n\
            \ (any stored assignment is retained but suppressed). A non-empty URL means\n the address\
            \ was assigned, not that the application or edge is ready to serve.\n TLS passthrough endpoints\
            \ leave this empty."
          type: string
          readOnly: true
        requestTimeoutSeconds:
          description: "Effective configured HTTPS request timeout in seconds while the sandbox\n remains\
            \ alive. Unset or 0 on create is echoed as the platform default.\n Unset when kind is not\
            \ HTTPS. This is the accepted create value, not a\n live observation of the serving path.\
            \ Sandbox lifetime, deletion, or\n failure may end the request first, possibly as a transport\
            \ error rather\n than HTTP 504."
          type: integer
          format: int32
          readOnly: true
        address:
          description: "Assigned product TLS passthrough target as host:port. Clients must use\n the host\
            \ as TLS SNI. When present, the same host:port is durable across\n live Create, GetSandbox,\
            \ ListSandboxes, and idempotent Create replay\n while the sandbox is CREATING or RUNNING.\
            \ Empty until assignment\n completes, when no product TLS passthrough endpoints were requested,\
            \ or\n when the sandbox is TERMINATING/terminal (any stored assignment is\n retained but suppressed).\
            \ A non-empty address means the target was\n assigned, not that the application or edge is\
            \ ready to serve. HTTPS\n endpoints leave this empty; TLS passthrough endpoints leave url\
            \ empty."
          type: string
          readOnly: true
    coreweave.sandbox.v1.ExecRequest:
      type: object
      properties:
        sandboxId:
          type: string
        command:
          type: array
          items:
            type: string
        env:
          type: object
          additionalProperties:
            type: string
        maxOutputBytes:
          description: "Cap on buffered output per stream; output beyond this is truncated (see\n ExecResponse.*_truncated).\
            \ 0 = platform default."
          type: integer
          format: int32
        container:
          description: "Target container name. Empty = the primary. Unknown names and\n platform sidecar\
            \ names are INVALID_ARGUMENT (CWSANDBOX_INVALID_REQUEST).\n In a CONTROL_CONTAINER_ENGINE\
            \ sandbox, cws-engine is the only container\n and the primary."
          type: string
      required:
      - sandboxId
      - command
    coreweave.sandbox.v1.ExecResponse:
      type: object
      properties:
        stdout:
          type: string
          format: bytes
        stderr:
          type: string
          format: bytes
        exitCode:
          type: integer
          format: int32
        stdoutTruncated:
          type: boolean
        stderrTruncated:
          type: boolean
        stdoutBytesProduced:
          description: Total bytes the process wrote to stdout, even when stdout was truncated.
          type: string
        stderrBytesProduced:
          description: Total bytes the process wrote to stderr, even when stderr was truncated.
          type: string
    coreweave.sandbox.v1.FileMount:
      description: FileMount is a file written into a container at startup.
      type: object
      properties:
        path:
          type: string
        content:
          format: bytes
          type: string
      required:
      - path
      - content
    coreweave.sandbox.v1.FileSystemSnapshot:
      type: object
      properties:
        fileSystemSnapshotId:
          type: string
          readOnly: true
        state:
          description: Reported snapshot state. SNAPSHOT_STATE_UNSPECIFIED means no recognized public
            state is available for the stored state.
          type: string
          format: enum
          enum:
          - SNAPSHOT_STATE_UNSPECIFIED
          - SNAPSHOT_STATE_CREATING
          - SNAPSHOT_STATE_READY
          - SNAPSHOT_STATE_FAILED
          - SNAPSHOT_STATE_DELETING
          readOnly: true
        stateReason:
          type: string
          readOnly: true
        sizeBytes:
          type: string
          readOnly: true
        sourceSandboxId:
          type: string
          readOnly: true
        trigger:
          description: Reported creation trigger. SNAPSHOT_TRIGGER_UNSPECIFIED means no recognized public
            trigger is available for the stored trigger; it does not imply manual creation.
          type: string
          format: enum
          enum:
          - SNAPSHOT_TRIGGER_UNSPECIFIED
          - SNAPSHOT_TRIGGER_MANUAL
          - SNAPSHOT_TRIGGER_ON_DELETE
          readOnly: true
        createTime:
          type: string
          format: date-time
          readOnly: true
        completeTime:
          type: string
          format: date-time
          readOnly: true
        sourceVolumeName:
          description: Name of the source volume this snapshot was taken from.
          type: string
          readOnly: true
        objectBucket:
          description: Object-storage bucket the snapshot archive landed in.
          type: string
          readOnly: true
        updatedAt:
          description: When the snapshot record was last updated.
          type: string
          format: date-time
          readOnly: true
        requestId:
          description: Echoes the request_id supplied to CreateFileSystemSnapshot, if any.
          type: string
          readOnly: true
    coreweave.sandbox.v1.FileSystemSnapshotBucketConfig:
      description: FileSystemSnapshotBucketConfig is the organization's FSS bucket configuration.
      type: object
      properties:
        bucketName:
          description: Bring-your-own bucket name. Empty means CoreWeave manages the bucket.
          type: string
        region:
          description: "Object-store region for the bring-your-own bucket. Required iff bucket_name\n\
            \ is set."
          type: string
        mode:
          description: Output-only ownership mode, derived by the server. An empty bucketName uses FILE_SYSTEM_SNAPSHOT_BUCKET_MODE_CW_MANAGED;
            a configured bucket uses FILE_SYSTEM_SNAPSHOT_BUCKET_MODE_BRING_YOUR_OWN. FILE_SYSTEM_SNAPSHOT_BUCKET_MODE_UNSPECIFIED
            means the output mode is unset or unrecognized, not a default ownership mode. Do not use this
            field to select a mode in requests.
          type: string
          format: enum
          enum:
          - FILE_SYSTEM_SNAPSHOT_BUCKET_MODE_UNSPECIFIED
          - FILE_SYSTEM_SNAPSHOT_BUCKET_MODE_CW_MANAGED
          - FILE_SYSTEM_SNAPSHOT_BUCKET_MODE_BRING_YOUR_OWN
          readOnly: true
        effectiveBucketName:
          description: "The bucket actually in effect: the customer bucket, or the CoreWeave-managed\n\
            \ derived name."
          type: string
          readOnly: true
    coreweave.sandbox.v1.GetSandboxBuildLogsResponse:
      type: object
      properties:
        url:
          description: "Presigned HTTPS GET URL for the plain-text build log. It is a bearer\n credential:\
            \ anyone holding it can read the log until expire_time, so do\n not log or share it."
          type: string
        expireTime:
          description: When url stops working.
          type: string
          format: date-time
    coreweave.sandbox.v1.Gpu:
      description: Gpu specifies GPU allocation by type or by VRAM.
      type: object
      properties:
        count:
          type: string
        type:
          type: string
        memoryGb:
          type: string
    coreweave.sandbox.v1.ImageConstraints:
      description: ImageConstraints restricts which images may run.
      type: object
      properties:
        allowedRegistries:
          description: Allowed registry prefixes (empty = any).
          type: array
          items:
            type: string
        allowedImages:
          description: Allowed image references (empty = any within allowed_registries).
          type: array
          items:
            type: string
    coreweave.sandbox.v1.ImagePullCredentials:
      description: "ImagePullCredentials identifies the registry authority and provider secret\n source\
        \ used to synthesize Docker config JSON for a private image pull."
      type: object
      properties:
        registry:
          description: Registry authority for the credential and generated Docker config auth key.
          type: string
        credentials:
          description: "Provider secret source that resolves to a structured object containing\n non-empty\
            \ string fields named \"username\" and \"password\"."
          allOf:
          - $ref: '#/components/schemas/coreweave.sandbox.v1.SecretSource'
      required:
      - registry
      - credentials
    coreweave.sandbox.v1.IngressRule:
      description: "IngressRule allows inbound traffic from one source class to the sandbox's\n CUSTOM-visibility\
        \ ports, optionally narrowed to specific ports (source AND\n ports; empty ports = all CUSTOM-visibility\
        \ ports). Sources are\n address-shaped or relational; inbound packets carry no names, so there\
        \ are\n no name-based sources. SANDBOX_NETWORK tenant scope is rejected until\n network_ids has\
        \ an enforcement backend."
      type: object
      properties:
        cidr:
          description: Source addresses, with optional carve-outs.
          allOf:
          - $ref: '#/components/schemas/coreweave.sandbox.v1.CidrBlock'
        tenant:
          description: Other sandboxes, selected by tenant relationship. When selecting this source, use
            TENANT_SCOPE_SAME_USER or TENANT_SCOPE_SAME_ORG. TENANT_SCOPE_UNSPECIFIED and TENANT_SCOPE_SANDBOX_NETWORK
            are invalid. Omit tenant when selecting another source.
          type: string
          format: enum
          enum:
          - TENANT_SCOPE_UNSPECIFIED
          - TENANT_SCOPE_SAME_USER
          - TENANT_SCOPE_SAME_ORG
          - TENANT_SCOPE_SANDBOX_NETWORK
        any:
          description: "Any source, including the public internet. Authorizes packets that\n arrive on\
            \ CUSTOM ports without peer restriction; reachability /\n front-door exposure is out of scope\
            \ for this rule."
          type: boolean
        ports:
          description: Declared ports this rule applies to. Empty = all CUSTOM-visibility ports.
          type: array
          items:
            $ref: '#/components/schemas/coreweave.sandbox.v1.PortRange'
    coreweave.sandbox.v1.InstanceConstraints:
      description: InstanceConstraints restricts node instance-type selection.
      type: object
      properties:
        allowedInstanceTypes:
          description: Allowed SandboxSpec.instance_type values (empty = any the runner offers).
          type: array
          items:
            type: string
    coreweave.sandbox.v1.LifecycleConstraints:
      description: "LifecycleConstraints supplies sandbox lifetime defaults. Values above the\n platform\
        \ maximum (currently 30 days) are rejected at create time; Policy\n only supplies a default when\
        \ the create omits lifetime."
      type: object
      properties:
        defaultLifetimeSeconds:
          description: Default applied when SandboxSpec.max_lifetime_seconds is 0.
          type: integer
          format: int32
    coreweave.sandbox.v1.ListAvailableRunnersResponse:
      type: object
      properties:
        runners:
          type: array
          items:
            $ref: '#/components/schemas/coreweave.sandbox.v1.AvailableRunner'
        nextPageToken:
          type: string
    coreweave.sandbox.v1.ListFileSystemSnapshotsResponse:
      type: object
      properties:
        fileSystemSnapshots:
          type: array
          items:
            $ref: '#/components/schemas/coreweave.sandbox.v1.FileSystemSnapshot'
        nextPageToken:
          type: string
    coreweave.sandbox.v1.ListManagedRunnersResponse:
      type: object
      properties:
        managedRunners:
          type: array
          items:
            $ref: '#/components/schemas/coreweave.sandbox.v1.ManagedRunner'
        nextPageToken:
          type: string
    coreweave.sandbox.v1.ListNetworkConfigsResponse:
      type: object
      properties:
        networkConfigs:
          type: array
          items:
            $ref: '#/components/schemas/coreweave.sandbox.v1.NetworkConfig'
        nextPageToken:
          type: string
    coreweave.sandbox.v1.ListNetworksResponse:
      type: object
      properties:
        networks:
          type: array
          items:
            $ref: '#/components/schemas/coreweave.sandbox.v1.Network'
        nextPageToken:
          type: string
    coreweave.sandbox.v1.ListProfileTemplatesResponse:
      type: object
      properties:
        profileTemplates:
          type: array
          items:
            $ref: '#/components/schemas/coreweave.sandbox.v1.ProfileTemplate'
        nextPageToken:
          type: string
    coreweave.sandbox.v1.ListSandboxLogsResponse:
      type: object
      properties:
        entries:
          type: array
          items:
            $ref: '#/components/schemas/coreweave.sandbox.v1.StoredSandboxLogEntry'
          readOnly: true
        nextPageToken:
          description: Token for the next page; empty on the last page.
          type: string
          readOnly: true
        retentionExpiresAt:
          description: "When the stored logs stop being readable. Absent while the sandbox has\n not ended."
          type: string
          format: date-time
          readOnly: true
    coreweave.sandbox.v1.ListSandboxTemplatesResponse:
      type: object
      properties:
        sandboxTemplates:
          type: array
          items:
            $ref: '#/components/schemas/coreweave.sandbox.v1.SandboxTemplate'
        nextPageToken:
          type: string
    coreweave.sandbox.v1.ListSandboxesResponse:
      type: object
      properties:
        sandboxes:
          type: array
          items:
            $ref: '#/components/schemas/coreweave.sandbox.v1.Sandbox'
        nextPageToken:
          type: string
    coreweave.sandbox.v1.ListSecretStoresResponse:
      type: object
      properties:
        secretStores:
          type: array
          items:
            $ref: '#/components/schemas/coreweave.sandbox.v1.SecretStore'
        nextPageToken:
          type: string
    coreweave.sandbox.v1.ListVolumesResponse:
      type: object
      properties:
        volumes:
          type: array
          items:
            $ref: '#/components/schemas/coreweave.sandbox.v1.Volume'
        nextPageToken:
          type: string
    coreweave.sandbox.v1.LogEntry:
      type: object
      properties:
        data:
          type: string
          format: bytes
        timestamp:
          type: string
          format: date-time
        logSessionId:
          description: Stream session id; pass to StreamLogsRequest.resume_log_session_id to resume.
          type: string
          readOnly: true
        nextLogOffset:
          description: Byte offset of the next unread byte; pass to resume_log_offset to resume.
          type: string
          readOnly: true
        error:
          description: Terminal stream error. When set, this is the final item on the stream.
          allOf:
          - $ref: '#/components/schemas/coreweave.sandbox.v1.LogStreamError'
          readOnly: true
    coreweave.sandbox.v1.LogStreamError:
      description: "LogStreamError is a terminal error on the log stream (the final message).\n code is\
        \ a machine-readable streaming-channel code (e.g. SESSION_NOT_FOUND,\n REPLAY_GAP, INVALID_RESUME_OFFSET);\
        \ message is a human-readable description."
      type: object
      properties:
        message:
          type: string
        code:
          type: string
    coreweave.sandbox.v1.MaintenanceExclusion:
      description: "MaintenanceExclusion defines a one-time period during which no updates\n start, overriding\
        \ any open maintenance window."
      type: object
      properties:
        startTime:
          description: Start of the exclusion period (inclusive).
          type: string
          format: date-time
        endTime:
          description: End of the exclusion period (exclusive). Must be after start_time.
          type: string
          format: date-time
        reason:
          type: string
      required:
      - startTime
      - endTime
    coreweave.sandbox.v1.MaintenancePolicy:
      description: MaintenancePolicy controls when updates can be applied to managed runners.
      type: object
      properties:
        windows:
          type: array
          items:
            $ref: '#/components/schemas/coreweave.sandbox.v1.MaintenanceWindow'
        exclusions:
          type: array
          items:
            $ref: '#/components/schemas/coreweave.sandbox.v1.MaintenanceExclusion'
    coreweave.sandbox.v1.MaintenanceWindow:
      description: "MaintenanceWindow defines a recurring window during which updates may\n start. If\
        \ any windows are configured, updates start only while one is\n open; exclusions override windows."
      type: object
      properties:
        cron:
          description: "Standard 5-field cron expression for the window start (e.g.,\n \"0 2 * * SAT\"\
            \ for Saturdays at 02:00), evaluated in UTC. Descriptor\n forms such as \"@daily\" or \"@every\
            \ 1h\" are rejected, as are expressions\n that never fire."
          type: string
        durationSeconds:
          description: "Duration of the window in seconds. Must be between 60 (1 minute) and\n 604800\
            \ (7 days)."
          type: integer
          format: int32
      required:
      - cron
      - durationSeconds
    coreweave.sandbox.v1.ManagedRunner:
      description: ManagedRunner is an admin-owned runner deployment.
      type: object
      properties:
        identity:
          description: "Core runner identity. Required on create; immutable identity fields cannot\n be\
            \ changed afterward."
          allOf:
          - $ref: '#/components/schemas/coreweave.sandbox.v1.RunnerIdentity'
        displayName:
          description: Human-readable name for the runner, at most 256 characters.
          type: string
        spec:
          description: Desired managed-runner configuration.
          allOf:
          - $ref: '#/components/schemas/coreweave.sandbox.v1.ManagedRunnerSpec'
        installStatus:
          description: Current installation status. RUNNER_INSTALL_STATUS_UNSPECIFIED means no installation
            status is specified.
          type: string
          format: enum
          enum:
          - RUNNER_INSTALL_STATUS_UNSPECIFIED
          - RUNNER_INSTALL_STATUS_PENDING
          - RUNNER_INSTALL_STATUS_PROVISIONING
          - RUNNER_INSTALL_STATUS_READY
          - RUNNER_INSTALL_STATUS_FAILED
          - RUNNER_INSTALL_STATUS_DELETING
          readOnly: true
        connectionStatus:
          description: Live connection status. RUNNER_CONNECTION_STATUS_UNSPECIFIED means no connection
            status is specified.
          type: string
          format: enum
          enum:
          - RUNNER_CONNECTION_STATUS_UNSPECIFIED
          - RUNNER_CONNECTION_STATUS_CONNECTED
          - RUNNER_CONNECTION_STATUS_DISCONNECTED
          readOnly: true
        activeConfigVersion:
          description: Active configuration version running on the runner.
          type: string
          readOnly: true
        activeProfileSpecVersion:
          description: Active profile spec version running on the runner.
          type: string
          readOnly: true
        activeRevision:
          description: Active revision number currently running on the runner.
          type: integer
          format: int32
          readOnly: true
        targetRevision:
          description: Target revision number that should be rolled out.
          type: integer
          format: int32
          readOnly: true
        deploymentSpec:
          description: Resolved deployment spec for the runner.
          allOf:
          - $ref: '#/components/schemas/coreweave.sandbox.v1.RunnerDeploymentSpec'
          readOnly: true
        updateAvailable:
          description: Whether an update is available on this runner's release channel.
          type: boolean
          readOnly: true
        createTime:
          type: string
          format: date-time
          readOnly: true
        updateTime:
          type: string
          format: date-time
          readOnly: true
        lastHeartbeatTime:
          type: string
          format: date-time
          readOnly: true
        profileBindings:
          description: "Legacy profile bindings. Not accepted by v1 managed-runner writes;\n configure\
            \ policy instead."
          type: array
          items:
            $ref: '#/components/schemas/coreweave.sandbox.v1.RunnerProfileBinding'
        installError:
          description: Populated when install_status == FAILED.
          allOf:
          - $ref: '#/components/schemas/coreweave.sandbox.v1.RunnerInstallError'
          readOnly: true
        rolloutInProgress:
          description: True when target_revision is newer than active_revision.
          type: boolean
          readOnly: true
        policy:
          description: The policy governing sandboxes on this runner. v1 managed-runner creation requires
            an explicit policy. An empty policy supplies no base defaults or explicit constraints. Platform
            safety gates still apply, and an absent runtime-class allowlist permits no concrete runtimeClass
            pin.
          allOf:
          - $ref: '#/components/schemas/coreweave.sandbox.v1.Policy'
        etag:
          description: "Opaque revision token for policy updates. Clients must send the value\n returned\
            \ by GetManagedRunner when updating policy. A stale value causes\n FAILED_PRECONDITION and\
            \ no mutation is applied."
          type: string
        dataPlaneStatus:
          description: Observed direct data-plane endpoint state.
          allOf:
          - $ref: '#/components/schemas/coreweave.sandbox.v1.RunnerDataPlaneStatus'
          readOnly: true
      required:
      - identity
      - policy
    coreweave.sandbox.v1.ManagedRunnerSpec:
      description: ManagedRunnerSpec contains configuration specific to platform-managed runners.
      type: object
      properties:
        releaseChannel:
          description: Release channel for automatic updates. Omit this field to use RELEASE_CHANNEL_STABLE
            on create or whole-spec replacement. RELEASE_CHANNEL_UNSPECIFIED also defaults to RELEASE_CHANNEL_STABLE
            in those cases. An update that selects only spec.releaseChannel requires a concrete channel.
          type: string
          format: enum
          enum:
          - RELEASE_CHANNEL_UNSPECIFIED
          - RELEASE_CHANNEL_STABLE
          - RELEASE_CHANNEL_RAPID
        maintenancePolicy:
          description: Maintenance policy for update scheduling.
          allOf:
          - $ref: '#/components/schemas/coreweave.sandbox.v1.MaintenancePolicy'
        overrides:
          description: Customer-settable deployment overrides.
          allOf:
          - $ref: '#/components/schemas/coreweave.sandbox.v1.RunnerDeploymentOverrides'
        allowPrivilegedProfileAnnotations:
          description: Legacy profile setting. Not accepted by v1 managed-runner writes.
          type: boolean
        enforceResourceLimits:
          description: "Requires sandboxes and bound profile templates to declare both memory and\n CPU\
            \ limits."
          type: boolean
        volumes:
          description: "Registered-Volume (PVC) support for this runner. When present, this\n typed toggle\
            \ is authoritative over any ENABLE_VOLUMES /\n VOLUME_DRIVER_ALLOWLIST entries in deployment\
            \ env."
          allOf:
          - $ref: '#/components/schemas/coreweave.sandbox.v1.RunnerVolumesConfig'
        tenantMetrics:
          description: "Tenant-metrics collector for this runner's cluster. When present,\n authoritative\
            \ over the equivalent deployment-env entries; when absent,\n env passthrough applies."
          allOf:
          - $ref: '#/components/schemas/coreweave.sandbox.v1.RunnerTenantMetricsConfig'
        dataPlane:
          description: "Direct sandbox data-plane endpoint configuration. Unset uses the platform\n default;\
            \ the disabled exposure keeps all data operations on the Gateway."
          allOf:
          - $ref: '#/components/schemas/coreweave.sandbox.v1.RunnerDataPlaneConfig'
        imagePull:
          description: "Image pull behavior for sandbox workload containers on this runner. When\n present,\
            \ this typed setting is authoritative over any equivalent\n deployment env entry; when absent,\
            \ the platform default applies."
          allOf:
          - $ref: '#/components/schemas/coreweave.sandbox.v1.RunnerImagePullConfig'
    coreweave.sandbox.v1.MetadataConstraints:
      description: MetadataConstraints clamps sandbox annotations.
      type: object
      properties:
        deniedAnnotationPrefixes:
          description: Annotation key prefixes that are rejected.
          type: array
          items:
            type: string
        maxAnnotationCount:
          description: Maximum number of annotations (0 = no limit).
          type: integer
          format: int32
    coreweave.sandbox.v1.Network:
      description: "Network is a private network. Sandboxes that join it (via\n SandboxSpec.network_ids)\
        \ can reach each other."
      type: object
      properties:
        networkId:
          type: string
          readOnly: true
        displayName:
          type: string
        createTime:
          type: string
          format: date-time
          readOnly: true
    coreweave.sandbox.v1.NetworkConfig:
      description: NetworkConfig is the desired network document a sandbox binds 1:1.
      type: object
      properties:
        networkConfigId:
          description: Immutable, organization-unique ID matching ^[a-z][a-z0-9-]{2,62}$. Choose the ID
            on CreateNetworkConfig, without the reserved nc- prefix. The platform assigns an nc- ID when
            it creates a configuration automatically for a sandbox.
          type: string
        spec:
          $ref: '#/components/schemas/coreweave.sandbox.v1.NetworkOptions'
        status:
          allOf:
          - $ref: '#/components/schemas/coreweave.sandbox.v1.NetworkConfigStatus'
          readOnly: true
        etag:
          description: Optional concurrency token. Send the last returned value in the NetworkConfig update
            body to protect a desired-state write. A mismatch on that write returns ABORTED with CWSANDBOX_ETAG_MISMATCH.
            A bound update whose resulting spec already matches stored desired state reapplies enforcement
            without checking the token. Omitting the token permits the last persisted desired-state write
            to win. The token does not make enforcement atomic.
          type: string
      required:
      - spec
    coreweave.sandbox.v1.NetworkConfigStatus:
      type: object
      properties:
        sandboxId:
          description: Last bound sandbox. This field can briefly name a terminal sandbox until cleanup
            completes. A configuration is considered in use only while its bound sandbox exists and is
            non-terminal.
          type: string
          readOnly: true
        platformManaged:
          description: True when the platform created the configuration for a sandbox. Platform-managed
            configurations are deleted after that sandbox terminates. Caller-created configurations remain
            available for reuse.
          type: boolean
          readOnly: true
        createTime:
          type: string
          format: date-time
          readOnly: true
        updateTime:
          type: string
          format: date-time
          readOnly: true
    coreweave.sandbox.v1.NetworkConstraints:
      description: "NetworkConstraints clamps the sandbox's declared network intent\n (SandboxSpec.network,\
        \ using the EgressRule/IngressRule types from\n sandbox.proto) and bounds port visibility."
      type: object
      properties:
        allowedEgress:
          description: "Allowed egress envelope, validated at create time. When non-empty, every\n declared\
            \ egress rule must fit inside the union of these rules; a rule\n outside it is rejected, never\
            \ silently narrowed. Carve-outs are expressed\n with CidrBlock.except (e.g. \"everything but\
            \ an internal range\" is\n {cidr: 0.0.0.0/0, except: [10.8.0.0/16]}) and with https_hostname:\
            \ \"*\" plus\n https_hostname_except. Excluding \"evil.com\" and \"*.evil.com\" removes the\n\
            \ apex and one label under it, but leaves a.b.evil.com entitled.\n Containment is type-wise:\
            \ a declared CIDR must fit the allowed CIDR space;\n an HTTPS hostname must match an allowed\
            \ hostname pattern, minus that\n rule's https_hostname_except, or an `any` entitlement; a\
            \ declared tenant\n scope must appear as an allowed scope; and declaring `any` requires an\n\
            \ `any` entitlement. An `any` entitlement admits CIDR, tenant, HTTPS\n hostnames, and `any`\
            \ — but never selectors: label-based\n selection of cluster workloads requires its own selector\
            \ entitlement\n (see EgressRule.selector). Empty = any egress is declarable, selectors\n included."
          type: array
          items:
            $ref: '#/components/schemas/coreweave.sandbox.v1.EgressRule'
        defaultEgress:
          description: "Egress applied when the spec declares none; entirely displaced by a spec\n that\
            \ declares its own rules. Must fit the allowed envelope (validated when\n the policy is written).\
            \ Must not carry https_hostname — a curated site set\n belongs on a SandboxTemplate, not the\
            \ policy default."
          type: array
          items:
            $ref: '#/components/schemas/coreweave.sandbox.v1.EgressRule'
        denyHttpsHostnameRules:
          description: "When true, rejects https_hostname rules in allowed_egress and\n SandboxSpec.network.egress.\
            \ False permits those rules subject to\n allowed_egress. This controls permission to declare\
            \ hostname-based HTTPS\n access; it does not block DNS queries or HTTPS allowed by CIDR rules.\
            \ Use\n dns_egress to control outbound DNS traffic on UDP/TCP port 53."
          type: boolean
        allowedIngress:
          description: "Allowed ingress envelope for CUSTOM-visibility ports, validated at create\n time\
            \ with the same type-wise containment as allowed_egress. Empty = any\n ingress is declarable."
          type: array
          items:
            $ref: '#/components/schemas/coreweave.sandbox.v1.IngressRule'
        defaultIngress:
          description: "Ingress applied when a CUSTOM-visibility port is declared and the spec\n declares\
            \ no ingress rules; entirely displaced by a spec that declares its\n own. Must fit the allowed\
            \ envelope (validated when the policy is written)."
          type: array
          items:
            $ref: '#/components/schemas/coreweave.sandbox.v1.IngressRule'
        dnsEgress:
          description: "Outbound DNS traffic ceiling, inherited by SandboxSpec.network.dns_egress.\n UNSPECIFIED\
            \ defaults to ALLOW. ALLOW permits platform resolver access;\n a sandbox may choose DENY.\
            \ DENY requires every sandbox to block outbound\n UDP/TCP destination port 53; an explicit\
            \ sandbox ALLOW is rejected.\n This does not restrict which https_hostname rules may be declared;\n\
            \ allowed_egress and deny_https_hostname_rules govern those rules."
          type: string
          format: enum
          enum:
          - DNS_EGRESS_MODE_UNSPECIFIED
          - DNS_EGRESS_MODE_ALLOW
          - DNS_EGRESS_MODE_DENY
    coreweave.sandbox.v1.NetworkOptions:
      description: NetworkOptions declares the sandbox's network intent beyond port exposure.
      type: object
      properties:
        ingress:
          description: "Inbound sources for ports with visibility = CUSTOM: an allow-only rule set\n over\
            \ a default-deny base. A CUSTOM port not matched by any rule is\n unreachable. A rule outside\
            \ the runner policy's allowed ingress envelope\n is rejected at create, never silently narrowed.\
            \ Empty = the policy's\n default ingress. The rules in effect are echoed in\n SandboxStatus.effective_ingress."
          type: array
          items:
            $ref: '#/components/schemas/coreweave.sandbox.v1.IngressRule'
        egress:
          description: "Egress destinations the sandbox needs. These grants are additive: traffic\n matching\
            \ any rule is allowed, subject to dns_egress. A rule outside the\n runner policy's allowed\
            \ envelope is rejected at create, never silently\n narrowed. Empty = the policy's default\
            \ egress. Platform DNS and storage\n access are granted separately; dns_egress=DENY blocks\
            \ UDP/TCP port 53\n across all grants. Resolved destination rules are echoed in\n SandboxStatus.effective_egress."
          type: array
          items:
            $ref: '#/components/schemas/coreweave.sandbox.v1.EgressRule'
        denyEgress:
          description: "When true, applies no declared or default egress rules. Mutually exclusive\n with\
            \ egress rules and always admitted as a narrowing of allowed_egress.\n Platform DNS and storage\
            \ access remain separate. Set dns_egress=DENY to\n also block outbound UDP/TCP port 53. An\
            \ empty egress list with this flag\n unset instead inherits the policy's default_egress."
          type: boolean
        denyIngress:
          description: When true, deny declared and policy-default ingress to CUSTOM services. NetworkConfig
            create and update requests reject a non-empty ingress list when denyIngress is true. To deny
            ingress in an update, clear the list and set this flag in the same request. PUBLIC and PRIVATE
            service visibility is unchanged.
          type: boolean
        dnsEgress:
          description: "Outbound DNS traffic mode on UDP/TCP destination port 53. UNSPECIFIED\n inherits\
            \ Policy.constraints.network.dns_egress. DENY overrides port-53\n access in all egress grants;\
            \ ALLOW is rejected when the policy requires\n DENY. This is independent of https_hostname\
            \ destination rules and does\n not provide a DNS query-name allowlist. See DNSEgressMode for\
            \ scope."
          type: string
          format: enum
          enum:
          - DNS_EGRESS_MODE_UNSPECIFIED
          - DNS_EGRESS_MODE_ALLOW
          - DNS_EGRESS_MODE_DENY
    coreweave.sandbox.v1.ObjectStorageAccess:
      description: "ObjectStorageAccess grants the sandbox temporary access to object-storage\n buckets.\
        \ The minted credential is injected into every user container."
      type: object
      properties:
        buckets:
          type: array
          items:
            type: string
        permission:
          description: Requested object-storage permission. Specify OBJECT_STORAGE_PERMISSION_READ or
            OBJECT_STORAGE_PERMISSION_READ_WRITE. Omitted or OBJECT_STORAGE_PERMISSION_UNSPECIFIED is
            invalid; it does not default to read access.
          type: string
          format: enum
          enum:
          - OBJECT_STORAGE_PERMISSION_UNSPECIFIED
          - OBJECT_STORAGE_PERMISSION_READ
          - OBJECT_STORAGE_PERMISSION_READ_WRITE
        objectPrefix:
          description: "Optional object-prefix that scopes the minted credential to a sub-path\n within\
            \ the granted buckets. Stamped verbatim into the CAIOS bucket policy;\n see v1beta2 ObjectStorageAccess.object_prefix\
            \ for the validation contract."
          type: string
    coreweave.sandbox.v1.ObjectStorageWifConfig:
      description: "ObjectStorageWifConfig is the organization's object-storage workload-identity\n federation\
        \ config and the policy ceiling for per-sandbox object_storage_access."
      type: object
      properties:
        wifConfigId:
          description: "The WIF config id from the CoreWeave Cloud Console (a Workload Federation\n configuration).\
            \ Required on create / full-replace."
          type: string
        enabled:
          description: Whether object-storage access is enabled for the organization.
          type: boolean
        allowedBuckets:
          description: Buckets the org may access; empty means all buckets.
          type: array
          items:
            type: string
        maxPermission:
          description: Maximum permission a sandbox may be granted. Specify OBJECT_STORAGE_PERMISSION_READ
            or OBJECT_STORAGE_PERMISSION_READ_WRITE on create, full replacement, or an update that selects
            maxPermission. OBJECT_STORAGE_PERMISSION_UNSPECIFIED is invalid in these writes. A partial
            update that excludes this field preserves its current value.
          type: string
          format: enum
          enum:
          - OBJECT_STORAGE_PERMISSION_UNSPECIFIED
          - OBJECT_STORAGE_PERMISSION_READ
          - OBJECT_STORAGE_PERMISSION_READ_WRITE
        createTime:
          type: string
          format: date-time
          readOnly: true
        updateTime:
          type: string
          format: date-time
          readOnly: true
    coreweave.sandbox.v1.PartialContainer:
      description: 'Container fields for a partial stored template or a create-time container override.
        A stored template may omit image if create-time overrides supply a complete, valid containers
        list. A containers override replaces the entire list: entries are not merged with template containers
        and cannot inherit an omitted image or other container fields. Each replacement container must
        be complete and valid.'
      type: object
      properties:
        name:
          type: string
        image:
          description: "OCI image. Optional on templates and overlays; required on the sandbox\n after\
            \ CreateSandboxFromTemplate merge completes."
          type: string
        command:
          type: string
        args:
          type: array
          items:
            type: string
        environmentVariables:
          type: object
          additionalProperties:
            type: string
        resources:
          $ref: '#/components/schemas/coreweave.sandbox.v1.Resources'
        files:
          type: array
          items:
            $ref: '#/components/schemas/coreweave.sandbox.v1.FileMount'
        volumeMounts:
          type: array
          items:
            $ref: '#/components/schemas/coreweave.sandbox.v1.VolumeMount'
        secretStores:
          description: "Same meaning as Container.secret_stores: resolved values inject into\n this container\
            \ only."
          type: array
          items:
            $ref: '#/components/schemas/coreweave.sandbox.v1.SecretStoreReference'
        workingDir:
          type: string
        resourceRequirements:
          $ref: '#/components/schemas/coreweave.sandbox.v1.ResourceRequirements'
        securityContext:
          $ref: '#/components/schemas/coreweave.sandbox.v1.SecurityContext'
        imagePullCredentials:
          description: "Request-scoped image pull credentials for this container's image.\n Same type\
            \ and required inner fields as Container.image_pull_credentials.\n When this message is present\
            \ on a template, registry must be a lowercase\n host or host:port, and credentials (store_name,\
            \ path) must be set.\n Image/registry match and secret resolution run when the sandbox is\
            \ created."
          allOf:
          - $ref: '#/components/schemas/coreweave.sandbox.v1.ImagePullCredentials'
        primary:
          description: Same meaning and field number as Container.primary.
          type: boolean
        startupProbe:
          description: Same meaning and field number as Container.startup_probe.
          allOf:
          - $ref: '#/components/schemas/coreweave.sandbox.v1.Probe'
      required:
      - name
    coreweave.sandbox.v1.PartialSandboxSpec:
      description: 'Partial specification for SandboxTemplate.spec and CreateSandboxFromTemplateRequest.overrides.
        Templates and overrides together must produce a valid sandbox specification. In JSON overrides,
        a present message replaces the whole message, a present map replaces the whole map, and a non-empty
        list replaces the whole list. An empty JSON list preserves the template list; it cannot clear
        inherited entries. Nonzero scalars and nonempty strings replace template values; zero or empty
        values preserve them. A containers override replaces the entire list and must supply complete,
        valid containers. runtimeClass and runtimeClassSelection form one runtime selection: setting either
        replaces both, and an explicitly present RUNTIME_CLASS_UNSPECIFIED clears the template selection.'
      type: object
      properties:
        containers:
          description: "Optional on templates. CreateSandboxFromTemplate requires at least one\n container\
            \ on the resolved sandbox after overrides are applied."
          type: array
          items:
            $ref: '#/components/schemas/coreweave.sandbox.v1.PartialContainer'
        volumes:
          type: array
          items:
            $ref: '#/components/schemas/coreweave.sandbox.v1.SandboxVolume'
        services:
          type: array
          items:
            $ref: '#/components/schemas/coreweave.sandbox.v1.Service'
        maxLifetimeSeconds:
          type: integer
          format: int32
        networkIds:
          description: Network membership is not supported. v1 sandbox creation and stored template validation
            reject a non-empty networkIds list. Use network or networkConfigId where supported to configure
            network rules; these fields do not join sandbox networks.
          type: array
          items:
            type: string
        objectStorageAccess:
          $ref: '#/components/schemas/coreweave.sandbox.v1.ObjectStorageAccess'
        tags:
          type: array
          items:
            type: string
        runnerIds:
          type: array
          items:
            type: string
        network:
          $ref: '#/components/schemas/coreweave.sandbox.v1.NetworkOptions'
        annotations:
          type: object
          additionalProperties:
            type: string
        instanceType:
          type: string
        mode:
          description: Placement override. Omitted or SANDBOX_MODE_UNSPECIFIED preserves the template's
            mode. If the merged mode remains unspecified, non-empty template attachments select SANDBOX_MODE_CKS;
            otherwise, placement defaults to SANDBOX_MODE_SERVERLESS.
          type: string
          format: enum
          enum:
          - SANDBOX_MODE_UNSPECIFIED
          - SANDBOX_MODE_SERVERLESS
          - SANDBOX_MODE_CKS
        runtimeClass:
          type: string
        networkConfigId:
          description: Set only in CreateSandboxFromTemplate overrides to bind an unused caller-created
            NetworkConfig. Do not also set overrides.network. A stored SandboxTemplate cannot set networkConfigId;
            keep reusable rules in its network field instead.
          type: string
        runtimeClassSelection:
          description: Portable runtime selection override. If neither runtimeClass nor runtimeClassSelection
            is supplied, the template's runtime selection is preserved. Explicit RUNTIME_CLASS_UNSPECIFIED
            clears both the template's concrete and portable runtime selections and returns to automatic
            selection. Automatic selection uses the CPU or GPU default class on runners with runtime mappings;
            other runners retain their runtime-class default behavior. See SandboxSpec.runtimeClassSelection
            for placement and validation rules.
          type: string
          format: enum
          enum:
          - RUNTIME_CLASS_UNSPECIFIED
          - RUNTIME_CLASS_CPU_DEFAULT
          - RUNTIME_CLASS_CPU_NESTED_VIRT
          - RUNTIME_CLASS_CPU_SNAPSHOT_RESTORE
          - RUNTIME_CLASS_GPU_DEFAULT
    coreweave.sandbox.v1.PlacementOrgConfig:
      description: Legacy configuration for one placement organization. The gateway no longer reads this
        resource to enforce quotas. Get and Delete remain available for inspecting and removing legacy
        rows; Update returns UNIMPLEMENTED. The caller must hold sandbox_admin and target its own placement
        organization.
      type: object
      properties:
        placementOrganizationId:
          description: "The placement (pool) organization this config governs — the resource\n identifier,\
            \ unique across configs. Named explicitly by the admin."
          type: string
        activeSandboxQuota:
          description: Legacy per-placement-organization quota. This value is no longer enforced by the
            gateway. Serverless quotas come from gateway runtime configuration; UpdatePlacementOrgConfig
            returns UNIMPLEMENTED.
          allOf:
          - $ref: '#/components/schemas/coreweave.sandbox.v1.ActiveSandboxQuota'
        createTime:
          type: string
          format: date-time
          readOnly: true
        updateTime:
          type: string
          format: date-time
          readOnly: true
      required:
      - activeSandboxQuota
    coreweave.sandbox.v1.Policy:
      description: Policy governs sandboxes on its runner. Resolution applies runtime defaults, then policy
        base, then the sandbox spec. The sandbox spec takes precedence for scalar defaults; policy attachments
        still apply, and administrator-pinned Pod metadata takes precedence when annotation keys overlap.
        Constraints validate the fully resolved spec and reject violations rather than silently rewriting
        values. An empty policy supplies no base defaults or explicit constraints, but platform safety
        gates and runtime-class restrictions still apply. An absent allowedRuntimeClasses list permits
        no concrete runtimeClass pin. v1 managed-runner creation requires an explicit policy.
      type: object
      properties:
        displayName:
          description: Human-readable name for this policy posture.
          type: string
        base:
          description: "Admin attachments and runtime defaults applied to every sandbox on the\n runner.\
            \ Opaque: its schema is determined by the runner's runtime (for\n example, a PodSpec fragment\
            \ on a Kubernetes runner). Not a second home for\n security, lifetime, or other typed constraint\
            \ concerns — those live under\n constraints."
          type: object
        constraints:
          description: Typed clamps validated against the resolved sandbox spec.
          allOf:
          - $ref: '#/components/schemas/coreweave.sandbox.v1.PolicyConstraints'
        controlPlaneAccess:
          description: "Request-time controls for Sandbox API operations targeting this runner.\n These\
            \ controls supplement authentication and tenant authorization; they\n do not restrict traffic\
            \ sent directly to services exposed by a Sandbox."
          allOf:
          - $ref: '#/components/schemas/coreweave.sandbox.v1.ControlPlaneAccessPolicy'
    coreweave.sandbox.v1.PolicyConstraints:
      description: Typed constraints a policy enforces. Each group is optional. Omitting a group adds
        no explicit constraints of that kind, but platform safety gates and runtime-class restrictions
        still apply. An empty or absent allowedRuntimeClasses list permits no concrete runtimeClass pin.
      type: object
      properties:
        resources:
          $ref: '#/components/schemas/coreweave.sandbox.v1.ResourceConstraints'
        image:
          $ref: '#/components/schemas/coreweave.sandbox.v1.ImageConstraints'
        network:
          $ref: '#/components/schemas/coreweave.sandbox.v1.NetworkConstraints'
        security:
          $ref: '#/components/schemas/coreweave.sandbox.v1.SecurityConstraints'
        instance:
          $ref: '#/components/schemas/coreweave.sandbox.v1.InstanceConstraints'
        lifecycle:
          $ref: '#/components/schemas/coreweave.sandbox.v1.LifecycleConstraints'
        metadata:
          $ref: '#/components/schemas/coreweave.sandbox.v1.MetadataConstraints'
        volumes:
          $ref: '#/components/schemas/coreweave.sandbox.v1.VolumeConstraints'
    coreweave.sandbox.v1.PortRange:
      description: PortRange is a protocol plus a single port or contiguous port range.
      type: object
      properties:
        protocol:
          description: TCP (default), UDP, or SCTP.
          type: string
        port:
          type: integer
          format: int32
        endPort:
          description: Inclusive end of a contiguous range; unset or equal to port = single port.
          type: integer
          format: int32
      required:
      - port
    coreweave.sandbox.v1.Probe:
      description: "Probe is an exec-only startup check on a container.\n\n CreateSandbox omitted timings:\
        \ period 10s, timeout 1s, failure_threshold 3,\n initial_delay_seconds 0. An empty Probe (no exec)\
        \ is omit.\n\n CreateSandboxFromFile Compose healthcheck: omitted timings take Compose\n defaults,\
        \ then map. interval → period_seconds and timeout →\n timeout_seconds (integer seconds; sub-second\
        \ values reject). start_period\n raises failure_threshold (retries + ceil(start_period / period));\n\
        \ initial_delay_seconds stays 0. The container is killed when\n failure_threshold is reached."
      type: object
      properties:
        exec:
          type: array
          items:
            type: string
        periodSeconds:
          type: integer
          format: int32
        timeoutSeconds:
          type: integer
          format: int32
        failureThreshold:
          type: integer
          format: int32
        initialDelaySeconds:
          type: integer
          format: int32
    coreweave.sandbox.v1.ProfileEgressModeConfig:
      description: ProfileEgressModeConfig defines one named egress mode.
      type: object
      properties:
        type:
          type: string
          format: enum
          enum:
          - PROFILE_EGRESS_TYPE_UNSPECIFIED
          - PROFILE_EGRESS_TYPE_INTERNET
          - PROFILE_EGRESS_TYPE_USER
          - PROFILE_EGRESS_TYPE_ORG
          - PROFILE_EGRESS_TYPE_PROFILE
          - PROFILE_EGRESS_TYPE_ALLOWLIST
          - PROFILE_EGRESS_TYPE_NONE
        cidrs:
          type: array
          items:
            type: string
    coreweave.sandbox.v1.ProfileIngressConfig:
      description: ProfileIngressConfig defines native Kubernetes Ingress exposure settings.
      type: object
      properties:
        controllerName:
          type: string
        template:
          type: string
    coreweave.sandbox.v1.ProfileIngressModeConfig:
      description: ProfileIngressModeConfig defines one named ingress mode.
      type: object
      properties:
        service:
          $ref: '#/components/schemas/coreweave.sandbox.v1.ProfileServiceConfig'
        ingress:
          $ref: '#/components/schemas/coreweave.sandbox.v1.ProfileIngressConfig'
        route:
          $ref: '#/components/schemas/coreweave.sandbox.v1.ProfileRouteConfig'
        scope:
          type: string
          format: enum
          enum:
          - PROFILE_INGRESS_SCOPE_UNSPECIFIED
          - PROFILE_INGRESS_SCOPE_USER
          - PROFILE_INGRESS_SCOPE_ORG
          - PROFILE_INGRESS_SCOPE_PROFILE
          - PROFILE_INGRESS_SCOPE_ANY
        expectsExternalAddress:
          type: boolean
    coreweave.sandbox.v1.ProfileNamespaceConfig:
      description: ProfileNamespaceConfig controls sandbox namespace placement.
      type: object
      properties:
        strategy:
          type: string
          format: enum
          enum:
          - PROFILE_NAMESPACE_STRATEGY_UNSPECIFIED
          - PROFILE_NAMESPACE_STRATEGY_STATIC
          - PROFILE_NAMESPACE_STRATEGY_PER_PROFILE
          - PROFILE_NAMESPACE_STRATEGY_PER_ORG
          - PROFILE_NAMESPACE_STRATEGY_PER_USER
        staticNamespace:
          type: string
        namespacePrefix:
          type: string
        autoCreate:
          description: Defaults to true when unset.
          type: boolean
        labels:
          type: object
          additionalProperties:
            type: string
        annotations:
          type: object
          additionalProperties:
            type: string
    coreweave.sandbox.v1.ProfileNetworkConfig:
      description: ProfileNetworkConfig controls sandbox network policy and service exposure.
      type: object
      properties:
        egress:
          $ref: '#/components/schemas/coreweave.sandbox.v1.ProfileNetworkEgressConfig'
        ingress:
          type: object
          additionalProperties:
            $ref: '#/components/schemas/coreweave.sandbox.v1.ProfileIngressModeConfig'
    coreweave.sandbox.v1.ProfileNetworkEgressConfig:
      description: ProfileNetworkEgressConfig defines named egress modes.
      type: object
      properties:
        defaultMode:
          description: Default egress mode name. Required when multiple modes are defined.
          type: string
        modes:
          description: Named egress modes.
          type: object
          additionalProperties:
            $ref: '#/components/schemas/coreweave.sandbox.v1.ProfileEgressModeConfig'
    coreweave.sandbox.v1.ProfileRouteConfig:
      description: ProfileRouteConfig selects a pluggable exposure-route provider.
      type: object
      properties:
        provider:
          type: string
        hostnameTemplate:
          type: string
        config:
          type: object
          additionalProperties:
            type: string
    coreweave.sandbox.v1.ProfileServiceConfig:
      description: ProfileServiceConfig defines Kubernetes Service exposure settings.
      type: object
      properties:
        serviceType:
          description: Kubernetes Service type, for example ClusterIP, NodePort, or LoadBalancer.
          type: string
        serviceSelectorAnnotation:
          $ref: '#/components/schemas/coreweave.sandbox.v1.AnnotationPair'
        dnsAnnotation:
          $ref: '#/components/schemas/coreweave.sandbox.v1.AnnotationPair'
    coreweave.sandbox.v1.ProfileSpec:
      description: "ProfileSpec defines compute, placement, namespace, networking, and pod-template\n\
        \ defaults for sandboxes scheduled through a profile."
      type: object
      properties:
        containerImage:
          description: Container image default.
          type: string
        runtimeClass:
          description: Runtime class name for sandbox isolation.
          type: string
        resourceDefaults:
          description: Resource defaults for sandboxes on this profile.
          allOf:
          - $ref: '#/components/schemas/coreweave.sandbox.v1.ResourceDefaults'
        instanceTypes:
          description: Node instance types this profile may schedule onto.
          type: array
          items:
            type: string
        nodeSelector:
          description: Node selector labels.
          type: object
          additionalProperties:
            type: string
        tags:
          description: Tags for RBAC-based access control.
          type: array
          items:
            type: string
        namespace:
          description: Namespace placement strategy.
          allOf:
          - $ref: '#/components/schemas/coreweave.sandbox.v1.ProfileNamespaceConfig'
        network:
          description: Network policy and exposure modes.
          allOf:
          - $ref: '#/components/schemas/coreweave.sandbox.v1.ProfileNetworkConfig'
        podTemplate:
          description: "Admin-authored pod template fragment in the runner's PodConfig shape. This\n remains\
            \ opaque because it contains Kubernetes-specific PodSpec fields."
          type: object
    coreweave.sandbox.v1.ProfileTemplate:
      description: ProfileTemplate defines a reusable profile configuration.
      type: object
      properties:
        profileTemplateId:
          description: Server-assigned profile template identifier.
          type: string
          readOnly: true
        displayName:
          description: Human-readable template name, unique within the organization.
          type: string
        description:
          description: Human-readable description.
          type: string
        spec:
          description: Profile specification. Required on create / full-replace.
          allOf:
          - $ref: '#/components/schemas/coreweave.sandbox.v1.ProfileSpec'
        labels:
          description: User-defined labels for organizing templates.
          type: object
          additionalProperties:
            type: string
        createTime:
          type: string
          format: date-time
          readOnly: true
        updateTime:
          type: string
          format: date-time
          readOnly: true
    coreweave.sandbox.v1.PurgeSandboxesRequest:
      type: object
      properties:
        tags:
          description: "Scope selector: sandboxes matching all tags (AND). Must be non-empty unless\n\
            \ purge_all is true."
          type: array
          items:
            type: string
        dryRun:
          description: "Dry-run guard. false (default) terminates the matched sandboxes; true reports\n\
            \ how many sandboxes would be purged and terminates nothing."
          type: boolean
        requestId:
          description: "Idempotency key (AIP-155), reserved for future support. Non-empty values\n are\
            \ currently rejected with UNIMPLEMENTED."
          type: string
        purgeAll:
          description: "Scope selector: match every active in-scope sandbox. Mutually exclusive with\n\
            \ tags, and required when tags is empty."
          type: boolean
    coreweave.sandbox.v1.PurgeSandboxesResponse:
      type: object
      properties:
        purgeCount:
          description: "Number of sandboxes successfully purged, or, on a dry-run (dry_run=true), the\n\
            \ number that would be purged."
          type: integer
          format: int32
        failedSandboxIds:
          description: "Ids of sandboxes that matched but could not be terminated; retry to purge\n them.\
            \ Empty on a dry-run (dry_run=true)."
          type: array
          items:
            type: string
        retryableFailedSandboxIds:
          description: "Subset of failed_sandbox_ids whose failure was retryable. These sandboxes\n were\
            \ not purged by this request, but may converge on a later retry (for\n example placement or\
            \ route reconciliation was still in flight)."
          type: array
          items:
            type: string
    coreweave.sandbox.v1.PvcVolumeSource:
      description: "PvcVolumeSource references an existing PersistentVolumeClaim in the cluster\n that\
        \ hosts the referenced managed runner. Registration is by reference\n only: the claim and its\
        \ data are read, never written, by the platform.\n Mounting a Volume with this source pins sandbox\
        \ scheduling to the owning\n runner."
      type: object
      properties:
        runnerId:
          description: Org-unique managed-runner id whose cluster holds the claim. Immutable.
          type: string
        namespace:
          description: The claim's namespace in that cluster. Immutable.
          type: string
        claimName:
          description: The PersistentVolumeClaim name. Immutable.
          type: string
        subPath:
          description: "Optional volume-level root prefix inside the claim. Relative and\n canonical (no\
            \ \".\" / \"..\"). Immutable."
          type: string
      required:
      - runnerId
      - namespace
      - claimName
    coreweave.sandbox.v1.ReadFileResponse:
      type: object
      properties:
        content:
          format: bytes
          type: string
    coreweave.sandbox.v1.ResourceConstraints:
      description: "ResourceConstraints bounds a container's compute. String quantities mirror\n Resources\
        \ (e.g. \"8\", \"500m\", \"32Gi\")."
      type: object
      properties:
        maxCpu:
          description: Per-container maxima.
          type: string
        maxMemory:
          type: string
        minCpu:
          description: Per-container minima.
          type: string
        minMemory:
          type: string
        defaultCpu:
          description: "Per-container defaults applied when the spec leaves a value unset.\n When neither\
            \ requests nor limits is declared, positive CPU and memory\n defaults also supply matching\
            \ limits."
          type: string
        defaultMemory:
          type: string
        maxGpuCount:
          description: "Maximum GPUs per container. Presence-aware: unset = no cap; an explicit 0\n bans\
            \ GPU requests entirely (a GPU-free pool is expressible)."
          type: string
        cpuCeiling:
          description: Sum-of-requests ceiling across the whole sandbox.
          type: string
        memoryCeiling:
          type: string
        requireLimits:
          description: Require every container to have requests and limits after defaulting.
          type: boolean
    coreweave.sandbox.v1.ResourceDefaults:
      description: ResourceDefaults defines default resource requests and limits for sandboxes.
      type: object
      properties:
        cpuRequest:
          type: string
        memoryRequest:
          type: string
        cpuLimit:
          type: string
        memoryLimit:
          type: string
    coreweave.sandbox.v1.ResourceRequirements:
      description: "ResourceRequirements is a container's compute allocation: requests (the\n guaranteed\
        \ floor) and optional limits (the burst ceiling). Guaranteed QoS when\n limits is empty or equals\
        \ requests; Burstable when limits exceeds requests.\n GPU is taken from requests (it is not a\
        \ burst dimension)."
      type: object
      properties:
        requests:
          $ref: '#/components/schemas/coreweave.sandbox.v1.Resources'
        limits:
          $ref: '#/components/schemas/coreweave.sandbox.v1.Resources'
    coreweave.sandbox.v1.ResourceUsage:
      description: ResourceUsage is real-time consumption.
      type: object
      properties:
        cpuMillicores:
          type: string
          readOnly: true
        memoryMb:
          type: string
          readOnly: true
        gpuCount:
          type: string
          readOnly: true
    coreweave.sandbox.v1.Resources:
      description: Resources is a guaranteed compute allocation for a container.
      type: object
      properties:
        cpu:
          description: CPU cores, decimal or milli (e.g. "500m", "2", "2.5").
          type: string
        memory:
          description: Memory with a binary/decimal suffix (e.g. "512Mi", "4Gi").
          type: string
        gpu:
          description: "GPU allocation. Permitted on the primary container only; a non-primary\n container\
            \ that sets gpu is INVALID_ARGUMENT (CWSANDBOX_INVALID_REQUEST)."
          allOf:
          - $ref: '#/components/schemas/coreweave.sandbox.v1.Gpu'
    coreweave.sandbox.v1.RunnerCapabilitySummary:
      description: "RunnerCapabilitySummary describes a runner's reported features and aggregate\n capacity\
        \ ceilings, rather than its currently available resources.\n\n The max_cpu_millicores, max_memory_bytes,\
        \ and max_gpu_count values can change\n between responses. Depending on runner configuration,\
        \ CPU and memory ceilings\n may exclude capacity reserved for GPU workloads and can change without\
        \ nodes\n being added or removed. These values do not guarantee that a placement fits.\n\n When\
        \ capability information is available, feature fields are exposed for\n both owned and shared\
        \ runners. The max_* values are disclosed only for owned\n runners; they remain zero for shared\
        \ runners (AvailableRunner.is_shared).\n A zero value alone does not distinguish zero capacity\
        \ from an unreported or\n undisclosed ceiling.\n\n When capabilities and resources are both present,\
        \ use values from the same\n response rather than combining resources with cached ceilings. They\
        \ need not\n reflect the same measurement time."
      type: object
      properties:
        maxCpuMillicores:
          description: Reported aggregate CPU capacity ceiling, in millicores.
          type: string
          readOnly: true
        maxMemoryBytes:
          description: Reported aggregate memory capacity ceiling, in bytes.
          type: string
          readOnly: true
        maxGpuCount:
          description: Reported aggregate GPU capacity, including GPUs currently in use.
          type: string
          readOnly: true
        supportedGpuTypes:
          type: array
          items:
            type: string
          readOnly: true
        supportedArchitectures:
          type: array
          items:
            type: string
          readOnly: true
        supportsPrivileged:
          type: boolean
          readOnly: true
        availableStorageClasses:
          type: array
          items:
            type: string
          readOnly: true
        supportedServiceVisibilities:
          description: Generic L4 service visibilities this runner can enforce through the v1 Service
            path. VISIBILITY_UNSPECIFIED denotes ports that are not reachable from outside the sandbox.
            Operator-defined beta mode names are never exposed.
          type: array
          items:
            enum:
            - VISIBILITY_UNSPECIFIED
            - VISIBILITY_PUBLIC
            - VISIBILITY_PRIVATE
            - VISIBILITY_CUSTOM
            type: string
            format: enum
          readOnly: true
    coreweave.sandbox.v1.RunnerDataPlaneClusterIPConfig:
      description: "RunnerDataPlaneClusterIPConfig exposes the direct endpoint through a stable\n ClusterIP\
        \ Service. The platform derives its URI and server-certificate SANs."
      type: object
      properties:
        annotations:
          type: object
          additionalProperties:
            type: string
    coreweave.sandbox.v1.RunnerDataPlaneConfig:
      description: "RunnerDataPlaneConfig controls the dedicated Runner endpoint for direct\n sandbox\
        \ data operations. The platform issues and rotates the endpoint's\n server certificate; this configuration\
        \ contains no certificate source or\n private key material."
      type: object
      properties:
        disabled:
          $ref: '#/components/schemas/coreweave.sandbox.v1.RunnerDataPlaneDisabledConfig'
        clusterIp:
          $ref: '#/components/schemas/coreweave.sandbox.v1.RunnerDataPlaneClusterIPConfig'
        loadBalancer:
          $ref: '#/components/schemas/coreweave.sandbox.v1.RunnerDataPlaneLoadBalancerConfig'
        custom:
          $ref: '#/components/schemas/coreweave.sandbox.v1.RunnerDataPlaneCustomConfig'
    coreweave.sandbox.v1.RunnerDataPlaneCustomConfig:
      description: "RunnerDataPlaneCustomConfig advertises a customer-managed network path such\n as a\
        \ VPC route, VPN, service mesh, or Tailscale address. The platform still\n issues the Runner's\
        \ server certificate for the URI's authority."
      type: object
      properties:
        advertisedUri:
          description: Stable absolute URI returned to direct clients.
          type: string
        serviceAnnotations:
          description: "Annotations applied to the backing ClusterIP Service for integrations that\n discover\
            \ or route Kubernetes Services."
          type: object
          additionalProperties:
            type: string
      required:
      - advertisedUri
    coreweave.sandbox.v1.RunnerDataPlaneDisabledConfig:
      description: RunnerDataPlaneDisabledConfig explicitly disables the direct endpoint.
      type: object
      properties: {}
    coreweave.sandbox.v1.RunnerDataPlaneLoadBalancerConfig:
      description: "RunnerDataPlaneLoadBalancerConfig exposes the direct endpoint through a\n stable L4\
        \ LoadBalancer Service. The Service forwards TCP to the Runner and\n does not terminate mutual\
        \ TLS."
      type: object
      properties:
        scope:
          description: Reachability scope for the load balancer. Omit this field to use the public scope.
            RUNNER_DATA_PLANE_SERVICE_SCOPE_UNSPECIFIED uses the same scope as RUNNER_DATA_PLANE_SERVICE_SCOPE_PUBLIC.
            Private scope also requires a load balancer class or provider annotation.
          type: string
          format: enum
          enum:
          - RUNNER_DATA_PLANE_SERVICE_SCOPE_UNSPECIFIED
          - RUNNER_DATA_PLANE_SERVICE_SCOPE_PUBLIC
          - RUNNER_DATA_PLANE_SERVICE_SCOPE_PRIVATE
        loadBalancerClass:
          type: string
        annotations:
          type: object
          additionalProperties:
            type: string
        sourceRanges:
          type: array
          items:
            type: string
        externalTrafficPolicy:
          description: External traffic routing policy. Omit this field to use the cluster policy. RUNNER_DATA_PLANE_EXTERNAL_TRAFFIC_POLICY_UNSPECIFIED
            uses RUNNER_DATA_PLANE_EXTERNAL_TRAFFIC_POLICY_CLUSTER.
          type: string
          format: enum
          enum:
          - RUNNER_DATA_PLANE_EXTERNAL_TRAFFIC_POLICY_UNSPECIFIED
          - RUNNER_DATA_PLANE_EXTERNAL_TRAFFIC_POLICY_CLUSTER
          - RUNNER_DATA_PLANE_EXTERNAL_TRAFFIC_POLICY_LOCAL
        hostname:
          description: "DNS name to publish for the endpoint and include in its server\n certificate.\
            \ When empty, the platform may assign one."
          type: string
    coreweave.sandbox.v1.RunnerDataPlaneStatus:
      description: "RunnerDataPlaneStatus reports the endpoint observed across the logical\n Runner's\
        \ accepting shards."
      type: object
      properties:
        state:
          description: Reported endpoint state. RUNNER_DATA_PLANE_STATE_UNSPECIFIED means no endpoint
            state is specified.
          type: string
          format: enum
          enum:
          - RUNNER_DATA_PLANE_STATE_UNSPECIFIED
          - RUNNER_DATA_PLANE_STATE_DISABLED
          - RUNNER_DATA_PLANE_STATE_PENDING
          - RUNNER_DATA_PLANE_STATE_READY
          - RUNNER_DATA_PLANE_STATE_NOT_READY
          readOnly: true
        endpointId:
          type: string
          readOnly: true
        advertisedUri:
          type: string
          readOnly: true
        protocols:
          type: array
          items:
            type: string
          readOnly: true
        serverCertificateExpiresAt:
          type: string
          format: date-time
          readOnly: true
        message:
          type: string
          readOnly: true
        lastTransitionTime:
          type: string
          format: date-time
          readOnly: true
    coreweave.sandbox.v1.RunnerDeploymentOverrides:
      description: RunnerDeploymentOverrides contains customer-settable runner deployment overrides.
      type: object
      properties:
        nodeSelector:
          type: object
          additionalProperties:
            type: string
        tolerations:
          type: array
          items:
            $ref: '#/components/schemas/coreweave.sandbox.v1.RunnerToleration'
        resources:
          $ref: '#/components/schemas/coreweave.sandbox.v1.RunnerResourceRequirements'
        annotations:
          type: object
          additionalProperties:
            type: string
        labels:
          type: object
          additionalProperties:
            type: string
        env:
          type: object
          additionalProperties:
            type: string
        args:
          type: array
          items:
            type: string
        scaling:
          $ref: '#/components/schemas/coreweave.sandbox.v1.RunnerScalingConfig'
        cpuRuntimeClass:
          type: string
        gpuRuntimeClass:
          type: string
        affinity:
          description: "Kubernetes Affinity object for runner pods only, using Kubernetes JSON\n field\
            \ names. Supports node affinity, pod affinity, and pod anti-affinity.\n Replaces inherited\
            \ affinity as a whole; an empty object clears it."
          type: object
    coreweave.sandbox.v1.RunnerDeploymentSpec:
      description: RunnerDeploymentSpec is the resolved runner deployment specification.
      type: object
      properties:
        image:
          type: string
          readOnly: true
        env:
          type: object
          additionalProperties:
            type: string
          readOnly: true
        args:
          type: array
          items:
            type: string
          readOnly: true
        resources:
          allOf:
          - $ref: '#/components/schemas/coreweave.sandbox.v1.RunnerResourceRequirements'
          readOnly: true
        nodeSelector:
          type: object
          additionalProperties:
            type: string
          readOnly: true
        tolerations:
          type: array
          items:
            $ref: '#/components/schemas/coreweave.sandbox.v1.RunnerToleration'
          readOnly: true
        scaling:
          allOf:
          - $ref: '#/components/schemas/coreweave.sandbox.v1.RunnerScalingConfig'
          readOnly: true
        annotations:
          type: object
          additionalProperties:
            type: string
          readOnly: true
        labels:
          type: object
          additionalProperties:
            type: string
          readOnly: true
        serviceAccount:
          type: string
          readOnly: true
        extraVolumes:
          type: array
          items:
            $ref: '#/components/schemas/coreweave.sandbox.v1.RunnerVolumeMount'
          readOnly: true
        readinessProbe:
          allOf:
          - $ref: '#/components/schemas/coreweave.sandbox.v1.RunnerProbeConfig'
          readOnly: true
        livenessProbe:
          allOf:
          - $ref: '#/components/schemas/coreweave.sandbox.v1.RunnerProbeConfig'
          readOnly: true
        initResources:
          allOf:
          - $ref: '#/components/schemas/coreweave.sandbox.v1.RunnerResourceRequirements'
          readOnly: true
        imagePullPolicy:
          type: string
          readOnly: true
        gatewayServer:
          type: string
          readOnly: true
        cpuRuntimeClass:
          type: string
          readOnly: true
        gpuRuntimeClass:
          type: string
          readOnly: true
        endpointRoutes:
          description: "Platform-owned product endpoint-route configuration. OUTPUT_ONLY for\n customers;\
            \ configured via platform deployment defaults / version specs."
          allOf:
          - $ref: '#/components/schemas/coreweave.sandbox.v1.RunnerEndpointRoutes'
          readOnly: true
        dataPlane:
          description: Resolved direct data-plane endpoint configuration.
          allOf:
          - $ref: '#/components/schemas/coreweave.sandbox.v1.RunnerDataPlaneConfig'
          readOnly: true
        affinity:
          description: Resolved Kubernetes Affinity object for runner pods only.
          type: object
          readOnly: true
    coreweave.sandbox.v1.RunnerEndpointGateway:
      description: "RunnerEndpointGateway identifies the shared parent Gateway a product route\n attaches\
        \ to. DNS suffix is resolved from the Gateway Listener at create-path."
      type: object
      properties:
        name:
          type: string
          readOnly: true
        namespace:
          type: string
          readOnly: true
        listener:
          type: string
          readOnly: true
    coreweave.sandbox.v1.RunnerEndpointRoute:
      description: "RunnerEndpointRoute configures one independently mergeable endpoint-route\n slot.\
        \ enabled=true requires gateway; enabled=false clears an inherited slot\n and rejects gateway.\
        \ provider accepted values depend on the parent slot."
      type: object
      properties:
        enabled:
          type: boolean
          readOnly: true
        gateway:
          allOf:
          - $ref: '#/components/schemas/coreweave.sandbox.v1.RunnerEndpointGateway'
          readOnly: true
        provider:
          description: "Ingress extras for this slot. Accepted values are slot-dependent.\n OUTPUT_ONLY\
            \ on the customer surface; configured via the platform\n managed-runner API."
          type: string
          readOnly: true
    coreweave.sandbox.v1.RunnerEndpointRoutes:
      description: "RunnerEndpointRoutes is platform-owned product endpoint-route configuration.\n Slots\
        \ are independent: HTTPS-only, TLS-only, or both."
      type: object
      properties:
        https:
          description: Product HTTPS endpoint route. provider is omitted, empty, or exact "envoy".
          allOf:
          - $ref: '#/components/schemas/coreweave.sandbox.v1.RunnerEndpointRoute'
          readOnly: true
        tlsPassthrough:
          description: "SNI passthrough at the shared Gateway. Independent of https.\n provider is omitted\
            \ or empty."
          allOf:
          - $ref: '#/components/schemas/coreweave.sandbox.v1.RunnerEndpointRoute'
          readOnly: true
    coreweave.sandbox.v1.RunnerIdentity:
      description: RunnerIdentity contains stable runner identity fields.
      type: object
      properties:
        runnerId:
          description: Operator-assigned runner identifier, unique within the organization.
          type: string
        runnerGroupId:
          description: Runner group ID for scheduling affinity.
          type: string
        zone:
          description: Geographic zone. Immutable after create.
          type: string
        clusterId:
          description: Cluster UUID. Immutable after create.
          type: string
        clusterName:
          description: Cluster display name resolved by the server.
          type: string
          readOnly: true
    coreweave.sandbox.v1.RunnerImagePullConfig:
      description: "RunnerImagePullConfig sets the image pull behavior for sandbox workload\n containers\
        \ scheduled on a managed runner. Platform-owned helper containers\n keep their own pull behavior\
        \ and are unaffected."
      type: object
      properties:
        policy:
          description: Pull policy applied to every sandbox workload container on this runner. Defaults
            to IF_NOT_PRESENT. Omit this field for the default; SANDBOX_IMAGE_PULL_POLICY_UNSPECIFIED
            also uses SANDBOX_IMAGE_PULL_POLICY_IF_NOT_PRESENT.
          type: string
          format: enum
          enum:
          - SANDBOX_IMAGE_PULL_POLICY_UNSPECIFIED
          - SANDBOX_IMAGE_PULL_POLICY_IF_NOT_PRESENT
          - SANDBOX_IMAGE_PULL_POLICY_ALWAYS
    coreweave.sandbox.v1.RunnerInstallError:
      description: RunnerInstallError is structured failure detail for failed runner installs.
      type: object
      properties:
        reason:
          description: Installation failure reason. RUNNER_INSTALL_FAILURE_REASON_UNSPECIFIED means no
            specific failure reason is reported.
          type: string
          format: enum
          enum:
          - RUNNER_INSTALL_FAILURE_REASON_UNSPECIFIED
          - RUNNER_INSTALL_FAILURE_REASON_NO_SCHEDULABLE_NODES
          - RUNNER_INSTALL_FAILURE_REASON_TAINT_TOLERATION_MISMATCH
          - RUNNER_INSTALL_FAILURE_REASON_NODE_SELECTOR_NO_MATCH
          - RUNNER_INSTALL_FAILURE_REASON_INSUFFICIENT_RESOURCES
          - RUNNER_INSTALL_FAILURE_REASON_IMAGE_PULL_FAILED
          - RUNNER_INSTALL_FAILURE_REASON_CLUSTER_NOT_READY
          - RUNNER_INSTALL_FAILURE_REASON_QUOTA_EXCEEDED
          - RUNNER_INSTALL_FAILURE_REASON_ROLLOUT_TIMED_OUT
          - RUNNER_INSTALL_FAILURE_REASON_INTERNAL_ERROR
          - RUNNER_INSTALL_FAILURE_REASON_CLUSTER_ACCESS_FAILED
          - RUNNER_INSTALL_FAILURE_REASON_GATEWAY_UNREACHABLE
          - RUNNER_INSTALL_FAILURE_REASON_JOIN_TOKEN_FAILED
          - RUNNER_INSTALL_FAILURE_REASON_RUNNER_OFFLINE
          - RUNNER_INSTALL_FAILURE_REASON_CERT_EXPIRED
          - RUNNER_INSTALL_FAILURE_REASON_CLUSTER_NODES_UNHEALTHY
          readOnly: true
        message:
          type: string
          readOnly: true
        diagnosticDetail:
          type: string
          readOnly: true
        remediationHints:
          type: array
          items:
            type: string
          readOnly: true
        occurredTime:
          type: string
          format: date-time
          readOnly: true
    coreweave.sandbox.v1.RunnerProbeConfig:
      description: RunnerProbeConfig defines health probe configuration.
      type: object
      properties:
        path:
          type: string
        port:
          type: integer
          format: int32
        initialDelaySeconds:
          type: integer
          format: int32
        periodSeconds:
          type: integer
          format: int32
        failureThreshold:
          type: integer
          format: int32
        timeoutSeconds:
          type: integer
          format: int32
    coreweave.sandbox.v1.RunnerProfileBinding:
      description: RunnerProfileBinding associates a profile template with a managed runner.
      type: object
      properties:
        runnerProfileBindingId:
          description: Server-assigned binding identifier.
          type: string
          readOnly: true
        profileTemplateId:
          description: Profile template id to bind.
          type: string
        profileName:
          description: Profile name advertised on this runner. Defaults to the template display name.
          type: string
        isDefault:
          description: Whether this is the runner's default profile.
          type: boolean
        overrides:
          description: Per-binding profile overrides.
          allOf:
          - $ref: '#/components/schemas/coreweave.sandbox.v1.ProfileSpec'
        createTime:
          type: string
          format: date-time
          readOnly: true
        updateTime:
          type: string
          format: date-time
          readOnly: true
      required:
      - profileTemplateId
    coreweave.sandbox.v1.RunnerResourceRequirements:
      description: RunnerResourceRequirements defines CPU and memory requests/limits.
      type: object
      properties:
        cpuRequest:
          type: string
        memoryRequest:
          type: string
        cpuLimit:
          type: string
        memoryLimit:
          type: string
    coreweave.sandbox.v1.RunnerResourceSummary:
      description: "RunnerResourceSummary is a runner's dynamic, currently-available resources.\n\n available_cpu_millicores\
        \ and available_memory_bytes are usually the measured\n availability, but for a short window after\
        \ the runner's capacity changes they\n may instead be reported at the runner's advertised ceiling\
        \ while that ceiling\n is being republished. In that window a value derived as ceiling minus\n\
        \ available can read zero even though the runner has usage. available_gpu_count\n is always the\
        \ measurement.\n\n When comparing with capacity ceilings, use capabilities from the same\n response\
        \ when present. The values need not reflect the same measurement time."
      type: object
      properties:
        availableCpuMillicores:
          description: "Measured available CPU in millicores, or the advertised CPU ceiling during\n the\
            \ window described above."
          type: string
          readOnly: true
        availableMemoryBytes:
          description: "Measured available memory in bytes, or the advertised memory ceiling during\n\
            \ the window described above."
          type: string
          readOnly: true
        availableGpuCount:
          description: Measured available GPUs; never adjusted to a ceiling.
          type: string
          readOnly: true
        runningSandboxes:
          type: integer
          format: int32
          readOnly: true
    coreweave.sandbox.v1.RunnerScalingConfig:
      description: RunnerScalingConfig defines runner deployment scaling.
      type: object
      properties:
        replicas:
          type: integer
          format: int32
        autoscalingEnabled:
          type: boolean
        minReplicas:
          type: integer
          format: int32
        maxReplicas:
          type: integer
          format: int32
    coreweave.sandbox.v1.RunnerTenantMetricsConfig:
      description: "RunnerTenantMetricsConfig toggles the tenant-metrics collector on a\n managed runner's\
        \ cluster (per-sandbox usage metrics attributed to the\n tenant org)."
      type: object
      properties:
        enabled:
          description: Enable the tenant-metrics collector for this runner's cluster.
          type: boolean
        image:
          description: "Collector image, release-pinned. When empty, an image already present\n in the\
            \ deployment env applies."
          type: string
    coreweave.sandbox.v1.RunnerToleration:
      description: RunnerToleration defines a Kubernetes toleration.
      type: object
      properties:
        key:
          type: string
        operator:
          type: string
        value:
          type: string
        effect:
          type: string
    coreweave.sandbox.v1.RunnerVolumeMount:
      description: RunnerVolumeMount defines an extra volume mount for a runner pod.
      type: object
      properties:
        mountPath:
          type: string
        name:
          type: string
        readOnly:
          type: boolean
        subPath:
          type: string
        configMapName:
          type: string
        secretName:
          type: string
        emptyDir:
          type: boolean
    coreweave.sandbox.v1.RunnerVolumesConfig:
      description: "RunnerVolumesConfig toggles registered-Volume (PVC) mounts on a managed\n runner.\
        \ Enabling is necessary but not sufficient: the runner advertises\n volume support only after\
        \ its startup PVC/PV RBAC preflight passes."
      type: object
      properties:
        enabled:
          description: Enable registered-Volume mounts on this runner.
          type: boolean
        csiDriverAllowlist:
          description: "CSI drivers allowed to back registered Volumes on this runner. Empty =\n the platform\
            \ default allowlist (csi.vastdata.com)."
          type: array
          items:
            type: string
    coreweave.sandbox.v1.RuntimeClassMapping:
      description: "RuntimeClassMapping binds a recognized, nonzero runtime class to an explicit\n execution\
        \ target. Each runtime class can appear at most once in a catalog."
      type: object
      properties:
        runtimeClass:
          description: Required execution contract for this mapping. Specify a recognized nonzero runtime
            class. RUNTIME_CLASS_UNSPECIFIED is invalid in a mapping.
          type: string
          format: enum
          enum:
          - RUNTIME_CLASS_UNSPECIFIED
          - RUNTIME_CLASS_CPU_DEFAULT
          - RUNTIME_CLASS_CPU_NESTED_VIRT
          - RUNTIME_CLASS_CPU_SNAPSHOT_RESTORE
          - RUNTIME_CLASS_GPU_DEFAULT
        kubernetesRuntimeClassName:
          description: Nonempty Kubernetes RuntimeClass name.
          type: string
        nodeDefault:
          description: "Use the node's default container runtime. Must be true and is permitted\n only\
            \ for CPU_DEFAULT or GPU_DEFAULT in CKS placement."
          type: boolean
      required:
      - runtimeClass
    coreweave.sandbox.v1.Sandbox:
      description: Sandbox is a single running (or terminal) compute environment.
      type: object
      properties:
        sandboxId:
          description: Server-assigned unique identifier.
          type: string
          readOnly: true
        spec:
          description: "Desired workload. Required on create and immutable thereafter. It is absent\n\
            \ when v1 projects a sandbox created through v1beta2, which has no v1\n SandboxSpec. It is\
            \ also absent in STATE_PREPARING, and after an image fill\n fails before the spec is stored.\n\
            \ When create used a template, this is the resolved spec from\n that create — never re-read\
            \ from the live template."
          allOf:
          - $ref: '#/components/schemas/coreweave.sandbox.v1.SandboxSpec'
        status:
          description: Observed state.
          allOf:
          - $ref: '#/components/schemas/coreweave.sandbox.v1.SandboxStatus'
          readOnly: true
        sourceTemplateId:
          description: "Template selected at create time, if any. Historical provenance; retained\n even\
            \ if the template is later deleted."
          type: string
          readOnly: true
        sourceTemplateRevision:
          description: Revision of the template applied at create time.
          type: string
          readOnly: true
        displayName:
          description: "Optional, immutable lookup name, unique among active sandboxes in the\n tenant\
            \ organization. Case-sensitive, at most 128 UTF-8 bytes; leading or\n trailing whitespace,\
            \ slashes, colons, control characters, and UUIDs are invalid.\n The name becomes reusable\
            \ once the sandbox reaches a terminal state."
          type: string
        endpointShareToken:
          description: "CreateSandbox, CreateSandboxFromTemplate, and an identical request_id\n replay\
            \ of that call, after HTTPS URLs confirm. Omitted from Get, List,\n status, and from a successful\
            \ create while those URLs are unconfirmed.\n Send as X-Sandbox-Share-Token or ?share_token=;\
            \ both are stripped before\n forwarding."
          type: string
          readOnly: true
        control:
          description: 'Who controls the sandbox''s containers: CONTROL_CONTAINER_ENGINE for a sandbox
            created with it, and CONTROL_PLATFORM for every other sandbox. CONTROL_UNSPECIFIED means no
            controller is specified; successful creates resolve the default to CONTROL_PLATFORM.'
          type: string
          format: enum
          enum:
          - CONTROL_UNSPECIFIED
          - CONTROL_PLATFORM
          - CONTROL_CONTAINER_ENGINE
          readOnly: true
      required:
      - spec
    coreweave.sandbox.v1.SandboxConnection:
      description: "SandboxConnection contains everything except the client private key needed\n to establish\
        \ a sandbox-scoped direct connection."
      type: object
      properties:
        endpointUri:
          description: Stable absolute URI for the logical Runner data-plane endpoint.
          type: string
          readOnly: true
        clientCertificateChainPem:
          description: "PEM certificate chain for the public key in the request CSR. The leaf\n certificate\
            \ is first."
          type: string
          format: bytes
          readOnly: true
        serverCaBundlePem:
          description: "PEM trust bundle for authenticating the endpoint. Empty means the endpoint\n chains\
            \ to roots available from the client's system trust store."
          type: string
          format: bytes
          readOnly: true
        expiresAt:
          description: Time at which the client certificate and established connection expire.
          type: string
          format: date-time
          readOnly: true
        endpointId:
          description: Opaque stable identity of the logical Runner endpoint.
          type: string
          readOnly: true
        transport:
          description: Transport for the issued connection. Successful responses use SANDBOX_DATA_TRANSPORT_DIRECT_MTLS.
            SANDBOX_DATA_TRANSPORT_UNSPECIFIED means no transport is specified and is not emitted for
            a successful connection.
          type: string
          format: enum
          enum:
          - SANDBOX_DATA_TRANSPORT_UNSPECIFIED
          - SANDBOX_DATA_TRANSPORT_DIRECT_MTLS
          readOnly: true
        protocol:
          description: Protocol for the issued connection. Successful responses use SANDBOX_DATA_PROTOCOL_CONNECT_H2_V1.
            SANDBOX_DATA_PROTOCOL_UNSPECIFIED means no protocol is specified and is not emitted for a
            successful connection.
          type: string
          format: enum
          enum:
          - SANDBOX_DATA_PROTOCOL_UNSPECIFIED
          - SANDBOX_DATA_PROTOCOL_CONNECT_H2_V1
          readOnly: true
        grantedPermissions:
          description: Effective permissions encoded in the issued certificate. Successful responses contain
            at least one permission from the intersection of requested and allowed permissions and do
            not contain SANDBOX_DATA_PERMISSION_UNSPECIFIED.
          type: array
          items:
            enum:
            - SANDBOX_DATA_PERMISSION_UNSPECIFIED
            - SANDBOX_DATA_PERMISSION_EXEC
            - SANDBOX_DATA_PERMISSION_STREAM_EXEC
            - SANDBOX_DATA_PERMISSION_STREAM_LOGS
            - SANDBOX_DATA_PERMISSION_WRITE_FILE
            - SANDBOX_DATA_PERMISSION_READ_FILE
            type: string
            format: enum
          readOnly: true
    coreweave.sandbox.v1.SandboxSpec:
      description: "SandboxSpec is the user-declared workload: one or more containers that share\n the\
        \ sandbox's network and volumes. It is the complete, self-contained\n description of the sandbox\
        \ — it may not reference cluster-external objects by\n name (no ConfigMap/Secret refs, block devices,\
        \ or named PVCs); external access\n is only via secret_stores, network_ids, and object_storage_access.\n\
        \n Every sandbox runs under exactly one per-runner Policy, selected by\n placement. The Policy\
        \ resolves as a base layer of defaults/attachments\n (runtime defaults < policy base < this spec)\
        \ and then clamps the resolved\n result against typed constraints; a spec that violates a constraint\
        \ is\n rejected, not silently rewritten."
      type: object
      properties:
        containers:
          description: "The containers that make up the sandbox (at least one). They share the\n sandbox's\
            \ network (reachable over localhost) and any mounted volumes.\n Exactly one container is primary\
            \ (see Container.primary). In a\n CONTROL_CONTAINER_ENGINE sandbox, this lists one container,\
            \ cws-engine,\n with the sandbox's total resources and no image, because the platform\n owns\
            \ the engine image. That spec can't be sent back through\n CreateSandbox."
          type: array
          items:
            $ref: '#/components/schemas/coreweave.sandbox.v1.Container'
        volumes:
          description: "Sandbox-level volumes. Containers mount these by name via\n Container.volume_mounts;\
            \ a volume mounted by more than one container is\n shared between them."
          type: array
          items:
            $ref: '#/components/schemas/coreweave.sandbox.v1.SandboxVolume'
        services:
          description: Services exposed by the sandbox. Set endpoint to request an HTTPS or TLS passthrough
            product endpoint, subject to runner support. A service with an endpoint must use PUBLIC visibility
            and TCP or an unset protocol. Omit endpoint for a plain service port.
          type: array
          items:
            $ref: '#/components/schemas/coreweave.sandbox.v1.Service'
        maxLifetimeSeconds:
          description: "Maximum lifetime before automatic termination. 0 = platform default (NOT\n unbounded).\
            \ Values above the platform maximum (currently 30 days) are\n rejected; the applied value\
            \ is echoed in\n SandboxStatus.effective_max_lifetime_seconds."
          type: integer
          format: int32
        networkIds:
          description: Network membership is not supported. v1 sandbox creation and stored template validation
            reject a non-empty networkIds list. Use network or networkConfigId where supported to configure
            network rules; these fields do not join sandbox networks.
          type: array
          items:
            type: string
        objectStorageAccess:
          description: "Object-storage (S3) access for this sandbox. The minted credential is\n injected\
            \ into every user container."
          allOf:
          - $ref: '#/components/schemas/coreweave.sandbox.v1.ObjectStorageAccess'
        tags:
          description: User-defined tags for organization and List filtering.
          type: array
          items:
            type: string
        runnerIds:
          description: "Restrict scheduling to these operator-assigned runner ids. Valid only\n when mode\
            \ is SANDBOX_MODE_CKS. Entries must be non-blank and unique; at\n most 100 and 64 KiB total\
            \ may be supplied. If none of the named runners is\n currently eligible, CreateSandbox returns\
            \ retryable runner unavailability\n because runner registration and health can change."
          type: array
          items:
            type: string
        network:
          description: Optional write-only network rules for sandbox creation. The platform creates a
            platform-managed NetworkConfig from these rules. Do not also set networkConfigId. Sandbox
            Get and List responses omit this field; use networkConfigId to read the desired NetworkConfig
            instead.
          allOf:
          - $ref: '#/components/schemas/coreweave.sandbox.v1.NetworkOptions'
          writeOnly: true
        annotations:
          description: "Key-value metadata applied to the sandbox. On the Kubernetes backend these\n become\
            \ pod annotations; the policy filters dangerous prefixes and caps the\n count."
          type: object
          additionalProperties:
            type: string
        instanceType:
          description: "PROVISIONAL (subject to change): optionally pin the sandbox to a specific\n node\
            \ instance type, constrained to the policy's allow-list. When unset, the\n platform selects\
            \ an instance from the containers' resource requirements\n (cpu/memory and, for accelerated\
            \ workloads, Gpu)."
          type: string
        mode:
          description: Optionally select the placement candidate set. Unset defaults to SANDBOX_MODE_SERVERLESS.
            Set SANDBOX_MODE_CKS explicitly to use the caller's own-cluster runners; runner_ids requires
            that explicit CKS mode. SANDBOX_MODE_UNSPECIFIED has the same default as omission.
          type: string
          format: enum
          enum:
          - SANDBOX_MODE_UNSPECIFIED
          - SANDBOX_MODE_SERVERLESS
          - SANDBOX_MODE_CKS
        runtimeClass:
          description: "Optionally pin the sandbox's runtime class (e.g. \"kata-qemu\", \"gvisor\").\n\
            \ Unset = the policy's default runtime classes\n (SecurityConstraints.default_cpu_runtime_class\
            \ / default_gpu_runtime_class,\n selected by GPU presence), falling back to the runner's own\
            \ selection\n when the policy sets no default (a profile-level isolation override where\n\
            \ one is bound, then the runner's configured CPU/GPU pair). When set, the value is\n used\
            \ verbatim — the platform never substitutes a variant (a GPU sandbox\n must pin a GPU-capable\
            \ class itself) — and must be listed by the runner\n policy's allowed_runtime_classes (an\
            \ empty list permits no pin). The\n resolved class is validated against the policy at create\
            \ and against the\n placed runner's cluster at placement; a pin that fails either is\n rejected,\
            \ never rewritten. The class the runner actually applied is\n reported in SandboxStatus.effective_runtime_class.\
            \ NOTE: a pin requires\n the allow-list even when it names the policy's own default — copying\
            \ an\n observed effective_runtime_class into a new spec's pin (a clone flow)\n fails under\
            \ a policy that sets defaults without an allow-list; clone\n flows should leave this unset\
            \ and let the default apply. Mutually\n exclusive with runtime_class_selection. A runner whose\
            \ policy defines\n SecurityConstraints.runtime_class_mappings accepts no concrete pin."
          type: string
        networkConfigId:
          description: Immutable reference to a NetworkConfig. On create, set an unused caller-created
            configuration ID, or omit it to create a platform-managed configuration from inline network
            rules or policy defaults. Do not send both networkConfigId and network. Get and List project
            the ID from the binding. Copy NetworkConfig.spec into a new configuration to clone rules;
            copying this ID reuses the same resource.
          type: string
        runtimeClassSelection:
          description: "Optionally select a portable runtime class. Each runner policy's\n SecurityConstraints.runtime_class_mappings\
            \ binds the classes it offers to\n concrete runtimes; only runners whose policy maps the selected\
            \ class are\n eligible. UNSPECIFIED selects RUNTIME_CLASS_GPU_DEFAULT when any container\n\
            \ requests GPUs and RUNTIME_CLASS_CPU_DEFAULT otherwise, on runners whose\n policy defines\
            \ mappings; other runners keep the runtime_class behavior. CPU\n classes require zero GPUs\
            \ and GPU classes require GPUs (INVALID_ARGUMENT\n otherwise). A recognized class that no\
            \ runner policy in the requested\n placement scope offers, or that is not yet available, fails\
            \ with\n FAILED_PRECONDITION (reason CWSANDBOX_RUNTIME_CLASS_UNAVAILABLE); when\n runners\
            \ that offer it are busy, the create fails with a retryable error\n instead. Mutually exclusive\
            \ with runtime_class. The concrete runtime the\n runner applied is reported in SandboxStatus.effective_runtime_class."
          type: string
          format: enum
          enum:
          - RUNTIME_CLASS_UNSPECIFIED
          - RUNTIME_CLASS_CPU_DEFAULT
          - RUNTIME_CLASS_CPU_NESTED_VIRT
          - RUNTIME_CLASS_CPU_SNAPSHOT_RESTORE
          - RUNTIME_CLASS_GPU_DEFAULT
      required:
      - containers
    coreweave.sandbox.v1.SandboxStatus:
      description: SandboxStatus is the observed state of a sandbox.
      type: object
      properties:
        state:
          description: Overall sandbox state, derived from the primary container. In a CONTROL_CONTAINER_ENGINE
            sandbox, that is cws-engine (see Control). STATE_UNSPECIFIED means no state is specified.
          type: string
          format: enum
          enum:
          - STATE_UNSPECIFIED
          - STATE_CREATING
          - STATE_RUNNING
          - STATE_COMPLETED
          - STATE_FAILED
          - STATE_TERMINATING
          - STATE_TERMINATED
          - STATE_PENDING
          - STATE_PAUSED
          - STATE_PREPARING
          readOnly: true
        stateReason:
          description: Human-readable reason for the current state (esp. terminal states).
          type: string
          readOnly: true
        createTime:
          type: string
          format: date-time
          readOnly: true
        startTime:
          type: string
          format: date-time
          readOnly: true
        endTime:
          type: string
          format: date-time
          readOnly: true
        services:
          description: "Per-service status, including nested EndpointStatus when product endpoints\n are\
            \ filled on a successful Create response."
          type: array
          items:
            $ref: '#/components/schemas/coreweave.sandbox.v1.ServiceStatus'
          readOnly: true
        resourceUsage:
          description: Real-time resource usage, summed across containers.
          allOf:
          - $ref: '#/components/schemas/coreweave.sandbox.v1.ResourceUsage'
          readOnly: true
        exitCode:
          description: "Exit code of the primary container. Present only when the platform observed\n\
            \ it; zero is a valid observed exit code."
          type: integer
          format: int32
          readOnly: true
        effectiveResources:
          description: "Resolved guaranteed compute allocation (summed across containers) after\n platform\
            \ defaults were applied. For burstable allocations, see\n effective_resource_requirements."
          allOf:
          - $ref: '#/components/schemas/coreweave.sandbox.v1.Resources'
          readOnly: true
        effectiveMaxLifetimeSeconds:
          description: "Applied max lifetime after platform defaulting. Over-max create requests\n are\
            \ rejected and never appear here."
          type: integer
          format: int32
          readOnly: true
        containerStatuses:
          description: Per-container observed state.
          type: array
          items:
            $ref: '#/components/schemas/coreweave.sandbox.v1.ContainerStatus'
          readOnly: true
        runnerId:
          description: "Placement: the runner the sandbox was scheduled onto and its runner group.\n Every\
            \ sandbox — managed pool or CKS — lands on a runner."
          type: string
          readOnly: true
        runnerGroupId:
          type: string
          readOnly: true
        effectiveIngress:
          description: "Resolved ingress rules in effect (the declared rules, or the policy\n default\
            \ when the spec declared none)."
          type: array
          items:
            $ref: '#/components/schemas/coreweave.sandbox.v1.IngressRule'
          readOnly: true
        effectiveEgress:
          description: "Resolved egress rules in effect (the declared rules, or the policy default\n when\
            \ the spec declared none)."
          type: array
          items:
            $ref: '#/components/schemas/coreweave.sandbox.v1.EgressRule'
          readOnly: true
        effectiveResourceRequirements:
          description: "Resolved compute allocation (requests + limits, summed across containers)\n after\
            \ platform defaults were applied."
          allOf:
          - $ref: '#/components/schemas/coreweave.sandbox.v1.ResourceRequirements'
          readOnly: true
        attachedVolumeIds:
          description: Registered Volumes (volume.proto) attached to this sandbox, by volume_id.
          type: array
          items:
            type: string
          readOnly: true
        effectiveRuntimeClass:
          description: "The runtime class assigned to the sandbox, as reported by the runner\n that placed\
            \ it: the spec's pin, the policy's CPU/GPU default, or the\n runner's own configured selection.\
            \ The literal \"<node-default>\" means the\n runner affirmatively assigned NO RuntimeClass\
            \ — the pod runs the node's\n default container runtime, which Kubernetes does not name (the\
            \ value is\n intentionally not a valid RuntimeClass name, so it can never collide with\n a\
            \ real class or be pinned). Empty only when the assignment is unknown:\n the sandbox never\
            \ completed placement, or its runner predates\n runtime-class reporting — then this carries\
            \ the create-time resolution,\n which may itself be empty."
          type: string
          readOnly: true
        effectiveDnsEgress:
          description: "Effective outbound DNS traffic mode after policy resolution, governing\n UDP/TCP\
            \ destination port 53. UNSPECIFIED when unknown. This is separate\n from the https_hostname\
            \ destination rules in effective_egress."
          type: string
          format: enum
          enum:
          - DNS_EGRESS_MODE_UNSPECIFIED
          - DNS_EGRESS_MODE_ALLOW
          - DNS_EGRESS_MODE_DENY
          readOnly: true
    coreweave.sandbox.v1.SandboxTemplate:
      description: "SandboxTemplate is an organization-scoped partial workload template.\n PartialSandboxSpec\
        \ / PartialContainer are defined in sandbox.proto."
      type: object
      properties:
        sandboxTemplateId:
          description: Server-assigned unique identifier.
          type: string
          readOnly: true
        displayName:
          description: "Human-readable name, unique among active (non-deleted) templates in the\n tenant\
            \ organization. Trimmed; 1–128 Unicode characters; must not be\n empty. Prefer names that\
            \ are not UUID-shaped so they do not collide with\n id-first Get resolution."
          type: string
        spec:
          description: "Partial workload specification. May omit fields that\n CreateSandboxFromTemplate\
            \ supplies via overrides (for example containers).\n Must not carry policy selectors. Server-enforced\
            \ size ceiling: 1 MiB."
          allOf:
          - $ref: '#/components/schemas/coreweave.sandbox.v1.PartialSandboxSpec'
        revision:
          description: "Monotonic revision; incremented on each successful update.\n CreateSandboxFromTemplate\
            \ records the selected revision on the sandbox as\n source_template_revision."
          type: string
          readOnly: true
        createTime:
          type: string
          format: date-time
          readOnly: true
        updateTime:
          type: string
          format: date-time
          readOnly: true
        deleteTime:
          description: Set when soft-deleted; unset for active templates.
          type: string
          format: date-time
          readOnly: true
        createUserId:
          description: User id of the creator.
          type: string
          readOnly: true
        deleted:
          description: True when delete_time is set. Convenience for admin filtering.
          type: boolean
          readOnly: true
        attachments:
          description: "Optional admin runtime attachments applied when creating a sandbox from\n this\
            \ template. Same opaque fragment shape as Policy.base (for example, a\n PodSpec fragment on\
            \ a Kubernetes runner). Writable by sandbox_admin only.\n When set, CreateSandboxFromTemplate\
            \ requires SANDBOX_MODE_CKS (serverless\n is rejected; unset mode is treated as CKS). Not\
            \ part of SandboxSpec;\n CreateSandbox and create overrides cannot supply or change them."
          type: object
        requiresCks:
          description: "True when attachments are set. Indicates CreateSandboxFromTemplate for\n this\
            \ template requires CKS placement."
          type: boolean
          readOnly: true
      required:
      - displayName
    coreweave.sandbox.v1.SandboxVolume:
      description: "SandboxVolume is a sandbox-level volume declaration: either a scratch\n (or snapshot-restored)\
        \ volume that lives and dies with the sandbox, or a\n live mount of a registered Volume (volume.proto).\
        \ The two are a oneof —\n mixing them is unrepresentable, and only the scratch arm participates\
        \ in\n snapshots. Containers mount either kind via VolumeMount; a volume mounted\n by more than\
        \ one container is shared between them."
      type: object
      properties:
        name:
          description: "Unique name within the sandbox; referenced by VolumeMount.volume and used to\n\
            \ target snapshots."
          type: string
        scratch:
          description: A sandbox-lifetime scratch volume.
          allOf:
          - $ref: '#/components/schemas/coreweave.sandbox.v1.ScratchVolume'
        volumeId:
          description: "A registered Volume (VolumeService) mounted live: writes go against the\n shared\
            \ backing store and are visible to every mounter. Never\n snapshotted. A CLUSTER_LOCAL Volume\
            \ (pvc source) pins scheduling to\n its owning runner, so declaring one with mode = SANDBOX_MODE_SERVERLESS\n\
            \ is INVALID_ARGUMENT — the managed pool can never satisfy the pin."
          type: string
      required:
      - name
    coreweave.sandbox.v1.ScratchVolume:
      description: "ScratchVolume configures a sandbox-lifetime scratch volume, optionally\n restored\
        \ from a FileSystemSnapshot."
      type: object
      properties:
        size:
          description: "Size with a binary/decimal suffix, e.g. \"10Gi\". MEMORY-medium volumes may\n\
            \ instead declare a percentage of the sandbox's total resolved memory\n request, e.g. \"50%\"\
            \ (integer 1-100): the platform resolves it to an\n absolute size at create time against the\
            \ post-defaults request sum, and\n the resolved absolute size is what is enforced and echoed.\
            \ MEMORY-medium\n volumes MUST declare a size (absolute or percent) — an unbounded\n RAM-backed\
            \ volume is rejected; percent form is invalid for DISK."
          type: string
        medium:
          description: Backing medium. Defaults to disk; MEMORY is RAM-backed (tmpfs) and counts against
            the mounting container's memory (e.g. BuildKit's /var/lib/buildkit) and against the policy's
            memory ceiling (resolved sizes sum with container memory requests). Omit this field for disk-backed
            storage; STORAGE_MEDIUM_UNSPECIFIED also uses STORAGE_MEDIUM_DISK.
          type: string
          format: enum
          enum:
          - STORAGE_MEDIUM_UNSPECIFIED
          - STORAGE_MEDIUM_DISK
          - STORAGE_MEDIUM_MEMORY
        restoreFromSnapshotId:
          description: "If set, the volume is restored from this snapshot; otherwise it starts\n empty."
          type: string
    coreweave.sandbox.v1.SecretMapping:
      description: "SecretMapping maps one secret (optionally a sub-field of a structured secret)\n in\
        \ the store to an environment variable."
      type: object
      properties:
        path:
          description: Provider-specific secret identifier (a key or path within the store).
          type: string
        field:
          description: Optional sub-field within a structured secret; omit for a scalar secret.
          type: string
        envVar:
          description: Target environment variable.
          type: string
      required:
      - path
      - envVar
    coreweave.sandbox.v1.SecretSource:
      description: "SecretSource addresses one provider secret value without specifying any\n delivery\
        \ target such as an environment variable."
      type: object
      properties:
        storeName:
          description: "Name of a secret store, matching SecretStoreReference.store_name. W&B-\n authenticated\
            \ callers may use the built-in identity-backed store name\n \"wandb\"; all other names are\
            \ resolved from configured SecretStores."
          type: string
        path:
          description: Provider-specific secret identifier, matching SecretMapping.path.
          type: string
        field:
          description: Optional sub-field within a structured secret, matching SecretMapping.field.
          type: string
      required:
      - storeName
      - path
    coreweave.sandbox.v1.SecretStore:
      description: "SecretStore is an org-level secret-store registration. Sandboxes reference it\n by\
        \ name via SecretStoreReference.store_name."
      type: object
      properties:
        name:
          description: "Caller-chosen identifier, unique within the organization. Must match\n ^[a-z][a-z0-9-]{2,62}$.\
            \ Immutable after creation."
          type: string
        providerType:
          description: 'Provider type. Specify a concrete provider on create, full replacement, or an
            update that selects providerType. SECRET_STORE_PROVIDER_TYPE_UNSPECIFIED is invalid in these
            writes. An update that excludes this field preserves the existing provider. Provider type
            is immutable: full replacement or an update selecting providerType must retain the existing
            concrete provider.'
          type: string
          format: enum
          enum:
          - SECRET_STORE_PROVIDER_TYPE_UNSPECIFIED
          - SECRET_STORE_PROVIDER_TYPE_WANDB
        wandb:
          $ref: '#/components/schemas/coreweave.sandbox.v1.WandBStoreConfig'
        createTime:
          type: string
          format: date-time
          readOnly: true
        updateTime:
          type: string
          format: date-time
          readOnly: true
    coreweave.sandbox.v1.SecretStoreReference:
      description: "SecretStoreReference resolves secrets from a configured external store into\n environment\
        \ variables."
      type: object
      properties:
        storeName:
          description: "Name of the secret store. W&B-authenticated callers may use the built-in\n identity-backed\
            \ store name \"wandb\" without creating a SecretStore row; all\n other names are resolved\
            \ from configured SecretStores."
          type: string
        secrets:
          type: array
          items:
            $ref: '#/components/schemas/coreweave.sandbox.v1.SecretMapping'
      required:
      - storeName
      - secrets
    coreweave.sandbox.v1.SecurityConstraints:
      description: "SecurityConstraints clamps in-guest container privilege and bounds the\n sandbox's\
        \ isolation-boundary selection. Host-reaching settings default to\n forbidden and are only ever\
        \ granted on a runner whose isolation contains\n them."
      type: object
      properties:
        allowPrivileged:
          description: Permit SecurityContext.privileged.
          type: boolean
        allowedCapabilities:
          description: Linux capabilities a container may add (empty = none beyond the default set).
          type: array
          items:
            type: string
        allowedSeccompProfiles:
          description: Permitted seccomp profiles (e.g. "RuntimeDefault", "Unconfined").
          type: array
          items:
            type: string
        allowedRuntimeClasses:
          description: "Allowed SandboxSpec.runtime_class values. Like the capability and seccomp\n lists\
            \ — and unlike the instance-type allow-list — an EMPTY (or absent)\n list permits NO pin:\
            \ runtime-class selection is enabled by explicitly\n listing classes. Runtime class selects\
            \ the isolation boundary itself, so\n it is fail-closed even under an otherwise-unset security\
            \ group. The\n managed serverless pool lists only its Kata classes, keeping VM isolation\n\
            \ mandatory there. Defaults below are policy-authored posture and apply\n regardless of this\
            \ list."
          type: array
          items:
            type: string
        defaultCpuRuntimeClass:
          description: "Default runtime class applied when SandboxSpec.runtime_class is unset and\n the\
            \ sandbox requests no GPUs. Must fit allowed_runtime_classes when that\n list is non-empty\
            \ (validated when the policy is written). Unset = the\n runner's configured runtime-class\
            \ pair applies."
          type: string
        defaultGpuRuntimeClass:
          description: "Default runtime class applied when SandboxSpec.runtime_class is unset and\n the\
            \ sandbox requests GPUs. Same containment and fallback rules as the CPU\n default."
          type: string
        runtimeClassMappings:
          description: "Bindings from portable runtime classes to concrete runtimes. A non-empty\n list\
            \ switches the runner to runtime class mappings: a mapping permits its\n class for both SandboxSpec.runtime_class_selection\
            \ and automatic CPU/GPU\n default selection, a class without a mapping is unavailable on this\n\
            \ runner, and SandboxSpec.runtime_class pins are rejected. Omitting a\n default class disables\
            \ automatic selection for that resource family.\n Mutually exclusive with allowed_runtime_classes,\
            \ default_cpu_runtime_class,\n and default_gpu_runtime_class. Each class appears at most once.\
            \ A\n node_default target is permitted only for the CPU and GPU defaults, and\n only serves\
            \ SANDBOX_MODE_CKS placement outside the shared serverless pool."
          type: array
          items:
            $ref: '#/components/schemas/coreweave.sandbox.v1.RuntimeClassMapping'
    coreweave.sandbox.v1.SecurityContext:
      description: SecurityContext sets in-guest privilege for a container. These settings are contained
        within the sandbox's isolation boundary and are subject to the runner policy's security constraints.
        This resource does not configure host namespaces or hostPath volumes. Host-reaching settings are
        also rejected in v1 policy base attachments.
      type: object
      properties:
        runAsUser:
          description: "UID/GID to run the entrypoint as. Unset = the image's user. uint32 covers\n the\
            \ full Linux id space and renders as a JSON number for REST consumers."
          type: integer
          format: uint32
        runAsGroup:
          type: integer
          format: uint32
        privileged:
          description: "Run the container in privileged mode, within the sandbox's isolation\n boundary.\
            \ Policy-gated."
          type: boolean
        allowPrivilegeEscalation:
          description: Allow a process to gain more privileges than its parent.
          type: boolean
        readOnlyRootFilesystem:
          description: Mount the container's root filesystem read-only.
          type: boolean
        capabilitiesAdd:
          description: Linux capabilities to add and to drop (e.g. "NET_ADMIN", "SYS_PTRACE").
          type: array
          items:
            type: string
        capabilitiesDrop:
          type: array
          items:
            type: string
        seccompProfile:
          description: 'Seccomp profile: "RuntimeDefault" or "Unconfined".'
          type: string
    coreweave.sandbox.v1.SelectorBlock:
      description: "SelectorBlock selects cluster workloads by label, mirroring Kubernetes\n NetworkPolicyPeer\
        \ semantics. Matching is matchLabels-only (every listed\n label must be present with the exact\
        \ value); expression matching is not\n part of the contract. Adding a label narrows the match,\
        \ so containment is\n per dimension: a policy selector entitlement covers a declared selector\n\
        \ when the declared pod_labels carry every entitled pod label (and then\n some) AND the namespace\
        \ dimensions agree in form — both absent (own\n namespace), or both present with the declared\
        \ namespace_labels carrying\n every entitled namespace label. An own-namespace entitlement never\
        \ covers\n a cross-namespace declaration, and vice versa: the sandbox's own namespace\n is not\
        \ statically comparable to any labeled namespace set."
      type: object
      properties:
        podLabels:
          description: "Labels the destination pods must carry. At least one is required — an\n empty\
            \ pod selector would select everything, which is `any`'s job."
          type: object
          additionalProperties:
            type: string
        namespaceLabels:
          description: "Labels the destination pods' namespaces must carry. Absent = the\n sandbox's own\
            \ namespace ONLY (Kubernetes NetworkPolicyPeer behavior);\n reaching workloads in other namespaces\
            \ always requires namespace labels.\n There is deliberately no all-namespaces form."
          type: object
          additionalProperties:
            type: string
      required:
      - podLabels
    coreweave.sandbox.v1.Service:
      description: "Service declares a port the workload listens on, its reachability intent,\n and an\
        \ optional product endpoint opt-in."
      type: object
      properties:
        port:
          type: integer
          format: int32
        name:
          type: string
        protocol:
          description: L4 for K8s Service/Pod/NetworkPolicy. Unset = TCP. Not endpoint kind. Omit this
            field for TCP; SERVICE_PROTOCOL_UNSPECIFIED also uses SERVICE_PROTOCOL_TCP.
          type: string
          format: enum
          enum:
          - SERVICE_PROTOCOL_UNSPECIFIED
          - SERVICE_PROTOCOL_TCP
          - SERVICE_PROTOCOL_UDP
          - SERVICE_PROTOCOL_SCTP
        visibility:
          description: "Who may reach this port. Declared intent only — the platform chooses the\n mechanism.\
            \ Defaults to VISIBILITY_UNSPECIFIED (not reachable outside the\n sandbox)."
          type: string
          format: enum
          enum:
          - VISIBILITY_UNSPECIFIED
          - VISIBILITY_PUBLIC
          - VISIBILITY_PRIVATE
          - VISIBILITY_CUSTOM
        endpoint:
          description: Optional HTTPS or TLS passthrough product endpoint, subject to runner support.
            Requires PUBLIC visibility and TCP or an unset protocol. Omit for a plain service port.
          allOf:
          - $ref: '#/components/schemas/coreweave.sandbox.v1.EndpointSpec'
      required:
      - port
    coreweave.sandbox.v1.ServiceStatus:
      description: "ServiceStatus echoes a create Service row. Nested endpoint is unset when\n create\
        \ had no product endpoint; url stays empty until filled."
      type: object
      properties:
        port:
          type: integer
          format: int32
          readOnly: true
        name:
          type: string
          readOnly: true
        protocol:
          description: Declared service protocol. SERVICE_PROTOCOL_UNSPECIFIED means TCP; the response
            can retain the unspecified value instead of normalizing it to SERVICE_PROTOCOL_TCP.
          type: string
          format: enum
          enum:
          - SERVICE_PROTOCOL_UNSPECIFIED
          - SERVICE_PROTOCOL_TCP
          - SERVICE_PROTOCOL_UDP
          - SERVICE_PROTOCOL_SCTP
          readOnly: true
        visibility:
          description: Declared service visibility. VISIBILITY_UNSPECIFIED means the port is not reachable
            from outside the sandbox.
          type: string
          format: enum
          enum:
          - VISIBILITY_UNSPECIFIED
          - VISIBILITY_PUBLIC
          - VISIBILITY_PRIVATE
          - VISIBILITY_CUSTOM
          readOnly: true
        endpoint:
          allOf:
          - $ref: '#/components/schemas/coreweave.sandbox.v1.EndpointStatus'
          readOnly: true
        url:
          description: "Generic L4 connection target for this service (tcp/udp/sctp). Empty for\n VISIBILITY_UNSPECIFIED,\
            \ before the observed address is ready, and whenever\n the sandbox is not RUNNING. This is\
            \ separate from product endpoint status."
          type: string
          readOnly: true
    coreweave.sandbox.v1.SourceIpAllowlist:
      description: SourceIpAllowlist is a bounded set of IPv4 and IPv6 network prefixes.
      type: object
      properties:
        cidrs:
          description: "IPv4 or IPv6 CIDR prefixes. Prefixes are normalized when written. At most\n 256\
            \ entries and 16 KiB of source text are accepted. Use 0.0.0.0/0 or\n ::/0 to explicitly allow\
            \ every address in that family."
          type: array
          items:
            type: string
    coreweave.sandbox.v1.StoredSandboxLogEntry:
      description: StoredSandboxLogEntry is one stored log line.
      type: object
      properties:
        eventId:
          description: "Stable identity of the line. A line collected more than once is\n returned once."
          type: string
          readOnly: true
        data:
          description: The stored body.
          type: string
          format: bytes
          readOnly: true
        timestamp:
          description: When the container wrote the line.
          type: string
          format: date-time
          readOnly: true
        container:
          description: The container that wrote the line.
          type: string
          readOnly: true
        stream:
          type: string
          format: enum
          enum:
          - SANDBOX_LOG_STREAM_UNSPECIFIED
          - SANDBOX_LOG_STREAM_STDOUT
          - SANDBOX_LOG_STREAM_STDERR
          readOnly: true
    coreweave.sandbox.v1.StreamLogsRequest:
      type: object
      properties:
        sandboxId:
          type: string
        follow:
          description: Keep the stream open and follow new output.
          type: boolean
        tailLines:
          description: Start from the last N lines.
          type: integer
          format: int32
        sinceTime:
          description: Start from this time.
          type: string
          format: date-time
        container:
          description: "Target container name. Empty = the primary. Unknown names and\n platform sidecar\
            \ names are INVALID_ARGUMENT (CWSANDBOX_INVALID_REQUEST).\n In a CONTROL_CONTAINER_ENGINE\
            \ sandbox, cws-engine is the only container\n and the primary."
          type: string
        timestamps:
          description: "Prefix each emitted line with an ISO 8601 timestamp. A resume request must\n leave\
            \ this false because it inherits the original stream's formatting."
          type: boolean
        resumeLogSessionId:
          description: "Resume an interrupted follow stream: reattach to this log session and replay\n\
            \ from resume_log_offset onward. Requires follow=true; mutually exclusive\n with non-default\
            \ tail_lines, since_time, and timestamps. Resumed output\n retains the original stream's timestamp\
            \ formatting."
          type: string
        resumeLogOffset:
          description: "Byte offset to resume from within the session's replay window. If it is\n below\
            \ the oldest retained byte, the server emits a terminal LogEntry with\n error.code = \"REPLAY_GAP\"\
            ."
          type: string
      required:
      - sandboxId
    coreweave.sandbox.v1.Volume:
      description: Volume is org-registered shared storage, mountable by sandboxes.
      type: object
      properties:
        volumeId:
          description: "Caller-chosen identifier, unique within the organization, immutable.\n Pattern:\
            \ ^[a-z][a-z0-9-]{2,62}$"
          type: string
        spec:
          $ref: '#/components/schemas/coreweave.sandbox.v1.VolumeSpec'
        status:
          allOf:
          - $ref: '#/components/schemas/coreweave.sandbox.v1.VolumeStatus'
          readOnly: true
      required:
      - spec
    coreweave.sandbox.v1.VolumeConstraints:
      description: VolumeConstraints clamps sandbox volumes.
      type: object
      properties:
        allowedMedia:
          description: Permitted storage media. An empty list permits any medium; a non-empty list accepts
            only STORAGE_MEDIUM_DISK and STORAGE_MEDIUM_MEMORY. STORAGE_MEDIUM_UNSPECIFIED is invalid
            here and is not a wildcard. Excluding STORAGE_MEDIUM_MEMORY from a non-empty list forbids
            RAM-backed volumes.
          type: array
          items:
            enum:
            - STORAGE_MEDIUM_UNSPECIFIED
            - STORAGE_MEDIUM_DISK
            - STORAGE_MEDIUM_MEMORY
            type: string
            format: enum
        maxSize:
          description: Maximum size per volume (e.g. "100Gi").
          type: string
    coreweave.sandbox.v1.VolumeMount:
      description: VolumeMount mounts a SandboxVolume into a container.
      type: object
      properties:
        volume:
          type: string
        mountPath:
          type: string
        readOnly:
          type: boolean
        subPath:
          description: "Relative path inside the volume to mount instead of its root. For a\n registered\
            \ Volume the effective path is the volume source's sub_path\n joined with this value. Must\
            \ be relative and canonical (no \".\" / \"..\")."
          type: string
      required:
      - volume
      - mountPath
    coreweave.sandbox.v1.VolumeSpec:
      type: object
      properties:
        pvc:
          $ref: '#/components/schemas/coreweave.sandbox.v1.PvcVolumeSource'
        readOnly:
          description: "Volume-level read-only floor: when true, every mount of this Volume is\n read-only.\
            \ A mount may tighten (read_only=true) but never loosen."
          type: boolean
        description:
          description: Human description; the only mutable field.
          type: string
    coreweave.sandbox.v1.VolumeStatus:
      type: object
      properties:
        state:
          description: Reported lifecycle state. VOLUME_STATE_UNSPECIFIED means no recognized lifecycle
            state is reported.
          type: string
          format: enum
          enum:
          - VOLUME_STATE_UNSPECIFIED
          - VOLUME_STATE_VALIDATING
          - VOLUME_STATE_READY
          - VOLUME_STATE_ERROR
          - VOLUME_STATE_DELETING
          readOnly: true
        stateReason:
          description: Customer-actionable detail for ERROR/VALIDATING/DELETING.
          type: string
          readOnly: true
        locality:
          description: Server-derived placement class. PVC-backed volumes report VOLUME_LOCALITY_CLUSTER_LOCAL.
            VOLUME_LOCALITY_UNSPECIFIED means the source has no recognized locality. No supported source
            produces VOLUME_LOCALITY_GLOBAL.
          type: string
          format: enum
          enum:
          - VOLUME_LOCALITY_UNSPECIFIED
          - VOLUME_LOCALITY_CLUSTER_LOCAL
          - VOLUME_LOCALITY_GLOBAL
          readOnly: true
        createTime:
          type: string
          format: date-time
          readOnly: true
        updateTime:
          type: string
          format: date-time
          readOnly: true
        lastValidatedTime:
          type: string
          format: date-time
          readOnly: true
        accessModes:
          description: Observed from the claim (pvc source), e.g. ["ReadWriteMany"].
          type: array
          items:
            type: string
          readOnly: true
        capacity:
          description: Observed capacity as a Kubernetes quantity string, e.g. "100Gi".
          type: string
          readOnly: true
        attachedSandboxCount:
          description: Non-terminal sandboxes currently attached.
          type: integer
          format: int32
          readOnly: true
    coreweave.sandbox.v1.WandBStoreConfig:
      description: WandBStoreConfig configures a Weights & Biases secret store.
      type: object
      properties:
        apiUrl:
          description: Base URL for the W&B API (e.g. "https://api.wandb.ai").
          type: string
        team:
          description: Optional W&B team/entity scope.
          type: string
    coreweave.sandbox.v1.WriteFileRequest:
      type: object
      properties:
        sandboxId:
          type: string
        path:
          type: string
        content:
          format: bytes
          type: string
        container:
          description: "Target container name. Empty = the primary. Unknown names and\n platform sidecar\
            \ names are INVALID_ARGUMENT (CWSANDBOX_INVALID_REQUEST).\n In a CONTROL_CONTAINER_ENGINE\
            \ sandbox, cws-engine is the only container\n and the primary."
          type: string
      required:
      - sandboxId
      - path
    coreweave.sandbox.v1.WriteFileResponse:
      type: object
      properties: {}
    coreweave.sandbox.v1beta2.AddFileSandboxRequest:
      description: AddFileSandboxRequest writes (or overwrites) a file inside the sandbox filesystem.
      type: object
      properties:
        sandboxId:
          type: string
        fileContents:
          description: File contents to write. An empty value is valid and creates a zero-byte file.
          type: string
          format: bytes
        filepath:
          type: string
        maxTimeoutSeconds:
          type: integer
          format: int32
      required:
      - sandboxId
      - filepath
    coreweave.sandbox.v1beta2.AddFileSandboxResponse:
      description: AddFileSandboxResponse indicates success or failure.
      type: object
      properties:
        success:
          type: boolean
        errorMessage:
          type: string
    coreweave.sandbox.v1beta2.ApplyAvailableUpdateRequest:
      description: "ApplyAvailableUpdateRequest triggers an immediate update to the latest version\n on\
        \ the runner's release channel. The customer does not specify a version —\n Sandman resolves it\
        \ from the channel."
      type: object
      properties:
        id:
          description: "Runner DB ID (UUID) or runner_id. When the input parses as a UUID, the\n UUID\
            \ lookup is attempted first; on no-match it falls back to runner_id\n resolution."
          type: string
      required:
      - id
    coreweave.sandbox.v1beta2.AvailableRunner:
      description: "AvailableRunner is a user-facing view of a runner. Sensitive fields like\n cluster_name\
        \ and namespace are omitted. Resource availability is only\n populated for runners owned by the\
        \ caller's organization."
      type: object
      properties:
        runnerId:
          type: string
        runnerGroupId:
          type: string
        tags:
          type: array
          items:
            type: string
        healthy:
          type: boolean
        capabilities:
          $ref: '#/components/schemas/coreweave.sandbox.v1beta2.RunnerCapabilitySummary'
        resources:
          $ref: '#/components/schemas/coreweave.sandbox.v1beta2.RunnerResourceSummary'
        profileNames:
          type: array
          items:
            type: string
        connectedAt:
          type: string
          format: date-time
        isShared:
          type: boolean
    coreweave.sandbox.v1beta2.CertificateRequest:
      description: CertificateRequest contains CSR parameters
      type: object
      properties:
        ttl:
          description: Certificate validity duration (optional, defaults to 8760h = 1 year)
          type: string
    coreweave.sandbox.v1beta2.CreateFileSystemSnapshotRequest:
      description: "CreateFileSystemSnapshotRequest creates an FSS from a running sandbox without\n stopping\
        \ the sandbox."
      type: object
      properties:
        sandboxId:
          type: string
        idempotencyKey:
          type: string
        waitForReady:
          type: boolean
        maxTimeoutSeconds:
          type: integer
          format: int32
      required:
      - sandboxId
    coreweave.sandbox.v1beta2.CreateFileSystemSnapshotResponse:
      description: "CreateFileSystemSnapshotResponse indicates success or failure of a mid-life\n FSS\
        \ request."
      type: object
      properties:
        success:
          type: boolean
        errorMessage:
          type: string
        fileSystemSnapshotId:
          type: string
    coreweave.sandbox.v1beta2.CreateManagedRunnerRequest:
      type: object
      properties:
        runnerId:
          description: Client-assigned runner ID (must be unique within org).
          type: string
        runner:
          description: "The runner to create. Required fields on runner.identity: zone, and at\n least\
            \ one of cluster_id or cluster_name. If managed_spec.release_channel\n is not set, it defaults\
            \ to RELEASE_CHANNEL_STABLE."
          allOf:
          - $ref: '#/components/schemas/coreweave.sandbox.v1beta2.Runner'
      required:
      - runnerId
      - runner
    coreweave.sandbox.v1beta2.CreateProfileTemplateRequest:
      type: object
      properties:
        profileTemplate:
          description: 'The profile template to create. Required fields: display_name, spec.'
          allOf:
          - $ref: '#/components/schemas/coreweave.sandbox.v1beta2.ProfileTemplate'
      required:
      - profileTemplate
    coreweave.sandbox.v1beta2.CreateRunnerJoinTokenRequest:
      description: CreateRunnerJoinTokenRequest creates a new join token for runner registration
      type: object
      properties:
        runnerId:
          description: Runner ID to assign (required, must be unique)
          type: string
        runnerGroupId:
          description: Runner group for scheduling affinity (optional, defaults to "default")
          type: string
        ttlSeconds:
          description: Token TTL in seconds (optional, defaults to 86400 = 24 hours)
          type: integer
          format: int32
        description:
          description: Human-readable description
          type: string
        labels:
          description: Optional labels for organizing tokens
          type: object
          additionalProperties:
            type: string
      required:
      - runnerId
    coreweave.sandbox.v1beta2.CreateRunnerJoinTokenResponse:
      description: CreateRunnerJoinTokenResponse returns the generated join token
      type: object
      properties:
        token:
          description: Join token (secret, single-use)
          type: string
        tokenId:
          description: Token ID for tracking
          type: string
        runnerId:
          description: Runner ID assigned
          type: string
        runnerGroupId:
          description: Runner group ID
          type: string
        expiresAt:
          description: Token expiration time
          type: string
          format: date-time
        organizationId:
          description: Organization ID (from authentication)
          type: string
    coreweave.sandbox.v1beta2.CreateSecretStoreRequest:
      type: object
      properties:
        name:
          description: Store name, unique within the organization.
          type: string
        providerType:
          description: Provider type.
          type: string
          format: enum
          enum:
          - SECRET_STORE_PROVIDER_TYPE_UNSPECIFIED
          - SECRET_STORE_PROVIDER_TYPE_WANDB
        wandb:
          $ref: '#/components/schemas/coreweave.sandbox.v1beta2.WandBStoreConfig'
      required:
      - name
      - providerType
    coreweave.sandbox.v1beta2.CreateSecretStoreResponse:
      type: object
      properties:
        secretStore:
          $ref: '#/components/schemas/coreweave.sandbox.v1beta2.SecretStore'
    coreweave.sandbox.v1beta2.DeleteFileSystemSnapshotResponse:
      description: DeleteFileSystemSnapshotResponse indicates success or failure.
      type: object
      properties:
        success:
          type: boolean
        errorMessage:
          type: string
    coreweave.sandbox.v1beta2.DeleteObjectStorageWIFConfigResponse:
      type: object
      properties: {}
    coreweave.sandbox.v1beta2.DeleteSandboxResponse:
      description: DeleteSandboxResponse indicates success or failure of deletion.
      type: object
      properties:
        success:
          type: boolean
        errorMessage:
          type: string
    coreweave.sandbox.v1beta2.DeleteSecretStoreResponse:
      type: object
      properties: {}
    coreweave.sandbox.v1beta2.EgressMode:
      description: EgressMode describes a supported egress mode.
      type: object
      properties:
        name:
          type: string
    coreweave.sandbox.v1beta2.ExecPayload:
      description: ExecPayload describes a command execution inside an existing sandbox.
      type: object
      properties:
        command:
          type: string
        args:
          type: array
          items:
            type: string
      required:
      - command
    coreweave.sandbox.v1beta2.ExecResponse:
      description: ExecResponse is the result of an Exec call.
      type: object
      properties:
        stdout:
          type: string
          format: bytes
        stderr:
          type: string
          format: bytes
        exitCode:
          type: integer
          format: int32
        stdoutTruncated:
          type: boolean
        stderrTruncated:
          type: boolean
        stdoutBytesProduced:
          type: string
        stderrBytesProduced:
          type: string
    coreweave.sandbox.v1beta2.ExecSandboxRequest:
      description: ExecSandboxRequest executes a command within a sandbox.
      type: object
      properties:
        sandboxId:
          type: string
        command:
          type: array
          items:
            type: string
        args:
          type: array
          items:
            type: string
        maxTimeoutSeconds:
          type: integer
          format: int32
        outputHandling:
          type: string
          format: enum
          enum:
          - OUTPUT_POLICY_UNSPECIFIED
          - OUTPUT_POLICY_BUFFERED
          - OUTPUT_POLICY_STREAM
          - OUTPUT_POLICY_DISCARD
        bufferedMaxKib:
          type: integer
          format: uint32
      required:
      - sandboxId
      - command
    coreweave.sandbox.v1beta2.ExecSandboxResponse:
      description: ExecSandboxResponse returns command output.
      type: object
      properties:
        result:
          $ref: '#/components/schemas/coreweave.sandbox.v1beta2.ExecResponse'
    coreweave.sandbox.v1beta2.FileSystemSnapshot:
      description: "FileSystemSnapshot is an immutable, org-scoped snapshot of a sandbox\n filesystem\
        \ mount."
      type: object
      properties:
        fileSystemSnapshotId:
          type: string
        status:
          type: string
          format: enum
          enum:
          - FILE_SYSTEM_SNAPSHOT_STATUS_UNSPECIFIED
          - FILE_SYSTEM_SNAPSHOT_STATUS_CREATING
          - FILE_SYSTEM_SNAPSHOT_STATUS_READY
          - FILE_SYSTEM_SNAPSHOT_STATUS_FAILED
          - FILE_SYSTEM_SNAPSHOT_STATUS_DELETING
        statusReason:
          type: string
        sizeBytes:
          type: string
        createdAt:
          type: string
          format: date-time
        updatedAt:
          type: string
          format: date-time
        completedAt:
          type: string
          format: date-time
        sourceSandboxId:
          type: string
        trigger:
          type: string
          format: enum
          enum:
          - FILE_SYSTEM_SNAPSHOT_TRIGGER_UNSPECIFIED
          - FILE_SYSTEM_SNAPSHOT_TRIGGER_STOP
          - FILE_SYSTEM_SNAPSHOT_TRIGGER_MANUAL
        idempotencyKey:
          type: string
        objectBucket:
          description: "The object-storage bucket this snapshot's archive was written to. Lets a\n customer\
            \ see which snapshots a bucket change stranded: when object_bucket\n differs from the org's\
            \ current FSS bucket, restore returns\n CWSANDBOX_FSS_BUCKET_MISMATCH (reversible by reverting\
            \ the bucket)."
          type: string
          readOnly: true
    coreweave.sandbox.v1beta2.FileSystemSnapshotBucketConfig:
      description: "FileSystemSnapshotBucketConfig is an organization's FSS bucket configuration.\n The\
        \ mode is implied by field presence: supply bucket_name (+ region) to bring\n your own bucket;\
        \ leave both empty for CoreWeave-managed (the default)."
      type: object
      properties:
        bucketName:
          description: Bring-your-own bucket name. Empty means CoreWeave manages the bucket.
          type: string
        region:
          description: Object-store region for the bring-your-own bucket. Required iff bucket_name is
            set.
          type: string
        mode:
          description: The effective ownership mode, derived by the server.
          type: string
          format: enum
          enum:
          - FILE_SYSTEM_SNAPSHOT_BUCKET_MODE_UNSPECIFIED
          - FILE_SYSTEM_SNAPSHOT_BUCKET_MODE_CW_MANAGED
          - FILE_SYSTEM_SNAPSHOT_BUCKET_MODE_BRING_YOUR_OWN
          readOnly: true
        effectiveBucketName:
          description: 'The bucket actually in effect: the customer bucket, or the CoreWeave-managed derived
            name.'
          type: string
          readOnly: true
    coreweave.sandbox.v1beta2.FileSystemSnapshotSource:
      description: "FileSystemSnapshotSource identifies an immutable File System Snapshot (FSS)\n to restore\
        \ into a sandbox filesystem mount. Empty file_system_snapshot_id\n means start from an empty scratch\
        \ filesystem that can be snapshotted later."
      type: object
      properties:
        fileSystemSnapshotId:
          type: string
    coreweave.sandbox.v1beta2.GetSandboxResponse:
      description: GetSandboxResponse returns details about a sandbox.
      type: object
      properties:
        sandboxId:
          type: string
        startedAtTime:
          type: string
          format: date-time
        sandboxStatus:
          type: string
          format: enum
          enum:
          - SANDBOX_STATUS_UNSPECIFIED
          - SANDBOX_STATUS_CREATING
          - SANDBOX_STATUS_RUNNING
          - SANDBOX_STATUS_COMPLETED
          - SANDBOX_STATUS_FAILED
          - SANDBOX_STATUS_TERMINATED
          - SANDBOX_STATUS_PENDING
          - SANDBOX_STATUS_PAUSED
          - SANDBOX_STATUS_TERMINATING
        currentResourceUsage:
          $ref: '#/components/schemas/coreweave.sandbox.v1beta2.ResourceUsage'
        runnerId:
          type: string
        runnerGroupId:
          type: string
        profileId:
          type: string
        serviceAddress:
          type: string
        exposedPorts:
          type: array
          items:
            $ref: '#/components/schemas/coreweave.sandbox.v1beta2.Port'
        appliedIngressMode:
          type: string
        appliedEgressMode:
          type: string
        statusReason:
          description: "The reason recorded for the most recent status transition. Populated for\n terminal\
            \ statuses (FAILED, COMPLETED, TERMINATED) so clients can surface\n why a sandbox finished\
            \ without a separate API call. Empty for sandboxes\n still running normally."
          type: string
        exitCode:
          description: "Exit code of the sandbox's main process. Populated when the runner's own\n terminal\
            \ report ended the sandbox — the pod terminated of its own accord:\n always set for COMPLETED,\
            \ set for FAILED only when nonzero. Absent for\n non-terminal sandboxes, gateway-initiated\
            \ stops (a stop deletes the pod,\n so its final state is inferred rather than observed and\
            \ no code is\n reported), sandboxes that terminated before this field was introduced,\n and\
            \ FAILED sandboxes whose container never ran. Check presence; 0 is a\n meaningful exit code."
          type: integer
          format: int32
        userId:
          description: "ID of the user that created the sandbox, as recorded from the\n authenticated\
            \ identity at create time. Lets an org admin attribute the\n sandbox to its owner. Best-effort\
            \ on the live-status path; may be empty\n for sandboxes created before this field was introduced."
          type: string
    coreweave.sandbox.v1beta2.GetSecretStoreResponse:
      type: object
      properties:
        secretStore:
          $ref: '#/components/schemas/coreweave.sandbox.v1beta2.SecretStore'
    coreweave.sandbox.v1beta2.GpuRequest:
      type: object
      properties:
        gpuCount:
          type: string
        gpuType:
          type: string
        gpuMemoryGb:
          type: string
    coreweave.sandbox.v1beta2.KubernetesSecretSource:
      description: "KubernetesSecretSource identifies a specific key within a Kubernetes Secret.\n Used\
        \ for runner cluster secrets resolved locally by Runner."
      type: object
      properties:
        secretName:
          type: string
        secretKey:
          type: string
      required:
      - secretName
      - secretKey
    coreweave.sandbox.v1beta2.ListAvailableRunnersResponse:
      type: object
      properties:
        runners:
          type: array
          items:
            $ref: '#/components/schemas/coreweave.sandbox.v1beta2.AvailableRunner'
        nextPageToken:
          type: string
    coreweave.sandbox.v1beta2.ListFileSystemSnapshotsResponse:
      description: ListFileSystemSnapshotsResponse returns a page of FSS rows.
      type: object
      properties:
        fileSystemSnapshots:
          type: array
          items:
            $ref: '#/components/schemas/coreweave.sandbox.v1beta2.FileSystemSnapshot'
        nextPageToken:
          type: string
    coreweave.sandbox.v1beta2.ListManagedRunnersResponse:
      type: object
      properties:
        runners:
          type: array
          items:
            $ref: '#/components/schemas/coreweave.sandbox.v1beta2.Runner'
        nextPageToken:
          type: string
    coreweave.sandbox.v1beta2.ListProfileTemplatesResponse:
      type: object
      properties:
        profileTemplates:
          type: array
          items:
            $ref: '#/components/schemas/coreweave.sandbox.v1beta2.ProfileTemplate'
        nextPageToken:
          type: string
    coreweave.sandbox.v1beta2.ListProfilesResponse:
      type: object
      properties:
        profiles:
          type: array
          items:
            $ref: '#/components/schemas/coreweave.sandbox.v1beta2.ProfileSummary'
        nextPageToken:
          type: string
    coreweave.sandbox.v1beta2.ListRunnerJoinTokensResponse:
      description: ListRunnerJoinTokensResponse returns paginated list of tokens
      type: object
      properties:
        tokens:
          type: array
          items:
            $ref: '#/components/schemas/coreweave.sandbox.v1beta2.RunnerJoinToken'
        nextPageToken:
          type: string
    coreweave.sandbox.v1beta2.ListSandboxesResponse:
      description: ListSandboxesResponse returns a list of sandboxes.
      type: object
      properties:
        sandboxes:
          type: array
          items:
            $ref: '#/components/schemas/coreweave.sandbox.v1beta2.SandboxInfo'
        nextPageToken:
          description: "Token to pass as page_token in the next request. Empty when there are no\n more\
            \ pages."
          type: string
    coreweave.sandbox.v1beta2.ListSecretStoresResponse:
      type: object
      properties:
        secretStores:
          type: array
          items:
            $ref: '#/components/schemas/coreweave.sandbox.v1beta2.SecretStore'
        nextPageToken:
          description: Token for retrieving the next page. Empty if no more results.
          type: string
    coreweave.sandbox.v1beta2.MaintenanceExclusion:
      description: "MaintenanceExclusion defines a one-time exclusion period during which no\n updates\
        \ start, overriding any open maintenance window."
      type: object
      properties:
        startTime:
          description: Start of the exclusion period (inclusive).
          type: string
          format: date-time
        endTime:
          description: End of the exclusion period (exclusive). Must be after start_time.
          type: string
          format: date-time
        reason:
          description: Human-readable reason for the exclusion.
          type: string
      required:
      - startTime
      - endTime
    coreweave.sandbox.v1beta2.MaintenancePolicy:
      description: MaintenancePolicy controls when updates can be applied to managed runners.
      type: object
      properties:
        windows:
          description: Maintenance windows during which updates are allowed.
          type: array
          items:
            $ref: '#/components/schemas/coreweave.sandbox.v1beta2.MaintenanceWindow'
        exclusions:
          description: Exclusion periods during which no updates should be applied.
          type: array
          items:
            $ref: '#/components/schemas/coreweave.sandbox.v1beta2.MaintenanceExclusion'
    coreweave.sandbox.v1beta2.MaintenanceWindow:
      description: "MaintenanceWindow defines a recurring time window during which updates\n may start.\
        \ If any windows are configured, updates start only while one is\n open; exclusions override windows."
      type: object
      properties:
        cron:
          description: "Standard 5-field cron expression for the window start (e.g.,\n \"0 2 * * SAT\"\
            \ for Saturdays at 02:00), evaluated in UTC. Descriptor\n forms such as \"@daily\" or \"@every\
            \ 1h\" are rejected, as are expressions\n that never fire (e.g. a nonexistent calendar date)."
          type: string
        durationSeconds:
          description: "Duration of the window in seconds. Must be between 60 (1 minute) and\n 604800\
            \ (7 days)."
          type: integer
          format: int32
      required:
      - cron
      - durationSeconds
    coreweave.sandbox.v1beta2.ManagedRunnerSpec:
      description: ManagedRunnerSpec contains configuration specific to platform-managed runners.
      type: object
      properties:
        releaseChannel:
          description: Release channel for automatic updates.
          type: string
          format: enum
          enum:
          - RELEASE_CHANNEL_UNSPECIFIED
          - RELEASE_CHANNEL_STABLE
          - RELEASE_CHANNEL_RAPID
        maintenancePolicy:
          description: Maintenance policy for update scheduling.
          allOf:
          - $ref: '#/components/schemas/coreweave.sandbox.v1beta2.MaintenancePolicy'
        overrides:
          description: Customer-settable deployment overrides.
          allOf:
          - $ref: '#/components/schemas/coreweave.sandbox.v1beta2.RunnerDeploymentOverrides'
        allowPrivilegedProfileAnnotations:
          description: "When true, profile templates bound to this runner may carry a privileged\n posture\
            \ the platform otherwise restricts. Despite the name, this governs\n BOTH privileged pod annotations\
            \ (prefix categories) AND privileged\n structured pod-spec fields (e.g. serviceAccountName,\
            \ host namespaces,\n hostPath volumes, privileged/escalating containers). Defaults to false.\n\
            \ Contact CoreWeave support before enabling.\n\n To disable after enabling, include this field\
            \ path in update_mask;\n the call is rejected if any bound template would no longer be valid."
          type: boolean
        enforceResourceLimits:
          description: "When true, sandboxes and bound profile templates must declare both\n memory and\
            \ CPU limits. Recommended on multi-tenant runners. Defaults\n to false.\n\n To disable after\
            \ enabling, include this field path in update_mask;\n the call is rejected if any bound template\
            \ would no longer be valid."
          type: boolean
        volumes:
          description: "Registered-Volume (PVC) support for this runner. When present, this\n typed toggle\
            \ is authoritative over any ENABLE_VOLUMES /\n VOLUME_DRIVER_ALLOWLIST entries in deployment\
            \ env; when absent, env\n passthrough applies unchanged."
          allOf:
          - $ref: '#/components/schemas/coreweave.sandbox.v1beta2.RunnerVolumesConfig'
        tenantMetrics:
          description: "Tenant-metrics collector for this runner's cluster. When present, this\n typed\
            \ toggle is authoritative over any\n ENABLE_TENANT_METRICS_COLLECTOR / TENANT_METRICS_COLLECTOR_IMAGE\
            \ entries\n in deployment env; when absent, env passthrough applies unchanged.\n Enabling\
            \ is necessary but not sufficient: the zone's runner-controller\n must run --enable-tenant-metrics-collector,\
            \ which is sequenced on the\n collector RBAC pre-grant reaching the cluster."
          allOf:
          - $ref: '#/components/schemas/coreweave.sandbox.v1beta2.RunnerTenantMetricsConfig'
        endpointRoutes:
          description: "https and tls_passthrough attachments for this managed runner. Sole\n source of\
            \ Runner.deployment_spec.endpoint_routes; no zone, org, or\n version default. Slots are independent.\n\
            \n UpdateManagedRunner: a child path (managed_spec.endpoint_routes.https\n or .tls_passthrough)\
            \ or an omitted mask merges present slots and\n leaves absent siblings unchanged. A mask of\
            \ this field replaces the\n whole message; omit a slot to drop it. Enabling a slot is not\n\
            \ sufficient to advertise it. HTTPS advertises only after Gateway and\n HTTPRoute preflight.\
            \ TLS passthrough advertises only after Gateway\n and TLSRoute preflight."
          allOf:
          - $ref: '#/components/schemas/coreweave.sandbox.v1beta2.RunnerEndpointRoutes'
        dataPlane:
          description: "Direct sandbox data-plane endpoint configuration. Unset uses the platform\n default;\
            \ the disabled exposure keeps all data operations on the Gateway."
          allOf:
          - $ref: '#/components/schemas/coreweave.sandbox.v1beta2.RunnerDataPlaneConfig'
        imagePull:
          description: "Image pull behavior for sandbox workload containers on this runner. When\n present,\
            \ this typed setting is authoritative over any equivalent\n deployment env entry; when absent,\
            \ the platform default applies."
          allOf:
          - $ref: '#/components/schemas/coreweave.sandbox.v1beta2.RunnerImagePullConfig'
    coreweave.sandbox.v1beta2.MountedFile:
      description: "MountedFile describes a file injected at container startup time.\n The mount_path\
        \ should include the full path including the filename."
      type: object
      properties:
        mountPath:
          type: string
        fileContent:
          type: string
          format: bytes
      required:
      - mountPath
      - fileContent
    coreweave.sandbox.v1beta2.NetworkOptions:
      description: NetworkOptions defines network configuration options for the sandbox.
      type: object
      properties:
        ingressMode:
          description: "Ingress mode name configured by runner operator (e.g., \"internal\", \"public\"\
            , \"custom\").\n Empty means no service exposed. Must match a mode in runner's service_exposure_modes."
          type: string
        exposedPorts:
          description: "Which container ports (from request.ports) to expose via K8s Service.\n Must reference\
            \ valid port numbers from the ports field."
          type: array
          items:
            type: integer
            format: int32
        egressMode:
          description: "Egress mode name configured by runner operator (e.g., \"direct\", \"natgateway\"\
            ).\n Empty means default egress behavior. Must match a mode in runner's egress_modes."
          type: string
    coreweave.sandbox.v1beta2.ObjectStorageAccess:
      description: "ObjectStorageAccess describes object storage access to provision for a sandbox.\n\
        \ When provided, Gateway mints a per-sandbox OIDC token and Runner injects a credential\n vending\
        \ sidecar that exchanges it for temporary S3 credentials."
      type: object
      properties:
        buckets:
          type: array
          items:
            type: string
        permission:
          type: string
          format: enum
          enum:
          - OBJECT_STORAGE_PERMISSION_UNSPECIFIED
          - OBJECT_STORAGE_PERMISSION_READ
          - OBJECT_STORAGE_PERMISSION_READ_WRITE
        objectPrefix:
          description: "Optional object-key prefix that scopes the vended credential to keys under it,\n\
            \ applied to every bucket in the grant (e.g. \"tenants/<org>/cache/\"). When unset,\n the\
            \ credential is not prefix-scoped. The caller owns and supplies this scope.\n\n Validated\
            \ (InvalidArgument otherwise): must start with an alphanumeric, contain\n only characters\
            \ [a-zA-Z0-9._/-], contain no \"..\" or \"//\", be at most 512 bytes,\n and end with \"/\"\
            ."
          type: string
    coreweave.sandbox.v1beta2.ObjectStorageWIFConfig:
      description: The WIF configuration for an organization's object storage access.
      type: object
      properties:
        id:
          description: Server-assigned unique identifier.
          type: string
          readOnly: true
        wifConfigId:
          description: "The WIF config ID from CoreWeave Cloud Console.\n Obtained by creating a Workload\
            \ Federation configuration in the Console."
          type: string
        enabled:
          description: "Whether object storage access is enabled for this organization.\n When omitted\
            \ in a Set request, defaults to true (enabled)."
          type: boolean
        allowedBuckets:
          description: "Bucket names the organization is allowed to access.\n Empty means all buckets\
            \ are allowed."
          type: array
          items:
            type: string
        maxPermission:
          description: Maximum permission level for sandboxes.
          type: string
          format: enum
          enum:
          - OBJECT_STORAGE_PERMISSION_UNSPECIFIED
          - OBJECT_STORAGE_PERMISSION_READ
          - OBJECT_STORAGE_PERMISSION_READ_WRITE
        createdAt:
          description: Server-assigned timestamps.
          type: string
          format: date-time
          readOnly: true
        updatedAt:
          type: string
          format: date-time
          readOnly: true
      required:
      - wifConfigId
      - maxPermission
    coreweave.sandbox.v1beta2.PauseSandboxRequest:
      description: PauseSandboxRequest pauses a running sandbox.
      type: object
      properties:
        sandboxId:
          type: string
        maxTimeoutSeconds:
          type: integer
          format: int32
      required:
      - sandboxId
    coreweave.sandbox.v1beta2.PauseSandboxResponse:
      description: PauseSandboxResponse indicates success or failure.
      type: object
      properties:
        success:
          type: boolean
        errorMessage:
          type: string
    coreweave.sandbox.v1beta2.Port:
      description: Port defines a port to expose on the container.
      type: object
      properties:
        containerPort:
          type: integer
          format: int32
        name:
          type: string
        protocol:
          type: string
      required:
      - containerPort
    coreweave.sandbox.v1beta2.ProfileSpec:
      description: ProfileSpec defines the compute and networking parameters for a profile.
      type: object
      properties:
        containerImage:
          description: Container image override (optional).
          type: string
        runtimeClass:
          description: Runtime class name for isolation.
          type: string
        resourceDefaults:
          description: Resource defaults for sandboxes on this profile.
          allOf:
          - $ref: '#/components/schemas/coreweave.sandbox.v1beta2.ResourceDefaults'
        instanceTypes:
          description: Node placement constraints.
          type: array
          items:
            type: string
        nodeSelector:
          description: Node selector labels.
          type: object
          additionalProperties:
            type: string
        tags:
          description: Tags for RBAC-based access control.
          type: array
          items:
            type: string
        namespaceConfigJson:
          description: Namespace strategy configuration (JSON-encoded for flexibility).
          type: string
        networkConfigJson:
          description: Network configuration (JSON-encoded for flexibility).
          type: string
        podTemplateJson:
          description: Pod template overrides (JSON-encoded PodSpec fragment).
          type: string
    coreweave.sandbox.v1beta2.ProfileSummary:
      description: ProfileSummary describes a single profile on a single runner.
      type: object
      properties:
        profileName:
          type: string
        runnerId:
          type: string
        supportedGpuTypes:
          type: array
          items:
            type: string
        supportedArchitectures:
          type: array
          items:
            type: string
        serviceExposureModes:
          type: array
          items:
            $ref: '#/components/schemas/coreweave.sandbox.v1beta2.ServiceExposureMode'
        egressModes:
          type: array
          items:
            $ref: '#/components/schemas/coreweave.sandbox.v1beta2.EgressMode'
    coreweave.sandbox.v1beta2.ProfileTemplate:
      description: ProfileTemplate defines a reusable profile configuration.
      type: object
      properties:
        id:
          description: Server-assigned unique identifier (UUID).
          type: string
          readOnly: true
        organizationId:
          description: Organization that owns this template.
          type: string
          readOnly: true
        displayName:
          description: Human-readable template name (unique within org, set by the user).
          type: string
        description:
          description: Human-readable description.
          type: string
        spec:
          description: Profile specification.
          allOf:
          - $ref: '#/components/schemas/coreweave.sandbox.v1beta2.ProfileSpec'
        labels:
          description: User-defined labels for organizing templates.
          type: object
          additionalProperties:
            type: string
        createdAt:
          description: Timestamps.
          type: string
          format: date-time
          readOnly: true
        updatedAt:
          type: string
          format: date-time
          readOnly: true
      required:
      - displayName
      - spec
    coreweave.sandbox.v1beta2.RawSandboxRequest:
      description: RawSandboxRequest executes a raw action on a sandbox.
      type: object
      properties:
        sandboxId:
          type: string
        actionType:
          type: string
          format: enum
          enum:
          - ACTION_TYPE_UNSPECIFIED
          - ACTION_TYPE_EXEC
          - ACTION_TYPE_ADD_FILE
          - ACTION_TYPE_RETRIEVE_FILE
          - ACTION_TYPE_GET_LOGS
          - ACTION_TYPE_SNAPSHOT
          - ACTION_TYPE_RESTORE
          - ACTION_TYPE_STATUS
          - ACTION_TYPE_STOP
        execPayload:
          $ref: '#/components/schemas/coreweave.sandbox.v1beta2.ExecPayload'
        addFilePayload:
          $ref: '#/components/schemas/coreweave.sandbox.v1beta2.AddFileSandboxRequest'
        retrieveFilePayload:
          $ref: '#/components/schemas/coreweave.sandbox.v1beta2.RetrieveFileSandboxRequest'
        maxTimeoutSeconds:
          type: integer
          format: int32
      required:
      - sandboxId
      - actionType
    coreweave.sandbox.v1beta2.RawSandboxResponse:
      description: RawSandboxResponse returns the result of a raw action.
      type: object
      properties:
        actionType:
          type: string
          format: enum
          enum:
          - ACTION_TYPE_UNSPECIFIED
          - ACTION_TYPE_EXEC
          - ACTION_TYPE_ADD_FILE
          - ACTION_TYPE_RETRIEVE_FILE
          - ACTION_TYPE_GET_LOGS
          - ACTION_TYPE_SNAPSHOT
          - ACTION_TYPE_RESTORE
          - ACTION_TYPE_STATUS
          - ACTION_TYPE_STOP
        execResponse:
          $ref: '#/components/schemas/coreweave.sandbox.v1beta2.ExecSandboxResponse'
        addFileResponse:
          $ref: '#/components/schemas/coreweave.sandbox.v1beta2.AddFileSandboxResponse'
        retrieveFileResponse:
          $ref: '#/components/schemas/coreweave.sandbox.v1beta2.RetrieveFileSandboxResponse'
    coreweave.sandbox.v1beta2.ResourceDefaults:
      description: ResourceDefaults defines default resource requests/limits for sandboxes.
      type: object
      properties:
        cpuRequest:
          type: string
        memoryRequest:
          type: string
        cpuLimit:
          type: string
        memoryLimit:
          type: string
    coreweave.sandbox.v1beta2.ResourceRequest:
      description: ResourceRequest specifies compute resource requirements for a sandbox.
      type: object
      properties:
        cpu:
          type: string
        memory:
          type: string
        gpu:
          $ref: '#/components/schemas/coreweave.sandbox.v1beta2.GpuRequest'
    coreweave.sandbox.v1beta2.ResourceUsage:
      description: ResourceUsage represents current resource usage of a sandbox.
      type: object
      properties:
        cpuMillicoresUsed:
          type: string
        memoryMbUsed:
          type: string
        gpuCountUsed:
          type: string
    coreweave.sandbox.v1beta2.ResumeSandboxRequest:
      description: ResumeSandboxRequest resumes a paused sandbox.
      type: object
      properties:
        sandboxId:
          type: string
        maxTimeoutSeconds:
          type: integer
          format: int32
      required:
      - sandboxId
    coreweave.sandbox.v1beta2.ResumeSandboxResponse:
      description: ResumeSandboxResponse indicates success or failure.
      type: object
      properties:
        success:
          type: boolean
        errorMessage:
          type: string
    coreweave.sandbox.v1beta2.RetrieveFileSandboxRequest:
      description: RetrieveFileSandboxRequest retrieves a file's contents from the sandbox.
      type: object
      properties:
        sandboxId:
          type: string
        filepath:
          type: string
        maxTimeoutSeconds:
          type: integer
          format: int32
      required:
      - sandboxId
      - filepath
    coreweave.sandbox.v1beta2.RetrieveFileSandboxResponse:
      description: RetrieveFileSandboxResponse returns file contents.
      type: object
      properties:
        fileContents:
          type: string
          format: bytes
        success:
          type: boolean
        errorMessage:
          type: string
    coreweave.sandbox.v1beta2.RevokeRunnerJoinTokenResponse:
      description: RevokeRunnerJoinTokenResponse indicates revocation success
      type: object
      properties:
        success:
          type: boolean
        message:
          type: string
    coreweave.sandbox.v1beta2.Runner:
      description: Runner represents a registered runner (compute cluster endpoint).
      type: object
      properties:
        id:
          description: Server-assigned unique identifier (UUID).
          type: string
          readOnly: true
        displayName:
          description: Human-readable name for the runner (set by the user, unique within org).
          type: string
        identity:
          description: Core identity fields (shared with data-plane RunnerInfo).
          allOf:
          - $ref: '#/components/schemas/coreweave.sandbox.v1beta2.RunnerIdentity'
        managementMode:
          description: Management mode (MANAGED or SELF_MANAGED).
          type: string
          format: enum
          enum:
          - MANAGEMENT_MODE_UNSPECIFIED
          - MANAGEMENT_MODE_MANAGED
          - MANAGEMENT_MODE_SELF_MANAGED
          readOnly: true
        managedSpec:
          description: Managed runner specification (only set for MANAGED runners).
          allOf:
          - $ref: '#/components/schemas/coreweave.sandbox.v1beta2.ManagedRunnerSpec'
        installStatus:
          description: Current install status (only meaningful for MANAGED runners).
          type: string
          format: enum
          enum:
          - RUNNER_INSTALL_STATUS_UNSPECIFIED
          - RUNNER_INSTALL_STATUS_PENDING
          - RUNNER_INSTALL_STATUS_PROVISIONING
          - RUNNER_INSTALL_STATUS_READY
          - RUNNER_INSTALL_STATUS_FAILED
          - RUNNER_INSTALL_STATUS_DELETING
          readOnly: true
        connectionStatus:
          description: Live connection status.
          type: string
          format: enum
          enum:
          - RUNNER_CONNECTION_STATUS_UNSPECIFIED
          - RUNNER_CONNECTION_STATUS_CONNECTED
          - RUNNER_CONNECTION_STATUS_DISCONNECTED
          readOnly: true
        activeConfigVersion:
          description: Active configuration version running on the runner.
          type: string
          readOnly: true
        activeProfileSpecVersion:
          description: Active profile spec version.
          type: string
          readOnly: true
        activeRevision:
          description: Active revision number currently running on the runner.
          type: integer
          format: int32
          readOnly: true
        targetRevision:
          description: Target revision number that should be rolled out.
          type: integer
          format: int32
          readOnly: true
        deploymentSpec:
          description: Resolved deployment spec for the runner.
          allOf:
          - $ref: '#/components/schemas/coreweave.sandbox.v1beta2.RunnerDeploymentSpec'
          readOnly: true
        updateAvailable:
          description: "Whether an update is available on this runner's release channel.\n True when the\
            \ channel has a newer version than what's currently deployed."
          type: boolean
          readOnly: true
        createdAt:
          description: Timestamps.
          type: string
          format: date-time
          readOnly: true
        updatedAt:
          type: string
          format: date-time
          readOnly: true
        lastHeartbeatAt:
          type: string
          format: date-time
          readOnly: true
        profileBindings:
          description: "Profile bindings attached to this runner.\n\n On Create: REQUIRED. The runner\
            \ is created with these bindings in one\n transaction — there is no intermediate state where\
            \ the runner has zero\n profiles and is unschedulable. Exactly one binding must have is_default=true.\n\
            \n On Update with update_mask covering \"profile_bindings\": the desired list\n fully replaces\
            \ the current list. Entries are matched by profile_template_id;\n new entries are attached,\
            \ missing entries are detached, and changed entries\n are updated in place — all within one\
            \ transaction. The result must remain\n non-empty with exactly one is_default=true.\n\n On\
            \ Get / List: populated with the current bindings. Entries carry their\n server-assigned id\
            \ (OUTPUT_ONLY) so clients can correlate them."
          type: array
          items:
            $ref: '#/components/schemas/coreweave.sandbox.v1beta2.RunnerProfileBinding'
        installError:
          description: "Populated when install_status == FAILED. Cleared when status transitions\n back\
            \ to PROVISIONING/READY. Use reason to drive UX (retry hint vs.\n support contact) and message\
            \ for display."
          allOf:
          - $ref: '#/components/schemas/coreweave.sandbox.v1beta2.RunnerInstallError'
          readOnly: true
        rolloutInProgress:
          description: "True when the runner is mid-rollout: target_revision > active_revision.\n Derived\
            \ server-side from the persisted revision counters so clients don't\n re-implement the inequality.\
            \ Stays true through a ROLLOUT_TIMED_OUT\n failure (active_revision still trails) — clients\
            \ should pair this with\n install_status to render rollout state distinct from steady-state\
            \ health."
          type: boolean
          readOnly: true
        schedulingDisabled:
          description: "When true, this runner is excluded from placement selection: no new\n sandboxes\
            \ are scheduled onto it. Sandboxes already running on the runner\n are unaffected and remain\
            \ fully manageable (exec, file operations, stop).\n Defaults to false. Set or clear it with\
            \ UpdateManagedRunner using\n update_mask \"scheduling_disabled\" — typically before maintenance\
            \ or\n decommissioning a runner."
          type: boolean
        dataPlaneStatus:
          description: Observed direct data-plane endpoint state.
          allOf:
          - $ref: '#/components/schemas/coreweave.sandbox.v1beta2.RunnerDataPlaneStatus'
          readOnly: true
      required:
      - identity
    coreweave.sandbox.v1beta2.RunnerCapabilitySummary:
      description: "RunnerCapabilitySummary describes a runner's reported features and aggregate\n capacity\
        \ ceilings, rather than its currently available resources.\n\n The max_cpu_millicores, max_memory_bytes,\
        \ and max_gpu_count values can change\n between responses. Depending on runner configuration,\
        \ CPU and memory ceilings\n may exclude capacity reserved for GPU workloads and can change without\
        \ nodes\n being added or removed. These values do not guarantee that a placement fits.\n\n When\
        \ capability information is available, feature fields are exposed for\n both owned and shared\
        \ runners. The max_* values are disclosed only for owned\n runners; they remain zero for shared\
        \ runners (AvailableRunner.is_shared).\n A zero value alone does not distinguish zero capacity\
        \ from an unreported or\n undisclosed ceiling.\n\n When capabilities and resources are both present,\
        \ use values from the same\n response rather than combining resources with cached ceilings. They\
        \ need not\n reflect the same measurement time."
      type: object
      properties:
        maxCpuMillicores:
          description: Reported aggregate CPU capacity ceiling, in millicores.
          type: string
        maxMemoryBytes:
          description: Reported aggregate memory capacity ceiling, in bytes.
          type: string
        maxGpuCount:
          description: Reported aggregate GPU capacity, including GPUs currently in use.
          type: string
        supportedGpuTypes:
          type: array
          items:
            type: string
        supportedArchitectures:
          type: array
          items:
            type: string
        supportsPrivileged:
          type: boolean
        availableStorageClasses:
          type: array
          items:
            type: string
    coreweave.sandbox.v1beta2.RunnerClusterSecretReference:
      description: "RunnerClusterSecretReference describes a runner cluster secret to inject into a sandbox.\n\
        \ Distinct from external secret stores. This mechanism resolves secrets\n locally on the Runner's\
        \ cluster — secret values never transit Gateway,\n only references flow through the hub."
      type: object
      properties:
        kubernetes:
          $ref: '#/components/schemas/coreweave.sandbox.v1beta2.KubernetesSecretSource'
        envVar:
          description: Target environment variable name for the resolved secret value.
          type: string
      required:
      - envVar
    coreweave.sandbox.v1beta2.RunnerDataPlaneClusterIPConfig:
      description: "RunnerDataPlaneClusterIPConfig exposes the direct endpoint through a stable\n ClusterIP\
        \ Service. The platform derives its URI and server-certificate SANs."
      type: object
      properties:
        annotations:
          type: object
          additionalProperties:
            type: string
    coreweave.sandbox.v1beta2.RunnerDataPlaneConfig:
      description: "RunnerDataPlaneConfig controls the dedicated Runner endpoint for direct\n sandbox\
        \ data operations. The platform issues and rotates the endpoint's\n server certificate; this configuration\
        \ contains no certificate source or\n private key material."
      type: object
      properties:
        disabled:
          $ref: '#/components/schemas/coreweave.sandbox.v1beta2.RunnerDataPlaneDisabledConfig'
        clusterIp:
          $ref: '#/components/schemas/coreweave.sandbox.v1beta2.RunnerDataPlaneClusterIPConfig'
        loadBalancer:
          $ref: '#/components/schemas/coreweave.sandbox.v1beta2.RunnerDataPlaneLoadBalancerConfig'
        custom:
          $ref: '#/components/schemas/coreweave.sandbox.v1beta2.RunnerDataPlaneCustomConfig'
    coreweave.sandbox.v1beta2.RunnerDataPlaneCustomConfig:
      description: "RunnerDataPlaneCustomConfig advertises a customer-managed network path such\n as a\
        \ VPC route, VPN, service mesh, or Tailscale address. The platform still\n issues the Runner's\
        \ server certificate for the URI's authority."
      type: object
      properties:
        advertisedUri:
          description: Stable absolute URI returned to direct clients.
          type: string
        serviceAnnotations:
          description: "Annotations applied to the backing ClusterIP Service for integrations that\n discover\
            \ or route Kubernetes Services."
          type: object
          additionalProperties:
            type: string
      required:
      - advertisedUri
    coreweave.sandbox.v1beta2.RunnerDataPlaneDisabledConfig:
      description: RunnerDataPlaneDisabledConfig explicitly disables the direct endpoint.
      type: object
      properties: {}
    coreweave.sandbox.v1beta2.RunnerDataPlaneLoadBalancerConfig:
      description: "RunnerDataPlaneLoadBalancerConfig exposes the direct endpoint through a\n stable L4\
        \ LoadBalancer Service. The Service forwards TCP to the Runner and\n does not terminate mutual\
        \ TLS."
      type: object
      properties:
        scope:
          type: string
          format: enum
          enum:
          - RUNNER_DATA_PLANE_SERVICE_SCOPE_UNSPECIFIED
          - RUNNER_DATA_PLANE_SERVICE_SCOPE_PUBLIC
          - RUNNER_DATA_PLANE_SERVICE_SCOPE_PRIVATE
        loadBalancerClass:
          type: string
        annotations:
          type: object
          additionalProperties:
            type: string
        sourceRanges:
          type: array
          items:
            type: string
        externalTrafficPolicy:
          type: string
          format: enum
          enum:
          - RUNNER_DATA_PLANE_EXTERNAL_TRAFFIC_POLICY_UNSPECIFIED
          - RUNNER_DATA_PLANE_EXTERNAL_TRAFFIC_POLICY_CLUSTER
          - RUNNER_DATA_PLANE_EXTERNAL_TRAFFIC_POLICY_LOCAL
        hostname:
          description: "DNS name to publish for the endpoint and include in its server\n certificate.\
            \ When empty, the platform may assign one."
          type: string
    coreweave.sandbox.v1beta2.RunnerDataPlaneStatus:
      description: "RunnerDataPlaneStatus reports the endpoint observed across the logical\n Runner's\
        \ accepting shards."
      type: object
      properties:
        state:
          type: string
          format: enum
          enum:
          - RUNNER_DATA_PLANE_STATE_UNSPECIFIED
          - RUNNER_DATA_PLANE_STATE_DISABLED
          - RUNNER_DATA_PLANE_STATE_PENDING
          - RUNNER_DATA_PLANE_STATE_READY
          - RUNNER_DATA_PLANE_STATE_NOT_READY
          readOnly: true
        endpointId:
          type: string
          readOnly: true
        advertisedUri:
          type: string
          readOnly: true
        protocols:
          type: array
          items:
            type: string
          readOnly: true
        serverCertificateExpiresAt:
          type: string
          format: date-time
          readOnly: true
        message:
          type: string
          readOnly: true
        lastTransitionTime:
          type: string
          format: date-time
          readOnly: true
    coreweave.sandbox.v1beta2.RunnerDeploymentOverrides:
      description: "RunnerDeploymentOverrides contains customer-settable fields that override the\n base\
        \ deployment spec. These are exposed via the ManagedRunnerSpec."
      type: object
      properties:
        nodeSelector:
          description: Node selector labels.
          type: object
          additionalProperties:
            type: string
        tolerations:
          description: Tolerations for scheduling.
          type: array
          items:
            $ref: '#/components/schemas/coreweave.sandbox.v1beta2.RunnerToleration'
        resources:
          description: Resource requirements override.
          allOf:
          - $ref: '#/components/schemas/coreweave.sandbox.v1beta2.RunnerResourceRequirements'
        annotations:
          description: Additional annotations to apply to the runner pods.
          type: object
          additionalProperties:
            type: string
        labels:
          description: Additional labels to apply to the runner pods.
          type: object
          additionalProperties:
            type: string
        env:
          description: Additional environment variables.
          type: object
          additionalProperties:
            type: string
        args:
          description: Additional command-line arguments.
          type: array
          items:
            type: string
        scaling:
          description: Scaling configuration override.
          allOf:
          - $ref: '#/components/schemas/coreweave.sandbox.v1beta2.RunnerScalingConfig'
        cpuRuntimeClass:
          description: Runtime class for CPU-only sandbox pods (e.g., "kata-qemu", "gvisor").
          type: string
        gpuRuntimeClass:
          description: Runtime class for GPU sandbox pods (e.g., "kata-qemu-nvidia-gpu").
          type: string
        affinity:
          description: "Kubernetes Affinity object for runner pods only, using Kubernetes JSON\n field\
            \ names. Supports node affinity, pod affinity, and pod anti-affinity.\n Replaces inherited\
            \ affinity as a whole; an empty object clears it."
          type: object
    coreweave.sandbox.v1beta2.RunnerDeploymentSpec:
      description: "RunnerDeploymentSpec is the full resolved deployment specification for a runner.\n\
        \ This combines version defaults, org-level policies, and customer overrides."
      type: object
      properties:
        image:
          description: Container image (e.g., "ghcr.io/coreweave/sandbox-runner:v0.48.0").
          type: string
        env:
          description: Environment variables.
          type: object
          additionalProperties:
            type: string
        args:
          description: Command-line arguments.
          type: array
          items:
            type: string
        resources:
          description: Resource requirements.
          allOf:
          - $ref: '#/components/schemas/coreweave.sandbox.v1beta2.RunnerResourceRequirements'
        nodeSelector:
          description: Node selector labels.
          type: object
          additionalProperties:
            type: string
        tolerations:
          description: Tolerations for scheduling.
          type: array
          items:
            $ref: '#/components/schemas/coreweave.sandbox.v1beta2.RunnerToleration'
        scaling:
          description: Scaling configuration.
          allOf:
          - $ref: '#/components/schemas/coreweave.sandbox.v1beta2.RunnerScalingConfig'
        annotations:
          description: Additional annotations.
          type: object
          additionalProperties:
            type: string
        labels:
          description: Additional labels.
          type: object
          additionalProperties:
            type: string
        serviceAccount:
          description: Service account name.
          type: string
        extraVolumes:
          description: Extra volume mounts.
          type: array
          items:
            $ref: '#/components/schemas/coreweave.sandbox.v1beta2.RunnerVolumeMount'
        readinessProbe:
          description: Readiness probe configuration.
          allOf:
          - $ref: '#/components/schemas/coreweave.sandbox.v1beta2.RunnerProbeConfig'
        livenessProbe:
          description: Liveness probe configuration.
          allOf:
          - $ref: '#/components/schemas/coreweave.sandbox.v1beta2.RunnerProbeConfig'
        initResources:
          description: Init container resource requirements.
          allOf:
          - $ref: '#/components/schemas/coreweave.sandbox.v1beta2.RunnerResourceRequirements'
        imagePullPolicy:
          description: Image pull policy (Always, IfNotPresent, Never). Defaults to IfNotPresent.
          type: string
        gatewayServer:
          description: Gateway server address for runner join (e.g., "http://sandbox-gateway:8080").
          type: string
        cpuRuntimeClass:
          description: Runtime class for CPU-only sandbox pods.
          type: string
        gpuRuntimeClass:
          description: Runtime class for GPU sandbox pods.
          type: string
        endpointRoutes:
          description: "Resolved product endpoint routing for this runner. OUTPUT_ONLY on\n Runner — derived\
            \ from ManagedRunnerSpec.endpoint_routes when that field is\n present. Absent managed routes\
            \ leave this unset. Slots are independent:\n HTTPS-only, TLS-only, or both. Do not set\n deployment_spec.env[\"\
            ENDPOINT_ROUTES_CONFIG\"]; the controller projects\n typed routes into that env key."
          allOf:
          - $ref: '#/components/schemas/coreweave.sandbox.v1beta2.RunnerEndpointRoutes'
        dataPlane:
          description: Resolved direct data-plane endpoint configuration.
          allOf:
          - $ref: '#/components/schemas/coreweave.sandbox.v1beta2.RunnerDataPlaneConfig'
        workloadTopology:
          description: "Workload topology used to run this logical Runner. Unspecified preserves\n the\
            \ StatefulSet topology for compatibility. Immutable shards create one\n singleton Deployment\
            \ per fixed replica and require session-aware revision\n orchestration before an existing\
            \ Runner can migrate or update."
          type: string
          format: enum
          enum:
          - RUNNER_WORKLOAD_TOPOLOGY_UNSPECIFIED
          - RUNNER_WORKLOAD_TOPOLOGY_STATEFUL_SET
          - RUNNER_WORKLOAD_TOPOLOGY_IMMUTABLE_SHARDS
        affinity:
          description: Resolved Kubernetes Affinity object for runner pods only.
          type: object
    coreweave.sandbox.v1beta2.RunnerEndpointGateway:
      description: "RunnerEndpointGateway identifies the shared parent Gateway a product route\n attaches\
        \ to. Existence/listener checks are deferred to runner create-path;\n Sandman validates the static\
        \ wire contract only. The DNS suffix is resolved\n from the selected Gateway Listener hostname\
        \ at create-path."
      type: object
      properties:
        name:
          type: string
        namespace:
          type: string
        listener:
          type: string
    coreweave.sandbox.v1beta2.RunnerEndpointRoute:
      description: "RunnerEndpointRoute configures one independently mergeable endpoint-route\n slot.\
        \ When the message is present:\n   - enabled=true requires gateway (name/namespace/listener)\n\
        \   - enabled=false clears the inherited slot; gateway must be absent\n   - provider accepted\
        \ values depend on the parent slot"
      type: object
      properties:
        enabled:
          description: Whether this route slot is enabled.
          type: boolean
        gateway:
          description: "Parent Gateway attachment. Required when enabled; must be unset when\n disabled."
          allOf:
          - $ref: '#/components/schemas/coreweave.sandbox.v1beta2.RunnerEndpointGateway'
        provider:
          description: Ingress extras for this slot. Accepted values are slot-dependent.
          type: string
    coreweave.sandbox.v1beta2.RunnerEndpointRoutes:
      description: "Independent https (TLS terminate) and tls_passthrough (SNI passthrough)\n attachments\
        \ to a shared Gateway. Child-path and omitted-mask updates\n merge present slots; a parent-path\
        \ mask replaces the whole message."
      type: object
      properties:
        https:
          description: "Product HTTPS endpoint route (TLS terminate at shared Gateway).\n provider must\
            \ be omitted, empty, or the exact value \"envoy\"."
          allOf:
          - $ref: '#/components/schemas/coreweave.sandbox.v1beta2.RunnerEndpointRoute'
        tlsPassthrough:
          description: "Product TLS passthrough (SNI at the shared Gateway). Independent of https.\n provider\
            \ must be omitted or empty."
          allOf:
          - $ref: '#/components/schemas/coreweave.sandbox.v1beta2.RunnerEndpointRoute'
    coreweave.sandbox.v1beta2.RunnerIdentity:
      description: RunnerIdentity contains the core identity fields for a managed runner.
      type: object
      properties:
        runnerId:
          description: "Operator-assigned runner identifier (unique within org). Set on Create\n and never\
            \ modified afterward — moving runners between IDs is not a\n supported operation."
          type: string
        organizationId:
          description: Organization that owns this runner.
          type: string
          readOnly: true
        runnerGroupId:
          description: "Runner group ID for scheduling affinity. Optional. When omitted or set\n to the\
            \ empty string it is stored as `default`."
          type: string
        zone:
          description: "Geographic zone (e.g., \"us-east-1\", \"eu-west-1\"). Set on Create and\n never\
            \ modified afterward — a managed runner's zone is structurally\n tied to its cluster_id (which\
            \ is itself IMMUTABLE), and controllers\n are zone-sharded. Relocating across zones requires\
            \ re-registration."
          type: string
        clusterId:
          description: "Cluster UUID (CKS canonical identifier). Set on Create and never modified\n afterward\
            \ — relocating a managed runner to a different cluster requires\n a fresh registration."
          type: string
        clusterName:
          description: Cluster display name (human-readable, resolved from CKS at creation time).
          type: string
          readOnly: true
      required:
      - runnerId
    coreweave.sandbox.v1beta2.RunnerImagePullConfig:
      description: "RunnerImagePullConfig sets the image pull behavior for sandbox workload\n containers\
        \ scheduled on a managed runner. Platform-owned helper containers\n keep their own pull behavior\
        \ and are unaffected."
      type: object
      properties:
        policy:
          description: "Pull policy applied to every sandbox workload container on this runner.\n Defaults\
            \ to IF_NOT_PRESENT."
          type: string
          format: enum
          enum:
          - SANDBOX_IMAGE_PULL_POLICY_UNSPECIFIED
          - SANDBOX_IMAGE_PULL_POLICY_IF_NOT_PRESENT
          - SANDBOX_IMAGE_PULL_POLICY_ALWAYS
    coreweave.sandbox.v1beta2.RunnerInstallError:
      description: "RunnerInstallError is the structured failure detail populated on Runner\n when install_status\
        \ == FAILED. `message` is customer-safe display text\n produced from a fixed template per reason\
        \ — raw Kubernetes or driver\n error strings never flow through it. `diagnostic_detail` may include\n\
        \ additional diagnostic context for support cases."
      type: object
      properties:
        reason:
          description: Classified failure reason.
          type: string
          format: enum
          enum:
          - RUNNER_INSTALL_FAILURE_REASON_UNSPECIFIED
          - RUNNER_INSTALL_FAILURE_REASON_NO_SCHEDULABLE_NODES
          - RUNNER_INSTALL_FAILURE_REASON_TAINT_TOLERATION_MISMATCH
          - RUNNER_INSTALL_FAILURE_REASON_NODE_SELECTOR_NO_MATCH
          - RUNNER_INSTALL_FAILURE_REASON_INSUFFICIENT_RESOURCES
          - RUNNER_INSTALL_FAILURE_REASON_IMAGE_PULL_FAILED
          - RUNNER_INSTALL_FAILURE_REASON_CLUSTER_NOT_READY
          - RUNNER_INSTALL_FAILURE_REASON_QUOTA_EXCEEDED
          - RUNNER_INSTALL_FAILURE_REASON_ROLLOUT_TIMED_OUT
          - RUNNER_INSTALL_FAILURE_REASON_INTERNAL_ERROR
          - RUNNER_INSTALL_FAILURE_REASON_CLUSTER_ACCESS_FAILED
          - RUNNER_INSTALL_FAILURE_REASON_GATEWAY_UNREACHABLE
          - RUNNER_INSTALL_FAILURE_REASON_JOIN_TOKEN_FAILED
          - RUNNER_INSTALL_FAILURE_REASON_RUNNER_OFFLINE
          - RUNNER_INSTALL_FAILURE_REASON_CERT_EXPIRED
          - RUNNER_INSTALL_FAILURE_REASON_CLUSTER_NODES_UNHEALTHY
        message:
          description: "Customer-safe, actionable display message. Produced from a fixed\n template per\
            \ reason; never includes raw K8s/driver error strings."
          type: string
        diagnosticDetail:
          description: "Additional diagnostic context (for example error chains or event\n messages).\
            \ Intended for support cases; may be more detailed than\n `message`."
          type: string
        remediationHints:
          description: "Optional customer-facing notes for customer-fault reasons: usually\n structured\
            \ remediation steps (e.g., \"Add toleration for taint\n 'workload=gpu:NoSchedule'\"), occasionally\
            \ informational no-action\n notes (e.g., some nodes being temporarily unavailable alongside\
            \ a\n customer-actionable cause). Not a to-do checklist. Empty for\n platform-fault reasons."
          type: array
          items:
            type: string
        occurredAt:
          description: When the controller classified this failure.
          type: string
          format: date-time
    coreweave.sandbox.v1beta2.RunnerJoinRequest:
      description: RunnerJoinRequest initiates runner join with token
      type: object
      properties:
        token:
          description: Join token from CreateRunnerJoinToken
          type: string
        certificateRequest:
          description: Certificate signing request parameters
          allOf:
          - $ref: '#/components/schemas/coreweave.sandbox.v1beta2.CertificateRequest'
        shardId:
          description: Immutable singleton shard identity. Empty preserves legacy Runner join.
          type: string
        revision:
          description: Immutable Sandman revision rendered into the joining shard.
          type: integer
          format: int32
        podInstanceId:
          description: "Kubernetes Pod UID for this process incarnation. A replacement Pod must\n join\
            \ again and receives a distinct instance-bound certificate."
          type: string
      required:
      - token
    coreweave.sandbox.v1beta2.RunnerJoinResponse:
      description: RunnerJoinResponse returns issued MTLS certificate
      type: object
      properties:
        certificatePem:
          description: PEM-encoded certificate chain
          type: string
          format: bytes
        privateKeyPem:
          description: PEM-encoded private key
          type: string
          format: bytes
        caCertificatePem:
          description: PEM-encoded CA certificate
          type: string
          format: bytes
        serialNumber:
          description: Certificate serial number
          type: string
        expiresAt:
          description: Certificate expiration time
          type: string
          format: date-time
        runnerId:
          description: Runner ID from token
          type: string
        runnerGroupId:
          description: Runner group ID from token
          type: string
        organizationId:
          description: Organization ID from token
          type: string
        gatewayServerAddress:
          description: Gateway server address for connection
          type: string
        shardId:
          description: "Workload identity bound into the issued certificate. Empty for legacy\n Runner\
            \ certificates."
          type: string
        revision:
          type: integer
          format: int32
        podInstanceId:
          type: string
    coreweave.sandbox.v1beta2.RunnerJoinToken:
      description: RunnerJoinToken represents a join token
      type: object
      properties:
        tokenId:
          type: string
        runnerId:
          type: string
        runnerGroupId:
          type: string
        organizationId:
          type: string
        userId:
          type: string
        createdAt:
          type: string
          format: date-time
        expiresAt:
          type: string
          format: date-time
        status:
          type: string
        description:
          type: string
        labels:
          type: object
          additionalProperties:
            type: string
        usedAt:
          type: string
          format: date-time
        certSerialNumber:
          type: string
    coreweave.sandbox.v1beta2.RunnerProbeConfig:
      description: RunnerProbeConfig defines health probe configuration.
      type: object
      properties:
        path:
          description: Path for HTTP GET probe.
          type: string
        port:
          description: Port for the probe.
          type: integer
          format: int32
        initialDelaySeconds:
          description: Initial delay in seconds.
          type: integer
          format: int32
        periodSeconds:
          description: Period between probes in seconds.
          type: integer
          format: int32
        failureThreshold:
          description: Number of consecutive failures before unhealthy.
          type: integer
          format: int32
        timeoutSeconds:
          description: Timeout for each probe in seconds.
          type: integer
          format: int32
    coreweave.sandbox.v1beta2.RunnerProfileBinding:
      description: "RunnerProfileBinding associates a profile template with a runner. Bindings\n are embedded\
        \ on Runner and mutated only via CreateManagedRunner / UpdateManagedRunner;\n they are not independently\
        \ addressable."
      type: object
      properties:
        id:
          description: Server-assigned unique identifier (UUID).
          type: string
          readOnly: true
        profileTemplateId:
          description: Profile template DB ID (FK).
          type: string
        profileName:
          description: Profile name on this runner (overrides template name if set).
          type: string
        isDefault:
          description: Whether this is the default profile for the runner.
          type: boolean
        overridesJson:
          description: Per-binding overrides (JSON-encoded ProfileSpec fragment).
          type: string
        createdAt:
          description: Timestamps.
          type: string
          format: date-time
          readOnly: true
        updatedAt:
          type: string
          format: date-time
          readOnly: true
      required:
      - profileTemplateId
    coreweave.sandbox.v1beta2.RunnerResourceRequirements:
      description: RunnerResourceRequirements defines CPU/memory requests and limits.
      type: object
      properties:
        cpuRequest:
          type: string
        memoryRequest:
          type: string
        cpuLimit:
          type: string
        memoryLimit:
          type: string
    coreweave.sandbox.v1beta2.RunnerResourceSummary:
      description: "RunnerResourceSummary exposes dynamic resource availability.\n Only populated for\
        \ runners owned by the caller's organization.\n\n available_cpu_millicores and available_memory_bytes\
        \ are usually the measured\n availability, but for a short window after the runner's capacity\
        \ changes they\n may instead be reported at the runner's advertised ceiling while that ceiling\n\
        \ is being republished. In that window a value derived as ceiling minus\n available can read zero\
        \ even though the runner has usage. available_gpu_count\n is always the measurement.\n\n When\
        \ comparing with capacity ceilings, use capabilities from the same\n response when present. The\
        \ values need not reflect the same measurement time."
      type: object
      properties:
        availableCpuMillicores:
          description: "Measured available CPU in millicores, or the advertised CPU ceiling during\n the\
            \ window described above."
          type: string
        availableMemoryBytes:
          description: "Measured available memory in bytes, or the advertised memory ceiling during\n\
            \ the window described above."
          type: string
        availableGpuCount:
          description: Measured available GPUs; never adjusted to a ceiling.
          type: string
        runningSandboxes:
          type: integer
          format: int32
    coreweave.sandbox.v1beta2.RunnerScalingConfig:
      description: RunnerScalingConfig defines scaling parameters for a runner deployment.
      type: object
      properties:
        replicas:
          description: Number of replicas (when autoscaling is disabled).
          type: integer
          format: int32
        autoscalingEnabled:
          description: Whether autoscaling is enabled.
          type: boolean
        minReplicas:
          description: Minimum replicas when autoscaling.
          type: integer
          format: int32
        maxReplicas:
          description: Maximum replicas when autoscaling.
          type: integer
          format: int32
    coreweave.sandbox.v1beta2.RunnerTenantMetricsConfig:
      description: "RunnerTenantMetricsConfig toggles the tenant-metrics collector DaemonSet\n on a managed\
        \ runner's cluster. The collector reads the node-local kubelet\n and re-exports per-sandbox usage\
        \ attributed to the tenant org. Sandman\n projects this config onto the resolved deployment env\
        \ as canonical\n \"true\"/\"false\" strings, so typo-prone free-form env values never gate\n the\
        \ feature."
      type: object
      properties:
        enabled:
          description: Enable the tenant-metrics collector for this runner's cluster.
          type: boolean
        image:
          description: "Collector image, release-pinned (e.g.\n \"coreweave.jfrog.io/cw-sandbox-oci/cwsandbox-metrics-collector:v0.140.0\"\
            ).\n When empty, an image already present in the deployment env (zone\n default) applies;\
            \ the controller holds and alerts if no image resolves."
          type: string
    coreweave.sandbox.v1beta2.RunnerToleration:
      description: RunnerToleration defines a Kubernetes toleration.
      type: object
      properties:
        key:
          type: string
        operator:
          type: string
        value:
          type: string
        effect:
          type: string
    coreweave.sandbox.v1beta2.RunnerVolumeMount:
      description: RunnerVolumeMount defines a volume mount for a runner pod.
      type: object
      properties:
        mountPath:
          description: Mount path inside the container.
          type: string
        name:
          description: Volume name.
          type: string
        readOnly:
          description: Whether the volume is read-only.
          type: boolean
        subPath:
          description: Sub-path within the volume.
          type: string
        configMapName:
          type: string
        secretName:
          type: string
        emptyDir:
          type: boolean
    coreweave.sandbox.v1beta2.RunnerVolumesConfig:
      description: "RunnerVolumesConfig toggles registered-Volume (PVC) mounts on a managed\n runner.\
        \ Enabling is necessary but not sufficient: the runner advertises\n supports_volumes only after\
        \ its startup PVC/PV RBAC preflight passes,\n which requires the zone's runner-controller to grant\
        \ the volume RBAC\n (--enable-volumes-rbac). A runner that is toggled on but lacks RBAC keeps\n\
        \ rejecting volume operations with an actionable error."
      type: object
      properties:
        enabled:
          description: Enable registered-Volume mounts on this runner.
          type: boolean
        csiDriverAllowlist:
          description: "CSI drivers allowed to back registered Volumes on this runner. Empty =\n the platform\
            \ default allowlist (csi.vastdata.com). Entries are driver names\n as registered in the cluster\
            \ (e.g. \"csi.vastdata.com\")."
          type: array
          items:
            type: string
    coreweave.sandbox.v1beta2.S3Mount:
      description: S3Mount describes an object-storage mount. Not yet implemented.
      type: object
      properties:
        bucket:
          type: string
        directory:
          type: string
        mountPath:
          type: string
      required:
      - bucket
      - directory
      - mountPath
    coreweave.sandbox.v1beta2.SandboxFileSystemMount:
      description: "SandboxFileSystemMount describes a scratch filesystem mounted into the\n sandbox.\
        \ V1 implements File System Snapshot-backed EmptyDir semantics;\n live/shared filesystem sources\
        \ are reserved for a future product shape."
      type: object
      properties:
        mountPath:
          type: string
        size:
          type: string
        fileSystemSnapshot:
          $ref: '#/components/schemas/coreweave.sandbox.v1beta2.FileSystemSnapshotSource'
      required:
      - mountPath
    coreweave.sandbox.v1beta2.SandboxInfo:
      description: SandboxInfo contains basic information about a sandbox.
      type: object
      properties:
        sandboxId:
          type: string
        startedAtTime:
          type: string
          format: date-time
        sandboxStatus:
          type: string
          format: enum
          enum:
          - SANDBOX_STATUS_UNSPECIFIED
          - SANDBOX_STATUS_CREATING
          - SANDBOX_STATUS_RUNNING
          - SANDBOX_STATUS_COMPLETED
          - SANDBOX_STATUS_FAILED
          - SANDBOX_STATUS_TERMINATED
          - SANDBOX_STATUS_PENDING
          - SANDBOX_STATUS_PAUSED
          - SANDBOX_STATUS_TERMINATING
        currentResourceUsage:
          $ref: '#/components/schemas/coreweave.sandbox.v1beta2.ResourceUsage'
        runnerId:
          type: string
        runnerGroupId:
          type: string
        profileId:
          type: string
        serviceAddress:
          type: string
        exposedPorts:
          type: array
          items:
            $ref: '#/components/schemas/coreweave.sandbox.v1beta2.Port'
        appliedIngressMode:
          type: string
        appliedEgressMode:
          type: string
        userId:
          description: "ID of the user that created the sandbox, as recorded from the\n authenticated\
            \ identity at create time. Lets an org admin listing\n org-wide attribute each sandbox to\
            \ its owner. May be empty for\n sandboxes created before this field was introduced."
          type: string
    coreweave.sandbox.v1beta2.SecretMapping:
      description: SecretMapping maps a provider-specific secret path to an environment variable.
      type: object
      properties:
        path:
          description: Provider-specific secret identifier (e.g., "HF_TOKEN", "secret/data/myapp/db").
          type: string
        field:
          description: Optional field within a structured secret (for key-value secrets).
          type: string
        envVar:
          description: Environment variable name for delivery into the sandbox container.
          type: string
    coreweave.sandbox.v1beta2.SecretStore:
      description: "SecretStore represents an org-level secret store configuration.\n Stores define connections\
        \ to external secrets providers (W&B, AWS, GCP, etc.)."
      type: object
      properties:
        id:
          description: Server-generated unique identifier.
          type: string
          readOnly: true
        organizationId:
          description: Organization that owns this store (from auth context).
          type: string
          readOnly: true
        name:
          description: "User-provided name, unique within the organization.\n Must match pattern: ^[a-z][a-z0-9-]{2,62}$"
          type: string
        providerType:
          description: Provider type.
          type: string
          format: enum
          enum:
          - SECRET_STORE_PROVIDER_TYPE_UNSPECIFIED
          - SECRET_STORE_PROVIDER_TYPE_WANDB
        wandb:
          $ref: '#/components/schemas/coreweave.sandbox.v1beta2.WandBStoreConfig'
        createdAt:
          description: Server-generated timestamps.
          type: string
          format: date-time
          readOnly: true
        updatedAt:
          type: string
          format: date-time
          readOnly: true
    coreweave.sandbox.v1beta2.SecretStoreReference:
      description: "SecretStoreReference groups secret mappings by store name.\n Clients include these\
        \ in StartSandboxRequest to request secret injection."
      type: object
      properties:
        storeName:
          description: "Name of a secret store (resolved server-side). W&B-authenticated callers\n may\
            \ use the built-in identity-backed store name \"wandb\" without creating a\n SecretStore row;\
            \ all other names are resolved from configured SecretStores."
          type: string
        secrets:
          description: Secrets to fetch from this store and inject into the sandbox.
          type: array
          items:
            $ref: '#/components/schemas/coreweave.sandbox.v1beta2.SecretMapping'
    coreweave.sandbox.v1beta2.ServiceExposureMode:
      description: ServiceExposureMode describes a supported service exposure mode.
      type: object
      properties:
        name:
          type: string
    coreweave.sandbox.v1beta2.SetFileSystemSnapshotBucketConfigRequest:
      type: object
      properties:
        bucketName:
          description: Bring-your-own bucket name. Empty reverts the org to CoreWeave-managed (full-replace
            PUT).
          type: string
        region:
          description: Object-store region for the bring-your-own bucket. Required iff bucket_name is
            set.
          type: string
    coreweave.sandbox.v1beta2.SetObjectStorageWIFConfigRequest:
      type: object
      properties:
        wifConfigId:
          description: The WIF config ID from CoreWeave Cloud Console.
          type: string
        enabled:
          description: "Whether object storage access is enabled.\n When omitted, defaults to true (enabled).\
            \ Use `false` to explicitly disable."
          type: boolean
        allowedBuckets:
          description: "Bucket names the organization is allowed to access.\n Empty list means all buckets\
            \ are allowed."
          type: array
          items:
            type: string
        maxPermission:
          description: Maximum permission level for sandboxes. Must be READ or READ_WRITE.
          type: string
          format: enum
          enum:
          - OBJECT_STORAGE_PERMISSION_UNSPECIFIED
          - OBJECT_STORAGE_PERMISSION_READ
          - OBJECT_STORAGE_PERMISSION_READ_WRITE
      required:
      - wifConfigId
      - maxPermission
    coreweave.sandbox.v1beta2.StartSandboxRequest:
      description: StartSandboxRequest launches a new sandbox.
      type: object
      properties:
        command:
          type: string
        args:
          type: array
          items:
            type: string
        tags:
          type: array
          items:
            type: string
        resources:
          $ref: '#/components/schemas/coreweave.sandbox.v1beta2.ResourceRequest'
        containerImage:
          type: string
        environmentVariables:
          type: object
          additionalProperties:
            type: string
        ports:
          type: array
          items:
            $ref: '#/components/schemas/coreweave.sandbox.v1beta2.Port'
        mountedFiles:
          type: array
          items:
            $ref: '#/components/schemas/coreweave.sandbox.v1beta2.MountedFile'
        s3Mount:
          $ref: '#/components/schemas/coreweave.sandbox.v1beta2.S3Mount'
        network:
          $ref: '#/components/schemas/coreweave.sandbox.v1beta2.NetworkOptions'
        fileSystem:
          $ref: '#/components/schemas/coreweave.sandbox.v1beta2.SandboxFileSystemMount'
        profileIds:
          type: array
          items:
            type: string
        runnerIds:
          type: array
          items:
            type: string
        profileNames:
          type: array
          items:
            type: string
        maxLifetimeSeconds:
          type: integer
          format: int32
        maxTimeoutSeconds:
          type: integer
          format: int32
        runnerClusterSecrets:
          type: array
          items:
            $ref: '#/components/schemas/coreweave.sandbox.v1beta2.RunnerClusterSecretReference'
        objectStorageAccess:
          $ref: '#/components/schemas/coreweave.sandbox.v1beta2.ObjectStorageAccess'
        podAnnotations:
          type: object
          additionalProperties:
            type: string
        secretStores:
          type: array
          items:
            $ref: '#/components/schemas/coreweave.sandbox.v1beta2.SecretStoreReference'
        resourceLimits:
          $ref: '#/components/schemas/coreweave.sandbox.v1beta2.ResourceRequest'
        resourceRequests:
          $ref: '#/components/schemas/coreweave.sandbox.v1beta2.ResourceRequest'
        volumes:
          type: array
          items:
            $ref: '#/components/schemas/coreweave.sandbox.v1beta2.VolumeAttachment'
      required:
      - command
      - containerImage
    coreweave.sandbox.v1beta2.StartSandboxResponse:
      description: StartSandboxResponse returns identifiers and metadata for a started sandbox.
      type: object
      properties:
        sandboxId:
          type: string
        startedAtTime:
          type: string
          format: date-time
        serviceAddress:
          type: string
        exposedPorts:
          type: array
          items:
            $ref: '#/components/schemas/coreweave.sandbox.v1beta2.Port'
        requestedResources:
          $ref: '#/components/schemas/coreweave.sandbox.v1beta2.ResourceRequest'
        profileId:
          type: string
        runnerId:
          type: string
        sandboxStatus:
          type: string
          format: enum
          enum:
          - SANDBOX_STATUS_UNSPECIFIED
          - SANDBOX_STATUS_CREATING
          - SANDBOX_STATUS_RUNNING
          - SANDBOX_STATUS_COMPLETED
          - SANDBOX_STATUS_FAILED
          - SANDBOX_STATUS_TERMINATED
          - SANDBOX_STATUS_PENDING
          - SANDBOX_STATUS_PAUSED
          - SANDBOX_STATUS_TERMINATING
        appliedIngressMode:
          type: string
        appliedEgressMode:
          type: string
        requestedResourceLimits:
          $ref: '#/components/schemas/coreweave.sandbox.v1beta2.ResourceRequest'
        requestedResourceRequests:
          $ref: '#/components/schemas/coreweave.sandbox.v1beta2.ResourceRequest'
    coreweave.sandbox.v1beta2.StopSandboxRequest:
      description: StopSandboxRequest terminates a running sandbox.
      type: object
      properties:
        sandboxId:
          type: string
        gracefulShutdownSeconds:
          type: integer
          format: int32
        fileSystemSnapshotOnStop:
          type: boolean
        maxTimeoutSeconds:
          type: integer
          format: int32
        idempotencyKey:
          type: string
        waitForReady:
          type: boolean
      required:
      - sandboxId
    coreweave.sandbox.v1beta2.StopSandboxResponse:
      description: StopSandboxResponse indicates success or failure of stopping a sandbox.
      type: object
      properties:
        success:
          type: boolean
        errorMessage:
          type: string
        fileSystemSnapshotId:
          type: string
    coreweave.sandbox.v1beta2.VolumeAttachment:
      description: "VolumeAttachment mounts a registered Volume (an org-registered shared\n storage resource,\
        \ managed via the v1 VolumeService) into the sandbox.\n Mounts are live views of the shared backing\
        \ data: writes are immediately\n visible to every other mounter. A Volume with a cluster-local\
        \ source pins\n scheduling to the runner that owns it."
      type: object
      properties:
        volumeId:
          description: The registered Volume to mount.
          type: string
        mountPath:
          description: Absolute path to mount at inside the sandbox container.
          type: string
        subPath:
          description: "Relative path inside the volume to mount instead of its root — the\n per-sandbox\
            \ isolation knob. Composed under the volume source's own\n sub_path. Must be relative and\
            \ canonical (no \".\" / \"..\")."
          type: string
        readOnly:
          description: "Mount read-only. The volume-level read_only flag is a floor: when it is\n true\
            \ every mount is read-only regardless of this field."
          type: boolean
      required:
      - volumeId
      - mountPath
    coreweave.sandbox.v1beta2.WandBStoreConfig:
      description: WandBStoreConfig holds configuration for a Weights & Biases secret store.
      type: object
      properties:
        apiUrl:
          description: Base URL for the W&B API (e.g., "https://api.wandb.ai").
          type: string
        team:
          description: Optional W&B team/entity scope.
          type: string
    google.protobuf.Any:
      description: Contains an arbitrary serialized message along with a @type that describes the type
        of the serialized message.
      type: object
      properties:
        '@type':
          description: The type of the serialized message.
          type: string
      additionalProperties: true
    google.rpc.Status:
      description: 'The `Status` type defines a logical error model that is suitable for different programming
        environments, including REST APIs and RPC APIs. It is used by [gRPC](https://github.com/grpc).
        Each `Status` message contains three pieces of data: error code, error message, and error details.
        You can find out more about this error model and how to work with it in the [API Design Guide](https://cloud.google.com/apis/design/errors).'
      type: object
      properties:
        code:
          description: The status code, which should be an enum value of [google.rpc.Code][google.rpc.Code].
          type: integer
          format: int32
        message:
          description: A developer-facing error message, which should be in English. Any user-facing error
            message should be localized and sent in the [google.rpc.Status.details][google.rpc.Status.details]
            field, or localized by the client.
          type: string
        details:
          description: A list of messages that carry the error details.  There is a common set of message
            types for APIs to use.
          type: array
          items:
            $ref: '#/components/schemas/google.protobuf.Any'
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
      description: CoreWeave API access token sent as a bearer token.
      x-default: Bearer {API_ACCESS_TOKEN}
tags:
- name: NetworkConfigService
  description: Create, get, list, update, and delete desired network configurations. Updating a configuration
    bound to a running sandbox changes its network rules without a restart. Requires API enablement and
    a runner with live network update support.
- name: SandboxService
  description: 'Endpoints for the sandbox lifecycle: create (directly, from a template, or from a Compose
    file), get, list, exec, read and write files, snapshot, connect, purge, and delete.'
- name: DiscoveryService
  description: Read-only endpoints for discovering the runners visible to the caller's organization, with
    view, capability, and service-visibility filters. Runner IDs are unique only within an organization.
- name: SettingsService
  description: 'Organization-level sandbox settings: the object-storage Workload Identity Federation (WIF)
    configuration, the file-system snapshot bucket configuration, Compose build storage, and secret stores.'
- name: VolumeService
  description: CRUD operations for organization-registered volumes that sandboxes can mount, plus the
    validation call that confirms a volume's backing source is usable.
- name: RunnerManagementService
  description: CRUD operations for managed runners and the runner policy each one carries. Policy is a
    field on the runner, mutated through `CreateManagedRunner` and `UpdateManagedRunner`.
- name: SandboxTemplateService
  description: CRUD operations for organization-scoped sandbox templates, the partial specs that `CreateSandboxFromTemplate`
    merges with per-request overrides.
security:
- bearerAuth: []
```
