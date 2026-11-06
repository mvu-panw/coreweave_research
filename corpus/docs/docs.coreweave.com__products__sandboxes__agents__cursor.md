# Run Cursor in a sandbox

Source: https://docs.coreweave.com/products/sandboxes/agents/cursor

# Run Cursor in a sandbox

> Run Cursor CLI interactively or automate coding tasks in a CoreWeave sandbox.

Run the Cursor command-line interface (CLI) against a repository in a CoreWeave
sandbox. Attach your terminal for interactive work, or run a prompt through the
Sandboxes software development kit (SDK) and collect the result. The CLI process,
workspace, and commands run in the sandbox. Model requests go to Cursor.

Cursor also supports [Self-Hosted Machines](https://cursor.com/docs/cloud-agent/self-hosted),
where Cursor's cloud runs the agent loop and a separate worker executes tool calls.

## Prerequisites

Before you begin, you need the following:

* A [Forge API key or CoreWeave API access token](https://docs.coreweave.com/products/sandboxes/placement.md#choose-and-get-credentials).

* A [Cursor user API key](https://cursor.com/docs/cli/reference/authentication#api-key-authentication)
  and access to a model supported by Cursor CLI.

* A public repository URL. Private repositories require Git credentials inside
  the sandbox.

* Outbound connectivity to Cursor, its download host, and your Git host.

Cursor reads `CURSOR_API_KEY` inside the sandbox. Cursor can send
prompts, file contents, and tool output to its service. Use a repository and
credentials appropriate for the task.

## Choose sandbox credentials

These examples use serverless capacity. Both credentials support serverless sandboxes. See [Choose and get credentials](https://docs.coreweave.com/products/sandboxes/placement.md#choose-and-get-credentials) to obtain either credential. Agent and model-provider credentials are configured separately.

> [tab] Forge API key
>
> Replace `[WANDB-API-KEY]` with your Forge API key and export it in your local terminal:
>
> ```bash theme={"system"}
> export WANDB_API_KEY="[WANDB-API-KEY]"
> unset CWSANDBOX_API_KEY
> ```
>
> `cws-agent` selects Forge authentication when `CWSANDBOX_API_KEY` is unset.

> [tab] CoreWeave API access token
>
> Replace `[API-ACCESS-TOKEN]` with your CoreWeave API access token and export it in your local terminal:
>
> ```bash theme={"system"}
> export CWSANDBOX_API_KEY="[API-ACCESS-TOKEN]"
> ```

## Run Cursor CLI with cws-agent

Use `cws-agent` to create a sandbox, install Cursor, and attach your terminal.
Interactive attachment requires an interactive terminal (TTY) on macOS, Linux,
or Windows Subsystem for Linux (WSL). Native Windows terminals aren't supported.

Export your Cursor key locally. `cws-agent` forwards it into the sandbox's
environment:

```bash theme={"system"}
export CURSOR_API_KEY="[CURSOR-API-KEY]"
```

1. Follow the [`cws-agent` installation instructions](https://github.com/coreweave/cws-agent#install).

2. Replace `[SANDBOX-NAME]` with a session name containing 1 to 40 lowercase
   letters, digits, or hyphens, starting with a letter or digit. Replace
   `[REPOSITORY-URL]` with your repository URL:

   ```bash theme={"system"}
   cws-agent launch [SANDBOX-NAME] --agent cursor --repo-url [REPOSITORY-URL] --lifetime 2h --permission-mode native --no-config-sync
   ```

   Cursor opens in `/workspace/project`. If a workspace trust prompt appears,
   accept it. `--permission-mode native` retains Cursor's approval settings.
   `cws-agent` otherwise uses `--force`. `--no-config-sync` skips importing your
   local skills and Model Context Protocol (MCP) configuration.

3. Ask Cursor to create a file you can retrieve:

   ```text theme={"system"}
   Create sandbox-proof.txt in the current directory containing exactly
   Hello from CoreWeave followed by a newline, then read it back.
   Do not commit or push anything.
   ```

   Approve any prompts for the task. Exit Cursor with `/exit`.
   In your local terminal, read the file:

   ```bash theme={"system"}
   cws-agent exec [SANDBOX-NAME] 'cat /workspace/project/sandbox-proof.txt'
   ```

   The output should be `Hello from CoreWeave`. Exiting Cursor leaves the
   sandbox running.

4. After exiting all Cursor sessions in the sandbox, remove Cursor's leftover
   `worker.sock` socket files, save the workspace, and stop compute:

   ```bash theme={"system"}
   cws-agent exec [SANDBOX-NAME] 'find /workspace/home/.cursor/projects -type s -name worker.sock -delete'
   cws-agent down [SANDBOX-NAME]
   ```

   The cleanup removes socket files that can block snapshot creation. `down`
   takes a snapshot before stopping the sandbox.
   If snapshot creation fails, the sandbox stays running. Resolve the error and
   retry `down` before restoring.

5. To return to the saved workspace, keep `CURSOR_API_KEY` exported locally and run:

   ```bash theme={"system"}
   cws-agent restore [SANDBOX-NAME] --connect --permission-mode native --no-config-sync
   ```

   Ask Cursor to read the `sandbox-proof.txt` file to verify that it was restored.
   When finished, exit Cursor and repeat the cleanup and `down` commands.

### Run an unattended prompt

Choose a new session name. In your local terminal, launch with `--detach` to skip
terminal attachment, then send a prompt:

```bash theme={"system"}
cws-agent launch [SANDBOX-NAME] --agent cursor --repo-url [REPOSITORY-URL] --lifetime 2h --permission-mode native --no-config-sync --detach
cws-agent run [SANDBOX-NAME] 'Create sandbox-proof.txt containing exactly Hello from CoreWeave followed by a newline, then read it back. Do not commit or push anything.'
```

`cws-agent run` passes Cursor's `--force` flag by default so the headless task can
write files without interactive approval. Cursor retains explicit deny rules.

To attach your terminal to the running session, run:

```bash theme={"system"}
cws-agent connect [SANDBOX-NAME] --permission-mode native --no-config-sync
```

When finished, exit Cursor if attached, read the result with `cws-agent exec`,
then clean up the sockets and save with `cws-agent down` as shown in
[Run Cursor CLI with cws-agent](#run-cursor-cli-with-cws-agent).

## Run a task with the Sandboxes SDK

Use the Sandboxes SDK to manage a task directly. This
path creates a separate sandbox, runs Cursor in print mode, retrieves the file,
and stops the sandbox in a cleanup block. It doesn't configure snapshots or
require `cws-agent`.

### Choose how to supply the Cursor key

Both scripts take an authentication mode as their first argument:

| Mode | Sandbox credential | Cursor credential |
| - | - | - |
| `forge` | `WANDB_API_KEY` | A Forge team secret, resolved by the server. |
| `coreweave` | `CWSANDBOX_API_KEY` | Local `CURSOR_API_KEY`, passed through the sandbox environment map. |

These examples use serverless placement. Forge secret injection requires Forge authentication and serverless placement.

> [tab] Forge API key
>
> For `forge` mode, ask a Forge administrator to [add your Cursor key as a team secret](https://docs.coreweave.com/products/wandb/platform/secrets.md#add-a-secret).
> In your local terminal, replace `[WANDB-ENTITY]` with your team name and
> `[CURSOR-SECRET-NAME]` with the secret name:
>
> ```bash theme={"system"}
> export WANDB_API_KEY="[WANDB-API-KEY]"
> export WANDB_ENTITY="[WANDB-ENTITY]"
> export CURSOR_SECRET_NAME="[CURSOR-SECRET-NAME]"
> ```
>
> Your Forge API key must have access to that team. The scripts map the named
> secret to `CURSOR_API_KEY` inside the sandbox. See
> [Use Forge secrets](https://docs.coreweave.com/products/sandboxes/secrets.md).

> [tab] CoreWeave API access token
>
> For `coreweave` mode, set `CWSANDBOX_API_KEY` to a CoreWeave API access token with the `sandbox_user` IAM action. See [Choose and get credentials](https://docs.coreweave.com/products/sandboxes/placement.md#choose-and-get-credentials). Export your Cursor key in the same local terminal:
>
> ```bash theme={"system"}
> export CWSANDBOX_API_KEY="[API-ACCESS-TOKEN]"
> export CURSOR_API_KEY="[CURSOR-API-KEY]"
> ```
>
> The `coreweave` path passes the Cursor key as a plain environment value in the sandbox creation request. This is an exception to the SDK's recommendation to use secret references for credentials. Use this path only if your credential-handling policy permits it. Avoid logging the request or committing the key.

### Install a client

Choose a language and install the client locally:

> [tab] Python
>
> Use Python 3.11 or later and `uv`. In a new project directory, run:
>
> ```bash theme={"system"}
> uv init --python 3.11
> uv add 'cwsandbox==1.14.2'
> ```

> [tab] TypeScript
>
> Use Node.js 22 or later. In your project directory, run:
>
> ```bash theme={"system"}
> npm install @coreweave/cwsandbox@1.0.0 tsx
> ```

### Create, run, and clean up

Save the script for your language using the filename shown. Each script installs
Cursor, clones the repository passed on the command line, and asks Cursor to
write the `sandbox-proof.txt` file.

The `--print`, `--force`, and `--trust` flags enable non-interactive output,
permit file changes, and trust the workspace. Use this
example only with a repository you trust. See
[Cursor headless mode](https://cursor.com/docs/cli/headless).

> [tab] Python
>
> ```python title="run_cursor_sandbox.py" theme={"system"}
> import os
> import sys
>
> from cwsandbox import AuthHeaders, AuthStrategy, Sandbox, Secret
>
> if len(sys.argv) != 3 or sys.argv[1] not in ("forge", "coreweave"):
>     raise SystemExit("Pass forge or coreweave, then a repository URL.")
>
> mode, repository = sys.argv[1:]
> if mode == "forge":
>     auth = AuthHeaders(
>         headers={
>             "x-wandb-api-key": os.environ["WANDB_API_KEY"],
>             "x-entity-id": os.environ["WANDB_ENTITY"],
>         },
>         strategy="wandb_api_key",
>     )
>     credentials = {"secrets": [Secret(
>         store="wandb", name=os.environ["CURSOR_SECRET_NAME"],
>         env_var="CURSOR_API_KEY",
>     )]}
> else:
>     auth = AuthStrategy.COREWEAVE_API_KEY
>     credentials = {
>         "environment_variables": {"CURSOR_API_KEY": os.environ["CURSOR_API_KEY"]},
>     }
>
> sandbox = Sandbox.run(
>     auth=auth,
>     placement_mode="serverless",
>     container_image="node:22-bookworm",
>     resources={"cpu": "2", "memory": "4Gi"},
>     max_lifetime_seconds=2 * 3600,
>     **credentials,
> )
> try:
>     sandbox.wait()
>     commands = [
>         ["bash", "-o", "pipefail", "-ec", "curl -fsSL https://cursor.com/install | bash"],
>         ["mkdir", "-p", "/workspace"],
>         ["git", "clone", "--", repository, "/workspace/project"],
>     ]
>     for command in commands:
>         sandbox.exec(command, timeout_seconds=900, check=True).result()
>
>     result = sandbox.exec(
>         [
>             "/root/.local/bin/agent",
>             "--print", "--force", "--trust", "--output-format", "text",
>             "Create sandbox-proof.txt containing exactly Hello from CoreWeave "
>             "followed by a newline, then read it back. Do not commit or push anything.",
>         ],
>         cwd="/workspace/project",
>         timeout_seconds=300,
>         check=True,
>     ).result()
>     print(result.stdout)
>     proof = sandbox.exec(
>         ["cat", "/workspace/project/sandbox-proof.txt"], check=True
>     ).result()
>     print(proof.stdout, end="")
> finally:
>     sandbox.stop().result()
> ```

> [tab] TypeScript
>
> ```typescript title="run_cursor_sandbox.mts" theme={"system"}
> import { createSandboxClientFromEnv as coreweaveClient } from "@coreweave/cwsandbox/node";
> import { createSandboxClient as forgeClient } from "@coreweave/cwsandbox/wandb";
>
> const [mode, repository] = process.argv.slice(2);
> if (!repository || (mode !== "forge" && mode !== "coreweave")) {
>   throw new Error("Pass forge or coreweave, then a repository URL.");
> }
>
> const credential = mode === "forge"
>   ? process.env.CURSOR_SECRET_NAME : process.env.CURSOR_API_KEY;
> if (!credential) {
>   throw new Error("Set CURSOR_SECRET_NAME for forge or CURSOR_API_KEY for coreweave.");
> }
> const client = mode === "forge"
>   ? forgeClient({ apiKey: process.env.WANDB_API_KEY, entity: process.env.WANDB_ENTITY })
>   : coreweaveClient();
> const credentials = mode === "forge"
>   ? { secrets: [{ store: "wandb", name: credential, envVar: "CURSOR_API_KEY" }] }
>   : { environmentVariables: { CURSOR_API_KEY: credential } };
> const sandbox = await client.create({
>   containerImage: "node:22-bookworm",
>   resources: { cpu: "2", memory: "4Gi" },
>   maxLifetimeSeconds: 2 * 3600,
>   ...credentials,
>   waitUntilRunning: false,
> });
> try {
>   await sandbox.wait();
>   const commands = [
>     ["bash", "-o", "pipefail", "-ec", "curl -fsSL https://cursor.com/install | bash"],
>     ["mkdir", "-p", "/workspace"],
>     ["git", "clone", "--", repository, "/workspace/project"],
>   ];
>   for (const command of commands) {
>     await sandbox.commands.run(command, { timeoutMs: 900_000, check: true });
>   }
>
>   const result = await sandbox.commands.run(
>     [
>       "/root/.local/bin/agent",
>       "--print", "--force", "--trust", "--output-format", "text",
>       "Create sandbox-proof.txt containing exactly Hello from CoreWeave " +
>         "followed by a newline, then read it back. Do not commit or push anything.",
>     ],
>     { cwd: "/workspace/project", timeoutMs: 300_000, check: true },
>   );
>   console.log(result.stdout);
>   const proof = await sandbox.commands.run(
>     ["cat", "/workspace/project/sandbox-proof.txt"], { check: true },
>   );
>   process.stdout.write(proof.stdout);
> } finally {
>   await sandbox.stop();
> }
> ```

In the local terminal where you set your credentials, replace `[AUTH-MODE]`
with `forge` or `coreweave`, and `[REPOSITORY-URL]` with your repository URL:

> [tab] Python
>
> ```bash theme={"system"}
> uv run python run_cursor_sandbox.py [AUTH-MODE] [REPOSITORY-URL]
> ```

> [tab] TypeScript
>
> ```bash theme={"system"}
> npx tsx run_cursor_sandbox.mts [AUTH-MODE] [REPOSITORY-URL]
> ```

The script prints Cursor's response followed by the file contents,
`Hello from CoreWeave`. The cleanup block calls `stop()` even if setup or execution
raises an error.
Retrieve any additional files before the cleanup block runs. For larger results,
use [file operations](https://docs.coreweave.com/products/sandboxes/client/guides/file-operations.md).

The 2-hour lifetime is a maximum wall-clock limit, including startup. Each
command also has its own timeout. Changing the command timeout doesn't extend
the sandbox lifetime.

## Troubleshoot

Use these checks to resolve common issues:

* If sandbox creation fails, verify the credential for your selected
  authentication mode.

* If a Forge secret can't be resolved, check `WANDB_ENTITY`, `CURSOR_SECRET_NAME`,
  and your API key's team access.

* If Cursor reports an authentication error, verify the key in your Forge secret or local `CURSOR_API_KEY`, depending on the mode, and check your account's model access.

* If an SDK prompt only proposes changes, confirm that the Cursor command
  includes `--force`.

* If installation, cloning, or model requests fail, check outbound connectivity
  and provider credentials. For CoreWeave Kubernetes Service (CKS) placement,
  your runner policy must allow the required destinations.

## Next steps

For more information, see these guides:

* [Run agents on CoreWeave sandboxes](https://docs.coreweave.com/products/sandboxes/agents.md) covers placement,
  longer sessions, and workspace lifecycle.
* [Cursor with cws-agent](https://github.com/coreweave/cws-agent/blob/main/docs/cursor.md)
  covers saved conversations and configuration imports.
* [Cursor CLI documentation](https://cursor.com/docs/cli/overview) covers agent
  configuration and supported modes.
