# Get access key

Source: https://docs.coreweave.com/products/storage/object-storage/reference/object-storage-api-ref/cwobject/get-access-key

# Get access key

> Fetch metadata for a specific access key by ID.

### **gRPC method:** `GetAccessKeyInfo`

> [!NOTE]
>
> * The API server is `https://api.coreweave.com`.
> * Replace `{API_ACCESS_TOKEN}` with your [CoreWeave API access token](https://docs.coreweave.com/security/authn-authz/manage-api-access-tokens.md).
> * For required permissions, see [IAM Access Policies](https://docs.coreweave.com/security/iam/access-policies.md).

Substitute `{accessKeyId}` with the access-key ID returned
from List access keys or Create access key. The secret key
is never returned by this endpoint.

```bash title="Example request" theme={"system"}
curl -X GET https://api.coreweave.com/v1/cwobject/access-key/{accessKeyId} \
       -H "Content-Type: application/json" \
       -H "Authorization: Bearer {API_ACCESS_TOKEN}"
```


## OpenAPI

````yaml /openapi/storage/openapi.yaml get /v1/cwobject/access-key/{accessKeyId}
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
  /v1/cwobject/access-key/{accessKeyId}:
    get:
      tags:
        - CWObject
      summary: Get access key
      description: >-
        Retrieves metadata for a specific access key by ID. The secret key is
        never returned.
      operationId: CWObject_GetAccessKeyInfo
      parameters:
        - name: accessKeyId
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
                $ref: '#/components/schemas/GetAccessKeyInfoResponse'
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Status'
components:
  schemas:
    GetAccessKeyInfoResponse:
      description: Metadata for a single access key.
      type: object
      properties:
        info:
          $ref: '#/components/schemas/AccessKeyInfo'
          description: The access-key metadata.
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
    AccessKeyInfo:
      description: >-
        Metadata for a single access key. The secret value is never returned by
        any endpoint.
      type: object
      properties:
        accessKeyId:
          description: The access-key ID.
          type: string
        status:
          description: >-
            The current status of the access key (for example, `ACTIVE` or
            `SUSPENDED`).
          type: string
        principalName:
          description: The fully-qualified principal name that owns the access key.
          type: string
        attributes:
          description: >-
            Free-form caller-supplied attributes attached to the key (for
            example, `name`).
          type: object
          additionalProperties:
            type: string
        expiry:
          description: >-
            The expiration time of the access key. Permanent keys may report a
            sentinel value.
          type: string
          format: date-time
        orgId:
          description: The organization ID that owns the access key.
          type: string
        multiAttributes:
          description: >-
            Free-form caller-supplied multi-valued attributes attached to the
            key. Each value is an `AttributeList` (an array of strings) so a
            single attribute key can carry multiple values. Distinct from
            `attributes`, which holds a single string per key.
          type: object
          additionalProperties:
            $ref: '#/components/schemas/AttributeList'
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
