# MetricZScoreFilter

Source: https://docs.coreweave.com/products/wandb/ref/python/automations/metriczscorefilter

# MetricZScoreFilter

[View source](https://github.com/wandb/wandb/blob/main/wandb/automations/_run_metric_filters.py#L201)

## Class wandb.automations.MetricZScoreFilter

Filter that compares a metric's z-score against a user-defined threshold.

```python theme={"system"}
*,
name: str,
window_size: Annotated[int, Gt(gt=0)] = 30,
threshold: Union[Annotated[int, Gt(gt=0)], Annotated[float, Gt(gt=0)]] = 3.0,
change_dir: wandb.automations._run_metric_filters.ChangeDir = ANY
```

## Args

**name** `str`

Name of the observed metric.

**window\_size** `Annotated`

Size of the window to calculate the metric mean and standard deviation over.

**threshold** `Union`

Threshold for the z-score.

**change\_dir** `ChangeDir`

Direction of the z-score change to watch for.
