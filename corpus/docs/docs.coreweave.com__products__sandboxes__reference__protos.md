# Protobuf

Source: https://docs.coreweave.com/products/sandboxes/reference/protos

# Protobuf

> Find CoreWeave Sandboxes Protobuf definitions, service hosts, and generated software development kits (SDKs).

You can find the Protobuf definitions for the CoreWeave Sandboxes API in the Buf module at [`buf.build/coreweave/sandbox`](https://buf.build/coreweave/sandbox). Use them when you integrate from a language that has no first-party CoreWeave client. You can also use them for a remote procedure call (RPC) that the Python client or the TypeScript client (`@coreweave/cwsandbox`) doesn't expose.

The module page lists the service and field definitions. Use `coreweave.sandbox.v1` for new integrations. The earlier `coreweave.sandbox.v1beta2` package is still served for existing clients, and also carries profile templates and runner enrollment.

## Endpoints

Every RPC is served over the [Connect protocol](https://connectrpc.com/), and the same endpoints accept gRPC and gRPC-Web clients. The `v1` services are split across two hosts, plus a logical-runner endpoint for direct connections with sandbox-scoped credentials:

| Host | Serves |
| - | - |
| `https://api.cwsandbox.com` | `SandboxService`, `DiscoveryService`, `VolumeService`, `NetworkConfigService`, `NetworkService`, and `SettingsService`. |
| `https://api.coreweave.com` | `RunnerManagementService` and `SandboxTemplateService`. |
| Direct logical-runner data-plane endpoint | `SandboxDataPlaneService`. `SandboxService.ConnectSandbox` returns the endpoint URI, a short-lived client certificate, and a trust bundle. |

`NetworkService` isn't available yet: every RPC returns `UNIMPLEMENTED` with reason `CWSANDBOX_NOT_IMPLEMENTED`. More generally, RPC availability depends on the organization, deployment, and [placement mode](https://docs.coreweave.com/products/sandboxes/placement.md#compare-placement-modes). Other unimplemented RPCs can return `UNIMPLEMENTED` without that structured reason. Inspect the RPC code and any error details.

`PlacementOrgConfigService` remains registered on `api.coreweave.com` for legacy cleanup. Its configuration is no longer enforced: `UpdatePlacementOrgConfig` returns `UNIMPLEMENTED`, while Get and Delete remain available to inspect and remove legacy rows. These calls require `sandbox_admin` and target the caller's own placement organization. This service is excluded from the supported REST reference.

`NetworkConfigService` manages [dynamic network configurations](https://docs.coreweave.com/products/sandboxes/reference/network-configs.md). Its [availability prerequisites](https://docs.coreweave.com/products/sandboxes/reference/network-configs.md#availability-and-prerequisites) include API enablement and runner support for live updates.

Requests to `api.cwsandbox.com` and `api.coreweave.com` authenticate with a CoreWeave API access token. For how to create one and grant the `sandbox_user` or `sandbox_admin` identity and access management (IAM) action, see [Authentication](https://docs.coreweave.com/products/sandboxes/reference/control-plane-api.md#authentication).

The direct logical-runner data-plane endpoint uses mutual Transport Layer Security (TLS) with the sandbox-scoped client certificate and trust bundle returned by `ConnectSandbox`. It doesn't use the API bearer token.

## Install a generated SDK

The Buf Schema Registry builds SDKs for the module on demand. The following commands install common language and plugin combinations:

```bash title="Install a generated SDK" theme={"system"}
# Go: Connect clients and message types
go get buf.build/gen/go/coreweave/sandbox/connectrpc/go@latest
go get buf.build/gen/go/coreweave/sandbox/protocolbuffers/go@latest

# Python: message types and gRPC stubs
pip install coreweave-sandbox-protocolbuffers-python coreweave-sandbox-grpc-python \
  --extra-index-url https://buf.build/gen/python

# TypeScript: message types, paired with @connectrpc/connect
npm config set @buf:registry https://buf.build/gen/npm/v1/
npm install @buf/coreweave_sandbox.bufbuild_es
```

For every other language and plugin combination, see the [SDKs tab](https://buf.build/coreweave/sandbox/sdks) on the module page.

### Generate code locally

To generate code locally, follow these steps:

1. [Configure a `buf.gen.yaml` file](https://buf.build/docs/generate/) with the plugins to run and their output directories.
2. From the directory containing that file, run:

   ```bash theme={"system"}
   buf generate buf.build/coreweave/sandbox
   ```

## Read failed Compose build logs

For a failed service build from [Create a sandbox from a Compose file](https://docs.coreweave.com/products/sandboxes/create-from-file.md), call `SandboxService.GetSandboxBuildLogs()` over Connect. Replace `API_ACCESS_TOKEN`, `SANDBOX_ID_VALUE`, and `SERVICE_NAME` with your API access token, sandbox ID, and Compose service name:

```bash title="Get a failed build log link" theme={"system"}
curl -X POST "https://api.cwsandbox.com/coreweave.sandbox.v1.SandboxService/GetSandboxBuildLogs" \
  -H "Authorization: Bearer API_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -H "Connect-Protocol-Version: 1" \
  -d '{"sandboxId": "SANDBOX_ID_VALUE", "service": "SERVICE_NAME"}'
```

The response contains a temporary download `url` and its `expireTime`. Download from that URL without sending your API access token. The REST binding returns `302 Found` with the URL in the `Location` header and no response body.

## See also

For related guidance, see the following pages:

* [Sandboxes architecture](https://docs.coreweave.com/products/sandboxes/architecture.md): how the gateway brokers runtime requests, and the control plane and data plane split.
* [API overview](https://docs.coreweave.com/products/sandboxes/reference/control-plane-api.md): authentication, pagination, field masks, and error handling for the control plane.
* [Sandboxes Python client](https://docs.coreweave.com/products/sandboxes/client.md): the higher-level `cwsandbox` client built on this API.
* [Direct sandbox connections](https://docs.coreweave.com/products/sandboxes/client/guides/direct-connections.md): how a client reaches `SandboxDataPlaneService` over mutual TLS.
