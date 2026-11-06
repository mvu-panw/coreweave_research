# Tutorial: Use custom charts

Source: https://docs.coreweave.com/products/wandb/app/features/custom-charts/walkthrough

> Tutorial of using the custom charts feature in the W&B UI

# Tutorial: Use custom charts

Custom charts let you control both the data loaded into a panel and how it's visualized. This tutorial walks you through logging data, building a query, customizing the chart's Vega specification, and saving the result for reuse. It's intended for users who want to go beyond the default chart types and tailor visualizations to specific data.

By the end of this tutorial, you'll have a working custom chart in your project that you can save as a preset and a bonus composite histogram you can adapt to your own data.

## Log data to Weights & Biases

Before you can visualize anything in a custom chart, your run needs to log the data you want to display. Use [wandb.Run.config](https://docs.coreweave.com/products/wandb/track/config.md) for single points set at the beginning of training, like hyperparameters. Use [wandb.Run.log()](https://docs.coreweave.com/products/wandb/track/log.md) for multiple points over time, and log custom 2D arrays with `wandb.Table()`. We recommend logging up to 10,000 data points per logged key.

```python theme={"system"}
with wandb.init() as run: 

  # Logging a custom table of data
  my_custom_data = [[x1, y1, z1], [x2, y2, z2]]
  run.log(
    {"custom_data_table": wandb.Table(data=my_custom_data, columns=["x", "y", "z"])}
  )
```

[Try a quick example notebook](https://bit.ly/custom-charts-colab) to log the data tables, and in the next step you'll set up custom charts. See what the resulting charts look like in the [live report](https://forge.coreweave.com/wandb/demo-team/custom-charts/reports/Custom-Charts--VmlldzoyMTk5MDc).

With your data logged, you're ready to pull it into a custom chart panel.

## Create a query

A query tells the custom chart which logged data to load. After you've logged data to visualize, go to your project page and click the **`+`** button to add a new panel, then select **Custom Chart**. You can follow along in the [custom charts demo workspace](https://app.wandb.ai/demo-team/custom-charts).

![Blank custom chart](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/_media/create_a_query.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=7de15b04e03f6d5241668813c8acf0eb)

### Add a query

1. Click `summary` and select `historyTable` to set up a new query pulling data from the run history.
2. Type in the key where you logged the `wandb.Table()`. In the previous code snippet, it was `custom_data_table`. In the [example notebook](https://bit.ly/custom-charts-colab), the keys are `pr_curve` and `roc_curve`. For more information about **`summaryTable`**, **`historyTable`**, and **`tableKey`**, see [Build the GraphQL query](https://docs.coreweave.com/products/wandb/app/features/custom-charts.md#build-the-graphql-query).

### Set Vega fields

With the query in place, you can map your logged columns to the chart's visual encodings using the Vega fields dropdown menus:

![Pulling in columns from the query results to set Vega fields](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/_media/set_vega_fields.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=f13d8ae9a1b7f355fd4406f73225e5d7)

* **x-axis:** runSets\_historyTable\_r (recall)
* **y-axis:** runSets\_historyTable\_p (precision)
* **color:** runSets\_historyTable\_c (class label)

## Customize the chart

The default visualization is a good starting point, but you can edit the Vega spec to change the chart type, add titles, and refine the appearance. To switch from a scatter plot to a line plot, click **Edit** to change the Vega spec for this built-in chart. Follow along in the [custom charts demo workspace](https://app.wandb.ai/demo-team/custom-charts).

![Custom chart selection](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/_media/custom-charts-1.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=cb1a024420ba0891235b50ee8808c8ba)

Update the Vega spec to customize the visualization:

* Add titles for the plot, legend, x-axis, and y-axis (set "title" for each field).
* Change the value of "mark" from "point" to "line".
* Remove the unused "size" field.

![PR curve Vega spec](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/_media/customize_vega_spec_for_pr_curve.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=d6e3c64534a743b9bfcfcdfc156c8968)

Save a preset to reuse the same chart configuration on other panels in the project. To save this as a preset that you can use elsewhere in this project, click **Save as** at the top of the page. Here's what the result looks like, along with an ROC curve.

![PR curve chart](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/_media/custom-charts-2.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=cdb78d5bc6622f0ef0d4e6625cb1b5e7)

## Bonus: composite histograms

This section shows how to build a more advanced custom chart, a composite histogram that overlays two distributions in the same view, to demonstrate what's possible after you're comfortable editing the Vega spec.

Histograms can visualize numerical distributions to help you understand larger datasets. Composite histograms show multiple distributions across the same bins, letting you compare two or more metrics across different models or across different classes within your model. For a semantic segmentation model detecting objects in driving scenes, you might compare the effectiveness of optimizing for accuracy versus Intersection over Union (IoU), or you might want to know how well different models detect cars (large, common regions in the data) versus traffic signs (much smaller, less common regions). In the [demo Colab](https://bit.ly/custom-charts-colab), you can compare the confidence scores for two of the ten classes of living things.

![Composite histogram](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/_media/composite_histograms.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=6c61e0079eac029ac7e8dfcfeb9b1838)

To create your own version of the custom composite histogram panel:

1. Create a new custom chart panel in your workspace or report (by adding a **Custom Chart** visualization). Click **Edit** in the top right to modify the Vega spec starting from any built-in panel type.
2. Replace that built-in Vega spec with the [starter code for a composite histogram in Vega](https://gist.github.com/staceysv/9bed36a2c0c2a427365991403611ce21). You can modify the main title, axis titles, input domain, and any other details directly in this Vega spec [using Vega syntax](https://vega.github.io/). For example, you can change the colors or add a third histogram.
3. Modify the query in the right panel to load the correct data from your wandb logs. Add the field `summaryTable` and set the corresponding `tableKey` to `class_scores` to fetch the `wandb.Table` logged by your run. This lets you populate the two histogram bin sets (`red_bins` and `blue_bins`) through the dropdown menus with the columns of the `wandb.Table` logged as `class_scores`. For example, you can choose the `animal` class prediction scores for the red bins and `plant` for the blue bins.
4. You can keep making changes to the Vega spec and query until the plot you see in the preview rendering matches what you want. After you're done, click **Save as** in the top and give your custom plot a name so you can reuse it. Then click **Apply from panel library** to finish your plot.

Here's an example result from a brief experiment: training on only 1,000 examples for one epoch yields a model that's confident that most images are not plants and uncertain about which images might be animals.

![Chart configuration](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/_media/custom-charts-3.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=53c6d303b12aba54a06ed4155b8f0ec1)

![Chart result](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/_media/custom-charts-4.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=b4e672c01040da9d6ef1712713ca12c7)
