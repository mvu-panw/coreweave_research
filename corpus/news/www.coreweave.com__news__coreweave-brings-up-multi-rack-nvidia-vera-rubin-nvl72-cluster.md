# CoreWeave Brings Up Multi-Rack Vera Rubin Cluster

Source: https://www.coreweave.com/news/coreweave-brings-up-multi-rack-nvidia-vera-rubin-nvl72-cluster

Announcement

Webinar

Podcast

GTC 2026

CoreWeave Forge is here: connect your AI loop and compound every improvement. Read more

Contact us

LIVINGSTON, N.J. — September 16, 2026 — CoreWeave, Inc. (Nasdaq: CRWV), The Essential Cloud for AI™, today announced the bring up of multi-rack NVIDIA Vera Rubin NVL72 on CoreWeave Cloud, putting hundreds of NVIDIA Rubin GPUs into a single scale-out cluster for agentic AI. The company also announced two new capabilities in CoreWeave AI Object Storage, cross-region write acceleration and a new Archive tier, that keep the data those workloads depend on close to the GPUs. 
Multi-rack Vera Rubin NVL72 clusters allow for training and inference jobs to run across hundreds of Rubin GPUs. That matters for multi-step agentic workloads, which are sensitive to data-access latency because delays can compound across repeated model calls and tool use. Cross-region write acceleration removes the wait even when working across multiple regions. A job writes locally while CoreWeave replicates the data to another region in the background, so an agent's intermediate state, retrieved context, and outputs move as fast as its reasoning. The GPUs don't wait, and neither does the loop.
“CoreWeave was the first AI cloud provider to validate and bring up a Vera Rubin NVL72, demonstrating that this advanced rack-scale architecture could operate as a reliable, high-performance cloud service,” said Chen Goldberg, executive vice president of product & engineering at CoreWeave. “With multi-rack Vera Rubin, we are connecting hundreds of Rubin GPUs as a single scale-out cluster. For customers building agentic AI, that means greater scale, faster iteration, and higher productivity as models and agents continuously learn and improve.”
Scaling agentic AI with multi-rack NVIDIA Vera Rubin NVL72
A single NVIDIA Vera Rubin NVL72 rack pairs 72 Rubin GPUs with 36 Vera CPUs, NVIDIA NVLink 6, NVIDIA ConnectX-9 SuperNICs, and NVIDIA BlueField-4 DPUs. With multi-rack Vera Rubin NVL72, CoreWeave unifies racks of hundreds of accelerators using NVIDIA Spectrum-X Ethernet networking into a single scale-out cluster. This delivers the capacity to train larger models, serve more demanding inference workloads, and run reinforcement learning at scale, and achieves required engineering at every layer across compute, networking, storage, cooling, power, firmware, and software, to perform as one coordinated system.
CoreWeave brings multiple racks up as a single system through:
- Automating rack life cycle control. Racks arrive as hardware that needs to be connected and validated. CoreWeave Mission Control® automates rack setup through the Rack LifeCycle Controller, which coordinates hardware detection, firmware updates, validation, power, and cooling, with Racky providing rack control and Valvey executing cooling actions. 
- Validating performance from components to systems. CoreWeave combines NVIDIA field diagnostics with full-rack workload testing, comparing every result, building upon years of real-world experience, before a rack goes into production. Only racks that clear this bar as a system move into production, so every GPU performs at its best.
- Scaling the network with the GPUs. Every Rubin GPU is equipped with two NVIDIA Connect X-9 SuperNICs per Rubin GPU, providing 1.6 Tb/s of connectivity scale out connectivity per GPU across multiplane, multirail paths, supporting roughly 128,000 GPUs per rail in a non-blocking fabric. The modular topology allows racks to be added without redesigning the fabric at each expansion.
Keeping AI data close to compute across regions
AI performance depends on keeping data moving as quickly as compute. CoreWeave AI Object Storage LOTA (Local Object Transport Accelerator) brings data closer to AI workloads through managed caching on each CoreWeave Kubernetes Service node, delivering reads at local NVMe speeds and reducing latency by 8x compared to reading from a traditional storage cluster. LOTA provides up to 7 GB/s of throughput per GPU and scales linearly as clusters grow, helping eliminate network bottlenecks and accelerate AI training. 
“Our datasets span multiple regions, and we can’t afford to have our training schedule dictated by cross-region retrieval delays,” said Cécile Robert-Michon, director of internal infrastructure at Cohere. “CoreWeave AI Object Storage gives us a unified dataset footprint across regions with reads cached locally, so nothing waits on the network. It’s the difference between planning around our data and simply training.”
New capabilities now allow customers to run workloads across two regions while avoiding cross-region write latency and reducing long-term storage costs.
- Checkpoints can now be written locally within a region, closest to the available compute. Data can now be written at local latency while being migrated to a second remote region in the background. This benefits companies with compute in multiple regions, but data in only one region, that are writing checkpoints during training jobs. The new cross-region write feature minimizes the pause, and enables the CKS cluster to continue training. Since the application sees a single bucket, there are  no code changes, and permissions and retention rules work the same regardless of which region a write came from. This improves operations by eliminating the need to manually copy or move data from one region to another for critical AI workloads.
- The decision to keep critical data longer just became easier and less expensive. Teams routinely delete data they would rather keep: the checkpoint from the run that almost worked, the dataset needed to reproduce a result, the model version someone may ask about in six months. Archive is a new lower-cost storage tier built for exactly that data, with no fee to retrieve it, no fee to delete it early, and no fee when reading it from the Archive tier. 

CoreWeave consistently delivers industry-leading performance, demonstrated by record-breaking MLPerf benchmark results in inference and training, its position as the only AI cloud to earn the top Platinum ranking in both SemiAnalysis ClusterMAX™ 1.0 and 2.0, and its #1 ranking for inference speed and price-performance for Moonshot AI’s Kimi K2.6 and Kimi K2.7 Code in independent inference benchmarking conducted by Artificial Analysis.About CoreWeave
CoreWeave is The Essential Cloud for AI™️. Built for pioneers by pioneers, CoreWeave delivers a fully integrated platform of technology and teams that enables innovators to move at the pace of innovation, building and scaling AI with confidence. Trusted by 9 of the 10 leading foundation model providers, CoreWeave serves as a force multiplier by combining superior infrastructure performance with deep technical expertise to accelerate human discovery. Established in 2017, CoreWeave completed its public listing on Nasdaq (CRWV) in March 2025.

Share this article:

Copied

## Media Contacts

CoreWeave Media[email protected]

## More press releases

### CoreWeave Expands Global AI Cloud Platform With New Capacity in Denmark and First Global AI Network Backbone
Expansion brings additional AI computing capacity online in Europe and extends CoreWeave’s high-performance global network to support customers building and scaling AI worldwide

3
min read

### CoreWeave Launches the CoreWeave Zero Trust AI Framework, Keeping Customers in Control of Access to Their Models, Data and Runtime Environments 
Six layers of customer-controlled security, from encryption keys to runtime, designed to keep CoreWeave out of the customer's trust chain

4
min read

### CoreWeave Unveils CoreWeave Physical AI Launchables, Taking the Setup Work Out of Robotics and AV Development
Engineers get tested configurations for the software they already use, so time goes into the work instead of the plumbing

4
min read

### CoreWeave Enters India, Expanding AI Cloud Platform With AdaniConneX
CoreWeave enters India with AdaniConneX, planning a 240 MW deployment in Navi Mumbai to bring its purpose-built AI Cloud closer to customers.

3
min read

### Ennoble Care selects CoreWeave to power AI inference across its home-based care network
The home-based care provider and accountable care organization will run its inference workloads on NVIDIA RTX PRO 6000 GPUs deployed through CoreWeave Kubernetes Service

3
min read

### CoreWeave Partner Network Accelerates the Path to AI Innovation
Brings validated partner integrations into one curated place
Spans the AI loop, anchored by years-deep collaborations with Reflection, VAST Data, ClickHouse, CrowdStrike and more

min read

### CoreWeave to Offer NVIDIA Vera, the First CPU Built for AI agents
CoreWeave expands compute portfolio to meet the needs of AI workloads.

min read

### CoreWeave Delivers NVIDIA Vera Rubin NVL72 Performance at Production Scale, Starting With Cognition
CoreWeave maintains industry-leading AI cloud performance across multiple compute generations with its software platform

3
min read

### CoreWeave Forge Launches, Turning the AI Loop Production Run Into a Better Model and Agent
One connected environment for training, inference, evaluation and agent development, open across models, frameworks and other clouds, so every version ships sooner and performs better than the last

4
min read

### CoreWeave Becomes the Only Provider to Earn SemiAnalysis' Platinum ClusterMAX™ Rating Three Consecutive Times
Repeat recognition as the only Platinum AI cloud in every ClusterMAX evaluation underscores CoreWeave's sustained leadership

2
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
