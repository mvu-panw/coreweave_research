# How to Serve Inference Faster with Infrastructure That Scales Securely | CoreWeave

Source: https://www.coreweave.com/blog/inference-deep-dive-how-to-serve-inference-faster-with-infrastructure-that-scales-securely-with-you

Announcement

Webinar

Podcast

GTC 2026

CoreWeave Forge is here: connect your AI loop and compound every improvement. Read more

Contact us

### Learn the common challenges around serving inference on the cloud, the infrastructure that optimizes performance, and why more companies are using CoreWeave Inference Service.
With AI permeating nearly every industry today, performance has never been more vital.  For an AI application to break through, it must deliver the experience users want and expect: faster, better inference.  
Inference is the process of using a trained machine learning (ML) model to make predictions, answer a query, or generate content. While it may not be as glamorous or buzzworthy as its counterpart, model training, effective inference plays a huge role in how users evaluate the quality of a model or application. Users have high expectations for the types of experience they want, and if your inference falls flat, they’ll quickly move on. 
However, many cloud platforms aren’t built to support the scale, access, and responsiveness required for serving inference today. These limitations force companies to choose between subpar performance or an expensive infrastructure bill—in many cases, leaving companies with both. All the while, models are expanding rapidly, compounding an already frustrating, industry-wide challenge.
Companies need an inference solution that can scale across multiple GPUs on demand—without breaking the bank. That’s where CoreWeave Inference Service comes in.
In this article, we’ll discuss the current challenges around serving inference, what CoreWeave Inference Service is, and how its tech stack is built specifically for companies to serve inference efficiently. Already using CoreWeave for inference? Read our documentation for more details on how to get started.

## Serving Inference in the Cloud Today
Efficient inference relies on fast spin-up times and responsive auto-scaling. Without it, end users may experience annoying latency, service interruptions or inaccurate responses and move on to a different application next time. That’s why it’s critical to leverage the right infrastructure that delivers fast and scalable AI in production to produce great experiences, even during demand spikes.

#### Challenges of Serving Inference
Many companies leverage cloud computing to deploy models that power applications via inference. Cloud computing gives you the ability to access the hardware you need, like NVIDIA Tensor Core GPUs, without having to manage the underlying infrastructure. Amazon Web Services, Google Cloud Platform, Microsoft Azure were among the first and largest cloud providers, providing compute solutions for a range of projects, from hosting a website to training an ML model.
However,  many cloud providers didn’t build their infrastructure to scale and optimize resources for these compute-intensive workloads—or when an application sees large spikes in users. Because of these spiky usage patterns, the traditional way of running inference in the cloud (let alone on premises) presents many challenges for companies leveraging these platforms.  
Common inference challenges include:
- High latency: Many of today's successful AI models are very large, which means serving inference can be slow. However, many applications of these models demand real-time performance and inference every second, such as autonomous navigation, critical material handling, and medical equipment.
- Lack of access to GPUs: Access to GPUs is the biggest bottleneck in the industry. ML models require a massive scale of high-performance compute resources, with larger models demanding even more resources to deploy. Even if a company reserves GPUs well in advance, they still might not have enough capacity to account for a spike in users or overspend on GPU access. 
- GPU options: NVIDIA GPUs are the gold standard for training models and inferencing on deployed models, and NVIDIA offers a wide range of GPUs. Companies benefit from having a variety of GPUs to choose from to ensure they’ve got the right tool for the job. 
- High infrastructure costs: When it comes to AI, infrastructure is often the biggest expense. Serving inference can be much more expensive than model training based on the scale of users and queries. A model might need to run millions of times for a popular product, such as ChatGPT, which was estimated to cost $40 million in the month of January alone.
- Limited interoperability: Engineers use frameworks like Tensorflow, Pytorch, JAX and Keras to develop ML models. When running inference, these different models need to work together and may need to run in diverse environments, such as on premises and in the cloud. If a cloud provider’s stack isn’t built for easy interoperability, the result can be a slow and challenging experience. 
- Difficult to scale: Traditional cloud computing infrastructure relies on legacy processes and software, like a hypervisor, rather than running on bare metal. This older design inhibits a company’s ability to optimize for speed and performance, so users have to wait a long time for the model to answer their query. 
- Lack of technical knowledge: Newer applications, software, and systems used for model training and deployment, like Kubernetes, have a steep learning curve. Companies often don’t have the in-house expertise to effectively manage and maintain everything.
- Crippling costs to access storage, API calls:  Many cloud providers charge small fees for data ingress and egress, as well as API calls. These functions are critical for serving inference, and the cost can climb quickly.

#### How the Generative AI Boom Exacerbates Cloud Computing
Since 2022, generative AI and machine learning have captured the mainstream spotlight. Companies are building and releasing new large language models (LLMs) to the public, and apps that leverage generative AI are flooding social feeds. As a result, more companies are investing millions of dollars to build and serve their own models. 
While this AI boom has helped accelerate progress in the industry, it also sharpens the challenges of serving inference today—especially around access to GPUs and infrastructure. Right now, it’s a race to build the infrastructure that can support the speed at which AI and machine learning are growing, and many cloud providers simply can’t keep up.
Meanwhile, LLMs have ballooned in size over the past year, with many of the well-known models totalling billions of parameters. Back in February 2022, Eleuther AI released its open source GPT-NeoX-20B, a 20 billion parameter LLM and the largest at that time. Fast forward to autumn of 2022, Big Science released its open source, autoregressive LLM,  BLOOM-176B, which contains 176 billion parameters. 
From the private sector, OpenAI made ChatGPT-3 (a 175 billion parameter model) accessible to the public for the first time; which was a massive increase from its six-billion parameter open-source version,  ChatGPT-J-6B. 
This growth is monumentous, but not without consequences. More parameters require more (or more high-performance) GPUs, and with that comes more costs. When a model expands past the number of parameters that can fit on a single GPU memory, teams serving inference must decide whether to increase the number of GPUs or upgrade to a larger, newer GPU. Either way, this can skyrocket the cost to serve inference at scale.  

#### What You Need to Solve These Challenges
As AI and machine learning continue to expand and evolve, demand for more GPUs and better infrastructure rises with it. Start-ups and enterprises alike will need reliable, flexible, and highly available cloud compute resources to fuel their growth.
Companies need an inference solution that meets their three criteria:
- Deliver high performance (high throughput and inference accuracy)
- Create great user experiences. Low latency and near real-time inference are critical here.
- Operate in a cost-effective way. Teams need an inference solution that optimizes hardware usage at a fair price, without any nickel-and-diming.
CoreWeave’s unique infrastructure offers a modern way to run inference that delivers better performance—the lowest latency and highest throughput—while being more cost-effective than other platforms.

## CoreWeave Inference Service: A solution that actually scales with you.
An optimized inference solution built for scale must do two things: fast spin-up times and responsive auto-scaling. Without it, high latency and inconsistent performance creates a poor user experience. 
But improving scale and performance is not as simple as the type of GPU you’re using—or the number of GPUs. That’s why it’s critical that the infrastructure you rely on leverages the right tools (systems, software, GPUs, etc.) that deliver fast and scalable AI in production. To every user. Every time.
This is what sets CoreWeave apart when it comes to inference. A specialized cloud provider built for GPU-accelerated workloads, CoreWeave provides unparalleled access to an extensive range of NVIDIA GPUs, available at scale and on demand. Companies on CoreWeave leverage compute solutions that are up to 35x faster and 80% less expensive than legacy cloud providers.

#### What Is CoreWeave Inference Service? 
CoreWeave Inference Service, a compute solution for companies serving inference in the cloud, offers a modern way to run inference that delivers better performance and minimal latency while being more cost-effective than other platforms. This solution enables teams to serve inference faster with infrastructure that actually scales with them.
The result: An inference solution that lets you autoscale from 0 to 1,000s of NVIDIA GPUs at scale and on demand, so you never get crushed by user growth.
At CoreWeave, we don’t try to fit your company into a box. We work with you to find the best GPUs for serving inference, networking, and storage solutions depending on your use case. Testing and benchmarking is also a big part of what we do to ensure you have the answers to your inference questions, from “Which GPUs have the lowest latency on Stable Diffusion?” to “How much can I reduce latency by using  NVIDIA Triton Inference Server software on CoreWeave Cloud?”
See how much companies have saved with CoreWeave Inference Service:
- NovelAI served requests 3x faster, resulting in a much enhanced user experience and significantly better performance-adjusted cost.
- NightCafe saw out of memory (OOM) errors down 100%, lag time down 80%, and costs down by as much as 60% since moving to CoreWeave.
- Tarteel AI leveraged Zeet to smoothly move its deployment from AWS to CoreWeave, translating to a 22% improvement in latency and ~56% cost reduction.
- AI Dungeon was able to cut spin-up time and inference latency by 50% and lower computing costs by 76% with a seamless migration to CoreWeave.
To understand how companies levering our inference solution achieved these results, let’s take a look at the underlying infrastructure.

#### Traditional Tech Stack: A Managed Cloud Service
Most cloud providers offer a managed cloud service or “managed Kubernetes.” This type of cloud architecture serves a wide range of legacy use cases and general hosting environments as well as AI model training and inference. Because this architecture was not designed for compute-intensive workloads, it can be very difficult or impossible to get the best performance and minimal latency out of the hardware. 
Disadvantages of traditional cloud infrastructure: 
- VMs host Kubernetes (K8s), which need to run through a hypervisor, slowing the inference process
- Difficult to scale
- Can take >5-10 min. to spin up instances
Many of the challenges to optimize for speed and performance revolve around the hypervisor, a program used to run and manage one or more virtual machines on a computer. It’s a helpful virtualization tool in that it schedules and manages virtual machines based on the allocated resources. However, because the hypervisor rests on top of the operating system (as shown in the graphic above), it cannot directly communicate with the hardware,which can lead to less efficiency.
Key Takeaway: Traditional architecture that leverages a hypervisor can get the job done but is less efficient and can’t take advantage of bare-metal performance.

#### CoreWeave’s Tech Stack: Serverless Kubernetes in the Cloud
At CoreWeave, we built things a bit differently than cloud architecture that uses traditional hyperscalers. A typical company that uses CoreWeave Cloud will consume hundreds or tens of thousands of GPUs, and they need to be able to scale up and down at rapid speed. Our tech stack is optimized for that, taking full advantage of the maximum performance of the hardware and systems.
Advantages of CoreWeave’s tech stack:
- No hypervisor layer, so Kubernetes runs directly on bare metal (hardware) 
- Option to host virtual machines (VMs) inside of Kubernetes containers
- Easy to scale
We built our tech stack around bare-metal compute because we believe it’s the truest way to get the highest performance from these very sophisticated devices. 
On top of our bare-metal compute, we layer Kubernetes in what we call serverless Kubernetes. This allows customers to deploy their applications without having to worry about cluster autoscaling, idle version machines, and more. We handle that in the background and can scale up a new Kubernetes pod in ten seconds. All this is made possible by KServe, an open-source tool that provides an easy to use interface via Kubernetes resource definitions for deploying models without the fuss of correctly configuring the underlying framework (i.e., Tensorflow).
On top of our serverless Kubernetes system, we’ve layered a couple more open-source tools that we built together and modified specifically for different scenarios and models, like LLMs. Knative, an open-source tool, is a core component in our infrastructure tech stack. This tool allows us to support features like Scale-to-Zero for models that are not consistently used, so these models incur zero usage and zero costs. We also leverage Kubevirt to host virtual machines inside of Kubernetes containers.
Key Takeaway: CoreWeave Inference Service runs on bare-metal, serverless Kubernetes, so you can access GPUs by deploying containerized workloads via Kubernetes for increased portability, less complexity, and overall lower costs.

## Why use CoreWeave Inference Service?
We’ve covered our underlying tech stack and how that compares to other cloud providers. Now let’s talk about the tangible benefits that it gives you—from performance enhancements to cost-benefits. 
Here’s how we maximize inference speed and performance while minimizing resource usage.
- Access GPUs on demand. CoreWeave delivers a massive scale of highly available NVIDIA GPU resources to your fingertips, including the NVIDIA HGX H100 platform.
- Deploy inference with a single YAML. We support all popular ML frameworks: TensorFlow, PyTorch, JAX, SKLearn, TensorRt, ONNX, and custom serving implementations. 
- Autoscale without breaking the bank. CoreWeave's infrastructure automatically scales capacity up and down as demand changes.
- Scale to zero. Inference Services with long periods of idle time can automatically scale to zero, consuming neither resources nor incurring billing. 
- Easy installation and deployment. Run applications directly on the OS without needing additional library installations.
- Spin up new instances faster.  As soon as a new request comes in, requests can be served as quickly as 5 seconds for small models and 30-60 seconds for larger models. 

#### Enabling More Responsive Auto-Scaling
Auto-scaling is enabled by default for all applications on CoreWeave Inference Service. Autoscaling parameters are pre-configured for GPU-based workloads that leverage large datasets. 
Engineers can autoscale containers based on demand to quickly fulfill user requests. How fast? For some ball-park measurements, requests can be served as quickly as five seconds for small models, 10 seconds for GPT-J, 15 seconds for NeoX in 15, and 30-60 seconds for larger models.
You can also control scaling in the InferenceService configuration. Increasing the number of maxReplicas will allow the CoreWeave Cloud to automatically scale up replicas when there are multiple outstanding requests to your endpoints and scale down replicas automatically as demand decreases. You can also achieve Scale-to-Zero by setting minReplicas to 0. This will completely scale down the InferenceService when there are no requests for a period of time, during which you incur no hardware usage and no costs.

#### Networking and Storage for Inference
Two important but often overlooked elements of cloud computing are networking and storage. For high-performance use cases like inference, connectivity between compute hardware as well as storage play a major role in overall system performance.
CoreWeave Cloud Native Networking (CCNN) fabric offers ultramodern, high-performance networking out-of-the-box. CoreWeave's Kubernetes-native network design moves functionality into the network fabric, so you get the function, speed, and security you need without having to manage IPs and VLANs.  This allows you to:
- More effectively send data between endpoints,
- Deploy Load Balancer services with ease
- Access the public internet via multiple global Tier 1 providers at up to 100 Gbps per node
You can also get custom configuration with CoreWeave Virtual Private Cloud (VPC). This networking solution is very different from CCNN in that networking policies and Kubernetes load balancing are not present in order to give you more control. VPC was built for specific use cases,such as specific firewall or routing requirements that can not be achieved any other way.
High-performance, network-attached storage volumes are critical for containerized workloads and virtual servers. We designed storage solutions that are easy to provision and manage separately from compute, so you can:
- Realize storage volumes at any time
- Create storage volumes as Block Volumes or Shared File System Volumes
- Seamlessly move between instances and hardware types 
With CoreWeave, you can easily access and scale storage capacity with solutions designed for your workloads, including Block, Shared File System, and Object Storage volumes. We built our storage volumes on top of Ceph, an open-source software built to support scalability for enterprises. This allows for easy serving of machine learning models, sourced from a range of storage backends, including S3 compatible object storage, HTTP and a CoreWeave Storage Volume.

#### Seamless integrations for inference
CoreWeave Inference Service allows users to leverage other tools and software that can enhance performance. Here’s a list of popular tools that help make it easier, faster, and more cost-effective to serve inference from CoreWeave Cloud:
- NVIDIA Triton Inference Server software helps standardize model deployment and execution to deliver fast and scalable AI in production.    
- CoreWeave's Tensorizer: a module, model, and tensor serializer and deserializer that makes it possible to load models in less than five seconds, making it easier, more flexible, and more cost-efficient to serve models at scale. 
- One-click models: Deploy popular open-source machine learning models with one click.
- Zeet: shortcut to rolling out production-ready cloud services, operated by DevOps, and delivering a self-service developer experience for your engineering organization.

## Get Started with Inference on CoreWeave Cloud  
Never choose between price and performance again. Serving inference is essential to your business’ success, so you should never have to compromise.
With CoreWeave, you can choose from a wide selection of GPUs to ensure your compute resources match the complexity of your workloads. Leverage cloud architecture built for faster spin-up times and more responsive autoscaling. And, save costs on serving inference with increased performance, highly configurable instances, and resource-based pricing.
Talk with an expert today to learn how you can take the next step toward success with CoreWeave Inference Service. 

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
