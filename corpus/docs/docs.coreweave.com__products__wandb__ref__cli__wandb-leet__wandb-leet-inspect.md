# wandb leet inspect

Source: https://docs.coreweave.com/products/wandb/ref/cli/wandb-leet/wandb-leet-inspect

# wandb leet inspect

[View source](https://github.com/wandb/wandb/blob/v0.31.0/wandb/cli/leet.py#L114)

## Usage

```bash theme={"system"}
inspect [OPTIONS] [PATH]
```

## Description

Inspect a run's .wandb transaction log.

Opens a browsable list of the records stored in the log next to a
text view of the selected record. When stdout is not a terminal, or
with --json or --follow, prints the records instead.



## Examples

wandb leet inspect --summary            State, latest metrics, console tail
wandb leet inspect --summary --json     The same as one JSON object
wandb leet inspect --json | grep '"type":"history"' | tail -n 5
wandb leet inspect --follow --json      Stream records as they are written
wandb leet inspect run.wandb | less     Browse the records as text

PATH can be a .wandb file, a run directory containing one, or a
wandb directory. If PATH is not provided, the latest run is used.

## Arguments

| Name | Default | Type |
| - | - | - |
| `path` | STR | False |

## Options

| Flag | Type | Description |
| - | - | - |
| `--summary` | BOOL Flag | Print the run's state, latest metric values, config and console tail instead of its records. **Default**: False |
| `--json` | BOOL Flag | Print JSON: one line per record, or one object with --summary. **Default**: False |
| `--follow, -f` | BOOL Flag | Keep printing records as the run writes them until it exits. **Default**: False |
| `--idle-timeout` | STR | With --follow, stop once the run's file has gone this long without a write (e.g. 30s, 1h; 0 waits forever). Defaults to 10m. **Default**: |
| `-h, --help` | BOOL Flag | Show this message and exit. **Default**: False |
