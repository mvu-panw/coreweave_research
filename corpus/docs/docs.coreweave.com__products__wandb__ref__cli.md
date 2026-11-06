# CLI Reference SDK 0.31.0

Source: https://docs.coreweave.com/products/wandb/ref/cli

# CLI Reference SDK 0.31.0

> Use the W&B Command Line Interface (CLI) to log in, run jobs, execute sweeps, and more using shell commands

## Usage

```bash theme={"system"}
wandb [OPTIONS] COMMAND [ARGS]...
```

## Options

| Option | Description |
| :- | :- |
| `--version` | Show the version and exit. (default: False) |

## Commands

| Command | Description |
| :- | :- |
| [agent](https://docs.coreweave.com/products/wandb/ref/cli/wandb-agent.md) | Start a sweep agent. |
| [artifact](https://docs.coreweave.com/products/wandb/ref/cli/wandb-artifact.md) | Upload, download, and manage W\&B artifacts. |
| [beta](https://docs.coreweave.com/products/wandb/ref/cli/wandb-beta.md) | Beta versions of wandb CLI commands. |
| [controller](https://docs.coreweave.com/products/wandb/ref/cli/wandb-controller.md) | Start a local sweep controller for a W\&B hyperparameter sweep. |
| [disabled](https://docs.coreweave.com/products/wandb/ref/cli/wandb-disabled.md) | Disable W\&B functionality. |
| [docker](https://docs.coreweave.com/products/wandb/ref/cli/wandb-docker.md) | Run code in a Docker container with W\&B configured. |
| [docker-run](https://docs.coreweave.com/products/wandb/ref/cli/wandb-docker-run.md) | Wrap `docker run` and inject W\&B environment variables automatically. |
| [enabled](https://docs.coreweave.com/products/wandb/ref/cli/wandb-enabled.md) | Re-enable W\&B after it was deactivated with `wandb disabled`. |
| [init](https://docs.coreweave.com/products/wandb/ref/cli/wandb-init.md) | Initialize or update W\&B configuration for the current directory. |
| [job](https://docs.coreweave.com/products/wandb/ref/cli/wandb-job.md) | Commands for managing and viewing W\&B jobs. |
| [launch](https://docs.coreweave.com/products/wandb/ref/cli/wandb-launch) | Launch or queue a W\&B Job. |
| [launch-agent](https://docs.coreweave.com/products/wandb/ref/cli/wandb-launch-agent) | Run a W\&B launch agent. |
| [launch-sweep](https://docs.coreweave.com/products/wandb/ref/cli/wandb-launch-sweep) | Run a W\&B launch sweep (Experimental). |
| [leet](https://docs.coreweave.com/products/wandb/ref/cli/wandb-leet.md) | Run W\&B leet commands. |
| [login](https://docs.coreweave.com/products/wandb/ref/cli/wandb-login.md) | Authenticate your machine with W\&B. |
| [offline](https://docs.coreweave.com/products/wandb/ref/cli/wandb-offline.md) | Save data logged to W\&B locally without uploading it to the cloud. |
| [online](https://docs.coreweave.com/products/wandb/ref/cli/wandb-online.md) | Re-enable cloud syncing for W\&B runs. |
| [pull](https://docs.coreweave.com/products/wandb/ref/cli/wandb-pull.md) | Download files from a W\&B run. |
| [purge-cache](https://docs.coreweave.com/products/wandb/ref/cli/wandb-purge-cache.md) | Purges cached logs, run history, and artifacts from the local W\&B cache. |
| [restore](https://docs.coreweave.com/products/wandb/ref/cli/wandb-restore.md) | Restore the code, config, or Docker environment from a previous W\&B run. |
| [scheduler](https://docs.coreweave.com/products/wandb/ref/cli/wandb-scheduler.md) | Run a W\&B launch sweep scheduler (Experimental). |
| [server](https://docs.coreweave.com/products/wandb/ref/cli/wandb-server.md) | Commands for operating a local W\&B server |
| [status](https://docs.coreweave.com/products/wandb/ref/cli/wandb-status.md) | Display the current W\&B configuration settings. |
| [sweep](https://docs.coreweave.com/products/wandb/ref/cli/wandb-sweep.md) | Create, update, or manage a hyperparameter sweep. |
| [sync](https://docs.coreweave.com/products/wandb/ref/cli/wandb-sync.md) | Upload existing local W\&B run data to the cloud. |
| [verify](https://docs.coreweave.com/products/wandb/ref/cli/wandb-verify.md) | Run integration checks against a self-hosted W\&B instance. |
