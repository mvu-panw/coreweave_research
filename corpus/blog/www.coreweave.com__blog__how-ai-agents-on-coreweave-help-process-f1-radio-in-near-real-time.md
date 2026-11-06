# AI Agents Decode F1® Radio in Near Real Time | CoreWeave Blog

Source: https://www.coreweave.com/blog/how-ai-agents-on-coreweave-help-process-f1-radio-in-near-real-time

Announcement

Webinar

Podcast

GTC 2026

CoreWeave Forge is here: connect your AI loop and compound every improvement. Read more

Contact us

It's lap thirty-two of the 2026 British Grand Prix. Forty radio channels are live. One is reporting debris on track. Another is discussing tire wear. A third is debating whether to pit the lead car.
Then the question lands: "Should we box for mediums or hards?"
Somewhere in those 40 channels, the answer exists. Drivers and engineers on 11 competitor teams have been talking about their tires for the last ten laps. Two cars on hards are struggling. Someone said so, clearly, twelve minutes ago. But nobody heard it, because nobody can monitor 40 channels and run a race at the same time.
That's the problem CoreWeave and Aston Martin Aramco set out to solve.

## The challenge: too much audio, too little time
Every Formula 1® team has legal access to competitor radio channels. In theory, that's a significant intelligence advantage. In practice, it's an ocean of noise with no reliable way to find what matters before the pit window closes.
At the 2026 Monaco Grand Prix, over 380,000 words were spoken across radio channels over race weekend: over 50 hours of audio containing more than 21,000 individual messages. Useful information is in there, including competitor tire feedback, strategy signals, driver complaints, and engineering observations. All of it legally available. Almost none of it accessible fast enough to act on during the race.
Before this project, answering a question like "how are other drivers finding the medium tire?" meant pulling an engineer off other duties to manually monitor channels and trawl through transcriptions mid-race. That process could take several minutes. In a sport where a pit stop window opens and closes in under thirty seconds, that's too slow to be useful.
Keyword search doesn't solve it either. A driver saying "struggling for grip" tells you something, but only when you know what tire they're on, how many laps those tires have done, and what conditions they're running in. Connecting those data points by hand, mid-race, under pressure, is exactly the kind of task that breaks down when it matters most.

### Why F1® audio is so hard to transcribe accurately
The audio itself is a problem. F1® radio is hostile to standard transcription models: engine noise, helmet acoustics, 300km/h wind, multilingual drivers, and team-specific shorthand that no generic transcription model is trained to parse.
Here's a real example from race weekend. One transmission, transcribed by the model: "I need to manage the tire overheating." One missed word — overheating instead of over racing — and you've gone from worthless noise to a car in trouble.

### The solution: a real-time AI radio intelligence platform
In October 2025, CoreWeave engineers embedded with Aston Martin Aramco on site alongside race engineers during live race weekends. The goal was to build something that could do what no engineer could: monitor every channel, extract what matters, and surface it fast enough to change a decision on race day.
The platform has two modes.
The first covers the 22 competitor channels. Every transmission is transcribed, categorized by topic—tires, strategy, grip, energy management—and surfaced in a searchable interface that updates as the race runs. An engineer who needs to know how the field is finding the hard tire can find out in seconds, not minutes.

#### From cockpit chatter to pit wall decision in seconds
The second covers Aston Martin Aramco’s own internal channels. Driver feedback, engineering communications, session notes: all captured, indexed, and searchable in one place for the first time. If a driver says "I had a lot more understeer compared to FP1" mid-session, that observation is logged, timestamped, and tied to the car setup data from that session. No dedicated note-taker required, nothing lost in the noise.
On top of both modes sits a natural language chat interface. A race engineer types "what are the Ferraris saying about tire deg?" and gets a synthesized answer drawn from live audio in seconds. The same interface works after the race for deeper analysis and debrief.
Back at Silverstone, lap thirty-two. The question is mediums or hards. An engineer pulls up the platform, filters by tire compound, and sees that two cars on hards have been reporting grip issues for the last eight laps. The call takes seconds. The car pits for mediums.
That's what this is built for.

### The engineering challenge: 40 channels, sub-five-second reaction time
Managing 40 high-fidelity audio streams without drops is a serious data orchestration challenge. Doing it with a sub-five-second reaction time requires infrastructure that most cloud environments simply weren't built to handle.
The numbers behind the build reflect how seriously the team took the problem:
- 75 model iterations before the transcription model reached production accuracy
- 7 hours of F1® radio data hand-annotated by the team
- Over 3,000 labeled samples built specifically to reflect real race conditions
- 40 channels processed simultaneously, with full transcription, diarization, and topic categorization within five seconds of capture
Evaluated using Weights & Biases Weave, the fine-tuned model hit production-grade accuracy on both word error rate and LLM-based quality scoring. The tire overheating example above isn't an edge case. It's the kind of difference that shows up across thousands of messages every race weekend.
The system ran in the final two races of the 2025 season, Qatar and Abu Dhabi, as a live test. Full deployment followed for the 2026 season.

## How CoreWeave Cloud makes it possible
The performance requirements here are unforgiving. Decisions in seconds. Forty simultaneous streams. No drops. The infrastructure has to work every lap of every session, not just in benchmarks.
CoreWeave and Aston Martin Aramco are building on an AI cloud platform purpose-built for AI at scale. This AI cloud provides the compute foundation this use case demands. Weights & Biases Serverless Inference, running on CoreWeave Kubernetes Service, handles the inference stack, with TensorRT-LLM delivering the throughput and latency the use case demands.
Fine-tuning ran on CoreWeave, with Weights & Biases managing experiment tracking and dataset versioning throughout. Every iteration of the 75-model development process was tracked, evaluated, and versioned before the team committed to a production build.

## What it means beyond race day
When the race weekend ends, the platform keeps working. Every message from every session, competitor and internal, is indexed and retained. Engineers run post-race analysis, review strategic decisions with full audio context, and build institutional memory that persists across the entire season.
The question that used to require hours of manual audio review now takes seconds to answer: "what happened on the radio in the final ten laps at last year's British Grand Prix?" That kind of recall changes how teams prepare, debrief, and develop the race strategy instincts that compound over a full season.
Formula 1® has always been a sport decided at the margin. Tenths of a second. A tire compound call. A pit stop timed one lap earlier than the competition. AI inference infrastructure built for this kind of real-time F1® data analysis is what makes those margins smaller. CoreWeave and Aston Martin Aramco are building it together, one race weekend at a time.
Explore how CoreWeave combines the tools, teams, and technology required to build physical AI systems, from large-scale simulation and model training to deployment and validation.
Join Aston Martin Aramco Formula 1 team and other top AI pioneers at Fully Connected 2026 to learn how to accelerate the superintelligence loop.

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

Inference,

Copy code

Copied!

Inference,
