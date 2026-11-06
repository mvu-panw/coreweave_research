# wandb restore

Source: https://docs.coreweave.com/products/wandb/ref/cli/wandb-restore

# wandb restore

[View source](https://github.com/wandb/wandb/blob/v0.31.0/wandb/cli/cli.py#L3121)

## Usage

```bash theme={"system"}
restore [OPTIONS] RUN
```

## Description

Restore the code, config, or Docker environment from a previous W\&B run.

Recreate the environment of a previous run so you can reproduce it.
Requires authentication with W\&B.

Restore up to three pieces of state, depending on what the original
run recorded:

1. Config (always): Write the run config to wandb/config.yaml.

2. Git (if available): Check out the original commit on a new
   wandb/run\_id branch. Fetch and apply any saved diff patch.
   If the original commit cannot be found,
   fall back to an upstream commit if the original cannot be found.
   Run this command from the same git repository as the original run. Skip
   this step with `--no-git`.

3. Docker (if available): If the run was executed inside a Docker
   container, start the same image with the original command.

If the run has no git history and no Docker image,
restore only the config.

Accept the run identifier in any of the following formats:
run\_id, project:run\_id, entity/project:run\_id, or entity/project/run\_id .

For example, to restore a run with run ID  in the default project
(stored as the WANDB\_PROJECT environment variable) and entity
(set from WANDB\_ENTITY or the authenticated user's default entity):

```bash theme={"system"}
wandb restore abcd1234
```

To restore a run from the "foobar" project and "team-awesome" entity with
run ID abcd1234:

```bash theme={"system"}
wandb restore team-awesome/foobar/abcd1234
```

To restore run abcd1234 without restoring git state. Only restore config
and Docker state:

```bash theme={"system"}
wandb restore --no-git abcd1234
```

To restore run abcd1234 in detached HEAD mode instead of creating a branch:

```bash theme={"system"}
wandb restore --no-branch abcd1234
```

To restore run abcd1234 from another team's project:

```bash theme={"system"}
wandb restore other-team/their-project:abcd1234
```

## Arguments

| Name | Default | Type |
| - | - | - |
| `run` | STR | True |

## Options

| Flag | Type | Description |
| - | - | - |
| `--no-git` | BOOL Flag | Skip git restoration. Only restore config and Docker state. **Default**: False |
| `--branch` | BOOL Flag | Create a wandb/run\_id branch or check out the commit in detached HEAD mode. **Default**: True |
| `--project, -p` | STR | Specify the project to look up the run in. **Default**: None |
| `--entity, -e` | STR | Specify the entity to scope the run lookup to. **Default**: None |
