# AI in Financial Markets | AI Cloud Essentials Ep 9

Source: https://www.coreweave.com/resources/videos/exploring-the-financial-frontier

Announcement

Webinar

Podcast

GTC 2026

CoreWeave Forge is here: connect your AI loop and compound every improvement. Read more

Contact us

Copied

Overview
Transcript

## Episode 9: AI Cloud Essentials Podcast
In this episode of the AI Cloud Essentials Podcast, Dimitris Tsementzis, Founder and CEO of hLevel, joins host Ritu Jyoti to explore how AI systems can adapt to constantly changing market conditions and why traditional approaches often fall short in non-stationary environments.
Learn why controllability matters more than interpretability in high-risk systems, how AI is reshaping financial infrastructure, and where organizations can create real competitive advantage beyond operational efficiency.
In this session, you’ll learn:
- How AI is transforming pricing, risk, and trading systems
- Why financial markets are uniquely challenging for AI
- The role of controllability in high-risk environments
- How firms can move beyond back-office automation
- Where AI can create long-term competitive advantage in finance

### Podcast Guest: 
Dimitris Tsementzis, Founder and CEO of hLevel

00:00

1
00:00:00,120 --> 00:00:05,920
The markets are the complete opposite. They change all the time. Is AI the next innovation that will
2
00:00:05,920 --> 00:00:11,960
transform how financial markets operate? Imagine designing an LLM product, a chatbot of some kind,
3
00:00:12,000 --> 00:00:18,080
let's say something to interact with someone under the constraint that your target audience
4
00:00:18,120 --> 00:00:22,319
will start speaking a completely different language overnight. In this episode of AI Cloud
5
00:00:22,320 --> 00:00:28,560
Essentials, we talked with Dmitris, the founder and CEO of hlevel about how AI is reshaping the
6
00:00:28,560 --> 00:00:34,800
foundations of financial markets. Some systems have reached a level of complexity that we should
7
00:00:34,800 --> 00:00:39,080
focus on controlling them versus interpreting them. Whether you're a technical or a financial
8
00:00:39,080 --> 00:00:42,200
analyst, join us for a great conversation.
9
00:00:51,160 --> 00:00:56,760
Hello, everyone. Welcome to season two of the AI Cloud Essentials, a podcast series brought to you
10
00:00:56,760 --> 00:01:03,040
by Covid. In this series, we are going to the value realization phase. And I'm super excited to have,
11
00:01:03,080 --> 00:01:09,160
you know, Dimitris today with us. And guess what? We are going to talk about some of the most
12
00:01:09,160 --> 00:01:15,080
interesting areas that is being impacted by AI AI's impact in the financial market. So welcome,
13
00:01:15,080 --> 00:01:20,280
Dimitris. Good to be here. Great to be here. You know, we all have watched that AI has almost
14
00:01:20,280 --> 00:01:24,880
become a staple in the financial market over decades, right? Starting from statistical
15
00:01:24,880 --> 00:01:31,480
algorithms to modern machine learning, generative AI, genetic AI, you know, people who work in this
16
00:01:31,480 --> 00:01:38,280
industry like you, you guys are geeks in this area, right? Uh, so but
17
00:01:38,280 --> 00:01:45,000
I always kind of sit and think that. Have we moved beyond the incremental efficiency we are
18
00:01:45,000 --> 00:01:50,000
missing? It seems to me like we're missing the Black-Scholes moment for the financial market. You
19
00:01:50,000 --> 00:01:56,240
know, incremental gains are very powerful. But, you know, how do we move beyond and how do we get the
20
00:01:56,240 --> 00:02:02,040
trust and the confidence level to go beyond it. Uh, so I'd love to get your perspective on that, but
21
00:02:02,080 --> 00:02:06,360
would you mind starting a little bit with your own background, in your own journey for our
22
00:02:06,360 --> 00:02:12,479
audience? Yes. Of course, yes. And thank you very much. Uh, thank you very much for that set up. It's,
23
00:02:12,520 --> 00:02:17,039
you know, kind of touches on all the most important issues. So my background, I was, you know,
24
00:02:17,039 --> 00:02:22,520
a mathematician for a very long time. As abstract as it gets. I was writing things on blackboards.
25
00:02:22,720 --> 00:02:27,720
You know, basically, I didn't have to touch a computer. And towards the end of my PhD, I got very
26
00:02:27,720 --> 00:02:33,960
interested in machine learning and AI. So this was around the tensions. All you need, uh, era, you know,
27
00:02:34,000 --> 00:02:39,120
when those papers were beginning to come out and I thought, this is going to be a big thing. And the
28
00:02:39,120 --> 00:02:42,760
reason why I thought it was going to be a big thing is because the math kind of made sense,
29
00:02:43,000 --> 00:02:49,679
right? And I also learned during that time that in finance and in trading,
30
00:02:49,880 --> 00:02:54,720
applications of machine learning and AI were not really considered a solved problem. I thought that
31
00:02:54,720 --> 00:03:00,760
was fascinating. Here's a technology that clearly will work in some way. And here's an industry that
32
00:03:00,760 --> 00:03:06,640
hasn't fully applied it. Right. Of course, there's a reason, because there's unique difficulties that
33
00:03:06,640 --> 00:03:12,200
we're going to talk about a little bit. And I was fascinated I was completely fascinated by that.
34
00:03:12,200 --> 00:03:17,920
And I've been doing that ever since. Awesome. So AI can be the souls, black souls. So let me let me
35
00:03:17,920 --> 00:03:23,280
break that down a little bit. Maybe. Um, I think AI has two
36
00:03:23,760 --> 00:03:30,320
manifestations. One is as a technology. As a software, essentially. Uh, the
37
00:03:30,480 --> 00:03:36,480
program as a as a software product, let's say. Right. And the other has a mathematical algorithm
38
00:03:36,560 --> 00:03:42,240
now, especially in quantitative finance. Mathematical algorithms have been applied for a
39
00:03:42,240 --> 00:03:48,719
long time. Right. So AI is just one more collection of algorithms that you can potentially apply to
40
00:03:48,720 --> 00:03:55,000
the markets. Right. Um, I think with AI in its current
41
00:03:55,160 --> 00:04:01,119
form, LLMs and all these things, The black shows moment, if you will, hasn't come. What I mean by
42
00:04:01,120 --> 00:04:07,119
that, to be precise. Right. Some mathematical model of the markets that uses this specific
43
00:04:07,120 --> 00:04:14,119
mathematics to to model the markets. Hasn't had been a knockout success. But there
44
00:04:14,119 --> 00:04:21,039
is continuity here, right? Black shows was applied as a piece of very elegant mathematics. Yeah. Will
45
00:04:21,079 --> 00:04:26,600
AI also be applied as a piece of very elegant mathematics in the markets? Yeah, I think so. Great.
46
00:04:26,640 --> 00:04:32,119
It gives us all a lot of confidence. Right. So then we think about the financial markets. You know I
47
00:04:32,119 --> 00:04:38,239
mean there's a lot of risk and trust factor there, right. I mean they are also non-stationary. It's a
48
00:04:38,240 --> 00:04:44,279
completely volatile real time, you know, like so how do you see what is the current state. How does
49
00:04:44,320 --> 00:04:49,200
you know where's the frontier, the next frontier. How are we solving for the non-stationary markets.
50
00:04:49,200 --> 00:04:55,039
And it's a unique use case, right. Yes. So we'd love to hear, you know, how do you see the AI? You know,
51
00:04:55,079 --> 00:05:00,959
kind of, you know, identify all the subtle signals and how does it pick the noise and kind of make
52
00:05:00,960 --> 00:05:05,760
all our lives and all our investments much more interesting? Yes, I don't know about the latter
53
00:05:05,760 --> 00:05:12,720
parts, but I'll talk about the former part. You're correct. The tremendous success of
54
00:05:12,720 --> 00:05:19,160
AI in its current instantiation has been in context that you can call stationary language
55
00:05:19,160 --> 00:05:25,439
coding, even math. Very recently there stationary in the sense that they don't really change.
56
00:05:26,079 --> 00:05:31,799
Math is, of course a fantastic example of that. It hasn't changed for millennia. Um, you know what was
57
00:05:31,799 --> 00:05:38,200
proven by, you know, my forefathers in ancient Greece is still true today. Yeah, right. Language
58
00:05:38,200 --> 00:05:43,720
also moves very slowly. Coding, of course, didn't really exist, but once it's there, it won't really.
59
00:05:43,760 --> 00:05:48,119
What works and doesn't encoding won't really work. The markets are the complete opposite of that.
60
00:05:48,160 --> 00:05:54,960
They change all the time. So the analogy that I always use is um, imagine designing an LLM. Imagine
61
00:05:54,960 --> 00:06:00,480
designing an LLM product, a chatbot of some kind, let's say. Right. So something to interact with
62
00:06:00,480 --> 00:06:07,039
someone under the constraint that your target audience will start speaking a completely
63
00:06:07,040 --> 00:06:12,560
different language overnight. Yeah. How do you design a system that is able to cope with that?
64
00:06:12,600 --> 00:06:19,359
Yeah. Continue to function as it is learning to adapt to a completely new language, a completely
65
00:06:19,359 --> 00:06:23,559
new reality. That's really what you have to do when you design algorithms that operate
66
00:06:23,600 --> 00:06:29,159
autonomously in the market. So that's a frontier for AI. Yeah. I think, you know, the AI in its
67
00:06:29,160 --> 00:06:35,880
current form, tremendous, though it is incredible and magical sometimes, hasn't really solved that
68
00:06:35,880 --> 00:06:42,479
problem. Yeah. And the markets are one and a very prominent example of setting where you need to
69
00:06:42,480 --> 00:06:48,359
solve it in order to maximize your success. But I think this I'm hearing you speak about all of
70
00:06:48,359 --> 00:06:52,559
this. There seems to be a lot of promise that it can be a great testing ground for all the
71
00:06:52,560 --> 00:06:56,959
innovations that we've seen happening, and it can accelerate some of the innovation. I'm more
72
00:06:56,999 --> 00:07:03,959
optimistic. I mean, it is it is naturally a testing ground. Although of course, we have to be, you know,
73
00:07:04,000 --> 00:07:07,839
mindful that it cannot be an actual testing ground because we're talking about, you know, of
74
00:07:07,840 --> 00:07:14,720
course, real money, real risk. But it is it is a frontier. Yeah. It is a frontier setting. I think
75
00:07:14,720 --> 00:07:18,039
that that would be a better way to put it. I'm kind of thinking, you know, like, you know, there are
76
00:07:18,040 --> 00:07:23,199
a lot of other very interesting aspects when you think about the financial market, is the
77
00:07:23,200 --> 00:07:28,519
regulation, the constant changing geopolitical situation, the
78
00:07:30,480 --> 00:07:35,480
yeah, the shift, you know, that it's you know, you have to be we can't afford to have a black box
79
00:07:35,480 --> 00:07:41,078
moment. Right. We need to have interpret the results, have the confidence in that. So where do
80
00:07:41,079 --> 00:07:46,279
you see that. You know what kind of, you know, specialized requirements are there. What kind of
81
00:07:46,279 --> 00:07:51,279
enhancements are being worked upon in the industry to kind of address some of these very
82
00:07:51,279 --> 00:07:57,079
dynamic, apart from the real nature of the financial markets. Yeah. I think there's tremendous
83
00:07:57,079 --> 00:08:03,679
research going on on interpretability. Right. And that that research is very fascinating.
84
00:08:03,680 --> 00:08:10,359
And for anyone who's followed it, it is, you know, almost philosophically interesting, um, in the
85
00:08:10,359 --> 00:08:16,079
sense that we're kind of studying these, um, collections essentially of floating point numbers,
86
00:08:16,079 --> 00:08:22,840
as if they were human brains in some sense to, to understand what they do and where they go wrong. I
87
00:08:23,119 --> 00:08:29,439
am less optimistic about interpretability being the ultimate solution here. Okay. To us using the
88
00:08:29,440 --> 00:08:35,399
models. Yeah. So the standard that I stress is controllability. Okay. I think these models can be
89
00:08:35,400 --> 00:08:41,199
controlled and can be controlled much more practically and much sooner than we will ever
90
00:08:41,200 --> 00:08:47,559
understand exactly what they do. And at some point, I think we do need to accept that some systems
91
00:08:47,559 --> 00:08:53,359
have reached a level of complexity that we should focus on controlling them versus interpreting
92
00:08:53,440 --> 00:08:59,079
them. That's not to say that the interpretability research is not interesting and shouldn't
93
00:08:59,080 --> 00:09:03,639
continue, but we shouldn't rely on that as the ultimate solution for applying it. Got it.
94
00:09:03,680 --> 00:09:09,439
Controllability versus interpretability as a standard I. Yeah, yeah. I like that approach because
95
00:09:09,440 --> 00:09:13,519
if you think about it, you know of course it's being worked in parallel. Right. We're looking into
96
00:09:13,560 --> 00:09:18,280
how you can interpret this better and all. But if you can control because there are ramifications
97
00:09:18,280 --> 00:09:22,960
of something going wrong is really, really kind of, you know, challenging. I mean, think about, you know,
98
00:09:23,000 --> 00:09:28,399
think about when you mentor a human being, you know, you don't wait until you understand what's
99
00:09:28,400 --> 00:09:34,519
going on in their brains fully to before you have them. All your analogies. Before you have them do
100
00:09:34,520 --> 00:09:40,199
something right. Yeah. You you just create. You know, control is too strong a word for humans, but you
101
00:09:40,239 --> 00:09:46,200
create a framework to which their choices, you know, you take less risk and a more risk. And then,
102
00:09:46,240 --> 00:09:51,400
you know, if we all. If I waited to talk to you until I understood exactly what is going on in
103
00:09:51,400 --> 00:09:55,839
your brain, you know we'd never talk. So are you seeing a lot of advancements in the systems that
104
00:09:56,039 --> 00:10:00,799
help you and provide you these kind of, you know, capabilities in terms of setting the guardrails,
105
00:10:00,800 --> 00:10:05,520
in terms of setting the boundaries? Uh, are you seeing all of those enhancements happening and
106
00:10:05,520 --> 00:10:09,839
then. Yeah, I think I think a very big part of it is the hardware. You know, I mean, a very big part
107
00:10:09,840 --> 00:10:16,839
of controlling is experimenting. And if you can experiment more and more, you become more and
108
00:10:16,840 --> 00:10:23,199
more aware of edge cases, failure modes and these types of things. So I think
109
00:10:23,520 --> 00:10:29,399
really the first, the most important dimension in which systems are helping with controllability, if
110
00:10:29,400 --> 00:10:36,359
you will, is just having better hardware and being able to experiment more. Okay. Okay. So when
111
00:10:36,359 --> 00:10:41,079
you talk about better hardware, you're talking in terms of performance scale. Yeah. Being able to run
112
00:10:41,400 --> 00:10:46,879
more experiments. Okay. Yeah okay. Yeah. Awesome. So where do you see are we heading in terms of the
113
00:10:46,880 --> 00:10:51,479
industry? I know, you know, uh, financial markets have been at the forefront of a lot of
114
00:10:51,520 --> 00:10:57,200
innovations in the AI field, right? They have been the source of actually starting some of the, you
115
00:10:57,200 --> 00:11:04,079
know, fastest generations and stuff. So where do you see is the role of the financial market or in
116
00:11:04,080 --> 00:11:09,719
general, where do you see the next 3 to 5 years? I know it's difficult for any of us to predict. I
117
00:11:09,760 --> 00:11:14,519
come from an analyst background, so we always used to take stances, and I'm very happy to share that.
118
00:11:14,520 --> 00:11:19,199
We had predicted about the foundation models even before they came. There's a secret reason as to
119
00:11:19,200 --> 00:11:23,080
why we had done that, because we had just the way, you know, the attention you need. And, you know,
120
00:11:23,080 --> 00:11:29,479
we've been reading a lot of people's and all the advancements. And so it was very interesting. So
121
00:11:29,840 --> 00:11:33,839
where do you see what is happening in the industry and where we are heading in the next 3
122
00:11:33,840 --> 00:11:39,320
to 5 years? So I think the financial industry over the next 2 to 5 years is going to see increased,
123
00:11:39,479 --> 00:11:43,119
increased adoption, for sure. There's going to be a lot of adoption. People are going to get
124
00:11:43,119 --> 00:11:50,080
comfortable with these tools and some workflows in banking, in trading, back office, middle office
125
00:11:50,080 --> 00:11:55,159
are going to change fundamentally. I think there's no doubt about that. In the same way that coding
126
00:11:55,159 --> 00:12:02,119
is changing fundamentally, some of these functions are deterministic mechanical and AI systems will
127
00:12:02,119 --> 00:12:08,918
help with that. Absolutely. So I think that's the 3 to 5. 2 to 4, you know, whatever within the next
128
00:12:08,919 --> 00:12:15,599
five years. Right. And that's already happening. Of course beyond that, I think we have to focus
129
00:12:15,599 --> 00:12:22,520
on what are the people that think about deep problems in this particular industry. And
130
00:12:22,520 --> 00:12:28,439
one of the peculiarities and of course, very interesting aspects of this industry. And one of
131
00:12:28,440 --> 00:12:31,479
the things that attracted me is that you have a lot of mathematicians, a lot of pure
132
00:12:31,479 --> 00:12:38,399
mathematicians, right? So you have a combination of extremely mathematical folks, right? Including
133
00:12:38,400 --> 00:12:44,959
physics, including related disciplines, thinking about the problem of very large scale models in
134
00:12:44,999 --> 00:12:49,999
non-stationary contexts. So I think very interesting things are going to come out of that
135
00:12:50,039 --> 00:12:55,239
combination. Things that probably will not naturally come out of Silicon Valley, for example.
136
00:12:55,320 --> 00:13:01,439
Yeah. That's a that's a very, very astute observation, you know, because when you think about,
137
00:13:01,440 --> 00:13:06,679
uh, you know, like in the general realm, in the industry, we see there's a lot of paranoia about,
138
00:13:06,719 --> 00:13:13,080
you know, uh, AI taking over human jobs. So I definitely think, you know, even not just from the
139
00:13:13,080 --> 00:13:18,759
core innovation and exploration of the expansion of the use cases, but even for the financial
140
00:13:18,759 --> 00:13:23,879
analyst, it's not replacing the financial analyst. It's kind of augmenting or empowering the
141
00:13:23,879 --> 00:13:29,879
individual. Uh, do you see some similar threats in the financial market as well in terms of usage of
142
00:13:29,880 --> 00:13:35,879
AI, or do you think it's a little bit more, uh, I should say easier for them to kind of embrace it?
143
00:13:35,919 --> 00:13:41,880
Uh, in terms of their, the balance of their jobs or in terms of their adoption. Balance of their job.
144
00:13:41,920 --> 00:13:47,760
Yeah. I honestly don't know. I kind of think that who will have what job is the wrong question to
145
00:13:47,760 --> 00:13:54,199
ask? I think the right question to ask is who and why is the earliest and quickest adopter of this
146
00:13:54,200 --> 00:13:58,639
technology? Yeah, that's a very interesting way to look at. I think once we have those data points,
147
00:13:58,640 --> 00:14:04,599
we'll be able to see exactly which jobs balance out. In what way. Right. But do you see any kind of
148
00:14:04,599 --> 00:14:10,680
a pushback from certain personas, or do you feel it's pretty early or premature to kind of I. Feel
149
00:14:10,719 --> 00:14:15,999
decreasing pushback. Okay, okay. That's a positive sign. And of course, I think you're entering the
150
00:14:16,000 --> 00:14:22,759
the mechanics of folks using it in their personal lives, using using AI in their personal lives.
151
00:14:22,799 --> 00:14:27,760
And I would imagine that similar things happen in the early days of the internet and search. Right.
152
00:14:27,960 --> 00:14:32,959
You know, folks in their offices would have said, can't, you know, rely on this type of search. We
153
00:14:32,960 --> 00:14:36,359
need to rely, let's say, on specialized publications. But then they used it in their
154
00:14:36,359 --> 00:14:41,399
personal lives and they were able to find, you know, restaurants and, you know, what have you. And
155
00:14:41,400 --> 00:14:46,880
then eventually that trust bled over to the work environment. So I think I'm seeing that mechanism.
156
00:14:46,880 --> 00:14:53,119
But I do think we we right now don't have full clarity on exactly who will be the best
157
00:14:53,120 --> 00:14:58,439
adopter in terms of traditional roles in more traditional. So the next couple of years will kind
158
00:14:58,439 --> 00:15:04,280
of shape it for us. So I wouldn't speculate on the job situation. Okay. Okay. I know we can talk for
159
00:15:04,280 --> 00:15:09,959
hours on this very interesting topic, but if you have to give, you know, your parting advice to the
160
00:15:09,959 --> 00:15:15,479
people who are listening to you today, uh, what should be their approach to kind of embrace it, uh,
161
00:15:15,479 --> 00:15:22,439
play with it or iterate? What would your advice be to them? So to the technical people, I would say
162
00:15:23,560 --> 00:15:29,159
these are algorithms. Yeah. At the end of the day there's still mathematical functions, data in
163
00:15:29,159 --> 00:15:35,759
inputs in things out. So don't maybe be overly focused on the
164
00:15:35,759 --> 00:15:41,639
metaphysics around AI. Treat them as algorithms. That's kind of the best way to extend them. Yeah.
165
00:15:41,680 --> 00:15:46,919
To the non-technical folks or to the folks not necessarily interested in, in, you know, pushing the
166
00:15:46,919 --> 00:15:53,199
frontier or frontier, advancing AI. Yeah, I would say just adopt it and treat it a little bit like
167
00:15:53,200 --> 00:15:59,400
you're mentoring someone. Yeah. As opposed to, you know, someone who just has the answers for you?
168
00:15:59,439 --> 00:16:05,519
Yeah. I think that's the best approach. Yeah. Awesome. Fantastic advice. Uh, so I'd like to close
169
00:16:05,519 --> 00:16:11,079
off by thanking you. So, such a nice, uh, opportunity to meet you and kind of talk to you. And thank you
170
00:16:11,079 --> 00:16:16,959
very much. Particular episode to the viewers. I'd just like to say that there's nothing wrong in
171
00:16:16,960 --> 00:16:21,359
applying your hair to areas where there's uncertainty and try to play with it and
172
00:16:21,360 --> 00:16:28,199
experiment and feel fast. If you actually have a challenge, learn and feel fast. And, uh, stay tuned
173
00:16:28,200 --> 00:16:32,879
to be a thank you for listening to us today. Stay tuned. We have lots more to kind of share with you.
174
00:16:32,919 --> 00:16:36,119
Thank you. Have a wonderful rest of the day. Thank you very much.
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
