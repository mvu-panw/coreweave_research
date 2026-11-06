# US-CENTRAL

Source: https://docs.coreweave.com/platform/regions/us-central

# US-CENTRAL

> Availability Zones in the CoreWeave US-CENTRAL super region, including locations in Texas, Indiana, and Illinois.

## AUS1A

This is a Dedicated Access zone located in Texas, USA. It is reserved for select customers.

## DFW1A

This is a Dedicated Access zone located in Texas, USA. It is reserved for select customers.

## SBN1A

This is a Dedicated Access zone located in Indiana, USA. It is reserved for select customers.

## US-CENTRAL-01A

This is a Dedicated Access zone located in Illinois, USA. It is reserved for select customers.

## US-CENTRAL-02A

This is a Dedicated Access zone located in Texas, USA. It is reserved for select customers.

## US-CENTRAL-03A

This is a Dedicated Access zone located in Texas, USA. It is reserved for select customers.

## US-CENTRAL-04A

This is a Dedicated Access zone located in Texas, USA. It is reserved for select customers.

## US-CENTRAL-05A

This is a Dedicated Access zone located in Texas, USA. It is reserved for select customers.

AI Object Storage is available.

## US-CENTRAL-06A

This is a General Access zone located in Texas, USA. It is available to all customers.

Instances and AI Object Storage

| GPU Instances | CPU Instances | AI Object Storage |
| :- | :- | :- |
| [B300 (InfiniBand)](https://docs.coreweave.com/platform/instances/gpu/b300-8x.md) [H100 (InfiniBand)](https://docs.coreweave.com/platform/instances/gpu/gd-8xh100ib-i128.md) | [General Purpose AMD Turin (High Memory)](https://docs.coreweave.com/platform/instances/cpu/turin-gp.md) [General Purpose Intel Emerald Rapids (High Memory)](https://docs.coreweave.com/platform/instances/cpu/cd-gp-i64-erapids.md) | Yes |
| Network information | | |

| Type | Address Range | Description |
| :- | :- | :- |
| **Public IP** | `166.19.152.0/22` | Public IP address range for this AZ |
| **NAT Egress** | `166.19.152.0/24`, `166.19.153.0/24` | Subset of the Public Range used for Service egress |
| **Node Range** | `10.51.128.0/17` | RFC 1918 private range used exclusively by this AZ |
| **Pods** | `10.0.0.0/13` | RFC 1918 space dedicated to all Pods |
| **Services** | `10.16.0.0/22` | Subset of Pod RFC 1918 space dedicated to Services |
| **Load Balancers** | `10.16.4.0/22` | Subset of Services RFC 1918 space dedicated to Load Balancers |
| [**Speedtest 1GB**](https://docs.coreweave.com/platform/regions/about-regions-and-azs.md#speedtest) | `http://http.speedtest.us-central-06.coreweave.com/1G` | 1 GB test file for bandwidth testing |
| [**Speedtest 10GB**](https://docs.coreweave.com/platform/regions/about-regions-and-azs.md#speedtest) | `http://http.speedtest.us-central-06.coreweave.com/10G` | 10 GB test file for bandwidth testing |
| [**ICMP Latency**](https://docs.coreweave.com/platform/regions/about-regions-and-azs.md#speedtest) | `ping.speedtest.us-central-06.coreweave.com` | ICMP latency test address |

## US-CENTRAL-07A

This is a General Access zone located in Illinois, USA. It is available to all customers.

Instances and AI Object Storage

| GPU Instances | CPU Instances | AI Object Storage |
| :- | :- | :- |
| [GB300 NVL72 Quantum-X InfiniBand](https://docs.coreweave.com/platform/instances/gpu/gb300-4x.md) [B200 (InfiniBand)](https://docs.coreweave.com/platform/instances/gpu/b200-8x.md) | [General Purpose AMD Turin (High Memory)](https://docs.coreweave.com/platform/instances/cpu/turin-gp.md) [General Purpose Intel Emerald Rapids (High Memory)](https://docs.coreweave.com/platform/instances/cpu/cd-gp-i64-erapids.md) | Yes |
| Network information | | |

| Type | Address Range | Description |
| :- | :- | :- |
| **Public IP** | `166.19.112.0/22` | Public IP address range for this AZ |
| **NAT Egress** | `166.19.112.0/24`, `166.19.113.0/24` | Subset of the Public Range used for Service egress |
| **Node Range** | `10.109.128.0/18` | RFC 1918 private range used exclusively by this AZ |
| **Pods** | `10.0.0.0/13` | RFC 1918 space dedicated to all Pods |
| **Services** | `10.16.0.0/22` | Subset of Pod RFC 1918 space dedicated to Services |
| **Load Balancers** | `10.16.4.0/22` | Subset of Services RFC 1918 space dedicated to Load Balancers |
| [**Speedtest 1GB**](https://docs.coreweave.com/platform/regions/about-regions-and-azs.md#speedtest) | `http://http.speedtest.us-central-07.coreweave.com/1G` | 1 GB test file for bandwidth testing |
| [**Speedtest 10GB**](https://docs.coreweave.com/platform/regions/about-regions-and-azs.md#speedtest) | `http://http.speedtest.us-central-07.coreweave.com/10G` | 10 GB test file for bandwidth testing |
| [**ICMP Latency**](https://docs.coreweave.com/platform/regions/about-regions-and-azs.md#speedtest) | `ping.speedtest.us-central-07.coreweave.com` | ICMP latency test address |

## US-CENTRAL-08A

This is a Dedicated Access zone located in North Dakota, USA. It is reserved for select customers.

AI Object Storage is available.

## US-CENTRAL-08B

This is a Dedicated Access zone located in North Dakota, USA. It is reserved for select customers.

AI Object Storage is available.

## US-CENTRAL-09A

This is a General Access zone located in Texas, USA. It is available to all customers.

Instances and AI Object Storage

| GPU Instances | CPU Instances | AI Object Storage |
| :- | :- | :- |
| [Vera Rubin NVL72 Spectrum-X RoCE](https://docs.coreweave.com/platform/instances/gpu/verarubin-4x-e.md) [GB300 NVL72 Quantum-X InfiniBand](https://docs.coreweave.com/platform/instances/gpu/gb300-4x.md) | [General Purpose AMD Turin (High Memory)](https://docs.coreweave.com/platform/instances/cpu/turin-gp.md) [General Purpose AMD Turin (High Storage)](https://docs.coreweave.com/platform/instances/cpu/turin-gp-l.md) | |
| Network information | | |

| Type | Address Range | Description |
| :- | :- | :- |
| **Public IP** | `166.19.128.0/22` | Public IP address range for this AZ |
| **NAT Egress** | `166.19.128.0/24`, `166.19.129.0/24` | Subset of the Public Range used for Service egress |
| **Pods** | `10.0.0.0/13` | RFC 1918 space dedicated to all Pods |
| **Services** | `10.16.0.0/22` | Subset of Pod RFC 1918 space dedicated to Services |
| **Load Balancers** | `10.16.4.0/22` | Subset of Services RFC 1918 space dedicated to Load Balancers |
| [**Speedtest 1GB**](https://docs.coreweave.com/platform/regions/about-regions-and-azs.md#speedtest) | `http://http.speedtest.us-central-09.coreweave.com/1G` | 1 GB test file for bandwidth testing |
| [**Speedtest 10GB**](https://docs.coreweave.com/platform/regions/about-regions-and-azs.md#speedtest) | `http://http.speedtest.us-central-09.coreweave.com/10G` | 10 GB test file for bandwidth testing |
| [**ICMP Latency**](https://docs.coreweave.com/platform/regions/about-regions-and-azs.md#speedtest) | `ping.speedtest.us-central-09.coreweave.com` | ICMP latency test address |

## US-CENTRAL-10A

This is a Dedicated Access zone located in Oklahoma, USA. It is reserved for select customers.

## US-CENTRAL-11A

This is a Dedicated Access zone located in Ohio, USA. It is reserved for select customers.
