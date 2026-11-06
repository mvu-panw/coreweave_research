# Use pgvector with CoreWeave Database

Source: https://docs.coreweave.com/products/cks/tutorials/deploy-vector-databases-on-cks/pgvector

# Use pgvector with CoreWeave Database

> Deploy managed PostgreSQL on CKS, store vectors, and query them with pgvector

[CoreWeave Database (CWDB)](https://docs.coreweave.com/products/storage/cwdb.md) runs managed PostgreSQL inside your CoreWeave Kubernetes Service (CKS) cluster. With the pgvector extension, you can store embeddings alongside application data and query them with SQL. In this tutorial, you create a CWDB database with pgvector, connect from a client Pod, and run cosine similarity searches.

You then add a hierarchical navigable small world (HNSW) index for approximate nearest-neighbor search. CoreWeave manages the database operator, replication, and backups.

## Before you begin

Before you begin, make sure you have the following:

* A CKS cluster with [CWDB enabled](https://docs.coreweave.com/products/storage/cwdb.md#request-limited-availability-access). To request access, contact CoreWeave through your customer Slack channel with the CKS cluster name and the Namespace you plan to use.
* CPU capacity for three database instances. This example requests 1 CPU and 2 GiB of memory per instance, plus capacity for the managed supporting Pods and a client Pod.
* A default CoreWeave Distributed File Storage (DFS) StorageClass with capacity for three 25 GiB volumes. These are provisioned volume sizes, not the amount of data stored by this example.
* `kubectl` configured for the target CKS cluster, with permission to create a Namespace, a `CWDBCluster`, and a client Pod. You also need permission to execute commands in the client Pod.

Confirm the target context and CWDB API before creating resources:

```bash theme={"system"}
kubectl config current-context
kubectl cluster-info
kubectl api-resources --api-group=data.coreweave.com
kubectl get storageclasses
```

The API resource list must include `cwdbclusters`. If it doesn't, confirm CWDB enablement with CoreWeave. If access is forbidden, ask your cluster administrator to check your permissions. See [Create a database](https://docs.coreweave.com/products/storage/cwdb/create.md#before-you-begin) for CPU capacity requirements.

The commands use a new Namespace named `cwdb-pgvector-tutorial` and a database resource named `vector-db`. Use these names throughout the walkthrough. The resource sizes are for learning, not production sizing guidance.

## Deploy CoreWeave Database with pgvector

Create a dedicated Namespace:

```bash theme={"system"}
kubectl create namespace cwdb-pgvector-tutorial
```

Save the following manifest as the `cwdb-pgvector.yaml` file:

```yaml title="cwdb-pgvector.yaml" theme={"system"}
apiVersion: data.coreweave.com/v1
kind: CWDBCluster
metadata:
  name: vector-db
  namespace: cwdb-pgvector-tutorial
spec:
  type: postgres
  postgres:
    instances: 3
    dbName: vectors
    owner: app
    extension:
      name: pgvector
  storage:
    resources:
      requests:
        storage: 25Gi
  resources:
    requests:
      cpu: "1"
      memory: 2Gi
    limits:
      memory: 4Gi
```

The `extension.name: pgvector` setting selects the pgvector-enabled PostgreSQL image. CWDB creates the SQL extension named `vector` in the initial database, `vectors`. You don't need to run `CREATE EXTENSION` in this database. The `owner` field creates the application role, `app`.

This manifest creates three PostgreSQL instances and leaves managed backups enabled. For supported PostgreSQL versions and other options, see [Configure database](https://docs.coreweave.com/products/storage/cwdb/configure.md#extensions).

Validate and apply the manifest, then wait for CWDB to report readiness:

```bash theme={"system"}
kubectl apply --dry-run=server -f cwdb-pgvector.yaml
kubectl apply -f cwdb-pgvector.yaml
kubectl wait --for=condition=Ready cwdbcluster/vector-db \
  --namespace cwdb-pgvector-tutorial --timeout=600s
```

The wait command returns the following output:

```text theme={"system"}
cwdbcluster.data.coreweave.com/vector-db condition met
```

If the wait times out, inspect the resource and its events before continuing:

```bash theme={"system"}
kubectl describe cwdbcluster vector-db --namespace cwdb-pgvector-tutorial
kubectl get pods,pvc --namespace cwdb-pgvector-tutorial
kubectl get events --namespace cwdb-pgvector-tutorial --sort-by=.metadata.creationTimestamp
```

See [Troubleshoot CWDB](https://docs.coreweave.com/products/storage/cwdb/troubleshooting.md) for provisioning failures.

## Connect with application credentials

CWDB creates a Secret containing the application connection URI. For this manifest, the Secret is `vector-db-vectors-credentials`: the resource name followed by the initial database name and `-credentials`. Its `uri` key points to the read-write pooler Service, `vector-db-pooler-rw`.

Use a client Pod in the same Namespace to resolve that Service name. Save the following manifest as the `pgvector-client.yaml` file. Kubernetes injects the URI directly from the Secret, so you don't need to print or copy a password.

```yaml title="pgvector-client.yaml" theme={"system"}
apiVersion: v1
kind: Pod
metadata:
  name: pgvector-client
  namespace: cwdb-pgvector-tutorial
spec:
  restartPolicy: Never
  automountServiceAccountToken: false
  containers:
    - name: psql
      image: postgres:18-bookworm
      command: ["sleep", "infinity"]
      resources:
        requests:
          cpu: 100m
          memory: 128Mi
        limits:
          memory: 256Mi
      env:
        - name: PGSSLMODE
          value: require
        - name: PGURI
          valueFrom:
            secretKeyRef:
              name: vector-db-vectors-credentials
              key: uri
```

Create the client and open `psql`:

```bash theme={"system"}
kubectl apply -f pgvector-client.yaml
kubectl wait --for=condition=Ready pod/pgvector-client \
  --namespace cwdb-pgvector-tutorial --timeout=120s
kubectl exec -it pgvector-client --namespace cwdb-pgvector-tutorial -- \
  sh -c 'psql "$PGURI" -X -v ON_ERROR_STOP=1'
```

A successful connection displays the `vectors=>` prompt. Run the remaining SQL commands in this `psql` session. Application traffic should use the pooler Services. See [Connect to a database](https://docs.coreweave.com/products/storage/cwdb/connect.md) for other connection methods and cross-Namespace DNS names.

## Verify pgvector

Check the connected database, role, and installed extension:

```sql theme={"system"}
SELECT current_database(), current_user;
SELECT extname, extversion FROM pg_extension WHERE extname = 'vector';
```

The first query must return `vectors` and `app`. The second must return one row for `vector`. Its version depends on the CWDB image deployed in your cluster.

If the extension query returns no rows, confirm that you're connected to `vectors`, that the manifest specifies `extension.name: pgvector`, and that CWDB reports `Ready`. This tutorial uses the initial database that CWDB manages. It doesn't configure extensions in additional databases you create yourself.

## Store and search vectors

Create a table with text, a category, and a three-dimensional vector:

```sql theme={"system"}
CREATE TABLE documents (
  id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  content text NOT NULL,
  category text NOT NULL,
  embedding vector(3) NOT NULL
);

INSERT INTO documents (content, category, embedding) VALUES
  ('Store application data in PostgreSQL', 'database', '[1,0,0]'),
  ('Search embeddings with pgvector', 'database', '[0.9,0.1,0]'),
  ('Serve a language model', 'inference', '[0,1,0]'),
  ('Train an image classifier', 'training', '[0,0,1]');
```

These vectors are hand-written examples to make the results reproducible. They aren't embeddings generated from the text. In an application, generate document and query embeddings with the same embedding model and use its output dimension in place of `3`. pgvector stores and searches vectors. It doesn't generate embeddings.

The `<=>` operator calculates cosine distance. Order by distance in ascending order to retrieve the nearest vectors. Subtract the distance from `1` to display cosine similarity:

```sql theme={"system"}
SELECT id, content,
       round((1 - (embedding <=> '[1,0,0]'::vector))::numeric, 4) AS similarity
FROM documents
ORDER BY embedding <=> '[1,0,0]'::vector
LIMIT 2;
```

The query returns the following output:

```text theme={"system"}
 id |               content                | similarity
----+--------------------------------------+------------
  1 | Store application data in PostgreSQL |     1.0000
  2 | Search embeddings with pgvector      |     0.9939
(2 rows)
```

No vector index exists yet, so this is an exact nearest-neighbor search. You can also combine vector search with a SQL filter:

```sql theme={"system"}
SELECT id, content
FROM documents
WHERE category = 'database'
ORDER BY embedding <=> '[1,0,0]'::vector
LIMIT 2;
```

This query returns rows `1` and `2`. In your application, send query vectors as bound parameters through your PostgreSQL driver instead of interpolating them into SQL strings.

## Add an approximate nearest-neighbor index

HNSW indexes on the `vector` type support up to 2,000 dimensions. Check your embedding model's dimensions before using this index.

For larger datasets, an HNSW index can speed up nearest-neighbor queries by trading some recall for speed. Create an index with the operator class that matches cosine distance:

```sql theme={"system"}
CREATE INDEX documents_embedding_hnsw
ON documents USING hnsw (embedding vector_cosine_ops);
ANALYZE documents;
```

Run the same nearest-neighbor query:

```sql theme={"system"}
SELECT id, content
FROM documents
ORDER BY embedding <=> '[1,0,0]'::vector
LIMIT 2;
```

For this example, the result is still rows `1` and `2`. Keep the distance operator directly in `ORDER BY`, with ascending order and a `LIMIT`, so the query can use the vector index. Inspect the query plan:

```sql theme={"system"}
EXPLAIN (COSTS OFF)
SELECT id, content
FROM documents
ORDER BY embedding <=> '[1,0,0]'::vector
LIMIT 2;
```

PostgreSQL may choose a sequential scan for this four-row table. That's expected and doesn't mean index creation failed. Test latency and recall with representative data before choosing index settings for production.

> [!NOTE]
>
> When a query uses an approximate vector index, SQL filters can reduce the number of returned rows below `LIMIT`. See the [pgvector filtering guidance](https://github.com/pgvector/pgvector#filtering) for indexing and iterative-scan options supported by your installed version.

## Clean up

Exit `psql`:

```text theme={"system"}
\q
```

> [!WARNING]
>
> The following commands delete the tutorial database and its Kubernetes resources. Only run them when you no longer need the example data. Storage retained by the StorageClass reclaim policy and managed backups can outlive the database. See [Delete a database](https://docs.coreweave.com/products/storage/cwdb/manage.md#delete-a-database) before deleting resources that contain data you need.

```bash theme={"system"}
kubectl delete pod pgvector-client --namespace cwdb-pgvector-tutorial
kubectl delete cwdbcluster vector-db --namespace cwdb-pgvector-tutorial --wait=true
kubectl delete namespace cwdb-pgvector-tutorial
```

## Next steps

Explore the following resources to adapt this tutorial to your workload:

* Read the [pgvector documentation](https://github.com/pgvector/pgvector) for supported distance functions, index tuning, and client libraries.
* [Configure CWDB](https://docs.coreweave.com/products/storage/cwdb/configure.md) to size the database for your workload.
* Review [managed backups](https://docs.coreweave.com/products/storage/cwdb/backups.md) and recovery options.
