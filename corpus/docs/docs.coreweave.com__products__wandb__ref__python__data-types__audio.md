# Audio

Source: https://docs.coreweave.com/products/wandb/ref/python/data-types/audio

# Audio

[View source](https://github.com/wandb/wandb/blob/main/wandb/sdk/data_types/audio.py#L19)

## Class wandb.Audio

W\&B class for audio clips.

```python theme={"system"}
(data_or_path: 'str | pathlib.Path | list | np.ndarray',
sample_rate: 'int | None' = None,
caption: 'str | None' = None)
```

## Args

**data\_or\_path** `str | pathlib.Path | list | np.ndarray`

A path to an audio file or a NumPy array of audio data.

**sample\_rate** `int | None`

Sample rate, required when passing in raw NumPy array of audio data.

**caption** `str | None`

Caption to display with audio.

## Methods

### method Audio.durations()

```python theme={"system"}
(audio_list)
```

Calculate the duration of the audio files.

##### Arguments

**audio\_list** `_empty`

No description provided.

### method Audio.sample\_rates()

```python theme={"system"}
(audio_list)
```

Get sample rates of the audio files.

##### Arguments

**audio\_list** `_empty`

No description provided.
