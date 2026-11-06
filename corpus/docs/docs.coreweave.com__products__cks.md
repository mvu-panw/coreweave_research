# Introduction to CoreWeave Kubernetes Service (CKS)

Source: https://docs.coreweave.com/products/cks

# Introduction to CoreWeave Kubernetes Service (CKS)

> High-performance managed Kubernetes on bare metal with DPU isolation and per-cluster VPCs

# Kubernetes on bare-metal GPUs

CoreWeave Kubernetes Service runs your clusters directly on bare-metal GPU Nodes, with DPU isolation, per-cluster VPCs, and InfiniBand networking built for large-scale training, inference, and HPC.

**CoreWeave Kubernetes Service (CKS)** offers a managed Kubernetes service that lets you run clusters on [bare metal servers](https://docs.coreweave.com/products/cks/clusters/introduction.md) in CoreWeave Cloud. CKS is built to offer granular control, high performance, enhanced security, and high reliability, as well as high visibility into cluster metrics. CKS is designed to serve as a managed workload orchestration solution for High-Performance Computing (HPC) workloads, taking advantage of bare-metal performance and HPC networking.

On CKS, clusters use Data Processing Unit (DPU) (A Data Processing Unit (DPU) is a 'computer-in-front-of-a-computer', fully isolated from the host's CPU, that provides network and other functions.) technology to provide enhanced isolation and performance. Each CKS cluster operates within its own private Virtual Private Cloud (VPC). This offers a level of security and acceleration among managed Kubernetes solutions that is unique among major cloud providers.

## Choose your path

Choose a path based on what you need to do. **Create and manage clusters** covers cluster and Node operations. **Configure cluster access** covers authentication to existing clusters. **Deploy workloads** covers scheduling, Charts, and frameworks. **Secure your cluster** covers optional private access, workload identity, and Object Storage federation.

> [card] [Create and manage clusters](https://docs.coreweave.com/products/cks/clusters/create.md)
>
> Create clusters and Node Pools, and manage Nodes.

> [card] [Configure cluster access](https://docs.coreweave.com/products/cks/auth-access/introduction.md)
>
> Authenticate users to an existing cluster with Managed Auth or an external identity provider.

> [card] [Deploy workloads](https://docs.coreweave.com/products/cks/deploy-model.md)
>
> Schedule workloads, use CoreWeave Charts and third-party frameworks, and follow tutorials.

> [card] [Secure your cluster](https://docs.coreweave.com/products/cks/auth-access/tailscale-vpn.md)
>
> Private API access, workload identity, and Object Storage federation.

### Create and manage clusters

If you're new to CoreWeave, start with [Get started with CoreWeave](https://docs.coreweave.com/get-started.md) for account activation, Identity and Access Management (IAM), and tool setup.

Complete these steps to create a cluster and make it usable:

1. [Create a CKS cluster](https://docs.coreweave.com/products/cks/clusters/create.md).
2. [Create a Node Pool](https://docs.coreweave.com/products/cks/nodes/create.md).
3. [Configure cluster access](https://docs.coreweave.com/products/cks/auth-access/introduction.md).

To maintain an existing cluster, [manage Node Pools](https://docs.coreweave.com/products/cks/nodes/manage.md), [check Node Pool status](https://docs.coreweave.com/products/cks/nodes/nodepool-status.md), [cordon Nodes](https://docs.coreweave.com/products/cks/nodes/cordon.md), [reboot Nodes](https://docs.coreweave.com/products/cks/nodes/reboot.md), or [connect to a Node](https://docs.coreweave.com/products/cks/nodes/connect.md) for troubleshooting. For how CoreWeave provisions and repairs Nodes, see [Node Lifecycle](https://docs.coreweave.com/platform/fleet-management/node-lifecycle.md) under **Nodes and Node Pools**.

To customize DNS resolution for Pods, [configure DNS overrides on CKS](https://docs.coreweave.com/products/networking/configure-dns-overrides.md) for private-domain forwarding or hostname mappings.

### Configure cluster access

Use [Configure cluster access](https://docs.coreweave.com/products/cks/auth-access/introduction.md) after a cluster exists to choose how users authenticate to its Kubernetes API. Platform identity, Managed Auth, SAML, API access tokens, and IAM roles live in the Security docs. CKS pages cover Managed Auth kubeconfig and unmanaged authentication. Private API access, workload identity, and Object Storage federation live under **Secure your cluster**.

### Deploy workloads

When you already have a cluster, use these resources to run workloads:

* [Deploy an open source LLM](https://docs.coreweave.com/products/cks/deploy-model.md) for an end-to-end first workload.
* Read [Workload scheduling](https://docs.coreweave.com/products/cks/clusters/scheduling/workload-scheduling.md) to learn how CKS places Pods, including interruptible workloads and Internode Memory Exchange (IMEX).
* Review [Container runtimes](https://docs.coreweave.com/products/cks/container-runtimes.md) for isolation options, platform compatibility, and support limitations.
* Install [CoreWeave Charts](https://docs.coreweave.com/products/cks/clusters/coreweave-charts/introduction.md) or use a [third-party framework](https://docs.coreweave.com/products/cks/clusters/frameworks/introduction.md).
* Follow a tutorial such as [Deploy vLLM for Inference](https://docs.coreweave.com/products/cks/tutorials/deploy-vllm-inference.md).

### Secure your cluster

Use these guides for optional or advanced hardening after you have a cluster:

* [Access a CKS cluster through Tailscale VPN](https://docs.coreweave.com/products/cks/auth-access/tailscale-vpn.md) for private API access.
* [Workload Identity](https://docs.coreweave.com/products/cks/auth-access/workload-identity/introduction.md) when Pods need short-lived credentials for external services.
* [CKS Workload Federation for AI Object Storage](https://docs.coreweave.com/security/tutorials/cks-object-storage-authentication.md) to federate access to Object Storage.

## How CKS is different

The following sections describe how CKS differs from other managed Kubernetes services.

### High-performance Kubernetes on high-performance compute

CKS is engineered to orchestrate and serve highly computationally intensive workloads, designed for model training, inference, and HPC tasks.

* CKS harnesses CoreWeave's extensive fleet of high-performance [GPU](https://docs.coreweave.com/platform/instances/gpu-instances.md) and [CPU](https://docs.coreweave.com/platform/instances/cpu-instances.md) servers and [advanced HPC networking infrastructure](https://docs.coreweave.com/products/networking/hpc-interconnect/about-hpc-interconnect.md) to maximize throughput and minimize latency.
* CKS runs Kubernetes directly on bare metal Nodes. With CoreWeave coordination, [Kata container runtimes](https://docs.coreweave.com/products/cks/container-runtimes.md) can run individual Pods inside VMs.
* CKS clusters use NVIDIA® BlueField® [Data Processing Units](https://docs.coreweave.com/products/networking/nimbus.md) (DPUs (A Data Processing Unit (DPU) is a 'computer-in-front-of-a-computer', fully isolated from the host's CPU, that provides network and other functions.)) attached to each Node to offload processing tasks. This allows the Node to focus primarily on executing application workloads.
* CKS Nodes are stateless. At each boot, they load a clean Operating System image. This allows Nodes to be rapidly scaled and re-provisioned, and ensures that all Nodes use the correct software versions.
* Clusters integrate with an InfiniBand fabric that features a non-blocking, Fat-Tree architecture with [NVIDIA® Scalable Hierarchical Aggregation and Reduction Protocol (SHARP)™](https://docs.nvidia.com/networking/software/accelerator-software/index.html#nvidia-sharp) optimizations. These optimizations are capable of supporting the demand of tasks like training Large Language Models (LLMs) across clusters comprised of thousands of GPU instances. CoreWeave doesn't turn on SHARP by default. See [NCCL network plugin guidance](https://docs.coreweave.com/products/networking/hpc-interconnect/nccl-configuration-reference.md#nccl-network-plugin-guidance) to learn how to enable SHARP.

#### Do not install the NVIDIA GPU Operator on CKS clusters

> [!WARNING]
>
> CoreWeave manages the [NVIDIA GPU Operator](https://docs.nvidia.com/datacenter/cloud-native/gpu-operator/latest/getting-started.html) on your behalf. Do not install the NVIDIA GPU Operator on CKS clusters. Doing so conflicts with the platform-managed deployment and is not supported.

### Hyper-secure infrastructure

CKS is engineered with a strong emphasis on security.

* The [DPU-based architecture](https://docs.coreweave.com/products/networking/nimbus.md) used by CKS enables advanced security features including custom network and security policies, dedicated [Virtual Private Clouds (VPCs)](https://docs.coreweave.com/products/networking/vpc/about-vpcs.md), and privileged network access controls.
* CoreWeave houses physical infrastructure in high-surveillance data centers, providing comprehensive security. Within the CKS platform, your data is operationally isolated, ensuring complete separation and confidentiality.

### Data Plane flexibility

CKS provides a managed Control Plane alongside configurable Data Plane elements. This strikes a balance between operational simplicity and the flexibility to tailor the environment to specific workload requirements.

* CKS clusters include a pre-installed [Container Storage Interface (CSI) and Container Network Interface (CNI)](https://docs.coreweave.com/products/cks/reference/cluster-components.md) to standardize storage and networking across container environments.
* Unlike other managed Kubernetes services, CKS extends your control beyond the Control Plane by allowing direct management of [Data Plane components](https://docs.coreweave.com/products/cks/reference/cluster-components.md). This approach minimizes your infrastructure management burden while still offering extensive customization possibilities.

## Additional advantages

The following sections describe additional advantages that CKS offers.

### Privilege and access management

CKS offers comprehensive privilege management, balancing managed solutions with the flexibility of self-managed ones. This gives you the freedom to choose the most suitable option for your security needs.

[CKS Managed Auth](https://docs.coreweave.com/security/authn-authz/managed-auth/introduction.md) provides a managed solution backed by role-based access control (RBAC) for cluster-wide access control and organization management. CKS supports third-party RBAC providers for granular in-cluster permissions.

### Metrics and observability

CKS provides comprehensive support for auditing and compliance requirements. You can also integrate performance and data metrics with your existing infrastructure, enabling a flexible observability solution.

* For enhanced monitoring, CKS grants access to the CKS cluster API server, enabling Control Plane audit logs.
* This extensive access also lets you deploy your own metrics stacks with custom collection tools, including DaemonSet or Loki logging.
* You can also monitor Node logs, GPU utilization, and other Node-level metrics through [CoreWeave Grafana](https://docs.coreweave.com/observability/managed-grafana.md).

### Node lifecycle

CoreWeave validates every Node before it joins your cluster and continuously monitors it in production. See [Node lifecycle](https://docs.coreweave.com/platform/fleet-management/node-lifecycle.md) for Day 0 through Day 2+ operations, and [Node state transitions in CKS](https://docs.coreweave.com/platform/fleet-management/node-lifecycle/state-transitions.md) for how remediations appear inside your cluster.
