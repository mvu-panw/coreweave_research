# Direct sandbox connections

Source: https://docs.coreweave.com/products/sandboxes/client/guides/direct-connections

# Direct sandbox connections

> Route exec, log, and file operations over direct mutual Transport Layer Security (mTLS), bypassing the gateway.

A direct sandbox connection carries exec, log, and file operations from your client to the logical runner hosting the sandbox over mTLS. These operations bypass the CoreWeave Sandboxes gateway. Removing the gateway hop lowers latency and raises throughput for workloads that move large amounts of data in and out of a sandbox.

Lifecycle and management operations, such as starting a sandbox, listing sandboxes, and stopping one, always use the CoreWeave Sandboxes API. A direct connection applies only to data operations on a sandbox that's already running.

This page is for developers who use the `cwsandbox` Python software development kit (SDK) to launch and manage sandboxes. It explains how to choose a transport policy for data operations and how the SDK establishes a direct connection. It also explains how to confirm which transport an operation used.

## Choose authentication

These examples run on serverless capacity unless a section specifies CoreWeave Kubernetes Service (CKS). Choose the credential for the account that owns your sandboxes. See [Choose and get credentials](https://docs.coreweave.com/products/sandboxes/placement.md#choose-and-get-credentials) to obtain a key or token.

Run the installation commands in an [active Python virtual environment](https://docs.coreweave.com/products/sandboxes/client.md#prepare-your-python-environment).

Save the Python code from your credential tab as the `sandbox_auth.py` file beside the Python scripts you run from this page. It stores the authentication choice, not your credential. The examples import `AUTH` from that file and pass it explicitly to each new sandbox or session.

> [tab] Forge API key
>
> Use your Forge API key through the SDK's W\&B authentication strategy. Replace `WANDB_API_KEY_VALUE` with your API key:
>
> ```bash theme={"system"}
> uv pip install 'cwsandbox[wandb]>=1.14.2'
> export WANDB_API_KEY="WANDB_API_KEY_VALUE"
> ```
>
> ```python title="sandbox_auth.py" theme={"system"}
> from cwsandbox import AuthStrategy
>
> AUTH = AuthStrategy.WANDB
> ```

> [tab] CoreWeave API access token
>
> Use the token for your CoreWeave organization. Replace `API_ACCESS_TOKEN` with that token:
>
> ```bash theme={"system"}
> uv pip install 'cwsandbox>=1.14.2'
> export CWSANDBOX_API_KEY="API_ACCESS_TOKEN"
> ```
>
> ```python title="sandbox_auth.py" theme={"system"}
> from cwsandbox import AuthStrategy
>
> AUTH = AuthStrategy.COREWEAVE_API_KEY
> ```

For CKS placement, choose the CoreWeave token, [enable a runner](https://docs.coreweave.com/products/sandboxes/get-started-cks.md), and set `placement_mode="cks"` on sandbox creation or in `SandboxDefaults`. Creating a session with `auth=AUTH` also authenticates the sandboxes it owns. Keep the same credential when reconnecting, listing, or cleaning up sandboxes.

## Overview

The `DataPlaneMode` enum sets the transport policy for data operations. The SDK uses `AUTO` unless you choose otherwise, so most callers get direct connections without changing any code.

| Mode | Behavior | When to use it |
| - | - | - |
| `AUTO` | Prefers a direct mTLS connection and transparently falls back to the gateway when direct access is unavailable. | The default. Use it unless you need to pin one transport. |
| `DIRECT` | Requires the direct mTLS connection and raises an error when it can't be established. | Validating that direct connectivity works in your environment. |
| `GATEWAY` | Always routes data operations through the gateway. | A deterministic rollback path when you need to rule out the direct transport. |

## Set the transport policy

To set the transport policy for a single sandbox, pass `data_plane_mode` to `Sandbox.run()`. To set it for a group of sandboxes, pass `data_plane_mode` to `SandboxDefaults`.

```python theme={"system"}
from sandbox_auth import AUTH
from cwsandbox import DataPlaneMode, Sandbox, SandboxDefaults

# AUTO is the default: prefer direct, fall back to the gateway.
with Sandbox.run(resources={"cpu": "1", "memory": "1Gi"}, auth=AUTH) as sandbox:
    result = sandbox.exec(["echo", "hello"]).result()
    print(result.stdout)

# Require the direct path. Useful when validating connectivity.
with Sandbox.run(
    data_plane_mode=DataPlaneMode.DIRECT,
    resources={"cpu": "1", "memory": "1Gi"},
    auth=AUTH,
) as sandbox:
    print(sandbox.read_file("/etc/hostname").result().decode())

# Force the gateway path for every sandbox that uses these defaults.
defaults = SandboxDefaults(
    data_plane_mode=DataPlaneMode.GATEWAY,
    resources={"cpu": "1", "memory": "1Gi"},
)
with Sandbox.run(defaults=defaults, auth=AUTH) as sandbox:
    print(sandbox.exec(["echo", "gateway"]).result().stdout)
```

## How a direct connection is established

When a sandbox is running and you issue its first data operation, the SDK generates a P-256 private key in memory. It sends only a certificate signing request to the CoreWeave Sandboxes API. The API returns a certificate scoped to that sandbox. The SDK uses it to open an mTLS connection to the logical runner's data-plane endpoint. Sandboxes on that logical runner share the endpoint. The certificate scopes access to the requested sandbox.

The credential exchange has the following properties:

* The private key never leaves the client process. The SDK transmits a certificate signing request, not the key.
* Your API bearer token is never sent to the sandbox data endpoint. The logical runner authenticates the client with the sandbox-scoped certificate.

The SDK creates credentials lazily, so a sandbox that only ever runs lifecycle calls never requests them. The SDK uses the certificate expiry that the server issues rather than imposing a shorter session lifetime of its own.

## Timing and fallback

`AUTO` and `DIRECT` differ in how long they wait and in what happens when setup doesn't finish in time.

* In `AUTO`, credential issuance plus channel readiness share a 1-second budget. If that budget runs out, the operation proceeds over the gateway. The SDK waits 30 seconds before attempting a direct connection again. The gateway attempt can still fail with an operation or transport error.
* In `DIRECT`, connection setup gets up to 10 seconds, with no fallback. If setup doesn't complete, the operation raises an error.

A `PERMISSION_DENIED` or `UNAUTHENTICATED` error from credential issuance fails in both modes. If a direct certificate lacks permission for an operation, `AUTO` can use the gateway.

## Connection reuse

The SDK keeps a process-wide pool of idle direct channels, bounded at 64. Bounding the pool means a program holding a large collection of inactive sandbox objects doesn't retain one socket per sandbox.

An active stream keeps the channel it started on. When a channel is marked stale, existing streams drain on it while new calls create a replacement channel.

## Verify which transport an operation used

To confirm that direct connectivity works from your environment, run an operation under `DIRECT`. Because that mode never falls back, an operation that returns successfully used the direct transport. An operation that can't establish the connection raises an error instead of silently using the gateway.

```python theme={"system"}
from sandbox_auth import AUTH
from cwsandbox import DataPlaneMode, Sandbox

with Sandbox.run(
    data_plane_mode=DataPlaneMode.DIRECT,
    resources={"cpu": "1", "memory": "1Gi"},
    auth=AUTH,
) as sandbox:
    result = sandbox.exec(["echo", "direct"]).result()
    print(result.stdout)
```

If this raises an error while the same call under `GATEWAY` succeeds, inspect the error before choosing a transport. A connection timeout can indicate that your client can't reach the logical runner's data-plane endpoint. Check egress restrictions on that path. `AUTO` permits gateway fallback for unavailable direct connections, subject to the exceptions in [Timing and fallback](#timing-and-fallback).

## See also

For related guidance, see the following pages:

* [Sandboxes architecture](https://docs.coreweave.com/products/sandboxes/architecture.md): how the control plane, gateway, and runners fit together.

* [Execution](https://docs.coreweave.com/products/sandboxes/client/guides/execution.md): running commands in a sandbox.

* [File operations](https://docs.coreweave.com/products/sandboxes/client/guides/file-operations.md): reading and writing files in a sandbox.

* [Sandbox configuration](https://docs.coreweave.com/products/sandboxes/client/guides/sandbox-configuration.md): the other options you can set through `SandboxDefaults` and `Sandbox.run()`.
