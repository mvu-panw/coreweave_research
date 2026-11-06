# Update cluster

Source: https://docs.coreweave.com/products/cks/reference/cks-api/clusterservice/update-cluster

# Update cluster

> Update selected fields on a CoreWeave CKS cluster using a field mask.

> [!NOTE]
>
> * The API server is `https://api.coreweave.com`.
> * Replace `{API_ACCESS_TOKEN}` with your [CoreWeave API access token](https://docs.coreweave.com/security/authn-authz/manage-api-access-tokens.md).
> * For required permissions, see [IAM Access Policies](https://docs.coreweave.com/security/iam/access-policies.md).

This method uses a field mask, provided in the `updateMask`
field, to specify which fields to modify. When `updateMask`
is omitted, all fields in the request body are updated. For
more information on field masks, see the
[Google AIP-157 guidance](https://google.aip.dev/157).

Required fields on every PATCH request body:

* `id`
* `version`

The following list of `updateMask` paths is derived from
`UpdateClusterRequest` in the upstream proto and from the
`update_request.json` fixture in the CKS API repository.

* `public`
* `version`
* `auditPolicy`
* `oidc` (and nested paths such as `oidc.issuerUrl`,
  `oidc.clientId`, `oidc.ca`)
* `authzWebhook` (and nested `authzWebhook.server`,
  `authzWebhook.ca`)
* `authnWebhook` (and nested `authnWebhook.server`,
  `authnWebhook.ca`)
* `network.internalLbCidrNames` (append-only)
* `network.serviceNodePortRange`
* `disableOidcInfoPublication`
* `kubelet`
* `additionalServerSans`
* `tailscale`
* `kubeApiAccess` (and nested paths such as `kubeApiAccess.public`)

To disable direct public Kubernetes API access, include
`kubeApiAccess` in `updateMask` and omit `kubeApiAccess` from
the request body. JSON field-mask paths use camelCase; this
is `kube_api_access` in the proto. Without an update mask,
omitting `kubeApiAccess` preserves the stored configuration.
Access updates require a `RUNNING` cluster and are processed
asynchronously. A successful PATCH response does not mean
the requested access policy is enforced.

```bash title="Example request" theme={"system"}
curl -X PATCH https://api.coreweave.com/v1beta1/cks/clusters/{id} \
       -H "Content-Type: application/json" \
       -H "Authorization: Bearer {API_ACCESS_TOKEN}" \
       -d @data.json
```

### Example: upgrade a cluster's Kubernetes version

To upgrade a cluster, set `version` to the new minor version
and include `version` in `updateMask`. See
[Upgrade Kubernetes](https://docs.coreweave.com/products/cks/clusters/upgrade-kubernetes.md)
for the end-to-end procedure.

```json title="data.json"
{
  "version": "v1.32",
  "updateMask": "version"
}
```


## OpenAPI

````yaml /openapi/cks/openapi.yaml patch /v1beta1/cks/clusters/{id}
openapi: 3.0.3
info:
  title: CoreWeave Kubernetes Service API
  version: 0.0.1
  description: >-
    The CKS API lets you create, list, get, update, and delete managed
    Kubernetes clusters on CoreWeave infrastructure.
servers:
  - url: https://api.coreweave.com
    description: CoreWeave production API.
security:
  - bearerAuth: []
tags:
  - name: ClusterService
    description: >-
      Endpoints for creating, listing, getting, updating, and deleting CoreWeave
      CKS clusters.
paths:
  /v1beta1/cks/clusters/{id}:
    patch:
      tags:
        - ClusterService
      summary: Update cluster
      description: Updates a CKS cluster by ID. Use `updateMask` to target specific fields.
      operationId: ClusterService_UpdateCluster
      parameters:
        - name: id
          in: path
          description: The ID of the cluster to update.
          required: true
          schema:
            type: string
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/UpdateClusterRequest'
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UpdateClusterResponse'
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Status'
components:
  schemas:
    UpdateClusterRequest:
      type: object
      properties:
        updateMask:
          description: >-
            A field mask specifying which fields to update. When omitted, all
            fields in the request body are updated. See the PATCH operation
            documentation for the preliminary list of valid paths and [Google
            AIP-157](https://google.aip.dev/157) for field-mask syntax.
          type: string
          format: field-mask
        id:
          description: The unique identifier for the cluster to update.
          type: string
        public:
          description: >-
            Whether legacy public ingress to the cluster's Kubernetes API server
            is enabled. This is independent of the direct public endpoint
            configured by `kubeApiAccess.public`.
          type: boolean
        version:
          description: >-
            The version of Kubernetes to run on the cluster, in minor version
            format (for example, `v1.32`). Patch versions are applied
            automatically by CKS as they are released.
          type: string
        oidc:
          description: >-
            OpenID Connect (OIDC) configuration for authentication to the
            api-server.
          allOf:
            - $ref: '#/components/schemas/OIDCConfig'
        authzWebhook:
          description: Authorization webhook configuration for the cluster.
          allOf:
            - $ref: '#/components/schemas/AuthWebhookConfig'
        authnWebhook:
          description: Authentication webhook configuration for the cluster.
          allOf:
            - $ref: '#/components/schemas/AuthWebhookConfig'
        auditPolicy:
          description: >-
            Audit policy for the cluster. Must be provided as a base64-encoded
            JSON or YAML string.
          type: string
        network:
          description: >-
            Mutable subset of the Kubernetes overlay network configuration. Only
            `internalLbCidrNames` and `serviceNodePortRange` may be updated.
          allOf:
            - $ref: '#/components/schemas/UpdateClusterRequest_Network'
        disableOidcInfoPublication:
          description: >-
            When `true`, suppresses publication of the
            `/.well-known/openid-configuration` and `/openid/v1/jwks` endpoints
            to `oidc.cks.coreweave.com/id/[CLUSTER-ID]`, so the cluster cannot
            be used as a public OIDC provider. Publishing these endpoints
            exposes the cluster's OIDC configuration and JWKS to the public
            Internet.
          type: boolean
        kubelet:
          description: >-
            A JSON object of selective overrides applied to every cluster Node's
            kubelet configuration. A Node reboot is required for changes to take
            effect. Unknown options are stored but ignored. See the [Kubernetes
            kubelet configuration
            reference](https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/)
            for supported options.
          type: object
        additionalServerSans:
          description: >-
            Up to 10 additional Subject Alternative Names to include on the
            Kubernetes API server certificate. Each entry must be unique.
          type: array
          items:
            type: string
        tailscale:
          description: Tailscale configuration for the cluster.
          allOf:
            - $ref: '#/components/schemas/Tailscale'
        kubeApiAccess:
          description: |-
            Configures external access to the cluster's Kubernetes API server.
             Legacy ingress is controlled separately by public.
             To disable access, include kube_api_access in the update mask and omit this field.
             Without an update mask, omitting this field preserves the stored configuration.
             Updates require a RUNNING cluster and are processed asynchronously. Processing
             can wait for operator readiness; there is no guaranteed enforcement deadline.
          allOf:
            - $ref: '#/components/schemas/KubeAPIAccess'
      required:
        - id
        - version
    UpdateClusterResponse:
      type: object
      properties:
        cluster:
          description: >-
            The cluster after the update is accepted for asynchronous
            processing.
             Success does not mean the requested policy is enforced. Configuration and
             observed access status can still describe the previous policy.
          allOf:
            - $ref: '#/components/schemas/Cluster'
    Status:
      description: >-
        Standard error response. `code` is a
        [`google.rpc.Code`](https://cloud.google.com/apis/design/errors#error_codes);
        `message` is human-readable English; `details` carries machine-readable
        error details when present.
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
            $ref: '#/components/schemas/GoogleProtobufAny'
    OIDCConfig:
      description: >-
        OpenID Connect (OIDC) configuration for authentication to the cluster's
        api-server. The whole object is optional on the cluster, but when
        supplied, `issuerUrl` and `clientId` are required within it.
      type: object
      properties:
        issuerUrl:
          description: >-
            The URL of the OIDC issuer. Required when `oidc` is configured on a
            cluster.
          type: string
        clientId:
          description: >-
            The client ID for the OIDC client. Required when `oidc` is
            configured on a cluster.
          type: string
        usernameClaim:
          description: The claim to use as the username.
          type: string
        usernamePrefix:
          description: The prefix to apply to the username.
          type: string
        groupsClaim:
          description: The claim to use as the groups.
          type: string
        groupsPrefix:
          description: The prefix to apply to the groups.
          type: string
        ca:
          description: >-
            The CA certificate for the OIDC issuer. Must be a base64-encoded
            PEM-encoded certificate.
          type: string
        requiredClaim:
          description: >-
            A claim that must be present on every token for authentication to
            succeed.
          type: string
        adminGroupBinding:
          description: >-
            Optional OIDC group name to bind to the cluster-admin RBAC role in
            the cluster.
          type: string
        signingAlgorithms:
          description: >-
            A list of signing algorithms that the OpenID Connect discovery
            endpoint uses.
          type: array
          items:
            type: string
      required:
        - issuerUrl
        - clientId
    AuthWebhookConfig:
      description: >-
        Configuration for an authentication or authorization webhook server used
        by the cluster's api-server. Each webhook (`authzWebhook`,
        `authnWebhook`) is optional on the cluster, but when supplied, `server`
        is required within it.
      type: object
      properties:
        server:
          description: >-
            The URL of the webhook server. Required when the webhook is
            configured on a cluster.
          type: string
        ca:
          description: >-
            The CA certificate for the webhook server. Must be a base64-encoded
            PEM-encoded certificate.
          type: string
      required:
        - server
    UpdateClusterRequest_Network:
      description: >-
        Mutable subset of the cluster's network configuration accepted by the
        PATCH endpoint.
      type: object
      properties:
        internalLbCidrNames:
          description: >-
            The names of the VPC prefixes to use as internal load balancer CIDR
            ranges. Internal load balancers are reachable within the VPC but not
            accessible from the Internet. The prefixes must exist in the
            cluster's VPC. This field is append-only.
          type: array
          items:
            type: string
        serviceNodePortRange:
          description: The range of ports to use for NodePort services.
          allOf:
            - $ref: '#/components/schemas/PortRange'
    Tailscale:
      description: Tailscale configuration for a cluster.
      type: object
      properties:
        clientId:
          description: Tailscale OAuth client ID. Maximum 255 characters.
          type: string
        tailnetDomain:
          description: The Tailscale tailnet DNS name assigned to this cluster.
          type: string
          readOnly: true
    KubeAPIAccess:
      description: |-
        Configures access to the cluster's Kubernetes API server.
         An absent public configuration leaves direct public access disabled.
         Legacy public ingress is controlled independently.
      type: object
      properties:
        public:
          description: >-
            Configures direct public access. A present configuration, including
            an empty
             object, enables the endpoint. An absent public configuration means direct public
             access is disabled. This does not affect legacy public ingress.
          allOf:
            - $ref: '#/components/schemas/PublicKubeAPIAccess'
    Cluster:
      description: A managed Kubernetes cluster running on CoreWeave infrastructure.
      type: object
      properties:
        id:
          description: The unique identifier for the cluster, assigned by the server.
          type: string
          readOnly: true
        name:
          description: >-
            The name of the cluster. Must be 1-30 characters and match the regex
            `^[a-z0-9]([-a-z0-9]*[a-z0-9])?$` (lowercase alphanumeric and
            hyphens; cannot start or end with a hyphen). Immutable once set.
          type: string
        zone:
          description: >-
            The [Availability
            Zone](https://docs.coreweave.com/platform/regions/about-regions-and-azs#complete-region-list)
            in which the cluster is located. Immutable once set.
          type: string
        vpcId:
          description: >-
            The ID of the VPC in which the cluster is located. The VPC must be
            in the same Availability Zone as the cluster. Immutable once set.
          type: string
        public:
          description: >-
            Whether legacy public ingress to the cluster's Kubernetes API server
            is enabled. This is independent of the direct public endpoint
            configured by `kubeApiAccess.public`.
          type: boolean
        version:
          description: >-
            The version of Kubernetes to run on the cluster, in minor version
            format (for example, `v1.32`). Patch versions are applied
            automatically by CKS as they are released.
          type: string
        network:
          description: The Kubernetes overlay network configuration for the cluster.
          allOf:
            - $ref: '#/components/schemas/ClusterNetworkConfig'
        oidc:
          description: >-
            OpenID Connect (OIDC) configuration for authentication to the
            api-server.
          allOf:
            - $ref: '#/components/schemas/OIDCConfig'
        authzWebhook:
          description: Authorization webhook configuration for the cluster.
          allOf:
            - $ref: '#/components/schemas/AuthWebhookConfig'
        authnWebhook:
          description: Authentication webhook configuration for the cluster.
          allOf:
            - $ref: '#/components/schemas/AuthWebhookConfig'
        auditPolicy:
          description: >-
            Audit policy for the cluster. Must be provided as a base64-encoded
            JSON or YAML string.
          type: string
        apiServerEndpoint:
          description: The endpoint for the cluster's api-server.
          type: string
          readOnly: true
        createdAt:
          description: The time the cluster was created.
          type: string
          format: date-time
          readOnly: true
        updatedAt:
          description: The time the cluster was last updated.
          type: string
          format: date-time
          readOnly: true
        isUpgradeable:
          description: >-
            Whether self-serve Kubernetes upgrades are currently supported for
            the cluster.
          type: boolean
          readOnly: true
        disableOidcInfoPublication:
          description: >-
            When `true`, suppresses publication of the
            `/.well-known/openid-configuration` and `/openid/v1/jwks` endpoints
            to `oidc.cks.coreweave.com/id/[CLUSTER-ID]`, so the cluster cannot
            be used as a public OIDC provider. Publishing these endpoints
            exposes the cluster's OIDC configuration and JWKS to the public
            Internet.
          type: boolean
        kubelet:
          description: >-
            A JSON object of selective overrides applied to every cluster Node's
            kubelet configuration. A Node reboot is required for changes to take
            effect. Unknown options are stored but ignored. See the [Kubernetes
            kubelet configuration
            reference](https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/)
            for supported options.
          type: object
        additionalServerSans:
          description: >-
            Up to 10 additional Subject Alternative Names to include on the
            Kubernetes API server certificate. Each entry must be unique.
          type: array
          items:
            type: string
        tailscale:
          description: Tailscale configuration for the cluster.
          allOf:
            - $ref: '#/components/schemas/Tailscale'
        kubeApiAccess:
          description: |-
            Configures external access to the cluster's Kubernetes API server.
             Legacy ingress is controlled separately by public.
          allOf:
            - $ref: '#/components/schemas/KubeAPIAccess'
        kubeApiAccessStatus:
          description: Details for Kubernetes API access paths.
          allOf:
            - $ref: '#/components/schemas/KubeAPIAccessStatus'
          readOnly: true
        status:
          description: The current status of the cluster.
          type: string
          readOnly: true
      required:
        - name
        - zone
        - vpcId
        - version
        - network
    GoogleProtobufAny:
      description: >-
        Contains an arbitrary serialized message along with a @type that
        describes the type of the serialized message.
      type: object
      properties:
        '@type':
          description: The type of the serialized message.
          type: string
      additionalProperties: true
    PortRange:
      description: >-
        An inclusive port range. `end` must be greater than or equal to `start`,
        and both must be in `1-65535`.
      type: object
      properties:
        start:
          description: The start of the range, inclusive. Must be between 1 and 65535.
          type: integer
          format: int32
        end:
          description: >-
            The end of the range, inclusive. Must be greater than or equal to
            `start` and at most 65535.
          type: integer
          format: int32
      required:
        - start
        - end
    PublicKubeAPIAccess:
      description: >-
        Configures a public endpoint that connects clients directly to the
        cluster's
         Kubernetes API server. CoreWeave-managed authentication is not currently supported.
         A present public configuration enables this endpoint; an absent configuration
         means direct public access is disabled.
         These CIDR rules apply only to the managed endpoint returned in status, not to legacy public ingress.
      type: object
      properties:
        allowCidrs:
          description: >-
            Up to 1024 IPv4 or IPv6 CIDR ranges permitted to access this direct
            public endpoint.
             An omitted or empty list allows all IPv4 and IPv6 sources, subject to deny_cidrs.
             A non-empty list denies sources that do not match any entry.
             To allow only IPv4 or only IPv6 sources, specify 0.0.0.0/0 or ::/0, respectively.
          type: array
          items:
            type: string
        denyCidrs:
          description: >-
            Up to 1024 IPv4 or IPv6 CIDR ranges excluded from this direct public
            endpoint.
             An omitted or empty list applies no exclusions. Deny ranges take precedence
             over allow_cidrs, including when they exclude every allowed address.
          type: array
          items:
            type: string
    ClusterNetworkConfig:
      description: >-
        The Kubernetes overlay network configuration for a cluster, including
        pod, service, and internal load balancer CIDR ranges.
      type: object
      properties:
        podCidrName:
          description: >-
            The name of the VPC prefix to use as the pod CIDR range. The prefix
            must exist in the cluster's VPC.
          type: string
        serviceCidrName:
          description: >-
            The name of the VPC prefix to use as the service CIDR range. The
            prefix must exist in the cluster's VPC.
          type: string
        internalLbCidrNames:
          description: >-
            The names of the VPC prefixes to use as internal load balancer CIDR
            ranges. Internal load balancers are reachable within the VPC but not
            accessible from the Internet. The prefixes must exist in the
            cluster's VPC. This field is append-only.
          type: array
          items:
            type: string
        serviceNodePortRange:
          description: The range of ports to use for NodePort services.
          allOf:
            - $ref: '#/components/schemas/PortRange'
      required:
        - podCidrName
        - serviceCidrName
        - internalLbCidrNames
    KubeAPIAccessStatus:
      description: |-
        Observed state of Kubernetes API access paths.
         After an update is accepted, this may still describe the previous configuration
         until asynchronous processing and observation persist a new status.
      type: object
      properties:
        public:
          description: Observed state of the managed public endpoint.
          allOf:
            - $ref: '#/components/schemas/PublicKubeAPIAccessStatus'
          readOnly: true
        caData:
          description: >-
            PEM-encoded certificate authority bundle for the cluster's
            Kubernetes API server.
             Raw PEM bytes in protobuf; base64-encoded in JSON. Omitted until collected.
          type: string
          format: bytes
          readOnly: true
    PublicKubeAPIAccessStatus:
      description: >-
        Observed endpoint and configuration acceptance for public Kubernetes API
        access.
      type: object
      properties:
        endpoint:
          description: >-
            Full HTTPS URL, including the external port, suitable for a
            kubeconfig server.
             Omitted until the endpoint is available.
          type: string
          readOnly: true
        status:
          description: >-
            Acceptance of the managed route and access policy is independent of
            endpoint presence. This does not indicate certificate readiness,
            end-to-end endpoint availability, or enforcement of traffic
            restrictions by every gateway. `STATUS_UNSPECIFIED` means no status
            was specified.
          type: string
          format: enum
          enum:
            - STATUS_UNSPECIFIED
            - STATUS_UNKNOWN
            - STATUS_PENDING
            - STATUS_ACCEPTED
            - STATUS_REJECTED
            - STATUS_ERROR
          readOnly: true
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
      description: CoreWeave API access token sent as a bearer token.
      x-default: Bearer {API_ACCESS_TOKEN}

````
