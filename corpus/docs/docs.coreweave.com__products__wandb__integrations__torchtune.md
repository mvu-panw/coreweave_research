# PyTorch torchtune

Source: https://docs.coreweave.com/products/wandb/integrations/torchtune

# PyTorch torchtune

> Use Weights & Biases in PyTorch torchtune to track LLM fine-tuning experiments with the WandBLogger metric logger.

[Try in Colab](https://colab.research.google.com/github/wandb/examples/blob/master/colabs/torchtune/torchtune_and_wandb.ipynb)

[torchtune](https://meta-pytorch.org/torchtune/stable/index.html) is a PyTorch-based library that streamlines authoring, fine-tuning, and experimentation for LLMs. torchtune also has built-in support for [logging with Weights & Biases](https://meta-pytorch.org/torchtune/stable/deep_dives/wandb_logging.html), which enhances tracking and visualization of training processes.

This guide shows you how to enable Weights & Biases logging in torchtune recipes, configure the `WandBLogger` metric logger, understand which metrics torchtune tracks by default, and save model checkpoints to W\&B Artifacts.

![torchtune training dashboard](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/_media/torchtune_dashboard.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=66901c71786a69ac2bae0cc5e04dbec4)

Check the Weights & Biases blog post on [Fine-tuning Mistral 7B using torchtune](https://forge.coreweave.com/wandb/capecape/torchtune-mistral/reports/torchtune-The-new-PyTorch-LLM-fine-tuning-library---Vmlldzo3NTUwNjM0).

## Enable Weights & Biases logging

You can enable Weights & Biases logging in two ways: override arguments at launch from the command line, or edit the recipe's config file. Choose whichever fits your workflow.

> [tab] Command line
>
> Override command-line arguments at launch:
>
> ```bash theme={"system"}
> tune run lora_finetune_single_device --config llama3/8B_lora_single_device \
>   metric_logger._component_=torchtune.utils.metric_logging.WandBLogger \
>   metric_logger.project="llama3_lora" \
>   log_every_n_steps=5
> ```

> [tab] Recipe
>
> Enable Weights & Biases logging on the recipe's config:
>
> ```yaml theme={"system"}
> # inside llama3/8B_lora_single_device.yaml
> metric_logger:
>   _component_: torchtune.utils.metric_logging.WandBLogger
>   project: llama3_lora
> log_every_n_steps: 5
> ```

## Use the Weights & Biases metric logger

Enable Weights & Biases logging on the recipe's config file by modifying the `metric_logger` section. Change the `_component_` to `torchtune.utils.metric_logging.WandBLogger` class. You can also pass a `project` name and `log_every_n_steps` to customize the logging behavior.

You can also pass any other `kwargs` as you would to the [wandb.init()](https://docs.coreweave.com/products/wandb/ref/python/functions/init.md) method. For example, if you work on a team, you can pass the `entity` argument to the `WandBLogger` class to specify the team name.

> [tab] Recipe
>
> ```yaml theme={"system"}
> # inside llama3/8B_lora_single_device.yaml
> metric_logger:
>   _component_: torchtune.utils.metric_logging.WandBLogger
>   project: llama3_lora
>   entity: my_project
>   job_type: lora_finetune_single_device
>   group: my_awesome_experiments
> log_every_n_steps: 5
> ```

> [tab] Command line
>
> ```shell theme={"system"}
> tune run lora_finetune_single_device --config llama3/8B_lora_single_device \
>   metric_logger._component_=torchtune.utils.metric_logging.WandBLogger \
>   metric_logger.project="llama3_lora" \
>   metric_logger.entity="my_project" \
>   metric_logger.job_type="lora_finetune_single_device" \
>   metric_logger.group="my_awesome_experiments" \
>   log_every_n_steps=5
> ```

## Logged data

After you enable Weights & Biases logging, you can explore the Weights & Biases dashboard to see the logged metrics. By default, Weights & Biases logs all of the hyperparameters from the config file and the launch overrides, so you have a record of each run's configuration alongside its metrics.

Weights & Biases captures the resolved config on the **Overview** tab. Weights & Biases also stores the config in YAML format on the [Files tab](https://forge.coreweave.com/wandb/capecape/torchtune/runs/joyknwwa/files).

![torchtune configuration](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/_media/torchtune_config.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=25aa802a1a9e13005aadf0a1773690e2)

### Logged metrics

Each recipe has its own training loop. Check each individual recipe to see its logged metrics, which include these by default:

| Metric | Description |
| - | - |
| `loss` | The loss of the model. |
| `lr` | The learning rate. |
| `tokens_per_second` | The tokens per second of the model. |
| `grad_norm` | The gradient norm of the model. |
| `global_step` | Corresponds to the current step in the training loop. Accounts for gradient accumulation. Each time an optimizer step runs, the model updates, the gradients accumulate, and the model updates once every `gradient_accumulation_steps`. |

> [!NOTE]
>
> `global_step` isn't the same as the number of training steps. It corresponds to the current step in the training loop and accounts for gradient accumulation. Each time an optimizer step runs, `global_step` increments by 1. For example, if the dataloader has 10 batches, gradient accumulation steps is 2, and you run for 3 epochs, the optimizer steps 15 times, so `global_step` ranges from 1 to 15.

The design of torchtune lets you add custom metrics or modify existing ones. Modify the corresponding [recipe file](https://github.com/meta-pytorch/torchtune/tree/main/recipes). For example, you can log `current_epoch` as a percentage of the total number of epochs like this:

```python theme={"system"}
# inside `train.py` function in the recipe file
self._metric_logger.log_dict(
    {"current_epoch": self.epochs * self.global_step / self._steps_per_epoch},
    step=self.global_step,
)
```

> [!NOTE]
>
> The set of logged metrics can change between torchtune releases. To add a custom metric, modify the recipe and call the corresponding `self._metric_logger.*` function.

## Save and load checkpoints

Save checkpoints to W\&B Artifacts to version model weights alongside the metrics and configuration of each run, so you can reproduce results and compare model versions later.

The torchtune library supports several [checkpoint formats](https://meta-pytorch.org/torchtune/stable/deep_dives/checkpointer.html). Depending on the origin of the model you use, you must switch to the appropriate [checkpointer class](https://meta-pytorch.org/torchtune/stable/deep_dives/checkpointer.html).

To save the model checkpoints to [W\&B Artifacts](https://docs.coreweave.com/products/wandb/artifacts.md), the recommended approach is to override the `save_checkpoint` functions inside the corresponding recipe.

The following example shows how to override the `save_checkpoint` function to save the model checkpoints to W\&B Artifacts.

```python theme={"system"}
def save_checkpoint(self, epoch: int) -> None:
    ...
    ## Save the checkpoint to W&B.
    ## The file name depends on the Checkpointer Class.
    ## The following is an example for the full_finetune case.
    checkpoint_file = Path.joinpath(
        self._checkpointer._output_dir, f"torchtune_model_{epoch}"
    ).with_suffix(".pt")
    wandb_artifact = wandb.Artifact(
        name=f"torchtune_model_{epoch}",
        type="model",
        # description of the model checkpoint
        description="Model checkpoint",
        # you can add whatever metadata you want as a dict
        metadata={
            utils.SEED_KEY: self.seed,
            utils.EPOCHS_KEY: self.epochs_run,
            utils.TOTAL_EPOCHS_KEY: self.total_epochs,
            utils.MAX_STEPS_KEY: self.max_steps_per_epoch,
        },
    )
    wandb_artifact.add_file(checkpoint_file)
    wandb.log_artifact(wandb_artifact)
```
