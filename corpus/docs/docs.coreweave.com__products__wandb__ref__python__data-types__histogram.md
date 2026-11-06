# Histogram

Source: https://docs.coreweave.com/products/wandb/ref/python/data-types/histogram

# Histogram

[View source](https://github.com/wandb/wandb/blob/main/wandb/sdk/data_types/histogram.py#L20)

## Class wandb.Histogram

W\&B class for histograms.

This object works just like numpy's histogram function
[https://docs.scipy.org/doc/numpy/reference/generated/numpy.histogram.html](https://docs.scipy.org/doc/numpy/reference/generated/numpy.histogram.html)

```python theme={"system"}
sequence: 'Sequence | None' = None,
np_histogram: 'NumpyHistogram | None' = None,
num_bins: 'int' = 64
```

## Args

**sequence** `Sequence | None`

Input data for histogram.

**np\_histogram** `NumpyHistogram | None`

Alternative input of a precomputed histogram.

**num\_bins** `int`

Number of bins for the histogram.  The default number of bins is 64. The maximum number of bins is 512.

## Attributes

* `bins` (`[float]`): Edges of bins
* `histogram` (`[int]`): Number of elements falling in each bin.
