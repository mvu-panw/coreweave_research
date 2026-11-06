# Deploy Dragonfly on CKS

Source: https://docs.coreweave.com/products/cks/tutorials/deploy-vector-databases-on-cks/dragonfly

# Deploy Dragonfly on CKS

> Deploy Dragonfly Vector Database on CoreWeave Kubernetes Service (CKS)

This tutorial explains how to deploy Dragonfly, an open-source vector database built for GenAI applications, on CoreWeave Kubernetes Service (CKS). By the end, you have a running Dragonfly cluster managed by the Dragonfly Operator. The cluster is configured with automated snapshotting to persistent storage, and reachable from your local machine through a Redis-compatible client.

This tutorial is for platform engineers and ML practitioners who want a low-latency, Redis-compatible in-memory store to back GenAI workloads on CKS.

## Prerequisites

Before you start, you need a working [CKS cluster](https://docs.coreweave.com/products/cks/clusters/create.md), ideally with CPU Nodes. You can also use a GPU Node cluster, but Dragonfly has no capability that would benefit from GPUs.

You'll need the following tools on your local machine:

* [`kubectl`](https://kubernetes.io/docs/reference/kubectl/) installed and configured for your cluster.
* [Helm](https://helm.sh/docs/intro/install/) version 3.8+.
* Git.

## Step 1. Verify your system configuration

Before deploying Dragonfly, confirm that your local tooling can reach the cluster and that the cluster has Nodes suitable for running the database.

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

2. Verify your cluster has at least one CPU Node. GPU Nodes are also supported, but CPU Nodes are preferred since Dragonfly cannot use GPUs for any of its functionality. For example:

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

## Step 2. Deploy Dragonfly

In this step, you install the Dragonfly Operator and prepare the CoreWeave Dragonfly Helm chart that defines your database cluster.

1. Install the Dragonfly Operator. See the [Operator installation guide](https://www.dragonflydb.io/docs/managing-dragonfly/operator/installation#installation) for more details.

   ```bash theme={"system"}
   kubectl apply -f https://raw.githubusercontent.com/dragonflydb/dragonfly-operator/main/manifests/dragonfly-operator.yaml
   ```

   This installs the Dragonfly Custom Resource Definition (CRD), which defines Dragonfly clusters, along with the Operator that manages them. It creates a new namespace called `dragonfly-operator-system` for the Operator itself.

   You can add `dragonfly-operator` as a dependency to the CoreWeave chart, which you download in the next step. However, installing it in a separate namespace from the database is preferred. The Operator can manage multiple Dragonfly clusters in different namespaces.

2. Clone the CoreWeave Dragonfly chart repository. It's located at [https://github.com/coreweave/reference-architecture/tree/main/tooling/vector\_dbs/cw-dragonfly](https://github.com/coreweave/reference-architecture/tree/main/tooling/vector_dbs/cw-dragonfly).

3. Edit the chart's `values.yaml` with your details. None of the values in `values.yaml` must be changed, but you can adjust them for your specific use case. Keep the following principles in mind:

   * Dragonfly allocates 80% of the limit memory.
   * If the CPU limit is set, the I/O threads are equal to it.
   * If the CPU limit is not set, all visible cores are used.
   * If the CPU limit is not set and the proactor threads parameter is set, the parameter is used.
   * Ensure you have 256MiB memory per thread.
   * See [CoreWeave CPU Instances](https://docs.coreweave.com/platform/instances/cpu-instances.md) for details about the number of cores and memory per Node.

   The CoreWeave chart handles the following items:

   * Provisioning a secret for the database password. You can also specify one of your own through the `dbPassword` attribute in `values.yaml`, or provide an existing secret containing the password through `existingDbPasswordSecretName`.
   * Setting Node affinities for the Dragonfly Pods to CPU Nodes. Pods *will* be scheduled onto GPU Nodes if no CPU Nodes are available.

   For example:

   ```yaml theme={"system"}
   affinity:
     # prefer running on CPU nodes, if available
     nodeAffinity:
       preferredDuringSchedulingIgnoredDuringExecution:
         - weight: 100
           preference:
             matchExpressions:
             - key: node.coreweave.cloud/class
               operator: In
               values:
               - cpu
   ```

   * Configuring [snapshotting to PVC](https://www.dragonflydb.io/docs/managing-dragonfly/operator/snapshot-pvc) backed by VAST.

   You can control the cron expression for scheduling the job, as well as the volume size, through the following block in `values.yaml`.

   ```yaml theme={"system"}
   snapshot:
     cron: "30 7 * * *"
     enableOnMasterOnly: false
     persistentVolumeClaimSpec:
         storageClassName: shared-vast
         accessModes:
         - ReadWriteMany
         resources:
           requests:
             storage: 2Gi
   ```

   By default, the chart configures Dragonfly to maintain [a single snapshot file](https://www.dragonflydb.io/docs/managing-dragonfly/backups#the-dbfilename-flag) and provisions a sidecar container that copies the snapshot to a persistent volume. You can control the scheduling of the snapshot copy job through `snapshotMoveCron`.

   > [!WARNING]
   >
   > **Snapshots will accumulate**
   >
   > Snapshots are not pruned, regardless of which mechanism you use (timestamped snapshots or scheduled snapshot copies). They accumulate on your volume unless you clean out unneeded ones periodically.
   > Alternatively, you can specify a database file name as an argument. The effect is that a single snapshot is kept with that name. The cron expression governs the timing of creating that snapshot.

## Step 3. Install the chart

With the Operator running and the chart values reviewed, install the chart to create the Dragonfly cluster in your CKS environment.

1. Change to the chart directory:

   ```bash theme={"system"}
   cd reference-architecture/tooling/vector_dbs/cw-dragonfly
   ```

2. Install the chart in a new namespace, for example, `dragonfly`:

   ```bash theme={"system"}
   helm install -n dragonfly --create-namespace cw-dragonfly .
   ```

3. Check the status of the custom resource. This may take several minutes to complete, as the Operator sets up the database.

   ```bash theme={"system"}
   kubectl -n dragonfly describe dragonfly cw-dragonfly
   ```

   The `Status` block shows the status of the database. Once everything is set up, that block should look like this:

   ```text theme={"system"}
   Status:
     Phase:  Ready
   ```

## Step 4. Access the database

After the database is ready, its service is available on port `6379`. To access it, forward local ports from your machine to the service.

1. Forward a local port to the database service.

   ```bash theme={"system"}
   kubectl -n dragonfly port-forward --address 0.0.0.0 service/cw-dragonfly 27017:6379
   ```

   You should see output similar to:

   ```text theme={"system"}
   Forwarding from 0.0.0.0:27017 -> 6379
   ```

2. Connect to the database at `localhost:27017`. You can use any Redis client, such as the Redis CLI, to connect:

   ```bash theme={"system"}
   redis-cli -h localhost -p 27017
   ```

   Authenticate before you read or write keys. Replace `[YOUR-PASSWORD]` with your Dragonfly password:

   ```text title="Example session" theme={"system"}
   localhost:27017> GET 1
   (error) NOAUTH Authentication required.
   localhost:27017> AUTH [YOUR-PASSWORD]
   OK
   localhost:27017> GET 1
   (nil)
   ```

   If you didn't specify your own password, you can get the password by looking at the `cw-dragonfly-db-password` secret in the `dragonfly` namespace. Note the password is base64 encoded.

You now have a running Dragonfly cluster on CKS, managed by the Dragonfly Operator, with snapshotting configured to a VAST-backed persistent volume and reachable from your local machine through a Redis-compatible client.

## Additional resources

See the [Dragonfly documentation](https://www.dragonflydb.io/docs) to learn more.
