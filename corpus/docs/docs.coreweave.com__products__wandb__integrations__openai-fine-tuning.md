# OpenAI fine-tuning

Source: https://docs.coreweave.com/products/wandb/integrations/openai-fine-tuning

> Fine-tune OpenAI models with Weights & Biases to log metrics, monitor jobs, and compare model performance over time.

# OpenAI fine-tuning

[Try in Colab](https://wandb.me/openai-colab)

This page shows you how to log your OpenAI GPT-3.5 or GPT-4 model's fine-tuning metrics and configuration to Weights & Biases. By integrating Weights & Biases with OpenAI's fine-tuning API, you can track your fine-tuning experiments, models, and datasets in one place and share results with your colleagues. Use this integration when you fine-tune OpenAI models and want centralized experiment tracking and version control over the training data and resulting models.

> [!NOTE]
>
> See the [OpenAI documentation](https://platform.openai.com/docs/guides/fine-tuning/which-models-can-be-fine-tuned) for a list of models that you can fine-tune.

See the [Weights & Biases Integration](https://developers.openai.com/cookbook/examples/third_party/gpt_finetuning_with_wandb) section in the OpenAI documentation for supplemental information on how to integrate Weights & Biases with OpenAI for fine-tuning.

## Install or update OpenAI Python API

Before you sync fine-tuning results, make sure you have a compatible version of the OpenAI Python client installed. The Weights & Biases OpenAI fine-tuning integration works with OpenAI version 1.0 or later. See the PyPI documentation for the latest version of the [OpenAI Python API](https://pypi.org/project/openai/) library.

To install the OpenAI Python API, run:

```bash theme={"system"}
pip install openai
```

If you already have the OpenAI Python API installed, update it with:

```bash theme={"system"}
pip install -U openai
```

## Sync your OpenAI fine-tuning results

This section shows you how to send the metrics and configuration from an OpenAI fine-tuning job to Weights & Biases so you can review them alongside your other experiments. To do this, use the `WandbLogger` class from the `wandb.integration.openai.fine_tuning` module.

```python theme={"system"}
from wandb.integration.openai.fine_tuning import WandbLogger

# Finetuning logic

WandbLogger.sync(fine_tune_job_id=FINETUNE_JOB_ID)
```

![OpenAI auto-scan feature](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/_media/open_ai_auto_scan.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=9d681535cdda2798ca81208609ede18b)

### Sync your fine-tunes

Sync your results from your script. The following example shows both the minimal one-line call and the full set of optional parameters you can pass to control how the sync behaves.

```python theme={"system"}
from wandb.integration.openai.fine_tuning import WandbLogger

# one line command
WandbLogger.sync()

# passing optional parameters
WandbLogger.sync(
    fine_tune_job_id=None,
    num_fine_tunes=None,
    project="OpenAI-Fine-Tune",
    entity=None,
    overwrite=False,
    model_artifact_name="model-metadata",
    model_artifact_type="model",
    **kwargs_wandb_init
)
```

### Reference

The following table describes each argument accepted by `WandbLogger.sync`.

| Argument | Description |
| - | - |
| `fine_tune_job_id` | The OpenAI fine-tune ID you get when you create your fine-tune job with `client.fine_tuning.jobs.create`. If this argument is `None` (default), Weights & Biases syncs all OpenAI fine-tune jobs that haven't already been synced. |
| `openai_client` | Pass an initialized OpenAI client to `sync`. If you don't provide a client, the logger initializes one. The default is `None`. |
| `num_fine_tunes` | If you don't provide an ID, Weights & Biases logs all unsynced fine-tunes. This argument lets you select the number of recent fine-tunes to sync. If `num_fine_tunes` is 5, Weights & Biases selects the 5 most recent fine-tunes. |
| `project` | Weights & Biases project name where Weights & Biases logs your fine-tune metrics, models, data, and so on. By default, the project name is `"OpenAI-Fine-Tune"`. |
| `entity` | Weights & Biases username or team name where you send runs. By default, Weights & Biases uses your default entity, which is usually your username. |
| `overwrite` | Forces logging and overwrites the existing `wandb` run for the same fine-tune job. The default is `False`. |
| `wait_for_job_success` | An OpenAI fine-tuning job takes some time after it starts. To ensure that Weights & Biases logs your metrics as soon as the fine-tune job finishes, this setting checks every 60 seconds for the fine-tune job status to change to `succeeded`. Once the fine-tune job succeeds, Weights & Biases syncs the metrics automatically. The default is `True`. |
| `model_artifact_name` | The name of the logged model artifact. Defaults to `"model-metadata"`. |
| `model_artifact_type` | The type of the logged model artifact. Defaults to `"model"`. |
| `**kwargs_wandb_init` | Any additional argument passed directly to [`wandb.init()`](https://docs.coreweave.com/products/wandb/ref/python/functions/init). |

## Dataset versioning and visualization

When you sync a fine-tuning job, Weights & Biases also captures the training and validation data so you can version it and explore it interactively. The following subsections describe what Weights & Biases tracks and how to view it.

### Versioning

The training and validation data that you upload to OpenAI for fine-tuning are automatically logged as W\&B Artifacts for easier version control. The following image shows a view of the training file in Artifacts. You can see the W\&B run that logged this file, when it was logged, the version of the dataset, the metadata, and DAG lineage from the training data to the trained model.

![W\&B Artifacts with training datasets](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/_media/openai_data_artifacts.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=fdffde1b7ccdc84eaacb60ef7df7f9cc)

### Visualization

Weights & Biases visualizes the datasets as W\&B Tables, which lets you explore, search, and interact with the dataset. The following image shows training samples visualized in W\&B Tables.

![OpenAI data](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/_media/openai_data_visualization.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=8afc52341cfc0247f4ca0ec2d5fdb07c)

## The fine-tuned model and model versioning

OpenAI doesn't expose the underlying weights of a fine-tuned model, so Weights & Biases tracks the model by capturing its metadata instead. OpenAI gives you an ID of the fine-tuned model. Since you don't have access to the model weights, the `WandbLogger` creates a `model_metadata.json` file with all the details (hyperparameters, data file IDs, and so on) of the model along with the `fine_tuned_model` ID, and logs it as a W\&B Artifact.

You can link this model (metadata) artifact to a model in the [Registry](https://docs.coreweave.com/products/registry.md).

![OpenAI model metadata](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/_media/openai_model_metadata.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=590d049063991a49392df0c508ce99fa)

## Frequently asked questions

The following sections answer common questions about sharing, organizing, and recovering fine-tuning runs synced from OpenAI.

### Share fine-tune results with your team

Log your fine-tune jobs to your team account with:

```python theme={"system"}
WandbLogger.sync(entity="<your-team-name>")
```

### Organize your runs

Weights & Biases automatically organizes your runs. You can filter and sort them based on any configuration parameter such as job type, base model, learning rate, training filename, and any other hyperparameter.

You can also rename your runs, add notes, or create tags to group them.

Once you're satisfied, save your workspace and use it to create a report, importing data from your runs and saved artifacts (training and validation files).

### Access your fine-tuned model

Weights & Biases logs the fine-tuned model ID as artifacts (`model_metadata.json`) and as config.

```python theme={"system"}
import wandb
    
with wandb.init(project="OpenAI-Fine-Tune", entity="<your-team-name>") as run:
    ft_artifact = run.use_artifact("<entity>/<project>/model_metadata:<version>")
    artifact_dir = ft_artifact.download()
```

The `<version>` placeholder is one of the following:

* A version number such as `v2`.
* The fine-tune ID such as `ft-xxxxxxxxx`.
* An alias added automatically such as `latest`, or added manually.

You can then access the `fine_tuned_model` ID by reading the downloaded `model_metadata.json` file.

### Recover a fine-tune that didn't sync

If a fine-tune wasn't logged to Weights & Biases successfully, use `overwrite=True` and pass the fine-tune job ID:

```python theme={"system"}
WandbLogger.sync(
    fine_tune_job_id="<fine-tune-job-id>",
    overwrite=True,
)
```

### Track datasets and models with Weights & Biases

Weights & Biases logs the training and validation data automatically as artifacts. Weights & Biases also logs the metadata, including the ID for the fine-tuned model, as artifacts.

You can also control the pipeline with low-level `wandb` APIs like `wandb.Artifact`, `wandb.Run.log`, and so on. This gives you full traceability of your data and models.

![OpenAI tracking FAQ](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/_media/open_ai_faq_can_track.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=a6ea1cf3afb0100d8bf76103f9c46be8)

## Resources

For deeper background and end-to-end examples, see the following resources.

* [OpenAI Fine-tuning Documentation](https://platform.openai.com/docs/guides/fine-tuning/) for thorough guidance and tips.
* [Demo Colab](https://wandb.me/openai-colab).
* [How to Fine-Tune Your OpenAI GPT-3.5 and GPT-4 Models with Weights & Biases](https://wandb.me/openai-report) report.
