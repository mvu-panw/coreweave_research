# XGBoost

Source: https://docs.coreweave.com/products/wandb/integrations/xgboost

> Use Weights & Biases with XGBoost to automatically log gradient boosting metrics, feature importance, and performance.

# XGBoost

[Try in Colab](https://colab.research.google.com/github/wandb/examples/blob/master/colabs/boosting/Credit_Scorecards_with_XGBoost_and_W%26B.ipynb)

This page shows you how to use the Weights & Biases integration with XGBoost to automatically log gradient boosting metrics, model configurations, feature importance, and trained boosters so you can track, compare, and reproduce your XGBoost experiments.

The W\&B Python SDK (`wandb`) has a `WandbCallback` callback that logs metrics, configs, and saved boosters from training with XGBoost. See a [live W\&B Dashboard](https://wandb.ai/morg/credit_scorecard) with outputs from the XGBoost `WandbCallback`.

![W\&B Dashboard using XGBoost](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/_media/xgb_dashboard.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=cc5d70f5f84ba45748f080471dabffc9)

## Get started

To log XGBoost metrics, configs, and booster models to Weights & Biases, pass the `WandbCallback` to XGBoost:

```python theme={"system"}
import wandb
from wandb.integration.xgboost import WandbCallback
from xgboost import XGBClassifier

...
# Start a wandb run
with wandb.init() as run:
  # Pass WandbCallback to the model
  bst = XGBClassifier()
  bst.fit(X_train, y_train, callbacks=[WandbCallback(log_model=True)])
```

For a comprehensive look at logging with XGBoost and Weights & Biases, see the [XGBoost and Weights & Biases logging notebook](https://wandb.me/xgboost).

## `WandbCallback` reference

### Functionality

Passing `WandbCallback` to an XGBoost model does the following:

* Logs the booster model configuration to Weights & Biases.
* Logs evaluation metrics collected by XGBoost, such as `rmse`, accuracy, and so on to Weights & Biases.
* Logs training metrics collected by XGBoost (if you provide data to `eval_set`).
* Logs the best score and the best iteration.
* Saves and uploads your trained model to W\&B Artifacts (when `log_model = True`).
* Logs the feature importance plot when `log_feature_importance=True` (default).
* Captures the best eval metric in `wandb.Run.summary` when `define_metric=True` (default).

### Arguments

* `log_model`: (boolean) if True, saves and uploads the model to W\&B Artifacts.

* `log_feature_importance`: (boolean) if True, logs a feature importance bar plot.

* `importance_type`: (str) one of `{weight, gain, cover, total_gain, total_cover}` for tree model. `weight` for linear model.

* `define_metric`: (boolean) if True (default), captures model performance at the best step, instead of the last step, of training in your `run.summary`.

Review the [source code for WandbCallback](https://github.com/wandb/wandb/blob/main/wandb/integration/xgboost/xgboost.py).

For more examples, see the [repository of examples on GitHub](https://github.com/wandb/examples/tree/master/examples/boosting-algorithms).

## Tune your hyperparameters with Sweeps

W\&B [Sweeps](https://docs.coreweave.com/products/wandb/sweeps.md) is a toolkit for configuring, orchestrating, and analyzing hyperparameter testing experiments. This section shows how to combine the XGBoost integration with W\&B Sweeps to search across hyperparameter configurations.

To improve model performance, tune hyperparameters like tree depth and learning rate.

[Try in Colab](https://colab.research.google.com/github/wandb/examples/blob/master/colabs/boosting/Using_W%26B_Sweeps_with_XGBoost.ipynb)

You can also try this [XGBoost and Sweeps Python script](https://github.com/wandb/examples/blob/master/examples/wandb-sweeps/sweeps-xgboost/xgboost_tune.py).

![XGBoost performance comparison](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/_media/xgboost_sweeps_example.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=a524e277faa6ec202fc33fe99ff57f64)
