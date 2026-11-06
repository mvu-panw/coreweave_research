# Delete registry

Source: https://docs.coreweave.com/products/registry/delete_registry

# Delete registry

> Delete a Registry as a Team admin or Registry admin using the Python SDK or the W&B App UI.

This page shows how a Team admin or Registry admin can delete a registry.

* A Team admin can delete any registry in the organization.
* A Registry admin can delete a registry that they created.

Deleting a registry also deletes collections that belong to that registry, but does not delete artifacts linked to the registry.  Such an artifact remains in the original project that the artifact was logged to.

> [tab] W\&B Python SDK
>
> Use the W\&B Public API `delete()` method to delete a registry programmatically. The following example illustrates how to:
>
> 1. Fetch the registry you want to delete with `wandb.Api.registry()`.
> 2. Call the `delete()` method on the returned registry object to delete the registry.
>
> ```python theme={"system"}
> import wandb
>
> # Initialize the W&B API
> api = wandb.Api()
>
> # Fetch the registry you want to delete
> fetched_registry = api.registry("<registry_name>")
>
> # Deleting a registry
> fetched_registry.delete()
> ```

> [tab] W\&B App
>
> 1. Navigate to **Registry**.
> 2. Select the registry you want to delete.
> 3. Click the gear icon in the upper right corner to view the registry's settings.
> 4. To delete the registry, click the trash can icon in the upper right corner of the settings page.
> 5. Confirm the registry to delete by entering its name in the modal that appears, then click **Delete**.
