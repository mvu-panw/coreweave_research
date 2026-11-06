# Mercado Libre Scales AI Search | CoreWeave Video

Source: https://www.coreweave.com/resources/videos/mercado-libre-rebuilds-search-with-ai-at-massive-scale

Announcement

Webinar

Podcast

GTC 2026

CoreWeave Forge is here: connect your AI loop and compound every improvement. Read more

Contact us

Copied

Overview
Transcript

### Mercado Libre Scales AI Search
Part of the Who’s Ready for Anything series, this episode features Mercado Libre’s Sebastian Yunge at NVIDIA GTC 2026. Learn how the team rebuilt search with AI—moving from pilot to production quickly using CoreWeave infrastructure.
In this video:
- How Mercado Libre uses AI-driven query expansion to improve search relevance
- What to look for in an AI cloud provider, from GPU capacity to pricing transparency
- How to go from POC to production in weeks, not months
- Why starting small, measuring impact, and iterating quickly drives AI success
‍

00:00

1
00:00:10,427 --> 00:00:11,344
Hey,
2
00:00:11,344 --> 00:00:14,347
welcome to CoreWeave's booth here in our podcast studio
3
00:00:14,472 --> 00:00:19,102
on the second Story of CoreWeave’s booth at NVIDIA GTC 2026.
4
00:00:19,310 --> 00:00:20,854
I'm your host, Lisa Martin,
5
00:00:20,854 --> 00:00:23,440
and we're going to walk you through a great customer story.
6
00:00:23,440 --> 00:00:25,316
Sebastian Yunge is here with us.
7
00:00:25,316 --> 00:00:28,028
He is the senior staff software engineer at
8
00:00:28,028 --> 00:00:30,572
CoreWeave customer Mercado Libre.
9
00:00:30,572 --> 00:00:32,198
We're going to tell you a story
10
00:00:32,198 --> 00:00:35,368
through Sebastian's perspective of one of Latin America's
11
00:00:35,618 --> 00:00:40,165
most sophisticated and largest consumer technology companies.
12
00:00:40,498 --> 00:00:43,209
Sebastian is going to talk to us about how they evaluated,
13
00:00:43,209 --> 00:00:46,546
they piloted, and then moved into production with CoreWeave
14
00:00:46,755 --> 00:00:50,008
to really deliver this purpose built AI infrastructure
15
00:00:50,216 --> 00:00:53,928
for demanding scale and a huge volume of transactions.
16
00:00:54,012 --> 00:00:56,598
Sebastian, thank you so much for taking some time with us today.
17
00:00:56,598 --> 00:00:57,766
Thank you.
18
00:00:57,766 --> 00:01:00,894
So we did some research on Mercado Libre, but I want you to share with the audience
19
00:01:01,102 --> 00:01:04,105
a little bit about this organization is huge in Latin America.
20
00:01:04,272 --> 00:01:04,856
Yeah, yeah.
21
00:01:04,856 --> 00:01:07,442
I mean, if you could, if I could condense it
22
00:01:07,442 --> 00:01:12,113
and if you were to feel like Amazon people rolled into one, you know,
23
00:01:12,405 --> 00:01:15,366
because we do have Mercado Libre in, which is, as you know,
24
00:01:15,366 --> 00:01:18,787
akin to Amazon. Then we have Mercado Pago, which is akin to PayPal.
25
00:01:18,912 --> 00:01:20,830
Oh, okay. Fintech services.
26
00:01:20,830 --> 00:01:22,624
Okay. It's a pretty big company.
27
00:01:22,624 --> 00:01:26,044
We're already up to 120,000,
28
00:01:27,003 --> 00:01:28,880
I don't know, and 25.
29
00:01:28,880 --> 00:01:31,883
Wow. Huge. Across 18 countries.
30
00:01:31,925 --> 00:01:33,343
Yeah, we're we're really big in that.
31
00:01:33,343 --> 00:01:38,640
I learned and I was also reading that this is the sixth largest
32
00:01:39,390 --> 00:01:43,686
e-commerce platform in the world by gross merchandise volume, massive scale.
33
00:01:43,686 --> 00:01:46,689
We're also the biggest company Latin America by GMV.
34
00:01:47,232 --> 00:01:50,235
And you said e-commerce, payments, logistics,
35
00:01:50,610 --> 00:01:52,862
credit, logistical network in Latin America.
36
00:01:52,862 --> 00:01:57,909
That gives us a huge advantage over anyone that wants to enter into the regions.
37
00:01:58,493 --> 00:01:59,369
Excellent.
38
00:01:59,369 --> 00:02:01,121
So tell us about Mercado Libre.
39
00:02:01,121 --> 00:02:04,124
As are use case. What does that look like?
40
00:02:04,833 --> 00:02:09,754
So Duda doesn't fly all across the board, for instance, for prevention
41
00:02:10,296 --> 00:02:13,299
use a lot of public provision.
42
00:02:13,508 --> 00:02:16,511
Where I can speak both about is the search engine.
43
00:02:17,137 --> 00:02:19,806
Right now, we're in the process of rebuilding our search engine,
44
00:02:19,806 --> 00:02:22,976
and we're leveraging AI for different capabilities.
45
00:02:24,644 --> 00:02:25,520
Actually, one of the use
46
00:02:25,520 --> 00:02:30,191
cases that drove us to for we was actually one of the use cases
47
00:02:30,191 --> 00:02:34,237
we were right now building within search search 2.0, if you will.
48
00:02:34,237 --> 00:02:37,240
Okay. So,
49
00:02:37,907 --> 00:02:40,410
right now what we're trying to do is, well, we're rebuilding.
50
00:02:40,410 --> 00:02:41,870
But of course, you know,
51
00:02:41,870 --> 00:02:44,873
when you're doing the AI, you also want to start small. Yes.
52
00:02:46,207 --> 00:02:49,919
See what once was a little land and build something responsibly.
53
00:02:49,919 --> 00:02:52,922
See if there's any revenue.
54
00:02:53,089 --> 00:02:53,923
Is into this.
55
00:02:53,923 --> 00:02:55,633
You see all that?
56
00:02:55,633 --> 00:02:58,636
So one of the experiments that we wanted to go forward with
57
00:02:58,720 --> 00:03:01,639
was actually mechanism of query expansion,
58
00:03:01,639 --> 00:03:05,143
where you take the query that your user
59
00:03:05,143 --> 00:03:08,104
makes and enrich, and with all the context that you have put out, the.
60
00:03:09,189 --> 00:03:12,192
So after that, you can you create new rules
61
00:03:12,442 --> 00:03:15,445
and then merge them all together to get a more precise result
62
00:03:15,528 --> 00:03:18,323
on what they might be actually looking for.
63
00:03:18,323 --> 00:03:21,743
Talk us through what you were looking for in an AI
64
00:03:21,743 --> 00:03:25,496
cloud provider and what stood out with query.
65
00:03:25,830 --> 00:03:26,289
Sure.
66
00:03:26,289 --> 00:03:30,043
Well, first of all, we were looking for someone that had capacity, you know,
67
00:03:30,043 --> 00:03:34,422
because right now you only know looking for GPUs is a slugfest.
68
00:03:34,464 --> 00:03:39,427
Yes. Capacity, especially in the Virginia area
69
00:03:39,427 --> 00:03:42,305
where all the data centers are specialty scores. Gaffney.
70
00:03:43,890 --> 00:03:46,392
But core we actually had capacity there.
71
00:03:46,392 --> 00:03:50,021
And in fact, when we were doing the policy, they even told us.
72
00:03:50,021 --> 00:03:53,691
So you can use like, our 6200,
73
00:03:53,983 --> 00:03:56,945
which are very powerful GPUs in our class.
74
00:03:57,654 --> 00:04:00,573
And that was a huge surprise for us for
75
00:04:00,573 --> 00:04:03,576
having all the capacity of the platform at a below sea level.
76
00:04:03,868 --> 00:04:07,622
So that was huge for us, you know, to test out what Corwin was all about.
77
00:04:07,830 --> 00:04:11,376
Sounds like that what Corey was offering was kind of a tipping point.
78
00:04:11,376 --> 00:04:12,919
And why you said yes.
79
00:04:12,919 --> 00:04:14,295
Let's sign up for a PFC.
80
00:04:14,295 --> 00:04:15,046
Know for sure.
81
00:04:15,046 --> 00:04:18,424
And all the capabilities that we also heard from,
82
00:04:18,758 --> 00:04:22,303
you know, Slurm, just got south on the platform.
83
00:04:22,929 --> 00:04:24,764
The fact that it is run on bare metal.
84
00:04:24,764 --> 00:04:28,101
So you all do anything, you know, and performance wise,
85
00:04:29,894 --> 00:04:32,772
and also,
86
00:04:32,772 --> 00:04:34,232
a clear pricing structure.
87
00:04:34,232 --> 00:04:36,609
That was that was a huge runo as well.
88
00:04:36,609 --> 00:04:39,487
Transparency. Yes. Yes, yes.
89
00:04:39,487 --> 00:04:42,490
So you you made the decision to do the PLC.
90
00:04:42,740 --> 00:04:43,992
What were you mentioned?
91
00:04:43,992 --> 00:04:47,620
What were some of the core technologies, the key technologies of core waves
92
00:04:47,745 --> 00:04:48,997
that you put to the test?
93
00:04:48,997 --> 00:04:52,250
And how did they match up to your expectations?
94
00:04:52,625 --> 00:04:55,628
Well, obviously we tried, you know,
95
00:04:56,045 --> 00:04:59,716
the supernatants with the platform and that's where we are today, actually
96
00:04:59,716 --> 00:05:04,721
running all of our inference for the query expression that I mentioned before.
97
00:05:04,804 --> 00:05:07,807
I also got personally to, to be able
98
00:05:07,807 --> 00:05:10,810
to test the same capability.
99
00:05:10,935 --> 00:05:14,355
That becomes especially useful when you actually
100
00:05:14,397 --> 00:05:17,400
to times like deep and actually
101
00:05:18,026 --> 00:05:20,111
start prioritizing the to use it.
102
00:05:20,111 --> 00:05:22,113
Once you start to have a lot of compute there,
103
00:05:22,113 --> 00:05:25,241
you actually need to keep the Q fields because otherwise you're losing money.
104
00:05:25,491 --> 00:05:27,994
But you actually need to know the inventory of
105
00:05:27,994 --> 00:05:30,246
who wants to win one on one time frame.
106
00:05:30,246 --> 00:05:31,956
So having that,
107
00:05:33,374 --> 00:05:36,044
and as recently as sunk is,
108
00:05:36,044 --> 00:05:40,840
is really a great feature to have because everyone will know something about them.
109
00:05:40,882 --> 00:05:44,177
Customer on your own is it's it's not a simple task.
110
00:05:44,344 --> 00:05:46,512
It can take a while, but you have the visibility now.
111
00:05:46,512 --> 00:05:48,639
Yeah, yeah, it's one click. It's done.
112
00:05:48,639 --> 00:05:52,685
You have a Slurm cluster running right beside your Kubernetes infra.
113
00:05:52,935 --> 00:05:54,729
It's really, really, really easy.
114
00:05:54,729 --> 00:05:56,981
So how long was the POC and what were some of the
115
00:05:56,981 --> 00:05:59,734
the benefits that you immediately saw.
116
00:05:59,734 --> 00:06:04,322
So if I recall correctly, the PLC ran around three weeks.
117
00:06:04,489 --> 00:06:05,281
Okay.
118
00:06:05,281 --> 00:06:06,866
And we were surprised that
119
00:06:06,866 --> 00:06:09,869
they even left us the infrastructure over that period of time.
120
00:06:09,994 --> 00:06:12,288
It's a hot commodity.
121
00:06:12,288 --> 00:06:13,039
Things that we saw.
122
00:06:13,039 --> 00:06:15,833
Well, yes, of of durability, you know, of operations.
123
00:06:18,044 --> 00:06:20,880
There was no feature created whatsoever.
124
00:06:20,880 --> 00:06:25,426
So from the get go, we were able to see how that meshed with our operations.
125
00:06:26,260 --> 00:06:27,428
Because sometimes you get
126
00:06:27,428 --> 00:06:30,515
they give you this platform demos and you get to give your tires around for a bit.
127
00:06:31,307 --> 00:06:33,643
And, you know, the performance is there,
128
00:06:33,643 --> 00:06:36,062
but then how does that mesh on a day to day basis?
129
00:06:36,062 --> 00:06:36,771
Right.
130
00:06:36,771 --> 00:06:39,899
You kind of do, the way that the PLC was handled.
131
00:06:40,274 --> 00:06:43,236
We were from day zero, be able to see, okay,
132
00:06:43,236 --> 00:06:46,239
this is how we would interact from scratch.
133
00:06:47,031 --> 00:06:50,201
It was the giveaways to see that Ames was really well,
134
00:06:50,201 --> 00:06:53,204
and we would like to move forward with this contract.
135
00:06:53,538 --> 00:06:57,834
You said from scratch, and I've heard that a number of times this week from Corps.
136
00:06:57,834 --> 00:07:00,837
We've engineers, leaders that they built
137
00:07:00,920 --> 00:07:04,006
the platform from scratch to be purpose built for AI.
138
00:07:04,340 --> 00:07:07,760
We've heard that from partners as well, like the Aston Martin Formula
139
00:07:07,760 --> 00:07:10,179
One team that they that built that team from scratch.
140
00:07:10,179 --> 00:07:11,889
Core is a part of that.
141
00:07:11,889 --> 00:07:14,183
You're in early production, I understand. Yeah.
142
00:07:14,183 --> 00:07:15,476
Talk about how that's going
143
00:07:15,476 --> 00:07:18,813
and what are some of the things that you are gleaning or learning so far?
144
00:07:19,564 --> 00:07:23,401
the team on for week has a ton of expertise in a lot of areas.
145
00:07:23,901 --> 00:07:26,571
So sometimes, I mean, we have our own experts as well,
146
00:07:26,571 --> 00:07:29,907
but sometimes we may be drawing a blank or seeking out an opinion.
147
00:07:29,907 --> 00:07:33,244
So for we've is obviously a cloud provider.
148
00:07:33,244 --> 00:07:36,205
So they can get information for other use cases
149
00:07:36,205 --> 00:07:38,082
and actually see what sticks and whatnot.
150
00:07:38,082 --> 00:07:41,878
So having that support there is it's a blessing.
151
00:07:42,295 --> 00:07:45,798
What our day to day operations like right now in early production.
152
00:07:46,924 --> 00:07:49,510
So it's it's not I can't say a lot to that.
153
00:07:49,510 --> 00:07:51,387
Basically we just
154
00:07:51,387 --> 00:07:55,099
throw our inferencing, you know workloads and everything works well.
155
00:07:55,266 --> 00:07:56,559
So far so good.
156
00:07:56,559 --> 00:07:58,519
We haven't had an issue yet. That's nice.
157
00:07:58,519 --> 00:08:02,106
So from an efficiency a productivity perspective it sounds like
158
00:08:02,106 --> 00:08:04,734
it's made a pretty big impact already.
159
00:08:04,734 --> 00:08:06,110
Yeah, it's been transparent.
160
00:08:06,110 --> 00:08:06,694
Basically
161
00:08:06,694 --> 00:08:09,864
you're working with other cloud providers who are running these workloads.
162
00:08:10,281 --> 00:08:11,282
Another stacks.
163
00:08:11,282 --> 00:08:14,285
And we just, you know, make the click and
164
00:08:14,827 --> 00:08:17,830
on running, you know, like we were never switching in the first place.
165
00:08:18,080 --> 00:08:20,958
Or most places like in your past experience, kind of like
166
00:08:20,958 --> 00:08:23,961
features are locked down used to give us access to the GPUs.
167
00:08:24,086 --> 00:08:27,924
Every feature was available and that's not normal or common.
168
00:08:28,049 --> 00:08:29,842
I wouldn't know if it's coming or not,
169
00:08:29,842 --> 00:08:32,845
but I've run into a few instances where features were gated.
170
00:08:33,221 --> 00:08:38,392
Features did not work the same way in the field, and then the final version,
171
00:08:39,477 --> 00:08:40,561
stuff like that happens.
172
00:08:40,561 --> 00:08:44,106
I, I'd like to say it's not common, but I've seen it time and time again.
173
00:08:44,148 --> 00:08:47,693
Yeah, well, maybe a refreshing experience that you've had with Huawei.
174
00:08:47,860 --> 00:08:49,737
You know, we were talking yesterday,
175
00:08:49,737 --> 00:08:53,324
with the Aston Martin F1 team and three things.
176
00:08:53,449 --> 00:08:56,452
The CMO Jean English as performance about core performance.
177
00:08:56,827 --> 00:08:59,705
Piece and partnership.
178
00:08:59,705 --> 00:09:03,834
And it sounds like that's what you're getting from this that partnership angle,
179
00:09:04,126 --> 00:09:07,922
the word transparency I think that's one of the words I,
180
00:09:08,548 --> 00:09:11,175
I think of when I think of core, we've and how they operate,
181
00:09:11,175 --> 00:09:14,011
because a lot of companies have trouble doing that.
182
00:09:14,011 --> 00:09:15,054
They don't.
183
00:09:15,054 --> 00:09:19,267
How is the the performance, the pace, the partnership really helped define
184
00:09:19,809 --> 00:09:23,062
your decision to choose core to your leaders.
185
00:09:23,938 --> 00:09:25,731
I think it's important that,
186
00:09:27,483 --> 00:09:28,693
or we miss our organization
187
00:09:28,693 --> 00:09:32,071
show from the get go any time we've had any issue,
188
00:09:32,572 --> 00:09:35,908
I don't think more than a couple of hours fast and feel we get a response.
189
00:09:37,493 --> 00:09:40,871
Whenever there was an issue, they did not try to hide what the issue was.
190
00:09:40,871 --> 00:09:44,000
They told us, hey, like this, this, that happened here, you know, like,
191
00:09:44,667 --> 00:09:48,379
a document detailing what actually happened, how they solved it.
192
00:09:48,379 --> 00:09:51,382
And you know, what to look out for in the future.
193
00:09:51,716 --> 00:09:53,843
So, right from the get go, everything is transparent.
194
00:09:53,843 --> 00:09:56,178
There's no like, oh, let me talk to my team,
195
00:09:56,178 --> 00:09:58,264
and they'll like, I'm in the corner and see what's what.
196
00:09:58,264 --> 00:09:58,973
No, no, no.
197
00:09:58,973 --> 00:10:01,976
We have a live one on one chat with everyone on slack.
198
00:10:02,310 --> 00:10:03,394
They tell us everything.
199
00:10:03,394 --> 00:10:05,688
24, seven and so far.
200
00:10:05,688 --> 00:10:07,773
And that's the way that we've been operating.
201
00:10:08,941 --> 00:10:09,775
So you have access
202
00:10:09,775 --> 00:10:12,778
to their direct to expert engineering team.
203
00:10:12,862 --> 00:10:14,530
You said slack, for example.
204
00:10:14,530 --> 00:10:19,577
Really getting, getting collaborating with you on the channel or with or with,
205
00:10:20,911 --> 00:10:22,330
you know, on organization.
206
00:10:22,330 --> 00:10:23,497
So whenever we need to chat
207
00:10:23,497 --> 00:10:27,627
with someone, you know, an expert on X, Y, and Z technology, they're there.
208
00:10:27,627 --> 00:10:30,171
You have I mean, there is a time difference, I'm sure.
209
00:10:30,171 --> 00:10:30,963
There we go. Yep.
210
00:10:30,963 --> 00:10:33,758
But they answer as soon as possible.
211
00:10:33,758 --> 00:10:36,385
From a user, a customer perspective.
212
00:10:36,385 --> 00:10:38,679
You know, we think of Mercado Libre, we think of Amazon.
213
00:10:38,679 --> 00:10:43,142
And and as consumers, we want to find whatever we want right away.
214
00:10:43,434 --> 00:10:48,022
We want them to show us relevant products and services.
215
00:10:48,272 --> 00:10:52,360
And, and the consumer is just becoming more and more demanding
216
00:10:52,860 --> 00:10:55,404
that that experience is seamless.
217
00:10:55,404 --> 00:11:00,159
So how what are some of the business outcomes in that context
218
00:11:00,576 --> 00:11:04,330
that you expect Mercado Libre to be able to deliver to those
219
00:11:04,330 --> 00:11:07,375
demanding customers because of the partnership with what we've.
220
00:11:08,417 --> 00:11:09,835
That's a great question.
221
00:11:09,835 --> 00:11:12,838
The results that we're trying to achieve is,
222
00:11:13,381 --> 00:11:16,550
as you mentioned, for the experience, the buying experience of our customers
223
00:11:16,550 --> 00:11:20,721
to actually be better, to actually get to what they're trying to buy.
224
00:11:20,930 --> 00:11:23,891
Sometimes not by asking the question, but by us
225
00:11:23,891 --> 00:11:26,852
knowing our customer can see all this talk about
226
00:11:27,228 --> 00:11:31,440
AI is capturing the context and truly knowing that customers
227
00:11:31,440 --> 00:11:33,401
to get deep down into what they actually mean.
228
00:11:33,401 --> 00:11:36,904
Yes, when they search for something and that's what we're trying to get it.
229
00:11:37,530 --> 00:11:41,075
It's something really easily measurable, you know,
230
00:11:41,409 --> 00:11:44,620
basically circumcision rate whenever we do something.
231
00:11:45,037 --> 00:11:48,290
And if they buy something, hey, back to what they were looking for, right?
232
00:11:49,208 --> 00:11:53,671
So in the next like 6 to 12 months, AI is moving so incredibly quickly.
233
00:11:53,963 --> 00:11:56,966
GTC, as you can see behind us this
234
00:11:57,007 --> 00:12:00,010
amazing time square, but the vibe is still great since day three.
235
00:12:00,344 --> 00:12:01,595
What are some of the things you're hoping
236
00:12:01,595 --> 00:12:05,099
in the next 6 to 12 months from an energetic perspective?
237
00:12:05,391 --> 00:12:10,521
To really help continue this business transformation, what's on your wish list?
238
00:12:11,689 --> 00:12:14,692
Honestly, I want to continue to see the
239
00:12:16,485 --> 00:12:17,194
the performance.
240
00:12:17,194 --> 00:12:22,533
For what better chance to introduce this whole new product for inferencing,
241
00:12:22,867 --> 00:12:25,870
where we can get a lot more tokens, more bang for our buck account?
242
00:12:25,953 --> 00:12:30,791
Yeah, because we are seeing some barriers, on the trading front.
243
00:12:30,875 --> 00:12:34,712
Okay, so once we get better inferencing performance,
244
00:12:35,463 --> 00:12:38,591
then we can really start doing better work on.
245
00:12:40,718 --> 00:12:43,387
On production for inferencing is real time.
246
00:12:43,387 --> 00:12:46,348
It's when the user is actually using your platform.
247
00:12:46,348 --> 00:12:50,102
And having better performance there allows us to think
248
00:12:50,102 --> 00:12:53,105
for more time to write more on what their needs are.
249
00:12:53,272 --> 00:12:56,275
So I'd really like to see that trend to continue to go further.
250
00:12:56,859 --> 00:12:59,695
It's exciting if there are any AI pioneers out there,
251
00:12:59,695 --> 00:13:03,407
and we know there are, and they're maybe embarking on a similar journey
252
00:13:03,991 --> 00:13:07,119
that you've done in the last year or so, what would you
253
00:13:07,411 --> 00:13:13,417
what's your three key takeaways be to advise them you got this. So
254
00:13:14,376 --> 00:13:14,919
I think the
255
00:13:14,919 --> 00:13:18,172
first one would be to try out something
256
00:13:18,172 --> 00:13:22,968
that is very near to your best to a non use case
257
00:13:23,636 --> 00:13:27,640
like try to work with something where you truly have a ton of metrics
258
00:13:28,015 --> 00:13:30,893
so that when you actually do something with the AI,
259
00:13:30,893 --> 00:13:33,896
you know, in a few seconds, if there's a good return, right?
260
00:13:34,271 --> 00:13:34,730
Yeah.
261
00:13:34,730 --> 00:13:36,982
Because otherwise you're just burning money, right?
262
00:13:36,982 --> 00:13:39,485
So having that use case really well established.
263
00:13:39,485 --> 00:13:42,154
And when you talk to your business,
264
00:13:42,154 --> 00:13:45,574
you can actually start seeing right away if there's any return there.
265
00:13:46,033 --> 00:13:49,370
So that's one of the things that we got started to actually send out
266
00:13:50,287 --> 00:13:52,540
where we,
267
00:13:52,540 --> 00:13:54,333
another one.
268
00:13:54,333 --> 00:13:57,503
there's a lot of hype around the AI and so much not unfounded,
269
00:13:57,670 --> 00:14:00,673
but really try to take a breath.
270
00:14:00,756 --> 00:14:04,885
There's a lot to learn and you can get started with simpler mechanisms.
271
00:14:04,885 --> 00:14:08,889
You do not need a full blown, you know, frontier model
272
00:14:08,889 --> 00:14:12,476
training with skill training on the fly with real time data.
273
00:14:12,685 --> 00:14:14,645
You do not need all of that from the get go.
274
00:14:14,645 --> 00:14:18,232
Know, patience and truly getting to know what you actually need.
275
00:14:18,649 --> 00:14:21,277
I think might be the best advice I can give at this point.
276
00:14:21,277 --> 00:14:25,030
I think that's fantastic advice because, you know, the speed with
277
00:14:25,030 --> 00:14:28,868
which air is accelerating is just can't even quantify it.
278
00:14:29,243 --> 00:14:32,246
And there's so many companies that are under pressure,
279
00:14:32,329 --> 00:14:35,499
as I mentioned, to move so fast.
280
00:14:36,000 --> 00:14:39,670
But you bring you bring up a great point like start small, identify
281
00:14:39,962 --> 00:14:42,840
the business processes where you're going to have
282
00:14:42,840 --> 00:14:46,302
metrics, measurable metrics where you can see the needle moving.
283
00:14:46,594 --> 00:14:49,430
And if it's not moving, start from scratch.
284
00:14:49,430 --> 00:14:50,306
Go somewhere else.
285
00:14:50,306 --> 00:14:51,932
Very start up minded in that way.
286
00:14:51,932 --> 00:14:53,642
Yeah. Failure.
287
00:14:53,642 --> 00:14:55,269
Yes. You're going to fail. Failure.
288
00:14:55,269 --> 00:14:59,064
So that you spend a as little as possible and move on to the next item
289
00:14:59,064 --> 00:15:00,274
and just iterate.
290
00:15:00,274 --> 00:15:03,277
Do you think that the culture of Mercado Libre
291
00:15:03,611 --> 00:15:06,280
is was important to have that startup
292
00:15:06,280 --> 00:15:09,283
small, fail fast mentality too, right. Yes.
293
00:15:09,408 --> 00:15:12,036
You create a lot of startups
294
00:15:12,036 --> 00:15:15,039
working in conjunction, so that fail fast.
295
00:15:15,247 --> 00:15:17,333
I mean, we call it continues beta.
296
00:15:17,333 --> 00:15:19,460
I love that continuous manner. Yeah.
297
00:15:19,460 --> 00:15:20,127
Oh yeah.
298
00:15:20,127 --> 00:15:23,380
That's how we interact with the future and every single day of how we work.
299
00:15:23,797 --> 00:15:25,382
That's a great continuous.
300
00:15:25,382 --> 00:15:26,592
That's a great approach.
301
00:15:26,592 --> 00:15:29,553
Last question for you, Sebastian GTC
302
00:15:30,095 --> 00:15:32,348
2026 30,000 plus people.
303
00:15:32,348 --> 00:15:35,351
People are calling this the AI Super Bowl.
304
00:15:35,351 --> 00:15:37,811
A carnival, the heartbeat of AI.
305
00:15:37,811 --> 00:15:41,732
What are your takeaways when you board a plane to go home to Chile
306
00:15:41,899 --> 00:15:45,611
that you've learned this week from, from NVIDIA, from its partner ecosystem,
307
00:15:45,611 --> 00:15:46,862
from core? We've.
308
00:15:46,862 --> 00:15:49,698
Well, first of all, I learned that the ecosystem is huge.
309
00:15:49,698 --> 00:15:51,283
And it was bigger than I actually
310
00:15:52,534 --> 00:15:53,327
is to.
311
00:15:53,327 --> 00:15:56,288
Right. Yeah. And it's on the growing. Yeah it's yeah.
312
00:15:56,288 --> 00:15:57,790
And the thing that I take to heart the most
313
00:15:57,790 --> 00:16:01,210
is that I've seen a lot of talks that I've engaged with the speakers
314
00:16:01,585 --> 00:16:05,422
is that the open source movement is especially prevalent nowadays,
315
00:16:05,756 --> 00:16:09,426
like everybody is trying to open source so that we can continue to grow
316
00:16:09,426 --> 00:16:13,263
as a business and not hiding behind closed doors especially.
317
00:16:13,555 --> 00:16:17,935
I talked to Jensen, Gabe, about open sourcing, a lot of the wall stuff
318
00:16:18,227 --> 00:16:19,561
and working through the engage
319
00:16:19,561 --> 00:16:22,564
with companies to be able to push the new forward path.
320
00:16:22,606 --> 00:16:26,026
Yeah, that spirit of the ecosystem is is only going to get bigger.
321
00:16:26,026 --> 00:16:30,531
I can't even imagine what we'll see at GTC 2027.
322
00:16:30,698 --> 00:16:33,993
I mean, the I think the possibilities are limitless.
323
00:16:33,993 --> 00:16:34,952
Well, Sebastian, thank you for
324
00:16:34,952 --> 00:16:38,497
joining us on the podcast today and sharing the Mercado Libre story.
325
00:16:38,914 --> 00:16:42,418
Your air use case, why you went to Core Weave
326
00:16:42,418 --> 00:16:44,378
and what it's enabling you to do so far,
327
00:16:44,378 --> 00:16:48,632
and also for sharing that really wise advice for those out there
328
00:16:48,632 --> 00:16:51,635
who are struggling with how do I deal with the pressure and the speed?
329
00:16:51,760 --> 00:16:54,263
Start small, fail fast.
330
00:16:54,263 --> 00:16:56,390
Really be prescriptive in your processes.
331
00:16:56,390 --> 00:16:58,767
We thank you so much for your insights. Glad to be here.
332
00:16:58,767 --> 00:17:01,353
All right. For Sebastian Yunge, I am Lisa Martin.
333
00:17:01,353 --> 00:17:04,148
We are coming to you live GTC day three.
334
00:17:04,148 --> 00:17:06,442
CoreWeave booth. Thanks for watching guys.
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
