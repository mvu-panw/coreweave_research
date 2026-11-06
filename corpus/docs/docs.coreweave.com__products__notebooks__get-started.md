# Get started

Source: https://docs.coreweave.com/products/notebooks/get-started

# Get started

The following guide will help you get started with Notebooks, from creating your first notebook to running a training experiment.

## Create your first notebook

1. Navigate to your project's workspace.
2. Select **Notebooks** from the project sidebar.
3. Click **Create notebook**.

See the [Create and manage notebooks](https://docs.coreweave.com/products/notebooks/create-notebook.md) for more information.

## Run a training experiment

This mock training script logs simulated accuracy and loss metrics to W\&B. Copy and paste the following code into a Python script or notebook cell and run it:

1. Select **Python** to create a new code cell.

2. Copy and paste the following code into the cell:

   ```python theme={"system"}
   import random
   import wandb

   PROJECT = "your-project-name"

   # Dictionary with hyperparameters
   config = {
       'epochs' : 10,
       'lr' : 0.01
   }

   with wandb.init(project=PROJECT, config=config) as run:
       offset = random.random() / 5
       print(f"lr: {config['lr']}")
       
       # Simulate a training run
       for epoch in range(2, config['epochs']):
           acc = 1 - 2**-config['epochs'] - random.random() / config['epochs'] - offset
           loss = 2**-config['epochs'] + random.random() / config['epochs'] + offset
           print(f"epoch={config['epochs']}, accuracy={acc}, loss={loss}")
           run.log({"accuracy": acc, "loss": loss})
   ```

3. Press **Command + Enter** on macOS or **Ctrl+Enter** on Windows or Linux. Alternatively, click **Play** () next to the cell.

## View your experiment

View the accuracy and loss metrics logged during the training experiment:

1. Select **Workspace** from the project sidebar.
2. Review the runs and visualizations in the workspace. The [runs](https://docs.coreweave.com/products/wandb/runs.md) list shows each run logged to the project and its details. [Workspace panels](https://docs.coreweave.com/products/wandb/app/features/panels.md) display visualizations of the metrics logged during each run.

## Save the notebook

W\&B stores your notebook as a [W\&B Artifact](https://docs.coreweave.com/products/wandb/artifacts.md) and automatically saves changes as a new [Artifact version](https://docs.coreweave.com/products/wandb/artifacts/create-a-new-artifact-version.md) every 30 seconds and when the notebook's compute session stops.

To save your latest changes immediately, use one of the following options:

* Press **Command+S** on macOS or **Ctrl+S** on Windows or Linux.
* In the notebook footer, click **Save** ().
