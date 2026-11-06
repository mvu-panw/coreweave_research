# wandb beta core

Source: https://docs.coreweave.com/products/wandb/ref/cli/wandb-beta/wandb-beta-core

# wandb beta core

[View source](https://github.com/wandb/wandb/blob/v0.31.0/wandb/cli/beta.py#L196)

## Usage

```bash theme={"system"}
core [OPTIONS] COMMAND [ARGS]...
```

## Description

Manage a shared local wandb-core service for multi-process workloads.

wandb-core is the local backend process that handles run data,
file uploads, and system metrics collection. By default, each
process that calls `wandb.init()` starts its own backend. On a
machine running many independent workers, that duplicates work
and wastes CPU and memory.

Use these commands to start one detached wandb-core instance and
point multiple workers on the same machine at it with the
WANDB\_SERVICE environment variable.

Typical workflow:

```bash theme={"system"}
wandb beta core start
```

```bash theme={"system"}
export WANDB_SERVICE=printed_value
```

```bash theme={"system"}
python -m your_launcher
```

```bash theme={"system"}
wandb beta core stop
```

For shell scripts, capture the raw WANDB\_SERVICE value from stdout:

```bash theme={"system"}
export WANDB_SERVICE="$(wandb beta core start)"
```

The shared service exits after 10 minutes of idleness by default.
Override this with --idle-timeout on the start command.

## Subcommands

| Command | Description |
| - | - |
| `wandb beta core start` | Start a detached wandb-core service. |
| `wandb beta core stop` | Stop a detached wandb-core service. |
