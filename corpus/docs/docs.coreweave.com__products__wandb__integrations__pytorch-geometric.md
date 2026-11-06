# PyTorch Geometric

Source: https://docs.coreweave.com/products/wandb/integrations/pytorch-geometric

# PyTorch Geometric

> Use Weights & Biases with PyTorch Geometric for graph visualization and experiment tracking in geometric deep learning.

[PyTorch Geometric](https://github.com/pyg-team/pytorch_geometric) (PyG) is a library for geometric deep learning, and Weights & Biases works with it for visualizing graphs and tracking experiments.

This guide shows you how to authenticate to Weights & Biases, install the `wandb` library, visualize PyG graphs with PyVis or Plotly, and log training metrics from your PyG workflows. Use it to track experiments and share graph visualizations in Weights & Biases.

After you install PyTorch Geometric, follow these steps to get started.

## Sign up and create an API key

An API key authenticates your machine to Weights & Biases. You can generate an API key from your user profile.

> [!NOTE]
>
> For a more streamlined approach, go to [User settings](https://forge.coreweave.com/settings) and create an API key. Copy the API key immediately and save it in a secure location such as a password manager.

1. Click the account selector in the upper-right corner.
2. Select **User settings**, then scroll to the **API keys** section.

## Install the `wandb` library and log in

To install the `wandb` library locally and log in:

> [tab] Command Line
>
> 1. Set the `WANDB_API_KEY` [environment variable](https://docs.coreweave.com/products/wandb/track/environment-variables.md) to your API key. Replace values enclosed in `<>` with your own:
>
>    ```bash theme={"system"}
>    export WANDB_API_KEY=<your_api_key>
>    ```
>
> 2. Install the `wandb` library and log in.
>
>    ```bash theme={"system"}
>    pip install wandb
>
>    wandb login
>    ```

> [tab] Python
>
> ```bash theme={"system"}
> pip install wandb
> ```
>
> ```python theme={"system"}
> import wandb
> wandb.login()
> ```

> [tab] Python notebook
>
> ```python theme={"system"}
> !pip install wandb
>
> import wandb
> wandb.login()
> ```

## Visualize the graphs

After you log in, you can begin sending graph visualizations and run data to Weights & Biases.

You can save details about the input graphs, including number of edges, number of nodes, and more. Weights & Biases supports logging Plotly charts and HTML panels, so you can also log any visualizations you create for your graph to Weights & Biases. The following sections show two common approaches: PyVis for interactive HTML visualizations and Plotly for chart-based visualizations.

### Use PyVis

The following snippet shows how to do that with PyVis and HTML.

```python theme={"system"}
from pyvis.network import Network
import wandb

with wandb.init(project="graph_vis") as run:
    net = Network(height="750px", width="100%", bgcolor="#222222", font_color="white")

    # Add the edges from the PyG graph to the PyVis network
    for e in tqdm(g.edge_index.T):
        src = e[0].item()
        dst = e[1].item()

        net.add_node(dst)
        net.add_node(src)
        
        net.add_edge(src, dst, value=0.1)

    # Save the PyVis visualisation to a HTML file
    net.show("graph.html")
    run.log({"eda/graph": wandb.Html("graph.html")})
```

![Interactive graph visualization](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/_media/pyg_graph_wandb.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=4ce993545929de04d41a487948821f7b)

### Use Plotly

To use Plotly to create a graph visualization, first convert the PyG graph to a networkx object. Then create Plotly scatter plots for both nodes and edges. Use the following snippet for this task.

```python theme={"system"}
def create_vis(graph):
    G = to_networkx(graph)
    pos = nx.spring_layout(G)

    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines'
    )

    node_x = []
    node_y = []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        hoverinfo='text',
        line_width=2
    )

    fig = go.Figure(data=[edge_trace, node_trace], layout=go.Layout())

    return fig


with wandb.init(project="visualize_graph") as run:
    run.log({"graph": wandb.Plotly(create_vis(graph))})
```

![A visualization created using the example function and logged inside a W\&B Table.](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/_media/pyg_graph_plotly.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=3deabcd8fc683e4dcf6ac4495dd03125)

## Log metrics

In addition to graph visualizations, you can use Weights & Biases to track your experiments and related metrics, such as loss functions, accuracy, and more. Add the following lines to your training loop:

```python theme={"system"}
with wandb.init(project="my_project", entity="my_entity") as run:
    run.log({
        'train/loss': training_loss,
        'train/acc': training_acc,
        'val/loss': validation_loss,
        'val/acc': validation_acc
        })
```

![hits@K metrics over epochs](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/_media/pyg_metrics.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=c4ab3efbe0dec7b76ca97d1234655654)

With graph visualizations and training metrics logged to Weights & Biases, you can compare runs and share results from your PyG experiments in your Weights & Biases workspace.

## More resources

The following W\&B reports show PyG in action:

* [Recommending Amazon Products using Graph Neural Networks in PyTorch Geometric](https://forge.coreweave.com/wandb/manan-goel/gnn-recommender/reports/Recommending-Amazon-Products-using-Graph-Neural-Networks-in-PyTorch-Geometric--VmlldzozMTA3MzYw#what-does-the-data-look-like?)
* [Point Cloud Classification using PyTorch Geometric](https://forge.coreweave.com/wandb/geekyrakshit/pyg-point-cloud/reports/Point-Cloud-Classification-using-PyTorch-Geometric--VmlldzozMTExMTE3)
* [Point Cloud Segmentation using PyTorch Geometric](https://forge.coreweave.com/wandb/wandb/point-cloud-segmentation/reports/Point-Cloud-Segmentation-using-Dynamic-Graph-CNN--VmlldzozMTk5MDcy)
