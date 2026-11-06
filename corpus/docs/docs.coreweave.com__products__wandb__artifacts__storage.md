# Manage artifact storage and memory allocation

Source: https://docs.coreweave.com/products/wandb/artifacts/storage

> Manage storage, memory allocation of W&B Artifacts.

# Manage artifact storage and memory allocation

Weights & Biases stores artifact files in a private Google Cloud Storage bucket located in the United States by default. All files are encrypted at rest and in transit.

For sensitive files, we recommend you set up [Private Hosting](https://docs.coreweave.com/products/wandb/platform/hosting.md) or use [reference artifacts](https://docs.coreweave.com/products/wandb/artifacts/track-external-files.md).

During training, Weights & Biases locally saves logs, artifacts, and configuration files in the following local directories:

| File | Default location | To change default location set: |
| - | - | - |
| logs | `./wandb` | `dir` in `wandb.init()` or set the `WANDB_DIR` environment variable |
| artifacts | `~/.cache/wandb` | the `WANDB_CACHE_DIR` environment variable |
| configs | `~/.config/wandb` | the `WANDB_CONFIG_DIR` environment variable |
| staging artifacts for upload | `~/.cache/wandb-data/` | the `WANDB_DATA_DIR` environment variable |
| downloaded artifacts | `./artifacts` | the `WANDB_ARTIFACT_DIR` environment variable |

For a complete guide to using environment variables to configure Weights & Biases, see the [environment variables reference](https://docs.coreweave.com/products/wandb/track/environment-variables.md).

> [!WARNING]
>
> Depending on the machine on `wandb` is initialized on, these default folders may not be located in a writeable part of the file system. This might trigger an error.

### Clean up local artifact cache

Weights & Biases caches artifact files to speed up downloads across versions that share files in common. Over time this cache directory can become large. Run the [`wandb artifact cache cleanup`](https://docs.coreweave.com/products/wandb/ref/cli/wandb-artifact/wandb-artifact-cache) command to prune the cache and to remove any files that have not been used recently.

The following code snippet demonstrates how to limit the size of the cache to 1GB. Copy and paste the code snippet into your terminal:

```bash theme={"system"}
$ wandb artifact cache cleanup 1GB
```
