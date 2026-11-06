# Kimi K3: Claude Clone or a New Kind of Model?

Source: https://www.coreweave.com/blog/kimi-k3-a-claude-clone-or-something-else

Announcement

Webinar

Podcast

GTC 2026

CoreWeave Forge is here: connect your AI loop and compound every improvement. Read more

Contact us

Originally published on the Weights & Biases by CoreWeave blog on July 26, 2026.
On July 16, 2026, Moonshot AI released Kimi K3, a 2.8 trillion-parameter open-weight model that became the most debated release of the year within days. Kimi K3 is the first open model to reach 2.8 trillion parameters. Demand overwhelmed Moonshot's compute capacity, and the company suspended new subscriptions 48 hours after launch. On July 22, the director of the White House Office of Science and Technology Policy posted on X that his office had information Moonshot distilled Anthropic's Fable model to build K3, using a purpose-built internal platform that rotated access methods to evade detection. Treasury Secretary Scott Bessent floated sanctions. Moonshot denied it.
Then Moonshot did something that changes the shape of the argument: it released the weights on schedule and published a full technical report covering architecture, pre-training, post-training, infrastructure, and evaluations. Reports are not proof of provenance, and a lab that wanted to hide external teacher data would not document it. But the report is a large, specific, falsifiable artifact, and it contains a post-training pipeline that explains most of K3's capability jump without invoking Claude at all. It also, read carefully, explains why K3 sometimes feels like Claude.

## What we know about Kimi K3
Architecture breakdown: Kimi-K3 Technical Report
Kimi K3 is a natively multimodal Mixture of Experts model with 2.8 trillion total parameters and 104.2 billion activated per token, 93 layers, a 160K vocabulary, and a context window of up to 1 million tokens. Three architectural ideas carry the design:
- Hybrid attention. Each block stacks three Kimi Delta Attention (KDA) layers followed by one Gated MLA layer, a 3:1 ratio repeated through the backbone, with a final Gated MLA layer ensuring the last layer performs global attention. KDA extends the delta-rule recurrence with a channel-wise forget gate. K3's change over the earlier Kimi Linear formulation is a scaled sigmoid that bounds the log-decay from below at a fixed floor, which keeps the reciprocal rescaling factor inside the BF16 dynamic range and lets every causal tile run as a dense Tensor Core matmul. That removes the position-pair diagonal path that had been the intra-chunk bottleneck.
- Attention Residuals. Instead of accumulating everything into one hidden state across depth, each layer applies a learnable pseudo-query over the embedding and preceding block outputs, so a layer selectively retrieves from earlier representations. The full form costs O(L²d) arithmetic, which is affordable at fewer than 100 layers, but the O(Ld) memory is not, so K3 uses Block AttnRes: 8 blocks of 12 layers, dropping memory and cross-stage communication to O(Nd).
- Stable LatentMoE. Routed experts operate in a compact latent space while two full-width shared experts handle common transformations, which makes 896 routed experts with 16 active per token (sparsity 56) affordable. At that sparsity two failure modes appear, and the report names both: exploding activations in the routed branch, addressed with an RMSNorm before the up-projection plus a new activation called SiTU-GLU that smoothly caps both branches of the gated unit; and load balancing across nearly a thousand experts, addressed with Quantile Balancing, which sets each expert's bias from the router-score quantile matching its target load rather than nudging it with a signed fixed step.
Since the model 1M context, Positional encoding needs to be studied too. K3 applies No Position Encoding to all MLA layers and lets the KDA recurrence carry position implicitly, which means the model extrapolates to 1M tokens with no RoPE rescaling or YaRN interpolation. Context grew through a four-stage curriculum, 8K to 64K during pre-training and 256K to 1M during cooldown. 
Two more details matter for anyone planning to serve the weights:
- Quantization-aware training runs from SFT onward with MXFP4 expert weights and MXFP8 activations, and rollout and training share the same quantization scheme during RL, eliminating the train-inference mismatch. 
- The vision tower, MoonViT-V2, is a 27-layer, roughly 0.4B parameter encoder trained from scratch with next-token prediction rather than initialized from a contrastively pre-trained checkpoint like SigLIP.

### Kimi-K3 benchmarks and pricing
K3 ranks first on four of the twelve benchmarks shown in the K3 technical report: ProgramBench at 77.8, SWE-Marathon at 42.0, BrowseComp at 91.2, and AutomationBench at 30.8. It finishes second on Terminal-Bench 2.1 at 88.3, FrontierSWE at 81.2, Kimi Code Bench 2.0 at 72.9, JobBench at 54.3, and CharXiv at 91.3. K3 also ties GPT-5.5 on Zerobench at 41.0.
K3’s weaker results are DeepSWE, where its 67.5 trails GPT-5.6 Sol at 73.0 and Fable 5 at 70.0, and GDPval-AA v2, where its 1668 Elo trails Fable 5 at 1747 and GPT-5.6 Sol at 1736. The overall pattern is clear: K3 does not dominate every category, but it remains near the top across coding, browsing, automation, and visual-agent evaluations. All results shown use each model’s maximum or high reasoning effort.
Benchmarks breakdown: Kimi-K3 Technical Report
Cost is where the gap inverts, with one caveat. On Moonshot's internal Kimi Code Bench 2.0, K3 sits 4.0 points behind Fable 5 at 38% of the cost, and at high effort, it matches Claude Opus 4.8's maximum-effort score at roughly a third of the cost. On BrowseComp, it takes the top score at $2.03 per task, half the cost of GPT-5.6 Sol, and an order of magnitude below the Claude models at max effort. API pricing is $0.30 per million cache-hit input tokens, $3.00 cache-miss, $15.00 output.
Generated using ChatGPT Create Images from Model Pricing docs

## Using the K2 line as a reference point
K3’s broader capabilities and stronger agent performance make it a substantial leap beyond K2.7. Architecturally, K2.7 was still fundamentally a K2 model. It retained the same 61 layer MoE backbone with 384 routed experts, MLA attention, SwiGLU activations, and a 128K context window. K3, released barely a month later, is a ground up redesign: 93 layers, 896 routed experts, hybrid KDA and MLA attention, SiTU GLU activations, and a 1 million token context.

The coding trajectory is the clearest comparison because Moonshot benchmarks its own models consistently. K2.7 Code improved 21.8% on Kimi Code Bench v2, 11.0% on Program Bench, and 31.5% on MLS Bench Lite over K2.6, while reducing reasoning tokens by 30%. Even then, it trailed GPT 5.5, scoring 62.0 versus 69.0. K3 jumps to 73.7 under Claude Code and 72.9 under Kimi Code, moving from chasing GPT 5.5 to trailing only Claude Fable 5. The comparison is directional because the harnesses and benchmark versions differ.
As for reasoning, K2.7 made thinking mandatory, removing the instant mode available in K2.5 and K2.6. K3 builds on that by preserving reasoning history across long agent sessions and training separate low, high, and max reasoning experts before merging them into a single model through post-training. The largest leap is in Agenting execution. K2.7 delivered roughly 10% gains over K2.6 on agent benchmarks such as MCP Atlas and MCP Mark Verified. K3 closes much of the remaining gap: on Moonshot's black box system replication benchmark, K2.6 scores 0.560, GPT 5.5 0.893, Claude Opus 4.8 0.918, while K3 reaches 1.000, fully solving the task.

## Understanding model distillation
Model distillation, at its core, is one model learning from another instead of learning from raw data alone. That simple idea splits into at least three methods in practice, and the K3 dispute hinges entirely on which one is being alleged.
HuggingFace - Everything You Need to Know about Knowledge Distillation 
Classical knowledge distillation starts from a simple observation: a trained model knows more than its answers reveal. Ask a strong language model to complete "The capital of France is" and it says "Paris". But under the hood, it didn't just pick Paris. It weighed every token in its vocabulary and produced a full probability distribution: heavy mass on "Paris", a sliver on "located", a whisper on "the", effectively nothing on "banana". That distribution is a snapshot of everything the model believes about the question, including which wrong answers are almost right and which are absurd.
The idea of classical distillation is to train a smaller student on that entire distribution rather than on the final answer. Formally, the student minimizes the KL divergence between its predicted distribution and the teacher's at every token position. The difference from normal training is easy to see. A hard label is a one hot vector: all the mass on "Paris", zero everywhere else, so the gradient only says "push this token up." The teacher's distribution is dense: push "Paris" up, keep "located" moderately plausible, bury "banana", all in one signal. That relational structure is part of what makes the teacher smart, and it's exactly what a one-hot label throws away.
There's one practical wrinkle. A confident teacher puts nearly all its mass on the top token, so the informative near misses sit at tiny probabilities and barely contribute to the loss. The fix is temperature: divide the logits by a temperature T > 1 before applying the softmax during training. This flattens both distributions and amplifies the tails enough for the near misses to carry meaningful gradients. At inference, the temperature returns to 1, and the student runs normally. Done well, the student punches above its parameter count because it inherited the teacher's judgment, and that judgment often lives in the near misses.
Now the catch, and it matters for the K3 story: this description applies to classical logit distillation, which requires the teacher's full output distribution, typically obtained from its raw logits. Commercial APIs return generated text and at most a small top-k slice of log probabilities, never the full distribution, so classical logit distillation against a closed model like Claude Fable 5 is not practical through the API. 

## Did K3 distill from Claude?
The evidence for the allegation comes in three grades, and only one is documented.
The evidence comes in three grades, and only one is documented. In February 2026 Anthropic published findings accusing DeepSeek, Moonshot, and MiniMax of extracting Claude at scale: 16 million exchanges through roughly 24,000 fraudulent accounts, with Moonshot's 3.4 million targeting agentic reasoning, coding, computer use, and vision, plus a later phase aimed at reasoning traces. Serious, but months before K3, with no line drawn to K3's training data. The K3-specific government claim remains unsubstantiated, no logs or filings published, and Moonshot denied it. Weakest of all is K3 calling itself Claude in screenshots, which proves Claude text exists somewhere in a web-scale corpus, including public Fable trace datasets that predate K3, and nothing more.
The technical report cuts against the allegation three ways. The teacher chain is internal end to end: SFT trajectories from prior Kimi models, nine RL experts, MOPD consolidation, no step needing an external teacher. The Claude-flavored behavior has a non-distillation explanation: Moonshot's RL environment instantiates the Claude Code, Codex, OpenClaw, and Hermes harnesses, and a model trained inside a Claude-Code-shaped harness picks up Claude-Code-shaped conventions. And the timeline is hostile: Fable 5 was publicly available from June 9 to 12 and from July 1, K3 launched July 16 with testing reported before Fable was public, and K3 beats its alleged teacher on SWE-Marathon (+7), BrowseComp (+3.2), and the WebDev Arena (+44 Elo), which students rarely manage on the teacher's home ground.
The synthesis is narrower than either camp wants. Full distillation from Fable 5 is ruled out by the calendar and an architecture that shares nothing with Anthropic's. Post-training contamination stays open: the report publishes no data provenance, its internal-teacher claims are unverifiable from outside, and February-era material could have reached an earlier Kimi checkpoint that fed K3's SFT synthesis. What changed is that the question is now testable, the weights are public, and K3's output distribution can be probed against Claude's directly. 
Until then, Nathan Lambert's read holds: if adversarial distillation contributed, it did so to a relatively small degree. His argument runs through capability rather than provenance: observers who concluded from the distillation panic that Chinese labs only produce good models through IP theft are, in his words, in for an awakening, because Moonshot is solving the same scaling problems as OpenAI and Anthropic with orders of magnitude less capital.

## Benchmarking Claude Fable and Kimi K3 with W&B Weave
In the tutorial we will use OpenAI's HumanEval data, a set of 164 Python problems where each prompt is a function signature with a docstring and each item ships canonical hidden tests. We use a few questions to run both models against identical prompts, execute their code against those tests, and let W&B Weave handle tracing, scoring, and the side-by-side comparison. 
Every generation, its extracted code, its pass or fail, and its latency lands in the Weave dashboard.

### Step 0: Prerequisites & Install
You need three API keys before any of this runs: Kimi for the model doing the generating, Anthropic for Claude Fable 5, and one for Weights & Biases so traces and tables have somewhere to land.
For the Kimi API key to use K3:
- Navigate to https://platform.kimi.ai/‍
- Create your account by signing up.
- In the console page, select API keys.
- Create a new secret key and copy it. 
For the Weights & Biases key:
- Navigate to https://wandb.ai/ and sign up for a free account.
- Go to https://wandb.ai/authorize, or open API keys in your user settings.
- Create a key and copy it immediately.
For the Anthropic API Key to use Claude Fable 5:
- Navigate to https://platform.claude.com/‍
- Create your account by signing up.
- In the console page, select API keys, give a name and copy the API key. 
Export the keys to environment variables or save it inside .env file so nothing sensitive ends up in the script or in your Weave traces. As for the installation, we will use the OpenAI SDK for inference with Kimi K3 because Moonshot serves an OpenAI-compatible endpoint rather than a bespoke one.
1pip install openai weave anthropic

### Step 1: Imports and credentials
Three keys are needed: Moonshot for K3, Anthropic for Fable 5, and Weights & Biases for Weave logging. Moonshot caps organization concurrency at 3, and Weave's default parallelism will exceed that and fail generations with 429s, so set WEAVE_PARALLELISM before anything else runs.
1import os
2import json, re, subprocess, sys, tempfile, time
3from pathlib import Path
4import weave
5from anthropic import AsyncAnthropic
6from openai import AsyncOpenAI
7
8
9os.environ["MOONSHOT_API_KEY"] = ""
10os.environ["WANDB_API_KEY"] = ""
11os.environ["ANTHROPIC_API_KEY"] = ""
12os.environ["WEAVE_PARALLELISM"] = "2" 
13

### Step 2: Fable and Kimi LLM Inference functions
Start by defining a system prompt that is identical for both, and the sampling settings are each vendor's documented maximum: reasoning effort max for K3, the only level it exposes, and adaptive thinking at xhigh effort for Fable 5, which is what Anthropic recommends for coding work. Both return the same dictionary shape so the scorers do not need to know which model produced the output.
1SYSTEM = ("Complete the Python function. Reply with a single code block "
2 "containing the full function implementation and nothing else.")
3kimi_client = AsyncOpenAI(api_key=os.getenv("MOONSHOT_API_KEY"),
4 base_url="https://api.moonshot.ai/v1")
5
6
7claude_client = AsyncAnthropic()
8
9
10@weave.op()
11async def kimi_k3(prompt: str) -> dict:
12 t0 = time.monotonic()
13 res = await kimi_client.chat.completions.create(
14 model="kimi-k3",
15 messages=[{"role": "system", "content": SYSTEM},
16 {"role": "user", "content": prompt}],
17 temperature=1.0, reasoning_effort="max", max_tokens=1024
18 )
19 
20 return {"code": extract_code(res.choices[0].message.content),
21 "latency_s": round(time.monotonic() - t0, 2),
22 "output_tokens": res.usage.completion_tokens}
23
24
25@weave.op()
26async def claude_fable_5(prompt: str) -> dict:
27 t0 = time.monotonic()
28 res = await claude_client.messages.create(
29 model="claude-fable-5", max_tokens=1024, system=SYSTEM,
30 thinking={"type": "adaptive"}, 
31 output_config={"effort": "xhigh"}, 
32 messages=[{"role": "user", "content": prompt}]
33 )
34 text = "".join(b.text for b in res.content if b.type == "text")
35 
36 return {"code": extract_code(text),
37 "latency_s": round(time.monotonic() - t0, 2),
38 "output_tokens": res.usage.output_tokens}
39

### Step 3: Extraction and scorers to trace
Models wrap code in markdown fences, so extract_code pulls the last block out. The execution scorer does the real work: it rebuilds the program the way the official HumanEval harness does, prepending the prompt when a model replies with only a function body, then runs it against the hidden tests in a subprocess with a timeout. 
The latency scorer surfaces speed and token counts, and pass_rate reads pass@1 back out of the eval summary, degrading to an error message rather than crashing when every generation fails.
1def extract_code(text):
2 blocks = re.findall(r"```(?:python)?\n(.*?)```", text or "", re.DOTALL)
3 return blocks[-1].strip() if blocks else (text or "").strip()
4
5
6@weave.op()
7def latency_scorer(output: dict) -> dict:
8 return {"latency_s": output["latency_s"],
9 "output_tokens": output["output_tokens"]}
10
11
12@weave.op()
13def execution_scorer(prompt: str, test: str, entry_point: str, output: dict) -> dict:
14 code = output["code"]
15 if f"def {entry_point}" not in code: 
16 code = prompt + code 
17
18
19 program = f"{code}\n\n{test}\n\ncheck({entry_point})\n"
20
21
22 with tempfile.TemporaryDirectory() as td:
23 f = Path(td) / "sol.py"
24 f.write_text(program)
25 try:
26 p = subprocess.run([sys.executable, str(f)], capture_output=True,
27 text=True, timeout=20, cwd=td)
28 return {"passed": p.returncode == 0, "stderr": p.stderr[-300:]}
29 
30 except subprocess.TimeoutExpired:
31 return {"passed": False, "stderr": "TIMEOUT"}
32
33
34@weave.op()
35def pass_rate(model: str, summary: dict) -> dict:
36 """pass@1 = fraction of generations passing the hidden tests.
37 Scorer summaries come back null if every generation errored."""
38 passed = ((summary or {}).get("execution_scorer") or {}).get("passed") or {}
39 
40 return {"model": model,
41 "pass_at_1": passed.get("true_fraction"),
42 "n_passed": passed.get("true_count"),
43 "error": None if passed else "all generations failed - see API errors above"}
44

### Step 4: Initialize Weave project and load the data
Each data row contains a task_id, prompt, entry_point, canonical_solution, and test. We keep four of them: task_id, prompt, test, and entry_point. Initialize the Weave project, then load the first few problems to test the benchmark.
Download the data: https://github.com/openai/human-eval/raw/master/data/HumanEval.jsonl.gz
The data contains 164 prompts with Python problem statements. 
1weave.init("kimi-k3")
2
3
4rows = [json.loads(l) for l in Path("HumanEval.jsonl").read_text().splitlines() if l.strip()]
5dataset = [{"task_id": r["task_id"], "prompt": r["prompt"],
6 "test": r["test"], "entry_point": r["entry_point"]} for r in rows]
7
8
9print(f"{len(dataset)} problems loaded") # output: 164 problems loaded
10

### Step 5: Run Evals
One Evaluation object serves both models, which is what keeps the comparison honest: same problems and same scorers. Creating an Evaluation object is the first step in setting up your evaluation configuration. An Evaluation consists of example data, scoring logic, and optional preprocessing. You later use it to run one or more evaluations.
Evaluations help you compare changes against a consistent set of examples and detect regressions before they reach users. Here, Kimi K3 and Claude Fable 5 create two experiments with the above traces, and using this trace, we can use the Evals section in the dashboard to compare the results with a few charts, as shown in the image below the code:
1evaluation = weave.Evaluation(dataset=dataset,
2 scorers=[execution_scorer, latency_scorer])
3
4
5for fn in (kimi_k3, claude_fable_5):
6 print("evaluating", fn.name)
7 summary = await evaluation.evaluate(fn)
8 print(pass_rate(fn.name, summary))
9
Compare Evaluations for the traces passed through Kimi K3 and Claude Fable 5. Fable 5 passed 93.3% and K3 90.2%, a gap of five problems out of 164, while K3 took 18.62s per problem against Fable's 5.19s and spent 461.6 output tokens against 252.6.
Pass Rate Human Eval Results: Claude Fable 5 vs Kimi K3
Overview: Fable 5 solved 153 of 164 problems and K3 solved 148, a 93.3% to 90.2% gap of five problems, while K3 took 18.62s per problem against Fable's 5.19s and spent 461.6 output tokens against 252.6. One detail worth noticing in this view: model_latency (5.1914 / 18.6251) and the scorer's latency_s (5.1907 / 18.6244) agree to within a millisecond.
Evals Overview Metrics for both Claude Fable and Kimi K3 Experiment
In Weave, you can open any individual trace to see the full function-level breakdown: the model call, the extracted code, and each scorer's result side by side. That makes it straightforward to check exactly why a given example passed or failed rather than inferring it from the aggregate numbers.

## What this means for the open model ecosystem
K3 is frontier-class on code, ahead on visual and frontend work, behind Fable 5 on the hardest long-horizon repository tasks, and far ahead on cost. It does not behave like a Claude clone under inspection. Its failure modes are its own, over-proactiveness, sensitivity to thinking-history handling, higher run-to-run variance, and none of them are Fable traits. Teacher-student training on model outputs is now load-bearing infrastructure for the entire field. K3's own report makes the point better than any argument could: its post-training is a nine-teacher distillation pipeline, published openly, with an equation for the reward. Labs distill from their own larger checkpoints as routine practice.
The open frontier gap is now measured in weeks. K3's lineage is documented across three technical reports, its architecture is novel enough that nobody has suggested it resembles an Anthropic design, its capability jump decomposes cleanly into scale, attention redesign, and RL compute, and its weights are on Hugging Face where anyone can test the distillation hypothesis directly instead of arguing. Until someone does that work, the right way to evaluate K3 is the way you would evaluate any model: instrument it, run it on your own tasks, and read the traces.

## Resources
- Kimi K3 Technical Report: https://arxiv.org/pdf/2607.24653‍
- Kimi K3 Technical blog: https://www.kimi.com/blog/kimi-k3‍
- Distilling the Knowledge in a Neural Network: https://arxiv.org/pdf/1503.02531‍
- Simon Willison’s Weblog on Kimi K3: https://simonwillison.net/2026/Jul/16/kimi-k3/‍
- Interconnects AI newsletter by Nathan Lambert: https://www.interconnects.ai/p/kimi-k3-the-open-weights-escalation

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
