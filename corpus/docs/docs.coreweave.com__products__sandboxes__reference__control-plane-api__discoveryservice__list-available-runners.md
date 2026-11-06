# List available runners

Source: https://docs.coreweave.com/products/sandboxes/reference/control-plane-api/discoveryservice/list-available-runners

# List available runners

> List the runners visible to the caller's organization, with optional view, capability, and visibility filters.



## OpenAPI

````yaml /openapi/sandboxes/openapi.yaml get /v1/availableRunners
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
  /v1/availableRunners:
    get:
      tags:
        - DiscoveryService
      summary: List available runners
      description: >-
        ListAvailableRunners lists the runners visible to the caller's
        organization,
         optionally filtered. RunnerView defaults to BASIC when unspecified.
      operationId: DiscoveryService_ListAvailableRunners
      parameters:
        - name: runnerGroupId
          in: query
          description: Filters (all optional; AND-combined).
          schema:
            type: string
        - name: gpuType
          in: query
          schema:
            type: string
        - name: architecture
          in: query
          schema:
            type: string
        - name: healthyOnly
          in: query
          schema:
            type: boolean
        - name: pageSize
          in: query
          schema:
            type: integer
            format: int32
        - name: pageToken
          in: query
          schema:
            type: string
        - name: view
          in: query
          description: Detail level. Unspecified defaults to BASIC for List.
          schema:
            type: string
            format: enum
            enum:
              - RUNNER_VIEW_UNSPECIFIED
              - RUNNER_VIEW_BASIC
              - RUNNER_VIEW_FULL
        - name: serviceVisibility
          in: query
          description: >-
            Require a runner that can enforce this generic L4 service
            visibility.
             UNSPECIFIED does not filter.
          schema:
            enum:
              - VISIBILITY_UNSPECIFIED
              - VISIBILITY_PUBLIC
              - VISIBILITY_PRIVATE
              - VISIBILITY_CUSTOM
            type: string
            format: enum
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: >-
                  #/components/schemas/coreweave.sandbox.v1.ListAvailableRunnersResponse
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
    coreweave.sandbox.v1.ListAvailableRunnersResponse:
      type: object
      properties:
        runners:
          type: array
          items:
            $ref: '#/components/schemas/coreweave.sandbox.v1.AvailableRunner'
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
    coreweave.sandbox.v1.AvailableRunner:
      description: |-
        AvailableRunner is a caller-facing view of a runner. Sensitive internals
         (cluster, namespace) are omitted.
      type: object
      properties:
        runnerId:
          type: string
          readOnly: true
        runnerGroupId:
          type: string
          readOnly: true
        tags:
          type: array
          items:
            type: string
          readOnly: true
        healthy:
          type: boolean
          readOnly: true
        capabilities:
          description: >-
            Reported features and aggregate capacity ceilings; included at BASIC
            and
             FULL views when capability information is available.
          allOf:
            - $ref: >-
                #/components/schemas/coreweave.sandbox.v1.RunnerCapabilitySummary
          readOnly: true
        resources:
          description: >-
            Dynamic availability; populated at FULL view for owned runners only
            (unset
             for shared-org runners).
          allOf:
            - $ref: '#/components/schemas/coreweave.sandbox.v1.RunnerResourceSummary'
          readOnly: true
        connectedAt:
          type: string
          format: date-time
          readOnly: true
        isShared:
          description: >-
            True if the runner belongs to a shared organization (resources
            omitted).
          type: boolean
          readOnly: true
        organizationId:
          description: |-
            Organization that owns the runner. Runner identity is the pair
             (organization_id, runner_id); runner_id alone is not globally unique.
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
    coreweave.sandbox.v1.RunnerCapabilitySummary:
      description: >-
        RunnerCapabilitySummary describes a runner's reported features and
        aggregate
         capacity ceilings, rather than its currently available resources.

         The max_cpu_millicores, max_memory_bytes, and max_gpu_count values can change
         between responses. Depending on runner configuration, CPU and memory ceilings
         may exclude capacity reserved for GPU workloads and can change without nodes
         being added or removed. These values do not guarantee that a placement fits.

         When capability information is available, feature fields are exposed for
         both owned and shared runners. The max_* values are disclosed only for owned
         runners; they remain zero for shared runners (AvailableRunner.is_shared).
         A zero value alone does not distinguish zero capacity from an unreported or
         undisclosed ceiling.

         When capabilities and resources are both present, use values from the same
         response rather than combining resources with cached ceilings. They need not
         reflect the same measurement time.
      type: object
      properties:
        maxCpuMillicores:
          description: Reported aggregate CPU capacity ceiling, in millicores.
          type: string
          readOnly: true
        maxMemoryBytes:
          description: Reported aggregate memory capacity ceiling, in bytes.
          type: string
          readOnly: true
        maxGpuCount:
          description: Reported aggregate GPU capacity, including GPUs currently in use.
          type: string
          readOnly: true
        supportedGpuTypes:
          type: array
          items:
            type: string
          readOnly: true
        supportedArchitectures:
          type: array
          items:
            type: string
          readOnly: true
        supportsPrivileged:
          type: boolean
          readOnly: true
        availableStorageClasses:
          type: array
          items:
            type: string
          readOnly: true
        supportedServiceVisibilities:
          description: >-
            Generic L4 service visibilities this runner can enforce through the
            v1 Service path. VISIBILITY_UNSPECIFIED denotes ports that are not
            reachable from outside the sandbox. Operator-defined beta mode names
            are never exposed.
          type: array
          items:
            enum:
              - VISIBILITY_UNSPECIFIED
              - VISIBILITY_PUBLIC
              - VISIBILITY_PRIVATE
              - VISIBILITY_CUSTOM
            type: string
            format: enum
          readOnly: true
    coreweave.sandbox.v1.RunnerResourceSummary:
      description: >-
        RunnerResourceSummary is a runner's dynamic, currently-available
        resources.

         available_cpu_millicores and available_memory_bytes are usually the measured
         availability, but for a short window after the runner's capacity changes they
         may instead be reported at the runner's advertised ceiling while that ceiling
         is being republished. In that window a value derived as ceiling minus
         available can read zero even though the runner has usage. available_gpu_count
         is always the measurement.

         When comparing with capacity ceilings, use capabilities from the same
         response when present. The values need not reflect the same measurement time.
      type: object
      properties:
        availableCpuMillicores:
          description: >-
            Measured available CPU in millicores, or the advertised CPU ceiling
            during
             the window described above.
          type: string
          readOnly: true
        availableMemoryBytes:
          description: >-
            Measured available memory in bytes, or the advertised memory ceiling
            during
             the window described above.
          type: string
          readOnly: true
        availableGpuCount:
          description: Measured available GPUs; never adjusted to a ceiling.
          type: string
          readOnly: true
        runningSandboxes:
          type: integer
          format: int32
          readOnly: true
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
      description: CoreWeave API access token sent as a bearer token.
      x-default: Bearer {API_ACCESS_TOKEN}

````
