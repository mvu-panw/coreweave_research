# Create and manage VPCs

Source: https://docs.coreweave.com/products/networking/vpc/create-manage-vpcs

# Create and manage VPCs

> How to create and manage Virtual Private Clouds on CoreWeave Kubernetes Service

A VPC defines a network isolation configuration for attaching CoreWeave products, such as CKS clusters. This guide is for administrators who provision or update network isolation for CoreWeave workloads. It covers how to create a new VPC and how to edit or delete an existing one using the Cloud Console. By the end, you have a VPC configured with the address ranges and DNS settings required to attach a CKS cluster or other CoreWeave product.

## Create a VPC with the Cloud Console

This section walks through creating a new VPC from the Cloud Console, including the required address ranges and any advanced settings.

To create a VPC using the Cloud Console, navigate to the [VPCs](https://console.coreweave.com/vpcs) page. This page lists your deployed VPCs along with their statuses.

![Cloud Console VPC dashboard](https://mintcdn.com/coreweave-dbfa0e8d/Diszsi3qOqeLxowx/products/networking/_media/create-vpc-list.png?fit=max\&auto=format\&n=Diszsi3qOqeLxowx\&q=85\&s=1a455ac7c50f3e88ddacadcc99438a6b)

To open the VPC creation form, click the **Create a VPC** button on the top right of the screen.

![Create a New VPC menu in the Cloud Console](https://mintcdn.com/coreweave-dbfa0e8d/Diszsi3qOqeLxowx/products/networking/_media/create-vpc.png?fit=max\&auto=format\&n=Diszsi3qOqeLxowx\&q=85\&s=d5391919fa0681aa09426be387214b87)

The configuration fields on this page include:

| Value | Description |
| - | - |
| **Name** | Specify a name for the VPC. |
| **Zone** | A dropdown menu where you can select a Zone. A VPC must exist in the same Zone as the cluster you attach it to. See [Regions](https://docs.coreweave.com/platform/regions/about-regions-and-azs.md) for more information. |
| **Allow Public Prefix Announcement** | Specifies whether the VPC allows public prefixes advertised from Nodes to be imported into public-facing networks, making them accessible from the internet. |
| **VPC Prefixes** | A list of additional prefixes associated with the VPC. For example, CKS clusters use these prefixes for Pod and Service CIDR ranges. |
| **Host Prefixes** | Unique IPv4 IP ranges assigned to hosts in the VPC, validated for IPv4 CIDR format with prefix. |
| **Custom DNS Servers** | DNS servers announced through DHCP, validated for IP format. |

### VPC prefixes

VPC prefixes define the address ranges that workloads inside the VPC draw from, so you must plan them before attaching a cluster. A VPC requires at least three unique prefixes to be compatible with a CKS cluster. Prefixes can't use any address in the [RFC6598](https://datatracker.ietf.org/doc/html/rfc6598) (Carrier-Grade NAT) range of `100.64.0.0/10`.

For example, your VPC prefixes might look like this:

| Prefix | Description |
| - | - |
| `10.0.0.0/13` | Pod CIDR Range |
| `10.16.0.0/22` | Service CIDR Range |
| `10.16.4.0/22` | Internal Load Balancer CIDR Range |

Click the **Add a Prefix** button.

![Add a Prefix button in the VPC Prefixes menu](https://mintcdn.com/coreweave-dbfa0e8d/Diszsi3qOqeLxowx/products/networking/_media/create-vpc-add-prefix.png?fit=max\&auto=format\&n=Diszsi3qOqeLxowx\&q=85\&s=f0025afe7bd8603cc2559ee910742645)

The **New VPC Prefix** window opens, where you can enter the prefix details.

![New VPC Prefix menu in the Cloud Console](https://mintcdn.com/coreweave-dbfa0e8d/Diszsi3qOqeLxowx/products/networking/_media/create-vpc-prefixes.png?fit=max\&auto=format\&n=Diszsi3qOqeLxowx\&q=85\&s=852d1ca58bd47997be45bf35db5c53a3)

Additional configuration settings for the VPC are found under **Advanced Settings**.

![Advanced Settings for a new VPC prefix in the Cloud Console](https://mintcdn.com/coreweave-dbfa0e8d/Diszsi3qOqeLxowx/products/networking/_media/create-vpc-advanced.png?fit=max\&auto=format\&n=Diszsi3qOqeLxowx\&q=85\&s=aa45636b397f52b9e8e18bf109d8c66d)

| Value | Description |
| - | - |
| **Disable External Propagate** | Disables external propagation for this prefix, preventing the advertisement of the address space to external networks. |
| **Disable Host BGP Peering** | Disables BGP Peering for this prefix. |
| **Host DHCP Route** | Indicates this prefix has a DHCP route. |
| **Public** | Marks the prefix as publicly accessible. |

### Host prefixes

**Host prefixes** define the IP address ranges assigned to the Nodes within a VPC. Nodes use these ranges for network communications with other resources within the VPC.

> [!WARNING]
>
> You can add more Host Prefixes at any time, but you can't remove an existing Host Prefix.

To add a new range of host IP addresses, click the **Add a Prefix** button to open the **New Host Prefix** window.

![Add a Prefix button in the Host Prefixes menu](https://mintcdn.com/coreweave-dbfa0e8d/Diszsi3qOqeLxowx/products/networking/_media/create-vpc-add-host-prefix.png?fit=max\&auto=format\&n=Diszsi3qOqeLxowx\&q=85\&s=5a0c2fca061d223c9687908000aa042c)

![New Host Prefix menu in the Cloud Console](https://mintcdn.com/coreweave-dbfa0e8d/Diszsi3qOqeLxowx/products/networking/_media/create-vpc-new-host-prefix.png?fit=max\&auto=format\&n=Diszsi3qOqeLxowx\&q=85\&s=687606028bc1458b7e9674482bc76cfe)

Each CoreWeave Availability Zone (AZ) (An Availability Zone (AZ) is a partition within a region that hosts one or more data halls. AZs are physically and operationally independent from each other.) features a default Host Prefix. CoreWeave assigns it automatically unless you specify a different prefix. The default Host Prefixes for each AZ are:

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

> [!WARNING]
>
> **For SUNK users:** If you supply `network.hostPrefixes`, each host prefix must be no smaller than your zone's default shown in the list above. For example, if your zone has a default prefix of /18, use a subnet mask of that size or larger. Host prefixes smaller than the zone default don't carry physical-location-based IP addresses, which SUNK uses to calculate Node adjacency.
>
> **For [NVL72 rack-level instances](https://docs.coreweave.com/platform/instances/nvl72.md):** The same limit applies to the VPC primary host prefix. A prefix smaller than the zone default forces dynamic address allocation, which breaks IMEX address mapping across the cluster. See [IMEX overview](https://docs.coreweave.com/products/cks/clusters/scheduling/imex-overview.md) for details.

## Manage VPCs in the Cloud Console

This section covers ongoing management tasks for existing VPCs, including how to sort, edit, and delete them. After you create a VPC, you can edit its configuration or remove it when you no longer need it. The [VPCs](https://console.coreweave.com/vpcs) page displays a list of your VPCs and their statuses.

![Cloud Console VPC dashboard](https://mintcdn.com/coreweave-dbfa0e8d/Diszsi3qOqeLxowx/products/networking/_media/create-vpc-list.png?fit=max\&auto=format\&n=Diszsi3qOqeLxowx\&q=85\&s=1a455ac7c50f3e88ddacadcc99438a6b)

You can sort VPCs by **Name**, **Zone**, **Age**, or **Status**. Use the **arrow** buttons near each field to sort the list accordingly.

![Cloud Console VPC dashboard with sort arrows next to each column header](https://mintcdn.com/coreweave-dbfa0e8d/Diszsi3qOqeLxowx/products/networking/_media/create-vpc-sort-arrows.png?fit=max\&auto=format\&n=Diszsi3qOqeLxowx\&q=85\&s=cdb9f0580b20881767bb48c6c40afbde)

### Edit a VPC

To make changes to an existing VPC, click the vertical ellipsis menu button to the right of the VPC name. Then, click the **Edit** button.

![Cloud Console VPC dashboard with the three-dot and Edit menus highlighted](https://mintcdn.com/coreweave-dbfa0e8d/Diszsi3qOqeLxowx/products/networking/_media/create-vpc-ellipse.png?fit=max\&auto=format\&n=Diszsi3qOqeLxowx\&q=85\&s=4add0ddec74173ce0f7746f82291b740)

This opens the **Edit VPC** window, which includes all the same options as the Create VPC window.

![Edit a VPC menu in the Cloud Console](https://mintcdn.com/coreweave-dbfa0e8d/Diszsi3qOqeLxowx/products/networking/_media/create-vpc-edit.png?fit=max\&auto=format\&n=Diszsi3qOqeLxowx\&q=85\&s=7cc2ca316b66925a220631a7494a70dd)

### Delete a VPC

To delete a VPC, select the vertical ellipsis beside the VPC name, then select **Delete**.

![Cloud Console VPC dashboard with the Delete button highlighted](https://mintcdn.com/coreweave-dbfa0e8d/Diszsi3qOqeLxowx/products/networking/_media/manage-vpc-delete.png?fit=max\&auto=format\&n=Diszsi3qOqeLxowx\&q=85\&s=b4ecb2e1fd438edd87fa7d388ad8ecaf)
