# Containers

Source: https://docs.coreweave.com/products/sandboxes/client/ref/workload/containers

# Containers

> Container definitions, observed container state, and per-container privilege.

## Container

Source: [src/cwsandbox/\_types.py:1181](https://github.com/coreweave/cwsandbox-client/blob/v1.14.2/src/cwsandbox/_types.py#L1181)

```python theme={"system"}
class Container(*, image: str, name: str | None = None, command: str | None = None, args: Sequence[str] | None = None, environment_variables: Mapping[str, str] | None = None, resources: ResourceOptions | dict[str, Any] | None = None, mounted_files: Sequence[Mapping[str, Any]] | None = None, volume_mounts: Sequence[VolumeMount | Mapping[str, Any]] | None = None, secrets: Sequence[Secret | Mapping[str, Any]] | None = None, working_dir: str | None = None, image_pull_credentials: ImagePullCredentials | Mapping[str, Any] | None = None, primary: bool = False)
```

One user container in a sandbox.

Pass a list to `Sandbox.run(containers=[...])`. That form is mutually
exclusive with the single-container kwargs (`container_image`,
`command`/`args`, `resources`, `mounted_files`, `secrets`,
`image_pull_credentials`, `environment_variables`,
`security_context`, `working_dir`) and does not inherit those
same fields from `SandboxDefaults`.

One container: `primary` may be omitted or False (that row is primary).
More than one: exactly one row must set `primary=True`, and every row
needs a name and resources. GPU is allowed only on the primary.

**Attributes**

* `name` (`str | None`) : DNS-1123 label. Optional for a single container; required when
  more than one container is specified.
* `command` (`str | None`) : Entrypoint. Empty/None uses the image entrypoint. Args may
  be set without command.
* `args` (`Sequence[str] | None`) : Arguments to the command or image entrypoint.
* `environment_variables` (`Mapping[str, str] | None`) : Env vars injected into this container only.
* `resources` (`ResourceOptions | dict[str, Any] | None`) : CPU/memory/GPU for this container. Required when more
  than one container is specified.
* `mounted_files` (`Sequence[Mapping[str, Any]] | None`) : Files written into this container at startup.
* `volume_mounts` (`Sequence[VolumeMount | Mapping[str, Any]] | None`) : Sandbox-level volumes to mount into this container.
* `secrets` (`Sequence[Secret | Mapping[str, Any]] | None`) : Secret-store inject for this container only.
* `working_dir` (`str | None`) : Working directory for the command. Must be absolute
  when set.
* `image_pull_credentials` (`ImagePullCredentials | Mapping[str, Any] | None`) : Private-registry pull credentials.
* `primary` (`bool`) : When True, this container owns sandbox lifecycle and is
  the default exec/logs/files target. Default: `False`.

***

## ContainerStatus

Source: [src/cwsandbox/\_sandbox.py:335](https://github.com/coreweave/cwsandbox-client/blob/v1.14.2/src/cwsandbox/_sandbox.py#L335)

```python theme={"system"}
class ContainerStatus(*, name: str, state: SandboxStatus, exit_code: int | None = None, restart_count: int = 0)
```

Observed state of one container on a sandbox.

Sandbox `status` / `returncode` stay primary-owned. This row is the
kubelet's view of that named container.

**Attributes**

* `exit_code` (`int | None`) : Exit code once the container is in a terminal state.
  None while the container is still running.
* `restart_count` (`int`) : Times the container has restarted. Default: `0`.

***

## SecurityContext

Source: [src/cwsandbox/\_types.py:993](https://github.com/coreweave/cwsandbox-client/blob/v1.14.2/src/cwsandbox/_types.py#L993)

```python theme={"system"}
class SecurityContext(*, run_as_user: int | None = None, run_as_group: int | None = None, privileged: bool | None = None, allow_privilege_escalation: bool | None = None, read_only_root_filesystem: bool | None = None, capabilities_add: Sequence[str] | None = None, capabilities_drop: Sequence[str] | None = None, seccomp_profile: str | None = None)
```

In-guest container privilege, clamped by the runner policy.

Host-reaching settings (host network, host PID, hostPath) are not
expressible here. `privileged`, capabilities, run-as, and seccomp
apply inside the sandbox isolation boundary.

**Attributes**

* `run_as_user` (`int | None`) : UID for the entrypoint. Unset uses the image user.
* `run_as_group` (`int | None`) : GID for the entrypoint. Unset uses the image group.
* `privileged` (`bool | None`) : Run privileged inside the isolation boundary.
* `allow_privilege_escalation` (`bool | None`) : Allow a process to gain more privileges
  than its parent.
* `read_only_root_filesystem` (`bool | None`) : Mount the container root filesystem read-only.
* `capabilities_add` (`Sequence[str] | None`) : Linux capabilities to add (e.g. `"SYS_PTRACE"`).
* `capabilities_drop` (`Sequence[str] | None`) : Linux capabilities to drop.
* `seccomp_profile` (`str | None`) : `"RuntimeDefault"` or `"Unconfined"`.

***

## ImagePullCredentials

Source: [src/cwsandbox/\_types.py:912](https://github.com/coreweave/cwsandbox-client/blob/v1.14.2/src/cwsandbox/_types.py#L912)

```python theme={"system"}
class ImagePullCredentials(*, registry: str, store: str, name: str, field: str = '')
```

Private-registry pull credentials resolved from a secret store.

**Attributes**

* `field` (`str`) : Optional structured-secret field. Default: `''`.

***
