# Run Pi in a sandbox

Source: https://docs.coreweave.com/products/sandboxes/agents/pi

# Run Pi in a sandbox

> Run Pi from an attached terminal with optional Serverless Inference, then retrieve your work.

Run [Pi](https://github.com/earendil-works/pi) inside a CoreWeave sandbox to work on a repository from your terminal. Pi's agent process, files, and shell commands run in the sandbox. Model requests go to your chosen provider. This guide covers creating the workspace, connecting to Pi, checking its work, and stopping compute.

## Prerequisites

Before you begin, you need the following:

* A macOS or Linux terminal with either Python 3.12 or later and [`uv`](https://docs.astral.sh/uv/getting-started/installation/), or Node.js 22 or later.
* A [Forge API key or CoreWeave API access token](https://docs.coreweave.com/products/sandboxes/placement.md#choose-and-get-credentials).
* Credentials for a [Pi-supported model provider](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/providers.md). This guide uses Serverless Inference, which requires [inference credits](https://docs.coreweave.com/products/inference/serverless/api-reference.md#prerequisites).
* A public Git repository URL. Private repositories require separate Git authentication inside the sandbox.

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

## Prepare your local environment

Create a local project and install the Sandboxes software development kit (SDK):

> [tab] Python
>
> ```bash theme={"system"}
> uv init --bare pi-sandbox
> cd pi-sandbox
> uv venv --python 3.12
> source .venv/bin/activate
> uv pip install 'cwsandbox[wandb]==1.14.2'
> ```

> [tab] TypeScript
>
> ```bash theme={"system"}
> mkdir pi-sandbox
> cd pi-sandbox
> npm install @coreweave/cwsandbox@1.0.0 tsx
> ```

The SDK uses your selected local credential to manage the sandbox. The creation script doesn't copy it into the sandbox. You configure model authentication separately.

## Create the sandbox

Save the script for your language as `create_pi_sandbox.py` or `create_pi_sandbox.mts`. It creates a CPU sandbox, installs Pi `0.87.1`, and clones the repository. The Node.js image supplies the runtime and Git. If setup fails, the script stops the sandbox before reporting the error.

> [tab] Python
>
> ```python title="create_pi_sandbox.py" theme={"system"}
> import sys
>
> from cwsandbox import Sandbox
> from sandbox_auth import AUTH
>
> if len(sys.argv) != 2:
>     raise SystemExit("Pass a repository URL.")
>
> sandbox = Sandbox.run(
>     placement_mode="serverless",
>     container_image="node:22-bookworm",
>     resources={"cpu": "2", "memory": "4Gi"},
>     max_lifetime_seconds=4 * 3600,
>     tags=["pi-cli"],
>     auth=AUTH,
> )
> print(f"Sandbox ID: {sandbox.sandbox_id}", flush=True)
> try:
>     sandbox.wait()
>     commands = [
>         ["npm", "install", "--global", "--ignore-scripts", "@earendil-works/pi-coding-agent@0.87.1"],
>         ["mkdir", "-p", "/workspace"],
>         ["git", "clone", "--", sys.argv[1], "/workspace/project"],
>         ["pi", "--version"],
>     ]
>     for command in commands:
>         result = sandbox.exec(command, timeout_seconds=900, check=True).result()
>         print(result.stdout, end="")
> except BaseException:
>     sandbox.stop().result()
>     raise
> ```

> [tab] TypeScript
>
> ```typescript title="create_pi_sandbox.mts" theme={"system"}
> import { client } from "./sandbox-client.mts";
>
> const repository = process.argv[2];
> if (!repository) throw new Error("Pass a repository URL.");
>
> const sandbox = await client.create({
>   containerImage: "node:22-bookworm",
>   resources: { cpu: "2", memory: "4Gi" },
>   maxLifetimeSeconds: 4 * 3600,
>   waitUntilRunning: false,
>   tags: ["pi-cli"],
> });
> console.log(`Sandbox ID: ${sandbox.sandboxId}`);
> try {
>   await sandbox.wait();
>   const commands = [
>     ["npm", "install", "--global", "--ignore-scripts", "@earendil-works/pi-coding-agent@0.87.1"],
>     ["mkdir", "-p", "/workspace"],
>     ["git", "clone", "--", repository, "/workspace/project"],
>     ["pi", "--version"],
>   ];
>   for (const command of commands) {
>     const result = await sandbox.commands.run(command, { timeoutMs: 900_000, check: true });
>     process.stdout.write(result.stdout);
>   }
> } catch (error) {
>   await sandbox.stop();
>   throw error;
> }
> ```

Replace `[REPOSITORY-URL]` with your repository URL, then run:

> [tab] Python
>
> ```bash theme={"system"}
> python create_pi_sandbox.py [REPOSITORY-URL]
> ```

> [tab] TypeScript
>
> ```bash theme={"system"}
> npx tsx create_pi_sandbox.mts [REPOSITORY-URL]
> ```

Keep the printed sandbox ID. Successful setup prints Pi's version, `0.87.1`. The sandbox remains running after the script exits, until you stop it or its 4-hour lifetime expires. The lifetime includes startup time.

## Attach your terminal

Save the script for your language as `attach_sandbox.py` or `attach_sandbox.mts`. It forwards your terminal input to a Bash shell in the sandbox and restores your local terminal settings when the shell exits.

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

Replace `[SANDBOX-ID]` with your sandbox ID:

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

At the sandbox's Bash prompt, enter the cloned repository:

```bash theme={"system"}
cd /workspace/project
```

Inside this shell, run the provider setup and Pi commands in the following sections.

## Choose a model provider

Choose one of the following options. Sandbox authentication and model authentication use separate credentials in this guide. Pi can access credentials provided to its process and can send workspace content to the selected model provider.

### Use Serverless Inference

We recommend [Serverless Inference](https://docs.coreweave.com/products/inference/serverless.md) for this walkthrough. The example uses `zai-org/GLM-5.2`. Choose another model from the [model catalog](https://docs.coreweave.com/products/inference/serverless/models.md) if it better fits your task.

In the sandbox shell, enter a Forge API key for an account with inference credits at the hidden prompt:

```bash theme={"system"}
read -r -s -p 'Forge inference API key: ' WANDB_API_KEY
export WANDB_API_KEY
printf '\n'
```

In the sandbox shell, configure Pi's OpenAI-compatible provider. The following commands create the `~/.pi/agent/models.json` file. The quoted heredoc preserves the environment-variable reference so the file doesn't contain the key:

```bash theme={"system"}
mkdir -p ~/.pi/agent
cat > ~/.pi/agent/models.json <<'JSON'
{
  "providers": {
    "forge": {
      "baseUrl": "https://api.inference.wandb.ai/v1",
      "api": "openai-completions",
      "apiKey": "${WANDB_API_KEY}",
      "models": [
        {
          "id": "zai-org/GLM-5.2",
          "name": "GLM 5.2 (Forge)",
          "reasoning": true,
          "input": ["text"],
          "contextWindow": 1048576,
          "maxTokens": 8192
        }
      ]
    }
  }
}
JSON
pi --provider forge --model zai-org/GLM-5.2
```

Pi opens its terminal interface with `/workspace/project` and `zai-org/GLM-5.2` in the status area. Submit a task in [Run Pi and check its work](#run-pi-and-check-its-work) to verify model access.

The configuration limits each response to 8,192 tokens. If you change models, update the model ID and capabilities to match the provider. For more configuration options, see [Pi model configuration](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/models.md).

### Use another provider

To use Anthropic or OpenAI directly, choose the corresponding API key and start Pi in the same sandbox shell:

> [tab] Anthropic
>
> ```bash theme={"system"}
> read -r -s -p 'Anthropic API key: ' ANTHROPIC_API_KEY
> export ANTHROPIC_API_KEY
> printf '\n'
> pi --provider anthropic
> ```

> [tab] OpenAI
>
> ```bash theme={"system"}
> read -r -s -p 'OpenAI API key: ' OPENAI_API_KEY
> export OPENAI_API_KEY
> printf '\n'
> pi --provider openai
> ```

Use `/model` inside Pi to choose a model available to your provider. The Pi provider documentation linked in the prerequisites covers other providers and account sign-in options.

## Run Pi and check its work

If Pi displays a project trust prompt, follow it. To check that Pi can create and read a file in the cloned repository, submit this task in Pi:

```text theme={"system"}
Create sandbox-proof.txt in the current directory containing exactly "Hello from CoreWeave", then read it back.
```

Pi can read, write, and edit files and run shell commands. Its tools operate with the permissions of the sandbox process. Review the repository and any Pi extensions you load. See [Pi security](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/security.md).

After Pi finishes, enter `/quit` to return to the sandbox shell. Pi prints a `To resume this session:` line with a `pi --session` command. Keep that command to reopen this conversation.

Verify the file independently:

```bash theme={"system"}
cat /workspace/project/sandbox-proof.txt
```

The output should contain `Hello from CoreWeave`.

For an unattended task with the Forge setup, run Pi in print mode from the same shell:

```bash theme={"system"}
pi --provider forge --model zai-org/GLM-5.2 --print 'Read sandbox-proof.txt and report its contents.'
```

Print mode processes the prompt, prints Pi's response, and exits. For another provider, replace the provider and model arguments with your selection.

## Reconnect to a conversation

To reconnect while the sandbox is running, run the attach script again. Re-enter any API keys supplied through the previous shell and return to the `/workspace/project` directory before starting Pi. To reopen your interactive conversation, replace `[SESSION-ID]` with the ID from the `To resume this session:` line Pi printed when you exited:

```bash theme={"system"}
pi --session [SESSION-ID]
```

Alternatively, `pi --continue` resumes the most recent session for the project. If you ran the print-mode example after your interactive conversation, it resumes the print-mode session. Use `--session` to return to a specific conversation.

## Retrieve the result and stop

Enter `exit` to leave the sandbox shell. In your local terminal, save the script for your language as `collect_pi_result.py` or `collect_pi_result.mts`:

> [tab] Python
>
> ```python title="collect_pi_result.py" theme={"system"}
> import sys
> from pathlib import Path
>
> from cwsandbox import Sandbox
> from sandbox_auth import AUTH
>
> if len(sys.argv) != 2:
>     raise SystemExit("Pass a sandbox ID.")
>
> sandbox = Sandbox.from_id(sys.argv[1], auth=AUTH).result()
> content = sandbox.read_file("/workspace/project/sandbox-proof.txt").result()
> Path("sandbox-proof.txt").write_bytes(content)
> print(content.decode(), end="")
> sandbox.stop().result()
> ```

> [tab] TypeScript
>
> ```typescript title="collect_pi_result.mts" theme={"system"}
> import { writeFile } from "node:fs/promises";
>
> import { client } from "./sandbox-client.mts";
>
> const sandboxId = process.argv[2];
> if (!sandboxId) throw new Error("Pass a sandbox ID.");
>
> const sandbox = await client.fromId(sandboxId);
> const content = await sandbox.files.read("/workspace/project/sandbox-proof.txt");
> await writeFile("sandbox-proof.txt", content);
> process.stdout.write(new TextDecoder().decode(content));
> await sandbox.stop();
> ```

To save the file locally and stop compute, replace `[SANDBOX-ID]` with your sandbox ID and run the script:

> [tab] Python
>
> ```bash theme={"system"}
> python collect_pi_result.py [SANDBOX-ID]
> ```

> [tab] TypeScript
>
> ```bash theme={"system"}
> npx tsx collect_pi_result.mts [SANDBOX-ID]
> ```

This script stops the sandbox only after it retrieves the file. If retrieval fails, fix the error and retry. To stop the sandbox separately when you no longer need its files, save the script for your language as `stop_pi_sandbox.py` or `stop_pi_sandbox.mts`:

> [tab] Python
>
> ```python title="stop_pi_sandbox.py" theme={"system"}
> import sys
>
> from cwsandbox import Sandbox
> from sandbox_auth import AUTH
>
> if len(sys.argv) != 2:
>     raise SystemExit("Pass a sandbox ID.")
>
> sandbox = Sandbox.from_id(sys.argv[1], auth=AUTH).result()
> sandbox.stop().result()
> ```

> [tab] TypeScript
>
> ```typescript title="stop_pi_sandbox.mts" theme={"system"}
> import { client } from "./sandbox-client.mts";
>
> const sandboxId = process.argv[2];
> if (!sandboxId) throw new Error("Pass a sandbox ID.");
>
> const sandbox = await client.fromId(sandboxId);
> await sandbox.stop();
> ```

Run the script with your sandbox ID:

> [tab] Python
>
> ```bash theme={"system"}
> python stop_pi_sandbox.py [SANDBOX-ID]
> ```

> [tab] TypeScript
>
> ```bash theme={"system"}
> npx tsx stop_pi_sandbox.mts [SANDBOX-ID]
> ```

Exiting Pi or the shell doesn't stop the sandbox. This example has no persistent mount. Retrieve any files you need before stopping or expiry. For a workspace you can restore into a new sandbox, configure [file system snapshots](https://docs.coreweave.com/products/sandboxes/file-system-snapshots.md) at creation.

## Troubleshoot

Use these checks to resolve common issues:

* If sandbox creation fails, check your sandbox credential and the sandbox authentication requirements linked in the prerequisites.
* If Pi can't authenticate, check that the model credential is exported in the shell that starts Pi. With Forge, also check inference credits and the model ID.
* If Pi can't reach its provider, check outbound access to the provider endpoint. Installation and cloning also require access to npm and your Git host.
* If your connection drops, attach again while the sandbox runs. If you need a process to survive terminal disconnections, use a terminal multiplexer such as `tmux`.

## Next steps

For more information, see the following resources:

* [Interactive shells](https://docs.coreweave.com/products/sandboxes/client/guides/interactive-shells.md) covers terminal access through the SDK.
* [File operations](https://docs.coreweave.com/products/sandboxes/client/guides/file-operations.md) covers uploading and retrieving workspace files.
* [Pi documentation](https://github.com/earendil-works/pi/tree/main/packages/coding-agent/docs) covers sessions, model selection, and extensions.
