# Manage database

Source: https://docs.coreweave.com/products/storage/cwdb/manage

# Manage database

> Edit, resize, scale, and delete a CoreWeave Database after creation

After you create your database, you can modify most configuration properties to ensure your database remains right-sized as your workload's demands change. This page covers each lifecycle action through both the Cloud Console and `kubectl`.

For configurable fields and their constraints, see [Configure database](https://docs.coreweave.com/products/storage/cwdb/configure.md). For backup-driven database replacement (the only way to change immutable fields like name or initial database name), see [Manage backups](https://docs.coreweave.com/products/storage/cwdb/backups.md).

Each row in the **Databases** list has a three-dot menu with the following actions:

* **View details** opens the database details panel on the **Details** tab.
* **Resize / scale** opens the **Edit database** form. See [Edit a database](#edit-a-database).
* **Manage backups** opens the database details panel on the **Backups** tab. See [Manage backups](https://docs.coreweave.com/products/storage/cwdb/backups.md#view-backups-from-the-cloud-console).
* **Delete** opens a confirmation dialog. See [Delete a database](#delete-a-database).

## Edit a database

You can edit a database after creation. The database name, namespace, initial database name, database engine, and compute cluster can't change.

Replica scale-out (increasing or decreasing `spec.postgres.instances`) is supported in limited availability. In-place vertical scaling (changing per-instance CPU or memory) hasn't been verified yet. To change per-instance compute, restore the database into a new one with the desired sizing. See [Manage backups](https://docs.coreweave.com/products/storage/cwdb/backups.md).

### Edit from the Cloud Console

To edit a database from the Cloud Console, follow these steps:

1. In the Cloud Console, open **Infrastructure > Data and storage** and select the **Databases** tab.
2. Click the database row to open the details view, then click **Edit configuration**. The row's three-dot menu **Resize / scale** action opens the same form.
3. The **Edit database** form opens with a YAML preview pane on the right. Immutable fields are shown but disabled.
4. Update the form fields, or edit the YAML pane directly. Changes in either pane sync to the other.
5. Click **Submit** to apply.

The database is updated with the new configuration.

### Edit with kubectl

Open the resource in your default editor. Replace `[CLUSTER-NAME]` with the name of your `CWDBCluster` and `[NAMESPACE]` with the namespace it runs in:

```bash theme={"system"}
kubectl edit cwdbcluster [CLUSTER-NAME] --namespace [NAMESPACE]
```

Alternatively, apply an updated manifest:

```bash theme={"system"}
kubectl apply -f cwdb_cluster.yaml --namespace [NAMESPACE]
```

The operator rejects changes to immutable fields.

## Resize a database

You can increase per-instance storage size after creation. See [Storage](https://docs.coreweave.com/products/storage/cwdb/configure.md#storage) and [Compute](https://docs.coreweave.com/products/storage/cwdb/configure.md#compute).

Resize uses the Edit form internally. For changes to fields other than storage size, see [Edit a database](#edit-a-database).

### Resize from the Cloud Console

To resize a database from the Cloud Console, follow these steps:

1. In the **Databases** list, open the database row's three-dot menu and select **Resize / scale**. The **Edit database** form opens.
2. In the **Resources** section, increase **Storage size (GiB)**.
3. Click **Submit**.

The new storage size is applied to each instance's Distributed File Storage (DFS) volume.

### Resize with kubectl

Increase `spec.storage.resources.requests.storage` on the database:

```bash theme={"system"}
kubectl edit cwdbcluster [CLUSTER-NAME] --namespace [NAMESPACE]
```

The new size is applied to each instance's DFS volume.

## Delete a database

When you delete a database, Kubernetes removes the database `Pods`, the pooler `Services`, the credentials `Secrets`, and the PersistentVolumeClaims (PVCs) for the per-instance DFS volumes. Deleting a PVC doesn't immediately delete the DFS volume behind it, so retained storage can outlive the database. On CKS, the DFS StorageClass retains a volume after its PVC is deleted, and the Persistent Volume Management Operator (PVMO) removes it after a soft-delete window, 24 hours by default. See [Volume deletion and data recovery](https://docs.coreweave.com/products/storage/distributed-file-storage/about.md#volume-deletion-and-data-recovery).

Treat deletion as irreversible.

> [!WARNING]
>
> Don't rely on retained volumes to recover a deleted database. Restores always create a new database. If you may need the data later, take an on-demand backup before deleting. See [Manage backups](https://docs.coreweave.com/products/storage/cwdb/backups.md).

### Delete from the Cloud Console

The Cloud Console provides two ways to delete a database:

* In the **Databases** list, open the database row's three-dot menu and select **Delete**.
* In the database's details view, scroll to **Danger zone** and click **Delete database**.

Both open a confirmation dialog before deletion.

### Delete with kubectl

To delete the database, remove the `cwdbcluster` resource:

```bash theme={"system"}
kubectl delete cwdbcluster [CLUSTER-NAME] --namespace [NAMESPACE]
```

Kubernetes removes the database `Pods`, the pooler `Services`, the credentials `Secrets`, and the PVCs for the per-instance DFS volumes. The underlying DFS volumes are retained and then removed as described in [Delete a database](#delete-a-database).
