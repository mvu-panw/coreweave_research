# CoreWeave's Innovation Velocity Drives in MLPerf 6.0 Leadership

Source: https://www.coreweave.com/blog/coreweaves-innovation-velocity-drives-mlperf-6-0-leadership

Announcement

Webinar

Podcast

GTC 2026

CoreWeave Forge is here: connect your AI loop and compound every improvement. Read more

Contact us

Since CoreWeave’s inception we have consistently been the first to move and the first to scale across multiple generations of AI-native cloud infrastructure, and that has repeatedly resulted in optimized and leading performance for our customers. That’s why pioneers like Cursor AI, Cline, Mercado Libre, and 8 of the 10 leading foundation model providers rely on CoreWeave. This leadership was reflected in MLPerf 5.0 inference benchmarks, and continues in MLPerf 6.0.
Excellence isn’t a single act—it’s the result of consistent, repeated actions, over time, that deliver exceptional results.

 | Improvement
 | Details

 | NVIDIA GB200 NVL72
 | MLPerf 5.0 Inference benchmark, Llama 3.1 405B7
> 2x NVIDIA H200 GPU7

 | NVIDIA GB300 NVL72
 | MLPerf 6.0 inference benchmark, DeepSeek R110,11
2x MLPerf 5.1 inference benchmark for server mode8

 | Performance Gain
 | 1.6x MLPerf 5.1 inference benchmark for offline mode9

When CoreWeave leads, it doesn’t stand still. In MLPerf 5, CoreWeave demonstrated that we're first to move and first to scale, resulting in leading NVIDIA GB200 NVL72 inference performance. That lead continues in MLPerf 6.0, where CoreWeave remains the top performer for DeepSeek R1.
CoreWeave moves first, scales first, and delivers optimized performance—consistently reflected across MLPerf benchmarks.

 | Platform
 | Benchmark Model
 | Server TPS/GPU
 | Offline TPS/GPU
 | Results

 | NVIDIA GB300 NVL722
 | DeepSeek R1 (671B, NVFP4)3
 | 5,5745
 | 9,8215
 | Doubled throughput performance from MLPerf 5.1 in server mode5.

 | NVIDIA GB300 NVL721
 | DeepSeek R1 (671B, NVFP4)3
 | 5,5745
 | 9,8215
 | Led all submitters in offline mode5.

 | NVIDIA GB300 NVL721
 | GPT-OSS-120B
 | 14,94614
 | 14,2264
 | Led all submitters in improvement over NVIDIA GB200 NVL72, including >28% in offline mode5.

 | NVIDIA GB200 NVL721
 | DeepSeek R1 (671B, NVFP4)3
 | 4,8684
 | 7,3234
 | Led all submitters in server and offline mode5.

## CoreWeave doubles NVIDIA GB300 NVL72 MLPerf performance
The NVIDIA GB300 NVL72 is a rack-scale system built for AI reasoning with 1.5x more dense NVFP4 Tensor Core FLOPS and 2x higher attention performance than NVIDIA Blackwell GPUs15. Since deploying GB300 NVL72 systems in production last year, CoreWeave has continued to refine the throughput performance. Using  DeepSeek R1, CoreWeave demonstrated faster inference throughput, improving by 1.6x in offline mode  and  2x in server mode from  MLPerf  5.1 over the last 6 months.
Figure 1. CoreWeave delivers 2x the Tokens/GPU inference performance with NVIDIA GB300 NVL72 in server mode.
With GPT-OSS-120B, CoreWeave delivered high throughput inference performance in both offline and server modes with NVIDIA GB300 NVL72, demonstrating up to 28% higher inference throughput compared to NVIDIA GB200 NVL72. For DeepSeek R1, CoreWeave inference throughput in offline mode for the NVIDIA GB300 NVL72 was the highest of all submitters.

## CoreWeave demonstrates the performance benefits of NVIDIA GB300 NVL72 vs NVIDIA GB200 NVL72
The NVIDIA GB300 NVL72 leverages the same architecture as the NVIDIA GB200 NVL72 but has more memory and other performance improvements. CoreWeave’s MLPerf results demonstrate these performance improvements with a 14% improvement compared to the GB200 in server mode, and 34% improvement in offline mode.
Figure 2. CoreWeave improves DeepSeek R1 server throughput by more than 14% in server mode on NVIDIA GB300 NVL72 compared to NVIDIA GB200 NVL72, and more than 34% in offline benchmark.

## CoreWeave continues MLPerf NVIDIA GB200 NVL72 inference leadership
CoreWeave was the first AI-native Cloud to offer the NVIDIA GB200 NVL72 in production at scale, and the NVIDIA GB200 NVL72 benchmark leader in MLPerf 5.0. That leadership continued in MLPerf 6.0, for example by leading all submitters in DeepSeek R1 inference benchmarks in both server and offline mode10 ,11.
Figure 3. CoreWeave led all submitters in the DeepSeek R1 benchmarks for NVIDIA GB200

## From MLPerf to real-world inference products
CoreWeave Inference is architected to support every level of operational need, giving teams a clear path from fully managed serverless to fully self-managed infrastructure as their requirements evolve. 
For teams who want to move fastest without managing any infrastructure, CoreWeave offers Serverless Inference through Weights & Biases (W&B) Inference. Teams can deploy and iterate instantly with autoscaling, high availability, and integrated observability out of the box, while pay-per-token pricing keeps costs aligned with actual usage as workloads grow.
CoreWeave recently announced Dedicated Inference which provides lifecycle-supported inference that lets customers bring their own weights, pick GPUs and open runtimes, while CoreWeave handles production operations and cost visibility. Currently in preview, Dedicated Inference is designed to keep performance behavior and cost drivers predictable as workloads scale. AI pioneers can request preview access to Dedicated Inference and experiment with their own inference workloads. 
For those who prefer to have more control, Inference on CKS (CoreWeave Kubernetes Service) enables developers  to self-host their models, runtimes, and orchestration. This provides the ultimate level of infrastructure control, tuning, and end-to-end observability, ensuring their stack is aligned with the required performance and security.
Because these inference paths share a consistent architectural base, teams can move from iteration to scaled production without replatforming or introducing cost ambiguity. Performance behavior, scaling dynamics, and cost drivers remain visible and aligned to underlying infrastructure as AI applications evolve.

## Results at a glance:
- CoreWeave doubled the DeepSeek R1 server mode throughput performance from MLPerf   5.1 with the NVIDIA GB300 NVL72  in just 6 months.

- CoreWeave led all submitters in DeepSeek R1 throughput performance, measured in tokens per second per GPU, for the NVIDIA GB300 NVL72  in offline mode.

- CoreWeave led with the highest tokens per second per GPU with NVIDIA GB200 NVL72 for DeepSeek R1 among submitters  
- ‍CoreWeave achieved the highest increase with more than 28% higher throughput from NVIDIA GB200 NVL72 to NVIDIA GB300 NVL72 with GPT-OSS-120B in server mode.
Learn more about how CoreWeave can support your AI Inference needs.

 1
 CoreWeave MLPerf 6.0-0020 node with 64 x NVIDIA GB200 GPUs, each with 186GB of HBM3e memory. Other submitter nodes used 72 x NVIDIA GB200 GPUs, each with 186GB of HBM3e memory.

 2
 CoreWeave Node MLPerf 6.0-0022 node with 8 x NVIDIA GB300 GPUs, each with 288GB of HBM3e memory. CoreWeave Node MLPerf 5.1-0097 node with 8 x NVIDIA GB300 GPUs, each with 288GB of HBM3e memory.

 3
 Input/output tokens, precision, and batch sizes are defined by MLPerf for each benchmark.

 4
 CoreWeave MLPerf 6.0-0020 server and offline mode. TPS/GPU is not an official MLPerf metric. It is used in this article to normalize submissions that use different numbers of GPUs.

 5
 CoreWeave MLPerf 6.0-0022 server and offline mode. TPS/GPU is not an official MLPerf metric. It is used in this article to normalize submissions that use different numbers of GPUs.

 6
 Tokens per second (TPS) per GPU is not an official MLPerf metric; however, it is used for comparison as a way of normalizing results from configurations with different numbers of GPUs.

 7
 The >2x speedup of NVIDIA GB200 NVL72 over NVIDIA H200 GPU for the Llama 3.1 405B model is measured on a per-GPU basis against NVIDIA’s MLPerf Inference v5.0 submission with 8 x NVIDIA H200 GPUs at FP8 precision, ID: 5.0-0077.

 8
 Verified MLPerf score of v5.1 Inference Closed DeepSeek R1 server. Retrieved from https://mlcommons.org/benchmarks/inference, April 2, 2025, entry 5.1-0097. The MLPerf name and logo are registered and unregistered trademarks of MLCommons Association in the United States and other countries. All rights reserved. Unauthorized use strictly prohibited. See www.mlcommons.org for more information.

 9
 Verified MLPerf score of v5.1 Inference Closed DeepSeek R1 offline. Retrieved from https://mlcommons.org/benchmarks/inference, April 2, 2025, entry 5.1-0097. The MLPerf name and logo are registered and unregistered trademarks of MLCommons Association in the United States and other countries. All rights reserved. Unauthorized use strictly prohibited. See www.mlcommons.org for more information.

 10
 Verified MLPerf score of v6.0 Inference Closed DeepSeek R1 server. Retrieved from https://mlcommons.org/benchmarks/inference, April 1, 2026, entry 6.0-0020. The MLPerf name and logo are registered and unregistered trademarks of MLCommons Association in the United States and other countries. All rights reserved. Unauthorized use strictly prohibited. See www.mlcommons.org for more information.

 11
 Verified MLPerf score of v6.0 Inference Closed DeepSeek R1 offline. Retrieved from https://mlcommons.org/benchmarks/inference, April 1, 2026, entry 6.0-0022. The MLPerf name and logo are registered and unregistered trademarks of MLCommons Association in the United States and other countries. All rights reserved. Unauthorized use strictly prohibited. See www.mlcommons.org for more information.

 12
 Verified MLPerf score of v6.0 Inference Closed DeepSeek R1 server. Retrieved from https://mlcommons.org/benchmarks/inference, April 1, 2026, entry 6.0-0022. The MLPerf name and logo are registered and unregistered trademarks of MLCommons Association in the United States and other countries. All rights reserved. Unauthorized use strictly prohibited. See www.mlcommons.org for more information.

 13
 Verified MLPerf score of v6.0 Inference Closed DeepSeek R1 offline. Retrieved from https://mlcommons.org/benchmarks/inference, April 1, 2026, entry 6.0-0022. The MLPerf name and logo are registered and unregistered trademarks of MLCommons Association in the United States and other countries. All rights reserved. Unauthorized use is strictly prohibited. See www.mlcommons.org for more information.

 14
 CoreWeave MLPerf 6.0-0021 server and offline mode. TPS/GPU is not an official MLPerf metric. It is used in this article to normalize submissions that use different numbers of GPUs.

 15
 NVIDIA GB300 NVL72, https://www.nvidia.com/en-us/data-center/gb300-nvl72/

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

GPU Compute,

Copy code

Copied!

GPU Compute,
