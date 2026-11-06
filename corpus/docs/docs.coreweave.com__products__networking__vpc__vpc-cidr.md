# VPC CIDR blocks

Source: https://docs.coreweave.com/products/networking/vpc/vpc-cidr

# VPC CIDR blocks

> Learn how VPCs use CIDR notation to define address ranges

CoreWeave VPCs (A Virtual Private Cloud (VPC) is a private network hosted within a public cloud infrastructure.) use Classless Inter-Domain Routing (CIDR) (Classless Inter-Domain Routing (CIDR) is a method for allocating IP addresses and routing IP packets.) notation to define IP address ranges for the hosts, Pods, Load Balancers, and other Services used in each VPC. This page describes how to size and assign CIDR blocks when you configure a VPC, so you can plan address space that supports your workloads and integrates cleanly with other networks.

Understanding CIDR blocks is especially useful if you need to know IP ranges before you integrate with existing environments, such as with [Direct Connect](https://docs.coreweave.com/products/networking/direct-connect/about-direct-connect.md).

When you plan your network architecture, allocate enough IP addresses for your Nodes and their associated services. To convert CIDRs to IP address ranges, we recommend the [ARIN CIDR Calculator](https://account.arin.net/public/cidrCalculator).

## Configure CIDR blocks in VPCs

Use the following YAML fields to assign CIDR ranges to each resource type when you create or edit a VPC configuration. The following example shows a single VPC containing multiple clusters, with different CIDR ranges assigned to different resources:

```yaml title="Example vpc.yaml" highlight={5-6,21-23} theme={"system"}
organizations:
  abc123:
    vpcs:
      default-us-east-04:
        hostPrefixes:
          - 10.176.192.0/18
        pubImport: true
        site: us-east-04
    clusters:
      poc-gpu:
        version: v1.30
        site: us-east-04
        vpc: default-us-east-04
        podCIDR: 10.24.0.0/13
        serviceCIDR: 10.32.0.0/22
        internalLbCIDR: 10.32.4.0/22
      poc-cpu:
        version: v1.30
        site: us-east-04
        vpc: default-us-east-04
        podCIDR: 10.48.0.0/13
        serviceCIDR: 10.56.0.0/22
        internalLbCIDR: 10.56.4.0/22
```

### CIDR block size guidelines

CIDR blocks for Nodes, Pods, Services, and Load Balancers have different subnet allocation limits. The following guidelines are based on the maximum number of resources each CIDR block can accommodate:

| Key | Value | Description |
| - | - | - |
| `hostPrefixes` | `/18` | A `/18` CIDR block supports up to 4,000 **Nodes**. Each Node requires `2` IP addresses. |
| `podCIDR` | `/13` | A `/13` CIDR block supports up to 100 **Pods** per Node. |
| `serviceCIDR` | `/22` | A `/22` CIDR block supports up to 1,000 **Services**. |
| `internalLbCIDR` | `/22` | A `/22` CIDR block supports up to 1,000 **Load Balancers**. |

> [!NOTE]
>
> If you have a smaller environment, you can use smaller CIDR ranges. For example, if you plan only 500 Nodes for the cluster, a large CIDR block isn't required. However, smaller CIDR ranges can limit future expansion, since Service IPs must be contiguous.

### Pod CIDR capacity planning

CKS uses Cilium for Pod networking, and Cilium allocates a fixed block of 128 Pod IP addresses per Node. This block size doesn't change when you lower the maximum Pods per Node, so the Pod CIDR sets a hard ceiling on how many Nodes the cluster can ever hold. Size the Pod CIDR for the total Node count you plan to reach, summed across every Node Pool:

| Pod CIDR size | Maximum Nodes |
| - | - |
| `/17` | 256 |
| `/16` | 512 |
| `/15` | 1,024 |
| `/14` | 2,048 |
| `/13` | 4,096 |

The Node count includes both GPU and CPU Node Pools. For example, a cluster planned for 256 GPU Nodes plus any CPU Nodes exceeds the 256-Node limit of a `/17`, so it needs at least a `/16`.

When a cluster runs out of Pod IP addresses, new Nodes can't get Pod IPs, system Pods fail to start on them, and the Node Pool can report an `InternalError` status. If Node delivery fails as you approach a 256, 512, or 1,024 Node boundary, check Pod CIDR capacity before investigating Node hardware. On a cluster provisioned with too small a Pod CIDR from the start, the symptom can instead be Cilium agent Pods entering `CrashLoopBackOff`, followed by a cascade of downstream Pod failures. For a Node Pool already at its ceiling, contact support: expanding a live cluster's Pod CIDR is a coordinated change, and on Direct Connect clusters it also requires advertising the new range.

### Avoid rapidly recreating VPCs with the same name

VPC creation runs as an asynchronous workflow. If you delete a VPC and immediately recreate it with the same name, the new VPC can get stuck in a creating state for an extended period. When you test VPC creation and teardown, use a different, throwaway name for each attempt instead of reusing one name in quick succession.

Treat a VPC as effectively immutable once you associate Direct Connect or custom endpoints with it. Deleting and recreating such a VPC destroys the provisioned resources and assigns a new VPC identifier, which also invalidates any infrastructure-as-code state that referenced the old identifier.

If a VPC or cluster creation fails with a generic error such as "invalid request" in the Cloud Console, suspect a CIDR overlap with an existing VPC range. The VPC API returns a more descriptive error than the console surfaces, so check your new prefixes against existing VPC ranges.

## Plan CIDRs for connected VPCs

If your architecture connects multiple VPCs, plan address space carefully to avoid routing conflicts. When you connect two CoreWeave VPCs between CKS clusters, you must plan unique, non-overlapping address space across the clusters. At a minimum, the two clusters must have non-overlapping internal Load Balancer CIDR blocks. To simplify routing between VPCs, keep all CIDR ranges in each cluster non-overlapping, including the Pod, Service, and Load Balancer CIDRs.

Set non-overlapping CIDR ranges when you create or edit each VPC in the Cloud Console. For the configuration flow, see [Create and manage VPCs](https://docs.coreweave.com/products/networking/vpc/create-manage-vpcs.md). For automation, you can provision VPCs and their prefixes with the VPC API (for example, with the `hostPrefixes` and `vpcPrefixes` fields).

Non-overlapping address space also benefits multi-cluster networking tools. If you use [Liqo](https://docs.liqo.io/en/v1.0.0/) for multi-cluster networking, its network fabric prefers NAT-less communication when PodCIDRs are disjoint, and applies address translation only when overlaps exist.

Same-zone connectivity between two separate VPCs isn't a standard self-service product. If you need to connect clusters in the same zone across separate VPCs, contact support or engage your CoreWeave representative to discuss the supported options for your deployment.

## Advertise the right prefixes over Direct Connect

When you connect a cluster to your network over Direct Connect, advertise prefixes deliberately:

* Advertise Pod IP ranges and LoadBalancer ranges as needed for the traffic you expect. Pod ranges are appropriate to advertise when on-premises systems must reach Pods directly.
* Don't advertise the Service (ClusterIP) CIDR. ClusterIP addresses are virtual and resolve only inside the cluster, so routes to that range aren't usable from your network.

Keep advertisements compact. Direct Connect sessions enforce limits on the number of routes you can advertise, so advertising a default route or a small number of aggregates is more sustainable than advertising many specific prefixes. For provider-specific details, see [About Direct Connect](https://docs.coreweave.com/products/networking/direct-connect/about-direct-connect.md).

## Locked-down VPCs and Node boot

A VPC with restricted public egress can prevent new Nodes from booting if the boot path can't reach the CoreWeave Node image host. If you run a locked-down VPC, make sure your egress rules allow DNS resolution and the image fetch that Node boot requires. Restricted egress can also block a booted Node from reaching the cluster API server, which produces the same symptom of Nodes failing delivery and churning. If new Nodes time out during boot in a restricted VPC, confirm the boot path is reachable before you investigate the Nodes themselves.

## Additional resources

### How-to guides

* [Create and manage VPCs](https://docs.coreweave.com/products/networking/vpc/create-manage-vpcs.md)

### References

* [VPC API](https://docs.coreweave.com/products/networking/vpc/vpc-api.md)
