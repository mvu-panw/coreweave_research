# Run Devin Outposts on Sandboxes

Source: https://docs.coreweave.com/products/sandboxes/agents/devin-outposts

# Run Devin Outposts on Sandboxes

> Let Devin plan in Devin Cloud while its commands run in a CoreWeave sandbox you control.

[Devin Outposts](https://docs.devin.ai/cloud/outposts/overview) keep Devin's planning and model inference in Devin Cloud. Devin runs commands, edits files, and accesses repositories on a machine you operate. This guide makes that machine a CoreWeave sandbox: an isolated environment with the image, CPU, memory, GPU, and lifetime you choose.

An outpost is a named queue in Devin Cloud. A worker is the `devin worker` process that connects to Devin Cloud over outbound HTTPS, claims sessions from the queue, and runs them locally. It doesn't require inbound ports, a public IP address, or a virtual private network (VPN). Here, one sandbox runs one worker, and that worker serves sessions one after another for as long as the sandbox lives.

Each worker serves one active session at a time. Additional sessions wait until a worker becomes available. This guide starts a fixed number of workers. It doesn't create more sandboxes when sessions queue. Start more workers manually or use an orchestrator to provision them automatically.

## Prerequisites

Before you begin, make sure you have the following:

* A Devin organization with Outposts enabled. If you don't see **Outposts** under **Settings > Environment** in Devin Cloud, ask your Devin administrator.
* A [Forge API key or CoreWeave API access token](https://docs.coreweave.com/products/sandboxes/placement.md#choose-and-get-credentials).
* For the direct software development kit (SDK) path, either Python 3.11 or later with [`uv`](https://docs.astral.sh/uv/), or Node.js 22 or later.

## Choose sandbox credentials

These examples use serverless capacity. The Sandboxes SDK examples require a Forge API key to resolve secret references. For `cws-agent`, choose either credential. See [Choose and get credentials](https://docs.coreweave.com/products/sandboxes/placement.md#choose-and-get-credentials) to obtain either credential. Agent and model-provider credentials are configured separately.

For the SDK path, create your local project before you save the configuration file. Save the file for your language beside the scripts you run from this guide. Use the same file for creation, reconnection, and cleanup. It stores your authentication choice, not the key itself.

> [tab] Forge API key
>
> Replace `[WANDB-API-KEY]` with your Forge API key and `[WANDB-ENTITY]` with the Forge team that holds your worker secret:
>
> ```bash theme={"system"}
> export WANDB_API_KEY="[WANDB-API-KEY]"
> export WANDB_ENTITY="[WANDB-ENTITY]"
> unset CWSANDBOX_API_KEY
> ```
>
> `cws-agent` selects Forge authentication when `CWSANDBOX_API_KEY` is unset. The SDK configuration in this tab selects it explicitly.
>
> > [tab] Python
> >
> > ```python title="sandbox_auth.py" theme={"system"}
> > import os
> >
> > from cwsandbox import AuthHeaders
> >
> > AUTH = AuthHeaders(
> >     headers={
> >         "x-wandb-api-key": os.environ["WANDB_API_KEY"],
> >         "x-entity-id": os.environ["WANDB_ENTITY"],
> >     },
> >     strategy="wandb_api_key",
> > )
> > ```
>
> > [tab] TypeScript
> >
> > ```typescript title="sandbox-client.mts" theme={"system"}
> > import { createSandboxClient } from "@coreweave/cwsandbox/wandb";
> >
> > export const client = createSandboxClient({
> >   apiKey: process.env.WANDB_API_KEY,
> >   entity: process.env.WANDB_ENTITY,
> > });
> > ```

> [tab] CoreWeave API access token
>
> Replace `[API-ACCESS-TOKEN]` with your CoreWeave API access token and export it in your local terminal:
>
> ```bash theme={"system"}
> export CWSANDBOX_API_KEY="[API-ACCESS-TOKEN]"
> ```
>
> Use this credential for the `cws-agent` path. The SDK worker examples require Forge secret injection.

## Create an outpost in Devin Cloud

To create an outpost and get its token, follow these steps:

1. In [Devin Cloud](https://app.devin.ai), go to **Settings > Environment > Outposts**.
2. Click **Create Outpost**, enter a name, and select **Linux**.
3. Copy the outpost token. Devin Cloud shows it once.

With the outpost ready, choose either `cws-agent` or the Sandboxes SDK to start its worker, then run the verification session.

## Quick start with cws-agent

Follow the [`cws-agent` installation instructions](https://github.com/coreweave/cws-agent#install). The tool configures a snapshot mount to save and restore your workspace with [file system snapshots](https://docs.coreweave.com/products/sandboxes/file-system-snapshots.md#start-a-sandbox-with-a-snapshot-mount).

Replace `[OUTPOST-TOKEN]` with the token you copied, `[OUTPOST-NAME]` with your outpost name, and `[SANDBOX-NAME]` with a `cws-agent` workspace name for this sandbox. For the workspace name, use 1 to 40 lowercase letters, digits, or hyphens, starting with a letter or digit:

```bash theme={"system"}
export DEVIN_OUTPOSTS_TOKEN="[OUTPOST-TOKEN]"
cws-agent launch [SANDBOX-NAME] --outpost [OUTPOST-NAME]
```

The tool passes the token into the sandbox and starts one worker.

To view the worker's terminal, run:

```bash theme={"system"}
cws-agent connect [SANDBOX-NAME] --cmd 'tmux attach -t outpost-0'
```

Detach with **Ctrl-b**, then **d**, and continue to [Run and verify a Devin session](#run-and-verify-a-devin-session). This worker connects to Devin Cloud. It's separate from the interactive Devin command-line interface (CLI) launched with `--agent devin`.

## Set up with the Sandboxes SDK

Use this alternative to launch a worker directly, without `cws-agent`. It doesn't configure persistent storage.

Run Python snippets in the virtual environment created in [Configure credentials and install the client](#configure-credentials-and-install-the-client). Save TypeScript snippets as `.mts` files in the project where you install the client, then run them with `npx tsx [FILENAME].mts`.

### Configure credentials and install the client

Use the **Forge API key** configuration from [Choose sandbox credentials](#choose-sandbox-credentials), including `WANDB_ENTITY` for the team that holds the secret. This SDK flow uses [Forge secret injection](https://docs.coreweave.com/products/sandboxes/secrets.md) on serverless capacity. It doesn't support a CoreWeave API access token or CoreWeave Kubernetes Service (CKS) placement.

Ask a Forge administrator to [add a team secret](https://docs.coreweave.com/products/wandb/platform/secrets.md#add-a-secret) named `DEVIN_OUTPOSTS_TOKEN` with your outpost token as its value. Use a Forge API key with access to that team. Keep the value in Secret Manager. The SDK script sends only the secret's name.

Choose a client and install it locally:

> [tab] Python
>
> Use Python 3.11 or later and `uv`:
>
> ```bash theme={"system"}
> uv venv --python 3.11
> source .venv/bin/activate
> uv pip install 'cwsandbox[wandb]>=1.14.2'
> ```

> [tab] TypeScript
>
> Use Node.js 22 or later. Install the client and TypeScript runner in your project:
>
> ```bash theme={"system"}
> npm install @coreweave/cwsandbox@1.0.0 tsx
> ```

### Start the worker

The platform resolves the Forge secret and injects it as `DEVIN_OUTPOSTS_TOKEN` for the worker. You don't need to export the outpost token locally for this SDK flow.

> [!TIP]
>
> To reduce worker startup time, use your own image with the Devin CLI, Git, language runtimes, and project dependencies preinstalled. Set `container_image` in Python or `containerImage` in TypeScript to that image. If it already includes Git and certificate authority (CA) certificates, remove the `apt-get` commands from the example.

The following script creates a sandbox from Cognition's official worker image and runs `devin worker` as the sandbox's main command. The worker's output becomes the sandbox log. If the worker exits with an error, the platform restarts the container up to a restart limit.

> [tab] Python
>
> ```python title="start_outpost_worker.py" theme={"system"}
> from sandbox_auth import AUTH
> import sys
>
> from cwsandbox import ResourceOptions, Sandbox, Secret
>
> outpost = sys.argv[1]
>
> # The worker image ships the Devin CLI but not git, which Devin needs to
> # clone repositories. Install it, then hand the process over to the worker.
> command = """
> apt-get update -qq
> DEBIAN_FRONTEND=noninteractive apt-get install -y -qq git ca-certificates >/dev/null
> mkdir -p /workspace
> cd /workspace
> exec devin worker start --outpost="$DEVIN_OUTPOST"
> """
>
> sandbox = Sandbox.run(
>     "bash", "-ec", command,
>     container_image="public.ecr.aws/e0h8a4b6/devin-cli:stable",
>     placement_mode="serverless",
>     secrets=[Secret(store="wandb", name="DEVIN_OUTPOSTS_TOKEN")],
>     environment_variables={
>         "DEVIN_OUTPOST": outpost,
>     },
>     max_lifetime_seconds=8 * 3600,
>     resources=ResourceOptions(
>         requests={"cpu": "2", "memory": "4Gi"},
>         limits={"cpu": "2", "memory": "4Gi"},
>     ),
>     tags=["devin-outpost-worker"],
>     auth=AUTH,
> )
> try:
>     sandbox.wait()
> except BaseException:
>     sandbox.stop().result()
>     raise
>
> print(f"Worker sandbox ID: {sandbox.sandbox_id}")
> ```

> [tab] TypeScript
>
> ```typescript title="start_outpost_worker.mts" theme={"system"}
> import { client } from "./sandbox-client.mts";
>
> const outpost = process.argv[2];
> if (!outpost) throw new Error("Pass an outpost name.");
>
> const command = `
> apt-get update -qq
> DEBIAN_FRONTEND=noninteractive apt-get install -y -qq git ca-certificates >/dev/null
> mkdir -p /workspace
> cd /workspace
> exec devin worker start --outpost="$DEVIN_OUTPOST"
> `;
>
> const sandbox = await client.run(["bash", "-ec", command], {
>   containerImage: "public.ecr.aws/e0h8a4b6/devin-cli:stable",
>   secrets: [{ store: "wandb", name: "DEVIN_OUTPOSTS_TOKEN" }],
>   environmentVariables: {
>     DEVIN_OUTPOST: outpost,
>   },
>   resources: { cpu: "2", memory: "4Gi" },
>   maxLifetimeSeconds: 8 * 3600,
>   waitUntilRunning: false,
>   tags: ["devin-outpost-worker"],
> });
> try {
>   await sandbox.wait();
> } catch (error) {
>   await sandbox.stop();
>   throw error;
> }
> console.log(`Worker sandbox ID: ${sandbox.sandboxId}`);
> ```

Run it with the outpost name from [Create an outpost in Devin Cloud](#create-an-outpost-in-devin-cloud):

> [tab] Python
>
> ```bash theme={"system"}
> python start_outpost_worker.py [OUTPOST-NAME]
> ```

> [tab] TypeScript
>
> ```bash theme={"system"}
> npx tsx start_outpost_worker.mts [OUTPOST-NAME]
> ```

In Python, `sandbox.wait()` returns when the sandbox is running or has already completed. Installation and worker authentication can still be in progress, so check the worker before submitting a task. The worker starts from `/workspace`. A session for `your-org/app` checks out its repository under `/workspace/repos/app`.

The script doesn't use a `with` block, so a running sandbox continues after the script exits.

> [!WARNING]
>
> `max_lifetime_seconds` is a hard cap that can't be extended later. When it expires, the platform terminates the sandbox, interrupting execution for any session using the worker. This script configures no snapshot or persistent volume. A container restart resets its writable filesystem, including files under `/workspace`. Keep results outside the sandbox, such as in a repository Devin pushes to.

## Run and verify a Devin session

Use an outpost with only this worker and no other queued or active sessions for the test. Choose a unique, non-secret value for this test and replace `[PROOF-VALUE]` in the following task. In Devin Cloud, start a new session and select your outpost under **Configuration > Virtual environment**. Submit the following task, beginning with `Write the exact text`. Or, in Slack, send the full message:

```text theme={"system"}
@Devin !outpost [OUTPOST-NAME] Write the exact text [PROOF-VALUE] to /workspace/outpost-proof.txt and read the file back. Report its contents.
```

After Devin reports completion, read the file from your own terminal using the command for your setup. Replace `[SANDBOX-NAME]` with your `cws-agent` workspace name or `[SANDBOX-ID]` with the ID printed by the SDK script:

> [tab] cws-agent
>
> ```bash theme={"system"}
> cws-agent exec [SANDBOX-NAME] 'cat /workspace/outpost-proof.txt'
> ```

> [tab] Sandboxes SDK
>
> > [tab] Python
> >
> > ```python theme={"system"}
> > from sandbox_auth import AUTH
> > from cwsandbox import Sandbox
> >
> > sandbox = Sandbox.from_id("[SANDBOX-ID]", auth=AUTH).result()
> > result = sandbox.exec(["cat", "/workspace/outpost-proof.txt"], check=True).result()
> > print(result.stdout, end="")
> > ```
>
> > [tab] TypeScript
> >
> > ```typescript theme={"system"}
> > import { client } from "./sandbox-client.mts";
> >
> > const sandbox = await client.fromId("[SANDBOX-ID]");
> > const result = await sandbox.commands.run(["cat", "/workspace/outpost-proof.txt"], { check: true });
> > process.stdout.write(result.stdout);
> > ```

Confirm that the output matches your unique value. Reading it through that sandbox's ID ties the session's file write to the sandbox you created. The absolute path avoids relying on the session's working directory.

If the session stays queued, check the worker's log as shown in the next section. A worker serving an earlier session can't claim another until the earlier session ends or is suspended. If you no longer need the earlier session, end it in Devin Cloud. Alternatively, start another worker.

## Check the worker and stop it

For `cws-agent`, attach to the worker terminal as shown in the quick start. For the SDK path, inspect its status and recent logs. Replace `[SANDBOX-ID]` with the printed ID:

> [tab] Python
>
> ```python theme={"system"}
> from sandbox_auth import AUTH
> from cwsandbox import Sandbox
>
> sandbox = Sandbox.from_id("[SANDBOX-ID]", auth=AUTH).result()
> print("Sandbox status:", sandbox.get_status())
> for container in sandbox.container_statuses:
>     print(container.name, container.state, container.exit_code, container.restart_count)
> for line in sandbox.stream_logs(tail_lines=100):
>     print(line, end="")
> ```

> [tab] TypeScript
>
> ```typescript theme={"system"}
> import { client } from "./sandbox-client.mts";
>
> const sandbox = await client.fromId("[SANDBOX-ID]");
> console.log("Sandbox status:", sandbox.status, "Exit code:", sandbox.exitCode);
> for (const line of await sandbox.logs.read({ tailLines: 100 })) {
>   process.stdout.write(line);
> }
> ```

Rerun this check to fetch newer logs. The Python client also reports per-container state, exit codes, and restart counts. The TypeScript client doesn't expose those details.

If the log reports that the Outposts API rejected the worker's token, confirm that you used the token copied when creating the outpost. Confirm that the token belongs to the account that owns the outpost. If you use a service user's v3 API token instead, its role must grant **Outposts write** (`account.outposts.write`). Correct the credential, then create the sandbox again.

A sandbox can report `running` while its worker repeatedly exits and restarts. Inspect its logs and, with the Python client, the per-container details shown in the preceding example.

Stop a worker that keeps failing authentication before creating its replacement. If startup fails without a useful reason, retain the sandbox ID and logs for [CoreWeave Support](https://docs.coreweave.com/support/contact.md).

Stop the sandbox when you no longer need the worker. For serverless setup, see [Get started](https://docs.coreweave.com/products/sandboxes/get-started.md).

Wait for the active Devin session to finish and save its results, then stop compute using the command for your setup:

> [tab] cws-agent
>
> ```bash theme={"system"}
> cws-agent down [SANDBOX-NAME]
> ```
>
> `down` snapshots the workspace before stopping. If capture fails, inspect the reported error and `cws-agent status [SANDBOX-NAME]`, then resolve the failure before retrying. If you can discard unsaved changes, use `cws-agent down [SANDBOX-NAME] --no-snapshot`.

> [tab] Sandboxes SDK
>
> > [tab] Python
> >
> > ```python theme={"system"}
> > from sandbox_auth import AUTH
> > from cwsandbox import Sandbox
> >
> > sandbox = Sandbox.from_id("[SANDBOX-ID]", auth=AUTH).result()
> > sandbox.stop().result()
> > ```
>
> > [tab] TypeScript
> >
> > ```typescript theme={"system"}
> > import { client } from "./sandbox-client.mts";
> >
> > const sandbox = await client.fromId("[SANDBOX-ID]");
> > await sandbox.stop();
> > ```
>
> This example has no persistent mount. Copy files out or push changes to your repository before stopping.

Ending a Devin session doesn't stop this worker's sandbox. To restore a `cws-agent` workspace, see its [Devin Outposts guide](https://github.com/coreweave/cws-agent/blob/main/docs/self-hosted.md#devin-outposts).

## Optional: Customize the environment

You can customize the worker environment in the following ways:

* **Bring your own image.** The official image contains the `devin` CLI and little else. Build an image from it that adds your toolchain, and pass it as `container_image` in Python or `containerImage` in TypeScript. Devin requires `git`. Screen recording requires `ffmpeg`, and the browser and computer-use tools require a compatible browser binary.

  For amd64 images based on the official Ubuntu image, install Google Chrome. Ubuntu's `chromium` package is a snap stub that doesn't work in containers. See [Devin's container setup](https://docs.devin.ai/cloud/outposts/quickstart). Computer use also requires a running graphical display, such as Xvfb, with `DISPLAY` set for the worker.

  The worker searches standard install locations. If it doesn't find your binary, set `DEVIN_CHROME_PATH` to its absolute path. See the [Devin Outposts reference](https://docs.devin.ai/cloud/outposts/reference).
* **Configure GPUs.** See [sandbox GPU configuration](https://docs.coreweave.com/products/sandboxes/client/guides/sandbox-configuration.md#gpu) for the available options. This guide's worker example uses CPU resources only.
* **Run more workers.** A worker serves one session at a time. Run the script again with the same outpost name to start another worker for the queue.
* **Create one sandbox per session.** The worker here reuses its sandbox across sessions. For a fresh sandbox per session, see Devin's [orchestration guide](https://docs.devin.ai/cloud/outposts/orchestration).
