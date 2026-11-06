# Configure storage mounts on SUNK Self-Service

Source: https://docs.coreweave.com/products/sunk/manage_sunk/configure-storage-mounts

# Configure storage mounts on SUNK Self-Service

> Size the home directory and add shared storage mounts on a SUNK Self-Service cluster through spec.storage

[SUNK Self-Service](https://docs.coreweave.com/products/sunk/about-self-service-sunk.md)

A SUNK Self-Service cluster provisions shared storage for you from the `spec.storage` field of the `SunkCluster` resource. You define a home directory and any additional mounts by path and size, and the operator creates the underlying storage and mounts it on every login and compute node. This page shows how to size the home directory, add extra mounts, and change storage after the cluster is running.

This is the SUNK-managed storage path. To mount PVCs that you manage yourself, see [Share storage across Slurm nodes on SUNK Standard](https://docs.coreweave.com/products/sunk/manage_sunk/shared-storage.md). For the full storage configuration reference, including field definitions, see the [`SunkCluster` reference](https://docs.coreweave.com/products/sunk/reference/sunkcluster-reference#storageconfig).

## How managed storage works

Each entry in `spec.storage` becomes one shared volume that the operator provisions as a `ReadWriteMany` PVC and mounts at the path you specify. Because the volumes are `ReadWriteMany`, every login and compute node in the cluster mounts the same storage at the same path, so a file written from one node is visible on all of them.

The managed volumes belong to the cluster: each PVC is owned by the `SunkCluster` resource. Data persists across pod restarts and node replacement, but deleting the `SunkCluster` also deletes its managed storage. Persist anything you need to keep outside the cluster before you delete it.

## Size the home directory

The `spec.storage.homeDir` field sets the shared home directory. If you omit it, the cluster provisions a `2Ti` volume mounted at `/mnt/home`. To use a different size or path, set the field explicitly:

```yaml theme={"system"}
spec:
  storage:
    homeDir:
      path: /mnt/home
      size: 4Ti
```

When you set `homeDir`, both `path` and `size` are required. The `size` is a [Kubernetes quantity](https://kubernetes.io/docs/reference/kubernetes-api/common-definitions/quantity/), such as `2Ti` or `500Gi`.

## Add additional mounts

Use `spec.storage.additionalMounts` to provision shared storage beyond the home directory, such as a volume for datasets or job output. Each entry is a path and a size:

```yaml theme={"system"}
spec:
  storage:
    homeDir:
      path: /mnt/home
      size: 2Ti
    additionalMounts:
      - path: /mnt/data
        size: 10Ti
      - path: /mnt/scratch
        size: 5Ti
```

Each mount becomes its own `ReadWriteMany` volume available at its path on every node. Mount paths must be unique within the cluster.

## Change storage after creation

To change storage on a running cluster, edit `spec.storage` and reapply the `SunkCluster`. The operator reconciles the difference, but the safe changes are limited, and some changes delete data. The following table summarizes what each kind of change does.

| Change | Result |
| - | - |
| Add an entry to `additionalMounts` | Safe. The operator provisions a new volume at the new path. |
| Increase a `size` | The operator requests a volume expansion. This succeeds only if the underlying storage class allows expansion. |
| Decrease a `size` | Not supported. Kubernetes does not allow shrinking a volume, and the change is rejected. |
| Change a `path` | Destructive. The operator treats the new path as a new volume and removes the old one, which deletes the data stored at the old path. |
| Remove an entry from `additionalMounts` | Destructive. The operator deletes the volume for that path, which deletes its data. |

> [!WARNING]
>
> Because the operator identifies a managed volume by its path, a path that is no longer in `spec.storage` is removed. If you change a mount `path` or remove a mount, the underlying volume and its data are destroyed. Treat paths as fixed after creation, and back up any data you need before removing a mount.

In practice, treat `additionalMounts` as additive and treat `size` as growable but not shrinkable. To reorganize storage without losing data, add the new mount, copy the data across from a login node, and only then remove the old mount.

## Next steps

* [`SunkCluster` reference](https://docs.coreweave.com/products/sunk/reference/sunkcluster-reference#storageconfig) for the `StorageConfig` and `VolumeSpec` field definitions.
* [Share storage across Slurm nodes on SUNK Standard](https://docs.coreweave.com/products/sunk/manage_sunk/shared-storage.md) to mount PVCs you provision yourself.
* [Create a SUNK Self-Service cluster](https://docs.coreweave.com/products/sunk/deploy_sunk/create-sunk-cluster.md) for the full cluster creation flow.
