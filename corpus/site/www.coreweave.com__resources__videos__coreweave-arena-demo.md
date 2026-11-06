# CoreWeave ARENA Demo | CoreWeave Video

Source: https://www.coreweave.com/resources/videos/coreweave-arena-demo

Announcement

Webinar

Podcast

GTC 2026

CoreWeave Forge is here: connect your AI loop and compound every improvement. Read more

Contact us

Copied

Overview
Transcript

CoreWeave ARENA is a production-ready AI lab engineered to enable teams to move into full-scale production with confidence. In this demo, Corey Sanders walks through the CoreWeave ARENA experience, starting with gaining access to your CoreWeave ARENA environment and orienting around the guided lab workflow.
You’ll see how teams use CoreWeave ARENA to run real evaluation workflows, submit jobs, and review baseline outputs before iterating to optimize. The walkthrough also covers validating communication performance with NCCL tests on Slurm/SUNK and using CoreWeave Mission Control visibility to understand what’s happening during execution. By the end, you’ll have a practical view of how CoreWeave ARENA brings together the tools and signals needed to evaluate readiness and keep experimenting with confidence.
‍

00:00

1
00:00:04,400 --> 00:00:05,066
Hi there.
2
00:00:05,066 --> 00:00:06,200
My name is Corey Sanders
3
00:00:06,200 --> 00:00:07,366
and I'm here to give you a quick
4
00:00:07,366 --> 00:00:08,466
walkthrough on the new
5
00:00:08,466 --> 00:00:11,233
ARENA experience on the CoreWeave cloud.
6
00:00:11,233 --> 00:00:12,033
Now, it started by me
7
00:00:12,033 --> 00:00:13,433
receiving an invitation,
8
00:00:13,433 --> 00:00:14,600
from the solution architects
9
00:00:14,600 --> 00:00:15,366
at CoreWeave
10
00:00:15,366 --> 00:00:17,266
who had set up an environment for me
11
00:00:17,266 --> 00:00:19,233
to be able to do some of these tests
12
00:00:19,233 --> 00:00:21,266
and an example walkthroughs on the,
13
00:00:21,266 --> 00:00:22,800
the cloud that's been
14
00:00:22,800 --> 00:00:23,933
that's been made for me.
15
00:00:23,933 --> 00:00:25,100
And so it started with me
16
00:00:25,100 --> 00:00:26,066
to be able to log
17
00:00:26,066 --> 00:00:27,600
right in here into the console.
18
00:00:27,600 --> 00:00:28,466
And so I logged in,
19
00:00:28,466 --> 00:00:31,133
and you can see here
20
00:00:31,133 --> 00:00:32,433
I have a cluster already up and running
21
00:00:32,433 --> 00:00:33,300
that's been set up for me,
22
00:00:33,300 --> 00:00:34,066
which is lovely.
23
00:00:34,066 --> 00:00:36,866
This is a, Kubernetes cluster running
24
00:00:36,866 --> 00:00:38,633
at the CoreWeave Kubernetes Service.
25
00:00:38,633 --> 00:00:40,300
And on top of this,
26
00:00:40,300 --> 00:00:41,500
they've also set up
27
00:00:41,500 --> 00:00:43,033
a SUNK environment for me,
28
00:00:43,033 --> 00:00:43,900
which we'll go through
29
00:00:43,900 --> 00:00:44,533
a little bit later,
30
00:00:44,533 --> 00:00:46,633
which is a Slurm solution.
31
00:00:46,633 --> 00:00:48,133
It's very unique on CoreWeave
32
00:00:48,133 --> 00:00:49,300
that allows me to do
33
00:00:49,300 --> 00:00:50,466
Slurm operations
34
00:00:50,466 --> 00:00:52,900
on top of a Kubernetes based
35
00:00:52,900 --> 00:00:55,100
infrastructure environment.
36
00:00:55,100 --> 00:00:56,433
And so the only really thing
37
00:00:56,433 --> 00:00:57,200
I need to do to be able
38
00:00:57,200 --> 00:00:58,233
to get access here
39
00:00:58,233 --> 00:01:00,500
is to bring a public key
40
00:01:00,500 --> 00:01:01,800
in with the private key,
41
00:01:01,800 --> 00:01:03,200
on my local machine.
42
00:01:03,200 --> 00:01:05,066
So that I can access the environment.
43
00:01:05,066 --> 00:01:07,000
And so I've already created a key.
44
00:01:07,000 --> 00:01:09,100
And so I just want to,
45
00:01:09,100 --> 00:01:11,600
get the public key out, here.
46
00:01:11,600 --> 00:01:12,633
And so I'm going to copy
47
00:01:12,633 --> 00:01:13,233
and paste it,
48
00:01:13,233 --> 00:01:16,733
and go right back into the console.
49
00:01:16,966 --> 00:01:18,100
It's just down here.
50
00:01:18,100 --> 00:01:19,400
If I click on my name and click
51
00:01:19,400 --> 00:01:21,200
settings and scroll down,
52
00:01:21,200 --> 00:01:22,266
you can see here
53
00:01:22,266 --> 00:01:23,866
SSH Public Key for Slurm.
54
00:01:23,866 --> 00:01:26,933
Type that in save it and away I go.
55
00:01:27,200 --> 00:01:28,700
And that's it for me
56
00:01:28,700 --> 00:01:30,566
in the console for now.
57
00:01:30,566 --> 00:01:33,733
Now once I get that key up and running,
58
00:01:33,733 --> 00:01:36,800
the next big step is I could go in
59
00:01:36,800 --> 00:01:38,966
and actually SSH in to the machine,
60
00:01:38,966 --> 00:01:41,366
into the login node here for my
61
00:01:41,366 --> 00:01:42,533
for my Slurm environment.
62
00:01:42,533 --> 00:01:43,766
So here you can see I'm logged
63
00:01:43,766 --> 00:01:44,400
in, gives me
64
00:01:44,400 --> 00:01:45,433
a little bit of detail of what
65
00:01:45,433 --> 00:01:46,166
the CoreWeave Slurm
66
00:01:46,166 --> 00:01:48,066
HPC cluster looks like,
67
00:01:48,066 --> 00:01:49,500
the things that have been pre-installed
68
00:01:49,500 --> 00:01:50,300
for me and set up,
69
00:01:50,300 --> 00:01:52,366
you can sort of see I'm running here,
70
00:01:52,366 --> 00:01:53,266
but instead of actually
71
00:01:53,266 --> 00:01:54,233
doing this through SSH,
72
00:01:54,233 --> 00:01:55,366
here's what I'm going to do.
73
00:01:55,366 --> 00:01:55,800
I'm actually
74
00:01:55,800 --> 00:01:57,466
going to run this through marimo
75
00:01:57,466 --> 00:01:58,866
because it helps me understand
76
00:01:58,866 --> 00:02:00,333
what I'm doing step by step
77
00:02:00,333 --> 00:02:01,566
and actually be able to,
78
00:02:02,933 --> 00:02:03,933
run the command
79
00:02:03,933 --> 00:02:04,966
directly from that environment.
80
00:02:04,966 --> 00:02:06,666
So let me spin up a marimo
81
00:02:06,666 --> 00:02:07,566
deployment here.
82
00:02:07,566 --> 00:02:08,566
It's going to be running
83
00:02:08,566 --> 00:02:11,266
on that login node. Okay.
84
00:02:11,266 --> 00:02:13,133
And so let me just copy that
85
00:02:13,133 --> 00:02:16,133
and let me open back up into,
86
00:02:16,233 --> 00:02:17,933
my console here.
87
00:02:17,933 --> 00:02:19,466
Bingo. Bango.
88
00:02:19,466 --> 00:02:22,100
And I have my marimo environment up
89
00:02:22,100 --> 00:02:23,266
and running
90
00:02:23,266 --> 00:02:25,366
as part of my SUNK deployment
91
00:02:25,366 --> 00:02:26,566
on the CoreWeave cloud.
92
00:02:26,566 --> 00:02:27,066
Okay,
93
00:02:27,066 --> 00:02:29,800
so let me just run my prerequisites here.
94
00:02:29,800 --> 00:02:30,633
I just have to make sure
95
00:02:30,633 --> 00:02:32,366
bash execution can happen.
96
00:02:32,366 --> 00:02:34,033
And so here we are. Welcome to SUNK.
97
00:02:34,033 --> 00:02:35,733
This allows me to play
98
00:02:35,733 --> 00:02:36,700
with the environment
99
00:02:36,700 --> 00:02:37,600
for SUNK deployment
100
00:02:37,600 --> 00:02:39,000
that's been set up for me.
101
00:02:39,000 --> 00:02:40,533
Within seconds,
102
00:02:40,533 --> 00:02:42,366
you can see I'm up and running
103
00:02:42,366 --> 00:02:43,966
and ready to run some commands.
104
00:02:43,966 --> 00:02:45,733
So the first thing you know, I can see.
105
00:02:45,733 --> 00:02:47,400
Hey, what's my storage look like?
106
00:02:47,400 --> 00:02:48,866
Running these commands
107
00:02:48,866 --> 00:02:50,000
give me exactly storage
108
00:02:50,000 --> 00:02:50,833
that's been set up for me
109
00:02:50,833 --> 00:02:51,833
in the environment.
110
00:02:51,833 --> 00:02:54,933
I can see what resources do I have?
111
00:02:55,066 --> 00:02:56,566
Right. And what's the defaults here?
112
00:02:56,566 --> 00:02:57,766
So I've got the partition
113
00:02:57,766 --> 00:02:58,833
be all partition.
114
00:02:58,833 --> 00:03:01,200
And it gives me four nodes.
115
00:03:01,200 --> 00:03:02,900
These are H100s
116
00:03:02,900 --> 00:03:03,800
which will be, you know, pretty
117
00:03:03,800 --> 00:03:05,866
nice to me to run a couple of jobs on.
118
00:03:05,866 --> 00:03:07,433
And so I can even go into some details
119
00:03:07,433 --> 00:03:08,700
on those partitions
120
00:03:08,700 --> 00:03:09,333
and take a look
121
00:03:09,333 --> 00:03:11,466
and see things like default. Yes.
122
00:03:11,466 --> 00:03:13,166
And so what other other
123
00:03:13,166 --> 00:03:14,366
sort of configurations
124
00:03:14,366 --> 00:03:16,866
have been set for me ahead of time?
125
00:03:16,866 --> 00:03:17,933
And so this makes,
126
00:03:17,933 --> 00:03:19,200
of course, the running of these jobs
127
00:03:19,200 --> 00:03:20,200
so much easier.
128
00:03:20,200 --> 00:03:22,466
I'm interacting with Slurm right now.
129
00:03:22,466 --> 00:03:24,833
And so I can go in and take a deeper
130
00:03:24,833 --> 00:03:26,866
look here at some of the configuration.
131
00:03:26,866 --> 00:03:28,266
And so this is sort of one
132
00:03:28,266 --> 00:03:29,400
of the many configuration files,
133
00:03:29,400 --> 00:03:30,600
but this is a key one for Slurm.
134
00:03:30,600 --> 00:03:34,066
And so you can see things like, preempt
135
00:03:34,066 --> 00:03:35,666
type es for policy.
136
00:03:35,666 --> 00:03:37,000
So you can understand
137
00:03:37,000 --> 00:03:37,466
sort of
138
00:03:37,466 --> 00:03:38,700
what, you know,
139
00:03:38,700 --> 00:03:41,166
what's expected for preemption.
140
00:03:41,166 --> 00:03:43,833
You can, as jobs are sort of prioritized.
141
00:03:43,833 --> 00:03:45,200
A whole bunch of different settings
142
00:03:45,200 --> 00:03:45,766
and controls
143
00:03:45,766 --> 00:03:46,666
here around
144
00:03:46,666 --> 00:03:47,433
sort of how you're going
145
00:03:47,433 --> 00:03:49,033
to run your Slurm job
146
00:03:49,033 --> 00:03:49,900
on this environment.
147
00:03:49,900 --> 00:03:50,766
I'm going to leave it all
148
00:03:50,766 --> 00:03:52,966
as it has been set for me.
149
00:03:52,966 --> 00:03:55,366
But I could go in and modify, right?
150
00:03:55,366 --> 00:03:56,500
I could even create,
151
00:03:56,500 --> 00:03:58,033
you know, in my own little,
152
00:03:58,033 --> 00:03:59,833
window here and cat out,
153
00:03:59,833 --> 00:04:01,600
do it, you know, do an SSH
154
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
