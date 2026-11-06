# wandb offline

Source: https://docs.coreweave.com/products/wandb/ref/cli/wandb-offline

# wandb offline

[View source](https://github.com/wandb/wandb/blob/v0.31.0/wandb/cli/cli.py#L3344)

## Usage

```bash theme={"system"}
offline [OPTIONS]
```

## Description

Save data logged to W\&B locally without uploading it to the cloud.

Use `wandb online` or `wandb sync` to upload offline runs.

For example, to run a script in offline mode to log data locally without syncing
to the cloud:

```bash theme={"system"}
wandb offline && python train.py
```

To run a script in offline mode:

```bash theme={"system"}
wandb offline && python train.py
```

At a later time, sync all offline runs to the cloud:

```bash theme={"system"}
wandb sync --sync-all
```
