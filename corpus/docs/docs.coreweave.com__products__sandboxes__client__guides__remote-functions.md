# Remote functions

Source: https://docs.coreweave.com/products/sandboxes/client/guides/remote-functions

# Remote functions

> Execute Python functions inside sandboxes with the function decorator.

This guide covers the `@session.function()` decorator for running Python functions in sandboxes. It's intended for developers who want to offload individual Python computations to isolated environments without managing a sandbox lifecycle directly, and explains how to define remote functions, which argument and return types the API supports, and when this API is the right fit.

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

## Overview

The function decorator API lets you execute Python functions in isolated sandbox containers. Use it when you want to run discrete Python work remotely while keeping your calling code simple:

```python theme={"system"}
from sandbox_auth import AUTH
import cwsandbox
from cwsandbox import SandboxDefaults

with cwsandbox.Session(SandboxDefaults(
    container_image="python:3.11",
    resources={"cpu": "1", "memory": "1Gi"},
), auth=AUTH) as session:
    @session.function()
    def compute(x: int, y: int) -> int:
        return x + y

    # Execute in sandbox
    result = compute.remote(2, 3).result()
    print(result)  # 5
```

## Basic usage

### Define functions

Decorate functions with `@session.function()`:

```python theme={"system"}
@session.function()
def process_data(data: dict) -> dict:
    # Code runs inside the sandbox
    import pandas as pd
    df = pd.DataFrame(data)
    return {"mean": df["value"].mean()}
```

### Call functions

Call `.remote()` on the decorated function to execute in the sandbox:

```python theme={"system"}
# Returns OperationRef immediately
ref = compute.remote(2, 3)

# Block for result
result = ref.result()

# One-liner
result = compute.remote(2, 3).result()
```

## Execution methods

### Run in parallel with map()

Execute across multiple inputs:

```python theme={"system"}
@session.function()
def square(x: int) -> int:
    return x * x

# Execute for each input
refs = square.map((x,) for x in range(10))

# Collect all results
from cwsandbox import results
all_results = results(refs)  # [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
```

With tuples for multiple arguments:

```python theme={"system"}
@session.function()
def add(x: int, y: int) -> int:
    return x + y

# Each tuple is unpacked as arguments
refs = add.map([(1, 2), (3, 4), (5, 6)])
all_results = results(refs)  # [3, 7, 11]
```

### Run locally with local()

Run locally without a sandbox, which is useful for testing:

```python theme={"system"}
# No sandbox created - runs in current process
result = compute.local(2, 3)
print(result)  # 5
```

## Argument and return types

Remote functions transfer arguments and return values as JSON. Both must be JSON-serializable: dictionaries, lists, strings, numbers, booleans, and `None`.

```python theme={"system"}
@session.function()
def process(data: dict) -> dict:
    return {"result": data["value"] * 2}
```

If you pass an argument that JSON can't represent, the call raises `TypeError` before the sandbox starts:

```text title="Example output" theme={"system"}
TypeError: Function arguments are not JSON-serializable: Object of type ndarray is not JSON serializable
```

A return value that JSON can't represent fails the same way, with the message `return value is not JSON-serializable`.

JSON objects support string keys only. A dictionary keyed by integers, floats, or booleans is rejected rather than converted, so the types your function receives in the sandbox match the types you passed.

To work with NumPy arrays, pandas DataFrames, or custom class instances, convert them to JSON-compatible values before you call the function, then reconstruct them inside it:

```python theme={"system"}
@session.function()
def array_mean(values: list[float]) -> float:
    from statistics import fmean
    return fmean(values)

result = array_mean.remote([1.0, 2.0, 3.0, 4.0, 5.0]).result()  # 3.0
```

The client installs nothing before it runs your function. Any library the function imports, such as NumPy, must already be in the container image.

For data too large to pass as JSON, write it to storage the sandbox can reach and pass a reference instead. See [File operations](https://docs.coreweave.com/products/sandboxes/client/guides/file-operations.md).

## Closures and globals

### Closure variables

Functions capture variables from their enclosing scope:

```python theme={"system"}
multiplier = 10

@session.function()
def multiply(x: int) -> int:
    return x * multiplier  # Captures 'multiplier'

result = multiply.remote(5).result()  # 50
```

### Global variables

The decorator serializes referenced globals with the function:

```python theme={"system"}
CONFIG = {"threshold": 0.5}

@session.function()
def check_value(x: float) -> bool:
    return x > CONFIG["threshold"]

result = check_value.remote(0.7).result()  # True
```

Captured closure variables and globals are transferred to the sandbox as JSON, the same as arguments and return values. If a function captures a value that JSON can't represent, the call fails for that reason, even when every argument you pass is valid.

## Container image

Override the container image for specific functions:

```python theme={"system"}
@session.function(container_image="pytorch/pytorch:latest")
def train_model(data: dict) -> dict:
    import torch
    # GPU training code
    return {"loss": 0.01}
```

## Error handling

Function exceptions propagate to the caller:

```python theme={"system"}
@session.function()
def failing_function() -> None:
    raise ValueError("Something went wrong")

try:
    failing_function.remote().result()
except Exception as e:
    print(f"Function failed: {e}")
```

## When to use functions compared to sandboxes

Use the following table to decide whether the function decorator API or the sandbox API is a better fit for your workload.

| Use case | Recommended API |
| - | - |
| Simple Python computation | Function decorator |
| Map/reduce over data | Function decorator |
| Interactive workflow, multiple commands | Sandbox |
| Streaming output | Sandbox |
| File manipulation | Sandbox |
| Long-running processes | Sandbox |

## Limitations

The function API is intentionally simple. For complex workflows:

* **Retries and backoff**: Implement in calling code.
* **Task dependencies and DAGs**: Use a workflow orchestrator such as Airflow or Prefect.
* **Complex scheduling**: Use the sandbox API directly.

## Complete example

The following example combines the concepts in this guide. It shows single and parallel execution, and a computation whose argument and return value pass as JSON:

```python theme={"system"}
from sandbox_auth import AUTH
import cwsandbox
from cwsandbox import SandboxDefaults, results

defaults = SandboxDefaults(
    container_image="python:3.11",
    tags=("remote-functions-demo",),
    resources={"cpu": "1", "memory": "1Gi"},
)

with cwsandbox.Session(defaults=defaults, auth=AUTH) as session:
    @session.function()
    def square(x: int) -> int:
        return x * x

    # The argument is a list and the result a float, so both pass as JSON
    @session.function()
    def array_mean(values: list[float]) -> float:
        from statistics import fmean
        return fmean(values)

    # Single execution
    result = square.remote(7).result()
    print(f"7 squared: {result}")

    # Parallel execution
    refs = square.map((x,) for x in range(5))
    all_results = results(refs)
    print(f"Squares: {all_results}")

    # JSON-compatible computation
    mean = array_mean.remote([1.0, 2.0, 3.0, 4.0, 5.0]).result()
    print(f"Array mean: {mean}")
```
