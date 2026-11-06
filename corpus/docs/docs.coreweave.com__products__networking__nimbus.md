# Nimbus

Source: https://docs.coreweave.com/products/networking/nimbus

# Nimbus

> Proprietary control and data-plane software for CoreWeave Kubernetes Service Nodes

This page explains what Nimbus is, how its components work together, and the role it plays in CoreWeave Kubernetes Service (CKS). Read it to understand how CoreWeave delivers tenant isolation, VPC networking, and Node lifecycle management without relying on virtual machines.

Nimbus is CoreWeave's control and data-plane software, integrated into the NVIDIA® BlueField® Data Processing Unit (DPU (A Data Processing Unit (DPU) is a 'computer-in-front-of-a-computer', fully isolated from the host's CPU, that provides network and other functions.)) that's affixed to each of our Nodes.

The DPU combines ARM-based CPU cores, specialized acceleration engines, and a network interface.
This combination creates an "infrastructure on a chip," acting as a "computer-in-front-of-a-computer."
The ARM processors operate in isolation from the host CPU, which provides an added layer of security and efficiency.

Nimbus operates behind the scenes to enable the resource requests you initiate.
For instance, when you request a Virtual Private Cloud (VPC (A Virtual Private Cloud (VPC) is a private network hosted within a public cloud infrastructure.)) Custom Resource within CKS (CoreWeave Kubernetes Service (CKS) is CoreWeave's managed Kubernetes service.), Nimbus creates the appropriate network policy directly on the DPU.

Nimbus enables our stateless Nodes to deliver features traditionally exclusive to virtualized environments.
Through its API-driven, extensible network programming capabilities, Nimbus coordinates tenant isolation, VPC setups, and public internet routing.
As a result, our Nodes offer scalability, flexibility, and isolation without the need for virtual machines.

## Understanding Nimbus

The following sections describe Nimbus's architecture and how its components coordinate to manage Nodes and DPUs.

Nimbus operates through a dual-component system: an Operator situated on the DPU, and a Controller within the CKS management cluster.
This pair oversees both the DPU and the Node's lifecycle.

Embedded directly on the DPUs, the Nimbus Operator is part of the Kubernetes ecosystem at CoreWeave, treated with the same level of importance and management as Kubernetes Nodes themselves.

The Controller's role extends to managing Node responses to fleet lifecycle events.
These include updates and checks such as firmware upgrades, adjustments in network configurations, changes in VPC memberships, and hardware integrity assessments.

Key to Nimbus's functionality is its ability to offload operations such as firewalling and encryption directly to the DPU.
This offloading keeps the host CPU free for computational tasks, which improves system efficiency.

Nimbus's architecture creates a secure, isolated network environment for each Node.
By managing VPC memberships and network interfaces, Nimbus enables Nodes to support multiple client VPCs simultaneously.
Network routing and isolation are handled through a Type 5 (A Type 5 EVPN deals exclusively with IP route advertisement.) (Layer 3) EVPN-VXLAN (Ethernet VPN-Virtual Extensible LAN (EVPN-VXLAN) combines EVPN's Control Plane with VXLAN's Data Plane.) overlay network, shifting network intelligence from traditional Top-of-Rack (TOR (A Top-of-Rack (TOR) network switch connects servers in a data center to the rest of the network.)) switches to the DPU.
In this setup, TOR switches are repurposed as mere packet-forwarding devices, using unnumbered BGP (Border Gateway Protocol (BGP) protocol makes the core routing decisions on the internet.) for the underlying network infrastructure.

## Nimbus's role in CKS

Nimbus is a critical component of CoreWeave Kubernetes Service (CKS (CoreWeave Kubernetes Service (CKS) is CoreWeave's managed Kubernetes service.)). During [Day 0](https://docs.coreweave.com/platform/fleet-management/node-lifecycle.md#day-0-initialization) and [Day 1](https://docs.coreweave.com/platform/fleet-management/node-lifecycle/day1.md) operations, Nimbus joins the Node to CoreWeave's internal onboarding cluster.

For [Day 2+](https://docs.coreweave.com/platform/fleet-management/node-lifecycle/day2.md) operations, other CKS components like the VPC Operator use Nimbus to maintain the desired state of the DPU and the Node's VPC membership.

Nimbus is responsible for confirming that the Node:

* Has the correct network configuration.
* Has joined the correct customer's cluster.
* Is a member of the correct VPCs.

Nimbus also verifies that the DPU runs the correct firmware and has the correct configuration to support the Node's workload.
