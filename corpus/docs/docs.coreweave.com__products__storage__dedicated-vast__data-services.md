# Data services

Source: https://docs.coreweave.com/products/storage/dedicated-vast/data-services

# Data services

> VAST Catalog, DataEngine, DataBase, Global Access, SyncEngine, and snapshot policies on Dedicated VAST clusters.

Dedicated VAST provides access to the full VAST data services stack. This page describes the services available on a Dedicated VAST cluster, including the metadata catalog, pipeline orchestration, embedded analytics, cross-cluster access, data mobility, and snapshot capabilities. Use this page to understand what each service does and where to find the upstream VAST documentation for configuration details.

## VAST Catalog

VAST Catalog is a built-in metadata index that automatically catalogs all files and objects on the cluster to enable search and query across the entire filesystem without external indexing tools.

VAST Catalog provides the following characteristics:

* **Automatic indexing**: Catalogs file and object metadata including creation time, size, ownership, S3 tags, and custom metadata.
* **SQL-queryable**: Query the catalog through VAST DataBase for search, filtering, and aggregation across billions of files and objects.
* **Always up to date**: Refreshed on a configurable schedule, as frequently as every 15 seconds, using VAST's snapshot engine.
* **No external infrastructure**: Runs entirely on the VAST cluster with no additional systems to deploy or manage.

Common use cases include the following:

* Using S3 object tags as an AI and ML feature store, embedding attributes directly on objects for retrieval by training pipelines.
* Capacity reporting across users, projects, and file types.
* Finding and managing data at scale across petabytes of storage.

For VAST Catalog configuration and query details, see the [VAST Cluster documentation](https://kb.vastdata.com/documentation/docs/vast-cluster).

## DataEngine

VAST DataEngine is a compute orchestration framework that lets you write, deploy, and manage execution pipelines directly on the VAST cluster. Pipelines run serverlessly on the cluster hardware, with no separate compute infrastructure to provision.

DataEngine provides the following capabilities:

* **Event-driven triggers**: Pipelines execute automatically in response to data events, such as file creation or modification.
* **Scheduled execution**: Pipelines run on configurable schedules for recurring batch operations.
* **Serverless execution**: Pipeline logic runs directly on the VAST cluster without managing additional infrastructure.

Use cases include automated data processing on ingest, event-driven AI and ML data pipelines, and scheduled batch operations across the filesystem.

For DataEngine capabilities and configuration details, see the [VAST DataEngine documentation](https://kb.vastdata.com/documentation/docs/vast-dataengine).

## DataBase

VAST DataBase is an embedded columnar analytics database that lets you run SQL queries directly against data stored on your VAST cluster. Queries execute on the VAST hardware itself, with no ETL pipeline, data movement, or separate analytics cluster required.

Common use cases include the following:

* Running analytics over training datasets stored on VAST without egress.
* Querying checkpoint metadata or experiment logs directly from storage.
* Joining structured data from object storage with file-based datasets.

DataBase is accessible through the SQL protocol using VAST Views.

For DataBase capabilities and query interface details, see the [VAST DataBase documentation](https://kb.vastdata.com/documentation/docs/administrators-guide-1).

## VAST Global Access and SyncEngine

### Global Access

VAST Global Access enables cross-cluster data access between VAST clusters, presenting data on remote clusters as a unified namespace. This supports active-active configurations where workloads on one cluster can access data residing on another without explicit data movement.

Built-in asynchronous replication between VAST clusters is a separate capability from Global Access and SyncEngine. For replication policy configuration, see the [VAST Administrator's Guide](https://kb.vastdata.com/documentation/docs/administrators-guide-1).

### SyncEngine

VAST SyncEngine is a universal data router and mobility platform. It discovers, catalogs, and moves data across hybrid storage environments.

SyncEngine provides the following capabilities:

* **Data migration and synchronization**: Move and synchronize data across storage systems with integrity verification.
* **Deep metadata indexing**: Catalog and index metadata across billions of unstructured files for discovery and search.
* **AI data preparation**: Prepare data for AI pipelines, including chunking, vectorization, and indexing for retrieval-augmented generation (RAG) workflows.

Global Access and SyncEngine require Dedicated VAST on both ends of the configuration.

For Global Access and SyncEngine configuration details, see the [VAST Administrator's Guide](https://kb.vastdata.com/documentation/docs/administrators-guide-1).

## Snapshots

Dedicated VAST supports customer-configurable snapshot policies, managed directly in VMS. Snapshots are point-in-time consistent copies of a View's filesystem state.

You can configure the following snapshot policy settings:

* **Schedule**: Snapshot frequency (for example, hourly, daily, weekly).
* **Retention**: How long the cluster retains snapshots before automatic deletion.
* **Scope**: Snapshots are scoped to a View.

Snapshots are accessible through the `.snapshot` directory within a mounted View, consistent with the behavior on CoreWeave's Distributed File Storage. Snapshots are read-only and do not consume additional capacity beyond the changed blocks since the previous snapshot.

Full snapshot policy management is available through VMS. For configuration details, see the [VAST Administrator's Guide](https://kb.vastdata.com/documentation/docs/administrators-guide-1).
