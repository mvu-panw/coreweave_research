# Manage backups

Source: https://docs.coreweave.com/products/storage/cwdb/backups

# Manage backups

> How automatic backups work, taking on-demand backups, and restoring into a new database

CoreWeave Database (CWDB) protects every database with automatic, scheduled backups by default. You don't configure storage credentials, choose a location, or set up a schedule. The operator handles all of that against CoreWeave-managed storage.

Scheduled backups run automatically against every database. Create a `CWDBBackup` resource when you want an explicit on-demand recovery point. Restores always provision a new database. CWDB doesn't modify the source database.

This page explains how automatic backups work, how to take on-demand backups, and how to restore from a backup into a new database.

## How automatic backups work

For every database, the operator runs two coordinated backup streams against CoreWeave-managed object storage:

* **Daily base backups** of the entire database, retained for 7 days. The schedule is configurable. See [Customize the backup schedule](#customize-the-backup-schedule).
* **Continuous write-ahead log (WAL) archiving**, which streams every change to backup storage to keep base backups consistent and to support restores.

These scheduled backups let you restore the database from an available base backup, or recover to a point in time for which a successful scheduled base backup and the required archived WAL are available. See [Restore to a point in time](#restore-to-a-point-in-time).

CWDB encrypts backups at rest using a CoreWeave-managed key. CoreWeave handles lifecycle, credentials, and access policies for backup storage. You don't see or manage backup storage directly.

## Customize the backup schedule

To run base backups on a different cadence, set `spec.postgres.backupSchedule` on the `CWDBCluster` manifest to a cron expression. By default, CWDB takes one base backup per database per day at midnight (equivalent to a `0 0 0 * * *` cron expression). The following example schedules base backups every two hours, at the 15-minute mark:

```yaml theme={"system"}
spec:
  postgres:
    instances: 3
    backupSchedule: "0 15 */2 * * *"
```

The operator evaluates schedules in the cluster's local time zone, which corresponds to the region the cluster runs in. For example, `0 0 6 * * *` triggers a backup at 6 AM in the cluster's region, not at 6 AM UTC. You can change `backupSchedule` after the database is created. The operator applies the new cadence on the next reconcile.

CWDB uses the [CNPG backup schedule format](https://cloudnative-pg.io/docs/1.28/backup/#cron-schedule), which is a six-field cron expression. The first field is **seconds**, not minutes. This differs from the more common five-field Unix cron format:

```text theme={"system"}
<seconds> <minutes> <hours> <day-of-month> <month> <day-of-week>
```

The following table shows common schedule expressions:

| Expression | Schedule |
| - | - |
| `0 0 0 * * *` | Every day at midnight (equivalent to the default). |
| `0 15 */2 * * *` | Every two hours, at the 15-minute mark. |
| `@daily`, `@midnight` | Every day at midnight (equivalent to the default). |
| `@hourly` | Every hour. |

For the full set of supported expressions and predefined schedules, see the [robfig/cron documentation](https://pkg.go.dev/github.com/robfig/cron#hdr-CRON_Expression_Format), the underlying parser CNPG uses.

The following table describes the field:

| Field | Required | Description |
| - | - | - |
| `spec.postgres.backupSchedule` | No | Six-field cron expression that controls how often base backups run. Defaults to daily at midnight (`0 0 0 * * *`). |

Retention is fixed at 7 days regardless of cadence. More frequent base backups produce more recovery points within the same 7-day window, not a longer backup history. For most workloads, daily base backups are sufficient. Schedule more frequent base backups only when you have a recovery-point objective the default cadence doesn't meet. Continuous WAL archiving already covers the gap between base backups for restores.

## Opt out of managed backups

Managed backups are on by default for every database. To opt out, set `spec.postgres.disableManagedBackups: true` on the manifest. The CoreWeave Cloud Console exposes this as the **Enable backups** toggle in the **Create database** form (see [Create a database](https://docs.coreweave.com/products/storage/cwdb/create.md#advanced)).

| Field | Required | Description |
| - | - | - |
| `spec.postgres.disableManagedBackups` | No | When `true`, opts the database out of CWDB managed backups. No scheduled base backups or WAL archives are produced, and managed restores aren't available for the database. Defaults to `false`. |

> [!WARNING]
>
> Disabling managed backups means the database has no recovery point. Only opt out if you have another backup strategy.

## View backup status

The Cloud Console lists every backup for a database. On-demand backups are also visible with `kubectl` as `CWDBBackup` resources.

### View backups from the Cloud Console

The Cloud Console exposes a **Backups** tab on each database's details panel. The tab lists every available backup for the database, including scheduled base backups and on-demand backups. It's also the entry point for the **Take backup** and **Restore** actions described later on this page.

To open the **Backups** tab, follow these steps:

1. In the [Cloud Console](https://console.coreweave.com/), open **Infrastructure > Data and storage** and select the **Databases** tab.
2. Open the Backups tab in one of two ways:

   * Click the database row to open the details view, then click the **Backups** tab alongside **Details** and **YAML**.
   * In the row's three-dot menu, select **Manage backups**.

   Both open the same panel.

Each entry in the list shows the time the backup was taken, a `Scheduled` or `On-demand` badge, the compressed size, and the backup ID. Entries are grouped by day and sorted from newest to oldest. To copy a backup ID, click the copy icon next to it. When you [restore from a specific backup](#restore-from-a-specific-backup) with `kubectl`, pass this value to `spec.postgres.restore.backupID`.

The search field above the list accepts free-text matches against backup IDs and supports filtering by field. To list only one backup type, enter `type:scheduled` or `type:on-demand` in the search field.

### View backups with kubectl

On-demand backups are `CWDBBackup` resources. To list them, see [List on-demand backups](#list-on-demand-backups). Each one reports its backup ID in `status.backupID`, the value you pass to `spec.postgres.restore.backupID` when you [restore from a specific backup](#restore-from-a-specific-backup).

To find the backup ID of a scheduled backup, use the [Backups tab in the Cloud Console](#view-backups-from-the-cloud-console).

## Create an on-demand backup

An on-demand backup is an explicit recovery point that you create outside the daily schedule. Use one before any operation you want a precise rollback point for: major version upgrades, schema migrations, large data imports, or one-off batch jobs.

You can take an on-demand backup from the Cloud Console or by applying a `CWDBBackup` resource with `kubectl`. Both methods create the same `CWDBBackup` resource and count against the [on-demand backup quotas](#on-demand-backup-quotas).

### Create from the Cloud Console

To take an on-demand backup from the Cloud Console, follow these steps:

1. [Open the Backups tab](#view-backups-from-the-cloud-console) for the database.
2. At the top right of the **Backups** tab, click **Take backup**.

The Console submits a `CWDBBackup` resource with an auto-generated name and shows a `Backup started` notification. The backup appears at the top of the list under **Today** with an `On-demand` badge as soon as the operator picks it up, and the size column updates from `-` to the compressed size when the backup completes.

The Cloud Console doesn't let you set the `CWDBBackup` resource name. When you need a specific resource name (for example, to reference the backup from a GitOps manifest or an automated rollback procedure), use the [kubectl flow](#create-with-kubectl).

### Create with kubectl

Create an on-demand backup with a `CWDBBackup` resource. Save the following manifest as `cwdb_backup.yaml`. Replace `[BACKUP-NAME]` with a name for this backup and `[CLUSTER-NAME]` with your database name:

```yaml title="cwdb_backup.yaml" theme={"system"}
apiVersion: data.coreweave.com/v1
kind: CWDBBackup
metadata:
  name: [BACKUP-NAME]
spec:
  clusterName: [CLUSTER-NAME]
```

The `CWDBBackup` spec is intentionally minimal. The operator resolves the backup destination from the referenced database's configuration. You never specify object storage details for on-demand backups.

| Field | Required | Description |
| - | - | - |
| `metadata.name` | Yes | Name of the on-demand backup resource. |
| `spec.clusterName` | Yes | Name of the `CWDBCluster` to back up. Must exist in the same namespace. |

Apply it to the same namespace as the database:

```bash theme={"system"}
kubectl apply -f cwdb_backup.yaml --namespace [NAMESPACE]
```

Poll the resource to track the backup as it progresses through `Pending`, `Running`, and `Succeeded` phases. A failed backup transitions to `Failed`:

```bash theme={"system"}
kubectl get cwdbbackup [BACKUP-NAME] --namespace [NAMESPACE] -o yaml
```

After it reports `Succeeded`, the recovery point is durable in backup storage. The `status.backupID` field is the identifier you pass to `spec.postgres.restore.backupID` when you restore from this specific backup.

## On-demand backup status fields

The `CWDBBackup.status` exposes the following fields:

| Field | Description |
| - | - |
| `phase` | `Pending`, `Running`, `Succeeded`, or `Failed`. |
| `startTime` | When the backup operation started. |
| `completionTime` | When the backup operation completed. |
| `backupID` | Composite identifier formatted `<lifecycle-ts>-<barman-id>`. Pass this to `spec.postgres.restore.backupID` to restore from this specific backup. |
| `compressedSizeBytes` | Compressed footprint in object storage. Counted against the 10 TB per-database on-demand quota. |
| `actualSizeBytes` | Uncompressed database size at backup time, parsed from the underlying backup metadata. Used by restores to size destination volumes. |
| `error` | Populated only when `phase` is `Failed`. |

## List on-demand backups

To see all on-demand backups in a namespace and their current status, run:

```bash theme={"system"}
kubectl get cwdbbackup --namespace [NAMESPACE]
```

You should see output similar to the following:

```text title="Example output" theme={"system"}
NAME                       CLUSTER   STATUS      AGE
my-db-before-migration     my-db     Succeeded   1h
my-db-pre-v15-upgrade      my-db     Succeeded   2d
```

## On-demand backup quotas

Each database has the following quotas on `CWDBBackup` resources:

* **Maximum 50 on-demand backups per database.**
* **Maximum 10 TB cumulative compressed size per database**, summed from `status.compressedSizeBytes` across all `Succeeded` backups.

The operator rejects new `CWDBBackup` resources with `phase=Failed` if either quota would be exceeded. On-demand backups aren't subject to the 7-day scheduled-backup retention. They persist until you delete them or until a quota cap is hit.

If your workload needs higher quotas (for example, to keep monthly recovery points for compliance), contact your CoreWeave account team.

## Delete an on-demand backup

To permanently remove an on-demand backup and free its slot against the per-database quota, run:

```bash theme={"system"}
kubectl delete cwdbbackup [BACKUP-NAME] --namespace [NAMESPACE]
```

The operator runs a deletion finalizer that removes the backup data from object storage and updates the backup registry before the `CWDBBackup` resource is removed. Deletion is irreversible. If you may need the recovery point, restore from it into a new database before deleting.

## Restore from a backup

A restore in CWDB creates a new database from a previously captured backup. There's no separate restore resource. You create a new `CWDBCluster` and set `spec.postgres.restore` to point at the source database and, optionally, a specific backup. The operator bootstraps the new database from the chosen backup as part of its normal provisioning lifecycle.

Restores always create a new database. CWDB doesn't support in-place rollback of an existing database. Common use cases include:

* Recovering after data loss or corruption.
* Cloning a production database into a sandbox for testing.
* Validating a backup before relying on it.
* Migrating to a new database after a major version upgrade or topology change.

You can restore from the Cloud Console or with `kubectl`. The Console restore flow is a quick path for a one-off recovery from an existing backup. Use `kubectl` when you need to script the restore, [recover to a specific point in time](#restore-to-a-point-in-time), [resize storage during the restore](#resize-storage-during-restore), or restore from user-managed object storage with `spec.postgres.restoreObjectStore`.

### Restore from the Cloud Console

To restore from a specific backup using the Cloud Console, follow these steps:

1. [Open the Backups tab](#view-backups-from-the-cloud-console) for the source database.
2. Locate the backup you want to restore from. Use the `type:scheduled` or `type:on-demand` filter to narrow the list.
3. On the backup row, click **Restore**. The Console opens a **Restore from backup** panel.
4. Review the **Backup** and **Configuration** summaries (described in the following section) and edit **New database name** if you want a name other than the pre-filled default.
5. Click **Restore to new database**.

The **Restore from backup** panel summarizes the restore in three sections:

* **Backup** identifies the source database, the timestamp the backup was taken, its type (`Scheduled` or `On-demand`), its compressed size, and its backup ID.
* **Configuration** shows the compute and storage settings the new database inherits from the source. The Console restore flow doesn't let you change these before provisioning. If the backup is much smaller than the inherited storage size, the panel surfaces a note that you can increase storage after provisioning.
* **New database name** is the name of the new `CWDBCluster`. The Console pre-fills `[SOURCE-NAME]-restore-[YYYYMMDD]-[HHMM]`. Edit it to give the restored database a different name.

The Console submits a new `CWDBCluster` with `spec.postgres.restore.sourceClusterName` set to the source database and `spec.postgres.restore.backupID` set to the selected backup's ID. The new database appears in the **Databases** list with a `Provisioning` status and transitions to `Ready` once the operator has bootstrapped Postgres from the backup. The source database keeps running unchanged.

After the restored database reaches `Ready`, you can point your application at the new database, run both side by side, or delete either one. For the cut-over steps, see [Cut over to the restored database](#cut-over-to-the-restored-database).

> [!NOTE]
>
> A restore always provisions the new database in the same namespace as the source, whether you use the Cloud Console or `kubectl`. Cross-namespace restore isn't supported in limited availability.

### Restore from the latest scheduled backup

The minimum required field is `spec.postgres.restore.sourceClusterName`. When `backupID` is omitted, the operator restores from the latest entry in the source's scheduled backup history.

Save the following manifest as `cwdb_restore.yaml`. Replace `[SOURCE-CLUSTER-NAME]` with the source database name and `[NEW-CLUSTER-NAME]` with a name for the new database:

```yaml title="cwdb_restore.yaml" theme={"system"}
apiVersion: data.coreweave.com/v1
kind: CWDBCluster
metadata:
  name: [NEW-CLUSTER-NAME]
spec:
  type: postgres
  postgres:
    instances: 3
    dbName: app
    owner: app
    restore:
      sourceClusterName: [SOURCE-CLUSTER-NAME]
  storage:
    resources:
      requests:
        storage: 25Gi
```

Apply the manifest to the same namespace as the source database:

```bash theme={"system"}
kubectl apply -f cwdb_restore.yaml --namespace [NAMESPACE]
```

### Restore from a specific backup

To restore from a specific backup (for example, the on-demand backup you took before a schema migration), set `spec.postgres.restore.backupID` to the composite identifier of that backup:

```yaml title="cwdb_restore.yaml" theme={"system"}
apiVersion: data.coreweave.com/v1
kind: CWDBCluster
metadata:
  name: [NEW-CLUSTER-NAME]
spec:
  type: postgres
  postgres:
    instances: 3
    dbName: app
    owner: app
    restore:
      sourceClusterName: [SOURCE-CLUSTER-NAME]
      backupID: "20260318T153042-20260330T140000"
  storage:
    resources:
      requests:
        storage: 25Gi
```

Find available backup IDs in either of the following places:

* The `status.backupID` field on a `CWDBBackup` resource, for on-demand backups.
* The **Backups** tab for the source database in the Cloud Console, which lists both scheduled and on-demand backups.

### Restore to a point in time

Point-in-time recovery (PITR) restores the source database's state as of a timestamp you choose. Set `spec.postgres.restore.pitr.timestamp` to an RFC 3339 timestamp. The operator replays the WAL up to that moment, then stops. Use PITR to recover to the moment just before a bad migration, an accidental `DELETE`, or any other change you want to exclude from the restored database.

PITR recovers the state between backups because continuous WAL archiving covers the gap. A restore with a specific `backupID` recovers the state captured by that backup. If you omit both `backupID` and `pitr.timestamp`, recovery replays the available WAL from the latest scheduled backup.

You don't choose a backup for a PITR restore. The operator selects the most recent successful scheduled backup that completed at or before your timestamp and replays WAL forward from there. Setting `backupID` alongside `pitr.timestamp` is rejected with `only one of spec.postgres.restore.backupID and spec.postgres.restore.pitr.timestamp may be specified, not both`.

Save the following manifest as `cwdb_pitr_restore.yaml`. Replace `[SOURCE-CLUSTER-NAME]` with the source database name, `[NEW-CLUSTER-NAME]` with a name for the new database, and the timestamp with your recovery target:

```yaml title="cwdb_pitr_restore.yaml" theme={"system"}
apiVersion: data.coreweave.com/v1
kind: CWDBCluster
metadata:
  name: [NEW-CLUSTER-NAME]
spec:
  type: postgres
  postgres:
    instances: 3
    dbName: app
    owner: app
    restore:
      sourceClusterName: [SOURCE-CLUSTER-NAME]
      pitr:
        timestamp: "2026-08-20T20:41:00Z"
  storage:
    resources:
      requests:
        storage: 25Gi
```

Apply the manifest to the same namespace as the source database:

```bash theme={"system"}
kubectl apply -f cwdb_pitr_restore.yaml --namespace [NAMESPACE]
```

Track the new database to `Ready` the same way as any other restore. See [Monitor the restore](#monitor-the-restore).

PITR isn't available in the Cloud Console restore flow. Use `kubectl` to recover to a specific point in time.

#### Choose a valid point-in-time recovery timestamp

A PITR timestamp can't be in the future, and a successful scheduled backup must have completed at or before it. The required WAL must also be available in backup storage. If the target is newer than the latest archived WAL, the restored database can't finish bootstrapping and won't reach `Ready`. The operator rejects a future timestamp with `PITR timestamp cannot be in the future`. CWDB retains scheduled backups for 7 days, so the completion time of the oldest successful scheduled backup still available bounds the oldest recovery target. On-demand backups aren't candidates for the PITR base backup. When an existing backup history has no qualifying scheduled backup, the restore fails with an error naming the recovery time:

```text title="Example output" theme={"system"}
no scheduled backup exists for cluster [NAMESPACE]/[SOURCE-CLUSTER-NAME] prior to recovery time 2026-08-20T20:41:00Z
```

To see which scheduled backups are available and when each was taken, open the **Backups** tab for the source database. See [View backups from the Cloud Console](#view-backups-from-the-cloud-console).

### Resize storage during restore

When you restore with `kubectl`, you can set the new database's `spec.storage.resources.requests.storage` to a different value than the source. The new database is sized according to its own manifest. The source's storage size doesn't carry over. Pick a size that comfortably exceeds `CWDBBackup.status.actualSizeBytes` for the backup you're restoring from.

Resizing during restore isn't available in the Cloud Console restore flow. Use `kubectl` when you need different storage sizing on the restored database.

### Restore after deleting the source database

You can restore even after the source database has been deleted. CWDB keeps backup history in a registry independent of the source database's lifecycle. Set `sourceClusterName` to the deleted database's name and the operator looks up its backup history.

The new database can reuse the deleted source's name. The operator allocates a fresh lifecycle context, so there's no collision with the source's backup data.

### CWDBCluster restore fields

The following fields on a new `CWDBCluster` control restore behavior:

| Field | Required | Description |
| - | - | - |
| `spec.postgres.restore.sourceClusterName` | Yes | Name of the source database whose backups to restore from. Must exist in the backup registry. The source `CWDBCluster` may or may not still exist. |
| `spec.postgres.restore.backupID` | No | Composite identifier of a specific backup, formatted `<lifecycle-ts>-<barman-id>`. If both `backupID` and `pitr.timestamp` are omitted, the operator recovers from the latest available scheduled backup and replays the available WAL. Mutually exclusive with `spec.postgres.restore.pitr.timestamp`. |
| `spec.postgres.restore.pitr.timestamp` | No | RFC 3339 timestamp to recover the source database's state to. The operator picks the base backup for you. Must be in the past and covered by archived WAL, and a successful scheduled backup must have completed at or before it. Mutually exclusive with `spec.postgres.restore.backupID`. |
| `spec.postgres.restoreObjectStore` | No | Alternative restore path. Provides full object storage configuration (bucket, endpoint, and credentials Secret) for restoring from user-managed backup storage. Mutually exclusive with `spec.postgres.restore`. |

`spec.postgres.restore` is a one-time bootstrap instruction. After the new database reaches `Ready`, the operator doesn't re-process the field on subsequent reconciles.

### Monitor the restore

The new `CWDBCluster` goes through its normal provisioning lifecycle. Track progress with:

```bash theme={"system"}
kubectl get cwdbcluster [NEW-CLUSTER-NAME] --namespace [NAMESPACE]
```

The cluster reports `Provisioning` while the operator bootstraps from the backup, then transitions to `Ready` once the database is online. Wait for `Ready` before cutting traffic over:

```bash theme={"system"}
kubectl wait --for=condition=Ready cwdbcluster [NEW-CLUSTER-NAME] \
  --namespace [NAMESPACE] \
  --timeout=600s
```

Large databases take proportionally longer to bootstrap. Plan your recovery time objective accordingly.

### Cut over to the restored database

After the restored database is `Ready`:

1. **Validate the data.** Run application-level checks against the new database to confirm the expected recovery point.
2. **Update connection strings.** Point your application at the new database's pooler Service (`[NEW-CLUSTER-NAME]-pooler-rw`). The credentials Secret is named `[NEW-CLUSTER-NAME]-[DBNAME]-credentials`. For the default `dbName: app`, that resolves to `[NEW-CLUSTER-NAME]-app-credentials`. Use `[NEW-CLUSTER-NAME]-[DBNAME]-credentials-ro` to route read-only traffic to replicas.
3. **Cut over traffic.** Deploy the updated configuration and drain connections from the old database.
4. **Optional: Retire the source database.** The source database is untouched by the restore. Keep it until you have confidence in the restored data, then delete it explicitly.

> [!WARNING]
>
> A restore doesn't modify or pause the source database. Writes to the source database after the restore starts won't appear in the restored database. If you need the two databases to align, plan a maintenance window or quiesce writes before you restore.
