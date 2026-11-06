# NewAutomation

Source: https://docs.coreweave.com/products/wandb/ref/python/automations/newautomation

# NewAutomation

[View source](https://github.com/wandb/wandb/blob/main/wandb/automations/automations.py#L51)

## Class wandb.automations.NewAutomation

A new automation to be created.

```python theme={"system"}
*,
name: str | None = None,
description: str | None = None,
enabled: bool | None = None,
event: Optional[Annotated[wandb.automations.events.OnLinkArtifact | wandb.automations.events.OnAddArtifactAlias | wandb.automations.events.OnAddArtifactTag | wandb.automations.events.OnRemoveArtifactTag | wandb.automations.events.OnAddCollectionTag | wandb.automations.events.OnRemoveCollectionTag | wandb.automations.events.OnCreateArtifact | wandb.automations.events.OnUnlinkArtifact | wandb.automations.events.OnRunMetric | wandb.automations.events.OnRunState, FieldInfo(annotation=NoneType, required=True, discriminator='event_type')]] = None,
action: Optional[Annotated[wandb.automations.actions.SendNotification | wandb.automations.actions.SendWebhook | wandb.automations.actions.DoNothing | wandb.automations.actions.SendPromptToAria, BeforeValidator(func=<function parse_input_action>, json_schema_input_type=PydanticUndefined), FieldInfo(annotation=NoneType, required=True, discriminator='action_type')]] = None
```

## Args

**name** `str | None`

The name of this automation.

**description** `str | None`

An optional description of this automation.

**enabled** `bool | None`

Whether this automation is enabled.  Only enabled automations will trigger.

**event** `Optional`

The event that will trigger this automation.

**action** `Optional`

The action that will execute when this automation is triggered.

## Properties

**scope** `AutomationScope | None`

The scope in which the triggering event must occur.
