# wandb online

Source: https://docs.coreweave.com/products/wandb/ref/cli/wandb-online

# wandb online

[View source](https://github.com/wandb/wandb/blob/v0.31.0/wandb/cli/cli.py#L3317)

## Usage

```bash theme={"system"}
online [OPTIONS]
```

## Description

Re-enable cloud syncing for W\&B runs.

Clear the offline mode setting so subsequent runs in this directory
sync data to the W\&B cloud.

Undoes a previous call to `wandb offline`.

For example, to re-enable cloud syncing after working offline:

```bash theme={"system"}
wandb online
```

To re-enable cloud syncing, then run a training script:

```bash theme={"system"}
wandb online && python train.py
```
