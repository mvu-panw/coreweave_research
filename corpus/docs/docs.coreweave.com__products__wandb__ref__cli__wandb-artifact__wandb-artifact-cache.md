# wandb artifact cache

Source: https://docs.coreweave.com/products/wandb/ref/cli/wandb-artifact/wandb-artifact-cache

# wandb artifact cache

[View source](https://github.com/wandb/wandb/blob/v0.31.0/wandb/cli/cli.py#L3025)

## Usage

```bash theme={"system"}
cache [OPTIONS] COMMAND [ARGS]...
```

## Description

Manage the local artifact cache.

Cache downloaded artifact files locally to avoid redundant downloads.

Use subcommands to inspect and reclaim disk space used by the cache.

## Subcommands

| Command | Description |
| - | - |
| `wandb artifact cache cleanup` | Reduce the local artifact cache size. |
