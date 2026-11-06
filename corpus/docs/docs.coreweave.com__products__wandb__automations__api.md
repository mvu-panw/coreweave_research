# Manage automations with the API

Source: https://docs.coreweave.com/products/wandb/automations/api

# Manage automations with the API

> Programmatic automation management with the Python API. Create and update may be affected on some client versions. Prefer the W&B App until the SDK fix ships.

Manage W\&B automations programmatically with the `wandb` Python API when you script automation workflows instead of using the W\&B App.

> [!NOTE]
>
> Programmatic **create** and **update** for automations through `wandb.Api().create_automation()` and related helpers can fail on some `wandb` Python client versions because of a client-side feature check (for example, run-state automations). Until a fixed SDK ships, use the [W\&B App](https://docs.coreweave.com/products/wandb/automations/create-automations.md) to create and edit automations. The `list`, `get`, and `delete` methods aren't affected. Internal tracking: WB-34263.

> [!NOTE]
>
> The W\&B Python SDK (`wandb`) doesn't support [ARIA automations](https://docs.coreweave.com/products/wandb/automations/create-automations/aria.md). Creating one isn't possible from the library, and Weights & Biases omits ARIA automations from the results of `list` calls, because released client versions can't parse the ARIA action type. Manage ARIA automations in the W\&B UI. Support is planned for a future release of the library.

## Next steps

Refer to the following resources to manage automations and learn more about how they work:

* [Automations overview](https://docs.coreweave.com/products/wandb/automations.md)
* [Create an automation](https://docs.coreweave.com/products/wandb/automations/create-automations.md) (W\&B App)
* [Automation events and scopes](https://docs.coreweave.com/products/wandb/automations/automation-events.md)
* [Create an ARIA automation](https://docs.coreweave.com/products/wandb/automations/create-automations/aria.md) (W\&B UI)
