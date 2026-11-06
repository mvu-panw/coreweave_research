# Secret

Source: https://docs.coreweave.com/products/sandboxes/client/ref/configuration/secret

# Secret

> A secret to inject from a store into a sandbox environment variable.

Source: [src/cwsandbox/\_types.py:1087](https://github.com/coreweave/cwsandbox-client/blob/v1.14.2/src/cwsandbox/_types.py#L1087)

```python theme={"system"}
class Secret(*, store: str, name: str, field: str = '', env_var: str | None = None)
```

A secret to inject from a store into a sandbox environment variable.

All fields are keyword-only. When `env_var` is not specified it defaults
to `name`. Plain dicts with matching keys are also accepted and
converted automatically.

**Attributes**

* `field` (`str`) : Specific field within a structured secret (optional). Default: `''`.
* `env_var` (`str | None`) : Environment variable the secret is injected as (defaults to name).
