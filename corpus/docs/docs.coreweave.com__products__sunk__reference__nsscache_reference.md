# SCIM parameter reference

Source: https://docs.coreweave.com/products/sunk/reference/nsscache_reference

# SCIM parameter reference

> Complete reference of configurable SCIM parameters for SUNK user identity management

[SUNK Standard](https://docs.coreweave.com/products/sunk.md)

This reference lists the configurable parameters that control how `nsscache` retrieves user, group, shadow, and SSH key data from a SCIM source, along with the optional LDAP parameters SUNK adds to upstream `nsscache`. Use it when tuning identity sync behavior for a SUNK cluster.

## Available parameters for SCIM

### SCIM source options

The following options configure the behavior of the SCIM source:

> [accordion] SCIM source options
>
> | Parameter | Description |
> | - | - |
> | `scim_base_url` | The base URL of the SCIM server endpoint. This is the root URL that combines with the `users` and `groups` endpoints to form complete URLs. |
> | `scim_auth_token` | The authentication token, or Bearer token, for SCIM API access. You can also provide this through the `NSSCACHE_SCIM_AUTH_TOKEN` environment variable. |
> | `scim_users_endpoint` | The SCIM endpoint path for retrieving user data. Defaults to `Users`. |
> | `scim_groups_endpoint` | The SCIM endpoint path for retrieving group data. Defaults to `Groups`. |
> | `scim_users_parameters` | Optional URL parameters to add to the `users` endpoint. Special characters (spaces, quotes, and so on) are automatically URL-encoded. Example: `groups=admin&filter=active eq true` |
> | `scim_groups_parameters` | Optional URL parameters to add to the `groups` endpoint. Special characters (spaces, quotes, and so on) are automatically URL-encoded. Example: `filter=displayName eq users or displayName eq admin` |
> | `scim_timeout` | Timeout in seconds for SCIM requests. Defaults to `60`. |
> | `scim_verify_ssl` | Specifies whether to verify SSL certificates when making SCIM requests. Defaults to `true`. Set to `false` to disable SSL verification. |
> | `scim_retry_delay` | Delay in seconds between retry attempts when SCIM requests fail. Defaults to `5`. |
> | `scim_default_shell` | Default shell to assign to users if not specified in SCIM data. Defaults to `/bin/bash`. |
> | `scim_override_home_directory` | If specified in a `[passwd]` section, sets every user's home directory to the given value. Optionally, use `%%u` to substitute the username. For example, `/mnt/home/%%u` sets user `john` to `/mnt/home/john`, while `/shared/home` sets all users to the same directory. **Changing this value changes it for the entire cluster, not per user.** |

### SCIM path configuration options

The following path configuration options let you customize how data is extracted from SCIM responses. These can be set per-map in `[passwd]`, `[group]`, `[shadow]`, and `[sshkey]` sections.

> [accordion] SCIM path configuration options
>
> | Parameter | Description |
> | - | - |
> | `scim_path_username` | Path within SCIM user/group resources to extract the username. Defaults to `userName`. |
> | `scim_path_uid` | Path within SCIM user resources to extract the user ID (UID). Defaults to `id`. |
> | `scim_path_gid` | Path within SCIM user/group resources to extract the group ID (GID). |
> | `scim_path_home_directory` | Path within SCIM user resources to extract the home directory. Defaults to `/home/username` format. |
> | `scim_path_login_shell` | Path within SCIM user resources to extract the login shell. If not specified, uses the `scim_default_shell` value. |
> | `scim_path_ssh_keys` | Path within SCIM user resources to extract the SSH public keys. Should point to an array of SSH key strings or a single SSH key string. |

### `[shadow]` map parameters for SCIM

The `shadow` map creates `shadow(5)` format entries for user data from the SCIM users endpoint. This requires only the `scim_path_username` configuration in the `[shadow]` section, because other `shadow` fields are generally not available from SCIM sources. All `shadow` entries are created in the format `username:*:::::::`, where `*` indicates that authentication is handled elsewhere (not through local password files).

The following optional configuration parameters are available for the `[shadow]` section to provide default values for `shadow` fields:

> [accordion] SCIM shadow parameters
>
> | Parameter | Description |
> | - | - |
> | `scim_shadow_default_lstchg` | Default value for the last password change field (days since January 1, 1970). Defaults to empty string. |
> | `scim_shadow_default_min` | Default value for the minimum password age field, in days. Defaults to empty string. |
> | `scim_shadow_default_max` | Default value for the maximum password age field, in days. Defaults to empty string. |
> | `scim_shadow_default_warn` | Default value for the password warning period field, in days. Defaults to empty string. |
> | `scim_shadow_default_inact` | Default value for the password inactivity period field, in days. Defaults to empty string. |
> | `scim_shadow_default_expire` | Default value for the account expiration date field (days since January 1, 1970). Defaults to empty string. |
> | `scim_shadow_default_flag` | Default value for the reserved flag field. Defaults to empty string. |

## Optional parameters for LDAP

SUNK adds optional parameters to `nsscache` for LDAP.

### Default shell

The `nsscache.nsscacheConfig.default.ldap_default_shell` parameter provides a default shell for all users. You can specify a different shell with the `loginShell` value in the user attributes configuration.

This parameter differs from the [`ldap_override_shell`](https://github.com/google/nsscache/blob/66e3789910b2641e52707bba55d6e5d381069257/nsscache.conf.5#L216), which sets a shell that overrides the user's preferences in their LDAP profile.

### Home directory override

Use the `nsscache.nsscacheConfig.default.ldap_override_home_dir` parameter for a home directory override. Use `%%u` to substitute the username in the home directory.

Use this to set a mount point for the home directories. For example, `/mnt/home/%%u`. The mount point should match the mount specified in `compute.VolumeMounts`.
