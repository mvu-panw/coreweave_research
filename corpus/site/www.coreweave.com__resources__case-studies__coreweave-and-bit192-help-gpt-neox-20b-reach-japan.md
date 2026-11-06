# CoreWeave and Bit192: GPT-NeoX-20B in Japan | Bit192 Case Study

Source: https://www.coreweave.com/resources/case-studies/coreweave-and-bit192-help-gpt-neox-20b-reach-japan

Announcement

Webinar

Podcast

GTC 2026

CoreWeave Forge is here: connect your AI loop and compound every improvement. Read more

Contact us

Resources

Case Studies

CoreWeave and Bit192 Help GPT-NeoX-20B Reach Japan

CoreWeave and Bit192 Help GPT-NeoX-20B Reach Japan

Industry
AI native company

Headquarters
Japan

Use Cases

AI inference

AI model training

Fine-tuning

#### Ready to get started?

Contact Sales

5
min read

Copied

How Bit192, Inc. used CoreWeave's GPU cloud to bring large-scale Japanese NLP models to life

What began as a small office creating contract work for Japanese publishing houses, has quickly become one of the few Japanese companies investing in open-source AI.
Yasu Seno, CEO of Bit192, Inc., grew interested in the power of AI because of his love and fascination with video games. Yasu is an avid follower of the video game writer and designer and Game Developers Conference founder, Chris Crawford, who pushed the boundaries of interactive storytelling through games like Balance of Power and Legacy of Siboot.
Bit192, Inc. has recently released cutting edge NLP ideas like prompt/adapter tuning and entropy sampling in Japanese and they are preparing to serve the latest multimodal AI, including diffusion model image generation with Japanese CLIP.

## A 20-Billion Parameter Japanese Model
Yasu and Bit192, Inc. are currently working to train a new 20B-parameter Japanese model from scratch, independent from GPT-NeoX-20B, and using a slightly modified GPT-NeoX codebase.
The big challenge for Yasu is the lack of refined, adequately-sized, publicly trained datasets and validation datasets. There are plenty of high-quality English datasets, like The Pile, and curated validation datasets such as HellaSwag, Winogrande and LAMBADA, so Yasu and Bit192, Inc. have set out to create sets of this quality for Japan.

Yasu began by crawling the internet, scanning ebooks, and de-noising and normalizing the large and extremely noisy C4-Japanese datasets provided by Google. Yasu has also built his own validation dataset for creative writing, which consists of about 1.5GB of professionally written ebooks.
Yasu and Bit192, Inc. have refined their models to reflect the language-specific attributes of Japanese. Normalization has been especially important, as Japanese has many variations for commonly used symbols. Without a proper normalization, the model would not be able to generalize.
Additionally, because the Japanese language is ideographic and can be more repetitive than English, Bit192, Inc. is working on both tokenization and pre and post processing to improve performance.

## Bit129 + CoreWeave
After not finding much success with previous cloud providers, Bit192, Inc. discovered CoreWeave through the EleutherAI community. The availability and reliability of CoreWeave’s cloud infrastructure service not only made it possible for Bit192, Inc. to serve their current models, it also allowed them to continuously build and test new ideas in NLP and image generation.

“The availability and reliability of CoreWeave’s service allowed us to serve our current models and continuously build and test new ideas.”

— Yasu Seno, CEO Bit192, Inc.
Knowing that they can continuously innovate without being limited by uncontrollable supply issues has been a game changer for Bit192, Inc. as they serve their 400k unique users per month, 24/7.
Bit192, Inc. has employed CoreWeave’s NVIDIA A40 GPUs for flexibility and the ability to continuously evaluate the process and outputs during training runs. While most companies default to NVIDIA A100 GPUs for distributed training workloads, after some experimentation, Bit192 was able to achieve the performance needed to train models of the same quality and take advantage of CoreWeave Cloud's massive A40 deployment.
CoreWeave gives Yasu access to the largest fleet of NVIDIA A40 GPUs in North America. The NVIDIA A40 is the world’s most powerful data center GPU for visual computing, giving VFX studios, data scientists, and engineering teams the ability to render, process, and analyze faster than ever.
Incredible training and inferencing performance, combined with enterprise-class stability and reliability, make NVIDIA A40-powered servers ideal for professional AI deployments and the A40’s 336 third-generation Tensor Cores vastly accelerate AI workloads.
As NVIDIA’s first Elite Cloud Services Provider for Compute, CoreWeave is able to leverage the latest generation of NVIDIA GPUs and enable companies like Bit192, Inc. to run incredibly compute-intensive workloads.

“The availability and reliability of CoreWeave’s service allowed us to serve our current models and continuously build and test new ideas.”

— Yasu Seno, CEO Bit192, Inc.
“NVIDIA A40 GPUs are an evolutionary leap forward in performance and multi-workload capabilities, with powerful compute and AI acceleration to meet today’s most creative challenges,” said Dave Salvator, Senior Manager in the Accelerated Computing Group at NVIDIA.
The Tensor Float 32 (TF32) precision provides up to 5X the training throughput  over the previous generation to accelerate AI and data science model training without requiring any code changes, hardware support for structural sparsity doubles the throughput for inferencing and second-generation RT Cores deliver massive speedups for photorealistic rendering used in film, architectural design and product development.

## AI Novelist
Bit192, Inc. has recently released a new project called AI Novelist.
Originally invented as a chatbot engine for the new game Starbirth, Yasu wondered if the AI powered engine might also act as a writing assistant as he and his team worked to develop the Starbirth plot.
The engine was a huge help and Yasu decided to share the engine with a handful of friends, who also found it incredibly helpful for sparking creativity across various projects. Based on the stellar feedback, Yasu and Bit192, Inc. released the engine under the name AI Novelist.
Professional writers and editors across Japan currently use the service, as do streamers and casual users who use AI Novelist to help create everything from stories about their interests to fresh haikus.
“I demoed the service for my grandmom – who is in her 90’s – and when I showed her that AI Novelist can generate a haiku, she was excited, which made me feel incredibly fulfilled.” – Yasu Seno, CEO Bit192, Inc.

## The Future
Yasu and Bit192, Inc. see a developing consumer-grade AI market, which, they believe, in a few years will be massive. They are hoping to spark a community-driven supernova of AI innovation in Japan and beyond.
Bit192, Inc. is working hard to put high-end AI in the hands of consumers and working professionals in a variety of fields, including gaming and interactive storytelling.
Eventually, Yasu believes that innovations shared and built in-community by AI companies and enthusiastic consumers will create huge opportunities.
Japanese NLP is still in its infancy and Yasu believes exciting changes are on the horizon, including a consumer-grade AI that might one day fit into smartphones and home computers, adapted and fine-tuned to each user’s preferences.
As AI continues to grow and expand across Japan, CoreWeave and Bit192, Inc. will be there to keep pushing the boundaries of what is possible.
‍

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
