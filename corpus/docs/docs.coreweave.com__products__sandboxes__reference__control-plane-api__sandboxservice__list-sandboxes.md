# List sandboxes

Source: https://docs.coreweave.com/products/sandboxes/reference/control-plane-api/sandboxservice/list-sandboxes

# List sandboxes

> List the sandboxes in the caller's organization.



## OpenAPI

````yaml /openapi/sandboxes/openapi.yaml get /v1/sandboxes
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
  /v1/sandboxes:
    get:
      tags:
        - SandboxService
      summary: List sandboxes
      description: ListSandboxes lists the caller's sandboxes.
      operationId: SandboxService_ListSandboxes
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
        - name: tags
          in: query
          description: 'Filter: sandboxes matching all tags (AND).'
          schema:
            type: array
            items:
              type: string
        - name: state
          in: query
          description: 'Filter: only sandboxes in this state (STATE_UNSPECIFIED = any).'
          schema:
            type: string
            format: enum
            enum:
              - STATE_UNSPECIFIED
              - STATE_CREATING
              - STATE_RUNNING
              - STATE_COMPLETED
              - STATE_FAILED
              - STATE_TERMINATING
              - STATE_TERMINATED
              - STATE_PENDING
              - STATE_PAUSED
              - STATE_PREPARING
        - name: showTerminated
          in: query
          description: |-
            Include terminal sandboxes within the retention window. Defaults to
             active-only.
          schema:
            type: boolean
        - name: runnerIds
          in: query
          description: 'Filter: sandboxes on any of these runners.'
          schema:
            type: array
            items:
              type: string
        - name: volumeIds
          in: query
          description: 'Filter: sandboxes with any of these registered Volumes attached.'
          schema:
            type: array
            items:
              type: string
        - name: sortDirection
          in: query
          description: >-
            Direction of the creation-time ordering, with sandbox_id breaking
            ties.
             Unspecified means descending: newest first. A page_token must be reused
             with the direction that produced it.
          schema:
            type: string
            format: enum
            enum:
              - SORT_DIRECTION_UNSPECIFIED
              - SORT_DIRECTION_DESCENDING
              - SORT_DIRECTION_ASCENDING
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: >-
                  #/components/schemas/coreweave.sandbox.v1.ListSandboxesResponse
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
    coreweave.sandbox.v1.ListSandboxesResponse:
      type: object
      properties:
        sandboxes:
          type: array
          items:
            $ref: '#/components/schemas/coreweave.sandbox.v1.Sandbox'
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
    coreweave.sandbox.v1.Sandbox:
      description: Sandbox is a single running (or terminal) compute environment.
      type: object
      properties:
        sandboxId:
          description: Server-assigned unique identifier.
          type: string
          readOnly: true
        spec:
          description: >-
            Desired workload. Required on create and immutable thereafter. It is
            absent
             when v1 projects a sandbox created through v1beta2, which has no v1
             SandboxSpec. It is also absent in STATE_PREPARING, and after an image fill
             fails before the spec is stored.
             When create used a template, this is the resolved spec from
             that create — never re-read from the live template.
          allOf:
            - $ref: '#/components/schemas/coreweave.sandbox.v1.SandboxSpec'
        status:
          description: Observed state.
          allOf:
            - $ref: '#/components/schemas/coreweave.sandbox.v1.SandboxStatus'
          readOnly: true
        sourceTemplateId:
          description: >-
            Template selected at create time, if any. Historical provenance;
            retained
             even if the template is later deleted.
          type: string
          readOnly: true
        sourceTemplateRevision:
          description: Revision of the template applied at create time.
          type: string
          readOnly: true
        displayName:
          description: >-
            Optional, immutable lookup name, unique among active sandboxes in
            the
             tenant organization. Case-sensitive, at most 128 UTF-8 bytes; leading or
             trailing whitespace, slashes, colons, control characters, and UUIDs are invalid.
             The name becomes reusable once the sandbox reaches a terminal state.
          type: string
        endpointShareToken:
          description: >-
            CreateSandbox, CreateSandboxFromTemplate, and an identical
            request_id
             replay of that call, after HTTPS URLs confirm. Omitted from Get, List,
             status, and from a successful create while those URLs are unconfirmed.
             Send as X-Sandbox-Share-Token or ?share_token=; both are stripped before
             forwarding.
          type: string
          readOnly: true
        control:
          description: >-
            Who controls the sandbox's containers: CONTROL_CONTAINER_ENGINE for
            a sandbox created with it, and CONTROL_PLATFORM for every other
            sandbox. CONTROL_UNSPECIFIED means no controller is specified;
            successful creates resolve the default to CONTROL_PLATFORM.
          type: string
          format: enum
          enum:
            - CONTROL_UNSPECIFIED
            - CONTROL_PLATFORM
            - CONTROL_CONTAINER_ENGINE
          readOnly: true
      required:
        - spec
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
    coreweave.sandbox.v1.SandboxSpec:
      description: >-
        SandboxSpec is the user-declared workload: one or more containers that
        share
         the sandbox's network and volumes. It is the complete, self-contained
         description of the sandbox — it may not reference cluster-external objects by
         name (no ConfigMap/Secret refs, block devices, or named PVCs); external access
         is only via secret_stores, network_ids, and object_storage_access.

         Every sandbox runs under exactly one per-runner Policy, selected by
         placement. The Policy resolves as a base layer of defaults/attachments
         (runtime defaults < policy base < this spec) and then clamps the resolved
         result against typed constraints; a spec that violates a constraint is
         rejected, not silently rewritten.
      type: object
      properties:
        containers:
          description: >-
            The containers that make up the sandbox (at least one). They share
            the
             sandbox's network (reachable over localhost) and any mounted volumes.
             Exactly one container is primary (see Container.primary). In a
             CONTROL_CONTAINER_ENGINE sandbox, this lists one container, cws-engine,
             with the sandbox's total resources and no image, because the platform
             owns the engine image. That spec can't be sent back through
             CreateSandbox.
          type: array
          items:
            $ref: '#/components/schemas/coreweave.sandbox.v1.Container'
        volumes:
          description: |-
            Sandbox-level volumes. Containers mount these by name via
             Container.volume_mounts; a volume mounted by more than one container is
             shared between them.
          type: array
          items:
            $ref: '#/components/schemas/coreweave.sandbox.v1.SandboxVolume'
        services:
          description: >-
            Services exposed by the sandbox. Set endpoint to request an HTTPS or
            TLS passthrough product endpoint, subject to runner support. A
            service with an endpoint must use PUBLIC visibility and TCP or an
            unset protocol. Omit endpoint for a plain service port.
          type: array
          items:
            $ref: '#/components/schemas/coreweave.sandbox.v1.Service'
        maxLifetimeSeconds:
          description: >-
            Maximum lifetime before automatic termination. 0 = platform default
            (NOT
             unbounded). Values above the platform maximum (currently 30 days) are
             rejected; the applied value is echoed in
             SandboxStatus.effective_max_lifetime_seconds.
          type: integer
          format: int32
        networkIds:
          description: >-
            Network membership is not supported. v1 sandbox creation and stored
            template validation reject a non-empty networkIds list. Use network
            or networkConfigId where supported to configure network rules; these
            fields do not join sandbox networks.
          type: array
          items:
            type: string
        objectStorageAccess:
          description: >-
            Object-storage (S3) access for this sandbox. The minted credential
            is
             injected into every user container.
          allOf:
            - $ref: '#/components/schemas/coreweave.sandbox.v1.ObjectStorageAccess'
        tags:
          description: User-defined tags for organization and List filtering.
          type: array
          items:
            type: string
        runnerIds:
          description: >-
            Restrict scheduling to these operator-assigned runner ids. Valid
            only
             when mode is SANDBOX_MODE_CKS. Entries must be non-blank and unique; at
             most 100 and 64 KiB total may be supplied. If none of the named runners is
             currently eligible, CreateSandbox returns retryable runner unavailability
             because runner registration and health can change.
          type: array
          items:
            type: string
        network:
          description: >-
            Optional write-only network rules for sandbox creation. The platform
            creates a platform-managed NetworkConfig from these rules. Do not
            also set networkConfigId. Sandbox Get and List responses omit this
            field; use networkConfigId to read the desired NetworkConfig
            instead.
          allOf:
            - $ref: '#/components/schemas/coreweave.sandbox.v1.NetworkOptions'
          writeOnly: true
        annotations:
          description: >-
            Key-value metadata applied to the sandbox. On the Kubernetes backend
            these
             become pod annotations; the policy filters dangerous prefixes and caps the
             count.
          type: object
          additionalProperties:
            type: string
        instanceType:
          description: >-
            PROVISIONAL (subject to change): optionally pin the sandbox to a
            specific
             node instance type, constrained to the policy's allow-list. When unset, the
             platform selects an instance from the containers' resource requirements
             (cpu/memory and, for accelerated workloads, Gpu).
          type: string
        mode:
          description: >-
            Optionally select the placement candidate set. Unset defaults to
            SANDBOX_MODE_SERVERLESS. Set SANDBOX_MODE_CKS explicitly to use the
            caller's own-cluster runners; runner_ids requires that explicit CKS
            mode. SANDBOX_MODE_UNSPECIFIED has the same default as omission.
          type: string
          format: enum
          enum:
            - SANDBOX_MODE_UNSPECIFIED
            - SANDBOX_MODE_SERVERLESS
            - SANDBOX_MODE_CKS
        runtimeClass:
          description: >-
            Optionally pin the sandbox's runtime class (e.g. "kata-qemu",
            "gvisor").
             Unset = the policy's default runtime classes
             (SecurityConstraints.default_cpu_runtime_class / default_gpu_runtime_class,
             selected by GPU presence), falling back to the runner's own selection
             when the policy sets no default (a profile-level isolation override where
             one is bound, then the runner's configured CPU/GPU pair). When set, the value is
             used verbatim — the platform never substitutes a variant (a GPU sandbox
             must pin a GPU-capable class itself) — and must be listed by the runner
             policy's allowed_runtime_classes (an empty list permits no pin). The
             resolved class is validated against the policy at create and against the
             placed runner's cluster at placement; a pin that fails either is
             rejected, never rewritten. The class the runner actually applied is
             reported in SandboxStatus.effective_runtime_class. NOTE: a pin requires
             the allow-list even when it names the policy's own default — copying an
             observed effective_runtime_class into a new spec's pin (a clone flow)
             fails under a policy that sets defaults without an allow-list; clone
             flows should leave this unset and let the default apply. Mutually
             exclusive with runtime_class_selection. A runner whose policy defines
             SecurityConstraints.runtime_class_mappings accepts no concrete pin.
          type: string
        networkConfigId:
          description: >-
            Immutable reference to a NetworkConfig. On create, set an unused
            caller-created configuration ID, or omit it to create a
            platform-managed configuration from inline network rules or policy
            defaults. Do not send both networkConfigId and network. Get and List
            project the ID from the binding. Copy NetworkConfig.spec into a new
            configuration to clone rules; copying this ID reuses the same
            resource.
          type: string
        runtimeClassSelection:
          description: |-
            Optionally select a portable runtime class. Each runner policy's
             SecurityConstraints.runtime_class_mappings binds the classes it offers to
             concrete runtimes; only runners whose policy maps the selected class are
             eligible. UNSPECIFIED selects RUNTIME_CLASS_GPU_DEFAULT when any container
             requests GPUs and RUNTIME_CLASS_CPU_DEFAULT otherwise, on runners whose
             policy defines mappings; other runners keep the runtime_class behavior. CPU
             classes require zero GPUs and GPU classes require GPUs (INVALID_ARGUMENT
             otherwise). A recognized class that no runner policy in the requested
             placement scope offers, or that is not yet available, fails with
             FAILED_PRECONDITION (reason CWSANDBOX_RUNTIME_CLASS_UNAVAILABLE); when
             runners that offer it are busy, the create fails with a retryable error
             instead. Mutually exclusive with runtime_class. The concrete runtime the
             runner applied is reported in SandboxStatus.effective_runtime_class.
          type: string
          format: enum
          enum:
            - RUNTIME_CLASS_UNSPECIFIED
            - RUNTIME_CLASS_CPU_DEFAULT
            - RUNTIME_CLASS_CPU_NESTED_VIRT
            - RUNTIME_CLASS_CPU_SNAPSHOT_RESTORE
            - RUNTIME_CLASS_GPU_DEFAULT
      required:
        - containers
    coreweave.sandbox.v1.SandboxStatus:
      description: SandboxStatus is the observed state of a sandbox.
      type: object
      properties:
        state:
          description: >-
            Overall sandbox state, derived from the primary container. In a
            CONTROL_CONTAINER_ENGINE sandbox, that is cws-engine (see Control).
            STATE_UNSPECIFIED means no state is specified.
          type: string
          format: enum
          enum:
            - STATE_UNSPECIFIED
            - STATE_CREATING
            - STATE_RUNNING
            - STATE_COMPLETED
            - STATE_FAILED
            - STATE_TERMINATING
            - STATE_TERMINATED
            - STATE_PENDING
            - STATE_PAUSED
            - STATE_PREPARING
          readOnly: true
        stateReason:
          description: Human-readable reason for the current state (esp. terminal states).
          type: string
          readOnly: true
        createTime:
          type: string
          format: date-time
          readOnly: true
        startTime:
          type: string
          format: date-time
          readOnly: true
        endTime:
          type: string
          format: date-time
          readOnly: true
        services:
          description: >-
            Per-service status, including nested EndpointStatus when product
            endpoints
             are filled on a successful Create response.
          type: array
          items:
            $ref: '#/components/schemas/coreweave.sandbox.v1.ServiceStatus'
          readOnly: true
        resourceUsage:
          description: Real-time resource usage, summed across containers.
          allOf:
            - $ref: '#/components/schemas/coreweave.sandbox.v1.ResourceUsage'
          readOnly: true
        exitCode:
          description: >-
            Exit code of the primary container. Present only when the platform
            observed
             it; zero is a valid observed exit code.
          type: integer
          format: int32
          readOnly: true
        effectiveResources:
          description: >-
            Resolved guaranteed compute allocation (summed across containers)
            after
             platform defaults were applied. For burstable allocations, see
             effective_resource_requirements.
          allOf:
            - $ref: '#/components/schemas/coreweave.sandbox.v1.Resources'
          readOnly: true
        effectiveMaxLifetimeSeconds:
          description: >-
            Applied max lifetime after platform defaulting. Over-max create
            requests
             are rejected and never appear here.
          type: integer
          format: int32
          readOnly: true
        containerStatuses:
          description: Per-container observed state.
          type: array
          items:
            $ref: '#/components/schemas/coreweave.sandbox.v1.ContainerStatus'
          readOnly: true
        runnerId:
          description: >-
            Placement: the runner the sandbox was scheduled onto and its runner
            group.
             Every sandbox — managed pool or CKS — lands on a runner.
          type: string
          readOnly: true
        runnerGroupId:
          type: string
          readOnly: true
        effectiveIngress:
          description: |-
            Resolved ingress rules in effect (the declared rules, or the policy
             default when the spec declared none).
          type: array
          items:
            $ref: '#/components/schemas/coreweave.sandbox.v1.IngressRule'
          readOnly: true
        effectiveEgress:
          description: >-
            Resolved egress rules in effect (the declared rules, or the policy
            default
             when the spec declared none).
          type: array
          items:
            $ref: '#/components/schemas/coreweave.sandbox.v1.EgressRule'
          readOnly: true
        effectiveResourceRequirements:
          description: >-
            Resolved compute allocation (requests + limits, summed across
            containers)
             after platform defaults were applied.
          allOf:
            - $ref: '#/components/schemas/coreweave.sandbox.v1.ResourceRequirements'
          readOnly: true
        attachedVolumeIds:
          description: >-
            Registered Volumes (volume.proto) attached to this sandbox, by
            volume_id.
          type: array
          items:
            type: string
          readOnly: true
        effectiveRuntimeClass:
          description: |-
            The runtime class assigned to the sandbox, as reported by the runner
             that placed it: the spec's pin, the policy's CPU/GPU default, or the
             runner's own configured selection. The literal "<node-default>" means the
             runner affirmatively assigned NO RuntimeClass — the pod runs the node's
             default container runtime, which Kubernetes does not name (the value is
             intentionally not a valid RuntimeClass name, so it can never collide with
             a real class or be pinned). Empty only when the assignment is unknown:
             the sandbox never completed placement, or its runner predates
             runtime-class reporting — then this carries the create-time resolution,
             which may itself be empty.
          type: string
          readOnly: true
        effectiveDnsEgress:
          description: >-
            Effective outbound DNS traffic mode after policy resolution,
            governing
             UDP/TCP destination port 53. UNSPECIFIED when unknown. This is separate
             from the https_hostname destination rules in effective_egress.
          type: string
          format: enum
          enum:
            - DNS_EGRESS_MODE_UNSPECIFIED
            - DNS_EGRESS_MODE_ALLOW
            - DNS_EGRESS_MODE_DENY
          readOnly: true
    coreweave.sandbox.v1.Container:
      description: Container is one container in a sandbox.
      type: object
      properties:
        name:
          description: >-
            Unique name within the sandbox; used as the runtime container name
            and
             to target operations and mount volumes. Must be a DNS-1123 label.
             Must not be cw-object-store-agent, cw-object-store-agent-restore,
             cws-engine, dns-egress, dns-egress-probe, or start with
             cw-object-store-agent-restore-. Duplicate or reserved names are
             INVALID_ARGUMENT (CWSANDBOX_INVALID_REQUEST).
          type: string
        image:
          description: OCI image to run.
          type: string
        command:
          description: Command to run. If empty, the image's entrypoint is used.
          type: string
        args:
          description: Arguments to the command.
          type: array
          items:
            type: string
        environmentVariables:
          description: Environment variables injected into the container.
          type: object
          additionalProperties:
            type: string
        resources:
          description: >-
            Guaranteed compute allocation for this container. Preserved for
            existing v1
             clients. For burstable allocations, use resource_requirements instead.
          allOf:
            - $ref: '#/components/schemas/coreweave.sandbox.v1.Resources'
        files:
          description: Files written into this container's filesystem at startup.
          type: array
          items:
            $ref: '#/components/schemas/coreweave.sandbox.v1.FileMount'
        volumeMounts:
          description: Volumes (from SandboxSpec.volumes) to mount into this container.
          type: array
          items:
            $ref: '#/components/schemas/coreweave.sandbox.v1.VolumeMount'
        secretStores:
          description: >-
            External secret stores to resolve and inject as environment
            variables
             into this container only. Other containers on the same sandbox do not
             receive these values. Referencing a store that is not provisioned for
             the caller returns FAILED_PRECONDITION
             (CWSANDBOX_SECRET_STORE_NOT_PROVISIONED).
          type: array
          items:
            $ref: '#/components/schemas/coreweave.sandbox.v1.SecretStoreReference'
        workingDir:
          description: >-
            Working directory for the command. Defaults to the image's working
            directory.
          type: string
        resourceRequirements:
          description: >-
            Compute allocation for this container: requests (the guaranteed
            floor) and
             optional limits (the burst ceiling). Guaranteed QoS when limits is empty or
             equals requests; Burstable when limits exceeds requests. The sandbox is
             billed for the sum of requests across its containers, which must not exceed
             the platform ceiling — an over-ceiling sandbox is rejected with
             INVALID_ARGUMENT (CWSANDBOX_RESOURCE_CEILING_EXCEEDED), not silently reduced.
             Mutually exclusive with resources. (Serverless pins limits == requests.)
          allOf:
            - $ref: '#/components/schemas/coreweave.sandbox.v1.ResourceRequirements'
        securityContext:
          description: >-
            In-guest security settings (privileged, capabilities, run-as user,
            …),
             contained by the sandbox's isolation boundary and clamped by the runner's
             policy.
          allOf:
            - $ref: '#/components/schemas/coreweave.sandbox.v1.SecurityContext'
        imagePullCredentials:
          description: >-
            Request-scoped image pull credentials for this container's image.
            The
             credential value is resolved from a configured external secret store at
             create time and delivered to the runner as generated Docker config JSON.
          allOf:
            - $ref: '#/components/schemas/coreweave.sandbox.v1.ImagePullCredentials'
        primary:
          description: |-
            When true, this container is the primary: its exit is the sandbox
             outcome (exit_code / COMPLETED / FAILED) and it is the default target
             for Exec, StreamExec, StreamLogs, ReadFile, and WriteFile.

             One container: omit or false — that container is primary. true is also
             accepted.
             More than one container: exactly one must be true. None set, or more
             than one true, is INVALID_ARGUMENT (CWSANDBOX_INVALID_REQUEST).
          type: boolean
        startupProbe:
          description: |-
            Exec probe that must succeed before this container is started. On a
             non-primary container, the next container waits. On the primary, a
             failed probe can fail the sandbox after retries. CreateSandbox omitted
             timings use Probe defaults. An empty probe is omit.
          allOf:
            - $ref: '#/components/schemas/coreweave.sandbox.v1.Probe'
      required:
        - name
        - image
    coreweave.sandbox.v1.SandboxVolume:
      description: |-
        SandboxVolume is a sandbox-level volume declaration: either a scratch
         (or snapshot-restored) volume that lives and dies with the sandbox, or a
         live mount of a registered Volume (volume.proto). The two are a oneof —
         mixing them is unrepresentable, and only the scratch arm participates in
         snapshots. Containers mount either kind via VolumeMount; a volume mounted
         by more than one container is shared between them.
      type: object
      properties:
        name:
          description: >-
            Unique name within the sandbox; referenced by VolumeMount.volume and
            used to
             target snapshots.
          type: string
        scratch:
          description: A sandbox-lifetime scratch volume.
          allOf:
            - $ref: '#/components/schemas/coreweave.sandbox.v1.ScratchVolume'
        volumeId:
          description: >-
            A registered Volume (VolumeService) mounted live: writes go against
            the
             shared backing store and are visible to every mounter. Never
             snapshotted. A CLUSTER_LOCAL Volume (pvc source) pins scheduling to
             its owning runner, so declaring one with mode = SANDBOX_MODE_SERVERLESS
             is INVALID_ARGUMENT — the managed pool can never satisfy the pin.
          type: string
      required:
        - name
    coreweave.sandbox.v1.Service:
      description: >-
        Service declares a port the workload listens on, its reachability
        intent,
         and an optional product endpoint opt-in.
      type: object
      properties:
        port:
          type: integer
          format: int32
        name:
          type: string
        protocol:
          description: >-
            L4 for K8s Service/Pod/NetworkPolicy. Unset = TCP. Not endpoint
            kind. Omit this field for TCP; SERVICE_PROTOCOL_UNSPECIFIED also
            uses SERVICE_PROTOCOL_TCP.
          type: string
          format: enum
          enum:
            - SERVICE_PROTOCOL_UNSPECIFIED
            - SERVICE_PROTOCOL_TCP
            - SERVICE_PROTOCOL_UDP
            - SERVICE_PROTOCOL_SCTP
        visibility:
          description: >-
            Who may reach this port. Declared intent only — the platform chooses
            the
             mechanism. Defaults to VISIBILITY_UNSPECIFIED (not reachable outside the
             sandbox).
          type: string
          format: enum
          enum:
            - VISIBILITY_UNSPECIFIED
            - VISIBILITY_PUBLIC
            - VISIBILITY_PRIVATE
            - VISIBILITY_CUSTOM
        endpoint:
          description: >-
            Optional HTTPS or TLS passthrough product endpoint, subject to
            runner support. Requires PUBLIC visibility and TCP or an unset
            protocol. Omit for a plain service port.
          allOf:
            - $ref: '#/components/schemas/coreweave.sandbox.v1.EndpointSpec'
      required:
        - port
    coreweave.sandbox.v1.ObjectStorageAccess:
      description: >-
        ObjectStorageAccess grants the sandbox temporary access to
        object-storage
         buckets. The minted credential is injected into every user container.
      type: object
      properties:
        buckets:
          type: array
          items:
            type: string
        permission:
          description: >-
            Requested object-storage permission. Specify
            OBJECT_STORAGE_PERMISSION_READ or
            OBJECT_STORAGE_PERMISSION_READ_WRITE. Omitted or
            OBJECT_STORAGE_PERMISSION_UNSPECIFIED is invalid; it does not
            default to read access.
          type: string
          format: enum
          enum:
            - OBJECT_STORAGE_PERMISSION_UNSPECIFIED
            - OBJECT_STORAGE_PERMISSION_READ
            - OBJECT_STORAGE_PERMISSION_READ_WRITE
        objectPrefix:
          description: >-
            Optional object-prefix that scopes the minted credential to a
            sub-path
             within the granted buckets. Stamped verbatim into the CAIOS bucket policy;
             see v1beta2 ObjectStorageAccess.object_prefix for the validation contract.
          type: string
    coreweave.sandbox.v1.NetworkOptions:
      description: >-
        NetworkOptions declares the sandbox's network intent beyond port
        exposure.
      type: object
      properties:
        ingress:
          description: >-
            Inbound sources for ports with visibility = CUSTOM: an allow-only
            rule set
             over a default-deny base. A CUSTOM port not matched by any rule is
             unreachable. A rule outside the runner policy's allowed ingress envelope
             is rejected at create, never silently narrowed. Empty = the policy's
             default ingress. The rules in effect are echoed in
             SandboxStatus.effective_ingress.
          type: array
          items:
            $ref: '#/components/schemas/coreweave.sandbox.v1.IngressRule'
        egress:
          description: >-
            Egress destinations the sandbox needs. These grants are additive:
            traffic
             matching any rule is allowed, subject to dns_egress. A rule outside the
             runner policy's allowed envelope is rejected at create, never silently
             narrowed. Empty = the policy's default egress. Platform DNS and storage
             access are granted separately; dns_egress=DENY blocks UDP/TCP port 53
             across all grants. Resolved destination rules are echoed in
             SandboxStatus.effective_egress.
          type: array
          items:
            $ref: '#/components/schemas/coreweave.sandbox.v1.EgressRule'
        denyEgress:
          description: >-
            When true, applies no declared or default egress rules. Mutually
            exclusive
             with egress rules and always admitted as a narrowing of allowed_egress.
             Platform DNS and storage access remain separate. Set dns_egress=DENY to
             also block outbound UDP/TCP port 53. An empty egress list with this flag
             unset instead inherits the policy's default_egress.
          type: boolean
        denyIngress:
          description: >-
            When true, deny declared and policy-default ingress to CUSTOM
            services. NetworkConfig create and update requests reject a
            non-empty ingress list when denyIngress is true. To deny ingress in
            an update, clear the list and set this flag in the same request.
            PUBLIC and PRIVATE service visibility is unchanged.
          type: boolean
        dnsEgress:
          description: >-
            Outbound DNS traffic mode on UDP/TCP destination port 53.
            UNSPECIFIED
             inherits Policy.constraints.network.dns_egress. DENY overrides port-53
             access in all egress grants; ALLOW is rejected when the policy requires
             DENY. This is independent of https_hostname destination rules and does
             not provide a DNS query-name allowlist. See DNSEgressMode for scope.
          type: string
          format: enum
          enum:
            - DNS_EGRESS_MODE_UNSPECIFIED
            - DNS_EGRESS_MODE_ALLOW
            - DNS_EGRESS_MODE_DENY
    coreweave.sandbox.v1.ServiceStatus:
      description: |-
        ServiceStatus echoes a create Service row. Nested endpoint is unset when
         create had no product endpoint; url stays empty until filled.
      type: object
      properties:
        port:
          type: integer
          format: int32
          readOnly: true
        name:
          type: string
          readOnly: true
        protocol:
          description: >-
            Declared service protocol. SERVICE_PROTOCOL_UNSPECIFIED means TCP;
            the response can retain the unspecified value instead of normalizing
            it to SERVICE_PROTOCOL_TCP.
          type: string
          format: enum
          enum:
            - SERVICE_PROTOCOL_UNSPECIFIED
            - SERVICE_PROTOCOL_TCP
            - SERVICE_PROTOCOL_UDP
            - SERVICE_PROTOCOL_SCTP
          readOnly: true
        visibility:
          description: >-
            Declared service visibility. VISIBILITY_UNSPECIFIED means the port
            is not reachable from outside the sandbox.
          type: string
          format: enum
          enum:
            - VISIBILITY_UNSPECIFIED
            - VISIBILITY_PUBLIC
            - VISIBILITY_PRIVATE
            - VISIBILITY_CUSTOM
          readOnly: true
        endpoint:
          allOf:
            - $ref: '#/components/schemas/coreweave.sandbox.v1.EndpointStatus'
          readOnly: true
        url:
          description: >-
            Generic L4 connection target for this service (tcp/udp/sctp). Empty
            for
             VISIBILITY_UNSPECIFIED, before the observed address is ready, and whenever
             the sandbox is not RUNNING. This is separate from product endpoint status.
          type: string
          readOnly: true
    coreweave.sandbox.v1.ResourceUsage:
      description: ResourceUsage is real-time consumption.
      type: object
      properties:
        cpuMillicores:
          type: string
          readOnly: true
        memoryMb:
          type: string
          readOnly: true
        gpuCount:
          type: string
          readOnly: true
    coreweave.sandbox.v1.Resources:
      description: Resources is a guaranteed compute allocation for a container.
      type: object
      properties:
        cpu:
          description: CPU cores, decimal or milli (e.g. "500m", "2", "2.5").
          type: string
        memory:
          description: Memory with a binary/decimal suffix (e.g. "512Mi", "4Gi").
          type: string
        gpu:
          description: >-
            GPU allocation. Permitted on the primary container only; a
            non-primary
             container that sets gpu is INVALID_ARGUMENT (CWSANDBOX_INVALID_REQUEST).
          allOf:
            - $ref: '#/components/schemas/coreweave.sandbox.v1.Gpu'
    coreweave.sandbox.v1.ContainerStatus:
      description: ContainerStatus is the observed state of a single container.
      type: object
      properties:
        name:
          type: string
          readOnly: true
        state:
          description: >-
            Reported container state. STATE_UNSPECIFIED means no state is
            specified.
          type: string
          format: enum
          enum:
            - STATE_UNSPECIFIED
            - STATE_CREATING
            - STATE_RUNNING
            - STATE_COMPLETED
            - STATE_FAILED
            - STATE_TERMINATING
            - STATE_TERMINATED
            - STATE_PENDING
            - STATE_PAUSED
            - STATE_PREPARING
          readOnly: true
        exitCode:
          description: Exit code; set once the container reaches COMPLETED or FAILED.
          type: integer
          format: int32
          readOnly: true
        restartCount:
          description: Number of times the container has restarted.
          type: integer
          format: int32
          readOnly: true
    coreweave.sandbox.v1.IngressRule:
      description: >-
        IngressRule allows inbound traffic from one source class to the
        sandbox's
         CUSTOM-visibility ports, optionally narrowed to specific ports (source AND
         ports; empty ports = all CUSTOM-visibility ports). Sources are
         address-shaped or relational; inbound packets carry no names, so there are
         no name-based sources. SANDBOX_NETWORK tenant scope is rejected until
         network_ids has an enforcement backend.
      type: object
      properties:
        cidr:
          description: Source addresses, with optional carve-outs.
          allOf:
            - $ref: '#/components/schemas/coreweave.sandbox.v1.CidrBlock'
        tenant:
          description: >-
            Other sandboxes, selected by tenant relationship. When selecting
            this source, use TENANT_SCOPE_SAME_USER or TENANT_SCOPE_SAME_ORG.
            TENANT_SCOPE_UNSPECIFIED and TENANT_SCOPE_SANDBOX_NETWORK are
            invalid. Omit tenant when selecting another source.
          type: string
          format: enum
          enum:
            - TENANT_SCOPE_UNSPECIFIED
            - TENANT_SCOPE_SAME_USER
            - TENANT_SCOPE_SAME_ORG
            - TENANT_SCOPE_SANDBOX_NETWORK
        any:
          description: |-
            Any source, including the public internet. Authorizes packets that
             arrive on CUSTOM ports without peer restriction; reachability /
             front-door exposure is out of scope for this rule.
          type: boolean
        ports:
          description: >-
            Declared ports this rule applies to. Empty = all CUSTOM-visibility
            ports.
          type: array
          items:
            $ref: '#/components/schemas/coreweave.sandbox.v1.PortRange'
    coreweave.sandbox.v1.EgressRule:
      description: >-
        EgressRule allows traffic to one destination class, optionally narrowed
        to
         specific ports (destination AND ports; empty ports = all ports).
      type: object
      properties:
        cidr:
          description: >-
            An IP range with optional carve-outs. An except narrows only THIS
            rule's
             range — another rule may still allow the excepted addresses.
          allOf:
            - $ref: '#/components/schemas/coreweave.sandbox.v1.CidrBlock'
        httpsHostname:
          description: |-
            An HTTPS destination hostname, matched against TLS Server Name
             Indication (SNI): exact ("pypi.org") or a single leftmost wildcard label
             ("*.example.com" matches "foo.example.com", not "bar.foo.example.com").
             On Policy.allowed_egress, "*" entitles every name; it is not a sandbox
             grant. No other pattern forms. On a sandbox this is a hostname grant
             for HTTPS (TCP 443). On a name rule, ports must be empty or exactly
             TCP 443; empty means this 443 path, not all ports. Any other ports
             list is rejected. On Policy.allowed_egress it is a ceiling for those
             grants: every declared name must match an allowed pattern or an `any`
             entitlement; a CIDR-only envelope does not entitle names. Carve names
             out of this ceiling with https_hostname_except. Policy.default_egress must
             not set https_hostname — a curated site set belongs on a SandboxTemplate.
             This rule authorizes HTTPS access, not DNS queries or resolutions.
             Outbound DNS traffic is governed separately by network.dns_egress.
             Requires a runner that can enforce hostname-based HTTPS rules;
             otherwise create is rejected rather than ignoring the rule.
          type: string
        tenant:
          description: >-
            Other sandboxes, selected by tenant relationship. When selecting
            this destination, use TENANT_SCOPE_SAME_USER or
            TENANT_SCOPE_SAME_ORG. TENANT_SCOPE_UNSPECIFIED and
            TENANT_SCOPE_SANDBOX_NETWORK are invalid. Omit tenant when selecting
            another destination.
          type: string
          format: enum
          enum:
            - TENANT_SCOPE_UNSPECIFIED
            - TENANT_SCOPE_SAME_USER
            - TENANT_SCOPE_SAME_ORG
            - TENANT_SCOPE_SANDBOX_NETWORK
        any:
          description: |-
            All destinations reachable from the sandbox's network, excluding
             platform-internal ranges (cluster-internal, link-local, and
             cloud-metadata addresses are always carved out). Use tenant or
             selector rules to reach other sandboxes or in-cluster workloads.
          type: boolean
        selector:
          description: |-
            Cluster workloads selected by label. Entitlement is EXPLICIT-ONLY: a
             policy `any` entitlement covers address-shaped destinations but never
             selectors — when the policy constrains egress (non-empty
             allowed_egress), declaring a selector requires a selector entitlement
             there, so an open-egress policy does not silently grant label-based
             selection of co-located workloads. A policy with EMPTY allowed_egress
             constrains nothing and admits selector declarations like every other
             type.
          allOf:
            - $ref: '#/components/schemas/coreweave.sandbox.v1.SelectorBlock'
        ports:
          description: Ports the destination may be reached on. Empty = all ports.
          type: array
          items:
            $ref: '#/components/schemas/coreweave.sandbox.v1.PortRange'
        httpsHostnameExcept:
          description: |-
            Hostnames excluded from this rule's HTTPS grant. Valid only with
             https_hostname on Policy.allowed_egress. An except narrows only THIS rule;
             another allowed_egress rule may still entitle the hostname. Grammar matches
             https_hostname except "*". Each except must be covered by this rule's
             hostname pattern ("*" may except any name; "*.example.com" may except
             "foo.example.com"). "evil.com"
             does not except "www.evil.com"; add "*.evil.com" to cover one label
             under that apex. Extra labels (a.b.evil.com) remain entitled under
             those excepts. A declared name or wildcard whose match set covers an
             except is not entitled by this rule.
          type: array
          items:
            type: string
    coreweave.sandbox.v1.ResourceRequirements:
      description: |-
        ResourceRequirements is a container's compute allocation: requests (the
         guaranteed floor) and optional limits (the burst ceiling). Guaranteed QoS when
         limits is empty or equals requests; Burstable when limits exceeds requests.
         GPU is taken from requests (it is not a burst dimension).
      type: object
      properties:
        requests:
          $ref: '#/components/schemas/coreweave.sandbox.v1.Resources'
        limits:
          $ref: '#/components/schemas/coreweave.sandbox.v1.Resources'
    coreweave.sandbox.v1.FileMount:
      description: FileMount is a file written into a container at startup.
      type: object
      properties:
        path:
          type: string
        content:
          type: string
          format: bytes
      required:
        - path
        - content
    coreweave.sandbox.v1.VolumeMount:
      description: VolumeMount mounts a SandboxVolume into a container.
      type: object
      properties:
        volume:
          type: string
        mountPath:
          type: string
        readOnly:
          type: boolean
        subPath:
          description: |-
            Relative path inside the volume to mount instead of its root. For a
             registered Volume the effective path is the volume source's sub_path
             joined with this value. Must be relative and canonical (no "." / "..").
          type: string
      required:
        - volume
        - mountPath
    coreweave.sandbox.v1.SecretStoreReference:
      description: >-
        SecretStoreReference resolves secrets from a configured external store
        into
         environment variables.
      type: object
      properties:
        storeName:
          description: >-
            Name of the secret store. W&B-authenticated callers may use the
            built-in
             identity-backed store name "wandb" without creating a SecretStore row; all
             other names are resolved from configured SecretStores.
          type: string
        secrets:
          type: array
          items:
            $ref: '#/components/schemas/coreweave.sandbox.v1.SecretMapping'
      required:
        - storeName
        - secrets
    coreweave.sandbox.v1.SecurityContext:
      description: >-
        SecurityContext sets in-guest privilege for a container. These settings
        are contained within the sandbox's isolation boundary and are subject to
        the runner policy's security constraints. This resource does not
        configure host namespaces or hostPath volumes. Host-reaching settings
        are also rejected in v1 policy base attachments.
      type: object
      properties:
        runAsUser:
          description: >-
            UID/GID to run the entrypoint as. Unset = the image's user. uint32
            covers
             the full Linux id space and renders as a JSON number for REST consumers.
          type: integer
          format: uint32
        runAsGroup:
          type: integer
          format: uint32
        privileged:
          description: |-
            Run the container in privileged mode, within the sandbox's isolation
             boundary. Policy-gated.
          type: boolean
        allowPrivilegeEscalation:
          description: Allow a process to gain more privileges than its parent.
          type: boolean
        readOnlyRootFilesystem:
          description: Mount the container's root filesystem read-only.
          type: boolean
        capabilitiesAdd:
          description: >-
            Linux capabilities to add and to drop (e.g. "NET_ADMIN",
            "SYS_PTRACE").
          type: array
          items:
            type: string
        capabilitiesDrop:
          type: array
          items:
            type: string
        seccompProfile:
          description: 'Seccomp profile: "RuntimeDefault" or "Unconfined".'
          type: string
    coreweave.sandbox.v1.ImagePullCredentials:
      description: >-
        ImagePullCredentials identifies the registry authority and provider
        secret
         source used to synthesize Docker config JSON for a private image pull.
      type: object
      properties:
        registry:
          description: >-
            Registry authority for the credential and generated Docker config
            auth key.
          type: string
        credentials:
          description: >-
            Provider secret source that resolves to a structured object
            containing
             non-empty string fields named "username" and "password".
          allOf:
            - $ref: '#/components/schemas/coreweave.sandbox.v1.SecretSource'
      required:
        - registry
        - credentials
    coreweave.sandbox.v1.Probe:
      description: |-
        Probe is an exec-only startup check on a container.

         CreateSandbox omitted timings: period 10s, timeout 1s, failure_threshold 3,
         initial_delay_seconds 0. An empty Probe (no exec) is omit.

         CreateSandboxFromFile Compose healthcheck: omitted timings take Compose
         defaults, then map. interval → period_seconds and timeout →
         timeout_seconds (integer seconds; sub-second values reject). start_period
         raises failure_threshold (retries + ceil(start_period / period));
         initial_delay_seconds stays 0. The container is killed when
         failure_threshold is reached.
      type: object
      properties:
        exec:
          type: array
          items:
            type: string
        periodSeconds:
          type: integer
          format: int32
        timeoutSeconds:
          type: integer
          format: int32
        failureThreshold:
          type: integer
          format: int32
        initialDelaySeconds:
          type: integer
          format: int32
    coreweave.sandbox.v1.ScratchVolume:
      description: |-
        ScratchVolume configures a sandbox-lifetime scratch volume, optionally
         restored from a FileSystemSnapshot.
      type: object
      properties:
        size:
          description: >-
            Size with a binary/decimal suffix, e.g. "10Gi". MEMORY-medium
            volumes may
             instead declare a percentage of the sandbox's total resolved memory
             request, e.g. "50%" (integer 1-100): the platform resolves it to an
             absolute size at create time against the post-defaults request sum, and
             the resolved absolute size is what is enforced and echoed. MEMORY-medium
             volumes MUST declare a size (absolute or percent) — an unbounded
             RAM-backed volume is rejected; percent form is invalid for DISK.
          type: string
        medium:
          description: >-
            Backing medium. Defaults to disk; MEMORY is RAM-backed (tmpfs) and
            counts against the mounting container's memory (e.g. BuildKit's
            /var/lib/buildkit) and against the policy's memory ceiling (resolved
            sizes sum with container memory requests). Omit this field for
            disk-backed storage; STORAGE_MEDIUM_UNSPECIFIED also uses
            STORAGE_MEDIUM_DISK.
          type: string
          format: enum
          enum:
            - STORAGE_MEDIUM_UNSPECIFIED
            - STORAGE_MEDIUM_DISK
            - STORAGE_MEDIUM_MEMORY
        restoreFromSnapshotId:
          description: >-
            If set, the volume is restored from this snapshot; otherwise it
            starts
             empty.
          type: string
    coreweave.sandbox.v1.EndpointSpec:
      description: >-
        EndpointSpec is the create-time opt-in for a product endpoint on a
        Service.
      type: object
      properties:
        kind:
          description: Required when endpoint is set. UNSPECIFIED is rejected when wired.
          type: string
          format: enum
          enum:
            - ENDPOINT_KIND_UNSPECIFIED
            - ENDPOINT_KIND_HTTPS
            - ENDPOINT_KIND_TLS_PASSTHROUGH
        auth:
          description: >-
            Required when kind = HTTPS. UNSPECIFIED is rejected when wired. For
            TLS passthrough, leave authentication unset;
            ENDPOINT_AUTH_UNSPECIFIED is required and does not mean
            ENDPOINT_AUTH_OPEN.
          type: string
          format: enum
          enum:
            - ENDPOINT_AUTH_UNSPECIFIED
            - ENDPOINT_AUTH_OPEN
            - ENDPOINT_AUTH_SHARE_TOKEN
        requestTimeoutSeconds:
          description: >-
            Seconds before the platform closes an in-flight HTTPS request while
            the
             sandbox remains alive. Unset or 0 selects the platform default of 15 seconds.
             An explicit value must be between 15 and 900 inclusive. Rejected when kind
             is not HTTPS. Sandbox lifetime, deletion, or failure may end the request
             first, possibly as a transport error rather than HTTP 504.
          type: integer
          format: int32
      required:
        - kind
    coreweave.sandbox.v1.EndpointStatus:
      type: object
      properties:
        kind:
          description: >-
            Accepted endpoint kind. ENDPOINT_KIND_UNSPECIFIED is invalid when
            requesting an endpoint. When no endpoint was requested, the endpoint
            status is absent.
          type: string
          format: enum
          enum:
            - ENDPOINT_KIND_UNSPECIFIED
            - ENDPOINT_KIND_HTTPS
            - ENDPOINT_KIND_TLS_PASSTHROUGH
          readOnly: true
        auth:
          description: >-
            Accepted endpoint authentication setting. HTTPS requires
            ENDPOINT_AUTH_OPEN or ENDPOINT_AUTH_SHARE_TOKEN. TLS passthrough
            requires authentication to be unset and reports
            ENDPOINT_AUTH_UNSPECIFIED; this does not mean ENDPOINT_AUTH_OPEN.
          type: string
          format: enum
          enum:
            - ENDPOINT_AUTH_UNSPECIFIED
            - ENDPOINT_AUTH_OPEN
            - ENDPOINT_AUTH_SHARE_TOKEN
          readOnly: true
        url:
          description: |-
            Assigned product HTTPS URL for this endpoint. When present, the same
             absolute https:// URL is durable across live Create, GetSandbox,
             ListSandboxes, and idempotent Create replay while the sandbox is CREATING
             or RUNNING. Empty until assignment completes, when no product HTTPS
             endpoints were requested, or when the sandbox is TERMINATING/terminal
             (any stored assignment is retained but suppressed). A non-empty URL means
             the address was assigned, not that the application or edge is ready to serve.
             TLS passthrough endpoints leave this empty.
          type: string
          readOnly: true
        requestTimeoutSeconds:
          description: >-
            Effective configured HTTPS request timeout in seconds while the
            sandbox
             remains alive. Unset or 0 on create is echoed as the platform default.
             Unset when kind is not HTTPS. This is the accepted create value, not a
             live observation of the serving path. Sandbox lifetime, deletion, or
             failure may end the request first, possibly as a transport error rather
             than HTTP 504.
          type: integer
          format: int32
          readOnly: true
        address:
          description: >-
            Assigned product TLS passthrough target as host:port. Clients must
            use
             the host as TLS SNI. When present, the same host:port is durable across
             live Create, GetSandbox, ListSandboxes, and idempotent Create replay
             while the sandbox is CREATING or RUNNING. Empty until assignment
             completes, when no product TLS passthrough endpoints were requested, or
             when the sandbox is TERMINATING/terminal (any stored assignment is
             retained but suppressed). A non-empty address means the target was
             assigned, not that the application or edge is ready to serve. HTTPS
             endpoints leave this empty; TLS passthrough endpoints leave url empty.
          type: string
          readOnly: true
    coreweave.sandbox.v1.Gpu:
      description: Gpu specifies GPU allocation by type or by VRAM.
      type: object
      properties:
        count:
          type: string
        type:
          type: string
        memoryGb:
          type: string
    coreweave.sandbox.v1.CidrBlock:
      description: CidrBlock is an IP range with optional carved-out sub-ranges.
      type: object
      properties:
        cidr:
          description: CIDR, e.g. "0.0.0.0/0" or "203.0.113.0/24".
          type: string
        except:
          description: Sub-ranges of cidr excluded from this rule.
          type: array
          items:
            type: string
      required:
        - cidr
    coreweave.sandbox.v1.PortRange:
      description: PortRange is a protocol plus a single port or contiguous port range.
      type: object
      properties:
        protocol:
          description: TCP (default), UDP, or SCTP.
          type: string
        port:
          type: integer
          format: int32
        endPort:
          description: >-
            Inclusive end of a contiguous range; unset or equal to port = single
            port.
          type: integer
          format: int32
      required:
        - port
    coreweave.sandbox.v1.SelectorBlock:
      description: |-
        SelectorBlock selects cluster workloads by label, mirroring Kubernetes
         NetworkPolicyPeer semantics. Matching is matchLabels-only (every listed
         label must be present with the exact value); expression matching is not
         part of the contract. Adding a label narrows the match, so containment is
         per dimension: a policy selector entitlement covers a declared selector
         when the declared pod_labels carry every entitled pod label (and then
         some) AND the namespace dimensions agree in form — both absent (own
         namespace), or both present with the declared namespace_labels carrying
         every entitled namespace label. An own-namespace entitlement never covers
         a cross-namespace declaration, and vice versa: the sandbox's own namespace
         is not statically comparable to any labeled namespace set.
      type: object
      properties:
        podLabels:
          description: >-
            Labels the destination pods must carry. At least one is required —
            an
             empty pod selector would select everything, which is `any`'s job.
          type: object
          additionalProperties:
            type: string
        namespaceLabels:
          description: |-
            Labels the destination pods' namespaces must carry. Absent = the
             sandbox's own namespace ONLY (Kubernetes NetworkPolicyPeer behavior);
             reaching workloads in other namespaces always requires namespace labels.
             There is deliberately no all-namespaces form.
          type: object
          additionalProperties:
            type: string
      required:
        - podLabels
    coreweave.sandbox.v1.SecretMapping:
      description: >-
        SecretMapping maps one secret (optionally a sub-field of a structured
        secret)
         in the store to an environment variable.
      type: object
      properties:
        path:
          description: >-
            Provider-specific secret identifier (a key or path within the
            store).
          type: string
        field:
          description: >-
            Optional sub-field within a structured secret; omit for a scalar
            secret.
          type: string
        envVar:
          description: Target environment variable.
          type: string
      required:
        - path
        - envVar
    coreweave.sandbox.v1.SecretSource:
      description: |-
        SecretSource addresses one provider secret value without specifying any
         delivery target such as an environment variable.
      type: object
      properties:
        storeName:
          description: >-
            Name of a secret store, matching SecretStoreReference.store_name.
            W&B-
             authenticated callers may use the built-in identity-backed store name
             "wandb"; all other names are resolved from configured SecretStores.
          type: string
        path:
          description: Provider-specific secret identifier, matching SecretMapping.path.
          type: string
        field:
          description: >-
            Optional sub-field within a structured secret, matching
            SecretMapping.field.
          type: string
      required:
        - storeName
        - path
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
      description: CoreWeave API access token sent as a bearer token.
      x-default: Bearer {API_ACCESS_TOKEN}

````
