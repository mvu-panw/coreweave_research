# DownloadHistoryResult

Source: https://docs.coreweave.com/products/wandb/ref/python/public-api/downloadhistoryresult

# DownloadHistoryResult

[View source](https://github.com/wandb/wandb/blob/main/wandb/apis/public/runhistory/downloads.py#L26)

## Class wandb.apis.public.DownloadHistoryResult

Result of downloading a run's history exports.

```python theme={"system"}
paths: 'list[pathlib.Path]',
contains_live_data: 'bool',
errors: 'dict[pathlib.Path, str] | None' = None
```

## Args

**paths** `list[pathlib.Path]`

No description provided.

**contains\_live\_data** `bool`

No description provided.

**errors** `dict[pathlib.Path, str] | None`

No description provided.

## Attributes

* `paths`: The paths to the downloaded history files.
* `errors`: A dictionary mapping file paths to error messages for files that failed to download. None if all downloads succeeded.
* `contains_live_data`: Whether the run contains live data, not yet exported to parquet files.
