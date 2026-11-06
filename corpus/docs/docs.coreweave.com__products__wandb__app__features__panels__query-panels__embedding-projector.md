# Embed objects

Source: https://docs.coreweave.com/products/wandb/app/features/panels/query-panels/embedding-projector

> Plot multidimensional embeddings on a 2D plane with Embedding Projector using PCA, UMAP, and t-SNE.

# Embed objects

![Embedding projector](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/_media/embedding_projector.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=b15706a1387e149549edb201aa73ce84)

[Embeddings](https://developers.google.com/machine-learning/crash-course/embeddings/video-lecture) represent objects such as people, images, posts, or words with a list of numbers, sometimes referred to as a *vector*. In machine learning and data science use cases, you can generate embeddings using a variety of approaches across a range of applications. This page assumes you're familiar with embeddings and want to visually analyze them inside Weights & Biases.

This guide shows you how to log embeddings to Weights & Biases and use the Embedding Projector to plot them on a 2D plane with dimension reduction algorithms such as PCA, UMAP, and t-SNE. Visualizing embeddings this way helps you explore clusters, inspect relationships between data points, and validate that your embeddings capture the structure you expect.

## Embedding examples

The following resources demonstrate the Embedding Projector in action before you try it yourself:

* [Live interactive demo report](https://forge.coreweave.com/wandb/timssweeney/toy_datasets/reports/Feature-Report-W-B-Embeddings-Projector--VmlldzoxMjg2MjY4?accessToken=bo36zrgl0gref1th5nj59nrft9rc4r71s53zr2qvqlz68jwn8d8yyjdz73cqfyhq)
* [Example Colab](https://colab.research.google.com/drive/1DaKL4lZVh3ETyYEM1oJ46ffjpGs8glXA#scrollTo=D--9i6-gXBm_)

### Hello world

This minimal example shows the smallest amount of code needed to log embeddings and view them in the projector. Weights & Biases lets you log embeddings using the `wandb.Table` class. Consider the following example of three embeddings, each consisting of five dimensions:

```python theme={"system"}
import wandb

with wandb.init(project="embedding_tutorial") as run:
  embeddings = [
      # D1   D2   D3   D4   D5
      [0.2, 0.4, 0.1, 0.7, 0.5],  # embedding 1
      [0.3, 0.1, 0.9, 0.2, 0.7],  # embedding 2
      [0.4, 0.5, 0.2, 0.2, 0.1],  # embedding 3
  ]
  run.log(
      {"embeddings": wandb.Table(columns=["D1", "D2", "D3", "D4", "D5"], data=embeddings)}
  )
  run.finish()
```

After you run the preceding code, the Weights & Biases dashboard contains a new Table with your data. Select **2D Projection** from the upper-right panel selector to plot the embeddings in two dimensions. Weights & Biases automatically selects smart defaults, which you can override in the configuration menu by clicking the gear icon. In this example, Weights & Biases uses all five available numeric dimensions.

![2D projection example](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/_media/weave_hello_world.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=c1648e929a524539cfd247f6f9d022db)

### Digits MNIST

The next example demonstrates a more realistic workflow with higher-dimensional data and richer overlays. While the preceding example shows the basic mechanics of logging embeddings, you typically work with many more dimensions and samples. Consider the MNIST Digits dataset ([UCI ML hand-written digits dataset](https://archive.ics.uci.edu/ml/datasets/Optical+Recognition+of+Handwritten+Digits)) made available through [SciKit-Learn](https://scikit-learn.org/stable/modules/generated/sklearn.datasets.load_digits.html). This dataset has 1,797 records, each with 64 dimensions. The problem is a 10-class classification use case. You can also convert the input data to an image for visualization.

```python theme={"system"}
import wandb
from sklearn.datasets import load_digits

with wandb.init(project="embedding_tutorial") as run:

  # Load the dataset
  ds = load_digits(as_frame=True)
  df = ds.data

  # Create a "target" column
  df["target"] = ds.target.astype(str)
  cols = df.columns.tolist()
  df = df[cols[-1:] + cols[:-1]]

  # Create an "image" column
  df["image"] = df.apply(
      lambda row: wandb.Image(row[1:].values.reshape(8, 8) / 16.0), axis=1
  )
  cols = df.columns.tolist()
  df = df[cols[-1:] + cols[:-1]]

  run.log({"digits": df})
```

After you run the preceding code, the UI again presents a Table. Select **2D Projection** to configure the embedding definition, coloring, algorithm (PCA, UMAP, t-SNE), algorithm parameters, and overlay. In this case, Weights & Biases shows the image when you hover over a point. These are all smart defaults, and you should see something similar with a single click of **2D Projection**. [Interact with this embedding tutorial example](https://forge.coreweave.com/wandb/timssweeney/embedding_tutorial/runs/k6guxhum?workspace=user-timssweeney).

![MNIST digits projection](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/_media/embedding_projector.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=b15706a1387e149549edb201aa73ce84)

## Logging options

The following sections describe the supported ways to structure embedding data when you log it to Weights & Biases. You can log embeddings in several formats:

* **Single embedding column:** Often your data is already in a matrix-like format. In this case, you can create a single embedding column, where the data type of the cell values can be `list[int]`, `list[float]`, or `np.ndarray`.
* **Multiple numeric columns:** The preceding two examples use this approach and create a column for each dimension. Weights & Biases accepts Python `int` or `float` for the cells.

![Single embedding column](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/_media/logging_options.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=d5ab4209fba5d608a754157f4be6ee92)

![Multiple numeric columns](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/_media/logging_option_image_right.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=b8735ef1a300d9a0355846c7afea1da8)

Just like all tables, you have several options for how to construct the table:

* Directly from a **dataframe** using `wandb.Table(dataframe=df)`.
* Directly from a **list of data** using `wandb.Table(data=[...], columns=[...])`.
* Build the table **incrementally row by row** (great if you have a loop in your code). Add rows to your table using `table.add_data(...)`.
* Add an **embedding column** to your table (great if you have a list of predictions in the form of embeddings): `table.add_col("col_name", ...)`.
* Add a **computed column** (great if you have a function or model you want to map over your table): `table.add_computed_columns(lambda row, ndx: {"embedding": model.predict(row)})`.

## Plotting options

After you log your embeddings, you can adjust how they are projected and rendered. After you select **2D Projection**, click the gear icon to edit the rendering settings. Besides selecting the intended columns (see preceding sections), you can select an algorithm of interest along with the desired parameters. The following images show the parameters for UMAP and t-SNE.

![UMAP parameters](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/_media/plotting_options_left.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=681cc6439ac6c33e4fb5c37c7a428275)

![t-SNE parameters](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/_media/plotting_options_right.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=8cf09b9ea80002ee77eab9a7d2512afb)

> [!NOTE]
>
> Weights & Biases downsamples to a random subset of 1,000 rows and 50 dimensions for all three algorithms.
