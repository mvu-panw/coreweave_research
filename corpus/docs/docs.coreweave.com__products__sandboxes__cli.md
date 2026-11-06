# Manage sandboxes with the CLI

Source: https://docs.coreweave.com/products/sandboxes/cli

# Manage sandboxes with the CLI

> Install the Sandboxes CLI to inspect sandboxes, run commands, transfer files, and manage snapshots.

The `cwsandbox` command-line interface (CLI) manages existing CoreWeave sandboxes from your terminal. Use it to inspect sandboxes, run commands, retrieve logs, transfer files, manage file system snapshots, and clean up resources. Install the CLI as an optional extra of the [Sandboxes Python client](https://docs.coreweave.com/products/sandboxes/client.md).

Create sandboxes with the SDK before using the CLI. Follow the [serverless quickstart](https://docs.coreweave.com/products/sandboxes/get-started.md) or [Use your own compute](https://docs.coreweave.com/products/sandboxes/get-started-cks.md) to create one.

## Prerequisites

Before you begin, prepare the following:

* An [active Python 3.11 or later virtual environment](https://docs.coreweave.com/products/sandboxes/client.md#prepare-your-python-environment) with `uv` installed.
* A credential for the account that owns your sandboxes. See [Choose and get credentials](https://docs.coreweave.com/products/sandboxes/placement.md#choose-and-get-credentials) for credential setup and required roles.
* A running sandbox for command execution, interactive shells, log retrieval, file operations, and snapshot creation.

## Install and authenticate

Choose the credential you used to create your sandboxes. Run the commands from one tab in your active virtual environment, replacing the credential placeholder with your key or token:

> [tab] Forge API key
>
> Install the `cli` and `wandb` extras, then select the W\&B authentication strategy for your Forge API key:
>
> ```bash theme={"system"}
> uv pip install --upgrade 'cwsandbox[cli,wandb]'
> export WANDB_API_KEY="WANDB_API_KEY_VALUE"
> export CWSANDBOX_AUTH="wandb"
> cwsandbox --help
> ```

> [tab] CoreWeave API access token
>
> Install the `cli` extra and select CoreWeave authentication:
>
> ```bash theme={"system"}
> uv pip install --upgrade 'cwsandbox[cli]'
> export CWSANDBOX_API_KEY="API_ACCESS_TOKEN"
> export CWSANDBOX_AUTH="coreweave_api_key"
> cwsandbox --help
> ```

The help output lists the available commands. Keep the authentication variables set in the terminal where you run the remaining examples.

`CWSANDBOX_AUTH` selects the credential strategy. The top-level `--auth` option overrides it for one invocation. For example, with Forge dependencies and credentials configured:

```bash theme={"system"}
cwsandbox --auth wandb ls
```

To see the options for any command or subcommand, use `--help`:

```bash theme={"system"}
cwsandbox exec --help
cwsandbox files read --help
cwsandbox snapshots create --help
```

## Find your sandboxes

List sandboxes visible to your credential:

```bash theme={"system"}
cwsandbox ls
```

Filter by status, or combine a status and a tag. Replace `TAG` with a tag attached to your sandboxes:

```bash theme={"system"}
cwsandbox ls --status running
cwsandbox ls --status running --tag "TAG" --output json
```

The default table shows sandbox IDs, statuses, runners, and start times. `--output json` returns structured output. Repeat `--tag` or `--runner-id` to supply multiple filter values.

## Inspect a sandbox

Replace `SANDBOX_ID_VALUE` with an ID from `cwsandbox ls`, and set it in your terminal:

```bash theme={"system"}
export SANDBOX_ID="SANDBOX_ID_VALUE"
cwsandbox get "$SANDBOX_ID"
cwsandbox get "$SANDBOX_ID" --output json
```

The following examples use this variable. The details include the sandbox status, runner information, start time, and return code when available.

## Run commands

Execute a command in a running sandbox. The command must be available in the sandbox image:

```bash theme={"system"}
cwsandbox exec "$SANDBOX_ID" echo hello
cwsandbox exec "$SANDBOX_ID" python -c "print('hello')"
```

To set the remote working directory, pass `--cwd` before the remote command. Replace `REMOTE_DIRECTORY` with an existing directory in the sandbox:

```bash theme={"system"}
cwsandbox exec "$SANDBOX_ID" --cwd "REMOTE_DIRECTORY" pwd
```

The CLI streams standard output and standard error to your local terminal. When the remote command completes normally, the CLI exits with its exit code.

## Open an interactive shell

From a local terminal on macOS or Linux, open an interactive shell:

```bash theme={"system"}
cwsandbox sh "$SANDBOX_ID"
```

The default shell is `/bin/bash`. Use `--cmd` to choose a different shell or an interactive program installed in the sandbox:

```bash theme={"system"}
cwsandbox sh "$SANDBOX_ID" --cmd /bin/sh
cwsandbox sh "$SANDBOX_ID" --cmd "python -i"
```

The interactive shell requires a terminal for both standard input and standard output and isn't supported on Windows. To leave a shell session, type `exit` or press `Ctrl+D`. `Ctrl+C` is forwarded to the remote process.

## View logs

Retrieve logs from the sandbox's main process:

```bash theme={"system"}
cwsandbox logs "$SANDBOX_ID" --tail 100
cwsandbox logs "$SANDBOX_ID" --tail 100 --timestamps
```

Use `--follow` to stream new log output. Press `Ctrl+C` to stop following:

```bash theme={"system"}
cwsandbox logs "$SANDBOX_ID" --follow
```

Use `--since` to filter logs by a timestamp. Replace `2026-09-10 09:00:00` with the start time you want. The CLI interprets a timestamp without a timezone as UTC:

```bash theme={"system"}
cwsandbox logs "$SANDBOX_ID" --since "2026-09-10 09:00:00"
```

Logs contain standard output and standard error from the main process, which is the command used to create the sandbox. They don't include output from `cwsandbox exec`. Sandboxes created with the default keep-alive command produce no log output.

Log retrieval requires a running sandbox. Retrieve logs before stopping the sandbox. For more information, see [Sandbox logging](https://docs.coreweave.com/products/sandboxes/client/guides/logging.md).

## Read and write files

File operations require a running sandbox. To print a remote file to standard output, replace `REMOTE_PATH` with its path inside the sandbox:

```bash theme={"system"}
cwsandbox files read "$SANDBOX_ID" "REMOTE_PATH"
```

To download the file, add `--output` with a local destination. Replace `LOCAL_PATH` with the path where you want to save it:

```bash theme={"system"}
cwsandbox files read "$SANDBOX_ID" "REMOTE_PATH" --output "LOCAL_PATH"
```

To upload a file, supply the remote destination first and the existing local source file second:

```bash theme={"system"}
cwsandbox files write "$SANDBOX_ID" "REMOTE_PATH" "LOCAL_PATH"
```

## Manage file system snapshots

Snapshot creation requires a running sandbox configured with a [file system snapshot mount](https://docs.coreweave.com/products/sandboxes/file-system-snapshots.md#start-a-sandbox-with-a-snapshot-mount). Your organization must be enabled for file system snapshots.

Create a snapshot:

```bash theme={"system"}
cwsandbox snapshots create "$SANDBOX_ID"
```

The command waits for the snapshot to become ready and prints its ID. To return without waiting for readiness and print the ID as JSON, use:

```bash theme={"system"}
cwsandbox snapshots create "$SANDBOX_ID" --no-wait --output json
```

List snapshots, or filter to ready snapshots created from a specific sandbox:

```bash theme={"system"}
cwsandbox snapshots list
cwsandbox snapshots list --source-sandbox-id "$SANDBOX_ID" --status ready
```

To inspect a snapshot, replace `SNAPSHOT_ID_VALUE` with its ID:

```bash theme={"system"}
export SNAPSHOT_ID="SNAPSHOT_ID_VALUE"
cwsandbox snapshots get "$SNAPSHOT_ID"
cwsandbox snapshots get "$SNAPSHOT_ID" --output json
```

To delete a snapshot you no longer need, run:

```bash theme={"system"}
cwsandbox snapshots delete "$SNAPSHOT_ID"
```

For snapshot requirements, supported storage, and restoring a sandbox with the SDK, see [File system snapshots](https://docs.coreweave.com/products/sandboxes/file-system-snapshots.md).

## Stop or delete a sandbox

Stop a sandbox when you finish using it:

```bash theme={"system"}
cwsandbox stop "$SANDBOX_ID"
```

To allow up to 30 seconds for graceful shutdown, use this alternative:

```bash theme={"system"}
cwsandbox stop "$SANDBOX_ID" --graceful-shutdown-seconds 30
```

For a sandbox configured with a file system snapshot mount, capture a snapshot before stopping with this alternative:

```bash theme={"system"}
cwsandbox stop "$SANDBOX_ID" --snapshot-on-stop
```

To delete a sandbox, run:

```bash theme={"system"}
cwsandbox delete "$SANDBOX_ID"
```

For cleanup scripts, use `--missing-ok` so an already missing sandbox doesn't cause an error:

```bash theme={"system"}
cwsandbox delete "$SANDBOX_ID" --missing-ok
```
