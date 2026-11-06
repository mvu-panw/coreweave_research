# AI Object Storage API

Source: https://docs.coreweave.com/products/storage/object-storage/reference/object-storage-api-ref

# AI Object Storage API

> Manage organization-wide access policies, bucket settings, and access keys

With an access token, you can interact with the CoreWeave AI Object Storage API using `curl` or any other HTTP client. The AI Object Storage API allows users to set organization-wide access policies, configure bucket settings, and manage access keys.

> [!WARNING]
>
> CoreWeave AI Object Storage is an [S3-compatible](https://docs.coreweave.com/products/storage/object-storage/reference/object-storage-s3.md) object storage solution with two APIs.
>
> * Use the **S3-compatible API** for operations like uploading objects.
> * Use the **AI Object Storage API** for tasks outside the S3-compatible API command set, like creating access keys from SAML assertions.

> [!NOTE]
>
> * The API server is `https://api.coreweave.com`.
> * Replace `[API-ACCESS-TOKEN]` in the following examples with your [CoreWeave API access token](https://docs.coreweave.com/security/authn-authz/manage-api-access-tokens.md).

## Operations

Each operation below links to its request and response schema. The same pages are listed in the left sidebar under **AI Object Storage API**. Each HTTP endpoint maps to a gRPC method of the same name on the `CWObject` service.

| Operation | Method | Endpoint | Description |
| - | - | - | - |
| [AuthCanI](https://docs.coreweave.com/products/storage/object-storage/reference/object-storage-api-ref/cwobject/check-authorization.md) | `POST` | `/v1/cwobject/auth/can-i` | Check whether the current user is allowed to perform a set of actions on a set of resources. |
| [CreateAccessKeyFromApiToken](https://docs.coreweave.com/products/storage/object-storage/reference/object-storage-api-ref/cwobject/create-access-key-from-api-token.md) | `GET` | `/v1/cwobject/temporary-credentials/api-token` | Exchange a CoreWeave API access token for temporary credentials, in the AWS container-credentials response format. |
| [CreateAccessKeyFromContainerCreds](https://docs.coreweave.com/products/storage/object-storage/reference/object-storage-api-ref/cwobject/create-access-key-from-container-credentials.md) | `GET` | `/v1/cwobject/temporary-credentials/oidc/[ORG-ID]` | Return short-lived access keys to an in-cluster workload using the workload's own OIDC token. |
| [CreateAccessKeyFromJWT](https://docs.coreweave.com/products/storage/object-storage/reference/object-storage-api-ref/cwobject/create-access-key.md) | `POST` | `/v1/cwobject/access-key` | Create an access key through an API access token. |
| [CreateAccessKeyFromOIDC](https://docs.coreweave.com/products/storage/object-storage/reference/object-storage-api-ref/cwobject/create-access-key-from-oidc.md) | `POST` | `/v1/cwobject/temporary-credentials/oidc` | Exchange an OIDC token from a Workload Identity Federation provider for a time-limited access key. |
| [CreateAccessKeyFromSAML](https://docs.coreweave.com/products/storage/object-storage/reference/object-storage-api-ref/cwobject/create-access-key-from-saml.md) | `POST` | `/v1/cwobject/temporary-credentials/saml` | Generate temporary access keys for CoreWeave AI Object Storage access through a SAML assertion. |
| [DeleteAccessPolicy](https://docs.coreweave.com/products/storage/object-storage/reference/object-storage-api-ref/cwobject/delete-access-policy.md) | `DELETE` | `/v1/cwobject/access-policy/[POLICY-NAME]` | Delete an access policy. |
| [EnsureAccessPolicy](https://docs.coreweave.com/products/storage/object-storage/reference/object-storage-api-ref/cwobject/apply-or-update-access-policy.md) | `POST` | `/v1/cwobject/access-policy` | Apply or update access policies. |
| [GetAccessKeyInfo](https://docs.coreweave.com/products/storage/object-storage/reference/object-storage-api-ref/cwobject/get-access-key.md) | `GET` | `/v1/cwobject/access-key/[ACCESS-KEY-ID]` | Get information about a specific access key. |
| [GetBucketInfo](https://docs.coreweave.com/products/storage/object-storage/reference/object-storage-api-ref/cwobject/get-bucket-info.md) | `GET` | `/v1/cwobject/bucket-info/[BUCKET-NAME]` | Get information about a specific bucket. |
| [ListAccessKeyInfo](https://docs.coreweave.com/products/storage/object-storage/reference/object-storage-api-ref/cwobject/list-access-keys.md) | `GET` | `/v1/cwobject/access-key` | List information about all access keys. |
| [ListAccessPolicies](https://docs.coreweave.com/products/storage/object-storage/reference/object-storage-api-ref/cwobject/list-access-policies.md) | `GET` | `/v1/cwobject/access-policy` | List all Object Storage access policies in the organization. |
| [ListBucketInfo](https://docs.coreweave.com/products/storage/object-storage/reference/object-storage-api-ref/cwobject/list-bucket-info.md) | `GET` | `/v1/cwobject/bucket-info` | List information about all buckets. |
| [RevokeAccessKeyByAccessKey](https://docs.coreweave.com/products/storage/object-storage/reference/object-storage-api-ref/cwobject/revoke-an-access-key.md) | `POST` | `/v1/cwobject/revoke-access-key/access-key` | Revoke a specific access key. |
| [RevokeAccessKeysByPrincipal](https://docs.coreweave.com/products/storage/object-storage/reference/object-storage-api-ref/cwobject/revoke-a-principals-access-keys.md) | `POST` | `/v1/cwobject/revoke-access-key/principal` | Revoke all access keys for a principal. |
| [SetBucketSettings](https://docs.coreweave.com/products/storage/object-storage/reference/object-storage-api-ref/cwobject/set-bucket-settings.md) | `PUT` | `/v1/cwobject/bucket/settings` | Configure bucket settings that aren't exposed in the [S3-compatible API](https://docs.coreweave.com/products/storage/object-storage/reference/object-storage-s3.md). |
| [SetOrganizationSettings](https://docs.coreweave.com/products/storage/object-storage/reference/object-storage-api-ref/cwobject/set-organization-settings.md) | `PUT` | `/v1/cwobject/organization/settings` | Configure settings related to your organization and CoreWeave AI Object Storage. |
| [UpdateAccessKeyStatus](https://docs.coreweave.com/products/storage/object-storage/reference/object-storage-api-ref/cwobject/update-access-key-status.md) | `PUT` | `/v1/cwobject/access-key-status` | Set every access key for a principal to active or suspended. |

## Authentication

Most requests authenticate with a [CoreWeave API access token](https://docs.coreweave.com/security/authn-authz/manage-api-access-tokens.md) sent as a bearer token in the `Authorization` header (the `TokenAuth` scheme). For required permissions on each operation, see [IAM Access Policies](https://docs.coreweave.com/security/iam/access-policies.md).

`GET /v1/cwobject/temporary-credentials/api-token` also uses `TokenAuth`, with the `Bearer` prefix, even though it returns credentials in the AWS container credentials response format. For setup instructions, see [Direct access token exchange](https://docs.coreweave.com/products/storage/object-storage/auth-access/manage-access-keys/api-access-token.md).

Three endpoints are special and call out their own authentication requirements on the per-operation page:

* `POST /v1/cwobject/temporary-credentials/saml` and `POST /v1/cwobject/temporary-credentials/oidc` are **anonymous** on the CoreWeave side. They exchange an external IdP assertion for a CoreWeave access key, so no CoreWeave bearer token is required.
* `GET /v1/cwobject/temporary-credentials/oidc/{orgId}` uses the **`ContainerCredentialsAuth`** scheme: send a raw JWT/OIDC token as the `Authorization` header value with **no** `Bearer` prefix. This shape matches the AWS container-credentials provider for in-cluster workloads.

## gRPC schema and SDKs (Buf)

The AI Object Storage API is also exposed as a gRPC service defined in Protobuf. Use the same API host, `https://api.coreweave.com`, with token-based authentication.

* **Service**: `CWObject` (package `coreweave.cwobject.v1`)
* **Public BSR module**: `buf.build/coreweave/cwobject`
* **TypeScript SDK namespace**: `@buf/coreweave_cwobject.bufbuild_es`

The gRPC methods align with the HTTP endpoints listed in [Operations](#operations).

## Access-key status values

The `status` field on access keys uses the proto-3 enum `AccessKeyStatus`. The wire format is the symbolic name:

| Value | Meaning |
| - | - |
| `ACCESS_KEY_STATUS_ACTIVE` | The key can be used to authenticate. |
| `ACCESS_KEY_STATUS_SUSPENDED` | The key exists but cannot authenticate; reactivate it to restore access. |
| `ACCESS_KEY_STATUS_UNSPECIFIED` | Proto zero value (`field not set`). Do not send it -- the server treats it as missing and rejects the request. The `ListAccessKeyInfo` filter treats it as "no filter applied". |

## Access policies

Access policies use a small grammar that maps cleanly to the AWS IAM shape. Policies are documented in [IAM Access Policies](https://docs.coreweave.com/security/iam/access-policies.md); the canonical list of actions (`cwobject:*`, `s3:*`) lives in the [CoreWeave AI Object Storage actions reference](https://docs.coreweave.com/products/storage/object-storage/auth-access/organization-policies/manage.md#allowed-ai-object-storage-api-actions).

Two fields on the policy schema are open strings on the wire today (upstream emits them as `type: string` with no `enum:` list):

| Field | Valid values |
| - | - |
| `CWObjectPolicyStatement.effect` | `Allow`, `Deny` |
| `CWObjectPolicy.version` | `v1alpha1` |

The auto-generated reference documents these values in the field description prose; the overlay does not add a tooling-enforced `enum` constraint, because upstream would have to renegotiate that constraint every time it adds a new effect or policy version. See the storage overlay report for the upstream recommendation.

## Pagination

The `limit` parameter on `ListAccessKeyInfo` and `ListBucketInfo` accepts values from `1` to `1000` (declared in the proto, reasserted in the overlay because `protoc-gen-openapi` strips the bound). Use `offset` for zero-based pagination.

## OpenAPI specification

The complete OpenAPI 3.0 specification for the CoreWeave AI Object Storage API is embedded below. Expand the code block by clicking "See all" at the bottom, or use the download and copy buttons in the title bar.

```yaml expandable title="Object Storage OpenAPI" theme={"system"}
openapi: 3.0.3
info:
  title: CoreWeave AI Object Storage API
  version: 0.0.1
  description: Manage organization-wide access policies, configure bucket and organization settings, mint
    and revoke access keys, and inspect bucket and access-key inventory.
servers:
- url: https://api.coreweave.com
  description: CoreWeave production API.
paths:
  /v1/cwobject/access-key:
    get:
      operationId: CWObject_ListAccessKeyInfo
      summary: List access keys
      description: Lists access keys in the caller's organization. Secret keys are never returned.
      parameters:
      - name: offset
        in: query
        description: Zero-based offset into the result set. Used with `limit` for pagination.
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
      - name: status
        in: query
        description: Optional access-key status filter. When unset, access keys of every status are returned.
        schema:
          type: string
          format: enum
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ListAccessKeyInfoResponse'
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Status'
      tags:
      - CWObject
    post:
      operationId: CWObject_CreateAccessKeyFromJWT
      summary: Create access key
      description: Creates a CoreWeave AI Object Storage access key, exchanging a CoreWeave API access
        token (Cloud token) for object-storage credentials.
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
      tags:
      - CWObject
  /v1/cwobject/access-key-status:
    put:
      operationId: CWObject_UpdateAccessKeyStatus
      summary: Update access key status
      description: Updates the status of every access key for a principal to `ACTIVE` or `SUSPENDED`.
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/UpdateAccessKeyStatusRequest'
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
      tags:
      - CWObject
  /v1/cwobject/access-key/{accessKeyId}:
    get:
      operationId: CWObject_GetAccessKeyInfo
      summary: Get access key
      description: Retrieves metadata for a specific access key by ID. The secret key is never returned.
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
      tags:
      - CWObject
  /v1/cwobject/access-policy:
    get:
      operationId: CWObject_ListAccessPolicies
      summary: List access policies
      description: Lists every CoreWeave AI Object Storage access policy in the caller's organization.
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ListAccessPoliciesResponse'
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Status'
      tags:
      - CWObject
    post:
      operationId: CWObject_EnsureAccessPolicy
      summary: Apply or update access policy
      description: Creates or updates an access policy that defines who can access object storage and
        what actions they can perform.
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
      tags:
      - CWObject
  /v1/cwobject/access-policy/{name}:
    delete:
      operationId: CWObject_DeleteAccessPolicy
      summary: Delete access policy
      description: Deletes an access policy by name.
      parameters:
      - name: name
        in: path
        required: true
        schema:
          type: string
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
      tags:
      - CWObject
  /v1/cwobject/auth/can-i:
    post:
      operationId: CWObject_AuthCanI
      summary: Check authorization
      description: Checks whether the caller is allowed to perform a set of actions on a set of resources.
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
      tags:
      - CWObject
  /v1/cwobject/bucket-info:
    get:
      operationId: CWObject_ListBucketInfo
      summary: List bucket info
      description: Lists information about every bucket in the caller's organization, including details
        unavailable through the S3-compatible API.
      parameters:
      - name: offset
        in: query
        description: Zero-based offset into the result set. Used with `limit` for pagination.
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
      tags:
      - CWObject
  /v1/cwobject/bucket-info/{bucketName}:
    get:
      operationId: CWObject_GetBucketInfo
      summary: Get bucket info
      description: Retrieves information about a specific bucket, including details unavailable through
        the S3-compatible API.
      parameters:
      - name: bucketName
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
                $ref: '#/components/schemas/GetBucketInfoResponse'
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Status'
      tags:
      - CWObject
  /v1/cwobject/bucket/settings:
    put:
      operationId: CWObject_SetBucketSettings
      summary: Set bucket settings
      description: Configures bucket settings that aren't exposed by the S3-compatible API.
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
      tags:
      - CWObject
  /v1/cwobject/organization/settings:
    put:
      operationId: CWObject_SetOrganizationSettings
      summary: Set organization settings
      description: Configures organization-wide CoreWeave AI Object Storage settings such as default audit
        logging.
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
      tags:
      - CWObject
  /v1/cwobject/revoke-access-key/access-key:
    post:
      operationId: CWObject_RevokeAccessKeyByAccessKey
      summary: Revoke an access key
      description: Revokes a single access key by its access-key value.
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/RevokeAccessKeyByAccessKeyRequest'
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
      tags:
      - CWObject
  /v1/cwobject/revoke-access-key/principal:
    post:
      operationId: CWObject_RevokeAccessKeysByPrincipal
      summary: Revoke a principal's access keys
      description: Revokes every access key owned by the named principal.
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/RevokeAccessKeysByPrincipalRequest'
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
      tags:
      - CWObject
  /v1/cwobject/temporary-credentials/api-token:
    get:
      operationId: CWObject_CreateAccessKeyFromApiToken
      summary: Create access key from API token
      description: Exchanges a CoreWeave API access token for temporary AI Object Storage credentials
        in the AWS container credentials response format. Send the API access token in the `Authorization`
        header with the `Bearer` prefix. For setup instructions, see [Direct access token exchange](/products/storage/object-storage/auth-access/manage-access-keys/api-access-token).
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
      tags:
      - CWObject
  /v1/cwobject/temporary-credentials/oidc:
    post:
      operationId: CWObject_CreateAccessKeyFromOIDC
      summary: Create access key from OIDC
      description: Exchanges an OIDC token from a configured Workload Identity Federation provider for
        a time-limited CoreWeave AI Object Storage access key. No CoreWeave bearer token is required.
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
      tags:
      - CWObject
  /v1/cwobject/temporary-credentials/oidc/{orgId}:
    get:
      operationId: CWObject_CreateAccessKeyFromContainerCreds
      summary: Create access key from container credentials
      description: AWS-style container-credentials provider. Returns short-lived access keys for in-cluster
        workloads using the workload's own OIDC token.
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
      tags:
      - CWObject
  /v1/cwobject/temporary-credentials/saml:
    post:
      operationId: CWObject_CreateAccessKeyFromSAML
      summary: Create access key from SAML
      description: Exchanges a base64-encoded SAML assertion from a configured Workload Identity Federation
        provider for a time-limited CoreWeave AI Object Storage access key. No CoreWeave bearer token
        is required.
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateAccessKeyFromSAMLRequest'
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/CreateAccessKeyFromSAMLResponse'
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Status'
      security: []
      tags:
      - CWObject
components:
  schemas:
    AccessKeyInfo:
      description: Metadata for a single access key. The secret value is never returned by any endpoint.
      type: object
      properties:
        accessKeyId:
          description: The access-key ID.
          type: string
        status:
          description: The current status of the access key (for example, `ACTIVE` or `SUSPENDED`).
          type: string
        principalName:
          description: The fully-qualified principal name that owns the access key.
          type: string
        attributes:
          description: Free-form caller-supplied attributes attached to the key (for example, `name`).
          type: object
          additionalProperties:
            type: string
        expiry:
          description: The expiration time of the access key. Permanent keys may report a sentinel value.
          type: string
          format: date-time
        orgId:
          description: The organization ID that owns the access key.
          type: string
        multiAttributes:
          description: Free-form caller-supplied multi-valued attributes attached to the key. Each value
            is an `AttributeList` (an array of strings) so a single attribute key can carry multiple values.
            Distinct from `attributes`, which holds a single string per key.
          type: object
          additionalProperties:
            $ref: '#/components/schemas/AttributeList'
    AttributeList:
      description: A list of string values used as a single multi-valued attribute on `multiAttributes`.
      type: object
      properties:
        values:
          description: The list of string values for this attribute.
          type: array
          items:
            type: string
    AuthCanIRequest:
      description: Inputs for an authorization check. Both fields are required.
      type: object
      properties:
        actions:
          description: The list of actions to check (for example, `cwobject:ListBucketInfo`).
          type: array
          items:
            type: string
        resources:
          description: The list of resources to check the actions against. Use `["*"]` to check against
            every resource.
          type: array
          items:
            type: string
    AuthCanIResponse:
      description: The verdict for an authorization check.
      type: object
      properties:
        verdict:
          description: '`true` only if the caller is allowed to perform **every** requested action on
            **every** requested resource; `false` otherwise.'
          type: boolean
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
          description: Bucket settings managed through this API (audit logging, and so on).
          $ref: '#/components/schemas/CWObjectBucketSettings'
        location:
          description: The [Availability Zone](https://docs.coreweave.com/platform/regions/about-regions-and-azs#complete-region-list)
            that hosts the bucket (for example, `US-EAST-04A`).
          type: string
        usage:
          description: An array of usage measurements for the bucket.
          type: array
          items:
            $ref: '#/components/schemas/BucketUsageInfo'
    BucketUsageInfo:
      description: A single usage measurement for a bucket.
      type: object
      properties:
        measurementType:
          description: The kind of measurement reported by `value` (for example, `MEASUREMENT_TYPE_USAGE_BYTES`).
          type: string
        value:
          description: The measurement value, encoded as a string for unsigned 64-bit safety across JSON
            consumers.
          type: string
        valueHumanReadable:
          description: A human-readable formatting of `value` (for example, `1.2 GiB`).
          type: string
    CWObjectBucketSettings:
      description: Per-bucket settings managed through the AI Object Storage API.
      type: object
      properties:
        auditLoggingEnabled:
          description: When `true`, audit logging is enabled for the bucket.
          type: boolean
        archiveEnabled:
          description: "When true, idle STANDARD objects are archived to STANDARD_IA after\n archive_after_last_access_days\
            \ without access. Org must be entitled to\n configure this setting."
          type: boolean
        archiveAfterLastAccessDays:
          description: "Days since last access (or creation if never accessed) before a STANDARD\n object\
            \ version is archived to STANDARD_IA. Required when archive_enabled\n is true. Ignored when\
            \ archive_enabled is false."
          type: integer
          format: int32
        capacityCapBytes:
          description: "Sets or replaces the capacity cap in bytes. Zero is a valid cap. Values\n greater\
            \ than 9,223,372,036,854,775,807 bytes are rejected. The caller's\n organization must be entitled."
          type: string
        configuredCapacityCapBytes:
          description: "Read-only: the capacity cap currently configured on the bucket, populated\n on\
            \ GetBucketInfo / ListBucketInfo / SetBucketSettings responses. Unset\n means no cap is configured.\
            \ Ignored on SetBucketSettings requests; use\n capacity_cap_update to modify the cap."
          type: string
    CWObjectOrganizationSettings:
      description: Organization-wide settings managed through the AI Object Storage API.
      type: object
      properties:
        controlPlaneAuditLoggingEnabled:
          description: When `true`, audit logging is enabled for control-plane operations.
          type: boolean
        bucketAuditLoggingEnabled:
          description: When `true`, audit logging is enabled by default for every bucket in the organization.
          type: boolean
    CWObjectPolicy:
      description: A named access policy that grants or denies actions on resources for principals.
      type: object
      properties:
        version:
          description: The schema version for the access policy. Currently always `v1alpha1`.
          type: string
        name:
          description: The unique policy name within the organization.
          type: string
        statements:
          description: An ordered list of statements that make up the policy. The first matching statement
            determines the result.
          type: array
          items:
            $ref: '#/components/schemas/CWObjectPolicyStatement'
    CWObjectPolicyStatement:
      description: A single statement within an access policy.
      type: object
      properties:
        name:
          description: A descriptive name for the statement, scoped to the policy.
          type: string
        effect:
          description: 'Whether the statement allows or denies the listed actions on the listed resources
            for the listed principals. The server accepts exactly two values: `Allow` and `Deny`.'
          type: string
        actions:
          description: The actions the statement applies to. Accepts every S3 action (`s3:*`) and the
            CoreWeave-specific `cwobject:*` namespace. The canonical list lives in [the CoreWeave AI Object
            Storage actions reference](/products/storage/object-storage/auth-access/organization-policies/manage#allowed-ai-object-storage-api-actions)
            and the [IAM Access Policies](/security/iam/access-policies) documentation. `cwobject:*` actions
            must use `"*"` as the resource value.
          type: array
          items:
            type: string
        resources:
          description: The resources the statement applies to. Use `["*"]` to match every resource. `cwobject:*`
            actions must use `["*"]`.
          type: array
          items:
            type: string
        principals:
          description: The principals the statement applies to. Use `["*"]` to match every principal in
            the organization.
          type: array
          items:
            type: string
    CreateAccessKeyFromApiTokenResponse:
      description: "CreateAccessKeyFromApiTokenResponse implements the AWS Container Credentials\n provider\
        \ response format, so the credentials can be consumed directly by AWS\n SDKs and the AWS CLI configured\
        \ for container credentials.\n See https://docs.aws.amazon.com/sdkref/latest/guide/feature-container-credentials.html"
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
    CreateAccessKeyFromContainerCredsResponse:
      description: AWS-compatible container-credentials response shape. The property names use PascalCase
        (`AccessKeyId`, `SecretAccessKey`, `Token`, `Expiration`) so existing AWS SDKs and tooling that
        consume `AWS_CONTAINER_CREDENTIALS_FULL_URI` can adopt this endpoint without code changes. This
        is intentional and differs from every other endpoint, which uses camelCase.
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
          description: Free-form caller-supplied attributes attached to the key (for example, `name`).
          type: object
          additionalProperties:
            type: string
        multiAttributes:
          description: Free-form caller-supplied multi-valued attributes attached to the key. Each value
            is an `AttributeList` (an array of strings).
          type: object
          additionalProperties:
            $ref: '#/components/schemas/AttributeList'
    CreateAccessKeyFromJWTRequest:
      description: Inputs for creating an access key from a CoreWeave Cloud token.
      type: object
      properties:
        durationSeconds:
          description: Lifespan of the resulting access key in seconds. Set to `0` to create a permanent
            key; set to a positive integer to create a temporary key with that lifespan. Required.
          type: integer
          format: uint32
          minimum: 0
        attributes:
          description: Free-form caller-supplied attributes attached to the key (for example, `name`).
          type: object
          additionalProperties:
            type: string
      required:
      - durationSeconds
    CreateAccessKeyFromJWTResponse:
      description: The newly-minted access key. The `secretKey` is the only opportunity to read the secret
        value.
      type: object
      properties:
        accessKeyId:
          description: The access-key ID.
          type: string
        secretKey:
          description: The secret access key. Treat as a credential and store it securely on receipt.
          type: string
        principalName:
          description: The fully-qualified principal name that owns the access key.
          type: string
        expiry:
          description: The expiration time of the access key. Permanent keys may report a sentinel value.
          type: string
          format: date-time
        attributes:
          description: The attributes that were attached to the key on creation.
          type: object
          additionalProperties:
            type: string
    CreateAccessKeyFromOIDCRequest:
      description: Inputs for exchanging an OIDC token for a CoreWeave AI Object Storage access key.
      type: object
      properties:
        durationSeconds:
          description: Lifespan of the resulting access key in seconds. Must be `0-43200` (12 hours maximum).
          type: integer
          format: uint32
          maximum: 43200
          minimum: 0
        orgId:
          description: The CoreWeave organization ID to mint the access key for.
          type: string
        oidcToken:
          description: The OIDC token from the configured Workload Identity Federation provider.
          type: string
        attributes:
          description: Free-form caller-supplied attributes attached to the key (for example, `name`).
          type: object
          additionalProperties:
            type: string
      required:
      - durationSeconds
      - orgId
      - oidcToken
    CreateAccessKeyFromOIDCResponse:
      description: The newly-minted access key. The `secretKey` is the only opportunity to read the secret
        value.
      type: object
      properties:
        accessKeyId:
          description: The access-key ID.
          type: string
        secretKey:
          description: The secret access key. Treat as a credential and store it securely on receipt.
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
    CreateAccessKeyFromSAMLRequest:
      description: Inputs for exchanging a SAML assertion for a CoreWeave AI Object Storage access key.
      type: object
      properties:
        durationSeconds:
          description: Lifespan of the resulting access key in seconds. Must be `0-43200` (12 hours maximum).
          type: integer
          format: uint32
          maximum: 43200
          minimum: 0
        orgId:
          description: The CoreWeave organization ID to mint the access key for.
          type: string
        samlResponse:
          description: The SAML assertion, base64-encoded.
          type: string
        attributes:
          description: Free-form caller-supplied attributes attached to the key (for example, `name`).
          type: object
          additionalProperties:
            type: string
        configId:
          description: The Workload Identity Federation configuration ID that corresponds to the SAML
            provider. Configurations are created from the Cloud Console; see [Using Workload Identity
            Federation with SAML](/products/storage/object-storage/auth-access/workload-identity-federation/saml-workload-federation).
          type: string
      required:
      - durationSeconds
      - orgId
      - samlResponse
    CreateAccessKeyFromSAMLResponse:
      description: The newly-minted access key. The `secretKey` is the only opportunity to read the secret
        value.
      type: object
      properties:
        accessKeyId:
          description: The access-key ID.
          type: string
        secretKey:
          description: The secret access key. Treat as a credential and store it securely on receipt.
          type: string
        principalName:
          description: The fully-qualified principal name that owns the access key (for example, `saml/examplerole`).
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
    EnsureAccessPolicyRequest:
      description: Inputs for creating or replacing an access policy by name.
      type: object
      properties:
        policy:
          description: The full access-policy document. Replaces any existing policy with the same name.
          $ref: '#/components/schemas/CWObjectPolicy'
      required:
      - policy
    GetAccessKeyInfoResponse:
      description: Metadata for a single access key.
      type: object
      properties:
        info:
          description: The access-key metadata.
          $ref: '#/components/schemas/AccessKeyInfo'
    GetBucketInfoResponse:
      description: Inventory and usage information for a single bucket.
      type: object
      properties:
        info:
          description: The bucket metadata.
          $ref: '#/components/schemas/BucketInfo'
    GoogleProtobufAny:
      description: Contains an arbitrary serialized message along with a @type that describes the type
        of the serialized message.
      type: object
      properties:
        '@type':
          description: The type of the serialized message.
          type: string
      additionalProperties: true
    ListAccessKeyInfoResponse:
      description: A page of access-key metadata for the caller's organization.
      type: object
      properties:
        info:
          description: The list of access-key metadata records.
          type: array
          items:
            $ref: '#/components/schemas/AccessKeyInfo'
    ListAccessPoliciesResponse:
      description: Every access policy defined in the caller's organization.
      type: object
      properties:
        policies:
          description: The list of access policies.
          type: array
          items:
            $ref: '#/components/schemas/CWObjectPolicy'
    ListBucketInfoResponse:
      description: A page of bucket inventory and usage records for the caller's organization.
      type: object
      properties:
        info:
          description: The list of bucket metadata records.
          type: array
          items:
            $ref: '#/components/schemas/BucketInfo'
    RevokeAccessKeyByAccessKeyRequest:
      description: Inputs for revoking a single access key by its access-key value.
      type: object
      properties:
        accessKey:
          description: The access-key value (not the ID) to revoke.
          type: string
      required:
      - accessKey
    RevokeAccessKeysByPrincipalRequest:
      description: Inputs for revoking every access key owned by a principal.
      type: object
      properties:
        principalName:
          description: The fully-qualified principal whose access keys should be revoked.
          type: string
      required:
      - principalName
    SetBucketSettingsRequest:
      description: Inputs for configuring per-bucket settings managed through the AI Object Storage API.
      type: object
      properties:
        bucketName:
          description: The name of the bucket to configure.
          type: string
        settings:
          description: The new bucket settings to apply.
          $ref: '#/components/schemas/CWObjectBucketSettings'
    SetBucketSettingsResponse:
      description: The bucket settings after the update is applied.
      type: object
      properties:
        settings:
          description: The bucket settings now in effect.
          $ref: '#/components/schemas/CWObjectBucketSettings'
    SetOrganizationSettingsRequest:
      description: Inputs for configuring organization-wide AI Object Storage settings.
      type: object
      properties:
        settings:
          description: The new organization settings to apply.
          $ref: '#/components/schemas/CWObjectOrganizationSettings'
    SetOrganizationSettingsResponse:
      description: The organization settings after the update is applied.
      type: object
      properties:
        settings:
          description: The organization settings now in effect.
          $ref: '#/components/schemas/CWObjectOrganizationSettings'
    Status:
      description: 'The `Status` type defines a logical error model that is suitable for different programming
        environments, including REST APIs and RPC APIs. It is used by [gRPC](https://github.com/grpc).
        Each `Status` message contains three pieces of data: error code, error message, and error details.
        You can find out more about this error model and how to work with it in the [API Design Guide](https://cloud.google.com/apis/design/errors).'
      type: object
      properties:
        code:
          description: The status code, which should be an enum value of [google.rpc.Code][google.rpc.Code].
          type: integer
          format: int32
        message:
          description: A developer-facing error message, which should be in English. Any user-facing error
            message should be localized and sent in the [google.rpc.Status.details][google.rpc.Status.details]
            field, or localized by the client.
          type: string
        details:
          description: A list of messages that carry the error details.  There is a common set of message
            types for APIs to use.
          type: array
          items:
            $ref: '#/components/schemas/GoogleProtobufAny'
    UpdateAccessKeyStatusRequest:
      description: Inputs for updating the status of every access key owned by a principal.
      type: object
      properties:
        principalName:
          description: The fully-qualified principal whose access-key status should change.
          type: string
        status:
          description: The new status to apply to every access key for the principal. `ACTIVE` makes the
            keys usable; `SUSPENDED` prevents authentication without revoking them. The underlying enum
            also declares `INVALID` (its zero value), which is never valid to send.
          type: string
          format: enum
          enum:
          - ACTIVE
          - SUSPENDED
      required:
      - principalName
      - status
  securitySchemes:
    TokenAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
      description: CoreWeave API access token sent as a bearer token in the `Authorization` header (the
        value is prefixed with `Bearer`). Used by every operation except the SAML/OIDC POST token-exchange
        endpoints (anonymous) and the OIDC container credentials GET (which uses `ContainerCredentialsAuth`).
      x-default: Bearer {API_ACCESS_TOKEN}
    ContainerCredentialsAuth:
      type: apiKey
      in: header
      name: Authorization
      description: Raw JWT/OIDC token sent as the `Authorization` header value with **no** `Bearer` prefix.
        Only used by `GET /v1/cwobject/temporary-credentials/oidc/{orgId}` for the AWS-style container-credentials
        provider.
tags:
- name: CWObject
  description: Endpoints that interact with CoreWeave AI Object Storage outside the S3-compatible API.
security:
- TokenAuth: []
```
