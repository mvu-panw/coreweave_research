# Setup and shutdown

Source: https://docs.coreweave.com/products/agent-lens/reference/python-sdk/setup

# Setup and shutdown

> Start, flush, and stop tracing with init, force_flush, shutdown, and TracingSession.

Access these through the `tracing` module:

```python theme={"system"}
from coreweave.forge.agentlens import tracing
```

## init

```python theme={"system"}
def init(
    project_name: str,
    *,
    api_key: Union[str, None] = None,
    base_url: Union[str, None] = None,
    service_name: str = 'coreweave-forge-sdk',
    autopatch_integrations: bool = True,
) -> TracingSession: ...
```

Start exporting package-created agent spans to an Agent Lens project.

`project_name` must be `entity/project`; this package deliberately does not
depend on W\&B account APIs to discover a default entity. Credentials come
from `api_key`, `WANDB_API_KEY`, or the W\&B host entry in `.netrc`.
`autopatch_integrations=True` patches supported provider SDKs already in
`sys.modules` and watches for providers imported later.
Reinitialization flushes the previous session and reroutes new spans to the
new project. Spans that are still open keep exporting to the project they
started in; the previous session is closed by the next `init` or by
`shutdown`.

## force\_flush

```python theme={"system"}
def force_flush(timeout_millis: int = 30000) -> bool: ...
```

## shutdown

```python theme={"system"}
def shutdown() -> None: ...
```

## TracingSession

```python theme={"system"}
@dataclass
class TracingSession: ...
```

Owns the OTLP provider and its background export worker.

**Fields**

| Field | Type | Default |
| - | - | - |
| `provider` | `TracerProvider` | Required |
| `endpoint` | `str` | Required |
| `project_id` | `str` | Required |

### TracingSession.force\_flush

```python theme={"system"}
def force_flush(timeout_millis: int = 30000) -> bool: ...
```

### TracingSession.shutdown

```python theme={"system"}
def shutdown() -> None: ...
```
