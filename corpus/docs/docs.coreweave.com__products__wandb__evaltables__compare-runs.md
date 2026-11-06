# Compare runs with Eval Tables

Source: https://docs.coreweave.com/products/wandb/evaltables/compare-runs

# Compare runs with Eval Tables

Use Eval Tables to compare inputs, outputs, and scores across multiple runs. Weights & Biases aligns corresponding examples and calculates aggregate scores and score differences for the selected runs.

> [!NOTE]
>
> To compare runs with workspace-level summary metrics, line plots, pinned runs, or a baseline run, see [Pin and compare runs](https://docs.coreweave.com/products/wandb/runs/compare-runs.md). Eval Tables compare aligned examples and Eval Table-specific scores within a logged table.

To compare runs:

1. Navigate to your project workspace.
2. Scroll to the Eval Tables panel.
3. Select the **+** button.
4. Select the run that you want to add.

Weights & Biases groups columns that have the same role and name across the selected runs. For example, if two runs use the same `input_columns`, Weights & Biases displays those columns together in the **Inputs** section. Weights & Biases similarly groups shared `output_columns` and `score_columns` in the **Outputs** and **Scores** sections.

The following screenshot shows an Eval Table that compares the `summer-butterfly-9` and `gentle-flower-8` runs:

![Eval Table view](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/_media/overview_basic_compare_two_runs.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=4414d3394d99462237d158e53c586788)

## Set the reference run

When you compare multiple runs, Weights & Biases defaults to designating the left-most run as the reference run. The reference run is the baseline to calculate score deltas.

To choose a different reference run, hover over the run, open its menu, and select **Set as reference**.

## View aggregate scores

Weights & Biases calculates an aggregate value for each score column in each selected run. The calculation depends on the score's data type:

| Type of score | Aggregate value |
| - | - |
| Boolean | Count and fraction of `true` values |
| Numeric | Mean |
| String or categorical | No scalar aggregate |
| Null | Excluded from calculation |

The following screenshot highlights the aggregate values for the correct and confidence scores:

![Eval Table view](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/_media/overview_basic_compare_two_runs_labled.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=95fae414bd40572d9b5f055b67e045a8)

## Compare score deltas

For each score column, Weights & Biases calculates the difference between the reference run and every other selected run.

Weights & Biases calculates each delta as:

```text theme={"system"}
comparison run value - reference run value
```

For example, suppose `summer-butterfly-9` is the reference run and `gentle-flower-8` is the comparison run. Weights & Biases calculates the confidence delta as follows:

| `summer-butterfly-9` | `gentle-flower-8` | delta |
| - | - | - |
| 0.43 | 0.62 | +0.19 |
| 0.92 | 0.86 | -0.06 |
| 0.97 | 0.85 | -0.12 |

A positive delta means that the comparison run has a higher value than the reference run. A negative delta means that it has a lower value.

The following screenshot highlights the score deltas:

![Eval Table view](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/_media/overview_basic_compare_two_runs_delta_labled.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=8e57198cebb5b796571a6e7e09ec6e8d)
