# What Is Node Lifecycle Management and Why Does It Matter for ML Training and Inference? | CoreWeave Blog

Source: https://www.coreweave.com/blog/what-is-node-lifecycle-management-ml-training-and-inference

Announcement

Webinar

Podcast

GTC 2026

CoreWeave Forge is here: connect your AI loop and compound every improvement. Read more

Contact us

Large-scale AI clusters require a different approach than traditional massively parallel processing. While these clusters deliver the speed and performance needed for generative AI, they require careful management and upkeep to maintain peak efficiency and seamless operation.   A single component failure in an AI cluster could take down a whole training job, if not managed properly.
In their latest paper, the Llama Team at Meta demonstrated the reliability and operational challenges of AI training.  During a 54-day snapshot period of pre-training, the Llama Team experienced a total of 466 job interruptions, approximately 78% of which were attributed to confirmed or suspected hardware issues (Table 5 in the paper).
“The complexity and potential failure scenarios of 16K GPU training surpass those of much larger CPU clusters that we have operated. Moreover, the synchronous nature of training makes it less fault-tolerant—a single GPU failure may require a restart of the entire job.” 
— The Llama 3 Herd of Models, Llama Team at Meta, published July 23, 2024, page 13.
While GPU clusters have some maintenance challenges, they execute an order of magnitude more work in less time than general-purpose servers with CPUs, making GPUs great for AI. 
To understand this challenge and how CoreWeave is addressing it given the need for accelerated computing for AI, we spoke with Navarre Pratt, a Solutions Architect at CoreWeave who worked through last year’s NVIDIA H100 Tensor Core GPU  rollout and the implementation of our new node lifecycle management. Take a look at the Q&A below, and reach out to our team if you have more questions about node health checks and lifecycle management.
‍

#### What do health checking and node lifecycle management mean for ML clusters?
Clusters are not static. They involve continuous monitoring of the node performance in the cluster and auxiliary components, like ethernet and NVIDIA Quantum-2 InfiniBand fabrics, to maintain integrity and performance. To handle these dynamic states, you need automated node lifecycle management. 
Node lifecycle management is the process of continuously monitoring and acting on the performance of nodes in AI clusters. It reacts to data events triggered by health checks and takes the appropriate action, like moving a node from “production” to “triage” or rebooting it. Health checking can involve both “passive” and “active” checks.
Passive health checks run in the background of a node, meaning they do not utilize the GPUs in any way. They can be used to collect metrics, but also to detect GPU errors (i.e. XID errors), temperature spikes, etc. Active health checks are those that require using the GPU, therefore they can’t be run 24/7. Therefore these mostly run during node bring-up, but also have mechanisms to run them on “production” nodes while our customers leave them idle. Our suite of active health checks includes basics like GPU burn and NCCL tests but increases in complexity to include various ML training tasks. 

#### How detrimental are node failures in model training?
Specifically for training, you try to use every node in the cluster—all at once — in the same job. All the nodes have to be working together to improve the model, batch by batch. If an isolated failure occurs, the entire job restarts from the latest checkpoint. Many of these clusters are built at a large scale, some 30,000+ GPUs, which means a failure can have a significant impact on GPU utilization if not managed properly.
If you do some quick math, a large job going down, plus accounting for restarting at a previous checkpoint, can be very costly. Then there are other detriments in a cluster that aren’t specifically due to a failed node, like a faulty switch, which lowers the performance,  but unlikely the job will completely fail due to InfiniBand’s autonomous self-healing capabilities. Still, a 10% performance reduction can be very costly if it’s not caught and fixed promptly.
All that to say is that being able to detect issues and solve them quickly is extremely important. 

#### What about inference workloads—how do health checks impact these clusters?
With training jobs, many nodes are working together on the same task. In contrast, running inference on large scales involves nodes operating with increased independence. Each instance of the model works on separate tasks. Therefore if any one node fails, the blast radius is reduced. Nevertheless, inference services often demand exceptionally high uptime standards relative to training jobs. Adding pipelines with different models working together on a request by the end user only adds to the importance of keeping your GPU fleet healthy.

#### How has node lifecycle management evolved over the last year and a half, and what’s driving those changes?
Node failures aren’t a new problem, but they are more prevalent now than they used to be. New generations of components come with novel issues, and we remain committed to providing a level of performance only achieved for using cutting-edge technologies.
Combining the increasing intricacies of these nodes, coupled with the pace at which we deliver capacity to customers, has necessitated enhanced focus on post-deployment testing and monitoring, even after nodes have passed all initial burn-in tests. Some nodes may operate at optimal performance for weeks before issues manifest. By implementing robust lifecycle management for deployed nodes, we can efficiently establish and maintain the health of large clusters over a long period of time.
Another way this process has evolved is the increasing sophistication of our active health checks. Given the intricate nature of these clusters, identifying issues without running real workloads proves challenging. To address this, we’ve developed a suite of tests to better match customer workloads which includes various forms of ML training. We’ve found that these do a great job of revealing issues that more standard performance tests have missed.  

#### What are some of the biggest challenges engineers face when it comes to managing nodes and the overall health of the cluster? 
A significant challenge in working with cutting-edge technologies is the constantly evolving environment. This dynamic nature, combined with the immense scale of these modern clusters, results in a system that is difficult to manage. Consequently, the implementation of a comprehensive observability stack becomes crucial.
When something goes wrong in a training job, step 1 is everything involved with getting it back up and running like rescheduling the job and reloading checkpoints. Step 2 is to find the root cause so the same issue won’t cause another failure. There are countless different reasons why a job could fail, many of which manifest themselves the same way, i.e. an NCCL timeout. Without observability into the infrastructure, it is hard to discern between a software issue or an XID error on a GPU.

#### Let’s talk more specifically about node lifecycle management. CoreWeave has a two-phased approach. Could you explain what this is?
Phase 1, or “node bring-up,” is everything we do before it gets into a customer’s hands. This ensures the cluster is healthy and performant before they start running jobs.  As nodes come online, the first step is installing (or updating) firmware and checking the server inventory to ensure that all the components are in place and accounted for. 
When the node looks as we expected, we start running tests on the GPUs. Currently, this process takes 24-48 hours. Any of these tests failing will trigger automated or manual action, but passive metrics like temperature are also constantly monitored.  If all that ends successfully, it goes into production for the client to use.
Once it’s in production, we’re in Phase 2.  This involves running health checks, both passive and active, which trigger events our system acts on. The action we take depends on the type of issue that we notice, but also whether or not the client is actively using the node. It might be as simple as rebooting it back into production, but it might be more complex, requiring the node to be drained (the process of removing all customer workloads from the node) or even returned to the vendor for return merchandise authorization (RMA).
RMA is the process of returning a faulty server back to the supplier so that they can physically inspect why it failed. Faulty nodes can take up to a month before a failure is detected, so the faster we turn out the bad ones in RMA, the faster we can get a stable cluster.

#### How much visibility do clients have into the health checks and node lifecycle management of their CoreWeave cluster?
Across our entire stack, much more than node lifecycle management, we strive to give the customer as much visibility onto their nodes as we have internally. We’re able to provide visibility into the node directly because the Kubernetes environment we manage for users runs directly on bare metal. They see the whole lifecycle graph: events, alerts, nodes moving between states, and the history of a node (i.e. if a node had previous errors and is now back to production). 

#### Where is all this happening? Do you still need an engineer in the data center to debug, or is a lot of the automation/software implemented through the cloud?
All of the automation we are running, the Fleet and Node Lifecycle Controllers, are built into CoreWeave’s software platform. Much of the info about alerts and actions taken on nodes in production can be seen inside of customers’ CoreWeave Kubernetes Service (CKS) clusters.
The team that owns this in CoreWeave is the Fleet Engineering Team, which has three or four different teams within itself. There are dozens of engineers all focused on automating these tests, adding new tests, and debugging issues that we haven’t seen yet. While we might be able to detect every error automatically, there will always be nodes that need to be routed through RMA, which require in-person Data Center Technicians that CoreWeave has at all of our locations 24/7.

#### How does automation improve node lifecycle management? 
As we’ve previously discussed, moving quickly to diagnose and resolve issues is very important. Without automation to detect issues, we’d have to rely on customers opening support tickets. Even if we were very responsive to support tickets, it still relies on the customer diagnosing issues with their jobs as hardware issues.
The automation isn’t just automatically rebooting a node whenever we see a certain error, but it also deals with impacting customer workloads. If we know a certain error is catastrophic, we can immediately reboot the node. If there is a less severe issue, we can stage the node to be moved out of production whenever a customer’s job finishes. All of this prevents time spent going back and forth with a customer about when it’s ok to remove a node from their cluster. The customers of course have visibility into everything that we did and what happened, but they don’t have to do anything to make sure their cluster stays healthy and running.
 A few of our  AI enterprise clients have mentioned, “This is one of the healthiest clusters we ever had”  and, “This is the fastest bring-up we’ve ever had for a cluster.”

#### What’s the biggest piece of advice you would give other engineers about health checks and node lifecycle management?
Think about health checks and lifecycle management from the very beginning and implement observability wherever you can as much as possible. You don’t just want to add it on top of your platform at the end.
CoreWeave is The AI Hyperscaler, so we’ve been thinking about GPU health checking and all the complexities of that from the very beginning. Again, there’s not a specific layer for health checking that works on top of our stack. We’ve integrated it through everything we do.

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

Mission Control,

Copy code

Copied!

Mission Control,
