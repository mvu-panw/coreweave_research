# Artifacts overview

Source: https://docs.coreweave.com/products/wandb/artifacts

> Overview of W&B Artifacts, how they work, and how to get started using them.

# Artifacts overview

[Try in Colab](https://colab.research.google.com/github/wandb/examples/blob/master/colabs/wandb-artifacts/Pipeline_Versioning_with_W\&B_Artifacts.ipynb)

[Try in W\&B](https://forge.coreweave.com/wandb/wandb/arttest/artifacts/model/iv3_trained/5334ab69740f9dda4fed/lineage)

Use W\&B Artifacts to track and version data as the inputs and outputs of your [W\&B Runs](https://docs.coreweave.com/products/wandb/runs.md). For example, a model training run might take in a dataset as input and produce a trained model as output. You can log hyperparameters, metadata, and metrics to a run, and you can use an artifact to log, track, and version the dataset used to train the model as input and another artifact for the resulting model checkpoints as output.

## Use cases

You can use artifacts throughout your entire ML workflow as inputs and outputs of [runs](https://docs.coreweave.com/products/wandb/runs.md). You can use datasets, models, or even other artifacts as inputs for processing.

![Artifacts workflow diagram with inputs and outputs for model training, data processing, and model evaluation](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/_media/artifacts_landing_page2.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=473134067fd8e18b8e2cc3988de8b5de)

| Use Case | Input | Output |
| - | - | - |
| Model Training | Dataset (training and validation data) | Trained Model |
| Dataset Pre-Processing | Dataset (raw data) | Dataset (pre-processed data) |
| Model Evaluation | Model + Dataset (test data) | [W\&B Table](https://docs.coreweave.com/products/wandb/tables.md) |
| Model Optimization | Model | Optimized Model |

> [!NOTE]
>
> The following code snippets are meant to be run in order.

## Create an artifact

Create an artifact with four lines of code:

1. Create a [W\&B run](https://docs.coreweave.com/products/wandb/runs.md).
2. Create an artifact object with [`wandb.Artifact`](https://docs.coreweave.com/products/wandb/ref/python/experiments/artifact).
3. Add one or more files, such as a model file or dataset, to the artifact object with `wandb.Artifact.add_file()`.
4. Log your artifact to Weights & Biases with `wandb.Run.log_artifact()`.

For example, the following code snippet shows how to log a file called `dataset.h5` to an artifact called `example_artifact`:

```python theme={"system"}
import wandb

with wandb.init(project="artifacts-example", job_type="add-dataset") as run:
    artifact = wandb.Artifact(name="example_artifact", type="dataset")
    artifact.add_file(local_path="./dataset.h5", name="training_dataset")
    run.log_artifact(artifact)
```

* The `type` of the artifact affects how it appears in Weights & Biases. If you do not specify a `type`, it defaults to `unspecified`.
* Each label of the dropdown represents a different `type` parameter value. In the above code snippet, the artifact's `type` is `dataset`.

> [!NOTE]
>
> See the [track external files](https://docs.coreweave.com/products/wandb/artifacts/track-external-files.md) page for information on how to add references to files or directories stored in external object storage, like an Amazon S3 bucket.

## Download an artifact

Indicate the artifact you want to mark as input to your run with the [`wandb.Run.use_artifact()`](https://docs.coreweave.com/products/wandb/ref/python/experiments/run#use_artifact) method.

Continuing from the previous code snippet, the following code example shows how to use the artifact called `example_artifact` that was created earlier:

```python theme={"system"}
with wandb.init(project="artifacts-example", job_type="add-dataset") as run:
    artifact = run.use_artifact("training_dataset:latest")  # returns a run object using the "my_data" artifact
```

This returns an artifact object.

Next, use the returned object to download all contents of the artifact:

```python theme={"system"}
datadir = artifact.download()  # downloads the full `my_data` artifact to the default directory.
```

> [!NOTE]
>
> You can pass a custom path into the `root` [parameter](https://docs.coreweave.com/products/wandb/ref/python/experiments/artifact.md) to download an artifact to a specific directory. For alternate ways to download artifacts and to see additional parameters, see the guide on [downloading and using artifacts](https://docs.coreweave.com/products/wandb/artifacts/download-and-use-an-artifact.md).

## Next steps

* Learn how to [version](https://docs.coreweave.com/products/wandb/artifacts/create-a-new-artifact-version.md) and [update](https://docs.coreweave.com/products/wandb/artifacts/update-an-artifact.md) artifacts.
* Learn how to trigger downstream workflows or notify a Slack channel in response to changes to your artifacts with [automations](https://docs.coreweave.com/products/wandb/automations.md).
* Learn about the [registry](https://docs.coreweave.com/products/registry.md), a space that houses trained models.
* Explore the [Python SDK](https://docs.coreweave.com/products/wandb/ref/python/experiments/artifact.md) and [CLI](https://docs.coreweave.com/products/wandb/ref/cli/wandb-artifact.md) reference guides.
