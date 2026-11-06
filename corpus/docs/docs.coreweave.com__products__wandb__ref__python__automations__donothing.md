# DoNothing

Source: https://docs.coreweave.com/products/wandb/ref/python/automations/donothing

# DoNothing

[View source](https://github.com/wandb/wandb/blob/main/wandb/automations/actions.py#L218)

## Class wandb.automations.DoNothing

Defines an automation action that intentionally does nothing.

```python theme={"system"}
*,
no_op: Annotated[bool, BeforeValidator(func=<function default_if_none>, json_schema_input_type=PydanticUndefined)] = True,
action_type: Literal[NO_OP] = NO_OP
```

## Args

**no\_op** `Annotated`

Placeholder field which exists only to satisfy backend schema requirements.

There should never be a need to set this field explicitly, as its value is ignored.

**action\_type** `Literal`

No description provided.
