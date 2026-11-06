# File operations

Source: https://docs.coreweave.com/products/sandboxes/client/tutorial/files

# File operations

> Tutorial for uploading and downloading files to and from CoreWeave sandbox instances

```python theme={"system"}
# Write (content must be bytes)
sandbox.write_file("/tmp/hello.txt", b"Hello!").result()

# Read (returns bytes)
content = sandbox.read_file("/tmp/hello.txt").result()
print(content.decode())
```

Like `exec()`, file operations return an `OperationRef` immediately and don't wait for completion. Call `.result()` when you need the data. This lets you start multiple operations and wait for them together:

```python theme={"system"}
refs = [sandbox.write_file(f"/tmp/{i}.txt", b"data") for i in range(5)]
for ref in refs:
    ref.result()
```

For parallel upload and download patterns and S3 mounts, see the [File operations guide](https://docs.coreweave.com/products/sandboxes/client/guides/file-operations.md).
