# Annotated[str, BeforeValidator(func=<function default_if_none>, json_schema_input_type=PydanticUndefined)] = '',

Source: https://docs.coreweave.com/products/wandb/ref/python/automations/sendnotification

# SendNotification

[View source](https://github.com/wandb/wandb/blob/main/wandb/automations/actions.py#L151)

## Class wandb.automations.SendNotification

Defines an automation action that sends a (Slack) notification.

```python theme={"system"}
*,
integration_id: Annotated[str, Strict(strict=True)],
text: Annotated[str, BeforeValidator(func=<function default_if_none>, json_schema_input_type=PydanticUndefined)] = '',
level: Annotated[wandb.automations._generated.enums.AlertSeverity, BeforeValidator(func=<function default_if_none>, json_schema_input_type=PydanticUndefined), BeforeValidator(func=<function upper_if_str>, json_schema_input_type=PydanticUndefined)] = <AlertSeverity.INFO: 'INFO'>,
title: Annotated[str, BeforeValidator(func=<function default_if_none>, json_schema_input_type=PydanticUndefined)] = '',
action_type: Literal[NOTIFICATION] = NOTIFICATION
```

## Args

**integration\_id** `Annotated`

The ID of the Slack integration that will be used to send the notification.

**text** `Annotated`

The message body of the sent notification.

**level** `Annotated`

The severity (`INFO`, `WARN`, `ERROR`) of the sent notification.

**title** `Annotated`

The title of the sent notification.

**action\_type** `Literal`

No description provided.

## Methods

### method SendNotification.from\_integration()

```python theme={"system"}
integration: 'SlackIntegration', *,
title: 'str' = '',
text: 'str' = '',
level: 'AlertSeverity' = <AlertSeverity.INFO: 'INFO'>
```

Define a notification action that sends to the given (Slack) integration.

##### Arguments

**integration** `SlackIntegration`

No description provided.

**title** `str`

No description provided.

**text** `str`

No description provided.

**level** `AlertSeverity`

No description provided.
