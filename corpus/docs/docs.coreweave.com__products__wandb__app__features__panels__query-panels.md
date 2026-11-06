# Query panels overview

Source: https://docs.coreweave.com/products/wandb/app/features/panels/query-panels

> Some features on this page are in beta, hidden behind a feature flag. Add `weave-plot` to your bio on your profile page to unlock all related features.

# Query panels overview

> [!NOTE]
>
> Looking for W\&B Weave, Weights & Biases' suite of tools for generative AI application building? See the [Weave documentation](https://wandb.github.io/weave/?utm_source=wandb_docs\&utm_medium=docs\&utm_campaign=weave-nudge).

Use query panels to query and interactively visualize your data. With a query panel, you can pull specific runs, artifacts, tables, and other Weights & Biases objects into a single view and explore them as tables or plots without leaving your workspace or report. This page is for users who want to compose ad hoc queries against logged Weights & Biases data and surface the results inside a workspace or report.

A query panel combines three pieces:

* **[Expression](#expressions)**: The data you select.
* **[Configuration](#configurations)**: Optional settings for the panel, such as the panel type and options from the gear menu.
* **[Result panel](#result-panels)**: How to show the results, such as in a table or plot.

For interactive examples you can try and a guided walkthrough of query syntax, see the public [Query panel examples report](https://forge.coreweave.com/wandb/luis_team_test/weave_example_queries/reports/Weave-queries---Vmlldzo1NzIxOTY2?accessToken=bvzq5hwooare9zy790yfl3oitutbvno2i6c2s81gk91750m53m2hdclj0jvryhcr). Generated types and ops are listed in the [query expression language overview](https://docs.coreweave.com/products/wandb/ref/query-panel.md).

![Query panel](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/_media/pretty_panel.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=38e62e3bad5e871e36c06f54502f8738)

## Create a query panel

Add a query panel so you have a surface to write expressions against and visualize the results. You can add one to a project workspace or within a report.

> [tab] Project workspace
>
> 1. Navigate to your project's workspace.
> 2. In the upper-right corner, click **Add panel**.
> 3. From the dropdown menu, select **Query panel**.

> [tab] W\&B Report
>
> * Type and select **/Query panel**.
>
> ![Query panel option](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/_media/add_weave_panel_report_1.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=aa593a0dad7fc945272917451b0df542)
>
> Alternatively, you can associate a query with a set of runs:
>
> 1. Within your report, type and select **/Panel grid**.
> 2. Click the **Add panel** button.
> 3. From the dropdown menu, select **Query panel**.

## Query components

The following sections describe the three pieces that make up a query panel: the expression that selects data, the configuration that controls how the panel behaves, and the result panel that renders the output.

### Expressions

Use query expressions to query your data stored in Weights & Biases such as runs, artifacts, models, tables, and more.

#### Example: Query a table

Suppose you want to query a W\&B Table. In your training code, you log a table called `"cifar10_sample_table"`:

```python theme={"system"}
import wandb
with wandb.init() as run:
  run.log({"cifar10_sample_table":[MY-TABLE]})
```

Within the query panel, you can query your table with:

```python theme={"system"}
runs.summary["cifar10_sample_table"]
```

![Table query expression](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/_media/basic_weave_expression.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=d7690752f74596939bf571a2dbf0f83c)

Breaking this down:

* `runs` is a variable automatically injected in query panel expressions when the query panel is in a workspace. Its value is the list of runs visible for that workspace. For details about the different attributes available within a run, see [Understanding the different attributes](https://docs.coreweave.com/products/wandb/track/public-api-guide.md#understanding-the-different-attributes).
* `summary` is an op that returns the Summary object for a run. Ops are *mapped*, meaning this op is applied to each run in the list, resulting in a list of Summary objects.
* `["cifar10_sample_table"]` is a Pick op (denoted with brackets) with a key of `cifar10_sample_table`. Because Summary objects act like dictionaries or maps, this operation picks that field from each Summary object.

### Configurations

In the upper-left corner of the panel, click the gear icon to expand the query configuration. The configuration lets you set the type of panel and the parameters for the result panel.

![Panel configuration menu](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/_media/weave_panel_config.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=f4e02df818f31851f45686d25ce347ac)

#### Panel options

The configuration menu can include options that change how the panel combines or loads table-style results. Exact labels and availability depend on your expression and panel type. For concrete setups, see the [Query panel examples report](https://forge.coreweave.com/wandb/luis_team_test/weave_example_queries/reports/Weave-queries---Vmlldzo1NzIxOTY2?accessToken=bvzq5hwooare9zy790yfl3oitutbvno2i6c2s81gk91750m53m2hdclj0jvryhcr).

**Concat**

Use **Concat** in the configuration when you want the panel to merge compatible table-style results and treat them as a single table for viewing and downstream operations. Expression-level row merging (for example, `concat` and `join` in the query) is separate from this setting. For more information, see [Combine tables in expressions](#combine-tables-in-expressions).

**Paginate**

Use **Paginate** when a table result might be too large to render at once. Pagination loads rows in chunks so the panel stays responsive. Pair this option with expressions that return large row lists. For patterns that work well with pagination, see the [Query panel examples report](https://forge.coreweave.com/wandb/luis_team_test/weave_example_queries/reports/Weave-queries---Vmlldzo1NzIxOTY2?accessToken=bvzq5hwooare9zy790yfl3oitutbvno2i6c2s81gk91750m53m2hdclj0jvryhcr).

### Result panels

The query result panel renders the result of the query expression, using the selected query panel, configured to display the data in an interactive form. The following images show a Table and a Plot of the same data.

![Table result panel](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/_media/result_panel_table.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=175f306abc19dcefb50f0088029ef059)

![Plot result panel](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/_media/result_panel_plot.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=f40b3cb175208c0a653fcddad015fbfc)

### Step through run history

In tables and plots built from `runs` or `runs.history`, the app can show a **step** control (for example, a slider) so you can move through logged steps and inspect metrics, text, or media over the course of your runs. After you change the expression, edit the query panel's configuration and change **Render As** to **Stepper**. The control can follow a different metric instead of `_step` if it better matches how you logged data. For sample expressions, see the [Query panel examples report](https://forge.coreweave.com/wandb/luis_team_test/weave_example_queries/reports/Weave-queries---Vmlldzo1NzIxOTY2?accessToken=bvzq5hwooare9zy790yfl3oitutbvno2i6c2s81gk91750m53m2hdclj0jvryhcr).

## Basic operations

After a query panel renders results, you can refine what you see by sorting, filtering, mapping, or grouping the rows. The following are common operations you can perform within your query panels.

### Sort

Sort from the column options:

![Column sort options](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/_media/weave_sort.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=9f0dc5dc9ba1591b2ed972dc6284566c)

### Filter

You can either filter directly in the query or use the filter button in the upper-left corner of the panel.

![Query filter syntax](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/_media/weave_filter_1.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=773ab72a6b53961db1f9e6a100fa59d4)

![Filter button](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/_media/weave_filter_2.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=357c95207f9b1816a4d52c336b68521e)

### Map

Map operations iterate over lists and apply a function to each element in the data. You can do this directly with a panel query or by inserting a new column from the column options.

![Map operation query](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/_media/weave_map.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=4ee41e01914c5cfc0b98a5abd17d1214)

![Map column insertion](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/_media/weave_map.gif?s=b327dae5cac50a6812f8d64b51d4eef1)

### Group by

You can group by using a query or from the column options.

![Group by query](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/_media/weave_groupby.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=406ad3c21e204b19949705a87c49a856)

![Group by column options](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/_media/weave_groupby.gif?s=983aa12979f3b80df3136399b6de95be)

### Combine tables in expressions

Use `concat`, `join`, and related ops in your expression when you need to stack or merge row lists from tables. See [Join](#join) for a full example. The **Concat** and **Paginate** items in [Panel options](#panel-options) are separate controls for how the UI merges and loads table results.

### Join

You can also join tables directly in the query. Consider the following query expression:

```python theme={"system"}
project("luis_team_test", "weave_example_queries").runs.summary["short_table_0"].table.rows.concat.join(\
project("luis_team_test", "weave_example_queries").runs.summary["short_table_1"].table.rows.concat,\
(row) => row["Label"],(row) => row["Label"], "Table1", "Table2",\
"false", "false")
```

![Table join operation](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/_media/weave_join.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=b8fb21eda2589c724c5e1b64713293fb)

The table on the left is generated from:

```python theme={"system"}
project("luis_team_test", "weave_example_queries").\
runs.summary["short_table_0"].table.rows.concat.join
```

The table on the right is generated from:

```python theme={"system"}
project("luis_team_test", "weave_example_queries").\
runs.summary["short_table_1"].table.rows.concat
```

Where:

* `(row) => row["Label"]` are selectors for each table, determining which column to join on.
* `"Table1"` and `"Table2"` are the names of each table when joined.
* `true` and `false` are for left and right inner/outer join settings.

## Runs object

Use query panels to access the `runs` object. Run objects store records of your experiments. For more details, see [Accessing runs object](https://forge.coreweave.com/wandb/luis_team_test/weave_example_queries/reports/Weave-queries---Vmlldzo1NzIxOTY2?accessToken=bvzq5hwooare9zy790yfl3oitutbvno2i6c2s81gk91750m53m2hdclj0jvryhcr#3.-accessing-runs-object). As a quick overview, the `runs` object has the following available:

* `summary`: A dictionary of information that summarizes the run's results. The summary can contain scalars like accuracy and loss, or large files. By default, `wandb.Run.log()` sets the summary to the final value of a logged time series. You can set the contents of the summary directly. Think of the summary as the run's outputs.
* `history`: A list of dictionaries meant to store values that change while the model is training, such as loss. The command `wandb.Run.log()` appends to this object.
* `config`: A dictionary of the run's configuration information, such as the hyperparameters for a training run or the preprocessing methods for a run that creates a dataset artifact. Think of these as the run's inputs.

![Runs object structure](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/_media/weave_runs_object.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=221fd5cc6e7b4b0da109e8e69e7116ff)

## Access artifacts

Artifacts are a core concept in Weights & Biases. They are a versioned, named collection of files and directories. Use artifacts to track model weights, datasets, and any other file or directory. Weights & Biases stores artifacts, and you can download them or use them in other runs. For more details and examples, see [Accessing artifacts](https://forge.coreweave.com/wandb/luis_team_test/weave_example_queries/reports/Weave-queries---Vmlldzo1NzIxOTY2?accessToken=bvzq5hwooare9zy790yfl3oitutbvno2i6c2s81gk91750m53m2hdclj0jvryhcr#4.-accessing-artifacts). You normally access artifacts from the `project` object:

* `project.artifactVersion()`: Returns the specific artifact version for a given name and version within a project.
* `project.artifact("")`: Returns the artifact for a given name within a project. You can then use `.versions` to get a list of all versions of this artifact.
* `project.artifactType()`: Returns the `artifactType` for a given name within a project. You can then use `.artifacts` to get a list of all artifacts with this type.
* `project.artifactTypes`: Returns a list of all artifact types under the project.

![Artifact access methods](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/_media/weave_artifacts.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=aa05642756d044c69a3c4609a3fd2f53)
