# List secret stores

Source: https://docs.coreweave.com/products/sandboxes/reference/control-plane-api/settingsservice/list-secret-stores

# List secret stores

> List the secret stores registered for the caller's organization.



## OpenAPI

````yaml /openapi/sandboxes/openapi.yaml get /v1/settings/secretStores
openapi: 3.0.3
info:
  title: CoreWeave Sandboxes API
  version: 0.0.1
  description: >-
    The Sandboxes API lets you manage runners, templates, volumes, network
    configurations, organization settings, and the lifecycle of individual
    sandboxes on CoreWeave.
servers:
  - url: https://api.cwsandbox.com
    description: >-
      CoreWeave sandbox data plane. Hosts the sandbox lifecycle, volumes,
      snapshots, runner discovery, and organization settings.
  - url: https://api.coreweave.com
    description: >-
      CoreWeave control plane. Hosts managed runner and sandbox template
      administration.
security:
  - bearerAuth: []
tags:
  - name: NetworkConfigService
    description: >-
      Create, get, list, update, and delete desired network configurations.
      Updating a configuration bound to a running sandbox changes its network
      rules without a restart. Requires API enablement and a runner with live
      network update support.
  - name: SandboxService
    description: >-
      Endpoints for the sandbox lifecycle: create (directly, from a template, or
      from a Compose file), get, list, exec, read and write files, snapshot,
      connect, purge, and delete.
  - name: DiscoveryService
    description: >-
      Read-only endpoints for discovering the runners visible to the caller's
      organization, with view, capability, and service-visibility filters.
      Runner IDs are unique only within an organization.
  - name: SettingsService
    description: >-
      Organization-level sandbox settings: the object-storage Workload Identity
      Federation (WIF) configuration, the file-system snapshot bucket
      configuration, Compose build storage, and secret stores.
  - name: VolumeService
    description: >-
      CRUD operations for organization-registered volumes that sandboxes can
      mount, plus the validation call that confirms a volume's backing source is
      usable.
  - name: RunnerManagementService
    description: >-
      CRUD operations for managed runners and the runner policy each one
      carries. Policy is a field on the runner, mutated through
      `CreateManagedRunner` and `UpdateManagedRunner`.
  - name: SandboxTemplateService
    description: >-
      CRUD operations for organization-scoped sandbox templates, the partial
      specs that `CreateSandboxFromTemplate` merges with per-request overrides.
paths:
  /v1/settings/secretStores:
    get:
      tags:
        - SettingsService
      summary: List secret stores
      description: ListSecretStores lists the caller's secret stores.
      operationId: SettingsService_ListSecretStores
      parameters:
        - name: pageSize
          in: query
          schema:
            type: integer
            format: int32
        - name: pageToken
          in: query
          schema:
            type: string
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: >-
                  #/components/schemas/coreweave.sandbox.v1.ListSecretStoresResponse
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/google.rpc.Status'
      servers:
        - url: https://api.cwsandbox.com
          description: CoreWeave sandbox data plane.
components:
  schemas:
    coreweave.sandbox.v1.ListSecretStoresResponse:
      type: object
      properties:
        secretStores:
          type: array
          items:
            $ref: '#/components/schemas/coreweave.sandbox.v1.SecretStore'
        nextPageToken:
          type: string
    google.rpc.Status:
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
            $ref: '#/components/schemas/google.protobuf.Any'
    coreweave.sandbox.v1.SecretStore:
      description: >-
        SecretStore is an org-level secret-store registration. Sandboxes
        reference it
         by name via SecretStoreReference.store_name.
      type: object
      properties:
        name:
          description: |-
            Caller-chosen identifier, unique within the organization. Must match
             ^[a-z][a-z0-9-]{2,62}$. Immutable after creation.
          type: string
        providerType:
          description: >-
            Provider type. Specify a concrete provider on create, full
            replacement, or an update that selects providerType.
            SECRET_STORE_PROVIDER_TYPE_UNSPECIFIED is invalid in these writes.
            An update that excludes this field preserves the existing provider.
            Provider type is immutable: full replacement or an update selecting
            providerType must retain the existing concrete provider.
          type: string
          format: enum
          enum:
            - SECRET_STORE_PROVIDER_TYPE_UNSPECIFIED
            - SECRET_STORE_PROVIDER_TYPE_WANDB
        wandb:
          $ref: '#/components/schemas/coreweave.sandbox.v1.WandBStoreConfig'
        createTime:
          type: string
          format: date-time
          readOnly: true
        updateTime:
          type: string
          format: date-time
          readOnly: true
    google.protobuf.Any:
      description: >-
        Contains an arbitrary serialized message along with a @type that
        describes the type of the serialized message.
      type: object
      properties:
        '@type':
          description: The type of the serialized message.
          type: string
      additionalProperties: true
    coreweave.sandbox.v1.WandBStoreConfig:
      description: WandBStoreConfig configures a Weights & Biases secret store.
      type: object
      properties:
        apiUrl:
          description: Base URL for the W&B API (e.g. "https://api.wandb.ai").
          type: string
        team:
          description: Optional W&B team/entity scope.
          type: string
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
      description: CoreWeave API access token sent as a bearer token.
      x-default: Bearer {API_ACCESS_TOKEN}

````
