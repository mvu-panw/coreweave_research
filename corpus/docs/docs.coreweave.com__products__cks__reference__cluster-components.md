# Cluster components

Source: https://docs.coreweave.com/products/cks/reference/cluster-components

# Cluster components

> Reference for the components within the CKS Managed Control Plane and Managed Data Plane

## Kubernetes versions

CoreWeave Kubernetes Service (CKS) supports the three latest Kubernetes versions. When the upstream project releases a new version, we test it for compatibility and performance, then add it to the CKS support matrix. This happens three times a year, about every 120 days.

### Supported versions

New clusters use the latest supported version by default, but you can choose any supported version and its associated [control group (cgroup)](https://kubernetes.io/docs/concepts/architecture/cgroups/) from the list below when you create a new cluster.

> [!WARNING]
>
> **cgroup v2 requirement for v1.35 and later**
>
> When you upgrade to v1.35 or later, all Nodes must use `cgroup v2`. Kubernetes v1.35 and later don't support `cgroup v1`.

| Kubernetes Version | Control Group Version | DRA Enablement | Notes |
| - | - | - | - |
| `v1.35` | `cgroup v2` | Yes | |
| `v1.36` | `cgroup v2` | Yes | |
| `v1.37` | `cgroup v2` | Yes | Default version for new clusters |

To ensure your cluster has access to new features, security patches, and stability improvements, [update it to a supported version](https://docs.coreweave.com/products/cks/clusters/upgrade-kubernetes.md) before it is deprecated.

### Deprecated versions

These versions are no longer supported for new CKS clusters.

| Kubernetes Version | Control Group Version | Notes |
| - | - | - |
| `v1.29` | `cgroup v1` | Deprecated |
| `v1.30` | `cgroup v1` | Deprecated |
| `v1.31` | `cgroup v1` | Deprecated |
| `v1.32` | `cgroup v1` | Deprecated |
| `v1.33` | `cgroup v2` | Deprecated |
| `v1.34` | `cgroup v2` | Deprecated |

While existing clusters can continue to use these deprecated versions, CoreWeave's ability to support them is limited by the [upstream support period](https://kubernetes.io/releases/patch-releases/#support-period).

## Managed Control Plane

To ensure security and stability, CoreWeave provides a Managed Control Plane for CKS clusters. Learn more about [CKS cluster architecture](https://docs.coreweave.com/products/cks/clusters/introduction.md).

The managed Cluster Autoscaler includes ProvisioningRequest support, enabled by default on all CKS clusters. CoreWeave installs the `provisioningrequests.autoscaling.x-k8s.io` custom resource definition (CRD). For details, see [Provisioning requests](https://docs.coreweave.com/products/cks/nodes/autoscaling.md#provisioning-requests).

## Managed Data Plane components

The CKS Managed Data Plane comes with several preinstalled components, which let you start running workloads immediately after you deploy your CKS cluster. These components are configurable to support the desired state of a CKS cluster.

On clusters created on or after July 7, 2025, CoreWeave runs these components out-of-band on the CKS Control Plane, while some continue to run on your own Node Pools. Clusters created before that date instead ran them on a dedicated `cpu-control-plane` Node Pool, which CoreWeave no longer provisions. For the list of affected components and where each one runs, see the [Control Plane Node Pools release note](https://docs.coreweave.com/release-notes/control-plane-node-pools.md).

> [!NOTE]
>
> * Some older clusters' namespaces may not have the `cw-` prefix shown in the tables below.
> * Components and API versions change often. The versions deployed to your cluster may be newer than shown below.

### Networking

| Component | Namespace | Version | Description |
| - | - | - | - |
| `calico` (deprecated) | `cw-calico-system` | `3.29.1` | Container Network Interface (CNI) used on older clusters; no longer supported for new CKS clusters. |
| [`cilium`](https://github.com/cilium/cilium) | `cw-cilium-system` | `v1.18.1` | Container Network Interface (CNI) that uses eBPF for efficient load-balancing. |
| [`coredns`](https://github.com/coredns/coredns) (internally versioned) | | `v1.5.1` | A flexible DNS server consisting of [multiple plugins](https://coredns.io/plugins/) that manage in-cluster DNS and resolve service records inside clusters. This runs in the CKS Managed Control Plane. |
| [`konnectivity-agent`](https://kubernetes.io/docs/tasks/extend-kubernetes/setup-konnectivity/) | `kube-system` | `v0.37.0` | Isolates CKS Control Plane traffic from the cluster network and creates a TCP level proxy to `konnectivity-server`, which sits alongside the Control Plane to tunnel traffic from the Control Plane to in-cluster endpoints. |
| [`metallb`](https://github.com/metallb/metallb) | `cw-metallb-system` | `v0.13.4-90f9edd` | Handles IP Address Management (IPAM) for `LoadBalancer` services; is not used for advertisements. See [How to: Expose a Service](https://docs.coreweave.com/products/networking/ingress-service/expose-service-dns.md) |
| `multus-cni` | | | Enables attaching multiple network interfaces to Pods. Used to configure InfiniBand as a secondary interface for workloads that require high throughput and low latency in HPC environments. |
| [`node-local-dns`](https://kubernetes.io/docs/tasks/administer-cluster/nodelocaldns/) (internally versioned) | `kube-system` | `v1.0.2` | Improves cluster DNS performance and speeds up traffic between CoreDNS instances. The `node-local-dns` Pods run CoreDNS in local caching mode as a DaemonSet over TCP, avoiding dropped packets and reducing tail latency. |

#### Networking notes

* To customize DNS resolution, use the supported `node-local-dns-overrides` ConfigMap in `kube-system`. CoreWeave manages the DNS components that read it. See [Configure DNS overrides on CKS](https://docs.coreweave.com/products/networking/configure-dns-overrides.md).
* Cilium, like CKS, is a managed product. We deploy Cilium with a minimal feature set. If you require a feature that isn't enabled, or is only available in Cilium Enterprise, [contact support](https://docs.coreweave.com/support.md).
* Argo CD has [documented issues](https://docs.cilium.io/en/stable/configuration/argocd-issues/) with Cilium when you don't use [annotation tracking](https://argo-cd.readthedocs.io/en/stable/user-guide/resource_tracking/#additional-tracking-methods-via-an-annotation). To prevent issues, [declare resource exclusions in the Argo CD ConfigMap](https://docs.cilium.io/en/stable/configuration/argocd-issues/#argo-cd-deletes-customresourcedefinitions).
* If you require a specific CNI (such as *Cilium Enterprise* instead of *Cilium Open Source*), you can bring your own. This manual process requires coordination with CoreWeave when you deploy the cluster. [Contact support](https://docs.coreweave.com/support.md) for more information.

### Cluster management

| Component | Namespace | Version | Description |
| - | - | - | - |
| `hpc-verification` | `cw-hpc-verification` | `v3.5.11` | Validates the Node is in an optimal state. These tests [only run on idle Nodes](https://docs.coreweave.com/platform/fleet-management/hpc-verification.md). |
| [`nfd`](https://github.com/kubernetes-sigs/node-feature-discovery) | `cw-nfd` | `v1.1.0` | Node Feature Discovery. Detects hardware features and labels Nodes accordingly for use in scheduling decisions. |
| [`node-problem-detector`](https://github.com/kubernetes/node-problem-detector) | `cw-node-problem-detector` | `v1.16.0` | Framework for running health checks for each Node run as a DaemonSet. It allows CoreWeave to quickly identify Nodes that are misbehaving and mark them as `Unschedulable`. |

> [!NOTE]
>
> Older clusters may have `jspolicy` installed in the `jspolicy-policies-[ORG-ID]-[CLUSTER-ID]` and `tenant-[ORG-ID]-[CLUSTER-ID]` namespaces. Newer clusters don't include JSPolicy.

### Observability and security

| Component | Namespace | Version | Description |
| - | - | - | - |
| `chrony-exporter` | `cw-exporters` | `v1.0.0` | Exporter for Chrony NTP. |
| `crowdstrike` | `cw-crowdstrike` | `7.29.0-18202-1.falcon-linux.Release.US-2` | [CrowdStrike Falcon](https://www.crowdstrike.com/en-us/) cybersecurity tooling. |
| `dcgm-exporter` | `cw-exporters` | `4.4.1-4.6.0-ubuntu22.04` | Exports NVIDIA Data Center GPU Manager (DCGM) metrics. |
| `gpu-thermal-exporter` | `cw-exporters` | `v1.1.0` | Emits hardware metrics for GPU thermal data for Node health monitoring. |
| [`metrics-server`](https://github.com/kubernetes-sigs/metrics-server) | `kube-system` | `0.6.2` | Only installed on clusters deployed [before July 7, 2025](https://docs.coreweave.com/release-notes/control-plane-node-pools.md). |
| `node-exporter` | `cw-exporters` | `v1.0.0` | Exports hardware and OS metrics exposed by \*NIX kernels. |
| `node-pci-exporter` | `cw-exporters` | `v1.1.0` | Exports the operating system's PCI tree as metrics, representing the current and capable width and speed of every device available on the PCI bus. |
| `nvlink-exporter` | `cw-exporters` | `v1.1.0` | Exports metrics for NVLink performance in GPU Nodes. |
| `ping-exporter` | `cw-ping-exporter` | `v1.3.0` | Measures packet loss to configured network targets for connectivity checks. |
| `promtail` | `cw-promtail` | `3.2.0` | Forwards Node logs centrally using Grafana's Promtail. |
| `transceiver-exporter` | `cw-exporters` | `v1.0.0` | Provides diagnostics for pluggable transceivers (SFP, SFP+, QSFP, and other types) using the [ethtool](https://docs.nvidia.com/doca/sdk/ethtool/index.html) library |
| [`victoria-metrics`](https://victoriametrics.com/) | `cw-victoria-metrics` | `v0.61.2` | Collects metrics from inside the cluster and relays them to a logging solution. |
| [`vmagent`](https://victoriametrics.com/) | `cw-victoria-metrics` | `v1.123.0` | Gathers metrics for Victoria Metrics. |

### Storage

| Component | Namespace | Version | Description |
| - | - | - | - |
| [`vast-csi`](https://github.com/vast-data/vast-csi) | `cw-vast-csi` | `v2.4.2` | Container Storage Interface for VAST Storage. |

### Object Storage

| Component | Namespace | Version | Description |
| - | - | - | - |
| [`lota`](https://docs.coreweave.com/products/storage/object-storage/improving-performance/about-lota) | `cw-object-storage` | `v2.2.6` | CoreWeave's **Local Object Transport Accelerator (LOTA)** for AI Object Storage. [Learn more about LOTA.](https://docs.coreweave.com/products/storage/object-storage/improving-performance/about-lota.md) |

### Hardware

| Component | Namespace | Version | Description |
| - | - | - | - |
| [`gpu-operator`](https://github.com/NVIDIA/gpu-operator) | `cw-nvidia-gpu-operator` | `v25.3.0` | CoreWeave manages the NVIDIA GPU Operator on recent clusters. Manages the lifecycle of GPU-related components such as the device plugin, GPU Feature Discovery (GFD), and more. |
| [`k8s-device-plugin`](https://github.com/NVIDIA/k8s-device-plugin) (deprecated) | `cw-nvidia-device-plugin` | `v0.17.0-2cb7b71` | Standalone NVIDIA device plugin used on older clusters. Replaced by the GPU Operator-managed device plugin. |
| [`k8s-dra-driver-gpu`](https://github.com/kubernetes-sigs/dra-driver-nvidia-gpu) | `cw-nvidia-gpu-operator` | `v25.8.0` | NVIDIA's DRA driver for GPUs. Required for [IMEX with DRA](https://docs.coreweave.com/products/cks/clusters/scheduling/imex-dra-scheduling.md). Currently used only for IMEX channel allocation via `ComputeDomain` resources. GPU allocation via DRA is not supported today. |
| `nvidia-imex` (deprecated) | `cw-nvidia-imex` | `v1.2.0` | Previously provided transparent IMEX channel access to all Pods. Replaced by [IMEX with DRA](https://docs.coreweave.com/products/cks/clusters/scheduling/imex-dra-scheduling.md). |
| `rdma-shared-dp` | `cw-rdma` | `1.4.0` | Device plugin to support InfiniBand and RDMA hardware resources. |

#### Do not install the NVIDIA GPU Operator on CKS clusters

> [!WARNING]
>
> CoreWeave manages the [NVIDIA GPU Operator](https://docs.nvidia.com/datacenter/cloud-native/gpu-operator/latest/getting-started.html) on your behalf. Do not install the NVIDIA GPU Operator on CKS clusters. Doing so conflicts with the platform-managed deployment and is not supported.
