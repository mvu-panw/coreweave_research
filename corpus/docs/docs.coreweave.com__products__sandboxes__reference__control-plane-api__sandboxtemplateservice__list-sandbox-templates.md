# List sandbox templates

Source: https://docs.coreweave.com/products/sandboxes/reference/control-plane-api/sandboxtemplateservice/list-sandbox-templates

# List sandbox templates

> List the sandbox templates in the caller's organization.



## OpenAPI

````yaml /openapi/sandboxes/openapi.yaml get /v1/sandboxTemplates
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
  /v1/sandboxTemplates:
    get:
      tags:
        - SandboxTemplateService
      summary: List sandbox templates
      description: >-
        ListSandboxTemplates lists templates in the caller's tenant
        organization.
         Soft-deleted rows are omitted unless show_deleted is set (admin only).
      operationId: SandboxTemplateService_ListSandboxTemplates
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
        - name: showDeleted
          in: query
          description: |-
            When true, include soft-deleted templates. Requires sandbox_admin.
             Default false.
          schema:
            type: boolean
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: >-
                  #/components/schemas/coreweave.sandbox.v1.ListSandboxTemplatesResponse
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/google.rpc.Status'
      servers:
        - url: https://api.coreweave.com
          description: CoreWeave control plane.
components:
  schemas:
    coreweave.sandbox.v1.ListSandboxTemplatesResponse:
      type: object
      properties:
        sandboxTemplates:
          type: array
          items:
            $ref: '#/components/schemas/coreweave.sandbox.v1.SandboxTemplate'
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
    coreweave.sandbox.v1.SandboxTemplate:
      description: |-
        SandboxTemplate is an organization-scoped partial workload template.
         PartialSandboxSpec / PartialContainer are defined in sandbox.proto.
      type: object
      properties:
        sandboxTemplateId:
          description: Server-assigned unique identifier.
          type: string
          readOnly: true
        displayName:
          description: >-
            Human-readable name, unique among active (non-deleted) templates in
            the
             tenant organization. Trimmed; 1–128 Unicode characters; must not be
             empty. Prefer names that are not UUID-shaped so they do not collide with
             id-first Get resolution.
          type: string
        spec:
          description: |-
            Partial workload specification. May omit fields that
             CreateSandboxFromTemplate supplies via overrides (for example containers).
             Must not carry policy selectors. Server-enforced size ceiling: 1 MiB.
          allOf:
            - $ref: '#/components/schemas/coreweave.sandbox.v1.PartialSandboxSpec'
        revision:
          description: |-
            Monotonic revision; incremented on each successful update.
             CreateSandboxFromTemplate records the selected revision on the sandbox as
             source_template_revision.
          type: string
          readOnly: true
        createTime:
          type: string
          format: date-time
          readOnly: true
        updateTime:
          type: string
          format: date-time
          readOnly: true
        deleteTime:
          description: Set when soft-deleted; unset for active templates.
          type: string
          format: date-time
          readOnly: true
        createUserId:
          description: User id of the creator.
          type: string
          readOnly: true
        deleted:
          description: True when delete_time is set. Convenience for admin filtering.
          type: boolean
          readOnly: true
        attachments:
          description: >-
            Optional admin runtime attachments applied when creating a sandbox
            from
             this template. Same opaque fragment shape as Policy.base (for example, a
             PodSpec fragment on a Kubernetes runner). Writable by sandbox_admin only.
             When set, CreateSandboxFromTemplate requires SANDBOX_MODE_CKS (serverless
             is rejected; unset mode is treated as CKS). Not part of SandboxSpec;
             CreateSandbox and create overrides cannot supply or change them.
          type: object
        requiresCks:
          description: >-
            True when attachments are set. Indicates CreateSandboxFromTemplate
            for
             this template requires CKS placement.
          type: boolean
          readOnly: true
      required:
        - displayName
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
    coreweave.sandbox.v1.PartialSandboxSpec:
      description: >-
        Partial specification for SandboxTemplate.spec and
        CreateSandboxFromTemplateRequest.overrides. Templates and overrides
        together must produce a valid sandbox specification. In JSON overrides,
        a present message replaces the whole message, a present map replaces the
        whole map, and a non-empty list replaces the whole list. An empty JSON
        list preserves the template list; it cannot clear inherited entries.
        Nonzero scalars and nonempty strings replace template values; zero or
        empty values preserve them. A containers override replaces the entire
        list and must supply complete, valid containers. runtimeClass and
        runtimeClassSelection form one runtime selection: setting either
        replaces both, and an explicitly present RUNTIME_CLASS_UNSPECIFIED
        clears the template selection.
      type: object
      properties:
        containers:
          description: >-
            Optional on templates. CreateSandboxFromTemplate requires at least
            one
             container on the resolved sandbox after overrides are applied.
          type: array
          items:
            $ref: '#/components/schemas/coreweave.sandbox.v1.PartialContainer'
        volumes:
          type: array
          items:
            $ref: '#/components/schemas/coreweave.sandbox.v1.SandboxVolume'
        services:
          type: array
          items:
            $ref: '#/components/schemas/coreweave.sandbox.v1.Service'
        maxLifetimeSeconds:
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
          $ref: '#/components/schemas/coreweave.sandbox.v1.ObjectStorageAccess'
        tags:
          type: array
          items:
            type: string
        runnerIds:
          type: array
          items:
            type: string
        network:
          $ref: '#/components/schemas/coreweave.sandbox.v1.NetworkOptions'
        annotations:
          type: object
          additionalProperties:
            type: string
        instanceType:
          type: string
        mode:
          description: >-
            Placement override. Omitted or SANDBOX_MODE_UNSPECIFIED preserves
            the template's mode. If the merged mode remains unspecified,
            non-empty template attachments select SANDBOX_MODE_CKS; otherwise,
            placement defaults to SANDBOX_MODE_SERVERLESS.
          type: string
          format: enum
          enum:
            - SANDBOX_MODE_UNSPECIFIED
            - SANDBOX_MODE_SERVERLESS
            - SANDBOX_MODE_CKS
        runtimeClass:
          type: string
        networkConfigId:
          description: >-
            Set only in CreateSandboxFromTemplate overrides to bind an unused
            caller-created NetworkConfig. Do not also set overrides.network. A
            stored SandboxTemplate cannot set networkConfigId; keep reusable
            rules in its network field instead.
          type: string
        runtimeClassSelection:
          description: >-
            Portable runtime selection override. If neither runtimeClass nor
            runtimeClassSelection is supplied, the template's runtime selection
            is preserved. Explicit RUNTIME_CLASS_UNSPECIFIED clears both the
            template's concrete and portable runtime selections and returns to
            automatic selection. Automatic selection uses the CPU or GPU default
            class on runners with runtime mappings; other runners retain their
            runtime-class default behavior. See
            SandboxSpec.runtimeClassSelection for placement and validation
            rules.
          type: string
          format: enum
          enum:
            - RUNTIME_CLASS_UNSPECIFIED
            - RUNTIME_CLASS_CPU_DEFAULT
            - RUNTIME_CLASS_CPU_NESTED_VIRT
            - RUNTIME_CLASS_CPU_SNAPSHOT_RESTORE
            - RUNTIME_CLASS_GPU_DEFAULT
    coreweave.sandbox.v1.PartialContainer:
      description: >-
        Container fields for a partial stored template or a create-time
        container override. A stored template may omit image if create-time
        overrides supply a complete, valid containers list. A containers
        override replaces the entire list: entries are not merged with template
        containers and cannot inherit an omitted image or other container
        fields. Each replacement container must be complete and valid.
      type: object
      properties:
        name:
          type: string
        image:
          description: >-
            OCI image. Optional on templates and overlays; required on the
            sandbox
             after CreateSandboxFromTemplate merge completes.
          type: string
        command:
          type: string
        args:
          type: array
          items:
            type: string
        environmentVariables:
          type: object
          additionalProperties:
            type: string
        resources:
          $ref: '#/components/schemas/coreweave.sandbox.v1.Resources'
        files:
          type: array
          items:
            $ref: '#/components/schemas/coreweave.sandbox.v1.FileMount'
        volumeMounts:
          type: array
          items:
            $ref: '#/components/schemas/coreweave.sandbox.v1.VolumeMount'
        secretStores:
          description: |-
            Same meaning as Container.secret_stores: resolved values inject into
             this container only.
          type: array
          items:
            $ref: '#/components/schemas/coreweave.sandbox.v1.SecretStoreReference'
        workingDir:
          type: string
        resourceRequirements:
          $ref: '#/components/schemas/coreweave.sandbox.v1.ResourceRequirements'
        securityContext:
          $ref: '#/components/schemas/coreweave.sandbox.v1.SecurityContext'
        imagePullCredentials:
          description: |-
            Request-scoped image pull credentials for this container's image.
             Same type and required inner fields as Container.image_pull_credentials.
             When this message is present on a template, registry must be a lowercase
             host or host:port, and credentials (store_name, path) must be set.
             Image/registry match and secret resolution run when the sandbox is created.
          allOf:
            - $ref: '#/components/schemas/coreweave.sandbox.v1.ImagePullCredentials'
        primary:
          description: Same meaning and field number as Container.primary.
          type: boolean
        startupProbe:
          description: Same meaning and field number as Container.startup_probe.
          allOf:
            - $ref: '#/components/schemas/coreweave.sandbox.v1.Probe'
      required:
        - name
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
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
      description: CoreWeave API access token sent as a bearer token.
      x-default: Bearer {API_ACCESS_TOKEN}

````
