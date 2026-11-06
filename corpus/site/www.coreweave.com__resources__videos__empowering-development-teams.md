# AI-Powered Engineering | AI Cloud Essentials Ep 10

Source: https://www.coreweave.com/resources/videos/empowering-development-teams

Announcement

Webinar

Podcast

GTC 2026

CoreWeave Forge is here: connect your AI loop and compound every improvement. Read more

Contact us

Copied

Overview
Transcript

## Episode 10: AI Cloud Essentials Podcast
 In this episode of the AI Cloud Essentials Podcast, Camille Fournier, VP of Engineering at CoreWeave, joins host Ritu Jyoti to discuss how AI agents are reshaping engineering workflows, accelerating development, and changing the role of developers.
Learn where AI coding tools deliver the most value today, why code review and validation are becoming new bottlenecks, and how organizations are adopting agent-driven workflows across software development and operations.
In this session, you’ll learn:
- How AI agents are changing engineering workflows
- Where AI coding tools are most effective today
- Why code review and validation are emerging challenges
- How non-engineers are using AI to build and automate work
- What engineers need to do to stay relevant as AI evolves rapidly
‍

00:00

1
00:00:00,320 --> 00:00:06,320
AI is triggering a fundamental shift in the software development process. Instead of being in
2
00:00:06,320 --> 00:00:12,080
the IDE and actually looking directly at the code yourself, you are talking to an agent or sometimes
3
00:00:12,080 --> 00:00:19,040
multiple agents doing the coding for you. What is the next generation of software teams look like? I
4
00:00:19,040 --> 00:00:25,320
talk with Camille, VP of Engineering at CoreWeave, to get her insights. There's a whole pipeline from
5
00:00:25,320 --> 00:00:31,800
idea to code to validation and testing to release, to support. Yeah.
6
00:00:31,840 --> 00:00:37,520
And I think we've all really gone deep into the generating code part of that. The rest of that
7
00:00:37,520 --> 00:00:42,480
pipeline, we're just going to hit all the bottlenecks everywhere else. Whether you had a CIO,
8
00:00:42,520 --> 00:00:48,079
VP of software development or a developer, you will find this exploration insightful and
9
00:00:48,080 --> 00:00:49,039
enlightening.
10
00:00:58,160 --> 00:01:04,329
Hello, everyone. Welcome to season two of the AI Cloud Essentials, a podcast series brought to you
11
00:01:04,330 --> 00:01:10,529
by CoreWeave. Today we are talking about the autonomous engineering frontier and I'm super
12
00:01:10,529 --> 00:01:15,969
excited to be joined by Camille. So Camille, welcome. Thank you. You know, in the past couple of
13
00:01:15,970 --> 00:01:21,849
years, we have seen. A lot of advancements. Into how the developers role and the developer's life is
14
00:01:21,849 --> 00:01:27,930
completely transformed. I would love to get your take on your personal journey and what you're
15
00:01:27,930 --> 00:01:33,410
seeing in the industry. Yeah, sure. So I mean, it's been a very interesting few years, as you
16
00:01:33,410 --> 00:01:40,169
said. You know, I think that two years ago, two and a half years ago, we were sort of
17
00:01:40,209 --> 00:01:47,050
starting to see a little bit of traction with copilot and, you know, some of the tools
18
00:01:47,050 --> 00:01:53,609
where you would be in your, in your IDE or, you know, and it would sort of suggest code for you. You
19
00:01:53,609 --> 00:01:58,569
could, you know, you could get a little bit more than your normal autocomplete kind of activity
20
00:01:58,609 --> 00:02:03,809
from the AI. And that was definitely a benefit. And lots of teams use that. Lots of teams have
21
00:02:03,809 --> 00:02:10,809
been using that. But things started to really change about, you know, last November ish
22
00:02:10,809 --> 00:02:15,609
and certainly even really early this year. Right. Just very quickly, as more and more people have
23
00:02:15,609 --> 00:02:22,329
realized the power of that sort of a genetic coding where instead of being in the IDE and
24
00:02:22,369 --> 00:02:27,969
actually looking directly at the code yourself, you are talking to an agent or sometimes multiple
25
00:02:27,969 --> 00:02:33,609
agents doing the coding for you, and you are giving them various types of instructions in
26
00:02:33,609 --> 00:02:40,569
order to actually generate the code without you really necessarily looking at the code in context
27
00:02:40,570 --> 00:02:47,289
yourself. And that is a huge change that I think is really rocking the tech industry right now. Um,
28
00:02:47,289 --> 00:02:52,009
you know, as people try to figure out how in the world do I adapt to this? What does this mean? What
29
00:02:52,009 --> 00:02:57,369
does this mean for me as a developer? Uh, you know, what does this mean for me as a product manager?
30
00:02:57,369 --> 00:03:01,289
What does this mean for me as a marketing person? You know, here, here at CoreWeave, we're actually
31
00:03:01,289 --> 00:03:08,179
doing a hack week this week. Um, and it is amazing to see. I so I, I
32
00:03:08,220 --> 00:03:13,059
happen to, you know, lead the developer experience team here. So I have sort of access to the stats
33
00:03:13,059 --> 00:03:18,579
of what kind, you know, people using these AI coding tools. And it is remarkable how many people
34
00:03:18,580 --> 00:03:24,459
not in engineering are using them to play around, to do things for, you know, for their job in
35
00:03:24,460 --> 00:03:31,100
marketing or revenue or, you know, HR recruiting, right? People are really, you know,
36
00:03:31,139 --> 00:03:35,739
non coders are definitely getting into the game. And it's definitely a very interesting time. Yeah,
37
00:03:35,779 --> 00:03:40,659
I can completely relate with it because I started my career as a developer and I remember, you know,
38
00:03:40,659 --> 00:03:46,859
all the boilerplate text and all the conundrums that we had to do. So GitHub Copilot itself was
39
00:03:46,860 --> 00:03:51,939
interesting, but now, you know, looking into all the agents and now started my own company and I have
40
00:03:51,939 --> 00:03:56,099
moved, gotten back to my engineering roots and doing the development. And you are so spot on. You
41
00:03:56,099 --> 00:04:01,820
know, like in terms of talking about how you could actually see an agent do the things for you, and
42
00:04:01,820 --> 00:04:07,100
I'm experiencing it firsthand. So I'm super excited to talk to you further on this. How do you
43
00:04:07,100 --> 00:04:13,179
see the use cases and scenarios that are being awarded? Right? As you said, people were using it
44
00:04:13,179 --> 00:04:19,539
first just for code completion, but now helping it reason and plan and write the entire code. So
45
00:04:19,820 --> 00:04:24,299
could you talk about a couple of use cases in scenarios where the internal or external that
46
00:04:24,299 --> 00:04:30,940
you're seeing? Yeah, I mean, the most I would say that still in, you know, most
47
00:04:30,940 --> 00:04:34,659
companies that maybe aren't like, I don't know, Anthropic where they say they're not writing any
48
00:04:34,659 --> 00:04:40,099
code at all by hand, which, you know, may very well be true for them, but I think most companies that
49
00:04:40,099 --> 00:04:46,499
are still trying to figure out how to adopt this. Uh, people definitely see a huge amount of value
50
00:04:46,499 --> 00:04:52,179
in using it, both for like, kind of new things. So Greenfield, as we call it. Right. And engineering. So
51
00:04:52,179 --> 00:04:58,179
you, you have a new idea of a new brand new project starting from that and letting the agent
52
00:04:58,179 --> 00:05:04,859
really do it, do all of the all of the, like, work itself from the jump, or in a lot of cases, people
53
00:05:04,859 --> 00:05:11,510
are also using it for kind of like the side work that you might not normally have bothered to
54
00:05:11,549 --> 00:05:16,790
do, but that's so easy to get generated from the agents that now it's like actually like, you know,
55
00:05:16,869 --> 00:05:23,829
I can make this like weird sort of testing setup that, you know, because Claude can just kind of
56
00:05:23,870 --> 00:05:27,989
write it for me. Or Cursor can kind of generate it for me or whatever, you know, whatever I'm using.
57
00:05:28,269 --> 00:05:33,349
Um, and I don't have to remember how to use that particular library and this other weird, weird
58
00:05:33,390 --> 00:05:38,630
tool. Uh, and it's okay if it isn't perfect, because it's not like something I'm putting into
59
00:05:38,630 --> 00:05:43,829
production. It's just a a tool to help me do the parts of my job faster. Yeah. So I feel like we see
60
00:05:43,829 --> 00:05:50,069
a lot of that adoption. Um, and then a lot of greenfield adoption. And slowly people are trying
61
00:05:50,070 --> 00:05:55,070
to work it into how do I actually use this for my preexisting code base? So that's still, I think the
62
00:05:55,070 --> 00:06:00,189
area where everyone's doing a lot more work to figure it out. I see a lot of people doing some
63
00:06:00,190 --> 00:06:06,030
migration of their legacy code into the new code. I know cursor is one of your customers. I've been
64
00:06:06,030 --> 00:06:11,589
reading about them. And I also seen that people are using it, as you said, for the greenfield
65
00:06:11,589 --> 00:06:17,510
opportunities. Like, I love to use it for doing some mock ups, right? If I have to do some mock ups
66
00:06:17,510 --> 00:06:22,709
to get some inspiration, and then I might write the whole code myself. So internally, how are you
67
00:06:22,709 --> 00:06:27,789
folks using it at code V? How is your own developers and your own internal customers? It is
68
00:06:27,829 --> 00:06:32,590
a, you know, a breadth of of usages, right? So definitely lots of greenfield. Right? We have a lot
69
00:06:32,590 --> 00:06:39,589
of new initiatives that, you know, have kicked off very, very quickly because, you know, the people,
70
00:06:39,630 --> 00:06:42,750
you know, the engineers working on those initiatives are very comfortable working in this
71
00:06:42,750 --> 00:06:46,950
multi-agent environment and throwing a bunch of things at it. One of the most interesting things
72
00:06:46,950 --> 00:06:53,829
here, so our CTO is the biggest spender on AI tools here. Yeah. Um, which and I actually
73
00:06:53,829 --> 00:06:57,429
discovered this yesterday and I asked him, hey, Peter, like, what are you what are you doing? And
74
00:06:57,429 --> 00:07:04,149
he's like, well, you know, I am. He's using a huge amount for operational automation,
75
00:07:04,190 --> 00:07:09,439
understanding what's going on, making better and better dashboards and correlations. You know,
76
00:07:09,480 --> 00:07:15,119
because a lot of what we do here at CoreWeave, we've obviously is we support these massively complex
77
00:07:15,160 --> 00:07:21,479
AI data centers. And, you know, this very complex AI cloud, right. And a lot of that work is, you know,
78
00:07:21,519 --> 00:07:27,520
having really deep awareness of what's going on and sort of why something is failing and in
79
00:07:27,520 --> 00:07:32,159
detecting it before our customers detected so that we can get on it and fix it and make sure it
80
00:07:32,160 --> 00:07:35,679
doesn't, you know, doesn't affect their training workloads or their their inference workloads.
81
00:07:35,680 --> 00:07:42,479
Right. Um, and, you know, Peter has always been incredibly hands on when it comes to, you know,
82
00:07:42,520 --> 00:07:46,879
detecting and fixing problems. Frankly, throughout our customers. I mean, anybody who's a
83
00:07:46,880 --> 00:07:53,358
customer, of course, knows knows Peter. And so he's just making incredibly valuable use of these
84
00:07:53,359 --> 00:08:00,079
tools to help him do that part of his job and, you know, to get more sleep. But, you know, to to help
85
00:08:00,079 --> 00:08:04,479
all the rest of us who do those kinds of activities from time to time or all the time. Uh,
86
00:08:04,480 --> 00:08:08,999
you know, also answer those questions. And so I think that's a really, you know, that is really
87
00:08:09,040 --> 00:08:12,679
interesting to me is where I'm seeing it, not for the thing that everybody thinks about, which is
88
00:08:12,679 --> 00:08:17,639
like writing new code and building new features, but actually, like, you know, just like thinking
89
00:08:17,640 --> 00:08:23,840
about your job and how you gather information and how you answer questions and how these tools can
90
00:08:23,879 --> 00:08:29,159
build automation and build dashboards and build support for you to do that. Even better. Yeah, it's.
91
00:08:29,159 --> 00:08:33,679
Such an interesting example, as you said, right? Because if you start from what your pain points
92
00:08:33,679 --> 00:08:38,479
are currently, not just the greenfield, which is exciting and how you could do it better and how
93
00:08:38,479 --> 00:08:44,039
you could actually enhance it, uh, where do you see where we are heading in terms in the future? I
94
00:08:44,039 --> 00:08:50,479
mean, the pace of innovation has been out, you know, outright insane, right? I mean, so where do you see
95
00:08:50,479 --> 00:08:55,599
what do you predict for 2026? The later half of 2026? You know, people love to ask me for
96
00:08:55,599 --> 00:09:00,918
predictions. And I always tell them I'm like, I'm not a futurist. The pace of change has
97
00:09:00,919 --> 00:09:07,679
changed is is very rapid. And I think one of the reasons that the overall world as a whole has
98
00:09:07,680 --> 00:09:12,329
still sort of struggled to make the most use of AI is because it keeps changing so quickly, and
99
00:09:12,330 --> 00:09:18,450
it's really hard to figure out how to adopt something that a month later, you have to
100
00:09:18,490 --> 00:09:24,368
completely change the way you're using it to get the most value out of it. And so I think that we
101
00:09:24,369 --> 00:09:30,089
are not yet done with that particular treadmill. Um, but I also look, I definitely think no matter
102
00:09:30,090 --> 00:09:36,769
what, everybody is seeing the value in these coding agents, it's just it's undeniable. Not I'm
103
00:09:36,769 --> 00:09:41,770
not saying that it solves every coding problem. I know plenty of people who regularly apply it to
104
00:09:41,770 --> 00:09:46,649
their code bases, and they're like, it's just not ready for this complexity, this gigantic, super
105
00:09:46,650 --> 00:09:52,569
complex, odd language code base, what have you. Right. But, you know, for a lot of things that
106
00:09:52,570 --> 00:09:56,408
people do, they get they are, you know, in the engineering space, I think they are figuring out
107
00:09:56,409 --> 00:10:02,530
how to get value from it. Um, now, as a person who, among other things, runs a developer experience
108
00:10:02,530 --> 00:10:07,288
team, one of the challenges is, of course, writing code is not the only thing that we do, but there's
109
00:10:07,289 --> 00:10:13,699
a whole pipeline from idea to code to validation and testing to, you know,
110
00:10:13,739 --> 00:10:20,259
release to support. And I think we've all really gone deep into the generating code part of that.
111
00:10:20,380 --> 00:10:25,299
The rest of that pipeline, you know, we're just going to hit all the bottlenecks everywhere else,
112
00:10:25,340 --> 00:10:29,539
right? Um, you know, a lot of people are talking about code review is a big bottleneck right now,
113
00:10:29,580 --> 00:10:35,820
right? So when you've got, you know, when you spend, you know, so I was talking to a friend who almost
114
00:10:35,820 --> 00:10:40,179
entirely just writes code through agents. And I was like, you know, what is your okay. So if you
115
00:10:40,179 --> 00:10:44,659
never, barely ever touch the code yourself, like, what does it look like? He's like, well, you know, we
116
00:10:44,659 --> 00:10:51,579
spend whatever like a month, like banging away on this design and like, you know, sort of proposal
117
00:10:51,580 --> 00:10:55,499
spec that we want to do. So then me and other engineers are really talking about what do we
118
00:10:55,499 --> 00:11:00,820
want to do? Okay. Then we give it to the agent and whatever, you know, breakdown they have. And the
119
00:11:00,820 --> 00:11:06,339
agent spends like 30 hours or however long chugging away at it. And then, you know, I was like,
120
00:11:06,379 --> 00:11:12,139
and now I've got a stack of pull requests and I'm babysitting those through kind of the review and
121
00:11:12,140 --> 00:11:17,419
validation process. And, you know, on the one hand, he's like, and it's like, this is an this is
122
00:11:17,419 --> 00:11:21,900
interesting for me because like, it's like the as an engineer, some of the fun part of being an
123
00:11:21,900 --> 00:11:25,780
engineer is actually writing the code. And there's none of that in there. Right? It's all the kind of
124
00:11:25,820 --> 00:11:31,099
like, uh, you know, dealing with your coworkers, you know, trying to figure out the design and then
125
00:11:31,139 --> 00:11:35,538
dealing with your coworkers, trying to get the pull requests approved. But, you know, it is
126
00:11:35,539 --> 00:11:40,779
interesting to see, like, okay, if if he's in the situation where he's really managed to get away
127
00:11:40,780 --> 00:11:46,378
from that writing of the code entirely now it's like, okay, well, we've got the rest of these steps.
128
00:11:46,419 --> 00:11:52,140
What does that look like? You know, and this is just a first pass of optimization. So okay, you
129
00:11:52,140 --> 00:11:57,459
know, now that now that we've got, you know, the the agent writing all these stack pull requests, you
130
00:11:57,460 --> 00:12:04,178
know, can we use the agent to actually help with the pull requests. What are we reviewing really.
131
00:12:04,259 --> 00:12:10,139
Are we really expecting the engineers to really review the code that they didn't write, or are we
132
00:12:10,140 --> 00:12:16,069
expecting them to review the spec and review the testing and review the, you know, the support plan.
133
00:12:16,109 --> 00:12:21,909
Right? I think these are all questions that we are going to be answering and trying and failing at
134
00:12:21,909 --> 00:12:26,709
and trying and succeeding at in both ways throughout. Certainly the rest of the year. I would
135
00:12:26,710 --> 00:12:30,829
guess the next several years, to be honest with you, as things change, we're going to continuously
136
00:12:30,830 --> 00:12:36,589
have to be changing our workflows and really identifying those bottlenecks and optimizing for
137
00:12:36,590 --> 00:12:42,309
them. What are the early lessons learned based on all the code that has been written by an agent?
138
00:12:42,390 --> 00:12:47,469
You know, the the concerns and of course, people, you know, when you're using it in your own
139
00:12:47,510 --> 00:12:52,788
internal setup, you might be able to kind of provide it to your existing code, your existing
140
00:12:52,789 --> 00:12:58,548
style of writing and all. So what are the lessons and takeaways from that aspect? And as you said,
141
00:12:58,590 --> 00:13:03,869
you know, code review the code that has not been written by them. But at the same time, if it has
142
00:13:03,870 --> 00:13:09,589
picked up some of their nuances and best practices and how we can actually do it better, I
143
00:13:09,590 --> 00:13:14,309
do. I think that's, you know, so much of the concerns and challenges and issues right now are
144
00:13:14,309 --> 00:13:18,430
really just about like the humans and how they interact with one another with regards to this
145
00:13:18,430 --> 00:13:25,030
stuff. So like, yeah, definitely everyone I know has had the experience of someone on the team went a
146
00:13:25,030 --> 00:13:30,989
little too wild, generated a whole bunch of code that they themselves didn't really
147
00:13:31,349 --> 00:13:36,869
review very carefully, and then threw it over the fence to their colleagues to say, review this. And
148
00:13:36,869 --> 00:13:42,749
their colleagues are like, I'm looking at this and it's clearly sloppy or it's not. You know, it seems
149
00:13:42,750 --> 00:13:46,589
like it makes sense. But then I have to like, peel it apart. And I'm just like, wait, what? What does
150
00:13:46,590 --> 00:13:52,549
this do? What does that do? And I feel like you're giving me a lot of work, uh, because you didn't
151
00:13:52,549 --> 00:13:57,189
really think about what was produced that carefully. You were just like, I produced a bunch,
152
00:13:57,229 --> 00:14:03,629
and you guys go now. Have to have to read it. I think that is like, that is a
153
00:14:03,630 --> 00:14:09,790
lesson that it's interesting. I think we've all learned it, but not all of us know how to approach
154
00:14:09,790 --> 00:14:13,989
it. You know, I have friends that are talking about, you know, they have, uh, early career developers
155
00:14:14,030 --> 00:14:19,559
right on their teams. and they like, look. Some of them are very, you know, are very careful and
156
00:14:19,560 --> 00:14:23,840
they're really trying to do the work and they're not even always generating. They're actually
157
00:14:23,840 --> 00:14:27,798
sometimes writing it by hand to really make sure they understand. And that's that's going fine
158
00:14:27,840 --> 00:14:31,839
right there. They're doing great. They're learning. They're very, very productive. And then some of
159
00:14:31,840 --> 00:14:36,879
them like are very clearly using a lot of AI. And that's fine, except that when we come in and give
160
00:14:36,879 --> 00:14:41,359
them feedback about like this isn't that good and you need to redo it, they're like, why should I do
161
00:14:41,359 --> 00:14:46,120
that? Like the AI is just going to support it. The AI is just going to write the next one. And you
162
00:14:46,120 --> 00:14:51,359
know, nobody's quite comfortable with that yet. Is my is my feeling right? Like, you know, I think that,
163
00:14:51,399 --> 00:14:55,879
you know, in reality, especially when it comes to more early career engineers who are trying to
164
00:14:55,879 --> 00:15:00,640
make the most use out of this, as they should. Yeah. Um, I think, you know, people who don't want to
165
00:15:00,640 --> 00:15:06,040
listen to their colleagues saying, hey, like, no, we can't. We especially with certain types of systems.
166
00:15:06,040 --> 00:15:09,439
And I'm working on a database, I'm working on an operating system, working on something that's
167
00:15:09,440 --> 00:15:15,399
really foundational to the way a lot of people work. You know, we actually have to have higher
168
00:15:15,399 --> 00:15:20,199
standards for what good looks like. This isn't a toy web app that you know three people are going
169
00:15:20,199 --> 00:15:25,199
to use, and it doesn't really matter, right? Um, so I think that a lot of it really is just still the
170
00:15:25,199 --> 00:15:31,599
interpersonal. It's the how do teams work together once these content is generated and, you know, make
171
00:15:31,640 --> 00:15:37,879
sure that they're not setting themselves up for later challenges and failures. Great, great. I think,
172
00:15:37,879 --> 00:15:43,879
uh, as you were talking about this whole, you know, context, I was thinking about it. What we've seen
173
00:15:43,879 --> 00:15:48,559
so far, in my humble opinion, is that it's very good in sometimes, you know, creating some one
174
00:15:48,559 --> 00:15:53,919
piece of module or something, but it's not very good in a holistic, systematic design or a whole
175
00:15:53,920 --> 00:15:58,879
system design. So I think a lot of advancements need to be there as well. But this is fantastic
176
00:15:58,880 --> 00:16:04,480
conversation, Camila. I am sure our viewers learned a lot. What will be your parting advice to anyone
177
00:16:04,480 --> 00:16:11,479
who's listening to us today? My parting advice is always, you know, keep, keep learning
178
00:16:11,479 --> 00:16:18,209
and stay open minded and accept that you are going to do some not quite
179
00:16:18,209 --> 00:16:23,928
throw away work, but you're going to do some like iterations right now, right? If you you can't just
180
00:16:23,969 --> 00:16:28,729
ignore what's going on and wait for it to settle, because it's going to take a while to settle. So
181
00:16:28,729 --> 00:16:33,889
you do need to be keeping up and learning and trying to figure it out and just be comfortable
182
00:16:33,889 --> 00:16:38,449
with the fact that, like the way you approach getting value from these tools today, it may
183
00:16:38,449 --> 00:16:42,369
change in a month and that will be a little bit annoying because you're going to have to like,
184
00:16:42,409 --> 00:16:48,850
change it up and to meet to meet the new, you know, the new styles. But you know, this is also kind of
185
00:16:48,890 --> 00:16:55,609
exciting, right? And I think the people, everyone I know who is, um, you know, open
186
00:16:55,609 --> 00:17:02,129
minded, you don't have to be open minded and, and like, totally like, but in that it is the way the
187
00:17:02,129 --> 00:17:07,368
world will be for all things. Right. You can be open minded and skeptical, but open mindedness is
188
00:17:07,369 --> 00:17:13,728
so important right now when it comes to learning how to use these tools, making the best, getting
189
00:17:13,729 --> 00:17:18,529
the best out of them, you know, take the best and leave the rest. But you've got to keep looking
190
00:17:18,530 --> 00:17:23,409
regularly because they change so quickly that something that they couldn't do three months ago,
191
00:17:23,449 --> 00:17:30,289
they may be able to do for you today. And you know that hopefully over time will allow you
192
00:17:30,290 --> 00:17:35,449
to focus more on the things that are fun and get rid of some of the grunt work and tedious work
193
00:17:35,449 --> 00:17:41,369
for yourself. And you know, I am cautiously optimistic that that is the direction we can we
194
00:17:41,369 --> 00:17:46,889
can make this all go if we if we really put our minds to it. Awesome. Very nice. Nice. Couldn't agree
195
00:17:46,890 --> 00:17:53,009
more. One cannot sit on the fence, but I have to go with the flow. But also be cautious and be, you
196
00:17:53,009 --> 00:17:57,969
know, pragmatic about what really works and what doesn't work. Thank you so much, Camille. It was
197
00:17:57,969 --> 00:18:03,009
such a pleasure to have you with us in this episode. And thank you, everyone, all our viewers
198
00:18:03,010 --> 00:18:08,208
who are listening to us, and stay tuned. We are coming up with more episodes. Thank you.
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
