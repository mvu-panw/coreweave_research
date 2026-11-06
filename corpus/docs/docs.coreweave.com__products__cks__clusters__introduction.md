# Introduction to clusters

Source: https://docs.coreweave.com/products/cks/clusters/introduction

# Introduction to clusters

> Introduction to CKS clusters as bare-metal Kubernetes infrastructure with managed control and data planes

[CoreWeave Kubernetes Service (CKS)](https://docs.coreweave.com/products/cks.md) provides high-performance computing and a flexible Kubernetes experience by running Kubernetes on bare metal. This page introduces the architecture of CKS clusters, explains how the managed control and data planes work together, and outlines the advantages of running Kubernetes directly on dedicated hardware. Read this page to understand the foundational concepts before creating or operating CKS clusters.

## Kubernetes on bare metal

The following sections describe what running Kubernetes on bare metal means and the benefits it provides.

CKS runs Kubernetes directly on bare metal GPU Nodes without any intermediary software, such as a hypervisor or virtual machine. This direct hardware access is the defining difference of CKS. Nodes in your cluster access their GPUs without any virtualization overhead.

![Difference between bare metal versus hypervisor.](https://mintcdn.com/coreweave-dbfa0e8d/PdmoozL7fT8Luz34/products/cks/_media/bare-metal.png?fit=max\&auto=format\&n=PdmoozL7fT8Luz34\&q=85\&s=6a6c83ad8237514f82b1545dbcfcae94)

CoreWeave maintains, scales, and updates Kubernetes clusters that run directly on Nodes hosted in CoreWeave regions. CKS provides the following benefits by eliminating most of the virtualized intermediary stages between customer and cluster:

* **Better performance**: Virtualization layers aren't competing for hardware resources.
* **Increased efficiency**: Quicker data access and processing.
* **Reduced latency**: Applications have direct access to the underlying hardware.
* **Better observability**: More fine-grained access to kernel logs and Node behavior.

## CKS clusters

CKS clusters grant you privileged access to Kubernetes resources. You run workloads on your own dedicated hardware. These servers operate independently of other operations and connect through isolated [Virtual Private Clouds (VPCs)](https://docs.coreweave.com/products/networking/vpc/about-vpcs.md). Host permissions to Nodes are also securely managed within VPCs, so you don't need to manage the underlying infrastructure.

CKS uses clusters to provide efficient, scalable, secure Kubernetes workload orchestration. Containers access server hardware directly, which suits workloads such as model training and VFX rendering. The architecture and components are designed for efficiency, low latency, and customization.

## Cluster architecture

The following sections describe the two planes that make up a CKS cluster and the role each plays in cluster operation.

CKS (CoreWeave Kubernetes Service (CKS) is CoreWeave's managed Kubernetes service.) clusters use two planes:

* The **Managed Data Plane**
* The **Managed Control Plane**

Each plane has distinct components responsible for different functionalities within the cluster.

The **Managed Control Plane** is a Kubernetes Control Plane managed by CoreWeave, providing a managed Kubernetes environment that is secure, stable, and optimized for high-performance computing tasks. CoreWeave builds the Managed Control Plane to take advantage of high-performance computing (HPC) hardware, and designs it to support compute-intensive applications.

The Managed Control Plane includes [components](https://docs.coreweave.com/products/cks/reference/cluster-components.md) that manage the overall state and lifecycle of CKS clusters. These components handle cluster orchestration, scheduling, and control functionality.

The **Managed Data Plane** includes components responsible for handling the data traffic and operations within the Kubernetes cluster. These components ensure that the workloads are managed efficiently and securely, and can be customized for flexibility.

CoreWeave runs these managed components out-of-band on the CKS Control Plane, while some continue to run on your own Node Pools. For the components affected and where each one runs, see the [Control Plane Node Pools release note](https://docs.coreweave.com/release-notes/control-plane-node-pools.md).

> [!NOTE]
>
> Learn more about [the specific components within the Managed Control Plane and Managed Data Plane](https://docs.coreweave.com/products/cks/reference/cluster-components.md), and how they support CKS cluster performance.

### Region-level image proxy

CoreWeave operates a region-level registry proxy that accelerates container image pulls and reduces exposure to public registry rate limits for your cluster's Nodes.

The proxy has the following advantages:

* Caches some image layers to improve startup time and lower bandwidth consumption.
* Caches image metadata (manifests) to mitigate external rate limiting.

#### Avoid mutable tags

> [!WARNING]
>
> Mutable tags behave as if they are immutable. For example, using `:latest` doesn't pull the latest image since the proxy serves only the cached manifest, which might not be the latest. Therefore, avoid reusing tags like `:latest` across different image builds. Doing so can result in Nodes pulling an older cached manifest until the cache expires.

To load the correct image, you must use immutable tags or pin by digest for production workloads to avoid "sticky" results from proxy metadata caching.

#### Digest pinning example

Pinning by digest ensures every Node pulls the exact same artifact, independent of tag changes.

```yaml theme={"system"}
# Deployment snippet (example)
spec:
  template:
    spec:
      containers:
        - name: app
          image: registry.example.com/myapp@sha256:3f5e8b5c7ab2740c0f7b1e3e8d3d7b5f0c1a2b3c4d5e6f7081920a1b2c3d4e5f
          imagePullPolicy: IfNotPresent
```

If your workloads require it, CoreWeave can disable the transparent proxy (but not the metadata caching feature) on a per-cluster basis. To disable the transparent proxy, contact [Support](https://docs.coreweave.com/support.md) with your cluster details.

## Advantages

The following list summarizes the key benefits CKS clusters offer for compute-intensive workloads:

* **Strong security**: CKS clusters exist in their own VPCs, created by on-site networking. Isolation is built in from start to finish. Each server is equipped with a Data Processing Unit (DPU) that aids in VPC orchestration, further supporting security and performance.
* **Suited to compute-intensive workloads**: CoreWeave clusters provide Reserved Node Pools for running large jobs with static Node requirements, such as model training. Nodes are available when and where they're needed.
* **Visibility into systems**: CKS lets you run your own metrics exporters, gather detailed logs, and use low-level access for [insight](https://docs.coreweave.com/observability/logs-metrics/introduction.md) into system health.
* **Observable infrastructure**: CKS oversees your compute infrastructure, taking care of the heavy lifting while still allowing you to manage and observe resources at the Control Plane level.
