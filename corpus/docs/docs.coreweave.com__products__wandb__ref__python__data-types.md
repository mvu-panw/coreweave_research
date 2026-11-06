# Data Types overview

Source: https://docs.coreweave.com/products/wandb/ref/python/data-types

# Data Types overview

> Data Types in the W&B Python SDK for logging media and structured data

Data Types in W\&B are classes that wrap media and structured data for logging to runs. They include visualization components in the W\&B UI and handle data serialization, storage, and retrieval.

## Available data types

| Data Type | Description |
| - | - |
| [`Image`](https://docs.coreweave.com/products/wandb/ref/python/data-types/image) | Log images with support for masks, bounding boxes, and segmentation. |
| [`Video`](https://docs.coreweave.com/products/wandb/ref/python/data-types/video) | Track video data for model outputs or dataset samples. |
| [`Audio`](https://docs.coreweave.com/products/wandb/ref/python/data-types/audio) | Log audio samples for audio processing tasks. |
| [`Table`](https://docs.coreweave.com/products/wandb/ref/python/data-types/table) | Create tables that can contain mixed media types. |
| [`Plotly`](https://docs.coreweave.com/products/wandb/ref/python/data-types/plotly) | Log Plotly charts for data visualization. |
| [`Html`](https://docs.coreweave.com/products/wandb/ref/python/data-types/html) | Embed custom HTML content. |
| [`Object3D`](https://docs.coreweave.com/products/wandb/ref/python/data-types/object3d) | Visualize 3D point clouds and meshes. |
| [`Molecule`](https://docs.coreweave.com/products/wandb/ref/python/data-types/molecule) | Log molecular structures for computational chemistry. |

## Examples

This example uses an `Image`:

```python theme={"system"}
import wandb
import matplotlib.pyplot as plt

# Generate an image for demonstration purposes
path_to_img = "/path/to/cafe.png"
im = plt.imread(path_to_img)

# Initialize a new run
with wandb.init(project="awesome-project") as run:

    # Log the image
    run.log({"img": [wandb.Image(im, caption="Cafe")]})
```

This example uses a `Table` to log a table with mixed text and labels:

```python theme={"system"}
import wandb

# Initialize a new run
with wandb.init(project="visualize-predictions", name="tables") as run:

    # Create tabular data, using a list of lists
    data = [["Cat", "1", "1"],["Dog", "0", "-1"]]
    run.log({"Table 1": wandb.Table(data=data, columns=["Text", "Predicted Label", "True Label"])})

    # Create tabular data, using `wandb.Table.add_data()` method
    table = wandb.Table(columns=["Text", "Predicted Label", "True Label"])
    table.add_data("Cat", "1", "1")
    table.add_data("Dog", "0", "-1")
    run.log({"Table 2": table})
```
