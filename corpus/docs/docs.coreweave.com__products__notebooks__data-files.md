# Work with data files

Source: https://docs.coreweave.com/products/notebooks/data-files

# Work with data files

Use the notebook sidebar to manage files in the notebook sandbox and connect to remote data sources. You can also download [W\&B Artifacts](https://docs.coreweave.com/products/wandb/artifacts/download-and-use-an-artifact.md) into the notebook.

## Notebook storage and persistence

Each notebook runs in a temporary sandbox provided by [CoreWeave Sandboxes](https://docs.coreweave.com/products/sandboxes.md). Files that you create, upload, or download appear under **Files** in the notebook sidebar and exist only in the sandbox.

Connected object storage, databases, and data catalogs appear under **Remote storage**.

> [!WARNING]
>
> Files in the notebook sandbox are temporary. Copy files that you want to keep to persistent storage before the sandbox is reset or deleted.

## View files

To view files in the notebook sidebar:

1. In the notebook sidebar, select **View files** ().
2. Expand one of the following sections:
   * **Files** to view files in the notebook sandbox.
   * **Remote storage** to browse connected remote data sources.

## Manage files and folders

To upload or create a file or folder:

1. In the notebook sidebar, select **View files** ().
2. Expand **Files**.
3. Select one of the following actions:
   * **Upload file** () to upload an existing file to the sandbox.
   * **Add file** () to create a file.
   * **Add folder** () to create a folder.

## Download a W\&B Artifact

You can [download and use a W\&B Artifact](https://docs.coreweave.com/products/wandb/artifacts/download-and-use-an-artifact.md) in a notebook. The downloaded files are stored in the notebook sandbox.

For example, the following code downloads a model Artifact from Registry:

```python theme={"system"}
import wandb

REGISTRY_NAME = "Zoo"
MODEL_COLLECTION_NAME = "Classifier_Models"
MODEL_VERSION = 0

artifact_name = (
    f"wandb-registry-{REGISTRY_NAME}/"
    f"{MODEL_COLLECTION_NAME}:v{MODEL_VERSION}"
)

with wandb.init() as run:
    artifact = run.use_artifact(artifact_name)
    artifact_path = artifact.download()
    print(artifact_path)
```

The command returns the path to the downloaded Artifact directory. For example:

```text theme={"system"}
/workspace/artifacts/zoo-pznwefqb:v0
```

The downloaded Artifact appears in the `artifacts` directory:

**artifacts**

**zoo-pznwefqb:v0**

**zoo\_wandb.pth**

**wandb**

**latest-run**

**files**

**config.yaml**

**debug.log**

**notebook.py**
