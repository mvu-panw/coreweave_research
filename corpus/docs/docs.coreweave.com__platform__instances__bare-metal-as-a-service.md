# Bare Metal as a Service (BMaaS)

Source: https://docs.coreweave.com/platform/instances/bare-metal-as-a-service

# Bare Metal as a Service (BMaaS)

## BMaaS Definition

"Bare Metal as a Service (BMaaS)" means CoreWeave's provision to a customer of dedicated physical servers (each, a "Node") with direct hardware access and no CoreWeave virtualization layer, together with the physical infrastructure and network on which those Nodes operate. Under BMaaS, CoreWeave: (a) provides and operates the data center facilities, including physical security, liquid cooling, power and racks; (b) provides and operates all frontend, backend and management networking, including provisioning, monitoring and break/fix; (c) performs hardware lifecycle management, including firmware management, BIOS, burn-in testing, RMA triage and replacement, and storage media sanitization; (d) administers the BlueField data processing unit ("DPU") and enforces VPC isolation through it; and (e) performs out-of-band monitoring and forwards telemetry to customer-designated endpoints.
Customer retains sole responsibility for each Node from the host operating system upward, including the node boot image and bootloader; host OS security, patching and configuration hardening; drivers and containers; cluster orchestration, scheduling and workload management; node health monitoring, GPU fault detection and continuous active testing; encryption of customer data in transit and at rest; and application security and use of the BMC console via the Serial over LAN ("SOL") API. Note that use of the SOL API does not provide direct access to the Node's BMC device, it provides a console to the Node, not to the BMC itself. Supply chain governance for third-party agents is a shared responsibility of CoreWeave and the customer.
BMaaS does not include CoreWeave visibility into customer workloads, any CoreWeave in-band agent on the host, or the automated health detection and remediation provided under CoreWeave Kubernetes Service ("CKS").
