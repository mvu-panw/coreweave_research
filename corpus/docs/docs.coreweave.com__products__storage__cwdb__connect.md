# Connect to a database

Source: https://docs.coreweave.com/products/storage/cwdb/connect

# Connect to a database

> Find connection details, use the pooler Services, and authenticate to a CoreWeave Database

CoreWeave Database (CWDB) exposes a standard PostgreSQL endpoint. You connect using any PostgreSQL-compatible driver or tool. This page covers authentication modes, where to find the connection details, and which Service to point your application at.

## Authentication modes

In limited availability, CWDB supports password authentication only. The operator generates the application user's password when the database is created and exposes it through a Kubernetes Secret. Decode the Secret and supply the password to your client.

CWDB enforces TLS for all client connections to the database server. CoreWeave manages server certificates and rotation. You don't configure them. TLS terminates between the client and the database server. DFS, which backs the live database, is encrypted at rest but isn't encrypted in transit by default in limited availability.

The credentials Secrets described in the following section provide the password and connection details your client needs. To manage database-level roles, grants, and permissions, use standard PostgreSQL commands. See [Manage database roles and grants](#manage-database-roles-and-grants).

## Credentials Secrets

For each database, the operator creates two credentials Secrets, one for read-write traffic and one for read-only traffic against replicas:

* `[CLUSTER-NAME]-[DBNAME]-credentials`: read-write credentials for the database's owner role. By default `dbName` is `app`, so the default Secret is `[CLUSTER-NAME]-app-credentials`. If you set `spec.postgres.dbName: orders`, the Secret is `[CLUSTER-NAME]-orders-credentials`.
* `[CLUSTER-NAME]-[DBNAME]-credentials-ro`: read-only credentials that route to a read replica. This Secret automatically load-balances reads across replicas, so your application doesn't need to track how many replicas exist.

The operator doesn't create a separate Secret for the built-in `postgres` superuser. Break-glass access is granted by approving a Teleport session to a database `Pod` rather than through a Secret. If you need superuser access, contact the CWDB team through your customer Slack channel.

Each Secret carries the same connection information in several formats. The following table lists the most useful keys:

| Key | Format | Use for |
| - | - | - |
| `uri` | `postgresql://[USER]:[PASSWORD]@[HOST]:[PORT]/[DB]` | Most PostgreSQL clients and ORMs. |
| `jdbc-uri` | `jdbc:postgresql://[HOST]:[PORT]/[DB]?user=[USER]&password=[PASSWORD]` | JVM-based clients. |
| `pgpass` | A `.pgpass`-formatted line for the host. | `psql` and tools that read `.pgpass`. |
| `host` | The pooler Service DNS name. | Splitting connection details across config keys. |
| `port` | The TCP port (usually `5432`). | Splitting connection details across config keys. |
| `username` | The role name (for example, `app`). | Splitting connection details across config keys. |
| `password` | The role's password. | Splitting connection details across config keys. |
| `dbname` | The database name (for example, `app`). | Splitting connection details across config keys. |

Each value is base64-encoded in the Secret. Decode a key by piping `kubectl get secret` output through `base64 -d`:

```bash theme={"system"}
kubectl get secret [CLUSTER-NAME]-app-credentials \
  --namespace [NAMESPACE] \
  -o jsonpath='{.data.uri}' | base64 -d
```

Replace `[CLUSTER-NAME]` and `[NAMESPACE]` with your values.

## Use the pooler Services, not the database Services

CWDB exposes two layers of Kubernetes Services for every database:

* **Pooler Services**: backed by a connection pooler that fronts the database pods and reroutes traffic during primary failover.
  * `[CLUSTER-NAME]-pooler-rw`: read-write traffic.
  * `[CLUSTER-NAME]-pooler-ro`: read-only traffic.
* **Direct database Services**: point straight at the PostgreSQL pods.
  * `[CLUSTER-NAME]-rw`: direct read-write Service.
  * `[CLUSTER-NAME]-ro`: direct read-only Service.

> [!WARNING]
>
> Always connect production application traffic through the pooler Services. The pooler handles primary failover transparently and protects the database pods from connection storms. Reserve direct connections to `[CLUSTER-NAME]-rw` and `[CLUSTER-NAME]-ro` for ad hoc operations such as schema migrations or debugging.

The `uri` field in each credentials Secret already points at the matching pooler. The read-write Secret targets `[CLUSTER-NAME]-pooler-rw`. The read-only Secret targets `[CLUSTER-NAME]-pooler-ro`. When you assemble a connection string manually, use `[CLUSTER-NAME]-pooler-rw` for application writes and `[CLUSTER-NAME]-pooler-ro` for read-replica traffic.

## Connect from inside the CKS cluster

Applications in the same namespace as the database resolve the pooler Services using their short DNS names. For example, an application reading the `uri` Secret key gets a connection string of the form:

```text theme={"system"}
postgresql://app:[PASSWORD]@my-db-pooler-rw:5432/app
```

This works as-is from any pod in the same namespace.

Applications in a different namespace within the same CoreWeave Kubernetes Service (CKS) cluster should use the fully qualified name `[CLUSTER-NAME]-pooler-rw.[DB-NAMESPACE].svc.cluster.local`.

## Connect from a debug pod

For quick smoke tests, start a temporary pod with a PostgreSQL client and connect using the URI from the Secret:

```bash theme={"system"}
kubectl run shell \
  --namespace [NAMESPACE] \
  --rm -it --restart=Never \
  --image=debian:bookworm \
  -- bash
```

Inside the pod, install the PostgreSQL client and connect using the decoded connection URI from the credentials Secret:

```bash theme={"system"}
apt update && apt install -y postgresql-client
psql "$(kubectl get secret [CLUSTER-NAME]-app-credentials -o jsonpath='{.data.uri}' | base64 -d)"
```

The debug pod doesn't have `kubectl` by default. If you prefer, pull the URI to the pod through an environment variable when you launch the pod. Alternatively, copy and paste the decoded URI into `psql`.

## Connect from outside the CKS cluster

CWDB doesn't publish its endpoints to the public internet. Reach the database from outside the CKS cluster using the same ingress, bastion, or VPN pattern you use for other in-cluster services. For example, you might do one of the following:

* Port-forward the pooler Service to your laptop for one-off use: `kubectl port-forward svc/[CLUSTER-NAME]-pooler-rw 5432:5432 --namespace [NAMESPACE]`, then connect to `localhost:5432`.
* Deploy a bastion pod in the database's namespace and use SSH or `kubectl exec` to connect to it.
* Use your existing VPN solution to route traffic into the CKS cluster's pod network.

## Manage database roles and grants

The credentials Secrets give you the database's owner role for read-write and read-only access. To create additional roles, schemas, and grants, use standard PostgreSQL commands while connected as the owner role:

```sql theme={"system"}
CREATE ROLE reporting LOGIN PASSWORD '[PASSWORD]';
GRANT CONNECT ON DATABASE app TO reporting;
GRANT USAGE ON SCHEMA public TO reporting;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO reporting;
```

Treat the credentials Secrets as the source of truth for database access, and protect them with Kubernetes RBAC so only application service accounts can read them.

> [!NOTE]
>
> Anyone with `get` access on a credentials Secret can authenticate as the corresponding role. Anyone with the `exec` verb on the database `Pods` can open a local session as the `postgres` superuser. Tighten RBAC accordingly.
