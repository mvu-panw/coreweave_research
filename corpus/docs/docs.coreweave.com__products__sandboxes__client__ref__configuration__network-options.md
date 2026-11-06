# NetworkOptions

Source: https://docs.coreweave.com/products/sandboxes/client/ref/configuration/network-options

# NetworkOptions

> Network deny flags and create-time ingress/egress grants.

Source: [src/cwsandbox/\_types.py:676](https://github.com/coreweave/cwsandbox-client/blob/v1.14.2/src/cwsandbox/_types.py#L676)

```python theme={"system"}
class NetworkOptions(*, deny_egress: bool | None = None, deny_ingress: bool | None = None, egress: Sequence[EgressRule | Mapping[str, Any]] | None = None, ingress: Sequence[IngressRule | Mapping[str, Any]] | None = None)
```

Network deny flags and create-time ingress/egress grants.

Port exposure uses typed `services=`. `egress` and `ingress` are
allow-only rule sets over default-deny; empty/None leaves the runner
policy default in effect.

**Attributes**

* `deny_egress` (`bool | None`) : When True, deny all declared egress (policy default unused).
  Mutually exclusive with a non-empty `egress` list.
* `deny_ingress` (`bool | None`) : When True, deny CUSTOM ingress (policy default unused).
* `egress` (`Sequence[EgressRule | Mapping[str, Any]] | None`) : Egress grants (`EgressRule` or dict).
* `ingress` (`Sequence[IngressRule | Mapping[str, Any]] | None`) : CUSTOM-port ingress sources (`IngressRule` or dict).
