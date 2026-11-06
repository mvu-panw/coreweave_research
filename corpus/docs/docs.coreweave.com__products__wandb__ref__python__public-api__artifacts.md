# Artifacts

Source: https://docs.coreweave.com/products/wandb/ref/python/public-api/artifacts

# Artifacts

[View source](https://github.com/wandb/wandb/blob/main/wandb/apis/public/artifacts.py#L932)

## Class wandb.apis.public.Artifacts

An iterable collection of artifact versions associated with a project.

Optionally pass in filters to narrow down the results based on specific criteria.

## Methods

### method Paginator.**next**()

```python theme={"system"}
self
```

Return the next item from the iterator. When exhausted, raise StopIteration

### method Paginator.update\_variables()

```python theme={"system"}
self
```

Update the query variables for the next page fetch.
