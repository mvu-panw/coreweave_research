# coreweave_workload_federation_oidc_config (Data source)

Source: https://docs.coreweave.com/platform/terraform/data-sources/workload_federation_oidc_config

# coreweave_workload_federation_oidc_config (Data source)

Looks up an existing workload federation OIDC configuration by its stable UID or unique issuer URL and audience pair. The organization is determined by the provider's authenticated context.

## Example usage

```terraform theme={"system"}
# Look up a Cloud Console-created OIDC configuration by its stable ID.
data "coreweave_workload_federation_oidc_config" "github_actions" {
  id = "13db6848-17e8-42b0-8615-4d3fc86bd721"
}

# Look up a configuration by its unique trust identity. The organization is
# determined by the provider's authenticated context.
data "coreweave_workload_federation_oidc_config" "by_trust_identity" {
  issuer_url = "https://token.actions.githubusercontent.com"
  audience   = "coreweave"
}

# Pass the stable ID to a runtime workspace or module without recreating the
# organization-level bootstrap object there.
output "workload_federation_oidc_config_id" {
  value = data.coreweave_workload_federation_oidc_config.github_actions.id
}
```

## Schema

### Optional

* `audience` (String) The audience to look up. Must be configured together with `issuer_url` when `id` is omitted.
* `id` (String) The server-assigned stable ID to look up. Configure either `id`, or both `issuer_url` and `audience`.
* `issuer_url` (String) The issuer URL to look up. Must be configured together with `audience` when `id` is omitted.

### Read-Only

* `active` (Boolean) Whether tokens from this OIDC provider are accepted for workload identity federation.
* `created_at` (String) The RFC 3339 timestamp at which the OIDC configuration was created.
* `deactivated_at` (String) The RFC 3339 timestamp at which the OIDC configuration was deactivated, or null while active.
* `description` (String) The optional human-readable description of the OIDC configuration.
* `name` (String) The human-readable name of the OIDC configuration.
* `organization_id` (String) The unique identifier of the CoreWeave organization that owns the OIDC configuration.
* `updated_at` (String) The RFC 3339 timestamp at which the OIDC configuration was last updated.
