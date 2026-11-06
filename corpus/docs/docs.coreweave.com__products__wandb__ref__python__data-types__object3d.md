# Object3D

Source: https://docs.coreweave.com/products/wandb/ref/python/data-types/object3d

# Object3D

[View source](https://github.com/wandb/wandb/blob/main/wandb/sdk/data_types/object_3d.py#L245)

## Class wandb.Object3D

W\&B class for 3D point clouds.

```python theme={"system"}
data_or_path: 'np.ndarray | str | pathlib.Path | TextIO | dict',
caption: 'str | None' = None, **kwargs: 'str | FileFormat3D | None'
```

## Args

**data\_or\_path** `np.ndarray | str | pathlib.Path | TextIO | dict`

Object3D can be initialized from a file or a numpy array.

**caption** `str | None`

Caption associated with the object for display.

**kwargs** `str | FileFormat3D | None`

No description provided.

## Methods

### method Object3D.from\_file()

```python theme={"system"}
data_or_path: 'TextIO | str',
file_type: 'FileFormat3D | None' = None
```

Initializes Object3D from a file or stream.

##### Arguments

**data\_or\_path** `TextIO | str`

A path to a file or a `TextIO` stream.

### method Object3D.from\_numpy()

```python theme={"system"}
data: 'np.ndarray'
```

Initializes Object3D from a numpy array.

### method Object3D.from\_point\_cloud()

```python theme={"system"}
points: 'Sequence[Point]',
boxes: 'Sequence[Box3D]',
vectors: 'Sequence[Vector3D] | None' = None,
point_cloud_type: 'PointCloudType' = 'lidar/beta'
```

Initializes Object3D from a python object.

##### Arguments

**points** `Sequence[Point]`

The points in the point cloud.

**boxes** `Sequence[Box3D]`

3D bounding boxes for labeling the point cloud. Boxes are displayed in point cloud visualizations.

**vectors** `Sequence[Vector3D] | None`

Each vector is displayed in the point cloud visualization. Can be used to indicate directionality of bounding boxes. Defaults to None.
