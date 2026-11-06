# 'str' = 'Confusion Matrix Curve',

Source: https://docs.coreweave.com/products/wandb/ref/python/custom-charts/confusion_matrix

# confusion_matrix()

[View source](https://github.com/wandb/wandb/blob/main/wandb/plot/confusion_matrix.py#L16)

## function wandb.plot.confusion\_matrix()

Constructs a confusion matrix from a sequence of probabilities or predictions.

```python theme={"system"}
probs: 'Sequence[Sequence[float]] | None' = None,
y_true: 'Sequence[T] | None' = None,
preds: 'Sequence[T] | None' = None,
class_names: 'Sequence[str] | None' = None,
title: 'str' = 'Confusion Matrix Curve',
split_table: 'bool' = False
```

## Args

**probs** `Sequence[Sequence[float]] | None`

A sequence of predicted probabilities for each class. The sequence shape should be (N, K) where N is the number of samples and K is the number of classes. If provided, `preds` should not be provided.

**y\_true** `Sequence[T] | None`

A sequence of true labels.

**preds** `Sequence[T] | None`

A sequence of predicted class labels. If provided, `probs` should not be provided.

**class\_names** `Sequence[str] | None`

Sequence of class names. If not provided, class names will be defined as "Class\_1", "Class\_2", etc.

**title** `str`

Title of the confusion matrix chart.

**split\_table** `bool`

Whether the table should be split into a separate section in the W\&B UI. If `True`, the table will be displayed in a section named "Custom Chart Tables". Default is `False`.

## Returns

`CustomChart`: A custom chart object that can be logged to W\&B. To log the chart, pass it to `wandb.log()`.

## Raises

* `ValueError`: If both `probs` and `preds` are provided or if the number of predictions and true labels are not equal. If the number of unique predicted classes exceeds the number of class names or if the number of unique true labels exceeds the number of class names.
* `wandb.Error`: If numpy is not installed.

## Examples

Logging a confusion matrix with random probabilities for wildlife
classification:

```python theme={"system"}
import numpy as np
import wandb

# Define class names for wildlife
wildlife_class_names = ["Lion", "Tiger", "Elephant", "Zebra"]

# Generate random true labels (0 to 3 for 10 samples)
wildlife_y_true = np.random.randint(0, 4, size=10)

# Generate random probabilities for each class (10 samples x 4 classes)
wildlife_probs = np.random.rand(10, 4)
wildlife_probs = np.exp(wildlife_probs) / np.sum(
    np.exp(wildlife_probs),
    axis=1,
    keepdims=True,
)

# Initialize W&B run and log confusion matrix
with wandb.init(project="wildlife_classification") as run:
    confusion_matrix = wandb.plot.confusion_matrix(
        probs=wildlife_probs,
        y_true=wildlife_y_true,
        class_names=wildlife_class_names,
        title="Wildlife Classification Confusion Matrix",
    )
    run.log({"wildlife_confusion_matrix": confusion_matrix})
```

In this example, random probabilities are used to generate a confusion
matrix.

Logging a confusion matrix with simulated model predictions and 85%
accuracy:

```python theme={"system"}
import numpy as np
import wandb

# Define class names for wildlife
wildlife_class_names = ["Lion", "Tiger", "Elephant", "Zebra"]

# Simulate true labels for 200 animal images (imbalanced distribution)
wildlife_y_true = np.random.choice(
    [0, 1, 2, 3],
    size=200,
    p=[0.2, 0.3, 0.25, 0.25],
)

# Simulate model predictions with 85% accuracy
wildlife_preds = [
    y_t
    if np.random.rand() < 0.85
    else np.random.choice([x for x in range(4) if x != y_t])
    for y_t in wildlife_y_true
]

# Initialize W&B run and log confusion matrix
with wandb.init(project="wildlife_classification") as run:
    confusion_matrix = wandb.plot.confusion_matrix(
        preds=wildlife_preds,
        y_true=wildlife_y_true,
        class_names=wildlife_class_names,
        title="Simulated Wildlife Classification Confusion Matrix",
    )
    run.log({"wildlife_confusion_matrix": confusion_matrix})
```

In this example, predictions are simulated with 85% accuracy to generate a
confusion matrix.
