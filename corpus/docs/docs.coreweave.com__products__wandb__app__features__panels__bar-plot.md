# Bar plots

Source: https://docs.coreweave.com/products/wandb/app/features/panels/bar-plot

> Visualize metrics, customize axes, and compare categorical data as bars.

# Bar plots

A bar plot presents categorical data with rectangular bars that you can plot vertically or horizontally. Use bar plots to visualize metrics, compare categorical data, and customize axes for your runs. Bar plots appear by default with `wandb.Run.log()` when all logged values are of length one.

![Box and horizontal bar plots in Weights & Biases](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/_media/bar_plot.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=8dd6200af206956e49dded2cd84110c0)

Use chart settings to limit the maximum number of runs shown, group runs by any config, and rename labels.

![Customized bar plot](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/_media/bar_plot_custom.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=b35ca8695c2aca3116c48adb27f14130)

## Customize bar plots

You can also create **Box Plot** or **Violin** plots to combine many summary statistics into one chart type, if you group your runs.

To create a box or violin plot:

1. [Group your runs in the runs table](https://docs.coreweave.com/products/wandb/runs/grouping.md), or enable grouping in the panel.
2. In the workspace, click **Add panel**, then choose **Bar Chart**.
3. On the **Data** tab, use the **Metric** selector to choose your summary metric.
4. On the **Grouping** tab, in the **Style** control, choose **Box Plot** or **Violin**.

If you do not see the **Style** control or the **Box Plot** and **Violin** options, your runs are not grouped. Group your runs and the options appear.

![Customizing a bar plot with grouping options](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/_media/bar_plots.gif?s=49a18d59958a394eb7d7f60c779378b2)
