# Run Muse Code in a sandbox

Source: https://docs.coreweave.com/products/sandboxes/agents/muse-code

# Run Muse Code in a sandbox

> Run Muse Code CLI on a repository in a sandbox, retrieve the result, and stop compute.

Run Muse Code inside a CoreWeave sandbox to edit files and execute commands in a remote workspace. This guide uses the Sandboxes software development kit (SDK) to install the command-line interface (CLI) and clone a repository. You then run a task without an interactive terminal and retrieve the result before you stop the sandbox. The agent process and workspace run on CoreWeave, and model requests go to Meta.

## Prerequisites

Before you begin, you need the following:

* A [Forge API key or CoreWeave API access token](https://docs.coreweave.com/products/sandboxes/placement.md#choose-and-get-credentials).
* A [Meta API key](https://dev.meta.ai/docs/muse-code/auth) with access to Muse Code.
* A public repository URL the sandbox can clone. Private repositories require Git credentials inside the sandbox.
* Python 3.11 or later with `uv`, or Node.js 22 or later with `npm`.

Load your credentials from your secret manager into your local terminal environment. Replace `[META-API-KEY]` with your Meta API key:

```bash theme={"system"}
export META_API_KEY="[META-API-KEY]"
```

The script passes the Meta key over standard input so it doesn't appear in command arguments or sandbox configuration. For a shared team credential injected as an environment variable at sandbox creation, see [Forge secrets](https://docs.coreweave.com/products/sandboxes/secrets.md).

## Choose sandbox credentials

These examples use serverless capacity. Both credentials support serverless sandboxes. See [Choose and get credentials](https://docs.coreweave.com/products/sandboxes/placement.md#choose-and-get-credentials) to obtain either credential. Agent and model-provider credentials are configured separately.

After creating your local project in the next section, save `sandbox_auth.py` or `sandbox-client.mts` for your language beside the scripts you run from this guide. Use the same file for creation, reconnection, and cleanup. It stores your authentication choice, not the key itself.

> [tab] Forge API key
>
> Replace `[WANDB-API-KEY]` with your Forge API key and export it in your local terminal:
>
> ```bash theme={"system"}
> export WANDB_API_KEY="[WANDB-API-KEY]"
> ```
>
> > [tab] Python
> >
> > ```python title="sandbox_auth.py" theme={"system"}
> > from cwsandbox import AuthStrategy
> >
> > AUTH = AuthStrategy.WANDB
> > ```
>
> > [tab] TypeScript
> >
> > ```typescript title="sandbox-client.mts" theme={"system"}
> > import { createSandboxClientFromEnv } from "@coreweave/cwsandbox/wandb";
> >
> > export const client = createSandboxClientFromEnv();
> > ```

> [tab] CoreWeave API access token
>
> Replace `[API-ACCESS-TOKEN]` with your CoreWeave API access token and export it in your local terminal:
>
> ```bash theme={"system"}
> export CWSANDBOX_API_KEY="[API-ACCESS-TOKEN]"
> ```
>
> > [tab] Python
> >
> > ```python title="sandbox_auth.py" theme={"system"}
> > from cwsandbox import AuthStrategy
> >
> > AUTH = AuthStrategy.COREWEAVE_API_KEY
> > ```
>
> > [tab] TypeScript
> >
> > ```typescript title="sandbox-client.mts" theme={"system"}
> > import { createSandboxClientFromEnv } from "@coreweave/cwsandbox/node";
> >
> > export const client = createSandboxClientFromEnv();
> > ```

## Install the Sandboxes client

Choose a language and prepare a local project:

> [tab] Python
>
> ```bash theme={"system"}
> mkdir muse-sandbox
> cd muse-sandbox
> uv init --bare --python 3.11
> uv venv --python 3.11
> source .venv/bin/activate
> uv pip install 'cwsandbox[wandb]>=1.14.2'
> ```

> [tab] TypeScript
>
> ```bash theme={"system"}
> mkdir muse-sandbox
> cd muse-sandbox
> npm init -y
> npm install @coreweave/cwsandbox@1.0.0 tsx
> ```

## Run a task in the sandbox

Save the script for your language using the filename shown. Each script creates a serverless sandbox with a 30-minute maximum lifetime and performs these steps:

1. Installs Muse Code with Meta's installer.
2. Clones your repository into the `/workspace/project` directory.
3. Runs `muse exec` to build and test a sparkline CLI that renders numbers as a small chart.
4. Runs the generated CLI independently, checks its output, and saves the `sparkline.mjs` file locally.
5. Stops the sandbox in a `finally` block, including when setup or execution fails.

These examples were tested with Muse Code 1.3.0. The installer can install a newer version, so each script runs `muse --version` after installation.

The example uses `--yolo` to disable Muse Code's approval prompts and operating system (OS) sandbox and trust the workspace for this run. CoreWeave supplies the outer sandbox. Muse can access files, credentials, and network destinations available inside that sandbox. Use a repository you trust and provide only the credentials the task needs. For more information, see [Muse Code permissions](https://dev.meta.ai/docs/muse-code/permissions).

> [tab] Python
>
> ```python title="run_muse.py" theme={"system"}
> from sandbox_auth import AUTH
> import os
> import sys
> from pathlib import Path
>
> from cwsandbox import Sandbox
>
> if len(sys.argv) != 2:
>     raise SystemExit("Usage: python run_muse.py [REPOSITORY-URL]")
> meta_api_key = os.environ["META_API_KEY"]
>
> sandbox = Sandbox.run(
>     container_image="node:22-bookworm",
>     resources={"cpu": "2", "memory": "4Gi"},
>     max_lifetime_seconds=1800,
>     tags=["muse-code"],
>     auth=AUTH,
> )
> try:
>     sandbox.wait()
>     commands = [
>         ["bash", "-o", "pipefail", "-ec", "curl -fsSL https://dev.meta.ai/install.sh | bash"],
>         ["bash", "-ec", '"$HOME/.local/bin/muse" --version'],
>         ["git", "clone", "--", sys.argv[1], "/workspace/project"],
>     ]
>     for command in commands:
>         result = sandbox.exec(command, timeout_seconds=600, check=True).result()
>         print(result.stdout, end="")
>
>     agent = sandbox.exec(
>         [
>             "bash", "-ec",
>             'IFS= read -r META_API_KEY; export META_API_KEY; '
>             'exec "$HOME/.local/bin/muse" exec --yolo "$1"',
>             "bash",
>             "Create sparkline.mjs, a dependency-free Node.js CLI that converts its "
>             "numeric arguments to a sparkline using ▁▂▃▄▅▆▇█. Scale from the minimum "
>             "to the maximum and round to the nearest bar index. "
>             "Running node sparkline.mjs 2 4 8 4 2 must print ▁▃█▃▁ followed by "
>             "a newline. Run that command to test it.",
>         ],
>         cwd="/workspace/project",
>         stdin=True,
>         timeout_seconds=600,
>     )
>     # Keep stdin open until Muse finishes to avoid aborting a quiet request.
>     agent.stdin.writeline(meta_api_key).result()
>     result = agent.result()
>     print(result.stdout, end="")
>     print(result.stderr, end="", file=sys.stderr)
>     if result.returncode != 0:
>         raise SystemExit(result.returncode)
>
>     chart = sandbox.exec(
>         ["node", "sparkline.mjs", "2", "4", "8", "4", "2"],
>         cwd="/workspace/project", check=True,
>     ).result()
>     if chart.stdout != "▁▃█▃▁\n":
>         raise RuntimeError(f"Unexpected sparkline: {chart.stdout!r}")
>     print(chart.stdout, end="")
>     source = sandbox.exec(
>         ["cat", "/workspace/project/sparkline.mjs"], check=True
>     ).result()
>     Path("sparkline.mjs").write_text(source.stdout, encoding="utf-8")
> finally:
>     sandbox.stop().result()
> ```

> [tab] TypeScript
>
> ```typescript title="run_muse.mts" theme={"system"}
> import { writeFile } from "node:fs/promises";
> import { client } from "./sandbox-client.mts";
>
> const repository = process.argv[2];
> if (!repository) throw new Error("Pass a repository URL.");
> const metaApiKey = process.env.META_API_KEY;
> if (!metaApiKey) throw new Error("Set META_API_KEY.");
>
> const sandbox = await client.create({
>   containerImage: "node:22-bookworm",
>   resources: { cpu: "2", memory: "4Gi" },
>   maxLifetimeSeconds: 1800,
>   waitUntilRunning: false,
>   tags: ["muse-code"],
> });
> try {
>   await sandbox.wait();
>   const commands = [
>     ["bash", "-o", "pipefail", "-ec", "curl -fsSL https://dev.meta.ai/install.sh | bash"],
>     ["bash", "-ec", '"$HOME/.local/bin/muse" --version'],
>     ["git", "clone", "--", repository, "/workspace/project"],
>   ];
>   for (const command of commands) {
>     const result = await sandbox.commands.run(command, { timeoutMs: 600_000, check: true });
>     process.stdout.write(result.stdout);
>   }
>
>   const agent = await sandbox.commands.start(
>     [
>       "bash", "-ec",
>       'IFS= read -r META_API_KEY; export META_API_KEY; ' +
>         'exec "$HOME/.local/bin/muse" exec --yolo "$1"',
>       "bash",
>       "Create sparkline.mjs, a dependency-free Node.js CLI that converts its " +
>         "numeric arguments to a sparkline using ▁▂▃▄▅▆▇█. Scale from the minimum " +
>         "to the maximum and round to the nearest bar index. " +
>         "Running node sparkline.mjs 2 4 8 4 2 must print ▁▃█▃▁ followed by " +
>         "a newline. Run that command to test it.",
>     ],
>     {
>       cwd: "/workspace/project",
>       stdin: true,
>       timeoutMs: 600_000,
>     },
>   );
>   // Keep stdin open until Muse finishes to avoid aborting a quiet request.
>   await agent.stdin.write(metaApiKey + "\n");
>   const result = await agent.wait();
>   process.stdout.write(result.stdout);
>   process.stderr.write(result.stderr);
>   if (!result.ok) throw new Error(`Muse Code exited with code ${result.exitCode}.`);
>
>   const chart = await sandbox.commands.run(
>     ["node", "sparkline.mjs", "2", "4", "8", "4", "2"],
>     { cwd: "/workspace/project", check: true },
>   );
>   if (chart.stdout !== "▁▃█▃▁\n") {
>     throw new Error(`Unexpected sparkline: ${JSON.stringify(chart.stdout)}`);
>   }
>   process.stdout.write(chart.stdout);
>   const source = await sandbox.commands.run(
>     ["cat", "/workspace/project/sparkline.mjs"], { check: true },
>   );
>   await writeFile("sparkline.mjs", source.stdout, "utf8");
> } finally {
>   await sandbox.stop();
> }
> ```

In your local project directory, replace `[REPOSITORY-URL]` with your public repository URL, then run the script:

> [tab] Python
>
> ```bash theme={"system"}
> python run_muse.py [REPOSITORY-URL]
> ```

> [tab] TypeScript
>
> ```bash theme={"system"}
> npx tsx run_muse.mts [REPOSITORY-URL]
> ```

After the installation and agent output, the script checks and prints the sparkline:

```text theme={"system"}
▁▃█▃▁
```

The script saves the generated `sparkline.mjs` file in your local project directory, then stops the sandbox. If the file already exists locally, the script overwrites it. The output check runs independently of Muse's own test and verifies this example's input. For a larger task, replace it with tests for your requirements.

These examples don't configure persistent storage. Copy the files you need out of the sandbox before the `finally` block runs. See [file operations](https://docs.coreweave.com/products/sandboxes/client/guides/file-operations.md) and [file system snapshots](https://docs.coreweave.com/products/sandboxes/file-system-snapshots.md).

## Troubleshoot

Use these checks to resolve common issues:

* If sandbox creation fails, check your selected sandbox credential and authentication strategy.
* If Muse Code reports an authentication error, check `META_API_KEY` and your Meta account setup. The sandbox credential doesn't authenticate model requests.
* If installation, cloning, or model requests fail, check outbound access to Meta and your Git host. These examples use serverless placement. To use your own CoreWeave Kubernetes Service (CKS) cluster, apply the client settings in [Configure CKS placement and policy](https://docs.coreweave.com/products/sandboxes/agents.md#configure-cks-placement-and-policy). Confirm that the runner's policy grants egress to those destinations.
* If a larger task times out, adjust the command timeout and sandbox lifetime before running it. The 30-minute lifetime includes startup and installation. See [command timeouts](https://docs.coreweave.com/products/sandboxes/client/guides/execution.md#set-a-timeout) and [sandbox lifecycle](https://docs.coreweave.com/products/sandboxes/client/guides/sandbox-lifecycle.md).

## Next steps

For more information, see these guides:

* [Interactive shells and TTY](https://docs.coreweave.com/products/sandboxes/client/guides/interactive-shells.md) covers terminal access for interactive agents.
* [Run agents on CoreWeave sandboxes](https://docs.coreweave.com/products/sandboxes/agents.md) compares agent integrations and workspace options.
* [Meta's sandboxed execution cookbook](https://dev.meta.ai/docs/cookbook/sandboxed-execution) demonstrates a reproduce, fix, and verify workflow with a custom tool loop in Docker.
* [Muse Code documentation](https://dev.meta.ai/docs/muse-code) covers agent configuration and other CLI workflows.
