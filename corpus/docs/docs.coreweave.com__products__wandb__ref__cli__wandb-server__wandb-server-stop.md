# wandb server stop

Source: https://docs.coreweave.com/products/wandb/ref/cli/wandb-server/wandb-server-stop

# wandb server stop

[View source](https://github.com/wandb/wandb/blob/v0.31.0/wandb/cli/cli.py#L2763)

## Usage

```bash theme={"system"}
stop [OPTIONS]
```

## Description

Stop a running local W\&B server.

Stops the Docker container named `wandb-local` that was started
by `wandb server start`. Requires Docker to be installed.

For example, to stop the local W\&B server:

```bash theme={"system"}
wandb server stop
```
