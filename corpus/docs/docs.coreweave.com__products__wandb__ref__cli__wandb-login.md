# wandb login

Source: https://docs.coreweave.com/products/wandb/ref/cli/wandb-login

# wandb login

[View source](https://github.com/wandb/wandb/blob/v0.31.0/wandb/cli/cli.py#L266)

## Usage

```bash theme={"system"}
login [OPTIONS] [KEY]...
```

## Description

Authenticate your machine with W\&B.

Store an API key locally for authenticating with W\&B services.
By default, credentials are stored without server-side verification.

If no API key is provided as an argument, the command looks for
credentials in the following order:

1. The WANDB\_API\_KEY environment variable

2. The api\_key setting in a system or workspace settings file (use
   `wandb status` to see which settings file is used)

3. The .netrc file (\~/.netrc, \~/\_netrc, or the NETRC env var path)

4. An interactive prompt (if a TTY is available)

For self-hosted or dedicated cloud deployments, specify the server
URL with `--host`, or set the WANDB\_BASE\_URL environment variable.

For example, to log in interactively (prompts for API key):

```bash theme={"system"}
wandb login
```

To log in with an explicit API key (WANDB\_API\_KEY\_EXAMPLE):

```bash theme={"system"}
wandb login WANDB_API_KEY_EXAMPLE
```

To log in and bypass verifying the API key:

```bash theme={"system"}
wandb login --no-verify
```

To log in to the W\&B public cloud instead of a configured self-hosted instance:

```bash theme={"system"}
wandb login --cloud
```

To log in to a self-hosted W\&B instance:

```bash theme={"system"}
wandb login --host https://my-wandb-server.example.com
```

To force a new login prompt even if already authenticated:

```bash theme={"system"}
wandb login --relogin
```

## Arguments

| Name | Default | Type |
| - | - | - |
| `key` | STR | False |

## Options

| Flag | Type | Description |
| - | - | - |
| `--cloud` | BOOL Flag | Log in to the W\&B public cloud (`https://api.forge.coreweave.com`). Mutually exclusive with --host. **Default**: False |
| `--host, --base-url` | STR | Log in to a specific W\&B server instance by URL (e.g. [https://my-wandb.example.com](https://my-wandb.example.com)). Mutually exclusive with --cloud. **Default**: None |
| `--relogin` | BOOL Flag | Force a new login prompt, ignoring any existing credentials. **Default**: None |
| `--verify` | BOOL Flag | Verify the API key with W\&B after storing it. If verification is successful, display the source of the credentials and the default team. **Default**: True |
