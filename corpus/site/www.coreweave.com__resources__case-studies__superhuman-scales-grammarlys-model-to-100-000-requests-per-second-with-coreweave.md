# Superhuman Scales Grammarly Inference | CoreWeave Case Study

Source: https://www.coreweave.com/resources/case-studies/superhuman-scales-grammarlys-model-to-100-000-requests-per-second-with-coreweave

Announcement

Webinar

Podcast

GTC 2026

CoreWeave Forge is here: connect your AI loop and compound every improvement. Read more

Contact us

Resources

Case Studies

Superhuman Scales Grammarly’s Model to 100,000 Requests Per Second With CoreWeave

Superhuman Scales Grammarly’s Model to 100,000 Requests Per Second With CoreWeave

Industry
Software and SaaS

Headquarters
San Francisco, United States

Use Cases

AI inference

#### Ready to get started?

Contact Sales

1
min read

Copied

## Challenge
Grammarly’s correction model runs proactively in the background, so suggestions have to arrive fast enough for people to act on them, at high quality and low cost. Superhuman’s ML team runs about 50 services handling up to 200,000 LLM requests per second, with a 99.99% availability target. To protect that, it wanted a second source of GPU capacity that could keep pace.

## Solution
Superhuman deployed Grammarly’s grammar correction model on CoreWeave Dedicated Inference, using reserved GPU capacity and a configurable vLLM engine alongside its existing infrastructure. The team validated the deployment with production-like traffic and compared latency, errors, and outputs before shifting live requests. CoreWeave engineers worked with Superhuman to identify hotspots and improve ingress autoscaling, helping the deployment reach stable serving at 100,000 requests per second.

## Benefits
- Stable inference at high volume: The grammar correction model reached 100,000 requests per second on CoreWeave after the teams resolved bottlenecks exposed during testing.
- Diversified GPU capacity at competitive pricing: A separate serving cloud gives Superhuman an additional source of capacity without competing for GPUs on the same underlying cloud.
- Less infrastructure management, with control retained: Dedicated Inference handles cluster and instance management while allowing the team to configure vLLM and bring the metrics it needs into its own Grafana dashboards.

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
