# Persistent Volume Management Operator

Source: https://docs.coreweave.com/products/storage/distributed-file-storage/about-pvmo

# Persistent Volume Management Operator

> Learn about the Persistent Volume Management Operator (PVMO) for managing DFS volumes in CKS

## Persistent Volume Management Operator

CKS features a **Persistent Volume Management Operator (PVMO)**. PVMO is a Kubernetes controller manager that runs periodically to clean up orphaned volumes.

PVMO tracks PVC `delete` events through [admission webhooks](https://kubernetes.io/docs/reference/access-authn-authz/extensible-admission-controllers/#what-are-admission-webhooks). If it finds a `delete` event, it adds the label `pv-failsafe.coreweave.cloud/[DELETION-TIMESTAMP]` (where `[DELETION-TIMESTAMP]` is the current time) to the Persistent Volume to which the PVC was attached.

PVMO also adds a watcher service that periodically lists all Persistent Volumes in the cluster.

> [!NOTE]
>
> By default, the watcher lists all PVs in the cluster once per hour.

The watcher service checks for any "orphaned" PVs. A PV is considered orphaned if it has been released from its PVC and doesn't have the soft delete label described earlier. If the watcher finds an orphaned PV, it adds the soft delete label to it.

The watcher service also checks Persistent Volumes to see if they're eligible for deletion. To be eligible, a PV must have the soft delete label and must have exceeded the soft delete window.

> [!NOTE]
>
> The default soft delete window for PVs is 24 hours.

If both conditions are met, PVMO updates the reclaim policy on the PV from `Retain` to `Delete`. This update prompts CKS to reclaim the PV and delete all its underlying volumes.

For more information about creating a Distributed File Storage volume, see [Create Distributed File Storage volumes](https://docs.coreweave.com/products/storage/distributed-file-storage/create-volumes.md).
