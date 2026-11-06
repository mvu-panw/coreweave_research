# wandb verify

Source: https://docs.coreweave.com/products/wandb/ref/cli/wandb-verify

# wandb verify

[View source](https://github.com/wandb/wandb/blob/v0.31.0/wandb/cli/cli.py#L3497)

## Usage

```bash theme={"system"}
verify [OPTIONS]
```

## Description

Run integration checks against a self-hosted W\&B instance.

Validate that a self-hosted or dedicated cloud W\&B deployment is configured
and operating correctly. Do not run this command against the public W\&B
cloud at forge.coreweave.com.

Exits with `code 1` if any critical check fails.

For example, to verify the currently configured W\&B instance:

```bash theme={"system"}
wandb verify --host https://my-wandb-instance.com
```

To verify a specific self-hosted instance:

```bash theme={"system"}
wandb verify --host https://my-wandb-server.example.com
```

## Options

| Flag | Type | Description |
| - | - | - |
| `--host` | STR | Target a specific W\&B instance URL. Default to configured base URL. **Default**: None |
