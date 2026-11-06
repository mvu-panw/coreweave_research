# wandb clean

Source: https://docs.coreweave.com/products/wandb/ref/cli/wandb-clean

# wandb clean

[View source](https://github.com/wandb/wandb/blob/v0.31.0/wandb/cli/clean.py#L20)

## Usage

```bash theme={"system"}
clean [OPTIONS]
```

## Description

Remove synced run data.

Cleans up the wandb folder, as determined by settings. Usually, this is
the "wandb" or ".wandb" folder in the current working directory, or
in the directory specified by the WANDB\_DIR environment variable if that
is set.

By default, this removes all runs created more than 24 hours ago (based
on the timestamp in the run folder name) that are online runs or that
were synced with `wandb sync`.

## Options

| Flag | Type | Description |
| - | - | - |
| `--min-hours` | INT | Minimum run age in hours for deletion (default 24). **Default**: 24 |
| `--include-unsynced` | BOOL Flag | Delete unsynced run directories as well. **Default**: False |
| `--force` | BOOL Flag | Skip the confirmation prompt. **Default**: False |
