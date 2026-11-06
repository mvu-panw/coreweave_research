# Custom Charts overview

Source: https://docs.coreweave.com/products/wandb/ref/python/custom-charts

# Custom Charts overview

> Use custom charts in the W&B Python SDK for interactive visualizations in project dashboards

Custom charts in W\&B are programmable through a group of functions in the `wandb.plot` namespace. These functions create interactive visualizations in W\&B project dashboards, and support common ML visualizations such as confusion matrices, ROC curves, and distribution plots.

## Available chart functions

| Function | Description |
| - | - |
| [`confusion_matrix()`](https://docs.coreweave.com/products/wandb/ref/python/custom-charts/confusion_matrix) | Generate confusion matrices for classification performance visualization. |
| [`roc_curve()`](https://docs.coreweave.com/products/wandb/ref/python/custom-charts/roc_curve) | Create Receiver Operating Characteristic curves for binary and multi-class classifiers. |
| [`pr_curve()`](https://docs.coreweave.com/products/wandb/ref/python/custom-charts/pr_curve) | Build Precision-Recall curves for classifier evaluation. |
| [`line()`](https://docs.coreweave.com/products/wandb/ref/python/custom-charts/line) | Construct line charts from tabular data. |
| [`scatter()`](https://docs.coreweave.com/products/wandb/ref/python/custom-charts/scatter) | Create scatter plots for variable relationships. |
| [`bar()`](https://docs.coreweave.com/products/wandb/ref/python/custom-charts/bar) | Generate bar charts for categorical data. |
| [`histogram()`](https://docs.coreweave.com/products/wandb/ref/python/custom-charts/histogram) | Build histograms for data distribution analysis. |
| [`line_series()`](https://docs.coreweave.com/products/wandb/ref/python/custom-charts/line_series) | Plot multiple line series on a single chart. |
| [`plot_table()`](https://docs.coreweave.com/products/wandb/ref/python/custom-charts/plot_table) | Create custom charts using Vega-Lite specifications. |

## Common use cases

### Model evaluation

* **Classification**: `confusion_matrix()`, `roc_curve()`, and `pr_curve()` for classifier evaluation
* **Regression**: `scatter()` for prediction vs. actual plots and `histogram()` for residual analysis
* **Vega-Lite Charts**: `plot_table()` for domain-specific visualizations

### Training monitoring

* **Learning Curves**: `line()` or `line_series()` for tracking metrics over epochs
* **Hyperparameter Comparison**: `bar()` charts for comparing configurations

### Data analysis

* **Distribution Analysis**: `histogram()` for feature distributions
* **Correlation Analysis**: `scatter()` plots for variable relationships

## Getting started

### Log a confusion matrix

```python theme={"system"}
import wandb

y_true = [0, 1, 2, 0, 1, 2]
y_pred = [0, 2, 2, 0, 1, 1]
class_names = ["class_0", "class_1", "class_2"]

# Initialize a run
with wandb.init(project="custom-charts-demo") as run:
    run.log({
        "conf_mat": wandb.plot.confusion_matrix(
            y_true=y_true, 
            preds=y_pred,
            class_names=class_names
        )
    })
```

### Build a scatter plot for feature analysis

```python theme={"system"}
import numpy as np

# Generate synthetic data
data_table = wandb.Table(columns=["feature_1", "feature_2", "label"])

with wandb.init(project="custom-charts-demo") as run:

    for _ in range(100):
        data_table.add_data(
            np.random.randn(), 
            np.random.randn(), 
            np.random.choice(["A", "B"])
        )

    run.log({
        "feature_scatter": wandb.plot.scatter(
            data_table, x="feature_1", y="feature_2",
            title="Feature Distribution"
        )
    })

```
