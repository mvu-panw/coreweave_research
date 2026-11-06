# Files

Source: https://docs.coreweave.com/products/wandb/ref/python/public-api/files

# Files

[View source](https://github.com/wandb/wandb/blob/main/wandb/apis/public/files.py#L79)

## Class wandb.apis.public.Files

A lazy iterator over a collection of `File` objects.

Access and manage files uploaded to W\&B during a run. Handles pagination
automatically when iterating through large collections of files.

```python theme={"system"}
(service_api: 'ServiceApi',
run: 'Run',
names: 'list[str] | None' = None,
per_page: 'int' = 50,
upload: 'bool' = False,
pattern: 'str | None' = None)
```

## Args

**service\_api** `ServiceApi`

The service API instance to use for querying W\&B.

**run** `Run`

The run object that contains the files

**names** `list[str] | None`

A list of file names to filter the files

**per\_page** `int`

The number of files to fetch per page

**upload** `bool`

If `True`, fetch the upload URL for each file

**pattern** `str | None`

Pattern to match when returning files from W\&B This pattern uses mySQL's LIKE syntax, so matching all files that end with .json would be "%.json". If both names and pattern are provided, a ValueError will be raised.

## Examples

```python theme={"system"}
from wandb.apis.public.files import Files
from wandb.apis.public.api import Api

# Example run object
run = Api().run("entity/project/run-id")

# Get the files for the run
files = run.files()

# Iterate over files
for file in files:
    print(file.name)
    print(file.url)
    print(file.size)

    # Download the file
    file.download(root="download_directory", replace=True)
```

## Methods

### method Paginator.**next**()

```python theme={"system"}
self
```

Return the next item from the iterator. When exhausted, raise StopIteration
