# SWE-bench

Source: https://docs.coreweave.com/products/sandboxes/client/guides/swebench

# SWE-bench

> Run SWE-bench evaluations using CoreWeave sandboxes.

Run SWE-bench evaluations in parallel using sandboxes on CoreWeave. This guide is for ML practitioners and researchers who want to evaluate language model code-fixing performance at scale. By the end, you have a working setup that runs SWE-bench evaluations concurrently across many CoreWeave sandboxes, with results written locally for analysis.

## What this does

[SWE-bench](https://www.swebench.com/) tests whether language models can fix real bugs in real repositories. Each task applies a patch, runs the test suite, and checks if the fix works.

You can run SWE-bench locally with Docker, but your machine's resources limit you. CoreWeave sandboxes let you run evaluations at scale on CoreWeave infrastructure. Spin up dozens or hundreds of sandboxes concurrently without managing any of it yourself. Each sandbox starts from a pre-built image in Epoch AI's registry on GitHub Container Registry (GHCR). The sandbox platform pulls the image, not your machine, so you don't need Docker or a local build step.

## Setup

Complete the following steps to install the required tools and configure authentication before running any evaluations.

1. Prepare and activate a [Python virtual environment](https://docs.coreweave.com/products/sandboxes/client.md#prepare-your-python-environment), then install the evaluation dependencies. Keep this environment active for all commands in this guide:

   ```bash theme={"system"}
   uv pip install 'swebench==4.1.0' datasets
   ```

2. Clone the repo for the example evaluation scripts:

   ```bash theme={"system"}
   git clone https://github.com/coreweave/cwsandbox-client.git
   cd cwsandbox-client
   ```

Choose the credential for the account that owns your sandboxes. To obtain a Forge API key or CoreWeave API access token, see [Choose and get credentials](https://docs.coreweave.com/products/sandboxes/placement.md#choose-and-get-credentials).

Run the installation commands in an [active Python virtual environment](https://docs.coreweave.com/products/sandboxes/client.md#prepare-your-python-environment).

Save the Python code from your credential tab as a `sandbox_auth.py` file beside the Python script that uses it. This file stores only the authentication choice. Import `AUTH` from that file. When you create a sandbox or session, pass `AUTH` explicitly or set it in `SandboxDefaults`.

> [tab] Forge API key
>
> Use your Forge API key with the `wandb` integration in the software development kit (SDK). Replace `[WANDB-API-KEY]` with your API key:
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
> Use the CoreWeave API access token for your organization. Replace `[API-ACCESS-TOKEN]` with your token:
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

The examples use serverless capacity unless a section specifies CoreWeave Kubernetes Service (CKS). For CKS placement, choose a CoreWeave API access token and [enable a runner](https://docs.coreweave.com/products/sandboxes/get-started-cks.md). Set `placement_mode="cks"` when you create a sandbox or in `SandboxDefaults`.

To authenticate a session and the sandboxes it owns, create the session with `auth=AUTH`. When you reconnect, list, or clean up sandboxes, keep the same credential.

Save the `sandbox_auth.py` file in the `examples/swebench/` directory. In the `examples/swebench/run_evaluation.py` file, add `from sandbox_auth import AUTH` to the imports and `auth=AUTH` to the existing `SandboxDefaults(...)` call. This applies your authentication choice to every sandbox in the evaluation session.

For CKS placement, add `placement_mode="cks"` to the same call.

## Quick start

Before you scale up, start with a single-instance run to confirm that your environment and credentials work and that a sandbox can start from its GHCR image. The `gold` option uses the known-correct fix from the dataset:

```bash theme={"system"}
python examples/swebench/run_evaluation.py \
    --predictions-path gold \
    --instance-ids astropy__astropy-12907 \
    --run-id test
```

With working infrastructure and the expected image and test environment, this gold-patch run is expected to resolve the instance. A resolved result confirms that the harness can start a sandbox, apply the patch, run the tests, and grade this instance. Use the gold run as a harness confidence check, not a guarantee that every evaluation succeeds. If an instance fails or errors, [inspect its results](#inspect-failed-or-errored-instances).

### Run in parallel

Run multiple instances at once:

```bash theme={"system"}
python examples/swebench/run_evaluation.py \
    --predictions-path gold \
    --instance-ids \
        astropy__astropy-12907 \
        django__django-11039 \
        django__django-11099 \
        django__django-11283 \
        matplotlib__matplotlib-23476 \
        scikit-learn__scikit-learn-13142 \
        sympy__sympy-13031 \
        sympy__sympy-13647 \
    --run-id parallel-test \
    --max-workers 8
```

This command runs up to eight instance evaluations concurrently. When the infrastructure and test environments work, gold patches are expected to resolve these instances. Individual evaluations can still fail or error.

### Evaluate model predictions

To test custom model output:

```bash theme={"system"}
python examples/swebench/run_evaluation.py \
    --predictions-path predictions.json \
    --instance-ids django__django-11039 scikit-learn__scikit-learn-13142 \
    --run-id eval-run-1 \
    --max-workers 10
```

The predictions file maps instance IDs to patches:

```json theme={"system"}
[
  {
    "instance_id": "django__django-11039",
    "model_name_or_path": "gpt-4",
    "model_patch": "diff --git a/..."
  }
]
```

## Options

| Option | Default | Description |
| - | - | - |
| `--predictions-path` | Required | Path to predictions JSON, or `gold` for gold patches |
| `--instance-ids` | Required | Space-separated instance IDs |
| `--run-id` | Required | Identifier for this run |
| `--max-workers` | 10 | Max parallel sandboxes |
| `--timeout` | 1800 | Per-instance timeout in seconds (30 minutes) |
| `--output-dir` | `logs/swebench` | Where to write logs and reports |
| `--dataset` | `princeton-nlp/SWE-bench_Lite` | Hugging Face dataset name |
| `--force` | false | Re-run instances even if report.json exists |

### Adjust resources

The `resources` argument controls CPU and memory per sandbox. The default is 2 CPUs and `4Gi` memory. In the `examples/swebench/run_evaluation.py` file, replace only the `resources` value in the existing `SandboxDefaults(...)` call. Use this dictionary:

```python theme={"system"}
{"cpu": "4", "memory": "8Gi"}
```

Keep `auth=AUTH`, any `placement_mode="cks"` setting, and the other arguments in that call.

## How it works

This section explains the moving parts behind the script so you can adapt it to your own evaluation workflows.

### Container images

Epoch AI hosts pre-built images on GHCR. Each instance has its own image with the repository checked out at the right commit, dependencies installed, and test environment ready.

The image name has this format: `ghcr.io/epoch-research/swe-bench.eval.{arch}.{instance_id.lower()}:latest`

The script lowercases the instance ID for the image name. It takes `arch` from the test specification's `arch` attribute. If that attribute is absent, the script uses `x86_64`.

The sandbox platform pulls each image from GHCR when it starts the sandbox. On your own CKS capacity, your cluster's Nodes do the pull. Your machine needs no access to `ghcr.io`, and no local builds are needed.

### Evaluation flow

Each instance goes through these steps:

| Step | Where | What happens |
| - | - | - |
| 1. Load dataset | Local | Fetch instance metadata from Hugging Face |
| 2. Create sandbox | Sandbox | Start sandbox with the instance's image |
| 3. Write patch | Sandbox | Write patch to `/tmp/patch.diff` |
| 4. Apply patch | Sandbox | Run `git apply` (falls back to `patch` if needed) |
| 5. Run tests | Sandbox | Execute `/root/eval.sh` |
| 6. Grade results | Local | Parse output with `swebench.harness.grading` |
| 7. Write report | Local | Save results to `logs/swebench/` |
| 8. Cleanup | Sandbox | Stop sandbox |

Steps 2 to 5 and 8 run remotely. Steps 1, 6, and 7 run on your machine.

### Parallel execution

The script uses `ThreadPoolExecutor` to run instance workflows concurrently. Each thread drives one instance through its workflow. While one instance runs tests, another can apply its patch, another grade locally, another start up. The overlap is where the speed comes from.

Results come back as workflows finish through `as_completed()`.

### Cleanup

The script uses a sandbox `Session` to track sandboxes. When the session exits (normal exit, exception, or `Ctrl+C`), the session cleans up all sandboxes.

```python theme={"system"}
with cwsandbox.Session(defaults=defaults) as session:
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # The session cleans up sandboxes created here when it exits
```

## Output

Results go to `{output-dir}/{run-id}/{model-name}/{instance-id}/`:

| File | Contents |
| - | - |
| `report.json` | Resolved status, sandbox ID, duration, and the error for an instance that errored |
| `test_output.txt` | Full test output |
| `patch.diff` | The applied patch |

### Report format

This simplified example shows a resolved result with test-status details. When present, `tests_status` groups test names by transition category, with `success` and `failure` arrays in each category. The grader can return before producing these details, so `tests_status` can be absent.

```json theme={"system"}
{
  "instance_id": {
    "resolved": true,
    "tests_status": {
      "FAIL_TO_PASS": {
        "success": ["test_foo"],
        "failure": []
      },
      "PASS_TO_PASS": {
        "success": ["test_bar"],
        "failure": []
      },
      "FAIL_TO_FAIL": {
        "success": [],
        "failure": []
      },
      "PASS_TO_FAIL": {
        "success": [],
        "failure": []
      }
    }
  },
  "sandbox_id": "sandbox-abc123",
  "duration_seconds": 45.2
}
```

When an instance errors, for example because its sandbox fails to start, `report.json` also contains `"errored": true` and an `error_message` string. It can omit the test results and `sandbox_id`.

The format is compatible with standard SWE-bench tooling.

### Inspect failed or errored instances

Check the script's per-instance `Complete:` log messages, then open the corresponding `report.json` file in the instance's output directory. For the single-instance quick start, the default path is `logs/swebench/test/gold/astropy__astropy-12907/report.json`.

* `Complete: failed`: the instance wasn't resolved. Inspect its `resolved` value and any available test-status details in the `report.json` file, then read the `test_output.txt` file for the test output.
* `Complete: error`: read `error_message` in the `report.json` file, which also records `"errored": true`. Image pulls, sandbox startup, patch application, or test execution can fail even with gold patches. If the `test_output.txt` file exists, check it. Failures before tests run can leave no test output file.

## Troubleshooting

### Patch application fails

If you see `APPLY_PATCH_FAIL` in logs, the patch is probably malformed, targets the wrong commit, or has whitespace issues. Run `git apply --check` locally to see what's wrong. Make sure the instance ID matches the prediction.

### Test timeouts

Some test suites take longer than 30 minutes. Model-generated code might also have infinite loops. If needed, increase `--timeout`, or check the test output to see where it's stuck.

### Image pull errors

If the sandbox platform can't pull an instance's image, that sandbox fails to start. The script logs the error with the instance ID, such as `[astropy__astropy-12907] Error: ...`, and records it in the `error_message` field of that instance's `report.json`. The pull runs on CoreWeave infrastructure, not on your machine, so your local network access to `ghcr.io` isn't the cause. Read the error message, then check the likely causes:

* **Image not found:** verify that Epoch AI publishes an image for the instance ID. An instance ID that isn't in the `--dataset` dataset never reaches a sandbox: the script logs `Instance IDs not found in dataset` and skips it.
* **Your own CKS capacity:** if you set `placement_mode="cks"`, your cluster's Nodes pull the image, so they need outbound access to `ghcr.io`. The runner's [sandbox policy](https://docs.coreweave.com/products/sandboxes/profiles/configure.md#constrain-images) must also allow images from `ghcr.io/epoch-research`.

## See also

* [Command execution guide](https://docs.coreweave.com/products/sandboxes/client/guides/execution.md): details about `exec()` patterns.
* [Cleanup patterns](https://docs.coreweave.com/products/sandboxes/client/guides/cleanup-patterns.md): managing sandbox lifecycle.
