# Scheduling profiles

Source: https://docs.coreweave.com/products/cks/clusters/scheduling/scheduling-profiles

# Scheduling profiles

> Configure scheduling profiles in CKS, including binpack, best-spread, and image locality options

## Scheduling profiles in Kubernetes

With [Scheduling Profiles](https://kubernetes.io/docs/reference/scheduling/config/#profiles), you can customize the behavior of scheduling Pods onto Nodes to meet the requirements for your workloads. This page describes the Scheduling Profiles available on CKS clusters and explains when each one is appropriate, so you can choose the right Profile for your workload or confirm that the default is the best fit.

> [!WARNING]
>
> If you don't explicitly set an alternative, CKS uses the `default-scheduler` Profile automatically. CoreWeave recommends continuing to use the default Profile, `default-scheduler`, because it suits most workloads. Unless you have a specific use case that requires a different Profile, you don't need to take action.

## CKS scheduling profiles

The `default-scheduler` discourages scheduling workloads on Nodes that are incompatible with workload specifications. It's the right choice for most workloads. Use other Scheduling Profiles only in specific cases.

### Profiles for edge cases

If you have a special case that requires a specialized scheduler, the following Profiles are also available. Each Profile suits a different optimization goal, so review the descriptions to determine which one matches your workload.

#### `best-spread-scheduler`

The `best-spread-scheduler` distributes Pods across Nodes to balance resource usage and reduce the chance of any one Node becoming overloaded. By avoiding single points of failure, it can improve resource utilization, cluster reliability, and fault tolerance for workloads where even distribution matters.

#### `least-allocated-scheduler`

The `least-allocated-scheduler` prioritizes Nodes with the least allocated (that is, the most remaining available) resources when scheduling Pods. This keeps Nodes from being either overburdened or underutilized. It suits use cases where resource balancing is a higher priority than binpacking.

#### `binpack-scheduler`

The `binpack-scheduler` improves resource efficiency, which can reduce cost and energy usage. It packs as many Pods as possible onto the smallest number of Nodes, leaving any unused Nodes free. It also delays adding Nodes so that each available Node fills up first.

#### `prioritize-image-locality`

The `prioritize-image-locality` Profile favors Nodes that already have a locally cached version of a Pod's container images, which reduces the time spent pulling images from remote sources. This is useful when fast startup times are important or when container images are large.

#### `exhaustive`

The `exhaustive` Profile considers every Pod in the cluster and evaluates each scheduling option before choosing one. It evaluates the capacity of every Node before making a decision.

> [!WARNING]
>
> Choose the `exhaustive` Scheduling Profile only if you have advanced Kubernetes experience. This option can overload the API server and can be costly and time-consuming, especially for clusters running a large number of Pods.

CKS customers can't currently customize Scheduling Profiles. If you have a use case that requires something not covered on this page, [contact support](https://docs.coreweave.com/support.md).
