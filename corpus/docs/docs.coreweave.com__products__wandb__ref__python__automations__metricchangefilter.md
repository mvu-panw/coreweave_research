# MetricChangeFilter

Source: https://docs.coreweave.com/products/wandb/ref/python/automations/metricchangefilter

# MetricChangeFilter

[View source](https://github.com/wandb/wandb/blob/main/wandb/automations/_run_metric_filters.py#L152)

## Class wandb.automations.MetricChangeFilter

Filter that compares a **change** in a metric value to a user-defined threshold.

The change is calculated over "tumbling" windows, i.e. the difference
between the current window and the non-overlapping prior window.

```python theme={"system"}
*,
name: str,
agg_op: wandb.automations._run_metric_filters.Agg | None = None,
current_window_size: Annotated[int, Gt(gt=0)] = 1,
cmp: NoneType = None,
change_amount: Union[Annotated[int, Gt(gt=0)], Annotated[float, Gt(gt=0)]],
prior_window_size: Annotated[int, Gt(gt=0)] = <factory>,
change_type: wandb.automations._run_metric_filters.ChangeType,
change_dir: wandb.automations._run_metric_filters.ChangeDir
```

## Args

**name** `str`

No description provided.

**agg\_op** `wandb.automations._run_metric_filters.Agg | None`

No description provided.

**current\_window\_size** `Annotated`

No description provided.

**cmp** `NoneType`

Ignored.

**change\_amount** `Union`

No description provided.

**prior\_window\_size** `Annotated`

Size of the "prior" metric aggregation window (ignored if `agg` is `None`).

If omitted, defaults to the size of the current window.

**change\_type** `ChangeType`

No description provided.

**change\_dir** `ChangeDir`

No description provided.
