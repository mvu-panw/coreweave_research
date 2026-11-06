# Stream real-time output from a sandbox

Source: https://docs.coreweave.com/products/sandboxes/client/tutorial/streaming

# Stream real-time output from a sandbox

> Stream command output in real time from a sandbox.

This tutorial shows how to stream command output from a sandbox as it's produced, instead of waiting for the command to finish. Streaming is useful when you want to display progress, monitor long-running commands, or react to output incrementally.

The following example runs a short loop in the sandbox and prints each line as it arrives:

```python theme={"system"}
process = sandbox.exec(["bash", "-c", "for i in 1 2 3; do echo $i; sleep 1; done"])

for line in process.stdout:
    print(line, end="")

result = process.result()
```

> [!NOTE]
>
> To stream output in real time, iterate over `process.stdout` before you call `.result()`. If you only need the final output, skip the iteration and access it through `result.stdout` after you call `.result()`.

For more streaming patterns, see the [Execution guide](https://docs.coreweave.com/products/sandboxes/client/guides/execution.md).
