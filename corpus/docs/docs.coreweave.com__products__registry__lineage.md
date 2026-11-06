# Lineage graphs and audit history

Source: https://docs.coreweave.com/products/registry/lineage

> Use lineage graphs to visualize a linked artifact's history and audit a collection's history.

# Lineage graphs and audit history

Use a lineage graph to visualize a linked artifact's history. Audit a collection's history to track changes made to artifacts in that collection.

## Lineage graphs

Within a collection in the Registry, you can view a history of the artifacts that an ML experiment uses. This history is called a *lineage graph*.

A lineage graph shows:

* Artifacts used as [inputs to a run](https://docs.coreweave.com/products/wandb/artifacts/explore-and-traverse-an-artifact-graph.md#track-the-input-of-a-run).
* Artifacts created as [outputs from a run](https://docs.coreweave.com/products/wandb/artifacts/explore-and-traverse-an-artifact-graph.md#track-the-output-of-a-run).

In other words, a lineage graph shows the input and output of a run.

For example, the following image shows a typical lineage graph for artifacts created and used throughout an ML experiment:

![Registry lineage](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/registry/_media/registry_lineage.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=f5078ce7e540c301bcf23d2456b281d3)

From left to right, the image shows:

1. Multiple runs log the `split_zoo_dataset:v0` artifact.
2. The `astral-deulge-3` run uses the `split_zoo_dataset:v0` artifact for training.
3. The output of the `astral-deulge-3` run is a model artifact called `zoo-l4oqundu:v0`.
4. A run called `denim-night-4` uses the model artifact `zoo-l4oqundu:v0` to evaluate the model.

To view a lineage graph for an artifact in a collection:

1. Navigate to **Registry**.
2. Select the collection that contains the artifact.
3. From the dropdown, select the artifact version you want to view its lineage graph.
4. Select the **Lineage** tab.
5. Select a node to view detailed information about the run or artifact.

> [!NOTE]
>
> See [Enable lineage graph tracking](https://docs.coreweave.com/products/wandb/artifacts/explore-and-traverse-an-artifact-graph.md#enable-lineage-graph-tracking) to learn how to track the input and output of a run using the W\&B Python SDK.

The following image shows the expanded detailed view of a run (`astral-deluge-3`) when you select a node in the lineage graph:

![Expanded lineage node](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/registry/_media/lineage_expanded_node.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=2a31f0d92db9b2b4142a04fa08dc4fa5)

The following image shows the expanded detailed view of an artifact (`zoo-l4oqundu:v0`) when you select an artifact node in the lineage graph:

![Expanded artifact node details](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/registry/_media/lineage_expanded_artifact_node.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=514f4de4e3d4a806d5bff41835998315)

The **Created by run** shows the run that created the artifact. In this example, it is the `astral-deulge-3` run.

> [!NOTE]
>
> You can also view lineage graphs for artifacts you log to W\&B that are not part of a collection. See [Explore artifact lineage graphs](https://docs.coreweave.com/products/wandb/artifacts/explore-and-traverse-an-artifact-graph.md) for more information.

### Create a custom view

Click **Custom** in the top-right corner of the lineage graph to create a custom view. You can filter and customize the lineage graph with the following options:

* **Filter by artifact type**: Filter by artifact type values logged to W\&B. For example, if you log an artifact with the type "dataset", then "dataset" is available as a filter value.
* **Filter by run job type**: Filter by run job type values logged to W\&B. For example, if you log a run with the job type "training", then "training" is available as a filter value.
* **Include extended lineage**: Display items that are not in the direct lineage for the base version.
* **Include generated artifacts**: Items created programmatically will show.
* **Expand clusters**: Similar items with similar connections will not be grouped together.
* **Downstream hops**: Descendant generations relative to the active node.
* **Upstream hops**: Ancestor generations relative to the active node.

To reset the lineage graph to its default view, click the backward arrow button.

## Audit a collection's history

View actions that members of your organization take on that collection. You can view:

* If an alias was added or removed from an artifact version.
* If an artifact version was added or removed from a collection.

For both actions, you can view the user that performed the action and the date the action occurred.

To view a collection's action history:

1. Navigate to **Registry**.
2. Select the collection you want to view its action history.
3. Select the dropdown menu next to the collection name.
4. Select the **Action History** option.
