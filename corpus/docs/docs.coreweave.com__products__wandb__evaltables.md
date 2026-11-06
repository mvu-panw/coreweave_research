# Overview

Source: https://docs.coreweave.com/products/wandb/evaltables

# Overview

> Learn how to create, compare, and visualize Eval Tables in Weights & Biases.

Eval Tables help you compare aggregate scores and example-level model inputs, outputs, and scores across multiple runs. Use an Eval Table to compare model versions or training steps, review aggregate score changes, and investigate the examples behind changes in model performance.

The following image shows an Eval Table called `"validation_prediction_eval"` that compares two runs `"summer-butterfly-9"` and `"gentle-flower-8"`:

![Eval Table view](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/_media/overview_basic_compare_two_runs_landing_page_notlabled.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=6147e5cdc48132c03c9781715eb59e29)

An **Eval Table** panel contains three sections:

1. Run comparison selector: Select the [runs that you want to compare](https://docs.coreweave.com/products/wandb/evaltables/compare-runs.md).
2. Aggregate scores: Review aggregate scores for the selected runs and compare the differences between them. For more information, see [View aggregate scores](https://docs.coreweave.com/products/wandb/evaltables/compare-runs.md#aggregate-scores).
3. Examples: Compare the inputs, outputs, and scores for each example across the selected runs.

The following image highlights each section of the panel:

![Eval Table view](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/_media/overview_basic_compare_two_runs_landing_page.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=9e85abb5211b6413e2d83e129737ad90)

[Create an Eval Table with the `EvalTable` class from the W\&B Python SDK](https://docs.coreweave.com/products/wandb/evaltables/create-an-evaluation-table).

Existing [W\&B Tables](https://docs.coreweave.com/products/wandb/tables.md) can also be converted to Eval Tables with ARIA. For more information, see [Convert a W\&B Table to an Eval Table](https://docs.coreweave.com/products/wandb/evaltables/create-an-evaluation-table.md#convert-a-wb-table-to-an-eval-table).

> [!TIP]
>
> Convert existing W\&B Tables to Eval Tables to improve rendering performance and access additional comparison features.

To create your first Eval Table, see [Create an Eval Table](https://docs.coreweave.com/products/wandb/evaltables/create-an-evaluation-table.md).
