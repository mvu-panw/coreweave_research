# Run pull request checks in sandboxes

Source: https://docs.coreweave.com/products/sandboxes/tutorials/github-actions

# Run pull request checks in sandboxes

> Run repository tests in CoreWeave sandboxes from GitHub Actions, with optional advisory AI review.

Run pull request tests in a fresh CoreWeave sandbox while GitHub Actions handles orchestration and reporting. This tutorial is for developers who already use GitHub Actions. You run repository code and dependencies outside the continuous integration (CI) runner.

You run a sample locally, test a public repository at a specific commit, and install a workflow that reports test results on pull requests. The [GitHub Actions recipe](https://github.com/coreweave/cwsandbox-recipes/tree/main/recipes/github-actions) contains the complete script, workflow, sample project, and tests. You can copy the recipe into another repository and run it independently.

The orchestrator, either your machine or the CI runner, keeps the CoreWeave credential and creates one serverless sandbox per run. The sandbox fetches public source code and runs the test command. An optional AI review sends the diff and test output to Anthropic from the orchestrator. The recipe doesn't pass API keys into the sandbox.

## Prerequisites

Before you start, prepare the following:

* A CoreWeave API access token with the `sandbox_user` Identity and Access Management (IAM) action. See [Manage API access tokens](https://docs.coreweave.com/security/authn-authz/manage-api-access-tokens.md).
* Serverless sandbox access and capacity for 1 CPU and 2 GiB of memory. See [Get started](https://docs.coreweave.com/products/sandboxes/get-started.md).
* [Git](https://git-scm.com/downloads), [`uv`](https://docs.astral.sh/uv/getting-started/installation/), and Python 3.11 or later. You can use `uv` to install Python.
* A public GitHub repository where you can add a workflow and an Actions secret.
* An [Anthropic API key](https://console.anthropic.com/settings/keys) (Optional) for advisory AI review.

The script stops the sandbox when it finishes, and each sandbox has a maximum lifetime. For the lifetime and other limits, see [Results and limits](https://github.com/coreweave/cwsandbox-recipes/tree/main/recipes/github-actions#results-and-limits) in the recipe README. AI review also consumes Anthropic API usage.

This recipe uses a CoreWeave API access token explicitly. For authentication options, see [Choose and get credentials](https://docs.coreweave.com/products/sandboxes/placement.md#choose-and-get-credentials).

## Run the sample

Use the bundled sample to verify authentication, remote execution, and cleanup before you connect your repository.

1. Clone the recipes repository and install the locked dependencies:

   ```bash theme={"system"}
   git clone https://github.com/coreweave/cwsandbox-recipes.git
   cd cwsandbox-recipes/recipes/github-actions
   uv sync --locked
   ```

2. Set your CoreWeave token. Replace `[API-ACCESS-TOKEN]` with your token's secret value:

   ```bash theme={"system"}
   export CWSANDBOX_API_KEY="[API-ACCESS-TOKEN]"
   ```

3. Run the sample and inspect its result:

   ```bash theme={"system"}
   uv run --locked python run.py
   cat outputs/result.json
   ```

   Expect `Status: passed` in the terminal. The result file records `returncode: 0` and `stopped: true`. The sample checks addition and verifies that the sandbox environment doesn't contain the orchestrator's CoreWeave, GitHub, or Anthropic keys.

4. Verify the failure path:

   ```bash theme={"system"}
   uv run --locked python run.py \
     --command 'python -c "raise SystemExit(7)"' \
     --output outputs/failure
   ```

   This command intentionally exits with status `1`. The result file records `status: failed`, the test's `returncode: 7`, and `stopped: true`.

## Test a repository commit

From the recipe directory, fetch a fixed MarkupSafe commit, install dependencies, and run `pytest` inside the sandbox:

```bash theme={"system"}
uv run --locked python run.py \
  --repo pallets/markupsafe \
  --head b2e4d9c7687be25695fffbe93a37622302b24fb1 \
  --command 'pip install . pytest==8.4.2 && python -m pytest -q' \
  --timeout 300 \
  --output outputs/repository
```

Expect `Status: passed`. For your project, replace the repository, full commit hash, and test command. To fail the check if dependency installation fails, use `&&` between the installation and test commands.

The recipe uses `python:3.12-bookworm`. If your project requires another toolchain, change the `container_image` setting in the `run.py` file.

The recipe checks out the head commit itself. It doesn't test GitHub's synthetic merge commit. The orchestration script runs on the local machine or CI runner. The repository checkout and test command execute in the sandbox.

### Optional: Add an AI review

In the orchestrator's environment, set the `ANTHROPIC_API_KEY` environment variable, then add `--base [BASE-COMMIT-SHA] --review` to your repository command. Replace `[BASE-COMMIT-SHA]` with the full 40-character commit hash of the base revision in the same repository. The recipe README includes a complete runnable example.

The script fetches both revisions and computes `git diff BASE...HEAD`. It sends the diff, standard output, and standard error to Anthropic, each truncated to a fixed size. The model has no tools. The script saves its response as advisory text for human review. If the review request fails, the `review_error` field records the error type and the test outcome remains unchanged.

## Add the GitHub Actions workflow

Use this workflow for trusted repository contributors. The workflow definition comes from the pull request's merge ref. A same-repository pull request can therefore change the workflow, test command, checkout ref, and use of secrets. Even if you check out base-branch files, the pull request can still make those changes.

Keep the `pull_request` trigger. If you change it to `pull_request_target`, you need a separate security design.

To run these checks on pull requests, install the recipe in your public repository:

1. From the root of your public repository, copy the runtime files and workflow. Replace `[RECIPES-CHECKOUT]` with the path to your recipes clone:

   ```bash theme={"system"}
   recipe_dir="[RECIPES-CHECKOUT]/recipes/github-actions"
   mkdir -p ci/sandbox .github/workflows
   cp "$recipe_dir/run.py" "$recipe_dir/pyproject.toml" \
     "$recipe_dir/uv.lock" "$recipe_dir/.gitignore" ci/sandbox/
   cp "$recipe_dir/workflow.yml" .github/workflows/sandbox-ci.yml
   ```

   Leave the recipe's `tests/` and `sample/` directories in the recipes clone so your project's test runner doesn't collect them. The copied files support repository mode. Run the bundled sample from the recipes clone. If the copied script fails to run, compare the file list with [Add to GitHub Actions](https://github.com/coreweave/cwsandbox-recipes/tree/main/recipes/github-actions#add-to-github-actions) in the recipe README.
2. Review the copied [`workflow.yml` file](https://github.com/coreweave/cwsandbox-recipes/blob/main/recipes/github-actions/workflow.yml) at `.github/workflows/sandbox-ci.yml`.
3. Set the workflow's `--command` to your project's dependency installation and test command.
4. Add an Actions repository secret named `CWSANDBOX_API_KEY` containing your CoreWeave token. See [Using secrets in GitHub Actions](https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/use-secrets).
5. Merge the workflow and `ci/sandbox/` files into your target base branch. The workflow loads orchestration from the pull request's base commit. Before you test a pull request, those files must exist there.
6. Open or update a same-repository pull request.

The **Sandbox CI** workflow runs on `opened`, `synchronize`, and `reopened` events. The supplied workflow checks out the `run.py` file and its dependency files from the base commit. It passes the pull request's head commit hash to the sandbox. It requests `contents: read` permission and disables persisted checkout credentials.

The supplied workflow skips fork pull requests, Dependabot pull requests, and private repositories. GitHub doesn't provide repository secrets to fork or Dependabot pull request workflows. A skipped job satisfies a required status check, so requiring this check doesn't enforce tests for skipped pull requests. See [Handling skipped but required checks](https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/troubleshooting-required-status-checks#handling-skipped-but-required-checks).

For optional AI review in Actions, follow the recipe's instructions to add the Anthropic secret to the test step and enable `--review`.

## Inspect the results

To read the job summary, open the **Sandbox CI** check. Download the **`sandbox-ci-results`** artifact for the `result.json` and `summary.md` files. The workflow uploads results even when tests fail. The `retention-days` setting in the workflow controls how long artifacts remain available.

The result file includes the tested commit, sandbox ID, test return code, captured output, and cleanup outcome. The script keeps the end of standard output and standard error, where failure messages usually appear. It escapes returned text in the summary and doesn't print test output directly to the CI runner console. On failure, a fixed-text error annotation points to the job summary and artifact.

A successful test run exits `0`. Failed tests, setup errors, timeouts, and cleanup errors exit `1`. AI review is advisory and doesn't change that result. A passing test suite isn't a security assessment of the submitted code.

The `--timeout` option sets the test command's timeout. Setup commands, sandbox startup, the sandbox lifetime, and the runner job each have a separate limit. For default and maximum values, and for the stored output size, see [Results and limits](https://github.com/coreweave/cwsandbox-recipes/tree/main/recipes/github-actions#results-and-limits) in the recipe README.

The recipe buffers command output before truncation, so use it for small repositories and test suites with limited output. On timeout, the script records `status: error` and `error: SandboxTimeoutError` without partial command output.

## Clean up

The script calls `stop(missing_ok=True)` in a `finally` block after successful and failed runs. The maximum lifetime limits execution if the orchestrator is terminated before cleanup. The recipe creates no snapshots, volumes, or sandbox runners.

If the `cleanup_error` field appears in the result, use the recipe's cleanup command with the saved sandbox ID and the same CoreWeave credential to delete it. For more patterns, see [Cleanup patterns](https://docs.coreweave.com/products/sandboxes/client/guides/cleanup-patterns.md).

Keep any result files you need, then remove the local `outputs/` directory. When you no longer want pull requests to create sandboxes, remove or disable the workflow.
