# Configure database

Source: https://docs.coreweave.com/products/storage/cwdb/configure

# Configure database

> Field reference for the CWDBCluster resource: topology, compute, storage, and extensions

This page is the field reference for the `CWDBCluster` resource. Use it to tune topology, compute, storage, extensions, affinity, and the initial database name and owner.

For the creation workflow, see [Create a database](https://docs.coreweave.com/products/storage/cwdb/create.md). For day-2 actions like editing, resizing, and deleting a database, see [Manage database](https://docs.coreweave.com/products/storage/cwdb/manage.md). For the `CWDBBackup` field reference and the `spec.postgres.restore` field reference, see [Manage backups](https://docs.coreweave.com/products/storage/cwdb/backups.md).

> [!NOTE]
>
> By default, your CoreWeave Database (CWDB) only has password authentication. For the modes CWDB supports and how to configure clients, see [Authentication modes](https://docs.coreweave.com/products/storage/cwdb/connect.md#authentication-modes).

All CWDB resources live in the `data.coreweave.com/v1` API group and are namespaced.

## Minimal manifest

The following manifest sets only the fields the operator requires: the database type, the number of instances, and the storage size per instance:

```yaml theme={"system"}
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
```

This manifest omits `spec.resources`, so each instance gets the default compute described in [Compute](#compute). Every other configuration knob layers on top of this manifest.

## Topology

`spec.postgres.instances` controls how many PostgreSQL instances the operator runs. The operator places one primary and all replicas across distinct nodes through pod anti-affinity, assuming the CoreWeave Kubernetes Service (CKS) cluster has enough nodes to spread out on.

The following table describes the instances field:

| Field | Required | Description |
| - | - | - |
| `spec.postgres.instances` | Yes | Number of database instances. CoreWeave recommends `3` or more for production workloads (one primary plus two or more replicas). |

> [!WARNING]
>
> Choose three or more instances for production workloads.
>
> A single instance can't tolerate any disruption: maintenance, configuration changes, node failure, or a database crash result in a definitive outage.
>
> Two instances make quorum harder to establish and can cause availability issues under some failure modes.

For most workloads, 3 instances is the right balance of availability and cost. Scaling beyond 3 instances primarily adds read capacity, not durability. Set `spec.postgres.instances` to 5 or more when your workload is read-heavy and benefits from spreading reads across additional replicas.

## Compute

`spec.resources` sets the CPU and memory requests and limits for each instance in the database. The following example configures every instance with 2 CPU requested, 4 GiB of memory, and an 8 GiB memory limit:

```yaml theme={"system"}
spec:
  resources:
    requests:
      cpu: "2"
      memory: 4Gi
    limits:
      memory: 8Gi
```

`spec.resources` is optional. If you omit the entire `spec.resources` object, each instance requests 1 CPU and 1 GiB of memory, with a 2 GiB memory limit. If you set `spec.resources`, the operator uses it as written and doesn't fill in missing fields from these defaults.

The following table describes each `spec.resources` field:

| Field | Required | Description |
| - | - | - |
| `spec.resources.requests.cpu` | No | CPU request per instance, in standard Kubernetes units (for example, `"1"`, `"2"`). Must be at least `1`. |
| `spec.resources.requests.memory` | No | Memory request per instance (for example, `1Gi`, `4Gi`). Must be at least `1Gi`. |
| `spec.resources.limits.memory` | No | Memory limit per instance. Should comfortably exceed `requests.memory` to absorb query bursts. |

Replica scale-out (increasing or decreasing `spec.postgres.instances` after creation) is supported in limited availability. In-place vertical scaling (changing per-instance CPU or memory) hasn't been verified yet. To change per-instance compute, restore the database into a new one with the desired sizing. See [Manage database](https://docs.coreweave.com/products/storage/cwdb/manage.md) and [Manage backups](https://docs.coreweave.com/products/storage/cwdb/backups.md).

## Storage

`spec.storage` configures the per-instance persistent volume on DFS. The following example requests 50 GiB of storage for each instance:

```yaml theme={"system"}
spec:
  storage:
    resources:
      requests:
        storage: 50Gi
```

The following table describes the storage field:

| Field | Required | Description |
| - | - | - |
| `spec.storage.resources.requests.storage` | Yes | Storage size per instance, in standard Kubernetes quantity units (for example, `5Gi`, `100Gi`, `1Ti`). Can be increased after creation. |

A 3-instance database with `storage: 50Gi` provisions 150 GiB of DFS in total (each instance has its own replicated volume). Storage cost is billed as standard DFS usage. Start small and grow as data grows.

## Extensions

For a complete walkthrough, see [Use pgvector with CoreWeave Database](https://docs.coreweave.com/products/cks/tutorials/deploy-vector-databases-on-cks/pgvector.md).

`spec.postgres.extension` selects which curated PostgreSQL image the database runs and which extension the operator creates in the initial database. A database runs one extension at a time.

The following table describes the values `spec.postgres.extension.name` accepts:

| Value | Description |
| - | - |
| `postgresql` | Vanilla PostgreSQL with no extensions. This is the default. |
| `pgvector` | [pgvector](https://github.com/pgvector/pgvector), for storing embeddings and running approximate nearest-neighbor search. The operator creates the `vector` extension. |
| `pgduckdb` | [pg\_duckdb](https://github.com/duckdb/pg_duckdb), which embeds the DuckDB analytical engine in PostgreSQL. The operator creates the `pg_duckdb` extension and adds `pg_duckdb` to `shared_preload_libraries`. |

The following example enables pg\_duckdb:

```yaml theme={"system"}
spec:
  postgres:
    instances: 3
    extension:
      name: pgduckdb
```

The following table describes the extension fields:

| Field | Required | Description |
| - | - | - |
| `spec.postgres.extension.name` | No | Curated extension to enable. Supported values are `postgresql`, `pgvector`, and `pgduckdb`. Defaults to `postgresql`. |
| `spec.postgres.extension.majorVersion` | No | PostgreSQL major version. Supported values are `16`, `17`, and `18`. Defaults to `18`. |

`spec.postgres.extension.majorVersion` sets the PostgreSQL major version for every database, including databases that run vanilla PostgreSQL. It is the only field that sets the major version. The following example pins a pg\_duckdb database to PostgreSQL 17:

```yaml theme={"system"}
spec:
  postgres:
    instances: 3
    extension:
      name: pgduckdb
      majorVersion: 17
```

The operator creates the extension in the initial database, so no `CREATE EXTENSION` statement is needed there. In any other database you create yourself, run `CREATE EXTENSION vector;` or `CREATE EXTENSION pg_duckdb;` before using it. For pg\_duckdb query syntax and functions, see the [pg\_duckdb documentation](https://github.com/duckdb/pg_duckdb/tree/main/docs).

## Affinity overrides

`spec.affinity` overrides the default Kubernetes affinity rules for the database. By default, every database carries node-affinity rules that prefer CPU nodes and pod anti-affinity rules that spread instances across distinct nodes. The following example hard-requires CPU nodes rather than preferring them:

```yaml theme={"system"}
spec:
  affinity:
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
          - matchExpressions:
              - key: node.coreweave.cloud/class
                operator: In
                values: ["cpu"]
```

The following table describes the affinity field:

| Field | Required | Description |
| - | - | - |
| `spec.affinity` | No | Kubernetes affinity overrides. The operator applies CPU node-affinity and pod anti-affinity by default. Override only when necessary. |

> [!WARNING]
>
> Affinity overrides can prevent the operator from spreading instances across nodes, which weakens the failure model. Override only when necessary and validate that pods still land on distinct nodes by running `kubectl get pods -o wide -l cnpg.io/cluster=[CLUSTER-NAME]`.

## Database name and owner

`spec.postgres.dbName` and `spec.postgres.owner` set the initial database name and owner role. By default, CWDB creates a database named `app` with an owner role named `app`. The following example names the database `orders` and the owner role `orders_app`:

```yaml theme={"system"}
spec:
  postgres:
    instances: 3
    dbName: orders
    owner: orders_app
```

The following table describes both fields:

| Field | Required | Description |
| - | - | - |
| `spec.postgres.dbName` | No | Name of the initial database. Defaults to `app`. |
| `spec.postgres.owner` | No | Name of the owner role created for the initial database. Defaults to `app`. |

The operator creates two credentials Secrets per database, named after `dbName`: `[CLUSTER-NAME]-[DBNAME]-credentials` for read-write traffic and `[CLUSTER-NAME]-[DBNAME]-credentials-ro` for read-only traffic to replicas. For `dbName: orders`, those are `[CLUSTER-NAME]-orders-credentials` and `[CLUSTER-NAME]-orders-credentials-ro`. The defaults for `dbName: app` are `[CLUSTER-NAME]-app-credentials` and `[CLUSTER-NAME]-app-credentials-ro`.

A built-in `postgres` superuser role is always created alongside the owner role. The `postgres` role is reserved for break-glass access and database maintenance. Use the owner role for application traffic.

## Complete example

A 3-instance database sized for a moderate application workload, with a custom database name and `pgvector` enabled:

```yaml theme={"system"}
apiVersion: data.coreweave.com/v1
kind: CWDBCluster
metadata:
  name: my-db
spec:
  type: postgres
  postgres:
    instances: 3
    dbName: orders
    owner: orders_app
    extension:
      name: pgvector
  storage:
    resources:
      requests:
        storage: 50Gi
  resources:
    requests:
      cpu: "2"
      memory: 4Gi
    limits:
      memory: 8Gi
```

## Database status

The operator manages the `status` section of a `CWDBCluster`. To inspect it, run the following command from a terminal with `kubectl` access to your CKS cluster. Replace `[CLUSTER-NAME]` with the name of your `CWDBCluster` and `[NAMESPACE]` with the namespace it runs in:

```bash theme={"system"}
kubectl describe cwdbcluster [CLUSTER-NAME] --namespace [NAMESPACE]
```

The `status` section reports the following information:

| Status field | Description |
| - | - |
| `conditions` | `Ready`, `Provisioning`, and other lifecycle conditions. |
| `instances` | Per-instance status including role (primary or replica), pod name, and persistent volume. |

For the `CWDBBackup` field reference and the `spec.postgres.restore` field reference, see [Manage backups](https://docs.coreweave.com/products/storage/cwdb/backups.md).
