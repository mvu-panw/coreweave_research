# Delete volume

Source: https://docs.coreweave.com/products/sandboxes/reference/control-plane-api/volumeservice/delete-volume

# Delete volume

> Deregister a volume asynchronously. The source storage and its data are never touched.



## OpenAPI

````yaml /openapi/sandboxes/openapi.yaml delete /v1/volumes/{volumeId}
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
  /v1/volumes/{volumeId}:
    delete:
      tags:
        - VolumeService
      summary: Delete volume
      description: >-
        DeleteVolume deregisters a Volume. Deletion is asynchronous: the
        returned
         resource is in VOLUME_STATE_DELETING while platform-created mount
         plumbing is cleaned up, after which GetVolume returns NOT_FOUND. The
         source storage and its data are never touched. Fails FAILED_PRECONDITION
         (CWSANDBOX_VOLUME_IN_USE) while non-terminal sandboxes are attached.
      operationId: VolumeService_DeleteVolume
      parameters:
        - name: volumeId
          in: path
          required: true
          schema:
            type: string
        - name: allowMissing
          in: query
          description: >-
            If true, deleting an absent volume succeeds instead of returning
            NOT_FOUND.
          schema:
            type: boolean
        - name: force
          in: query
          description: >-
            Force deletion when the owning runner is permanently gone:
            hard-deletes
             the registration without waiting for plumbing cleanup, delegating any
             surviving platform-created objects to the background sweep. Never touches
             the source storage or its data.
          schema:
            type: boolean
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/coreweave.sandbox.v1.Volume'
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
    coreweave.sandbox.v1.Volume:
      description: Volume is org-registered shared storage, mountable by sandboxes.
      type: object
      properties:
        volumeId:
          description: |-
            Caller-chosen identifier, unique within the organization, immutable.
             Pattern: ^[a-z][a-z0-9-]{2,62}$
          type: string
        spec:
          $ref: '#/components/schemas/coreweave.sandbox.v1.VolumeSpec'
        status:
          allOf:
            - $ref: '#/components/schemas/coreweave.sandbox.v1.VolumeStatus'
          readOnly: true
      required:
        - spec
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
    coreweave.sandbox.v1.VolumeSpec:
      type: object
      properties:
        pvc:
          $ref: '#/components/schemas/coreweave.sandbox.v1.PvcVolumeSource'
        readOnly:
          description: >-
            Volume-level read-only floor: when true, every mount of this Volume
            is
             read-only. A mount may tighten (read_only=true) but never loosen.
          type: boolean
        description:
          description: Human description; the only mutable field.
          type: string
    coreweave.sandbox.v1.VolumeStatus:
      type: object
      properties:
        state:
          description: >-
            Reported lifecycle state. VOLUME_STATE_UNSPECIFIED means no
            recognized lifecycle state is reported.
          type: string
          format: enum
          enum:
            - VOLUME_STATE_UNSPECIFIED
            - VOLUME_STATE_VALIDATING
            - VOLUME_STATE_READY
            - VOLUME_STATE_ERROR
            - VOLUME_STATE_DELETING
          readOnly: true
        stateReason:
          description: Customer-actionable detail for ERROR/VALIDATING/DELETING.
          type: string
          readOnly: true
        locality:
          description: >-
            Server-derived placement class. PVC-backed volumes report
            VOLUME_LOCALITY_CLUSTER_LOCAL. VOLUME_LOCALITY_UNSPECIFIED means the
            source has no recognized locality. No supported source produces
            VOLUME_LOCALITY_GLOBAL.
          type: string
          format: enum
          enum:
            - VOLUME_LOCALITY_UNSPECIFIED
            - VOLUME_LOCALITY_CLUSTER_LOCAL
            - VOLUME_LOCALITY_GLOBAL
          readOnly: true
        createTime:
          type: string
          format: date-time
          readOnly: true
        updateTime:
          type: string
          format: date-time
          readOnly: true
        lastValidatedTime:
          type: string
          format: date-time
          readOnly: true
        accessModes:
          description: Observed from the claim (pvc source), e.g. ["ReadWriteMany"].
          type: array
          items:
            type: string
          readOnly: true
        capacity:
          description: Observed capacity as a Kubernetes quantity string, e.g. "100Gi".
          type: string
          readOnly: true
        attachedSandboxCount:
          description: Non-terminal sandboxes currently attached.
          type: integer
          format: int32
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
    coreweave.sandbox.v1.PvcVolumeSource:
      description: >-
        PvcVolumeSource references an existing PersistentVolumeClaim in the
        cluster
         that hosts the referenced managed runner. Registration is by reference
         only: the claim and its data are read, never written, by the platform.
         Mounting a Volume with this source pins sandbox scheduling to the owning
         runner.
      type: object
      properties:
        runnerId:
          description: >-
            Org-unique managed-runner id whose cluster holds the claim.
            Immutable.
          type: string
        namespace:
          description: The claim's namespace in that cluster. Immutable.
          type: string
        claimName:
          description: The PersistentVolumeClaim name. Immutable.
          type: string
        subPath:
          description: |-
            Optional volume-level root prefix inside the claim. Relative and
             canonical (no "." / ".."). Immutable.
          type: string
      required:
        - runnerId
        - namespace
        - claimName
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
      description: CoreWeave API access token sent as a bearer token.
      x-default: Bearer {API_ACCESS_TOKEN}

````
