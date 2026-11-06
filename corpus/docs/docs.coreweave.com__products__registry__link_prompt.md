# Link a Weave prompt to a collection

Source: https://docs.coreweave.com/products/registry/link_prompt

# Link a Weave prompt to a collection

Track, version, and manage your AI prompts in the Registry by linking Weave prompt objects to a collection. *Linking* a prompt object to a [collection](https://docs.coreweave.com/products/registry/create_collection.md) moves the prompt version from a [private, project-level scope to a shared, organization-level scope](https://docs.coreweave.com/products/registry/create_registry.md#visibility-types).

> [!NOTE]
>
> Before you start, check the following:
>
> * The object types that collection permits. For more information about collection types, see "Collection types" within [Create a collection](https://docs.coreweave.com/products/registry/create_collection.md).
> * The registry that the collection belongs to already exists. To check that the registry exists, navigate to the [Registry App and search for](https://docs.coreweave.com/products/registry/search_registry.md) the name of the registry.

To track and manage your AI prompts, use the Weave Python SDK. The Weave Python SDK enables you to create, publish, and link prompt objects to a collection in a registry.

The following steps outline how to link a prompt to a collection in a registry:

1. Initialize a Weave client with `weave.init()`.
2. Create a Weave prompt object with a built-in prompt class such as [`weave.StringPrompt()`](https://docs.coreweave.com/products/wandb/weave/reference/python-sdk#class-stringprompt).
   > [!TIP]
   >
   > `weave.StringPrompt` is a built-in prompt class for single-string prompts, such as a system prompt, user prompt, or reusable text template. For more information about creating prompt objects in Weave, and supported prompt types, see [Create prompt objects](https://docs.coreweave.com/products/wandb/weave/guides/core-types/prompts.md).
3. Publish the prompt to Weave with [`weave.publish()`](https://docs.coreweave.com/products/wandb/weave/reference/python-sdk#method-publish).
4. Link the published prompt version to a collection in a registry with [`weave_client.link_prompt_to_registry()`](https://docs.coreweave.com/products/wandb/weave/reference/python-sdk/trace/weave_client#method-link_prompt_to_registry). Pass the destination collection path to the `target_path` parameter. The path consists of the `wandb-registry-` prefix, the registry name, and the collection name:
   ```text theme={"system"}
   wandb-registry-{REGISTRY_NAME}/{COLLECTION_NAME}
   ```

Copy and paste the following code snippet into your Python script, replacing the placeholder values enclosed in `<>` with your own:

```python theme={"system"}
import weave

# Initialize Weave client
weave_client = weave.init(project="<project>")

prompt = "<You are a helpful assistant...>"

# Publish the prompt object to Weave
weave_prompt_ref = weave.publish(
    obj=weave.StringPrompt(prompt),
    name="<prompt_name>",
)

# Specify the collection and registry to link the prompt version to
REGISTRY_NAME = "<registry_name>"
COLLECTION_NAME = "<collection_name>"
registry_target = f"wandb-registry-{REGISTRY_NAME}/{COLLECTION_NAME}"

# Link the published prompt version to a collection in the specified registry
weave_client.link_prompt_to_registry(
    prompt=weave_prompt_ref,
    target_path=registry_target,
)
```

## View linked prompts in a registry

View the content, usage instructions, and Registry details for a linked prompt version. Each linked prompt version includes the following tabs:

| Tab | Description |
| - | - |
| Overview | View version details such as its Registry path, aliases, tags, description, source, and creation time. |
| Prompt | View the immutable prompt content. Depending on the prompt type, the content can be a string, a parameterized template, or an ordered list of messages with roles such as `system`, `user`, and `assistant`. |
| Use | View generated Python code and the Registry URI for retrieving the prompt. The URI can reference an immutable version, such as `:v4`, or an alias that can be reassigned, such as `:production`. Use the returned prompt object directly or format it with variables in your application. |

To view a linked prompt in a registry:

1. Navigate to **Registry**.
2. Select the name of the registry that you linked the prompt to.
3. Select the name of the collection. This expands the list of prompt versions within the collection.
4. Select a version.

> [!NOTE]
>
> The information displayed for a linked prompt version differs from that for a [linked artifact version](https://docs.coreweave.com/products/registry/link_version.md#view-linked-artifacts-in-a-registry).

## Use a prompt linked to a registry

Use the `weave.get()` method to retrieve a prompt object linked to a registry. You can fetch a prompt by its alias or version number. The following code snippet shows how to fetch a prompt by its alias and version number.

To fetch a prompt object by its alias, use the following URI path:

```text theme={"system"}
registry:///{ORG}/{REGISTRY_NAME}/{COLLECTION_NAME}:{VERSION-OR-ALIAS}
```

Replace the placeholder values enclosed in `<>` with your own:

> [tab] Fetch by alias
>
> ```python theme={"system"}
> # Fetch by alias
> URI_path = f"registry:///{ORG}/{REGISTRY_NAME}/{COLLECTION_NAME}:{ALIAS}"
>
> # Fetch by alias
> prompt = weave.get(URI_path)
>
> # Use the prompt
> print(prompt.content)
> ```

> [tab] Fetch by version
>
> ```python theme={"system"}
> # Fetch by version
> URI_path = f"registry:///{ORG}/{REGISTRY_NAME}/{COLLECTION_NAME}:{VERSION}"
>
> # Fetch by version
> prompt = weave.get(URI_path)
>
> # Use the prompt
> print(prompt.content)
> ```

W\&B autogenerates the URI path and sample code to fetch your prompt object. To view the sample code:

1. Navigate to **Registry**.
2. Select the name of the registry that you linked the prompt to.
3. Select the name of the collection.
4. From the list of prompt versions, select the version you want to access.
5. Select the **Use** tab to view the sample code to fetch your prompt by alias or version number.
