# Update VPC

Source: https://docs.coreweave.com/products/networking/vpc/vpc-api/vpcservice/update-vpc

# Update VPC

> Update selected fields on a CoreWeave VPC using a field mask.

> [!NOTE]
>
> * The API server is `https://api.coreweave.com`.
> * Replace `{API_ACCESS_TOKEN}` with your [CoreWeave API access token](https://docs.coreweave.com/security/authn-authz/manage-api-access-tokens.md).
> * For required permissions, see [IAM Access Policies](https://docs.coreweave.com/security/iam/access-policies.md).

This method uses a field mask, provided in the `updateMask`
field, to specify which fields to modify.
Requests with an omitted or empty `updateMask` are supported only
for backward compatibility. For new code, always provide an explicit
`updateMask`. Without one, update behavior varies by field and can
clear values that you don't resend.
For general guidance on update masks, see
[Google AIP-134](https://google.aip.dev/134#request-message).

The valid `updateMask` field paths are:

* `vpcPrefixes`
* `hostPrefixes`
* `ingress.disablePublicServices`
* `egress.disablePublicAccess`
* `dhcp.dns.servers`
* `dhcp.dns.searchDomains`

Any other path, including a top-level path like `ingress`
or `dhcp`, is invalid. The server returns an error
and makes no changes.

When `vpcPrefixes`, `dhcp.dns.servers`, or `dhcp.dns.searchDomains`
is included in `updateMask`, the supplied list replaces the stored one.
An empty list clears that field.

To clear search domains, include `dhcp.dns.searchDomains` in
`updateMask` and supply an empty list. With an omitted or empty mask,
an empty search-domain list preserves existing search domains.

The `hostPrefixes` field is append-only. Include all existing entries
unchanged and in their original order, followed by any new entries.

```bash title="Example request" theme={"system"}
curl -X PATCH https://api.coreweave.com/v1beta1/networking/vpcs/{id} \
       -H "Content-Type: application/json" \
       -H "Authorization: Bearer {API_ACCESS_TOKEN}" \
       -d @data.json
```


## OpenAPI

````yaml /openapi/vpc/openapi.yaml patch /v1beta1/networking/vpcs/{id}
openapi: 3.0.3
info:
  title: CoreWeave VPC API
  version: 0.0.1
  description: >-
    The VPC API lets you create, list, update, and delete CoreWeave Virtual
    Private Clouds (VPCs).
servers:
  - url: https://api.coreweave.com
    description: CoreWeave production API.
security:
  - bearerAuth: []
tags:
  - name: VPCService
    description: Endpoints for creating, listing, updating, and deleting CoreWeave VPCs.
    x-group: VPCService
paths:
  /v1beta1/networking/vpcs/{id}:
    patch:
      tags:
        - VPCService
      summary: Update VPC
      description: Updates a VPC by ID. Use `updateMask` to target specific fields.
      operationId: VPCService_UpdateVPC
      parameters:
        - name: id
          in: path
          description: The unique identifier for the VPC.
          required: true
          schema:
            type: string
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/UpdateVPCRequest'
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UpdateVPCResponse'
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Status'
components:
  schemas:
    UpdateVPCRequest:
      type: object
      properties:
        updateMask:
          description: >-
            A field mask specifying which fields to update. The valid field
            paths are:


            - `vpcPrefixes`

            - `hostPrefixes`

            - `ingress.disablePublicServices`

            - `egress.disablePublicAccess`

            - `dhcp.dns.servers`

            - `dhcp.dns.searchDomains`


            The server rejects any other path with an `INVALID_ARGUMENT` error.


            Requests with an omitted or empty `updateMask` are supported only

            for backward compatibility. For new code, always provide an explicit

            `updateMask`. Without one, update behavior varies by field and can

            clear values that you don't resend.


            To clear search domains, include `dhcp.dns.searchDomains` in

            `updateMask` and supply an empty list. With an omitted or empty
            mask,

            an empty search-domain list preserves existing search domains.


            For general guidance on update masks, see

            [Google AIP-134](https://google.aip.dev/134#request-message).
          type: string
          format: field-mask
        id:
          description: The unique identifier for the VPC.
          type: string
        vpcPrefixes:
          description: >-
            An array of additional prefixes associated with the VPC. Must be
            given in CIDR notation.
          type: array
          items:
            $ref: '#/components/schemas/Prefix'
        ingress:
          description: The ingress configuration of the VPC.
          allOf:
            - $ref: '#/components/schemas/Ingress'
        egress:
          description: The egress configuration of the VPC.
          allOf:
            - $ref: '#/components/schemas/Egress'
        dhcp:
          description: The DHCP configuration of the VPC.
          allOf:
            - $ref: '#/components/schemas/DHCP'
        hostPrefixes:
          description: >-
            Complete desired list of host prefixes. Every existing element must
            be
             included unchanged and in its original position, followed by any new elements.
             New elements follow the same validation as CreateVPC.
             Existing elements cannot be removed or modified, including their CIDR lists.
             Existing elements cannot be reordered; new elements must be appended.
          type: array
          items:
            $ref: '#/components/schemas/HostPrefix'
      required:
        - id
    UpdateVPCResponse:
      type: object
      properties:
        vpc:
          description: The VPC.
          allOf:
            - $ref: '#/components/schemas/VPC'
          readOnly: true
    Status:
      description: >-
        Standard error response. `code` is a
        [`google.rpc.Code`](https://cloud.google.com/apis/design/errors#error_codes);
        `message` is human-readable English; `details` carries machine-readable
        error details when present.
      type: object
      properties:
        code:
          description: >-
            The status code, which should be an enum value of
            [google.rpc.Code][google.rpc.Code].
          type: integer
          format: int32
        message:
          description: >-
            A developer-facing error message, which should be in English. Any
            user-facing error message should be localized and sent in the
            [google.rpc.Status.details][google.rpc.Status.details] field, or
            localized by the client.
          type: string
        details:
          description: >-
            A list of messages that carry the error details.  There is a common
            set of message types for APIs to use.
          type: array
          items:
            $ref: '#/components/schemas/GoogleProtobufAny'
    Prefix:
      description: >-
        An IP prefix associated with a VPC. The `status` field reflects the
        lifecycle: `STATUS_PENDING_ALLOCATION` → `STATUS_AVAILABLE` →
        `STATUS_ALLOCATED`.
      type: object
      properties:
        name:
          description: >-
            The user-specified name of the VPC Prefix. Must not be longer than
            30 characters.
          type: string
        value:
          description: The value of the prefix in IPv4 or IPv6 CIDR notation.
          type: string
        createdAt:
          description: The time the prefix was created.
          type: string
          format: date-time
          readOnly: true
        updatedAt:
          description: The time the prefix was last updated.
          type: string
          format: date-time
          readOnly: true
        status:
          description: >-
            The current status of the prefix. The lifecycle is
            `STATUS_PENDING_ALLOCATION` → `STATUS_AVAILABLE` →
            `STATUS_ALLOCATED`. `STATUS_UNSPECIFIED` means the status has not
            been set.
          type: string
          format: enum
          example: STATUS_AVAILABLE
          enum:
            - STATUS_UNSPECIFIED
            - STATUS_AVAILABLE
            - STATUS_PENDING_ALLOCATION
            - STATUS_ALLOCATED
          readOnly: true
        type:
          description: >-
            The intended use for the prefix. Values are `PRIVATE_ACCESS`, `POD`,
            `SERVICE`, and `LOAD_BALANCER`; omit the field rather than sending
            the zero value `UNSPECIFIED`. On create, specifying this field
            assigns the type; omitting it creates the prefix without a type. For
            an existing prefix, this field is immutable.
          type: string
          format: enum
          example: POD
          enum:
            - UNSPECIFIED
            - PRIVATE_ACCESS
            - POD
            - SERVICE
            - LOAD_BALANCER
      required:
        - name
        - value
    Ingress:
      type: object
      properties:
        disablePublicServices:
          description: >-
            Disables ingress from the Internet at the VPC level when set to
            `true`. Defaults to `false`, so ingress from the Internet is enabled
            unless you change this field.
          type: boolean
    Egress:
      type: object
      properties:
        disablePublicAccess:
          description: >-
            Disables egress from the Internet at the VPC level when set to
            `true`. Defaults to `false`, so egress from the Internet is enabled
            unless you change this field.
          type: boolean
    DHCP:
      description: DHCP configuration for the VPC.
      type: object
      properties:
        dns:
          description: The DNS configuration for DHCP within the VPC.
          allOf:
            - $ref: '#/components/schemas/DHCP_DNS'
    HostPrefix:
      description: >-
        A Host Prefix describes an IP range from which host-specific prefixes
        are allocated for Nodes in a VPC. Host prefixes of any type cannot be
        changed after the VPC is created. The `type` field's values are
        `PRIMARY`, `ROUTED`, and `ATTACHED`. See the Create VPC operation for
        the full taxonomy.
      type: object
      properties:
        name:
          description: The user-specified name of the Host Prefix.
          type: string
        type:
          description: >-
            The host prefix's type, which controls network connectivity from the
            prefix to the host. Must be uppercase. Values are `PRIMARY`,
            `ROUTED`, and `ATTACHED`; omit the field rather than sending the
            zero value `UNSPECIFIED`. See the Create VPC operation for the full
            taxonomy.
          type: string
          format: enum
          example: PRIMARY
          enum:
            - UNSPECIFIED
            - PRIMARY
            - ROUTED
            - ATTACHED
        prefixes:
          description: >-
            The VPC-wide aggregates from which host-specific prefixes are
            allocated. May be IPv4 or IPv6.
          type: array
          items:
            type: string
        ipam:
          description: >-
            The IP address management (IPAM) configuration for a secondary host
            prefix. Must not be set for a `PRIMARY` prefix.
          allOf:
            - $ref: '#/components/schemas/IPAddressManagementPolicy'
      required:
        - name
        - type
        - prefixes
    VPC:
      description: >-
        A CoreWeave Virtual Private Cloud. The `status` field reflects the
        lifecycle: `STATUS_CREATING` → `STATUS_READY`, with `STATUS_UPDATING`
        during in-place edits and `STATUS_DELETING` during teardown.
      type: object
      properties:
        id:
          description: The unique identifier for the VPC.
          type: string
          readOnly: true
        name:
          description: The name of the VPC. Must not be longer than 30 characters.
          type: string
        status:
          description: >-
            The current status of the VPC. The lifecycle is `STATUS_CREATING` →
            `STATUS_READY`, with `STATUS_UPDATING` during in-place edits and
            `STATUS_DELETING` during teardown. `STATUS_UNSPECIFIED` means the
            status has not been set.
          type: string
          format: enum
          example: STATUS_READY
          enum:
            - STATUS_UNSPECIFIED
            - STATUS_CREATING
            - STATUS_UPDATING
            - STATUS_READY
            - STATUS_DELETING
          readOnly: true
        zone:
          description: >-
            The [Availability
            Zone](https://docs.coreweave.com/platform/regions/about-regions-and-azs#complete-region-list)
            in which the VPC is located.
          type: string
        vpcPrefixes:
          description: An array of the VPC prefixes. Must be given in CIDR notation.
          type: array
          items:
            $ref: '#/components/schemas/Prefix'
        createdAt:
          description: The time the VPC was created.
          type: string
          format: date-time
          readOnly: true
        updatedAt:
          description: The time the VPC was last updated.
          type: string
          format: date-time
          readOnly: true
        hostPrefix:
          description: |-
            A single IPv4 CIDR range from which host addresses are allocated
            for compute in this VPC. Must meet the Availability Zone's
            minimum mask size (typically `/18` or larger). Immutable once
            set.

            **Deprecated:** use `hostPrefixes` instead. Present only on VPCs
            created with this legacy field; mutually exclusive with
            `hostPrefixes`.
          type: string
          deprecated: true
        hostPrefixes:
          description: >-
            The Host Prefixes of the VPC. If configured, each IPv4 prefix must
            meet the Availability Zone's minimum mask size (typically `/18` or
            larger), and each IPv6 prefix must be `/51` or larger. You can
            append new entries after creation. Existing entries can't be
            modified, removed, or reordered.
          type: array
          items:
            $ref: '#/components/schemas/HostPrefix'
        ingress:
          description: The ingress configuration of the VPC.
          allOf:
            - $ref: '#/components/schemas/Ingress'
        egress:
          description: The egress configuration of the VPC.
          allOf:
            - $ref: '#/components/schemas/Egress'
        dhcp:
          description: The DHCP configuration of the VPC.
          allOf:
            - $ref: '#/components/schemas/DHCP'
      required:
        - name
        - zone
    GoogleProtobufAny:
      description: >-
        Contains an arbitrary serialized message along with a @type that
        describes the type of the serialized message.
      type: object
      properties:
        '@type':
          description: The type of the serialized message.
          type: string
      additionalProperties: true
    DHCP_DNS:
      description: Settings affecting DNS for DHCP within the VPC
      type: object
      properties:
        servers:
          description: An array of user-provided DNS servers.
          type: array
          items:
            type: string
        searchDomains:
          description: >-
            An array of DNS search domains advertised to DHCP clients in the
            VPC.
          type: array
          items:
            type: string
    IPAddressManagementPolicy:
      description: >-
        IP address management (IPAM) configuration for a secondary host prefix.
        The `gatewayAddressPolicy` field's values are `EUI64`, `FIRST_IP`, and
        `LAST_IP`. See the Create VPC operation for the full taxonomy.
      type: object
      properties:
        prefixLength:
          description: >-
            The desired length for each Node's allocation from the VPC-wide
            aggregate prefix.
          type: integer
          format: int32
        gatewayAddressPolicy:
          description: >-
            Describes which IP address from the prefix is allocated to the
            network gateway. Optional, and only valid when the parent Host
            Prefix's `type` is `ATTACHED`. Must be uppercase. Values are
            `EUI64`, `FIRST_IP`, and `LAST_IP`; omit the field rather than
            sending the zero value `UNSPECIFIED`. See the Create VPC operation
            for the full taxonomy.
          type: string
          format: enum
          example: FIRST_IP
          enum:
            - UNSPECIFIED
            - EUI64
            - FIRST_IP
            - LAST_IP
      required:
        - prefixLength
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
      description: CoreWeave API access token sent as a bearer token.
      x-default: Bearer {API_ACCESS_TOKEN}

````
