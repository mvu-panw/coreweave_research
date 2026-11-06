# Grammarly Scales Real-Time Inference with vLLM | CoreWeave

Source: https://www.coreweave.com/resources/videos/how-grammarly-scales-real-time-inference-with-vllm-on-coreweave

Announcement

Webinar

Podcast

GTC 2026

CoreWeave Forge is here: connect your AI loop and compound every improvement. Read more

Contact us

Copied

Overview
Transcript

At Superhuman (formerly Grammarly), a fine-tuned language model corrects grammatical errors for millions of monthly users, served with vLLM on CoreWeave's dedicated inference. Consumer scale stresses everything: throughput, latency, correctness, and cost. This talk covers how the team pressure-tests a serving setup against those requirements, vLLM tuning, and where dedicated inference and fully managed inference platforms converge or diverge. Beyond benchmarks, the team also validates in production with A/B tests. Expect an overview of how the model works and how serving is architected at Superhuman.
Speakers: Christoph Stuber, Software Engineer - ML Platform, Grammarly

00:00

1
00:00:00,000 --> 00:00:05,800
All right.
2
00:00:05,800 --> 00:00:07,970
Let's get started.
3
00:00:07,970 --> 00:00:09,560
Yeah, thank
4
00:00:09,560 --> 00:00:12,940
you everybody for coming. My name is
5
00:00:12,940 --> 00:00:18,450
Christoph from Superhuman and today I'm
going to talk about how we onboarded
6
00:00:18,450 --> 00:00:24,760
one of our highest traffic ML model
to CoreWeave dedicated inference.
7
00:00:24,760 --> 00:00:30,560
We'll explain the challenges that we
experienced on the way and how we overcame
8
00:00:30,560 --> 00:00:35,310
them and hopefully give you some sort
of checklist and tools that may be useful
9
00:00:35,310 --> 00:00:37,600
for your own setup.
10
00:00:37,600 --> 00:00:44,640
But before we start, let me run a quick
poll. Who of you is running open
11
00:00:44,640 --> 00:00:46,520
weights models?
12
00:00:46,520 --> 00:00:52,510
All right. And who of you have like
deployed at least like a hundreds in the
13
00:00:52,510 --> 00:00:54,560
hundreds range of GPUs?
14
00:00:54,560 --> 00:00:59,780
All right. So and last question, who
15
00:00:59,780 --> 00:01:02,240
of you have ever experienced like the
16
00:01:02,240 --> 00:01:08,520
dreaded like out of capacity errors
or insufficient capacity hit the wall?
17
00:01:08,520 --> 00:01:13,880
Yeah. Yeah. OK. Yeah. Then this hopefully
this talk is for you because that was
18
00:01:13,880 --> 00:01:20,560
also one of the reasons why we
tried CoreWeave dedicated inference.
19
00:01:20,560 --> 00:01:25,920
So here's the agenda for today. First,
we'll introduce our team real quick.
20
00:01:25,920 --> 00:01:29,140
Then we'll go over the company and
21
00:01:29,140 --> 00:01:33,600
service that we want to talk about today.
22
00:01:33,600 --> 00:01:37,590
Then there will be a little bit of a
longer section about the integration and
23
00:01:37,590 --> 00:01:42,560
the challenges and the outcome. And in
the end, we'll have a quick live demo.
24
00:01:42,560 --> 00:01:48,620
All right. That's Mike is our tech lead
25
00:01:48,620 --> 00:01:52,440
manager. He's over there. Martin is
26
00:01:52,440 --> 00:01:55,290
also here. So if you
want to connect later,
27
00:01:55,290 --> 00:01:58,560
feel free to do so. And I'm Christoph.
28
00:01:58,560 --> 00:02:02,050
All right. Yeah. And our group has a
29
00:02:02,050 --> 00:02:06,550
technical ownership of around 50 machine
30
00:02:06,550 --> 00:02:12,690
learning services running up to 200,000
LLM requests per second on larger
31
00:02:12,690 --> 00:02:15,560
models where larger models
is something between
32
00:02:15,560 --> 00:02:18,560
like one and four billion at the moment.
33
00:02:18,560 --> 00:02:24,560
And we are a production focused team.
34
00:02:24,560 --> 00:02:27,200
So that means basically the precious
35
00:02:27,200 --> 00:02:31,600
customer traffic is in our hands and we
have to make sure that we keep the
36
00:02:31,600 --> 00:02:35,560
availability at like 99.99 percent.
37
00:02:35,560 --> 00:02:41,000
And to do that, we need our observability
of the metrics. We need to make sure
38
00:02:41,000 --> 00:02:47,750
that there's on-call and incident support
and yeah, basically scalability as
39
00:02:47,750 --> 00:02:48,560
mentioned in the beginning.
40
00:02:48,560 --> 00:02:53,920
This is we have to make sure there's
enough GPUs. And last but not least,
41
00:02:53,920 --> 00:02:57,140
everything should be
really cost effective,
42
00:02:57,140 --> 00:03:00,560
meaning that's throughput for the dollar.
43
00:03:00,560 --> 00:03:05,400
All right. So I think many of you may
44
00:03:05,400 --> 00:03:10,530
know Grammarly. It was even in the
45
00:03:10,530 --> 00:03:16,350
keynote and last year Grammarly acquired
46
00:03:16,350 --> 00:03:19,560
two companies that is Superhuman Mail
47
00:03:19,560 --> 00:03:23,560
and Coda and we changed our
corporate name to Superhuman.
48
00:03:23,560 --> 00:03:29,780
So that basically reflects the move from
the company from a single to a multi
49
00:03:29,780 --> 00:03:36,560
product company. And today our
suite is composed of four products.
50
00:03:36,560 --> 00:03:41,920
It's Grammarly Go,
Grammarly and Docs and Mail.
51
00:03:41,920 --> 00:03:45,140
And yeah, we're still not done
52
00:03:45,140 --> 00:03:46,560
with acquisitions.
53
00:03:46,560 --> 00:03:53,560
This year we acquired
GPTZero, ROSE and Fathom.
54
00:03:53,560 --> 00:03:55,560
Yep.
55
00:03:55,560 --> 00:03:59,560
So here's a few more
statistics about Superhuman.
56
00:03:59,560 --> 00:04:04,560
Yeah, we run like a hundred
billion plus LLM calls per week.
57
00:04:04,560 --> 00:04:07,560
That seems like a pretty
large number and I'll
58
00:04:07,560 --> 00:04:10,560
explain later where
that number comes from.
59
00:04:10,560 --> 00:04:17,560
We have 40 million daily active users
and 700 million in annual company revenue.
60
00:04:20,560 --> 00:04:25,560
All right. Any Grammarly users here?
Anybody? Oh, that's quite a few.
61
00:04:25,560 --> 00:04:30,560
Okay, cool. Yeah. Then you probably
already know the box on the right there.
62
00:04:30,560 --> 00:04:37,600
So basically that's the grammar correction
system that we have and it makes
63
00:04:37,600 --> 00:04:42,560
suggestions in your texts and suggest
like corrections for those.
64
00:04:42,560 --> 00:04:48,260
And yeah, what is also important to
understand here, this is like a proactive
65
00:04:48,260 --> 00:04:49,560
triggered LLM.
66
00:04:49,560 --> 00:04:53,950
Basically it runs all the time in
the background. It's not like you have to
67
00:04:53,950 --> 00:04:55,560
kick it off by some chat.
68
00:04:55,560 --> 00:05:00,560
It's triggered automatically.
It needs really low latency.
69
00:05:00,560 --> 00:05:04,560
So if the service is too slow,
then you can really see an A/B test.
70
00:05:04,560 --> 00:05:09,920
There is a certain maximum where the users
then are not really looking at the
71
00:05:09,920 --> 00:05:11,560
suggestions anymore.
72
00:05:11,560 --> 00:05:17,560
And as mentioned in the beginning, we
have a high number of requests per second.
73
00:05:17,560 --> 00:05:19,560
Of course, this needs to be high quality.
74
00:05:19,560 --> 00:05:24,560
And again, for this volume,
it needs to be cost efficient.
75
00:05:24,560 --> 00:05:31,600
All right. Yeah, I think
76
00:05:31,600 --> 00:05:33,140
nowadays many
77
00:05:33,140 --> 00:05:35,570
companies, they take some complex model
78
00:05:35,570 --> 00:05:41,040
and try to make it or they
go from a foundation-like
79
00:05:41,040 --> 00:05:43,560
model and do distillation and stuff.
80
00:05:43,560 --> 00:05:46,560
But we kind of went
the other way around here.
81
00:05:46,560 --> 00:05:53,600
We come from a smaller multi-model system
that was running Grammarly before and
82
00:05:53,600 --> 00:05:57,560
the system was composed
of a couple of components.
83
00:05:57,560 --> 00:06:01,560
So you see there's the input text
and there's like small language networks.
84
00:06:01,560 --> 00:06:05,520
There's NLP where there's like maybe
even some static rules in there or
85
00:06:05,520 --> 00:06:07,560
different sorts of algorithms.
86
00:06:07,560 --> 00:06:13,560
Then all of this gets aggregated
and filtered and the suggestion comes out.
87
00:06:13,560 --> 00:06:18,930
And yeah, actually a small fun fact,
Grammarly was already running transformer
88
00:06:18,930 --> 00:06:23,560
based models for text correction
before everybody had ChatGPT.
89
00:06:23,560 --> 00:06:28,560
But yeah, it looks kind
of complex and it is complex.
90
00:06:28,560 --> 00:06:32,560
And so we were looking to unify that.
91
00:06:32,560 --> 00:06:38,560
And for that we were trying out, okay,
can we do everything with a single LLM?
92
00:06:38,560 --> 00:06:42,790
And our goal was that this of course
93
00:06:42,790 --> 00:06:49,110
has to satisfy the latency cost and the
94
00:06:49,110 --> 00:06:51,560
other requirements mentioned
in the previous slide.
95
00:06:51,560 --> 00:06:55,560
And yeah, we were successful doing that.
96
00:06:55,560 --> 00:07:00,560
So we designed this
OpenAI compatible service.
97
00:07:00,560 --> 00:07:07,580
We used techniques like quantization
and speculative decoding to get it so fast
98
00:07:07,580 --> 00:07:14,300
and efficient that it's now orders of
magnitude more cost efficient than using
99
00:07:14,300 --> 00:07:16,560
the lowest priced frontier model.
100
00:07:16,560 --> 00:07:21,560
And this is also something that
you, it needs to be this way.
101
00:07:21,560 --> 00:07:28,560
Okay, here's an example of a prompt
and this hopefully easy to understand.
102
00:07:28,560 --> 00:07:31,560
You can see there's the input.
103
00:07:31,560 --> 00:07:35,560
It has a little bit of context
to the left and to the right.
104
00:07:35,560 --> 00:07:41,380
There's these edit tags and then there's
a join tag that basically tells LLM to
105
00:07:41,380 --> 00:07:48,560
do the correction and the output
is the correct output.
106
00:07:51,560 --> 00:07:55,560
All right.
107
00:07:55,560 --> 00:08:01,210
Before we decided on dedicated inference,
we had to make sure that we use a
108
00:08:01,210 --> 00:08:02,560
right abstraction layer.
109
00:08:02,560 --> 00:08:09,180
And that means basically there are,
there's a couple of like, so from left to
110
00:08:09,180 --> 00:08:12,560
right, this gets less abstract.
111
00:08:12,560 --> 00:08:17,560
And if you go to the very left, you may
have a fully managed inference service.
112
00:08:17,560 --> 00:08:23,560
So basically you upload your weights and
everything is done by the vendor, right?
113
00:08:23,560 --> 00:08:25,560
You don't know which GPU type they use.
114
00:08:25,560 --> 00:08:28,560
You don't know how many GPUs they run.
115
00:08:28,560 --> 00:08:32,700
Maybe they have some sort of in-game
currency that you have to convert to
116
00:08:32,700 --> 00:08:35,560
understand how expensive the service is.
117
00:08:35,560 --> 00:08:40,560
But yeah, if they are good,
then maybe good enough for you.
118
00:08:40,560 --> 00:08:44,560
We then went one step further right.
119
00:08:44,560 --> 00:08:48,560
The dedicated inference already
takes a couple of difficulties away.
120
00:08:48,560 --> 00:08:52,560
You don't have to manage
your cluster, your instances.
121
00:08:52,560 --> 00:08:56,560
And you can have a routing
layer in there from CoreWeave.
122
00:08:56,560 --> 00:09:03,600
It's configurable and you can configure
the inference engine and also the
123
00:09:03,600 --> 00:09:08,560
version autoscaling
and all sorts of flags.
124
00:09:08,560 --> 00:09:10,560
Then there is managed Kubernetes.
125
00:09:10,560 --> 00:09:16,560
It's also available where you have to do
the routing and inference engine yourself.
126
00:09:16,560 --> 00:09:21,440
And to the very right is a self-managed
Kubernetes, which we actually also have
127
00:09:21,440 --> 00:09:22,560
at Grammarly.
128
00:09:22,560 --> 00:09:23,560
We had it before.
129
00:09:23,560 --> 00:09:27,560
So if you don't have it, you may not
want to build it, but we had it before.
130
00:09:27,560 --> 00:09:32,560
And this is also where we did all
the testing and deployments as well.
131
00:09:32,560 --> 00:09:37,560
So we are having a mix now of the very
right column and the dedicated inference.
132
00:09:37,560 --> 00:09:41,920
All right, here's
133
00:09:41,920 --> 00:09:47,120
the integration with
134
00:09:47,120 --> 00:09:53,560
the client API where the user connects
135
00:09:53,560 --> 00:09:55,560
that goes to a Grammar source
that does all sorts of things,
136
00:09:55,560 --> 00:09:57,560
but mainly also composes the prompt.
137
00:09:57,560 --> 00:10:00,560
And that goes to a component,
the LLM load balancer.
138
00:10:00,560 --> 00:10:03,080
So that's something we developed
139
00:10:03,080 --> 00:10:06,560
internally a little
bit more on that later.
140
00:10:06,560 --> 00:10:11,880
And this can then decide if it sends it
to the in-house vLLM and Kubernetes or
141
00:10:11,880 --> 00:10:14,560
to the CoreWeave dedicated inference.
142
00:10:14,560 --> 00:10:17,560
Yeah, what do you need to do for this?
143
00:10:17,560 --> 00:10:19,560
Set up this inference gateway.
144
00:10:19,560 --> 00:10:23,560
Then you have a model deployment
and there is the object storage.
145
00:10:23,560 --> 00:10:26,280
So we built our weights pipeline that
146
00:10:26,280 --> 00:10:29,560
moves the weights into
this object storage.
147
00:10:29,560 --> 00:10:34,560
And for this deployment,
we went for a reserved capacity.
148
00:10:34,560 --> 00:10:37,560
So a fixed number of GPUs.
149
00:10:43,560 --> 00:10:50,600
And another thing you need to do before
you deploy is to test how to test the
150
00:10:50,600 --> 00:10:54,560
concurrency that you can
put on a single node.
151
00:10:54,560 --> 00:10:58,560
So basically you can choose
the GPU that you want to use.
152
00:10:58,560 --> 00:11:02,560
You take a single instance of this
and then you run a concurrency sweep.
153
00:11:02,560 --> 00:11:07,090
That means like you gradually increase
the number of requests that run
154
00:11:07,090 --> 00:11:09,560
simultaneously against this node.
155
00:11:09,560 --> 00:11:12,560
Got to make sure that you
use production like traffic.
156
00:11:12,560 --> 00:11:18,560
So if it's not matching the right
distribution, it may get less meaningful.
157
00:11:18,560 --> 00:11:23,560
And for our use case, you can see
we have this one second budget.
158
00:11:23,560 --> 00:11:28,560
So that's our maximum latency
that we were willing to tolerate.
159
00:11:28,560 --> 00:11:33,560
And yeah, you can run this for all
sorts of hardware configuration.
160
00:11:33,560 --> 00:11:37,560
You can run this for all,
iterate some flags on vLLM.
161
00:11:37,560 --> 00:11:39,560
And that's what we did.
162
00:11:42,560 --> 00:11:46,560
And yeah, this is how you
then can configure it.
163
00:11:46,560 --> 00:11:49,560
So yeah, we decided to go for Terraform.
164
00:11:49,560 --> 00:11:52,560
We like infrastructure as code.
165
00:11:52,560 --> 00:11:56,560
And here you can see that you can
choose the engine, the version.
166
00:11:56,560 --> 00:11:59,560
And then this is our configuration there.
167
00:11:59,560 --> 00:12:02,560
You can see that our
models are rather short.
168
00:12:02,560 --> 00:12:05,560
They're like a single
sentence correction model.
169
00:12:05,560 --> 00:12:09,560
So the total length is
like 768 tokens here.
170
00:12:09,560 --> 00:12:13,560
And there's a couple of changes that
increase the performance for us.
171
00:12:13,560 --> 00:12:16,800
And the main change
maybe is the speculative
172
00:12:16,800 --> 00:12:19,520
decoding for a grammar correction
173
00:12:19,520 --> 00:12:20,560
system
174
00:12:20,560 --> 00:12:25,560
where a lot of the output may be
actually repeated from the input.
175
00:12:25,560 --> 00:12:30,560
This is a very efficient
way to accelerate inference.
176
00:12:36,560 --> 00:12:37,560
All right.
177
00:12:37,560 --> 00:12:44,560
So yeah, we didn't like immediately throw
all of our production traffic there.
178
00:12:44,560 --> 00:12:51,560
So what we did is use some sort of shadow
production traffic, basically a copy
179
00:12:51,560 --> 00:12:52,560
of our traffic
180
00:12:52,560 --> 00:12:58,520
that we can gradually, slowly ramp up
and see what's happening to the dedicated
181
00:12:58,520 --> 00:12:59,560
inference system,
182
00:12:59,560 --> 00:13:00,560
if it can keep up.
183
00:13:00,560 --> 00:13:05,840
And before all of that, we also had a
small scale proof of concept to make sure
184
00:13:05,840 --> 00:13:07,560
that we understand the system.
185
00:13:10,560 --> 00:13:15,560
So what happened there, this was our
first kind of observation, is that okay,
186
00:13:16,560 --> 00:13:18,820
on the right you can
see the vLLM end-to-end
187
00:13:18,820 --> 00:13:21,140
latency and we had a vLLM running
188
00:13:21,140 --> 00:13:22,560
internally as well.
189
00:13:22,560 --> 00:13:25,560
And okay, there is like
a little bit of spikes,
190
00:13:25,560 --> 00:13:28,560
but otherwise it looks like very bored.
191
00:13:28,560 --> 00:13:31,480
And on the left side
of things, you can see that
192
00:13:31,480 --> 00:13:34,560
suddenly the system got
really, really slow.
193
00:13:34,560 --> 00:13:37,560
And so this is something
we needed to investigate.
194
00:13:40,560 --> 00:13:43,560
And the answer is basically that our
traffic is very different, right?
195
00:13:43,560 --> 00:13:48,560
I mean, many companies here,
they have like huge contacts.
196
00:13:48,560 --> 00:13:55,840
They have agents running very slowly and
197
00:13:55,840 --> 00:13:57,560
prompted, need to be manually prompted,
198
00:13:57,560 --> 00:14:00,560
low RPS per GPU node.
199
00:14:00,560 --> 00:14:01,560
And for us, it's very different.
200
00:14:01,560 --> 00:14:04,560
We have a very high number
of requests per GPU.
201
00:14:04,560 --> 00:14:06,560
Requests are really short.
202
00:14:06,560 --> 00:14:10,560
There is not so much like
usage of KV cache and so on.
203
00:14:10,560 --> 00:14:13,850
And so the, basically the relation, if
204
00:14:13,850 --> 00:14:18,710
you design your cluster of the ingress,
205
00:14:18,710 --> 00:14:24,950
like routing or authentication gateway
layer versus the inference is like
206
00:14:24,950 --> 00:14:26,560
different than other customers.
207
00:14:26,560 --> 00:14:32,560
And so the CoreWeave team helped us out
here and found like these hotspots and
208
00:14:32,560 --> 00:14:38,560
improved their auto scaling,
mainly like of the ingress layer.
209
00:14:38,560 --> 00:14:43,560
And so that helped us then a lot.
210
00:14:43,560 --> 00:14:48,560
So you can see, we had a couple
of like challenges along the way.
211
00:14:48,560 --> 00:14:51,560
There were like connection resets.
212
00:14:51,560 --> 00:14:58,830
And when we went over 80,000 RPS there,
there was another system problem, but,
213
00:14:58,830 --> 00:15:00,560
or traffic oscillations and so on.
214
00:15:00,560 --> 00:15:04,340
But in the end, you can, you can see,
we made it to our goal that we're a
215
00:15:04,340 --> 00:15:07,560
stable 100,000 RPS for a single model.
216
00:15:07,560 --> 00:15:13,560
And yeah, I put this message from ACE.
217
00:15:13,560 --> 00:15:18,560
Thank you for helping us out here.
218
00:15:18,560 --> 00:15:22,560
Apparently we are not only like a
stressful customer, at least also a little
219
00:15:22,560 --> 00:15:23,560
bit interesting.
220
00:15:23,560 --> 00:15:28,560
So he liked the challenge.
221
00:15:28,560 --> 00:15:32,560
All right.
222
00:15:32,560 --> 00:15:37,560
Internally, we also have a system to make
sure that, that everything works well.
223
00:15:37,560 --> 00:15:43,710
And that system is basically this load
balancer that can not only create like a
224
00:15:43,710 --> 00:15:46,760
shadow traffic copy of the production
225
00:15:46,760 --> 00:15:49,560
traffic, but it can also
compare the outcome.
226
00:15:49,560 --> 00:15:54,850
So we have the ability to compare like
the latency between the internal system
227
00:15:54,850 --> 00:15:56,560
and the external system.
228
00:15:56,560 --> 00:16:00,560
We can see errors and we
can also see the match rate.
229
00:16:00,560 --> 00:16:04,550
So I think everybody who's working with
LLM knows even with temperature zero
230
00:16:04,550 --> 00:16:09,550
because of batching and floating point
arithmetic and stuff, you get like not
231
00:16:09,550 --> 00:16:12,750
always a hundred percent match, but
232
00:16:12,750 --> 00:16:14,690
we can keep it under
233
00:16:14,690 --> 00:16:21,560
control like this.
234
00:16:21,560 --> 00:16:25,560
So here's a short
screenshot of that system.
235
00:16:25,560 --> 00:16:29,560
You can see the latency comparison.
236
00:16:29,560 --> 00:16:31,560
You can see the match rate.
237
00:16:31,560 --> 00:16:37,560
So we were kind of okay if it's like at
two percent is something that we expect.
238
00:16:37,560 --> 00:16:40,560
And if it goes higher than that,
you can also set an alarm.
239
00:16:40,560 --> 00:16:45,990
So we actually ran into this where
we had an external vendor where the
240
00:16:45,990 --> 00:16:48,560
configuration was strange.
241
00:16:48,560 --> 00:16:52,480
And so this, the system can
242
00:16:52,480 --> 00:16:59,560
catch that pretty effectively.
243
00:16:59,560 --> 00:17:00,560
All right.
244
00:17:00,560 --> 00:17:01,560
Yeah.
245
00:17:01,560 --> 00:17:06,560
So what did we achieve?
246
00:17:06,560 --> 00:17:10,590
So we are able to serve like a hundred
247
00:17:10,590 --> 00:17:15,560
thousand RPS stable on our GEC model.
248
00:17:15,560 --> 00:17:18,380
And we enabled true serving cloud
249
00:17:18,380 --> 00:17:22,560
diversification with
a competitive pricing.
250
00:17:22,560 --> 00:17:28,560
So, yeah, for us, it's also important
that we don't run on another.
251
00:17:28,560 --> 00:17:33,070
Or if you go to a vendor that runs on
the same cloud as you run, then maybe you
252
00:17:33,070 --> 00:17:34,560
even compete for the same GPUs.
253
00:17:34,560 --> 00:17:37,560
And he's taking your GPUs
that you want to use.
254
00:17:37,560 --> 00:17:41,560
And so that is a nice
diversification for us.
255
00:17:47,560 --> 00:17:48,560
Okay.
256
00:17:48,560 --> 00:17:52,560
There's a couple of things
that we still want to do.
257
00:17:52,560 --> 00:17:55,560
We develop our own drafter.
258
00:17:55,560 --> 00:17:57,560
So this is a specialized.
259
00:17:59,560 --> 00:18:02,190
So, yeah, what I showed
in the configuration
260
00:18:02,190 --> 00:18:04,900
before was the standard like Ngram
261
00:18:04,900 --> 00:18:08,560
GPU drafter that's
somehow included in vLLM.
262
00:18:08,560 --> 00:18:15,600
But especially for our grammar correction
model, we developed our own drafter
263
00:18:15,600 --> 00:18:20,560
that is basically able to ignore
like irrelevant parts of the prompt.
264
00:18:20,560 --> 00:18:25,560
And that knows that mostly like you
insert or delete certain tokens.
265
00:18:25,560 --> 00:18:29,560
And so it's kind
of optimized for our model.
266
00:18:29,560 --> 00:18:34,960
And now we're working together with
the dedicated inference team to see can we
267
00:18:34,960 --> 00:18:41,560
do this maybe as a vLLM plugin
or a custom Docker image.
268
00:18:41,560 --> 00:18:44,560
So there's still to do.
269
00:18:47,560 --> 00:18:48,560
Yeah.
270
00:18:48,560 --> 00:18:54,550
And then as mentioned, like the CoreWeave
deployment is basically running on
271
00:18:54,550 --> 00:18:58,560
fixed traffic like that
is static, always on.
272
00:18:58,560 --> 00:19:02,560
And then we have like our in-house
system that scales with demand.
273
00:19:02,560 --> 00:19:08,960
And we're now developing another component
that is able to do this controlling
274
00:19:08,960 --> 00:19:12,560
like a smooth and efficient as possible.
275
00:19:12,560 --> 00:19:18,490
So we always basically have most
of the traffic being served by the static
276
00:19:18,490 --> 00:19:22,560
deployment that we pay money anyway for
277
00:19:22,560 --> 00:19:26,190
and only use as little as possible for
278
00:19:26,190 --> 00:19:27,560
the elastic part.
279
00:19:36,560 --> 00:19:37,560
Right.
280
00:19:37,560 --> 00:19:38,560
Yeah.
281
00:19:38,560 --> 00:19:41,080
So as I mentioned in
the beginning, Superhuman
282
00:19:41,080 --> 00:19:43,920
has is now like like a many like
283
00:19:43,920 --> 00:19:46,560
different smaller companies inside.
284
00:19:46,560 --> 00:19:50,130
And so we're having
more and more models and
285
00:19:50,130 --> 00:19:53,560
also like models with way bigger context.
286
00:19:53,560 --> 00:19:57,310
And also where like the whole, yeah, the
287
00:19:57,310 --> 00:20:01,560
routing layer may become more interesting.
288
00:20:01,560 --> 00:20:04,560
For example, one example,
you could be superhuman mail.
289
00:20:04,560 --> 00:20:10,560
We're now looking into a model that
generates TLDR for email threads.
290
00:20:10,560 --> 00:20:15,990
And what we also want to do because,
291
00:20:15,990 --> 00:20:18,110
yeah, we always want to kind of also
292
00:20:18,110 --> 00:20:22,050
research and develop
our own deployments and
293
00:20:22,050 --> 00:20:25,560
see what we where we
can tweak performance.
294
00:20:25,560 --> 00:20:28,560
We still want to do
the managed Kubernetes.
295
00:20:28,560 --> 00:20:30,560
We want to test this out from CoreWeave.
296
00:20:30,560 --> 00:20:31,560
Yeah.
297
00:20:31,560 --> 00:20:35,560
Just to test more specialized setups.
298
00:20:42,560 --> 00:20:43,560
All right.
299
00:20:43,560 --> 00:20:45,560
We're already demo part.
300
00:20:45,560 --> 00:20:49,560
So I guess I was pretty fast again.
301
00:20:49,560 --> 00:20:53,950
So yeah, this is a little bit of redacted
302
00:20:53,950 --> 00:20:58,140
dashboard, but you can see it's a
303
00:20:58,140 --> 00:20:59,560
refreshing life.
304
00:20:59,560 --> 00:21:02,560
And this is basically one of our models.
305
00:21:02,560 --> 00:21:07,560
You can see that it runs with
like 50,000 RPS at the moment.
306
00:21:07,560 --> 00:21:11,720
And yeah, what we also liked is that,
307
00:21:11,720 --> 00:21:16,560
yeah, we can build our own Grafana board.
308
00:21:16,560 --> 00:21:19,560
So we're not like locked in by a vendor.
309
00:21:19,560 --> 00:21:20,560
Can you expose this metric?
310
00:21:20,560 --> 00:21:22,560
Can you expose that metric?
311
00:21:22,560 --> 00:21:29,560
So here you can see that we're able to
pull out all the needed metrics from vLLM.
312
00:21:29,560 --> 00:21:33,560
So that was, that is
very convenient for us.
313
00:21:33,560 --> 00:21:38,560
You can see the acceptance rate and so on.
314
00:21:38,560 --> 00:21:42,240
And yeah, here you can see the load
315
00:21:42,240 --> 00:21:47,140
balancing component that is, that I
316
00:21:47,140 --> 00:21:48,560
explained.
317
00:21:48,560 --> 00:21:51,560
So here you can see the different passes.
318
00:21:51,560 --> 00:21:58,560
You can see, for example, in our in-house
cluster, we only have about 2,000
319
00:21:58,560 --> 00:22:00,560
requests per second at the moment running.
320
00:22:00,560 --> 00:22:05,560
And on CoreWeave, yeah,
it's around 50,000.
321
00:22:05,560 --> 00:22:11,560
Here you can see me to do
a little bit of scaling.
322
00:22:11,560 --> 00:22:15,560
And here you can see the match rate.
323
00:22:15,560 --> 00:22:20,560
So this is basically input/output
matches from like a shadow fraction.
324
00:22:22,560 --> 00:22:24,560
Yeah.
325
00:22:24,560 --> 00:22:27,560
And yeah, how do you use it?
326
00:22:27,560 --> 00:22:31,560
Basically, this is the model
that we talked about.
327
00:22:31,560 --> 00:22:35,560
Basically, you can just
call the inference gateway.
328
00:22:35,560 --> 00:22:37,560
You get a model name here.
329
00:22:37,560 --> 00:22:42,560
And this is all like OpenAI compatible,
as you may know from vLLM.
330
00:22:42,560 --> 00:22:46,560
And so, yeah, here you
get your correction.
331
00:22:46,560 --> 00:22:50,560
Basically, yeah, this is how it works.
332
00:22:53,560 --> 00:22:55,560
All right.
333
00:22:59,560 --> 00:23:00,560
Yeah, thank you.
334
00:23:00,560 --> 00:23:02,560
And let me know if you have any questions.
335
00:23:04,000 --> 00:23:09,992
[Music]
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
