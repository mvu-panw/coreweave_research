# SendWebhook

Source: https://docs.coreweave.com/products/wandb/ref/python/automations/sendwebhook

# SendWebhook

[View source](https://github.com/wandb/wandb/blob/main/wandb/automations/actions.py#L193)

## Class wandb.automations.SendWebhook

Defines an automation action that sends a webhook request.

```python theme={"system"}
*,
integration_id: Annotated[str, Strict(strict=True)],
requestPayload: Optional[Annotated[dict[str, Any], Json, BeforeValidator(func=<function ensure_json>, json_schema_input_type=PydanticUndefined), PlainSerializer(func=<function to_json>, return_type=PydanticUndefined, when_used='always')]] = None,
action_type: Literal[GENERIC_WEBHOOK] = GENERIC_WEBHOOK
```

## Args

**integration\_id** `Annotated`

The ID of the webhook integration that will be used to send the request.

**requestPayload** `Optional`

The payload, possibly with template variables, to send in the webhook request.

**action\_type** `Literal`

No description provided.

## Methods

### method SendWebhook.from\_integration()

```python theme={"system"}
integration: 'WebhookIntegration', *,
payload: 'JsonEncoded[dict[str, Any]] | None' = None
```

Define a webhook action that sends to the given (webhook) integration.

##### Arguments

**integration** `WebhookIntegration`

No description provided.

**payload** `JsonEncoded[dict[str, Any]] | None`

No description provided.
