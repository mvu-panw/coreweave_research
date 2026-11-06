# ConsoleLogLine

Source: https://docs.coreweave.com/products/wandb/ref/python/public-api/consolelogline

# ConsoleLogLine

[View source](https://github.com/wandb/wandb/blob/main/wandb/apis/public/console_logs.py#L40)

## Class wandb.apis.public.ConsoleLogLine

A single line of a run's captured console output.

```python theme={"system"}
number: 'int',
timestamp: 'datetime | None',
level: 'str',
label: 'str',
content: 'str'
```

## Args

**number** `int`

No description provided.

**timestamp** `datetime | None`

No description provided.

**level** `str`

No description provided.

**label** `str`

No description provided.

**content** `str`

No description provided.

## Attributes

* `number`: Position of the line in the run's console log, starting at 0.
* `timestamp`: The time the line was captured, as a timezone-aware UTC datetime. None if the backend did not record a time for the line or sent one in an unexpected format.
* `level`: The severity of the line: `"error"` for lines written to stderr, empty otherwise.
* `label`: A label identifying the process that wrote the line when several processes write to the same run, as set by the `x_label` setting in shared mode. Empty for single-writer runs.
* `content`: The text of the line.
