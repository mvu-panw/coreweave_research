# box3d()

Source: https://docs.coreweave.com/products/wandb/ref/python/functions/box3d

# box3d()

[View source](https://github.com/wandb/wandb/blob/main/wandb/sdk/data_types/object_3d.py#L122)

## function wandb.box3d()

A 3D bounding box. The box is specified by its center, size and orientation.

```python theme={"system"}
*,
center: 'npt.ArrayLike',
size: 'npt.ArrayLike',
orientation: 'npt.ArrayLike',
color: 'RGBColor',
label: 'str | None' = None,
score: 'numeric | None' = None
```

## Args

**center** `npt.ArrayLike`

The center point of the box as a length-3 ndarray.

**size** `npt.ArrayLike`

The box's X, Y and Z dimensions as a length-3 ndarray.

**orientation** `npt.ArrayLike`

The rotation transforming global XYZ coordinates into the box's local XYZ coordinates, given as a length-4 ndarray \[r, x, y, z] corresponding to the non-zero quaternion r + xi + yj + zk.

**color** `RGBColor`

The box's color as an (r, g, b) tuple with `0 <= r,g,b <= 1`.

**label** `str | None`

An optional label for the box.

**score** `numeric | None`

An optional score for the box. Typically used to indicate the confidence of a detection.

## Returns

A Box3D object.

## Examples

The following example creates a point cloud with 60 boxes rotating
around the X, Y and Z axes.

```python theme={"system"}
import wandb

import math
import numpy as np
from scipy.spatial.transform import Rotation


with wandb.init() as run:
    run.log(
        {
            "points": wandb.Object3D.from_point_cloud(
                points=np.random.uniform(-5, 5, size=(100, 3)),
                boxes=[
                    wandb.box3d(
                        center=(0.3 * t - 3, 0, 0),
                        size=(0.1, 0.1, 0.1),
                        orientation=Rotation.from_euler(
                            "xyz", [t * math.pi / 10, 0, 0]
                        ).as_quat(),
                        color=(0.5 + t / 40, 0.5, 0.5),
                        label=f"box {t}",
                        score=0.9,
                    )
                    for t in range(20)
                ]
                + [
                    wandb.box3d(
                        center=(0, 0.3 * t - 3, 0.3),
                        size=(0.1, 0.1, 0.1),
                        orientation=Rotation.from_euler(
                            "xyz", [0, t * math.pi / 10, 0]
                        ).as_quat(),
                        color=(0.5, 0.5 + t / 40, 0.5),
                        label=f"box {t}",
                        score=0.9,
                    )
                    for t in range(20)
                ]
                + [
                    wandb.box3d(
                        center=(0.3, 0.3, 0.3 * t - 3),
                        size=(0.1, 0.1, 0.1),
                        orientation=Rotation.from_euler(
                            "xyz", [0, 0, t * math.pi / 10]
                        ).as_quat(),
                        color=(0.5, 0.5, 0.5 + t / 40),
                        label=f"box {t}",
                        score=0.9,
                    )
                    for t in range(20)
                ],
            ),
        }
    )
```
