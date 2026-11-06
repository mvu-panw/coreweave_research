# Create a database

Source: https://docs.coreweave.com/products/storage/cwdb/create

# Create a database

> Deploy a high-availability PostgreSQL database with the Cloud Console or kubectl

This page walks through deploying a 3-instance high-availability PostgreSQL database on CoreWeave Database (CWDB) using the Cloud Console or `kubectl`. Both creation methods produce the same `CWDBCluster` resource.

The defaults are a database named `app`, an application user named `app`, password authentication, and the default storage size on Distributed File Storage (DFS).

## Before you begin

CWDB must be enabled on your CKS cluster before you can create a database. If it isn't enabled yet, follow [Request limited availability access](https://docs.coreweave.com/products/storage/cwdb.md#request-limited-availability-access).

### Verify your CKS cluster

You need a working CKS cluster with at least one CPU node. CWDB instances run on CPU nodes by default. To confirm your cluster is reachable and has at least one CPU node available for scheduling, run the following commands:

```bash theme={"system"}
kubectl cluster-info
kubectl get nodes -o=custom-columns="NAME:metadata.name,CLASS:metadata.labels['node\.coreweave\.cloud\/class']"
```

You should see at least one node with `CLASS` set to `cpu`. If your cluster has no CPU nodes, request CPU capacity through your usual CKS workflow before proceeding.

### Local tooling

You need `kubectl` configured against the target CKS cluster. Optional but useful: `helm` for managing manifests through Helm charts, or a GitOps tool such as Argo CD or Flux.

### Choose a namespace

CWDB is a namespaced resource. CoreWeave recommends placing each database in the same namespace as the application that owns it, so the credentials Secret lives next to the workload that consumes it.

The following sections describe each creation method. Both result in a database named `my-db` running in the namespace you chose.

## Create from the Cloud Console

The Cloud Console **Data and storage > Databases** page provides a form-based workflow for creating and listing CoreWeave databases. Use it when you prefer a guided form over writing YAML by hand. The form composes a `CWDBCluster` manifest as you fill it in, and a live YAML preview alongside the form shows exactly what the Console submits.

You need Cloud Console access to your CoreWeave organization and permission to create resources in the target namespace.

1. In the Cloud Console, open **Infrastructure > Data and storage**.

2. Select the **Databases** tab, alongside **Object storage** and **File storage**.

3. Use the cluster selector at the top of the page to pick the CKS cluster that hosts the database. The dropdown lists running CKS clusters in your organization and shows each CKS cluster's zone (for example, `US-EAST-02A`).

   The page lists the existing CoreWeave databases in the selected CKS cluster, with columns for `Name`, `Namespace`, `Type`, `Age`, `Size`, and `Status`. Use the search field to filter by name, and the three-dot menu on each row for row-level actions.

4. Click **Create database** at the top right of the Databases page. The Console opens a form titled **Create database**, with a YAML preview pane on the right. Fields in the form update the YAML preview in real time. Use the toggle icon next to the preview to show or hide the pane.

   The form has four sections: **Basics**, **Availability**, **Resources**, and **Advanced**. Each section maps directly to fields on the `CWDBCluster` resource.

> [!NOTE]
>
> If the CKS cluster selector is empty or doesn't show the CKS cluster you expect, the CWDB add-on may not be enabled on that cluster. See [Request limited availability access](https://docs.coreweave.com/products/storage/cwdb.md#request-limited-availability-access).

### Basics

The Basics section sets the database identity and the initial Postgres database. Each field maps to a field on the `CWDBCluster` manifest:

| Form field | Default | Maps to |
| - | - | - |
| Compute cluster | The CKS cluster selected on the Databases page | Kubernetes context. No field on the manifest. |
| Instance name | `new-database` | `metadata.name` |
| Namespace | `default` | `metadata.namespace` |
| Database engine | `postgres` (read-only) | `spec.type` |
| Database name | `app` | `spec.postgres.dbName` |
| Owner | `app` | `spec.postgres.owner` |

To follow along with the rest of this page, set **Instance name** to `my-db` and **Namespace** to the namespace you chose in "Before you begin". Leave the other fields at their defaults.

**Compute cluster** is the CKS cluster that hosts the database. The dropdown shows running CKS clusters in your organization, with each option's zone visible. **Database engine** is the engine selector. Postgres is the only option in limited availability. **Database name** and **Owner** correspond to the initial Postgres database and its owner role. For the underlying semantics, see [Database name and owner](https://docs.coreweave.com/products/storage/cwdb/configure.md#database-name-and-owner).

### Availability

The Availability section sets how many Postgres instances the database runs:

| Form field | Default | Maps to |
| - | - | - |
| Instance count | `3` | `spec.postgres.instances` |

Use three or more instances for production workloads. Choose five or more instances when you need additional read capacity. For availability tradeoffs and supported topology options, see [Topology](https://docs.coreweave.com/products/storage/cwdb/configure.md#topology).

### Resources

The Resources section configures per-instance CPU, memory, and storage. The Console applies the same values to **each** instance in the database.

Pick a compute preset, or select **Custom** to enter your own values:

| Preset | vCPU | Memory | Suggested workloads |
| - | - | - | - |
| 2 vCPU, 8 GiB RAM | 2 | 8 GiB | Development and light workloads |
| 4 vCPU, 16 GiB RAM | 4 | 16 GiB | Production workloads |
| 8 vCPU, 32 GiB RAM | 8 | 32 GiB | High-performance workloads |
| Custom | Any | Any | Specific needs |

The Console shows a running total below the presets. For example, when you choose **8 vCPU, 32 GiB RAM** with 3 instances, the Console displays `3 × 8 vCPU, 32 GiB RAM = 24 vCPU, 96 GiB RAM total`. Each preset writes the chosen values to `spec.resources.requests.cpu` and `spec.resources.requests.memory`, and sets the memory limit (`spec.resources.limits.memory`) to twice the memory request. **Custom** lets you set the requests and limit independently.

Set **Storage size (GiB)** to the per-instance volume size. The valid range is 1 to 10,240 GiB, and the default is `50` GiB. A 3-instance database with **Storage size** set to `50` provisions 150 GiB of DFS in total (each instance gets its own replicated 50 GiB volume). Storage cost is billed as standard DFS usage.

> [!WARNING]
>
> You can increase storage size after creation, but you can't decrease it. Start small and grow as data grows. For more context, see [Storage](https://docs.coreweave.com/products/storage/cwdb/configure.md#storage).

### Advanced

The Advanced section exposes optional settings. In limited availability, the only setting here is **Backups**.

**Enable backups** is on by default. With the toggle on, the database is opted into CWDB managed backups: daily base backups retained for 7 days and continuous write-ahead log archiving, stored in CoreWeave-managed object storage. CoreWeave manages retention and storage location at the organization level.

Turning the toggle off sets `spec.postgres.disableManagedBackups: true` on the manifest, which opts the database out of managed backups. After the database is created, no daily base backups or WAL archives are produced, and you can't restore from a managed backup. CoreWeave recommends keeping backups enabled unless you're running a development or test workload or have an alternative backup strategy in place. For details, see [Manage backups](https://docs.coreweave.com/products/storage/cwdb/backups.md).

### Review the YAML preview

The pane on the right shows the manifest the Console submits. With **Instance name** set to `my-db`, the defaults for everything else, and the 8 vCPU compute preset, the preview looks like the following:

```yaml theme={"system"}
apiVersion: data.coreweave.com/v1
kind: CWDBCluster
metadata:
  name: my-db
  namespace: default
spec:
  type: postgres
  postgres:
    instances: 3
    dbName: app
    owner: app
  resources:
    requests:
      cpu: "8"
      memory: 32Gi
    limits:
      memory: 64Gi
  storage:
    resources:
      requests:
        storage: 50Gi
```

This manifest is equivalent to applying the same YAML with `kubectl` in the target namespace. The YAML pane is editable: changes you make in the pane flow back into the form, and changes in the form update the pane in real time. If the YAML is invalid, the Console shows a `Your manifest has N error(s)` message, where `N` is the number of detected problems. Fix the errors before submitting.

### Submit

To apply the manifest, click **Submit**. To clear the form and start over, click **Reset**.

After submission, the Console returns to the Databases list. The new row appears with a `Status` of `Provisioning` while the CWDB operator schedules Pods, provisions DFS volumes, and brings up the database. The row transitions to `Ready` when the database is healthy. If the row stays in `Provisioning` for longer than a few minutes, see [Troubleshoot](https://docs.coreweave.com/products/storage/cwdb/troubleshooting.md#database-never-becomes-ready).

## Create with kubectl

Use `kubectl` when you want to version-control the manifest, manage CoreWeave databases through GitOps, or work without the Console.

> [!WARNING]
>
> If you apply a `CWDBCluster` manifest without specifying a namespace, the resource is created in the `default` namespace. Always include `--namespace [NAMESPACE]` (or set `metadata.namespace` in your manifest) to avoid this.

Save the following manifest as `cwdb_cluster.yaml`. This minimal example uses a small footprint suitable for evaluation. For production-sized defaults closer to what the Console form proposes, see [Configure database](https://docs.coreweave.com/products/storage/cwdb/configure.md).

```yaml title="cwdb_cluster.yaml" theme={"system"}
apiVersion: data.coreweave.com/v1
kind: CWDBCluster
metadata:
  name: my-db
spec:
  type: postgres
  postgres:
    instances: 3
  storage:
    resources:
      requests:
        storage: 5Gi
  resources:
    requests:
      memory: 1Gi
      cpu: "1"
    limits:
      memory: 2Gi
```

This manifest declares a Postgres database with 3 instances (one primary, two replicas), 5 GiB of DFS storage per instance, and 1 CPU and 1 to 2 GiB of memory per instance. For a deeper explanation of every field, see [Configure database](https://docs.coreweave.com/products/storage/cwdb/configure.md).

To create the database in your target namespace, apply the manifest. Replace `[NAMESPACE]` with the namespace you chose in "Before you begin":

```bash theme={"system"}
kubectl apply -f cwdb_cluster.yaml --namespace [NAMESPACE]
```

## Wait for the database to be ready

The CWDB operator provisions Pods, volumes, and Services in the background. Wait for the database to report `Ready`:

```bash theme={"system"}
kubectl wait --for=condition=Ready cwdbcluster my-db \
  --namespace [NAMESPACE] \
  --timeout=300s
```

You should see output similar to the following:

```text title="Example output" theme={"system"}
cwdbcluster.data.coreweave.com/my-db condition met
```

If you created the database from the Cloud Console, you can also watch the row's **Status** transition from `Provisioning` to `Ready` on the Databases list. If the wait command times out, or the row stays in `Provisioning` for longer than a few minutes, see [Troubleshoot](https://docs.coreweave.com/products/storage/cwdb/troubleshooting.md).

List the resources the operator created:

```bash theme={"system"}
kubectl get pods,svc,pvc --namespace [NAMESPACE] -l cnpg.io/cluster=my-db
```

You should see three Pods, the pooler Services (`my-db-pooler-rw` and `my-db-pooler-ro`), the direct database Services (`my-db-rw` and `my-db-ro`), and three persistent volume claims.

## Next steps

* [Connect to a database](https://docs.coreweave.com/products/storage/cwdb/connect.md) to retrieve credentials and run your first query.
* [Configure database](https://docs.coreweave.com/products/storage/cwdb/configure.md) to tune topology, compute, storage, and extensions.
* [Manage backups](https://docs.coreweave.com/products/storage/cwdb/backups.md) to learn how automatic backups work and how to restore.
* [About](https://docs.coreweave.com/products/storage/cwdb/about.md#observability) to review CWDB observability, alerts, and metrics.
