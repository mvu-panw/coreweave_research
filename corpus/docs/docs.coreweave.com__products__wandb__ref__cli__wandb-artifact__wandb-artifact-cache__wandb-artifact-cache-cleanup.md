# wandb artifact cache cleanup

Source: https://docs.coreweave.com/products/wandb/ref/cli/wandb-artifact/wandb-artifact-cache/wandb-artifact-cache-cleanup

# wandb artifact cache cleanup

[View source](https://github.com/wandb/wandb/blob/v0.31.0/wandb/cli/cli.py#L3037)

## Usage

```bash theme={"system"}
cleanup [OPTIONS] TARGET_SIZE
```

## Description

Reduce the local artifact cache size.

Remove the least recently accessed files first until the cache is
at or below the TARGET\_SIZE. TARGET\_SIZE accepts human-readable
formats (for example, 10GB or 500MB).

For example, to reduce the artifact cache to 10 GB:

```bash theme={"system"}
wandb artifact cache cleanup 10GB
```

To remove temporary files and reduce the artifact cache to 5 GB:

```bash theme={"system"}
wandb artifact cache cleanup --remove-temp 5GB
```

## Arguments

| Name | Default | Type |
| - | - | - |
| `target_size` | STR | True |

## Options

| Flag | Type | Description |
| - | - | - |
| `--remove-temp` | BOOL Flag | Also remove temporary files from the cache. **Default**: False |
