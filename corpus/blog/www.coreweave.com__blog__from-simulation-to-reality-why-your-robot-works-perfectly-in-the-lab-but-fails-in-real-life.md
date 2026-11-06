# From Simulation-to-Reality for Robotics

Source: https://www.coreweave.com/blog/from-simulation-to-reality-why-your-robot-works-perfectly-in-the-lab-but-fails-in-real-life

Announcement

Webinar

Podcast

GTC 2026

CoreWeave Forge is here: connect your AI loop and compound every improvement. Read more

Contact us

Originally published on the Weights & Biases by CoreWeave blog on May 31, 2026.
You've trained a self-driving model. It drives flawlessly with perfect lane changing, smooth acceleration, and zero accidents. You're ready to deploy it into the real world. Within seconds, it crashes.
What happened? The simulation gave you perfect road surfaces, no wind, instant brake response, and zero sensor lag. Reality threw potholes, gusts of wind, brake fade, and noisy GPS signals at your AI. Your model learned to drive in a world that doesn't exist.
This is the robotics version of "It works on my machine."
In machine learning robotics, we train robots in physics simulators for good reason. Real robots are expensive (a research robot can cost $10,000 to $100,000), you can run millions of training attempts overnight, and when the robot falls, nothing breaks. But here's the catch: simulators lie. They model an idealized world with perfect physics, zero noise, and instant responses. When you deploy that "perfect" AI to real hardware, the real world's messiness breaks everything.

## What will I learn in this tutorial?
In this tutorial, you'll learn four critical skills. 
- First, how to train a robot to walk using reinforcement learning, specifically an algorithm called PPO. 
- Second, how to detect hidden problems that standard metrics completely miss, like motor destroying vibrations. 
- Third, how to make your AI robust enough to handle varied real world conditions including different floors, temperatures, and wear and tear. 
- Fourth, how to track everything using Weights & Biases so you actually understand what's happening.
By the end, you won't just have a robot that walks in simulation. You'll have one that might actually survive first contact with reality.
No prior robotics experience needed. We'll explain everything as we go.

## Why can't I just program the robot directly instead of using machine learning?
You might wonder: "Why use machine learning at all? Can't we just program the robot directly?"

## What's wrong with traditional control methods?
For decades, engineers used something called PID controllers (Proportional Integral Derivative... fancy name, simple concept). Think of it like cruise control in a car. You set a target speed, the controller constantly adjusts the throttle to maintain it, adding more gas if you go uphill and reducing it downhill.
This works great when the environment is predictable (like smooth highways), when you can write explicit rules (if speed drops, add throttle), and when physics is simple with linear relationships. But what about a robot walking on gravel?
Suddenly, you need rules for how each footstep changes friction, how the ground deforms under weight, how all four legs coordinate when one slips, and how to balance when the surface tilts unexpectedly. You'd need thousands of rules, and you'd still miss edge cases.

## How does machine learning solve this problem?
Instead of writing rules, we show the robot what success looks like (walking forward without falling) and let it figure out the "how" through trial and error... millions of attempts in simulation. Think of it like learning to ride a bike. No one gave you equations for balance. You tried, fell, adjusted, tried again. Eventually, you learned without consciously understanding the physics. That's what we're doing with the robot.

## What exactly is this "sim to real gap" everyone talks about?
Here's where things get real (pun intended).

### Why do simulators fail to match reality?
In a simulator, you can press "reset" when the robot falls with no damage. Your sensors are perfect with no noise in measurements. Motors respond instantly with no mechanical delays. Friction stays consistent because the floor never changes. Temperature effects don't exist because motors never overheat. And physics is deterministic... the same action produces the same result, always.
Reality? A fall might cost $5,000 in repairs. Sensors are noisy with GPS drift and camera blur. Motors have 10 to 50 millisecond lag. Friction varies wildly across wood, carpet, and wet floors. Motors heat up and weaken over time. And physics is messy... the same action definitely doesn't equal the same result.

### What's the worst that can happen when I deploy my sim-trained robot?
Here's what actually happens when you deploy a simulation trained robot. Your training graph shows Episode 1 with a reward of negative 100 (terrible), Episode 100 at 0 (learning), and Episode 300 hitting 100 (success!). You think: "Amazing! The robot learned to walk!"
Then you deploy to hardware. Motors start vibrating rapidly. Within 30 seconds, they're burning hot. The robot hasn't moved forward at all. You just shortened the motor lifespan by 100 hours.
What went wrong? Your AI discovered it could "trick" the simulator by vibrating its legs at high frequency. The simulator's simplified physics allowed this to generate forward motion. The reward went up. The graph said "success." But real motors can't vibrate at 100 Hz. They just draw maximum current, overheat, and don't produce useful motion.
💡 The lesson: Reward going up does not equal a usable solution.

### Should I just make my simulator more realistic?
You might think: "Let's make the simulator more realistic!" That doesn't work because you'd never capture all of reality's complexity, your AI would just overfit to your improved simulator, and perfect simulation is impossible (and would be too slow anyway).
Instead, we use a clever trick called: Domain Randomization (training in chaos).

### How does training in chaos help my robot work in reality?
Here's the driving analogy. If you only practice driving on sunny days on an empty highway, you'll crash in the rain or heavy traffic. But if you practice in rain, snow, fog, and sunshine, in both heavy traffic and empty roads, in different cars (sedan, truck, sports car), and on various road conditions (smooth, potholed, gravel), you become a robust driver who handles anything.
For robots, we do the same thing:
Every single training episode, we randomly change several things. Gravity varies between negative 12 and negative 8 meters per second squared, which simulates different motor strengths. Floor friction changes between 0.5 times and 2.5 times normal, simulating everything from carpet to tile to ice. Motor power fluctuates between 80% and 120%, simulating manufacturing variation and battery drain. We add random sensor noise to all measurements, simulating real sensor imperfections.
# Every time the robot resets, we randomize the environment
def reset_environment():
 # Make gravity weaker or stronger (affects how hard it is to stand)
 gravity = random_value_between(-12, -8)
 
 # Make the floor more or less slippery
 floor_friction = random_value_between(0.5, 2.5)
 
 # Make motors weaker or stronger
 motor_power = random_value_between(0.8, 1.2)
 
 # Add noise to sensors (simulates real world measurement errors)
 sensor_noise = random_value_between(0.0, 0.05)

The result is that the AI learns to walk in ALL these conditions, so the real world is just another variation it's already seen. Yes, training takes 2 to 3 times longer, and peak performance in "ideal" conditions is slightly lower. But when real world conditions change, performance drops only 20% instead of the 80% or more drop you'd see without randomization.

### If reward is going up, isn't that enough? Why do we need other metrics?
This is the trap that destroys most robotics projects. Standard machine learning tracks one number: reward (how well the AI is doing). For robotics, one number is dangerously insufficient.

### What other metrics should I track besides reward?
Think of it like monitoring a car. The speedometer (reward) tells you one thing, but you also need a tachometer (engine RPM), temperature gauge, and oil pressure. If RPM is redlining or temperature is maxed, your speed doesn't matter. You're about to destroy the engine.
- firstly, For robots, we track Action Smoothness. Are motors moving smoothly, or jittering? This is like measuring engine vibration. Jittering equals mechanical wear and eventual failure. We target less than 0.1, with lower being better.
- Secondly, We monitor Average Torque. How hard are motors working on average? Like measuring average engine load, too high means overheating and energy waste. We target 0.3 to 0.6 for balanced effort.
- Thirdly, Peak Torque tells us if there are sudden force spikes. Like measuring peak engine load during acceleration, spikes create shock loads that damage gears. We target less than 0.9 to avoid saturation.
- Finally, Action Distribution shows how motors are being commanded. A healthy pattern shows a smooth, bell curve distribution with gradual movements. An unhealthy pattern has spikes at extremes, indicating bang bang control that's harsh on motors.

Motor health metrics: Action smoothness drops from 1.1 to 0.535 over training, showing the AI learned gentler motor control

## How do I actually build and train a walking robot? (Step by Step)
The equipment and software You'll need are a laptop (Mac, Windows, or Linux work fine... we'll use a Mac M4 in this tutorial), about 20 minutes of training time per experiment, and basic Python knowledge for running scripts. No robot required! We'll simulate everything.

### Which robot environment should I use for learning?
We're using a premade simulation called BipedalWalker v3. It's a simple 2D robot with two legs (four joints total: two hips, two knees) and 24 sensors tracking position, velocity, and ground contact. The goal is straightforward: walk forward without falling.
Why this environment? It works right out of the box with no custom robot models, trains fast (just 3 minutes on a laptop), demonstrates all the problems we're discussing, and is completely free and open source.
import gymnasium as gym

# Create the walking robot environment
# render_mode="rgb_array" means headless (no window), important for macOS
env = gym.make("BipedalWalker-v3", render_mode="rgb_array")

# The robot can control 4 joints (2 per leg)
print(env.action_space)
# Output: Box(-1.0, 1.0, (4,)) 
# This means: 4 numbers between negative 1 and 1 (motor commands)

# The robot sees 24 sensor values
print(env.observation_space)
# Output: Box(..., (24,))
# This means: 24 numbers (angles, velocities, ground contact, etc.)

### Experiment 1: What happens when I train without any safety considerations?
Let's start by training a robot the "normal" way. Just maximize reward with no safety considerations.
How do I run a basic training session?
Copy paste this on your terminal
# Train for 300,000 steps (roughly 3 minutes on M4 Mac)
python train_walker.py \
 --timesteps 300000 \
 --run_name baseline_no_safety

#### What results should I expect from naive training?
The good news? Reward climbs from negative 100 to 211. The robot learns to walk! Training completes in just 3 minutes. But there's a hidden problem lurking beneath these impressive numbers: action smoothness hits 0.615, meaning motors are jittering 61.5% more than ideal. In real hardware, this translates to shortened motor lifespan, noise, and instability.
Episode 100 videos: Baseline (211 reward) walks successfully, but notice the slight jitter in leg movements... invisible in reward metrics but deadly to real motors

#### Why don't standard metrics catch these problems?
Your training dashboard proudly displays a reward of 211 (excellent!), an episode length of 300 steps (didn't fall!), and a "Training Complete" status. But it doesn't show motor vibration at 61.5% above safe threshold, or that this would damage hardware in less than one hour.
💡 Lesson 1: Reward alone is a lie for robotics.

#### Experiment 2: Does domain randomization actually improve my robot's performance?
Now let's make training harder by randomizing the environment.
How do I add domain randomization to my training?
python train_walker.py \
 --timesteps 300000 \
 --domain_randomization \
 --run_name full_pipeline_safe

### What changes when I randomize the training environment?
During training, every episode randomly changes gravity (simulating different motor strengths), floor friction (simulating different surfaces), motor power (simulating manufacturing variation), and adds sensor noise (simulating real sensors).
Domain randomization in action: Gravity, friction, and motor power fluctuate every episode, forcing the AI to learn robust strategies

### Will domain randomization hurt my robot's performance?
We expected performance to drop since the task is harder now. What actually happened shocked us: reward increased to 247, a 17% improvement over baseline! The robot walks better WITH randomization.
Why? The baseline was overfitting, like a student who memorizes one test but fails when questions change slightly. With randomization, the AI had to learn general strategies that work in ALL conditions, which happens to work better even in the "average" case.
Surprise finding: Domain randomization improved performance! Baseline equals 211, Full pipeline equals 247 (plus 17%). Randomization prevented overfitting to the fixed environment.

#### Experiment 3: How do I stop my robot from destroying its own motors?
Domain randomization improved performance but actually made jitter worse. The baseline had 0.615 smoothness, but with domain randomization it jumped to 0.714. Time to explicitly penalize jerky movements.
What's a smoothness penalty and how does it work?
We modify the reward the AI receives:
# Original reward (from environment)
reward = distance_traveled - energy_used

# Add penalty for rapid changes in motor commands
if previous_action exists:
 change = |current_action - previous_action|
 penalty = 0.05 * change # 0.05 is the penalty strength
 
# New reward (what AI actually sees)
final_reward = reward - penalty

In plain English: "I'll give you points for walking forward, but I'll subtract points every time you change motor commands too quickly." The AI learns that smooth movements equal more reward.
How strong should I make the smoothness penalty?
We tried a light penalty of 0.01 first:
python train_walker.py \
 --domain_randomization \
 --smoothness_penalty 0.01

It didn't work! Smoothness got WORSE, hitting 0.714. The penalty was too small to matter, so the AI ignored it and prioritized performance.
Then we tried a strong penalty of 0.05:
python train_walker.py \
 --domain_randomization \
 --smoothness_penalty 0.05

Success! Smoothness improved to 0.535, a 25% reduction in jitter. But this came at a cost... reward dropped to 59, a 76% performance decrease.
Motor smoothness over training: Light penalty (pink) didn't help, but strong penalty (orange) successfully reduced jitter from 1.1 to 0.535, though at cost of lower performance

### Should I choose high performance or motor safety?
Let's see the complete picture:
Summary Table

### Which policy should I deploy to my expensive robot?
For a $10,000 robot, Policy 1 (247 reward, 0.714 smoothness) walks really well... for 30 seconds. Then motors overheat. You just damaged $2,000 in servos.
Policy 3 (59 reward, 0.535 smoothness) walks slower and less impressively, but runs for hours without issues. Motors stay cool and last years.
Which would you choose? For real deployment, you choose the safe one, even if it's less impressive on paper.
Side by side comparison at Episode 100: Notice the smoother, more deliberate movements in strong_smoothness (59 reward) vs the energetic but jittery baseline (211 reward). Visual evidence supports our quantitative smoothness measurements.

### How do I track all these metrics without going crazy?
Throughout this tutorial, we've been logging everything to Weights & Biases (W&B). Think of it as Git plus logging plus monitoring for traditional software, but for machine learning, it's all of the above combined with experiment tracking and visualization.

### What does Weights & Biases actually give me?
- Automatic Experiment Tracking means every training run logs hyperparameters (penalty strength, randomization ranges), metrics (reward, smoothness, torque), videos (actual robot behavior), and system stats (GPU usage, training time).
- Real Time Dashboards let you watch while training happens. You see reward curves updating live, motor health metrics updating live, and warning alerts if metrics go bad.
- Experiment Comparison becomes trivial after training. You can plot all three experiments on one chart, see exactly which configuration worked best, and share results with collaborators.
- Reproducibility is built in. W&B logged every parameter, so you can recreate the exact same run, and collaborators can reproduce your work.

### What should I look for in my W&B dashboard?
Complete W&B dashboard: Domain randomization (top), motor safety metrics (middle), and video recordings (bottom)... all tracked automatically
‍
The top row shows domain randomization: how gravity, friction, and motor power varied throughout training. This confirms randomization is actually happening and helps debug if something goes wrong.
The middle row displays motor health through action smoothness (the critical safety metric), average torque (energy efficiency), and peak torque (damage prevention).
The bottom row captures videos of actual robot behavior every 50 episodes. This catches problems invisible in metrics and provides the "ground truth" verification you need.

## What are the key takeaways from this tutorial

### What were the main problems we solved
Simulators lie because perfect physics doesn't exist in reality. Reward is insufficient: high scores can hide deadly behaviors. Overfitting happens when AI learns simulator quirks instead of general skills.
What solutions actually work in practice?
Domain Randomization trains in varied conditions to build robustness. Hardware Aware Metrics track what actually matters for real robots. Safety Penalties explicitly discourage harmful behaviors. Comprehensive Logging through tools like W&B lets you see everything.
What's the one insight that changes everything?
The "best" AI model isn't the one with the highest reward, the fastest training, or the most complex architecture. The "best" AI model is robust to real world variation, safe for hardware, and actually deployable.

### Where can I find the code and start experimenting
Complete code is available at GitHub under rl sim2real tutorial and you can view our experiments at the W&B Project dashboard.
Setup takes just 5 minutes
git clone https://github.com/your-username/rl-sim2real-tutorial
cd rl-sim2real-tutorial
pip install -r requirements.txt
wandb login
python train_walker.py --timesteps 300000

#### What should I do before deploying to real hardware?
Before deploying to hardware, follow this checklist. Train with strong domain randomization. Add safety penalties for your specific motors. Verify smoothness metrics in simulation. Start with 50% motor power in reality. Have an emergency stop button ready. Monitor motor temperatures continuously.
Reality will still surprise you, but you'll be prepared.

### Why does this approach matter more than traditional robotics methods?
The traditional approach to robotics follows a painful cycle: train AI in simulation, get high scores, deploy to hardware, watch it fail, and repeat (if hardware survived).
The approach you just learned is different. You train AI in varied conditions, track what actually matters, build safety into training, verify with multiple metrics, and deploy with confidence.
The difference? Traditional says "It worked in simulation!" and breaks in 30 seconds. Our approach says "It's robust and safe" and works reliably for hours.
That's the difference between research demos and deployable robots.
Code: GitHub | Experiments: W&B Dashboard
‍
‍
‍

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

CoreWeave Forge,

Copy code

Copied!

CoreWeave Forge,
