# Network rules

Source: https://docs.coreweave.com/products/sandboxes/client/ref/networking/network-rules

# Network rules

> Create-time egress and ingress rules, and the selectors they accept.

## EgressRule

Source: [src/cwsandbox/\_types.py:524](https://github.com/coreweave/cwsandbox-client/blob/v1.14.2/src/cwsandbox/_types.py#L524)

```python theme={"system"}
class EgressRule(*, dns_name: str | None = None, cidr: CidrBlock | Mapping[str, Any] | str | None = None, tenant: TenantScope | str | None = None, any: bool = False, selector: SelectorBlock | Mapping[str, Any] | None = None, ports: Sequence[PortRange | Mapping[str, Any] | int] | None = None, dns_name_except: Sequence[str] | None = None)
```

One create-time egress destination.

Exactly one destination must be set: `dns_name`, `cidr`, `tenant`,
`any`, or `selector`. DNS names are HTTPS (TCP 443) grants. Exact
names (`pypi.org`) or a single leftmost wildcard (`*.pypi.org`).
`"*"` is a policy ceiling, not a sandbox grant.

**Attributes**

* `dns_name` (`str | None`) : Hostname to grant for HTTPS (TCP 443).
* `cidr` (`CidrBlock | Mapping[str, Any] | str | None`) : IP range (`CidrBlock`, dict, or CIDR string).
* `tenant` (`TenantScope | str | None`) : Other sandboxes selected relationally.
* `any` (`bool`) : All destinations except platform-internal ranges. Default: `False`.
* `selector` (`SelectorBlock | Mapping[str, Any] | None`) : Cluster workloads selected by pod/namespace labels.
* `ports` (`Sequence[PortRange | Mapping[str, Any] | int] | None`) : Optional destination port filter. Empty = all ports
  on non-DNS rules. DNS-name grants omit ports or set
  exactly TCP 443.
* `dns_name_except` (`Sequence[str] | None`) : Policy-only carve-outs. Rejected on this
  create-time type.

***

## IngressRule

Source: [src/cwsandbox/\_types.py:633](https://github.com/coreweave/cwsandbox-client/blob/v1.14.2/src/cwsandbox/_types.py#L633)

```python theme={"system"}
class IngressRule(*, cidr: CidrBlock | Mapping[str, Any] | str | None = None, tenant: TenantScope | str | None = None, any: bool = False, ports: Sequence[PortRange | Mapping[str, Any] | int] | None = None)
```

One create-time CUSTOM-port ingress source.

Exactly one source must be set: `cidr`, `tenant`, or `any`.

**Attributes**

* `cidr` (`CidrBlock | Mapping[str, Any] | str | None`) : Source IP range.
* `tenant` (`TenantScope | str | None`) : Other sandboxes selected relationally.
* `any` (`bool`) : Any source, including the public internet. Default: `False`.
* `ports` (`Sequence[PortRange | Mapping[str, Any] | int] | None`) : Optional port filter. Empty = all CUSTOM-visibility ports.

***

## CidrBlock

Source: [src/cwsandbox/\_types.py:441](https://github.com/coreweave/cwsandbox-client/blob/v1.14.2/src/cwsandbox/_types.py#L441)

```python theme={"system"}
class CidrBlock(*, cidr: str, except_cidrs: Sequence[str] = ())
```

An IP range with optional carved-out sub-ranges.

**Attributes**

* `except_cidrs` (`Sequence[str]`) : Default: `()`.

***

## PortRange

Source: [src/cwsandbox/\_types.py:469](https://github.com/coreweave/cwsandbox-client/blob/v1.14.2/src/cwsandbox/_types.py#L469)

```python theme={"system"}
class PortRange(*, port: int, end_port: int | None = None, protocol: str | None = None)
```

A single port or inclusive port range.

**Attributes**

* `end_port` (`int | None`)
* `protocol` (`str | None`)

***

## SelectorBlock

Source: [src/cwsandbox/\_types.py:454](https://github.com/coreweave/cwsandbox-client/blob/v1.14.2/src/cwsandbox/_types.py#L454)

```python theme={"system"}
class SelectorBlock(*, pod_labels: Mapping[str, str], namespace_labels: Mapping[str, str] | None = None)
```

Label selector for cluster workloads (matchLabels only).

**Attributes**

* `namespace_labels` (`Mapping[str, str] | None`)

***

## TenantScope

Source: [src/cwsandbox/\_types.py:416](https://github.com/coreweave/cwsandbox-client/blob/v1.14.2/src/cwsandbox/_types.py#L416)

```python theme={"system"}
class TenantScope
```

* `UNSPECIFIED` = `'unspecified'`
* `SAME_USER` = `'same_user'`
* `SAME_ORG` = `'same_org'`
* `SANDBOX_NETWORK` = `'sandbox_network'`

***
