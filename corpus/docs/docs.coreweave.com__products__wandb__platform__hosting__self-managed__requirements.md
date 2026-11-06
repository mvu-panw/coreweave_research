# Self-Managed infrastructure requirements

Source: https://docs.coreweave.com/products/wandb/platform/hosting/self-managed/requirements

# Self-Managed infrastructure requirements

> Infrastructure and software requirements for W&B Self-Managed deployments

This page describes the infrastructure and software requirements for deploying W\&B Self-Managed. It's intended for platform and infrastructure engineers planning a Self-Managed installation. Review these requirements before you begin your deployment to confirm that your environment can support W\&B Server.

> [!NOTE]
>
> Weights & Biases recommends fully managed deployment options such as [W\&B Multi-tenant Cloud](https://docs.coreweave.com/products/wandb/platform/hosting/hosting-options/multi_tenant_cloud.md) or [W\&B Dedicated Cloud](https://docs.coreweave.com/products/wandb/platform/hosting/hosting-options/dedicated-cloud.md) deployment types. Weights & Biases fully managed services are straightforward and secure to use, and require minimal to no configuration.

For complete architectural guidance, see the [reference architecture](https://docs.coreweave.com/products/wandb/platform/hosting/self-managed/ref-arch.md).

## Software version requirements

| Software | Minimum version |
| - | - |
| Kubernetes | v1.34 or newer ([Supported Kubernetes versions](https://kubernetes.io/releases/patch-releases/)) |
| Helm | v3.x |
| MySQL | W\&B Self-Managed deployments must run a supported MySQL version that receives security patches and critical bug fixes. Install or upgrade to **MySQL 8.4.x**, or use a managed service version that your provider documents as supported and patched. Aurora MySQL version strings differ from community MySQL versions. Use `SELECT version()` to see the full engine version string and `SELECT aurora_version()` to see the Aurora version. [Aurora MySQL version 3](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/AuroraMySQL.MySQL80.html) is compatible with MySQL 8.0.x and is still supported. See [Amazon Aurora versioning](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/Aurora.VersionPolicy.Versioning.html) and your cloud provider's documentation when you choose a target version. |
| Redis | v7.x |
| ClickHouse | Required for Weave on Self-Managed deployments. Not required if your deployment does not use Weave. See [ClickHouse compatibility for upgrades](https://docs.coreweave.com/products/wandb/platform/hosting/self-managed/operator.md#clickhouse-compatibility-for-upgrades) and [Supported W\&B Server releases](https://docs.coreweave.com/release-notes/server-releases.md). |

## Hardware requirements

**CPU Architecture**: W\&B runs on Intel (x86) CPU architecture only. ARM is not supported.

**Sizing**: For CPU, memory, and disk sizing recommendations for Kubernetes nodes and MySQL, see the [Sizing section](https://docs.coreweave.com/products/wandb/platform/hosting/self-managed/ref-arch.md#sizing) in the reference architecture. Requirements vary based on whether you're running Models, Weave, or both.

For detailed sizing recommendations based on your use case (Models only, Weave only, or both), see the [reference architecture sizing section](https://docs.coreweave.com/products/wandb/platform/hosting/self-managed/ref-arch.md#sizing).

## Kubernetes

W\&B Server is deployed as a [Kubernetes Operator](https://docs.coreweave.com/products/wandb/platform/hosting/self-managed/operator.md) that manages multiple pods. Your Kubernetes cluster must meet the following requirements:

* **Version**: See the preceding [Software version requirements](#software-version-requirements) section.
* **Ingress controller**: A fully configured and functioning ingress controller (Nginx, Istio, Traefik, or cloud provider ingress).
* **Persistent volumes**: Capability to provision persistent volumes.
* **CPU architecture**: Intel or AMD 64-bit (ARM is not supported).

Weights & Biases supports deployment on [OpenShift Kubernetes clusters](https://www.redhat.com/en/technologies/cloud-computing/openshift) in cloud, on-premises, and air-gapped environments. For specific configuration instructions, see the [OpenShift section](https://docs.coreweave.com/products/wandb/platform/hosting/self-managed/operator.md#openshift-kubernetes-clusters) in the Operator guide.

For complete Kubernetes requirements, including load balancer and ingress configuration, see the [reference architecture Kubernetes section](https://docs.coreweave.com/products/wandb/platform/hosting/self-managed/ref-arch.md#kubernetes).

## MySQL database

MySQL 8.0.x reached end of life in April 2026. W\&B Self-Managed deployments must run a supported MySQL version that receives security patches and critical bug fixes. If you run community MySQL, install or upgrade to **MySQL 8.4.x**. If you use a managed service, run an engine version your provider documents as supported and patched (for example Amazon RDS for MySQL, Google Cloud SQL for MySQL, or Azure Database for MySQL). W\&B has validated the platform against MySQL 8.4.0 and current 8.4.x releases. If you are still on MySQL 8.0.x, plan an upgrade using the steps in [Upgrade MySQL to 8.4.x](https://docs.coreweave.com/products/wandb/platform/hosting/self-managed/operator.md#upgrade-mysql-to-84x).

W\&B requires an external MySQL database.

For production, W\&B recommends using managed database services:

* [AWS RDS Aurora MySQL](https://aws.amazon.com/rds/aurora/)
* [Google Cloud SQL for MySQL](https://cloud.google.com/sql/mysql)
* [Azure Database for MySQL](https://azure.microsoft.com/en-us/products/mysql/)

Managed database services provide automated backups, monitoring, high availability, patching, and reduce operational overhead.

See the [reference architecture](https://docs.coreweave.com/products/wandb/platform/hosting/self-managed/ref-arch.md#mysql) for MySQL requirements, including sizing recommendations and configuration parameters. For the SQL to create the database, see the [bare-metal guide](https://docs.coreweave.com/products/wandb/platform/hosting/self-managed/operator.md#mysql-database). For questions about your deployment's database configuration, contact [support](mailto:forge-support@coreweave.com) or your AISE.

Weights & Biases recommends using managed database services such as AWS RDS Aurora MySQL, Google Cloud SQL for MySQL, or Azure Database for MySQL for production deployments. Managed services provide automated backups, monitoring, high availability, and patching, and they reduce operational complexity.

### MySQL configuration parameters

If you're running your own MySQL instance, configure MySQL with the following settings for compatibility with W\&B Server:

```ini theme={"system"}
binlog_format = 'ROW'
binlog_row_image = 'MINIMAL'
innodb_flush_log_at_trx_commit = 1
innodb_online_alter_log_max_size = 268435456
max_prepared_stmt_count = 1048576
sort_buffer_size = '67108864'
sync_binlog = 1
```

Weights & Biases has validated these settings for performance and reliability.

### Database creation

If you aren't using a managed MySQL service that provisions the database automatically, follow these instructions to manually create the MySQL database and user that W\&B Server uses:

Create a database and a user with the following SQL commands. Replace `[PASSWORD]` with a secure password:

```sql theme={"system"}
CREATE USER 'wandb_local'@'%' IDENTIFIED BY '[PASSWORD]';
CREATE DATABASE wandb_local CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
GRANT ALL ON wandb_local.* TO 'wandb_local'@'%' WITH GRANT OPTION;
```

For additional considerations, including backups, performance, monitoring, and availability, see the [reference architecture MySQL section](https://docs.coreweave.com/products/wandb/platform/hosting/self-managed/ref-arch.md#mysql).

## Redis

W\&B Server uses Redis for caching and background job coordination.

W\&B depends on a single-node Redis 7.x deployment, which W\&B's components use for job queuing and data caching. For testing and proof-of-concept work, W\&B Self-Managed includes a local Redis deployment. This bundled deployment isn't appropriate for production use.

For production deployments, W\&B can connect to a Redis instance in the following environments:

* [Amazon ElastiCache](https://aws.amazon.com/elasticache/)
* [Google Cloud Memorystore](https://cloud.google.com/memorystore?hl=en)
* [Azure Cache for Redis](https://azure.microsoft.com/en-us/products/cache)
* Self-hosted Redis in your cloud or on-premises infrastructure

Weights & Biases can connect to a Redis instance in any of the following environments:

* [AWS Elasticache](https://aws.amazon.com/pm/elasticache/).
* [Google Cloud Memory Store](https://cloud.google.com/memorystore?hl=en).
* [Azure Cache for Redis](https://azure.microsoft.com/en-us/products/cache).
* Redis deployment hosted in your cloud or on-premises infrastructure.

## ClickHouse

W\&B Weave on Self-Managed deployments uses ClickHouse. ClickHouse is not required for every Self-Managed installation.

Before you upgrade W\&B Server or change your ClickHouse version, see [ClickHouse compatibility for upgrades](https://docs.coreweave.com/products/wandb/platform/hosting/self-managed/operator.md#clickhouse-compatibility-for-upgrades) in the Operator guide and the compatibility notes in [Supported W\&B Server releases](https://docs.coreweave.com/release-notes/server-releases.md).

For deployment procedures, see [Deploy Weave in a self-managed environment](https://docs.coreweave.com/products/wandb/weave/guides/platform/weave-self-managed.md).

## Object storage

W\&B Server requires an object storage bucket to store artifacts, media, and run data.

W\&B requires object storage with pre-signed URL and CORS support.

W\&B recommends the following storage providers:

* [Amazon S3](https://aws.amazon.com/s3/): Object storage service offering scalability, data availability, security, and performance.
* [Google Cloud Storage](https://cloud.google.com/storage): Managed service for storing unstructured data at scale.
* [Azure Blob Storage](https://azure.microsoft.com/en-us/products/storage/blobs): Cloud-based object storage for unstructured data at scale.
* [CoreWeave AI Object Storage](https://docs.coreweave.com/products/storage/object-storage.md): S3-compatible object storage optimized for AI workloads.
* Enterprise S3-compatible storage such as [MinIO Enterprise (AIStor)](https://www.min.io/product/aistor), [NetApp StorageGRID](https://www.netapp.com/data-storage/storagegrid/), or other enterprise solutions.

> [!NOTE]
>
> MinIO Open Source is in [maintenance mode](https://github.com/minio/minio) with no active development or pre-compiled binaries. For production deployments, W\&B recommends managed object storage services or enterprise S3-compatible solutions such as MinIO Enterprise (AIStor).

After you select a provider, configure the bucket so that W\&B can access it. For detailed bucket provisioning instructions including IAM policies, CORS configuration, and access setup, see the [Bring Your Own Bucket (BYOB) guide](https://docs.coreweave.com/products/wandb/platform/hosting/data-security/secure-storage-connector.md).

For the complete list of object storage requirements, including capacity and performance guidance, see the [reference architecture object storage section](https://docs.coreweave.com/products/wandb/platform/hosting/self-managed/ref-arch.md#object-storage).

### Provision your storage bucket

Before configuring W\&B, you must provision your object storage bucket with the required IAM policies, CORS configuration, and access credentials.

See the [Bring Your Own Bucket (BYOB) guide](https://docs.coreweave.com/products/wandb/platform/hosting/data-security/secure-storage-connector.md) for detailed step-by-step provisioning instructions for:

* Amazon S3 (including IAM policies and bucket policies)
* Google Cloud Storage (including PubSub notifications)
* Azure Blob Storage (including managed identities)
* CoreWeave AI Object Storage
* S3-compatible storage (MinIO Enterprise, NetApp StorageGRID, and other enterprise solutions)

### Configure Weights & Biases to use your bucket

After you provision your bucket, you must configure Weights & Biases to use it through the Operator's Helm values so that W\&B Server can read from and write to the bucket. See the [Operator object storage configuration section](https://docs.coreweave.com/products/wandb/platform/hosting/self-managed/operator.md#object-storage-bucket) for details.

## Networking

Networking configuration exposes W\&B Server to users and machine-learning workloads. The following sections describe DNS, load balancer, and ingress requirements.

For a networked deployment, allow egress to these endpoints during both installation and runtime:

* `https://deploy.wandb.ai`
* `https://charts.wandb.ai`
* `https://quay.io` (used for Prometheus images)

> [!NOTE]
>
> Additional container registries might be required depending on your deployment configuration:
>
> * `https://gcr.io` when you deploy Bufstream and etcd for Weave online evaluations.

To learn about air-gapped deployments, refer to [Kubernetes operator for air-gapped instances](https://docs.coreweave.com/products/wandb/platform/hosting/self-managed/on-premises-deployments/kubernetes-airgapped.md).

Grant the training infrastructure and each experiment tracking system access to W\&B and the object storage.

### DNS

The fully qualified domain name (FQDN) of the Weights & Biases deployment must resolve to the IP address of the ingress or load balancer using an A record.

### Load balancer and ingress

The W\&B Kubernetes Operator exposes services using a Kubernetes ingress controller, which routes to service endpoints based on URL paths. The ingress controller must be accessible by all machines that execute machine-learning payloads or access the service through web browsers.

For detailed load balancer options, ingress controller requirements, and configuration examples, see the [reference architecture load balancer section](https://docs.coreweave.com/products/wandb/platform/hosting/self-managed/ref-arch.md#load-balancer-and-ingress).

## SSL/TLS

W\&B requires a valid signed SSL/TLS certificate for secure communication between clients and the server. SSL/TLS termination must occur on the ingress or load balancer. The W\&B Server application doesn't terminate SSL or TLS connections.

> [!WARNING]
>
> W\&B doesn't support self-signed certificates or custom CAs. Self-signed certificates cause challenges for users and aren't supported.

If possible, use a service like [Let's Encrypt](https://letsencrypt.org) to provide trusted certificates to your load balancer. Services like Caddy and Cloudflare manage SSL for you.

If your security policies require SSL communication within your trusted networks, consider using a tool like Istio and [sidecar containers](https://istio.io/latest/docs/reference/config/networking/sidecar/).

## License

All Self-Managed deployments require a valid W\&B Server license. Without a license, W\&B Server can't start.

You need a license to deploy Weights & Biases Self-Managed. To obtain an evaluation or production license, see [Obtain an Enterprise license](https://docs.coreweave.com/products/wandb/platform/hosting/enterprise-licenses.md#obtain-an-enterprise-license) and select the **Self-Managed** tab.

To manage your deployment's licenses, sign in to the [deployment manager](https://deploy.wandb.ai/).

## Next steps

After you confirm that your infrastructure meets these requirements, proceed to the deployment guide that matches your environment:

* **Cloud and on-premises deployments**: See [Deploy Weights & Biases with Kubernetes Operator](https://docs.coreweave.com/products/wandb/platform/hosting/self-managed/operator.md) for Helm and Terraform deployment options.
* **Air-gapped deployments**: See [Deploy on Air-Gapped Kubernetes](https://docs.coreweave.com/products/wandb/platform/hosting/self-managed/on-premises-deployments/kubernetes-airgapped.md) for disconnected environments.
* **All deployment methods**: See [Deploy with Kubernetes Operator](https://docs.coreweave.com/products/wandb/platform/hosting/self-managed/operator.md) for the core operator deployment guide.
