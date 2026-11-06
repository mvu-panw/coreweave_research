# CA-EAST

Source: https://docs.coreweave.com/platform/regions/ca-east

# CA-EAST

> Availability Zones in the CoreWeave CA-EAST super region, including locations in Ontario, Canada, and access tiers.

## CA-EAST-01A

This is a General Access zone located in Ontario, Canada. It is available to all customers.

Instances and AI Object Storage

| GPU Instances | CPU Instances | AI Object Storage |
| :- | :- | :- |
| [GB300 NVL72 Quantum-X InfiniBand](https://docs.coreweave.com/platform/instances/gpu/gb300-4x.md) [GB200 NVL72-powered instances](https://docs.coreweave.com/platform/instances/gpu/gb200-4x.md) | [General Purpose AMD Turin (High Memory)](https://docs.coreweave.com/platform/instances/cpu/turin-gp.md) [General Purpose Intel Emerald Rapids (High Memory)](https://docs.coreweave.com/platform/instances/cpu/cd-gp-i64-erapids.md) | Yes |
| Network information | | |

| Type | Address Range | Description |
| :- | :- | :- |
| **Public IP** | `166.19.72.0/22` | Public IP address range for this AZ |
| **NAT Egress** | `166.19.72.0/24`, `166.19.73.0/24` | Subset of the Public Range used for Service egress |
| **Node Range** | `10.219.128.0/18` | RFC 1918 private range used exclusively by this AZ |
| **Pods** | `10.0.0.0/13` | RFC 1918 space dedicated to all Pods |
| **Services** | `10.16.0.0/22` | Subset of Pod RFC 1918 space dedicated to Services |
| **Load Balancers** | `10.16.4.0/22` | Subset of Services RFC 1918 space dedicated to Load Balancers |
| [**Speedtest 1GB**](https://docs.coreweave.com/platform/regions/about-regions-and-azs.md#speedtest) | `http://http.speedtest.ca-east-01.coreweave.com/1G` | 1 GB test file for bandwidth testing |
| [**Speedtest 10GB**](https://docs.coreweave.com/platform/regions/about-regions-and-azs.md#speedtest) | `http://http.speedtest.ca-east-01.coreweave.com/10G` | 10 GB test file for bandwidth testing |
| [**ICMP Latency**](https://docs.coreweave.com/platform/regions/about-regions-and-azs.md#speedtest) | `ping.speedtest.ca-east-01.coreweave.com` | ICMP latency test address |
