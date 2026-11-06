# I don't want Weights & Biases to build a container for me, can I still use Launch?

Source: https://docs.coreweave.com/products/wandb/platform/launch/launch-faq/build_container_launch

# I don't want Weights & Biases to build a container for me, can I still use Launch?

To launch a pre-built Docker image, replace the `<>` placeholders with your values and run:

```bash theme={"system"}
wandb launch -d <docker-image-uri> -q <queue-name> -E <entrypoint>
```

This command creates a job and starts a run.

To create a job from an image, run:

```bash theme={"system"}
wandb job create image <image-name> -p <project> -e <entity>
```
