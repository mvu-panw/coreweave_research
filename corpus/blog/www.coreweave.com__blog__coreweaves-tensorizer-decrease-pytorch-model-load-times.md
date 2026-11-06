# Decrease PyTorch Model Load Times with CoreWeave’s Tensorizer | CoreWeave

Source: https://www.coreweave.com/blog/coreweaves-tensorizer-decrease-pytorch-model-load-times

Announcement

Webinar

Podcast

GTC 2026

CoreWeave Forge is here: connect your AI loop and compound every improvement. Read more

Contact us

### CoreWeave Tensorizer: In Summary
- CoreWeave Tensorizer is a tool for fast PyTorch module, model, and tensor serialization and deserialization, making it possible to load models extremely quickly from HTTP/HTTPS and S3 endpoints. It also speeds up loading from network and local disk volumes.
- With faster model loading times for LLMs and reduces GPU memory utilization, Tensorizer helps accelerate model instance spin up times while reducing overall costs to serve inference.
- Tensorizer is S3/HTTP-compatible, enabling model streams directly from S3 into the container without having to download the model to the container's local filesystem.
- The average latency per request was >5x faster for Tensorizer compared to Hugging Face when scaling from zero, and required fewer pod spin ups and less RAM. 
The sizes of state-of-the-art machine learning models have ballooned into billions of parameters, which means using them for inference is becoming much harder. These massive models can take a long time to load, which can severely impact the ability to quickly scale up with increases in demand. To mitigate the startup lead time, you can pay to have large quantities of GPUs sitting idle ready for bursts in requests but this is a very expensive solution.
To improve inference performance while maintaining cost-effectiveness, CoreWeave employs a range of open-source tools to help reduce latency, improve throughput, and reduce resource usage. One such tool is vital for enabling companies to scale inference in a fast and cost-efficient way: CoreWeave Tensorizer.

## What is CoreWeave’s Tensorizer?
CoreWeave Tensorizer is a tool built for PyTorch models that enables extremely fast and efficient model loading. 
Whereas the process to load a very large model into GPU memory through normal means can be slow, Tensorizer significantly reduces latency and resource usage with its “zero-copy” model loading. Instead of loading the whole model into RAM before transferring it to the GPU, Tensorizer pulls it over chunk by chunk. This “tensor streaming” process is enabled by Tensorizer’s bespoke serialization format that puts all the necessary metadata at the beginning of a single binary file. This file can be loaded quickly and efficiently from local storage, an HTTP/HTTPS endpoint, or S3 bucket. 
High-level features of Tensorizer:
- Extremely fast model loading speeds: By not needing to use Python to allocate memory for the entire model and performing a single pass through the serialized file, Tensorizer can load models with billions of parameters in as little as 5 seconds.
- Reduction in resource and memory usage: Transfers occur with the wire speed of the network to the GPU when using CoreWeave Tensorizer, so the amount of RAM necessary for the instance is greatly reduced due to only storing a single tensor at a time in memory, while in transit to the GPU, with Tensorizer’s “Plaid Mode”. 
Via a “zero-copy” model load, CoreWeave Tensorizer will use a negligible amount of RAM compared to loading the entire model into memory before copying it into the GPU. CoreWeave Tensorizer uses a buffer of the largest tensor size plus some additional metadata to fetch the locations of tensors.
- S3/HTTP-compatible: Serialized models can be stored in CoreWeave's S3-compatible Object Storage, enabling model streams directly from S3 into the container without having to download the model to the container's local filesystem.
- Sharding and Filtering: Tensorizer can accept a filter function to select for specific tensors in a model, allowing for fast sharding of a large model across multiple nodes. This is augmented by Tensorizer’s HTTP range support for seeking to specific tensors.
- Local filesystem support: CoreWeave Tensorizer supports loading models from a local filesystem, so it can be used to serialize and load models locally.
- Improved Safety: A normal PyTorch checkpoint file uses the pickle format, which can enable arbitrary code execution. By using a single binary file, Tensorizer prevents this potential security threat.  

### What this means for serving large models
When serving inference, requests aren’t always coming in at a steady load. One day, your product might go viral and you might receive a burst of requests much higher than normal.
However, for LLMs and image models with billions of parameters, spinning up new instances of the model to handle these bursts can take many minutes. This is a major challenge for companies looking to serve inference from these models. To maintain an average request latency, many companies will accept the large overhead of compute that sits idle with the model loaded, only to be used during these bursts. This can be very expensive, so in an attempt to reduce the cost, companies will build complex and specialized queuing mechanisms which attempts to save money by reducing the required overhead but increases average customer latency.
Customer latency and compute costs are often at odds with each other, but with CoreWeave’s Tensorizer, developers can see model load times of <5 seconds. This makes it easier, more flexible, and more cost-efficient to serve large models at scale while scaling with demand.
Faster spin-up times are a massive differentiator for the user experience. If a general Google search took 30 seconds or more to load a user’s first inquiry, we would probably say “Bing it,” rather than “Google it.” 
For a company looking to productize its machine learning applications, it’s important to consider the trade-off between cost vs. latency. Leaving idle compute without much traffic can lead to unnecessary expenses. Leveraging faster spin-up can cause additional latency in response time compared to having idle compute ready, but not nearly to the degree of other model loading methods. Long response times can lead users to not use the service or product. Therefore, it is important to balance both, and tools like CoreWeave Tensorizer help companies find a balance that suits their application.  
CoreWeave’s Tensorizer also makes serving inference more affordable. Companies pay a steep price for the resources needed for inference (GPU capacity, memory bandwidth, storage fees, networking, etc.). By enabling fast scaling, CoreWeave’s Tensorizer reduces the cost of serving inference at scale from large language, image, and audio models.

## How CoreWeave’s Tensorizer Works
To understand how CoreWeave’s Tensorizer works, it’s important to understand how CoreWeave compares to a typical inference setup and the serialization process. 

### Open source tools for serverless deployment
CoreWeave Cloud is built on serverless Kubernetes, an open-source deployment framework that allows developers to run their applications as if in a serverless model while still enjoying the benefits of a bare-metal Kubernetes platform. This enables CoreWeave Cloud users to run their own code, manage data, and integrate applications—without ever having to manage any infrastructure.
Inference on CoreWeave Cloud leverages many well-supported open source tools within, and in addition to, Kubernetes:
- Knative Serving acts as the serverless runtime, which manages autoscaling, revision control, and canary deployments; in short, the load balancer and autoscaler.
- KServe provides an easy-to-use interface via Kubernetes resource definitions for deploying models without the fuss of correctly configuring the underlying framework (i.e., TensorFlow).
- Ceph, a software-defined, scale-out, enterprise-grade storage platform. Built with triple replication, the CoreWeave Cloud Storage platform is built to provide high-availability, performant storage for your most demanding Cloud-native workloads.
These open-source tools enable seamless autoscaling and scale to zero. Combined with bare-metal performance and high-performance, network-attached storage volumes, these features enable users on CoreWeave Cloud to see improved throughput and minimal latency for serving inference.
However, model load time is still a major factor in the latency of Knative scale-up. This is where CoreWeave’s Tensorizer fits in. As an efficient serializer and deserializer, CoreWeave’s Tensorizer helps reduce the time it takes for a new model instance to be ready—improving overall latency and performance with minimal resource utilization.
How Tensorizer fits into the flow of the request in the inference engine on CoreWeave Cloud
‍
CoreWeave Tensorizer helps shrink overhead, which enables faster model load times.

### Serialization and Deserialization
Both serialization and deserialization are important processes for serving inference for large models because these models are too big to be stored on a single GPU.
Serialization is the process of converting a data object (e.g. a model) into a format that can be stored or transmitted. This is a slow process that’s not optimized for writing; it’s meant to happen only a few times compared to deserialization, which is that process in the opposite direction: recreating the data object when needed. 
CoreWeave’s Tensorizer serializes a model into a single binary file. This requires the metadata up front and supports bfloat16. This is a safe process since no arbitrary code is saved.
Many of Tensorizer’s benefits come to life during deserialization:
- Efficient streaming. Unlike normal deserialization, which loads all the tensors into a single buffer, Tensorizer uses CURL to load the binary file tensor by tensor. This is a common use case at CoreWeave because our accelerated object storage solution allows us to use a single S3 endpoint to pull from caches local to the respective data center region.
- Lazy loading. The metadata is loaded into memory first, which allows for efficient loading of the tensor data with a single, efficient pass through the file. Since the metadata is at the beginning of the file, you can only load the tensors you care about. This allows you to use a single tensorized file for many different distributions simply by using a different lazy loading filter for each rank.
- Zero-copy “plaid mode.” A single buffer is used for each tensor before it is copied into the GPU, meaning each new tensor overwrites the previous one. This isn’t ideal for training, in which every tensor in the GPU is mapped to the same buffer, but it does make it very fast—perfect for inference. This keeps memory usage very low since only the metadata and one tensor at a time is in memory, so you don’t have to pay for slow Python memory allocation.
A quick note about shared tensors. Some models have multiple layers pointing to the same tensor, which some LLMs use for the word token embeddings and the LM head. The purpose is to save GPU memory and help training since gradient flow isn’t great going all the way back to the word token embeddings. 
CoreWeave’s Tensorizer writes the same tensor to the tensorized file twice; tensors are not shared when the model is deserialized. SafeTensors also supports shared tensors. In the benchmark section that follows, the tensor is cloned before having SafeTensors serialize it, matching the behavior of CoreWeave’s Tensorizer. Adding support for non-slice shared tensors is in the backlog and will be implemented soon for CoreWeave’s Tensorizer.

## Benchmarks for CoreWeave’s Tensorizer
For the following benchmarks, all frameworks loaded files off of CoreWeave’s NVMe-backed shared file system, so no downloading was required. All the code we used to create these benchmarks is available in the public coreweave/tensorizer repo. 
For HuggingFace, the transformer library was used to initialize the model from its pytorch.bin file. For SafeTensors, the transformers or SafeTensors library was used to load the ‘model.safetensors’ file. 

### Smaller model metrics
In the first test, we compared CoreWeave’s Tensorizer with SafeTensors and HuggingFace on Eleuther AI’s GPT-J-6B with NVIDIA A40 GPUs. In the chart below, you see that Tensorizer recorded the fastest model load time:
- CoreWeave’s Tensorizer: 8.22 sec. (median); 10.74 sec. (average)
- SafeTensors: 10.87 sec. (median); 15.07 sec. (average)
- Hugging Face: 15.02 sec. (median); 17.26 sec. (average)
‍

### Larger model metrics
When tested on a larger model size using a higher-performing GPU, the impact of Tensorizer on model load time significantly increased. The chart below shows that CoreWeave’s Tensorizer outperformed both SafeTensors and Hugging Face on average model load times on OPT-30B with NVIDIA A100 Tensor Core GPUs.
- CoreWeave’s Tensorizer: 23.23 sec. (median); 22.8 sec. (average)
- SafeTensors: 36.75 sec. (median); 39.3 sec. (average)
- HuggingFace: 35.18 sec. (median); 32.1 sec. (average)
‍

### Tensorizer vs. Hugging Face
Going back to GPT-J-6B, we wanted to test how Tensorizer compared to Hugging Face for resource utilization, RAM, and average request latency. For this test, 100 concurrent asynchronous requests were sent to two endpoints (Hugging Face vs. Tensorizer) with maximum number of replicas set to 100.
Key findings:
- Average latency per request is >5x faster for Tensorizer due to fast model loading
- Tensorizer required fewer pods spun up due to faster container spin up, which allows for more requests to be served
- Significantly less RAM usage for “lazy loading,” which was done here, on Tensorizer compared to Hugging Face
‍

## Pre-built Tensorizer Models on CoreWeave Cloud
CoreWeave Cloud provides several pre-Tensorized models for free. So if you’re eager to start using Tensorizer to speed up model load times and reduce resource usage, you can begin today. 
Pre-built Tensorized models include:
- EleutherAI/gpt-neo
- EleutherAI/gpt-j-6B
- EleutherAI/gpt-neox-20b
- EleutherAI/pythia
- KoboldAI/fairseq-dense
- Salesforce/codegen
See all available pre-Tensorized models in the GitHub ReadMe file, and learn more about Tensorizer in our documentation. 
If you’re looking to serve inference from LLMs, you need a solution that can scale quickly and cost-effectively. CoreWeave Inference Service offers a streamlined way to run inference that improves performance and minimizes latency while being more cost-effective than other platforms. Talk with our team today to learn more about CoreWeave Tensorizer or how you can serve inference better. 

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
