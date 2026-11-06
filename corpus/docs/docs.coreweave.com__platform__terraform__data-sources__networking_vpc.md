# coreweave_networking_vpc (Data source)

Source: https://docs.coreweave.com/platform/terraform/data-sources/networking_vpc

# coreweave_networking_vpc (Data source)

> Terraform data source for querying information about an existing CoreWeave VPC by ID

Query information about an existing VPC by ID. See the [CoreWeave VPC API reference](https://docs.coreweave.com/products/networking/vpc/vpc-api.md).

## Example usage

```terraform theme={"system"}
data "coreweave_networking_vpc" "default" {
  id = "1063bce6-6e5b-4b0a-b73a-7e6106b2a77c"
}
```

## Schema

### Required

* `id` (String) The ID of the VPC.

### Read-Only

* `dhcp` (Attributes) Settings affecting DHCP behavior within the VPC. (see [below for nested schema](#nestedatt--dhcp))
* `egress` (Attributes) Settings affecting traffic leaving the VPC. (see [below for nested schema](#nestedatt--egress))
* `host_prefix` (String, Deprecated) An IPv4 CIDR range used to allocate host addresses when booting compute into a VPC.
* `host_prefixes` (Attributes Set) The IPv4 or IPv6 CIDR ranges used to allocate host addresses when booting compute into a VPC. (see [below for nested schema](#nestedatt--host_prefixes))
* `ingress` (Attributes) Settings affecting traffic entering the VPC. (see [below for nested schema](#nestedatt--ingress))
* `name` (String) The name of the VPC.
* `vpc_prefixes` (Attributes List) A list of additional named IPv4 prefixes for the VPC. (see [below for nested schema](#nestedatt--vpc_prefixes))
* `zone` (String) The Availability Zone in which the VPC is located.

### Nested Schema for `dhcp`

Read-Only:

* `dns` (Attributes) Settings affecting DNS for DHCP within the VPC (see [below for nested schema](#nestedatt--dhcp--dns))

### Nested Schema for `dhcp.dns`

Optional:

* `servers` (Set of String) The DNS servers advertised to DHCP clients within the VPC.

Read-Only:

* `search_domains` (List of String) The DNS search domains advertised to DHCP clients within the VPC, in order of resolution precedence.

### Nested Schema for `egress`

Read-Only:

* `disable_public_access` (Boolean) True if the VPC is blocked from consuming public Internet. False otherwise.

### Nested Schema for `host_prefixes`

Read-Only:

* `ipam` (Attributes) The configuration for a secondary host prefix. (see [below for nested schema](#nestedatt--host_prefixes--ipam))
* `name` (String) The user-specified name of the host prefix.
* `prefixes` (List of String) The VPC-wide aggregates from which host-specific prefixes are allocated. May be IPv4 or IPv6.
* `type` (String) Controls network connectivity from the prefix to the host.

### Nested Schema for `host_prefixes.ipam`

Read-Only:

* `gateway_address_policy` (String) Describes which IP address from the prefix is allocated to the network gateway.
* `prefix_length` (Number) The desired length for each Node's allocation from the VPC-wide aggregate prefix.

### Nested Schema for `ingress`

Read-Only:

* `disable_public_services` (Boolean) True if the VPC will prevent public prefixes advertised from Nodes from being imported into public-facing networks, making them inaccessible from the Internet. False otherwise.

### Nested Schema for `vpc_prefixes`

Read-Only:

* `name` (String)
* `type` (String) The intended use of the prefix; null when no type is assigned.
* `value` (String)
