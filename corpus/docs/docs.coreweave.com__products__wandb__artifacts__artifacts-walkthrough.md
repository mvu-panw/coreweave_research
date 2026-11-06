# Tutorial: Create, track, and use a dataset artifact

Source: https://docs.coreweave.com/products/wandb/artifacts/artifacts-walkthrough

> Create, track, and use a dataset artifact with Weights & Biases.

# Tutorial: Create, track, and use a dataset artifact

This walkthrough demonstrates how to create, track, and use a dataset artifact.

## 1. Log into Weights & Biases

Import the W\&B library and log in to Weights & Biases. You will need to sign up for a free Weights & Biases account if you have not done so already.

```python theme={"system"}
import wandb

wandb.login()
```

## 2. Initialize a run

Use [`wandb.init()`](https://docs.coreweave.com/products/wandb/ref/python/functions/init) to initialize a run. This generates a background process to sync and log data. Provide a project name and a job type:

```python theme={"system"}
# Create a W&B Run. Here we specify 'dataset' as the job type since this example
# shows how to create a dataset artifact.
with wandb.init(project="artifacts-example", job_type="upload-dataset") as run:
    # Your code here
```

## 3. Create an artifact object

Create an artifact object with the [`wandb.Artifact()`](https://docs.coreweave.com/products/wandb/ref/python/experiments/artifact). Provide a name for the artifact and a description of the file type for the `name` and `type` parameters, respectively.

For example, the following code snippet demonstrates how to create an artifact called `‘bicycle-dataset’` with a `‘dataset’` label:

```python theme={"system"}
artifact = wandb.Artifact(name="bicycle-dataset", type="dataset")
```

For more information about how to construct an artifact, see [Construct artifacts](https://docs.coreweave.com/products/wandb/artifacts/construct-an-artifact.md).

## 4. Add the dataset to the artifact

Add a file to the artifact. Common file types include models and datasets. The following example adds a dataset named `dataset.h5` that is saved locally on our machine to the artifact:

```python theme={"system"}
# Add a file to the artifact's contents
artifact.add_file(local_path="dataset.h5")
```

Replace the filename `dataset.h5` in the previous code snippet with the path to the file you want to add to the artifact.

## 5. Log the dataset

Use the W\&B run objects `wandb.Run.log_artifact()` method to both save your artifact version and declare the artifact as an [output of the run](https://docs.coreweave.com/products/wandb/artifacts/explore-and-traverse-an-artifact-graph.md).

```python theme={"system"}
# Save the artifact version to W&B and mark it
# as the output of this run
run.log_artifact(artifact)
```

A `'latest'` [alias](https://docs.coreweave.com/products/wandb/artifacts/create-a-custom-alias.md) is created by default when you log an artifact. For more information about artifact aliases and versions, see [Create a custom alias](https://docs.coreweave.com/products/wandb/artifacts/create-a-custom-alias.md) and [Create new artifact versions](https://docs.coreweave.com/products/wandb/artifacts/create-a-new-artifact-version.md), respectively.

Putting this together, you script so far should look like this:

```python theme={"system"}
import wandb

wandb.login()

with wandb.init(project="artifacts-example", job_type="upload-dataset") as run:
    artifact = wandb.Artifact(name="bicycle-dataset", type="dataset")
    artifact.add_file(local_path="dataset.h5")
    run.log_artifact(artifact)
```

## 6. Download and use the artifact

The following code example demonstrates the steps you can take to use an artifact you have logged and saved to the Weights & Biases servers.

1. First, initialize a new run object with **`wandb.init()`.**
2. Second, use the run objects [`wandb.Run.use_artifact()`](https://docs.coreweave.com/products/wandb/ref/python/experiments/run#use_artifact) method to tell Weights & Biases what artifact to use. This returns an artifact object.
3. Third, use the artifacts [`wandb.Artifact.download()`](https://docs.coreweave.com/products/wandb/ref/python/experiments/artifact#download) method to download the contents of the artifact.

```python theme={"system"}
# Create a W&B Run. Here we specify 'training' for 'type'
# because we will use this run to track training.
with wandb.init(project="artifacts-example", job_type="training") as run:

  # Query W&B for an artifact and mark it as input to this run
  artifact = run.use_artifact("bicycle-dataset:latest")

  # Download the artifact's contents
  artifact_dir = artifact.download()
```

Alternatively, you can use the Public API (`wandb.Api`) to export (or update data) data already saved in Weights & Biases outside of a Run. See [Track external files](https://docs.coreweave.com/products/wandb/artifacts/track-external-files.md) for more information.
