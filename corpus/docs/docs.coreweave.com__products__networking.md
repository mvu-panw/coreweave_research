# About networking

Source: https://docs.coreweave.com/products/networking

# About networking

> Overview of CoreWeave networking products, including VPCs, HPC Interconnect, Direct Connect, IP addresses, and Ingress

# Networking for GPU-scale workloads

CoreWeave networking spans per-cluster VPCs, non-blocking InfiniBand and Spectrum-X interconnect, Direct Connect, bring-your-own IP addressing, and ingress load balancing for secure, high-throughput connectivity.

CoreWeave offers a suite of networking products for managing network infrastructure. Our networking products are designed to create a secure, high-performance, and scalable network that interconnects your resources and services. This page introduces each product and links to more detailed documentation so you can choose the right ones for your workloads.

## Virtual private clouds

[Virtual Private Clouds](https://docs.coreweave.com/products/networking/vpc/about-vpcs.md) (VPCs (A Virtual Private Cloud (VPC) is a private network hosted within a public cloud infrastructure.)) are isolated networks used by CoreWeave Kubernetes Service (CKS) clusters to securely communicate with each other and the internet while maintaining privacy and security by defining the network isolation for attached CoreWeave products.

VPCs allow for the creation of segregated and secure networks for your resources within the CoreWeave Cloud infrastructure. This isolation ensures that your data and applications remain private and protected. VPCs are essential for organizations using cloud computing while maintaining strict control over network environments.

## HPC Interconnect

[HPC Interconnect](https://docs.coreweave.com/products/networking/hpc-interconnect/about-hpc-interconnect.md) provides high-performance, RDMA-enabled fabrics for GPU-to-GPU communication. CoreWeave offers two distinct fabrics: NVIDIA Quantum InfiniBand and NVIDIA Spectrum-X (RoCE). Both are optimized for the high throughput and low latency required for large-scale model training and other demanding parallel workloads.

GPUDirect RDMA enables direct access between the main memory of two computers without involving the operating system, cache, or storage, which reduces latency and increases throughput.

## Direct Connect

[Direct Connect](https://docs.coreweave.com/products/networking/direct-connect/about-direct-connect.md) lets you connect directly to CoreWeave through private, dedicated links. If you use Equinix or Megaport, you can use your existing connections when establishing direct connections to CoreWeave. You don't need to add additional dedicated physical ports or establish a network presence in our regions.

## IP addresses

CoreWeave supports both [Public IPv4](https://docs.coreweave.com/products/networking/ip/public-ipv4.md) addresses and [Bring Your Own IP (BYOIP)](https://docs.coreweave.com/products/networking/ip/bring-your-own-ip.md). Public IPv4 addresses ensure that your Services are accessible over the internet, which is necessary for deploying web applications and Services that need to be available globally. BYOIP lets you use your own IPv4 (Internet Protocol version 4 (IPv4) is one of the core protocols that enables the internet.) addresses on CoreWeave Cloud, which is useful for customers who have existing IP address spaces they want to use for workloads on CoreWeave.

## Ingress Service

The [Ingress Service](https://docs.coreweave.com/products/networking/ingress-service/expose-service-dns.md) exposes Services running on CKS to the public internet using `LoadBalancer` Services and public IPv4 addresses. You can also [request a fully qualified domain name (FQDN) or wildcard record](https://docs.coreweave.com/products/networking/ingress-service/create-public-dns-name.md) to provide a stable, human-readable address for your publicly exposed Services.

## DNS overrides on CKS

[Configure DNS overrides on CKS](https://docs.coreweave.com/products/networking/configure-dns-overrides.md) to forward private domains to your own resolvers or map hostnames to IP addresses. The guide explains how to preserve managed entries, store configuration in version control, and verify DNS resolution from Pods.

## Nimbus

[Nimbus](https://docs.coreweave.com/products/networking/nimbus.md) is CoreWeave's control and data-plane software, integrated into the NVIDIA BlueField Data Processing Unit (DPU) affixed to each Node. The DPU operates in isolation from the host CPU and handles VPC networking, tenant isolation, and public internet routing directly on-chip. When you request a VPC or other network resource in CKS, Nimbus programs the appropriate network policy on the DPU without involving the host operating system.

## Outbound traffic and IP allowlisting

Outbound traffic from your Pods leaves the cluster through a NAT that uses a stable, documented set of public IP ranges per Availability Zone. When an external service needs an allowlist, such as MongoDB Atlas, a partner API, or a firewalled database, allowlist the `NAT Egress` ranges for the Availability Zones your workloads run in.

Each region page lists its `NAT Egress` ranges in the **Network information** table. See [Regions and Availability Zones](https://docs.coreweave.com/platform/regions/about-regions-and-azs.md) for the full list, or [Does outbound traffic have a stable public IP?](https://docs.coreweave.com/support/networking/articles/does-outbound-traffic-have-a-stable-public-ip) for a summary.

## Bandwidth and data transfer

Per-instance Ethernet bandwidth is bounded by the NIC of the underlying instance type, with no separate per-public-IP throttle. Each instance's NIC configuration appears in its specification table on the [GPU instances](https://docs.coreweave.com/platform/instances/gpu-instances.md) and [CPU instances](https://docs.coreweave.com/platform/instances/cpu-instances.md) pages. For high-bandwidth distributed workloads such as multi-Node training, use the dedicated [HPC Interconnect](https://docs.coreweave.com/products/networking/hpc-interconnect/about-hpc-interconnect.md) rather than the standard Ethernet path. See [What are the bandwidth limits per instance or public IP?](https://docs.coreweave.com/support/networking/articles/what-are-the-bandwidth-limits-per-instance-or-public-ip) for details.

Data transfer between CoreWeave Regions is free. See [Region features](https://docs.coreweave.com/platform/regions/about-regions-and-azs.md#region-features).

## Private cluster access

By default, self-service CKS clusters expose the Kubernetes API over the internet. Private clusters have no public API endpoint, so you reach the API through a proxy:

* [Tailscale VPN](https://docs.coreweave.com/products/cks/auth-access/tailscale-vpn.md) provides a CoreWeave-managed private access path.
* [Traefik ingress](https://docs.coreweave.com/products/cks/clusters/coreweave-charts/traefik.md), often paired with [Direct Connect](https://docs.coreweave.com/products/networking/direct-connect/about-direct-connect.md), provides an in-cluster proxy over dedicated private links.

Self-service cluster creation supports public clusters only. To set up a private cluster, [contact CoreWeave Support](https://docs.coreweave.com/support.md). For authentication details, see [CKS authentication and access](https://docs.coreweave.com/products/cks/auth-access/introduction.md).
