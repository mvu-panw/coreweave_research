# ArtifactCollection

Source: https://docs.coreweave.com/products/wandb/ref/python/public-api/artifactcollection

# ArtifactCollection

[View source](https://github.com/wandb/wandb/blob/main/wandb/apis/public/artifacts.py#L540)

## Class wandb.apis.public.ArtifactCollection

An artifact collection that represents a group of related artifacts.

## Properties

**aliases** `list[str]`

The aliases for all artifact versions contained in this collection.

**created\_at** `str`

The creation date of the artifact collection.

**description** `str | None`

A description of the artifact collection.

**entity** `str`

The entity (user or team) that owns the project.

**id** `str`

The unique identifier of the artifact collection.

**name** `str`

The name of the artifact collection.

**project** `str`

The project that contains the artifact collection.

**project\_id** `str`

The encoded GraphQL ID for this collection's project.

**project\_internal\_id** `str | None`

The GraphQL `internalId` for this collection's backing project, if fetched.

This is a base64-encoded global ID. When decoded, it looks like
`Project:123` or `ProjectInternalId:123`.

**tags** `list[str]`

The tags associated with the artifact collection.

**type**

Returns the type of the artifact collection.

**updated\_at** `str | None`

The date at which the artifact collection was last updated.

## Methods

### method ArtifactCollection.artifacts()

```python theme={"system"}
self,
per_page: 'int' = 50,
start: 'str | None' = None
```

Get all artifacts in the collection.

##### Arguments

**per\_page** `int`

The number of artifacts to fetch per page.

**start** `str | None`

Pagination cursor for resuming a past query, captured from a previous paginator's `.cursor` attribute.

### method ArtifactCollection.change\_type()

```python theme={"system"}
self,
new_type: 'str'
```

Deprecated, change type directly with `save` instead.

##### Arguments

**new\_type** `str`

No description provided.

### method ArtifactCollection.delete()

```python theme={"system"}
self
```

Delete the entire artifact collection.

### method ArtifactCollection.is\_sequence()

```python theme={"system"}
self
```

Return whether the artifact collection is a sequence.

### method ArtifactCollection.save()

```python theme={"system"}
self
```

Persist any changes made to the artifact collection.
