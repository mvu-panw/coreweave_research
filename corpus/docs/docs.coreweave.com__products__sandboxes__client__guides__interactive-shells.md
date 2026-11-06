# Interactive shells and TTY

Source: https://docs.coreweave.com/products/sandboxes/client/guides/interactive-shells

# Interactive shells and TTY

> Use interactive TTY sessions with shell() for terminal applications and raw byte streaming.

Use `Sandbox.shell()` for interactive TTY sessions. It returns a `TerminalSession` with raw byte streaming and no output buffering, designed for interactive use. For batch command execution, use [`exec()`](https://docs.coreweave.com/products/sandboxes/client/guides/execution) instead.

## Choose authentication

These examples run on serverless capacity unless a section specifies CKS. Choose the credential for the account that owns your sandboxes. See [Choose and get credentials](https://docs.coreweave.com/products/sandboxes/placement.md#choose-and-get-credentials) to obtain a key or token.

Run the installation commands in an [active Python virtual environment](https://docs.coreweave.com/products/sandboxes/client.md#prepare-your-python-environment).

Save the Python code from your credential tab as `sandbox_auth.py` beside the Python scripts you run from this page. It stores the authentication choice, not your credential. The examples import `AUTH` from that file and pass it explicitly to each new sandbox or session.

> [tab] Forge API key
>
> Use your Forge API key through the SDK's W\&B authentication strategy:
>
> ```bash theme={"system"}
> uv pip install 'cwsandbox[wandb]>=1.14.2'
> export WANDB_API_KEY="[WANDB-API-KEY]"
> ```
>
> ```python title="sandbox_auth.py" theme={"system"}
> from cwsandbox import AuthStrategy
>
> AUTH = AuthStrategy.WANDB
> ```

> [tab] CoreWeave API access token
>
> Use the token for your CoreWeave organization:
>
> ```bash theme={"system"}
> uv pip install 'cwsandbox>=1.14.2'
> export CWSANDBOX_API_KEY="[API-ACCESS-TOKEN]"
> ```
>
> ```python title="sandbox_auth.py" theme={"system"}
> from cwsandbox import AuthStrategy
>
> AUTH = AuthStrategy.COREWEAVE_API_KEY
> ```

For CKS placement, choose the CoreWeave token, [enable a runner](https://docs.coreweave.com/products/sandboxes/get-started-cks.md), and set `placement_mode="cks"` on sandbox creation or in `SandboxDefaults`. Creating a session with `auth=AUTH` also authenticates the sandboxes it owns. Keep the same credential when reconnecting, listing, or cleaning up sandboxes.

## Shell session

Create a sandbox and open an interactive shell session. `Sandbox.run()` with no command uses the default long-running command. This example sends commands, reads their output, and waits for the shell to exit before leaving the `with` block. Leaving the block stops the sandbox.

```python theme={"system"}
import sys

from sandbox_auth import AUTH
from cwsandbox import Sandbox

with Sandbox.run(resources={"cpu": "1", "memory": "1Gi"}, auth=AUTH) as sandbox:
    terminal = sandbox.shell(
        ["/bin/bash"],
        width=80,
        height=24,
    )
    terminal.stdin.writeline("echo hello").result()
    terminal.stdin.writeline("ls -la /tmp").result()
    terminal.stdin.writeline("exit").result()

    # Read output while the sandbox context is active.
    for chunk in terminal.output:
        sys.stdout.buffer.write(chunk)
        sys.stdout.buffer.flush()

    exit_code = terminal.wait(timeout=5.0)
```

`shell()` always allocates a TTY and enables stdin. The returned `TerminalSession` streams raw bytes with no UTF-8 decode or encode round-trip, making it safe for terminal escape sequences and binary output.

## Send commands and read output

While the shell session is active, write commands to `terminal.stdin` and stream the merged byte output from `terminal.output`, as shown in the preceding example. Keep these operations inside the `with` block.

`TerminalSession` doesn't buffer output. Stdout and stderr are merged into a single raw byte stream on `terminal.output`. There are no separate `stdout` or `stderr` attributes on the result. Consume `terminal.output` continuously. If you stop reading, backpressure from the bounded queue stalls the remote session.

## Terminal resize

Send resize messages when the terminal dimensions change. Call `resize()` inside the `with` block while the shell session is active:

```python theme={"system"}
terminal.resize(120, 40)
```

`resize()` is fire-and-forget on `TerminalSession`.

## Exit a shell session

Inside the `with` block, end a shell session by closing stdin or sending an exit command:

```python theme={"system"}
terminal.stdin.writeline("exit").result()  # Ask the remote shell to exit
# or
terminal.stdin.close().result()            # Close the stdin stream
```

The shell session completes when the remote process exits. Call `terminal.wait()` or `terminal.result()` to block for the exit code.

## Attach your local terminal

To work in a running sandbox from your own terminal, put the local terminal in raw mode and forward its input to a `shell()` session. The following script attaches to an existing sandbox by ID, forwards your keystrokes to a Bash shell in the sandbox, and restores your local terminal settings when the shell exits. It uses `termios`, so it runs on macOS or Linux.

Save the script as `attach_sandbox.py` beside `sandbox_auth.py`:

```python title="attach_sandbox.py" theme={"system"}
import os
import shutil
import sys
import termios
import threading
import tty

from cwsandbox import Sandbox
from sandbox_auth import AUTH

if not sys.stdin.isatty() or not sys.stdout.isatty():
    raise SystemExit("Run this script in an interactive terminal.")

sandbox = Sandbox.from_id(sys.argv[1], auth=AUTH).result()
size = shutil.get_terminal_size()
terminal = sandbox.shell(["/bin/bash"], width=size.columns, height=size.lines)
fd = sys.stdin.fileno()
saved = termios.tcgetattr(fd)

def forward_input():
    while data := os.read(fd, 1024):
        terminal.stdin.write(data).result()
    terminal.stdin.close().result()

try:
    tty.setraw(fd)
    threading.Thread(target=forward_input, daemon=True).start()
    for chunk in terminal.output:
        sys.stdout.buffer.write(chunk)
        sys.stdout.buffer.flush()
    result = terminal.result()
finally:
    termios.tcsetattr(fd, termios.TCSADRAIN, saved)
    terminal.stdin.close().result()

raise SystemExit(result.returncode)
```

Replace `[SANDBOX-ID]` with the ID of a running sandbox, then run the script from an interactive terminal:

```bash theme={"system"}
python attach_sandbox.py [SANDBOX-ID]
```

The script exits with the remote shell's exit code.

## Commands and use cases

To run commands with the command-line interface (CLI), [install the CLI and configure your credentials](https://docs.coreweave.com/products/sandboxes/cli.md#install-and-authenticate). The CLI uses a CoreWeave API access token in `CWSANDBOX_API_KEY` by default. For a Forge API key, install the `cli` and `wandb` extras, set `WANDB_API_KEY`, and pass `--auth wandb` before the command. Use the credential that owns the sandbox.

For terminal access through the SDK with either credential, use the [`sandbox.shell()` attachment script](#attach-your-local-terminal) on this page.

| Use case | Approach |
| - | - |
| One-off command from your terminal (CoreWeave API access token) | `cwsandbox --auth coreweave_api_key exec [SANDBOX-ID] echo hello` |
| Interactive shell from your terminal (CoreWeave API access token) | `cwsandbox --auth coreweave_api_key sh [SANDBOX-ID]` |
| Interactive shell from your terminal (Forge API key) | `cwsandbox --auth wandb sh [SANDBOX-ID]` |
| Run a script, capture output (SDK) | `exec(["python", "script.py"])` |
| Interactive shell session (SDK) | `shell(["/bin/bash"])` |
| Send input to a command (SDK) | `exec(["cat"], stdin=True)` |
| Terminal application (vim, htop) | `shell(["vim"])` + [local terminal raw mode](#attach-your-local-terminal) |

## See also

* [Command execution](https://docs.coreweave.com/products/sandboxes/client/guides/execution.md) - Run commands with `exec()`.
* [Sandbox logging](https://docs.coreweave.com/products/sandboxes/client/guides/logging.md) - Stream container logs.
