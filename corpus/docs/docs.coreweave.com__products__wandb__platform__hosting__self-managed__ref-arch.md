# Reference architecture

Source: https://docs.coreweave.com/products/wandb/platform/hosting/self-managed/ref-arch

# Reference architecture

> Review self-managed Weights & Biases architecture covering Kubernetes, MySQL, object storage, and networking.

This page describes a reference architecture for a Weights & Biases deployment and outlines the recommended infrastructure and resources to support a production deployment of the platform. Use it as a planning guide to size, provision, and integrate the components required for a reliable Self-Managed installation.

This page is intended for platform engineers, site reliability engineers, and infrastructure administrators who deploy and operate Weights & Biases on their own infrastructure.

Depending on your chosen deployment environment for Weights & Biases, different services can help to enhance the resiliency of your deployment.

For instance, major cloud providers offer managed database services that help to reduce the complexity of database configuration, maintenance, high availability, and resilience.

This reference architecture addresses common deployment scenarios and shows how you can integrate your Weights & Biases deployment with cloud vendor services for performance and reliability.

## Before you start

Running any application in production comes with its own set of challenges, and Weights & Biases is no exception. Although Weights & Biases aims to streamline the process, complexities may arise depending on your architecture and design decisions. Typically, managing a production deployment involves overseeing components including hardware, operating systems, networking, storage, security, the Weights & Biases platform itself, and other dependencies. This responsibility extends to both the initial setup of the environment and its ongoing maintenance.

Consider carefully whether a Self-Managed approach with Weights & Biases is suitable for your team and your requirements.

A strong understanding of how to run and maintain production-grade application is an important prerequisite before you deploy Self-Managed Weights & Biases. If your team needs assistance, the CoreWeave Professional Services team and partners offer support for implementation and optimization.

To learn more about managed solutions for running Weights & Biases instead of managing it yourself, refer to [W\&B Multi-tenant Cloud](https://docs.coreweave.com/products/wandb/platform/hosting/hosting-options/multi_tenant_cloud.md) and [W\&B Dedicated Cloud](https://docs.coreweave.com/products/wandb/platform/hosting/hosting-options/dedicated-cloud.md).

## Infrastructure

A Weights & Biases deployment consists of an application layer and a storage layer. The following diagram shows how these layers fit together, and the subsections that follow describe each one.

![Weights & Biases infrastructure diagram](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/platform/_media/reference_architecture.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=832a4f347550db6c0d97872128fa6333)

### Application layer

The application layer consists of a multi-node Kubernetes cluster, with resilience against node failures. The Kubernetes cluster runs and maintains the Weights & Biases pods.

### Storage layer

The storage layer consists of a MySQL database and object storage. The MySQL database stores metadata and the object storage stores artifacts such as models and datasets.

## Infrastructure requirements

The following sections detail requirements for a Weights & Biases deployment, including Kubernetes cluster details, MySQL, Redis, object storage, software versions, networking, DNS, load balancer and ingress, SSL/TLS, and supported CPU architectures. Confirm that your environment meets each of these requirements before you begin a deployment.

### Kubernetes

Weights & Biases deploys the W\&B Server application as a [Kubernetes Operator](https://docs.coreweave.com/products/wandb/platform/hosting/self-managed/operator.md) that deploys multiple pods. For this reason, Weights & Biases requires a Kubernetes cluster with:

* A fully configured and functioning ingress controller.
* The capability to provision Persistent Volumes.

Weights & Biases supports deployment on [OpenShift Kubernetes clusters](https://www.redhat.com/en/technologies/cloud-computing/openshift) in cloud, on-premises, and air-gapped environments. For specific configuration instructions, see the [OpenShift section](https://docs.coreweave.com/products/wandb/platform/hosting/self-managed/operator.md#openshift-kubernetes-clusters) in the Operator guide.

### MySQL

MySQL 8.0.x reached end of life in April 2026. W\&B Self-Managed deployments must run a supported MySQL version that receives security patches and critical bug fixes. If you run community MySQL, install or upgrade to **MySQL 8.4.x**. If you use a managed service, run an engine version your provider documents as supported and patched (for example Amazon RDS for MySQL, Google Cloud SQL for MySQL, or Azure Database for MySQL). W\&B has validated the platform against MySQL 8.4.0 and current 8.4.x releases. If you are still on MySQL 8.0.x, plan an upgrade using the steps in [Upgrade MySQL to 8.4.x](https://docs.coreweave.com/products/wandb/platform/hosting/self-managed/operator.md#upgrade-mysql-to-84x).

Weights & Biases stores metadata in a MySQL database. The database's performance and storage requirements depend on the shapes of the model parameters and related metadata. For example, the database grows in size as you track more training runs, and load on the database increases based on queries in run tables, user workspaces, and reports.

**Weights & Biases strongly recommends using managed database services** (such as AWS RDS Aurora MySQL, Google Cloud SQL for MySQL, or Azure Database for MySQL) for production deployments. Managed services provide automated backups, monitoring, high availability, and patching, and reduce operational complexity. See the [Cloud provider instance recommendations](#cloud-provider-instance-recommendations) section for specific service recommendations.

If you choose to deploy a self-managed MySQL database, consider the following:

* **Backups**: Periodically back up the database to a separate facility. Weights & Biases recommends daily backups with at least 1 week of retention.
* **Performance**: The database requires fast storage hardware, such as SSD or accelerated NAS.
* **Monitoring**: The database requires adequate CPU resources. Monitor the database server's CPU load. If CPU usage is sustained at > 90% of the system for more than 5 minutes, consider adding CPU capacity.
* **Availability**: To meet your availability and durability requirements, Weights & Biases recommends configuring a hot standby deployment on a separate machine. The standby streams all updates in real time from the primary deployment and is ready to fail over if the primary server crashes, becomes corrupted, or experiences sustained downtime.

#### MySQL topology

For production, a managed MySQL service is the simplest path to high availability because the cloud provider handles failover, backups, and patching. Use the provider's high availability option, for example, Aurora Multi-AZ on AWS.

If you run self-managed MySQL, use a primary database with a hot standby that receives a real-time replication stream and can take over on failure. Weights & Biases doesn't support a multi-primary topology or read-only replicas for the application database.

#### MySQL database creation

For instructions to manually create the MySQL database and user, see the [bare-metal guide MySQL database section](https://docs.coreweave.com/products/wandb/platform/hosting/self-managed/operator.md#mysql-database).

#### MySQL configuration parameters

These parameters tune MySQL for the write patterns and schema changes that Weights & Biases performs at scale. If you're running your own MySQL instance, configure MySQL with these settings:

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

### Redis

Weights & Biases depends on a single-node Redis 7.x deployment that Weights & Biases components use for job queuing and data caching. For convenience during testing and development of proofs of concept, W\&B Self-Managed includes a local Redis deployment that isn't appropriate for production deployments.

Weights & Biases can connect to a Redis instance in the following environments:

* [AWS Elasticache](https://aws.amazon.com/elasticache/).
* [Google Cloud Memory Store](https://cloud.google.com/memorystore?hl=en).
* [Azure Cache for Redis](https://azure.microsoft.com/en-us/products/cache).
* Redis deployment hosted in your cloud or on-premises infrastructure.

### Object storage

Weights & Biases requires object storage with pre-signed URL and CORS support, deployed in one of:

* [CoreWeave AI Object Storage](https://docs.coreweave.com/products/storage/object-storage.md) is an S3-compatible object storage service optimized for AI workloads.
* [Amazon S3](https://aws.amazon.com/s3/) is an object storage service that provides scalability, data availability, security, and performance.
* [Google Cloud Storage](https://cloud.google.com/storage) is a managed service for storing unstructured data at scale.
* [Azure Blob Storage](https://azure.microsoft.com/en-us/products/storage/blobs) is a cloud-based object storage solution for storing unstructured data like text, binary data, images, videos, and logs.
* S3-compatible storage such as [MinIO Enterprise (AIStor)](https://www.min.io/product/aistor), [NetApp StorageGRID](https://www.netapp.com/data-storage/storagegrid/), or other enterprise-grade solutions hosted in your cloud or on-premises infrastructure.

### Versions

| Software | Minimum version |
| - | - |
| Kubernetes | v1.34 or newer ([Supported Kubernetes versions](https://kubernetes.io/releases/patch-releases/)) |
| Helm | v3.x |
| MySQL | W\&B Self-Managed deployments must run a supported MySQL version that receives security patches and critical bug fixes. Install or upgrade to **MySQL 8.4.x**, or use a managed service version that your provider documents as supported and patched. Aurora MySQL version strings differ from community MySQL versions. Use `SELECT version()` to see the full engine version string and `SELECT aurora_version()` to see the Aurora version. [Aurora MySQL version 3](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/AuroraMySQL.MySQL80.html) is compatible with MySQL 8.0.x and is still supported. See [Amazon Aurora versioning](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/Aurora.VersionPolicy.Versioning.html) and your cloud provider's documentation when you choose a target version. |
| Redis | v7.x |
| ClickHouse | Required for Weave on Self-Managed deployments. Not required if your deployment does not use Weave. See [ClickHouse compatibility for upgrades](https://docs.coreweave.com/products/wandb/platform/hosting/self-managed/operator.md#clickhouse-compatibility-for-upgrades) and [Supported W\&B Server releases](https://docs.coreweave.com/release-notes/server-releases.md). |

### Networking

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

The fully qualified domain name (FQDN) of the Weights & Biases deployment must resolve to the IP address of the ingress or load balancer using an `A` record.

### Load balancer and ingress

The W\&B Kubernetes Operator can expose services using a Kubernetes ingress controller, which routes to service endpoints based on URL paths with different ports. The ingress controller must be accessible by all machines that execute machine learning payloads or access the service through web browsers.

#### Ingress controller requirements

Your Kubernetes cluster must have an `IngressClass` available. Common ingress controller options include:

* [Nginx Ingress Controller](https://kubernetes.github.io/ingress-nginx/).
* [Istio](https://istio.io).
* [Traefik](https://traefik.io/).
* Cloud provider ingress controllers (AWS ALB, GCP Ingress, and Azure Application Gateway).

#### Weights & Biases service routing

The W\&B Operator routes requests automatically to multiple backend services based on path:

| Path | Service | Default port | Purpose |
| - | - | - | - |
| `/` | `wandb-app` | 8080 | Main web application UI |
| `/api` | `wandb-api` | 8081 | API service |
| `/graphql` | `wandb-api` | 8081 | GraphQL API endpoint |
| `/graphql2` | `wandb-api` | 8081 | GraphQL API v2 endpoint |
| `/console` | `wandb-console` | 8082 | System Console |
| `/traces` | `wandb-weave-trace` | 8722 | Weave tracing service (if enabled) |

#### Example ingress configuration

The following shows an example ingress resource created by the W\&B Operator:

```yaml theme={"system"}
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: wandb
  namespace: wandb
  annotations:
    nginx.ingress.kubernetes.io/proxy-body-size: "0"
spec:
  ingressClassName: nginx
  rules:
  - host: wandb.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: wandb-app
            port:
              number: 8080
      - path: /api
        pathType: Prefix
        backend:
          service:
            name: wandb-api
            port:
              number: 8081
      - path: /graphql
        pathType: Prefix
        backend:
          service:
            name: wandb-api
            port:
              number: 8081
      - path: /graphql2
        pathType: Prefix
        backend:
          service:
            name: wandb-api
            port:
              number: 8081
      - path: /console
        pathType: Prefix
        backend:
          service:
            name: wandb-console
            port:
              number: 8082
  tls:
  - hosts:
    - wandb.example.com
    secretName: wandb-tls
```

> [!NOTE]
>
> The W\&B Operator creates and manages the ingress configuration automatically. You typically don't need to create ingress resources manually. Make sure your cluster has a functioning ingress controller and the appropriate `IngressClass` configured.

### SSL/TLS

W\&B requires a valid signed SSL/TLS certificate for secure communication between clients and the server. SSL/TLS termination must occur on the ingress or load balancer. The W\&B Server application doesn't terminate SSL or TLS connections.

> [!WARNING]
>
> W\&B doesn't support self-signed certificates or custom CAs. Self-signed certificates cause challenges for users and aren't supported.

If possible, use a service like [Let's Encrypt](https://letsencrypt.org) to provide trusted certificates to your load balancer. Services like Caddy and Cloudflare manage SSL for you.

If your security policies require SSL communication within your trusted networks, consider using a tool like Istio and [sidecar containers](https://istio.io/latest/docs/reference/config/networking/sidecar/).

### Supported CPU architectures

Weights & Biases runs on Intel and AMD 64-bit architecture. ARM isn't supported.

## Deployment method

After your infrastructure meets the preceding requirements, choose how to install Weights & Biases and provision the underlying resources. The following sections describe the recommended deployment method and the recommended approach for infrastructure provisioning.

### W\&B Kubernetes Operator with Helm

The recommended installation method for W\&B Self-Managed uses the **W\&B Kubernetes Operator**, deployed through Helm. This approach provides:

* Automated updates and management of Weights & Biases components.
* Simplified configuration and deployment.
* Support for all deployment scenarios (cloud, on-premises, and air-gapped).

For detailed installation instructions, see:

* [Deploy W\&B Platform On-premises](https://docs.coreweave.com/products/wandb/platform/hosting/self-managed/operator.md) - Primary installation guide.
* [Kubernetes operator for air-gapped instances](https://docs.coreweave.com/products/wandb/platform/hosting/self-managed/on-premises-deployments/kubernetes-airgapped.md) - For disconnected environments.

### Infrastructure provisioning

Terraform is the recommended way to provision infrastructure for Weights & Biases production deployments. With Terraform, you define the required resources, their references to other resources, and their dependencies. Weights & Biases provides Terraform modules for the major cloud providers. For details, refer to [Deploy W\&B Server within Self-Managed cloud accounts](https://docs.coreweave.com/products/wandb/platform/hosting/hosting-options/self-managed.md#deploy-wb-server-within-Self-Managed-cloud-accounts).

## Sizing

Use the following guidelines as a starting point when planning a deployment. Weights & Biases recommends that you monitor all components of a deployment closely and that you make adjustments based on observed usage patterns. Continue to monitor production deployments over time and make adjustments as needed to maintain performance.

When you plan capacity, you size two core components: a Kubernetes cluster for the W\&B Operator workload and a MySQL database for metadata. Recommendations vary by **environment** (Test/Dev or Production) and, for Kubernetes only, by **product mix** (Models only, Weave only, or Models and Weave). Weights & Biases recommends starting with a minimum of 3 worker nodes for both Test/Dev and Production, and enabling cluster autoscaling in Production.

The following sections give per-node sizing recommendations for the Kubernetes cluster and the MySQL database.

### Kubernetes sizing

> [tab] Models only
>
> | Environment | CPU | Memory | Disk |
> | - | - | - | - |
> | Test/Dev | 2 cores | 16 GB | 100 GB |
> | Production | 8 cores | 64 GB | 100 GB |
>
> Numbers are per Kubernetes worker node.

> [tab] Weave only
>
> | Environment | CPU | Memory | Disk |
> | - | - | - | - |
> | Test/Dev | 4 cores | 32 GB | 100 GB |
> | Production | 12 cores | 96 GB | 100 GB |
>
> Numbers are per Kubernetes worker node.

> [tab] Models and Weave
>
> | Environment | CPU | Memory | Disk |
> | - | - | - | - |
> | Test/Dev | 4 cores | 32 GB | 100 GB |
> | Production | 16 cores | 128 GB | 100 GB |
>
> Numbers are per Kubernetes worker node.

### MySQL sizing

These recommendations don't vary by product mix. For topology and availability guidance, see [MySQL topology](#mysql-topology) under [MySQL](#mysql).

| Environment | CPU | Memory | Disk |
| - | - | - | - |
| Test/Dev | 2 cores | 16 GB | 100 GB |
| Production | 8 cores | 64 GB | 500 GB |

Numbers are per MySQL node.

#### MySQL sizing for run width

Database load also depends on *run width*, the number of distinct metrics that a single run logs at each step. For example, a run that logs 50,000 distinct metrics per step has a run width of 50K. Wide runs increase CPU load on the database, especially when the UI loads them in workspaces and reports.

If your teams log wide runs, size each MySQL node for the widest runs you expect:

| Run width (metrics per step) | CPU | Memory | Example AWS instance class |
| - | - | - | - |
| Up to 1K | 2 cores | 16 GB | `db.r6g.large` |
| Up to 25K | 4 cores | 32 GB | `db.r6g.xlarge` |
| Up to 50K | 8 cores | 64 GB | `db.r6g.2xlarge` |
| Up to 75K | 16 cores | 128 GB | `db.r6g.4xlarge` |
| Up to 100K | 32 cores | 256 GB | `db.r6g.8xlarge` |

The Production recommendation in the [MySQL sizing](#mysql-sizing) table supports run widths up to 50K.

## Cloud provider instance recommendations

After you determine the per-node CPU, memory, and disk requirements from the preceding sizing tables, use the following recommendations to pick specific cloud provider instance types and managed services that meet those requirements. These recommendations apply to each node of a Self-Managed deployment of Weights & Biases in cloud infrastructure.

> [tab] AWS
>
> **Recommended managed services**
>
> * **Kubernetes**: Amazon EKS
> * **MySQL**: Amazon RDS Aurora
> * **Object storage**: Amazon S3
>
> | Environment | K8s (Models only) | K8s (Weave only) | K8s (Models\&Weave) | MySQL |
> | - | - | - | - | - |
> | Test/Dev | r6i.large | r6i.xlarge | r6i.xlarge | db.r6g.large |
> | Production | r6i.2xlarge | r6i.4xlarge | r6i.4xlarge | db.r6g.2xlarge |

> [tab] Google Cloud
>
> **Recommended managed services**
>
> * **Kubernetes**: Google Kubernetes Engine (GKE)
> * **MySQL**: Google Cloud SQL for MySQL
> * **Object storage**: Google Cloud Storage (GCS)
>
> | Environment | K8s (Models only) | K8s (Weave only) | K8s (Models\&Weave) | MySQL |
> | - | - | - | - | - |
> | Test/Dev | n2-highmem-2 | n2-highmem-4 | n2-highmem-4 | db-n1-highmem-2 |
> | Production | n2-highmem-8 | n2-highmem-16 | n2-highmem-16 | db-n1-highmem-8 |

> [tab] Azure
>
> **Recommended managed services**
>
> * **Kubernetes**: Azure Kubernetes Service (AKS)
> * **MySQL**: Azure Database for MySQL
> * **Object storage**: Azure Blob Storage
>
> | Environment | K8s (Models only) | K8s (Weave only) | K8s (Models\&Weave) | MySQL |
> | - | - | - | - | - |
> | Test/Dev | Standard\_E2\_v5 | Standard\_E4\_v5 | Standard\_E4\_v5 | MO\_Standard\_E2ds\_v4 |
> | Production | Standard\_E8\_v5 | Standard\_E16\_v5 | Standard\_E16\_v5 | MO\_Standard\_E8ds\_v4 |
