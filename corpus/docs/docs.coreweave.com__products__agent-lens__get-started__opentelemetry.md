# Send OpenTelemetry spans to Agent Lens

Source: https://docs.coreweave.com/products/agent-lens/get-started/opentelemetry

# Send OpenTelemetry spans to Agent Lens

> Send OTLP trace data from any OpenTelemetry pipeline to the Agent Lens endpoint. No SDK integration required.

CoreWeave Agent Lens is built on [OpenTelemetry (OTel)](https://opentelemetry.io/docs/concepts/) and provides a dedicated OTLP endpoint that ingests spans into Agent Lens. This means that you can quickly redirect your OTel-instrumented application's spans to Agent Lens by swapping your OTel exporter's current endpoint configuration with Agent Lens's endpoint configuration. You do not need to install the CoreWeave Forge SDK to do this.

This page covers how to authenticate with and send spans to the endpoint.

> [!NOTE]
>
> Agent Lens runs on the same backend as Weights & Biases, so some configuration names keep the `wandb` prefix: the `WANDB_API_KEY` environment variable, the `wandb-api-key` header, and the `wandb.entity` and `wandb.project` resource attributes. Use these names as shown.

## Authentication

You can send spans to the following endpoint:

* **Path**: `/agents/otel/v1/traces`
* **Method**: `POST`
* **Content-Type**: `application/x-protobuf`
* **Base URL**: `https://trace.wandb.ai` for Forge.

The endpoint accepts OTLP protobuf payloads only. Use a protobuf HTTP exporter such as `opentelemetry-exporter-otlp-proto-http` (Python) or `@opentelemetry/exporter-trace-otlp-proto` (TypeScript). The endpoint also accepts `gzip` and `deflate` content encoding.

To authenticate with the endpoint, set your [API key](https://forge.coreweave.com/settings#apikeys) in your `OTLPSpanExporter` configuration using one of the following values:

* `wandb-api-key`: Your Forge API key as the value.
* `Authorization`: HTTP Basic authentication with `api` as the user and your Forge API key as the password. This form is useful when your exporter or collector only supports standard authorization headers.

## Project routing

Agent Lens routes spans to a project using either OTel resource attributes or a request header:

* **Resource attributes** (recommended): Set `wandb.entity` to your Forge team or user name and `wandb.project` to the project name on your `TracerProvider` resource.
* **`project_id` header**: Set the value to `[YOUR-TEAM]/[YOUR-PROJECT]`.

If both are present, the resource attributes take precedence. Spans that arrive with no entity and project are dropped.

## Shape spans for the Conversations tab

Agent Lens accepts any OTel span and stores all of its attributes, but the Conversations tab renders spans that follow the [OTel GenAI semantic conventions](https://github.com/open-telemetry/semantic-conventions-genai/blob/main/docs/gen-ai/gen-ai-agent-spans.md). Set `gen_ai.operation.name` on each span to tell Agent Lens what the span represents:

| `gen_ai.operation.name` | Represents | Rendered as |
| - | - | - |
| `invoke_agent` | One complete user-agent exchange. | A turn. |
| `chat` | One call to a language model API. | An LLM call within a turn. |
| `execute_tool` | One tool execution. | A tool call. |

Two more attributes control grouping:

* `gen_ai.conversation.id`: Groups turns into a conversation. Use a stable ID for the lifetime of the conversation.
* `gen_ai.agent.name`: Groups conversations under a named agent in the Conversations tab.

Other GenAI semantic-convention attributes, such as `gen_ai.request.model`, `gen_ai.usage.input_tokens`, and `gen_ai.usage.output_tokens`, enrich the rendering with model names and token counts but are optional. For the agent data model that these spans map onto, see [Trace your agents](https://docs.coreweave.com/products/agent-lens/tracing/instrument.md#the-agent-data-model).

## Configure with environment variables only

If your application or collector reads the standard OTel exporter environment variables, you can set the following variables and route spans to Agent Lens without changing any code:

```bash lines theme={"system"}
export OTEL_EXPORTER_OTLP_TRACES_ENDPOINT="https://trace.wandb.ai/agents/otel/v1/traces"
export OTEL_EXPORTER_OTLP_TRACES_HEADERS="wandb-api-key=$WANDB_API_KEY"
export OTEL_RESOURCE_ATTRIBUTES="wandb.entity=[YOUR-TEAM],wandb.project=[YOUR-PROJECT]"
export OTEL_EXPORTER_OTLP_TRACES_PROTOCOL=http/protobuf
```

* `OTEL_EXPORTER_OTLP_TRACES_ENDPOINT`: The Agent Lens endpoint your exporter sends spans to.
* `OTEL_EXPORTER_OTLP_TRACES_HEADERS`: Authenticates each request with your Forge API key, sent in the `wandb-api-key` header.
* `OTEL_RESOURCE_ATTRIBUTES`: Sends spans to your project. Set `wandb.entity` to your Forge team or user name and `wandb.project` to the project name.
* `OTEL_EXPORTER_OTLP_TRACES_PROTOCOL`: Sets the exporter to send OTLP protobuf over HTTP. It must be `http/protobuf`, because the endpoint accepts only protobuf payloads.

## Example: emit agent spans without the Agent Lens SDK

The following example instruments one agent turn using only OTel packages. A user asks about the weather, the model calls a `get_weather` tool, and then the model answers with the result. The example emits an `invoke_agent` span for the turn, a `chat` span for each LLM call, and an `execute_tool` span for the tool call, then exports them to the Agent Lens agents endpoint.

The turn and each LLM call carry the user's prompt and the model's replies in `gen_ai.input.messages` and `gen_ai.output.messages`. The tool call carries its input and output in `gen_ai.tool.call.arguments` and `gen_ai.tool.call.result`. The example hardcodes these values. In your agent, record the real messages, tool results, and token counts.

First, install the required dependencies:

```bash Python theme={"system"}
pip install opentelemetry-sdk opentelemetry-exporter-otlp-proto-http
```

```bash TypeScript theme={"system"}
npm install @opentelemetry/api @opentelemetry/sdk-trace-node @opentelemetry/sdk-trace-base @opentelemetry/resources @opentelemetry/exporter-trace-otlp-proto
```

Set the `WANDB_API_KEY` environment variable to your [API key](https://forge.coreweave.com/settings#apikeys):

```bash theme={"system"}
export WANDB_API_KEY="[YOUR-API-KEY]"
```

Then replace `[YOUR-TEAM]` and `[YOUR-PROJECT]` in the following code with your Forge team and project names, and run it:

```python Python lines highlight="9,10" theme={"system"}
import json
import os
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk import trace as trace_sdk
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace.export import BatchSpanProcessor

ENTITY = "[YOUR-TEAM]"
PROJECT = "[YOUR-PROJECT]"

AGENT_LENS_OTLP_ENDPOINT = "https://trace.wandb.ai/agents/otel/v1/traces"

# Read the API key that you exported in the previous step.
WANDB_API_KEY = os.environ["WANDB_API_KEY"]

exporter = OTLPSpanExporter(
    endpoint=AGENT_LENS_OTLP_ENDPOINT,
    headers={"wandb-api-key": WANDB_API_KEY},
)

tracer_provider = trace_sdk.TracerProvider(resource=Resource({
    "wandb.entity": ENTITY,
    "wandb.project": PROJECT,
}))
tracer_provider.add_span_processor(BatchSpanProcessor(exporter))
trace.set_tracer_provider(tracer_provider)

tracer = trace.get_tracer("my-agent")

CONVERSATION_ID = "conversation-001"
TOOL_CALL_ID = "call-001"
ARGUMENTS = {"city": "Paris"}
WEATHER = {"temperature_c": 18, "conditions": "partly cloudy"}

# Each message has a role and a list of typed parts, per the GenAI semantic conventions.
user_message = {
    "role": "user",
    "parts": [{"type": "text", "content": "What's the weather in Paris?"}],
}
tool_call_message = {
    "role": "assistant",
    "parts": [{"type": "tool_call", "id": TOOL_CALL_ID, "name": "get_weather", "arguments": ARGUMENTS}],
}
tool_result_message = {
    "role": "tool",
    "parts": [{"type": "tool_call_response", "id": TOOL_CALL_ID, "response": WEATHER}],
}
answer_message = {
    "role": "assistant",
    "parts": [{"type": "text", "content": "It's 18°C and partly cloudy in Paris."}],
}

# One turn: the user asks a question, the model calls a tool, then answers.
with tracer.start_as_current_span("invoke_agent my-agent") as turn:
    turn.set_attribute("gen_ai.operation.name", "invoke_agent")
    turn.set_attribute("gen_ai.agent.name", "my-agent")
    turn.set_attribute("gen_ai.conversation.id", CONVERSATION_ID)
    turn.set_attribute("gen_ai.input.messages", json.dumps([user_message]))

    # First LLM call: the model asks to call a tool.
    with tracer.start_as_current_span("chat gpt-4o") as llm:
        llm.set_attribute("gen_ai.operation.name", "chat")
        llm.set_attribute("gen_ai.conversation.id", CONVERSATION_ID)
        llm.set_attribute("gen_ai.request.model", "gpt-4o")
        llm.set_attribute("gen_ai.input.messages", json.dumps([user_message]))
        llm.set_attribute("gen_ai.output.messages", json.dumps([tool_call_message]))
        llm.set_attribute("gen_ai.usage.input_tokens", 100)
        llm.set_attribute("gen_ai.usage.output_tokens", 20)

    # The tool runs under the turn, after the LLM call that requested it.
    with tracer.start_as_current_span("execute_tool get_weather") as tool:
        tool.set_attribute("gen_ai.operation.name", "execute_tool")
        tool.set_attribute("gen_ai.conversation.id", CONVERSATION_ID)
        tool.set_attribute("gen_ai.tool.name", "get_weather")
        tool.set_attribute("gen_ai.tool.call.id", TOOL_CALL_ID)
        tool.set_attribute("gen_ai.tool.call.arguments", json.dumps(ARGUMENTS))
        tool.set_attribute("gen_ai.tool.call.result", json.dumps(WEATHER))

    # Second LLM call: the model answers from the tool result.
    with tracer.start_as_current_span("chat gpt-4o") as llm:
        llm.set_attribute("gen_ai.operation.name", "chat")
        llm.set_attribute("gen_ai.conversation.id", CONVERSATION_ID)
        llm.set_attribute("gen_ai.request.model", "gpt-4o")
        llm.set_attribute("gen_ai.input.messages", json.dumps(
            [user_message, tool_call_message, tool_result_message]
        ))
        llm.set_attribute("gen_ai.output.messages", json.dumps([answer_message]))
        llm.set_attribute("gen_ai.usage.input_tokens", 140)
        llm.set_attribute("gen_ai.usage.output_tokens", 15)

    turn.set_attribute("gen_ai.output.messages", json.dumps([answer_message]))

tracer_provider.shutdown()  # Flush all pending spans before exit.
```

```typescript TypeScript lines highlight="7,8" theme={"system"}
import { trace } from "@opentelemetry/api";
import { NodeTracerProvider } from "@opentelemetry/sdk-trace-node";
import { BatchSpanProcessor } from "@opentelemetry/sdk-trace-base";
import { OTLPTraceExporter } from "@opentelemetry/exporter-trace-otlp-proto";
import { resourceFromAttributes } from "@opentelemetry/resources";

const ENTITY = "[YOUR-TEAM]";
const PROJECT = "[YOUR-PROJECT]";

const AGENT_LENS_OTLP_ENDPOINT = "https://trace.wandb.ai/agents/otel/v1/traces";

// Read the API key that you exported in the previous step.
const WANDB_API_KEY = process.env.WANDB_API_KEY!;

const exporter = new OTLPTraceExporter({
  url: AGENT_LENS_OTLP_ENDPOINT,
  headers: { "wandb-api-key": WANDB_API_KEY },
});

const provider = new NodeTracerProvider({
  resource: resourceFromAttributes({
    "wandb.entity": ENTITY,
    "wandb.project": PROJECT,
  }),
  spanProcessors: [new BatchSpanProcessor(exporter)],
});

provider.register();

const tracer = trace.getTracer("my-agent");

const CONVERSATION_ID = "conversation-001";
const TOOL_CALL_ID = "call-001";
const ARGUMENTS = { city: "Paris" };
const WEATHER = { temperature_c: 18, conditions: "partly cloudy" };

// Each message has a role and a list of typed parts, per the GenAI semantic conventions.
const userMessage = {
  role: "user",
  parts: [{ type: "text", content: "What's the weather in Paris?" }],
};
const toolCallMessage = {
  role: "assistant",
  parts: [{ type: "tool_call", id: TOOL_CALL_ID, name: "get_weather", arguments: ARGUMENTS }],
};
const toolResultMessage = {
  role: "tool",
  parts: [{ type: "tool_call_response", id: TOOL_CALL_ID, response: WEATHER }],
};
const answerMessage = {
  role: "assistant",
  parts: [{ type: "text", content: "It's 18°C and partly cloudy in Paris." }],
};

// One turn: the user asks a question, the model calls a tool, then answers.
tracer.startActiveSpan("invoke_agent my-agent", (turn) => {
  turn.setAttribute("gen_ai.operation.name", "invoke_agent");
  turn.setAttribute("gen_ai.agent.name", "my-agent");
  turn.setAttribute("gen_ai.conversation.id", CONVERSATION_ID);
  turn.setAttribute("gen_ai.input.messages", JSON.stringify([userMessage]));

  // First LLM call: the model asks to call a tool.
  tracer.startActiveSpan("chat gpt-4o", (llm) => {
    llm.setAttribute("gen_ai.operation.name", "chat");
    llm.setAttribute("gen_ai.conversation.id", CONVERSATION_ID);
    llm.setAttribute("gen_ai.request.model", "gpt-4o");
    llm.setAttribute("gen_ai.input.messages", JSON.stringify([userMessage]));
    llm.setAttribute("gen_ai.output.messages", JSON.stringify([toolCallMessage]));
    llm.setAttribute("gen_ai.usage.input_tokens", 100);
    llm.setAttribute("gen_ai.usage.output_tokens", 20);
    llm.end();
  });

  // The tool runs under the turn, after the LLM call that requested it.
  tracer.startActiveSpan("execute_tool get_weather", (tool) => {
    tool.setAttribute("gen_ai.operation.name", "execute_tool");
    tool.setAttribute("gen_ai.conversation.id", CONVERSATION_ID);
    tool.setAttribute("gen_ai.tool.name", "get_weather");
    tool.setAttribute("gen_ai.tool.call.id", TOOL_CALL_ID);
    tool.setAttribute("gen_ai.tool.call.arguments", JSON.stringify(ARGUMENTS));
    tool.setAttribute("gen_ai.tool.call.result", JSON.stringify(WEATHER));
    tool.end();
  });

  // Second LLM call: the model answers from the tool result.
  tracer.startActiveSpan("chat gpt-4o", (llm) => {
    llm.setAttribute("gen_ai.operation.name", "chat");
    llm.setAttribute("gen_ai.conversation.id", CONVERSATION_ID);
    llm.setAttribute("gen_ai.request.model", "gpt-4o");
    llm.setAttribute(
      "gen_ai.input.messages",
      JSON.stringify([userMessage, toolCallMessage, toolResultMessage]),
    );
    llm.setAttribute("gen_ai.output.messages", JSON.stringify([answerMessage]));
    llm.setAttribute("gen_ai.usage.input_tokens", 140);
    llm.setAttribute("gen_ai.usage.output_tokens", 15);
    llm.end();
  });

  turn.setAttribute("gen_ai.output.messages", JSON.stringify([answerMessage]));
  turn.end();
});

// Flush all pending spans before exit.
provider.shutdown().catch(console.error);
```

To add more turns to the same conversation, emit more `invoke_agent` spans with the same `gen_ai.conversation.id`. Each turn is the root span of its own trace, so turns don't need to share a parent span. Give all of a turn's spans timestamps from one clock, and end the turn's span after its children. See [Keep span timing consistent](https://docs.coreweave.com/products/agent-lens/tracing/instrument.md#keep-span-timing-consistent).

After your application exports spans, open the **Conversations** view of your Agent Lens project.
