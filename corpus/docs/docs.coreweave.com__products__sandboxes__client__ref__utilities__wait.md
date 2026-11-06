# wait

Source: https://docs.coreweave.com/products/sandboxes/client/ref/utilities/wait

# wait

> Wait for waitables to complete, return (done, pending).

Source: [src/cwsandbox/**init**.py:176](https://github.com/coreweave/cwsandbox-client/blob/v1.14.2/src/cwsandbox/__init__.py#L176)

```python theme={"system"}
wait(waitables: Sequence[Waitable], num_returns: int | None = None, timeout: float | None = None) -> tuple[list[Waitable], list[Waitable]]
```

Wait for waitables to complete, return (done, pending).

Each waitable type has natural "wait for" behavior:

* Sandbox: waits until RUNNING status

* OperationRef: waits until operation completes

* Process: waits until process completes
  **Parameters**

* `waitables` (`Sequence[Waitable]`): Sequence of Sandbox, OperationRef, or Process objects.

* `num_returns` (`int | None`): If specified, return after this many complete. If None, wait for all to complete.

* `timeout` (`float | None`): Maximum seconds to wait. If None, wait forever.

**Returns**

* `tuple[list[Waitable], list[Waitable]]`: Tuple of (done, pending) lists containing the original waitable objects.

**Raises**

* `ValueError`: If num\_returns is less than 1.

**Examples**

Wait for all sandboxes to be running:

```python theme={"system"}
sandboxes = [Sandbox.run(...) for _ in range(5)]
done, pending = cwsandbox.wait(sandboxes)
```

Wait for first 2 operations to complete:

```python theme={"system"}
refs = [sb.read_file(f) for f in files]
done, pending = cwsandbox.wait(refs, num_returns=2)
```

Wait with timeout:

```python theme={"system"}
done, pending = cwsandbox.wait(procs, timeout=30.0)
```
