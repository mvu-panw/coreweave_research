# wandb init

Source: https://docs.coreweave.com/products/wandb/ref/cli/wandb-init

# wandb init

[View source](https://github.com/wandb/wandb/blob/v0.31.0/wandb/cli/cli.py#L384)

## Usage

```bash theme={"system"}
init [OPTIONS]
```

## Description

Initialize or update W\&B configuration for the current directory.

Set a project and entity, create local W\&B settings, and
prepare the directory for experiment tracking.

For example, set up W\&B for the current directory with guided prompts
for team and project selection:

```bash theme={"system"}
wandb init
```

To set the default project to "foobar" and the default entity to "team-awesome" without prompts:

```bash theme={"system"}
wandb init --project foobar --entity team-awesome
```

To set the W\&B mode to offline:

```bash theme={"system"}
wandb init --mode offline
```

To reset existing W\&B configuration for the current directory:

```bash theme={"system"}
wandb init --reset
```

## Options

| Flag | Type | Description |
| - | - | - |
| `--project, -p` | STR | Set the project to upload runs to. **Default**: None |
| `--entity, -e` | STR | Set the entity to scope the project to. **Default**: None |
| `--reset` | BOOL Flag | Reset existing W\&B configuration for the directory. **Default**: False |
| `--mode, -m` | STR | Set the W\&B mode. One of 'online', 'offline', or 'disabled'. **Default**: None |
