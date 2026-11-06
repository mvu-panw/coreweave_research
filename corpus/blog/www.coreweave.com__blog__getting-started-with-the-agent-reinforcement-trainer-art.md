# Getting started with the Agent Reinforcement Trainer (ART)

Source: https://www.coreweave.com/blog/getting-started-with-the-agent-reinforcement-trainer-art

Announcement

Webinar

Podcast

GTC 2026

CoreWeave Forge is here: connect your AI loop and compound every improvement. Read more

Contact us

Originally published on the Weights & Biases by CoreWeave blog on July 18, 2026.
Reinforcement learning (RL) is driving some of the most impressive recent advances in machine learning by enabling agents not only to learn from pre-existing data, but to actively improve through experience. 
As language models shift from being static text generators to dynamic, agentic participants in complex workflows, the need to reliably train, evaluate, and enhance these agents becomes critical.
The Agent Reinforcement Trainer (ART) is an open-source framework designed to make RL for large language models accessible, robust, and efficient. ART combines modern reinforcement learning algorithms like GRPO with automation tools such as the RULER reward function to create a seamless workflow. This lets developers rapidly train and deploy LLM-powered agents that actually improve over time.
In this article, we provide a step-by-step walkthrough of applying RL to LLM agents using ART. You will learn the fundamentals of RL and ART, how to structure an RL challenge for LLMs, set up the training pipeline, and evaluate agent improvements. The process is illustrated with clear, hands-on code examples, including training a model to play the game of tic-tac-toe.

## What is RL? 
Reinforcement learning is a field of machine learning focused on training agents to make a sequence of decisions that maximize some notion of cumulative reward. Unlike supervised learning, where a model learns from labeled datasets, RL agents learn by interacting with an environment. At each step, the agent observes the current state of the environment, takes an action, and then receives feedback in the form of a reward that indicates how good or bad the action was.
The fundamental idea behind RL is trial and error. The agent explores different actions and learns over time which strategies lead to better outcomes. This is particularly important for tasks where there is no single correct answer, and success depends on making a series of good decisions.
Key components of RL include:
Agent: The learner or decision maker.
Environment: The world the agent interacts with.
State: The current situation or context for the agent.
Action: A choice made by the agent that affects the state.
Reward: Feedback from the environment to evaluate the agent's action.
By optimizing its actions to maximize the total reward over time, the agent improves its decision-making capabilities. RL has powered breakthroughs in areas such as robotics, game playing, and recommendation systems, and is now an essential technique for teaching language models to become more reliable, useful, and adaptive as agents.
In the context of large language models, RL enables agents to go beyond merely predicting the next word. It empowers them to learn from the consequences of their responses, become more aligned with user expectations, and deliver better multi-turn or goal-directed performance.

## Basics of ART
ART is an open-source framework designed to help developers train and improve language model agents using reinforcement learning with minimal setup. ART streamlines RL by providing clear abstractions, intelligent defaults, and seamless support for the open source ML ecosystem.
At its core, ART enables agents to learn from experience within simulated environments. When an agent interacts with its environment, the full sequence of prompts, responses, and received feedback (known as a trajectory) is captured. These trajectories are used to guide the model toward better, reward-optimizing behavior.
ART consists of two primary components:
Client: This is integrated into your Python project and manages agent-environment interactions, collection of experience, and communication with the backend.
Backend: This component handles the computational heavy lifting, including model inference, reinforcement learning via group relative policy optimization (GRPO), memory management, and saving checkpoints. The backend can run locally on a GPU or make use of a cloud backend for scalable GPU resources.
ART stands out for its tight integration with open source tooling. It provides excellent compatibility with Hugging Face models and supports training LoRA adapters, so you can quickly fine-tune or reinforce a wide range of community models without engineering friction.
A major benefit of ART is its fully automated reward system through RULER, which can score agent outputs using a language model as evaluator. This allows you to start training even when you do not have an explicit ground-truth dataset or must use subjective rewards.
According to the ART docs, to get good results it is recommended that your task meets the following requirements:
Open source models should be able to solve the task at least 30 percent of the time. If your model cannot complete the task at all, it will be difficult for ART to teach the model efficiently.
It is important to have a clear and consistent way to verify task success. Since ART and other reinforcement learning methods depend on optimizing a quantifiable reward, you need to define a reward signal that can be measured for each agent run. This reward can be objective, such as matching a reference output, or subjective, such as approval from an LLM-as-judge, but it must be consistent and reproducible.
Your agent should be runnable many times in a repeatable environment. ART’s RL algorithms, such as GRPO, rely on comparing results from many agent runs in parallel, so this approach is best suited for simulations or tasks that do not cause real-world side effects.
With broad support for Hugging Face models, easy LoRA training, and a streamlined approach to gathering, scoring, and training on agent experiences, ART makes it possible for ML practitioners to bring reinforcement learning to a wide range of LLM tasks and open source models.

## Installing ART 
Getting everything working can sometimes take a bit of effort on a new cloud machine. 
First, make sure you have Python 3 and pip installed. On a clean system, I had to install pip and a few system libraries. Some commands needed sudo to work, especially when installing Python packages or running scripts.
Start by making sure pip is installed and up to date. Note that apt commands are for linux systems only. 
sudo apt update
sudo apt install python3-pip python3-dev libcairo2-dev
Install ART and other dependencies. Sometimes sudo was required for permissions: 
sudo python3 -m pip install openpipe-art wandb weave torchtune --upgrade pip setuptools packaging
If you run into errors about missing permissions or missing libraries, try adding sudo at the front of the command.
Once all dependencies are installed, the scripts will run as expected. Now let’s walk through a hands-on demo of using ART to train a language model agent for the game of Tic-Tac-Toe. The goal here is to show how ART can be used to structure a full reinforcement learning loop for a language model, including environment definition, agent interaction, reward assignment, and iterative model updates with only a few components you control.

## Training Qwen 2.5 to play tic-tac-toe
In this example, we’ll use Qwen2.5, a small but capable open-source language model, and have it play Tic-Tac-Toe against a random opponent. The ART framework will handle the RL training loop, letting our agent play full games, receive rewards based on its performance, and gradually improve over successive training steps. By expressing the entire flow in code, we can precisely define the rules of the game, what counts as a valid move, and give feedback to the agent after each match.
We’ll also see how ART’s abstractions make it easy to run these RL experiments locally, track metrics, and control the model’s checkpoints, all without building RL orchestration or training infrastructure from scratch. This example starts simple, but mirrors the same workflow you could use for much more advanced LLM agent training scenarios.
Here’s the full script to get you started:
import asyncio
import random
import math
import os
import xml.etree.ElementTree as ET
from typing import TypedDict, Literal

import art
from art.local.backend import LocalBackend
from pydantic import BaseModel

import sys
WANDB_API_KEY = "your_wandb_api_key"
if WANDB_API_KEY:
 os.environ["WANDB_API_KEY"] = WANDB_API_KEY

# --------- Tic Tac Toe Environment ----------

import weave; weave.init("tic-tac-toe")

class TicTacToeGame(TypedDict):
 board: list[list[str]]
 agent_symbol: Literal["x", "o"]
 opponent_symbol: Literal["x", "o"]

def generate_game(board_length: int = 3) -> TicTacToeGame:
 board = [["_" for _ in range(board_length)] for _ in range(board_length)]
 agent_symbol = random.choice(["x", "o"]
 )
 opponent_symbol = "x" if agent_symbol == "o" else "o"
 return {
 "board": board,
 "agent_symbol": agent_symbol,
 "opponent_symbol": opponent_symbol,
 }

def render_board(game: TicTacToeGame) -> str:
 board = game["board"]
 board_length = len(board)
 board_str = " " + " ".join([str(i + 1) for i in range(board_length)]) + "\n"
 for i in range(board_length):
 board_str += f"{chr(65 + i)} {board[i][0]} | {board[i][1]} | {board[i][2]}\n"
 return board_str

def get_opponent_move(game: TicTacToeGame) -> tuple[int, int]:
 empty_cells = [
 (i, j) for i in range(3) for j in range(3) if game["board"][i][j] == "_"
 ]
 return random.choice(empty_cells)

def apply_agent_move(game: TicTacToeGame, move: str) -> None:
 board_length = len(game["board"])
 try:
 root = ET.fromstring(move)
 square = root.text.strip()
 except Exception:
 raise ValueError("Invalid xml")

 try:
 row_index = ord(square[0].upper()) - 65
 col_index = int(square[1]) - 1
 except Exception as e:
 raise ValueError("Unable to parse square") from e

 if (row_index < 0 or row_index >= board_length or
 col_index < 0 or col_index >= board_length):
 raise ValueError(
 f"Invalid move, row or column out of bounds: {row_index}, {col_index}"
 )
 if game["board"][row_index][col_index] != "_":
 raise ValueError("Square already occupied")
 game["board"][row_index][col_index] = game["agent_symbol"]

def check_winner(board: list[list[str]]) -> Literal["x", "o", "draw", None]:
 board_length = len(board)
 # check rows
 for row in board:
 if row.count(row[0]) == board_length and row[0] != "_":
 return row[0]
 # check columns
 for col in range(board_length):
 col_vals = [board[row][col] for row in range(board_length)]
 if col_vals.count(col_vals[0]) == board_length and col_vals[0] != "_":
 return col_vals[0]
 # diagonals
 up_diag = [board[i][board_length - i - 1] for i in range(board_length)]
 if up_diag.count(up_diag[0]) == board_length and up_diag[0] != "_":
 return up_diag[0]
 down_diag = [board[i][i] for i in range(board_length)]
 if down_diag.count(down_diag[0]) == board_length and down_diag[0] != "_":
 return down_diag[0]
 # draw
 if all(cell != "_" for row in board for cell in row):
 return "draw"
 return None

# --------- ART RL Setup ----------

class TicTacToeScenario(BaseModel):
 step: int

async def rollout(model: art.Model, scenario: TicTacToeScenario) -> art.Trajectory:
 game = generate_game()
 trajectory = art.Trajectory(
 messages_and_choices=[{
 "role": "system",
 "content":
 f"You are a tic-tac-toe player. You are playing against an opponent. Always choose the move most likely to lead to an eventual win. Return your move as an XML object with a single property 'move', like so: <move>A1</move>. Optional moves are 'A1', 'B3', 'C2', etc. You are the {game['agent_symbol']} symbol."
 }],
 metadata={
 "step": scenario.step,
 },
 reward=0,
 )

 move_number = 0

 if game["agent_symbol"] == "o":
 starting_opponent_move = get_opponent_move(game)
 game["board"][starting_opponent_move[0]][starting_opponent_move[1]] = game["opponent_symbol"]

 while check_winner(game["board"]) is None:
 trajectory.messages_and_choices.append(
 {"role": "user", "content": render_board(game)}
 )
 messages = trajectory.messages()
 try:
 client = model.openai_client()
 chat_completion = await client.chat.completions.create(
 model=model.get_inference_name(),
 messages=messages,
 max_completion_tokens=128,
 )
 except Exception as e:
 print("Exception in chat completion:", e)
 break

 choice = chat_completion.choices[0]
 content = choice.message.content
 trajectory.messages_and_choices.append(choice)

 try:
 apply_agent_move(game, content)
 except ValueError:
 trajectory.reward = -1 + (math.log(move_number + 1) / math.log(100))
 break

 move_number += 1
 if check_winner(game["board"]) is not None:
 break

 opponent_move = get_opponent_move(game)
 game["board"][opponent_move[0]][opponent_move[1]] = game["opponent_symbol"]

 winner = check_winner(game["board"])
 if winner == game["agent_symbol"]:
 trajectory.reward = 1
 trajectory.metrics["win"] = 1
 print("win!!!", flush=True)
 elif winner == game["opponent_symbol"]:
 trajectory.reward = 0
 trajectory.metrics["win"] = 0
 print("loss!!!", flush=True)
 elif winner == "draw":
 trajectory.reward = 0.5
 trajectory.metrics["win"] = 0.5

 trajectory.metrics["num_moves"] = move_number
 return trajectory

# --------- Main Training Loop ----------

async def main():
 random.seed(42)
 backend = LocalBackend(path="./.art")

 model = art.TrainableModel(
 name="002-script",
 project="tic-tac-toe",
 base_model="Qwen/Qwen2.5-3B-Instruct",
 # base_model="openai-community/gpt2"
 )
 await model.register(backend)

 # Training loop (reduce 48 to a smaller number for speed if needed)
 for i in range(await model.get_step(), 1000): # For demo, only 10 steps
 print(f"Training step {i}...")
 train_groups = await art.gather_trajectory_groups(
 (
 art.TrajectoryGroup(
 rollout(model, TicTacToeScenario(step=i)) for _ in range(8)
 )
 for _ in range(1)
 ),
 pbar_desc="gather",
 )
 await model.delete_checkpoints()
 await model.train(train_groups, config=art.TrainConfig(learning_rate=5e-5))
 print("Training complete.")
 sys.exit()

if __name__ == "__main__":
 asyncio.run(main())

Let’s break down what’s happening in this script and highlight how ART streamlines the workflow. 
The code first defines the mechanics of the tic-tac-toe environment in Python, covering the board setup, move validation, opponent logic, and winner detection functions. By creating the environment as standard Python code, you get full control over the game’s rules, including what counts as a legal move and when the agent receives a reward or penalty. This makes it easy to experiment with new gameplay dynamics or modify reward structures by tweaking just a few functions.
The core of the RL process is handled in the rollout function. Here, the agent engages in full games of tic-tac-toe, viewing the board rendered in a simple text grid and responding with moves formatted in XML. Each exchange adds to the interaction history, which is fed into the model at each step. ART manages the process of tracking all messages, choices, and outcomes for every episode. If the agent makes an illegal or badly formatted move, the script penalizes this, ensuring the agent learns both valid gameplay and correct communication.
A key benefit of using ART is that you do not need to manually code the RL training loop, manage checkpoints, or orchestrate trajectory collection yourself. ART's backend and the TrainableModel abstraction take care of these infrastructure details, freeing you to focus on designing your environment, reward functions, and agent strategies. This script also makes use of ART’s metric tracking, letting you monitor agent performance trends such as win rate or move count progress throughout training.
Since ART is compatible with open source models like Qwen and supports efficient fine tuning strategies like LoRA, it is straightforward to experiment with different architectures or scale up your training setup as needed. Swapping between local GPU and cloud resources is also simple, as ART’s backend abstraction handles the details for you.
This workflow shows how ART can be leveraged to rapidly prototype and run reinforcement learning experiments with language models. With ART handling the orchestration, distributed training, and experiment management, you can focus on what matters: designing your custom environment, defining rewards, and shaping the behavior of your LLM agent.
After running our training script, you can navigate to W&B to visualize the performance of our model in real time as it learns through experience. 
Since W&B is natively integrated with ART, we don’t need any extra code to track the performance of our model! Here are the training logs from my run: 
 Training reward over time as the agent improves through reinforcement learning.
The train/reward chart shows the average reward achieved by the agent at each training step. You’ll notice that the average reward increases gradually over time, indicating that the agent is learning how to win or draw more often as training progresses. 
There’s a noticeable peak around step 300, followed by a dip and a later recovery. These ups and downs are typical in reinforcement learning: they can be caused by shifts in the agent’s policy as it explores new strategies, by the inherent randomness in the environment (like the random moves of the opponent), or by instability during learning updates. Overall, these fluctuations reflect the dynamic process of the agent both improving and sometimes regressing as it balances exploration with exploitation, but the general upward trend is a strong indicator that learning is taking place.

## Evaluating our fine-tuned model
Once we have a trained Tic-Tac-Toe agent, it is essential to evaluate its performance in a systematic way. This helps us measure how often the agent is able to win, draw, avoid mistakes, and how it compares to both its original base model and to much larger models in the same family. For this project, our base model is a 3 billion parameter Qwen model, while we will also include results from a much larger 14 billion parameter Qwen model (without RL fine-tuning on tic-tac-toe) as a reference point. We can also benchmark against strong external models like GPT-4o-mini to provide additional context for our results.
The script below automates these head-to-head evaluations. It supports running tests for any of our models, including the base model, our LoRA fine-tuned version, and larger open models. To make the comparison fair, the agent will alternate playing as X and O, so we are not biased by the starting position. It records statistics for wins, losses, draws, and errors across many games.
Running this kind of objective evaluation lets us see how much progress our training has made, and where our agent stands relative to both smaller and much larger models. It also helps us catch issues, spot overfitting, and decide if further tuning or changes to the reward scheme are needed.
Here is the complete evaluation script you can use to benchmark your trained agent and see a side-by-side performance summary for all models under test.
import os
import random
import sys
import xml.etree.ElementTree as ET
import litellm
from litellm import completion
import weave; weave.init("tic-tac-toe")

os.environ["OPENAI_API_KEY"] = "your_openai_api_key"

lora_model_project = "tic-tac-toe"
lora_model_name = "002-script"
lora_model_step = 3
lora_model_max_seq_length = 4096

# Set this to your actual base model (e.g. your pre-untrained checkpoint from Huggingface's hub)
base_model_path = "Qwen/Qwen2.5-14B-Instruct" # Change as needed!

# Globals for LoRA
LORA_PEFT_MODEL = None
LORA_TOKENIZER = None

# Globals for BASE
BASE_MODEL = None
BASE_TOKENIZER = None

def load_lora_model_once():
 global LORA_PEFT_MODEL, LORA_TOKENIZER
 if LORA_PEFT_MODEL is None or LORA_TOKENIZER is None:
 import torch
 from unsloth import FastLanguageModel
 lora_model_path = f".art/{lora_model_project}/models/{lora_model_name}/checkpoints/0571"
 print(f"Loading LoRA model from {lora_model_path}\n")
 LORA_PEFT_MODEL, LORA_TOKENIZER = FastLanguageModel.from_pretrained(
 model_name=lora_model_path,
 max_seq_length=lora_model_max_seq_length,
 dtype=torch.bfloat16,
 load_in_4bit=True,
 )
 FastLanguageModel.for_inference(LORA_PEFT_MODEL)

def load_base_model_once():
 global BASE_MODEL, BASE_TOKENIZER
 if BASE_MODEL is None or BASE_TOKENIZER is None:
 import torch
 from unsloth import FastLanguageModel
 print(f"Loading BASE model from {base_model_path}\n")
 BASE_MODEL, BASE_TOKENIZER = FastLanguageModel.from_pretrained(
 model_name=base_model_path,
 max_seq_length=lora_model_max_seq_length,
 dtype=torch.bfloat16,
 load_in_4bit=True,
 )
 FastLanguageModel.for_inference(BASE_MODEL)

def generate_game(board_length: int = 3, agent_symbol=None):
 board = [["_" for _ in range(board_length)] for _ in range(board_length)]
 if agent_symbol is None:
 agent_symbol = random.choice(["x", "o"])
 opponent_symbol = "x" if agent_symbol == "o" else "o"
 return {
 "board": board,
 "agent_symbol": agent_symbol,
 "opponent_symbol": opponent_symbol,
 }

def render_board(game):
 board = game["board"]
 board_length = len(board)
 board_str = " " + " ".join([str(i + 1) for i in range(board_length)]) + "\n"
 for i in range(board_length):
 row = " | ".join(board[i])
 board_str += f"{chr(65 + i)} {row}\n"
 return board_str

def get_opponent_move(game):
 empty_cells = [
 (i, j) for i in range(3) for j in range(3) if game["board"][i][j] == "_"
 ]
 return random.choice(empty_cells)

def apply_agent_move(game, move):
 board_length = len(game["board"])
 try:
 root = ET.fromstring(move)
 square = root.text.strip()
 except Exception:
 raise ValueError(f"Invalid xml: {move!r}")
 try:
 row_index = ord(square[0].upper()) - 65
 col_index = int(square[1]) - 1
 except Exception as e:
 raise ValueError(f"Unable to parse square from {move!r}") from e
 if (row_index < 0 or row_index >= board_length or
 col_index < 0 or col_index >= board_length):
 raise ValueError(
 f"Invalid move, row or column out of bounds: {row_index}, {col_index}"
 )
 if game["board"][row_index][col_index] != "_":
 raise ValueError("Square already occupied")
 game["board"][row_index][col_index] = game["agent_symbol"]

def check_winner(board):
 board_length = len(board)
 # check rows
 for row in board:
 if row.count(row[0]) == board_length and row[0] != "_":
 return row[0]
 # check columns
 for col in range(board_length):
 col_vals = [board[row][col] for row in range(board_length)]
 if col_vals.count(col_vals[0]) == board_length and col_vals[0] != "_":
 return col_vals[0]
 # diagonals
 up_diag = [board[i][board_length - i - 1] for i in range(board_length)]
 if up_diag.count(up_diag[0]) == board_length and up_diag[0] != "_":
 return up_diag[0]
 down_diag = [board[i][i] for i in range(board_length)]
 if down_diag.count(down_diag[0]) == board_length and down_diag[0] != "_":
 return down_diag[0]
 # draw
 if all(cell != "_" for row in board for cell in row):
 return "draw"
 return None

def lora_get_completion(messages):
 import torch
 load_lora_model_once()
 peft_model = LORA_PEFT_MODEL
 tokenizer = LORA_TOKENIZER
 inputs = tokenizer.apply_chat_template(
 messages, return_tensors="pt", add_generation_prompt=True
 ).to(peft_model.device)
 with torch.no_grad():
 outputs = peft_model.generate(
 input_ids=inputs,
 max_new_tokens=100,
 do_sample=True,
 temperature=0.7,
 top_p=0.9,
 )
 return tokenizer.decode(
 outputs[0][inputs.shape[1]:], skip_special_tokens=True
 )

def base_get_completion(messages):
 import torch
 load_base_model_once()
 base_model = BASE_MODEL
 tokenizer = BASE_TOKENIZER
 inputs = tokenizer.apply_chat_template(
 messages, return_tensors="pt", add_generation_prompt=True
 ).to(base_model.device)
 with torch.no_grad():
 outputs = base_model.generate(
 input_ids=inputs,
 max_new_tokens=100,
 do_sample=True,
 temperature=0.7,
 top_p=0.9,
 )
 return tokenizer.decode(
 outputs[0][inputs.shape[1]:], skip_special_tokens=True
 )

def convert_to_content_blocks(messages):
 out = []
 for m in messages:
 c = m["content"]
 if isinstance(c, tuple): # tuple to str
 c = "".join(c)
 if isinstance(c, str):
 c = [{"type": "text", "text": c}]
 elif isinstance(c, list):
 c = [{"type": "text", "text": x} if isinstance(x, str) else x for x in c]
 out.append({"role": m["role"], "content": c})
 return out

def gpt4omini_get_completion(messages):
 messages = convert_to_content_blocks(messages)
 response = completion(
 model="gpt-4o-mini",
 messages=messages, # MUST use blocks format!
 temperature=0.7,
 max_tokens=64,
 )
 return response["choices"][0]["message"]["content"]

def get_system_prompt(agent_symbol):
 return (
 "You are a tic-tac-toe player. You are competing against a random opponent. \n"
 "Your ONLY job is to output your move using a single XML tag in this format:\n"
 "\n"
 " <move>B2</move>\n"
 "\n"
 "Pick a square that is empty and most likely to help you win.\n"
 "\n"
 "Allowed choices are any unused square, named like: A1, A2, A3, B1, B2, B3, C1, C2, C3.\n"
 "Respond ONLY with a single XML object, NO explanation or text, NO punctuation or words outside the XML tag!\n"
 "\n"
 "Examples of valid output:\n"
 "<move>A2</move>\n"
 "<move>C3</move>\n"
 "\n"
 "DO NOT output anything except the XML tag. NO explanations, NO reasoning. If you do, you LOSE the game.\n"
 "\n"
 f"You are playing as: {agent_symbol}.\n DO NOT move to squares that are already occupied"
 "\n"
 "Repeat: OUTPUT ONLY a single <move>...</move> XML tag as your entire response, nothing else."
 )

@weave.op 
def play_single_game(get_completion, agent_symbol='x'):
 random.seed()
 move_number = 0
 trace = []
 game = generate_game(agent_symbol=agent_symbol)

 messages = [
 {
 "role": "system",
 "content": get_system_prompt(agent_symbol)
 },
 ]

 trace.append(f"Game start (Agent: {game['agent_symbol']}, Opponent: {game['opponent_symbol']})\n{render_board(game)}")

 if game["agent_symbol"] == "o":
 starting_opponent_move = get_opponent_move(game)
 game["board"][starting_opponent_move[0]][starting_opponent_move[1]] = game["opponent_symbol"]
 trace.append(f"Opponent ({game['opponent_symbol']}) opens at {chr(65+starting_opponent_move[0])}{starting_opponent_move[1]+1}:\n{render_board(game)}")

 while check_winner(game["board"]) is None:
 rendered_board = render_board(game)
 messages.append({"role": "user", "content": rendered_board})

 try:
 content = get_completion(messages)
 except Exception as e:
 trace.append(f"\nERROR during agent generation: {e}\n")
 return "error", "\n".join(trace)

 messages.append({"role": "assistant", "content": content})

 try:
 # Parse agent's move
 root = ET.fromstring(content)
 move_str = root.text.strip()
 ally = game['agent_symbol']
 except Exception:
 trace.append(f"\nERROR: Agent move invalid XML: {content}\n")
 return "error", "\n".join(trace)
 try:
 apply_agent_move(game, content)
 move_number += 1
 except ValueError as e:
 trace.append(f"\nERROR: Invalid agent move on move {move_number}: {content} ({e})\n")
 return "error", "\n".join(trace)

 trace.append(f"Move {move_number} - Agent ({ally}) at {move_str}:\n{render_board(game)}")

 if check_winner(game["board"]) is not None:
 break

 # Opponent's move (random)
 opponent_move = get_opponent_move(game)
 row, col = opponent_move
 game["board"][row][col] = game["opponent_symbol"]
 trace.append(f"Move {move_number} - Opponent ({game['opponent_symbol']}) at {chr(65+row)}{col+1}:\n{render_board(game)}")

 winner = check_winner(game["board"])
 if winner == game["agent_symbol"]:
 result_str = "AGENT WON! 💪"
 elif winner == game["opponent_symbol"]:
 result_str = "AGENT LOST! 😢"
 elif winner == "draw":
 result_str = "DRAW! 🤷‍♂️"
 else:
 result_str = "ERROR?"
 trace.append(f"Game finished after {move_number} moves: {result_str}")
 trace.append(f"Final board:\n{render_board(game)}")
 return winner, "\n".join(trace)

def evaluate_models_over_n_games(n_games=10, verbose=False):
 stats = {
 'gpt-4o-mini': {'x': {'win': 0, 'draw': 0, 'loss': 0, 'error': 0}, 'o': {'win': 0, 'draw': 0, 'loss': 0, 'error': 0}},
 'lora': {'x': {'win': 0, 'draw': 0, 'loss': 0, 'error': 0}, 'o': {'win': 0, 'draw': 0, 'loss': 0, 'error': 0}},
 'base': {'x': {'win': 0, 'draw': 0, 'loss': 0, 'error': 0}, 'o': {'win': 0, 'draw': 0, 'loss': 0, 'error': 0}},
 }
 for model_type in ['gpt-4o-mini', 'lora', 'base']:
 if model_type == "lora":
 load_lora_model_once()
 get_completion = lora_get_completion
 elif model_type == "base":
 load_base_model_once()
 get_completion = base_get_completion
 else:
 get_completion = gpt4omini_get_completion
 for i in range(n_games):
 agent_symbol = 'x' if i % 2 == 0 else 'o'
 winner, trace = play_single_game(get_completion, agent_symbol)
 print(f"\n=== {model_type.upper()} GAME {i+1} as {agent_symbol.upper()} ===\n" + trace + "\n", flush=True)
 if winner == agent_symbol:
 stats[model_type][agent_symbol]['win'] += 1
 elif winner == "draw":
 stats[model_type][agent_symbol]['draw'] += 1
 elif winner == "error":
 stats[model_type][agent_symbol]['error'] += 1
 else:
 stats[model_type][agent_symbol]['loss'] += 1
 if verbose:
 print(f"[{model_type} | {agent_symbol}] Winner: {winner}\n{'-'*32}")
 return stats

if __name__ == "__main__":
 N = 100 # Increase for more robust stats
 verbose = False # True for debugging
 results = evaluate_models_over_n_games(N, verbose=verbose)
 for model_type in results:
 print(f"\n=== Results for {model_type} ===")
 for symbol in ['x', 'o']:
 s = results[model_type][symbol]
 print(f" As {symbol.upper()} - Wins: {s['win']} Draws: {s['draw']} Losses: {s['loss']} Errors: {s['error']}")

Let's look a bit closer at how this evaluation script operates and how it benefits your workflow. One of the key design choices is flexibility: the script can easily evaluate any number of model backends. Whether you are working with your original base Qwen 3B model, a fine-tuned LoRA version, a much larger 14B model from the same family, or even external models like GPT-4o-mini, the same logic and evaluation routines will work without modification. This design lets you run fair and reproducible tests under identical conditions, so you can truly see the effect of different model sizes and fine-tuning techniques.
The script also captures not just the overall outcome of each game, but also errors such as invalid moves or incorrectly formatted outputs. This is helpful because it surfaces problems with robustness, stability, or prompt adherence, not just pure playing strength. With enough games in each batch, you can be confident the summary statistics represent how each model really behaves.
A major feature of this workflow is the integration with Weights & Biases Weave. By initializing Weave at the start of your session and decorating the core gameplay function with @weave.op, the entire process, including all inputs and outputs is tracked automatically and stored in your Weave dashboard. This gives you a detailed trace for every evaluation run, making it easy to analyze individual games, spot failure cases, and share results with your team. Weave also makes it possible to aggregate results from different experiments, compare model outputs side by side, and keep track of key metrics like LLM usage and costs over time.
With this approach, you get a robust and transparent evaluation pipeline that scales gracefully whether you are just getting started or benchmarking across multiple large models and prompt variations. All crucial details are logged, reproducible, and accessible for further analysis or collaboration.
Here’s the results for my evaluation: 
Here, "Base" is the 14B Qwen Model, and "lora" is the fine-tuned Qwen 3b Model
When we look at the total number of wins and losses across both X and O, the fine-tuned model comes out on top. It scored the most wins overall and had fewer losses compared to gpt-4o-mini. In contrast, the base model had the fewest wins, highlighting how much difference fine-tuning made. These results clearly show that our fine-tuned agent was the most successful in actual gameplay, consistently outperforming both the base model and the much larger external model in head-to-head matches.
If we also are interested in the specifics of how the model performed at every move, we can also navigate to Weave to visualize the game trajectories! Here’s a screenshot inside Weave showing a trace of a game:
Inspecting a tic-tac-toe agent rollout in W&B Weave, including the model call, inputs, and final game result.
Here we can see the entire game. This is useful for debugging strange behavior, analyzing individual decisions, and ensuring the agent’s logic aligns with expectations. By tracing each move we gain insight into how the agent interprets the state of the board and selects actions. This is a powerful tool when refining reward functions or adjusting training dynamics.

## Conclusion
This project shows that reinforcement learning, combined with tools like ART and Weights & Biases Weave, can noticeably boost how well language model agents learn and improve. With ART, setting up the RL workflow becomes straightforward. You can design your environment, automate reward signals, track experience, and update your model without heavy engineering overhead.
The results make one thing clear. RL fine-tuning helps agents perform better than the original base models and even lets them compete with much larger external models. Detailed evaluation with tracked results and error reports gives a full picture of progress, making it easy to spot areas for further improvement.
The methods and tools demonstrated here are not limited to games but can be applied to a wide range of LLM-powered agents and real-world tasks. Open access to both the RL code and evaluation pipelines means anyone can build on these foundations, test new ideas, or bring agentic LLMs into production. As the field moves forward, practical RL and systematic evaluation will remain key to building reliable, adaptive AI agents. With ART and Weave, these best practices are now within reach for any developer or researcher who wants to push the boundaries of what language models can do.

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
