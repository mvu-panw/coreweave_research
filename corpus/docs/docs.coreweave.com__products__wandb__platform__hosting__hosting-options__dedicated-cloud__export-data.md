# Export data from Dedicated Cloud

Source: https://docs.coreweave.com/products/wandb/platform/hosting/hosting-options/dedicated-cloud/export-data

> Export runs, metrics, artifacts, and reports from a W&B Dedicated Cloud instance using the Python SDK API.

# Export data from Dedicated Cloud

Export the data managed in your W\&B Dedicated Cloud instance, such as runs, metrics, artifacts, and reports, when you need a portable copy for backup, migration, or external analysis. To extract this data, use the W\&B SDK API with the [Import and Export API](https://docs.coreweave.com/products/wandb/ref/python/public-api.md). The following table covers some key export use cases.

| Purpose | Documentation |
| - | - |
| Export project metadata | [Projects API](https://docs.coreweave.com/products/wandb/ref/python/public-api/projects.md) |
| Export runs in a project | [Runs API](https://docs.coreweave.com/products/wandb/ref/python/public-api/runs.md) |
| Export reports | [Report and Workspace API](https://docs.coreweave.com/products/wandb/reports/clone-and-export-reports.md) |
| Export artifacts | [Explore artifact graphs](https://docs.coreweave.com/products/wandb/artifacts/explore-and-traverse-an-artifact-graph.md), [Download and use artifacts](https://docs.coreweave.com/products/wandb/artifacts/download-and-use-an-artifact.md#download-and-use-an-artifact-stored-on-wb) |

If you manage artifacts stored in the Dedicated Cloud with [Secure Storage Connector](https://docs.coreweave.com/products/wandb/platform/app/settings-page/teams.md#secure-storage-connector), you might not need to export the artifacts using the W\&B SDK API.

> [!NOTE]
>
> Using the W\&B SDK API to export all of your data can be slow if you have many runs, artifacts, and similar resources. Weights & Biases recommends running the export process in appropriately sized batches to avoid overwhelming your Dedicated Cloud instance.
