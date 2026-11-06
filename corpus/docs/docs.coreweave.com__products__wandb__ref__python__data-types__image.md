# Image

Source: https://docs.coreweave.com/products/wandb/ref/python/data-types/image

# Image

[View source](https://github.com/wandb/wandb/blob/main/wandb/sdk/data_types/image.py#L47)

## Class wandb.Image

A class for logging images to W\&B.

```python theme={"system"}
data_or_path: 'ImageDataOrPathType',
mode: 'str | None' = None,
caption: 'str | None' = None,
grouping: 'int | None' = None,
classes: 'Classes | Sequence[dict] | None' = None,
boxes: 'dict[str, BoundingBoxes2D] | dict[str, dict] | None' = None,
masks: 'dict[str, ImageMask] | dict[str, dict] | None' = None,
file_type: 'str | None' = None
```

## Args

**data\_or\_path** `ImageDataOrPathType`

Accepts NumPy array/pytorch tensor of image data,
a PIL image object, or a path to an image file. If a NumPy
array or pytorch tensor is provided,
the image data will be saved to the given file type.
Values are expected to already be in the range \[0, 255].

* pytorch tensor should be in the format (channel, height, width)
* NumPy array should be in the format (height, width, channel)

**mode** `str | None`

The PIL mode for an image. Most common are "L", "RGB", "RGBA". Full Pillow docs for more information [https://pillow.readthedocs.io/en/stable/handbook/concepts.html#modes](https://pillow.readthedocs.io/en/stable/handbook/concepts.html#modes)

**caption** `str | None`

Label for display of image.

**grouping** `int | None`

The grouping number for the image.

**classes** `Classes | Sequence[dict] | None`

A list of class information for the image, used for labeling bounding boxes, and image masks.

**boxes** `dict[str, BoundingBoxes2D] | dict[str, dict] | None`

A dictionary containing bounding box information for the image. see [https://docs.wandb.ai/models/ref/python/data-types/boundingboxes2d](https://docs.wandb.ai/models/ref/python/data-types/boundingboxes2d)

**masks** `dict[str, ImageMask] | dict[str, dict] | None`

A dictionary containing mask information for the image. see [https://docs.wandb.ai/models/ref/python/data-types/imagemask](https://docs.wandb.ai/models/ref/python/data-types/imagemask)

**file\_type** `str | None`

The file type to save the image as. This parameter has no effect if `data_or_path` is a path to an image file.

## Properties

**image** `PILImage | None`

No description provided.
