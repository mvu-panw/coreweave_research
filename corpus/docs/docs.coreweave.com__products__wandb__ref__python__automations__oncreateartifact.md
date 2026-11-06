# OnCreateArtifact

Source: https://docs.coreweave.com/products/wandb/ref/python/automations/oncreateartifact

# OnCreateArtifact

[View source](https://github.com/wandb/wandb/blob/main/wandb/automations/events.py#L338)

## Class wandb.automations.OnCreateArtifact

A new artifact is created.

```python theme={"system"}
*,
event_type: Literal[CREATE_ARTIFACT] = CREATE_ARTIFACT,
scope: Annotated[wandb.automations.scopes._ArtifactSequenceScope | wandb.automations.scopes._ArtifactPortfolioScope, BeforeValidator(func=<function parse_scope>, json_schema_input_type=PydanticUndefined), Discriminator(discriminator='typename__', custom_error_type=None, custom_error_message=None, custom_error_context=None)],
filter: Annotated[wandb._filters.operators.And | wandb._filters.operators.Or | wandb._filters.operators.Nor | wandb._filters.operators.Not | wandb._filters.operators.Lt | wandb._filters.operators.Gt | wandb._filters.operators.Lte | wandb._filters.operators.Gte | wandb._filters.operators.Eq | wandb._filters.operators.Ne | wandb._filters.operators.In | wandb._filters.operators.NotIn | wandb._filters.operators.Exists | wandb._filters.operators.Regex | wandb._filters.operators.Contains | wandb._filters.operators.Size | wandb._filters.operators.All | wandb._filters.expressions.FilterExpr | dict[str, Any], Json, BeforeValidator(func=<function ensure_json>, json_schema_input_type=PydanticUndefined), PlainSerializer(func=<function to_json>, return_type=PydanticUndefined, when_used='always'), AfterValidator(func=<function wrap_mutation_event_filter>)] = And(())
```

## Args

**event\_type** `Literal`

No description provided.

**scope** `Annotated`

The scope of the event: must be an artifact collection.

**filter** `Annotated`

Additional conditions(s), if any, that are required for this event to trigger.

## Examples

Define an event that triggers when a new artifact is created in the
collection "my-collection":

```python theme={"system"}
from wandb import Api
from wandb.automations import OnCreateArtifact

api = Api()
collection = api.artifact_collection(name="my-collection", type_name="model")

event = OnCreateArtifact(scope=collection)
```
