# Run Codex in a sandbox

Source: https://docs.coreweave.com/products/sandboxes/agents/codex

# Run Codex in a sandbox

> Run Codex CLI in a sandbox, connect a local CLI, or use desktop and mobile apps with a remote project.

Run Codex against a repository in a CoreWeave sandbox. You can run the Codex
command-line interface (CLI) inside the sandbox, connect your local CLI to Codex
app server, or use the desktop and mobile apps with a remote project. In all three
options, the agent process, workspace, and command execution stay in the sandbox.
These examples use OpenAI for model requests.

## Choose how to run Codex in a sandbox

The app server is the agent backend for the remote CLI and desktop
connections. Choose where you want to interact with the agent:

| Interface | Where the interface runs | Where the agent process runs | Connection |
| - | - | - | - |
| [Run Codex CLI in a sandbox](#run-codex-cli-in-a-sandbox) | In the sandbox, displayed through your terminal | In the sandbox | Attach with `cws-agent` |
| [Connect your local CLI to Codex app server](#connect-your-local-cli-to-codex-app-server) | On your computer | In the sandbox, through Codex app server | Connect with `codex --remote` |
| [Use the desktop and mobile apps](#use-the-desktop-and-mobile-apps) | On your computer, or on a phone paired with that computer | In the sandbox, through Codex app server | Add a Secure Shell (SSH) project in the desktop app. Pair your phone through Remote. |

The attached CLI uses `cws-agent` to create a sandbox. The local CLI and desktop
app share the [SSH sandbox setup](#create-an-ssh-accessible-sandbox).

For mobile access, pair your phone with the desktop host through Remote. The
phone connects to that host, which connects to the sandbox over SSH. Keep the
desktop host awake, online, and running the app. See
[Mobile and another desktop through Remote](#mobile-and-another-desktop-through-remote).

The local terminal user interface (TUI) sends input, presents output, and handles
approvals. The app server owns the remote agent session. It doesn't forward
individual commands from an agent running on your laptop. See the
[OpenAI app server guide](https://learn.chatgpt.com/docs/app-server).

Starting the app server doesn't register its sessions with the desktop or mobile app.
Those interfaces use the separate connection setup described in
[Use the desktop and mobile apps](#use-the-desktop-and-mobile-apps). OpenAI's
Remote documentation doesn't establish a website attachment flow for this
self-hosted session. Browser access is outside the scope of this guide.

The programmatic Agents API workflow uses a separate execution model. See the
[OpenAI Agents API recipe](https://github.com/coreweave/cwsandbox-recipes/tree/main/recipes/openai-agents-api).

## Prerequisites

Before you begin, make sure you have the following:

* A [Forge API key or CoreWeave API access token](https://docs.coreweave.com/products/sandboxes/placement.md#choose-and-get-credentials). You also need capacity for a CPU sandbox.
* An OpenAI account supported by Codex, or an OpenAI API key. The app server
  example in this guide uses API-key authentication and API billing.
* A public repository URL. Private clones require Git credentials in the sandbox.
* Outbound connectivity to OpenAI, package registries, and your Git host

The sandbox creation examples set an 8-hour maximum wall-clock lifetime, not an
inactivity timer. Stop the sandbox when you finish. Model usage
and sandbox compute can incur separate charges.

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
> ```python title="sandbox_auth.py" theme={"system"}
> from cwsandbox import AuthStrategy
>
> AUTH = AuthStrategy.WANDB
> ```

> [tab] CoreWeave API access token
>
> Replace `[API-ACCESS-TOKEN]` with your CoreWeave API access token and export it in your local terminal:
>
> ```bash theme={"system"}
> export CWSANDBOX_API_KEY="[API-ACCESS-TOKEN]"
> ```
>
> ```python title="sandbox_auth.py" theme={"system"}
> from cwsandbox import AuthStrategy
>
> AUTH = AuthStrategy.COREWEAVE_API_KEY
> ```

## Run Codex CLI in a sandbox

Use `cws-agent` to launch a sandbox and attach your terminal. Both the Codex TUI
and agent process run inside the sandbox.

1. Follow the [`cws-agent` installation instructions](https://github.com/coreweave/cws-agent#install).
   For API-key authentication, export `OPENAI_API_KEY` locally before launch.
   The tool passes it to the sandbox and stores it through Codex's login command.

2. Replace `[SANDBOX-NAME]` with a name that contains 1 to 40 lowercase letters,
   digits, or hyphens and starts with a letter or digit. Replace `[REPOSITORY-URL]`
   with your public repository URL:

   ```bash theme={"system"}
   cws-agent launch [SANDBOX-NAME] --agent codex --repo-url [REPOSITORY-URL] --lifetime 8h --permission-mode native
   ```

   If a skills or Model Context Protocol (MCP) import prompt appears, press
   **Enter** to skip it for this example. Codex opens in the sandbox's project directory. Follow its workspace
   trust and authentication prompts.

   `--permission-mode native` retains Codex's own permission settings. The wrapper
   otherwise defaults to bypassing approval prompts. See
   [`cws-agent` permission modes](https://github.com/coreweave/cws-agent/blob/main/docs/permissions.md).

3. If you need account sign-in, exit the TUI, then authenticate in the sandbox:

   ```bash theme={"system"}
   cws-agent login [SANDBOX-NAME]
   cws-agent connect [SANDBOX-NAME] --permission-mode native
   ```

   Follow the login flow that Codex shows. For headless device sign-in and workspace
   restrictions, see [Codex authentication](https://learn.chatgpt.com/docs/auth).

4. Complete [Check the session](#check-the-session). To reconnect later while the
   sandbox runs, use the same `connect` command. To resume a saved Codex
   conversation, see [`cws-agent` sessions](https://github.com/coreweave/cws-agent/blob/main/docs/sessions.md).

## Create an SSH-accessible sandbox

Complete this setup for either the local CLI or the desktop app. It uses the
Sandboxes software development kit (SDK) to create a sandbox with Codex installed
and authenticated for a non-root SSH user. It doesn't require `cws-agent`.

The setup uses a [Transport Layer Security (TLS) passthrough endpoint](https://docs.coreweave.com/products/sandboxes/public-endpoints.md)
and `stunnel` to carry SSH through the endpoint. A generated Python
`ProxyCommand` verifies the TLS certificate, then SSH
authenticates your key and verifies the host key. The app server has no public
listener. This follows OpenAI's [network exposure guidance](https://learn.chatgpt.com/docs/remote-connections#authentication-and-network-exposure).

### Prepare the SSH client

Use a macOS or Linux computer with Python 3.12+, `uv`, and OpenSSH.
For desktop access, use a supported app and operating system from OpenAI's
[SSH-host instructions](https://learn.chatgpt.com/docs/remote-connections#connect-to-an-ssh-host).
This setup uses the sandbox credential from [Prerequisites](#prerequisites) and an
OpenAI API key with API billing.

Replace `[OPENAI-API-KEY]` with your OpenAI API key:

```bash theme={"system"}
uv venv --python 3.12
source .venv/bin/activate
uv pip install 'cwsandbox[wandb]==1.14.2'
export OPENAI_API_KEY="[OPENAI-API-KEY]"
```

The generated SSH configuration uses the absolute path of this Python interpreter
to run the TLS forwarder. Keep the Python installation and output directory
available while you use the sandbox. Because of this forwarder, the setup uses the
Python client only.

Create a dedicated SSH key, then load it into your running SSH agent. Choose an
unused filename and enter a passphrase when prompted:

```bash theme={"system"}
ssh-keygen -t ed25519 -f ~/.ssh/cw-codex
ssh-add ~/.ssh/cw-codex
```

The private key stays on your computer. The setup script copies only the public
key into the sandbox.

### Create the SSH sandbox

Save the following in the `create_codex_ssh.py` file. It creates an 8-hour sandbox, installs
Codex `0.154.0`, and configures a non-root `agent` account with public-key SSH
authentication. It passes the OpenAI key to `codex login` through standard input (stdin).
It doesn't store the key in the sandbox's creation configuration. Codex saves its login
inside the sandbox.

The script also creates a 1-day TLS certificate and retrieves the public
certificate and SSH host key through the authenticated Sandboxes SDK. The generated
client configuration verifies both. Keep the output directory to reconnect.

> [accordion] Sandbox setup script
>
> ```python title="create_codex_ssh.py" theme={"system"}
> from sandbox_auth import AUTH
> import os
> from pathlib import Path
> import shlex
> import sys
>
> from cwsandbox import Endpoint, Sandbox, Service
>
> if len(sys.argv) != 4:
>     raise SystemExit(
>         "Usage: python create_codex_ssh.py REPOSITORY_URL SSH_KEY OUTPUT_DIR"
>     )
> repository, identity_arg, directory_arg = sys.argv[1:]
> identity = Path(identity_arg).expanduser().resolve()
> if not identity.is_file():
>     raise SystemExit("SSH private key not found. Generate the key pair first.")
> public_key = Path(str(identity) + ".pub").read_bytes()
> api_key = os.environ["OPENAI_API_KEY"]
> if not api_key:
>     raise SystemExit("Set OPENAI_API_KEY first.")
> directory = Path(directory_arg).expanduser().resolve()
> directory.mkdir(mode=0o700, parents=True, exist_ok=False)
> sandbox = Sandbox.run(
>     container_image="node:22-bookworm",
>     resources={"cpu": "2", "memory": "4Gi"},
>     max_lifetime_seconds=8 * 3600,
>     services=[
>         Service(
>             port=8443,
>             name="ssh",
>             visibility="public",
>             endpoint=Endpoint(kind="tls_passthrough"),
>         )
>     ],
>     auth=AUTH,
> )
>
> def run(command):
>     result = sandbox.exec(command, timeout_seconds=900).result()
>     if result.returncode != 0:
>         details = (result.stdout + result.stderr).replace(api_key, "[REDACTED]")
>         raise RuntimeError(details[-3000:])
>     return result.stdout
>
> try:
>     (directory / "sandbox-id").write_text(sandbox.sandbox_id + "\n")
>     print("Sandbox created; ID saved in", directory / "sandbox-id", flush=True)
>     sandbox.wait()
>     address = next(
>         item.address for item in sandbox.service_addresses if item.port == 8443
>     )
>     host, port = address.rsplit(":", 1)
>     run(
>         [
>             "bash",
>             "-c",
>             """
> set -eu
> apt-get update -qq
> DEBIAN_FRONTEND=noninteractive apt-get install -y -qq openssh-server stunnel4 bubblewrap
> npm install --global @openai/codex@0.154.0
> useradd --create-home --shell /bin/bash agent
> usermod --password '*' agent
> install -d -m 700 -o agent -g agent /home/agent/.ssh
> install -d -m 755 /run/sshd /workspace
> mkdir -p /etc/codex-ssh
> chmod 700 /etc/codex-ssh
> """,
>         ]
>     )
>     sandbox.write_file("/home/agent/.ssh/authorized_keys", public_key).result()
>     run(
>         [
>             "bash",
>             "-c",
>             "chmod 600 /home/agent/.ssh/authorized_keys; chown agent:agent /home/agent/.ssh/authorized_keys",
>         ]
>     )
>     run(["git", "clone", "--", repository, "/workspace/project"])
>     run(["chown", "-R", "agent:agent", "/workspace/project"])
>     login = sandbox.exec(
>         ["runuser", "-u", "agent", "--", "codex", "login", "--with-api-key"],
>         stdin=True,
>         timeout_seconds=60,
>     )
>     login.stdin.write((api_key + "\n").encode()).result()
>     login.stdin.close().result()
>     if login.result().returncode != 0:
>         raise RuntimeError("Codex authentication failed.")
>     run(
>         [
>             "openssl",
>             "req",
>             "-x509",
>             "-newkey",
>             "rsa:2048",
>             "-noenc",
>             "-keyout",
>             "/etc/codex-ssh/tls.key",
>             "-out",
>             "/etc/codex-ssh/tls.crt",
>             "-days",
>             "1",
>             "-subj",
>             "/CN=codex-sandbox",
>             "-addext",
>             f"subjectAltName=DNS:{host}",
>         ]
>     )
>     sandbox.write_file(
>         "/etc/codex-ssh/sshd_config",
>         b"""Port 2222
> ListenAddress 127.0.0.1
> HostKey /etc/ssh/ssh_host_ed25519_key
> AuthorizedKeysFile .ssh/authorized_keys
> PubkeyAuthentication yes
> PasswordAuthentication no
> KbdInteractiveAuthentication no
> PermitRootLogin no
> AllowUsers agent
> AllowTcpForwarding local
> X11Forwarding no
> Subsystem sftp internal-sftp
> """,
>     ).result()
>     sandbox.write_file(
>         "/etc/codex-ssh/stunnel.conf",
>         b"""pid = /run/codex-stunnel.pid
> output = /var/log/codex-stunnel.log
> [ssh]
> accept = 0.0.0.0:8443
> connect = 127.0.0.1:2222
> cert = /etc/codex-ssh/tls.crt
> key = /etc/codex-ssh/tls.key
> """,
>     ).result()
>     run(["chmod", "600", "/etc/codex-ssh/tls.key"])
>     run(
>         [
>             "/usr/sbin/sshd",
>             "-f",
>             "/etc/codex-ssh/sshd_config",
>             "-E",
>             "/var/log/codex-sshd.log",
>         ]
>     )
>     run(["stunnel", "/etc/codex-ssh/stunnel.conf"])
>     certificate = directory / "tls.crt"
>     certificate.write_bytes(sandbox.read_file("/etc/codex-ssh/tls.crt").result())
>     host_key = (
>         sandbox.read_file("/etc/ssh/ssh_host_ed25519_key.pub").result().decode().strip()
>     )
>     known_hosts = directory / "known_hosts"
>     known_hosts.write_text("cw-codex " + host_key + "\n")
>     forwarder = directory / "tls_proxy.py"
>     forwarder.write_text('''"""Forward SSH through verified TLS, with backpressure in both directions."""
> import asyncio
> import ssl
> import sys
>
> async def main():
>     host, port, certificate = sys.argv[1:]
>     context = ssl.create_default_context(cafile=certificate)
>     remote_reader, remote_writer = await asyncio.open_connection(
>         host, int(port), ssl=context, server_hostname=host
>     )
>     local_reader = asyncio.StreamReader()
>     transport, _ = await asyncio.get_running_loop().connect_read_pipe(
>         lambda: asyncio.StreamReaderProtocol(local_reader), sys.stdin.buffer
>     )
>     async def upload():
>         while data := await local_reader.read(65536):
>             remote_writer.write(data)
>             await remote_writer.drain()
>     def write_output(data):
>         sys.stdout.buffer.write(data)
>         sys.stdout.buffer.flush()
>     async def download():
>         while data := await remote_reader.read(65536):
>             await asyncio.to_thread(write_output, data)
>     tasks = [asyncio.create_task(upload()), asyncio.create_task(download())]
>     try:
>         done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
>         for task in done:
>             task.result()
>     finally:
>         for task in tasks:
>             task.cancel()
>         transport.close()
>         remote_writer.close()
>         await remote_writer.wait_closed()
>
> try:
>     asyncio.run(main())
> except (OSError, ssl.SSLError) as error:
>     print(f'TLS proxy: {error}', file=sys.stderr)
>     sys.exit(1)
> ''')
>     proxy = shlex.join(
>         [sys.executable, str(forwarder), "%h", "%p", str(certificate)]
>     )
>     config = directory / "ssh_config"
>     config.write_text(f'''Host cw-codex
>     HostName {host}
>     Port {port}
>     User agent
>     IdentityFile "{identity}"
>     IdentitiesOnly yes
>     HostKeyAlias cw-codex
>     UserKnownHostsFile "{known_hosts}"
>     StrictHostKeyChecking yes
>     ServerAliveInterval 30
>     ProxyCommand {proxy}
> ''')
>     print("SSH config:", config, flush=True)
> except BaseException as error:
>     try:
>         sandbox.stop().result()
>     except BaseException:
>         error.add_note(
>             f"Automatic cleanup failed. Stop sandbox {sandbox.sandbox_id} manually."
>         )
>     raise
> ```

Replace `[REPOSITORY-URL]` with a public Git repository URL, and choose a new
output directory outside your repository:

```bash theme={"system"}
python create_codex_ssh.py [REPOSITORY-URL] ~/.ssh/cw-codex ~/.ssh/cw-codex-session
```

Successful setup prints the location of the `ssh_config` file and leaves the
sandbox running. The output directory also contains the `sandbox-id`, `tls.crt`,
and `known_hosts` files, plus the `tls_proxy.py` forwarder. If setup fails after
creation, the script attempts to stop the sandbox. If stopping also fails, the
original error includes the sandbox ID for manual cleanup.

Before you connect Codex, verify the SSH connection:

```bash theme={"system"}
ssh -F ~/.ssh/cw-codex-session/ssh_config cw-codex 'id -un; codex --version; test -d /workspace/project/.git && echo repository-ready'
```

The output should include `agent`, `codex-cli 0.154.0`, and `repository-ready`.
If the first connection fails, retry after the endpoint and services finish
starting. If connections continue to fail, inspect the `/var/log/codex-sshd.log` and
`/var/log/codex-stunnel.log` files through the Sandboxes SDK.

With the SSH connection verified, continue with either
[your local CLI](#connect-your-local-cli-to-codex-app-server) or the
[desktop and mobile apps](#use-the-desktop-and-mobile-apps).

## Connect your local CLI to Codex app server

Complete [Create an SSH-accessible sandbox](#create-an-ssh-accessible-sandbox)
first. Use a supported Node.js long-term support (LTS) release to install the same
Codex version locally. The npm package declares Node.js 16 or later as its minimum:

```bash theme={"system"}
npm install --global @openai/codex@0.154.0
```

> [!WARNING]
>
> OpenAI marks the app server WebSocket transport experimental and unsupported for
> production workloads. This example binds the listener and forwarded port to
> loopback addresses and carries traffic through SSH. Other processes on those
> hosts can reach the loopback ports. Use trusted hosts.

Connect the local CLI through an SSH tunnel:

1. In the sandbox's project directory, start the app server. This command saves startup
   output even if the app server exits. Keep the terminal open:

   ```bash theme={"system"}
   ssh -t -F ~/.ssh/cw-codex-session/ssh_config cw-codex 'cd /workspace/project && exec codex app-server --listen ws://127.0.0.1:4500 > /home/agent/codex-app-server.log 2>&1'
   ```

   The `-t` option allocates a remote terminal so **Ctrl+C** reaches the listener.

2. In a second terminal, forward a local port to that listener and keep the
   connection open:

   ```bash theme={"system"}
   ssh -F ~/.ssh/cw-codex-session/ssh_config -N -o ExitOnForwardFailure=yes -L 127.0.0.1:4500:127.0.0.1:4500 cw-codex
   ```

3. In a third terminal, connect the local TUI and explicitly select the remote
   project directory:

   ```bash theme={"system"}
   codex --remote ws://127.0.0.1:4500 --cd /workspace/project
   ```

4. Confirm that the TUI shows `/workspace/project`, then complete
   [Check the session](#check-the-session). If the connection fails, inspect the
   retained startup output:

   ```bash theme={"system"}
   ssh -F ~/.ssh/cw-codex-session/ssh_config cw-codex 'cat /home/agent/codex-app-server.log'
   ```

To continue a saved conversation while the listener is running, restore the SSH
tunnel, then open the remote session picker:

```bash theme={"system"}
codex resume --remote ws://127.0.0.1:4500 --cd /workspace/project
```

Select the conversation to resume. To start a new conversation instead, use the
original `codex --remote` command.

This listener is separate from the app server managed by the desktop app.
Sharing a conversation between the two hasn't been verified. See OpenAI's
[local TUI connection reference](https://learn.chatgpt.com/docs/app-server#connect-the-cli-terminal-ui).

When you finish, exit the TUI, then press **Ctrl+C** in the listener terminal
and the forwarding terminal. Follow
[Reconnect and stop the SSH sandbox](#reconnect-and-stop-the-ssh-sandbox)
to retrieve files and stop compute.

## Use the desktop and mobile apps

Complete [Create an SSH-accessible sandbox](#create-an-ssh-accessible-sandbox)
first. Add the sandbox as an SSH project in the desktop app, then use Remote to
continue from a paired phone. The desktop host maintains the SSH connection.

### Connect the desktop app

Add the sandbox as a remote project, then confirm that Codex writes to its
filesystem.

1. In the `~/.ssh/cw-codex-session/ssh_config` file, copy the generated
   `Host cw-codex` block. In the `~/.ssh/config` file, paste it before any `Host *`
   defaults. Replace an existing `Host cw-codex` entry rather than adding a duplicate.
2. Run `ssh cw-codex 'codex --version'`. Resolve authentication or host-key errors
   before continuing.
3. In the desktop app, open **Settings > Connections**, then add or enable
   the `cw-codex` SSH host.
4. Choose `/workspace/project` as the remote project folder and save the project.
5. Open that remote project and start a conversation. Ask Codex to write a unique,
   non-secret value to the `/workspace/project/sandbox-proof.txt` file.
6. From your terminal, verify the result independently:

   ```bash theme={"system"}
   ssh cw-codex 'cat /workspace/project/sandbox-proof.txt'
   ```

The file content should match the value you requested.

The desktop app starts the remote app server using the SSH user's login shell. Codex
must be installed and authenticated for that user. See OpenAI's
[desktop SSH setup](https://learn.chatgpt.com/docs/remote-connections#connect-to-an-ssh-host).

### Mobile and another desktop through Remote

OpenAI's Remote feature connects supported desktop and mobile apps through a
paired host. The documented mobile setup starts in the ChatGPT desktop app on a
Mac or Windows host, with the same account and workspace on both devices.
Organization settings and rollout availability can restrict access.

To work in the sandbox from your phone, first connect that desktop host to the
sandbox's SSH project. Then pair your phone with the desktop host. In ChatGPT
on iOS or Android, use **Remote**. Your phone connects to the desktop host, which
connects to the sandbox. The desktop app must stay running, awake, and
online. Another supported Mac or Windows desktop app can connect to the same
host when **Control other devices** is available.

Follow OpenAI's [Remote setup instructions](https://learn.chatgpt.com/docs/remote-connections).
An app server WebSocket URL isn't a mobile pairing URL. The Agents API's
`codex exec-server --remote` connection also doesn't pair a mobile device.

### Session continuity and other entry points

Remote supports continuing a connected host's chats from paired devices. That
doesn't establish that a conversation started with the direct `codex --remote`
example appears in an independently configured desktop SSH project. Treat
that cross-interface session handoff as unverified for this setup.

The published Remote setup lists mobile and supported desktop clients. It doesn't
document attaching the ChatGPT or Codex website to this sandbox session. Website
access is outside the interfaces covered in this guide.

Some Codex builds expose experimental `codex remote-control start` and
`codex remote-control pair` commands. They manage an app server daemon and pairing,
but the published mobile instructions don't establish a supported headless Linux
sandbox pairing flow. This guide doesn't treat them as a verified equivalent of
Claude Remote Control. Check the installed CLI help and current OpenAI guidance
before relying on them.

## Check the session

For [Run Codex CLI in a sandbox](#run-codex-cli-in-a-sandbox) or
[Connect your local CLI to Codex app server](#connect-your-local-cli-to-codex-app-server), verify that
Codex writes to the sandbox's filesystem. For desktop access, follow
[Connect the desktop app](#connect-the-desktop-app).

Replace `[PROOF-VALUE]` with a unique non-secret value, then send this prompt in
the connected Codex TUI:

```text theme={"system"}
Write the exact text [PROOF-VALUE] to /workspace/project/sandbox-proof.txt, then read it back.
```

If prompted, approve the write. Exit the TUI, then verify the file independently
from your local terminal using the command for your setup:

> [tab] cws-agent
>
> ```bash theme={"system"}
> cws-agent exec [SANDBOX-NAME] 'cat /workspace/project/sandbox-proof.txt'
> ```

> [tab] Local CLI over SSH
>
> ```bash theme={"system"}
> ssh -F ~/.ssh/cw-codex-session/ssh_config cw-codex 'cat /workspace/project/sandbox-proof.txt'
> ```

The matching value confirms that the agent wrote to this sandbox's filesystem.
It doesn't demonstrate mobile pairing or access from another app.

## Reconnect and stop the SSH sandbox

While the sandbox runs, use the same `cw-codex` host and project.
Closing an SSH connection or the desktop app doesn't stop sandbox compute.

Before you stop the sandbox, save your work to Git or copy files you need:

```bash theme={"system"}
scp -F ~/.ssh/cw-codex-session/ssh_config cw-codex:/workspace/project/sandbox-proof.txt ./sandbox-proof.txt
```

Stop the sandbox using its saved ID:

```python theme={"system"}
from sandbox_auth import AUTH
from pathlib import Path

from cwsandbox import Sandbox

sandbox_id = Path("~/.ssh/cw-codex-session/sandbox-id").expanduser().read_text().strip()
sandbox = Sandbox.from_id(sandbox_id, auth=AUTH).result()
sandbox.stop().result()
```

This example has no persistent volume or snapshot. Stopping or expiry removes
access to its files, login state, and endpoint. To start again, create a new
sandbox and output directory, then replace the `Host cw-codex` block with the new
configuration. Each sandbox has a new endpoint, TLS certificate, and SSH host key.

## Keep results and stop

For the local CLI and desktop app, follow
[Reconnect and stop the SSH sandbox](#reconnect-and-stop-the-ssh-sandbox).

For `cws-agent`, save a workspace snapshot and stop compute:

```bash theme={"system"}
cws-agent down [SANDBOX-NAME]
```

If snapshot creation fails, inspect the reported error before you retry. To stop
without saving, use `cws-agent down [SANDBOX-NAME] --no-snapshot`.

Exiting the TUI doesn't stop compute. When you stop the sandbox or it expires,
its processes end. To restart compute, restore any saved files and start Codex
again. Snapshots don't preserve running processes. Treat saved Codex
authentication and session files as sensitive when you choose what to preserve.

## Troubleshoot

Use the following checks to troubleshoot common issues:

* Authentication fails: distinguish sandbox provisioning credentials, Codex
  model authentication, and SSH keys. They serve different purposes.
* App server flags are rejected: compare local and sandbox `codex --version`
  output. The local CLI example requires the documented WebSocket flags.
* The TUI connects but work fails: inspect model access, billing, workspace
  trust, and approval settings. A transport connection alone doesn't prove model access.
* The connection drops: reconnect while the sandbox is running. Endpoint or
  transport timeouts don't extend its lifetime or guarantee an in-flight turn completed.
* Remote isn't available in the mobile app: check OpenAI's account, workspace,
  host, and rollout requirements. Starting the app server alone doesn't enable it.
