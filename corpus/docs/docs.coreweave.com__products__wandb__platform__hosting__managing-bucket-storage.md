# Manage bucket storage and costs

Source: https://docs.coreweave.com/products/wandb/platform/hosting/managing-bucket-storage

# Manage bucket storage and costs

> Learn how Weights & Biases uses object storage, how deletion affects bucket bytes, and how to reduce usage and costs.

When you use [Bring your own bucket (BYOB)](https://docs.coreweave.com/products/wandb/platform/hosting/data-security/secure-storage-connector.md), [W\&B Dedicated Cloud](https://docs.coreweave.com/products/wandb/platform/hosting/hosting-options/dedicated-cloud.md), or [W\&B Self-Managed](https://docs.coreweave.com/products/wandb/platform/hosting/hosting-options/self-managed.md), your team often pays cloud storage providers directly. This page explains what occupies your bucket, how Weights & Biases removes objects after deletion in the app or API, and what you should expect. Use it to understand bucket usage, plan cleanup, and set realistic expectations for when storage is reclaimed.

This page is intended for organization administrators and operators who manage object storage for Self-Managed or Dedicated Cloud deployments.

## What uses bucket space

Weights & Biases stores several categories of data in your configured object storage. The [BYOB overview](https://docs.coreweave.com/products/wandb/platform/hosting/data-security/secure-storage-connector.md#data-stored-in-the-central-database-vs-buckets) lists examples, including experiment files and metrics, artifact files, media files, run files, and exported history in Parquet form. Together these drive bucket size and cost.

## How Weights & Biases removes data from storage

Deletion in the W\&B App or [Public API](https://docs.coreweave.com/products/wandb/ref/python/public-api/api.md) updates Weights & Biases metadata first. Removing a run, artifact, or file from the product doesn't guarantee an immediate drop in reported bucket usage. Object storage cleanup runs as background work that can lag, especially on busy instances.

### Artifacts

Deleted artifacts are soft-deleted, then processed by artifact garbage collection. Self-managed deployments must set `GORILLA_ARTIFACT_GC_ENABLED` and meet provider requirements such as versioning or soft delete. See [Delete an artifact](https://docs.coreweave.com/products/wandb/artifacts/delete-artifacts.md) and [Configure environment variables](https://docs.coreweave.com/products/wandb/platform/hosting/env-vars.md).

### Run data and run files

After runs or run-associated files are deleted, permanent removal of the underlying stored objects is controlled separately from artifacts. On Dedicated Cloud and Self-Managed deployments, `GORILLA_DATA_RETENTION_PERIOD` sets how long deleted run data is retained before it can be removed from storage. This setting does not delete artifacts. See [Configure environment variables](https://docs.coreweave.com/products/wandb/platform/hosting/env-vars.md), [Data retention policy](https://docs.coreweave.com/products/wandb/platform/hosting/hosting-options/dedicated-cloud.md#data-retention-policy) for Dedicated Cloud, and [Delete runs](https://docs.coreweave.com/products/wandb/runs/delete-runs.md#when-deleted-run-data-is-removed-from-storage) for how run and file deletion relates to storage.

## What to expect from background cleanup

Garbage collection and related jobs that free object storage run without timing guarantees. Weights & Biases does not guarantee that a given object disappears from your bucket within a specific time after you delete content in the UI or API. For projects with a large number of files per run, such as when logging many media files per run, expect longer delays before storage usage is released.

Monitor your bucket in your cloud provider and contact [Support](mailto:forge-support@coreweave.com) or your account team if cleanup appears stuck.

## Reduce bucket usage

This section describes the recommended order of operations for freeing space in your bucket, starting with safe product flows and ending with direct bucket operations that require more care.

Use supported product flows first:

* [Delete runs in the W\&B App](https://docs.coreweave.com/products/wandb/runs/delete-runs.md#ui) or [with Python](https://docs.coreweave.com/products/wandb/runs/delete-runs.md#python) when you no longer need them.
* [Delete artifacts](https://docs.coreweave.com/products/wandb/artifacts/delete-artifacts.md) you no longer need, and use [Artifact TTL](https://docs.coreweave.com/products/wandb/artifacts/ttl.md) where it fits your workflow.

If you must reclaim space immediately, operators with access to the bucket may delete specific object keys directly in cloud storage.

> [!WARNING]
>
> Deleting object keys directly in your bucket bypasses Weights & Biases and can cause data loss or break access for the app. Review the following before you proceed:
>
> * Objects you remove are **no longer available to download** through Weights & Biases.
> * You should delete **only** keys you intend to remove. Incorrect deletes can break access to data the app still references.
> * If your bucket uses **object versioning** or **provider soft delete** (for example on Google Cloud Storage), storage charges can persist until non-current versions or soft-deleted objects expire under your cloud lifecycle rules.

For high-level usage in W\&B Multi-tenant Cloud, organization admins can review storage-related usage from organization settings. See [Billing settings](https://docs.coreweave.com/products/wandb/platform/app/settings-page/billing-settings.md).

## Troubleshooting

If deletions don't appear correctly in the W\&B App after you use the Public API, upgrade the W\&B Python SDK to a current release and retry. Large per-run file counts can increase how long background cleanup takes across the instance.

For scripted cleanup patterns that match your deployment, contact [Support](mailto:forge-support@coreweave.com) or your account team.

## Related documentation

For more information, see the following resources:

* [Delete runs](https://docs.coreweave.com/products/wandb/runs/delete-runs.md#delete-runs)
* [Delete an artifact](https://docs.coreweave.com/products/wandb/artifacts/delete-artifacts.md)
* [Configure environment variables](https://docs.coreweave.com/products/wandb/platform/hosting/env-vars.md)
* [Bring your own bucket (BYOB)](https://docs.coreweave.com/products/wandb/platform/hosting/data-security/secure-storage-connector.md)
