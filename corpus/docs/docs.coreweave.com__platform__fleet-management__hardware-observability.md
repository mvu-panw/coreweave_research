# Hardware observability

Source: https://docs.coreweave.com/platform/fleet-management/hardware-observability

# Hardware observability

> GPU chip telemetry, server-level IPMI metrics, and storage performance metrics available in CKS

CoreWeave Kubernetes Service (CKS) provides hardware transparency and observability with built-in telemetry. Hardware observability is available immediately on deployment and requires no setup or configuration. CKS includes the following hardware observability features:

* **Managed telemetry platform**: CoreWeave manages a high-performance platform for ingesting, storing, and exposing telemetry data.
* **Purpose-built dashboards**: CoreWeave provides curated dashboards that offer insights and draw on CoreWeave expertise in managing large GPU supercomputing fleets.
* **No additional cost**: All observability features are included for CKS customers at no additional charge.

## Hardware telemetry layers

The following sections describe the telemetry available across different layers of the hardware stack.

### GPU chip telemetry

CKS provides chip-level metrics through NVIDIA's Data Center GPU Management (DCGM) tool, which is pre-installed on all servers. You can query these metrics through the CoreWeave metrics query service or view them in the [Node Details dashboard](https://cks-grafana.coreweave.com/d/ddbdicm9sw7c5x/node-details).

These metrics help identify failures, performance issues, and power inefficiencies. Use them to optimize job performance and resource utilization. CoreWeave provides pre-configured alerts for critical thresholds.

### Server telemetry

CKS offers transparency at the physical server level, providing metrics and statuses for the entire server.

| Category | Details |
| - | - |
| **IPMI Metrics** | <ul><li>Electrical current</li><li>Power</li><li>Power consumption (server-wide)</li><li>Voltage</li><li>Temperature</li><li>Fan speed</li><li>Fan speed ratio</li><li>System Event Log (SEL) free space</li><li>System Event Log (SEL) log count</li></ul> |
| **IPMI Statuses** | <ul><li>Chassis power state</li><li>Electrical current sensor state</li><li>Fan speed sensor state</li><li>Power sensor state</li><li>Cable/interconnect VGA cable presence</li><li>Power supply status</li><li>Serial cable status</li><li>PCIe slot critical interrupt</li><li>Physical security intrusion</li><li>Fan redundancy state</li><li>CMOS battery state</li><li>Temperature sensor state</li><li>Voltage sensor state</li></ul> |
| **Node Problem and Lifecycle Conditions** | A set of conditions from kernel logs and temperature metrics that offer insight into node problems and lifecycle stages. Examples include `SlurmCordon`, `KernelDeadlock`, `InfiniBandLinkFault`, `GPUFallenOffBus`, and `DNSFailure`. |
| **Storage Performance Metrics** | <ul><li>Read Bandwidth</li><li>Write Bandwidth</li><li>Average Request Time by Operation</li><li>Queue Time by Operation and VIP</li><li>Timeouts by Operation</li><li>Average Response Time by Operation</li><li>Transmissions</li><li>Retransmissions</li><li>Mean Queue Time by Mount Address</li></ul> |
| **InfiniBand Interface Metrics** | <ul><li>`node_infiniband_port_data_received_bytes_total`</li><li>`node_infiniband_port_data_transmitted_bytes_total`</li><li>`node_infiniband_port_transmit_wait_total`</li><li>`node_infiniband_rate_bytes_per_second`</li></ul> |

### HPC Verification telemetry

CoreWeave's HPC Verification helps maintain high performance under sustained compute loads. HPC Verification raises alerts for failure conditions such as the following:

* `NodeVerificationFailure`
* `NodeVerificationFailureDCGMBadMemory`
* `NodeVerificationFailureGPUBlazeTLimit`
* `NodeVerificationFailureGPUBlazeThrottling`
* `NodeVerificationFailureGPUBurn`
* `NodeVerificationFailureGPUBurnTLimit`
* `NodeVerificationFailureMemBW`
* `NodeVerificationFailureNVFabric`
* `NodeVerificationFailureNVLink`
* `NodeVerificationFailureNonDeterminism`
* `NodeVerificationIncomplete`
* `NodeVerificationSRAMThresholdExceeded`

Log telemetry from all HPC Verification tests is also available to help you troubleshoot workload performance issues.

Together, these tools help you optimize applications, diagnose issues, and improve resource utilization on CKS.
