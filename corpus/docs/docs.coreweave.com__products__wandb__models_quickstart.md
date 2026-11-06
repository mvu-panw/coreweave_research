# Get Started with Weights & Biases

Source: https://docs.coreweave.com/products/wandb/models_quickstart

# Get Started with Weights & Biases

> Track experiments, log metrics, and visualize results with Weights & Biases in a few lines of code.

Learn when and how to use Weights & Biases to track, share, and manage model artifacts in your machine learning workflows. This page covers logging experiments, generating reports, and accessing logged data using the appropriate W\&B API for each task.

This tutorial uses the following:

* [W\&B Python SDK](https://docs.coreweave.com/products/wandb/ref/python.md) (`wandb.sdk`): to log and monitor experiments during training.
* [W\&B Public API](https://docs.coreweave.com/products/wandb/ref/python/public-api.md) (`wandb.apis.public`): to query and analyze logged experiment data.
* [W\&B Reports and Workspaces API](https://docs.coreweave.com/products/wandb/ref/wandb_workspaces) (`wandb.wandb-workspaces`): to create a report to summarize findings.

## Sign up and create an API key

To authenticate your machine with Weights & Biases, you must first generate an API key at [forge.coreweave.com/settings](https://forge.coreweave.com/settings). Copy the API key and store it securely.

## Install and import packages

Install the Weights & Biases library and some other packages you will need for this walkthrough.

```python theme={"system"}
pip install wandb
```

Import W\&B Python SDK:

```python theme={"system"}
import wandb
```

Specify the entity of your team in the following code block:

```python theme={"system"}
TEAM_ENTITY = "team_entity" # Replace with your team entity
PROJECT = "my-awesome-project"
```

## Train a model

The following code simulates a basic machine learning workflow: training a model, logging metrics, and saving the model as an artifact.

Use the W\&B Python SDK (`wandb.sdk`) to interact with Weights & Biases during training. Log the loss using [`wandb.Run.log()`](https://docs.coreweave.com/products/wandb/ref/python/experiments/run#method-runlog), then save the trained model as an artifact using [`wandb.Artifact`](https://docs.coreweave.com/products/wandb/ref/python/experiments/artifact) before finally adding the model file using [`Artifact.add_file`](https://docs.coreweave.com/products/wandb/ref/python/experiments/artifact#add_file).

```python theme={"system"}
import random # For simulating data

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
with wandb.init(entity=TEAM_ENTITY, project=PROJECT, config=config) as run:    
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

    # Unique name for the model artifact,
    model_artifact_name = f"model-demo"  

    # Local path to save the simulated model file
    PATH = "model.txt" 

    # Save model locally
    with open(PATH, "w") as f:
        f.write(str(weights)) # Saving model weights to a file

    # Create an artifact object
    # Add locally saved model to artifact object
    artifact = wandb.Artifact(name=model_artifact_name, type="model", description="My trained model")
    artifact.add_file(local_path=PATH)
    artifact.save()
```

The key takeaways from the previous code block are:

* Use `wandb.Run.log()` to log metrics during training.
* Use `wandb.Artifact` to save models (datasets, and so forth) as an artifact to your Weights & Biases project.

Now that you have trained a model and saved it as an artifact, you can publish it to a registry in Weights & Biases. Use [`wandb.Run.use_artifact()`](https://docs.coreweave.com/products/wandb/ref/python/experiments/run#method-runuse_artifact) to retrieve the artifact from your project and prepare it for publication in the Model registry. `wandb.Run.use_artifact()` serves two key purposes:

* Retrieves the artifact object from your project.
* Marks the artifact as an input to the run, ensuring reproducibility and traceability. See [Create and view lineage map](https://docs.coreweave.com/products/registry/lineage.md) for details.

## View the training data in the dashboard

Navigate to your Weights & Biases dashboard. Select the **Projects** tabs and search for `my-awesome-project` (or whatever you used as a project name above). Click this to enter the workspace for your project.

From here, you can see details about every run you've done. In this screenshot, the code was re-run several times, generating a number of runs, each of which is given a randomly-generated name.

![Weights & Biases project page with multiple runs in a table view, including run names, metrics, and status information](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/_media/quickstart_image.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=bd51b523b4bce2c7009d3877740b7a96)

## Publish the model to the Registry

To share the model with others in your organization, publish it to a [collection](https://docs.coreweave.com/products/registry/create_collection.md) using `wandb.Run.link_artifact()`. The following code links the artifact to a [registry](https://docs.coreweave.com/products/registry.md), making it accessible to your team.

```python theme={"system"}
# Artifact name specifies the specific artifact version within our team's project
artifact_name = f'{TEAM_ENTITY}/{PROJECT}/{model_artifact_name}:v0'
print("Artifact name: ", artifact_name)

REGISTRY_NAME = "DemoRegistry" # Name of the registry
COLLECTION_NAME = "DemoModels"  # Name of the collection in the registry

# Create a target path for our artifact in the registry
target_path = f"wandb-registry-{REGISTRY_NAME}/{COLLECTION_NAME}"
print("Target path: ", target_path)

with wandb.init(entity=TEAM_ENTITY, project=PROJECT) as run:
    model_artifact = run.use_artifact(artifact_or_name=artifact_name, type="model")
    run.link_artifact(artifact=model_artifact, target_path=target_path)
```

After running `wandb.Run.link_artifact()`, the model artifact will be in the `DemoModels` collection in your registry. From there, you can view details such as the version history, [lineage map](https://docs.coreweave.com/products/registry/lineage.md), and other [metadata](https://docs.coreweave.com/products/registry/registry_cards.md).

For additional information on how to link artifacts to a registry, see [Link artifacts to a registry](https://docs.coreweave.com/products/registry/link_version.md).

## Retrieve model artifact from registry for inference

To use a model for inference, use `wandb.Run.use_artifact()` to retrieve the published artifact from the registry. This returns an artifact object that you can then use [`wandb.Artifact.download()`](https://docs.coreweave.com/products/wandb/ref/python/experiments/artifact#method-artifactdownload) to download the artifact to a local file.

```python theme={"system"}
REGISTRY_NAME = "DemoRegistry"  # Name of the registry
COLLECTION_NAME = "DemoModels"  # Name of the collection in the registry
VERSION = 0 # Version of the artifact to retrieve

model_artifact_name = f"wandb-registry-{REGISTRY_NAME}/{COLLECTION_NAME}:v{VERSION}"
print(f"Model artifact name: {model_artifact_name}")

with wandb.init(entity=TEAM_ENTITY, project=PROJECT) as run:
    registry_model = run.use_artifact(artifact_or_name=model_artifact_name)
    local_model_path = registry_model.download()
```

For more information on how to retrieve artifacts from a registry, see [Download an artifact from a registry](https://docs.coreweave.com/products/registry/download_use_artifact.md).

Depending on your machine learning framework, you may need to recreate the model architecture before loading the weights. This is left as an exercise for the reader, as it depends on the specific framework and model you are using.

## Share your findings with a report

> [!NOTE]
>
> W\&B Report and Workspace API is in Public Preview.

Create and share a [report](https://docs.coreweave.com/products/wandb/reports.md) to summarize your work. To create a report programmatically, use the [W\&B Report and Workspace API](https://docs.coreweave.com/products/wandb/ref/wandb_workspaces/reports.md).

First, install the W\&B Reports API:

```bash theme={"system"}
pip install wandb wandb-workspaces -qqq
```

The following code block creates a report with multiple blocks, including markdown, panel grids, and more. You can customize the report by adding more blocks or changing the content of existing blocks.

The output of the code block prints a link to the URL report created. You can open this link in your browser to view the report.

```python theme={"system"}
import wandb_workspaces.reports.v2 as wr

experiment_summary = """This is a summary of the experiment conducted to train a simple model using W&B."""
dataset_info = """The dataset used for training consists of synthetic data generated by a simple model."""
model_info = """The model is a simple linear regression model that predicts output based on input data with some noise."""

report = wr.Report(
    entity=TEAM_ENTITY,
    project=PROJECT,
    title="My Awesome Model Training Report",
    description=experiment_summary,
    blocks= [
        wr.TableOfContents(),
        wr.H2("Experiment Summary"),
        wr.MarkdownBlock(text=experiment_summary),
        wr.H2("Dataset Information"),
        wr.MarkdownBlock(text=dataset_info),
        wr.H2("Model Information"),
        wr.MarkdownBlock(text = model_info),
        wr.PanelGrid(
            panels=[
                wr.LinePlot(title="Train Loss", x="Step", y=["loss"], title_x="Step", title_y="Loss")
                ],
            ),  
    ]

)

# Save the report to W&B
report.save()
```

For more information on how to create a report programmatically or how to create a report interactively with the W\&B App, see [Create a report](https://docs.coreweave.com/products/wandb/reports/create-a-report.md).

## Query the registry

Use the [W\&B Public APIs](https://docs.coreweave.com/products/wandb/ref/python/public-api.md) to query, analyze, and manage historical data from Weights & Biases. This can be useful for tracking the lineage of artifacts, comparing different versions, and analyzing the performance of models over time.

The following code block demonstrates how to query the Model registry for all artifacts in a specific collection. It retrieves the collection and iterates through its versions, printing out the name and version of each artifact.

```python theme={"system"}
import wandb

# Initialize wandb API
api = wandb.Api()

# Find all artifact versions that contains the string `model` and 
# has either the tag `text-classification` or an `latest` alias
registry_filters = {
    "name": {"$regex": "model"}
}

# Use logical $or operator to filter artifact versions
version_filters = {
    "$or": [
        {"tag": "text-classification"},
        {"alias": "latest"}
    ]
}

# Returns an iterable of all artifact versions that match the filters
artifacts = api.registries(filter=registry_filters).collections().versions(filter=version_filters)

# Print out the name, collection, aliases, tags, and created_at date of each artifact found
for art in artifacts:
    print(f"artifact name: {art.name}")
    print(f"collection artifact belongs to: { art.collection.name}")
    print(f"artifact aliases: {art.aliases}")
    print(f"tags attached to artifact: {art.tags}")
    print(f"artifact created at: {art.created_at}\n")
```

For more information on querying the registry, see the [Query registry items](https://docs.coreweave.com/products/registry/search_registry.md#query-registry-items-with-mongodb-style-queries).
