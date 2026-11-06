# Add Weights & Biases to a Python library

Source: https://docs.coreweave.com/products/wandb/integrations/add-wandb-to-any-library

# Add Weights & Biases to a Python library

> Add Weights & Biases to your Python library for experiment tracking, system monitoring, and model management.

This guide describes patterns for integrating Weights & Biases into a Python library, framework, or SDK. It covers dependency management, authentication, optional logging, run initialization, artifacts, hyperparameter tuning, and distributed execution.

Use this guide when your integration spans reusable library code rather than a single training script or notebook. For an introduction to Weights & Biases, see [Experiment Tracking](https://docs.coreweave.com/products/wandb/track.md).

## Design the integration

Before adding Weights & Biases to your library, decide:

* Whether wandb is a required or optional dependency.
* Whether users can run your library without saving or uploading Weights & Biases data.
* Which configuration values, metrics, and artifacts your library logs.
* Whether to support hyperparameter tuning with W\&B Sweeps.
* Whether to share artifacts, such as models and datasets, through your organization's Registry.
* How your library handles distributed training and multiple processes.

These decisions determine how your library imports Weights & Biases, manages run lifecycles, and behaves when Weights & Biases is unavailable.

## Decide how to install Weights & Biases

Choose whether to install Weights & Biases automatically with your library or expose it as an optional feature.

### Require Weights & Biases as a dependency

If Weights & Biases is central to your library, add `wandb` to its dependencies.

For a `requirements.txt` file:

```txt title="requirements.txt" type="text" theme={"system"}
torch
wandb
```

For a `pyproject.toml` file:

```toml title="pyproject.toml" type="toml" theme={"system"}
[project]
name = "my_awesome_lib"
version = "0.1.0"
dependencies = [
    "torch",
    "wandb",
]
```

Consider specifying a compatible version range based on the Weights & Biases features your integration uses.

### Make Weights & Biases an optional dependency

If Weights & Biases is an optional feature, enable installation of your library without `wandb`.

Declare Weights & Biases as an optional dependency in `pyproject.toml`:

```toml title="pyproject.toml" theme={"system"}
[project]
name = "my_awesome_lib"
version = "0.1.0"
dependencies = [
    "torch",
]

[project.optional-dependencies]
wandb = [
    "wandb",
]
```

Then install the integration with:

```bash theme={"system"}
pip install "my_awesome_lib[wandb]"
```

## Authenticate users

Weights & Biases uses API keys to authenticate users and machines. Before you can log runs from your library, you must generate an API key and make it available to the `wandb` client.

Weights & Biases supports authentication through the CLI, environment variables, and `wandb.login()`.

### Create an API key

> [!NOTE]
>
> For a more streamlined approach, go to [User settings](https://forge.coreweave.com/settings) and create an API key. Copy the API key immediately and save it in a secure location such as a password manager.

### Authenticate from the command line

From your terminal, run:

```bash theme={"system"}
wandb login
```

Weights & Biases prompts you to enter an API key.

Alternatively, set the `WANDB_API_KEY` environment variable:

```bash theme={"system"}
export WANDB_API_KEY="<api_key>"
```

For more information, see [Environment variables](https://docs.coreweave.com/products/wandb/track/environment-variables.md).

### Authenticate from Python

In an interactive Python environment or notebook, call:

```python theme={"system"}
import wandb

wandb.login()
```

Avoid calling [`wandb.login()`](https://docs.coreweave.com/products/wandb/ref/python/functions/login) automatically from reusable library code because it can interrupt noninteractive workflows.

## Make Weights & Biases logging optional

Choose whether Weights & Biases saves or uploads run data.

| Mode | Behavior |
| - | - |
| `disabled` | Deactivates Weights & Biases logging. Weights & Biases does not save or upload run data. Calls to Weights & Biases methods have no effect. |
| `offline` | Saves run data locally without uploading it. You can upload the run later with [`wandb sync`](https://docs.coreweave.com/products/wandb/ref/cli/wandb-sync). |

Use `disabled` when you do not want to save run data. Use `offline` when you want to save data locally for later upload.

### Use `disabled` mode

Pass `mode="disabled"` to `wandb.init()`:

```python theme={"system"}
with wandb.init(mode="disabled") as run:
    # Training logic.
```

Or set `WANDB_MODE` in the environment:

```bash theme={"system"}
export WANDB_MODE=disabled
```

You can also set the mode with the W\&B CLI:

```bash theme={"system"}
wandb disabled
```

### Use `offline` mode

Pass `mode="offline"` to `wandb.init()`:

```python theme={"system"}
with wandb.init(mode="offline") as run:
    # Training logic.
```

Or set `WANDB_MODE` in the environment:

```bash theme={"system"}
export WANDB_MODE=offline
```

In Python, set the environment variable before calling `wandb.init()`:

```python theme={"system"}
import os

os.environ["WANDB_MODE"] = "offline"
```

You can also set the mode with the W\&B CLI:

```bash theme={"system"}
wandb offline
```

Upload an offline run later with:

```bash theme={"system"}
wandb sync <run_directory>
```

## Initialize a run

After authenticating, initialize a [run](https://docs.coreweave.com/products/wandb/runs.md) to log metrics, [configuration](https://docs.coreweave.com/products/wandb/track/config.md) values, and [artifacts](https://docs.coreweave.com/products/wandb/artifacts.md) from your library.

Call [`wandb.init()`](https://docs.coreweave.com/products/wandb/ref/python/functions/init) and specify the project and team entity. If you omit the project, Weights & Biases stores the run in the default `"uncategorized"` project.

Use `wandb.init()` as a context manager around the training loop. When the block exits, Weights & Biases finishes the run and processes pending data before the process ends.

For example, suppose your library contains the following training loop:

```python icon="python" title="Python" theme={"system"}
import random # For simulating data

def model(training_data: int) -> int:
    """Model simulation for demonstration purposes."""
    return training_data * 2 + random.randint(-1, 1)  

# Simulate weights and noise
weights = random.random() # Initialize random weights
noise = random.random() / 5  # Small random noise to simulate noise

for epoch in range(epochs):
    xb = weights + noise  # Simulated input training data
    yb = weights + noise * 2  # Simulated target output (double the input noise)
    
    y_pred = model(xb)  # Model prediction
    loss = (yb - y_pred) ** 2  # Mean Squared Error loss

    print(f"epoch={epoch}, loss={loss}")
```

To integrate Weights & Biases, initialize a run with a context manager, pass configuration values to `wandb.init()`, and log metrics with `wandb.Run.log()`:

```python icon="python" title="Python" highlight={2,13-16,19,30-33} theme={"system"}
import random # For simulating data
import wandb

def model(training_data: int) -> int:
    """Model simulation for demonstration purposes."""
    return training_data * 2 + random.randint(-1, 1)  

# Simulate weights and noise
weights = random.random() # Initialize random weights
noise = random.random() / 5  # Small random noise to simulate noise

# Hyperparameters and configuration
config = {
    "epochs": 10,  # Number of epochs to train
    "learning_rate": 0.01,  # Learning rate for the optimizer
}

# Use context manager to initialize and close W&B runs
with wandb.init(entity="your-entity", project="your-project-name", config=config) as run:    
    # Simulate training loop
    for epoch in range(config["epochs"]):
        xb = weights + noise  # Simulated input training data
        yb = weights + noise * 2  # Simulated target output (double the input noise)
        
        y_pred = model(xb)  # Model prediction
        loss = (yb - y_pred) ** 2  # Mean Squared Error loss

        print(f"epoch={epoch}, loss={loss}")
        # Log epoch and loss to W&B
        run.log({
            "epoch": epoch,
            "loss": loss,
        })
```

> [!TIP]
>
> **When to call `wandb.init()`**
>
> Call `wandb.init()` before the work you want Weights & Biases to monitor. Use it as a context manager around the entire training loop so the run captures relevant standard output, standard error, and error messages for debugging.

The [next section](#log-configuration-and-metrics) describes in detail how to log configuration values and metrics from your library.

## Log configuration and metrics

Log configuration values and metrics to Weights & Biases so you, and members of your team, can [compare](https://docs.coreweave.com/products/wandb/runs/compare-runs.md), [filter](https://docs.coreweave.com/products/wandb/runs/filter-runs.md#example-filter-run-configuration-values-with-contains), [group](https://docs.coreweave.com/products/wandb/runs/grouping.md), and [reproduce](https://docs.coreweave.com/products/wandb/track/reproduce_experiments.md) experiments.

### Log configuration values

Pass a [configuration](https://docs.coreweave.com/products/wandb/track/config.md) dictionary to `wandb.init()` to record hyperparameters and other metadata.

Use descriptive keys and JSON-serializable values:

```python theme={"system"}
config = {
    "batch_size": 32,
    "learning_rate": 0.001,
    "optimizer": "adam",
    "model": {
        "type": "resnet",
        "depth": 50,
    },
    "dataset": {
        "name": "CIFAR-10",
        "num_classes": 10,
    },
}
```

Pass the dictionary to `wandb.init()`:

```python theme={"system"}
with wandb.init(entity="your-entity", project="your-project-name", config=config) as run:
    # Training logic.
```

Some values might not be available when the run starts. Add them later with `wandb.Run.config.update()`:

```python theme={"system"}
run.config.update(
    {
        "model_parameters": 3500,
    }
)
```

For more information, see [Configure experiments](https://docs.coreweave.com/products/wandb/track/config.md).

### Log metrics

Log metrics such as loss or accuracy during training. Create a dictionary where each key is the name of a metric and the value is the metric value. Pass this dictionary to [`wandb.Run.log()`](https://docs.coreweave.com/products/wandb/ref/python/experiments/run#method-run-log).

The following code snippet logs training and validation metrics to Weights & Biases:

```python icon="python" title="Python" theme={"system"}
import wandb

with wandb.init(entity="your-entity", project="your-project-name") as run:
    metrics = {
        "train/loss": 0.4,
        "train/learning_rate": 0.4,
        "val/loss": 0.5, 
        "val/accuracy": 0.7
    }
    run.log(metrics)
```

Use prefixes such as `train/` and `val/` to group related metrics.

For guidance on logging supported data types, automatically tracked data, and best practices, see [Log metrics and data](https://docs.coreweave.com/products/wandb/track/log.md).

To track models and datasets, see the [Track models and datasets with artifacts](#track-models-and-datasets-with-artifacts) section.

### Define a custom log axis

By default, Weights & Biases plots logged metrics against an automatically incremented step. Each call to `wandb.Run.log()` advances the step.

Use `wandb.Run.define_metric()` to plot a metric against another value, such as an epoch or global step.

The following example defines `x_axis_squared` as the x-axis for `validation_loss`. For each loop iteration, `x_axis_squared` is the square of the index `i`, and `validation_loss` is a randomly generated value:

```python title="Python" icon="python" theme={"system"}
import wandb
import random

with wandb.init() as run:
    run.define_metric(step_metric = "x_axis_squared", name = "validation_loss")

    for i in range(10):
        log_dict = {
            "x_axis_squared": i**2,
            "validation_loss": random.random(),
        }
        run.log(log_dict)
```

For more information, see [Define a custom log axis](https://docs.coreweave.com/products/wandb/track/log/customize-logging-axes.md).

## Track models and datasets with artifacts

In addition to metrics, you can persist the models and datasets your library produces or consumes so that you, and members of your team, can reproduce and compare runs.

Use [W\&B Artifacts](https://docs.coreweave.com/products/wandb/artifacts.md) to version models, datasets, and other files that your library produces or consumes.

Before adding artifact support, decide:

* Which files to log.
* Whether artifact logging is optional.
* How frequently to log checkpoints.
* How to name artifacts and aliases.
* Which artifacts represent run inputs and outputs.

### Log model checkpoints

Log model checkpoints as artifacts so you can recover, version, and share trained weights. Include the run ID in the artifact name to associate each checkpoint with its source run.

The following example logs a checkpoint every 10 epochs. It creates an artifact whose name includes the run ID, adds model weights from a local directory, and logs the artifact with a [custom alias](https://docs.coreweave.com/products/wandb/artifacts/create-a-custom-alias.md).

```python title="Python" icon="python" theme={"system"}
import wandb
with wandb.init(entity="your-entity", project="your-project-name") as run:

    # Training data and model training logic here

    if epoch % 10 == 0: # Log model checkpoint every 10 epochs

        metadata = {"eval/accuracy": 0.8, "train/steps": 800} 

        artifact = wandb.Artifact(
                        name=f"model-{run.id}", 
                        metadata=metadata, 
                        type="model"
                        )
        artifact.add_dir("./models/output_model") # local directory where the model weights are stored

        run.log_artifact(artifact, aliases=f"epoch_{epoch}")
```

### Track run inputs

Use [`wandb.Run.use_artifact()`](https://docs.coreweave.com/products/wandb/ref/python/experiments/run#method-run-use_artifact) when a run consumes an artifact, such as a dataset or model checkpoint. Weights & Biases records the artifact as an input to the run.

Specify the name of the artifact and an optional alias to reference a specific version of that artifact. The name of the artifact is in the format `artifact_name:version` or `artifact_name:alias`.

```python title="Python" icon="python" theme={"system"}
import wandb

# Initialize a run
with wandb.init(entity="your-entity", project="your-project") as run:
  # Get artifact, mark it as a dependency
  artifact = run.use_artifact(artifact_or_name="artifact_name:alias_or_version")
```

### Track run outputs

Use [`wandb.Run.log_artifact()`](https://docs.coreweave.com/products/wandb/ref/python/experiments/run#method-run-log_artifact) to log an artifact as an output of a run.

1. Create an artifact with `wandb.Artifact()`.
2. Add one or more files to the artifact.
3. Log the artifact with `wandb.Run.log_artifact()`.

```python theme={"system"}
import wandb

# Initialize a run
with wandb.init(entity="your-entity", project="project-name") as run:
  
  # Create an artifact
  artifact = wandb.Artifact(name = "artifact-name", type = "artifact-type")
  artifact.add_file(local_path = "path/to/file", name="optional-filename") # Add a file to the artifact

  # Log the artifact as an output of the run
  run.log_artifact(artifact_or_path = artifact)
```

For more information about creating, managing, and using artifacts, see [Artifacts](https://docs.coreweave.com/products/wandb/artifacts.md).

### Download artifacts

Use the [W\&B Public API](https://docs.coreweave.com/products/wandb/ref/python/public-api.md) to download an artifact without creating a run or recording a run input relationship.

```python theme={"system"}
import wandb

api = wandb.Api()

artifact = api.artifact(
    "<entity>/<project>/<artifact_name>:<alias_or_version>"
)

local_path = artifact.download()
```

For information, see [Download and use artifacts](https://docs.coreweave.com/products/registry/download_use_artifact.md).

## Link artifacts to the Registry

Use [Registry](https://docs.coreweave.com/products/registry.md) to share and manage artifact versions across teams.

Before you link an artifact version, decide:

* Which artifact versions to share.
* Which [collections](https://docs.coreweave.com/products/registry/create_collection.md) to link them to.
* Which [registry](https://docs.coreweave.com/products/registry.md) to publish them in.

> [!NOTE]
>
> The destination registry must already exist.

The following example logs an artifact and links it to a collection in a registry:

```python theme={"system"}
import wandb
import random

# Specify the name of the collection and registry
# you want to publish the artifact to
COLLECTION_NAME = "collection-name"
REGISTRY_NAME = "registry-name"

# Initialize a W&B Run to track the artifact
with wandb.init(project="project-name") as run:
    # Create a simulated model file so that you can log it
    with open("my_model.txt", "w") as f:
        f.write("Model: " + str(random.random()))

    # Log the artifact to W&B
    logged_artifact = run.log_artifact(
        artifact_or_path="./my_model.txt", 
        name="artifact-name",
        type="artifact-type" # Specifies artifact type
    )

    # Link the artifact to the registry
    run.link_artifact(
        artifact=logged_artifact, 
        target_path=f"wandb-registry-{REGISTRY_NAME}/{COLLECTION_NAME}"
    )
```

For more information, see [Link an artifact version to a collection](https://docs.coreweave.com/products/registry/link_version.md).

## Tune hyperparameters

If your library supports hyperparameter tuning, integrate [W\&B Sweeps](https://docs.coreweave.com/products/wandb/sweeps.md) to run grid, random, or Bayesian searches.

> [!TIP]
>
> Weights & Biases recommends that you keep the sweep configuration separate from the underlying training logic. The training function should read its parameters from `wandb.Run.config` rather than depending directly on sweep-specific logic.

For more information, see [Sweeps](https://docs.coreweave.com/products/wandb/sweeps.md).

## Support distributed training

If your library supports multiple processes or machines, define which processes create runs and log data.

Common approaches include:

* Log only from the main process. This approach avoids duplicate metrics and artifacts.
* Create one run for each process and group the runs with a shared `group` value.

For more information, see [Log distributed training experiments](https://docs.coreweave.com/products/wandb/track/log/distributed-training.md).
