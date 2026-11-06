# AuthProvider

Source: https://docs.coreweave.com/products/sandboxes/client/ref/configuration/auth-provider

# AuthProvider

> Provider that resolves authentication for a Sandbox API endpoint.

Source: [src/cwsandbox/\_auth.py:42](https://github.com/coreweave/cwsandbox-client/blob/v1.14.2/src/cwsandbox/_auth.py#L42)

```python theme={"system"}
class AuthProvider
```

Provider that resolves authentication for a Sandbox API endpoint.

## Methods

### resolve\_auth

```python theme={"system"}
resolve_auth(*, base_url: str) -> AuthHeaders
```

Resolve headers for `base_url` or raise an authentication error.
