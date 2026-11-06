# OnRunMetric

Source: https://docs.coreweave.com/products/wandb/ref/python/automations/onrunmetric

# OnRunMetric

[View source](https://github.com/wandb/wandb/blob/main/wandb/automations/events.py#L373)

## Class wandb.automations.OnRunMetric

A run metric satisfies a user-defined condition.

```python theme={"system"}
*,
event_type: Literal[RUN_METRIC_THRESHOLD, RUN_METRIC_CHANGE, RUN_METRIC_ZSCORE],
scope: Annotated[Union[wandb.automations.scopes.ProjectScope, Annotated[wandb.automations.scopes.TeamScope | wandb.automations.scopes.OrgScope, BeforeValidator(func=<function parse_scope>, json_schema_input_type=PydanticUndefined), Discriminator(discriminator='entity_type', custom_error_type=None, custom_error_message=None, custom_error_context=None)]], BeforeValidator(func=<function parse_scope>, json_schema_input_type=PydanticUndefined), Discriminator(discriminator='typename__', custom_error_type=None, custom_error_message=None, custom_error_context=None)],
filter: Annotated[wandb.automations.events.RunMetricFilter, Json, BeforeValidator(func=<function ensure_json>, json_schema_input_type=PydanticUndefined), PlainSerializer(func=<function to_json>, return_type=PydanticUndefined, when_used='always')]
```

## Args

**event\_type** `Literal`

No description provided.

**scope** `Annotated`

The scope of the event: must be a project or a team/org entity.

**filter** `Annotated`

Run and/or metric condition(s) that must be satisfied for this event to trigger.

## Examples

Define an event that triggers for any run in project "my-project" when
the average of the last 5 values of metric "my-metric" exceeds 123.45:

```python theme={"system"}
from wandb import Api
from wandb.automations import OnRunMetric, RunEvent

api = Api()
project = api.project(name="my-project")

event = OnRunMetric(
    scope=project,
    filter=RunEvent.metric("my-metric").avg(5).gt(123.45),
)
```
