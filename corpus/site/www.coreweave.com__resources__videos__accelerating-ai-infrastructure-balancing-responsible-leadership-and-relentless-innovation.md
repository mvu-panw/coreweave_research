# Inside how Nvidia and CoreWeave approach AI at scale

Source: https://www.coreweave.com/resources/videos/accelerating-ai-infrastructure-balancing-responsible-leadership-and-relentless-innovation

Announcement

Webinar

Podcast

GTC 2026

CoreWeave Forge is here: connect your AI loop and compound every improvement. Read more

Contact us

Copied

Overview
Transcript

Watch CoreWeave Chief Revenue Officer, John Jones, and NVIDIA’s Director of Accelerated Computing Products, Dave Salvatore, break down what leaders need to know about the next wave of AI. They explore how to think about modern infrastructure decisions, what today’s benchmarks really signal, and how emerging trends—from agentic AI to new system architectures—are reshaping what’s possible for teams building AI at scale.
Here’s what you’ll learn:
- How to think about AI readiness, skills, and the pace of change

- Why benchmark-proven performance matters for real-world infrastructure planning

- How mixture-of-experts architectures are impacting agents and reasoning

- How market disruptions actually move AI forward

- What’s coming next in accelerated computing, including new architectures and interconnects
‍

00:00

1
00:00:04,371 --> 00:00:05,722
So, without further
2
00:00:05,722 --> 00:00:06,923
ado, let's keep the momentum going.
3
00:00:06,923 --> 00:00:09,392
Let's please welcome to the stage
4
00:00:09,392 --> 00:00:12,595
Jon Jones, the new right, just onboarded,
5
00:00:12,812 --> 00:00:15,715
new Chief Revenue Officer at CoreWeave.
6
00:00:15,715 --> 00:00:17,100
And Dave Salvator,
7
00:00:17,100 --> 00:00:18,418
Director of Accelerated
8
00:00:18,418 --> 00:00:20,603
Computing Products at Nvidia.
9
00:00:20,603 --> 00:00:21,921
They're going to talk about accelerating
10
00:00:21,921 --> 00:00:23,006
AI infrastructure
11
00:00:23,006 --> 00:00:24,858
and balancing responsible leadership
12
00:00:24,858 --> 00:00:26,393
and relentless innovation.
13
00:00:26,393 --> 00:00:27,560
Let's give them a round of applause.
14
00:00:27,560 --> 00:00:30,563
Come on up.
15
00:00:36,469 --> 00:00:37,170
Okay.
16
00:00:37,170 --> 00:00:38,938
Thank you for that introduction, Dave.
17
00:00:38,938 --> 00:00:40,306
Thank you for joining us.
18
00:00:40,306 --> 00:00:40,840
Yeah. Good.
19
00:00:40,840 --> 00:00:43,076
For everyone who,
20
00:00:43,076 --> 00:00:44,127
got to eat lunch with Mike
21
00:00:44,127 --> 00:00:46,496
if you didn't get to eat lunch with Mike,
22
00:00:46,496 --> 00:00:47,964
this is about the only time
23
00:00:47,964 --> 00:00:48,531
you'll see him
24
00:00:48,531 --> 00:00:49,849
without his security detail.
25
00:00:49,849 --> 00:00:51,451
So go get a selfie
26
00:00:51,451 --> 00:00:54,287
and ambush him on the way out.
27
00:00:54,287 --> 00:00:55,038
All right.
28
00:00:55,038 --> 00:00:57,057
So thank you for the introduction.
29
00:00:57,057 --> 00:00:59,059
Dave, that was kind of a quick one.
30
00:00:59,059 --> 00:00:59,909
Why don't you tell us a little bit
31
00:00:59,909 --> 00:01:00,527
about what you do?
32
00:01:00,527 --> 00:01:00,977
Sure.
33
00:01:00,977 --> 00:01:02,629
So, my team at Nvidia,
34
00:01:02,629 --> 00:01:04,397
we work with our cloud providers,
35
00:01:04,397 --> 00:01:06,950
and work very closely with CoreWeave,
36
00:01:06,950 --> 00:01:08,101
on all things
37
00:01:08,101 --> 00:01:09,319
related to bring the Nvidia
38
00:01:09,319 --> 00:01:10,670
sort of technology to the cloud
39
00:01:10,670 --> 00:01:12,355
and helping to raise awareness
40
00:01:12,355 --> 00:01:14,040
and make sure that customers
41
00:01:14,040 --> 00:01:15,141
and the market in general
42
00:01:15,141 --> 00:01:16,192
just really understands
43
00:01:16,192 --> 00:01:17,627
the full scope of our partnership,
44
00:01:17,627 --> 00:01:19,112
but also the full scope
45
00:01:19,112 --> 00:01:21,347
of the capabilities of the platform.
46
00:01:21,347 --> 00:01:22,465
There is a bit of a tendency
47
00:01:22,465 --> 00:01:23,433
to think of Nvidia as,
48
00:01:23,433 --> 00:01:24,951
oh, those GPU guys,
49
00:01:24,951 --> 00:01:26,119
but the GPU really is just the beginning
50
00:01:26,119 --> 00:01:28,104
 CoreWeave and Nvidia
51
00:01:28,104 --> 00:01:29,189
have a lot of what I'll call
52
00:01:29,189 --> 00:01:30,406
cultural simpatico.
53
00:01:30,406 --> 00:01:31,741
You know, Jean talked earlier
54
00:01:31,741 --> 00:01:34,010
about your three P's, you know, being,
55
00:01:34,010 --> 00:01:37,464
performance, partnership and pace.
56
00:01:37,464 --> 00:01:38,148
Right.
57
00:01:38,148 --> 00:01:39,449
And I may have gotten the order wrong,
58
00:01:39,449 --> 00:01:40,517
but those are the three,
59
00:01:40,517 --> 00:01:42,018
we're very much wired
60
00:01:42,018 --> 00:01:42,952
the same way at Nvidia.
61
00:01:42,952 --> 00:01:43,553
You know, at Nvidia,
62
00:01:43,553 --> 00:01:45,054
we talk about speed of light, right?
63
00:01:45,054 --> 00:01:46,039
Which is how quickly
64
00:01:46,039 --> 00:01:48,024
can we move to make something happen.
65
00:01:48,024 --> 00:01:48,925
And we have done
66
00:01:48,925 --> 00:01:50,543
some great collaborations with Kevin.
67
00:01:50,543 --> 00:01:51,361
Continue to do them.
68
00:01:51,361 --> 00:01:52,662
They're ongoing of course.
69
00:01:52,662 --> 00:01:54,030
But particularly around things
70
00:01:54,030 --> 00:01:55,315
like some of the work you've done
71
00:01:55,315 --> 00:01:56,549
with, your submissions
72
00:01:56,549 --> 00:01:58,017
to industry standard benchmarks
73
00:01:58,017 --> 00:01:58,668
like Mlperf
74
00:01:58,668 --> 00:01:59,002
is something
75
00:01:59,002 --> 00:02:00,537
I've been involved in myself,
76
00:02:00,537 --> 00:02:02,388
but you guys actually hold the record
77
00:02:02,388 --> 00:02:03,807
for the largest scale
78
00:02:03,807 --> 00:02:04,257
submission
79
00:02:04,257 --> 00:02:05,492
the benchmarks ever seen at over
80
00:02:05,492 --> 00:02:07,827
11,600 GPUs.
81
00:02:07,827 --> 00:02:08,611
And along with that,
82
00:02:08,611 --> 00:02:09,813
you have the training performance
83
00:02:09,813 --> 00:02:11,281
record to go with it.
84
00:02:11,281 --> 00:02:12,565
And at the end of that
85
00:02:12,565 --> 00:02:14,517
CoreWeave has a pretty good track record of,
86
00:02:14,517 --> 00:02:15,568
phenomenal track record.
87
00:02:15,568 --> 00:02:18,721
Yeah I think, again, that's the agility piece,
88
00:02:18,721 --> 00:02:20,039
that sort of that bias towards
89
00:02:20,039 --> 00:02:22,442
just go, go, go and being able
90
00:02:22,442 --> 00:02:23,393
to also work closely
91
00:02:23,393 --> 00:02:24,377
with our engineering teams.
92
00:02:24,377 --> 00:02:24,828
You know,
93
00:02:24,828 --> 00:02:25,979
we have reference designs
94
00:02:25,979 --> 00:02:28,014
we make available to our partners called
95
00:02:28,014 --> 00:02:29,332
Reference Designs.
96
00:02:29,332 --> 00:02:32,302
And I believe CoreWeave doesn't quite use it 1 to 1,
97
00:02:32,302 --> 00:02:33,153
but they do
98
00:02:33,153 --> 00:02:34,020
sort of take
99
00:02:34,020 --> 00:02:35,188
or you do take a fair
100
00:02:35,188 --> 00:02:36,422
amount of what's
101
00:02:36,422 --> 00:02:37,373
in our reference designs.
102
00:02:37,373 --> 00:02:37,941
You take it,
103
00:02:37,941 --> 00:02:38,842
maybe tweak it a little bit
104
00:02:38,842 --> 00:02:39,926
for how you want to deploy it,
105
00:02:39,926 --> 00:02:41,327
and then you guys deploy
106
00:02:41,327 --> 00:02:43,346
and that helps speed your time to market.
107
00:02:43,346 --> 00:02:43,730
Yeah.
108
00:02:43,730 --> 00:02:45,748
And and as part of that process,
109
00:02:45,748 --> 00:02:46,466
there's a lot of talk
110
00:02:46,466 --> 00:02:48,501
about GPUs and GPU availability,
111
00:02:48,501 --> 00:02:51,504
but that it's not it's not really a chip
112
00:02:51,621 --> 00:02:52,705
constraint alone
113
00:02:52,705 --> 00:02:54,290
or chip deployment alone. Right.
114
00:02:54,290 --> 00:02:55,341
There's a lot of hard work
115
00:02:55,341 --> 00:02:56,709
at the software layer.
116
00:02:56,709 --> 00:02:58,061
But the interconnect
117
00:02:58,061 --> 00:02:58,761
layer, building
118
00:02:58,761 --> 00:02:59,846
clusters of these things
119
00:02:59,846 --> 00:03:00,480
is very different
120
00:03:00,480 --> 00:03:02,065
than building a few of these things
121
00:03:02,065 --> 00:03:03,349
very much talk a little bit.
122
00:03:03,349 --> 00:03:05,118
And the software stack, of course,
123
00:03:05,118 --> 00:03:06,753
the Nvidia built is world class
124
00:03:06,753 --> 00:03:08,338
and is by far the market leader.
125
00:03:08,338 --> 00:03:08,872
Talk a little bit
126
00:03:08,872 --> 00:03:10,373
about the importance of software
127
00:03:10,373 --> 00:03:11,658
as part of these deployments.
128
00:03:11,658 --> 00:03:13,459
Software plays a huge role.
129
00:03:13,459 --> 00:03:13,877
I mean,
130
00:03:13,877 --> 00:03:15,411
without the software to really unlock
131
00:03:15,411 --> 00:03:17,180
the full potential of the hardware,
132
00:03:17,180 --> 00:03:18,648
the hardware is a glorified space
133
00:03:18,648 --> 00:03:19,315
heater, right?
134
00:03:19,315 --> 00:03:20,600
I mean, you really need
135
00:03:20,600 --> 00:03:22,669
software to be a performant,
136
00:03:22,669 --> 00:03:24,470
but it involves so much work
137
00:03:24,470 --> 00:03:25,405
with the ecosystem.
138
00:03:25,405 --> 00:03:27,390
As many of your audience members know,
139
00:03:28,675 --> 00:03:29,209
open source
140
00:03:29,209 --> 00:03:31,194
software is a hugely important component
141
00:03:31,194 --> 00:03:33,079
to driving AI innovation, right?
142
00:03:33,079 --> 00:03:33,680
It's one of the things
143
00:03:33,680 --> 00:03:34,647
that allows developers
144
00:03:34,647 --> 00:03:36,266
to kind of share, work with each other
145
00:03:36,266 --> 00:03:36,933
and be able to take
146
00:03:36,933 --> 00:03:38,484
that work, build upon that work,
147
00:03:38,484 --> 00:03:40,370
and sequentially drive innovation
148
00:03:40,370 --> 00:03:41,004
into the market.
149
00:03:41,004 --> 00:03:41,671
Right.
150
00:03:41,671 --> 00:03:43,439
CoreWeave makes a lot of contributions
151
00:03:43,439 --> 00:03:44,190
into the open source
152
00:03:44,190 --> 00:03:45,475
world, as does Nvidia.
153
00:03:45,475 --> 00:03:45,959
We you know,
154
00:03:45,959 --> 00:03:46,559
we contribute
155
00:03:46,559 --> 00:03:49,762
on models, on frameworks, on things
156
00:03:49,762 --> 00:03:50,847
like our dynamo,
157
00:03:50,847 --> 00:03:51,864
inference serving software,
158
00:03:51,864 --> 00:03:53,299
which is also open source.
159
00:03:53,299 --> 00:03:54,717
And we do a huge amount of work
160
00:03:54,717 --> 00:03:55,551
in terms of submissions
161
00:03:55,551 --> 00:03:57,237
we make into the Linux project,
162
00:03:57,237 --> 00:03:59,188
which ultimately get rolled into,
163
00:03:59,188 --> 00:03:59,939
you know, the main
164
00:03:59,939 --> 00:04:01,591
code base of it,
165
00:04:01,591 --> 00:04:03,476
to help enable accelerated computing.
166
00:04:03,476 --> 00:04:04,978
And then a number of our own libraries
167
00:04:04,978 --> 00:04:06,679
as well are also open source.
168
00:04:06,679 --> 00:04:07,580
So,
169
00:04:07,580 --> 00:04:09,115
you know, the software piece
170
00:04:09,115 --> 00:04:10,650
is just incredibly important.
171
00:04:10,650 --> 00:04:13,019
And because the early, early work on
172
00:04:13,019 --> 00:04:13,770
deep learning was done
173
00:04:13,770 --> 00:04:14,637
on Nvidia products,
174
00:04:14,637 --> 00:04:16,322
if you go all the way back to AlexNet,
175
00:04:16,322 --> 00:04:18,358
back in 2012,
176
00:04:18,358 --> 00:04:19,592
we saw that opportunity
177
00:04:19,592 --> 00:04:20,760
and we already had something in place
178
00:04:20,760 --> 00:04:21,411
called Cuda,
179
00:04:21,411 --> 00:04:22,312
which had been in the market
180
00:04:22,312 --> 00:04:24,564
for a, you know, about five or so years.
181
00:04:24,564 --> 00:04:25,648
And we were trying to find
182
00:04:25,648 --> 00:04:26,733
we were starting to do things with it
183
00:04:26,733 --> 00:04:28,101
around scientific simulation,
184
00:04:28,101 --> 00:04:29,252
you know, whether it's CFD,
185
00:04:29,252 --> 00:04:31,187
molecular dynamics, what have you.
186
00:04:31,187 --> 00:04:31,738
And it turned out
187
00:04:31,738 --> 00:04:33,539
GPUs are really good at that.
188
00:04:33,539 --> 00:04:33,890
In fact,
189
00:04:33,890 --> 00:04:35,458
GPUs are pretty much really good
190
00:04:35,458 --> 00:04:37,160
at anything that can be parallelized
191
00:04:37,160 --> 00:04:38,278
because it's a massively
192
00:04:38,278 --> 00:04:40,079
parallel machine. Right?
193
00:04:40,079 --> 00:04:41,297
Alex comes along, built
194
00:04:41,297 --> 00:04:43,099
AlexNet was done on our product
195
00:04:43,099 --> 00:04:44,484
and then we saw an opportunity for Cuda.
196
00:04:44,484 --> 00:04:45,535
So then we started building
197
00:04:45,535 --> 00:04:46,552
more libraries to help
198
00:04:46,552 --> 00:04:47,236
support
199
00:04:47,236 --> 00:04:48,621
this notion of deep learning because,
200
00:04:48,621 --> 00:04:50,456
I mean, I it's been with us for decades.
201
00:04:50,456 --> 00:04:50,990
Right.
202
00:04:50,990 --> 00:04:52,225
But the notion of deep learning,
203
00:04:52,225 --> 00:04:53,159
of building networks
204
00:04:53,159 --> 00:04:55,194
that have multiple, multiple layers
205
00:04:55,194 --> 00:04:56,129
and massive amounts
206
00:04:56,129 --> 00:04:58,431
of compute necessary to drive them
207
00:04:58,431 --> 00:05:00,116
wasn't was simply infeasible
208
00:05:00,116 --> 00:05:01,317
in the past, right?
209
00:05:01,317 --> 00:05:02,969
GPUs made that possible.
210
00:05:02,969 --> 00:05:03,770
So we've been driving
211
00:05:03,770 --> 00:05:06,773
and innovating software really for over,
212
00:05:06,956 --> 00:05:08,574
you know, over a dozen years
213
00:05:08,574 --> 00:05:09,709
to make AI
214
00:05:09,709 --> 00:05:11,661
and help it drive, drive it forward.
215
00:05:11,661 --> 00:05:12,028
Right.
216
00:05:12,028 --> 00:05:13,579
And then of course, CoreWeave
217
00:05:13,579 --> 00:05:14,130
you know, is doing
218
00:05:14,130 --> 00:05:15,264
a lot of that as well,
219
00:05:15,264 --> 00:05:15,782
through work
220
00:05:15,782 --> 00:05:16,949
you do certainly internally
221
00:05:16,949 --> 00:05:17,817
and some of your recent
222
00:05:17,817 --> 00:05:19,202
acquisitions as well.
223
00:05:19,202 --> 00:05:20,603
You guys are also building out
224
00:05:20,603 --> 00:05:21,504
a pretty robust software
225
00:05:21,504 --> 00:05:22,939
stack of your own.
226
00:05:22,939 --> 00:05:24,023
A lot of the workloads
227
00:05:24,023 --> 00:05:25,224
that you talked about,
228
00:05:25,224 --> 00:05:26,909
simulation and rendering
229
00:05:26,909 --> 00:05:28,728
are very high performance,
230
00:05:28,728 --> 00:05:29,729
classical, high performance
231
00:05:29,729 --> 00:05:30,530
computing workloads.
232
00:05:30,530 --> 00:05:30,863
By the way,
233
00:05:30,863 --> 00:05:31,547
is anybody in here
234
00:05:31,547 --> 00:05:32,749
willing to self-identify as
235
00:05:32,749 --> 00:05:34,250
having HPC expertise?
236
00:05:35,418 --> 00:05:36,919
No, it
237
00:05:36,919 --> 00:05:37,704
just means you're all
238
00:05:37,704 --> 00:05:40,673
much younger than I am. Six, 16 months.
239
00:05:40,673 --> 00:05:41,190
Okay.
240
00:05:41,190 --> 00:05:44,477
So, once you get into, just up to
241
00:05:44,477 --> 00:05:45,178
and through the GPU
242
00:05:45,178 --> 00:05:46,429
in the software stack,
243
00:05:46,429 --> 00:05:47,847
we were talking in the back of
244
00:05:47,847 --> 00:05:48,564
you have a lot of long
245
00:05:48,564 --> 00:05:49,499
history of benchmarking.
246
00:05:49,499 --> 00:05:51,734
Two going going, way back.
247
00:05:51,734 --> 00:05:53,603
Maybe you can talk a little bit
248
00:05:53,603 --> 00:05:54,987
about the arc of,
249
00:05:54,987 --> 00:05:56,839
of the benchmarking progress
250
00:05:56,839 --> 00:05:59,342
as it, as it, relates to pre
251
00:05:59,342 --> 00:06:01,677
AI and then post AI because ultimately
252
00:06:01,677 --> 00:06:03,813
AI clusters
253
00:06:03,813 --> 00:06:06,799
are just big supercomputers.
254
00:06:07,650 --> 00:06:07,917
Yeah.
255
00:06:07,917 --> 00:06:09,052
I guess we just had a pick up
256
00:06:09,052 --> 00:06:10,353
in the volume there. That's fine.
257
00:06:10,353 --> 00:06:11,387
You know lunch.
258
00:06:11,387 --> 00:06:12,388
Come on. Might be setting in.
259
00:06:12,388 --> 00:06:13,790
So this will help keep them awake.
260
00:06:13,790 --> 00:06:16,642
No. They are similar workloads.
261
00:06:16,642 --> 00:06:17,276
They both have
262
00:06:17,276 --> 00:06:19,112
parallelizable aspects, but
263
00:06:19,112 --> 00:06:20,430
but AI in particular
264
00:06:20,430 --> 00:06:22,532
is just embarrassingly parallelizable,
265
00:06:22,532 --> 00:06:23,449
which is what makes it such
266
00:06:23,449 --> 00:06:24,767
a great fit for GPUs.
267
00:06:26,069 --> 00:06:26,602
But, you know,
268
00:06:26,602 --> 00:06:29,005
again, the benchmarking space of
269
00:06:29,005 --> 00:06:30,773
AI has been pretty crazy.
270
00:06:30,773 --> 00:06:32,725
I would say it's been kind of Wild West,
271
00:06:32,725 --> 00:06:34,110
for some time,
272
00:06:34,110 --> 00:06:35,027
which is why,
273
00:06:35,027 --> 00:06:35,328
you know,
274
00:06:35,328 --> 00:06:36,362
we're a member of what's called
275
00:06:36,362 --> 00:06:37,880
the ML Commons Consortium,
276
00:06:37,880 --> 00:06:38,431
which builds
277
00:06:38,431 --> 00:06:39,715
the mlperf benchmarks both
278
00:06:39,715 --> 00:06:41,451
for training and inference.
279
00:06:41,451 --> 00:06:42,235
And they build a number
280
00:06:42,235 --> 00:06:43,202
of other benchmarks as well.
281
00:06:43,202 --> 00:06:44,337
But the data center benchmarks
282
00:06:44,337 --> 00:06:46,639
is our primary focus at Nvidia.
283
00:06:46,639 --> 00:06:48,324
And we have done very,
284
00:06:48,324 --> 00:06:49,409
very well on those benchmarks.
285
00:06:49,409 --> 00:06:50,777
And we try and, you know, bring out
286
00:06:50,777 --> 00:06:52,011
new versions of those benchmarks
287
00:06:52,011 --> 00:06:52,979
about every six months,
288
00:06:52,979 --> 00:06:54,480
which has industry
289
00:06:54,480 --> 00:06:55,765
consortium driven benchmarks.
290
00:06:55,765 --> 00:06:58,050
Go is a very fast pace.
291
00:06:58,050 --> 00:06:59,368
That said, we're trying
292
00:06:59,368 --> 00:07:00,887
to even make that pace faster
293
00:07:00,887 --> 00:07:01,587
because of the rate at
294
00:07:01,587 --> 00:07:02,722
which AI is evolving.
295
00:07:04,307 --> 00:07:05,274
And so this is an
296
00:07:05,274 --> 00:07:05,942
attempt, frankly,
297
00:07:05,942 --> 00:07:06,692
to kind of bring some order
298
00:07:06,692 --> 00:07:07,677
to chaos to kind of say,
299
00:07:07,677 --> 00:07:08,911
let's build a benchmark
300
00:07:08,911 --> 00:07:09,595
where we have directly
301
00:07:09,595 --> 00:07:10,847
comparable results.
302
00:07:10,847 --> 00:07:12,348
So we can actually look at two systems
303
00:07:12,348 --> 00:07:13,850
and go, okay, they did the same work.
304
00:07:13,850 --> 00:07:15,618
Who's better? Right.
305
00:07:15,618 --> 00:07:16,586
And they're fairly
306
00:07:16,586 --> 00:07:18,988
stringent requirements around accuracy,
307
00:07:18,988 --> 00:07:19,822
around the ability
308
00:07:19,822 --> 00:07:21,107
that the models have to converge.
309
00:07:21,107 --> 00:07:22,742
If you're training as an example.
310
00:07:22,742 --> 00:07:24,260
And these are peer reviewed benchmarks.
311
00:07:24,260 --> 00:07:25,978
So once the results are submitted,
312
00:07:25,978 --> 00:07:27,530
there's about a month long period
313
00:07:27,530 --> 00:07:28,998
where every submitter and, you know,
314
00:07:28,998 --> 00:07:30,683
a lot of these are competitors
315
00:07:30,683 --> 00:07:31,734
can basically scrutinize
316
00:07:31,734 --> 00:07:32,752
everyone else's submission.
317
00:07:32,752 --> 00:07:33,870
And if they see something
318
00:07:33,870 --> 00:07:35,972
that they think might be questionable,
319
00:07:35,972 --> 00:07:37,140
they can raise a concern.
320
00:07:37,140 --> 00:07:38,541
And that concern has to be addressed
321
00:07:38,541 --> 00:07:40,009
before the benchmark results
322
00:07:40,009 --> 00:07:41,093
will see light of day.
323
00:07:41,093 --> 00:07:42,411
So what you're getting is results
324
00:07:42,411 --> 00:07:42,962
that have kind of,
325
00:07:42,962 --> 00:07:45,331
you know, had held the fire, if you will,
326
00:07:45,331 --> 00:07:46,382
that frankly,
327
00:07:46,382 --> 00:07:46,999
are more meaningful
328
00:07:46,999 --> 00:07:48,351
and directly comparable.
329
00:07:48,351 --> 00:07:48,718
Right.
330
00:07:48,718 --> 00:07:49,469
You know, that said,
331
00:07:49,469 --> 00:07:50,486
there are other benchmarking
332
00:07:50,486 --> 00:07:51,654
efforts underway.
333
00:07:51,654 --> 00:07:52,705
Most recently,
334
00:07:52,705 --> 00:07:53,539
some of the analysis did
335
00:07:53,539 --> 00:07:54,690
a thing called inference. Max.
336
00:07:54,690 --> 00:07:55,741
We did very well with that
337
00:07:55,741 --> 00:07:57,677
with our Blackwell architecture.
338
00:07:57,677 --> 00:07:59,061
Very pleased to see those results.
339
00:07:59,061 --> 00:08:00,480
And it speaks to the
340
00:08:00,480 --> 00:08:01,831
the growing importance of inference.
341
00:08:01,831 --> 00:08:02,698
And Peter spoke to this
342
00:08:02,698 --> 00:08:04,317
a little bit earlier this morning
343
00:08:04,317 --> 00:08:06,802
about about the growth of this scale
344
00:08:06,802 --> 00:08:08,704
and the demands of inference.
345
00:08:08,704 --> 00:08:10,256
Really just kind of,
346
00:08:10,256 --> 00:08:12,325
you know, on this, on this incredible,
347
00:08:12,325 --> 00:08:14,310
basically exponential trajectory.
348
00:08:14,310 --> 00:08:15,361
So, so you get to see
349
00:08:15,361 --> 00:08:16,829
most of the benchmarking work.
350
00:08:16,829 --> 00:08:18,297
I know our teams
351
00:08:18,297 --> 00:08:19,649
collaborate closely together on that.
352
00:08:19,649 --> 00:08:20,967
I'll ask you about that in a minute.
353
00:08:20,967 --> 00:08:23,903
But, from from that objective viewpoint, how
354
00:08:23,903 --> 00:08:24,470
How’s CoreWeave doing?
355
00:08:25,521 --> 00:08:27,123
CoreWeave, again, does very well.
356
00:08:27,123 --> 00:08:28,441
I think because of the close
357
00:08:28,441 --> 00:08:28,975
collaboration
358
00:08:28,975 --> 00:08:30,593
we have on the engineering side,
359
00:08:30,593 --> 00:08:31,527
and because you guys
360
00:08:31,527 --> 00:08:32,879
are also very focused on
361
00:08:32,879 --> 00:08:33,629
making sure you get
362
00:08:33,629 --> 00:08:34,680
phenomenal performance
363
00:08:34,680 --> 00:08:36,482
from from our technologies.
364
00:08:36,482 --> 00:08:38,267
The result comes out in places
365
00:08:38,267 --> 00:08:39,051
like Mlperf.
366
00:08:39,051 --> 00:08:39,619
And, you know,
367
00:08:39,619 --> 00:08:40,436
you also, of course,
368
00:08:40,436 --> 00:08:41,571
on the recent cluster
369
00:08:41,571 --> 00:08:43,339
Max evaluation that SA,
370
00:08:43,339 --> 00:08:45,541
did you guys also were the only,
371
00:08:45,541 --> 00:08:46,792
submitter,
372
00:08:46,792 --> 00:08:47,510
I think, who achieved,
373
00:08:47,510 --> 00:08:48,628
I guess they call it the platinum level,
374
00:08:48,628 --> 00:08:50,096
which is the highest level.
375
00:08:50,096 --> 00:08:52,315
So no, CoreWeave has definitely proven itself.
376
00:08:52,315 --> 00:08:54,617
I mean, track record matters, right?
377
00:08:54,617 --> 00:08:56,419
And it's one thing to sort of
378
00:08:56,419 --> 00:08:58,321
basically do some kind of a performance
379
00:08:58,321 --> 00:08:58,821
stunt and go
380
00:08:58,821 --> 00:08:59,572
look at how fast we are
381
00:08:59,572 --> 00:09:01,407
on this one model. In this one condition,
382
00:09:02,658 --> 00:09:03,109
it can be a
383
00:09:03,109 --> 00:09:03,859
valid data point,
384
00:09:03,859 --> 00:09:05,177
but we all know that I,
385
00:09:05,177 --> 00:09:06,212
particularly on the inference
386
00:09:06,212 --> 00:09:06,979
side,
387
00:09:06,979 --> 00:09:08,748
has so many parametric knobs
388
00:09:08,748 --> 00:09:10,099
that can be played with,
389
00:09:10,099 --> 00:09:11,701
that getting to directly
390
00:09:11,701 --> 00:09:12,652
comparable performance
391
00:09:12,652 --> 00:09:14,036
can be a real challenge. Right?
392
00:09:14,036 --> 00:09:16,172
Whereas when you're willing to basically
393
00:09:16,172 --> 00:09:16,739
be weighed
394
00:09:16,739 --> 00:09:17,607
and measured in a place
395
00:09:17,607 --> 00:09:18,658
like, say, mlperf,
396
00:09:18,658 --> 00:09:19,942
where you're going to be scrutinized,
397
00:09:19,942 --> 00:09:21,928
if you do anything that's at. All.
398
00:09:21,928 --> 00:09:23,062
Odd looking.
399
00:09:23,062 --> 00:09:25,047
It means that the results
400
00:09:25,047 --> 00:09:26,732
that ultimately come out of that,
401
00:09:26,732 --> 00:09:28,484
frankly, are more meaningful.
402
00:09:28,484 --> 00:09:29,368
They're more credible,
403
00:09:29,368 --> 00:09:30,319
and I think they're ultimately
404
00:09:30,319 --> 00:09:31,437
a better guide to make,
405
00:09:31,437 --> 00:09:32,989
you know, informed investment decisions
406
00:09:32,989 --> 00:09:33,723
about where you want
407
00:09:33,723 --> 00:09:35,541
to build out your infrastructure.
408
00:09:35,541 --> 00:09:37,260
And again, we were talking in the back,
409
00:09:37,260 --> 00:09:40,313
but pretty consistently, CoreWeave’s shown that
410
00:09:40,313 --> 00:09:41,547
the company has the expertise
411
00:09:41,547 --> 00:09:42,748
and the engineering collaboration
412
00:09:42,748 --> 00:09:44,216
is showing up in those benchmarks.
413
00:09:44,216 --> 00:09:45,418
And,
414
00:09:45,418 --> 00:09:46,319
and pretty consistently
415
00:09:46,319 --> 00:09:47,687
Cory's coming out on top.
416
00:09:47,687 --> 00:09:48,871
Yeah, CoreWeave has done
417
00:09:48,871 --> 00:09:49,739
very well with those.
418
00:09:49,739 --> 00:09:50,373
And again,
419
00:09:50,373 --> 00:09:51,240
I think that's a testament
420
00:09:51,240 --> 00:09:52,141
to the partnership.
421
00:09:52,141 --> 00:09:53,643
And it's also a testament to,
422
00:09:53,643 --> 00:09:55,077
the level of engineering skill
423
00:09:55,077 --> 00:09:56,429
that, you know, Peter and his team have.
424
00:09:56,429 --> 00:09:58,698
I mean, they, they do terrific work.
425
00:09:58,698 --> 00:09:59,515
Okay. All right. Great.
426
00:09:59,515 --> 00:10:00,049
Well, let's move
427
00:10:00,049 --> 00:10:00,716
a little bit past
428
00:10:00,716 --> 00:10:01,917
the technical conversation.
429
00:10:01,917 --> 00:10:03,569
There are a lot of leaders in the room
430
00:10:03,569 --> 00:10:05,004
thinking about some of the hard decisions
431
00:10:05,004 --> 00:10:06,505
they have to make as it relates to AI,
432
00:10:06,505 --> 00:10:08,124
as it relates to infrastructure.
433
00:10:08,124 --> 00:10:08,941
I know
434
00:10:08,941 --> 00:10:09,508
one of the things
435
00:10:09,508 --> 00:10:10,910
you wanted to talk about
436
00:10:10,910 --> 00:10:12,778
is mental models around leaders
437
00:10:12,778 --> 00:10:14,447
making decisions about the future
438
00:10:14,447 --> 00:10:15,931
and how that impacts their business.
439
00:10:15,931 --> 00:10:17,750
Maybe maybe you can share a little bit,
440
00:10:17,750 --> 00:10:19,018
with the crowd
441
00:10:19,018 --> 00:10:20,102
here on how
442
00:10:20,102 --> 00:10:20,786
they should think about
443
00:10:20,786 --> 00:10:22,038
some of those decisions.
444
00:10:22,038 --> 00:10:22,888
Yeah, it's
445
00:10:22,888 --> 00:10:24,173
it's an interesting time
446
00:10:24,173 --> 00:10:26,542
because AI is really
447
00:10:26,542 --> 00:10:27,543
is getting going now.
448
00:10:27,543 --> 00:10:29,128
And we've seen some of the initial things
449
00:10:29,128 --> 00:10:30,863
that agenda guy can do for us. Right.
450
00:10:30,863 --> 00:10:32,148
But I'd say we're still very much
451
00:10:32,148 --> 00:10:34,233
in the early innings on a genetic AI.
452
00:10:34,233 --> 00:10:35,751
So as you think about,
453
00:10:35,751 --> 00:10:36,686
I mean, in a lot of ways
454
00:10:36,686 --> 00:10:38,037
for business leaders,
455
00:10:38,037 --> 00:10:39,171
AI is no different
456
00:10:39,171 --> 00:10:40,790
than any other technology or tool
457
00:10:40,790 --> 00:10:42,058
you consider for your business.
458
00:10:42,058 --> 00:10:42,842
And the first question
459
00:10:42,842 --> 00:10:43,592
you want to ask yourself
460
00:10:43,592 --> 00:10:44,910
is, what business problem
461
00:10:44,910 --> 00:10:46,829
am I going to solve with it, right?
462
00:10:46,829 --> 00:10:47,163
In other words,
463
00:10:47,163 --> 00:10:48,047
what are your biggest pain
464
00:10:48,047 --> 00:10:49,765
points in your business? Is it?
465
00:10:49,765 --> 00:10:51,651
It could be as simple as our wait
466
00:10:51,651 --> 00:10:52,401
times are too long
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
