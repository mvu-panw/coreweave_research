# Create access key from OIDC

Source: https://docs.coreweave.com/products/storage/object-storage/reference/object-storage-api-ref/cwobject/create-access-key-from-oidc

# Create access key from OIDC

> Exchange an OIDC token for a temporary access key (anonymous on the CoreWeave side).

### **gRPC method:** `CreateAccessKeyFromOIDC`

> [!NOTE]
>
> * The API server is `https://api.coreweave.com`.
> * This endpoint is **anonymous on the CoreWeave side**,
>   authentication comes from the OIDC token in the
>   request body, not a `Bearer` token in the header.

Exchanges an OIDC token from a configured
[Workload Identity Federation](https://docs.coreweave.com/products/storage/object-storage/auth-access/workload-identity-federation/oidc-workload-federation)
provider for a temporary CoreWeave AI Object Storage
access key. The lifespan is set by `durationSeconds` and
must be `0-43200` seconds (12 hours maximum).

```json title="data.json"
{
  "durationSeconds": 300,
  "orgId": "abc123",
  "oidcToken": "[OIDC-TOKEN]",
  "attributes": {
    "name": "test-key"
  }
}
```

```bash title="Example request" theme={"system"}
curl -X POST https://api.coreweave.com/v1/cwobject/temporary-credentials/oidc \
       -H "Content-Type: application/json" \
       -d @data.json
```


## OpenAPI

````yaml /openapi/storage/openapi.yaml post /v1/cwobject/temporary-credentials/oidc
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
  /v1/cwobject/temporary-credentials/oidc:
    post:
      tags:
        - CWObject
      summary: Create access key from OIDC
      description: >-
        Exchanges an OIDC token from a configured Workload Identity Federation
        provider for a time-limited CoreWeave AI Object Storage access key. No
        CoreWeave bearer token is required.
      operationId: CWObject_CreateAccessKeyFromOIDC
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateAccessKeyFromOIDCRequest'
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/CreateAccessKeyFromOIDCResponse'
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Status'
      security: []
components:
  schemas:
    CreateAccessKeyFromOIDCRequest:
      description: >-
        Inputs for exchanging an OIDC token for a CoreWeave AI Object Storage
        access key.
      type: object
      properties:
        durationSeconds:
          description: >-
            Lifespan of the resulting access key in seconds. Must be `0-43200`
            (12 hours maximum).
          type: integer
          format: uint32
          maximum: 43200
          minimum: 0
        orgId:
          description: The CoreWeave organization ID to mint the access key for.
          type: string
        oidcToken:
          description: >-
            The OIDC token from the configured Workload Identity Federation
            provider.
          type: string
        attributes:
          description: >-
            Free-form caller-supplied attributes attached to the key (for
            example, `name`).
          type: object
          additionalProperties:
            type: string
      required:
        - durationSeconds
        - orgId
        - oidcToken
    CreateAccessKeyFromOIDCResponse:
      description: >-
        The newly-minted access key. The `secretKey` is the only opportunity to
        read the secret value.
      type: object
      properties:
        accessKeyId:
          description: The access-key ID.
          type: string
        secretKey:
          description: >-
            The secret access key. Treat as a credential and store it securely
            on receipt.
          type: string
        principalName:
          description: The fully-qualified principal name that owns the access key.
          type: string
        expiry:
          description: The expiration time of the access key.
          type: string
          format: date-time
        attributes:
          description: The attributes that were attached to the key on creation.
          type: object
          additionalProperties:
            type: string
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
