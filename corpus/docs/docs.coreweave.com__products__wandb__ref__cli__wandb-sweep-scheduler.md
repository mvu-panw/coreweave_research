# wandb sweep-scheduler

Source: https://docs.coreweave.com/products/wandb/ref/cli/wandb-sweep-scheduler

# wandb sweep-scheduler

[View source](https://github.com/wandb/wandb/blob/v0.31.0/wandb/cli/cli.py#L1997)

## Usage

```bash theme={"system"}
sweep-scheduler [OPTIONS] SWEEP_ID
```

## Description

Run a local scheduler that suggests a sweep's runs (Experimental).

## Arguments

| Name | Default | Type |
| - | - | - |
| `sweep_id` | STR | True |

## Options

| Flag | Type | Description |
| - | - | - |
| `--entity, -e` | STR | Entity that owns the sweep. **Default**: None |
| `--project, -p` | STR | Project that owns the sweep. **Default**: None |
| `--batch-size` | INT | Number of runs to keep in flight at once. **Default**: 10 |
| `--poll-interval` | FLOAT | Seconds to wait between polls of the sweep's runs. **Default**: 10.0 |
