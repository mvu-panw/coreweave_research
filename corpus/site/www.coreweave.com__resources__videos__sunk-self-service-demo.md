# SUNK Self-Service Demo | CoreWeave Video

Source: https://www.coreweave.com/resources/videos/sunk-self-service-demo

Announcement

Webinar

Podcast

GTC 2026

CoreWeave Forge is here: connect your AI loop and compound every improvement. Read more

Contact us

Copied

Overview
Transcript

SUNK is designed for AI research teams running the most demanding training workloads—where job duration, scale, and failure tolerance make reliability and predictability as critical as raw performance. SUNK delivers a production-ready, researcher-first training system that abstracts infrastructure complexity while preserving the Slurm workflows researchers rely on. 
And now you can spin up a SUNK cluster using SUNK self-service. In just one click, researchers and platform teams can get a unified training system able to handle the most critical workloads, without the operational burden.

00:00

1
00:00:03,520 --> 00:00:06,360
Hi, I'm Deok, a PM here at CoreWeave.
2
00:00:06,520 --> 00:00:07,920
Let me tell you about some exciting
3
00:00:07,920 --> 00:00:10,080
things we're doing with SUNK.
4
00:00:10,080 --> 00:00:11,880
SUNK Self-Service
5
00:00:11,880 --> 00:00:12,920
turns spinning up
6
00:00:12,920 --> 00:00:14,040
a Slurm-on-Kubernetes
7
00:00:14,040 --> 00:00:14,640
cluster
8
00:00:14,640 --> 00:00:16,320
from a week of infrastructure
9
00:00:16,320 --> 00:00:18,200
work into a few clicks.
10
00:00:18,200 --> 00:00:19,440
With only one click,
11
00:00:19,440 --> 00:00:20,160
all your nodes
12
00:00:20,160 --> 00:00:23,240
magically flow into Slurm, IAM users get
13
00:00:23,360 --> 00:00:24,240
SSH access,
14
00:00:24,240 --> 00:00:25,000
the control plane
15
00:00:25,000 --> 00:00:26,320
is automatically right-sized
16
00:00:26,320 --> 00:00:27,240
to your needs,
17
00:00:27,240 --> 00:00:28,560
and a shared file system spans
18
00:00:28,560 --> 00:00:30,120
your whole cluster.
19
00:00:30,120 --> 00:00:31,720
One click to get a production
20
00:00:31,720 --> 00:00:33,120
research cluster.
21
00:00:33,120 --> 00:00:34,880
Users can change the default
22
00:00:34,880 --> 00:00:36,440
to fit their needs:
23
00:00:36,440 --> 00:00:37,800
You can safely manage access
24
00:00:37,800 --> 00:00:38,400
through IAM
25
00:00:38,400 --> 00:00:39,360
groups, reduce
26
00:00:39,360 --> 00:00:42,360
CPU costs by turning off login pods,
27
00:00:42,360 --> 00:00:43,520
or drop into the YAML
28
00:00:43,520 --> 00:00:45,040
for advanced configs.
29
00:00:45,040 --> 00:00:46,160
There's no helm charts,
30
00:00:46,160 --> 00:00:47,840
and there's no waiting.
31
00:00:47,840 --> 00:00:48,880
CoreWeave manages
32
00:00:48,880 --> 00:00:49,680
the end-to-end
33
00:00:49,680 --> 00:00:51,720
SUNK cluster life cycle
34
00:00:51,720 --> 00:00:54,000
with automated upgrades and patches,
35
00:00:54,000 --> 00:00:55,520
so you can get the Slurm experience
36
00:00:55,520 --> 00:00:56,680
your researchers expect
37
00:00:56,680 --> 00:00:59,360
without owning the operational burden.
38
00:00:59,360 --> 00:01:01,040
Customers can also deploy SUNK
39
00:01:01,040 --> 00:01:03,600
through a Kubernetes custom resource.
40
00:01:03,600 --> 00:01:05,600
You edit the CR directly
41
00:01:05,600 --> 00:01:07,600
for advanced workflows
42
00:01:07,600 --> 00:01:09,120
so you can change things
43
00:01:09,120 --> 00:01:10,720
like your Slurm configurations,
44
00:01:10,720 --> 00:01:12,800
QOS settings partitions.
45
00:01:12,800 --> 00:01:14,680
And because it's just a CR,
46
00:01:14,680 --> 00:01:16,360
it drops right into your existing
47
00:01:16,360 --> 00:01:17,640
GitOps workflow,
48
00:01:17,640 --> 00:01:18,760
so you can use a tool
49
00:01:18,760 --> 00:01:19,360
like Argo
50
00:01:19,360 --> 00:01:20,760
CD or whatever continuous
51
00:01:20,760 --> 00:01:22,720
delivery thing you use.
52
00:01:22,720 --> 00:01:23,720
You keep everything
53
00:01:23,720 --> 00:01:25,880
customers love about SUNK:
54
00:01:25,880 --> 00:01:27,000
the SUNK pod scheduler
55
00:01:27,000 --> 00:01:28,480
for unifying workloads
56
00:01:28,480 --> 00:01:30,600
like inference, sandboxes and training,
57
00:01:30,600 --> 00:01:32,400
in the same cluster
58
00:01:32,400 --> 00:01:34,520
driving up the utilization.
59
00:01:34,520 --> 00:01:35,520
You can also do
60
00:01:35,520 --> 00:01:36,600
the same prebuilt
61
00:01:36,600 --> 00:01:38,120
dashboards and custom metrics
62
00:01:38,120 --> 00:01:40,440
with our deep observability capabilities,
63
00:01:40,440 --> 00:01:41,280
and you get the benefit
64
00:01:41,280 --> 00:01:42,560
of the CoreWeave integration
65
00:01:42,560 --> 00:01:44,240
with health checks and burn-in tests.
66
00:01:45,240 --> 00:01:45,960
Finally, you get
67
00:01:45,960 --> 00:01:47,920
optimized job performance
68
00:01:47,920 --> 00:01:50,160
with topology aware scheduling.
69
00:01:50,160 --> 00:01:52,840
So it's the same SUNK, same scheduler
70
00:01:52,840 --> 00:01:54,360
your researchers trust,
71
00:01:54,360 --> 00:01:56,400
but now self-service
72
00:01:56,400 --> 00:01:57,960
and managed in day one.

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
