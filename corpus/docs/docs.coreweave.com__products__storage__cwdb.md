# CoreWeave Database

Source: https://docs.coreweave.com/products/storage/cwdb

# CoreWeave Database

> Managed, PostgreSQL-compatible database service that runs inside your CKS cluster

Now in limited availability, CoreWeave Database (CWDB) is a managed, PostgreSQL-compatible database service that runs inside a CoreWeave Kubernetes Service (CKS) cluster. CWDB uses CoreWeave Distributed File Storage (DFS) for the live database and CoreWeave-managed storage for backups. CoreWeave runs the database operator on your behalf, handles high availability, takes automatic backups, and surfaces monitoring.

You can create and manage a CoreWeave Database through the CoreWeave Cloud Console, directly in Kubernetes with `kubectl`, through GitOps tools like Argo CD or Flux, or by writing your own controllers against the Kubernetes API. For the underlying resource model and field reference, see [Configure database](https://docs.coreweave.com/products/storage/cwdb/configure.md).

## Request limited availability access

CWDB is enabled per CKS cluster through a feature flag managed by the CWDB team. To request enablement:

1. Contact CoreWeave through your customer Slack channel with your CKS cluster name and the namespace or namespaces you plan to use.
2. Wait for confirmation that the CWDB add-on is active on your CKS cluster.

To verify that you're enabled, list the CWDB Custom Resource Definitions (CRDs):

```bash theme={"system"}
kubectl get crd | grep coreweave.com
```

If enabled, you should see `cwdbclusters.data.coreweave.com` and `cwdbbackups.data.coreweave.com` listed in the output.

## Resources

CWDB exposes two Kubernetes custom resources:

> [card] [CWDBCluster](https://docs.coreweave.com/products/storage/cwdb/configure.md)
>
> A managed PostgreSQL database. Defines the topology (primary plus replicas), compute, storage, and access settings for one database. Restores from a backup are also configured on this resource, through `spec.postgres.restore`.

> [card] [CWDBBackup](https://docs.coreweave.com/products/storage/cwdb/backups.md)
>
> An on-demand backup of a database. Use it for known recovery points before risky operations.

## Get started

> [card] [About](https://docs.coreweave.com/products/storage/cwdb/about.md)
>
> Architecture, topology, observability, and the shared responsibility model.

> [card] [Create a database](https://docs.coreweave.com/products/storage/cwdb/create.md)
>
> Verify prerequisites and deploy your first database from the Cloud Console or with `kubectl`.

> [card] [Configure database](https://docs.coreweave.com/products/storage/cwdb/configure.md)
>
> Tune topology, compute, storage, database name, and extensions. Includes the full field reference for all CWDB resources.

> [card] [Manage database](https://docs.coreweave.com/products/storage/cwdb/manage.md)
>
> Edit a database, resize storage, or delete a database after creation.

> [card] [Connect to a database](https://docs.coreweave.com/products/storage/cwdb/connect.md)
>
> Extract connection strings and route traffic through the pooler Services.

> [card] [Manage backups](https://docs.coreweave.com/products/storage/cwdb/backups.md)
>
> How automatic backups work, how to take on-demand backups, and how to restore from a backup into a new database.

> [card] [Troubleshoot](https://docs.coreweave.com/products/storage/cwdb/troubleshooting.md)
>
> Common issues during limited availability and how to escalate.
