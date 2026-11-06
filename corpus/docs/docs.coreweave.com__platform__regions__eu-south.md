# EU-SOUTH

Source: https://docs.coreweave.com/platform/regions/eu-south

# EU-SOUTH

> Availability Zones in the CoreWeave EU-SOUTH super region, including Barcelona, Spain locations and access tiers.

## EU-SOUTH-01A

This is a Dedicated Access zone located in Barcelona, Spain. It is reserved for select customers.

## EU-SOUTH-03B

This is a General Access zone located in Barcelona, Spain. It is available to all customers.

Instances and AI Object Storage

| GPU Instances | CPU Instances | AI Object Storage |
| :- | :- | :- |
| [H200 (InfiniBand)](https://docs.coreweave.com/platform/instances/gpu/gd-8xh200ib-i128.md) | [General Purpose AMD Turin (High Memory)](https://docs.coreweave.com/platform/instances/cpu/turin-gp.md) [General Purpose Intel Emerald Rapids (High Memory)](https://docs.coreweave.com/platform/instances/cpu/cd-gp-i64-erapids.md) | Yes |
| Network information | | |

| Type | Address Range | Description |
| :- | :- | :- |
| **Public IP** | `83.228.136.0/22` | Public IP address range for this AZ |
| **NAT Egress** | `83.228.136.0/24`, `83.228.137.0/24` | Subset of the Public Range used for Service egress |
| **Node Range** | `10.206.192.0/18` | RFC 1918 private range used exclusively by this AZ |
| **Pods** | `10.0.0.0/13` | RFC 1918 space dedicated to all Pods |
| **Services** | `10.16.0.0/22` | Subset of Pod RFC 1918 space dedicated to Services |
| **Load Balancers** | `10.16.4.0/22` | Subset of Services RFC 1918 space dedicated to Load Balancers |
| [**Speedtest 1GB**](https://docs.coreweave.com/platform/regions/about-regions-and-azs.md#speedtest) | `http://http.speedtest.eu-south-03.coreweave.com/1G` | 1 GB test file for bandwidth testing |
| [**Speedtest 10GB**](https://docs.coreweave.com/platform/regions/about-regions-and-azs.md#speedtest) | `http://http.speedtest.eu-south-03.coreweave.com/10G` | 10 GB test file for bandwidth testing |
| [**ICMP Latency**](https://docs.coreweave.com/platform/regions/about-regions-and-azs.md#speedtest) | `ping.speedtest.eu-south-03.coreweave.com` | ICMP latency test address |

## EU-SOUTH-04A

This is a General Access zone located in Alava, Spain. It is available to all customers.

Instances and AI Object Storage

| GPU Instances | CPU Instances | AI Object Storage |
| :- | :- | :- |
| [B200 (InfiniBand)](https://docs.coreweave.com/platform/instances/gpu/b200-8x.md) [RTX PRO 6000 Blackwell Server Edition (High Memory)](https://docs.coreweave.com/platform/instances/gpu/rtxp6000-8x.md) | [General Purpose AMD Turin (High Memory)](https://docs.coreweave.com/platform/instances/cpu/turin-gp.md) [General Purpose Intel Emerald Rapids (High Memory)](https://docs.coreweave.com/platform/instances/cpu/cd-gp-i64-erapids.md) | Yes |
| Network information | | |

| Type | Address Range | Description |
| :- | :- | :- |
| **Public IP** | `83.228.144.0/22` | Public IP address range for this AZ |
| **NAT Egress** | `83.228.144.0/24`, `83.228.145.0/24` | Subset of the Public Range used for Service egress |
| **Node Range** | `10.104.192.0/18` | RFC 1918 private range used exclusively by this AZ |
| **Pods** | `10.0.0.0/13` | RFC 1918 space dedicated to all Pods |
| **Services** | `10.16.0.0/22` | Subset of Pod RFC 1918 space dedicated to Services |
| **Load Balancers** | `10.16.4.0/22` | Subset of Services RFC 1918 space dedicated to Load Balancers |
| [**Speedtest 1GB**](https://docs.coreweave.com/platform/regions/about-regions-and-azs.md#speedtest) | `http://http.speedtest.eu-south-04.coreweave.com/1G` | 1 GB test file for bandwidth testing |
| [**Speedtest 10GB**](https://docs.coreweave.com/platform/regions/about-regions-and-azs.md#speedtest) | `http://http.speedtest.eu-south-04.coreweave.com/10G` | 10 GB test file for bandwidth testing |
| [**ICMP Latency**](https://docs.coreweave.com/platform/regions/about-regions-and-azs.md#speedtest) | `ping.speedtest.eu-south-04.coreweave.com` | ICMP latency test address |
