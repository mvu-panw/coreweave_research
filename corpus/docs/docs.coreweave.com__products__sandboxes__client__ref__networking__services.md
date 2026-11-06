# Services

Source: https://docs.coreweave.com/products/sandboxes/client/ref/networking/services

# Services

> Typed service ports a sandbox exposes.

## Service

Source: [src/cwsandbox/\_types.py:323](https://github.com/coreweave/cwsandbox-client/blob/v1.14.2/src/cwsandbox/_types.py#L323)

```python theme={"system"}
class Service(*, port: int, name: str | None = None, protocol: ServiceProtocol | str | None = None, visibility: ServiceVisibility | str | None = None, endpoint: Endpoint | dict[str, Any] | None = None)
```

Typed service port exposed by a sandbox.

Replaces the beta string `NetworkOptions` ingress/egress mode model.

**Attributes**

* `name` (`str | None`) : Optional service name.
* `protocol` (`ServiceProtocol | str | None`) : L4 protocol (defaults to TCP when unset). Must be unset or
  TCP when `endpoint` is set.
* `visibility` (`ServiceVisibility | str | None`) : Who may reach this port (PUBLIC/PRIVATE/CUSTOM).
  CUSTOM means the fleet assigns reachability; `service_urls`
  stays empty unless the API reports a URL. The service still
  appears in `exposed_ports`. Must be PUBLIC when `endpoint`
  is set.
* `endpoint` (`Endpoint | dict[str, Any] | None`) : Optional product endpoint. HTTPS/OPEN (optional
  `request_timeout_seconds`) or TLS\_PASSTHROUGH (auth and
  timeout unset). Omit for a plain TCP/UDP port.

***

## ServiceProtocol

Source: [src/cwsandbox/\_types.py:197](https://github.com/coreweave/cwsandbox-client/blob/v1.14.2/src/cwsandbox/_types.py#L197)

```python theme={"system"}
class ServiceProtocol
```

* `UNSPECIFIED` = `'unspecified'`
* `TCP` = `'tcp'`
* `UDP` = `'udp'`
* `SCTP` = `'sctp'`

***

## ServiceVisibility

Source: [src/cwsandbox/\_types.py:188](https://github.com/coreweave/cwsandbox-client/blob/v1.14.2/src/cwsandbox/_types.py#L188)

```python theme={"system"}
class ServiceVisibility
```

* `UNSPECIFIED` = `'unspecified'`
* `PUBLIC` = `'public'`
* `PRIVATE` = `'private'`
* `CUSTOM` = `'custom'`

***
