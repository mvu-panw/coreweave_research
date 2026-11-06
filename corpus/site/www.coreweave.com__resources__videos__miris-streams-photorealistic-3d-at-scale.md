# Miris Streams Photorealistic 3D at Scale | CoreWeave Video

Source: https://www.coreweave.com/resources/videos/miris-streams-photorealistic-3d-at-scale

Announcement

Webinar

Podcast

GTC 2026

CoreWeave Forge is here: connect your AI loop and compound every improvement. Read more

Contact us

Copied

Overview
Transcript

### Miris Streams Photorealistic 3D in Real Time
Part of the Who’s Ready for Anything series, this episode features Miris Chief Product Officer Will McDonald at NVIDIA GTC 2026. Learn how AI is accelerating 3D content creation—and how Miris streams photorealistic experiences at scale using CoreWeave Cloud.
In this video:
- Why generative AI is driving a surge in 3D content creation
- How Miris delivers high-fidelity 3D without sacrificing scale or performance
- The architectural shift from real-time rendering to streaming volumetric content
- How to prepare for the next wave of spatial and AI-driven applications

00:00

1
00:00:12,929 --> 00:00:13,596
Welcome back to
2
00:00:13,596 --> 00:00:15,473
GTC live Day two
3
00:00:15,473 --> 00:00:17,600
Lisa Martin here with CoreWeave.
4
00:00:17,600 --> 00:00:20,061
You can see some of the energy behind me.
5
00:00:20,061 --> 00:00:22,272
And I gotta tell you, as I've said before
6
00:00:22,272 --> 00:00:23,106
saying it's electric.
7
00:00:23,106 --> 00:00:24,024
I gotta find a new word
8
00:00:24,024 --> 00:00:25,734
because this is next level.
9
00:00:25,734 --> 00:00:27,652
This is the Super Bowl for AI.
10
00:00:27,652 --> 00:00:28,737
People have been describing it
11
00:00:28,737 --> 00:00:31,406
as a carnival, as the heartbeat of AI.
12
00:00:31,406 --> 00:00:32,907
It's all true.
13
00:00:32,907 --> 00:00:34,159
Super excited to be joined
14
00:00:34,159 --> 00:00:37,620
by Miris, Will McDonald the Chief Product Officer.
15
00:00:37,620 --> 00:00:38,455
Well, thank you so much
16
00:00:38,455 --> 00:00:39,330
for spending some time with us.
17
00:00:39,330 --> 00:00:39,748
I caught you
18
00:00:39,748 --> 00:00:41,207
as part of your presentation
19
00:00:41,207 --> 00:00:42,876
and the with yesterday.
20
00:00:42,876 --> 00:00:44,753
Yeah. Thanks for having me.
21
00:00:44,753 --> 00:00:46,212
You are such a cool background,
22
00:00:46,212 --> 00:00:47,881
and I want the audience to know this.
23
00:00:47,881 --> 00:00:52,427
You worked at ILM, Pixar, unity, AWS.
24
00:00:52,552 --> 00:00:53,678
Now you're building
25
00:00:53,678 --> 00:00:55,180
streaming infrastructure
26
00:00:55,180 --> 00:00:57,390
for photorealistic 3D mirrors.
27
00:00:57,390 --> 00:01:00,727
What drew you to to Miris last year?
28
00:01:01,352 --> 00:01:01,978
Yeah. It's funny.
29
00:01:01,978 --> 00:01:03,855
You know, you name all those companies.
30
00:01:03,855 --> 00:01:05,815
I was thinking about that the other day.
31
00:01:05,815 --> 00:01:07,150
Someone might look at my background.
32
00:01:07,150 --> 00:01:07,525
I was like, wow,
33
00:01:07,525 --> 00:01:09,110
this person has shiny objects and
34
00:01:10,904 --> 00:01:12,113
all these different roles and
35
00:01:12,113 --> 00:01:13,740
all these exciting companies,
36
00:01:13,740 --> 00:01:14,991
and I've really had a
37
00:01:14,991 --> 00:01:15,992
really exciting career.
38
00:01:15,992 --> 00:01:17,410
It's been a lot of fun for me.
39
00:01:17,410 --> 00:01:17,619
You know,
40
00:01:17,619 --> 00:01:18,661
I was thinking about
41
00:01:18,661 --> 00:01:21,081
how the common thread connected
42
00:01:21,081 --> 00:01:22,624
amid all those experiences.
43
00:01:22,624 --> 00:01:23,958
And at the heart of it,
44
00:01:23,958 --> 00:01:25,627
I just really like being in a place
45
00:01:25,627 --> 00:01:26,419
where I can help
46
00:01:26,419 --> 00:01:28,505
co-creators and technologists
47
00:01:28,505 --> 00:01:30,632
actually deliver what they wanted to
48
00:01:30,632 --> 00:01:31,883
build, what they want to build.
49
00:01:31,883 --> 00:01:34,094
So that's been kind of the common thread,
50
00:01:34,094 --> 00:01:36,179
starting when I was at Lucasfilm,
51
00:01:36,179 --> 00:01:36,679
all the way
52
00:01:36,679 --> 00:01:38,848
past working today with Miris.
53
00:01:38,848 --> 00:01:40,475
It's interesting the,
54
00:01:40,475 --> 00:01:41,601
you know, earlier in my career,
55
00:01:41,601 --> 00:01:43,520
I was really focused on
56
00:01:43,520 --> 00:01:45,897
how do I help artists really create
57
00:01:45,897 --> 00:01:47,398
amazing things on screen
58
00:01:47,398 --> 00:01:49,234
or amazing experiences.
59
00:01:49,234 --> 00:01:49,859
And one of the things
60
00:01:49,859 --> 00:01:51,027
that led me to Miris,
61
00:01:51,027 --> 00:01:52,862
like fast forwarding to today, is
62
00:01:52,862 --> 00:01:54,614
how do I help people actually deliver
63
00:01:54,614 --> 00:01:55,907
that content at scale?
64
00:01:55,907 --> 00:01:57,951
You built all this amazing work.
65
00:01:57,951 --> 00:01:58,493
How do you get it
66
00:01:58,493 --> 00:02:00,036
to where it needs to be?
67
00:02:00,036 --> 00:02:00,537
So yeah, it's been
68
00:02:00,537 --> 00:02:02,455
to have a nice little full circle
69
00:02:02,455 --> 00:02:03,164
sort of moment.
70
00:02:03,164 --> 00:02:04,415
Like I started
71
00:02:04,415 --> 00:02:05,834
on the creation side
72
00:02:05,834 --> 00:02:06,501
and now I'm over
73
00:02:06,501 --> 00:02:08,336
on the distribution side.
74
00:02:08,336 --> 00:02:11,339
I think it's fun when you think back to
75
00:02:11,422 --> 00:02:12,715
a career that may look zig zaggy.
76
00:02:12,715 --> 00:02:13,424
I have the same thing
77
00:02:13,424 --> 00:02:14,759
I started at NASA back in the day,
78
00:02:14,759 --> 00:02:15,760
and now here I am.
79
00:02:15,760 --> 00:02:17,428
But there are common threads
80
00:02:17,428 --> 00:02:18,680
and I think when you discover those,
81
00:02:18,680 --> 00:02:20,515
I think it just empowers you
82
00:02:20,515 --> 00:02:21,891
to to want to do
83
00:02:21,891 --> 00:02:24,060
an even better job for your customers.
84
00:02:24,060 --> 00:02:24,602
Well, CoreWeave
85
00:02:24,602 --> 00:02:26,020
has this brand new brand
86
00:02:26,020 --> 00:02:27,981
campaign called Ready for Anything.
87
00:02:27,981 --> 00:02:30,984
I want to you to kind of walk us back
88
00:02:30,984 --> 00:02:33,987
when you were doing R&D for ILM or Pixar,
89
00:02:34,404 --> 00:02:35,780
what did ready for
90
00:02:35,780 --> 00:02:36,865
anything infrastructure...
91
00:02:36,865 --> 00:02:38,158
What did it mean,
92
00:02:38,158 --> 00:02:38,992
what does it look like
93
00:02:38,992 --> 00:02:40,118
behind the scenes back then?
94
00:02:40,118 --> 00:02:40,618
Oh wow.
95
00:02:40,618 --> 00:02:41,744
There's so many stories
96
00:02:41,744 --> 00:02:42,829
I could tell about that.
97
00:02:42,829 --> 00:02:43,121
You know,
98
00:02:43,121 --> 00:02:44,706
the interesting thing about
99
00:02:44,706 --> 00:02:45,707
film production,
100
00:02:45,707 --> 00:02:48,960
be it for VFX or be it for animation,
101
00:02:49,460 --> 00:02:50,545
is ultimately
102
00:02:50,545 --> 00:02:52,630
you're not shipping software.
103
00:02:52,630 --> 00:02:54,465
You're shipping pixels.
104
00:02:54,465 --> 00:02:56,634
All that matters is
105
00:02:56,634 --> 00:02:58,553
how it looks on the screen
106
00:02:58,553 --> 00:02:59,679
or what you're interacting
107
00:02:59,679 --> 00:03:01,139
with in a game.
108
00:03:01,139 --> 00:03:02,432
So oftentimes
109
00:03:02,432 --> 00:03:04,767
production ends up being really messy
110
00:03:04,767 --> 00:03:06,352
from a technology standpoint.
111
00:03:06,352 --> 00:03:08,104
You're building tools that oftentimes
112
00:03:08,104 --> 00:03:09,564
you're having to throw out quickly
113
00:03:09,564 --> 00:03:11,608
because it's just used to solve
114
00:03:11,608 --> 00:03:12,442
a particular problem,
115
00:03:12,442 --> 00:03:14,360
one problem for one shot, right?
116
00:03:14,360 --> 00:03:16,529
And then after that, off it goes.
117
00:03:16,529 --> 00:03:16,696
You know
118
00:03:16,696 --> 00:03:17,697
we're always trying to do our best
119
00:03:17,697 --> 00:03:18,406
to build things
120
00:03:18,406 --> 00:03:20,575
that are more generalized, that work
121
00:03:20,575 --> 00:03:22,535
for lots of different spaces.
122
00:03:22,535 --> 00:03:24,120
But in production, where in the end
123
00:03:24,120 --> 00:03:25,622
you just need to get it on the screen
124
00:03:25,622 --> 00:03:26,122
and looks
125
00:03:26,122 --> 00:03:27,207
really, really good,
126
00:03:27,207 --> 00:03:28,291
you're kind of doing whatever
127
00:03:28,291 --> 00:03:29,876
it takes to do that.
128
00:03:29,876 --> 00:03:32,128
So that was always a lot of fun,
129
00:03:32,128 --> 00:03:33,129
being able to do that.
130
00:03:33,129 --> 00:03:36,132
Like working with creatives
131
00:03:36,174 --> 00:03:37,342
who are really just,
132
00:03:37,342 --> 00:03:38,843
you know, at the height of their powers,
133
00:03:38,843 --> 00:03:41,304
building incredible content.
134
00:03:41,304 --> 00:03:42,513
I've always just loved
135
00:03:42,513 --> 00:03:44,724
helping that sort of person
136
00:03:44,724 --> 00:03:45,642
realize what they want to realize
137
00:03:45,642 --> 00:03:46,434
in terms of content.
138
00:03:46,434 --> 00:03:48,019
I imagine that they're very
139
00:03:48,019 --> 00:03:49,187
inspirational to you
140
00:03:49,187 --> 00:03:51,022
because they have these grand visions
141
00:03:51,022 --> 00:03:53,316
that they want to see brought to life.
142
00:03:53,316 --> 00:03:54,859
And you got to figure out how to do that.
143
00:03:54,859 --> 00:03:55,652
But I imagine
144
00:03:55,652 --> 00:03:57,320
the momentum that they kind of
145
00:03:57,320 --> 00:03:59,155
carry forward is inspiring.
146
00:03:59,155 --> 00:04:00,448
It is. Absolutely.
147
00:04:00,448 --> 00:04:02,283
And so, like your earlier question,
148
00:04:02,283 --> 00:04:04,285
kind of what brought me to Miris,
149
00:04:04,285 --> 00:04:05,036
like a lot of the things
150
00:04:05,036 --> 00:04:06,746
I was noticing and a lot of folks in
151
00:04:06,746 --> 00:04:08,623
Miris have noticed the same inspired
152
00:04:08,623 --> 00:04:11,334
a lot of us from VFX and animation
153
00:04:11,334 --> 00:04:13,670
and from the cloud world and so on.
154
00:04:13,670 --> 00:04:15,088
Like, one of the things that we noticed
155
00:04:15,088 --> 00:04:17,090
is that people can build
156
00:04:17,090 --> 00:04:19,801
and visualize incredible work, right?
157
00:04:19,801 --> 00:04:21,386
But then when it comes time
158
00:04:21,386 --> 00:04:22,971
to actually getting it to where it needs
159
00:04:22,971 --> 00:04:25,181
to be really, really quickly
160
00:04:25,181 --> 00:04:26,432
and at scale,
161
00:04:26,432 --> 00:04:27,100
they're kind of stuck
162
00:04:27,100 --> 00:04:29,394
between these two options, either
163
00:04:29,394 --> 00:04:31,354
decimating it down into like a web
164
00:04:31,354 --> 00:04:33,314
format that can render in the browser,
165
00:04:33,314 --> 00:04:34,315
or they're doing things
166
00:04:34,315 --> 00:04:35,400
like pixel streaming
167
00:04:35,400 --> 00:04:37,610
where they really just can't scale up
168
00:04:37,610 --> 00:04:39,612
to like a consumer grade internet.
169
00:04:39,612 --> 00:04:40,905
And so we thought, hey,
170
00:04:40,905 --> 00:04:41,531
how can we help
171
00:04:41,531 --> 00:04:42,949
creators and developers
172
00:04:42,949 --> 00:04:44,242
actually be able to reach
173
00:04:44,242 --> 00:04:45,493
that billion user scale,
174
00:04:45,493 --> 00:04:47,203
be able to deliver really,
175
00:04:47,203 --> 00:04:49,247
really nice looking content
176
00:04:49,247 --> 00:04:50,748
without compromise?
177
00:04:50,748 --> 00:04:52,208
So yeah, again, like one of the reasons
178
00:04:52,208 --> 00:04:53,543
I'm really excited about being in
179
00:04:53,543 --> 00:04:54,794
Miris is like,
180
00:04:54,794 --> 00:04:56,129
this allows us to help
181
00:04:56,129 --> 00:04:58,589
the right set of creators and developers
182
00:04:58,589 --> 00:04:59,132
realize that.
183
00:04:59,132 --> 00:05:00,717
Without compromise,
184
00:05:00,717 --> 00:05:01,759
that's kind a kind of a key thing
185
00:05:01,759 --> 00:05:02,510
that you mentioned.
186
00:05:02,510 --> 00:05:05,555
When we think about VFX, 3D pipelines,
187
00:05:06,139 --> 00:05:06,806
they've always been
188
00:05:06,806 --> 00:05:08,308
really compute intensive,
189
00:05:08,308 --> 00:05:10,435
but now enter AI.
190
00:05:10,435 --> 00:05:13,438
How is it changing the game in real time?
191
00:05:13,479 --> 00:05:14,063
Yeah, I mean,
192
00:05:14,063 --> 00:05:15,189
I came from a world,
193
00:05:15,189 --> 00:05:16,816
particularly with vFX,
194
00:05:16,816 --> 00:05:18,359
it's very CPU bound.
195
00:05:18,359 --> 00:05:20,320
A lot of the render engines
196
00:05:20,320 --> 00:05:22,071
hadn’t started to leverage GPUs.
197
00:05:22,071 --> 00:05:24,157
And then going back to kind the idea
198
00:05:24,157 --> 00:05:25,992
that it's never really been
199
00:05:25,992 --> 00:05:27,201
so much about the how,
200
00:05:27,201 --> 00:05:27,660
per se,
201
00:05:27,660 --> 00:05:29,037
it's all been about
202
00:05:29,037 --> 00:05:31,497
how do we get the best pixels on screen.
203
00:05:31,497 --> 00:05:32,332
So when we start thinking
204
00:05:32,332 --> 00:05:33,499
about factoring in things
205
00:05:33,499 --> 00:05:34,792
like generative AI,
206
00:05:34,792 --> 00:05:37,795
and AI just more broadly, it's all about
207
00:05:38,254 --> 00:05:39,088
are they produce
208
00:05:39,088 --> 00:05:40,214
or are they providing
209
00:05:40,214 --> 00:05:42,175
tooling in a way of being able
210
00:05:42,175 --> 00:05:43,760
to get to that final image?
211
00:05:43,760 --> 00:05:45,887
That's just like a really exciting time,
212
00:05:45,887 --> 00:05:46,304
I think,
213
00:05:46,304 --> 00:05:47,889
in the industry at large,
214
00:05:47,889 --> 00:05:50,516
not only for VFX and animation,
215
00:05:50,516 --> 00:05:51,976
but also more broadly into things
216
00:05:51,976 --> 00:05:53,770
like physical AI,
217
00:05:53,770 --> 00:05:55,772
digital twins, retail, right?
218
00:05:55,772 --> 00:05:56,314
Like they're all
219
00:05:57,482 --> 00:05:58,649
similar sort of problems,
220
00:05:58,649 --> 00:05:59,400
which is like, you know,
221
00:05:59,400 --> 00:06:02,362
if I'm a, retailer or a brand,
222
00:06:02,487 --> 00:06:05,448
Sameh Louis Vuitton or I feed Spain,
223
00:06:05,448 --> 00:06:06,574
I want to be a little bit
224
00:06:06,574 --> 00:06:09,577
show the, or the products that I have
225
00:06:09,744 --> 00:06:11,120
and the best way possible.
226
00:06:11,120 --> 00:06:13,206
I want things like the fabrics
227
00:06:13,206 --> 00:06:14,665
to really come through.
228
00:06:14,665 --> 00:06:15,833
I might not be doing that.
229
00:06:15,833 --> 00:06:17,085
And so a lot of these companies
230
00:06:17,085 --> 00:06:20,088
are leveraging traditional 3D approaches,
231
00:06:20,088 --> 00:06:20,421
like what
232
00:06:20,421 --> 00:06:23,424
we've used in VFX animation for ages
233
00:06:23,466 --> 00:06:24,801
alongside generative
234
00:06:24,801 --> 00:06:26,094
AI approaches,
235
00:06:26,094 --> 00:06:27,178
and that convergence
236
00:06:27,178 --> 00:06:29,097
of technology together for music.
237
00:06:29,097 --> 00:06:30,973
Really exciting results.
238
00:06:30,973 --> 00:06:31,391
I love that
239
00:06:31,391 --> 00:06:32,975
you mentioned some brands
240
00:06:32,975 --> 00:06:36,062
and I'm fans, but this is more than VFX.
241
00:06:36,479 --> 00:06:37,772
This is and
242
00:06:37,772 --> 00:06:39,690
this is really transcendental
243
00:06:39,690 --> 00:06:41,067
across industries.
244
00:06:41,067 --> 00:06:42,777
Yes, we were with the Aston
245
00:06:42,777 --> 00:06:44,612
Martin Formula one folks this morning.
246
00:06:44,612 --> 00:06:46,030
Call this a sponsor of the team.
247
00:06:46,030 --> 00:06:47,240
And they got one fan.
248
00:06:47,240 --> 00:06:49,575
And one of the things that struck me
249
00:06:49,575 --> 00:06:50,952
is that
250
00:06:50,952 --> 00:06:53,871
what happens in the AI race at F1 races
251
00:06:53,871 --> 00:06:54,956
and with the car
252
00:06:54,956 --> 00:06:58,376
is so influential in other industries.
253
00:06:58,709 --> 00:07:00,628
Talk more about the parallels there.
254
00:07:00,628 --> 00:07:03,923
You mentioned your experiences with VFX,
255
00:07:03,923 --> 00:07:04,799
3D pipelines,
256
00:07:04,799 --> 00:07:07,176
but you also mentioned retail commerce.
257
00:07:07,176 --> 00:07:09,971
Yeah, physical. Are the next frontier.
258
00:07:09,971 --> 00:07:12,181
Walk me through how Miris is helping
259
00:07:12,181 --> 00:07:14,183
those types of organizations
260
00:07:14,183 --> 00:07:16,144
truly accelerate in this age of AI,
261
00:07:16,144 --> 00:07:17,895
and to be able to not compromise,
262
00:07:17,895 --> 00:07:18,604
as you said.
263
00:07:18,604 --> 00:07:19,313
That's right. Yeah.
264
00:07:19,313 --> 00:07:20,106
I mean, I've always been
265
00:07:20,106 --> 00:07:21,315
a really big believer,
266
00:07:21,315 --> 00:07:22,316
no matter
267
00:07:22,316 --> 00:07:23,901
where I've been throughout my career,
268
00:07:23,901 --> 00:07:25,027
and Miris in particular,
269
00:07:25,027 --> 00:07:25,820
in that
270
00:07:25,820 --> 00:07:26,988
the best way to drive
271
00:07:26,988 --> 00:07:29,157
innovation is alongside a customer.
272
00:07:29,157 --> 00:07:31,075
So like when you see innovation
273
00:07:31,075 --> 00:07:32,660
for like an F1,
274
00:07:32,660 --> 00:07:33,453
they're trying to solve
275
00:07:33,453 --> 00:07:35,746
very particular business problems
276
00:07:35,746 --> 00:07:37,081
and they're innovating their way
277
00:07:37,081 --> 00:07:37,498
through that,
278
00:07:37,498 --> 00:07:38,958
which is always just so exciting
279
00:07:38,958 --> 00:07:40,001
to see that sort of thing take shape.
280
00:07:40,001 --> 00:07:40,918
Yeah, yeah,
281
00:07:40,918 --> 00:07:42,545
certainly when I was at industrial,
282
00:07:42,545 --> 00:07:44,005
like magic places
283
00:07:44,005 --> 00:07:45,506
like Electronic Arts
284
00:07:45,506 --> 00:07:46,090
again, like we're
285
00:07:46,090 --> 00:07:47,967
just trying to get like the end product,
286
00:07:47,967 --> 00:07:49,135
the end result.
287
00:07:49,135 --> 00:07:50,595
And there's like a lot of innovation
288
00:07:50,595 --> 00:07:53,139
that takes place as part of that.
289
00:07:53,139 --> 00:07:54,056
I found that,
290
00:07:54,056 --> 00:07:57,018
you know, in unity or at Amazon,
291
00:07:57,018 --> 00:07:57,810
the best way
292
00:07:57,810 --> 00:07:59,061
we were able to really drive,
293
00:07:59,061 --> 00:07:59,896
like a lot of big
294
00:07:59,896 --> 00:08:01,397
leaps in our technology,
295
00:08:01,397 --> 00:08:02,315
is really around
296
00:08:02,315 --> 00:08:03,566
finding those customers
297
00:08:03,566 --> 00:08:04,859
that are trying to do
298
00:08:04,859 --> 00:08:05,818
things that have never been done
299
00:08:05,818 --> 00:08:06,569
before or had,
300
00:08:06,569 --> 00:08:09,197
like a really gnarly scale problem
301
00:08:09,197 --> 00:08:12,200
or a speed problem problem, you name it.
302
00:08:12,617 --> 00:08:13,659
Like jumping in there
303
00:08:13,659 --> 00:08:14,744
headfirst into the customer
304
00:08:14,744 --> 00:08:16,412
to be able to solve that together.
305
00:08:16,412 --> 00:08:17,205
That's where you see
306
00:08:17,205 --> 00:08:18,164
the really interesting
307
00:08:18,164 --> 00:08:19,749
technology innovation.
308
00:08:19,749 --> 00:08:21,626
Like doing it in common Ivory tower.
309
00:08:21,626 --> 00:08:23,586
People can do that and you can see
310
00:08:23,586 --> 00:08:25,129
interesting things from that.
311
00:08:25,129 --> 00:08:26,547
But the rubber really hits the road
312
00:08:26,547 --> 00:08:27,590
when you've got a partner
313
00:08:27,590 --> 00:08:30,051
or a customer can be with together.
314
00:08:30,051 --> 00:08:31,511
Yeah. That shared vision.
315
00:08:31,511 --> 00:08:33,596
Absolutely. Well it's motivating.
316
00:08:33,596 --> 00:08:34,430
It's inspiring.
317
00:08:34,430 --> 00:08:36,682
It's it's probably helping you push past
318
00:08:36,682 --> 00:08:37,934
what we thought was possible
319
00:08:37,934 --> 00:08:38,726
because there's there's
320
00:08:38,726 --> 00:08:40,436
a strong demand for it
321
00:08:40,436 --> 00:08:41,938
in these other industries.
322
00:08:41,938 --> 00:08:42,772
What is driving
323
00:08:42,772 --> 00:08:46,108
the demand for spatial content in retail
324
00:08:46,108 --> 00:08:49,278
and in, physical AI in commerce?
325
00:08:49,278 --> 00:08:50,863
Yeah, there's a common thread.
326
00:08:50,863 --> 00:08:52,573
I have a fun little story about this.
327
00:08:52,573 --> 00:08:54,408
So it actually is tied to
328
00:08:54,408 --> 00:08:55,952
why I came to Microsoft.
329
00:08:55,952 --> 00:08:57,995
So not a year ago.
330
00:08:57,995 --> 00:09:00,665
I have a ten year old and a five year old
331
00:09:00,665 --> 00:09:01,290
at best. Boy.
332
00:09:02,333 --> 00:09:03,543
I walk into my ten year old
333
00:09:03,543 --> 00:09:04,335
into his room
334
00:09:04,335 --> 00:09:05,795
and he's at his computer
335
00:09:05,795 --> 00:09:07,797
and he's making 3D content, right.
336
00:09:07,797 --> 00:09:10,383
So I went to school to make 3D content,
337
00:09:10,383 --> 00:09:12,051
you know, four year college.
338
00:09:12,051 --> 00:09:13,344
Like I'm learning all these tools,
339
00:09:13,344 --> 00:09:14,679
like my, blender.
340
00:09:14,679 --> 00:09:16,556
Yeah, everything about materials
341
00:09:16,556 --> 00:09:16,973
and lighting.
342
00:09:16,973 --> 00:09:18,015
It's quite technical, right?
343
00:09:18,015 --> 00:09:19,267
It always has that.
344
00:09:19,267 --> 00:09:19,642
And here
345
00:09:19,642 --> 00:09:20,518
I catch my ten year
346
00:09:20,518 --> 00:09:21,894
old using one of these generative
347
00:09:21,894 --> 00:09:23,396
AI tools to make, like,
348
00:09:23,396 --> 00:09:26,107
very convincing 3D content, like, wow,
349
00:09:26,107 --> 00:09:27,441
this is amazing, right?
350
00:09:27,441 --> 00:09:30,278
And it dawned on me in that moment that
351
00:09:30,278 --> 00:09:31,445
what we're about to see
352
00:09:31,445 --> 00:09:32,738
and what's already here, it's
353
00:09:32,738 --> 00:09:33,197
just this
354
00:09:33,197 --> 00:09:34,282
absolutely tidal
355
00:09:34,282 --> 00:09:35,783
wave of 3D content,
356
00:09:35,783 --> 00:09:38,160
because this barrier of entry
357
00:09:38,160 --> 00:09:41,080
to creating the content is lowering.
358
00:09:41,080 --> 00:09:41,581
Yes.
359
00:09:41,581 --> 00:09:43,416
It kind of reminds me of
360
00:09:43,416 --> 00:09:43,833
you know,
361
00:09:43,833 --> 00:09:45,543
the democratization of video
362
00:09:45,543 --> 00:09:47,920
that happened at the early March 2000.
363
00:09:47,920 --> 00:09:48,421
That's right.
364
00:09:48,421 --> 00:09:48,629
Yeah.
365
00:09:48,629 --> 00:09:50,172
All things like video
366
00:09:50,172 --> 00:09:53,175
cameras and, video editing software
367
00:09:53,426 --> 00:09:54,760
like The Price has Come down
368
00:09:54,760 --> 00:09:56,053
become accessible, right?
369
00:09:56,053 --> 00:09:56,971
Since, like me,
370
00:09:56,971 --> 00:09:59,181
like younger, like picking up camcorders
371
00:09:59,181 --> 00:10:00,891
and making their movies and editing them.
372
00:10:00,891 --> 00:10:01,100
Yeah.
373
00:10:01,100 --> 00:10:02,310
And they worked all of that, right?
374
00:10:02,310 --> 00:10:03,853
Those things like YouTube
375
00:10:03,853 --> 00:10:05,187
and Twitch text.
376
00:10:05,187 --> 00:10:06,355
Yeah. Netflix.
377
00:10:06,355 --> 00:10:07,189
On and on it goes.
378
00:10:07,189 --> 00:10:08,608
Because the amount of content
379
00:10:08,608 --> 00:10:10,901
being created just, oh, rocketed.
380
00:10:10,901 --> 00:10:11,861
And then all of a sudden people
381
00:10:11,861 --> 00:10:13,613
wanted more channels of distribution.
382
00:10:13,613 --> 00:10:16,115
Discord. Substack. Yep yep yep.
383
00:10:16,115 --> 00:10:18,409
So, you know, fast forward to Boris.
384
00:10:18,409 --> 00:10:18,868
Like, now
385
00:10:18,868 --> 00:10:20,161
that I'm seeing this tidal wave
386
00:10:20,161 --> 00:10:22,163
on the content creation side
387
00:10:22,163 --> 00:10:22,872
really increased
388
00:10:22,872 --> 00:10:23,748
because of generative
389
00:10:23,748 --> 00:10:25,916
AI and everything going on there.
390
00:10:25,916 --> 00:10:27,668
There's just this amazing opportunity
391
00:10:27,668 --> 00:10:29,128
to kind of catch me
392
00:10:29,128 --> 00:10:30,379
downstream of this tidal
393
00:10:30,379 --> 00:10:31,756
wave and catch that.
394
00:10:31,756 --> 00:10:32,423
And so I really,
395
00:10:32,423 --> 00:10:33,215
really tried to solve
396
00:10:33,215 --> 00:10:34,842
that problem of like, hey,
397
00:10:34,842 --> 00:10:36,177
you got all this content
398
00:10:36,177 --> 00:10:37,219
being created by,
399
00:10:37,219 --> 00:10:39,180
you know, people that are always been
400
00:10:39,180 --> 00:10:40,765
incredibly talented around
401
00:10:40,765 --> 00:10:42,141
or even the new creators
402
00:10:42,141 --> 00:10:42,683
that they don't have
403
00:10:42,683 --> 00:10:43,434
any experience with it.
404
00:10:43,434 --> 00:10:44,352
I mean, the
405
00:10:44,352 --> 00:10:45,895
the content creator gig
406
00:10:45,895 --> 00:10:47,730
economy is massively growing.
407
00:10:47,730 --> 00:10:48,939
It's just like
408
00:10:48,939 --> 00:10:50,858
that barrier of entry is lowering where,
409
00:10:50,858 --> 00:10:51,984
you know, I wouldn't be surprised.
410
00:10:51,984 --> 00:10:54,528
You know, my mom increased my 3D content.
411
00:10:54,528 --> 00:10:57,365
Shout out to my mom like she
412
00:10:57,365 --> 00:10:58,282
because my mom is too.
413
00:10:58,282 --> 00:10:59,992
Oh she is. She calls it shut ABC.
414
00:10:59,992 --> 00:11:01,410
But I know what she's talking about.
415
00:11:01,410 --> 00:11:02,912
Oh, that was amazing.
416
00:11:02,912 --> 00:11:04,288
Yeah, I love that.
417
00:11:04,288 --> 00:11:05,706
Tools like that,
418
00:11:05,706 --> 00:11:06,707
like that barrier of entry
419
00:11:06,707 --> 00:11:08,292
and using them is so low.
420
00:11:08,292 --> 00:11:10,795
So when I see that happening for 3D,
421
00:11:10,795 --> 00:11:12,922
it's just a really exciting time to say,
422
00:11:12,922 --> 00:11:13,964
how do we help people
423
00:11:13,964 --> 00:11:16,175
create that at scale? Right.
424
00:11:16,175 --> 00:11:16,884
And that's always been
425
00:11:16,884 --> 00:11:18,344
a bit of the problem
426
00:11:18,344 --> 00:11:20,179
when you're either stuck
427
00:11:20,179 --> 00:11:21,806
decimating your content to be able
428
00:11:21,806 --> 00:11:23,099
to distribute that at scale
429
00:11:23,099 --> 00:11:24,266
and then wait for the downside
430
00:11:24,266 --> 00:11:26,102
and then you compromise, right?
431
00:11:26,102 --> 00:11:27,645
Yeah. Yeah. Quality.
432
00:11:27,645 --> 00:11:28,270
Yeah, yeah.
433
00:11:28,270 --> 00:11:29,480
You're compromising quality
434
00:11:29,480 --> 00:11:31,941
or you're compromising scale.
435
00:11:31,941 --> 00:11:32,358
Right.
436
00:11:32,358 --> 00:11:34,318
And so again, we're kind of in that
437
00:11:34,318 --> 00:11:35,778
like big fat middle
438
00:11:35,778 --> 00:11:36,487
where
439
00:11:36,487 --> 00:11:38,072
we're able to provide like that
440
00:11:38,072 --> 00:11:39,949
really high fidelity content,
441
00:11:39,949 --> 00:11:40,783
but then be able
442
00:11:40,783 --> 00:11:42,368
to uphold things like scale
443
00:11:42,368 --> 00:11:44,120
and then have like 2D economics
444
00:11:44,120 --> 00:11:46,706
and so on. Yeah, it's exciting to talk.
445
00:11:46,706 --> 00:11:47,832
I mentioned that I caught
446
00:11:47,832 --> 00:11:48,833
some of your presentation
447
00:11:48,833 --> 00:11:49,750
downstairs in the car.
448
00:11:49,750 --> 00:11:50,793
We did talk to me
449
00:11:50,793 --> 00:11:52,002
about the CoreWeave partnership.
450
00:11:52,002 --> 00:11:52,586
What are they
451
00:11:52,586 --> 00:11:54,296
how are they enabling you
452
00:11:54,296 --> 00:11:56,215
to enable the creators
453
00:11:56,215 --> 00:11:58,718
to just do what's in their minds?
454
00:11:58,718 --> 00:11:59,176
Yeah.
455
00:11:59,176 --> 00:11:59,844
You know,
456
00:11:59,844 --> 00:12:00,594
the things I mentioned
457
00:12:00,594 --> 00:12:02,179
in my presentation,
458
00:12:02,179 --> 00:12:03,681
there's no for 20 years anymore.
459
00:12:03,681 --> 00:12:05,933
We keep you awake.
460
00:12:05,933 --> 00:12:06,892
The key unlock.
461
00:12:06,892 --> 00:12:08,060
And the reason why we partner
462
00:12:08,060 --> 00:12:09,478
so closely with CoreWeave,
463
00:12:09,478 --> 00:12:10,730
yes it's the GPUs,
464
00:12:10,730 --> 00:12:13,357
but it's actually the platform
465
00:12:13,357 --> 00:12:14,567
as a whole, right?
466
00:12:14,567 --> 00:12:16,736
Like you can go and rent cloud
467
00:12:16,736 --> 00:12:19,155
GPUs from anywhere if you want to.
468
00:12:19,155 --> 00:12:20,322
But like the magic of flex,
469
00:12:20,322 --> 00:12:21,866
where we bring in while we're partners
470
00:12:21,866 --> 00:12:23,242
so closely with them
471
00:12:23,242 --> 00:12:24,535
is things like, hey,
472
00:12:24,535 --> 00:12:26,662
they design their storage solution
473
00:12:26,662 --> 00:12:28,330
such that it has very tightly
474
00:12:28,330 --> 00:12:29,498
to GP workloads.
475
00:12:29,498 --> 00:12:31,375
We're getting that nice performance,
476
00:12:31,375 --> 00:12:32,668
things like how we spin up
477
00:12:32,668 --> 00:12:33,419
our Kubernetes
478
00:12:33,419 --> 00:12:35,087
cluster to be able to
479
00:12:35,087 --> 00:12:36,464
handle the scale that we want,
480
00:12:36,464 --> 00:12:37,715
because remember,
481
00:12:37,715 --> 00:12:38,215
Miris
482
00:12:38,215 --> 00:12:40,176
like we're looking at assets
483
00:12:40,176 --> 00:12:41,552
coming through a pipeline
484
00:12:41,552 --> 00:12:42,928
where we can be dealing with
485
00:12:42,928 --> 00:12:44,513
thousands, tens of thousands,
486
00:12:44,513 --> 00:12:46,182
millions of assets to process
487
00:12:46,182 --> 00:12:48,350
essentially in a single day.
488
00:12:48,350 --> 00:12:49,477
Like we need a platform
489
00:12:49,477 --> 00:12:52,062
that's not only to scale up cheap views,
490
00:12:52,062 --> 00:12:54,523
but like 0.3 storage
491
00:12:54,523 --> 00:12:57,318
to scale the infrastructure as a whole.
492
00:12:57,318 --> 00:12:57,818
So for me,
493
00:12:57,818 --> 00:12:59,361
it's been really exciting to work with,
494
00:12:59,361 --> 00:13:01,739
mainly because they're an AI platform,
495
00:13:01,739 --> 00:13:03,574
they're optimizing around workloads
496
00:13:03,574 --> 00:13:05,451
that we're optimizing around.
497
00:13:05,451 --> 00:13:06,619
And so like that partnership
498
00:13:06,619 --> 00:13:07,703
together has worked
499
00:13:07,703 --> 00:13:09,413
really, really well for us.
500
00:13:09,413 --> 00:13:10,372
And what's the
501
00:13:10,372 --> 00:13:11,540
what are the problems
502
00:13:11,540 --> 00:13:13,167
that that architecture
503
00:13:13,167 --> 00:13:14,585
is helping you to eliminate
504
00:13:14,585 --> 00:13:15,836
for your customers?
505
00:13:15,836 --> 00:13:17,213
It's scale mainly.
506
00:13:17,213 --> 00:13:17,338
Right.
507
00:13:17,338 --> 00:13:19,298
Like scale is like over the years
508
00:13:19,298 --> 00:13:20,466
it's huge driver of that.
509
00:13:20,466 --> 00:13:22,343
So you can think of Miris
510
00:13:22,343 --> 00:13:24,303
and you think about something like
511
00:13:24,303 --> 00:13:25,888
pixel streaming historically.
512
00:13:25,888 --> 00:13:27,640
What happens is here
513
00:13:27,640 --> 00:13:29,266
you have users on the other side and say,
514
00:13:29,266 --> 00:13:30,351
hey, I want to view this
515
00:13:30,351 --> 00:13:32,269
3D asset on the back end.
516
00:13:32,269 --> 00:13:33,395
A service might say, I'm
517
00:13:33,395 --> 00:13:34,522
going to spin up
518
00:13:34,522 --> 00:13:36,398
all this cloud infrastructure
519
00:13:36,398 --> 00:13:37,817
and then deliver that to you.
520
00:13:37,817 --> 00:13:39,360
And like, hey, subscriptions, right?
521
00:13:39,360 --> 00:13:40,528
Like a buffer.
522
00:13:40,528 --> 00:13:41,070
The problem is
523
00:13:41,070 --> 00:13:43,405
it's like you're having to spin up a GQ
524
00:13:43,405 --> 00:13:44,990
for a user, right? Okay.
525
00:13:44,990 --> 00:13:46,617
So what matters is what we do with for we
526
00:13:46,617 --> 00:13:48,077
because we flip that equation,
527
00:13:48,077 --> 00:13:49,286
we say, hey,
528
00:13:49,286 --> 00:13:50,746
we're gonna take your asset
529
00:13:50,746 --> 00:13:51,580
and we're going to spin up
530
00:13:51,580 --> 00:13:54,291
a GPU upstream, upstream.
531
00:13:54,291 --> 00:13:56,961
And so we're running all these GPUs
532
00:13:56,961 --> 00:13:57,253
and you know,
533
00:13:57,253 --> 00:13:58,462
we're using the latest
534
00:13:58,462 --> 00:14:00,381
hardware from Nvidia
535
00:14:00,381 --> 00:14:02,299
for we to be able to do that.
536
00:14:02,299 --> 00:14:03,467
But we do that once it's
537
00:14:03,467 --> 00:14:05,427
actively for that.
538
00:14:05,427 --> 00:14:06,095
And then when it comes
539
00:14:06,095 --> 00:14:07,346
time to actually deliver that
540
00:14:07,346 --> 00:14:09,181
to customers, for clients,
541
00:14:09,181 --> 00:14:10,933
it's like GPUs are effectively
542
00:14:10,933 --> 00:14:12,643
out of the equation at that point. Okay.
543
00:14:12,643 --> 00:14:13,978
So like that, that ends up
544
00:14:13,978 --> 00:14:14,562
allowing us
545
00:14:14,562 --> 00:14:16,981
to deliver at billion user scale.
546
00:14:16,981 --> 00:14:17,773
And it's not because
547
00:14:17,773 --> 00:14:19,191
we're not using GPUs.
548
00:14:19,191 --> 00:14:20,192
It's mainly that,
549
00:14:20,192 --> 00:14:20,609
again,
550
00:14:20,609 --> 00:14:21,819
with the support in the sense
551
00:14:21,819 --> 00:14:23,821
that we're using it upstream.
552
00:14:23,821 --> 00:14:25,030
And that's the big
553
00:14:25,030 --> 00:14:25,573
I imagine
554
00:14:25,573 --> 00:14:27,116
that's a pretty big differentiator
555
00:14:27,116 --> 00:14:27,867
for mirrors
556
00:14:27,867 --> 00:14:29,785
that flipping the script
557
00:14:29,785 --> 00:14:31,078
and going upstream.
558
00:14:31,078 --> 00:14:32,746
Yes. Yeah, it's a big deal.
559
00:14:32,746 --> 00:14:35,332
And like the other part of this is like
560
00:14:35,332 --> 00:14:37,459
the reason why it's an AI and ML sort of
561
00:14:37,459 --> 00:14:38,669
workload is
562
00:14:38,669 --> 00:14:40,254
what comes out the other
563
00:14:40,254 --> 00:14:41,881
side of Miris is not meshes.
564
00:14:41,881 --> 00:14:42,756
It's not the things
565
00:14:42,756 --> 00:14:43,799
that we've been using over
566
00:14:43,799 --> 00:14:45,718
the last many decades. Right.
567
00:14:45,718 --> 00:14:47,469
What comes out the other side of Miris
568
00:14:47,469 --> 00:14:49,555
is actually volumetric content. Okay.
569
00:14:49,555 --> 00:14:51,557
We're using things like radiance fields
570
00:14:51,557 --> 00:14:52,099
and so on.
571
00:14:52,099 --> 00:14:53,893
To be able to effectively construct
572
00:14:53,893 --> 00:14:55,853
a representation of your asset
573
00:14:55,853 --> 00:14:57,897
now allows us a lot of flexibility
574
00:14:57,897 --> 00:14:58,606
in the ability
575
00:14:58,606 --> 00:15:00,649
to deliver the content at scale
576
00:15:00,649 --> 00:15:02,693
and in a very adaptive way.
577
00:15:02,693 --> 00:15:04,194
And that's actually paid off
578
00:15:04,194 --> 00:15:05,029
huge for us,
579
00:15:05,029 --> 00:15:05,946
because it allows us to do
580
00:15:05,946 --> 00:15:07,072
a lot of creative things
581
00:15:07,072 --> 00:15:09,366
in terms of optimization,
582
00:15:09,366 --> 00:15:10,284
if you think about things
583
00:15:10,284 --> 00:15:12,995
like display, AI or robotics. Yeah.
584
00:15:12,995 --> 00:15:14,288
One of the things we hear often
585
00:15:14,288 --> 00:15:16,206
from those customers are, hey,
586
00:15:16,206 --> 00:15:17,666
I want to run all these simulations,
587
00:15:17,666 --> 00:15:18,584
but I kind of moved
588
00:15:18,584 --> 00:15:20,044
all this 3D
589
00:15:20,044 --> 00:15:22,379
gigabytes, terabytes worth of data.
590
00:15:22,379 --> 00:15:24,340
I only have so much Vram on these
591
00:15:24,340 --> 00:15:25,341
GPUs now.
592
00:15:25,341 --> 00:15:25,966
I can only run
593
00:15:25,966 --> 00:15:27,593
maybe one simulation at a time.
594
00:15:27,593 --> 00:15:30,262
Oh, because Miris is able to stream
595
00:15:30,262 --> 00:15:31,430
now all of a sudden
596
00:15:31,430 --> 00:15:34,058
we can very creatively kind of impact
597
00:15:34,058 --> 00:15:35,184
the Ram of
598
00:15:35,184 --> 00:15:36,143
what's not being used,
599
00:15:36,143 --> 00:15:37,603
what the robot isn't seeing in
600
00:15:37,603 --> 00:15:38,812
any given time.
601
00:15:38,812 --> 00:15:39,438
Now all of a sudden,
602
00:15:39,438 --> 00:15:40,898
these companies can run
603
00:15:40,898 --> 00:15:43,651
2030 simulations on the same.
604
00:15:43,651 --> 00:15:45,444
So for them, it's a huge cost savings
605
00:15:45,444 --> 00:15:45,986
that allows them
606
00:15:45,986 --> 00:15:47,196
to actually scale up even more.
607
00:15:47,196 --> 00:15:49,406
That's the scale story. That's right.
608
00:15:49,406 --> 00:15:50,783
And so what are you guys demoing
609
00:15:50,783 --> 00:15:52,076
in the CoreWeave booth downstairs?
610
00:15:52,076 --> 00:15:53,243
Yeah, we've got a couple interesting
611
00:15:53,243 --> 00:15:53,953
things we're showing.
612
00:15:53,953 --> 00:15:54,536
So namely
613
00:15:54,536 --> 00:15:54,954
we're showing
614
00:15:54,954 --> 00:15:56,997
a digital twin presentation.
615
00:15:56,997 --> 00:15:58,457
So really high fidelity
616
00:15:58,457 --> 00:16:00,292
digital content that's being streamed.
617
00:16:00,292 --> 00:16:01,919
So it has the same visual fidelity
618
00:16:01,919 --> 00:16:02,586
that you might expect
619
00:16:02,586 --> 00:16:04,296
from like a pixel stream.
620
00:16:04,296 --> 00:16:05,339
But as we've discussed, it's
621
00:16:05,339 --> 00:16:06,590
not a pixel stream.
622
00:16:06,590 --> 00:16:07,675
It's being rasterized
623
00:16:07,675 --> 00:16:09,843
right there on the computer.
624
00:16:09,843 --> 00:16:10,803
But we're even a stream
625
00:16:10,803 --> 00:16:12,346
that in a very adaptive way.
626
00:16:12,346 --> 00:16:13,347
So, you know,
627
00:16:13,347 --> 00:16:15,265
say we have bad Wi-Fi in here.
628
00:16:15,265 --> 00:16:15,891
It's fine.
629
00:16:15,891 --> 00:16:16,141
Right?
630
00:16:16,141 --> 00:16:16,976
Like little adapt
631
00:16:16,976 --> 00:16:18,185
based on those conditions.
632
00:16:18,185 --> 00:16:18,602
Okay.
633
00:16:18,602 --> 00:16:18,978
Let's say
634
00:16:18,978 --> 00:16:21,271
you want to look at it up real close
635
00:16:21,271 --> 00:16:22,982
or stream that content.
636
00:16:22,982 --> 00:16:25,234
So we're showing a really high detail
637
00:16:25,234 --> 00:16:27,778
turbine, right?
638
00:16:27,778 --> 00:16:28,529
Oh yes yes yes
639
00:16:28,529 --> 00:16:29,530
I saw that in your presentation.
640
00:16:29,530 --> 00:16:30,698
Yeah. That was awesome. Right?
641
00:16:30,698 --> 00:16:32,783
I haven't even better one in the demo.
642
00:16:32,783 --> 00:16:34,493
So you have to see it. Okay.
643
00:16:34,493 --> 00:16:34,743
You know,
644
00:16:34,743 --> 00:16:36,078
you can zoom in and it, like,
645
00:16:36,078 --> 00:16:37,746
automatically resolves, right?
646
00:16:37,746 --> 00:16:38,956
It's really, really cool.
647
00:16:38,956 --> 00:16:40,207
You showed I forget
648
00:16:40,207 --> 00:16:41,041
what the who the comparison
649
00:16:41,041 --> 00:16:42,251
was on the left side.
650
00:16:42,251 --> 00:16:44,837
The speed difference was dramatic.
651
00:16:44,837 --> 00:16:45,087
Yeah.
652
00:16:45,087 --> 00:16:48,799
With what general Acme versus Miris.
653
00:16:48,799 --> 00:16:50,592
It was like oh exactly.
654
00:16:50,592 --> 00:16:50,843
Wow.
655
00:16:50,843 --> 00:16:52,761
Factor in like that's so important
656
00:16:52,761 --> 00:16:55,889
because when we talk to like, retailers,
657
00:16:55,889 --> 00:16:56,974
like people building
658
00:16:56,974 --> 00:16:57,558
like product
659
00:16:57,558 --> 00:17:00,561
integrators, or advertisers, right.
660
00:17:00,894 --> 00:17:01,937
Their big thing is like, hey,
661
00:17:01,937 --> 00:17:03,439
I want to get my customers
662
00:17:03,439 --> 00:17:05,065
into this experience.
663
00:17:05,065 --> 00:17:06,608
But in the current like web
664
00:17:06,608 --> 00:17:08,736
download model, they're waiting
665
00:17:08,736 --> 00:17:10,779
three seconds, five seconds, 10s,
666
00:17:10,779 --> 00:17:12,239
maybe even up to 30s.
667
00:17:12,239 --> 00:17:13,699
And what they want is, is like
668
00:17:13,699 --> 00:17:14,366
we see people
669
00:17:14,366 --> 00:17:16,201
just churning out of those experiences
670
00:17:16,201 --> 00:17:17,619
because they're so used to the experience
671
00:17:17,619 --> 00:17:19,580
being instant or non-voting.
672
00:17:19,580 --> 00:17:20,664
Yeah. Yes.
673
00:17:20,664 --> 00:17:22,791
And they churn. Yeah. Yes.
674
00:17:22,791 --> 00:17:24,084
The fact that we can show some interest.
675
00:17:24,084 --> 00:17:25,377
Oh yes, it
676
00:17:25,377 --> 00:17:26,628
is a game changer for them
677
00:17:26,628 --> 00:17:27,379
because all of a sudden
678
00:17:27,379 --> 00:17:28,672
you've got that customer
679
00:17:28,672 --> 00:17:29,548
in the experience.
680
00:17:29,548 --> 00:17:32,134
They can start using it right away.
681
00:17:32,134 --> 00:17:33,594
And like you can kind of extrapolate
682
00:17:33,594 --> 00:17:35,471
that out from like retail customers
683
00:17:35,471 --> 00:17:36,680
to physical eye
684
00:17:36,680 --> 00:17:39,016
digital twin media entertainment.
685
00:17:39,016 --> 00:17:39,433
So I'm
686
00:17:39,433 --> 00:17:40,642
like who's going to turn down the speed.
687
00:17:40,642 --> 00:17:42,019
Right. Like right.
688
00:17:42,019 --> 00:17:42,436
Yes.
689
00:17:42,436 --> 00:17:43,103
No one is saying,
690
00:17:43,103 --> 00:17:44,605
hey, it'd be cool if it's slower,
691
00:17:44,605 --> 00:17:46,565
less data slower. Yes. Right.
692
00:17:46,565 --> 00:17:49,109
There's no there's no, sticker for that.
693
00:17:49,109 --> 00:17:51,403
No. No one's worry that slow is good.
694
00:17:51,403 --> 00:17:52,654
You know, a great sticker.
695
00:17:52,654 --> 00:17:54,823
So if a fortune 500 leader
696
00:17:54,823 --> 00:17:57,242
is watching this and what? What's neat?
697
00:17:57,242 --> 00:17:58,619
And if they're wondering,
698
00:17:58,619 --> 00:17:59,995
is my
699
00:17:59,995 --> 00:18:02,456
use case ready for AI infrastructure?
700
00:18:02,456 --> 00:18:04,708
What would you tell them now
701
00:18:04,708 --> 00:18:06,168
to flip that script?
702
00:18:06,168 --> 00:18:06,502
Yeah.
703
00:18:06,502 --> 00:18:07,586
Well, I'd say, number one
704
00:18:07,586 --> 00:18:09,421
that the status quo is terrorist.
705
00:18:09,421 --> 00:18:09,713
Right.
706
00:18:09,713 --> 00:18:11,006
Like there is
707
00:18:11,006 --> 00:18:11,965
things are changing
708
00:18:11,965 --> 00:18:13,133
at such a rapid rate
709
00:18:13,133 --> 00:18:13,884
and things,
710
00:18:13,884 --> 00:18:14,218
you know,
711
00:18:14,218 --> 00:18:15,928
just talking about computer graphics
712
00:18:15,928 --> 00:18:17,096
in particular,
713
00:18:17,096 --> 00:18:20,057
we've been so, so used to living in a
714
00:18:20,057 --> 00:18:21,308
like polygon.
715
00:18:21,308 --> 00:18:22,518
Yeah. Forever.
716
00:18:22,518 --> 00:18:24,144
And polygons will persist, right?
717
00:18:24,144 --> 00:18:25,687
Like they're not going anywhere.
718
00:18:25,687 --> 00:18:26,980
But things that way, they're
719
00:18:26,980 --> 00:18:29,274
we're seeing like the radiance field,
720
00:18:29,274 --> 00:18:30,859
Gaussian splat, etc.
721
00:18:30,859 --> 00:18:32,152
space or accelerating
722
00:18:32,152 --> 00:18:33,278
essentially created that.
723
00:18:33,278 --> 00:18:34,738
And what I would tell people
724
00:18:34,738 --> 00:18:35,697
leaders in the fortune
725
00:18:35,697 --> 00:18:36,782
500 companies are
726
00:18:36,782 --> 00:18:37,991
using that as an example.
727
00:18:37,991 --> 00:18:40,994
And it's like be mindful of like how fast
728
00:18:41,203 --> 00:18:42,496
this is changing
729
00:18:42,496 --> 00:18:44,581
and stay ahead of the adoption curve.
730
00:18:44,581 --> 00:18:45,082
Okay.
731
00:18:45,082 --> 00:18:47,918
So our goal is in effect, an exponential.
732
00:18:47,918 --> 00:18:48,210
Yes.
733
00:18:48,210 --> 00:18:49,169
Like maybe even beyond
734
00:18:49,169 --> 00:18:50,462
an exponential curve.
735
00:18:50,462 --> 00:18:52,548
And it's really like a good time
736
00:18:52,548 --> 00:18:52,923
every day.
737
00:18:52,923 --> 00:18:54,216
Like when I wake up in the morning
738
00:18:54,216 --> 00:18:55,884
I'm seeing the world
739
00:18:55,884 --> 00:18:57,386
subtly change, right?
740
00:18:57,386 --> 00:18:58,929
Sometimes right, in subtle ways.
741
00:18:58,929 --> 00:18:59,847
And so for me,
742
00:18:59,847 --> 00:19:01,515
like really staying very close
743
00:19:01,515 --> 00:19:02,808
to all the innovation
744
00:19:02,808 --> 00:19:03,976
that's happening
745
00:19:03,976 --> 00:19:06,979
in computer graphics and AI in general,
746
00:19:07,062 --> 00:19:07,896
and how you can, like,
747
00:19:07,896 --> 00:19:08,981
train your workforce
748
00:19:08,981 --> 00:19:10,482
to take advantage of that.
749
00:19:10,482 --> 00:19:12,568
Really take a second, third, fourth
750
00:19:12,568 --> 00:19:14,278
look at how you can move
751
00:19:14,278 --> 00:19:16,029
faster or scale
752
00:19:16,029 --> 00:19:17,573
to like millions of users,
753
00:19:17,573 --> 00:19:17,865
like what
754
00:19:17,865 --> 00:19:19,408
would that potentially look like?
755
00:19:19,408 --> 00:19:20,659
It's just all changing.
756
00:19:21,869 --> 00:19:22,744
Quickly.
757
00:19:22,744 --> 00:19:23,537
And it's yeah, it's
758
00:19:23,537 --> 00:19:24,746
an exciting time to be a tech.
759
00:19:24,746 --> 00:19:26,790
It is such an exciting time because,
760
00:19:26,790 --> 00:19:27,291
I mean,
761
00:19:27,291 --> 00:19:28,250
I can't even imagine
762
00:19:28,250 --> 00:19:28,834
what we're going to be
763
00:19:28,834 --> 00:19:29,835
talking about next.
764
00:19:29,835 --> 00:19:32,337
GTC oh, is it fair to say, though, that
765
00:19:32,337 --> 00:19:33,213
that mirrors
766
00:19:33,213 --> 00:19:36,216
where we are, you enabling your customers
767
00:19:36,383 --> 00:19:38,969
to get ahead of that of that
768
00:19:38,969 --> 00:19:40,637
curve because
769
00:19:40,637 --> 00:19:41,722
so many folks are behind
770
00:19:41,722 --> 00:19:42,848
how what you're saying
771
00:19:42,848 --> 00:19:44,099
it's it's realistic
772
00:19:44,099 --> 00:19:45,058
with these two companies.
773
00:19:45,058 --> 00:19:46,476
You can get ahead of this.
774
00:19:46,476 --> 00:19:47,519
Yeah, absolutely.
775
00:19:47,519 --> 00:19:47,936
I get like
776
00:19:47,936 --> 00:19:49,021
this is where the CoreWeave
777
00:19:49,021 --> 00:19:51,064
partnership has been so vital
778
00:19:51,064 --> 00:19:52,566
because they have this same vision
779
00:19:52,566 --> 00:19:53,400
of like
780
00:19:53,400 --> 00:19:55,861
computer graphics is having this shift,
781
00:19:55,861 --> 00:19:57,029
that moment.
782
00:19:57,029 --> 00:19:57,613
And so,
783
00:19:57,613 --> 00:19:58,655
you know, going back
784
00:19:58,655 --> 00:20:01,450
to like my ten year old son like, yeah,
785
00:20:01,450 --> 00:20:02,784
we're seeing just like this
786
00:20:02,784 --> 00:20:05,204
the views of 3D content.
787
00:20:05,204 --> 00:20:07,039
How do we provide a platform together
788
00:20:07,039 --> 00:20:08,665
that can truly scale to that?
789
00:20:08,665 --> 00:20:10,292
How can we get content
790
00:20:10,292 --> 00:20:11,168
where it needs to be?
791
00:20:11,168 --> 00:20:12,002
How can we take
792
00:20:12,002 --> 00:20:14,171
even like really rich physical
793
00:20:14,171 --> 00:20:15,255
AI, multi
794
00:20:15,255 --> 00:20:17,090
gigabyte ranging into terabytes
795
00:20:17,090 --> 00:20:18,050
of content?
796
00:20:18,050 --> 00:20:18,759
How can we get that
797
00:20:18,759 --> 00:20:19,676
to where it needs to be,
798
00:20:19,676 --> 00:20:21,178
and how can we get it to a place
799
00:20:21,178 --> 00:20:23,305
where upwards of billions of people
800
00:20:23,305 --> 00:20:25,349
can all see that at the same time?
801
00:20:25,349 --> 00:20:26,475
Like that?
802
00:20:26,475 --> 00:20:27,601
All those things
803
00:20:27,601 --> 00:20:28,977
like we talk about
804
00:20:28,977 --> 00:20:32,105
scale, fidelity, cost and speed
805
00:20:32,481 --> 00:20:33,523
when you're able to like, hit
806
00:20:33,523 --> 00:20:35,275
all those four things in parallel.
807
00:20:35,275 --> 00:20:37,402
Again, that's where the magic is.
808
00:20:37,402 --> 00:20:38,612
That's Nirvana.
809
00:20:38,612 --> 00:20:39,363
It is. Right.
810
00:20:39,363 --> 00:20:40,280
Like that
811
00:20:40,280 --> 00:20:41,240
kind of going all the way back
812
00:20:41,240 --> 00:20:43,158
to where we started, like in my career.
813
00:20:43,158 --> 00:20:43,492
Yeah,
814
00:20:43,492 --> 00:20:44,743
like being able to build
815
00:20:44,743 --> 00:20:45,410
a platform
816
00:20:45,410 --> 00:20:46,370
that allows you
817
00:20:46,370 --> 00:20:49,373
to kind of unleash 3D content at scale
818
00:20:49,414 --> 00:20:50,540
to get it to everyone.
819
00:20:50,540 --> 00:20:52,042
Like, that's kind of a holy grail for me,
820
00:20:52,042 --> 00:20:54,211
is able to help creators and developers.
821
00:20:54,211 --> 00:20:55,420
I'm sure that you from 10
822
00:20:55,420 --> 00:20:56,463
or 15 years ago couldn't
823
00:20:56,463 --> 00:20:59,466
even imagine where we are in 2026.
824
00:20:59,466 --> 00:20:59,967
Oh no.
825
00:20:59,967 --> 00:21:01,510
I mean, I was
826
00:21:01,510 --> 00:21:02,844
in my early 3D,
827
00:21:02,844 --> 00:21:04,554
you know, my early 3D years.
828
00:21:04,554 --> 00:21:04,763
You know,
829
00:21:04,763 --> 00:21:06,014
I was used to like
830
00:21:06,014 --> 00:21:07,516
downloading off the network
831
00:21:07,516 --> 00:21:09,393
like a bytes of data
832
00:21:09,393 --> 00:21:10,769
coming back the next day.
833
00:21:10,769 --> 00:21:13,272
Right, like rendering massive frames
834
00:21:13,272 --> 00:21:14,690
that could take weeks, right?
835
00:21:14,690 --> 00:21:15,816
Like, you know,
836
00:21:15,816 --> 00:21:17,859
some of these things will persist by
837
00:21:17,859 --> 00:21:18,235
the way,
838
00:21:18,235 --> 00:21:19,278
I just
839
00:21:19,278 --> 00:21:19,778
again, like,
840
00:21:19,778 --> 00:21:21,321
things are changing at such a rate,
841
00:21:21,321 --> 00:21:23,282
like the idea that I can provide,
842
00:21:23,282 --> 00:21:25,701
I can take a ten gigabyte asset
843
00:21:25,701 --> 00:21:26,493
and get that to
844
00:21:26,493 --> 00:21:28,745
someone in almost an instant.
845
00:21:28,745 --> 00:21:29,037
You know,
846
00:21:29,037 --> 00:21:30,998
if you told me that 20 years ago,
847
00:21:30,998 --> 00:21:31,373
like, oh,
848
00:21:31,373 --> 00:21:33,208
you saw the speed of light right now.
849
00:21:33,208 --> 00:21:34,584
Yeah. Not by the way,
850
00:21:35,961 --> 00:21:36,545
is it?
851
00:21:36,545 --> 00:21:36,795
Yeah.
852
00:21:36,795 --> 00:21:38,380
That's a concept
853
00:21:38,380 --> 00:21:40,048
that has radically changed.
854
00:21:40,048 --> 00:21:41,091
And again,
855
00:21:41,091 --> 00:21:43,385
that's the last question for you.
856
00:21:43,385 --> 00:21:46,388
You've been to 4 or 5 gigs before.
857
00:21:46,430 --> 00:21:48,890
What is different this year
858
00:21:48,890 --> 00:21:50,225
even compared to last year.
859
00:21:50,225 --> 00:21:51,768
Oh I mean look at it down here.
860
00:21:51,768 --> 00:21:53,270
It's just like wow.
861
00:21:53,270 --> 00:21:54,813
Right. Like it is wild.
862
00:21:54,813 --> 00:21:55,063
You know,
863
00:21:55,063 --> 00:21:57,816
I've been to so many conferences, right?
864
00:21:57,816 --> 00:21:59,067
GDC and
865
00:21:59,067 --> 00:22:01,403
what I'm like noticing about GDC,
866
00:22:01,403 --> 00:22:03,030
when you talk about like an exponential,
867
00:22:03,030 --> 00:22:04,114
like the energy
868
00:22:04,114 --> 00:22:05,365
and cheating in GTC
869
00:22:05,365 --> 00:22:07,117
is like on this exponential curve,
870
00:22:07,117 --> 00:22:10,203
like it's really, really high this year.
871
00:22:10,203 --> 00:22:13,290
I was noticing even yesterday, like just
872
00:22:13,290 --> 00:22:13,707
the sheer
873
00:22:13,707 --> 00:22:14,875
number of people here
874
00:22:14,875 --> 00:22:17,085
are just, like, incredible.
875
00:22:17,085 --> 00:22:17,878
It's not even,
876
00:22:17,878 --> 00:22:18,337
you know, like, you
877
00:22:18,337 --> 00:22:19,504
go to a lot of these problems.
878
00:22:19,504 --> 00:22:20,756
It's it's like, you know,
879
00:22:20,756 --> 00:22:21,631
the experience is like
880
00:22:21,631 --> 00:22:22,632
within the exhibit,
881
00:22:22,632 --> 00:22:24,634
all GDC has gotten to the scale
882
00:22:24,634 --> 00:22:26,261
where it's like spilled out. Oh, yeah.
883
00:22:26,261 --> 00:22:26,678
And there's like
884
00:22:26,678 --> 00:22:28,055
a whole festival outside.
885
00:22:28,055 --> 00:22:30,682
Yeah, it is like a festival. Yeah. Yes.
886
00:22:30,682 --> 00:22:31,808
You know, I was like,
887
00:22:31,808 --> 00:22:33,143
I was walking in the other day,
888
00:22:33,143 --> 00:22:34,102
I heard like
889
00:22:34,102 --> 00:22:36,521
a live band with a singing country
890
00:22:36,521 --> 00:22:37,647
song about fiscal.
891
00:22:37,647 --> 00:22:39,316
I know, I'm like, wow.
892
00:22:39,316 --> 00:22:39,775
Like,
893
00:22:39,775 --> 00:22:40,650
I don't know if this is, like,
894
00:22:40,650 --> 00:22:42,110
the sound of a cold or what,
895
00:22:42,110 --> 00:22:43,403
but whatever it is like,
896
00:22:43,403 --> 00:22:44,237
it's pretty incredible.
897
00:22:44,237 --> 00:22:45,739
I love I yeah, I love it
898
00:22:45,739 --> 00:22:47,366
and and my wrist has a beta program.
899
00:22:47,366 --> 00:22:47,949
Tell the audience
900
00:22:47,949 --> 00:22:49,284
a little bit more about the beta program
901
00:22:49,284 --> 00:22:50,077
and where they can access
902
00:22:50,077 --> 00:22:50,952
the beta program.
903
00:22:50,952 --> 00:22:53,580
Starting on, March 24th and next week.
904
00:22:53,580 --> 00:22:54,414
We are hard at work
905
00:22:54,414 --> 00:22:56,416
and making it a great point.
906
00:22:56,416 --> 00:22:58,126
Yeah, we're signing people up now.
907
00:22:58,126 --> 00:22:59,503
We're going to start
908
00:22:59,503 --> 00:23:01,004
with when on the 24th.
909
00:23:01,004 --> 00:23:03,924
And yeah, we're really excited about it.
910
00:23:03,924 --> 00:23:05,258
Very interested
911
00:23:05,258 --> 00:23:06,510
in seeing what people create
912
00:23:06,510 --> 00:23:07,719
and distribute on this platform.
913
00:23:07,719 --> 00:23:08,720
What interest theta.
914
00:23:08,720 --> 00:23:09,596
What will they have
915
00:23:09,596 --> 00:23:11,681
unique access to from Miris?
916
00:23:11,681 --> 00:23:12,182
Oh, sure.
917
00:23:12,182 --> 00:23:13,767
They'll have access to the full faith.
918
00:23:13,767 --> 00:23:14,101
Right.
919
00:23:14,101 --> 00:23:17,229
So you'll be able to upload, 3D content.
920
00:23:17,229 --> 00:23:19,606
So we support open USD,
921
00:23:19,606 --> 00:23:21,775
similar to our friends over at Nvidia.
922
00:23:21,775 --> 00:23:23,318
So that's why we call it a video player.
923
00:23:23,318 --> 00:23:24,569
And also,
924
00:23:24,569 --> 00:23:27,072
you'll be able to open, or upload open
925
00:23:27,072 --> 00:23:29,574
USD content. We take it from there.
926
00:23:29,574 --> 00:23:32,661
We put that into our streaming content
927
00:23:32,661 --> 00:23:33,578
and out the other end
928
00:23:33,578 --> 00:23:35,664
you'll be able to see it in our software.
929
00:23:35,664 --> 00:23:36,706
You'll be able to take that
930
00:23:36,706 --> 00:23:38,417
with a few lines of code
931
00:23:38,417 --> 00:23:39,000
and integrate
932
00:23:39,000 --> 00:23:41,044
that into a web application.
933
00:23:41,044 --> 00:23:43,338
So three.js as an example,
934
00:23:43,338 --> 00:23:44,798
you don't have to do everything.
935
00:23:44,798 --> 00:23:47,384
It just seamlessly works, with bridges.
936
00:23:47,384 --> 00:23:48,301
And it's accessible
937
00:23:48,301 --> 00:23:49,302
from the virus website.
938
00:23:49,302 --> 00:23:50,429
That's right. Yeah.
939
00:23:50,429 --> 00:23:51,513
That's all you need to do this thing.
940
00:23:51,513 --> 00:23:54,015
Yes. I did have a little bit of code.
941
00:23:54,015 --> 00:23:54,683
We got plenty of,
942
00:23:54,683 --> 00:23:57,269
tutorials and documentation galore,
943
00:23:57,269 --> 00:23:58,687
and, yeah,
944
00:23:58,687 --> 00:24:00,105
you get up and running super fast.
945
00:24:00,105 --> 00:24:00,439
Okay.
946
00:24:00,439 --> 00:24:01,273
I bet you cannot wait
947
00:24:01,273 --> 00:24:02,190
to see the use cases
948
00:24:02,190 --> 00:24:03,066
that explode from this.
949
00:24:03,066 --> 00:24:05,152
Yeah, I'm very a kid in a candy store.
950
00:24:05,152 --> 00:24:06,903
I imagine a few early customers
951
00:24:06,903 --> 00:24:08,321
and just seeing
952
00:24:08,321 --> 00:24:10,073
not only like the visual quality,
953
00:24:10,073 --> 00:24:11,450
but also just like the scale
954
00:24:11,450 --> 00:24:12,534
that they're talking about.
955
00:24:12,534 --> 00:24:12,909
Yeah.
956
00:24:12,909 --> 00:24:14,453
You know, again, like talking
957
00:24:14,453 --> 00:24:15,412
to like the 20 years,
958
00:24:15,412 --> 00:24:17,164
like 20 years in the past first to me.
959
00:24:17,164 --> 00:24:18,582
Yeah. Right.
960
00:24:18,582 --> 00:24:19,916
Oh no.
961
00:24:19,916 --> 00:24:20,709
So I can't even
962
00:24:20,709 --> 00:24:22,586
I can't even like think out to next year
963
00:24:22,586 --> 00:24:23,753
because,
964
00:24:23,753 --> 00:24:25,380
you know, generative AI is so fast
965
00:24:25,380 --> 00:24:26,840
a genetic and everything. But.
966
00:24:26,840 --> 00:24:29,009
Well, thank you for sharing your story.
967
00:24:29,009 --> 00:24:31,136
The common thread of what you bring in,
968
00:24:31,136 --> 00:24:33,430
but also the massive impact
969
00:24:33,430 --> 00:24:34,431
that Miris and CoreWeave
970
00:24:34,431 --> 00:24:36,266
are making on other industries
971
00:24:36,266 --> 00:24:39,144
besides VFX, retail, commerce, physical.
972
00:24:39,144 --> 00:24:41,188
I cannot wait to hear
973
00:24:41,188 --> 00:24:41,938
what's next
974
00:24:41,938 --> 00:24:42,522
because I'm sure it's
975
00:24:42,522 --> 00:24:43,398
going to be fantastic.
976
00:24:43,398 --> 00:24:44,399
But thank you for stopping by
977
00:24:44,399 --> 00:24:45,650
and sharing your story.
978
00:24:45,650 --> 00:24:47,110
Yeah, for well, McDonald.
979
00:24:47,110 --> 00:24:48,320
I'm Lisa Martin, coming to you
980
00:24:48,320 --> 00:24:51,323
live from CoreWeave booth at GTC day two.
981
00:24:51,364 --> 00:24:52,574
Thanks for watching guys, and we'll
982
00:24:52,574 --> 00:24:53,867
see you on the next episode.
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
