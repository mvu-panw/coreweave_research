# US-WEST

Source: https://docs.coreweave.com/platform/regions/us-west

# US-WEST

> Availability Zones in the CoreWeave US-WEST super region, including locations in Oregon and Nevada and access tiers.

## PDX2A

This is a Dedicated Access zone located in Oregon, USA. It is reserved for select customers.

## RNO2A

This is a General Access zone located in Nevada, USA. It is available to all customers.

Instances and AI Object Storage

| GPU Instances | CPU Instances | AI Object Storage |
| :- | :- | :- |
| [H100 (InfiniBand)](https://docs.coreweave.com/platform/instances/gpu/gd-8xh100ib-i128.md) [L40](https://docs.coreweave.com/platform/instances/gpu/gd-8xl40-i128.md) [GH200](https://docs.coreweave.com/platform/instances/gpu/gd-1xgh200.md) [A100](https://docs.coreweave.com/platform/instances/gpu/gd-8xa100-i128.md) | [General Purpose AMD Genoa](https://docs.coreweave.com/platform/instances/cpu/cd-gp-a192-genoa.md) [General Purpose AMD Turin (High Storage)](https://docs.coreweave.com/platform/instances/cpu/turin-gp-l.md) [General Purpose AMD Turin (High Memory)](https://docs.coreweave.com/platform/instances/cpu/turin-gp.md) [General Purpose Intel Ice Lake](https://docs.coreweave.com/platform/instances/cpu/cd-gp-i96-icelake.md) | Yes |
| Network information | | |

| Type | Address Range | Description |
| :- | :- | :- |
| **Public IP** | `192.112.164.0/23` | Public IP address range for this AZ |
| **NAT Egress** | `192.112.165.128/25` | Subset of the Public Range used for Service egress |
| **Node Range** | `10.168.192.0/18` | RFC 1918 private range used exclusively by this AZ |
| **Pods** | `10.0.0.0/13` | RFC 1918 space dedicated to all Pods |
| **Services** | `10.16.0.0/22` | Subset of Pod RFC 1918 space dedicated to Services |
| **Load Balancers** | `10.16.4.0/22` | Subset of Services RFC 1918 space dedicated to Load Balancers |
| [**Speedtest 1GB**](https://docs.coreweave.com/platform/regions/about-regions-and-azs.md#speedtest) | `http://http.speedtest.rno2.coreweave.com/1G` | 1 GB test file for bandwidth testing |
| [**Speedtest 10GB**](https://docs.coreweave.com/platform/regions/about-regions-and-azs.md#speedtest) | `http://http.speedtest.rno2.coreweave.com/10G` | 10 GB test file for bandwidth testing |
| [**ICMP Latency**](https://docs.coreweave.com/platform/regions/about-regions-and-azs.md#speedtest) | `ping.speedtest.rno2.coreweave.com` | ICMP latency test address |

## US-WEST-01A

This is a General Access zone located in Nevada, USA. It is available to all customers.

Instances and AI Object Storage

| GPU Instances | CPU Instances | AI Object Storage |
| :- | :- | :- |
| [GB300 NVL72 Quantum-X InfiniBand](https://docs.coreweave.com/platform/instances/gpu/gb300-4x.md) [GB200 NVL72-powered instances](https://docs.coreweave.com/platform/instances/gpu/gb200-4x.md) [B300 (InfiniBand)](https://docs.coreweave.com/platform/instances/gpu/b300-8x.md) [H100 (InfiniBand)](https://docs.coreweave.com/platform/instances/gpu/gd-8xh100ib-i128.md) [RTX PRO 6000 Blackwell Server Edition (High Memory)](https://docs.coreweave.com/platform/instances/gpu/rtxp6000-8x.md) | [General Purpose AMD Genoa](https://docs.coreweave.com/platform/instances/cpu/cd-gp-a192-genoa.md) [General Purpose Intel Emerald Rapids (High Memory)](https://docs.coreweave.com/platform/instances/cpu/cd-gp-i64-erapids.md) | Yes |
| Network information | | |

| Type | Address Range | Description |
| :- | :- | :- |
| **Public IP** | `166.19.28.0/22` | Public IP address range for this AZ |
| **NAT Egress** | `166.19.28.0/23` | Subset of the Public Range used for Service egress |
| **Node Range** | `10.188.192.0/18` | RFC 1918 private range used exclusively by this AZ |
| **Pods** | `10.0.0.0/13` | RFC 1918 space dedicated to all Pods |
| **Services** | `10.16.0.0/22` | Subset of Pod RFC 1918 space dedicated to Services |
| **Load Balancers** | `10.16.4.0/22` | Subset of Services RFC 1918 space dedicated to Load Balancers |
| [**Speedtest 1GB**](https://docs.coreweave.com/platform/regions/about-regions-and-azs.md#speedtest) | `http://http.speedtest.us-west-01.coreweave.com/1G` | 1 GB test file for bandwidth testing |
| [**Speedtest 10GB**](https://docs.coreweave.com/platform/regions/about-regions-and-azs.md#speedtest) | `http://http.speedtest.us-west-01.coreweave.com/10G` | 10 GB test file for bandwidth testing |
| [**ICMP Latency**](https://docs.coreweave.com/platform/regions/about-regions-and-azs.md#speedtest) | `ping.speedtest.us-west-01.coreweave.com` | ICMP latency test address |

## US-WEST-02A

This is a Dedicated Access zone located in Arizona, USA. It is reserved for select customers.

## US-WEST-02B

This is a General Access zone located in Arizona, USA. It is available to all customers.

Instances and AI Object Storage

| GPU Instances | CPU Instances | AI Object Storage |
| :- | :- | :- |
| [H100 (InfiniBand)](https://docs.coreweave.com/platform/instances/gpu/gd-8xh100ib-i128.md) | | |
| Network information | | |

| Type | Address Range | Description |
| :- | :- | :- |
| **Public IP** | `166.19.96.0/22` | Public IP address range for this AZ |
| **NAT Egress** | `166.19.96.0/24`, `166.19.97.0/24` | Subset of the Public Range used for Service egress |
| **Node Range** | `10.112.192.0/18` | RFC 1918 private range used exclusively by this AZ |
| **Pods** | `10.0.0.0/13` | RFC 1918 space dedicated to all Pods |
| **Services** | `10.16.0.0/22` | Subset of Pod RFC 1918 space dedicated to Services |
| **Load Balancers** | `10.16.4.0/22` | Subset of Services RFC 1918 space dedicated to Load Balancers |
| [**Speedtest 1GB**](https://docs.coreweave.com/platform/regions/about-regions-and-azs.md#speedtest) | `http://http.speedtest.us-west-02.coreweave.com/1G` | 1 GB test file for bandwidth testing |
| [**Speedtest 10GB**](https://docs.coreweave.com/platform/regions/about-regions-and-azs.md#speedtest) | `http://http.speedtest.us-west-02.coreweave.com/10G` | 10 GB test file for bandwidth testing |
| [**ICMP Latency**](https://docs.coreweave.com/platform/regions/about-regions-and-azs.md#speedtest) | `ping.speedtest.us-west-02.coreweave.com` | ICMP latency test address |

## US-WEST-03A

This is a Dedicated Access zone located in Oregon, USA. It is reserved for select customers.

## US-WEST-04A

This is a General Access zone located in Arizona, USA. It is available to all customers.

Instances and AI Object Storage

| GPU Instances | CPU Instances | AI Object Storage |
| :- | :- | :- |
| [H200 (InfiniBand)](https://docs.coreweave.com/platform/instances/gpu/gd-8xh200ib-i128.md) [H100 (InfiniBand)](https://docs.coreweave.com/platform/instances/gpu/gd-8xh100ib-i128.md) [RTX PRO 6000 Blackwell Server Edition (High Memory)](https://docs.coreweave.com/platform/instances/gpu/rtxp6000-8x.md) | [General Purpose AMD Genoa](https://docs.coreweave.com/platform/instances/cpu/cd-gp-a192-genoa.md) [General Purpose Intel Emerald Rapids (High Memory)](https://docs.coreweave.com/platform/instances/cpu/cd-gp-i64-erapids.md) | Yes |
| Network information | | |

| Type | Address Range | Description |
| :- | :- | :- |
| **Public IP** | `166.19.32.0/22` | Public IP address range for this AZ |
| **NAT Egress** | `166.19.32.0/24`, `166.19.33.0/24` | Subset of the Public Range used for Service egress |
| **Node Range** | `10.190.192.0/18` | RFC 1918 private range used exclusively by this AZ |
| **Pods** | `10.0.0.0/13` | RFC 1918 space dedicated to all Pods |
| **Services** | `10.16.0.0/22` | Subset of Pod RFC 1918 space dedicated to Services |
| **Load Balancers** | `10.16.4.0/22` | Subset of Services RFC 1918 space dedicated to Load Balancers |
| [**Speedtest 1GB**](https://docs.coreweave.com/platform/regions/about-regions-and-azs.md#speedtest) | `http://http.speedtest.us-west-04.coreweave.com/1G` | 1 GB test file for bandwidth testing |
| [**Speedtest 10GB**](https://docs.coreweave.com/platform/regions/about-regions-and-azs.md#speedtest) | `http://http.speedtest.us-west-04.coreweave.com/10G` | 10 GB test file for bandwidth testing |
| [**ICMP Latency**](https://docs.coreweave.com/platform/regions/about-regions-and-azs.md#speedtest) | `ping.speedtest.us-west-04.coreweave.com` | ICMP latency test address |

## US-WEST-05A

This is a Dedicated Access zone located in Washington, USA. It is reserved for select customers.

## US-WEST-06A

This is a Dedicated Access zone located in Oregon, USA. It is reserved for select customers.

## US-WEST-07A

This is a Dedicated Access zone located in Colorado, USA. It is reserved for select customers.

## US-WEST-08A

This is a Dedicated Access zone located in California, USA. It is reserved for select customers.

## US-WEST-09B

This is a General Access zone located in Washington, USA. It is available to all customers.

Instances and AI Object Storage

| GPU Instances | CPU Instances | AI Object Storage |
| :- | :- | :- |
| [B200 (InfiniBand)](https://docs.coreweave.com/platform/instances/gpu/b200-8x.md) [H100 (InfiniBand)](https://docs.coreweave.com/platform/instances/gpu/gd-8xh100ib-i128.md) [RTX PRO 6000 Blackwell Server Edition (High Memory)](https://docs.coreweave.com/platform/instances/gpu/rtxp6000-8x.md) | [General Purpose AMD Turin (High Memory)](https://docs.coreweave.com/platform/instances/cpu/turin-gp.md) [General Purpose Intel Emerald Rapids (High Memory)](https://docs.coreweave.com/platform/instances/cpu/cd-gp-i64-erapids.md) | Yes |
| Network information | | |

| Type | Address Range | Description |
| :- | :- | :- |
| **Public IP** | `166.19.80.0/22` | Public IP address range for this AZ |
| **NAT Egress** | `166.19.80.0/24`, `166.19.81.0/24` | Subset of the Public Range used for Service egress |
| **Node Range** | `10.210.192.0/18` | RFC 1918 private range used exclusively by this AZ |
| **Pods** | `10.0.0.0/13` | RFC 1918 space dedicated to all Pods |
| **Services** | `10.16.0.0/22` | Subset of Pod RFC 1918 space dedicated to Services |
| **Load Balancers** | `10.16.4.0/22` | Subset of Services RFC 1918 space dedicated to Load Balancers |
| [**Speedtest 1GB**](https://docs.coreweave.com/platform/regions/about-regions-and-azs.md#speedtest) | `http://http.speedtest.us-west-09.coreweave.com/1G` | 1 GB test file for bandwidth testing |
| [**Speedtest 10GB**](https://docs.coreweave.com/platform/regions/about-regions-and-azs.md#speedtest) | `http://http.speedtest.us-west-09.coreweave.com/10G` | 10 GB test file for bandwidth testing |
| [**ICMP Latency**](https://docs.coreweave.com/platform/regions/about-regions-and-azs.md#speedtest) | `ping.speedtest.us-west-09.coreweave.com` | ICMP latency test address |

## US-WEST-10A

This is a General Access zone located in Nevada, USA. It is available to all customers.

Instances and AI Object Storage

| GPU Instances | CPU Instances | AI Object Storage |
| :- | :- | :- |
| [B300 (InfiniBand)](https://docs.coreweave.com/platform/instances/gpu/b300-8x.md) [RTX PRO 6000 Blackwell Server Edition (High Memory)](https://docs.coreweave.com/platform/instances/gpu/rtxp6000-8x.md) | [General Purpose AMD Turin (High Memory)](https://docs.coreweave.com/platform/instances/cpu/turin-gp.md) [General Purpose Intel Emerald Rapids (High Memory)](https://docs.coreweave.com/platform/instances/cpu/cd-gp-i64-erapids.md) | Yes |
| Network information | | |

| Type | Address Range | Description |
| :- | :- | :- |
| **Public IP** | `166.19.132.0/22` | Public IP address range for this AZ |
| **NAT Egress** | `166.19.132.0/24`, `166.19.133.0/24` | Subset of the Public Range used for Service egress |
| **Node Range** | `10.57.128.0/17` | RFC 1918 private range used exclusively by this AZ |
| **Pods** | `10.0.0.0/13` | RFC 1918 space dedicated to all Pods |
| **Services** | `10.16.0.0/22` | Subset of Pod RFC 1918 space dedicated to Services |
| **Load Balancers** | `10.16.4.0/22` | Subset of Services RFC 1918 space dedicated to Load Balancers |
| [**Speedtest 1GB**](https://docs.coreweave.com/platform/regions/about-regions-and-azs.md#speedtest) | `http://http.speedtest.us-west-10.coreweave.com/1G` | 1 GB test file for bandwidth testing |
| [**Speedtest 10GB**](https://docs.coreweave.com/platform/regions/about-regions-and-azs.md#speedtest) | `http://http.speedtest.us-west-10.coreweave.com/10G` | 10 GB test file for bandwidth testing |
| [**ICMP Latency**](https://docs.coreweave.com/platform/regions/about-regions-and-azs.md#speedtest) | `ping.speedtest.us-west-10.coreweave.com` | ICMP latency test address |
