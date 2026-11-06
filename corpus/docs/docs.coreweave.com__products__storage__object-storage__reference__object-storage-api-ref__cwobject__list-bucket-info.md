# List bucket info

Source: https://docs.coreweave.com/products/storage/object-storage/reference/object-storage-api-ref/cwobject/list-bucket-info

# List bucket info

> List inventory and usage for every bucket in the organization.

### **gRPC method:** `ListBucketInfo`

> [!NOTE]
>
> * The API server is `https://api.coreweave.com`.
> * Replace `{API_ACCESS_TOKEN}` with your [CoreWeave API access token](https://docs.coreweave.com/security/authn-authz/manage-api-access-tokens.md).
> * For required permissions, see [IAM Access Policies](https://docs.coreweave.com/security/iam/access-policies.md).

Returns inventory and usage information for every bucket
in the caller's organization, including fields that are not
available through the S3-compatible API. Use `offset` and
`limit` (1-1000) for pagination.

```bash title="Example request" theme={"system"}
curl -X GET https://api.coreweave.com/v1/cwobject/bucket-info \
       -H "Content-Type: application/json" \
       -H "Authorization: Bearer {API_ACCESS_TOKEN}"
```


## OpenAPI

````yaml /openapi/storage/openapi.yaml get /v1/cwobject/bucket-info
openapi: 3.0.3
info:
  title: CoreWeave AI Object Storage API
  version: 0.0.1
  description: >-
    Manage organization-wide access policies, configure bucket and organization
    settings, mint and revoke access keys, and inspect bucket and access-key
    inventory.
servers:
  - url: https://api.coreweave.com
    description: CoreWeave production API.
security:
  - TokenAuth: []
tags:
  - name: CWObject
    description: >-
      Endpoints that interact with CoreWeave AI Object Storage outside the
      S3-compatible API.
paths:
  /v1/cwobject/bucket-info:
    get:
      tags:
        - CWObject
      summary: List bucket info
      description: >-
        Lists information about every bucket in the caller's organization,
        including details unavailable through the S3-compatible API.
      operationId: CWObject_ListBucketInfo
      parameters:
        - name: offset
          in: query
          description: >-
            Zero-based offset into the result set. Used with `limit` for
            pagination.
          schema:
            type: integer
            format: uint32
        - name: limit
          in: query
          description: Page size. Must be `1-1000`.
          schema:
            type: integer
            format: uint32
            maximum: 1000
            minimum: 1
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ListBucketInfoResponse'
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Status'
components:
  schemas:
    ListBucketInfoResponse:
      description: >-
        A page of bucket inventory and usage records for the caller's
        organization.
      type: object
      properties:
        info:
          description: The list of bucket metadata records.
          type: array
          items:
            $ref: '#/components/schemas/BucketInfo'
    Status:
      description: >-
        The `Status` type defines a logical error model that is suitable for
        different programming environments, including REST APIs and RPC APIs. It
        is used by [gRPC](https://github.com/grpc). Each `Status` message
        contains three pieces of data: error code, error message, and error
        details. You can find out more about this error model and how to work
        with it in the [API Design
        Guide](https://cloud.google.com/apis/design/errors).
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
    BucketInfo:
      description: Inventory and usage information for a single bucket.
      type: object
      properties:
        orgId:
          description: The organization ID that owns the bucket.
          type: string
        name:
          description: The bucket name.
          type: string
        creationTime:
          description: The time the bucket was created.
          type: string
          format: date-time
        settings:
          $ref: '#/components/schemas/CWObjectBucketSettings'
          description: Bucket settings managed through this API (audit logging, and so on).
        location:
          description: >-
            The [Availability
            Zone](https://docs.coreweave.com/platform/regions/about-regions-and-azs#complete-region-list)
            that hosts the bucket (for example, `US-EAST-04A`).
          type: string
        usage:
          description: An array of usage measurements for the bucket.
          type: array
          items:
            $ref: '#/components/schemas/BucketUsageInfo'
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
    CWObjectBucketSettings:
      description: Per-bucket settings managed through the AI Object Storage API.
      type: object
      properties:
        auditLoggingEnabled:
          description: When `true`, audit logging is enabled for the bucket.
          type: boolean
        archiveEnabled:
          description: |-
            When true, idle STANDARD objects are archived to STANDARD_IA after
             archive_after_last_access_days without access. Org must be entitled to
             configure this setting.
          type: boolean
        archiveAfterLastAccessDays:
          description: >-
            Days since last access (or creation if never accessed) before a
            STANDARD
             object version is archived to STANDARD_IA. Required when archive_enabled
             is true. Ignored when archive_enabled is false.
          type: integer
          format: int32
        capacityCapBytes:
          description: >-
            Sets or replaces the capacity cap in bytes. Zero is a valid cap.
            Values
             greater than 9,223,372,036,854,775,807 bytes are rejected. The caller's
             organization must be entitled.
          type: string
        configuredCapacityCapBytes:
          description: >-
            Read-only: the capacity cap currently configured on the bucket,
            populated
             on GetBucketInfo / ListBucketInfo / SetBucketSettings responses. Unset
             means no cap is configured. Ignored on SetBucketSettings requests; use
             capacity_cap_update to modify the cap.
          type: string
    BucketUsageInfo:
      description: A single usage measurement for a bucket.
      type: object
      properties:
        measurementType:
          description: >-
            The kind of measurement reported by `value` (for example,
            `MEASUREMENT_TYPE_USAGE_BYTES`).
          type: string
        value:
          description: >-
            The measurement value, encoded as a string for unsigned 64-bit
            safety across JSON consumers.
          type: string
        valueHumanReadable:
          description: A human-readable formatting of `value` (for example, `1.2 GiB`).
          type: string
  securitySchemes:
    TokenAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
      description: >-
        CoreWeave API access token sent as a bearer token in the `Authorization`
        header (the value is prefixed with `Bearer`). Used by every operation
        except the SAML/OIDC POST token-exchange endpoints (anonymous) and the
        OIDC container credentials GET (which uses `ContainerCredentialsAuth`).
      x-default: Bearer {API_ACCESS_TOKEN}

````
