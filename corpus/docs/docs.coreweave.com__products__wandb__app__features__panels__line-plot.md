# Line plots overview

Source: https://docs.coreweave.com/products/wandb/app/features/panels/line-plot

> Visualize metrics, customize axes, and compare multiple lines on a plot

# Line plots overview

Line plots display by default for metrics logged with `wandb.Run.log()` over time. Line plots support plotting multiple metrics, calculating custom axes, and more.

This page shows how to create, configure, and manage line plots in a [workspace](https://docs.coreweave.com/products/wandb/track/workspaces.md).

![Line plot example](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/_media/line_plot_example.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=43705c977605e716d19d0313fc17e4b7)

> [!TIP]
>
> For [runs](https://docs.coreweave.com/products/wandb/runs.md) that execute on [CoreWeave Kubernetes Service (CKS)](https://docs.coreweave.com/products/cks.md) clusters, [CoreWeave Mission Control](https://www.coreweave.com/mission-control) can monitor your compute infrastructure when the integration is enabled. If an error occurs, Weights & Biases populates infrastructure information onto your run's plots in your project's workspace. For prerequisites and details, see [Visualize CoreWeave infrastructure alerts](https://docs.coreweave.com/products/wandb/runs/infrastructure-alerts.md).

## Add a line plot

The following sections describe how to create a line plot for a single metric or multiple metrics.

> [tab] Single-metric line plot
>
> In an [automatic workspace](https://docs.coreweave.com/products/wandb/app/features/panels.md#workspace-modes), Weights & Biases creates a single-metric line plot automatically for each logged metric. Follow these steps to re-add a line plot that was deleted from an automatic workspace, or to add a line plot to a manual workspace.
>
> 1. Navigate to your workspace.
> 2. To add a line plot globally, click **Add panels** in the control bar near the panel search field.
>
>    To add a line plot directly to a section instead, click the section's **action ()** menu, then click **+ Add panels**.
> 3. To add a single-metric plot with default settings, click **Quick panel builder**.
>    1. In the **Single-key panels** tab, hover over a metric, then click **Add**. Repeat this step for each panel you want to add.
>    2. Click **Create \[NUMBER] panels**.
> 4. To add a custom line plot instead, click **Line plot**.
>    1. Configure the line plot's data, grouping, and display preferences using the corresponding tabs. For details, see [Edit line plot settings](#edit-line-plot-settings).
>    2. To add calculated expressions to the x-axis or y-axis, click **Expressions**. [JavaScript regular expressions](https://www.w3schools.com/js/js_regexp.asp) are supported.
> 5. Select the type of panel to add, such as a chart. The panel's configuration details appear with selected defaults.
> 6. Optionally, customize the panel and its display preferences. Configuration options depend on the type of panel you select. For more information about the options for each type of panel, see [Line plots](https://docs.coreweave.com/products/wandb/app/features/panels/line-plot.md) or [Bar plots](https://docs.coreweave.com/products/wandb/app/features/panels/bar-plot.md).
> 7. Click **Apply**.

> [tab] Multi-metric line plot
>
> In an [automatic workspace](https://docs.coreweave.com/products/wandb/app/features/panels.md#workspace-modes), Weights & Biases creates a single-metric line plot automatically for each logged metric.
>
> This section shows how to create a line plot that displays multiple metrics selected with a JavaScript regular expression. A multi-metric line plot lets you compare related metrics in one panel instead of reviewing them across multiple panels.
>
> 1. Navigate to your workspace.
> 2. To add a line plot globally, click **Add panels** in the control bar near the panel search field.
>
>    To add a line plot directly to a section instead, click the section's **action ()** menu, then click **+ Add panels**.
> 3. Click **Quick panel builder**, then click the **Multi-metric panels** tab.
> 4. In **Regex** enter an expression with [Google's RE2](https://github.com/google/re2/wiki/Syntax) format. As you type, the UI updates to show which metrics match the expression. By default, the plot name shows the regular expression used by the plot. The plot includes lines for all metrics that match the expression, including metrics logged in the future.
> 5. To optionally remove duplicate single-metric panels when the multi-metric plot is created, toggle **Clean up auto-generated panels**. A preview shows which panels are cleaned up. \[!NOTE] When this option is turned on, Weights & Biases doesn't create a single-metric plot for a newly logged metric that matches the expression. Instead, it appears only in this multi-metric plot.
> 6. Click **Create \[NUMBER] panels**.
>
> ### Multi-metric regular expressions
>
> Multi-metric line plots use [Google's RE2](https://github.com/google/re2/wiki/Syntax) syntax to match metric names. The following sections describe common use cases and provide more details about how the regular expressions work, such as how capture groups affect the panels that Weights & Biases creates.
>
> #### Common use cases
>
> The following examples show some ways you can use multi-metric panels to help you analyze your experiment results.
>
> **Compare metrics across layers or model components**
> Instead of creating separate panels for each layer's metrics, you can view them together in a single panel. For example, if you log metrics with consistent naming, like `layer_0_loss`, `layer_1_loss`, and `layer_2_loss` in this Python example code, you can use the regex `layer_\d+_loss` to display all layer losses on one plot.
>
> ```python theme={"system"}
> with wandb.init(project="multi-layer-model") as run:
>     for step in range(100):
>         run.log({
>             "layer_0_loss": loss_0,
>             "layer_1_loss": loss_1,
>             "layer_2_loss": loss_2,
>             "step": step
>         })
> ```
>
> **Group related metrics by prefix or suffix**
> Match all metrics that share a common naming pattern. For example:
>
> * `train_.*` matches all training metrics like `train_loss`, `train_accuracy`, `train_f1_score`.
> * `.*_accuracy` matches accuracy metrics across different datasets like `train_accuracy`, `val_accuracy`, `test_accuracy`.
>
> **Match specific metric variations**
> Use alternation to match only the metrics you want. For example, the non-capture group `(?:layer_0|layer_10)_loss` matches only the first and tenth layer losses, excluding intermediate layers.
>
> #### Capture groups
>
> Capture groups in your regular expression control how multi-metric panels are created. This behavior can be confusing if you're not expecting it.
>
> * **Capture groups create multiple panels**
>   When your regular expression includes parentheses that form a capture group, the UI creates a separate panel for each unique value captured by that group.
>
>   For example, the expression `(layer_0|layer_10)_loss` includes a capture group and creates two separate panels:
>
>   1. One panel for metrics matching `layer_0`.
>   2. One panel for metrics matching `layer_10`.
> * **Non-capturing groups keep metrics together**
>   To match multiple alternatives without creating separate panels, use a non-capturing group with the `?:` syntax. The expression `(?:layer_0|layer_10)_loss` matches the same metrics as the previous example, but displays them together in a single panel.
>
> Here's the difference:
>
> * `(layer_0|layer_10)_loss` - Creates two panels, one for each layer.
> * `(?:layer_0|layer_10)_loss` - Creates one panel showing both layers together.
>
> This gives you flexibility to choose the approach that best fits your analysis needs. Use capture groups when you want to separate metrics into distinct panels. Use non-capturing groups when you want to compare metrics together on a single plot.

## Edit line plot settings

The following sections describe how to edit the settings for an individual line plot panel, all line plot panels in a section, or all line plot panels in a workspace. For details about line plot settings, see [Line plot reference](https://docs.coreweave.com/products/wandb/app/features/panels/line-plot/reference.md).

### Individual line plot

A line plot's individual settings override the line plot settings for the section or the workspace. To customize a line plot:

1. Navigate to your workspace.
2. Hover your mouse over the panel, then click the gear icon.
3. Within the drawer that appears, select a tab to edit its settings.
4. Click **Apply**.

Line plot settings are organized into tabs:

* **Data**: Configure x-axis, y-axis, sampling method, smoothing, outliers, and chart type.
* **Grouping**: Configure whether and how to group and aggregate runs in the plot.
* **Chart**: Specify titles for the panel and axes, and configure legend visibility and position.
* **Legend**: Customize the appearance and content of the panel's legend.
* **Expressions**: Add custom calculated expressions for the axes. For the full list of operators and example expressions, including arithmetic such as multiplication, see [Expressions](https://docs.coreweave.com/products/wandb/app/features/panels/line-plot/reference.md#expressions).

For detailed information about each setting, see the [Line plot reference](https://docs.coreweave.com/products/wandb/app/features/panels/line-plot/reference.md).

### All line plots in a section

To customize the default settings for all line plots in a section, overriding workspace settings for line plots:

1. Navigate to your workspace.
2. Click the section's gear icon to open its settings.
3. Within the drawer that appears, select the **Data** or **Display preferences** tabs to configure the default settings for the section. For details about each **Data** setting, see the [Line plot reference](https://docs.coreweave.com/products/wandb/app/features/panels/line-plot/reference.md). For details about each display preference, see [Configure section layout](https://docs.coreweave.com/products/wandb/app/features.md#configure-section-layout).

### All line plots in a workspace

To customize the default settings for all line plots in a workspace:

1. Navigate to your workspace.
2. Click the workspace settings icon, which has a gear with the label **Settings**.
3. Click **Line plots**.
4. Within the drawer that appears, select the **Data** or **Display preferences** tabs to configure the default settings for the workspace.
   * For details about each **Data** setting, see the [Line plot reference](https://docs.coreweave.com/products/wandb/app/features/panels/line-plot/reference.md).
   * For details about each **Display preferences** section, see [Workspace display preferences](https://docs.coreweave.com/products/wandb/app/features.md#configure-workspace-layout). At the workspace level, you can configure the default **Zooming** behavior for line plots. This setting controls whether to sync zooming across line plots with a matching x-axis key. Deactivated by default.

## Visualize average values on a plot

If you have several different experiments and you want to see the average of their values on a plot, you can use the Grouping feature in the table. Click **Group** above the run table and select **All** to show averaged values in your graphs.

The following image shows the graph before averaging, with one line per run:

![Individual precision lines](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/_media/demo_precision_lines.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=39ec1186c5d360963b250112a1e8cb90)

The following image shows a graph that represents average values across runs using grouped lines.

![Averaged precision lines](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/_media/demo_average_precision_lines.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=5ca37e1a93a51e5e431ed2e5176aadf7)

## Visualize NaN value on a plot

To track metrics that might sometimes be undefined, such as a loss that returns `NaN`, you can log them and Weights & Biases renders them on the line plot. You can also plot `NaN` values including PyTorch tensors on a line plot with `wandb.Run.log()`. For example:

```python theme={"system"}
with wandb.init() as run:
    # Log a NaN value
    run.log({"test": float("nan")})
```

![NaN value handling](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/_media/visualize_nan.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=dbc9bf070f62111faec60a15173ca709)

## Compare multiple metrics on one chart

To compare multiple metrics from one or more runs side by side, add a **Run comparer** panel to your workspace.

![Adding visualization panels](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/_media/visualization_add.gif?s=91d9a5add5d026b0c51d93e15e97f8e3)

1. Navigate to your workspace.
2. Select the **Add panels** button in the top right corner of the page.
3. From the drawer that appears, expand the **Evaluation** dropdown.
4. Select **Run comparer**.

## Change the colors of the lines

If the default color of runs isn't helpful for comparison, Weights & Biases provides two ways to change the colors: from the run table or from a chart's legend settings.

> [tab] From the run table
>
> Each run is given a random color by default upon initialization.
>
> ![Random colors given to runs](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/_media/line_plots_run_table_random_colors.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=55a20460bcac59277069fee8eacec1c7)
>
> Upon clicking any of the colors, a color palette appears from which you can choose the color you want.
>
> ![The color palette](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/_media/line_plots_run_table_color_palette.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=cb1dfd1308d76ddb9423ebf20ce20e60)

> [tab] From the chart legend settings
>
> 1. Navigate to your workspace.
> 2. Hover your mouse over the panel whose settings you want to edit.
> 3. Select the pencil icon that appears.
> 4. Choose the **Legend** tab.
>
> ![Line plot legend settings](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/_media/plot_style_line_plot_legend.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=c5b5a7916db550f6141d650da3d2dc85)

## Visualize on different x axes

By default, line plots use training steps as the x-axis, but you can switch to a different x-axis to view your data from another perspective. If you want to see the absolute time that an experiment has taken, or see what day an experiment ran, you can switch the x-axis. The following example shows switching from steps to relative time and then to wall time.

![X-axis time options](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/_media/howto_use_relative_time_or_wall_time.gif?s=599e0e411b48993dfeb9040dd979f5c1)

To use a custom x-axis, log the metric in the same call to `wandb.Run.log()` where you log the y-axis. For example:

```python theme={"system"}
with wandb.init() as run:
    for i in range(100):
        run.log({"accuracy": acc, "custom_x": i * 10})
```

For more details, see [Customize log axes](https://docs.coreweave.com/products/wandb/track/log/customize-logging-axes.md#customize-log-axes).

## Zoom

To inspect a specific region of a line plot more closely, you can zoom in on both axes at once. Click and drag a rectangle to zoom vertically and horizontally at the same time. This changes the x-axis and y-axis zoom.

![Plot zoom functionality](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/_media/line_plots_zoom.gif?s=b304205e205996ba87ee0c7559858a1e)

## Hide chart legend

If the chart legend is taking up space you want to use for the plot, you can turn it off. Turn off the legend in the line plot with this toggle:

![Hide legend toggle](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/_media/demo_hide_legend.gif?s=be5296cece36d9eb11da486e00ca0fdc)

## Create a run metrics notification

Use [Automations](https://docs.coreweave.com/products/wandb/automations.md) to notify your team when a run metric meets a condition you specify. An automation can post to a Slack channel or run a webhook.

From a line plot, you can create a [run metrics notification](https://docs.coreweave.com/products/wandb/automations/automation-events.md#run-events) for the metric it shows:

1. Navigate to your workspace.
2. Hover over the panel, then click the bell icon.
3. Configure the automation using the basic or advanced configuration controls. For example, apply a run filter to limit the scope of the automation, or configure an absolute threshold.

Learn more about [Automations](https://docs.coreweave.com/products/wandb/automations.md).
