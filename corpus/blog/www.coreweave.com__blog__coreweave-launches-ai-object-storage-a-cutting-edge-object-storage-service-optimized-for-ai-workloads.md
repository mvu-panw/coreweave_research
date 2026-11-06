# CoreWeave Launches AI Object Storage: Optimized for AI Workloads | CoreWeave

Source: https://www.coreweave.com/blog/coreweave-launches-ai-object-storage-a-cutting-edge-object-storage-service-optimized-for-ai-workloads

Announcement

Webinar

Podcast

GTC 2026

CoreWeave Forge is here: connect your AI loop and compound every improvement. Read more

Contact us

The world of AI is evolving rapidly, and the need for performance-optimized, scalable, and secure storage solutions has never been greater. Today, at NVIDIA GTC, CoreWeave, the AI Hyperscaler®, proudly announces the General Availability (GA) of CoreWeave AI Object Storage—a managed object storage service purpose-built for AI training and inference at scale. AI Object Storage adds to an existing storage product lineup, including CoreWeave’s Distributed File Storage and Dedicated Storage products, solutions that are designed to provide performant, scalable storage for AI workloads.
As AI models grow in size and complexity, traditional cloud storage solutions fall short of the performance demands required to fuel innovation. AI Object Storage was engineered from the ground up to meet these challenges, enabling organizations to accelerate their AI workloads with unprecedented speed and efficiency.

## Built for AI from the Ground Up
AI Object Storage delivers exabyte-scale, S3-compatible storage tailored for GPU-intensive AI model training. Designed to integrate seamlessly with CoreWeave's NVIDIA GPU compute clusters, it supports performance levels up to 2 GB/s per GPU and scales effortlessly to hundreds of thousands of GPUs. With its unique Local Object Transport Accelerator (LOTA™), AI Object Storage caches frequently used datasets and/or prestages data directly on the local NVMe disks of GPU nodes, reducing network latency and dramatically improving training speeds.
Traditional object storage systems often create bottlenecks in data-intensive AI workflows. In contrast, AI Object Storage eliminates these challenges, providing the performance required to maximize GPU utilization while simplifying operations. Its caching technology can operate seamlessly without requiring additional tools or complex configurations, allowing AI teams to focus on building and refining their models.
‍
Data flow from the customer through CoreWeave AI Object Storage and LOTA to the Compute nodes

## Key Benefits
- Blazing Fast Performance: Up to 2 GB/s per GPU, enabling faster training and inference cycles.
- Unmatched Scalability: Trillions of objects, exabytes of data, and performance that grows with your storage needs.
- Optimized for NVIDIA GPUs: Fully supports the latest NVIDIA GPU architectures, including Blackwell and Hopper.
- Simple and Flexible Pricing: No egress, per-request, or hidden fees—pay only for the storage you use.
- Enterprise-Grade Security: Encryption at rest and in transit, with role-based access control, audit logging, and lifecycle policies.

## Streamlined Deployment Across the CoreWeave Ecosystem
AI Object Storage is designed for effortless integration within the CoreWeave Cloud ecosystem, enabling a streamlined experience for AI and ML workloads. It supports CoreWeave Cloud’s SAML/SSO authentication for seamless user management, ensuring secure access and simplified identity federation. A managed Grafana dashboard—available directly from the CoreWeave Console—provides real-time insights into requests per second, bandwidth usage, and response durations, helping teams monitor performance and optimize workloads. 
LOTA is seamlessly integrated with CoreWeave’s Kubernetes Service (CKS), allowing for tight integration between CKS applications and LOTA’s high-performance caching capabilities. Developers can also manage their storage infrastructure using the CoreWeave Terraform provider, enabling automation, infrastructure-as-code workflows, and rapid deployment of storage resources alongside GPU compute clusters. With deep integration into CoreWeave’s high-performance AI infrastructure, users can efficiently orchestrate and scale their workloads without added complexity.
CoreWeave AI Object Storage also includes built-in observability data via managed Grafana dashboards, providing valuable insights about the product’s performance. An example of one of the dashboards is shown below. This dashboard includes insights on requests per second, throughput, and request duration. Data can be dynamically grouped or filtered by bucket, region, operation type, or response code, allowing for deeper analysis and troubleshooting. With these insights, users can better understand usage patterns, identify potential issues, and ensure optimal performance of their AI-driven workloads.
Sample view of the managed Grafana Dashboard

## Our AI Infrastructure
Each part of our stack, including CoreWeave AI Object Storage, is purpose-built for AI use cases. Learn how we've designed the elements of our infrastructure to unlock up to 20% higher GPU performance.

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

CoreWeave AI Object Storage,

Copy code

Copied!

CoreWeave AI Object Storage,
