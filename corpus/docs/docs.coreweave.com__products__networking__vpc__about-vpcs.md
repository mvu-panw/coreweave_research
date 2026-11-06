# Virtual Private Clouds (VPCs)

Source: https://docs.coreweave.com/products/networking/vpc/about-vpcs

# Virtual Private Clouds (VPCs)

> Virtual Private Clouds provide network isolation and custom addressing for CKS clusters

CoreWeave Virtual Private Clouds (VPCs (A Virtual Private Cloud (VPC) is a private network hosted within a public cloud infrastructure.)) define the network isolation configuration for attached CoreWeave products, like [CKS clusters](https://docs.coreweave.com/products/cks/clusters/introduction.md). VPCs let clusters securely communicate with resources in a Region (A region encompasses a broader geographic area, expanding service availability and meeting data residency requirements.), and with the public internet if desired, while preserving the privacy and security of the cluster's network.

This page introduces how CoreWeave VPCs work, the default VPC behavior for new CKS clusters, the prefix types you can configure, and when to define a custom VPC.

## Why a VPC is required for cluster creation

Every CKS cluster attaches to a VPC because the VPC provides the network foundation the cluster depends on:

* **Isolation**: The VPC defines the network isolation boundary for the cluster, so it can communicate securely with resources in a Region, and with the public internet when you allow it, while preserving the privacy of the cluster's network.
* **Addressing**: The VPC supplies the IP address ranges that cluster resources draw from. A VPC needs at least three unique prefixes to be compatible with a CKS cluster: a Pod CIDR, a Service CIDR, and an internal Load Balancer CIDR. Nodes draw their addresses from the VPC's Host Prefixes.
* **Routing**: VPC Prefixes let the cluster reach other VPCs in the same Region, remote cloud providers, or on-premises networks through a VPN or Direct Connect.

Because a cluster can't function without this network configuration, CoreWeave creates a default VPC for you when you create your first cluster, unless you define a custom VPC. See [Default VPCs](#default-vpcs).

## Safe defaults for your first cluster

If you're creating a single cluster and don't have specific addressing or external connectivity requirements, the default VPC is a safe choice. CoreWeave assigns the default Host Prefix for the Zone and creates working network isolation without upfront planning. See [Default VPCs](#default-vpcs).

When you define a custom VPC or customize the default VPC, you set the Pod, Service, and internal Load Balancer CIDR blocks yourself. The following block sizes from [VPC CIDR blocks](https://docs.coreweave.com/products/networking/vpc/vpc-cidr.md) suit most first clusters:

| Prefix | Recommended block size | Capacity |
| - | - | - |
| Host Prefix | `/18` | Up to 4,000 Nodes, with 2 IP addresses per Node. |
| Pod CIDR | `/13` | Up to 100 Pods per Node. |
| Service CIDR | `/22` | Up to 1,000 Services. |
| Internal LB CIDR | `/22` | Up to 1,000 Load Balancers. |

For a smaller cluster, you can use smaller CIDR ranges. For example, if you plan only 500 Nodes, you don't need a full `/18` Host Prefix.

However, smaller ranges can limit future growth because Service ClusterIPs are allocated from a contiguous Service CIDR block. Expanding that space later requires defining a new Service CIDR and recreating Services.

Keep all CIDR ranges non-overlapping so you can connect to other VPCs later without routing conflicts.

For sizing rules, example CIDR values, and multi-cluster planning, see [VPC CIDR blocks](https://docs.coreweave.com/products/networking/vpc/vpc-cidr.md).

## When to use a custom VPC

Create a custom VPC when any of the following apply:

* You plan to connect multiple clusters or VPCs. Connected VPCs need unique, non-overlapping address space, so you must plan CIDR ranges up front to avoid routing conflicts. See [Plan CIDRs for connected VPCs](https://docs.coreweave.com/products/networking/vpc/vpc-cidr.md#plan-cidrs-for-connected-vpcs).
* You need to integrate with existing networks, such as on-premises networks or remote cloud providers through a VPN or [Direct Connect](https://docs.coreweave.com/products/networking/direct-connect/about-direct-connect.md). These integrations need known, non-overlapping IP ranges.
* You need specific addressing or larger CIDR blocks than the defaults provide.

You can't remove a Host Prefix after you add it to a VPC, so plan your addressing scheme before you create the custom VPC.

To define a custom VPC, see [Create and manage VPCs](https://docs.coreweave.com/products/networking/vpc/create-manage-vpcs.md), or define one [during cluster creation](https://docs.coreweave.com/products/cks/clusters/create.md#select-a-vpc).

## Default VPCs

When you create your first CKS cluster through the Cloud Console, CoreWeave creates a default VPC in the same Zone as that cluster, unless you define a custom VPC. This default ensures that clusters have working network isolation without requiring upfront VPC configuration.

### Custom prefixes

You can add custom VPC Prefixes to custom or default VPCs to allow communication with other VPCs in the same Region, with remote cloud providers, or with on-premises networks through a VPN or Direct Connect. Configure custom prefixes when your workloads need to reach networks outside the VPC. Add custom prefixes to a VPC [through the Cloud Console during VPC creation](https://docs.coreweave.com/products/networking/vpc/create-manage-vpcs.md#vpc-prefixes), or [during cluster creation at the network configuration step](https://docs.coreweave.com/products/cks/clusters/create.md#select-a-vpc).

You can configure two types of prefixes for VPCs:

| Prefix type | Description |
| - | - |
| **Host Prefixes** | A range of IP addresses to assign to the Nodes within a VPC. Nodes use these addresses for network communications with other resources within the VPC. |
| **VPC Prefixes** | A range of IP addresses you can use to communicate with other VPCs in the same Region, with remote cloud providers, or with on-premises networks through a VPN or Direct Connect. |

Each CoreWeave Availability Zone (AZ) (An Availability Zone (AZ) is a partition within a region that hosts one or more data halls. AZs are physically and operationally independent from each other.) has a default Host Prefix, which CoreWeave assigns automatically unless you specify a different prefix.

The default Host Prefixes for each AZ are:

| General Access AZ | Default Host Prefix CIDR |
| - | - |
| [`CA-EAST-01A`](https://docs.coreweave.com/platform/regions/ca-east#ca-east-01a) | `10.219.128.0/18` |
| [`EU-SOUTH-03B`](https://docs.coreweave.com/platform/regions/eu-south#eu-south-03b) | `10.206.192.0/18` |
| [`EU-SOUTH-04A`](https://docs.coreweave.com/platform/regions/eu-south#eu-south-04a) | `10.104.192.0/18` |
| [`RNO2A`](https://docs.coreweave.com/platform/regions/us-west#rno2a) | `10.168.192.0/18` |
| [`US-CENTRAL-06A`](https://docs.coreweave.com/platform/regions/us-central#us-central-06a) | `10.51.128.0/17` |
| [`US-CENTRAL-07A`](https://docs.coreweave.com/platform/regions/us-central#us-central-07a) | `10.109.128.0/18` |
| [`US-EAST-01A`](https://docs.coreweave.com/platform/regions/us-east#us-east-01a) | `10.202.192.0/18` |
| [`US-EAST-02A`](https://docs.coreweave.com/platform/regions/us-east#us-east-02a) | `10.184.192.0/18` |
| [`US-EAST-04A`](https://docs.coreweave.com/platform/regions/us-east#us-east-04a) | `10.176.192.0/18` |
| [`US-EAST-06A`](https://docs.coreweave.com/platform/regions/us-east#us-east-06a) | `10.192.192.0/18` |
| [`US-EAST-08A`](https://docs.coreweave.com/platform/regions/us-east#us-east-08a) | `10.186.192.0/18` |
| [`US-EAST-13A`](https://docs.coreweave.com/platform/regions/us-east#us-east-13a) | `10.221.128.0/18` |
| [`US-EAST-14A`](https://docs.coreweave.com/platform/regions/us-east#us-east-14a) | `10.213.128.0/18` |
| [`US-EAST-15A`](https://docs.coreweave.com/platform/regions/us-east#us-east-15a) | `10.125.128.0/18` |
| [`US-EAST-17A`](https://docs.coreweave.com/platform/regions/us-east#us-east-17a) | `10.59.128.0/17` |
| [`US-WEST-01A`](https://docs.coreweave.com/platform/regions/us-west#us-west-01a) | `10.188.192.0/18` |
| [`US-WEST-02B`](https://docs.coreweave.com/platform/regions/us-west#us-west-02b) | `10.112.192.0/18` |
| [`US-WEST-04A`](https://docs.coreweave.com/platform/regions/us-west#us-west-04a) | `10.190.192.0/18` |
| [`US-WEST-09B`](https://docs.coreweave.com/platform/regions/us-west#us-west-09b) | `10.210.192.0/18` |
| [`US-WEST-10A`](https://docs.coreweave.com/platform/regions/us-west#us-west-10a) | `10.57.128.0/17` |

> [!NOTE]
>
> You can't modify or remove Host Prefixes after you add them to a VPC. CoreWeave assigns Host Prefixes when the Node boots, so you can't modify them while the Node is running.

### Default VPC names

CoreWeave automatically creates a default VPC when you first create a cluster. The name of a new default VPC uses the following format:

`cw-vpc-[CLUSTER-NAME]-[SIX-DIGIT-STRING]`

To see the name of the default VPC, click the **Customize** option beside the default VPC selector during [cluster creation](https://docs.coreweave.com/products/cks/clusters/create.md#2-network).

## Custom VPCs

When the default VPC doesn't meet your network requirements, for example when you need custom addressing or connectivity to external networks, define a custom VPC instead. If you need a custom VPC configuration, define it by [creating a VPC](https://docs.coreweave.com/products/networking/vpc/create-manage-vpcs.md) from the Cloud Console, or during the cluster creation process by [defining a custom VPC](https://docs.coreweave.com/products/cks/clusters/create.md#select-a-vpc).

For more information, see [VPC API reference](https://docs.coreweave.com/products/networking/vpc/vpc-api.md).
