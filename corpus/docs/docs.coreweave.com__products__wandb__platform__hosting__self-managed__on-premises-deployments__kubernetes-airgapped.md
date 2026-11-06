# Deploy on Air-Gapped Kubernetes

Source: https://docs.coreweave.com/products/wandb/platform/hosting/self-managed/on-premises-deployments/kubernetes-airgapped

> Deploy W&B Platform in air-gapped and disconnected Kubernetes environments

# Deploy on Air-Gapped Kubernetes

## Introduction

This guide provides step-by-step instructions to deploy the W\&B Platform in air-gapped, disconnected, or restricted network customer-managed environments. By following this guide, you set up an internal container registry and Helm repository to host Weights & Biases images and charts, install the W\&B Kubernetes Operator, and deploy the W\&B Platform without requiring outbound internet connectivity. This guide targets platform administrators and DevOps engineers who manage Kubernetes infrastructure in regulated or isolated networks.

Air-gapped deployments are common in the following environments:

* Secure government facilities.
* Financial institutions with strict network isolation.
* Healthcare organizations with compliance requirements.
* Industrial control systems (ICS) environments.
* Research facilities with classified networks.

Run these commands in a shell console with proper access to the Kubernetes cluster. You can adapt these commands to work with any CI/CD tooling you use to deploy Kubernetes applications.

For standard on-premises Kubernetes deployments with internet connectivity, see [Deploy Weights & Biases with Kubernetes Operator](https://docs.coreweave.com/products/wandb/platform/hosting/self-managed/operator.md).

## Prerequisites

Before starting, ensure your air-gapped environment meets the following requirements.

### Version requirements

| Software | Minimum version |
| - | - |
| Kubernetes | v1.34 or newer ([Supported Kubernetes versions](https://kubernetes.io/releases/patch-releases/)) |
| Helm | v3.x |
| MySQL | W\&B Self-Managed deployments must run a supported MySQL version that receives security patches and critical bug fixes. Install or upgrade to **MySQL 8.4.x**, or use a managed service version that your provider documents as supported and patched. Aurora MySQL version strings differ from community MySQL versions. Use `SELECT version()` to see the full engine version string and `SELECT aurora_version()` to see the Aurora version. [Aurora MySQL version 3](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/AuroraMySQL.MySQL80.html) is compatible with MySQL 8.0.x and is still supported. See [Amazon Aurora versioning](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/Aurora.VersionPolicy.Versioning.html) and your cloud provider's documentation when you choose a target version. |
| Redis | v7.x |
| ClickHouse | Required for Weave on Self-Managed deployments. Not required if your deployment does not use Weave. See [ClickHouse compatibility for upgrades](https://docs.coreweave.com/products/wandb/platform/hosting/self-managed/operator.md#clickhouse-compatibility-for-upgrades) and [Supported W\&B Server releases](https://docs.coreweave.com/release-notes/server-releases.md). |

### SSL/TLS requirements

W\&B requires a valid signed SSL/TLS certificate for secure communication between clients and the server. SSL/TLS termination must occur on the ingress or load balancer. The W\&B Server application doesn't terminate SSL or TLS connections.

> [!WARNING]
>
> W\&B doesn't support self-signed certificates or custom CAs. Self-signed certificates cause challenges for users and aren't supported.

If possible, use a service like [Let's Encrypt](https://letsencrypt.org) to provide trusted certificates to your load balancer. Services like Caddy and Cloudflare manage SSL for you.

If your security policies require SSL communication within your trusted networks, consider using a tool like Istio and [sidecar containers](https://istio.io/latest/docs/reference/config/networking/sidecar/).

### Hardware requirements

**CPU Architecture**: W\&B runs on Intel (x86) CPU architecture only. ARM is not supported.

**Sizing**: For CPU, memory, and disk sizing recommendations for Kubernetes nodes and MySQL, see the [Sizing section](https://docs.coreweave.com/products/wandb/platform/hosting/self-managed/ref-arch.md#sizing) in the reference architecture. Requirements vary based on whether you're running Models, Weave, or both.

### MySQL database

W\&B requires an external MySQL database.

For production, W\&B recommends using managed database services:

* [AWS RDS Aurora MySQL](https://aws.amazon.com/rds/aurora/)
* [Google Cloud SQL for MySQL](https://cloud.google.com/sql/mysql)
* [Azure Database for MySQL](https://azure.microsoft.com/en-us/products/mysql/)

Managed database services provide automated backups, monitoring, high availability, patching, and reduce operational overhead.

See the [reference architecture](https://docs.coreweave.com/products/wandb/platform/hosting/self-managed/ref-arch.md#mysql) for MySQL requirements, including sizing recommendations and configuration parameters. For the SQL to create the database, see the [bare-metal guide](https://docs.coreweave.com/products/wandb/platform/hosting/self-managed/operator.md#mysql-database). For questions about your deployment's database configuration, contact [support](mailto:forge-support@coreweave.com) or your AISE.

For MySQL configuration parameters for self-managed instances, see the [reference architecture MySQL configuration section](https://docs.coreweave.com/products/wandb/platform/hosting/self-managed/ref-arch.md#mysql-configuration-parameters).

### Redis

W\&B depends on a single-node Redis 7.x deployment, which W\&B's components use for job queuing and data caching. For testing and proof-of-concept work, W\&B Self-Managed includes a local Redis deployment. This bundled deployment isn't appropriate for production use.

For production deployments, W\&B can connect to a Redis instance in the following environments:

* [Amazon ElastiCache](https://aws.amazon.com/elasticache/)
* [Google Cloud Memorystore](https://cloud.google.com/memorystore?hl=en)
* [Azure Cache for Redis](https://azure.microsoft.com/en-us/products/cache)
* Self-hosted Redis in your cloud or on-premises infrastructure

### Object storage

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

For detailed object storage provisioning guidance, see the [Bring Your Own Bucket (BYOB)](https://docs.coreweave.com/products/wandb/platform/hosting/data-security/secure-storage-connector.md) guide. In air-gapped environments, you'll typically use on-premises S3-compatible storage such as MinIO Enterprise, NetApp StorageGRID, or Dell ECS.

### Air-gapped specific requirements

In addition to the preceding standard requirements, air-gapped deployments require the following:

* **Internal container registry**: Access to a private container registry such as Harbor, JFrog Artifactory, or Nexus, with all required Weights & Biases images.
* **Internal Helm repository**: Access to a private Helm chart repository with W\&B Helm charts.
* **Image transfer capability**: A method to transfer container images from an internet-connected system to your air-gapped registry.
* **License file**: A valid Weights & Biases Enterprise license. To obtain a license (for example, from an internet-connected machine), see the [License](https://docs.coreweave.com/products/wandb/platform/hosting/self-managed/requirements.md#license) section on the Requirements page, or contact your Weights & Biases account team.

For complete infrastructure requirements, including networking and load balancer configuration, see the [reference architecture](https://docs.coreweave.com/products/wandb/platform/hosting/self-managed/ref-arch.md#infrastructure-requirements).

## Prepare your air-gapped environment

The following steps prepare your air-gapped environment to host the Weights & Biases container images and Helm charts. Complete these steps before installing the operator or deploying the platform.

### Step 1: Set up internal container registry

Because the Kubernetes cluster cannot pull images from public registries, all required container images must be available in your internal air-gapped container registry before deployment.

> [!NOTE]
>
> You are responsible for tracking the W\&B Operator's requirements and maintaining your container registry with updated images regularly. For the most current list of required container images and versions, refer to the Helm chart, or contact [Support](mailto:forge-support@coreweave.com) or your assigned Weights & Biases support engineer.

#### Core Weights & Biases component containers

The following core images are required:

* [`docker.io/wandb/controller`](https://hub.docker.com/r/wandb/controller): W\&B Kubernetes Operator.
* [`docker.io/wandb/local`](https://hub.docker.com/r/wandb/local): Weights & Biases application server.
* [`docker.io/wandb/console`](https://hub.docker.com/r/wandb/console): Weights & Biases management console.
* [`docker.io/wandb/megabinary`](https://hub.docker.com/r/wandb/megabinary): Weights & Biases microservices (API, executor, glue, parquet).

#### Dependency containers

The following third-party dependency images are required:

* [`docker.io/bitnamilegacy/redis`](https://hub.docker.com/r/bitnamilegacy/redis): Required for local Redis deployment during testing and development. For production Redis requirements, see the [Redis section](#redis) in Prerequisites.
* [`docker.io/otel/opentelemetry-collector-contrib`](https://hub.docker.com/r/otel/opentelemetry-collector-contrib): OpenTelemetry agent for collecting metrics and logs.
* [`quay.io/prometheus/prometheus`](https://quay.io/repository/prometheus/prometheus): Prometheus for metrics collection.
* [`quay.io/prometheus-operator/prometheus-config-reloader`](https://quay.io/repository/prometheus-operator/prometheus-config-reloader): Prometheus dependency.

#### Get the complete image list

To extract the complete list of required images and versions from the Helm chart:

1. On an internet-connected system, download the W\&B Helm charts from the [W\&B Helm charts repository](https://github.com/wandb/helm-charts):

   ```bash theme={"system"}
   # Clone the helm-charts repository
   git clone https://github.com/wandb/helm-charts.git
   cd helm-charts
   ```

2. Inspect the `values.yaml` files to identify all container images and their versions:

   ```bash theme={"system"}
   # Extract image references from the operator chart
   helm show values charts/operator | grep -E "repository:|tag:" | grep -v "^#"

   # Extract image references from the platform chart
   helm show values charts/operator-wandb | grep -E "repository:|tag:" | grep -v "^#"
   ```

   Alternatively, use this command to extract only the repository names (without version tags):

   ```bash theme={"system"}
   helm show values charts/operator-wandb \
     | awk -F': *' '/^[[:space:]]*repository:/{print $2}' \
     | grep -v "^#" \
     | sort -u
   ```

   The list of repositories looks similar to the following:

   ```text theme={"system"}
   wandb/controller
   wandb/local
   wandb/console
   wandb/megabinary
   wandb/weave-python
   wandb/weave-trace
   otel/opentelemetry-collector-contrib
   prometheus/prometheus
   prometheus-operator/prometheus-config-reloader
   bitnamilegacy/redis
   ```

   To get the specific version tags for each image, use the preceding first command (`grep -E "repository:|tag:"`), which shows both repository names and their corresponding version tags.

#### Transfer images to air-gapped registry

1. On an internet-connected system, pull and save all required images.

   > [!NOTE]
   >
   > Replace version numbers in the following examples with the actual versions from your Helm chart inspection in the preceding step. The versions shown here are examples and become outdated over time.

   Use shell variables to manage versions consistently:

   ```bash theme={"system"}
   # Set version variables (update these based on your Helm chart versions)
   CONTROLLER_VERSION="1.13.3"
   APP_VERSION="0.59.2"
   CONSOLE_VERSION="2.12.2"

   # Pull images
   docker pull wandb/controller:${CONTROLLER_VERSION}
   docker pull wandb/local:${APP_VERSION}
   docker pull wandb/console:${CONSOLE_VERSION}
   docker pull wandb/megabinary:${APP_VERSION}
   # ... pull all other required images with their versions

   # Save images to .tar files
   docker save wandb/controller:${CONTROLLER_VERSION} -o wandb-controller-${CONTROLLER_VERSION}.tar
   docker save wandb/local:${APP_VERSION} -o wandb-local-${APP_VERSION}.tar
   docker save wandb/console:${CONSOLE_VERSION} -o wandb-console-${CONSOLE_VERSION}.tar
   docker save wandb/megabinary:${APP_VERSION} -o wandb-megabinary-${APP_VERSION}.tar
   # ... save all other images
   ```

2. Transfer the `.tar` files to your air-gapped environment using your approved method, such as a USB drive or secure file transfer.

3. In your air-gapped environment, load and push images to your internal registry:

   ```bash theme={"system"}
   # Set the same version variables used above
   CONTROLLER_VERSION="1.13.3"
   APP_VERSION="0.59.2"
   CONSOLE_VERSION="2.12.2"
   INTERNAL_REGISTRY="registry.yourdomain.com"

   # Load images
   docker load -i wandb-controller-${CONTROLLER_VERSION}.tar
   docker load -i wandb-local-${APP_VERSION}.tar
   docker load -i wandb-console-${CONSOLE_VERSION}.tar
   docker load -i wandb-megabinary-${APP_VERSION}.tar
   # ... load all other images

   # Tag for internal registry
   docker tag wandb/controller:${CONTROLLER_VERSION} ${INTERNAL_REGISTRY}/wandb/controller:${CONTROLLER_VERSION}
   docker tag wandb/local:${APP_VERSION} ${INTERNAL_REGISTRY}/wandb/local:${APP_VERSION}
   docker tag wandb/console:${CONSOLE_VERSION} ${INTERNAL_REGISTRY}/wandb/console:${CONSOLE_VERSION}
   docker tag wandb/megabinary:${APP_VERSION} ${INTERNAL_REGISTRY}/wandb/megabinary:${APP_VERSION}
   # ... tag all other images

   # Push to internal registry
   docker push ${INTERNAL_REGISTRY}/wandb/controller:${CONTROLLER_VERSION}
   docker push ${INTERNAL_REGISTRY}/wandb/local:${APP_VERSION}
   docker push ${INTERNAL_REGISTRY}/wandb/console:${CONSOLE_VERSION}
   docker push ${INTERNAL_REGISTRY}/wandb/megabinary:${APP_VERSION}
   # ... push all other images
   ```

### Step 2: Set up internal Helm chart repository

With the container images in place, the Kubernetes Operator also needs access to the W\&B Helm charts. Ensure the following Helm charts are available in your internal Helm repository:

* [W\&B Operator chart](https://github.com/wandb/helm-charts/tree/main/charts/operator)
* [W\&B Platform chart](https://github.com/wandb/helm-charts/tree/main/charts/operator-wandb)

1. On an internet-connected system, download the charts:

   ```bash theme={"system"}
   # Add W&B Helm repository
   helm repo add wandb https://wandb.github.io/helm-charts
   helm repo update

   # Download the charts
   helm pull wandb/operator --version 1.13.3
   helm pull wandb/operator-wandb --version 0.18.0
   ```

2. Transfer the `.tgz` chart files to your air-gapped environment and upload them to your internal Helm repository according to your repository's procedures.

   The `operator` chart deploys the W\&B Kubernetes Operator (Controller Manager). The `operator-wandb` chart deploys the W\&B Platform using the values configured in the Custom Resource (CR).

### Step 3: Configure Helm repository access

Configure your local Helm client in the air-gapped environment to point to your internal repository so that subsequent install commands can locate the charts.

1. In your air-gapped environment, configure Helm to use your internal repository:

   ```bash theme={"system"}
   helm repo add local-repo https://charts.yourdomain.com
   helm repo update
   ```

2. Verify the charts are available:

   ```bash theme={"system"}
   helm search repo local-repo/operator
   helm search repo local-repo/operator-wandb
   ```

## Deploy Weights & Biases in air-gapped environment

With your internal registry and Helm repository in place, you can now install the Kubernetes Operator, configure external services, and deploy the W\&B Platform.

### Step 4: Install the Kubernetes Operator

The W\&B Kubernetes Operator (controller manager) manages the W\&B Platform components. To install it in an air-gapped environment, configure it to use your internal container registry.

1. Create a `values.yaml` file with the following content:

   ```yaml theme={"system"}
   image:
     repository: registry.yourdomain.com/wandb/controller
     tag: 1.13.3

   airgapped: true
   ```

   > [!NOTE]
   >
   > Replace the repository and tag with the actual versions you transferred to your internal registry in Step 1. The version shown here (`1.13.3`) is an example and becomes outdated over time.

2. Install the operator and Custom Resource Definition (CRD):

   ```bash theme={"system"}
   helm upgrade --install operator local-repo/operator \
     --namespace wandb \
     --create-namespace \
     --values values.yaml
   ```

3. Verify the operator is running:

   ```bash theme={"system"}
   kubectl get pods -n wandb
   ```

   You should see the operator pod in a `Running` state.

The W\&B Kubernetes Operator is now installed and ready to deploy the W\&B Platform from your internal chart repository.

For full details about supported values, refer to the [Kubernetes operator GitHub repository values file](https://github.com/wandb/helm-charts/blob/main/charts/operator/values.yaml).

### Step 5: Set up MySQL database

Before configuring the W\&B Custom Resource, set up an external MySQL database. For production deployments, Weights & Biases strongly recommends using managed database services where available. However, if you're running your own MySQL instance, create the database and user:

Create a database and a user with the following SQL commands. Replace `[PASSWORD]` with a secure password:

```sql theme={"system"}
CREATE USER 'wandb_local'@'%' IDENTIFIED BY '[PASSWORD]';
CREATE DATABASE wandb_local CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
GRANT ALL ON wandb_local.* TO 'wandb_local'@'%' WITH GRANT OPTION;
```

For MySQL configuration parameters, see the [reference architecture MySQL configuration section](https://docs.coreweave.com/products/wandb/platform/hosting/self-managed/ref-arch.md#mysql-configuration-parameters).

### Step 6: Configure W\&B Custom Resource

After installing the W\&B Kubernetes Operator, configure the Custom Resource (CR) to point to your internal Helm repository and container registry. This configuration ensures the Kubernetes operator uses your internal registry and repository when deploying the required components of the W\&B Platform, instead of attempting to reach public sources.

> [!NOTE]
>
> The following example configuration includes image version tags that become outdated over time. Replace all `tag:` values with the actual versions you transferred to your internal registry in Step 1.

Create a file named `wandb.yaml` with the following content:

```yaml theme={"system"}
apiVersion: apps.wandb.com/v1
kind: WeightsAndBiases
metadata:
  labels:
    app.kubernetes.io/instance: wandb
    app.kubernetes.io/name: weightsandbiases
  name: wandb
  namespace: wandb

spec:
  chart:
    url: https://charts.yourdomain.com
    name: operator-wandb
    version: 0.18.0

  values:
    global:
      host: https://wandb.yourdomain.com
      license: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
      
      bucket:
        accessKey: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
        secretKey: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
        name: s3.yourdomain.com:9000
        path: wandb
        provider: s3
        region: us-east-1
      
      mysql:
        database: wandb
        host: mysql.yourdomain.com
        password: [YOUR-MYSQL-PASSWORD]
        port: 3306
        user: wandb
      
      redis:
        host: redis.yourdomain.com
        port: 6379
        password: [YOUR-REDIS-PASSWORD]
      
      api:
        enabled: true
      
      glue:
        enabled: true
      
      executor:
        enabled: true
      
      extraEnv:
        ENABLE_REGISTRY_UI: 'true'

    # Configure all component images to use internal registry
    app:
      image:
        repository: registry.yourdomain.com/wandb/local
        tag: 0.59.2

    console:
      image:
        repository: registry.yourdomain.com/wandb/console
        tag: 2.12.2

    api:
      image:
        repository: registry.yourdomain.com/wandb/megabinary
        tag: 0.59.2

    executor:
      image:
        repository: registry.yourdomain.com/wandb/megabinary
        tag: 0.59.2

    glue:
      image:
        repository: registry.yourdomain.com/wandb/megabinary
        tag: 0.59.2

    parquet:
      image:
        repository: registry.yourdomain.com/wandb/megabinary
        tag: 0.59.2

    weave:
      image:
        repository: registry.yourdomain.com/wandb/weave-python
        tag: 0.59.2

    otel:
      image:
        repository: registry.yourdomain.com/otel/opentelemetry-collector-contrib
        tag: 0.97.0

    prometheus:
      server:
        image:
          repository: registry.yourdomain.com/prometheus/prometheus
          tag: v2.47.0
      configmapReload:
        prometheus:
          image:
            repository: registry.yourdomain.com/prometheus-operator/prometheus-config-reloader
            tag: v0.67.0

    ingress:
      annotations:
        nginx.ingress.kubernetes.io/proxy-body-size: "0"
      class: nginx
```

> [!NOTE]
>
> Replace all placeholder values, such as hostnames, passwords, and tags, with your actual configuration values. The preceding example shows the most commonly used components.

Depending on your deployment needs, you may also need to configure image repositories for additional components such as the following:

* `settingsMigrationJob`
* `weave-trace`
* `filestream`
* `flat-runs-table`

Refer to the [W\&B Helm repository values file](https://github.com/wandb/helm-charts/blob/main/charts/operator-wandb/values.yaml) for the complete list of configurable components.

### Step 7: Deploy the W\&B Platform

Applying the Custom Resource triggers the operator to install the W\&B Platform components defined in the `operator-wandb` chart, using the configuration and image references from `wandb.yaml`.

1. Apply the W\&B Custom Resource to deploy the platform:

   ```bash theme={"system"}
   kubectl apply -f wandb.yaml
   ```

2. Monitor the deployment progress:

   ```bash theme={"system"}
   # Watch pods being created
   kubectl get pods -n wandb --watch

   # Check deployment status
   kubectl get weightsandbiases -n wandb

   # View operator logs
   kubectl logs -n wandb deployment/wandb-operator-controller-manager
   ```

   The deployment may take several minutes as the operator creates all necessary components.

## OpenShift configuration

Weights & Biases supports deployment on air-gapped OpenShift Kubernetes clusters. OpenShift deployments require additional security context configurations because of OpenShift's stricter security policies. If you're deploying on OpenShift, apply the configurations in this section in addition to the preceding steps.

### OpenShift security context constraints

OpenShift uses Security Context Constraints (SCCs) to control pod permissions. By default, OpenShift assigns the `restricted` SCC to pods, which prevents running as root and requires specific user IDs.

#### Option 1: Use restricted SCC (recommended)

Configure Weights & Biases components to run with the restricted SCC by setting appropriate security contexts in your Custom Resource:

```yaml theme={"system"}
spec:
  values:
    # Configure security contexts for all pods
    app:
      podSecurityContext:
        fsGroup: 1000
        runAsUser: 1000
        runAsNonRoot: true
      securityContext:
        allowPrivilegeEscalation: false
        capabilities:
          drop:
            - ALL
        runAsNonRoot: true
        seccompProfile:
          type: RuntimeDefault

    console:
      podSecurityContext:
        fsGroup: 1000
        runAsUser: 1000
        runAsNonRoot: true
      securityContext:
        allowPrivilegeEscalation: false
        capabilities:
          drop:
            - ALL
        runAsNonRoot: true
        seccompProfile:
          type: RuntimeDefault

    # Repeat for other components: api, executor, glue, parquet, weave
```

#### Option 2: Create custom SCC (if required)

If your deployment requires capabilities not available in the `restricted` SCC, create a custom SCC:

```yaml theme={"system"}
apiVersion: security.openshift.io/v1
kind: SecurityContextConstraints
metadata:
  name: wandb-scc
allowHostDirVolumePlugin: false
allowHostIPC: false
allowHostNetwork: false
allowHostPID: false
allowHostPorts: false
allowPrivilegeEscalation: false
allowPrivilegedContainer: false
allowedCapabilities: []
defaultAddCapabilities: []
fsGroup:
  type: MustRunAs
  ranges:
    - min: 1000
      max: 65535
readOnlyRootFilesystem: false
requiredDropCapabilities:
  - ALL
runAsUser:
  type: MustRunAsRange
  uidRangeMin: 1000
  uidRangeMax: 65535
seLinuxContext:
  type: MustRunAs
supplementalGroups:
  type: RunAsAny
volumes:
  - configMap
  - downwardAPI
  - emptyDir
  - persistentVolumeClaim
  - projected
  - secret
```

1. Apply the SCC:

   ```bash theme={"system"}
   oc apply -f wandb-scc.yaml
   ```

2. Bind the SCC to the Weights & Biases service accounts:

   ```bash theme={"system"}
   oc adm policy add-scc-to-user wandb-scc -z wandb-app -n wandb
   oc adm policy add-scc-to-user wandb-scc -z wandb-console -n wandb
   ```

### OpenShift routes

OpenShift uses Routes instead of standard Kubernetes Ingress. Configure Weights & Biases to use OpenShift Routes:

```yaml theme={"system"}
spec:
  values:
    ingress:
      enabled: false
    
    route:
      enabled: true
      host: wandb.apps.openshift.yourdomain.com
      tls:
        enabled: true
        termination: edge
        insecureEdgeTerminationPolicy: Redirect
```

### OpenShift image pull configuration

If your OpenShift cluster uses an internal image registry with authentication:

1. Create an image pull secret:

   ```bash theme={"system"}
   kubectl create secret docker-registry wandb-registry-secret \
     --docker-server=registry.yourdomain.com \
     --docker-username=[USERNAME] \
     --docker-password=[PASSWORD] \
     --namespace=wandb
   ```

2. Reference the secret in your Custom Resource:

   ```yaml theme={"system"}
   spec:
     values:
       imagePullSecrets:
         - name: wandb-registry-secret
   ```

### OpenShift complete example

The following example shows a complete CR for OpenShift air-gapped deployment:

> [!NOTE]
>
> Replace all `tag:` values in this example with the actual versions you transferred to your internal registry in Step 1. The versions shown are examples and become outdated over time.

```yaml theme={"system"}
apiVersion: apps.wandb.com/v1
kind: WeightsAndBiases
metadata:
  name: wandb
  namespace: wandb

spec:
  chart:
    url: https://charts.yourdomain.com
    name: operator-wandb
    version: 0.18.0

  values:
    global:
      host: https://wandb.apps.openshift.yourdomain.com
      license: [YOUR-LICENSE]
      
      bucket:
        accessKey: [YOUR-ACCESS-KEY]
        secretKey: [YOUR-SECRET-KEY]
        name: s3.yourdomain.com:9000
        path: wandb
        provider: s3
        region: us-east-1
      
      mysql:
        database: wandb
        host: mysql.yourdomain.com
        password: [YOUR-MYSQL-PASSWORD]
        port: 3306
        user: wandb
      
      redis:
        host: redis.yourdomain.com
        port: 6379
        password: [YOUR-REDIS-PASSWORD]

    # OpenShift-specific: Use Routes instead of Ingress
    ingress:
      enabled: false
    
    route:
      enabled: true
      host: wandb.apps.openshift.yourdomain.com
      tls:
        enabled: true
        termination: edge

    # Image pull secret for internal registry
    imagePullSecrets:
      - name: wandb-registry-secret

    # Security contexts for OpenShift restricted SCC
    app:
      image:
        repository: registry.yourdomain.com/wandb/local
        tag: 0.59.2
      podSecurityContext:
        fsGroup: 1000
        runAsUser: 1000
        runAsNonRoot: true
      securityContext:
        allowPrivilegeEscalation: false
        capabilities:
          drop:
            - ALL
        runAsNonRoot: true
        seccompProfile:
          type: RuntimeDefault

    console:
      image:
        repository: registry.yourdomain.com/wandb/console
        tag: 2.12.2
      podSecurityContext:
        fsGroup: 1000
        runAsUser: 1000
        runAsNonRoot: true
      securityContext:
        allowPrivilegeEscalation: false
        capabilities:
          drop:
            - ALL
        runAsNonRoot: true
        seccompProfile:
          type: RuntimeDefault

    # Repeat security contexts for: api, executor, glue, parquet, weave
    # (abbreviated for clarity)
```

> [!NOTE]
>
> Contact [Weights & Biases Support](mailto:forge-support@coreweave.com) or your assigned Weights & Biases support engineer for comprehensive OpenShift configuration examples tailored to your security requirements.

## Verify your installation

After deploying Weights & Biases, verify the installation is working correctly so that you can confirm the platform is reachable, pods are healthy, and the deployment is using only your internal resources.

Follow the general verification steps, then complete the additional air-gapped checks in the following section.

To verify the installation, W\&B recommends using the [W\&B CLI](https://docs.coreweave.com/products/wandb/ref/cli.md). The `wandb verify` command runs tests that confirm components and configurations work as expected.

> [!NOTE]
>
> This procedure assumes that you create the first admin user account in a browser.

To verify the installation:

1. Install the W\&B CLI:

   ```bash theme={"system"}
   pip install wandb
   ```

2. Log in to W\&B:

   ```bash theme={"system"}
   wandb login --host=https://YOUR_DNS_DOMAIN
   ```

   For example:

   ```bash theme={"system"}
   wandb login --host=https://wandb.company-name.com
   ```

3. Verify the installation:

   ```bash theme={"system"}
   wandb verify
   ```

After the command runs, a successful installation displays the following output:

```console theme={"system"}
Default host selected:  https://wandb.company-name.com
Find detailed logs for this test at: /var/folders/pn/b3g3gnc11_sbsykqkm3tx5rh0000gp/T/tmpdtdjbxua/wandb
Checking if logged in...................................................✅
Checking signed URL upload..............................................✅
Checking ability to send large payloads through proxy...................✅
Checking requests to base url...........................................✅
Checking requests made over signed URLs.................................✅
Checking CORs configuration of the bucket...............................✅
Checking wandb package version is up to date............................✅
Checking logged metrics, saving and downloading a file..................✅
Checking artifact save and download workflows...........................✅
```

Contact W\&B Support if you encounter errors.

### Additional air-gapped verification

For air-gapped deployments, also verify:

1. **Image pull**: Confirm all pods successfully pulled images from your internal registry:

   ```bash theme={"system"}
   kubectl get pods -n wandb -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.status.phase}{"\t"}{.status.containerStatuses[*].image}{"\n"}{end}'
   ```

   All images should point to your internal registry and all pods should be in `Running` state.

2. **External connectivity**: Verify Weights & Biases is not attempting external connections (it shouldn't in air-gapped mode):

   ```bash theme={"system"}
   kubectl logs -n wandb deployment/wandb-app --tail=100 | grep -i "connection"
   ```

3. **License validation**: Access the Weights & Biases console and verify your license is active.

## Troubleshooting

### Image pull errors

If pods fail to pull images, check the following:

* Verify images exist in your internal registry.
* Check that the image pull secret is correctly configured.
* Verify network connectivity from Kubernetes nodes to the registry.
* Check registry authentication credentials.

To test an image pull manually:

```bash theme={"system"}
kubectl run test-pull --image=registry.yourdomain.com/wandb/local:0.59.2 --namespace=wandb
kubectl logs test-pull -n wandb
kubectl delete pod test-pull -n wandb
```

### OpenShift SCC errors

If pods fail with permission errors on OpenShift:

```bash theme={"system"}
# Check which SCC is being used
oc get pod [POD-NAME] -n wandb -o yaml | grep scc

# Check service account permissions
oc describe scc wandb-scc
oc get rolebinding -n wandb
```

### Helm chart not found

If the operator can't find the platform chart, check the following:

* Verify the chart repository URL in the Custom Resource.
* Check that the operator pod can reach your internal Helm repository.
* Verify the chart exists in your repository:

  ```bash theme={"system"}
  helm search repo local-repo/operator-wandb
  ```

## Frequently asked questions

### Can I use a different ingress class?

Yes, configure your ingress class by modifying the ingress settings in your Custom Resource:

```yaml theme={"system"}
spec:
  values:
    ingress:
      class: your-ingress-class
```

### How do I handle certificate bundles with multiple certificates?

Split the certificates into multiple entries in the `customCACerts` section:

```yaml theme={"system"}
spec:
  values:
    customCACerts:
      cert1.crt: |
        -----BEGIN CERTIFICATE-----
        ...
        -----END CERTIFICATE-----
      cert2.crt: |
        -----BEGIN CERTIFICATE-----
        ...
        -----END CERTIFICATE-----
```

### How do I prevent automatic updates?

To configure the operator to not automatically update Weights & Biases, do the following:

* Set `airgapped: true` in the operator installation (this disables automatic update checks).
* Control version updates by manually updating the `spec.chart.version` in your Custom Resource.
* Optionally, disable automatic updates from the W\&B System Console.

See [Disable automatic app version updates](https://docs.coreweave.com/products/wandb/platform/hosting/self-managed/disable-automatic-app-version-updates.md) for more details.

> [!NOTE]
>
> Weights & Biases strongly recommends customers with Self-Managed instances update their deployments with the latest release at minimum once per quarter to maintain support and receive the latest features, performance improvements, and fixes. Weights & Biases supports a major release for 12 months from its initial release date. Refer to [Release policies and processes](https://docs.coreweave.com/release-notes/release-policies.md).

### Does the deployment work with no connection to public repositories?

Yes. When `airgapped: true` is set in the operator configuration, the Kubernetes operator uses only your internal resources and doesn't attempt to connect to public repositories.

### How do I update Weights & Biases in an air-gapped environment?

To update Weights & Biases:

1. Pull new container images on an internet-connected system.
2. Transfer images to your air-gapped registry.
3. Upload new Helm charts to your internal repository.
4. Update the `spec.chart.version` and image tags in your Custom Resource.
5. Apply the updated Custom Resource.

   The operator performs a rolling update of the Weights & Biases components.

## Next steps

After successful deployment, complete the following tasks:

* **Configure user authentication**: Set up [SSO](https://docs.coreweave.com/products/wandb/platform/hosting/iam/sso.md) or other authentication methods.
* **Set up monitoring**: Configure monitoring for your Weights & Biases instance and infrastructure.
* **Plan for updates**: Review the [Server upgrade process](https://docs.coreweave.com/products/wandb/platform/hosting/server-upgrade-process.md) and establish an update cadence.
* **Configure backups**: Establish backup procedures for your MySQL database.
* **Document your process**: Create runbooks for your specific air-gapped update procedures.

## Get help

If you encounter issues during deployment:

* Review the [Reference Architecture](https://docs.coreweave.com/products/wandb/platform/hosting/self-managed/ref-arch.md) for infrastructure guidance.
* Check the [Operator guide](https://docs.coreweave.com/products/wandb/platform/hosting/self-managed/operator.md) for configuration details.
* Contact [Support](mailto:forge-support@coreweave.com) or your assigned Weights & Biases support engineer.
* For OpenShift-specific issues, reference Red Hat OpenShift documentation.
