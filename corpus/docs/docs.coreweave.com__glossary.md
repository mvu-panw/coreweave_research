# Glossary

Source: https://docs.coreweave.com/glossary

# Glossary

> A glossary of terms and definitions used across the CoreWeave platform and documentation

Use this page as a reference for terminology that appears throughout CoreWeave's products and documentation, with entries listed alphabetically.

## Algorithm

A set of rules or instructions to solve a problem or perform a computation.

## Attribute-Based Access Control (ABAC)

A policy-based access control model where access is determined by evaluating attributes (for example, user, resource, environment).

## Audit logging

Tracking and recording system events and user activities for security analysis and compliance.

## Automation

The use of technology to perform tasks with minimal human intervention.

## Availability Zone (AZ)

An AZ is a partition within a Region that hosts one or more data halls.
AZs are physically and operationally independent from each other to prevent failures from propagating across them.
For example, in the `US-EAST-05` Region, Availability Zone `a` is named `US-EAST-05a`.

See also: [Geo](#geo), [Region](#region)

## Border Gateway Protocol (BGP)

A standardized exterior gateway protocol that exchanges routing information between different autonomous systems on the internet.
BGP is the protocol used to make core routing decisions on the internet.

## Classless Inter-Domain Routing (CIDR)

CIDR is a method for allocating IP addresses and routing IP packets. See also: [CIDR notation](https://en.wikipedia.org/wiki/Classless_Inter-Domain_Routing#CIDR_notation).

## cloud-init

An industry standard method for cloud instance initialization.
CoreWeave uses cloud-init to pass configuration data to Nodes at boot time.

## Cloud Access Security Broker (CASB)

A security tool that provides visibility and control over data and threats in cloud services.

## Cloud compliance

Ensuring that cloud systems adhere to regulatory standards like SOC 2, HIPAA, ISO 27001, or FedRAMP.

## Cloud-Native Application Protection Platform (CNAPP)

Unified security architecture that integrates CWPP, CSPM, and CI/CD pipeline protection.

## Cloud security

Practices and technologies designed to protect cloud-based infrastructure, data, and applications from threats and unauthorized access.

## Cloud Security Posture Management (CSPM)

Tools that continuously monitor cloud configurations to identify security risks and misconfigurations.

## Cloud Service Provider (CSP)

A company that offers cloud computing services, such as AWS, Azure, and Google Cloud.

## Cloud Workload Protection Platform (CWPP)

A security solution that protects workloads across cloud and on-premises environments.

## Cluster

A group of interconnected computers working together as a single system.

## Cognitive computing

Computer systems that simulate human thought processes.

## Confidential computing

Protecting data in use by performing computations in hardware-based Trusted Execution Environments (TEEs).

## Control Plane

The Control Plane is a collection of resources that manages the state of the cluster as a whole. Its job is to regulate the cluster, making sure it's responsive, it efficiently manages containerized applications, and it's stable.

## Cordon

A cordoned Node is one the scheduler doesn't place new work on, while existing Pods keep running. CoreWeave cordons a Node when its Node lifecycle automation detects a problem, so that new workloads avoid unhealthy hardware while CoreWeave investigates or replaces it. You can also cordon a Node yourself for maintenance. When CoreWeave cordons a Node, it records a customer-visible reason in the `node.coreweave.cloud/cordonReason` annotation; a Node you cordon yourself with `kubectl cordon` carries no CoreWeave cordon reason.

See also: [Node condition](#node-condition), [Node lifecycle automation](#node-lifecycle-automation), [Node cordoning](https://docs.coreweave.com/products/cks/nodes/cordon.md)

## CoreWeave Cloud Console

The interface for managing CoreWeave resources, hosted at [console.coreweave.com](https://console.coreweave.com).

## CoreWeave Kubernetes Service (CKS)

[CoreWeave Kubernetes Service (CKS)](https://docs.coreweave.com/products/cks.md) is a managed Kubernetes service that provides a secure, scalable, and reliable platform for deploying containerized applications. CKS is built on CoreWeave's proprietary infrastructure and is designed to deliver high-performance computing resources to customers.

## CoreWeave Node lifecycle controller

The CoreWeave Node lifecycle controller coordinates Node lifecycle state transitions, including reboots and moves to triage. It is part of CoreWeave's [Node lifecycle automation](#node-lifecycle-automation). The CoreWeave Node lifecycle controller is separate from the SUNK Node Controller, which synchronizes data between Kubernetes Nodes and `slurmd` Pods.

See also: [Node state transitions in CKS](https://docs.coreweave.com/platform/fleet-management/node-lifecycle/state-transitions.md), [Reboot Nodes](https://docs.coreweave.com/products/cks/nodes/reboot.md), [SUNK Node Controller](https://docs.coreweave.com/products/sunk/discover_sunk/node-controller.md)

## CPU

A Central Processing Unit (CPU) is the hardware within a computer that carries out the instructions of a computer program by performing basic arithmetic, logical, control, and input/output operations specified by the instructions.

## Custom Resource (CR)

A Custom Resource is an instance of a CRD (Custom Resource Definitions (CRDs) extend the Kubernetes API with user-definable resources and controllers.). It's the actual object created with the Kubernetes API.

See also: [Custom Resources](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/)

## Custom Resource Definition (CRD)

CRDs are an extension of the Kubernetes API that lets you define custom resources and controllers.
CRDs enable you to extend the functionality of Kubernetes by defining new resources and controllers that are not part of the core Kubernetes API.

A CRD is the blueprint for a type of CR (A Custom Resource (CR) is the deployed instance of an object defined by a CRD.).

See also: [Custom Resources](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/)

## Data Loss Prevention (DLP)

A strategy to prevent unauthorized sharing or leakage of sensitive data.

## Data Plane

The part of Kubernetes that deals with application and data traffic.

## Data Processing Unit (DPU)

A programmable infrastructure-on-a-chip that combines an array of ARM-based CPU cores, acceleration engines, and a high-performance network interface.
DPUs function as a "computer-in-front-of-a-computer" and are fully isolated from the host's CPU.
DPUs provide network, storage, and encryption functions on Direct Metal Nodes, enabling CoreWeave to deliver scalable, flexible, and secure cloud services.

See [What Is a DPU? at NVIDIA's Blog](https://blogs.nvidia.com/blog/whats-a-dpu-data-processing-unit/).

## Day 0

The phase in the lifecycle of a CoreWeave Node where it is initially configured after powering on.

## Day 1

The phase in the lifecycle of a CoreWeave Node where it is intensively validated before delivery to a customer.

## Day 2+

The phase in the lifecycle of a CoreWeave Node once it has been delivered to a customer, and is continuously monitored and validated by CoreWeave.

## DevSecOps

An approach that integrates security practices directly into DevOps workflows.

## Dynamic Host Configuration Protocol (DHCP)

A network protocol that automatically assigns IP addresses and other network configuration settings to devices on a network.

## Encryption at rest

Protecting stored data using encryption mechanisms.

## Encryption in transit

Securing data as it travels across networks using protocols like TLS.

## Ethernet Virtual Private Network (EVPN)

EVPN simplifies Control Planes for various Virtual Private Network (VPN) services by extending Ethernet (Layer 2) services over a broader network, typically an IP/MPLS network.
EVPN supports multi-tenancy, allowing different customers' networks to share the same physical infrastructure while keeping their traffic separate and secure.
EVPN is widely used in interconnect scenarios, and for integrating distributed regional and campus networks.
EVPN brings the advantages of traffic balancing and flexible deployment from IP VPNs into the Ethernet domain.

## EVPN Type 5

A Type 5 EVPN (An Ethernet Virtual Private Network (EVPN) interconnects Layer 2 networks and carries Layer 3 VPN services.) deals exclusively with IP route advertisement, differentiating it from other types (such as Type 2) that include MAC (A Medium Access Control (MAC) address is a unique identifier assigned to a Network Interface Controller (NIC).) address advertisement.

## EVPN-VXLAN integration

Ethernet VPN-Virtual Extensible LAN (EVPN-VXLAN) combines EVPN (An Ethernet Virtual Private Network (EVPN) interconnects Layer 2 networks and carries Layer 3 VPN services.)'s Control Plane with VXLAN (A Virtual Extensible LAN (VXLAN) addresses the limitations of traditional VLANs in large-scale environments, such as data centers.)'s Data Plane.
Combined, these technologies create virtual Layer 2 networks that span Layer 3 boundaries in large-scale environments.
This integration allows seamless communication between devices, regardless of their physical location or the underlying network infrastructure, while maintaining efficient traffic handling and scalability.

## Fabric (backend network)

A fabric is a distinct high-performance backend network, such as an InfiniBand or RoCE fabric, that connects Nodes for low-latency, high-throughput communication. CoreWeave labels each Node with the fabric it belongs to, so you can keep the Nodes of a single distributed job within one fabric. The fabric label is one of several topology labels CoreWeave exposes for placement.

See also: [Superpod](#superpod), [Leafgroup](#leafgroup), [InfiniBand and RoCE labels](https://docs.coreweave.com/products/networking/hpc-interconnect/infiniband-roce-labels.md)

## Federated identity

An authentication method allowing users to log in across multiple systems using a single identity (through OIDC and SAML).

## Geo

A Geo covers multiple Regions (A region encompasses a broader geographic area, expanding service availability and meeting data residency requirements.), facilitating global service distribution and disaster recovery.
At CoreWeave, the term Geo defines an entire continent, ensuring coverage and reliability for global operations.
For example, all Regions in the United States are in the `US` Geo.

See also: [Region](#region), [Availability Zone (AZ)](#availability-zone-az)

## GPU

A Graphics Processing Unit (GPU) is a parallel processor that is designed to accelerate vector and matrix operations. GPUs are commonly used in high-performance computing and machine learning applications.

## GPUDirect RDMA

GPUDirect RDMA is a technology that enables remote direct memory access (RDMA (Remote Direct Memory Access (RDMA) allows data to be transferred directly between the memory of two computers without involving the operating system.)) transfers between GPUs and other devices without involving the operating system or CPU.

See also: [Remote Direct Memory Access (RDMA)](#remote-direct-memory-access-rdma)

## Hard Disk Drive (HDD)

A hard disk drive (HDD) is a non-volatile data storage device. An HDD includes two main elements: a spinning circular magnetic platter and an actuator arm that moves across the platter to read and write data. HDDs are slower than NVMe (Non-Volatile Memory Express (NVMe) is a storage protocol that provides high-performance access to non-volatile memory devices, such as solid-state drives (SSDs).) drives, but are typically less expensive and have higher storage capacities.

## Helm-installed component

A Helm-installed component is software you install into your own cluster, often from a CoreWeave-provided Helm chart, and that you own and operate. CoreWeave provides the chart and documents the safe configuration, but the running release is yours to manage. This is distinct from a managed component, which CoreWeave installs and reconciles. When deciding who fixes a broken component, a Helm-installed component is your responsibility, while a managed component is CoreWeave's.

See also: [Managed component](#managed-component), [What CoreWeave manages](https://docs.coreweave.com/support/what-coreweave-manages.md)

## HPC Verification

HPC Verification is CoreWeave's proactive, on-Node testing framework. At the top of each hour, if a Node is idle, meaning no customer Pod holds any of its GPUs, CoreWeave runs a 20- to 30-minute test that uses all of the Node's GPUs to catch problems that passive monitoring can't detect, such as silent data corruption, performance regressions, and thermal deficiencies. The test Pods run at a low priority and stop as soon as Kubernetes or Slurm schedules a workload that needs the Node's GPUs. The tests aren't billable and can't be disabled. HPC Verification is separate from Node Health Check (NHC): HPC Verification is a fleet-wide CoreWeave test that runs on idle Nodes, while NHC is a tool that SUNK runs on a node after a Slurm job. On SUNK clusters, a passing HPC Verification test is what returns a node whose drain reason carries `sunk:verify-undrain` to service.

See also: [Node Health Check (NHC)](#node-health-check-nhc), [Day 2+](#day-2), [HPC Verification](https://docs.coreweave.com/platform/fleet-management/hpc-verification.md)

## Identity and Access Management (IAM)

A framework for managing user identities and access permissions across cloud services.

## Identity provider (IdP)

An identity provider (IdP) is an entity that stores and serves user authentication information as an authentication service for users. IdPs can then be used to validate user identity to other services, such as cloud applications.

## iPXE (i Preboot eXecution Environment)

The **i Preboot eXecution Environment** is the leading open source network boot firmware.
It provides a full PXE (Preboot eXecution Environment (PXE) is a standardized client-server environment that boots a software assembly retrieved from a network.) implementation enhanced with additional features and flexibility for network booting.
iPXE is commonly used in cloud environments with complex configurations and network installations to boot servers over the network.
[From the official FAQ](https://ipxe.org/faq):

> Q: What does the "i" in "iPXE" stand for?\
>
> A: It doesn't.

## InfiniBand

A high-performance network architecture that provides high throughput and low latency, commonly used in high-performance computing environments.

## Internode Memory Exchange (IMEX)

Internode Memory Exchange (IMEX) is NVIDIA's software for coordinating GPU memory import and export across OS instances in an NVLink multi-Node deployment. On [CoreWeave Kubernetes Service (CKS)](https://docs.coreweave.com/products/cks.md), customer workloads access IMEX channels through Dynamic Resource Allocation. See [IMEX overview](https://docs.coreweave.com/products/cks/clusters/scheduling/imex-overview.md).

## Infrastructure as Code (IaC) Security

Securing declarative infrastructure templates (such as Terraform and CloudFormation) from misconfigurations or vulnerabilities.

## Input/output operations per second (IOPS)

IOPS (pronounced *eye-ops*) is an input/output performance measurement used to characterize computer storage devices.

## Ingress/egress filtering

Controlling the flow of traffic into (ingress) and out of (egress) cloud environments.

## Internet Protocol version 4 (IPv4)

IPv4 is the fourth version of the Internet Protocol (IP), and one of the core protocols of standards-based internetworking methods in the internet and other packet-switched networks. IPv4 is the most widely used version of the Internet Protocol.

## Internet Protocol version 6 (IPv6)

IPv6 is the most recent version of the Internet Protocol (IP), the communications protocol that provides an identification and location system for computers on networks and routes traffic across the internet.

## Key Management System (KMS)

A service that manages cryptographic keys used for data encryption and digital signatures.

## Kubeconfig

A configuration file containing details like cluster API server addresses, contexts, and user credentials used by `kubectl` and other Kubernetes tools to authenticate and manage access to Kubernetes clusters. Kubeconfig files let you switch between different clusters and manage multiple environments securely.

## Least privilege

A security principle where users or systems are given only the minimum access required to perform their tasks.

## Leafgroup

A leafgroup is a group of leaf switches in a backend network topology that serves a common set of Nodes. CoreWeave labels each Node with its leafgroup, so you can keep tightly coupled workloads within one leafgroup to reduce network hops. A leafgroup sits below a superpod in the topology hierarchy.

See also: [Fabric (backend network)](#fabric-backend-network), [Superpod](#superpod), [InfiniBand and RoCE labels](https://docs.coreweave.com/products/networking/hpc-interconnect/infiniband-roce-labels.md)

## LOTA

CoreWeave's [Local Object Transport Accelerator (LOTA)](https://docs.coreweave.com/products/storage/object-storage/improving-performance/about-lota.md) is a container that lives on every GPU and CPU Node inside a client's cluster, performing intelligent acceleration. Conventional transfer accelerators speed up the data transfer rates of bucket contents over long distances.

LOTA uses NVMe SSDs in each Node to create a cluster-wide cache, increasing throughput and reducing latency.

## MACsec

MACsec (Media Access Control Security) is an IEEE standard for securing Ethernet networks at the link layer. MACsec provides secure communication between network devices by encrypting and authenticating Ethernet frames. MACsec is commonly used to protect data in transit and prevent unauthorized access to network traffic. See also: [IEEE 802.1AE](https://en.wikipedia.org/wiki/IEEE_802.1AE)

## Managed component

A managed component is software that CoreWeave installs into your cluster and keeps reconciled to its intended state. You shouldn't modify a managed component directly, because CoreWeave automation reverts changes to it. If a managed component misbehaves, that is a CoreWeave responsibility and a valid reason to open a support ticket. This is distinct from a Helm-installed component, which you install and own.

See also: [Helm-installed component](#helm-installed-component), [What CoreWeave manages](https://docs.coreweave.com/support/what-coreweave-manages.md)

## Medium Access Control (MAC) address

A MAC address is a unique identifier assigned to a Network Interface Controller (NIC (A Network Interface Controller (NIC) is a hardware component that connects a computer to a network.)) for use as a network address within a network segment.

## Microsegmentation

Dividing networks into smaller zones to enforce granular security controls.

## Multi-Factor Authentication (MFA)

A security mechanism requiring multiple forms of verification to access systems, for example, a password and mobile code.

## Multipart upload

Multipart uploads (or "MPUs") refer to uploading large objects as multiple pieces. See also: [Uploading and copying objects using multipart upload](https://docs.aws.amazon.com/AmazonS3/latest/userguide/mpuoverview.html) (Amazon)

## Mutual TLS (mTLS)

An extension of TLS where both client and server authenticate each other using certificates.

## Natural Language Processing (NLP)

The ability of computers to understand, interpret, and generate human language.

## Network Access Control Lists (NACLs)

Stateless filters that control traffic at the subnet level in a cloud network.

## Network Interface Controller (NIC)

A network interface controller (NIC) is a hardware component that connects a computer to a network.
NICs are commonly used to connect computers to Ethernet networks, wireless networks, and other types of networks.

## Node

An individual computer within a cluster.

## Node condition

A Node condition is a status signal that describes some aspect of a Node's health or readiness. Kubernetes reports standard conditions, and CoreWeave surfaces a subset of customer-visible conditions that explain why a Node is healthy, cordoned, or being serviced. When a Node is cordoned, its condition and reason show you whether the cause is a hardware fault CoreWeave is handling or an action you can take. The Node conditions that CoreWeave sets drive its own Node lifecycle automation: don't rely on them for your own automation or management, and change them only through documented procedures, such as [cordoning a Node yourself](https://docs.coreweave.com/products/cks/nodes/cordon.md#cordon-a-node-yourself) or [requesting a Node reboot](https://docs.coreweave.com/products/cks/nodes/reboot.md#request-a-node-reboot). You can add your own custom Node conditions.

See also: [Cordon](#cordon), [Node lifecycle automation](#node-lifecycle-automation), [Node cordoning](https://docs.coreweave.com/products/cks/nodes/cordon.md)

## Node Health Check (NHC)

SUNK runs [Node Health Check (NHC)](https://github.com/mej/nhc) as one of the scripts in the Epilog chain after a job, and only when no other job is still running on the node. A failed check drains the node with a reason that begins with `NHC:`.

The text after `NHC:` names the failed check. Most NHC drains carry `sunk:verify-undrain`, so they clear on their own once the node passes the next HPC Verification test. NHC is separate from HPC Verification: NHC is a tool that SUNK runs on a node in the Epilog after a job, while HPC Verification is CoreWeave's hourly test of idle Nodes across the fleet.

See also: [HPC Verification](#hpc-verification), [Node Health Check (NHC) drains](https://docs.coreweave.com/products/sunk/manage_sunk/drain-and-undrain-nodes.md#node-health-check-nhc-drains)

## Node label

A Node label is a key-value pair attached to a Node that describes its hardware, location, or network topology. CoreWeave applies labels automatically, including topology labels for the backend network fabric, superpod, leafgroup, and rack, and labels that identify the instance type and capabilities. You use Node labels in node selectors and affinity rules to control where Pods are scheduled. CoreWeave-applied labels are the supported vocabulary for placement.

See also: [Fabric (backend network)](#fabric-backend-network), [Superpod](#superpod), [Leafgroup](#leafgroup), [InfiniBand and RoCE labels](https://docs.coreweave.com/products/networking/hpc-interconnect/infiniband-roce-labels.md)

## Node lifecycle automation

Node lifecycle automation is the CoreWeave system that manages each Node from Day 0 initialization through Day 2+ production operations. In a CKS cluster, when a Node condition fires, it cordons the Node and, depending on the condition, keeps it cordoned until the condition clears, reboots it, or moves it to triage for investigation. It re-validates a failed Node before the Node returns to production, and replaces Nodes that leave your cluster to keep it at full capacity. Node lifecycle automation is distinct from SUNK's Node Controller, which synchronizes data between Kubernetes Nodes and `slurmd` Pods.

See also: [Cordon](#cordon), [Node condition](#node-condition), [Node lifecycle](https://docs.coreweave.com/platform/fleet-management/node-lifecycle.md), [Node state transitions in CKS](https://docs.coreweave.com/platform/fleet-management/node-lifecycle/state-transitions.md), [Node Controller](https://docs.coreweave.com/products/sunk/discover_sunk/node-controller.md)

## Node Pool

A Node Pool is a logical grouping of Nodes in a CKS cluster with the same Instance Type, Labels, Taints, and Annotations.
Node Pools are useful for managing a group of Nodes as a single entity or assigning workloads to specific Nodes based on their configuration.

## Non-Volatile Memory Express (NVMe)

NVMe is a storage protocol that provides high-performance access to non-volatile memory devices. NVMe is designed to take advantage of the low latency and high throughput of modern storage devices, providing improved performance over traditional storage protocols.

## OpenID Connect (OIDC)

[OpenID Connect (OIDC)](https://openid.net/developers/how-connect-works/) is an identity layer laid atop the OAuth 2.0 protocol, which allows users to authenticate themselves by way of verifying their identity through an identity provider (IdP), such as Okta. CoreWeave supports OIDC as an authentication method to CKS clusters.

## Open vSwitch (OVS)

[Open vSwitch (OVS)](https://en.wikipedia.org/wiki/Open_vSwitch) is a production-quality, multilayer virtual switch licensed under the open source Apache 2.0 license.

## Parallel processing

Simultaneous execution of tasks across multiple processors or cores.

## PCI Express (PCIe)

Peripheral Component Interconnect Express, officially abbreviated as PCIe, is a high-speed serial computer expansion bus standard.

## Penetration testing

Simulated cyberattacks used to evaluate the security of cloud environments.

## Persistent Volume Management Operator (PVMO)

A Kubernetes controller manager that periodically runs to clean up any orphaned storage volumes.

See also: [Persistent Volume Management Operator (PVMO)](https://docs.coreweave.com/products/storage/distributed-file-storage/about-pvmo.md)

## Point of Presence (POP)

A Point of Presence (POP) is a location where two or more networks interconnect.

## Policy as code

The practice of defining and enforcing security and compliance rules using machine-readable code, for instance, using Open Policy Agent.

## Preboot eXecution Environment (PXE)

The [PXE](https://en.wikipedia.org/wiki/Preboot_Execution_Environment) specification describes a standardized client-server environment that boots a software assembly, retrieved from a network, on PXE-enabled clients.
On the client side it requires only a PXE-capable network interface controller (NIC (A Network Interface Controller (NIC) is a hardware component that connects a computer to a network.)), and uses a small set of industry-standard network protocols such as DHCP (Dynamic Host Configuration Protocol (DHCP) is a protocol that automatically assigns network configuration settings to devices.) and TFTP (Trivial File Transfer Protocol (TFTP) is a lightweight file transfer protocol that does not provide authentication or encryption.).
PXE is most often pronounced as "pixie", and the process is often called "pixie boot".

See also: [iPXE](#ipxe-i-preboot-execution-environment)

## RDMA over Converged Ethernet (RoCE)

A network protocol that allows RDMA (Remote Direct Memory Access (RDMA) allows data to be transferred directly between the memory of two computers without involving the operating system.) over an Ethernet network.

See also: [Remote Direct Memory Access (RDMA)](#remote-direct-memory-access-rdma)

## Region

An area within a Geo that contains multiple Availability Zones (AZs). Regions provide redundancy and failover capabilities by allowing workloads to be distributed across multiple AZs. Regions are strategically placed to offer low latency, high-performance connectivity, and meet data residency requirements. For example, in `US-EAST-05`, the Geo is `US` and the Region is `EAST-05`.

See also: [Geo](#geo), [Availability Zone (AZ)](#availability-zone-az)

## Remote Direct Memory Access (RDMA)

RDMA allows data to be transferred directly between the memory of two computers without involving the operating system or CPU.
RDMA provides low latency and high throughput data transfers, making it ideal for high-performance computing environments.

See also: [GPUDirect RDMA](#gpudirect-rdma), [RDMA over Converged Ethernet (RoCE)](#rdma-over-converged-ethernet-roce)

## Role-Based Access Control (RBAC)

An authorization method where users are granted permissions based on their role within an organization.

## Runtime security

Monitoring and securing workloads during execution, for example, using tools like Falco or Tetragon.

## Security groups

Virtual firewalls used to control inbound and outbound traffic to resources in the cloud.

## Security Token Service (STS)

A service that issues temporary, limited-privilege credentials to users or services.

## Secrets management

Storing and retrieving sensitive information (such as passwords and API keys) securely in a cloud-native vault.

## Service mesh

A network layer (such as Istio or Linkerd) that handles secure service-to-service communication with observability and policy enforcement.

## Shared responsibility model

A framework outlining security responsibilities split between the cloud provider and the customer.

## SIEM (Security Information and Event Management)

Tools that aggregate and analyze log data for real-time threat detection.

## Single-root input/output virtualization (SR-IOV)

SR-IOV is a specification that allows a single physical PCIe (Peripheral Component Interconnect Express (PCIe) is a high-speed serial computer expansion bus standard.) device to appear as multiple separate physical devices.
SR-IOV allows a single physical device to be shared by multiple virtual machines, providing improved performance and reduced latency.

Learn more at Wikipedia: [Single-root input/output virtualization](https://en.wikipedia.org/wiki/Single-root_input/output_virtualization)

## Slurm

A popular job scheduling system typically deployed on HPC clusters.

## Storage

A system for saving and retrieving data.

See also: [Object Storage](https://docs.coreweave.com/products/storage/object-storage/about.md), [Distributed File Storage](https://docs.coreweave.com/products/storage/distributed-file-storage/about.md), [Local Storage](https://docs.coreweave.com/products/storage/local-storage.md)

## Supercomputer

A computer with a high level of performance compared to a general-purpose computer.

## Superpod

A superpod is a high-level grouping within a backend fabric that contains multiple leafgroups. CoreWeave labels each Node with its superpod, so you can keep a large distributed job within a single superpod to limit the network distance between its Nodes.

See also: [Fabric (backend network)](#fabric-backend-network), [Leafgroup](#leafgroup), [InfiniBand and RoCE labels](https://docs.coreweave.com/products/networking/hpc-interconnect/infiniband-roce-labels.md)

## Supply chain security

Protecting cloud software pipelines from tampering, including the use of signed artifacts and SBOMs.

## Throughput

The amount of work completed in a given time period.

## Top of Rack (TOR)

A network switch that connects servers in an [Availability Zone](#availability-zone-az) to the rest of the network.
TOR switches are typically located at the top of a rack of servers and provide network connectivity to the servers within the rack.

## Trivial File Transfer Protocol (TFTP)

TFTP is a lightweight file transfer protocol that does not provide authentication or encryption.
TFTP is commonly used for network booting and firmware updates.

## Virtual Extensible LAN (VXLAN)

VXLAN addresses the limitations of traditional Virtual Local Area Networks (VLANs (A Virtual Local Area Network (VLAN) is a broadcast domain that is partitioned and isolated in a computer network at the data link layer (OSI layer 2).)) in large-scale environments.
VXLAN encapsulates Ethernet frames within User Datagram Protocol (UDP) packets, enabling them to traverse across IP networks.
By extending Layer 2 networks over Layer 3 infrastructure, VXLAN allows for greater flexibility and scalability in large-scale, multi-tenant environments.

## Virtual Local Area Network (VLAN)

A Virtual Local Area Network (VLAN) is a broadcast domain that is partitioned and isolated in a computer network at the data link layer ([OSI layer 2](https://en.wikipedia.org/wiki/Data_link_layer)).

## Virtual Private Cloud (VPC)

A VPC is a private network hosted within a public cloud infrastructure.
A VPC provides a secure environment where resources can be isolated from the public internet and other VPCs.
VPCs are commonly used to create virtual networks with specific IP address ranges, subnets, and security groups.

## Virtual Routing and Forwarding (VRF)

VRF allows multiple instances of a routing table to coexist within the same router at the same time.
Each VRF instance maintains its own routing table, which is separate from the global routing table.

## Workload identity

Associating workloads (like containers and VMs) with verifiable identities for secure communication and policy enforcement.

## Zero trust architecture

A security model where no user or device is trusted by default, even if it's inside the network perimeter.
