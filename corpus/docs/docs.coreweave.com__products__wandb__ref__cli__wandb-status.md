# wandb status

Source: https://docs.coreweave.com/products/wandb/ref/cli/wandb-status

# wandb status

[View source](https://github.com/wandb/wandb/blob/v0.31.0/wandb/cli/cli.py#L3388)

## Usage

```bash theme={"system"}
status [OPTIONS]
```

## Description

Display the current W\&B configuration settings.

Print all active W\&B settings as formatted JSON, including the
base URL, API key, project, entity, and other resolved values.

For example, to show current settings:

```bash theme={"system"}
wandb status
```

## Options

| Flag | Type | Description |
| - | - | - |
| `--settings` | BOOL Flag | Display the current settings. **Default**: True |
