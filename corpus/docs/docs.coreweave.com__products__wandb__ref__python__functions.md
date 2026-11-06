# Global Functions overview

Source: https://docs.coreweave.com/products/wandb/ref/python/functions

# Global Functions overview

> Reference for top-level functions in the W&B Python SDK, including init, login, setup, sweep, and agent.

Global functions in W\&B are top-level functions that you call directly, such as `wandb.init()` or `wandb.login()`. Unlike methods that belong to specific classes, these functions provide direct access to W\&B's core functionality without needing to instantiate objects first.

## Available functions

| Function | Description |
| - | - |
| [`init()`](https://docs.coreweave.com/products/wandb/ref/python/functions/init) | Start a new run to track and log to W\&B. This is typically the first function you'll call in your ML training pipeline. |
| [`login()`](https://docs.coreweave.com/products/wandb/ref/python/functions/login) | Set up W\&B login credentials to authenticate your machine with the platform. |
| [`setup()`](https://docs.coreweave.com/products/wandb/ref/python/functions/setup) | Prepare W\&B for use in the current process and its children. Useful for multi-process applications. |
| [`teardown()`](https://docs.coreweave.com/products/wandb/ref/python/functions/teardown) | Clean up W\&B resources and shut down the backend process. |
| [`sweep()`](https://docs.coreweave.com/products/wandb/ref/python/functions/sweep) | Initialize a hyperparameter sweep to search for optimal model configurations. |
| [`agent()`](https://docs.coreweave.com/products/wandb/ref/python/functions/agent) | Create a sweep agent to run hyperparameter optimization experiments. |
| [`controller()`](https://docs.coreweave.com/products/wandb/ref/python/functions/controller) | Manage and control sweep agents and their execution. |
| [`restore()`](https://docs.coreweave.com/products/wandb/ref/python/functions/restore) | Restore a previous run or experiment state for resuming work. |
| [`finish()`](https://docs.coreweave.com/products/wandb/ref/python/functions/finish) | Finish a run and clean up resources. |

## Example

The most common workflow begins with authenticating with W\&B, initializing a run, and logging values (such as accuracy and loss) from your training loop. The first steps are to import `wandb` and use the global functions `login()` and `init()`:

```python theme={"system"}
import wandb

# Authenticate with W&B
wandb.login()

# Hyperparameters and metadata
config = {
   "learning_rate": 0.01,
   "epochs": 10,
}

# Project that the run is recorded to
project = "my-awesome-project"

# Initialize a new run
with wandb.init(project=project, config=config) as run:
   # Your training code here...
   
   # Log values to W&B
   run.log({"accuracy": 0.9, "loss": 0.1})
```
