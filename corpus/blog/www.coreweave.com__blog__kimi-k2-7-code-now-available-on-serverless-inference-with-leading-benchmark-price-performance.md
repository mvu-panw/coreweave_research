# CoreWeave Leads on Artificial Analysis for Kimi K2.7 Code Inference | CoreWeave Blog

Source: https://www.coreweave.com/blog/kimi-k2-7-code-now-available-on-serverless-inference-with-leading-benchmark-price-performance

Announcement

Webinar

Podcast

GTC 2026

CoreWeave Forge is here: connect your AI loop and compound every improvement. Read more

Contact us

Kimi K2.7 Code, the latest coding model from Moonshot AI, is now available on CoreWeave Serverless Inference. In addition, CoreWeave is the leading AI inference provider in the most attractive quadrant of Artificial Analysis's Speed vs. Price chart for Kimi K2.7 Code, delivering the highest output speed at a low blended price. This is the second Kimi model in a row that our team has optimized and put live on CoreWeave Inference with improved performance.
Artificial Analysis measures the two metrics that matter most to production teams: output speed in tokens per second and price per million tokens. For price, a 7:2:1 blend of cache-hit, input, and output costs reflects real workload distribution more accurately than input or output price alone. Among all providers serving Kimi K2.7 Code, the latest coding model from Moonshot AI, CoreWeave delivers the highest token throughput with the lowest latency, delivering the best price-performance.1
Speed vs. Price for Kimi K2.7 Code across inference providers (source: Artificial Analysis). 
This result comes from metal-to-model optimization and collaboration between our Applied Training and Inference teams. In a previous blog, we covered the Kimi K2.6 optimization that earned CoreWeave the same validation on Artificial Analysis. In this post we go into the engineering work delivered for Kimi K2.7 Code that earned the team this validation for the second consecutive time and what that means for your inference workloads.

## Kimi K2.7 Code is Moonshot AI’s latest coding model
Kimi K2.7 Code is Moonshot AI’s latest coding-focused agentic model, built on the same trillion-parameter MoE (Mixture-of-Experts) architecture as Kimi K2.6, with 32 billion active parameters per token, a 256K-token context window, and open weights released under a Modified MIT license.2
The model is tuned for long-horizon, end-to-end coding tasks and agentic tool use.The most production-relevant change is in efficiency: Moonshot AI reports Kimi K2.7 Code uses about 30% fewer reasoning tokens than K2.6 on the same work,3 which cuts cost and latency in agent loops that call the model repeatedly.

## Optimizing Kimi K2.7 Code on Blackwell: NVFP4 quantization and a DFlash speculator
CoreWeave’s Applied Training team uses NVIDIA GB300 NVL72 and GB200 NVL72 clusters to optimize the latest AI models for production inference, with tooling that includes NVIDIA’s Model-Optimizer for post-training quantization. Every experiment is backed by accuracy and quality evaluations in Weights & Biases and modern test-harness frameworks. 
Kimi K2.7 Code shipped pre-quantized in INT4 (4-bit integer). Because INT4 is an integer format and Blackwell accelerates FP4 (4-bit floating point), including NVFP4 (NVIDIA 4-bit floating point), the released weights need quantization before they can fully benefit from Blackwell’s FP4 execution. 
The CoreWeave Applied Training team did exactly that, pairing a custom NVFP4 quantization with a DFlash speculative decoder. Getting to this level of performance on a 1T parameter scale model required a multi-step training and evaluation process.
First, we started by mirroring the original weights from Moonshot AI to a CoreWeave AI Object Storage bucket with Local Object Transport Acceleration enabled so that we could horizontally scale out access to the weights without hitting any rate limits. To get a baseline for the model, we measured the INT4 weights with a comprehensive list of evals like Terminal-Bench 2.0, AIME2025, SWE-Bench Pro and SWE-Bench Multilingual, powered by the Harbor framework with the Terminus-2 agent with multiple trials each. Then we used the NVIDIA Model-Optimizer project with a custom  3-pass calibration for converting the INT4 weights into NVFP4 weights. This included a short context window pass over general conversation data and long context window passes over math and coding datasets to help align to Kimi K2.7 Code’s own focus on coding work. All evals were executed in CoreWeave’s very own Sandbox platform and evaluated with large amounts of concurrency to speed up the iteration loop.
Once we were confident in the accuracy of the quantized checkpoint, we moved on to training a DFlash speculative decoding model. This involved generating a new dataset using the NVFP4 checkpoint, where we used over 1 million different prompts, once again spanning various long context agentic tasks involving tool calling and other agentic coding work. We generate these new responses based on the NVFP4 checkpoint to guarantee that our speculator model learns the distributions of the NVFP4 checkpoint specifically, to maximize acceptance length in the most diverse set of cases. In order to facilitate the training itself, we used the TorchSpec project from the LightSeek Foundation. We used a modified loss function with the DFlash architecture called D-PACE which came from a combination of Harvard and MIT researchers which showed us an approximate 8% improvement in acceptance length across all categories as measured by the SPEED-Bench AL dataset. We have since contributed D-PACE support back to TorchSpec upstream. To measure the acceptance length of our speculator model, we made heavy use of AIPerf from the NVIDIA Dynamo team which already included direct support for SPEED-Bench, but we also contributed support for running the most commonly reported AL evals according to the modern literature to make it easy to compare our results to those published online.
The draft model training occurred on multiple GB300 NVL72 racks managed by the CoreWeave Kubernetes Service and scaled out over a RoCE fabric for the fastest training speeds such that we can deliver this fast and high-quality Kimi K2.7 Code deployment to our customers.
The production K2.7 Code endpoint on CoreWeave Inference runs this NVFP4 + DFlash configuration on vLMM by default, allowing customers to benefit from the throughput and cost improvements, with no additional setup on their side.

## Inference performance goes beyond model-level optimizations
In production inference, performance and cost are tightly coupled, and the relative priority depends on the workload. Customer-facing applications often optimize for latency, while offline workloads such as evaluation, synthetic data generation, or batch processing prioritize throughput at the lowest possible cost. GPU selection, quantization, attention kernels, KV-cache layout, batching strategy, and speculative decoding all influence both.
The Kimi K2.7 Code optimization is only part of the story. Model-level improvements such as quantization and speculative decoding are amplified by optimizations throughout the infrastructure stack. CoreWeave is designed to maximize inference performance at every layer, from bare-metal access to the latest NVIDIA GPUs and high-speed interconnects to optimized memory architectures and custom inference stack tuning. Together, these layers determine how efficiently model-level gains translate into production throughput, latency, and cost. And more importantly, this is the benefit customers get when they build their AI applications on the CoreWeave platform. Faster responses at a lower price point can deliver meaningful improvements in AI applications. The resulting performance is what appears consistently in third-party benchmarks such as Artificial Analysis and MLPerf earlier this week. 
These repeated validations come from running the work as a continual loop: the Applied Training team trains the DFlash speculator and quantizes the model, validates quality in Weights & Biases, and ships the result to CoreWeave Inference. Train, evaluate, serve, measure, repeat, on one platform: the same closed loop CoreWeave runs between training and inference gets applied to model optimization and using CoreWeave capabilities like Serverless RL, Sandboxes, W&B Weave, W&B Models, and W&B Evals, customers can execute this same loop for their application improvements. 
CoreWeave Inference customers can get access to this incremental price-performance across all inference deployment paths and can tune to the right cost-performance level for each workload. CoreWeave serves these optimizations on vLLM, the open-source inference engine, with quantization and speculative decoding tuned in our own vLLM build. On Serverless Inference, you call K2.7 Code through one API, pay per-token and inherit the performance optimizations without running any infrastructure. Dedicated Inference adds control over GPU selection, runtime configuration, and auto-scaling when you want to tune for a specific workload, with CoreWeave managing the infrastructure. Inference on CoreWeave Kubernetes Service (CKS) gives direct control over GPUs, runtimes, orchestration, and capacity for teams that want the knobs themselves.
Try Kimi K2.7 Code on CoreWeave Inference now
Learn more about CoreWeave Inference
‍
1. Price-performance is measured in speed vs. price
2. https://www.kimi.com/resources/kimi-k2-7-code
3. https://www.kimi.com/resources/kimi-k2-7-code

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
