# Get build storage configuration

Source: https://docs.coreweave.com/products/sandboxes/reference/control-plane-api/settingsservice/get-build-storage-configuration

# Get build storage configuration

> Read your organization's Compose build storage configuration.



## OpenAPI

````yaml /openapi/sandboxes/openapi.yaml get /v1/settings/buildStorageConfig
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
  /v1/settings/buildStorageConfig:
    get:
      tags:
        - SettingsService
      summary: Get build storage configuration
      description: |-
        GetBuildStorageConfig returns the caller organization's current Compose
         build storage configuration. NOT_FOUND means it has not been configured.
      operationId: SettingsService_GetBuildStorageConfig
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/coreweave.sandbox.v1.BuildStorageConfig'
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
    coreweave.sandbox.v1.BuildStorageConfig:
      description: |-
        BuildStorageConfig is the organization's current Compose build storage
         configuration. Build contexts are stored under the contexts/ prefix and
         failed-build logs under the bob-build-logs/ prefix of the selected bucket.
         Existing builds retain the revision selected at admission.
      type: object
      properties:
        enabled:
          description: >-
            Whether new builds may use this configuration. Setting false
            preserves
             existing builds and does not provision or validate storage.
          type: boolean
        mode:
          description: >-
            Storage ownership mode. Specify a concrete mode on initial
            configuration, full replacement, or an update that selects mode.
            BUILD_STORAGE_MODE_UNSPECIFIED is invalid in these writes. A partial
            update that excludes mode preserves the existing mode.
          type: string
          format: enum
          enum:
            - BUILD_STORAGE_MODE_UNSPECIFIED
            - BUILD_STORAGE_MODE_MANAGED
            - BUILD_STORAGE_MODE_CUSTOMER_OWNED
        bucketName:
          description: Required in CUSTOMER_OWNED mode; must be empty in MANAGED mode.
          type: string
        location:
          description: >-
            Object-storage location. Required on initial configuration/full
            replacement.
             The location of an existing managed bucket can't change.
          type: string
        registryNamespace:
          description: |-
            Customer-owned CWCR namespace for build images. Required on initial
             configuration and full replacement.
          type: string
        billingReference:
          description: >-
            Customer billing attribution reference. Required on initial
            configuration
             and full replacement.
          type: string
        etag:
          description: >-
            Opaque revision token. Omit only for initial configuration. Send the
            value
             returned by Get when updating; a stale value returns FAILED_PRECONDITION.
          type: string
        revision:
          description: Monotonically increasing revision, retained for existing builds.
          type: string
          readOnly: true
        effectiveBucketName:
          description: |-
            Actual bucket selected for this revision. It may still be awaiting
             provisioning when enabled is false.
          type: string
          readOnly: true
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
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
      description: CoreWeave API access token sent as a bearer token.
      x-default: Bearer {API_ACCESS_TOKEN}

````
