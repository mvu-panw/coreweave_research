# RunStateFilter

Source: https://docs.coreweave.com/products/wandb/ref/python/automations/runstatefilter

# RunStateFilter

[View source](https://github.com/wandb/wandb/blob/main/wandb/automations/events.py#L166)

## Class wandb.automations.RunStateFilter

Represents a filter for triggering events based on changes in run states.

```python theme={"system"}
*,
run_filter: Annotated[wandb._filters.operators.And | wandb._filters.operators.Or | wandb._filters.operators.Nor | wandb._filters.operators.Not | wandb._filters.operators.Lt | wandb._filters.operators.Gt | wandb._filters.operators.Lte | wandb._filters.operators.Gte | wandb._filters.operators.Eq | wandb._filters.operators.Ne | wandb._filters.operators.In | wandb._filters.operators.NotIn | wandb._filters.operators.Exists | wandb._filters.operators.Regex | wandb._filters.operators.Contains | wandb._filters.operators.Size | wandb._filters.operators.All | wandb._filters.expressions.FilterExpr | dict[str, Any], Json, BeforeValidator(func=<function ensure_json>, json_schema_input_type=PydanticUndefined), PlainSerializer(func=<function to_json>, return_type=PydanticUndefined, when_used='always'), AfterValidator(func=<function wrap_run_filter>)] = And(()),
run_state_filter: wandb.automations._run_state_filters.StateFilter
```

## Args

**run\_filter** `Annotated`

Filters that must match any runs that will trigger this event.

**run\_state\_filter** `StateFilter`

Run state condition(s) that must be satisfied for this event to trigger.
