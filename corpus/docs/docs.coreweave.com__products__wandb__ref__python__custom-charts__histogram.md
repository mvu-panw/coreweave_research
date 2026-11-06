# 'str' = '',

Source: https://docs.coreweave.com/products/wandb/ref/python/custom-charts/histogram

# histogram()

[View source](https://github.com/wandb/wandb/blob/main/wandb/plot/histogram.py#L12)

## function wandb.plot.histogram()

Constructs a histogram chart from a W\&B Table.

```python theme={"system"}
table: 'wandb.Table',
value: 'str',
title: 'str' = '',
split_table: 'bool' = False
```

## Args

**table** `wandb.Table`

The W\&B Table containing the data for the histogram.

**value** `str`

The label for the bin axis (x-axis).

**title** `str`

The title of the histogram plot.

**split\_table** `bool`

Whether the table should be split into a separate section in the W\&B UI. If `True`, the table will be displayed in a section named "Custom Chart Tables". Default is `False`.

## Returns

`CustomChart`: A custom chart object that can be logged to W\&B. To log the chart, pass it to `wandb.log()`.

## Examples

```python theme={"system"}
import math
import random
import wandb

# Generate random data
data = [[i, random.random() + math.sin(i / 10)] for i in range(100)]

# Create a W&B Table
table = wandb.Table(
    data=data,
    columns=["step", "height"],
)

# Create a histogram plot
histogram = wandb.plot.histogram(
    table,
    value="height",
    title="My Histogram",
)

# Log the histogram plot to W&B
with wandb.init(...) as run:
    run.log({"histogram-plot1": histogram})
```
