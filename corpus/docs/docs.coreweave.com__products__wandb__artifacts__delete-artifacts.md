# Delete an artifact

Source: https://docs.coreweave.com/products/wandb/artifacts/delete-artifacts

> Delete artifacts interactively with the App UI or programmatically with the W&B Python SDK.

# Delete an artifact

Delete artifacts interactively with the W\&B App or programmatically with the W\&B Python SDK. When you delete an artifact, Weights & Biases marks that artifact as a *soft-delete*. In other words, the artifact is marked for deletion but files are not immediately deleted from storage.

The contents of the artifact remain as a soft-delete, or pending deletion state, until a regularly run garbage collection process reviews all artifacts marked for deletion. The garbage collection process deletes associated files from storage if the artifact and its associated files are not used by a previous or subsequent artifact versions.

> [!NOTE]
>
> Garbage collection is **best-effort**. Weights & Biases does not guarantee how quickly freed space appears in your object storage after you delete an artifact. Large deployments or backlogs can take longer than expected. For how this fits with run data, retention settings, and optional operator actions, see [Manage bucket storage and costs](https://docs.coreweave.com/products/wandb/platform/hosting/managing-bucket-storage.md).

## Artifact garbage collection workflow

The following diagram illustrates the complete artifact garbage collection process:

```mermaid theme={"system"}
graph TB
    Start([Artifact Deletion Initiated]) --> DeleteMethod{Deletion Method}
    
    DeleteMethod -->|UI| UIDelete[Delete via W&B App]
    DeleteMethod -->|SDK| SDKDelete[Delete via W&B Python SDK]
    DeleteMethod -->|TTL| TTLDelete[TTL Policy Expires]
    
    UIDelete --> SoftDelete[Artifact Marked as<br/>'Soft Delete']
    SDKDelete --> SoftDelete
    TTLDelete --> SoftDelete
    
    SoftDelete --> GCWait[(Wait for<br/>best-effort<br/>Garbage Collection)]
    
    GCWait --> GCRun[Garbage Collection<br/>Process Runs<br/><br/>- Reviews all soft-deleted artifacts<br/>- Checks file dependencies]
    
    GCRun --> CheckUsage{Are files used by<br/>other artifact versions?}
    
    CheckUsage -->|Yes| KeepFiles[Files Kept in Storage<br/><br/>- Artifact marked deleted<br/>- Files remain for other versions]
    CheckUsage -->|No| DeleteFiles[Files Deleted from Storage<br/><br/>- Artifact fully removed<br/>- Storage space reclaimed]
    
    KeepFiles --> End([End])
    DeleteFiles --> End
    
    style Start fill:#e1f5fe,stroke:#333,stroke-width:2px,color:#000
    style SoftDelete fill:#fff3e0,stroke:#333,stroke-width:2px,color:#000
    style GCRun fill:#f3e5f5,stroke:#333,stroke-width:2px,color:#000
    style KeepFiles fill:#e8f5e9,stroke:#333,stroke-width:2px,color:#000
    style DeleteFiles fill:#ffebee,stroke:#333,stroke-width:2px,color:#000
    style End fill:#e0e0e0,stroke:#333,stroke-width:2px,color:#000
```

You can schedule when artifacts are deleted from Weights & Biases with TTL policies. For more information, see [Manage data retention with Artifact TTL policy](https://docs.coreweave.com/products/wandb/artifacts/ttl.md).

> [!NOTE]
>
> Artifacts deleted by a TTL policy, the W\&B Python SDK, or the W\&B App are first soft-deleted. Soft-deleted artifacts are then garbage-collected before they are permanently deleted.

> [!NOTE]
>
> Deleting an entity, project, or artifact collection triggers the artifact deletion process described on this page. When you delete a run and choose to delete its associated artifacts, those artifacts follow the same soft-delete and garbage collection workflow.

## Delete an artifact version

Delete an artifact version interactively with the W\&B App or programmatically with the W\&B Python SDK.

> [tab] W\&B App
>
> To delete an artifact version:
>
> 1. Navigate to the project that contains the artifact version you want to delete.
> 2. Select the **Artifacts** tab.
> 3. From the list of artifact types, select the type of artifact that contains the version you want to delete.
> 4. Click the **action ()** menu next to the artifact version you want to delete.
> 5. From the dropdown, choose **Delete Version**.

> [tab] W\&B Python SDK
>
> Delete an artifact version programmatically with the [wandb.Artifact.delete()](https://docs.coreweave.com/products/wandb/ref/python/experiments/artifact.md#delete) method. Provide the full name of the artifact. The full name consists of `<entity>/<project>/<artifact_name>:<version>`. Set the `delete_aliases` parameter to `True` to delete the artifact even if it has one or more aliases associated with it.
>
> ```python theme={"system"}
> import wandb
>
> api = wandb.Api()
>
> # Get the artifact by its path
> artifact = api.artifact("<entity>/<project>/<artifact_name>:<version>")
>
> # Delete the artifact version along with any aliases
> artifact.delete(delete_aliases=True)
> ```

## Delete multiple artifact versions

The following code example shows how to delete multiple artifact versions. Provide the entity, project name, and run ID that created the artifact as arguments to `wandb.Api.run()`. This returns a run object that you can use to access all artifact versions created by that run. Next, iterate through the artifact versions and delete the ones that match your criteria.

> [!TIP]
>
> Set the `delete_aliases` parameter to `True` (`wandb.Artifact.delete(delete_aliases=True)`) to delete an artifact version and any aliases associated with it.

Replace the `<entity>`, `<project>`, `<run_id>`, and `<artifact_name>` placeholders with your own values:

```python theme={"system"}
import wandb

# Initialize W&B API
api = wandb.Api()

# Get the run by its path. Consists of <entity>/<project>/<run_id>
run = api.run("<entity>/<project>/<run_id>")

# Specify the artifact name to delete versions for
artifact_name = "<artifact_name>"

# Search and delete artifact versions with the specified name
for artifact in run.logged_artifacts():
    print(f"Found artifact: {artifact.name}") # Example name run_4dfbufgq_model:v0
    # Grab only the artifact name without the version with split()
    if artifact.name.split(":")[0] == artifact_name:
        print(f"Deleting artifact version: {artifact.name}")
        artifact.delete(delete_aliases=True)
```

## Delete multiple artifact versions with a specific alias

The following code demonstrates how to delete multiple artifact versions that have a specific alias.

Replace the `<entity>`, `<project>`, `<run_id>`, `<artifact_name>`, and `<alias>` placeholders with your own values:

```python theme={"system"}
import wandb

# Initialize W&B API
api = wandb.Api()

# Get the run by its path. Consists of <entity>/<project>/<run_id>
run = api.run("<entity>/<project>/<run_id>")

# Specify the artifact name to delete versions for
artifact_name = "<artifact_name>"

# Specify the alias to filter artifact versions for deletion
desired_alias = "<alias>"

# Delete artifacts logged to run with alias 'v3' and 'v4
for artifact in run.logged_artifacts():
    print(f"Found artifact: {artifact.name}")
    if (artifact.name.split(":")[0] == artifact_name) and (desired_alias in artifact.aliases):
            artifact.delete(delete_aliases=True)
```

## Delete an artifact collection

> [tab] W\&B App
>
> To delete an artifact collection:
>
> 1. Navigate to the artifact collection you want to delete.
> 2. Select the **action ()** menu next to the artifact collection name.
> 3. From the dropdown menu, select **Delete**.

> [tab] W\&B Python SDK
>
> Delete artifact collection programmatically with the [wandb.Artifact.delete()](https://docs.coreweave.com/products/wandb/ref/python/experiments/artifact.md#delete) method.
>
> Provide the full path of the artifact collection to `wandb.Api.artifact_collection(name="")`. The full path consists of `<entity>/<project>/<artifact_collection_name>`.
>
> ```python theme={"system"}
> import wandb
>
> # Initialize W&B API
> api = wandb.Api()
>
> # Get the artifact collection by its path. Consists of
> # <entity>/<project>/<artifact_collection_name>
> collection = api.artifact_collection(
>     type_name = "<artifact_type>",
>     name = "<entity>/<project>/<artifact_collection_name>"
> )
> collection.delete()
> ```

## Protected aliases and deletion permissions

Artifacts with protected aliases have special deletion restrictions. [Protected aliases](https://docs.coreweave.com/products/registry/aliases.md#protected-aliases) are aliases in the Registry that registry admins can set to prevent unauthorized deletion.

> [!NOTE]
>
> **Important considerations for protected aliases:**
>
> * Artifacts with protected aliases cannot be deleted by non-registry admins.
> * Within a registry, registry admins can unlink protected artifact versions and delete collections/registries that contain protected aliases.
> * For source artifacts: if a source artifact is linked to a registry with a protected alias, it cannot be deleted by any user
> * Registry admins can remove the protected aliases from source artifacts and then delete them.

## Enable garbage collection based on how Weights & Biases is hosted

> [!NOTE]
>
> Garbage collection timing is not guaranteed. See [Manage bucket storage and costs](https://docs.coreweave.com/products/wandb/platform/hosting/managing-bucket-storage.md) for details.

Garbage collection is active by default if you use W\&B Multi-tenant Cloud. In W\&B Dedicated and Self-Managed, you might need to take these additional steps to activate garbage collection.

1. **W\&B Self-Managed**: Set `GORILLA_ARTIFACT_GC_ENABLED=true`.
2. **Dedicated Cloud**: Contact support to verify that garbage collection is active.
3. Enable bucket versioning if you use [AWS](https://docs.aws.amazon.com/AmazonS3/latest/userguide/manage-versioning-examples.html), [Google Cloud](https://cloud.google.com/storage/docs/object-versioning) or any other storage provider such as [Minio](https://min.io/docs/minio/linux/administration/object-management/object-versioning.html#enable-bucket-versioning). If you use Azure, [enable soft deletion](https://learn.microsoft.com/azure/storage/blobs/soft-delete-blob-overview), which is equivalent to bucket versioning.

The following table describes how to satisfy requirements to enable garbage collection based on your deployment type.

The `X` indicates you must satisfy the requirement:

| | Environment variable | Enable versioning |
| - | - | - |
| Multi-tenant Cloud | | |
| Multi-tenant Cloud with [BYOB storage](https://docs.coreweave.com/products/wandb/platform/hosting/data-security/secure-storage-connector.md) | | X |
| Dedicated Cloud | | |
| Dedicated Cloud with [BYOB storage](https://docs.coreweave.com/products/wandb/platform/hosting/data-security/secure-storage-connector.md) | | X |
| Self-Managed | X | X |

> [!NOTE]
>
> note
> Secure storage connector is currently only available for Google Cloud Platform and Amazon Web Services.
