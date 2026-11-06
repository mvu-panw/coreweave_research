# Artifact

Source: https://docs.coreweave.com/products/wandb/ref/python/experiments/artifact

# Artifact

[View source](https://github.com/wandb/wandb/blob/main/wandb/sdk/artifacts/artifact.py#L128)

## Class wandb.Artifact

Flexible and lightweight building block for dataset and model versioning.

Construct an empty W\&B Artifact. Populate an artifacts contents with methods that
begin with `add`. Once the artifact has all the desired files, you can call
`run.log_artifact()` to log it.

```python theme={"system"}
name: 'str',
type: 'str',
description: 'str | None' = None,
metadata: 'dict[str, Any] | None' = None,
incremental: 'bool' = False,
use_as: 'str | None' = None,
storage_region: 'str | None' = None,
digest_algorithm: "Literal['MD5', 'XXH128']" = 'MD5'
```

## Args

**name** `str`

A human-readable name for the artifact. Use the name to identify a specific artifact in the W\&B App UI or programmatically. You can interactively reference an artifact with the `use_artifact` Public API. A name can contain letters, numbers, underscores, hyphens, and dots. The name must be unique across a project.

**type** `str`

The artifact's type. Use the type of an artifact to both organize and differentiate artifacts. You can use any string that contains letters, numbers, underscores, hyphens, and dots. Common types include `dataset` or `model`. Include `model` within your type string if you want to link the artifact to the W\&B Model Registry. Note that some types reserved for internal use and cannot be set by users. Such types include `job` and types that start with `wandb-`.

**description** `str | None`

A description of the artifact. For Model or Dataset Artifacts, add documentation for your standardized team model or dataset card. View an artifact's description programmatically with the `Artifact.description` attribute or programmatically with the W\&B App UI. W\&B renders the description as markdown in the W\&B App.

**metadata** `dict[str, Any] | None`

Additional information about an artifact. Specify metadata as a dictionary of key-value pairs. You can specify no more than 100 total keys.

**incremental** `bool`

Use `Artifact.new_draft()` method instead to modify an existing artifact.

**use\_as** `str | None`

Deprecated.

**storage\_region** `str | None`

No description provided.

**digest\_algorithm** `Literal['MD5', 'XXH128']`

The digest algorithm to use for the artifact. Defaults to MD5. If set to XXH128, the artifact will be hashed using the XXH128 algorithm unless it is part of a collection that is already using MD5. Calls to `artifact.verify()` on SDK versions before 0.29.0 will always fail on XXH128 artifacts.

## Properties

**aliases** `list[str]`

List of one or more semantically-friendly references or

identifying "nicknames" assigned to an artifact version.

Aliases are mutable references that you can programmatically reference.
Change an artifact's alias with the W\&B App UI or programmatically.
See [Create new artifact versions](https://docs.wandb.ai/models/artifacts/create-a-new-artifact-version)
for more information.

**collection** `ArtifactCollection`

The collection this artifact is retrieved from.

A collection is an ordered group of artifact versions.
If this artifact is retrieved from a collection that it is linked to,
return that collection. Otherwise, return the collection
that the artifact version originates from.

The collection that an artifact originates from is known as
the source sequence.

**commit\_hash** `str`

The hash returned when this artifact was committed.

**created\_at** `str`

Timestamp when the artifact was created.

**description** `str | None`

A description of the artifact.

**digest** `str`

The logical digest of the artifact.

The digest is the checksum of the artifact's contents. If an artifact has the
same digest as the current `latest` version, then `log_artifact` is a no-op.

**digest\_algorithm** `ArtifactDigestAlgorithm`

The digest algorithm used to compute the artifact's digest.

**entity** `str`

The name of the entity that the artifact collection belongs to.

If the artifact is a link, the entity will be the entity of the linked artifact.

**file\_count** `int`

The number of files (including references).

**history\_step** `int | None`

The nearest step which logged history metrics for this artifact's source run.

**id** `str | None`

The artifact's ID.

**is\_link** `bool`

Boolean flag indicating if the artifact is a link artifact.

True: The artifact is a link artifact to a source artifact.
False: The artifact is a source artifact.

**linked\_artifacts** `list[Artifact]`

Returns a list of all the linked artifacts of a source artifact.

If this artifact is a link artifact (`artifact.is_link == True`),
it will return an empty list.

Limited to 500 results.

**linked\_at** `str | None`

The time when this artifact was linked to its current collection.

Only valid for linked artifacts, returns `None` otherwise.

**manifest** `ArtifactManifest`

The artifact's manifest.

The manifest lists all of its contents, and can't be changed once the artifact
has been logged.

**metadata** `dict`

User-defined artifact metadata.

Structured data associated with the artifact.

**name** `str`

The artifact name and version of the artifact.

A string with the format `{collection}:{alias}`. If fetched before an artifact is
logged/saved, the name won't contain the alias.
If the artifact is a link, the name will be the name of the linked artifact.

**project** `str`

The name of the project that the artifact collection belongs to.

If the artifact is a link, the project will be the project of the linked artifact.

**qualified\_name** `str`

The entity/project/name of the artifact.

If the artifact is a link, the qualified name will be the qualified name of the
linked artifact path.

**size** `int`

The total size of the artifact in bytes.

Includes any references tracked by this artifact.

**source\_artifact** `Artifact`

Returns the source artifact, which is the original logged artifact.

If this artifact is a source artifact (`artifact.is_link == False`),
it will return itself.

**source\_collection** `ArtifactCollection`

The artifact's source collection.

The source collection is the collection that the artifact was logged from.

**source\_entity** `str`

The name of the entity of the source artifact.

**source\_name** `str`

The artifact name and version of the source artifact.

A string with the format `{source_collection}:{alias}`. Before the artifact
is saved, contains only the name since the version is not yet known.

**source\_project** `str`

The name of the project of the source artifact.

**source\_qualified\_name** `str`

The source\_entity/source\_project/source\_name of the source artifact.

**source\_version** `str`

The source artifact's version.

A string with the format `v{number}`.

**state** `str`

The status of the artifact. One of: "PENDING", "COMMITTED", or "DELETED".

**tags** `list[str]`

List of one or more tags assigned to this artifact version.

**ttl** `timedelta | None`

The time-to-live (TTL) policy of an artifact.

Artifacts are deleted shortly after a TTL policy's duration passes.
If set to `None`, the artifact deactivates TTL policies and will be not
scheduled for deletion, even if there is a team default TTL.
An artifact inherits a TTL policy from
the team default if the team administrator defines a default
TTL and there is no custom policy set on an artifact.

**type** `str`

The artifact's type. Common types include `dataset` or `model`.

**updated\_at** `str`

The time when the artifact was last updated.

**url** `The URL of the artifact.`

Constructs the URL of the artifact.

**use\_as** `str | None`

Deprecated.

**version** `str`

The artifact's version.

A string with the format `v{number}`.
If this is a link artifact, the version will be from the linked collection.

## Methods

### method Artifact.add()

```python theme={"system"}
self,
obj: 'WBValue',
name: 'StrPath',
overwrite: 'bool' = False
```

Add wandb.WBValue `obj` to the artifact.

##### Arguments

**obj** `WBValue`

The object to add. Currently support one of Bokeh, JoinedTable, PartitionedTable, Table, Classes, ImageMask, BoundingBoxes2D, Audio, Image, Video, Html, Object3D

**name** `StrPath`

The path within the artifact to add the object.

**overwrite** `bool`

If True, overwrite existing objects with the same file path if applicable.

##### Raises

* `ArtifactFinalizedError`: You cannot make changes to the current artifact version because it is finalized. Log a new artifact version instead.

### method Artifact.add\_dir()

```python theme={"system"}
self,
local_path: 'str',
name: 'str | None' = None,
skip_cache: 'bool | None' = False,
policy: "Literal['mutable', 'immutable'] | None" = 'mutable',
merge: 'bool' = False
```

Add a local directory to the artifact.

##### Arguments

**local\_path** `str`

The path of the local directory.

**name** `str | None`

The subdirectory name within an artifact. The name you specify appears in the W\&B App UI nested by artifact's `type`. Defaults to the root of the artifact.

**skip\_cache** `bool | None`

If set to `True`, W\&B will not copy/move files to the cache while uploading

**policy** `Literal['mutable', 'immutable'] | None`

By default, "mutable".

* mutable: Create a temporary copy of the file to prevent
  corruption during upload.
* immutable: Disable protection, rely on the user not to delete
  or change the file.

**merge** `bool`

If `False` (default), throws ValueError if a file was already added in a previous add\_dir call and its content has changed. If `True`, overwrites existing files with changed content. Always adds new files and never removes files. To replace an entire directory, pass a name when adding the directory using `add_dir(local_path, name=my_prefix)` and call `remove(my_prefix)` to remove the directory, then add it again.

##### Raises

* `ArtifactFinalizedError`: You cannot make changes to the current artifact version because it is finalized. Log a new artifact version instead.
* `ValueError`: Policy must be "mutable" or "immutable"

### method Artifact.add\_file()

```python theme={"system"}
self,
local_path: 'str',
name: 'str | None' = None,
is_tmp: 'bool | None' = False,
skip_cache: 'bool | None' = False,
policy: "Literal['mutable', 'immutable'] | None" = 'mutable',
overwrite: 'bool' = False
```

Add a local file to the artifact.

##### Arguments

**local\_path** `str`

The path to the file being added.

**name** `str | None`

The path within the artifact to use for the file being added. Defaults to the basename of the file.

**is\_tmp** `bool | None`

If true, then the file is renamed deterministically to avoid collisions.

**skip\_cache** `bool | None`

If `True`, do not copy files to the cache after uploading.

**policy** `Literal['mutable', 'immutable'] | None`

By default, set to "mutable". If set to "mutable", create a temporary copy of the file to prevent corruption during upload. If set to "immutable", disable protection and rely on the user not to delete or change the file.

**overwrite** `bool`

If `True`, overwrite the file if it already exists.

##### Raises

* `ArtifactFinalizedError`: You cannot make changes to the current artifact version because it is finalized. Log a new artifact version instead.
* `ValueError`: Policy must be "mutable" or "immutable"

### method Artifact.add\_reference()

```python theme={"system"}
self,
uri: 'ArtifactManifestEntry | str',
name: 'StrPath | None' = None,
checksum: 'bool' = True,
max_objects: 'int | None' = None
```

Add a reference denoted by a URI to the artifact.

Unlike files or directories that you add to an artifact, references are not
uploaded to W\&B. For more information,
see [Track external files](https://docs.wandb.ai/models/artifacts/track-external-files).

By default, the following schemes are supported:

* http(s): The size and digest of the file will be inferred by the
  `Content-Length` and the `ETag` response headers returned by the server.
* s3: The checksum and size are pulled from the object metadata.
  If bucket versioning is enabled, then the version ID is also tracked.
* gs: The checksum and size are pulled from the object metadata. If bucket
  versioning is enabled, then the version ID is also tracked.
* https, domain matching `*.blob.core.windows.net`
* Azure: The checksum and size are be pulled from the blob metadata.
  If storage account versioning is enabled, then the version ID is
  also tracked.
* file: The checksum and size are pulled from the file system. This scheme
  is useful if you have an NFS share or other externally mounted volume
  containing files you wish to track but not necessarily upload.

For any other scheme, the digest is just a hash of the URI and the size is left
blank.

##### Arguments

**uri** `ArtifactManifestEntry | str`

The URI path of the reference to add. The URI path can be an object returned from `Artifact.get_entry` to store a reference to another artifact's entry.

**name** `StrPath | None`

The path within the artifact to place the contents of this reference.

**checksum** `bool`

Whether or not to checksum the resource(s) located at the reference URI. Checksumming is strongly recommended as it enables automatic integrity validation. Disabling checksumming will speed up artifact creation but reference directories will not iterated through so the objects in the directory will not be saved to the artifact. We recommend setting `checksum=False` when adding reference objects, in which case a new version will only be created if the reference URI changes.

**max\_objects** `int | None`

The maximum number of objects to consider when adding a reference that points to directory or bucket store prefix. By default, the maximum number of objects allowed for Amazon S3, GCS, Azure, and local files is 10,000,000. Other URI schemas do not have a maximum.

##### Raises

* `ArtifactFinalizedError`: You cannot make changes to the current artifact version because it is finalized. Log a new artifact version instead.

### method Artifact.checkout()

```python theme={"system"}
self,
root: 'str | None' = None
```

Replace the specified root directory with the contents of the artifact.

WARNING: This will delete all files in `root` that are not included in the
artifact.

##### Arguments

**root** `str | None`

The directory to replace with this artifact's files.

##### Raises

* `ArtifactNotLoggedError`: If the artifact is not logged.

### method Artifact.delete()

```python theme={"system"}
self,
delete_aliases: 'bool' = False
```

Delete an artifact and its files.

If called on a linked artifact, only the link is deleted, and the
source artifact is unaffected.

Use `Artifact.unlink()` instead of `Artifact.delete()` to remove a
link between a source artifact and a collection.

##### Arguments

**delete\_aliases** `bool`

If set to `True`, delete all aliases associated with the artifact. If `False`, raise an exception if the artifact has existing aliases. This parameter is ignored if the artifact is retrieved from a collection it is linked to.

##### Raises

* `ArtifactNotLoggedError`: If the artifact is not logged.

### method Artifact.download()

```python theme={"system"}
self,
root: 'StrPath | None' = None,
allow_missing_references: 'bool' = False,
skip_cache: 'bool | None' = None,
path_prefix: 'StrPath | None' = None,
multipart: 'bool | None' = None
```

Download the contents of the artifact to the specified root directory.

Existing files located within `root` are not modified. Explicitly delete `root`
before you call `download` if you want the contents of `root` to exactly match
the artifact.

##### Arguments

**root** `StrPath | None`

The directory W\&B stores the artifact's files.

**allow\_missing\_references** `bool`

If set to `True`, any invalid reference paths will be ignored while downloading referenced files.

**skip\_cache** `bool | None`

If set to `True`, the artifact cache will be skipped when downloading and W\&B will download each file into the default root or specified download directory.

**path\_prefix** `StrPath | None`

If specified, only files with a path that starts with the given prefix will be downloaded. Uses unix format (forward slashes).

**multipart** `bool | None`

If set to `None` (default), the artifact will be downloaded in parallel using multipart download if individual file size is greater than 2GB. If set to `True` or `False`, the artifact will be downloaded in parallel or serially regardless of the file size.

##### Raises

* `ArtifactNotLoggedError`: If the artifact is not logged.

### method Artifact.file()

```python theme={"system"}
self,
root: 'str | None' = None
```

Download a single file artifact to the directory you specify with `root`.

##### Arguments

**root** `str | None`

The root directory to store the file. Defaults to `./artifacts/self.name/`.

##### Raises

* `ArtifactNotLoggedError`: If the artifact is not logged.
* `ValueError`: If the artifact contains more than one file.

### method Artifact.files()

```python theme={"system"}
self,
names: 'list[str] | None' = None,
per_page: 'int' = 50,
start: 'str | None' = None
```

Iterate over all files stored in this artifact.

##### Arguments

**names** `list[str] | None`

The filename paths relative to the root of the artifact you wish to list.

**per\_page** `int`

The number of files to return per request.

**start** `str | None`

Pagination cursor for resuming a past query, captured from a previous paginator's `.cursor` attribute.

##### Raises

* `ArtifactNotLoggedError`: If the artifact is not logged.

### method Artifact.finalize()

```python theme={"system"}
self
```

Finalize the artifact version.

You cannot modify an artifact version once it is finalized because the artifact
is logged as a specific artifact version. Create a new artifact version
to log more data to an artifact. An artifact is automatically finalized
when you log the artifact with `log_artifact`.

### method Artifact.get()

```python theme={"system"}
self,
name: 'str'
```

Get the WBValue object located at the artifact relative `name`.

##### Arguments

**name** `str`

The artifact relative name to retrieve.

##### Raises

* `ArtifactNotLoggedError`: if the artifact isn't logged or the run is offline.

### method Artifact.get\_added\_local\_path\_name()

```python theme={"system"}
self,
local_path: 'str'
```

Get the artifact relative name of a file added by a local filesystem path.

##### Arguments

**local\_path** `str`

The local path to resolve into an artifact relative name.

### method Artifact.get\_entry()

```python theme={"system"}
self,
name: 'StrPath'
```

Get the entry with the given name.

##### Arguments

**name** `StrPath`

The artifact relative name to get

##### Raises

* `ArtifactNotLoggedError`: if the artifact isn't logged or the run is offline.
* `KeyError`: if the artifact doesn't contain an entry with the given name.

### method Artifact.get\_path()

```python theme={"system"}
self,
name: 'StrPath'
```

Deprecated. Use `get_entry(name)`.

##### Arguments

**name** `StrPath`

No description provided.

### method Artifact.is\_draft()

```python theme={"system"}
self
```

Check if artifact is not saved.

### method Artifact.json\_encode()

```python theme={"system"}
self
```

Returns the artifact encoded to the JSON format.

### method Artifact.link()

```python theme={"system"}
self,
target_path: 'str',
aliases: 'Iterable[str] | None' = None
```

Link this artifact to a collection.

##### Arguments

**target\_path** `str`

The path of the collection. Path consists of the prefix "wandb-registry-" along with the registry name and the collection name `wandb-registry-{REGISTRY_NAME}/{COLLECTION_NAME}`.

**aliases** `Iterable[str] | None`

Add one or more aliases to the linked artifact. The "latest" alias is automatically applied to the most recent artifact you link.

##### Raises

* `ArtifactNotLoggedError`: If the artifact is not logged.

### method Artifact.logged\_by()

```python theme={"system"}
self
```

Get the W\&B run that originally logged the artifact.

##### Raises

* `ArtifactNotLoggedError`: If the artifact is not logged.

### method Artifact.new\_draft()

```python theme={"system"}
self
```

Create a new draft artifact with the same content as this committed artifact.

Modifying an existing artifact creates a new artifact version known
as an "incremental artifact". The artifact returned can be extended or
modified and logged as a new version.

##### Raises

* `ArtifactNotLoggedError`: If the artifact is not logged.

### method Artifact.new\_file()

```python theme={"system"}
self,
name: 'str',
mode: 'str' = 'x',
encoding: 'str | None' = None,
policy: "Literal['mutable', 'immutable']" = 'mutable'
```

Open a new temporary file and add it to the artifact.

##### Arguments

**name** `str`

The name of the new file to add to the artifact.

**mode** `str`

The file access mode to use to open the new file.

**encoding** `str | None`

The encoding used to open the new file.

**policy** `Literal['mutable', 'immutable']`

By default, set to "mutable". If set to "mutable", create a temporary copy of the file to prevent corruption during upload. If set to "immutable", disable protection and rely on the user not to delete or change the file.

##### Raises

* `ArtifactFinalizedError`: You cannot make changes to the current artifact version because it is finalized. Log a new artifact version instead.

### method Artifact.remove()

```python theme={"system"}
self,
item: 'StrPath | ArtifactManifestEntry'
```

Remove an item from the artifact.

##### Arguments

**item** `StrPath | ArtifactManifestEntry`

The item to remove. Can be a specific manifest entry or the name of an artifact-relative path. If the item matches a directory all items in that directory will be removed.

##### Raises

* `ArtifactFinalizedError`: You cannot make changes to the current artifact version because it is finalized. Log a new artifact version instead.
* `FileNotFoundError`: If the item isn't found in the artifact.

### method Artifact.save()

```python theme={"system"}
self,
project: 'str | None' = None,
settings: 'wandb.Settings | None' = None
```

Persist any changes made to the artifact.

If currently in a run, that run will log this artifact. If not currently in a
run, a run of type "auto" is created to track this artifact.

##### Arguments

**project** `str | None`

A project to use for the artifact in the case that a run is not already in context.

**settings** `wandb.Settings | None`

A settings object to use when initializing an automatic run. Most commonly used in testing harness.

### method Artifact.unlink()

```python theme={"system"}
self
```

Unlink this artifact if it is a linked member of an artifact collection.

##### Raises

* `ArtifactNotLoggedError`: If the artifact is not logged.
* `ValueError`: If the artifact is not linked to any collection.

### method Artifact.used\_by()

```python theme={"system"}
self
```

Get a list of the runs that have used this artifact and its linked artifacts.

##### Raises

* `ArtifactNotLoggedError`: If the artifact is not logged.

### method Artifact.verify()

```python theme={"system"}
self,
root: 'str | None' = None
```

Verify that the contents of an artifact match the manifest.

All files in the directory are checksummed and the checksums are then
cross-referenced against the artifact's manifest. References are not verified.

##### Arguments

**root** `str | None`

The directory to verify. If None artifact will be downloaded to './artifacts/self.name/'.

##### Raises

* `ArtifactNotLoggedError`: If the artifact is not logged.
* `ValueError`: If the verification fails.

### method Artifact.wait()

```python theme={"system"}
self,
timeout: 'int | None' = None
```

If needed, wait for this artifact to finish logging.

##### Arguments

**timeout** `int | None`

The time, in seconds, to wait.
