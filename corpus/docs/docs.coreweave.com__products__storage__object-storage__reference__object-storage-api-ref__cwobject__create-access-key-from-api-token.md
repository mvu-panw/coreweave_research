# Create access key from API token

Source: https://docs.coreweave.com/products/storage/object-storage/reference/object-storage-api-ref/cwobject/create-access-key-from-api-token

# Create access key from API token

> Exchanges a CoreWeave API access token for temporary AI Object Storage credentials in the AWS container credentials response format. Send the API access token in the `Authorization` header with the `Bearer` prefix. For setup instructions, see [Direct access token exchange](/products/storage/object-storage/auth-access/manage-access-keys/api-access-token).



## OpenAPI

````yaml /openapi/storage/openapi.yaml get /v1/cwobject/temporary-credentials/api-token
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
  /v1/cwobject/temporary-credentials/api-token:
    get:
      tags:
        - CWObject
      summary: Create access key from API token
      description: >-
        Exchanges a CoreWeave API access token for temporary AI Object Storage
        credentials in the AWS container credentials response format. Send the
        API access token in the `Authorization` header with the `Bearer` prefix.
        For setup instructions, see [Direct access token
        exchange](/products/storage/object-storage/auth-access/manage-access-keys/api-access-token).
      operationId: CWObject_CreateAccessKeyFromApiToken
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/CreateAccessKeyFromApiTokenResponse'
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Status'
components:
  schemas:
    CreateAccessKeyFromApiTokenResponse:
      description: >-
        CreateAccessKeyFromApiTokenResponse implements the AWS Container
        Credentials
         provider response format, so the credentials can be consumed directly by AWS
         SDKs and the AWS CLI configured for container credentials.
         See https://docs.aws.amazon.com/sdkref/latest/guide/feature-container-credentials.html
      type: object
      properties:
        AccessKeyId:
          type: string
        SecretAccessKey:
          type: string
        Token:
          type: string
        Expiration:
          type: string
          format: date-time
        attributes:
          type: object
          additionalProperties:
            type: string
        multiAttributes:
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

````
