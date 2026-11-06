# Dynamic Resource Allocation feature gates

Source: https://docs.coreweave.com/products/cks/clusters/scheduling/dynamic-resource-featuregates

# Dynamic Resource Allocation feature gates

> Dynamic Resource Allocation feature gates by Kubernetes version in CKS.

This page lists the Kubernetes Dynamic Resource Allocation (DRA) feature gates available in CoreWeave Kubernetes Service (CKS), along with their default values, lifecycle stages, and the Kubernetes versions in which CKS enables them. Use this reference to understand which DRA capabilities are available in your CKS cluster and how CKS defaults differ from upstream Kubernetes.

## Summary

CoreWeave enables `DynamicResourceAllocation` starting in v1.30, earlier than upstream, which enables it in v1.32.

CoreWeave enables `DRAResourceClaimDeviceStatus` starting in v1.32.

## Upstream docs

For background on DRA concepts and the Kubernetes feature gate lifecycle, see the following upstream Kubernetes documentation:

* [Dynamic Resource Allocation concepts](https://kubernetes.io/docs/concepts/scheduling-eviction/dynamic-resource-allocation/#resourceclaims-templates)
* [Kubernetes feature gate stages](https://kubernetes.io/docs/reference/command-line-tools-reference/feature-gates/#feature-stages)

## Feature gates by version

| Feature gate | Default | Stage | Introduced | Deprecated | Description |
| - | - | - | - | - | - |
| `DynamicResourceAllocation` | `false` (until 1.30, CoreWeave: `true` from 1.30+) | Beta | 1.30 | - | Enables DRA framework integration with scheduling and controllers |
| `DRAResourceClaimDeviceStatus` | `false` (upstream 1.32), `true` (CoreWeave 1.32+) | Alpha to Beta | 1.32 | 1.34 | Enables `.status.devices` field in `ResourceClaim` and updates from DRA drivers |
| `DRAAdminAccess` | `false` | Alpha to Beta | 1.32 | - | Enables administrative control of DRA objects |
| `DRAConsumableCapacity` | `false` | Alpha | 1.34 | - | Adds capacity awareness for consumable DRA devices |
| `DRADeviceBindingConditions` | `false` | Alpha | 1.34 | - | Tracks conditions for device binding states |
| `DRADeviceTaints` | `false` | Alpha | 1.33 | - | Enables taints for DRA device constraints |
| `DRAExtendedResource` | `false` | Alpha | 1.34 | - | Adds support for extended resource integration |
| `DRAPartitionableDevices` | `false` | Alpha | 1.33 | - | Enables partitionable device support |
| `DRAPrioritizedList` | `false` to `true` | Alpha to Beta | 1.33 | - | Adds prioritization support for DRA resource lists |
| `DRASchedulerFilterTimeout` | `false` | Alpha | 1.34 | - | Adds scheduler timeout filtering for DRA |
