# Introduction to third-party frameworks

Source: https://docs.coreweave.com/products/cks/clusters/frameworks/introduction

# Introduction to third-party frameworks

> Integrate your CoreWeave Kubernetes Service (CKS) clusters with third-party tools and services

Any framework that runs on Kubernetes or in Linux containers works on [CoreWeave Kubernetes Service (CKS)](https://docs.coreweave.com/products/cks.md) and [SUNK](https://docs.coreweave.com/products/sunk.md). The following sections highlight popular AI and ML frameworks, grouped by category, with links to CoreWeave guides where available.

## Interactive development

The following table lists notebook environments and interactive UIs.

| Framework | Description | CKS guide | SUNK guide |
| - | - | - | - |
| [marimo](https://docs.marimo.io/) | Reactive notebook environment for interactive Python development with GPU support. | [marimo notebooks on CKS](https://docs.coreweave.com/products/cks/tutorials/marimo-notebooks.md) | [Notebooks on SUNK](https://docs.coreweave.com/products/sunk/tutorials/notebooks-on-sunk.md) |
| [Jupyter](https://jupyter.org/) | Interactive computing platform for notebooks, code, and data visualization. | Compatible on CKS | [Notebooks on SUNK](https://docs.coreweave.com/products/sunk/tutorials/notebooks-on-sunk.md) |
| [Open WebUI](https://docs.openwebui.com/) | Web-based chat interface for interacting with locally deployed language models. | [Deploy a model on CKS](https://docs.coreweave.com/products/cks/deploy-model.md) | Not applicable |

## Training frameworks

The following table lists frameworks used for training models and distributed training. CoreWeave also publishes optimized PyTorch base images you can use as a starting point for distributed training on CKS and SUNK. For details, see [ML container images](https://docs.coreweave.com/products/sunk/discover_sunk/ml-containers.md).

| Framework | Description | CKS guide | SUNK guide |
| - | - | - | - |
| [PyTorch](https://pytorch.org/) | Open source deep-learning framework with GPU acceleration and distributed training through `torchrun`. | Compatible on CKS | [Submit a training job](https://docs.coreweave.com/products/sunk/tutorials/train-on-sunk/3-submit-a-training-job.md) |
| [TensorFlow](https://www.tensorflow.org/) | Open source platform for building and deploying machine-learning models across a range of tasks. | Compatible on CKS | [Submit a training job](https://docs.coreweave.com/products/sunk/tutorials/train-on-sunk/3-submit-a-training-job.md) |
| [Keras](https://keras.io/) | High-level neural network API that runs on top of TensorFlow, JAX, or PyTorch. | Compatible on CKS | Compatible on SUNK |
| [JAX](https://docs.jax.dev/en/latest/) | High-performance numerical computing library with automatic differentiation and XLA compilation for GPUs and TPUs. | [JAX on marimo notebooks](https://docs.coreweave.com/products/cks/tutorials/marimo-notebooks/jax.md) | Compatible on SUNK |
| [Hugging Face Transformers](https://huggingface.co/docs/transformers/index) | Library for pretrained models for natural language processing, computer vision, and audio tasks. | Compatible on CKS | Compatible on SUNK |
| [DeepSpeed](https://www.deepspeed.ai/) | Deep-learning optimization library for distributed training and inference with memory-efficient techniques. | Compatible on CKS | Compatible on SUNK |
| [Megatron-LM](https://github.com/NVIDIA/Megatron-LM) | NVIDIA framework for training large transformer models using model and data parallelism. | Compatible on CKS | Compatible on SUNK |
| [Horovod](https://horovod.ai/) | Distributed deep-learning training framework supporting TensorFlow, Keras, PyTorch, and Apache MXNet. | Compatible on CKS | Compatible on SUNK |
| [PaddlePaddle](https://www.paddlepaddle.org.cn/en) | Deep-learning framework with support for distributed training and model deployment. | Compatible on CKS | Compatible on SUNK |
| [PAX](https://github.com/google/paxml) | JAX-based framework for configuring and running ML experiments at scale. | Compatible on CKS | Compatible on SUNK |
| [BigDL](https://github.com/intel/ipex-llm) | Distributed deep-learning library for Apache Spark and Intel hardware. | Compatible on CKS | Compatible on SUNK |
| [MegEngine](https://github.com/MegEngine/MegEngine) | Deep-learning framework with dynamic and static graph support. | Compatible on CKS | Compatible on SUNK |
| [MindSpore](https://www.mindspore.cn/en) | AI computing framework for training and inference across cloud, edge, and device. | Compatible on CKS | Compatible on SUNK |
| [torchforge](https://github.com/meta-pytorch/torchforge) | Training framework for reinforcement learning with group relative policy optimization (GRPO). | Compatible on CKS | [torchforge on SUNK](https://docs.coreweave.com/products/sunk/tutorials/torchforge-on-sunk.md) |
| [veRL](https://github.com/verl-project/verl) | Framework for reinforcement learning training of large language models with Slurm and Ray integration. | Compatible on CKS | [veRL on SUNK](https://docs.coreweave.com/products/sunk/tutorials/verl-on-sunk.md) |

## Inference frameworks

The following table lists frameworks used for model serving and inference.

| Framework | Description | CKS guide | SUNK guide |
| - | - | - | - |
| [vLLM](https://docs.vllm.ai/en/latest/) | High-throughput and memory-efficient LLM inference and serving engine. | [Deploy vLLM inference](https://docs.coreweave.com/products/cks/tutorials/deploy-vllm-inference.md) | Compatible on SUNK |
| [SGLang](https://docs.sglang.io/) | Serving framework for large language models and vision language models. | [SGLang on CKS](https://docs.coreweave.com/products/cks/clusters/frameworks/sglang.md) | Compatible on SUNK |
| [NVIDIA TensorRT](https://developer.nvidia.com/tensorrt) | GPU inference optimizer that delivers low-latency and high-throughput model serving. | Compatible on CKS | Compatible on SUNK |
| [NVIDIA TensorRT-LLM](https://nvidia.github.io/TensorRT-LLM/) | Library for optimizing and deploying large language model inference on GPUs. | [TensorRT-LLM on marimo notebooks](https://docs.coreweave.com/products/cks/tutorials/marimo-notebooks/tensorrt.md) | Compatible on SUNK |
| [NVIDIA NIM](https://docs.nvidia.com/nim/) | NVIDIA inference microservices for deploying optimized AI models as containerized services. | [Deploy NIMs on CKS](https://docs.coreweave.com/products/cks/tutorials/hello-world-nims-on-cks.md) | Compatible on SUNK |
| [NVIDIA Dynamo](https://github.com/ai-dynamo/dynamo) | Cluster-wide inference orchestration with the Kai scheduler and Grove. | [Dynamo inference on CKS](https://docs.coreweave.com/products/cks/tutorials/dynamo-inference.md) | Compatible on SUNK |
| [Red Hat AI Inference Stack](https://github.com/opendatahub-io/rhaii-on-xks) | GPU-based LLM inference using llm-d, KServe, Istio, and the Gateway API. | [Red Hat AI on CKS](https://docs.coreweave.com/products/cks/tutorials/redhat-inference.md) | Compatible on SUNK |
| [OpenVINO](https://docs.openvino.ai/2026/index.html) | Intel toolkit for optimizing and deploying inference across CPU, GPU, and accelerator hardware. | Compatible on CKS | Compatible on SUNK |
| [TensorFlow Lite](https://developers.google.com/edge/litert) | Lightweight runtime for running TensorFlow models on edge and mobile devices. | Compatible on CKS | Compatible on SUNK |

## Orchestration and management

The following table lists frameworks for scheduling workloads and managing ML operations on clusters.

| Framework | Description | CKS guide | SUNK guide |
| - | - | - | - |
| [Ray](https://docs.ray.io/en/latest/) | Distributed computing framework for scaling AI and Python applications across clusters. | [Ray with Kueue](https://docs.coreweave.com/products/cks/clusters/frameworks/ray-with-kueue.md) | [Ray on SUNK](https://docs.coreweave.com/products/sunk/tutorials/ray-on-sunk.md) |
| [Anyscale](https://docs.anyscale.com/) | Managed platform for deploying and scaling Ray-based distributed AI and ML workloads. | [Anyscale on CKS](https://docs.coreweave.com/products/cks/clusters/frameworks/anyscale.md) | Compatible on SUNK |
| [Kubeflow](https://www.kubeflow.org/) | Open source machine-learning platform for portable, scalable ML workflows on Kubernetes. | [Kubeflow on CKS](https://docs.coreweave.com/products/cks/clusters/frameworks/kubeflow.md) | Compatible on SUNK |
| [SkyPilot](https://docs.skypilot.ai/en/latest/) | Framework for running AI and ML workloads across cloud infrastructure. | [SkyPilot on CKS](https://docs.coreweave.com/products/cks/tutorials/skypilot.md) | [SkyPilot on SUNK](https://docs.coreweave.com/products/sunk/tutorials/skypilot-on-sunk.md) |
| [Union.ai](https://www.union.ai/) | Managed platform for Flyte, providing workflow orchestration for data and ML pipelines with a hosted control plane. | [Union.ai on CKS](https://docs.coreweave.com/products/cks/clusters/frameworks/union-ai.md) | Compatible on SUNK |
| [Kueue](https://kueue.sigs.k8s.io/) | Kubernetes-native job queueing system for prioritized workload scheduling and resource management. | [Ray with Kueue](https://docs.coreweave.com/products/cks/clusters/frameworks/ray-with-kueue.md) | Compatible on SUNK |

## Code execution sandboxes

The following table lists platforms that run untrusted or AI-generated code in isolated environments.

| Framework | Description | CKS guide | SUNK guide |
| - | - | - | - |
| [SPACE](https://github.com/perplexityai/SPACE) | Open source platform from Perplexity that runs code in isolated Firecracker microVMs through an HTTP API. | [SPACE on CKS](https://docs.coreweave.com/products/cks/clusters/frameworks/space.md) | Not applicable |

## ML libraries

The following table lists general-purpose machine-learning and AutoML libraries.

| Framework | Description | CKS guide | SUNK guide |
| - | - | - | - |
| [XGBoost](https://xgboost.readthedocs.io/en/release_3.2.0/) | Optimized gradient boosting library for classification, regression, and ranking tasks. | Compatible on CKS | Compatible on SUNK |
| [scikit-learn](https://scikit-learn.org/) | General-purpose machine-learning library for classification, regression, clustering, and preprocessing. | Compatible on CKS | Compatible on SUNK |
| [MLlib](https://spark.apache.org/mllib/) | Apache Spark's distributed machine-learning library for classification, regression, clustering, and pipelines. | Compatible on CKS | Compatible on SUNK |
| [ML.NET](https://dotnet.microsoft.com/en-us/apps/ai/ml-dotnet) | Cross-platform machine-learning framework for .NET applications. | Compatible on CKS | Compatible on SUNK |
| [TPOT](http://epistasislab.github.io/tpot/) | Automated machine-learning tool that optimizes ML pipelines using genetic programming. | Compatible on CKS | Compatible on SUNK |
| [AutoKeras](https://autokeras.com/) | AutoML library built on Keras for automated neural architecture search. | Compatible on CKS | Compatible on SUNK |
| [Auto-sklearn](https://automl.github.io/auto-sklearn/) | AutoML toolkit that automatically selects and tunes scikit-learn models. | Compatible on CKS | Compatible on SUNK |
| [PlaidML](https://github.com/plaidml/plaidml) | Portable deep-learning backend that runs on a variety of hardware including CPUs and GPUs. | Compatible on CKS | Compatible on SUNK |

## GPU acceleration libraries

The following table lists GPU-accelerated computing libraries.

| Framework | Description | CKS guide | SUNK guide |
| - | - | - | - |
| [cuDNN](https://developer.nvidia.com/cuda/cuda-x-libraries/cudnn) | NVIDIA GPU-accelerated library of primitives for deep neural networks. | Compatible on CKS | Compatible on SUNK |
| [cuBLAS](https://developer.nvidia.com/cublas) | NVIDIA GPU-accelerated implementation of the BLAS (Basic Linear Algebra Subprograms) standard. | Compatible on CKS | Compatible on SUNK |

## Deprecated frameworks

The following frameworks are deprecated or no longer actively maintained by their upstream projects. They can still run on CKS and SUNK in custom container images.

| Framework | Description | Status |
| - | - | - |
| [Apache MXNet](https://mxnet.apache.org/versions/1.9.1/) | Distributed deep-learning framework. | Retired by the Apache Software Foundation in 2023. |
| [Caffe](https://caffe.berkeleyvision.org/) and [Caffe2](https://caffe2.ai/) | Deep-learning frameworks for image classification and convolutional networks. | Caffe2 merged into PyTorch. Caffe is no longer actively maintained. |
| [Chainer](https://chainer.org/) | Deep-learning framework with a define-by-run approach. | Development ended in 2019. Successor: PyTorch. |
| [Microsoft Cognitive Toolkit (CNTK)](https://learn.microsoft.com/en-us/previous-versions/cognitive-toolkit/) | Deep-learning framework for distributed training. | Archived by Microsoft in 2019. |
| [Theano](https://github.com/Theano/Theano) | Numerical computation library with GPU support for defining and optimizing mathematical expressions. | Development ended in 2017. |
| [Torch](http://torch.ch/) | Scientific computing framework with GPU support based on Lua. | Superseded by PyTorch. |

> [!NOTE]
>
> This list isn't exhaustive. If a framework isn't listed, you can build custom container images and deploy them on CKS or SUNK.
