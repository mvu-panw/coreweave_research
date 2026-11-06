# Auto-Scaling Deadline Workflows and Tasks | CoreWeave

Source: https://www.coreweave.com/resources/videos/auto-scaling-deadline-workflows-and-tasks

Announcement

Webinar

Podcast

GTC 2026

CoreWeave Forge is here: connect your AI loop and compound every improvement. Read more

Contact us

Copied

Overview
Transcript

This video walks through how Auto-Scaling works inside Deadline when running on CoreWeave. Jacob demonstrates how to submit a Cinema 4D render job, configure pools and groups, and use these properties to automatically scale workers up or down based on workload demand. You’ll see how quickly CoreWeave provisions workers for each task, how scaling limits can be managed through Deadline’s built-in settings, and how the system automatically cleans up workers once a job is complete. With CoreWeave’s optimized compute and behind-the-scenes automation, teams can render efficiently without manually managing infrastructure.
‍

00:00

1
00:00:00,120 --> 00:00:02,940
Hey everyone this is Jacob from CoreWeave today I’m going to be showing you how to deploy some applications
2
00:00:02,940 --> 00:00:04,940
[Music]
3
00:00:04,940 --> 00:00:10,100
So we’re going to take a look at the ways we can trigger auto scaling and functionally the work you have to do in order to scale your workloads up and down inside of Deadline on CoreWeave
4
00:00:10,100 --> 00:00:14,480
And in reality there’s really not a whole lot you have to do and that’s the beauty of it
5
00:00:14,480 --> 00:00:18,200
So what I’m going to show you is just a quick example let’s say I’m in Deadline here
6
00:00:18,200 --> 00:00:21,280
Here I have an empty monitor I have no workers or anything like that
7
00:00:21,280 --> 00:00:26,040
And I’m just going to go and submit a job here from the monitor in this case I’ll submit a Cinema 4D job
8
00:00:26,040 --> 00:00:31,260
And I’ll get my normal user interface to call it something fun maybe not so fun
9
00:00:31,260 --> 00:00:34,860
And then I have to select a few extra items here I have a pool and a group
10
00:00:34,860 --> 00:00:40,140
And these properties here can be used to drive your auto scaling relationships
11
00:00:40,140 --> 00:00:45,260
For example you could say I want to render up to 50 workers for any job that’s submitted to the VFX pool or any other pool you set up
12
00:00:45,260 --> 00:00:48,880
And in this case the way we have it organized for most people is that we drive auto scaling using these groups here
13
00:00:48,880 --> 00:00:52,960
As you’ll see if I hit this drop down I have a bunch of different options for hardware types that I can use to render my job
14
00:00:52,960 --> 00:00:58,580
They’re labeled as such so it’s C4D Arnold and then the name of a specific compute type that we’ve set up in the background
15
00:00:58,580 --> 00:01:01,840
And these will be set up for you when we give you your Deadline instances
16
00:01:01,840 --> 00:01:06,480
If you’re managing them yourself using Helm and deploying with your own values files these can be defined super easily
17
00:01:06,480 --> 00:01:10,440
And those same files can be used to adjust all the scaling relationships that I’m referencing here
18
00:01:10,440 --> 00:01:15,200
In this case I’m just going to select here at the top the C4D Arnold EPYC that runs on our new EPYC CPUs
19
00:01:15,200 --> 00:01:19,520
Everything else I’m going to leave exactly as it is I can specify my frame list and the C4D file I’ll be rendering with
20
00:01:19,520 --> 00:01:23,320
And I’m just going to go ahead and hit submit
21
00:01:23,320 --> 00:01:26,340
When that happens you can upload the job and what you’ll see is that very quickly here we’re going to get a bunch of workers popping up below
22
00:01:26,340 --> 00:01:30,280
Scaling times are usually anywhere from 5 to about 30 seconds
23
00:01:30,280 --> 00:01:35,700
Sometimes it could be a little higher if you haven’t used a group in a long time
24
00:01:35,700 --> 00:01:40,260
We cache Docker images and containerized images we use for rendering on our nodes
25
00:01:40,260 --> 00:01:43,700
So your first time submitting to a group might take a little extra time
26
00:01:43,700 --> 00:01:47,340
But here we should see it pretty quick there we go we got some workers popping up
27
00:01:47,340 --> 00:01:51,260
We should get workers essentially for every task here we’ve got 20 frames so we should get about 20 workers
28
00:01:51,260 --> 00:01:54,960
They’ll come online pretty quickly there we go they're going to keep coming online at a steady rate
29
00:01:54,960 --> 00:01:58,200
All of this is managed behind the scenes we have services written to allow you to adjust scaling relationships hands-off
30
00:01:58,200 --> 00:02:02,560
You can also control your scaling with limits inside the Deadline interface I’ll show you that in a moment
31
00:02:02,560 --> 00:02:07,040
Now that we have some workers let’s show how easy it is to clean up after you're done
32
00:02:07,040 --> 00:02:11,040
So let’s say this job finishes I’m going to manually complete the job for now
33
00:02:11,040 --> 00:02:15,780
Once the job is finished it will spin all these workers down and clean them up for us easily
34
00:02:15,780 --> 00:02:20,000
You never have to manage spinning up or shutting down workers you get compute when you need it and it disappears when you don’t
35
00:02:20,000 --> 00:02:25,200
Like I mentioned you can manage scaling limits using Deadline’s limits
36
00:02:25,200 --> 00:02:28,980
You simply create a limit inside Deadline here I’ve created one and named it the same as my group
37
00:02:28,980 --> 00:02:33,520
Inside the properties I’ve set the resource count to whatever I want the maximum number of workers to be
38
00:02:33,520 --> 00:02:37,560
Behind the scenes the name of this limit is added to your values files for the Helm deployment
39
00:02:37,560 --> 00:02:41,560
If you aren’t using Helm or CoreWeave is assisting you with deployment this will likely be created automatically
40
00:02:41,560 --> 00:02:45,960
With my limit set up and limit count set to 10 let’s submit the same job and see how the behavior changes
41
00:02:45,960 --> 00:02:49,960
I’ll submit the same job the frame list is still 1 to 20
42
00:02:49,960 --> 00:02:53,600
Now with 20 frames we should see just 10 workers spin up
43
00:02:53,600 --> 00:02:56,920
There we go now we got 10 workers and we shouldn’t get any more scaling than that
44
00:02:56,920 --> 00:03:00,560
They should just start rendering as expected
45
00:03:00,560 --> 00:03:04,560
Using limits and the deployments we’ve created you can manage the scale and flexibility of your fleet
46
00:03:04,560 --> 00:03:09,120
That’s really all there is to it auto scaling with Deadline takes the burden of managing infrastructure off of you
47
00:03:09,120 --> 00:03:13,960
If you have any questions reach out to CoreWeave at support.vfxcoreweave.com or check out our documentation
48
00:03:13,960 --> 00:03:17,140
foreign
49
00:03:17,140 --> 00:03:17,795
[Music]
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
