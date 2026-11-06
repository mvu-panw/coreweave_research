# Html

Source: https://docs.coreweave.com/products/wandb/ref/python/data-types/html

# Html

[View source](https://github.com/wandb/wandb/blob/main/wandb/sdk/data_types/html.py#L22)

## Class wandb.Html

W\&B class for logging HTML content to W\&B.

```python theme={"system"}
data: 'str | pathlib.Path | TextIO',
inject: 'bool' = True,
data_is_not_path: 'bool' = False
```

## Args

**data** `str | pathlib.Path | TextIO`

A string that is a path to a file with the extension ".html", or a string or IO object containing literal HTML.

**inject** `bool`

Add a stylesheet to the HTML object. If set to False the HTML will pass through unchanged.

**data\_is\_not\_path** `bool`

If set to False, the data will be treated as a path to a file.
