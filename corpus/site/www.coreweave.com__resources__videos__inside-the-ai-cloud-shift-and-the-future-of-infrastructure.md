# Inside the AI Cloud Shift and Future Infra | CoreWeave Video

Source: https://www.coreweave.com/resources/videos/inside-the-ai-cloud-shift-and-the-future-of-infrastructure

Announcement

Webinar

Podcast

GTC 2026

CoreWeave Forge is here: connect your AI loop and compound every improvement. Read more

Contact us

Copied

Overview
Transcript

Part of the Who’s Ready for Anything series, this episode features CoreWeave’s Chen Goldberg at NVIDIA GTC 2026. Learn how AI is reshaping the cloud from the ground up and what it takes to move from experimentation to production.
In this video:
- Why the shift from experimentation to production is defining the next phase of AI
- How AI workloads are changing requirements for compute, storage, and networking
- What makes an AI-native cloud different from traditional cloud models
- Why speed of experimentation drives innovation and competitive advantage

00:00

1
00:00:12,346 --> 00:00:13,192
Hey, everyone.
2
00:00:13,192 --> 00:00:16,192
Welcome to the AI Cloud Essentials podcast.
3
00:00:16,462 --> 00:00:18,731
I'm Lisa Martin, your host for the next couple of days.
4
00:00:18,731 --> 00:00:21,808
We are live at GTC. This is day 2.
5
00:00:22,115 --> 00:00:24,808
We are in, as you can see behind me, the buzz of the event,
6
00:00:24,808 --> 00:00:27,808
This gives you a little bit of a glimpse of the energy at GTC.
7
00:00:28,154 --> 00:00:31,500
It is electric. I’m so thrilled to be joined by Chen Goldberg.
8
00:00:31,769 --> 00:00:34,654
She's the EVP of Product & Engineering at CoreWeave.
9
00:00:34,654 --> 00:00:36,462
We're going to be talking to you a little bit about what
10
00:00:36,462 --> 00:00:38,000
Chen has been talking about with the audience,
11
00:00:38,000 --> 00:00:39,462
what she’s been hearing.
12
00:00:39,462 --> 00:00:43,231
and the overall partnership with NVIDIA and CoreWeave.
13
00:00:43,500 --> 00:00:45,038
Chen it's so great to have you on the podcast.
14
00:00:45,038 --> 00:00:46,154
Thank you so much for having me.
15
00:00:46,154 --> 00:00:47,308
Thank you so much for having me.
16
00:00:47,308 --> 00:00:48,308
So this is Day 2. Yes.
17
00:00:48,308 --> 00:00:51,731
Ane the energy yesterday was off the charts.
18
00:00:52,654 --> 00:00:56,231
People were describing this is the AI Super Bowl,
19
00:00:56,385 --> 00:00:59,038
the heartbeat of AI. Tell me a little bit...
20
00:00:59,038 --> 00:01:01,692
You were on stage with Corey yesterday.
21
00:01:01,692 --> 00:01:05,000
What were some of the things that you were sharing, and what stuck out to you
22
00:01:05,000 --> 00:01:08,231
in terms of what the audience is really absorbing.
23
00:01:08,577 --> 00:01:10,692
So this is, for me, the second time as part of CoreWeave
24
00:01:10,692 --> 00:01:12,846
that we are presenting at GTC.
25
00:01:13,423 --> 00:01:15,769
And the big change, right.
26
00:01:15,769 --> 00:01:18,038
If you think about last year,
27
00:01:18,038 --> 00:01:19,692
there was a lot of uncertainty.
28
00:01:19,692 --> 00:01:21,462
Things around, like how inference would be.
29
00:01:21,500 --> 00:01:22,615
What would be the size of the models.
30
00:01:22,615 --> 00:01:26,192
Can you create applications with AI?
31
00:01:26,692 --> 00:01:28,538
And what we’ve seen over the past
32
00:01:28,538 --> 00:01:30,423
12 months has been mind blowing.
33
00:01:30,654 --> 00:01:32,808
And everybody that is here noticed that.
34
00:01:32,808 --> 00:01:35,808
And I think that's from our perspective, the most exciting thing
35
00:01:36,115 --> 00:01:41,269
is that we, instead of just talking about basic education,
36
00:01:41,500 --> 00:01:45,385
we're talking about how can you move from experimentation to production?
37
00:01:45,692 --> 00:01:46,808
What do you need to do?
38
00:01:46,808 --> 00:01:48,808
How do you bring folks onboard?
39
00:01:48,808 --> 00:01:50,615
As an engineering leader,
40
00:01:50,615 --> 00:01:54,654
there's also a lot of conversation of productivity and the tools you are using.
41
00:01:54,692 --> 00:01:55,462
There are so many things
42
00:01:55,462 --> 00:01:59,192
that have changed over these 12 months, and that's really amazing.
43
00:01:59,385 --> 00:02:03,231
You speaking... I mean, in AI we speak of like six month,
44
00:02:03,269 --> 00:02:06,462
three month, 12 month timeframes,
45
00:02:06,462 --> 00:02:08,115
because it is moving...
46
00:02:08,115 --> 00:02:09,692
I can't even I can't describe the speed. It's amazing.
47
00:02:09,692 --> 00:02:14,308
But yesterday in Jensen's keynote was NVIDIA [heart] CoreWeave.
48
00:02:14,308 --> 00:02:15,731
Yes.
49
00:02:15,731 --> 00:02:17,115
I got chills just seeing that.
50
00:02:17,115 --> 00:02:19,731
And then when Jensen came by the booth,
51
00:02:19,731 --> 00:02:21,154
I heard him say to you and the leaders,
52
00:02:21,154 --> 00:02:22,538
just very genuine things.
53
00:02:22,538 --> 00:02:26,115
Talk about the expansion, the deepening of the NVIDIA CoreWeave
54
00:02:26,115 --> 00:02:28,115
relationship and what that will enable customers
55
00:02:28,115 --> 00:02:31,615
to do to get from what you said, experimentation to production.
56
00:02:32,731 --> 00:02:35,577
That was definitely a very special moment for us, as well.
57
00:02:35,577 --> 00:02:39,154
And we we thank Jensen for that.
58
00:02:39,154 --> 00:02:41,423
Because it was a recognition of the hard work that
59
00:02:41,423 --> 00:02:43,692
the entire CoreWeave team and our customers
60
00:02:43,692 --> 00:02:45,577
and the partners and and everybody that trusted in us,
61
00:02:45,577 --> 00:02:50,615
went through because, know...
62
00:02:50,615 --> 00:02:57,269
Everybody thinks of us as, like, a GPU reseller.
63
00:02:57,269 --> 00:03:00,038
And then recognition that we are leading in this space
64
00:03:00,038 --> 00:03:02,731
and being the AI cloud, was amazing.
65
00:03:03,115 --> 00:03:05,846
And really candidly,
66
00:03:05,846 --> 00:03:10,077
NVIDIA has been an amazing partner customer.
67
00:03:10,231 --> 00:03:12,885
And we are their customer, as well.
68
00:03:12,885 --> 00:03:16,192
And I would say that there are like a couple of things
69
00:03:16,192 --> 00:03:19,000
that really work well, between our two companies.
70
00:03:19,000 --> 00:03:22,692
One, we are really leaning in.
71
00:03:22,692 --> 00:03:24,846
Okay. We we believe in AI.
72
00:03:24,846 --> 00:03:26,885
We have a very similar vision.
73
00:03:26,885 --> 00:03:29,077
And that's really helping.
74
00:03:29,077 --> 00:03:31,538
We are really focused on customers together.
75
00:03:31,538 --> 00:03:33,808
The second thing that I think is really critical,
76
00:03:33,808 --> 00:03:36,808
you know, we talk about how our customers want to experiment.
77
00:03:37,077 --> 00:03:38,769
We like to experiment.
78
00:03:38,769 --> 00:03:40,269
Okay. I think all of us as people,
79
00:03:40,269 --> 00:03:42,692
we need to be humble and knowing like, hey, we're not great at
80
00:03:42,692 --> 00:03:43,692
predicting the future.
81
00:03:44,808 --> 00:03:45,846
But if we experiment and we see signals
82
00:03:45,846 --> 00:03:49,808
and we move fast, we get to great results.
83
00:03:49,808 --> 00:03:52,808
And NVIDIA also has that kind of culture.
84
00:03:53,192 --> 00:03:57,308
And we are both really wanting to build the best products.
85
00:03:57,846 --> 00:04:00,115
And that's actually what led, you know
86
00:04:00,115 --> 00:04:02,692
we had a big announcement last month.
87
00:04:02,692 --> 00:04:07,231
And you know the media definitely got the investment part,
88
00:04:07,500 --> 00:04:09,154
the billion dollar amount.
89
00:04:09,154 --> 00:04:12,269
But there were more things there that made me really excited.
90
00:04:12,269 --> 00:04:13,654
Tell me.
91
00:04:14,038 --> 00:04:16,615
You know, one thing was, of course, us using
92
00:04:16,615 --> 00:04:21,231
CPUs now from so Jensen in his keynote, he talked about expanding new platforms,
93
00:04:21,231 --> 00:04:24,192
so expanding from just GPUs to also CPU.
94
00:04:24,192 --> 00:04:27,692
And the other thing that we were really excited about is two things.
95
00:04:27,692 --> 00:04:30,038
One is the collaboration.
96
00:04:30,038 --> 00:04:33,769
It was actually telling the world how our teams have been collaborating
97
00:04:34,154 --> 00:04:37,308
on producing reference architecture and improving products.
98
00:04:38,000 --> 00:04:39,077
So that was one part.
99
00:04:39,077 --> 00:04:41,192
And the second part was really about us.
100
00:04:42,269 --> 00:04:45,346
Getting into the world and offering our services
101
00:04:45,346 --> 00:04:47,192
and our software to other people
102
00:04:47,462 --> 00:04:50,462
in the industry outside of even CoreWeave cloud.
103
00:04:50,577 --> 00:04:52,692
We started that with the acquisition we made
104
00:04:52,692 --> 00:04:55,077
with Weights and Biases, which is already a multi-cloud.
105
00:04:55,077 --> 00:04:58,654
But having more and more cross-cloud cloud solutions
106
00:04:58,654 --> 00:05:01,038
is something that, we plan to invest more in.
107
00:05:01,346 --> 00:05:02,577
And that's what customers are demanding.
108
00:05:02,577 --> 00:05:03,846
You talked about, basically the customer obsession
109
00:05:03,846 --> 00:05:08,385
and that symbiosis that you share with NVIDIA.
110
00:05:08,385 --> 00:05:10,692
You said something yesterday on LinkedIn, I stalked you.
111
00:05:10,692 --> 00:05:12,154
And I wanted to get your thoughts behind it.
112
00:05:12,154 --> 00:05:13,538
You were speaking with Corey.
113
00:05:13,538 --> 00:05:15,385
And you said, GTC this year 2026
114
00:05:15,385 --> 00:05:18,385
is about the next great leap.
115
00:05:18,385 --> 00:05:21,692
Tokens powering robots,
116
00:05:21,692 --> 00:05:23,500
energy grids, scientific discovery.
117
00:05:23,500 --> 00:05:24,885
I love that.
118
00:05:24,885 --> 00:05:27,846
You said, that leap needs a factory behind it.
119
00:05:27,846 --> 00:05:29,308
Talk about how NVIDIA is that factory,
120
00:05:29,462 --> 00:05:32,462
and how CoreWeave is an enabler of that.
121
00:05:32,692 --> 00:05:36,577
Back again, this year what Jensen was talking on stage,
122
00:05:36,577 --> 00:05:39,500
and also what we hear from people around us,
123
00:05:39,500 --> 00:05:44,231
is that in most companies,
124
00:05:44,231 --> 00:05:47,654
because the tools, by the way, have gotten so great
125
00:05:47,654 --> 00:05:49,462
they start seeing value.
126
00:05:49,462 --> 00:05:52,192
Yesterday on stage we had, for example,
127
00:05:52,192 --> 00:05:53,615
a person from Mercado Libre.
128
00:05:54,077 --> 00:05:56,077
So Sebastian from Mercado Libre,
129
00:05:56,077 --> 00:05:58,038
he joined us and he was telling
130
00:05:58,038 --> 00:06:01,038
the audience how they are planning to
131
00:06:01,846 --> 00:06:05,000
re imagine their search capabilities
132
00:06:05,000 --> 00:06:06,385
in their e-commerce platform.
133
00:06:06,385 --> 00:06:10,000
But even before doing that, he was talking about how even with
134
00:06:10,000 --> 00:06:13,885
small experimentation, they've been getting amazing results already.
135
00:06:14,654 --> 00:06:16,000
And what I love about it is,
136
00:06:16,000 --> 00:06:18,885
you know, like downstairs we have like a physical AI demo.
137
00:06:19,192 --> 00:06:22,192
So you see in different industry, whether it's health
138
00:06:22,500 --> 00:06:24,885
finance, e-commerce,
139
00:06:24,885 --> 00:06:29,077
media, a lot of areas where we see
140
00:06:29,577 --> 00:06:33,346
starting for a small experimentation to bigger opportunities.
141
00:06:34,038 --> 00:06:37,192
And that's really what NVIDIA is talking about.
142
00:06:37,192 --> 00:06:40,308
And part of what I think NVIDIA again, was really highlighting, Jensen
143
00:06:40,308 --> 00:06:44,385
was highlighting yesterday, that it's not just NVIDIA on its own.
144
00:06:44,808 --> 00:06:48,538
Jensen has been really investing in building an ecosystem.
145
00:06:49,308 --> 00:06:52,154
And I really appreciate that.
146
00:06:52,154 --> 00:06:55,000
I was actually part of the cloud
147
00:06:55,000 --> 00:06:59,077
transformation in the industry and the ecosystem was key to that.
148
00:06:59,462 --> 00:07:02,462
And I think Jensen is definitely recognizing
149
00:07:02,731 --> 00:07:05,731
and we are participating across the board,
150
00:07:06,000 --> 00:07:08,808
from developer tools to researcher tools
151
00:07:08,808 --> 00:07:13,000
to applications to infrastructure and just building
152
00:07:13,000 --> 00:07:16,846
that momentum, that flywheel, it creates that innovation.
153
00:07:16,885 --> 00:07:20,654
Yes. Well, the validation, the recognition you’re talking about
154
00:07:20,654 --> 00:07:22,308
from Jensen, but also to your point,
155
00:07:22,308 --> 00:07:24,808
And I talked about this on TV all the time,
156
00:07:24,808 --> 00:07:26,846
NVIDIA is not doing this alone.
157
00:07:26,846 --> 00:07:28,731
They are synonymous with AI.
158
00:07:28,731 --> 00:07:31,154
Even people locally around here that are Uber drivers
159
00:07:31,154 --> 00:07:33,000
drivers are asking me, they know AI. They see Jensen and the know AI.
160
00:07:33,000 --> 00:07:34,500
They see Jensen, AI.
161
00:07:34,500 --> 00:07:36,385
But it's the ecosystem
162
00:07:36,385 --> 00:07:39,462
and NVIDIA seems to really respect that and acknowledge it,
163
00:07:39,462 --> 00:07:42,769
obviously, with the NVIDIA [heart] CoreWeave.
164
00:07:42,769 --> 00:07:46,692
But in terms of like differentiation, there's a lot of a lot of companies here.
165
00:07:47,269 --> 00:07:51,192
The energy at this conference, I've been to a lot of them as you, is next level.
166
00:07:51,192 --> 00:07:53,769
but there's a lot of, I don't want to say me, too.
167
00:07:53,769 --> 00:07:56,423
But a lot of people saying, we’re the AI cloud.
168
00:07:56,423 --> 00:07:59,192
What makes CoreWeave really stand out
169
00:07:59,192 --> 00:08:03,154
as the essential cloud for AI in 2026 and beyond?
170
00:08:04,577 --> 00:08:05,808
I I think that a year ago
171
00:08:05,808 --> 00:08:08,769
people were not true, that we need an AI cloud.
172
00:08:09,115 --> 00:08:12,500
But now folks, that once they are trying to experiment more,
173
00:08:12,538 --> 00:08:14,077
they see there is a need.
174
00:08:14,077 --> 00:08:17,423
And one of the things, you know, and maybe I can tell you why I joined call wave.
175
00:08:17,654 --> 00:08:21,500
So before Call wave, I was part of Google Cloud and working,
176
00:08:21,500 --> 00:08:24,577
on building that cloud native ecosystem.
177
00:08:25,385 --> 00:08:28,385
And back at the day
178
00:08:28,462 --> 00:08:31,808
when we talked about the value of the cloud,
179
00:08:32,308 --> 00:08:35,077
it wasn't just enough to move to the cloud, right?
180
00:08:35,077 --> 00:08:36,269
The lift and shift.
181
00:08:36,269 --> 00:08:38,000
There was a change of ecosystem.
182
00:08:38,000 --> 00:08:39,269
You had to change the way you do tooling,
183
00:08:39,269 --> 00:08:41,538
how you develop, how you deploy, how you manage.
184
00:08:42,538 --> 00:08:44,077
And when I started
185
00:08:44,077 --> 00:08:47,500
experimenting and experiencing more of these new type of workloads,
186
00:08:48,500 --> 00:08:51,500
it felt similar, but actually a much bigger,
187
00:08:51,769 --> 00:08:54,769
opportunity to reimagine how cloud should look like.
188
00:08:55,154 --> 00:08:58,115
And I think that's the most unique thing about CoreWeave.
189
00:08:58,462 --> 00:09:01,000
And that from the get go, right,
190
00:09:01,000 --> 00:09:04,077
if you talk with the founders, that's what they were trying to do.
191
00:09:04,231 --> 00:09:09,731
It was not like me to, Peter, our CTO, they took a step back and said,
192
00:09:09,731 --> 00:09:12,692
like, okay, what are the hard problems we need to solve?
193
00:09:12,846 --> 00:09:15,192
They didn't just look at the other reference architecture.
194
00:09:15,192 --> 00:09:17,038
They actually build from scratch.
195
00:09:17,038 --> 00:09:20,077
And there are some things that we are doing very differently
196
00:09:20,308 --> 00:09:23,308
than others, and that's what really delivered the results.
197
00:09:23,808 --> 00:09:27,346
I think the way that you I, I think it's easy to understand
198
00:09:27,346 --> 00:09:30,346
there are like probably three categories that we are doing differently.
199
00:09:30,500 --> 00:09:33,423
The first one is that we are,
200
00:09:34,885 --> 00:09:37,885
started with a vertically integrated stack.
201
00:09:38,000 --> 00:09:38,346
Okay.
202
00:09:38,346 --> 00:09:38,731
You now
203
00:09:38,731 --> 00:09:42,231
see some of the folks announcing it, but it's like they're trying to retrofit
204
00:09:42,615 --> 00:09:45,885
that vertical integration was a huge difference.
205
00:09:47,308 --> 00:09:50,308
What we are doing, we understand the complexity of the stack
206
00:09:51,385 --> 00:09:52,385
is huge.
207
00:09:52,385 --> 00:09:55,885
And in order to manage that, you need to allow flexibility
208
00:09:55,885 --> 00:10:00,115
and quick decisions across the stack and knowing how to react to events
209
00:10:00,654 --> 00:10:01,423
lower in the stack.
210
00:10:01,423 --> 00:10:06,346
So we like saying from metal to model, from metal to job.
211
00:10:07,077 --> 00:10:07,500
And right.
212
00:10:07,500 --> 00:10:12,038
Bringing all of that information and really creating a new way to operate
213
00:10:12,654 --> 00:10:15,192
a cloud stack in the AI era,
214
00:10:15,192 --> 00:10:18,577
we differentiate we think capabilities like mission control
215
00:10:18,846 --> 00:10:22,615
that are both reactive and proactive in solving customer problems.
216
00:10:22,615 --> 00:10:23,885
So that would be one.
217
00:10:23,885 --> 00:10:27,538
The second part that even though we were thinking about an integrated stack,
218
00:10:28,115 --> 00:10:32,577
we are still looking for opportunities to optimize specific problems
219
00:10:32,577 --> 00:10:35,231
or bottlenecks. And again, we don't try to solve for everything.
220
00:10:35,231 --> 00:10:37,192
We are really, really focused.
221
00:10:37,192 --> 00:10:41,154
So if you think about AI workloads, and one of the challenges is
222
00:10:41,462 --> 00:10:45,346
you want to make sure the GPUs are, with high utilization.
223
00:10:45,346 --> 00:10:49,115
They are very expensive, very important resource.
224
00:10:49,423 --> 00:10:53,308
So we are building, for example, specific solutions that will bring more data
225
00:10:53,808 --> 00:10:57,192
into the GPU with our own distributed caching mechanism, or
226
00:10:57,731 --> 00:11:01,423
building a new solution for orchestration of workloads,
227
00:11:01,654 --> 00:11:05,231
for example, again, for the technical audience folks here that are familiar
228
00:11:05,231 --> 00:11:09,423
with Slurm, Slurm is a known
229
00:11:10,885 --> 00:11:13,038
industry standard for,
230
00:11:13,038 --> 00:11:16,038
HP workloads, high performing workloads.
231
00:11:16,423 --> 00:11:18,808
But what we've done, we created a solution that bring
232
00:11:18,808 --> 00:11:21,808
those workloads into the cloud native era.
233
00:11:22,269 --> 00:11:26,654
And the last point, which maybe that's really brings us back to where we started.
234
00:11:27,231 --> 00:11:30,885
We know when we talk with our customers that speed of experimentation
235
00:11:31,192 --> 00:11:33,115
is the most important thing.
236
00:11:33,115 --> 00:11:36,115
And I'm a believer that we cannot predict the future.
237
00:11:36,692 --> 00:11:40,654
So how can we increase the signals that people see?
238
00:11:41,000 --> 00:11:44,385
Okay, how quickly can I experiment, iterate and see what I need to go?
239
00:11:44,769 --> 00:11:48,538
And so we have a lot of investment on that, both from an infrastructure
240
00:11:48,538 --> 00:11:52,192
perspective but also on tunings, like we said, W and B models.
241
00:11:52,192 --> 00:11:56,462
And we've just giving those signals that allow our customers
242
00:11:56,462 --> 00:12:00,308
to make decisions faster and with confidence.
243
00:12:00,654 --> 00:12:03,000
That's the key word is confidence.
244
00:12:03,000 --> 00:12:04,808
Yeah. Because the speed is just
245
00:12:05,846 --> 00:12:07,192
not going to slow down.
246
00:12:07,192 --> 00:12:07,885
What do you think you said
247
00:12:07,885 --> 00:12:11,308
when we were preparing for this conversation was it's not just meetings.
248
00:12:12,000 --> 00:12:12,577
Yeah.
249
00:12:12,577 --> 00:12:16,423
So walk me through the steps of for each stack started to allude to it
250
00:12:17,038 --> 00:12:21,346
in a part for the technical side and explain where the differentiation lies
251
00:12:21,538 --> 00:12:24,500
and where are you really enabling customers to build
252
00:12:24,500 --> 00:12:28,269
the AI infrastructure from scratch to power?
253
00:12:28,308 --> 00:12:31,115
Awesome, and thank you so much for asking it.
254
00:12:31,115 --> 00:12:33,654
I think that we are using a lot of jargon all the time,
255
00:12:33,654 --> 00:12:35,423
and people don't always understand.
256
00:12:35,423 --> 00:12:37,538
What does it actually mean to build a cloud?
257
00:12:37,538 --> 00:12:39,269
How does it look like?
258
00:12:39,269 --> 00:12:42,769
And so first of all, there is of course the physical infrastructure.
259
00:12:43,231 --> 00:12:43,654
Okay.
260
00:12:43,654 --> 00:12:48,692
And there is already just on that layer, there's a lot of new challenges
261
00:12:48,885 --> 00:12:52,692
that appear in the AI era from a lot of power
262
00:12:52,692 --> 00:12:55,692
consumption, cooling needs.
263
00:12:56,115 --> 00:12:59,115
And there's a lot of work that our team is doing,
264
00:12:59,500 --> 00:13:02,423
around, power efficiency,
265
00:13:02,423 --> 00:13:07,538
space, liquid cooling, and just making sure that we build and,
266
00:13:07,538 --> 00:13:12,385
of course, security, across the stack, that we innovate in that space.
267
00:13:12,692 --> 00:13:16,808
But then on top of that, there is actually a different layers of the stack.
268
00:13:17,077 --> 00:13:20,692
You know, when we say infrastructure, we should all think about,
269
00:13:21,654 --> 00:13:23,654
starting with what we call infrastructure as a service.
270
00:13:23,654 --> 00:13:26,846
Very simple compute, storage and network.
271
00:13:26,846 --> 00:13:27,538
Right.
272
00:13:27,538 --> 00:13:31,000
What's been very interesting, when you move from the cloud 1.0
273
00:13:31,192 --> 00:13:34,192
to cloud 2.0, is that
274
00:13:35,077 --> 00:13:39,269
in the cloud 1.0 ERA, the goal was to make
275
00:13:39,538 --> 00:13:43,115
infrastructure, specifically compute, storage and network boring.
276
00:13:43,808 --> 00:13:44,808
Okay, okay, okay.
277
00:13:44,808 --> 00:13:48,808
I'm as a developer, as a business owner, I should know I think about it. Yes.
278
00:13:48,808 --> 00:13:50,308
Should not care about that. And. Right.
279
00:13:50,308 --> 00:13:52,385
And that's been my journey.
280
00:13:52,385 --> 00:13:54,615
In the industry making that
281
00:13:54,615 --> 00:13:57,615
a reality with technologies like Kubernetes.
282
00:13:57,769 --> 00:14:01,115
Make it make it invisible, make the infrastructure boring.
283
00:14:01,115 --> 00:14:02,731
You can you can like Google that.
284
00:14:02,731 --> 00:14:05,615
And you will see like those kind of quotes.
285
00:14:05,615 --> 00:14:08,385
And I think we've actually done a great job,
286
00:14:08,385 --> 00:14:11,115
in the industry of creating technologies that have done that.
287
00:14:11,115 --> 00:14:11,808
However,
288
00:14:13,192 --> 00:14:15,654
what's happening right now, and that's exactly what Jensen
289
00:14:15,654 --> 00:14:20,115
was talking about yesterday, is that the workloads, the applications,
290
00:14:21,538 --> 00:14:24,538
they care about, the compute storage network,
291
00:14:25,654 --> 00:14:27,038
okay, because
292
00:14:27,038 --> 00:14:30,385
the amount of data that has to go on the network is impacting the latency.
293
00:14:30,423 --> 00:14:33,423
And now let's say I have an agent,
294
00:14:33,654 --> 00:14:36,500
this is no longer it can be a mission
295
00:14:36,500 --> 00:14:40,000
critical workload that we need someone to immediately respond.
296
00:14:40,000 --> 00:14:43,000
Or if we have video generation, right, it cannot be lagging.
297
00:14:43,308 --> 00:14:46,500
And you think about storage, how quickly can I scale?
298
00:14:46,769 --> 00:14:48,846
How do I get the data, how quickly can I load things?
299
00:14:48,846 --> 00:14:52,808
And from a compute perspective, not only
300
00:14:52,808 --> 00:14:56,654
I want to get the best utilization, we actually have lots of workloads.
301
00:14:56,654 --> 00:14:59,154
I have models that are now running
302
00:14:59,154 --> 00:14:59,577
not on a
303
00:14:59,577 --> 00:15:01,000
one node or ten nodes,
304
00:15:01,000 --> 00:15:04,000
but sometimes ten thousands of nodes.
305
00:15:04,154 --> 00:15:07,308
And that's creates a lot of, complexity in that stack.
306
00:15:07,308 --> 00:15:10,154
And we are been innovating in that area area.
307
00:15:10,154 --> 00:15:11,269
And then on top of this
308
00:15:12,385 --> 00:15:13,269
we have
309
00:15:13,269 --> 00:15:16,192
a new inference services and training services.
310
00:15:16,192 --> 00:15:16,346
Right.
311
00:15:16,346 --> 00:15:21,231
Because as a developer, I have new tasks that I need to perform.
312
00:15:21,423 --> 00:15:24,231
So I need new tools and new ecosystem.
313
00:15:24,231 --> 00:15:25,192
And maybe on top of that,
314
00:15:25,192 --> 00:15:28,885
I think the things that really excites me the most is our entire what we call our,
315
00:15:29,808 --> 00:15:32,231
you know, when we think about serverless, it's not about making
316
00:15:32,231 --> 00:15:35,231
the infrastructure boring.
317
00:15:35,462 --> 00:15:37,885
But helping our customers
318
00:15:37,885 --> 00:15:40,846
rely on us in making some of those decisions.
319
00:15:41,115 --> 00:15:44,115
So one of the things that I'm really excited about is,
320
00:15:44,462 --> 00:15:48,000
the tools that we are providing, it's like what we call that serverless layer,
321
00:15:48,000 --> 00:15:51,231
where we are not trying to really make the infrastructure disappear,
322
00:15:51,769 --> 00:15:55,654
but we're trying to help customers, to rely on us.
323
00:15:56,231 --> 00:15:56,500
Okay.
324
00:15:56,500 --> 00:16:00,385
And lets us do the heavy lifting in making those tough decisions.
325
00:16:01,038 --> 00:16:04,308
And we've been announcing this week and you,
326
00:16:04,308 --> 00:16:07,846
tool in our serverless RL, which is a reinforcement learning.
327
00:16:08,269 --> 00:16:11,731
And in that space, if before a lot of this experimentation
328
00:16:12,038 --> 00:16:16,269
required simulation data, now we are allowing customers to use production
329
00:16:16,269 --> 00:16:21,000
tracing in order to train the agents to get better automatically.
330
00:16:21,346 --> 00:16:24,038
So that would be one example of a token production.
331
00:16:24,038 --> 00:16:25,731
Yes. In production.
332
00:16:25,731 --> 00:16:28,231
Oh, for example, we have a new customer, Klein,
333
00:16:28,231 --> 00:16:29,577
that they are using our inference service.
334
00:16:29,577 --> 00:16:32,577
So they are a customer, a partner as well.
335
00:16:32,846 --> 00:16:33,654
And they are
336
00:16:34,808 --> 00:16:37,192
actually building a coding solution
337
00:16:37,192 --> 00:16:40,192
that allows them to leverage our platform.
338
00:16:40,500 --> 00:16:42,115
Maybe, you know, you asked about differentiation.
339
00:16:42,115 --> 00:16:43,769
I should have led with that.
340
00:16:43,769 --> 00:16:47,269
And we offer all this new stuff
341
00:16:48,000 --> 00:16:52,462
without compromising security and resiliency and production ready.
342
00:16:52,846 --> 00:16:55,269
And we take a lot of pride in that.
343
00:16:55,269 --> 00:16:58,346
And that's like, actually would be probably the number one reason
344
00:16:58,346 --> 00:16:59,731
why customers come to us.
345
00:16:59,731 --> 00:17:03,269
And second last question, what you talk about some of the challenges
346
00:17:03,269 --> 00:17:08,423
customers have, technical challenges, power, tooling, space, capacity.
347
00:17:09,077 --> 00:17:13,115
What are some of the business challenges that you're proud to for me, to help
348
00:17:13,154 --> 00:17:16,154
such customers eliminate,
349
00:17:16,577 --> 00:17:17,885
don't. There are many challenges.
350
00:17:17,885 --> 00:17:22,231
And, you know, like, we were just say I had a customer meeting, today
351
00:17:22,538 --> 00:17:25,308
and they said, like, you know, every time we saw the hard problem,
352
00:17:25,308 --> 00:17:27,346
a new hard problem pops up.
353
00:17:27,346 --> 00:17:30,577
So, it feels like that's the business that we are in.
354
00:17:31,808 --> 00:17:35,500
But the thing that I feel like we are most helping
355
00:17:35,846 --> 00:17:38,846
customers, one is speed of innovation.
356
00:17:39,346 --> 00:17:42,269
And the idea that our customers are telling us
357
00:17:42,269 --> 00:17:45,269
that on day one, they can be productive,
358
00:17:45,692 --> 00:17:48,692
that they have the signals that they can make the right decisions,
359
00:17:49,692 --> 00:17:52,000
that we are not wasting their time,
360
00:17:52,000 --> 00:17:54,885
okay, that their team is productive
361
00:17:54,885 --> 00:17:57,077
is really, really important.
362
00:17:57,077 --> 00:17:58,654
There's no competitive advantage for them.
363
00:17:58,654 --> 00:18:01,038
Yes, yes, for sure.
364
00:18:01,038 --> 00:18:04,038
The second thing is that,
365
00:18:06,038 --> 00:18:08,731
We do see our customers as partners.
366
00:18:08,731 --> 00:18:12,615
I think it's a privilege for us to partner
367
00:18:12,615 --> 00:18:16,077
with them and enable this next, gen innovation.
368
00:18:16,885 --> 00:18:18,808
And it looks differently. Okay.
369
00:18:18,808 --> 00:18:23,231
It looks in a way that our customers, we are not just talking about
370
00:18:24,385 --> 00:18:27,385
the platform or what services we are talking to them about.
371
00:18:27,462 --> 00:18:30,462
What changes do they have, how can we help?
372
00:18:30,577 --> 00:18:33,462
And if they need us, we'll be there, okay.
373
00:18:33,462 --> 00:18:36,462
We'll be there to help them with whatever they need.
374
00:18:36,577 --> 00:18:40,308
And as part of that, state of mind,
375
00:18:40,615 --> 00:18:43,500
it's also impact of how we support our customers.
376
00:18:43,500 --> 00:18:48,654
We are actually not a really like a traditional, support process.
377
00:18:49,154 --> 00:18:52,769
And the way we are working, we believe in engineering
378
00:18:52,769 --> 00:18:57,000
to engineering relationships because our customers are sophisticated.
379
00:18:57,385 --> 00:18:59,000
They have the hardest problem.
380
00:18:59,000 --> 00:19:02,423
They want to know that they can quickly find solutions.
381
00:19:02,885 --> 00:19:05,808
And so we really automated and manage that process.
382
00:19:05,808 --> 00:19:07,231
We call it direct to expert.
383
00:19:08,462 --> 00:19:11,154
And we have engineers working with our customers day
384
00:19:11,154 --> 00:19:14,269
in day out on the hardest problems, same language like
385
00:19:15,269 --> 00:19:18,731
difference from a differentiation perspective and really getting in there
386
00:19:18,731 --> 00:19:22,885
and allowing those experts to deliver to their customers what they expect.
387
00:19:22,885 --> 00:19:23,846
For sure.
388
00:19:23,846 --> 00:19:26,500
So you're not a mind reader, can't predict a future.
389
00:19:26,500 --> 00:19:29,500
But a year from now, GTC 2027,
390
00:19:30,115 --> 00:19:33,115
we think we might see.
391
00:19:33,577 --> 00:19:34,615
That's it.
392
00:19:34,615 --> 00:19:36,577
I keep thinking, I keep thinking about it.
393
00:19:36,577 --> 00:19:40,346
If someone would have told me and that like in
394
00:19:40,346 --> 00:19:43,346
2025 would look the way it is, I would not have believed it.
395
00:19:43,462 --> 00:19:43,692
Okay?
396
00:19:43,692 --> 00:19:47,231
There's been so many things that happened that surprised all of us
397
00:19:47,500 --> 00:19:49,346
from an advancement perspective.
398
00:19:49,346 --> 00:19:53,231
However, I do expect that we will see,
399
00:19:54,654 --> 00:19:56,308
an explosion of use cases.
400
00:19:57,885 --> 00:20:03,769
And. More and more people will speak the AI language.
401
00:20:04,308 --> 00:20:06,038
It's so powerful.
402
00:20:06,038 --> 00:20:09,038
And the tools are becoming so accessible
403
00:20:09,462 --> 00:20:11,346
that I, I think that
404
00:20:11,346 --> 00:20:15,308
we will see less people be worried about it,
405
00:20:15,308 --> 00:20:18,308
because what we are seeing today, that the people that lean in
406
00:20:19,038 --> 00:20:21,500
find that is their superpower.
407
00:20:21,500 --> 00:20:23,346
Yeah. Yes.
408
00:20:23,346 --> 00:20:25,000
Yeah. I love that leaning in.
409
00:20:25,000 --> 00:20:28,000
And thank you so much for an outstanding conversation.
410
00:20:28,115 --> 00:20:31,038
I appreciate you taking some time to be on the podcast and share
411
00:20:31,038 --> 00:20:33,769
what you're talking about, what you're hearing from customers,
412
00:20:33,769 --> 00:20:37,077
the strength of the NVIDIA partnership, and also other partnerships
413
00:20:37,308 --> 00:20:41,846
in that ecosystem that really make AI accessible for customers.
414
00:20:41,846 --> 00:20:43,115
I appreciate your time. Thank you.
415
00:20:43,115 --> 00:20:44,885
Thank you so much for having me.
416
00:20:44,885 --> 00:20:47,231
For Chen Goldberg, I'm Lisa Martin. You're watching
417
00:20:47,231 --> 00:20:50,385
AI Cloud Essentials podcast live from GTC.
418
00:20:50,654 --> 00:20:52,654
Thanks for watching guys. We'll see you on the next pod.
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
