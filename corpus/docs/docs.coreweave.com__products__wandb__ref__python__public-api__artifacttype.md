# ArtifactType

Source: https://docs.coreweave.com/products/wandb/ref/python/public-api/artifacttype

# ArtifactType

[View source](https://github.com/wandb/wandb/blob/main/wandb/apis/public/artifacts.py#L204)

## Class wandb.apis.public.ArtifactType

An artifact object that satisfies query based on the specified type.

## Properties

**id** `str`

The unique identifier of the artifact type.

**name** `str`

The name of the artifact type.

## Methods

### method ArtifactType.collection()

```python theme={"system"}
self,
name: 'str'
```

Get a specific artifact collection by name.

##### Arguments

**name** `str`

The name of the artifact collection to retrieve.

### method ArtifactType.collections()

```python theme={"system"}
self,
filters: 'Mapping[str, Any] | None' = None,
order: 'str | None' = None,
per_page: 'int' = 50,
start: 'str | None' = None
```

Get all artifact collections associated with this artifact type.

##### Arguments

**filters** `Mapping[str, Any] | None`

Optional mapping of filters to apply to the query.

**order** `str | None`

Optional string to specify the order of the results. If prefixed with '+', sorts ascending (default). If prefixed with '-', sorts descending. The default order is the collection ID in descending order.

**per\_page** `int`

The number of artifact collections to fetch per page. Default is 50.

**start** `str | None`

Pagination cursor for resuming a past query, captured from a previous paginator's `.cursor` attribute.
