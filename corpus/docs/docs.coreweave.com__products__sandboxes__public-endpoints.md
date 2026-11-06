# Public endpoints

Source: https://docs.coreweave.com/products/sandboxes/public-endpoints

# Public endpoints

> Give a service inside a sandbox a public address, with platform TLS or TLS passthrough.

This page describes how public endpoints work, how to declare one when you create a sandbox, and how to connect to it.

A public endpoint gives a service running inside a sandbox an address that clients can reach from the internet. You request one when you create the sandbox, and the platform provisions the routing, DNS, and network access for it. The address belongs to the sandbox for as long as the sandbox runs.

Endpoints come in two kinds, which differ in where TLS terminates:

* **HTTPS**: The platform terminates TLS at its edge with a certificate it provisions and renews, then forwards the request to your port as cleartext HTTP.
* **TLS passthrough**: The platform routes the connection to your port by [Server Name Indication (SNI)](https://en.wikipedia.org/wiki/Server_Name_Indication) without decrypting it. Your workload terminates TLS and owns its own certificates.

Choose TLS passthrough when the workload must hold the private key itself: mutual TLS, a client that pins a certificate, or a protocol that isn't HTTP.

## Choose authentication

These examples run on serverless capacity unless a section specifies CoreWeave Kubernetes Service (CKS). Choose the credential for the account that owns your sandboxes. See [Choose and get credentials](https://docs.coreweave.com/products/sandboxes/placement.md#choose-and-get-credentials) to obtain a key or token.

Save the configuration for your language beside the scripts you run from this page. Python examples import `AUTH` from `sandbox_auth.py`. TypeScript examples import `client` from `sandbox-client.mts`. These files select authentication without storing your credential. For Python, use an [active virtual environment](https://docs.coreweave.com/products/sandboxes/client.md#prepare-your-python-environment). For TypeScript, first install the client with `npm install @coreweave/cwsandbox@1.0.0`.

> [tab] Forge API key
>
> Use your Forge API key with the SDK's `wandb` integration. Replace `[WANDB-API-KEY]` with your API key:
>
> ```bash theme={"system"}
> export WANDB_API_KEY="[WANDB-API-KEY]"
> ```
>
> > [tab] Python
> >
> > ```bash theme={"system"}
> > uv pip install 'cwsandbox[wandb]>=1.16.0'
> > ```
> >
> > ```python title="sandbox_auth.py" theme={"system"}
> > from cwsandbox import AuthStrategy
> >
> > AUTH = AuthStrategy.WANDB
> > ```
>
> > [tab] TypeScript
> >
> > ```typescript title="sandbox-client.mts" theme={"system"}
> > import { createSandboxClientFromEnv } from "@coreweave/cwsandbox/wandb";
> >
> > export const client = createSandboxClientFromEnv();
> > ```

> [tab] CoreWeave API access token
>
> Use the token for your CoreWeave organization. Replace `[API-ACCESS-TOKEN]` with your token:
>
> ```bash theme={"system"}
> export CWSANDBOX_API_KEY="[API-ACCESS-TOKEN]"
> ```
>
> > [tab] Python
> >
> > ```bash theme={"system"}
> > uv pip install 'cwsandbox>=1.16.0'
> > ```
> >
> > ```python title="sandbox_auth.py" theme={"system"}
> > from cwsandbox import AuthStrategy
> >
> > AUTH = AuthStrategy.COREWEAVE_API_KEY
> > ```
>
> > [tab] TypeScript
> >
> > ```typescript title="sandbox-client.mts" theme={"system"}
> > import { createSandboxClientFromEnv } from "@coreweave/cwsandbox/node";
> >
> > export const client = createSandboxClientFromEnv();
> > ```

For CKS placement, choose the CoreWeave token, [enable a runner](https://docs.coreweave.com/products/sandboxes/get-started-cks.md), and set `placement_mode="cks"` on sandbox creation or in `SandboxDefaults`. In TypeScript, choose the CoreWeave token and set a nonempty `runnerIds` array to select CKS. Creating a Python session with `auth=AUTH` also authenticates the sandboxes it owns. Keep the same credential when reconnecting, listing, or cleaning up sandboxes.

The Python share-token example requires `cwsandbox` 1.16.0 or later and a deployment with HTTPS share-token support. The credential you configure in this section authenticates SDK operations such as creating and deleting sandboxes. It's separate from the endpoint share token that callers use to access a protected HTTPS URL.

## Compare the two kinds

| | HTTPS | TLS passthrough |
| - | - | - |
| Terminates TLS | Platform edge | Your workload |
| Owns certificates | Platform | You |
| Carries | HTTP, WebSockets over HTTP Upgrade, and Server-Sent Events | Any protocol over TLS |
| `endpoint.kind` | `HTTPS` | `TLS_PASSTHROUGH` |
| `endpoint.auth` | `OPEN` or `SHARE_TOKEN` (required) | Omit |
| Read the address from | `service_urls` | `service_addresses` |

> [!WARNING]
>
> Both kinds are reachable from the internet. HTTPS with `OPEN` and TLS passthrough have no platform caller authentication. The workload must enforce any access control you need. HTTPS with `SHARE_TOKEN` requires the issued token on each request. Anyone with that token can access the protected endpoint.

## Declare an endpoint

Declare endpoints in the `services` list when you create the sandbox. Ports are fixed for the sandbox's lifetime, and no call exposes a port on a sandbox that is already running.

To give a service a public endpoint, set `visibility=ServiceVisibility.PUBLIC` and an `endpoint` value on it. A plain service has no `endpoint` value. For example, `Service(port=8080, name="web")` leaves visibility and endpoint unset: It declares a container-local port without requesting external exposure. Visibility on a plain service controls reachability through the deployment's service networking. It doesn't request a public HTTPS URL or TLS passthrough address.

To require a token, use `EndpointAuth.SHARE_TOKEN` as shown in [Connect with a share token](#connect-with-a-share-token). For an HTTPS endpoint without platform caller authentication, set `kind=EndpointKind.HTTPS` and `auth=EndpointAuth.OPEN`:

> [tab] Python
>
> ```python theme={"system"}
> from sandbox_auth import AUTH
> from cwsandbox import (
>     Endpoint,
>     EndpointAuth,
>     EndpointKind,
>     Sandbox,
>     Service,
>     ServiceVisibility,
> )
>
> sandbox = Sandbox.run(
>     "python3", "-m", "http.server", "8080",
>     container_image="python:3.11",
>     services=[
>         Service(
>             port=8080,
>             name="web",
>             visibility=ServiceVisibility.PUBLIC,
>             endpoint=Endpoint(kind=EndpointKind.HTTPS, auth=EndpointAuth.OPEN),
>         ),
>     ],
>     resources={"cpu": "1", "memory": "1Gi"},
>     auth=AUTH,
> )
> ```

> [tab] TypeScript
>
> Set `kind: "https"` and `auth: "open"`:
>
> ```typescript theme={"system"}
> import { client } from "./sandbox-client.mts";
>
> const sandbox = await client.run(["python3", "-m", "http.server", "8080"], {
>   containerImage: "python:3.11",
>   services: [
>     {
>       port: 8080,
>       name: "web",
>       visibility: "public",
>       endpoint: { kind: "https", auth: "open" },
>     },
>   ],
> });
> ```

For a TLS passthrough endpoint, set `kind=EndpointKind.TLS_PASSTHROUGH` and leave `auth` unset. Your workload terminates TLS because the platform forwards the connection without decrypting it.

The following examples declare the endpoint for a prepared TLS workload. Replace `[TLS-SERVER-IMAGE]` with a container image that contains Python 3 and your `/srv/serve_tls.py` server. The server must listen on `0.0.0.0:8443` and load a server certificate and matching private key. The examples don't supply the server implementation, certificates, or private key.

Prepare a certificate-provisioning workflow that supplies the certificate and key to your server. For the [validating client](#connect-to-a-tls-passthrough-endpoint), the certificate must cover the platform-assigned hostname. It must also chain to a certificate authority (CA) that the client trusts. If you issue a certificate for the exact hostname, [read the assigned address](#read-the-assigned-address) after sandbox creation and provision the certificate before the server accepts TLS connections.

> [tab] Python
>
> ```python theme={"system"}
> from sandbox_auth import AUTH
> from cwsandbox import (
>     Endpoint,
>     EndpointKind,
>     Sandbox,
>     Service,
>     ServiceVisibility,
> )
>
> sandbox = Sandbox.run(
>     "python3", "/srv/serve_tls.py",
>     container_image="[TLS-SERVER-IMAGE]",
>     services=[
>         Service(
>             port=8443,
>             name="tls",
>             visibility=ServiceVisibility.PUBLIC,
>             endpoint=Endpoint(kind=EndpointKind.TLS_PASSTHROUGH),
>         ),
>     ],
>     resources={"cpu": "1", "memory": "1Gi"},
>     auth=AUTH,
> )
> ```

> [tab] TypeScript
>
> Set `kind: "tls_passthrough"` and omit `auth`:
>
> ```typescript theme={"system"}
> import { client } from "./sandbox-client.mts";
>
> const sandbox = await client.run(["python3", "/srv/serve_tls.py"], {
>   containerImage: "[TLS-SERVER-IMAGE]",
>   services: [
>     {
>       port: 8443,
>       name: "tls",
>       visibility: "public",
>       endpoint: { kind: "tls_passthrough" },
>     },
>   ],
> });
> ```

One sandbox can mix both endpoint kinds, including `OPEN` and `SHARE_TOKEN` HTTPS endpoints. The following rules apply:

* **Ports and names must be unique** across all `services` entries, including names generated for unnamed ports.
* **Entries with an `endpoint` require `visibility=PUBLIC`.** Set `protocol=TCP` or leave `protocol` unset. The platform rejects `UDP` and `SCTP` endpoints.
* **Plain entries without an `endpoint` can leave visibility unset or use `PRIVATE`, `PUBLIC`, or `CUSTOM`.** They can declare `TCP`, `UDP`, or `SCTP`. An unset protocol defaults to `TCP`. Actual exposure depends on deployment capabilities and policy. These fields don't create a public endpoint. For changing the allowed sources of existing `CUSTOM` services, see [Dynamic network policies](https://docs.coreweave.com/products/sandboxes/dynamic-network-policies.md).
* **Don't mix exposed plain services with endpoint entries.** In a sandbox with endpoints, leave visibility unset on any plain service. Without endpoints, use at most one exposed visibility value across plain services.
* **Omit `auth` and `request_timeout_seconds` for TLS passthrough.** In Python, pass `None` rather than `0`. The SDK rejects a set timeout, including `0`.
* **A platform limit caps how many services one sandbox declares.** Operators configure the cap for their deployment.

## Connect with a share token

To require platform authentication for an HTTPS endpoint, set `auth=EndpointAuth.SHARE_TOKEN`. Read `sandbox.endpoint_share_token` from the handle that creates the sandbox, and send its `as_headers()` result with each request. This helper sets the `X-Sandbox-Share-Token` header. The platform checks the token before forwarding the request to your HTTP service.

In TypeScript, set `auth: "share_token"` and send `sandbox.endpointShareToken` in the `X-Sandbox-Share-Token` request header.

The token is returned at creation. Get, list, and `Sandbox.from_id()` don't return it. The original handle retains it across `wait()` and `get_status()`. If the initial response omits it, `sandbox.start().result()` retries recovery on the same create handle. If recovery still returns no token, stop the sandbox and create another.

Keep the token secret: The dictionary returned by `as_headers()` contains the credential. Don't log this dictionary.

The following Python example starts a 5-minute HTTP service behind a protected HTTPS endpoint. It waits for URL assignment and retries authenticated requests while the application and route become ready. After a successful request, it verifies that an anonymous request is rejected. The context manager stops the sandbox when the example exits.

```python theme={"system"}
import time
import urllib.error
import urllib.request

from sandbox_auth import AUTH
from cwsandbox import (
    Endpoint,
    EndpointAuth,
    EndpointKind,
    Sandbox,
    Service,
    ServiceVisibility,
)


def get_status(url, headers=None):
    request = urllib.request.Request(url, headers=headers or {})
    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            return response.status
    except urllib.error.HTTPError as error:
        return error.code


with Sandbox.run(
    "python3", "-m", "http.server", "8080",
    container_image="python:3.11",
    services=[
        Service(
            port=8080,
            name="web",
            visibility=ServiceVisibility.PUBLIC,
            endpoint=Endpoint(kind=EndpointKind.HTTPS, auth=EndpointAuth.SHARE_TOKEN),
        ),
    ],
    resources={"cpu": "1", "memory": "1Gi"},
    max_lifetime_seconds=300,
    auth=AUTH,
) as sandbox:
    token = sandbox.endpoint_share_token
    if token is None:
        sandbox.start().result()
        token = sandbox.endpoint_share_token
    if token is None:
        raise RuntimeError("No share token returned; recreate the sandbox.")

    sandbox.wait()
    deadline = time.monotonic() + 60
    while time.monotonic() < deadline:
        sandbox.get_status()
        if sandbox.service_urls:
            url = sandbox.service_urls[0][2]
            try:
                if get_status(url, token.as_headers()) == 200:
                    break
            except (urllib.error.URLError, TimeoutError, OSError):
                pass
        time.sleep(2)
    else:
        raise TimeoutError("Authenticated request did not succeed within 60 seconds.")

    assert get_status(url) == 401, "Expected anonymous access to be rejected."
    print("Authenticated request: 200; anonymous request: 401")
```

For the same HTTP service with `auth=EndpointAuth.OPEN`, an anonymous request succeeds once the service is ready. No share token is required. To change the auth mode, create a new sandbox. One sandbox can contain both modes, and the token protects only its `SHARE_TOKEN` endpoints.

The generated [Endpoint reference](https://docs.coreweave.com/products/sandboxes/client/ref/networking/endpoints.md) describes Python SDK version 1.14.2, which supports `OPEN` but predates `SHARE_TOKEN`.

## Read the assigned address

The platform assigns the address. You can't choose the hostname or supply your own domain. Read it back from the sandbox rather than constructing it, because the DNS zone differs per cluster and isn't part of the API contract.

TLS passthrough addresses arrive on `service_addresses` as `host:port`, and HTTPS URLs arrive on `service_urls`. The two lists stay separate: A TLS endpoint never appears in `service_urls`.

> [tab] Python
>
> ```python theme={"system"}
> for endpoint in sandbox.service_addresses:
>     print(endpoint.port, endpoint.name, endpoint.address)
> ```

> [tab] TypeScript
>
> TypeScript returns TLS passthrough addresses in `serviceAddresses` and assigned HTTPS URLs in `serviceUrls`. In `@coreweave/cwsandbox` 1.0.0, `serviceEndpoints` also exposes HTTPS metadata as [`HttpsEndpointStatus`](https://docs.coreweave.com/products/sandboxes/typescript-client/ref/network#httpsendpointstatus) entries. These entries include `port`, `name`, `kind`, `auth`, `requestTimeoutSeconds`, and `url`.
>
> An HTTPS entry appears in `serviceEndpoints` only when the API returns an endpoint with `requestTimeoutSeconds` greater than zero. When the API omits the hostname, including for a sandbox in a terminal state, its `url` can be an empty string. `serviceUrls` omits entries without a URL. Each `inspect()` refresh replaces `serviceEndpoints` and `serviceUrls`. Metadata alone doesn't mean an address is available or the application is ready.
>
> To read TLS passthrough addresses, use the sandbox handle from the Declare an endpoint section:
>
> ```typescript theme={"system"}
> for (const endpoint of sandbox.serviceAddresses ?? []) {
>   console.log(endpoint.port, endpoint.name, endpoint.address);
> }
> ```
>
> For HTTPS metadata, refresh the handle and read `serviceEndpoints`:
>
> ```typescript theme={"system"}
> import type { HttpsEndpointStatus } from "@coreweave/cwsandbox";
>
> await sandbox.inspect();
> const endpoints: readonly HttpsEndpointStatus[] = sandbox.serviceEndpoints ?? [];
> for (const endpoint of endpoints) {
>   console.log(
>     endpoint.port,
>     endpoint.name,
>     endpoint.auth,
>     endpoint.requestTimeoutSeconds,
>     endpoint.url || "(no URL)",
>   );
> }
> ```

For TLS passthrough, you should see output similar to the following:

```text theme={"system"}
8443 tls 8443-2f8d41b6-9c3e-4a17-b5d2-7e0a13c64f89.a1b2c3d4.ep2.cwsandbox.com:443
```

The advertised port is the platform's TLS listener port, not the port your process binds inside the sandbox. In this example, the workload listens on `8443` and clients connect to `443`.

The two kinds become readable at different points in the sandbox's startup:

* **A TLS passthrough address is assigned when the sandbox is created**, so it is on the create response and stays available while the sandbox is creating or running.
* **An HTTPS URL is available once its route has a hostname**, while the sandbox is creating or running. Call `get_status()` in Python or `inspect()` in TypeScript in a loop until the URL appears or your own deadline passes.
* **Neither one means the application is serving.** The platform doesn't wait for your process to bind the port before reporting the sandbox as running, so retry your first connection.

The platform reports endpoint addresses while a sandbox is creating or running, and clears them in every other state. Even if `serviceEndpoints` still contains HTTPS metadata, a paused or completed sandbox has no reachable endpoint.

## Connect to a TLS passthrough endpoint

Because the platform doesn't decrypt the connection, the certificate a client receives is the one your workload presents. Before connecting, start the TLS server with its certificate and private key, as described in the Declare an endpoint section. The following validating client has three requirements:

* Send the endpoint host as the SNI server name. The platform routes on SNI alone, so a connection that omits it, or sends a different name, doesn't reach your sandbox.
* Trust the workload's certificate chain. Configure the client with the CA certificates it needs to validate your workload's certificate chain.
* Match the assigned hostname. The server certificate must cover the endpoint host, such as through a matching DNS entry in its subject alternative name (SAN) extension. Trusting the CA alone doesn't make a certificate for another hostname valid. Keep hostname verification enabled.

The following client sends the endpoint host as SNI and verifies both the certificate chain and hostname. Replace `[ENDPOINT-ADDRESS]` with the address you read from `service_addresses`, and `[PATH-TO-CA-CERT]` with the path to the trusted CA certificate in Privacy-Enhanced Mail (PEM) format. The client uses the same `host` value for routing and certificate verification:

```python theme={"system"}
import socket
import ssl

address = "[ENDPOINT-ADDRESS]"  # host:port from service_addresses
host, port = address.rsplit(":", 1)

context = ssl.create_default_context(cafile="[PATH-TO-CA-CERT]")

with socket.create_connection((host, int(port))) as sock:
    with context.wrap_socket(sock, server_hostname=host) as tls:
        print(tls.version(), tls.getpeercert()["subject"])
```

A successful connection prints the negotiated TLS version and the server certificate's subject. If the client doesn't trust the certificate chain or the certificate doesn't cover `host`, certificate verification fails.

## Endpoint lifetime

An endpoint lives as long as the sandbox that owns it:

* **It's keyed to the sandbox, not to a Pod.** If the underlying Pod restarts, the address stays the same.
* **Deleting the sandbox removes the endpoint.** The address doesn't move to another sandbox, and a new sandbox gets a new address.
* **Nothing is reserved between sandboxes.** You can't hold a hostname for reuse.

## Troubleshoot create failures

If no runner in your fleet supports the endpoint kind you requested, the create call fails rather than starting a sandbox with the endpoint silently dropped.

| Reason | Meaning |
| - | - |
| `CWSANDBOX_TLS_PASSTHROUGH_ENDPOINTS_NOT_SUPPORTED` | No runner you can reach is configured for TLS passthrough. Ask your administrator to enable it on a runner. |
| `CWSANDBOX_NO_SUITABLE_RUNNER` | The sandbox declared both endpoint kinds, and no runner supports both. The response's `unsupported_endpoint_kinds` metadata names the kinds that are missing. |
| `CWSANDBOX_INVALID_REQUEST` | A `services` entry breaks one of the rules in [Declare an endpoint](#declare-an-endpoint), such as a duplicate port or `auth` set on a TLS passthrough endpoint. |
| `CWSANDBOX_HTTPS_SHARE_TOKEN_NOT_SUPPORTED` | No compatible runner advertises HTTPS share-token support. Ask your administrator to enable it on a runner. Upgrading the SDK alone doesn't enable this capability. |
| `CWSANDBOX_NOT_IMPLEMENTED` | The request combines unsupported service exposure modes, such as a plain `PUBLIC` service and a product endpoint in the same sandbox. |

## Related pages

* [Sandbox configuration](https://docs.coreweave.com/products/sandboxes/client/guides/sandbox-configuration.md): resources, ports, secrets, and timeouts.

* [Sandbox architecture](https://docs.coreweave.com/products/sandboxes/architecture.md): how runners, profiles, and the control plane interact.

* [Reach a tailnet service from a sandbox](https://docs.coreweave.com/products/sandboxes/tailscale-egress.md): connect outbound to a private service over Tailscale.

* [Sandbox lifecycle](https://docs.coreweave.com/products/sandboxes/client/guides/sandbox-lifecycle.md): the states a sandbox moves through.
