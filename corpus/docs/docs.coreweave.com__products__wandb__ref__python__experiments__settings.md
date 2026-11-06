# Settings

Source: https://docs.coreweave.com/products/wandb/ref/python/experiments/settings

# Settings

[View source](https://github.com/wandb/wandb/blob/main/wandb/sdk/wandb_settings.py#L73)

## Class wandb.Settings

Settings for the W\&B SDK.

This class manages configuration settings for the W\&B SDK,
ensuring type safety and validation of all settings. Settings are accessible
as attributes and can be initialized programmatically, through environment
variables (`WANDB_ prefix`), and with configuration files.

The settings are organized into three categories:

1. Public settings: Core configuration options that users can safely modify to customize
   W\&B's behavior for their specific needs.
2. Internal settings: Settings prefixed with 'x\_' that handle low-level SDK behavior.
   These settings are primarily for internal use and debugging. While they can be modified,
   they are not considered part of the public API and may change without notice in future
   versions.
3. Computed settings: Read-only settings that are automatically derived from other settings or
   the environment.

Settings are loaded from multiple sources. When the same setting is supplied
by more than one source, the source listed later wins. From lowest to highest
precedence:

1. Default values defined on this `Settings` model.
2. Configuration files (`~/.config/wandb/settings`, or the `settings` file in
   the directory named by the `WANDB_CONFIG_DIR` environment variable).
3. Environment variables (those prefixed with `WANDB_`, e.g. `WANDB_MODE`).
4. Values detected from the runtime environment, such as the hostname, the
   running program/script path, the Python executable, the Docker image, and
   Jupyter notebook details.
5. SageMaker settings, when running in an Amazon SageMaker environment.
6. The `settings` parameter of `wandb.setup()`.
7. The `settings` parameter of `wandb.init()`.
8. Certain `wandb.init()` parameters (for example, `mode=` overrides the
   `mode` setting).

```python theme={"system"}
*,
allow_media_symlink: bool = False,
allow_offline_artifacts: bool = True,
allow_val_change: bool = False,
anonymous: object = object(),
api_key: str | None = None,
azure_account_url_to_access_key: dict[str, str] | None = None,
app_url_override: str | None = None,
base_url: str = 'https://api.forge.coreweave.com',
code_dir: str | None = None,
config_paths: collections.abc.Sequence[str] | None = None,
console: Literal['auto', 'off', 'wrap', 'redirect', 'wrap_raw', 'wrap_emu'] = 'auto',
console_multipart: bool = False,
console_chunk_max_bytes: int = 0,
console_chunk_max_seconds: int = 0,
capture_loggers: dict[str, str] | None = None,
credentials_file: str = <factory>,
disable_code: bool = False,
disable_git: bool = False,
disable_git_fork_point: bool = True,
disable_job_creation: bool = True,
docker: str | None = None,
email: str | None = None,
entity: str | None = None,
organization: str | None = None,
force: bool = False,
fork_from: wandb.sdk.lib.run_moment.RunMoment | None = None,
git_commit: str | None = None,
git_remote: str = 'origin',
git_remote_url: str | None = None,
git_root: str | None = None,
heartbeat_seconds: int = 30,
host: str | None = None,
http_proxy: str | None = None,
https_proxy: str | None = None,
identity_token_file: str | None = None,
ignore_globs: collections.abc.Sequence[str] = (),
init_timeout: float = 90.0,
finish_timeout: float = 0.0,
finish_timeout_raises: bool = False,
insecure_disable_ssl: bool = False,
job_name: str | None = None,
job_source: Optional[Literal['repo', 'artifact', 'image']] = None,
label_disable: bool = False,
launch: bool = False,
launch_config_path: str | None = None,
login_timeout: float | None = None,
mode: Literal['online', 'offline', 'shared', 'disabled', 'dryrun', 'run'] = 'online',
notebook_name: str | None = None,
program: str | None = None,
program_abspath: str | None = None,
program_relpath: str | None = None,
project: str | None = None,
quiet: bool = False,
reinit: Union[Literal['default', 'return_previous', 'finish_previous', 'create_new'], bool] = 'default',
relogin: bool = False,
resume: Optional[Literal['allow', 'must', 'never', 'auto']] = None,
resume_from: wandb.sdk.lib.run_moment.RunMoment | None = None,
resumed: bool = False,
root_dir: str = <factory>,
run_group: str | None = None,
run_id: str | None = None,
run_job_type: str | None = None,
run_name: str | None = None,
run_notes: str | None = None,
run_tags: tuple[str, ...] | None = None,
sagemaker_disable: bool = False,
save_code: bool | None = None,
settings_system: str | None = None,
stop_fn: collections.abc.Callable[[], None] | None = None,
max_end_of_run_history_metrics: int = 10,
max_end_of_run_summary_metrics: int = 10,
show_colors: bool | None = None,
show_emoji: bool | None = None,
show_errors: bool = True,
show_info: bool = True,
show_warnings: bool = True,
silent: bool = False,
stop_on_fatal_error: bool = False,
strict: bool | None = None,
summary_timeout: int = 60,
summary_warnings: int = 5,
sweep_id: str | None = None,
sweep_param_path: str | None = None,
symlink: bool = <factory>,
sync_tensorboard: bool | None = None,
table_raise_on_max_row_limit_exceeded: bool = False,
use_dot_wandb: bool | None = None,
username: str | None = None,
x_cli_only_mode: bool = False,
x_disable_meta: bool = False,
x_disable_stats: bool = False,
x_disable_viewer: bool = False,
x_disable_machine_info: bool = False,
x_executable: str | None = None,
x_extra_http_headers: dict[str, str] | None = None,
x_file_stream_max_bytes: int | None = None,
x_file_stream_max_line_bytes: int | None = None,
x_file_stream_transmit_interval: float | None = None,
x_file_stream_no_gzip: bool = True,
x_file_stream_retry_max: int | None = None,
x_file_stream_retry_wait_min_seconds: float | None = None,
x_file_stream_retry_wait_max_seconds: float | None = None,
x_file_stream_timeout_seconds: float | None = None,
x_file_transfer_retry_max: int | None = None,
x_file_transfer_retry_wait_min_seconds: float | None = None,
x_file_transfer_retry_wait_max_seconds: float | None = None,
x_file_transfer_timeout_seconds: float | None = None,
x_files_dir: str | None = None,
x_flow_control_custom: bool | None = None,
x_flow_control_disabled: bool | None = None,
x_graphql_retry_max: int | None = None,
x_graphql_retry_wait_min_seconds: float | None = None,
x_graphql_retry_wait_max_seconds: float | None = None,
x_graphql_timeout_seconds: float | None = None,
x_history_value_encoding: str = 'json',
x_internal_check_process: float = 8.0,
x_jupyter_name: str | None = None,
x_jupyter_path: str | None = None,
x_jupyter_root: str | None = None,
x_label: str | None = None,
x_live_policy_rate_limit: int | None = None,
x_live_policy_wait_time: int | None = None,
x_log_level: int = 20,
x_network_buffer: int | None = None,
x_primary: bool = True,
x_proxies: dict[str, str] | None = None,
x_runqueue_item_id: str | None = None,
x_save_requirements: bool = True,
x_server_side_derived_summary: bool = False,
x_service_transport: str | None = None,
x_service_wait: float = 30.0,
x_skip_transaction_log: bool = False,
x_start_time: float | None = None,
x_stats_pid: int = 53463,
x_stats_sampling_interval: float = 15.0,
x_stats_neuron_monitor_config_path: str | None = None,
x_stats_dcgm_exporter: str | None = None,
x_stats_open_metrics_endpoints: dict[str, str] | None = None,
x_stats_open_metrics_filters: dict[str, dict[str, str]] | collections.abc.Sequence[str] | None = None,
x_stats_open_metrics_http_headers: dict[str, str] | None = None,
x_stats_disk_paths: collections.abc.Sequence[str] | None = ('/',),
x_stats_cpu_count: int | None = None,
x_stats_cpu_logical_count: int | None = None,
x_stats_gpu_count: int | None = None,
x_stats_gpu_type: str | None = None,
x_stats_gpu_device_ids: collections.abc.Sequence[int] | None = None,
x_stats_buffer_size: int = 0,
x_stats_coreweave_metadata_base_url: str = 'http://169.254.169.254',
x_stats_coreweave_metadata_endpoint: str = '/api/v2/cloud-init/meta-data',
x_stats_track_process_tree: bool = False,
x_stats_no_cgroup: bool = False,
x_stats_self_usage: bool = False,
x_sync: bool = False,
x_sync_dir_suffix: str = '',
x_transaction_log_flush_interval: float = 15.0,
x_update_finish_state: bool = True
```

## Args

**allow\_media\_symlink** `bool`

Whether to symlink media files to the run directory.

If true, media files will be symlinked or hardlinked to the
run directory instead of copied. This may result in faster
logging and reduced disk usage. However, deleting or modifying
the original files before upload to the W\&B server will be
reflected in the uploaded data.

**allow\_offline\_artifacts** `bool`

Flag to allow table artifacts to be synced in offline mode.

To revert to the old behavior, set this to False.

**allow\_val\_change** `bool`

Flag to allow modification of `Config` values after they've been set.

**anonymous** `object`

Deprecated and will be removed.

**api\_key** `str | None`

The W\&B API key.

**azure\_account\_url\_to\_access\_key** `dict[str, str] | None`

Mapping of Azure account URLs to their corresponding access keys for Azure integration.

**app\_url\_override** `str | None`

Override for the 'app' URL for the W\&B UI.

The `app_url` is normally computed based on `base_url`, but this can be
used to set it explicitly.

WANDB\_APP\_URL is the corresponding environment variable.

**base\_url** `str`

The URL of the W\&B backend for data synchronization.

**code\_dir** `str | None`

Directory containing the code to be tracked by W\&B.

**config\_paths** `collections.abc.Sequence[str] | None`

Paths to files to load configuration from into the `Config` object.

**console** `Literal`

The type of console capture to be applied.

Possible values are:

* "auto" - Automatically selects the console capture method based on the
  system environment and settings.
* "off" - Disables console capture.
* "redirect" - Redirects low-level file descriptors for capturing output.
* "wrap" - Overrides the write methods of sys.stdout/sys.stderr. Will be
  mapped to either "wrap\_raw" or "wrap\_emu" based on the state of the system.
* "wrap\_raw" - Same as "wrap" but captures raw output directly instead of
  through an emulator. Derived from the `wrap` setting and should not be set manually.
* "wrap\_emu" - Same as "wrap" but captures output through an emulator.
  Derived from the `wrap` setting and should not be set manually.

**console\_multipart** `bool`

Enable multipart console logging.

When True, the SDK writes console output to timestamped files
under the `logs/` directory instead of a single `output.log`.

Each part is uploaded as soon as it is closed, giving users live
access to logs while the run is active. Rollover cadence is
controlled by `console_chunk_max_bytes` and/or `console_chunk_max_seconds`.
If both limits are `0`, all logs are uploaded once at run finish.

Note: Uploaded chunks are immutable; terminal control sequences
that modify previous lines (e.g., progress bars using carriage returns)
only affect the current chunk.

**console\_chunk\_max\_bytes** `int`

Size-based rollover threshold for multipart console logs, in bytes.

Starts a new console log file when the current part reaches this
size. Has an effect only when `console_multipart` is `True`.
Can be combined with `console_chunk_max_seconds`; whichever limit is
hit first triggers the rollover. A value of `0` disables the
size-based limit.

**console\_chunk\_max\_seconds** `int`

Time-based rollover threshold for multipart console logs, in seconds.

Starts a new console log file after this many seconds have elapsed
since the current part began. Requires `console_multipart` to be
`True`.  May be used with `console_chunk_max_bytes`; the first limit
reached closes the part. A value of `0` disables the time-based
limit.

**capture\_loggers** `dict[str, str] | None`

Names of Python loggers to capture into the run's Logs tab.

A mapping of logger name to minimum log level. When set, wandb installs a
logging.Handler on each named logger and removes it when the run finishes.
Log records emitted by those loggers are published as console output to the
run, similar to stdout/stderr capture.

Log records are formatted the same as `logging.basicConfig()`, like
`INFO:my_module:Some message.` This is not currently customizable.

To capture all logs, pass the name of the root logger, which is 'root'.

This is independent of the `console` setting: both can be active
simultaneously.

Example:

```python theme={"system"}
wandb.init(
    settings=wandb.Settings(
        console="off",
        capture_loggers={
            "my_app": "INFO",
            "my_app.training": "ERROR",
        },
    ),
)
```

**credentials\_file** `str`

Path to file for writing temporary access tokens.

**disable\_code** `bool`

Whether to disable capturing the code.

**disable\_git** `bool`

Whether to disable capturing the git state.

**disable\_git\_fork\_point** `bool`

Whether to disable inferring fork point from remote branches

When set to True, the SDK will use the latest commit from the upstream
branch, if one is set. Otherwise skip generating the diff patch.

When set to False, the SDK will try to use the latest commit from the upstream branch,
if one is set.
Otherwise, it will find the closest commit from all remote branches.
This may impact performance for repos with many upstream branches.

**disable\_job\_creation** `bool`

Whether to disable the creation of a job artifact for W\&B Launch.

**docker** `str | None`

The Docker image used to execute the script.

**email** `str | None`

The email address of the user.

**entity** `str | None`

The W\&B entity, such as a user or a team.

**organization** `str | None`

The W\&B organization.

**force** `bool`

Whether to pass the `force` flag to `wandb.login()`.

**fork\_from** `wandb.sdk.lib.run_moment.RunMoment | None`

Specifies a point in a previous execution of a run to fork from.

The point is defined by the run ID, a metric, and its value.
Currently, only the metric '\_step' is supported.

**git\_commit** `str | None`

The git commit hash to associate with the run.

**git\_remote** `str`

The git remote to associate with the run.

**git\_remote\_url** `str | None`

The URL of the git remote repository.

**git\_root** `str | None`

Root directory of the git repository.

**host** `str | None`

Hostname of the machine running the script.

**http\_proxy** `str | None`

Custom proxy servers for http requests to W\&B.

**https\_proxy** `str | None`

Custom proxy servers for https requests to W\&B.

**identity\_token\_file** `str | None`

Path to file containing an identity token (JWT) for authentication.

**ignore\_globs** `Sequence`

Unix glob patterns relative to `files_dir` specifying files to exclude from upload.

**init\_timeout** `float`

Time in seconds to wait for the `wandb.init` call to complete before timing out.

**finish\_timeout** `float`

Time in seconds to wait for data to upload at the end of a run.

Setting this can limit costs caused by slow uploads to W\&B at the end of a
run, with the trade-off that the run will be marked crashed and may be
missing some data. The default is for `run.finish()` to block until all
data finishes uploading.

If this is set to a number greater than zero, W\&B gives up on uploading a
run's data after this many seconds at the end of a run, unblocking your
script. After some time, the run becomes Crashed or Failed in the UI. Any
unuploaded data is still stored on disk and can be uploaded with `wandb
  sync`.

Use the `finish_timeout_raises` setting to raise an error in addition to
printing a warning message.

Runs shut down by `wandb.teardown()` (which automatically runs at the end
of a script in an atexit hook) will also respect this setting.

**finish\_timeout\_raises** `bool`

Whether to raise a TimeoutError if finish\_timeout expires.

Using this together with the `finish_timeout` setting causes `run.finish()`
to raise a TimeoutError after a timeout in addition to printing a message.

Note that `run.finish()` is called implicitly when using a Run as a context
manager:

with wandb.init() as run:
...  # run.finish() executes at the end of the `with` block

This does not cause `wandb.teardown()` to raise an error (since it runs
at the end of a script anyway).

**insecure\_disable\_ssl** `bool`

Whether to insecurely disable SSL verification.

**job\_name** `str | None`

Name of the Launch job running the script.

**job\_source** `Optional`

Source type for Launch.

**label\_disable** `bool`

Whether to disable automatic labeling features.

**launch\_config\_path** `str | None`

Path to the launch configuration file.

**login\_timeout** `float | None`

Time in seconds to wait for login operations before timing out.

**mode** `Literal`

The operating mode for W\&B logging and synchronization.

**notebook\_name** `str | None`

Name of the notebook if running in a Jupyter-like environment.

**program** `str | None`

Path to the script that created the run, if available.

**program\_abspath** `str | None`

The absolute path from the root repository directory to the script that
created the run.

Root repository directory is defined as the directory containing the
.git directory, if it exists. Otherwise, it's the current working directory.

**program\_relpath** `str | None`

The relative path to the script that created the run.

**project** `str | None`

The W\&B project ID.

**quiet** `bool`

Flag to suppress non-essential output.

**reinit** `Union`

What to do when `wandb.init()` is called while a run is active.

Options:

* "default": Use "finish\_previous" in notebooks and "return\_previous"
  otherwise.
* "return\_previous": Return the most recently created run
  that is not yet finished. This does not update `wandb.run`; see
  the "create\_new" option.
* "finish\_previous": Finish all active runs, then return a new run.
* "create\_new": Create a new run without modifying other active runs.
  Does not update `wandb.run` and top-level functions like `wandb.log`.
  Because of this, some older integrations that rely on the global run
  will not work.

Can also be a boolean, but this is deprecated. False is the same as
"return\_previous", and True is the same as "finish\_previous".

**relogin** `bool`

Flag to force a new login attempt.

**resume** `Optional`

Specifies the resume behavior for the run.

Options:

* "must": Resumes from an existing run with the same ID. If no such run exists,
  it will result in failure.
* "allow": Attempts to resume from an existing run with the same ID. If none is
  found, a new run will be created.
* "never": Always starts a new run. If a run with the same ID already exists,
  it will result in failure.
* "auto": Automatically resumes from the most recent failed run on the same
  machine.

**resume\_from** `wandb.sdk.lib.run_moment.RunMoment | None`

Specifies a point in a previous execution of a run to resume from.

The point is defined by the run ID, a metric, and its value.
Currently, only the metric '\_step' is supported.

**root\_dir** `str`

The root directory to use as the base for all run-related paths.

In particular, this is used to derive the wandb directory and the run directory.

**run\_group** `str | None`

Group identifier for related runs.

Used for grouping runs in the UI.

**run\_id** `str | None`

The ID of the run.

**run\_job\_type** `str | None`

Type of job being run (e.g., training, evaluation).

**run\_name** `str | None`

Human-readable name for the run.

**run\_notes** `str | None`

Additional notes or description for the run.

**run\_tags** `tuple[str, ...] | None`

Tags to associate with the run for organization and filtering.

**sagemaker\_disable** `bool`

Flag to disable SageMaker-specific functionality.

**save\_code** `bool | None`

Whether to save the code associated with the run.

**settings\_system** `str | None`

Path to the system-wide settings file.

**stop\_fn** `collections.abc.Callable[[], None] | None`

A callback to execute to stop the run.

A run can be stopped through the web UI, or after a fatal error
(if configured via a setting).

By default, to stop a run, W\&B sends a SIGINT to the main thread.
Set this callback to override this behavior, like to use a different
signal or to take some other action before interrupting.

The callback runs in a separate thread. It runs soon after a stop is
requested, but not immediately.

**max\_end\_of\_run\_history\_metrics** `int`

Maximum number of history sparklines to display at the end of a run.

**max\_end\_of\_run\_summary\_metrics** `int`

Maximum number of summary metrics to display at the end of a run.

**show\_errors** `bool`

Whether to display error messages.

**show\_info** `bool`

Whether to display informational messages.

**show\_warnings** `bool`

Whether to display warning messages.

**silent** `bool`

Flag to suppress all output.

**stop\_on\_fatal\_error** `bool`

Whether to stop the run after a fatal error.

After W\&B hits an unrecoverable error while uploading data, it prints
a message and stops uploading, but still allows logging more data.
This is usually desirable: your training metrics get stored on disk
and can be recovered using `wandb sync`, even if they aren't uploaded.

This is not useful if your files get deleted after training.
In that case, setting this to True will stop the run after a fatal error,
as if the stop button was pressed in the web UI.

**strict** `bool | None`

Whether to enable strict mode for validation and error checking.

**summary\_timeout** `int`

Time in seconds to wait for summary operations before timing out.

**sweep\_id** `str | None`

Identifier of the sweep this run belongs to.

**sweep\_param\_path** `str | None`

Path to the sweep parameters configuration.

**symlink** `bool`

Whether to use symlinks (True by default except on Windows).

**sync\_tensorboard** `bool | None`

Whether to synchronize TensorBoard logs with W\&B.

**table\_raise\_on\_max\_row\_limit\_exceeded** `bool`

Whether to raise an exception when table row limits are exceeded.

**use\_dot\_wandb** `bool | None`

Whether to use a hidden `.wandb` or visible `wandb` directory for run data.

If True, the SDK uses `.wandb`. If False, `wandb`.
If not set, defaults to `.wandb` if it already exists, otherwise `wandb`.

**username** `str | None`

Username.

**x\_disable\_meta** `bool`

Flag to disable the collection of system metadata.

**x\_disable\_stats** `bool`

Flag to disable the collection of system metrics.

**x\_extra\_http\_headers** `dict[str, str] | None`

Additional headers to add to all outgoing HTTP requests.

**x\_label** `str | None`

Label to assign to system metrics and console logs collected for the run.

This is used to group data by on the frontend and can be used to distinguish data
from different processes in a distributed training job.

**x\_primary** `bool`

Determines whether to save internal wandb files and metadata.

In a distributed setting, this is useful for avoiding file overwrites
from secondary processes when only system metrics and logs are needed,
as the primary process handles the main logging.

**x\_save\_requirements** `bool`

Flag to save the requirements file.

**x\_server\_side\_derived\_summary** `bool`

Flag to delegate automatic computation of summary from history to the server.

This does not disable user-provided summary updates.

**x\_service\_wait** `float`

Time in seconds to wait for the wandb-core internal service to start.

**x\_skip\_transaction\_log** `bool`

Whether to skip saving the run events to the transaction log.

This is only relevant for online runs. Can be used to reduce the amount of
data written to disk.

Should be used with caution, as it removes the gurantees about
recoverability.

**x\_stats\_sampling\_interval** `float`

Sampling interval for the system monitor in seconds.

**x\_stats\_open\_metrics\_endpoints** `dict[str, str] | None`

OpenMetrics `/metrics` endpoints to monitor for system metrics.

**x\_stats\_open\_metrics\_filters** `dict[str, dict[str, str]] | collections.abc.Sequence[str] | None`

Filter to apply to metrics collected from OpenMetrics `/metrics` endpoints.

Supports two formats:

* `{"metric regex pattern, including endpoint name as prefix": {"label": "label value regex pattern"}}`
* `("metric regex pattern 1", "metric regex pattern 2", ...)`

**x\_stats\_open\_metrics\_http\_headers** `dict[str, str] | None`

HTTP headers to add to OpenMetrics requests.

**x\_stats\_disk\_paths** `collections.abc.Sequence[str] | None`

System paths to monitor for disk usage.

**x\_stats\_cpu\_count** `int | None`

System CPU count.

If set, overrides the auto-detected value in the run metadata.

**x\_stats\_cpu\_logical\_count** `int | None`

Logical CPU count.

If set, overrides the auto-detected value in the run metadata.

**x\_stats\_gpu\_count** `int | None`

GPU device count.

If set, overrides the auto-detected value in the run metadata.

**x\_stats\_gpu\_type** `str | None`

GPU device type.

If set, overrides the auto-detected value in the run metadata.

**x\_stats\_gpu\_device\_ids** `collections.abc.Sequence[int] | None`

GPU device indices to monitor.

If not set, the system monitor captures metrics for all GPUs.
Assumes 0-based indexing matching CUDA/ROCm device enumeration.

**x\_stats\_track\_process\_tree** `bool`

Monitor the entire process tree for resource usage, starting from `x_stats_pid`.

When `True`, the system monitor aggregates the RSS, CPU%, and thread count
from the process with PID `x_stats_pid` and all of its descendants.
This can have a performance overhead and is disabled by default.

**x\_stats\_no\_cgroup** `bool`

Disable cgroup v2 CPU and memory limits for system metric percentages.

**x\_stats\_self\_usage** `bool`

Report the CPU and memory used by W\&B's own processes.

Adds the `wandb.cpu` and `wandb.memory.rssMB` system metrics. On by default
in development and release-candidate versions, off in releases.

**x\_sync\_dir\_suffix** `str`

Suffix to add to the run's directory name (sync\_dir).

This is set in wandb.init() to avoid naming conflicts.
If set, it is joined to the default name with a dash.

**x\_update\_finish\_state** `bool`

Flag to indicate whether this process can update the run's final state on the server.

Set to False in distributed training when only the main process should determine the final state.

## Properties

**app\_url** `str`

The URL for the W\&B UI, usually [https://forge.coreweave.com/wandb](https://forge.coreweave.com/wandb).

This is different from `base_url` (like `https://api.forge.coreweave.com`)
which is used to access W\&B APIs programmatically.

**colab\_url** `str | None`

The URL to the Colab notebook, if running in Colab.

**deployment** `Literal['local', 'cloud']`

No description provided.

**files\_dir** `str`

Absolute path to the local directory where the run's files are stored.

**is\_local** `bool`

No description provided.

**log\_dir** `str`

The directory for storing log files.

**log\_internal** `str`

The path to the file to use for internal logs.

**log\_symlink\_internal** `str`

The path to the symlink to the internal log file of the most recent run.

**log\_symlink\_user** `str`

The path to the symlink to the user-process log file of the most recent run.

**log\_user** `str`

The path to the file to use for user-process logs.

**project\_url** `str`

The W\&B URL where the project can be viewed.

**resume\_fname** `str`

The path to the resume file.

**run\_mode** `Literal['run', 'offline-run']`

The mode of the run. Can be either "run" or "offline-run".

**run\_url** `str`

The W\&B URL where the run can be viewed.

**settings\_workspace** `str`

The path to the workspace settings file.

**sweep\_url** `str`

The W\&B URL where the sweep can be viewed.

**sync\_dir** `str`

The directory for storing the run's files.

**sync\_file** `str`

Path to the append-only binary transaction log file.

**sync\_symlink\_latest** `str`

Path to the symlink to the most recent run's transaction log file.

**timespec** `str`

The time specification for the run.

**wandb\_dir** `str`

Full path to the wandb directory.

## Methods

### method Settings.validate\_anonymous()

```python theme={"system"}
value: 'object'
```

##### Arguments

**value** `object`

No description provided.

### method Settings.validate\_x\_extra\_http\_headers()

```python theme={"system"}
(value)
```

##### Arguments

**value** `_empty`

No description provided.

### method Settings.validate\_x\_stats\_coreweave\_metadata\_base\_url()

```python theme={"system"}
(value)
```

##### Arguments

**value** `_empty`

No description provided.
