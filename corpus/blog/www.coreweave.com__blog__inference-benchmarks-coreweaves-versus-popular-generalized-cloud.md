# Inference Benchmarks: CoreWeave’s Inference Solution 8 to 10x Faster Than a Popular Generalized Cloud

Source: https://www.coreweave.com/blog/inference-benchmarks-coreweaves-versus-popular-generalized-cloud

Announcement

Webinar

Podcast

GTC 2026

CoreWeave Forge is here: connect your AI loop and compound every improvement. Read more

Contact us

In Summary:
- The underlying infrastructure of your cloud provider can have a massive impact on performance, especially for serving inference and autoscaling.
- Our team ran several tests to benchmark how CoreWeave’s specialized infrastructure and autoscaling capabilities compare to a popular generalized cloud provider. 
- CoreWeave’s inference service has 3 - 5x faster container spin-up times on average and 8 - 10x faster performance compared to a major generalized cloud provider when tested using EleutherAI’s GPT-J-6B.
- Downloading a model from CoreWeave’s accelerated object storage network speed was 3 -5x faster than downloading the model from a generalized cloud’s storage solution in the same region; CoreWeave’s transfer speed has the ability to reach 12GB/s.
___________________________________________________________
When it comes to serving inference, performance, and speed are critical. Users of your product expect a model to respond in a reasonable amount of time. A slow inference solution means a bad experience, and it may be the last time that person uses your application.
Achieving a good customer experience can be especially difficult when your service sees large spikes in traffic. (You don’t want to be remembered as the app that crashed when a few thousand, or a million, people all tried to use it.) The problem: Not all inference solutions are built to handle large bursts of activity.
An AI inference solution needs to quickly scale up new instances in order to meet spikes in user demand. Depending on the cloud infrastructure you use, this process can take several minutes. While access to GPUs may be a factor, perhaps the biggest overlooked factor and a key driver for performance is the underlying infrastructure of your cloud provider.
To demonstrate the performance difference of specialized cloud infrastructure, we ran benchmarks to test inference autoscaling at CoreWeave versus one of the most popular generalized cloud providers.

## Inference Benchmarks
To demonstrate the power of CoreWeave’s inference service, we ran benchmarks comparing our service to a popular large cloud provider using EleutherAI’s GPT-J-6B as the model. The tests examined container spin-up time, networking speed, and overall latency for autoscaling, all of which impact performance for inference.
We chose GPT-J-6B as it’s a standard mid-sized model with 6B parameters, meaning it’s not too big or small that it fits on a broad range of GPUs.  It is also not image-based, which also helps make this appropriate to benchmark for LLM-based, machine learning inference.

### Container spin-up time
In this first chart (below), CoreWeave averaged ~30-45 seconds for container spin-up time while the generalized cloud averaged ~120-150 seconds. The results show a 3-5x performance improvement for container spin-up time on CoreWeave. 

### Transfer Speed from Object Storage
This second chart (below) compares the average transfer speed for downloading from the generalized cloud object storage versus CoreWeave’s compatible object storage in the same region. CoreWeave’s transfer speed averaged 700MB/s while the generalized cloud averaged 72MB/s.
In the chart below, the lower wall-clock times shows that CoreWeave’s average transfer speed was 3 - 5x faster. In some instances, CoreWeave’s transfer speed can go up to 12Gb/s.

### Container Spin-Up Time for Cluster Autoscaling + Pod Spin-Up
This last chart (below) takes a look at the full process for autoscaling an inference service when you need to spin up more pods. The overall average latency on CoreWeave was 45-70s (30-45s for container spin-up + 15-25s to load the model from accelerated object storage). For the generalized cloud, the average latency was between 270-390s (120-150s average container spin-up + 150-240s to load the model from accelerated object storage storage). 
These results show it is 8 - 10x faster to serve ML inference on CoreWeave than the generalized cloud.

## How Is CoreWeave’s Inference Service So Much Faster?
The results from these benchmarks demonstrate the staggering performance enhancements you get from specialized cloud infrastructure that’s designed for AI and ML workloads.

### CoreWeave’s Tech Stack vs. a Generalized Cloud Provider
The key differences between CoreWeave and the generalized cloud that impact performance come down to the underlying infrastructure. 
Most generalized cloud providers offer a managed cloud service (or “managed Kubernetes”) that uses a hypervisor, a program used to run and manage one or more virtual machines on a computer. The hypervisor (illustrated in the graphic below) is a helpful virtualization tool in that it schedules and manages virtual machines based on the allocated resources. However, because the hypervisor layer rests on top of the operating system, it cannot directly communicate with the hardware, which can lead to less efficiency and unoptimized performance.
‍

‍
On the right of the graphic (above), you see how CoreWeave built its tech stack around bare-metal compute. The Kubernetes layer sits almost directly on top of the hardware—only a lightweight OS system is required—which enables clients to efficiently deploy applications and scale up new pods without having to configure the underlying framework. We call this system serverless Kubernetes.
Here are some of the key differences between CoreWeave and a generalized cloud’s underlying architecture:
Traditional cloud infrastructure: 
- VMs host Kubernetes, which need to run through a hypervisor, slowing the inference process
- Difficult to scale
- Can take >5-10 min. to spin up new instances
CoreWeave’s tech stack:
- No hypervisor layer, so Kubernetes runs directly on bare metal (hardware) 
- Option to host virtual machines (VMs) inside of Kubernetes containers
- Easy to scale

### Pod Spin-Ups & Autoscaling 
In any inference solution, you will need to spin up pods to fulfill user requests. The ability to automate this process is essential, especially for use cases in which rapid responses are necessary. 
The process to spin up new pods is much different on a generalized cloud. First, you have to make sure you have enough quota for the compute you need. Many generalized clouds will have a maximum compute quota that you are allotted for the month or quarter; if you need to surpass that quota, you have to reach out to request access to more. This can be a very tedious, and unless you are a large company spending millions of dollars on compute, GPU allocation can be very restrictive and will require a lot of communication regarding your plans and budget for using GPUs.
The process to spin up new pods on a generalized cloud isn’t seamless. It can be very tedious and time-consuming to get access to more GPUs at scale—which doesn’t help you or your end-users get the real-time compute needed for spikes in demand. Without that access, the success of your product is capped by a limited amount of computing resources, the overall performance of your infrastructure will be strained during high-demand times, and the user experience will fall short.
If you have access to enough compute, then you can start the process of spinning up more pods. Typically, the Kubernetes control plane spins up a pod on top of a virtual machine. With a standard container concurrency of 1, each pod is assigned to a virtual machine, which causes further delays in additional virtual machines and pods to scale for bursts in traffic. These added layers and steps slow down the process of inference autoscaling, in which you need to scale pods up and down quickly to reflect demand.
In cases where there are many requests coming in while pods are spinning up, the activator for KNative may not be able to queue all those requests due to limits on the size of the buffer queue. In this case, some requests are dropped (also known as “timed out”), which creates a frustrating user experience.
At CoreWeave, the process to spin up new pods is more straightforward because the platform is built on bare metal (aka, you don’t need to launch a virtual machine in order to spin up more pods). You can autoscale across tens to thousands of GPUs on demand and scale back down when demand slows. CoreWeave also takes advantage of Tensorizer, an open-source tool that makes it extremely quick to load a PyTorch model from HTTP/HTTPS and S3 endpoints.
‍

## How This Impacts User Experience
These benchmarks show just how much of an impact the underlying infrastructure of your inference service can have on performance, which impacts user experience and price.
The first and most obvious impact is on the user experience. By leveraging specialized infrastructure built for AI and ML, you can quickly and more easily autoscale based on user demand. This means faster responses and better access to on-demand compute. 
Clouds that leverage general-purpose infrastructure are less suited to meet the complex demands of unpredictable inference workloads. Because the generalized cloud could timeout during cluster autoscaling and pod spin-ups, users are more at risk of being dropped during large spikes in usage. Overall, user experience will be significantly hampered when there are bursts of traffic, which can result in bad reviews, abandonment, and a mediocre ML product.
In addition, efficient autoscaling for inference can also mean a better price point for compute when you pay only for the compute you use. The ability to scale to zero during idle times can help you significantly reduce costs because you don’t need to keep GPUs running in order to avoid slow spin-up times. CoreWeave Cloud GPU instance pricing is highly flexible and meant to provide you with ultimate control over configuration and cost.
Whether you’re looking to serve inference at scale or simply want to ensure your application can handle large bursts of requests, you need an inference solution built for AI inference. CoreWeave’s inference service enables scalable ML with performance-adjusted costs, so you can autoscale with ease based on your user demand without overpaying for compute or leaving users with a slow experience.

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
