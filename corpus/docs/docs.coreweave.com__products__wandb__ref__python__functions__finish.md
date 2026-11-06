# finish()

Source: https://docs.coreweave.com/products/wandb/ref/python/functions/finish

# finish()

[View source](https://github.com/wandb/wandb/blob/main/wandb/sdk/wandb_run.py#L4105)

## function wandb.finish()

Finish a run and upload any remaining data.

Marks the completion of a W\&B run and ensures all data is synced to the server.
The run's final state is determined by its exit conditions and sync status.

Run States:

* Running: Active run that is logging data and/or sending heartbeats.
* Crashed: Run that stopped sending heartbeats unexpectedly.
* Finished: Run completed successfully (`exit_code=0`) with all data synced.
* Failed: Run completed with errors (`exit_code!=0`).

```python theme={"system"}
exit_code: 'int | None' = None
```

## Args

**exit\_code** `int | None`

Integer indicating the run's exit status. Use 0 for success, any other value marks the run as failed.

## Returns

None
