# SendPromptToAria

Source: https://docs.coreweave.com/products/wandb/ref/python/automations/sendprompttoaria

# SendPromptToAria

[View source](https://github.com/wandb/wandb/blob/main/wandb/automations/actions.py#L243)

## Class wandb.automations.SendPromptToAria

Defines an automation action that sends a prompt to ARIA.

```python theme={"system"}
*,
prompt: Annotated[str, AfterValidator(func=<function _validate_aria_prompt>)],
action_type: Literal[ARIA] = ARIA
```

## Args

**prompt** `Annotated`

The prompt ARIA receives when this automation is triggered.

**action\_type** `Literal`

No description provided.
