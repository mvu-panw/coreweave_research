# Python SDK

Source: https://docs.coreweave.com/products/agent-lens/reference/python-sdk

# Python SDK

> Reference for the CoreWeave Forge Python SDK, which sends agent traces to Agent Lens.

The CoreWeave Forge Python SDK (`coreweave`) records agent conversations, turns, LLM calls, tool calls, and sub-agents as OpenTelemetry spans and exports them to Agent Lens. This reference covers version 0.1.0b0 of the SDK.

## Install

The SDK requires Python 3.10 or later.

```bash theme={"system"}
pip install coreweave
```

To trace a provider SDK automatically, install the matching extra:

```bash theme={"system"}
pip install "coreweave[openai]"
pip install "coreweave[anthropic]"
pip install "coreweave[google-genai]"
```

## Import and initialize

Import the tracing module, then call [`init`](https://docs.coreweave.com/products/agent-lens/reference/python-sdk/setup#init) with your project in `entity/project` form. `init` reads your API key from the `WANDB_API_KEY` environment variable unless you pass `api_key`.

```python theme={"system"}
from coreweave.forge.agentlens import tracing

tracing.init("[ENTITY]/[PROJECT]")
```

## Reference pages

### Setup

| Page | Covers |
| - | - |
| [Setup and shutdown](https://docs.coreweave.com/products/agent-lens/reference/python-sdk/setup.md) | `init`, `force_flush`, `shutdown`, `TracingSession` |

### Spans

| Page | Covers |
| - | - |
| [Conversation](https://docs.coreweave.com/products/agent-lens/reference/python-sdk/conversation.md) | `Conversation` |
| [Turn](https://docs.coreweave.com/products/agent-lens/reference/python-sdk/turn.md) | `Turn` |
| [LLM](https://docs.coreweave.com/products/agent-lens/reference/python-sdk/llm.md) | `LLM` |
| [Tool](https://docs.coreweave.com/products/agent-lens/reference/python-sdk/tool.md) | `Tool` |
| [SubAgent](https://docs.coreweave.com/products/agent-lens/reference/python-sdk/subagent.md) | `SubAgent` |
| [Span functions](https://docs.coreweave.com/products/agent-lens/reference/python-sdk/span-functions.md) | `start_conversation`, `start_turn`, `start_llm`, `start_tool`, `start_subagent`, `end_conversation`, `end_turn`, `end_llm`, `get_current_conversation`, `get_current_turn`, `get_current_llm` |

### Batch logging

| Page | Covers |
| - | - |
| [Batch logging](https://docs.coreweave.com/products/agent-lens/reference/python-sdk/batch-logging.md) | `log_turn`, `log_conversation`, `LogResult` |

### Messages

| Page | Covers |
| - | - |
| [Message types](https://docs.coreweave.com/products/agent-lens/reference/python-sdk/message-types.md) | `Message`, `MessagePart`, `TextPart`, `ReasoningPart`, `ToolCallPart`, `ToolCallResponsePart`, `BlobPart`, `UriPart`, `FilePart`, `Usage`, `Reasoning`, `MediaAttachment` |

### Provider integrations

| Page | Covers |
| - | - |
| [Integrations](https://docs.coreweave.com/products/agent-lens/reference/python-sdk/integrations.md) | `autopatch`, `disable_autopatch`, `patch_openai`, `unpatch_openai`, `patch_anthropic`, `unpatch_anthropic`, `patch_google_genai`, `unpatch_google_genai`, `unpatch_all` |
