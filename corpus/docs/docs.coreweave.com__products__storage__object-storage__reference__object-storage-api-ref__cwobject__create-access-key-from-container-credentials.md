# Create access key from container credentials

Source: https://docs.coreweave.com/products/storage/object-storage/reference/object-storage-api-ref/cwobject/create-access-key-from-container-credentials

# Create access key from container credentials

> Mint short-lived credentials for in-cluster workloads using the AWS container-credentials provider shape.

### **gRPC method:** `CreateAccessKeyFromContainerCreds`

> [!NOTE]
>
> * The API server is `https://api.coreweave.com`.
> * This endpoint uses the **`ContainerCredentialsAuth`**
>   scheme: send a raw JWT/OIDC token as the
>   `Authorization` header value, with **no** `Bearer`
>   prefix. This shape matches the
>   [AWS container-credentials provider](https://docs.aws.amazon.com/sdkref/latest/guide/feature-container-credentials.html)
>   for in-cluster workloads.

Returns a short-lived CoreWeave AI Object Storage access
key for an in-cluster workload, authenticated by the
workload's own OIDC token. The response uses the
AWS-compatible PascalCase shape (`AccessKeyId`,
`SecretAccessKey`, `Token`, `Expiration`) so existing AWS
SDKs and tooling that consume the
`AWS_CONTAINER_CREDENTIALS_FULL_URI` environment variable
can adopt it without code changes.

Substitute `{orgId}` with your organization ID.

```bash title="Example request" theme={"system"}
curl -X GET https://api.coreweave.com/v1/cwobject/temporary-credentials/oidc/{orgId} \
       -H "Content-Type: application/json" \
       -H "Authorization: [OIDC-TOKEN]"
```


## OpenAPI

````yaml /openapi/storage/openapi.yaml get /v1/cwobject/temporary-credentials/oidc/{orgId}
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
  /v1/cwobject/temporary-credentials/oidc/{orgId}:
    get:
      tags:
        - CWObject
      summary: Create access key from container credentials
      description: >-
        AWS-style container-credentials provider. Returns short-lived access
        keys for in-cluster workloads using the workload's own OIDC token.
      operationId: CWObject_CreateAccessKeyFromContainerCreds
      parameters:
        - name: orgId
          in: path
          required: true
          schema:
            type: string
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/CreateAccessKeyFromContainerCredsResponse'
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Status'
      security:
        - ContainerCredentialsAuth: []
components:
  schemas:
    CreateAccessKeyFromContainerCredsResponse:
      description: >-
        AWS-compatible container-credentials response shape. The property names
        use PascalCase (`AccessKeyId`, `SecretAccessKey`, `Token`, `Expiration`)
        so existing AWS SDKs and tooling that consume
        `AWS_CONTAINER_CREDENTIALS_FULL_URI` can adopt this endpoint without
        code changes. This is intentional and differs from every other endpoint,
        which uses camelCase.
      type: object
      properties:
        AccessKeyId:
          description: The access-key ID.
          type: string
        SecretAccessKey:
          description: The secret access key. Treat as a credential.
          type: string
        Token:
          description: An optional session token. May be empty for non-session credentials.
          type: string
        Expiration:
          description: The expiration time of the credentials.
          type: string
          format: date-time
        attributes:
          description: >-
            Free-form caller-supplied attributes attached to the key (for
            example, `name`).
          type: object
          additionalProperties:
            type: string
        multiAttributes:
          description: >-
            Free-form caller-supplied multi-valued attributes attached to the
            key. Each value is an `AttributeList` (an array of strings).
          type: object
          additionalProperties:
            $ref: '#/components/schemas/AttributeList'
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
    AttributeList:
      description: >-
        A list of string values used as a single multi-valued attribute on
        `multiAttributes`.
      type: object
      properties:
        values:
          description: The list of string values for this attribute.
          type: array
          items:
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
    ContainerCredentialsAuth:
      type: apiKey
      in: header
      name: Authorization
      description: >-
        Raw JWT/OIDC token sent as the `Authorization` header value with **no**
        `Bearer` prefix. Only used by `GET
        /v1/cwobject/temporary-credentials/oidc/{orgId}` for the AWS-style
        container-credentials provider.

````
