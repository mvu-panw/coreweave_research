# Apply or update access policy

Source: https://docs.coreweave.com/products/storage/object-storage/reference/object-storage-api-ref/cwobject/apply-or-update-access-policy

# Apply or update access policy

> Create or update an access policy by name.

### **gRPC method:** `EnsureAccessPolicy`

> [!NOTE]
>
> * The API server is `https://api.coreweave.com`.
> * Replace `{API_ACCESS_TOKEN}` with your [CoreWeave API access token](https://docs.coreweave.com/security/authn-authz/manage-api-access-tokens.md).
> * For required permissions, see [IAM Access Policies](https://docs.coreweave.com/security/iam/access-policies.md).

Creates or updates an access policy by name. The supplied
policy replaces any existing policy with the same name.

The `version` field must be `v1alpha1`. Each statement
carries an `effect` (`Allow` or `Deny`), a list of
`actions`, a list of `resources`, and a list of
`principals`. To allow every action on every resource for
every principal, save the following as `data.json`:

```json title="data.json"
{
  "policy": {
    "version": "v1alpha1",
    "name": "test-policy",
    "statements": [
      {
        "name": "allow-everything",
        "effect": "Allow",
        "actions": ["*"],
        "resources": ["*"],
        "principals": ["*"]
      }
    ]
  }
}
```

```bash title="Example request" theme={"system"}
curl -X POST https://api.coreweave.com/v1/cwobject/access-policy \
       -H "Content-Type: application/json" \
       -H "Authorization: Bearer {API_ACCESS_TOKEN}" \
       -d @data.json
```

### Supported actions

Access policies accept every S3 action (`s3:*`) plus a set
of CoreWeave-specific actions in the `cwobject:*` namespace.
The canonical list of `cwobject:*` actions and their
required `resources` value lives in
[the CoreWeave AI Object Storage actions reference](https://docs.coreweave.com/products/storage/object-storage/auth-access/organization-policies/manage.md#allowed-ai-object-storage-api-actions)
and the
[IAM Access Policies](https://docs.coreweave.com/security/iam/access-policies.md)
documentation.


## OpenAPI

````yaml /openapi/storage/openapi.yaml post /v1/cwobject/access-policy
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
  /v1/cwobject/access-policy:
    post:
      tags:
        - CWObject
      summary: Apply or update access policy
      description: >-
        Creates or updates an access policy that defines who can access object
        storage and what actions they can perform.
      operationId: CWObject_EnsureAccessPolicy
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/EnsureAccessPolicyRequest'
      responses:
        '200':
          description: OK
          content: {}
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Status'
components:
  schemas:
    EnsureAccessPolicyRequest:
      description: Inputs for creating or replacing an access policy by name.
      type: object
      properties:
        policy:
          $ref: '#/components/schemas/CWObjectPolicy'
          description: >-
            The full access-policy document. Replaces any existing policy with
            the same name.
      required:
        - policy
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
    CWObjectPolicy:
      description: >-
        A named access policy that grants or denies actions on resources for
        principals.
      type: object
      properties:
        version:
          description: >-
            The schema version for the access policy. Currently always
            `v1alpha1`.
          type: string
        name:
          description: The unique policy name within the organization.
          type: string
        statements:
          description: >-
            An ordered list of statements that make up the policy. The first
            matching statement determines the result.
          type: array
          items:
            $ref: '#/components/schemas/CWObjectPolicyStatement'
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
    CWObjectPolicyStatement:
      description: A single statement within an access policy.
      type: object
      properties:
        name:
          description: A descriptive name for the statement, scoped to the policy.
          type: string
        effect:
          description: >-
            Whether the statement allows or denies the listed actions on the
            listed resources for the listed principals. The server accepts
            exactly two values: `Allow` and `Deny`.
          type: string
        actions:
          description: >-
            The actions the statement applies to. Accepts every S3 action
            (`s3:*`) and the CoreWeave-specific `cwobject:*` namespace. The
            canonical list lives in [the CoreWeave AI Object Storage actions
            reference](/products/storage/object-storage/auth-access/organization-policies/manage#allowed-ai-object-storage-api-actions)
            and the [IAM Access Policies](/security/iam/access-policies)
            documentation. `cwobject:*` actions must use `"*"` as the resource
            value.
          type: array
          items:
            type: string
        resources:
          description: >-
            The resources the statement applies to. Use `["*"]` to match every
            resource. `cwobject:*` actions must use `["*"]`.
          type: array
          items:
            type: string
        principals:
          description: >-
            The principals the statement applies to. Use `["*"]` to match every
            principal in the organization.
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
