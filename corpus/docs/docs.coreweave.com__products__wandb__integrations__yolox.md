# YOLOX

Source: https://docs.coreweave.com/products/wandb/integrations/yolox

> Use Weights & Biases with YOLOX to track object detection training, log metrics, and visualize detection results.

# YOLOX

[YOLOX](https://github.com/Megvii-BaseDetection/YOLOX) is an anchor-free version of YOLO for object detection. You can use the YOLOX Weights & Biases integration to turn on logging of metrics related to training, validation, and the system, and to interactively validate predictions with a single command-line argument.

This guide shows you how to authenticate with Weights & Biases, install the integration, and enable Weights & Biases logging when you train a YOLOX object detection model so you can track metrics and inspect predictions in the W\&B UI.

## Sign up and create an API key

An API key authenticates your machine to Weights & Biases. You can generate an API key from your user profile.

> [!NOTE]
>
> For a more streamlined approach, go to [User settings](https://forge.coreweave.com/settings) and create an API key. Copy the API key immediately and save it in a secure location such as a password manager.

1. Click the account selector in the upper-right corner.
2. Select **User settings**, then scroll to the **API keys** section.

## Install the `wandb` library and log in

To install the `wandb` library locally and log in:

> [tab] Command line
>
> 1. Set the `WANDB_API_KEY` [environment variable](https://docs.coreweave.com/products/wandb/track/environment-variables.md) to your API key. Replace values enclosed in `<>` with your own:
>
>    ```bash theme={"system"}
>    export WANDB_API_KEY=<your_api_key>
>    ```
>
> 2. Install the `wandb` library and log in.
>
>    ```shell theme={"system"}
>    pip install wandb
>
>    wandb login
>    ```

> [tab] Python
>
> ```bash theme={"system"}
> pip install wandb
> ```
>
> ```python theme={"system"}
> import wandb
> wandb.login()
> ```

> [tab] Python notebook
>
> ```notebook theme={"system"}
> !pip install wandb
>
> import wandb
> wandb.login()
> ```

## Log metrics

With the `wandb` library installed and your machine authenticated, you can enable Weights & Biases logging from the YOLOX training script.

Use the `--logger wandb` command-line argument to turn on logging with `wandb`. Optionally, you can also pass all of the arguments that [`wandb.init()`](https://docs.coreweave.com/products/wandb/ref/python/functions/init) expects. Prepend each argument with `wandb-`.

`num_eval_imges` controls the number of validation set images and predictions that Weights & Biases logs to tables for model evaluation.

Replace the following placeholders before you run the command:

* `<project-name>`: The name of your Weights & Biases project.
* `<entity>`: Your Forge team name.
* `<run-name>`: A name for this training run.
* `<run-id>`: A unique identifier for this run.
* `<save-dir>`: The directory where YOLOX saves checkpoints and logs.
* `<num-images>`: The number of validation images to log.
* `<bool>`: Whether to log checkpoints (`true` or `false`).

```shell theme={"system"}
# Log in to W&B
wandb login

# Call your YOLOX training script with the wandb logger argument
python tools/train.py .... --logger wandb \
                wandb-project <project-name> \
                wandb-entity <entity> \
                wandb-name <run-name> \
                wandb-id <run-id> \
                wandb-save_dir <save-dir> \
                wandb-num_eval_imges <num-images> \
                wandb-log_checkpoints <bool>
```

## Example

After your training run starts, YOLOX streams training, validation, and system metrics to your Weights & Biases project, where you can compare runs and inspect predictions. See the following example for what a populated dashboard looks like.

See the [example dashboard with YOLOX training and validation metrics](https://forge.coreweave.com/wandb/manan-goel/yolox-nano/runs/3pzfeom).

![YOLOX training dashboard](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/_media/yolox_example_dashboard.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=3063b17554512c5e3e577aff228ce855)

If you have questions or issues about this Weights & Biases integration, open an issue in the [YOLOX repository](https://github.com/Megvii-BaseDetection/YOLOX).
