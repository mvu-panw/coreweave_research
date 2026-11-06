# set_auth_mode

Source: https://docs.coreweave.com/products/sandboxes/client/ref/configuration/set-auth-mode

# set_auth_mode

> Set the legacy process-global auth mode.

Source: [src/cwsandbox/\_auth.py:158](https://github.com/coreweave/cwsandbox-client/blob/v1.14.2/src/cwsandbox/_auth.py#L158)

```python theme={"system"}
set_auth_mode(name: str, get_auth: Callable[[], AuthHeaders]) -> None
```

Set the legacy process-global auth mode.

New integrations should pass `auth=` to `Sandbox`, `Session`, or
class-level operations instead. This hook remains for compatibility with
integrations that install an auth mode at import time.
