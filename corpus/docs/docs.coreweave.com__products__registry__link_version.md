# Link an artifact version to a collection

Source: https://docs.coreweave.com/products/registry/link_version

# Link an artifact version to a collection

> Link an artifact version to a collection in Registry to share it across your organization.

To make an artifact version available to your organization, *link* it to a [collection](https://docs.coreweave.com/products/registry/create_collection.md) in
the Registry. Linking moves the version from a [private, project-level scope to a shared, organization-level scope](https://docs.coreweave.com/products/registry/create_registry.md#visibility-types). You
can link an artifact version [programmatically by using the W\&B Python SDK or interactively in the W\&B App](https://docs.coreweave.com/products/registry/link_version.md#link-an-artifact-to-a-collection).

When you link an artifact, W\&B creates a reference between the source artifact and the collection entry. The linked version points to the source artifact version that was logged to a run within a project. You can view both the linked version in the collection and the source version in the project where it was logged.

## Link an artifact to a collection

Choose a workflow based on whether you want to create the artifact during a run, create it without a run, or link an existing artifact version.

> [!NOTE]
>
> Before you start, check the following:
>
> * The types of artifacts that collection permits. For more information about collection types, see "Collection types" within [Create a collection](https://docs.coreweave.com/products/registry/create_collection.md).
> * The registry that the collection belongs to already exists. To check that the registry exists, navigate to the [Registry App and search for](https://docs.coreweave.com/products/registry/search_registry.md) the name of the registry.

> [tab] W\&B Python SDK
>
> Programmatically link an artifact version to a collection with [`wandb.Run.link_artifact()`](https://docs.coreweave.com/products/wandb/ref/python/experiments/run#method-run-link_artifact) or
> [`wandb.Artifact.link()`](https://docs.coreweave.com/products/wandb/ref/python/experiments/artifact#method-artifact-link)
>
> The following table summarizes the methods you can use to link an artifact version to a collection and what W\&B records when you use each method.
>
> | Use case | Method | What W\&B records |
> | - | - | - |
> | Create an artifact during a run and link it to a collection | `wandb.Run.link_artifact()` | Logs the artifact as an output of the active run, then links it |
> | Create and link an artifact without explicitly starting a run | `wandb.Artifact.link()` on a draft artifact | Saves the artifact first; if no run is active, creates an automatic run |
> | Link an existing committed artifact | `wandb.Artifact.link()` on an artifact from `wandb.Api().artifact()` | Links the artifact without creating a new run |
>
> Pass the destination collection path to the `target_path` parameter. The path consists of the `wandb-registry-` prefix, the registry name, and the collection name:
>
> ```text theme={"system"}
> wandb-registry-{REGISTRY_NAME}/{COLLECTION_NAME}
> ```
>
> ##### Link an artifact from a run
>
> Use `wandb.Run.link_artifact()` to create and link an artifact version during an active run. W\&B logs draft artifacts as outputs of the run before linking them.
>
> To create and link an artifact version:
>
> 1. Initialize a run with `wandb.init()`.
> 2. Create an `Artifact` object and add one or more files.
> 3. Call `wandb.Run.link_artifact()` and specify the destination collection.
>
> Replace values enclosed in angle brackets (`<>`) with your own values:
>
> ```python theme={"system"}
> import wandb
>
> entity = "<team_entity>"          # Your team entity
> project = "<project_name>"        # The name of the project that contains your artifact
>
> # Initialize a run
> with wandb.init(entity = entity, project = project) as run:
>
>   # Create an artifact object
>   # The type parameter specifies both the type of the
>   # artifact object and the collection type
>   artifact = wandb.Artifact(name = "<name>", type = "<type>")
>
>   # Add the file to the artifact object.
>   # Specify the path to the file on your local machine.
>   artifact.add_file(local_path = "<local_path_to_artifact>")
>
>   # Specify the collection and registry to link the artifact to
>   REGISTRY_NAME = "<registry_name>"
>   COLLECTION_NAME = "<collection_name>"
>   target_path=f"wandb-registry-{REGISTRY_NAME}/{COLLECTION_NAME}"
>
>   # Link the artifact to the collection
>   run.link_artifact(artifact = artifact, target_path = target_path)
> ```
>
> ##### Create and link an artifact
>
> Use `wandb.Artifact.link()` to create and link a draft artifact without explicitly initializing a run. W\&B creates an automatic run if needed to save the artifact before linking it.
>
> To create and link an artifact version:
>
> 1. Create an `Artifact` object and add one or more files.
> 2. Call `wandb.Artifact.link()` and specify the destination collection.
>
> Replace values in angle brackets (`<>`) with your own:
>
> ```python theme={"system"}
> import wandb
>
> # Create an artifact object
> # The type parameter specifies both the type of the
> # artifact object and the collection type
> artifact = wandb.Artifact(name = "<name>", type = "<type>")
>
> # Add the file to the artifact object.
> # Specify the path to the file on your local machine.
> artifact.add_file(local_path = "<local_path_to_artifact>")
>
> # Specify the collection and registry to link the artifact to
> REGISTRY_NAME = "<registry_name>"
> COLLECTION_NAME = "<collection_name>"
> target_path=f"wandb-registry-{REGISTRY_NAME}/{COLLECTION_NAME}"
>
> # Link the artifact to the collection
> artifact.link(target_path = target_path)
> ```
>
> ##### Link an existing artifact
>
> Use `wandb.Artifact.link()` on an artifact fetched with `wandb.Api().artifact()` to link an existing committed artifact version without creating a new run.
>
> 1. Create a Public API client with `wandb.Api()`.
> 2. Retrieve the artifact version with `wandb.Api.artifact()`.
> 3. Call `wandb.Artifact.link()` and specify the destination collection.
>
> ```python theme={"system"}
> import wandb
>
> api = wandb.Api()
>
> artifact = api.artifact(
>     "<entity>/<project>/<artifact-name>:<alias-or-version>"
> )
>
> artifact.link(
>     target_path="wandb-registry-<registry-name>/<collection-name>",
>     aliases=["latest"],
> )
> ```

> [tab] Registry
>
> 1. Navigate to **Registry**.
> 2. Select the collection you want to link an artifact version to.
> 3. Select the **action ()** menu next to **View details**.
> 4. From the dropdown, select **Link new version**.
> 5. From the sidebar that appears, select the name of a team from the **Team** dropdown.
> 6. From the **Project** dropdown, select the name of the project that contains your artifact.
> 7. From the **Artifact** dropdown, select the name of the artifact.
> 8. From the **Version** dropdown, select the artifact version you want to link to the collection.

> [tab] Artifact browser
>
> 1. Navigate to your project's artifact browser on the W\&B App at: `https://wandb.ai/<entity>/<project>/artifacts`
> 2. Select the Artifacts icon in the project sidebar.
> 3. Click on the artifact version you want to link to your registry.
> 4. Within the **Version overview** section, click the **Link to registry** button.
> 5. From the modal that appears on the right of the screen, select an artifact from the **Select a registered model** menu dropdown.
> 6. Click **Next step**.
> 7. (Optional) Select an alias from the **Aliases** dropdown.
> 8. Click **Link to registry**.

You can [view a linked artifact's metadata, version data, usage, lineage information](https://docs.coreweave.com/products/registry/link_version.md#view-linked-artifacts-in-a-registry) and more in the Registry App.

## Unlink an artifact version from a collection

Use the W\&B Python SDK or the Registry to unlink an artifact version from a collection.

Unlinking removes the artifact version from the collection but does not delete the source artifact version or its files.

> [!WARNING]
>
> Linking an artifact version to a registry collection deactivates its time-to-live (TTL) policy and sets its TTL to `None`. If you later unlink the version, W\&B does not restore the previous TTL or preserve its original duration. Reconfigure the TTL after unlinking if the version still requires one.
>
> For more information about TTL policies, see [Manage artifact data retention](https://docs.coreweave.com/products/wandb/artifacts/ttl.md).

> [tab] W\&B Python SDK
>
> To unlink an artifact version with the W\&B Python SDK:
>
> 1. Create a Public API client with `wandb.Api()`.
> 2. Retrieve the linked artifact version with `wandb.Api.artifact()`.
> 3. Call [`wandb.Artifact.unlink()`](https://docs.coreweave.com/products/wandb/ref/python/experiments/artifact#method-artifact-unlink) to unlink the artifact version from the collection.
>
> ```text theme={"system"}
> wandb-registry-<registry_name>/<collection_name>:<version_or_alias>
> ```
>
> Replace the placeholder values with your own values:
>
> ```python theme={"system"}
> import wandb
>
> registry_name = "your-registry-name"  # Replace with the name of the registry
> collection_name = "your-collection-name"  # Replace with the name of the collection
> version = "version-or-alias"  # Replace with the version of the artifact you want to unlink
>
> target_path=f"wandb-registry-{registry_name}/{collection_name}:{version}"
>
> api = wandb.Api()
> linked_artifact = api.artifact(name=target_path)
>
> # Unlink the artifact version from the collection
> linked_artifact.unlink()
> ```

> [tab] Registry
>
> 1. Navigate to **Registry**.
> 2. Select the name of the registry that contains the collection.
> 3. Select the collection.
> 4. Select the artifact version you want to unlink.
> 5. From the **Version** tab, select **Unlink version**.

## View linked artifacts in a registry

View the metadata, usage, files, lineage, and deployment information for an artifact version linked to a Registry collection. Each linked artifact version includes the following tabs:

| Tab | Description |
| - | - |
| **Version** | View identifying details such as the Registry full name, aliases, tags, source version, digest, description, producing run, creation time, size, file count, the storage region, and the time to live (TTL). If you have the required permissions, you can manage aliases and tags or unlink the version. |
| **Metadata** | View key-value metadata added when the source artifact was logged or imported, such as a dataset split, model framework, hyperparameters, source repository, or import revision. |
| **Usage** | View instructions for using the selected artifact version programmatically. The **Used by** section lists runs that use the artifact version as an input. |
| **Files** | Browse the immutable files in the artifact manifest. You can inspect directories and file sizes, preview supported files, or download individual files or the complete artifact. |
| **Lineage** | View a [dependency graph](https://docs.coreweave.com/products/registry/lineage.md) of how the artifact version was produced and used. The graph can include upstream artifacts, producing runs, downstream runs, and output artifacts. |
| **Deployments** | (Private preview only) View deployment information associated with the selected artifact version. |

> [!TIP]
>
> Make note of the **Full Name** field within the **Version** tab. The full name of a linked artifact consists of the registry, collection name, and the alias or index of the artifact version.
>
> ```text title="Full name of a linked artifact" theme={"system"}
> wandb-registry-{REGISTRY_NAME}/{COLLECTION_NAME}:v{INTEGER}
> ```
>
> You need the full name of a linked artifact to access the artifact version programmatically.

To view linked artifacts in a registry:

1. Navigate to **Registry**.
2. Select a registry.
3. Select a collection. This expands the list of artifact versions within the collection.
4. Select a version.

> [!NOTE]
>
> The information displayed for a linked artifact differs from that for a [linked prompt](https://docs.coreweave.com/products/registry/link_prompt.md#view-linked-prompts-in-a-registry).

## Troubleshooting

Below are some common things to check if you are not able to link an artifact.

### Logging artifacts from a personal account

Artifacts logged to W\&B with a personal entity can not be linked to the registry. Make sure that you log artifacts using a team entity within your organization. Only artifacts logged within an organization's team can be linked to the organization's registry.

> [!NOTE]
>
> Ensure that you log an artifact with a team entity if you want to link that artifact to a registry.

#### Find your team entity

W\&B uses the name of your team as the team's entity. For example, if your team is called **team-awesome**, your team entity is `team-awesome`.

You can confirm the name of your team by:

1. Navigate to your team's W\&B profile page.
2. Copy the site's URL. It has the form of `https://wandb.ai/<team>`. Where `<team>` is both the name of your team and the team's entity.

#### Log from a team entity

1. Specify the team as the entity when you initialize a run with [`wandb.init()`](https://docs.coreweave.com/products/wandb/ref/python/functions/init). If you do not specify the `entity` when you initialize a run, the run uses your default entity which may or may not be your team entity.

   ```python theme={"system"}
   import wandb

   with wandb.init(entity='<team_entity>', project='<project_name>') as run:
       # Log your artifact here
   ```

2. Log the artifact to the run either with `wandb.Run.log_artifact()` or by creating an Artifact object and then adding files to it with:

   ```python theme={"system"}
   artifact = wandb.Artifact(name="<artifact_name>", type="<type>")
   ```

   To log artifacts, see [Construct artifacts](https://docs.coreweave.com/products/wandb/artifacts/construct-an-artifact.md).

3. If an artifact is logged to your personal entity, you will need to re-log it to an entity within your organization.

### Confirm the path of a registry in the W\&B App UI

Create an empty collection to confirm the path of the registry in the W\&B App UI. To do so, follow the steps below:

1. Navigate to **Registry**.
2. Click the registry you want to link an artifact to.
3. Click on the empty collection. If an empty collection does not exist, create a new collection.
4. Within the code snippet that appears, identify the `target_path=` field within `.link_artifact()`.
5. (Optional) Delete the collection.

For example, after completing the steps outlined, you find the code block with the `target_path` parameter:

![Create an empty collection](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/registry/_media/check_empty_collection.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=d056d6e2177061f85d8b9ebe9532d7ef)

```python theme={"system"}
target_path =
      "wandb-registry-Zoo-Classifier-Registry/Temp Collection"
```

Breaking this down into its components, you can see what you will need to use to create the path to link your artifact programmatically:

```python theme={"system"}
ORG_ENTITY_NAME = "wandb"
REGISTRY_NAME = "Zoo-Classifier-Registry"
COLLECTION_NAME = "Temp Collection"
```

> [!NOTE]
>
> Ensure that you replace the name of the collection from the temporary collection with the name of the collection that you want to link your artifact to.
