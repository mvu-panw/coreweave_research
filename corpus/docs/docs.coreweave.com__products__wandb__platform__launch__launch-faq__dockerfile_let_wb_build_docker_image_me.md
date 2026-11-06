# Can I specify a Dockerfile and let Weights & Biases build a Docker image for me?

Source: https://docs.coreweave.com/products/wandb/platform/launch/launch-faq/dockerfile_let_wb_build_docker_image_me

# Can I specify a Dockerfile and let Weights & Biases build a Docker image for me?

Yes. You can provide your own Dockerfile and have W\&B Launch build the image for your run. This lets you control the build environment while still using Launch to queue and run jobs. This approach works well for projects with stable requirements but changing codebases.

> [!WARNING]
>
> Format your Dockerfile to use mounts. For details, see the [Docker mounts documentation](https://docs.docker.com/build/guide/mounts/).

After you configure the Dockerfile, specify it to Weights & Biases in one of the following ways:

* Use `Dockerfile.wandb`
* Use W\&B CLI
* Use W\&B App

> [tab] Dockerfile.wandb
>
> Include a `Dockerfile.wandb` file in the same directory as the W\&B run's entrypoint. Weights & Biases uses this file instead of the built-in Dockerfile.

> [tab] W\&B CLI
>
> To queue a job, use the `--dockerfile` flag with the `wandb launch` command:
>
> ```bash theme={"system"}
> wandb launch --dockerfile path/to/Dockerfile
> ```

> [tab] W\&B App
>
> When you add a job to a queue in the W\&B App, provide the Dockerfile path in the **Overrides** section. Enter it as a key-value pair with `"dockerfile"` as the key and the path as the value.
>
> The following JSON shows how to include a Dockerfile from a local directory:
>
> ```json title="Launch job W&B App" theme={"system"}
> {
>   "args": [],
>   "run_config": {
>     "lr": 0,
>     "batch_size": 0,
>     "epochs": 0
>   },
>   "entrypoint": [],
>   "dockerfile": "./Dockerfile"
> }
> ```
