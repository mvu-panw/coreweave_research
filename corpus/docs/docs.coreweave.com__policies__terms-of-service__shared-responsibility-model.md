# Shared Responsibility Model

Source: https://docs.coreweave.com/policies/terms-of-service/shared-responsibility-model

# Shared Responsibility Model

> How CoreWeave and its clients platform use responsibilities

## What is a Shared Responsibility Model?

A Shared Responsibility Model is a tool to help communicate the distinction between the responsibilities held by CoreWeave and the responsibilities held by our clients when using the CoreWeave Cloud platform. The table below illustrates the basic aspects of CoreWeave Cloud for which the client is ultimately responsible, as well as those for which CoreWeave itself is ultimately responsible. You can read more about each listed aspect under the table.

**Security and compliance** on CoreWeave operates as a **shared responsibility** between CoreWeave and our customers. This shared model relieves the operational burden of customers while CoreWeave operates, manages, and controls the infrastructure components that support our services.

The Shared Responsibility Model below delineates the responsibilities that CoreWeave customers ("Client") maintain, versus those that CoreWeave itself maintains.

### Terms

* **Client:** A CoreWeave Cloud customer
* **End user:** A user connecting to the Client's services; the Client's customers

## The CoreWeave Shared Responsibility Model

| Client responsibilities | CoreWeave responsibilities |
| - | - |
| **1. Customer Layer** Customer Data Access Collection, Protection and Use; Legal, Acceptable Use, Privacy Policy Requirements | **1. Platform Layer** Kubernetes Container Orchestration; API Services; Identity and Access Management Platform; Cloud Console; Virtual Private Cloud |
| **2. Application Layer** Application Performance; Reliability; Security and Management; Application Code | **2. Compute Layer** Operating System; Container Support; Hardware Drivers; Health Checking and Node Lifecycle; Endpoint Detection and Response |
| **3. Access Layer** Identity and Access Management Policy Definitions; Third-Party Identity Providers Network Policies | **3. Network Layer** Internal and External Connectivity; Network Encapsulation; VPC Isolation; Direct Connect |
| **4. Data Layer** Data Classification; Data Protection; Encryption; Disaster Recovery Plans; Backups | **4. Physical Layer** Data Center Security; Power and Cooling; IT Inventory and Asset Management; Physical |

## Client responsibilities

Any aspects of using CoreWeave Cloud that are within the Client's absolute control are the responsibility of the Client.

The following are elements that fall under the Client's responsibility.

* **Client software and applications and client-side data:** the software and applications Clients choose to run within their containers, as well as all client-side data, is the sole responsibility of the Client
* **Any guest Operating System used on Virtual Servers:** Clients are responsible for guest Operating Systems and network configurations, including firewall configurations

The following are all **Client responsibilities** described in depth.

### Customer layer

| Responsibility | Description |
| - | - |
| **Customer Data Access Collection, Protection and Use** | The method by which end users normally access hosted data is the Client's responsibility. The methods by which any data is collected from or about end users is the Client's responsibility. |
| **Legal, Acceptable Use, Privacy Policy Requirements** | It is the Client's responsibility to adhere to all legal, acceptable use, and requirements as stipulated in [the CoreWeave Privacy Policy](https://docs.coreweave.com/policies/terms-of-service/privacy-policy.md) and [Terms of Service](https://docs.coreweave.com/policies/terms-of-service.md). |

### Application layer

| Responsibility | Description |
| - | - |
| **Application Performance** | The performance of applications deployed by the Client are the responsibility of the Client with regard to performance of the underlying application code. |
| **Reliability** | Reliability of applications deployed by the Client are the responsibility of the Client for any type of service level reliability they must meet. |
| **Security and Management** | Clients are responsible for the security of their applications, including configuration and application security for all applications deployed by the Client onto CoreWeave Products. |
| **Application Code** | The performance, reliability, security, and management of the Client's application is the Client's responsibility. |

### Access layer

| Responsibility | Description |
| - | - |
| **Identity and Access Management Policy Definitions** | All identity-based access management (IAM) configurations are the Client's responsibility that serve authentication and authorization for CoreWeave Cloud services. |
| **Third Party Identity Providers** | Secure configuration and management of third-party identity providers (IdP's) are the Client's responsibility to maintain for SAML/SSO or OIDC based connections |
| **Network Policies** | Secure configuration of the Client's network policies in CKS clusters are the Client's responsibility within CoreWeave Cloud products such as utilizing Kubernetes resources such as Kubernetes Network Policies. |

### Data layer

| Responsibility | Description |
| - | - |
| **Data Classification** | It is the responsibility of the Client to properly classify data used within CoreWeave Cloud products and data collected from or about end users. |
| **Data Protection** | It is the responsibility of the Client to ensure that classified data is adequately secured. |
| **Encryption** | It is the responsibility of the Client to ensure that any data determined to require encryption at rest or in transit utilizes the required protocols for securing data. |
| **Disaster Recovery Plans** | It is the responsibility of the Client to construct any disaster recovery plans for use of CoreWeave Products. |
| **Backups** | It is the responsibility of the Client to construct any backup systems for data recovery purposes. |
| **Metadata** | It is the responsibility of the Client to ensure that confidential information is not stored in metadata fields. |
| **Resource Identifiers** | It is the responsibility of the Client to ensure that confidential information is not stored in resource identifiers. |

## CoreWeave responsibilities

CoreWeave's responsibilities **begin at the physical level** spanning across data centers in the United States and European regions that contain CoreWeave assets.

It is our responsibility to ensure that our physical data centers are always secure, and that power is always on and flowing to where it is needed with redundant mechanisms in place.

**Storage, compute, network infrastructure, and software services** are the responsibilities of CoreWeave. Our high-performance NVIDIA GPUs and CPUs all fall under the care of our dedicated teams, to include all services and software provisioned for our clients to use.

The following are all **CoreWeave responsibilities** described in depth from our Shared Responsibility Model.

### Platform layer

| Responsibility | Description |
| - | - |
| **Kubernetes Container Orchestration** | The proper functionality, security, and operations of CoreWeave's Kubernetes cluster is the responsibility of CoreWeave. |
| **API Services** | The functionality and availability of all API services pertaining to CoreWeave Cloud is the responsibility of CoreWeave. |
| **Identity and Access Management Platform** | The functionality and security of the Identity and Access Management Platform offered to Clients through CoreWeave Cloud platform services is the responsibility of CoreWeave. |
| **Cloud Console** | The reliability, accessibility, serviceability and security of the CoreWeave Cloud Console is the responsibility of CoreWeave. |
| **Virtual Private Cloud** | The reliability, accessibility, serviceability and security of [CoreWeave VPCs](https://docs.coreweave.com/products/networking.md#virtual-private-clouds) is the responsibility of CoreWeave. |

### Compute layer

| Responsibility | Description |
| - | - |
| **Operating System** | The integrity of all native Operating Systems offered directly through CoreWeave Cloud Console (but not guest OSes through container images, which [fall under the responsibility of the Client](#client-responsibilities)) is the responsibility of CoreWeave. |
| **Container Support** | The health and functionality of CoreWeave deployed software within the CoreWeave Kubernetes cluster is the responsibility of CoreWeave, noted by "cw-" prefixed namespaces. |
| **Hardware Drivers** | The integrity of any drivers installed on CoreWeave hardware is the responsibility of CoreWeave. |
| **Health Checking and Node Lifecycle** | The availability and serviceability of CoreWeave infrastructure is the responsibility of CoreWeave. |
| **Endpoint Detection and Response** | The monitoring of all CoreWeave endpoints to ensure security and functionality is the responsibility of CoreWeave. |

### Network layer

| Responsibility | Description |
| - | - |
| **Internal and External Connectivity** | CoreWeave leverages BlueField DPUs for access to one or multiple VPCs, with optional internet access. CoreWeave maintains the security of these connections made by Clients. |
| **Network Encapsulation** | VPCs are encapsulated as industry standard Layer 3 EVPN VXLAN which is secured and the responsibility of CoreWeave |
| **VPC Isolation** | Tenant isolation inside of all VPCs provisioned by Clients are secured through the configuration of DPUs and hosts which are the responsibility of CoreWeave. |
| **Direct Connect** | The security of all Direct Connects is maintained by CoreWeave through the use of industry standard MACsec protection for securing Client data |

### Physical layer

| Responsibility | Description |
| - | - |
| **Data Center Security** | The security of all data centers internal and external, to include CoreWeave hardware assets within them are the responsibility of CoreWeave. |
| **Power and Cooling** | The availability and proper flow of power, as well as the availability and proper flow of data center cooling, is the responsibility of CoreWeave. |
| **IT Inventory and Asset Management** | Processing hardware inventory and access to CoreWeave hardware is the responsibility of CoreWeave. |
| **Physical** | The integrity and serviceability of the physical networking infrastructure for CoreWeave is the responsibility of CoreWeave. |
