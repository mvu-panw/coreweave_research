# File

Source: https://docs.coreweave.com/products/wandb/ref/python/public-api/file

# File

[View source](https://github.com/wandb/wandb/blob/main/wandb/apis/public/files.py#L246)

## Class wandb.apis.public.File

File saved to W\&B.

Represents a single file stored in W\&B. Includes access to file metadata.
Files are associated with a specific run and
can include text files, model weights, datasets, visualizations, and other
artifacts. You can download the file, delete the file, and access file
properties.

Specify one or more attributes in a dictionary to fine a specific
file logged to a specific run. You can search using the following keys:

* id (str): The ID of the run that contains the file
* name (str): Name of the file
* url (str): path to file
* direct\_url (str): path to file in the bucket
* sizeBytes (int): size of file in bytes
* md5 (str): md5 of file
* mimetype (str): mimetype of file
* updated\_at (str): timestamp of last update
* path\_uri (str): path to file in the bucket, currently only available for S3 objects and reference files

## Properties

**path\_uri** `The S3 URI (e.g., 's3://bucket/path/to/file') if the file is stored in S3, the direct URL if it's a reference file, or an empty string if unavailable.`

Returns the URI path to the file in the storage bucket.

**size** `int`

Returns the size of the file in bytes.

## Methods

### method File.delete()

```python theme={"system"}
self
```

Delete the file from the W\&B server.

### method File.download()

```python theme={"system"}
self,
root: 'str' = '.',
replace: 'bool' = False,
exist_ok: 'bool' = False,
api: 'Api | None' = None
```

Downloads a file previously saved by a run from the wandb server.

##### Arguments

**root** `str`

Local directory to save the file. Defaults to the current working directory (".").

**replace** `bool`

If `True`, download will overwrite a local file if it exists. Defaults to `False`.

**exist\_ok** `bool`

If `True`, will not raise ValueError if file already exists and will not re-download unless replace=True. Defaults to `False`.

**api** `Api | None`

If specified, the `Api` instance used to download the file.
