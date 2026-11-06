# wandb leet run

Source: https://docs.coreweave.com/products/wandb/ref/cli/wandb-leet/wandb-leet-run

# wandb leet run

[View source](https://github.com/wandb/wandb/blob/v0.31.0/wandb/cli/leet.py#L74)

## Usage

```bash theme={"system"}
run [OPTIONS] [PATH]
```

## Description

Launch the LEET TUI.

LEET is a terminal UI for viewing a W\&B run specified by an optional PATH.

PATH can include a .wandb file, a run directory containing a .wandb file,
or a W\&B run URL.
If PATH is not provided, the command will look for the latest run.

## Arguments

| Name | Default | Type |
| - | - | - |
| `path` | STR | False |

## Options

| Flag | Type | Description |
| - | - | - |
| `-h, --help` | BOOL Flag | Show this message and exit. **Default**: False |
