# wandb purge-cache

Source: https://docs.coreweave.com/products/wandb/ref/cli/wandb-purge-cache

# wandb purge-cache

[View source](https://github.com/wandb/wandb/blob/v0.31.0/wandb/cli/cli.py#L3570)

## Usage

```bash theme={"system"}
purge-cache [OPTIONS]
```

## Description

Purges cached logs, run history, and artifacts from the
local W\&B cache.

## Options

| Flag | Type | Description |
| - | - | - |
| `--age` | STR | Removes items older than the specified time period (e.g., '10s', '5m', '8h', '7d', '6M', '1y'). **Default**: 0d |
| `--force` | BOOL Flag | Do not prompt for confirmation when deleting files. **Default**: False |
