# wandb artifact ls

Source: https://docs.coreweave.com/products/wandb/ref/cli/wandb-artifact/wandb-artifact-ls

# wandb artifact ls

[View source](https://github.com/wandb/wandb/blob/v0.31.0/wandb/cli/cli.py#L2977)

## Usage

```bash theme={"system"}
ls [OPTIONS] PATH
```

## Description

List all artifacts in a W\&B project.

Display the latest version of each artifact collection in a
project. Show the type, last updated time, size, and name.

The PATH consists of the entity and project (entity/project) to
list artifacts from.

For example, to list all artifacts in a project called "foobar" under
the "team-awesome" entity:

```bash theme={"system"}
wandb artifact ls team-awesome/foobar
```

To list only artifacts of type "model" in the same project:

```bash theme={"system"}
wandb artifact ls --type model team-awesome/foobar
```

## Arguments

| Name | Default | Type |
| - | - | - |
| `path` | STR | True |

## Options

| Flag | Type | Description |
| - | - | - |
| `--type, -t` | STR | Filter artifacts by type. **Default**: None |
