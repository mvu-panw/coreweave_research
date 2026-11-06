# Endpoints

Source: https://docs.coreweave.com/products/sandboxes/client/ref/networking/endpoints

# Endpoints

> Product endpoints on public services, and the status shapes echoed back.

## Endpoint

Source: [src/cwsandbox/\_types.py:219](https://github.com/coreweave/cwsandbox-client/blob/v1.14.2/src/cwsandbox/_types.py#L219)

```python theme={"system"}
class Endpoint(*, kind: EndpointKind | str, auth: EndpointAuth | str | None = None, request_timeout_seconds: int | None = None)
```

Product endpoint on a PUBLIC service. Set at create time.

HTTPS + OPEN: CoreWeave terminates TLS. A URL in
`Sandbox.service_urls` means the hostname was assigned, not that
the app is listening yet. `auth` is required.

TLS\_PASSTHROUGH: the platform forwards TLS by SNI to the container.
`auth` and `request_timeout_seconds` must be unset. The assigned
target is `host:port` on `Sandbox.service_addresses`. Use the
host as TLS SNI. The workload owns certs.

`request_timeout_seconds` is the server-side HTTPS request clock on
this product endpoint (504 while the sandbox stays alive). It is not
`Sandbox.run(request_timeout_seconds=...)`, which is the client RPC
deadline. This client only requires an `int` (or `None`).

**Attributes**

* `auth` (`EndpointAuth | str | None`) : `OPEN` when kind is HTTPS. Must be omitted for TLS
  passthrough.
* `request_timeout_seconds` (`int | None`) : Seconds before the platform closes an
  in-flight HTTPS request. `None` or `0` selects the
  platform default (15s on serverless). The server accepts
  `0` or `[15, 900]`. On create-from-template, `0` is
  replace-on-presence and does not clear a template timeout
  back to the platform default. Must be unset for TLS
  passthrough.

***

## EndpointAuth

Source: [src/cwsandbox/\_types.py:213](https://github.com/coreweave/cwsandbox-client/blob/v1.14.2/src/cwsandbox/_types.py#L213)

```python theme={"system"}
class EndpointAuth
```

* `OPEN` = `'open'`

***

## EndpointKind

Source: [src/cwsandbox/\_types.py:206](https://github.com/coreweave/cwsandbox-client/blob/v1.14.2/src/cwsandbox/_types.py#L206)

```python theme={"system"}
class EndpointKind
```

* `HTTPS` = `'https'`
* `TLS_PASSTHROUGH` = `'tls_passthrough'`

***

## HttpsEndpointStatus

Source: [src/cwsandbox/\_types.py:278](https://github.com/coreweave/cwsandbox-client/blob/v1.14.2/src/cwsandbox/_types.py#L278)

```python theme={"system"}
class HttpsEndpointStatus(*, port: int, name: str, kind: EndpointKind, auth: EndpointAuth, url: str, request_timeout_seconds: int)
```

Applied HTTPS product endpoint echoed on `Sandbox.service_endpoints`.

`request_timeout_seconds` is the effective server-side clock (15 when
create omitted or sent `0`). `url` is empty when the API suppresses
it (terminal sandboxes). This is not `Sandbox.run(request_timeout_seconds=...)`.

***

## TlsPassthroughEndpointStatus

Source: [src/cwsandbox/\_types.py:303](https://github.com/coreweave/cwsandbox-client/blob/v1.14.2/src/cwsandbox/_types.py#L303)

```python theme={"system"}
class TlsPassthroughEndpointStatus(*, port: int, name: str, kind: EndpointKind, address: str)
```

Applied TLS passthrough endpoint echoed on `Sandbox.service_addresses`.

`address` is `host:port`. Use the host as TLS SNI. The workload
owns certs. Empty after stop.

***
