# Get managed runner

Source: https://docs.coreweave.com/products/sandboxes/reference/control-plane-api/runnermanagementservice/get-managed-runner

# Get managed runner

> Get a managed runner by runner ID.



## OpenAPI

````yaml /openapi/sandboxes/openapi.yaml get /v1/sandbox/managedRunners/{runnerId}
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
  /v1/sandbox/managedRunners/{runnerId}:
    get:
      tags:
        - RunnerManagementService
      summary: Get managed runner
      description: GetManagedRunner returns a managed runner by runner_id.
      operationId: SandboxV1RunnerManagementService_GetManagedRunner
      parameters:
        - name: runnerId
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
                $ref: '#/components/schemas/coreweave.sandbox.v1.ManagedRunner'
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
    coreweave.sandbox.v1.ManagedRunner:
      description: ManagedRunner is an admin-owned runner deployment.
      type: object
      properties:
        identity:
          description: >-
            Core runner identity. Required on create; immutable identity fields
            cannot
             be changed afterward.
          allOf:
            - $ref: '#/components/schemas/coreweave.sandbox.v1.RunnerIdentity'
        displayName:
          description: Human-readable name for the runner, at most 256 characters.
          type: string
        spec:
          description: Desired managed-runner configuration.
          allOf:
            - $ref: '#/components/schemas/coreweave.sandbox.v1.ManagedRunnerSpec'
        installStatus:
          description: >-
            Current installation status. RUNNER_INSTALL_STATUS_UNSPECIFIED means
            no installation status is specified.
          type: string
          format: enum
          enum:
            - RUNNER_INSTALL_STATUS_UNSPECIFIED
            - RUNNER_INSTALL_STATUS_PENDING
            - RUNNER_INSTALL_STATUS_PROVISIONING
            - RUNNER_INSTALL_STATUS_READY
            - RUNNER_INSTALL_STATUS_FAILED
            - RUNNER_INSTALL_STATUS_DELETING
          readOnly: true
        connectionStatus:
          description: >-
            Live connection status. RUNNER_CONNECTION_STATUS_UNSPECIFIED means
            no connection status is specified.
          type: string
          format: enum
          enum:
            - RUNNER_CONNECTION_STATUS_UNSPECIFIED
            - RUNNER_CONNECTION_STATUS_CONNECTED
            - RUNNER_CONNECTION_STATUS_DISCONNECTED
          readOnly: true
        activeConfigVersion:
          description: Active configuration version running on the runner.
          type: string
          readOnly: true
        activeProfileSpecVersion:
          description: Active profile spec version running on the runner.
          type: string
          readOnly: true
        activeRevision:
          description: Active revision number currently running on the runner.
          type: integer
          format: int32
          readOnly: true
        targetRevision:
          description: Target revision number that should be rolled out.
          type: integer
          format: int32
          readOnly: true
        deploymentSpec:
          description: Resolved deployment spec for the runner.
          allOf:
            - $ref: '#/components/schemas/coreweave.sandbox.v1.RunnerDeploymentSpec'
          readOnly: true
        updateAvailable:
          description: Whether an update is available on this runner's release channel.
          type: boolean
          readOnly: true
        createTime:
          type: string
          format: date-time
          readOnly: true
        updateTime:
          type: string
          format: date-time
          readOnly: true
        lastHeartbeatTime:
          type: string
          format: date-time
          readOnly: true
        profileBindings:
          description: |-
            Legacy profile bindings. Not accepted by v1 managed-runner writes;
             configure policy instead.
          type: array
          items:
            $ref: '#/components/schemas/coreweave.sandbox.v1.RunnerProfileBinding'
        installError:
          description: Populated when install_status == FAILED.
          allOf:
            - $ref: '#/components/schemas/coreweave.sandbox.v1.RunnerInstallError'
          readOnly: true
        rolloutInProgress:
          description: True when target_revision is newer than active_revision.
          type: boolean
          readOnly: true
        policy:
          description: >-
            The policy governing sandboxes on this runner. v1 managed-runner
            creation requires an explicit policy. An empty policy supplies no
            base defaults or explicit constraints. Platform safety gates still
            apply, and an absent runtime-class allowlist permits no concrete
            runtimeClass pin.
          allOf:
            - $ref: '#/components/schemas/coreweave.sandbox.v1.Policy'
        etag:
          description: >-
            Opaque revision token for policy updates. Clients must send the
            value
             returned by GetManagedRunner when updating policy. A stale value causes
             FAILED_PRECONDITION and no mutation is applied.
          type: string
        dataPlaneStatus:
          description: Observed direct data-plane endpoint state.
          allOf:
            - $ref: '#/components/schemas/coreweave.sandbox.v1.RunnerDataPlaneStatus'
          readOnly: true
      required:
        - identity
        - policy
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
    coreweave.sandbox.v1.RunnerIdentity:
      description: RunnerIdentity contains stable runner identity fields.
      type: object
      properties:
        runnerId:
          description: Operator-assigned runner identifier, unique within the organization.
          type: string
        runnerGroupId:
          description: Runner group ID for scheduling affinity.
          type: string
        zone:
          description: Geographic zone. Immutable after create.
          type: string
        clusterId:
          description: Cluster UUID. Immutable after create.
          type: string
        clusterName:
          description: Cluster display name resolved by the server.
          type: string
          readOnly: true
    coreweave.sandbox.v1.ManagedRunnerSpec:
      description: >-
        ManagedRunnerSpec contains configuration specific to platform-managed
        runners.
      type: object
      properties:
        releaseChannel:
          description: >-
            Release channel for automatic updates. Omit this field to use
            RELEASE_CHANNEL_STABLE on create or whole-spec replacement.
            RELEASE_CHANNEL_UNSPECIFIED also defaults to RELEASE_CHANNEL_STABLE
            in those cases. An update that selects only spec.releaseChannel
            requires a concrete channel.
          type: string
          format: enum
          enum:
            - RELEASE_CHANNEL_UNSPECIFIED
            - RELEASE_CHANNEL_STABLE
            - RELEASE_CHANNEL_RAPID
        maintenancePolicy:
          description: Maintenance policy for update scheduling.
          allOf:
            - $ref: '#/components/schemas/coreweave.sandbox.v1.MaintenancePolicy'
        overrides:
          description: Customer-settable deployment overrides.
          allOf:
            - $ref: >-
                #/components/schemas/coreweave.sandbox.v1.RunnerDeploymentOverrides
        allowPrivilegedProfileAnnotations:
          description: Legacy profile setting. Not accepted by v1 managed-runner writes.
          type: boolean
        enforceResourceLimits:
          description: >-
            Requires sandboxes and bound profile templates to declare both
            memory and
             CPU limits.
          type: boolean
        volumes:
          description: |-
            Registered-Volume (PVC) support for this runner. When present, this
             typed toggle is authoritative over any ENABLE_VOLUMES /
             VOLUME_DRIVER_ALLOWLIST entries in deployment env.
          allOf:
            - $ref: '#/components/schemas/coreweave.sandbox.v1.RunnerVolumesConfig'
        tenantMetrics:
          description: |-
            Tenant-metrics collector for this runner's cluster. When present,
             authoritative over the equivalent deployment-env entries; when absent,
             env passthrough applies.
          allOf:
            - $ref: >-
                #/components/schemas/coreweave.sandbox.v1.RunnerTenantMetricsConfig
        dataPlane:
          description: >-
            Direct sandbox data-plane endpoint configuration. Unset uses the
            platform
             default; the disabled exposure keeps all data operations on the Gateway.
          allOf:
            - $ref: '#/components/schemas/coreweave.sandbox.v1.RunnerDataPlaneConfig'
        imagePull:
          description: >-
            Image pull behavior for sandbox workload containers on this runner.
            When
             present, this typed setting is authoritative over any equivalent
             deployment env entry; when absent, the platform default applies.
          allOf:
            - $ref: '#/components/schemas/coreweave.sandbox.v1.RunnerImagePullConfig'
    coreweave.sandbox.v1.RunnerDeploymentSpec:
      description: RunnerDeploymentSpec is the resolved runner deployment specification.
      type: object
      properties:
        image:
          type: string
          readOnly: true
        env:
          type: object
          additionalProperties:
            type: string
          readOnly: true
        args:
          type: array
          items:
            type: string
          readOnly: true
        resources:
          allOf:
            - $ref: >-
                #/components/schemas/coreweave.sandbox.v1.RunnerResourceRequirements
          readOnly: true
        nodeSelector:
          type: object
          additionalProperties:
            type: string
          readOnly: true
        tolerations:
          type: array
          items:
            $ref: '#/components/schemas/coreweave.sandbox.v1.RunnerToleration'
          readOnly: true
        scaling:
          allOf:
            - $ref: '#/components/schemas/coreweave.sandbox.v1.RunnerScalingConfig'
          readOnly: true
        annotations:
          type: object
          additionalProperties:
            type: string
          readOnly: true
        labels:
          type: object
          additionalProperties:
            type: string
          readOnly: true
        serviceAccount:
          type: string
          readOnly: true
        extraVolumes:
          type: array
          items:
            $ref: '#/components/schemas/coreweave.sandbox.v1.RunnerVolumeMount'
          readOnly: true
        readinessProbe:
          allOf:
            - $ref: '#/components/schemas/coreweave.sandbox.v1.RunnerProbeConfig'
          readOnly: true
        livenessProbe:
          allOf:
            - $ref: '#/components/schemas/coreweave.sandbox.v1.RunnerProbeConfig'
          readOnly: true
        initResources:
          allOf:
            - $ref: >-
                #/components/schemas/coreweave.sandbox.v1.RunnerResourceRequirements
          readOnly: true
        imagePullPolicy:
          type: string
          readOnly: true
        gatewayServer:
          type: string
          readOnly: true
        cpuRuntimeClass:
          type: string
          readOnly: true
        gpuRuntimeClass:
          type: string
          readOnly: true
        endpointRoutes:
          description: |-
            Platform-owned product endpoint-route configuration. OUTPUT_ONLY for
             customers; configured via platform deployment defaults / version specs.
          allOf:
            - $ref: '#/components/schemas/coreweave.sandbox.v1.RunnerEndpointRoutes'
          readOnly: true
        dataPlane:
          description: Resolved direct data-plane endpoint configuration.
          allOf:
            - $ref: '#/components/schemas/coreweave.sandbox.v1.RunnerDataPlaneConfig'
          readOnly: true
        affinity:
          description: Resolved Kubernetes Affinity object for runner pods only.
          type: object
          readOnly: true
    coreweave.sandbox.v1.RunnerProfileBinding:
      description: >-
        RunnerProfileBinding associates a profile template with a managed
        runner.
      type: object
      properties:
        runnerProfileBindingId:
          description: Server-assigned binding identifier.
          type: string
          readOnly: true
        profileTemplateId:
          description: Profile template id to bind.
          type: string
        profileName:
          description: >-
            Profile name advertised on this runner. Defaults to the template
            display name.
          type: string
        isDefault:
          description: Whether this is the runner's default profile.
          type: boolean
        overrides:
          description: Per-binding profile overrides.
          allOf:
            - $ref: '#/components/schemas/coreweave.sandbox.v1.ProfileSpec'
        createTime:
          type: string
          format: date-time
          readOnly: true
        updateTime:
          type: string
          format: date-time
          readOnly: true
      required:
        - profileTemplateId
    coreweave.sandbox.v1.RunnerInstallError:
      description: >-
        RunnerInstallError is structured failure detail for failed runner
        installs.
      type: object
      properties:
        reason:
          description: >-
            Installation failure reason.
            RUNNER_INSTALL_FAILURE_REASON_UNSPECIFIED means no specific failure
            reason is reported.
          type: string
          format: enum
          enum:
            - RUNNER_INSTALL_FAILURE_REASON_UNSPECIFIED
            - RUNNER_INSTALL_FAILURE_REASON_NO_SCHEDULABLE_NODES
            - RUNNER_INSTALL_FAILURE_REASON_TAINT_TOLERATION_MISMATCH
            - RUNNER_INSTALL_FAILURE_REASON_NODE_SELECTOR_NO_MATCH
            - RUNNER_INSTALL_FAILURE_REASON_INSUFFICIENT_RESOURCES
            - RUNNER_INSTALL_FAILURE_REASON_IMAGE_PULL_FAILED
            - RUNNER_INSTALL_FAILURE_REASON_CLUSTER_NOT_READY
            - RUNNER_INSTALL_FAILURE_REASON_QUOTA_EXCEEDED
            - RUNNER_INSTALL_FAILURE_REASON_ROLLOUT_TIMED_OUT
            - RUNNER_INSTALL_FAILURE_REASON_INTERNAL_ERROR
            - RUNNER_INSTALL_FAILURE_REASON_CLUSTER_ACCESS_FAILED
            - RUNNER_INSTALL_FAILURE_REASON_GATEWAY_UNREACHABLE
            - RUNNER_INSTALL_FAILURE_REASON_JOIN_TOKEN_FAILED
            - RUNNER_INSTALL_FAILURE_REASON_RUNNER_OFFLINE
            - RUNNER_INSTALL_FAILURE_REASON_CERT_EXPIRED
            - RUNNER_INSTALL_FAILURE_REASON_CLUSTER_NODES_UNHEALTHY
          readOnly: true
        message:
          type: string
          readOnly: true
        diagnosticDetail:
          type: string
          readOnly: true
        remediationHints:
          type: array
          items:
            type: string
          readOnly: true
        occurredTime:
          type: string
          format: date-time
          readOnly: true
    coreweave.sandbox.v1.Policy:
      description: >-
        Policy governs sandboxes on its runner. Resolution applies runtime
        defaults, then policy base, then the sandbox spec. The sandbox spec
        takes precedence for scalar defaults; policy attachments still apply,
        and administrator-pinned Pod metadata takes precedence when annotation
        keys overlap. Constraints validate the fully resolved spec and reject
        violations rather than silently rewriting values. An empty policy
        supplies no base defaults or explicit constraints, but platform safety
        gates and runtime-class restrictions still apply. An absent
        allowedRuntimeClasses list permits no concrete runtimeClass pin. v1
        managed-runner creation requires an explicit policy.
      type: object
      properties:
        displayName:
          description: Human-readable name for this policy posture.
          type: string
        base:
          description: >-
            Admin attachments and runtime defaults applied to every sandbox on
            the
             runner. Opaque: its schema is determined by the runner's runtime (for
             example, a PodSpec fragment on a Kubernetes runner). Not a second home for
             security, lifetime, or other typed constraint concerns — those live under
             constraints.
          type: object
        constraints:
          description: Typed clamps validated against the resolved sandbox spec.
          allOf:
            - $ref: '#/components/schemas/coreweave.sandbox.v1.PolicyConstraints'
        controlPlaneAccess:
          description: >-
            Request-time controls for Sandbox API operations targeting this
            runner.
             These controls supplement authentication and tenant authorization; they
             do not restrict traffic sent directly to services exposed by a Sandbox.
          allOf:
            - $ref: >-
                #/components/schemas/coreweave.sandbox.v1.ControlPlaneAccessPolicy
    coreweave.sandbox.v1.RunnerDataPlaneStatus:
      description: |-
        RunnerDataPlaneStatus reports the endpoint observed across the logical
         Runner's accepting shards.
      type: object
      properties:
        state:
          description: >-
            Reported endpoint state. RUNNER_DATA_PLANE_STATE_UNSPECIFIED means
            no endpoint state is specified.
          type: string
          format: enum
          enum:
            - RUNNER_DATA_PLANE_STATE_UNSPECIFIED
            - RUNNER_DATA_PLANE_STATE_DISABLED
            - RUNNER_DATA_PLANE_STATE_PENDING
            - RUNNER_DATA_PLANE_STATE_READY
            - RUNNER_DATA_PLANE_STATE_NOT_READY
          readOnly: true
        endpointId:
          type: string
          readOnly: true
        advertisedUri:
          type: string
          readOnly: true
        protocols:
          type: array
          items:
            type: string
          readOnly: true
        serverCertificateExpiresAt:
          type: string
          format: date-time
          readOnly: true
        message:
          type: string
          readOnly: true
        lastTransitionTime:
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
    coreweave.sandbox.v1.MaintenancePolicy:
      description: >-
        MaintenancePolicy controls when updates can be applied to managed
        runners.
      type: object
      properties:
        windows:
          type: array
          items:
            $ref: '#/components/schemas/coreweave.sandbox.v1.MaintenanceWindow'
        exclusions:
          type: array
          items:
            $ref: '#/components/schemas/coreweave.sandbox.v1.MaintenanceExclusion'
    coreweave.sandbox.v1.RunnerDeploymentOverrides:
      description: >-
        RunnerDeploymentOverrides contains customer-settable runner deployment
        overrides.
      type: object
      properties:
        nodeSelector:
          type: object
          additionalProperties:
            type: string
        tolerations:
          type: array
          items:
            $ref: '#/components/schemas/coreweave.sandbox.v1.RunnerToleration'
        resources:
          $ref: '#/components/schemas/coreweave.sandbox.v1.RunnerResourceRequirements'
        annotations:
          type: object
          additionalProperties:
            type: string
        labels:
          type: object
          additionalProperties:
            type: string
        env:
          type: object
          additionalProperties:
            type: string
        args:
          type: array
          items:
            type: string
        scaling:
          $ref: '#/components/schemas/coreweave.sandbox.v1.RunnerScalingConfig'
        cpuRuntimeClass:
          type: string
        gpuRuntimeClass:
          type: string
        affinity:
          description: >-
            Kubernetes Affinity object for runner pods only, using Kubernetes
            JSON
             field names. Supports node affinity, pod affinity, and pod anti-affinity.
             Replaces inherited affinity as a whole; an empty object clears it.
          type: object
    coreweave.sandbox.v1.RunnerVolumesConfig:
      description: |-
        RunnerVolumesConfig toggles registered-Volume (PVC) mounts on a managed
         runner. Enabling is necessary but not sufficient: the runner advertises
         volume support only after its startup PVC/PV RBAC preflight passes.
      type: object
      properties:
        enabled:
          description: Enable registered-Volume mounts on this runner.
          type: boolean
        csiDriverAllowlist:
          description: >-
            CSI drivers allowed to back registered Volumes on this runner. Empty
            =
             the platform default allowlist (csi.vastdata.com).
          type: array
          items:
            type: string
    coreweave.sandbox.v1.RunnerTenantMetricsConfig:
      description: |-
        RunnerTenantMetricsConfig toggles the tenant-metrics collector on a
         managed runner's cluster (per-sandbox usage metrics attributed to the
         tenant org).
      type: object
      properties:
        enabled:
          description: Enable the tenant-metrics collector for this runner's cluster.
          type: boolean
        image:
          description: >-
            Collector image, release-pinned. When empty, an image already
            present
             in the deployment env applies.
          type: string
    coreweave.sandbox.v1.RunnerDataPlaneConfig:
      description: |-
        RunnerDataPlaneConfig controls the dedicated Runner endpoint for direct
         sandbox data operations. The platform issues and rotates the endpoint's
         server certificate; this configuration contains no certificate source or
         private key material.
      type: object
      properties:
        disabled:
          $ref: >-
            #/components/schemas/coreweave.sandbox.v1.RunnerDataPlaneDisabledConfig
        clusterIp:
          $ref: >-
            #/components/schemas/coreweave.sandbox.v1.RunnerDataPlaneClusterIPConfig
        loadBalancer:
          $ref: >-
            #/components/schemas/coreweave.sandbox.v1.RunnerDataPlaneLoadBalancerConfig
        custom:
          $ref: >-
            #/components/schemas/coreweave.sandbox.v1.RunnerDataPlaneCustomConfig
    coreweave.sandbox.v1.RunnerImagePullConfig:
      description: |-
        RunnerImagePullConfig sets the image pull behavior for sandbox workload
         containers scheduled on a managed runner. Platform-owned helper containers
         keep their own pull behavior and are unaffected.
      type: object
      properties:
        policy:
          description: >-
            Pull policy applied to every sandbox workload container on this
            runner. Defaults to IF_NOT_PRESENT. Omit this field for the default;
            SANDBOX_IMAGE_PULL_POLICY_UNSPECIFIED also uses
            SANDBOX_IMAGE_PULL_POLICY_IF_NOT_PRESENT.
          type: string
          format: enum
          enum:
            - SANDBOX_IMAGE_PULL_POLICY_UNSPECIFIED
            - SANDBOX_IMAGE_PULL_POLICY_IF_NOT_PRESENT
            - SANDBOX_IMAGE_PULL_POLICY_ALWAYS
    coreweave.sandbox.v1.RunnerResourceRequirements:
      description: RunnerResourceRequirements defines CPU and memory requests/limits.
      type: object
      properties:
        cpuRequest:
          type: string
        memoryRequest:
          type: string
        cpuLimit:
          type: string
        memoryLimit:
          type: string
    coreweave.sandbox.v1.RunnerToleration:
      description: RunnerToleration defines a Kubernetes toleration.
      type: object
      properties:
        key:
          type: string
        operator:
          type: string
        value:
          type: string
        effect:
          type: string
    coreweave.sandbox.v1.RunnerScalingConfig:
      description: RunnerScalingConfig defines runner deployment scaling.
      type: object
      properties:
        replicas:
          type: integer
          format: int32
        autoscalingEnabled:
          type: boolean
        minReplicas:
          type: integer
          format: int32
        maxReplicas:
          type: integer
          format: int32
    coreweave.sandbox.v1.RunnerVolumeMount:
      description: RunnerVolumeMount defines an extra volume mount for a runner pod.
      type: object
      properties:
        mountPath:
          type: string
        name:
          type: string
        readOnly:
          type: boolean
        subPath:
          type: string
        configMapName:
          type: string
        secretName:
          type: string
        emptyDir:
          type: boolean
    coreweave.sandbox.v1.RunnerProbeConfig:
      description: RunnerProbeConfig defines health probe configuration.
      type: object
      properties:
        path:
          type: string
        port:
          type: integer
          format: int32
        initialDelaySeconds:
          type: integer
          format: int32
        periodSeconds:
          type: integer
          format: int32
        failureThreshold:
          type: integer
          format: int32
        timeoutSeconds:
          type: integer
          format: int32
    coreweave.sandbox.v1.RunnerEndpointRoutes:
      description: >-
        RunnerEndpointRoutes is platform-owned product endpoint-route
        configuration.
         Slots are independent: HTTPS-only, TLS-only, or both.
      type: object
      properties:
        https:
          description: >-
            Product HTTPS endpoint route. provider is omitted, empty, or exact
            "envoy".
          allOf:
            - $ref: '#/components/schemas/coreweave.sandbox.v1.RunnerEndpointRoute'
          readOnly: true
        tlsPassthrough:
          description: |-
            SNI passthrough at the shared Gateway. Independent of https.
             provider is omitted or empty.
          allOf:
            - $ref: '#/components/schemas/coreweave.sandbox.v1.RunnerEndpointRoute'
          readOnly: true
    coreweave.sandbox.v1.ProfileSpec:
      description: >-
        ProfileSpec defines compute, placement, namespace, networking, and
        pod-template
         defaults for sandboxes scheduled through a profile.
      type: object
      properties:
        containerImage:
          description: Container image default.
          type: string
        runtimeClass:
          description: Runtime class name for sandbox isolation.
          type: string
        resourceDefaults:
          description: Resource defaults for sandboxes on this profile.
          allOf:
            - $ref: '#/components/schemas/coreweave.sandbox.v1.ResourceDefaults'
        instanceTypes:
          description: Node instance types this profile may schedule onto.
          type: array
          items:
            type: string
        nodeSelector:
          description: Node selector labels.
          type: object
          additionalProperties:
            type: string
        tags:
          description: Tags for RBAC-based access control.
          type: array
          items:
            type: string
        namespace:
          description: Namespace placement strategy.
          allOf:
            - $ref: '#/components/schemas/coreweave.sandbox.v1.ProfileNamespaceConfig'
        network:
          description: Network policy and exposure modes.
          allOf:
            - $ref: '#/components/schemas/coreweave.sandbox.v1.ProfileNetworkConfig'
        podTemplate:
          description: >-
            Admin-authored pod template fragment in the runner's PodConfig
            shape. This
             remains opaque because it contains Kubernetes-specific PodSpec fields.
          type: object
    coreweave.sandbox.v1.PolicyConstraints:
      description: >-
        Typed constraints a policy enforces. Each group is optional. Omitting a
        group adds no explicit constraints of that kind, but platform safety
        gates and runtime-class restrictions still apply. An empty or absent
        allowedRuntimeClasses list permits no concrete runtimeClass pin.
      type: object
      properties:
        resources:
          $ref: '#/components/schemas/coreweave.sandbox.v1.ResourceConstraints'
        image:
          $ref: '#/components/schemas/coreweave.sandbox.v1.ImageConstraints'
        network:
          $ref: '#/components/schemas/coreweave.sandbox.v1.NetworkConstraints'
        security:
          $ref: '#/components/schemas/coreweave.sandbox.v1.SecurityConstraints'
        instance:
          $ref: '#/components/schemas/coreweave.sandbox.v1.InstanceConstraints'
        lifecycle:
          $ref: '#/components/schemas/coreweave.sandbox.v1.LifecycleConstraints'
        metadata:
          $ref: '#/components/schemas/coreweave.sandbox.v1.MetadataConstraints'
        volumes:
          $ref: '#/components/schemas/coreweave.sandbox.v1.VolumeConstraints'
    coreweave.sandbox.v1.ControlPlaneAccessPolicy:
      description: >-
        ControlPlaneAccessPolicy limits which network origins may use Sandbox
        API
         operations that select this runner or target a Sandbox placed on it.
      type: object
      properties:
        sourceIpAllowlist:
          description: >-
            Allowed public client source ranges. An absent allowlist leaves
            access
             unrestricted. A present allowlist with no CIDRs denies every public
             source. Runner and platform lifecycle traffic is not governed by it.
          allOf:
            - $ref: '#/components/schemas/coreweave.sandbox.v1.SourceIpAllowlist'
    coreweave.sandbox.v1.MaintenanceWindow:
      description: |-
        MaintenanceWindow defines a recurring window during which updates may
         start. If any windows are configured, updates start only while one is
         open; exclusions override windows.
      type: object
      properties:
        cron:
          description: |-
            Standard 5-field cron expression for the window start (e.g.,
             "0 2 * * SAT" for Saturdays at 02:00), evaluated in UTC. Descriptor
             forms such as "@daily" or "@every 1h" are rejected, as are expressions
             that never fire.
          type: string
        durationSeconds:
          description: |-
            Duration of the window in seconds. Must be between 60 (1 minute) and
             604800 (7 days).
          type: integer
          format: int32
      required:
        - cron
        - durationSeconds
    coreweave.sandbox.v1.MaintenanceExclusion:
      description: |-
        MaintenanceExclusion defines a one-time period during which no updates
         start, overriding any open maintenance window.
      type: object
      properties:
        startTime:
          description: Start of the exclusion period (inclusive).
          type: string
          format: date-time
        endTime:
          description: End of the exclusion period (exclusive). Must be after start_time.
          type: string
          format: date-time
        reason:
          type: string
      required:
        - startTime
        - endTime
    coreweave.sandbox.v1.RunnerDataPlaneDisabledConfig:
      description: RunnerDataPlaneDisabledConfig explicitly disables the direct endpoint.
      type: object
      properties: {}
    coreweave.sandbox.v1.RunnerDataPlaneClusterIPConfig:
      description: >-
        RunnerDataPlaneClusterIPConfig exposes the direct endpoint through a
        stable
         ClusterIP Service. The platform derives its URI and server-certificate SANs.
      type: object
      properties:
        annotations:
          type: object
          additionalProperties:
            type: string
    coreweave.sandbox.v1.RunnerDataPlaneLoadBalancerConfig:
      description: |-
        RunnerDataPlaneLoadBalancerConfig exposes the direct endpoint through a
         stable L4 LoadBalancer Service. The Service forwards TCP to the Runner and
         does not terminate mutual TLS.
      type: object
      properties:
        scope:
          description: >-
            Reachability scope for the load balancer. Omit this field to use the
            public scope. RUNNER_DATA_PLANE_SERVICE_SCOPE_UNSPECIFIED uses the
            same scope as RUNNER_DATA_PLANE_SERVICE_SCOPE_PUBLIC. Private scope
            also requires a load balancer class or provider annotation.
          type: string
          format: enum
          enum:
            - RUNNER_DATA_PLANE_SERVICE_SCOPE_UNSPECIFIED
            - RUNNER_DATA_PLANE_SERVICE_SCOPE_PUBLIC
            - RUNNER_DATA_PLANE_SERVICE_SCOPE_PRIVATE
        loadBalancerClass:
          type: string
        annotations:
          type: object
          additionalProperties:
            type: string
        sourceRanges:
          type: array
          items:
            type: string
        externalTrafficPolicy:
          description: >-
            External traffic routing policy. Omit this field to use the cluster
            policy. RUNNER_DATA_PLANE_EXTERNAL_TRAFFIC_POLICY_UNSPECIFIED uses
            RUNNER_DATA_PLANE_EXTERNAL_TRAFFIC_POLICY_CLUSTER.
          type: string
          format: enum
          enum:
            - RUNNER_DATA_PLANE_EXTERNAL_TRAFFIC_POLICY_UNSPECIFIED
            - RUNNER_DATA_PLANE_EXTERNAL_TRAFFIC_POLICY_CLUSTER
            - RUNNER_DATA_PLANE_EXTERNAL_TRAFFIC_POLICY_LOCAL
        hostname:
          description: |-
            DNS name to publish for the endpoint and include in its server
             certificate. When empty, the platform may assign one.
          type: string
    coreweave.sandbox.v1.RunnerDataPlaneCustomConfig:
      description: >-
        RunnerDataPlaneCustomConfig advertises a customer-managed network path
        such
         as a VPC route, VPN, service mesh, or Tailscale address. The platform still
         issues the Runner's server certificate for the URI's authority.
      type: object
      properties:
        advertisedUri:
          description: Stable absolute URI returned to direct clients.
          type: string
        serviceAnnotations:
          description: >-
            Annotations applied to the backing ClusterIP Service for
            integrations that
             discover or route Kubernetes Services.
          type: object
          additionalProperties:
            type: string
      required:
        - advertisedUri
    coreweave.sandbox.v1.RunnerEndpointRoute:
      description: >-
        RunnerEndpointRoute configures one independently mergeable
        endpoint-route
         slot. enabled=true requires gateway; enabled=false clears an inherited slot
         and rejects gateway. provider accepted values depend on the parent slot.
      type: object
      properties:
        enabled:
          type: boolean
          readOnly: true
        gateway:
          allOf:
            - $ref: '#/components/schemas/coreweave.sandbox.v1.RunnerEndpointGateway'
          readOnly: true
        provider:
          description: |-
            Ingress extras for this slot. Accepted values are slot-dependent.
             OUTPUT_ONLY on the customer surface; configured via the platform
             managed-runner API.
          type: string
          readOnly: true
    coreweave.sandbox.v1.ResourceDefaults:
      description: >-
        ResourceDefaults defines default resource requests and limits for
        sandboxes.
      type: object
      properties:
        cpuRequest:
          type: string
        memoryRequest:
          type: string
        cpuLimit:
          type: string
        memoryLimit:
          type: string
    coreweave.sandbox.v1.ProfileNamespaceConfig:
      description: ProfileNamespaceConfig controls sandbox namespace placement.
      type: object
      properties:
        strategy:
          type: string
          format: enum
          enum:
            - PROFILE_NAMESPACE_STRATEGY_UNSPECIFIED
            - PROFILE_NAMESPACE_STRATEGY_STATIC
            - PROFILE_NAMESPACE_STRATEGY_PER_PROFILE
            - PROFILE_NAMESPACE_STRATEGY_PER_ORG
            - PROFILE_NAMESPACE_STRATEGY_PER_USER
        staticNamespace:
          type: string
        namespacePrefix:
          type: string
        autoCreate:
          description: Defaults to true when unset.
          type: boolean
        labels:
          type: object
          additionalProperties:
            type: string
        annotations:
          type: object
          additionalProperties:
            type: string
    coreweave.sandbox.v1.ProfileNetworkConfig:
      description: >-
        ProfileNetworkConfig controls sandbox network policy and service
        exposure.
      type: object
      properties:
        egress:
          $ref: '#/components/schemas/coreweave.sandbox.v1.ProfileNetworkEgressConfig'
        ingress:
          type: object
          additionalProperties:
            $ref: '#/components/schemas/coreweave.sandbox.v1.ProfileIngressModeConfig'
    coreweave.sandbox.v1.ResourceConstraints:
      description: >-
        ResourceConstraints bounds a container's compute. String quantities
        mirror
         Resources (e.g. "8", "500m", "32Gi").
      type: object
      properties:
        maxCpu:
          description: Per-container maxima.
          type: string
        maxMemory:
          type: string
        minCpu:
          description: Per-container minima.
          type: string
        minMemory:
          type: string
        defaultCpu:
          description: |-
            Per-container defaults applied when the spec leaves a value unset.
             When neither requests nor limits is declared, positive CPU and memory
             defaults also supply matching limits.
          type: string
        defaultMemory:
          type: string
        maxGpuCount:
          description: >-
            Maximum GPUs per container. Presence-aware: unset = no cap; an
            explicit 0
             bans GPU requests entirely (a GPU-free pool is expressible).
          type: string
        cpuCeiling:
          description: Sum-of-requests ceiling across the whole sandbox.
          type: string
        memoryCeiling:
          type: string
        requireLimits:
          description: >-
            Require every container to have requests and limits after
            defaulting.
          type: boolean
    coreweave.sandbox.v1.ImageConstraints:
      description: ImageConstraints restricts which images may run.
      type: object
      properties:
        allowedRegistries:
          description: Allowed registry prefixes (empty = any).
          type: array
          items:
            type: string
        allowedImages:
          description: Allowed image references (empty = any within allowed_registries).
          type: array
          items:
            type: string
    coreweave.sandbox.v1.NetworkConstraints:
      description: |-
        NetworkConstraints clamps the sandbox's declared network intent
         (SandboxSpec.network, using the EgressRule/IngressRule types from
         sandbox.proto) and bounds port visibility.
      type: object
      properties:
        allowedEgress:
          description: >-
            Allowed egress envelope, validated at create time. When non-empty,
            every
             declared egress rule must fit inside the union of these rules; a rule
             outside it is rejected, never silently narrowed. Carve-outs are expressed
             with CidrBlock.except (e.g. "everything but an internal range" is
             {cidr: 0.0.0.0/0, except: [10.8.0.0/16]}) and with https_hostname: "*" plus
             https_hostname_except. Excluding "evil.com" and "*.evil.com" removes the
             apex and one label under it, but leaves a.b.evil.com entitled.
             Containment is type-wise: a declared CIDR must fit the allowed CIDR space;
             an HTTPS hostname must match an allowed hostname pattern, minus that
             rule's https_hostname_except, or an `any` entitlement; a declared tenant
             scope must appear as an allowed scope; and declaring `any` requires an
             `any` entitlement. An `any` entitlement admits CIDR, tenant, HTTPS
             hostnames, and `any` — but never selectors: label-based
             selection of cluster workloads requires its own selector entitlement
             (see EgressRule.selector). Empty = any egress is declarable, selectors
             included.
          type: array
          items:
            $ref: '#/components/schemas/coreweave.sandbox.v1.EgressRule'
        defaultEgress:
          description: >-
            Egress applied when the spec declares none; entirely displaced by a
            spec
             that declares its own rules. Must fit the allowed envelope (validated when
             the policy is written). Must not carry https_hostname — a curated site set
             belongs on a SandboxTemplate, not the policy default.
          type: array
          items:
            $ref: '#/components/schemas/coreweave.sandbox.v1.EgressRule'
        denyHttpsHostnameRules:
          description: |-
            When true, rejects https_hostname rules in allowed_egress and
             SandboxSpec.network.egress. False permits those rules subject to
             allowed_egress. This controls permission to declare hostname-based HTTPS
             access; it does not block DNS queries or HTTPS allowed by CIDR rules. Use
             dns_egress to control outbound DNS traffic on UDP/TCP port 53.
          type: boolean
        allowedIngress:
          description: >-
            Allowed ingress envelope for CUSTOM-visibility ports, validated at
            create
             time with the same type-wise containment as allowed_egress. Empty = any
             ingress is declarable.
          type: array
          items:
            $ref: '#/components/schemas/coreweave.sandbox.v1.IngressRule'
        defaultIngress:
          description: >-
            Ingress applied when a CUSTOM-visibility port is declared and the
            spec
             declares no ingress rules; entirely displaced by a spec that declares its
             own. Must fit the allowed envelope (validated when the policy is written).
          type: array
          items:
            $ref: '#/components/schemas/coreweave.sandbox.v1.IngressRule'
        dnsEgress:
          description: >-
            Outbound DNS traffic ceiling, inherited by
            SandboxSpec.network.dns_egress.
             UNSPECIFIED defaults to ALLOW. ALLOW permits platform resolver access;
             a sandbox may choose DENY. DENY requires every sandbox to block outbound
             UDP/TCP destination port 53; an explicit sandbox ALLOW is rejected.
             This does not restrict which https_hostname rules may be declared;
             allowed_egress and deny_https_hostname_rules govern those rules.
          type: string
          format: enum
          enum:
            - DNS_EGRESS_MODE_UNSPECIFIED
            - DNS_EGRESS_MODE_ALLOW
            - DNS_EGRESS_MODE_DENY
    coreweave.sandbox.v1.SecurityConstraints:
      description: |-
        SecurityConstraints clamps in-guest container privilege and bounds the
         sandbox's isolation-boundary selection. Host-reaching settings default to
         forbidden and are only ever granted on a runner whose isolation contains
         them.
      type: object
      properties:
        allowPrivileged:
          description: Permit SecurityContext.privileged.
          type: boolean
        allowedCapabilities:
          description: >-
            Linux capabilities a container may add (empty = none beyond the
            default set).
          type: array
          items:
            type: string
        allowedSeccompProfiles:
          description: Permitted seccomp profiles (e.g. "RuntimeDefault", "Unconfined").
          type: array
          items:
            type: string
        allowedRuntimeClasses:
          description: >-
            Allowed SandboxSpec.runtime_class values. Like the capability and
            seccomp
             lists — and unlike the instance-type allow-list — an EMPTY (or absent)
             list permits NO pin: runtime-class selection is enabled by explicitly
             listing classes. Runtime class selects the isolation boundary itself, so
             it is fail-closed even under an otherwise-unset security group. The
             managed serverless pool lists only its Kata classes, keeping VM isolation
             mandatory there. Defaults below are policy-authored posture and apply
             regardless of this list.
          type: array
          items:
            type: string
        defaultCpuRuntimeClass:
          description: >-
            Default runtime class applied when SandboxSpec.runtime_class is
            unset and
             the sandbox requests no GPUs. Must fit allowed_runtime_classes when that
             list is non-empty (validated when the policy is written). Unset = the
             runner's configured runtime-class pair applies.
          type: string
        defaultGpuRuntimeClass:
          description: >-
            Default runtime class applied when SandboxSpec.runtime_class is
            unset and
             the sandbox requests GPUs. Same containment and fallback rules as the CPU
             default.
          type: string
        runtimeClassMappings:
          description: >-
            Bindings from portable runtime classes to concrete runtimes. A
            non-empty
             list switches the runner to runtime class mappings: a mapping permits its
             class for both SandboxSpec.runtime_class_selection and automatic CPU/GPU
             default selection, a class without a mapping is unavailable on this
             runner, and SandboxSpec.runtime_class pins are rejected. Omitting a
             default class disables automatic selection for that resource family.
             Mutually exclusive with allowed_runtime_classes, default_cpu_runtime_class,
             and default_gpu_runtime_class. Each class appears at most once. A
             node_default target is permitted only for the CPU and GPU defaults, and
             only serves SANDBOX_MODE_CKS placement outside the shared serverless pool.
          type: array
          items:
            $ref: '#/components/schemas/coreweave.sandbox.v1.RuntimeClassMapping'
    coreweave.sandbox.v1.InstanceConstraints:
      description: InstanceConstraints restricts node instance-type selection.
      type: object
      properties:
        allowedInstanceTypes:
          description: >-
            Allowed SandboxSpec.instance_type values (empty = any the runner
            offers).
          type: array
          items:
            type: string
    coreweave.sandbox.v1.LifecycleConstraints:
      description: >-
        LifecycleConstraints supplies sandbox lifetime defaults. Values above
        the
         platform maximum (currently 30 days) are rejected at create time; Policy
         only supplies a default when the create omits lifetime.
      type: object
      properties:
        defaultLifetimeSeconds:
          description: Default applied when SandboxSpec.max_lifetime_seconds is 0.
          type: integer
          format: int32
    coreweave.sandbox.v1.MetadataConstraints:
      description: MetadataConstraints clamps sandbox annotations.
      type: object
      properties:
        deniedAnnotationPrefixes:
          description: Annotation key prefixes that are rejected.
          type: array
          items:
            type: string
        maxAnnotationCount:
          description: Maximum number of annotations (0 = no limit).
          type: integer
          format: int32
    coreweave.sandbox.v1.VolumeConstraints:
      description: VolumeConstraints clamps sandbox volumes.
      type: object
      properties:
        allowedMedia:
          description: >-
            Permitted storage media. An empty list permits any medium; a
            non-empty list accepts only STORAGE_MEDIUM_DISK and
            STORAGE_MEDIUM_MEMORY. STORAGE_MEDIUM_UNSPECIFIED is invalid here
            and is not a wildcard. Excluding STORAGE_MEDIUM_MEMORY from a
            non-empty list forbids RAM-backed volumes.
          type: array
          items:
            enum:
              - STORAGE_MEDIUM_UNSPECIFIED
              - STORAGE_MEDIUM_DISK
              - STORAGE_MEDIUM_MEMORY
            type: string
            format: enum
        maxSize:
          description: Maximum size per volume (e.g. "100Gi").
          type: string
    coreweave.sandbox.v1.SourceIpAllowlist:
      description: SourceIpAllowlist is a bounded set of IPv4 and IPv6 network prefixes.
      type: object
      properties:
        cidrs:
          description: >-
            IPv4 or IPv6 CIDR prefixes. Prefixes are normalized when written. At
            most
             256 entries and 16 KiB of source text are accepted. Use 0.0.0.0/0 or
             ::/0 to explicitly allow every address in that family.
          type: array
          items:
            type: string
    coreweave.sandbox.v1.RunnerEndpointGateway:
      description: >-
        RunnerEndpointGateway identifies the shared parent Gateway a product
        route
         attaches to. DNS suffix is resolved from the Gateway Listener at create-path.
      type: object
      properties:
        name:
          type: string
          readOnly: true
        namespace:
          type: string
          readOnly: true
        listener:
          type: string
          readOnly: true
    coreweave.sandbox.v1.ProfileNetworkEgressConfig:
      description: ProfileNetworkEgressConfig defines named egress modes.
      type: object
      properties:
        defaultMode:
          description: Default egress mode name. Required when multiple modes are defined.
          type: string
        modes:
          description: Named egress modes.
          type: object
          additionalProperties:
            $ref: '#/components/schemas/coreweave.sandbox.v1.ProfileEgressModeConfig'
    coreweave.sandbox.v1.ProfileIngressModeConfig:
      description: ProfileIngressModeConfig defines one named ingress mode.
      type: object
      properties:
        service:
          $ref: '#/components/schemas/coreweave.sandbox.v1.ProfileServiceConfig'
        ingress:
          $ref: '#/components/schemas/coreweave.sandbox.v1.ProfileIngressConfig'
        route:
          $ref: '#/components/schemas/coreweave.sandbox.v1.ProfileRouteConfig'
        scope:
          type: string
          format: enum
          enum:
            - PROFILE_INGRESS_SCOPE_UNSPECIFIED
            - PROFILE_INGRESS_SCOPE_USER
            - PROFILE_INGRESS_SCOPE_ORG
            - PROFILE_INGRESS_SCOPE_PROFILE
            - PROFILE_INGRESS_SCOPE_ANY
        expectsExternalAddress:
          type: boolean
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
    coreweave.sandbox.v1.RuntimeClassMapping:
      description: >-
        RuntimeClassMapping binds a recognized, nonzero runtime class to an
        explicit
         execution target. Each runtime class can appear at most once in a catalog.
      type: object
      properties:
        runtimeClass:
          description: >-
            Required execution contract for this mapping. Specify a recognized
            nonzero runtime class. RUNTIME_CLASS_UNSPECIFIED is invalid in a
            mapping.
          type: string
          format: enum
          enum:
            - RUNTIME_CLASS_UNSPECIFIED
            - RUNTIME_CLASS_CPU_DEFAULT
            - RUNTIME_CLASS_CPU_NESTED_VIRT
            - RUNTIME_CLASS_CPU_SNAPSHOT_RESTORE
            - RUNTIME_CLASS_GPU_DEFAULT
        kubernetesRuntimeClassName:
          description: Nonempty Kubernetes RuntimeClass name.
          type: string
        nodeDefault:
          description: >-
            Use the node's default container runtime. Must be true and is
            permitted
             only for CPU_DEFAULT or GPU_DEFAULT in CKS placement.
          type: boolean
      required:
        - runtimeClass
    coreweave.sandbox.v1.ProfileEgressModeConfig:
      description: ProfileEgressModeConfig defines one named egress mode.
      type: object
      properties:
        type:
          type: string
          format: enum
          enum:
            - PROFILE_EGRESS_TYPE_UNSPECIFIED
            - PROFILE_EGRESS_TYPE_INTERNET
            - PROFILE_EGRESS_TYPE_USER
            - PROFILE_EGRESS_TYPE_ORG
            - PROFILE_EGRESS_TYPE_PROFILE
            - PROFILE_EGRESS_TYPE_ALLOWLIST
            - PROFILE_EGRESS_TYPE_NONE
        cidrs:
          type: array
          items:
            type: string
    coreweave.sandbox.v1.ProfileServiceConfig:
      description: ProfileServiceConfig defines Kubernetes Service exposure settings.
      type: object
      properties:
        serviceType:
          description: >-
            Kubernetes Service type, for example ClusterIP, NodePort, or
            LoadBalancer.
          type: string
        serviceSelectorAnnotation:
          $ref: '#/components/schemas/coreweave.sandbox.v1.AnnotationPair'
        dnsAnnotation:
          $ref: '#/components/schemas/coreweave.sandbox.v1.AnnotationPair'
    coreweave.sandbox.v1.ProfileIngressConfig:
      description: >-
        ProfileIngressConfig defines native Kubernetes Ingress exposure
        settings.
      type: object
      properties:
        controllerName:
          type: string
        template:
          type: string
    coreweave.sandbox.v1.ProfileRouteConfig:
      description: ProfileRouteConfig selects a pluggable exposure-route provider.
      type: object
      properties:
        provider:
          type: string
        hostnameTemplate:
          type: string
        config:
          type: object
          additionalProperties:
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
    coreweave.sandbox.v1.AnnotationPair:
      description: AnnotationPair is a Kubernetes annotation key/value pair.
      type: object
      properties:
        key:
          type: string
        value:
          type: string
      required:
        - key
        - value
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
      description: CoreWeave API access token sent as a bearer token.
      x-default: Bearer {API_ACCESS_TOKEN}

````
