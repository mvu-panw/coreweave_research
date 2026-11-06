# Api

Source: https://docs.coreweave.com/products/wandb/ref/python/public-api/api

# Api

[View source](https://github.com/wandb/wandb/blob/main/wandb/apis/public/api.py#L100)

## Class wandb.Api

Used for querying the W\&B server.

```python theme={"system"}
overrides: 'dict[str, Any] | None' = None,
timeout: 'int | None' = None,
api_key: 'str | None' = None
```

## Args

**overrides** `dict[str, Any] | None`

You can set `base_url` if you are using a W\&B server other than `https://api.forge.coreweave.com`. You can also set defaults for `entity`, `project`, and `run`.

**timeout** `int | None`

HTTP timeout in seconds for API requests. If not specified, the default timeout will be used.

**api\_key** `str | None`

API key to use for authentication. If not provided, the API key from the current environment or configuration will be used. Prompts for an API key if none is provided or configured in the environment.

## Examples

```python theme={"system"}
import wandb

wandb.Api()
```

## Properties

**default\_entity** `str | None`

Returns the default W\&B entity.

**user\_agent** `str`

Returns W\&B public user agent.

**viewer** `User`

Returns the viewer object.

## Methods

### method Api.artifact()

```python theme={"system"}
(self,
name: 'str',
type: 'str | None' = None)
```

Returns a single artifact.

##### Arguments

**name** `str`

The artifact's name. The name of an artifact resembles a filepath that consists, at a minimum, the name of the project the artifact was logged to, the name of the artifact, and the artifact's version or alias. Optionally append the entity that logged the artifact as a prefix followed by a forward slash. If no entity is specified in the name, the Run or API setting's entity is used.

**type** `str | None`

The type of artifact to fetch.

##### Raises

* `ValueError`: If the artifact name is not specified.
* `ValueError`: If the artifact type is specified but does not match the type of the fetched artifact.

##### Examples

In the following code snippets "entity", "project", "artifact",
"version", and "alias" are placeholders for your W\&B entity, name
of the project the artifact is in, the name of the artifact,
and artifact's version, respectively.

```python theme={"system"}
import wandb

# Specify the project, artifact's name, and the artifact's alias
wandb.Api().artifact(name="project/artifact:alias")

# Specify the project, artifact's name, and a specific artifact version
wandb.Api().artifact(name="project/artifact:version")

# Specify the entity, project, artifact's name, and the artifact's alias
wandb.Api().artifact(name="entity/project/artifact:alias")

# Specify the entity, project, artifact's name, and a specific artifact version
wandb.Api().artifact(name="entity/project/artifact:version")
```

### method Api.artifact\_collection()

```python theme={"system"}
self,
type_name: 'str',
name: 'str'
```

Returns a single artifact collection by type.

You can use the returned `ArtifactCollection` object to retrieve
information about specific artifacts in that collection, and more.

##### Arguments

**type\_name** `str`

The type of artifact collection to fetch.

**name** `str`

An artifact collection name. Optionally append the entity that logged the artifact as a prefix followed by a forward slash.

##### Examples

In the proceeding code snippet "type", "entity", "project", and
"artifact\_name" are placeholders for the collection type, your W\&B
entity, name of the project the artifact is in, and the name of
the artifact, respectively.

```python theme={"system"}
import wandb

collections = wandb.Api().artifact_collection(
    type_name="type", name="entity/project/artifact_name"
)

# Get the first artifact in the collection
artifact_example = collections.artifacts()[0]

# Download the contents of the artifact to the specified root directory.
artifact_example.download()
```

### method Api.artifact\_collection\_exists()

```python theme={"system"}
self,
name: 'str',
type: 'str'
```

Whether an artifact collection exists within a specified project and entity.

##### Arguments

**name** `str`

An artifact collection name. Optionally append the entity that logged the artifact as a prefix followed by a forward slash. If entity or project is not specified, infer the collection from the override params if they exist. Otherwise, entity is pulled from the user settings and project will default to "uncategorized".

**type** `str`

The type of artifact collection.

##### Examples

In the proceeding code snippet "type", and "collection\_name" refer to the type
of the artifact collection and the name of the collection, respectively.

```python theme={"system"}
import wandb

wandb.Api.artifact_collection_exists(type="type", name="collection_name")
```

### method Api.artifact\_collections()

```python theme={"system"}
self,
project_name: 'str',
type_name: 'str',
order: 'str | None' = None,
per_page: 'int' = 50,
start: 'str | None' = None
```

Returns a collection of matching artifact collections.

##### Arguments

**project\_name** `str`

The name of the project to filter on.

**type\_name** `str`

The name of the artifact type to filter on.

**order** `str | None`

Optional string to specify the order of the results. If prefixed with '+', sorts ascending (default). If prefixed with '-', sorts descending.

**per\_page** `int`

Sets the page size for query pagination. Usually there is no reason to change this.

**start** `str | None`

Pagination cursor for resuming a past query, captured from a previous paginator's `.cursor` attribute.

### method Api.artifact\_exists()

```python theme={"system"}
self,
name: 'str',
type: 'str | None' = None
```

Whether an artifact version exists within the specified project and entity.

##### Arguments

**name** `str`

The name of artifact. Add the artifact's entity and project as a prefix. Append the version or the alias of the artifact with a colon. If the entity or project is not specified, W\&B uses override parameters if populated. Otherwise, the entity is pulled from the user settings and the project is set to "Uncategorized".

**type** `str | None`

The type of artifact.

##### Examples

In the proceeding code snippets "entity", "project", "artifact",
"version", and "alias" are placeholders for your W\&B entity, name of
the project the artifact is in, the name of the artifact, and
artifact's version, respectively.

```python theme={"system"}
import wandb

wandb.Api().artifact_exists("entity/project/artifact:version")
wandb.Api().artifact_exists("entity/project/artifact:alias")
```

### method Api.artifact\_type()

```python theme={"system"}
self,
type_name: 'str',
project: 'str | None' = None
```

Returns the matching `ArtifactType`.

##### Arguments

**type\_name** `str`

The name of the artifact type to retrieve.

**project** `str | None`

If given, a project name or path to filter on.

### method Api.artifact\_types()

```python theme={"system"}
self,
project: 'str | None' = None,
start: 'str | None' = None
```

Returns a collection of matching artifact types.

##### Arguments

**project** `str | None`

The project name or path to filter on.

**start** `str | None`

Pagination cursor for resuming a past query, captured from a previous paginator's `.cursor` attribute.

### method Api.artifact\_versions()

```python theme={"system"}
(self, type_name, name, per_page=50)
```

Deprecated. Use `Api.artifacts(type_name, name)` method instead.

##### Arguments

**type\_name** `_empty`

No description provided.

**name** `_empty`

No description provided.

**per\_page** `_empty`

No description provided.

### method Api.artifacts()

```python theme={"system"}
self,
type_name: 'str',
name: 'str',
order: 'str | None' = None,
per_page: 'int' = 50,
tags: 'list[str] | None' = None,
start: 'str | None' = None
```

Return an `Artifacts` collection.

##### Arguments

**type\_name** `str`

The type of artifacts to fetch.

**name** `str`

The artifact's collection name. Optionally append the entity that logged the artifact as a prefix followed by a forward slash.

**order** `str | None`

Optional string to specify the order of the results. If prefixed with '+', sorts ascending (default). If prefixed with '-', sorts descending.

**per\_page** `int`

Sets the page size for query pagination. Usually there is no reason to change this.

**tags** `list[str] | None`

Only return artifacts with all of these tags.

**start** `str | None`

Pagination cursor for resuming a past query, captured from a previous paginator's `.cursor` attribute.

##### Examples

In the proceeding code snippet, "type", "entity", "project", and
"artifact\_name" are placeholders for the artifact type, W\&B entity,
name of the project the artifact was logged to,
and the name of the artifact, respectively.

```python theme={"system"}
import wandb

wandb.Api().artifacts(type_name="type", name="entity/project/artifact_name")
```

Pause iteration and resume later from the same position by saving
the paginator's `.cursor` and passing it as `start=`:

```python theme={"system"}
from itertools import islice

import wandb

api = wandb.Api()

# Consume the first page of results, then save the cursor.
page_size = 10
artifacts = api.artifacts(
    type_name="type",
    name="entity/project/artifact_name",
    per_page=page_size,
)
first_page = list(islice(artifacts, page_size))

saved_cursor = artifacts.cursor

# Later (e.g. in a new process), resume iteration from the saved cursor.
remaining_artifacts = api.artifacts(
    type_name="type",
    name="entity/project/artifact_name",
    per_page=page_size,
    start=saved_cursor,
)
```

### method Api.automation()

```python theme={"system"}
self,
name: 'str', *,
entity: 'str | None' = None
```

Returns the only Automation matching the parameters.

##### Arguments

**name** `str`

The name of the automation to fetch.

**entity** `str | None`

The entity to fetch the automation for.

##### Raises

* `ValueError`: If zero or multiple Automations match the search criteria.

##### Examples

Get an existing automation named "my-automation":

```python theme={"system"}
import wandb

api = wandb.Api()
automation = api.automation(name="my-automation")
```

Get an existing automation named "other-automation", from the entity "my-team":

```python theme={"system"}
automation = api.automation(name="other-automation", entity="my-team")
```

### method Api.automations()

```python theme={"system"}
self,
entity: 'str | None' = None, *,
name: 'str | None' = None,
per_page: 'int' = 50,
start: 'str | None' = None
```

Returns an iterator over all Automations that match the given parameters.

If no parameters are provided, the returned iterator will contain all
Automations that the user has access to.

##### Arguments

**entity** `str | None`

The entity to fetch the automations for.

**name** `str | None`

The name of the automation to fetch.

**per\_page** `int`

The number of automations to fetch per page. Defaults to 50.  Usually there is no reason to change this.

**start** `str | None`

Pagination cursor for resuming a past query, captured from a previous paginator's `.cursor` attribute.

##### Examples

Fetch all existing automations for the entity "my-team":

```python theme={"system"}
import wandb

api = wandb.Api()
automations = api.automations(entity="my-team")
```

### method Api.create\_automation()

```python theme={"system"}
self,
obj: 'NewAutomation', *,
fetch_existing: 'bool' = False, **kwargs: 'Unpack[WriteAutomationsKwargs]'
```

Create a new Automation.

##### Arguments

**obj** `NewAutomation`

The automation to create.

**fetch\_existing** `bool`

If True, and a conflicting automation already exists, attempt to fetch the existing automation instead of raising an error.

**kwargs** `Unpack[WriteAutomationsKwargs]`

No description provided.

##### Examples

Create a new automation named "my-automation" that sends a Slack notification
when a run within a specific project logs a metric exceeding a custom threshold:

```python theme={"system"}
import wandb
from wandb.automations import OnRunMetric, RunEvent, SendNotification

api = wandb.Api()

project = api.project("my-project", entity="my-team")

# Use the first Slack integration for the team
slack_hook = next(api.slack_integrations(entity="my-team"))

event = OnRunMetric(
    scope=project,
    filter=RunEvent.metric("custom-metric") > 10,
)
action = SendNotification.from_integration(slack_hook)

automation = api.create_automation(
    event >> action,
    name="my-automation",
    description="Send a Slack message whenever 'custom-metric' exceeds 10.",
)
```

### method Api.create\_custom\_chart()

```python theme={"system"}
self,
entity: 'str',
name: 'str',
display_name: 'str',
spec_type: "Literal['vega2']",
access: "Literal['private', 'public']",
spec: 'str | dict'
```

Create a custom chart preset and return its id.

##### Arguments

**entity** `str`

The entity (user or team) that owns the chart

**name** `str`

Unique identifier for the chart preset

**display\_name** `str`

Human-readable name shown in the UI

**spec\_type** `Literal['vega2']`

Type of specification. Must be "vega2" for Vega-Lite v2 specifications.

**access** `Literal['private', 'public']`

Access level for the chart:

* "private": Chart is only accessible to the entity that created it
* "public": Chart is publicly accessible

**spec** `str | dict`

The Vega/Vega-Lite specification as a dictionary or JSON string

##### Raises

* `wandb.Error`: If chart creation fails
* `UnsupportedError`: If the server doesn't support custom charts

##### Examples

```python theme={"system"}
    import wandb

    api = wandb.Api()

    # Define a simple bar chart specification
    vega_spec = {
        "$schema": "https://vega.github.io/schema/vega-lite/v6.json",
        "mark": "bar",
        "data": {"name": "wandb"},
        "encoding": {
            "x": {"field": "${field:x}", "type": "ordinal"},
            "y": {"field": "${field:y}", "type": "quantitative"},
        },
    }

    # Create the custom chart
    chart_id = api.create_custom_chart(
        entity="my-team",
        name="my-bar-chart",
        display_name="My Custom Bar Chart",
        spec_type="vega2",
        access="private",
        spec=vega_spec,
    )

    # Use with wandb.plot_table()
    chart = wandb.plot_table(
        vega_spec_name=chart_id,
        data_table=my_table,
        fields={"x": "category", "y": "value"},
    )
```

### method Api.create\_project()

```python theme={"system"}
self,
name: 'str',
entity: 'str'
```

Create a new project.

##### Arguments

**name** `str`

The name of the new project.

**entity** `str`

The entity of the new project.

### method Api.create\_registry()

```python theme={"system"}
self,
name: 'str',
visibility: "Literal['organization', 'restricted']",
organization: 'str | None' = None,
description: 'str | None' = None,
artifact_types: 'list[str] | None' = None
```

Create a new registry.

##### Arguments

**name** `str`

The name of the registry. Name must be unique within the organization.

**visibility** `Literal['organization', 'restricted']`

The visibility of the registry. organization: Anyone in the organization can view this registry. You can edit their roles later from the settings in the UI. restricted: Only invited members via the UI can access this registry. Public sharing is disabled.

**organization** `str | None`

The organization of the registry. If no organization is set in the settings, the organization will be fetched from the entity if the entity only belongs to one organization.

**description** `str | None`

The description of the registry.

**artifact\_types** `list[str] | None`

The accepted artifact types of the registry. A type is no more than 128 characters and do not include characters `/` or `:`. If not specified, all types are accepted. Allowed types added to the registry cannot be removed later.

##### Examples

```python theme={"system"}
import wandb

api = wandb.Api()
registry = api.create_registry(
    name="my-registry",
    visibility="restricted",
    organization="my-org",
    description="This is a test registry",
    artifact_types=["model"],
)
```

### method Api.create\_run()

```python theme={"system"}
self, *,
run_id: 'str | None' = None,
project: 'str | None' = None,
entity: 'str | None' = None
```

Create a new run.

##### Arguments

**run\_id** `str | None`

The ID to assign to the run. If not specified, W\&B creates a random ID.

**project** `str | None`

The project where to log the run to. If no project is specified, log the run to a project called "Uncategorized".

**entity** `str | None`

The entity that owns the project. If no entity is specified, log the run to the default entity.

### method Api.create\_run\_queue()

```python theme={"system"}
self,
name: 'str',
type: 'public.RunQueueResourceType',
entity: 'str | None' = None,
prioritization_mode: 'public.RunQueuePrioritizationMode | None' = None,
config: 'dict | None' = None,
template_variables: 'dict | None' = None
```

Create a new run queue in W\&B Launch.

##### Arguments

**name** `str`

Name of the queue to create

**type** `public.RunQueueResourceType`

Type of resource to be used for the queue. One of "local-container", "local-process", "kubernetes","sagemaker", or "gcp-vertex".

**entity** `str | None`

Name of the entity to create the queue. If `None`, use the configured or default entity.

**prioritization\_mode** `public.RunQueuePrioritizationMode | None`

Version of prioritization to use. Either "V0" or `None`.

**config** `dict | None`

Default resource configuration to be used for the queue. Use handlebars (eg. `{{var}}`) to specify template variables.

**template\_variables** `dict | None`

A dictionary of template variable schemas to use with the config.

### method Api.create\_team()

```python theme={"system"}
self,
team: 'str',
admin_username: 'str | None' = None
```

Create a new team.

For W\&B Multi-tenant Cloud users, set the Default API organization in
your user settings in the W\&B UI before calling `create_team()`.
This setting determines the organization the new team will belong to.

##### Arguments

**team** `str`

The name of the team.

**admin\_username** `str | None`

Username of the admin user of the team. Defaults to the current user.

### method Api.create\_user()

```python theme={"system"}
self,
email: 'str',
admin: 'bool | None' = False
```

Create a new user.

##### Arguments

**email** `str`

The email address of the user.

**admin** `bool | None`

Set user as a global instance administrator.

### method Api.delete\_automation()

```python theme={"system"}
self,
obj: 'Automation | str'
```

Delete an automation.

##### Arguments

**obj** `Automation | str`

The automation to delete, or its ID.

### method Api.flush()

```python theme={"system"}
(self)
```

Flush the local cache.

The api object keeps a local cache of runs, so if the state of the run
may change while executing your script you must clear the local cache
with `api.flush()` to get the latest values associated with the run.

### method Api.from\_path()

```python theme={"system"}
(self,
path: 'str')
```

Return a run, sweep, project or report from a path.

##### Arguments

**path** `str`

The path to the project, run, sweep or report

##### Examples

In the proceeding code snippets "project", "team", "run\_id", "sweep\_id",
and "report\_name" are placeholders for the project, team, run ID,
sweep ID, and the name of a specific report, respectively.

```python theme={"system"}
import wandb

api = wandb.Api()

project = api.from_path("project")
team_project = api.from_path("team/project")
run = api.from_path("team/project/runs/run_id")
sweep = api.from_path("team/project/sweeps/sweep_id")
report = api.from_path("team/project/reports/report_name")
```

### method Api.integrations()

```python theme={"system"}
self,
entity: 'str | None' = None, *,
per_page: 'int' = 50,
start: 'str | None' = None
```

Return an iterator of all integrations for an entity.

##### Arguments

**entity** `str | None`

The entity (e.g. team name) for which to fetch integrations.  If not provided, the user's default entity will be used.

**per\_page** `int`

Number of integrations to fetch per page. Defaults to 50.  Usually there is no reason to change this.

**start** `str | None`

No description provided.

### method Api.job()

```python theme={"system"}
self,
name: 'str | None',
path: 'str | None' = None
```

Return a `Job` object.

##### Arguments

**name** `str | None`

The name of the job.

**path** `str | None`

The root path to download the job artifact.

### method Api.list\_jobs()

```python theme={"system"}
self,
entity: 'str',
project: 'str'
```

Return a list of jobs, if any, for the given entity and project.

##### Arguments

**entity** `str`

The entity for the listed jobs.

**project** `str`

The project for the listed jobs.

### method Api.organization()

```python theme={"system"}
self,
name: 'str | None' = None
```

Return the matching `Organization`.

##### Arguments

**name** `str | None`

The name of the organization. If omitted, this method will attempt to infer and return the current default organization.

### method Api.project()

```python theme={"system"}
self,
name: 'str',
entity: 'str | None' = None
```

Return the `Project` with the given name (and entity, if given).

##### Arguments

**name** `str`

The project name.

**entity** `str | None`

Name of the entity requested.  If None, will fall back to the default entity passed to `Api`.  If no default entity, will raise a `ValueError`.

### method Api.projects()

```python theme={"system"}
self,
entity: 'str | None' = None,
per_page: 'int' = 200
```

Get projects for a given entity.

##### Arguments

**entity** `str | None`

Name of the entity requested.  If None, will fall back to the default entity passed to `Api`.  If no default entity, will raise a `ValueError`.

**per\_page** `int`

Sets the page size for query pagination. Usually there is no reason to change this.

### method Api.queued\_run()

```python theme={"system"}
(self,
entity: 'str',
project: 'str',
queue_name: 'str',
run_queue_item_id: 'str', project_queue=None, priority=None)
```

Return a single queued run based on the path.

Parses paths of the form `entity/project/queue_id/run_queue_item_id`.

##### Arguments

**entity** `str`

No description provided.

**project** `str`

No description provided.

**queue\_name** `str`

No description provided.

**run\_queue\_item\_id** `str`

No description provided.

**project\_queue** `_empty`

No description provided.

**priority** `_empty`

No description provided.

### method Api.registries()

```python theme={"system"}
self,
organization: 'str | None' = None,
filter: 'dict[str, Any] | None' = None,
order: 'str | None' = None,
per_page: 'int' = 100,
start: 'str | None' = None
```

Returns a lazy iterator of `Registry` objects.

Use the iterator to search and filter registries, collections,
or artifact versions across your organization's registry. Results are
fetched lazily as you iterate, so you can stop after any number of
items—for example, with :func:`itertools.islice`—without requesting
the rest.

##### Arguments

**organization** `str | None`

The organization of the registry to fetch. If not specified, use the organization specified in the user's settings.

**filter** `dict[str, Any] | None`

Optional MongoDB-style filter to apply to each object in the lazy registry iterator. Fields available to filter for registries are `name`, `description`, `created_at`, `updated_at`. Fields available to filter for collections are `name`, `tag`, `description`, `created_at`, `updated_at` Fields available to filter for versions are `tag`, `alias`, `created_at`, `updated_at`, `metadata`

**order** `str | None`

Optional string to specify the order of the results. If prefixed with '+', sorts ascending (default). If prefixed with '-', sorts descending.

**per\_page** `int`

Sets the page size for query pagination.

**start** `str | None`

Pagination cursor for resuming a past query, captured from a previous paginator's `.cursor` attribute.

##### Examples

Find all registries with the names that contain "model"

```python theme={"system"}
import wandb

api = wandb.Api()  # specify an org if your entity belongs to multiple orgs
api.registries(filter={"name": {"$regex": "model"}})
```

Find all collections in the registries with the name "my\_collection" and the tag "my\_tag"

```python theme={"system"}
api.registries().collections(filter={"name": "my_collection", "tag": "my_tag"})
```

Find all artifact versions in the registries with a collection name that contains "my\_collection" and a version that has the alias "best"

```python theme={"system"}
api.registries().collections(
    filter={"name": {"$regex": "my_collection"}}
).versions(filter={"alias": "best"})
```

Find all artifact versions in the registries that contain "model" and have the tag "prod" or alias "best"

```python theme={"system"}
api.registries(filter={"name": {"$regex": "model"}}).versions(
    filter={"$or": [{"tag": "prod"}, {"alias": "best"}]}
)
```

Pause iteration and resume later from the same position by saving
the paginator's `.cursor` and passing it as `start=`:

```python theme={"system"}
from itertools import islice

import wandb

api = wandb.Api()

# Consume the first page of results, then save the cursor.
page_size = 10
registries = api.registries(per_page=page_size)
first_page = list(islice(registries, page_size))

saved_cursor = registries.cursor

# Later (e.g. in a new process), resume iteration from the saved cursor.
remaining_registries = api.registries(per_page=page_size, start=saved_cursor)
```

### method Api.registry()

```python theme={"system"}
self,
name: 'str',
organization: 'str | None' = None
```

Return a registry given a registry name.

##### Arguments

**name** `str`

The name of the registry. This is without the `wandb-registry-` prefix.

**organization** `str | None`

The organization of the registry. If no organization is set in the settings, the organization will be fetched from the entity if the entity only belongs to one organization.

##### Examples

Fetch and update a registry

```python theme={"system"}
import wandb

api = wandb.Api()
registry = api.registry(name="my-registry", organization="my-org")
registry.description = "This is an updated description"
registry.save()
```

### method Api.reports()

```python theme={"system"}
self,
path: 'str' = '',
name: 'str | None' = None,
per_page: 'int' = 50
```

Get reports for a given project path.

Note: `wandb.Api.reports()` API is in beta and will likely change in
future releases.

##### Arguments

**path** `str`

The path to the project the report resides in. Specify the entity that created the project as a prefix followed by a forward slash.

**name** `str | None`

Name of the report requested.

**per\_page** `int`

Sets the page size for query pagination. Usually there is no reason to change this.

##### Examples

```python theme={"system"}
import wandb

wandb.Api.reports("entity/project")
```

### method Api.run()

```python theme={"system"}
self,
path: 'str' = ''
```

Return a single run by parsing path in the form `entity/project/run_id`.

##### Arguments

**path** `str`

Path to run in the form `entity/project/run_id`. If `api.entity` is set, this can be in the form `project/run_id` and if `api.project` is set this can just be the run\_id.

##### Raises

* `RunNotFoundError`: If a run is not found, or run data is not able to be loaded.

### method Api.run\_queue()

```python theme={"system"}
(self,
entity: 'str',
name: 'str')
```

Return the named `RunQueue` for entity.

See `Api.create_run_queue` for more information on how to create a run queue.

##### Arguments

**entity** `str`

No description provided.

**name** `str`

No description provided.

### method Api.runs()

```python theme={"system"}
(self,
path: 'str | None' = None,
filters: 'dict[str, Any] | None' = None,
order: 'str' = '+created_at',
per_page: 'int' = 50,
include_sweeps: 'bool' = False,
lazy: 'bool' = True)
```

Returns a `Runs` object, which lazily iterates over `Run` objects.

Fields you can filter by include:

* `createdAt`: The timestamp when the run was created. (in ISO 8601 format, e.g. "2023-01-01T12:00:00Z")
* `displayName`: The human-readable display name of the run. (e.g. "eager-fox-1")
* `duration`: The total runtime of the run in seconds.
* `group`: The group name used to organize related runs together.
* `host`: The hostname where the run was executed.
* `jobType`: The type of job or purpose of the run.
* `name`: The unique identifier of the run. (e.g. "a1b2cdef")
* `state`: The current state of the run.
* `tags`: The tags associated with the run.
* `username`: The username of the user who initiated the run

Additionally, you can filter by items in the run config or summary metrics.
Such as `config.experiment_name`, `summary_metrics.loss`, etc.

For more complex filtering, you can use MongoDB query operators.
For details, see: [https://docs.mongodb.com/manual/reference/operator/query](https://docs.mongodb.com/manual/reference/operator/query)
The following operations are supported:

* `$and`
* `$or`
* `$nor`
* `$eq`
* `$ne`
* `$gt`
* `$gte`
* `$lt`
* `$lte`
* `$in`
* `$nin`
* `$exists`
* `$regex`

##### Arguments

**path** `str | None`

(str) path to project, should be in the form: "entity/project"

**filters** `dict[str, Any] | None`

(dict) queries for specific runs using the MongoDB query language. You can filter by run properties such as config.key, summary\_metrics.key, state, entity, createdAt, etc. For example: `{"config.experiment_name": "foo"}` would find runs with a config entry of experiment name set to "foo"

**order** `str`

(str) Order can be `created_at`, `heartbeat_at`, `config.*.value`, or `summary_metrics.*`. If you prepend order with a + order is ascending (default). If you prepend order with a - order is descending. The default order is run.created\_at from oldest to newest.

**per\_page** `int`

(int) Sets the page size for query pagination.

**include\_sweeps** `bool`

(bool) Whether to eagerly fetch the sweep object in each run result.

**lazy** `bool`

(bool) Whether to use lazy loading for faster performance. When True (default), only essential run metadata is loaded initially. Heavy fields like config, summaryMetrics, and systemMetrics are loaded on-demand when accessed. Set to False for full data upfront.

##### Examples

```python theme={"system"}
import wandb
from wandb.apis.public import Api

# Find runs in project where config.experiment_name has been set to "foo"
Api.runs(path="my_entity/project", filters={"config.experiment_name": "foo"})
```

```python theme={"system"}
# Find runs in project where config.experiment_name has been set to "foo" or "bar"
Api.runs(
    path="my_entity/project",
    filters={
        "$or": [
            {"config.experiment_name": "foo"},
            {"config.experiment_name": "bar"},
        ]
    },
)
```

```python theme={"system"}
# Find runs in project where config.experiment_name matches a regex
Api.runs(
    path="my_entity/project",
    filters={"config.experiment_name": {"$regex": "b.*"}},
)
```

Note:
Regular expressions use Google's RE2 syntax:
[https://github.com/google/re2/wiki/Syntax](https://github.com/google/re2/wiki/Syntax)

```python theme={"system"}
# Find runs in project where the run name matches a regex
Api.runs(
    path="my_entity/project", filters={"display_name": {"$regex": "^foo.*"}}
)
```

```python theme={"system"}
# Find runs in project sorted by ascending loss
Api.runs(path="my_entity/project", order="+summary_metrics.loss")
```

### method Api.slack\_integrations()

```python theme={"system"}
self, *,
entity: 'str | None' = None,
per_page: 'int' = 50,
start: 'str | None' = None
```

Returns an iterator of Slack integrations for an entity.

##### Arguments

**entity** `str | None`

The entity (e.g. team name) for which to fetch integrations.  If not provided, the user's default entity will be used.

**per\_page** `int`

Number of integrations to fetch per page. Defaults to 50.  Usually there is no reason to change this.

**start** `str | None`

No description provided.

##### Examples

Get all registered Slack integrations for the team "my-team":

```python theme={"system"}
import wandb

api = wandb.Api()
slack_integrations = api.slack_integrations(entity="my-team")
```

Find only Slack integrations that post to channel names starting with "team-alerts-":

```python theme={"system"}
slack_integrations = api.slack_integrations(entity="my-team")
team_alert_integrations = [
    ig
    for ig in slack_integrations
    if ig.channel_name.startswith("team-alerts-")
]
```

### method Api.sweep()

```python theme={"system"}
(self, path='')
```

Return a sweep by parsing path in the form `entity/project/sweep_id`.

##### Arguments

**path** `_empty`

Path to sweep in the form entity/project/sweep\_id. If `api.entity` is set, this can be in the form project/sweep\_id and if `api.project` is set this can just be the sweep\_id.

### method Api.sync\_tensorboard()

```python theme={"system"}
(self, root_dir, run_id=None, project=None, entity=None)
```

Sync a local directory containing tfevent files to wandb.

##### Arguments

**root\_dir** `_empty`

No description provided.

**run\_id** `_empty`

No description provided.

**project** `_empty`

No description provided.

**entity** `_empty`

No description provided.

### method Api.team()

```python theme={"system"}
self,
team: 'str'
```

Return the matching `Team` with the given name.

##### Arguments

**team** `str`

The name of the team.

### method Api.update\_automation()

```python theme={"system"}
self,
obj: 'Automation', *,
create_missing: 'bool' = False, **kwargs: 'Unpack[WriteAutomationsKwargs]'
```

Update an existing automation.

##### Arguments

**obj** `Automation`

The automation to update.  Must be an existing automation.

**create\_missing** `bool`

If True, and the automation does not exist, create it.

**kwargs** `Unpack[WriteAutomationsKwargs]`

No description provided.

##### Examples

Disable and edit the description of an existing automation ("my-automation"):

```python theme={"system"}
import wandb

api = wandb.Api()

automation = api.automation(name="my-automation")
automation.enabled = False
automation.description = "Kept for reference, but no longer used."

updated_automation = api.update_automation(automation)
```

OR

```python theme={"system"}
import wandb

api = wandb.Api()

automation = api.automation(name="my-automation")

updated_automation = api.update_automation(
    automation,
    enabled=False,
    description="Kept for reference, but no longer used.",
)
```

### method Api.upsert\_run\_queue()

```python theme={"system"}
(self,
name: 'str',
resource_config: 'dict',
resource_type: 'public.RunQueueResourceType',
entity: 'str | None' = None,
template_variables: 'dict | None' = None,
external_links: 'dict | None' = None,
prioritization_mode: 'public.RunQueuePrioritizationMode | None' = None)
```

Upsert a run queue in W\&B Launch.

##### Arguments

**name** `str`

Name of the queue to create

**resource\_config** `dict`

Optional default resource configuration to be used for the queue. Use handlebars (eg. `{{var}}`) to specify template variables.

**resource\_type** `public.RunQueueResourceType`

Type of resource to be used for the queue. One of "local-container", "local-process", "kubernetes", "sagemaker", or "gcp-vertex".

**entity** `str | None`

Optional name of the entity to create the queue. If `None`, use the configured or default entity.

**template\_variables** `dict | None`

A dictionary of template variable schemas to be used with the config.

**external\_links** `dict | None`

Optional dictionary of external links to be used with the queue.

**prioritization\_mode** `public.RunQueuePrioritizationMode | None`

Optional version of prioritization to use. Either "V0" or None

### method Api.user()

```python theme={"system"}
self,
username_or_email: 'str'
```

Return a user from a username or email address.

This function only works for local administrators. Use `api.viewer`
to get your own user object.

##### Arguments

**username\_or\_email** `str`

The username or email address of the user.

### method Api.users()

```python theme={"system"}
self,
username_or_email: 'str'
```

Return all users from a partial username or email address query.

This function only works for local administrators. Use `api.viewer`
to get your own user object.

##### Arguments

**username\_or\_email** `str`

The prefix or suffix of the user you want to find.

### method Api.webhook\_integrations()

```python theme={"system"}
self,
entity: 'str | None' = None, *,
per_page: 'int' = 50,
start: 'str | None' = None
```

Returns an iterator of webhook integrations for an entity.

##### Arguments

**entity** `str | None`

The entity (e.g. team name) for which to fetch integrations.  If not provided, the user's default entity will be used.

**per\_page** `int`

Number of integrations to fetch per page. Defaults to 50.  Usually there is no reason to change this.

**start** `str | None`

No description provided.

##### Examples

Get all registered webhook integrations for the team "my-team":

```python theme={"system"}
import wandb

api = wandb.Api()
webhook_integrations = api.webhook_integrations(entity="my-team")
```

Find only webhook integrations that post requests to "[https://my-fake-url.com](https://my-fake-url.com)":

```python theme={"system"}
webhook_integrations = api.webhook_integrations(entity="my-team")
my_webhooks = [
    ig
    for ig in webhook_integrations
    if ig.url_endpoint.startswith("https://my-fake-url.com")
]
```
