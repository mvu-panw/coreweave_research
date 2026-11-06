# wandb sync

Source: https://docs.coreweave.com/products/wandb/ref/cli/wandb-sync

# wandb sync

[View source](https://github.com/wandb/wandb/blob/v0.31.0/wandb/cli/cli.py#L510)

## Usage

```bash theme={"system"}
sync [OPTIONS] [PATHS]...
```

## Description

Upload existing local W\&B run data to the cloud.

Sync offline or incomplete runs to the W\&B server. Provide PATHS to sync
specific runs, or run with no arguments to sync un-uploaded runs in the
wandb folder.

When no PATHS are given, this will ask for confirmation before
syncing. Pass --yes to skip confirmation or --dry-run to exit without
syncing.

PATHS should be run directories, usually in the format

./wandb/run-YYYYMMDD\_HHMMSS-RUN\_ID

YYYYMMDD\_HHMMSS is the timestamp of when the run was created and RUN\_ID is
its unique ID.

For example, to show a summary of local runs and their sync status:

```bash theme={"system"}
wandb sync --dry-run
```

To sync run ID abcd1234 that is saved in ./wandb/run-20170617\_000000-abcd1234:

```bash theme={"system"}
wandb sync ./wandb/run-20170617_000000-abcd1234
```

To sync all unsynced runs in the wandb folder:

```bash theme={"system"}
wandb sync
```

Use `wandb clean` to delete local data for runs that have been synced. See

```bash theme={"system"}
wandb clean --help
```

for more info.

## Arguments

| Name | Default | Type |
| - | - | - |
| `paths` | PATH | False |

## Options

| Flag | Type | Description |
| - | - | - |
| `-v, --verbose` | BOOL Flag | Print more information. **Default**: False |
| `--yes` | BOOL Flag | Don't prompt for confirmation. **Default**: False |
| `--id` | STR | Upload to an existing run ID.  If this is set when syncing multiple files (with the same entity and project), the files will be synced in order of start time. **Default**: None |
| `--project, -p` | STR | Override the project for all synced runs. **Default**: None |
| `--entity, -e` | STR | Override the entity for all synced runs. **Default**: None |
| `--job-type` | STR | Override the job type for all synced runs. **Default**: None |
| `--include-online, --no-skip-online` | BOOL Flag | Include runs created in online mode. **Default**: None |
| `--include-synced, --no-skip-synced` | BOOL Flag | Include runs that are already synced. **Default**: None |
| `--replace-tags` | STR | Rename tags using the format 'old1=new1,old2=new2'. **Default**: None |
| `--dry-run` | BOOL Flag | Print what would happen without uploading anything. **Default**: False |
| `-n` | INT | Max number of runs to sync at a time.  When syncing multiple files that are part of the same run, the files are synced sequentially in order of start time regardless of this setting. This happens for resumed runs or when using the --id parameter. **Default**: 5 |
