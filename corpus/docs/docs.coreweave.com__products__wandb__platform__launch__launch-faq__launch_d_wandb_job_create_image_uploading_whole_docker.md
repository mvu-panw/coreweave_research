# Is `wandb launch -d` or `wandb job create image` uploading a whole Docker artifact and not pulling from a registry?

Source: https://docs.coreweave.com/products/wandb/platform/launch/launch-faq/launch_d_wandb_job_create_image_uploading_whole_docker

# Is `wandb launch -d` or `wandb job create image` uploading a whole Docker artifact and not pulling from a registry?

No, the `wandb launch -d` command doesn't upload images to a registry. Upload images to a registry separately. Follow these steps:

1. Build an image.
2. Push the image to a registry.

The workflow is as follows. Replace `[REPO-URL]` with your registry URL and `[TAG]` with the image tag:

```bash theme={"system"}
docker build -t [REPO-URL]:[TAG] .
docker push [REPO-URL]:[TAG]
wandb launch -d [REPO-URL]:[TAG]
```

The launch agent then starts a job pointing to the specified container. For examples of configuring agent access to pull images from a container registry, see [Advanced agent setup](https://docs.coreweave.com/products/wandb/platform/launch/setup-agent-advanced.md#agent-configuration).

For Kubernetes, ensure that the Pods in the cluster have access to the registry where the image is pushed.
