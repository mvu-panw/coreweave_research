# Set organization settings

Source: https://docs.coreweave.com/products/storage/object-storage/reference/object-storage-api-ref/cwobject/set-organization-settings

# Set organization settings

> Configure organization-wide AI Object Storage settings.

### **gRPC method:** `SetOrganizationSettings`

> [!NOTE]
>
> * The API server is `https://api.coreweave.com`.
> * Replace `{API_ACCESS_TOKEN}` with your [CoreWeave API access token](https://docs.coreweave.com/security/authn-authz/manage-api-access-tokens.md).
> * For required permissions, see [IAM Access Policies](https://docs.coreweave.com/security/iam/access-policies.md).

Configures organization-wide settings, such as default
audit logging for the control plane and for buckets.

```json title="data.json"
{
  "settings": {
    "controlPlaneAuditLoggingEnabled": true,
    "bucketAuditLoggingEnabled": true
  }
}
```

```bash title="Example request" theme={"system"}
curl -X PUT https://api.coreweave.com/v1/cwobject/organization/settings \
       -H "Content-Type: application/json" \
       -H "Authorization: Bearer {API_ACCESS_TOKEN}" \
       -d @data.json
```


## OpenAPI

````yaml /openapi/storage/openapi.yaml put /v1/cwobject/organization/settings
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
  /v1/cwobject/organization/settings:
    put:
      tags:
        - CWObject
      summary: Set organization settings
      description: >-
        Configures organization-wide CoreWeave AI Object Storage settings such
        as default audit logging.
      operationId: CWObject_SetOrganizationSettings
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/SetOrganizationSettingsRequest'
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/SetOrganizationSettingsResponse'
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Status'
components:
  schemas:
    SetOrganizationSettingsRequest:
      description: Inputs for configuring organization-wide AI Object Storage settings.
      type: object
      properties:
        settings:
          $ref: '#/components/schemas/CWObjectOrganizationSettings'
          description: The new organization settings to apply.
    SetOrganizationSettingsResponse:
      description: The organization settings after the update is applied.
      type: object
      properties:
        settings:
          $ref: '#/components/schemas/CWObjectOrganizationSettings'
          description: The organization settings now in effect.
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
    CWObjectOrganizationSettings:
      description: Organization-wide settings managed through the AI Object Storage API.
      type: object
      properties:
        controlPlaneAuditLoggingEnabled:
          description: When `true`, audit logging is enabled for control-plane operations.
          type: boolean
        bucketAuditLoggingEnabled:
          description: >-
            When `true`, audit logging is enabled by default for every bucket in
            the organization.
          type: boolean
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
