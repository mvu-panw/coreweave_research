# results

Source: https://docs.coreweave.com/products/sandboxes/client/ref/utilities/results

# results

> Block for one or more OperationRefs and return results.

Source: [src/cwsandbox/**init**.py:144](https://github.com/coreweave/cwsandbox-client/blob/v1.14.2/src/cwsandbox/__init__.py#L144)

```python theme={"system"}
results(ref: OperationRef[T], /) -> T
```

```python theme={"system"}
results(refs: Sequence[OperationRef[T]], /) -> list[T]
```

Block for one or more OperationRefs and return results.

This is a convenience function for retrieving results from OperationRefs.
For a single ref, returns the result directly. For a sequence of refs,
returns a list of results in the same order.
**Parameters**

* `refs` (`OperationRef[T] | Sequence[OperationRef[T]]`): A single OperationRef or a sequence of OperationRefs.

**Returns**

* `T | list[T]`: The result(s) from the operation(s).

**Raises**

* `Exception`: Any exception raised by the underlying operation(s).

**Examples**

Single ref:

```python theme={"system"}
data = cwsandbox.results(sandbox.read_file("/path"))
```

Multiple refs:

```python theme={"system"}
all_results = cwsandbox.results([sb.read_file(f) for f in files])
```
