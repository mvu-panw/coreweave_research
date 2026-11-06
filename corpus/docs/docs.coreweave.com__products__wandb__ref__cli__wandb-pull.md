# wandb pull

Source: https://docs.coreweave.com/products/wandb/ref/cli/wandb-pull

# wandb pull

[View source](https://github.com/wandb/wandb/blob/v0.31.0/wandb/cli/cli.py#L3068)

## Usage

```bash theme={"system"}
pull [OPTIONS] RUN
```

## Description

Download files from a W\&B run.

Fetch all files associated with the specified run. Skip files that already
exist locally with the same content. Create subdirectories as needed to
mirror the structure of the files in W\&B.

Use the run ID to reference the run, and optionally specify the project
and entity if not included in the run argument.

For example, to download files from a run with run ID "abcd1234" in the "foobar" project
and "team-awesome" entity:

```bash theme={"system"}
wandb pull -p foobar -e team-awesome abcd1234
```

## Arguments

| Name | Default | Type |
| - | - | - |
| `run` | STR | True |

## Options

| Flag | Type | Description |
| - | - | - |
| `--project, -p` | STR | The project containing the run to pull files from. **Default**: None |
| `--entity, -e` | STR | The entity that owns the project. Defaults to the value of the WANDB\_ENTITY environment variable or the default entity if not set. **Default**: models |
