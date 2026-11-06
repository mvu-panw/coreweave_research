# wandb artifact get

Source: https://docs.coreweave.com/products/wandb/ref/cli/wandb-artifact/wandb-artifact-get

# wandb artifact get

[View source](https://github.com/wandb/wandb/blob/v0.31.0/wandb/cli/cli.py#L2915)

## Usage

```bash theme={"system"}
get [OPTIONS] PATH
```

## Description

Download an artifact from W\&B by its path.

The PATH format is entity/project/artifact\_name:version. If
the version is omitted, use the "latest" alias.

For example, to download the latest version of an artifact called "processed-training-set"
from the "foobar" project under the "team-awesome" entity:

```bash theme={"system"}
wandb artifact get team-awesome/foobar/processed-training-set:latest
```

To download a specific version (v2) of the "processed-training-set" artifact
to a local directory (./data):

```bash theme={"system"}
wandb artifact get --root ./data team-awesome/foobar/processed-training-set:v2
```

## Arguments

| Name | Default | Type |
| - | - | - |
| `path` | STR | True |

## Options

| Flag | Type | Description |
| - | - | - |
| `--root` | STR | Directory to download the artifact to. Uses the default artifact cache if not set. **Default**: None |
| `--type` | STR | Expected artifact type. Fails if the artifact does not match. **Default**: None |
