# Are there best practices for using Launch effectively?

Source: https://docs.coreweave.com/products/wandb/platform/launch/launch-faq/best_practices_launch_effectively

# Are there best practices for using Launch effectively?

Follow these practices to avoid common setup errors and keep your Launch workflows maintainable:

* Create the queue before you start the agent to streamline configuration. Otherwise, the agent fails with errors until you add a queue.
* Create a Weights & Biases service account to start the agent so that it doesn't link to an individual user account.
* Use `wandb.Run.config` to manage hyperparameters, which lets you overwrite values during job re-runs. For more information about using `argparse`, see [Set the configuration with argparse](https://docs.coreweave.com/products/wandb/track/config.md#set-the-configuration-with-argparse).
