# Cline with Serverless Inference

Source: https://docs.coreweave.com/products/inference/serverless/tutorials/integration-cline

# Cline with Serverless Inference

> Learn how to configure the Cline coding agent to use Serverless Inference.


[Cline](https://cline.bot) is an AI-powered coding assistant. This tutorial demonstrates how to configure Cline to use models provided by Serverless Inference, so that you can use open-weight models hosted on Serverless Inference for your coding tasks.

The Cline agent is available as a command line tool or as an integration with many IDEs. The following sections describe configuration with the Cline CLI and with Cline as a Visual Studio Code extension. Configuration in other IDEs is similar.

## Prerequisites

Before you begin, complete the following:

* [Create an account](https://docs.coreweave.com/products/wandb/quickstart.md#create-an-account).
* [Create an API key](https://docs.coreweave.com/products/wandb/quickstart.md#create-an-api-key).

## Set up Cline in the command line

Install the [Cline CLI](https://docs.cline.bot/cline-cli/installation).

```bash theme={"system"}
npm install -g cline
```

See [Cline's installation instructions](https://docs.cline.bot/cline-cli/installation) for troubleshooting.

Run `cline version` to verify what you have installed.

### Use the native Weights & Biases provider

This configuration was tested with Cline CLI version `3.0.61` on macOS. Set the `WANDB_API_KEY` environment variable to your CoreWeave Forge API key. Then run:

```bash theme={"system"}
cline -P wandb -m zai-org/GLM-5.3-Flash "What is 2 + 2?"
```

The provider's command-line ID is `wandb`. Depending on your Cline version, the provider appears as **Weights & Biases** or **W\&B**. Cline uses that provider's configured Serverless Inference endpoint. If Cline responds with an answer, the connection is working.

### Use the OpenAI-compatible provider

The following instructions were tested with Cline CLI version `2.5.1`.

Next, authenticate Cline against the Serverless Inference endpoint. The following command configures Cline to use the Serverless Inference OpenAI-compatible endpoint and the Kimi K2.6 model. Substitute `[YOUR-API-KEY]` with your CoreWeave Forge API key.

```bash theme={"system"}
cline auth -k [YOUR-API-KEY] -p openai -b https://api.inference.wandb.ai/v1 -m moonshotai/Kimi-K2.6
```

For model availability, see the [Serverless Inference models documentation](https://forge.coreweave.com/inference/serverless/models).

Run a test to verify everything is working:

```bash theme={"system"}
cline "What is 2 + 2?"
```

If Cline responds with an answer, your installation and authentication are complete.

For more information about using the Cline CLI, see the [Cline Quickstart](https://docs.cline.bot/cline-cli/installation#quick-start).

## Set up Cline in Visual Studio Code

If you prefer to use Cline inside an IDE, you can install it as a Visual Studio Code extension. Search for **Cline** in the VS Code Extensions Marketplace, or install it from the [Visual Studio Code Marketplace](https://marketplace.visualstudio.com/items?itemName=saoudrizwan.claude-dev).

Click **Install**.

![VS Code extension installation](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/inference/_media/inference-tutorial-cline-install.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=7adaa55f3f5a579012fec329624c7045)

Click the newly added Cline icon in your Activity Bar to open the Cline sidebar. If the Cline icon isn't showing in the Activity Bar, click the dropdown to see more options.

![Cline icon in the VS Code Activity Bar](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/inference/_media/inference-tutorial-cline-activity-bar.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=82986a6d6012474ad215f6ad4bd3901d)

Select **Bring my own API key** and click **Continue**.

![Select Bring Your Own Key](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/inference/_media/inference-tutorial-cline-byok.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=d8f5fa7ea8264d1ec975388c77dd46f0)

Specify the following values, substituting `[YOUR-API-KEY]` with your CoreWeave Forge API key:

| Setting | Value |
| - | - |
| API Provider | `OpenAI Compatible` |
| Base URL | `https://api.inference.wandb.ai/v1` |
| OpenAI Compatible API Key | `[API-KEY]` |
| Model ID | `moonshotai/Kimi-K2.6` |

Specify pricing by expanding **Model Configuration**.

Click **Continue**.

Try submitting a prompt like "Write a Python program to compute the first 10 Fibonacci Numbers".

![Submit your coding task to the agent](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/inference/_media/inference-tutorial-cline-act.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=5841d7855033be36115af50411a810a0)

For more information about using Cline, see the [Cline Documentation](https://docs.cline.bot).
