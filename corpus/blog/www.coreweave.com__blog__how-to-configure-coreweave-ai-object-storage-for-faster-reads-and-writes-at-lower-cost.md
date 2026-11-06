# CoreWeave AI Object Storage Setup: LOTA, Writes, Archive

Source: https://www.coreweave.com/blog/how-to-configure-coreweave-ai-object-storage-for-faster-reads-and-writes-at-lower-cost

Announcement

Webinar

Podcast

GTC 2026

CoreWeave Forge is here: connect your AI loop and compound every improvement. Read more

Contact us

Three things in CoreWeave AI Object Storage (CAIOS) determine how fast your GPUs read, how long your writes take, and what you pay to keep data you're not actively using: Local Object Transport Accelerator (LOTA), cross-region write acceleration, and the Archive tier. All three are configurations, not architectures, and none require rewriting an application.
Part 1 covered what each one does and why it matters. In Part 2, we demonstrate how to configure each: pointing a client at the LOTA endpoint, pre-staging a cache before the first epoch, enabling cross-region writes on a bucket, and setting an Archive policy that ages checkpoints on its own. Every example includes code you can copy and adapt: Python, boto3, or a CLI command for bucket settings.

## Select a storage class and billing level
First, decide which region a bucket lives in, then choose how its data is stored and billed. 
We offer a simple decision: whether you want the new Archive billing level. That comes down to two S3 API values: 
Each bucket can have four storage billing levels. They relate like this:

 | Storage class
 | Storage billing level
 | How data gets there

 | STANDARD
 | Hot
 | Recently accessed

 | STANDARD
 | Warm
 | No access for 7 days

 | STANDARD
 | Cold
 | No access for 30+ days

 | STANDARD_IA
 | Archive
 | Opt in and customize

## Accelerate reads with LOTA
LOTA provides a compute-local NVMe endpoint to improve read latency. Everything else about your S3 client remains the same, and reads now come from the node-local NVMe cache when the object is present.
Three things affect how much your read latency can improve: 
- object size, 
- using multipart uploads, and 
- pre-staging the cache before the job starts.
LOTA caches objects larger than 4 MB; anything smaller is read directly from persistent storage. For large objects, it's best practice to use multipart uploads. The object is split into parts that upload in parallel to make the best use of available bandwidth, and smaller parts limit the impact of a network error. LOTA also distributes those parts across GPU nodes so that reads are served from several nodes at once, whereas an object uploaded with a single PutObject sits on one node. 

### Pre-staging the LOTA cache
In the first epoch, objects are read from the bucket and stored in cache as they are initially requested. That first read pays the full bucket latency, and every miss after it adds latency you didn't need to spend. 
Instead, pre-staging fills the cache with your predetermined dataset ahead of the job. This significantly improves your cache hits from the first epoch, rather than letting the ratio climb as the job runs.
To pre-stage the dataset a job will read, issue a HeadObject call with a zero-length range header against each object in it:
1from botocore.client import Config
2from concurrent.futures import ThreadPoolExecutor
3
4s3 = boto3.client(
5 "s3",
6 endpoint_url="http://cwlota.com",
7 config=Config(
8 max_pool_connections=32,
9 s3={"addressing_style": "virtual"},
10 ),
11)
12
13def prestage(key):
14 s3.head_object(
15 Bucket="training-data",
16 Key=key,
17 Range="bytes=0-0",
18 )
19
20with ThreadPoolExecutor(max_workers=32) as pool:
21 list(pool.map(prestage, shard_keys))
22
23
24
25
LOTA sees each ranged head request, fetches the complete object from the bucket, and places it in the cache. No response body comes back to your client. Populate shard_keys with the objects that the job will read, and the first epoch reads local.
Three things to know: 
- It only works through the LOTA endpoint: the same call against the primary endpoint returns metadata and fills nothing 
- The call counts as an access: pre-staging pulls objects up into the Hot tier, which matters if you're pre-staging data that has aged down 
- It's worth doing when the first-read latency is the thing holding you up: first-epoch training reads, loading model weights for inference, and checkpoint restores

## Enable cross-region write acceleration
Cross-region writes are enabled on a per-bucket level between any CoreWeave region pairs.
Similar to LOTA, when cross-region writes are enabled, nothing in your application changes. The application writes to the LOTA endpoint exactly as before, and the object bytes land durably in the local region and are acknowledged at local latency. Metadata is written synchronously to the bucket's remote region, so the bucket presents a single namespace. Any reader sees the same object regardless of which region it reads. The object data migrates to the remote region in the background.
1s3.upload_file(
2 "/tmp/checkpoint-4200.pt",
3 "checkpoints",
4 "run-17/checkpoint-4200.pt",
5)
6
Data migration timing: migration enqueues within 24 hours and typically completes within 72 hours, depending on object size and network link conditions. This is often fine for checkpoints, since a restart reads from the local region anyway. If an object must be in the remote region by a deadline, plan for 72 hours.

Checkpoint cadence: training pauses while a checkpoint writes, so cadence has always been a tradeoff between recovery granularity and time spent training. Removing the cross-region round-trip latency from each commit removes that tradeoff. If you throttled your cadence because commit latency was high, it's worth re-testing what cadence you can now sustain.

## Enable the Archive storage tier
Similar to cross-region write acceleration, Archive is enabled at a bucket level. There are two ways to utilize the new Archive storage tier: write directly to Archive or enable automated Archive on the bucket.
‍Option 1: Write directly to Archive. This works best if you know that an object is a long-term record rather than something you'll read soon. Writes to Archive carry additional latency compared to the Hot, Warm, and Cold billing level, so consider your application's latency tolerance.

1s3.upload_file(
2 "/tmp/final-weights.pt",
3 "checkpoints",
4 "run-17/final-weights.pt",
5 ExtraArgs={"StorageClass": "STANDARD_IA"},
6)
7
8
Option 2: Enable automated Archive on the bucket. Use this method when you'd rather set a rule, based on last access time, to migrate objects to the Archive tier. Two fields control this option:
1# Enable automated archive after 60 days without access
2cwic cwobject bucket update my-bucket \
3 --archive-enabled=true \
4 --archive-after-last-access-days=60
5

 | Field
 | What it does

 | --archive-enabled
 | Turns automated archive on for the bucket

 | --archive-after-last-access-days
 | Days since last access, or since creation if the object has never been read; required when --archive-enabled is true

The threshold is based on last access time and can be customized, with a 60-day minimum. The rule applies to STANDARD object versions and does not reprocess anything already in STANDARD_IA.

### Reading from the Archive storage tier
Since there's no restore step, an archived object reads with a standard GET, at the same bucket and key it always had:
1s3.download_file(
2 "checkpoints",
3 "run-17/final-weights.pt",
4 "/tmp/final-weights.pt",
5)
6
What differs is time-to-first-byte, which is longer than the other billing levels, and overall throughput, which is lower. This is something to consider for your applications. If latency is important, you can copy the object to the STANDARD storage class ahead of a bulk read. A copy onto itself with a new storage class is the standard S3 pattern. On a versioned bucket, it creates a new version rather than replacing the existing one, which is worth accounting for in any tooling that walks version history.
1s3.copy_object(
2 Bucket="checkpoints",
3 Key="run-17/final-weights.pt",
4 CopySource={"Bucket": "checkpoints", "Key": "run-17/final-weights.pt"},
5 StorageClass="STANDARD",
6 MetadataDirective="COPY",
7)
8

## Build a checkpoint retention policy
Let’s assume a training run in whichever region had GPUs available, writing checkpoints to a bucket hosted elsewhere. Here are the five decisions, in the order you'd make them:

- Checkpoints commit through the LOTA endpoint.
The job writes in whichever region it's running. With cross-region writes enabled, each commit is acknowledged locally and migrates to the remote region in the background. Nothing in the training script knows about any of this.
 
- Consider read latency for recent checkpoints.
Since they're being read, or at least recently written, they stay in the STANDARD tier. A recovery from a prior checkpoint occurs at lower latency than the Archive tier.
 
- Automated archive handles the tail.
Set a threshold; 60 days is the minimum. It needs to be long enough that anything still part of an active run has been touched and short enough that a finished run's checkpoints aren't paying Cold rates longer than they need to.
 
- Final weights can skip the ladder.
If a run is done and its final artifact is a record rather than a restart candidate, write straight to STANDARD_IA.
 
- Copy back before a planned bulk read.
If you know in advance that an application needs a set of objects, a copy pass ahead of it removes the longer time-to-first-byte. There are no retrieval, access, or operation fees for doing it.

## Confirm it works in Mission Control
CoreWeave Mission Control® gives you visibility into your storage estate without any setup. Grafana dashboards and storage metrics are available out of the box, and the cost and CAIOS usage monitoring guide has a worked query for AI Object Storage consumption grouped by bucket. 
Once automated archive is enabled, watch the Auto Archive panel group in the AI Object Storage usage panel and build your own views from the same metrics. Watch tier distribution shift as idle objects move.

Alternatively, you can use Mission Control MCP, which exposes metrics, logs, and AI Object Storage buckets as read-only tools for MCP-compatible clients. It's in public preview.

## Next steps
That's the full CAIOS configuration: an endpoint change, a pre-stage pass, a per-bucket enablement, and an archive policy. Two of them you can do today; two need to be turned on for your account first.
Begin using LOTA and pre-staging today. Cross-region write acceleration and Archive are both available. Contact your account team to see how these features can improve your AI workloads.

#### Learn more about AI Object Storage:
- Blog Part 1: New in CoreWeave AI Object Storage: Cross-Region Writes and Archive Storage
- CoreWeave AI Object Storage (CAIOS) documentation: LOTA best practices, pre-staging, and multipart upload guidance
- On-demand webinar: How to Move Beyond Tiers, Tradeoffs, and Runaway Costs in AI Storage

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
