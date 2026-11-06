# Run DeepSWE v1.1 evaluations

Source: https://docs.coreweave.com/products/sandboxes/evals/deepswe

# Run DeepSWE v1.1 evaluations

> Generate code patches and grade them in separate sandboxes with a small DeepSWE v1.1 sample.

Evaluate a coding agent on a small [DeepSWE](https://github.com/datacurve-ai/deep-swe) v1.1 sample. CoreWeave Sandboxes provides the environments where the agent edits code and the benchmark verifies its patches. The DeepSWE recipe provides the evaluation script, dependency lockfile, and sandbox adapter.

The recipe runs the [mini-swe-agent](https://github.com/SWE-agent/mini-swe-agent) coding agent on your local machine and sends its shell commands to a serverless sandbox. After the agent finishes, [Pier](https://pypi.org/project/datacurve-pier/0.3.1/), the evaluation framework, collects its committed changes and stops the agent sandbox. A fresh verifier sandbox applies the patch and runs the held-out tests.

The example uses `moonshotai/Kimi-K2.7-Code` through [Serverless Inference](https://docs.wandb.ai/inference) for model requests. DeepSWE and Sandboxes don't require that provider. The supplied recipe fixes the Forge endpoint and credential handling. Its `--model` option selects another model on that endpoint. Using another provider requires adapting the recipe's model configuration and authentication.

Only the verifier receives the held-out test files. The recipe creates both sandboxes with outbound network access denied. The sandbox and inference credentials stay on your local machine.

> [!NOTE]
>
> This guide validates an integration with a small sample. The host-side agent adapter and run limits differ from the official DeepSWE leaderboard setup. Results from two tasks don't estimate performance across the full benchmark.

## Prerequisites

Before you begin, make sure you have the following prerequisites:

* Python 3.12 or later, Git, and the [`uv`](https://docs.astral.sh/uv/getting-started/installation/) package manager.
* A [CoreWeave API access token](https://docs.coreweave.com/products/sandboxes/placement.md#coreweave-api-access-token) with the Sandbox User role in an organization enabled for serverless sandboxes.
* A [Forge API key](https://forge.coreweave.com/wandb/authorize) with access to the example model on Serverless Inference.
* Network access from your local machine to the Sandboxes API and `https://api.inference.wandb.ai/v1`.

Each task requests 2 CPUs and 8 GiB of memory. By default, tasks run sequentially, with separate agent and verifier sandboxes. No GPU or local Docker installation is required. The adapter uses the task's CPU and memory settings but doesn't enforce its `storage_mb` setting.

Check [which account is billed for sandbox usage](https://docs.coreweave.com/products/sandboxes/placement.md#choose-and-get-credentials) and the [inference rates](https://docs.wandb.ai/inference/usage-limits/). The step and time limits bound execution but aren't a spending limit.

## Install the recipe

Clone the recipes repository and install its locked dependencies:

```bash theme={"system"}
git clone https://github.com/coreweave/cwsandbox-recipes.git
cd cwsandbox-recipes/recipes/deepswe
uv sync --locked
```

The recipe pins Pier 0.3.1, `mini-swe-agent` 2.2.6, and `cwsandbox` 1.14.2. Run the remaining commands from the `recipes/deepswe` directory.

To match the task images and verifier layout to the adapter, fetch the tested DeepSWE revision:

```bash theme={"system"}
git clone https://github.com/datacurve-ai/deep-swe.git
git -C deep-swe checkout 0b9fabbb63b9104d678fe965e1632f2dd9eaa2ea
```

## Configure the example model and credentials

In the terminal where you run the recipe, set both credentials. Replace `[API-ACCESS-TOKEN]` with your CoreWeave API access token and `[WANDB-API-KEY]` with your Forge API key, or export them from your secret manager:

```bash theme={"system"}
export CWSANDBOX_API_KEY="[API-ACCESS-TOKEN]"
export WANDB_API_KEY="[WANDB-API-KEY]"
export MSWEA_MODEL_RETRY_STOP_AFTER_ATTEMPT=3
export MSWEA_SILENT_STARTUP=1
```

The recipe uses `CWSANDBOX_API_KEY` for sandbox authentication and `WANDB_API_KEY` for inference. It passes the inference key to LiteLLM through `OPENAI_API_KEY`, keeping it out of the serialized model configuration. The recipe reads your process environment and doesn't automatically load a project `.env` file.

Before you create a sandbox, verify model access:

```bash theme={"system"}
uv run --locked python - <<'PY'
import os
from openai import OpenAI

client = OpenAI(
    base_url="https://api.inference.wandb.ai/v1",
    api_key=os.environ["WANDB_API_KEY"],
    timeout=60,
)
response = client.chat.completions.create(
    model="moonshotai/Kimi-K2.7-Code",
    messages=[{"role": "user", "content": "Respond with exactly OK."}],
    max_tokens=64,
)
print(response.choices[0].message.content)
PY
```

A successful request returns a short response such as `OK`. Before you start the sample, resolve any authentication, model-access, or credit errors.

## Run a sample

For an initial integration check, run one Python task:

```bash theme={"system"}
uv run --locked python run.py \
  --tasks deep-swe/tasks \
  --task tomlkit-toml-table-converters \
  --steps 160 --agent-timeout 1800 \
  --job-name kimi-smoke
```

A one-task run can still use most of the step or time allowance. It checks the integration, and a successful run doesn't require the model to solve the task.

To expand the sample, run one Go task and one Python task with a new job name:

```bash theme={"system"}
uv run --locked python run.py \
  --tasks deep-swe/tasks \
  --task abs-stepped-slices \
  --task tomlkit-toml-table-converters \
  --steps 160 --agent-timeout 1800 \
  --job-name kimi-sample
```

The recipe reports sandbox creation, completed model steps, and sandbox shutdown. Each task has a limit of 160 agent steps and a 30-minute agent timeout. Shell commands have a 120-second timeout. A command timeout becomes an observation that lets the agent continue.

The task's collection hook extracts the difference between its base commit and the `HEAD` reference. The agent must commit its changes for them to appear in the submitted patch. Uncommitted edits aren't collected.

For a fresh run, use a new job name. Pier can resume an existing job directory, so reusing the `kimi-sample` job name doesn't start a clean rerun. For deterministic random sampling and other recipe options, see the [recipe README](https://github.com/coreweave/cwsandbox-recipes/blob/main/recipes/deepswe/README.md).

### Configure concurrency and retries

Pier manages the recipe's trial queue. Use `--concurrency` to set the maximum number of concurrent trials. The default is `1`. Verify the complete workflow at that setting. Then increase concurrency gradually within your inference provider's allowance, including requests from other jobs using the same account. A successful model-access check doesn't validate capacity for concurrent requests.

The recipe defaults to `--max-retries 2`. After a `RateLimitError`, `APIConnectionError`, or `ServiceUnavailableError`, Pier can restart a trial twice. Pier waits 30 seconds before the first retry and 60 seconds before the second.

Each retry starts a fresh agent attempt and can incur additional charges. Step and agent-time limits apply separately to each execution. Retries create fresh sandboxes, so the total number created can exceed the concurrent-trial limit.

Authentication errors, sandbox startup failures such as `SandboxFailedError`, other unlisted exceptions, and low verifier scores don't trigger automatic retries. To disable trial retries, set `--max-retries 0`.

The recipe preserves unsuccessful attempts under `jobs/[JOB-NAME]/failed-attempts/[TRIAL-NAME]/[ATTEMPT-ID]/` before Pier replaces their trial directories. The normal trial directory and job summary contain the final execution's result. For a parallel-run command, see the recipe's [concurrency and retry settings](https://github.com/coreweave/cwsandbox-recipes/blob/main/recipes/deepswe/README.md#configure-concurrency-and-retries).

### Handle inference throttling

An HTTP `429` response with `rate_limit_exceeded` and `concurrency limit reached for requests` means the inference provider rejected a model request. Forge applies limits per project and per user. Reduce `--concurrency` and simultaneous model requests from other jobs using the same inference account. For a higher limit, contact support through the [inference limits documentation](https://docs.wandb.ai/inference/usage-limits/#concurrency-limits).

With the example's `MSWEA_MODEL_RETRY_STOP_AFTER_ATTEMPT=3` setting, mini-swe-agent makes up to three attempts per failed model query, including the initial attempt. These retries continue the same conversation if a request succeeds. The model client can also retry within an attempt. If request retries are exhausted with an eligible exception, Pier applies the trial retry policy.

Pier 0.3.1 limits whole trials. The recipe has no separate inference-request concurrency limit or automatic concurrency adjustment. Increasing retries alone doesn't resolve sustained overload.

A job can recover some throttled trials while others exhaust their retries. Those trials retain their final exception, and the recipe exits with a nonzero status. They aren't silently skipped.

After you resolve persistent throttling, rerun only the affected tasks with lower concurrency and a new job name. If a retry ends with a different error, inspect the `failed-attempts/` directory as well. Inference throttling and sandbox startup failures require separate diagnosis. For commands and Pier's built-in error-filtered job recovery, follow the recipe's [throttling recovery procedure](https://github.com/coreweave/cwsandbox-recipes/blob/main/recipes/deepswe/README.md#recover-from-inference-throttling).

## Inspect the results

The following examples inspect the two-task job. For the one-task run, replace `kimi-sample` with `kimi-smoke`. Read the job summary:

```bash theme={"system"}
uv run --locked python -m json.tool jobs/kimi-sample/result.json
```

`stats.n_completed_trials` counts finished trials, including errors. `stats.n_retries` counts extra trial executions, not additional benchmark samples. A recovered trial can have archived errors while its final result has no exception.

Before you interpret the job's aggregate score, check `stats.n_errored_trials` and each trial's final `exception_info` and `verifier_result`. The aggregate mean can be `0` when verification failed to start and no patch was graded.

A trial with a binary verifier reward of `0` or `1` and no exception completed the workflow. Reward `1` means all required checks passed. Reward `0` means the patch didn't satisfy all required checks. An exception, missing reward, or reward of `-1` is a run error. Investigate run errors separately from model performance.

Each trial directory under `jobs/kimi-sample/` contains:

| File | Contents |
| - | - |
| `result.json` | Trial status, timings, token counts, and verifier result |
| `agent/mini.trajectory.json` | Model conversation and shell actions |
| `artifacts/model.patch` | Patch collected from the agent's commits |
| `verifier/reward.json` | Binary reward and partial scores |
| `verifier/ctrf.json` | Structured test results |
| `verifier/test-stdout.txt` | Verifier output |

Inspect the held-out test results even if the agent reports that its own tests passed. In `reward.json`, `f2p_passed` and `f2p_total` count checks for new behavior, and `p2p_passed` and `p2p_total` count existing checks. A high `partial` score can still accompany a binary `reward` of `0` when a required check fails.

Saved token counts can be incomplete. In this adapter, a response rejected for missing tool calls can consume tokens without retaining its usage in the trajectory. Treat costs calculated from those counts as partial estimates, and use provider billing for actual charges. Preflight requests and sandbox charges are separate.

If the agent submitted a patch but verifier startup failed, preserve `artifacts/model.patch` and the original error result. The recipe has no supported verifier-only retry command. A new model run produces a new attempt, not a regrade of the saved patch. Any separate regrade must use the unchanged patch and matching task revision and retain its own result.

To check the verifier independently, follow the recipe's [no-edit and reference-solution controls](https://github.com/coreweave/cwsandbox-recipes/blob/main/recipes/deepswe/README.md#4-inspect-the-results). The controls don't call the model and must remain separate from model results.

## Clean up

Pier stops agent and verifier sandboxes on normal completion and during error cleanup. Each sandbox also has a 90-minute maximum lifetime. If you need the patches, trajectories, or test reports, keep the job directory.

If the local evaluation process is terminated before cleanup finishes, stop any remaining sandbox. Replace `[SANDBOX-ID]` with the sandbox ID from the run logs:

```bash theme={"system"}
uv run --locked python - <<'PY'
from cwsandbox import AuthStrategy, Sandbox

sandbox = Sandbox.from_id(
    "[SANDBOX-ID]", auth=AuthStrategy.COREWEAVE_API_KEY
).result()
sandbox.stop(missing_ok=True).result()
PY
```

The recipe doesn't create a GPU deployment, model endpoint, or persistent volume.

## Troubleshooting

| Symptom | Action |
| - | - |
| Inference authentication or permission error | Check the Forge API key, model access, and inference credits. Sandbox authentication is separate. |
| Inference HTTP `429` or `RateLimitError` | Read the provider's error message. For concurrency errors, follow [Handle inference throttling](#handle-inference-throttling). An exhausted retry is a run error, not a model score. |
| Sandbox fails before a model step or verifier result | Inspect the sandbox status for an image-pull or capacity failure. Preserve the job artifacts and resolve the infrastructure error before rerunning. |
| `Unsupported verifier Dockerfile` | Use the pinned dataset revision and supported sample tasks. Other verifier layouts require adapter changes. |
| Empty `model.patch` file | Check whether the agent committed its changes before reaching its limit. |
| Agent reaches its step or time limit | Inspect the saved trajectory and token usage before increasing the `--steps` or `--agent-timeout` values. |
| Dependency installation fails in the sandbox | Outbound network access is denied. Use the preinstalled task dependencies or investigate the task image. |

## Next steps

For more information, see the following resources:

* [Evals overview](https://docs.coreweave.com/products/sandboxes/evals.md): choose an evaluation workflow and separate model inference from benchmark execution.
* [DeepSWE recipe](https://github.com/coreweave/cwsandbox-recipes/tree/main/recipes/deepswe): review the adapter, tests, and sampling options.
* [SWE-bench evaluation](https://docs.coreweave.com/products/sandboxes/client/guides/swebench.md): evaluate existing patches on a different benchmark.
* [Cleanup patterns](https://docs.coreweave.com/products/sandboxes/client/guides/cleanup-patterns.md): manage sandbox lifecycles in your own applications.
