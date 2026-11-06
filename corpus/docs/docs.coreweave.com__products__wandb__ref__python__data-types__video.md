# Video

Source: https://docs.coreweave.com/products/wandb/ref/python/data-types/video

# Video

[View source](https://github.com/wandb/wandb/blob/main/wandb/sdk/data_types/video.py#L75)

## Class wandb.Video

A class for logging videos to W\&B.

```python theme={"system"}
(data_or_path: 'str | pathlib.Path | np.ndarray | TextIO | BytesIO',
caption: 'str | None' = None,
fps: 'int | None' = None,
format: "Literal['gif', 'mp4', 'webm', 'ogg'] | None" = None)
```

## Args

**data\_or\_path** `str | pathlib.Path | np.ndarray | TextIO | BytesIO`

Video can be initialized with a path to a file or an io object. Video can be initialized with a numpy tensor. The numpy tensor must be either 4 dimensional or 5 dimensional. The dimensions should be (number of frames, channel, height, width) or (batch, number of frames, channel, height, width) The format parameter must be specified with the format argument when initializing with a numpy array or io object.

**caption** `str | None`

Caption associated with the video for display.

**fps** `int | None`

The frame rate to use when encoding raw video frames. Default value is 4. This parameter has no effect when data\_or\_path is a string, or bytes.

**format** `Literal['gif', 'mp4', 'webm', 'ogg'] | None`

Format of video, necessary if initializing with a numpy array or io object. This parameter will be used to determine the format to use when encoding the video data. Accepted values are "gif", "mp4", "webm", or "ogg".
