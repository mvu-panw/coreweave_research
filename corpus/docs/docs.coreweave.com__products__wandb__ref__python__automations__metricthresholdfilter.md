# MetricThresholdFilter

Source: https://docs.coreweave.com/products/wandb/ref/python/automations/metricthresholdfilter

# MetricThresholdFilter

[View source](https://github.com/wandb/wandb/blob/main/wandb/automations/_run_metric_filters.py#L125)

## Class wandb.automations.MetricThresholdFilter

Filter that compares an **absolute** metric value against a user-defined threshold.

The value may be a single value or an aggregated result over a window of
multiple values.

```python theme={"system"}
*,
name: str,
agg_op: wandb.automations._run_metric_filters.Agg | None = None,
window_size: Annotated[int, Gt(gt=0)] = 1,
cmp_op: Literal['$gte', '$gt', '$lt', '$lte'],
threshold: Union[Annotated[int, Strict(strict=True)], Annotated[float, Strict(strict=True)]]
```

## Args

**name** `str`

No description provided.

**agg\_op** `wandb.automations._run_metric_filters.Agg | None`

No description provided.

**window\_size** `Annotated`

No description provided.

**cmp\_op** `Literal`

Comparison operator between the metric value (left) vs. the threshold (right).

**threshold** `Union`

No description provided.
