# wandb docker-run

Source: https://docs.coreweave.com/products/wandb/ref/cli/wandb-docker-run

# wandb docker-run

[View source](https://github.com/wandb/wandb/blob/v0.31.0/wandb/cli/cli.py#L2385)

## Usage

```bash theme={"system"}
docker-run [OPTIONS] [DOCKER_RUN_ARGS]...
```

## Description

Wrap `docker run` and inject W\&B environment variables automatically.

Pass all arguments through to `docker run` while injecting:

* WANDB\_API\_KEY: Inject the current API key if logged in so the
  container can authenticate with W\&B.

* WANDB\_DOCKER: Inject the resolved image ID if the image can be detected
  from the arguments so W\&B can track which Docker image produced the run.

Add `--runtime nvidia` automatically if `nvidia-docker` is detected
on the host and `--runtime` is not already set.

For example, to run the Python script train.py inside the "my-image" container:

```bash theme={"system"}
wandb docker-run my-image python train.py
```

## Arguments

| Name | Default | Type |
| - | - | - |
| `docker_run_args` | STR | False |
