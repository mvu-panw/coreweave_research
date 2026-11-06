# Track external files

Source: https://docs.coreweave.com/products/wandb/artifacts/track-external-files

> Track files saved in an external bucket, HTTP file server, or an NFS share.

# Track external files

Use *reference artifacts* to track and use files saved outside of Weights & Biases servers. Common external storage solutions include: CoreWeave AI Object Storage, Backblaze B2 Cloud Storage, an Amazon Simple Storage Service (Amazon S3) bucket, GCS bucket, Azure blob, HTTP file server, or NFS share.

Reference artifacts behave similar to non-reference artifacts. The key difference is that the reference artifacts only consists of metadata about the files, such as their sizes and MD5 checksums. The files themselves never leave your system.

You can interact with reference artifact similarly to non-reference artifacts. In the W\&B App, you can browse the contents of the reference artifact using the file browser, explore the full dependency graph, and scan through the versioned history of your artifact. However, the UI cannot render rich media such as images, audio, because the data itself is not contained within the artifact.

> [!NOTE]
>
> If you log an artifact that does not track external files, Weights & Biases saves the artifact's files to Weights & Biases servers. This is the default behavior when you log artifacts with the W\&B Python SDK.
>
> If you log an artifact that tracks external files, Weights & Biases logs metadata about the object, such as the object's ETag and size. If object versioning is enabled on the bucket, the version ID is also logged.

The following sections describe how to track external reference artifacts.

## Track an artifact in an external bucket

Use the W\&B Python SDK to track references to files stored outside of Weights & Biases.

1. Initialize a run with `wandb.init()`.
2. Create an artifact object with `wandb.Artifact()`.
3. Specify the reference to the bucket path with the artifact object's `wandb.Artifact.add_reference()` method.
4. Log the artifact's metadata with `run.log_artifact()`.

```python theme={"system"}
import wandb

# Initialize a W&B run
with wandb.init(project="my-project") as run:

  # Create an artifact object
  artifact = wandb.Artifact(name="name", type="type")

  # Add a reference to the bucket path
  artifact.add_reference(uri = "uri/to/your/bucket/path")

  # Log the artifact's metadata
  run.log_artifact(artifact)
```

As an example, suppose your bucket has the following directory structure:

```text theme={"system"}
s3://my-bucket

|datasets/
  |-- mnist/
|models/
  |-- cnn/
```

The `datasets/mnist/` directory contains a collection of images. To track the image `datasets/mnist/` directory as a dataset artifact, specify:

1. Provide a name for the artifact, such as `"mnist"`.
2. Set the `type` parameter to `"dataset"` when you construct the artifact object (`wandb.Artifact(type="dataset")`).
3. Provide the path to the `datasets/mnist/` directory as an Amazon S3 URI (`s3://my-bucket/datasets/mnist/`) when you call `wandb.Artifact.add_reference()`.
4. Log the artifact with `run.log_artifact()`.

The following code sample creates a reference artifact `mnist:latest`:

```python theme={"system"}
import wandb

with wandb.init(project="my-project") as run:
  artifact = wandb.Artifact(name="mnist", type="dataset")
  artifact.add_reference(uri="s3://my-bucket/datasets/mnist")
  run.log_artifact(artifact)
```

Within the W\&B App, you can look through the contents of the reference artifact using the file browser, [explore the full dependency graph](https://docs.coreweave.com/products/wandb/artifacts/explore-and-traverse-an-artifact-graph.md), and scan through the versioned history of your artifact. The W\&B App does not render rich media such as images, audio, and so forth because the data itself is not contained within the artifact.

> [!NOTE]
>
> W\&B Artifacts support any Amazon S3-compatible interface, including CoreWeave Storage, Backblaze B2 Cloud Storage, and MinIO. The scripts described below work as-is with these providers when you set the `AWS_S3_ENDPOINT_URL` environment variable to point at your S3-compatible server (for example, `https://s3.us-west-001.backblazeb2.com` for Backblaze B2).

> [!WARNING]
>
> By default, Weights & Biases imposes a 10,000 object limit when adding an object prefix. You can adjust this limit by specifying `max_objects=` when you call `wandb.Artifact.add_reference()`.

## Download an artifact from an external bucket

Weights & Biases retrieves the files from the underlying bucket when it downloads a reference artifact using the metadata recorded when the artifact is logged. If your bucket has object versioning enabled, Weights & Biases retrieves the object version that corresponds to the state of the file at the time an artifact was logged. As you evolve the contents of your bucket, you can always point to the exact version of your data a given model was trained on, because the artifact serves as a snapshot of your bucket during the training run.

The following code sample shows how to download a reference artifact. The APIs for downloading artifacts are the same for both reference and non-reference artifacts:

```python theme={"system"}
import wandb

with wandb.init(project="my-project") as run:
  artifact = run.use_artifact("mnist:latest", type="dataset")
  artifact_dir = artifact.download()
```

> [!NOTE]
>
> Weights & Biases recommends that you enable 'Object Versioning' on your storage buckets if you overwrite files as part of your workflow.
>
> If versioning is enabled, Weights & Biases can always retrieve the correct version of the file when you download an artifact, even if the file has been overwritten since the artifact was logged.
>
> Based on your use case, read the instructions to enable object versioning: [AWS](https://docs.aws.amazon.com/AmazonS3/latest/userguide/manage-versioning-examples.html), [Google Cloud](https://cloud.google.com/storage/docs/using-object-versioning#set), [Azure](https://learn.microsoft.com/azure/storage/blobs/versioning-enable).

## Add and download an external from a bucket

The following code sample uploads a dataset to an Amazon S3 bucket, tracks it with a reference artifact, then downloads it:

```python theme={"system"}
import boto3
import wandb

with wandb.init() as run:
  # Training here...

  s3_client = boto3.client("s3")
  s3_client.upload_file(file_name="my_model.h5", bucket="my-bucket", object_name="models/cnn/my_model.h5")

  # Log the model artifact
  model_artifact = wandb.Artifact("cnn", type="model")
  model_artifact.add_reference("s3://my-bucket/models/cnn/")
  run.log_artifact(model_artifact)
```

At a later point, you can download the model artifact. Specify the name of the artifact and its type:

```python theme={"system"}
import wandb

with wandb.init() as run:
  artifact = run.use_artifact(artifact_or_name = "cnn", type="model")
  datadir = artifact.download()
```

> [!NOTE]
>
> See the following reports for an end-to-end walkthrough on how to track artifacts by reference for Google Cloud or Azure:
>
> * [Guide to Tracking Artifacts by Reference with Google Cloud](https://forge.coreweave.com/wandb/stacey/artifacts/reports/Tracking-Artifacts-by-Reference--Vmlldzo1NDMwOTE)
> * [Working with Reference Artifacts in Microsoft Azure](https://forge.coreweave.com/wandb/andrea0/azure-2023/reports/Efficiently-Harnessing-Microsoft-Azure-Blob-Storage-with-Weights-Biases--Vmlldzo0NDA2NDgw)

## Cloud storage credentials

Weights & Biases uses the default mechanism to look for credentials based on the cloud provider you use. Read the documentation from your cloud provider to learn more about the credentials used:

| Cloud provider | Credentials Documentation |
| - | - |
| CoreWeave AI Object Storage | [CoreWeave AI Object Storage documentation](https://docs.coreweave.com/products/storage/object-storage/auth-access/manage-access-keys/create-keys.md) |
| Backblaze B2 Cloud Storage | [Backblaze B2 Application Keys documentation](https://www.backblaze.com/docs/cloud-storage-application-keys) |
| AWS | [Boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html#configuring-credentials) |
| Google Cloud | [Google Cloud documentation](https://cloud.google.com/docs/authentication/provide-credentials-adc) |
| Azure | [Azure documentation](https://learn.microsoft.com/python/api/azure-identity/azure.identity.defaultazurecredential?view=azure-python) |

For AWS, if the bucket is not located in the configured user's default region, you must set the `AWS_REGION` environment variable to match the bucket region.

> [!WARNING]
>
> Rich media such as images, audio, video, and point clouds may fail to render in the App UI depending on the CORS configuration of your bucket. Allow listing **app.wandb.ai** in your bucket's CORS settings will allow the W\&B App to properly render such rich media.
>
> If rich media such as images, audio, video, and point clouds does not render in the App UI, ensure that `app.wandb.ai` is allowlisted in your bucket's CORS policy.

## Track an artifact in a filesystem

A common pattern for accessing datasets is to expose an NFS mount point to a remote filesystem on all machines running training jobs. This can be an alternative solution to a cloud storage bucket because from the perspective of the training script, the files appear local to your filesystem.

To track an artifact in a filesystem:

1. Initialize a run with `wandb.init()`.
2. Create an artifact object with `wandb.Artifact()`.
3. Specify the reference to the filesystem path with the artifact object's `wandb.Artifact.add_reference()` method.
4. Log the artifact's metadata with `run.log_artifact()`.

Copy and paste the following code snippet to track files in a mounted filesystem. Replace the values enclosed in angle brackets (`< >`) with your own values.

```python theme={"system"}
import wandb

# Initialize a run
with wandb.init(entity="<entity>", project="<project>") as run:

  # Create an artifact object
  artifact = wandb.Artifact(name="<name>", type="<type>")

  # Add a reference to the filesystem path
  artifact.add_reference("file:///path/to/dataset/")

  # Log the artifact (metadata only)
  run.log_artifact(artifact)
```

Note the triple slash in the URL. The first component is the `file://` prefix that denotes the use of filesystem references. The second component is the root `/` of the filesystem. The remaining components are the path to the directory or file you want to track.

As an example, suppose you have a filesystem mounted at `/mount` with the following structure:

```text theme={"system"}
mount
|datasets/
  |-- mnist/
|models/
  |-- cnn/
```

You want to track the `datasets/mnist/` directory as a dataset artifact. To track it, you could use the following code snippet.

```python theme={"system"}
import wandb

with wandb.init() as run:
  artifact = wandb.Artifact("mnist", type="dataset")
  artifact.add_reference("file:///mount/datasets/mnist/")
  run.log_artifact(artifact)
```

This creates a reference artifact `mnist:latest` that points to the files stored under `/mount/datasets/mnist/`.

> [!WARNING]
>
> By default, Weights & Biases imposes a 10,000 file limit when adding a reference to a directory. You can adjust this limit by specifying `max_objects=` when you call `wandb.Artifact.add_reference()`.

Similarly, to track a model stored at `models/cnn/my_model.h5`, you could use the following code snippet:

```python theme={"system"}
import wandb

with wandb.init() as run:

  # Training here...

  # Write model to disk

  # Create an artifact object
  model_artifact = wandb.Artifact("cnn", type="model")

  # Add a reference to the model file path
  model_artifact.add_reference("file:///mount/cnn/my_model.h5")

  # Log the artifact to W&B
  run.log_artifact(model_artifact)
```

## Download an artifact from an external filesystem

Download files from a referenced filesystem using the same APIs as non-reference artifacts:

1. Initialize a run with `wandb.init()`.
2. Use the `wandb.Run.use_artifact()` method to indicate the artifact you want to download.
3. Call the artifact's `wandb.Artifact.download()` method to download the files from the referenced filesystem

```python theme={"system"}
with wandb.init() as run:
  artifact = run.use_artifact("entity/project/mnist:latest", type="dataset")
  artifact_dir = artifact.download()
```

Weights & Biases copies the contents of `/mount/datasets/mnist` to the `artifacts/mnist:v0/` directory.

> [!NOTE]
>
> `Artifact.download()` throws an error if it cannot reconstruct the artifact. For example, if an artifact contains a reference to a file that was overwritten, `Artifact.download()` will throw an error because the artifact can no longer be reconstructed.
