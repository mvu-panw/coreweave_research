# Integrations

Source: https://docs.coreweave.com/products/agent-lens/reference/python-sdk/integrations

# Integrations

> Patch the OpenAI, Anthropic, and Google Gen AI SDKs so their calls are traced automatically.

Automatic tracing integrations for optional Python provider SDKs.

Access these through the `integrations` module:

```python theme={"system"}
from coreweave.forge.agentlens.tracing import integrations
```

## autopatch

```python theme={"system"}
def autopatch() -> None: ...
```

Patch loaded providers and watch for providers imported later.

## disable\_autopatch

```python theme={"system"}
def disable_autopatch() -> None: ...
```

Stop watching future imports; already-patched symbols stay patched.

## patch\_openai

```python theme={"system"}
def patch_openai() -> bool: ...
```

Patch installed OpenAI SDK methods. Safe to call repeatedly.

## unpatch\_openai

```python theme={"system"}
def unpatch_openai() -> bool: ...
```

Restore OpenAI SDK methods replaced by Forge.

## patch\_anthropic

```python theme={"system"}
def patch_anthropic() -> bool: ...
```

Patch installed Anthropic SDK methods. Safe to call repeatedly.

## unpatch\_anthropic

```python theme={"system"}
def unpatch_anthropic() -> bool: ...
```

Restore Anthropic SDK methods replaced by Forge.

## patch\_google\_genai

```python theme={"system"}
def patch_google_genai() -> bool: ...
```

Patch installed Google Gen AI SDK methods. Safe to call repeatedly.

## unpatch\_google\_genai

```python theme={"system"}
def unpatch_google_genai() -> bool: ...
```

Restore Google Gen AI SDK methods replaced by Forge.

## unpatch\_all

```python theme={"system"}
def unpatch_all() -> None: ...
```

Restore every provider patched by this package.
