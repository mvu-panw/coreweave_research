# Claude Code

Source: https://docs.coreweave.com/products/sandboxes/agents/claude-code

# Claude Code

> Run Claude Code in a CoreWeave sandbox and interact from your terminal, Claude apps, or claude.ai.

Run Claude Code in a CoreWeave sandbox and choose how you interact with it. With the terminal user interface (TUI), you use your local terminal to control Claude Code inside the sandbox. With Remote Control, you use the Claude mobile app, Claude Desktop, or [claude.ai/code](https://claude.ai/code). In both cases, the agent process, tools, and workspace run in the sandbox. Model requests go to your configured model provider.

| Interface | Where you interact | Claude authentication |
| - | - | - |
| Terminal (TUI) | Your local terminal, attached to the sandbox | A Claude account or supported API credentials |
| Remote Control | The Claude mobile app, Claude Desktop, or claude.ai/code | A Claude subscription signed in through `/login` |

For an integration where Anthropic manages the agent loop and a sandbox executes tools, see [Claude Managed Agents](https://docs.coreweave.com/products/sandboxes/agents/claude-managed-agents.md).

## Prerequisites

Before you begin, you need the following:

* A [Forge API key or CoreWeave API access token](https://docs.coreweave.com/products/sandboxes/placement.md#choose-and-get-credentials).
* For the terminal interface, a Claude account or API credentials supported by Claude Code. For Remote Control, a Claude Pro, Max, Team, or Enterprise subscription. API keys and `claude setup-token` tokens don't authenticate Remote Control.
* A repository URL the sandbox can clone. The examples use a public repository. Private repositories require Git credentials inside the sandbox.

For Remote Control, Team and Enterprise accounts need an Owner to enable the feature. Your organization must also permit its transcript storage. Organizations with Zero Data Retention requirements can't enable it. Review Anthropic's [Remote Control requirements](https://code.claude.com/docs/en/remote-control#requirements).

Connections use outbound HTTPS and don't require a public sandbox endpoint or inbound port.

Both setup paths use an 8-hour sandbox lifetime for a working day. The lifetime starts at creation, includes setup and idle time, and can't be extended. When it expires, the sandbox stops even if Claude is working, ending the session. [Save your results and stop the sandbox](#keep-results-and-stop) when you're finished, before the lifetime expires.

For overnight work, choose 24 hours at creation. With `cws-agent`, use `--lifetime 24h`. In the software development kit (SDK) examples, set Python's `max_lifetime_seconds` or TypeScript's `maxLifetimeSeconds` to `24 * 3600`.

## Choose sandbox credentials

These examples use serverless capacity. Both credentials support serverless sandboxes. See [Choose and get credentials](https://docs.coreweave.com/products/sandboxes/placement.md#choose-and-get-credentials) to obtain either credential. Agent and model-provider credentials are configured separately.

For the SDK path, create your local project before you save the configuration file. Save the file for your language beside the scripts you run from this guide. Use the same file for creation, reconnection, and cleanup. It stores your authentication choice, not the key itself.

> [tab] Forge API key
>
> Replace `[WANDB-API-KEY]` with your Forge API key and export it in your local terminal:
>
> ```bash theme={"system"}
> export WANDB_API_KEY="[WANDB-API-KEY]"
> unset CWSANDBOX_API_KEY
> ```
>
> `cws-agent` selects Forge authentication when `CWSANDBOX_API_KEY` is unset. The SDK configuration in this tab selects it explicitly.
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

## Quick start with cws-agent

Choose this setup path to create the sandbox with `cws-agent`. To create it directly with a client library, skip to [Set up with the Sandboxes SDK](#set-up-with-the-sandbox-sdk). Both paths support either interface.

Follow the [`cws-agent` installation instructions](https://github.com/coreweave/cws-agent#install). The tool configures a snapshot mount to save and restore your workspace with [file system snapshots](https://docs.coreweave.com/products/sandboxes/file-system-snapshots.md#start-a-sandbox-with-a-snapshot-mount).

Before Claude opens, `cws-agent` may show a preview of local skills and Model Context Protocol (MCP) servers to import. For this guide, press **Enter** at the import prompt to skip it. You can configure imports later using the [agent tools guidance](https://docs.coreweave.com/products/sandboxes/agents.md#use-tools-efficiently).

Choose one of the following interfaces. Replace `[SANDBOX-NAME]` with a `cws-agent` session name and `[REPOSITORY-URL]` with a public repository URL. Use 1 to 40 lowercase letters, digits, or hyphens for the session name, starting with a letter or digit.

### Use the terminal interface

To use an Anthropic API key, load it into `ANTHROPIC_API_KEY` in your local terminal before launching or restoring the sandbox. `cws-agent` passes this variable into the sandbox. API-key authentication doesn't require browser sign-in. See [Claude Code authentication](https://code.claude.com/docs/en/authentication).

Launch Claude Code and connect your local terminal:

```bash theme={"system"}
cws-agent launch [SANDBOX-NAME] --repo-url [REPOSITORY-URL] --lifetime 8h --permission-mode native
```

Claude Code opens in the sandbox's project directory. Follow any workspace trust prompts. For API-key authentication, approve the key when prompted. If you need account authentication, exit Claude and run `cws-agent login [SANDBOX-NAME]`, then complete `/login` there.

The `--permission-mode native` option uses Claude's own approval settings. Without it, `cws-agent` defaults to bypassing those approval prompts. See [permission modes](https://github.com/coreweave/cws-agent/blob/main/docs/permissions.md).

If Claude reports `Not logged in` despite a configured API key and never offers to approve it, exit with `/exit`, then reconnect with onboarding enabled:

```bash theme={"system"}
cws-agent connect [SANDBOX-NAME] --cmd 'unset IS_DEMO; exec claude'
```

This command uses Claude's own approval settings. Accept the workspace trust and API-key prompts before continuing.

Continue to [Check the session](#check-the-session) to send a prompt and verify the result.

### Use Remote Control

Create a detached sandbox, then connect your terminal for subscription sign-in:

```bash theme={"system"}
cws-agent launch [SANDBOX-NAME] --repo-url [REPOSITORY-URL] --lifetime 8h --detach
cws-agent connect [SANDBOX-NAME] --cmd 'unset IS_DEMO CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC CLAUDE_CODE_OAUTH_TOKEN ANTHROPIC_API_KEY; exec claude'
```

The connection command clears settings that would prevent subscription sign-in or Remote Control feature checks. It also unsets `IS_DEMO` to enable onboarding. See [Claude Code environment variables](https://code.claude.com/docs/en/env-vars).

Inside Claude, complete `/login` with your Claude subscription account and accept the project trust prompt. Run `/remote-control` and accept its first-use confirmation, then exit Claude with `/exit`. Complete this step interactively to answer the confirmation before you start the detached server.

From your local terminal, start Remote Control with Claude's own approval settings:

```bash theme={"system"}
cws-agent rc [SANDBOX-NAME] --permission-mode native
```

Open the session URL when it appears. A message that a process started isn't sufficient to confirm the connection. Send a prompt from the web, mobile, or desktop client and verify its result as described in [Check the session](#check-the-session).

If no URL appears, inspect the remote log:

```bash theme={"system"}
cws-agent exec [SANDBOX-NAME] 'cat /workspace/home/remote-control.log'
```

Resolve any sign-in or eligibility error before retrying. If the server is waiting for an interactive prompt, restart it in an attached `tmux` session in the same sandbox. The `cws-agent rc` command redirects output to the log, so attaching to its existing session doesn't display the prompts.

From your local terminal, stop the waiting server and open a replacement session:

```bash theme={"system"}
cws-agent exec [SANDBOX-NAME] 'tmux kill-session -t cws-remote-control'
cws-agent connect [SANDBOX-NAME] --cmd 'tmux new-session -s cws-remote-control'
```

Inside `tmux`, start Remote Control so its sessions use the project directory:

```bash theme={"system"}
unset IS_DEMO CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC CLAUDE_CODE_OAUTH_TOKEN ANTHROPIC_API_KEY
cd /workspace/project
claude remote-control --spawn same-dir
```

Answer any prompts and open the displayed Claude Code URL. After the connection works, detach with **Ctrl-b**, then **d**, to leave the server running. The replacement session displays output in `tmux` instead of updating the log. To return, run `cws-agent connect [SANDBOX-NAME] --cmd 'tmux attach -t cws-remote-control'`.

## Set up with the Sandboxes SDK

Use this alternative to create a sandbox for either interface with the Sandboxes SDK. It doesn't depend on `cws-agent` or configure snapshots.

Run Python snippets in the virtual environment created in this guide. Save TypeScript snippets as `.mts` files in the project where you install the client, then run them with `npx tsx [FILENAME].mts`.

### Create the sandbox

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

Save the script for your language using the filename shown. It installs Claude Code and `tmux`, then clones the repository you pass on the command line.

Both scripts require the container to run as root to install packages with `apt-get` and use `/root/.local/bin/claude`. Your runner's policy must allow that user.

> [tab] Python
>
> ```python title="create_claude_sandbox.py" theme={"system"}
> from sandbox_auth import AUTH
> import sys
>
> from cwsandbox import Sandbox
>
> bootstrap = """
> set -o pipefail
> apt-get update -qq
> DEBIAN_FRONTEND=noninteractive apt-get install -y -qq tmux >/dev/null
> curl -fsSL https://claude.ai/install.sh | bash
> mkdir -p /workspace
> """
>
> sandbox = Sandbox.run(
>     container_image="node:22-bookworm",
>     resources={"cpu": "2", "memory": "4Gi"},
>     max_lifetime_seconds=8 * 3600,
>     tags=["claude-code"],
>     auth=AUTH,
> )
> try:
>     sandbox.wait()
>     commands = [
>         ["bash", "-ec", bootstrap],
>         ["git", "clone", "--", sys.argv[1], "/workspace/project"],
>     ]
>     for command in commands:
>         result = sandbox.exec(command, timeout_seconds=900).result()
>         if result.returncode != 0:
>             raise RuntimeError(result.stderr or result.stdout)
> except BaseException:
>     sandbox.stop().result()
>     raise
>
> print(f"Sandbox ID: {sandbox.sandbox_id}")
> ```

> [tab] TypeScript
>
> ```typescript title="create_claude_sandbox.mts" theme={"system"}
> import { client } from "./sandbox-client.mts";
>
> const repository = process.argv[2];
> if (!repository) throw new Error("Pass a repository URL.");
>
> const bootstrap = `
> set -o pipefail
> apt-get update -qq
> DEBIAN_FRONTEND=noninteractive apt-get install -y -qq tmux >/dev/null
> curl -fsSL https://claude.ai/install.sh | bash
> mkdir -p /workspace
> `;
>
> const sandbox = await client.create({
>   containerImage: "node:22-bookworm",
>   resources: { cpu: "2", memory: "4Gi" },
>   maxLifetimeSeconds: 8 * 3600,
>   waitUntilRunning: false,
>   tags: ["claude-code"],
> });
> try {
>   await sandbox.wait();
>   const commands = [
>     ["bash", "-ec", bootstrap],
>     ["git", "clone", "--", repository, "/workspace/project"],
>   ];
>   for (const command of commands) {
>     await sandbox.commands.run(command, { timeoutMs: 900_000, check: true });
>   }
> } catch (error) {
>   await sandbox.stop();
>   throw error;
> }
> console.log(`Sandbox ID: ${sandbox.sandboxId}`);
> ```

Replace `[REPOSITORY-URL]` with your public repository URL:

> [tab] Python
>
> ```bash theme={"system"}
> python create_claude_sandbox.py [REPOSITORY-URL]
> ```

> [tab] TypeScript
>
> ```bash theme={"system"}
> npx tsx create_claude_sandbox.mts [REPOSITORY-URL]
> ```

Keep the printed sandbox ID. These standalone examples leave the sandbox running after the script exits. The sandbox runs until you stop it or its 8-hour lifetime expires. In Python, wrapping the sandbox in a `Session` or context manager changes that cleanup behavior.

### Attach your terminal

Use the SDK to attach your local terminal with the same sandbox credentials. Save the script for your language as `attach_sandbox.py` or `attach_sandbox.mts`. The Python script runs on macOS or Linux. The script forwards keystrokes to a sandbox shell and restores your terminal when the shell exits.

> [tab] Python
>
> ```python title="attach_sandbox.py" theme={"system"}
> import os
> import shutil
> import sys
> import termios
> import threading
> import tty
>
> from cwsandbox import Sandbox
> from sandbox_auth import AUTH
>
> if not sys.stdin.isatty() or not sys.stdout.isatty():
>     raise SystemExit("Run this script in an interactive terminal.")
>
> sandbox = Sandbox.from_id(sys.argv[1], auth=AUTH).result()
> size = shutil.get_terminal_size()
> terminal = sandbox.shell(["/bin/bash"], width=size.columns, height=size.lines)
> fd = sys.stdin.fileno()
> saved = termios.tcgetattr(fd)
>
> def forward_input():
>     while data := os.read(fd, 1024):
>         terminal.stdin.write(data).result()
>     terminal.stdin.close().result()
>
> try:
>     tty.setraw(fd)
>     threading.Thread(target=forward_input, daemon=True).start()
>     for chunk in terminal.output:
>         sys.stdout.buffer.write(chunk)
>         sys.stdout.buffer.flush()
>     result = terminal.result()
> finally:
>     termios.tcsetattr(fd, termios.TCSADRAIN, saved)
>     terminal.stdin.close().result()
>
> raise SystemExit(result.returncode)
> ```

> [tab] TypeScript
>
> ```typescript title="attach_sandbox.mts" theme={"system"}
> import { client } from "./sandbox-client.mts";
>
> if (!process.stdin.isTTY || !process.stdout.isTTY) {
>   throw new Error("Run this script in an interactive terminal.");
> }
> const sandboxId = process.argv[2];
> if (!sandboxId) throw new Error("Pass a sandbox ID.");
>
> const sandbox = await client.fromId(sandboxId);
> const terminal = await sandbox.shell({
>   command: ["/bin/bash"],
>   cols: process.stdout.columns || 80,
>   rows: process.stdout.rows || 24,
> });
> const wasRaw = process.stdin.isRaw;
> const forwardInput = (chunk: Buffer) => {
>   void terminal.stdin.write(chunk).catch((error) => {
>     console.error(error);
>     void terminal.cancel();
>   });
> };
>
> try {
>   process.stdin.setRawMode(true);
>   process.stdin.on("data", forwardInput);
>   process.stdin.resume();
>   for await (const chunk of terminal.output) {
>     process.stdout.write(chunk);
>   }
>   const result = await terminal.wait();
>   process.exitCode = result.exitCode;
> } finally {
>   process.stdin.off("data", forwardInput);
>   process.stdin.setRawMode(wasRaw);
>   process.stdin.pause();
>   await terminal.stdin.close();
> }
> ```

Replace `[SANDBOX-ID]` with the printed ID, then run:

> [tab] Python
>
> ```bash theme={"system"}
> python attach_sandbox.py [SANDBOX-ID]
> ```

> [tab] TypeScript
>
> ```bash theme={"system"}
> npx tsx attach_sandbox.mts [SANDBOX-ID]
> ```

With the Python client and a CoreWeave API access token, `cwsandbox --auth coreweave_api_key sh [SANDBOX-ID]` is an optional shortcut. Install the `cli` extra and keep `CWSANDBOX_API_KEY` set to the CoreWeave API access token used for that sandbox.

Your terminal is now attached to a shell inside the sandbox. Choose one of the following interfaces to start Claude Code.

### Start the terminal interface

For API-key authentication, enter the key in the sandbox's Bash shell before starting Claude. The input is hidden and isn't included in the command history:

```bash theme={"system"}
read -r -s -p 'Anthropic API key: ' ANTHROPIC_API_KEY
export ANTHROPIC_API_KEY
printf '\n'
```

Inside the sandbox, start Claude from the cloned repository:

```bash theme={"system"}
cd /workspace/project
/root/.local/bin/claude
```

If you use an API key, approve it. Otherwise, complete account sign-in. Then accept the workspace trust prompts and continue to [Check the session](#check-the-session).

### Start Remote Control

Use Claude subscription sign-in for this interface. If you previously used an API key in this sandbox, remove it from the shell and any Claude settings before signing in:

```bash theme={"system"}
unset ANTHROPIC_API_KEY CLAUDE_CODE_OAUTH_TOKEN
```

Inside the sandbox, open a named `tmux` session in your project:

```bash theme={"system"}
cd /workspace/project
tmux new-session -s claude-remote
```

In `tmux`, start Claude:

```bash theme={"system"}
/root/.local/bin/claude
```

Complete subscription sign-in and accept the workspace trust prompt. Exit Claude with `/exit`, then start the Remote Control server in the same directory:

```bash theme={"system"}
/root/.local/bin/claude remote-control --name "CoreWeave sandbox" --spawn same-dir
```

The `--spawn same-dir` option uses the project directory for remote sessions. If prompted, accept the first-use confirmation. Open the displayed Claude Code URL in a browser signed in to the same Claude account.

After the connection works, detach from `tmux` with **Ctrl-b**, then **d**, and exit the sandbox shell. The `tmux` session keeps the server running. To return, rerun the attachment script and run `tmux attach -t claude-remote`.

## Check the session

For the terminal interface, send the prompt in the attached Claude Code TUI. For Remote Control, open the session at claude.ai/code in your browser, or in the Claude mobile or Desktop app, using the same account.

Choose a unique, non-secret test value and replace `[PROOF-VALUE]` in this prompt:

```text theme={"system"}
Write the exact text [PROOF-VALUE] to /workspace/project/sandbox-proof.txt, then read it back.
```

If asked, approve the file write. If you used the terminal interface, exit Claude with `/exit` and, for the SDK setup, exit the sandbox shell with `exit`. From your local terminal, verify the result using the command for your setup:

> [tab] cws-agent
>
> ```bash theme={"system"}
> cws-agent exec [SANDBOX-NAME] 'cat /workspace/project/sandbox-proof.txt'
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
> > result = sandbox.exec(["cat", "/workspace/project/sandbox-proof.txt"], check=True).result()
> > print(result.stdout, end="")
> > ```
>
> > [tab] TypeScript
> >
> > ```typescript theme={"system"}
> > import { client } from "./sandbox-client.mts";
> >
> > const sandbox = await client.fromId("[SANDBOX-ID]");
> > const result = await sandbox.commands.run(["cat", "/workspace/project/sandbox-proof.txt"], { check: true });
> > process.stdout.write(result.stdout);
> > ```

Matching the value confirms that Claude wrote to the sandbox you created.

## Return to a running sandbox

Exiting Claude or closing your terminal leaves the sandbox running. To return from another terminal or machine, install the same client and authenticate with credentials that can access the sandbox.

For `cws-agent`, find the session by name and open a new Claude terminal:

```bash theme={"system"}
cws-agent list
cws-agent status [SANDBOX-NAME]
cws-agent connect [SANDBOX-NAME] --permission-mode native
```

The `connect` command uses the existing sandbox and files. It doesn't resume a previous conversation. To continue a saved conversation, first exit its original Claude process. Then list the history and replace `[CONVERSATION-ID]` with the ID to resume:

```bash theme={"system"}
cws-agent session history [SANDBOX-NAME]
cws-agent session resume [SANDBOX-NAME] [CONVERSATION-ID] --permission-mode native
```

For the SDK path, rerun the [terminal attachment script](#attach-your-terminal) with the same sandbox ID, then start Claude again. A single SDK shell session ends after 24 hours, even when the sandbox's lifetime is longer. The sandbox keeps running, so rerun the script to reconnect. For Remote Control, reopen the session URL while its server is still running.

A sandbox connection and an agent process have separate lifetimes. If a terminal agent must keep working after you disconnect, use `tmux` or the `cws-agent` worktree sessions.

Reconnecting doesn't reset the sandbox's lifetime. If the sandbox has stopped, restore a saved workspace instead.

## Keep results and stop

Save progress during a long session instead of waiting until the lifetime is nearly over. With `cws-agent`, wait for Claude to finish writing and pause other workspace writers, then capture the `/workspace` directory without stopping the sandbox:

```bash theme={"system"}
cws-agent snapshot [SANDBOX-NAME]
```

Wait for the command to report a `READY` snapshot. A snapshot captures files at that point in time. Later edits need another snapshot. For capture behavior and saved credentials, see the [snapshot guidance](https://github.com/coreweave/cws-agent/blob/main/docs/usage.md#snapshots). Don't rely on lifetime expiry to save your latest changes.

In your local terminal, copy the verified text result to your machine:

```bash theme={"system"}
cws-agent exec [SANDBOX-NAME] 'cat /workspace/project/sandbox-proof.txt' > sandbox-proof.txt
```

For code changes, see [Get changes back](https://github.com/coreweave/cws-agent/blob/main/docs/usage.md#get-changes-back). A snapshot preserves the remote workspace. It doesn't copy files to your machine.

When you finish, wait for active tasks and workspace writes to complete, then save the workspace and stop compute:

```bash theme={"system"}
cws-agent down [SANDBOX-NAME]
```

The `down` command confirms a snapshot before stopping. If snapshot creation fails, it leaves the sandbox running. Check `cws-agent status [SANDBOX-NAME]` and resolve the failure before retrying. To stop without saving current changes, use `cws-agent down [SANDBOX-NAME] --no-snapshot`.

For the direct SDK path, this example has no persistent mount. For a restorable workspace, configure [file system snapshots](https://docs.coreweave.com/products/sandboxes/file-system-snapshots.md) at creation. Copy results out with [file operations](https://docs.coreweave.com/products/sandboxes/client/guides/file-operations.md), then stop the sandbox:

> [tab] Python
>
> ```python theme={"system"}
> from sandbox_auth import AUTH
> from cwsandbox import Sandbox
>
> sandbox = Sandbox.from_id("[SANDBOX-ID]", auth=AUTH).result()
> sandbox.stop().result()
> ```

> [tab] TypeScript
>
> ```typescript theme={"system"}
> import { client } from "./sandbox-client.mts";
>
> const sandbox = await client.fromId("[SANDBOX-ID]");
> await sandbox.stop();
> ```

Exiting Claude alone leaves the sandbox running. Stopping the sandbox ends its agent processes, including Remote Control. Restoring files from a snapshot doesn't restore that process. Sign in as needed and start Remote Control again.

To return to a workspace saved by `cws-agent`, restore it into a new sandbox. If the skills/MCP import prompt appears, press **Enter** to skip it:

```bash theme={"system"}
cws-agent restore [SANDBOX-NAME] --lifetime 8h --connect --permission-mode native
```

For Remote Control, exit the restored Claude TUI with `/exit`, then repeat the [sign-in and server startup steps](#use-remote-control), starting with `cws-agent connect`. Skip the launch command because restore has already created the sandbox. For saved conversations and parallel worktrees, see the [`cws-agent` sessions guide](https://github.com/coreweave/cws-agent/blob/main/docs/sessions.md).

## Troubleshoot

Use these checks to resolve common issues:

* If sandbox creation fails, check your selected sandbox credential and authentication settings.
* If installation, cloning, or model requests fail, check outbound connectivity and the relevant provider credentials. For [CoreWeave Kubernetes Service (CKS) placement](https://docs.coreweave.com/products/sandboxes/get-started-cks.md), your runner's policy must permit those destinations.
* If the terminal disconnects, attach again while the sandbox is running. To retain a process across terminal disconnects, run it in a terminal multiplexer such as `tmux`.
* If Remote Control rejects authentication, sign in with a Claude subscription. Remove conflicting API-key credentials from the remote environment or Claude settings.
* If Remote Control is unavailable, review [Anthropic's troubleshooting guidance](https://code.claude.com/docs/en/remote-control#troubleshooting) for organization settings, custom API endpoints, and environment variables that disable required feature checks.
* If the sandbox expires, create a new one. The lifetime can't be extended after creation, and this SDK example doesn't save its filesystem automatically.

## Data handling

Commands execute in the sandbox, while model requests go to your configured provider. Remote Control sends prompts, tool activity, and conversation content to Anthropic and stores a transcript to synchronize connected devices. See [Remote Control security](https://code.claude.com/docs/en/remote-control#connection-and-security) and [Claude Code data usage](https://code.claude.com/docs/en/data-usage).

## Next steps

For more information, see these guides:

* [Interactive shells and TTY](https://docs.coreweave.com/products/sandboxes/client/guides/interactive-shells.md) covers terminal access from the SDK.
* [Sandbox lifecycle](https://docs.coreweave.com/products/sandboxes/client/guides/sandbox-lifecycle.md) covers waiting, reconnecting, and stopping.
* [Claude Code documentation](https://code.claude.com/docs/en/overview) covers agent configuration and authentication.

To provision a worker sandbox for each new cloud session you start at claude.ai/code, see [Claude Code cloud sessions](https://docs.coreweave.com/products/sandboxes/agents/claude-code-cloud.md).
