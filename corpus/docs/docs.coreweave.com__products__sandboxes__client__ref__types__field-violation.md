# FieldViolation

Source: https://docs.coreweave.com/products/sandboxes/client/ref/types/field-violation

# FieldViolation

> Field-level validation failure returned by the backend.

Source: [src/cwsandbox/exceptions.py:56](https://github.com/coreweave/cwsandbox-client/blob/v1.14.2/src/cwsandbox/exceptions.py#L56)

```python theme={"system"}
class FieldViolation(field: str = '', description: str = '')
```

Field-level validation failure returned by the backend.

**Attributes**

* `field` (`str`) : Default: `''`.
* `description` (`str`) : Default: `''`.
