# Physical AI in Action: Caterpillar & NVIDIA | CoreWeave Video

Source: https://www.coreweave.com/resources/videos/physical-ai-in-action-how-caterpillar-is-advancing-real-world-autonomy

Announcement

Webinar

Podcast

GTC 2026

CoreWeave Forge is here: connect your AI loop and compound every improvement. Read more

Contact us

Copied

Overview
Transcript

#### Physical AI in Action: From Simulation to Real-World Autonomy
What does it take to move physical AI beyond impressive demonstrations and into real-world production environments?
In this fireside chat, leaders from CoreWeave, Caterpillar, and NVIDIA explore how advances in robotics, world models, simulation, and AI infrastructure are accelerating the development of autonomous machines.
From mining operations to complex construction sites, physical AI is creating new opportunities for machines to perceive their surroundings, reason through unpredictable environments, and take action in the physical world.
The conversation examines how Caterpillar is building on decades of autonomous equipment experience, how NVIDIA is advancing the physical AI ecosystem, and why scalable AI infrastructure is essential for training and deploying increasingly sophisticated models.
In this discussion, you’ll learn:
- How physical AI is transforming autonomous construction and industrial equipment.
- Why synthetic data, simulation, and closing the sim-to-real gap are critical to developing physical AI.
- How world models and reasoning capabilities are accelerating robotics development.
- Why GPU compute, data infrastructure, and edge deployment are essential for scaling physical AI.
- What it takes to move autonomous systems from controlled demonstrations into safe, reliable real-world operations.
Watch the conversation to discover how physical AI is moving from research to real-world applications and what it takes to bring intelligent machines into production.

00:00

1
00:00:00,000 --> 00:00:07,460
Hello everyone, we
2
00:00:07,460 --> 00:00:08,160
managed to show you
3
00:00:08,160 --> 00:00:12,400
the video of the excavator truck needed
4
00:00:12,400 --> 00:00:15,000
to be but like a little bit of sort
of clear those are two separate machines.
5
00:00:15,000 --> 00:00:19,200
There's excavators and there's trucks.
We're getting into this. Yes. Thank you
6
00:00:19,200 --> 00:00:26,530
Brandon. You're welcome. Yes. So love
how full the room is. I think in general
7
00:00:26,530 --> 00:00:29,980
right like excavators are
to the engineering world.
8
00:00:29,980 --> 00:00:33,980
as cat videos are to the internet. They're
just amazing and everyone loves them
9
00:00:33,980 --> 00:00:39,190
the most. Appreciate that. Especially my
nephew. Let me quickly introduce who I've
10
00:00:39,190 --> 00:00:44,000
got here on the panel with me. Starting
with Amit Goel, who's the head of the
11
00:00:44,000 --> 00:00:49,180
Physical AI Ecosystem at NVIDIA.
He just told me he loves robots. And the
12
00:00:49,180 --> 00:00:56,060
bigger the robot, the more he loves them.
Absolutely. We get along just fine.
13
00:00:56,060 --> 00:00:59,960
Right? So next to me then is Brandon.
14
00:00:59,960 --> 00:01:05,960
who has the biggest robots. Your
mining trucks are some of the biggest
15
00:01:05,960 --> 00:01:11,640
machinery in the world. He's the VP for
physical AI platforms and construction
16
00:01:11,640 --> 00:01:16,870
autonomy at Caterpillar. He's been there
for 28 years? 27. 27 years. We'll see
17
00:01:16,870 --> 00:01:18,540
if I make it to 28. Okay.
18
00:01:20,540 --> 00:01:25,830
And in this time, I think his LinkedIn
profile was basically always one step
19
00:01:25,830 --> 00:01:30,050
ahead of the latest, greatest trend,
whether it was big data or digital
20
00:01:30,050 --> 00:01:35,820
transformation, machine learning,
internet of things, and now, of course,
21
00:01:35,820 --> 00:01:36,820
physical AI.
22
00:01:38,260 --> 00:01:43,460
Cool. All right. So today we want to talk
a little bit more about physical AI
23
00:01:43,460 --> 00:01:46,620
and from world models
to real in production
24
00:01:46,620 --> 00:01:49,760
use cases. You've probably all seen
25
00:01:49,760 --> 00:01:54,890
all of these funny videos of robot kung
fu that are trending. Hopefully you saw
26
00:01:54,890 --> 00:01:59,200
the robot coffee maker that we have
downstairs from the CoreWeave side.
27
00:01:59,260 --> 00:02:04,690
And today I want to talk with NVIDIA
and Caterpillar about where are we with
28
00:02:04,690 --> 00:02:08,260
actually sort of putting these
things into real world systems.
29
00:02:08,260 --> 00:02:14,790
Because Wes, there's cool demos out
there, but what can teams do today that
30
00:02:14,790 --> 00:02:18,260
simply wasn't possible so far?
And how did that get unlocked?
31
00:02:18,260 --> 00:02:25,230
Maybe Brandon, since I showed your truck
video. Yeah. Yeah. I shared a little
32
00:02:25,230 --> 00:02:27,320
bit of this during the keynote.
33
00:02:27,320 --> 00:02:30,590
Caterpillar leaned into
autonomy really, really
34
00:02:30,590 --> 00:02:37,380
early. And if you look at the work that
we've done on mine sites 15 years ago,
35
00:02:37,380 --> 00:02:41,260
we were working with customers to bring
autonomous operations to mining.
36
00:02:41,260 --> 00:02:45,330
It's always been our vision that we bring
that capability across the industries
37
00:02:45,330 --> 00:02:50,880
that we serve. The complexity on a
construction site is overwhelming when you
38
00:02:50,880 --> 00:02:56,260
think about it. And construction as
an industry is extremely diverse.
39
00:02:56,260 --> 00:03:01,390
It can be home construction. It can be
residential commercial construction. It
40
00:03:01,390 --> 00:03:08,460
can be building infrastructure,
power plants, data centers. It can be on
41
00:03:08,460 --> 00:03:11,260
highway construction,
metropolitan construction.
42
00:03:11,260 --> 00:03:16,110
So if you think about the dynamic nature
of the work that is done and the skill
43
00:03:16,110 --> 00:03:21,450
that it takes to operate in those
environments, taking deterministic systems
44
00:03:21,450 --> 00:03:26,260
that largely work on exception basis
and putting them into those types of
45
00:03:26,260 --> 00:03:29,260
environments is extremely challenging.
46
00:03:29,260 --> 00:03:33,570
So we've been keeping a very close eye on,
you know, from the very beginning of
47
00:03:33,570 --> 00:03:37,900
what's happened with large language
models getting introduced in the ChatGPT
48
00:03:37,900 --> 00:03:44,260
moment that everybody experienced four
or five years ago through the switch to
49
00:03:44,260 --> 00:03:48,880
agentic architectures and the models
actually have an agency to the point where
50
00:03:48,880 --> 00:03:51,260
now the models are able
to perceive the world around them.
51
00:03:51,260 --> 00:03:55,440
They're able to learn from those
environments. They're able to now invoke
52
00:03:55,440 --> 00:03:59,800
actions in the physical world. Doesn't
mean we abandon the technology that we've
53
00:03:59,800 --> 00:04:02,830
developed, but those two things start
to come together in a very, very
54
00:04:02,830 --> 00:04:04,260
meaningful way.
55
00:04:04,260 --> 00:04:07,650
So I mentioned during the keynote, you
know, a few years ago, this was always
56
00:04:07,650 --> 00:04:11,220
something that we wanted to do. We just
didn't know technically when it would
57
00:04:11,220 --> 00:04:15,260
be possible to do it. We're
really close, really close.
58
00:04:15,260 --> 00:04:22,060
Mm-hmm. So what actually changes when
a demo leaves the lab and gets into the
59
00:04:22,060 --> 00:04:25,260
messy environment of a construction site?
60
00:04:25,260 --> 00:04:29,710
I think the thing that we've all got
to ground ourselves in is there's the
61
00:04:29,710 --> 00:04:33,620
cognitive world of AI that we all live
in, of chatbots and agents doing things
62
00:04:33,620 --> 00:04:36,830
on your behalf, booking
travel, helping you
63
00:04:36,830 --> 00:04:38,260
with your shopping and things like that.
64
00:04:38,260 --> 00:04:45,720
When you get into the real world of what
our customers do, you're talking about
65
00:04:45,720 --> 00:04:50,260
heavy equipment working around
the clock doing very critical work.
66
00:04:50,260 --> 00:04:54,260
And if the technology doesn't work in
a way where it actually delivers value,
67
00:04:54,260 --> 00:04:58,260
it just becomes a cool demo that you
see a video of on YouTube and adoption
68
00:04:58,260 --> 00:05:01,260
actually, you know, flatlines.
69
00:05:01,260 --> 00:05:05,610
So that means that you've got to be
able to do the work efficiently. If you
70
00:05:05,610 --> 00:05:09,800
think about the amount of fuel that
these machines utilize, you've got to be
71
00:05:09,800 --> 00:05:13,260
able to do it as efficient as
possible, as effective as possible.
72
00:05:13,260 --> 00:05:15,160
And it has to fit into
the way the customers
73
00:05:15,160 --> 00:05:17,260
orchestrate and manage their job sites.
74
00:05:17,260 --> 00:05:20,740
So that's the most important piece and
really that motivates a lot of the work
75
00:05:20,740 --> 00:05:22,890
that we do. And that's
also why we're pulling
76
00:05:22,890 --> 00:05:25,730
customers in very early
to do co-development
77
00:05:25,730 --> 00:05:27,260
with us as we build the technology.
78
00:05:27,260 --> 00:05:31,500
Talking about co-development, Amit,
I'd like to sort of get you in here. From
79
00:05:31,500 --> 00:05:35,260
an NVIDIA perspective, what has
changed over the last couple of years?
80
00:05:35,260 --> 00:05:39,580
I think I've had the fortune or misfortune
81
00:05:39,580 --> 00:05:43,550
of seeing robotics for the last 10
82
00:05:43,550 --> 00:05:49,230
years. And robotics was fundamentally
a projects business. And that's why, as
83
00:05:49,230 --> 00:05:53,260
Brian was saying, every site is so
different, every job is so different.
84
00:05:53,260 --> 00:05:58,560
You really could not bring autonomy at
scale with the old way of doing things.
85
00:05:58,560 --> 00:06:04,830
Now, what changed in the last 18 months
is the capabilities of these large
86
00:06:04,830 --> 00:06:09,260
models, which were primarily grounded
language, now became multimodal.
87
00:06:09,260 --> 00:06:14,890
They understand the video. They had
an understanding of the semantics of the
88
00:06:14,890 --> 00:06:19,260
word. You could bring in LIDAR data.
You could bring in audio data.
89
00:06:19,260 --> 00:06:24,890
So when they became multimodal, now
you could think about using them and
90
00:06:24,890 --> 00:06:27,260
generalizing across domains.
91
00:06:27,260 --> 00:06:33,040
So that capabilities of the foundation
models that were grounded in videos and
92
00:06:33,040 --> 00:06:38,830
real world data, now made it possible
to extend and create models that can
93
00:06:38,830 --> 00:06:41,260
generalize across these different domains.
94
00:06:41,260 --> 00:06:47,260
If you go solve a problem for construction
of a residential, all the learnings
95
00:06:47,260 --> 00:06:49,260
from there, all the data that you collect,
96
00:06:49,260 --> 00:06:52,210
also helps the construction
work that you're
97
00:06:52,210 --> 00:06:55,260
doing probably for an industrial complex.
98
00:06:55,260 --> 00:07:01,260
So this compounding effect with the model
becoming multimodal was important.
99
00:07:01,260 --> 00:07:06,260
The second thing that happened
was simulation became good.
100
00:07:06,260 --> 00:07:12,890
And it's a combination of simulation that
is physics-based simulation, but also
101
00:07:12,890 --> 00:07:17,830
learned simulation, which people say
is world model, where you take in real
102
00:07:17,830 --> 00:07:21,530
world data and train a model to understand
the dynamics, the spatial, the
103
00:07:21,530 --> 00:07:25,260
temporal aspects of the universe
and bring it into a model.
104
00:07:25,260 --> 00:07:29,640
So now with that model, you cannot
just create the data, you can actually
105
00:07:29,640 --> 00:07:33,260
reason about the world,
you can validate your models.
106
00:07:33,260 --> 00:07:38,890
And the third thing was just the compute
capability that is needed to realize
107
00:07:38,890 --> 00:07:41,260
something like this
came into being, right?
108
00:07:41,260 --> 00:07:45,580
So whether it's the compute needed
to actually train the models with this
109
00:07:45,580 --> 00:07:50,760
enormous physical world data that you
collect to simulate the world in high
110
00:07:50,760 --> 00:07:53,260
fidelity or to actually
deploy it onto the edge.
111
00:07:53,260 --> 00:07:59,110
Because physical AI cannot happen
without having computing on the device as
112
00:07:59,110 --> 00:08:02,260
well to do the real-time computation.
113
00:08:02,260 --> 00:08:05,870
So I think the amalgamation of all these
three things coming together is what
114
00:08:05,870 --> 00:08:11,260
really made it possible to build
models that can generalize the scale.
115
00:08:11,260 --> 00:08:16,170
So everyone's super fascinated about what
comes out the other side of the model,
116
00:08:16,170 --> 00:08:20,760
but the amount of effort to get
to a model that has the right graph and
117
00:08:20,760 --> 00:08:22,260
understanding and context.
118
00:08:22,260 --> 00:08:27,890
The amount of work to get there, like
before, was almost like prohibitive to
119
00:08:27,890 --> 00:08:30,260
even undertaking it, right?
120
00:08:30,260 --> 00:08:32,260
So you think about what we have to do.
121
00:08:32,260 --> 00:08:34,590
And we're working very closely with NVIDIA
122
00:08:34,590 --> 00:08:37,260
on adapting their models
to our environment.
123
00:08:37,260 --> 00:08:39,260
But these models don't
understand our machines.
124
00:08:39,260 --> 00:08:40,260
They don't understand job sites.
125
00:08:40,260 --> 00:08:43,260
Think about all those job
sites that I described to you.
126
00:08:43,260 --> 00:08:45,260
Think about the different
permutations of those.
127
00:08:45,260 --> 00:08:47,630
Think about working with other autonomous
128
00:08:47,630 --> 00:08:50,260
machines or manned
machines on the job site.
129
00:08:50,260 --> 00:08:53,260
Think about all of those
scenarios that you have to go do.
130
00:08:53,260 --> 00:08:56,260
Now think about you've got
to go collect all of that data.
131
00:08:56,260 --> 00:08:57,260
Okay, I've collected it.
132
00:08:57,260 --> 00:08:59,260
Now I actually have to put
context on that data.
133
00:08:59,260 --> 00:09:00,260
What's that mean?
134
00:09:00,260 --> 00:09:02,260
That means I have to go
annotate and label the data.
135
00:09:02,260 --> 00:09:03,260
Before, what'd that mean?
136
00:09:03,260 --> 00:09:06,260
Well, I go hire a bunch of people that
actually understood what the data meant,
137
00:09:06,260 --> 00:09:09,260
and they watched the data, and then
they would annotate it and label it.
138
00:09:09,260 --> 00:09:14,490
We actually now have NeMo skills that
we utilize from NVIDIA that help us with
139
00:09:14,490 --> 00:09:16,260
that annotation and labeling
of that data coming in.
140
00:09:16,260 --> 00:09:20,580
So just like the, and it isn't the
glamorous part of this, but the building
141
00:09:20,580 --> 00:09:23,260
blocks of this being feasible now,
142
00:09:23,260 --> 00:09:25,690
just the whole AI chain
around how these things
143
00:09:25,690 --> 00:09:28,260
get developed have
completely busted loose.
144
00:09:28,260 --> 00:09:32,790
I think it might be really nice for
the audience if you paint us a little bit
145
00:09:32,790 --> 00:09:38,260
of a closer picture, like one use case,
whether it's an excavator or a truck,
146
00:09:38,260 --> 00:09:41,260
where you basically put
together what this looks like.
147
00:09:41,260 --> 00:09:42,260
What is the use case?
148
00:09:42,260 --> 00:09:43,260
What is it doing?
149
00:09:43,260 --> 00:09:44,260
What data goes in?
150
00:09:44,260 --> 00:09:45,260
What action comes out?
151
00:09:45,260 --> 00:09:49,230
Well, if you think about it, and for us
it really starts with have to have the
152
00:09:49,230 --> 00:09:51,260
understanding of the job site.
153
00:09:51,260 --> 00:09:56,260
So the very first thing we're undertaking,
it becomes immutable in robotics.
154
00:09:56,260 --> 00:10:01,890
Anybody that wants to do any level
of perception-based robotics and AI-based
155
00:10:01,890 --> 00:10:04,260
robotics, reasoning-based robotics,
156
00:10:04,260 --> 00:10:08,260
it starts with you have to have real
world data to be able to train on.
157
00:10:08,260 --> 00:10:09,260
So for us, that becomes massive.
158
00:10:09,260 --> 00:10:13,330
That means we've got a fleet of machines
out there operating that you've got to
159
00:10:13,330 --> 00:10:14,260
be able to do data collection on.
160
00:10:14,260 --> 00:10:18,260
That means you've got
stereoscopic video data coming in.
161
00:10:18,260 --> 00:10:20,260
You've got LiDAR data coming in.
162
00:10:20,260 --> 00:10:25,260
You've got performance control subsystem
data coming in off the machine.
163
00:10:25,260 --> 00:10:27,260
By the way, all that's
got to be synchronized.
164
00:10:27,260 --> 00:10:28,740
The model needs
to understand what happened
165
00:10:28,740 --> 00:10:30,260
in the world, what
happened in the machine,
166
00:10:30,260 --> 00:10:35,260
and how the machine interacted
with the world around it.
167
00:10:35,260 --> 00:10:37,260
That really becomes
the first piece of this.
168
00:10:37,260 --> 00:10:41,340
And then after that, then the simulation
environment really comes into play in
169
00:10:41,340 --> 00:10:43,260
terms of what we have
to do with simulation.
170
00:10:43,260 --> 00:10:50,260
For us, in order to go do this, closing
the sim to real gap is an absolute must.
171
00:10:50,260 --> 00:10:55,510
There is no way we will go capture
enough data to be able to train models on
172
00:10:55,510 --> 00:10:57,260
all of the different permutations.
173
00:10:57,260 --> 00:10:59,150
So these scenarios that
you see of starting
174
00:10:59,150 --> 00:11:00,690
with a little bit of data and then
175
00:11:00,690 --> 00:11:03,260
turning it into a massive simulation
176
00:11:03,260 --> 00:11:06,260
and synthetic data generation
exercise, that's real.
177
00:11:06,260 --> 00:11:10,620
For every one hour of data that we
collect, we'll probably do 1,000 hours of
178
00:11:10,620 --> 00:11:12,260
synthetic simulated data,
179
00:11:12,260 --> 00:11:15,260
but you've got to have a good sim to real
180
00:11:15,260 --> 00:11:17,260
that's got to be closed
in order to do that.
181
00:11:17,260 --> 00:11:21,440
Then from there, I won't describe
the -- and we don't want to disclose the
182
00:11:21,440 --> 00:11:23,260
exact machines that we're working on
183
00:11:23,260 --> 00:11:27,260
or the specific workflows
that we're working on yet.
184
00:11:27,260 --> 00:11:29,260
We'll talk about those soon.
185
00:11:29,260 --> 00:11:34,890
But what I will tell you is we have
pulled customers in to really help us
186
00:11:34,890 --> 00:11:37,260
understand where the constraints
187
00:11:37,260 --> 00:11:40,260
and where the most value can be
delivered on construction sites,
188
00:11:40,260 --> 00:11:43,010
and we're working very closely with
them to bring the technology to the
189
00:11:43,010 --> 00:11:45,260
machines and the workflows,
190
00:11:45,260 --> 00:11:47,260
the power of their business.
191
00:11:47,260 --> 00:11:48,260
Okay, cool.
192
00:11:48,260 --> 00:11:54,260
Adding to what Brandon was saying that
the sim to real and why Caterpillar is
193
00:11:54,260 --> 00:11:56,260
making such good progress
194
00:11:56,260 --> 00:12:01,890
is because the environment that you're
operating is so complicated that you
195
00:12:01,890 --> 00:12:06,260
cannot by nature have a very high
fidelity simulation model of it.
196
00:12:06,260 --> 00:12:11,890
But guess what? We can cheat now.
We can get real-world data and make a
197
00:12:11,890 --> 00:12:13,260
simulator learn it.
198
00:12:13,260 --> 00:12:17,870
And with the data that they have access
to, they're actually able to bring the
199
00:12:17,870 --> 00:12:19,260
data back into the simulator
200
00:12:19,260 --> 00:12:23,260
and train these world models that
can now have very good fidelity.
201
00:12:23,260 --> 00:12:26,140
So I think the physical AI journey
202
00:12:26,140 --> 00:12:29,410
requires this flywheel
where you start with
203
00:12:29,410 --> 00:12:32,260
simulation, you go to the real world,
204
00:12:32,260 --> 00:12:37,260
you get the data back, refine your
models and improve the capabilities.
205
00:12:37,260 --> 00:12:42,890
And that is, again, as Brandon was saying,
the tools, the libraries, the models
206
00:12:42,890 --> 00:12:47,260
are just now available to bring
this data flywheel into action.
207
00:12:47,260 --> 00:12:51,000
You know, the other thing that we've
learned too, Richard, if you'll allow me
208
00:12:51,000 --> 00:12:53,260
just to build on that a bit.
209
00:12:53,260 --> 00:12:56,880
You look at these construction sites
and I would encourage, I mean, obviously,
210
00:12:56,880 --> 00:12:58,260
25 years of Caterpillar Plus,
211
00:12:58,260 --> 00:12:59,070
I mean, every time I drive it by a
212
00:12:59,070 --> 00:13:00,460
construction site,
it draws my attention, so
213
00:13:00,460 --> 00:13:02,260
I have to look at it.
214
00:13:02,260 --> 00:13:06,400
But if you look at what happens on
a job site is like an orchestra of
215
00:13:06,400 --> 00:13:09,260
instruments going off
all in the right order.
216
00:13:09,260 --> 00:13:15,260
So bringing this technology to a job
site isn't just about having one machine
217
00:13:15,260 --> 00:13:19,260
or one class of machine that
has autonomous operations on it.
218
00:13:19,260 --> 00:13:24,890
It is about orchestrating all of those
machines together with complementary
219
00:13:24,890 --> 00:13:26,260
technologies.
220
00:13:26,260 --> 00:13:28,260
You know, we're doing
autonomy in addition.
221
00:13:28,260 --> 00:13:32,260
We've also got an amazing remote
control teleoperations solution.
222
00:13:32,260 --> 00:13:35,260
We've got an amazing fleet management
application called VisionLink.
223
00:13:35,260 --> 00:13:39,250
So if you think about all of these things
that come together around a job site,
224
00:13:39,250 --> 00:13:44,260
those are the things that we think will
help customers move the industry forward.
225
00:13:44,260 --> 00:13:48,560
And things that will differentiate
Caterpillar as we start to work with
226
00:13:48,560 --> 00:13:51,260
customers on this advanced technology.
227
00:13:51,260 --> 00:13:58,090
Nice. Amit, do you maybe have a lesson
learned from a real physical AI
228
00:13:58,090 --> 00:14:03,460
deployment where you changed the
simulation environment based on what you
229
00:14:03,460 --> 00:14:05,260
actually saw happened in the real world?
230
00:14:05,260 --> 00:14:08,260
And so how did you close
that sim-to-real gap?
231
00:14:08,260 --> 00:14:15,260
Yeah, I think the sim-to-real gap
is an important thing to solve.
232
00:14:15,260 --> 00:14:22,260
As Brand said, there is no other way we
can build, test or deploy physical AI.
233
00:14:22,260 --> 00:14:25,260
We absolutely have to rely on simulation.
234
00:14:25,260 --> 00:14:32,260
And over the years we have been solving
this problem from many different angles.
235
00:14:32,260 --> 00:14:38,260
We continue to make our traditional
physics based solvers better.
236
00:14:38,260 --> 00:14:45,010
We started off with using physics, which
is great for rigid body, really large
237
00:14:45,010 --> 00:14:46,260
environments.
238
00:14:46,260 --> 00:14:51,260
And it was great if you had
to just go navigate, right?
239
00:14:51,260 --> 00:14:56,050
If you don't have to come in contact
with anything in the world, you know, you
240
00:14:56,050 --> 00:15:00,260
can have a pretty recent simulation
today and go learn from there.
241
00:15:00,260 --> 00:15:06,120
However, the work that Caterpillar is
doing or the journalist robots are doing
242
00:15:06,120 --> 00:15:10,260
where you are in contact with
the objects, now things change.
243
00:15:10,260 --> 00:15:14,260
The physics before contact,
after contact looks very different.
244
00:15:14,260 --> 00:15:16,450
Now the world, the material, the physics
245
00:15:16,450 --> 00:15:19,260
properties of the world
become really important.
246
00:15:19,260 --> 00:15:22,260
How does the sand behave? How does
the particular concrete behave?
247
00:15:22,260 --> 00:15:25,260
All of those things
become really important.
248
00:15:25,260 --> 00:15:30,260
So we are, we continue to evolve
the core physics capabilities.
249
00:15:30,260 --> 00:15:34,860
We are building Newton, which is a solver
that is, that can combine different
250
00:15:34,860 --> 00:15:36,260
physics engines.
251
00:15:36,260 --> 00:15:37,260
So you can use physics for something.
252
00:15:37,260 --> 00:15:40,260
You can use MuJoCo Warp for another thing.
253
00:15:40,260 --> 00:15:44,670
You can use our core capabilities that
you're developing with this need for
254
00:15:44,670 --> 00:15:46,260
some of the hard things.
255
00:15:46,260 --> 00:15:52,230
So all of these things come together
to actually solve a very complex physics
256
00:15:52,230 --> 00:15:53,260
problem.
257
00:15:53,260 --> 00:15:56,260
But as I was saying earlier,
that's not enough.
258
00:15:56,260 --> 00:16:00,540
We have to complement this with the real
259
00:16:00,540 --> 00:16:04,260
to sim flywheel where you can get to,
260
00:16:04,260 --> 00:16:09,570
you can have a good model that has
a general understanding that has been
261
00:16:09,570 --> 00:16:12,260
trained with this physics that is modeled.
262
00:16:12,260 --> 00:16:19,720
But when you go back to the field and do
your deployments and your trials, you
263
00:16:19,720 --> 00:16:23,260
bring back the data from
there back into simulator.
264
00:16:23,260 --> 00:16:26,260
And this is where Cosmos comes in, right?
265
00:16:26,260 --> 00:16:29,260
You can take videos that has been
collected all around the world.
266
00:16:29,260 --> 00:16:33,360
You can take the data that's coming from
your particular machine and now train
267
00:16:33,360 --> 00:16:37,260
a model that is grounded
on real world data.
268
00:16:37,260 --> 00:16:41,850
So combining this traditional physics
models with what we like to call as
269
00:16:41,850 --> 00:16:47,480
neural physics or learned physics,
we are able to really close the gap,
270
00:16:47,480 --> 00:16:52,260
enabling both data generation,
data augmentation, policy evaluation.
271
00:16:52,260 --> 00:16:56,670
And one day these models could be smart
enough that they understand the world
272
00:16:56,670 --> 00:16:59,260
and they could become the policy itself.
273
00:16:59,260 --> 00:17:04,700
And that would be my feedback too is
up to probably this time last year,
274
00:17:04,700 --> 00:17:06,260
somebody mentioned digital twins to me.
275
00:17:06,260 --> 00:17:11,050
I probably tried to exit the conversation
as quickly as I could because the
276
00:17:11,050 --> 00:17:15,760
digital twin was useful up until the point
where like you actually put it into
277
00:17:15,760 --> 00:17:19,260
production and then you found out that
the whole world around it had changed
278
00:17:19,260 --> 00:17:20,260
and it was no longer useful.
279
00:17:20,260 --> 00:17:23,560
And I think what NVIDIA has built
with this closed loop system now with
280
00:17:23,560 --> 00:17:27,720
continued reinforcement of real world
data coming in has actually turned
281
00:17:27,720 --> 00:17:33,990
simulation into something immensely
useful and absolutely critical in robotics
282
00:17:33,990 --> 00:17:35,260
development.
283
00:17:35,260 --> 00:17:41,790
So I've worked in simulations and physical
test data for almost 10 years and in
284
00:17:41,790 --> 00:17:46,950
my experience has always
been if it's rigid physics
285
00:17:46,950 --> 00:17:50,260
and solid then you can
let the simulation run.
286
00:17:50,260 --> 00:17:52,260
If it's not rigid you won't have fun.
287
00:17:52,260 --> 00:17:56,870
I think that in the last four weeks
288
00:17:56,870 --> 00:18:02,610
itself, if you look at
what GPT-6 Astra can
289
00:18:02,610 --> 00:18:08,260
do, if you give it a problem,
it can combine these capabilities.
290
00:18:08,260 --> 00:18:12,020
You'll say, you know, it can bring a rigid
body solver from here, it can bring
291
00:18:12,020 --> 00:18:17,760
a fluid dynamic solver from here, it
can bring a contact modeling solver from
292
00:18:17,760 --> 00:18:19,260
another place and stitch it all together.
293
00:18:19,260 --> 00:18:24,260
And really just extend the capabilities.
294
00:18:24,260 --> 00:18:29,260
The industry has been building these
capabilities in bits and pieces.
295
00:18:29,260 --> 00:18:31,260
The hard part was integrating it together.
296
00:18:31,260 --> 00:18:35,730
But now with the solver, with the frontier
models, we can actually combine them
297
00:18:35,730 --> 00:18:42,310
together to create really, really fast
and accurate representation and combine
298
00:18:42,310 --> 00:18:44,260
that with bringing the real world data in.
299
00:18:44,260 --> 00:18:47,530
I think we'll see a huge acceleration in
300
00:18:47,530 --> 00:18:51,260
generating the data
and training the models.
301
00:18:51,260 --> 00:18:55,550
Right. So now that we've got data
and we know that the frontier models are
302
00:18:55,550 --> 00:18:57,580
actually, you know,
enabling a lot of people
303
00:18:57,580 --> 00:18:59,260
to quickly get going
with complex robotics.
304
00:18:59,260 --> 00:19:04,110
Right. Like what used to take six months
can now be accomplished by I literally
305
00:19:04,110 --> 00:19:08,760
just saw it in San Francisco last week
where I visited like three students at a
306
00:19:08,760 --> 00:19:10,920
Stanford dorm who managed
to train a robot arm
307
00:19:10,920 --> 00:19:13,260
over the weekend to sort
of tidy their desk.
308
00:19:13,260 --> 00:19:17,260
Epic to think that, you know, that
should have been possible six months ago.
309
00:19:17,260 --> 00:19:18,260
It's absolutely mind blowing.
310
00:19:18,260 --> 00:19:22,600
I think the main bottleneck then if
you can provide the data because you're
311
00:19:22,600 --> 00:19:25,880
sitting on a century of data,
a Caterpillar and you can figure out the
312
00:19:25,880 --> 00:19:29,260
simulation loop and the sim to real
gap, I think it becomes compute.
313
00:19:29,260 --> 00:19:33,250
And so I'd love to sort of hear a little
bit from you, right? Like how is
314
00:19:33,250 --> 00:19:39,110
physical AI different to run and train
when you're just thinking about data
315
00:19:39,110 --> 00:19:41,260
center infrastructure?
316
00:19:41,260 --> 00:19:45,260
Well, there's there's the combination, I
would say, of data center infrastructure.
317
00:19:45,260 --> 00:19:49,130
But then also if you think about the world
that we operate in, a lot of these
318
00:19:49,130 --> 00:19:52,260
models that we have
to run happen at the edge.
319
00:19:52,260 --> 00:19:56,260
So it's the combination
of those two working together.
320
00:19:59,260 --> 00:20:02,730
You look at the Caterpillar portfolio
of machines that we've got, you look at
321
00:20:02,730 --> 00:20:04,260
the diversity of application.
322
00:20:04,260 --> 00:20:09,890
I walked you through just a little bit
of what we're dealing with in real world
323
00:20:09,890 --> 00:20:11,260
data collection.
324
00:20:11,260 --> 00:20:15,790
Multiply that by the somewhere between
100 to 1 to 1,000 to 1 ratio of
325
00:20:15,790 --> 00:20:17,260
synthetic data generation.
326
00:20:17,260 --> 00:20:20,260
Then take a existing model.
327
00:20:20,260 --> 00:20:26,100
Let's just say Alpamayo is an example
and say now I need to go do a training
328
00:20:26,100 --> 00:20:29,670
run on that model to go,
you know, essentially
329
00:20:29,670 --> 00:20:31,260
start to teach it what
a job site looks like.
330
00:20:31,260 --> 00:20:35,260
Instead of running a car out,
run controls on a machine.
331
00:20:35,260 --> 00:20:40,190
That is not a inconsequential amount
of compute that is required to go do all
332
00:20:40,190 --> 00:20:41,260
of those things.
333
00:20:41,260 --> 00:20:44,260
And by the way, to get just to get
to the training run is one piece of it.
334
00:20:44,260 --> 00:20:48,260
You've got data preparation,
management storage, all all through that.
335
00:20:48,260 --> 00:20:52,260
So the kind of the scale
of AI in the physical world.
336
00:20:52,260 --> 00:20:56,760
It is, it's a different scale, but the
337
00:20:56,760 --> 00:21:00,950
problem I would say is real enough that
338
00:21:00,950 --> 00:21:05,260
it isn't just a handful of GPUs
that go solve the problem for you.
339
00:21:05,260 --> 00:21:11,260
And what we've also found too is that
whole chain of developing physical AI.
340
00:21:11,260 --> 00:21:18,260
Like there's obviously big hardware
constraints right now in the market.
341
00:21:18,260 --> 00:21:19,260
Sorry.
342
00:21:19,260 --> 00:21:22,260
I know you're doing your
part and you guys are too.
343
00:21:22,260 --> 00:21:29,260
But once you get the GPUs,
that's just the start of the game.
344
00:21:29,260 --> 00:21:34,510
The tooling and some of what we saw
from CoreWeave today around just how do
345
00:21:34,510 --> 00:21:38,770
you instantiate this to be able to
optimize what that whole tool chain looks
346
00:21:38,770 --> 00:21:42,260
like and the loop looks like to be
able to iterate and move quickly.
347
00:21:42,260 --> 00:21:47,060
I would say is probably equally as hard
as just the provisioning of getting,
348
00:21:47,060 --> 00:21:49,260
finding GPUs and getting GPUs.
349
00:21:49,260 --> 00:21:53,760
So that's one of the things that we've
learned is don't underestimate the, just
350
00:21:53,760 --> 00:21:59,790
the harnesses and the tooling and the
infrastructure that goes around the core
351
00:21:59,790 --> 00:22:01,260
infrastructure itself.
352
00:22:01,260 --> 00:22:05,790
And how is this loop different to I
think the normal loop of training in LLM
353
00:22:05,790 --> 00:22:08,260
that people might have seen before?
354
00:22:08,260 --> 00:22:15,720
I think as Brandon was saying, right,
the amount of new data that comes in from
355
00:22:15,720 --> 00:22:21,260
probably a single machine is
so much and it's multimodal.
356
00:22:21,260 --> 00:22:27,090
It has to be synchronized and you need
to, so just bring that data in whether
357
00:22:27,090 --> 00:22:30,720
it's six or eight
different cameras, whether
358
00:22:30,720 --> 00:22:33,260
it's LIDARs, all the controls information.
359
00:22:33,260 --> 00:22:37,260
Annotating this data, the text
data is self-annotated, right?
360
00:22:37,260 --> 00:22:43,260
So you need to, because we are training
these VLM models or world action models,
361
00:22:43,260 --> 00:22:46,260
all of the data that's
coming in is not annotated.
362
00:22:46,260 --> 00:22:51,480
There's a huge processing pipeline that
goes in before it can be tokenized in a
363
00:22:51,480 --> 00:22:54,260
way that now you can train your model.
364
00:22:54,260 --> 00:23:00,260
So you have to spend a lot
of compute to process this data.
365
00:23:00,260 --> 00:23:05,620
The volume of data is orders of magnitude
more than what you would see in an LLM
366
00:23:05,620 --> 00:23:07,260
because it's just inherently multimodal.
367
00:23:07,260 --> 00:23:10,260
It's running 24/7, creating
data all the time, right?
368
00:23:10,260 --> 00:23:14,260
So the data velocity and volume is huge.
369
00:23:14,260 --> 00:23:18,670
That impacts what kind of infrastructure
you need for training and curation and
370
00:23:18,670 --> 00:23:20,260
processing of this data.
371
00:23:20,260 --> 00:23:25,890
But then, once you've trained the model,
you're constantly, as Brandon was
372
00:23:25,890 --> 00:23:29,260
saying, you have to be augmenting
this data all the time.
373
00:23:29,260 --> 00:23:36,260
Because even though this data velocity
is there, the diversity is not there.
374
00:23:36,260 --> 00:23:40,730
You're still operating in one environment,
probably in a given weather
375
00:23:40,730 --> 00:23:43,260
condition, in a given environment.
376
00:23:43,260 --> 00:23:48,410
You don't have the luxury to wait for
five years to experience all the seasons
377
00:23:48,410 --> 00:23:50,260
and all the environments
to collect the data.
378
00:23:50,260 --> 00:23:55,890
So you want to maximize the value of this
data by augmenting it with all the AI
379
00:23:55,890 --> 00:23:58,260
capabilities that are available.
380
00:23:58,260 --> 00:24:02,520
So you need another set of infrastructure
that is going to take this data and
381
00:24:02,520 --> 00:24:07,260
augment it and add more variations of it.
382
00:24:07,260 --> 00:24:12,260
Then you go into your training
loop, followed by evaluations.
383
00:24:12,260 --> 00:24:14,260
So evals are super important.
384
00:24:14,260 --> 00:24:19,890
You cannot just throw these models out
over to, you know, for people to give
385
00:24:19,890 --> 00:24:23,260
thumbs up and thumbs down
and learn from human feedback.
386
00:24:23,260 --> 00:24:25,260
That's not an option.
387
00:24:25,260 --> 00:24:29,250
You need to have a very
good infrastructure
388
00:24:29,250 --> 00:24:32,710
that's scalable where you can do
389
00:24:32,710 --> 00:24:35,260
these evals at scale and autonomously.
390
00:24:35,260 --> 00:24:40,100
It's an extremely hard problem and that
requires another scale of computer
391
00:24:40,100 --> 00:24:41,260
infrastructure.
392
00:24:41,260 --> 00:24:45,790
And the training and evals have to be
talking to each other because once your
393
00:24:45,790 --> 00:24:48,260
eval tells you this model is not
working in this particular area,
394
00:24:48,260 --> 00:24:52,260
you have to go back and create more data
and go through another training loop.
395
00:24:52,260 --> 00:24:55,040
So the proximity
of the eval infrastructure,
396
00:24:55,040 --> 00:24:57,400
your training infrastructure close
397
00:24:57,400 --> 00:25:03,260
to each other, high throughput data
connection between them is important.
398
00:25:03,260 --> 00:25:06,260
And the last piece is deployment.
399
00:25:06,260 --> 00:25:11,260
You need to have edge computing
to deploy these models.
400
00:25:11,260 --> 00:25:14,260
And again, bring the data back from
the field back into your training.
401
00:25:14,260 --> 00:25:18,120
So doing this at scale in a production
402
00:25:18,120 --> 00:25:22,260
environment that is reliable is where,
403
00:25:22,260 --> 00:25:24,260
you know, partners like CoreWeave come in.
404
00:25:24,260 --> 00:25:28,260
Yeah. Thanks. I wasn't fishing for that.
405
00:25:28,260 --> 00:25:30,260
Good. I think we're almost
running out of time.
406
00:25:30,260 --> 00:25:32,260
And so maybe last one, right?
407
00:25:32,260 --> 00:25:34,220
I think we've sort of gone
really nicely through
408
00:25:34,220 --> 00:25:36,260
the development loop,
the physical AI loop, right?
409
00:25:36,260 --> 00:25:41,570
Like real-world simulation data,
data augmentation, the edge that makes
410
00:25:41,570 --> 00:25:44,260
physical AI so much different
from, you know, Gen AI.
411
00:25:44,260 --> 00:25:46,260
And so last question for the two of you.
412
00:25:46,260 --> 00:25:49,260
So what's it actually going
to take from here on now, right?
413
00:25:49,260 --> 00:25:54,260
Like you started on this incredible
journey with Caterpillar.
414
00:25:54,260 --> 00:26:00,040
What's it going to take to sort of get
things and fleets into the field working
415
00:26:00,040 --> 00:26:02,260
on an entirely new level?
416
00:26:02,260 --> 00:26:05,260
Do you want me to start?
417
00:26:05,260 --> 00:26:06,260
Of course.
418
00:26:06,260 --> 00:26:10,350
So I think one of the things that we've
learned as we've gone through this is
419
00:26:10,350 --> 00:26:12,790
this is much different
than any technology or
420
00:26:12,790 --> 00:26:14,260
machine development
that we've done before.
421
00:26:14,260 --> 00:26:19,580
And I think irrespective of whether it's
an automotive OEM or heavy equipment,
422
00:26:19,580 --> 00:26:22,260
whether they're in construction
or agriculture, really doesn't matter.
423
00:26:22,260 --> 00:26:25,530
Or you'd typically have a multi-year
new product introduction cycle and you
424
00:26:25,530 --> 00:26:28,790
would have technology that would come
to market at the same time your new
425
00:26:28,790 --> 00:26:32,260
machine model would come to market
or vehicle would come to market.
426
00:26:32,260 --> 00:26:34,260
That's all condensed and changed now.
427
00:26:34,260 --> 00:26:36,980
Our cycles have gone from what used to be
428
00:26:36,980 --> 00:26:40,260
years and now we're
measuring it in months.
429
00:26:40,260 --> 00:26:45,890
We've went from, you know, kind
of things being relatively stagnant and
430
00:26:45,890 --> 00:26:51,260
relatively contained to things now
being very iterative and capabilities.
431
00:26:51,260 --> 00:26:54,580
And that's part of what we're learning
about is how do you develop this
432
00:26:54,580 --> 00:26:59,200
technology in a very modular, iterative
way where you can get it into the
433
00:26:59,200 --> 00:27:03,260
market quickly and start
to learn with your customers.
434
00:27:03,260 --> 00:27:06,500
That's really where we're focused. So
the whole clock cycle of the way we build
435
00:27:06,500 --> 00:27:10,720
inside of Caterpillar has completely
changed with the dynamics of what's
436
00:27:10,720 --> 00:27:12,260
happening in the market now.
437
00:27:12,260 --> 00:27:15,260
We're excited by it. Our
customers are excited by it.
438
00:27:15,260 --> 00:27:19,430
Just a big change for a company that's
been around and has a rich heritage in
439
00:27:19,430 --> 00:27:21,260
iron and machine development.
440
00:27:21,260 --> 00:27:26,930
Now going to a cycle like this has been
very interesting, but also very, very
441
00:27:26,930 --> 00:27:28,260
fun to be a part of.
442
00:27:30,260 --> 00:27:35,890
I think Brandon covered most of the
things, but as a technology provider, as a
443
00:27:35,890 --> 00:27:39,260
platform on which these
capabilities are being built.
444
00:27:39,260 --> 00:27:43,750
We do understand that physical AI has
445
00:27:43,750 --> 00:27:46,850
this element of deploying, diffusing this
446
00:27:46,850 --> 00:27:51,960
technology into the physical world,
which requires extreme hardware software
447
00:27:51,960 --> 00:27:53,260
core design.
448
00:27:53,260 --> 00:27:56,670
And that's why we're excited to working
with Caterpillar on this because they
449
00:27:56,670 --> 00:28:00,520
are in a unique position to actually
do this hardware software co-design,
450
00:28:00,520 --> 00:28:03,260
which is essential to get the maximum
benefit of this technology.
451
00:28:03,260 --> 00:28:08,890
The other thing that we are also very
focused on and working on right now is
452
00:28:08,890 --> 00:28:12,260
making this technology
deployable in a safe way.
453
00:28:12,260 --> 00:28:17,620
So we're building all the tooling
and infrastructure that is needed to make
454
00:28:17,620 --> 00:28:20,070
sure when you're deploying AI in the real
455
00:28:20,070 --> 00:28:23,260
physical world, it can
be done in a safe way.
456
00:28:23,260 --> 00:28:27,600
So I think requiring that execution
discipline, having that operations
457
00:28:27,600 --> 00:28:32,260
experience to actually go deploy this
thing, not just keep building it in the
458
00:28:32,260 --> 00:28:33,260
lab, is going to be important.
459
00:28:33,260 --> 00:28:36,260
And then doing it in a safe way
is going to be important as well.
460
00:28:36,260 --> 00:28:37,260
Very good.
461
00:28:37,260 --> 00:28:41,580
I mean, I think we've seen in autonomous
vehicles, the long tail, all of the
462
00:28:41,580 --> 00:28:45,850
scenarios that you didn't have originally,
that is the reason why it just takes
463
00:28:45,850 --> 00:28:47,260
longer and is much harder.
464
00:28:47,260 --> 00:28:52,260
And that, you know, that is
why reasoning is so important.
465
00:28:52,260 --> 00:28:57,840
The ability that you can reason is the
only way that you can find your way out
466
00:28:57,840 --> 00:28:59,260
of the long tail.
467
00:28:59,260 --> 00:29:03,940
If everything has to be, you have
to have a data for everything, you should
468
00:29:03,940 --> 00:29:08,260
have the robot and the brain
should have seen everything before.
469
00:29:08,260 --> 00:29:11,260
That is, that's not possible
in the physical world.
470
00:29:11,260 --> 00:29:13,260
So you have to have the reasoning.
471
00:29:13,260 --> 00:29:16,260
And now the models are able to do reason.
472
00:29:16,260 --> 00:29:22,260
They are able to use agentic AI, multiple
tools together to come up with a solution.
473
00:29:22,260 --> 00:29:28,260
And that's how you get over the long tail
problem that's been plaguing physical AI.
474
00:29:29,260 --> 00:29:30,260
Very cool.
475
00:29:30,260 --> 00:29:31,260
Thank you very much.
476
00:29:31,260 --> 00:29:32,260
Thanks, guys.
477
00:29:32,260 --> 00:29:33,260
Thank you.
478
00:29:33,260 --> 00:29:34,260
Thank you for listening.
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
