# CoreWeave ranks as #1 AI Cloud, Backed by SemiAnalysis’s Platinum ClusterMAX™ Rating

Source: https://www.coreweave.com/blog/coreweave-ranks-as-1-ai-cloud-backed-by-semianalysiss-platinum-clustermax-tm-rating

Announcement

Webinar

Podcast

GTC 2026

CoreWeave Forge is here: connect your AI loop and compound every improvement. Read more

Contact us

We are proud that CoreWeave, the AI Hyperscaler™, was the only AI cloud provider to receive the highest Platinum rating based on SemiAnalysis’s ClusterMAX™ Rating System. 
ClusterMAX™ evaluated dozens of providers including AWS, GCP, Azure, Crusoe, Nebius, and Lambda, and rated them from the perspective of an average reasonable customer. 
The ClusterMAX™ Platinum rating represents providers that are raising the industry bar and according to SemiAnalysis, there is only one AI cloud, CoreWeave, that provides services at the Platinum tier.
SemiAnalysis also recognized that CoreWeave’s cloud platform, purpose-built for AI, demonstrated industry leadership in operating large-scale 10k+ H100 clusters reliably.
CoreWeave’s unmatched performance and scalability are why leading AI labs including OpenAI, Mistral, Cohere and enterprises including IBM and JaneStreet choose CoreWeave for their AI workloads. The CoreWeave Cloud Platform is purpose-built—from metal to model—to deliver maximum performance and efficiency for AI workloads. We’ve led the way with a series of industry firsts—from early access to NVIDIA GB200, H100 and H200 GPUs, to achieving record-breaking AI inference performance with MLPerf 5.0 benchmarks using NVIDIA Grace Blackwell Superchips. Performance optimizations are integrated across every layer—from infrastructure to managed Kubernetes and application services such as CoreWeave Kubernetes Service and Slurm on Kubernetes (SUNK) —delivering 20% Higher GPU Cluster Performance than alternative solutions. Our Mission Control platform enables rapid deployment of the latest hardware, and our focus on reliability means 50% fewer interruptions and higher system goodput (96% vs. 90% industry average). With CoreWeave, customers get industry leading reliability, scale, and infrastructure efficiency for AI workloads — and everything is included in the price, with no hidden fees or surprise support costs. 
“CoreWeave’s product offerings set a new standard across the GPU cloud industry. Their industry-leading cluster burn-in and automated node lifecycle controller proactively run both passive and active health checks to catch unhealthy nodes and identifies issues such as Link flaps, convergence issues, silent data corruptions (SDC), etc. As demand for high-performance compute continues to grow, CoreWeave’s investments in software and hardware infrastructure makes them a clear leader in GPU cloud reliability." — Dylan Patel, Chief Analyst, SemiAnalysis
In this blog, we summarize the methodology and findings from the report, and also go deeper into how we build and operate CoreWeave Cloud Platform to deliver industry leading performance and reliability. 

## ClusterMAX™ rating system by SemiAnalysis - Methodology
Over the last 12 months, SemiAnalysis independently tested and/or collected customer feedback from dozens of cloud providers they view as ready for customers for AI workloads and created the GPU Cloud ClusterMAX™ Rating System, or ClusterMAX™ for short. SemiAnalysis performed extensive benchmarking and profiling to represent customer needs. They also attempted to scale workloads from single nodes to thousands of GPUs to arrive at their results and evaluated providers across multiple dimensions including security, performance, reliability, technical expertise, operational posture etc. Upon completion of their assessment, SemiAnalysis rated cloud providers across 5 tiers (from highest to lowest): Platinum, Gold, Silver, Bronze, and UnderPerform. 
CoreWeave’s rating of ClusterMAX™ Platinum tier represents the highest rating in the industry, and currently CoreWeave is the only AI cloud that is “raising the industry bar and qualifies for ClusterMAX™ Platinum”, according to SemiAnalysis. “Providers in this category consistently excel across evaluation criteria, including security, price for value, technical expertise, reliability backed by clearly defined SLAs, seamless managed Slurm/Kubernetes offering, and best in class NCCL/RCCL networking performance. Platinum-tier providers are proactive, innovative, and maintain an active feedback loop with the community to continually raise the bar.” 
SemiAnalysis concluded in their report that “CoreWeave is clearly leading in providing the best GPU cloud experience and has very high goodput and are entrusted to manage the large-scale GPU infrastructure for AGI labs like OpenAI, high frequency trading firms like Jane Street, and even NVIDIA’s internal clusters. ‍”
The ClusterMAX™ Rating System and content within the SemiAnalysis report were prepared independently by SemiAnalysis. No part of SemiAnalysis’s compensation by SemiAnalysis's clients was, is, or will be directly or indirectly related to the specific tiering, ratings or comments expressed in SemiAnalysis's article. The full report from SemiAnalysis is published here. 
In the following sections, we cover the assessment criteria used by SemiAnalysis and provide an in-depth view into how CoreWeave achieves industry leadership .

## Deep dive into CoreWeave’s results and differentiation
CoreWeave’s Cloud Platform is an integrated solution that is purpose-built for running AI workloads such as model training and inference at superior performance and efficiency. It includes Infrastructure Services, Managed Software Services, and Application Software Services, all of which are augmented by our Mission Control and Observability software. Our proprietary software enables the provisioning of infrastructure, the orchestration of workloads, and the monitoring of our customers’ training and inference environments to enable high availability and minimize downtime. 
CoreWeave has consistently been first to deploy the latest GPU technologies and make them available at scale for some of the world’s leading and most discerning AI labs and AI enterprises. Our team understands the complex requirements of running supercomputers efficiently to extract maximum performance, automate operations, and optimize total cost of management for the most compute intensive AI workloads. This data, which is only used internally to improve our services for our customers, is a critical input into our engineering process and strengthens our technological differentiation as we continue to push the boundaries of what is possible in computing. This “economy of AI leadership” ensures we can continuously improve our CoreWeave Cloud Platform over time in a positive feedback loop, by enabling us to learn from any issues or misconfigurations detected across our large infrastructure base. We apply those learnings to all our clusters, which in turn positions us as a leading-edge provider of choice for new customers.

Let’s deep dive into why CoreWeave is rated the highest AI cloud provider based on a few dimensions covered in the ClusterMAX™ ratings and how we enable these results for our customers. 

#### 1. Security, Reliability, and SLAs 
‍Security is paramount for leading AI labs and enterprises while training and deploying foundation models. The development and use of these models drives direct business impact and may require handling of sensitive customer data, as well as adherence to various security standards. CoreWeave implements top-tier industry best practices and standards to prioritize security and privacy every step of the way. We leverage advanced security capabilities such as Extended Detection and Response (XDR) and Data Loss Prevention (DLP), adhere to industry leading security standards such as SOC2 and ISO 27001, and employ our in-house information security teams to ensure that our customers operate in a secure environment.
CoreWeave Kubernetes Service (CKS) offers robust node isolation—where every node is single-tenant, providing advanced security and complete operational isolation for your data. CoreWeave’s architecture, which relies on “bare metal” instances running CKS, mitigates container escape vulnerabilities that would otherwise allow an attacker to escape a container and escalate to another tenant’s host within the Kubernetes cluster, a common risk with traditional hypervisor based approach. CoreWeave cloud offers encryption, identity management solutions, tenant networking isolation on both the Ethernet and InfiniBand network, Virtual Private Cloud (VPC) and Direct Connect networking to secure workloads, in addition to proactive monitoring and patching of security vulnerabilities (CVEs). CoreWeave storage solutions follow industry best practices for security including encryption of data at rest and in transit, identity management, authentication, and policies with role based access. For customers with sensitive data and security needs, CoreWeave also offers dedicated data center deployments which provide the highest level of physical infrastructure, network, storage, and workload isolation. 
The SemiAnalysis report also noted that CoreWeave was among the few providers who offer tenant level isolation using NVIDIA Bluefield Data Processing Units (DPUs) which SemiAnalysis explains is a characteristic of only the most advanced GPU operators. DPUs optimize compute for AI workloads by offloading networking, security, and storage management tasks from GPUs and CPUs. They are a critical enabling component for increasing overall efficiency and performance. Nimbus is our control and data-plane software running on our DPUs inside our Bare Metal instances, performing the typical role of a hypervisor in enabling security, flexibility and performance. Nimbus-enabled DPUs remove the need for a virtualization layer and give customers the flexibility to run directly on our servers without a hypervisor, enabling greater compute performance. Nimbus also provides security through the isolation of customer models and data encryption, while enabling them to set up VPC environments.
CoreWeave applies the same high standards of software and hardware security to our physical data centers as well. All of CoreWeave's data centers are limited-access buildings, with no visible CoreWeave signage. All data centers are protected by security personnel, 24 hours a day, 7 days a week, 365 days a year. Even data center employees cannot gain access to our data centers without biometric identification. All infrastructure hardware is contained within locked and secured cabinets, with cameras positioned at each cage, aisle, and door access point. This defense-in-depth approach ensures the utmost level of data privacy for our customers.
Our strong security posture has enabled high-frequency trading companies, such as Jane Street to adopt CoreWeave. The SemiAnalysis report noted that typically customers in this space have the strictest security requirements, as they deal with proprietary data and algorithms, which are the secret sauce to how they generate profits. 

#### 2. Lifecycle and Technical Expertise, Automated Active and Passive Health Checks 
‍The SemiAnalysis report evaluated the technical expertise offered across various phases (e.g., sales, preparatory, onboarding, main working, and offboarding). In addition, the ClusterMAX™ rating looked at timely delivery of infrastructure, infrastructure readiness with proper burn-in tests and acceptance tests, failure rates of infrastructure and recovery times, and overall reliability improving consistency and maximizing performance. At CoreWeave, we support customers through each of these stages, burn-in, delivery, and recovery/reliability, by providing hands-on partnership with technical experts and automated solutions for infrastructure lifecycle management to maximize performance of AI workloads. Our purpose-built technology stack is augmented by our lifecycle management and monitoring software, Mission Control, and our advanced cluster validation, proactive health checking capabilities, and observability capabilities. 
CoreWeave’s cloud platform is highly performant from Day1. We perform automated provisioning and node validation that remove the need for manual burn-in testing. This makes it possible for customers to immediately schedule and run training and inference jobs instead of investing significant time and resources in stress-testing compute nodes and verifying their health. CKS helps to ensure workloads of any type can be immediately scheduled on the infrastructure, while Mission Control automatically vets all the infrastructure to ensure on an ongoing basis that any faults are proactively detected and remediated. This shifts the burden of infrastructure management away from customers, significantly reducing costs and accelerating their time to solution.

CoreWeave Fleet Lifecycle Controller performs rigorous AI infrastructure validation from initial deployment through the entire node and cluster lifecycle. It runs a series of proprietary tests to validate node and network health and performance—along with sophisticated end-to-end testing for the entire cluster before bringing capacity into the production fleet. The SemiAnalysis report noted CoreWeave’s full burn-in test and full cluster InfiniBand network high-temperature burn-in with NCCL-tests and ib_write_bw. Not only does our testing identify nodes that do not meet performance expectations but also detects silent data corruptions, and proactively removes them from operations to optimize overall cluster performance. This means that customers’ clusters are ready to be used at scale, as soon as they go live, and continue to remain healthy. 
In addition, CoreWeave Mission Control provides advanced cluster validation, health monitoring, proactive node replacement, and deep observability to deliver and maintain vetted cloud infrastructure and provide observability into the health and performance of the entire solution. We perform several checks to identify PCIe errors, GPUs falling off the bus, Ethernet and InfiniBand events such as Link Flaps, Thermals such as GPU temperature, and GPU and CPU Memory statistics such as ECC error rate, to name a few. In addition to passive health checks, we automatically schedule active health checks to run on idle GPUs to do a full set of active testing to verify nodes are healthy on a constant basis. 
These capabilities help ensure your workloads run on healthy infrastructure, significantly reducing the likelihood of disruptions. We consistently observe 50% fewer job interruptions when running GPU clusters of over 1K+ nodes. By minimizing interruptions and recovering faster, we can help clients achieve a goodput rate as high as 96% versus industry average of 90%. Lower interruptions, faster recovery and higher goodput ultimately result in faster training times and several millions of dollars in saved costs. 
SemiAnalysis’s assessment validated the smooth onboarding experience on CoreWeave and the technical expertise of CoreWeave teams (engineers and solution architects), as well as summarized the benefits of our automated lifecycle management solutions “What we find amazing about CoreWeave is that they provide an automated, managed solution that abstracts away all the tasks that an ML engineer or scientist ideally doesn’t want to do.” 

#### 3. Slurm and Kubernetes 
‍The SemiAnalysis report stated that 90% of customers prefer Kubernetes for inference workloads, and about 50% of the customers use Slurm for training. It also notes that the effectiveness and reliability of CoreWeave’s managed Slurm and Kubernetes (CKS) help increase goodput and increase time to value for customers. 
CoreWeave Kubernetes Service (CKS) is a managed Kubernetes solution designed specifically for building, training, and deploying AI applications with cutting-edge performance, scalability, and efficiency. By running directly on bare metal servers without the overhead of a hypervisor, CKS maximizes resource utilization and minimizes latency. CKS offloads networking, security, and storage tasks to a Data Processing Unit to allow compute nodes to focus entirely on application workloads for maximum efficiency. CKS also provides pre-installed Container Storage Interface (CSI) and Container Network Interface (CNI) to simplify integration with  storage and networking so customers can successfully run their AI workloads on clusters of tens of thousands of GPUs on Day1. 
CoreWeave SUNK ("Slurm on Kubernetes") integrates Slurm, a popular workload manager for HPC and AI, with Kubernetes. This integration eliminates the need to maintain separate infrastructure for Slurm and Kubernetes workloads, leading to greater efficiency and better utilization of resources. SUNK helps large organizations accelerate innovation by supporting a high volume of isolated, customizable user environments, seamlessly integrating with existing identity providers, and enabling both inference and training workloads within a single cluster. 
CoreWeave supports the largest scale of AI model training with 100K+ GPU clusters and achieves higher Model FLOPs Utilization (MFU) for training workloads through topology-aware scheduling, including optimizations for scheduling on NVIDIA GB200 NVL72 systems. The SemiAnalysis report also highlights that CoreWeave’s Slurm and Kubernetes offerings set up NVIDIA HPC-X modules or Slurm MPI integrations, offer topology-aware resource allocation to optimize job performance and fully exploit the speed of the InfiniBand fabric for node-to-node communication, and NVIDIA pyxis plugins for ease of use - meeting the core needs of customers.

#### 4. Storage 
Efficient and performant storage solutions including managed object storage options are essential for machine learning workloads, both for training and inference. The SemiAnalysis report notes that during training, large quantities of data must be quickly and reliably accessed to feed GPUs without bottlenecks. This means that high-performance and AI optimized storage is needed for model checkpoint loads and saves such that GPUs can maximize Model FLOPS Utilization (MFU) and thereby significantly accelerate training time.
CoreWeave AI Object Storage, is an exabyte-scale, S3-compatible managed object storage platform purpose-built for AI training and inference at scale. Traditional object storage systems often create bottlenecks in data-intensive AI workflows. In contrast, AI Object Storage eliminates these challenges, providing the performance required to maximize GPU utilization while simplifying operations. Designed to integrate seamlessly with CoreWeave's NVIDIA GPU compute clusters, it supports performance levels up to 2 GB/s per GPU, scales effortlessly to hundreds of thousands of GPUs, and supports encryption of data at rest and in transit. With its unique Local Object Transport Accelerator (LOTA™), CoreWeave AI Object Storage caches frequently used datasets and/or prestages data directly on the local NVMe disks of GPU nodes, reducing network latency and dramatically improving training speeds. This caching technology is also integrated in CKS and can operate seamlessly without requiring additional tools or complex configurations, allowing AI teams to focus on building and refining their models.  AI Object Storage helps reduce model training time and overall costs, and increases iteration and innovation cycles. Moreover, customers only pay for storage costs and there are no egress or per-request fees. CoreWeave also offers Distributed File Storage and Dedicated Storage products, solutions that are designed to provide performant, scalable storage for AI workloads.
In addition, CoreWeave Tensorizer delivers secure, industry-leading model loading performance, enabling asynchronous checkpointing and virtually eliminating any impact of checkpointing on Model FLOPS Utilization (MFU). CoreWeave provides always up-to-date container images, built with performance-tuned libraries like NCCL, HPC-X, and cuDNN, along with optimization flags tailored to our platform—ensuring customer workloads run at peak performance across the entire stack. As a result, customers see MFU exceeding 50% on CoreWeave, driving up to 20% higher performance than public foundation model training benchmarks, which typically range from 35% to 45%. 

#### 5. NCCL/RCCL Networking Performance 
‍The SemiAnalysis report notes that when selecting GPU cloud services, thorough validation of NCCL/RCCL networking performance is vital for maximizing training and inference performance. After completing a set of networking NCCL/RCCL benchmarks from 128 GPUs to 1024 GPUs, SemiAnalysis concluded that InfiniBand still performs the best, especially when enabling Scalable Hierarchical Aggregation and Reduction Protocol (SHARP) in-network reductions. It also noted that CoreWeave was one of only 3 cloud providers in the ClusterMAX™ rating that have correctly set up SHARP on InfiniBand. 
CoreWeave’s best-in-class networking performance is the result of our relationship with NVIDIA to design a networking architecture that is purpose-built for AI clusters. The NVIDIA InfiniBand networks that we deploy using the Quantum InfiniBand switches are some of the largest in existence, with up to 3,200Gbps of rail-optimized and non-blocking GPU interconnect between nodes, and up to 32 nodes in a single pod. We built our InfiniBand networks to be non-blocking such that all GPUs can communicate with each other simultaneously and at full bandwidth. 
Our rail-optimized design with large rail pods means that there is less hop between GPUs that need to frequently communicate with each other in collective operations. We also built a number of inhouse tools to monitor the health of our InfiniBand networks and to respond to link flaps and bit errors, not only in a timely manner, but in a way that is contextually aware of the performance impact of a given InfiniBand link in the rail group, the SuperPOD and the overall fabric. All of these result in an industry-leading effective networking throughput to accelerate time to train and serve models. Our InfiniBand networks are also among the few with SHARP enabled, which boosts network performance by offloading collective operations from the Streaming Multiprocessors of the GPUs to the InfiniBand switch ASICs. 
CoreWeave’s Blackwell deployments will further be supported by external NVLink Switches, a low latency, scalable, and energy-efficient protocol that allows GPUs to communicate with other GPUs and CPUs within the same and different systems more efficiently. These technologies enable us to offer our customers access to tens of thousands of GPUs connected in a single cluster, and the ability to create massive megaclusters. 

#### 6. Monitoring 
CoreWeave’s observability solutions empower customers to monitor, analyze, and optimize their ML workloads with unparalleled transparency and efficiency. Faults can occur for various reasons, such as bad user configuration (memory allocation issues), misbehaving software updates, server component malfunctions, or issues in the high speed node-to-node network. By providing comprehensive insights into node and system-level metrics, CoreWeave enables faster time-to-resolution for issues and ensures sustained peak performance. 
Through managed Grafana and pre-built dashboards that visualize either the entire cluster or individual jobs, CoreWeave provides customers with total transparency into their infrastructure, down to the metal, such as Infiniband bandwidth, GPU temperature, and power consumption. CoreWeave overlays this infrastructure telemetry with visibility into Slurm job health and CKS cluster, together with real-time alerts. This level of observability is unique in-market and allows customers to troubleshoot and resolve issues faster and maximize the performance of their workloads on our platform. This deep level of telemetry data and actionable insights are available immediately for customers, with no extra configuration or setup, powered by CoreWeave’s massive scale metrics platform which ingests over 4000 metric samples/s per node across CoreWeave’s entire hardware and software stack.
SemiAnalysis highlighted CoreWeave’s detailed Grafana dashboards and deep observability suite, and summarized the benefits with this statement - “The monitoring, passive and automated schedule active health checks and out-of-the-box managed scheduler, all of this loop back into what an ML engineer/scientist wants, which is to focus on non-infra tasks and have a healthy set of verified nodes that is constantly scanned by passive health checks and automatically weekly scanned by active health checks. But an ML engineer/scientist also recognizes that sometimes things may break and broken nodes are not caught by the health checks and in those cases, they want FULL visibility into everything that is going on.” 

## Conclusion 
CoreWeave was the only AI cloud provider among dozens of cloud providers (including hyperscalers and neo clouds) to earn the highest ClusterMAX™ Platinum rating from SemiAnalysis. This indicates that CoreWeave is raising the bar across the industry and has demonstrated experience running large-scale 10K+ GPU clusters reliably. Leading AI labs and enterprises trust CoreWeave for their highly demanding AI workloads and realize industry leading performance. 
Whether you're building large language models, training cutting-edge multimodal systems, or optimizing inference pipelines, CoreWeave provides the foundation for AI-driven success. Contact us to get connected with our team of experts and experience our industry leading cloud platform.

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

CoreWeave Cloud,

Copy code

Copied!

CoreWeave Cloud,
