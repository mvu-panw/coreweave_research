# Implement a warm pool

Source: https://docs.coreweave.com/products/sandboxes/warm-pools

# Implement a warm pool

> Keep sandboxes ready for incoming work using a Python warm pool recipe.

Use a warm pool when requests need a running sandbox without waiting for one to
start. The [warm pool recipe](https://github.com/coreweave/cwsandbox-recipes/tree/main/recipes/warm-pool) maintains a buffer of prepared sandboxes,
assigns each workload its own sandbox, and replenishes the buffer in the background.
Idle sandboxes consume compute while waiting for work.

## How the pool works

The recipe's `WarmPool` helper starts the configured number of sandboxes and runs
a readiness check in each. Their main processes stay running between commands.
No periodic ping is needed.

Each workload claims one ready sandbox, triggering preparation of a replacement.
Every `exec()` within that claim shares the same sandbox and files. When the
workload finishes or fails, the helper stops its sandbox. Subsequent workloads
receive separate sandboxes, so they don't inherit previous workloads' local state.

## Run the recipe

You need Python 3.11+, [`uv`](https://docs.astral.sh/uv/getting-started/installation/),
and [serverless access and credentials](https://docs.coreweave.com/products/sandboxes/get-started.md#run-a-sandbox-on-serverless-capacity).

1. Download or clone the [recipe repository](https://github.com/coreweave/cwsandbox-recipes/tree/main/recipes/warm-pool) and open
   `recipes/warm-pool`. Install dependencies and create your environment file:

   ```bash theme={"system"}
   uv sync --frozen
   cp .env.example .env
   ```

2. Configure your credential in `.env` and near the top of `demo.py`:

   > [tab] Forge API key
   >
   > Add your Forge API key to `.env`:
   >
   > ```bash theme={"system"}
   > WANDB_API_KEY="[WANDB-API-KEY]"
   > ```
   >
   > In `demo.py`, add the following imports and replace the existing `AUTH` assignment:
   >
   > ```python theme={"system"}
   > import os
   > from cwsandbox import AuthHeaders
   >
   > AUTH = AuthHeaders(
   >     headers={"x-wandb-api-key": os.environ["WANDB_API_KEY"]},
   >     strategy="wandb_api_key",
   > )
   > ```
   >
   > This reads `WANDB_API_KEY` explicitly and uses the SDK's supported authentication headers. The header and strategy names are compatibility identifiers; the credential is a Forge API key. No optional `wandb` dependency is needed.

   > [tab] CoreWeave API access token
   >
   > Add your token to `.env`:
   >
   > ```bash theme={"system"}
   > CWSANDBOX_API_KEY="[API-ACCESS-TOKEN]"
   > ```
   >
   > Keep the recipe's default `AUTH` setting:
   >
   > ```python theme={"system"}
   > from cwsandbox import AuthStrategy
   >
   > AUTH = AuthStrategy.COREWEAVE_API_KEY
   > ```

3. Run the comparison:

   ```bash theme={"system"}
   uv run --frozen --env-file .env demo.py
   ```

The demo compares four requests using on-demand creation with four using the pool.
It reports initial pool preparation separately from request timings and checks
that every workload receives a distinct sandbox. Expect this final message:

```text theme={"system"}
Verified 8 distinct workload sandboxes; all sandboxes stopped.
```

## Adapt the pool to your workload

Edit the constants in `demo.py`:

```python theme={"system"}
POOL_SIZE = 2     # Target number of idle sandboxes.
CONCURRENCY = 2   # Maximum active workloads.
REQUESTS = 4      # Requests per comparison mode.
```

These defaults allow up to four sandboxes at once: two buffer sandboxes in
addition to two active workloads. Each sandbox requests 2 vCPU and 4 GiB RAM.
If the buffer empties, requests wait for replenishment. If the active limit is
reached, they wait for a workload to finish. Measure with your own arrival pattern
before increasing the buffer.

Replace `WORKLOAD` in `demo.py` with your code. Add shared setup to `prepare()` in
`warm_pool.py` and use a readiness check appropriate for your application. Within
an asynchronous workload handler, use the recipe's claim context for multiple
commands:

```python theme={"system"}
async with pool.claim() as sandbox:
    await sandbox.exec(["sh", "-c", "echo hello > /tmp/result.txt"], check=True)
    result = await sandbox.exec(["cat", "/tmp/result.txt"], check=True)
    print(result.stdout)
```

Collect outputs before leaving the claim. Supply customer inputs and credentials
after claiming, and scope shared external storage to the appropriate customer.

## Keep the pool running

Keep the pool and enclosing `Session` contexts open while accepting requests.
Each Python process owns a separate pool. The demo closes both after its comparison.

The helper replaces idle sandboxes at 5 minutes. Each sandbox has a 10-minute
lifetime. The pool continues replenishing while its context is open. Keep jobs
comfortably under 5 minutes with these defaults: claiming a sandbox doesn't
reset its deadline. For longer-job settings and cleanup after interrupted runs,
see the [recipe](https://github.com/coreweave/cwsandbox-recipes/tree/main/recipes/warm-pool).

Transient preparation failures get up to three attempts. If those attempts are
exhausted or preparation encounters a non-retryable error, all further claims fail,
even if ready sandboxes remain. Exit the pool and `Session` contexts to clean up,
then create a new pool when the underlying issue is resolved.

To shorten replenishment, build stable dependencies into your image or restore
prepared workspace files from a [file system snapshot](https://docs.coreweave.com/products/sandboxes/file-system-snapshots.md).
Snapshots capture files in the configured mount. Application processes still
start separately. A [sandbox template](https://docs.coreweave.com/products/sandboxes/profiles/templates.md)
can store the shared image and snapshot configuration.
