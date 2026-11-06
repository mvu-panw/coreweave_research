# YOLOv5

Source: https://docs.coreweave.com/products/wandb/integrations/yolov5

# YOLOv5

> Use Weights & Biases in YOLOv5 for experiment tracking, model versioning, and prediction visualization.

[Try in Colab](https://colab.research.google.com/github/wandb/examples/blob/master/colabs/yolo/Train_and_Debug_YOLOv5_Models_with_Weights_%26_Biases_.ipynb)

[Ultralytics' YOLOv5](https://www.ultralytics.com/yolo) ("You Only Look Once") model family enables real-time object detection with convolutional neural networks.

[Weights & Biases](https://wandb.com) integrates directly with YOLOv5, providing experiment metric tracking, model and dataset versioning, rich model prediction visualization, and more. **Run a single `pip install` before you run your YOLO experiments.**

> [!NOTE]
>
> All Weights & Biases logging features are compatible with data-parallel multi-GPU training, such as with [PyTorch DDP](https://pytorch.org/tutorials/intermediate/ddp_tutorial.html).

## Track core experiments

To get started, install the W\&B Python SDK (`wandb`) alongside YOLOv5 and run training as usual. By installing `wandb`, you activate the built-in Weights & Biases [logging features](https://docs.coreweave.com/products/wandb/track/log.md): system metrics, model metrics, and media logged to interactive [Dashboards](https://docs.coreweave.com/products/wandb/track/workspaces.md).

```bash theme={"system"}
pip install wandb
git clone https://github.com/ultralytics/yolov5.git
python yolov5/train.py  # train a small network on a small dataset
```

Follow the links that Weights & Biases prints to standard out.

![Weights & Biases dashboard showing YOLOv5 training metrics and system charts.](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/_media/yolov5_experiment_tracking.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=d93e6f498a7f8236e22b069ebc8c8f8a)

## Customize the integration

Once experiment tracking is working, you can enable additional Weights & Biases features (such as model versioning, dataset versioning, and prediction visualization) by passing a few command-line arguments to YOLO.

* If you pass a number to `--save_period`, Weights & Biases saves a [model version](https://docs.coreweave.com/products/registry.md) at the end of every `save_period` epochs. The model version includes the model weights and tags the best-performing model in the validation set.
* Turning on the `--upload_dataset` flag also uploads the dataset for data versioning.
* Passing a number to `--bbox_interval` turns on data visualization. At the end of every `bbox_interval` epochs, Weights & Biases uploads the outputs of the model on the validation set.

> [tab] Model versioning only
>
> ```bash theme={"system"}
> python yolov5/train.py --epochs 20 --save_period 1
> ```

> [tab] Model versioning and data visualization
>
> ```bash theme={"system"}
> python yolov5/train.py --epochs 20 --save_period 1 \
>   --upload_dataset --bbox_interval 1
> ```

> [!NOTE]
>
> Every Weights & Biases account comes with 100 GB of free storage for datasets and models.

Here's what that looks like.

![Model versioning](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/_media/yolov5_model_versioning.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=7ded6e99ba12fc48d616e1b40d5e0d2b)

![Data visualization](https://mintcdn.com/coreweave-dbfa0e8d/3Dv_sw2eg8feUJlx/products/wandb/_media/yolov5_data_visualization.png?fit=max\&auto=format\&n=3Dv_sw2eg8feUJlx\&q=85\&s=62be1027f2613749434d1fb7bfc82e5d)

> [!NOTE]
>
> With data and model versioning, you can resume paused or crashed experiments from any device, no setup necessary. See [the Colab](https://wandb.me/yolo-colab) for details.
