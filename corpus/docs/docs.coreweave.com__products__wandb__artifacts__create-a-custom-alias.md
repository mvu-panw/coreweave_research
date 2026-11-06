# Create an artifact alias

Source: https://docs.coreweave.com/products/wandb/artifacts/create-a-custom-alias

> Create and manage custom aliases to reference specific W&B artifact versions by meaningful names like best or production.

# Create an artifact alias

Use aliases as pointers to specific versions. By default, `wandb.Run.log_artifact()` adds the `latest` alias to the logged version.

Weights & Biases creates an artifact version `v0` and attaches it to your artifact when you log that artifact for the first time. Weights & Biases checksums the contents when you log again to the same artifact. If the artifact changed, Weights & Biases saves a new version `v1`.

For example, if you want your training script to pull the most recent version of a dataset, specify `latest` when you use that artifact. The following code example demonstrates how to download a recent dataset artifact named `bike-dataset` that has an alias, `latest`:

```python theme={"system"}
import wandb

with wandb.init(project="<project>") as run:
    artifact = run.use_artifact("bike-dataset:latest")
    artifact.download()
```

You can also apply a custom alias to an artifact version. For example, if you want to mark that model checkpoint is the best on the metric AP-50, you could add the string `'best-ap50'` as an alias when you log the model artifact.

```python theme={"system"}
with wandb.init(project="<project>") as run:
    artifact = wandb.Artifact("run-3nq3ctyy-bike-model", type="model")
    artifact.add_file("model.h5")
    run.log_artifact(artifact, aliases=["latest", "best-ap50"])
```
