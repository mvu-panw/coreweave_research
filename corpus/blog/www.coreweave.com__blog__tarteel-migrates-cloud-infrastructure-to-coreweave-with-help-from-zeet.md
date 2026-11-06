# Tarteel Migrates to CoreWeave with Support from Zeet

Source: https://www.coreweave.com/blog/tarteel-migrates-cloud-infrastructure-to-coreweave-with-help-from-zeet

Announcement

Webinar

Podcast

GTC 2026

CoreWeave Forge is here: connect your AI loop and compound every improvement. Read more

Contact us

### Tarteel AI leveraged Zeet to smoothly move its deployment from AWS to CoreWeave, translating to a 22% improvement in latency and ~56% cost reduction.
‍
For Tarteel, an AI-powered Quran app, switching from AWS to CoreWeave was a no-brainer.
Lured by the flexibility to choose from a broad portfolio of the latest NVIDIA GPUs, affordable pricing, and integration with deployment partner Zeet, Tarteel migrated its entire cloud infrastructure over to CoreWeave.

## Groundbreaking AI
Tarteel is an AI-powered Quran study app that helps 2B+ Muslims around the world practice and improve their relationship with their faith. The app is interactive and voice-guided, meaning users converse with it, much like they would with a teacher.
Tarteel follows along as users recite verses, highlighting the words as they’re said and flagging mistakes in real time. Users can also search the Quran and related texts in Arabic using their voice.
Tarteel corrects recitation (the eponymous use case of the app), sentence structure, detects incorrect word choices, and points out the distinctions between similar verses to help users understand context and aid in memorizing the Quran. 
With 3M+ downloads, a growing user base, and 250k+ audio hours transcribed per month, Zeet and CoreWeave are helping Tarteel hit its stride.

## Big Opportunity
Unsatisfied with legacy cloud offerings, including a lack of observability for workloads, an underwhelming GPU selection and an unoptimized solution for inference and production workloads, Tarteel saw multiple growth opportunities with CoreWeave.
CoreWeave offers clients tangible advantages over large legacy cloud providers, including out-of-the-box observability, the industry's broadest range of NVIDIA GPUs, responsive autoscaling, best-in-class support, excellent documentation, and seamless integration with Zeet.
CoreWeave gives Tarteel out-of-the-box observability with access to Grafana and Prometheus and offers a native S3 solution, which minimizes Tarteel’s cloud and data transfer costs.

## NVIDIA Riva & NeMo
Tarteel had experimented with various toolkits, but most were tailored for research or specific use cases, with poor inference latency and difficult-to-reproduce SOTA results.
“Many STT toolkits and libraries we explored failed to deliver on both the performance and accuracy requirements necessary to deliver our unique product experience. They also were not optimized for deploying models in a production environment.”
– Anas Abou Allaban, Co-Founder and CEO, Tarteel 
On CoreWeave, Tarteel can access NVIDIA’s Riva and NVIDIA NeMo toolkits. NeMo gave the team the ability to quickly train and fine-tune SOTA ASR and TTS models on Tarteel’s own data and custom hyperparameters. This allowed the team to maximize WER performance and achieve amazing results recognizing Quran recitation. 
The team then leveraged Riva to deploy NeMo models with Triton, delivering blazing-fast inference speeds compared to other frameworks. Riva also gave Tarteel the ability to modify the behavior of the models in production by adjusting parameters related to audio chunk size, padding, and Voice Activity Detection (VAD) to deliver the best end-user experience possible.  

## Post-Migration
With Riva and NeMo, Tarteel achieved real-time production performance and reproducible SOTA results by optimizing latency and streaming audio, and support for scaling AI model inferencing to multiple GPUs with NVIDIA Triton.
After migration, Tarteel recorded:
- ~1,600 requests/min. On average over 40 NVIDIA GPUs (A4000/5000s)
- 22% improvement in latency
- Median request latency: 423.5ms
- ~56% cost reduction
Tarteel plans to use NVIDIA’s SDKs and toolkits for new use cases like NLP and TTS.

## Can’t Beat Zeet
Tarteel uses Zeet to deploy services to multiple cloud providers in multiple regions (US, EU, AP).
Zeet made the migration to CoreWeave swift and simple, quickly resolving issues, like setting up load balancing and DNS, to ensure that migration time was minimal, at 1-2 days total.
“Zeet made the switch to CoreWeave a breeze. We had minimal downtime and did not need any K8s or CW expertise, we just clicked a few buttons and we were live.”
– Anas Abou Allaban, Co-Founder and CEO, Tarteel
Zeet made autoscaling and deploying incredibly straightforward. Without having to worry about deployments, Tarteel has been able to focus on improving its product and services.
“Just write a Docker container and your app is ready to be shipped on Zeet and CoreWeave. When you’re ready to scale, all you need is a few clicks to configure autoscaling or manually increase your replica count.”
– Anas Abou Allaban, Co-Founder and CEO, Tarteel 

## What’s Next for Tarteel?
As Tarteel continues to harness AI to help enrich Muslims' experience with the Quran, they seek to save ancient texts that are at risk of being lost to history and provide important context on verses of the Quran. 
“Our goal is to continue leveraging AI to deliver unique and personalized experiences for Muslims to better practice & engage with their faith. This includes experiences related to semantic search, Q&A (NLP), forecasting/spaced repetition to find the best chapter to recite/revise, and digitizing Islamic/Arabic literature.”
– Anas Abou Allaban, Co-Founder and CEO, Tarteel
Zeet and CoreWeave will be with them every step of the way to help deliver maximum value to their users.

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

CoreWeave Kubernetes Service (CKS),

Copy code

Copied!

CoreWeave Kubernetes Service (CKS),
