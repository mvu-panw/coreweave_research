# Deploy Milvus on CKS

Source: https://docs.coreweave.com/products/cks/tutorials/deploy-vector-databases-on-cks/milvus

# Deploy Milvus on CKS

> Deploy Milvus Vector Database on CoreWeave Kubernetes Service (CKS)

These instructions explain how to deploy Milvus, an open source vector database built for GenAI applications, on CoreWeave Kubernetes Service (CKS). By the end of this tutorial, you'll have a running Milvus cluster backed by CoreWeave AI Object Storage, with optional GPU-based indexing and scheduled backups.

This tutorial is intended for platform engineers and ML practitioners who want to run a managed Milvus deployment on CKS to support similarity search and other vector workloads.

## Prerequisites

Before you start, you need:

* A working [CKS cluster](https://docs.coreweave.com/products/cks/clusters/create.md) with at least one CPU Node. GPU Nodes are also supported, but CPU Nodes are preferred unless you plan to use GPU-based indexing.
* Access Key and Secret Key with permissions to use a [CoreWeave AI Object Storage](https://docs.coreweave.com/products/storage/object-storage/get-started-caios.md) bucket.

You'll need the following tools on your local machine:

* [`kubectl`](https://kubernetes.io/docs/reference/kubectl/) installed and configured for your cluster.
* [`helm`](https://helm.sh/docs/intro/install/) version 3.8 or later.
* Git.

It's also helpful to have an Object Storage command-line tool such as the [AWS CLI](https://docs.coreweave.com/products/storage/object-storage/using-object-storage/manage-objects.md) to access your bucket when testing.

## Step 1. Verify your system configuration

Before installing Milvus, confirm that your cluster is reachable and has the Node types required for the deployment.

1. Verify that you can access your cluster with `kubectl`. For example:

   ```bash theme={"system"}
   kubectl cluster-info
   ```

   You should see something similar to:

   ```text theme={"system"}
   Kubernetes control plane is running at...
   CoreDNS is running at...
   node-local-dns is running at...
   ```

2. Verify your cluster has at least one CPU Node. GPU Nodes are also supported, but CPU Nodes are preferred unless you plan to use GPU-based indexing. For example:

   ```bash theme={"system"}
   kubectl get nodes -o=custom-columns="NAME:metadata.name,CLASS:metadata.labels['node\.coreweave\.cloud\/class']"
   ```

   You should see something similar to the following:

   ```text theme={"system"}
   NAME      CLASS
   g137a10   gpu
   g5424e0   cpu
   g77575e   cpu
   gd926d4   gpu
   ```

## Step 2. Deploy Milvus

In this step, you install the Milvus Operator and prepare the CoreWeave Milvus Helm chart with your Object Storage and indexing settings.

1. Install the Milvus Operator. See the [Operator installation guide](https://milvus.io/docs/install_cluster-milvusoperator.md?tab=helm) for more details.

   ```bash theme={"system"}
   helm install milvus-operator \
     -n milvus-operator --create-namespace \
     --wait --wait-for-jobs \
     https://github.com/zilliztech/milvus-operator/releases/download/v1.3.0/milvus-operator-1.3.0.tgz
   ```

   This installs the Milvus Custom Resource Definition (CRD), which defines Milvus clusters, along with the Operator that manages them. It creates a new namespace called `milvus-operator` for the Operator itself.

   You can add `milvus-operator` as a dependency to the CoreWeave chart (which you'll download in the next step), but installing it in a separate namespace from the database is preferred. The Operator can manage multiple Milvus clusters in different namespaces.

2. Clone the CoreWeave Milvus chart repository at:

   [https://github.com/coreweave/reference-architecture/tree/main/tooling/vector\_dbs/cw-milvus](https://github.com/coreweave/reference-architecture/tree/main/tooling/vector_dbs/cw-milvus)

3. Edit the chart's `values.yaml` with your details:

   Replace `[BUCKET-NAME]` with the name of your Object Storage bucket, and replace `[ACCESS-KEY]` and `[SECRET-KEY]` with your Object Storage credentials.

   ```yaml theme={"system"}
   caiosBucketName: [BUCKET-NAME]
   caiosAccessKey: [ACCESS-KEY]
   caiosSecretKey: [SECRET-KEY]
   ```

   > [!CAUTION]
   >
   > **Check the deleteDependencies policy**
   >
   > This chart automatically deletes dependencies like `etcd` and `kafka` by default. This makes it easier to clean up after an experiment is complete.
   >
   > You should set `deleteDependencies` to `false` if you want to retain these dependencies after deleting the Milvus custom resource.

4. If you plan to use [GPU-based indexing](https://milvus.io/docs/index-with-gpu.md), set the `gpuIndexing` value to `true` in `values.yaml`. This schedules the relevant components on GPU Nodes as shown.

   ```yaml theme={"system"}
   dataNode:
     affinity:
       nodeAffinity:
         # override global component affinity when using GPU indexing
         requiredDuringSchedulingIgnoredDuringExecution:
           nodeSelectorTerms:
           - matchExpressions:
             - key: node.coreweave.cloud/class
               operator: In
               values:
               - gpu
   queryNode:
     affinity:
       nodeAffinity:
         # override global component affinity when using GPU indexing
         requiredDuringSchedulingIgnoredDuringExecution:
           nodeSelectorTerms:
           - matchExpressions:
             - key: node.coreweave.cloud/class
               operator: In
               values:
               - gpu
   ```

### Chart defaults

The CoreWeave chart handles the following items:

* It provisions a secret with the Object Storage credentials you specified in `values.yaml`.

* It configures the Object Storage bucket you specified, with `aliyun` as the provider. This ensures that Milvus [uses virtual-host style addressing](https://github.com/milvus-io/milvus/blob/cc53b25ba4e885bc905adae3b4d88a09fe110a59/configs/milvus.yaml#L142).

  ```yaml theme={"system"}
  config:
    minio:
      # Use "aliyun" as cloud provider, as that enables virtual host style bucket requests
      cloudProvider: aliyun
      useVirtualHost: true
      bucketName: {{ .Values.caiosBucketName }}
      # Optional, config the prefix of the bucket milvus will use
      rootPath: {{ include "cw-milvus.name" . }}
      useSSL: true
  ```

* It sets the storage type to `S3` and uses the CoreWeave AI Object Storage endpoint (`cwobject.com:443`).

  ```yaml theme={"system"}
  dependencies:
    storage:
    # enable external object storage
    external: true
    type: S3 # MinIO | S3
    # the endpoint of AWS S3
    endpoint: cwobject.com:443
    # the secret storing the access key and secret key
    secretRef: '{{ include "cw-milvus.name" . }}-caios-secret'
  ```

* It configures Kafka as the message storage service and overrides the default image.

  ```yaml theme={"system"}
  kafka:
    inCluster:
      deletionPolicy: Delete
      pvcDeletion: true
      values:
      image:
        repository: bitnami/kafka
        tag: 3.7.0-debian-12-r6
  ```

* It sets Node affinities for the Milvus components to CPU Nodes. However, scheduling onto GPU Nodes is also possible when using [GPU-based indexing](https://milvus.io/docs/index-with-gpu.md) as described in Step 2.

  ```yaml theme={"system"}
  affinity:
    nodeAffinity:
      # prefer running on CPU nodes, if available
      # see also queryNode and dataNode affinities for GPU-based indexing
      preferredDuringSchedulingIgnoredDuringExecution:
        - weight: 100
          preference:
            matchExpressions:
            - key: node.coreweave.cloud/class
              operator: In
              values:
              - cpu
  ```

* It configures a `CronJob` for backup using [milvus-backup](https://milvus.io/docs/single-instance-backup-and-restore.md). You can control the cron expression for scheduling the job, as well as settings for the backup bucket through values in `values.yaml`. If you don't specify a bucket name and credentials for backups, the ones specified for the database are used.

  Replace `[BACKUP-BUCKET-NAME]` with the name of your backup bucket, and replace `[BACKUP-ACCESS-KEY]` and `[BACKUP-SECRET-KEY]` with the credentials for that bucket.

  ```yaml theme={"system"}
  backupCaiosBucketName: [BACKUP-BUCKET-NAME]
  backupCaiosAccessKey: [BACKUP-ACCESS-KEY]
  backupCaiosSecretKey: [BACKUP-SECRET-KEY]
  # defaults to "backup"
  backupCaiosBucketRootPath:
  backupCronExpression: "30 7 * * *"
  ```

  > [!WARNING]
  >
  > **Backups accumulate over time**
  >
  > Backup names are based on timestamps, so they're unique. Backups accumulate in your bucket unless you periodically clean out unneeded ones.

## Step 3. Install the chart

With the Operator running and `values.yaml` configured, install the CoreWeave Milvus chart to create the Milvus custom resource and provision the database.

1. Change to the chart directory:

   ```bash theme={"system"}
   cd reference-architecture/tooling/vector_dbs/cw-milvus
   ```

2. Install the chart in a new namespace, for example `milvus`:

   ```bash theme={"system"}
   helm install -n milvus cw-milvus .
   ```

3. Check the status of the custom resource. This might take several minutes to complete, as the Operator sets up the database and its dependencies.

   ```bash theme={"system"}
   kubectl -n milvus describe milvus cw-milvus
   ```

   The `Conditions` block shows the status of individual components. After everything is set up, that block should look like this:

   ```text theme={"system"}
   Conditions:
       Last Transition Time:  2025-09-22T21:47:24Z
       Message:               All Milvus components are healthy
       Reason:                ReasonMilvusHealthy
       Status:                True
       Type:                  MilvusReady
       Last Transition Time:  2025-09-18T23:14:29Z
       Message:               Milvus components are all updated
       Reason:                MilvusComponentsUpdated
       Status:                True
       Type:                  MilvusUpdated
       Last Transition Time:  2025-09-18T23:12:32Z
       Message:               Etcd endpoints is healthy
       Reason:                EtcdReady
       Status:                True
       Type:                  EtcdReady
       Last Transition Time:  2025-09-18T23:12:32Z
       Reason:                StorageReady
       Status:                True
       Type:                  StorageReady
       Last Transition Time:  2025-09-18T23:13:29Z
       Reason:                MsgStreamReady
       Status:                True
       Type:                  MsgStreamReady
   ```

## Step 4. Access the database

After the database is ready, the web UI service is available on port 9091, and the database service is available on port 19530. To access these, forward local ports from your machine to the service.

1. Forward a local port to the database service.

   ```bash theme={"system"}
   kubectl port-forward --address 0.0.0.0 service/cw-milvus-milvus 27017:19530
   Forwarding from 0.0.0.0:27017 -> 19530
   ```

2. Forward a local port to the web UI service.

   ```bash theme={"system"}
   kubectl port-forward --address 0.0.0.0 service/cw-milvus-milvus 27018:9091
   Forwarding from 0.0.0.0:27018 -> 9091
   ```

You can now access the web UI at `http://localhost:27018` and connect to the database at `localhost:27017`. At this point, your Milvus cluster is deployed on CKS, backed by CoreWeave AI Object Storage, and ready for you to create collections and load data.

## Additional resources

See the [Milvus documentation](https://milvus.io/docs) to learn more.
