# teardown()

Source: https://docs.coreweave.com/products/wandb/ref/python/functions/teardown

# teardown()

[View source](https://github.com/wandb/wandb/blob/main//Users/noahluna/.pyenv/versions/3.13.0/lib/python3.13/contextlib.py#L571)

## function wandb.teardown()

Waits for W\&B to finish and frees resources.

Completes any runs that were not explicitly finished
using `run.finish()` and waits for all data to be uploaded.

It is recommended to call this at the end of a session
that used `wandb.setup()`. It is invoked automatically
in an `atexit` hook, but this is not reliable in certain setups
such as when using Python's `multiprocessing` module.

```python theme={"system"}
exit_code: 'int | None' = None
```

## Args

**exit\_code** `int | None`

No description provided.

## Returns

None
