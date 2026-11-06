# US-EAST

Source: https://docs.coreweave.com/platform/regions/us-east

# US-EAST

> Availability Zones in the CoreWeave US-EAST super region, including locations in Georgia, Virginia, and New York.

## ATL2A

This is a Dedicated Access zone located in Georgia, USA. It is reserved for select customers.

## ATL4A

This is a Dedicated Access zone located in Georgia, USA. It is reserved for select customers.

## RDU1A

This is a Dedicated Access zone located in Virginia, USA. It is reserved for select customers.

## US-EAST-01A

This is a General Access zone located in New York, USA. It is available to all customers.

Instances and AI Object Storage

| GPU Instances | CPU Instances | AI Object Storage |
| :- | :- | :- |
| [GB200 NVL72-powered instances](https://docs.coreweave.com/platform/instances/gpu/gb200-4x.md) [H200 (InfiniBand)](https://docs.coreweave.com/platform/instances/gpu/gd-8xh200ib-i128.md) [H100 (InfiniBand)](https://docs.coreweave.com/platform/instances/gpu/gd-8xh100ib-i128.md) [RTX PRO 6000 Blackwell Server Edition (High Memory)](https://docs.coreweave.com/platform/instances/gpu/rtxp6000-8x.md) | [General Purpose AMD Turin (High Memory)](https://docs.coreweave.com/platform/instances/cpu/turin-gp.md) [General Purpose Intel Emerald Rapids (High Memory)](https://docs.coreweave.com/platform/instances/cpu/cd-gp-i64-erapids.md) | Yes |
| Network information | | |

| Type | Address Range | Description |
| :- | :- | :- |
| **Public IP** | `166.19.48.0/22` | Public IP address range for this AZ |
| **NAT Egress** | `166.19.48.0/24`, `166.19.49.0/24` | Subset of the Public Range used for Service egress |
| **Node Range** | `10.202.192.0/18` | RFC 1918 private range used exclusively by this AZ |
| **Pods** | `10.0.0.0/13` | RFC 1918 space dedicated to all Pods |
| **Services** | `10.16.0.0/22` | Subset of Pod RFC 1918 space dedicated to Services |
| **Load Balancers** | `10.16.4.0/22` | Subset of Services RFC 1918 space dedicated to Load Balancers |
| [**Speedtest 1GB**](https://docs.coreweave.com/platform/regions/about-regions-and-azs.md#speedtest) | `http://http.speedtest.us-east-01.coreweave.com/1G` | 1 GB test file for bandwidth testing |
| [**Speedtest 10GB**](https://docs.coreweave.com/platform/regions/about-regions-and-azs.md#speedtest) | `http://http.speedtest.us-east-01.coreweave.com/10G` | 10 GB test file for bandwidth testing |
| [**ICMP Latency**](https://docs.coreweave.com/platform/regions/about-regions-and-azs.md#speedtest) | `ping.speedtest.us-east-01.coreweave.com` | ICMP latency test address |

## US-EAST-02A

This is a General Access zone located in New Jersey, USA. It is available to all customers.

Instances and AI Object Storage

| GPU Instances | CPU Instances | AI Object Storage |
| :- | :- | :- |
| [GB200 NVL72-powered instances](https://docs.coreweave.com/platform/instances/gpu/gb200-4x.md) [H200 (InfiniBand)](https://docs.coreweave.com/platform/instances/gpu/gd-8xh200ib-i128.md) [H100 (InfiniBand)](https://docs.coreweave.com/platform/instances/gpu/gd-8xh100ib-i128.md) [L40](https://docs.coreweave.com/platform/instances/gpu/gd-8xl40-i128.md) | [General Purpose AMD Genoa](https://docs.coreweave.com/platform/instances/cpu/cd-gp-a192-genoa.md) [General Purpose AMD Turin (High Memory)](https://docs.coreweave.com/platform/instances/cpu/turin-gp.md) [General Purpose AMD Turin (High Storage)](https://docs.coreweave.com/platform/instances/cpu/turin-gp-l.md) | Yes |
| Network information | | |

| Type | Address Range | Description |
| :- | :- | :- |
| **Public IP** | `166.19.8.0/23` | Public IP address range for this AZ |
| **NAT Egress** | `166.19.8.192/26` | Subset of the Public Range used for Service egress |
| **Node Range** | `10.184.192.0/18` | RFC 1918 private range used exclusively by this AZ |
| **Pods** | `10.0.0.0/13` | RFC 1918 space dedicated to all Pods |
| **Services** | `10.16.0.0/22` | Subset of Pod RFC 1918 space dedicated to Services |
| **Load Balancers** | `10.16.4.0/22` | Subset of Services RFC 1918 space dedicated to Load Balancers |
| [**Speedtest 1GB**](https://docs.coreweave.com/platform/regions/about-regions-and-azs.md#speedtest) | `http://http.speedtest.us-east-02.coreweave.com/1G` | 1 GB test file for bandwidth testing |
| [**Speedtest 10GB**](https://docs.coreweave.com/platform/regions/about-regions-and-azs.md#speedtest) | `http://http.speedtest.us-east-02.coreweave.com/10G` | 10 GB test file for bandwidth testing |
| [**ICMP Latency**](https://docs.coreweave.com/platform/regions/about-regions-and-azs.md#speedtest) | `ping.speedtest.us-east-02.coreweave.com` | ICMP latency test address |

## US-EAST-02B

This is a Dedicated Access zone located in New Jersey, USA. It is reserved for select customers.

## US-EAST-03A

This is a Dedicated Access zone located in Pennsylvania, USA. It is reserved for select customers.

AI Object Storage is available.

## US-EAST-04A

This is a General Access zone located in Virginia, USA. It is available to all customers.

Instances and AI Object Storage

| GPU Instances | CPU Instances | AI Object Storage |
| :- | :- | :- |
| [H200 (InfiniBand)](https://docs.coreweave.com/platform/instances/gpu/gd-8xh200ib-i128.md) [H100 (InfiniBand)](https://docs.coreweave.com/platform/instances/gpu/gd-8xh100ib-i128.md) [RTX PRO 6000 Blackwell Server Edition (High Memory)](https://docs.coreweave.com/platform/instances/gpu/rtxp6000-8x.md) [L40S](https://docs.coreweave.com/platform/instances/gpu/gd-8xl40s-i128.md) [L40](https://docs.coreweave.com/platform/instances/gpu/gd-8xl40-i128.md) [GH200](https://docs.coreweave.com/platform/instances/gpu/gd-1xgh200.md) [A100](https://docs.coreweave.com/platform/instances/gpu/gd-8xa100-i128.md) | [High Performance AMD Genoa](https://docs.coreweave.com/platform/instances/cpu/cd-hp-a96-genoa.md) [High Core AMD Genoa](https://docs.coreweave.com/platform/instances/cpu/cd-hc-a384-genoa.md) [High Core AMD Genoa (InfiniBand)](https://docs.coreweave.com/platform/instances/cpu/cd-hc-a384ib-genoa.md) [General Purpose AMD Turin (High Memory)](https://docs.coreweave.com/platform/instances/cpu/turin-gp.md) [General Purpose AMD Turin (High Storage)](https://docs.coreweave.com/platform/instances/cpu/turin-gp-l.md) [General Purpose Intel Emerald Rapids (High Memory)](https://docs.coreweave.com/platform/instances/cpu/cd-gp-i64-erapids.md) | Yes |
| Network information | | |

| Type | Address Range | Description |
| :- | :- | :- |
| **Public IP** | `166.19.10.0/23`, `166.19.16.0/21` | Public IP address range for this AZ |
| **NAT Egress** | `166.19.10.192/26`, `166.19.19.0/24` | Subset of the Public Range used for Service egress |
| **Node Range** | `10.176.192.0/18` | RFC 1918 private range used exclusively by this AZ |
| **Pods** | `10.0.0.0/13` | RFC 1918 space dedicated to all Pods |
| **Services** | `10.16.0.0/22` | Subset of Pod RFC 1918 space dedicated to Services |
| **Load Balancers** | `10.16.4.0/22` | Subset of Services RFC 1918 space dedicated to Load Balancers |
| [**Speedtest 1GB**](https://docs.coreweave.com/platform/regions/about-regions-and-azs.md#speedtest) | `http://http.speedtest.us-east-04.coreweave.com/1G` | 1 GB test file for bandwidth testing |
| [**Speedtest 10GB**](https://docs.coreweave.com/platform/regions/about-regions-and-azs.md#speedtest) | `http://http.speedtest.us-east-04.coreweave.com/10G` | 10 GB test file for bandwidth testing |
| [**ICMP Latency**](https://docs.coreweave.com/platform/regions/about-regions-and-azs.md#speedtest) | `ping.speedtest.us-east-04.coreweave.com` | ICMP latency test address |

## US-EAST-04B

This is a Dedicated Access zone located in Virginia, USA. It is reserved for select customers.

AI Object Storage is available.

## US-EAST-05A

This is a Dedicated Access zone located in Georgia, USA. It is reserved for select customers.

## US-EAST-06A

This is a General Access zone located in Ohio, USA. It is available to all customers.

Instances and AI Object Storage

| GPU Instances | CPU Instances | AI Object Storage |
| :- | :- | :- |
| [H100 (InfiniBand)](https://docs.coreweave.com/platform/instances/gpu/gd-8xh100ib-i128.md) [RTX PRO 6000 Blackwell Server Edition (High Memory)](https://docs.coreweave.com/platform/instances/gpu/rtxp6000-8x.md) | [General Purpose AMD Genoa](https://docs.coreweave.com/platform/instances/cpu/cd-gp-a192-genoa.md) [General Purpose AMD Turin (High Memory)](https://docs.coreweave.com/platform/instances/cpu/turin-gp.md) [General Purpose Intel Emerald Rapids (High Memory)](https://docs.coreweave.com/platform/instances/cpu/cd-gp-i64-erapids.md) | Yes |
| Network information | | |

| Type | Address Range | Description |
| :- | :- | :- |
| **Public IP** | `166.19.36.0/22` | Public IP address range for this AZ |
| **NAT Egress** | `166.19.36.0/24`, `166.19.37.0/24` | Subset of the Public Range used for Service egress |
| **Node Range** | `10.192.192.0/18` | RFC 1918 private range used exclusively by this AZ |
| **Pods** | `10.0.0.0/13` | RFC 1918 space dedicated to all Pods |
| **Services** | `10.16.0.0/22` | Subset of Pod RFC 1918 space dedicated to Services |
| **Load Balancers** | `10.16.4.0/22` | Subset of Services RFC 1918 space dedicated to Load Balancers |
| [**Speedtest 1GB**](https://docs.coreweave.com/platform/regions/about-regions-and-azs.md#speedtest) | `http://http.speedtest.us-east-06.coreweave.com/1G` | 1 GB test file for bandwidth testing |
| [**Speedtest 10GB**](https://docs.coreweave.com/platform/regions/about-regions-and-azs.md#speedtest) | `http://http.speedtest.us-east-06.coreweave.com/10G` | 10 GB test file for bandwidth testing |
| [**ICMP Latency**](https://docs.coreweave.com/platform/regions/about-regions-and-azs.md#speedtest) | `ping.speedtest.us-east-06.coreweave.com` | ICMP latency test address |

## US-EAST-07A

This is a Dedicated Access zone located in Ohio, USA. It is reserved for select customers.

## US-EAST-08A

This is a General Access zone located in Ohio, USA. It is available to all customers.

Instances and AI Object Storage

| GPU Instances | CPU Instances | AI Object Storage |
| :- | :- | :- |
| [GB200 NVL72-powered instances](https://docs.coreweave.com/platform/instances/gpu/gb200-4x.md) [H200 (InfiniBand)](https://docs.coreweave.com/platform/instances/gpu/gd-8xh200ib-i128.md) | [General Purpose AMD Genoa (High Storage)](https://docs.coreweave.com/platform/instances/cpu/cd-gp-l-a192-genoa.md) [General Purpose Intel Emerald Rapids (High Memory)](https://docs.coreweave.com/platform/instances/cpu/cd-gp-i64-erapids.md) | Yes |
| Network information | | |

| Type | Address Range | Description |
| :- | :- | :- |
| **Public IP** | `166.19.12.0/22` | Public IP address range for this AZ |
| **NAT Egress** | `166.19.12.0/24`, `166.19.13.0/24` | Subset of the Public Range used for Service egress |
| **Node Range** | `10.186.192.0/18` | RFC 1918 private range used exclusively by this AZ |
| **Pods** | `10.0.0.0/13` | RFC 1918 space dedicated to all Pods |
| **Services** | `10.16.0.0/22` | Subset of Pod RFC 1918 space dedicated to Services |
| **Load Balancers** | `10.16.4.0/22` | Subset of Services RFC 1918 space dedicated to Load Balancers |
| [**Speedtest 1GB**](https://docs.coreweave.com/platform/regions/about-regions-and-azs.md#speedtest) | `http://http.speedtest.us-east-08.coreweave.com/1G` | 1 GB test file for bandwidth testing |
| [**Speedtest 10GB**](https://docs.coreweave.com/platform/regions/about-regions-and-azs.md#speedtest) | `http://http.speedtest.us-east-08.coreweave.com/10G` | 10 GB test file for bandwidth testing |
| [**ICMP Latency**](https://docs.coreweave.com/platform/regions/about-regions-and-azs.md#speedtest) | `ping.speedtest.us-east-08.coreweave.com` | ICMP latency test address |

## US-EAST-09A

This is a Dedicated Access zone located in Georgia, USA. It is reserved for select customers.

## US-EAST-10A

This is a Dedicated Access zone located in Massachusetts, USA. It is reserved for select customers.

## US-EAST-11A

This is a Dedicated Access zone located in North Carolina, USA. It is reserved for select customers.

## US-EAST-12A

This is a Dedicated Access zone located in Georgia, USA. It is reserved for select customers.

## US-EAST-13A

This is a General Access zone located in Michigan, USA. It is available to all customers.

Instances and AI Object Storage

| GPU Instances | CPU Instances | AI Object Storage |
| :- | :- | :- |
| [GB200 NVL72-powered instances](https://docs.coreweave.com/platform/instances/gpu/gb200-4x.md) [B300 (InfiniBand)](https://docs.coreweave.com/platform/instances/gpu/b300-8x.md) [B200 (InfiniBand)](https://docs.coreweave.com/platform/instances/gpu/b200-8x.md) [RTX PRO 6000 Blackwell Server Edition (High Memory)](https://docs.coreweave.com/platform/instances/gpu/rtxp6000-8x.md) | [General Purpose AMD Turin (High Memory)](https://docs.coreweave.com/platform/instances/cpu/turin-gp.md) | Yes |
| Network information | | |

| Type | Address Range | Description |
| :- | :- | :- |
| **Public IP** | `166.19.88.0/22` | Public IP address range for this AZ |
| **NAT Egress** | `166.19.88.0/24`, `166.19.89.0/24` | Subset of the Public Range used for Service egress |
| **Node Range** | `10.221.128.0/18` | RFC 1918 private range used exclusively by this AZ |
| **Pods** | `10.0.0.0/13` | RFC 1918 space dedicated to all Pods |
| **Services** | `10.16.0.0/22` | Subset of Pod RFC 1918 space dedicated to Services |
| **Load Balancers** | `10.16.4.0/22` | Subset of Services RFC 1918 space dedicated to Load Balancers |
| [**Speedtest 1GB**](https://docs.coreweave.com/platform/regions/about-regions-and-azs.md#speedtest) | `http://http.speedtest.us-east-13.coreweave.com/1G` | 1 GB test file for bandwidth testing |
| [**Speedtest 10GB**](https://docs.coreweave.com/platform/regions/about-regions-and-azs.md#speedtest) | `http://http.speedtest.us-east-13.coreweave.com/10G` | 10 GB test file for bandwidth testing |
| [**ICMP Latency**](https://docs.coreweave.com/platform/regions/about-regions-and-azs.md#speedtest) | `ping.speedtest.us-east-13.coreweave.com` | ICMP latency test address |

## US-EAST-14A

This is a General Access zone located in New Jersey, USA. It is available to all customers.

Instances and AI Object Storage

| GPU Instances | CPU Instances | AI Object Storage |
| :- | :- | :- |
| [RTX PRO 6000 Blackwell Server Edition (High Memory)](https://docs.coreweave.com/platform/instances/gpu/rtxp6000-8x.md) | [General Purpose AMD Turin (High Memory)](https://docs.coreweave.com/platform/instances/cpu/turin-gp.md) [General Purpose Intel Emerald Rapids (High Memory)](https://docs.coreweave.com/platform/instances/cpu/cd-gp-i64-erapids.md) | Yes |
| Network information | | |

| Type | Address Range | Description |
| :- | :- | :- |
| **Public IP** | `166.19.116.0/22` | Public IP address range for this AZ |
| **NAT Egress** | `166.19.116.0/24`, `166.19.117.0/24` | Subset of the Public Range used for Service egress |
| **Node Range** | `10.213.128.0/18` | RFC 1918 private range used exclusively by this AZ |
| **Pods** | `10.0.0.0/13` | RFC 1918 space dedicated to all Pods |
| **Services** | `10.16.0.0/22` | Subset of Pod RFC 1918 space dedicated to Services |
| **Load Balancers** | `10.16.4.0/22` | Subset of Services RFC 1918 space dedicated to Load Balancers |
| [**Speedtest 1GB**](https://docs.coreweave.com/platform/regions/about-regions-and-azs.md#speedtest) | `http://http.speedtest.us-east-14.coreweave.com/1G` | 1 GB test file for bandwidth testing |
| [**Speedtest 10GB**](https://docs.coreweave.com/platform/regions/about-regions-and-azs.md#speedtest) | `http://http.speedtest.us-east-14.coreweave.com/10G` | 10 GB test file for bandwidth testing |
| [**ICMP Latency**](https://docs.coreweave.com/platform/regions/about-regions-and-azs.md#speedtest) | `ping.speedtest.us-east-14.coreweave.com` | ICMP latency test address |

## US-EAST-15A

This is a General Access zone located in Virginia, USA. It is available to all customers.

Instances and AI Object Storage

| GPU Instances | CPU Instances | AI Object Storage |
| :- | :- | :- |
| [B200 (InfiniBand)](https://docs.coreweave.com/platform/instances/gpu/b200-8x.md) [RTX PRO 6000 Blackwell Server Edition (Standard Memory)](https://docs.coreweave.com/platform/instances/gpu/rtxp6000-8x-v2.md) | [General Purpose AMD Turin (High Memory)](https://docs.coreweave.com/platform/instances/cpu/turin-gp.md) [General Purpose AMD Turin (High Storage)](https://docs.coreweave.com/platform/instances/cpu/turin-gp-l.md) [General Purpose Intel Emerald Rapids (High Memory)](https://docs.coreweave.com/platform/instances/cpu/cd-gp-i64-erapids.md) | Yes |
| Network information | | |

| Type | Address Range | Description |
| :- | :- | :- |
| **Public IP** | `166.19.160.0/22` | Public IP address range for this AZ |
| **Node Range** | `10.125.128.0/18` | RFC 1918 private range used exclusively by this AZ |
| **Pods** | `10.0.0.0/13` | RFC 1918 space dedicated to all Pods |
| **Services** | `10.16.0.0/22` | Subset of Pod RFC 1918 space dedicated to Services |
| **Load Balancers** | `10.16.4.0/22` | Subset of Services RFC 1918 space dedicated to Load Balancers |
| [**Speedtest 1GB**](https://docs.coreweave.com/platform/regions/about-regions-and-azs.md#speedtest) | `http://http.speedtest.us-east-15.coreweave.com/1G` | 1 GB test file for bandwidth testing |
| [**Speedtest 10GB**](https://docs.coreweave.com/platform/regions/about-regions-and-azs.md#speedtest) | `http://http.speedtest.us-east-15.coreweave.com/10G` | 10 GB test file for bandwidth testing |
| [**ICMP Latency**](https://docs.coreweave.com/platform/regions/about-regions-and-azs.md#speedtest) | `ping.speedtest.us-east-15.coreweave.com` | ICMP latency test address |

## US-EAST-17A

This is a General Access zone located in New Jersey, USA. It is available to all customers.

Instances and AI Object Storage

| GPU Instances | CPU Instances | AI Object Storage |
| :- | :- | :- |
| | [General Purpose AMD Turin (High Storage)](https://docs.coreweave.com/platform/instances/cpu/turin-gp-l.md) | Yes |
| Network information | | |

| Type | Address Range | Description |
| :- | :- | :- |
| **Public IP** | `166.19.136.0/22` | Public IP address range for this AZ |
| **NAT Egress** | `166.19.136.0/24`, `166.19.137.0/24` | Subset of the Public Range used for Service egress |
| **Node Range** | `10.59.128.0/17` | RFC 1918 private range used exclusively by this AZ |
| **Pods** | `10.0.0.0/13` | RFC 1918 space dedicated to all Pods |
| **Services** | `10.16.0.0/22` | Subset of Pod RFC 1918 space dedicated to Services |
| **Load Balancers** | `10.16.4.0/22` | Subset of Services RFC 1918 space dedicated to Load Balancers |
| [**Speedtest 1GB**](https://docs.coreweave.com/platform/regions/about-regions-and-azs.md#speedtest) | `http://http.speedtest.us-east-17.coreweave.com/1G` | 1 GB test file for bandwidth testing |
| [**Speedtest 10GB**](https://docs.coreweave.com/platform/regions/about-regions-and-azs.md#speedtest) | `http://http.speedtest.us-east-17.coreweave.com/10G` | 10 GB test file for bandwidth testing |
| [**ICMP Latency**](https://docs.coreweave.com/platform/regions/about-regions-and-azs.md#speedtest) | `ping.speedtest.us-east-17.coreweave.com` | ICMP latency test address |
