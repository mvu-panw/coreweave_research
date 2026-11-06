# Create network configuration

Source: https://docs.coreweave.com/products/sandboxes/reference/control-plane-api/networkconfigservice/create-network-configuration

# Create network configuration

> Register desired network rules for a sandbox.



## OpenAPI

````yaml /openapi/sandboxes/openapi.yaml post /v1/networkConfigs
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
  /v1/networkConfigs:
    post:
      tags:
        - NetworkConfigService
      summary: Create network configuration
      description: >-
        Create an organization-scoped desired network configuration. Choose an
        ID matching ^[a-z][a-z0-9-]{2,62}$ without the reserved nc- prefix.
        Creation validates syntax; runner-policy constraints are checked when a
        sandbox binds the configuration. Requires the sandbox_user action.
      operationId: NetworkConfigService_CreateNetworkConfig
      parameters:
        - name: requestId
          in: query
          schema:
            type: string
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/coreweave.sandbox.v1.NetworkConfig'
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/coreweave.sandbox.v1.NetworkConfig'
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/google.rpc.Status'
      servers:
        - url: https://api.cwsandbox.com
components:
  schemas:
    coreweave.sandbox.v1.NetworkConfig:
      description: NetworkConfig is the desired network document a sandbox binds 1:1.
      type: object
      properties:
        networkConfigId:
          description: >-
            Immutable, organization-unique ID matching ^[a-z][a-z0-9-]{2,62}$.
            Choose the ID on CreateNetworkConfig, without the reserved nc-
            prefix. The platform assigns an nc- ID when it creates a
            configuration automatically for a sandbox.
          type: string
        spec:
          $ref: '#/components/schemas/coreweave.sandbox.v1.NetworkOptions'
        status:
          allOf:
            - $ref: '#/components/schemas/coreweave.sandbox.v1.NetworkConfigStatus'
          readOnly: true
        etag:
          description: >-
            Optional concurrency token. Send the last returned value in the
            NetworkConfig update body to protect a desired-state write. A
            mismatch on that write returns ABORTED with CWSANDBOX_ETAG_MISMATCH.
            A bound update whose resulting spec already matches stored desired
            state reapplies enforcement without checking the token. Omitting the
            token permits the last persisted desired-state write to win. The
            token does not make enforcement atomic.
          type: string
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
    coreweave.sandbox.v1.NetworkConfigStatus:
      type: object
      properties:
        sandboxId:
          description: >-
            Last bound sandbox. This field can briefly name a terminal sandbox
            until cleanup completes. A configuration is considered in use only
            while its bound sandbox exists and is non-terminal.
          type: string
          readOnly: true
        platformManaged:
          description: >-
            True when the platform created the configuration for a sandbox.
            Platform-managed configurations are deleted after that sandbox
            terminates. Caller-created configurations remain available for
            reuse.
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
