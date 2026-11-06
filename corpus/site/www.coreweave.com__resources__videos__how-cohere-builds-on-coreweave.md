# Scaling Enterprise AI with Cohere | CoreWeave Video

Source: https://www.coreweave.com/resources/videos/how-cohere-builds-on-coreweave

Announcement

Webinar

Podcast

GTC 2026

CoreWeave Forge is here: connect your AI loop and compound every improvement. Read more

Contact us

Copied

Overview
Transcript

Cohere CEO Aidan Gomez and CTO Phil Blunsom explore why trust, security, and data sovereignty are becoming critical to enterprise AI adoption—and how the right infrastructure can help organizations move from experimentation to production.
Hear how Cohere and CoreWeave work together to accelerate training performance, adopt next-generation NVIDIA infrastructure, and operate demanding AI workloads at scale. The conversation reveals what it takes to build AI infrastructure that delivers when performance, reliability, and security are non-negotiable.

00:00

1
00:00:09,134 --> 00:00:11,094
When I speak to customers, what I hear
2
00:00:11,094 --> 00:00:13,847
is that the bottleneck isn't the model anymore.
3
00:00:13,847 --> 00:00:15,598
The models are incredibly capable.
4
00:00:15,598 --> 00:00:17,100
They can do so much more than what
5
00:00:17,100 --> 00:00:19,310
we're already using them for.
6
00:00:19,310 --> 00:00:21,646
Really, the bottleneck is in security
7
00:00:21,646 --> 00:00:23,857
and trust in the technology.
8
00:00:23,857 --> 00:00:25,900
Cohere, we're a large language model
9
00:00:25,900 --> 00:00:28,653
provider specifically focused on enterprises
10
00:00:28,653 --> 00:00:30,864
and particularly on critical industries:
11
00:00:30,864 --> 00:00:32,782
financial services, healthcare,
12
00:00:32,782 --> 00:00:34,784
telecom, the government.
13
00:00:34,784 --> 00:00:37,120
They are the bedrock of our economy
14
00:00:37,120 --> 00:00:38,371
and they have to have access to
15
00:00:38,371 --> 00:00:41,082
AI in a completely secure way.
16
00:00:41,082 --> 00:00:43,460
With Cohere, you don't need to trust us.
17
00:00:43,460 --> 00:00:45,170
So at the end of the day,
18
00:00:45,170 --> 00:00:47,172
they have sovereignty over that model.
19
00:00:47,172 --> 00:00:50,800
It's running in their their data center or their VPC.
20
00:00:50,800 --> 00:00:52,635
They control it. We can't switch it off.
21
00:00:52,635 --> 00:00:55,096
We can't see the data that's going through it.
22
00:00:55,096 --> 00:00:56,431
We've been working with
23
00:00:56,431 --> 00:00:59,392
CoreWeave for a few years now, really
24
00:00:59,392 --> 00:01:00,393
in multiple generations of models
25
00:01:00,393 --> 00:01:02,187
we've trained on CoreWeave going back to
26
00:01:02,187 --> 00:01:04,355
I think initially H100s from Nvidia
27
00:01:04,355 --> 00:01:06,024
was the first hardware generation.
28
00:01:06,024 --> 00:01:08,651
And then we've transitioned onto GB200s.
29
00:01:08,651 --> 00:01:09,569
Getting early access to
30
00:01:09,569 --> 00:01:11,154
those was crucial in terms of being able
31
00:01:11,154 --> 00:01:13,156
to accelerate our modeling programs.
32
00:01:13,156 --> 00:01:16,117
And now we're working with CoreWeave on Vera Rubin.
33
00:01:16,117 --> 00:01:18,328
AI is an extremely fast moving business.
34
00:01:18,328 --> 00:01:19,662
We're moving very fast.
35
00:01:19,662 --> 00:01:20,747
We move at startup pace,
36
00:01:20,747 --> 00:01:23,041
so expect our collaborators
37
00:01:23,041 --> 00:01:24,542
to move at startup pace, as well.
38
00:01:24,542 --> 00:01:26,211
And we find that with CoreWeave, we’re
39
00:01:26,211 --> 00:01:28,379
able to achieve some pretty incredible results.
40
00:01:28,379 --> 00:01:29,214
One of the most notable
41
00:01:29,214 --> 00:01:30,715
being tripling
42
00:01:30,715 --> 00:01:32,467
our training performance together.
43
00:01:32,467 --> 00:01:33,426
And that was in partnership
44
00:01:33,426 --> 00:01:35,053
with both CoreWeave and Nvidia
45
00:01:35,053 --> 00:01:36,554
— optimizing that training
46
00:01:36,554 --> 00:01:37,222
stack, writing
47
00:01:37,222 --> 00:01:38,348
custom kernels
48
00:01:38,348 --> 00:01:39,307
and delivering a product
49
00:01:39,307 --> 00:01:41,226
that beat everything else in the market.
50
00:01:41,226 --> 00:01:42,018
It's one thing to put
51
00:01:42,018 --> 00:01:43,937
a whole lot of GPUs in a warehouse
52
00:01:43,937 --> 00:01:44,646
and turn them on.
53
00:01:44,646 --> 00:01:45,188
It's another to
54
00:01:45,188 --> 00:01:47,107
we are able to administer them
55
00:01:47,107 --> 00:01:49,192
well in such a way that they’re reliable,
56
00:01:49,192 --> 00:01:49,859
they're robust,
57
00:01:49,859 --> 00:01:50,735
they can run
58
00:01:50,735 --> 00:01:52,028
giant training jobs
59
00:01:52,028 --> 00:01:53,196
that when they fail,
60
00:01:53,196 --> 00:01:54,280
that can be addressed
61
00:01:54,280 --> 00:01:55,615
without interrupting things.
62
00:01:55,615 --> 00:01:56,533
These clusters
63
00:01:56,533 --> 00:01:58,284
cost millions and millions to run,
64
00:01:58,284 --> 00:02:00,578
so any downtime is hugely expensive.
65
00:02:00,578 --> 00:02:02,080
What's so unique about the Cohere
66
00:02:02,080 --> 00:02:04,332
CoreWeave relationship is the pace,
67
00:02:04,332 --> 00:02:06,000
the performance and the partnership
68
00:02:06,000 --> 00:02:06,626
that we've been able
69
00:02:06,626 --> 00:02:07,836
to establish together.
70
00:02:07,836 --> 00:02:09,087
And we produce something incredible
71
00:02:09,087 --> 00:02:10,296
as a result.
72
00:02:10,296 --> 00:02:12,715
Day by day, as society depends
73
00:02:12,715 --> 00:02:14,092
more and more on AI,
74
00:02:14,092 --> 00:02:16,719
we need to ensure that we protect data,
75
00:02:16,719 --> 00:02:18,805
that we have resilient options
76
00:02:18,805 --> 00:02:21,808
and that our infrastructure is protected
77
00:02:21,933 --> 00:02:23,476
and stays up and running.
78
00:02:23,476 --> 00:02:24,769
Because at this point,
79
00:02:24,769 --> 00:02:26,771
it's becoming an essential component
80
00:02:26,771 --> 00:02:29,399
of every piece of day to day life. And.
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
