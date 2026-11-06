# Serving LLM Inference with NVIDIA Triton and Eleuther AI

Source: https://www.coreweave.com/blog/serving-inference-for-llms-nvidia-triton-inference-server-eleuther-ai

Announcement

Webinar

Podcast

GTC 2026

CoreWeave Forge is here: connect your AI loop and compound every improvement. Read more

Contact us

### NVIDIA Triton Inference Server helped reduce latency by up to 40% for Eleuther AI’s GPT-J and GPT-NeoX-20B.
Efficient inference relies on fast spin-up times and responsive auto-scaling. Without it, end users may experience annoying latency and move on to a different application next time. But serving inference for large language models (LLMs) is not as simple as the type of GPU you’re using—or even the number of GPUs.
That’s why it’s critical to leverage the right tools (infrastructure, software, GPUs, etc.) that deliver fast and scalable AI in production and help standardize model deployment and execution.
In a session at GTC23, Peter Salanki, VP of Engineering at CoreWeave, and Shankar Chandrasekaran, Senior Product Marketing Manager for Accelerated Computing at NVIDIA, discuss solutions to this challenge, plus:
- The importance of infrastructure when serving inference for LLMs
- How to improve the speed and efficiency of models using the NVIDIA Triton Inference Server with the FasterTransformer backend
- How to seamlessly autoscale and access GPUs in the cloud to serve inference with CoreWeave Inference Service
- Benchmark comparisons between Triton Inference Server and HuggingFace for Eleuther AI’s GPT-J and GPT-NeoX-20B
‍
Click here to watch the session and visit NVIDIA On-Demand for more sessions, podcasts, demos, research posters, and more.
‍

## More Parameters, More GPUs, More Costs
Over the last year, LLMs have ballooned in size. The major LLMs known today include billions of parameters. ChatGPT-3 from OpenAI, the generative AI model that had everyone talking this year, contains 175 billion parameters. That’s a big increase from OpenAI’s ChatGPT-J-6B, a six-billion parameter open-source version. BLOOM, launched just months prior, contains 176 billion parameters. 
As model size increases, especially in the area of natural language processing, models expand past the number of parameters that can fit on a single GPU memory—requiring multiple GPUs to run inference on these models without skirting performance. But, as teams scale across more GPUs, the cost to serve inference scales, too—often outpacing what a company can afford. Another consideration is that many LLM-based services run in real time, so low latency is a must to deliver great user experiences.
Teams today need an efficient way to serve inference from LLMs that allows infrastructure to scale across multiple GPUs—without breaking the bank. This forces companies to consider multiple factors when serving inference from LLMs:
- How to get high performance (high throughput and inference accuracy)
- How to ensure it’s cost-effective (affordable access to GPUs at scale)
- How to create a good user experience (low latency)
Two solutions stand out, which can be used together as shown in the case study with Eleuther AI’s two models. One, engineers can leverage software like the NVIDIA Triton Inference Server that enables high-performance multi-GPU, multi-node inference. Two, leveraging cloud solutions that are built to scale.
‍

## What is NVIDIA Triton Inference Server?
Triton Inference Server is an open-source inference serving software that streamlines and standardizes AI inference by enabling teams to deploy, run, and scale trained AI models from any framework on any GPU- or CPU-based infrastructure.Part of the NVIDIA AI Enterprise software platform, Triton helps developers and teams deliver high-performance inference for maximal throughput and utilization.
How Triton delivers a fast, scalable, and simplified inference serving:
- Any Framework: It natively supports multiple popular frameworks and languages like Tensorflow, PyTorch, ONNX, and Python as execution backends. That way, there is a consistent way to deploy models across frameworks.
- Any Query Type:  It optimizes inference for different query types (like real time, batch, and audio/video streaming) and even supports a pipeline of models and pre/post-processing for inference.
- Any platform: It allows models to run on CPU or GPU on any platform: cloud, data center, or edge.
- DevOps/MLOps Ready: It is integrated  with major DevOps & MLOps tools.
- High Performance: It is a high-performance serving software that maximizes GPU/CPU utilization and thus provides very high throughput and low latency.

#### FasterTransformer Backend
The way Triton Inference Server can be used for LLMs is through a backend called FasterTransformer. 
FasterTransformer (FT) is NVIDIA's open-source framework to optimize the inference computation of Transformer-based models and enable model parallelism.
This backend was designed for LLM inference—specifically multi-GPU, multi-node inference—and supports transformer-based infrastructure, which is what most LLMs use today.
FasterTransformer optimized execution with two types of parallelism: pipeline parallelism and tensor parallelism. It also enables efficient inter-node communication, which is vital for performance when running inference across multiple GPUs. Take a look at the charts below to learn more. 
image curtesy of NVIDIA: the FasterTransformer backend
‍

## CoreWeave Inference Service: Faster spin-up times, more responsive autoscaling 
Another major challenge companies face around serving inference is limited access to GPUs. Despite reserving instances of top-tier GPUs well in advance, teams can struggle to access the scale of GPUs needed as well as the types of GPUs that work best for serving inference. All the while, they could be paying a heavy premium from a cloud provider.
CoreWeave helps companies avoid this common trap. A specialized cloud provider built for GPU-accelerated workloads, CoreWeave provides unparalleled access to a broad range of NVIDIA GPUs, available at scale and on demand. Companies can spin up a new GPU on CoreWeave in as little as 5 seconds for smaller models and less than one minute for larger models.  
CoreWeave Inference Service, its compute solution for companies serving inference in the cloud, offers a modern way to run inference that delivers better performance and minimal latency while being more cost-effective than other platforms. This solution enables teams to serve inference faster with infrastructure that actually scales with them.
Advantages of CoreWeave Inference Service include: 
- Access GPUs on-demand from a wide variety of highly-available NVIDIA GPUs 
- Autoscale with ease; go from 0 to 1,000s of GPUs and down again automatically
- Spin-up new instances faster; scale-up GPT-J in 10 seconds; NeoX in 15 seconds
- Deploy in your preferred framework, including TensorFlow, PyTorch, and more; with a single YAML
- Easily install applications directly on a lightweight OS and without additional installation libraries

#### Enabling more responsive auto-scaling
CoreWeave Inference Service was built for scale—so teams never get crushed by user growth or hardware costs. Engineers can autoscale containers based on demand to quickly fulfill user requests significantly faster than cloud infrastructure that depends on scaling of hypervisor backed instances. As soon as a new request comes in, requests can be served as quickly as 5 seconds for small models, 10 seconds for GPT-J, 15 seconds for NeoX in 15, and 30-60 seconds for larger models.
How it works: Scaling is controlled in the InferenceService configuration. Developers can set autoscaling to always run one replica, regardless of number of requests. Increasing the number of maxReplicas will allow the CoreWeave infrastructure to automatically scale up replicas when there are multiple outstanding requests to your endpoints. 
Replicas will automatically be scaled down as demand decreases. By setting minReplicas to 0, Scale-to-Zero can be enabled, which will completely scale down the InferenceService when there have been no requests for a period of time.
‍

## Benchmarks: Testing on GPT-J and GPT-NeoX-20B
CoreWeave tested NVIDIA Triton Inference Server against non-optimized vanilla HuggingFace PyTorch implementation on EleutherAI’s GPT-J and GPT-NeoX-20B, an open-source 20-billion parameter LLM that launched in February 2022. 

#### Performance on GPT-J
This example was set to use one NVIDIA RTX A5000 PCIe GPU. CoreWeave has performed prior benchmarking to analyze performance of Triton with FasterTransformer against the vanilla Hugging Face version of GPTJ-6B. For additional performance for handling large models, FasterTransformer supports running over multiple GPUs and streaming of partial completions, token by token.
Key observations for:
- 30% faster tokens_per_second in general using FasterTransformer GPTJ vs. Hugging Face
-  2X average speedups for GPTJ using multiple (4) GPUs vs. 1 GPU on Hugging Face

#### Performance: GPT-NeoX-20B
Looking at the larger, 20-billion parameter model, we see strong performance, as well. This example was set to use one NVIDIA A40 PCIe GPU, since the model weights are too large to fit on one NVIDIA RTX A5000 GPU. 
Key observations: 
- 15.6 tokens/second on average for a 1024 token input context
- For additional performance, FasterTransformer supports running over multiple GPUs
Taking a look at the results from both tests, CoreWeave concluded that Triton Inference Server with FasterTransformer can accelerate inference for most GPT-based LLMs with an expected 30-40% improvement in speed compared to a non-optimized vanilla HuggingFace PyTorch implementation.
Read more about how we conducted the test in our documentation. Learn more about NVIDIA Triton Inference Server, and reach out to our team to learn how you can serve inference in the cloud. 

Share this article:

Copied

## Related blogs

### Convergent Science Advances Engineering Simulation on CoreWeave

10
min read

### CoreWeave Builds the First Global Backbone Network Purpose-Built for AI

5
min read

### Post-Training at the Frontier

7
min read

### CoreWeave Powers Agentic AI, HPC, and Data Analytics Workloads with NVIDIA HGX Rubin NVL8

5
min read

### Introducing CoreWeave Physical AI Launchables: Run Workloads With One Command

min read

### CoreWeave Zero Trust AI Framework: Your Model. Your Data. Your Trust. 

8
min read

### From Training to Serving: Reflection’s Beam on CoreWeave

min read

### Why the AI Loop Will Test Every Security Assumption

min read

### Agents on Live Hardware: Reason Where You Must, Engineer Everywhere Else

min read

### CoreWeave Direct-to-Expert: Work With the Engineers Who Built CoreWeave Cloud

5
min read

- Contact us
- Login

### Products
- GPU Compute
- CPU Compute
- Storage Services
- Networking Services
- Managed Services
- Bare Metal Servers
- 
Platform
- Fleet LifeCycle Controller

- Node LifeCycle Controller
- Tensorizer
- Observability

### Solutions
- AI Model Training
- AI Inference
- VFX & Rendering
- Mission Control

### AI Infrastructure

### Why CoreWeave

### Resources
- Customer Stories
- Documentation
- Status
- Pricing
- Resource Center
- Events & Webinars

### About
- About Us
- Careers
- Life at CoreWeave
- 
- Newsroom
- Investors
- Supplier Code of Conduct
- GHG Emissions Statement
- Privacy Policy
- Terms of Service
- 
Do Not Sell or Share My Personal Information

© CoreWeave.
290 W Mt Pleasant Ave
Suite 4100
Livingston, NJ 07039 

- 

- 

Inference,

Copy code

Copied!

Inference,
