# Democratizing Data Access with AI at Nasdaq | CoreWeave

Source: https://www.coreweave.com/resources/videos/empowering-intelligence-democratizing-data-access-enhancing-efficiency-and-driving-smarter-decisions-at-nasdaq

Announcement

Webinar

Podcast

GTC 2026

CoreWeave Forge is here: connect your AI loop and compound every improvement. Read more

Contact us

Copied

Overview
Transcript

See how one of the world's most data-intensive technology companies is putting AI-ready capabilities into the hands of its clients, not just a specialized few. Nasdaq will share how it's rethinking the path from raw market and operational data to decisions clients can act on in real time. You'll hear where self-service access unlocks speed, where governance and compliance still have to hold the line, and how CoreWeave's infrastructure factors into scaling that work. You'll also hear concrete examples of efficiency gains from reducing the friction between data and the people who need it, and what it took organizationally, not just technically, to get there. Walk away with a practical view of how a highly regulated, high-stakes environment is balancing broader data democratization with the resilience its business depends on.
Speakers: Marc Murphy, Senior Vice President, Nasdaq

00:00

1
00:00:00,000 --> 00:00:05,860
So, first of all, maybe a little bit about
2
00:00:05,860 --> 00:00:09,900
Nasdaq and what we do, and there'll
3
00:00:09,900 --> 00:00:10,620
be two pillars
4
00:00:10,620 --> 00:00:12,540
that I talk about today.
One will be about our
5
00:00:12,540 --> 00:00:14,860
physical infrastructure
that supports trading
6
00:00:14,860 --> 00:00:18,200
and markets, and the other
will be about software.
7
00:00:18,200 --> 00:00:20,460
But from an overall point of view,
8
00:00:20,960 --> 00:00:22,900
Nasdaq is the Nasdaq
stock exchange, and we
9
00:00:22,900 --> 00:00:25,400
have many other exchanges around the world
10
00:00:25,400 --> 00:00:29,580
as well that operate in a similar
fashion. I think many know that and
11
00:00:29,580 --> 00:00:30,740
understand that.
12
00:00:31,180 --> 00:00:35,800
We also offer a lot of services to listed
companies. So, think of Apple, Google,
13
00:00:35,960 --> 00:00:41,180
CoreWeave, etc. We also have a financial
technology business. This is a little bit
14
00:00:41,180 --> 00:00:44,590
less known, but we provide software
15
00:00:44,590 --> 00:00:49,140
products, applications, etc. to financial
16
00:00:49,140 --> 00:00:49,920
institutions
17
00:00:49,920 --> 00:00:54,080
all over the world, central banks,
large banks, regulators, etc.
18
00:00:54,080 --> 00:00:57,200
And that business is
something that is critical for
19
00:00:57,200 --> 00:00:59,800
the day-to-day operation
of many of these firms.
20
00:01:02,700 --> 00:01:06,860
So, where I wanted to start today and what
I'll share with you from a context
21
00:01:06,860 --> 00:01:08,200
point of view
22
00:01:08,200 --> 00:01:11,720
is how we're responding
and reacting, positioning
23
00:01:11,720 --> 00:01:14,940
for the future as it
relates to something that
24
00:01:14,940 --> 00:01:18,860
is obvious to all of you, I'm sure,
and that is that you have this convergence
25
00:01:18,860 --> 00:01:19,860
over the last
26
00:01:19,860 --> 00:01:24,620
number of years of high-performance
compute and agentic capabilities.
27
00:01:25,540 --> 00:01:27,820
And that is changing the world
in a lot of different
28
00:01:27,820 --> 00:01:30,180
ways, but obviously
from our point of view,
29
00:01:30,240 --> 00:01:33,360
we look at that, you know, both
for ourselves, but for our clients.
30
00:01:33,860 --> 00:01:37,220
And it's very interesting how it's
impacting trading, and it's changing the
31
00:01:37,220 --> 00:01:38,320
requirements and
32
00:01:38,320 --> 00:01:41,640
what we need to be and how we need
to position in a dramatic way.
33
00:01:42,480 --> 00:01:44,520
So, if you think about capacity,
34
00:01:44,520 --> 00:01:47,320
capability, and trust,
these are things that
35
00:01:47,320 --> 00:01:48,360
we all need to
36
00:01:48,360 --> 00:01:52,770
think about going forward, and when you
particularly think about high-performance
37
00:01:52,770 --> 00:01:55,400
compute and agentic capabilities.
38
00:01:55,820 --> 00:02:00,000
I heard in the keynote earlier, you know,
a lot about context, a lot about trust.
39
00:02:00,200 --> 00:02:02,930
So, obviously, with what
we do on a day-to-day
40
00:02:02,930 --> 00:02:05,800
basis, particularly
serving the clients that
41
00:02:05,800 --> 00:02:09,380
we serve, we don't have
an option to fail, right?
42
00:02:09,400 --> 00:02:11,450
We don't have an option for downtime, so
43
00:02:11,450 --> 00:02:14,380
resilience and trust is
really, really important.
44
00:02:15,860 --> 00:02:19,980
So, if you think about capacity, you know,
we think about, in a physical sense,
45
00:02:19,980 --> 00:02:21,120
power, space,
46
00:02:21,200 --> 00:02:24,680
and compute capability,
what we put on top of that,
47
00:02:24,680 --> 00:02:28,100
so a lot of our software,
and then, obviously, trust.
48
00:02:28,540 --> 00:02:31,480
You know, when we think about trust,
you can't go and buy trust.
49
00:02:31,780 --> 00:02:34,040
You can't manifest trust quickly.
50
00:02:34,580 --> 00:02:38,280
So, that is something that you earn over
time, through years and years, usually,
51
00:02:38,280 --> 00:02:39,480
of production
52
00:02:39,480 --> 00:02:41,600
grade success and zero downtime.
53
00:02:42,680 --> 00:02:46,430
And for those that, you know, look after
production systems, you never get that
54
00:02:46,430 --> 00:02:47,520
phone call to thank
55
00:02:47,520 --> 00:02:48,640
you for being up that day.
56
00:02:48,700 --> 00:02:49,700
It's just expected.
57
00:02:50,240 --> 00:02:56,440
So, the two pillars we'll talk about are,
you know, from microseconds to megawatts.
58
00:02:56,980 --> 00:03:01,000
So, that's talking about how, in
the trading world, speed has always been
59
00:03:01,000 --> 00:03:02,600
really, really important.
60
00:03:03,100 --> 00:03:04,140
It's always relative.
61
00:03:04,400 --> 00:03:07,040
So, if you go back,
you know, 100 years, there
62
00:03:07,040 --> 00:03:09,520
was speed for trading was still important.
63
00:03:09,520 --> 00:03:13,080
It was just being conveyed differently,
whether that be pigeons or otherwise.
64
00:03:13,980 --> 00:03:15,280
And then, megawatts.
65
00:03:15,580 --> 00:03:19,720
You know, power, since probably around
the 70s, when Nasdaq was formed.
66
00:03:19,720 --> 00:03:24,280
And maybe a little bit before,
compute and electricity was important.
67
00:03:24,280 --> 00:03:26,710
But we're now seeing something interesting
68
00:03:26,710 --> 00:03:29,200
happen in recent years,
where more and more
69
00:03:29,200 --> 00:03:34,040
power is being demanded as compute
grows around the trading systems.
70
00:03:35,500 --> 00:03:39,300
And then, pillar two, when we get to it,
we'll talk about the software side.
71
00:03:39,800 --> 00:03:44,440
Nasdaq's financial technology software and
how that's being impacted by these trends.
72
00:03:46,740 --> 00:03:52,720
So, starting with the physical, for
those that don't know, some of you might
73
00:03:52,720 --> 00:03:54,520
not have a trading background.
74
00:03:54,900 --> 00:03:55,900
You know, what are markets?
75
00:03:56,620 --> 00:03:57,540
And there's a lot that goes into that.
76
00:03:57,540 --> 00:03:58,580
And there's a lot that goes into that.
77
00:03:58,580 --> 00:04:01,850
But interestingly, it's very much a
78
00:04:01,850 --> 00:04:06,200
API-driven world and a programmatic world,
79
00:04:06,200 --> 00:04:07,200
where you have
80
00:04:07,200 --> 00:04:09,400
a hardware stack sitting somewhere.
81
00:04:09,720 --> 00:04:11,160
It's physically somewhere.
82
00:04:11,560 --> 00:04:14,700
And people are plugging into that
in a variety of different ways.
83
00:04:14,900 --> 00:04:17,240
And they're receiving
messages and information.
84
00:04:17,400 --> 00:04:20,240
And they're also pumping
messages and information into
85
00:04:20,240 --> 00:04:22,860
it, based on the signals
and information they receive.
86
00:04:23,700 --> 00:04:29,720
So, you have brokers, investors,
market makers, people connecting to it.
87
00:04:30,220 --> 00:04:34,970
Sometimes it's directly, other times
it's, you know, secondary and through
88
00:04:34,970 --> 00:04:36,080
other people.
89
00:04:36,760 --> 00:04:39,980
But what comes out of that
is trust, in a way, right?
90
00:04:40,380 --> 00:04:43,080
You have to trust what comes
out of it, and that is prices.
91
00:04:43,780 --> 00:04:45,280
You get liquidity out of it.
92
00:04:45,720 --> 00:04:49,440
And then you have a bunch of risk
management that is sitting around that.
93
00:04:50,320 --> 00:04:55,820
So, you look at this, and, you know,
you think, wow, that's complicated and,
94
00:04:55,820 --> 00:04:58,180
you know, very
95
00:04:58,180 --> 00:05:01,090
nuanced in, you know,
being able to have this
96
00:05:01,090 --> 00:05:03,840
operate on a day-to-day
basis in a good way.
97
00:05:04,440 --> 00:05:07,160
But the key point here
is that it's physical.
98
00:05:07,780 --> 00:05:10,320
And because it's physical,
you have latency.
99
00:05:10,320 --> 00:05:12,200
And latency matters in trading.
100
00:05:13,100 --> 00:05:15,910
So, imagine, and this is
important, particularly
101
00:05:15,910 --> 00:05:18,060
in the U.S., where you
have multiple different
102
00:05:18,060 --> 00:05:20,590
trading venues dispersed
geographically, you
103
00:05:20,590 --> 00:05:23,080
have different prices at different venues.
104
00:05:23,580 --> 00:05:27,780
So, your source of truth is different
depending on where you physically are.
105
00:05:28,520 --> 00:05:30,660
And it's not that one is
wrong or one that's, you
106
00:05:30,660 --> 00:05:33,660
know, is not, you know,
it's not wrong or right.
107
00:05:34,220 --> 00:05:36,500
It's just where it is
at that point in time.
108
00:05:37,040 --> 00:05:39,470
Now, you might be informed
by that at a point,
109
00:05:39,470 --> 00:05:42,320
you know, point A might
inform you that point
110
00:05:42,320 --> 00:05:45,380
B is an opportunity, or it could
inform you that it's a risk.
111
00:05:46,280 --> 00:05:50,240
So, it's just important to realize when
we think about markets and we think
112
00:05:50,240 --> 00:05:51,300
about compute
113
00:05:51,300 --> 00:05:54,160
and we think about agentic
capabilities coming
114
00:05:54,160 --> 00:05:56,860
into the mix, that we're
dealing with a physical
115
00:05:56,860 --> 00:05:58,420
system when we talk about trading.
116
00:05:58,660 --> 00:06:01,230
It's sitting somewhere,
and there can be multiple
117
00:06:01,230 --> 00:06:04,040
instances of that,
whether it's run by Nasdaq
118
00:06:04,040 --> 00:06:08,300
or others, that could reflect a different
truth, and that's all driven by the
119
00:06:08,300 --> 00:06:09,620
physical location.
120
00:06:10,680 --> 00:06:15,520
So, this is obvious, but it's important
to reflect on when we start talking
121
00:06:15,520 --> 00:06:16,660
about, again,
122
00:06:16,760 --> 00:06:20,900
how we're impacted by high-performance
compute and agentic capabilities.
123
00:06:22,180 --> 00:06:24,180
All of what the market is, you might think
124
00:06:24,180 --> 00:06:26,580
of it as, well, it's just,
you know, a ticker
125
00:06:26,580 --> 00:06:30,440
that I see in Times Square or it's
just prices on a screen, but obviously
126
00:06:30,440 --> 00:06:31,720
somewhere, given
127
00:06:31,720 --> 00:06:34,560
that it's physical, it's
sitting on land and plant.
128
00:06:34,980 --> 00:06:37,000
It has HVAC attached to it.
129
00:06:37,480 --> 00:06:40,040
It has power running
into it, and it has all
130
00:06:40,040 --> 00:06:42,520
of the things that we know and love of any
131
00:06:42,520 --> 00:06:44,260
traditional data center, and that would be
132
00:06:44,260 --> 00:06:46,080
true if it was running
in the cloud as well.
133
00:06:47,180 --> 00:06:48,620
So, here's the interesting
thing that we're
134
00:06:48,620 --> 00:06:51,320
observing, and it's not
a new thing, but it's
135
00:06:51,320 --> 00:06:57,300
probably accelerating, and that is, you
know, traditionally or from the dawn of
136
00:06:57,300 --> 00:06:58,580
time, you've
137
00:06:58,580 --> 00:07:03,950
had trading firms think about research,
eventually develop different trading
138
00:07:03,950 --> 00:07:05,820
strategies, and with
139
00:07:05,820 --> 00:07:08,500
that, different ways of managing risk, and
140
00:07:08,500 --> 00:07:11,160
they do that, you know,
if I was just to make
141
00:07:11,160 --> 00:07:14,530
it up, they might do that, you know,
over the course of a year, they might do
142
00:07:14,530 --> 00:07:15,820
that 25 times
143
00:07:15,820 --> 00:07:21,180
or 50 times, and they would sometimes
use compute to do that, other times they
144
00:07:21,180 --> 00:07:22,660
would do unit-based
145
00:07:22,660 --> 00:07:25,320
testing, you know, deep
research, depending on
146
00:07:25,320 --> 00:07:27,840
the type of people they
have and the strategies
147
00:07:27,840 --> 00:07:30,150
that they like to execute, they would do
148
00:07:30,150 --> 00:07:32,940
that in different ways,
but what we're seeing
149
00:07:32,940 --> 00:07:39,180
now is that there is a much greater
investment in deep research powered by the
150
00:07:39,180 --> 00:07:40,260
advances in
151
00:07:40,260 --> 00:07:43,310
compute and agentic
capabilities, so you're seeing
152
00:07:43,310 --> 00:07:46,220
the velocity of that
and the volume of that grow.
153
00:07:46,720 --> 00:07:49,480
So, to use that basic
example, if there was 50
154
00:07:49,480 --> 00:07:52,280
strategies being developed in a given year
155
00:07:52,280 --> 00:07:55,610
by trading firm ABC, maybe they're doing
156
00:07:55,610 --> 00:07:59,890
300 or 500 today, because they have,
157
00:07:59,890 --> 00:08:02,000
you know, capabilities
158
00:08:02,000 --> 00:08:04,900
somewhere where they can do
deep research, they can do
159
00:08:04,900 --> 00:08:07,720
modeling, and then they can
bring that to production.
160
00:08:09,060 --> 00:08:11,800
So, imagine this happening,
you know, in Norway,
161
00:08:11,800 --> 00:08:15,360
Iceland, somewhere cheap,
where they can run
162
00:08:15,360 --> 00:08:18,740
these, you know, models
and research programs,
163
00:08:18,740 --> 00:08:21,680
and then that spits out,
it says, okay, based
164
00:08:21,680 --> 00:08:26,630
on the market data we've been consuming,
we think there's an opportunity to
165
00:08:26,630 --> 00:08:27,740
deploy strategy
166
00:08:27,740 --> 00:08:34,260
X and Y to US equities, in particular
to Nasdaq, to the Nasdaq stock exchange.
167
00:08:34,780 --> 00:08:36,560
So, what is the next step in that?
168
00:08:36,840 --> 00:08:39,860
Well, you actually have
to deploy that, usually, to
169
00:08:39,860 --> 00:08:42,660
the co-location environment
of that trading market.
170
00:08:43,320 --> 00:08:45,350
So, you have a data center somewhere to do
171
00:08:45,350 --> 00:08:48,420
your deep research
and modeling, that gives
172
00:08:48,420 --> 00:08:52,620
you confidence that you should execute
or at least try this in production.
173
00:08:53,480 --> 00:08:57,940
Part of your strategy requires that it
has low latency between, you know, its
174
00:08:57,940 --> 00:08:58,940
calculation
175
00:08:58,940 --> 00:09:03,740
and what it's, you know, maintaining
over a course of a trading day to the
176
00:09:03,740 --> 00:09:04,820
exchange, so
177
00:09:04,820 --> 00:09:06,820
it needs to go next to the,
where the exchange
178
00:09:06,820 --> 00:09:08,720
stack is that we talked about earlier.
179
00:09:09,020 --> 00:09:11,450
So, we're seeing, you
know, this flywheel, if
180
00:09:11,450 --> 00:09:14,020
you will, increase
and become more dramatic.
181
00:09:14,700 --> 00:09:18,860
And as a result, we need more compute,
we need more power and space, we need
182
00:09:18,860 --> 00:09:19,980
more cooling,
183
00:09:20,260 --> 00:09:21,860
et cetera, to support that.
184
00:09:22,620 --> 00:09:25,130
So, why is this a good
thing and why do, you
185
00:09:25,130 --> 00:09:28,800
know, exchanges care about it like Nasdaq?
186
00:09:30,980 --> 00:09:33,730
Basically, the more
compute that we can get
187
00:09:33,730 --> 00:09:36,740
around our trading system,
the more power and
188
00:09:36,740 --> 00:09:41,080
cooling that we can provide, then
the better off our markets can be.
189
00:09:41,880 --> 00:09:45,560
And the reason for that is that with
more strategies and more participation,
190
00:09:45,560 --> 00:09:47,520
you will get deeper
191
00:09:47,520 --> 00:09:49,840
liquidity and then broader participation.
192
00:09:50,380 --> 00:09:52,950
So, people have the opportunity
to come in and try
193
00:09:52,950 --> 00:09:55,260
out what they think would
be a great strategy.
194
00:09:55,940 --> 00:09:58,620
So, I've touched on this
already, but large-scale
195
00:09:58,620 --> 00:10:01,460
compute equals more research
and experimentation.
196
00:10:02,080 --> 00:10:03,360
So, that's sort of a macro trend.
197
00:10:03,440 --> 00:10:06,860
It's not something that
we control or decide upon.
198
00:10:07,360 --> 00:10:10,200
Our different clients and trading
firms are doing that themselves.
199
00:10:11,920 --> 00:10:15,340
They're then discovering different
risk techniques, different trading
200
00:10:15,340 --> 00:10:16,680
strategies, as we talked
201
00:10:16,680 --> 00:10:19,520
about, that they can then bring to market.
202
00:10:20,620 --> 00:10:21,950
And I would say that this is a fundamental
203
00:10:21,950 --> 00:10:24,680
shift over the last
five years in particular
204
00:10:24,680 --> 00:10:28,680
that is changing, you know, again,
the requirements that we have.
205
00:10:28,860 --> 00:10:33,140
And today is all about sharing that
context with you to support all of that
206
00:10:33,140 --> 00:10:34,720
coming into, you
207
00:10:34,720 --> 00:10:36,420
know, our systems, our data centers.
208
00:10:37,100 --> 00:10:39,160
So, what have we done about it?
209
00:10:39,560 --> 00:10:41,910
At Nasdaq, we do spend
a lot of time looking
210
00:10:41,910 --> 00:10:44,840
at trends, as I mentioned
up front, working
211
00:10:44,840 --> 00:10:47,210
with partners like CoreWeave to, you know,
212
00:10:47,210 --> 00:10:49,760
engage with the industry,
understand what's
213
00:10:49,760 --> 00:10:51,600
happening, understand how to be ready.
214
00:10:52,060 --> 00:10:54,250
And obviously, with a lot
of these things, it takes
215
00:10:54,250 --> 00:10:57,100
a number of years, usually,
to prepare and be ready.
216
00:10:57,620 --> 00:10:59,570
So, the things we've done, which are, you
217
00:10:59,570 --> 00:11:02,340
know, not going to solve
everything for us in
218
00:11:02,340 --> 00:11:06,200
the next, you know, couple of decades,
but we have expanded our data center.
219
00:11:07,040 --> 00:11:09,140
Over the last, I think, three, four, five
220
00:11:09,140 --> 00:11:11,600
years, we've roughly
doubled that footprint.
221
00:11:12,200 --> 00:11:15,540
It's not a huge footprint to start
with, but doubling is doubling.
222
00:11:16,380 --> 00:11:18,460
And we've also introduced,
again, not novel,
223
00:11:18,460 --> 00:11:21,200
but for exchanges around
the world, I think
224
00:11:21,200 --> 00:11:25,540
we were the first to introduce liquid
cooling, which we'll go live with shortly.
225
00:11:26,620 --> 00:11:28,500
And, you know, what that signifies is that
226
00:11:28,500 --> 00:11:31,640
high-density compute
to run what I mentioned
227
00:11:31,640 --> 00:11:34,250
earlier, the trading
strategies and the risk
228
00:11:34,250 --> 00:11:36,880
management programs,
does offer a solution,
229
00:11:36,980 --> 00:11:40,660
right, because now you have two
things coming together, which is more
230
00:11:40,660 --> 00:11:42,000
opportunities are being
231
00:11:42,000 --> 00:11:44,920
discovered, more strategies
are being developed.
232
00:11:45,480 --> 00:11:48,200
And then when you go to place them
next to the exchange, you have more
233
00:11:48,200 --> 00:11:49,380
availability to
234
00:11:49,380 --> 00:11:50,480
high-performance compute.
235
00:11:50,920 --> 00:11:52,180
So, what does all of that equal?
236
00:11:52,260 --> 00:11:56,830
It equals opportunity and difference,
which I think is interesting and
237
00:11:56,830 --> 00:11:58,120
certainly helpful
238
00:11:58,120 --> 00:12:02,950
to expand our markets and make sure that
they're liquid and wonderful, right,
239
00:12:02,950 --> 00:12:04,800
have a good experience with them.
240
00:12:05,140 --> 00:12:09,440
I just wanted to, I mean, a little
bit different, but I just wanted to
241
00:12:09,440 --> 00:12:11,220
highlight from an AI point
242
00:12:11,220 --> 00:12:17,800
of view, we also use agentic development
and tooling to further the market.
243
00:12:17,980 --> 00:12:19,640
So, our internal product development.
244
00:12:19,640 --> 00:12:23,080
And one of those things was
something we called Dynamic M-ELO.
245
00:12:23,920 --> 00:12:29,290
So, we have an agentic capability of
basically when an order comes in, we will
246
00:12:29,290 --> 00:12:30,320
determine at
247
00:12:30,320 --> 00:12:32,410
that point in time using agentic
248
00:12:32,410 --> 00:12:35,190
capabilities what is
the right time to hold
249
00:12:35,190 --> 00:12:36,240
that order.
250
00:12:36,700 --> 00:12:41,040
So, it could be 12 seconds, it could
be 8 or, you know, that type of thing.
251
00:12:41,120 --> 00:12:43,440
So, it's a variable thing,
but the whole point
252
00:12:43,440 --> 00:12:45,640
is to give a good
experience for our clients.
253
00:12:46,060 --> 00:12:50,770
So, that is just one example where
the high-performance compute that we're
254
00:12:50,770 --> 00:12:52,260
putting into our data centers
255
00:12:52,260 --> 00:12:56,640
for our clients, we're also starting
to use ourselves to actually operate the
256
00:12:56,640 --> 00:12:57,720
trading stack.
257
00:12:58,420 --> 00:13:01,660
So, I'm going to shift gears a little
bit here and we'll move into the fintech
258
00:13:01,660 --> 00:13:02,720
side of things.
259
00:13:02,720 --> 00:13:03,880
We talked about the physical.
260
00:13:04,560 --> 00:13:08,720
We talked about the fact that, you know,
compute and the agentic capabilities
261
00:13:08,720 --> 00:13:09,740
is changing what
262
00:13:09,740 --> 00:13:12,780
our clients are bringing to us, what
they're wanting to put into production.
263
00:13:13,360 --> 00:13:15,570
Now, we'll talk about
on the software side of
264
00:13:15,570 --> 00:13:18,600
things, how we're preparing
and what infrastructure
265
00:13:18,600 --> 00:13:21,170
we're building to ensure
that that software is
266
00:13:21,170 --> 00:13:24,040
fit for purpose in the,
you know, coming decades.
267
00:13:25,500 --> 00:13:27,800
And we call that the Nasdaq
intelligence layer.
268
00:13:29,120 --> 00:13:35,100
It's simply an infrastructure and a
technical stack that we overlay with our
269
00:13:35,100 --> 00:13:36,660
existing products.
270
00:13:37,180 --> 00:13:38,680
And the reason we do that is that it gives
271
00:13:38,680 --> 00:13:41,500
our clients a common
interface and something
272
00:13:41,500 --> 00:13:43,920
that they can plug into
and build on top of.
273
00:13:44,380 --> 00:13:45,720
And it gives them optionality.
274
00:13:46,800 --> 00:13:50,940
And when I talk about the products that
we have, we have these core products
275
00:13:50,940 --> 00:13:52,220
within our fintech
276
00:13:52,220 --> 00:13:57,740
suite, so we have Verafin, which is
a anti-money laundering and anti-financial
277
00:13:57,740 --> 00:13:59,480
crime software stack
278
00:13:59,480 --> 00:14:02,940
that sits in many banks
throughout the U.S.
279
00:14:02,940 --> 00:14:05,500
and the world and, you
know, does things like
280
00:14:05,500 --> 00:14:10,200
check fraud or identifies signals for,
you know, human trafficking even.
281
00:14:10,440 --> 00:14:14,840
So, it helps people to investigate and
understand what's happening within their,
282
00:14:14,840 --> 00:14:16,020
you know, transaction
283
00:14:16,020 --> 00:14:20,120
data set of a bank and then
address those issues.
284
00:14:21,040 --> 00:14:25,100
And then within our regulatory tech
group, we have Axiom and market
285
00:14:25,100 --> 00:14:26,560
surveillance.
286
00:14:27,240 --> 00:14:29,040
So, those are both regulatory tools.
287
00:14:29,220 --> 00:14:32,760
On the Axiom side, it's things like
regulatory reporting, et cetera.
288
00:14:33,060 --> 00:14:37,820
And then for market surveillance,
that is surveilling the markets to ensure
289
00:14:37,820 --> 00:14:38,940
that if there's anything
290
00:14:38,940 --> 00:14:44,000
improper happening, those that are
responsible can view that and address it.
291
00:14:44,860 --> 00:14:49,050
And then you have on capital markets
tech where this would be our trading,
292
00:14:49,050 --> 00:14:51,700
clearing, CSD and
293
00:14:51,700 --> 00:14:53,280
treasury management systems.
294
00:14:53,820 --> 00:14:56,820
So, as I mentioned earlier, these
are all super critical for different
295
00:14:56,820 --> 00:14:58,120
stakeholders depending
296
00:14:58,120 --> 00:14:59,860
on who they are.
297
00:14:59,960 --> 00:15:03,200
And these are things that, you know,
can't be down at any point in time.
298
00:15:03,540 --> 00:15:06,340
The other interesting thing
here is that there's sources
299
00:15:06,340 --> 00:15:08,940
of truth within these
applications that are critical.
300
00:15:09,880 --> 00:15:14,450
So, for Calypso, for example, if you're
running an asset manager and you want
301
00:15:14,450 --> 00:15:15,860
to know valuation
302
00:15:15,860 --> 00:15:20,800
at a point in time for all sorts
of reasons, what is the source of truth?
303
00:15:20,860 --> 00:15:25,210
You've probably got multiple different
applications or calculations within your
304
00:15:25,210 --> 00:15:27,000
company in your stack
305
00:15:27,000 --> 00:15:28,140
that would tell you that.
306
00:15:28,140 --> 00:15:29,360
But which one do you believe?
307
00:15:29,500 --> 00:15:33,420
Which one do you rest your laurels
on to say this is the gold source?
308
00:15:34,260 --> 00:15:36,800
And for all of our applications,
we're often that source.
309
00:15:37,360 --> 00:15:41,770
And that becomes important when you
have an ambition to overlay agentic
310
00:15:41,770 --> 00:15:44,540
workflows into this.
311
00:15:45,080 --> 00:15:50,450
Because an agent acting on information
that is not trusted or it has context
312
00:15:50,450 --> 00:15:51,860
that isn't accurate
313
00:15:51,860 --> 00:15:55,540
or misinterpreted or misinterpreted
is very severe and very dramatic.
314
00:15:55,720 --> 00:16:02,300
So, naturally, our clients and ourselves
are somewhat skeptical about, you know,
315
00:16:02,400 --> 00:16:06,720
overlaying agentic workflows on top
of this without first being rock solid and
316
00:16:06,720 --> 00:16:08,100
feeling very confident
317
00:16:08,100 --> 00:16:11,100
in regards to the context
and semantic layer.
318
00:16:11,800 --> 00:16:16,380
So, this is partly solved at the product
level, each of these areas, but also
319
00:16:16,380 --> 00:16:19,020
you want something
and infrastructure on top of that
320
00:16:19,020 --> 00:16:23,630
to represent, present that and make sure
it's consistent and something you can
321
00:16:23,630 --> 00:16:25,780
interact with or build on top of.
322
00:16:27,960 --> 00:16:31,820
So, I won't go through too much of this,
but all of the things that you would
323
00:16:31,820 --> 00:16:33,220
expect in this day and age
324
00:16:33,220 --> 00:16:36,200
and some of the things that you would
have heard about in the keynote as well.
325
00:16:36,800 --> 00:16:42,170
Everybody is craving and, you know,
it's really table stakes to have these
326
00:16:42,170 --> 00:16:45,420
things when you're wanting
to build agentic workflows
327
00:16:45,420 --> 00:16:50,180
for anything that is, you know, beyond,
you know, let's say consumer grade.
328
00:16:50,260 --> 00:16:53,200
When you get to the point of a regulator
329
00:16:53,200 --> 00:16:56,880
walking in, coming
to your desk and saying,
330
00:16:57,020 --> 00:17:01,880
you need to tell me why did this
agentic workflow behave the way it did
331
00:17:01,880 --> 00:17:06,660
and why did it take the decision that it
did and what documentation do you have
332
00:17:06,660 --> 00:17:07,960
of all of that occurring.
333
00:17:08,860 --> 00:17:13,440
That is the baseline and the table stakes
that we think about when we develop
334
00:17:13,440 --> 00:17:14,820
agentic workflows
335
00:17:14,820 --> 00:17:17,420
or where clients will build their own.
336
00:17:17,780 --> 00:17:20,210
So, to do that, we need
infrastructure under
337
00:17:20,210 --> 00:17:22,360
that and we need to spend a lot of time,
338
00:17:22,600 --> 00:17:28,020
a lot of effort documenting,
creating semantic context, etc.
339
00:17:28,760 --> 00:17:34,740
So, it does all come down to trust, as
I mentioned, and also, you know, there's
340
00:17:34,740 --> 00:17:35,980
opportunities as you build out
341
00:17:35,980 --> 00:17:40,890
this type of platform in that they can
talk to each other, you can open up for
342
00:17:40,890 --> 00:17:43,800
creative new ways of solving problems.
343
00:17:44,460 --> 00:17:49,760
One good example is we have a use case
working through now, which is, you know,
344
00:17:49,760 --> 00:17:51,380
the trading system of a,
345
00:17:51,620 --> 00:17:56,990
it's a national exchange that has
one single exchange that can now have
346
00:17:56,990 --> 00:17:58,840
interaction between the trading
347
00:17:58,840 --> 00:18:01,860
and clearing, which does
happen today, but now
348
00:18:01,860 --> 00:18:04,160
you've unlocked the agentic
connection to it
349
00:18:04,160 --> 00:18:09,520
and then you load it up with semantics
and context and definition that is
350
00:18:09,520 --> 00:18:10,720
trusted and common
351
00:18:10,720 --> 00:18:14,580
and then that allows for people to become
a lot more innovative in solving
352
00:18:14,580 --> 00:18:16,060
different problems,
353
00:18:16,260 --> 00:18:17,760
creating new products, etc.
354
00:18:17,760 --> 00:18:20,100
So, why is this hard?
355
00:18:21,940 --> 00:18:25,400
I think many of you probably grapple
with this yourselves already.
356
00:18:26,060 --> 00:18:27,980
It isn't hard to prototype.
357
00:18:29,000 --> 00:18:32,400
It isn't hard to explain
the value to someone.
358
00:18:33,340 --> 00:18:36,680
It isn't hard to get
into production for one
359
00:18:36,680 --> 00:18:39,000
or two clients with one or two use cases.
360
00:18:39,480 --> 00:18:45,960
What is really, really hard is to do
that at scale and still feel comfortable
361
00:18:45,960 --> 00:18:47,860
when you go to sleep at night
362
00:18:47,860 --> 00:18:53,220
that you trust it, that your client
trusts it, and that you won't have
363
00:18:53,220 --> 00:18:54,680
exceptions that you don't expect.
364
00:18:55,780 --> 00:18:58,390
And it's important that
it's not exceptions,
365
00:18:58,390 --> 00:19:01,200
you know, I'll underline
that you don't expect
366
00:19:01,200 --> 00:19:03,680
because you will have exceptions,
but they just need to be bounded.
367
00:19:04,240 --> 00:19:07,020
And everybody needs to understand
that you have bounded exceptions.
368
00:19:07,840 --> 00:19:09,720
And it's also where does the exception go?
369
00:19:10,560 --> 00:19:11,820
Does it go to a human or does it just go
370
00:19:11,820 --> 00:19:14,600
straight through and you
hope for the best?
371
00:19:15,900 --> 00:19:19,810
The other part of the, you know,
what we've built in the platform is the
372
00:19:19,810 --> 00:19:22,220
ability for data to come back into it.
373
00:19:22,580 --> 00:19:27,050
Again, it's not novel, it's not new,
but it's a really important requirement
374
00:19:27,050 --> 00:19:30,700
when you're wanting to learn about
workflows being successful or not
375
00:19:30,700 --> 00:19:34,520
and to what degree they are, you need
to have that data coming back in.
376
00:19:35,080 --> 00:19:37,820
So we do allow our clients
to feed the data back in.
377
00:19:38,320 --> 00:19:43,680
And a good example of that one is where
we have an agentic capability today
378
00:19:43,680 --> 00:19:46,640
where we help clients in
their treasury management
379
00:19:46,640 --> 00:19:51,360
to settle or clear breaks
with counterparties.
380
00:19:51,360 --> 00:19:57,760
So for example, very basic example,
you may need to send, let's say, 400,000
381
00:19:57,760 --> 00:20:00,220
Swiss francs to a bank account by 2 p.m.
382
00:20:00,240 --> 00:20:01,500
or you will incur a fee.
383
00:20:02,460 --> 00:20:04,500
Now, it's not an overly complex workflow.
384
00:20:05,080 --> 00:20:09,760
But if an agentic workflow that is
developed by the client, a third party or
385
00:20:09,760 --> 00:20:10,960
Nasdaq ourselves
386
00:20:10,960 --> 00:20:15,200
can save fees of, let's say, $100,000 in a
387
00:20:15,200 --> 00:20:18,200
given week, how do you
know that that happened?
388
00:20:19,020 --> 00:20:20,640
How do you know the value of that?
389
00:20:20,720 --> 00:20:24,820
Well, you need to feed that information
back in, capture it, and then, you know,
390
00:20:24,880 --> 00:20:27,920
align it back with the workflow
that had driven that outcome.
391
00:20:28,400 --> 00:20:32,600
I spoke about it earlier, but, you
know, critical market infrastructure.
392
00:20:32,600 --> 00:20:35,120
I mean, we live
and breathe this every day.
393
00:20:35,880 --> 00:20:37,840
It just isn't an option to fail.
394
00:20:37,940 --> 00:20:40,100
It's not an option to be,
you know, going down.
395
00:20:40,580 --> 00:20:46,350
So in building this, we have so many more
expectations for ourselves that we do
396
00:20:46,350 --> 00:20:48,880
it in a way that is really
robust and rigorous.
397
00:20:49,160 --> 00:20:52,660
So again, I'm sure some
of you can appreciate that.
398
00:20:52,720 --> 00:20:56,420
But for us, it adds a lot of complexity,
but it's a non-negotiable.
399
00:20:56,700 --> 00:21:01,100
Probably the biggest point about these
two things that I talked about, right?
400
00:21:01,160 --> 00:21:04,880
We talked about the physical trading
environment and it rapidly changing and
401
00:21:04,880 --> 00:21:06,820
creating new requirements for us.
402
00:21:07,000 --> 00:21:11,860
And we talked about being ready for the
agentic age with our software products.
403
00:21:12,000 --> 00:21:17,850
These are things that we thought about
with our clients and partners years and
404
00:21:17,850 --> 00:21:18,860
years ago.
405
00:21:19,240 --> 00:21:22,740
We didn't know all the answers, but we
knew enough that we had to do something
406
00:21:22,740 --> 00:21:24,480
and position for the future.
407
00:21:24,920 --> 00:21:27,240
So we've continued to do that.
408
00:21:27,320 --> 00:21:27,940
We did that.
409
00:21:27,940 --> 00:21:28,940
We continue to do that.
410
00:21:29,120 --> 00:21:32,810
Positioning for the future, not knowing
fully what will happen, but knowing
411
00:21:32,810 --> 00:21:36,360
that we need to be a certain place
to have flexibility and optionality.
412
00:21:37,280 --> 00:21:40,420
And that's something that we
spend a lot of time on at Nasdaq.
413
00:21:40,880 --> 00:21:44,570
Things will keep changing and we'll
keep trying to change with it and being
414
00:21:44,570 --> 00:21:49,280
ahead of the curve so that we can, you
know, take the actions that often take
415
00:21:49,280 --> 00:21:50,520
many years to be ready.
416
00:21:51,480 --> 00:21:56,710
Well, I hope me sharing some context
about our industry and how we're impacted
417
00:21:56,710 --> 00:22:00,100
and how we're positioning
for the future was useful.
418
00:22:00,660 --> 00:22:04,520
I certainly appreciated you giving me
your time and I hope you enjoy the rest
419
00:22:04,520 --> 00:22:05,880
of the conference.
420
00:22:05,880 --> 00:22:07,440
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
