# Inside Pinterest's Machine Learning Platform | CoreWeave

Source: https://www.coreweave.com/resources/videos/fueling-innovation-at-scale-inside-pinterests-machine-learning-platform

Announcement

Webinar

Podcast

GTC 2026

CoreWeave Forge is here: connect your AI loop and compound every improvement. Read more

Contact us

Copied

Overview
Transcript

In this on-demand session, Pinterest’s Jose Lopez and Priyanka Taneja share how the company’s machine learning platform has evolved across each stage of that lifecycle. Hear what Pinterest learned from its migration to W&B Models, including what became easier, what challenges emerged, and which tradeoffs shaped the journey. You’ll leave with practical guidance on what to prioritize as your own model lifecycle matures.
Speakers: Jose Lopez, Software Engineer, Pinterest; Priyanka Taneja, Software Engineer, Pinterest

00:00

1
00:00:00,000 --> 00:00:07,000
Hey, everyone. Thanks for
attending our session.
2
00:00:07,000 --> 00:00:09,160
I'm Jose, and this is Priyanka,
3
00:00:09,160 --> 00:00:12,630
and we're both software engineers at
Pinterest. I work on model deployment and
4
00:00:12,630 --> 00:00:17,380
model serving, and Priyanka works on
ML training, model registration, and
5
00:00:17,380 --> 00:00:21,870
experiment tracking. And over the past
year, we've been working on migrating
6
00:00:21,870 --> 00:00:25,840
Pinterest ML platform from MLflow
to Weights & Biases, and in this session,
7
00:00:25,840 --> 00:00:29,660
we'll discuss how we approach
that, along with our learnings
8
00:00:29,660 --> 00:00:34,400
on both the training and the serving side.
For the agenda, I'll first start off
9
00:00:34,400 --> 00:00:37,270
by giving a brief
introduction on Pinterest
10
00:00:37,270 --> 00:00:39,300
ML platform, and then Priyanka will
11
00:00:39,300 --> 00:00:43,010
cover why we migrated to Weights &
Biases, along with how we approach the
12
00:00:43,010 --> 00:00:46,960
migration, and then I'll come back
to discuss how we integrated weights and
13
00:00:46,960 --> 00:00:50,580
biases into the serving side, and then
I'll wrap it up by discussing our future
14
00:00:50,580 --> 00:00:52,840
plans and opening it up for any questions.
15
00:00:55,320 --> 00:00:58,680
So at Pinterest, our mission is to bring
everyone the inspiration to create a life
16
00:00:58,680 --> 00:01:03,220
they love, and just a couple of main views
we have where users come to interact with.
17
00:01:03,820 --> 00:01:07,440
First is home feed, which will give you
recommendations based on your interest.
18
00:01:08,160 --> 00:01:12,680
Search, which given like an image or a
query will help you find specific ideas.
19
00:01:13,440 --> 00:01:17,820
Related pins, which given a pin will
help you find pins similar to those.
20
00:01:18,320 --> 00:01:22,260
And then a shopping, which helps
you connect your ideas to products.
21
00:01:23,260 --> 00:01:26,900
And with all these views, they're
all powered by machine learning.
22
00:01:29,040 --> 00:01:32,900
So to give you a sense of the skill we're
working with, Pinterest has over 580
23
00:01:32,900 --> 00:01:38,610
million monthly active users, with
over 390 billion pins saved, with ML
24
00:01:38,610 --> 00:01:40,580
workloads running on thousands of GPUs.
25
00:01:41,320 --> 00:01:45,820
And on these GPUs, we have a variety
of models, for example, like recommender
26
00:01:45,820 --> 00:01:50,560
models, which help us decide which pins
to show users, or object detection and
27
00:01:50,560 --> 00:01:54,760
representation learning models, which
help us understand the content, or visual
28
00:01:54,760 --> 00:01:56,760
search, which help us find specific ideas.
29
00:01:57,760 --> 00:02:01,710
And with a large variety of models,
it means we had to have a very reliable
30
00:02:01,710 --> 00:02:05,980
platform for engineers to come train,
track, and deploy their models.
31
00:02:07,980 --> 00:02:13,490
So at Pinterest ML platform, we support
over 400 ML engineers, running over 30,000
32
00:02:13,490 --> 00:02:16,820
ML workloads a week, across
300 different use cases.
33
00:02:17,420 --> 00:02:21,570
On the data side, we work with around
300 petabytes of data, and on the serving
34
00:02:21,570 --> 00:02:26,550
side, we deploy around 500 models a week,
and run inference on over 400 million
35
00:02:26,550 --> 00:02:27,600
items per second.
36
00:02:28,740 --> 00:02:32,120
And at this scale, there's always someone
like either deploying their model,
37
00:02:32,120 --> 00:02:35,540
training their model,
or managing their experiments.
38
00:02:36,240 --> 00:02:40,520
So during the migration, it was very
important for us to make sure, like their
39
00:02:40,520 --> 00:02:44,000
existing tools and workflows
remain without any disruption.
40
00:02:45,100 --> 00:02:48,720
And to, and Priyanka will now explain how
we approach that on the training side.
41
00:02:49,160 --> 00:02:49,600
Okay, yeah.
42
00:02:49,600 --> 00:02:50,900
Thank you, Jose, for the context.
43
00:02:51,060 --> 00:02:54,960
So I'll just give a brief overview
of our ML training runtime infra.
44
00:02:55,320 --> 00:02:57,410
So we basically broadly
spread infrastructure
45
00:02:57,410 --> 00:02:59,100
into one, ML runtime, and two,
46
00:02:59,100 --> 00:03:00,820
the compute infrastructure.
47
00:03:01,400 --> 00:03:05,430
So the compute infrastructure basically
sits on top of AWS and K8s, and there
48
00:03:05,430 --> 00:03:09,500
we seek to provide GPUs for ML
training and batch inference workloads.
49
00:03:09,960 --> 00:03:11,820
We call this layer
the training compute platform.
50
00:03:12,260 --> 00:03:15,440
And this includes things like job
management, scheduling, auto scaling, and
51
00:03:15,440 --> 00:03:16,460
fault tolerance.
52
00:03:16,880 --> 00:03:21,560
On top of that sits ML runtime, and these
are basically our internal libraries
53
00:03:21,560 --> 00:03:26,210
and SDKs on top of Ray and PyTorch that
we provide to accelerate ML training
54
00:03:26,210 --> 00:03:27,360
and batch inference workloads.
55
00:03:27,580 --> 00:03:29,480
But the part that we're
going to focus on today
56
00:03:29,480 --> 00:03:31,640
is experiment tracking
and the model registry.
57
00:03:32,580 --> 00:03:35,650
So before we dive into how we migrated
our experiment tracking platform, I'll
58
00:03:35,650 --> 00:03:38,260
briefly explain what
experiment tracking is.
59
00:03:38,400 --> 00:03:41,900
So let's say you're an ML engineer and
your training models to present the most
60
00:03:41,900 --> 00:03:43,500
clickable ad to the end user.
61
00:03:43,740 --> 00:03:46,070
You'd want to train a bunch of different
models on a bunch of different
62
00:03:46,070 --> 00:03:48,420
parameters to figure out which
produces the best results.
63
00:03:48,900 --> 00:03:53,220
So sure, you could save all your metrics
and weights locally or on GitHub, but
64
00:03:53,220 --> 00:03:58,030
we wanted to offer something a bit richer,
and that's where experiment tracking
65
00:03:58,030 --> 00:03:59,360
platforms come in.
66
00:03:59,900 --> 00:04:02,970
So all these training runs sit in
a centralized platform where they can find
67
00:04:02,970 --> 00:04:06,840
all their experiments, model metrics,
files, and weights for each run.
68
00:04:06,900 --> 00:04:10,600
So they can then use this information
to analyze and iterate and compare their
69
00:04:10,600 --> 00:04:12,690
models, and once they
found a model they're
70
00:04:12,690 --> 00:04:14,510
happy with, they can register their
71
00:04:14,510 --> 00:04:17,680
models under the model registry, which
is just a centralized place to store
72
00:04:17,680 --> 00:04:21,590
models as immutable, and then our serving
infrastructure then reads the models
73
00:04:21,590 --> 00:04:23,000
from the registry to deploy them online.
74
00:04:24,280 --> 00:04:27,630
Okay, so now we have a broad understanding
of what experiment tracking actually
75
00:04:27,630 --> 00:04:31,040
is, let's discuss some of the challenges
we've been dealing with it at Pinterest.
76
00:04:31,620 --> 00:04:35,540
So back in 2019, we actually forked
MLflow to add some custom logic, and while
77
00:04:35,540 --> 00:04:39,540
a lot of the times the internal fork is
never the way to go, it's been really
78
00:04:39,540 --> 00:04:42,000
hard to upgrade our
internal library, and we're
79
00:04:42,000 --> 00:04:44,160
stuck on a version that's
about five years old.
80
00:04:44,260 --> 00:04:48,240
So as a result, the current experiment
tracking is pretty unreliable.
81
00:04:48,720 --> 00:04:52,530
We've had numerous outages, and it was
never meant to handle MLM at the scale
82
00:04:52,530 --> 00:04:53,760
that it is today.
83
00:04:54,280 --> 00:04:58,470
It's also slowing down dev velocity,
so a very specific example is all of our
84
00:04:58,470 --> 00:05:03,140
forking and logging operations are
physically copying each file to S3 every
85
00:05:03,140 --> 00:05:05,400
single time, which can
be so slow sometimes
86
00:05:05,400 --> 00:05:07,330
at times out, and this is becoming
87
00:05:07,330 --> 00:05:10,720
untenable, especially for
larger models like LLMs.
88
00:05:10,720 --> 00:05:13,720
And generally, this platform is
just in maintenance mode, and no new
89
00:05:13,720 --> 00:05:17,260
innovations are coming out of it, and it's
basically a sunk cost at this point.
90
00:05:17,640 --> 00:05:21,380
So our solution is replacing our old
system with Weights & Biases to establish
91
00:05:21,380 --> 00:05:23,220
a new unified MLOps platform.
92
00:05:24,220 --> 00:05:27,850
Okay, and now although we know we want
to migrate to Weights & Biases, I just
93
00:05:27,850 --> 00:05:30,460
want to add some context
on what that really means.
94
00:05:30,580 --> 00:05:33,450
It would be great if we could just
turn it on and be done with it, but
95
00:05:33,450 --> 00:05:35,370
experiment tracking is actually a really
96
00:05:35,370 --> 00:05:37,180
important piece
of infrastructure at Pinterest,
97
00:05:37,460 --> 00:05:41,370
and it's on the critical path for model
deployment, and therefore has direct
98
00:05:41,370 --> 00:05:42,460
revenue impact.
99
00:05:42,860 --> 00:05:46,030
So if it's down, models that curate
a pinner's feed can go stale, or models
100
00:05:46,030 --> 00:05:48,420
that fetch the right
ads can be out of date.
101
00:05:48,660 --> 00:05:50,900
So we want to approach this
migration very carefully.
102
00:05:50,900 --> 00:05:55,190
And first, we decided some overarching
goals we wanted to achieve, and the
103
00:05:55,190 --> 00:05:59,420
three main goals were one, system parity,
so no changes in model quality,
104
00:05:59,420 --> 00:06:00,620
content, or performance.
105
00:06:00,620 --> 00:06:01,900
Two, no downtime.
106
00:06:01,900 --> 00:06:05,360
As I mentioned, it's a very critical
piece of infrastructure, and any sort of
107
00:06:05,360 --> 00:06:07,900
model staleness or downtime
can be very costly.
108
00:06:07,900 --> 00:06:11,450
And three, we didn't want to just maintain
the exact same system, but we also
109
00:06:11,450 --> 00:06:14,300
wanted to add innovation
and improvements along the way.
110
00:06:14,300 --> 00:06:17,700
Having these goals helped guide
how we went about the migration.
111
00:06:17,700 --> 00:06:22,150
Okay, I won't get too into the technical
details, but I wanted to highlight a
112
00:06:22,150 --> 00:06:24,210
few techniques and strategies we used for
113
00:06:24,210 --> 00:06:25,940
the migration that we
found really helpful.
114
00:06:25,940 --> 00:06:31,220
So a general strategy is we did a parallel
migration, and what that means is we
115
00:06:31,220 --> 00:06:35,700
supported both MLflow, our old system,
and Weights & Biases at the same time.
116
00:06:36,260 --> 00:06:39,850
And while there's a higher operational
cost, maintaining both platforms at the
117
00:06:39,850 --> 00:06:41,860
same time, this mitigated
a lot of risk and
118
00:06:41,860 --> 00:06:44,260
impact, as we can fall
back to MLflow at any time.
119
00:06:45,020 --> 00:06:48,330
Specifically, a few things we did
to achieve this was we added automatic
120
00:06:48,330 --> 00:06:52,590
logging to all of our MLflow tracking
functions, so they would log to weights
121
00:06:52,590 --> 00:06:54,100
and bias in the background as well.
122
00:06:54,500 --> 00:06:57,030
This way, ML engineers did not have
to make any changes on their side, but
123
00:06:57,030 --> 00:06:59,420
found their runs on Weights
& Biases automatically.
124
00:07:00,220 --> 00:07:03,250
We also provided some self-serve
tools that were really easy to use, so
125
00:07:03,250 --> 00:07:06,570
engineers could find out if their models
or runs were missing from weights and
126
00:07:06,570 --> 00:07:09,620
bias and use those tools to copy
from MLflow to Weights & Biases.
127
00:07:10,060 --> 00:07:11,380
And then this brings
us to our third point.
128
00:07:11,500 --> 00:07:14,890
We didn't want engineers to just rely
on these tools and always copy from the
129
00:07:14,890 --> 00:07:16,460
old system to the new system.
130
00:07:16,780 --> 00:07:19,880
We wanted to incentivize them to actually
onboard onto the new Weights & Biases
131
00:07:19,880 --> 00:07:22,120
system and use it as
the first-class platform.
132
00:07:22,620 --> 00:07:25,910
So you had to find a balance between
automating parts of the migration and
133
00:07:25,910 --> 00:07:30,150
creating enough friction for the engineers
to actually motivate them to onboard,
134
00:07:30,150 --> 00:07:31,780
which I think is an inherent problem
135
00:07:31,780 --> 00:07:33,420
whenever you're doing
a parallel migration.
136
00:07:34,420 --> 00:07:37,220
And we also worked really closely with
the serving team to be the final check
137
00:07:37,220 --> 00:07:41,540
before deploying any models from Weights
& Biases to actual online production.
138
00:07:42,140 --> 00:07:44,020
And Jose will talk about
this more in a little bit.
139
00:07:44,420 --> 00:07:48,030
But yeah, having all of these, I think,
really grounded the migration and I
140
00:07:48,030 --> 00:07:49,750
found really helpful if anyone finds
141
00:07:49,750 --> 00:07:52,060
themselves porting over
to weights and bias.
142
00:07:52,620 --> 00:07:56,040
And one of the last things we wanted to
highlight that we did was having good OBS
143
00:07:56,040 --> 00:07:58,560
availability from the start
was immensely helpful.
144
00:07:59,100 --> 00:08:01,680
And some things we built were dashboards
that would track jobs that were
145
00:08:01,680 --> 00:08:05,500
missing from Weights & Biases so then we
can go find them, root cause why, and fix.
146
00:08:06,340 --> 00:08:07,060
And then this brings us to another
147
00:08:07,060 --> 00:08:08,820
technique that we used
during the migration
148
00:08:08,820 --> 00:08:11,200
that helped a lot,
and that was employing agents.
149
00:08:11,720 --> 00:08:15,460
And I just mentioned we added all this
automatic logging to Weights & Biases,
150
00:08:15,460 --> 00:08:18,900
but there are so many different use cases
at Pinterest, so many different users
151
00:08:18,900 --> 00:08:21,100
who have all those custom
scripts, custom logic.
152
00:08:21,740 --> 00:08:24,970
And at first, we would manually migrate
all of these one by one, but once we
153
00:08:24,970 --> 00:08:29,220
collected enough data, we were able
to build an agent to feed all this
154
00:08:29,220 --> 00:08:32,380
information to an agent who could then
identify these custom logging scripts
155
00:08:32,380 --> 00:08:33,880
and apply the code changes as possible.
156
00:08:34,160 --> 00:08:37,420
And this helps speed up the migration
considerably and reduce a lot of tedious
157
00:08:37,420 --> 00:08:38,500
operational work.
158
00:08:39,620 --> 00:08:42,740
Secondly, a lot of our support time was
spent helping new users onboard onto
159
00:08:42,740 --> 00:08:47,230
Weights & Biases, and many of their
questions were simply because it was a new
160
00:08:47,230 --> 00:08:48,340
platform to them.
161
00:08:48,740 --> 00:08:52,200
So since the questions were not super
complex, we decided to automate this and
162
00:08:52,200 --> 00:08:55,740
trained an on-call agent using Pinclaw
to answer these questions, and it was
163
00:08:55,740 --> 00:08:59,230
basically just a one-time investment
where we had to consolidate all these
164
00:08:59,230 --> 00:09:02,690
questions and answers to create a runbook
that we fed to the agent that we
165
00:09:02,690 --> 00:09:04,860
completed during one
of our internal hackathons.
166
00:09:05,420 --> 00:09:08,980
And just for some context, we use Pinclaw,
which is Pinterest agent execution
167
00:09:08,980 --> 00:09:12,700
platform, and it's super helpful, so it
can be directly integrated with Slack
168
00:09:12,700 --> 00:09:14,160
and answer questions there.
169
00:09:15,560 --> 00:09:17,850
And lastly, we also integrated with
Weights & Biases skills, which has been
170
00:09:17,850 --> 00:09:19,700
really helpful for our engineers.
171
00:09:20,200 --> 00:09:21,680
Many of them are using
it to create reports
172
00:09:21,680 --> 00:09:23,530
for their models, eval their models,
173
00:09:23,530 --> 00:09:25,140
and query specific metrics.
174
00:09:25,640 --> 00:09:29,100
It also helped people onboard onto
the specific Pinterest instance and
175
00:09:29,100 --> 00:09:33,220
generally increased dev velocity,
and it also got people more excited about
176
00:09:33,220 --> 00:09:34,820
Weights & Biases because it was easier for
177
00:09:34,820 --> 00:09:37,280
them to learn what
features were available.
178
00:09:38,600 --> 00:09:41,680
Okay, and one of the last things I want
to discuss is just some improvements
179
00:09:41,680 --> 00:09:44,080
that we added along
the way, and one of the
180
00:09:44,080 --> 00:09:46,580
major ones was better dev prod separation.
181
00:09:47,420 --> 00:09:49,460
And so, just some quick
context on what that means.
182
00:09:49,460 --> 00:09:53,320
We can think of dev as an environment
for rapid iterations and experiments,
183
00:09:53,320 --> 00:09:55,490
whereas prod is
an environment for the models
184
00:09:55,490 --> 00:09:57,880
to be very reliable,
compliant, and secure.
185
00:09:58,580 --> 00:10:02,230
You don't ever want anything in dev
to override something in prod, and we want
186
00:10:02,230 --> 00:10:06,720
to make sure all our prod models are
easily reproducible, follow any data
187
00:10:06,720 --> 00:10:10,500
privacy rules or legal
requirements, and a lot
188
00:10:10,500 --> 00:10:11,940
of different models have
different requirements.
189
00:10:11,940 --> 00:10:15,090
So, it's actually a pretty deep problem,
and it's a problem that's often
190
00:10:15,090 --> 00:10:18,470
overlooked and added as an afterthought,
so we wanted to make sure it was the
191
00:10:18,470 --> 00:10:20,040
first principle in our migration.
192
00:10:20,880 --> 00:10:22,110
So, there were two
built-in Weights & Biases
193
00:10:22,110 --> 00:10:24,060
features that helped us achieve this.
194
00:10:24,060 --> 00:10:27,820
One was entity-based access, so basically,
training runs are organized into
195
00:10:27,820 --> 00:10:31,670
different entities, and we used that
to create dev entities and prod entities,
196
00:10:31,670 --> 00:10:35,230
and only prod workflows could
access the prod entities,
197
00:10:35,230 --> 00:10:37,380
and local jobs could
access the dev entities.
198
00:10:37,940 --> 00:10:41,890
Second, we used to have all our models
in one single global registry with every
199
00:10:41,890 --> 00:10:45,740
single model at Pinterest, but now we
have a registry per use case, like per
200
00:10:45,740 --> 00:10:50,780
team, so this better helps manage
access control for specific team models.
201
00:10:51,380 --> 00:10:54,580
And the third one was we added promotion
guardrails so users cannot promote
202
00:10:54,580 --> 00:10:58,910
their models to production if they did
not pass specific production rules, so
203
00:10:58,910 --> 00:11:02,160
this meant if they were missing any files,
or the model didn't have the right
204
00:11:02,160 --> 00:11:04,220
licenses, or it was
failing basic load tests,
205
00:11:04,220 --> 00:11:08,760
they wouldn't allow it to be promoted
to production, and this helped save dev
206
00:11:08,760 --> 00:11:12,870
time in the long run, as users didn't
have to wait to deploy their models
207
00:11:12,870 --> 00:11:16,100
online to find out these issues, but
they could find them upon promotion.
208
00:11:16,940 --> 00:11:19,940
This also helped a lot with
reliability and governance.
209
00:11:20,540 --> 00:11:23,460
And now, just to wrap up, what we would
consider a successful end state of this
210
00:11:23,460 --> 00:11:27,220
migration was one, 100% of models
are onboarded onto Weights & Biases,
211
00:11:27,220 --> 00:11:31,620
two, there's exact parity, so all
the old models are the exact same as the
212
00:11:31,620 --> 00:11:36,050
models now on Weights & Biases, three,
all our read and writes are going
213
00:11:36,050 --> 00:11:38,000
through Weights & Biases,
and four, directly
214
00:11:38,000 --> 00:11:40,050
integrating with our model serving,
215
00:11:40,050 --> 00:11:42,940
so all of their infrastructure
reads from Weights & Biases,
216
00:11:42,940 --> 00:11:44,330
and Jose is going to go into more details
217
00:11:44,330 --> 00:11:46,140
about the migration
from the serving stack.
218
00:11:48,620 --> 00:11:51,500
Alright, thanks, Priyanka. So now I'll
dive into how we integrated weights and
219
00:11:51,500 --> 00:11:52,860
biases into the serving stack.
220
00:11:54,420 --> 00:11:58,280
Just as a quick overview of our serving
stack, we first start with our use
221
00:11:58,280 --> 00:12:03,300
cases, so for example, like ads, home
feed and search, who will send a request
222
00:12:03,300 --> 00:12:05,700
to Scorpion, which is our ranking service.
223
00:12:05,940 --> 00:12:10,740
And Scorpion's job is to fetch and cache
the features, along with calling the
224
00:12:10,740 --> 00:12:12,780
model server and returning
back the output.
225
00:12:13,620 --> 00:12:17,740
Our model server is a Scorpion model
server, whose job it is to load and run
226
00:12:17,740 --> 00:12:20,020
the models that are deployed to it.
227
00:12:20,580 --> 00:12:25,410
And these models run on like PyTorch
and TensorFlow, along with either like CPU
228
00:12:25,410 --> 00:12:28,660
or GPU EC2 hosts,
depending on the model itself.
229
00:12:29,860 --> 00:12:33,800
And to better understand how Weights
& Biases plays a role here, I'll dive
230
00:12:33,800 --> 00:12:37,540
deeper into how we actually get these
models deployed into our model server.
231
00:12:39,700 --> 00:12:43,360
So during deployment, we first start by
fetching all the models a specific use
232
00:12:43,360 --> 00:12:44,540
case needs.
233
00:12:44,540 --> 00:12:48,050
So for example, like all the models that
home feed needs, and then we package
234
00:12:48,050 --> 00:12:49,100
it into a build.
235
00:12:49,680 --> 00:12:53,650
And then this build could be deployed
into the host, which their model server
236
00:12:53,650 --> 00:12:55,900
will pick up the changes
and load the models.
237
00:12:57,100 --> 00:13:01,010
And these use cases have a dedicated set
of hosts, which for the most part will
238
00:13:01,010 --> 00:13:02,640
load the full set of models.
239
00:13:03,300 --> 00:13:06,990
What this means is that if a specific
use case receives a request, any of their
240
00:13:06,990 --> 00:13:08,600
hosts could fulfill it.
241
00:13:09,520 --> 00:13:14,800
And just to reiterate a previous point,
we rank over 400 million items per
242
00:13:14,800 --> 00:13:17,220
second, which means that
during the migration,
243
00:13:17,220 --> 00:13:21,670
it was very important for us to make sure
that no bad models or no small issues
244
00:13:21,670 --> 00:13:22,720
went through,
245
00:13:23,100 --> 00:13:26,500
as a very small issue could quickly
balloon up to a very big incident.
246
00:13:28,600 --> 00:13:32,130
This is a bit of a simplified view
of the previous slide, but there are a
247
00:13:32,130 --> 00:13:35,920
couple key areas in our deployment cycle
where Weights & Biases play a role in.
248
00:13:36,500 --> 00:13:39,520
The first is a build stage, which we
just covered in the previous slide.
249
00:13:40,080 --> 00:13:43,640
So for the use case, we fetch all of its
models and package it into a build.
250
00:13:44,420 --> 00:13:47,600
And before we deploy this build, we want
to make sure that we validate the build.
251
00:13:48,160 --> 00:13:52,690
As Priyanka mentioned, we make sure
that all their files are able to be
252
00:13:52,690 --> 00:13:56,480
accessed, and we also make sure
that it has parity with MLflow.
253
00:13:57,040 --> 00:13:58,780
I'll dive deeper in
this in the next slide.
254
00:13:59,920 --> 00:14:03,680
So once validation goes through, we could
actually look into deploying this build.
255
00:14:04,240 --> 00:14:06,040
So we have good control
of whether we deploy
256
00:14:06,040 --> 00:14:08,000
the MLflow or the weights
and biases build.
257
00:14:08,740 --> 00:14:10,080
And then the final step is monitoring.
258
00:14:10,300 --> 00:14:14,200
So making sure like our logs, our database
records, our metrics, raw integrated
259
00:14:14,200 --> 00:14:15,660
with Weights & Biases.
260
00:14:16,560 --> 00:14:20,300
The important thing here is that there
were a couple of convention differences
261
00:14:20,300 --> 00:14:22,360
between Weights & Biases and MLflow.
262
00:14:22,960 --> 00:14:26,880
For example, like their version
mismatches or like model name uniqueness.
263
00:14:27,840 --> 00:14:29,840
So we had to make sure that
we were able to support those.
264
00:14:32,060 --> 00:14:35,110
So as mentioned in the previous slide,
once we have the build and before we
265
00:14:35,110 --> 00:14:38,060
deploy it, we want to make sure
that we validate the build.
266
00:14:38,840 --> 00:14:40,690
So for the validation step, we fetch every
267
00:14:40,690 --> 00:14:43,700
single Weights & Biases
model in the build.
268
00:14:43,700 --> 00:14:47,760
And we verify that all of its files are
able to be accessed, that they're not
269
00:14:47,760 --> 00:14:49,600
like malformed or corrupted.
270
00:14:50,300 --> 00:14:53,060
And we also make sure that all
the required serving files are present.
271
00:14:54,160 --> 00:14:59,440
The second thing we do is that we fetch
the MLflow equivalent model and then we
272
00:14:59,440 --> 00:15:01,700
verify that they have parity.
273
00:15:02,500 --> 00:15:06,120
So for all of its metadata, we make sure
that, for example, like its version,
274
00:15:06,120 --> 00:15:10,820
its stages, its aliases,
its tags are all matching.
275
00:15:11,520 --> 00:15:16,680
The reason for this is that if other
metadata matches, other files match, then
276
00:15:16,680 --> 00:15:20,580
we won't expect there to be any
big difference in performance
277
00:15:20,580 --> 00:15:23,620
if we deploy either the MLflow
or the Weights & Biases model.
278
00:15:24,260 --> 00:15:28,420
And for the migration, this was very
useful because if we deploy the MLflow
279
00:15:28,420 --> 00:15:32,490
model and everything looks good and we
have the Weights & Biases model that
280
00:15:32,490 --> 00:15:33,540
has parity with it,
281
00:15:33,860 --> 00:15:35,570
we have very high
confidence we could deploy
282
00:15:35,570 --> 00:15:37,460
that model and there will be no issues.
283
00:15:38,180 --> 00:15:41,000
It acted kind of like a green light
for when we could actually migrate.
284
00:15:43,360 --> 00:15:46,610
So during the migration, we also wanted
to make sure we had good control of
285
00:15:46,610 --> 00:15:48,400
which build we actually deployed.
286
00:15:49,540 --> 00:15:51,660
So we updated our build logic.
287
00:15:52,000 --> 00:15:55,590
So instead of just creating the MLflow
build, now it creates both the MLflow
288
00:15:55,590 --> 00:15:59,420
and the Weights & Biases build,
both sharing the same set of models.
289
00:16:00,300 --> 00:16:03,600
So as I mentioned in the previous slide,
once this Weights & Biases build
290
00:16:03,600 --> 00:16:06,610
passes the parity check
and once this MLflow build
291
00:16:06,610 --> 00:16:08,720
is going through
successively with no issues,
292
00:16:09,400 --> 00:16:13,400
this is a bit of a green light for us
to roll out this Weights & Biases build.
293
00:16:13,960 --> 00:16:17,020
And if there's no issue with the Weights
& Biases build and all the metrics
294
00:16:17,020 --> 00:16:20,140
look good, then we have
successfully migrated a use case.
295
00:16:21,420 --> 00:16:24,830
And in case there are any issues, for
example, like if we roll out the weights
296
00:16:24,830 --> 00:16:26,880
and biases build and there's like a metric
297
00:16:26,880 --> 00:16:30,040
drop or some like unknown
issue that pops up,
298
00:16:30,480 --> 00:16:35,020
it's very quick for us to find its
MLflow equivalent build and roll it back.
299
00:16:35,480 --> 00:16:38,620
And this helped in like mitigating
incidents and reducing the impact.
300
00:16:40,700 --> 00:16:44,080
So looking forward, there are a couple
of key areas we want to build on top of.
301
00:16:44,620 --> 00:16:48,080
First is adding like automated
evaluations with Weights & Biases model
302
00:16:48,080 --> 00:16:50,880
reports so engineers could
better understand their models.
303
00:16:51,420 --> 00:16:53,850
Second is adding open
source model integration
304
00:16:53,850 --> 00:16:56,060
with any governance needed on that side.
305
00:16:56,800 --> 00:17:00,910
Third is lineage tracking so engineers
could better track their models from the
306
00:17:00,910 --> 00:17:03,480
experiment down to the model
version that is created.
307
00:17:04,340 --> 00:17:07,400
And then fourth is migrating
our serving stack to Kubernetes.
308
00:17:09,520 --> 00:17:11,280
And with that, that's all we had.
309
00:17:11,380 --> 00:17:13,340
So once again, thank you
for attending our session.
310
00:17:14,420 --> 00:17:16,940
I guess we'll open it up for any questions
or if you want to meet us afterwards
311
00:17:16,940 --> 00:17:19,040
to ask us anything, that also works.
312
00:17:21,420 --> 00:17:22,420
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
