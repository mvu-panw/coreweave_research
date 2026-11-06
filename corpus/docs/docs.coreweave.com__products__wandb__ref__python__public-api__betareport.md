# BetaReport

Source: https://docs.coreweave.com/products/wandb/ref/python/public-api/betareport

# BetaReport

[View source](https://github.com/wandb/wandb/blob/main/wandb/apis/public/reports.py#L170)

## Class wandb.apis.public.BetaReport

BetaReport is a class associated with reports created in W\&B.

Provides access to report attributes (name, description, user, spec,
timestamps) and methods for retrieving associated runs,
sections, and for rendering the report as HTML.

```python theme={"system"}
(service_api: 'ServiceApi',
attrs: 'dict',
entity: 'str | None' = None,
project: 'str | None' = None)
```

## Args

**service\_api** `ServiceApi`

No description provided.

**attrs** `dict`

No description provided.

**entity** `str | None`

No description provided.

**project** `str | None`

No description provided.

## Attributes

* `id` (`string`): Unique identifier of the report.
* `display_name` (`string`): Human-readable display name of the report.
* `name` (`string`): The name of the report. Use `display_name` for a more user-friendly name.
* `description` (`string`): Description of the report.
* `user` (`User`): Dictionary containing user info (username, email) who created the report.
* `spec` (`dict`): The spec of the report.
* `url` (`string`): The URL of the report.
* `updated_at` (`string`): Timestamp of last update.
* `created_at` (`string`): Timestamp when the report was created.

## Properties

**created\_at**

No description provided.

**description** `str | None`

No description provided.

**display\_name** `str | None`

No description provided.

**id** `str`

No description provided.

**name** `str | None`

No description provided.

**sections**

Get the panel sections (groups) from the report.

**spec** `dict[str, Any]`

No description provided.

**updated\_at**

No description provided.

**url** `str | None`

No description provided.

**user**

No description provided.

## Methods

### method BetaReport.runs()

```python theme={"system"}
self,
section: 'dict[str, Any]',
per_page: 'int' = 50,
only_selected: 'bool' = True
```

Get runs associated with a section of the report.

##### Arguments

**section** `dict[str, Any]`

No description provided.

**per\_page** `int`

No description provided.

**only\_selected** `bool`

No description provided.

### method BetaReport.to\_html()

```python theme={"system"}
self,
height: 'int' = 1024,
hidden: 'bool' = False
```

Generate HTML containing an iframe displaying this report.

##### Arguments

**height** `int`

No description provided.

**hidden** `bool`

No description provided.
