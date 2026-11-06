# MasterClass Builds Multi-Agent AI Learners Trust | CoreWeave

Source: https://www.coreweave.com/resources/videos/how-masterclass-builds-multi-agent-ai-that-learners-can-trust

Announcement

Webinar

Podcast

GTC 2026

CoreWeave Forge is here: connect your AI loop and compound every improvement. Read more

Contact us

Copied

Overview
Transcript

See how MasterClass uses AI agents to deliver personalized learning that students can genuinely rely on. In this session, the team shares how they monitor complex AI systems on CoreWeave, catch mistakes before they impact students, and help their models learn from real usage to automatically improve over time.
Speakers: Mandar Bapaye, CPO and CTO, MasterClass

00:00

1
00:00:00,000 --> 00:00:07,250
Welcome to the session. I'm Mandar.
2
00:00:07,250 --> 00:00:09,360
I'm Chief Product Officer at MasterClass.
3
00:00:09,920 --> 00:00:12,720
I'm Priya. I'm a Senior Staff
Engineer at MasterClass.
4
00:00:13,640 --> 00:00:17,330
We are super excited to talk to you
guys about what we have been building at
5
00:00:17,330 --> 00:00:19,800
MasterClass over the past couple of years.
6
00:00:20,740 --> 00:00:24,940
Before we get started, how many
of you are familiar with MasterClass?
7
00:00:24,940 --> 00:00:30,010
Product company. I see some hand raised.
Awesome. For those who are not
8
00:00:30,010 --> 00:00:33,660
familiar with what MasterClass is,
we are an online education company.
9
00:00:34,440 --> 00:00:38,380
We have classes from some of the best
of the best talent in the world across
10
00:00:38,380 --> 00:00:39,560
many fields.
11
00:00:39,700 --> 00:00:43,600
So you can think about like Mark Cuban,
Richard Branson of the world, Kim
12
00:00:43,600 --> 00:00:48,660
Kardashian of the world, Chef Ramsay,
Steph Curry, so on and so forth.
13
00:00:48,660 --> 00:00:52,220
We have hundreds of these classes,
right? They're predominantly on videos.
14
00:00:53,380 --> 00:00:55,650
In that case, you must
be wondering, why are
15
00:00:55,650 --> 00:00:58,420
you speaking at CoreWeave
conference, right?
16
00:00:58,680 --> 00:01:03,470
So what we have also been doing for
the past few years now is we have been
17
00:01:03,470 --> 00:01:10,060
rebuilding learning with AI, and that has
taken many different shapes along the way.
18
00:01:10,920 --> 00:01:14,730
We started off with something fairly
simplistic. This was, I would say, like
19
00:01:14,730 --> 00:01:17,140
two, two and a half years
ago when GPT-3 came out.
20
00:01:17,980 --> 00:01:21,380
This is what we call AI
augmented learning experiences.
21
00:01:22,120 --> 00:01:26,800
This is, you can think about, hey, you
have a video. Video is playing. All the
22
00:01:26,800 --> 00:01:30,260
content from that video,
everything is fed into a RAG.
23
00:01:30,600 --> 00:01:34,220
There is a chatbot on the side that
you can talk to about the video. That's
24
00:01:34,220 --> 00:01:36,280
what we call the class TA.
25
00:01:36,780 --> 00:01:40,400
That is, the first product offering we
launched about a couple of years ago,
26
00:01:40,400 --> 00:01:42,340
and then with Certificates, which is our
27
00:01:42,340 --> 00:01:44,820
different product,
we had something similar.
28
00:01:44,820 --> 00:01:47,000
But again, it's a very
augmentative experience.
29
00:01:48,400 --> 00:01:53,300
Then we matured into what we are now
calling AI native learning experiences.
30
00:01:54,000 --> 00:01:56,240
So there are two that I
have put on the screen here.
31
00:01:56,340 --> 00:01:58,900
The one on the left,
the product is called OnCall.
32
00:01:59,580 --> 00:02:04,500
The idea of OnCall is, with MasterClass
proper, you have access to the Mark Cubans
33
00:02:04,500 --> 00:02:06,120
of the world on video.
34
00:02:06,940 --> 00:02:09,800
How great would it be if
you can talk to Mark Cuban?
35
00:02:09,880 --> 00:02:11,460
Now, I cannot get Mark
Cuban to talk to all
36
00:02:11,460 --> 00:02:13,360
of us every single day,
every single minute.
37
00:02:13,460 --> 00:02:14,640
Unfortunately, I would love that.
38
00:02:15,520 --> 00:02:19,230
But what we do is we create AI personas
of these instructors, and you can
39
00:02:19,230 --> 00:02:21,380
literally call them
and talk to the AI personas.
40
00:02:21,380 --> 00:02:24,840
That's the product on the left,
and the product on the right, what we are
41
00:02:24,840 --> 00:02:26,460
calling MasterClass Coach.
42
00:02:27,100 --> 00:02:31,050
The idea of MasterClass Coach is,
we believe incredible executive coaching
43
00:02:31,050 --> 00:02:33,260
should be available to everyone.
44
00:02:33,880 --> 00:02:36,580
There is a problem with respect
to cost and supply and all of it.
45
00:02:37,160 --> 00:02:40,700
So idea with MasterClass Coach,
we created it with many exec coaches.
46
00:02:41,220 --> 00:02:42,160
We trained it.
47
00:02:42,160 --> 00:02:44,500
The idea is, it listens
in on your meeting.
48
00:02:44,500 --> 00:02:48,390
It sits with you in your meetings,
listens in, and then it will give you
49
00:02:48,390 --> 00:02:51,080
feedback based on, these are
the things you are doing well.
50
00:02:51,320 --> 00:02:52,580
These are the things you can improve at.
51
00:02:52,920 --> 00:02:56,340
Here are some videos, articles you can
read, and you can have a conversation.
52
00:02:56,460 --> 00:02:58,720
But the idea is, you have a really
good exec coach in your pocket.
53
00:03:00,800 --> 00:03:05,040
While we were building all of this, one
question that we have always dabbled in
54
00:03:05,040 --> 00:03:08,400
and has been on the back of our mind is,
55
00:03:08,780 --> 00:03:10,960
what if everyone had a personal teacher?
56
00:03:11,960 --> 00:03:12,960
I grew up in India.
57
00:03:13,720 --> 00:03:16,080
Growing up, I really,
really struggled with biology.
58
00:03:16,820 --> 00:03:18,170
I come from a family of doctors, so my mom
59
00:03:18,170 --> 00:03:21,020
and dad were disappointed
in me from day one.
60
00:03:21,260 --> 00:03:27,200
But one thing they did, which was really
cool, was they hired Professor Kumar,
61
00:03:27,200 --> 00:03:29,960
who was my personal teacher for biology.
62
00:03:30,560 --> 00:03:32,580
And it changed the game for me.
63
00:03:33,140 --> 00:03:34,380
Like, I started loving the subject.
64
00:03:34,920 --> 00:03:39,200
I started, like, again, enjoying
the conversations with my teacher.
65
00:03:40,140 --> 00:03:41,900
I didn't land up becoming a doctor.
66
00:03:42,100 --> 00:03:42,560
He was good.
67
00:03:42,560 --> 00:03:43,560
He was not that good.
68
00:03:44,120 --> 00:03:44,840
I'm kidding.
69
00:03:44,840 --> 00:03:45,840
He was great.
70
00:03:45,860 --> 00:03:50,930
But one of the main things that we have
seen benefits of is personal teaching
71
00:03:50,930 --> 00:03:54,520
has always had massive
impact on the students.
72
00:03:55,580 --> 00:03:56,980
And this shows up in data.
73
00:03:57,320 --> 00:03:58,900
And this data is not new, by the way.
74
00:03:58,960 --> 00:04:01,140
This data has existed for decades.
75
00:04:03,120 --> 00:04:07,440
98% of the people who got personal
tutoring, they out, sorry, people who got
76
00:04:07,440 --> 00:04:11,780
personal tutoring, even average,
outperformed 98% of the class.
77
00:04:13,880 --> 00:04:17,240
The performance went up
for people or students
78
00:04:17,240 --> 00:04:20,660
who got personal teaching by 16 points.
79
00:04:20,820 --> 00:04:24,420
So the impacts of personal
teaching have always been massive.
80
00:04:25,580 --> 00:04:30,450
What has been difficult throughout
this period is it's very hard to scale
81
00:04:30,450 --> 00:04:32,360
personalized teaching.
82
00:04:33,080 --> 00:04:35,000
From cost standpoint, it's expensive.
83
00:04:35,720 --> 00:04:40,470
From supply standpoint, it's hard because
finding one teacher for every student,
84
00:04:40,470 --> 00:04:42,280
it's just not feasible.
85
00:04:43,180 --> 00:04:45,800
And the quality consistency
is just not there.
86
00:04:45,940 --> 00:04:46,940
Like, some teachers are great.
87
00:04:47,120 --> 00:04:48,300
Some teachers are not that well.
88
00:04:50,480 --> 00:04:56,110
So as we were thinking about it, this
was in 2025, we were building really
89
00:04:56,110 --> 00:04:58,780
complex AI systems in our products.
90
00:04:59,580 --> 00:05:02,620
And we were looking at, like, if we were
to build a personal teacher ourselves,
91
00:05:02,620 --> 00:05:04,080
what could that look like?
92
00:05:04,940 --> 00:05:08,240
And we were doing a bunch of research,
a bunch of testing on it.
93
00:05:08,340 --> 00:05:10,920
At the same time, there were
two papers that came up.
94
00:05:11,400 --> 00:05:15,060
The one on the left that you see is a
paper from World Bank, and the one on the
95
00:05:15,060 --> 00:05:16,660
right is from Harvard.
96
00:05:17,660 --> 00:05:22,730
What both the papers showed, and it
100% aligned with what we were seeing in
97
00:05:22,730 --> 00:05:24,820
our research and our testing.
98
00:05:26,620 --> 00:05:31,220
World Bank did a study where this was
based out of South Africa, out of Africa.
99
00:05:31,740 --> 00:05:37,060
They augmented classroom teaching
for English with Copilot.
100
00:05:38,260 --> 00:05:44,250
What they saw was students who engaged
with AI conversations after classroom,
101
00:05:44,250 --> 00:05:48,480
they actually learned the amount of
content in a tremendously short period of
102
00:05:48,480 --> 00:05:52,520
time, as compared to the control,
which were people just sitting through the
103
00:05:52,520 --> 00:05:53,580
regular classes.
104
00:05:54,180 --> 00:05:57,100
On the Harvard side, they ran
the experiment for physics.
105
00:05:57,640 --> 00:05:59,020
They saw something very, very similar.
106
00:05:59,500 --> 00:06:02,920
Less number of hours required
to grab the same amount of content.
107
00:06:03,920 --> 00:06:08,080
And the students were way more
engaged, and the content was sticky.
108
00:06:09,800 --> 00:06:12,680
These were some of the key learnings
that came out of all those studies.
109
00:06:12,820 --> 00:06:13,820
We ran a similar study.
110
00:06:13,960 --> 00:06:15,280
We ran a similar research.
111
00:06:15,460 --> 00:06:18,200
We saw pretty much identical
findings in that regard.
112
00:06:20,280 --> 00:06:21,420
Engagement was high.
113
00:06:21,900 --> 00:06:23,280
Very highly cost-effective.
114
00:06:24,280 --> 00:06:28,920
The more someone used the product,
the better the learning became.
115
00:06:29,060 --> 00:06:30,060
All of that was good.
116
00:06:30,120 --> 00:06:33,580
But the main thing, which was common
to them, and what we saw was that point
117
00:06:33,580 --> 00:06:37,810
number one, is this is not just you
putting a chatbot in front of someone and
118
00:06:37,810 --> 00:06:39,320
let them engage with it.
119
00:06:40,240 --> 00:06:42,500
Your system, your teaching system, has to
120
00:06:42,500 --> 00:06:46,030
be extremely well-designed
and pedagogically
121
00:06:46,030 --> 00:06:49,140
sound on how it is teaching the students.
122
00:06:49,860 --> 00:06:52,520
There are aspects with
respect to cognition overload.
123
00:06:52,680 --> 00:06:54,920
There are aspects with
respect to periodic recall.
124
00:06:55,040 --> 00:06:58,620
There are aspects with respect to active
learning, not just giving up answers.
125
00:06:59,240 --> 00:07:03,400
All of that is not just a bot
put in front of a student.
126
00:07:03,400 --> 00:07:05,400
That requires engineering.
127
00:07:05,780 --> 00:07:09,080
That requires having a point of view as
a product, as a company, to say, hey,
128
00:07:09,080 --> 00:07:11,180
this is what good education looks like.
129
00:07:12,040 --> 00:07:14,150
So while we were doing this research, in
130
00:07:14,150 --> 00:07:16,840
parallel, we were working
on our new product.
131
00:07:17,640 --> 00:07:18,660
This was last year.
132
00:07:18,760 --> 00:07:20,380
The product is called
MasterClass Executive.
133
00:07:21,420 --> 00:07:25,230
The idea of MasterClass Executive as
a product is the way businesses are run,
134
00:07:25,230 --> 00:07:30,250
the way different functions are run
within businesses is drastically changing
135
00:07:30,250 --> 00:07:31,700
in the world of AI.
136
00:07:32,080 --> 00:07:36,350
And people are just not getting taught
great education on what does it mean to
137
00:07:36,350 --> 00:07:40,800
be a great business leader who is native
when it comes to various functions.
138
00:07:40,920 --> 00:07:42,660
So MasterClass Executive
is focused on that.
139
00:07:43,300 --> 00:07:46,940
We build the product in partnership
with Chicago Booth and OpenAI.
140
00:07:47,740 --> 00:07:51,660
It has 10 subjects, very
well-curated business curriculum.
141
00:07:52,900 --> 00:07:55,480
It has 12 AI labs, which is hands-on.
142
00:07:55,580 --> 00:07:56,700
You get involved with the instructor.
143
00:07:57,120 --> 00:07:58,120
You're building things.
144
00:07:58,480 --> 00:07:59,500
All of that is well and good.
145
00:07:59,600 --> 00:08:00,880
But as our research was coming to
146
00:08:00,880 --> 00:08:03,000
fruition, the stuff
that we talked earlier,
147
00:08:03,000 --> 00:08:06,250
one thing we thought is, what if the
148
00:08:06,250 --> 00:08:10,150
core experience itself had a personal
149
00:08:10,150 --> 00:08:12,520
teacher at its root?
150
00:08:13,080 --> 00:08:14,860
So the way you learn is
not just you read a bunch
151
00:08:14,860 --> 00:08:16,800
of articles and you
watch a bunch of videos.
152
00:08:17,400 --> 00:08:19,920
There is a personal teacher
who knows everything about you.
153
00:08:21,140 --> 00:08:24,930
It starts to take the learnings, take
the curriculum, and teach you in a manner,
154
00:08:24,930 --> 00:08:27,630
in the context that you
really care about and
155
00:08:27,630 --> 00:08:30,580
what you really live
and breathe every day.
156
00:08:30,580 --> 00:08:31,580
I'll give one example.
157
00:08:32,520 --> 00:08:34,300
I'm from product
and engineering background.
158
00:08:34,540 --> 00:08:36,340
Nothing against people
in finance or accounting.
159
00:08:37,200 --> 00:08:41,980
I find cost amortization
a little bit dry on the subject.
160
00:08:42,620 --> 00:08:44,040
I try to learn it a bunch of times.
161
00:08:44,400 --> 00:08:45,400
I couldn't make a lot of [unclear].
162
00:08:45,760 --> 00:08:49,920
When I was engaging with the teacher,
learning about cost amortization, it
163
00:08:49,920 --> 00:08:53,340
looked at my engagement pattern
and clearly saw I was not engaged.
164
00:08:53,760 --> 00:08:55,120
It's like, hey, let's take a pause.
165
00:08:56,140 --> 00:08:57,460
You work at MasterClass.
166
00:08:57,540 --> 00:08:58,800
You're an executive at MasterClass.
167
00:08:59,480 --> 00:09:02,900
You must really care about content
amortization or content cost amortization.
168
00:09:03,300 --> 00:09:04,300
I was like, heck yeah.
169
00:09:04,720 --> 00:09:06,100
I want to know more about it.
170
00:09:06,100 --> 00:09:10,440
And then it took the curriculum and it
taught me cost amortization from the
171
00:09:10,440 --> 00:09:14,680
frame of how should I think about
it with content cost amortization.
172
00:09:15,100 --> 00:09:18,050
All of a sudden, I'm more engaged
because I can actually use this tomorrow,
173
00:09:18,050 --> 00:09:19,540
this information tomorrow.
174
00:09:19,940 --> 00:09:22,260
I am like grokking things
much faster because
175
00:09:22,260 --> 00:09:24,700
it's way more personalized for my context.
176
00:09:25,320 --> 00:09:27,320
So at the root of MasterClass executive,
177
00:09:27,320 --> 00:09:30,240
there's an AI teacher
that you engage with.
178
00:09:30,360 --> 00:09:32,460
And the teacher has hundreds of videos.
179
00:09:32,680 --> 00:09:35,160
We have 20 different tools that it has.
180
00:09:35,360 --> 00:09:38,910
And it will leverage all of that to teach
you a concept from the context that
181
00:09:38,910 --> 00:09:42,300
you care about in an extremely,
extremely personalized way.
182
00:09:43,260 --> 00:09:46,780
And the feedback we are getting, what
we are seeing from our founding cohort
183
00:09:46,780 --> 00:09:48,280
has been phenomenal.
184
00:09:49,160 --> 00:09:50,500
People are loving the experience.
185
00:09:51,020 --> 00:09:52,940
People are leaning in a lot.
186
00:09:52,940 --> 00:09:57,220
Although it's a very active learning
experience, the time to learn thing has
187
00:09:57,220 --> 00:09:59,420
shortened and it's way more sticky.
188
00:09:59,940 --> 00:10:04,130
And the AI is able to like dive deep
into your background, understand what you
189
00:10:04,130 --> 00:10:07,640
are really good at, and then teach from
that standpoint where you are good at
190
00:10:07,640 --> 00:10:08,860
and where you struggle.
191
00:10:09,860 --> 00:10:13,440
Now, at the root of all of this,
this is all well and great.
192
00:10:13,760 --> 00:10:18,360
And we do, the team does fantastic job in
terms of writing rubrics, writing evals,
193
00:10:18,360 --> 00:10:20,800
doing red teaming on it, pre-launch.
194
00:10:20,880 --> 00:10:21,680
All of that is good.
195
00:10:21,680 --> 00:10:25,920
But how do we make sure that once we
are in production, the architecture that
196
00:10:25,920 --> 00:10:27,780
we got, did we get it right?
197
00:10:28,420 --> 00:10:29,420
Are we doing a good job?
198
00:10:29,520 --> 00:10:33,380
And this is where Priya and her team
have been hard at work, and I'm going to
199
00:10:33,380 --> 00:10:35,820
hand it over to Priya to talk
about the architecture.
200
00:10:37,580 --> 00:10:38,380
Awesome.
201
00:10:38,380 --> 00:10:39,380
Thanks, Mandar.
202
00:10:40,940 --> 00:10:41,660
So I'll start by explaining the
203
00:10:41,660 --> 00:10:44,470
architecture of our
MCX system, and through
204
00:10:44,470 --> 00:10:49,440
that, we can explain how we do
this whole personalized learning.
205
00:10:50,280 --> 00:10:56,120
So at its core, MCX is a multi-agent
system that consists of four agents.
206
00:10:56,580 --> 00:11:00,080
We have the planner,
orchestrator, teacher, and memory.
207
00:11:00,740 --> 00:11:03,180
And then these combine
together to give that
208
00:11:03,180 --> 00:11:05,920
amazing experience that
you saw in the video.
209
00:11:05,920 --> 00:11:10,850
They are capable of engaging learners
on sessions that can be like hours long
210
00:11:10,850 --> 00:11:14,160
and a learning journey
that can be months long.
211
00:11:15,040 --> 00:11:20,280
The planner agent is responsible for
designing a curriculum for a learner to
212
00:11:20,280 --> 00:11:24,750
follow in a way that I will completely
teach them the concept using a variety
213
00:11:24,750 --> 00:11:26,120
of different tools.
214
00:11:26,880 --> 00:11:29,160
The orchestrator and the
teacher are our main agent.
215
00:11:29,620 --> 00:11:32,380
You can think of orchestrator
as kind of like a router.
216
00:11:32,920 --> 00:11:37,330
Its job is to decide whether to stay on
the current topic and teach it more or
217
00:11:37,330 --> 00:11:39,540
to transition to the next one.
218
00:11:40,060 --> 00:11:42,560
I think of the orchestrator
as more like a head teacher.
219
00:11:42,940 --> 00:11:46,700
So it's looking at everything that's
going on, what's the learner doing, how
220
00:11:46,700 --> 00:11:50,940
the teacher is teaching, what
the completion criteria for something is.
221
00:11:51,300 --> 00:11:55,010
And based on that, it decides whether
the subject has been taught enough and I
222
00:11:55,010 --> 00:11:57,140
should move on or I should stay here.
223
00:11:57,320 --> 00:11:59,000
And it also connects to the teacher.
224
00:11:59,120 --> 00:12:02,060
So it gives it feedback saying, hey,
you know what, we've covered this well
225
00:12:02,060 --> 00:12:04,220
enough, but this aspect
we haven't touched on.
226
00:12:04,280 --> 00:12:06,220
So let's do that and then let's move on.
227
00:12:07,060 --> 00:12:11,130
The teacher is the main agent that
delivers the whole personalized learning
228
00:12:11,130 --> 00:12:13,400
experience that Mandar talked about.
229
00:12:13,640 --> 00:12:19,740
It has all the pedagogy principles so
that we are not spoon feeding answers.
230
00:12:19,880 --> 00:12:22,180
We're pushing people,
pushing them the right amount.
231
00:12:22,740 --> 00:12:25,000
And it's connected to our memory agent.
232
00:12:25,380 --> 00:12:27,880
The memory is what allows us
to personalize the experience.
233
00:12:28,480 --> 00:12:31,300
Inside memory, we store
a bunch of different
234
00:12:31,300 --> 00:12:34,240
things like background on the user.
235
00:12:34,240 --> 00:12:38,170
For example, for Mandar, it knows his
background and how it can teach the
236
00:12:38,170 --> 00:12:41,190
concept to them, as well
as learner strengths,
237
00:12:41,190 --> 00:12:43,640
weaknesses, what their
learning preferences are.
238
00:12:44,020 --> 00:12:47,960
And the teacher agent uses that
to actively personalize experience.
239
00:12:48,180 --> 00:12:52,200
So two people going through the same
course will have very different journeys.
240
00:12:52,600 --> 00:12:56,590
And the goal of this entire experience
is to actually teach you the concept so
241
00:12:56,590 --> 00:12:57,980
that it sticks for you.
242
00:12:59,540 --> 00:13:03,800
And then so overall, I mean, this is
a fairly complex system of agents.
243
00:13:04,000 --> 00:13:06,880
And we use CoreWeave to track everything.
244
00:13:06,980 --> 00:13:08,040
They have a product called Weave.
245
00:13:08,540 --> 00:13:13,080
And so everything here, all the input,
output prompts for each of the agents,
246
00:13:13,080 --> 00:13:17,600
the tools they use, their reasoning,
their rationale, all of that is stored in
247
00:13:17,600 --> 00:13:18,640
CoreWeave.
248
00:13:18,640 --> 00:13:24,190
So as you can imagine, this becomes like
a huge amount of data, but it's a real
249
00:13:24,190 --> 00:13:30,250
goldmine of data that traditionally would
have been very difficult to mine and
250
00:13:30,250 --> 00:13:34,100
understand, like, how we improve
experiences for our individual learners.
251
00:13:34,620 --> 00:13:36,660
And that's the core problem
that we've solved here.
252
00:13:37,340 --> 00:13:39,860
And that's the bulk
of what my talk is about.
253
00:13:40,660 --> 00:13:45,120
Now that we have this data, we're actually
able to use it in three different ways.
254
00:13:46,020 --> 00:13:48,640
We're able to answer any hard questions.
255
00:13:48,860 --> 00:13:52,390
So if somebody had a bad experience,
we can understand, you know, why, what
256
00:13:52,390 --> 00:13:53,720
potentially led to it.
257
00:13:54,040 --> 00:13:58,040
If we ourselves want to QA our entire
data set and ask about specific things,
258
00:13:58,040 --> 00:14:00,560
we can pose questions and get answers.
259
00:14:01,560 --> 00:14:07,110
And secondly, if we do identify any
failures, we can identify other patterns,
260
00:14:07,110 --> 00:14:11,330
other failures of the same kind,
and make issue data sets, which are very
261
00:14:11,330 --> 00:14:12,820
useful for testing fixes.
262
00:14:13,700 --> 00:14:19,330
And finally, this is also helping us
to get into a spot where we're monitoring
263
00:14:19,330 --> 00:14:25,620
our portfolio in a more automated fashion,
where, you know, there's loops in
264
00:14:25,620 --> 00:14:30,360
there to check for experiences
and flag issues for us.
265
00:14:30,560 --> 00:14:32,480
So I'll talk about all of these pieces.
266
00:14:33,260 --> 00:14:37,510
The main thing that allows us to do
all of this, the basic Lego block, is a
267
00:14:37,510 --> 00:14:40,800
tracing skill that we
built through CoreWeave.
268
00:14:41,660 --> 00:14:44,880
This tracing skill has
three main components.
269
00:14:45,400 --> 00:14:48,160
There is an MCP server that
we built through CoreWeave.
270
00:14:49,120 --> 00:14:52,870
There's the skill itself, the logic
of the skill that tells how to use the
271
00:14:52,870 --> 00:14:55,540
server to search through the traces.
272
00:14:56,460 --> 00:15:00,550
And then finally, we have attached a
memory book so that the skill is actually
273
00:15:00,550 --> 00:15:01,700
self-learning.
274
00:15:02,200 --> 00:15:06,220
So essentially, you can give the skill to,
like, a Claude Code or a Cursor agent,
275
00:15:06,220 --> 00:15:10,540
and they're able to then look through
the traces to identify whatever they were
276
00:15:10,540 --> 00:15:11,560
looking for.
277
00:15:12,560 --> 00:15:16,680
The server that CoreWeave has,
has in it four different tools.
278
00:15:17,180 --> 00:15:21,040
These tools are pretty generic tools,
and they can be used by anybody.
279
00:15:21,400 --> 00:15:25,120
And there's nothing special
purpose for our use case here.
280
00:15:25,700 --> 00:15:30,220
The first tool is a tool to infer
the schema of the traces.
281
00:15:31,800 --> 00:15:33,990
Then we have a tool to count traces and
282
00:15:33,990 --> 00:15:36,720
return how many counts
were hit on a query.
283
00:15:37,320 --> 00:15:39,640
And then finally,
we have two different tools.
284
00:15:40,100 --> 00:15:44,200
One of them does a shallow scan of the
trace, and the other does a deep scan.
285
00:15:44,800 --> 00:15:49,610
And I'll kind of now show you how this
combination of tools along with the
286
00:15:49,610 --> 00:15:54,860
agent can actually become a very
powerful, almost magical combination.
287
00:15:55,680 --> 00:15:59,440
So, for example, we, let's say, let's
take a hypothetical example of a learner
288
00:15:59,440 --> 00:16:04,820
who, when encountering a concept in
the learner, in the teaching experience,
289
00:16:04,820 --> 00:16:07,120
said, wait, what's this?
290
00:16:07,320 --> 00:16:08,620
Did you actually teach me this?
291
00:16:08,700 --> 00:16:09,700
Because I don't remember that.
292
00:16:10,080 --> 00:16:13,480
That particular thing can be said so
many different ways by so many people.
293
00:16:14,040 --> 00:16:15,760
It could be just expressed as confusion.
294
00:16:15,900 --> 00:16:18,060
It could be like, you know,
I don't remember this.
295
00:16:18,060 --> 00:16:22,630
But all of those do imply that whenever
we taught the concept, we could
296
00:16:22,630 --> 00:16:26,060
probably have done a better
job of finding that.
297
00:16:26,920 --> 00:16:31,100
And so this is a very fuzzy kind of
search, and this would have been very hard
298
00:16:31,100 --> 00:16:32,180
in the past.
299
00:16:32,800 --> 00:16:38,640
But now the way the system does this by
using, so the system is able to use the
300
00:16:38,640 --> 00:16:42,260
tools inside the CoreWeave MCP to do that.
301
00:16:42,740 --> 00:16:45,680
And the way it does that is it
makes a whole bunch of hypotheses.
302
00:16:45,880 --> 00:16:50,280
It doesn't know what phrases to search
for to find learner confusion.
303
00:16:50,760 --> 00:16:53,920
So it's going to make like, you know,
maybe make 10, 15 hypotheses.
304
00:16:54,020 --> 00:16:58,400
And then it's going to go hit the count
traces tool to see, you know, whether
305
00:16:58,400 --> 00:17:00,120
that path is valid or not.
306
00:17:00,540 --> 00:17:04,220
If the traces are very low or they're
very high, it knows it's a dead path.
307
00:17:04,300 --> 00:17:05,300
It's going to prune them.
308
00:17:05,660 --> 00:17:09,670
And then the ones that seem viable,
it's then going to use the shallow scan
309
00:17:09,670 --> 00:17:11,880
tool to get an idea of the trace.
310
00:17:11,960 --> 00:17:13,460
It's going to read a bit
of the conversation.
311
00:17:14,120 --> 00:17:19,300
And then it will know whether it's on
the right path or something can be fixed.
312
00:17:19,860 --> 00:17:23,160
And so basically it goes back and forth.
313
00:17:23,240 --> 00:17:24,240
It makes more hypotheses.
314
00:17:24,480 --> 00:17:25,320
It counts them.
315
00:17:25,320 --> 00:17:26,320
It does a shallow scan.
316
00:17:26,760 --> 00:17:30,650
Once it feels like it's in a good spot,
it can then look at the deep scan tool
317
00:17:30,650 --> 00:17:33,700
and now pull more of the data,
look through it.
318
00:17:33,980 --> 00:17:37,060
It can start to look at what
happened in the multi-agent system.
319
00:17:37,260 --> 00:17:39,460
What did different
agents say to each other
320
00:17:39,460 --> 00:17:41,940
and through that start
to build hypotheses.
321
00:17:42,900 --> 00:17:46,290
And so essentially when you call the tool,
it could be anywhere between 20 and
322
00:17:46,290 --> 00:17:50,590
100 tool calls it has done to fetch
different things, check different things,
323
00:17:50,590 --> 00:17:52,780
and then it presents its
hypothesis back to you.
324
00:17:53,200 --> 00:17:55,940
And you can take over from there
and dig into any different aspect.
325
00:17:58,940 --> 00:18:04,050
So as I mentioned, the system searches
in a way that only agents can by just
326
00:18:04,050 --> 00:18:07,430
looking in broad,
looking across many things,
327
00:18:07,430 --> 00:18:10,400
just doing a whole bunch of tool calls.
328
00:18:11,060 --> 00:18:14,680
And so we wanted to make the system more
intelligent over time, and that's why
329
00:18:14,680 --> 00:18:16,660
we attached a memory book to it.
330
00:18:17,180 --> 00:18:22,830
What the memory has is information on
good ways to search, things that worked
331
00:18:22,830 --> 00:18:25,880
well in the past, do's and don'ts.
332
00:18:26,100 --> 00:18:29,960
And so when a new agent starts a search,
it can look at its memory book, and it
333
00:18:29,960 --> 00:18:33,840
already is a little bit more efficient
because it knows how to approach it.
334
00:18:35,160 --> 00:18:39,940
But we have many people in our team
use this tool, so we went a level up.
335
00:18:40,400 --> 00:18:44,940
And what we did is we started recording,
we started pushing all of those traces
336
00:18:44,940 --> 00:18:49,500
as well of just the tool use into
a different project on CoreWeave.
337
00:18:49,500 --> 00:18:52,440
And so now, in a very
kind of metacognitive
338
00:18:52,440 --> 00:18:54,920
way, we are also storing the traces
339
00:18:54,920 --> 00:18:57,680
of the agent doing the trace search.
340
00:18:58,560 --> 00:19:03,470
And this becomes a flywheel of improvement
because periodically we can look at
341
00:19:03,470 --> 00:19:07,620
that project, look at all the tool calls,
all the paths that the agent went through.
342
00:19:07,620 --> 00:19:12,780
And especially on a bulk, I can figure
out where are patterns that I'm missing,
343
00:19:12,780 --> 00:19:17,790
and what new learnings I can have, and
then put them in the memory book, and so
344
00:19:17,790 --> 00:19:19,680
it becomes a continuous
loop of improvement.
345
00:19:19,680 --> 00:19:24,550
And this kind of pattern of building
skills that iterate and self-improve is a
346
00:19:24,550 --> 00:19:28,620
pretty good pattern that can
be followed elsewhere as well.
347
00:19:28,680 --> 00:19:35,100
So essentially, in a nutshell, we have
a tracing skill that uses a variety of
348
00:19:35,100 --> 00:19:41,340
different tools, and an agent, and memory
to search through things and identify,
349
00:19:41,340 --> 00:19:43,740
like, why something might have happened.
350
00:19:43,740 --> 00:19:49,740
With this, we've been able to unlock
a whole bunch of use cases.
351
00:19:49,740 --> 00:19:54,400
One of the first ones is that if we do
find one instance of a problem through
352
00:19:54,400 --> 00:19:59,350
this, and through all the digging in,
we know that, you know, when something
353
00:19:59,350 --> 00:20:02,740
like A happens, and it leads to B,
and an agent ends up doing C,
354
00:20:02,740 --> 00:20:06,740
then this whole pattern is something
that we can go back to the trace and say,
355
00:20:06,740 --> 00:20:10,800
"Hey, now find me all instances in the
last six months when this has happened."
356
00:20:10,800 --> 00:20:13,740
And usually, you know, what happens
is a single person complains.
357
00:20:13,740 --> 00:20:16,480
There are a lot of people who don't
complain but might have had a similar
358
00:20:16,480 --> 00:20:19,680
experience that's suboptimal,
so it's able to bring all of that up.
359
00:20:19,740 --> 00:20:23,600
In that dataset that it brings, there
are also all the input prompts for the
360
00:20:23,600 --> 00:20:26,190
different agents, so this becomes very
361
00:20:26,190 --> 00:20:29,740
useful if you are trying
to find a solution.
362
00:20:29,740 --> 00:20:34,320
You can iterate on that right away
and try different, you know, fixes, test
363
00:20:34,320 --> 00:20:40,710
them, replay them, and so this helps us
actually build more efficient solutions
364
00:20:40,710 --> 00:20:41,740
on the go.
365
00:20:45,740 --> 00:20:50,740
We've also started to use this tracing
skill to do a lot more monitoring.
366
00:20:50,740 --> 00:20:52,740
We do two kinds of monitoring.
367
00:20:52,740 --> 00:20:58,830
The first is automated monitoring where
we're monitoring all different aspects
368
00:20:58,830 --> 00:21:01,960
of our production experience, and we
369
00:21:01,960 --> 00:21:06,810
then have agents go and basically extract
370
00:21:06,810 --> 00:21:09,500
anything that would be meaningful for
us to look at in terms of trends and
371
00:21:09,500 --> 00:21:11,740
stuff and surface that to us.
372
00:21:11,740 --> 00:21:14,680
I would call that more
standard monitoring that's
373
00:21:14,680 --> 00:21:16,740
kind of happening to agents
on a regular cadence.
374
00:21:16,740 --> 00:21:19,260
But we're also moving
on to more autonomous
375
00:21:19,260 --> 00:21:21,210
monitoring where we don't have to
376
00:21:21,210 --> 00:21:23,740
always be involved in checking things.
377
00:21:23,740 --> 00:21:28,600
And one of the initial ways that we've
done that is by building a bigger skill
378
00:21:28,600 --> 00:21:31,740
that is connecting
a whole bunch of things.
379
00:21:31,740 --> 00:21:34,100
It's connecting our
traces, it's connecting
380
00:21:34,100 --> 00:21:36,020
our GitHub, our Jira board, and it's
381
00:21:36,020 --> 00:21:40,960
also connected to the community pages
where our learners share both positive
382
00:21:40,960 --> 00:21:41,740
and negative feedback with us.
383
00:21:41,740 --> 00:21:45,810
So if a learner has
flagged something that's
384
00:21:45,810 --> 00:21:49,740
of concern to them, then the meta-skill
385
00:21:49,740 --> 00:21:55,810
is able to look through the traces
and identify what happened, go look for
386
00:21:55,810 --> 00:22:00,370
other cases and automatically make an
issue data set, check our Jira and GitHub
387
00:22:00,370 --> 00:22:03,740
to see if we are working on them,
and if we're not, then flag that to us and
388
00:22:03,740 --> 00:22:09,490
then we can take over and start to look
at and see if this is something that we
389
00:22:09,490 --> 00:22:09,740
should investigate more.
390
00:22:09,740 --> 00:22:16,160
So essentially, I think once you do
have a good way of looking through your
391
00:22:16,160 --> 00:22:21,640
traces, there's a lot of different use
cases that get enabled and ultimately
392
00:22:21,640 --> 00:22:25,580
the kind of holy grail here is a system
that more and more automatically
393
00:22:25,580 --> 00:22:32,070
understands where somebody has had
an experience that can be improved and it
394
00:22:32,070 --> 00:22:35,810
starts to cluster them, identify more
of them and helps you with creating all
395
00:22:35,810 --> 00:22:37,740
the data sets and stuff so that
you can go ahead and solve it.
396
00:22:37,740 --> 00:22:45,740
So in conclusion, I want to leave with
397
00:22:45,740 --> 00:22:47,980
five key findings or key things to walk
398
00:22:47,980 --> 00:22:52,500
away with. First is that it's important
to trace everything, not just the
399
00:22:52,500 --> 00:22:56,920
inputs and outputs, not just the user
message and your assistant message, but
400
00:22:56,920 --> 00:23:00,940
everything in the middle because that's
where there's a lot of value in knowing
401
00:23:00,940 --> 00:23:04,740
why the system behaves a certain way.
402
00:23:04,740 --> 00:23:07,060
So, you can now connect these traces to an
403
00:23:07,060 --> 00:23:09,740
agent in the agent ops
kind of way that we did.
404
00:23:09,740 --> 00:23:15,530
So you should try and make the skill more
effective and self-learning so attach
405
00:23:15,530 --> 00:23:19,740
a journal to it so it can record itself,
it can become more efficient over time.
406
00:23:19,740 --> 00:23:23,680
And then use the findings to build bigger
407
00:23:23,680 --> 00:23:27,030
data sets that can then help you with
408
00:23:27,030 --> 00:23:28,740
iterating on your fixes.
409
00:23:28,740 --> 00:23:33,060
And then finally, the overall bigger
picture here is to then enable more
410
00:23:33,060 --> 00:23:34,740
automated monitoring.
411
00:23:38,000 --> 00:23:42,160
Awesome. Before I end,
I just want to play this video.
412
00:23:43,680 --> 00:23:49,460
For three years, [unclear] was
focused on teaching one kid.
413
00:23:50,040 --> 00:23:51,740
That kid became Alexander the Great.
414
00:23:52,260 --> 00:23:56,740
For 2,000 years, that kind of mentorship
was reserved only for [unclear].
415
00:23:57,380 --> 00:23:58,380
But that's all about to change.
416
00:24:03,040 --> 00:24:05,360
This program has the potential
to change your life.
417
00:24:05,800 --> 00:24:07,780
We are looking for people
who want to do the work.
418
00:24:08,000 --> 00:24:11,020
If that's you, I can't wait
to see how this changes you.
419
00:24:11,980 --> 00:24:12,980
MasterClass Executive.
420
00:24:13,320 --> 00:24:15,600
The next cohort is enrolling right now.
421
00:24:15,980 --> 00:24:16,980
Apply for free today.
422
00:24:19,380 --> 00:24:20,660
Thank you, everyone, for joining.
423
00:24:21,400 --> 00:24:23,000
Thanks so much. Have
a wonderful day ahead.
424
00:24:23,300 --> 00:24:24,300
Thank you.
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
