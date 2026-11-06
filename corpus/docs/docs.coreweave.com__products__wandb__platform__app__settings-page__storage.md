# Manage storage

Source: https://docs.coreweave.com/products/wandb/platform/app/settings-page/storage

> Manage Weights & Biases data storage consumption using reference artifacts, external buckets, and TTL deletion policies.

# Manage storage

This page describes how to manage your Weights & Biases data storage so you can stay within your storage limit. If you're approaching or exceeding your storage limit, you have multiple ways to manage your data. The best option depends on your account type and your current project setup.

## Manage storage consumption

To reduce how much storage your account uses, Weights & Biases offers different methods of optimizing your storage consumption:

* Use [reference artifacts](https://docs.coreweave.com/products/wandb/artifacts/track-external-files.md) to track files saved outside the Weights & Biases system instead of uploading them to Weights & Biases storage.
* Use an [external cloud storage bucket](https://docs.coreweave.com/products/wandb/platform/app/settings-page/teams.md) for storage (Enterprise only).

## Delete data

If optimizing consumption isn't sufficient, you can also choose to delete data to remain under your storage limit. You have several ways to do this:

* Delete data interactively with the app UI.
* [Set a TTL policy](https://docs.coreweave.com/products/wandb/artifacts/ttl.md) on artifacts so Weights & Biases deletes them automatically.
