# controller()

Source: https://docs.coreweave.com/products/wandb/ref/python/functions/controller

# controller()

[View source](https://github.com/wandb/wandb/blob/main/wandb/sdk/wandb_sweep.py#L96)

## function wandb.controller()

Public sweep controller constructor.

```python theme={"system"}
sweep_id_or_config: 'str | dict | None' = None,
entity: 'str | None' = None,
project: 'str | None' = None
```

## Args

**sweep\_id\_or\_config** `str | dict | None`

No description provided.

**entity** `str | None`

No description provided.

**project** `str | None`

No description provided.

## Examples

```python theme={"system"}
import wandb

tuner = wandb.controller(...)
print(tuner.sweep_config)
print(tuner.sweep_id)
tuner.configure_search(...)
tuner.configure_stopping(...)
```
