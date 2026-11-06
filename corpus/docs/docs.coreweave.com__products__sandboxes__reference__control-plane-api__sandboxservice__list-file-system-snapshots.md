# List file system snapshots

Source: https://docs.coreweave.com/products/sandboxes/reference/control-plane-api/sandboxservice/list-file-system-snapshots

# List file system snapshots

> List the file system snapshots in the caller's organization.



## OpenAPI

````yaml /openapi/sandboxes/openapi.yaml get /v1/fileSystemSnapshots
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
  /v1/fileSystemSnapshots:
    get:
      tags:
        - SandboxService
      summary: List file system snapshots
      description: ListFileSystemSnapshots lists the caller's snapshots.
      operationId: SandboxService_ListFileSystemSnapshots
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
        - name: sourceSandboxId
          in: query
          description: Filter to snapshots created by a specific sandbox.
          schema:
            type: string
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: >-
                  #/components/schemas/coreweave.sandbox.v1.ListFileSystemSnapshotsResponse
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
    coreweave.sandbox.v1.ListFileSystemSnapshotsResponse:
      type: object
      properties:
        fileSystemSnapshots:
          type: array
          items:
            $ref: '#/components/schemas/coreweave.sandbox.v1.FileSystemSnapshot'
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
    coreweave.sandbox.v1.FileSystemSnapshot:
      type: object
      properties:
        fileSystemSnapshotId:
          type: string
          readOnly: true
        state:
          description: >-
            Reported snapshot state. SNAPSHOT_STATE_UNSPECIFIED means no
            recognized public state is available for the stored state.
          type: string
          format: enum
          enum:
            - SNAPSHOT_STATE_UNSPECIFIED
            - SNAPSHOT_STATE_CREATING
            - SNAPSHOT_STATE_READY
            - SNAPSHOT_STATE_FAILED
            - SNAPSHOT_STATE_DELETING
          readOnly: true
        stateReason:
          type: string
          readOnly: true
        sizeBytes:
          type: string
          readOnly: true
        sourceSandboxId:
          type: string
          readOnly: true
        trigger:
          description: >-
            Reported creation trigger. SNAPSHOT_TRIGGER_UNSPECIFIED means no
            recognized public trigger is available for the stored trigger; it
            does not imply manual creation.
          type: string
          format: enum
          enum:
            - SNAPSHOT_TRIGGER_UNSPECIFIED
            - SNAPSHOT_TRIGGER_MANUAL
            - SNAPSHOT_TRIGGER_ON_DELETE
          readOnly: true
        createTime:
          type: string
          format: date-time
          readOnly: true
        completeTime:
          type: string
          format: date-time
          readOnly: true
        sourceVolumeName:
          description: Name of the source volume this snapshot was taken from.
          type: string
          readOnly: true
        objectBucket:
          description: Object-storage bucket the snapshot archive landed in.
          type: string
          readOnly: true
        updatedAt:
          description: When the snapshot record was last updated.
          type: string
          format: date-time
          readOnly: true
        requestId:
          description: Echoes the request_id supplied to CreateFileSystemSnapshot, if any.
          type: string
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
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
      description: CoreWeave API access token sent as a bearer token.
      x-default: Bearer {API_ACCESS_TOKEN}

````
