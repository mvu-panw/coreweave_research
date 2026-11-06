# coreweave_container_registry_zones (Data source)

Source: https://docs.coreweave.com/platform/terraform/data-sources/container_registry_zones

# coreweave_container_registry_zones (Data source)

Lists Container Registry zones, sorted by zone name. Zone availability is advisory and does not reserve capacity.

## Example usage

```terraform theme={"system"}
data "coreweave_container_registry_zones" "available" {
  zone_names = ["US-LAB-01A"]
}
```

## Schema

### Optional

* `timeouts` (Attributes) (see [below for nested schema](#nestedatt--timeouts))
* `zone_names` (Set of String) At most 100 zone filters. Null or empty selects all. Case-equivalent duplicates are rejected.

### Read-Only

* `zones` (Attributes List) Matching zones, sorted by zone name. Availability is advisory. (see [below for nested schema](#nestedatt--zones))

### Nested Schema for `timeouts`

Optional:

* `read` (String) A string that can be [parsed as a duration](https://pkg.go.dev/time#ParseDuration) consisting of numbers and unit suffixes, such as "30s" or "2h45m". Valid time units are "s" (seconds), "m" (minutes), "h" (hours).

### Nested Schema for `zones`

Read-Only:

* `available` (Boolean) Whether new namespaces can currently be provisioned in this zone.
* `zone` (String) Upper-case zone identifier.
