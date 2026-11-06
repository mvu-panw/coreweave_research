# Direct Connect

Source: https://docs.coreweave.com/products/networking/direct-connect/about-direct-connect

# Direct Connect

> Use dedicated physical cross-connects or virtual connections through our on-ramp partners

**Direct Connect (DX)** is a networking product that lets you connect your Virtual Private Clouds (VPCs) on the CoreWeave platform to your on-premises or hyperscaler networks. Unlike standard internet connections, Direct Connect bypasses the public internet, which provides guaranteed port speeds, secure data transfer, lower latency, and the ability to place workloads where they fit best.

This page explains the following, so you can choose the right option for your workloads and prepare to request a connection:

* Connectivity options.
* Supported locations.
* Network and BGP requirements.
* Deployment topologies.
* Provisioning and billing.

## Connectivity options

CoreWeave offers two connectivity options: **Dedicated DX** and **Virtual DX**.

### Dedicated DX

**Dedicated DX** is a dedicated physical cross-connect (XC) with guaranteed port speeds in CoreWeave's facilities throughout North America and Europe. Dedicated DX provides the highest throughput and resilience among DX options, letting you bypass the public internet when transferring data and resources securely between clouds and on-premises networks. To find the facilities where Dedicated DX is available, see [CoreWeave DX locations](#coreweave-dx-locations).

Dedicated DX uses physical and dedicated cross-connects (XCs) to connect directly to CoreWeave's edge networks. It supports high-speed connections of 10G, 100G, or 400G, and supports MACsec encryption for secure data transmission. To support larger MTU sizes, you can request that we enable jumbo frames.

### Virtual DX

**Virtual DX** is a virtual connection (VC) through our on-ramp partners, Equinix Fabric and Megaport. You can use your existing Equinix or Megaport ports without adding dedicated physical ports or establishing a network presence in our regions. To find the supported Cloud On-Ramps for Virtual DX, see [CoreWeave DX locations](#coreweave-dx-locations). This lets you interconnect in hundreds of colocations around the world while still bypassing the public internet for secure data transfer between clouds and on-premises networks.

Virtual DX supports 10G connections, which suit many workloads that don't need the high throughput of Dedicated DX. It doesn't support MACsec encryption or jumbo frames. Consider your security and performance requirements before choosing this option.

### Common features

The following features apply to both Dedicated and Virtual DX.

* Link Aggregation Control Protocol (LACP) is enabled by default. If you have multiple DXs, you can bond them into a single Link Aggregation Group (LAG) to aggregate bandwidth and improve resilience. For example, if you need 100G DX now but plan to scale to 400G later, you can add three 100G ports when you need the capacity and use LAG to bond all four links together.
* If you have multiple VPCs that need to be isolated over your DXs, you can enable 802.1Q VLAN tagging. This ensures traffic ingressing the Direct Connect Router from one VPC can't reach others, regardless of whether the VPCs are in the same or different Regions or Availability Zones (AZs).
* To support secure data transmission, you can request BGP with MD5 or TCP-AO authentication.
* Data transfer is free of charge.

## Dedicated and Virtual DX comparison summary

The following table summarizes the differences between Dedicated DX and Virtual DX to help you choose the option that best fits your performance, security, and reach requirements.

| | Dedicated DX | Virtual DX |
| - | - | - |
| Description | The highest-throughput interconnection option | Available in hundreds of Equinix or Megaport colocations and can reuse customers' existing ports |
| Connectivity Medium | Physical and dedicated Cross Connects (XCs) | Virtual Connection through Equinix Fabric or Megaport |
| DX Speed | 10G, 100G, or 400G | 10G |
| MACsec | Yes | No |
| Jumbo Frames | Yes | No |
| Link Aggregation | Yes | Yes |
| VLAN Tagging | Yes | Yes |
| BGP Authentication | Yes | Yes |
| Free Data Transfer | Yes | Yes |

## CoreWeave DX locations

CoreWeave has established Direct Connect (DX) locations across North America and Europe. These locations provide low-latency connections to our cloud infrastructure. Dedicated DX connections are available in the following facilities, while Virtual DX can be established through them from any supported Cloud On-Ramp location. When choosing a DX facility, consider the proximity to your on-premises data center.

The North American facilities specify a **Low Latency Region**, which is the CoreWeave region with the lowest latency to that facility. For example, CoreSite DE1 and Equinix DE2 have the lowest latency to CoreWeave `US-WEST-07`.

### North America

| Facility Name | Location | Supported Cloud On-Ramps | Low Latency Region |
| - | - | - | - |
| CoreSite DE1 | Denver, CO, USA | Megaport | `US-WEST-07` |
| CoreSite LA1 | Los Angeles, CA, USA | Megaport | `US-WEST-01` |
| Digital Realty SEA10 | Seattle, WA, USA | Megaport | `US-WEST-09` |
| Equinix AT1 | Atlanta, GA, USA | Equinix Fabric, Megaport | `US-EAST-04` |
| Equinix CH2 | Chicago, IL, USA | Equinix Fabric, Megaport | `US-EAST-04` |
| Equinix DA11 | Dallas, TX, USA | Equinix Fabric, Megaport | `US-EAST-06` |
| Equinix DC2 | Ashburn, VA, USA | Equinix Fabric, Megaport | `US-EAST-04` |
| Equinix DE2 | Denver, CO, USA | Equinix Fabric, Megaport | `US-WEST-07` |
| Equinix NY6 | Secaucus, NJ, USA | Equinix Fabric, Megaport | `US-EAST-02` |
| Equinix PH1 | Philadelphia, PA, USA | Equinix Fabric, Megaport | `US-EAST-02` |
| Equinix SE2 | Seattle, WA, USA | Equinix Fabric, Megaport | `US-WEST-09` |
| Equinix SV1 | San Jose, CA, USA | Equinix Fabric, Megaport | `US-WEST-01` |
| Equinix TR2 | Toronto, ON, Canada | Equinix Fabric, Megaport | `CA-EAST-01` |
| Switch Las Vegas | Las Vegas, NV, USA | Megaport | `US-WEST-01` |

### Europe

| Facility Name | Location | Supported Cloud On-Ramps |
| - | - | - |
| Digital Realty AMS17 | Amsterdam, Netherlands | Megaport |
| Equinix BA1 | Barcelona, Spain | Equinix Fabric, Megaport |
| Equinix FR5 | Frankfurt, Germany | Equinix Fabric, Megaport |
| Equinix LD5 | Slough, England | Equinix Fabric, Megaport |
| Equinix SK1 | Stockholm, Sweden | Equinix Fabric, Megaport |
| Stock OSL01A | Oslo, Norway | Megaport |

## On-demand provisioning

To provide flexible and cost-effective service, CoreWeave provisions virtual connection ports on-demand. This means you might not see CoreWeave listed as an available service provider in the Equinix Fabric or Megaport portals for a specific location. After you request a connection, we provision the necessary port, and it becomes visible in the partner portal. After the first customer connects in a given location, the port remains visible for all subsequent customers.

To connect through a provider not listed here, contact your Account Manager to discuss your requirements.

## Network requirements

To successfully deploy Direct Connect, customer networks must meet the following requirements.

| Requirement Type | Requirement |
| - | - |
| Colocation | Customers must be colocated in a CoreWeave Interconnection Location or reachable through Equinix Fabric/Megaport |
| Hardware - 10G DX | - **Dedicated DX**: Single-mode fiber with 10G-LR transceiver - **Virtual DX**: See Equinix Fabric/Megaport documentation for supported hardware |
| Hardware - 100G DX | - **Dedicated DX**: 100G-LR1 (preferred) or 100G-LR4 - **Virtual DX**: Not available |
| Hardware - 400G DX | - **Dedicated DX**: 400G-LR4 - **Virtual DX**: Not available |
| Protocols | Equipment must support LACP (unless requested disabled), and BGP with MD5/TCP-AO if authentication is desired |
| Prefix Limits | Customer network equipment should not advertise more than 200 prefixes. |

## BGP configuration

To establish a BGP session, CoreWeave needs a list of the BGP configurations and the specific prefixes you intend to advertise. For more details, see the [BGP configuration](#layer-3-bgp-configuration) section. We support MD5/TCP-AO authentication, and LACP. You can request these protocols when you request a DX connection.

## BGP prefix requirements

Customer network equipment shouldn't advertise more than 200 prefixes. This is a soft limit. To protect the network, if your network advertises more than 200 prefixes, the BGP session is torn down.

When exchanging BGP configurations, you must inform the Backbone Engineering team of your prefixes through Slack or email. CoreWeave uses exact-match import policies. If you advertise a prefix that hasn't been pre-approved, the BGP session is torn down.

You can advertise the same prefixes at all your DXs. We always route traffic from our data centers to the closest operational DX location based on our internal IGP metrics.

## Deployment topologies

We classify DX deployments into the following topologies:

* **Single-Location Non-Redundant:** Single connectivity in one location. This is not recommended for production.
* **Single-Location Redundant:** Two or more sets of connectivity in a single location to protect against equipment failure but not location failure.
* **Multi-Location Redundant:** Connectivity across two or more locations to protect against router, cross-connect, and full location failures.

For production workloads, we recommend either **Single-Location Redundant** or **Multi-Location Redundant** deployments.

## Routing and VPCs

If you have multiple VPCs, you can access all of them using one or multiple DXs over CoreWeave's backbone network. Traffic routing is determined by the following rules.

* If you announce specific prefixes at each DX location, traffic routes based on those prefixes.
* If you announce the *same* prefixes at all DX locations, traffic routes from CoreWeave data centers to the closest DX location based on internal IGP metrics.
* If a DX location goes down, traffic automatically routes to the next available location.

If you have one DX, and multiple VPCs in one AZ, you can reach all of them. Likewise, if you have one DX, and multiple VPCs in multiple AZs, you can reach all of them. You can also choose to enable 802.1Q VLAN tagging to isolate traffic so that ingress from one VPC can't reach another.

## When to choose Direct Connect over the public internet

Latency to an external cloud provider depends on where CoreWeave peers with that provider relative to your CoreWeave region. When your region and the provider's peering location are in the same metro, latency is low. When they are far apart, traffic travels to the peering location first, which adds latency. This is a function of geography, not a fault. If cross-cloud latency matters for your workload, choose a CoreWeave region close to the provider region you depend on, or use Direct Connect. For sustained high-throughput transfers, such as large object downloads or frequent checkpoint syncs, Direct Connect provides more predictable performance than the shared internet path.

### Internet2 peering

CoreWeave peers with Internet2 at several locations. This is BGP peering, not Direct Connect. Because CoreWeave VPCs are isolated and don't have general internet access, adding an Internet2 prefix to a VPC LoadBalancer CIDR doesn't by itself make those addresses externally routable. Reaching Internet2-routable services requires additional architecture, such as Direct Connect from your premises or a VPN overlay. If you need Internet2 connectivity, engage your CoreWeave representative to design the path.

## Test path connectivity to CoreWeave

CoreWeave Kubernetes API and ingress endpoints don't respond to ICMP echo (ping) by design. A failed ping to a CKS or SUNK hostname doesn't indicate a connectivity problem. To test path connectivity to a zone with ICMP, use the zone speedtest endpoint instead. Replace `[ZONE]` with your zone, for example `us-east-04a`:

```bash theme={"system"}
# Test reachability to a CoreWeave zone.
# Safe, read-only network probe.
ping ping.speedtest.[ZONE].coreweave.com
```

To isolate your local network from transit, run parallel pings to the zone endpoint and to two public resolvers, then compare the loss:

```bash theme={"system"}
# Run these at the same time, in separate terminals.
ping -i 0.5 ping.speedtest.[ZONE].coreweave.com
ping -i 0.5 1.1.1.1
ping -i 0.5 8.8.8.8
```

* Similar loss to all three targets points to your local network or internet service provider, not CoreWeave.
* Loss only to the CoreWeave endpoint points to the path toward CoreWeave. Gather the details and open a ticket.
* Loss to CoreWeave and one other target can indicate a routing problem at an intermediate provider.

To separate your local link from your provider, add a ping to your default gateway. Loss to the gateway points to your local link, such as wireless. No loss to the gateway but loss to internet targets points to your provider.

## Find your egress IP range to allowlist

When an external system must allow inbound connections from your CoreWeave workloads, allowlist the zone's NAT egress range. Confirm the current egress IP from a Node:

```bash theme={"system"}
# Show the public source IP your Node's traffic uses. Read-only.
curl -4 ifconfig.me
```

Then find the published range for your zone in [Regions and availability zones](https://docs.coreweave.com/platform/regions/about-regions-and-azs.md). If your cluster is in a dedicated, single-tenant zone, its egress range may not be on the public page. Contact support to confirm the range to allowlist.

## Kubernetes API server access

When you access a CKS cluster's Kubernetes API server over Direct Connect through the Traefik `traefik-k8s` Service, connect by the Service's hostname, not its private load balancer IP. For the hostname and certificate requirements, see [Traefik IngressRouteTCP and Kubernetes API proxy](https://docs.coreweave.com/products/cks/clusters/coreweave-charts/traefik.md#ingressroutetcp-and-kubernetes-api-proxy).

## Provisioning workflow

CoreWeave offers a hands-on provisioning experience where our Solutions Architects, Technical Solution Managers, and Engineers work directly with you. Provisioning happens in two stages: first you establish Layer 2 connectivity to a CoreWeave facility or on-ramp partner, then CoreWeave brings up Layer 3 BGP sessions across that connection. The following sections describe each stage.

### Layer 2 connectivity

How you establish Layer 2 connectivity depends on whether you use Dedicated DX or Virtual DX.

#### For Dedicated DX

Before requesting a dedicated DX connection, you must have an established production Org ID and a running CKS cluster.

To initiate the process, contact your Account Manager. They coordinate with you and our networking team to provision your connection and provide a Letter of Authorization (LOA). Using the CoreWeave LOA, you order Cross Connects (XCs) from the colocation provider to connect your equipment to CoreWeave.

If connecting to a hyperscaler, you must provide the hyperscaler's LOA to CoreWeave, and we order the XCs.

#### For Virtual DX

Creating a virtual connection is a manual process coordinated with our support team. Before initiating a connection in your provider's portal, contact your Account Manager. Provide them with your desired connection location, required bandwidth, and timeline. They coordinate with you and our networking team to provision your connection and provide a token or service key.

When those steps are complete, you can use the token or service key to order Virtual Connections (VCs) through the Equinix or Megaport portal. For detailed connection instructions, refer to the provider's documentation:

* **Equinix Fabric**: [Connect to a Service Provider](https://docs.equinix.com/fabric-marketplace/)
* **Megaport**: [Creating a Connection using a Service Key](https://docs.megaport.com/marketplace/create-connection-service-key/)

### Layer 3 (BGP) configuration

After Layer 2 connectivity is established, CoreWeave establishes Border Gateway Protocol (BGP) sessions. Before BGP sessions can be established, you must have a CKS cluster built and associated with a production Org ID.

We establish one BGP session per circuit by default. You must provide a list of prefixes and exact prefix lengths you intend to advertise. We implement exact-match import policies. If you advertise prefixes not on this list, or exceed the provided list, the BGP session is torn down.

| Configuration Parameter | Value details |
| - | - |
| Autonomous System Number (ASN) | Our BGP ASN is `33425`. Customers must inform us of their ASN. |
| IP Addressing | By default, we use `169.254.0.0/30`, with our DCR on `.1` and the customer's network equipment on `.2`. We support `/31` or `/30` CIDR ranges. |
| Pre-shared Key | Customers can choose to use a pre-shared key to authenticate BGP sessions. This is optional. |
| LACP | Customers can choose to create LAG. This is optional. |
| 802.1Q Tagging | Customers can choose to enable 802.1Q VLAN tagging. By default, we start at `101` for each of the customer VPCs, but this can be customized. |
| MACsec | If using Dedicated DX, customers can choose to enable MACsec between our DCRs and their network equipment over XCs |
| MTU Size | If using Dedicated DX, customers can choose an MTU size such as `1500` or `9000` for jumbo frames |

## Billing

Monthly recurring billing begins when the DX is established or 30 days after the LOA or token/service key is issued, whichever is sooner. Billing is based on the following:

* **DX Speed**: Billed based on the subscribed speed. Dedicated DX supports 10G, 100G, or 400G. Virtual DX supports 10G.
* **Cross Connects (Dedicated)**: CoreWeave passes through costs for any XCs we're required to order (such as hyperscaler connections). If you order the XC with the facility, no XC fee is billed by CoreWeave.
* **Data Transfer**: Free of charge.

For detailed pricing information, contact your CoreWeave Account Manager or refer to the [CoreWeave Cloud Pricing](https://www.coreweave.com/pricing) page.
