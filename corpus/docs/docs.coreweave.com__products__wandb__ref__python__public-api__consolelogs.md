# ConsoleLogs

Source: https://docs.coreweave.com/products/wandb/ref/python/public-api/consolelogs

# ConsoleLogs

[View source](https://github.com/wandb/wandb/blob/main/wandb/apis/public/console_logs.py#L67)

## Class wandb.apis.public.ConsoleLogs

A lazy iterator over a run's console log lines, oldest first.

Fetched from the W\&B backend page by page. Fetched lines are kept in
memory, so iterating a second time replays the same lines instead of
refetching; create a new instance to re-read a log that may have
grown.

```python theme={"system"}
(service_api: 'ServiceApi',
run: 'Run',
per_page: 'int' = 1000,
last: 'int | None' = None)
```

## Args

**service\_api** `ServiceApi`

The service API instance used to query W\&B.

**run** `Run`

The run whose console log is read.

**per\_page** `int`

Number of lines to fetch per request when reading the log from the beginning. Ignored when `last` is given.

**last** `int | None`

If set, fetch only the last N lines of the log in a single request instead of reading from the beginning. The backend caps how many lines one request returns, so a larger tail comes back truncated to the newest lines.

## Methods

### method Paginator.**next**()

```python theme={"system"}
self
```

Return the next item from the iterator. When exhausted, raise StopIteration
