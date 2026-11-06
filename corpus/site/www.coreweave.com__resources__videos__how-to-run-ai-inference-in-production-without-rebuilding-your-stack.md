# Running Predictable Inference | CoreWeave Demo

Source: https://www.coreweave.com/resources/videos/how-to-run-ai-inference-in-production-without-rebuilding-your-stack

Announcement

Webinar

Podcast

GTC 2026

CoreWeave Forge is here: connect your AI loop and compound every improvement. Read more

Contact us

Copied

Overview
Transcript

Learn how to take AI from prototype to production using CoreWeave’s flexible inference stack—from serverless inference to BYOW (bring your own weights) and fully custom deployments on CoreWeave Kubernetes Service (CKS). This demo shows how teams maintain performance, scalability, and control across real-time and batch workloads.
‍

00:00

1
00:00:02,680 --> 00:00:03,510
Hi!
2
00:00:04,590 --> 00:00:08,700
Today, we're gonna talk about running predictable inference on CoreWeave.
3
00:00:09,980 --> 00:00:15,820
Before we talk about inference on CoreWeave, let's look at the inference landscape.
4
00:00:16,520 --> 00:00:20,519
Inference landscape is very similar to software development lifecycle.
5
00:00:20,830 --> 00:00:21,730
Where...
6
00:00:21,900 --> 00:00:32,170
You start with experimentation, most likely you will use a general-purpose proprietary model, which has least amount of control, like just access to inference hyperparameters.
7
00:00:32,630 --> 00:00:37,780
But when you start moving towards production, you want to make sure that you control the scale.
8
00:00:38,230 --> 00:00:39,799
You control the cost.
9
00:00:40,310 --> 00:00:49,299
Most likely, you will use custom models, because you want your models to be accurate and give responses very specific to your business.
10
00:00:49,640 --> 00:00:52,240
You want high amount of customization.
11
00:00:52,370 --> 00:01:00,970
Like choosing your own runtime, APIs, and you also want the most amount of control.
12
00:01:03,150 --> 00:01:09,310
CoreWeave Inference offers three products to cover the complete inference landscape.
13
00:01:10,080 --> 00:01:11,020
We have...
14
00:01:11,380 --> 00:01:24,390
Serverless inference, which enables rapid model iteration and deployment with built-in experimentation tracking, observability, and automatic scaling.
15
00:01:24,740 --> 00:01:28,019
Serverless inference is built on dedicated inference.
16
00:01:28,150 --> 00:01:43,170
Dedicated inference supports lifecycle-managed inference where customers bring their own weights, choose GPUs, and use open runtimes while Core Weave handles operations.
17
00:01:43,540 --> 00:01:50,089
Lastly, we have inference on CKS, where customers self-host models with full infrastructure control.
18
00:01:50,260 --> 00:02:09,899
They choose runtimes, frameworks like LLMD or NVIDIA Dynamo, with orchestration on CKS and full observability.
19
00:02:11,380 --> 00:02:17,350
Before we dive deeper into each service, let's walk through a multi-agent use case.
20
00:02:17,460 --> 00:02:20,219
A multi-agent research assistant.
21
00:02:21,390 --> 00:02:23,890
It's complex and involves multiple agents.
22
00:02:24,240 --> 00:02:38,169
Some agents ingest documents, others perform reasoning, and answer complex questions.
23
00:02:38,420 --> 00:02:54,240
To build such systems, you need different types of inference, including OSS models for routing and specialized models for business-specific responses.
24
00:02:54,550 --> 00:03:02,339
You may also use multimodal models for images and video understanding.
25
00:03:02,340 --> 00:03:22,030
Regardless of model type, a key requirement is OpenAI-compatible endpoints across all systems.
26
00:03:22,910 --> 00:03:27,010
Now let's explore each CoreWeave inference option.
27
00:03:27,010 --> 00:03:44,150
We’ll show how to access OSS, custom, and multimodal models using CoreWeave Inference.
28
00:04:01,220 --> 00:04:04,570
First, serverless inference.
29
00:04:04,730 --> 00:04:18,130
It enables pay-per-token inference with no infrastructure management.
30
00:04:18,209 --> 00:04:26,490
It provides auto-scaling, high availability, tracing, evals, and observability.
31
00:04:26,950 --> 00:04:33,059
It also supports custom LoRA models.
32
00:04:33,440 --> 00:04:44,239
Best suited for teams wanting SaaS simplicity with a path to deeper control.
33
00:04:44,540 --> 00:04:53,699
Ideal for engineers iterating quickly with built-in tracing and evaluation.
34
00:04:55,690 --> 00:04:57,299
Now let's look at the demo.
35
00:04:57,870 --> 00:05:09,890
Here is the Weights & Biases homepage with OpenAI-compatible APIs for inference.
36
00:05:09,940 --> 00:05:19,019
It includes a model garden where you can explore and test models.
37
00:05:19,080 --> 00:05:21,230
You can try models in a playground.
38
00:05:21,490 --> 00:05:30,080
This allows simple querying and observing responses.
39
00:05:30,350 --> 00:05:42,520
You can also view traces, call history, and inference parameters.
40
00:05:42,920 --> 00:05:49,380
Including token usage, latency, and cost.
41
00:05:50,190 --> 00:05:53,949
These are critical for experimentation.
42
00:05:54,180 --> 00:06:03,340
You can also use SDKs to query endpoints.
43
00:06:08,690 --> 00:06:22,360
Next, dedicated inference provides production-grade control.
44
00:06:24,600 --> 00:06:27,440
Deploy custom models with GPU selection and open runtimes.
45
00:06:27,600 --> 00:06:30,949
Includes auto-scaling, routing, and availability.
46
00:06:31,410 --> 00:06:44,670
Supports real-time and batch endpoints with infrastructure-aligned pricing.
47
00:06:44,900 --> 00:06:52,250
Best for teams needing control and operational transparency.
48
00:06:52,790 --> 00:07:00,769
Also suitable for enterprises with SLOs and governance needs.
49
00:07:00,940 --> 00:07:18,460
And organizations scaling multi-node inference workloads.
50
00:07:19,680 --> 00:07:23,370
Now a quick demo.
51
00:07:24,800 --> 00:07:31,430
Using a Python SDK in a notebook.
52
00:07:31,770 --> 00:07:35,250
First, check available zones.
53
00:07:35,400 --> 00:07:44,380
Then create a gateway for routing and authentication.
54
00:07:44,790 --> 00:07:51,040
Gateways manage deployments.
55
00:07:51,240 --> 00:08:01,979
Deploy models behind the gateway.
56
00:08:02,310 --> 00:08:05,990
Configure runtime, GPUs, and scaling.
57
00:08:06,120 --> 00:08:10,199
Update deployments as needed.
58
00:08:10,360 --> 00:08:18,239
All endpoints are OpenAI-compatible.
59
00:08:21,410 --> 00:08:29,890
Next, inference on CKS.
60
00:08:30,110 --> 00:08:38,960
Run distributed inference on Kubernetes with full control.
61
00:08:40,380 --> 00:09:00,000
Supports LLMD, NVIDIA Dynamo, and custom runtimes.
62
00:09:00,100 --> 00:09:08,969
Includes infrastructure tuning and network optimization.
63
00:09:09,100 --> 00:09:14,189
Best for large-scale, latency-critical workloads.
64
00:09:14,380 --> 00:09:23,059
Ideal for regulated industries like fintech and healthcare.
65
00:10:46,290 --> 00:10:56,860
Demo: deploying models via Kubernetes YAML.
66
00:10:57,080 --> 00:10:59,929
Apply configuration and run the model.
67
00:11:00,100 --> 00:11:11,959
View pods and services.
68
00:11:12,440 --> 00:11:14,660
Access via OpenAI-compatible endpoint.
69
00:12:03,800 --> 00:12:07,379
Similar process for LLMD.
70
00:12:08,990 --> 00:12:24,040
Deploy models with YAML specifying GPUs and runtime.
71
00:12:24,450 --> 00:12:30,250
Apply and run workloads.
72
00:13:04,060 --> 00:13:16,730
All services use OpenAI-compatible APIs.
73
00:13:17,330 --> 00:13:31,920
Core Weave enables easy movement between products.
74
00:13:34,390 --> 00:13:42,099
Customers include Goodfire, Perplexity, Method.ai, and others.
75
00:13:47,030 --> 00:13:48,000
Thank you.
76
00:13:49,180 --> 00:13:56,709
Access resources via the QR code.
‍

## Related videos

See all

{{ contentTypes[resource.contentType].name }}
{{ resource.title }}

{{resource.published}}{{ resource.timeToRead ? ` | ${resource.timeToRead} min read` : '' }}

██████████
███████████
█████████
█████████████
██████████

██████████
███████████
█████████
█████████████
██████████

██████████
███████████
█████████
█████████████
██████████

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
