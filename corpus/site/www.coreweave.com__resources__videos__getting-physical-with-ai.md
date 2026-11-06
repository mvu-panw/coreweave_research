# Getting Physical with AI | AI Cloud Essentials Ep 8

Source: https://www.coreweave.com/resources/videos/getting-physical-with-ai

Announcement

Webinar

Podcast

GTC 2026

CoreWeave Forge is here: connect your AI loop and compound every improvement. Read more

Contact us

Copied

Overview
Transcript

### Episode 8: AI Cloud Essentials Podcast
AI-powered engineering is transforming how organizations accelerate simulation, testing, and decision-making across automotive, manufacturing, robotics, and scientific AI. In this episode of AI Cloud Essentials, Richard Ahlfeld, SVP for Physical and Scientific AI at CoreWeave, joins host Ritu Jyoti to discuss how AI is helping teams move faster by combining simulation with real-world testing.
Learn how transformer models improve physical simulations, where AI is driving the most impact today, and what it takes to scale AI-powered engineering workflows in production.
In this session, you’ll learn:
- How AI accelerates engineering and simulation workflows
- Why combining simulation and real-world testing improves outcomes
- Key use cases across automotive, manufacturing, and robotics
- Practical lessons for scaling physical and scientific AI

### Podcast Guests:
Richard Ahlfeld, SVP for Physical and Scientific AI, CoreWeave

00:00

1
00:00:00,000 --> 00:00:05,279
And it came back with very perfect prediction within the design space, the data that we had. I
2
00:00:05,280 --> 00:00:11,040
was like, wow, that was quite easy. AI has made great progress over the last couple of years, not
3
00:00:11,040 --> 00:00:17,280
just in language models, but also in physical simulations, robotics, automotive and industrial
4
00:00:17,280 --> 00:00:23,240
manufacturing. It's only been really in the last, let's say, six months that I think this space has
5
00:00:23,240 --> 00:00:28,840
gotten really exciting. And you can create foundational physics models that predict
6
00:00:28,840 --> 00:00:34,640
simulation runs without having to do them. In this episode of AI Cloud Essentials, I sit down with
7
00:00:34,640 --> 00:00:40,600
Richard, who leads physical AI or VIF, and we talk about the rapidly evolving innovations in this
8
00:00:40,600 --> 00:00:47,479
field. Sometimes you have to get out of the AI space to make actual progress. Don't miss
9
00:00:47,480 --> 00:00:48,880
this conversation.
10
00:00:58,000 --> 00:01:03,960
Hello everyone! Welcome to season two of the AI Cloud Essentials, a podcast series brought to you
11
00:01:03,960 --> 00:01:10,200
by Corby. Today we are in episode two and I'm super excited because I'm joined by Richard and
12
00:01:10,200 --> 00:01:15,120
we are going to talk about how AI is breaking into the physical world out of the digital
13
00:01:15,160 --> 00:01:20,560
terminal, into the physical world. So welcome, Richard. Uh, let's kick things off with your
14
00:01:20,560 --> 00:01:26,839
journey in this area. How did you get into the physical simulation? What is so exciting about it?
15
00:01:26,880 --> 00:01:33,360
Would love to hear your perspective on it. Thanks. First of all, great to be here. I probably got into
16
00:01:33,360 --> 00:01:40,280
the whole AI for physics and physical systems long before ChatGPT, long before it was one of the
17
00:01:40,280 --> 00:01:45,480
biggest topics to talk about at the world's leading conferences. Some people might say, I've
18
00:01:45,480 --> 00:01:52,240
been too early. I think I just wasn't the right place half a decade too early. So I
19
00:01:52,600 --> 00:01:57,360
started a company right out of university. I was a PhD student at Imperial College in London
20
00:01:57,480 --> 00:02:03,880
Researching how to optimize aircraft engines with Rolls-Royce. I had a little stint at NASA where I
21
00:02:03,880 --> 00:02:09,560
worked on the Mars rocket trying to optimize that, and then did a research project, actually in
22
00:02:09,560 --> 00:02:15,800
Stanford, where I was supposed to model turbulence. And few people know turbulence is one of the most
23
00:02:15,800 --> 00:02:22,360
difficult problems in the world. It's almost impossible to solve, and I couldn't solve it
24
00:02:22,360 --> 00:02:28,800
either. Big surprise. And so I cheated. I used AI. This was in 2016. It was a big conference in
25
00:02:28,800 --> 00:02:33,400
Stanford. The world's smartest people were there. Nobody could figure out these equations. And I was
26
00:02:33,400 --> 00:02:38,640
like, you know what I'm going to do? I'm gonna take a little bit of data from some real wind tunnel.
27
00:02:38,640 --> 00:02:43,360
I'm going to fit a deep neural network on this, and I'm going to see what this predicts. And it
28
00:02:43,360 --> 00:02:48,839
came back with very perfect prediction within the design space, the data that we had. And I was like,
29
00:02:48,840 --> 00:02:53,960
wow, that was quite easy. Like this is one of the hardest problems in the world. And with a couple
30
00:02:53,960 --> 00:02:58,400
of lines of code and a little bit of training, I could suddenly solve it. When I say I. AI could
31
00:02:58,400 --> 00:03:04,120
suddenly solve it. And so that's I was hooked, I got in, I was like amazing. I'm gonna from now on
32
00:03:04,120 --> 00:03:10,880
work on AI for science and engineering. And so I did. Awesome. That was
33
00:03:10,920 --> 00:03:16,800
really your aha moment. Right. So that this is going to be something really transformative. So
34
00:03:16,840 --> 00:03:21,200
I've been reading a lot about some of your successes and proven wins and case specifics. It
35
00:03:21,200 --> 00:03:26,720
would be fantastic to hear, for example, if you could talk about some of the use cases where it
36
00:03:26,720 --> 00:03:32,320
really transformed the aha moment that you just talked about and how usage of those data and how
37
00:03:32,320 --> 00:03:38,439
those physical simulations really solving the problem. So I think it's fair to say that I've
38
00:03:38,480 --> 00:03:43,720
tried everything you can with AI in engineering, literally everything. Right. Like when you, I
39
00:03:43,720 --> 00:03:48,560
started a startup or my company with a main idea I want to do AI in science and AI in science is
40
00:03:48,560 --> 00:03:54,039
everything. Einsteins is aerospace engineering, rocket engineering. It's automotive, it's pharma,
41
00:03:54,039 --> 00:04:00,879
it's robotics. It's, um, trying to figure out new medical equipment. And over the last nine years,
42
00:04:00,880 --> 00:04:07,880
I've literally tried everything. And one of the first things that I was really excited
43
00:04:07,880 --> 00:04:13,039
by is the fact that physical simulations, the tools that large engineering companies use to
44
00:04:13,040 --> 00:04:18,159
avoid prototyping something and trying to understand just how they work in the virtual
45
00:04:18,160 --> 00:04:22,799
world before building something, tend to be very compute intensive, and then tend to take a very
46
00:04:22,800 --> 00:04:27,079
long time. Right at the beginning, we used dynamic graph neural networks and they were very
47
00:04:27,079 --> 00:04:33,359
impressive. You could very quickly impress a VP of engineering that he could run a simulation 10,000
48
00:04:33,399 --> 00:04:38,800
times faster than they could ever do it before. And it was impressive. But the problem was that
49
00:04:38,800 --> 00:04:45,239
the economics of training versus inference didn't quite work out. People needed to train
50
00:04:45,280 --> 00:04:52,239
1500 2000 simulations to essentially predict one simulation run, and then realize that
51
00:04:52,240 --> 00:04:58,279
that didn't quite work because they had changed the design too much out of the learning space, and
52
00:04:58,279 --> 00:05:02,719
so they couldn't actually predict it. So they'd run another 500 simulations. So long story short,
53
00:05:02,760 --> 00:05:08,319
we were just too early because models weren't quite intelligent enough yet to actually make
54
00:05:08,320 --> 00:05:13,959
predictions and save people design iterations. That all changed massively when Transformers were
55
00:05:13,959 --> 00:05:20,519
introduced, and suddenly you could actually train an AI model on ten, 15,
56
00:05:20,560 --> 00:05:26,519
20 fairly complex simulations with huge design spaces and get a prediction for a future design
57
00:05:26,519 --> 00:05:33,200
run that actually helped you make a decision and was, like, miraculously correct without having to
58
00:05:33,239 --> 00:05:39,079
rerun the simulation. And that only happened really recently. It's only been really in the last,
59
00:05:39,120 --> 00:05:44,760
let's say, six months, that I think this space has gotten really exciting. And you can create
60
00:05:44,800 --> 00:05:50,159
foundational physics models that predict simulation runs without having to do them. Yeah,
61
00:05:50,160 --> 00:05:55,359
that's fantastic to hear, Richard. And I think it also helps in kind of taking care of a lot of
62
00:05:55,359 --> 00:06:00,359
historical data, which in the past people couldn't have used it. Is that a fair statement? Because now
63
00:06:00,359 --> 00:06:04,479
when you're working with, you know, transformer models which can process, you know, not just, you
64
00:06:04,480 --> 00:06:09,959
know, multiple simulations, but a lot of, you know, historical data to kind of predict the future
65
00:06:09,959 --> 00:06:15,559
much more accurately. Is that a fair statement? I've always loved the idea of that. I've gone to
66
00:06:15,559 --> 00:06:20,920
all of the big engineering companies and I've asked them, hey, how many chassis simulations do
67
00:06:20,920 --> 00:06:26,279
you actually have? And they're like, oh yeah, I think we've run 150,000 of those in the last six
68
00:06:26,279 --> 00:06:31,920
months alone, and we probably have a million in storage. And then we tried to build AI models that
69
00:06:31,920 --> 00:06:36,679
actually learn from them. And then you very quickly realize how much of a problem data
70
00:06:36,880 --> 00:06:43,760
uniformity actually is, because, yes, they have 150,000 simulations, but 150 of those
71
00:06:43,760 --> 00:06:47,959
were designed by this person who had chose slightly different set up conditions, and they
72
00:06:47,959 --> 00:06:52,760
changed software vendor six months ago. And so that's a completely different silver. And
73
00:06:52,760 --> 00:06:58,319
comparing this is apple and oranges. And so I think in general that is the idea. But in reality,
74
00:06:58,359 --> 00:07:03,399
just like with every historic data problem, it's remarkably hard to go and sort through all of
75
00:07:03,399 --> 00:07:08,839
this data and actually bring it together. And so with the latest transformer models, I don't think
76
00:07:08,839 --> 00:07:14,240
that is that much of an issue anymore, because you can literally come up with an intelligent model
77
00:07:14,240 --> 00:07:20,439
from fairly few designs and simulations, and people have tried to come up with ways to bridge
78
00:07:20,440 --> 00:07:25,319
the gap. But yes, it's been. That's where the real value is. And it has historically been very, very
79
00:07:25,319 --> 00:07:30,680
hard to unify all of this. Yeah, that's a fantastic insight for our viewers today because, you know, we
80
00:07:30,720 --> 00:07:35,519
kind of assume that, you know, you have tons of data and you can make progress. So now let's pivot
81
00:07:35,520 --> 00:07:39,559
to a little bit more as to because there's a lot of excitement in the industry about where the
82
00:07:39,559 --> 00:07:44,159
future is headed. The potential that we are talking about is not just limited to the physical
83
00:07:44,160 --> 00:07:49,400
simulations, but a lot of other industries. So I would love to get your take on what are the other
84
00:07:49,400 --> 00:07:55,359
industries, where are we actually venturing and some of the hard happening items around physical
85
00:07:55,360 --> 00:08:01,799
robots? Uh, I would love to hear what you guys are up to. And what are you seeing in the industry? So
86
00:08:01,839 --> 00:08:06,200
monolith and I think we took a very different route to all of the other startups and even big
87
00:08:06,200 --> 00:08:11,040
engineering companies in this industry, because we were too early for the simulation space. We
88
00:08:11,040 --> 00:08:17,319
basically gave up on simulations and instead focused on testing, which very different idea. You
89
00:08:17,319 --> 00:08:23,320
basically say, hey, look, everyone, we've tried to simulate what happens with this chassis or in
90
00:08:23,320 --> 00:08:28,359
this crash test, it didn't work. The reality was more complex than any simulation that we can
91
00:08:28,359 --> 00:08:33,039
really run. So we're just going to go and have to test this anyway. And so we came up with this
92
00:08:33,039 --> 00:08:39,400
counterintuitive notion that simulations are good, but they will never be as good as the real
93
00:08:39,400 --> 00:08:45,679
world. And so instead of running simulations, why don't we directly include AI into the real world?
94
00:08:45,679 --> 00:08:52,479
Learn from real physical data, real physical prototypes. And this is where we actually started
95
00:08:52,480 --> 00:08:58,840
getting into robotics, because within robotics, one of the big topics out there is what people call
96
00:08:59,080 --> 00:09:05,799
um, the sim to real gap, where everyone is excited about how I can now run a million simulations of
97
00:09:05,799 --> 00:09:12,640
a robot on a cloud. But I've been arguing for a while, um, that this doesn't really help
98
00:09:12,640 --> 00:09:19,400
you if you ask a robot arm to essentially pick up a plastic bottle in virtual reality, this plastic
99
00:09:19,400 --> 00:09:25,560
bottle is solid. It's firm, it doesn't move. It's rigid because simulating how plastic crumbles
100
00:09:25,560 --> 00:09:30,520
when you touch it is remarkably hard and takes a huge amount of computational effort. That you
101
00:09:30,520 --> 00:09:35,840
could run in two seconds is impossible. And so instead of doing this in virtual reality,
102
00:09:35,879 --> 00:09:40,840
basically you could do it in the real physical world. You could set up a robot, put it into a lab,
103
00:09:40,840 --> 00:09:47,199
and just practice with a water bottle and just see what does it really do, like learning faster
104
00:09:47,200 --> 00:09:53,759
with fewer data points from real physical data is not the same thing as the physical
105
00:09:53,760 --> 00:09:57,799
simulation world, but as a different area of machine learning where you're literally trying
106
00:09:57,840 --> 00:10:04,319
within control systems to just see how do I very quickly learn in real time, in a feedback
107
00:10:04,320 --> 00:10:10,079
loop, in a real world environment? There's a couple of use cases that we've published as monoliths,
108
00:10:10,080 --> 00:10:14,399
where these things have actually yielded great results. There's a case study published with
109
00:10:14,400 --> 00:10:19,559
Nissan where we sort them, got them off the path of, hey, let's try and simulate everything and just
110
00:10:19,559 --> 00:10:24,999
say, look, guys, like in physical testing, there are very simple components in your systems, just like
111
00:10:24,999 --> 00:10:30,479
simple bolts, right? Like you bolt together two metal components should be trivial, but turns out
112
00:10:30,479 --> 00:10:35,639
is surprisingly hard. But somewhere out there is specialists who spend 90 years trying to figure
113
00:10:35,640 --> 00:10:40,880
out how to attach two metal plates with a bolt. And there's a lot of knowledge in this. There's a
114
00:10:40,880 --> 00:10:45,719
lot of hardware testing in this. I mean, okay, why don't we just take all of this hardware data, put
115
00:10:45,719 --> 00:10:51,118
it into a machine learning algorithm and have it learn. If I'm going to go and build this, what's
116
00:10:51,119 --> 00:10:55,680
your recommendation? What's going to happen in the real world? No simulations, just learning from real,
117
00:10:55,719 --> 00:11:00,400
real world experience. And it turned out that worked really well. Like once Nissan started
118
00:11:00,400 --> 00:11:05,879
rolling this out for physical tests, they could reduce testing across all of their chassis by
119
00:11:05,920 --> 00:11:11,478
like 17%, which doesn't sound like a lot. But a lot of these tests are very critical for safety, so
120
00:11:11,520 --> 00:11:17,560
they couldn't be omitted. Awesome. Awesome. So as we are kind of expanding into the other industries
121
00:11:17,560 --> 00:11:22,479
and looking into, could you give us some perspective on what other industry segments are
122
00:11:22,479 --> 00:11:28,199
you kind of expanding into or looking into? Uh, you know, there's a lot of buzz in the industry about
123
00:11:28,199 --> 00:11:34,919
collaborative robots or humanoid robots. Are you looking into those areas as well? So for me, within
124
00:11:34,919 --> 00:11:41,799
physical AI, the biggest areas are, number one, automotive autonomous cars
125
00:11:41,840 --> 00:11:48,760
have made a huge leap in the last three months alone, in particular through releases like Nvidia
126
00:11:48,800 --> 00:11:53,959
Alpa Mayo, where your car cannot argue with you and say, no, I'm not going to go and turn left
127
00:11:53,960 --> 00:12:00,639
because there's a cyclist on the road there and it stops being the it stops. It's not that these
128
00:12:00,679 --> 00:12:05,120
AI models were black boxes. It's like, well, I don't trust my autonomous car because it's a black box.
129
00:12:05,120 --> 00:12:10,119
I don't know what it does. I don't trust it. They cannot argue back and explain in words why
130
00:12:10,119 --> 00:12:15,999
they've tried to do it in a specific way, and even involve you in the process. So that and the fact
131
00:12:16,000 --> 00:12:21,559
that the enormous amount of compute that is now available, thanks to the AI boom, they can train
132
00:12:21,560 --> 00:12:27,119
autonomous cars in a completely different way. So automotive autonomous cars, I think, are the number
133
00:12:27,119 --> 00:12:33,119
one area for me where I'm expecting big jumps. The second area that I think is really huge is
134
00:12:33,120 --> 00:12:39,479
manufacturing. Like I keep saying, like when Jensen Huang goes on stage and says it's going to be a
135
00:12:39,479 --> 00:12:46,199
$50 trillion industry by 2050 physical AI. I keep joking that out of that $50 trillion,
136
00:12:46,240 --> 00:12:53,159
probably 49 trillion is in good old fact, good old fashioned manufacturing.
137
00:12:53,600 --> 00:12:58,679
Like, how do I create a Starbucks cup? Like somebody needs to manufacture that. Somebody needs
138
00:12:58,680 --> 00:13:02,799
to check that the quality of this cup is actually all right. Right. Like there shouldn't be a leak in
139
00:13:02,799 --> 00:13:07,679
that ideally. And you should be able to close the lid on it. That's a lot of manufacturing quality
140
00:13:07,680 --> 00:13:12,479
control. That is a lot of robots and cameras trying to figure out does this actually work?
141
00:13:12,559 --> 00:13:17,439
Nobody wants to look at a Starbucks cups every morning to see whether it's perfect. And so that
142
00:13:17,440 --> 00:13:23,039
is I think, the biggest use case out there. Yeah, I'm mentioning these two first because I think
143
00:13:23,040 --> 00:13:28,279
these are the real big ones. Um, humanoid robots. I know they get the most attention in the media
144
00:13:28,320 --> 00:13:34,999
because like a dancing robot is always fun to watch. But that said, there's just
145
00:13:35,000 --> 00:13:41,839
still a lot of technical challenges that we have to overcome in humanoid robots. It's true that if
146
00:13:41,840 --> 00:13:47,559
you put ChatGPT into a robot, there's this moment where you amaze. Because suddenly this thing can
147
00:13:47,559 --> 00:13:54,159
see. It can talk to you, it can reason and argue back. But the problem is, it still does these
148
00:13:54,159 --> 00:13:59,319
things fairly slowly. There's a little bit of a lag here, right? And it still needs to learn a lot
149
00:13:59,320 --> 00:14:05,799
of different things. And it can very quickly be out of scope when you realize are actually this
150
00:14:05,799 --> 00:14:10,519
is a fantastic robot. And it's learn how to cook, but it doesn't work in my kitchen. I've heard that
151
00:14:10,520 --> 00:14:15,599
right. Like there's problems with renting Airbnbs in California these days because robotic
152
00:14:15,599 --> 00:14:20,399
companies are renting so many kitchens to train their cooking robots that you can't get an Airbnb
153
00:14:20,400 --> 00:14:25,959
in California anymore. It's probably exaggerated, but I think it's one of these funny anecdotes
154
00:14:25,960 --> 00:14:32,798
that just say that it's still quite early within robotics. That said, there have been
155
00:14:32,799 --> 00:14:38,759
moments recently where I'm thinking we might be on the verge of a breakthrough. So the journey has
156
00:14:38,799 --> 00:14:44,159
begun. And, you know, we have a long ways to go. But this is fascinating, Richard. We can have a
157
00:14:44,160 --> 00:14:50,759
separate episode. Just going deeper, dive on this. Um, for the interest of for the sake of time, uh,
158
00:14:50,759 --> 00:14:55,919
I'd love to kind of wrap this up right now and come up with, uh, you know, your parting advice,
159
00:14:55,920 --> 00:15:01,800
share your parting advice to the viewers. Uh, if they're listening to you, what's next that they
160
00:15:01,800 --> 00:15:07,559
should do after this? So I think the most interesting thing I've learned working in AI over
161
00:15:07,560 --> 00:15:13,119
the last eight years is that
162
00:15:13,239 --> 00:15:20,239
sometimes you have to get out of the AI space to make actual progress. Yeah, I know
163
00:15:20,240 --> 00:15:24,999
it's a little bit counter-intuitive, but if you look at what engineering companies make the
164
00:15:24,999 --> 00:15:31,918
fastest progress, like SpaceX, they actually do this in a very simplistic manner. They're
165
00:15:31,919 --> 00:15:36,519
like, let's go build this rocket, let's go test this rocket and see what happens, and then learn
166
00:15:36,519 --> 00:15:41,959
from this and iterate from this. I think engineers who love. Next generation tools, whether that is
167
00:15:41,959 --> 00:15:48,839
advanced simulation or AI, can get very swept up in, oh, I'm going to go and solve this with AI and
168
00:15:48,840 --> 00:15:53,760
then don't realize that in many cases, sometimes there can actually be a very simple and intuitive
169
00:15:53,760 --> 00:15:58,678
solution and are practical, right? Like get out of the simulator and just check whether this thing
170
00:15:58,679 --> 00:16:04,520
drops when you sort of stop holding it, right. Like can sometimes actually solve a lot of problems.
171
00:16:04,559 --> 00:16:10,439
Awesome. Awesome. So my closing thing would be just AI isn't replacing an engineer, it's giving them
172
00:16:10,439 --> 00:16:15,759
the superpowers to use it constructively and learn from it, test more and iterate more. Thank
173
00:16:15,759 --> 00:16:20,799
you everyone for joining us for this episode. We had a fantastic conversation with Richard. I'm
174
00:16:20,800 --> 00:16:25,279
sure you all will love listening to this and stay tuned for more. Thank you.
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
