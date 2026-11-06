# Point aggregation

Source: https://docs.coreweave.com/products/wandb/app/features/panels/line-plot/sampling

# Point aggregation

> Explore full fidelity bucketed sampling and random sampling for Weights & Biases line plots.

Use point aggregation methods within your line plots for improved data visualization accuracy and performance. This page explains the two available aggregation modes and how to configure each one, so you can choose the right tradeoff between detail and rendering speed for your workspace. Two types of point aggregation modes are available: [full fidelity](#full-fidelity) and [random sampling](#random-sampling). Weights & Biases uses full fidelity mode by default.

## Full fidelity

Full fidelity is the default aggregation method and preserves the extreme values in your data. This section explains how full fidelity works, its main advantages, and how to turn it on for a single chart or an entire workspace.

When you use full fidelity mode, Weights & Biases breaks the x-axis into dynamic buckets. The number of points per line adapts to chart size and the number of runs. It calculates the minimum and maximum values within each bucket (used for optional shading) and uses the last value in each bucket (not the average) to draw the primary line.

Full fidelity mode for point aggregation has three main advantages:

* Preserve extreme values and spikes: retain extreme values and spikes in your data.
* Configure how minimum and maximum points render: use the W\&B App to interactively decide whether you want to show extreme (min/max) values as a shaded area.
* Explore your data without losing data fidelity: Weights & Biases recalculates x-axis bucket sizes when you zoom into specific data points. This helps ensure that you can explore your data without losing accuracy. Weights & Biases caches previously computed aggregations to help reduce loading times, which is useful when you navigate through large datasets.

There are two ways to render full-fidelity line plots:

* **Band** (default): Shows the minimum and maximum values within each bucket as a shaded band, while the line shows the overall trend.
* **Line**: Connects points directly, making spikes and dips easier to identify.

### Turn on full fidelity

Weights & Biases uses full fidelity mode by default. To configure it manually, follow these steps:

> [tab] All charts in a workspace
>
> 1. Navigate to your workspace.
> 2. Select the gear icon on the top right corner of the screen next to the left of the **Add panels** button.
> 3. From the UI slider that appears, select **Line plots**.
> 4. Choose **Full fidelity** from the **Point aggregation** section.
> 5. From the **Full fidelity display** dropdown, select **Band** or **Line**.
> 6. Configure the **Smoothing** algorithm and settings.
> 7. Set **Aggregation** to **Mean**, **Min**, or **Max**.
> 8. Click **Apply**.

> [tab] Individual chart in a workspace
>
> 1. Navigate to your workspace.
> 2. Select the **Workspace** icon on the left tab.
> 3. Hover over the line plot panel you want to configure, then click the gear icon.
> 4. Within the modal that appears, set **Point aggregation method** to **Full fidelity**.
> 5. From the **Full fidelity display** dropdown, select **Band** or **Line**.
> 6. Configure the **Smoothing** algorithm and settings.
> 7. Click **Apply**.

### Configure shading

Shading visualizes the variability within each bucket so you can see how much points spread around the line. The shaded areas of a full-fidelity line plot can show:

* **Min/Max**: For each x-axis point, shade the area between the minimum and maximum values. The shaded area shows all points from the lowest to the highest value in each bucket:

  ```math theme={"system"}
  \text{Min/Max Range} = [\min(x_1, x_2, \ldots, x_n),\ \max(x_1, x_2, \ldots, x_n)]
  ```

  The values in a given bucket are:

  ```math theme={"system"}
  x_1, x_2, \ldots, x_n
  ```

* **Standard deviation**: For each x-axis point, calculate the variability of the values using standard deviation, and shade the resulting area.
  ```math theme={"system"}
  SD = \sqrt{\frac{1}{n}\sum_{i=1}^{n}(x_i - \overline{x})^2}
  ```

* **Standard error**: For each x-axis point, calculate the likelihood of a sampling error by dividing the value by the square root of the sample size:
  ```math theme={"system"}
  SE = \frac{SD}{\sqrt{n}}
  ```

* **None**: No shading (the default).

The following image shows a blue line plot. The light blue shaded area represents the minimum and maximum values for each bucket.

![Shaded confidence areas](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/_media/shaded-areas.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=217d1c975cb33cef7826862e3dba954f)

To configure shading:

1. Navigate to your workspace.
2. Hover over a line plot, then click the gear icon.
3. In the **Data** tab, set **Point aggregation** to **Full fidelity** if necessary, then configure the smoothing algorithm.
4. In the **Grouping** tab, turn on **Group runs**. Optionally, set **Group by** to a run attribute.
5. Set **Agg** to **Mean** (default), **Min**, or **Max**.
6. Set **Range** to **Min/Max**, **Std Dev**, **Std Err**, or **None**.
7. Click **Apply**.

### Explore your data without losing data fidelity

Analyze specific regions of the dataset without missing critical points like extreme values or spikes. When you zoom in on a line plot, Weights & Biases adjusts the bucket sizes used to calculate the minimum, maximum, and last value within each bucket.

![Plot zoom functionality](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/_media/zoom_in.gif?s=9638c4922d84caaa3db2197503af7529)

Weights & Biases uses dynamic binning to divide the x-axis into buckets. The number of points shown per line adapts to chart size and the number of runs: smaller chart dimensions or more runs can reduce the number of points per line so that the chart remains responsive and can display more lines. For each bucket, Weights & Biases calculates the following values:

* **Minimum**: The lowest value in that bucket (used for shading).
* **Maximum**: The highest value in that bucket (used for shading).
* **Line value**: The last value in that bucket, used to draw the line.

Weights & Biases plots values in buckets in a way that preserves full data representation and includes extreme values in every plot. The line is drawn from the last value in each bucket. When you zoom in far enough, full fidelity mode can render every data point without additional aggregation. The exact threshold depends on the current chart dimensions and number of runs.

To zoom in on a line plot, follow these steps:

1. Navigate to your Weights & Biases project.
2. Select the **Workspace** icon on the left tab.
3. Optional: Add a line plot panel to your workspace or navigate to an existing line plot panel.
4. Click and drag to select a specific region to zoom in on.

> [!NOTE]
>
> **Line plot grouping and expressions**
>
> When you use Line Plot Grouping, Weights & Biases applies the following based on the mode selected:
>
> * **Non-windowed sampling (grouping)**: Aligns points across runs on the x-axis. Weights & Biases takes the average if multiple points share the same x-value. Otherwise, they appear as discrete points.
> * **Windowed sampling (grouping and expressions)**: Divides the x-axis either into 250 buckets or the number of points in the longest line (whichever is smaller). Weights & Biases takes an average of points within each bucket.
> * **Full fidelity (grouping and expressions)**: Similar to non-windowed sampling, but fetches up to 500 points per run to balance performance and detail.

## Random sampling

Random sampling is an alternative aggregation method that prioritizes rendering speed over data fidelity. Use it when you need faster chart performance and you don't need to preserve every extreme value.

Random sampling uses 1,500 randomly sampled points to render line plots. Because sampling drops points, spotting outliers or spikes becomes more difficult.

> [!WARNING]
>
> Random sampling samples non-deterministically. As a result, random sampling sometimes excludes outliers or spikes in the data and therefore reduces data accuracy.

### Enable random sampling

By default, Weights & Biases uses full fidelity mode. To enable random sampling, follow these steps:

> [tab] All charts in a workspace
>
> 1. Navigate to your Weights & Biases project.
> 2. Select the **Workspace** icon on the left tab.
> 3. Select the gear icon on the top right corner of the screen next to the left of the **Add panels** button.
> 4. From the UI slider that appears, select **Line plots**.
> 5. Choose **Random sampling** from the **Point aggregation** section.

> [tab] Individual chart in a workspace
>
> 1. Navigate to your Weights & Biases project.
> 2. Select the **Workspace** icon on the left tab.
> 3. Select the line plot panel you want to enable random sampling for.
> 4. Within the modal that appears, select **Random sampling** from the **Point aggregation method** section.

### Access non-sampled data

If random sampling drops points you need, you can still access the complete, unsampled metric history programmatically. You can access the complete history of metrics logged during a run using the [Public API](https://docs.coreweave.com/products/wandb/ref/python/public-api/runs.md). The following example demonstrates how to retrieve and process the loss values from a specific run:

```python theme={"system"}
# Initialize the W&B API
api = wandb.Api()
run = api.run("l2k2/examples-numpy-boston/i0wt6xua")

# Retrieve the history of the 'Loss' metric
history = run.scan_history(keys=["Loss"])

# Extract the loss values from the history
losses = [row["Loss"] for row in history]
```
