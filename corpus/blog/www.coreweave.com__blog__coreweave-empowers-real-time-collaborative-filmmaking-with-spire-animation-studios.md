# CoreWeave Empowers Real-Time Collaborative Filmmaking with Spire Animation Studios

Source: https://www.coreweave.com/blog/coreweave-empowers-real-time-collaborative-filmmaking-with-spire-animation-studios

Announcement

Webinar

Podcast

GTC 2026

CoreWeave Forge is here: connect your AI loop and compound every improvement. Read more

Contact us

## Radically Collaborative
Co-founded by veteran animation producer Brad Lewis (Ratatouille; How to Train Your Dragon: The Hidden World) and industry entrepreneur P.J. Gunsagar (Cofounder of Prana Studios and edtech company Kidaptive), Spire Animation Studios is a new, highly collaborative animation company, creating feature films with Unreal Engine.
During the pandemic, Spire Studios had teams of creators spread across the world and sought to proactively build a single unified workflow, free from the compartmentalization found at many studios.
Having no legacy infrastructure to constrain their choices down to a specific platform or pipeline, Spire was free to make the best choice for their artists. Maintaining full-context for an entire film and all associated decision making was key as Spire sought to provide a radically new collaborative environment.
Spire ultimately decided to partner with CoreWeave to build out the studio’s infrastructure and fully leverage the power of Unreal Engine - workstations, storage, renderfarm and networking - all in the cloud.

## Goodbye Linear Design & Rebuild Process, Hello Real-Time Iteration
Traditional animation pipeline structure is linear, moving from concept to final film, step by step.

Spire is pioneering a much more collaborative process. “We decided to use Unreal Engine as the base where we can bring in all the elements of the environment, assemble those environments, capture the story elements, add lighting, do effects and render it all interactively within the engine itself,” says Rajesh Sharma, VP of Engineering at Spire Studios.

At the heart of Spire’s new process is real-time filmmaking. CoreWeave is bringing this together, helping Spire teams create and prepare assets from the very beginning of a project right through to finalizing. At Spire, an entire film is always available for all artists to look at and iterate upon in the current state. This allows multiple stakeholders to simultaneously take part in the process of world-building and storytelling.
“By having faster iterations, we are able to get more of them, and the refinement process, whether we want to give reviews, change the lighting or move characters, can be done interactively, rather than waiting 2 or 3 hours for a render to come back in a traditional setting. We can make our decisions quickly because everything is interactive and everything is at full resolution.” Rajesh Sharma, VP of Engineering at Spire Animation Studios

Landing an Epic Mega Grant last year allowed Spire to immerse their artists in the full power of the Unreal Engine, including prototyping their ultra collaborative workflows and ultimately pushing the engine to achieve the complexity and animation style they were looking for.

## Multi-User Editing & Pixel Streaming

Real-time workflows present a major shift in how studios like Spire can interact in the cloud and accelerate their pipelines with real-time feedback loops that more closely mirror live-action filmmaking.
Beyond the faster iterations that an individual artist can achieve with Unreal, there are capabilities for multi-user editing and even more collaborative workflows. Rajesh and Spire look forward to having multiple artists work on the same set, while offering the opportunity for a director to review work remotely.
“Pixel streaming is another technology that we are looking at. We have a vision to provide full access to the current state of the film, whatever state it is in currently. We want our team to have the capability to scroll through the entire film and look at it historically, in terms of versions of a particular shot sequence, all the way back into the story stage and then progressing as it is iterated upon to create the final pixels. Having that particular view, either by shot or by sequence or for the entire film – in a single interface will be one great use of the pixel stream technologies.” Rajesh Sharma, VP of Engineering at Spire Animation Studios
As they continue to look for new visualization pipeline opportunities, Spire and CoreWeave are investigating how best to leverage USD and NVIDIA GPUs with Pixel Streaming to allow Spire high-quality previews of any asset at any time.

## Cloud-Native GPUS and Virtual Machines

To achieve the incredible scene-complexity they desire, while allowing for multi-user editing, Spire needed a large number of high-end GPUs and plenty of  memory. They had explored consumer-market graphics cards in the past, but the memory and compute wasn’t enough. 
They had also tried shipping physical workstations to each artist’s home and setting up drive storage platforms to facilitate data sharing. 
Neither solution allowed for the scale Spire needed to adequately tackle feature-length animation work, especially as their workforce expanded around the world. 
That’s when Spire turned to CoreWeave to help build out an infrastructure in the cloud. CoreWeave helped Spire access virtually unlimited compute, with the flexibility to configure instances precisely for each artist's workflows across the production pipeline.
When an artist starts, as part of the onboarding process, Spire and CoreWeave automatically provision a machine for them with the right software needed for their particular type of work. The day they begin, their tailored machine is ready and they simply need to press a button to begin working.
CoreWeave allows changes to the specification of any Virtual Machine in real-time because everything is managed through the Kubernetes interface. This means studios like Spire can immediately get a new Virtual Machine for any artist and have complete control over the specs. For instance, Spire may want to attach an artist to a NVIDIA A40 and then switch them down to a NVIDIA A4000 when they no longer need the more robust hardware. This helps studios like Spire save costs and rightsize their workflow.
“CoreWeave provides us with virtual workstations that have high-end NVIDIA GPUs. Not just for the individual artists, but also for rendering on the queue as well. If we need to provision hundreds of GPU’s for a long sequence, we are able to do that quickly and easily – and that’s been awesome.” Rajesh Sharma, VP of Engineering at Spire Animation Studios

## Kubernetes & The Cloud

At CoreWeave, we have the ability to scale up workloads significantly faster because we are a Kubernetes native cloud. That means, when an artist goes to view a film project, we can spin-up a NVIDIA GPU in 20-30 seconds or less and we can have an artist viewing it immediately; there is no delay and the artist does not need to wait for resources to come up.
Inside Kubernetes, CoreWeave can also provision containerized rendering workers on demand and automatically scale the deadline workers to meet any need. This means Spire can quickly go from 0 to 1,000 deadline workers within a minute, which is something they could not accomplish on another cloud and would be difficult to manage manually.

## Spire Studios' New Architecture 

Using CoreWeave's VS API, Spire built a custom dashboard to assign workstations for specific artists and allow them to spin that workstation up or down at any time.
Tapping into CoreWeave’s on-demand compute, Spire used the VS API to test and spin-up short lived machines that perform a particular task and then self-destruct. 
As a startup, Spire had to be mindful about investing large sums upfront into technology that could change or not meet demands down the road. Spire also did not want to create a situation where they had large unused capacity or came up short during later parts of the production process.
Instead, Spire was able to offload hardware & infrastructure to CoreWeave, rather than making the large capital expenditures and on-going maintenance investments it would take to build it themselves.
Having been part of larger studios in the past, Spire’s management and artists were familiar with the constant need to accurately balance the utilization of their hardware resources. CoreWeave’s scale-on-demand was the perfect solution, even allowing Spire to narrowly focus-in on optimal allocation of memory, processors and storage per artist, based on actual usage stats.
Within the cloud-native workflow that Spire and CoreWeave have designed,  storage lives in the exact same place as all of the other resources, giving all resources access to it instantly with extremely high performance. This means there is no delay between when Spire needs to render a job and when that job is actually rendered.
“One great thing about building our entire infrastructure in the cloud is that we don’t have to ‘upload’ scene data to render it. It’s all already there!” Rajesh Sharma, VP of Engineering at Spire Animation Studios

## Next-Level Solutions
As Spire Studios adds additional artists and workflows to the cloud, the complexity of animation infrastructure and the associated storage continue to deepen and develop. While Spire ramps up and adds multiple feature films to their pipeline, CoreWeave will be hard at work building solutions.
“CoreWeave has been a great partner for the last 6 months! We are learning together and building solutions together. The support has been fantastic and it truly feels like a partnership.” Rajesh Sharma, VP of Engineering at Spire Animation Studios
Watch the full interview with Spire Studios and learn more about their cloud-native architecture below:

Stay tuned for Spire’s first feature film, Trouble, out soon with Danny McBride’s Rough House Pictures. The story follows 13-year-old Jax, who gets in trouble with his family and is swept into a parallel reality known as the World of Trouble. He embarks on an adventure, making new friends, reflecting on his character and learns the value of self-forgiveness, all while trying to figure out how to get out of trouble, and get back home.

Share this article:

Copied

## Related blogs

### Convergent Science Advances Engineering Simulation on CoreWeave

10
min read

### CoreWeave Builds the First Global Backbone Network Purpose-Built for AI

5
min read

### Post-Training at the Frontier

7
min read

### CoreWeave Powers Agentic AI, HPC, and Data Analytics Workloads with NVIDIA HGX Rubin NVL8

5
min read

### Introducing CoreWeave Physical AI Launchables: Run Workloads With One Command

min read

### CoreWeave Zero Trust AI Framework: Your Model. Your Data. Your Trust. 

8
min read

### From Training to Serving: Reflection’s Beam on CoreWeave

min read

### Why the AI Loop Will Test Every Security Assumption

min read

### Agents on Live Hardware: Reason Where You Must, Engineer Everywhere Else

min read

### CoreWeave Direct-to-Expert: Work With the Engineers Who Built CoreWeave Cloud

5
min read

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

CoreWeave for Media & Entertainment,

Copy code

Copied!

CoreWeave for Media & Entertainment,
