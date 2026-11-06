# Conductor on CoreWave: GPU rendering benchmarks | CoreWeave

Source: https://www.coreweave.com/blog/conductor-on-coreweave-rendering-benchmarks-for-gpu-and-cpu-instances

Announcement

Webinar

Podcast

GTC 2026

CoreWeave Forge is here: connect your AI loop and compound every improvement. Read more

Contact us

#### Conductor on CoreWeave Benchmarks: In Summary
- CoreWeave offers a broader range of more modern, performant NVIDIA GPUs than other major cloud providers, contributing to improved performance, faster runtime, and lower overall costs for rendering on Conductor. 
- GPU benchmarks: CoreWeave’s NVIDIA GPU-powered instances are consistently more performant than instances available from the other cloud providers on Conductor, resulting in significant cost and time savings for artists and studios.
- CPU benchmarks: CoreWeave CPU-only instances on Conductor are more cost-effective than comparable instances from the other cloud.
___________________________________________________________________________________________
Conductor customers can now access a broader, more powerful range of compute resources on CoreWeave for rendering visual effects (VFX), animation, motion graphics, and design projects, including for large-scale workloads requiring GPU acceleration.
How does this impact rendering on Conductor for artists from a time and cost perspective?
Earlier this summer, we ran some benchmarks to compare rendering on CoreWeave through Conductor versus rendering on one of the biggest worldwide cloud providers through Conductor. These tests ran on all currently available instance offerings for Conductor customers. The scene used is a very simple Universal Scene Description (USD) scene rendered with a significant amount of rays per pixel to lengthen the time taken to complete the task. 
Here’s a snapshot of what we tested:
Controls:
- Instance types for GPU workloads: Cinema4D/Redshift 3.5.14
- Instance types for CPU workloads: Cinema4D/Arnold 4.6.3.0
Tests (CoreWeave vs. other cloud provider):
- Runtime for on-demand GPU instances
- Job cost for on-demand and spot GPU instances
- Comparable GPU instances on a major cloud provider and CoreWeave
- CPU instances (runtime and job cost combined in one chart)
Before we dive into the benchmarks, let’s quickly compare CoreWeave vs. the other cloud provider so that you can better analyze the results.
‍

## Rendering on Conductor: CoreWeave vs. General Cloud Provider
There are a few fundamental differences between CoreWeave and this major cloud provider that help explain the large gaps in performance in the following benchmarks section.
CoreWeave features:
- More modern, performant GPU resources
- Consistent economical pricing
- Availability vs. spot instances
- Fast instance spin-up time

### Available GPU Resources
GPU instance types available on Conductor from CoreWeave leverage newer architecture from NVIDIA than those made available from the other cloud provider.

The key differences here are optionality and GPU types. With more GPU SKUs, CoreWeave helps you better match your workloads' compute needs with the available instance type, which can help you avoid overpaying for unused compute. Artists and studios using Conductor on CoreWeave will have access to the latest NVIDIA Ada Lovelace GPU architecture on demand,  including NVIDIA RTX A5000 cards. 
On the other hand, the other cloud provider offers NVIDIA T4 as the only GPU option for VFX and animation workloads. For some projects, T4 GPUs adequately support all the compute needs when available at scale. This “one-size-fits-all” approach can be a challenge for projects with greater rendering needs that demand T4 GPUs at scale in order to match the compute capabilities of the NVIDIA RTX GPUs.

### Pricing
CoreWeave offers economical pricing for compute resources on CoreWeave. The price does not fluctuate based on demand. CoreWeave also has no egress charges, so you can easily move data between regions or even cloud providers at no cost and with no long-term agreements.
The main differences in pricing tie back to the range of GPU SKUs offered. Since CoreWeave offers more GPU SKUs, you can use the right GPU configuration for your production needs without overpaying for unused compute. A limited selection of GPUs can be overkill for many artists, often resulting in overpaying for compute resources or waiting longer for renderings to finish on a lower-performant resource.

### Availability vs. Spot Instances
Spot instances are only available on the other cloud provider. Spot instances are spare computing resources offered by cloud service providers at significantly reduced prices compared to on-demand instances, but with the possibility of termination with short notice. 
While these instance types tend to be cheaper, you’re not guaranteed access to the compute resources for the duration your renders require. This means if your job takes 20 minutes to render, and someone else needs the compute at the 19th minute, you lose all the progress on your renders and have to start again. This results in unexpected costs that can negate the benefits of using spot instances in the first place. Spot instance types tend to be in high demand, and delays of minutes to hours should be factored in when choosing spot over on demand.
CoreWeave’s compute is generally priced at or lower than the other cloud provider’s spot equivalent, with a guarantee that your workload will complete without interruption. This way, you can be confident that your jobs will successfully render and can plan accordingly, without concern about resources being reallocated to higher-paying customers. 

### Instance Spin-Up Time
As the charts in the benchmark section will show, runtimes for CoreWeave instances are faster than comparable instances from the other cloud provider, which can in part be attributed to faster instance spin-up time, more responsive autoscaling, and containerization on CoreWeave.
Faster spin-up times on CoreWeave can be partly attributed to the underlying infrastructure. CoreWeave Cloud is a serverless Kubernetes platform, which means workloads run on bare metal; most generalized cloud or hyperscalers have a hypervisor layer that prevents 100% utilization of the server’s resources, without compromise. This means you get the most performance for your money and much faster instance spin-up times on CoreWeave than on the other cloud.
‍

## Benchmarks
We ran a total of 39 different instances, six for the other cloud and 33 for CoreWeave, each with different combinations of GPU types and the amount of GPUs, CPUs, and memory used.
The charts below illustrate cost and time comparisons for rendering on Conductor from CoreWeave vs. the other cloud provider. We’ll first look at overall cost and rendering time comparisons for a variety of GPU instance types. Then, we’ll take a look at two comparable instance types from CoreWeave and the general cloud to see a more apples-to-apples comparison. Finally, we’ll examine CPU-only instances.

### Runtime for All On-Demand GPU Instances

In the chart above, you see that all CoreWeave instances (blue) had a faster runtime (minutes) than all instances from the other cloud (gray). The fastest general cloud instance (g4dn.12xlarge: 31.43 minutes) required slightly more time than the slowest CoreWeave instance (cw-epycmilan-4-rtx4000-1: 29.5 minutes). TIP: Hover or click on a bar to see more details about each instance, including the number of GPUs, CPUs, and memory usage.

### Job Cost for All On-Demand & Spot GPU Instances

The first chart, Job cost (on-demand), compares the price to run on-demand instances on the general cloud provider against on-demand instances on CoreWeave. You can see that every CoreWeave on-demand instance costs less than the least expensive instance from the other cloud. Hover or click on a bar to see the exact price and more details.
The second chart, Job costs (spot on general cloud vs. CoreWeave on-demand), compared the price to run spot instances on a general cloud against on-demand instances on CoreWeave—again, CoreWeave doesn’t offer spot instances. Only two spot instances from the other cloud provider (g4dn.xlarge: $0.68; g4dn.2xlarge: $0.77) come in at a lower price than the most expensive CoreWeave instance (CoreWeave 22: $1.04). When factoring in the inherent risks of instance interruption with the other cloud’s spot instances, CoreWeave on-demand instances bring the best of both worlds to the table: affordable, reliable compute.

### Comparable GPU Instances: General Cloud vs. CoreWeave
For the reasons listed earlier in this blog post, comparing instances on the general cloud provider versus CoreWeave isn’t an exact science. However, there are some comparable instance types that we can take a closer look at that help illustrate the difference between two general cloud instances and two similar instances on CoreWeave.
TIP: Click on the legend—Runtime (minutes), Job cost (on-demand; $), and Job cost (spot, general cloud only; $)—to hide categories and view others in more detail.

The two charts above look at the runtime and job costs for two instance types that use only one GPU: g4dn.xlarge and cw-epycmilan-4-rtx4000-1. For two categories, runtime and on-demand job cost, CoreWeave outperforms the general cloud. A primary difference between the two instances is the GPU type used; the general cloud uses an NVIDIA T4, released in 2018, and CoreWeave uses an NVIDIA Quadro RTX 4000, released two months later. The CPU and memory allocation, which you can see by clicking or hovering over a bar, are the same. 

These two charts above are nearly the same as the last comparison, but these instances (g4dn.12xlarge and cw-epycmilan-4-rtx4000-4) used four GPUs instead of one. Here, CoreWeave outperforms the general cloud provider in both runtime and job costs. 
TIP: Click or hover over the bar charts to see the big discrepancies in CPU and memory usage. The other cloud’s instance, g4dn.12xlarge, required 48 CPUs and 192 RAM (memory) versus CoreWeave, cw-epycmilan-4-rtx4000-4, which only used four CPUs and 16GB RAM. While the general cloud strong-arms you into selecting predetermined CPU, memory, and GPU instance types, CoreWeave supports granular CPU, memory, and GPU selection to help you right-size your instances and pay only for the compute you need.
‍

### CPU-Only Instances on Conductor
We ran a total of 10 different CPU-only instances, five for the general cloud provider and five for CoreWeave, each instance including an increase in CPUs and memory. The charts below show CPU-only instances on Maxon’s Cinema4D on the general cloud with Intel Xeon Platinum 8000 and Intel Xeon v3  CPUs on CoreWeave. While the instances are not a clear 1-for-1 comparison, you can draw comparisons from the instances as shown.
Comparable general cloud and CoreWeave instances:
- m5.xlarge (general cloud) and cw-xeonv3-4 (CoreWeave)
- m5.2xlarge and cw-xeonv3-8
- m5.4xlarge and cw-xeonv3-16
- m5.8xlarge and cw-xeonv3-32
- m5.16xlarge and cw-xeonv3-64
TIP: Click on the legend—Runtime (minutes), Job cost (on-demand; $), and Job cost (spot, general cloud only; $)—to hide categories and view others in more detail.

The chart above shows runtime (in minutes), on-demand job cost, and spot job costs for all 10  instances. 
At first glance, it appears that the general cloud is the faster but less economical option. You can make that assumption when comparing similar instances for the general cloud and CoreWeave (listed above), which show that the job runs slightly faster on the other cloud but also at a higher cost. 
However, you’re not locked into a limited number of CPUs and memory. Let’s compare m5.xlarge (general cloud) versus cw-xeonv3-8 (CoreWeave). By switching to CoreWeave and jumping up by one instance type, you can actually render the same image in less time and at a lower cost.

‍

## Looking Ahead
At CoreWeave and Conductor, our engineering teams are consistently benchmarking to help clients find the best solutions for their compute needs, and we encourage clients to perform their own benchmarks, as well. 
By the end of this year, we aim to make CoreWeave’s premium compute AMD Epyc Milan CPU as well as  Intel Xeon v4 and Intel Xeon Scalable CPUs available to Conductor users, which will lead to even greater performance at a better price. 
However, as we continue to improve your experience on Conductor, we don’t want to rely solely on hardware upgrades for performance optimization. Our team is continually looking to build and integrate solutions that help studios directly manage the full cycle of cloud workflow requirements. This includes new features like upload optimization, storage performance, automated machine selection, and virtual wrangling to further automate post-submission shot orchestration. New product features, along with the significant performance improvements gained with CoreWeave’s compute capabilities, create an invaluable toolset for our studio customers to meet their deadlines.
‍

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

CoreWeave for Media & Entertainment,

Copy code

Copied!

CoreWeave for Media & Entertainment,
