# Set bucket settings

Source: https://docs.coreweave.com/products/storage/object-storage/reference/object-storage-api-ref/cwobject/set-bucket-settings

# Set bucket settings

> Configure non-S3 bucket settings such as audit logging.

### **gRPC method:** `SetBucketSettings`

> [!NOTE]
>
> * The API server is `https://api.coreweave.com`.
> * Replace `{API_ACCESS_TOKEN}` with your [CoreWeave API access token](https://docs.coreweave.com/security/authn-authz/manage-api-access-tokens.md).
> * For required permissions, see [IAM Access Policies](https://docs.coreweave.com/security/iam/access-policies.md).

Configures bucket settings that are not exposed by the
S3-compatible API. Currently supports toggling per-bucket
audit logging via `settings.auditLoggingEnabled`.

```json title="data.json"
{
  "bucketName": "my-bucket",
  "settings": {
    "auditLoggingEnabled": true
  }
}
```

```bash title="Example request" theme={"system"}
curl -X PUT https://api.coreweave.com/v1/cwobject/bucket/settings \
       -H "Content-Type: application/json" \
       -H "Authorization: Bearer {API_ACCESS_TOKEN}" \
       -d @data.json
```


## OpenAPI

````yaml /openapi/storage/openapi.yaml put /v1/cwobject/bucket/settings
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
  /v1/cwobject/bucket/settings:
    put:
      tags:
        - CWObject
      summary: Set bucket settings
      description: Configures bucket settings that aren't exposed by the S3-compatible API.
      operationId: CWObject_SetBucketSettings
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/SetBucketSettingsRequest'
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/SetBucketSettingsResponse'
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Status'
components:
  schemas:
    SetBucketSettingsRequest:
      description: >-
        Inputs for configuring per-bucket settings managed through the AI Object
        Storage API.
      type: object
      properties:
        bucketName:
          description: The name of the bucket to configure.
          type: string
        settings:
          $ref: '#/components/schemas/CWObjectBucketSettings'
          description: The new bucket settings to apply.
    SetBucketSettingsResponse:
      description: The bucket settings after the update is applied.
      type: object
      properties:
        settings:
          $ref: '#/components/schemas/CWObjectBucketSettings'
          description: The bucket settings now in effect.
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
