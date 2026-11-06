# Troubleshoot

Source: https://docs.coreweave.com/products/storage/cwdb/troubleshooting

# Troubleshoot

> Symptoms, causes, and fixes for common CoreWeave Database issues, plus how to escalate

This page covers the issues most pilot customers hit during limited availability. For each, it lists the symptom, the likely cause, and how to verify or fix it.

## Database never becomes `Ready`

### Symptom

The following wait command times out, and `kubectl describe` shows the database stuck in `Provisioning` or `Pending`:

```bash theme={"system"}
kubectl wait --for=condition=Ready cwdbcluster [CLUSTER-NAME] \
  --namespace [NAMESPACE] \
  --timeout=300s
```

### What to check

1. **Inspect the database status:**

   ```bash theme={"system"}
   kubectl describe cwdbcluster [CLUSTER-NAME] --namespace [NAMESPACE]
   ```

   Look at the `Status.Conditions` section. The condition messages typically point at the underlying problem (scheduling, storage, image pull, certificate generation).

2. **Check the pods:**

   ```bash theme={"system"}
   kubectl get pods --namespace [NAMESPACE] -l cnpg.io/cluster=[CLUSTER-NAME]
   ```

   A pod in `Pending` state usually means the scheduler can't place it. `kubectl describe pod` on that pod surfaces the reason, most often "no CPU nodes available" or "Insufficient memory".

3. **Check the PersistentVolumeClaims (PVCs):**

   ```bash theme={"system"}
   kubectl get pvc --namespace [NAMESPACE] -l cnpg.io/cluster=[CLUSTER-NAME]
   ```

   A PVC stuck in `Pending` means Distributed File Storage (DFS) couldn't provision the volume.

### Common causes

* The CKS cluster has no CPU nodes with sufficient capacity. Provision CPU capacity through your usual CKS workflow.
* The CoreWeave Database (CWDB) add-on isn't enabled on this CKS cluster. Confirm `kubectl get crd | grep coreweave.com` shows the CWDB CRDs. If not, request enablement through your customer Slack channel.
* The requested storage size exceeds available DFS capacity in the zone.

## Resource is created in the wrong namespace

### Symptom

You apply a `CWDBCluster` manifest and the database appears in the `default` namespace, not the one you expected. Applications in your target namespace can't resolve the pooler Service.

### Cause

The manifest didn't specify a namespace and you didn't pass `--namespace` on the command line. Kubernetes defaults to the `default` namespace in that case.

### Fix

Delete the resource from `default` and recreate it in the correct namespace:

```bash theme={"system"}
kubectl delete cwdbcluster [CLUSTER-NAME] --namespace default
kubectl apply -f cwdb_cluster.yaml --namespace [NAMESPACE]
```

To prevent this, either set `metadata.namespace` in the manifest or always pass `--namespace [NAMESPACE]` on `kubectl apply`.

## Application can't connect to the database

### Symptom

Your application reports a connection error such as `connection refused`, `name resolution failed`, or `password authentication failed`.

### What to check

1. **Confirm the database is `Ready`:**

   ```bash theme={"system"}
   kubectl get cwdbcluster [CLUSTER-NAME] --namespace [NAMESPACE]
   ```

2. **Verify the Service exists:**

   ```bash theme={"system"}
   kubectl get svc [CLUSTER-NAME]-pooler-rw --namespace [NAMESPACE]
   ```

3. **Check that your application is connecting to the pooler, not the direct database Service.** Application traffic should go to `[CLUSTER-NAME]-pooler-rw` or `[CLUSTER-NAME]-pooler-ro`. The `uri` field in the `[CLUSTER-NAME]-[DBNAME]-credentials` Secret already points at the pooler. `[DBNAME]` is the initial database name set in `spec.postgres.dbName`, which defaults to `app`. For example, a `CWDBCluster` named `vector-db` with `dbName: vectors` has the Secret `vector-db-vectors-credentials`. If `dbName` isn't a valid RFC 1035 label (at most 63 lowercase letters, digits, and hyphens, starting with a letter and ending with a letter or digit), the operator uses `app` in the Secret name instead, so `dbName: orders_db` produces `[CLUSTER-NAME]-app-credentials`.

4. **Verify cross-namespace name resolution.** From a pod in a different namespace, use the fully qualified name: `[CLUSTER-NAME]-pooler-rw.[DB-NAMESPACE].svc.cluster.local`.

5. **Re-decode the credentials Secret.** If the password has rotated, your application may be using a stale value:

   ```bash theme={"system"}
   kubectl get secret [CLUSTER-NAME]-[DBNAME]-credentials \
     --namespace [NAMESPACE] \
     -o jsonpath='{.data.password}' | base64 -d
   ```

See [Connect to a database](https://docs.coreweave.com/products/storage/cwdb/connect.md) for the full list of connection options.

## `psql` works from a debug pod but fails from the application

### Symptom

You can connect from a debug pod using the URI from the Secret, but the application pod cannot.

### Common causes

* The application is reading the wrong Secret. Confirm it mounts `[CLUSTER-NAME]-[DBNAME]-credentials` for read-write traffic (`[CLUSTER-NAME]-app-credentials` for the default `dbName: app`) or `[CLUSTER-NAME]-[DBNAME]-credentials-ro` for read-only traffic to replicas.
* The application has a NetworkPolicy that blocks egress to the database namespace. Check NetworkPolicies in the application's namespace.
* The application is configured with a hard-coded hostname or port that doesn't match the pooler Service.

## On-demand backup stays in `Pending`

### Symptom

The backup stays in `Pending` for longer than a few minutes when you check its status. Replace `[BACKUP-NAME]` with the name of the `CWDBBackup` resource:

```bash theme={"system"}
kubectl get cwdbbackup [BACKUP-NAME] --namespace [NAMESPACE]
```

### What to check

1. **Confirm the source database is `Ready`:** an on-demand backup can't start if the database is unhealthy.

2. **Check the backup status detail:**

   ```bash theme={"system"}
   kubectl describe cwdbbackup [BACKUP-NAME] --namespace [NAMESPACE]
   ```

   Look for events such as `BackupFailed` or quota errors.

3. **Check whether you're over the on-demand backup quota for the database.** Delete unneeded backups, or contact your CoreWeave account team to raise the quota.

## Restore takes too long

### Symptom

A new `CWDBCluster` created with `spec.postgres.restore` set stays in `Provisioning` for much longer than expected.

### Notes

* Restore time scales with database size and the write-ahead log (WAL) replay distance from the base backup. A small database restored from a recent base backup completes quickly. Restoring a multi-TiB database from older base backups can take hours.
* The new database only becomes `Ready` after the bootstrap completes. Don't cut application traffic over until the new `CWDBCluster` reports `Ready`.
* If a restore appears stuck (no progress for more than 30 minutes for a small database), escalate through your customer Slack channel with the new database name, the `spec.postgres.restore.sourceClusterName`, and namespace.

## Pods aren't spread across distinct nodes

### Symptom

The pod listing shows two or more instances on the same node:

```bash theme={"system"}
kubectl get pods --namespace [NAMESPACE] -l cnpg.io/cluster=[CLUSTER-NAME] -o wide
```

### Common causes

* You added a custom `spec.affinity` block that turned off the default anti-affinity rules.
* The CKS cluster doesn't have enough CPU nodes for all instances. The scheduler falls back to co-locating pods when no spread is possible.

### Fix

Either remove the custom affinity override and let the operator manage scheduling, or add CPU node capacity so the scheduler can place each instance on a distinct node. The default rules use "preferred" anti-affinity (not "required") to avoid blocking provisioning, but on a CKS cluster with enough capacity you should see one instance per node.

## Known issues

These are known limitations in the current limited availability release. They don't require any action from you and are tracked for resolution.

### Database size doesn't appear in the Cloud Console immediately after creation

For some time after you create a database, the **Size** column on the Cloud Console **Databases** list may not reflect the database's actual size. This is display-only. The database itself is healthy, your storage is provisioned at the size you requested, and applications can read and write normally.

## Escalate an issue

If the steps on this page don't resolve your issue, contact CoreWeave through your customer Slack channel with:

* The database name and namespace.
* The full output of `kubectl describe cwdbcluster [CLUSTER-NAME] --namespace [NAMESPACE]`.
* Relevant pod or backup status: `kubectl get pods,cwdbbackup --namespace [NAMESPACE]`.
* A short description of what you expected to happen and what happened instead.

During limited availability, the CWDB team aims to triage issues within one business day.
