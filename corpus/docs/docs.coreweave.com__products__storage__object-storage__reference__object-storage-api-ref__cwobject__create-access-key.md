# Create access key

Source: https://docs.coreweave.com/products/storage/object-storage/reference/object-storage-api-ref/cwobject/create-access-key

# Create access key

> Create a permanent or time-limited access key from a CoreWeave Cloud token.

### **gRPC method:** `CreateAccessKeyFromJWT`

> [!NOTE]
>
> * The API server is `https://api.coreweave.com`.
> * Replace `{API_ACCESS_TOKEN}` with your [CoreWeave API access token](https://docs.coreweave.com/security/authn-authz/manage-api-access-tokens.md).
> * For required permissions, see [IAM Access Policies](https://docs.coreweave.com/security/iam/access-policies.md).

[Generate an access key](https://docs.coreweave.com/products/storage/object-storage/auth-access/manage-access-keys/about.md)
using a CoreWeave Cloud token. The key can be permanent or
time-limited depending on the value of `durationSeconds`.

* Set `durationSeconds` to `0` to create a **permanent** key.
* Set `durationSeconds` to a positive integer to create a
  **temporary** key with that lifespan in seconds.

```json title="data.json (permanent)"
{
  "durationSeconds": 0,
  "attributes": {
    "name": "permanent-key"
  }
}
```

```json title="data.json (temporary)"
{
  "durationSeconds": 300,
  "attributes": {
    "name": "temporary-key"
  }
}
```

```bash title="Example request" theme={"system"}
curl -X POST https://api.coreweave.com/v1/cwobject/access-key \
       -H "Content-Type: application/json" \
       -H "Authorization: Bearer {API_ACCESS_TOKEN}" \
       -d @data.json
```


## OpenAPI

````yaml /openapi/storage/openapi.yaml post /v1/cwobject/access-key
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
  /v1/cwobject/access-key:
    post:
      tags:
        - CWObject
      summary: Create access key
      description: >-
        Creates a CoreWeave AI Object Storage access key, exchanging a CoreWeave
        API access token (Cloud token) for object-storage credentials.
      operationId: CWObject_CreateAccessKeyFromJWT
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateAccessKeyFromJWTRequest'
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/CreateAccessKeyFromJWTResponse'
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Status'
components:
  schemas:
    CreateAccessKeyFromJWTRequest:
      description: Inputs for creating an access key from a CoreWeave Cloud token.
      type: object
      properties:
        durationSeconds:
          description: >-
            Lifespan of the resulting access key in seconds. Set to `0` to
            create a permanent key; set to a positive integer to create a
            temporary key with that lifespan. Required.
          type: integer
          format: uint32
          minimum: 0
        attributes:
          description: >-
            Free-form caller-supplied attributes attached to the key (for
            example, `name`).
          type: object
          additionalProperties:
            type: string
      required:
        - durationSeconds
    CreateAccessKeyFromJWTResponse:
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
          description: >-
            The expiration time of the access key. Permanent keys may report a
            sentinel value.
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
