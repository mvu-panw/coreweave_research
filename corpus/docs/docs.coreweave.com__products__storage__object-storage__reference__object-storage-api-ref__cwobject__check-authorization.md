# Check authorization

Source: https://docs.coreweave.com/products/storage/object-storage/reference/object-storage-api-ref/cwobject/check-authorization

# Check authorization

> Check whether the caller is allowed to perform actions on resources.

### **gRPC method:** `AuthCanI`

> [!NOTE]
>
> * The API server is `https://api.coreweave.com`.
> * Replace `{API_ACCESS_TOKEN}` with your [CoreWeave API access token](https://docs.coreweave.com/security/authn-authz/manage-api-access-tokens.md).
> * For required permissions, see [IAM Access Policies](https://docs.coreweave.com/security/iam/access-policies.md).

The endpoint returns a single `verdict` that is `true` only
if the caller is allowed to perform **all** listed actions on
**all** listed resources. Both `actions` and `resources` are
required.

```json title="data.json"
{
  "actions": ["cwobject:ListBucketInfo", "cwobject:ListAccessKeyInfo"],
  "resources": ["*"]
}
```

```bash title="Example request" theme={"system"}
curl -X POST https://api.coreweave.com/v1/cwobject/auth/can-i \
       -H "Content-Type: application/json" \
       -H "Authorization: Bearer {API_ACCESS_TOKEN}" \
       -d @data.json
```


## OpenAPI

````yaml /openapi/storage/openapi.yaml post /v1/cwobject/auth/can-i
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
  /v1/cwobject/auth/can-i:
    post:
      tags:
        - CWObject
      summary: Check authorization
      description: >-
        Checks whether the caller is allowed to perform a set of actions on a
        set of resources.
      operationId: CWObject_AuthCanI
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/AuthCanIRequest'
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/AuthCanIResponse'
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Status'
components:
  schemas:
    AuthCanIRequest:
      description: Inputs for an authorization check. Both fields are required.
      type: object
      properties:
        actions:
          description: >-
            The list of actions to check (for example,
            `cwobject:ListBucketInfo`).
          type: array
          items:
            type: string
        resources:
          description: >-
            The list of resources to check the actions against. Use `["*"]` to
            check against every resource.
          type: array
          items:
            type: string
    AuthCanIResponse:
      description: The verdict for an authorization check.
      type: object
      properties:
        verdict:
          description: >-
            `true` only if the caller is allowed to perform **every** requested
            action on **every** requested resource; `false` otherwise.
          type: boolean
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
