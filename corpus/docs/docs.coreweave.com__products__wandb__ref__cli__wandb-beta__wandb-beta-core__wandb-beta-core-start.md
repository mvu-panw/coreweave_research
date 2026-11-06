# wandb beta core start

Source: https://docs.coreweave.com/products/wandb/ref/cli/wandb-beta/wandb-beta-core/wandb-beta-core-start

# wandb beta core start

[View source](https://github.com/wandb/wandb/blob/v0.31.0/wandb/cli/beta.py#L234)

## Usage

```bash theme={"system"}
start [OPTIONS]
```

## Description

Start a detached wandb-core service.

## Options

| Flag | Type | Description |
| - | - | - |
| `--idle-timeout` | STR | Shut down wandb-core after this much idle time with no connected clients. Uses Go duration syntax, for example 30s, 10m, or 0 to disable idle shutdown. **Default**: 10m |
