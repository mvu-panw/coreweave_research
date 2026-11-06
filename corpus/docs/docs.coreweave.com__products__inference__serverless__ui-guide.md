# Try models in the Playground UI

Source: https://docs.coreweave.com/products/inference/serverless/ui-guide

# Try models in the Playground UI

> Access Serverless Inference models through the web interface


Learn how to use the Serverless Inference service through the web UI. This guide shows you how to access the service, browse and compare available models, and try them out in the Playground. Use the UI when you want to explore models interactively without writing code.

## Prerequisites

Before you use the UI, complete the following:

* [Create an account](https://docs.coreweave.com/products/wandb/quickstart.md#create-an-account).
* [Create an API key](https://docs.coreweave.com/products/wandb/quickstart.md#create-an-api-key).
* A Weights & Biases project. Create a project in your CoreWeave Forge account to track usage. If you don't specify a project, Serverless Inference uses your default team and the project name `inference`.

## Access the Serverless Inference service

Get started using Serverless Inference at [https://forge.coreweave.com/inference](https://forge.coreweave.com/inference).

### Models

To see available Serverless Inference models, choose `Models` from the Serverless Inference sidebar menu or navigate to [https://forge.coreweave.com/inference/models](https://forge.coreweave.com/inference/models).

Double-click the model name to view model details, including pricing, features, and example code for usage.

From the model details page, you can:

* Click `Compare` to view a side-by-side, complete comparison of model details to one or more other models.
* Click `Playground` to interact directly with this model in the Playground.

You can also compare models directly in the Models table by using the action menu for the model's row.

### Playground

To try out Serverless Inference models, choose `Playground` from the Serverless Inference sidebar menu or navigate to [https://forge.coreweave.com/inference/playground](https://forge.coreweave.com/inference/playground).

Select the model you want to test using the model dropdown in the title toolbar.

The Playground can also connect to a [Dedicated Inference](https://docs.coreweave.com/products/inference/dedicated.md) deployment, if you have one configured.

![The models dropdown in Serverless Inference Playground](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/inference/_media/inference-playground.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=58439f015894f8c763cdcc155e9d96da)

Additionally from the Playground title toolbar you can:

* Enable and disable Weave tracing.  This records your conversation to Weave for later analysis and exploration.
  * When enabled, a `View call` link appears under each message that opens the trace tree for the chat.
* Select a project.  This is the project linked to your Playground conversation.  If unset, it defaults to `inference`.
* [Modify Playground settings](#modify-playground-settings).

After you select a model, you can test it in the Playground to evaluate its responses and tune its behavior before you integrate it elsewhere. You can add, edit, and delete messages.\
In the `Add a message` entry box you can also:

* `Add image`: Upload an image from file.
* `Add image URL`: Link to an image.
* `Specify role`: Specify the role of the message being defined (`System`, `Assistant`, or `User` role).

## Modify Playground settings

Click the **Settings** icon in the title toolbar to open the settings drawer. The drawer is organized into four collapsible sections:

![The Playground settings drawer showing the Reasoning, Tools, Generation, and Output sections](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/inference/_media/inference-playground-settings.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=abc97b6af6e2de258a692ad171b0f9bf)

**Reasoning**

* **Reasoning**: Controls whether the model produces reasoning before its final answer. Not configurable for models that are always on or don't support reasoning.
* **Reasoning effort**: Controls how much reasoning the model uses. Higher effort can increase latency and token usage.

**Tools**

* **Add Tool**: Define a function, with a name, description, and JSON Schema parameters, that the model can call.
* **Tool Choice**: Controls whether the model can't call tools, may choose to call them, or must call one.

**Generation**

* **Frequency penalty**: Penalizes tokens in proportion to how often they already appear. Positive values reduce verbatim repetition; negative values encourage it.
* **Presence penalty**: Penalizes tokens that have appeared at least once. Positive values encourage new topics; negative values encourage returning to existing topics.

**Output**

* **Response format**: Controls whether the model returns normal text, a valid JSON object, or output matching a supplied JSON Schema.
* **Max completion tokens**: Sets an upper bound on generated tokens, including visible output and reasoning tokens.

## Next steps

* Track your [billing and usage](https://docs.coreweave.com/products/inference/serverless/usage-limits.md#view-billing-and-usage-information).
* Review [available models](https://docs.coreweave.com/products/inference/serverless/models.md) to find the best one for your needs.
* Try the [API](https://docs.coreweave.com/products/inference/serverless/api-reference.md) for programmatic access.
* See [usage examples](https://docs.coreweave.com/products/inference/serverless/examples.md) for code samples.
