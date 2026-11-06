# Azure OpenAI fine-tuning

Source: https://docs.coreweave.com/products/wandb/integrations/azure-openai-fine-tuning

> Fine-tune Azure OpenAI models with Weights & Biases to log metrics, hyperparameters, and training progress.

# Azure OpenAI fine-tuning

This guide shows you how to use Weights & Biases with Azure OpenAI to track and evaluate fine-tuning jobs for GPT-3.5 or GPT-4 models. When you integrate Weights & Biases, experiment tracking captures metrics, hyperparameters, and training artifacts so you can analyze and improve model performance. You can also use Weights & Biases' evaluation tools to make data-driven decisions about model selection.

This guide is for machine learning practitioners who fine-tune Azure OpenAI models and want a systematic way to track and compare runs.

![Azure OpenAI fine-tuning metrics](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/_media/aoai_ft_plot.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=d671347c47842614efa552808a3f7033)

## Prerequisites

Before you begin, complete the following:

* Set up Azure OpenAI service according to [official Azure documentation](https://wandb.me/aoai-wb-int).
* Configure a Weights & Biases account with an API key.

## Workflow overview

The following stages summarize how a typical Azure OpenAI fine-tuning job flows through Weights & Biases, from preparing the job through evaluating the resulting model.

### Fine-tuning setup

Fine-tuning setup involves the following steps:

* Prepare training data according to Azure OpenAI requirements.
* Configure the fine-tuning job in Azure OpenAI.
* Track the fine-tuning process and log metrics and hyperparameters with Weights & Biases.

### Experiment tracking

During fine-tuning, Weights & Biases captures:

* Training and validation metrics.
* Model hyperparameters.
* Resource usage.
* Training artifacts.

### Model evaluation

After fine-tuning, use [W\&B Weave](https://weave-docs.wandb.ai) to:

* Evaluate model outputs against reference datasets.
* Compare performance across different fine-tuning runs.
* Analyze model behavior on specific test cases.
* Make data-driven decisions for model selection.

## Real-world example

To see the integration applied end-to-end, explore the following resources:

* Explore the [medical note generation demo](https://wandb.me/aoai-ft-colab) to see how this integration facilitates:
  * Systematic tracking of fine-tuning experiments.
  * Model evaluation using domain-specific metrics.
* Work through an [interactive fine-tuning notebook](https://colab.research.google.com/github/wandb/examples/blob/master/colabs/azure/azure_gpt_medical_notes.ipynb).

## Additional resources

* [Azure OpenAI Weights & Biases Integration Guide](https://wandb.me/aoai-wb-int)
* [Azure OpenAI Fine-tuning Documentation](https://learn.microsoft.com/azure/ai-services/openai/how-to/fine-tuning?tabs=turbo%2Cpython\&pivots=programming-language-python)
