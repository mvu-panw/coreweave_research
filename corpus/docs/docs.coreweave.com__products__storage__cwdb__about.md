# About CoreWeave Database

Source: https://docs.coreweave.com/products/storage/cwdb/about

# About CoreWeave Database

> Architecture, topology, storage and backup model, observability, and shared responsibility for CWDB

CoreWeave Database (CWDB) is a Kubernetes-native, PostgreSQL-compatible database service. CWDB lives in your CoreWeave Kubernetes Service (CKS) cluster and runs on your compute, integrating closely with your workloads and providing low-latency access from inside the cluster.

This page explains CWDB's architecture, default topology, storage and backup model, connection and authentication options, observability integration, and shared responsibility boundaries.

## How CWDB runs

A `CWDBCluster` resource creates several Kubernetes objects in your namespace:

* **PostgreSQL pods**, one primary and one or more read replicas, scheduled on CPU nodes with anti-affinity so pods prefer to land on different hosts.
* **Persistent volumes** backed by Distributed File Storage (DFS). Each instance has its own volume that holds the live database.
* **Connection pooler pods** that sit in front of the database pods and route read-write and read-only traffic to the right instance.
* **Kubernetes Services** for both the pooler and the underlying database pods.
* **A credentials Secret** containing the database user, password, and several connection-string formats.

The CWDB operator manages day-2 lifecycle on these objects: rolling restarts, primary failover, patch upgrades, replication, and backup configuration.

> [!WARNING]
>
> Don't install the CloudNativePG operator in the same CKS cluster as CWDB. The CWDB operator conflicts with CloudNativePG and produces unpredictable behavior.

## Default topology

A CWDB cluster can run any number of instances. The default and recommended configuration for most workloads is **3 instances**: one primary and two replicas. The primary handles writes and read-write queries, while replicas handle read-only queries and provide automatic failover. Choose five or more instances only when you need additional read capacity. For availability tradeoffs and topology configuration, see [Topology](https://docs.coreweave.com/products/storage/cwdb/configure.md#topology).

Each instance maintains its own replicated copy of the database on a dedicated DFS volume. A 3-instance database sized for 50 GiB provisions three separate 50 GiB DFS volumes for a total of 150 GiB.

## Storage and backups

CWDB stores live data and backups on two separate CoreWeave storage services:

* **Live data** lives on DFS, attached to each instance as a Kubernetes persistent volume. You choose the initial size when you create the database, and you can increase it later.
* **Backups** stream continuously to CoreWeave-managed storage. You don't manage credentials, retention, or lifecycle policies for backup storage.
* **Encryption at rest** is provided by DFS for your active database and by a CoreWeave-managed key for your fully managed backups.

For details about backup cadence, retention, on-demand backups, and restoring, see [Manage backups](https://docs.coreweave.com/products/storage/cwdb/backups.md).

## Connections and authentication

CWDB enforces TLS for all client connections, manages server certificates and rotation, and supports password authentication by default. Applications connect through the pooler Services rather than directly to the database pods. For authentication modes, credential handling, and Service details, see [Connect to a database](https://docs.coreweave.com/products/storage/cwdb/connect.md).

## Observability

Every CWDB cluster is wired into CoreWeave's monitoring stack at creation. The operator emits metrics and logs, and CoreWeave provides a customer-facing alert for disk capacity.

### Alerts

CWDB sends a disk capacity alert through CoreWeave Alerts, which routes notifications to Slack channels, email addresses, or webhooks. The alert fires when disk usage on an instance approaches the volume's capacity.

### Metrics and logs

The CWDB operator emits Prometheus metrics for every database instance, including standard PostgreSQL metrics such as `pg_stat_database` and `pg_stat_replication`, and a CWDB-specific set covering backup pipeline health. Logs from the database pods and the operator are searchable through CoreWeave's logging stack.

## Shared responsibility

CWDB is built around a shared-responsibility model. The following summary applies in limited availability.

| Area | CoreWeave manages | You manage |
| - | - | - |
| Data plane | Provisioning, replication, failover, patch upgrades, automatic backups, restore primitives. | When to apply major upgrades, when to trigger on-demand backups, when to restore. |
| Storage | DFS for live data, managed storage for backups, encryption at rest. | Initial storage size and capacity headroom. Growing storage as data grows. |
| Networking | In-cluster Service endpoints and the pooler. | Ingress, bastion, or VPN paths from outside your CKS cluster. |
| Security | TLS termination between clients and the database server, server certificates. | Database-level roles, grants, application credential handling and rotation, network policies in your namespaces. |
| Observability | Default alerts, operator metrics. | Application-level dashboards, on-call routing, custom alert thresholds. |
