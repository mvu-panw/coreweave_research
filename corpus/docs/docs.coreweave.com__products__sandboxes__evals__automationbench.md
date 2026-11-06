# Evaluate models with AutomationBench

Source: https://docs.coreweave.com/products/sandboxes/evals/automationbench

# Evaluate models with AutomationBench

> Run AutomationBench with Harbor, CoreWeave Sandboxes, and a configurable model endpoint.

Run [AutomationBench](https://github.com/zapier/AutomationBench) in CPU sandboxes to evaluate a tool-calling model on simulated business workflows. This tutorial uses Harbor to schedule tasks independently, retry selected infrastructure failures, and retain results. Start with one task, then increase concurrency as your sandbox and inference quotas permit.

The example uses [CoreWeave Serverless Inference](https://docs.coreweave.com/products/inference/serverless.md). You can evaluate another model by changing the OpenAI-compatible Chat Completions endpoint, model ID, and inference key.

## Evaluation workflow

The [AutomationBench recipe](https://github.com/coreweave/cwsandbox-recipes/tree/main/recipes/automationbench) runs Harbor on your local machine. Each trial gets a CPU sandbox where AutomationBench installs its agent loop, simulated applications, and assertion-based evaluator. The model runs at your inference endpoint. No GPU or real application credentials are required in the sandbox.

The recipe implements Harbor's `BaseAgent` and `BaseEnvironment` interfaces and uses public CoreWeave Sandboxes software development kit (SDK) calls. It runs the unchanged native `auto-bench` evaluator and doesn't require an upstream AutomationBench Harbor adapter. Harbor, AutomationBench, and `cwsandbox` SDK versions are pinned in the recipe.

## Prerequisites

Before you begin, prepare the following:

* [`uv`](https://docs.astral.sh/uv/getting-started/installation/) and Git on your local machine. The recipe requires Python 3.13 or later. If it isn't installed, `uv` [downloads a matching Python version](https://docs.astral.sh/uv/concepts/python-versions/).
* A [CoreWeave API access token](https://docs.coreweave.com/products/sandboxes/get-started.md#choose-a-credential) with sandbox access.
* Enough [concurrent sandbox quota](https://docs.coreweave.com/products/sandboxes/reference/limits-and-quotas.md) for the selected concurrency and resource policies that permit 2 vCPUs and 4 GiB of memory per sandbox.
* An inference endpoint with tool calling, an API key, and sufficient inference quota. For the example, create a [Serverless Inference](https://docs.coreweave.com/products/inference/serverless.md) API key.
* Network access from your machine to the sandbox API and package repositories, and from sandboxes to GitHub, Debian and Python package repositories, and your inference endpoint.

The initial check creates one CPU sandbox. Sandbox resources and inference are metered separately. Review [sandbox pricing](https://www.coreweave.com/forge-pricing/inference-agents) and your inference provider's [usage limits and pricing](https://docs.coreweave.com/products/inference/serverless/usage-limits.md) before scaling the evaluation.

## Install the recipe

Clone the recipes repository and install the pinned dependencies:

```bash theme={"system"}
git clone https://github.com/coreweave/cwsandbox-recipes.git
cd cwsandbox-recipes/recipes/automationbench
uv sync --frozen
cp .env.example .env
```

From this recipe directory, run the remaining commands. The local environment contains Harbor and the sandbox SDK. Each sandbox installs AutomationBench from its pinned checkout using the benchmark's frozen lockfile.

## Configure the model and credentials

Load credentials from your secret manager into the process environment. Set `CWSANDBOX_API_KEY` to your CoreWeave sandbox credential and `MODEL_API_KEY` to your inference credential. Don't save keys in the `.env` file.

In the `.env` file, set only the model endpoint, model name, and optional project. For the Serverless Inference example, use these settings. Replace `[WANDB-TEAM]` and `[WANDB-PROJECT]` with names you can access:

```bash theme={"system"}
MODEL_BASE_URL="https://api.inference.wandb.ai/v1"
MODEL_NAME="openai/gpt-oss-120b"
MODEL_PROJECT="[WANDB-TEAM]/[WANDB-PROJECT]"
```

`MODEL_PROJECT` sets the `OpenAI-Project` header for Serverless Inference usage tracking.

The model ID is an example, not a requirement. Choose a tool-calling model from the [available models](https://docs.coreweave.com/products/inference/serverless/models.md). For another compatible provider or a model you serve yourself, replace the model settings in the `.env` file. Replace `[INFERENCE-HOST]` and `[MODEL-ID]` with your provider's values:

```bash theme={"system"}
MODEL_BASE_URL="https://[INFERENCE-HOST]/v1"
MODEL_NAME="[MODEL-ID]"
```

Load that provider's key into `MODEL_API_KEY` in the process environment and keep `CWSANDBOX_API_KEY` set. If the provider doesn't use the project header, remove `MODEL_PROJECT` from the `.env` file and unset any inherited `MODEL_PROJECT` environment variable before running the command. The endpoint must be reachable from the sandbox. `localhost` refers to the sandbox itself, not your machine. Other API protocols require adapting the native evaluator options.

The recipe explicitly uses CoreWeave authentication for sandbox operations. The sandbox token stays on the host. Only model configuration and the inference key are injected into the sandbox at creation. The job configuration doesn't contain credential values.

For broader credential-handling guidance, see [environment variables and secrets](https://docs.coreweave.com/products/sandboxes/client/guides/environment-variables.md). Protect downloaded logs and traces, which can contain task data and provider error messages.

## Run a setup check

Evaluate one simple task with one sandbox:

```bash theme={"system"}
uv run --env-file .env python run.py \
  --task simple.email_sf_contact_phone_update \
  --concurrency 1 \
  --output results-smoke
```

The output directory must be new. Harbor starts the sandbox, installs AutomationBench, runs the task, collects results, and deletes the sandbox. A completed job prints:

```text theme={"system"}
Harbor job finished; inspect job-result.json and archived attempts.
```

Inspect the `results-smoke/job-result.json` file for completed and errored trial counts. An exit status of zero means no trials remain errored or missing. It doesn't mean the model passed the task's assertions. The native `agent/automationbench.json` export records `passed`, `score`, timing, and token usage. The verifier maps `passed` and `score` to Harbor rewards named `pass` and `partial_credit`. In `job-result.json`, the `stats.evals` entry reports the mean of each reward across trials under `metrics`. Trials without a reward count as zero. `reward_stats` lists the trials for each reward value.

The agent uses the `api` toolset, a maximum of 50 response steps, one task at a time per sandbox, and the provider's default reasoning setting. Native whole-task autohealing is deactivated so Harbor owns trial retries. The model client can still retry individual requests internally.

## Increase parallelism

After the setup check succeeds, start with a small subset:

```bash theme={"system"}
head -n 8 tasks-scored.txt > tasks-small.txt
uv run --env-file .env python run.py \
  --tasks-file tasks-small.txt \
  --concurrency 4 \
  --output results-small
```

Each trial requests 2 vCPUs and 4 GiB of memory, so four concurrent trials request up to 8 vCPUs and 16 GiB. Harbor schedules each task independently: when one finishes, another can use its slot. Per-task setup adds overhead because each sandbox installs the evaluator.

The recipe includes two task lists for the pinned benchmark revision:

| Task list | Tasks | Purpose |
| - | -: | - |
| `tasks-scored.txt` | 600 | 100 tasks each for sales, marketing, operations, support, finance, and HR |
| `tasks-simple.txt` | 200 | Separate simple baseline tasks |

To evaluate the scored set, select its task list and a concurrency your quotas support:

```bash theme={"system"}
uv run --env-file .env python run.py \
  --tasks-file tasks-scored.txt \
  --concurrency 16 \
  --output results-scored
```

Sixteen concurrent trials request up to 32 vCPUs and 64 GiB in total. This is an example setting, not a validated throughput target. Increase concurrency gradually and monitor inference limits as well as sandbox capacity.

Run baseline tasks into a separate output directory. Don't include the 200 simple tasks in the scored-set denominator. These are public tasks. AutomationBench's official leaderboard uses a separate private task set, so scores aren't directly comparable.

## Retry capacity and inference-limit failures

The recipe configures Harbor's `RetryConfig` to allow five retries after the original attempt, waiting 30, 60, 120, 240, and 300 seconds. The retry allowlist includes these exceptions:

* `SandboxResourceExhaustedError`
* `SandboxUnavailableError`
* `SandboxRequestTimeoutError`
* `EnvironmentStartTimeoutError`
* `ApiRateLimitError`
* `ApiUsageLimitError`

Harbor excludes `ApiUsageLimitError` by default. The recipe removes it from that exclusion set and adds it to the allowlist. The adapter maps recognized terminal inference quota and rate-limit messages from the native evaluator to the corresponding Harbor exceptions. This mapping depends on provider error text. Inspect logs when a provider reports a different format.

Persistent capacity or credit exhaustion still requires capacity or credits to become available. If errors remain after retries, the script exits nonzero and retains the final error. Ordinary assertion failures, refusals, malformed tool-call JSON, and agent execution timeouts don't trigger the retry policy.

Harbor removes failed trial directories before retrying. The recipe's end-of-trial hook archives each attempt first, including its result and available logs. Keep those attempts and disclose infrastructure recovery when reporting scores. Don't silently substitute better retry outcomes for model failures.

## Inspect results and slow trials

Each output directory contains the following artifacts:

| Path | Contents |
| - | - |
| `job-config.json` | Harbor job configuration without credential values |
| `job-result.json` | Final job statistics and errors |
| `jobs/automationbench/` | Final trials, native exports, logs, and verifier rewards |
| `attempts/` | Archived trial attempts, including failures |
| `sandbox-ids.jsonl` | Sandbox IDs recorded for cleanup |

Use native exports for task timing and token usage. The adapter doesn't populate Harbor's aggregate agent token or cost fields. Record the model, endpoint, benchmark revision, task list, reasoning settings, concurrency, and retry policy alongside results. If you stop a run, report only the exported tasks as completed evaluations and label the results as partial.

Model response time can dominate a task even with few steps or output tokens. Compare `model_time_s` with `tool_time_s` and inspect the `agent/eval.log` file before attributing delays to sandbox resources. Provider rejection of malformed tool-call JSON is a model or protocol failure, not evidence of sandbox quota exhaustion. AutomationBench lists rollouts that stopped mid-turn in the export's `summary.aborted_tasks` field. Their per-task `errors` arrays can be empty, so check that field and the logs as well as task errors.

Setup has an 11-minute timeout. Agent execution has a separate 45-minute timeout, and the native evaluation command inside it has a 40-minute timeout. Each sandbox has a 1-hour lifetime cap, which ends the sandbox even if a timeout hasn't elapsed. Agent execution timeouts aren't retried by this policy.

## Stop and clean up

To stop a foreground run, press Ctrl+C and allow Harbor to exit. The job sets `delete=True` for teardown. If the process is forcibly terminated or cleanup fails, stop the local runner before deleting remaining sandboxes so it can't create replacements.

After the runner stops, use its output directory to verify cleanup:

```bash theme={"system"}
uv run --env-file .env python cleanup.py results-smoke
```

Replace `results-smoke` with the directory for the job you stopped. The script deletes only recorded sandbox IDs and prints their terminal states. A sandbox that's already absent is reported as `not_found`. Investigate a nonzero exit, which means deletion or terminal-state verification failed. The configured lifetime cap also bounds sandbox lifetime if the host process disappears.

## Validation scope

During recipe development, the native evaluator exported results for 730 of 800 public tasks across eight parallel CPU sandboxes with `openai/gpt-oss-120b` on Serverless Inference. That run was stopped before completion, so its results aren't a benchmark score. Harbor retry scheduling was verified separately: an injected `SandboxResourceExhaustedError`, a 30-second backoff, and one real task that completed, exported results, and cleaned up. The recipe replaces the initial experiment's environment hooks with a `BaseEnvironment` implementation using public SDK calls. That refactor has offline coverage but hasn't been run against the live service. A full dataset at high Harbor concurrency hasn't been validated.

For offline tests and an optional controlled retry check, see the [recipe README](https://github.com/coreweave/cwsandbox-recipes/tree/main/recipes/automationbench#test-and-compatibility).
