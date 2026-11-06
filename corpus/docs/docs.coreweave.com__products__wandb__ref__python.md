# Weights & Biases Python SDK 0.31.0

Source: https://docs.coreweave.com/products/wandb/ref/python

# Weights & Biases Python SDK 0.31.0

> Browse the Weights & Biases Python SDK API reference, including installation, classes, and functions.

The Weights & Biases Python SDK (`wandb` package) enables you to train and fine-tune models, and manage models from experimentation to production.

> After performing your training and fine-tuning operations with this SDK, you can use [the Public API](https://docs.coreweave.com/products/wandb/ref/python/public-api.md) to query and analyze the data that was logged, and [the Reports and Workspaces API](https://docs.coreweave.com/products/wandb/ref/wandb_workspaces) to generate a web-publishable [report](https://docs.coreweave.com/products/wandb/reports.md) summarizing your work.

## Installation and setup

### Sign up and create an API key

To authenticate your machine with W\&B, you must first generate an API key at [User settings](https://forge.coreweave.com/settings).

### Install and import packages

Install the W\&B library.

```
pip install wandb
```

### Import W\&B Python SDK:

```python theme={"system"}
import wandb

# Specify your team entity
entity = "<team_entity>"

# Project that the run is recorded to
project = "my-awesome-project"

with wandb.init(entity=entity, project=project) as run:
   run.log({"accuracy": 0.9, "loss": 0.1})
```
