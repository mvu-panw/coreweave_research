# CoreWeave AI Object Storage: Cross-region writes, Archive

Source: https://www.coreweave.com/blog/new-in-coreweave-ai-object-storage-cross-region-writes-and-archive-storage

Announcement

Webinar

Podcast

GTC 2026

CoreWeave Forge is here: connect your AI loop and compound every improvement. Read more

Contact us

You take GPU capacity where you can get it. Your data stays where you put it. Two new capabilities in CoreWeave AI Object Storage close the gap between them, and both are now available. Cross-region write acceleration lets a job write to a bucket in a remote region at local latency. And a new storage class, Archive, holds data you want to keep but expect to read rarely.
Compute (GPU and CPU) availability decides where your jobs run. Data doesn't relocate as easily, so you move it yourself: staging datasets ahead of a run, keeping copies near compute, and sequencing work around wherever the data already sits. That adds operational overhead, often requiring several copies of the same dataset and time. Every workaround costs the same thing: time you're paying GPU prices for.
This is the first part of a two-part blog series. Here we cover what the new capabilities do and why they matter alongside LOTA. Part 2 covers how to implement and use them.

## LOTA keeps read local and the GPUs fed
LOTA, Local Object Transport Accelerator, is an integral part of CoreWeave AI Object Storage, keeping reads local to the GPU and CPU nodes and generally available. It runs as a caching proxy on every GPU and CPU node in your CKS (CoreWeave Kubernetes Service) cluster, holding objects on local NVMe and serving cached reads at up to 7 GB/s per GPU.

Cache capacity and throughput scale linearly with the cluster. There's no additional cost to enable it, and pointing an S3-compatible client at the LOTA endpoint is the only change your code needs.
Feeding data into GPUs quickly and efficiently is critical to the success of AI workloads. Picture a sprinter who has to stop dead every 10 meters, wait, then start again. Top speed stops mattering when the sprinter never reaches it. That's analogous to a GPU waiting to read from a bucket. LOTA keeps the data on the node, so the workload runs the whole distance without stopping.
LOTA accelerates reads from a bucket regardless of which CoreWeave region that bucket sits in. A workload running in one region can read a bucket in another and achieve cache-local latency, without a costly second copy of the dataset or a replication job to keep those copies in sync. A leading frontier model provider runs LOTA across more than 15,000 GPUs and 20 PB of cache capacity, hitting cache 99.7% of the time. On those hits, p99 read latency is more than 8x lower than reading from the bucket.
Where the cache lives is the part that matters. LOTA holds objects on NVMe in the GPU node itself, so a cached read never needs to come from outside the machine. Some cloud providers offer a zonal read cache, but it puts network hops between the node and its data. For these jobs running at high throughput, that hop is the difference. LOTA is the closest an object cache can sit to the compute reading from it.
Our datasets don't live in one region, and we don't want our training schedule in one region dictated by how long it takes to retrieve data from a different region. CoreWeave AI Object Storage gives us unified datasets across regions with reads cached locally, so nothing waits on the network. That's the difference between planning around our data and simply training.
Cecile Robert-Michon, Director of Internal Infrastructure at Cohere

## Cross-region writes land at local latency
LOTA accelerates GETs. Writes are a separate problem.
A training job writing checkpoints to a bucket in a remote region waits on a round trip for every commit, and the training job waits with it. Training can pause while each checkpoint is written, so the more you increase your checkpoint cadence, the more it impacts the time spent training. Even with async checkpoints, storage must keep up and prevent the training process from stalling. The balance is keeping frequent recovery points, writing them as quickly as possible, and spend as close to 100% of the time training as you can.
Distance between regions adds latency and extends job completion time. It doesn't incur transfer fees, CoreWeave charges nothing for egress, ingress, or requests, cost you training time. At GPU prices, that's something to optimize.
Cross-region write acceleration makes a remote write behave like a local one. The path works like this:
- Your application issues a standard S3 write to the LOTA endpoint. No API changes, no SDK changes.
- The object data is written durably in the local region and acknowledged at local latency. Metadata commits to the remote region, and both regions share a single bucket namespace, and every reader sees the same object regardless of which region it reads from.
- The object is immediately visible and readable, including to the application that just wrote it.
- In the background, the object data migrates to the remote region.
Local Object Transport Accelerator and Cross-Region Write
Lower latency is the benefit you'd expect. The one that matters six months in is that this is still one bucket. IAM policies, lifecycle rules, and access controls apply uniformly regardless of which region a write originated in. One namespace, one source of truth, no replication pipeline for someone on your team to own, and no per-region forks to reconcile later.
Cross-region writes are enabled per bucket for any CoreWeave region pair of your choosing. Take the GPUs wherever you can get them—your data no longer has to follow.
During training, keeping GPUs from data starvation is a delicate balance of minimizing storage latency without complicating storage operations. Caching on the compute node itself, across thousands of nodes in a cluster, is a meaningful architectural difference from zone-level approaches. Doing it without application changes or a replication pipeline to maintain is what makes it operationally viable at scale.
Dave McCarthy, Group Vice President, IDC

## Archive keeps what you would have deleted
Somewhere in your storage right now, there's a checkpoint from the epoch that almost worked. A preprocessed corpus you'd need to reproduce a result. A model version somebody might ask about in six months. Every few quarters someone runs a cleanup, and some of it is deleted.
The data isn’t worthless, but the cost of keeping it is hard to predict. Storage is priced per GB, but reading it back, listing it, deleting it early, or moving it somewhere else are actions each priced separately. The cost of retention depends on what you'll do with the data later, which is the unknown part.
The new Archive option available in CoreWeave AI Object Storage removes that calculation. It's a fourth option alongside Hot, Warm, and Cold, priced for AI workload data you intend to keep and expect to read rarely. You pay for what you store, and nothing else. 
Archive something today, delete it next week, and it costs you nothing extra. Here's how that compares:

 | 
 | CoreWeave
 | Typical cloud providers

 | Retrieval fees
 | No
 | Yes

 | Cache fees
 | No
 | Yes

 | Per request fees
 | No
 | Yes

 | Early-deletion fees
 | No
 | Yes

 | Tiering fees
 | No
 | Yes

 | Egress fees
 | No
 | Yes

Every choice here has a cost and a consequence. Data can stay in Hot, Warm, and Cold; this works, but may not be cost-optimized. Archive costs less, and the consequence is a longer time to first byte than the other three.
You see this tradeoff most clearly with checkpoints. Treat them like a backup policy: keep recent checkpoints out of Archive, where a restart can reach them immediately, and let the policies move them across tiers as they age past 60 days without access. If you want to customize this beyond 60 days, that’s an option as well, or write directly to Archive when you already know a checkpoint is a long-term record rather than a restart candidate. 
In doing so, Archive turns retention from a quarterly judgment call into a policy you set once. Keep in mind that writes to Archive carry additional latency.
Intelligent tiering across high performance and archive tiers

## One bucket, one AI loop
Each turn of the AI loop produces evidence: checkpoints, eval results, a record of how the model actually behaved. Run, observe, curate, evaluate, improve, then repeat. Launch day is day one; once a model or agent meets production, that evidence arrives faster and matters more. How fast the loop turns depends on how quickly the infrastructure underneath can write it, move it, and hand it back.
Follow a single checkpoint. It's written from whichever region had the GPUs, at local latency. It migrates to the desired remote region in the background, without anyone scheduling any data replication. It then moves into Archive after 60 days of inactivity, with no manual intervention. A year later somebody pulls it back for an ablation with a standard GET, from the same bucket and object key.
That tiering policy is what keeps the AI loop turning through training and reinforcement learning. Recovery pulls from the most recent checkpoint, which may sit in Hot, Warm, or Cold, all of which read at similar latency. Everything older ages into Archive, still available when a result needs reproducing or a run needs auditing, at a price that makes keeping it an easier call.
Three capabilities, one bucket, one namespace. LOTA lowers read latency. Cross-region writes lower write latency. Archive keeps the record each turn of the AI loop produces, so the next epoch has something to build on.

### Remove the manual storage steps from your workflow 
Contact your account team to see how your AI workloads can benefit from these new features. Not using CoreWeave AI Object Storage? Reach out to our team to learn more. 
Part 2 walks through how platform engineers and storage admins can implement these features.

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
