# login()

Source: https://docs.coreweave.com/products/wandb/ref/python/functions/login

# login()

[View source](https://github.com/wandb/wandb/blob/main/wandb/sdk/wandb_login.py#L24)

## function wandb.login()

Log into W\&B.

You generally don't have to use this because most W\&B methods that need
authentication can log in implicitly. This is the programmatic counterpart
to the `wandb login` CLI.

This updates global credentials for the session (affecting all wandb usage
in the current Python process after this call) and possibly the .netrc file.

If an identity token file is configured, like through the
WANDB\_IDENTITY\_TOKEN\_FILE environment variable, then it is used for the
session (federated identity) and no API key is read or saved.

Otherwise, if an explicit API key is provided, it is used and written to
the system .netrc file. If no key is provided, but the session is already
authenticated, then the session key is used for verification (if verify
is True) and the .netrc file is not updated.

If none of the above is true, then this gets the API key from the first of:

* The WANDB\_API\_KEY environment variable
* The api\_key setting in a system or workspace settings file
* The .netrc file (either \~/.netrc, \~/\_netrc or the path specified by the
  NETRC environment variable)
* An interactive prompt, if available and `prompt` is True

```python theme={"system"}
key: 'str | None' = None,
relogin: 'bool | None' = None,
host: 'str | None' = None,
force: 'bool | None' = None,
timeout: 'int | None' = None,
verify: 'bool' = True,
referrer: 'str | None' = None,
prompt: 'bool' = True,
anonymous: 'DoNotSet' = DoNotSet
```

## Args

**key** `str | None`

The API key to use.

**relogin** `bool | None`

If true, get the API key from an interactive prompt, skipping reading .netrc, environment variables, etc.

**host** `str | None`

The W\&B server URL to connect to.

**force** `bool | None`

If true, disallows selecting offline mode in the interactive prompt.

**timeout** `int | None`

Number of seconds to wait for user input in the interactive prompt. This can be used as a failsafe if an interactive prompt is incorrectly shown in a non-interactive environment.

**verify** `bool`

Verify the credentials with the W\&B server and raise an AuthenticationError on failure. This works for API keys as well as identity tokens.

**referrer** `str | None`

The referrer to use in the URL login request for analytics.

**prompt** `bool`

Whether to ask for an API key interactively when none is configured. If False, this returns False and leaves the session and settings unchanged.

**anonymous** `DoNotSet`

No description provided.

## Returns

True if the session has credentials after this call.

## Raises

* `AuthenticationError`: If the credentials fail verification with the server.
* `UsageError`: If no credentials are configured, `prompt` is True and there is no terminal to ask for an API key.
