# wandb disabled

Source: https://docs.coreweave.com/products/wandb/ref/cli/wandb-disabled

# wandb disabled

[View source](https://github.com/wandb/wandb/blob/v0.31.0/wandb/cli/cli.py#L3424)

## Usage

```bash theme={"system"}
disabled [OPTIONS]
```

## Description

Disable W\&B functionality.

While W\&B is in `disabled` mode, it does not log or sync data.

Use `wandb enable` to restore W\&B functionality.

Use `wandb offline` to stop cloud syncing while continuning to log data
locally.

For example, to turn off W\&B so that the train.py script executes without logging or
syncing data to W\&B:

```bash theme={"system"}
wandb disabled
```

Next, train the model without logging or syncing to W\&B:

```bash theme={"system"}
python train.py  # Does not log or sync data to W&B
```

Restore W\&B functionality when ready to log and sync again:

```bash theme={"system"}
wandb enabled
```

## Options

| Flag | Type | Description |
| - | - | - |
| `--service` | BOOL Flag | No effect. Accepted for backwards compatibility. **Default**: True |
