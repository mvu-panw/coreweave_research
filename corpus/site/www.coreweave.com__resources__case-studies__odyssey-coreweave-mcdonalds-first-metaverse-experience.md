# McDonald's Metaverse Powered by Odyssey | Odyssey Case Study

Source: https://www.coreweave.com/resources/case-studies/odyssey-coreweave-mcdonalds-first-metaverse-experience

Announcement

Webinar

Podcast

GTC 2026

CoreWeave Forge is here: connect your AI loop and compound every improvement. Read more

Contact us

Resources

Case Studies

Odyssey Hosts McDonald’s First Metaverse Experience, Powered by CoreWeave

Odyssey Hosts McDonald’s First Metaverse Experience, Powered by CoreWeave

Industry
Media and entertainment

Headquarters
Seattle, WA

Use Cases

#### Ready to get started?

Contact Sales

5
min read

Copied

How Odyssey scaled to 2,500 GPUs in real time to power McDonald's first metaverse experience

#### Using CoreWeave Cloud, Odyssey scaled its GPU capacity by as much as 500 NVIDIA GPUs every 5 minutes to host an event for 900+ McDonald’s employees.
Every year, McDonald’s brings together teams across the globe to celebrate their creative work, employee milestones, and achievements. But last year’s Feel Good Marketing Awards (FGMAs) looked very different from years before.
McDonald’s brought 900+ employees together in the metaverse.
To pull it off, McDonald’s partnered with Metaversed Consulting, which chose Odyssey, a high-fidelity pixel streaming platform. Together they created an incredible experience for McDonald’s employees that featured a two-part venue, a live stream on a virtual stage, Dolby audio effects, virtual McDonald’s swag, and more. At its culmination, the event totaled 1,800+ hours streamed from 85 different countries—and was nominated for a Webby Award in the category of Metaverse, Immersive & Virtual Best Audience Integration 2023.
Behind the scenes, thousands of NVIDIA GPUs, including the NVIDIA Quadro RTX 4000, NVIDIA RTX A4000, NVIDIA RTX A5000, and NVIDIA RTX A6000, powered up across the US, quietly powering a seamless metaverse experience for hundreds of streamers at the event.

## Odyssey Charts Its Own Path for Pixel Streaming
Pixel streaming platforms, like Odyssey, have three major concerns when considering their cloud infrastructure:
- It's too expensive.
- They can't access the GPUs in real time, forcing a decision to over-provision and spend an excessive amount of engineering resources to spin up compute well in advance of the event.
- They’re limited in the type of GPUs they can get on the large public clouds, which limits the performance they can expect out of the Unreal experiences they're building.
Most pixel streaming platforms operate in virtual machines, which is the traditional way of working with Unreal Engine, the game engine Odyssey used to build McDonald’s experience. At traditional cloud providers, Odyssey would have had to reserve GPUs in virtual machines, spin up instances well in advance, and keep them running. This substantially drives up the cost of hosting an event like what Odyssey and McDonald’s wanted to create, making these metaverse experiences far less accessible or financially viable.
What’s more, hundreds or thousands of streamers could join a metaverse experience at once. Virtual machines in a traditional cloud tech stack aren’t performance-optimized to provide GPU access in real time or handle large spikes in demand. In this scenario, if Odyssey didn’t have enough GPU capacity to support the number of attendees, latecomers to the event won’t be able to access the experience. And, Odyssey would have had more DevOps overhead to grapple with internally.
Odyssey sought a different path entirely—one that would give them access to scale, elasticity, and deployment flexibility without the high price point.

"By providing a large pool of open GPU resources that can be provisioned just-in-time, CoreWeave has given Odyssey the ability to deliver Unreal pixel streaming with a flexible payment model where users pay for only what they use."

— Maxime Long, CTO @ Odyssey
‍

### Commitment to Containerization
Odyssey partnered with CoreWeave to build and support their GPU infrastructure using containerization instead of virtual machines. The team worked closely with CoreWeave’s engineering team to re-imagine their deployments to make use of the elasticity, efficiency, and performance delivered by CoreWeave’s serverless Kubernetes structure.

"Odyssey committed themselves to using the CoreWeave platform in a way that enabled the most scale."

— Brian Venturo, Chief Technology Officer at CoreWeave
With CoreWeave, Odyssey could autoscale across thousands of GPUs in just seconds—without having to accumulate instances ahead of time to ensure enough compute for the event. And, because of CoreWeave’s pricing structure, Odyssey only paid for the GPUs used.

"Within 30 seconds of a user opening a link to the McDonald’s Odyssey space, they each had their own secure, unique, beautiful, high-resolution, 60 frames-per-second Unreal Engine-powered experience. This is only possible because of CoreWeave’s Kubernetes API and range of high-performance compute and storage options. To be clear — this is not possible on any other provider or platform we’ve seen or tried to date."

— Bram Horton, Systems Architect @ Odyssey

## A Metaverse First for a Major Brand
With their cloud infrastructure ready, Odyssey could focus on creating the cool elements and venue for the McDonald’s metaverse event.
The event held two firsts for the fast food brand: its first metaverse activation and the first time many attendees would be entering a 3D experience. Keeping both these in mind, Odyssey’s team and artists worked closely with Metaversed Consulting and McDonald’s to execute an event that aligned with the brand’s vision and gave attendees a breathtaking, user-friendly experience.

### Building the McDonald’s Venue
The groundbreaking event had to represent the future while still honoring the McDonald’s brand. Odyssey’s artists collaborated with Metaversed Consulting and McDonald’s to ensure the experience aligned with the brand’s guidelines and created a futuristic yet familiar venue for its employees.
Working in Unreal Engine, Odyssey created a two-part experience that mimicked the architecture of McDonald’s headquarters in Chicago, IL. Employees who attended the event started at the gold carpet entrance to the virtual headquarters that led them to the inside gallery. From afar, the gallery looked just that, but as attendees came closer to the award-winning work on the wall, they could interact with each project in more depth.
From inside, users could then teleport to the upper level, which featured custom virtual McDonald’s swag for their avatars to wear and a stage with a large screen behind. Attendees joined together here to watch two McDonald’s leaders give a live stream presentation of the award ceremony.
Here, Odyssey leveraged two immersive technologies to level up the 3D experience. The first was the in-app streaming integration, which created the look and feel of a live-stream event within the metaverse. The second was Dolby.io Spatial Audio, which allowed users to converse with each other in real time and adjusted the audio volume based on where the users stood in relation to the audio source. This position-based listing listening experience immersed each avatar in the event, furthering the real-life qualities of the 3D event.

### An Experience Created for Everyone
Odyssey’s user-friendly platform welcomed new streamers to the event by first giving everyone the ability to create their own avatar. The Odyssey platform included simple guides throughout the onboarding process and venue, so no user was left guessing how to interact with each other and the 3D elements.
Here are some of the elements attendees enjoyed at The Feel-Good Marketing Awards:
- A golden-carpet paparazzi style photo-op entrance
- Dolby.io Spatial Audio, immersing each avatar in a unique, position-based listening experience
- Custom level design using Unreal Engine, to showcase the architecture of McDonald’s Chicago headquarters
- Teleportation to the 10th floor, newly imagined rooftop stage
- Virtual custom McDonald’s swag
- A live-streamed, fully produced metaverse awards show
- Authentic conversation and engagement opportunities with people seated nearby during the awards show in real time
- Selfies with friends and co-workers from around the world
- Embedded video galleries, showcasing the nominated works
The front entrance of the two-part venue, which closely resembles the McDonald’s headquarters in Chicago, IL. Image courtesy of Odyssey.
The live stream period of the event featured two McDonald’s executives entering the stage through branded arches. Image courtesy of Odyssey.

## The Metaverse in GPUs
Behind the scenes of the McDonald’s FGMAs, Odyssey’s deployments were lighting up on CoreWeave Cloud. Taking advantage of the industry’s most responsive auto-scaling, delivered out-of-the-box on CoreWeave Cloud, the team’s cloud infrastructure adjusted with ease—consuming more compute power when needed and de-escalating as attendees dropped off.
The graphics below illustrate what was happening under the hood.
graphic shows GPU usage over time from October 31, 2022, through November 3, 2022
The chart above shows just how massive the spikes were in GPU usage for the event. The first group of spikes (occurring just before November 1) represents Odyssey’s test run for the event, which reached just under 2,000 GPUs in total. The next group of spikes (everything from the afternoon and evening of November 1), shows the total GPU usage from the McDonald’s FGMAs. The peaks represent the most compute-intensive moments from the event, such as users logging into the metaverse experience and the live stream, with the highest peak reaching around 2,500 GPUs.
graphic shows GPU usage over time from 6:00 p.m. to midnight on November 1
A close-up view (above) of the compute power behind the McDonald’s FGMAs shows just how quickly Odyssey needed to scale up their GPU capacity to meet demand. These spikes also demonstrate how quickly they scaled down usage during a segment of the event and post-event. This scale-to-zero ability helped Odyssey save costs by not running compute (or as much compute) when they didn’t need it.
graphic shows GPU usage over time from 5:30 p.m. to 6:00 p.m. on November 1
The last chart (above) takes an even closer look at how quickly Odyssey expanded its GPU capacity. As attendees joined the experience and explored the 3D venue (the time of the steepest incline in GPU usage), Odyssey burst across an average of 500 GPUs every five minutes.

"This is what we mean when we say we built CoreWeave Cloud for compute-intensive workloads. Our infrastructure design—plus Odyssey’s commitment to delivering best-in-class experiences —is what enabled their team to scale their compute so quickly and efficiently, which in turn helped them deliver the incredible experience they designed with McDonald’s."

— Brian Venturo, Chief Technology Officer at CoreWeave
On the right of the chart (above), Odyssey could see the type and number of GPUs used during the last time frame shown on the graph. By offering over 10 different NVIDIA GPU SKUs on-demand, CoreWeave could enable Odyssey to access the compute to meet the complexity of their workloads—and seamless scale between GPU types with a single deployment, as needed. Those NVIDIA GPUs include:
- NVIDIA Quadro RTX 4000
- NVIDIA RTX A4000
- NVIDIA RTX A5000
- NVIDIA RTX A6000

## Powering the Future of 3D Experiences
Odyssey continues to bring more major brands into the metaverse. On May 9-10, 2023, Odyssey exclusively hosted Ad Age’s Web3 Marketing Summit, an event that showcases what's next for brands in the metaverse, AI, the next generation of computing, and more. This two-day event took place exclusively on the Odyssey metaverse platform in its Naturedome with brand leaders from Coca-Cola, Chipotle Mexican Grill, and PepsiCo all taking to the virtual stage.
In early June, Odyssey announced its move out of beta and released a new model for accessing its social metaverse tools—making it easier than ever to sign up, explore, create, and engage with others in groundbreaking 3D experiences.
Looking ahead, Odyssey hopes to enable more people to explore the metaverse and launch their own 3D experience. And, its platform is designed to do just that. With pre-built templates and integrations with Unreal Engine, Odyssey helps new and beginner users experiment with the platform without having to code or download anything on their computers.
Learn more about Odyssey on their website or follow them on LinkedIn to see what extraordinary 3D experience they will create next.

## Read more case studies

See all customer stories

### General Intuition Scales World Model Training with CoreWeave ARENA

Learn More

### Cohere Accelerates Training of North, Agentic AI for Enterprise

Learn More

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
